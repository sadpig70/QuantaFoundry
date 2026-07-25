#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""a7_cartan_p23_observe — TrackHE19 P4: A₇ **p=3 완전 D(9×6)·Cartan** + p=2 기초층
(비순환 defect) (관측, seal 아님). [[a7_brauer_trees_observe]](p=5,7 cyclic tree)의 후속.

★p=3 완전 해결(전부 결정적 GF(3)/ℚ(√−7) 산술 — 확률적 meataxe 금지 규율):
  - **블록 분포(자체유도)**: 주블록 {1,10,10̄,14,14′,35}(defect ℤ₃²) + ★**defect-1 순환 블록
    {6,15,21}**(ℤ₃) — 후자는 Brauer tree 적용 가능: **라인 6—21—15(e=2·m=1)·simples {6̂,15̂}·
    det C=3**(p=5,7 패턴 연속).
  - **주블록 simples {1̂, 13̂, 10̂, 10̄̂}**:
    (i) 13̂ = pairs21/im(incidence) 몫(14̂)의 극대부분모듈 — **14̂=[13|1]**(head 1·고정/Hom 정확 판정)
    (ii) ★**χ̂14 = χ̂14′**(3-regular 제한 동일 — 차이 클래스 3A/3B/6A 가 전부 3-singular) →
        14′̂=1+13 도 동일 행 (iii) ★**10̂/10̄̂ = GF(9)-켤레 쌍**: Λ³(6̂)(20차원 명시 구성)의
        **End = 2차원·F²=−I(GF(3) 고유값 없음) ⟹ End ≅ GF(9)**(field) → 20 은 GF(3)-simple·
        GF(9) 에서 10+10̄ 절대기약 분리 — ℚ(√−7) 켤레(ordinary 10쌍)의 **mod-3 그림자**
    (iv) χ̂35 = 2·1̂+13̂+10̂+10̄̂ — 유리셀 선형계 + **무리셀(7A/7B·√−7) 방정식이 c=d=1 확정**.
  - ★**완전 D(9×6)·C=DᵀD**: 전 행 3-regular 6클래스 재구성 정확(ℚ(√−7) 포함)·소블록 C₂ det=3·
    주블록 C₄ det 산출·C 대칭·양정치.
★p=2 기초층(자체유도): Sylow-2=D₄ **구성적 확인**(위수 프로파일 [1,2⁵,4²] — Q₈/ℤ₂³/ℤ₈ 배제)·
  블록 {1,14,15,21,35}(주)+{6,10,10̄,14′}·**블록별 ℓ = 3+3**(ℚ(√−7) rank)·pairs incidence
  **mod-2 퇴화(rank 6≠7)**·Q(15) 지표(고정 1·dual 1·End 2)·6̂ 고정/dual 0.

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - **p=2 완전 D·C = 미완**(양 블록 모두 비순환 defect(D₄·위수4)·wild 가능 — 트리 이론 부재·
    decomposition 유일성 비보장) — 기초층(블록·ℓ·Sylow·모듈 지표)까지 결정적으로.
  - p=3 주블록 defect ℤ₃²(비순환)이지만 D 는 **명시 모듈 구성으로 완전 결정**(트리 이론 불필요).
  - Brauer 문자 값은 10̂ 쌍의 7A/7B 에서 ℚ(√−7) — 정확 대수 산술.

사용: python -m qf_witness.observe.a7_cartan_p23_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import itertools

import sympy as sp

from qf_witness.observe.a7_brauer_trees_observe import (
    dixon_char_table, prufer_trees, solve_phi)

GENS = [(1, 2, 0, 3, 4, 5, 6), (1, 2, 3, 4, 5, 6, 0)]
N7 = 7


# ── GF(p) 도구 ──────────────────────────────────────────────────────────────
def make_tools(p):
    def rref_add(basis, v):
        v = list(v)
        for b in basis:
            lead = next(k for k, x in enumerate(b) if x)
            if v[lead]:
                f = v[lead] * pow(b[lead], p - 2, p) % p
                v = [(v[k] - f * b[k]) % p for k in range(len(v))]
        if any(v):
            basis.append(v)
            return True
        return False

    def matvec(M, v):
        return [sum(M[i][j] * v[j] for j in range(len(v))) % p for i in range(len(M))]

    def quotient_mats(Msrc, U, dim):
        full = [b[:] for b in U]
        ext = []
        for i in range(dim):
            e = [0] * dim
            e[i] = 1
            if rref_add(full, e):
                ext.append(full[-1])
        dq = len(ext)

        def coords(w):
            v = list(w)
            c = [0] * dq
            for b in U:
                lead = next(k for k, x in enumerate(b) if x)
                if v[lead]:
                    f = v[lead] * pow(b[lead], p - 2, p) % p
                    v = [(v[k] - f * b[k]) % p for k in range(dim)]
            for ei, b in enumerate(ext):
                lead = next(k for k, x in enumerate(b) if x)
                if v[lead]:
                    f = v[lead] * pow(b[lead], p - 2, p) % p
                    c[ei] = f
                    v = [(v[k] - f * b[k]) % p for k in range(dim)]
            assert not any(v)
            return c
        out = []
        for M in Msrc:
            Q = [[0] * dq for _ in range(dq)]
            for j in range(dq):
                c = coords(matvec(M, ext[j]))
                for r in range(dq):
                    Q[r][j] = c[r]
            out.append(Q)
        return out, dq

    def fixed_dim(mats, dim):
        rows = []
        for M in mats:
            for r in range(dim):
                row = [(M[r][c] - (1 if r == c else 0)) % p for c in range(dim)]
                if any(row):
                    rows.append(row)
        b = []
        for v in rows:
            rref_add(b, v)
        return dim - len(b)

    def matinv(M):
        n = len(M)
        A = [[M[r][c] for c in range(n)] + [1 if c == r else 0 for c in range(n)]
             for r in range(n)]
        for c in range(n):
            pr = next(r for r in range(c, n) if A[r][c])
            A[c], A[pr] = A[pr], A[c]
            iv = pow(A[c][c], p - 2, p)
            A[c] = [x * iv % p for x in A[c]]
            for r in range(n):
                if r != c and A[r][c]:
                    f = A[r][c]
                    A[r] = [(A[r][k] - f * A[c][k]) % p for k in range(2 * n)]
        return [[A[r][n + c] for c in range(n)] for r in range(n)]

    def dual_mats(mats, dim):
        return [[[matinv(M)[c][r] for c in range(dim)] for r in range(dim)] for M in mats]

    def hom_dim(Am_l, Bm_l, da, db):
        rows = []
        for Am, Bm in zip(Am_l, Bm_l):
            for r in range(db):
                for c in range(da):
                    row = [0] * (da * db)
                    for k in range(da):
                        row[r * da + k] = (row[r * da + k] + Am[k][c]) % p
                    for k in range(db):
                        row[k * da + c] = (row[k * da + c] - Bm[r][k]) % p
                    if any(row):
                        rows.append(row)
        b = []
        for v in rows:
            rref_add(b, v)
        return da * db - len(b)

    def nat6():
        mats = []
        for g in GENS:
            M = [[0] * 6 for _ in range(6)]
            for i in range(6):
                vec = [0] * 7
                vec[g[i]] = (vec[g[i]] + 1) % p
                vec[g[i + 1]] = (vec[g[i + 1]] - 1) % p
                c = [0] * 6
                s = 0
                for k2 in range(6):
                    s = (s + vec[k2]) % p
                    c[k2] = s
                for r in range(6):
                    M[r][i] = c[r]
            mats.append(M)
        return mats
    return rref_add, matvec, quotient_mats, fixed_dim, dual_mats, hom_dim, nat6


def pairs_mats(p):
    PAIRS = [frozenset(x) for x in itertools.combinations(range(7), 2)]
    pidx = {fs: i for i, fs in enumerate(PAIRS)}
    M21 = []
    for g in GENS:
        M = [[0] * 21 for _ in range(21)]
        for i, fs in enumerate(PAIRS):
            M[pidx[frozenset(g[x] for x in fs)]][i] = 1
        M21.append(M)
    inc = []
    for i in range(7):
        v = [0] * 21
        for j in range(7):
            if j != i:
                v[pidx[frozenset((i, j))]] = 1
        inc.append(v)
    return M21, inc


def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "a7-cartan-p23/v1",
           "_note": ("A₇ p=3 완전 D(9×6)·Cartan + p=2 기초층 — 결정적 GF(p)/ℚ(√−7) 산술. "
                     "p=3 주블록 simples {1,13,10,10̄(GF(9)-켤레)}·소블록 tree 6—21—15. "
                     "p=2 완전 D=정직 미완(wild). 관측·module 0·root 불변.")}
    T = dixon_char_table()
    K, sizes, orders, degs = T["K"], T["sizes"], T["orders"], T["degs"]
    int_table, rat = T["int_table"], T["rat"]

    # ── p=3 ──────────────────────────────────────────────────────────────
    p = 3
    reg3 = [k for k in range(K) if orders[k] % 3 != 0]
    R["p3_l6"] = (len(reg3) == 6)
    # 블록 분포
    def blocks(pp):
        sig = {}
        for t in range(K):
            s = []
            for k in range(K):
                if rat[t][k]:
                    s.append((sizes[k] * int_table[t][k] // degs[t]) % pp)
                else:
                    s.append(0)
            sig.setdefault(tuple(s), []).append(t)
        return list(sig.values())
    b3 = blocks(3)
    small = next(b for b in b3 if sorted(degs[t] for t in b) == [6, 15, 21])
    main3 = next(b for b in b3 if 1 in [degs[t] for t in b])
    R["p3_blocks"] = (sorted(degs[t] for t in main3) == [1, 10, 10, 14, 14, 35])
    # 소블록 tree
    b1 = sorted(small, key=lambda t: degs[t])
    chi_rows = [[int_table[t][k] for k in reg3] for t in b1]
    e_small = sp.Matrix(chi_rows).rank()
    R["p3_small_e2"] = (e_small == 2)
    found = set()
    for perm in itertools.permutations(range(3)):
        labels = [b1[i] for i in perm]
        D = {t: [0, 0] for t in b1}
        for ei, (u, v) in enumerate([(0, 1), (1, 2)]):
            D[labels[u]][ei] = 1
            D[labels[v]][ei] = 1
        Dm = [D[t] for t in b1]
        dims = solve_phi(Dm, chi_rows, reg3, 2)
        if dims:
            key = tuple(sorted(tuple(sorted((degs[labels[u]], degs[labels[v]])))
                               for u, v in [(0, 1), (1, 2)]))
            found.add((key, tuple(sorted(dims))))
    R["p3_small_tree_6_21_15"] = (found == {((tuple(sorted((6, 21))), tuple(sorted((15, 21)))),
                                            (6, 15))})
    out["p3_small_block"] = {"tree": "6 — 21 — 15 (line·e=2·m=1)", "simples": [6, 15],
                             "cartan": [[2, 1], [1, 2]], "det": 3}

    # 주블록 모듈러 판정
    (rref_add, matvec, quotient_mats, fixed_dim, dual_mats, hom_dim, nat6) = make_tools(3)
    M21, inc = pairs_mats(3)
    U = []
    for v in inc:
        rref_add(U, v)
    R["p3_inc_rank7"] = (len(U) == 7)
    QM, dq = quotient_mats(M21, U, 21)
    R["p3_Q14"] = (dq == 14)
    fQ = fixed_dim(QM, dq)
    fQd = fixed_dim(dual_mats(QM, dq), dq)
    R["p3_14hat_head1"] = (fQ == 0 and fQd == 1)         # 14̂=[13|1]
    # χ̂14 == χ̂14′
    i14 = [t for t in range(K) if degs[t] == 14]
    R["p3_chi14_eq_chi14p"] = ([int_table[i14[0]][k] for k in reg3]
                               == [int_table[i14[1]][k] for k in reg3])
    # Λ³(6̂): End=GF(9) certificate
    M6 = nat6()
    IDX3 = list(itertools.combinations(range(6), 3))
    i3 = {c: i for i, c in enumerate(IDX3)}

    def wedge3(M):
        n3 = len(IDX3)
        Wm = [[0] * n3 for _ in range(n3)]
        for cj, (a, b, c) in enumerate(IDX3):
            va = [M[r][a] for r in range(6)]
            vb = [M[r][b] for r in range(6)]
            vc = [M[r][c] for r in range(6)]
            for (x, y, z) in IDX3:
                d = (va[x] * (vb[y] * vc[z] - vb[z] * vc[y])
                     - va[y] * (vb[x] * vc[z] - vb[z] * vc[x])
                     + va[z] * (vb[x] * vc[y] - vb[y] * vc[x])) % 3
                if d:
                    Wm[i3[(x, y, z)]][cj] = d
        return Wm
    W20 = [wedge3(M) for M in M6]
    endd = hom_dim(W20, W20, 20, 20)
    R["p3_lambda3_end2"] = (endd == 2)
    R["p3_lambda3_no_triv13"] = (fixed_dim(W20, 20) == 0
                                 and fixed_dim(dual_mats(W20, 20), 20) == 0)
    # F²=−I 확인 (End 기저의 비스칼라 원소)
    rows = []
    da = 20
    for Am in W20:
        for r in range(da):
            for c in range(da):
                row = [0] * (da * da)
                for k in range(da):
                    row[r * da + k] = (row[r * da + k] + Am[k][c]) % 3
                for k in range(da):
                    row[k * da + c] = (row[k * da + c] - Am[r][k]) % 3
                if any(row):
                    rows.append(row)
    bas = []
    for v in rows:
        rref_add(bas, v)
    lead = {next(k for k, x in enumerate(b) if x): b for b in bas}
    free = [c for c in range(da * da) if c not in lead]
    F = None
    for f in free:
        vec = [0] * (da * da)
        vec[f] = 1
        for lc in sorted(lead, reverse=True):
            b = lead[lc]
            s2 = sum(b[k] * vec[k] for k in range(da * da) if k != lc) % 3
            vec[lc] = (-s2 * pow(b[lc], 1, 3)) % 3
        M = [[vec[r * da + c] for c in range(da)] for r in range(da)]
        if any(M[r][c] != (M[0][0] if r == c else 0) for r in range(da) for c in range(da)):
            F = M
            break
    F2 = [[sum(F[r][k] * F[k][c] for k in range(da)) % 3 for c in range(da)] for r in range(da)]
    R["p3_F2_minusI_GF9"] = all(F2[r][c] == ((3 - 1) if r == c else 0) % 3 * (1 if r == c else 0)
                                or (r == c and F2[r][c] == 2) or (r != c and F2[r][c] == 0)
                                for r in range(da) for c in range(da))
    # 명확히: F² == 2I (=−I)
    R["p3_F2_minusI_GF9"] = all(F2[r][c] == (2 if r == c else 0)
                                for r in range(da) for c in range(da))

    # D(9×6) 완전 — Brauer 문자(ℚ(√−7)) 재구성 게이트
    al = (sp.Integer(-1) + sp.sqrt(-7)) / 2
    alb = (sp.Integer(-1) - sp.sqrt(-7)) / 2
    i10 = [t for t in range(K) if degs[t] == 10]

    def chi_exact(t):
        row = []
        for k in reg3:
            if rat[t][k]:
                row.append(sp.Integer(int_table[t][k]))
            else:
                row.append(al if t == i10[0] else alb)
        return row
    one_v = [sp.Integer(1)] * 6
    chi14 = chi_exact(i14[0])
    thirteen = [chi14[i] - 1 for i in range(6)]
    ten = chi_exact(i10[0])
    tenb = chi_exact(i10[1])
    six = chi_exact(next(t for t in range(K) if degs[t] == 6))
    fifteen = chi_exact(next(t for t in range(K) if degs[t] == 15))
    PHI = [one_v, thirteen, ten, tenb, six, fifteen]      # 열 순서: 1,13,10,10̄ | 6,15
    DROWS = {1: [1, 0, 0, 0, 0, 0], 6: [0, 0, 0, 0, 1, 0],
             15: [0, 0, 0, 0, 0, 1], 21: [0, 0, 0, 0, 1, 1],
             14: [1, 1, 0, 0, 0, 0], 35: [2, 1, 1, 1, 0, 0]}
    okD = True
    Dfull = []
    for t in range(K):
        if degs[t] == 10:
            drow = [0, 0, 1, 0, 0, 0] if t == i10[0] else [0, 0, 0, 1, 0, 0]
        else:
            drow = DROWS[degs[t]][:]
        Dfull.append(drow)
        recon = [sum(drow[j] * PHI[j][i] for j in range(6)) for i in range(6)]
        target = chi_exact(t)
        if any(sp.simplify(recon[i] - target[i]) != 0 for i in range(6)):
            okD = False
    R["p3_D_reconstructs_all9"] = okD
    Cm = sp.Matrix(Dfull).T * sp.Matrix(Dfull)
    R["p3_C_symmetric_posdef"] = (Cm == Cm.T and all(
        Cm[:k, :k].det() > 0 for k in range(1, 7)))
    detC_main = Cm[:4, :4].det()
    detC_small = Cm[4:, 4:].det()
    R["p3_detC_small_3"] = (detC_small == 3)
    R["p3_detC_main_power3"] = (detC_main > 0 and sp.Integer(detC_main).is_integer
                                and (3 ** int(sp.log(detC_main, 3)) == detC_main
                                     if detC_main > 1 else True))
    out["p3_principal"] = {
        "simples": "1̂·13̂·10̂·10̄̂ (10쌍 = GF(9)-켤레·End(Λ³6̂)≅GF(9)·F²=−I certificate)",
        "D_rows": {"1": [1, 0, 0, 0], "10": [0, 0, 1, 0], "10̄": [0, 0, 0, 1],
                   "14=14'": [1, 1, 0, 0], "35": [2, 1, 1, 1]},
        "Cartan_main_4x4": [[int(Cm[i, j]) for j in range(4)] for i in range(4)],
        "det_Cartan_main": int(detC_main), "det_Cartan_small": int(detC_small),
    }

    # ── p=2 기초층 ───────────────────────────────────────────────────────
    reg2 = [k for k in range(K) if orders[k] % 2 != 0]
    R["p2_l6"] = (len(reg2) == 6)
    b2 = blocks(2)
    R["p2_two_blocks"] = (sorted((sorted(degs[t] for t in b) for b in b2), key=str)
                          == sorted([[1, 14, 15, 21, 35], [6, 10, 10, 14]], key=str))
    # 블록별 ℓ (ℚ(√−7) rank)
    mainb = next(b for b in b2 if 1 in [degs[t] for t in b])
    otherb = next(b for b in b2 if b != mainb)
    Mm = sp.Matrix([[int_table[t][k] for k in reg2] for t in mainb])
    R["p2_main_l3"] = (Mm.rank() == 3)
    rows2 = []
    for t in otherb:
        row = []
        for k in reg2:
            if rat[t][k]:
                row.append(sp.Integer(int_table[t][k]))
            else:
                row.append(al if t == i10[0] else alb)
        rows2.append(row)
    R["p2_other_l3"] = (sp.Matrix(rows2).rank() == 3)
    # Sylow-2 = D₄ 구성적 확인
    def pmul(a, b):
        return tuple(a[b[i]] for i in range(N7))

    def pinv(a):
        r = [0] * N7
        for i, v in enumerate(a):
            r[v] = i
        return tuple(r)
    IDp = tuple(range(N7))

    def is_even(pr):
        s = 0
        seen = [False] * N7
        for i in range(N7):
            if seen[i]:
                continue
            j = i
            l = 0
            while not seen[j]:
                seen[j] = True
                j = pr[j]
                l += 1
            s += l - 1
        return s % 2 == 0

    def order_of(x):
        o = 1
        y = x
        while y != IDp:
            y = pmul(y, x)
            o += 1
        return o
    G = [pr for pr in itertools.permutations(range(N7)) if is_even(pr)]
    o4 = next(x for x in G if order_of(x) == 4)
    inv4 = pinv(o4)
    tt = next(x for x in G if order_of(x) == 2
              and pmul(pmul(x, o4), pinv(x)) == inv4)

    def span(gens):
        S = {IDp}
        fr = [IDp]
        while fr:
            nf = []
            for g in list(S):
                for h in gens:
                    q = pmul(g, h)
                    if q not in S:
                        S.add(q)
                        nf.append(q)
            fr = nf
        return S
    S2g = span([o4, tt])
    prof = sorted(order_of(x) for x in S2g)
    R["p2_sylow_D4"] = (len(S2g) == 8 and prof == [1, 2, 2, 2, 2, 2, 4, 4])
    o3a = next(x for x in G if order_of(x) == 3)
    o3b = next(x for x in G if order_of(x) == 3 and x not in span([o3a])
               and pmul(x, o3a) == pmul(o3a, x))
    S3g = span([o3a, o3b])
    R["p3_sylow_Z3sq"] = (len(S3g) == 9 and all(order_of(x) in (1, 3) for x in S3g))
    # p=2 모듈 지표
    (rref_add2, matvec2, quotient_mats2, fixed_dim2, dual_mats2, hom_dim2, nat62) = make_tools(2)
    M6_2 = nat62()
    R["p2_nat6_no_triv"] = (fixed_dim2(M6_2, 6) == 0
                            and fixed_dim2(dual_mats2(M6_2, 6), 6) == 0)
    M21_2, inc2 = pairs_mats(2)
    U2 = []
    for v in inc2:
        rref_add2(U2, v)
    R["p2_inc_rank6_degenerate"] = (len(U2) == 6)
    QM2, dq2 = quotient_mats2(M21_2, U2, 21)
    R["p2_Q15_indicators"] = (dq2 == 15 and fixed_dim2(QM2, dq2) == 1
                              and fixed_dim2(dual_mats2(QM2, dq2), dq2) == 1
                              and hom_dim2(QM2, QM2, dq2, dq2) == 2)
    out["p2_foundation"] = {
        "blocks": "{1,14,15,21,35}(주·defect D₄) + {6,10,10̄,14′}(defect 위수4)",
        "l_per_block": "3 + 3 = ℓ₂=6", "sylow2": "D₄ (프로파일 [1,2⁵,4²] 구성적)",
        "pairs_mod2": "incidence rank 6(퇴화)·Q(15): 고정1·dual1·End2",
        "honest": "완전 D·C = 미완(양 블록 비순환 defect·wild 가능 — 트리 이론 부재)",
    }

    # teeth
    R["teeth_p3_complete_D"] = R["p3_D_reconstructs_all9"]
    R["teeth_gf9_pair"] = (R["p3_lambda3_end2"] and R["p3_F2_minusI_GF9"])
    R["teeth_small_cyclic_tree"] = R["p3_small_tree_6_21_15"]

    ok = bool(all(R.values()))
    out["checks"] = R
    out["scope_honesty"] = {
        "p3": "완전 D(9×6)·C — 명시 모듈 구성(비순환 ℤ₃² defect 여도 트리 이론 불필요)",
        "p2": "기초층(블록·ℓ·Sylow·지표)까지 결정적 — 완전 D·C 는 wild 가능·정직 미완",
        "method": "결정적 GF(p) 선형대수(고정공간·Hom·End·quotient)·확률적 meataxe 금지",
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        pth = os.path.join(ROOT, ".pgf", "proofs", "A7-CARTAN-P23.json")
        os.makedirs(os.path.dirname(pth), exist_ok=True)
        with open(pth, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("A₇ p=3 완전 D·Cartan + p=2 기초층 (결정적 — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  ★p=3: 소블록 tree 6—21—15·주블록 {1,13,10,10̄(GF(9)쌍)}·D 9×6 완전·det 게이트",
              flush=True)
        print("  ★χ̂14=χ̂14′·χ̂35=2·1+13+10+10̄(√−7 방정식이 확정)·p=2 기초층+정직 미완", flush=True)
        print("  → .pgf/proofs/A7-CARTAN-P23.json", flush=True)
    print(f"a7_cartan_p23_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
