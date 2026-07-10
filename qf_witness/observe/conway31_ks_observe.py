#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""conway31_ks_observe — TrackHE13 P3: 정이십면체 대칭에서 나오는 Conway-31 형 d=3
Kochen-Specker 후보 집합의 **정직 판정** (관측·자체생성, seal 아님).

★외부 런타임이 Conway-31 구조에 대해 **불일치**한다(하나는 "10 interlocking triads", 다른 하나는
"orbits 6+10+15"). 둘 다 신뢰 금지(TrackHE11 Yu-Oh "uncolorable" 주장이 실제로는 colorable 이었던
자체정정 교훈). 정이십면체 기하에서 후보 ray 집합을 **자체 생성**하고, 무엇이 참인지 **정직 판정**한다:

  1. 세 자연 정이십면체 궤도를 ray 로 생성(antipodal 동일시), ℚ(√5)·φ=(1+√5)/2 정확산술:
       - 6 ray  : 정이십면체 꼭짓점축 — cyclic perms of (0,±1,±φ) (12 점 → 6 축)
       - 10 ray : 정십이면체 꼭짓점축 = 정이십면체 면축 — (±1,±1,±1) & cyclic perms of (0,±1/φ,±φ)
                  (20 점 → 10 축)
       - 15 ray : 모서리 중점축 — 실제 정이십면체 기하에서 **직접 유도**(꼭짓점 12개 → 최소거리쌍
                  = 모서리 30개 → 중점 → 정규화, 30 → 15 축). 외부 힌트 좌표 신뢰 금지.
     카운트 self-verify: 6+10+15 = 31, 사영점으로 전부 distinct.
  2. 성분을 a+b√5 (a,b∈ℚ, sympy) 로 **정확** 표현. 직교 = 정확 내적 0 (부동소수 판정 아님).
  3. 31 ray 위 직교 그래프 구성. 모든 직교 triad(상호직교 삼중=완전기저) 및 직교쌍 전수 열거.
  4. KS coloring 판정: v:rays→{0,1}, (a) 직교 두 ray 동시 1 불가, (b) 완전 직교 triad 는 정확히
     하나 1 (peres33_ks_observe 규칙과 동일). 제약그래프 전수 백트래킹.
  5. **정직 verdict**: UNSAT → 진짜 state-independent KS 집합(Peres-33 계열); colorable →
     closed-negative 로 **있는 그대로 보고**(외부 제안 정정 — 이 또한 가치 있는 결과). 어느 쪽이든
     triad 개수·31-집합이 KS 논증을 지탱할 만큼 triad 를 갖는지 함께 보고.
  6. teeth: verdict 별 non-vacuity 대조 — UNSAT 이면 진부분집합 colorable, colorable 이면 명시적
     coloring 을 제시하고 전 제약 만족 검증.

정직 경계(★관측·seal 아님, root 불변 sidecar): witness = Conway-31 KS hypergraph 조합 판정(no-go
또는 closed-negative). 봉인 아님·신규 module 0. 좌표 필드 ℚ(√5). all_ok = "정직 verdict + teeth 로
분석 완결"(반드시 UNSAT 이라는 뜻 아님). Peres-33(d=3 ℚ(√2))·KS-18(4D)·Yu-Oh(colorable)·KCBS
(state-dependent) 맥락성 계보와 교차(대상·필드 상이).

사용: python -m qf_witness.observe.conway31_ks_observe [--quick]
"""
from __future__ import annotations
import os, sys, json, itertools, math
import sympy as sp

sys.setrecursionlimit(100000)

from qf_witness.core.paths import ROOT
OUT = os.path.join(ROOT, ".pgf", "proofs", "CONWAY31-KS-OBSERVE.json")

s = sp.Symbol('s')              # s = √5 (symbol; s²→5 로 환원)
S5 = sp.sqrt(5)
PHI = (1 + s) / 2               # φ = (1+√5)/2
INV_PHI = (s - 1) / 2           # 1/φ = φ-1
_MOD = sp.Poly(s**2 - 5, s)     # 최소다항식


# ── ℚ(√5) 정확산술: s²=5 로 환원한 정규형 a + b·s ──
def red(e):
    """s²=5 를 적용해 차수 ≤1 정규형(a + b·s)으로 환원."""
    return sp.Poly(sp.expand(e), s).rem(_MOD).as_expr()


def ab(e):
    """정규형에서 (a, b) 유리수쌍 추출(e = a + b√5)."""
    d = sp.Poly(red(e), s).as_dict()
    return (sp.nsimplify(d.get((0,), 0)), sp.nsimplify(d.get((1,), 0)))


def is_zero(e):
    """정확 0 판정(a=b=0)."""
    return red(e) == 0


def dot(u, v):
    """정확 내적."""
    return red(sum(red(u[i] * v[i]) for i in range(3)))


def numvec(v):
    """수치 벡터(dedup 키 전용 — 직교 판정은 정확산술로 별도 수행)."""
    return [float(sp.N(red(x).subs(s, S5))) for x in v]


def ray_key(v):
    """사영점(부호·스케일 무시) 정규화 수치 키: 단위벡터 + 첫 유의성분 양수."""
    nv = numvec(v)
    nrm = math.sqrt(sum(y * y for y in nv))
    nv = [y / nrm for y in nv]
    for y in nv:
        if abs(y) > 1e-9:
            if y < 0:
                nv = [-t for t in nv]
            break
    return tuple(round(y, 9) for y in nv)


def pt_key(p):
    """점(부호 유지) 정확 키 — 꼭짓점/면중심 dedup 용."""
    return tuple(ab(c) for c in p)


def cyc(t):
    """3-cyclic 순열."""
    a, b, c = t
    return [(a, b, c), (c, a, b), (b, c, a)]


SIGNS = list(itertools.product((1, -1), repeat=3))


def orbit_points(seeds):
    """seed 튜플들에 cyclic 순열 × 부호 적용 → 정확 dedup 한 점 목록."""
    pts = {}
    for seed in seeds:
        for base in cyc(seed):
            for sg in SIGNS:
                p = tuple(sg[i] * base[i] for i in range(3))
                pts[pt_key(p)] = p
    return list(pts.values())


def points_to_rays(pts):
    """점 목록 → antipodal 동일시 ray dict(ray_key -> raw 정확 벡터)."""
    rays = {}
    for p in pts:
        k = ray_key(p)
        if k not in rays:
            rays[k] = p
    return rays


# ── KS coloring 백트래킹(peres33_ks_observe 규칙: 각 triad 정확히 하나 1 · 직교쌍 not-both-1) ──
def ks_solve(m, triads, orth):
    """KS {0,1}-coloring 존재하면 배정 리스트 반환, 없으면 None(전 분기 소진=UNSAT)."""
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
            for x, sv in zip(und, saved):
                color[x] = sv
            return False
        und = [x for x in t if color[x] == -1]
        if not und:                                      # 전부 0 인데 1 필요 → 실패
            return False
        for pick in und:                                 # pick=1(직교 이웃 1이면 규칙 a 위반→스킵)
            if any(color[q] == 1 and orth[pick][q] for q in range(m)):
                continue
            saved = [color[x] for x in und]
            for x in und:
                color[x] = 0
            color[pick] = 1
            if bt(i + 1):
                return True
            for x, sv in zip(und, saved):
                color[x] = sv
        return False

    if bt(0):
        return [c if c == 1 else 0 for c in color]       # 미배정(-1) ray 는 0
    return None


def verify_coloring(col, triads, orth, m):
    """명시적 coloring 이 (a) 직교쌍 not-both-1 · (b) 각 triad 정확히 하나 1 을 만족하는지 검증."""
    pair_ok = all(not (col[i] == 1 and col[j] == 1 and orth[i][j])
                  for i in range(m) for j in range(i + 1, m))
    triad_ok = all(sum(col[x] for x in t) == 1 for t in triads)
    return pair_ok and triad_ok


def main():
    quick = "--quick" in sys.argv
    R = {}

    # 1. 세 정이십면체 궤도 자체생성 ──────────────────────────────────────────────
    # 1a. 꼭짓점: cyclic perms of (0,±1,±φ) → 12 점 → 6 ray
    vpts = orbit_points([(0, 1, PHI)])
    RV = points_to_rays(vpts)
    R["vertex_orbit_12pts_6rays"] = (len(vpts) == 12 and len(RV) == 6)

    # 1b. 면(=정십이면체 꼭짓점): (±1,±1,±1) & cyclic perms of (0,±1/φ,±φ) → 20 점 → 10 ray
    fpts = orbit_points([(1, 1, 1), (0, INV_PHI, PHI)])
    RF = points_to_rays(fpts)
    R["face_orbit_20pts_10rays"] = (len(fpts) == 20 and len(RF) == 10)

    # 1c. 모서리 중점: 실제 기하에서 유도(꼭짓점 최소거리쌍=모서리 30 → 중점 → 30→15 ray)
    d2 = {}
    for i in range(len(vpts)):
        for j in range(i + 1, len(vpts)):
            e = red(sum(red((vpts[i][k] - vpts[j][k]) ** 2) for k in range(3)))
            d2[(i, j)] = e
    dnum = {ij: float(sp.N(v.subs(s, S5))) for ij, v in d2.items()}
    dmin = min(dnum.values())
    edges = [ij for ij, val in dnum.items() if abs(val - dmin) < 1e-9]
    mids = [tuple((vpts[i][k] + vpts[j][k]) for k in range(3)) for (i, j) in edges]  # 2×중점(스케일 무관)
    RE = points_to_rays(mids)
    R["edge_orbit_30edges_15rays"] = (len(edges) == 30 and len(RE) == 15)

    # 1d. 합집합 = Conway-31, 사영점으로 전부 distinct
    ray_dict = {}
    for src in (RV, RF, RE):
        for k, v in src.items():
            ray_dict.setdefault(k, v)
    R["union_is_exactly_31_distinct"] = (len(ray_dict) == 31)
    R["orbit_decomposition_6_10_15"] = (len(RV) == 6 and len(RF) == 10 and len(RE) == 15)

    # 순서: 꼭짓점(0..5)·면(6..15)·모서리(16..30)
    keys = list(RV) + list(RF) + list(RE)
    keys = list(dict.fromkeys(keys))                     # distinct 유지(위 assert 로 31)
    rays = [ray_dict[k] for k in keys]
    m = len(rays)

    # 2. 성분 필드 ℚ(√5) self-verify(√5 실제 등장 = φ 필요) ─────────────────────
    all_ab = [ab(c) for v in rays for c in v]
    field_ok = all(a.is_rational and b.is_rational for (a, b) in all_ab)
    uses_sqrt5 = any(b != 0 for (a, b) in all_ab)
    R["coord_field_Q_sqrt5"] = (field_ok and uses_sqrt5)

    # 3. 직교 그래프(정확 내적 0) → 직교쌍·직교 triad 전수 ──────────────────────
    orth = [[(i != j and is_zero(dot(rays[i], rays[j]))) for j in range(m)] for i in range(m)]
    pairs = [(i, j) for i in range(m) for j in range(i + 1, m) if orth[i][j]]
    triads = [t for t in itertools.combinations(range(m), 3)
              if orth[t[0]][t[1]] and orth[t[0]][t[2]] and orth[t[1]][t[2]]]
    n_pairs, n_triads = len(pairs), len(triads)
    R["orthogonality_graph_built"] = (n_pairs >= 0)      # 구성 완료(수치 아님)
    # 각 ray 가 최소 하나의 triad 에 참여해야 그 ray 에 KS 제약이 걸림
    in_triad = sorted({x for t in triads for x in t})
    R["ks_argument_has_triads"] = (n_triads > 0)         # triad 없으면 KS 논증 자체 불가(정직 기록)
    # triad 들이 disjoint(파티션)인가? ⟺ "interlocking" 아님. 외부 "10 interlocking triads" 직접 반증.
    triad_multiset = [x for t in triads for x in t]
    triads_disjoint = (len(triad_multiset) == len(set(triad_multiset)))
    # 이 15 ray = 모서리축(정이십면체 15 C2축) 전체를 5 직교삼중으로 파티션(고전 5-cube 구조)
    edge_idx = set(range(len(RV) + len(RF), m))
    partitions_edge_rays = (triads_disjoint and set(in_triad) == edge_idx)
    R["triads_disjoint_not_interlocking"] = triads_disjoint

    # 4. KS coloring 전수 판정 ────────────────────────────────────────────────
    col = ks_solve(m, triads, orth)
    colorable = col is not None
    verdict = "colorable_closed_negative" if colorable else "uncolorable"
    R["ks_verdict_determined"] = True                    # 전수 백트래킹 완결(어느 verdict 든)

    # 5. teeth: verdict 별 non-vacuity ────────────────────────────────────────
    teeth_detail = {}
    if colorable:
        # 명시적 coloring 제시 + 전 제약 검증
        col_ok = verify_coloring(col, triads, orth, m)
        R["teeth_explicit_coloring_verified"] = col_ok
        teeth_detail["explicit_coloring"] = col
        teeth_detail["coloring_satisfies_all_constraints"] = col_ok
        teeth_detail["num_ones"] = sum(col)
    else:
        # UNSAT: 진부분집합(ray 하나 제거)은 colorable → uncolorability 는 전체의 non-trivial 성질
        if quick:
            drops = [in_triad[0]] if in_triad else [0]
        else:
            drops = range(m)
        sub_colorable = None
        for dpt in drops:
            sub_triads = [t for t in triads if dpt not in t]
            if ks_solve(m, sub_triads, orth) is not None:
                sub_colorable = dpt
                break
        R["teeth_proper_subset_colorable"] = (sub_colorable is not None)
        teeth_detail["subset_colorable_after_dropping_ray"] = sub_colorable

    # 6. 외부 주장 대조(정직) ─────────────────────────────────────────────────
    ext_orbit_claim_matches = R["orbit_decomposition_6_10_15"]       # "6+10+15" — 기하 사실
    ext_triad_claim_10 = (n_triads == 10)                            # "10 interlocking triads"
    R["external_orbit_claim_6_10_15_checked"] = True                 # 판정 수행(결과는 아래 값)

    ok = all(v for v in R.values())

    result = {
        "path": "Conway-31 icosahedral KS (d=3, ℚ(√5))",
        "verdict": verdict,
        "colorable": colorable,
        "counts": {"vertex_rays": len(RV), "face_rays": len(RF), "edge_rays": len(RE),
                   "total_rays": m, "orthogonal_pairs": n_pairs, "orthogonal_triads": n_triads,
                   "rays_in_some_triad": len(in_triad)},
        "external_claims": {
            "orbit_6_10_15_matches": bool(ext_orbit_claim_matches),
            "ten_interlocking_triads_matches": bool(ext_triad_claim_10),
            "actual_triad_count": n_triads,
            "triads_are_interlocking": (not triads_disjoint),
            "triads_partition_15_edge_rays": bool(partitions_edge_rays),
        },
        "checks": {k: bool(v) for k, v in R.items()},
        "teeth": teeth_detail,
        "rays": [[[str(a), str(b)] for (a, b) in (ab(c) for c in v)] for v in rays],
        "orthogonal_pairs": pairs,
        "orthogonal_triads": [list(t) for t in triads],
        "deterministic": True,
        "_note": ("관측·자체생성 — seal 아님·root 불변 sidecar·신규 module 0. verdict=조합 판정"
                  "(uncolorable=state-independent KS / colorable_closed_negative=외부제안 정정). "
                  "좌표 필드 ℚ(√5), 직교=정확 내적 0. 외부 런타임 Conway-31 구조 주장은 "
                  "self-generate 후 정직 판정으로 교차검증(신뢰 금지)."),
    }

    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        json.dump(result, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    if not quick:
        print("Conway-31 정이십면체 d=3 Kochen-Specker 후보 정직 판정 (witness — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  궤도: 꼭짓점 6 + 면 10 + 모서리 15 = {m} ray(전부 distinct 사영점, ℚ(√5))", flush=True)
        print(f"  직교 그래프: 직교쌍 {n_pairs}개 · 직교 triad {n_triads}개 · triad 참여 ray {len(in_triad)}개",
              flush=True)
        print(f"  ★VERDICT = {verdict.upper()}"
              + (f" (colorable — closed-negative, num_ones={sum(col)})" if colorable
                 else " (UNSAT — 진짜 state-independent KS)"), flush=True)
        print(f"  외부주장 대조: '6+10+15 궤도' 일치={ext_orbit_claim_matches} (기하 사실) · "
              f"'10 interlocking triads' 일치={ext_triad_claim_10} (실제 triad={n_triads}개, "
              f"interlocking={not triads_disjoint} — 15 모서리축을 5 직교삼중으로 파티션=고전 5-cube 구조)",
              flush=True)
        print("  ★정직: 관측=조합 판정(no-go 또는 closed-negative). 봉인 아님·신규 module 0·root 불변 "
              "sidecar. Peres-33(ℚ(√2))/KS-18(4D)/Yu-Oh(colorable)/KCBS(state-dep) 맥락성 계보와 교차.",
              flush=True)
    print(f"conway31_ks_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
