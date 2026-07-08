#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""peres_mermin_observe — TrackHE8 P5: Peres-Mermin 사각형 state-independent 맥락성 증명서 (관측, seal 아님).

report8 수렴축(맥락성 2/8). §3j·§4 "맥락성 증명서 아직 없음" 관문 개창 — magic 자원(extent/robustness,
기봉인)과 다른 **자원 렌즈**(관측가능량 대수의 모순 구조). ★TrackHE8 마지막 축(완주 시 트랙 폐합).

Peres-Mermin 3×3 magic square (2큐빗 Pauli 관측가능량):
    X⊗I   I⊗X   X⊗X          각 row 곱 = +I (3개)
    I⊗Z   Z⊗I   Z⊗Z          col0·col1 곱 = +I · col2 곱 = **−I**
    X⊗Z   Z⊗X   Y⊗Y
관측(오라클 독립, 정수 Pauli 대수 exact):
  1. 9 관측가능량 전부 Hermitian·involutory(A²=I)·고유값 ±1 (유효 관측가능량).
  2. 각 row/col 내 3개 pairwise commute (동시 고유기저 = context 존재 필요조건).
  3. row 곱 = +I ×3 · col 곱 = +I,+I,**−I**.
  4. ★모순(state-independent contextuality): noncontextual ±1 값배정 v 가정 시 전 9개 곱을
     row 경로 Π(row곱)=(+1)³=+1 vs col 경로 Π(col곱)=(+1)(+1)(−1)=−1 → **parity 모순** → 배정 불가.
     KS 정리의 최소 state-independent 실증(어떤 양자상태에도 무관).

정직 경계(seal 아님, root 불변 sidecar): 관측 = Peres-Mermin 대수적 모순(exact Pauli 대수 정수 witness).
  ★증명서(certificate) — 회로 유니터리 아님(봉인 아님). contextual fraction·LP 정량화 = 차기/범위밖.
  신규 module 0. magic 자원(ξ/R)·채널 magic 과 다른 축(맥락성 렌즈).

사용: python scripts/peres_mermin_observe.py [--quick]
"""
from __future__ import annotations
import sys
import numpy as np

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def kron(a, b):
    return np.kron(a, b)


# Peres-Mermin 사각형 (2큐빗)
SQ = [
    [kron(X, I2), kron(I2, X), kron(X, X)],
    [kron(I2, Z), kron(Z, I2), kron(Z, Z)],
    [kron(X, Z), kron(Z, X), kron(Y, Y)],
]
LABEL = [["X⊗I", "I⊗X", "X⊗X"], ["I⊗Z", "Z⊗I", "Z⊗Z"], ["X⊗Z", "Z⊗X", "Y⊗Y"]]
Id = np.eye(4, dtype=complex)


def prod(mats):
    r = np.eye(4, dtype=complex)
    for m in mats:
        r = r @ m
    return r


def is_pm(M):                       # +I 또는 −I 판정 → +1/−1, 아니면 0
    if np.allclose(M, Id):
        return 1
    if np.allclose(M, -Id):
        return -1
    return 0


def main():
    quick = "--quick" in sys.argv
    R = {}

    # 1. 유효 관측가능량: Hermitian·involutory·고유값 ±1
    def valid(A):
        return (np.allclose(A, A.conj().T) and np.allclose(A @ A, Id)
                and np.allclose(sorted(np.linalg.eigvalsh(A).round(6)), [-1, -1, 1, 1]))
    R["observables_valid"] = all(valid(SQ[i][j]) for i in range(3) for j in range(3))

    # 2. row/col 내 pairwise commute
    def commute(A, B):
        return np.allclose(A @ B, B @ A)
    row_comm = all(commute(SQ[i][a], SQ[i][b]) for i in range(3) for a in range(3) for b in range(a + 1, 3))
    col_comm = all(commute(SQ[a][j], SQ[b][j]) for j in range(3) for a in range(3) for b in range(a + 1, 3))
    R["lines_commute"] = row_comm and col_comm

    # 3. row 곱 = +I ×3 · col 곱 = +I,+I,−I
    rowp = [is_pm(prod(SQ[i])) for i in range(3)]
    colp = [is_pm(prod([SQ[i][j] for i in range(3)])) for j in range(3)]
    R["row_products_plus"] = (rowp == [1, 1, 1])
    R["col_products_plus_plus_minus"] = (colp == [1, 1, -1])

    # 4. ★parity 모순: Π(row곱)=+1 vs Π(col곱)=−1 → noncontextual 값배정 불가
    prow = int(np.prod(rowp))
    pcol = int(np.prod(colp))
    R["parity_contradiction"] = (prow == 1 and pcol == -1)

    # teeth: 오염(Y⊗Y → X⊗X)하면 col2 곱이 −I 가 아니게 되어 모순 소멸
    SQ2 = [row[:] for row in SQ]
    SQ2[2][2] = kron(X, X)
    colp2 = [is_pm(prod([SQ2[i][j] for i in range(3)])) for j in range(3)]
    R["teeth_corruption_breaks"] = (colp2 != [1, 1, -1] or int(np.prod(colp2)) == 1)

    ok = all(R.values())
    if not quick:
        print("Peres-Mermin 사각형 state-independent 맥락성 증명서 (§3j 맥락성 개창, witness — seal 아님):",
              flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  row 곱 = {rowp} (전부 +1) · col 곱 = {colp} (+1,+1,−1) → Π_row={prow} vs Π_col={pcol} 모순",
              flush=True)
        print("  ★정직: 관측=Peres-Mermin 대수적 모순(exact Pauli 정수 witness)·certificate(회로 유니터리 "
              "아님=봉인 아님)·contextual fraction 정량화=차기. 신규 module 0·root 불변 sidecar.", flush=True)
    print(f"peres_mermin_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
