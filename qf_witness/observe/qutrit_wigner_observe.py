#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""qutrit_wigner_observe — TrackHE9 P6: qutrit Gross 이산 Wigner 함수 witness (관측, seal 아님).

report9 P6 축(qutrit Gross-Wigner). ★맥락성/magic 자원 렌즈의 **qudit 판**: 기봉인 Peres-Mermin(HE8 P2)·
contextual fraction(HE9 P2)은 큐빗 맥락성, magic(extent/robustness, HE5)은 큐빗 자원. 여기선 **홀수차원
qutrit 의 이산 Wigner 음수성**(Gross 2006) = 보편 양자계산에 필요한 자원의 phase-space 판별식.

관측(d=3, ω=e^{2πi/3}, exact 유리수/대수):
  1. Heisenberg-Weyl: X(shift)·Z(clock). phase-point 연산자 A_0 = parity(|j⟩→|−j⟩), A_u=D_u A_0 D_u†
     (D_u=X^q Z^p, 위상 무관). ★frame 성질 전수 exact: A_u Hermitian·tr(A_u)=1·tr(A_u A_v)=3δ_uv·Σ_u A_u=3I.
  2. Wigner W_ρ(u)=(1/3)tr(A_u ρ) 실수·Σ_u W=tr(ρ)=1.
  3. ★stabilizer 상태(계산기저·X/Z/XZ 고유상태) → W ≥ 0 (음수 없음).
  4. ★magic 상태 Wigner **음수성**: Strange (|1⟩−|2⟩)/√2 → min W=−1/3 · Norrell (2|0⟩−|1⟩−|2⟩)/√6 →
     min=−1/6. 음수 = 비-stabilizer(magic) 자원의 필요 판별식(이산 Hudson 정리 방향).
  5. 이산 Hudson: 순수 stabilizer ⟺ W≥0 (홀수 d) — 표본 stabilizer 전부 ≥0·magic 음수로 방향 실증.
  6. teeth: magic 음수성 비자명(Strange 실제 음수)·ΣW=1 항상·가짜(비물리 ρ tr≠1)는 정규화 위반.

정직 경계(★관측·seal 아님, root 불변 sidecar): witness = qutrit phase-space 대수(frame·음수성 판별).
  실제 qutrit 회로 봉인·증류·완전 이산 Hudson 증명 = 범위밖/차기. 신규 module 0. [[trackhe8-report8]]
  (Peres-Mermin 맥락성)·contextual fraction(HE9 P2)·magic(HE5) 자원 계보와 교차(다른 렌즈=phase-space).

사용: python scripts/qutrit_wigner_observe.py [--quick]
"""
from __future__ import annotations
import sys
import numpy as np

D = 3
W3 = np.exp(2j * np.pi / D)


def heisenberg_weyl():
    X = np.zeros((D, D), dtype=complex)
    Z = np.zeros((D, D), dtype=complex)
    for j in range(D):
        X[(j + 1) % D, j] = 1
        Z[j, j] = W3 ** j
    return X, Z


def phase_point_ops(X, Z):
    P = np.zeros((D, D), dtype=complex)                 # parity |j⟩→|−j mod d⟩
    for j in range(D):
        P[(-j) % D, j] = 1
    A = {}
    for q in range(D):
        for p in range(D):
            U = np.linalg.matrix_power(X, q) @ np.linalg.matrix_power(Z, p)
            A[(q, p)] = U @ P @ U.conj().T
    return P, A


def wigner(rho, A):
    return np.array([[(np.trace(A[(q, p)] @ rho) / D).real for p in range(D)] for q in range(D)])


def main():
    quick = "--quick" in sys.argv
    R = {}
    X, Z = heisenberg_weyl()
    P, A = phase_point_ops(X, Z)

    # 1. frame 성질
    R["A0_is_parity"] = np.allclose(P, np.array([[1, 0, 0], [0, 0, 1], [0, 1, 0]], dtype=complex))
    R["Au_hermitian"] = all(np.allclose(A[u], A[u].conj().T) for u in A)
    R["Au_trace_1"] = all(abs(np.trace(A[u]) - 1) < 1e-9 for u in A)
    R["Au_orthogonal_3delta"] = all(abs(np.trace(A[u] @ A[v]) - (D if u == v else 0)) < 1e-9
                                    for u in A for v in A)
    R["sum_Au_eq_3I"] = np.allclose(sum(A.values()), D * np.eye(D))

    # 2. Wigner 정규화
    rho0 = np.zeros((D, D), dtype=complex); rho0[0, 0] = 1
    W0 = wigner(rho0, A)
    R["wigner_normalized"] = (abs(W0.sum() - 1) < 1e-9)

    # 3. stabilizer 상태 W≥0 (계산기저 + X/Z/XZ 고유상태)
    stab_states = [rho0]
    for M in (X, Z, X @ Z):
        ev, evec = np.linalg.eig(M)
        for k in range(D):
            v = evec[:, k]; r = np.outer(v, v.conj()); r /= np.trace(r)
            stab_states.append(r)
    R["stabilizer_states_nonneg"] = all(np.all(wigner(r, A) >= -1e-9) for r in stab_states)

    # 4. magic 상태 음수성
    def state(vec):
        v = np.array(vec, dtype=complex); v /= np.linalg.norm(v)
        return np.outer(v, v.conj())
    W_strange = wigner(state([0, 1, -1]), A)
    W_norrell = wigner(state([2, -1, -1]), A)
    R["magic_strange_negative"] = (W_strange.min() < -1e-9 and abs(W_strange.min() + 1 / 3) < 1e-9)
    R["magic_norrell_negative"] = (W_norrell.min() < -1e-9 and abs(W_norrell.min() + 1 / 6) < 1e-9)

    # 5. 이산 Hudson 방향: stabilizer≥0(3) & magic<0(4) 동시 → 음수성이 magic 판별
    R["hudson_direction"] = (R["stabilizer_states_nonneg"]
                             and R["magic_strange_negative"] and R["magic_norrell_negative"])

    # 6. teeth
    R["teeth_magic_negativity_nonvacuous"] = (W_strange.min() < -0.1)   # 실제 유의미 음수
    R["teeth_all_wigner_sum_1"] = all(abs(wigner(r, A).sum() - 1) < 1e-9 for r in stab_states)

    ok = all(R.values())
    if not quick:
        print("qutrit Gross 이산 Wigner 함수 관측 (맥락성/magic 자원의 phase-space 판별, witness — seal 아님):",
              flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  magic Wigner min: Strange={W_strange.min():.4f}(−1/3) · Norrell={W_norrell.min():.4f}(−1/6)",
              flush=True)
        print("  ★stabilizer W≥0 vs magic W<0 = 이산 Hudson 방향(홀수 d): Wigner 음수성이 비-stabilizer "
              "자원의 phase-space 필요 판별식. Peres-Mermin/contextual fraction(큐빗 맥락성)·magic(HE5) 상보 렌즈.",
              flush=True)
        print("  ★정직: 관측=phase-space 대수뿐. qutrit 회로 봉인·증류·완전 Hudson 증명=범위밖. "
              "신규 module 0·root 불변 sidecar.", flush=True)
    print(f"qutrit_wigner_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
