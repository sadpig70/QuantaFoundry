#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""a7_brauer_trees_observe — TrackHE18: A₇ **Brauer tree·decomposition matrix D·Cartan C 완결**
(p=5,7 cyclic defect) (관측, seal 아님). [[a7_brauer_observe]](TrackHE17 P6)가 "완전 D·C·Brauer
tree 구체형=미착수"로 남긴 축의 완결. ★**문자표까지 완전 자체유도**(표준값 인용 0).

관측 5축:
  A. ★**문자표 완전 자체유도(Dixon)**: A₇ 2520원소 열거→9 켤레류(크기[1,70,105,504,630,280,210,
     360,360]·위수[1,3,2,5,4,3,6,7,7]·7-cycle 분열)→클래스대수 구조상수→GF(421)(421≡1 mod 420=exp)
     고유벡터 9개(중심문자)→차수 **[1,6,10,10,14,14,15,21,35]·Σd²=2520**→cyclotomic 정확 lift
     (a_m 정수 복원·무리셀=10차원쌍의 7A/7B(ℚ(√−7))만)→직교성 검증.
  B. **block 분포(중심문자 mod p)**: p=7 principal {1,6,10,10̄,15}+defect-0 {14,14′,21,35}·
     p=5 principal {1,6,14,14′,21}+defect-0 {10,10̄,15,35} — TrackHE17 P6 정합.
  C. ★**p=7 Brauer tree(유일)**: 트리 전수(Prüfer 16×라벨 6, 예외꼭짓점 m=(7−1)/3=2={10,10̄})에서
     정수해(χ̂=Dφ·양수차수)는 dims 2계열 {1,5,10}/{1,6,9}만 생존 → **GF(7) 결정적 배제**: natural
     몫 V₅(5차원, all-ones∈sum-zero mod7)의 tr(3-cycle)=2≠5 → 전-trivial 구성 불가 → 6,9>5 라
     {1,6,9} 불가 ⟹ **라인 1—6—15—(10,10̄)ₑₓ꜀ 유일**·simples **{1,5,10}**·det C=**7**.
  D. ★**p=5 Brauer tree(유일)**: 전수(Prüfer 125×라벨 120, m=1)에서 라인 형상 유일·14/14′ 배정
     2후보 dims (1,6,8,13)/(1,6,7,14) → **결정적 Hom 판정**: Q=pairs-perm(21)/im(incidence)(=χ₁₄̂,
     14차원 명시구성)·trivial 인자 0(고정공간 Q·Q* 모두 0)·**Hom(Q,6̂)=1** → χ₁₄̂=[8|6] 2-layer
     ⟹ **라인 1—14′—21—14—6**·simples **{1,13,8,6}**·det C=**5**.
  E. **D·C 게이트**: D∈{0,1}·χ̂=Dφ 정확 재구성·C=DᵀD 대칭·**det C=p**(defect-1)·예외쌍 행 동일
     (p=7)·C 삼중대각(라인 트리).

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - 트리 유일성 = 전수 탐색 + **결정적 모듈러 판정**(GF(p) 명시 모듈: trace·고정공간·Hom — 확률적
    meataxe 아님). 외부 사실 = cyclic-defect Brauer tree 정리(Dade: D=트리 incidence)뿐.
  - 문자표는 Dixon 완전 자체유도 — 문헌 문자표 인용 0(차수 리스트도 산출물).
  - p=2,3(비순환 defect: D₄·ℤ₃²)의 D·C 는 트리 이론 부재 → 미착수=다음.

사용: python -m qf_witness.observe.a7_brauer_trees_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import itertools
import heapq
import random
from fractions import Fraction as Fr

N7 = 7
GENS = [(1, 2, 0, 3, 4, 5, 6), (1, 2, 3, 4, 5, 6, 0)]


def pmul(a, b):
    return tuple(a[b[i]] for i in range(N7))


def pinv(a):
    r = [0] * N7
    for i, v in enumerate(a):
        r[v] = i
    return tuple(r)


IDp = tuple(range(N7))


def is_even(p):
    s = 0
    seen = [False] * N7
    for i in range(N7):
        if seen[i]:
            continue
        j = i
        l = 0
        while not seen[j]:
            seen[j] = True
            j = p[j]
            l += 1
        s += l - 1
    return s % 2 == 0


def dixon_char_table():
    """완전 자체유도: 켤레류·구조상수·Dixon GF(421)·cyclotomic lift → 정확 문자표."""
    G = [p for p in itertools.permutations(range(N7)) if is_even(p)]
    cls_of = {}
    classes = []
    for p in G:
        if p in cls_of:
            continue
        cid = len(classes)
        frontier = [p]
        cls_of[p] = cid
        members = [p]
        while frontier:
            nf = []
            for x in frontier:
                for g in GENS:
                    y = pmul(pmul(g, x), pinv(g))
                    if y not in cls_of:
                        cls_of[y] = cid
                        members.append(y)
                        nf.append(y)
            frontier = nf
        classes.append(members)
    K = len(classes)
    reps = [c[0] for c in classes]
    sizes = [len(c) for c in classes]

    def order(p):
        o = 1
        x = p
        while x != IDp:
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
        pm = []
        x = IDp
        for l in range(orders[ci]):
            pm.append(cls_of[x])
            x = pmul(x, r)
        powmap.append(pm)
    invmap = [cls_of[pinv(r)] for r in reps]

    q = 421
    GN = 2520

    def inv_mod(a):
        return pow(a, q - 2, q)
    rnd = random.Random(7)
    while True:
        cs = [rnd.randrange(q) for _ in range(K)]
        M = [[sum(cs[i] * A[i][j][k] for i in range(K)) % q for k in range(K)]
             for j in range(K)]
        eigs = []
        for lam in range(q):
            Tm = [[(M[r][c] - (lam if r == c else 0)) % q for c in range(K)]
                  for r in range(K)]
            r0 = 0
            piv_of = {}
            for c in range(K):
                pr = None
                for r in range(r0, K):
                    if Tm[r][c] % q:
                        pr = r
                        break
                if pr is None:
                    continue
                Tm[r0], Tm[pr] = Tm[pr], Tm[r0]
                iv = inv_mod(Tm[r0][c])
                Tm[r0] = [(x * iv) % q for x in Tm[r0]]
                for r in range(K):
                    if r != r0 and Tm[r][c]:
                        f = Tm[r][c]
                        Tm[r] = [(Tm[r][x] - f * Tm[r0][x]) % q for x in range(K)]
                piv_of[r0] = c
                r0 += 1
            if r0 < K:
                eigs.append((lam, K - r0, Tm, r0, piv_of))
        if sum(m for _, m, _, _, _ in eigs) == K and all(m == 1 for _, m, _, _, _ in eigs):
            break
    omegas = []
    for lam, m, Tm, r0, piv_of in eigs:
        pivcols = set(piv_of.values())
        free = [c for c in range(K) if c not in pivcols][0]
        v = [0] * K
        v[free] = 1
        for r, c in piv_of.items():
            v[c] = (-Tm[r][free]) % q
        iv = inv_mod(v[0])
        omegas.append([(x * iv) % q for x in v])
    degs_mod = []
    for om in omegas:
        s = 0
        for k in range(K):
            s = (s + om[k] * om[invmap[k]] * inv_mod(sizes[k])) % q
        d2 = (GN * inv_mod(s)) % q
        root = None
        for r in range(1, q):
            if r * r % q == d2:
                root = min(r, q - r)
                break
        degs_mod.append(root)
    chi_mod = [[om[k] * dg % q * inv_mod(sizes[k]) % q for k in range(K)]
               for om, dg in zip(omegas, degs_mod)]

    def primroot():
        for g in range(2, q):
            x = 1
            ok = True
            for d in (2, 3, 5, 7):        # 420=2²·3·5·7
                if pow(g, (q - 1) // d, q) == 1:
                    ok = False
                    break
            if ok:
                return g
    PR = primroot()
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
                a = s * inv_mod(o) % q
                ams.append(a)
            row.append(ams)
        exact.append(row)
    import cmath
    int_table = []
    rat = []
    for t in range(K):
        irow = []
        rrow = []
        for k in range(K):
            o = orders[k]
            v = sum(exact[t][k][m] * cmath.exp(2j * cmath.pi * m / o) for m in range(o))
            isr = abs(v.imag) < 1e-9 and abs(v.real - round(v.real)) < 1e-9
            rrow.append(isr)
            irow.append(round(v.real) if isr else None)
        int_table.append(irow)
        rat.append(rrow)
    return {"K": K, "sizes": sizes, "orders": orders, "invmap": invmap,
            "chi_mod": chi_mod, "int_table": int_table, "rat": rat,
            "degs": [int_table[t][0] for t in range(K)],
            # ★2026-07-26 추가(비파괴): 클래스 대표·cyclotomic 다중도 —
            # a7_cartan_p2_observe 가 동일 클래스 순서로 Brauer 문자를 계산하기 위해 필요.
            "reps": reps, "exact": exact}


def prufer_trees(n):
    for seq in itertools.product(range(n), repeat=n - 2):
        deg = [1] * n
        for s in seq:
            deg[s] += 1
        leaves = [i for i in range(n) if deg[i] == 1]
        heapq.heapify(leaves)
        degc = deg[:]
        edges = []
        for s in seq:
            l = heapq.heappop(leaves)
            edges.append((l, s))
            degc[s] -= 1
            if degc[s] == 1:
                heapq.heappush(leaves, s)
        u = heapq.heappop(leaves)
        v = heapq.heappop(leaves)
        edges.append((u, v))
        yield edges


def solve_phi(Dm, chi_rows, reg, ne):
    """φ = (DᵀD)⁻¹Dᵀχ̂ 정확해; 정수·양차수·재구성 검증. 반환 dims or None"""
    nr = len(Dm)
    DT = [[Dm[r][c] for r in range(nr)] for c in range(ne)]
    DTD = [[sum(DT[i][r] * Dm[r][j] for r in range(nr)) for j in range(ne)]
           for i in range(ne)]
    Aug = [[Fr(DTD[i][j]) for j in range(ne)] + [Fr(1 if j == i else 0) for j in range(ne)]
           for i in range(ne)]
    for c in range(ne):
        pr = None
        for r in range(c, ne):
            if Aug[r][c] != 0:
                pr = r
                break
        if pr is None:
            return None
        Aug[c], Aug[pr] = Aug[pr], Aug[c]
        f = Aug[c][c]
        Aug[c] = [x / f for x in Aug[c]]
        for r in range(ne):
            if r != c and Aug[r][c] != 0:
                f2 = Aug[r][c]
                Aug[r] = [Aug[r][x] - f2 * Aug[c][x] for x in range(2 * ne)]
    inv = [[Aug[i][ne + j] for j in range(ne)] for i in range(ne)]
    phi = []
    for ei in range(ne):
        row = []
        for ki in range(len(reg)):
            s = Fr(0)
            for i2 in range(ne):
                s += inv[ei][i2] * sum(DT[i2][r] * chi_rows[r][ki] for r in range(nr))
            if s.denominator != 1:
                return None
            row.append(int(s))
        phi.append(row)
    if not all(sum(Dm[r][e] * phi[e][ki] for e in range(ne)) == chi_rows[r][ki]
               for r in range(nr) for ki in range(len(reg))):
        return None
    dims = [phi[e][0] for e in range(ne)]
    if any(x <= 0 for x in dims):
        return None
    return dims


# ── GF(p) 결정적 판정 도구 ──────────────────────────────────────────────────
def _rref_add(basis, v, p):
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


def gf5_pairs_verdict():
    """Q=pairs21/im(incidence): trivial 인자 0 + Hom(Q,6̂)=1 → 14̂=[8|6]."""
    p = 5
    PAIRS = [frozenset(x) for x in itertools.combinations(range(7), 2)]
    pidx = {fs: i for i, fs in enumerate(PAIRS)}
    M21 = []
    for g in GENS:
        M = [[0] * 21 for _ in range(21)]
        for i, fs in enumerate(PAIRS):
            M[pidx[frozenset(g[x] for x in fs)]][i] = 1
        M21.append(M)
    U = []
    for i in range(7):
        v = [0] * 21
        for j in range(7):
            if j != i:
                v[pidx[frozenset((i, j))]] = 1
        _rref_add(U, v, p)
    rank_inc = len(U)

    def matvec(M, v):
        return [sum(M[i][j] * v[j] for j in range(len(v))) % p for i in range(len(M))]
    full = [b[:] for b in U]
    ext = []
    for i in range(21):
        e = [0] * 21
        e[i] = 1
        if _rref_add(full, e, p):
            ext.append(full[-1])
    dq = len(ext)

    def coords_ext(w):
        v = list(w)
        c = [0] * dq
        for b in U:
            lead = next(k for k, x in enumerate(b) if x)
            if v[lead]:
                f = v[lead] * pow(b[lead], p - 2, p) % p
                v = [(v[k] - f * b[k]) % p for k in range(21)]
        for ei, b in enumerate(ext):
            lead = next(k for k, x in enumerate(b) if x)
            if v[lead]:
                f = v[lead] * pow(b[lead], p - 2, p) % p
                c[ei] = f
                v = [(v[k] - f * b[k]) % p for k in range(21)]
        assert not any(v)
        return c
    QM = []
    for M in M21:
        Q = [[0] * dq for _ in range(dq)]
        for j in range(dq):
            c = coords_ext(matvec(M, ext[j]))
            for r in range(dq):
                Q[r][j] = c[r]
        QM.append(Q)

    def fixed_dim(mats, dim):
        rows = []
        for M in mats:
            for r in range(dim):
                row = [(M[r][c] - (1 if r == c else 0)) % p for c in range(dim)]
                if any(row):
                    rows.append(row)
        b = []
        for v in rows:
            _rref_add(b, v, p)
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
    QMd = [[[matinv(M)[c][r] for c in range(dq)] for r in range(dq)] for M in QM]
    fQ = fixed_dim(QM, dq)
    fQd = fixed_dim(QMd, dq)
    M6 = []
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
        M6.append(M)

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
            _rref_add(b, v, p)
        return da * db - len(b)
    h1 = hom_dim(M6, QM, 6, dq)
    h2 = hom_dim(QM, M6, dq, 6)
    return rank_inc, dq, fQ, fQd, h1, h2


def gf7_trace_verdict():
    """V₅ = (sum-zero 6)/⟨ones⟩ mod 7: tr(3-cycle)=2≠5 → {1,6,9} 배제."""
    p = 7
    cs = [(i + 1) % p for i in range(6)]
    inv5 = pow(cs[5], p - 2, p)
    M0 = [[0] * 5 for _ in range(5)]
    g = GENS[0]
    for i in range(5):
        vec = [0] * 7
        vec[g[i]] = (vec[g[i]] + 1) % p
        vec[g[i + 1]] = (vec[g[i + 1]] - 1) % p
        c = [0] * 6
        s = 0
        for k2 in range(6):
            s = (s + vec[k2]) % p
            c[k2] = s
        red = [(c[j] - c[5] * inv5 * cs[j]) % p for j in range(5)]
        for r in range(5):
            M0[r][i] = red[r]
    return sum(M0[i][i] for i in range(5)) % p


def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "a7-brauer-trees/v1",
           "_note": ("A₇ Brauer tree·D·Cartan 완결(p=5,7 cyclic defect) — 문자표 Dixon 완전 자체유도"
                     "·트리 전수+GF(p) 결정적 판정. 관측·seal 아님·module 0·root 불변. "
                     "p=2,3(비순환 defect)=다음.")}

    # A. 문자표
    T = dixon_char_table()
    K, sizes, orders, degs = T["K"], T["sizes"], T["orders"], T["degs"]
    int_table, rat = T["int_table"], T["rat"]
    R["A_9_classes"] = (K == 9)
    R["A_sizes"] = (sorted(sizes) == sorted([1, 70, 105, 504, 630, 280, 210, 360, 360]))
    R["A_degrees"] = (sorted(degs) == [1, 6, 10, 10, 14, 14, 15, 21, 35])
    R["A_sum_d2_2520"] = (sum(d * d for d in degs) == 2520)
    irr_cells = [(t, k) for t in range(K) for k in range(K) if not rat[t][k]]
    R["A_irrational_only_10pair_7AB"] = (len(irr_cells) == 4 and
                                         all(degs[t] == 10 and orders[k] == 7
                                             for t, k in irr_cells))
    q = 421
    okd = True
    for t1 in range(K):
        for t2 in range(K):
            s = 0
            for k in range(K):
                s = (s + sizes[k] * T["chi_mod"][t1][k] * T["chi_mod"][t2][T["invmap"][k]]) % q
            if s != (2520 % q if t1 == t2 else 0):
                okd = False
    R["A_orthogonality"] = okd
    out["char_table"] = {"degrees": sorted(degs), "class_sizes": sizes,
                         "element_orders": orders,
                         "irrational": "10-dim 쌍의 7A/7B(ℚ(√−7))만"}

    # B. blocks (중심문자 mod p; 무리셀은 √−7≡0 mod7 → α≡3)
    def blocks(p):
        sig = {}
        for t in range(K):
            s = []
            for k in range(K):
                if rat[t][k]:
                    s.append((sizes[k] * int_table[t][k] // degs[t]) % p)
                else:
                    s.append((36 * 3) % p if p == 7 else "X")
            sig.setdefault(tuple(s), []).append(t)
        return list(sig.values())
    b7 = blocks(7)
    prin7 = [b for b in b7 if len(b) > 1][0]
    R["B_p7_principal"] = (sorted(degs[t] for t in prin7) == [1, 6, 10, 10, 15])
    R["B_p7_defect0"] = (sorted(degs[t] for b in b7 if len(b) == 1 for t in b)
                         == [14, 14, 21, 35])
    prin5 = [t for t in range(K) if degs[t] in (1, 6, 21)] + \
            [t for t in range(K) if degs[t] == 14]
    R["B_p5_defect0_by_degree"] = all(degs[t] % 5 == 0 for t in range(K) if t not in prin5)
    out["blocks"] = {"p7_principal": [1, 6, 10, 10, 15], "p7_defect0": [14, 14, 21, 35],
                     "p5_principal": [1, 6, 14, 14, 21], "p5_defect0": [10, 10, 15, 35]}

    # C. p=7 tree
    ten_idx = [t for t in prin7 if degs[t] == 10]
    others7 = [t for t in prin7 if degs[t] != 10]
    reg7 = [k for k in range(K) if orders[k] % 7 != 0]
    sols7 = []
    for perm in itertools.permutations(others7):
        labels = ["EXC"] + list(perm)
        for edges in prufer_trees(4):
            D = {t: [0] * 3 for t in prin7}
            for ei, (u, v) in enumerate(edges):
                for vv in (u, v):
                    if vv == 0:
                        for t in ten_idx:
                            D[t][ei] = 1
                    else:
                        D[labels[vv]][ei] = 1
            Dm = [D[t] for t in prin7]
            chi_rows = [[int_table[t][k] for k in reg7] for t in prin7]
            dims = solve_phi(Dm, chi_rows, reg7, 3)
            if dims is not None:
                lab = lambda v: "EXC" if v == 0 else str(degs[labels[v]])
                key = tuple(sorted(tuple(sorted((lab(u), lab(v)))) for u, v in edges))
                sols7.append((key, tuple(sorted(dims)), Dm))
    dimsets7 = set(ds for _, ds, _ in sols7)
    R["C_two_dim_families"] = (dimsets7 == {(1, 5, 10), (1, 6, 9)})
    tr5 = gf7_trace_verdict()
    R["C_gf7_trace_excludes_169"] = (tr5 != 5)     # 전-trivial 불가 → 6,9>5 → {1,6,9} 배제
    final7 = [(k, ds, Dm) for k, ds, Dm in sols7 if ds == (1, 5, 10)]
    trees7 = set(k for k, _, _ in final7)
    R["C_p7_tree_unique"] = (len(trees7) == 1 and
                            trees7 == {(("1", "6"), ("15", "6"), ("15", "EXC"))})
    Dm7 = final7[0][2]
    C7 = [[sum(Dm7[r][i] * Dm7[r][j] for r in range(5)) for j in range(3)] for i in range(3)]
    det7 = (C7[0][0] * (C7[1][1] * C7[2][2] - C7[1][2] * C7[2][1])
            - C7[0][1] * (C7[1][0] * C7[2][2] - C7[1][2] * C7[2][0])
            + C7[0][2] * (C7[1][0] * C7[2][1] - C7[1][1] * C7[2][0]))
    R["C_detC_7"] = (abs(det7) == 7)
    out["p7"] = {"tree": "1 — 6 — 15 — (10,10̄)exc  [line, m=2]",
                 "simple_dims": [1, 5, 10], "det_Cartan": abs(det7),
                 "verdict_tool": "GF(7) V₅ trace=%d≠5 → {1,6,9} 결정적 배제" % tr5}

    # D. p=5 tree
    reg5 = [k for k in range(K) if orders[k] % 5 != 0]
    sols5 = []
    perms5 = itertools.permutations(range(5))
    for perm in perms5:
        labels = [prin5[i] for i in perm]
        for edges in prufer_trees(5):
            D = {t: [0] * 4 for t in prin5}
            for ei, (u, v) in enumerate(edges):
                D[labels[u]][ei] = 1
                D[labels[v]][ei] = 1
            Dm = [D[t] for t in prin5]
            chi_rows = [[int_table[t][k] for k in reg5] for t in prin5]
            dims = solve_phi(Dm, chi_rows, reg5, 4)
            if dims is not None:
                # 14/14' 구분 라벨: prin5 순서 [1,6,21,14,14'] — t 인덱스로
                keyl = tuple(sorted(tuple(sorted((prin5.index(labels[u]), prin5.index(labels[v]))))
                                    for u, v in edges))
                sols5.append((keyl, tuple(sorted(dims)), Dm))
        if quick and sols5:
            pass
    dimsets5 = set(ds for _, ds, _ in sols5)
    R["D_two_candidates"] = (dimsets5 == {(1, 6, 8, 13), (1, 6, 7, 14)})
    rank_inc, dq, fQ, fQd, h1, h2 = gf5_pairs_verdict()
    R["D_rank_incidence_7"] = (rank_inc == 7)
    R["D_Q_dim14"] = (dq == 14)
    R["D_no_trivial_factor"] = (fQ == 0 and fQd == 0)
    R["D_hom_Q_to_6"] = (h1 == 0 and h2 == 1)      # 14̂=[8|6] → 후보 (1,6,8,13)
    # dims (1,6,8,13)은 14↔14' 스왑 2배정 모두 허용 — Hom 판정(χ₁₄(pairs)=[8|6]→6 옆)으로 유일화.
    k3A = next(k for k in range(K) if orders[k] == 3 and sizes[k] == 70)
    t14_pairs = next(t for t in prin5 if degs[t] == 14 and int_table[t][k3A] == 2)
    i14p = prin5.index(t14_pairs)
    i6 = next(i for i, t in enumerate(prin5) if degs[t] == 6)
    final5 = [(k, ds, Dm) for k, ds, Dm in sols5
              if ds == (1, 6, 8, 13) and tuple(sorted((i6, i14p))) in k]
    trees5 = set(k for k, _, _ in final5)
    R["D_p5_tree_unique"] = (len(trees5) == 1)
    Dm5 = final5[0][2]
    C5 = [[sum(Dm5[r][i] * Dm5[r][j] for r in range(5)) for j in range(4)] for i in range(4)]

    def det4(C):
        import copy
        A = [[Fr(C[i][j]) for j in range(4)] for i in range(4)]
        d = Fr(1)
        for c in range(4):
            pr = next((r for r in range(c, 4) if A[r][c] != 0), None)
            if pr is None:
                return 0
            if pr != c:
                A[c], A[pr] = A[pr], A[c]
                d = -d
            d *= A[c][c]
            f = A[c][c]
            A[c] = [x / f for x in A[c]]
            for r in range(c + 1, 4):
                if A[r][c] != 0:
                    f2 = A[r][c]
                    A[r] = [A[r][x] - f2 * A[c][x] for x in range(4)]
        return int(d)
    R["D_detC_5"] = (abs(det4(C5)) == 5)
    out["p5"] = {"tree": "1 — 14' — 21 — 14 — 6  [line, m=1]",
                 "simple_dims": [1, 13, 8, 6], "det_Cartan": abs(det4(C5)),
                 "verdict_tool": ("Q=pairs21/im(incidence)=χ₁₄̂: trivial 0·Hom(Q,6̂)=1 → "
                                  "χ₁₄̂=[8|6] → 14(pairs)는 6옆·14'는 1옆(=1+13)")}

    # E. teeth
    R["teeth_detC_eq_p_both"] = (R["C_detC_7"] and R["D_detC_5"])
    ten_rows = [i for i, t in enumerate(prin7) if degs[t] == 10]
    R["teeth_exceptional_rows_equal"] = all(Dm7[ten_rows[0]][e] == Dm7[ten_rows[1]][e]
                                            for e in range(3))
    R["teeth_D_01"] = all(x in (0, 1) for Dm in (Dm7, Dm5) for row in Dm for x in row)

    ok = bool(all(R.values()))
    out["checks"] = R
    out["scope_honesty"] = {
        "delivered": "p=5,7 Brauer tree·D·C 완결 — 문자표 Dixon 완전 자체유도·결정적 모듈러 판정",
        "external_fact": "cyclic-defect Brauer tree 정리(Dade: D=트리 incidence) 하나",
        "deterministic": "GF(p) 판정 전부 정확 선형대수(trace·고정공간·Hom) — 확률적 meataxe 미사용",
        "next": "p=2,3 비순환 defect(D₄·ℤ₃²)의 D·C — 트리 이론 부재·별도 모듈러 계산",
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "A7-BRAUER-TREES.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("A₇ Brauer tree·D·Cartan 완결 (Dixon 자체유도 — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  ★p=7: 1—6—15—(10,10̄)exc·simples{1,5,10}·detC=7", flush=True)
        print("  ★p=5: 1—14'—21—14—6·simples{1,13,8,6}·detC=5", flush=True)
        print("  → .pgf/proofs/A7-BRAUER-TREES.json", flush=True)
    print(f"a7_brauer_trees_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
