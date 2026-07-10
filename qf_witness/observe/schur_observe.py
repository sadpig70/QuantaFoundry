#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""schur_observe — HE2 T1: 3-qubit Schur-Weyl transform J²/Jz 동시대각 witness (신규 봉인 0).

봉인된 schur3(encoder U: 계산기저 label → Schur 기저)의 표현론 성질을 관측:
  1. U†J²U · U†JzU 동시 대각 (J²=(ΣS⃗ᵢ)²·Jz=ΣZᵢ/2) — 유효 Schur transform 판정(C4 독립경로).
  2. J² 스펙트럼 {3.75×4, 0.75×4} = spin-3/2 ⊕ spin-1/2×2 · Jz label map 정합.
  3. Schur-Weyl duality: S₃ 전치 3종이 Schur 기저에서 (j,m)-sector 보존 —
     j=3/2 열(완전대칭)은 고정(Pv=v), j=1/2 은 m별 2×2 multiplicity block 내부만 혼합.
  4. teeth: 틀린 각도(0.9θ_cg)·sector 교차 열교환은 witness 가 검출해야.

정직 경계(INV-Q3, seal 아님, root 불변):
  - 봉인 = schur3 회로==CG golden exact(C-app) 뿐. J²/Jz 대각화·duality = 관측(witness).
  - n≥4 Schur·S₃ irrep 레지스터 명시 분리 = 차기. 신규 봉인 0.

사용: python scripts/schur_observe.py [--quick]
"""
import os, sys, re, json
from functools import reduce
import numpy as np

from qf_witness.core.paths import ROOT
OUT = os.path.join(ROOT, ".pgf", "proofs", "SCHUR-OBSERVE.json")
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
NQ = 3
DIM = 8


def emb(op, q):
    return reduce(np.kron, [op if i == q else I for i in range(NQ)])


def load_golden(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    ns = {}
    exec(re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1), ns)
    return ns["golden"]


def total_ops():
    Jx = sum(emb(X, q) for q in range(NQ)) / 2.0
    Jy = sum(emb(Y, q) for q in range(NQ)) / 2.0
    Jz = sum(emb(Z, q) for q in range(NQ)) / 2.0
    return Jx @ Jx + Jy @ Jy + Jz @ Jz, Jz


def qubit_swap(a, b):
    M = np.zeros((DIM, DIM), dtype=complex)
    for x in range(DIM):
        bits = [(x >> (NQ - 1 - i)) & 1 for i in range(NQ)]
        bits[a], bits[b] = bits[b], bits[a]
        M[sum((bits[i] & 1) << (NQ - 1 - i) for i in range(NQ)), x] = 1.0
    return M


def offdiag(M):
    return float(np.abs(M - np.diag(np.diag(M))).max())


def witness(U):
    """J²/Jz 동시대각 + 스펙트럼 + S₃ sector 보존 판정 (True/False)."""
    J2, Jz = total_ops()
    A = U.conj().T @ J2 @ U
    B = U.conj().T @ Jz @ U
    if offdiag(A) > 1e-9 or offdiag(B) > 1e-9:
        return False, {"offdiag_J2": offdiag(A), "offdiag_Jz": offdiag(B)}
    j2d = np.real(np.diag(A))
    jzd = np.real(np.diag(B))
    if sorted(np.round(j2d, 9).tolist()) != [0.75] * 4 + [3.75] * 4:
        return False, {"J2_diag": j2d.tolist()}
    # label map: 000/001/101/111 → j=3/2 (m=+3/2,+1/2,−1/2,−3/2) · 100/010(+½)·011/110(−½) → j=1/2
    lm = {0: (3.75, 1.5), 1: (3.75, 0.5), 5: (3.75, -0.5), 7: (3.75, -1.5),
          4: (0.75, 0.5), 2: (0.75, 0.5), 3: (0.75, -0.5), 6: (0.75, -0.5)}
    for k, (j2, m) in lm.items():
        if abs(j2d[k] - j2) > 1e-9 or abs(jzd[k] - m) > 1e-9:
            return False, {"label": k, "got": (j2d[k], jzd[k]), "want": (j2, m)}
    # Schur-Weyl duality: 전치 3종 sector 보존
    sym_cols = [0, 1, 5, 7]                        # j=3/2 완전대칭 → P v = v
    blocks = [[4, 2], [3, 6]]                      # j=1/2 multiplicity 2×2 (m=+½ / m=−½)
    for (a, b) in [(0, 1), (1, 2), (0, 2)]:
        P = qubit_swap(a, b)
        PU = U.conj().T @ P @ U                    # Schur 기저에서의 전치
        for c in sym_cols:
            e = np.zeros(DIM); e[c] = 1.0
            if not np.allclose(PU @ e, e, atol=1e-9):
                return False, {"transposition": (a, b), "sym_col_not_fixed": c}
        for blk in blocks:
            comp = [k for k in range(DIM) if k not in blk]
            if np.abs(PU[np.ix_(comp, blk)]).max() > 1e-9:
                return False, {"transposition": (a, b), "block_leak": blk}
    return True, {"offdiag_J2": offdiag(A), "offdiag_Jz": offdiag(B)}


def observe():
    U = load_golden("schur3.app.pg")
    unitary = bool(np.allclose(U.conj().T @ U, np.eye(DIM), atol=1e-9))
    ok_main, detail = witness(U)

    # teeth 1: 틀린 CG 각(0.9·arccos⅓) 주입 — G1 자리에 잘못된 2-level 회전
    th = 0.9 * np.arccos(1.0 / 3.0)
    Gbad = np.eye(DIM, dtype=complex)
    c, s = np.cos(th / 2), np.sin(th / 2)
    Gbad[1, 1], Gbad[1, 4], Gbad[4, 1], Gbad[4, 4] = c, -s, s, c
    bad1_ok, _ = witness(U @ Gbad)
    # teeth 2: sector 교차 열교환(001↔100: j=3/2 ↔ j=1/2, 같은 m=+½) — Jz 유지되나 J² label 깨짐
    Uswap = U.copy()
    Uswap[:, [1, 4]] = Uswap[:, [4, 1]]
    bad2_ok, _ = witness(Uswap)
    teeth = (not bad1_ok) and (not bad2_ok)

    ok = unitary and ok_main and teeth
    return {"axis": "Schur-Weyl transform (3-qubit, SU(2)×S₃ duality)",
            "sealed_asset": "schur3 (encoder: 계산기저 label → Schur 기저, CG cascade)",
            "unitary": unitary,
            "simultaneous_diagonal_J2_Jz": ok_main, "witness_detail": detail,
            "spectrum": "J² {3.75×4, 0.75×4} = spin-3/2 ⊕ spin-1/2×2 · Jz label map 정합",
            "s3_duality_sector_preserving": ok_main,
            "teeth_wrong_angle_and_sector_swap_detected": teeth,
            "honest_boundary": "봉인=schur3 회로==CG golden exact(C-app) 뿐. J²/Jz 대각화·S₃ duality=관측 witness. "
                               "n≥4 Schur·irrep 레지스터 분리=차기. 신규 봉인 0(INV-Q3).",
            "ok": bool(ok)}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        report = {"_schema": "schur-observe-v1",
                  "_note": "3-qubit Schur transform J²/Jz 동시대각 + S₃ duality witness. 봉인=schur3 뿐(INV-Q3). 신규 봉인 0.",
                  "observation": res}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("Schur-Weyl transform witness 관측:", flush=True)
        print(f"  U†J²U·U†JzU 동시대각: {res['simultaneous_diagonal_J2_Jz']} · 스펙트럼 3.75×4/0.75×4 ✓ · unitary: {res['unitary']}", flush=True)
        print(f"  S₃ 전치 sector 보존(duality): {res['s3_duality_sector_preserving']} · teeth(틀린각·sector교환) 검출: {res['teeth_wrong_angle_and_sector_swap_detected']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"schur_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
