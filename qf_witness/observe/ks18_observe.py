#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ks18_observe — TrackHE10 P1: Kochen-Specker 18-벡터 state-independent 맥락성 witness (관측, seal 아님).

report10 최다수렴축(KS-18, 7/8). §3m P2·§4 "Kochen-Specker 18-vector 아직 없음" 관문. Peres-Mermin(TrackHE8
P5, qubit 9-관측가능 operator-product parity)·contextual fraction LP(TrackHE9 P2, 정량)의 **상보** — 4D(2큐빗)
**18-ray / 9-orthogonal-basis hypergraph 의 {0,1}-coloring 불가능**(ray-coloring 계층, 다른 조합 대상).

구조(정수 exact, 계산 탐색으로 구성·검증 — 기억 의존 배제):
  18 벡터 ∈ {0,±1}⁴, 9 basis(각 4-상호직교 정수 내적=0), ★**각 벡터 정확히 2 basis** 에 등장.
  KS coloring: c(v)∈{0,1}, 각 basis 에서 정확히 1개 ray 만 c=1(비맥락 hidden-variable 가정).

두 독립 경로로 불가능성:
  path A ★**parity certificate**: Σ_{9 basis}(basis당 1) = 9. 그러나 각 ray 가 정확히 2 basis 에 등장 →
    Σ = 2·Σ_v c(v) = **짝수**. 9(홀수) ≠ 짝수 → **정수 모순**(2k=9 불가). = state-independent KS.
  path B **exhaustive coloring 탐색**(독립): 2^18 {0,1}-배정 중 "각 basis 정확히 1" 만족하는 것이 **없음**을
    결정론적 백트래킹으로 확인 → path A 재확인.
  teeth: (a) 8 basis 부분집합은 coloring 존재(모순은 9-set 전체의 성질, 자명-불가능 아님)
    (b) 각 basis 4-상호직교·각 ray 2회 정수 검증.

정직 경계(★관측·seal 아님, root 불변 sidecar): witness = KS-18 hypergraph 조합 불가능성 정수 certificate.
  봉인 아님(§5, no-go 정리). Peres-Mermin(operator-product) 과 **대상 상이**(ray-coloring). 신규 module 0.
  [[trackhe8-report8]](Peres-Mermin)·contextual fraction(HE9 P2)·qutrit Wigner(HE9 P6) 맥락성 계보와 교차.

사용: python -m qf_witness.observe.ks18_observe [--quick]
"""
from __future__ import annotations
import sys
from itertools import combinations
from collections import Counter

# 계산 탐색(scripts 스캔)으로 구성·검증된 CEGA-등가 18-벡터 / 9-basis (정수 {0,±1}⁴)
VEC = [
    (0, 0, 0, 1), (0, 0, 1, -1), (0, 0, 1, 0), (0, 1, -1, 0), (0, 1, 0, -1),
    (0, 1, 0, 1), (0, 1, 1, 0), (1, -1, -1, -1), (1, -1, 0, 0), (1, -1, 1, -1),
    (1, -1, 1, 1), (1, 0, -1, 0), (1, 0, 0, 0), (1, 0, 0, 1), (1, 1, -1, -1),
    (1, 1, 0, 0), (1, 1, 1, -1), (1, 1, 1, 1),
]                                                       # index 0..17 (문서상 v1..v18)
BASES = [                                                # 1-based → 0-based
    [1, 3, 9, 16], [1, 4, 7, 13], [2, 8, 11, 16], [2, 9, 15, 18], [3, 5, 6, 13],
    [4, 8, 14, 17], [5, 10, 12, 18], [6, 11, 12, 17], [7, 10, 14, 15],
]
BASES = [[i - 1 for i in b] for b in BASES]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def basis_orthogonal(b):
    return all(dot(VEC[b[i]], VEC[b[j]]) == 0 for i in range(4) for j in range(i + 1, 4))


def has_coloring(bases, nv=18):
    """각 basis 정확히 1개 c=1 인 {0,1}-배정 존재? 결정론적 백트래킹."""
    color = [-1] * nv                                    # -1 미정, 0/1
    # basis 를 순서대로 채우며 제약 전파
    def bt(bi):
        if bi == len(bases):
            return True
        b = bases[bi]
        assigned = [color[v] for v in b]
        ones = assigned.count(1)
        if ones > 1:
            return False
        undecided = [v for v in b if color[v] == -1]
        if ones == 1:                                    # 나머지 전부 0
            saved = {}
            for v in undecided:
                saved[v] = color[v]; color[v] = 0
            ok = bt(bi + 1)
            if not ok:
                for v in undecided:
                    color[v] = saved[v]
            return ok
        # ones==0: undecided 중 정확히 1개를 1 로 (0-과거배정과 무모순)
        if not undecided:
            return False                                 # 전부 0 인데 1 필요 → 실패
        for pick in undecided:
            saved = {v: color[v] for v in undecided}
            for v in undecided:
                color[v] = 0
            color[pick] = 1
            if bt(bi + 1):
                return True
            for v in undecided:
                color[v] = saved[v]
        return False
    return bt(0)


def main():
    quick = "--quick" in sys.argv
    R = {}

    R["count_18_vectors_9_bases"] = (len(VEC) == 18 and len(BASES) == 9
                                     and len(set(VEC)) == 18)
    R["bases_4_mutually_orthogonal"] = all(basis_orthogonal(b) for b in BASES)
    cnt = Counter(v for b in BASES for v in b)
    R["each_ray_in_exactly_2_bases"] = (len(cnt) == 18 and all(c == 2 for c in cnt.values()))

    # path A: parity certificate — Σ(basis당 1)=9 vs 2·Σc(v)=짝수
    total_over_bases = 9                                  # 각 basis 정확히 1
    R["parity_certificate_2k_eq_9"] = (total_over_bases % 2 == 1)   # 9 홀수, 2·Σc 짝수 → 모순
    R["incidence_forces_even_sum"] = all(c == 2 for c in cnt.values())  # 2·Σc = Σ_bases

    # path B: exhaustive/backtracking — 유효 coloring 부재
    R["no_valid_coloring_pathB"] = (not has_coloring(BASES))

    # teeth: (a) 8-basis 부분집합은 coloring 존재(자명-불가능 아님)
    sub_colorable = any(has_coloring([b for j, b in enumerate(BASES) if j != drop])
                        for drop in range(9))
    R["teeth_8basis_subset_colorable"] = sub_colorable
    # teeth (b): 실제 양자 사영자 직교 = 정수 내적 0 (근사 없음)
    R["teeth_integer_orthogonality_exact"] = all(
        dot(VEC[b[i]], VEC[b[j]]) == 0 for b in BASES for i in range(4) for j in range(i + 1, 4))

    ok = all(R.values())
    if not quick:
        print("Kochen-Specker 18-벡터 state-independent 맥락성 관측 (ray-coloring 불가, witness — seal 아님):",
              flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  18 벡터 ∈ {{0,±1}}⁴ · 9 basis(각 4-상호직교) · 각 ray 정확히 2 basis(Σ_basis=2·Σ_v c)",
              flush=True)
        print("  ★path A parity: Σ(basis당 1)=9(홀수) = 2·Σ_v c(v)(짝수) → 2k=9 정수 모순 = state-independent "
              "KS(비맥락 hidden-variable 불가). path B: 2^18 배정 백트래킹 → 유효 coloring 없음(독립 재확인).",
              flush=True)
        print("  ★정직: 관측=KS hypergraph 조합 불가능성 정수 certificate(no-go). Peres-Mermin(operator-product "
              "parity)·contextual fraction(정량)와 대상 상이(ray-coloring). 봉인 아님·신규 module 0·root 불변 sidecar.",
              flush=True)
    print(f"ks18_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
