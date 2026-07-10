#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""temperley_lieb_observe — Temperley-Lieb TL_n(δ=2) 정수 행렬 표현 witness (관측, seal 아님).

Hecke H₃(q=i) (`hecke_h3_observe`)의 **정수층 상보**. 거기서 q+q⁻¹=i+(−i)=0 가 Markov trace 정규화
특이였다(Jones 정규화 함정). 본 witness 는 그 **특수점의 정수 실현**: TL 루프값 δ=−(q+q⁻¹) 에서 q=−1 을
잡으면 δ=2 → 생성원 e_i 의 표준 표현 성분이 **전부 정수**(ℤ, ℤ[i]조차 아님). Hecke q=i(ℤ[i]) 와 대조.

관측(순수 ℤ — 승인 게이트 0):
  1. TL_n(δ) 생성원 e_1,…,e_{n-1} 관계: (i) e_i²=δ·e_i · (ii) e_i e_{i±1} e_i = e_i ·
     (iii) e_i e_j = e_j e_i (|i−j|≥2). δ=2 고정.
  2. 표준 (ℂ²)^⊗n 표현: e_i 는 사이트 (i,i+1) 에 작용하는 rank-1 연산자 δ배. Kauffman δ=−A²−A⁻²,
     A²=−1(A=i) → δ=2. 2-site 블록 = |ψ⟩⟨ψ|, |ψ⟩=|01⟩−|10⟩ (singlet 방향, ⟨ψ|ψ⟩=2=δ) →
     [[0,0,0,0],[0,1,−1,0],[0,−1,1,0],[0,0,0,0]] **정수 4×4**. e²=2e (eigenvalue 2 on singlet).
  3. n=4 로 세 관계 전부 커버: e_1=block⊗I⊗I · e_2=I⊗block⊗I · e_3=I⊗I⊗block (16×16 정수). |1−3|=2 → far commute 비자명.
  4. Kauffman braid: σ_i = A·I + A⁻¹·e_i, A=i → braid 관계 σ_i σ_{i+1} σ_i = σ_{i+1} σ_i σ_{i+1} (TL 로부터 유도, ℤ[i] 성분).
  5. teeth: δ=3 로 같은 정수 블록을 쓰면 e²=2e≠3e → 관계 붕괴(δ=2 고정성).

정직 경계(★관측·seal 아님, root 불변 sidecar): witness = TL_n(δ=2) 정수 표현의 생성원 관계·braid 유도.
  ★Hecke H₃(q=i, q+q⁻¹=0 Markov특이)의 정수 상보(δ=−(q+q⁻¹)=2, q=−1). 일반 δ Jones·TL_n(n>4)·knot 불변량=범위밖.
  신규 module 0. [[hecke-h3-observe]] 교차.

사용: python -m qf_witness.observe.temperley_lieb_observe [--quick]
"""
from __future__ import annotations
import sys
import numpy as np

DELTA = 2                                                # δ = 2 = −(q+q⁻¹), q = −1


def _is_integer(M):
    return all(abs(x.real - round(x.real)) < 1e-9 and abs(x.imag) < 1e-9
               for x in np.asarray(M).flatten())


def _is_gaussian_int(M):
    return all(abs(x.real - round(x.real)) < 1e-9 and abs(x.imag - round(x.imag)) < 1e-9
               for x in np.asarray(M).flatten())


def _kron(*mats):
    out = mats[0]
    for m in mats[1:]:
        out = np.kron(out, m)
    return out


def main():
    quick = "--quick" in sys.argv
    R = {}
    I2 = np.eye(2, dtype=complex)

    # 2-site TL 블록: |ψ⟩=|01⟩−|10⟩ (singlet), block=|ψ⟩⟨ψ|, ⟨ψ|ψ⟩=δ=2. 정수 4×4.
    block = np.array([[0, 0, 0, 0],
                      [0, 1, -1, 0],
                      [0, -1, 1, 0],
                      [0, 0, 0, 0]], dtype=complex)

    # 블록 자체: e²=δe, trace=δ, 정수
    R["block_e_squared_delta_e"] = np.allclose(block @ block, DELTA * block)
    R["block_trace_is_delta"] = bool(abs(np.trace(block) - DELTA) < 1e-9)
    R["block_integer"] = _is_integer(block)

    # n=4 표현: e_1,e_2,e_3 (16×16 정수)
    e1 = _kron(block, I2, I2)                             # 사이트 (1,2)
    e2 = _kron(I2, block, I2)                             # 사이트 (2,3)
    e3 = _kron(I2, I2, block)                             # 사이트 (3,4)
    es = [e1, e2, e3]

    # (i) e_i² = δ e_i, 성분 정수
    R["e_squared_delta_e_integer"] = all(
        np.allclose(e @ e, DELTA * e) and _is_integer(e @ e) for e in es)

    # (ii) e_i e_{i±1} e_i = e_i (인접 삼중곱)
    R["e_i_ei1_ei_relation"] = (np.allclose(e1 @ e2 @ e1, e1)
                                and np.allclose(e2 @ e1 @ e2, e2)
                                and np.allclose(e2 @ e3 @ e2, e2)
                                and np.allclose(e3 @ e2 @ e3, e3))

    # (iii) e_1 e_3 = e_3 e_1 (|1−3|=2 ≥ 2, 비자명 far commute)
    R["far_commute"] = np.allclose(e1 @ e3, e3 @ e1)

    # 3. 모든 e_i 및 곱 결과 성분 ∈ ℤ (순수 정수 — δ=2 덕분, Hecke q=i의 ℤ[i]와 대조)
    R["all_entries_integer"] = all(_is_integer(e) for e in es) and _is_integer(e1 @ e2 @ e1)

    # 4. Hecke 상보 명시: TL δ=−(q+q⁻¹)=2 ↔ q=−1; Hecke H₃ q=i 는 q+q⁻¹=0 (Markov 특이).
    q_tl = -1.0 + 0j
    R["hecke_qi_complementary"] = (bool(abs(DELTA - (-(q_tl + 1 / q_tl))) < 1e-12)   # δ=−(q+q⁻¹), q=−1
                                   and bool(abs((1j) + 1 / (1j)) < 1e-12))            # Hecke q=i: q+q⁻¹=0

    # 5. Kauffman braid: σ_i = A·I + A⁻¹·e_i, A=i (A²=−1 → δ=−A²−A⁻²=2). ℤ[i] 성분, braid 관계 유도.
    A = 1j
    dim = e1.shape[0]
    Idim = np.eye(dim, dtype=complex)
    sig = [A * Idim + (1 / A) * e for e in es]            # 1/A = −i
    R["braid_from_kauffman"] = (np.allclose(sig[0] @ sig[1] @ sig[0], sig[1] @ sig[0] @ sig[1])
                                and np.allclose(sig[1] @ sig[2] @ sig[1], sig[2] @ sig[1] @ sig[2]))
    R["braid_entries_gaussian_int"] = all(_is_gaussian_int(s) for s in sig)

    # teeth: δ=3 로 같은 정수 블록 → e²=2e ≠ 3e → 관계 붕괴 (δ=2 고정성)
    R["teeth_delta_not_2_breaks"] = (not np.allclose(block @ block, 3 * block))

    ok = all(R.values())
    if not quick:
        print("Temperley-Lieb TL_n(δ=2) 정수 표현 관측 (Hecke H₃(q=i) 정수층 상보, witness — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  block=[[0,0,0,0],[0,1,−1,0],[0,−1,1,0],[0,0,0,0]] (singlet |01⟩−|10⟩, trace=δ=2) · "
              "e_i²=2e_i · e_i e_{i±1} e_i=e_i · e_1e_3=e_3e_1 (n=4, |1−3|=2) · 성분 ∈ ℤ", flush=True)
        print("  ★Hecke 상보: TL δ=−(q+q⁻¹)=2 ↔ q=−1 (정수 well-defined) vs Hecke H₃ q=i 는 q+q⁻¹=0 "
              "(Markov trace 정규화 특이). δ=2 → 순수 ℤ (Hecke q=i의 ℤ[i]와 대조).", flush=True)
        print("  Kauffman σ_i=A·I+A⁻¹·e_i (A=i, A²=−1) → braid σ_iσ_{i+1}σ_i=σ_{i+1}σ_iσ_{i+1} 유도 (ℤ[i] 성분).",
              flush=True)
        print("  ★관측: 신규 module 0 · root 불변 sidecar · 일반 δ Jones·TL_n(n>4)·knot 불변량=범위밖.", flush=True)
    print(f"temperley_lieb_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
