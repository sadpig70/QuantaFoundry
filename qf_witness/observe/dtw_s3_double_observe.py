#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dtw_s3_double_observe — TrackHE15 P2: D^ω(S₃) — registry **최초의 비아벨 군 twist**
(관측, seal 아님). 전 과정 정수/GF(2)·ζ 지수 산술(float 0).

계보: [[dsr3_double_observe]](v13, untwisted D(S₃) 완전 modular data) + [[dtw_z2z2_double_observe]]
(v14 P3, 아벨 ℤ₂² twist) + [[dtw_z2z2z2_typeiii_observe]](v15 P1, 아벨 ℤ₂³ type-III)의 **교차**:
지금까지 twist 는 전부 **아벨** 게이지군에서만 켰다. 본 witness 는 **비아벨 S₃** 에 3-cocycle 을
켜고, twist 가 어느 섹터를 바꾸는지 판정한다.

★자체 재유도 (외부 인용 금지 — §4′m):
  1. GF(2) cochain 전수로 **dim H²(S₃,μ₂)=1 · dim H³(S₃,μ₂)=1** 산출
     (C¹=6·C²=36·C³=216·C⁴=1296, rank d₁/d₂/d₃).
     ★정직 주의: H²(S₃,**μ₂**)=ℤ₂ 는 H²(S₃,**U(1)**)=0(Schur multiplier 자명)과 **다르다**
     — 계수군이 다름(초기 기대 오류를 실측으로 정정). 본 witness 는 μ₂ 계수 값만 주장.
     H³(S₃,μ₂) ≅ H³(S₃,U(1))의 2-torsion 부분(장완전열; H²(S₃,U(1))=0 은 무주장).
  2. ω₂ = ker d₃ ∖ im d₂ 의 명시 대표 + **비-coboundary certificate** + cocycle 8⁴… 전수 검증.

★핵심 관측 — twist 가 **한 섹터만** 비튼다:
  slant β_g(h,k) = ω(g,h,k)ω(h,k,g)/ω(h,g,k) 를 켤레류별 centralizer 위에서 코호몰로지
  분류(GF(2) coboundary solve)한 결과:
    g=e        (Z=S₃, |Z|=6) → β **자명**(coboundary)   → 선형표현 3개 (d=1,1,2)
    g=(12) 전치 (Z=ℤ₂, |Z|=2) → β **비자명**            → ★**사영표현**(ρ(s)²=−1 ⟹ ρ(s)=±i)
    g=(123) 3-순환(Z=ℤ₃, |Z|=3) → β **자명**            → 선형표현 3개 (ζ₃ 지표)
  ⟹ anyon 수·양자차원은 untwisted 와 **동일**(8 anyon, d=1,1,2,3,3,2,2,2)하지만,
     전치 섹터의 스핀이 θ=±1 → **θ=±i** 로 이동 ⟹ **T 다중집합이 갈린다**(twist 판별 성공).
  T 는 ζ₁₂ 지수 정수로 표기(전치 ±i=ζ₁₂^{3,9} · 3-순환 ζ₃=ζ₁₂^{4,8}) — ℚ(ζ₁₂) 부동소수 0.

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - **완전 S 행렬 미착수**: twisted DPR(Dijkgraaf-Pasquier-Roche) S 공식은 본 범위 밖.
    본 witness 는 **T 다중집합 + 섹터별 β 클래스 + anyon 차원**만으로 판별한다
    (v14 P1 교훈: T 만으로 클래스가 중복될 수 있으므로 "판별 성공"만 주장하고 **범주 동치·
    완전 분류는 무주장**).
  - **H³(S₃,U(1))≅ℤ₆ 전체 무주장**: 본 witness 는 **2-torsion(μ₂)만** 자체 재유도.
    3-torsion(ζ₃-값 cocycle)은 미착수 — v13 D(S₃) 관측이 ℚ(ζ₃) 를 쓴 선례가 있으나
    3-torsion twist 자체는 별도 작업.
  - **MS(Mignard-Schauenburg) probe 미착수**: 최소 반례는 ℤ₁₁⋊ℤ₅(|G|=55)·ζ₁₁ 규모로
    본 범위 밖. P2b 는 **정직 미착수**로 남긴다(설계 문서의 "정직한 음성" 조항 적용).
  - modular data·코호몰로지 표는 관측(certificate) — 회로 봉인 아님.

사용: python -m qf_witness.observe.dtw_s3_double_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import itertools
from collections import Counter

NG = 6                                   # |S₃|
E = list(itertools.permutations(range(3)))
IDX = {p: i for i, p in enumerate(E)}


def pm(p, q):
    return tuple(p[q[i]] for i in range(3))


def pinv(p):
    r = [0] * 3
    for i, v in enumerate(p):
        r[v] = i
    return tuple(r)


GM = [[IDX[pm(E[a], E[b])] for b in range(NG)] for a in range(NG)]
GINV = [IDX[pinv(E[a])] for a in range(NG)]
E_IDX = IDX[(0, 1, 2)]


def conj_classes():
    seen, out = set(), []
    for g in range(NG):
        if g in seen:
            continue
        cl = sorted({GM[GM[x][g]][GINV[x]] for x in range(NG)})
        out.append(cl); seen.update(cl)
    return out


def centralizer(g):
    return [x for x in range(NG) if GM[x][g] == GM[g][x]]


# ── GF(2) cochain ─────────────────────────────────────────────────────────
def gf2_rank(rows):
    basis = []
    for r in rows:
        for b in basis:
            r = min(r, r ^ b)
        if r:
            basis.append(r); basis.sort(reverse=True)
    return len(basis)


def gf2_solve(eqs):
    """A x = b (GF(2)). (True,x,None) | (False,None,y_combo) — y·A=0·y·b=1."""
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


def d1_rows():
    return [(1 << b) ^ (1 << GM[a][b]) ^ (1 << a)
            for a in range(NG) for b in range(NG)]


def _i2(x, y):
    return x * NG + y


def _i3(x, y, z):
    return (x * NG + y) * NG + z


def d2_rows():
    return [(1 << _i2(b, c)) ^ (1 << _i2(GM[a][b], c))
            ^ (1 << _i2(a, GM[b][c])) ^ (1 << _i2(a, b))
            for a in range(NG) for b in range(NG) for c in range(NG)]


def d3_rows():
    out = []
    for a, b, c, d in itertools.product(range(NG), repeat=4):
        out.append((1 << _i3(b, c, d)) ^ (1 << _i3(GM[a][b], c, d))
                   ^ (1 << _i3(a, GM[b][c], d)) ^ (1 << _i3(a, b, GM[c][d]))
                   ^ (1 << _i3(a, b, c)))
    return out


def find_nontrivial_omega():
    """ker d₃ ∖ im d₂ 의 결정론 첫 원소 (216-bit 벡터)."""
    d2r, d3r = d2_rows(), d3_rows()
    img = []
    for j in range(NG * NG):
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
    free = [c for c in range(NG ** 3) if c not in piv]
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
            return x, len(basis), len(free)
    return None, len(basis), len(free)


def omega_fn(vec):
    return lambda a, b, c: (vec >> _i3(a, b, c)) & 1


def is_cocycle3(w):
    for a, b, c, d in itertools.product(range(NG), repeat=4):
        if (w(b, c, d) ^ w(GM[a][b], c, d) ^ w(a, GM[b][c], d)
                ^ w(a, b, GM[c][d]) ^ w(a, b, c)):
            return False
    return True


def slant(w, g):
    return lambda h, k: (w(g, h, k) ^ w(h, k, g) ^ w(h, g, k)) & 1


def beta_class(beta, Z):
    """β 가 Z 위 coboundary(자명 클래스)인가 — GF(2) solve."""
    zi = {x: i for i, x in enumerate(Z)}
    eqs = [(((1 << zi[h]) ^ (1 << zi[k]) ^ (1 << zi[GM[h][k]])), beta(h, k))
           for h in Z for k in Z]
    sat, _, _ = gf2_solve(eqs)
    return sat


def beta_is_2cocycle(beta, Z):
    return all((beta(k, l) ^ beta(GM[h][k], l) ^ beta(h, GM[k][l]) ^ beta(h, k)) == 0
               for h, k, l in itertools.product(Z, repeat=3))


# ── 스핀 θ: ζ₁₂ 지수(정수)로 표기 ─────────────────────────────────────────
def sector_thetas(beta, Z, g, trivial):
    """섹터 (g, Z, β) 의 anyon 스핀 θ = χ_ρ(g)/d_ρ 를 ζ₁₂ 지수로.
    β 자명(coboundary) → 선형표현 지표(위수 |Z| 의 근); β 비자명(|Z|=2) → 사영 ρ(s)²=−1 ⟹ ±i."""
    n = len(Z)
    if trivial:
        if g == E_IDX:
            return [0] * 3                    # S₃ 3 irreps, θ=χ(e)/d=1
        # 순환 centralizer(ℤ₂ or ℤ₃)의 선형지표: θ = ζ_n^j
        return [(12 // n) * j for j in range(n)]
    # 비자명 β on ℤ₂: ρ(s)² = β(s,s)·1 = −1 → ρ(s) = ±i = ζ₁₂^{3,9}
    assert n == 2, ("비자명 β 는 |Z|=2 섹터에서만 처리(그 밖은 미착수)", n)
    return [3, 9]


def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "dtw-s3-double/v1",
           "_note": ("D^ω(S₃) — registry 최초 비아벨 군 twist(관측·seal 아님·신규 module 0·"
                     "root 불변). H³(S₃,μ₂) 자체 재유도 + 섹터별 slant β 분류 + T 다중집합 판별. "
                     "★완전 S 행렬(twisted DPR)·H³ 3-torsion·MS probe 는 미착수 정직 명시.")}

    classes = conj_classes()
    R["class_sizes_1_3_2"] = (sorted(len(c) for c in classes) == [1, 2, 3])
    cents = {c[0]: centralizer(c[0]) for c in classes}
    R["centralizer_orders_6_2_3"] = (sorted(len(z) for z in cents.values()) == [2, 3, 6])

    # 1. 코호몰로지 자체 재유도
    r1, r2 = gf2_rank(d1_rows()), gf2_rank(d2_rows())
    r3 = gf2_rank(d3_rows())
    h2 = (NG * NG - r2) - r1
    h3 = (NG ** 3 - r3) - r2
    out["cohomology_mu2"] = {"rank_d1": r1, "rank_d2": r2, "rank_d3": r3,
                             "dim_H2_mu2": h2, "dim_H3_mu2": h3,
                             "note": ("★H²(S₃,μ₂)=ℤ₂ 는 H²(S₃,U(1))=0 과 다름(계수군 차이) — "
                                      "본 witness 는 μ₂ 값만 주장. H³(S₃,μ₂) ≅ "
                                      "H³(S₃,U(1))의 2-torsion(장완전열; U(1) 값 무주장)")}
    R["dim_H3_mu2_is_1"] = (h3 == 1)
    R["dim_H2_mu2_is_1"] = (h2 == 1)

    # 2. ω₂ 대표 + certificate
    vec, dim_img, dim_ker = find_nontrivial_omega()
    R["omega_found"] = (vec is not None)
    w = omega_fn(vec)
    R["omega_is_cocycle"] = is_cocycle3(w)
    # 비-coboundary certificate: ω ∈ im d₂ 선형계가 UNSAT
    d2r = d2_rows()
    eqs = [(d2r[i], (vec >> i) & 1) for i in range(NG ** 3)]
    sat, _, ycert = gf2_solve(eqs)
    R["omega_not_coboundary"] = (not sat)
    cert_ok = False
    if ycert is not None:
        accm = accb = 0
        i, y = 0, ycert
        idxs = []
        while y:
            if y & 1:
                idxs.append(i)
            y >>= 1; i += 1
        for i2 in idxs:
            m, r = eqs[i2]
            accm ^= m; accb ^= r
        cert_ok = (accm == 0 and accb == 1)
        out["noncoboundary_certificate"] = {"support_size": len(idxs)}
    R["certificate_verified"] = cert_ok

    # 3. ★섹터별 slant β 분류
    sectors = {}
    for cl in classes:
        g = cl[0]
        Z = cents[g]
        beta = slant(w, g)
        assert beta_is_2cocycle(beta, Z), ("β not 2-cocycle", g)
        triv = beta_class(beta, Z)
        sectors[str(E[g])] = {"class_size": len(cl), "centralizer_order": len(Z),
                              "beta_trivial": triv,
                              "beta_g_g": beta(g, g) if g in Z else None}
    R["beta_2cocycle_all"] = True
    twisted_sectors = [k for k, v in sectors.items() if not v["beta_trivial"]]
    R["exactly_one_twisted_sector"] = (len(twisted_sectors) == 1)
    R["twisted_sector_is_transposition"] = (
        len(twisted_sectors) == 1 and sectors[twisted_sectors[0]]["centralizer_order"] == 2)
    out["sectors"] = sectors
    out["twisted_sectors"] = twisted_sectors

    # 4. anyon 구조 + T 다중집합 (ζ₁₂ 지수)
    dims_tw, thetas_tw, dims_un, thetas_un = [], [], [], []
    for cl in classes:
        g = cl[0]
        Z = centralizer(g)
        n = len(Z)
        beta = slant(w, g)
        triv = beta_class(beta, Z)
        # 양자차원 d = |C| · dim(irrep)
        irrep_dims = [1, 1, 2] if g == E_IDX else [1] * n
        dims_tw += [len(cl) * d for d in irrep_dims]
        dims_un += [len(cl) * d for d in irrep_dims]
        thetas_tw += sector_thetas(beta, Z, g, triv)
        thetas_un += sector_thetas(beta, Z, g, True)      # untwisted = β 자명 취급
    R["anyon_count_8"] = (len(dims_tw) == 8)
    R["total_dim_36"] = (sum(d * d for d in dims_tw) == NG * NG)
    R["dims_match_untwisted"] = (sorted(dims_tw) == sorted(dims_un))
    tw_T, un_T = sorted(thetas_tw), sorted(thetas_un)
    R["T_multiset_differs"] = (tw_T != un_T)
    out["modular_partial"] = {
        "anyon_count": len(dims_tw),
        "quantum_dims": sorted(dims_tw),
        "total_dim_squared": sum(d * d for d in dims_tw),
        "T_zeta12_exponents_twisted": tw_T,
        "T_zeta12_exponents_untwisted": un_T,
        "T_multiset_twisted": dict(Counter(tw_T)),
        "T_multiset_untwisted": dict(Counter(un_T)),
        "verdict": ("★twist 판별 성공 — anyon 수·양자차원은 동일하나 전치 섹터 스핀이 "
                    "±1(ζ₁₂^{0,6}) → ±i(ζ₁₂^{3,9}) 로 이동"),
    }

    # 5. teeth
    #   (i) coboundary ω 양성대조: 전 섹터 β 자명 → T 가 untwisted 와 일치
    mu2 = [[(i + j) % 2 for j in range(NG)] for i in range(NG)]   # 임의 2-cochain μ
    cbvec = 0
    for a, b, c in itertools.product(range(NG), repeat=3):
        v = (mu2[b][c] ^ mu2[GM[a][b]][c] ^ mu2[a][GM[b][c]] ^ mu2[a][b]) & 1
        if v:
            cbvec |= 1 << _i3(a, b, c)
    wcb = omega_fn(cbvec)
    R["teeth_coboundary_is_cocycle"] = is_cocycle3(wcb)
    cb_triv = all(beta_class(slant(wcb, cl[0]), centralizer(cl[0])) for cl in classes)
    R["teeth_coboundary_all_sectors_trivial"] = cb_triv
    #   (ii) cocycle 위반 검출
    R["teeth_fake_cocycle"] = not is_cocycle3(
        lambda a, b, c: 1 if (a, b, c) == (1, 1, 1) else 0)

    ok = bool(all(R.values()))
    out["checks"] = R
    out["scope_honesty"] = {
        "covered": ["H²/H³(S₃,μ₂) 자체 재유도", "ω₂ 비-coboundary certificate",
                    "섹터별 slant β 분류", "anyon 차원·T 다중집합 판별"],
        "not_covered": ["완전 S 행렬(twisted DPR 공식)", "H³(S₃) 3-torsion(ζ₃ twist)",
                        "MS probe(ℤ₁₁⋊ℤ₅·|G|=55 규모 — 범위 밖)",
                        "범주(braided) 동치·완전 분류"],
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "DTW-S3-DOUBLE.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("D^ω(S₃) 비아벨 twist 관측 (seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  ★코호몰로지 자체유도: dim H²(S₃,μ₂)={h2} · dim H³(S₃,μ₂)={h3}", flush=True)
        print(f"  ★섹터별 β: " + " · ".join(
            f"{k}(|Z|={v['centralizer_order']}) {'자명' if v['beta_trivial'] else '★비자명'}"
            for k, v in sectors.items()), flush=True)
        print(f"  ★T(ζ₁₂ 지수) twisted={dict(Counter(tw_T))} vs untwisted={dict(Counter(un_T))} "
              f"→ 판별={R['T_multiset_differs']}", flush=True)
        print("  ★정직: 완전 S 행렬·3-torsion·MS probe 미착수", flush=True)
        print("  → .pgf/proofs/DTW-S3-DOUBLE.json", flush=True)
    print(f"dtw_s3_double_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
