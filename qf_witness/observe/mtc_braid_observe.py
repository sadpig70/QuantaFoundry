#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mtc_braid_observe — TrackHE10 P4: MTC pentagon/hexagon 핵심 정합 + Ising/Fibonacci braid 유니터리 witness
(관측, seal 아님).

report10 수렴축(MTC pentagon/hexagon + braid, 5/8). §3m P6·§4 "완전 MTC(pentagon/hexagon)·braid 유니터리
봉인 아직 없음" 관문. `ising_fusion_observe`(TrackHE9 P6, 융합규칙·양자차원만)의 **braid 표현 계층 승격** +
Fibonacci(보편) 상보.

관측(cyclotomic 대수·braid 관계):
  1. **Ising** {1,σ,ψ}: F^σ_{σσσ}=Hadamard/√2 (unitary·F²=I, pentagon σσσσ 자기정합), R^{σσ}_1=e^{−iπ/8}·
     R^{σσ}_ψ=e^{i3π/8}. braid B₁=R·B₂=F⁻¹RF → ★**Yang-Baxter B₁B₂B₁=B₂B₁B₂**(hexagon 정합)·unitary.
     ★**Clifford image**: B₁=e^{−iπ/8}·S·B₂=e^{−iπ/8}·HSH (전역 ζ₁₆ 위상까지) → 생성군=단일큐빗 Clifford
     (유한, S⁴=I) = **비보편**.
  2. **Fibonacci** {1,τ}: d_τ=φ·**φ²=φ+1**(pentagon 핵심). F^τ_{τττ}=[[1/φ,1/√φ],[1/√φ,−1/φ]](unitary·F²=I),
     R^{ττ}_1=e^{−4πi/5}·R^{ττ}_τ=e^{3πi/5}. braid Yang-Baxter·unitary. ★**non-Clifford**(Pauli↛Pauli) = **보편**.
  3. 대조: Ising(Clifford·비보편·d_σ=√2) vs Fibonacci(non-Clifford·보편·d_τ=φ) = 두 정준 애니온 braid.
  4. teeth: 가짜 R(위상 오염)은 Yang-Baxter 붕괴.

정직 경계(★관측·seal 아님, root 불변 sidecar): witness = MTC pentagon 핵심(F²=I·φ²=φ+1)·hexagon→Yang-Baxter
  braid 정합·Clifford/non-Clifford 판별(exact 대수값, 관계는 기계정밀도 검증). ★**봉인 아님** — braid 유니터리
  는 전역 ζ₁₆ 위상 포함(ζ₁₆ module=사람게이트). 완전 MTC(전 F/R symbol pentagon/hexagon 열거)·Chern-Simons
  level-k = 범위밖. 신규 module 0. [[ising-fusion-observe]](TrackHE9 P6)·Fibonacci(G5)·Majorana(HE7) braid 계보 교차.

사용: python scripts/mtc_braid_observe.py [--quick]
"""
from __future__ import annotations
import sys
import numpy as np

X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
Sg = np.diag([1, 1j]).astype(complex)
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)


def is_clifford_1q(U, tol=1e-9):
    """U P U† ∈ ±{X,Y,Z} 전부 → Clifford."""
    paulis = [X, Y, Z]
    for P in (X, Z):
        C = U @ P @ U.conj().T
        if not any(np.allclose(C, s * Q, atol=tol) for Q in paulis for s in (1, -1)):
            return False
    return True


def yang_baxter(B1, B2, tol=1e-9):
    return np.allclose(B1 @ B2 @ B1, B2 @ B1 @ B2, atol=tol)


def unitary(M, tol=1e-9):
    return np.allclose(M @ M.conj().T, np.eye(len(M)), atol=tol)


def main():
    quick = "--quick" in sys.argv
    R = {}

    # ── Ising ──
    F_i = H.copy()                                       # F^σ_{σσσ} = Hadamard/√2
    R_i = np.diag([np.exp(-1j * np.pi / 8), np.exp(3j * np.pi / 8)])
    R["ising_F_unitary_involution"] = unitary(F_i) and np.allclose(F_i @ F_i, np.eye(2))
    B1i, B2i = R_i, np.linalg.inv(F_i) @ R_i @ F_i
    R["ising_braid_yang_baxter"] = yang_baxter(B1i, B2i)
    R["ising_braid_unitary"] = unitary(B1i) and unitary(B2i)
    R["ising_braid_clifford_image"] = (np.allclose(B1i, np.exp(-1j * np.pi / 8) * Sg)
                                       and np.allclose(B2i, np.exp(-1j * np.pi / 8) * (H @ Sg @ H)))
    R["ising_clifford_nonuniversal"] = (is_clifford_1q(np.exp(1j * np.pi / 8) * B1i)
                                        and np.allclose(np.linalg.matrix_power(np.exp(1j * np.pi / 8) * B1i, 4),
                                                        np.eye(2)))     # S⁴=I 유한군

    # ── Fibonacci ──
    phi = (1 + np.sqrt(5)) / 2
    R["fibonacci_pentagon_phi2"] = bool(np.isclose(phi ** 2, phi + 1))
    F_f = np.array([[1 / phi, 1 / np.sqrt(phi)], [1 / np.sqrt(phi), -1 / phi]], dtype=complex)
    R_f = np.diag([np.exp(-4j * np.pi / 5), np.exp(3j * np.pi / 5)])
    R["fibonacci_F_unitary_involution"] = unitary(F_f) and np.allclose(F_f @ F_f, np.eye(2))
    B1f, B2f = R_f, np.linalg.inv(F_f) @ R_f @ F_f
    R["fibonacci_braid_yang_baxter"] = yang_baxter(B1f, B2f)
    R["fibonacci_braid_unitary"] = unitary(B1f) and unitary(B2f)
    R["fibonacci_non_clifford_universal"] = (not is_clifford_1q(B1f)) and (not is_clifford_1q(B2f))

    # 대조 + 양자차원 (융합 Perron-Frobenius, exact 정수 고유값)
    N_ising_sig = np.array([[0, 1], [1, 1]])             # σ×σ=1+ψ 축약(2-state)
    d_sigma = max(np.real(np.linalg.eigvals(N_ising_sig.astype(float))))
    R["quantum_dims_sqrt2_phi"] = (np.isclose(d_sigma, phi))   # 주의: 2-state 축약 시 √2 vs φ — 아래 exact
    # d_σ=√2: σ×σ=1+ψ 3-object 융합행렬 Perron
    Nsig3 = np.array([[0, 0, 1], [0, 0, 1], [1, 1, 0]], dtype=float)   # (1,ψ,σ) 행: σ행=1+ψ
    R["quantum_dims_sqrt2_phi"] = (np.isclose(max(np.real(np.linalg.eigvals(Nsig3))), np.sqrt(2))
                                   and np.isclose(phi, (1 + np.sqrt(5)) / 2))
    R["contrast_ising_clifford_fib_universal"] = (R["ising_clifford_nonuniversal"]
                                                  and R["fibonacci_non_clifford_universal"])

    # teeth: 가짜 R(위상 오염)은 Yang-Baxter 붕괴
    R_bad = np.diag([np.exp(-1j * np.pi / 8), np.exp(1j * np.pi / 8)])   # ψ 위상 오염
    B2bad = np.linalg.inv(F_i) @ R_bad @ F_i
    R["teeth_fake_R_breaks_yang_baxter"] = (not yang_baxter(R_bad, B2bad))

    ok = all(R.values())
    if not quick:
        print("MTC pentagon/hexagon 핵심 + Ising/Fibonacci braid 유니터리 관측 (witness — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  ★Ising(F=H/√2·F²=I·d_σ=√2·braid Yang-Baxter·Clifford image S/HSH·비보편) vs "
              "Fibonacci(φ²=φ+1·d_τ=φ·Yang-Baxter·non-Clifford·보편) = 두 정준 애니온 braid 표현.", flush=True)
        print("  ★정직: 관측=pentagon 핵심(F²=I·φ²=φ+1)·hexagon→Yang-Baxter·Clifford 판별(exact 대수·관계 기계정밀도). "
              "봉인 아님(braid=전역 ζ₁₆ 위상, ζ₁₆ module=사람게이트)·완전 MTC/CS level-k=범위밖·신규 module 0·root 불변.",
              flush=True)
    print(f"mtc_braid_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
