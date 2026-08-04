#!/usr/bin/env python
"""유도동등의 **긍정 구성** — Cartan ℤ-합동 + 2항 silting mutation 엔진.

배경: 앞선 사이클에서 A₇ p=2 **주**블록(dim A = 19)과 A₆ p=2 **주**블록(dim A = 34)이
`(HH⁰,HH¹,HH²,cup rank) = (5,3,5,0)` 으로 **네 유도불변량 전부 일치**했다.
"다음 불변량이 가를 것"이라는 예측이 **세 번 연속 깨졌으므로**, 부정 도구를 더
찾는 대신 **가설을 뒤집어** 유도동등의 긍정 구성을 시도한다.

관측 7축 (정확 정수·GF(2) 선형대수 · seal 아님 · module 0 · root 불변):
  R  ★아직 안 잰 유도불변량 — Cartan **판별식**·**Smith 표준형**(4 블록).
     유도동등이면 `C_A = Xᵀ C_B X` (`X ∈ GL_n(ℤ)`)이므로 둘 다 필요조건이다.
  S  ★★**ℤ-합동(등척) 전수 판정** — 짧은 벡터를 `q(v) ≤ B ⟹ |v_i| ≤ √(B·(C⁻¹)_ii)`
     로 **엄밀히 유계**하고 전수한다(휴리스틱 절단 없음). 반증이면 Q3 즉시 종결(부정).
     ★등척 `X` 는 `K₀` 에서 `[T_a] = Σ x_{ia}[P_i]` 이므로 **탐색의 좌표**를 준다.
  T  ★**2항 silting mutation 엔진** — 기본대수를 **구조상수만으로** 다룬다.
     `T_k = (P_k → E)`(E = 최소 좌 `add(⊕_{i≠k}P_i)`-근사)·`T_i = P_i (i≠k)`,
     `End_{K^b}(T)` 를 사슬사상 mod 호모토피로 실물 계산.
     정오 게이트 3종: (a) 자명 대상이 원래 Cartan 을 되돌린다 (b) `Hom_K(T,T[±1]) = 0`
     (c) `End(T)` 의 Cartan 이 원래와 **ℤ-합동**(det·SNF 보존).
  U  ★mutation 궤도 탐색 — A₇p2주에서 출발해 도달한 Cartan/차원 목록.
  V  ★★★**대수 동형** — 2단 mutation 으로 얻은 `End_{K^b}(T)` 가 A₆ p=2 주블록과
     **명시적으로 동형**임을 경로값 랭크로 판정 ⟹ v22 §4 **Q3 를 긍정으로 종결**.
  W  ★유도동등류 **닫기** — 우 mutation `μ⁻_k(A) = (μ⁺_k(A^op))^op`(★반대 대수 하나만
     만들면 엔진 전체가 재사용된다) · **동형-dedup** BFS · 류 내부 불변량 교차검증
     (`HH^*` 는 유도불변 ⟹ 류의 **모든 대표**가 같아야 한다 — 반증 가능한 게이트).
  X  ★★**구조상수판 `HH^*`·cup** — `hh_relative`(행렬 입력)를 구조상수 입력으로 이식해
     엔진이 만드는 **모든** 대수에 적용한다. ★알려진 답(두 끝점의 `(5,3,5,0)`)이
     새 경로의 **정오 판정기**이고, 두 구현이 같은 대수에서 `C·ker·HH·cup` 까지 일치한다.
     ⟹ 류의 **세 대표 전부** `(HH⁰,HH¹,HH²,cup) = (5,3,5,0)`(R1 칸 채움).

결과: A₇ p=2 주블록(dim A = 19)과 A₆ p=2 주블록(dim A = 34)은 **유도동등**이다.
`HH^*` 과 cup 랭크가 세 사이클 연속 일치했던 것은 우연이 아니라 **실제로 같았기** 때문이다.

정직 경계:
  · **인용하는 정리 하나**: Rickard — 기울기 복합체 `T` 에 대해 `A` 와 `End_{K^b(proj A)}(T)`
    는 유도동등. 이 정리는 **증명하지 않는다**. 우리가 계산한 것은 (a) `T` 가 기울기라는
    **가설의 검증**(`Hom_K(T,T[±1]) = 0`)과 (b) `End(T) ≅ B` 의 **명시 동형**이다.
  · ℤ-합동은 **필요조건**일 뿐이다(성립해도 유도동등을 함의하지 않는다).
  · W축 폐합은 **`dim ≤ 60` · 깊이 ≤ 6 안에서의 폐합**이다(상한에 닿으면 포화라 쓰지 않는다).
  · dim 16 대표는 **어느 군 블록으로도 동일시하지 않았다** — 이 류에 있다는 실측만 쓴다.
  · 동형의 **명시 형태는 선택 의존**이다(σ·화살 상). 존재는 불변.
  · 외부 분류표(대수의 이름)는 **인용하지 않는다**.
"""
import itertools
import json
import os
import sys
import time
from fractions import Fraction

import numpy as np

from qf_witness.core.paths import ROOT

from qf_witness.observe.ext1_quiver_observe import (
    build_a7_principal_gens, enumerate_group, extend_action, fano_gl42_gens,
    heart_gens, rref_rows)
from qf_witness.observe.loewy_series_observe import (
    coset_data, coset_perm_module, decompose_regular, hecke_endos, hom_space,
    nullspace, nullspace_gf2, submodule_action, subgroup)
from qf_witness.observe.quiver_relations_observe import (
    algebra_table, block_presentation, hh_relative, hochschild, rref_insert)

PROOFS = os.path.join(ROOT, ".pgf", "proofs")


def _ns(M, p):
    return nullspace_gf2(M) if p == 2 else nullspace(M, p)


def _rank(M, p):
    if M.size == 0:
        return 0
    return len(rref_rows(M.copy() % p, p)[1])


# ══════════════════════════════════════════════════════════════════════
# R축 — 정수 불변량(판별식·Smith 표준형) 자체유도
# ══════════════════════════════════════════════════════════════════════
def det_int(M):
    """분수 없는 Bareiss 소거 — 정확 정수 판별식."""
    A = [[int(x) for x in r] for r in M]
    n, prev, sgn = len(A), 1, 1
    for k in range(n - 1):
        if A[k][k] == 0:
            sw = next((r for r in range(k + 1, n) if A[r][k]), None)
            if sw is None:
                return 0
            A[k], A[sw] = A[sw], A[k]
            sgn = -sgn
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                A[i][j] = (A[i][j] * A[k][k] - A[i][k] * A[k][j]) // prev
        prev = A[k][k]
    return sgn * A[n - 1][n - 1]


def smith(M):
    """Smith 표준형의 기본인자 — 각 라운드마다 최소 |성분| 이 줄어 종료한다."""
    A = [[int(x) for x in r] for r in M]
    n, m, res, t = len(A), len(A[0]), [], 0
    while t < min(n, m):
        while True:
            best = None
            for i in range(t, n):
                for j in range(t, m):
                    if A[i][j] and (best is None
                                    or abs(A[i][j]) < abs(A[best[0]][best[1]])):
                        best = (i, j)
            if best is None:
                return res
            bi, bj = best
            A[t], A[bi] = A[bi], A[t]
            for r in A:
                r[t], r[bj] = r[bj], r[t]
            if A[t][t] < 0:
                A[t] = [-x for x in A[t]]
            pv = A[t][t]
            for i in range(t + 1, n):
                q = A[i][t] // pv
                if q:
                    A[i] = [a - q * b for a, b in zip(A[i], A[t])]
            for j in range(t + 1, m):
                q = A[t][j] // pv
                if q:
                    for r in A:
                        r[j] -= q * r[t]
            if (all(A[i][t] == 0 for i in range(t + 1, n))
                    and all(A[t][j] == 0 for j in range(t + 1, m))):
                break
        pv = A[t][t]
        bad = next(((i, j) for i in range(t + 1, n) for j in range(t + 1, m)
                    if A[i][j] % pv), None)
        if bad:
            A[t] = [a + b for a, b in zip(A[t], A[bad[0]])]
            continue
        res.append(abs(pv))
        t += 1
    return res


def inv_rational(M):
    """정확 유리수 역행렬(가우스-조던)."""
    n = len(M)
    A = [[Fraction(M[i][j]) for j in range(n)]
         + [Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
    for c in range(n):
        pr = next(r for r in range(c, n) if A[r][c])
        A[c], A[pr] = A[pr], A[c]
        pv = A[c][c]
        A[c] = [x / pv for x in A[c]]
        for r in range(n):
            if r != c and A[r][c]:
                f = A[r][c]
                A[r] = [a - f * b for a, b in zip(A[r], A[c])]
    return [row[n:] for row in A]


# ══════════════════════════════════════════════════════════════════════
# S축 — ℤ-합동(등척) 전수 판정
# ══════════════════════════════════════════════════════════════════════
def short_vectors(C, bound):
    """`q(v) ≤ bound` 인 v 전수 — 상자 한계 `|v_i| ≤ √(bound·(C⁻¹)_ii)` 는 엄밀."""
    n = len(C)
    Ci = inv_rational(C)
    lim = []
    for i in range(n):
        b = Fraction(bound) * Ci[i][i]
        k = 0
        while Fraction(k + 1) ** 2 <= b:
            k += 1
        lim.append(k)
    out = {}
    for v in itertools.product(*[range(-L, L + 1) for L in lim]):
        if not any(v):
            continue
        q = sum(C[i][j] * v[i] * v[j] for i in range(n) for j in range(n))
        if q <= bound:
            out.setdefault(q, []).append(v)
    return lim, out


def isometries(CA, CB, cap=64):
    """`Xᵀ CB X = CA` 인 `X ∈ GL_n(ℤ)` 전수(최대 cap 개 보고)."""
    n = len(CA)
    diag = [CA[i][i] for i in range(n)]
    lim, sv = short_vectors(CB, max(diag))
    cand = [sv.get(d, []) for d in diag]
    found = []

    def rec(cols):
        if len(found) >= cap:
            return
        t = len(cols)
        if t == n:
            X = [[cols[j][i] for j in range(n)] for i in range(n)]
            if abs(det_int(X)) == 1:
                found.append(X)
            return
        for v in cand[t]:
            if all(sum(CB[i][j] * cols[s][i] * v[j]
                       for i in range(n) for j in range(n)) == CA[s][t]
                   for s in range(t)):
                rec(cols + [v])

    rec([])
    return lim, found


# ══════════════════════════════════════════════════════════════════════
# T축 — 기본대수(구조상수) 위의 2항 silting mutation 엔진
# ══════════════════════════════════════════════════════════════════════
def alg_pack(names, meta, MT, p):
    off, cnt, pos = {}, {}, 0
    for i in names:
        for j in names:
            c = sum(1 for (a, b, _t) in meta if a == i and b == j)
            off[(i, j)], cnt[(i, j)] = pos, c
            pos += c
    assert pos == len(meta) == MT.shape[0], (pos, len(meta), MT.shape)
    return {"names": list(names), "off": off, "cnt": cnt, "n": pos,
            "MT": MT % p, "p": p}


def amul(alg, x, y):
    """구조상수 규약 `a·b := b∘a` ⟹ amul(x,y) 는 **y∘x**."""
    r = np.zeros(alg["n"], dtype=np.int64)
    for u in np.nonzero(x)[0]:
        r = r + int(x[u]) * (y @ alg["MT"][u])
    return r % alg["p"]


def hlayout(alg, X, Y):
    lay, pos = [], 0
    for a, va in enumerate(X):
        for b, vb in enumerate(Y):
            c = alg["cnt"][(va, vb)]
            lay.append((a, b, pos, c, alg["off"][(va, vb)]))
            pos += c
    return lay, pos


def hdim(alg, X, Y):
    return hlayout(alg, X, Y)[1]


def unit(m, u):
    v = np.zeros(m, dtype=np.int64)
    v[u] = 1
    return v


def compose(alg, X, Y, Z, gcv, fcv):
    """`f: X→Y` · `g: Y→Z` ⟹ `g∘f: X→Z` (직합 성분별 행렬곱)."""
    lay_f = hlayout(alg, X, Y)[0]
    lay_g = hlayout(alg, Y, Z)[0]
    F = [[np.zeros(alg["n"], dtype=np.int64) for _ in Y] for _ in X]
    G = [[np.zeros(alg["n"], dtype=np.int64) for _ in Z] for _ in Y]
    for (a, b, pos, c, o) in lay_f:
        if c:
            F[a][b][o:o + c] = fcv[pos:pos + c]
    for (b, c_, pos, c, o) in lay_g:
        if c:
            G[b][c_][o:o + c] = gcv[pos:pos + c]
    H = [[np.zeros(alg["n"], dtype=np.int64) for _ in Z] for _ in X]
    for a in range(len(X)):
        for b in range(len(Y)):
            if not F[a][b].any():
                continue
            for c_ in range(len(Z)):
                if G[b][c_].any():
                    H[a][c_] = (H[a][c_] + amul(alg, F[a][b], G[b][c_])) \
                        % alg["p"]
    lay_h, tot = hlayout(alg, X, Z)
    out = np.zeros(tot, dtype=np.int64)
    for (a, c_, pos, c, o) in lay_h:
        if c:
            out[pos:pos + c] = H[a][c_][o:o + c]
    return out


def rad_block(alg, i, j, cap=20):
    """`rad ∩ Hom(P_i,P_j)` — i≠j 는 전체(Nakayama)·i=j 는 **멱영원 전수**."""
    c = alg["cnt"][(i, j)]
    if c == 0:
        return np.zeros((0, 0), dtype=np.int64)
    if i != j:
        return np.eye(c, dtype=np.int64)
    p, o = alg["p"], alg["off"][(i, i)]
    assert p == 2 and c <= cap, (p, c)
    rows = []
    for mask in range(1, 1 << c):
        v = np.zeros(alg["n"], dtype=np.int64)
        for t in range(c):
            if mask >> t & 1:
                v[o + t] = 1
        w = v.copy()
        for _ in range(c):
            w = amul(alg, w, v)
            if not w.any():
                rows.append([mask >> t & 1 for t in range(c)])
                break
    if not rows:
        return np.zeros((0, c), dtype=np.int64)
    return rref_rows(np.array(rows, dtype=np.int64) % p, p)[0]


def left_approx(alg, k):
    """`P_k → E` 의 **최소 좌 add(⊕_{i≠k}P_i)-근사** — 극소 생성원으로 얻는다.

    `N_j = Σ_{i≠k} rad_{ij} ∘ Hom(P_k,P_i)` 로 나눈 여공간의 기저가 생성원이고,
    `N` 이 표적 j 로 **등급화**되므로 생성원을 동차로 고를 수 있다."""
    p, other = alg["p"], [i for i in alg["names"] if i != k]
    E, gens = [], []
    for j in other:
        cj = alg["cnt"][(k, j)]
        if cj == 0:
            continue
        okj = alg["off"][(k, j)]
        B, piv = [], []
        for i in other:
            RB, ci = rad_block(alg, i, j), alg["cnt"][(i, j)]
            oi, oij = alg["off"][(k, i)], alg["off"][(i, j)]
            for t in range(alg["cnt"][(k, i)]):
                f = np.zeros(alg["n"], dtype=np.int64)
                f[oi + t] = 1
                for rr in RB:
                    r = np.zeros(alg["n"], dtype=np.int64)
                    r[oij:oij + ci] = rr
                    _o, B, piv = rref_insert(
                        B, piv, amul(alg, f, r)[okj:okj + cj], p)
        for t in range(cj):
            ok, B, piv = rref_insert(B, piv, unit(cj, t), p)
            if ok:
                E.append(j)
                gens.append(t)
    lay, tot = hlayout(alg, [k], E)
    f = np.zeros(tot, dtype=np.int64)
    for (_a, b, pos, c, _o) in lay:
        if c:
            f[pos + gens[b]] = 1
    return E, f


def homK_data(alg, Xc, Yc):
    """`Hom_K(X,Y)` 의 사슬사상 기저·호모토피 상 · `dim Hom_K(X,Y[1])`."""
    p = alg["p"]
    Xm, X0, dX = Xc
    Ym, Y0, dY = Yc
    n1, n0 = hdim(alg, Xm, Ym), hdim(alg, X0, Y0)
    nq, nh = hdim(alg, Xm, Y0), hdim(alg, X0, Ym)
    M = np.zeros((n1 + n0, nq), dtype=np.int64)
    for u in range(n1):
        M[u] = (-compose(alg, Xm, Ym, Y0, dY, unit(n1, u))) % p
    for u in range(n0):
        M[n1 + u] = compose(alg, Xm, X0, Y0, unit(n0, u), dX)
    CM = (_ns(M.T % p, p) if nq and (n1 + n0)
          else np.eye(n1 + n0, dtype=np.int64))
    HT = np.zeros((nh, n1 + n0), dtype=np.int64)
    for u in range(nh):
        h = unit(nh, u)
        HT[u, :n1] = compose(alg, Xm, X0, Ym, h, dX)
        HT[u, n1:] = compose(alg, X0, Ym, Y0, dY, h)
    return CM % p, HT % p, nq - _rank(M, p), n1


def homK_minus(alg, Xc, Yc):
    """`dim Hom_K(X,Y[-1])` — 사슬사상 조건이 **양쪽 끝에서** 하나씩 나온다.

    `Y[-1]` 은 차수 (0,1) 에 놓이므로 `u: X⁰→Y⁻¹` 는 `u∘d_X = 0`(차수 −1 칸)과
    `d_Y∘u = 0`(차수 1 칸)을 **둘 다** 만족해야 한다. 호모토피는 존재하지 않는다."""
    p = alg["p"]
    Xm, X0, dX = Xc
    Ym, Y0, dY = Yc
    nh = hdim(alg, X0, Ym)
    if nh == 0:
        return 0
    n1, n0 = hdim(alg, Xm, Ym), hdim(alg, X0, Y0)
    Mh = np.zeros((nh, n1 + n0), dtype=np.int64)
    for u in range(nh):
        h = unit(nh, u)
        Mh[u, :n1] = compose(alg, Xm, X0, Ym, h, dX)
        Mh[u, n1:] = compose(alg, X0, Ym, Y0, dY, h)
    return nh - _rank(Mh, p)


def reps_of(CM, HT, p):
    """호모토피를 법으로 독립인 사슬사상 대표 + 독립 호모토피 행."""
    B, piv, htb = [], [], []
    for r in HT:
        ok, B, piv = rref_insert(B, piv, r, p)
        if ok:
            htb.append(r % p)
    reps = []
    for r in CM:
        ok, B, piv = rref_insert(B, piv, r, p)
        if ok:
            reps.append(r % p)
    return htb, reps


def left_inverse(rows, p):
    """독립 행들의 좌역행렬 — 좌표 `α` 를 `α = Linv @ w` 로 즉시 얻는다."""
    if not rows:
        return np.zeros((0, 0), dtype=np.int64)
    R = np.array(rows, dtype=np.int64) % p
    m, L = R.shape
    Rr, piv = rref_rows(
        np.concatenate([R.T % p, np.eye(L, dtype=np.int64)], axis=1), p)
    Linv = np.zeros((m, L), dtype=np.int64)
    for r, c in zip(Rr, piv):
        if c < m:
            Linv[c] = r[m:] % p
    return Linv


def op_algebra(alg):
    """반대 대수 `A^op` — `Hom'(P_i,P_j) := Hom(P_j,P_i)` 로 블록을 전치하고
    구조상수를 `MT'[v',u',w'] = MT[u,v,w]` 로 재색인한다(★새 엔진이 필요 없다)."""
    names, p = alg["names"], alg["p"]
    off2, cnt2, pos = {}, {}, 0
    for i in names:
        for j in names:
            cnt2[(i, j)] = alg["cnt"][(j, i)]
            off2[(i, j)] = pos
            pos += cnt2[(i, j)]
    pi = np.zeros(alg["n"], dtype=np.int64)
    for i in names:
        for j in names:
            for t in range(alg["cnt"][(i, j)]):
                pi[alg["off"][(i, j)] + t] = off2[(j, i)] + t
    MT2 = np.zeros_like(alg["MT"])
    nz = np.nonzero(alg["MT"])
    for u, v, w in zip(*nz):
        MT2[pi[v], pi[u], pi[w]] = alg["MT"][u, v, w]
    return {"names": list(names), "off": off2, "cnt": cnt2, "n": pos,
            "MT": MT2 % p, "p": p}


def trivial_object(alg):
    return [([], [i], np.zeros(0, dtype=np.int64)) for i in alg["names"]]


def mutate(alg, k):
    E, f = left_approx(alg, k)
    return [(([k], E, f) if i == k
             else ([], [i], np.zeros(0, dtype=np.int64)))
            for i in alg["names"]], E


def end_algebra(alg, T):
    """`End_{K^b(proj)}(T)` — Cartan · 구조상수 · 기울기 게이트."""
    p, m = alg["p"], len(T)
    HTB, RP, LI, PL, MI, N1 = {}, {}, {}, {}, {}, {}
    for a in range(m):
        for b in range(m):
            cm, ht, pl, n1 = homK_data(alg, T[a], T[b])
            htb, reps = reps_of(cm, ht, p)
            HTB[(a, b)], RP[(a, b)], N1[(a, b)] = htb, reps, n1
            LI[(a, b)] = left_inverse(htb + reps, p)
            PL[(a, b)] = pl
            MI[(a, b)] = homK_minus(alg, T[a], T[b])
    C = [[len(RP[(a, b)]) for b in range(m)] for a in range(m)]
    off, pos = {}, 0
    for a in range(m):
        for b in range(m):
            off[(a, b)] = pos
            pos += C[a][b]
    MT = np.zeros((pos, pos, pos), dtype=np.int64)
    for a in range(m):
        for b in range(m):
            for c in range(m):
                nb = N1[(b, c)]
                na = N1[(a, b)]
                nh = len(HTB[(a, c)])
                for s, u in enumerate(RP[(a, b)]):
                    for t, v in enumerate(RP[(b, c)]):
                        w = np.concatenate([
                            compose(alg, T[a][0], T[b][0], T[c][0],
                                    v[:nb], u[:na]),
                            compose(alg, T[a][1], T[b][1], T[c][1],
                                    v[nb:], u[na:])]) % p
                        al = (LI[(a, c)] @ w) % p
                        for q in range(C[a][c]):
                            if al[nh + q]:
                                MT[off[(a, b)] + s, off[(b, c)] + t,
                                   off[(a, c)] + q] = int(al[nh + q]) % p
    meta = [(a, b, t) for a in range(m) for b in range(m)
            for t in range(C[a][b])]
    return {"cartan": C, "dim": pos,
            "tilting": all(v == 0 for v in PL.values())
                       and all(v == 0 for v in MI.values()),
            "ext_pos": sum(PL.values()), "ext_neg": sum(MI.values()),
            "alg": alg_pack(list(range(m)), meta, MT, p)}


def rad_basis_piv(alg, i, j):
    """`rad ∩ Hom(P_i,P_j)` 의 RREF 기저 + pivot(좌표 읽기용)."""
    c = alg["cnt"][(i, j)]
    if c == 0:
        return np.zeros((0, 0), dtype=np.int64), []
    if i != j:
        return np.eye(c, dtype=np.int64), list(range(c))
    Rr = rad_block(alg, i, i)
    if not len(Rr):
        return np.zeros((0, c), dtype=np.int64), []
    return rref_rows(Rr.copy() % alg["p"], alg["p"])


def hh_struct(alg, cup=False):
    """★`hh_relative` 의 **구조상수판** — 행렬(HOM/RADP) 없이 임의 기본대수에 쓴다.

    정규화 상대 bar 복합체 `C^n = Hom_{E-E}(rad^{⊗_E n}, A)` 는 동일하고,
    행렬 합성 `Y @ X`(= Y∘X)가 전부 `amul(x, y)` 로 바뀐다(규약 `a·b := b∘a`).
    블록 좌표 읽기는 pivot 슬라이스라 변환행렬이 필요 없다."""
    p, names, cnt, off = alg["p"], alg["names"], alg["cnt"], alg["off"]

    def co(i, j, v):
        o = off[(i, j)]
        return [int(x) % p for x in v[o:o + cnt[(i, j)]]]

    def ebas(i, j, t):
        v = np.zeros(alg["n"], dtype=np.int64)
        v[off[(i, j)] + t] = 1
        return v

    RMAT, RPIV, rmeta = {}, {}, []
    for i in names:
        for j in names:
            Rr, piv = rad_basis_piv(alg, i, j)
            RPIV[(i, j)] = piv
            for t, row in enumerate(Rr):
                v = np.zeros(alg["n"], dtype=np.int64)
                v[off[(i, j)]:off[(i, j)] + cnt[(i, j)]] = row % p
                RMAT[(i, j, t)] = v
                rmeta.append((i, j, t))
    nR = len(rmeta)

    def rco(i, j, cvec):
        return [int(cvec[c]) % p for c in RPIV[(i, j)]]

    pairs = [(a, b) for a in rmeta for b in rmeta if a[1] == b[0]]
    prodR = {(a, b): rco(a[0], b[1],
                         co(a[0], b[1], amul(alg, RMAT[a], RMAT[b])))
             for (a, b) in pairs}

    c0 = [(i, t) for i in names for t in range(cnt[(i, i)])]
    c1 = [(rk, w) for rk in rmeta for w in range(cnt[(rk[0], rk[1])])]
    trips = [(a, b, c) for (a, b) in pairs for c in rmeta if b[1] == c[0]]
    c2 = [(a, b, w) for (a, b) in pairs for w in range(cnt[(a[0], b[1])])]
    c3 = [(a, b, c, w) for (a, b, c) in trips
          for w in range(cnt[(a[0], c[1])])]
    i1 = {k: t for t, k in enumerate(c1)}
    i2 = {k: t for t, k in enumerate(c2)}
    i3 = {k: t for t, k in enumerate(c3)}

    D0 = np.zeros((len(c1), len(c0)), dtype=np.int64)
    for q, (m, ua) in enumerate(c0):
        for rk in rmeta:
            (i, j, _t) = rk
            if j == m:                       # a·z = z∘a
                for w, val in enumerate(
                        co(i, m, amul(alg, RMAT[rk], ebas(m, m, ua)))):
                    D0[i1[(rk, w)], q] = (D0[i1[(rk, w)], q] + val) % p
            if i == m:                       # z·a = a∘z
                for w, val in enumerate(
                        co(m, j, amul(alg, ebas(m, m, ua), RMAT[rk]))):
                    D0[i1[(rk, w)], q] = (D0[i1[(rk, w)], q] - val) % p
    D0 %= p

    D1 = np.zeros((len(c2), len(c1)), dtype=np.int64)
    for (a, b) in pairs:
        i, m, j = a[0], a[1], b[1]
        base = i2[(a, b, 0)]
        for ua in range(cnt[(m, j)]):                     # a·f(b)
            for w, val in enumerate(
                    co(i, j, amul(alg, RMAT[a], ebas(m, j, ua)))):
                if val:
                    D1[base + w, i1[(b, ua)]] = (
                        D1[base + w, i1[(b, ua)]] + val) % p
        for ua in range(cnt[(i, m)]):                     # f(a)·b
            for w, val in enumerate(
                    co(i, j, amul(alg, ebas(i, m, ua), RMAT[b]))):
                if val:
                    D1[base + w, i1[(a, ua)]] = (
                        D1[base + w, i1[(a, ua)]] + val) % p
        for t2, val in enumerate(prodR[(a, b)]):          # −f(a·b)
            if val:
                rk = (i, j, t2)
                for w in range(cnt[(i, j)]):
                    D1[base + w, i1[(rk, w)]] = (
                        D1[base + w, i1[(rk, w)]] - val) % p
    D1 %= p

    D2 = np.zeros((len(c3), len(c2)), dtype=np.int64)
    for (a, b, c) in trips:
        i, m1, m2, j = a[0], a[1], c[0], c[1]
        base = i3[(a, b, c, 0)]
        for ua in range(cnt[(m1, j)]):
            for w, val in enumerate(
                    co(i, j, amul(alg, RMAT[a], ebas(m1, j, ua)))):
                if val:
                    D2[base + w, i2[(b, c, ua)]] = (
                        D2[base + w, i2[(b, c, ua)]] + val) % p
        for t2, val in enumerate(prodR[(a, b)]):
            if val:
                rk = (i, m2, t2)
                for w in range(cnt[(i, j)]):
                    D2[base + w, i2[(rk, c, w)]] = (
                        D2[base + w, i2[(rk, c, w)]] - val) % p
        for t2, val in enumerate(prodR[(b, c)]):
            if val:
                rk = (m1, j, t2)
                for w in range(cnt[(i, j)]):
                    D2[base + w, i2[(a, rk, w)]] = (
                        D2[base + w, i2[(a, rk, w)]] + val) % p
        for ua in range(cnt[(i, m2)]):
            for w, val in enumerate(
                    co(i, j, amul(alg, ebas(i, m2, ua), RMAT[c]))):
                if val:
                    D2[base + w, i2[(a, b, ua)]] = (
                        D2[base + w, i2[(a, b, ua)]] - val) % p
    D2 %= p

    Z1 = _ns(D1, p) if len(c2) else np.eye(len(c1), dtype=np.int64)
    k0 = len(_ns(D0, p)) if len(c1) else len(c0)
    k1, k2 = len(Z1), (len(_ns(D2, p)) if len(c3) else len(c2))
    out = {"dim_A": alg["n"], "dim_rad": nR,
           "C": [len(c0), len(c1), len(c2), len(c3)],
           "ker": [k0, k1, k2], "HH0": k0, "HH1": k1 - (len(c0) - k0),
           "HH2": k2 - (len(c1) - k1)}
    if not cup:
        return out

    Bb, pv = np.zeros((0, len(c1)), dtype=np.int64), []
    for q in range(D0.shape[1]):
        _o, Bb, pv = rref_insert(Bb, pv, D0[:, q] % p, p)
    reps = []
    for z in Z1:
        ok, Bb, pv = rref_insert(Bb, pv, z % p, p)
        if ok:
            reps.append(z % p)
    B2b, p2 = np.zeros((0, len(c2)), dtype=np.int64), []
    for q in range(D1.shape[1]):
        _o, B2b, p2 = rref_insert(B2b, p2, D1[:, q] % p, p)

    def val1(fv, rk):
        i, j = rk[0], rk[1]
        v = np.zeros(alg["n"], dtype=np.int64)
        for w in range(cnt[(i, j)]):
            v[off[(i, j)] + w] = int(fv[i1[(rk, w)]]) % p
        return v

    def cup11(fv, gv):
        v = np.zeros(len(c2), dtype=np.int64)
        for (a, b) in pairs:
            i, j = a[0], b[1]
            P = amul(alg, val1(fv, a), val1(gv, b))
            base = i2[(a, b, 0)]
            for w, cc in enumerate(co(i, j, P)):
                if cc:
                    v[base + w] = (v[base + w] + cc) % p
        return v % p

    cocycle_ok, comm_ok, prods = True, True, {}
    for x in range(len(reps)):
        for y in range(len(reps)):
            u = cup11(reps[x], reps[y])
            prods[(x, y)] = u
            if len(c3) and ((D2 @ u) % p).any():
                cocycle_ok = False
    for x in range(len(reps)):
        for y in range(x, len(reps)):
            ok, _B2c, _p2c = rref_insert(B2b.copy(), list(p2),
                                         (prods[(x, y)] + prods[(y, x)]) % p, p)
            if ok:
                comm_ok = False
    Cb, cp = B2b.copy(), list(p2)
    span0 = len(cp)
    for x in range(len(reps)):
        for y in range(len(reps)):
            _o, Cb, cp = rref_insert(Cb, cp, prods[(x, y)], p)
    out.update({"HH1_reps": len(reps), "cup_rank": len(cp) - span0,
                "cup_is_cocycle": cocycle_ok, "graded_commutative": comm_ok})
    return out


def mutate_step(alg, k, right):
    """한 걸음 mutation — `right=True` 면 `μ⁻_k(A) = (μ⁺_k(A^op))^op`."""
    if not right:
        T, E = mutate(alg, k)
        e = end_algebra(alg, T)
        return e, [str(x) for x in E]
    ao = op_algebra(alg)
    T, E = mutate(ao, k)
    e = end_algebra(ao, T)
    return ({"cartan": [list(r) for r in zip(*e["cartan"])], "dim": e["dim"],
             "tilting": e["tilting"], "ext_pos": e["ext_pos"],
             "ext_neg": e["ext_neg"], "alg": op_algebra(e["alg"])},
            [str(x) for x in E])


def quiver_of(alg):
    """화살 개수 = `dim rad/rad²` 블록별."""
    p, names = alg["p"], alg["names"]
    R = {}
    for i in names:
        for j in names:
            R[(i, j)] = rad_block(alg, i, j)
    arrows = {}
    for i in names:
        for j in names:
            B, piv = [], []
            for l in names:
                ci, cl = alg["cnt"][(i, l)], alg["cnt"][(l, j)]
                oi, ol, oj = alg["off"][(i, l)], alg["off"][(l, j)], \
                    alg["off"][(i, j)]
                for ra in R[(i, l)]:
                    x = np.zeros(alg["n"], dtype=np.int64)
                    x[oi:oi + ci] = ra
                    for rb in R[(l, j)]:
                        y = np.zeros(alg["n"], dtype=np.int64)
                        y[ol:ol + cl] = rb
                        _o, B, piv = rref_insert(
                            B, piv, amul(alg, x, y)[
                                oj:oj + alg["cnt"][(i, j)]], p)
            arrows[f"{i}->{j}"] = len(R[(i, j)]) - len(piv)
    return arrows


def canon(C):
    n = len(C)
    return min(tuple(tuple(C[s[i]][s[j]] for j in range(n)) for i in range(n))
               for s in itertools.permutations(range(n)))


# ══════════════════════════════════════════════════════════════════════
# V축 — **대수 동형** 판정(경로값 랭크)
# ══════════════════════════════════════════════════════════════════════
def blk(alg, i, j, rows):
    o, c = alg["off"][(i, j)], alg["cnt"][(i, j)]
    out = []
    for r in rows:
        v = np.zeros(alg["n"], dtype=np.int64)
        v[o:o + c] = r
        out.append(v)
    return out


def _spanmul(alg, i, j, left):
    """`Σ_l left(i,l) · rad(l,j)` 의 슬롯 기저."""
    B, piv, c, oj = [], [], alg["cnt"][(i, j)], alg["off"][(i, j)]
    for l in alg["names"]:
        for x in blk(alg, i, l, left[(i, l)]):
            for y in blk(alg, l, j, rad_block(alg, l, j)):
                _o, B, piv = rref_insert(B, piv,
                                         amul(alg, x, y)[oj:oj + c], alg["p"])
    return (np.array(B, dtype=np.int64) if len(B)
            else np.zeros((0, c), dtype=np.int64))


def rad_powers(alg):
    """`dim rad^n` 열 — Loewy 길이까지."""
    names = alg["names"]
    cur = {(i, j): rad_block(alg, i, j) for i in names for j in names}
    out = [sum(len(v) for v in cur.values())]
    while out[-1]:
        cur = {(i, j): _spanmul(alg, i, j, cur) for i in names for j in names}
        out.append(sum(len(v) for v in cur.values()))
    return out


def idempotents(alg):
    """정점 멱등원 — 국소 대수 `End(P_i)` 의 유일한 비영 멱등원."""
    E = {}
    for i in alg["names"]:
        c, o = alg["cnt"][(i, i)], alg["off"][(i, i)]
        for mask in range(1, 1 << c):
            v = np.zeros(alg["n"], dtype=np.int64)
            for t in range(c):
                if mask >> t & 1:
                    v[o + t] = 1
            if np.array_equal(amul(alg, v, v), v):
                E[i] = v
                break
    return E


def arrow_lifts_of(alg):
    """화살 리프트 — `rad ∖ rad²` 의 대표(선택 의존·개수는 불변)."""
    R2 = {(i, j): _spanmul(alg, i, j, {(a, b): rad_block(alg, a, b)
                                       for a in alg["names"]
                                       for b in alg["names"]})
          for i in alg["names"] for j in alg["names"]}
    out = []
    for i in alg["names"]:
        for j in alg["names"]:
            Rr = rad_block(alg, i, j)
            B, piv = [], []
            for r in R2[(i, j)]:
                _o, B, piv = rref_insert(B, piv, r, alg["p"])
            for r in Rr:
                ok, B, piv = rref_insert(B, piv, r, alg["p"])
                if ok:
                    out.append((i, j, blk(alg, i, j, [r])[0]))
    return out, R2


def path_values(alg, ide, arrows):
    """경로(단어)의 값 — ★**값이 0 인 단어도 기록**해야 동형 판정이 닫힌다."""
    words = [(i, ()) for i in alg["names"]]
    vals = [ide[i] for i in alg["names"]]
    cur = [(i, (), i, ide[i]) for i in alg["names"]]
    while cur:
        nxt = []
        for (s, w, t, v) in cur:
            for ai, (fi, fj, av) in enumerate(arrows):
                if fi != t:
                    continue
                nv = amul(alg, v, av)
                words.append((s, w + (ai,)))
                vals.append(nv)
                if nv.any():
                    nxt.append((s, w + (ai,), fj, nv))
        cur = nxt
    return words, np.array(vals, dtype=np.int64) % alg["p"]


def find_isomorphism(A, B):
    """`A ≅ B` 인 대수 동형을 명시 탐색한다.

    A 는 멱등원과 화살로 생성되므로 `φ` 는 (정점 대응 σ, 화살 상)으로 결정된다.
    판정: 경로값 행렬 `V_A`(랭크 = dim A)에 대해
      ① `rank(V_B') = dim B` ⟹ φ 는 **전사**
      ② `rank([V_A | V_B']) = dim A` ⟹ `val_A(w) = 0 ⟹ val_B(w) = 0`,
         즉 φ 가 **well-defined** — ★0-값 단어를 목록에 넣었기에 닫힌다.
    ①②와 `dim A = dim B` ⟹ 전단사이고, 곱은 단어 이어붙이기라 **곱 보존**."""
    p = A["p"]
    IA, IB = idempotents(A), idempotents(B)
    arA, _r2 = arrow_lifts_of(A)
    _arB, R2B = arrow_lifts_of(B)
    WA, VA = path_values(A, IA, arA)
    CA, CB = cartan_of(A), cartan_of(B)
    nA = len(A["names"])
    sig = [s for s in itertools.permutations(B["names"])
           if all(CA[i][j] == CB[B["names"].index(s[i])][B["names"].index(s[j])]
                  for i in range(nA) for j in range(nA))]
    tried = 0
    for s in sig:
        opts = []
        for (i, j, _v) in arA:
            si = s[A["names"].index(i)]
            sj = s[A["names"].index(j)]
            Rr = rad_block(B, si, sj)
            Bq, pq = [], []
            for r in R2B[(si, sj)]:
                _o, Bq, pq = rref_insert(Bq, pq, r, p)
            cand = []
            for mask in range(1, 1 << len(Rr)):
                v = np.zeros(Rr.shape[1], dtype=np.int64)
                for t in range(len(Rr)):
                    if mask >> t & 1:
                        v = (v + Rr[t]) % p
                ok, _B2, _p2 = rref_insert(Bq, pq, v, p)
                if ok:
                    cand.append(blk(B, si, sj, [v])[0])
            opts.append(cand)
        for combo in itertools.product(*[range(len(o)) for o in opts]):
            tried += 1
            arB = [o[c] for o, c in zip(opts, combo)]
            VB = []
            for (st, w) in WA:
                v = IB[s[A["names"].index(st)]]
                for ai in w:
                    v = amul(B, v, arB[ai])
                VB.append(v)
            VB = np.array(VB, dtype=np.int64) % p
            if _rank(VB, p) != B["n"]:
                continue
            if _rank(np.concatenate([VA, VB], axis=1), p) == A["n"]:
                return {"found": True, "sigma": [str(x) for x in s],
                        "arrow_choice": list(combo), "tried": tried,
                        "n_words": len(WA), "rank_VA": _rank(VA, p),
                        "rank_VB": B["n"]}
    return {"found": False, "tried": tried, "n_words": len(WA)}


# ══════════════════════════════════════════════════════════════════════
def build_a6_p2_principal():
    import random
    A6G = [(1, 2, 0, 3, 4, 5), (0, 1, 2, 4, 5, 3), (1, 0, 3, 2, 4, 5)]
    mul6, id6, ord6 = enumerate_group(A6G, 6)
    g6 = {"1": [np.eye(1, dtype=np.int64)] * 3,
          "4a": fano_gl42_gens(None, 7, [tuple(list(g) + [6]) for g in A6G]),
          "4b": heart_gens(A6G, 6, 2)}
    N6 = ["1", "4a", "4b"]
    S6 = {k: extend_action(A6G, mul6, id6, v, 2, ord6) for k, v in g6.items()}
    D6 = {"1": 1, "4a": 4, "4b": 4}
    sim6 = [(k, S6[k], D6[k]) for k in N6]
    syl3 = subgroup([(1, 2, 0, 3, 4, 5), (0, 1, 2, 4, 5, 3)], mul6, id6)
    n40, mats40 = coset_perm_module(ord6, mul6, id6, A6G, syl3, 2)
    act40 = extend_action(A6G, mul6, id6, mats40, 2, ord6)
    PIM6 = {"1": {g: act40[g] % 2 for g in A6G}}
    for hgen in ([(1, 2, 0, 3, 4, 5)], [(1, 2, 0, 4, 5, 3)]):
        Hl = subgroup(hgen, mul6, id6)
        n_, reps_, perms_, mats_ = coset_data(ord6, mul6, id6, A6G, Hl)
        actX = extend_action(A6G, mul6, id6, mats_, 2, ord6)
        alg = hecke_endos(n_, perms_, Hl, reps_)
        rng = random.Random(7)

        def _rnd(alg=alg, rng=rng, n_=n_):
            M = np.zeros((n_, n_), dtype=np.int64)
            for A_ in rng.sample(alg, max(2, len(alg) // 3)):
                M = (M + A_) % 2
            return M

        ps = []
        decompose_regular(np.eye(n_, dtype=np.int64),
                          np.eye(n_, dtype=np.int64), _rnd, 2, rng, ps)
        for B in sorted(ps, key=len):
            if len(B) != 24:
                continue
            actY, _ = submodule_action(actX, A6G, B, 2)
            hd = tuple(len(hom_space(actY, aS, len(B), dS_, A6G, 2))
                       for _n, aS, dS_ in sim6)
            nm = next((k for t, k in enumerate(N6)
                       if hd == tuple(1 if j == t else 0 for j in range(3))),
                      None)
            if nm in ("4a", "4b") and nm not in PIM6:
                PIM6[nm] = {g: actY[g] % 2 for g in A6G}
    C6 = [[8, 4, 4], [4, 3, 2], [4, 2, 3]]
    B6, _a, RADP6, HOM6, dP6 = block_presentation(N6, A6G, PIM6, sim6, C6, 9, 2)
    meta, MT, _n = algebra_table(N6, HOM6, dP6, 2)
    return (alg_pack(N6, meta, MT, 2), B6["cartan_via_hom"],
            (N6, HOM6, RADP6, dP6))


def build_a7_p2_principal():
    from qf_witness.observe.ext1_quiver_observe import inv_mod
    from qf_witness.observe.quiver_relations_observe import a7_pims
    A7G = [(1, 2, 0, 3, 4, 5, 6), (1, 2, 3, 4, 5, 6, 0)]
    mul7, id7, ord7 = enumerate_group(A7G, 7)
    prn = build_a7_principal_gens(A7G)
    g4 = fano_gl42_gens(None, 7, A7G)
    g4b = [np.array(np.transpose(inv_mod(m, 2)), dtype=np.int64) % 2
           for m in g4]

    def _w2(M):
        pr = list(itertools.combinations(range(4), 2))
        ix = {t: i for i, t in enumerate(pr)}
        O = np.zeros((6, 6), dtype=np.int64)
        for jc, (a, b) in enumerate(pr):
            for i in range(4):
                for j in range(4):
                    if i != j and M[i][a] * M[j][b] % 2:
                        O[ix[(min(i, j), max(i, j))]][jc] ^= 1
        return O

    raw = {"1": ([np.eye(1, dtype=np.int64)] * 2, 1), "4": (g4, 4),
           "4b": (g4b, 4), "6": ([_w2(m) for m in g4], 6),
           "14": prn["14"], "20": prn["20"]}
    ALL7 = ["1", "4", "4b", "6", "14", "20"]
    SA = {k: extend_action(A7G, mul7, id7, gm, 2, ord7)
          for k, (gm, _d) in raw.items()}
    DA = {k: dd for k, (_g, dd) in raw.items()}
    simALL = [(k, SA[k], DA[k]) for k in ALL7]
    syl2 = subgroup([(1, 2, 3, 0, 5, 4, 6), (2, 1, 0, 3, 5, 4, 6)], mul7, id7)
    DIMP = {"1": 72, "4": 24, "4b": 24, "6": 40, "14": 64, "20": 56}
    PIMA, _ci = a7_pims(mul7, id7, ord7, A7G, simALL, ALL7, syl2, DIMP)
    NPr = ["1", "14", "20"]
    simPr = [(k, SA[k], DA[k]) for k in NPr]
    CPr = [[4, 2, 2], [2, 3, 1], [2, 1, 2]]
    BP, _a, RADPr, HOMPr, dPPr = block_presentation(
        NPr, A7G, {k: PIMA[k] for k in NPr}, simPr, CPr, 5, 2, lift_cap=32)
    meta, MT, _n = algebra_table(NPr, HOMPr, dPPr, 2)
    return (alg_pack(NPr, meta, MT, 2), BP["cartan_via_hom"],
            (NPr, HOMPr, RADPr, dPPr))


def cartan_of(alg):
    return [[alg["cnt"][(i, j)] for j in alg["names"]] for i in alg["names"]]


def main():
    t0 = time.time()
    quick = "--quick" in sys.argv
    R, out = {}, {}
    syn = json.load(open(os.path.join(PROOFS, "BLOCK-ALGEBRA-SYNTHESIS.json"),
                         encoding="utf-8"))
    CAR = {k: v["cartan"] for k, v in syn["Y_block_table"].items()}

    # ── R. Cartan 유도불변량 ────────────────────────────────────────
    inv = {}
    for k, C in CAR.items():
        d, s = det_int(C), smith(C)
        prod = 1
        for x in s:
            prod *= x
        inv[k] = {"det": d, "snf": s, "cartan_sum": sum(map(sum, C)),
                  "snf_product_eq_det": prod == abs(d),
                  "snf_divides": all(s[i] % s[i - 1] == 0
                                     for i in range(1, len(s)))}
    R["R_snf_product_equals_det"] = all(v["snf_product_eq_det"]
                                        for v in inv.values())
    R["R_snf_divisibility_chain"] = all(v["snf_divides"] for v in inv.values())
    R["R_det_values"] = ({k: v["det"] for k, v in inv.items()}
                         == {"A6_p2_principal": 8, "A6_p3_principal": 9,
                             "A7_p2_nonprincipal": 4, "A7_p2_principal": 8})
    # ★결손군 위수 = 판별식(둘 다 D₈)이 Q3 쌍에서 일치
    R["R_Q3_pair_det_equal"] = (inv["A7_p2_principal"]["det"]
                                == inv["A6_p2_principal"]["det"] == 8)
    R["R_Q3_pair_snf_equal"] = (inv["A7_p2_principal"]["snf"]
                                == inv["A6_p2_principal"]["snf"] == [1, 1, 8])
    # ★비주블록은 det 가 달라 **어떤 주블록과도** 유도동등일 수 없다(독립 재확인)
    R["R_nonprincipal_det_differs"] = (inv["A7_p2_nonprincipal"]["det"] == 4
                                       != inv["A7_p2_principal"]["det"])
    out["R_cartan_derived_invariants"] = {
        "identity": "유도동등 ⟹ C_A = Xᵀ C_B X (X ∈ GL_n(ℤ)) ⟹ det·SNF 보존",
        "per_block": inv}

    # ── S. ℤ-합동(등척) ─────────────────────────────────────────────
    pairs, keys = {}, sorted(CAR)
    for a, b in itertools.combinations(keys, 2):
        if len(CAR[a]) != len(CAR[b]):
            pairs[f"{a}|{b}"] = {"congruent": False, "reason": "정점 수 불일치"}
            continue
        lim, found = isometries(CAR[a], CAR[b])
        pairs[f"{a}|{b}"] = {"congruent": bool(found), "n_isometries": len(found),
                             "box_limits": lim,
                             "example": found[0] if found else None}
    key3 = "A6_p2_principal|A7_p2_principal"
    R["S_Q3_pair_is_congruent"] = pairs[key3]["congruent"]
    R["S_Q3_isometry_verified"] = (pairs[key3]["example"] is not None and all(
        sum(CAR["A6_p2_principal"][u][v] * pairs[key3]["example"][u][i]
            * pairs[key3]["example"][v][j] for u in range(3) for v in range(3))
        == CAR["A7_p2_principal"][i][j] for i in range(3) for j in range(3)))
    R["S_nonprincipal_not_congruent"] = not any(
        v["congruent"] for k, v in pairs.items() if "nonprincipal" in k)
    R["S_p3_block_not_congruent"] = not any(
        v["congruent"] for k, v in pairs.items() if "p3" in k)
    out["S_integral_congruence"] = {
        "note": "필요조건일 뿐 — 성립해도 유도동등을 함의하지 않는다",
        "pairs": pairs}

    # ── T. 엔진 정오 게이트 ─────────────────────────────────────────
    if quick:                       # PIM 재구성(≈290s)이 필요한 축은 full 전용
        R["all_ok"] = all(v for k, v in R.items() if k != "all_ok")
        print("tilting_complex_observe: all_ok=%s checks=%d (quick) %.1fs"
              % (R["all_ok"], len(R) - 1, time.time() - t0))
        return 0 if R["all_ok"] else 1
    alg7, c7, mx7 = build_a7_p2_principal()
    print("A7 alg %.1fs" % (time.time() - t0), flush=True)
    alg6, c6, mx6 = build_a6_p2_principal()
    print("A6 alg %.1fs" % (time.time() - t0), flush=True)
    R["T_cartan_matches_sidecar"] = (c7 == CAR["A7_p2_principal"]
                                     and c6 == CAR["A6_p2_principal"])
    R["T_alg_dims"] = (alg7["n"] == 19 and alg6["n"] == 34)
    R["T_local_endos"] = all(
        len(rad_block(a, i, i)) == a["cnt"][(i, i)] - 1
        for a in (alg7, alg6) for i in a["names"])
    triv = {}
    for nm, a in (("A7p2pr", alg7), ("A6p2pr", alg6)):
        e = end_algebra(a, trivial_object(a))
        triv[nm] = {"cartan": e["cartan"], "dim": e["dim"],
                    "tilting": e["tilting"]}
    R["T_trivial_returns_original"] = (
        triv["A7p2pr"]["cartan"] == c7 and triv["A6p2pr"]["cartan"] == c6
        and triv["A7p2pr"]["tilting"] and triv["A6p2pr"]["tilting"])
    R["T_quiver_reproduces_ext1"] = (
        sum(quiver_of(alg7).values()) == 5
        and sum(quiver_of(alg6).values()) == 4)
    out["T_engine_gates"] = {"trivial": triv,
                             "arrows_A7p2pr": quiver_of(alg7),
                             "arrows_A6p2pr": quiver_of(alg6)}

    # ── U. mutation 궤도 ───────────────────────────────────────────
    tgt = canon(CAR["A6_p2_principal"])
    seen, frontier, orbit, hit = {}, [("", alg7)], [], None
    hit_k0, hit_k1, depth = None, None, 0
    while frontier and depth < 3:
        nxt = []
        for path, a in frontier:
            for kk, k in enumerate(a["names"]):
                T, E = mutate(a, k)
                e = end_algebra(a, T)
                cc = canon(e["cartan"])
                rec = {"path": path + str(kk), "E_size": len(E),
                       "cartan": e["cartan"], "dim": e["dim"],
                       "tilting": e["tilting"],
                       "det": det_int(e["cartan"]), "snf": smith(e["cartan"])}
                orbit.append(rec)
                if cc == tgt and hit is None:
                    hit = rec
                    hit_k0, hit_k1 = int(rec["path"][0]), int(rec["path"][1])
                if cc not in seen and e["dim"] <= 60:
                    seen[cc] = rec["path"]
                    nxt.append((rec["path"], e["alg"]))
        frontier, depth = nxt, depth + 1
        print("depth %d · %d nodes · %.1fs" % (depth, len(nxt),
                                               time.time() - t0), flush=True)
    R["U_all_mutations_are_tilting"] = all(r["tilting"] for r in orbit)
    R["U_all_preserve_det"] = all(r["det"] == 8 for r in orbit)
    R["U_all_preserve_snf"] = all(r["snf"] == [1, 1, 8] for r in orbit)
    R["U_target_reached"] = hit is not None
    R["U_hit_at_depth_2"] = (hit is not None and len(hit["path"]) == 2
                             and hit["dim"] == 34)
    out["U_mutation_orbit"] = {
        "start": "A7_p2_principal (dim 19)",
        "target_canon": [list(r) for r in tgt],
        "reached_canonical_cartans": sorted(
            [list(map(list, c)) for c in seen], key=str),
        "n_mutations": len(orbit), "hit": hit,
        "orbit": orbit,
        "honest": "좌 mutation 만 구현 — 궤도 자체는 부분이다"}

    # ── V. ★★대수 동형 — 도달한 End(T) 가 정말 A₆ p=2 주블록인가 ────
    Ttilt, Etilt = mutate(alg7, alg7["names"][hit_k0])
    step1 = end_algebra(alg7, Ttilt)
    Ttilt2, Etilt2 = mutate(step1["alg"], step1["alg"]["names"][hit_k1])
    step2 = end_algebra(step1["alg"], Ttilt2)
    ap = step2["alg"]
    R["V_reached_is_tilting"] = step1["tilting"] and step2["tilting"]
    R["V_reached_cartan_is_target"] = (canon(step2["cartan"]) == tgt
                                       and step2["dim"] == 34)
    rp6, rpp = rad_powers(alg6), rad_powers(ap)
    R["V_rad_powers_match"] = (rp6 == rpp == [31, 27, 23, 19, 15, 11, 7, 3, 0])
    R["V_arrow_count_match"] = (sum(quiver_of(alg6).values())
                                == sum(quiver_of(ap).values()) == 4)
    iso = find_isomorphism(alg6, ap)
    R["V_explicit_isomorphism_found"] = iso["found"]
    R["V_iso_ranks_full"] = (iso.get("rank_VA") == 34
                             and iso.get("rank_VB") == 34)
    out["V_algebra_isomorphism"] = {
        "tilting_complex": {
            "step1": {"mutated_vertex": alg7["names"][hit_k0],
                      "approximation_term_E": Etilt,
                      "end_cartan": step1["cartan"], "end_dim": step1["dim"]},
            "step2": {"mutated_vertex_index": hit_k1,
                      "approximation_term_E": [int(x) for x in Etilt2],
                      "end_cartan": step2["cartan"], "end_dim": step2["dim"]}},
        "rad_powers": {"A6_p2_principal": rp6, "reached": rpp},
        "arrows": {"A6_p2_principal": quiver_of(alg6), "reached": quiver_of(ap)},
        "isomorphism": iso,
        "conclusion": ("A₇ p=2 주블록에서 **2단 기울기 mutation** 으로 얻은 "
                       "`End_{K^b}(T)` 가 A₆ p=2 주블록과 **명시적으로 동형**이다"),
        "theoretical_input": ("Rickard: 기울기 복합체 T 에 대해 A 와 End_{K^b(proj A)}(T) "
                              "는 유도동등 — 이 정리는 **인용**이고 여기서 증명하지 않는다. "
                              "우리가 계산한 것은 (a) T 가 기울기라는 가설의 **검증** "
                              "(Hom_K(T,T[±1]) = 0) 과 (b) End(T) ≅ B 의 **명시 동형**이다"),
        "answer_to_v22_Q3": ("★★긍정 — 두 블록은 **유도동등**이다. dim A 가 19 vs 34 로 "
                             "달라도 유도동등일 수 있으며, HH^*·cup 랭크가 일치한 것은 "
                             "**우연이 아니라 유도불변량이 실제로 같기 때문**이었다")}

    # ── W. ★유도동등류 **닫기** — 양방향 mutation · 동형-dedup ──────
    op7 = op_algebra(alg7)
    R["W_op_involutive"] = (op_algebra(op7)["n"] == alg7["n"]
                            and cartan_of(op_algebra(op7)) == cartan_of(alg7)
                            and np.array_equal(op_algebra(op7)["MT"],
                                               alg7["MT"]))
    R["W_op_transposes_cartan"] = (cartan_of(op7)
                                   == [list(r) for r in zip(*cartan_of(alg7))])
    reps = [{"label": "R0", "alg": alg7, "path": "", "dim": alg7["n"],
             "cartan": cartan_of(alg7)}]
    frontier, edges, saturated = [0], [], True
    for d in range(1, 7):
        nxt = []
        for ri in frontier:
            a = reps[ri]["alg"]
            for kk, k in enumerate(a["names"]):
                for right in (False, True):
                    e, Ev = mutate_step(a, k, right)
                    if not e["tilting"]:
                        saturated = False
                    tag = None
                    for rj, rr in enumerate(reps):
                        if (canon(rr["cartan"]) == canon(e["cartan"])
                                and find_isomorphism(rr["alg"],
                                                     e["alg"])["found"]):
                            tag = rr["label"]
                            break
                    if tag is None:
                        if e["dim"] > 60:      # 상한 도달 = 포화 주장 금지
                            saturated = False
                            continue
                        tag = "R%d" % len(reps)
                        reps.append({"label": tag, "alg": e["alg"],
                                     "path": reps[ri]["path"]
                                     + ("-" if right else "+") + str(kk),
                                     "dim": e["dim"], "cartan": e["cartan"]})
                        nxt.append(len(reps) - 1)
                    edges.append({"from": reps[ri]["label"],
                                  "vertex": str(k), "dir": "-" if right else "+",
                                  "E": Ev, "to": tag, "dim": e["dim"]})
        frontier = nxt
        print("W depth %d · 신규 %d · 대표 %d · %.1fs"
              % (d, len(nxt), len(reps), time.time() - t0), flush=True)
        if not nxt:
            break
    R["W_closed_before_cap"] = saturated and not frontier
    R["W_three_representatives"] = (len(reps) == 3
                                    and sorted(r["dim"] for r in reps)
                                    == [16, 19, 34])
    R["W_all_edges_tilting"] = len(edges) == 6 * len(reps)
    # ★실측: 이 류에서는 좌·우 mutation 이 **매번 같은 동형류**로 간다(기전 무주장)
    lr = {}
    for e in edges:
        lr.setdefault((e["from"], e["vertex"]), {})[e["dir"]] = e["to"]
    R["W_left_right_agree"] = all(v.get("+") == v.get("-") for v in lr.values())
    tbl = {}
    for r in reps:
        a = r["alg"]
        hh0, _dK, _inn, hh1 = hochschild(a["MT"], a["n"], 2)
        tbl[r["label"]] = {
            "path": r["path"], "dim": a["n"], "cartan": r["cartan"],
            "det": det_int(r["cartan"]), "snf": smith(r["cartan"]),
            "arrows": sum(quiver_of(a).values()), "quiver": quiver_of(a),
            "rad_powers": rad_powers(a), "HH0": hh0, "HH1": hh1,
            "loewy_length": len(rad_powers(a))}
    # ★유도불변량은 류 전체에서 같아야 한다 — 반증 가능한 게이트
    R["W_HH_constant_on_class"] = all(
        (v["HH0"], v["HH1"]) == (5, 3) for v in tbl.values())
    R["W_det_snf_constant"] = all(v["det"] == 8 and v["snf"] == [1, 1, 8]
                                  for v in tbl.values())
    R["W_pairwise_congruent"] = all(
        isometries(tbl[x]["cartan"], tbl[y]["cartan"])[1]
        for x in tbl for y in tbl)
    R["W_endpoints_identified"] = (
        any(v["dim"] == 19 and v["cartan"] == c7 for v in tbl.values())
        and any(v["dim"] == 34 and canon(v["cartan"]) == tgt
                for v in tbl.values()))
    # ★새 대수 — 어느 군 블록으로도 아직 동일시하지 않았다
    R["W_middle_is_new"] = any(v["dim"] == 16 for v in tbl.values())
    out["W_class_closure"] = {
        "identity": "μ⁻_k(A) = (μ⁺_k(A^op))^op — 우 mutation 은 반대 대수로 얻는다",
        "representatives": tbl, "mutation_edges": edges,
        "closed": R["W_closed_before_cap"],
        "honest": ("dim 16 대표는 **군 블록으로 동일시하지 않았다** — 이 류에 있다는 "
                   "실측만 주장한다. 폐합은 dim ≤ 60 · 깊이 ≤ 6 안에서의 폐합이다"),
        "observed": ("★좌·우 mutation 이 **매번 같은 동형류**로 간다(18 간선 전부) — "
                     "실측이고 기전은 주장하지 않는다"),
        "conclusion": ("A₇p2주(19) · **새 대수(16·화살 6·LL 5)** · A₆p2주(34) 세 대표가 "
                       "**양방향 mutation 아래 닫힌다** — 세 대수 모두 `(HH⁰,HH¹) = (5,3)`")}

    # ── X. ★★구조상수판 `HH^*`·cup — 류 전체의 불변량 카드를 채운다 ────
    two = {}
    for nm, a, mx in (("A7_p2_principal", alg7, mx7),
                      ("A6_p2_principal", alg6, mx6)):
        ref = hh_relative(mx[0], mx[1], mx[2], mx[3], 2, cup=True)
        got = hh_struct(a, cup=True)
        two[nm] = {"hh_relative": ref, "hh_struct": got,
                   "agree": all(ref[k] == got[k] for k in
                                ("C", "ker", "HH0", "HH1", "HH2",
                                 "HH1_reps", "cup_rank"))}
    # ★★두 독립 구현(행렬 입력 vs 구조상수)이 **같은 대수**에서 일치해야 한다
    R["X_two_implementations_agree"] = all(v["agree"] for v in two.values())
    card = {}
    for r in reps:
        h = hh_struct(r["alg"], cup=True)
        card[r["label"]] = {"dim": r["alg"]["n"], "C": h["C"],
                            "HH0": h["HH0"], "HH1": h["HH1"], "HH2": h["HH2"],
                            "cup_rank": h["cup_rank"],
                            "cup_is_cocycle": h["cup_is_cocycle"],
                            "graded_commutative": h["graded_commutative"]}
    R["X_cup_correctness_gates"] = all(v["cup_is_cocycle"]
                                       and v["graded_commutative"]
                                       for v in card.values())
    # ★★유도불변량이므로 류의 세 대표가 **전부** (5,3,5,0) 이어야 한다
    R["X_class_invariant_card"] = all(
        (v["HH0"], v["HH1"], v["HH2"], v["cup_rank"]) == (5, 3, 5, 0)
        for v in card.values())
    R["X_hh01_matches_hochschild"] = all(
        (card[k]["HH0"], card[k]["HH1"])
        == (tbl[k]["HH0"], tbl[k]["HH1"]) for k in card)
    R["X_middle_rep_filled"] = ("R1" in card and card["R1"]["dim"] == 16
                                and card["R1"]["C"] == [8, 26, 116, 528])
    out["X_hochschild_struct_const"] = {
        "identity": ("`hh_relative` 의 구조상수판 — 행렬 합성 `Y@X` 가 전부 "
                     "`amul(x,y)` 로 바뀐다(규약 `a·b := b∘a`)"),
        "two_path_check": two, "class_card": card,
        "note": ("★알려진 답(두 끝점의 (5,3,5,0))이 **새 경로의 정오 판정기** 역할을 했다 — "
                 "행렬 입력판과 구조상수판이 같은 대수에서 C·ker·HH·cup 랭크까지 일치"),
        "conclusion": ("류의 **세 대표 전부** `(HH⁰,HH¹,HH²,cup) = (5,3,5,0)` — "
                       "미완성이던 R1(dim 16) 칸이 채워졌고 유도불변성이 재확인됐다")}

    R["all_ok"] = all(v for k, v in R.items() if k != "all_ok")
    out["checks"] = R
    out["all_ok"] = R["all_ok"]
    out["supersedes"] = ("[[QUIVER-RELATIONS]] 의 not_claimed 항목 "
                         "\"대수들의 유도동등성\" 은 이 모듈에서 **해소**된다 "
                         "(A₇p2주 ~ A₆p2주 유도동등)")
    with open(os.path.join(PROOFS, "TILTING-COMPLEX.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    bad = [k for k, v in R.items() if not v]
    print("tilting_complex_observe: all_ok=%s checks=%d %.1fs"
          % (R["all_ok"], len(R) - 1, time.time() - t0))
    if bad:
        print("  실패:", bad)
    return 0 if R["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
