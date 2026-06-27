"""registry_tools.py — 레지스트리 1급 자료구조화 (외부 리뷰 R-G 대응).

레지스트리를 의존 DAG로 모델링하고 manifest/그래프/root hash를 자동 생성한다.
리뷰 결함: flat 54+ 파일, 의존 DAG·revocation·manifest·root hash 부재, cached vs canonical 미구분.

생성물:
  registry/DEPENDENCY-GRAPH.json   — 각 app → 의존 모듈/서브앱 (child u_hash 포함)
  registry/DEPENDENCY-GRAPH.md     — 사람용 트리
  registry/REGISTRY-MANIFEST.json  — 분류(modules/unique-apps/cached) + root hash + revocation 슬롯

사용:
  python scripts/registry_tools.py build           # 그래프+manifest 생성
  python scripts/registry_tools.py dependents <id> # blast-radius: 해당 모듈/앱에 의존하는 전부
"""
import os, sys, json, re, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
APPS = os.path.join(ROOT, "specs", "apps")
MODSPEC = os.path.join(ROOT, "specs", "modules")
MODREG = os.path.join(ROOT, "registry", "modules")
APPREG = os.path.join(ROOT, "registry", "apps")
REG = os.path.join(ROOT, "registry")


def _uhash(path):
    return json.load(open(path, encoding="utf-8"))["u_hash"] if os.path.exists(path) else None


def parse_plan_deps(app_pg_path):
    """app .pg 의 plan 블록 → 의존 (kind, id) 리스트."""
    src = open(app_pg_path, encoding="utf-8").read()
    m = re.search(r"```json id=plan\n(.*?)```", src, re.S)
    if not m:
        return []
    plan = json.loads(m.group(1))
    deps = []
    for step in plan.get("steps", []):
        if "spec" in step:
            deps.append(("module", os.path.basename(step["spec"])[:-3]))
        elif "app" in step:
            deps.append(("app", step["app"][:-7]))
    return deps


def build_graph():
    apps = sorted(f[:-7] for f in os.listdir(APPS) if f.endswith(".app.pg"))
    graph = {}
    for app in apps:
        deps = parse_plan_deps(os.path.join(APPS, f"{app}.app.pg"))
        # 중복 제거 + 카운트
        counts = {}
        for kind, did in deps:
            counts[(kind, did)] = counts.get((kind, did), 0) + 1
        edges = []
        for (kind, did), n in sorted(counts.items()):
            reg = MODREG if kind == "module" else APPREG
            edges.append({"kind": kind, "id": did, "uses": n,
                          "child_u_hash": _uhash(os.path.join(reg, f"{did}.sealed.json"))})
        app_uh = _uhash(os.path.join(APPREG, f"{app}.sealed.json"))
        graph[app] = {"u_hash": app_uh, "depends_on": edges}
    return graph


def render_tree(graph):
    """app → 의존 트리(서브앱 재귀)를 ASCII 로."""
    lines = []

    def walk(node, prefix, seen):
        info = graph.get(node)
        if not info:
            return
        deps = info["depends_on"]
        for i, e in enumerate(deps):
            last = i == len(deps) - 1
            branch = "└─ " if last else "├─ "
            lines.append(f"{prefix}{branch}{e['id']} ({e['kind']}{'×' + str(e['uses']) if e['uses'] > 1 else ''})")
            if e["kind"] == "app" and e["id"] not in seen:
                walk(e["id"], prefix + ("   " if last else "│  "), seen | {e["id"]})

    # 최상위(다른 앱의 의존에 안 나오는) 앱부터
    child_apps = {e["id"] for g in graph.values() for e in g["depends_on"] if e["kind"] == "app"}
    roots = [a for a in graph if a not in child_apps]
    for r in sorted(roots):
        lines.append(f"{r}")
        walk(r, "", {r})
        lines.append("")
    return "\n".join(lines)


def build_manifest(graph):
    mods = sorted(f[:-12] for f in os.listdir(MODREG) if f.endswith(".sealed.json"))
    app_files = sorted(f[:-12] for f in os.listdir(APPREG) if f.endswith(".sealed.json"))
    unique_apps = [a for a in app_files if os.path.exists(os.path.join(APPS, f"{a}.app.pg"))]
    cached = [a for a in app_files if a not in unique_apps]  # 모듈 재봉인 캐시 (app_assemble 산물)
    # root hash = 정렬된 (id:u_hash) 의 sha256
    items = []
    for mid in mods:
        items.append(f"module:{mid}:{_uhash(os.path.join(MODREG, mid + '.sealed.json'))}")
    for aid in unique_apps:
        items.append(f"app:{aid}:{_uhash(os.path.join(APPREG, aid + '.sealed.json'))}")
    root = hashlib.sha256("\n".join(sorted(items)).encode()).hexdigest()
    return {
        "schema": "registry-manifest/v1",
        "modules": {"count": len(mods), "path": "registry/modules", "items": mods},
        "apps": {"unique_app_count": len(unique_apps), "cached_app_side_module_count": len(cached),
                 "total_files": len(app_files), "path": "registry/apps",
                 "unique": unique_apps, "cached_leaf_modules": cached},
        "cached_canonical_map": {c: f"registry/modules/{c}.sealed.json" for c in cached},
        "registry_root_hash": root,
        "revocation_list": [],
        "note": "cached_leaf_modules 는 app_assemble 가 모듈 로드 시 app store 에 남긴 재봉인. canonical 은 registry/modules. "
                "단일 출처 검증은 registry_root_hash 로, 영향범위는 dependents 로 계산."
    }


def dependents(graph, target):
    """target(module/app)에 (재귀적으로) 의존하는 모든 app — revocation blast radius."""
    direct = {app for app, g in graph.items() if any(e["id"] == target for e in g["depends_on"])}
    out = set(direct)
    changed = True
    while changed:
        changed = False
        for app, g in graph.items():
            if app in out:
                continue
            if any(e["kind"] == "app" and e["id"] in out for e in g["depends_on"]):
                out.add(app); changed = True
    return sorted(out)


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "build"
    graph = build_graph()
    if cmd == "dependents":
        target = sys.argv[2]
        deps = dependents(graph, target)
        print(f"'{target}' 에 의존(blast radius) {len(deps)}개 app: {deps}")
        return 0
    # build
    json.dump(graph, open(os.path.join(REG, "DEPENDENCY-GRAPH.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    open(os.path.join(REG, "DEPENDENCY-GRAPH.md"), "w", encoding="utf-8", newline="\n").write(
        "# Registry Dependency Graph (auto-generated by scripts/registry_tools.py)\n\n```text\n"
        + render_tree(graph) + "```\n")
    man = build_manifest(graph)
    json.dump(man, open(os.path.join(REG, "REGISTRY-MANIFEST.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(f"DEPENDENCY-GRAPH.json: {len(graph)} apps")
    print(f"REGISTRY-MANIFEST.json: modules={man['modules']['count']} unique_apps={man['apps']['unique_app_count']} "
          f"cached={man['apps']['cached_app_side_module_count']} root={man['registry_root_hash'][:16]}..")
    return 0


if __name__ == "__main__":
    sys.exit(main())
