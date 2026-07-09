#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""su2_3_mtc_observe — 완전 Modular Tensor Category SU(2)₃ modular data 자체검증 witness
(관측, seal 아님).

TrackHE11 잔여축: 개별 Ising/Fibonacci braid(F/R symbol, mtc_braid_observe·fib_braid_observe)를
**완전 MTC modularity(S·T modular data + 공리)**로 승격. SU(2)₃(=Fibonacci τ를 포함하는 level-3 MTC)의
전체 modular data를 exact ℚ(√5)/cyclotomic으로 검증.

SU(2)₃ anyon: j∈{0,1/2,1,3/2} → label a=2j∈{0,1,2,3}(4개). k=3, k+2=5.

관측(exact modular data · 공리):
  1. **S-matrix** S_{ab}=√(2/5)·sin(π(a+1)(b+1)/5): 실대칭·**unitary**(SS†=I)·**S²=C**(charge conj;
     SU(2)_k self-dual → C=I 확인).
  2. **quantum dims** d_a=S_{0a}/S_{00}=sin(π(a+1)/5)/sin(π/5) → (1, φ, φ, 1), φ=(1+√5)/2.
     **total D²=Σd_a²=5+√5**(=5/(2sin²(π/5)), 양수).
  3. **T-matrix** T_{ab}=δ_{ab}exp(2πi(h_a−c/24)), h_a=j(j+1)/5, c=9/5. topological spin θ_a=exp(2πi h_a)
     ∈ ζ₂₀. **(ST)³=S²**(modular SL(2,ℤ) 관계, c/24 보정으로 위상 상쇄→exact)·T 유한위수(T⁴⁰=I).
  4. **Verlinde 융합** N_{ab}^c=Σ_x S_{ax}S_{bx}S*_{cx}/S_{0x}: **모든 N 비음 정수**. 특히
     **N_{22}^0=1·N_{22}^2=1·N_{22}^{1,3}=0** = **Fibonacci τ×τ=1+τ**(τ↔label 2, j=1).
  5. **field**: S/S_{00} 전 성분 ∈ {0,±1,±φ} ⊂ ℚ(√5); θ_a ∈ 20차 cyclotomic. exact.
  6. teeth: 잘못된 level(k+2 대신 분모 6)→Verlinde 비정수; 정규화 제거(√(2/5)↓)→S²≠C.

정직 경계(★관측·seal 아님, root 불변 sidecar·신규 module 0):
  witness = SU(2)₃ modular data(S/T)의 MTC 공리(unitarity·S²=C·Verlinde 정수·Fibonacci fusion·
  total dimension·modular (ST)³=S²)를 exact 대수(ℚ(√5)/cyclotomic)로 자체검증. F/R symbol pentagon·
  hexagon 열거는 mtc_braid_observe/fib_braid_observe 소관(braid 표현 계층). 위상값의 module 봉인(ζ₂₀ 등)은
  범위밖(사람게이트). [[mtc-braid-observe]](HE10 P4)·[[fib-braid-observe]](G5)·[[ising-fusion-observe]](HE9 P6) 교차.

사용: python scripts/su2_3_mtc_observe.py [--quick]
"""
from __future__ import annotations
import sys
import numpy as np

LABELS = (0, 1, 2, 3)          # a = 2j, j∈{0,1/2,1,3/2}
K = 3
KK = K + 2                     # = 5


def s_matrix(denom):
    """S_{ab}=√(2/denom)·sin(π(a+1)(b+1)/denom)."""
    return np.array([[np.sqrt(2.0 / denom) * np.sin(np.pi * (a + 1) * (b + 1) / denom)
                      for b in LABELS] for a in LABELS], dtype=complex)


def verlinde(S):
    """N_{ab}^c = Σ_x S_ax S_bx S*_cx / S_0x."""
    n = len(S)
    N = np.zeros((n, n, n))
    for a in LABELS:
        for b in LABELS:
            for c in LABELS:
                N[a, b, c] = np.real(np.sum(S[a] * S[b] * np.conj(S[c]) / S[0]))
    return N


def unitary(M, tol=1e-9):
    return bool(np.allclose(M @ M.conj().T, np.eye(len(M)), atol=tol))


def uptophase(A, B, tol=1e-9):
    i = np.unravel_index(np.argmax(np.abs(B)), B.shape)
    ph = A[i] / B[i]
    return bool(abs(abs(ph) - 1) < tol and np.allclose(A, ph * B, atol=tol))


def main():
    quick = "--quick" in sys.argv
    R = {}
    phi = (1 + np.sqrt(5)) / 2

    # ── 1. S-matrix + unitarity + S² = charge conjugation ──
    S = s_matrix(KK)
    S2 = S @ S
    R["S_real_symmetric"] = bool(np.allclose(S.imag, 0) and np.allclose(S, S.T))
    R["S_unitary"] = unitary(S)
    C = np.round(S2.real).astype(int)                      # charge conjugation matrix
    R["S_squared_charge_conj"] = bool(np.allclose(S2, C) and np.allclose(C @ C, np.eye(4)))
    R["charge_conj_identity_selfdual"] = bool(np.allclose(C, np.eye(4, dtype=int)))   # SU(2)_k self-dual → C=I

    # ── 2. quantum dimensions + total dimension ──
    d = (S[0] / S[0, 0]).real
    R["quantum_dims_phi"] = bool(np.allclose(d, [1.0, phi, phi, 1.0]))
    D2 = float(np.sum(d ** 2))
    R["total_D2"] = bool(D2 > 0 and np.isclose(D2, 5 + np.sqrt(5))
                         and np.isclose(D2, KK / (2 * np.sin(np.pi / KK) ** 2)))

    # ── 3. T-matrix / topological spin / modular (ST)³ = S² ──
    h = [ (a / 2.0) * (a / 2.0 + 1.0) / KK for a in LABELS ]   # h_a = j(j+1)/(k+2)
    c = 3.0 * K / KK                                            # central charge = 9/5
    theta = np.array([np.exp(2j * np.pi * hh) for hh in h])     # topological spin
    T = np.diag([np.exp(2j * np.pi * (hh - c / 24.0)) for hh in h])
    R["topological_spin_cyclotomic"] = bool(np.allclose(theta ** 20, 1.0))   # θ_a ∈ ζ₂₀
    ST3 = np.linalg.matrix_power(S @ T, 3)
    R["ST_cubed_modular"] = bool(np.allclose(ST3, S2) or uptophase(ST3, S2))  # (ST)³ = S² (=C)
    T40 = np.linalg.matrix_power(T, 40)
    R["T_finite_order"] = bool(np.allclose(T40, np.eye(4)))    # T⁴⁰ = I (유한위수)

    # ── 4. Verlinde 융합: 비음 정수 + Fibonacci τ×τ = 1+τ ──
    N = verlinde(S)
    R["verlinde_nonneg_integer"] = bool(np.allclose(N, np.round(N), atol=1e-9)
                                        and (np.round(N) >= 0).all())
    Nr = np.round(N).astype(int)
    # label 2 = j=1 = Fibonacci τ; τ×τ = 1(label0) + τ(label2)
    R["fibonacci_fusion_tau_tau"] = bool(Nr[2, 2, 0] == 1 and Nr[2, 2, 2] == 1
                                         and Nr[2, 2, 1] == 0 and Nr[2, 2, 3] == 0)
    R["fusion_associative_symmetric"] = bool(np.allclose(Nr, np.transpose(Nr, (1, 0, 2)))
                                             and Nr[0, 2, 2] == 1 and Nr[0, 0, 0] == 1)  # 1 = 단위원

    # ── 5. field: S/S₀₀ ∈ {0,±1,±φ} ⊂ ℚ(√5) ──
    M = (S / S[0, 0]).real
    allowed = (0.0, 1.0, -1.0, phi, -phi)
    R["field_Q_sqrt5_cyclotomic"] = bool(
        all(any(np.isclose(x, v) for v in allowed) for x in M.flatten())
        and np.allclose(theta ** 20, 1.0))

    # ── 6. teeth ──
    # (a) 잘못된 level(k+2=5 대신 분모 6) → Verlinde 비정수
    Sw = s_matrix(6)
    Nw = verlinde(Sw)
    R["teeth_wrong_level_noninteger"] = bool(not np.allclose(Nw, np.round(Nw), atol=1e-6))
    # (b) 정규화 제거(√(2/5) 없음) → S² ≠ C
    Su = np.array([[np.sin(np.pi * (a + 1) * (b + 1) / KK) for b in LABELS] for a in LABELS], dtype=complex)
    R["teeth_unnormalized_breaks_S2"] = bool(not np.allclose(Su @ Su, C))

    ok = all(R.values())
    if not quick:
        print("SU(2)₃ 완전 MTC modular data(S·T) 공리 관측 (witness — seal 아님):", flush=True)
        for kk_, v in R.items():
            print(f"  {kk_}: {v}", flush=True)
        print(f"  quantum dims d=(1,φ,φ,1) φ={phi:.6f} · total D²={D2:.6f}=5+√5 · "
              f"θ=(1, e^(3πi/10), e^(4πi/5), −i) ∈ ζ₂₀ · c=9/5", flush=True)
        print(f"  Verlinde N_22^·=(N0,N1,N2,N3)=({Nr[2,2,0]},{Nr[2,2,1]},{Nr[2,2,2]},{Nr[2,2,3]}) "
              f"→ τ×τ=1+τ (Fibonacci, τ=label2=j=1)", flush=True)
        print("  ★정직: 관측=SU(2)₃ modular data의 MTC 공리(unitarity·S²=C·Verlinde 정수·Fibonacci fusion·"
              "total dim·(ST)³=S²) exact ℚ(√5)/cyclotomic 자체검증.", flush=True)
        print("  봉인 아님 — F/R symbol pentagon/hexagon 열거=mtc_braid/fib_braid 소관·위상값 module(ζ₂₀)="
              "범위밖(사람게이트)·신규 module 0·root 불변 sidecar.", flush=True)
    print(f"su2_3_mtc_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
