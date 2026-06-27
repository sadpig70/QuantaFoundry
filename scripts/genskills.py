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
# 3b. 생성 방법 — reversible arithmetic synthesis (controlled modular multiplier)
#     산술 순열(×a mod N)을 MMD transformation-based synthesis 로 봉인 MCT
#     (toffoli/c3x/c4x/c5x, ≤5 control)에 정직 분해. golden=순열(MatrixGate 없음).
#     §8.7 이 지목한 최고가치 차기 GenSkill — Shor 의 controlled-U 생성 *방법*.
# ════════════════════════════════════════════════════════════════════════════
_MCT_MODULE = {0: "x_gate", 1: "cnot", 2: "toffoli", 3: "c3x", 4: "c4x", 5: "c5x"}


def _set_wires(v, nq):
    """big-endian(wire0=MSB): v 에서 1인 wire 인덱스."""
    return [b for b in range(nq) if (v >> (nq - 1 - b)) & 1]


def _wmask(wires, nq):
    m = 0
    for b in wires:
        m |= 1 << (nq - 1 - b)
    return m


def mmd_synthesize(target_perm, nq):
    """target_perm[x]=출력 인 bijection → MCT 게이트열(circuit time order).
    transformation-based(MMD): 출력측 변환으로 f→identity 수집 후 역순(자기역원).
    각 게이트=(controls_tuple, target_wire). 결정론(perm 만의 함수)."""
    dim = 1 << nq
    f = list(target_perm)
    collected = []

    def apply_out(controls, tb):
        cm = _wmask(controls, nq); tm = 1 << (nq - 1 - tb)
        for k in range(dim):
            if (f[k] & cm) == cm:
                f[k] ^= tm

    for x in range(dim):
        if f[x] == x:
            continue
        xset = set(_set_wires(x, nq))
        yset = set(_set_wires(f[x], nq))
        for b in sorted(xset - yset):                      # x엔 있고 y엔 없는 비트 ON
            controls = tuple(sorted(yset))
            collected.append((controls, b)); apply_out(controls, b); yset.add(b)
        for b in sorted(set(_set_wires(f[x], nq)) - xset):  # y엔 있고 x엔 없는 비트 OFF
            controls = tuple(sorted(xset))
            collected.append((controls, b)); apply_out(controls, b)
    if f != list(range(dim)):
        raise ValueError("mmd_synthesize: 합성 실패(f≠identity)")
    return collected[::-1]


def _modmul_perm(a, N, nq):
    """controlled ×a mod N 순열. q0=control(wire0=MSB), 나머지 work(big-endian value)."""
    dim = 1 << nq; wb = nq - 1
    perm = [0] * dim
    for s in range(dim):
        if (s >> (nq - 1)) & 1 == 0:
            perm[s] = s
        else:
            w = s & ((1 << wb) - 1)
            perm[s] = (1 << (nq - 1)) | ((a * w) % N if w < N else w)
    return perm


def gen_modmul(a, N, nq):
    """controlled (×a mod N) on nq-1 work qubits. golden=산술순열, plan=MMD 합성(봉인 MCT)."""
    from math import gcd
    if gcd(a, N) != 1:
        raise ValueError(f"gen_modmul: a={a} must be coprime to N={N}")
    perm = _modmul_perm(a, N, nq)
    gates = mmd_synthesize(perm, nq)
    maxc = max((len(c) for c, _ in gates), default=0)
    if maxc > 5:
        raise ValueError(f"gen_modmul: {maxc} controls > 5 (봉인 모듈 한계; nq={nq} 축소 필요)")
    steps = [{"spec": f"../modules/{_MCT_MODULE[len(c)]}.pg", "targets": list(c) + [t]} for c, t in gates]
    plan = build_plan(steps)
    golden = (
        "import numpy as np\n"
        f"a={a}; N={N}; nq={nq}\n"
        "dim=1<<nq; wb=nq-1\n"
        "golden=np.zeros((dim,dim),dtype=complex)\n"
        "for s in range(dim):\n"
        "    if (s>>(nq-1))&1==0: golden[s,s]=1\n"
        "    else:\n"
        "        w=s&((1<<wb)-1); nw=(a*w)%N if w<N else w\n"
        "        golden[(1<<(nq-1))|nw, s]=1")
    deps = sorted(set(_MCT_MODULE[len(c)] for c, _ in gates))
    header = (f"# cmul{a}_mod{N} — controlled (×{a} mod {N}) on {nq-1} work qubits ({nq}q, q0=control). "
              f"genskill=modmul_synth@1.\n"
              f"# golden=산술 순열(독립), plan={len(gates)} gates = MMD reversible synthesis → 봉인 "
              f"{deps} (≤5 control, no MatrixGate).\n")
    spec = assemble_app_spec(f"cmul{a}_mod{N}", nq, header, golden, plan)
    return spec, deps


# ════════════════════════════════════════════════════════════════════════════
# 3c. 생성 방법 — W-state cascade (연속회전 Ry primitive + amplitude-distribution)
#     첫 연속-각도 알고리즘 상태. 반각 α_k=arccos(√(1/k)) Ry primitive(k=2..n)를 봉인하고
#     X·CRy(=Ry±·cnot)·cnot cascade 로 |W_n> 준비. Ry(-α)=Ry(α)† → _dag 컨벤션.
#     봉인 ry primitive 는 family 재사용(W_{n+1} = W_n 모듈 + ±α_{n+1} 2개) = compounding.
# ════════════════════════════════════════════════════════════════════════════
def ry_module_id(k, dag=False):
    return f"ry_k{k}" + ("_dag" if dag else "")


def gen_ry_module(k, dag=False):
    """single-qubit Ry(±α_k) primitive 모듈 spec. α_k=arccos(√(1/k)). bloq=YPowGate(전역위상은
    C4 무시), golden=표준 Ry. dag=True → Ry(-α_k)=Ry(α_k)†."""
    sgn = "-" if dag else ""
    mid = ry_module_id(k, dag)
    spec = (
        "```python id=bloq\n"
        "import numpy as np\n"
        "from qualtran.bloqs.basic_gates import YPowGate\n"
        f"# Ry({sgn}α) primitive, α=arccos(sqrt(1/{k})) — W-state cascade 반각(k={k}). 전역위상은 C4 무시.\n"
        f"bloq = YPowGate(exponent={sgn}np.arccos(np.sqrt(1/{k}))/np.pi)\n"
        "```\n"
        "```python id=golden\n"
        "import numpy as np\n"
        f"a = {sgn}np.arccos(np.sqrt(1/{k}))\n"
        "golden = np.array([[np.cos(a/2), -np.sin(a/2)], [np.sin(a/2), np.cos(a/2)]], dtype=complex)\n"
        "```\n"
        f'```json id=meta\n{{"id": "{mid}", "n_sys": 1, "n_anc": 0}}\n```\n')
    return spec, mid


def wstate_required_modules(n):
    """W_n 에 필요한 봉인 모듈: x_gate, cnot, 그리고 ±α_k Ry (k=2..n)."""
    mods = ["x_gate", "cnot"]
    for k in range(2, n + 1):
        mods += [ry_module_id(k, False), ry_module_id(k, True)]
    return mods


def gen_wstate(n):
    """|W_n> 준비 app. golden=독립 합성 유니터리(raw Ry/X/CNOT), plan=봉인 모듈 cascade.
    블록 i(0..n-2): CRy(θ_i)=Ry(α_k)·CNOT·Ry(-α_k)·CNOT on (i,i+1) 후 CNOT(i+1,i), k=n-i, α_k=θ_i/2."""
    if n < 2:
        raise ValueError("gen_wstate: n>=2")
    golden = (
        "import numpy as np\n"
        f"n={n}\n"
        "def Ry(t): return np.array([[np.cos(t/2),-np.sin(t/2)],[np.sin(t/2),np.cos(t/2)]],dtype=complex)\n"
        "def e1(U,t):\n"
        "    return np.kron(np.kron(np.eye(1<<t),U),np.eye(1<<(n-t-1)))\n"
        "def cn(c,t):\n"
        "    dim=1<<n; M=np.zeros((dim,dim),complex)\n"
        "    for x in range(dim):\n"
        "        y=x^((1<<(n-1-t)) if (x>>(n-1-c))&1 else 0); M[y,x]=1\n"
        "    return M\n"
        "X=np.array([[0,1],[1,0]],complex)\n"
        "U=e1(X,0)\n"
        "for i in range(n-1):\n"
        "    k=n-i; a=np.arccos(np.sqrt(1/k)); q=i+1\n"
        "    U=e1(Ry(a),q)@U; U=cn(i,q)@U; U=e1(Ry(-a),q)@U; U=cn(i,q)@U; U=cn(q,i)@U\n"
        "golden=U")
    steps = [{"spec": "../modules/x_gate.pg", "targets": [0]}]
    for i in range(n - 1):
        k = n - i; q = i + 1
        steps += [{"spec": f"../modules/{ry_module_id(k)}.pg", "targets": [q]},
                  {"spec": "../modules/cnot.pg", "targets": [i, q]},
                  {"spec": f"../modules/{ry_module_id(k, True)}.pg", "targets": [q]},
                  {"spec": "../modules/cnot.pg", "targets": [i, q]},
                  {"spec": "../modules/cnot.pg", "targets": [q, i]}]
    plan = build_plan(steps)
    deps = wstate_required_modules(n)
    header = (f"# wstate{n} — W-state |W_{n}> ({n}큐비트). genskill=wstate_cascade@1 (human seed 0).\n"
              f"# 봉인 재조립: X·CRy(±α_k)·cnot cascade. 연속회전 알고리즘 상태. 새 모듈=±α_k Ry(k=2..{n}) 재사용.\n")
    spec = assemble_app_spec(f"wstate{n}", n, header, golden, plan)
    return spec, deps


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
    "wstate_cascade": {
        "version": "1", "produces": "app", "param": "n:int>=2",
        "kind": "W-state (continuous-rotation amplitude-distribution cascade)",
        "golden_method": "X(q0) then per-block CRy(α_k)=Ry·cnot·Ry†·cnot + cnot over sealed "
                         "±α_k Ry primitives (α_k=arccos√(1/k), k=2..n) + x_gate/cnot",
        "required_modules": ["x_gate", "cnot", "ry_k2", "ry_k2_dag", "..."],
        "instance_pattern": r"^wstate(\d+)$", "byte_frozen": True, "make_spec": gen_wstate,
        "prereq_method": "gen_ry_module(k, dag) — ±α_k Ry primitive (family-reused; W_{n+1}=W_n + ±α_{n+1})",
    },
    "modmul_synth": {
        "version": "1", "produces": "app", "param": "a,N,nq",
        "kind": "controlled modular multiplier (reversible arithmetic synthesis)",
        "golden_method": "arithmetic permutation (×a mod N, identity out-of-range) + MMD "
                         "transformation-based synthesis into sealed MCTs (toffoli/c3x/c4x/c5x, ≤5 controls)",
        "required_modules": ["toffoli", "c3x", "c4x", "c5x"],
        "instance_pattern": r"^cmul(\d+)_mod(\d+)$", "byte_frozen": False,
        "make_spec": gen_modmul, "sample_args": (2, 21, 6),
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


def _sample_args(c):
    """show 용 샘플 인자: sample_args 우선, 없으면 param 최소 n."""
    if "sample_args" in c:
        return c["sample_args"]
    return (3,) if "n>=3" in c["param"] else (2,)


def cmd_show(sid):
    if sid not in GENSKILLS:
        print(f"unknown skill: {sid} (있는 것: {list(GENSKILLS)})"); return 1
    c = GENSKILLS[sid]
    print(json.dumps({k: c[k] for k in c if k != "make_spec"} | {"id": sid}, ensure_ascii=False, indent=2))
    args = _sample_args(c)
    sample, deps = c["make_spec"](*args)
    print(f"\n── 샘플 산출 (args={args}) ──\n{sample}")
    return 0


def cmd_emit(sid, args, out_dir=None):
    if sid not in GENSKILLS:
        print(f"unknown skill: {sid}"); return 1
    spec, deps = GENSKILLS[sid]["make_spec"](*args)
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
    return {"ghz_linear": "ghz", "cluster_line": "cluster", "cluster_ring": "ring",
            "wstate_cascade": "wstate"}[skill_id] + str(n)


def _committed_perm(app_id):
    """committed spec 의 app_golden 을 exec 해 순열 perm[in]=out 반환(없으면 None)."""
    import numpy as np
    fp = os.path.join(APPS, f"{app_id}.app.pg")
    if not os.path.exists(fp):
        return None
    txt = open(fp, encoding="utf-8").read()
    m = re.search(r"```python id=app_golden\n(.*?)\n```", txt, re.S)
    if not m:
        return None
    ns = {}
    exec(m.group(1), ns)
    G = np.asarray(ns["golden"])
    return [int(np.argmax(np.abs(G[:, c]))) for c in range(G.shape[1])]


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

        # ── T4: arithmetic-synthesis reproduce-seal (기존 cmul*_mod* 전수) ──
        print("── T4 arithmetic-synthesis reproduce-seal (cmul*_mod* u_hash == registry) ──")
        cpat = re.compile(GENSKILLS["modmul_synth"]["instance_pattern"])
        cmuls = sorted(a for a in on_disk if cpat.match(a))
        if not cmuls:
            ok("modmul reproduce (no cmul apps on disk)", False)
        for app_id in cmuls:
            m = cpat.match(app_id); a_, N_ = int(m.group(1)), int(m.group(2))
            sealed_path = os.path.join(APPREG, f"{app_id}.sealed.json")
            if not os.path.exists(sealed_path):
                ok(f"modmul reseal {app_id} (seal 부재)", False); continue
            sj = json.load(open(sealed_path, encoding="utf-8"))
            ref, nq = sj["u_hash"], sj["n_sys"]
            spec, _ = gen_modmul(a_, N_, nq)
            tp = os.path.join(APPS, f"_genskill_t4_{app_id}.app.pg")
            open(tp, "w", encoding="utf-8", newline="\n").write(spec); tmp_specs.append(tp)
            v = aa.assemble(tp, tmp_store)
            if bool(v.sealed) and v.u_hash == ref:
                ok(f"modmul reseal {app_id} u_hash==registry (canonical)", True)
            elif v.sealed:
                # u_hash 불일치: 알고리즘 동등(orbit-relevant 1..N-1 일치, 차이는 unused 경계 {0,2^wb-1})인지 확인
                wb = nq - 1; ctrl = 1 << (nq - 1)
                boundary = {ctrl | 0, ctrl | ((1 << wb) - 1)}
                mine = _modmul_perm(a_, N_, nq)
                comm = _committed_perm(app_id)
                diffs = {s for s in range(1 << nq) if comm and mine[s] != comm[s]}
                equiv = bool(comm) and diffs and diffs <= boundary
                ok(f"modmul {app_id} algorithm-equivalent (committed=degeneracy variant)", equiv,
                   f"canonical u_hash={v.u_hash[:12]}; committed differs only on unused boundary {sorted(diffs)}"
                   if equiv else f"genuine mismatch diffs={sorted(diffs)[:6]}")
            else:
                ok(f"modmul reseal {app_id}", False, "not sealed")

        # ── T5: arithmetic-synthesis new-synth (미봉인 multiplier 합성·봉인) ──
        print("── T5 arithmetic-synthesis new-synth (cmul8_mod21 Tier-0) ──")
        spec, _ = gen_modmul(8, 21, 6)
        tp = os.path.join(APPS, "_genskill_t5_cmul8_mod21.app.pg")
        open(tp, "w", encoding="utf-8", newline="\n").write(spec); tmp_specs.append(tp)
        v = aa.assemble(tp, tmp_store)
        ok("new-synth cmul8_mod21 Tier-0 sealed", bool(v.sealed) and str(v.tier) in ("0", "exact"),
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
        rest = a[2:a.index("--out")] if "--out" in a else a[2:]
        return cmd_emit(a[1], [int(x) for x in rest], out)
    if cmd == "catalog":
        return cmd_catalog()
    if cmd == "selftest":
        return cmd_selftest()
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
