#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""steane_encoded_t_observe — HE H3.2: Steane [[7,1,3]] 논리 수준 T-injection 관측 (신규 봉인 0).

FTQC non-Clifford 3부작의 완결편:
  magic_a(물리 magic state, V08_20) → distill5to1(magic 공장, H3.1) → **encoded T(논리 사용, 본편)**.

Eastin-Knill: Steane 에 transversal T 는 없다 → 논리 T 의 유일한 정직 경로 = magic-injection
(gate teleportation). 봉인된 Steane 자산(W7.2 인코더·W7.3 transversal CNOT)의 회로 의미를
14q **상태벡터**(16384-dim, dense unitary 불필요)로 관측한다:

    |ψ_L⟩(블록A 7q) ⊗ |T_L⟩(블록B 7q, 논리 magic)
    → transversal CNOT(A_i→B_i ×7 = 봉인 steane_logical_cnot 의미)
    → 논리 Z_L 측정(블록B) coherent branch
    → m=0: 블록A == T_L|ψ_L⟩ 정확.  m=1: 논리 S 보정(=(S†)^⊗7) 후 == T_L|ψ_L⟩ 정확.

검증된 관례(설계 확인): dual code C(=Hamming 행 생성, 비영 codeword 전부 weight 4) →
  S^⊗7 = 논리 diag(1,−i) = S_L† (즉 논리 S = (S†)^⊗7). X_L=X^⊗7·Z_L=Z^⊗7.

정직 경계(INV-Q3, seal 아님, root 불변):
  - 논리 T 게이트는 **유니터리 봉인 대상이 아님**(측정+보정 프로토콜). 관측=branch 별 exact 항등.
  - p₀=p₁=1/2 확률성 = gate-teleportation 본질(관측). teeth: 무보정 branch≠타겟, 잘못된
    magic(|+_L⟩)→identity teleport(≠T_L).
  - 신규 봉인 0. 14q dense unitary 미실체화(벡터만) — Tier-0 dense 한계 정직 준수.

사용: python scripts/steane_encoded_t_observe.py [--quick]
"""
import os, sys, json
from itertools import product
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".pgf", "proofs", "STEANE-ENCODED-T-OBSERVE.json")
ROWS = [0b1010101, 0b0110011, 0b0001111]     # Hamming parity rows → dual [7,3] code
ALL1 = 0b1111111
W = np.exp(1j * np.pi / 4)


def logical_words():
    C = set()
    for a, b, c in product([0, 1], repeat=3):
        C.add((a * ROWS[0]) ^ (b * ROWS[1]) ^ (c * ROWS[2]))
    w0 = np.zeros(128, dtype=complex)
    w1 = np.zeros(128, dtype=complex)
    for x in C:
        w0[x] = 1 / np.sqrt(8)
        w1[x ^ ALL1] = 1 / np.sqrt(8)
    return w0, w1


def apply_x(vec, mask):
    out = np.zeros_like(vec)
    for x in range(128):
        out[x ^ mask] += vec[x]
    return out


def apply_z(vec, mask):
    out = vec.copy()
    for x in range(128):
        out[x] *= (-1) ** (bin(x & mask).count("1"))
    return out


def apply_s7(vec, dag=False):
    out = vec.copy()
    ph = -1j if dag else 1j
    for x in range(128):
        out[x] *= ph ** (bin(x).count("1"))
    return out


def transversal_cnot(M):
    """M[xA,xB] → M[xA, xB^xA]: 7개 CNOT(A_i→B_i) 동시 = 비트단위 XOR (CSS transversal)."""
    out = np.zeros_like(M)
    for xA in range(128):
        for xB in range(128):
            out[xA, xB ^ xA] += M[xA, xB]
    return out


def fid(u, v):
    return float(abs(np.vdot(u, v)) ** 2 / (np.vdot(u, u).real * np.vdot(v, v).real))


def observe():
    w0, w1 = logical_words()
    # 논리 기저·관례 재검증
    stab = all(bool(np.allclose(apply_x(w, r), w)) and bool(np.allclose(apply_z(w, r), w))
               for w in (w0, w1) for r in ROWS)
    conv = bool(np.allclose(apply_s7(w0), w0)) and bool(np.allclose(apply_s7(w1), -1j * w1)) \
        and bool(np.allclose(apply_x(w0, ALL1), w1)) and bool(np.allclose(apply_z(w1, ALL1), -w1))
    # T-injection (a,b 비자명·복소)
    a, b = 0.6, 0.8j
    psi = a * w0 + b * w1
    target = a * w0 + W * b * w1                      # T_L|ψ_L>
    magic = (w0 + W * w1) / np.sqrt(2)                # |T_L>
    M = transversal_cnot(np.outer(psi, magic))
    v0 = M @ np.conj(w0)
    v1 = M @ np.conj(w1)
    p0, p1 = float(np.linalg.norm(v0) ** 2), float(np.linalg.norm(v1) ** 2)
    b0 = fid(v0, target) > 1 - 1e-9
    b1 = fid(apply_s7(v1, dag=True), target) > 1 - 1e-9   # 논리 S 보정 = (S†)^⊗7
    teeth1 = fid(v1, target) < 1 - 1e-6                    # 무보정 ≠ 타겟
    Mw = transversal_cnot(np.outer(psi, (w0 + w1) / np.sqrt(2)))
    u0 = Mw @ np.conj(w0)
    teeth2 = fid(u0, target) < 1 - 1e-6 and fid(u0, psi) > 1 - 1e-9  # 잘못된 magic → identity
    ok = stab and conv and b0 and b1 and abs(p0 - 0.5) < 1e-9 and abs(p1 - 0.5) < 1e-9 \
        and teeth1 and teeth2
    return {"protocol": "Steane [[7,1,3]] 논리 T-injection (gate teleportation, coherent-branch)",
            "chain": "magic_a(물리) → distill5to1(공장) → encoded T(논리 사용) — non-Clifford 3부작 완결",
            "logical_basis_stabilizer_check": stab,
            "conventions": {"S^⊗7 == S_L†": True, "X_L=X^⊗7·Z_L=Z^⊗7": True, "ok": conv},
            "branch0_exact_TL_psi": b0, "branch1_SL_corrected_exact_TL_psi": b1,
            "branch_probabilities": [round(p0, 9), round(p1, 9)],
            "teeth": {"uncorrected_branch1_not_target": teeth1,
                      "wrong_magic_gives_identity_not_T": teeth2},
            "honest_boundary": "논리 T=측정+보정 프로토콜 → 유니터리 봉인 대상 아님. branch 별 exact "
                               "항등=관측(INV-Q3). p=1/2 확률성=본질. 신규 봉인 0·root 불변·14q dense 미실체화.",
            "ok": bool(ok)}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        report = {"_schema": "steane-encoded-t-observe-v1",
                  "_note": "논리 수준 T-injection 관측(Steane). 신규 봉인 0(INV-Q3). "
                           "봉인 Steane 자산(W7.2/W7.3)의 non-Clifford 소비 실증.",
                  "observation": res}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("Steane 논리 T-injection 관측 (encoded non-Clifford):", flush=True)
        print(f"  논리기저 stabilizer={res['logical_basis_stabilizer_check']} · 관례(S^7=S_L† 등)={res['conventions']['ok']}", flush=True)
        print(f"  branch0 == T_L|ψ_L>: {res['branch0_exact_TL_psi']} · branch1+S_L 보정 == T_L|ψ_L>: {res['branch1_SL_corrected_exact_TL_psi']}", flush=True)
        print(f"  branch 확률 = {res['branch_probabilities']} (=1/2,1/2)", flush=True)
        print(f"  teeth: 무보정≠타겟 {res['teeth']['uncorrected_branch1_not_target']} · 잘못된 magic→identity {res['teeth']['wrong_magic_gives_identity_not_T']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"steane_encoded_t_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
