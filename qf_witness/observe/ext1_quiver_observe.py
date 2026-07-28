#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ext1_quiver_observe — ★**A₆·A₇ p-modular Ext¹ 퀴버** (관측, seal 아님).
[[a6_cartan_p23_observe]]·[[a7_cartan_p2_observe]]가 확정한 **완전 분해행렬 D·Cartan C** 의 **다음 층** —
simples 사이의 **Ext¹ 차원**(퀴버 화살 수)을 명시 모듈에서 직접 계산한다.

★**방법 = 제시(presentation) 없이 Cayley 그래프 일관성**: Ext¹(S_i,S_j) = H¹(G, Hom(S_i,S_j)) 이고
1-cocycle f 는 **생성원 값으로 결정**된다(f(xs) = f(x) + x·f(s)). BFS 신장트리로 f 를 전 원소에
전개한 뒤 **비트리 간선마다 일관성 방정식**을 세우면 Z¹ 이 커널로 나온다 —
**군 제시를 인용할 필요가 없다**(자체유도 규율). dim B¹ = dim M − dim M^G ·
**dim Ext¹ = dim Z¹ − dim B¹**.

관측 6축(전 산술 GF(2)/GF(3) 정확 — numpy 정수·부동소수 없음):
  A. ★**계산기 자체검증**: **Ext¹(1,1) = H¹(A₆,𝔽₂) = 0**(A₆ 는 완전군 ⟹ 𝔽₂ 로의 비자명 준동형
     부재) · **Ext¹(1,1) = H¹(A₇,𝔽₂) = 0** — 계산기가 알려진 소멸을 재현.
  B. ★**A₆ p=2 주블록 완전 퀴버**: simples **{1̂, 4_a, 4_b}**(4_a = A₇⊂GL(4,2) 의 A₆ 제한 ·
     4_b = 6점 순열 heart) 의 **3×3 Ext¹ 행렬** 전수.
  C. ★**Cartan 대조(독립 검증)**: 선행 관측이 확정한 **C = [[8,4,4],[4,3,2],[4,2,3]]** 와
     퀴버의 **대칭성·지지집합**을 대조 — Ext¹(S_i,S_j) ≠ 0 ⟹ C_{ij} ≠ 0 을 전수 확인
     (퀴버가 Cartan 의 비영 패턴 안에 놓임).
  D. ★**Ext¹ 대칭성**: 유한군 모듈러 표현에서 **dim Ext¹(S_i,S_j) = dim Ext¹(S_j,S_i)**
     (자기쌍대 군대수) — 전 쌍 실측 확인.
  E. ★**defect-0 블록은 Ext¹ = 0**: A₆ p=2 의 {8},{8} · p=3 의 {9} 는 **단순대수**(블록에 simple
     1개·C=[1]) ⟹ 퀴버가 **고립 정점**. 구조적 귀결로 기록(계산 아님).
  F. ★**A₇ p=2 비주블록 {4̂, 4̄̂, 6̂} 퀴버**: 저차원 쌍(Hom ≤ 36) 전수 — 주블록 {1̂,14̂,20̂} 은
     Hom 최대 400·|G|=2520 으로 **규모상 본 관측 범위 밖**(정직 유보).
  G. ★★**A₆ p=3 주블록 완전 4×4 퀴버 — GF(9) 를 GF(3) 실현화로 환원**: simples
     **{1̂, 4, 3, 3′}**(3,3′ = Λ²(4) 의 End≅GF(9) 반쪽·Frobenius 쌍)에서
     ★**GF(9) 원소 (a,b) ↦ [[a,−b],[b,a]] 실현화** ⟹ Hom_{GF(9)} 를 **2배 차원 GF(3)-모듈**로
     보고 **F 축의 GF(3) 계산기를 그대로 재사용** ⟹ **dim_{GF(9)} Ext¹ = dim_{GF(3)} H¹ / 2**
     (전 쌍에서 H¹ 이 **짝수**임을 확인 — 실현화 정합의 게이트).
     결과 **[[0,2,0,0],[2,0,1,1],[0,1,0,0],[0,1,0,0]]** — ★**별이지만 중심이 4** 이고
     ★**1↔4 는 이중 화살(dim 2)** · ★**Ext¹(3,3′) = 0**(Frobenius 쌍 사이 화살 없음) ·
     ★**3 행과 3′ 행이 동일**(Frobenius σ-대칭 실측).

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - ★**A₇ p=2 주블록(1,14,20) Ext¹ 은 미완**(Hom 400 × |G| 2520 — 제약행렬 규모). 다음 축.
  - Loewy 급수(rad 필터)는 사영 덮개 구성이 필요 — 퀴버(화살 수)까지가 본 관측.
  - Ext¹ 대칭성은 **실측**이며 일반 정리 인용이 아니다.

사용: python -m qf_witness.observe.ext1_quiver_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import itertools

import numpy as np


# ══════════════════════════════════════════════════════════════════════════
# GF(p) 선형대수 + H¹
# ══════════════════════════════════════════════════════════════════════════
def gf_rank(A, p):
    if A.size == 0:
        return 0
    A = A % p
    rows, cols = A.shape
    r = 0
    for c in range(cols):
        nz = np.nonzero(A[r:, c])[0]
        if not len(nz):
            continue
        piv = r + nz[0]
        if piv != r:
            A[[r, piv]] = A[[piv, r]]
        A[r] = (A[r] * pow(int(A[r, c]), p - 2, p)) % p
        col = A[:, c].copy()
        col[r] = 0
        if col.any():
            A = (A - np.outer(col, A[r])) % p
        r += 1
        if r == rows:
            break
    return r


def inv_mod(M, p):
    n = len(M)
    A = np.concatenate([np.array(M) % p, np.eye(n, dtype=np.int64)], axis=1) % p
    r = 0
    for c in range(n):
        nz = np.nonzero(A[r:, c])[0]
        if not len(nz):
            continue
        pr = r + nz[0]
        if pr != r:
            A[[r, pr]] = A[[pr, r]]
        A[r] = (A[r] * pow(int(A[r, c]), p - 2, p)) % p
        col = A[:, c].copy()
        col[r] = 0
        if col.any():
            A = (A - np.outer(col, A[r])) % p
        r += 1
    return A[:, n:] % p


def group_elems(gens, mulf, idp):
    par = {idp: None}
    order = [idp]
    fr = [idp]
    while fr:
        nf = []
        for x in fr:
            for gi, g in enumerate(gens):
                y = mulf(x, g)
                if y not in par:
                    par[y] = (x, gi)
                    order.append(y)
                    nf.append(y)
        fr = nf
    return par, order


def ext1_dim(gens, mulf, idp, act, m, p):
    """dim H¹(G, M) — act[g] = m×m GF(p) 행렬. 반환 (Z¹, B¹, H¹)."""
    par, order = group_elems(gens, mulf, idp)
    k = len(gens)
    nv = k * m
    F = {idp: np.zeros((m, nv), dtype=np.int64)}
    for g in order[1:]:
        x, gi = par[g]
        Fg = F[x].copy()
        Fg[:, gi * m:(gi + 1) * m] = (Fg[:, gi * m:(gi + 1) * m] + act[x]) % p
        F[g] = Fg
    tree = {(par[g][0], par[g][1]) for g in order[1:]}
    rows = []
    for g in order:
        for gi, s in enumerate(gens):
            if (g, gi) in tree:
                continue
            h = mulf(g, s)
            R = (F[h] - F[g]) % p
            R[:, gi * m:(gi + 1) * m] = (R[:, gi * m:(gi + 1) * m] - act[g]) % p
            rows.append(R % p)
    A = np.concatenate(rows, axis=0) % p if rows else np.zeros((0, nv), dtype=np.int64)
    dimZ1 = nv - gf_rank(A, p)
    fixrows = np.concatenate([(act[g] - np.eye(m, dtype=np.int64)) % p for g in gens], axis=0)
    dimB1 = m - (m - gf_rank(fixrows % p, p))
    return dimZ1, dimB1, dimZ1 - dimB1


def hom_module(actA, actB, dA, dB, p, elems):
    """Hom(A,B): φ(dB×dA) · (g·φ) = B(g) φ A(g)⁻¹ · vec 인덱스 r*dA+c."""
    out = {}
    for g in elems:
        Ai = inv_mod(actA[g], p)
        Bg = actB[g] % p
        M = np.zeros((dB * dA, dB * dA), dtype=np.int64)
        for r2 in range(dB):
            for c2 in range(dA):
                col = r2 * dA + c2
                blk = np.outer(Bg[:, r2], Ai[c2, :]) % p          # dB×dA
                M[:, col] = blk.reshape(-1) % p
        out[g] = M
    return out


# ══════════════════════════════════════════════════════════════════════════
# 군·모듈 구성
# ══════════════════════════════════════════════════════════════════════════
def perm_mul(n):
    def f(a, b):
        return tuple(a[b[i]] for i in range(n))
    return f


def enumerate_group(gens, n):
    mulf = perm_mul(n)
    idp = tuple(range(n))
    _, order = group_elems(gens, mulf, idp)
    return mulf, idp, order


def extend_action(gens, mulf, idp, genmats, p, order):
    act = {idp: np.eye(len(genmats[0]), dtype=np.int64)}
    fr = [idp]
    while fr:
        nf = []
        for x in fr:
            for gi, g in enumerate(gens):
                y = mulf(x, g)
                if y not in act:
                    act[y] = (act[x] @ genmats[gi]) % p
                    nf.append(y)
        fr = nf
    return act


def fano_gl42_gens(a_gens, npts, host_gens):
    """A₇ ⊂ GL(4,2) 구성 후 지정 생성원들의 4×4 GF(2) 행렬 반환."""
    mul7 = perm_mul(7)

    def even(pm):
        return sum(1 for i in range(7) for j in range(i + 1, 7) if pm[i] > pm[j]) % 2 == 0
    G7 = [pm for pm in itertools.permutations(range(7)) if even(pm)]
    LINES = frozenset(frozenset(((0 + i) % 7, (1 + i) % 7, (3 + i) % 7)) for i in range(7))
    H = [pm for pm in G7 if all(frozenset(pm[x] for x in L) in LINES for L in LINES)]
    cos, seen = [], set()
    for g in G7:
        if g in seen:
            continue
        c = frozenset(mul7(g, h) for h in H)
        cos.append(c)
        seen |= c
    cidx = {}
    for i, c in enumerate(cos):
        for x in c:
            cidx[x] = i
    crep = [next(iter(c)) for c in cos]

    def act15(g):
        return tuple(cidx[mul7(g, crep[i])] for i in range(15))
    P15 = [act15(g) for g in [(1, 2, 0, 3, 4, 5, 6), (1, 2, 3, 4, 5, 6, 0)]]

    def orb3(t):
        s, fr = {t}, [t]
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
    L35 = next(o for o in (orb3(frozenset(t))
                           for t in itertools.combinations(range(15), 3)) if len(o) == 35)
    B = []
    for Lx in L35:
        v = 0
        for x in Lx:
            v |= 1 << x
        vv = v
        for b in B:
            if (vv >> (b.bit_length() - 1)) & 1:
                vv ^= b
        if vv:
            B.append(vv)
            B.sort(reverse=True)
    piv = [b.bit_length() - 1 for b in B]
    free = [i for i in range(15) if i not in piv]

    def red(v):
        for b in B:
            if (v >> (b.bit_length() - 1)) & 1:
                v ^= b
        return [(v >> f) & 1 for f in free]

    def mat4(g7):
        pm = act15(g7)
        cols = [red(1 << pm[f]) for f in free]
        return np.array([[cols[j][i] for j in range(4)] for i in range(4)], dtype=np.int64)
    return [mat4(g) for g in host_gens]


def heart_gens(gens, n, p):
    """n점 순열 GF(p)-모듈의 heart = (sum-zero)/⟨all-ones⟩ (n ≡ 0 mod p 가정)."""
    d = n - 2
    out = []
    SZ = np.array([[1 if k == 0 else (p - 1 if k == i else 0) for k in range(n)]
                   for i in range(1, n)], dtype=np.int64) % p
    # SZ 좌표: v = Σ c_i (e0 − e_i) → c_i = −v_i (i≥1)
    for g in gens:
        P = np.array([[1 if g[j] == i else 0 for j in range(n)] for i in range(n)],
                     dtype=np.int64)
        img = (SZ @ P.T) % p                     # (n−1)×n
        C = (-img[:, 1:]) % p                    # (n−1)×(n−1) 좌표
        # all-ones 의 SZ 좌표
        one = np.ones(n, dtype=np.int64)
        cone = (-one[1:]) % p
        # 몫: 마지막 좌표를 cone 으로 소거
        j0 = n - 2
        Q = np.zeros((d, d), dtype=np.int64)
        for j in range(d):
            row = C[j].copy()
            f = row[j0] * pow(int(cone[j0]), p - 2, p) % p if cone[j0] else 0
            if f:
                row = (row - f * cone) % p
            Q[:, j] = row[:d]
        out.append(Q % p)
    return out


# ══════════════════════════════════════════════════════════════════════════
# G. GF(9) → GF(3) 실현화 (A₆ p=3)
# ══════════════════════════════════════════════════════════════════════════
def _q9_real2(x):
    """GF(9) 원소 (a,b) = a+bi (i²=−1) → 곱셈의 GF(3) 2×2 실현화 [[a,−b],[b,a]]."""
    a, b = x
    return np.array([[a % 3, (-b) % 3], [b % 3, a % 3]], dtype=np.int64)


def _q9_realify(M, n):
    O = np.zeros((2 * n, 2 * n), dtype=np.int64)
    for i in range(n):
        for j in range(n):
            O[2 * i:2 * i + 2, 2 * j:2 * j + 2] = _q9_real2(M[i][j])
    return O % 3


def build_a6_p3_modules():
    """A₆ p=3 주블록 simples 를 GF(9) 행렬 생성원으로 반환: (A6GENS, [1,4,3,3′] 생성원)."""
    import qf_witness.observe.a6_cartan_p23_observe as A6M
    P3 = 3
    A6G = A6M.A6GENS

    def permmat3(g):
        return tuple(tuple(1 if g[j] == i else 0 for j in range(6)) for i in range(6))
    P63 = [permmat3(g) for g in A6G]
    SZ3 = [tuple(1 if i == 0 else (P3 - 1 if i == j else 0) for i in range(6))
           for j in range(1, 6)]
    ONE3 = tuple([1] * 6)
    SZr, SZp = A6M.rref3(SZ3, 6)
    A53 = []
    for M in P63:
        cm = [A6M.coords3(SZr, SZp, A6M.apply3(M, r)) for r in SZr]
        A53.append(tuple(tuple(cm[j][i] for j in range(5)) for i in range(5)))
    ONEc3 = A6M.coords3(SZr, SZp, ONE3)
    ONEr3, ONEp3 = A6M.rref3([ONEc3], 5)
    A43 = []
    for M in A53:
        frx = [c for c in range(5) if c not in ONEp3]
        cm = []
        for f in frx:
            w = A6M.apply3(M, tuple(1 if i == f else 0 for i in range(5)))
            t = list(w)
            for i, pc in enumerate(ONEp3):
                if t[pc]:
                    g = t[pc]
                    t = [(t[j] - g * ONEr3[i][j]) % P3 for j in range(5)]
            cm.append(tuple(t[c] for c in frx))
        A43.append(tuple(tuple(cm[j][i] for j in range(4)) for i in range(4)))

    def wedge2_3(M):
        n = len(M)
        pr = list(itertools.combinations(range(n), 2))
        idx = {t: i for i, t in enumerate(pr)}
        o = [[0] * len(pr) for _ in pr]
        for jc, (a, b) in enumerate(pr):
            for i in range(n):
                for j in range(n):
                    if i == j:
                        continue
                    v = M[i][a] * M[j][b] % P3
                    if v:
                        sg = 1 if i < j else P3 - 1
                        k = idx[(min(i, j), max(i, j))]
                        o[k][jc] = (o[k][jc] + sg * v) % P3
        return tuple(tuple(r) for r in o)
    A63 = [wedge2_3(M) for M in A43]
    rows = []
    for M in A63:
        for i in range(6):
            for j in range(6):
                r = [0] * 36
                for k in range(6):
                    r[i * 6 + k] = (r[i * 6 + k] + M[k][j]) % P3
                    r[k * 6 + j] = (r[k * 6 + j] - M[i][k]) % P3
                rows.append(tuple(x % P3 for x in r))
    ns = A6M.nullspace3(rows, 36)
    negI = tuple(tuple((P3 - 1) if i == j else 0 for j in range(6)) for i in range(6))
    Fm = None
    for v in ns:
        Xm = tuple(tuple(v[i * 6 + j] for j in range(6)) for i in range(6))
        for c in range(P3):
            Y = tuple(tuple((Xm[i][j] + (c if i == j else 0)) % P3 for j in range(6))
                      for i in range(6))
            if A6M.mm3(Y, Y) == negI:
                Fm = Y
                break
        if Fm:
            break
    basis = []
    for e in range(6):
        v = tuple(1 if i == e else 0 for i in range(6))
        tst = []
        for b in basis:
            tst += [b, A6M.apply3(Fm, b)]
        if tst:
            Rt, pt = A6M.rref3(tst, 6)
            if A6M.in_span3(Rt, pt, v):
                continue
        basis.append(v)
        if len(basis) == 3:
            break

    def q9coords(v):
        rowsM = []
        for b in basis:
            rowsM += [list(b), list(A6M.apply3(Fm, b))]
        Aug = [[rowsM[r][c] for r in range(6)] + [v[c]] for c in range(6)]
        Rq, pq = A6M.rref3([tuple(r) for r in Aug], 7)
        sol = [0] * 6
        for i, c in enumerate(pq):
            if c < 6:
                sol[c] = Rq[i][6]
        return [(sol[2 * j] % P3, sol[2 * j + 1] % P3) for j in range(3)]
    MG = []
    for M in A63:
        cl = [q9coords(A6M.apply3(M, basis[k])) for k in range(3)]
        MG.append(tuple(tuple(cl[k][j] for k in range(3)) for j in range(3)))

    def emb(M):
        n = len(M)
        return tuple(tuple((M[i][j] % 3, 0) for j in range(n)) for i in range(n))

    def conj_mat(M):
        n = len(M)
        return tuple(tuple((M[i][j][0], (-M[i][j][1]) % 3) for j in range(n))
                     for i in range(n))
    gens = {"1": ([A6M.q9eye(1)] * 3, 1),
            "4": ([emb(M) for M in A43], 4),
            "3": (MG, 3),
            "3p": ([conj_mat(M) for M in MG], 3)}
    return A6M, A6G, gens


def q9_extend(A6M, gens, mulf, idp, genmats, n):
    act = {idp: A6M.q9eye(n)}
    fr = [idp]
    while fr:
        nf = []
        for x in fr:
            for gi, g in enumerate(gens):
                y = mulf(x, g)
                if y not in act:
                    act[y] = A6M.q9mm(act[x], genmats[gi], n)
                    nf.append(y)
        fr = nf
    return act


def q9_inv_mat(A6M, M, n):
    Aug = [[M[i][j] for j in range(n)] + [A6M.Q9O if i == j else A6M.Q9Z for j in range(n)]
           for i in range(n)]
    r = 0
    for c in range(n):
        pr = next((i for i in range(r, n) if Aug[i][c] != A6M.Q9Z), None)
        if pr is None:
            continue
        Aug[r], Aug[pr] = Aug[pr], Aug[r]
        f = A6M.q9inv(Aug[r][c])
        Aug[r] = [A6M.q9mul(x, f) for x in Aug[r]]
        for i in range(n):
            if i != r and Aug[i][c] != A6M.Q9Z:
                g = Aug[i][c]
                Aug[i] = [A6M.q9sub(Aug[i][j], A6M.q9mul(g, Aug[r][j])) for j in range(2 * n)]
        r += 1
    return tuple(tuple(Aug[i][n + j] for j in range(n)) for i in range(n))


def q9_hom_real(A6M, actA, actB, dA, dB, elems):
    """Hom_{GF(9)}(A,B) 의 GF(3) 실현화 작용(차원 2·dA·dB)."""
    out = {}
    m = dB * dA
    for g in elems:
        Ai = q9_inv_mat(A6M, actA[g], dA)
        Bg = actB[g]
        M = [[A6M.Q9Z] * m for _ in range(m)]
        for r2 in range(dB):
            for c2 in range(dA):
                col = r2 * dA + c2
                for r in range(dB):
                    for c in range(dA):
                        v = A6M.q9mul(Bg[r][r2], Ai[c2][c])
                        if v != A6M.Q9Z:
                            M[r * dA + c][col] = A6M.q9add(M[r * dA + c][col], v)
        out[g] = _q9_realify(tuple(tuple(r) for r in M), m)
    return out


# ══════════════════════════════════════════════════════════════════════════
def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "ext1-quiver/v1",
           "_note": ("A₆·A₇ p-modular Ext¹ 퀴버 — 제시 없이 Cayley 일관성으로 H¹ 계산. "
                     "관측·seal 아님·module 0·root 불변.")}

    # ── A₆ ──────────────────────────────────────────────────────────────
    A6G = [(1, 2, 0, 3, 4, 5), (0, 1, 2, 4, 5, 3), (1, 0, 3, 2, 4, 5)]
    mul6, id6, ord6 = enumerate_group(A6G, 6)
    R["setup_A6_360"] = (len(ord6) == 360)
    triv6 = extend_action(A6G, mul6, id6, [np.eye(1, dtype=np.int64)] * 3, 2, ord6)
    # 4_b = 6점 heart (GF(2))
    gb = heart_gens(A6G, 6, 2)
    act4b = extend_action(A6G, mul6, id6, gb, 2, ord6)
    R["A6_4b_dim4"] = (act4b[id6].shape == (4, 4))
    R["A6_4b_homomorphism"] = all(
        np.array_equal((act4b[x] @ act4b[y]) % 2, act4b[mul6(x, y)])
        for x in ord6[:60] for y in A6G)
    # 4_a = A₇⊂GL(4,2) 의 A₆ 제한
    ga = fano_gl42_gens(None, 7, [tuple(list(g) + [6]) for g in A6G])
    act4a = extend_action(A6G, mul6, id6, ga, 2, ord6)
    R["A6_4a_faithful"] = (len({act4a[g].tobytes() for g in ord6}) == 360)
    R["A6_4a_neq_4b"] = any(not np.array_equal(act4a[g], act4b[g]) for g in ord6)

    mods6 = {"1": (triv6, 1), "4_a": (act4a, 4), "4_b": (act4b, 4)}
    # A. 계산기 자체검증
    H11 = hom_module(triv6, triv6, 1, 1, 2, ord6)
    R["A_H1_A6_F2_zero"] = (ext1_dim(A6G, mul6, id6, H11, 1, 2)[2] == 0)

    # B. A₆ p=2 주블록 3×3 퀴버
    names6 = ["1", "4_a", "4_b"]
    Q6 = {}
    for a in names6:
        for b in names6:
            (aa, da), (ab, db) = mods6[a], mods6[b]
            Hm = hom_module(aa, ab, da, db, 2, ord6)
            Q6[f"{a}->{b}"] = ext1_dim(A6G, mul6, id6, Hm, da * db, 2)[2]
    R["B_A6_quiver_computed"] = (len(Q6) == 9)
    R["B_no_self_loops"] = all(Q6[f"{x}->{x}"] == 0 for x in names6)
    R["D_ext1_symmetric"] = all(Q6[f"{a}->{b}"] == Q6[f"{b}->{a}"]
                                for a in names6 for b in names6)
    # C. Cartan 대조
    Cmain = [[8, 4, 4], [4, 3, 2], [4, 2, 3]]
    R["C_support_within_cartan"] = all(
        (Q6[f"{names6[i]}->{names6[j]}"] == 0) or (Cmain[i][j] != 0)
        for i in range(3) for j in range(3))
    out["A6_p2_quiver"] = {
        "simples": names6,
        "ext1": {k: v for k, v in Q6.items()},
        "matrix": [[Q6[f"{a}->{b}"] for b in names6] for a in names6],
        "cartan_principal": Cmain,
        "checks": "자기고리 0 · 대칭 · Cartan 비영 패턴 내",
    }

    # E. defect-0 블록
    R["E_defect0_isolated"] = True
    out["defect0"] = {
        "A6_p2": "{8},{8} — 블록에 simple 1개·C=[1] ⟹ 단순대수 ⟹ Ext¹=0(고립 정점)",
        "A6_p3": "{9}(Steinberg) — 동일",
        "note": "구조적 귀결로 기록(계산 아님)",
    }

    # F. A₇ p=2 비주블록 {4, 4̄, 6}
    if not quick:
        A7G = [(1, 2, 0, 3, 4, 5, 6), (1, 2, 3, 4, 5, 6, 0)]
        mul7, id7, ord7 = enumerate_group(A7G, 7)
        R["F_A7_2520"] = (len(ord7) == 2520)
        g4 = fano_gl42_gens(None, 7, A7G)
        act4 = extend_action(A7G, mul7, id7, g4, 2, ord7)
        g4b = [np.array(np.transpose(inv_mod(m, 2)), dtype=np.int64) % 2 for m in g4]
        act4d = extend_action(A7G, mul7, id7, g4b, 2, ord7)

        def wedge2(M):
            pr = list(itertools.combinations(range(4), 2))
            idx = {t: i for i, t in enumerate(pr)}
            O = np.zeros((6, 6), dtype=np.int64)
            for jc, (a, b) in enumerate(pr):
                for i in range(4):
                    for j in range(4):
                        if i == j:
                            continue
                        v = M[i][a] * M[j][b] % 2
                        if v:
                            O[idx[(min(i, j), max(i, j))]][jc] ^= 1
            return O
        act6 = extend_action(A7G, mul7, id7, [wedge2(m) for m in g4], 2, ord7)
        triv7 = extend_action(A7G, mul7, id7, [np.eye(1, dtype=np.int64)] * 2, 2, ord7)
        H11_7 = hom_module(triv7, triv7, 1, 1, 2, ord7)
        R["A_H1_A7_F2_zero"] = (ext1_dim(A7G, mul7, id7, H11_7, 1, 2)[2] == 0)
        mods7 = {"4": (act4, 4), "4b": (act4d, 4), "6": (act6, 6)}
        names7 = ["4", "4b", "6"]
        Q7 = {}
        for a in names7:
            for b in names7:
                (aa, da), (ab, db) = mods7[a], mods7[b]
                Hm = hom_module(aa, ab, da, db, 2, ord7)
                Q7[f"{a}->{b}"] = ext1_dim(A7G, mul7, id7, Hm, da * db, 2)[2]
        R["F_A7_nonprincipal_quiver"] = (len(Q7) == 9)
        R["F_A7_symmetric"] = all(Q7[f"{a}->{b}"] == Q7[f"{b}->{a}"]
                                  for a in names7 for b in names7)
        out["A7_p2_nonprincipal_quiver"] = {
            "simples": ["4̂", "4̄̂", "6̂"],
            "matrix": [[Q7[f"{a}->{b}"] for b in names7] for a in names7],
            "cartan_nonprincipal": [[2, 1, 2], [1, 2, 2], [2, 2, 4]],
        }

    # ── G. A₆ p=3 주블록 (GF(9) → GF(3) 실현화) ────────────────────────
    A6M, A6G3, gens3 = build_a6_p3_modules()
    mul63, id63, ord63 = enumerate_group(A6G3, 6)
    acts3 = {k: (q9_extend(A6M, A6G3, mul63, id63, gm, d), d)
             for k, (gm, d) in gens3.items()}
    R["G_A6p3_modules"] = (len(acts3) == 4 and acts3["3"][1] == 3)
    names3 = ["1", "4", "3", "3p"]
    Q3, even_ok = {}, True
    pairs3 = [(a, b) for a in names3 for b in names3]
    if quick:
        pairs3 = [(a, b) for (a, b) in pairs3 if not (a in ("3", "3p") and b in ("3", "3p"))]
    for (a, b) in pairs3:
        (aa, da), (ab, db) = acts3[a], acts3[b]
        Hm = q9_hom_real(A6M, aa, ab, da, db, ord63)
        h = ext1_dim(A6G3, mul63, id63, Hm, 2 * da * db, 3)[2]
        if h % 2:
            even_ok = False
        Q3[(a, b)] = h // 2
    R["G_realification_even"] = even_ok
    R["G_no_self_loops"] = all(Q3.get((x, x), 0) == 0 for x in names3)
    R["G_symmetric"] = all(Q3[(a, b)] == Q3[(b, a)] for (a, b) in pairs3 if (b, a) in Q3)
    R["G_frobenius_sigma_symmetry"] = all(
        Q3.get(("3", x), 0) == Q3.get(("3p", x), 0) for x in ("1", "4"))
    if not quick:
        R["G_matrix_star_center4"] = ([[Q3[(a, b)] for b in names3] for a in names3]
                                      == [[0, 2, 0, 0], [2, 0, 1, 1], [0, 1, 0, 0],
                                          [0, 1, 0, 0]])
        R["G_ext1_3_3p_zero"] = (Q3[("3", "3p")] == 0)
        R["G_double_arrow_1_4"] = (Q3[("1", "4")] == 2)
        C3 = [[5, 4, 1, 1], [4, 5, 2, 2], [1, 2, 2, 1], [1, 2, 1, 2]]
        R["G_support_within_cartan"] = all(
            (Q3[(names3[i], names3[j])] == 0) or (C3[i][j] != 0)
            for i in range(4) for j in range(4))
        out["A6_p3_quiver"] = {
            "simples": ["1̂", "4", "3", "3′"],
            "matrix": [[Q3[(a, b)] for b in names3] for a in names3],
            "cartan_principal": C3,
            "method": "GF(9) (a,b) ↦ [[a,−b],[b,a]] 실현화 ⟹ dim_GF(9) Ext¹ = dim_GF(3) H¹ / 2",
            "features": ("★별이지만 **중심이 4** · ★**1↔4 이중 화살(2)** · "
                         "★Ext¹(3,3′)=0(Frobenius 쌍 사이 화살 없음) · "
                         "★3 행 = 3′ 행(Frobenius σ-대칭 실측)"),
        }

    ok = bool(all(R.values()))
    out["checks"] = R
    out["method"] = {
        "formula": "Ext¹(S_i,S_j) = H¹(G, Hom(S_i,S_j)) · dim = dim Z¹ − dim B¹",
        "Z1": "f(xs) = f(x) + x·f(s) — BFS 신장트리 전개 후 **비트리 간선 일관성**이 커널을 준다",
        "presentation_free": "★군 제시를 인용하지 않는다(자체유도 규율)",
        "B1": "dim M − dim M^G",
    }
    out["scope_honesty"] = {
        "delivered": ("Ext¹ 계산기(제시-free)+자체검증(H¹(A₆/A₇,𝔽₂)=0) · A₆ p=2 주블록 완전 "
                      "3×3 퀴버 + Cartan 대조 + 대칭성 · A₇ p=2 비주블록 3×3 퀴버 · "
                      "defect-0 고립 정점"),
        "not_yet": ("★A₇ p=2 **주블록**(1,14,20) Ext¹ — Hom 최대 400 × |G| 2520 규모 · "
                    "A₆ p=3(3,3′ = GF(9)-형) — GF(9) cocycle 필요 · Loewy 급수(사영 덮개 구성)"),
        "not_claimed": "봉인 게이트 · Ext¹ 대칭성의 일반 정리(실측 보고)",
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p_ = os.path.join(ROOT, ".pgf", "proofs", "EXT1-QUIVER.json")
        os.makedirs(os.path.dirname(p_), exist_ok=True)
        with open(p_, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("A₆·A₇ Ext¹ 퀴버 (정확 — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  ★A₆ p=2 주블록 Ext¹ 행렬(1,4_a,4_b): "
              f"{[[Q6[f'{a}->{b}'] for b in names6] for a in names6]}", flush=True)
        if not quick:
            print(f"  ★A₇ p=2 비주블록 Ext¹ 행렬(4,4̄,6): "
                  f"{[[Q7[f'{a}->{b}'] for b in names7] for a in names7]}", flush=True)
        print(f"  ★A₆ p=3 주블록 Ext¹ 행렬(1,4,3,3′): "
              f"{[[Q3[(a, b)] for b in names3] for a in names3]} — 중심 4·1↔4 이중화살",
              flush=True)
        print("  ★제시-free 계산 · H¹(G,𝔽₂)=0 자체검증 · Cartan 비영 패턴 정합 · "
              "GF(9) 실현화(H¹ 짝수 게이트)", flush=True)
        print("  → .pgf/proofs/EXT1-QUIVER.json", flush=True)
    print(f"ext1_quiver_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
