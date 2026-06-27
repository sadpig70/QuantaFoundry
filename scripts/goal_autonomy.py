"""goal_autonomy.py — 목표 자율(Goal Autonomy) MVP (외부 리뷰 R-C / F-10 대응).

리뷰 결함: 시스템이 "무엇을 만들지"를 못 정한다(인간이 intent 큐잉). "비선형 생산성" 주장 데이터 0.
이 모듈은 registry 의존그래프를 스캔해 (1) composable gap 자율 탐지 (2) 가치 점수화
(3) 최고점 후보 자동 봉인(human seed 0) (4) compounding curve 측정 — self-growing foundry 본체.

honest: 새 진리를 발명하지 않는다. 이미 봉인된 부품의 *알려진 합성 규칙*(family extension)으로
다음 빌드 타깃을 시스템이 스스로 고른다. 인간 seed 0, 봉인 게이트만 재조립(no MatrixGate).

사용:
  python scripts/goal_autonomy.py scan      # gap 탐지 + 점수화 (빌드 안 함)
  python scripts/goal_autonomy.py forge      # 최고점 app-gap 자동 생성 + 봉인
  python scripts/goal_autonomy.py compound   # compounding curve 측정
"""
import os, sys, json, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts"))
sys.path.insert(0, HERE)   # genskills (생성-스킬 라이브러리) 동거 디렉터리
APPS = os.path.join(ROOT, "specs", "apps")
MODREG = os.path.join(ROOT, "registry", "modules")
APPREG = os.path.join(ROOT, "registry", "apps")
REG = os.path.join(ROOT, "registry")

# 생성 *방법* 은 genskills 라이브러리(1급 자산)에서 가져온다 — goal_autonomy 는 그 소비자.
# (이전엔 gen_ghz/gen_cluster 가 여기 박혀 있었음; §5[8](A) 로 라이브러리화)
from genskills import gen_ghz, gen_cluster


def sealed_apps():
    return set(f[:-7] for f in os.listdir(APPS) if f.endswith(".app.pg"))


def sealed_modules():
    return set(f[:-12] for f in os.listdir(MODREG) if f.endswith(".sealed.json"))


# ── family 레지스트리 ──
#   deps_fn(n): member n 빌드에 필요한 *봉인 모듈* id. gen(n): spec 생성(없으면 forge 불가, 탐지만).
#   seed: 멤버 0개일 때 bootstrap 시작 n(새 family 자율 시작). gatecount(n): 난이도(게이트 수) 추정.
FAMILIES = {
    "ghz": {"gen": gen_ghz, "deps_fn": lambda n: ["h_gate", "cnot"], "algo_value": 0.6,
            "pattern": re.compile(r"^ghz(\d+)$"), "kind": "entangling scaling (GHZ)",
            "seed": 3, "gatecount": lambda n: n},
    "cluster": {"gen": gen_cluster, "deps_fn": lambda n: ["h_gate", "cz"], "algo_value": 0.55,
                "pattern": re.compile(r"^cluster(\d+)$"), "kind": "1D cluster state (MBQC resource)",
                "seed": 3, "gatecount": lambda n: 2 * n - 1},
    # blocked family(정직 탐지): W-state 는 parametrized Ry primitive 가 선행 필요 — 미봉인 → buildable=False.
    "wstate": {"gen": None, "deps_fn": lambda n: ["ry_gate", "cnot", "x_gate"], "algo_value": 0.5,
               "pattern": re.compile(r"^wstate(\d+)$"), "kind": "W-state (needs Ry primitive — blocked)",
               "seed": 3, "gatecount": lambda n: 3 * n},
}

MAX_N = 10   # 자율 확장 상한(dense 2^10=1024; EXACT_BOUND=12 이내 안전)


def _candidate_ns(members, seed):
    """제안할 n 목록: 멤버 있으면 (내부 누락 [min..max] + 다음 2개), 없으면 bootstrap(seed, seed+1)."""
    if not members:
        return [seed, seed + 1]
    mn, mx = min(members), max(members)
    interior = [k for k in range(mn, mx) if k not in members]   # 중간 빠진 멤버
    nxt = [mx + 1, mx + 2]
    return [k for k in interior + nxt if k <= MAX_N]


def detect_gaps():
    apps = sealed_apps()
    mods = sealed_modules()
    gaps = []
    for fam, cfg in FAMILIES.items():
        members = sorted(int(m.group(1)) for a in apps if (m := cfg["pattern"].match(a)))
        for nxt in _candidate_ns(members, cfg["seed"]):
            cand_id = f"{fam}{nxt}"
            if cand_id in apps:
                continue
            required = cfg["deps_fn"](nxt)
            missing = [d for d in required if d not in mods]
            buildable = (not missing) and (cfg["gen"] is not None)
            gaps.append({"id": cand_id, "family": fam, "n": nxt, "buildable": buildable,
                         "required_modules": required, "missing_modules": missing,
                         "forgeable": cfg["gen"] is not None,
                         "bootstrap": not members, "algo_value": cfg["algo_value"],
                         "gate_count": cfg["gatecount"](nxt), "kind": cfg["kind"]})
    return gaps


def score(gap):
    """가치 점수 = 재사용성 × 알고리즘가치 × (1/난이도). 봉인부품 전원확보 → 재사용성 1.0, 아니면 0."""
    reuse = 1.0 if gap["buildable"] else 0.0
    difficulty = max(1, gap["gate_count"]) / 4.0          # 게이트 수 정규화
    return round(reuse * gap["algo_value"] * (1.0 / difficulty), 4)


def cmd_scan():
    gaps = detect_gaps()
    ranked = sorted(({**g, "score": score(g)} for g in gaps), key=lambda x: -x["score"])
    print("=" * 78)
    print("goal-autonomy SCAN — registry 의존그래프 기반 composable gap 자율 탐지")
    print("=" * 78)
    for g in ranked:
        tag = "BUILD" if g["buildable"] else ("BLOCKED" if g["missing_modules"] else "no-gen")
        boot = " [bootstrap]" if g.get("bootstrap") else ""
        extra = f" missing={g['missing_modules']}" if g["missing_modules"] else f" reuse={g['required_modules']}"
        print(f"  {g['score']:.4f}  {g['id']:10} {tag:7}{extra} v={g['algo_value']} ({g['kind']}){boot}")
    print("=" * 78)
    n_build = sum(1 for g in ranked if g["buildable"])
    fams = sorted({g["family"] for g in ranked})
    print(f"탐지 {len(ranked)} gap · buildable {n_build} · families {fams} · 최고점 = {ranked[0]['id'] if ranked else 'none'}")
    json.dump(ranked, open(os.path.join(ROOT, ".pgf", "autoforge", "GOAL-SCAN.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    return ranked


def cmd_forge():
    import app_assemble as aa
    ranked = [g for g in (dict(g, score=score(g)) for g in detect_gaps()) if g["buildable"]]
    ranked.sort(key=lambda x: -x["score"])
    if not ranked:
        print("자율 빌드 후보 없음."); return 1
    print("=" * 78)
    print("goal-autonomy FORGE — 최고점 후보 자동 생성·봉인 (human seed 0)")
    print("=" * 78)
    forged = []
    # 최고 가치 패밀리의 다음 2개 멤버까지 자율 봉인 (compounding 실증)
    for g in ranked:
        gen = FAMILIES[g["family"]]["gen"]
        spec, _ = gen(g["n"])
        sp = os.path.join(APPS, f"{g['id']}.app.pg")
        open(sp, "w", encoding="utf-8", newline="\n").write(spec)
        v = aa.assemble(sp, APPREG)
        ok = v.sealed
        print(f"  {'✅' if ok else '❌'} {g['id']:10} {'SEALED' if ok else 'REJECT'} "
              f"tier={v.tier} u_hash={v.u_hash[:14] if ok else ''}.. score={g['score']}")
        forged.append({"id": g["id"], "sealed": ok, "u_hash": v.u_hash if ok else None, "score": g["score"]})
        if not ok:
            os.remove(sp)
    print("=" * 78)
    n_ok = sum(1 for f in forged if f["sealed"])
    print(f"자율 봉인 {n_ok}/{len(forged)} · 인간 seed 0 · 새 모듈 0 (순수 재조립)")
    json.dump(forged, open(os.path.join(ROOT, ".pgf", "autoforge", "GOAL-FORGE-RESULT.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    return 0 if n_ok == len(forged) else 1


def cmd_compound():
    """compounding curve: registry 부품이 만든 app 수 / 재사용 배수 — 비선형 생산성 실증(F-10)."""
    graph = json.load(open(os.path.join(REG, "DEPENDENCY-GRAPH.json"), encoding="utf-8"))
    mods = sealed_modules()
    apps = sealed_apps()
    # 모듈별 재사용 횟수(앱이 직접 참조한 횟수, 가중)
    reuse = {}
    for app, info in graph.items():
        for e in info["depends_on"]:
            if e["kind"] == "module":
                reuse[e["id"]] = reuse.get(e["id"], 0) + 1
    total_reuse = sum(reuse.values())
    # family 별 compounding 자동 집계: 봉인 멤버 수, base 모듈, marginal new-module 비용.
    fam_compound = {}
    for fam, cfg in FAMILIES.items():
        members = sorted(int(m.group(1)) for a in apps if (m := cfg["pattern"].match(a)))
        base = sorted(set().union(*[set(cfg["deps_fn"](k)) for k in members])) if members else \
            sorted(set(cfg["deps_fn"](cfg["seed"])))
        all_base_sealed = all(b in mods for b in base)
        fam_compound[fam] = {
            "members": members, "n_members": len(members), "base_modules": base,
            "base_all_sealed": all_base_sealed,
            "marginal_new_module_cost": 0 if (all_base_sealed and members) else len([b for b in base if b not in mods]),
            "status": "compounding" if (members and all_base_sealed) else
                      ("blocked(missing primitive)" if not all_base_sealed else "dormant(no members)"),
            "kind": cfg["kind"]}
    # 부품→앱 레버리지: 봉인 모듈 1개가 평균 몇 앱에 재사용되나
    leverage = round(total_reuse / max(1, len(mods)), 2)
    result = {
        "sealed_modules": len(mods),
        "sealed_apps": len(apps),
        "total_module_reuse_instances": total_reuse,
        "avg_reuse_per_app": round(total_reuse / max(1, len(apps)), 2),
        "module_leverage(apps_per_module)": leverage,
        "top_reused": dict(sorted(reuse.items(), key=lambda x: -x[1])[:5]),
        "family_compounding": fam_compound,
        "compounding_thesis": "고정된 소수 봉인 모듈이 family-extension 으로 무한 멤버를 O(1) marginal "
                              "(new-module 비용 0)로 생성 → 비선형 생산성. goal-autonomy 가 그 확장을 자율 선택.",
        "honest_note": "선형 수동 조립과 구분되는 비선형 신호는 family-extension/goal-autonomy 자동 발견에 있다. "
                       "compounding family 가 늘수록(ghz·cluster…) 동일 base 재사용 레버리지가 증가."
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    json.dump(result, open(os.path.join(ROOT, ".pgf", "autoforge", "COMPOUNDING-CURVE.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    return 0


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "scan"
    r = {"scan": cmd_scan, "forge": cmd_forge, "compound": cmd_compound}.get(cmd, cmd_scan)()
    return r if isinstance(r, int) else 0


if __name__ == "__main__":
    sys.exit(main())
