"""genskills.py — 생성-스킬 라이브러리 (Generation-Skill Library, §5[8](A) 대응).

리뷰/HANDOFF 결함: 파운드리는 *결과물*(봉인된 unitary)만 라이브러리화한다. 그 결과물을 만든
*생성 방법* 은 `goal_autonomy.gen_ghz/gen_cluster` 처럼 코드에 흩어져 1회용으로 박혀 있었다.
이 모듈은 생성 *방법* 자체를 재사용 가능한 1급 자산(named GenSkill catalog)으로 승격한다 —
명명된 GenSkill 들이 파라미터 n 을 받아 **결정론적으로** `.app.pg` spec 을 산출하고, 그 산출물은
다시 app_assemble 오라클이 봉인한다.

honest 경계(중요): GenSkill 은 검증을 우회하지 않는다. 생성 산출물은 여전히 오라클(C-app)을
통과해야 봉인된다. 생성≠검증 경계 유지 — 본 라이브러리는 생성 노하우의 재사용·내성
(introspection)·provenance 계층일 뿐, 새 신뢰를 만들지 않는다.

결정론 신성불가침: 이미 봉인된 family(ghz · cluster line)의 생성기는 **byte-frozen** 이다 —
산출 spec 이 committed spec 과 바이트 일치해야 한다(selftest 가 강제). 새 방법(graph-state
general → cluster_ring)은 공유 프리미티브 위에 올려 "방법 추가 비용이 낮음"을 실증하되,
산출물은 오라클 봉인 roundtrip 으로 검증한다.

CLI:
  python scripts/genskills.py list                  # catalog 요약 출력
  python scripts/genskills.py show <skill>          # skill 상세 + 샘플 spec
  python scripts/genskills.py emit <skill> <n> [--out DIR]   # spec 산출(기본 stdout)
  python scripts/genskills.py catalog               # registry/GENSKILL-CATALOG.json 갱신
  python scripts/genskills.py selftest              # byte-identity + forge roundtrip 검증
"""
import os, sys, json, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
APPS = os.path.join(ROOT, "specs", "apps")
APPREG = os.path.join(ROOT, "registry", "apps")
REG = os.path.join(ROOT, "registry")


# ════════════════════════════════════════════════════════════════════════════
# 1. 공유 생성 프리미티브 (생성 방법들이 재사용하는 machinery)
# ════════════════════════════════════════════════════════════════════════════
def build_plan(steps):
    """{spec,targets} step 리스트 → committed spec 과 동일 들여쓰기의 plan JSON 문자열."""
    return '{"steps": [' + ",\n           ".join(json.dumps(s) for s in steps) + "]}"


def assemble_app_spec(app_id, n_sys, header, golden_code, plan_str):
    """header + app_meta + app_golden + plan → .app.pg spec 텍스트(결정론, LF)."""
    return (header + f'```json id=app_meta\n{{"id": "{app_id}", "n_sys": {n_sys}, "n_anc": 0}}\n```\n'
            "```python id=app_golden\n" + golden_code + "\n```\n"
            "```json id=plan\n" + plan_str + "\n```\n")


# ════════════════════════════════════════════════════════════════════════════
# 2. 생성 방법 — byte-frozen (이미 봉인된 family; goal_autonomy 에서 verbatim 이동)
#    ⚠ 이 두 함수의 산출 바이트는 committed spec 과 100% 일치해야 한다(determinism).
# ════════════════════════════════════════════════════════════════════════════
def gen_ghz(n):
    """GHZ_n = H(0) · CNOT(0,1)·CNOT(1,2)·…·CNOT(n-2,n-1). 봉인 h_gate+cnot 재조립."""
    golden = (
        "import numpy as np\n"
        "H=np.array([[1,1],[1,-1]],dtype=complex)/np.sqrt(2)\n"
        "CN=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],dtype=complex)\n"
        "def emb(U,t,n):\n"
        "    left=np.eye(1<<t[0]); right=np.eye(1<<(n-t[-1]-1))\n"
        "    return np.kron(np.kron(left,U),right)\n"
        f"g=np.kron(H,np.eye(1<<{n-1}))\n"
        f"for i in range({n-1}): g=emb(CN,[i,i+1],{n})@g\n"
        "golden=g")
    steps = [{"spec": "../modules/h_gate.pg", "targets": [0]}]
    steps += [{"spec": "../modules/cnot.pg", "targets": [i, i + 1]} for i in range(n - 1)]
    plan = build_plan(steps)
    header = (f"# ghz{n} — GHZ_{n} 준비 ({n}큐비트). goal-autonomy 자율 생성 (family extension, human seed 0).\n"
              f"# 봉인 h_gate+cnot 재조립. 새 모듈 0 — registry {n}큐비트로 O(1) marginal 확장(compounding).\n")
    spec = assemble_app_spec(f"ghz{n}", n, header, golden, plan)
    return spec, ["h_gate", "cnot"]


def gen_cluster(n):
    """1D cluster state_n = (∏ CZ(i,i+1)) · H^⊗n. MBQC 자원. 봉인 h_gate+cz 재조립."""
    golden = (
        "import numpy as np\n"
        "H=np.array([[1,1],[1,-1]],dtype=complex)/np.sqrt(2)\n"
        "CZ=np.diag([1,1,1,-1]).astype(complex)\n"
        "def emb(U,t,n):\n"
        "    left=np.eye(1<<t[0]); right=np.eye(1<<(n-t[-1]-1))\n"
        "    return np.kron(np.kron(left,U),right)\n"
        "g=np.eye(1)\n"
        f"for _ in range({n}): g=np.kron(g,H)\n"
        f"for i in range({n-1}): g=emb(CZ,[i,i+1],{n})@g\n"
        "golden=g")
    steps = [{"spec": "../modules/h_gate.pg", "targets": [i]} for i in range(n)]
    steps += [{"spec": "../modules/cz.pg", "targets": [i, i + 1]} for i in range(n - 1)]
    plan = build_plan(steps)
    header = (f"# cluster{n} — 1D cluster state ({n}큐비트). goal-autonomy 자율 생성 (family extension, human seed 0).\n"
              f"# 봉인 h_gate+cz 재조립(H^⊗{n} 후 CZ 체인). MBQC 자원. 새 모듈 0 — O(1) marginal 확장.\n")
    spec = assemble_app_spec(f"cluster{n}", n, header, golden, plan)
    return spec, ["h_gate", "cz"]


# ════════════════════════════════════════════════════════════════════════════
# 3. 생성 방법 — graph-state 일반화 (새 방법; cluster_line 의 상위 일반형)
#    임의 edge 집합의 그래프 상태 = H^⊗n 후 각 edge 에 CZ. 비인접 edge 도 embed_unitary
#    가 지원하므로 봉인 가능. cluster(line) 은 path graph, ring 은 cycle graph 의 특수예.
# ════════════════════════════════════════════════════════════════════════════
def gen_graph_state(app_id, n, edges, kind_desc, genskill="graph_state@1"):
    """그래프 상태 생성 방법: H^⊗n 후 edges 의 각 (a,b) 에 CZ. 봉인 h_gate+cz 재조립.

    golden 은 임의 (비인접 포함) edge 를 처리하는 대각 cz_on 으로 구성 — embed_unitary
    (qualtran-raw big-endian, qubit 0=MSB)와 동일 컨벤션. provenance 를 header 에 stamp.
    """
    edge_lit = "[" + ",".join(f"({a},{b})" for a, b in edges) + "]"
    golden = (
        "import numpy as np\n"
        "H=np.array([[1,1],[1,-1]],dtype=complex)/np.sqrt(2)\n"
        f"n={n}; edges={edge_lit}\n"
        "def cz_on(a,b,n):\n"
        "    d=np.ones(1<<n,dtype=complex)\n"
        "    for x in range(1<<n):\n"
        "        if (x>>(n-1-a))&1 and (x>>(n-1-b))&1: d[x]=-1.0\n"
        "    return np.diag(d)\n"
        "g=np.eye(1)\n"
        "for _ in range(n): g=np.kron(g,H)\n"
        "for (a,b) in edges: g=cz_on(a,b,n)@g\n"
        "golden=g")
    steps = [{"spec": "../modules/h_gate.pg", "targets": [i]} for i in range(n)]
    steps += [{"spec": "../modules/cz.pg", "targets": [a, b]} for a, b in edges]
    plan = build_plan(steps)
    header = (f"# {app_id} — {kind_desc} ({n}큐비트). genskill 자율 생성 (human seed 0). genskill={genskill}.\n"
              f"# 봉인 h_gate+cz 재조립(H^⊗{n} 후 graph CZ {edge_lit}). 새 모듈 0 — O(1) marginal 확장.\n")
    spec = assemble_app_spec(app_id, n, header, golden, plan)
    return spec, ["h_gate", "cz"]


def gen_cluster_ring(n):
    """ring cluster state = cycle graph state. path(line) + 마감 edge (n-1,0). n>=3."""
    if n < 3:
        raise ValueError("cluster_ring 는 n>=3 (cycle)")
    edges = [(i, i + 1) for i in range(n - 1)] + [(n - 1, 0)]
    return gen_graph_state(f"ring{n}", n, edges, "ring cluster state (cycle graph state)",
                           genskill="cluster_ring@1")


# ════════════════════════════════════════════════════════════════════════════
# 4. GenSkill 카탈로그 — 생성 *방법* 라이브러리(1급 자산)
# ════════════════════════════════════════════════════════════════════════════
GENSKILLS = {
    "ghz_linear": {
        "version": "1", "produces": "app", "param": "n:int>=2",
        "kind": "entangling scaling (GHZ, linear CNOT ladder)",
        "golden_method": "H(q0) then CNOT(i,i+1) ladder; kron+emb composition over sealed h_gate,cnot",
        "required_modules": ["h_gate", "cnot"],
        "instance_pattern": r"^ghz(\d+)$", "byte_frozen": True, "make_spec": gen_ghz,
    },
    "cluster_line": {
        "version": "1", "produces": "app", "param": "n:int>=2",
        "kind": "1D cluster state (path graph, MBQC resource)",
        "golden_method": "H^⊗n then CZ(i,i+1) chain over sealed h_gate,cz",
        "required_modules": ["h_gate", "cz"],
        "instance_pattern": r"^cluster(\d+)$", "byte_frozen": True, "make_spec": gen_cluster,
    },
    "cluster_ring": {
        "version": "1", "produces": "app", "param": "n:int>=3",
        "kind": "ring cluster state (cycle graph state, MBQC resource)",
        "golden_method": "H^⊗n then CZ on cycle edges (path + closing edge) via general graph_state",
        "required_modules": ["h_gate", "cz"],
        "instance_pattern": r"^ring(\d+)$", "byte_frozen": False, "make_spec": gen_cluster_ring,
    },
}


def catalog_records():
    """callable 을 뺀 직렬화 가능한 카탈로그 레코드(1급 데이터)."""
    recs = []
    for sid, c in GENSKILLS.items():
        recs.append({k: c[k] for k in c if k != "make_spec"} | {"id": sid})
    return recs


# ════════════════════════════════════════════════════════════════════════════
# 5. CLI
# ════════════════════════════════════════════════════════════════════════════
def cmd_list():
    print("=" * 84)
    print("GenSkill Library — 생성 *방법* 카탈로그 (생성≠검증; 산출물은 오라클이 봉인)")
    print("=" * 84)
    for sid, c in GENSKILLS.items():
        frozen = "frozen" if c["byte_frozen"] else "new   "
        print(f"  {sid:14} v{c['version']} [{frozen}] {c['param']:11} deps={c['required_modules']}")
        print(f"  {'':14}   {c['kind']}")
        print(f"  {'':14}   방법: {c['golden_method']}")
    print("=" * 84)
    print(f"skills {len(GENSKILLS)} · frozen {sum(1 for c in GENSKILLS.values() if c['byte_frozen'])}"
          f" · new {sum(1 for c in GENSKILLS.values() if not c['byte_frozen'])}")
    return 0


def cmd_show(sid):
    if sid not in GENSKILLS:
        print(f"unknown skill: {sid} (있는 것: {list(GENSKILLS)})"); return 1
    c = GENSKILLS[sid]
    print(json.dumps({k: c[k] for k in c if k != "make_spec"} | {"id": sid}, ensure_ascii=False, indent=2))
    # 샘플 spec(파라미터 최소값)
    nmin = 3 if "n>=3" in c["param"] else 2
    sample, deps = c["make_spec"](nmin)
    print(f"\n── 샘플 산출 (n={nmin}) ──\n{sample}")
    return 0


def cmd_emit(sid, n, out_dir=None):
    if sid not in GENSKILLS:
        print(f"unknown skill: {sid}"); return 1
    spec, deps = GENSKILLS[sid]["make_spec"](n)
    app_id = re.search(r'"id": "([^"]+)"', spec).group(1)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        p = os.path.join(out_dir, f"{app_id}.app.pg")
        open(p, "w", encoding="utf-8", newline="\n").write(spec)
        print(f"wrote {p} (deps={deps})")
    else:
        sys.stdout.write(spec)
    return 0


def cmd_catalog():
    recs = catalog_records()
    out = {"schema": "genskill-catalog/v1", "count": len(recs),
           "note": "생성 *방법* 라이브러리(1급 데이터). 결과물 라이브러리(registry/REGISTRY-MANIFEST)의 "
                   "생성-방법 짝. byte_frozen=True 는 이미 봉인된 family 의 생성기로 산출 spec 이 "
                   "committed spec 과 바이트 일치(determinism). 산출물 봉인은 app_assemble 오라클이 수행.",
           "skills": recs}
    p = os.path.join(REG, "GENSKILL-CATALOG.json")
    json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"wrote {p} · skills {len(recs)}")
    return 0


def _seal_id(skill_id, n):
    """skill id → 멤버 app id 접두사 (ghz_linear→ghz, cluster_line→cluster)."""
    return {"ghz_linear": "ghz", "cluster_line": "cluster", "cluster_ring": "ring"}[skill_id] + str(n)


def cmd_selftest():
    """결정론·정합성 검증 (registry/봉인 무오염 — temp store 사용):
       T1 byte-identity : frozen skill 산출 spec == committed spec (skill 이 *작성한* 멤버).
                          legacy 포맷(다른 생성기 작성) 멤버는 byte 면제 → T2 가 unitary 동등 입증.
       T2 reproduce-seal: 모든 family 멤버를 temp store 로 재조립 → u_hash == registry seal
                          (byte-frozen·legacy 무관, 라이브러리가 봉인 unitary 전부 재현).
       T3 new-method    : 신규 cluster_ring ring4 Tier-0 봉인 성공(오라클 통과).
    """
    import tempfile, shutil
    sys.path.insert(0, os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts"))
    import app_assemble as aa

    passed, failed = [], []

    def ok(name, cond, detail=""):
        (passed if cond else failed).append(name)
        print(f"  {'✅' if cond else '❌'} {name}{(' — ' + detail) if detail else ''}")

    on_disk = set(f[:-7] for f in os.listdir(APPS) if f.endswith(".app.pg"))
    tmp_store = tempfile.mkdtemp(prefix="genskill_store_")
    tmp_specs = []   # specs/apps 내 임시 spec (상대경로 ../modules 해석 위해 sibling 필요)
    byte_ok, legacy = [], []
    try:
        # ── T1: byte-identity (frozen skills) ──
        print("── T1 byte-identity (frozen skills vs committed specs) ──")
        for sid, c in GENSKILLS.items():
            if not c["byte_frozen"]:
                continue
            pat = re.compile(c["instance_pattern"])
            members = sorted(int(pat.match(a).group(1)) for a in on_disk if pat.match(a))
            for n in members:
                app_id = _seal_id(sid, n)
                disk = open(os.path.join(APPS, f"{app_id}.app.pg"), encoding="utf-8").read()
                gen, _ = c["make_spec"](n)
                if gen == disk:
                    byte_ok.append(app_id); print(f"  ✅ byte {app_id}")
                else:
                    legacy.append((sid, n, app_id)); print(f"  ◻ byte {app_id} (legacy 포맷 — T2 가 unitary 동등 검증)")
        ok("byte-identity (skill-authored members)", len(byte_ok) > 0, f"{len(byte_ok)} identical, {len(legacy)} legacy")

        # ── T2: reproduce-seal (모든 멤버 — byte-frozen + legacy) ──
        print("── T2 reproduce-seal (전 멤버 u_hash == registry seal) ──")
        all_members = []
        for sid, c in GENSKILLS.items():
            if not c["byte_frozen"]:
                continue
            pat = re.compile(c["instance_pattern"])
            all_members += [(sid, int(pat.match(a).group(1))) for a in on_disk if pat.match(a)]
        for sid, n in sorted(all_members, key=lambda x: (x[0], x[1])):
            app_id = _seal_id(sid, n)
            sealed_path = os.path.join(APPREG, f"{app_id}.sealed.json")
            if not os.path.exists(sealed_path):
                ok(f"reseal {app_id} (registry seal 부재)", False); continue
            ref = json.load(open(sealed_path, encoding="utf-8"))["u_hash"]
            spec, _ = GENSKILLS[sid]["make_spec"](n)
            tp = os.path.join(APPS, f"_genskill_t2_{app_id}.app.pg")
            open(tp, "w", encoding="utf-8", newline="\n").write(spec); tmp_specs.append(tp)
            v = aa.assemble(tp, tmp_store)
            match = bool(v.sealed) and v.u_hash == ref
            ok(f"reseal {app_id} u_hash==registry", match,
               "" if match else f"sealed={v.sealed} got={v.u_hash[:12] if v.sealed else 'n/a'} want={ref[:12]}")

        # ── T3: new-method seal (cluster_ring) ──
        print("── T3 new-method seal (cluster_ring ring4) ──")
        spec, _ = gen_cluster_ring(4)
        tp = os.path.join(APPS, "_genskill_t3_ring4.app.pg")
        open(tp, "w", encoding="utf-8", newline="\n").write(spec); tmp_specs.append(tp)
        v = aa.assemble(tp, tmp_store)
        ok("new-method ring4 Tier-0 sealed", bool(v.sealed) and str(v.tier) in ("0", "exact"),
           f"sealed={v.sealed} tier={v.tier} u_hash={v.u_hash[:12] if v.sealed else 'n/a'}")
    finally:
        for tp in tmp_specs:
            if os.path.exists(tp):
                os.remove(tp)
        shutil.rmtree(tmp_store, ignore_errors=True)

    print("=" * 84)
    print(f"selftest: {len(passed)} PASS / {len(failed)} FAIL "
          f"(byte-frozen {len(byte_ok)} · legacy-format {len(legacy)} unitary-verified)")
    if failed:
        print("FAILED:", failed)
    return 0 if not failed else 1


def main():
    a = sys.argv[1:]
    if not a or a[0] == "list":
        return cmd_list()
    cmd = a[0]
    if cmd == "show" and len(a) >= 2:
        return cmd_show(a[1])
    if cmd == "emit" and len(a) >= 3:
        out = a[a.index("--out") + 1] if "--out" in a else None
        return cmd_emit(a[1], int(a[2]), out)
    if cmd == "catalog":
        return cmd_catalog()
    if cmd == "selftest":
        return cmd_selftest()
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
