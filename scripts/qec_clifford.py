# -*- coding: utf-8 -*-
"""
qec_clifford.py — Stage 7 W7.2 CliffordTier2QEC

W7.1 정직성 갭 닫기. W7.1 QEC 인코더는 *순수 parity/Hadamard* 라 full-unitary golden 을
closed-form 으로 독립구성할 수 있었다. 그러나 일반 stabilizer 코드(Steane [[7,1,3]] 등)는 인코더가
코드워드 2컬럼만 고정하고 나머지는 회로-특정 → dense golden 이 "회로 재실행"으로 전락한다.
진짜 독립검증은 **stabilizer tableau** 로만 가능 — 이번 작업이 그 *더 강한 오라클*(Tier-2)을 실가동한다.

봉인 경로(VerifyTier2Path 확인 완료): verify_seal.py 의 module-level `tier="clifford"` →
정준 stabilizer tableau 해시(cirq, dense 미사용, 임의크기 정확, 전역위상 무시 유일결정). app_assemble
에는 Tier-2 경로 없음 → 이들은 **모듈**로 봉인(registry/modules).

봉인 대상(Tier-2 CLIFFORD 모듈):
 1. steane_zero_t2  [[7,1,3]] Steane 논리-0 상태준비 |0_L>=(1/√8)Σ_{c∈[7,3] simplex}|c>. CSS(Hamming).
 2. steane_one_t2   [[7,1,3]] 논리-1 |1_L>=X^⊗7|0_L>.
 3. shor9_encoder_t2 W7.1 Shor-9 인코더의 Tier-2 재봉인 — *동일 연산*을 더 강한 오라클로도 봉인 +
                    dense cross-validation(cirq dense == W7.1 closed-form golden).

정직성 경계:
 - Tier-2 seal = 정준 tableau(표현무관 지문). u_hash 는 tableau 해시 → dense u_hash 와 불일치(tier 구분 의도).
 - **코드-정확성 witness(드라이버, 오라클 독립)**: 준비된 논리상태가 코드 stabilizer 의 +1 고유상태인가를
   dense numpy(n≤10)로 직접 확인 — 이것이 "올바른 코드"의 독립 증거. cirq 회로(Qualtran spec 와 별도 경로)로 구성.
 - second_oracle 는 dense 재구성 기반 → Tier-2(tableau) 모듈은 그 범위 밖. 53 Tier-0 dense 모듈은 여전히 53/53.
 - 측정=비unitary → 상태준비/인코더 unitary 만. plan=Clifford 게이트(H·CNOT·X), MatrixGate 0.
 - 비파괴: 모듈 53→56(53 Tier-0 + 3 Tier-2), 앱 75 불변. frozen 23키·fingerprint byte-identical.
 - 미착수(정직 future work): full logical-input Steane 인코더, 5-qubit [[5,1,3]](비-CSS, 일반 stabilizer
   인코더 합성 필요).

사용:  python scripts/qec_clifford.py
"""
from __future__ import annotations

import os
import sys
import json
import itertools
import subprocess

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, ORACLE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import verify_seal as vs        # noqa: E402  (Tier-2 봉인 CLI — 사용만)
import clifford_seal as cs      # noqa: E402  (정준 tableau 독립 재확인 — 사용만)

SPECS_MODS = os.path.join(ROOT, "specs", "modules")
MODREG = os.path.join(ROOT, "registry", "modules")
OUT = os.path.join(ROOT, ".pgf", "arith")

# Hamming [7,4,3] 패리티검사 H (3×7, 열=binary 1..7). Steane = CSS(Hamming): H H^T=0(자기직교).
_HAMMING = np.array([[0, 0, 0, 1, 1, 1, 1],
                     [0, 1, 1, 0, 0, 1, 1],
                     [1, 0, 1, 0, 1, 0, 1]], dtype=int)


def _rref_gf2(M):
    """GF(2) RREF + pivot 열. 반환 (reduced, pivots)."""
    A = (M.copy() % 2)
    rows, cols = A.shape
    pivots = []
    r = 0
    for c in range(cols):
        sel = [i for i in range(r, rows) if A[i, c] == 1]
        if not sel:
            continue
        A[[r, sel[0]]] = A[[sel[0], r]]
        for i in range(rows):
            if i != r and A[i, c] == 1:
                A[i] = (A[i] + A[r]) % 2
        pivots.append(c)
        r += 1
        if r == rows:
            break
    return A, pivots


def _steane_zero_gates():
    """CSS |0_L> 준비: H on pivots + CNOT(pivot→nonpivot) per systematic generator."""
    Mr, pivots = _rref_gf2(_HAMMING)
    gates = [("h", p) for p in pivots]
    for i, p in enumerate(pivots):
        for j in range(7):
            if j != p and Mr[i, j] == 1:
                gates.append(("cnot", p, j))
    return gates


def _steane_one_gates():
    return _steane_zero_gates() + [("x", q) for q in range(7)]   # X̄ = X^⊗7


def _shor9_gates():
    """W7.1 Shor-9 인코더 회로(동일 정의): phase 확산 → H(0,3,6) → bit-flip 블록."""
    g = [("cnot", 0, 3), ("cnot", 0, 6)]
    g += [("h", 0), ("h", 3), ("h", 6)]
    g += [("cnot", 0, 1), ("cnot", 0, 2), ("cnot", 3, 4),
          ("cnot", 3, 5), ("cnot", 6, 7), ("cnot", 6, 8)]
    return g


SPECS = {
    "steane_zero_t2": dict(n=7, gates=_steane_zero_gates(),
                           note="[[7,1,3]] Steane 논리-0 상태준비 |0_L> (CSS Hamming, 자기직교)."),
    "steane_one_t2": dict(n=7, gates=_steane_one_gates(),
                          note="[[7,1,3]] Steane 논리-1 |1_L>=X^⊗7|0_L>."),
    "shor9_encoder_t2": dict(n=9, gates=_shor9_gates(),
                             note="W7.1 [[9,1,3]] Shor-9 인코더의 Tier-2 재봉인(동일 연산, 더 강한 오라클)."),
}


# ── BloqBuilder 코드 생성(ghz20.pg 패턴) ─────────────────────────────────────────
def _bloq_code(n, gates):
    L = ["from qualtran import BloqBuilder",
         "from qualtran.bloqs.basic_gates import Hadamard, CNOT, XGate",
         "bb = BloqBuilder()",
         f"qs = [bb.add_register(f'q{{i}}', 1) for i in range({n})]"]
    for g in gates:
        if g[0] == "h":
            L.append(f"qs[{g[1]}] = bb.add(Hadamard(), q=qs[{g[1]}])")
        elif g[0] == "x":
            L.append(f"qs[{g[1]}] = bb.add(XGate(), q=qs[{g[1]}])")
        else:
            c, t = g[1], g[2]
            L.append(f"qs[{c}], qs[{t}] = bb.add(CNOT(), ctrl=qs[{c}], target=qs[{t}])")
    L.append(f"bloq = bb.finalize(**{{f'q{{i}}': qs[i] for i in range({n})}})")
    return "\n".join(L)


def gen_spec(name):
    s = SPECS[name]
    header = (f"# {name} — {s['note']} Tier-2 CLIFFORD(정준 stabilizer tableau, dense 미사용). "
              f"plan=Clifford 게이트, no MatrixGate. 코드-정확성 witness=qec_clifford 드라이버(stabilizer 고유값).\n")
    return (header +
            "```python id=bloq\n" + _bloq_code(s["n"], s["gates"]) + "\n```\n"
            '```json id=meta\n'
            f'{{"id": "{name}", "n_sys": {s["n"]}, "n_anc": 0, "tier": "clifford"}}\n'
            "```\n")


# ── 독립 정확성 witness (cirq 회로 — Qualtran spec 와 별도 경로) ──────────────────
def _cirq_circuit(n, gates):
    import cirq
    q = cirq.LineQubit.range(n)
    c = cirq.Circuit()
    for g in gates:
        if g[0] == "h":
            c.append(cirq.H(q[g[1]]))
        elif g[0] == "x":
            c.append(cirq.X(q[g[1]]))
        else:
            c.append(cirq.CNOT(q[g[1]], q[g[2]]))
    return c, q


def _state(n, gates):
    import cirq
    c, q = _cirq_circuit(n, gates)
    return c.final_state_vector(initial_state=0, qubit_order=q)


def _apply_pauli(row_x, row_z, n, psi):
    """X^{row_x} Z^{row_z} 를 psi 에 적용(big-endian). 반환 새 벡터."""
    dim = 1 << n
    fx = 0
    for k in range(n):
        if row_x[k]:
            fx |= 1 << (n - 1 - k)
    out = np.zeros(dim, complex)
    for sidx in range(dim):
        a = psi[sidx]
        if abs(a) < 1e-12:
            continue
        x = [(sidx >> (n - 1 - k)) & 1 for k in range(n)]
        ph = sum(row_z[k] * x[k] for k in range(n)) % 2
        out[sidx ^ fx] += a * ((-1) ** ph)
    return out


def _steane_witness(name):
    """Steane stabilizer(3 X형 + 3 Z형) +1 고유값 + 논리Z̄ 고유값 확인 (dense, 오라클 독립)."""
    n = 7
    psi = _state(n, SPECS[name]["gates"])
    zero = np.zeros(n, int)
    stab_ok = True
    for r in _HAMMING:
        if not np.allclose(_apply_pauli(r, zero, n, psi), psi):   # X^r
            stab_ok = False
        if not np.allclose(_apply_pauli(zero, r, n, psi), psi):   # Z^r
            stab_ok = False
    ones = np.ones(n, int)
    zbar = _apply_pauli(zero, ones, n, psi)                       # Z̄ = Z^⊗7
    sign = +1 if name == "steane_zero_t2" else -1
    zbar_ok = np.allclose(zbar, sign * psi)
    support = int(np.sum(np.abs(psi) > 1e-9))
    return {"stabilizers_plus1": bool(stab_ok), "logicalZ_eigen": sign,
            "logicalZ_ok": bool(zbar_ok), "support": support, "pass": bool(stab_ok and zbar_ok)}


def _shor9_witness():
    """cirq dense(bloq 회로) == W7.1 closed-form golden → 동일 연산 cross-validation."""
    import cirq
    import qec_family as qf
    c, q = _cirq_circuit(9, SPECS["shor9_encoder_t2"]["gates"])
    dense = cirq.unitary(c)
    golden = qf._specs()["shor9_encoder"]["golden"]
    match = vs.hash_unitary(dense) == vs.hash_unitary(golden)
    return {"dense_eq_w71_golden": bool(match), "pass": bool(match)}


def seal(name):
    spec = gen_spec(name)
    sp = os.path.join(SPECS_MODS, f"{name}.pg")
    open(sp, "w", encoding="utf-8", newline="\n").write(spec)
    rc = subprocess.run([sys.executable, os.path.join(ORACLE, "verify_seal.py"), sp, "--out", MODREG],
                        capture_output=True, text=True, cwd=ORACLE).returncode
    seal_path = os.path.join(MODREG, f"{name}.sealed.json")
    if rc != 0 or not os.path.exists(seal_path):
        return {"id": name, "sealed": False}
    sealed = json.load(open(seal_path, encoding="utf-8"))
    # 독립 재확인: 정준 tableau 직접 재계산 == sealed u_hash (결정론/일관성)
    bloq = vs.instantiate(open(sp, encoding="utf-8").read().split("id=bloq\n")[1].split("```")[0], "bloq")
    indep_hash, _ = cs.canonical_tableau_hash(bloq)
    return {"id": name, "n_sys": sealed["n_sys"], "sealed": True, "tier": sealed["tier"],
            "u_hash": sealed["u_hash"], "tableau_recompute_match": indep_hash == sealed["u_hash"]}


def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 80)
    print("W7.2 CliffordTier2QEC — stabilizer-tableau 오라클로 QEC 심화(W7.1 정직성 갭 닫기)")
    print("Tier-2 CLIFFORD(dense-free 정준 tableau). 코드-정확성 witness=드라이버 stabilizer 고유값.")
    print("=" * 80)

    sealed = [seal(n) for n in ("steane_zero_t2", "steane_one_t2", "shor9_encoder_t2")]
    for s in sealed:
        print(f"[Seal-T2] {s['id']:18} n_sys={s.get('n_sys')} sealed={s['sealed']} "
              f"tier={s.get('tier')} tableau_recompute={s.get('tableau_recompute_match')} "
              f"u={str(s.get('u_hash'))[:14]}")

    wz = _steane_witness("steane_zero_t2")
    wo = _steane_witness("steane_one_t2")
    ws = _shor9_witness()
    print(f"[Witness] steane_zero: stab+1={wz['stabilizers_plus1']} Z̄=+1 ok={wz['logicalZ_ok']} "
          f"support={wz['support']} → {wz['pass']}")
    print(f"[Witness] steane_one : stab+1={wo['stabilizers_plus1']} Z̄=-1 ok={wo['logicalZ_ok']} "
          f"support={wo['support']} → {wo['pass']}")
    print(f"[Witness] shor9_t2   : cirq dense == W7.1 closed-form golden = {ws['dense_eq_w71_golden']} → {ws['pass']}")

    report = {
        "phase": "W7.2 CliffordTier2QEC",
        "honesty": "Tier-2 seal = canonical stabilizer tableau (representation-independent, dense-free, "
                   "exact up to global phase); u_hash is a tableau hash (≠ dense). Code-correctness is an "
                   "INDEPENDENT driver witness (stabilizer-eigenvalue check via dense numpy, distinct cirq "
                   "path from the Qualtran spec). second_oracle (dense reconstruction) covers the 53 Tier-0 "
                   "modules; these 3 Tier-2 modules are tableau-sealed (outside dense scope). shor9_t2 "
                   "cross-validates W7.1: same operator now also under the stronger oracle. Future work: "
                   "full logical-input Steane encoder, non-CSS [[5,1,3]] (general stabilizer encoder synthesis).",
        "seals": sealed,
        "witness": {"steane_zero": wz, "steane_one": wo, "shor9_t2": ws},
    }
    all_ok = (all(s["sealed"] and s["tier"] == 2 and s["tableau_recompute_match"] for s in sealed)
              and wz["pass"] and wo["pass"] and ws["pass"])
    report["all_ok"] = bool(all_ok)
    json.dump(report, open(os.path.join(OUT, "QEC-CLIFFORD-REPORT.json"), "w",
                           encoding="utf-8"), ensure_ascii=False, indent=2)
    print("-" * 80)
    print(f"all_ok={all_ok}  →  .pgf/arith/QEC-CLIFFORD-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
