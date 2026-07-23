#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dtw_d4_full_modular_observe — TrackHE18: D^ω(D₄) **완전 22×22 twisted modular data(S·T)**
+ ★16 클래스 전수 anyon-count 반증 (관측, seal 아님). [[dtw_d4_modular_strata_observe]](TrackHE17
P4)가 "완전 twisted S=미착수"로 남긴 축의 완결.

★설계 원칙 = **공식 암기 대신 기계검증 주도**: slant·모듈 κ-인자의 관례를 문헌 공식으로 신뢰하지
않고, **대수 결합법칙(64³ 전수)·모듈 공리(전수)·modular 공리(유니터리/Verlinde)** 가 통과하는
관례만 채택 — 관례 오류가 원천 차단된다.

관측 6축(전부 exact: GF(2) + ℤ[ζ₈] Fraction 산술):
  A. **H³(D₄,μ₂)=𝔽₂⁴ bar-resolution 자체유도**: 정규화 cochain C³(343)→C⁴, rank d³=298 →
     dim Z³=45·dim B³=41 → **dim H³=4**(16 클래스) — TrackHE17 P4 값 재유도.
  B. ★**16 클래스 전수 반증**: 전 H³(D₄,μ₂) 클래스에서 **anyon 수 22 고정**(섹터 [5,4,5,4,4]) —
     slant β_a 가 어느 centralizer 에도 nontrivial 사영류를 유도하지 않음(β-regular 전수). ⟹
     report17/18 의 "anyon 22→19→16 ω-가변" 주장 **반증**(μ₂ 계수 한정). ★TrackHE17 P4 의
     "22/19/16 재현"은 **조건부 Schur-collapse**(β nontrivial 이면 4→1)였지 실제 ω-slant 유도가
     아니었음 — 본 관측이 그 갭을 메우고 정정.
  C. **관례 기계확정**: D^ω(G) 곱 (δ_a⊗x)(δ_b⊗y)=[a=xbx⁻¹](−1)^{θ_a(x,y)}δ_a⊗xy 의 slant 를
     **product-flux θ_a variant 만** 결합법칙 64³ 전수 통과로 확정(θ_b variant 는 실패). 모듈
     κ=(−1)^{θ_g(x,t_i)+θ_g(t_j,c)} 도 모듈 공리 전수(64² 대수쌍×전 기저) 통과. Σdim²=64(정칙 완비).
  D. ★**완전 22×22 twisted S·T**: S̃_{IJ}=Σ_{g,h}tr_I(δ_{hgh⁻¹}⊗h)tr_J(δ_h⊗g), S=S̃/8. **gates:
     S 대칭·SS†=I(유니터리)·S²=C(순열·C²=1)·(ST)³=λS²·Verlinde N_{IJK} 전수 비음정수(22³)·
     S_vac,vac=1/8(D²=64)·d 전부 양의 정수 {1×8, 2×14}** — untwisted·twisted 모두 통과.
  E. ★**twist 검출 = T-스펙트럼**: anyon 수 22 불변에도 **untwisted T∈ζ₄({±1,±i}) vs twisted
     T∋ζ₈(e^{±iπ/4})** — ribbon z=Σδ_a⊗a 스칼라(Schur 전수). ζ₈ 은 **r-sector(ℤ₄ centralizer,
     λ⁴=Πβ(r,r^k)=−1)** 에서 유래 — agent 예상("ℤ₂² quaternionic 유래") **정정**.
  F. **16 클래스 T-스펙트럼 층화**(full): ζ₈ 등장 클래스 수 계수 — anyon-count 대신 spins 가
     ω-불변량(μ₂ 계수의 진짜 가변 지표).

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - **μ₂ 계수 한정**: H³(D₄,U(1))≅ℤ₄×ℤ₂² 의 **ℤ₄ 성분(order-4 twist)은 μ₂ 로 실현 불가** — 그
    성분에서 anyon 수 19/16 이 가능한지는 **미해결=다음**(본 반증은 μ₂-twist 에 대한 것).
  - T-스펙트럼 동일 클래스가 U(1)-자명인지의 완전 판별(모듈러 데이터 동형)은 별도.
  - braiding 게이트 실봉인 무주장 — modular data 조합·대수 관측.

사용: python -m qf_witness.observe.dtw_d4_full_modular_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import itertools
from fractions import Fraction


# ── D₄ ──────────────────────────────────────────────────────────────────────
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
CLASS_REPS = [0, 1, 2, 4, 5]        # e, r, r², s, sr


# ── ℤ[ζ₈] ───────────────────────────────────────────────────────────────────
class C8:
    __slots__ = ("c",)

    def __init__(s, c):
        s.c = tuple(Fraction(x) for x in c)

    @staticmethod
    def zeta(k):
        k %= 8
        c = [0, 0, 0, 0]
        if k < 4:
            c[k] = 1
        else:
            c[k - 4] = -1
        return C8(c)

    @staticmethod
    def zero():
        return C8((0, 0, 0, 0))

    @staticmethod
    def one():
        return C8((1, 0, 0, 0))

    def __add__(a, b):
        return C8(tuple(x + y for x, y in zip(a.c, b.c)))

    def __neg__(a):
        return C8(tuple(-x for x in a.c))

    def __mul__(a, b):
        r = [Fraction(0)] * 4
        for i, x in enumerate(a.c):
            if x == 0:
                continue
            for j, y in enumerate(b.c):
                if y == 0:
                    continue
                k = i + j
                v = x * y
                if k >= 4:
                    k -= 4
                    v = -v
                r[k] += v
        return C8(r)

    def conj(a):
        c0, c1, c2, c3 = a.c
        return C8((c0, -c3, -c2, -c1))

    def scale(a, f):
        return C8(tuple(x * Fraction(f) for x in a.c))

    def __eq__(a, b):
        return a.c == b.c

    def __hash__(a):
        return hash(a.c)

    def is_zero(a):
        return all(x == 0 for x in a.c)

    def has_odd_zeta8(a):
        return any(x != 0 for i, x in enumerate(a.c) if i % 2 == 1)


ZP = [C8.zeta(k) for k in range(8)]


# ── H³(D₄,μ₂) bar resolution ────────────────────────────────────────────────
def compute_h3():
    NE = [g for g in range(8) if g != E]
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
    pairs = list(itertools.product(NE, repeat=2))
    for (b1, b2) in pairs:
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

    def rref(checks):
        piv = {}
        for r in checks:
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
        return piv

    piv = rref(rows)
    pivset = set(piv)
    N = 343
    ker = []
    for f in range(N):
        if f in pivset:
            continue
        v = 1 << f
        for p, r in piv.items():
            if (r >> f) & 1:
                v |= (1 << p)
        ker.append(v)
    b3basis = gf2_basis(img_vecs)

    def reduce_by(v, basis):
        for b in basis:
            v = min(v, v ^ b)
        return v

    h3basis = []
    b3ext = list(b3basis)
    for v in ker:
        w = reduce_by(v, b3ext)
        if w:
            h3basis.append(v)
            b3ext.append(w)
            b3ext.sort(reverse=True)
        if len(h3basis) == 4:
            break
    return tri_idx, rows, len(ker), len(b3basis), h3basis


# ── ω / slant ───────────────────────────────────────────────────────────────
def make_omega(v, tri_idx):
    def w(g1, g2, g3):
        if g1 == E or g2 == E or g3 == E:
            return 0
        return (v >> tri_idx[(g1, g2, g3)]) & 1
    return w


def make_slant(w):
    def th(a, x, y):
        return (w(a, x, y) ^ w(x, conj(a, INV[x]), y)
                ^ w(x, y, conj(a, INV[mul(x, y)]))) & 1
    return th


def anyon_parts(v, tri_idx):
    w = make_omega(v, tri_idx)
    th = make_slant(w)
    parts = []
    for a in CLASS_REPS:
        C = CENT[a]
        beta = {(x, y): th(a, x, y) for x in C for y in C}

        def breg(g):
            return all(beta[(g, h)] == beta[(h, g)] for h in C if mul(g, h) == mul(h, g))
        cls, sn = [], set()
        for g in C:
            if g in sn:
                continue
            cc = sorted({conj(g, x) for x in C})
            cls.append(cc)
            sn |= set(cc)
        parts.append(sum(1 for cc in cls if breg(cc[0])))
    return parts


# ── 사영 irrep 구성기 (생성원 브루트 + 재귀 + 전수검증) ─────────────────────
def matmul(A, B):
    n = len(A)
    m = len(B[0])
    k = len(B)
    return [[sum((A[i][t] * B[t][j] for t in range(k)), C8.zero())
             for j in range(m)] for i in range(n)]


def proj_irreps(C, beta):
    n = len(C)
    sign = lambda x, y: (-1) ** beta[(x, y)]
    Cset = set(C)

    def gen_span(gens):
        S = {E}
        fr = [E]
        while fr:
            nf = []
            for g in list(S):
                for h in gens:
                    p = mul(g, h)
                    if p not in S:
                        S.add(p)
                        nf.append(p)
            fr = nf
        return S

    gens = None
    for g in C:
        if gen_span([g]) == Cset:
            gens = [g]
            break
    if gens is None:
        for g, h in itertools.product(C, repeat=2):
            if gen_span([g, h]) == Cset:
                gens = [g, h]
                break
    word = {E: []}
    fr = [E]
    while fr:
        nf = []
        for c in fr:
            for gi, g in enumerate(gens):
                p = mul(c, g)
                if p not in word:
                    word[p] = word[c] + [gi]
                    nf.append(p)
        fr = nf
    irreps = []
    for lam in itertools.product(range(8), repeat=len(gens)):
        rho = {E: ZP[0]}
        ok = True
        for c in C:
            if c == E:
                continue
            val = ZP[0]
            cur = E
            for gi in word[c]:
                g = gens[gi]
                val = val * ZP[lam[gi]]
                if sign(cur, g) < 0:
                    val = -val
                cur = mul(cur, g)
            rho[c] = val
        for x in C:
            for y in C:
                lhs = rho[x] * rho[y]
                rhs = rho[mul(x, y)] if sign(x, y) > 0 else -rho[mul(x, y)]
                if lhs != rhs:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            M = {c: [[rho[c]]] for c in C}
            if not any(all(irr[c][0][0] == rho[c] for c in C)
                       for irr in irreps if len(irr[E]) == 1):
                irreps.append(M)
    need = n - len(irreps)
    if need > 0:
        Hl = None
        for Hgen in itertools.product(C, repeat=2):
            H = gen_span(list(Hgen))
            if len(H) == n // 2 and all(mul(a, b) == mul(b, a) for a in H for b in H):
                Hl = sorted(H)
                break
        H = set(Hl)
        betaH = {(x, y): beta[(x, y)] for x in Hl for y in Hl}
        subs = [s for s in proj_irreps(Hl, betaH) if len(s[E]) == 1]
        t1 = [c for c in C if c not in H][0]
        T = [E, t1]
        for psi in subs:
            def pmat(g):
                M = [[C8.zero() for _ in range(2)] for _ in range(2)]
                for i, ti in enumerate(T):
                    gt = mul(g, ti)
                    j, h = (0, gt) if gt in H else (1, mul(INV[t1], gt))
                    v = psi[h][0][0]
                    s = sign(g, ti) * sign(T[j], h)
                    M[j][i] = v if s > 0 else -v
                return M
            P = {c: pmat(c) for c in C}
            ok = True
            for x in C:
                for y in C:
                    L = matmul(P[x], P[y])
                    Rm = P[mul(x, y)]
                    sg = sign(x, y)
                    for r in range(2):
                        for cc in range(2):
                            expect = Rm[r][cc] if sg > 0 else -Rm[r][cc]
                            if L[r][cc] != expect:
                                ok = False
            if not ok:
                continue
            ip = C8.zero()
            for c in C:
                ch = P[c][0][0] + P[c][1][1]
                ip = ip + ch * ch.conj()
            if ip == C8.one().scale(n):
                ch_new = {c: P[c][0][0] + P[c][1][1] for c in C}
                dup = any(len(irr[E]) == 2 and all(
                    (irr[c][0][0] + irr[c][1][1]) == ch_new[c] for c in C)
                    for irr in irreps)
                if not dup:
                    irreps.append(P)
    assert sum(len(m[E]) ** 2 for m in irreps) == n
    return irreps


# ── 모듈 구성 ───────────────────────────────────────────────────────────────
def build_modules(v, tri_idx):
    w = make_omega(v, tri_idx)
    th = make_slant(w)
    mods = []
    for a in CLASS_REPS:
        C = CENT[a]
        Cset = set(C)
        T = []
        covered = set()
        for g in range(8):
            if g not in covered:
                T.append(g)
                covered |= {mul(g, c) for c in C}
        beta = {(x, y): th(a, x, y) for x in C for y in C}
        irr = proj_irreps(C, beta)
        for ci, rho in enumerate(irr):
            d = len(rho[E])
            flux = [conj(a, t) for t in T]
            act = {}
            for g in range(8):
                for x in range(8):
                    m = {}
                    for i, ti in enumerate(T):
                        if conj(flux[i], x) != g:
                            continue
                        xt = mul(x, ti)
                        for j, tj in enumerate(T):
                            c = mul(INV[tj], xt)
                            if c in Cset:
                                break
                        s = (-1) ** (th(g, x, ti) ^ th(g, tj, c))
                        for k in range(d):
                            for k2 in range(d):
                                cf = rho[c][k2][k]
                                if cf.is_zero():
                                    continue
                                m.setdefault(i * d + k, []).append(
                                    (j * d + k2, cf if s > 0 else -cf))
                    act[(g, x)] = m
            mods.append((f"({a},{ci})", len(T) * d, act))
    return mods


def apply_op(act, g, x, vec, dim):
    out = [C8.zero()] * dim
    for colv, entries in act[(g, x)].items():
        cf0 = vec[colv]
        if cf0.is_zero():
            continue
        for (row, cf) in entries:
            out[row] = out[row] + cf * cf0
    return out


# ── 검증 스위트 ─────────────────────────────────────────────────────────────
def algebra_assoc(v, tri_idx, variant, quick=False):
    w = make_omega(v, tri_idx)
    th = make_slant(w)

    def prod(a, x, b, y):
        if a != conj(b, x):
            return None
        t = th(a, x, y) if variant == "a" else th(b, x, y)
        return ((-1) ** t, a, mul(x, y))
    rng = range(0, 8, 2) if quick else range(8)
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
                        lhs = (s1 * q[0], q[1], q[2])
                rhs = None
                if p2 is not None:
                    s2, bb, yz = p2
                    q = prod(a, x, bb, yz)
                    if q is not None:
                        rhs = (s2 * q[0], q[1], q[2])
                if lhs != rhs:
                    return False
    return True


def module_assoc(mods, v, tri_idx, quick=False):
    w = make_omega(v, tri_idx)
    th = make_slant(w)
    step = 2 if quick else 1
    for (lab, dim, act) in mods:
        for a1, x1 in itertools.product(range(0, 8, step), repeat=2):
            for b1, y1 in itertools.product(range(8), repeat=2):
                for j in range(dim):
                    vec = [C8.one() if i == j else C8.zero() for i in range(dim)]
                    bv = apply_op(act, b1, y1, vec, dim)
                    lhs = apply_op(act, a1, x1, bv, dim)
                    if conj(b1, x1) == a1:
                        s = (-1) ** th(a1, x1, y1)
                        rhs = apply_op(act, a1, mul(x1, y1), vec, dim)
                        if s < 0:
                            rhs = [-zz for zz in rhs]
                    else:
                        rhs = [C8.zero()] * dim
                    if any(l != r for l, r in zip(lhs, rhs)):
                        return False
    return True


def full_modular(v, tri_idx, quick=False):
    mods = build_modules(v, tri_idx)
    n = len(mods)
    R = {}
    R["n_22"] = (n == 22)
    R["sum_dim2_64"] = (sum(d * d for _, d, _ in mods) == 64)
    TR = []
    for (lab, dim, act) in mods:
        t = {}
        for g in range(8):
            for x in range(8):
                s = C8.zero()
                for col, entries in act[(g, x)].items():
                    for (row, cf) in entries:
                        if row == col:
                            s = s + cf
                t[(g, x)] = s
        TR.append(t)
    S = [[C8.zero() for _ in range(n)] for _ in range(n)]
    for I in range(n):
        for J in range(n):
            acc = C8.zero()
            for g in range(8):
                for h in range(8):
                    a = TR[I][(conj(g, h), h)]
                    if a.is_zero():
                        continue
                    b = TR[J][(h, g)]
                    if b.is_zero():
                        continue
                    acc = acc + a * b
            S[I][J] = acc.scale(Fraction(1, 8))
    vac = None
    for I in range(n):
        if all(TR[I][(g, x)] == (C8.one() if g == E else C8.zero())
               for g in range(8) for x in range(8)):
            vac = I
            break
    R["vacuum_found"] = (vac is not None)
    theta = []
    ribbon_ok = True
    for (lab, dim, act) in mods:
        th0 = None
        for j in range(dim):
            vec = [C8.one() if i == j else C8.zero() for i in range(dim)]
            out = [C8.zero()] * dim
            for a in range(8):
                o = apply_op(act, a, a, vec, dim)
                out = [p + q for p, q in zip(out, o)]
            if th0 is None:
                th0 = out[j]
            for i in range(dim):
                expect = th0 if i == j else C8.zero()
                if out[i] != expect:
                    ribbon_ok = False
        theta.append(th0)
    R["ribbon_scalar"] = ribbon_ok
    R["S_symmetric"] = all(S[i][j] == S[j][i] for i in range(n) for j in range(n))

    def mm(A, B, conjB=False):
        return [[sum((A[i][k] * (B[j][k].conj() if conjB else B[k][j])
                      for k in range(n)), C8.zero())
                 for j in range(n)] for i in range(n)]
    SSd = mm(S, S, conjB=True)
    R["S_unitary"] = all(SSd[i][j] == (C8.one() if i == j else C8.zero())
                         for i in range(n) for j in range(n))
    S2 = mm(S, S)
    permOK = True
    perm = []
    for i in range(n):
        nz = [j for j in range(n) if not S2[i][j].is_zero()]
        if len(nz) != 1 or S2[i][nz[0]] != C8.one():
            permOK = False
            break
        perm.append(nz[0])
    R["S2_charge_conj"] = permOK
    R["C2_id"] = permOK and all(perm[perm[i]] == i for i in range(n))
    Svv = S[vac][vac]
    R["S_vac_vac_1_8"] = (Svv == C8.one().scale(Fraction(1, 8)))
    dd = [S[vac][I].scale(8) for I in range(n)]
    R["sum_d2_64_S"] = (sum((d * d for d in dd), C8.zero()) == C8.one().scale(64))
    R["dims_pos_int"] = all(all(x == 0 for i, x in enumerate(d.c) if i > 0)
                            and d.c[0] > 0 and d.c[0].denominator == 1 for d in dd)
    Tm = [[(theta[i] if i == j else C8.zero()) for j in range(n)] for i in range(n)]
    ST = mm(S, Tm)
    ST3 = mm(mm(ST, ST), ST)
    lam = None
    for i in range(n):
        for j in range(n):
            if S2[i][j] == C8.one():
                lam = ST3[i][j]
                break
        if lam is not None:
            break
    R["ST3_prop_S2"] = (lam is not None and all(
        ST3[i][j] == lam * S2[i][j] for i in range(n) for j in range(n)))
    verl_ok = True
    trip = itertools.product(range(n), repeat=3)
    if quick:
        trip = [(i, j, k) for i in range(0, n, 3) for j in range(0, n, 3)
                for k in range(0, n, 3)]
    for (i, j, k) in trip:
        acc = C8.zero()
        for L in range(n):
            invS = C8.one().scale(Fraction(1, 1) / S[vac][L].c[0])
            acc = acc + S[i][L] * S[j][L] * S[k][L].conj() * invS
        cc = acc.c
        if any(cc[t] != 0 for t in (1, 2, 3)) or cc[0].denominator != 1 or cc[0] < 0:
            verl_ok = False
    R["verlinde_nonneg_int"] = verl_ok
    z8 = any(t.has_odd_zeta8() for t in theta)
    return R, theta, z8, [str(d.c[0]) for d in dd]


def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "dtw-d4-full-modular/v1",
           "_note": ("D^ω(D₄) 완전 22×22 twisted S·T + 16 클래스 전수 anyon-count 반증 — "
                     "관측·seal 아님·module 0·root 불변. 관례=기계검증 주도(결합/모듈공리/modular "
                     "게이트 전수). μ₂ 계수 한정(U(1) ℤ₄ 성분 미커버=다음).")}

    # A. H³
    tri_idx, rows, dimZ3, dimB3, h3basis = compute_h3()
    R["A_dimZ3_45"] = (dimZ3 == 45)
    R["A_dimB3_41"] = (dimB3 == 41)
    R["A_dimH3_4"] = (dimZ3 - dimB3 == 4 and len(h3basis) == 4)
    out["H3"] = {"dim_Z3": dimZ3, "dim_B3": dimB3, "dim_H3": dimZ3 - dimB3,
                 "classes": 16}

    # B. 16 클래스 전수 anyon counts
    h3reps = []
    for mask in range(16):
        v = 0
        for k in range(4):
            if (mask >> k) & 1:
                v ^= h3basis[k]
        h3reps.append(v)
    counts = [sum(anyon_parts(v, tri_idx)) for v in h3reps]
    R["B_all_22"] = all(c == 22 for c in counts)
    R["B_refutes_19_16"] = (19 not in counts and 16 not in counts)
    out["anyon_census"] = {
        "all_16_classes": counts,
        "verdict": "★전 클래스 22 고정 — report17/18 'anyon 22→19→16 ω-가변' 반증(μ₂ 한정)",
        "correction": "TrackHE17 P4 의 22/19/16 재현은 조건부 Schur-collapse 였음 — slant 는 "
                      "nontrivial 사영류를 유도하지 않음",
    }

    # C. 관례 기계확정
    vt = h3basis[0]
    R["C_assoc_theta_a"] = algebra_assoc(vt, tri_idx, "a", quick=quick)
    # θ_b 반증은 반례 1건이면 충분 — 전범위(short-circuit 로 즉시 False)
    R["C_assoc_theta_b_fails"] = (not algebra_assoc(vt, tri_idx, "b", quick=False))
    mods_t = build_modules(vt, tri_idx)
    R["C_module_assoc"] = module_assoc(mods_t, vt, tri_idx, quick=quick)

    # D/E. 완전 modular data — untwisted + twisted
    R0, th0, z80, dims0 = full_modular(0, tri_idx, quick=quick)
    R1, th1, z81, dims1 = full_modular(vt, tri_idx, quick=quick)
    for k, val in R0.items():
        R[f"D_untw_{k}"] = val
    for k, val in R1.items():
        R[f"D_tw_{k}"] = val
    R["E_untwisted_no_zeta8"] = (not z80)
    R["E_twisted_zeta8"] = z81
    out["modular_data"] = {
        "dims_untwisted": dims0, "dims_twisted": dims1,
        "T_zeta8_untwisted": z80, "T_zeta8_twisted": z81,
        "verdict": "★anyon 수 22 불변에도 twist 가 T-스펙트럼 ζ₄→ζ₈ 로 검출(r-sector ℤ₄ 유래 — "
                   "agent 'ℤ₂² quaternionic 유래' 예상 정정)",
    }

    # F. 16 클래스 T-스펙트럼 층화 (full 만)
    if not quick:
        z8_classes = []
        for mask, v in enumerate(h3reps):
            _, thv, z8v, _ = full_modular(v, tri_idx, quick=True)
            if z8v:
                z8_classes.append(mask)
        R["F_zeta8_strata_nonempty"] = (len(z8_classes) > 0)
        R["F_mask0_not_zeta8"] = (0 not in z8_classes)
        out["T_spectrum_census"] = {"zeta8_classes": z8_classes,
                                    "count": len(z8_classes),
                                    "note": "spins 가 μ₂-twist 의 진짜 가변 지표(anyon 수 아님)"}

    # teeth
    R["teeth_gates_all"] = all(v for k, v in R.items() if k.startswith("D_"))
    R["teeth_refutation"] = R["B_all_22"]
    R["teeth_zeta8_detect"] = (z81 and not z80)

    ok = bool(all(R.values()))
    out["checks"] = R
    out["scope_honesty"] = {
        "delivered": "완전 22×22 twisted S·T(전 modular 게이트)·16클래스 전수 반증·ζ₈ 검출",
        "mu2_only": "H³(D₄,U(1))≅ℤ₄×ℤ₂² 의 ℤ₄ 성분(order-4 twist)은 μ₂ 실현 불가 — 19/16 층 "
                    "가능성은 U(1) 완전판=다음",
        "method": "관례 전부 기계확정(결합 64³·모듈공리·modular 게이트) — 문헌 공식 무인용",
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "DTW-D4-FULL-MODULAR.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("D^ω(D₄) 완전 22×22 twisted modular data (exact — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  ★16 클래스 전수 anyon 22 고정 — 'ω-가변 22/19/16' 반증(μ₂ 한정)", flush=True)
        print("  ★완전 22×22 S: 유니터리·S²=C·(ST)³∝S²·Verlinde 비음정수·D²=64", flush=True)
        print("  ★twist 검출=T-스펙트럼 ζ₄→ζ₈(r-sector ℤ₄ 유래)", flush=True)
        print("  → .pgf/proofs/DTW-D4-FULL-MODULAR.json", flush=True)
    print(f"dtw_d4_full_modular_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
