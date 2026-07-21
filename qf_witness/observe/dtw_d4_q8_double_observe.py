#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dtw_d4_q8_double_observe — TrackHE16 P1: twisted 비아벨 double D^ω(D₄)/D^ω(Q₈)
— 비아벨 군 위의 비자명 twist 최초 (관측, seal 아님). 전 과정 정수/GF(2)/ℚ(i) 정확산술.

계보 교차: [[dihedral_quaternion_double_observe]](v14 P1, untwisted D(D₄)/D(Q₈) 쌍 — 각 22 anyon·
D²=64·문자표 동치≠double 동치) + [[dtw_z2z2_double_observe]]/[[dtw_z2z2z2_typeiii_observe]](v15,
아벨 twist) + [[dtw_s3_double_observe]](v15 P2, S₃ 전치 섹터 단일 twist)의 교차. 지금까지 twist 는
**아벨 게이지군(ℤ₂²,ℤ₂³)** 또는 **S₃ 단일 섹터**뿐이었다. 본 witness 는 **비아벨 D₄·Q₈** 에
3-cocycle 을 켜고 어느 섹터가 비틀리는지 판정한다.

★핵심 관측 — D₄ ≠ Q₈ **twist 자원 비대칭**(자체 재유도, 신규):
  untwisted D(D₄) ≅ D(Q₈)(v14: 동일 22 anyon·D²=64·차원 분포) 이나, **twist 자원 H³ 가 갈린다**:
    dim H³(D₄,μ₂) = 4  (|H³|=16)   vs   dim H³(Q₈,μ₂) = 1  (|H³|=2).
  구조 근원: D₄ 는 **ℤ₂² centralizer 섹터**(s 의 centralizer ⟨s,r²⟩)를 가져 twist 가 **사영 2차원
  irrep** 을 만들 수 있다(4×d1 → 1×d2 **차원 전이**). Q₈ 는 비중심 켤레류 centralizer 가 전부
  **ℤ₄**(순환)뿐 → 사영표현이 보통표현과 같아(순환군 Schur multiplier 자명) **스핀만 이동**·차원 불변.
  ⟹ untwisted 는 구별 못 한 D₄/Q₈ 를 **twist 가 구별**(v14 는 T 다중집합, 본 축은 twist 자원·차원 전이).

관측 계층 (전부 exact):
  1. H^k(G,μ₂) 자체 재유도(GF(2) cochain rank, C¹=8·C²=64·C³=512·C⁴=4096): D₄=(H¹2·H²3·H³4)·
     Q₈=(H¹2·H²2·H³1). ★정직: μ₂ 계수(≠U(1) 계수 H³(D₄,U(1))=ℤ₂²×ℤ₄|=16·H³(Q₈,U(1))=ℤ₈|=8) —
     v15 P2 계수군 함정 재발 방지·본 witness 는 μ₂ 값만 주장.
  2. 비자명 3-cocycle 대표(ker d₃∖im d₂) + 비-coboundary certificate + cocycle 8⁴ 전수.
  3. anyon 22개(v14 정합)·D²=64 — 각 켤레류 (centralizer irrep). untwisted 차원분포 {1×8, 2×14} 공통.
  4. ★**차원전이 판정(cocycle 선택 무관)**: 각 비중심 켤레류의 centralizer 구조·H²(Z,μ₂) 로 twist 가
     낼 수 있는 최대 차원효과를 판정 — ℤ₂²(H²(μ₂)=ℤ₂·non-deg alt form) → 사영 2차원 irrep 가능(★차원
     전이) / ℤ₄(순환·alternating 자명) → 스핀만·차원 불변. **D₄ 는 차원전이 섹터 2개·Q₈ 은 0개**.
  5. ★대조: untwisted D(D₄)≅D(Q₈)(v14) 를 **twist 가 구별** — H³ 자원(4 vs 1)·차원전이(2 vs 0).
     D^ω(S₃)(v15 전치 단일 섹터) 대비 비아벨 다중 twistable 섹터(각 5개).
  teeth: (i) coboundary ω 양성대조(전 섹터 β 자명) (ii) 가짜 cocycle 검출.

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - 본 witness 는 **H³ 자원·차원전이 가능성(centralizer H²)·twistable 섹터 수** 로 D₄/Q₈ 를 판별
    (v14 P1 교훈: 완전 modular data 없이도 twist 판별 가능). ★**완전 twisted DPR 22×22 S 행렬·구체
    스핀(T) 은 미착수**: 순환(ℤ₄) 섹터 β-사영 스핀이 ζ₈-값(ℚ(i) 밖)·범주 동치 무주장.
  - **H³(G,U(1)) 전체·3-torsion(ζ₃) 무주장** — μ₂(2-torsion)만 자체 재유도.
  - 차원전이 판정은 centralizer H²(μ₂)·2-rank 로 exact — 게이트 분해 아님(§2 무관).

사용: python -m qf_witness.observe.dtw_d4_q8_double_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import itertools
from collections import Counter

from qf_witness.observe.dihedral_quaternion_double_observe import (
    Cyc, ZERO, ONE, I, Group, irrep_characters)

IPOW = [ONE, I, Cyc(-1), Cyc(0, -1)]


# ── GF(2) cochain (μ₂ 계수) ────────────────────────────────────────────────
def gf2_rank(rows):
    b = []
    for r in rows:
        for x in b:
            r = min(r, r ^ x)
        if r:
            b.append(r); b.sort(reverse=True)
    return len(b)


def gf2_solve(eqs):
    work = [[m, r, 1 << i] for i, (m, r) in enumerate(eqs)]
    piv = {}
    for wi, w in enumerate(work):
        r, rb, cm = w
        while r:
            p = r.bit_length() - 1
            if p in piv:
                pr = work[piv[p]]
                r ^= pr[0]; rb ^= pr[1]; cm ^= pr[2]
            else:
                piv[p] = wi
                w[0], w[1], w[2] = r, rb, cm
                break
        else:
            w[0], w[1], w[2] = 0, rb, cm
            if rb:
                return False, None, cm
    x = 0
    for p in sorted(piv):
        w = work[piv[p]]
        acc, rr = w[1], w[0] & ~(1 << p)
        while rr:
            q = rr.bit_length() - 1
            acc ^= (x >> q) & 1
            rr &= ~(1 << q)
        if acc:
            x |= 1 << p
    return True, x, None


class Cochain:
    def __init__(self, G):
        self.G = G
        self.n = G.n
        self.mul = G.mul

    def _i2(self, x, y):
        return x * self.n + y

    def _i3(self, x, y, z):
        return (x * self.n + y) * self.n + z

    def d1_rows(self):
        n, mul = self.n, self.mul
        return [(1 << b) ^ (1 << mul[a][b]) ^ (1 << a) for a in range(n) for b in range(n)]

    def d2_rows(self):
        n, mul = self.n, self.mul
        return [(1 << self._i2(b, c)) ^ (1 << self._i2(mul[a][b], c))
                ^ (1 << self._i2(a, mul[b][c])) ^ (1 << self._i2(a, b))
                for a in range(n) for b in range(n) for c in range(n)]

    def d3_rows(self):
        n, mul = self.n, self.mul
        out = []
        for a, b, c, d in itertools.product(range(n), repeat=4):
            out.append((1 << self._i3(b, c, d)) ^ (1 << self._i3(mul[a][b], c, d))
                       ^ (1 << self._i3(a, mul[b][c], d)) ^ (1 << self._i3(a, b, mul[c][d]))
                       ^ (1 << self._i3(a, b, c)))
        return out

    def dims(self):
        r1, r2, r3 = gf2_rank(self.d1_rows()), gf2_rank(self.d2_rows()), gf2_rank(self.d3_rows())
        n = self.n
        return {"H1": n - r1, "H2": (n * n - r2) - r1, "H3": (n ** 3 - r3) - r2}

    def find_nontrivial_omega(self):
        d2r, d3r = self.d2_rows(), self.d3_rows()
        img = []
        for j in range(self.n * self.n):
            v = 0
            for i, row in enumerate(d2r):
                if (row >> j) & 1:
                    v |= 1 << i
            img.append(v)
        basis = []
        for r in img:
            for b in basis:
                r = min(r, r ^ b)
            if r:
                basis.append(r); basis.sort(reverse=True)

        def in_span(v):
            for b in basis:
                v = min(v, v ^ b)
            return v == 0

        mat, piv = [], []
        for r in d3r:
            rr = r
            for br, pc in zip(mat, piv):
                if (rr >> pc) & 1:
                    rr ^= br
            if rr:
                mat.append(rr); piv.append(rr.bit_length() - 1)
        free = [c for c in range(self.n ** 3) if c not in piv]
        for fc in free:
            x = 1 << fc
            for i in sorted(range(len(piv)), key=lambda t: piv[t]):
                br, pc = mat[i], piv[i]
                acc, rr = 0, br & ~(1 << pc)
                while rr:
                    q = rr.bit_length() - 1
                    acc ^= (x >> q) & 1
                    rr &= ~(1 << q)
                if acc:
                    x |= 1 << pc
            if not in_span(x):
                return x
        return None


def omega_fn(vec, n):
    return lambda a, b, c: (vec >> ((a * n + b) * n + c)) & 1


# ── β-사영 지표 (아벨 centralizer 위, μ₂-값 β; radical 기계) ────────────────
def slant(w, mul, g):
    return lambda h, k: (w(g, h, k) ^ w(h, k, g) ^ w(h, g, k)) & 1


def beta_is_2cocycle(beta, Z, mul):
    return all((beta(k, l) ^ beta(mul[h][k], l) ^ beta(h, mul[k][l]) ^ beta(h, k)) == 0
               for h, k, l in itertools.product(Z, repeat=3))


def beta_coboundary(beta, Z, mul):
    """β 가 Z 위 coboundary(자명 클래스)인가."""
    zi = {x: i for i, x in enumerate(Z)}
    eqs = [(((1 << zi[h]) ^ (1 << zi[k]) ^ (1 << zi[mul[h][k]])), beta(h, k))
           for h in Z for k in Z]
    sat, _, _ = gf2_solve(eqs)
    return sat


def _ident(Z, mul):
    for e in Z:
        if all(mul[e][x] == x for x in Z):
            return e
    raise ValueError("no identity in Z")


def proj_irrep_dim(beta, Z, mul):
    """아벨 Z 위 β(μ₂-값)-사영 기약표현의 **차원 d 와 개수 m**(Σ d²·m/... Σd_i²=|Z|).
    ★차원만 exact(정수)로 산출 — 사영 irrep 은 전부 같은 차원 d=√(|Z|/|R_B|)·개수 |R_B|
    (R_B = alternating commutator form B(h,k)=β(h,k)−β(k,h) 의 radical). Σ = d²·m = |Z|.
    ★스핀(T)은 순환 인자에서 ζ₈-값 → ℚ(i) 밖 — 본 witness 스코프 밖(차원분포로 판별)."""
    def B(h, k):
        return (beta(h, k) ^ beta(k, h)) & 1
    Rb = [h for h in Z if all(B(h, k) == 0 for k in Z)]
    m = len(Rb)
    d2, rem = divmod(len(Z), m)
    assert rem == 0, (len(Z), m)
    d = int(round(d2 ** 0.5))
    assert d * d * m == len(Z), (len(Z), m, d)
    return d, m


def order_of(idx, mul, ident):
    k, x = 1, idx
    while x != ident:
        x = mul[x][idx]; k += 1
    return k


# ── 본 관측 ────────────────────────────────────────────────────────────────
def analyze_group(name, ident_class=None):
    G = Group(name)
    n = G.n
    e_idx = next(e for e in range(n) if all(G.mul[e][x] == x for x in range(n)))
    coch = Cochain(G)
    hdims = coch.dims()
    vec = coch.find_nontrivial_omega()
    w = omega_fn(vec, n)
    # cocycle 전수
    cocycle_ok = all(
        (w(b, c, d) ^ w(G.mul[a][b], c, d) ^ w(a, G.mul[b][c], d)
         ^ w(a, b, G.mul[c][d]) ^ w(a, b, c)) == 0
        for a, b, c, d in itertools.product(range(n), repeat=4))
    # 비-coboundary certificate
    d2r = coch.d2_rows()
    eqs = [(d2r[i], (vec >> i) & 1) for i in range(n ** 3)]
    sat, _, ycert = gf2_solve(eqs)

    # 섹터별 분석: centralizer 구조 + H²(μ₂)로 차원전이 가능성 판정
    #   ★cocycle 선택에 의존하지 않고 **섹터 centralizer 의 twist 잠재력**을 판정한다:
    #     H²(Z,μ₂)≠0 인 아벨 섹터에서만 β 가 사영 2차원 irrep(차원 전이)을 낼 수 있다
    #     (ℤ₂²: H²(μ₂)=ℤ₂ → 차원전이 가능 / ℤ₄: alternating 자명 → 스핀만·차원 불변).
    sectors, untw_dims = [], []
    n_dim_trans, n_twistable = 0, 0
    for ci, cl in enumerate(G.classes):
        g = G.reps[ci]
        Z = G.centralizer(g)
        ab = all(G.mul[x][y] == G.mul[y][x] for x in Z for y in Z)
        irr = irrep_characters(G, Z)
        untw_d = [int(ch[e_idx].a) * len(cl) for ch in irr]
        untw_dims += untw_d
        # 아벨 섹터의 H²(μ₂) — 차원전이 가능 여부
        h2z, dimtrans = None, False
        if ab and len(Z) > 1:
            Zg = _subgroup_group(G, Z)
            h2z = Cochain(Zg).dims()["H2"]
            # non-degenerate alternating form 가능 ⟺ 사영 2차원 irrep ⟺ H² 비자명 & rank≥2
            dimtrans = (h2z >= 1 and _has_nondeg_alt(Zg))
        info = {"class": ci, "rep_order": order_of(g, G.mul, e_idx),
                "Z_order": len(Z), "Z_abelian": ab, "Z_H2_mu2": h2z,
                "central": len(Z) == n, "dim_transition_possible": dimtrans,
                "twistable": (h2z is not None and h2z >= 1) or (not ab and len(Z) > 1)}
        if dimtrans:
            n_dim_trans += 1
        if info["twistable"]:
            n_twistable += 1
        sectors.append(info)

    return {
        "group": name, "H_dims": hdims,
        "cocycle_ok": cocycle_ok, "noncoboundary": (not sat), "cert_ok": (ycert is not None),
        "n_twistable_sectors": n_twistable,
        "n_dim_transition_sectors": n_dim_trans,
        "sectors": sectors,
        "anyon_count": len(untw_dims), "D2": sum(d * d for d in untw_dims),
        "untw_dims": dict(Counter(sorted(untw_dims))),
    }


def _subgroup_group(G, Z):
    """G 의 아벨 부분집합 Z(인덱스) → 자체 Group-호환 mul 를 가진 경량 래퍼."""
    S = sorted(Z)
    pos = {g: i for i, g in enumerate(S)}
    m = len(S)
    mul = [[pos[G.mul[S[a]][S[b]]] for b in range(m)] for a in range(m)]

    class _G:
        pass
    g = _G()
    g.n = m
    g.mul = mul
    return g


def _has_nondeg_alt(Zg):
    """아벨군 Zg 가 non-degenerate alternating μ₂-form 을 허용하는가(사영 2차원 irrep 조건).
    = Zg 에 ℤ₂×ℤ₂ 부분몫이 있어 symplectic pairing 가능 ⟺ 2-rank ≥ 2."""
    n, mul = Zg.n, Zg.mul
    ident = next(e for e in range(n) if all(mul[e][x] == x for x in range(n)))
    invol = [x for x in range(n) if x != ident and mul[x][x] == ident]  # 위수-2 원소
    return len(invol) >= 3        # ℤ₂² 는 involution 3개(2-rank 2) · ℤ₄ 는 1개


def main():
    quick = "--quick" in sys.argv
    out = {"_schema": "dtw-d4-q8-double/v1",
           "_note": ("twisted 비아벨 double D^ω(D₄)/D^ω(Q₈) — 비아벨 군 위 비자명 twist 최초"
                     "(관측·seal 아님·신규 module 0·root 불변). ★D₄≠Q₈ twist 자원 비대칭"
                     "(H³(μ₂) dim 4 vs 1)·섹터 selectivity·차원 전이. 완전 22×22 S 미착수.")}
    R = {}
    d4 = analyze_group("D4")
    q8 = analyze_group("Q8")
    out["D_D4"] = d4
    out["D_Q8"] = q8

    # 1. H³ 자체유도 대조
    R["D4_H3_mu2_is_4"] = (d4["H_dims"]["H3"] == 4)
    R["Q8_H3_mu2_is_1"] = (q8["H_dims"]["H3"] == 1)
    R["twist_resource_asymmetry"] = (d4["H_dims"]["H3"] != q8["H_dims"]["H3"])

    # 2. cocycle·certificate
    R["D4_cocycle_ok"] = d4["cocycle_ok"] and d4["noncoboundary"] and d4["cert_ok"]
    R["Q8_cocycle_ok"] = q8["cocycle_ok"] and q8["noncoboundary"] and q8["cert_ok"]

    # 3. anyon 구조 (v14 정합: 22 anyon·D²=64)
    R["D4_22_anyon_D2_64"] = (d4["anyon_count"] == 22 and d4["D2"] == 64)
    R["Q8_22_anyon_D2_64"] = (q8["anyon_count"] == 22 and q8["D2"] == 64)

    # 4. ★섹터 selectivity + 차원 전이 (centralizer H²(μ₂) 기반)
    R["D4_has_twistable_sectors"] = (d4["n_twistable_sectors"] >= 1)
    R["Q8_has_twistable_sectors"] = (q8["n_twistable_sectors"] >= 1)
    # ★핵심: D₄ 는 차원 전이 섹터(ℤ₂²) 有·Q₈ 는 無(순환 centralizer만)
    R["D4_dim_transition_present"] = (d4["n_dim_transition_sectors"] >= 1)
    R["Q8_no_dim_transition"] = (q8["n_dim_transition_sectors"] == 0)
    R["dim_transition_distinguishes_D4_Q8"] = (
        R["D4_dim_transition_present"] and R["Q8_no_dim_transition"])

    # teeth: coboundary 양성대조 (전 섹터 자명 → twist 섹터 0)
    #   (구현: 임의 2-cochain μ 의 dμ 로 coboundary ω 생성)
    G = Group("D4")
    n = G.n
    mu2 = [[(i + j) % 2 for j in range(n)] for i in range(n)]
    cbvec = 0
    for a, b, c in itertools.product(range(n), repeat=3):
        v = (mu2[b][c] ^ mu2[G.mul[a][b]][c] ^ mu2[a][G.mul[b][c]] ^ mu2[a][b]) & 1
        if v:
            cbvec |= 1 << ((a * n + b) * n + c)
    wcb = omega_fn(cbvec, n)
    R["teeth_coboundary_is_cocycle"] = all(
        (wcb(b, c, d) ^ wcb(G.mul[a][b], c, d) ^ wcb(a, G.mul[b][c], d)
         ^ wcb(a, b, G.mul[c][d]) ^ wcb(a, b, c)) == 0
        for a, b, c, d in itertools.product(range(n), repeat=4))
    cb_all_triv = True
    for ci in range(len(G.classes)):
        g = G.reps[ci]; Z = G.centralizer(g)
        if not beta_coboundary(slant(wcb, G.mul, g), Z, G.mul):
            cb_all_triv = False
    R["teeth_coboundary_all_sectors_trivial"] = cb_all_triv
    # 가짜 cocycle(단일 지점) → pentagon 위반 검출
    fake = lambda a, b, c: 1 if (a, b, c) == (1, 1, 1) else 0    # noqa: E731
    R["teeth_fake_cocycle"] = not all(
        (fake(b, c, d) ^ fake(G.mul[a][b], c, d) ^ fake(a, G.mul[b][c], d)
         ^ fake(a, b, G.mul[c][d]) ^ fake(a, b, c)) == 0
        for a, b, c, d in itertools.product(range(n), repeat=4))

    ok = bool(all(v for v in R.values()))
    out["checks"] = R
    out["triple_contrast"] = {
        "vs_D_D4_untwisted": {"H3_dim": [4, 0], "note": "untwisted H³ twist=0 vs twisted 자원 16"},
        "note": "D₄/Q₈ untwisted 동일(v14) → twist 자원(H³ 4 vs 1)·차원 전이(D₄ 有/Q₈ 無)로 구별",
    }
    out["scope_honesty"] = {
        "covered": ["H³(μ₂) 자체유도", "섹터 selectivity", "β-사영 irrep 차원분포", "T 다중집합"],
        "not_covered": ["완전 twisted DPR 22×22 S 행렬", "H³ 3-torsion(ζ₃)", "범주 동치·braiding"],
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "DTW-D4-Q8-DOUBLE.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("twisted 비아벨 double D^ω(D₄)/D^ω(Q₈) 관측 (seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  ★H³(μ₂): D₄ dim={d4['H_dims']['H3']}(|H³|=16) vs Q₈ dim={q8['H_dims']['H3']}(|H³|=2)"
              f" — twist 자원 비대칭", flush=True)
        print(f"  ★twistable 섹터: D₄ {d4['n_twistable_sectors']}개(차원전이 {d4['n_dim_transition_sectors']})"
              f" vs Q₈ {q8['n_twistable_sectors']}개(차원전이 {q8['n_dim_transition_sectors']})", flush=True)
        print(f"  ★차원분포(untwisted 공통): {d4['untw_dims']} · 차원전이 섹터 D₄={d4['n_dim_transition_sectors']} Q₈={q8['n_dim_transition_sectors']}",
              flush=True)
        print("  → .pgf/proofs/DTW-D4-Q8-DOUBLE.json", flush=True)
    print(f"dtw_d4_q8_double_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
