#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""links_gould_observe — TrackHE19 P6 Stage 2: ★**Links-Gould LG^{2,1} 2변수 초대수 불변량** —
U_q(sl(2|1)) 4-dim typical 표현(자유 파라미터 p=q^α)·**16×16 super-braiding 완전 자체유도** (관측, seal 아님).

[[superalg_alexander_observe]](Stage 1, gl(1|1) Alexander) 파이프라인 위 첫 **2변수** 초대수 층:
  - 표현 자체유도: V(α) 가중치 {Λ,Λ−α₂,Λ−α₁−α₂,Λ−α₁−2α₂}·패리티 (0,1,1,0)·계수 c₁=[α]·c₂=1·
    c₄=[α+1] — 정의 관계식 12종(Cartan·(anti)commutator·E₂²=F₂²=0·q-Serre) **전수 심볼릭**.
  - ★**braiding 자체유도**(문헌 R-행렬 인용 0): graded 코곱 Δ(★super 부호=둘째 인자 패리티)·
    Δ(U)-commutant 를 가중치 블록 36 미지수 선형계로 풀어 **dim 3**(V⊗V=4⊕8⊕4 정합) →
    고유값 (1,−p²,p⁴q²) 지정으로 č 유일 → **charpoly=(Y−1)⁴(Y+p²)⁸(Y−p⁴q²)⁴ 심볼릭** +
    ★**YBE 심볼릭 전수**(64×64 희소 다항). 고유값 자체는 유리점 YBE 해(자명·역 제외 유일)로 선판정.
  - μ 게이지 기계확정: μ̃=(p²,−p²,−p²q²,p²q²)=K₂²·(−1)^F — ptr₂((1⊗μ̃)č^{±1})=p^{±2}·I 심볼릭·
    f₊f₋=1(Markov 안정화 양방향)·유일성(점 선형해=1-계수 족). sdim V=0 재발 ⟹ (1,1)-tangle 필수(Stage 1 함정).

관측 축(정확·유리 다점→텐서곱 보간 폐형식):
  A. **LG(a,z) 폐형식 5매듭**(4₁·5₁·5₂·6₂·6₃) — 정수계수 Laurent in (q²,p²), 예: LG(4₁)=
     p⁴q²−3p²q²−3p²+2q²+7+2q⁻²−3p⁻²−3p⁻²q⁻²+p⁻⁴q⁻². 격자보간+각 축 여분점 검증.
  B. ★**변수 사전 기계확정**: t₀=p², t₁=p⁻²q⁻² ⟹ **t₀↔t₁ 대칭**((q,p)→(q,1/(pq))) 5매듭 전수.
  C. ★**Alexander² 특수화**: q=1(t₀t₁=1) ⟹ LG=Δ(p²)² — Stage 1 자체확정 Δ와 5매듭 전수 일치.
  D. ★**Alexander 특수화(1제곱)**: q=i(t₀t₁=−1) ⟹ LG=Δ(p⁴) — 5매듭 전수.
  E. **det² 게이트**: q=1,p=i ⟹ LG=det² {25,25,49,121,169}.
  F. ★**chirality 판별**: mirror(q,p)→(1/q,1/p) 불변 ⟺ amphichiral — 4₁·6₃ 만 대칭(5₁·5₂·6₂ 검출).
  G. Markov/불변성 teeth: unknot(σ^{±1} 2-braid)=1 심볼릭·split unlink=0·순환어·거울어(4₁)·
     2-braid↔안정화 3-braid(5₁)·음성대조(μ̃ 부호 제거→스칼라성 붕괴·고유값 부호 오류→YBE 붕괴).

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - Alexander 특수화 궤적 p²q=±1 에서 **표현 자체가 atypical 퇴화**(4+8+1) — 특수화는 폐형식
    수준 항등식(q=1/q=i 대입)으로 검증(직접 유리점 평가 불가 궤적).
  - 표준 문헌 (t₀,t₁) 좌표와의 사전은 **게이트로 기계확정한 자체 사전** — 문헌 LG 표 인용 0.
  - 6₁(braid index 4)·7교차+·범주 동치·전 매듭 일반성 무주장.

사용: python -m qf_witness.observe.links_gould_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import itertools
from fractions import Fraction as Fr

import sympy as sp

q, p = sp.symbols("q p")
t = sp.symbols("t")
PAR = [0, 1, 1, 0]

# Stage 1 자체확정 Alexander(문헌 인용 0) — C/D 게이트 기준값
DEL = {"4_1": -t + 3 - 1/t, "5_2": 2*t - 3 + 2/t,
       "6_2": -t**2 + 3*t - 3 + 3/t - 1/t**2, "6_3": t**2 - 3*t + 5 - 3/t + 1/t**2,
       "5_1": t**2 - t + 1 - 1/t + 1/t**2}
DET = {"4_1": 5, "5_2": 7, "6_2": 11, "6_3": 13, "5_1": 5}
WORDS = {
    "4_1": [(1, 1), (-1, 2), (1, 1), (-1, 2)],
    "5_2": [(1, 1), (-1, 2), (-1, 1), (-1, 1), (-1, 1), (-1, 2)],
    "6_2": [(1, 1), (1, 1), (1, 1), (-1, 2), (1, 1), (-1, 2)],
    "6_3": [(1, 1), (1, 1), (-1, 2), (1, 1), (-1, 2), (-1, 2)],
}
QS = [Fr(a, b) for a, b in [(2, 1), (3, 1), (5, 2), (7, 2), (5, 3), (7, 3), (9, 4), (11, 4),
                            (4, 1), (5, 1), (11, 5), (13, 5)]]
PS = [Fr(a, b) for a, b in [(3, 2), (5, 2), (7, 2), (5, 3), (7, 4), (9, 4), (11, 5), (13, 5),
                            (8, 3), (11, 3), (12, 5), (13, 4), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1)]]


def rep():
    c1 = (p - 1/p)/(q - 1/q)
    c4 = (p*q - 1/(p*q))/(q - 1/q)
    Z = sp.zeros(4, 4)
    K1 = sp.diag(1, q, 1/q, 1)
    K2 = sp.diag(p, p, p*q, p*q)
    E1 = Z.copy(); E1[1, 2] = 1
    F1 = Z.copy(); F1[2, 1] = 1
    E2 = Z.copy(); E2[0, 1] = c1; E2[2, 3] = c4
    F2 = Z.copy(); F2[1, 0] = 1; F2[3, 2] = 1
    return K1, K2, E1, F1, E2, F2


def gkron(A, B, pb):
    """graded (a⊗b): 부호 (−1)^{|B|·|v_i|}, pb=둘째 인자 연산자 패리티"""
    M = sp.zeros(16, 16)
    for k in range(4):
        for i in range(4):
            if A[k, i] != 0:
                sgn = (-1)**(pb*PAR[i])
                for l in range(4):
                    for j in range(4):
                        if B[l, j] != 0:
                            M[4*k + l, 4*i + j] = sgn*A[k, i]*B[l, j]
    return M


def simp0(M):
    return all(sp.cancel(sp.together(x)) == 0 for x in M)


def fr(x):
    return Fr(int(sp.numer(x)), int(sp.denom(x)))


def sp_mul(A, B):
    """sparse dict-of-dict product (심볼릭/유리 공용)"""
    out = {}
    for i, ra in A.items():
        acc = {}
        for k, v in ra.items():
            rb = B.get(k)
            if rb:
                for j, w in rb.items():
                    acc[j] = acc.get(j, 0) + v*w
        row = {}
        for j, x in acc.items():
            xe = sp.expand(x) if not isinstance(x, Fr) else x
            if xe != 0:
                row[j] = xe
        if row:
            out[i] = row
    return out


def emb3(nz, which):
    """16×16 nonzero 목록 → 3가닥 64×64 sparse (which=1: C⊗I, 2: I⊗C)"""
    d = {}
    for i, j, v in nz:
        if which == 1:
            for k in range(4):
                d.setdefault(4*i + k, {})[4*j + k] = v
        else:
            for k in range(4):
                d.setdefault(16*k + i, {})[16*k + j] = v
    return d


def sp_eq(A, B):
    for i in set(A) | set(B):
        ra, rb = A.get(i, {}), B.get(i, {})
        for j in set(ra) | set(rb):
            if sp.simplify(ra.get(j, 0) - rb.get(j, 0)) != 0:
                return False
    return True


def derive():
    """표현→관계식→Δ→commutant→č→charpoly→YBE→μ̃ 전부 자체유도. returns (R, C, Ci, nzC, nzCi)"""
    R = {}
    K1, K2, E1, F1, E2, F2 = rep()
    Z = sp.zeros(4, 4)
    two = q + 1/q
    rel = {
        "K1E1": K1*E1*K1.inv() - q**2*E1, "K1E2": K1*E2*K1.inv() - E2/q,
        "K2E1": K2*E1*K2.inv() - E1/q, "K2E2": K2*E2*K2.inv() - E2,
        "EF1": E1*F1 - F1*E1 - (K1 - K1.inv())/(q - 1/q),
        "EF2": E2*F2 + F2*E2 - (K2 - K2.inv())/(q - 1/q),
        "E2sq": E2*E2, "F2sq": F2*F2,
        "E1F2": E1*F2 - F2*E1, "E2F1": E2*F1 - F1*E2,
        "SerreE": E1*E1*E2 - two*E1*E2*E1 + E2*E1*E1,
        "SerreF": F1*F1*F2 - two*F1*F2*F1 + F2*F1*F1,
    }
    R["A_relations_12"] = all(simp0(M) for M in rel.values())

    I4 = sp.eye(4)
    DE1 = gkron(E1, I4, 0) + gkron(K1, E1, 0)
    DF1 = gkron(F1, K1.inv(), 0) + gkron(I4, F1, 0)
    DE2 = gkron(E2, I4, 0) + gkron(K2, E2, 1)
    DF2 = gkron(F2, K2.inv(), 0) + gkron(I4, F2, 1)
    DK2 = gkron(K2, K2, 0)
    R["A_coproduct_hom"] = simp0(DE2*DF2 + DF2*DE2 - (DK2 - DK2.inv())/(q - 1/q)) \
        and simp0(DE2*DE2) and simp0(DE1*DF2 - DF2*DE1)

    # commutant: 가중치 블록 미지수
    h1 = [0, 1, -1, 0]; h2 = [0, 0, 1, 1]
    wt = {}
    for i in range(4):
        for j in range(4):
            wt.setdefault((h1[i] + h1[j], h2[i] + h2[j]), []).append(4*i + j)
    unk = {}
    syms = []
    for idxs in wt.values():
        for a in idxs:
            for b in idxs:
                s = sp.Symbol(f"x_{a}_{b}")
                unk[(a, b)] = s
                syms.append(s)
    X = sp.zeros(16, 16)
    for (a, b), s in unk.items():
        X[a, b] = s
    eqs = []
    for M in (DE1, DE2, DF1, DF2):
        D = X*M - M*X
        eqs += [sp.together(D[i, j]) for i in range(16) for j in range(16) if D[i, j] != 0]
    sol = sp.solve(eqs, syms, dict=True)
    s0 = sol[0]
    free = [s for s in syms if s not in s0]
    R["B_commutant_dim3"] = (len(free) == 3)
    Xg = X.subs(s0)

    # 고유값 지정: hw 벡터 3개에서 (1,−p²,p⁴q²)
    e0 = sp.zeros(16, 1); e0[0] = 1
    lam0 = (Xg*e0)[0]
    a_, b_ = sp.symbols("a_ b_")
    w = sp.zeros(16, 1); w[1] = a_; w[4] = b_
    cnd = DE2*w
    sab = sp.solve([sp.together(cnd[i]) for i in range(16) if cnd[i] != 0], [a_, b_], dict=True)
    w1 = w.subs(sab[0]).subs({a_: 1, b_: 1})
    sup1 = [i for i in range(16) if w1[i] != 0][0]
    lam1 = sp.cancel((Xg*w1)[sup1]/w1[sup1])
    cs = sp.symbols("ca_ cb_ cc_ cd_")
    w2 = sp.zeros(16, 1)
    for s, idx in zip(cs, (3, 6, 9, 12)):
        w2[idx] = s
    conds = []
    for M in (DE1, DE2):
        r2 = M*w2
        conds += [sp.together(r2[i]) for i in range(16) if r2[i] != 0]
    s2s = sp.solve(conds, list(cs), dict=True)
    w2s = w2.subs(s2s[0])
    freec = [s for s in cs if s not in s2s[0]]
    w2s = w2s.subs({freec[0]: 1})
    sup2 = [i for i in range(16) if w2s[i] != 0][0]
    lam2 = sp.cancel((Xg*w2s)[sup2]/w2s[sup2])
    fsol = sp.solve([sp.together(lam0 - 1), sp.together(lam1 + p**2),
                     sp.together(lam2 - p**4*q**2)], free, dict=True)
    R["B_eigen_assign_unique"] = (len(fsol) == 1)
    C = sp.Matrix([[sp.cancel(sp.together(x)) for x in Xg.subs(fsol[0]).row(i)] for i in range(16)])
    cp = sp.factor(C.charpoly(sp.Symbol("Y")).as_expr())
    Y = sp.Symbol("Y")
    R["B_charpoly_4_8_4"] = sp.simplify(
        cp - sp.expand((Y - 1)**4*(Y + p**2)**8*(Y - p**4*q**2)**4)*sp.sign(1)) == 0 \
        or sp.simplify(cp + sp.expand(-(Y - 1)**4*(Y + p**2)**8*(Y - p**4*q**2)**4)) == 0
    # C^{-1}: 최소다항식 (Y−1)(Y+p²)(Y−p⁴q²)
    ee = 1 - p**2 + p**4*q**2
    ff = -p**2 + p**4*q**2 - p**6*q**2
    gg = -p**6*q**2
    Ci = sp.Matrix([[sp.cancel(sp.together(x)) for x in ((C*C - ee*C + ff*sp.eye(16))/gg).row(i)]
                    for i in range(16)])
    R["B_inverse_exact"] = simp0(C*Ci - sp.eye(16))

    nzC = [(i, j, C[i, j]) for i in range(16) for j in range(16) if C[i, j] != 0]
    nzCi = [(i, j, Ci[i, j]) for i in range(16) for j in range(16) if Ci[i, j] != 0]
    s1 = emb3(nzC, 1); s2 = emb3(nzC, 2)
    R["B_YBE_symbolic"] = sp_eq(sp_mul(sp_mul(s1, s2), s1), sp_mul(sp_mul(s2, s1), s2))

    # μ̃ 심볼릭 게이트 + 점 유일성
    MU = [p**2, -p**2, -p**2*q**2, p**2*q**2]
    for M, fexp, key in ((C, p**2, "C_mu_markov_plus"), (Ci, 1/p**2, "C_mu_markov_minus")):
        P = sp.zeros(4, 4)
        for i in range(4):
            for j in range(4):
                P[i, j] = sum(MU[k]*M[4*i + k, 4*j + k] for k in range(4))
        R[key] = simp0(P - fexp*sp.eye(4))
    R["C_fpfm_1"] = True  # p²·p⁻² = 1 (구성적)
    m = sp.symbols("m0 m1 m2 m3")
    pt = {q: sp.Rational(3, 5), p: sp.Rational(7, 4)}
    eqs2 = []
    for M in (C.subs(pt), Ci.subs(pt)):
        P = [[sum(m[k]*M[4*i + k, 4*j + k] for k in range(4)) for j in range(4)] for i in range(4)]
        eqs2 += [P[i][j] for i in range(4) for j in range(4) if i != j]
        eqs2 += [P[i][i] - P[0][0] for i in range(1, 4)]
    msol = sp.solve(eqs2, m, dict=True)
    R["C_mu_unique_ray"] = (len(msol) == 1 and sum(1 for v in m if v not in msol[0]) == 1)
    return R, C, Ci, nzC, nzCi


def matvec(rows, x):
    out = {}
    for j, v in x.items():
        pass
    # row-oriented
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


class Engine:
    def __init__(self, nzC, nzCi):
        self.nzC = nzC; self.nzCi = nzCi
        self.cache = {}

    def gens(self, qv, pv):
        key = (qv, pv)
        if key not in self.cache:
            sub = {q: sp.Rational(qv), p: sp.Rational(pv)}
            def ev(nz):
                return [(i, j, fr(v.subs(sub))) for i, j, v in nz]
            eC = [(i, j, v) for i, j, v in ev(self.nzC) if v != 0]
            eCi = [(i, j, v) for i, j, v in ev(self.nzCi) if v != 0]
            self.cache[key] = {(1, 1): emb3(eC, 1), (-1, 1): emb3(eCi, 1),
                               (1, 2): emb3(eC, 2), (-1, 2): emb3(eCi, 2),
                               "C": eC, "Ci": eCi,
                               "mu": [fr(x.subs(sub)) for x in (p**2, -p**2, -p**2*q**2, p**2*q**2)],
                               "fp": fr((p**2).subs(sub))}
        return self.cache[key]

    def lg3(self, word, qv, pv, scal_check=False):
        g = self.gens(qv, pv)
        muf, fpf = g["mu"], g["fp"]
        e = sum(s for s, _ in word)
        vals = {}
        jr = range(2) if scal_check else range(1)
        for j in jr:
            for k in range(4):
                for l in range(4):
                    x = {16*j + 4*k + l: Fr(1)}
                    for gw in reversed(word):
                        x = matvec(g[gw], x)
                    w = muf[k]*muf[l]
                    for i in (range(2) if scal_check else (j,)):
                        v = x.get(16*i + 4*k + l)
                        if v is not None:
                            vals[(i, j)] = vals.get((i, j), Fr(0)) + w*v
        val = vals.get((0, 0), Fr(0))*fpf**(-e)
        if scal_check:
            ok = vals.get((0, 1), Fr(0)) == 0 and vals.get((1, 0), Fr(0)) == 0 \
                and vals.get((0, 0), Fr(0)) == vals.get((1, 1), Fr(0))
            return val, ok
        return val

    def lg2(self, npow, qv, pv):
        g = self.gens(qv, pv)
        rows = {}
        for i, j, v in (g["C"] if npow >= 0 else g["Ci"]):
            rows.setdefault(i, {})[j] = v
        muf, fpf = g["mu"], g["fp"]
        T00 = Fr(0)
        for k in range(4):
            x = {k: Fr(1)}
            for _ in range(abs(npow)):
                x = matvec(rows, x)
            v = x.get(k)
            if v is not None:
                T00 += muf[k]*v
        return T00*fpf**(-npow)


def vand_solve(xs, ys, lo, hi):
    n = hi - lo + 1
    A = [[xs[i]**(lo + k) for k in range(n)] for i in range(n)]
    c = [Fr(x) for x in ys]
    for col in range(n):
        piv = next(r for r in range(col, n) if A[r][col] != 0)
        A[col], A[piv] = A[piv], A[col]
        c[col], c[piv] = c[piv], c[col]
        inv = 1/A[col][col]
        A[col] = [v*inv for v in A[col]]
        c[col] = c[col]*inv
        for r in range(n):
            if r != col and A[r][col] != 0:
                f2 = A[r][col]
                A[r] = [x - f2*y for x, y in zip(A[r], A[col])]
                c[r] = c[r] - f2*c[col]
    return c


def reconstruct(getval, alo, ahi, blo, bhi):
    """LG = Σ c_ab q^{2a} p^{2b}; 텐서곱 보간 + 각 축 여분점 정확 검증"""
    na, nb = ahi - alo + 1, bhi - blo + 1
    qs, ps = QS[:na + 1], PS[:nb + 1]
    V = {(qv, pv): Fr(getval(qv, pv)) for qv in qs for pv in ps}
    cb = {}
    for qv in qs:
        c = vand_solve([pv**2 for pv in ps[:nb]], [V[(qv, pv)] for pv in ps[:nb]], blo, bhi)
        pv = ps[nb]
        if sum(c[k]*(pv**2)**(blo + k) for k in range(nb)) != V[(qv, pv)]:
            return None, False
        cb[qv] = c
    coef = {}
    for k in range(nb):
        c2 = vand_solve([qv**2 for qv in qs[:na]], [cb[qv][k] for qv in qs[:na]], alo, ahi)
        qv = qs[na]
        if sum(c2[mm]*(qv**2)**(alo + mm) for mm in range(na)) != cb[qv][k]:
            return None, False
        for mm in range(na):
            if c2[mm] != 0:
                coef[(alo + mm, blo + k)] = c2[mm]
    poly = sum(sp.Rational(v)*q**(2*a)*p**(2*b) for (a, b), v in coef.items())
    intc = all(v.denominator == 1 for v in coef.values())
    return sp.expand(poly), intc


def main():
    quick = "--quick" in sys.argv
    out = {"_schema": "links-gould/v1",
           "_note": ("★첫 2변수 초대수 불변량 — U_q(sl(2|1)) 4-dim typical·braiding 완전 자체유도"
                     "(commutant+YBE 심볼릭)·LG 폐형식 5매듭·사전 t₀=p²,t₁=p⁻²q⁻² 기계확정·"
                     "Alexander²(q=1)/Alexander(q=i) 특수화·chirality 판별. 관측·module 0·root 불변.")}
    R, C, Ci, nzC, nzCi = derive()
    eng = Engine(nzC, nzCi)

    # G: unknot/split/불변성 teeth
    MU = [p**2, -p**2, -p**2*q**2, p**2*q**2]
    for npw, key, expect in ((1, "G_unknot_w1", 1), (-1, "G_unknot_wm1", 1)):
        M = C if npw > 0 else Ci
        T00 = sum(MU[k]*M[4*0 + k, 4*0 + k] for k in range(4))
        R[key] = sp.simplify(T00*(p**2)**(-npw) - expect) == 0
    T00 = sum(MU[k]*sp.eye(16)[4*0 + k, 4*0 + k] for k in range(4))
    R["G_split_unlink_zero"] = sp.simplify(T00) == 0     # σ⁰ 폐합 = 2-성분 unlink, sdim=0
    qv, pv = Fr(3, 5), Fr(7, 4)
    v41, sc41 = eng.lg3(WORDS["4_1"], qv, pv, scal_check=True)
    R["G_11tangle_scalar"] = sc41
    R["G_cyclic_word"] = (eng.lg3([(-1, 2), (1, 1), (-1, 2), (1, 1)], qv, pv) == v41)
    R["G_41_mirror_word_eq"] = (eng.lg3([(-1, 1), (1, 2), (-1, 1), (1, 2)], qv, pv) == v41)
    R["G_51_markov_stab"] = (eng.lg2(5, qv, pv) == eng.lg3([(1, 1)]*5 + [(1, 2)], qv, pv))
    # 음성대조: μ̃ 부호 제거 → 스칼라성 붕괴 / λ₁ 부호 오류 → YBE 점 붕괴
    sub = {q: sp.Rational(qv), p: sp.Rational(pv)}
    Mn = C.subs(sub)
    mu_bad = [abs(fr(x.subs(sub))) for x in MU]
    Pb = [[sum(mu_bad[k]*Mn[4*i + k, 4*j + k] for k in range(4)) for j in range(4)] for i in range(4)]
    R["teeth_mu_sign"] = not all(Pb[i][i] == Pb[0][0] for i in range(4))
    Cw = Mn + sp.Rational(2)*sp.Rational(pv)**2*sp.eye(16)  # 고유값 이동(λ₁ −p²→+p²) 유사 교란
    nzW = [(i, j, fr(Cw[i, j])) for i in range(16) for j in range(16) if Cw[i, j] != 0]
    w1, w2m = emb3(nzW, 1), emb3(nzW, 2)
    R["teeth_eigen_perturb"] = not sp_eq(sp_mul(sp_mul(w1, w2m), w1), sp_mul(sp_mul(w2m, w1), w2m))

    # A: 폐형식 재구성
    specs = {"4_1": (lambda a, b: eng.lg3(WORDS["4_1"], a, b), -1, 1, -2, 2),
             "5_1": (lambda a, b: eng.lg2(5, a, b), -5, 5, -7, 7)}
    if not quick:
        for nm in ("5_2", "6_2", "6_3"):
            specs[nm] = (lambda a, b, w=WORDS[nm]: eng.lg3(w, a, b), -3, 3, -5, 5)
    polys = {}
    for name, (gv, alo, ahi, blo, bhi) in specs.items():
        P, intc = reconstruct(gv, alo, ahi, blo, bhi)
        polys[name] = P
        R[f"{name}_recon"] = P is not None
        R[f"{name}_int_coeffs"] = intc
        out[f"LG_{name}"] = str(P)

    # B~F: 폐형식 게이트
    amphi_expect = {"4_1": True, "6_3": True, "5_1": False, "5_2": False, "6_2": False}
    for name, P in polys.items():
        if P is None:
            continue
        sw = sp.expand(sp.cancel(P.subs({p: 1/(p*q)}, simultaneous=True)))
        R[f"{name}_t0t1_sym"] = sp.simplify(P - sw) == 0
        R[f"{name}_alex2_q1"] = sp.simplify(
            sp.expand(P.subs(q, 1)) - sp.expand(DEL[name].subs(t, p**2)**2)) == 0
        R[f"{name}_alex_qi"] = sp.simplify(
            sp.expand(P.subs(q, sp.I)) - sp.expand(DEL[name].subs(t, p**4))) == 0
        R[f"{name}_det2"] = sp.simplify(P.subs({q: 1, p: sp.I}, simultaneous=True) - DET[name]**2) == 0
        Pm = sp.expand(P.subs({q: 1/q, p: 1/p}, simultaneous=True))
        R[f"{name}_chirality"] = ((sp.simplify(P - Pm) == 0) == amphi_expect[name])
    # teeth: Alexander² 게이트 이빨(잘못된 t=p⁴ 대입은 불일치해야)
    if polys.get("4_1") is not None:
        R["teeth_alex_wrong_t"] = sp.simplify(
            sp.expand(polys["4_1"].subs(q, 1)) - sp.expand(DEL["4_1"].subs(t, p**4)**2)) != 0

    ok = bool(all(R.values()))
    out["checks"] = R
    out["scope_honesty"] = {
        "delivered": "★첫 2변수 초대수 층 — braiding 완전 자체유도(YBE 심볼릭)·LG 폐형식 "
                     + ("2매듭(quick)" if quick else "5매듭")
                     + "·Alexander²/Alexander 이중 특수화·chirality 판별·변수 사전 기계확정",
        "not_yet": "6₁(braid index 4)·7교차+·비-typical(atypical 궤적 표현 퇴화 4+8+1)·범주 동치 무주장",
        "gauge": "μ̃=K₂²·(−1)^F=(p²,−p²,−p²q²,p²q²)·f₊=p²·č 고유값 (1,−p²,p⁴q²) — 기계확정",
        "dictionary": "t₀=p², t₁=p⁻²q⁻² (t₀↔t₁ 대칭·q=1 ⟺ t₀t₁=1 Alexander²·q=i ⟺ t₀t₁=−1 Alexander)",
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        pth = os.path.join(ROOT, ".pgf", "proofs", "LINKS-GOULD.json")
        os.makedirs(os.path.dirname(pth), exist_ok=True)
        with open(pth, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("★Links-Gould LG^{2,1} 2변수 초대수 불변량 (정확 — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  ★braiding 자체유도(commutant dim3+YBE 심볼릭)·LG 폐형식 5매듭", flush=True)
        print("  ★Alexander²(q=1)/Alexander(q=i)·det²·chirality 판별·t₀↔t₁ 대칭", flush=True)
        print("  → .pgf/proofs/LINKS-GOULD.json", flush=True)
    print(f"links_gould_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
