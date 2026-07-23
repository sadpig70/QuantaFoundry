#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dtw_d4_u1_census_observe — TrackHE18: D^ω(D₄) **U(1) 완전 census** — H³(D₄,U(1)) 전체에서
anyon 수 22 고정 ⟹ "22→19→16 ω-가변" **완전 반증** (관측, seal 아님).
[[dtw_d4_full_modular_observe]] 의 "μ₂ 계수 한정" 정직 경계를 해소하는 완결편.

방법(★Bockstein lift 사다리): U(1)-값 3-cocycle 은 |G|=8-torsion(transfer 표준정리)이므로
**μ₈-값 cocycle 로 전 클래스 실현 가능**. μ₂→μ₄→μ₈ 을 Bockstein 장애물 사다리로 오른다:
  ω₄ = w + 2u (dω₄≡0 mod4 ⟺ d³u ≡ (d³w)/2 mod2, 해 존재 ⟺ 1차 Bockstein 소멸)
  ω₈ = ω₄ + 4v (해 존재 ⟺ 2차 Bockstein 소멸)
lift 의 코셋 구조 ω + 2·Z³(μ₂)(각 단계)가 상위 계수 클래스 전체를 전사적으로 커버 → census 완전.

관측 6축(전부 exact: GF(2)/ℤ₄/ℤ₈ 정수 산술):
  A. **1차 Bockstein census**: 16 μ₂-클래스 중 **{0,3,5,6}만 μ₄-lift 가능**(부분군: 3⊕5=6) —
     12 클래스는 Bockstein≠0(lift 불가·order-2 로 고정).
  B. **μ₄-slant 관례 기계확정**: θ_a(x,y)=n(a,x,y)+n(x,y,a^{xy})−n(x,a^x,y) mod4 — μ₂ 에선 부호
     무관했으나 μ₄ 에선 유의: **product-flux variant a 만** 대수 결합법칙 64³ 전수 통과(b 반증).
  C. ★**μ₄ 완전 census(64 조합)**: {w∈{0,3,5,6}}×{2z: 16 μ₂-대표} = 4-torsion 클래스 전사 커버 —
     **전부 22 anyons**([5,4,5,4,4]).
  D. ★**μ₈ 완전 census(128 조합)**: 2차 Bockstein 은 64 μ₄-조합 중 **8개만** lift 허용(56 장애) —
     lift 의 μ₈-코셋 128 조합 **전부 22 anyons**. ⟹ **H³(D₄,U(1)) 전체에서 anyon 수 22 고정**
     = report17/18 "anyon 22→19→16 ω-가변" **완전 반증**(계수 제한 없음).
  E. ★**r-sector P-census**: P=Σθ_r(r,r^k) mod8 ∈ **{0,2,4,6}** — P=4 는 λ⁴=−1(ζ₈ spins,
     [[dtw_d4_full_modular_observe]] 관측), **P=2,6 은 λ⁴=±i → spins ζ₁₆ 필요**(μ₄-twist 의
     새 위상 — 완전 S·T 의 ζ₁₆ 구현은 다음).
  F. **교차 정합**: μ₂ census(이전 모듈 16 클래스 22 고정)와 부분 census 로 정합.

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - census 완전성 = (i) H³ 이 8-torsion(transfer 표준정리, 유일한 외부 사실)·(ii) lift 코셋
    구조의 전사성(자체 논증) — 개별 U(1)-클래스 라벨링(어느 조합=어느 클래스·중복도)은 무주장.
  - anyon 수 는 U(1)-클래스 불변량(β-regular 판정은 β 의 코호몰로지류만 의존) — census 값 신뢰 근거.
  - ζ₁₆-spins 는 **필요조건 관측**(P-값) — 완전 twisted S·T ζ₁₆ 산술 구현=다음.

사용: python -m qf_witness.observe.dtw_d4_u1_census_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import itertools


def mul(x, y):
    i, j = x % 4, x // 4
    k, l = y % 4, y // 4
    return ((i + (k if j == 0 else -k)) % 4) + 4 * ((j + l) % 2)


E = 0
INV = [0] * 8
for _x in range(8):
    for _y in range(8):
        if mul(_x, _y) == E:
            INV[_x] = _y


def conj(g, x):
    return mul(mul(x, g), INV[x])


CENT = {g: [x for x in range(8) if mul(x, g) == mul(g, x)] for g in range(8)}
CLASS_REPS = [0, 1, 2, 4, 5]
NE = [g for g in range(8) if g != E]


def compute_h3_basis():
    tri_idx = {}
    for t in itertools.product(NE, repeat=3):
        tri_idx[t] = len(tri_idx)
    rows = []
    for g1, g2, g3, g4 in itertools.product(NE, repeat=4):
        r = 0
        for t in [(g2, g3, g4), (mul(g1, g2), g3, g4), (g1, mul(g2, g3), g4),
                  (g1, g2, mul(g3, g4)), (g1, g2, g3)]:
            p = tri_idx.get(t)
            if p is not None:
                r ^= (1 << p)
        if r:
            rows.append(r)
    img_vecs = []
    for (b1, b2) in itertools.product(NE, repeat=2):
        v = 0
        for g1, g2, g3 in itertools.product(NE, repeat=3):
            s = 0
            for t in [(g2, g3), (mul(g1, g2), g3), (g1, mul(g2, g3)), (g1, g2)]:
                if t == (b1, b2):
                    s ^= 1
            if s:
                v ^= (1 << tri_idx[(g1, g2, g3)])
        img_vecs.append(v)

    def gf2_basis(vecs):
        b = []
        for r in vecs:
            for x in b:
                r = min(r, r ^ x)
            if r:
                b.append(r)
                b.sort(reverse=True)
        return b

    piv = {}
    for r in rows:
        while r:
            p = r.bit_length() - 1
            if p in piv:
                r ^= piv[p]
            else:
                piv[p] = r
                break
    cols = sorted(piv, reverse=True)
    for p in cols:
        r = piv[p]
        for p2 in cols:
            if p2 > p and ((piv[p2] >> p) & 1):
                piv[p2] ^= r
    pivset = set(piv)
    ker = []
    for f in range(343):
        if f in pivset:
            continue
        v = 1 << f
        for p, r in piv.items():
            if (r >> f) & 1:
                v |= (1 << p)
        ker.append(v)
    b3 = gf2_basis(img_vecs)

    def reduce_by(v, basis):
        for b in basis:
            v = min(v, v ^ b)
        return v

    h3basis = []
    ext = list(b3)
    for v in ker:
        w = reduce_by(v, ext)
        if w:
            h3basis.append(v)
            ext.append(w)
            ext.sort(reverse=True)
        if len(h3basis) == 4:
            break
    return tri_idx, rows, h3basis


def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "dtw-d4-u1-census/v1",
           "_note": ("D^ω(D₄) U(1) 완전 census — Bockstein μ₂→μ₄→μ₈ lift 사다리·전 조합 anyon 22 "
                     "고정 ⟹ '22→19→16 ω-가변' 완전 반증. 관측·seal 아님·module 0·root 불변. "
                     "ζ₁₆-spins 필요조건 발견(완전 S·T ζ₁₆=다음).")}

    tri_idx, rows, h3basis = compute_h3_basis()
    R["H3_dim4"] = (len(h3basis) == 4)
    TRIS = list(tri_idx.keys())
    QUADS = list(itertools.product(NE, repeat=4))
    quad_idx = {q: i for i, q in enumerate(QUADS)}
    h3reps = []
    for mask in range(16):
        v = 0
        for k in range(4):
            if (mask >> k) & 1:
                v ^= h3basis[k]
        h3reps.append(v)

    def nval(W, t, mod):
        g1, g2, g3 = t
        if g1 == E or g2 == E or g3 == E:
            return 0
        return W[tri_idx[(g1, g2, g3)]] % mod

    def d3_val(W, quad, mod):
        g1, g2, g3, g4 = quad
        return (nval(W, (g2, g3, g4), mod) - nval(W, (mul(g1, g2), g3, g4), mod)
                + nval(W, (g1, mul(g2, g3), g4), mod) - nval(W, (g1, g2, mul(g3, g4)), mod)
                + nval(W, (g1, g2, g3), mod)) % mod

    col_img = []
    for t in TRIS:
        W = [0] * 343
        W[tri_idx[t]] = 1
        img = 0
        for q in QUADS:
            if d3_val(W, q, 2) == 1:
                img |= (1 << quad_idx[q])
        col_img.append(img)

    # GF(2) solve 준비(기저 1회 구축)
    basis = []
    for ci, cvec in enumerate(col_img):
        v = cvec
        comb = 1 << ci
        for (bv, bc) in basis:
            top = bv.bit_length() - 1
            if (v >> top) & 1:
                v ^= bv
                comb ^= bc
        if v:
            basis.append((v, comb))
            basis.sort(key=lambda p: -p[0].bit_length())

    def gf2_solve(target):
        v = target
        comb = 0
        for (bv, bc) in basis:
            top = bv.bit_length() - 1
            if (v >> top) & 1:
                v ^= bv
                comb ^= bc
        return comb if v == 0 else None

    # ── A. 1차 Bockstein census ───────────────────────────────────────────
    lifts = {}
    for mask in range(16):
        wbits = h3reps[mask]
        W = [(wbits >> i) & 1 for i in range(343)]
        c = 0
        for q in QUADS:
            d = d3_val(W, q, 4)
            if d == 2:
                c |= (1 << quad_idx[q])
        if c == 0:
            lifts[mask] = 0
            continue
        sol = gf2_solve(c)
        if sol is None:
            lifts[mask] = None
        else:
            u = 0
            for ci in range(343):
                if (sol >> ci) & 1:
                    u |= (1 << tri_idx[TRIS[ci]])
            lifts[mask] = u
    liftable = sorted(m for m, u in lifts.items() if u is not None)
    R["A_liftable_0356"] = (liftable == [0, 3, 5, 6])
    R["A_12_obstructed"] = (sum(1 for u in lifts.values() if u is None) == 12)
    R["A_subgroup"] = (3 in liftable and 5 in liftable and 6 in liftable)   # 3⊕5=6
    out["bockstein1"] = {"liftable_mu2_classes": liftable,
                        "obstructed": 12, "note": "부분군 구조 {0,3,5,6} (3⊕5=6)"}

    # ── B. slant 관례 (μ₄) ────────────────────────────────────────────────
    def make_slant(W, mod):
        def th(a, x, y):
            def nv(t):
                g1, g2, g3 = t
                if g1 == E or g2 == E or g3 == E:
                    return 0
                return W[tri_idx[(g1, g2, g3)]]
            return (nv((a, x, y)) + nv((x, y, conj(a, INV[mul(x, y)])))
                    - nv((x, conj(a, INV[x]), y))) % mod
        return th

    def assoc(W, mod, variant, sub=False):
        th = make_slant(W, mod)

        def prod(a, x, b, y):
            if a != conj(b, x):
                return None
            t = th(a, x, y) if variant == "a" else th(b, x, y)
            return (t, a, mul(x, y))
        rng = range(0, 8, 2) if sub else range(8)
        for a, x in itertools.product(range(8), repeat=2):
            for b, y in itertools.product(range(8), repeat=2):
                p1 = prod(a, x, b, y)
                for c, z in itertools.product(rng, repeat=2):
                    p2 = prod(b, y, c, z)
                    lhs = None
                    if p1 is not None:
                        s1, aa, xy = p1
                        q = prod(aa, xy, c, z)
                        if q is not None:
                            lhs = ((s1 + q[0]) % mod, q[1], q[2])
                    rhs = None
                    if p2 is not None:
                        s2, bb, yz = p2
                        q = prod(a, x, bb, yz)
                        if q is not None:
                            rhs = ((s2 + q[0]) % mod, q[1], q[2])
                    if lhs != rhs:
                        return False
        return True

    w3 = h3reps[3]
    u3 = lifts[3]
    W43 = [((w3 >> i) & 1) + 2 * ((u3 >> i) & 1) for i in range(343)]
    R["B_assoc_variant_a"] = assoc(W43, 4, "a", sub=quick)
    R["B_assoc_variant_b_fails"] = (not assoc(W43, 4, "b", sub=False))

    # ── C/D. census ───────────────────────────────────────────────────────
    def counts(W, mod):
        th = make_slant(W, mod)
        parts = []
        for a in CLASS_REPS:
            C = CENT[a]
            beta = {(x, y): th(a, x, y) for x in C for y in C}

            def breg(g):
                return all(beta[(g, h)] == beta[(h, g)] for h in C
                           if mul(g, h) == mul(h, g))
            cls, sn = [], set()
            for g in C:
                if g in sn:
                    continue
                cc = sorted({conj(g, x) for x in C})
                cls.append(cc)
                sn |= set(cc)
            parts.append(sum(1 for cc in cls if breg(cc[0])))
        return parts

    mu4_counts = []
    mu4_combos = []
    for wm in liftable:
        wbits = h3reps[wm]
        u0 = lifts[wm]
        for z4 in range(16):
            ub = u0 ^ h3reps[z4]
            W4 = [((wbits >> i) & 1) + 2 * ((ub >> i) & 1) for i in range(343)]
            mu4_counts.append(sum(counts(W4, 4)))
            mu4_combos.append((wm, z4, W4))
    R["C_mu4_64_combos"] = (len(mu4_counts) == 64)
    R["C_mu4_all_22"] = all(c == 22 for c in mu4_counts)

    mu8_counts = []
    Pvals = set()
    lift8_fail = 0
    if not quick:
        for (wm, z4, W4) in mu4_combos:
            c4 = 0
            ok = True
            for q in QUADS:
                d = d3_val(W4, q, 8)
                if d % 4 != 0:
                    ok = False
                    break
                if d == 4:
                    c4 |= (1 << quad_idx[q])
            if not ok:
                lift8_fail += 1
                continue
            sol = gf2_solve(c4)
            if sol is None:
                lift8_fail += 1
                continue
            v0 = 0
            for ci in range(343):
                if (sol >> ci) & 1:
                    v0 |= (1 << tri_idx[TRIS[ci]])
            for z8 in range(16):
                vb = v0 ^ h3reps[z8]
                W8 = [W4[i] + 4 * ((vb >> i) & 1) for i in range(343)]
                mu8_counts.append(sum(counts(W8, 8)))
                th = make_slant(W8, 8)
                Pvals.add((th(1, 1, 1) + th(1, 1, 2) + th(1, 1, 3)) % 8)
        R["D_mu8_second_bockstein_8_64"] = (64 - lift8_fail == 8)
        R["D_mu8_128_combos"] = (len(mu8_counts) == 128)
        R["D_mu8_all_22"] = all(c == 22 for c in mu8_counts)
        # E. r-sector P census
        R["E_P_census_0246"] = (Pvals == {0, 2, 4, 6})
        R["E_zeta16_needed"] = (2 in Pvals or 6 in Pvals)
        out["mu8"] = {"second_bockstein_pass": 64 - lift8_fail, "census_combos": len(mu8_counts),
                      "all_22": all(c == 22 for c in mu8_counts)}
        out["r_sector_P"] = {"values_mod8": sorted(Pvals),
                             "zeta8_case": "P=4 → λ⁴=−1 (dtw_d4_full_modular 관측)",
                             "zeta16_case": "★P=2,6 → λ⁴=±i → spins ζ₁₆ 필요(μ₄-twist 새 위상)"}
    out["census"] = {
        "mu2_prior": "16 클래스 전부 22 (dtw_d4_full_modular_observe)",
        "mu4": {"combos": len(mu4_counts), "all_22": all(c == 22 for c in mu4_counts)},
        "verdict": ("★H³(D₄,U(1)) 전체(8-torsion, transfer 표준정리)에서 anyon 수 22 고정 — "
                    "report17/18 '22→19→16 ω-가변' 완전 반증(계수 제한 없음)"),
    }

    # teeth
    R["teeth_bockstein_obstruction_real"] = R["A_12_obstructed"]
    R["teeth_convention_pinned"] = R["B_assoc_variant_b_fails"]
    R["teeth_census_complete"] = R["C_mu4_all_22"]

    ok = bool(all(v for v in R.values()))
    out["checks"] = R
    out["scope_honesty"] = {
        "delivered": "U(1) 완전 census(μ₂ 16·μ₄ 64·μ₈ 128 전 조합 22) — 완전 반증·μ₂-한정 경계 해소",
        "external_fact": "H³(G,U(1))=|G|-torsion (transfer 표준정리) — census 완전성의 유일 외부 사실",
        "no_claim": "개별 U(1)-클래스 라벨링(조합↔클래스 대응·중복도) 무주장",
        "next": "ζ₁₆ spins 의 완전 twisted S·T(μ₄-twist·ζ₁₆ 산술) — P=2,6 필요조건 관측까지",
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "DTW-D4-U1-CENSUS.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("D^ω(D₄) U(1) 완전 census (Bockstein 사다리 — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  ★μ₂ 16·μ₄ 64·μ₈ 128 조합 전부 anyon 22 — U(1) 전체 완전 반증", flush=True)
        print("  ★1차 Bockstein {0,3,5,6}만 lift·2차 8/64·★P=2,6 → spins ζ₁₆ 필요", flush=True)
        print("  → .pgf/proofs/DTW-D4-U1-CENSUS.json", flush=True)
    print(f"dtw_d4_u1_census_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
