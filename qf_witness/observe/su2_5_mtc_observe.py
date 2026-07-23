#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""su2_5_mtc_observe — TrackHE17 잔여: SU(2)₅ 모듈러 텐서 범주(MTC) 완전 modular data
(관측, seal 아님). report17 잔여(6축 밖·§3j "SU(2)_k(k≥5) 재평가").

기존 MTC 계보(SU(2)₂ Ising·SU(2)₃ Fibonacci·SU(2)₄·D(S₃)/D(D₄) double)의 다음 준위. SU(2)₅ =
level-5 WZW, **6 anyon**(j=0,½,1,3/2,2,5/2). 전 modular data(S,T,Verlinde,D²)를 mpmath 고정밀
자체유도한다. ★**§4′(o) 외부 수치 오류 포착**: report17 agent06 의 D²=7/(4sin²(π/7))≈12.99 는
**틀림** — 자체유도(Σ_{n=1}^{6} sin²(nπ/7)=7/2 항등식)로 **D²=7/(2sin²(π/7))≈18.59** 가 정확(factor-2).

관측 5축(mpmath dps=40 고정밀 — 초월수 exact 관계식):
  A. **6 anyon·양자차원**: d_j = sin((2j+1)π/7)/sin(π/7) = [2j+1]_q (q=e^{iπ/7}) → [1, [2], [3], [3], [2], 1]
     ≈ [1, 1.802, 2.247, 2.247, 1.802, 1] (self-dual 대칭·d_0=d_{5/2}=1).
  B. **★D² = Σd_j² = 7/(2 sin²(π/7)) ≈ 18.592** (자체유도·★agent06 의 /4 오류 정정). 항등식
     Σ_{n=1}^{K-1} sin²(nπ/K)=K/2 (K=7) 로 exact.
  C. **S-matrix**: S_{ab}=√(2/7) sin((a+1)(b+1)π/7) (a,b=2j) — **대칭·유니터리**·S_{0a}/S_{00}=d_a·
     **S²=C(charge conj, self-dual→I)·S⁴=1**.
  D. **Verlinde fusion**: N_{ab}^c = Σ_x S_ax S_bx S̄_cx/S_0x — **전부 비음정수** 전수(6³=216) 자체검증.
  E. **T-matrix·modular**: h_j=j(j+1)/7·central charge c=3·5/7=**15/7**·T_j=exp(2πi(h_j−c/24))·
     **(ST)³ = λ·S²**(모듈러 관계·λ=phase 산출). 부호장 ℚ(cos π/7)[S]·ζ₂₈[T].
  teeth: (i) ★agent06 D² 오류 대조(12.99 vs 정확 18.59) (ii) SU(2)₄ D²=12 와 구분(다른 MTC)
     (iii) Verlinde 음수 검출 시 비-MTC.

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - modular data = **조합적 exact 표**(mpmath 고정밀·초월수 관계식) — §2 Fourier 실봉인 경계 무관
    (D(S₃)/D(D₄) 선례). braiding 유니터리 honest 게이트 분해는 무주장(관측).
  - D² 는 **자체유도**(항등식) — 외부 인용 아님·agent06 수치 오류 정정(§4′o).
  - central charge·spin 은 CFT 사실(관측) — 봉인 자산 아님.

사용: python -m qf_witness.observe.su2_5_mtc_observe [--quick]
"""
from __future__ import annotations
import sys
import json

import mpmath as mp


def main():
    quick = "--quick" in sys.argv
    mp.mp.dps = 30 if quick else 40
    R = {}
    k = 5
    K = k + 2                        # = 7
    labels = list(range(k + 1))     # 2j = 0..5 → 6 anyons
    TOL = mp.mpf(10) ** (-(20 if quick else 25))

    out = {"_schema": "su2-5-mtc/v1",
           "_note": ("SU(2)₅ MTC 완전 modular data(6 anyon) — 관측·seal 아님·module 0·root 불변. "
                     "mpmath 고정밀 자체유도. ★D²=7/(2sin²π/7)(agent06 /4 오류 정정)·Verlinde 정수·"
                     "(ST)³∝S². modular data=조합 exact 표(§2 Fourier 경계 무관).")}

    # ── A. 양자차원 ───────────────────────────────────────────────────────
    def qdim(a):
        return mp.sin((a + 1) * mp.pi / K) / mp.sin(mp.pi / K)
    d = [qdim(a) for a in labels]
    R["A_6_anyons"] = (len(labels) == 6)
    R["A_selfdual_dims"] = (abs(d[0] - 1) < TOL and abs(d[5] - 1) < TOL
                            and abs(d[1] - d[4]) < TOL and abs(d[2] - d[3]) < TOL)
    out["quantum_dims"] = [mp.nstr(x, 8) for x in d]

    # ── B. D² 자체유도 + agent06 오류 정정 ────────────────────────────────
    D2 = sum(x * x for x in d)
    D2_correct = K / (2 * mp.sin(mp.pi / K) ** 2)         # 7/(2sin²π/7)
    D2_agent06 = K / (4 * mp.sin(mp.pi / K) ** 2)         # 7/(4sin²π/7) — 틀림
    R["B_D2_correct_formula"] = (abs(D2 - D2_correct) < TOL)
    R["B_agent06_D2_wrong"] = (abs(D2 - D2_agent06) > mp.mpf("0.5"))   # factor-2 불일치
    out["total_dim_squared"] = {"value": mp.nstr(D2, 12),
                                "formula_correct": "7/(2 sin²(π/7)) ≈ 18.592",
                                "agent06_wrong": "7/(4 sin²(π/7)) ≈ 9.296 (or 12.99) — factor-2 오류",
                                "identity": "Σ_{n=1}^{6} sin²(nπ/7) = 7/2"}

    # ── C. S-matrix ──────────────────────────────────────────────────────
    def Sel(a, b):
        return mp.sqrt(mp.mpf(2) / K) * mp.sin((a + 1) * (b + 1) * mp.pi / K)
    S = [[Sel(a, b) for b in labels] for a in labels]
    R["C_S_symmetric"] = all(abs(S[a][b] - S[b][a]) < TOL for a in labels for b in labels)
    R["C_S_unitary"] = all(abs(sum(S[i][l] * mp.conj(S[j][l]) for l in labels) - (1 if i == j else 0)) < TOL
                           for i in labels for j in labels)
    R["C_S0a_gives_dim"] = all(abs(S[0][a] / S[0][0] - d[a]) < TOL for a in labels)
    # S² = C (charge conj, self-dual → I)
    S2 = [[sum(S[i][l] * S[l][j] for l in labels) for j in labels] for i in labels]
    R["C_S2_charge_conj"] = all(abs(S2[i][j] - (1 if i == j else 0)) < TOL
                                for i in labels for j in labels)     # self-dual → I
    out["S_matrix_00"] = mp.nstr(S[0][0], 8)

    # ── D. Verlinde fusion 비음정수 ───────────────────────────────────────
    def Nfus(a, b, c):
        return sum(S[a][x] * S[b][x] * mp.conj(S[c][x]) / S[0][x] for x in labels)
    allint = True
    negfound = False
    for a in labels:
        for b in labels:
            for c in labels:
                v = Nfus(a, b, c)
                nv = mp.nint(v.real)
                if abs(v - nv) > TOL or abs(v.imag) > TOL:
                    allint = False
                if nv < -TOL:
                    negfound = True
    R["D_verlinde_integer"] = allint
    R["D_verlinde_nonneg"] = (not negfound)
    # 대표 fusion: ½ × ½ = 0 + 1 (N_{1,1}^0=1, N_{1,1}^2=1)
    R["D_fusion_half_half"] = (abs(Nfus(1, 1, 0) - 1) < TOL and abs(Nfus(1, 1, 2) - 1) < TOL
                               and abs(Nfus(1, 1, 4)) < TOL)
    out["fusion_sample"] = {"½×½": "0 + 1 (N=1 each)"}

    # ── E. T-matrix·modular ──────────────────────────────────────────────
    c_central = mp.mpf(3 * k) / K       # 15/7
    def hj(a):
        jj = mp.mpf(a) / 2
        return jj * (jj + 1) / K
    Tdiag = [mp.exp(2j * mp.pi * (hj(a) - c_central / 24)) for a in labels]
    R["E_central_charge_15_7"] = (abs(c_central - mp.mpf(15) / 7) < TOL)
    # (ST)³ = λ S²
    ST = [[S[i][j] * Tdiag[j] for j in labels] for i in labels]
    def matmul(A, B):
        return [[sum(A[i][l] * B[l][j] for l in labels) for j in labels] for i in labels]
    ST3 = matmul(matmul(ST, ST), ST)
    lam = ST3[0][0] / S2[0][0]
    R["E_ST3_prop_S2"] = all(abs(ST3[i][j] - lam * S2[i][j]) < TOL for i in labels for j in labels)
    out["T_matrix"] = {"central_charge": mp.nstr(c_central, 8),
                       "spins_h": [mp.nstr(hj(a), 6) for a in labels],
                       "ST3_over_S2_phase": mp.nstr(lam, 8)}

    # ── teeth ─────────────────────────────────────────────────────────────
    R["teeth_agent06_D2_caught"] = (abs(D2 - D2_agent06) > mp.mpf("0.5"))    # §4′o
    R["teeth_distinct_from_su2_4"] = (abs(D2 - 12) > mp.mpf("1"))            # SU(2)₄ D²=12 아님
    R["teeth_6_not_5_anyons"] = (len(labels) == 6)                          # SU(2)₄=5 아님

    ok = bool(all(R.values()))
    out["checks"] = R
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "SU2-5-MTC.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("SU(2)₅ MTC 완전 modular data 관측 (mpmath 고정밀 — seal 아님):", flush=True)
        for kk, v in R.items():
            print(f"  {kk}: {v}", flush=True)
        print(f"  ★6 anyon·양자차원 {[mp.nstr(x,5) for x in d]}", flush=True)
        print(f"  ★D²=Σd²={mp.nstr(D2,8)}=7/(2sin²π/7) (agent06 /4≈{mp.nstr(D2_agent06,5)} 오류 정정)", flush=True)
        print(f"  ★Verlinde 비음정수·(ST)³=phase·S²·c=15/7", flush=True)
        print("  ★정직: 조합 exact 표(관측)·§2 Fourier 경계 무관·braiding 게이트 무주장", flush=True)
        print("  → .pgf/proofs/SU2-5-MTC.json", flush=True)
    print(f"su2_5_mtc_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
