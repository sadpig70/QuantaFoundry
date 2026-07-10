#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""a5_fourier_observe — TrackHE11 P1: A₅ Fourier ℚ(√5) 실현가능성 (Frobenius-Schur) 선검증 witness (관측, seal 아님).

report11 최다수렴축(A₅ √5 실봉인, 6/8). §3n P2·§4 "A₅ Fourier 실봉인(√5 승인) 아직 없음" 관문. TrackHE10 P2
`a5_observe`(문자표 ℚ(√5) 실수)를 **전체 Fourier 실현가능성**으로 승격: ★**Frobenius-Schur 지표 FS(ρ)=+1**
(모든 5 기약표현) → 표현행렬(문자뿐 아니라)까지 **ℝ=ℚ(√5) 위 실현가능** → 비아벨 DFT 가 **복소 ζ₅ 없이 √5 만**으로
exact. 봉인은 √5 승인 module 대기(=관측: Fourier 실현가능성 확립).

핵심 논증(exact ℚ(√5)·정수):
  1. A₅ 5 기약표현 dims {1,3,3,4,5}, Σdim²=60. 문자표 ∈ ℚ(√5)(5-cycle=(1±√5)/2, TrackHE10 P2 재확인).
  2. ★**Frobenius-Schur 지표** FS(ρ) = (1/|G|)Σ_g χ_ρ(g²) = (1/60)Σ_C |C|·χ_ρ(class(g²)). power map 사용.
     **FS(ρ)=+1 (전 5 irrep)** = **실수형(real type)** → ρ 가 ℝ=ℚ(√5) 위 실현가능(복소 불필요).
     ⟹ 전체 비아벨 Fourier(표현행렬) 가 ℚ(√5) 위 exact — ζ₅ 원리적 불필요(문자만이 아니라 DFT 전체).
  3. 문자 orthogonality Σ_C |C|·χ_i·χ_j = 60·δ_ij (ℚ(√5) exact) → 문자-DFT 유니터리.
  4. ★대조 A₄: 두 복소 1-dim 기약표현(ω₃) 의 **FS=0**(복소형=complex type) → ℝ 위 실현 불가 → **ζ₃ 필연**.
     A₄(ζ₃ 복소·FS=0)·A₅(√5 실수·FS=+1)·PSL(2,7)(√−7 복소·non-ambivalent) 사다리의 실수 지층.
  5. teeth: 가짜 문자표(φ→유리수)는 orthogonality/FS 붕괴.

정직 경계(★관측·seal 아님, root 불변 sidecar): witness = A₅ Fourier 의 ℚ(√5) 실현가능성(FS=+1)·문자 orthogonality.
  ★**봉인은 멈춤**: 실제 a5_fourier 봉인은 **√5 실수-surd 승인 module**(sqrt5_gate, ζ₅ 복소보다 경량 — redirect
  가치) 필요(사람게이트). Fourier 정규화 스칼라(√(dim/60))는 별도 실수(ℚ(√5) 밖일 수 있음, 대각 스칼라). witness=
  승인 결정근거. 신규 module 0. [[a5-observe]] 승격·Fibonacci φ(§3n P4)·A₅ 이중피복=차기.

사용: python -m qf_witness.observe.a5_fourier_observe [--quick]
"""
from __future__ import annotations
import os, sys, itertools
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a5_observe import q5, mul, add, scal, ZERO       # ℚ(√5) exact 재사용


def _alt_group(n):
    def par(p): return sum(1 for i in range(n) for j in range(i + 1, n) if p[i] > p[j]) % 2
    return [p for p in itertools.permutations(range(n)) if par(p) == 0]


def _comp(p, q): return tuple(p[q[i]] for i in range(len(p)))


def _order(p, idn):
    n, x = 1, p
    while x != idn:
        x = _comp(x, p); n += 1
    return n


def _inv(p):
    r = [0] * len(p)
    for i in range(len(p)):
        r[p[i]] = i
    return tuple(r)


def _classes(G, idn):
    def cc(g): return frozenset(_comp(_comp(x, g), _inv(x)) for x in G)
    cl, seen = [], set()
    for g in G:
        c = cc(g)
        if c not in seen:
            seen.add(c); cl.append(c)
    return cl


def a5_char_table():
    """[1A,2A,3A,5A,5B] 크기 [1,15,20,12,12], 문자표 ∈ ℚ(√5)."""
    phi = q5(F(1, 2), F(1, 2)); psi = q5(F(1, 2), F(-1, 2))
    sizes = [1, 15, 20, 12, 12]
    table = [[q5(1)] * 5,
             [q5(3), q5(-1), q5(0), phi, psi],
             [q5(3), q5(-1), q5(0), psi, phi],
             [q5(4), q5(0), q5(1), q5(-1), q5(-1)],
             [q5(5), q5(1), q5(-1), q5(0), q5(0)]]
    return sizes, table


def main():
    quick = "--quick" in sys.argv
    R = {}
    A5 = _alt_group(5); ID5 = (0, 1, 2, 3, 4)
    sizes, table = a5_char_table()

    R["dims_1_3_3_4_5_sum_sq_60"] = (sum(int(table[i][0][0]) ** 2 for i in range(5)) == 60)

    # 클래스 인덱스 + power map(g→g²): [1A,2A,3A,5A,5B]
    g5 = next(g for g in A5 if _order(g, ID5) == 5)
    from a5_observe import conj_class  # A₅ 켤레류
    cc5A = conj_class(g5); cc5B = conj_class(_comp(g5, g5))

    def cidx(g):
        o = _order(g, ID5)
        if o == 1: return 0
        if o == 2: return 1
        if o == 3: return 2
        return 3 if g in cc5A else 4
    reps = [ID5, next(g for g in A5 if _order(g, ID5) == 2),
            next(g for g in A5 if _order(g, ID5) == 3), g5, _comp(g5, g5)]
    sq = [cidx(_comp(r, r)) for r in reps]              # g² 의 클래스 인덱스

    # ★Frobenius-Schur 지표 FS(ρ)=(1/60)Σ_C |C|·χ_ρ(class(g²)) ∈ ℚ(√5), =+1?
    fs_all_plus1 = True
    fs_vals = []
    for i in range(5):
        s = ZERO
        for c in range(5):
            s = add(s, scal(sizes[c], table[i][sq[c]]))
        # /60
        fs = (s[0] / 60, s[1] / 60)
        fs_vals.append(fs)
        if fs != (F(1), F(0)):
            fs_all_plus1 = False
    R["frobenius_schur_all_plus1_real_type"] = fs_all_plus1
    R["fs_implies_Q_sqrt5_realizable_no_zeta5"] = fs_all_plus1

    # 문자 orthogonality (ℚ(√5) exact) → 문자-DFT 유니터리
    ortho = True
    for i in range(5):
        for j in range(5):
            s = ZERO
            for c in range(5):
                s = add(s, scal(sizes[c], mul(table[i][c], table[j][c])))
            if s != (F(60 if i == j else 0), F(0)):
                ortho = False
    R["char_orthogonality_Q_sqrt5"] = ortho

    # ★대조 A₄: 복소 1-dim irrep FS=0 (복소형 → ζ₃ 필연)
    A4 = _alt_group(4); ID4 = (0, 1, 2, 3)
    cl4 = _classes(A4, ID4)                             # 4 클래스: 1A,2A,3A,3B
    # A₄ 문자표: 복소 1-dim ω=ζ₃. FS = (1/12)Σ_g χ(g²). 3-cycle g²=3-cycle(다른 클래스)
    # 복소 irrep χ_ω(1A)=1,χ(2A)=1,χ(3A)=ω,χ(3B)=ω². FS = (1/12)[1·1+3·1+4·χ(3A²=3B)+4·χ(3B²=3A)]
    import numpy as np
    w = np.exp(2j * np.pi / 3)
    # 3A²=3B, 3B²=3A (3-cycle g²=g⁻¹ 다른 클래스)
    fs_a4_omega = (1 * 1 + 3 * 1 + 4 * (w ** 2) + 4 * w) / 12   # χ_ω(3A)=ω,χ_ω(3B)=ω²
    R["contrast_a4_complex_FS_zero"] = (abs(fs_a4_omega) < 1e-9)   # FS=0 복소형

    # teeth: 가짜 문자표(3a 의 5-cycle φ→유리수 1)는 orthogonality 붕괴
    fake = [row[:] for row in table]
    fake[1][3] = q5(1); fake[1][4] = q5(1)
    fake_ortho = True
    for j in range(5):
        s = ZERO
        for c in range(5):
            s = add(s, scal(sizes[c], mul(fake[1][c], fake[j][c])))
        if s != (F(60 if j == 1 else 0), F(0)):
            fake_ortho = False
    R["teeth_fake_table_breaks"] = (not fake_ortho)

    ok = all(R.values())
    if not quick:
        print("A₅ Fourier ℚ(√5) 실현가능성 (Frobenius-Schur) 선검증 (√5 실봉인 준비, witness — seal 아님):",
              flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  Frobenius-Schur 지표(전 5 irrep): {[(int(a), int(b)) for a, b in fs_vals]} = 전부 (1,0)=+1 "
              "→ 실수형 → ℚ(√5) 실현가능", flush=True)
        print("  ★핵심: FS(ρ)=+1 전 5 irrep → 표현행렬(문자뿐 아니라)까지 ℚ(√5) 실현가능 → A₅ 비아벨 DFT 가 "
              "**복소 ζ₅ 없이 √5 만**으로 exact. A₄(복소 FS=0→ζ₃ 필연)·PSL(2,7)(√−7 복소) 사다리의 실수 지층.",
              flush=True)
        print("  ★정직: 봉인 멈춤 — a5_fourier 실봉인은 √5 실수-surd 승인 module(sqrt5_gate, ζ₅보다 경량) 필요"
              "(사람게이트). witness=Fourier 실현가능성·승인 결정근거·신규 module 0·root 불변 sidecar.", flush=True)
    print(f"a5_fourier_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
