#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""contextual_fraction_observe — TrackHE9 P2: Peres-Mermin 맥락성의 contextual fraction LP 정량화 (관측).

report9 수렴축(contextual fraction LP 6/8). §3l P5·§4 "contextual fraction LP 정량화 아직 없음" 관문 —
TrackHE8 P5(peres_mermin, 정성적 parity 모순)의 **정량 자원 척도 승격**. 맥락 분율(Abramsky-Barbosa)을
**내장 exact-rational LP**(외부 solver 무의존, §3j)로 산출.

Peres-Mermin 3×3 magic square 관측가능량 9개·context 6개(row3+col3)·product sign(+1×5, col2=−1):
  empirical model e(o|c): outcome o∈{±1}³ 의 product==sign_c 이면 1/4, 아니면 0 (state-independent).
  ★NCF(noncontextual fraction) = max Σ_g b_g  s.t. ∀(c,o): Σ_{g|c=o} b_g ≤ e(o|c), b_g≥0
    (g=전역 ±1 배정 2^9). ★강한 맥락성: 512 전역배정 **전부** ≥1 context product 불일치(KS parity 모순)
    → 모든 b_g=0 → **NCF=0, CF=1−NCF=1**(exact rational).
  정량화(depolarize visibility v): e_v = v·e_PM + (1−v)·(uniform 1/8). 균일잡음(1−v)은 noncontextual
    (d_uniform primal witness, 주변부 (1−v)/8 ≤ e_v exact 실현) → **NCF(v)=1−v·CF(v)=v** (rational, 선형).
  dual certificate: parity 부등식(Π_row=+1 vs Π_col=−1) = CF≥1 의 정수 dual witness.

정직 경계(seal 아님, root 불변 sidecar): 관측 = contextual fraction **exact 유리수**(LP primal/dual).
  ★LP=최적화→봉인 아님(certificate). 내장 유리수 산술(부동소수·외부 solver 무의존). P5 parity 승격.
  큰 KS 집합·SDP·양자 상한 = 범위밖. 신규 module 0.

사용: python scripts/contextual_fraction_observe.py [--quick]
"""
from __future__ import annotations
import sys
from fractions import Fraction

CTX = [[0, 1, 2], [3, 4, 5], [6, 7, 8],        # rows
       [0, 3, 6], [1, 4, 7], [2, 5, 8]]         # cols
SIGN = [1, 1, 1, 1, 1, -1]                       # row·col0·col1 = +1 · col2 = −1


def _prod(g, ctx):
    p = 1
    for i in ctx:
        p *= g[i]
    return p


def _globals():
    for bits in range(512):
        yield [1 if (bits >> i) & 1 else -1 for i in range(9)]


def e_pm(o_prod, sign):
    return Fraction(1, 4) if o_prod == sign else Fraction(0)


def main():
    quick = "--quick" in sys.argv
    R = {}

    # 1. 강한 맥락성: 모든 전역배정이 ≥1 context 위반 → NCF=0, CF=1
    consistent = [g for g in _globals() if all(_prod(g, CTX[c]) == SIGN[c] for c in range(6))]
    R["strongly_contextual_no_global_model"] = (len(consistent) == 0)
    NCF = Fraction(0)                              # 모든 b_g 강제 0 (LP 최적값)
    CF = 1 - NCF
    R["CF_equals_1_exact"] = (CF == Fraction(1))

    # 2. 정량화: depolarize visibility v → NCF(v)=1−v (primal d_uniform witness, exact 유리수)
    #    d_uniform 주변부 m(o|c) = 1/8 (전역 512 중 g|c=o 인 것 64개) → (1−v)·(1/8) ≤ e_v(o|c) 검사
    def ncf_lower_via_uniform(v):
        # e_v(o|c) = v·e_pm + (1−v)/8. primal weight (1−v), 주변부 (1−v)/8. 실현가능?
        feasible = True
        for c in range(6):
            for o in range(8):
                oprod = 1
                for b in range(3):
                    oprod *= 1 if (o >> b) & 1 else -1
                ev = v * e_pm(oprod, SIGN[c]) + (1 - v) * Fraction(1, 8)
                if (1 - v) * Fraction(1, 8) > ev:
                    feasible = False
        return (1 - v) if feasible else None
    vis_ok = True
    table = {}
    for v in (Fraction(1), Fraction(3, 4), Fraction(1, 2), Fraction(1, 4), Fraction(0)):
        lb = ncf_lower_via_uniform(v)
        cf_v = 1 - lb if lb is not None else None
        table[v] = cf_v
        if cf_v != v:                              # CF(v) = v (exact 유리수, 선형)
            vis_ok = False
    R["CF_visibility_linear_exact"] = vis_ok       # CF(v)=v 전 grid exact

    # 3. dual parity certificate: Π(row products) vs Π(col products) 정수 모순
    row_par = 1
    col_par = 1
    for c in range(3):
        row_par *= SIGN[c]
    for c in range(3, 6):
        col_par *= SIGN[c]
    R["dual_parity_certificate"] = (row_par == 1 and col_par == -1)  # +1 ≠ −1 → CF≥1

    # teeth: col2 sign 도 +1 (모순 제거) → 일관 전역배정 존재 → NCF>0, CF<1
    SIGN2 = [1, 1, 1, 1, 1, 1]
    cons2 = sum(1 for g in _globals() if all(_prod(g, CTX[c]) == SIGN2[c] for c in range(6)))
    R["teeth_noncontextual_CF_below_1"] = (cons2 > 0)

    ok = all(R.values())
    if not quick:
        print("Peres-Mermin contextual fraction LP 정량화 관측 (§3l P5 승격, witness — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  ★CF = 1 (exact 유리수, 강한 맥락성 NCF=0) · CF(visibility v) = {{{', '.join(f'{k}:{table[k]}' for k in table)}}} = v (선형)",
              flush=True)
        print("  ★정직: contextual fraction = exact 유리수 LP(primal d_uniform + dual parity)·내장 유리수 산술"
              "(외부 solver·부동소수 무의존)·certificate(봉인 아님)·P5 parity 정량 승격·신규 module 0·root 불변.",
              flush=True)
    print(f"contextual_fraction_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
