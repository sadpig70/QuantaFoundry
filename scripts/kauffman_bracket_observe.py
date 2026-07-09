#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kauffman_bracket_observe — TrackHE13 P4: Kauffman bracket 상태합(state-sum) witness (관측, seal 아님).

★fib_jones_observe(TrackHE4/HE5)와의 스코프 구분(반드시 명시):
  - fib_jones_observe 는 **braid word 유니터리**의 가중 trace·skein 재귀로 **특정 값**(A=e^{3πi/5},
    t=e^{−2πi/5} 고정점)에서 Jones **수치**를 계산했다(Fibonacci 소비층·행렬 trace).
  - 본 witness 의 신규 대상은 (i) **상태합 알고리즘 자체** — 2^n smoothing 전개로 얻는 **generic-A
    exact Laurent 다항식** ⟨L⟩ ∈ ℤ[A,A⁻¹](braid trace 아님·특정 A 대입 아님·심볼릭 다항식 객체), 그리고
    (ii) 이미 봉인/관측된 층으로의 **specialization 다리**(A=i → TL δ=2 정수골격, t=e^{−2πi/5} → fib_jones
    수치 교차). 즉 fib_jones 가 *한 점의 값*이라면 본 witness 는 *다항식 전체*를 조합적으로 생성한다.

관측(sympy exact — 승인 게이트 0·신규 module 0·root 불변 sidecar):
  1. 매듭/링크를 PD(planar diagram) 코드로 표현: 우삼엽 3₁(3교차)·figure-eight 4₁(4교차)·
     Hopf 링크(2교차)·unknot(0/1교차 sanity).
  2. 완전 상태합 Kauffman bracket: 각 교차 → A-smoothing 또는 A⁻¹(=B)-smoothing. 2^n 상태마다
     union-find 로 loop 수 ℓ 계수. ⟨L⟩ = Σ_states A^(#A−#B)·δ^(ℓ−1), δ=−A²−A⁻². exact Laurent(ℤ[A,A⁻¹]).
  3. Reidemeister/일관성: ⟨unknot⟩=1 · 양의 kink 추가 → ×(−A³)(kinked unknot 다이어그램 X[1,1,2,2]로
     R1 명시 검증) · ★R1 불변량 강검증: kinked trefoil(음의 curl, w −3→−4)의 Jones == 원 삼엽.
  4. Jones: V_L(t)=(−A)^(−3w)·⟨L⟩, t=A⁻⁴, w=writhe. 본 규약(아래) 삼엽 V=−t⁻⁴+t⁻³+t⁻¹(음멱 지지·
     writhe w=−3); figure-eight V=t⁻²−t⁻¹+1−t+t²(amphichiral V(t)==V(1/t) 검증);
     Hopf V=−t^(−5/2)−t^(−1/2)(2성분·반정수 멱·A 다항으로 처리).
  5. specialization 다리(복리 가치):
     (a) A=i → δ=−A²−A⁻²=−(−1)−(−1)=2 (봉인된 TL δ=2 정수골격의 loop 값). ★정직한 정정: 이때
         bracket 은 각 상태가 i^(#A−#B)·2^(ℓ−1) → **ℤ[i](가우스 정수)**에 착지(삼엽=i·순허수).
         real 정수 아님. 그러나 writhe 정규화 후 V(1)=(−2)^(성분수−1) ∈ ℤ(real 정수) 회복 —
         temperley_lieb_observe 의 δ=2·A=i·ℤ[i] Kauffman(σ=A·I+A⁻¹e)와 **정확히 동일 착지**.
     (b) fib_jones 교차: 본 generic 다항식을 t=e^{−2πi/5} 에서 수치 평가 → fib_jones 값과 대조.
         삼엽은 fib_jones 규약(V=t+t³−t⁴)이 본 규약의 **경상(t↔t⁻¹)** → mirror-V 로 정확 일치;
         figure-eight 는 amphichiral 이라 **직접 일치**(둘 다 1−√5 at that t). 규약차 정직 문서화.
  6. teeth: δ 멱 오염(ℓ 대신 ℓ−1 아님) → 삼엽 다항식 변함·unknot≠1 · 상태 한 개 누락 → 삼엽 변함.

정직 경계(★관측·seal 아님·root 불변 sidecar·module 0): witness = 상태합 알고리즘의 exact Laurent
불변량. 매듭 다항식 = exact **대수 불변량**(유니터리 아님) · 소형 매듭만(상태합 2^n·일반 bracket #P-hard) ·
Jones 값·매듭 동치판정·mirror 관계 = 관측(fib_jones INV-Q3 경계 상속). [[fib-jones-observe]]·
[[temperley-lieb-observe]] 교차.

사용: python scripts/kauffman_bracket_observe.py [--quick]
"""
from __future__ import annotations
import os, sys, json, itertools
import sympy as sp

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".pgf", "proofs", "KAUFFMAN-BRACKET-OBSERVE.json")

A = sp.Symbol("A")
DELTA = -A**2 - A**-2                                   # Kauffman δ = −A²−A⁻²
t = sp.Symbol("t")

# ── PD(planar diagram) 코드: 각 교차 X[a,b,c,d] (반시계 순서, understrand a→c).
#    각 edge 라벨은 정확히 2회 등장 → 외부 arc 매칭. writhe 는 본 규약(음교차) 명시값. ────────────
TREFOIL = [(1, 4, 2, 5), (3, 6, 4, 1), (5, 2, 6, 3)]           # 우삼엽 3₁, w=−3
FIG8 = [(4, 2, 5, 1), (8, 6, 1, 5), (6, 3, 7, 4), (2, 7, 3, 8)]  # 4₁, w=0
HOPF = [(1, 3, 2, 4), (3, 1, 4, 2)]                            # Hopf, w=−2 (2성분)
KINK_POS = [(1, 1, 2, 2)]                                      # 양의 kink unknot → −A³
KINKED_TREFOIL = [(7, 4, 2, 5), (3, 6, 4, 1), (5, 2, 6, 3), (1, 8, 8, 7)]  # 음 curl, w=−4


def _find(parent, x):
    root = x
    while parent[root] != root:
        root = parent[root]
    while parent[x] != root:
        parent[x], x = root, parent[x]
    return root


def _union(parent, a, b):
    ra, rb = _find(parent, a), _find(parent, b)
    if ra != rb:
        parent[ra] = rb


def count_loops(pd, state):
    """union-find 로 smoothing 후 loop(연결성분) 수 ℓ 계수. state[i]: 0=A, 1=B."""
    parent = {(ci, port): (ci, port) for ci in range(len(pd)) for port in range(4)}
    # 외부 arc: 같은 edge 라벨의 두 (crossing,port) 를 연결
    edgemap = {}
    for ci, cr in enumerate(pd):
        for port, e in enumerate(cr):
            edgemap.setdefault(e, []).append((ci, port))
    for occ in edgemap.values():
        _union(parent, occ[0], occ[1])
    # 내부 smoothing: A → (0-1,2-3), B → (0-3,1-2)  (kinked unknot 로 부호 검증됨)
    for ci, s in enumerate(state):
        if s == 0:
            _union(parent, (ci, 0), (ci, 1)); _union(parent, (ci, 2), (ci, 3))
        else:
            _union(parent, (ci, 0), (ci, 3)); _union(parent, (ci, 1), (ci, 2))
    roots = {_find(parent, (ci, port)) for ci in range(len(pd)) for port in range(4)}
    return len(roots)


def bracket(pd, loop_shift=1, drop_state=None):
    """generic-A exact Kauffman bracket ⟨L⟩ ∈ ℤ[A,A⁻¹] (완전 상태합).

    loop_shift: 정상=1 (δ^(ℓ−1)); teeth 에서 0 (δ^ℓ)로 오염.
    drop_state: teeth 에서 특정 상태 튜플 하나 누락.
    """
    n = len(pd)
    if n == 0:
        return sp.Integer(1)
    total = sp.Integer(0)
    for state in itertools.product((0, 1), repeat=n):
        if drop_state is not None and state == drop_state:
            continue
        loops = count_loops(pd, state)
        expo = sum(1 if s == 0 else -1 for s in state)        # #A − #B
        total += A**expo * DELTA**(loops - loop_shift)
    return sp.expand(total)


def _a_terms(expr):
    """expanded Laurent(A) → {A 멱: 정수계수} 딕셔너리 (as_coeff_exponent 로 분해)."""
    terms = {}
    for term in sp.Add.make_args(sp.expand(expr)):
        coeff, power = term.as_coeff_exponent(A)
        terms[int(power)] = terms.get(int(power), 0) + coeff
    return {p: c for p, c in terms.items() if c != 0}


def jones_in_t(pd, writhe):
    """V_L(t) = (−A)^(−3w)·⟨L⟩, t=A⁻⁴. A 멱 n → t^(−n/4) 로 정확 치환(exact sympy)."""
    v_in_a = sp.expand((-A)**(-3 * writhe) * bracket(pd))
    v = sp.Integer(0)
    for power, coeff in _a_terms(v_in_a).items():
        v += coeff * t**sp.Rational(-power, 4)
    return sp.expand(v)


def observe():
    R = {}
    # ── 1~2. generic-A exact bracket ─────────────────────────────────────
    b_unknot = bracket([])
    b_tref = bracket(TREFOIL)
    b_fig8 = bracket(FIG8)
    b_hopf = bracket(HOPF)
    R["bracket_unknot_eq_1"] = bool(sp.simplify(b_unknot - 1) == 0)
    # 삼엽 ⟨L⟩ = −A⁻⁵−A³+A⁷ (본 규약; 경상 = A→A⁻¹)
    R["bracket_trefoil"] = bool(sp.simplify(b_tref - (-A**-5 - A**3 + A**7)) == 0)
    # figure-eight ⟨L⟩ = A⁸−A⁴+1−A⁻⁴+A⁻⁸ (mirror 대칭 = amphichiral)
    R["bracket_fig8"] = bool(sp.simplify(b_fig8 - (A**8 - A**4 + 1 - A**-4 + A**-8)) == 0)
    R["bracket_fig8_amphichiral"] = bool(sp.simplify(b_fig8 - b_fig8.subs(A, 1 / A)) == 0)
    # Hopf ⟨L⟩ = −A⁴−A⁻⁴
    R["bracket_hopf"] = bool(sp.simplify(b_hopf - (-A**4 - A**-4)) == 0)

    # ── 3. R1: 양의 kink → ×(−A³) (kinked unknot 명시) + R1 불변 강검증 ──────
    b_kink = bracket(KINK_POS)
    R["R1_positive_kink_times_minusA3"] = bool(sp.simplify(b_kink - (-A**3)) == 0)
    b_ktref = bracket(KINKED_TREFOIL)
    R["R1_kinked_bracket_times_minusA_inv3"] = bool(
        sp.simplify(b_ktref - (-A**-3) * b_tref) == 0)

    # ── 4. Jones (t) ─────────────────────────────────────────────────────
    v_tref = jones_in_t(TREFOIL, -3)
    v_fig8 = jones_in_t(FIG8, 0)
    v_hopf = jones_in_t(HOPF, -2)
    R["jones_trefoil"] = bool(sp.simplify(v_tref - (-t**-4 + t**-3 + t**-1)) == 0)
    R["jones_fig8"] = bool(sp.simplify(v_fig8 - (t**-2 - t**-1 + 1 - t + t**2)) == 0)
    R["jones_fig8_amphichiral_V_t_eq_V_1overt"] = bool(
        sp.simplify(v_fig8 - v_fig8.subs(t, 1 / t)) == 0)
    R["jones_hopf"] = bool(sp.simplify(v_hopf - (-t**sp.Rational(-5, 2) - t**sp.Rational(-1, 2))) == 0)
    # R1 불변량 강검증: kinked trefoil(w=−4) Jones == 원 삼엽(w=−3)
    v_ktref = jones_in_t(KINKED_TREFOIL, -4)
    R["R1_invariance_jones_unchanged"] = bool(sp.simplify(v_ktref - v_tref) == 0)

    # ── 5a. A=i → δ=2, TL δ=2 정수골격 다리 (★ℤ[i] 착지 정직 정정) ──────────
    R["delta_at_A_i_eq_2"] = bool(sp.simplify(DELTA.subs(A, sp.I) - 2) == 0)
    gauss = {}
    for nm, pd, comps in [("unknot", [], 1), ("trefoil", TREFOIL, 1),
                          ("fig8", FIG8, 1), ("hopf", HOPF, 2)]:
        bi = sp.simplify(bracket(pd).subs(A, sp.I))
        re, im = sp.re(bi), sp.im(bi)
        is_gauss = bool(re == sp.nsimplify(re, rational=True).round() or re.is_integer) and \
            bool(im.is_integer) and bool(re.is_integer)
        gauss[nm] = {"bracket_at_A_i": str(bi),
                     "gaussian_integer": bool(sp.im(bi).is_integer and sp.re(bi).is_integer),
                     "real_integer": bool(sp.im(bi) == 0 and sp.re(bi).is_integer)}
    # 모든 bracket(A=i) ∈ ℤ[i] (δ=2·A=i 덕분)
    R["A_i_all_gaussian_integer"] = all(g["gaussian_integer"] for g in gauss.values())
    # 삼엽만 순허수(real 정수 아님) — 정직한 정정
    R["A_i_trefoil_not_real_integer"] = (gauss["trefoil"]["gaussian_integer"]
                                         and not gauss["trefoil"]["real_integer"])
    # writhe 정규화 후 V(1)=(−2)^(성분수−1) ∈ ℤ (real 정수 회복)
    v1 = {}
    for nm, pd, w, comps in [("trefoil", TREFOIL, -3, 1), ("fig8", FIG8, 0, 1),
                             ("hopf", HOPF, -2, 2)]:
        val = sp.simplify(jones_in_t(pd, w).subs(t, 1))
        v1[nm] = {"V_at_t_1": str(val), "ok": bool(sp.simplify(val - (-2)**(comps - 1)) == 0)}
    R["A_i_jones_V1_eq_neg2_pow_comps"] = all(x["ok"] for x in v1.values())

    # ── 5b. fib_jones 교차 (t=e^{−2πi/5}) ────────────────────────────────
    tval = sp.exp(-2 * sp.I * sp.pi / 5)
    fib_tref = tval + tval**3 - tval**4                    # fib_jones V(삼엽) 규약(경상)
    fib_fig8 = tval**-2 - tval**-1 + 1 - tval + tval**2    # fib_jones V(4₁)=1−√5
    # 본 삼엽 mirror-V(t↔t⁻¹) == fib_jones 삼엽 (규약차=mirror, exact 심볼릭)
    v_tref_mirror = sp.expand(v_tref.subs(t, 1 / t))
    R["fib_cross_trefoil_mirror_symbolic"] = bool(
        sp.simplify(v_tref_mirror - (t + t**3 - t**4)) == 0)
    my_tref_at = complex(sp.N(v_tref.subs(t, tval)))
    my_mirror_at = complex(sp.N(v_tref_mirror.subs(t, tval)))
    fib_tref_at = complex(sp.N(fib_tref))
    R["fib_cross_trefoil_numeric_mirror_matches"] = bool(abs(my_mirror_at - fib_tref_at) < 1e-9)
    R["fib_cross_trefoil_direct_differs_by_mirror"] = bool(abs(my_tref_at - fib_tref_at) > 1e-3)
    # figure-eight amphichiral → 직접 일치(둘 다 1−√5)
    my_fig8_at = complex(sp.N(v_fig8.subs(t, tval)))
    fib_fig8_at = complex(sp.N(fib_fig8))
    R["fib_cross_fig8_direct_matches"] = bool(abs(my_fig8_at - fib_fig8_at) < 1e-9
                                              and abs(my_fig8_at.real - (1 - 5**0.5)) < 1e-9)

    # ── 6. teeth ─────────────────────────────────────────────────────────
    bad_shift = bracket(TREFOIL, loop_shift=0)             # δ^ℓ (틀린 지수)
    R["teeth_wrong_delta_exponent"] = bool(sp.simplify(bad_shift - b_tref) != 0
                                           and sp.simplify(bracket([(1, 1, 2, 2)], loop_shift=0)) != -A**3)
    bad_drop = bracket(TREFOIL, drop_state=(0, 0, 0))      # 상태 한 개 누락
    R["teeth_drop_one_state"] = bool(sp.simplify(bad_drop - b_tref) != 0)
    # unknot≠1 하에서 오염 검출: kinked unknot 을 δ^ℓ 로 → −A³ 아님
    R["teeth_unknot_kink_corrupted"] = bool(
        sp.simplify(bracket(KINK_POS, loop_shift=0) - (-A**3)) != 0)

    ok = all(R.values())
    detail = {
        "brackets_generic_A": {"unknot": str(b_unknot), "trefoil": str(sp.expand(b_tref)),
                               "fig8": str(sp.expand(b_fig8)), "hopf": str(sp.expand(b_hopf)),
                               "kink_positive": str(b_kink)},
        "jones_t": {"trefoil": str(v_tref), "fig8": str(v_fig8), "hopf": str(v_hopf)},
        "A_i_specialization": gauss, "jones_at_t1": v1,
        "handedness": "삼엽 ⟨L⟩=−A⁻⁵−A³+A⁷ · writhe w=−3(본 PD 교차 전부 음) → V=−t⁻⁴+t⁻³+t⁻¹ "
                      "(음멱 지지). 경상(A→A⁻¹ / t↔t⁻¹) = −t⁴+t³+t. Hopf w=−2·fig8 w=0(amphichiral).",
        "fib_cross": {"trefoil_convention": "fib_jones V=t+t³−t⁴ = 본 규약의 mirror(t↔t⁻¹) → "
                                            "mirror-V 로 exact 일치 · direct 는 mirror 만큼 상이",
                      "fig8": "amphichiral → direct 일치 (둘 다 1−√5 at t=e^{−2πi/5})"}}
    return R, detail, ok


def main():
    quick = "--quick" in sys.argv
    R, detail, ok = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"_schema": "kauffman-bracket-observe-v1",
                       "_note": "Kauffman bracket 완전 상태합(2^n smoothing)으로 generic-A exact Laurent "
                                "불변량 ⟨L⟩∈ℤ[A,A⁻¹] 생성(fib_jones 의 특정-A trace 값과 스코프 구분). "
                                "R1·Jones·A=i→TL δ=2(ℤ[i] 착지)·fib_jones 교차(mirror 규약) 다리 + teeth. "
                                "★관측·seal 아님·신규 module 0·root 불변.",
                       "deterministic": True,
                       "checks": R, "detail": detail,
                       "honest_boundary": "witness=상태합 알고리즘 exact Laurent 불변량. 매듭 다항식=exact "
                                          "대수 불변량(유니터리 아님)·소형 매듭만(2^n·일반 #P-hard)·Jones 값/"
                                          "동치판정/mirror=관측. fib_jones INV-Q3 경계 상속.",
                       "ok": ok}, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("Kauffman bracket 상태합 관측 (generic-A exact Laurent — fib_jones 특정값과 스코프 구분):", flush=True)
        print(f"  ⟨trefoil⟩={detail['brackets_generic_A']['trefoil']}", flush=True)
        print(f"  ⟨fig8⟩={detail['brackets_generic_A']['fig8']}", flush=True)
        print(f"  ⟨hopf⟩={detail['brackets_generic_A']['hopf']} · kink+={detail['brackets_generic_A']['kink_positive']}", flush=True)
        print(f"  V(trefoil)={detail['jones_t']['trefoil']} · V(fig8)={detail['jones_t']['fig8']}", flush=True)
        print(f"  V(hopf)={detail['jones_t']['hopf']}", flush=True)
        print(f"  R1: 양kink×(−A³)={R['R1_positive_kink_times_minusA3']} · Jones 불변(kinked trefoil)={R['R1_invariance_jones_unchanged']}", flush=True)
        print(f"  A=i(δ=2): 전부 ℤ[i]={R['A_i_all_gaussian_integer']} · ★삼엽 순허수(real정수 아님)="
              f"{R['A_i_trefoil_not_real_integer']} · V(1)=(−2)^(c−1)={R['A_i_jones_V1_eq_neg2_pow_comps']}", flush=True)
        print(f"  fib_jones 교차: 삼엽 mirror 일치={R['fib_cross_trefoil_numeric_mirror_matches']} "
              f"(direct 는 규약차={R['fib_cross_trefoil_direct_differs_by_mirror']}) · fig8 직접 일치={R['fib_cross_fig8_direct_matches']}", flush=True)
        print(f"  teeth: δ지수오염={R['teeth_wrong_delta_exponent']} · 상태누락={R['teeth_drop_one_state']} · unknot오염={R['teeth_unknot_kink_corrupted']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"kauffman_bracket_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
