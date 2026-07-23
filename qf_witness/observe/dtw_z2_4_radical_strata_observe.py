#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dtw_z2_4_radical_strata_observe — TrackHE17 P5: D^ω(ℤ₂⁴) radical 층화 —
radical∈{2,4} 완전 판정 (관측, seal 아님). [[dtw_z2_4_typeiii_observe]](v16 P2)의 확장.

v16 P2 는 type-III cocycle 로 **완전 비아벨화(radical=0) 불가**(slant commutator rank ≤ 2)를
상한 증명했다. report17 은 (a) radical=1 부분류(agent06/08)와 (b) radical=0 금지(agent04)를
제안했다. 본 witness 는 **전 H³(ℤ₂⁴,μ₂) 층화**로 둘 다 정직 판정한다:

관측 4축(전부 GF(2)/정수 산술):
  A. **★radical=1 원리적 불가 (parity 정리)**: commutator form B_a 는 GF(2) **alternating** →
     rank 는 **항상 짝수** (전 type-III cocycle 15 × 전 flux a≠0 15 전수 실측 rank∈{0,2}).
     ⟹ radical = 4 − rank 도 **항상 짝수** ⟹ **radical ∈ {0,2,4}, radical=1(및 3) 불가**.
     (agent06-P2/08-HM6.2 의 "radical=1 부분류" 제안 반증 — 홀수 radical 은 존재할 수 없다.)
  B. **radical=0 불가 (rank≤2, 전 cocycle)**: max rank = 2 전수 확인(v16 재확인) ⟹ radical ≥ 2.
     구조 이유: a 고정 시 type-III 삼중항 a_i b_j c_k 는 (j,k) 2변수만 pairing → 각 rank≤2.
  C. **★type-I/II 는 commutator 무기여 (radical=0 전 H³ 반증)**: type-II cocycle(x_i x_j², i≠j)은
     is_cocycle 이나 comm_form rank ≡ 0 (전 a). 비아벨화(commutator)의 **유일 원천 = type-III**.
     ⟹ dim H³=20(type-I 4 + type-II 12 + type-III 4) 전체에서도 radical=0 불가(type-III rank≤2).
  D. **★GL(4,𝔽₂) 단일 궤도 (균일 층화)**: type-III 공간 = Λ³(V*) ≅ V (V=𝔽₂⁴) → GL(4,2)가 15 비영
     원소에 **transitive** ⟹ **단일 궤도(크기 15)**. 15 cocycle 전부 **동일 radical 프로파일**
     {radical=2: 14 flux, radical=4: 1 flux} 실측(단일triple ≡ all-4). ⟹ 층화는 궤도-불변.
  ★**완전 층화**: radical ∈ {2, 4} 정확. 최대 비아벨화 = radical 2(사영 irrep 차원 2^{rank/2}=2).

  teeth: (i) rank-4 alternating(symplectic J) 은 **존재**하나 type-III slant 로 도달 불가 —
     slant 제약이 rank≤2 원인 (ii) type-II cocycle rank=0 대조 (iii) coboundary(자명) rank 0.

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - 판정은 **GF(2) 선형대수 전수**(alternating rank·radical) — 봉인 아님. 완전 twisted S 미착수(별도).
  - dim H³(ℤ₂⁴,μ₂)=20 자체유도(μ₂ 계수 ≠ U(1) ℤ₂¹⁴ 함정, v16 재확인).
  - radical=1 불가는 **parity 정리**(alternating rank 짝수)·radical=0 불가는 **rank≤2 전수**(type-III
    유일 원천). GL(4,2) 단일궤도는 Λ³V*≅V(표현론) + 프로파일 균일 실측.

사용: python -m qf_witness.observe.dtw_z2_4_radical_strata_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import itertools
from collections import Counter

# v16 P2 기계 재사용(단일출처)
from qf_witness.observe.dtw_z2_4_typeiii_observe import (
    N, NG, TRIPLES, omega, is_cocycle, comm_form_rank, h3_mu2_dim, bit)


def omega_type2(i, j):
    """type-II cochain ω(a,b,c) = a_i·b_j·c_j (i≠j) — commutator 무기여 대조용."""
    def w(a, b, c):
        return (bit(a, i) & bit(b, j) & bit(c, j)) & 1
    return w


def radical_profile(mask):
    """cocycle(triple mask) → flux a≠0 별 radical(=N−rank) 다중집합."""
    w = omega(mask)
    return tuple(sorted(N - comm_form_rank(w, a) for a in range(1, NG)))


def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "dtw-z2-4-radical-strata/v1",
           "_note": ("D^ω(ℤ₂⁴) radical 층화 — 관측·seal 아님·신규 module 0·root 불변. "
                     "★radical=1 불가(parity: alternating rank 짝수)·radical=0 불가(rank≤2 전 cocycle·"
                     "type-III 유일 원천)·GL(4,2) 단일궤도(Λ³V*≅V). radical∈{2,4} 완전 층화.")}

    # ── 0. dim H³ 자체유도 ────────────────────────────────────────────────
    R["h3_mu2_dim_20"] = (h3_mu2_dim() == 20)          # μ₂ 계수 (≠U(1) 14 함정)
    R["type3_count_4"] = (len(TRIPLES) == 4)

    # ── A. radical=1 parity 정리 + B. rank≤2 (전 type-III × 전 flux) ──────
    all_even = True
    max_rank = 0
    strata = Counter()          # (triple수, radical) → flux 수
    rad_values = set()
    for mask in range(1, 16):   # 15 nonzero type-III cocycle
        w = omega(mask)
        assert is_cocycle(w), mask
        for a in range(1, NG):
            r = comm_form_rank(w, a)
            if r % 2:
                all_even = False
            max_rank = max(max_rank, r)
            rad = N - r
            rad_values.add(rad)
            strata[(bin(mask).count("1"), rad)] += 1
    R["A_rank_always_even"] = all_even                 # ★radical=1 불가 근거
    R["A_radical_never_odd"] = all(v % 2 == 0 for v in rad_values)   # radical ∈ {2,4} 짝수만
    R["A_radical1_impossible"] = (1 not in rad_values and 3 not in rad_values)
    R["B_max_rank_2"] = (max_rank == 2)                # radical ≥ 2 ⟹ radical=0 불가
    R["B_radical0_impossible"] = (0 not in rad_values)
    R["radical_values_are_2_4"] = (rad_values == {2, 4})
    out["stratification"] = {
        "radical_values": sorted(rad_values),
        "max_comm_rank": max_rank,
        "by_(triples,radical)": {f"{t},{r}": n for (t, r), n in sorted(strata.items())},
        "verdict": "radical ∈ {2,4} 정확 — radical=0(rank≤2)·radical=1(parity) 둘 다 불가",
    }

    # ── C. type-I/II commutator 무기여 (radical=0 전 H³ 반증) ─────────────
    wII = omega_type2(0, 1)
    R["C_type2_is_cocycle"] = is_cocycle(wII)
    R["C_type2_comm_rank_zero"] = all(comm_form_rank(wII, a) == 0 for a in range(1, NG))
    # 여러 type-II 조합 확인
    R["C_type2_all_zero"] = all(
        all(comm_form_rank(omega_type2(i, j), a) == 0 for a in range(1, NG))
        for i in range(N) for j in range(N) if i != j)
    out["type2_contribution"] = {
        "model": "ω(a,b,c)=a_i b_j c_j (type-II, i≠j)",
        "comm_form_rank": 0, "is_cocycle": True,
        "verdict": "★commutator 유일 원천 = type-III → dim H³=20 전체에서도 radical=0 불가",
    }

    # ── D. GL(4,2) 단일 궤도 (균일 층화) ──────────────────────────────────
    profiles = {mask: radical_profile(mask) for mask in range(1, 16)}
    uniq = set(profiles.values())
    R["D_all15_same_profile"] = (len(uniq) == 1)       # ★단일 궤도 증거
    ref = Counter(profiles[1])
    R["D_profile_14x2_1x4"] = (ref == Counter({2: 14, 4: 1}))
    R["D_single_eq_all4"] = (Counter(profiles[1]) == Counter(profiles[15]))
    out["gl42_orbit"] = {
        "type3_space": "Λ³(V*) ≅ V (V=𝔽₂⁴) → GL(4,2) transitive on 15 nonzero",
        "distinct_radical_profiles": len(uniq),
        "uniform_profile": {"radical=2": 14, "radical=4": 1},
        "verdict": "★단일 궤도(크기 15) — 단일 삼중항 ≡ 4-삼중항(균일 층화)",
    }

    # ── teeth ─────────────────────────────────────────────────────────────
    # (i) rank-4 symplectic 존재(J=x0∧x1+x2∧x3) 하나 type-III slant 로는 max 2
    #   존재성: 4×4 alternating full-rank 행렬이 있음을 명시(GF(2) rank 4)
    def gf2_rank_mat(rows):
        b = []
        for r in rows:
            for x in b:
                r = min(r, r ^ x)
            if r:
                b.append(r); b.sort(reverse=True)
        return len(b)
    J = [0b0100, 0b1000, 0b0001, 0b0010]      # symplectic J (0∧1)+(2∧3), alternating rank 4
    R["teeth_symplectic_rank4_exists"] = (gf2_rank_mat(J) == 4 and max_rank == 2)
    # (ii) type-II rank 0 대조 (이미 C)
    R["teeth_type2_contrast"] = (max_rank == 2 and all(comm_form_rank(wII, a) == 0 for a in range(1, NG)))
    # (iii) coboundary(자명 cocycle mask=0) → 전 rank 0
    R["teeth_trivial_rank0"] = all(comm_form_rank(omega(0), a) == 0 for a in range(1, NG))

    ok = bool(all(R.values()))
    out["checks"] = R
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "DTW-Z2-4-RADICAL-STRATA.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("D^ω(ℤ₂⁴) radical 층화 관측 (GF(2) 전수 — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  ★radical ∈ {sorted(rad_values)} 정확 (radical=0 rank≤2·radical=1 parity 둘 다 불가)", flush=True)
        print(f"  ★GL(4,2) 단일 궤도: 15 cocycle 동일 프로파일 {dict(ref)}", flush=True)
        print("  ★type-II commutator 0 → radical=0 전 H³(dim 20) 불가", flush=True)
        print("  → .pgf/proofs/DTW-Z2-4-RADICAL-STRATA.json", flush=True)
    print(f"dtw_z2_4_radical_strata_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
