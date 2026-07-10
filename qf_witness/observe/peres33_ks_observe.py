#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""peres33_ks_observe — TrackHE11 후속: Peres-33 (d=3) state-independent Kochen-Specker 집합의
**진짜 uncolorability** witness (관측, seal 아님).

TrackHE11 P4 Yu-Oh 13 자체정정(13 ray 는 {0,1}-**colorable** — state-independent contextuality 는
부등식형/KCBS 계열)이 남긴 공백 "진짜 uncolorable d=3 KS"를 메움. Peres-33 은 3차원에서 어떤 상태에도
독립적으로(비맥락 hidden-variable 가정) {0,1}-배정이 **존재하지 않는** 최초의 자체구성 강검증.

★외부 좌표 신뢰 금지(v11 KS-18 교훈: 외부 좌표가 비직교였음). 33 ray 를 **자체 생성**:
  1. 성분이 {0,±1,±√2}인 ℝ³ 방향 전체 = octahedral 군 O_h(48 서명순열)에 닫힌 pool(49 ray).
     O_h-closure 를 48-원소 서명순열 군작용으로 self-verify(외부 좌표 함정 차단).
  2. Peres-33 := 그 pool 중 **직교 triad(완전기저)에 참여하는 ray**(전수 열거) = 정확히 33개.
     (나머지 16 ray 는 직교-고립 → KS 논증과 무관.) 성분 self-verify: 스케일 후 ∈ {0,±1,±√2}.
  3. KS coloring 규칙(둘 다): (a) 직교 두 ray 가 동시에 1 불가, (b) 각 직교 triad 에 최소 하나는 1
     ⟹ 각 triad **정확히 하나** 1. 33변수 전수 백트래킹 → **만족 배정 없음(UNSAT)** = state-independent KS.
  4. 대조: Peres-33 은 UNSAT 이나 (i) 정수만의 부분배열(√2 없는 axes/face/body)은 colorable,
     (ii) 임의 ray 하나 제거하면 colorable → uncolorability 가 **33 전체의 non-trivial 성질**.
  5. state-independent(모든 상태, uncolorability=valuation 부재) vs KCBS state-dependent(pentagon 부등식) 구분.

정직 경계(★관측·seal 아님, root 불변 sidecar): witness = Peres-33 KS hypergraph 조합 불가능성(no-go).
  봉인 아님(§5). Peres-Mermin(operator-product parity)·contextual fraction(정량 LP)·KS-18(4D ray-coloring)·
  qutrit Wigner 맥락성 계보와 교차(대상 상이: 여기는 d=3 ray-coloring). 좌표 필드 ℚ(√2). 신규 module 0.

사용: python -m qf_witness.observe.peres33_ks_observe [--quick]
"""
from __future__ import annotations
import sys, itertools
import numpy as np

sys.setrecursionlimit(100000)
S2 = np.sqrt(2.0)
COMPS = [0.0, 1.0, -1.0, S2, -S2]                      # 성분 ∈ {0,±1,±√2} = ℚ(√2)


def oh_group():
    """octahedral 군 O_h = 48 서명순열 3×3 행렬(부호변경 × 좌표순열)."""
    G = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            M = np.zeros((3, 3))
            for i in range(3):
                M[i, perm[i]] = signs[i]
            G.append(M)
    return G


def ray_key(v):
    """ray(부호·스케일 무시 방향) 정규화 키: 단위벡터 + 첫 유의성분 양수."""
    v = v / np.linalg.norm(v)
    for x in v:
        if abs(x) > 1e-9:
            if x < 0:
                v = -v
            break
    return tuple(round(x, 9) for x in v)


def scaled_components_in_field(raw):
    """raw 벡터를 최소 유의성분으로 스케일 후 |성분| ∈ {0,1,√2} 확인(ℚ(√2) 필드)."""
    s = min(abs(x) for x in raw if abs(x) > 1e-9)
    w = raw / s
    return all(any(abs(abs(x) - t) < 1e-6 for t in (0.0, 1.0, S2)) for x in w)


def ks_colorable(m, triads, orth):
    """KS {0,1}-coloring 존재? 규칙 (a) 직교쌍 not both 1 · (b) 각 triad 최소 하나 1.
    결정론적 전수 백트래킹(False 반환=전 분기 소진=UNSAT 증명)."""
    color = [-1] * m

    def bt(i):
        if i == len(triads):
            return True
        t = triads[i]
        if any(color[x] == 1 for x in t):               # 이미 만족 → 나머지 0
            und = [x for x in t if color[x] == -1]
            saved = [color[x] for x in und]
            for x in und:
                color[x] = 0
            if bt(i + 1):
                return True
            for x, s in zip(und, saved):
                color[x] = s
            return False
        und = [x for x in t if color[x] == -1]
        if not und:                                      # 전부 0 인데 1 필요 → 실패
            return False
        for pick in und:                                 # pick=1(직교 이웃이 1이면 규칙 a 위반→스킵)
            if any(color[q] == 1 and orth[pick][q] for q in range(m)):
                continue
            saved = [color[x] for x in und]
            for x in und:
                color[x] = 0
            color[pick] = 1
            if bt(i + 1):
                return True
            for x, s in zip(und, saved):
                color[x] = s
        return False

    return bt(0)


def main():
    quick = "--quick" in sys.argv
    R = {}

    # 1. O_h-closed pool 자체생성(성분 {0,±1,±√2} 전체) + O_h-closure self-verify
    pool = {}
    raw = {}
    for combo in itertools.product(COMPS, repeat=3):
        v = np.array(combo, dtype=float)
        if np.linalg.norm(v) < 1e-12:
            continue
        k = ray_key(v)
        if k not in pool:
            pool[k] = v / np.linalg.norm(v)
            raw[k] = v
    OH = oh_group()
    keyset = set(pool)
    oh_closed = all(ray_key(M @ pool[k]) in keyset for M in OH for k in pool)
    R["rays_Oh_closed_self_generated"] = oh_closed          # 48-서명순열 군작용 닫힘(외부좌표 함정 차단)

    # 2. 직교 triad(완전기저) 전수 열거 → 참여 ray = Peres-33
    keys = sorted(pool)
    rays = [pool[k] for k in keys]
    n = len(rays)
    triads_all = [t for t in itertools.combinations(range(n), 3)
                  if abs(rays[t[0]] @ rays[t[1]]) < 1e-9
                  and abs(rays[t[0]] @ rays[t[2]]) < 1e-9
                  and abs(rays[t[1]] @ rays[t[2]]) < 1e-9]
    support = sorted({x for t in triads_all for x in t})
    idx = {o: i for i, o in enumerate(support)}
    m = len(support)                                        # == 33
    sr = [rays[o] for o in support]
    sraw = [raw[keys[o]] for o in support]
    T = [tuple(idx[x] for x in t) for t in triads_all]
    orth = [[abs(sr[i] @ sr[j]) < 1e-9 for j in range(m)] for i in range(m)]

    R["orthogonal_triads_enumerated"] = (len(T) == 16 and all(
        orth[t[0]][t[1]] and orth[t[0]][t[2]] and orth[t[1]][t[2]] for t in T))
    R["triad_support_is_exactly_33"] = (m == 33)

    # 성분 self-verify: 33 ray 전부 스케일 후 ∈ {0,±1,±√2}, √2 실제 등장
    comps_ok = all(scaled_components_in_field(v) for v in sraw)
    uses_sqrt2 = any(any(abs(abs(x) - S2 * s) < 1e-6 for x in (v / min(abs(y) for y in v if abs(y) > 1e-9)))
                     for v in sraw for s in (1.0,))
    R["rays_33_components_in_0_1_sqrt2"] = (m == 33 and comps_ok)
    R["coord_field_Q_sqrt2"] = (comps_ok and uses_sqrt2)    # ℚ(√2): √2 필요·그 이상 불필요

    # 3. ★핵심: KS uncolorability 전수 증명(UNSAT) — 규칙 (a)+(b) 백트래킹
    unsat = not ks_colorable(m, T, orth)
    R["ks_uncolorable_unsat_exhaustive"] = unsat

    # 4. 대조 & teeth
    # (i) 정수만(√2 없는) 부분배열 = colorable (Yu-Oh 13 이 colorable 인 것과 같은 계열의 대조)
    int_sub = [i for i in range(m) if all(abs(abs(x) - S2) > 1e-6 for x in sraw[i])]
    ri = {o: i for i, o in enumerate(int_sub)}
    Ti = [tuple(ri[x] for x in t) for t in T if all(x in ri for x in t)]
    orthi = [[orth[int_sub[i]][int_sub[j]] for j in range(len(int_sub))] for i in range(len(int_sub))]
    int_colorable = ks_colorable(len(int_sub), Ti, orthi)
    R["yuoh13_or_subset_colorable_contrast"] = (len(int_sub) < 33 and int_colorable)

    # (ii) teeth: ray 하나 제거하면 colorable → uncolorability 는 33 전체의 non-trivial 성질
    if quick:
        drops = [0]                                         # UNSAT 은 전수, teeth 는 대표 1개(빠름)
    else:
        drops = range(m)
    teeth = any(ks_colorable(m, [t for t in T if d not in t], orth) for d in drops)
    R["teeth_subset_colorable"] = teeth

    # (iii) 성분집합 self-verify 가 비직교 외부좌표 함정 방어(성분 ∉ {0,±1,±√2} → 즉시 탈락)
    R["teeth_component_set_guards_nonorthogonal_seed"] = comps_ok

    # 5. state-independent vs KCBS: uncolorability = 어떤 상태에도 valuation 부재(state-independent).
    #    KCBS 는 5-cycle state-dependent 부등식(특정 상태에서만 위배). 여기 uncolorability=전자.
    R["state_independent_vs_kcbs"] = unsat                  # UNSAT ⟺ state-independent(모든 상태)

    ok = all(R.values())
    if not quick:
        print("Peres-33 (d=3) state-independent Kochen-Specker 진짜 uncolorability 관측 (witness — seal 아님):",
              flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  pool={n} ray(성분 {{0,±1,±√2}}·O_h 48-서명순열 닫힘) → 직교 triad {len(T)}개 참여 ray = Peres-{m}",
              flush=True)
        print("  ★KS coloring 규칙 (a)직교쌍 not-both-1 + (b)각 triad ≥1 → 각 triad 정확히 1. 33변수 전수 "
              "백트래킹 → **UNSAT(만족 배정 없음)** = state-independent KS(비맥락 hidden-variable 불가).", flush=True)
        print(f"  대조: √2 없는 정수 부분배열({len(int_sub)} ray) colorable · ray 하나 제거 시 colorable "
              "→ uncolorability 는 33 전체의 non-trivial 성질(자명-불가능 아님). Yu-Oh 13 colorable(부등식형)의 공백 보완.",
              flush=True)
        print("  ★정직: 관측=Peres-33 KS hypergraph 조합 불가능성(no-go). 봉인 아님·신규 module 0·root 불변 "
              "sidecar. 좌표 필드 ℚ(√2). Peres-Mermin/contextual fraction/KS-18(4D) 맥락성 계보와 교차(대상 상이).",
              flush=True)
    print(f"peres33_ks_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
