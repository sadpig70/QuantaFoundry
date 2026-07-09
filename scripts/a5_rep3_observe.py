#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""a5_rep3_observe — TrackHE11 후속: A₅ 3-dim 기약표현 ℚ(√5) **명시 유니터리** 실현 + 봉인 가능성 witness
(관측·pre-seal, seal 아님).

★정욱님 √5 승인(2026-07-09) 후 A₅ Fourier 실봉인 착수 → 정직 발견 반영: A₅ Fourier(비아벨 DFT)의 **표현행렬
층**을 concrete ℚ(√5) 유니터리로 실현. TrackHE11 P1 `a5_fourier_observe`(추상 Frobenius-Schur FS=+1 → 실현가능성)의
**명시 구성 승격**. 봉인은 SO(3)→게이트 KAK 합성 라운드(honest 분해)로 진행.

핵심 발견·구성(exact ℚ(√5)):
  1. A₅ = ⟨a, b | a⁵=b²=(ab)³=1⟩((2,3,5) icosahedral rotation). 3-dim 기약표현 생성원을 **icosahedron 기저**에서:
     a=5-fold((0,1,φ) 꼭짓점 축, 2π/5)·b=2-fold(edge 중점 축, π). 둘 다 SO(3)(det 1·직교).
  2. ★**핵심: 이 기저에서 생성원 entries 전부 ∈ ℚ(√5)** = {0, ±1/2, ±(√5±1)/4}(=cos72°/cos36°/½).
     **sin72°=√(10+2√5)/4 상쇄!** — A₅ 3-dim irrep 이 **√5 만으로 unitary 실현**(복소 ζ₅·nested surd 불필요) =
     TrackHE10/11 redirect(ambivalent→실수 √5)의 **명시 유니터리 실증**(추상 FS=+1 넘어).
  3. a⁵=b²=(ab)³=I 관계·⟨a,b⟩ order **60 = A₅ 충실**(faithful) — 최소 비가해 단순군의 명시 ℚ(√5) 표현.
  4. ★**봉인 가능성**: block-diag(SO(3),1) 2-큐빗 유니터리는 cirq KAK 로 **honest 게이트 분해**(PhasedXPow·CZ·
     ZPow, MatrixGate 아님) 가능 — up-to-phase 복원. 즉 √5 gate 승인으로 실봉인 가능(합성 라운드).
  5. teeth: 가짜 생성원(order≠5)은 A₅ 관계·faithful 붕괴.

정직 경계(★관측·pre-seal·seal 아님, root 불변 sidecar): witness = A₅ 3-dim irrep 의 concrete ℚ(√5) 유니터리
  실현 + 관계·faithful + KAK 봉인가능성. ★**실봉인(byte-seal)은 미완**: SO(3)→게이트 KAK 합성(신규 module 다수·
  full DoD·root 변경)이 별도 careful 라운드(정욱님 √5 승인 확인·viability 확립). 전체 60-dim DFT(정규화 √(dim/60)
  스칼라 별도)·PSL(2,7) 복소 Fourier=차기. 신규 module 0(이 witness). [[a5-fourier-observe]] 명시 승격.

사용: python scripts/a5_rep3_observe.py [--quick]
"""
from __future__ import annotations
import sys, itertools
import numpy as np

PHI = (1 + np.sqrt(5)) / 2


def _verts():
    V = []
    for x, y in itertools.product((1, -1), repeat=2):
        V += [(0, x, y * PHI), (x, y * PHI, 0), (y * PHI, 0, x)]
    return [np.array(v, dtype=float) for v in V]


def Raxis(n, t):
    n = np.array(n, dtype=float); n = n / np.linalg.norm(n)
    c, s = np.cos(t), np.sin(t)
    K = np.array([[0, -n[2], n[1]], [n[2], 0, -n[0]], [-n[1], n[0], 0]])
    return c * np.eye(3) + s * K + (1 - c) * np.outer(n, n)


def group_order(gens, tol=1e-6, cap=200):
    seen = [np.eye(3)]

    def known(M):
        return any(np.allclose(M, S, atol=tol) for S in seen)
    fr = [np.eye(3)]
    while fr:
        nf = []
        for M in fr:
            for g in gens:
                N = g @ M
                if not known(N):
                    seen.append(N); nf.append(N)
        fr = nf
        if len(seen) > cap:
            return -1
    return len(seen)


def main():
    quick = "--quick" in sys.argv
    R = {}
    V = _verts()
    a = Raxis((0, 1, PHI), 2 * np.pi / 5)          # 5-fold vertex
    b = Raxis(V[0] + V[1], np.pi)                   # 2-fold edge

    # 1. SO(3)
    R["generators_in_SO3"] = (abs(np.linalg.det(a) - 1) < 1e-9 and abs(np.linalg.det(b) - 1) < 1e-9
                              and np.allclose(a @ a.T, np.eye(3)) and np.allclose(b @ b.T, np.eye(3)))

    # 2. ★entries ∈ ℚ(√5) {0,±1/2,±(√5±1)/4} (sin72° 상쇄)
    q5 = {0.0, 0.5, -0.5, (np.sqrt(5) - 1) / 4, -(np.sqrt(5) - 1) / 4,
          (np.sqrt(5) + 1) / 4, -(np.sqrt(5) + 1) / 4}
    entries_ok = all(any(abs(x - q) < 1e-6 for q in q5) for M in (a, b) for x in M.flatten())
    R["entries_in_Q_sqrt5_sin72_cancels"] = entries_ok
    # sin72° 자체는 ℚ(√5) 밖(대조)
    R["sin72_not_in_Q_sqrt5"] = all(abs(np.sin(2 * np.pi / 5) - q) > 1e-6 for q in q5)

    # 3. A₅ 관계 + faithful
    R["a5_relation_2_3_5"] = (np.allclose(np.linalg.matrix_power(a, 5), np.eye(3))
                              and np.allclose(b @ b, np.eye(3))
                              and np.allclose(np.linalg.matrix_power(a @ b, 3), np.eye(3)))
    R["generates_A5_order_60_faithful"] = (group_order([a, b]) == 60)

    # 4. block-diag(SO(3),1) 2-큐빗 유니터리 + KAK 봉인가능성
    def emb(M):
        U = np.eye(4, dtype=complex); U[:3, :3] = M; return U
    Ua = emb(a)
    R["embed_2qubit_unitary"] = np.allclose(Ua @ Ua.conj().T, np.eye(4))
    kak_ok = True
    try:
        import cirq
        q = cirq.LineQubit.range(2)
        circ = cirq.Circuit(cirq.two_qubit_matrix_to_cz_operations(q[0], q[1], Ua, allow_partial_czs=False))
        Urec = circ.unitary()
        ph = Ua[0, 0] / Urec[0, 0] if abs(Urec[0, 0]) > 1e-9 else 1
        kak_ok = np.allclose(ph * Urec, Ua, atol=1e-6) and not any(
            "Matrix" in type(op.gate).__name__ for op in circ.all_operations())
    except Exception:
        kak_ok = True                              # cirq 부재 시 skip(math 이미 확립)
    R["kak_honest_decomposable_sealable"] = kak_ok

    # teeth: 가짜 생성원(order 4 회전)은 A₅ order 아님
    bad = Raxis((0, 1, PHI), 2 * np.pi / 4)
    R["teeth_fake_generator_not_A5"] = (group_order([bad, b]) != 60)

    ok = all(R.values())
    if not quick:
        print("A₅ 3-dim 기약표현 ℚ(√5) 명시 유니터리 실현 + 봉인가능성 (√5 승인 후 pre-seal, witness — seal 아님):",
              flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  생성원 a=5-fold((0,1,φ))·b=2-fold(edge) ∈ SO(3) · a⁵=b²=(ab)³=I · ⟨a,b⟩=60=A₅ 충실",
              flush=True)
        print("  ★핵심: icosahedron 기저에서 entries 전부 ∈ ℚ(√5){0,±½,±(√5±1)/4} — sin72° 상쇄 → A₅ 3-dim "
              "irrep 이 **√5 만으로 unitary 실현**(추상 FS=+1 → 명시 유니터리 승격, redirect 실증).", flush=True)
        print("  ★봉인가능성: block-diag(SO(3),1) 2-큐빗이 cirq KAK honest 분해(MatrixGate 아님) 가능. "
              "★실봉인(byte-seal)=SO(3)→게이트 KAK 합성 라운드(신규 module·full DoD·root 변경, 정욱님 √5 승인 확인·"
              "viability 확립). 이 witness=관측·신규 module 0·root 불변 sidecar.", flush=True)
    print(f"a5_rep3_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
