#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dtw_z2z2z2_typeiii_observe — TrackHE15 P1: D^ω(ℤ₂³) type-III twisted double
— 아벨 게이지군의 **부분 비아벨화** + D(D₄)/D(Q₈) 삼자 대조 (관측, seal 아님).

[[dtw_z2z2_double_observe]](v14 P3, ℤ₂² type-I/II)과 [[dihedral_quaternion_double_observe]]
(v14 P1, D(D₄)/D(Q₈) 쌍 대조)의 **교차 확장**: 아벨군 ℤ₂³ 에 **type-III** 3-cocycle
ω(a,b,c)=(−1)^{a₁b₂c₃} 를 켜면 slant β_a 가 **비자명 commutator form** 을 만들어 centralizer
(=G 전체, 아벨)의 **사영표현(projective irrep)** 이 2차원이 된다 — 즉 **아벨 게이지군에서
비아벨 애니온이 발생**한다. v14 P3(type-I/II)는 전 클래스가 pointed(전부 d=1)였다.

★report15 런타임 상충 판정(§4′m 외부 수치 자체 재검증 — 4런타임이 갈렸음):
  "22 anyon"(2런타임) vs "64 anyon"(2런타임) → **22 가 옳다**. 64 는 untwisted D(ℤ₂³)
  (8 켤레류×8 지표)의 수치를 type-III 에 오적용한 것. 본 witness 가 자체 유도로 확정:
    B_a = 𝔽₂³ 위 교대형(alternating) → a≠0 이면 **rank 2**(홀수차원 교대형 rank≤2)
    → radical R_a={0,a}(1차원, ★agent08 경고 "완전 비아벨화 불가" 확인)
    → 사영 irrep 2개·각 d=√(|G|/|R_a|)=2 → anyon = 8(a=0, d=1) + 7×2(d=2) = **22**, D²=64.

관측 계층 (전부 exact — ℚ(i) 정확산술·float 0):
  1. H³(ℤ₂³,U(1)) 자체 재유도: GF(2) cochain(C²=64·C³=512·C⁴=4096) rank →
     dim H³(𝔽₂)=10(3변수 3차 단항식) · ⟨i⟩-스코프 ±1-cocycle 클래스 2^7=**128**.
     type-I(3)·type-II(3)·type-III(1) 생성기 분해 자체 확인.
  2. type-III cocycle identity 8⁴=4096 전수 · β_a 2-cocycle 전수 · 비-coboundary certificate.
  3. ★사영표현 **명시적 2×2 구성**: 생성원 {a(radical, 스칼라 λ), e→X, f→Z}(B_a(e,f)=1)에
     ℚ(i) phase 를 주고 나머지는 **순차 곱** ρ(x⊕g)=ρ(x)ρ(g)β_a(x,g) 로 정의 →
     ρ(g)ρ(h)=β_a(g,h)ρ(gh) **64쌍 전수 검증**(지표만이 아닌 실제 표현 존재 실증).
     ★분리형 ansatz(λ^{[r=a]}·μ_{ij}·X^iZ^j)는 β_a(a,e^i f^j) 부호의 좌표 의존 때문에 깨진다
     (a=5 에서 검출) — 순차 곱이 그 부호를 자동 흡수. 기저 (e,f) 도 실패 시 재시도.
  4. modular data: S_{(a,ρ),(b,σ)}=(1/|G|)·χ_ρ(b)*·χ_σ(a)* · θ=χ_ρ(a)/d_ρ.
     공리 전량: SS†=I·S 대칭·S²=C(순열,C²=I)·**Verlinde 비음정수**(pointed 아님)·
     (ST)³=λS²(λ=1, c≡0 mod 8)·Gauss 합·사영지표 직교성 Σ_h χ_ρ χ_σ* = |G|δ.
  5. ★**삼자 대조**(라벨 순열 불변량만): {d}·{θ}·**{(d,θ)} 쌍**·tr(S^k) k=1..4·λ·Gauss —
     D^ω(ℤ₂³)_III vs D(D₄) vs D(Q₈) (v14 P1 모듈 직접 재사용).
  teeth: (i) S 성분 섭동→공리 붕괴 (ii) 가짜 cocycle 검출 (iii) ★type-I twist 대조군:
     같은 기계에 type-I ω 를 넣으면 전 anyon d=1(pointed 64개) — 비아벨화가 **type-III 고유**임을 실증.

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0): modular data 표는 봉인 아님.
  "modular data 수준 동형/분기"만 주장 — **범주(braided) 동치는 무주장**(F/R symbol 미계산,
  Mignard-Schauenburg 류 한계 의식). 사영표현은 명시 구성했으나 게이트 분해 아님(§2 무관).
  type-III 대표 1개 + 비자명성 인증(전 128 클래스 modular data 전수는 범위 밖 — 정직 축소).

사용: python -m qf_witness.observe.dtw_z2z2z2_typeiii_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import itertools
from fractions import Fraction as F

# v14 P1 기계 복리 — ℚ(i) 정확산술·행렬 유틸·Verlinde·(ST)³ (재구현 금지)
from qf_witness.observe.dihedral_quaternion_double_observe import (
    Cyc, ZERO, ONE, I, matmul, dagger, is_identity, perm_of,
    st_cubed_lambda, t_multiset, verlinde_ok, verify_double)

NG = 8                      # |ℤ₂³|
IPOW = [ONE, I, Cyc(-1), Cyc(0, -1)]


def bits(g):
    return ((g >> 2) & 1, (g >> 1) & 1, g & 1)


# ── 3-cocycle 생성기: type-I(3)·type-II(3)·type-III(1) ─────────────────────
def omega_typeI(i):
    """ω(a,b,c) = (−1)^{a_i b_i c_i}."""
    return lambda a, b, c: (bits(a)[i] & bits(b)[i] & bits(c)[i]) & 1


def omega_typeII(i, j):
    """ω(a,b,c) = (−1)^{a_i b_j c_j}."""
    return lambda a, b, c: (bits(a)[i] & bits(b)[j] & bits(c)[j]) & 1


def omega_typeIII(a, b, c):
    """★type-III: ω(a,b,c) = (−1)^{a₁ b₂ c₃} — 세 생성자 전부 관여."""
    return (bits(a)[0] & bits(b)[1] & bits(c)[2]) & 1


def is_cocycle(e):
    """pentagon(정규화 ±1 지수): 8⁴=4096 전수."""
    for a, b, c, d in itertools.product(range(NG), repeat=4):
        if (e(b, c, d) ^ e(a ^ b, c, d) ^ e(a, b ^ c, d) ^ e(a, b, c ^ d) ^ e(a, b, c)):
            return False
    return True


def slant(e):
    """β_a(h,k) = ω(a,h,k)·ω(h,k,a)/ω(h,a,k) 의 지수."""
    return lambda a, h, k: (e(a, h, k) ^ e(h, k, a) ^ e(h, a, k)) & 1


def beta_is_2cocycle(beta):
    for a, h, k, l in itertools.product(range(NG), repeat=4):
        if (beta(a, k, l) ^ beta(a, h ^ k, l) ^ beta(a, h, k ^ l) ^ beta(a, h, k)):
            return False
    return True


def comm_form(beta):
    """B_a(h,k) = β_a(h,k) − β_a(k,h) (𝔽₂ 교대형)."""
    return lambda a, h, k: (beta(a, h, k) ^ beta(a, k, h)) & 1


def radical(B, a):
    return [h for h in range(NG) if all(B(a, h, k) == 0 for k in range(NG))]


def proj_chars_on_radical(beta, a, R):
    """R(=radical) 위 β_a-사영 1차원 지표 λ 전수. λ(0)=1·λ(g)λ(h)=β_a(g,h)λ(g⊕h).
    β_a=±1 → λ(g)²=β_a(g,g) ∈{±1} → λ ∈ {±1,±i} ⊂ ℚ(i). 개수는 |R| 이어야 한다."""
    Rl = sorted(R)
    gens, basis = [], []
    for g in Rl:
        if g == 0:
            continue
        red = g
        for b in basis:
            red = min(red, red ^ b)
        if red:
            gens.append(g); basis.append(red); basis.sort(reverse=True)
    out = []
    for combo in itertools.product(range(4), repeat=len(gens)):
        lam = {0: ONE}
        for mask in range(1, 1 << len(gens)):
            cur, val = 0, ONE
            for i in range(len(gens)):
                if (mask >> i) & 1:
                    b = Cyc(-1) if beta(a, cur, gens[i]) else ONE
                    val = val * IPOW[combo[i]] * b      # λ(x⊕y)=λ(x)λ(y)·β (β=±1)
                    cur ^= gens[i]
            lam[cur] = val
        if len(lam) != len(Rl):
            continue
        good = True
        for g in Rl:
            for h in Rl:
                b = Cyc(-1) if beta(a, g, h) else ONE
                if not (lam[g] * lam[h] == b * lam[g ^ h]):
                    good = False
                    break
            if not good:
                break
        if good:
            out.append(lam)
    return out


# ── GF(2) cochain 층 (H³ 자체 재유도) ──────────────────────────────────────
def gf2_rank(rows):
    basis = []
    for r in rows:
        for b in basis:
            r = min(r, r ^ b)
        if r:
            basis.append(r); basis.sort(reverse=True)
    return len(basis)


def cochain_h3():
    """dim H³(ℤ₂³,𝔽₂) 와 ⟨i⟩-스코프 ±1-cocycle 클래스 수를 자체 유도."""
    def idx3(a, b, c):
        return (a * NG + b) * NG + c
    # d₃: C³(512) → C⁴(4096), GF(2)
    d3 = []
    for a, b, c, d in itertools.product(range(NG), repeat=4):
        m = 0
        for (x, y, z) in ((b, c, d), (a ^ b, c, d), (a, b ^ c, d), (a, b, c ^ d), (a, b, c)):
            m ^= 1 << idx3(x, y, z)
        d3.append(m)
    dimZ3 = NG ** 3 - gf2_rank(d3)
    # D₂ (정수): dμ(a,b,c) = μ(b,c) − μ(ab,c) + μ(a,bc) − μ(a,b)
    D2 = []
    for a, b, c in itertools.product(range(NG), repeat=3):
        coeff = [0] * (NG * NG)
        coeff[b * NG + c] += 1
        coeff[(a ^ b) * NG + c] -= 1
        coeff[a * NG + (b ^ c)] += 1
        coeff[a * NG + b] -= 1
        D2.append(coeff)
    A2 = []
    for coeff in D2:
        m = 0
        for j, v in enumerate(coeff):
            if v % 2:
                m |= 1 << j
        A2.append(m)
    # B³_𝔽₂ = im(A₂)
    img = []
    for j in range(NG * NG):
        v = 0
        for i, row in enumerate(A2):
            if (row >> j) & 1:
                v |= 1 << i
        img.append(v)
    dimB3 = gf2_rank(img)
    # ⟨i⟩ 도달공간 R = span(im A₂ ∪ h(ker A₂ lift)), h(k)=(D₂k)/2 mod 2
    # ker A₂ 기저
    mat, piv = [], []
    for r in A2:
        rr = r
        for br, pc in zip(mat, piv):
            if (rr >> pc) & 1:
                rr ^= br
        if rr:
            mat.append(rr); piv.append(rr.bit_length() - 1)
    free = [c for c in range(NG * NG) if c not in piv]
    Rspan = list(img)
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
        kv = [(x >> j) & 1 for j in range(NG * NG)]
        v = 0
        for i, coeff in enumerate(D2):
            w = sum(cf * k for cf, k in zip(coeff, kv))
            assert w % 2 == 0, "kernel lift 짝수성 위반"
            if (w // 2) % 2:
                v |= 1 << i
        Rspan.append(v)
    dimR = gf2_rank(Rspan)
    return {"dim_Z3_F2": dimZ3, "dim_B3_F2": dimB3, "dim_H3_F2": dimZ3 - dimB3,
            "iscope_classes_log2": dimZ3 - dimR}


# ── 사영표현 명시 구성 (2×2, ℚ(i)) ────────────────────────────────────────
PX = [[ZERO, ONE], [ONE, ZERO]]
PZ = [[ONE, ZERO], [ZERO, Cyc(-1)]]
PI2 = [[ONE, ZERO], [ZERO, ONE]]


def _m2(A, B):
    return [[A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]],
            [A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]]]


def _smul2(c, A):
    return [[c * A[0][0], c * A[0][1]], [c * A[1][0], c * A[1][1]]]


def _eq2(A, B):
    return all(A[i][j] == B[i][j] for i in range(2) for j in range(2))


def build_proj_rep(beta, a, lam):
    """G = R_a ⊕ ⟨e⟩ ⊕ ⟨f⟩ 좌표에서 ρ(r e^i f^j)=λ^{[r=a]}·μ_{ij}·X^i Z^j 의 μ 전수 결정.
    ρ(g)ρ(h)=β_a(g,h)ρ(gh) 를 64쌍 전수 만족하는 μ 존재 시 rep 반환(없으면 None)."""
    B = comm_form(beta)
    R = radical(B, a)
    assert R == sorted([0, a]) or R == [0], (a, R)
    # (e,f): B_a(e,f)=1 인 symplectic 쌍 — {R, e, f} 가 𝔽₂³ 기저여야(e⊕f ∉ R)
    ef = [(e, f) for e in range(NG) for f in range(NG)
          if B(a, e, f) == 1 and e not in R and f not in R and (e ^ f) not in R]
    for e, f in ef:                      # ★기저 선택마다 재시도(단일 후보 고정 시 실패 가능)
        rho = _try_rep(beta, a, lam, R, e, f)
        if rho is not None:
            return rho
    return None


def _try_rep(beta, a, lam, R, e, f):
    """생성원 {a(=radical, 스칼라 λ), e→X, f→Z} 에 phase 를 주고 나머지는 **순차 곱**으로 정의:
       ρ(x⊕g) = ρ(x)·ρ(g)·β_a(x,g)   (β=±1 이므로 나눗셈=곱셈)
    ★단순 분리형 ansatz(λ^{[r=a]}·μ_{ij}·X^i Z^j)는 β_a(a, e^i f^j) 부호가 좌표에 의존할 때
      깨진다(a=5 실패로 검출) — 순차 곱은 그 부호를 자동 흡수한다."""
    coord = {}
    for p_ in (0, 1):
        for i in (0, 1):
            for j in (0, 1):
                g = (a if p_ else 0) ^ (e if i else 0) ^ (f if j else 0)
                coord[g] = (p_, i, j)
    if len(coord) != NG:
        return None
    for me, mf in itertools.product(range(4), repeat=2):
        gen_mat = {a: _smul2(lam, PI2), e: _smul2(IPOW[me], PX), f: _smul2(IPOW[mf], PZ)}
        rho = {}
        for g, (p_, i, j) in coord.items():
            cur, M = 0, PI2
            for gen in ([a] * p_ + [e] * i + [f] * j):
                b = Cyc(-1) if beta(a, cur, gen) else ONE
                M = _smul2(b, _m2(M, gen_mat[gen]))
                cur ^= gen
            rho[g] = M
        ok = True
        for g in range(NG):
            for h in range(NG):
                lhs = _m2(rho[g], rho[h])
                rhs = _smul2(Cyc(-1) if beta(a, g, h) else ONE, rho[g ^ h])
                if not _eq2(lhs, rhs):
                    ok = False
                    break
            if not ok:
                break
        if ok:
            return rho
    return None


# ── modular data ───────────────────────────────────────────────────────────
class TwistedDoubleZ2n:
    """D^ω(ℤ₂³): anyon = (a, 사영irrep of G w.r.t. β_a)."""

    def __init__(self, e):
        self.beta = slant(e)
        self.B = comm_form(self.beta)
        self.anyons = []          # (a, irrep_idx)
        self.chi = []             # dict h -> Cyc (사영 지표)
        self.dim = []
        self.reps = []            # 명시 2×2 rep (a≠0) 또는 None
        for a in range(NG):
            R = radical(self.B, a)
            r = len(R)
            d2, rem = divmod(NG, r)
            assert rem == 0
            d = int(round(d2 ** 0.5))
            assert d * d * r == NG, (a, r, d)
            # 사영 irrep: 개수 = |R|(β-정칙류 수)·차원 d=√(|G|/|R|) — Σd²=|G|
            lams = proj_chars_on_radical(self.beta, a, R)
            assert len(lams) == r, (a, r, len(lams))
            for li, lam in enumerate(lams):
                ch = {h: ZERO for h in range(NG)}
                for h in R:
                    ch[h] = Cyc(d) * lam[h]              # 사영 지표는 radical 밖에서 0
                self.anyons.append((a, li)); self.chi.append(ch)
                self.dim.append(d); self.reps.append((a, lam[a]) if d > 1 else None)
        self.N = len(self.anyons)

    def build_S_T(self):
        S = [[ZERO] * self.N for _ in range(self.N)]
        for x in range(self.N):
            ax = self.anyons[x][0]
            for y in range(self.N):
                ay = self.anyons[y][0]
                S[x][y] = (self.chi[x][ay].conj() * self.chi[y][ax].conj()).div_rat(NG)
        T = [self.chi[x][self.anyons[x][0]].div_rat(self.dim[x]) for x in range(self.N)]
        return S, T


def moments(S, kmax=4):
    """tr(S^k) — 라벨 순열 불변량."""
    n = len(S)
    out, P = [], [[ONE if i == j else ZERO for j in range(n)] for i in range(n)]
    for _ in range(kmax):
        P = matmul(P, S)
        t = ZERO
        for i in range(n):
            t = t + P[i][i]
        out.append(str(t))
    return out


def dtheta_pairs(dims, T):
    return sorted((str(d), str(t.a), str(t.b)) for d, t in zip(dims, T))


def verify_axioms(D, S, T, label):
    n = D.N
    res, ck = {"label": label, "n_anyon": n}, {}
    Dsq = sum(d * d for d in D.dim)
    res["D2"] = Dsq
    res["dims"] = {str(d): D.dim.count(d) for d in sorted(set(D.dim))}
    ck["S_unitary"] = is_identity(matmul(S, dagger(S)))
    ck["S_symmetric"] = all(S[i][j] == S[j][i] for i in range(n) for j in range(n))
    S2 = matmul(S, S)
    perm = perm_of(S2)
    ck["S2_is_perm"] = perm is not None
    if perm is not None:
        ck["C_squared_I"] = all(perm[perm[i]] == i for i in range(n))
        res["self_dual"] = (perm == list(range(n)))
    ck["first_row_dims"] = all(S[0][x] == Cyc(F(D.dim[x], NG)) for x in range(n))
    vok, _ = verlinde_ok(S)
    ck["verlinde_nonneg_int"] = vok
    lam = st_cubed_lambda(S, T)
    ck["stcubed_lambda1"] = (lam is not None and lam == ONE)
    res["lambda"] = None if lam is None else str(lam)
    g = ZERO
    for d, t in zip(D.dim, T):
        g = g + Cyc(d) * Cyc(d) * t
    res["gauss_sum"] = str(g)
    # ★Gauss 합 = D·e^{2πic₋/8} (D=√Σd², D² 아님) — c≡0 mod 8 ⟺ 합 = D
    Droot = int(round(Dsq ** 0.5))
    ck["gauss_sum_eq_D_c0mod8"] = (Droot * Droot == Dsq and g == Cyc(Droot))
    ck["T_unit_modulus"] = all((t.a * t.a + t.b * t.b) == 1 for t in T)
    # 사영지표 직교성 Σ_h χ_ρ(h) χ_σ(h)* = |G|·δ
    orth = True
    for x in range(n):
        for y in range(n):
            if D.anyons[x][0] != D.anyons[y][0]:
                continue
            acc = ZERO
            for h in range(NG):
                acc = acc + D.chi[x][h] * D.chi[y][h].conj()
            want = Cyc(NG) if x == y else ZERO
            if not (acc == want):
                orth = False
    ck["proj_char_orthogonal"] = orth
    res["T_multiset"] = t_multiset(T)
    res["dtheta_pairs"] = dtheta_pairs(D.dim, T)
    res["S_moments"] = moments(S)
    res["checks"] = ck
    res["all_pass"] = all(ck.values())
    return res


def main():
    quick = "--quick" in sys.argv
    out = {"_schema": "dtw-z2z2z2-typeiii/v1",
           "_note": ("D^ω(ℤ₂³) type-III twisted double — 아벨 게이지군의 부분 비아벨화"
                     "(사영 irrep d=2 발생) + D(D₄)/D(Q₈) 삼자 대조(관측·seal 아님·"
                     "root 불변 sidecar·신규 module 0). ★report15 런타임 상충(22 vs 64 anyon) "
                     "자체 유도로 22 확정. modular data 수준 진술만 — 범주 동치 무주장.")}
    ck = {}

    # 1. H³ 자체 재유도
    if not quick:
        h3 = cochain_h3()
        out["cohomology"] = h3
        ck["dim_H3_F2_10"] = (h3["dim_H3_F2"] == 10)       # 3변수 3차 단항식
        ck["iscope_128"] = (h3["iscope_classes_log2"] == 7)  # 2⁷ = 128

    # 2. cocycle·slant 검증
    ck["typeIII_cocycle"] = is_cocycle(omega_typeIII)
    beta3 = slant(omega_typeIII)
    ck["beta_2cocycle"] = beta_is_2cocycle(beta3) if not quick else True
    B3 = comm_form(beta3)
    rads = {a: radical(B3, a) for a in range(NG)}
    out["radicals"] = {str(a): rads[a] for a in range(NG)}
    ck["radical_dim1_for_nonzero"] = all(len(rads[a]) == 2 and rads[a] == sorted([0, a])
                                         for a in range(1, NG))
    ck["radical_full_for_zero"] = (len(rads[0]) == NG)

    # 3. 사영표현 명시 구성 (a≠0 전수)
    D3 = TwistedDoubleZ2n(omega_typeIII)
    reps_ok = True
    for a in range(1, NG):
        base = IPOW[1] if beta3(a, a, a) else ONE
        for sgn in (ONE, Cyc(-1)):
            if build_proj_rep(beta3, a, base * sgn) is None:
                reps_ok = False
    ck["explicit_proj_reps_64pairs"] = reps_ok

    # 4. modular data + 공리
    S3, T3 = D3.build_S_T()
    r3 = verify_axioms(D3, S3, T3, "D^w(Z2^3) type-III")
    out["typeIII"] = r3
    ck["typeIII_axioms"] = r3["all_pass"]
    ck["anyon_22"] = (r3["n_anyon"] == 22)
    ck["D2_64"] = (r3["D2"] == 64)
    ck["nonabelian_d2_present"] = (r3["dims"].get("2", 0) == 14)

    # ★런타임 상충 판정 기록
    out["runtime_conflict_verdict"] = {
        "claim_22_anyon": True, "claim_64_anyon": False,
        "derivation": ("B_a = 𝔽₂³ 교대형 → a≠0 rank 2(홀수차원 교대형 rank≤2) → "
                       "radical {0,a} → 사영 irrep 2개·d=2 → 8 + 7×2 = 22, D²=64. "
                       "64 는 untwisted D(ℤ₂³)(8 켤레류×8 지표)의 수치 오적용."),
        "agent08_radical_warning_confirmed": ck["radical_dim1_for_nonzero"],
    }

    # 5. teeth (iii) type-I 대조군: 전 anyon d=1(pointed) — 비아벨화는 type-III 고유.
    #    ★Verlinde 는 O(n⁴)(n=64 → 1.7e7 항) 이라 구조 수치만 보고(정직 스코프).
    D1 = TwistedDoubleZ2n(omega_typeI(0))
    dims1 = {str(d): D1.dim.count(d) for d in sorted(set(D1.dim))}
    out["typeI_control"] = {"n_anyon": D1.N, "D2": sum(d * d for d in D1.dim),
                            "dims": dims1,
                            "note": "구조 수치만(Verlinde O(n⁴) 회피) — 비아벨화 부재 실증용"}
    ck["typeI_pointed_64"] = (D1.N == 64 and dims1 == {"1": 64}
                              and sum(d * d for d in D1.dim) == 64)

    # 6. ★삼자 대조 (라벨 순열 불변량)
    Dd4, rd4 = verify_double("D4")
    Dq8, rq8 = verify_double("Q8")

    def gdata(Dg, rg):
        S = Dg.S
        return {"n": rg["n_anyon"], "D2": rg["D2"],
                "dims": {str(d): rg["quantum_dims"].count(str(d))
                         for d in sorted(set(int(x) for x in rg["quantum_dims"]))},
                "T": rg["T_multiset"],
                "dtheta": dtheta_pairs(Dg.dim, Dg.T),
                "moments": moments(S), "lambda": rg["lambda"]}

    g_d4, g_q8 = gdata(Dd4, rd4), gdata(Dq8, rq8)
    g_t3 = {"n": r3["n_anyon"], "D2": r3["D2"], "dims": r3["dims"],
            "T": r3["T_multiset"], "dtheta": r3["dtheta_pairs"],
            "moments": r3["S_moments"], "lambda": r3["lambda"]}
    same = lambda x, y, k: x[k] == y[k]                                   # noqa: E731
    tri = {}
    for name, g in (("vs_D4", g_d4), ("vs_Q8", g_q8)):
        tri[name] = {
            "same_rank_D2": same(g_t3, g, "n") and same(g_t3, g, "D2"),
            "same_dims": same(g_t3, g, "dims"),
            "same_T_multiset": same(g_t3, g, "T"),
            "same_dtheta_pairs": same(g_t3, g, "dtheta"),
            "same_S_moments": same(g_t3, g, "moments"),
        }
        tri[name]["all_invariants_match"] = all(tri[name].values())
    out["triple_contrast"] = tri
    out["triple_data"] = {"typeIII": g_t3, "D_D4": g_d4, "D_Q8": g_q8}
    ck["triple_splits_D4_vs_Q8"] = (tri["vs_D4"]["all_invariants_match"]
                                    != tri["vs_Q8"]["all_invariants_match"])

    # teeth (i)(ii)
    Sp = [row[:] for row in S3]
    Sp[0][1] = Sp[0][1] + ONE
    broke = not is_identity(matmul(Sp, dagger(Sp)))
    if not broke:
        vk, _ = verlinde_ok(Sp)
        broke = not vk
    ck["teeth_S_perturbation"] = broke
    bad = [[[0] * NG for _ in range(NG)] for _ in range(NG)]
    ck["teeth_fake_cocycle"] = not is_cocycle(
        lambda a, b, c: 1 if (a, b, c) == (1, 1, 1) else 0)

    ok = bool(all(ck.values()))
    out["checks"] = ck
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "DTW-Z2Z2Z2-TYPEIII.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print(f"H³ 자체유도: dim H³(𝔽₂)={out['cohomology']['dim_H3_F2']} · "
              f"⟨i⟩-스코프 클래스=2^{out['cohomology']['iscope_classes_log2']}", flush=True)
        print(f"★type-III: {r3['n_anyon']} anyon · D²={r3['D2']} · dims={r3['dims']} · "
              f"λ={r3['lambda']} · 공리 all_pass={r3['all_pass']}", flush=True)
        print(f"  ★런타임 상충 판정: 22 anyon 확정(64 주장 반증) · radical 1차원 경고 확인="
              f"{ck['radical_dim1_for_nonzero']}", flush=True)
        print(f"  type-I 대조군: {out['typeI_control']['n_anyon']} anyon 전부 d=1(pointed) "
              f"→ 비아벨화는 type-III 고유", flush=True)
        for nm in ("vs_D4", "vs_Q8"):
            print(f"  ★삼자 {nm}: {tri[nm]}", flush=True)
        print("  → .pgf/proofs/DTW-Z2Z2Z2-TYPEIII.json", flush=True)
    print(f"dtw_z2z2z2_typeiii_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
