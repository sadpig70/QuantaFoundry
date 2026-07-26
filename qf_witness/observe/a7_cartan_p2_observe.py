#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""a7_cartan_p2_observe — ★**A₇ p=2 완전 분해행렬 D(9×6)·Cartan** (관측, seal 아님).
[[a7_cartan_p23_observe]](TrackHE19 P4)가 "**p=2 완전 D·C = 미완**(양 블록 비순환 defect·wild
가능 — 트리 이론 부재·decomposition 유일성 비보장)"으로 명시 유보한 축을 **완결**한다. v20 §4 잔여.

★돌파 전략 = **6 simple 전부를 명시 GF(2)-모듈로 구성**. Sylow-2 = D₄(비순환)이라 Brauer tree
이론이 원리적으로 적용되지 않지만, **Brauer 문자표 Φ 가 확정되면 D = X|_{2-reg}·Φ⁻¹ 이 유일**하다
— p=3 주블록에서 쓴 "트리 이론 불필요(명시 모듈 구성)" 전략의 확장.

관측 7축(전 산술 GF(2)/ℚ(√−7) 정확 — 확률적 meataxe 금지 규율 준수):
  A. **통상 자산 + 2-regular 구조**: `dixon_char_table` 자체유도 문자표 · 9 클래스 ·
     2-regular **6**(위수 1,3,3,5,7,7) ⟹ ℓ=6 · 2-블록.
  B. ★★**A₇ ⊂ GL(4,2) 명시 구성**: Fano 평면(이차잉여 {0,1,3}+i mod 7) 안정화군
     **H ≅ PSL(3,2), |H|=168** 기계확인(index 15) → 15 좌잉여류 작용 →
     **3-부분집합 궤도 {35, 420} 자체발견**(35 = PG(3,2) 선) → 선벡터 span **dim 11** →
     **몫 = 4차원 GF(2)-모듈** · 준동형 검증 · **충실**(상 2520).
  C. ★★**6 simple 전부 명시 구성 + 기약성 전수 검증**:
     **1** · **4** · **4̄** = dual · **6** = Λ²(4) · **14** = sl₄(2)/⟨I⟩(trace-0 15차원
     부분모듈 → ⟨I⟩ 몫) · **20** = ker(4⊗Λ²4 → Λ³4)(Λ³4 ≅ 4차원 확인).
     기약성 = **전 궤도 대표 vector 가 전체를 생성** — 궤도 축약이 전수성을 보장
     (⟨v⟩⊊M ⟹ ⟨gv⟩ = g⟨v⟩ ⊊ M). 궤도수 1/1/1/3/27/478.
  D. ★**Brauer 문자표 6×6 자체유도** — GF(2) 특성다항식 인수분해 **다중도만으로**
     (GF(2^k) 산술 불필요): 위수 3 → Φ₃ 기약 ⟹ φ = a−b(유리) · 위수 5 → Φ₅ GF(2)-기약 ⟹
     φ = a−b(유리) · **위수 7 → x⁷−1 = (x−1)(x³+x+1)(x³+x²+1) ⟹ φ = a + bα + cᾱ**
     (α=(−1+√−7)/2) — 무리성은 7-클래스에만 나타난다.
  E. ★★**완전 D(9×6)·Cartan C=DᵀD**: D = X|_{2-reg}·Φ⁻¹ 정확해 · **전 성분 비음정수** ·
     **차수 정합 Σ_φ d·dim(φ) = deg(χ) 9행 전수** · 블록 분리:
     **주블록 simples {1̂, 14̂, 20̂}** / **비주블록 {4̂, 4̄̂, 6̂}** ·
     D 행: 1→1̂ · 14→14̂ · 15→1̂+14̂ · 21→1̂+20̂ · 35→1̂+14̂+20̂ ·
           6→6̂ · 10→4̄̂+6̂ · 10̄→4̂+6̂ · 14′→4̂+4̄̂+6̂ ·
     **C(주) = [[4,2,2],[2,3,1],[2,1,2]], det = 8 = |A₇|₂** ·
     **C(비주) = [[2,1,2],[1,2,2],[2,2,4]], det = 4** · **det C = 32**.
  F. ★**독립 교차확인**: (i) φ_6 = (7점 순열문자 − 1) 정확 일치 ⟹ **Λ²(4) ≅ 자연 6차원 모듈**
     (ii) **φ_14 = φ_4·φ_4̄ − 2** (iii) **φ_20 = φ_4·φ_6 − φ_4̄** — 구성과 무관한 산술 항등식.
  G. ★**게이지 고지(오늘의 교훈 상속)**: Brauer lift 의 μ₇(GF(8)) → μ₇(ℂ) 동형 선택은
     **2중 게이지**이고, 반대 선택은 D 의 **4̂↔4̄̂ 열 교환(= 10↔10̄ 행 교환)** 과 정확히 같다 —
     **양 게이지를 모두 계산해 실증**. ⟹ D 는 이 라벨링 게이지까지 유일하고,
     **Cartan·det·블록 구조는 게이지 불변**.

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - 선행 관측의 "p=2 완전 D·C 미완" **해소** — 단 그 유보 이유("wild 가능·유일성 비보장")는
    **일반론으로는 옳다**. 여기서는 6 simple 을 **전부 명시 구성**했기 때문에 Φ 가 확정되어
    유일성이 따라온 것 — 일반 wild 블록에 대한 방법 주장이 아니다.
  - 기약성은 **전수 검증**(궤도 축약) — 확률적 meataxe 미사용.
  - Brauer 문자는 modular 표현론 수준 — 봉인 게이트 아님.

사용: python -m qf_witness.observe.a7_cartan_p2_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import itertools

import sympy as sp

from qf_witness.observe.a7_brauer_trees_observe import dixon_char_table

N7 = 7
GENS = [(1, 2, 0, 3, 4, 5, 6), (1, 2, 3, 4, 5, 6, 0)]
IDp = tuple(range(N7))
S7 = sp.sqrt(-7)
AL = (sp.Integer(-1) + S7) / 2
ALB = (sp.Integer(-1) - S7) / 2


def pmul(a, b):
    return tuple(a[b[i]] for i in range(N7))


def is_even(p):
    s = 0
    for i in range(N7):
        for j in range(i + 1, N7):
            if p[i] > p[j]:
                s += 1
    return s % 2 == 0


# ══════════════════════════════════════════════════════════════════════════
# GF(2) 선형대수 (bitmask)
# ══════════════════════════════════════════════════════════════════════════
def rref_add(basis, v):
    for b in basis:
        lead = b.bit_length() - 1
        if (v >> lead) & 1:
            v ^= b
    if v:
        basis.append(v)
        basis.sort(reverse=True)
    return basis


def rref_basis(vs):
    B = []
    for v in vs:
        rref_add(B, v)
    return B


def mm(A, B):
    n, m, k = len(A), len(B[0]), len(B)
    return tuple(tuple(sum(A[i][t] * B[t][j] for t in range(k)) % 2 for j in range(m))
                 for i in range(n))


def eye(n):
    return tuple(tuple(1 if i == j else 0 for j in range(n)) for i in range(n))


def madd(A, B):
    return tuple(tuple((A[i][j] + B[i][j]) % 2 for j in range(len(A[0])))
                 for i in range(len(A)))


def nullity(A):
    rows = [sum(A[i][j] << j for j in range(len(A[0]))) for i in range(len(A))]
    return len(A[0]) - len(rref_basis(rows))


def inv2(M):
    n = len(M)
    A = [[M[i][j] for j in range(n)] + [1 if i == j else 0 for j in range(n)]
         for i in range(n)]
    r = 0
    for c in range(n):
        pr = next((i for i in range(r, n) if A[i][c]), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        for i in range(n):
            if i != r and A[i][c]:
                A[i] = [(A[i][k] + A[r][k]) % 2 for k in range(2 * n)]
        r += 1
    return tuple(tuple(A[i][n + j] for j in range(n)) for i in range(n))


def col_images(M):
    n = len(M)
    return [sum(M[i][j] << i for i in range(n)) for j in range(n)]


def apply_bm(cols, v):
    r = 0
    while v:
        b = v & -v
        r ^= cols[b.bit_length() - 1]
        v ^= b
    return r


def is_submodule(mats, B):
    Bs = rref_basis(B)
    for M in mats:
        cols = col_images(M)
        for b in Bs:
            t = apply_bm(cols, b)
            for x in Bs:
                lead = x.bit_length() - 1
                if (t >> lead) & 1:
                    t ^= x
            if t:
                return False
    return True


def sub_rep(mats, B):
    Bb = rref_basis(B)
    k = len(Bb)
    pv = [b.bit_length() - 1 for b in Bb]

    def coords(v):
        c = [0] * k
        t = v
        for i, x in enumerate(Bb):
            if (t >> pv[i]) & 1:
                t ^= x
                c[i] = 1
        assert t == 0
        return c
    out = []
    for M in mats:
        cols = col_images(M)
        cm = [coords(apply_bm(cols, b)) for b in Bb]
        out.append(tuple(tuple(cm[j][i] for j in range(k)) for i in range(k)))
    return out


def quot_rep(mats, B):
    Bb = rref_basis(B)
    pv = [b.bit_length() - 1 for b in Bb]
    n = len(mats[0])
    fr = [i for i in range(n) if i not in pv]

    def red(v):
        for x in Bb:
            lead = x.bit_length() - 1
            if (v >> lead) & 1:
                v ^= x
        return [(v >> f) & 1 for f in fr]
    out = []
    for M in mats:
        cols = col_images(M)
        cm = [red(apply_bm(cols, 1 << f)) for f in fr]
        out.append(tuple(tuple(cm[j][i] for j in range(len(fr))) for i in range(len(fr))))
    return out


def simple_and_orbits(mats, cap=None):
    """기약성 전수 검증: 모든 궤도 대표가 전체를 생성하는지. (simple, 궤도수)."""
    n = len(mats[0])
    colsL = [col_images(M) for M in mats]
    seen = bytearray(1 << n)
    seen[0] = 1
    nreps = 0
    for v0 in range(1, 1 << n):
        if seen[v0]:
            continue
        nreps += 1
        fr = [v0]
        seen[v0] = 1
        while fr:
            nf = []
            for v in fr:
                for cols in colsL:
                    w = apply_bm(cols, v)
                    if not seen[w]:
                        seen[w] = 1
                        nf.append(w)
            fr = nf
        if cap is not None and nreps > cap:
            continue
        B = rref_basis([v0])
        fr = list(B)
        while fr:
            nf = []
            for b in fr:
                for cols in colsL:
                    t = apply_bm(cols, b)
                    for x in B:
                        lead = x.bit_length() - 1
                        if (t >> lead) & 1:
                            t ^= x
                    if t:
                        rref_add(B, t)
                        nf.append(t)
            fr = nf
        if len(B) != n:
            return False, nreps
    return True, nreps


# ══════════════════════════════════════════════════════════════════════════
# 외적·텐서·켤레작용
# ══════════════════════════════════════════════════════════════════════════
def wedge_k(M, k):
    n = len(M)
    keys = list(itertools.combinations(range(n), k))
    idx = {t: i for i, t in enumerate(keys)}
    d = len(keys)
    out = [[0] * d for _ in range(d)]
    for jc, key in enumerate(keys):
        cols = [[M[i][x] for i in range(n)] for x in key]
        for combo in itertools.product(range(n), repeat=k):
            if len(set(combo)) != k:
                continue
            v = 1
            for t in range(k):
                v &= cols[t][combo[t]]
            if v:
                out[idx[tuple(sorted(combo))]][jc] ^= 1
    return tuple(tuple(r) for r in out)


def tensor(A, B):
    nb = len(B)
    d = len(A) * nb
    return tuple(tuple(A[i // nb][j // nb] * B[i % nb][j % nb] % 2 for j in range(d))
                 for i in range(d))


def conj_end(M):
    """End(V) 위 X ↦ M X M⁻¹ (기저 E_ab ↔ index a·n+b)."""
    n = len(M)
    Mi = inv2(M)
    d = n * n
    out = [[0] * d for _ in range(d)]
    for a in range(n):
        for b in range(n):
            col = a * n + b
            for i in range(n):
                for j in range(n):
                    if M[i][a] and Mi[b][j]:
                        out[i * n + j][col] ^= 1
    return tuple(tuple(r) for r in out)


def nullspace(rows, ncol):
    B = rref_basis(rows)
    pvs = [b.bit_length() - 1 for b in B]
    out = []
    for f in (j for j in range(ncol) if j not in pvs):
        x = 1 << f
        for i, b in enumerate(B):
            if bin(b & x).count("1") % 2:
                x ^= 1 << pvs[i]
        out.append(x)
    return out


# ══════════════════════════════════════════════════════════════════════════
def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "a7-cartan-p2/v1",
           "_note": ("A₇ p=2 완전 D(9×6)·Cartan — 6 simple 전부 명시 GF(2)-모듈 구성으로 "
                     "Φ 확정 → D 유일(트리 이론 불필요). 관측·seal 아님·module 0·root 불변.")}

    # ── A. 통상 자산 ────────────────────────────────────────────────────
    CT = dixon_char_table()
    K, orders, degs, reps, EX = CT["K"], CT["orders"], CT["degs"], CT["reps"], CT["exact"]
    R["A_K9"] = (K == 9)
    reg = [k for k in range(K) if orders[k] % 2 == 1]
    R["A_two_regular_6"] = (len(reg) == 6 and
                            sorted(orders[k] for k in reg) == [1, 3, 3, 5, 7, 7])
    R["A_degs"] = (sorted(degs) == [1, 6, 10, 10, 14, 14, 15, 21, 35])

    # ── B. A₇ ⊂ GL(4,2) ─────────────────────────────────────────────────
    G = [p for p in itertools.permutations(range(N7)) if is_even(p)]
    LINES = frozenset(frozenset(((0 + i) % 7, (1 + i) % 7, (3 + i) % 7)) for i in range(7))
    R["B_fano_7_lines"] = (len(LINES) == 7)
    H = [p for p in G if all(frozenset(p[x] for x in L) in LINES for L in LINES)]
    R["B_H_168"] = (len(H) == 168)
    cos, seen = [], set()
    for g in G:
        if g in seen:
            continue
        c = frozenset(pmul(g, h) for h in H)
        cos.append(c)
        seen |= c
    R["B_15_cosets"] = (len(cos) == 15)
    cidx = {}
    for i, c in enumerate(cos):
        for x in c:
            cidx[x] = i
    cos_rep = [next(iter(c)) for c in cos]

    def act15(g):
        return tuple(cidx[pmul(g, cos_rep[i])] for i in range(15))
    P15 = [act15(g) for g in GENS]

    def orb3(t):
        s = {t}
        fr = [t]
        while fr:
            nf = []
            for x in fr:
                for pp in P15:
                    nx = frozenset(pp[y] for y in x)
                    if nx not in s:
                        s.add(nx)
                        nf.append(nx)
            fr = nf
        return s
    sizes3, covered = [], set()
    for t in itertools.combinations(range(15), 3):
        fs = frozenset(t)
        if fs in covered:
            continue
        o = orb3(fs)
        covered |= o
        sizes3.append(len(o))
    R["B_orbit3_sizes_35_420"] = (sorted(sizes3) == [35, 420])
    L35 = next(o for o in (orb3(frozenset(t)) for t in itertools.combinations(range(15), 3))
               if len(o) == 35)
    Kb = []
    for Lx in L35:
        v = 0
        for x in Lx:
            v |= 1 << x
        rref_add(Kb, v)
    R["B_line_span_dim11"] = (len(Kb) == 11)
    piv = [b.bit_length() - 1 for b in Kb]
    free = [i for i in range(15) if i not in piv]

    def reduce_mod(v):
        for b in Kb:
            lead = b.bit_length() - 1
            if (v >> lead) & 1:
                v ^= b
        return tuple((v >> f) & 1 for f in free)

    def mat4(g):
        p = act15(g)
        cols = [reduce_mod(1 << p[f]) for f in free]
        return tuple(tuple(cols[j][i] for j in range(4)) for i in range(4))
    R["B_quotient_dim4"] = (len(free) == 4)
    sample = G if not quick else G[:300]
    R["B_homomorphism"] = all(mat4(pmul(g, h)) == mm(mat4(g), mat4(h))
                              for g in sample for h in GENS)
    R["B_faithful_2520"] = (len({mat4(g) for g in G}) == 2520)
    out["gl42_embedding"] = {
        "H": "Fano 평면 안정화군 ≅ PSL(3,2)·|H|=168·index 15",
        "orbits_on_3subsets": "{35, 420} — 35 = PG(3,2) 선(자체발견)",
        "construction": "F₂^15 / span(선벡터, dim 11) = 4차원 GF(2)-모듈 · 충실",
    }

    # ── C. 6 simple 명시 구성 ───────────────────────────────────────────
    g0, g1 = GENS
    M0, M1 = mat4(g0), mat4(g1)
    A1 = [eye(1), eye(1)]
    A4 = [M0, M1]
    A4b = [tuple(zip(*inv2(M0))), tuple(zip(*inv2(M1)))]
    A6 = [wedge_k(M0, 2), wedge_k(M1, 2)]
    W3 = [wedge_k(M0, 3), wedge_k(M1, 3)]
    R["C_wedge2_dim6"] = (len(A6[0]) == 6)
    R["C_wedge3_dim4"] = (len(W3[0]) == 4)
    # 14 = sl₄/⟨I⟩
    A16 = [conj_end(M0), conj_end(M1)]
    tz = [1 << (i * 4 + j) for i in range(4) for j in range(4) if i != j]
    tz += [(1 << 0) | (1 << (i * 4 + i)) for i in range(1, 4)]
    R["C_tracezero_submodule_15"] = (len(rref_basis(tz)) == 15 and is_submodule(A16, tz))
    A15 = sub_rep(A16, tz)
    Bb15 = rref_basis(tz)
    pv15 = [b.bit_length() - 1 for b in Bb15]
    Ivec = sum(1 << (i * 4 + i) for i in range(4))
    t_, c_ = Ivec, [0] * 15
    for i, x in enumerate(Bb15):
        if (t_ >> pv15[i]) & 1:
            t_ ^= x
            c_[i] = 1
    R["C_I_in_tracezero"] = (t_ == 0)
    Ic = sum(c_[i] << i for i in range(15))
    R["C_I_submodule"] = is_submodule(A15, [Ic])
    A14 = quot_rep(A15, [Ic])
    R["C_dim14"] = (len(A14[0]) == 14)
    # 20 = ker(4 ⊗ Λ²4 → Λ³4)
    A24 = [tensor(M0, A6[0]), tensor(M1, A6[1])]
    pairs = list(itertools.combinations(range(4), 2))
    tri = list(itertools.combinations(range(4), 3))
    tidx = {t: i for i, t in enumerate(tri)}
    PHIm = [[0] * 24 for _ in range(4)]
    for v in range(4):
        for pi, (a, b) in enumerate(pairs):
            if v in (a, b):
                continue
            PHIm[tidx[tuple(sorted((v, a, b)))]][v * 6 + pi] = 1
    KER = nullspace([sum(PHIm[i][j] << j for j in range(24)) for i in range(4)], 24)
    R["C_ker_dim20_submodule"] = (len(rref_basis(KER)) == 20 and is_submodule(A24, KER))
    A20 = sub_rep(A24, KER)
    R["C_dim20"] = (len(A20[0]) == 20)

    NAMES = ["1", "4", "4b", "6", "14", "20"]
    MODS = {"1": A1, "4": A4, "4b": A4b, "6": A6, "14": A14, "20": A20}
    DIMS = {"1": 1, "4": 4, "4b": 4, "6": 6, "14": 14, "20": 20}
    simple_ok, orbcnt = True, {}
    for nm in NAMES:
        s, nr = simple_and_orbits(MODS[nm])
        orbcnt[nm] = nr
        if not s:
            simple_ok = False
    R["C_all_six_simple_exhaustive"] = simple_ok
    R["C_orbit_counts"] = (orbcnt == {"1": 1, "4": 1, "4b": 1, "6": 3, "14": 27, "20": 478})
    out["simples"] = {
        "list": "1 · 4 · 4̄(dual) · 6=Λ²(4) · 14=sl₄(2)/⟨I⟩ · 20=ker(4⊗Λ²4→Λ³4)",
        "irreducibility": "전수(궤도 대표 vector 가 전체 생성 — ⟨v⟩⊊M ⟹ ⟨gv⟩⊊M 로 축약 정당)",
        "orbit_counts": orbcnt,
    }

    # ── D. Brauer 문자표 ────────────────────────────────────────────────
    par = {IDp: None}
    fr = [IDp]
    while fr:
        nf = []
        for x in fr:
            for gi, g in enumerate(GENS):
                y = pmul(g, x)
                if y not in par:
                    par[y] = (x, gi)
                    nf.append(y)
        fr = nf

    def word(p):
        w = []
        while par[p] is not None:
            x, gi = par[p]
            w.append(gi)
            p = x
        return w[::-1]

    def mat_of(mats, p):
        M = eye(len(mats[0]))
        for gi in word(p):
            M = mm(mats[gi], M)
        return M

    def brauer(mats, gauge):
        n = len(mats[0])
        vals = []
        for k in reg:
            o = orders[k]
            if o == 1:
                vals.append(sp.Integer(n))
                continue
            M = mat_of(mats, reps[k])
            a = nullity(madd(M, eye(n)))
            if o == 3:
                vals.append(sp.Integer(a - (n - a) // 2))
            elif o == 5:
                vals.append(sp.Integer(a - (n - a) // 4))
            else:
                M2 = mm(M, M)
                M3 = mm(M2, M)
                b = nullity(madd(madd(M3, M), eye(n))) // 3
                c = nullity(madd(madd(M3, M2), eye(n))) // 3
                assert a + 3 * b + 3 * c == n
                vals.append(a + (b * AL + c * ALB if gauge == 0 else b * ALB + c * AL))
        return vals

    # ── E. D·Cartan (양 게이지) ─────────────────────────────────────────
    def ord_val(t, k):
        o = orders[k]
        a = EX[t][k]
        if o == 1:
            return sp.Integer(a[0])
        if o in (3, 5):
            return sp.Integer(a[0] - a[1])
        p_, q_ = {a[1], a[2], a[4]}, {a[3], a[5], a[6]}
        assert len(p_) == 1 and len(q_) == 1
        return sp.Integer(a[0]) + a[1] * AL + a[3] * ALB
    X = sp.Matrix([[ord_val(t, k) for k in reg] for t in range(K)])

    Dm = {}
    for gauge in (0, 1):
        PH = sp.Matrix([brauer(MODS[nm], gauge) for nm in NAMES])
        if gauge == 0:
            R["E_Phi_invertible"] = (sp.simplify(PH.det()) != 0)
        Dg = sp.simplify(X * PH.inv())
        Dm[gauge] = Dg
    D = Dm[0]
    R["E_D_nonneg_int"] = all(sp.simplify(D[i, j]).is_integer and sp.simplify(D[i, j]) >= 0
                              for i in range(K) for j in range(6))
    R["E_degree_consistency"] = all(
        sum(int(D[i, j]) * DIMS[NAMES[j]] for j in range(6)) == degs[i] for i in range(K))
    Cm = D.T * D
    R["E_C_symmetric"] = (Cm == Cm.T)
    idx = {nm: j for j, nm in enumerate(NAMES)}
    main_cols = [idx["1"], idx["14"], idx["20"]]
    oth_cols = [idx["4"], idx["4b"], idx["6"]]
    R["E_block_diagonal"] = all(Cm[i, j] == 0 for i in main_cols for j in oth_cols)
    Cmain = sp.Matrix([[Cm[i, j] for j in main_cols] for i in main_cols])
    Coth = sp.Matrix([[Cm[i, j] for j in oth_cols] for i in oth_cols])
    R["E_Cmain_det8"] = (Cmain.det() == 8)
    R["E_Coth_det4"] = (Coth.det() == 4)
    R["E_detC_32"] = (Cm.det() == 32)
    R["E_Cmain_values"] = ([[int(Cmain[i, j]) for j in range(3)] for i in range(3)]
                           == [[4, 2, 2], [2, 3, 1], [2, 1, 2]])
    R["E_Coth_values"] = ([[int(Coth[i, j]) for j in range(3)] for i in range(3)]
                          == [[2, 1, 2], [1, 2, 2], [2, 2, 4]])
    drows = {}
    for t in range(K):
        drows[f"{degs[t]}#{t}"] = [int(D[t, j]) for j in range(6)]
    out["decomposition"] = {
        "columns": NAMES, "rows_by_degree_and_index": drows,
        "readable": {"1": "1̂", "14(주)": "14̂", "15": "1̂+14̂", "21": "1̂+20̂",
                     "35": "1̂+14̂+20̂", "6": "6̂", "10": "4̄̂+6̂", "10̄": "4̂+6̂",
                     "14′": "4̂+4̄̂+6̂"},
        "blocks": {"principal_simples": ["1̂", "14̂", "20̂"],
                   "other_simples": ["4̂", "4̄̂", "6̂"]},
        "Cartan_principal": [[int(Cmain[i, j]) for j in range(3)] for i in range(3)],
        "Cartan_other": [[int(Coth[i, j]) for j in range(3)] for i in range(3)],
        "det": {"principal": 8, "other": 4, "total": 32,
                "note": "det C(주) = 8 = |A₇|₂ (full defect) · 비주 defect 2 → 4"},
    }

    # ── F. 독립 교차확인 ────────────────────────────────────────────────
    PH0 = sp.Matrix([brauer(MODS[nm], 0) for nm in NAMES])
    permchar = []
    for k in reg:
        r = reps[k]
        permchar.append(sp.Integer(sum(1 for i in range(N7) if r[i] == i)))
    R["F_phi6_is_natural"] = all(sp.simplify(PH0[idx["6"], j] - (permchar[j] - 1)) == 0
                                 for j in range(6))
    R["F_phi14_identity"] = all(
        sp.simplify(PH0[idx["14"], j] - (PH0[idx["4"], j] * PH0[idx["4b"], j] - 2)) == 0
        for j in range(6))
    R["F_phi20_identity"] = all(
        sp.simplify(PH0[idx["20"], j]
                    - (PH0[idx["4"], j] * PH0[idx["6"], j] - PH0[idx["4b"], j])) == 0
        for j in range(6))

    # ── G. 게이지 고지 ──────────────────────────────────────────────────
    D1 = Dm[1]
    sw = [idx["1"], idx["4b"], idx["4"], idx["6"], idx["14"], idx["20"]]
    R["G_gauge1_also_nonneg_int"] = all(
        sp.simplify(D1[i, j]).is_integer and sp.simplify(D1[i, j]) >= 0
        for i in range(K) for j in range(6))
    R["G_gauge_is_column_swap"] = all(sp.simplify(D1[i, j] - D[i, sw[j]]) == 0
                                      for i in range(K) for j in range(6))
    C1 = D1.T * D1
    R["G_cartan_gauge_invariant"] = (C1.det() == Cm.det())
    out["gauge"] = {
        "origin": "Brauer lift 의 μ₇(GF(8)) → μ₇(ℂ) 동형 선택(2중)",
        "effect": "반대 게이지 = D 의 4̂↔4̄̂ 열 교환(= 10↔10̄ 행 교환) — 실증",
        "invariant": "Cartan·det·블록 구조는 게이지 불변 ⟹ D 는 라벨링 게이지까지 유일",
    }

    # ── teeth ───────────────────────────────────────────────────────────
    R["teeth_both_gauges_valid"] = (R["G_gauge1_also_nonneg_int"]
                                    and R["G_gauge_is_column_swap"])
    R["teeth_sylow2_noncyclic"] = True      # Sylow-2 = D₄ (선행 관측 확립) — 트리 이론 부적용
    R["teeth_Phi_needed_for_uniqueness"] = R["E_Phi_invertible"]

    ok = bool(all(R.values()))
    out["checks"] = R
    out["scope_honesty"] = {
        "delivered": ("A₇ p=2 완전 D(9×6)·Cartan(주 det 8·비주 det 4·전체 32) + "
                      "6 simple 전부 명시 구성·기약성 전수 + Brauer 문자표 + 게이지 고지"),
        "completes": "a7_cartan_p23_observe 의 'p=2 완전 D·C = 미완' 유보 해소",
        "boundary": ("선행 유보 이유(wild·유일성 비보장)는 **일반론으로 옳다** — 여기서는 "
                     "6 simple 을 전부 명시 구성해 Φ 가 확정되어 유일성이 따라온 것. "
                     "일반 wild 블록에 대한 방법 주장 아님."),
        "not_claimed": "봉인 게이트·Erdmann 분류 인용·p=2 사영 분해가능 모듈의 구조(Loewy 층)",
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "A7-CARTAN-P2.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("A₇ p=2 완전 D·Cartan (결정적 — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  ★A₇⊂GL(4,2) 명시(Fano H=168 → 15코셋 → 35선 → 4차원 몫)", flush=True)
        print("  ★6 simple {1,4,4̄,6,14,20} 전부 명시 구성·기약성 전수(궤도 1/1/1/3/27/478)",
              flush=True)
        print("  ★D 유일: 1→1̂·14→14̂·15→1̂+14̂·21→1̂+20̂·35→1̂+14̂+20̂·6→6̂·10→4̄̂+6̂·"
              "10̄→4̂+6̂·14′→4̂+4̄̂+6̂", flush=True)
        print("  ★C(주)det=8=|A₇|₂ · C(비주)det=4 · det C=32 · 게이지=4̂↔4̄̂ 열교환(불변량 동일)",
              flush=True)
        print("  → .pgf/proofs/A7-CARTAN-P2.json", flush=True)
    print(f"a7_cartan_p2_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
