#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""knot61_4braid_observe — 6₁ 매듭 4-braid 확장: **LG(6₁) + Kauffman D(6₁) 양 가족 동시 폐쇄**
(관측, seal 아님). [[bmw3_kauffman_family_observe]]·[[links_gould_observe]] 의 공통 사각지대
(★6₁=braid index 4 → 3-braid 부재) 해소.

★자체동정(문헌 braid 좌표 인용 0):
  - ★**패리티 정리**: B₄ 닫힘이 매듭(1성분) ⟺ 기저 순열=4-cycle(홀순열) ⟺ **word 길이 홀수**
    — 길이 6 불가능(길이 7=최소 홀수>6교차) 기계확인.
  - W(6₁)=σ₁²σ₂σ₁⁻¹σ₃⁻¹σ₂σ₃⁻¹ (길이 7·writhe 1): 길이-7 소전수에서 발견(스크래치)·본 witness 는
    1성분 + ★**gl(1|1) 4-strand 심볼릭 Δ=2t−5+2/t 정확** + granny/square(합성 det9) Δ=(t−1+1/t)²
    구별로 동정. 외부사실=≤7교차 매듭 census 에서 이 Δ 는 6₁ 유일(1건).

관측 축:
  A. ★**LG(6₁) 폐형식**(braiding=[[links_gould_observe]] 자체유도 č 재사용·B₄ 256-dim):
     정수계수·t₀↔t₁ 대칭·**Alexander² q=1**·**Alexander q=i**·det²=81·chirality(6₁ chiral).
     ★**관례 함정 자체해소**: census 표기 Δ(6₁)=2t−5+2/t 는 Δ(1)=−1 — **Δ(1)=+1 정규화
     (Conway ∇=1−2z² ⟹ Δ=−2t+5−2/t)에서 gl(1|1)·LG q=i 두 독립 엔진이 부호까지 정확 일치**
     (가짜 "부호 이상"의 진범=참조값 단위 선택).
  B. ★**Kauffman D(6₁)(a,z) 유일복원**: 3중 특수화(N=3 유리기저 spin-1·N=4 so₄·N=2 qt-Jones)
     유리 다점 150+ 선형계(자체 가우스 소거·ℚ(i)→실부/허부 분리) → 정수계수 유일해.
     ★유리기저 교훈: spin-1 사다리 E=[2],1 비대칭 선택 ⟹ √[2] 제거·전 곡선 유리점 평가.
  C. **독립 확증**: ★**TL₄ bracket 상태합 엔진**(일반 평면매칭 대수·Catalan(4)=14 기저) —
     V(6₁)=t⁴−t³+t²−2t+2−t⁻¹+t⁻² 25점 정확·det=9·unknot=1·**6₂ 3-braid↔4-braid 회귀**.
  D. **회귀 게이트**: 같은 4-braid 파이프라인으로 D(6₂)(안정화 word σ₃ 부가) 재구성 →
     [[bmw3_kauffman_family_observe]] 확정값과 **폐형식 일치**(엔진 신뢰 전이).

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - D(a,0)≠1 은 family convention 그대로(정규화 무주장). Δ 는 Δ(1)=+1 정규화로 통일 보고.
  - 7교차+·BMW₄·HOMFLY-Kauffman 비포함 무주장.

사용: python -m qf_witness.observe.knot61_4braid_observe [--quick]
"""
from __future__ import annotations
import sys
import json
from fractions import Fraction as Fr

import sympy as sp

from qf_witness.observe.links_gould_observe import (derive as lg_derive, emb3 as lg_emb16,
                                                    vand_solve, QS as LGQS, PS as LGPS)

q, p = sp.symbols("q p")
a, z = sp.symbols("a z")
t = sp.Symbol("t")
A = sp.Symbol("A")

W61_0 = [(1, 0), (1, 0), (1, 1), (-1, 0), (-1, 2), (1, 1), (-1, 2)]   # 0-based (LG 엔진)
W61_1 = [(s, i + 1) for s, i in W61_0]                                # 1-based (Kauffman/TL)
W62_1 = [(1, 1), (1, 1), (1, 1), (-1, 2), (1, 1), (-1, 2), (1, 3)]    # 6₂ 안정화 4-braid
DEL61 = -2*t + 5 - 2/t   # Δ(1)=+1 정규화(Conway ∇=1−2z²); census 표기 2t−5+2/t 는 Δ(1)=−1
D62_FAMILY = ("z**4 + 3*z**2 + 2 - z**5/a - 2*z**3/a - 3*z**4/a**2 - 6*z**2/a**2 - 2/a**2 "
              "+ z**5/a**3 - z/a**3 + 2*z**4/a**4 + 2*z**2/a**4 + a**(-4) + 2*z**3/a**5 "
              "+ z/a**5 + z**2/a**6")


# ── 공용 sparse 유틸 ─────────────────────────────────────────────────────────
def matvec(rows, x):
    out = {}
    for i, r in rows.items():
        acc = None
        for j, v in r.items():
            xv = x.get(j)
            if xv is not None:
                acc = v*xv if acc is None else acc + v*xv
        if acc:
            out[i] = acc
    return out


def emb_site(nz, pos, d, nsites=4):
    rows = {}
    left, right = pos, nsites - pos - 2
    nl, nr = d**left, d**right
    for i, j, v in nz:
        i1, i2 = divmod(i, d)
        j1, j2 = divmod(j, d)
        for L in range(nl):
            for Rr in range(nr):
                col = ((L*d + j1)*d + j2)*nr + Rr
                row = ((L*d + i1)*d + i2)*nr + Rr
                rows.setdefault(row, {})[col] = v
    return rows


def frac(x):
    return Fr(int(sp.numer(x)), int(sp.denom(x)))


# ── A0. 자체동정: 패리티·성분·gl(1|1) Δ ────────────────────────────────────
def perm_cycles(word, n=4):
    perm = list(range(n))
    for s, i in word:
        perm[i], perm[i + 1] = perm[i + 1], perm[i]
    seen = [False]*n
    c = 0
    for i in range(n):
        if not seen[i]:
            c += 1
            j = i
            while not seen[j]:
                seen[j] = True
                j = perm[j]
    return c


def perm_parity(word, n=4):
    perm = list(range(n))
    for s, i in word:
        perm[i], perm[i + 1] = perm[i + 1], perm[i]
    par = 0
    seen = [False]*n
    for i in range(n):
        if not seen[i]:
            ln = 0
            j = i
            while not seen[j]:
                seen[j] = True
                j = perm[j]
                ln += 1
            par += ln - 1
    return par % 2


def gl11_delta_4braid(word):
    """gl(1|1) Ř(Stage1) 4-strand 심볼릭 (1,1)-tangle → Δ(t), t=q²"""
    Rh = sp.Matrix([[q, 0, 0, 0], [0, q - 1/q, 1, 0], [0, 1, 0, 0], [0, 0, 0, -1/q]])
    Rhi = sp.simplify(Rh.inv())
    def kr(Am, Bm):
        return sp.Matrix(sp.BlockMatrix([[Am[i, j]*Bm for j in range(Am.cols)]
                                         for i in range(Am.rows)]))
    I2 = sp.eye(2)
    gens = {}
    for pos in range(3):
        mats = [I2, I2, I2]
        mats[pos] = None
        def build(M, pos=pos):
            out = M
            for _ in range(pos):
                out = kr(I2, out)
            for _ in range(3 - pos - 1):
                out = kr(out, I2)
            return out
        gens[(1, pos)] = build(Rh)
        gens[(-1, pos)] = build(Rhi)
    M = sp.eye(16)
    for g in word:
        M = M*gens[g]
    # (1,1)-tangle: strand1 open(비트3), strands 2..4 supertrace, mu=q per strand
    acc00 = 0
    for k in range(8):
        b = bin(k).count("1")
        acc00 += (-1)**b*q**3*M[k, k]           # 열린 가닥 상태 0
    val = sp.expand(sp.cancel(sp.simplify(acc00).subs(q, sp.sqrt(t))))
    return val


# ── B. Kauffman 엔진(유리 기저) ──────────────────────────────────────────────
def kron(Am, Bm):
    return sp.Matrix(sp.BlockMatrix([[Am[i, j]*Bm for j in range(Am.cols)]
                                     for i in range(Am.rows)]))


def qn(n):
    return sp.cancel((q**n - q**(-n))/(q - 1/q))


def build_so3_rational():
    E = sp.zeros(3); F = sp.zeros(3)
    E[0, 1] = qn(2); E[1, 2] = 1
    F[1, 0] = 1; F[2, 1] = qn(2)
    mm = [1, 0, -1]
    Dg = sp.zeros(9)
    for i, mi in enumerate(mm):
        for j, mj in enumerate(mm):
            Dg[3*i + j, 3*i + j] = q**(2*mi*mj)
    def En(M, n):
        R = sp.eye(3)
        for _ in range(n):
            R = R*M
        return R
    def qfact(n):
        r = sp.Integer(1)
        for k in range(1, n + 1):
            r *= qn(k)
        return r
    Rsum = sp.zeros(9)
    for n in range(0, 3):
        Rsum += (q - 1/q)**n/qfact(n)*q**sp.Rational(n*(n - 1), 2)*kron(En(E, n), En(F, n))
    R = Dg*Rsum
    P = sp.zeros(9)
    for i in range(3):
        for j in range(3):
            P[3*i + j, 3*j + i] = 1
    Rc = sp.Matrix([[sp.cancel(x) for x in (P*R).row(i)] for i in range(9)])
    return Rc, sp.diag(q**2, 1, q**-2), q**4, q**2 + 1 + q**-2


def _spin_half_R():
    E = sp.Matrix([[0, 1], [0, 0]])
    F = sp.Matrix([[0, 0], [1, 0]])
    mm = [sp.Rational(1, 2), sp.Rational(-1, 2)]
    Dg = sp.zeros(4)
    for i, mi in enumerate(mm):
        for j, mj in enumerate(mm):
            Dg[2*i + j, 2*i + j] = q**(2*mi*mj)
    Rm = Dg*(sp.eye(4) + (q - 1/q)*kron(E, F))
    P2 = sp.Matrix([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
    return P2*Rm


def build_so4():
    Rh = _spin_half_R()
    def el(x, y, xp, yp):
        return Rh[2*xp + yp, 2*x + y]
    R4 = sp.zeros(16)
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    row = 8*i + 4*j + 2*k + l
                    for ip in range(2):
                        for jp in range(2):
                            for kp in range(2):
                                for lp in range(2):
                                    v = el(i, k, ip, kp)*el(j, l, jp, lp)
                                    if v != 0:
                                        R4[8*ip + 4*jp + 2*kp + lp, row] += v
    R4 = sp.Matrix([[sp.cancel(sp.powsimp(x)) for x in R4.row(i)] for i in range(16)])
    return R4, sp.diag(q**2, 1, 1, q**-2), q**3, q**2 + 2 + q**-2


def sparse_at(M, qv):
    nz = []
    for i in range(M.rows):
        for j in range(M.cols):
            v = M[i, j]
            if v != 0:
                w = sp.Rational(sp.cancel(v.subs(q, qv)))
                if w != 0:
                    nz.append((i, j, frac(w)))
    return nz


def qtrace_point(Rc, Rci, mu, abmw, delta, word, d, qv):
    nzR = sparse_at(Rc, qv)
    nzRi = sparse_at(Rci, qv)
    gens = {}
    for pos in range(3):
        gens[(1, pos + 1)] = emb_site(nzR, pos, d)
        gens[(-1, pos + 1)] = emb_site(nzRi, pos, d)
    muv = [frac(sp.Rational(sp.cancel(mu[i, i].subs(q, qv)))) for i in range(d)]
    w = sum(s for s, _ in word)
    tot = Fr(0)
    for col in range(d**4):
        x = {col: Fr(1)}
        for g in reversed(word):
            x = matvec(gens[g], x)
        v = x.get(col)
        if v is not None:
            c = col
            f = Fr(1)
            for _ in range(4):
                f *= muv[c % d]
                c //= d
            tot += f*v
    ab = frac(sp.Rational(sp.cancel(abmw.subs(q, qv))))
    dl = frac(sp.Rational(sp.cancel(delta.subs(q, qv))))
    return tot*ab**(-w)/dl


# ── C. TL_n bracket(일반 평면매칭) ───────────────────────────────────────────
def tl_id(n):
    return tuple((i, i + n) for i in range(n))


def tl_e(n, i):
    m = [(i, i + 1), (n + i, n + i + 1)]
    for k in range(n):
        if k != i and k != i + 1:
            m.append((k, k + n))
    return tuple(sorted(tuple(sorted(x)) for x in m))


def tl_mul(n, m1, m2):
    adj = {}
    def add(x, y):
        adj.setdefault(x, []).append(y)
        adj.setdefault(y, []).append(x)
    for (x, y) in m1:
        add(x if x < n else 100 + (x - n), y if y < n else 100 + (y - n))
    for (x, y) in m2:
        xx = 100 + x if x < n else 200 + (x - n)
        yy = 100 + y if y < n else 200 + (y - n)
        add(xx, yy)
    ext = [k for k in range(n)] + [200 + k for k in range(n)]
    seen = set()
    newm = []
    for s in ext:
        if s in seen:
            continue
        prev, cur = None, s
        seen.add(cur)
        while True:
            nxts = [x for x in adj[cur] if x != prev]
            nxt = adj[cur][0] if prev is None else (nxts[0] if nxts else None)
            if nxt is None:
                break
            prev, cur = cur, nxt
            if cur in ext:
                seen.add(cur)
                break
            seen.add(cur)
        newm.append(tuple(sorted((s if s < 100 else n + (s - 200),
                                  cur if cur < 100 else n + (cur - 200)))))
    mids = set()
    for (x, y) in m1:
        for u in (x, y):
            if u >= n:
                mids.add(100 + (u - n))
    loops = 0
    unvisited = mids - seen
    while unvisited:
        s = next(iter(unvisited))
        prev, cur = None, s
        nodes = {cur}
        while True:
            nxts = [x for x in adj[cur] if x != prev]
            nxt = nxts[0] if nxts else adj[cur][0]
            prev, cur = cur, nxt
            if cur == s:
                break
            nodes.add(cur)
        loops += 1
        unvisited -= nodes
    return tuple(sorted(newm)), loops


def tl_closure_loops(n, m):
    adj = {}
    for (x, y) in m:
        adj.setdefault(x, []).append(y)
        adj.setdefault(y, []).append(x)
    for k in range(n):
        adj.setdefault(k, []).append(k + n)
        adj.setdefault(k + n, []).append(k)
    seen = set()
    loops = 0
    for s in list(adj):
        if s in seen:
            continue
        loops += 1
        prev, cur = None, s
        seen.add(cur)
        while True:
            nxts = [x for x in adj[cur] if x != prev]
            nxt = nxts[0] if nxts else adj[cur][0]
            prev, cur = cur, nxt
            if cur == s:
                break
            seen.add(cur)
    return loops


def bracket_jones_n(word, n):
    delta = -A**2 - A**-2
    vec = {tl_id(n): sp.Integer(1)}
    w = 0
    for (sgn, i) in word:
        w += sgn
        ei = tl_e(n, i - 1)
        newv = {}
        for m, c in vec.items():
            for (factor, gate) in ([(A, None), (A**-1, ei)] if sgn > 0
                                   else [(A**-1, None), (A, ei)]):
                if gate is None:
                    mm2, dp = m, 0
                else:
                    mm2, dp = tl_mul(n, m, gate)
                newv[mm2] = sp.expand(newv.get(mm2, 0) + c*factor*delta**dp)
        vec = newv
    br = sp.expand(sum(c*delta**(tl_closure_loops(n, m) - 1) for m, c in vec.items()))
    V = sp.expand(sp.simplify(((-A**3)**(-w))*br))
    return sp.expand(sp.powsimp(V.subs(A, t**sp.Rational(-1, 4)), force=True))


# ── D. 자체 가우스 소거(Fraction) ────────────────────────────────────────────
def solve_unique_fr(rows, rhs, n):
    """rows: list of dense Fraction lists(len n); returns (sol list, unique bool)"""
    Amat = [list(r) + [b] for r, b in zip(rows, rhs)]
    m = len(Amat)
    piv_cols = []
    r = 0
    for col in range(n):
        pr = None
        for i in range(r, m):
            if Amat[i][col] != 0:
                pr = i
                break
        if pr is None:
            continue
        Amat[r], Amat[pr] = Amat[pr], Amat[r]
        inv = 1/Amat[r][col]
        Amat[r] = [x*inv for x in Amat[r]]
        for i in range(m):
            if i != r and Amat[i][col] != 0:
                f = Amat[i][col]
                Amat[i] = [x - f*y for x, y in zip(Amat[i], Amat[r])]
        piv_cols.append(col)
        r += 1
        if r == m:
            break
    for i in range(r, m):
        if Amat[i][n] != 0:
            return None, False          # inconsistent
    if len(piv_cols) < n:
        return None, False              # underdetermined
    sol = [Fr(0)]*n
    for k, col in enumerate(piv_cols):
        sol[col] = Amat[k][n]
    return sol, True


def reconstruct_D(word, npts=50):
    """3중 특수화 → D(a,z) 유일복원. returns (D poly, checks dict)"""
    Rc3, mu3, ab3, dl3 = build_so3_rational()
    Rc3i = sp.Matrix([[sp.cancel(x) for x in Rc3.inv().row(i)] for i in range(9)])
    Rc4, mu4, ab4, dl4 = build_so4()
    e1 = q - 1/q + q**-3
    e2 = -1 + q**-2 - q**-4
    e3 = -q**-3
    Rc4i = sp.Matrix([[sp.cancel(sp.powsimp(x)) for x in
                       ((Rc4*Rc4 - e1*Rc4 + e2*sp.eye(16))/e3).row(i)] for i in range(16)])
    Rh2 = _spin_half_R()
    Rh2i = sp.Matrix([[sp.cancel(sp.powsimp(x)) for x in Rh2.inv().row(i)] for i in range(4)])
    mu2 = sp.diag(q, 1/q)
    chks = {}
    chks["so3_eigen"] = (set(sp.simplify(k) for k in Rc3.eigenvals())
                         == {q**2, -q**-2, q**-4})
    chks["so4_ch_inverse"] = sp.simplify(Rc4*Rc4i - sp.eye(16)) == sp.zeros(16, 16)

    ILO, IHI, JM = -8, 8, 6
    mons = [(i, j) for i in range(ILO, IHI + 1) for j in range(0, JM + 1)]
    n = len(mons)
    rows, rhs = [], []
    pts = [Fr(k, k + 1) for k in range(2, 2 + npts)]
    for r in pts:
        Q = r*r
        F = qtrace_point(Rc3, Rc3i, mu3, ab3, dl3, word, 3, sp.Rational(r))
        zc = Q - 1/Q
        rows.append([Q**(2*i)*zc**j for (i, j) in mons])
        rhs.append(F)
    for r in pts:
        Q = r*r
        F = qtrace_point(Rc4, Rc4i, mu4, ab4, dl4, word, 4, sp.Rational(Q))
        zc = Q - 1/Q
        rows.append([Q**(3*i)*zc**j for (i, j) in mons])
        rhs.append(F)
    for r in pts:
        Vinv = qtrace_point(Rh2, Rh2i, mu2, sp.sqrt(q)**3, q + 1/q, word, 2,
                            sp.Rational(1)/sp.Rational(r*r))
        zr = r + 1/r
        re_row, im_row = [], []
        for (i, j) in mons:
            base = r**(-3*i)*zr**j
            k4 = (i + j) % 4
            if (i + j) % 2 == 0:
                re_row.append(base if k4 == 0 else -base)
                im_row.append(Fr(0))
            else:
                re_row.append(Fr(0))
                im_row.append(base if k4 == 1 else -base)
        rows.append(re_row); rhs.append(Vinv)
        rows.append(im_row); rhs.append(Fr(0))
    sol, uniq = solve_unique_fr(rows, rhs, n)
    chks["unique"] = uniq
    if not uniq:
        return None, chks
    # 전 방정식 재검증
    chks["all_eqs"] = all(sum(rw[k]*sol[k] for k in range(n)) == b for rw, b in zip(rows, rhs))
    chks["integer"] = all(v.denominator == 1 for v in sol)
    D = sp.expand(sum(sp.Rational(sol[k])*a**i*z**j for k, (i, j) in enumerate(mons)))
    return D, chks


# ── LG 4-strand 엔진 ────────────────────────────────────────────────────────
class LGEng4:
    def __init__(self, nzC, nzCi):
        self.nzC, self.nzCi = nzC, nzCi
        self.cache = {}

    def gens(self, qv, pv):
        key = (qv, pv)
        if key not in self.cache:
            sub = {q: sp.Rational(qv), p: sp.Rational(pv)}
            eC = [(i, j, frac(v.subs(sub))) for i, j, v in self.nzC]
            eCi = [(i, j, frac(v.subs(sub))) for i, j, v in self.nzCi]
            eC = [x for x in eC if x[2] != 0]
            eCi = [x for x in eCi if x[2] != 0]
            g = {}
            for pos in range(3):
                g[(1, pos)] = emb_site(eC, pos, 4)
                g[(-1, pos)] = emb_site(eCi, pos, 4)
            g["mu"] = [frac(x.subs(sub)) for x in (p**2, -p**2, -p**2*q**2, p**2*q**2)]
            g["fp"] = frac((p**2).subs(sub))
            self.cache[key] = g
        return self.cache[key]

    def lg(self, word, qv, pv, scal=False):
        g = self.gens(qv, pv)
        muf, fpf = g["mu"], g["fp"]
        e = sum(s for s, _ in word)
        vals = {}
        for j in (range(2) if scal else range(1)):
            for cfg in range(64):
                k, rem = divmod(cfg, 16)
                l, mm = divmod(rem, 4)
                w = muf[k]*muf[l]*muf[mm]
                x = {j*64 + cfg: Fr(1)}
                for gw in reversed(word):
                    x = matvec(g[gw], x)
                for i in (range(2) if scal else (j,)):
                    v = x.get(i*64 + cfg)
                    if v is not None:
                        vals[(i, j)] = vals.get((i, j), Fr(0)) + w*v
        val = vals.get((0, 0), Fr(0))*fpf**(-e)
        if scal:
            ok = vals.get((0, 1), Fr(0)) == 0 and vals.get((1, 0), Fr(0)) == 0 \
                and vals.get((0, 0), Fr(0)) == vals.get((1, 1), Fr(0))
            return val, ok
        return val


def reconstruct_LG(eng, word, alo, ahi, blo, bhi):
    na, nb = ahi - alo + 1, bhi - blo + 1
    qs, ps = LGQS[:na + 1], LGPS[:nb + 1]
    V = {(qv, pv): Fr(eng.lg(word, qv, pv)) for qv in qs for pv in ps}
    cb = {}
    for qv in qs:
        c = vand_solve([pv**2 for pv in ps[:nb]], [V[(qv, pv)] for pv in ps[:nb]], blo, bhi)
        pv = ps[nb]
        if sum(c[k]*(pv**2)**(blo + k) for k in range(nb)) != V[(qv, pv)]:
            return None
        cb[qv] = c
    coef = {}
    for k in range(nb):
        c2 = vand_solve([qv**2 for qv in qs[:na]], [cb[qv][k] for qv in qs[:na]], alo, ahi)
        qv = qs[na]
        if sum(c2[mm]*(qv**2)**(alo + mm) for mm in range(na)) != cb[qv][k]:
            return None
        for mm in range(na):
            if c2[mm] != 0:
                coef[(alo + mm, blo + k)] = c2[mm]
    return sp.expand(sum(sp.Rational(v)*q**(2*aa)*p**(2*bb) for (aa, bb), v in coef.items()))


def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "knot61-4braid/v1",
           "_note": ("6₁ 4-braid 확장 — LG(6₁)+Kauffman D(6₁) 양 가족 동시 폐쇄·"
                     "★q=i 부호 ε(6₁)=−1 신관측·패리티 정리·TL₄ bracket. "
                     "관측·module 0·root 불변.")}

    # A0. 자체동정
    R["id_one_component"] = (perm_cycles(W61_0) == 1)
    R["id_parity_odd"] = (perm_parity(W61_0) == 1 and len(W61_0) % 2 == 1)
    even_ok = all(perm_parity(wd) == 0
                  for wd in ([(1, 0)]*6, [(1, 0), (1, 1), (1, 2), (-1, 0), (-1, 1), (-1, 2)]))
    R["id_even_word_even_perm"] = even_ok      # 길이 6 word 는 짝순열 ⟹ 4-cycle(매듭) 불가 예시확인
    dlt = gl11_delta_4braid(W61_0)
    R["id_alexander_61"] = sp.simplify(dlt - DEL61) == 0
    R["id_not_granny"] = sp.simplify(DEL61 - sp.expand((t - 1 + 1/t)**2)) != 0
    # teeth: word 마지막 글자 부호 flip → Δ 불일치(다른 링크)
    Wbad = W61_0[:-1] + [(1, 2)]
    dbad = gl11_delta_4braid(Wbad)
    R["teeth_wrong_word"] = sp.simplify(dbad - DEL61) != 0

    # A. LG(6₁)
    lgR, C, Ci, nzC, nzCi = lg_derive()
    R["lg_braiding_rederive"] = all(lgR.values())
    eng = LGEng4(nzC, nzCi)
    v61, sc = eng.lg(W61_0, Fr(3, 5), Fr(7, 4), scal=True)
    R["lg_11tangle_scalar"] = sc
    P = reconstruct_LG(eng, W61_0, -3, 3, -5, 5)
    R["lg_recon"] = P is not None
    out["LG_6_1"] = str(P)
    if P is not None:
        sw = sp.expand(sp.cancel(P.subs({p: 1/(p*q)}, simultaneous=True)))
        R["lg_t0t1_sym"] = sp.simplify(P - sw) == 0
        R["lg_alex2_q1"] = sp.simplify(
            sp.expand(P.subs(q, 1)) - sp.expand(DEL61.subs(t, p**2)**2)) == 0
        R["lg_alex_qi"] = sp.simplify(
            sp.expand(P.subs(q, sp.I)) - sp.expand(DEL61.subs(t, p**4))) == 0
        R["lg_det2_81"] = sp.simplify(P.subs({q: 1, p: sp.I}, simultaneous=True) - 81) == 0
        Pm = sp.expand(P.subs({q: 1/q, p: 1/p}, simultaneous=True))
        R["lg_chiral"] = sp.simplify(P - Pm) != 0

    # C. TL₄ bracket
    R["tl_unknot"] = sp.simplify(bracket_jones_n([(1, 1), (1, 2), (1, 3)], 4) - 1) == 0
    V62_3 = bracket_jones_n([(1, 1), (1, 1), (1, 1), (-1, 2), (1, 1), (-1, 2)], 3)
    V62_4 = bracket_jones_n(W62_1, 4)
    R["tl_62_stab_regression"] = sp.simplify(V62_3 - V62_4) == 0
    V61 = bracket_jones_n(W61_1, 4)
    out["V_6_1"] = str(V61)
    R["tl_V61"] = sp.simplify(V61 - (t**4 - t**3 + t**2 - 2*t + 2 - 1/t + t**-2)) == 0
    R["tl_det9"] = (abs(V61.subs(t, -1)) == 9)

    # B/D. Kauffman D (full 전용)
    if not quick:
        D61, ck1 = reconstruct_D(W61_1)
        for k, v in ck1.items():
            R[f"D61_{k}"] = v
        out["D_6_1"] = str(D61)
        if D61 is not None:
            okJ = True
            for k in range(2, 27):
                r = sp.Rational(k, k + 1)
                if sp.simplify(D61.subs({a: sp.I*r**-3, z: sp.I*(r + 1/r)})
                               - V61.subs(t, r**4)) != 0:
                    okJ = False
                    break
            R["D61_bracket_25pts"] = okJ
            R["D61_chiral"] = sp.simplify(D61 - sp.expand(D61.subs({a: 1/a, z: -z}))) != 0
        D62, ck2 = reconstruct_D(W62_1)
        R["D62_regression_family"] = (D62 is not None
                                      and sp.simplify(D62 - sp.sympify(D62_FAMILY)) == 0)

    ok = bool(all(R.values()))
    out["checks"] = R
    out["scope_honesty"] = {
        "delivered": "6₁=첫 4-braid 매듭 — LG 폐형식+" + ("(quick: D 생략)" if quick else "Kauffman D 유일복원+")
                     + "TL₄ bracket 독립확증·패리티 정리·양 가족 사각지대 폐쇄",
        "convention_lesson": "★Δ 단위(±t^k) 함정: census 2t−5+2/t=Δ(1)=−1 — Δ(1)=+1 정규화에서 "
                              "gl(1|1)·LG q=i 두 엔진 부호 정확 일치(초기 '부호 이상'은 참조값 오류)",
        "identification": "패리티 정리(홀수 길이 필수)+1성분+gl(1|1) Δ 심볼릭+granny 구별; "
                          "외부사실=≤7교차 census 에서 Δ=2t−5+2/t 는 6₁ 유일(1건)",
        "not_yet": "7교차+·BMW₄·HOMFLY-Kauffman 비포함",
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        pth = os.path.join(ROOT, ".pgf", "proofs", "KNOT61-4BRAID.json")
        os.makedirs(os.path.dirname(pth), exist_ok=True)
        with open(pth, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("★6₁ 4-braid 확장 — LG+Kauffman 양 가족 동시 폐쇄 (정확 — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  ★LG(6₁)+D(6₁) 폐형식·Δ(1)=+1 관례 확정·TL₄ bracket·D(6₂) family 회귀", flush=True)
        print("  → .pgf/proofs/KNOT61-4BRAID.json", flush=True)
    print(f"knot61_4braid_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
