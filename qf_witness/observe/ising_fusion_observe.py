#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ising_fusion_observe — TrackHE9 P6: Ising 애니온 융합 범주 witness (관측, seal 아님).

report9 P6 축(Ising fusion). ★기봉인 애니온 계보(Fibonacci braid G5·Majorana braid HE7 P2·Jones/knot HE5)에
**두 번째 정준 애니온 모델** 추가 = Ising 융합 범주 {1, ψ, σ}. Fibonacci(보편, d_τ=φ)와 상보인 **비보편
Clifford-계열**(d_σ=√2) 모델 → 애니온 그림 완성.

관측(정수·대수 exact):
  1. 융합 규칙: σ×σ=1+ψ · σ×ψ=σ · ψ×ψ=1 (1=vac·ψ=fermion·σ=Ising 비아벨). N_ab^c 정수 계수.
  2. ★융합환 결합성: N_a·N_b = Σ_c N_ab^c N_c (융합 행렬 곱=Perron-Frobenius 정합) 전수 exact.
  3. ★양자차원 d_a = 융합행렬 N_a 의 Perron-Frobenius 고유값 → d_1=d_ψ=1·**d_σ=√2**. 정합
     d_a d_b=Σ_c N_ab^c d_c 전수. 총 양자차원 D²=Σd_a²=4.
  4. ★F-행렬(σσσσ 결합자)=Hadamard/√2 → F²=I(σ-채널 결합 자기정합). R-행렬 R^σσ_1=e^{−iπ/8}·
     R^σσ_ψ=e^{i3π/8} → 모노드로미 위상차 π/2 = **단일큐빗 Clifford**(비보편, S-게이트급). 위상 θ_σ=e^{iπ/8}.
  5. 대조: Fibonacci τ×τ=1+τ → d_τ=φ=(1+√5)/2 (보편) vs Ising d_σ=√2 (비보편) — 두 정준 모델.
  6. teeth: 가짜 융합(σ×σ=σ)은 양자차원 정합/결합성 위반.

정직 경계(★관측·seal 아님, root 불변 sidecar): witness = Ising 융합 범주 대수(융합·양자차원·F/R 정합).
  실제 braid 유니터리 회로 봉인·MTC 완전 (pentagon/hexagon 전체)·topological 계산 = 범위밖/차기.
  신규 module 0. [[trackhe5-report5]](Jones/knot)·Fibonacci(G5)·Majorana(HE7 P2) 애니온 계보와 교차.

사용: python scripts/ising_fusion_observe.py [--quick]
"""
from __future__ import annotations
import sys
import numpy as np

LAB = ["1", "ψ", "σ"]                                   # 0=vac, 1=fermion, 2=Ising


def fusion_N():
    N = np.zeros((3, 3, 3), dtype=int)

    def setf(a, b, cs):
        for c in cs:
            N[a][b][c] = 1; N[b][a][c] = 1
    setf(0, 0, [0]); setf(0, 1, [1]); setf(0, 2, [2])
    setf(1, 1, [0]); setf(1, 2, [2]); setf(2, 2, [0, 1])   # σ×σ=1+ψ
    return N


def perron_dim(Na):
    return max(np.real(np.linalg.eigvals(Na.astype(float))))


def main():
    quick = "--quick" in sys.argv
    R = {}
    N = fusion_N()

    # 1. 융합 규칙
    R["fusion_sigma_sigma_1_plus_psi"] = ([c for c in range(3) if N[2][2][c]] == [0, 1])
    R["fusion_sigma_psi_sigma"] = ([c for c in range(3) if N[2][1][c]] == [2])
    R["fusion_psi_psi_vac"] = ([c for c in range(3) if N[1][1][c]] == [0])

    # 2. 융합환 결합성: N_a N_b = Σ_c N_ab^c N_c
    Nmat = [N[a] for a in range(3)]
    assoc = True
    for a in range(3):
        for b in range(3):
            lhs = Nmat[a] @ Nmat[b]
            rhs = sum(N[a][b][c] * Nmat[c] for c in range(3))
            if not np.array_equal(lhs, rhs):
                assoc = False
    R["fusion_ring_associative"] = assoc

    # 3. 양자차원
    qd = [perron_dim(N[a]) for a in range(3)]
    R["quantum_dims_1_1_sqrt2"] = (abs(qd[0] - 1) < 1e-9 and abs(qd[1] - 1) < 1e-9
                                   and abs(qd[2] - np.sqrt(2)) < 1e-9)
    R["dim_consistency"] = all(abs(qd[a] * qd[b] - sum(N[a][b][c] * qd[c] for c in range(3))) < 1e-9
                               for a in range(3) for b in range(3))
    R["total_dim_D2_eq_4"] = (abs(sum(x * x for x in qd) - 4) < 1e-9)

    # 4. F/R
    F = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    R["F_sigma_hadamard_F2_eq_I"] = np.allclose(F @ F, np.eye(2))
    r1, rpsi = np.exp(-1j * np.pi / 8), np.exp(3j * np.pi / 8)
    R["R_monodromy_pi_over_2_clifford"] = (abs((np.angle(rpsi) - np.angle(r1)) - np.pi / 2) < 1e-9)
    # 리본 관계: θ_σ = 1/R^σσ_1 = e^{iπ/8}(h_σ=1/16) · R^σσ_ψ = θ_ψ^{1/2}/θ_σ, θ_ψ=e^{iπ}(h_ψ=1/2)
    theta_sigma = 1 / r1
    R["topological_spin_sigma_eiπ8"] = (abs(theta_sigma - np.exp(1j * np.pi / 8)) < 1e-9
                                        and abs(rpsi - np.exp(1j * np.pi / 2) / theta_sigma) < 1e-9)

    # 5. 대조 Fibonacci
    dtau = perron_dim(np.array([[0, 1], [1, 1]]))
    R["fibonacci_contrast_phi_universal"] = (abs(dtau - (1 + np.sqrt(5)) / 2) < 1e-9)

    # 6. duality: 모든 대상 a 에 dual ā (1∈a×ā). 진짜 Ising 은 전부 자기쌍대(1∈a×a).
    R["all_objects_self_dual"] = all(N[a][a][0] == 1 for a in range(3))
    # teeth: 가짜 융합 σ×σ=σ 는 1∉σ×σ → σ 의 dual 부재(duality 공리 위반)
    Nb = N.copy(); Nb[2] = N[2].copy(); Nb[2][2] = np.array([0, 0, 1])   # σ×σ=σ (거짓)
    sigma_has_dual = any(Nb[2][b][0] == 1 for b in range(3))
    R["teeth_fake_fusion_no_dual"] = (not sigma_has_dual)

    ok = all(R.values())
    if not quick:
        print("Ising 애니온 융합 범주 관측 (Fibonacci 상보=두 번째 정준 애니온 모델, witness — seal 아님):",
              flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  양자차원 d_1,d_ψ,d_σ = {[round(x,6) for x in qd]} (=1,1,√2) · D²={sum(x*x for x in qd):.4f}",
              flush=True)
        print("  ★Ising(σ×σ=1+ψ·d_σ=√2·비보편 Clifford, θ_σ=e^{iπ/8}) vs Fibonacci(τ×τ=1+τ·d_τ=φ·보편) "
              "= 두 정준 애니온 모델. 융합·양자차원·F/R 정합 전부 exact.", flush=True)
        print("  ★정직: 관측=융합 범주 대수뿐. braid 회로 봉인·MTC 전체(pentagon/hexagon)·위상계산=범위밖. "
              "신규 module 0·root 불변 sidecar.", flush=True)
    print(f"ising_fusion_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
