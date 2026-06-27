"""second_oracle.py — Qualtran 비의존 독립 2차 검증기 (외부 리뷰 R-H / F-7 대응).

리뷰 결함: C4 핵심 비교 bloq.tensor_contract()==golden 이 Qualtran 단일 스택에서 일어남.
Qualtran tensor contraction/canonicalization 버그 하나면 전 라이브러리가 조용히 통과(risk d).
이 모듈은 sealed unitary 를 **순수 python(numpy만, Qualtran/spec-golden 코드 미사용)** 으로
독립 재구성해 registry 의 u_hash 와 교차대조한다. dense 경로에서 risk(d)를 실제로 닫는다.

honest 한계: 측정도구(vs.hash_unitary)는 공유한다(공통 canonicalization). 독립성은 *유니터리를
어떻게 구성했나*에 있다 — 본 검증기는 Qualtran bloq 도, specs 의 golden 코드도 실행하지 않고
제1원리 수학으로 재구성한다. 추가로 자체 canonical hash 도 계산해 내부 일관성을 함께 보고한다.

사용:  python scripts/second_oracle.py
"""
import os, sys, json, hashlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts"))
import verify_seal as vs    # noqa: E402  (공통 측정도구 — hash 비교용. 구성은 독립)
MODREG = os.path.join(ROOT, "registry", "modules")
APPREG = os.path.join(ROOT, "registry", "apps")
APPS = os.path.join(ROOT, "specs", "apps")

# ── 제1원리 독립 구성 (numpy만, qualtran/spec-golden 미사용) ──
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
Hd = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
P0 = np.array([[1, 0], [0, 0]], dtype=complex)
P1 = np.array([[0, 0], [0, 1]], dtype=complex)


def perm_gate(perm):
    n = len(perm); M = np.zeros((n, n), dtype=complex)
    for i, o in enumerate(perm):
        M[o, i] = 1
    return M


def cphase(k):  # controlled-R_k diag(1,1,1,exp(2pi i/2^k))
    return np.diag([1, 1, 1, np.exp(2j * np.pi / 2 ** k)]).astype(complex)


def cnx_perm(nc):
    n = nc + 1
    return perm_gate([(s ^ 1) if (s >> 1) == ((1 << nc) - 1) else s for s in range(1 << n)])


# 독립 구성기: gate_id -> unitary (qualtran/spec 코드 경로와 무관)
INDEP = {
    "x_gate": lambda: X, "z_gate": lambda: Z, "h_gate": lambda: Hd,
    "s_gate": lambda: np.diag([1, 1j]).astype(complex),
    "t_gate": lambda: np.diag([1, np.exp(1j * np.pi / 4)]).astype(complex),
    "cnot": lambda: perm_gate([0, 1, 3, 2]),
    "swap2": lambda: perm_gate([0, 2, 1, 3]),
    "cz": lambda: np.diag([1, 1, 1, -1]).astype(complex),
    "toffoli": lambda: cnx_perm(2),
    "fredkin": lambda: perm_gate([0, 1, 2, 3, 4, 6, 5, 7]),
    "c3x": lambda: cnx_perm(3), "c4x": lambda: cnx_perm(4), "c5x": lambda: cnx_perm(5),
    "cs_gate": lambda: cphase(2), "ct_gate": lambda: cphase(3),
    "cr4_gate": lambda: cphase(4), "cr5_gate": lambda: cphase(5),
    "cs_dag": lambda: np.diag([1, 1, 1, -1j]).astype(complex),
}


def my_canonical_hash(U):
    """독립 canonical hash — 측정도구 공유도 부분 차단(전역위상 제거 + tol 정규화 + sha256)."""
    U = np.array(U, dtype=complex)
    # 전역위상 제거: 첫 비영 원소 위상 정규화
    flat = U.flatten()
    nz = flat[np.abs(flat) > 1e-9]
    if len(nz):
        U = U * np.exp(-1j * np.angle(nz[0]))
    re = np.round(U.real, 7) + 0.0
    im = np.round(U.imag, 7) + 0.0
    return hashlib.sha256(re.tobytes() + im.tobytes()).hexdigest()[:16]


def embed(U, targets, n):
    """독립 embed (오라클 embed_unitary 미사용) — big-endian."""
    k = len(targets); g = U.reshape([2] * k + [2] * k)
    T = np.eye(1 << n, dtype=complex).reshape([2] * n + [1 << n])
    T = np.tensordot(g, T, axes=(list(range(k, 2 * k)), targets))
    T = np.moveaxis(T, list(range(k)), targets)
    return T.reshape(1 << n, 1 << n)


def check_modules():
    rows = []
    for gid, fn in INDEP.items():
        p = os.path.join(MODREG, f"{gid}.sealed.json")
        if not os.path.exists(p):
            continue
        sealed = json.load(open(p, encoding="utf-8"))["u_hash"]
        U = fn()
        match = vs.hash_unitary(U) == sealed
        rows.append((gid, match, my_canonical_hash(U)))
    return rows


def check_app_cmul2_mod21():
    """cmul2_mod21 을 독립 embed + 독립 모듈 유니터리로 재조립 → sealed u_hash 대조 (app_assemble/qualtran 미사용)."""
    import re
    src = open(os.path.join(APPS, "cmul2_mod21.app.pg"), encoding="utf-8").read()
    plan = json.loads(re.search(r"```json id=plan\n(.*?)```", src, re.S).group(1))
    n = 6
    V = np.eye(1 << n, dtype=complex)
    for step in plan["steps"]:
        gid = os.path.basename(step["spec"])[:-3]
        U = INDEP[gid]()
        V = embed(U, step["targets"], n) @ V
    sealed = json.load(open(os.path.join(APPREG, "cmul2_mod21.sealed.json"), encoding="utf-8"))["u_hash"]
    return vs.hash_unitary(V) == sealed


def main():
    print("=" * 78)
    print("Second Oracle — Qualtran 비의존 독립 재구성 vs registry u_hash (risk(d) 차단)")
    print("=" * 78)
    rows = check_modules()
    ok = sum(1 for _, m, _ in rows if m)
    for gid, m, h in rows:
        print(f"  {'✓' if m else '✗'} {gid:12} u_hash 일치={m}  (자체 canonical={h})")
    app_ok = check_app_cmul2_mod21()
    print(f"  {'✓' if app_ok else '✗'} cmul2_mod21  독립 재조립 u_hash 일치={app_ok} (app_assemble 미사용)")
    print("=" * 78)
    print(f"모듈 독립검증 {ok}/{len(rows)} 일치 · 앱(cmul2_mod21) {'PASS' if app_ok else 'FAIL'}")
    print("=" * 78)
    res = {"modules_checked": len(rows), "modules_match": ok,
           "app_cmul2_mod21_match": app_ok,
           "method": "pure-numpy independent reconstruction, no qualtran/no spec-golden, no oracle embed"}
    json.dump(res, open(os.path.join(ROOT, ".pgf", "autoforge", "SECOND-ORACLE-RESULT.json"), "w",
                        encoding="utf-8"), ensure_ascii=False, indent=2)
    return 0 if ok == len(rows) and app_ok else 1


if __name__ == "__main__":
    sys.exit(main())
