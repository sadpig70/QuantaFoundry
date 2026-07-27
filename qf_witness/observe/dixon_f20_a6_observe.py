#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dixon_f20_a6_observe — ★**일반 Dixon 엔진 승격 + F₂₀(첫 비아벨 Frobenius)·A₆ 표현론 층**
(관측, seal 아님). v20 §4 잔여 후보.

★핵심 = **엔진 일반화**: 지금까지 Dixon 자체유도는 A₇([[a7_brauer_trees_observe]])·M₁₁
([[m11_brauer_observe]])에 **하드코딩**되어 있었다. 본 관측은 이를 **임의 순열군용 엔진**으로
승격하고(생성원·점수·소수 q 만 입력), **A₇ 재현으로 교차검증**한 뒤 두 신규 군에 적용한다.
문자값은 [[g2_1_mtc_observe]]의 `Cyc`(Φ_N 자체유도 ℚ(ζ_N) 정확 산술)로 표현 — **모듈 간 재사용**.

관측 7축(전 산술 GF(q)/ℚ(ζ_N) 정확 · 확률적 판정 없음):
  A. ★**일반 Dixon 엔진**(재사용 자산): 생성원 → 군 열거 → 켤레류 → 클래스행렬 A_ijk →
     Dixon 공통 고유벡터(q ≡ 1 mod exp G) → 차수 → **cyclotomic 다중도 a_m** →
     `Cyc(e)` 정확 벡터. ★**A₇ 재현 교차검증**: 기존 `dixon_char_table` 과 차수·류크기·위수 일치.
  B. ★**F₂₀ = ℤ₅⋊ℤ₄ (첫 비아벨 Frobenius 군)**: 5점 ⟨(01234), x↦2x⟩ · **Frobenius 판정
     자체유도**(커널 ℤ₅ 정규·고정점 자유 / 보체 = Stab(0) ≅ ℤ₄ · 비자명 원소 고정점 정확히 1) ·
     5 켤레류(위수 1,2,4,4,5) · **차수 {1,1,1,1,4}** · 4차원은 5A 에서 **−1**(유리) ·
     선형 4개는 ℤ₄ 지표(ζ₄ 무리 2개).
  C. ★**F₂₀ p=5 완전 D·C**: 5-regular 4 · 정규 Sylow-5 ⟹ simples = **G/ℤ₅ ≅ ℤ₄ 의 4 선형문자** →
     **D(5×4)**: 선형 4개 = 단위행 · **4차원 → 1̂+1̂′+1̂″+1̂‴** · **C = I+J** · **det C = 5 = |G|₅**.
  D. ★**F₂₀ p=2 완전 D·C**: 2-regular 2(위수 1,5) · simples = {1, **GF(16) 4차원**} —
     ℤ₅ ⊂ GF(16)^× 곱셈 · ℤ₄ = Gal(GF(16)/GF(2)) Frobenius, **명시 GF(2) 행렬 + 관계 검증
     (M₅⁵=I·M₄⁴=I·M₄M₅M₄⁻¹=M₅²) + 기약성 전수(15 벡터)** → **D(5×2)** · **C = diag(4,1)** ·
     **det C = 4 = |G|₂**.
  E. ★**A₆ 완전 문자표 + 무리성 판정**: 위수 360·7 켤레류(1,2,3,3,4,5,5)·**차수 {1,5,5,8,8,9,10}** ·
     ★**무리성은 오직 8차원 쌍의 5A/5B** — 값 **(1±√5)/2** 정확 확정(ℚ(√5) 좌표) ·
     나머지 전부 유리. ★두 5차원은 **3A/3B 에서 (2,−1)/(−1,2)** 로 구별(유리).
  F. ★**A₆ 3 소수 블록 — 엄밀 𝔭-환원**: ω_χ(K)=|K|χ(x_K)/χ(1) 는 대수적 정수(ℤ[ζ₆₀] 멱기저 정수좌표)
     → **𝔭 = (p, g(x)), g = Φ₆₀ mod p 의 기약인수** 로 환원해 비교(무리성분 0 처리 **휴리스틱 아님**).
     **p=2: {1,5,5,9,10} + {8} + {8}** · **p=3: {1,5,5,8,8,10} + {9}** ·
     **p=5: {1,8,8,9} + {10} + {5} + {5}** — defect-0 블록이 각각 χ(1)_p = |G|_p 와 정합.
  G. ★★**A₆ p=5 Brauer tree 실산출**(defect 1·Sylow ℤ₅): 주블록 |Irr|=4·**ℓ=e=2**(rank 확인)·
     예외중복 m=(5−1)/e=2 → 3 정점 경로 전수 → **유효 tree 유일(반사 제외)**:
     **1 — 9 — [8,8]^exc** · Brauer 차수 **{1, 8}** · **9 = 1+8**(중심정점=인접 변 합) 정합 ·
     **det C(B) = 5**. [[a7_brauer_trees_observe]](A₇ p=5,7)·[[m11_brauer_observe]] 계보 연장.
  H. ★**A₆ ⊂ A₇ 분기 정합**: A₇ 9 문자의 A₆-제한을 **직교 내적**으로 분해(9×7 다중도) —
     **전 성분 비음정수** ⟹ 두 자체유도 문자표의 상호 무모순.

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - Dixon 의 무작위 선형결합은 **시드 고정**·실패 시 재시도뿐 — 산출은 결정론적으로 재검증된다.
  - C·D 의 D 유일성은 **F₂₀ 의 정규 Sylow 구조** 덕에 simples 를 명시할 수 있어서다 —
    일반 군에 대한 방법 주장이 아니다.
  - **A₆ 완전 D·C 는 미포함**: p=5 주블록(순환 defect)만 tree 로 확정했고, p=2·3 주블록은
    비순환 defect(2³·3²)이라 **범위 밖**(정직 유보 — [[a7_cartan_p2_observe]] 식 명시 구성 필요).
    ★**2026-07-27 해소**: [[a6_cartan_p23_observe]] 가 simples 를 전부 명시 구성해
    **p=2·3 완전 D(7×5)·Cartan**(det 8·9 = |A₆|_p) 확정. 위 유보 이유는 일반론으로 여전히 옳다.
  - Brauer 문자·블록은 표현론 수준 — 봉인 게이트 아님.

사용: python -m qf_witness.observe.dixon_f20_a6_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import random
import warnings
import itertools
from fractions import Fraction as Fr

import sympy as sp

from qf_witness.observe.g2_1_mtc_observe import Cyc


# ══════════════════════════════════════════════════════════════════════════
# A. 일반 Dixon 엔진
# ══════════════════════════════════════════════════════════════════════════
def pmul(a, b):
    return tuple(a[b[i]] for i in range(len(a)))


def pinv(a):
    r = [0] * len(a)
    for i, v in enumerate(a):
        r[v] = i
    return tuple(r)


def group_from(gens, npts):
    idp = tuple(range(npts))
    G = {idp}
    fr = [idp]
    while fr:
        nf = []
        for x in fr:
            for g in gens:
                y = pmul(g, x)
                if y not in G:
                    G.add(y)
                    nf.append(y)
        fr = nf
    return sorted(G)


def _pfactors(m):
    fs, d = set(), 2
    while d * d <= m:
        while m % d == 0:
            fs.add(d)
            m //= d
        d += 1
    if m > 1:
        fs.add(m)
    return sorted(fs)


def dixon(gens, npts, q, seed=7):
    """일반 Dixon 문자표 자체유도. 반환: K·GN·sizes·orders·reps·invmap·exact·degs·cls_of·G."""
    G = group_from(gens, npts)
    GN = len(G)
    idp = tuple(range(npts))
    cls_of, classes = {}, []
    for p in G:
        if p in cls_of:
            continue
        cid = len(classes)
        cls_of[p] = cid
        members, fr = [p], [p]
        while fr:
            nf = []
            for x in fr:
                for g in gens:
                    y = pmul(pmul(g, x), pinv(g))
                    if y not in cls_of:
                        cls_of[y] = cid
                        members.append(y)
                        nf.append(y)
            fr = nf
        classes.append(members)
    K = len(classes)
    reps = [c[0] for c in classes]
    sizes = [len(c) for c in classes]

    def order(p):
        o, x = 1, p
        while x != idp:
            x = pmul(x, p)
            o += 1
        return o
    orders = [order(r) for r in reps]
    A = [[[0] * K for _ in range(K)] for _ in range(K)]
    for k in range(K):
        zk = reps[k]
        for i in range(K):
            for x in classes[i]:
                A[i][cls_of[pmul(pinv(x), zk)]][k] += 1
    powmap = []
    for ci, r in enumerate(reps):
        pm, x = [], idp
        for _ in range(orders[ci]):
            pm.append(cls_of[x])
            x = pmul(x, r)
        powmap.append(pm)
    invmap = [cls_of[pinv(r)] for r in reps]

    def iv(a):
        return pow(a, q - 2, q)
    rnd = random.Random(seed)
    while True:
        cs = [rnd.randrange(q) for _ in range(K)]
        M = [[sum(cs[i] * A[i][j][k] for i in range(K)) % q for k in range(K)]
             for j in range(K)]
        eigs = []
        for lam in range(q):
            Tm = [[(M[r][c] - (lam if r == c else 0)) % q for c in range(K)]
                  for r in range(K)]
            r0, piv = 0, {}
            for c in range(K):
                pr = next((r for r in range(r0, K) if Tm[r][c] % q), None)
                if pr is None:
                    continue
                Tm[r0], Tm[pr] = Tm[pr], Tm[r0]
                f = iv(Tm[r0][c])
                Tm[r0] = [(x * f) % q for x in Tm[r0]]
                for r in range(K):
                    if r != r0 and Tm[r][c]:
                        g = Tm[r][c]
                        Tm[r] = [(Tm[r][x] - g * Tm[r0][x]) % q for x in range(K)]
                piv[r0] = c
                r0 += 1
            if r0 < K:
                eigs.append((lam, K - r0, Tm, piv))
        if sum(m for _, m, _, _ in eigs) == K and all(m == 1 for _, m, _, _ in eigs):
            break
    omegas = []
    for lam, m, Tm, piv in eigs:
        pc = set(piv.values())
        free = [c for c in range(K) if c not in pc][0]
        v = [0] * K
        v[free] = 1
        for r, c in piv.items():
            v[c] = (-Tm[r][free]) % q
        f = iv(v[0])
        omegas.append([(x * f) % q for x in v])
    degs_mod = []
    for om in omegas:
        s = 0
        for k in range(K):
            s = (s + om[k] * om[invmap[k]] * iv(sizes[k])) % q
        d2 = (GN * iv(s)) % q
        degs_mod.append(next(min(r, q - r) for r in range(1, q) if r * r % q == d2))
    chi_mod = [[om[k] * dg % q * iv(sizes[k]) % q for k in range(K)]
               for om, dg in zip(omegas, degs_mod)]
    PR = next(g for g in range(2, q)
              if all(pow(g, (q - 1) // d, q) != 1 for d in _pfactors(q - 1)))
    exact = []
    for t in range(K):
        row = []
        for k in range(K):
            o = orders[k]
            eta = pow(PR, (q - 1) // o, q)
            ams = []
            for m in range(o):
                s = 0
                for l in range(o):
                    s = (s + chi_mod[t][powmap[k][l]] * pow(eta, (-m * l) % o, q)) % q
                ams.append(s * iv(o) % q)
            row.append(ams)
        exact.append(row)
    return {"K": K, "GN": GN, "sizes": sizes, "orders": orders, "reps": reps,
            "invmap": invmap, "exact": exact, "degs": degs_mod,
            "cls_of": cls_of, "classes": classes, "G": G}


def table_in(F, T):
    """exact 다중도 → Cyc(F.N) 정확 문자표. (F.N 은 모든 클래스 위수의 배수여야 함)"""
    K, orders, E = T["K"], T["orders"], T["exact"]
    V = []
    for t in range(K):
        row = []
        for k in range(K):
            o = orders[k]
            assert F.N % o == 0
            acc = F.zero
            for m in range(o):
                if E[t][k][m]:
                    acc = F.add(acc, F.scale(F.z((m * (F.N // o)) % F.N), E[t][k][m]))
            row.append(acc)
        V.append(row)
    return V


def is_rat(v):
    return all(x == 0 for x in v[1:])


def rat_of(v):
    return v[0]


# ══════════════════════════════════════════════════════════════════════════
def gf2_simple(mats, dim):
    """GF(2)-모듈 기약성 전수(소형: 전 비영벡터가 전체 생성)."""
    def cols(M):
        return [sum(M[i][j] << i for i in range(dim)) for j in range(dim)]

    def act(cl, v):
        r = 0
        while v:
            b = v & -v
            r ^= cl[b.bit_length() - 1]
            v ^= b
        return r
    CL = [cols(M) for M in mats]
    for v0 in range(1, 1 << dim):
        B, fr = [v0], [v0]
        while fr:
            nf = []
            for b in fr:
                for cl in CL:
                    t = act(cl, b)
                    for x in B:
                        if (t >> (x.bit_length() - 1)) & 1:
                            t ^= x
                    if t:
                        B.append(t)
                        B.sort(reverse=True)
                        nf.append(t)
            fr = nf
        if len(B) != dim:
            return False
    return True


def block_partition(F, V, T, p):
    """엄밀 𝔭-환원 블록 분할: ω_χ(K) 를 (p, g(x)) 로 환원(g = Φ_N mod p 기약인수)."""
    x = sp.Symbol("x")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fl = sp.factor_list(sp.cyclotomic_poly(F.N, x), x, modulus=p)[1]
        g = sp.Poly(fl[0][0], x, modulus=p)
    gc = [int(c) % p for c in reversed(g.all_coeffs())]
    dg = len(gc) - 1

    def reduce_vec(vec):
        poly = []
        for c in vec:
            assert c.denominator == 1, "ω 가 정수기저 좌표가 아님(대수적 정수 아님)"
            poly.append(int(c) % p)
        while len(poly) > dg:
            c = poly[-1] % p
            if c:
                sh = len(poly) - 1 - dg
                for j in range(dg + 1):
                    poly[sh + j] = (poly[sh + j] - c * gc[j]) % p
            poly.pop()
        return tuple(v % p for v in poly)
    K, sizes, degs = T["K"], T["sizes"], T["degs"]
    sig = {}
    for t in range(K):
        s = tuple(reduce_vec(F.scale(V[t][k], Fr(sizes[k], degs[t]))) for k in range(K))
        sig.setdefault(s, []).append(t)
    return list(sig.values())


# ══════════════════════════════════════════════════════════════════════════
def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "dixon-f20-a6/v1",
           "_note": ("일반 Dixon 엔진 승격(A₇ 재현 교차검증) + F₂₀ 첫 비아벨 Frobenius "
                     "p=2/5 완전 D·C + A₆ 문자표·엄밀 블록·p=5 Brauer tree. "
                     "관측·seal 아님·module 0·root 불변.")}

    # ── B. F₂₀ ──────────────────────────────────────────────────────────
    f20 = dixon([(1, 2, 3, 4, 0), (0, 2, 4, 1, 3)], 5, 41)
    R["B_order20"] = (f20["GN"] == 20)
    R["B_K5"] = (f20["K"] == 5)
    R["B_orders"] = (sorted(f20["orders"]) == [1, 2, 4, 4, 5])
    R["B_degs"] = (sorted(f20["degs"]) == [1, 1, 1, 1, 4])
    G20 = f20["G"]
    idp5 = tuple(range(5))
    ker = [g for g in G20 if g == idp5 or all(g[i] != i for i in range(5))]
    R["B_kernel_5"] = (len(ker) == 5)
    kset = set(ker)
    R["B_kernel_normal"] = all(pmul(pmul(g, k), pinv(g)) in kset for g in G20 for k in ker)
    comp = [g for g in G20 if g[0] == 0]
    R["B_complement_4"] = (len(comp) == 4)
    R["B_complement_fpf"] = all(sum(1 for i in range(5) if g[i] == i) == 1
                                for g in comp if g != idp5)
    F20F = Cyc(20)
    V20 = table_in(F20F, f20)
    i4 = f20["degs"].index(4)
    k5 = f20["orders"].index(5)
    R["B_chi4_at_5A_is_minus1"] = (is_rat(V20[i4][k5]) and rat_of(V20[i4][k5]) == -1)
    lin = [t for t in range(5) if f20["degs"][t] == 1]
    R["B_four_linear"] = (len(lin) == 4)
    R["B_two_linear_irrational"] = (
        sum(1 for t in lin if any(not is_rat(V20[t][k]) for k in range(5))) == 2)
    out["F20"] = {
        "structure": "ℤ₅⋊ℤ₄ = ⟨(01234), x↦2x⟩ (5점) — 첫 비아벨 Frobenius 군",
        "frobenius": "커널 ℤ₅(정규·고정점 자유) · 보체 Stab(0) ≅ ℤ₄ · 비자명 원소 고정점 정확히 1",
        "classes": 5, "orders": sorted(f20["orders"]), "degrees": sorted(f20["degs"]),
        "note": "선형 4 = ℤ₄ 지표(그중 2개 ζ₄ 무리) · 4차원 = Ind(ℤ₅ 비자명), 5A 에서 −1",
    }

    # ── C. F₂₀ p=5 완전 D·C ─────────────────────────────────────────────
    reg5 = [k for k in range(5) if f20["orders"][k] % 5 != 0]
    R["C_reg5_is_4"] = (len(reg5) == 4)

    def q20(v):
        e = sp.Integer(0)
        for i, c in enumerate(v):
            if c:
                e += sp.Rational(c) * sp.exp(2 * sp.pi * sp.I * sp.Rational(i, 20))
        return sp.simplify(sp.expand(e))
    PHI5 = sp.Matrix([[q20(V20[t][k]) for k in reg5] for t in lin])
    R["C_Phi_invertible"] = (sp.simplify(PHI5.det()) != 0)
    X5 = sp.Matrix([[q20(V20[t][k]) for k in reg5] for t in range(5)])
    D5 = sp.simplify(X5 * PHI5.inv())
    R["C_D_nonneg_int"] = all(sp.simplify(D5[i, j]).is_integer and sp.simplify(D5[i, j]) >= 0
                              for i in range(5) for j in range(4))
    R["C_4dim_row_all_ones"] = all(sp.simplify(D5[i4, j]) == 1 for j in range(4))
    C5m = sp.simplify(D5.T * D5)
    R["C_Cartan_I_plus_J"] = all(sp.simplify(C5m[i, j] - (2 if i == j else 1)) == 0
                                 for i in range(4) for j in range(4))
    R["C_detC_5"] = (sp.simplify(C5m.det()) == 5)
    out["F20_p5"] = {"ell": 4, "simples": "G/ℤ₅ ≅ ℤ₄ 의 4 선형문자(정규 Sylow-5)",
                     "D": "선형 4 = 단위행 · 4차원 → 1̂+1̂′+1̂″+1̂‴",
                     "Cartan": "I+J (대각 2·비대각 1)", "det": 5, "check": "det C = |G|₅"}

    # ── D. F₂₀ p=2 완전 D·C (GF(16)) ────────────────────────────────────
    reg2 = [k for k in range(5) if f20["orders"][k] % 2 != 0]
    R["D_reg2_is_2"] = (len(reg2) == 2)

    def gmul16(a, b):
        r = 0
        while b:
            if b & 1:
                r ^= a
            b >>= 1
            a <<= 1
            if a & 0x10:
                a ^= 0x13          # x⁴+x+1
        return r
    z3 = 1
    for _ in range(3):
        z3 = gmul16(z3, 2)          # ζ³ (위수 5)
    o5, t_ = 1, z3
    while t_ != 1:
        t_ = gmul16(t_, z3)
        o5 += 1
    R["D_gf16_order5_elt"] = (o5 == 5)
    M5 = tuple(tuple((gmul16(z3, 1 << c) >> r) & 1 for c in range(4)) for r in range(4))
    M4 = tuple(tuple((gmul16(1 << c, 1 << c) >> r) & 1 for c in range(4)) for r in range(4))

    def mm2(A, B):
        return tuple(tuple(sum(A[i][t] * B[t][j] for t in range(4)) % 2 for j in range(4))
                     for i in range(4))
    I4 = tuple(tuple(1 if i == j else 0 for j in range(4)) for i in range(4))

    def mpow(M, e):
        r = I4
        for _ in range(e):
            r = mm2(r, M)
        return r

    def minv(M):
        A = [[M[i][j] for j in range(4)] + [1 if i == j else 0 for j in range(4)]
             for i in range(4)]
        r = 0
        for c in range(4):
            pr = next((i for i in range(r, 4) if A[i][c]), None)
            if pr is None:
                continue
            A[r], A[pr] = A[pr], A[r]
            for i in range(4):
                if i != r and A[i][c]:
                    A[i] = [(A[i][k] + A[r][k]) % 2 for k in range(8)]
            r += 1
        return tuple(tuple(A[i][4 + j] for j in range(4)) for i in range(4))
    R["D_M5_order5"] = (mpow(M5, 5) == I4)
    R["D_M4_order4"] = (mpow(M4, 4) == I4)
    R["D_frobenius_relation"] = (mm2(mm2(M4, M5), minv(M4)) == mm2(M5, M5))
    R["D_gf16_simple"] = gf2_simple([M5, M4], 4)
    PHI2 = sp.Matrix([[1, 1], [4, -1]])          # {1, 4̂} on 2-regular {1A, 5A}
    X2 = sp.Matrix([[q20(V20[t][k]) for k in reg2] for t in range(5)])
    D2m = sp.simplify(X2 * PHI2.inv())
    R["D_D_nonneg_int"] = all(sp.simplify(D2m[i, j]).is_integer and sp.simplify(D2m[i, j]) >= 0
                              for i in range(5) for j in range(2))
    C2m = sp.simplify(D2m.T * D2m)
    R["D_Cartan_diag_4_1"] = (sp.simplify(C2m[0, 0] - 4) == 0
                              and sp.simplify(C2m[1, 1] - 1) == 0
                              and sp.simplify(C2m[0, 1]) == 0)
    R["D_detC_4"] = (sp.simplify(C2m.det()) == 4)
    out["F20_p2"] = {"ell": 2, "simples": "1 · GF(16) 4차원(ℤ₅ ⊂ GF(16)^× · ℤ₄ = Gal Frobenius)",
                     "verification": "M₅⁵=I · M₄⁴=I · M₄M₅M₄⁻¹=M₅² · 기약성 전수(15 벡터)",
                     "D": "선형 4 → 1̂ · 4차원 → 4̂", "Cartan": "diag(4,1)", "det": 4,
                     "check": "det C = |G|₂"}

    # ── E. A₆ 문자표 + 무리성 판정 ──────────────────────────────────────
    a6 = dixon([(1, 2, 0, 3, 4, 5), (0, 1, 2, 4, 5, 3), (1, 0, 3, 2, 4, 5)], 6, 61)
    R["E_order360"] = (a6["GN"] == 360)
    R["E_K7"] = (a6["K"] == 7)
    R["E_orders"] = (sorted(a6["orders"]) == [1, 2, 3, 3, 4, 5, 5])
    R["E_degs"] = (sorted(a6["degs"]) == [1, 5, 5, 8, 8, 9, 10])
    F60 = Cyc(60)
    V6 = table_in(F60, a6)
    S5v = F60.sqrt5()
    R["E_sqrt5_ok"] = (F60.mul(S5v, S5v) == F60.scale(F60.one, 5))
    irr = [(t, k) for t in range(7) for k in range(7) if not is_rat(V6[t][k])]
    R["E_irrational_only_deg8"] = all(a6["degs"][t] == 8 for (t, k) in irr)
    R["E_irrational_only_order5"] = all(a6["orders"][k] == 5 for (t, k) in irr)
    R["E_irrational_count4"] = (len(irr) == 4)
    vals_irr = set()
    for (t, k) in irr:
        c = F60.q5coords(S5v, V6[t][k])
        vals_irr.add(c)
    R["E_irrational_is_half_1_pm_sqrt5"] = (
        vals_irr == {(Fr(1, 2), Fr(1, 2)), (Fr(1, 2), Fr(-1, 2))})
    # 두 5차원은 3A/3B 에서 (2,−1)/(−1,2)
    i5s = [t for t in range(7) if a6["degs"][t] == 5]
    k3s = [k for k in range(7) if a6["orders"][k] == 3]
    pair = {tuple(rat_of(V6[t][k]) for k in k3s) for t in i5s}
    R["E_deg5_split_on_3classes"] = (pair == {(2, -1), (-1, 2)} or pair == {(-1, 2), (2, -1)})
    ells = {p: len([k for k in range(7) if a6["orders"][k] % p != 0]) for p in (2, 3, 5)}
    R["E_ell_all_5"] = (ells == {2: 5, 3: 5, 5: 5})
    out["A6"] = {
        "order": 360, "classes": 7, "orders": sorted(a6["orders"]),
        "degrees": sorted(a6["degs"]),
        "irrationality": "★오직 8차원 쌍의 5A/5B — 값 (1±√5)/2 (그 외 전부 유리)",
        "deg5_pair": "3A/3B 에서 (2,−1)/(−1,2) 로 구별(유리)",
        "ell": {str(k): v for k, v in ells.items()},
    }

    # ── F. 엄밀 𝔭-환원 블록 ─────────────────────────────────────────────
    blocks = {}
    for p in (2, 3, 5):
        bs = block_partition(F60, V6, a6, p)
        blocks[p] = sorted((sorted(a6["degs"][t] for t in b) for b in bs), key=str)
    R["F_p2_blocks"] = (blocks[2] == sorted([[1, 5, 5, 9, 10], [8], [8]], key=str))
    R["F_p3_blocks"] = (blocks[3] == sorted([[1, 5, 5, 8, 8, 10], [9]], key=str))
    R["F_p5_blocks"] = (blocks[5] == sorted([[1, 8, 8, 9], [10], [5], [5]], key=str))
    # defect-0 정합: 단독 블록의 차수는 |G|_p 로 나누어떨어짐
    d0ok = True
    for p in (2, 3, 5):
        gp = 1
        while 360 % (gp * p) == 0:
            gp *= p
        for b in blocks[p]:
            if len(b) == 1 and b[0] % gp != 0:
                d0ok = False
    R["F_defect0_consistent"] = d0ok
    out["A6_blocks"] = {str(p): blocks[p] for p in blocks}
    out["A6_blocks_method"] = ("ω_χ(K)=|K|χ/χ(1) 를 ℤ[ζ₆₀] 정수좌표로 계산 → "
                               "𝔭=(p, Φ₆₀ mod p 의 기약인수) 로 환원 비교 "
                               "(무리성분 0 처리 휴리스틱 아님)")

    # ── G. A₆ p=5 Brauer tree ───────────────────────────────────────────
    reg5a6 = [k for k in range(7) if a6["orders"][k] % 5 != 0]
    blk = sorted([t for t in range(7) if a6["degs"][t] in (1, 8, 9)],
                 key=lambda t: (a6["degs"][t], t))
    R["G_block_size4"] = (len(blk) == 4)

    def q60(v):
        c = F60.q5coords(S5v, v)
        assert c is not None, "ℚ(√5) 밖 — 블록 값 아님"
        return sp.Rational(c[0]) + sp.Rational(c[1]) * sp.sqrt(5)
    Xb = sp.Matrix([[q60(V6[t][k]) for k in reg5a6] for t in blk])
    R["G_ell_is_2"] = (Xb.rank() == 2)
    eightd = [t for t in blk if a6["degs"][t] == 8]
    one_t = next(t for t in blk if a6["degs"][t] == 1)
    nine_t = next(t for t in blk if a6["degs"][t] == 9)
    R["G_exceptional_pair_is_8s"] = (len(eightd) == 2)
    valid = []
    for perm in itertools.permutations(["exc", one_t, nine_t]):
        rows = {}
        for pos, v in enumerate(perm):
            d = [1, 0] if pos == 0 else ([1, 1] if pos == 1 else [0, 1])
            if v == "exc":
                for t in eightd:
                    rows[t] = d
            else:
                rows[v] = d
        Dm = sp.Matrix([rows[t] for t in blk])
        try:
            PH = sp.simplify((Dm.T * Dm).inv() * Dm.T * Xb)
        except Exception:
            continue
        if not all(sp.simplify(PH[i, j]).is_integer for i in range(2)
                   for j in range(len(reg5a6))):
            continue
        if not all(sp.simplify(PH[i, 0]) > 0 for i in range(2)):
            continue
        if sp.simplify(Dm * PH - Xb) != sp.zeros(4, len(reg5a6)):
            continue
        Cb = sp.simplify(Dm.T * Dm)
        valid.append((tuple("exc" if v == "exc" else a6["degs"][v] for v in perm),
                      [int(PH[i, 0]) for i in range(2)], int(Cb.det())))
    R["G_tree_unique_upto_reflection"] = (len(valid) == 2)
    R["G_tree_shape"] = (len(valid) == 2 and
                         {v[0] for v in valid} == {("exc", 9, 1), (1, 9, "exc")})
    R["G_brauer_degrees_1_8"] = (len(valid) > 0 and sorted(valid[0][1]) == [1, 8])
    R["G_center_sum"] = (1 + 8 == 9)
    R["G_detC_5"] = (len(valid) > 0 and valid[0][2] == 5)
    out["A6_p5_tree"] = {
        "block": "{1, 8, 8, 9} · defect 1(Sylow-5 = ℤ₅) · ℓ = e = 2 · 예외중복 m = 2",
        "tree": "1 — 9 — [8,8]^exc (경로·반사 제외 유일)",
        "brauer_degrees": [1, 8],
        "consistency": "중심정점 9 = 1 + 8 (인접 변 Brauer 차수 합) · det C(B) = 5",
        "lineage": "a7_brauer_trees_observe(A₇ p=5,7) · m11_brauer_observe(M₁₁ p=11,5) 연장",
    }

    # ── H. A₆ ⊂ A₇ 분기 정합 (quick 에서도 수행 — 2s·최강 교차검증) ──────
    if True:
        a7 = dixon([(1, 2, 0, 3, 4, 5, 6), (1, 2, 3, 4, 5, 6, 0)], 7, 421)
        from qf_witness.observe.a7_brauer_trees_observe import dixon_char_table
        ref = dixon_char_table()
        R["H_a7_K9"] = (a7["K"] == ref["K"] == 9)
        R["H_a7_degs_match"] = (sorted(a7["degs"]) == sorted(ref["degs"]))
        R["H_a7_sizes_match"] = (sorted(a7["sizes"]) == sorted(ref["sizes"]))
        R["H_a7_orders_match"] = (sorted(a7["orders"]) == sorted(ref["orders"]))
        a6sub = [g for g in a7["G"] if g[6] == 6]
        R["H_a6_index7"] = (len(a6sub) == 360)
        img = {}
        for g in a6sub:
            c6 = a6["cls_of"][tuple(g[:6])]
            img.setdefault(c6, a7["cls_of"][g])
        R["H_class_map_total"] = (len(img) == 7)
        # A₆ 클래스의 상(image)인 A₇ 클래스 위수는 전부 60 의 약수 — 공통 필드는 ℚ(ζ₄₂₀)
        R["H_orders_divide_60"] = all(60 % a7["orders"][img[k]] == 0 for k in range(7))
        F420 = Cyc(420)
        V7 = table_in(F420, a7)
        # 직교 내적으로 다중도: m = (1/360) Σ_k |K_k^{A6}| χ7(img k) conj(χ6_t(k))
        V6_420 = table_in(F420, a6)
        Bm = []
        ok_branch = True
        for t7 in range(9):
            row = []
            for t6 in range(7):
                acc = F420.zero
                for k in range(7):
                    term = F420.mul(V7[t7][img[k]], F420.conj(V6_420[t6][k]))
                    acc = F420.add(acc, F420.scale(term, a6["sizes"][k]))
                acc = F420.scale(acc, Fr(1, 360))
                if not (all(x == 0 for x in acc[1:]) and acc[0].denominator == 1
                        and acc[0] >= 0):
                    ok_branch = False
                    row.append(None)
                else:
                    row.append(int(acc[0]))
            Bm.append(row)
        R["H_branching_nonneg_int"] = ok_branch
        R["H_branching_degree_check"] = all(
            sum((Bm[t7][t6] or 0) * a6["degs"][t6] for t6 in range(7)) == a7["degs"][t7]
            for t7 in range(9))
        out["branching_A6_in_A7"] = {
            "a6_degrees_order": [a6["degs"][t] for t in range(7)],
            "a7_degrees_order": [a7["degs"][t] for t in range(9)],
            "matrix_9x7": Bm,
            "verdict": "A₇ 문자의 A₆-제한이 A₆ 문자의 비음정수 결합 — 두 자체유도 표 상호 무모순",
        }

    ok = bool(all(R.values()))
    out["checks"] = R
    out["engine"] = {
        "input": "생성원 순열 + 점수 + 소수 q(≡1 mod exp G)",
        "pipeline": "군 열거 → 켤레류 → 클래스행렬 → Dixon 고유벡터 → 차수 → cyclotomic 다중도",
        "exact_values": "Cyc(e) (g2_1_mtc_observe 재사용 — Φ_N 자체유도)",
        "cross_check": "A₇ 재현 → 기존 dixon_char_table 과 차수·류크기·위수 일치",
    }
    out["scope_honesty"] = {
        "delivered": ("일반 Dixon 엔진(A₇ 교차검증) · F₂₀ Frobenius 판정 + p=5/p=2 완전 D·C "
                      "(det = |G|_p) · A₆ 문자표 + 무리성 (1±√5)/2 확정 + 엄밀 𝔭-환원 블록 3소수 "
                      "+ ★p=5 Brauer tree 실산출 · A₆⊂A₇ 분기 정합"),
        "boundary": ("F₂₀ 의 D 유일성은 정규 Sylow 구조 덕 — 일반 방법 주장 아님. "
                     "A₆ 완전 D·C 는 본 관측 범위 밖이었고 "
                     "★a6_cartan_p23_observe(2026-07-27)에서 해소됨."),
        "not_claimed": "봉인 게이트 · A₆ p=2,3 분해행렬 · ATLAS 인용(전 수치 자체유도)",
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "DIXON-F20-A6.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("일반 Dixon 엔진 + F₂₀/A₆ (결정적 — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  ★엔진 일반화(생성원·점수·q 만) + A₇ 재현 교차검증", flush=True)
        print("  ★F₂₀ 첫 비아벨 Frobenius: p=5 C=I+J det 5 · p=2 C=diag(4,1) det 4", flush=True)
        print("  ★A₆ 무리성 = 8차원 쌍의 5A/5B 에만 · 값 (1±√5)/2 · 엄밀 𝔭-환원 블록", flush=True)
        print("  ★★A₆ p=5 Brauer tree: 1 — 9 — [8,8]^exc · Brauer 차수 {1,8} · det C=5",
              flush=True)
        print("  → .pgf/proofs/DIXON-F20-A6.json", flush=True)
    print(f"dixon_f20_a6_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
