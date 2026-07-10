#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hecke_h3_observe — TrackHE11 P6: Hecke 대수 H₃(q=i) Burau 표현 witness (관측, seal 아님).

report11 수렴축(Hecke H₃, 3/8). §3j "Hecke 브레이드(H₃(q=i) Burau·Markov trace) 예비" 강화. TrackHE10 P4
`mtc_braid_observe`(Ising/Fibonacci, TQFT/융합 층)의 **대수적 뼈대 층 상보**: braid 군의 q-변형 대수(Hecke).

관측(ℤ[i]⊂ℤ[ζ₈] exact — ★승인 게이트 0):
  1. H₃(q) = 3-strand type-A₂ Hecke 대수. 생성원 T₁,T₂: **Hecke 이차식** T_i²=(q−1)T_i+q (고유값 {q,−1}) +
     **braid 관계** T₁T₂T₁=T₂T₁T₂. q=i 에서 2-dim 표현: T₁=[[i,1],[0,−1]]·T₂=[[−1,0],[i,i]].
  2. ★**승인 게이트 0**: q=i ∈ ℤ[i] = ℤ[ζ₄] ⊂ **ℤ[ζ₈]**(path-sum framework 기승인) → 신규 surd 불필요.
     표현행렬 성분 전부 Gaussian 정수. Yang-Baxter = 정수 행렬 항등.
  3. ★**Ising 대수 뼈대**(agent08): Jones q=e^{2πi/(k+2)}, q=i=e^{iπ/2} → k+2=4 → **k=2 = SU(2)₂ = Ising TQFT**.
     즉 H₃(q=i) Burau 는 봉인 Ising fusion(HE9 P6)·Ising braid(HE10 P4)의 대수적 뼈대.
  4. ★**정직 정정**(agent04·자체): q=i 에서 **q+q⁻¹ = i+(−i) = 0** → Markov trace 정규화 1/(q+q⁻¹) 가 **특이**
     (Jones 다항식 정규화 특이점). Burau 표현·braid 관계는 유효하나, Markov trace/Jones 값은 정규화 특이 —
     비정규화 trace(Tr(T₁T₂) 등)만 exact 관측. (q=i normalization 함정, agent04 지적 정확.)
  5. teeth: 가짜 생성원(고유값 오류)은 braid 관계 붕괴.

정직 경계(★관측·seal 아님, root 불변 sidecar): witness = Hecke H₃(q=i) Burau 표현 대수(이차식·braid·ℤ[i]).
  ★MTC braid(HE10 P4, TQFT 층)와 **대수층 상보**(Hecke=braid 군 q-변형). Markov trace 정규화=q=i 특이(관측만)·
  일반 q Jones·Hₙ(n>3)·knot 불변량=차기/범위밖. 신규 module 0. [[mtc-braid-observe]]·Ising 계보 교차.

사용: python -m qf_witness.observe.hecke_h3_observe [--quick]
"""
from __future__ import annotations
import sys
import numpy as np

Q = 1j                                                  # q = i


def _is_gaussian_int(M):
    return all(abs(x.real - round(x.real)) < 1e-9 and abs(x.imag - round(x.imag)) < 1e-9
               for x in np.asarray(M).flatten())


def main():
    quick = "--quick" in sys.argv
    R = {}
    I2 = np.eye(2, dtype=complex)
    T1 = np.array([[Q, 1], [0, -1]], dtype=complex)
    T2 = np.array([[-1, 0], [Q, Q]], dtype=complex)

    # 1. Hecke 이차식 T_i²=(q−1)T_i+q (고유값 {q,−1})
    R["hecke_quadratic_T1"] = np.allclose(T1 @ T1, (Q - 1) * T1 + Q * I2)
    R["hecke_quadratic_T2"] = np.allclose(T2 @ T2, (Q - 1) * T2 + Q * I2)
    ev1 = sorted(np.linalg.eigvals(T1), key=lambda z: (z.real, z.imag))
    R["eigenvalues_q_and_minus1"] = (any(abs(e - Q) < 1e-9 for e in ev1)
                                     and any(abs(e + 1) < 1e-9 for e in ev1))

    # 2. braid 관계 T₁T₂T₁=T₂T₁T₂ (Yang-Baxter)
    R["braid_yang_baxter"] = np.allclose(T1 @ T2 @ T1, T2 @ T1 @ T2)

    # 3. ★승인 게이트 0: 성분 ∈ ℤ[i] ⊂ ℤ[ζ₈]
    R["entries_gaussian_integers_gate0"] = (_is_gaussian_int(T1) and _is_gaussian_int(T2))

    # 4. ★Ising 대수 뼈대: q=i=e^{iπ/2} → k+2=4 → k=2 (SU(2)₂=Ising)
    R["q_i_maps_to_ising_k2"] = bool(abs(Q - np.exp(1j * np.pi / 2)) < 1e-12)   # q=e^{iπ/2}=e^{2πi/4}=ζ₄

    # 5. ★정직 정정: q+q⁻¹=0 (Markov trace 정규화 특이)
    R["markov_normalization_singular_at_q_i"] = bool(abs(Q + 1 / Q) < 1e-12)    # i+(-i)=0

    # 비정규화 trace 는 exact (Gaussian 정수)
    R["unnormalized_trace_exact"] = (_is_gaussian_int([np.trace(T1 @ T2)])
                                     and _is_gaussian_int([np.trace(T1)]))

    # teeth: 가짜 생성원(고유값 {1,-1}) 은 braid 관계 성립하나 Hecke 이차식(q=i) 붕괴
    fake = np.array([[1, 1], [0, -1]], dtype=complex)   # 고유값 {1,-1} (q=1, 대칭군)
    R["teeth_fake_generator_breaks_hecke"] = (not np.allclose(fake @ fake, (Q - 1) * fake + Q * I2))

    ok = all(R.values())
    if not quick:
        print("Hecke 대수 H₃(q=i) Burau 표현 관측 (MTC braid 대수층 상보, witness — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  T₁=[[i,1],[0,−1]]·T₂=[[−1,0],[i,i]] ∈ ℤ[i] · 고유값{{q,−1}} · Hecke 이차식 · braid Yang-Baxter",
              flush=True)
        print("  ★승인 게이트 0(q=i∈ℤ[i]⊂ℤ[ζ₈]) · Ising 대수 뼈대(q=i→k=2=SU(2)₂=Ising TQFT, HE9/HE10 봉인). "
              "★정직 정정(agent04): q+q⁻¹=0 → Markov trace 정규화 특이(비정규화 trace만 exact 관측).", flush=True)
        print("  ★관측: MTC braid(TQFT 층)와 대수층 상보. 일반 q Jones·Hₙ(n>3)=차기·신규 module 0·root 불변 sidecar.",
              flush=True)
    print(f"hecke_h3_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
