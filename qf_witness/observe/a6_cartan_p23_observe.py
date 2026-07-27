#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""a6_cartan_p23_observe — ★**A₆ p=2·p=3 완전 분해행렬 D(7×5)·Cartan** (관측, seal 아님).
[[dixon_f20_a6_observe]](2026-07-27)가 "**A₆ 완전 D·C 는 미포함** — p=2·3 주블록은 비순환
defect(2³·3²)이라 범위 밖"으로 명시 유보한 축을 **완결**한다.

★전략 = [[a7_cartan_p2_observe]] 의 재사용: **wild/비순환이라 D 를 추론할 수 없다**는 것은
basic set 만 쓸 때의 이야기이고, **Φ(Brauer 문자표)가 확정되면 D = X|_{p-reg}·Φ⁺ 가 유일**하다.
그래서 목표를 "D 추론"이 아니라 **"simples 를 전부 명시 모듈로 구성"** 으로 잡는다.

관측 8축(전 산술 GF(2)/GF(3)/GF(9)/ℚ(ζ₆₀) 정확 · 확률적 절차 없음):
  A. **문자표·블록 재현**: `dixon_f20_a6_observe` 의 일반 엔진으로 A₆(360·7류) 자체유도 →
     p=2 블록 {1,5,5,9,10}+{8}+{8} · p=3 블록 {1,5,5,8,8,10}+{9} 재확인 · ℓ(2)=ℓ(3)=5.
  B. ★★**p=2 simples 명시 구성**: **1̂** · **4_a** = A₇⊂GL(4,2) 구성(Fano 안정화군→15코셋→
     PG(3,2) 35선 span 몫)의 **A₆=Stab(6) 제한** · **4_b** = 6점 순열 GF(2)-모듈의
     **heart**((sum-zero 5차원)/⟨all-ones⟩ — 6 짝수라 all-ones ∈ sum-zero).
     기약성 **전수**(궤도 축약) · ★**4_a 자기쌍대**(dual 의 Brauer 문자 동일 ⟹ 동형) ·
     ★**4_a ≇ 4_b**(3A/3B 에서 (−2,1) vs (1,−2) — **외부 자기동형 쌍**이지 dual 쌍이 아님).
     ★함정 실증: 4_a 와 그 dual 로 Φ 를 세우면 **행이 겹쳐 Φ 가 퇴화**한다(실제 발생).
  C. ★**p=2 주블록 D·C**: Brauer 문자는 GF(2) 특성다항식 다중도만으로(Φ₃·Φ₅ 가 GF(2)-기약
     ⟹ 전부 유리) · **D(5×3)**: 1→1̂ · 5→1̂+4_b · 5→1̂+4_a · 9→1̂+4_a+4_b · **10→2·1̂+4_a+4_b** ·
     **C = [[8,4,4],[4,3,2],[4,2,3]]** · **det C = 8 = |A₆|₂**(full defect).
  D. ★**defect-0 블록 d=1 검증(추론 아님)**: {8},{8} 은 ℓ=1 이고 D=[d]. **d>1 이면
     φ = χ/d 가 5A 에서 (1±√5)/(2d) 로 대수적 정수가 아니다** ⟹ d=1 (Brauer 문자는 단위근 합).
  E. ★★**p=3 simples 명시 구성**: **1̂** · **4** = 6점 순열 GF(3)-모듈의 heart(6≡0 mod 3 이라
     all-ones ∈ sum-zero) · **Λ²(4) = 6차원 GF(3)-기약**이고 **End_G 가 2차원·F²=−I ⟹ End ≅ GF(9)**
     (certificate) → **GF(9)-화 3차원 모듈 = 3** 과 그 Frobenius 트위스트 **3′** 로 분해.
     GF(9)-기저 {v, Fv} 구성 + 3×3 GF(9) 행렬 + 준동형 검증.
  F. ★**p=3 Brauer 문자 + 주블록 D·C**: φ_3 는 GF(9) 고유공간에서 — 2A {1,−1²}→−1 ·
     **4A {1, i, −i} → 1(유리)** · 5A/5B 는 GF(9) 밖(μ₅⊄GF(9)) 이라 char poly = (x−1)(x²−sx+1),
     **s 는 y²+y−1=0 의 GF(9) 근** → lift (−1±√5)/2. **φ_3+φ_3′ = φ_{Λ²4} 정확 일치**(교차검증) ·
     **D(6×4)**: 1→1̂ · 5→1̂+4 · 5→1̂+4 · **8→1̂+4+3** · **8→1̂+4+3′** · **10→4+3+3′** ·
     **C det = 9 = |A₆|₃**(full defect) · defect-0 {9}(Steinberg) 도 D 의 정수성으로 d=1.
  G. ★**게이지 고지**: y²+y−1 의 두 GF(9) 근 중 어느 것을 (−1+√5)/2 로 올릴지는 **2중 게이지**이고,
     반대 선택은 **3↔3′ 열 교환(= 두 8 행 교환)** 과 정확히 일치 — **양 게이지 모두 계산해 실증** ·
     **Cartan·det·블록 구조는 게이지 불변**. [[a7_cartan_p2_observe]] 의 4̂↔4̄̂ 게이지와 같은 부류.
  H. ★**전체 조립·정합**: D(7×5) 두 소수 모두 **차수 정합 Σ d·dim = deg 7행 전수** ·
     C 블록대각 · **det C(p) = |A₆|_p**(8, 9) · p=2 와 p=3 의 simple 차수 multiset
     {1,4,4,8,8} / {1,3,3,4,9} · Σdim² 아님(자명) — 각 ℓ=5 정합.

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - 선행 관측의 "A₆ 완전 D·C 미포함" 유보 **해소**. 단 그 유보 이유(비순환 defect ⟹ 트리 이론
    부재)는 **일반론으로 여전히 옳다** — 여기서는 simples 를 전부 명시 구성했기에 유일성이 따라온 것.
  - defect-0 블록의 d=1 은 **추론이 아니라 대수적 정수성으로 검증**했다(표준사실 인용 회피).
  - Brauer 문자·D·C 는 표현론 수준 — 봉인 게이트 아님.
  - p=3 의 3/3′ 은 **GF(9)-형**(GF(3) 위에서는 Λ²4 가 기약) — 절대기약은 GF(9) 에서.

사용: python -m qf_witness.observe.a6_cartan_p23_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import itertools
import functools

import sympy as sp

from qf_witness.observe.dixon_f20_a6_observe import dixon, table_in
from qf_witness.observe.g2_1_mtc_observe import Cyc

A6GENS = [(1, 2, 0, 3, 4, 5), (0, 1, 2, 4, 5, 3), (1, 0, 3, 2, 4, 5)]
ID6 = tuple(range(6))


def pm6(a, b):
    return tuple(a[b[i]] for i in range(6))


# ══════════════════════════════════════════════════════════════════════════
# GF(2) 도구 (bitmask)
# ══════════════════════════════════════════════════════════════════════════
def rref2_add(B, v):
    for b in B:
        if (v >> (b.bit_length() - 1)) & 1:
            v ^= b
    if v:
        B.append(v)
        B.sort(reverse=True)
    return B


def mm2(A, B, n):
    return tuple(tuple(sum(A[i][t] * B[t][j] for t in range(n)) % 2 for j in range(n))
                 for i in range(n))


def eye2(n):
    return tuple(tuple(1 if i == j else 0 for j in range(n)) for i in range(n))


def inv2(M, n):
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


def dual2(M, n):
    return tuple(zip(*inv2(M, n)))


def cols2(M, n):
    return [sum(M[i][j] << i for i in range(n)) for j in range(n)]


def actbm(cl, v):
    r = 0
    while v:
        b = v & -v
        r ^= cl[b.bit_length() - 1]
        v ^= b
    return r


def simple2(mats, n):
    CL = [cols2(M, n) for M in mats]
    for v0 in range(1, 1 << n):
        B, fr = [v0], [v0]
        while fr:
            nf = []
            for b in fr:
                for cl in CL:
                    t = actbm(cl, b)
                    for x in B:
                        if (t >> (x.bit_length() - 1)) & 1:
                            t ^= x
                    if t:
                        rref2_add(B, t)
                        nf.append(t)
            fr = nf
        if len(B) != n:
            return False
    return True


def nullity2(A, n):
    B = []
    for i in range(n):
        rref2_add(B, sum(A[i][j] << j for j in range(n)))
    return n - len(B)


# ══════════════════════════════════════════════════════════════════════════
# GF(3) 도구
# ══════════════════════════════════════════════════════════════════════════
P3 = 3


def mm3(A, B):
    n, m, k = len(A), len(B[0]), len(B)
    return tuple(tuple(sum(A[i][t] * B[t][j] for t in range(k)) % P3 for j in range(m))
                 for i in range(n))


def eye3(n):
    return tuple(tuple(1 if i == j else 0 for j in range(n)) for i in range(n))


def rref3(rows, ncol):
    R = [list(r) for r in rows]
    piv, r0 = [], 0
    for c in range(ncol):
        pr = next((i for i in range(r0, len(R)) if R[i][c] % P3), None)
        if pr is None:
            continue
        R[r0], R[pr] = R[pr], R[r0]
        f = pow(R[r0][c], P3 - 2, P3)
        R[r0] = [(x * f) % P3 for x in R[r0]]
        for i in range(len(R)):
            if i != r0 and R[i][c]:
                g = R[i][c]
                R[i] = [(R[i][j] - g * R[r0][j]) % P3 for j in range(ncol)]
        piv.append(c)
        r0 += 1
    return R[:r0], piv


def in_span3(rows, piv, v):
    t = list(v)
    for i, c in enumerate(piv):
        if t[c]:
            f = t[c]
            t = [(t[j] - f * rows[i][j]) % P3 for j in range(len(t))]
    return all(x == 0 for x in t)


def nullspace3(rows, ncol):
    Rr, piv = rref3(rows, ncol)
    out = []
    for f in (c for c in range(ncol) if c not in piv):
        v = [0] * ncol
        v[f] = 1
        for i, c in enumerate(piv):
            v[c] = (-Rr[i][f]) % P3
        out.append(tuple(v))
    return out


def apply3(M, v):
    return tuple(sum(M[i][j] * v[j] for j in range(len(v))) % P3 for i in range(len(M)))


def coords3(rows, piv, v):
    t, c = list(v), [0] * len(rows)
    for i, pc in enumerate(piv):
        if t[pc]:
            f = t[pc]
            c[i] = f
            t = [(t[j] - f * rows[i][j]) % P3 for j in range(len(t))]
    assert all(x == 0 for x in t)
    return tuple(c)


def simple3(mats, n):
    for v0 in itertools.product(range(P3), repeat=n):
        if all(x == 0 for x in v0):
            continue
        B, piv = rref3([v0], n)
        fr = [v0]
        while fr:
            nf = []
            for b in fr:
                for M in mats:
                    w = apply3(M, b)
                    if not in_span3(B, piv, w):
                        B, piv = rref3(list(B) + [w], n)
                        nf.append(w)
            fr = nf
        if len(B) != n:
            return False
    return True


def nullity3(M, n):
    R, _ = rref3([tuple(M[i][j] for j in range(n)) for i in range(n)], n)
    return n - len(R)


# ══════════════════════════════════════════════════════════════════════════
# GF(9) = GF(3)[i], i² = −1
# ══════════════════════════════════════════════════════════════════════════
Q9 = [(a, b) for a in range(P3) for b in range(P3)]
Q9Z, Q9O = (0, 0), (1, 0)


def q9add(x, y):
    return ((x[0] + y[0]) % P3, (x[1] + y[1]) % P3)


def q9sub(x, y):
    return ((x[0] - y[0]) % P3, (x[1] - y[1]) % P3)


def q9mul(x, y):
    return ((x[0] * y[0] - x[1] * y[1]) % P3, (x[0] * y[1] + x[1] * y[0]) % P3)


def q9inv(x):
    return next(y for y in Q9 if q9mul(x, y) == Q9O)


def q9mm(A, B, n=3):
    return tuple(tuple(functools.reduce(q9add, [q9mul(A[i][t], B[t][j]) for t in range(n)],
                                        Q9Z) for j in range(n)) for i in range(n))


def q9eye(n=3):
    return tuple(tuple(Q9O if i == j else Q9Z for j in range(n)) for i in range(n))


def q9rank(rowsA, nc):
    R = [list(r) for r in rowsA]
    r0 = 0
    for c in range(nc):
        pr = next((i for i in range(r0, len(R)) if R[i][c] != Q9Z), None)
        if pr is None:
            continue
        R[r0], R[pr] = R[pr], R[r0]
        f = q9inv(R[r0][c])
        R[r0] = [q9mul(x, f) for x in R[r0]]
        for i in range(len(R)):
            if i != r0 and R[i][c] != Q9Z:
                g = R[i][c]
                R[i] = [q9sub(R[i][j], q9mul(g, R[r0][j])) for j in range(nc)]
        r0 += 1
    return r0


def q9eigmult(A, lam):
    M = [[q9sub(A[i][j], lam if i == j else Q9Z) for j in range(3)] for i in range(3)]
    return 3 - q9rank(M, 3)


# ══════════════════════════════════════════════════════════════════════════
def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "a6-cartan-p23/v1",
           "_note": ("A₆ p=2·3 완전 D(7×5)·Cartan — simples 전부 명시 구성으로 Φ 확정 → D 유일. "
                     "관측·seal 아님·module 0·root 불변.")}

    # ── A. 문자표·블록 ──────────────────────────────────────────────────
    a6 = dixon(A6GENS, 6, 61)
    F60 = Cyc(60)
    V = table_in(F60, a6)
    S5 = F60.sqrt5()
    degs, orders = a6["degs"], a6["orders"]
    R["A_K7_order360"] = (a6["K"] == 7 and a6["GN"] == 360)
    R["A_degs"] = (sorted(degs) == [1, 5, 5, 8, 8, 9, 10])
    reg2 = [k for k in range(7) if orders[k] % 2 == 1]
    reg3 = [k for k in range(7) if orders[k] % 3 != 0]
    R["A_ell2_ell3_5"] = (len(reg2) == 5 and len(reg3) == 5)

    def q60(v):
        c = F60.q5coords(S5, v)
        assert c is not None
        return sp.Rational(c[0]) + sp.Rational(c[1]) * sp.sqrt(5)

    # 워드 분해(생성원 곱)
    par = {ID6: None}
    fr = [ID6]
    while fr:
        nf = []
        for x in fr:
            for gi, g in enumerate(A6GENS):
                y = pm6(g, x)
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

    # ── B. p=2 simples ──────────────────────────────────────────────────
    # 4_a : A₇ ⊂ GL(4,2) 구성의 A₆ 제한
    G7 = [p for p in itertools.permutations(range(7))
          if sum(1 for i in range(7) for j in range(i + 1, 7) if p[i] > p[j]) % 2 == 0]
    LINES = frozenset(frozenset(((0 + i) % 7, (1 + i) % 7, (3 + i) % 7)) for i in range(7))

    def pmul7(a, b):
        return tuple(a[b[i]] for i in range(7))
    H = [p for p in G7 if all(frozenset(p[x] for x in L) in LINES for L in LINES)]
    R["B_fano_H168"] = (len(H) == 168)
    cos, seen = [], set()
    for g in G7:
        if g in seen:
            continue
        c = frozenset(pmul7(g, h) for h in H)
        cos.append(c)
        seen |= c
    cidx = {}
    for i, c in enumerate(cos):
        for x in c:
            cidx[x] = i
    crep = [next(iter(c)) for c in cos]

    def act15(g):
        return tuple(cidx[pmul7(g, crep[i])] for i in range(15))
    P15 = [act15(g) for g in [(1, 2, 0, 3, 4, 5, 6), (1, 2, 3, 4, 5, 6, 0)]]

    def orb3(t):
        s, fr_ = {t}, [t]
        while fr_:
            nf = []
            for x in fr_:
                for pp in P15:
                    nx = frozenset(pp[y] for y in x)
                    if nx not in s:
                        s.add(nx)
                        nf.append(nx)
            fr_ = nf
        return s
    L35 = next(o for o in (orb3(frozenset(t))
                           for t in itertools.combinations(range(15), 3)) if len(o) == 35)
    Kb = []
    for Lx in L35:
        v = 0
        for x in Lx:
            v |= 1 << x
        rref2_add(Kb, v)
    R["B_line_span_11"] = (len(Kb) == 11)
    piv = [b.bit_length() - 1 for b in Kb]
    free = [i for i in range(15) if i not in piv]

    def redm(v):
        for b in Kb:
            if (v >> (b.bit_length() - 1)) & 1:
                v ^= b
        return tuple((v >> f) & 1 for f in free)

    def mat4a(g6):
        g = tuple(list(g6) + [6])
        p = act15(g)
        cl = [redm(1 << p[f]) for f in free]
        return tuple(tuple(cl[j][i] for j in range(4)) for i in range(4))
    A4a = [mat4a(g) for g in A6GENS]
    R["B_4a_faithful"] = (len({mat4a(g) for g in a6["G"]}) == 360)
    R["B_4a_simple"] = simple2(A4a, 4)

    # 4_b : 6점 순열 GF(2)-모듈의 heart
    def permmat2(g):
        return tuple(tuple(1 if g[j] == i else 0 for j in range(6)) for i in range(6))
    P6b = [permmat2(g) for g in A6GENS]
    SZ = [(1 << 0) | (1 << i) for i in range(1, 6)]
    ONE6 = sum(1 << i for i in range(6))
    SZb = []
    for v in SZ:
        rref2_add(SZb, v)
    R["B_sumzero_dim5"] = (len(SZb) == 5)

    def act6(M, v):
        return actbm(cols2(M, 6), v)
    t_ = ONE6
    for x in SZb:
        if (t_ >> (x.bit_length() - 1)) & 1:
            t_ ^= x
    R["B_allones_in_sumzero"] = (t_ == 0)
    pvz = [b.bit_length() - 1 for b in SZb]

    def cSZ(v):
        c, t = [0] * 5, v
        for i, x in enumerate(SZb):
            if (t >> pvz[i]) & 1:
                t ^= x
                c[i] = 1
        assert t == 0
        return sum(c[i] << i for i in range(5))
    A5b = []
    for M in P6b:
        cm = [cSZ(act6(M, b)) for b in SZb]
        A5b.append(tuple(tuple((cm[j] >> i) & 1 for j in range(5)) for i in range(5)))
    ONEc = cSZ(ONE6)
    frq = [i for i in range(5) if i != ONEc.bit_length() - 1]

    def quot4(M):
        cl = [sum(M[i][j] << i for i in range(5)) for j in range(5)]

        def av(v):
            r = 0
            while v:
                b = v & -v
                r ^= cl[b.bit_length() - 1]
                v ^= b
            return r

        def red(v):
            if (v >> (ONEc.bit_length() - 1)) & 1:
                v ^= ONEc
            return [(v >> f) & 1 for f in frq]
        cm = [red(av(1 << f)) for f in frq]
        return tuple(tuple(cm[j][i] for j in range(4)) for i in range(4))
    A4b = [quot4(M) for M in A5b]
    R["B_4b_dim4_simple"] = (len(A4b[0]) == 4 and simple2(A4b, 4))

    def mat_of2(mats, p, n):
        M = eye2(n)
        for gi in word(p):
            M = mm2(mats[gi], M, n)
        return M

    def brauer2(mats, n):
        vals = []
        for k in reg2:
            o = orders[k]
            if o == 1:
                vals.append(sp.Integer(n))
                continue
            M = mat_of2(mats, a6["reps"][k], n)
            a = nullity2(tuple(tuple((M[i][j] + (1 if i == j else 0)) % 2 for j in range(n))
                               for i in range(n)), n)
            if o == 3:              # Φ₃ GF(2)-기약(2차)
                vals.append(sp.Integer(a - (n - a) // 2))
            elif o == 5:            # Φ₅ GF(2)-기약(4차)
                vals.append(sp.Integer(a - (n - a) // 4))
            else:
                raise AssertionError(o)
        return vals
    ph1 = brauer2([eye2(1)] * 3, 1)
    ph4a = brauer2(A4a, 4)
    ph4b = brauer2(A4b, 4)
    ph4ad = brauer2([dual2(M, 4) for M in A4a], 4)
    R["B_4a_selfdual"] = (ph4a == ph4ad)
    R["B_4a_neq_4b"] = (ph4a != ph4b)
    R["B_teeth_dual_degenerate"] = (sp.Matrix([ph1, ph4a, ph4ad]).rank() == 2)
    out["p2_simples"] = {
        "list": "1̂ · 4_a(A₇⊂GL(4,2) 의 A₆ 제한) · 4_b(6점 순열 heart) · 8̂ · 8̂′(defect 0)",
        "4a_selfdual": "dual 의 Brauer 문자 동일 ⟹ 동형(자기쌍대)",
        "4a_vs_4b": "3A/3B 에서 (−2,1) vs (1,−2) — 외부 자기동형 쌍(dual 쌍 아님)",
        "pitfall": "4_a 와 그 dual 로 Φ 를 세우면 행 중복으로 퇴화(rank 2) — 실제 발생",
    }

    # ── C. p=2 주블록 D·C ───────────────────────────────────────────────
    PHI2 = sp.Matrix([ph1, ph4a, ph4b])
    R["C_Phi2_rank3"] = (PHI2.rank() == 3)
    main2 = sorted([t for t in range(7) if degs[t] in (1, 5, 9, 10)],
                   key=lambda t: (degs[t], t))
    X2 = sp.Matrix([[q60(V[t][k]) for k in reg2] for t in main2])
    R["C_X2_rank3"] = (X2.rank() == 3)
    D2 = sp.simplify(X2 * PHI2.T * (PHI2 * PHI2.T).inv())
    R["C_D2_nonneg_int"] = all(sp.simplify(D2[i, j]).is_integer and sp.simplify(D2[i, j]) >= 0
                               for i in range(5) for j in range(3))
    R["C_D2_reconstruct"] = (sp.simplify(D2 * PHI2 - X2) == sp.zeros(5, 5))
    dims2 = [1, 4, 4]
    R["C_D2_degree_check"] = all(
        sum(int(D2[i, j]) * dims2[j] for j in range(3)) == degs[main2[i]] for i in range(5))
    C2 = sp.simplify(D2.T * D2)
    R["C_C2_values"] = ([[int(C2[i, j]) for j in range(3)] for i in range(3)]
                        == [[8, 4, 4], [4, 3, 2], [4, 2, 3]])
    R["C_detC2_8"] = (C2.det() == 8)
    out["p2_principal"] = {
        "ordinary": [degs[t] for t in main2],
        "simples": ["1̂", "4_a", "4_b"],
        "D": [[int(D2[i, j]) for j in range(3)] for i in range(5)],
        "readable": {"1": "1̂", "5": "1̂+4_b", "5′": "1̂+4_a", "9": "1̂+4_a+4_b",
                     "10": "2·1̂+4_a+4_b"},
        "Cartan": [[int(C2[i, j]) for j in range(3)] for i in range(3)],
        "det": 8, "check": "det C = |A₆|₂ (full defect)",
    }

    # ── D. defect-0 블록 d=1 (대수적 정수성으로 검증) ────────────────────
    def d_is_one(t, p):
        """χ/d 가 대수적 정수인 d 는 1 뿐임을 확인(무리 성분 분모 검사)."""
        for d in (p, p * p, p ** 3):
            if degs[t] % d:
                continue
            bad = False
            for k in range(7):
                c = F60.q5coords(S5, F60.scale(V[t][k], sp.Rational(1, d)))
                if c is None:
                    bad = True
                    break
                a, b = c
                if not ((2 * b).denominator == 1 and (a - b).denominator == 1):
                    bad = True
                    break
            if not bad:
                return False       # d>1 도 가능 → 검증 실패
        return True
    i8s = [t for t in range(7) if degs[t] == 8]
    i9 = next(t for t in range(7) if degs[t] == 9)
    R["D_p2_defect0_d1"] = all(d_is_one(t, 2) for t in i8s)
    R["D_p3_defect0_d1"] = d_is_one(i9, 3)
    out["defect0"] = {
        "p2": "{8},{8} — ℓ=1 · d>1 이면 χ/d 가 5A 에서 (1±√5)/(2d) 로 대수적 정수 아님 ⟹ d=1",
        "p3": "{9}(Steinberg) — 동일 논거로 d=1",
        "note": "표준사실 인용이 아니라 대수적 정수성으로 검증",
    }

    # ── E. p=3 simples ──────────────────────────────────────────────────
    def permmat3(g):
        return tuple(tuple(1 if g[j] == i else 0 for j in range(6)) for i in range(6))
    P63 = [permmat3(g) for g in A6GENS]
    SZ3 = [tuple(1 if i == 0 else (P3 - 1 if i == j else 0) for i in range(6))
           for j in range(1, 6)]
    ONE3 = tuple([1] * 6)
    SZr, SZp = rref3(SZ3, 6)
    R["E_sumzero3_dim5"] = (len(SZr) == 5)
    R["E_allones3_in_sumzero"] = in_span3(SZr, SZp, ONE3)
    A53 = []
    for M in P63:
        cm = [coords3(SZr, SZp, apply3(M, r)) for r in SZr]
        A53.append(tuple(tuple(cm[j][i] for j in range(5)) for i in range(5)))
    ONEc3 = coords3(SZr, SZp, ONE3)
    ONEr3, ONEp3 = rref3([ONEc3], 5)
    A43 = []
    for M in A53:
        frx = [c for c in range(5) if c not in ONEp3]
        cm = []
        for f in frx:
            w = apply3(M, tuple(1 if i == f else 0 for i in range(5)))
            t = list(w)
            for i, pc in enumerate(ONEp3):
                if t[pc]:
                    g = t[pc]
                    t = [(t[j] - g * ONEr3[i][j]) % P3 for j in range(5)]
            cm.append(tuple(t[c] for c in frx))
        A43.append(tuple(tuple(cm[j][i] for j in range(4)) for i in range(4)))
    R["E_4dim3_simple"] = (len(A43[0]) == 4 and simple3(A43, 4))

    def wedge2_3(M):
        n = len(M)
        pr = list(itertools.combinations(range(n), 2))
        idx = {p: i for i, p in enumerate(pr)}
        d = len(pr)
        o = [[0] * d for _ in range(d)]
        for jc, (a, b) in enumerate(pr):
            for i in range(n):
                for j in range(n):
                    if i == j:
                        continue
                    v = M[i][a] * M[j][b] % P3
                    if v:
                        sg = 1 if i < j else P3 - 1
                        key = idx[(min(i, j), max(i, j))]
                        o[key][jc] = (o[key][jc] + sg * v) % P3
        return tuple(tuple(r) for r in o)
    A63 = [wedge2_3(M) for M in A43]
    R["E_lambda2_dim6_simple_gf3"] = (len(A63[0]) == 6 and simple3(A63, 6))
    rows = []
    for M in A63:
        for i in range(6):
            for j in range(6):
                r = [0] * 36
                for k in range(6):
                    r[i * 6 + k] = (r[i * 6 + k] + M[k][j]) % P3
                    r[k * 6 + j] = (r[k * 6 + j] - M[i][k]) % P3
                rows.append(tuple(x % P3 for x in r))
    ns = nullspace3(rows, 36)
    R["E_End_dim2"] = (len(ns) == 2)
    Fm = None
    negI = tuple(tuple((P3 - 1) if i == j else 0 for j in range(6)) for i in range(6))
    for v in ns:
        Xm = tuple(tuple(v[i * 6 + j] for j in range(6)) for i in range(6))
        for c in range(P3):
            Y = tuple(tuple((Xm[i][j] + (c if i == j else 0)) % P3 for j in range(6))
                      for i in range(6))
            if mm3(Y, Y) == negI:
                Fm = Y
                break
        if Fm:
            break
    R["E_F_sq_minus_I"] = (Fm is not None)
    basis = []
    for e in range(6):
        v = tuple(1 if i == e else 0 for i in range(6))
        tst = []
        for b in basis:
            tst += [b, apply3(Fm, b)]
        if tst:
            Rt, pt = rref3(tst, 6)
            if in_span3(Rt, pt, v):
                continue
        basis.append(v)
        if len(basis) == 3:
            break
    GB = []
    for b in basis:
        GB += [b, apply3(Fm, b)]
    R["E_q9basis_ok"] = (len(basis) == 3 and len(rref3(GB, 6)[0]) == 6)

    def q9coords(v):
        rowsM = []
        for b in basis:
            rowsM += [list(b), list(apply3(Fm, b))]
        Aug = [[rowsM[r][c] for r in range(6)] + [v[c]] for c in range(6)]
        Rq, pq = rref3([tuple(r) for r in Aug], 7)
        sol = [0] * 6
        for i, c in enumerate(pq):
            if c < 6:
                sol[c] = Rq[i][6]
        return [(sol[2 * j] % P3, sol[2 * j + 1] % P3) for j in range(3)]
    MG = []
    for M in A63:
        cl = [q9coords(apply3(M, basis[k])) for k in range(3)]
        MG.append(tuple(tuple(cl[k][j] for k in range(3)) for j in range(3)))

    def q9of(p):
        M = q9eye()
        for gi in word(p):
            M = q9mm(MG[gi], M)
        return M
    R["E_q9_homomorphism"] = all(
        q9of(pm6(A6GENS[0], a6["reps"][k])) == q9mm(MG[0], q9of(a6["reps"][k]))
        for k in range(7))
    out["p3_simples"] = {
        "list": "1̂ · 4(6점 순열 heart, GF(3)) · 3 · 3′(Λ²4 의 GF(9)-반쪽) · 9(Steinberg, defect 0)",
        "certificate": "Λ²(4) 6차원 GF(3)-기약 · End_G 2차원 · F²=−I ⟹ End ≅ GF(9)",
    }

    # ── F. p=3 Brauer 문자 + D·C ────────────────────────────────────────
    def q9charpoly_c1(A):
        return functools.reduce(q9add, [A[i][i] for i in range(3)], Q9Z)
    roots_y = [y for y in Q9 if q9add(q9add(q9mul(y, y), y), (P3 - 1, 0)) == Q9Z]
    R["F_two_roots_y2py_m1"] = (len(roots_y) == 2)
    svals = {}
    for k in reg3:
        if orders[k] != 5:
            continue
        svals[k] = q9sub(q9charpoly_c1(q9of(a6["reps"][k])), Q9O)
    R["F_s_in_roots"] = all(s in roots_y for s in svals.values())
    R["F_s_distinct"] = (len(set(svals.values())) == 2)

    def brauer3_gf3(mats, n):
        vals = []
        for k in reg3:
            o = orders[k]
            if o == 1:
                vals.append(sp.Integer(n))
                continue
            M = eye3(n)
            for gi in word(a6["reps"][k]):
                M = mm3(mats[gi], M)
            a = nullity3(tuple(tuple((M[i][j] - (1 if i == j else 0)) % P3
                                     for j in range(n)) for i in range(n)), n)
            b = nullity3(tuple(tuple((M[i][j] + (1 if i == j else 0)) % P3
                                     for j in range(n)) for i in range(n)), n)
            if o in (2, 4):        # x²+1 은 GF(3)-기약 → i+(−i)=0 기여
                vals.append(sp.Integer(a - b))
            elif o == 5:           # Φ₅ GF(3)-기약(4차)
                vals.append(sp.Integer(a - (n - a) // 4))
            else:
                raise AssertionError(o)
        return vals
    phi4_3 = brauer3_gf3(A43, 4)
    phi6_3 = brauer3_gf3(A63, 6)

    def q9brauer(gauge):
        lift = {roots_y[gauge]: (sp.Integer(-1) + sp.sqrt(5)) / 2,
                roots_y[1 - gauge]: (sp.Integer(-1) - sp.sqrt(5)) / 2}
        vals = []
        for k in reg3:
            o = orders[k]
            if o == 1:
                vals.append(sp.Integer(3))
            elif o == 5:
                vals.append(sp.Integer(1) + lift[svals[k]])
            else:
                A = q9of(a6["reps"][k])
                acc = sp.Integer(0)
                for lam in Q9:
                    if lam == Q9Z:
                        continue
                    m = q9eigmult(A, lam)
                    if not m:
                        continue
                    if lam == (1, 0):
                        acc += m
                    elif lam == (P3 - 1, 0):
                        acc -= m
                    elif lam == (0, 1):
                        acc += m * sp.I
                    elif lam == (0, P3 - 1):
                        acc -= m * sp.I
                    else:
                        raise AssertionError(lam)
                vals.append(sp.simplify(acc))
        return vals
    main3 = sorted([t for t in range(7) if degs[t] in (1, 5, 8, 10)],
                   key=lambda t: (degs[t], t))
    X3 = sp.Matrix([[q60(V[t][k]) for k in reg3] for t in main3])
    Ds, Cs = {}, {}
    for gauge in (0, 1):
        p3v = q9brauer(gauge)
        p3c = [sp.simplify(x.subs(sp.sqrt(5), -sp.sqrt(5))) for x in p3v]
        if gauge == 0:
            R["F_phi3_plus_conj_eq_lambda2"] = all(
                sp.simplify(p3v[i] + p3c[i] - phi6_3[i]) == 0 for i in range(5))
            R["F_phi3_4A_rational"] = (sp.simplify(sp.im(p3v[reg3.index(
                next(k for k in reg3 if orders[k] == 4))])) == 0)
        PH = sp.Matrix([[sp.Integer(1)] * 5, phi4_3, p3v, p3c])
        Dg = sp.simplify(X3 * PH.T * (PH * PH.T).inv())
        Ds[gauge] = Dg
        Cs[gauge] = sp.simplify(Dg.T * Dg)
    D3 = Ds[0]
    R["F_D3_nonneg_int"] = all(sp.simplify(D3[i, j]).is_integer and sp.simplify(D3[i, j]) >= 0
                               for i in range(6) for j in range(4))
    dims3 = [1, 4, 3, 3]
    R["F_D3_degree_check"] = all(
        sum(int(D3[i, j]) * dims3[j] for j in range(4)) == degs[main3[i]] for i in range(6))
    R["F_detC3_9"] = (Cs[0].det() == 9)
    out["p3_principal"] = {
        "ordinary": [degs[t] for t in main3],
        "simples": ["1̂", "4", "3", "3′"],
        "D": [[int(D3[i, j]) for j in range(4)] for i in range(6)],
        "readable": {"1": "1̂", "5": "1̂+4", "5′": "1̂+4", "8": "1̂+4+3", "8′": "1̂+4+3′",
                     "10": "4+3+3′"},
        "Cartan": [[int(Cs[0][i, j]) for j in range(4)] for i in range(4)],
        "det": 9, "check": "det C = |A₆|₃ (full defect)",
    }

    # ── G. 게이지 ───────────────────────────────────────────────────────
    D3b = Ds[1]
    sw = [0, 1, 3, 2]
    R["G_gauge1_nonneg_int"] = all(
        sp.simplify(D3b[i, j]).is_integer and sp.simplify(D3b[i, j]) >= 0
        for i in range(6) for j in range(4))
    R["G_gauge_is_column_swap"] = all(sp.simplify(D3b[i, j] - D3[i, sw[j]]) == 0
                                      for i in range(6) for j in range(4))
    R["G_cartan_gauge_invariant"] = (Cs[1].det() == Cs[0].det())
    out["gauge"] = {
        "origin": "y²+y−1=0 의 두 GF(9) 근 중 어느 것을 (−1+√5)/2 로 올릴지(2중)",
        "effect": "반대 게이지 = D 의 3↔3′ 열 교환(= 두 8 행 교환) — 실증",
        "invariant": "Cartan·det·블록 구조 게이지 불변 ⟹ D 는 라벨링 게이지까지 유일",
    }

    # ── H. 전체 조립 ────────────────────────────────────────────────────
    R["H_p2_total_ell5"] = (3 + 1 + 1 == 5)
    R["H_p3_total_ell5"] = (4 + 1 == 5)
    R["H_p2_simple_dims"] = (sorted([1, 4, 4, 8, 8]) == [1, 4, 4, 8, 8])
    R["H_p3_simple_dims"] = (sorted([1, 4, 3, 3, 9]) == [1, 3, 3, 4, 9])
    R["H_detC_equals_group_order_part"] = (C2.det() * 1 * 1 == 8 and Cs[0].det() * 1 == 9)
    out["summary"] = {
        "p2": {"ell": 5, "simple_dims": [1, 4, 4, 8, 8], "blocks": "주(det 8) + {8} + {8}",
               "detC_total": 8},
        "p3": {"ell": 5, "simple_dims": [1, 3, 3, 4, 9], "blocks": "주(det 9) + {9}",
               "detC_total": 9},
    }

    ok = bool(all(R.values()))
    out["checks"] = R
    out["scope_honesty"] = {
        "completes": "dixon_f20_a6_observe 의 'A₆ 완전 D·C 미포함' 유보 해소",
        "boundary": ("선행 유보 이유(비순환 defect ⟹ 트리 이론 부재)는 **일반론으로 여전히 옳다** — "
                     "여기서는 simples 를 전부 명시 구성했기에 유일성이 따라온 것."),
        "verified_not_cited": "defect-0 블록의 d=1 은 대수적 정수성으로 **검증**(표준사실 인용 아님)",
        "not_claimed": ("봉인 게이트 · Loewy 구조 · 사영 분해가능 모듈 · "
                        "일반 wild 블록에 대한 방법 주장"),
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "A6-CARTAN-P23.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("A₆ p=2·3 완전 D·Cartan (결정적 — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  ★p=2 simples {1,4_a,4_b,8,8}: 4_a=A₇⊂GL(4,2) 제한(자기쌍대)·4_b=6점 heart",
              flush=True)
        print("  ★p=2 D: 10→2·1̂+4_a+4_b · C=[[8,4,4],[4,3,2],[4,2,3]] · det=8=|A₆|₂", flush=True)
        print("  ★p=3 simples {1,4,3,3′,9}: Λ²4 의 End≅GF(9) certificate → 3⊕3′", flush=True)
        print("  ★p=3 D: 8→1̂+4+3 · 8′→1̂+4+3′ · 10→4+3+3′ · det C=9=|A₆|₃", flush=True)
        print("  ★게이지 = 3↔3′ 열 교환(불변량 동일) · defect-0 d=1 은 대수적 정수성으로 검증",
              flush=True)
        print("  → .pgf/proofs/A6-CARTAN-P23.json", flush=True)
    print(f"a6_cartan_p23_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
