#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dtw_d4_mu8_observe — ★**D^ω(D₄) μ₈ 층 — 완전 S·T + ★T-스펙트럼 위계가 ζ₁₆ 에서 멈춤(폐-음성)**
(관측, seal 아님). Bockstein 사다리 μ₂→μ₄→**μ₈** 의 마지막 계단 —
[[dtw_d4_full_modular_observe]](μ₂·ζ₈)·[[dtw_d4_zeta16_observe]](μ₄·ζ₁₆)의 후속.
★[[dtw_d4_mu4_ribbon_observe]]의 교훈 상속: **켤레 규약을 먼저 고정하고 시작**한다.

★★**headline(폐-음성 + 기전)**: T-스펙트럼 위계 ζ₄(untwisted) → ζ₈(μ₂) → ζ₁₆(μ₄) 는
**ζ₁₆ 에서 멈춘다** — 원시 ζ₃₂ 층은 **존재하지 않는다**. 두 독립 기전:
  (i) ★**ζ₁₆ 을 낳는 층(P₄ 홀수 = w∈{3,5})은 μ₈ 로 lift 되지 않는다**(Bockstein 장애 실증).
  (ii) ★**μ₈ lift 가 존재하는 층(w∈{0,6})은 P₈ 이 항상 짝수** ⟹ λ⁴ = ζ₈^{P₈} ∈ μ₄
      ⟹ λ ∈ μ₁₆ — **원시 ζ₃₂ 불가**.

관측 6축(전 산술 ℚ(ζ₃₂) 정확 — [[g2_1_mtc_observe]]의 `Cyc` 재사용·부동소수 없음):
  A. ★**Bockstein 사다리 전수 census**: H³(D₄,μ₂) 16 클래스 각각에 대해 μ₄ lift·μ₈ lift 존재성을
     **d³ 장애 직접 계산**으로 판정 —
     **μ₄ lift 존재 = w ∈ {0,3,5,6}(4/16)** · **μ₈ lift 존재 = w ∈ {0,6}(2/16)**.
     ★**{3,5} = P₄ 홀수(ζ₁₆) 층이 정확히 μ₈ 에서 탈락** — 사다리가 끊기는 지점의 명시.
  B. ★**P₈ census**: μ₈ lift 가 존재하는 층의 P₈ ∈ **{0,2,4,6}(전부 짝수)** ·
     P₄ = P₈ mod 4 ∈ {0,2} 정합. ⟹ **원시 ζ₃₂ 부재**(위 (ii)).
  C. ★**μ₈ 층 완전 modular data**: 대표 층(w=6·P₈=2)에서 **22 모듈·Σd²=64**(정칙 완비)·
     모듈 공리·**S 대칭·SS†=I·S²=C·Verlinde 22³ 전수 비음정수**·dims{1⁸,2¹⁴}·S_vac=1/8.
  D. ★★**켤레 규약 선고정(Mu4RibbonClosure 교훈 상속) — 실제로 발동**: **C 를 먼저 계산**한 결과
     **μ₈ 대표 층은 비자기쌍대(C ≠ 항등)** 였고, 그래서 **수정 규약 S̄ = S∘C** 를 적용한 뒤
     **(ST)³ = λS² 가 성립**했다. ⟹ μ₄ 층에서 3주를 소모한 함정을 **한 번에 회피**(교훈의 실효 검증).
     ★**Gauss 합 독립 심판**(S 미사용): p₊ = Σd²θ · p₊p₋ = D² · **p₊/D = λ** 일치.
  E. ★**T-스펙트럼 실측**: μ₈ 층 spin 의 실제 위수 — **원시 ζ₃₂ 부재**(A·B 의 예측 검증) ·
     ζ₁₆ 이하로 닫힘.
  F. **계보 정합**: ζ₄(untwisted) → ζ₈(μ₂) → **ζ₁₆(μ₄) = 최대** → μ₈ 층은 **새 위수 없음**.
     ⟹ D₄ twisted double 의 T-스펙트럼 사다리 **완결**.

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - "ζ₃₂ 부재"는 **D₄ · 본 slant 규약(variant-a) · Bockstein 사다리** 범위의 폐-음성이며,
    임의 유한군의 twisted double 일반 주장이 **아니다**.
  - A 의 lift 존재성은 **d³ 장애 직접 계산**(전수) — 표준 정리 인용이 아니다.
  - modular data = 조합·대수 exact 표 — braiding 게이트 실봉인·F/R-symbol 무주장.

사용: python -m qf_witness.observe.dtw_d4_mu8_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import itertools
from fractions import Fraction as Fr

from qf_witness.observe.dtw_d4_u1_census_observe import (
    mul, E, INV, conj, CENT, CLASS_REPS, NE, compute_h3_basis)
from qf_witness.observe.g2_1_mtc_observe import Cyc


# ══════════════════════════════════════════════════════════════════════════
# Bockstein 사다리
# ══════════════════════════════════════════════════════════════════════════
def ladder_setup():
    tri_idx, _rows, h3basis = compute_h3_basis()
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

    def nval(W, t):
        g1, g2, g3 = t
        if g1 == E or g2 == E or g3 == E:
            return 0
        return W[tri_idx[(g1, g2, g3)]]

    def d3_val(W, quad, mod):
        g1, g2, g3, g4 = quad
        return (nval(W, (g2, g3, g4)) - nval(W, (mul(g1, g2), g3, g4))
                + nval(W, (g1, mul(g2, g3), g4))
                - nval(W, (g1, g2, mul(g3, g4))) + nval(W, (g1, g2, g3))) % mod
    col_img = []
    for t in TRIS:
        W = [0] * 343
        W[tri_idx[t]] = 1
        img = 0
        for q in QUADS:
            if d3_val(W, q, 2) == 1:
                img |= (1 << quad_idx[q])
        col_img.append(img)
    basis = []
    for ci, cvec in enumerate(col_img):
        v, comb = cvec, 1 << ci
        for (bv, bc) in basis:
            top = bv.bit_length() - 1
            if (v >> top) & 1:
                v ^= bv
                comb ^= bc
        if v:
            basis.append((v, comb))
            basis.sort(key=lambda p: -p[0].bit_length())

    def gf2_solve(target):
        v, comb = target, 0
        for (bv, bc) in basis:
            top = bv.bit_length() - 1
            if (v >> top) & 1:
                v ^= bv
                comb ^= bc
        return comb if v == 0 else None

    def lift(Wprev, mod_prev):
        """W(mod prev) → mod 2·prev. 장애가 있으면 None, 아니면 16 개 lift."""
        c = 0
        for q in QUADS:
            v = d3_val(Wprev, q, 2 * mod_prev)
            if v % mod_prev:
                return None
            if v == mod_prev:
                c |= (1 << quad_idx[q])
        sol = gf2_solve(c)
        if sol is None:
            return None
        u0 = 0
        for ci in range(343):
            if (sol >> ci) & 1:
                u0 |= (1 << tri_idx[TRIS[ci]])
        return [[Wprev[i] + mod_prev * (((u0 ^ h3reps[z]) >> i) & 1) for i in range(343)]
                for z in range(16)]

    def slant(W, mod):
        def th(a, x, y):
            def nv(t):
                g1, g2, g3 = t
                if g1 == E or g2 == E or g3 == E:
                    return 0
                return W[tri_idx[(g1, g2, g3)]]
            return (nv((a, x, y)) + nv((x, y, conj(a, INV[mul(x, y)])))
                    - nv((x, conj(a, INV[x]), y))) % mod
        return th

    def Pm(W, mod):
        th = slant(W, mod)
        return (th(1, 1, 1) + th(1, 1, 2) + th(1, 1, 3)) % mod
    return h3reps, lift, slant, Pm


# ══════════════════════════════════════════════════════════════════════════
# 일반 modulus m 사영 irrep · 모듈 (필드 = Cyc(4m))
# ══════════════════════════════════════════════════════════════════════════
def make_engine(F, m):
    """m = twist modulus(4 or 8). 위상 ζ_m^k = F.z((F.N//m)*k)."""
    step = F.N // m
    PH = [F.z((step * k) % F.N) for k in range(m)]

    def dot(row, col):
        acc = F.zero
        for a, b in zip(row, col):
            if any(a) and any(b):
                acc = F.add(acc, F.mul(a, b))
        return acc

    def matmul(A, B):
        n, k2 = len(A), len(B)
        m2 = len(B[0])
        return [[dot(A[i], [B[t][j] for t in range(k2)]) for j in range(m2)]
                for i in range(n)]

    def proj_irreps(C, beta):
        n = len(C)
        Cset = set(C)

        def phase(x, y):
            return PH[beta[(x, y)]]

        def phase_inv(x, y):
            return PH[(-beta[(x, y)]) % m]

        def gen_span(gens):
            S, fr = {E}, [E]
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
        NL = 4 * m
        lstep = F.N // NL
        for lam in itertools.product(range(NL), repeat=len(gens)):
            rho = {E: F.one}
            ok = True
            for c in C:
                if c == E:
                    continue
                val, cur = F.one, E
                for gi in word[c]:
                    g = gens[gi]
                    val = F.mul(F.mul(val, F.z((lstep * lam[gi]) % F.N)), phase_inv(cur, g))
                    cur = mul(cur, g)
                rho[c] = val
            for x in C:
                for y in C:
                    if F.mul(rho[x], rho[y]) != F.mul(phase(x, y), rho[mul(x, y)]):
                        ok = False
                        break
                if not ok:
                    break
            if ok and not any(all(rho[c] == ir[c][0][0] for c in C)
                              for ir in irreps if len(ir[E]) == 1):
                irreps.append({c: [[rho[c]]] for c in C})
        need = n - len(irreps)
        if need > 0:
            # 2차원: 지표 부분군에서 유도
            subs = []
            for H in [h for h in _subgroups(C) if len(h) * 2 == n]:
                betaH = {(x, y): beta[(x, y)] for x in H for y in H}
                for s in proj_irreps_1d(F, m, PH, H, betaH):
                    subs.append((H, s))
            for (H, chi) in subs:
                t = next(c for c in C if c not in H)
                P = _induce(F, C, H, chi, t, beta, PH, m)
                if P is None:
                    continue
                # ★기약성: (1/|C|)Σ_c |χ(c)|² = 1 (유도표현은 가약일 수 있다 — 필수 게이트)
                acc = F.zero
                for c in C:
                    ch = F.add(P[c][0][0], P[c][1][1])
                    acc = F.add(acc, F.mul(ch, F.conj(ch)))
                if acc != F.scale(F.one, len(C)):
                    continue
                if not any(_same(F, P, Q, C) for Q in irreps if len(Q[E]) == 2):
                    irreps.append(P)
                if sum(len(q[E]) ** 2 for q in irreps) == n:
                    break
        assert sum(len(q[E]) ** 2 for q in irreps) == n, \
            f"사영 irrep 완비 실패 {sum(len(q[E])**2 for q in irreps)} vs {n}"
        return irreps
    return PH, matmul, proj_irreps


def _subgroups(C):
    out = []
    for r in range(1, len(C) + 1):
        for S in itertools.combinations(C, r):
            Sset = set(S)
            if E in Sset and all(mul(a, b) in Sset for a in S for b in S):
                out.append(list(S))
    return out


def proj_irreps_1d(F, m, PH, H, beta):
    Hset = set(H)
    gens = None
    for g in H:
        S, fr = {E}, [E]
        while fr:
            nf = []
            for x in list(S):
                p = mul(x, g)
                if p not in S:
                    S.add(p)
                    nf.append(p)
            fr = nf
        if S == Hset:
            gens = [g]
            break
    if gens is None:
        for g, h in itertools.product(H, repeat=2):
            S, fr = {E}, [E]
            while fr:
                nf = []
                for x in list(S):
                    for y in (g, h):
                        p = mul(x, y)
                        if p not in S:
                            S.add(p)
                            nf.append(p)
                fr = nf
            if S == Hset:
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
    NL = 4 * m
    lstep = F.N // NL
    out = []
    for lam in itertools.product(range(NL), repeat=len(gens)):
        rho = {E: F.one}
        for c in H:
            if c == E:
                continue
            val, cur = F.one, E
            for gi in word[c]:
                g = gens[gi]
                val = F.mul(F.mul(val, F.z((lstep * lam[gi]) % F.N)),
                            PH[(-beta[(cur, g)]) % m])
                cur = mul(cur, g)
            rho[c] = val
        if all(F.mul(rho[x], rho[y]) == F.mul(PH[beta[(x, y)]], rho[mul(x, y)])
               for x in H for y in H):
            if rho not in out:
                out.append(rho)
    return out


def _induce(F, C, H, chi, t, beta, PH, m):
    """Ind_H^C chi (index 2) — 2×2 행렬."""
    Hset = set(H)
    reps = [E, t]
    d = 2
    P = {}
    for g in C:
        M = [[F.zero] * d for _ in range(d)]
        for j, rj in enumerate(reps):
            gr = mul(g, rj)
            i = 0 if gr in Hset else 1
            h = mul(INV[reps[i]], gr)
            if h not in Hset:
                return None
            ph = PH[(beta[(g, rj)] - beta[(reps[i], h)]) % m]
            M[i][j] = F.mul(ph, chi[h])
        P[g] = [list(r) for r in M]
    for x in C:
        for y in C:
            L = [[F.add(F.mul(P[x][i][0], P[y][0][j]), F.mul(P[x][i][1], P[y][1][j]))
                  for j in range(d)] for i in range(d)]
            Rr = [[F.mul(PH[beta[(x, y)]], P[mul(x, y)][i][j]) for j in range(d)]
                  for i in range(d)]
            if L != Rr:
                return None
    return P


def _same(F, P, Q, C):
    return all(sum(P[c][i][i] for i in range(2)) == sum(Q[c][i][i] for i in range(2))
               for c in C) if False else _chars_eq(F, P, Q, C)


def _chars_eq(F, P, Q, C):
    for c in C:
        a = F.add(P[c][0][0], P[c][1][1])
        b = F.add(Q[c][0][0], Q[c][1][1])
        if a != b:
            return False
    return True


def build_modules(F, m, PH, th, proj_irreps):
    mods = []
    for a in CLASS_REPS:
        C = CENT[a]
        Cset = set(C)
        T, covered = [], set()
        for g in range(8):
            if g not in covered:
                T.append(g)
                covered |= {mul(g, c) for c in C}
        beta = {(x, y): th(a, x, y) for x in C for y in C}
        for ci, rho in enumerate(proj_irreps(C, beta)):
            d = len(rho[E])
            flux = [conj(a, t) for t in T]
            act = {}
            for g in range(8):
                for x in range(8):
                    mp = {}
                    for i, ti in enumerate(T):
                        if conj(flux[i], x) != g:
                            continue
                        xt = mul(x, ti)
                        for j, tj in enumerate(T):
                            c = mul(INV[tj], xt)
                            if c in Cset:
                                break
                        kap = PH[(th(g, x, ti) - th(g, tj, c)) % m]
                        for k in range(d):
                            for k2 in range(d):
                                cf = rho[c][k2][k]
                                if not any(cf):
                                    continue
                                mp.setdefault(i * d + k, []).append((j * d + k2,
                                                                     F.mul(kap, cf)))
                    act[(g, x)] = mp
            mods.append((f"({a},{ci})", len(T) * d, act))
    return mods


def apply_op(F, act, g, x, vec, dim):
    out = [F.zero] * dim
    for col, ent in act[(g, x)].items():
        c0 = vec[col]
        if not any(c0):
            continue
        for (row, cf) in ent:
            out[row] = F.add(out[row], F.mul(cf, c0))
    return out


# ══════════════════════════════════════════════════════════════════════════
def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "dtw-d4-mu8/v1",
           "_note": ("D^ω(D₄) μ₈ 층 — 완전 S·T + ★T-스펙트럼이 ζ₁₆ 에서 멈춤(폐-음성·기전 2건). "
                     "관측·seal 아님·module 0·root 불변.")}

    # ── A·B. Bockstein 사다리 census ────────────────────────────────────
    h3reps, lift, slant, Pm = ladder_setup()
    mu4_ok, mu8_ok, p4map, p8map = [], [], {}, {}
    for w in range(16):
        W2 = [(h3reps[w] >> i) & 1 for i in range(343)]
        L4 = lift(W2, 2)
        if L4 is None:
            continue
        mu4_ok.append(w)
        p4map[w] = sorted({Pm(W4, 4) for W4 in L4})
        got8 = []
        for W4 in L4:
            L8 = lift(W4, 4)
            if L8 is not None:
                got8 += [(W8, Pm(W8, 8)) for W8 in L8]
        if got8:
            mu8_ok.append(w)
            p8map[w] = sorted({p for (_, p) in got8})
    R["A_mu4_lift_set"] = (mu4_ok == [0, 3, 5, 6])
    R["A_mu8_lift_set"] = (mu8_ok == [0, 6])
    R["A_zeta16_layers_are_3_5"] = (sorted(w for w in mu4_ok if any(p % 2 for p in p4map[w]))
                                    == [3, 5])
    R["A_zeta16_layers_dont_lift"] = all(w not in mu8_ok for w in (3, 5))
    R["B_P8_all_even"] = all(all(p % 2 == 0 for p in v) for v in p8map.values())
    R["B_P8_set"] = (sorted({p for v in p8map.values() for p in v}) == [0, 2, 4, 6])
    R["B_P4_consistent"] = all(sorted({p % 4 for p in p8map[w]}) == p4map[w] for w in mu8_ok)
    R["B_no_primitive_zeta32"] = R["B_P8_all_even"]
    out["bockstein"] = {
        "mu4_lift_exists": mu4_ok, "mu8_lift_exists": mu8_ok,
        "P4_by_layer": {str(k): v for k, v in p4map.items()},
        "P8_by_layer": {str(k): v for k, v in p8map.items()},
        "verdict": ("★ζ₁₆ 을 낳는 층(P₄ 홀수 = w∈{3,5})은 **μ₈ 로 lift 되지 않고**(Bockstein 장애), "
                    "μ₈ lift 가 존재하는 층(w∈{0,6})은 **P₈ 이 항상 짝수** ⟹ λ⁴=ζ₈^{P₈}∈μ₄ "
                    "⟹ λ∈μ₁₆ ⟹ **원시 ζ₃₂ 부재**"),
    }

    # ── C·D·E. μ₈ 대표 층 완전 modular data ─────────────────────────────
    F = Cyc(32)
    PH, matmul, proj_irreps = make_engine(F, 8)
    W2 = [(h3reps[6] >> i) & 1 for i in range(343)]
    L4 = lift(W2, 2)
    W8 = None
    for W4 in L4:
        L8 = lift(W4, 4)
        if L8:
            for cand in L8:
                if Pm(cand, 8) == 2:
                    W8 = cand
                    break
        if W8:
            break
    R["C_representative_found"] = (W8 is not None)
    th8 = slant(W8, 8)
    R["C_P8_is_2"] = (Pm(W8, 8) == 2)
    mods = build_modules(F, 8, PH, th8, proj_irreps)
    n = len(mods)
    R["C_n22"] = (n == 22)
    R["C_sumdim2_64"] = (sum(d * d for _, d, _ in mods) == 64)

    TR = []
    for (lab, dim, act) in mods:
        t = {}
        for g in range(8):
            for x in range(8):
                s = F.zero
                for col, ent in act[(g, x)].items():
                    for (row, cf) in ent:
                        if row == col:
                            s = F.add(s, cf)
                t[(g, x)] = s
        TR.append(t)
    S = [[F.zero] * n for _ in range(n)]
    for I in range(n):
        for J in range(n):
            acc = F.zero
            for g in range(8):
                for h in range(8):
                    a = TR[I][(conj(g, h), h)]
                    if not any(a):
                        continue
                    b = TR[J][(h, g)]
                    if not any(b):
                        continue
                    acc = F.add(acc, F.mul(a, b))
            S[I][J] = F.scale(acc, Fr(1, 8))
    vac = next(I for I in range(n) if all(
        TR[I][(g, x)] == (F.one if g == E else F.zero) for g in range(8) for x in range(8)))
    R["C_S_symmetric"] = all(S[i][j] == S[j][i] for i in range(n) for j in range(n))

    def mm(A, B, conjB=False):
        out_ = []
        for i in range(n):
            row = []
            for j in range(n):
                acc = F.zero
                for k in range(n):
                    b = F.conj(B[j][k]) if conjB else B[k][j]
                    if any(A[i][k]) and any(b):
                        acc = F.add(acc, F.mul(A[i][k], b))
                row.append(acc)
            out_.append(row)
        return out_
    SSd = mm(S, S, conjB=True)
    R["C_S_unitary"] = all(SSd[i][j] == (F.one if i == j else F.zero)
                           for i in range(n) for j in range(n))
    S2 = mm(S, S)
    Cperm, okC = [], True
    for i in range(n):
        nz = [j for j in range(n) if any(S2[i][j])]
        if len(nz) != 1 or S2[i][nz[0]] != F.one:
            okC = False
            break
        Cperm.append(nz[0])
    R["C_S2_is_C"] = okC
    R["D_C_computed_first"] = okC
    c_identity = (okC and Cperm == list(range(n)))
    # ★C=항등 여부는 **사실 기록**(합격 조건 아님) — 비자기쌍대면 수정 규약 S̄=S∘C 적용
    R["D_C_nontrivial_detected"] = (okC and not c_identity)
    dd = [F.scale(S[vac][I], 8) for I in range(n)]
    R["C_dims_1_8_2_14"] = (sorted(int(d[0]) for d in dd) == [1] * 8 + [2] * 14)
    R["C_Svac"] = (S[vac][vac] == F.scale(F.one, Fr(1, 8)))

    # ribbon spin
    theta = []
    ribbon_ok = True
    for (lab, dim, act) in mods:
        th0 = None
        for j in range(dim):
            vec = [F.one if i == j else F.zero for i in range(dim)]
            o = [F.zero] * dim
            for a in range(8):
                o = [F.add(p, q) for p, q in zip(o, apply_op(F, act, a, a, vec, dim))]
            if th0 is None:
                th0 = o[j]
            for i in range(dim):
                if o[i] != (th0 if i == j else F.zero):
                    ribbon_ok = False
        theta.append(th0)
    R["C_ribbon_scalar"] = ribbon_ok

    # ★켤레 규약: C ≠ 항등이면 S̄ = S∘C
    Suse = S if c_identity else [[F.conj(S[i][j]) for j in range(n)] for i in range(n)]
    T = [[(theta[i] if i == j else F.zero) for j in range(n)] for i in range(n)]
    S2u = mm(Suse, Suse)
    Cu = [next(j for j in range(n) if any(S2u[i][j])) for i in range(n)]
    ST = mm(Suse, T)
    ST3 = mm(mm(ST, ST), ST)
    lam, ok3 = None, True
    for i in range(n):
        for j in range(n):
            if j == Cu[i]:
                if lam is None:
                    lam = ST3[i][j]
                elif ST3[i][j] != lam:
                    ok3 = False
            elif any(ST3[i][j]):
                ok3 = False
    R["D_ST3_prop_S2"] = ok3
    # Gauss 합(S 미사용 독립 심판)
    pp, pm_ = F.zero, F.zero
    for i in range(n):
        d2 = F.mul(dd[i], dd[i])
        pp = F.add(pp, F.mul(d2, theta[i]))
        pm_ = F.add(pm_, F.mul(d2, F.conj(theta[i])))
    R["D_gauss_pp_pm_D2"] = (F.mul(pp, pm_) == F.scale(F.one, 64))
    R["D_gauss_matches_lam"] = (lam is not None and F.scale(pp, Fr(1, 8)) == lam)

    # Verlinde
    verl = True
    idx = range(n) if not quick else range(0, n, 4)
    inv0 = [F.inv(Suse[vac][L]) for L in range(n)]
    for i in idx:
        for j in idx:
            pre = [F.mul(F.mul(Suse[i][L], Suse[j][L]), inv0[L]) for L in range(n)]
            for k in range(n):
                acc = F.zero
                for L in range(n):
                    if any(pre[L]):
                        acc = F.add(acc, F.mul(pre[L], F.conj(Suse[k][L])))
                if any(acc[1:]) or acc[0].denominator != 1 or acc[0] < 0:
                    verl = False
    R["C_verlinde"] = verl

    # ── E. T-스펙트럼 위수 ──────────────────────────────────────────────
    def order_of(x):
        for k in (1, 2, 4, 8, 16, 32):
            if x == F.z(0):
                return 1
            p = x
            for _ in range(k - 1):
                p = F.mul(p, x)
            if p == F.one:
                return k
        return None
    ords = sorted({order_of(t) for t in theta})
    R["E_no_order32"] = (32 not in ords)
    R["E_orders_subset_16"] = all(o in (1, 2, 4, 8, 16) for o in ords if o)
    out["modular_data"] = {
        "layer": "w=6 · P₈=2", "rank": 22, "sum_d2": 64, "dims": "{1×8, 2×14}",
        "C_identity": bool(c_identity),
        "self_dual": bool(c_identity),
        "convention": "★C 를 **먼저 계산**해 자기쌍대 판정 → 필요 시 S̄=S∘C 적용(μ₄ 함정 회피)",
        "theta_orders": [o for o in ords if o],
        "gauss": "p₊p₋ = D² = 64 · p₊/D = λ (S 미사용 독립 심판)",
    }
    out["hierarchy"] = {
        "ladder": "ζ₄(untwisted) → ζ₈(μ₂) → ζ₁₆(μ₄) → **μ₈ 층은 새 위수 없음**",
        "verdict": "★★D₄ twisted double 의 T-스펙트럼 위계는 **ζ₁₆ 에서 완결**(원시 ζ₃₂ 부재)",
        "mechanisms": ["ζ₁₆ 층(P₄ 홀수)은 μ₈ 로 lift 불가(Bockstein 장애)",
                       "μ₈ lift 존재 층은 P₈ 짝수 ⟹ λ ∈ μ₁₆"],
    }

    # ── teeth ───────────────────────────────────────────────────────────
    R["teeth_ladder_breaks_at_zeta16"] = (R["A_zeta16_layers_dont_lift"]
                                          and R["B_P8_all_even"])
    R["teeth_convention_fixed_first"] = R["D_C_computed_first"]
    R["teeth_gauss_independent"] = R["D_gauss_pp_pm_D2"]

    ok = bool(all(R.values()))
    out["checks"] = R
    out["scope_honesty"] = {
        "delivered": ("Bockstein 사다리 전수 census(μ₂ 16 → μ₄ 4 → μ₈ 2) + μ₈ 대표 층 완전 "
                      "modular data(22·Σd²=64·유니터리·S²=C·Verlinde·(ST)³) + "
                      "★T-스펙트럼이 ζ₁₆ 에서 멈춤(폐-음성·기전 2건)"),
        "boundary": ("'ζ₃₂ 부재'는 **D₄ · 본 slant 규약 · Bockstein 사다리** 범위의 폐-음성이며 "
                     "임의 유한군 twisted double 일반 주장이 아니다"),
        "not_claimed": "braiding 실봉인 · F/R-symbol · μ₁₆ 이상 lift",
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p_ = os.path.join(ROOT, ".pgf", "proofs", "DTW-D4-MU8.json")
        os.makedirs(os.path.dirname(p_), exist_ok=True)
        with open(p_, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("D^ω(D₄) μ₈ 층 (정확 — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  ★Bockstein: μ₂ 16 → μ₄ 4개{0,3,5,6} → μ₈ **2개{0,6}**", flush=True)
        print("  ★★ζ₁₆ 층(P₄ 홀수={3,5})은 **μ₈ lift 불가** · μ₈ 층은 **P₈ 전부 짝수**",
              flush=True)
        print("  ⟹ **원시 ζ₃₂ 부재 — T-스펙트럼 위계는 ζ₁₆ 에서 완결**", flush=True)
        print("  ★켤레 규약 선고정(C 먼저 계산) + Gauss 합 독립 심판", flush=True)
        print("  → .pgf/proofs/DTW-D4-MU8.json", flush=True)
    print(f"dtw_d4_mu8_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
