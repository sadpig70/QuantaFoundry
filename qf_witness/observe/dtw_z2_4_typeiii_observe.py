#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dtw_z2_4_typeiii_observe — TrackHE16 P2: D^ω(ℤ₂⁴) type-III — ★완전 비아벨화 불가
(closed-negative) + 부분 비아벨화 프로파일 (관측, seal 아님). 전 과정 정수/GF(2) 정확산술.

[[dtw_z2z2z2_typeiii_observe]](v15 P1, ℤ₂³ **부분** 비아벨화·radical 1차원)의 ℤ₂⁴ 확장. report16
6/8 런타임이 "ℤ₂⁴ type-III **완전** 비아벨화(radical=0)"를 제안했다. 본 witness 는 선검증으로
그 주장을 **반증**한다(§4′o: 외부 수치 자체 재유도가 실제 오류를 잡는다).

★핵심 관측 1 — 완전 비아벨화 **불가**(closed-negative, agent 제안 반증):
  type-III 3-cocycle ω(a,b,c)=Σ_{i<j<k} c_{ijk}·a_i b_j c_k 의 slant β_a 의 commutator
  bilinear form B_a(h,k)=β_a(h,k)−β_a(k,h) 는 **rank ≤ 2**(전 삼중항 basis 조합 2⁴−1=15 ×
  전 a≠0 15 = 전수 실측). ⟹ 모든 a 에서 radical dim = 4−rank ≥ 2 → 사영 irrep 차원
  d_a = 2^{rank/2} ≤ 2 → **d=4(완전 비아벨화) 절대 불가**. v15 agent08 경고("radical=0 전제는
  cocycle 선택 의존")가 옳았고, ℤ₂⁴ 에서도 **부분**(radical≥2)만 가능함을 상한 증명.
  구조 이유: a 고정 시 type-III 삼중항 a_i b_j c_k 는 (j,k) 두 변수만 pairing → 각 삼중항 rank≤2,
  조합해도 상한 유지(실측).

★핵심 관측 2 — H³ 계수군 정정(§4′o·§5, agent "ℤ₂¹⁴" 반증):
  dim H³(ℤ₂⁴,**μ₂**) = **20**(= 𝔽₂[x₁..x₄] degree-3 단항식 수 C(6,3), 자체 유도) ≠ agent 주장
  "ℤ₂¹⁴"(= H³(ℤ₂⁴,**U(1)**) 의 2-torsion 계수 오적용). v15 P2·P4 에 이은 세 번째 계수군 함정 검출.

★positive — 부분 비아벨화 프로파일(ℤ₂³ v15 대비 확장):
  최대 twist cocycle(4 삼중항 전부)에서 rank-2 섹터 수·d=2 anyon 수·anyon 총수·차원분포 산출.
  v15 ℤ₂³(22 anyon·d=2 섹터 7·D²=64) → ℤ₂⁴(D²=256) 로 확장, 여전히 부분(d≤2).

관측 계층 (전부 exact ℤ/GF(2)):
  1. dim H³(ℤ₂⁴,μ₂)=20 자체유도(GF(2) cochain rank).
  2. type-III cocycle 전수(15 조합) cocycle identity 16⁴ 확인 + slant B_a rank 전수(≤2 상한).
  3. ★anyon 프로파일: a=0(16 pointed)·a≠0(rank별 사영 irrep 차원·개수)·Σd²=256.
  4. ★대조: ℤ₂³(v15) vs ℤ₂⁴ — 둘 다 부분(radical≥1)·d 상한 2. 완전(d=4) 불가 공통.
  teeth: (i) rank-4 alternating form 은 **존재**(symplectic J) 하나 type-III slant 로는 안 나옴 —
     slant 제약이 rank≤2 원인 실증 (ii) 가짜 cocycle 검출 (iii) coboundary 양성대조.

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - closed-negative(완전 비아벨화 불가)는 **type-III cocycle 부분류 한정** 상한 — 임의 μ₂ 3-cocycle
    전체(dim 20)에 대한 불가능성은 무주장(type-III basis 조합만 전수). 비-type-III(type-I/II)는
    pointed 또는 부분.
  - anyon 차원 exact(정수)·완전 modular data S/T·구체 스핀은 미착수(v15 P1 스코프 상속·ζ₈ 경계).
  - μ₂ 계수만(≠U(1)) — 자체 유도. 범주 동치 무주장.

사용: python -m qf_witness.observe.dtw_z2_4_typeiii_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import itertools
from collections import Counter

N = 4                       # ℤ₂⁴
NG = 1 << N                 # 16
TRIPLES = list(itertools.combinations(range(N), 3))   # 4개: type-III basis


def bit(g, i):
    return (g >> (N - 1 - i)) & 1


def omega(triple_mask):
    """삼중항 조합(비트마스크) → ω(a,b,c) 지수 함수."""
    active = [TRIPLES[t] for t in range(len(TRIPLES)) if (triple_mask >> t) & 1]

    def w(a, b, c):
        s = 0
        for (i, j, k) in active:
            s ^= bit(a, i) & bit(b, j) & bit(c, k)
        return s & 1
    return w


def is_cocycle(w):
    for a, b, c, d in itertools.product(range(NG), repeat=4):
        if (w(b, c, d) ^ w(a ^ b, c, d) ^ w(a, b ^ c, d) ^ w(a, b, c ^ d) ^ w(a, b, c)):
            return False
    return True


def slant(w, a):
    return lambda h, k: (w(a, h, k) ^ w(h, k, a) ^ w(h, a, k)) & 1


def comm_form_rank(w, a):
    """B_a(h,k)=β_a(h,k)−β_a(k,h) 의 GF(2) rank (4×4 alternating, 기저 2^i)."""
    beta = slant(w, a)
    M = [[(beta(1 << (N - 1 - i), 1 << (N - 1 - j)) ^ beta(1 << (N - 1 - j), 1 << (N - 1 - i)))
          for j in range(N)] for i in range(N)]
    rows = [sum(M[i][j] << j for j in range(N)) for i in range(N)]
    basis = []
    for r in rows:
        for b in basis:
            r = min(r, r ^ b)
        if r:
            basis.append(r); basis.sort(reverse=True)
    return len(basis)


# ── GF(2) cochain (H³ 차원 자체유도) ──────────────────────────────────────
def gf2_rank(rows):
    b = []
    for r in rows:
        for x in b:
            r = min(r, r ^ x)
        if r:
            b.append(r); b.sort(reverse=True)
    return len(b)


def _i3(a, b, c):
    return (a * NG + b) * NG + c


def h3_mu2_dim():
    d2 = [(1 << (b * NG + c)) ^ (1 << ((a ^ b) * NG + c))
          ^ (1 << (a * NG + (b ^ c))) ^ (1 << (a * NG + b))
          for a in range(NG) for b in range(NG) for c in range(NG)]
    d3 = []
    for a, b, c, d in itertools.product(range(NG), repeat=4):
        d3.append((1 << _i3(b, c, d)) ^ (1 << _i3(a ^ b, c, d)) ^ (1 << _i3(a, b ^ c, d))
                  ^ (1 << _i3(a, b, c ^ d)) ^ (1 << _i3(a, b, c)))
    r2, r3 = gf2_rank(d2), gf2_rank(d3)
    return (NG ** 3 - r3) - r2


def anyon_profile(w):
    """cocycle w → anyon 프로파일: 각 a 의 rank·radical·사영 irrep(차원 d=2^{r/2}·개수 2^{N−r/2})."""
    dims = []
    rank_counts = Counter()
    for a in range(NG):
        if a == 0:
            r = 0
        else:
            r = comm_form_rank(w, a)
        assert r % 2 == 0, ("alternating rank 홀수", a, r)
        d = 1 << (r // 2)                       # 사영 irrep 차원 = 2^{rank/2}
        m = 1 << (N - r)                        # 개수 = |radical| = 2^{N−rank}
        assert d * d * m == NG, (a, r, d, m)    # Σ d²·개수 = 2^r·2^{N−r} = 2^N = |G|
        dims += [d] * m
        rank_counts[r] += 1
    return dims, dict(rank_counts)


def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "dtw-z2-4-typeiii/v1",
           "_note": ("D^ω(ℤ₂⁴) type-III — ★완전 비아벨화 불가(closed-negative, agent 제안 반증) + "
                     "부분 비아벨화 프로파일(관측·seal 아님·신규 module 0·root 불변). "
                     "★H³(μ₂)=20≠agent 'ℤ₂¹⁴'(U(1) 오적용)·slant rank≤2 상한. μ₂ 계수만.")}

    # 1. H³ 계수군 자체유도 (agent "14" 반증) — full 전용(16³ cochain rank 무거움)
    if not quick:
        h3 = h3_mu2_dim()
        out["dim_H3_mu2"] = h3
        R["H3_mu2_is_20"] = (h3 == 20)
        R["H3_mu2_not_14"] = (h3 != 14)     # agent "ℤ₂¹⁴" = U(1) 계수 오적용
        out["coefficient_group_correction"] = {
            "self_derived_mu2": h3,
            "agent_claim_U1_14": 14,
            "note": "H³(ℤ₂⁴,μ₂)=20=𝔽₂[x₁..x₄] degree-3 단항식 C(6,3) vs H³(ℤ₂⁴,U(1)) 2-torsion=14. "
                    "v15 P2/P4 에 이은 세 번째 계수군 함정 검출(§4′o).",
        }
    else:
        h3 = None

    # 2. ★closed-negative: slant B_a rank ≤ 2 전수 (완전 비아벨화 불가)
    max_rank_overall = 0
    all_ranks = {}
    combos = range(1, 1 << len(TRIPLES)) if not quick else [0b1111, 0b0001, 0b0011]
    cocycle_all_ok = True
    for tm in combos:
        w = omega(tm)
        if not is_cocycle(w):
            cocycle_all_ok = False
            continue
        rks = [comm_form_rank(w, a) for a in range(1, NG)]
        mr = max(rks)
        max_rank_overall = max(max_rank_overall, mr)
        all_ranks[tm] = mr
    R["typeIII_cocycle_all_ok"] = cocycle_all_ok
    R["slant_rank_le_2_all"] = (max_rank_overall <= 2)      # ★핵심 상한
    R["radical_ge_2_always"] = (max_rank_overall <= 2)      # radical = 4−rank ≥ 2
    R["full_nonabelianization_impossible"] = (max_rank_overall < 4)   # d=4 불가
    out["closed_negative"] = {
        "claim_refuted": "D^ω(ℤ₂⁴) type-III 완전 비아벨화(radical=0·d=4)",
        "max_slant_commutator_rank": max_rank_overall,
        "verdict": ("type-III slant B_a rank ≤ 2 (전 삼중항 조합·전 a 전수) → radical ≥ 2 → "
                    "d_a ≤ 2 → 완전 비아벨화 불가. ★부분(v15 ℤ₂³)만 ℤ₂⁴ 에서도 가능."),
        "scope": "type-III cocycle basis 조합 한정(임의 μ₂ 3-cocycle 전체 무주장)",
    }

    # 3. ★positive: 최대 twist 부분 비아벨화 프로파일
    w_max = omega(0b1111)                    # 4 삼중항 전부
    dims, rank_counts = anyon_profile(w_max)
    out["partial_profile_maximal_twist"] = {
        "anyon_count": len(dims), "D2": sum(d * d for d in dims),
        "dim_distribution": dict(Counter(sorted(dims))),
        "rank_counts_over_a": rank_counts,
        "note": "d 상한 2(부분 비아벨화) — 완전(d=4) 부재 확인",
    }
    R["D2_256"] = (sum(d * d for d in dims) == NG * NG)
    R["dim_upper_bound_2"] = (max(dims) <= 2)              # 완전 비아벨화면 d=4 등장
    R["has_d2_anyons"] = (dims.count(2) > 0)               # 부분 비아벨화는 발생

    # 4. teeth
    #   (i) rank-4 alternating form 은 존재(symplectic) 하나 type-III slant 아님
    def symplectic_rank():
        # J = e0∧e1 + e2∧e3 (non-degenerate) → rank 4
        M = [[0] * N for _ in range(N)]
        M[0][1] = M[1][0] = 1
        M[2][3] = M[3][2] = 1
        rows = [sum(M[i][j] << j for j in range(N)) for i in range(N)]
        basis = []
        for r in rows:
            for b in basis:
                r = min(r, r ^ b)
            if r:
                basis.append(r); basis.sort(reverse=True)
        return len(basis)
    R["teeth_rank4_form_exists"] = (symplectic_rank() == 4 and max_rank_overall < 4)
    #   (ii) 가짜 cocycle 검출
    R["teeth_fake_cocycle"] = not is_cocycle(
        lambda a, b, c: 1 if (a, b, c) == (1, 1, 1) else 0)
    #   (iii) coboundary 양성대조 (μ(a,b)=a₀b₁b₂ 의 dμ → 전 a radical 전체=rank 0)
    mu = [[bit(a, 0) & bit(b, 1) & bit(b, 2) for b in range(NG)] for a in range(NG)]
    wcb = (lambda a, b, c: (mu[b][c] ^ mu[a ^ b][c] ^ mu[a][b ^ c] ^ mu[a][b]) & 1)
    R["teeth_coboundary_is_cocycle"] = is_cocycle(wcb)
    R["teeth_coboundary_rank0"] = (max(comm_form_rank(wcb, a) for a in range(1, NG)) == 0)

    ok = bool(all(R.values()))
    out["checks"] = R
    out["comparison_z2n"] = {
        "z2_3_v15": {"anyon": 22, "D2": 64, "d2_sectors": 7, "radical": "1(부분)"},
        "z2_4_this": {"anyon": len(dims), "D2": 256,
                      "d2_count": dims.count(2), "radical": "≥2(부분·완전 불가)"},
        "共通": "type-III 는 부분 비아벨화만 — 완전(radical=0·d 최대) 불가 상한",
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "DTW-Z2-4-TYPEIII.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("D^ω(ℤ₂⁴) type-III 관측 (closed-negative + 부분 프로파일 — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        if h3 is not None:
            print(f"  ★H³(μ₂)={h3} (agent 'ℤ₂¹⁴'=U(1) 오적용 반증)", flush=True)
        print(f"  ★slant B_a max rank={max_rank_overall}(≤2) → 완전 비아벨화 불가·radical≥2", flush=True)
        print(f"  ★부분 프로파일(최대 twist): {out['partial_profile_maximal_twist']['anyon_count']} anyon·"
              f"D²={out['partial_profile_maximal_twist']['D2']}·차원 "
              f"{out['partial_profile_maximal_twist']['dim_distribution']}", flush=True)
        print("  → .pgf/proofs/DTW-Z2-4-TYPEIII.json", flush=True)
    print(f"dtw_z2_4_typeiii_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
