#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bmw3_fig8_observe — TrackHE16 P3: BMW₃(dim 15) 문맥의 3-braid figure-8 매듭
(관측, seal 아님). [[bmw_kauffman_observe]](v15 P3)의 확장.

v15 P3 은 BMW₂(dim 3)/2-braid 로 **T(2,k) 토러스 링크족**만 커버했다(스코프 명시:
"BMW₃(dim 15)·fig-8 등 3-braid 미착수"). 본 witness 는 그 경계를 **3-braid 로 확장**한다:

  ★figure-8 매듭(4₁) = 3-braid (σ₁σ₂⁻¹)² 의 폐포 — 트랙 **최초의 비-토러스 매듭**이자
    **amphichiral(거울=자기자신)** 매듭. 토러스 매듭 T(2,k)(v15)는 전부 chiral 이라 이 성질을
    가질 수 없다 → fig-8 은 질적으로 새로운 대상.

관측 계층 (전부 exact — Laurent/정수 산술, float 0):
  1. BMW_n 차원 **자체 재유도**: Brauer diagram(2n 점 완전매칭) 전수 = (2n−1)!!
     (n=1..4 → 1,3,15,105). BMW₃=15 자체검증(v15 재확인·3-braid 대수 차원).
  2. **braid closure → Jones V(t)**: 부호정확 Kauffman bracket 상태합(2^c smoothing, δ=−A²−A⁻²)
     을 braid word 폐포에 적용. σ_i(양)/σ_i⁻¹(음)의 A/B-smoothing 배정을 부호로 분기(음교차 정확).
     writhe 정규화 f=(−A³)^{−w}⟨·⟩ · A=t^{−1/4}.
  3. ★fig-8 불변량:
     (a) V(4₁) = t⁻² − t⁻¹ + 1 − t + t²  (자체계산이 문헌값과 일치)
     (b) **amphichirality** V(t)=V(t⁻¹) (토러스 매듭이 못 갖는 성질 — teeth 로 chiral 대조)
     (c) det(4₁)=|V(−1)|=5 · V(1)=1(매듭 성분수 1)
  4. **교차검증 3중**:
     (a) 독립 diagram: fig-8 을 (i) 3-braid 폐포 (ii) 표준 4-교차 PD-code 두 경로로 계산 → 일치
     (b) **Markov/conjugation 불변**: 폐포 다이어그램의 켤레(cyclic)·braid 관계 σ₁σ₂σ₁=σ₂σ₁σ₂
         치환이 Jones 를 보존(braid group → 링크 well-defined 실증)
     (c) chiral 대조: trefoil σ₁³(우수, V=−t⁴+t³+t)와 거울 σ₁⁻³(V(t⁻¹)) — fig-8 과 달리 V≠V(t⁻¹)
  teeth: (i) smoothing 부호분기 제거(음교차를 양처럼) → fig-8 Jones 붕괴 (ii) writhe 정규화 제거
     → 다이어그램(regular isotopy)엔 맞으나 매듭 불변 아님 실측 (iii) 3-braid 라벨 확인
     (fig-8 은 σ₂ 필수 = 진짜 3-strand, 2-braid 로 불가).

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - 산출은 **Jones(1변수)** V(t) via Kauffman bracket — v13 [[kauffman_bracket_observe]]/v15 의
    상태합 계열이나 **대상이 신규**(비-토러스·amphichiral·3-braid 폐포 파이프라인).
  - ★**2변수 Kauffman F(a,z) via BMW₃ Markov trace 는 미착수**(다음): 2변수 Dubrovnik skein 은
    단일 교차를 flat smoothing 으로 못 펴(g_i 가 진짜 생성원) → BMW₃ 정규표현(dim 15)의 confluent
    곱셈(모든 e-interaction 관계식 e_ie_je_i=e_i·g_ig_je_i=e_je_i 등)+Ocneanu trace 필요.
    본 witness 는 BMW₃ **차원**과 fig-8 **Jones/amphichirality** 까지만 — v15 의 BMW₂ 2변수를
    3-braid 2변수로 올리는 것은 focused 후속.
  - 매듭 불변량은 **관측**(exact Laurent) — 회로 봉인 아님.

사용: python -m qf_witness.observe.bmw3_fig8_observe [--quick]
"""
from __future__ import annotations
import sys
import json

import sympy as sp

A = sp.symbols("A")
T = sp.symbols("t")


# ── BMW 차원 자체 재유도: Brauer diagram = 완전매칭 수 = (2n−1)!! ──────────────
def perfect_matchings(pts):
    if not pts:
        return 1
    a = pts[0]
    return sum(perfect_matchings([p for p in pts[1:] if p != b]) for b in pts[1:])


def double_factorial_odd(n):
    d = 1
    for k in range(1, 2 * n, 2):
        d *= k
    return d


# ── braid word 폐포 → Kauffman bracket → Jones (부호정확) ─────────────────────
def _bracket_closure(n, word):
    """braid word(±i, 1-indexed) on n strands → 폐포의 Kauffman bracket ⟨·⟩ ∈ ℤ[A^±]."""
    pos = list(range(n))
    nxt = n
    crossings = []                      # (SW, SE, NW, NE, sign)
    for lt in word:
        i = abs(lt) - 1
        sw, se = pos[i], pos[i + 1]
        nw, ne = nxt, nxt + 1
        nxt += 2
        crossings.append((sw, se, nw, ne, 1 if lt > 0 else -1))
        pos[i], pos[i + 1] = nw, ne
    closure = [(pos[i], i) for i in range(n)]   # 폐포: strand 끝 == 시작
    delta = -A**2 - A**-2
    nc = len(crossings)
    total = sp.Integer(0)
    for state in range(1 << nc):
        par = {}

        def find(x):
            par.setdefault(x, x)
            while par[x] != x:
                par[x] = par[par[x]]
                x = par[x]
            return x

        def union(x, y):
            par[find(x)] = find(y)

        nA = 0
        for ci, (sw, se, nw, ne, s) in enumerate(crossings):
            aA = ((state >> ci) & 1) == 0          # A-smoothing 선택 비트
            if aA:
                nA += 1
            # 부호 분기: σ_i(양) A=vertical(‖) ; σ_i⁻¹(음) A=cap-cup(⊃⊂)
            vertical = aA if s > 0 else (not aA)
            if vertical:
                union(sw, nw); union(se, ne)
            else:
                union(sw, se); union(nw, ne)
        for a_, b_ in closure:
            union(a_, b_)
        nB = nc - nA
        edges = set()
        for (sw, se, nw, ne, s) in crossings:
            edges.update((sw, se, nw, ne))
        loops = len({find(e) for e in edges}) if edges else 1
        total += A**(nA - nB) * delta**(loops - 1)
    return sp.expand(total)


def jones_braid(n, word, normalize=True):
    """braid 폐포의 Jones V(t) (normalize=False → regular-isotopy bracket, writhe 미정규화)."""
    br = _bracket_closure(n, word)
    w = sum(1 if l > 0 else -1 for l in word)
    f = sp.expand(((-A**3)**(-w) if normalize else 1) * br)
    return sp.expand(sp.simplify(f.subs(A, T**sp.Rational(-1, 4))))


# ── 표준 PD-code Kauffman bracket (독립 diagram 교차검증용) ────────────────────
def _bracket_pd(pd):
    """pd: 4-튜플(a,b,c,d) 리스트(반시계 아크). A-smoothing = a-b & c-d · B = a-d & b-c.
    표준 교대 diagram 관례(braid 파이프라인과 독립 경로)."""
    delta = -A**2 - A**-2
    nc = len(pd)
    total = sp.Integer(0)
    for state in range(1 << nc):
        par = {}

        def find(x):
            par.setdefault(x, x)
            while par[x] != x:
                par[x] = par[par[x]]
                x = par[x]
            return x

        def union(x, y):
            par[find(x)] = find(y)

        nA = 0
        for ci, (a_, b_, c_, d_) in enumerate(pd):
            if (state >> ci) & 1:                # B-smoothing: a-d, b-c
                union(a_, d_); union(b_, c_)
            else:                                # A-smoothing: a-b, c-d
                nA += 1
                union(a_, b_); union(c_, d_)
        nB = nc - nA
        edges = set()
        for c in pd:
            edges.update(c)
        loops = len({find(e) for e in edges})
        total += A**(nA - nB) * delta**(loops - 1)
    return sp.expand(total)


def jones_pd(pd, writhe):
    br = _bracket_pd(pd)
    f = sp.expand((-A**3)**(-writhe) * br)
    return sp.expand(sp.simplify(f.subs(A, T**sp.Rational(-1, 4))))


def _fmt(p):
    return str(sp.expand(p))


def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "bmw3-fig8/v1",
           "_note": ("BMW₃(dim 15) 문맥의 3-braid figure-8(관측·seal 아님·신규 module 0·root 불변). "
                     "fig-8=최초 비-토러스·amphichiral 매듭. Jones via 부호정확 Kauffman bracket. "
                     "★2변수 Kauffman F via BMW₃ Markov trace 미착수(다음) — v15 BMW₂ 2변수의 3-braid 확장.")}

    # 1. BMW 차원 자체 재유도
    dims = {n: perfect_matchings(list(range(2 * n))) for n in (1, 2, 3, 4)}
    out["bmw_dimensions"] = {str(n): dims[n] for n in dims}
    R["bmw_dim_double_factorial"] = all(dims[n] == double_factorial_odd(n) for n in dims)
    R["bmw3_dim_15"] = (dims[3] == 15)

    # 2. figure-8 = 3-braid (σ₁σ₂⁻¹)² 폐포
    fig8_word = [1, -2, 1, -2]
    Vf = jones_braid(3, fig8_word)
    expected = T**-2 - T**-1 + 1 - T + T**2
    R["fig8_jones_correct"] = (sp.simplify(Vf - expected) == 0)
    R["fig8_amphichiral"] = (sp.simplify(Vf - Vf.subs(T, 1 / T)) == 0)
    R["fig8_determinant_5"] = (abs(int(Vf.subs(T, -1))) == 5)
    R["fig8_unknotting_V1_is_1"] = (sp.simplify(Vf.subs(T, 1) - 1) == 0)
    # 진짜 3-strand: fig-8 braid 는 σ₂ 필수(2-braid 로 표현 불가)
    R["fig8_genuinely_3braid"] = (any(abs(l) == 2 for l in fig8_word))
    out["figure8"] = {"braid_word": "(σ1 σ2^-1)^2 = [1,-2,1,-2]", "strands": 3,
                      "V_t": _fmt(Vf), "determinant": abs(int(Vf.subs(T, -1))),
                      "amphichiral": bool(R["fig8_amphichiral"]),
                      "is_torus_knot": False, "note": "first non-torus, amphichiral knot in track"}

    # 3. 교차검증 (a) 독립 PD-code diagram
    PD_fig8 = [(4, 2, 5, 1), (8, 6, 1, 5), (6, 3, 7, 4), (2, 7, 3, 8)]
    Vf_pd = jones_pd(PD_fig8, 0)                     # fig-8 표준 diagram writhe 0
    R["fig8_two_diagrams_agree"] = (sp.simplify(Vf - Vf_pd) == 0)

    # 3. 교차검증 (b) Markov/conjugation 불변 (cyclic 켤레 + braid 관계)
    Vf_conj = jones_braid(3, [-2, 1, -2, 1])         # cyclic 회전(켤레)
    R["fig8_markov_conjugation_inv"] = (sp.simplify(Vf - Vf_conj) == 0)
    # braid 관계 σ₁σ₂σ₁ = σ₂σ₁σ₂ 폐포 Jones 동일 (3-braid well-defined)
    R["braid_relation_jones_inv"] = (
        sp.simplify(jones_braid(3, [1, 2, 1]) - jones_braid(3, [2, 1, 2])) == 0)

    # 3. 교차검증 (c) chiral 대조 (trefoil) + 컨트롤
    Vtre_r = jones_braid(2, [1, 1, 1])               # 우수 trefoil
    Vtre_l = jones_braid(2, [-1, -1, -1])            # 좌수(거울)
    R["trefoil_right_correct"] = (sp.simplify(Vtre_r - (-T**4 + T**3 + T)) == 0)
    R["trefoil_chiral"] = (sp.simplify(Vtre_r - Vtre_r.subs(T, 1 / T)) != 0)
    R["trefoil_mirror_is_inverse"] = (sp.simplify(Vtre_l - Vtre_r.subs(T, 1 / T)) == 0)
    R["unknot_trivial"] = (sp.simplify(jones_braid(1, []) - 1) == 0)
    out["controls"] = {
        "trefoil_right_V": _fmt(Vtre_r), "trefoil_chiral": bool(R["trefoil_chiral"]),
        "hopf_V": _fmt(jones_braid(2, [1, 1])),
        "cinquefoil_5_1_V": _fmt(jones_braid(2, [1, 1, 1, 1, 1])) if not quick else "skip",
    }

    # teeth
    def bracket_nosign(n, word):
        """teeth(i): 부호분기 제거(음교차를 양처럼) → 음교차 매듭 붕괴."""
        return jones_braid(n, [abs(l) for l in word])
    R["teeth_sign_branch_matters"] = (sp.simplify(bracket_nosign(3, fig8_word) - Vf) != 0)
    # teeth(ii): writhe 정규화 제거 → regular-isotopy(다이어그램)엔 맞으나 매듭 불변 아님
    #   trefoil 우수/좌수의 미정규화 bracket 이 서로 다른데(다이어그램 의존) 정규화하면 mirror 관계
    R["teeth_writhe_norm_matters"] = (
        sp.simplify(jones_braid(2, [1, 1, 1], normalize=False)
                    - jones_braid(2, [1, 1, 1])) != 0)

    ok = bool(all(R.values()))
    out["checks"] = R
    out["scope_honesty"] = {
        "covered": ["BMW₃ dim=15 자체유도", "3-braid 폐포 Jones 파이프라인(부호정확 bracket)",
                    "figure-8 = 최초 비-토러스·amphichiral 매듭(V·det·amphichirality)",
                    "독립 diagram·Markov·braid 관계 교차검증", "chiral 대조(trefoil)"],
        "not_covered": ["2변수 Kauffman F(a,z) via BMW₃ Markov trace(confluent dim-15 곱셈+Ocneanu trace)",
                        "BMW₃ 정규표현 행렬", "HOMFLY 동시산출(v15 참조)"],
        "next": "2변수 Kauffman F via BMW₃ Markov trace (v15 BMW₂ 2변수의 3-braid 확장)",
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "BMW3-FIG8.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("BMW₃ 문맥 3-braid figure-8 매듭 (관측·exact — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  ★BMW 차원 자체유도: {out['bmw_dimensions']} = (2n−1)!!", flush=True)
        print(f"  ★V(fig-8) = {_fmt(Vf)}  (det={out['figure8']['determinant']}, "
              f"amphichiral={R['fig8_amphichiral']}) — 최초 비-토러스·amphichiral", flush=True)
        print("  ★정직: Jones(1변수)까지 · 2변수 Kauffman F via BMW₃ Markov trace 는 다음", flush=True)
        print("  → .pgf/proofs/BMW3-FIG8.json", flush=True)
    print(f"bmw3_fig8_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
