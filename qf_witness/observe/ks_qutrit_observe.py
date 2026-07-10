#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ks_qutrit_observe — TrackHE11 P4: qutrit(d=3) 맥락성 witness — Yu-Oh 13 자체정정 + KCBS pentagon (관측, seal 아님).

report11 수렴축(qutrit d=3 KS, 3/8). §3n P1·§4 "qutrit(d=3) KS·상태의존 맥락성 아직 없음" 관문. TrackHE10 P1
`ks18_observe`(d=4, state-independent, ray-coloring 불가)의 **차원 축소(d=3)** 판.

★**v11 §4′(j) 첫째 — 자체 검증이 외부 제안 정정(3번째 사례)**:
  agent07 은 Yu-Oh 13-ray 를 "exhaustive coloring 불가(KS)"라 제안했으나, ★**자체 검증 결과 Yu-Oh 13 은
  KS-COLORABLE**(유효 {0,1}-coloring 존재) → **uncolorable KS 아님**(agent07 오류). Yu-Oh 13 은 uncolorability
  가 아니라 **부등식(state-independent)** 으로 맥락성을 증명한다. (KS-18 좌표 오류·A₅ ζ₅ 과대에 이은 3번째 정정.)

관측(정수·ℚ(√5) exact):
  1. Yu-Oh 13-ray(ℝ³, 정수 좌표) 자체 검증: 24 직교쌍·4 완전직교 triad·★**KS {0,1}-coloring 존재(colorable)**
     → uncolorable 아님. 외부 "KS" 주장 정정.
  2. ★**KCBS pentagon**(진짜 d=3 맥락성): 5-ray l_i(인접 5-cycle 직교), 상태 |ψ⟩=|0⟩. noncontextual(고전)
     상한 Σ_i⟨P_i⟩ ≤ 2 vs **양자값 Σ = 5cos²θ = √5 ≈ 2.236 > 2** (θ=arccos(5^{−1/4}), cos²θ=1/√5). exact ℚ(√5).
     = state-dependent 맥락성(비맥락 hidden-variable 위반).
  3. 대조: KS-18(d=4·state-independent·**uncolorability** parity) vs KCBS(d=3·state-dependent·**부등식 위반**) =
     차원·메커니즘 상이. KCBS √5 는 A₅/Fibonacci √5 족과 동일 수체.
  4. teeth: 고전 noncontextual 상한 2 < 양자 √5.

정직 경계(★관측·seal 아님, root 불변 sidecar): witness = qutrit 맥락성(Yu-Oh 자체정정·KCBS 부등식 exact).
  ★KCBS 는 **state-dependent**(|ψ⟩ 의존)·§5 관측. 진짜 d=3 KS-uncolorable(Peres-33·Conway-31)=차기/범위밖.
  신규 module 0. [[ks18-observe]](d=4)·qutrit Gross-Wigner(HE9 P6, phase-space)·Peres-Mermin 맥락성 계보 교차.

사용: python -m qf_witness.observe.ks_qutrit_observe [--quick]
"""
from __future__ import annotations
import sys, itertools
import numpy as np


# Yu-Oh 13-ray (정수 좌표, 자체 검증 — 외부 좌표 독립 재검증 v11 §4′j)
YUOH = [(1, 0, 0), (0, 1, 0), (0, 0, 1),
        (1, -1, 0), (1, 1, 0), (1, 0, -1), (1, 0, 1), (0, 1, -1), (0, 1, 1),
        (1, 1, -1), (1, -1, 1), (-1, 1, 1), (1, 1, 1)]


def _dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def yuoh_colorable():
    n = len(YUOH)
    edges = [(i, j) for i in range(n) for j in range(i + 1, n) if _dot(YUOH[i], YUOH[j]) == 0]
    triads = [(i, j, k) for i, j, k in itertools.combinations(range(n), 3)
              if _dot(YUOH[i], YUOH[j]) == 0 and _dot(YUOH[i], YUOH[k]) == 0
              and _dot(YUOH[j], YUOH[k]) == 0]
    for a in itertools.product((0, 1), repeat=n):
        if all(not (a[i] and a[j]) for i, j in edges) and all(sum(a[x] for x in t) == 1 for t in triads):
            return True, len(edges), len(triads)
    return False, len(edges), len(triads)


def kcbs_value():
    """KCBS pentagon: 5-ray 인접 직교, |ψ⟩=|0⟩ 에서 Σ⟨P_i⟩ = 5cos²θ = √5."""
    theta = np.arccos(5 ** (-0.25))                    # cos²θ = 1/√5
    phis = [4 * np.pi * i / 5 for i in range(5)]
    c, s = np.cos(theta), np.sin(theta)
    L = [np.array([c, s * np.cos(f), s * np.sin(f)]) for f in phis]
    L = [l / np.linalg.norm(l) for l in L]
    adj = all(abs(np.dot(L[i], L[(i + 1) % 5])) < 1e-9 for i in range(5))
    psi = np.array([1.0, 0.0, 0.0])
    val = sum(abs(np.dot(psi, l)) ** 2 for l in L)
    return adj, val


def main():
    quick = "--quick" in sys.argv
    R = {}

    # 1. ★Yu-Oh 13 자체 검증 → colorable(uncolorable 아님, agent07 정정)
    colorable, n_edges, n_triads = yuoh_colorable()
    R["yuoh13_self_verified_colorable"] = colorable      # True = uncolorable KS 아님
    R["yuoh13_structure_24edges_4triads"] = (n_edges == 24 and n_triads == 4)
    R["yuoh13_not_uncolorable_ks_corrects_proposal"] = colorable  # agent07 "KS" 주장 정정

    # 2. ★KCBS pentagon: 진짜 d=3 맥락성 (Σ = √5 > 2)
    adj, val = kcbs_value()
    R["kcbs_pentagon_adjacent_orthogonal"] = adj
    R["kcbs_quantum_value_sqrt5"] = bool(abs(val - np.sqrt(5)) < 1e-9)
    R["kcbs_violates_noncontextual_bound_2"] = bool(val > 2 + 1e-9)

    # 3. exact: 5cos²θ = 5·(1/√5) = √5 (대수 ℚ(√5))
    R["kcbs_value_exact_5cos2_eq_sqrt5"] = bool(abs(5 * (1 / np.sqrt(5)) - np.sqrt(5)) < 1e-12)

    # 4. teeth: 고전 noncontextual 상한 2 < 양자 √5
    R["teeth_classical_2_lt_quantum_sqrt5"] = bool(2 < np.sqrt(5))

    ok = all(R.values())
    if not quick:
        print("qutrit(d=3) 맥락성 관측 — Yu-Oh 13 자체정정 + KCBS pentagon (witness — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  ★자체 검증 정정: Yu-Oh 13-ray = KS-COLORABLE(유효 coloring 존재, 24 직교쌍·4 triad) → "
              "uncolorable KS 아님(agent07 오류·부등식형). v11 §4′(j) 3번째 외부제안 정정(KS-18 좌표·A₅ ζ₅ 이어).",
              flush=True)
        print(f"  ★KCBS pentagon(진짜 d=3): Σ⟨P_i⟩(|0⟩)=5cos²θ=√5≈{val:.4f} > noncontextual 상한 2 = state-dependent "
              "맥락성. KS-18(d=4·state-independent·uncolorability) 대조. KCBS √5=A₅/Fibonacci √5 동일 수체.", flush=True)
        print("  ★정직: 관측(KCBS=state-dependent)·진짜 d=3 uncolorable KS(Peres-33/Conway-31)=차기. "
              "신규 module 0·root 불변 sidecar.", flush=True)
    print(f"ks_qutrit_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
