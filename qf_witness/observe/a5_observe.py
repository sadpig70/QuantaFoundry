#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""a5_observe — TrackHE10 P2: 교대군 A₅ 문자표 ★ζ₅-vs-√5 redirect 선검증 witness (관측, seal 아님).

report10 ★redirect showcase(A₅, 5/8). §3m P4·§4 "A₅/PSL(2,7) 아직 없음" 관문. ★**report10 긴장 해소**:
agent08 "A₅ 문자 전부 실수→√5 충분, ζ₅ 불필요(redirect)" vs agent04/05/06 "ζ₅ 필연" — **선검증으로 판정**.

핵심 논증(정수·ℚ(√5) exact):
  1. A₅ = 5점 우치환 60원소, 켤레류 5개(크기 1/15/20/12/12). ★**5-cycle 이 2 클래스로 분열**(order-5, 12+12)
     → NOT rational group(√5 등장, 정수 문자표 아님). A₄(ζ₃)·B₃(ζ-free) 계보 다음.
  2. ★**ambivalent**: 모든 g 가 g⁻¹ 와 켤레(A₅ 전 원소) → **모든 기약문자값이 실수**(Frobenius-Schur, 복소 없음).
  3. 문자표 ∈ ℚ(√5)(실수): dims 1·3·3·4·5, 5-cycle 값 = (1±√5)/2 = φ,ψ (황금비 켤레). orthogonality
     Σ_C |C|·χ_i(C)·χ_j(C) = 60·δ_ij (실수라 켤레 불요) + |G|=Σχ(1)²=60, 전부 exact ℚ(√5).
  4. ★**redirect verdict**: A₅ Fourier 는 **√5 실수 surd 로 충분·복소 ζ₅ 불필요**(ambivalent→실수형 표현,
     3-dim irrep = ℚ(√5) 위 정이십면체 회전). 요청서/agent04/05/06 의 "ζ₅ 필연"은 **과대 게이트**(redirect).
     대조: A₄ 는 **NOT ambivalent**(3-cycle g≁g⁻¹) → ζ₃ 복소 필연 — √5 실수 vs ζ₃/ζ₅ 복소를 ambivalent 가 판별.
  5. teeth: A₄ ambivalent=False(복소 필연 대조)·가짜 정수 문자표(φ→유리수)는 orthogonality 붕괴.

정직 경계(★선검증·seal 아님, root 불변 sidecar): witness = A₅ 표현론(√5 실수·ambivalent·NOT rational).
  ★**봉인은 멈춤**: A₅ Fourier(DFT over A₅)는 **√5 실수-surd 승인 module**(ζ₅ 복소보다 **경량** — redirect 의
  핵심 가치)이 필요(사람게이트). witness=승인 결정근거. a5_qft 봉인·PSL(2,7) ζ₇=승인 후/범위밖. 신규 module 0.

사용: python -m qf_witness.observe.a5_observe [--quick]
"""
from __future__ import annotations
import sys, itertools
from fractions import Fraction as F


# ── ℚ(√5) exact: 수 = (a, b) 는 a + b√5 (a,b ∈ ℚ) ──
def q5(a, b=0):
    return (F(a), F(b))


def mul(x, y):
    a, b = x; c, d = y
    return (a * c + 5 * b * d, a * d + b * c)          # (a+b√5)(c+d√5)=ac+5bd + (ad+bc)√5


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def scal(k, x):
    return (F(k) * x[0], F(k) * x[1])


ZERO = q5(0)


def parity(p):
    return sum(1 for i in range(5) for j in range(i + 1, 5) if p[i] > p[j]) % 2


A5 = [p for p in itertools.permutations(range(5)) if parity(p) == 0]
ID = (0, 1, 2, 3, 4)


def comp(p, q):
    return tuple(p[q[i]] for i in range(5))


def inv(p):
    r = [0] * 5
    for i in range(5):
        r[p[i]] = i
    return tuple(r)


def order(p):
    n, x = 1, p
    while x != ID:
        x = comp(x, p); n += 1
    return n


def conj_class(g):
    return frozenset(comp(comp(x, g), inv(x)) for x in A5)


def is_ambivalent(elems, comp_f, inv_f, cc_f):
    return all(inv_f(g) in cc_f(g) for g in elems)


def a4_ambivalent():
    """대조: A₄ 는 NOT ambivalent (3-cycle g≁g⁻¹) → ζ₃ 복소 필연."""
    A4 = [p for p in itertools.permutations(range(4)) if
          sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j]) % 2 == 0]
    id4 = (0, 1, 2, 3)

    def c(p, q): return tuple(p[q[i]] for i in range(4))

    def iv(p):
        r = [0] * 4
        for i in range(4): r[p[i]] = i
        return tuple(r)

    def cc(g): return frozenset(c(c(x, g), iv(x)) for x in A4)
    return all(iv(g) in cc(g) for g in A4)


def main():
    quick = "--quick" in sys.argv
    R = {}

    # 1. 군 구조
    R["a5_order_60"] = (len(A5) == 60)
    classes = []
    seen = set()
    for g in A5:
        cc = conj_class(g)
        if cc not in seen:
            seen.add(cc); classes.append(cc)
    R["a5_five_classes_1_15_20_12_12"] = (sorted(len(c) for c in classes) == [1, 12, 12, 15, 20])

    # 2. ambivalent → 문자 전부 실수
    R["a5_ambivalent_all_real"] = is_ambivalent(A5, comp, inv, conj_class)

    # 3. NOT rational group: 5-cycle 두 클래스 분열
    five = [c for c in classes if len(c) == 12]
    g5 = next(g for g in A5 if order(g) == 5)
    R["a5_5cycle_splits_not_rational"] = (len(five) == 2 and comp(g5, g5) not in conj_class(g5))

    # 4. 문자표 ∈ ℚ(√5) orthogonality. 클래스 순서 [1A,2A,3A,5A,5B] 크기 [1,15,20,12,12]
    sizes = [1, 15, 20, 12, 12]
    phi = q5(F(1, 2), F(1, 2))                          # (1+√5)/2
    psi = q5(F(1, 2), F(-1, 2))                         # (1-√5)/2
    table = [
        [q5(1), q5(1), q5(1), q5(1), q5(1)],            # trivial
        [q5(3), q5(-1), q5(0), phi, psi],               # 3a
        [q5(3), q5(-1), q5(0), psi, phi],               # 3b
        [q5(4), q5(0), q5(1), q5(-1), q5(-1)],          # 4
        [q5(5), q5(1), q5(-1), q5(0), q5(0)],           # 5
    ]

    def row_inner(i, j):
        s = ZERO
        for k in range(5):
            s = add(s, scal(sizes[k], mul(table[i][k], table[j][k])))
        return s
    ortho = all(row_inner(i, j) == (F(60 if i == j else 0), F(0))
                for i in range(5) for j in range(5))
    R["char_table_orthogonal_Q_sqrt5"] = ortho
    R["sum_dims_squared_60"] = (sum(int(table[i][0][0]) ** 2 for i in range(5)) == 60)
    # 문자값 전부 실수 ℚ(√5)(복소 성분 없음 — 구성상 √5 실수만)·5-cycle 에 √5 등장
    R["five_cycle_has_sqrt5"] = (table[1][3][1] != 0 and table[2][3][1] != 0)   # b≠0 → √5 성분

    # 5. ★redirect verdict: √5 실수 충분·ζ₅ 불필요 (A₅ ambivalent) vs A₄ ζ₃ 복소 (NOT ambivalent)
    R["redirect_sqrt5_suffices_no_zeta5"] = (R["a5_ambivalent_all_real"] and R["char_table_orthogonal_Q_sqrt5"])
    R["contrast_a4_not_ambivalent_needs_zeta3"] = (a4_ambivalent() is False)

    # teeth: 가짜 정수 문자표(φ→1, ψ→0)는 orthogonality 붕괴
    fake = [row[:] for row in table]
    fake[1][3] = q5(1); fake[1][4] = q5(0)
    fake_ortho = True
    for j in range(5):
        s = ZERO
        for k in range(5):
            s = add(s, scal(sizes[k], mul(fake[1][k], fake[j][k])))
        if s != (F(60 if j == 1 else 0), F(0)):
            fake_ortho = False
    R["teeth_fake_integer_table_breaks"] = (not fake_ortho)

    ok = all(R.values())
    if not quick:
        print("교대군 A₅ 문자표 ★ζ₅-vs-√5 redirect 선검증 (★report10 긴장 해소, witness — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  문자표(ℚ(√5) 실수·5-cycle=(1±√5)/2): dims 1·3·3·4·5 · orthogonality Σ|C|χχ=60δ · |G|=Σχ(1)²=60",
              flush=True)
        print("  ★redirect verdict: A₅ ambivalent(모든 g~g⁻¹)→문자 전부 실수 → **√5 실수 surd 충분·복소 ζ₅ "
              "불필요**. 요청서/agent04·05·06 'ζ₅ 필연'=과대 게이트. 대조: A₄ NOT ambivalent→ζ₃ 복소 필연.", flush=True)
        print("  ★정직: 봉인 멈춤 — A₅ Fourier 는 √5 실수-surd 승인 module(ζ₅보다 경량) 필요(사람게이트). "
              "witness=승인 결정근거·신규 module 0·root 불변 sidecar.", flush=True)
    print(f"a5_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
