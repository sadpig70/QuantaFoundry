# -*- coding: utf-8 -*-
"""GF(q) 위의 **기본대수 엔진** — `tilting_complex_observe` 의 𝔽₂ 엔진을 체로 일반화.

동기: 𝔽₂ 엔진은 `End(S) = 𝔽₂`(분해체)를 전제해서 **비분해체 블록**(SL(2,3)·A₆ p=3)에서는
Cartan 층까지만 같은 의미로 간다. 실현화 대수에서 스칼라 `J` 는 **중심 원소**라
rad·Hom·사슬사상 공간이 전부 `J`-안정이고, 필요한 것은 **계수산술을 GF(q) 로 올리는 것**뿐이다.

정직 경계:
  · `tilting_complex_observe`(byte-결정론 확정)는 **건드리지 않는다** — 여기 코드는 별도 경로다.
  · 정오는 **q=2 회귀**로 판정한다: 같은 대수에 대해 𝔽₂ 엔진과 **모든 산출이 일치**해야 한다.
"""
import itertools

import numpy as np


# ══════════════════════════════════════════════════════════════════════
# GF(q) — 원소는 0..q-1 (p진 계수의 정수 인코딩)
# ══════════════════════════════════════════════════════════════════════
class GF:
    """`GF(p^k)`. `poly` = `x^k = Σ poly[i]·x^i` 의 계수(길이 k). k=1 이면 소체."""

    def __init__(self, p, k=1, poly=None):
        self.p, self.k, self.q = p, k, p ** k
        q = self.q
        if k == 1:
            A = (np.arange(q)[:, None] + np.arange(q)[None, :]) % p
            M = (np.arange(q)[:, None] * np.arange(q)[None, :]) % p
        else:
            assert poly is not None and len(poly) == k
            def dig(x):
                return [(x // p ** i) % p for i in range(k)]

            def enc(c):
                return sum(int(c[i]) % p * p ** i for i in range(k))

            A = np.zeros((q, q), dtype=np.int64)
            for a in range(q):
                for b in range(q):
                    A[a, b] = enc([x + y for x, y in zip(dig(a), dig(b))])
            # x^k 환원표
            red = [list(poly)]
            for _ in range(k - 2):
                prev = red[-1]
                nxt = [0] * k
                for i in range(k - 1):
                    nxt[i + 1] = prev[i]
                for i in range(k):
                    nxt[i] = (nxt[i] + prev[k - 1] * poly[i]) % p
                red.append(nxt)
            M = np.zeros((q, q), dtype=np.int64)
            for a in range(q):
                for b in range(q):
                    c = [0] * (2 * k - 1)
                    da, db = dig(a), dig(b)
                    for i in range(k):
                        for j in range(k):
                            c[i + j] = (c[i + j] + da[i] * db[j]) % p
                    for t in range(2 * k - 2, k - 1, -1):
                        if c[t]:
                            for i in range(k):
                                c[t - k + i] = (c[t - k + i]
                                                + c[t] * poly[i]) % p
                            c[t] = 0
                    M[a, b] = enc(c[:k])
        self.ADD, self.MUL = A, M
        self.NEG = np.array([next(b for b in range(q) if A[a, b] == 0)
                             for a in range(q)], dtype=np.int64)
        self.INV = np.zeros(q, dtype=np.int64)
        for a in range(1, q):
            self.INV[a] = next(b for b in range(1, q) if M[a, b] == 1)
        self.PW = p ** np.arange(k, dtype=np.int64)
        self.DIG = np.array([[(v // p ** i) % p for i in range(k)]
                             for v in range(q)], dtype=np.int64)
        # RED[i,j] = `x^i · x^j` 의 자릿수 — `p^i` 가 곧 `x^i` 의 인코딩이다
        self.RED = np.array([[self.DIG[M[int(self.PW[i]), int(self.PW[j])]]
                              for j in range(k)] for i in range(k)],
                            dtype=np.int64)

    def add(self, a, b):
        return self.ADD[a, b]

    def sub(self, a, b):
        return self.ADD[a, self.NEG[b]]

    def mul(self, a, b):
        return self.MUL[a, b]

    def digits(self, X):
        """원소 배열 → `p` 진 자릿수 평면 `(..., k)`."""
        return self.DIG[X]

    def mmd(self, A, Bd):
        """★`B` 를 **미리 자릿수로 펼친** 행렬곱 — 같은 `B` 를 반복해 쓸 때 gather 를 아낀다."""
        n, t = A.shape[0], A.shape[1]
        m = Bd.shape[1]
        if n == 0 or t == 0 or m == 0:
            return np.zeros((n, m), dtype=np.int64)
        if self.k == 1:
            return (A @ Bd[:, :, 0]) % self.p
        Ad = self.DIG[A]
        acc = np.zeros((n, m, self.k), dtype=np.int64)
        for i in range(self.k):
            for j in range(self.k):
                P = None
                for l in range(self.k):
                    c = int(self.RED[i, j, l])
                    if not c:
                        continue
                    if P is None:
                        P = (Ad[:, :, i] @ Bd[:, :, j]) % self.p
                    acc[:, :, l] += c * P
        return ((acc % self.p) * self.PW).sum(-1)

    def mm(self, A, B):
        """행렬곱 — ★`GF(p^k)` 곱은 **𝔽_p-쌍선형**이므로 자릿수 평면의 **정수 행렬곱** `k²` 개로 쪼갠다.

        `a·b = Σ_{i,j} a_i b_j x^{i+j}` 이고 `x^{i+j}` 의 자릿수가 `RED[i,j]` 다 ⟹
        `(n,t,m)` 중간 배열도, 축 길이만큼의 표 조회도 없어진다(`k=1` 이면 `(A@B) % p` 한 번)."""
        if self.k == 1:
            if A.shape[1] == 0 or A.shape[0] == 0 or B.shape[1] == 0:
                return np.zeros((A.shape[0], B.shape[1]), dtype=np.int64)
            return (A @ B) % self.p
        return self.mmd(A, self.DIG[B])


def rref(F, A):
    """행 RREF — pivot 열에서 완전 축약된 (basis, pivots). 𝔽₂ 판과 같은 순서."""
    A = A.copy()
    rows, cols = A.shape
    piv, r = [], 0
    for c in range(cols):
        nz = np.nonzero(A[r:, c])[0]
        if not len(nz):
            continue
        pr = r + int(nz[0])
        A[[r, pr]] = A[[pr, r]]
        A[r] = F.MUL[F.INV[A[r, c]], A[r]]
        col = A[:, c].copy()
        col[r] = 0
        if col.any():
            A = F.ADD[A, F.NEG[F.MUL[col[:, None], A[r][None, :]]]]
        piv.append(c)
        r += 1
        if r == rows:
            break
    return A[:r], piv


def rref_insert(F, B, piv, v):
    """RREF 기저에 v 를 증분 삽입 — 독립이면 (True, B′, piv′)."""
    w = v.copy()
    for i, c in enumerate(piv):
        if w[c]:
            w = F.ADD[w, F.NEG[F.MUL[w[c], B[i]]]]
    nz = np.nonzero(w)[0]
    if not len(nz):
        return False, B, piv
    c0 = int(nz[0])
    w = F.MUL[F.INV[w[c0]], w]
    if len(B):
        B = F.ADD[B, F.NEG[F.MUL[B[:, c0][:, None], w[None, :]]]]
        B = np.vstack([B, w[None, :]])
    else:
        B = w[None, :].copy()
    return True, B, piv + [c0]


def nullspace(F, M):
    """{x : M x = 0} 의 기저(행)."""
    if M.shape[0] == 0:
        return np.eye(M.shape[1], dtype=np.int64)
    R, piv = rref(F, M)
    n = M.shape[1]
    free = [c for c in range(n) if c not in piv]
    out = []
    for f in free:
        v = np.zeros(n, dtype=np.int64)
        v[f] = 1
        for i, c in enumerate(piv):
            v[c] = F.NEG[R[i, f]]
        out.append(v)
    return (np.array(out, dtype=np.int64) if out
            else np.zeros((0, n), dtype=np.int64))


# ══════════════════════════════════════════════════════════════════════
# ★GF(2^k) 비트평면 rank — 큰 미분행렬(HH²)의 규모 벽을 뚫는다
# ══════════════════════════════════════════════════════════════════════
def _scal_map(F):
    """스칼라 s 곱을 평면 위 𝔽₂-선형 사상으로: `M_s[t][u] = MUL[s, 2^u]` 의 t 비트."""
    k = F.k
    return {s: [[int(F.MUL[s, 1 << u] >> t) & 1 for u in range(k)]
                for t in range(k)] for s in range(1, F.q)}


def _smul_row(SM, s, row, k):
    out = []
    for t in range(k):
        acc = np.zeros_like(row[0])
        for u in range(k):
            if SM[s][t][u]:
                acc = acc ^ row[u]
        out.append(acc)
    return out


def rank_packed(F, A):
    """`p = 2` 전용 — 비트평면 + `packbits` 로 rank(전방 소거·값별 그룹 벡터화).

    ★행마다 파이썬 루프를 돌지 않는다: pivot 열의 값으로 행을 **q−1 그룹**으로 묶고
    그룹마다 `v·pivot행` 을 한 번 만들어 **브로드캐스트 XOR** 한다."""
    assert F.p == 2, F.p
    if A.size == 0:
        return 0
    n, m = A.shape
    k, SM = F.k, _scal_map(F)
    P = [np.packbits(((A.astype(np.int64) >> t) & 1).astype(np.uint8), axis=1)
         for t in range(k)]
    r = 0
    for c in range(m):
        if r >= n:
            break
        by, bt = c // 8, 7 - (c % 8)
        vals = np.zeros(n - r, dtype=np.int64)
        for t in range(k):
            vals |= (((P[t][r:, by] >> bt) & 1).astype(np.int64) << t)
        nz = np.nonzero(vals)[0]
        if not len(nz):
            continue
        j0 = int(nz[0])
        if j0:
            for t in range(k):
                P[t][[r, r + j0]] = P[t][[r + j0, r]]
            vals[0], vals[j0] = vals[j0], vals[0]
        rowp = _smul_row(SM, int(F.INV[int(vals[0])]),
                         [P[t][r] for t in range(k)], k)
        for t in range(k):
            P[t][r] = rowp[t]
        below = vals[1:]
        for sc in range(1, F.q):
            idx = np.nonzero(below == sc)[0]
            if not len(idx):
                continue
            sr = _smul_row(SM, sc, rowp, k)
            idx = idx + r + 1
            for t in range(k):
                P[t][idx] ^= sr[t]
        r += 1
    return r


def rank(F, M):
    return 0 if M.size == 0 else len(rref(F, M)[1])


def left_inverse(F, rows):
    """독립 행들의 좌역행렬 — α = Linv @ w."""
    if not len(rows):
        return np.zeros((0, 0), dtype=np.int64)
    R = np.array(rows, dtype=np.int64)
    m, L = R.shape
    Rr, piv = rref(F, np.concatenate(
        [R.T, np.eye(L, dtype=np.int64)], axis=1))
    Linv = np.zeros((m, L), dtype=np.int64)
    for r, c in zip(Rr, piv):
        if c < m:
            Linv[c] = r[m:]
    return Linv


# ══════════════════════════════════════════════════════════════════════
# 기본대수(구조상수) — 곱 규약 `a·b := b∘a`
# ══════════════════════════════════════════════════════════════════════
def inv_sq(F, M):
    """정사각 가역행렬의 역 — `[M | I]` RREF."""
    m = M.shape[0]
    R, piv = rref(F, np.concatenate([M, np.eye(m, dtype=np.int64)], axis=1))
    assert piv == list(range(m)), piv
    return R[:, m:]


def pack(F, names, cnt, MT):
    off, pos = {}, 0
    for i in names:
        for j in names:
            off[(i, j)] = pos
            pos += cnt[(i, j)]
    assert pos == MT.shape[0], (pos, MT.shape)
    return {"names": list(names), "cnt": dict(cnt), "off": off, "n": pos,
            "MT": MT, "F": F}


def _mtd(alg):
    """구조상수를 `(n, n², k)` 자릿수 평면으로 **한 번만** 펼쳐 캐시한다."""
    d = alg.get("_MTd")
    if d is None:
        n = alg["n"]
        d = alg["F"].DIG[alg["MT"].reshape(n, n * n)]
        alg["_MTd"] = d
    return d


def amul(alg, x, y):
    """★`Σ_{u,v} x[u] y[v] MT[u,v,w]` — **성분마다 `n×n` 곱을 돌리지 않는다**.

    `MT` 를 `(n, n²)` 로 보면 `S = x·MT` 는 **행렬곱 한 번**이고 `x·y = y·S` 다."""
    F, n = alg["F"], alg["n"]
    if not x.any() or not y.any():
        return np.zeros(n, dtype=np.int64)
    S = F.mmd(x[None, :], _mtd(alg)).reshape(n, n)
    return F.mm(y[None, :], S)[0]


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
    """`f: X→Y` · `g: Y→Z` ⟹ `g∘f: X→Z`."""
    F = alg["F"]
    Fm = [[np.zeros(alg["n"], dtype=np.int64) for _ in Y] for _ in X]
    Gm = [[np.zeros(alg["n"], dtype=np.int64) for _ in Z] for _ in Y]
    for (a, b, pos, c, o) in hlayout(alg, X, Y)[0]:
        if c:
            Fm[a][b][o:o + c] = fcv[pos:pos + c]
    for (b, c_, pos, c, o) in hlayout(alg, Y, Z)[0]:
        if c:
            Gm[b][c_][o:o + c] = gcv[pos:pos + c]
    H = [[np.zeros(alg["n"], dtype=np.int64) for _ in Z] for _ in X]
    for a in range(len(X)):
        for b in range(len(Y)):
            if not Fm[a][b].any():
                continue
            for c_ in range(len(Z)):
                if Gm[b][c_].any():
                    H[a][c_] = F.ADD[H[a][c_], amul(alg, Fm[a][b], Gm[b][c_])]
    lay, tot = hlayout(alg, X, Z)
    out = np.zeros(tot, dtype=np.int64)
    for (a, c_, pos, c, o) in lay:
        if c:
            out[pos:pos + c] = H[a][c_][o:o + c]
    return out


def identity_block(alg, i):
    """`End(P_i)` 의 항등원 — `e·x = x` 를 **선형 연립**으로 푼다(전수 불필요)."""
    F, c, o = alg["F"], alg["cnt"][(i, i)], alg["off"][(i, i)]
    rows, rhs = [], []
    for v in range(c):
        for w in range(c):
            rows.append([int(alg["MT"][o + u, o + v, o + w]) for u in range(c)])
            rhs.append(1 if v == w else 0)
    M = np.array([r + [F.NEG[b]] for r, b in zip(rows, rhs)], dtype=np.int64)
    ns = nullspace(F, M)
    sol = next(v for v in ns if v[c])
    e = np.zeros(alg["n"], dtype=np.int64)
    e[o:o + c] = F.MUL[F.INV[sol[c]], sol[:c]]
    return e


def _nilpotent(alg, v, c):
    w = v.copy()
    for _ in range(c + 1):
        w = amul(alg, w, v)
        if not w.any():
            return True
    return False


def rad_block(alg, i, j):
    """`rad ∩ Hom(P_i,P_j)` — i≠j 는 전체(Nakayama)·i=j 는 **여차원 1 초평면**.

    ★`End(P_i)` 는 국소이므로 `rad = ker λ`(λ = 유일한 대수 준동형 → GF(q))이고,
    각 기저 `b` 에 대해 `b − s·e` 가 멱영이 되는 **스칼라 s = λ(b) 하나**만 찾으면 된다
    (전수 `q^c` → `c·q`)."""
    key = ("rad", i, j)
    if key in alg.setdefault("_cache", {}):
        return alg["_cache"][key]
    F, c = alg["F"], alg["cnt"][(i, j)]
    if c == 0:
        out = np.zeros((0, 0), dtype=np.int64)
    elif i != j:
        out = np.eye(c, dtype=np.int64)
    else:
        o = alg["off"][(i, i)]
        e = identity_block(alg, i)
        rows = []
        for t in range(c):
            b = np.zeros(alg["n"], dtype=np.int64)
            b[o + t] = 1
            for sc in range(F.q):
                x = F.ADD[b, F.NEG[F.MUL[sc, e]]]
                if x.any() and _nilpotent(alg, x, c):
                    rows.append(list(x[o:o + c]))
                    break
                if not x.any():
                    break
        out = (rref(F, np.array(rows, dtype=np.int64))[0] if rows
               else np.zeros((0, c), dtype=np.int64))
    alg["_cache"][key] = out
    return out


def blk(alg, i, j, rows):
    out = []
    for r in rows:
        v = np.zeros(alg["n"], dtype=np.int64)
        v[alg["off"][(i, j)]:alg["off"][(i, j)] + alg["cnt"][(i, j)]] = r
        out.append(v)
    return out


def _spanmul(alg, i, j, left):
    F = alg["F"]
    B, piv, c = [], [], alg["cnt"][(i, j)]
    oj = alg["off"][(i, j)]
    for l in alg["names"]:
        for x in blk(alg, i, l, left[(i, l)]):
            for y in blk(alg, l, j, rad_block(alg, l, j)):
                _o, B, piv = rref_insert(F, B, piv,
                                         amul(alg, x, y)[oj:oj + c])
    return (np.array(B, dtype=np.int64) if len(B)
            else np.zeros((0, c), dtype=np.int64))


def rad_powers(alg):
    names = alg["names"]
    cur = {(i, j): rad_block(alg, i, j) for i in names for j in names}
    out = [sum(len(v) for v in cur.values())]
    while out[-1]:
        cur = {(i, j): _spanmul(alg, i, j, cur) for i in names for j in names}
        out.append(sum(len(v) for v in cur.values()))
    return out


def quiver_of(alg):
    F, names = alg["F"], alg["names"]
    R = {(i, j): rad_block(alg, i, j) for i in names for j in names}
    R2 = {(i, j): _spanmul(alg, i, j, R) for i in names for j in names}
    return {"%s->%s" % (i, j): len(R[(i, j)]) - len(R2[(i, j)])
            for i in names for j in names}


def idempotents(alg):
    """국소 `End(P_i)` 의 유일한 비영 멱등원 = 항등원(선형 연립으로 얻는다)."""
    return {i: identity_block(alg, i) for i in alg["names"]}


def cartan_of(alg):
    return [[alg["cnt"][(i, j)] for j in alg["names"]] for i in alg["names"]]


# ══════════════════════════════════════════════════════════════════════
# 2항 silting mutation
# ══════════════════════════════════════════════════════════════════════
def left_approx(alg, k):
    F, other = alg["F"], [i for i in alg["names"] if i != k]
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
                        F, B, piv, amul(alg, f, r)[okj:okj + cj])
        for t in range(cj):
            ok, B, piv = rref_insert(F, B, piv, unit(cj, t))
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
    F = alg["F"]
    Xm, X0, dX = Xc
    Ym, Y0, dY = Yc
    n1, n0 = hdim(alg, Xm, Ym), hdim(alg, X0, Y0)
    nq, nh = hdim(alg, Xm, Y0), hdim(alg, X0, Ym)
    M = np.zeros((n1 + n0, nq), dtype=np.int64)
    for u in range(n1):
        M[u] = F.NEG[compose(alg, Xm, Ym, Y0, dY, unit(n1, u))]
    for u in range(n0):
        M[n1 + u] = compose(alg, Xm, X0, Y0, unit(n0, u), dX)
    CM = (nullspace(F, M.T) if nq and (n1 + n0)
          else np.eye(n1 + n0, dtype=np.int64))
    HT = np.zeros((nh, n1 + n0), dtype=np.int64)
    for u in range(nh):
        h = unit(nh, u)
        HT[u, :n1] = compose(alg, Xm, X0, Ym, h, dX)
        HT[u, n1:] = compose(alg, X0, Ym, Y0, dY, h)
    return CM, HT, nq - rank(F, M), n1


def homK_minus(alg, Xc, Yc):
    F = alg["F"]
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
    return nh - rank(F, Mh)


def reps_of(F, CM, HT):
    B, piv, htb = [], [], []
    for r in HT:
        ok, B, piv = rref_insert(F, B, piv, r)
        if ok:
            htb.append(r)
    reps = []
    for z in CM:
        ok, B, piv = rref_insert(F, B, piv, z)
        if ok:
            reps.append(z)
    return htb, reps


def trivial_object(alg):
    return [([], [i], np.zeros(0, dtype=np.int64)) for i in alg["names"]]


def mutate(alg, k):
    E, f = left_approx(alg, k)
    return [(([k], E, f) if i == k
             else ([], [i], np.zeros(0, dtype=np.int64)))
            for i in alg["names"]], E


def end_algebra(alg, T):
    F, m = alg["F"], len(T)
    HTB, RP, LI, PL, MI, N1 = {}, {}, {}, {}, {}, {}
    for a in range(m):
        for b in range(m):
            cm, ht, pl, n1 = homK_data(alg, T[a], T[b])
            htb, reps = reps_of(F, cm, ht)
            HTB[(a, b)], RP[(a, b)], N1[(a, b)] = htb, reps, n1
            LI[(a, b)] = left_inverse(F, htb + reps)
            PL[(a, b)], MI[(a, b)] = pl, homK_minus(alg, T[a], T[b])
    C = [[len(RP[(a, b)]) for b in range(m)] for a in range(m)]
    cnt = {(a, b): C[a][b] for a in range(m) for b in range(m)}
    off, pos = {}, 0
    for a in range(m):
        for b in range(m):
            off[(a, b)] = pos
            pos += C[a][b]
    MT = np.zeros((pos, pos, pos), dtype=np.int64)
    for a in range(m):
        for b in range(m):
            for c in range(m):
                na, nb, nh = N1[(a, b)], N1[(b, c)], len(HTB[(a, c)])
                for s, u in enumerate(RP[(a, b)]):
                    for t, v in enumerate(RP[(b, c)]):
                        w = np.concatenate([
                            compose(alg, T[a][0], T[b][0], T[c][0],
                                    v[:nb], u[:na]),
                            compose(alg, T[a][1], T[b][1], T[c][1],
                                    v[nb:], u[na:])])
                        al = (F.mm(LI[(a, c)], w[:, None])[:, 0]
                              if LI[(a, c)].size else w[:0])
                        for q in range(C[a][c]):
                            if al[nh + q]:
                                MT[off[(a, b)] + s, off[(b, c)] + t,
                                   off[(a, c)] + q] = int(al[nh + q])
    return {"cartan": C, "dim": pos,
            "tilting": all(v == 0 for v in PL.values())
                       and all(v == 0 for v in MI.values()),
            "ext_pos": sum(PL.values()), "ext_neg": sum(MI.values()),
            "alg": pack(F, list(range(m)), cnt, MT)}


def op_algebra(alg):
    F, names = alg["F"], alg["names"]
    cnt2 = {(i, j): alg["cnt"][(j, i)] for i in names for j in names}
    off2, pos = {}, 0
    for i in names:
        for j in names:
            off2[(i, j)] = pos
            pos += cnt2[(i, j)]
    pi = np.zeros(alg["n"], dtype=np.int64)
    for i in names:
        for j in names:
            for t in range(alg["cnt"][(i, j)]):
                pi[alg["off"][(i, j)] + t] = off2[(j, i)] + t
    MT2 = np.zeros_like(alg["MT"])
    for u, v, w in zip(*np.nonzero(alg["MT"])):
        MT2[pi[v], pi[u], pi[w]] = alg["MT"][u, v, w]
    return pack(F, list(names), cnt2, MT2)


def mutate_step(alg, k, right):
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


# ══════════════════════════════════════════════════════════════════════
# 동형 판정 · Hochschild
# ══════════════════════════════════════════════════════════════════════
def arrow_lifts_of(alg):
    F = alg["F"]
    R = {(i, j): rad_block(alg, i, j)
         for i in alg["names"] for j in alg["names"]}
    R2 = {(i, j): _spanmul(alg, i, j, R)
          for i in alg["names"] for j in alg["names"]}
    out = []
    for i in alg["names"]:
        for j in alg["names"]:
            B, piv = [], []
            for r in R2[(i, j)]:
                _o, B, piv = rref_insert(F, B, piv, r)
            for r in R[(i, j)]:
                ok, B, piv = rref_insert(F, B, piv, r)
                if ok:
                    out.append((i, j, blk(alg, i, j, [r])[0]))
    return out, R2


def path_values(alg, ide, arrows):
    """★값이 0 인 단어도 기록해야 동형 판정이 닫힌다."""
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
    return words, np.array(vals, dtype=np.int64)


def find_isomorphism(A, B, cap=200000):
    F = A["F"]
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
            si, sj = s[A["names"].index(i)], s[A["names"].index(j)]
            Rr = rad_block(B, si, sj)
            Bq, pq = [], []
            for r in R2B[(si, sj)]:
                _o, Bq, pq = rref_insert(F, Bq, pq, r)
            cand = []
            for tup in itertools.product(range(F.q), repeat=len(Rr)):
                if not any(tup):
                    continue
                v = np.zeros(Rr.shape[1], dtype=np.int64)
                for t in range(len(Rr)):
                    if tup[t]:
                        v = F.ADD[v, F.MUL[tup[t], Rr[t]]]
                ok, _B2, _p2 = rref_insert(F, Bq, pq, v)
                if ok:
                    cand.append(blk(B, si, sj, [v])[0])
            opts.append(cand)
        # ★가지치기 — 화살 0..t 만 쓰는 단어들에 대해 well-defined 필요조건을 먼저 건다
        # (★화살 순서를 "닫힌 경로 우선"으로 재배열해 봤으나 A₆ p=3 을 못 풀고
        #  Q₈ 을 크게 느리게 만들어 **되돌렸다** — 실패한 휴리스틱)
        widx = [max(w, default=-1) for (_st, w) in WA]
        sub = [[u for u in range(len(WA)) if widx[u] <= t]
               for t in range(len(opts))]
        rkA = [rank(F, VA[sub[t]]) for t in range(len(opts))]
        st_hit = [None]

        def valB(assign, idxs):
            out = []
            for u in idxs:
                stt, w = WA[u]
                v = IB[s[A["names"].index(stt)]]
                for ai in w:
                    v = amul(B, v, assign[ai])
                out.append(v)
            return np.array(out, dtype=np.int64)

        def rec(assign, combo):
            nonlocal tried
            t = len(assign)
            if t == len(opts):
                tried += 1
                VB = valB(assign, range(len(WA)))
                if rank(F, VB) != B["n"]:
                    return None
                if rank(F, np.concatenate([VA, VB], axis=1)) == A["n"]:
                    return list(combo)
                return None
            for ci, cand in enumerate(opts[t]):
                if tried > cap:
                    st_hit[0] = True
                    return None
                a2 = assign + [cand]
                VBs = valB(a2, sub[t])
                tried += 1
                if rank(F, np.concatenate(
                        [VA[sub[t]], VBs], axis=1)) != rkA[t]:
                    continue                      # ★가지치기(필요조건 위반)
                r = rec(a2, combo + [ci])
                if r is not None:
                    return r
            return None

        got = rec([], [])
        if got is not None:
            arB = [o[c] for o, c in zip(opts, got)]
            VB = _wvals(A, B, IB, s, WA, arB)
            return {"found": True, "sigma": [str(x) for x in s],
                    "arrow_choice": got, "tried": tried,
                    "n_words": len(WA), "rank_VA": rank(F, VA),
                    "rank_VB": B["n"]}
        if st_hit[0]:
            return {"found": False, "tried": tried, "capped": True}
    return {"found": False, "tried": tried}


def _wv(A, B, IB, s, word, arB):
    stt, w = word
    v = IB[s[A["names"].index(stt)]]
    for ai in w:
        v = amul(B, v, arB[ai])
    return v


def _rmul_mat(alg, a):
    """★고정 원소 `a` 의 **우곱 행렬** `R_a[u,w] = Σ_v MT[u,v,w] a[v]`.

    `v ↦ v·a` 가 선형이므로 한 번 만들어 두면 곱이 `(1,n)·(n,n)` 하나로 끝난다."""
    F, n = alg["F"], alg["n"]
    d = alg.get("_MTtd")
    if d is None:
        d = F.DIG[np.ascontiguousarray(
            alg["MT"].transpose(1, 0, 2)).reshape(n, n * n)]
        alg["_MTtd"] = d
    ck = alg.setdefault("_Rc", {})            # ★같은 화살값은 계속 재등장한다
    key = a.tobytes()
    R = ck.get(key)
    if R is None:
        R = F.mmd(a[None, :], d).reshape(n, n)
        if len(ck) < 1024:
            ck[key] = R
    return R


def _wvals(A, B, IB, s, words, arB):
    """★단어값 **일괄** 계산 — 접두사 공유(트라이) + **화살별 일괄 행렬곱**.

    `_wv` 는 단어마다 멱등원부터 다시 곱해 같은 접두사를 몇 번이고 재계산하고,
    곱마다 `amul` 을 부른다. 여기서는 (a) 접두사를 캐시하고 (b) **같은 깊이·같은
    화살**을 쓰는 노드를 한 행렬로 쌓아 곱을 **한 번**에 끝낸다.
    결과는 `[_wv(..., w, arB) for w in words]` 와 **완전히 같다**(순수 최적화)."""
    F, n = B["F"], B["n"]
    idx = {nm: t for t, nm in enumerate(A["names"])}
    cache = {}
    for (stt, w) in words:
        cache.setdefault((stt,), IB[s[idx[stt]]])
    Rm, depth = {}, 1
    while True:
        pend = {}
        for (stt, w) in words:
            if len(w) < depth:
                continue
            key = (stt,) + tuple(w[:depth])
            if key not in cache:
                pend.setdefault(w[depth - 1], {})[key] = key[:-1]
        if not pend:
            break
        for ai, mp in pend.items():
            if ai not in Rm:
                Rm[ai] = _rmul_mat(B, arB[ai])
            ks = list(mp)
            W = F.mm(np.array([cache[mp[k]] for k in ks], dtype=np.int64),
                     Rm[ai])
            for t, k in enumerate(ks):
                cache[k] = W[t]
        depth += 1
    return np.array([cache[(stt,) + tuple(w)] for (stt, w) in words],
                    dtype=np.int64)


def rad_basis_piv(alg, i, j):
    F, c = alg["F"], alg["cnt"][(i, j)]
    if c == 0:
        return np.zeros((0, 0), dtype=np.int64), []
    if i != j:
        return np.eye(c, dtype=np.int64), list(range(c))
    Rr = rad_block(alg, i, i)
    if not len(Rr):
        return np.zeros((0, c), dtype=np.int64), []
    return rref(F, Rr)


def hh_struct(alg, cup=False, max_deg=2):
    """정규화 **상대** bar 복합체 `C^n = Hom_{E-E}(rad^{⊗_E n}, A)` — GF(q) 판."""
    F, names, cnt, off = alg["F"], alg["names"], alg["cnt"], alg["off"]

    def co(i, j, v):
        o = off[(i, j)]
        return list(v[o:o + cnt[(i, j)]])

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
                v[off[(i, j)]:off[(i, j)] + cnt[(i, j)]] = row
                RMAT[(i, j, t)] = v
                rmeta.append((i, j, t))
    nR = len(rmeta)

    def rco(i, j, cv):
        return [int(cv[c]) for c in RPIV[(i, j)]]

    pairs = [(a, b) for a in rmeta for b in rmeta if a[1] == b[0]]
    prodR = {(a, b): rco(a[0], b[1],
                         co(a[0], b[1], amul(alg, RMAT[a], RMAT[b])))
             for (a, b) in pairs}
    c0 = [(i, t) for i in names for t in range(cnt[(i, i)])]
    c1 = [(rk, w) for rk in rmeta for w in range(cnt[(rk[0], rk[1])])]
    c2 = [(a, b, w) for (a, b) in pairs for w in range(cnt[(a[0], b[1])])]
    # ★`max_deg < 2` 면 3-코사슬을 만들지 않는다(GF(q) rref 가 규모 밖일 때)
    trips = ([(a, b, c) for (a, b) in pairs for c in rmeta if b[1] == c[0]]
             if max_deg >= 2 else [])
    c3 = [(a, b, c, w) for (a, b, c) in trips
          for w in range(cnt[(a[0], c[1])])]
    i1 = {k: t for t, k in enumerate(c1)}
    i2 = {k: t for t, k in enumerate(c2)}
    i3 = {k: t for t, k in enumerate(c3)}

    D0 = np.zeros((len(c1), len(c0)), dtype=np.int64)
    for q, (m, ua) in enumerate(c0):
        for rk in rmeta:
            (i, j, _t) = rk
            if j == m:
                for w, val in enumerate(
                        co(i, m, amul(alg, RMAT[rk], ebas(m, m, ua)))):
                    D0[i1[(rk, w)], q] = F.ADD[D0[i1[(rk, w)], q], val]
            if i == m:
                for w, val in enumerate(
                        co(m, j, amul(alg, ebas(m, m, ua), RMAT[rk]))):
                    D0[i1[(rk, w)], q] = F.sub(D0[i1[(rk, w)], q], val)

    D1 = np.zeros((len(c2), len(c1)), dtype=np.int64)
    for (a, b) in pairs:
        i, m, j = a[0], a[1], b[1]
        base = i2[(a, b, 0)]
        for ua in range(cnt[(m, j)]):
            for w, val in enumerate(
                    co(i, j, amul(alg, RMAT[a], ebas(m, j, ua)))):
                if val:
                    D1[base + w, i1[(b, ua)]] = F.ADD[
                        D1[base + w, i1[(b, ua)]], val]
        for ua in range(cnt[(i, m)]):
            for w, val in enumerate(
                    co(i, j, amul(alg, ebas(i, m, ua), RMAT[b]))):
                if val:
                    D1[base + w, i1[(a, ua)]] = F.ADD[
                        D1[base + w, i1[(a, ua)]], val]
        for t2, val in enumerate(prodR[(a, b)]):
            if val:
                rk = (i, j, t2)
                for w in range(cnt[(i, j)]):
                    D1[base + w, i1[(rk, w)]] = F.sub(
                        D1[base + w, i1[(rk, w)]], val)

    D2 = np.zeros((len(c3), len(c2)), dtype=np.int8)   # ★메모리 8배 절감
    for (a, b, c) in trips:
        i, m1, m2, j = a[0], a[1], c[0], c[1]
        base = i3[(a, b, c, 0)]
        for ua in range(cnt[(m1, j)]):
            for w, val in enumerate(
                    co(i, j, amul(alg, RMAT[a], ebas(m1, j, ua)))):
                if val:
                    D2[base + w, i2[(b, c, ua)]] = F.ADD[
                        D2[base + w, i2[(b, c, ua)]], val]
        for t2, val in enumerate(prodR[(a, b)]):
            if val:
                rk = (i, m2, t2)
                for w in range(cnt[(i, j)]):
                    D2[base + w, i2[(rk, c, w)]] = F.sub(
                        D2[base + w, i2[(rk, c, w)]], val)
        for t2, val in enumerate(prodR[(b, c)]):
            if val:
                rk = (m1, j, t2)
                for w in range(cnt[(i, j)]):
                    D2[base + w, i2[(a, rk, w)]] = F.ADD[
                        D2[base + w, i2[(a, rk, w)]], val]
        for ua in range(cnt[(i, m2)]):
            for w, val in enumerate(
                    co(i, j, amul(alg, ebas(i, m2, ua), RMAT[c]))):
                if val:
                    D2[base + w, i2[(a, b, ua)]] = F.sub(
                        D2[base + w, i2[(a, b, ua)]], val)

    Z1 = nullspace(F, D1) if len(c2) else np.eye(len(c1), dtype=np.int64)
    k0 = len(nullspace(F, D0)) if len(c1) else len(c0)
    k1 = len(Z1)
    out = {"dim_A": alg["n"], "dim_rad": nR,
           "C": [len(c0), len(c1), len(c2), len(c3)],
           "HH0": k0, "HH1": k1 - (len(c0) - k0), "max_deg": max_deg}
    if max_deg < 2:
        out["ker"] = [k0, k1]
        return out
    # ★차원만 필요하므로 가장 큰 D2 는 **rank 만** 구한다
    # (p=2 는 비트평면 가속 · 그 외는 일반 rref)
    if len(c3):
        k2 = len(c2) - (rank_packed(F, D2) if F.p == 2
                        else rank(F, D2.astype(np.int64)))
    else:
        k2 = len(c2)
    out["ker"] = [k0, k1, k2]
    out["HH2"] = k2 - (len(c1) - k1)
    if not cup:
        return out

    Bb, pv = [], []
    for q in range(D0.shape[1]):
        _o, Bb, pv = rref_insert(F, Bb, pv, D0[:, q])
    reps = []
    for z in Z1:
        ok, Bb, pv = rref_insert(F, Bb, pv, z)
        if ok:
            reps.append(z)
    B2b, p2 = [], []
    for q in range(D1.shape[1]):
        _o, B2b, p2 = rref_insert(F, B2b, p2, D1[:, q])

    def val1(fv, rk):
        i, j = rk[0], rk[1]
        v = np.zeros(alg["n"], dtype=np.int64)
        for w in range(cnt[(i, j)]):
            v[off[(i, j)] + w] = fv[i1[(rk, w)]]
        return v

    def cup11(fv, gv):
        v = np.zeros(len(c2), dtype=np.int64)
        for (a, b) in pairs:
            i, j = a[0], b[1]
            P = amul(alg, val1(fv, a), val1(gv, b))
            base = i2[(a, b, 0)]
            for w, cc in enumerate(co(i, j, P)):
                if cc:
                    v[base + w] = F.ADD[v[base + w], cc]
        return v

    cocycle_ok, comm_ok, prods = True, True, {}
    for x in range(len(reps)):
        for y in range(len(reps)):
            u = cup11(reps[x], reps[y])
            prods[(x, y)] = u
            if len(c3) and F.mm(D2.astype(np.int64), u[:, None]).any():
                cocycle_ok = False
    for x in range(len(reps)):
        for y in range(x, len(reps)):
            ok, _B, _p = rref_insert(
                F, list(B2b) if isinstance(B2b, list) else B2b.copy(),
                list(p2), F.ADD[prods[(x, y)], prods[(y, x)]])
            if ok:
                comm_ok = False
    Cb = B2b.copy() if not isinstance(B2b, list) else list(B2b)
    cp = list(p2)
    span0 = len(cp)
    for x in range(len(reps)):
        for y in range(len(reps)):
            _o, Cb, cp = rref_insert(F, Cb, cp, prods[(x, y)])
    out.update({"HH1_reps": len(reps), "cup_rank": len(cp) - span0,
                "cup_is_cocycle": cocycle_ok, "graded_commutative": comm_ok})
    return out


# ══════════════════════════════════════════════════════════════════════
# 실현화 → GF(q) 구조상수
# ══════════════════════════════════════════════════════════════════════
def algebra_table_realified(F, names, HOM, Jact, d):
    """★실현화된 𝔽_p Hom 공간에서 **GF(q) 구조상수**를 뽑는다.

    스칼라 `J`(중심)는 Hom 위에 `φ ↦ J∘φ` 로 작용하므로, `φ` 를 고르고 `J^t∘φ` 를
    건너뛰는 **탐욕 GF(q)-기저**를 만든 뒤 `[φ; Jφ; …]` 의 좌역행렬로 좌표를 읽는다."""
    p, k = F.p, F.k
    Fp = GF(p)
    B, LIN, cnt = {}, {}, {}
    for i in names:
        for j in names:
            Rb, piv = [], []
            basis, rows = [], []
            for M in HOM[(i, j)]:
                v = (np.array(M, dtype=np.int64) % p)
                ok, Rb, piv = rref_insert(Fp, Rb, piv, v.reshape(-1))
                if not ok:
                    continue
                fam = [v]
                for _ in range(k - 1):
                    fam.append((Jact[j] @ fam[-1]) % p)
                for w in fam[1:]:
                    _o, Rb, piv = rref_insert(Fp, Rb, piv, w.reshape(-1))
                basis.append(fam)
                rows.extend([w.reshape(-1) for w in fam])
            B[(i, j)] = basis
            cnt[(i, j)] = len(basis)
            # ★좌역행렬(2304 열 RREF)은 병목 — **pivot 열만 뽑아 정사각 역행렬**로 대체
            if rows:
                Sm = np.array(rows, dtype=np.int64)
                _R, pv = rref(Fp, Sm.copy())
                LIN[(i, j)] = (list(pv), inv_sq(Fp, Sm[:, pv]))
            else:
                LIN[(i, j)] = ([], np.zeros((0, 0), dtype=np.int64))
    meta, off, pos = [], {}, 0
    for i in names:
        for j in names:
            off[(i, j)] = pos
            meta.extend([(i, j, t) for t in range(cnt[(i, j)])])
            pos += cnt[(i, j)]
    MT = np.zeros((pos, pos, pos), dtype=np.int64)
    for u, (i, j, t) in enumerate(meta):
        for v, (j2, l, s) in enumerate(meta):
            if j2 != j:
                continue
            P = (B[(j, l)][s][0] @ B[(i, j)][t][0]) % p     # b∘a
            pv, Mi = LIN[(i, l)]
            al = (P.reshape(-1)[pv] @ Mi) % p if pv else np.zeros(0, dtype=np.int64)
            for w in range(cnt[(i, l)]):
                e = sum(int(al[k * w + r]) * p ** r for r in range(k))
                if e:
                    MT[u, v, off[(i, l)] + w] = e
    _ = d
    return pack(F, names, cnt, MT)


# ══════════════════════════════════════════════════════════════════════
# ★★동형 판정 — **층별 successive lifting**(레벨 1 열거 + 이후 선형 연립)
# ══════════════════════════════════════════════════════════════════════
def rad_layers(alg):
    """`rad^m` 의 블록별 기저 목록 `[rad¹, rad², …]`(마지막은 0)."""
    names = alg["names"]
    cur = {(i, j): rad_block(alg, i, j) for i in names for j in names}
    out = [cur]
    while any(len(v) for v in cur.values()):
        cur = {(i, j): _spanmul(alg, i, j, cur) for i in names for j in names}
        out.append(cur)
    return out


def _quot_basis(F, big, small, blkdim):
    """`big/small` 의 **여공간 기저**(= 잉여공간의 기저 리프트)."""
    B, piv = [], []
    for r in small:
        _o, B, piv = rref_insert(F, B, piv, r)
    out = []
    for r in big:
        ok, B, piv = rref_insert(F, B, piv, r)
        if ok:
            out.append(r)
    return out


def _gl_mats(F, m):
    """`GL_m(GF q)` 전수."""
    for tup in itertools.product(range(F.q), repeat=m * m):
        M = np.array(tup, dtype=np.int64).reshape(m, m)
        if rank(F, M.copy()) == m:
            yield M


def diag_scale_is_auto(alg, lam):
    """★블록 등급 대수에서 `(i,j) ↦ λ_j/λ_i` 스케일이 **자기동형**인지 실제로 확인한다.

    이론상 자동이지만(경로가 telescoping) 가정을 코드로 검증한다."""
    F, names = alg["F"], alg["names"]
    sc = np.ones(alg["n"], dtype=np.int64)
    for i in names:
        for j in names:
            c, o = alg["cnt"][(i, j)], alg["off"][(i, j)]
            v = F.MUL[lam[j], F.INV[lam[i]]]
            for t in range(c):
                sc[o + t] = v

    def ap(x):
        return F.MUL[sc, x]

    for u in range(alg["n"]):
        for v in range(alg["n"]):
            lhs = ap(amul(alg, unit(alg["n"], u), unit(alg["n"], v)))
            rhs = amul(alg, ap(unit(alg["n"], u)), ap(unit(alg["n"], v)))
            if not np.array_equal(lhs, rhs):
                return False
    return True


def _spanning_blocks(bkeys, names):
    """정점 그래프의 **신장나무** 간선마다 블록 하나 — 몫 정규화 대상."""
    seen, tree = {names[0]}, []
    rest = list(bkeys)
    changed = True
    while changed:
        changed = False
        for bk in list(rest):
            a, b = bk
            if (a in seen) != (b in seen):
                seen.add(a)
                seen.add(b)
                tree.append(bk)
                rest.remove(bk)
                changed = True
    return tree


def _rad_glob(alg, layers):
    """`rad^m` 의 **전역**(블록 합) 기저 — `RAD[m] = layers[m-1]`, `RAD[L+1] = 0`."""
    out = [None]
    for m in range(1, len(layers) + 1):
        rows = []
        for (i, j), rs in layers[m - 1].items():
            rows += blk(alg, i, j, list(rs))
        out.append(rows)
    return out


def _codim(F, vs, mod):
    """`span(mod ∪ vs)` 의 `span(mod)` 위 여차원."""
    if not vs:
        return 0
    r0 = rank(F, np.array(mod, dtype=np.int64)) if mod else 0
    return rank(F, np.array(list(mod) + list(vs), dtype=np.int64)) - r0


def _elt_inv(alg, RAD, v):
    """★`rad/rad²` 원소의 **대수동형 불변량**(스칼라배·rad² 대표 선택에 불변).

    `v·rad^k` 와 `rad^k·v` 가 `rad^m`(`m ≥ k+2`) 위에서 갖는 차원만 쓴다 —
    대표를 `v + r`(`r ∈ rad²`)로 바꾸면 변화가 `rad^{k+2}` 안이라 값이 안 변하고,
    `αv` 로 스케일해도 span 이 같다. ⟹ **선(line) 위의 함수**이며 동형으로 보존된다."""
    F, out = alg["F"], []
    for k in (1, 2):
        if k >= len(RAD):
            break
        Lv = [amul(alg, b, v) for b in RAD[k]]
        Rv = [amul(alg, v, b) for b in RAD[k]]
        for mm in range(k + 2, len(RAD)):
            out.append(_codim(F, Lv, RAD[mm]))
            out.append(_codim(F, Rv, RAD[mm]))
    if len(RAD) > 1:
        Tw = [amul(alg, amul(alg, b, v), c) for b in RAD[1] for c in RAD[1]]
        for mm in range(4, len(RAD)):
            out.append(_codim(F, Tw, RAD[mm]))
    return tuple(out)


def _line_inv_table(alg, RAD, basis, cap=4096):
    """블록의 `rad/rad²` 기저에 대해 **선마다** 불변량 표 — 키는 정규화 계수."""
    F, m = alg["F"], len(basis)
    if m == 0 or F.q ** m > cap:
        return None
    tab = {}
    for c in itertools.product(range(F.q), repeat=m):
        t0 = next((t for t, x in enumerate(c) if x), None)
        if t0 is None or c[t0] != 1:
            continue                          # 사영 대표(첫 비영 = 1)만
        w = np.zeros(alg["n"], dtype=np.int64)
        for t, ct in enumerate(c):
            if ct:
                w = F.ADD[w, F.MUL[ct, basis[t]]]
        tab[c] = _elt_inv(alg, RAD, w)
    return tab


def _order_arrows_by_rarity(alg, RAD, arrows):
    """★소스 화살 기저를 **드문 불변량 류부터** 쓰도록 재선택.

    화살은 `rad/rad²` 의 기저 **선택**일 뿐이라 바꿔도 무방한데, 드문 류의 선을 먼저
    쓰면 그 행의 상(像) 후보가 그만큼 좁아진다 — ★가지치기 효율이 **기저 선택**에 달려 있다."""
    F, byblk = alg["F"], {}
    for (i, j, v) in arrows:
        byblk.setdefault((i, j), []).append(v)
    out = []
    for (i, j) in sorted(byblk):
        bas = byblk[(i, j)]
        tab = _line_inv_table(alg, RAD, bas) if len(bas) > 1 else None
        if tab is None:
            out += [(i, j, v) for v in bas]
            continue
        size = {}
        for iv in tab.values():
            size[iv] = size.get(iv, 0) + 1
        chosen, Bm, piv = [], [], []
        for c in sorted(tab, key=lambda c: (size[tab[c]], c)):
            ok, Bm, piv = rref_insert(F, Bm, piv,
                                      np.array(c, dtype=np.int64))
            if not ok:
                continue
            w = np.zeros(alg["n"], dtype=np.int64)
            for t, ct in enumerate(c):
                if ct:
                    w = F.ADD[w, F.MUL[ct, bas[t]]]
            chosen.append(w)
            if len(chosen) == len(bas):
                break
        out += [(i, j, v) for v in chosen]
    return out


def _line_key(F, row):
    """계수행 → 선 키(첫 비영을 1 로 정규화). 0 행이면 None."""
    t0 = next((t for t, x in enumerate(row) if x), None)
    if t0 is None:
        return None
    return tuple(int(F.MUL[F.INV[int(row[t0])], int(x)]) for x in row)


def _scalar_class_reps(F, mats):
    """`GL_m` 원소를 **스칼라 배 동치류 대표**로 줄인다(몫 정규화)."""
    out, seen = [], set()
    for M in mats:
        key = None
        for c in range(1, F.q):
            K = tuple(F.MUL[c, M].reshape(-1).tolist())
            if key is None or K < key:
                key = K
        if key not in seen:
            seen.add(key)
            out.append(M)
    return out


def iso_lift(A, B, cap=2000000, level1_cap=4000000,
             quotient=True, line_prune=True):
    """★`A ≅ B` 판정 — **레벨 1(rad/rad²)만 열거**하고 이후는 **선형 연립**으로 올린다.

    `φ` 를 `J^m` 을 법으로 알고 있을 때 보정 `δ ∈ J^m` 을 더하면 단어값 변화가
    **`δ` 에 선형**이다(`δ·δ ∈ J^{2m} ⊆ J^{m+1}`) ⟹ 열거는 레벨 1 뿐이다.
    반환에 `level1_space`(레벨 1 후보 곱)를 항상 넣어 **왜 되고/안 되는지**를 수치로 남긴다."""
    F = A["F"]
    IA, IB = idempotents(A), idempotents(B)
    arA, _r2 = arrow_lifts_of(A)
    WA, VA = path_values(A, IA, arA)
    KA = nullspace(F, VA.T)                      # ★A 쪽 관계(단어들의 선형 종속)
    CA, CB = cartan_of(A), cartan_of(B)
    nA = len(A["names"])
    sig = [s for s in itertools.permutations(B["names"])
           if all(CA[i][j] == CB[B["names"].index(s[i])][B["names"].index(s[j])]
                  for i in range(nA) for j in range(nA))]
    layers = rad_layers(B)
    L = len(layers) - 1                          # J^{L+1} = 0
    info = {"level1_space": None, "sigmas": len(sig), "n_words": len(WA),
            "n_relations": len(KA), "loewy": L, "quotient": quotient,
            "line_prune": line_prune}
    # ★선 불변량 — A 쪽 화살값은 σ 와 무관하므로 **한 번만** 잰다
    RA = _rad_glob(A, rad_layers(A))
    RB = _rad_glob(B, layers)
    invA = None
    if line_prune:
        arA = _order_arrows_by_rarity(A, RA, arA)   # ★기저부터 다시 고른다
        WA, VA = path_values(A, IA, arA)
        KA = nullspace(F, VA.T)
        invA = [_elt_inv(A, RA, v) for (_i, _j, v) in arA]
    tried = 0
    for s in sig:
        # ── 레벨 1: **블록별 `GL_m`** 열거(유도사상이 가역이어야 한다) ──
        blocks, blk_of = {}, []
        for t, (i, j, _v) in enumerate(arA):
            si, sj = s[A["names"].index(i)], s[A["names"].index(j)]
            blocks.setdefault((si, sj), []).append(t)
            blk_of.append((si, sj))
        qb, bkeys = {}, sorted(blocks)
        bad = False
        for bk in bkeys:
            Q = _quot_basis(F, layers[0][bk], layers[1][bk], B["cnt"][bk])
            if len(Q) != len(blocks[bk]):        # 화살 다중도 불일치 ⟹ 비동형
                bad = True
                break
            qb[bk] = [blk(B, bk[0], bk[1], [r])[0] for r in Q]
        if bad:
            continue
        gls = [list(_gl_mats(F, len(blocks[bk]))) for bk in bkeys]
        if line_prune:
            # ★★선 불변량 정합 — 동형은 `rad/rad²` 의 선을 **같은 불변량의 선**으로
            #   보내야 한다. 궤도를 자르는 것이 아니라 **불가능한 상(像)을 지우는**
            #   것이므로 완전성이 보존된다(무효화 시 `line_prune=False` 로 대조).
            n_pruned = []
            for bi, bk in enumerate(bkeys):
                tab = _line_inv_table(B, RB, qb[bk])
                if tab is None:
                    n_pruned.append((str(bk), len(gls[bi]), len(gls[bi])))
                    continue
                want = [invA[t] for t in blocks[bk]]
                keep = [M for M in gls[bi]
                        if all(tab.get(_line_key(F, M[k])) == want[k]
                               for k in range(len(want)))]
                n_pruned.append((str(bk), len(gls[bi]), len(keep)))
                gls[bi] = keep
            info["line_prune_per_block"] = n_pruned
        if quotient:
            # ★대각 스케일 몫 — 신장나무 간선 블록만 스칼라류 대표로
            tree = set(_spanning_blocks(bkeys, B["names"]))
            gls = [_scalar_class_reps(F, g) if bk in tree else g
                   for bk, g in zip(bkeys, gls)]
        space = 1
        for g in gls:
            space *= max(1, len(g))
        info["level1_space"] = space
        info["level1_per_block"] = [(str(bk), len(blocks[bk]), len(g))
                                    for bk, g in zip(bkeys, gls)]
        if space > level1_cap:
            info["capped_level1"] = True
            return dict(info, found=False)
        # ── 보정 자유도: 각 화살마다 J^m 블록 기저 ───────────────────
        # ★후보가 적은 블록부터 — 가지치기가 일찍 먹는다
        order = sorted(range(len(bkeys)), key=lambda t: len(gls[t]))
        arrows_upto = []
        acc = set()
        for t in order:
            acc |= set(blocks[bkeys[t]])
            arrows_upto.append(set(acc))
        widx = [set(w) for (_st, w) in WA]

        def _assign(sel):
            cur = [np.zeros(B["n"], dtype=np.int64)] * len(arA)
            cur = list(cur)
            for pos_, bi in enumerate(order[:len(sel)]):
                bk = bkeys[bi]
                M = gls[bi][sel[pos_]]
                for k, t in enumerate(blocks[bk]):
                    v = np.zeros(B["n"], dtype=np.int64)
                    for r in range(len(qb[bk])):
                        if M[k, r]:
                            v = F.ADD[v, F.MUL[int(M[k, r]), qb[bk][r]]]
                    cur[t] = v
            return cur

        # ★★노드 비용 절감 — 깊이/층에만 의존하는 것은 **캐시**하고
        #   단어값은 **바뀐 화살을 포함하는 행만** 갱신한다(순수 최적화·결과 불변)
        dcache, bcache = {}, {}

        def _depth_data(d_):
            if d_ in dcache:
                return dcache[d_]
            allow = arrows_upto[d_]
            idxs = [u for u in range(len(WA)) if widx[u] <= allow]
            Ks = nullspace(F, VA[idxs].T)
            cont = {t: [r for r, u in enumerate(idxs) if t in widx[u]]
                    for t in allow}
            dcache[d_] = (allow, idxs, [WA[u] for u in idxs], Ks, cont)
            return dcache[d_]

        def _basis(d_, m):
            if (d_, m) in bcache:
                return bcache[(d_, m)]
            allow = arrows_upto[d_]
            bs = []
            for t, (si, sj) in enumerate(blk_of):
                if t not in allow:
                    continue
                for r in (layers[m][(si, sj)] if m < len(layers) else []):
                    bs.append((t, blk(B, si, sj, [r])[0]))
            bcache[(d_, m)] = bs
            return bs

        def _vals(sub, work):
            return _wvals(A, B, IB, s, sub, work)

        def _try(cur, d_):
            """깊이 `d_` 의 단어 부분집합에서 층별 lifting 이 성공하는가."""
            allow, idxs, sub, Ks, cont = _depth_data(d_)
            work = list(cur)
            VB = _vals(sub, work)
            for m in range(1, L + 1):
                bs = _basis(d_, m)
                res = (F.mm(Ks, VB).reshape(-1) if len(Ks)
                       else np.zeros(0, dtype=np.int64))
                if not res.any():
                    continue
                if not bs:
                    return None
                cols = []
                for (t, d) in bs:
                    rows = cont[t]
                    if not rows:
                        cols.append(np.zeros_like(res))
                        continue
                    sav = work[t]
                    work[t] = F.ADD[sav, d]
                    # ★그 화살을 쓰는 행만 갱신하고, **차분만** Ks 에 곱한다
                    #   `Ks V₂ − Ks V_B = Ks[:, rows] (V₂ − V_B)[rows]`
                    dv = F.ADD[_wvals(A, B, IB, s, [sub[r] for r in rows],
                                      work), F.NEG[VB[rows]]]
                    work[t] = sav
                    cols.append(F.mm(Ks[:, rows], dv).reshape(-1))
                sol = _solve(F, np.array(cols, dtype=np.int64), F.NEG[res])
                if sol is None:
                    return None
                for t2, (t, d) in enumerate(bs):
                    if sol[t2]:
                        work[t] = F.ADD[work[t], F.MUL[sol[t2], d]]
                VB = _vals(sub, work)
            return work

        found_combo = [None]

        def rec1(sel):
            nonlocal tried
            d_ = len(sel)
            if d_ == len(order):
                return sel
            for ci in range(len(gls[order[d_]])):
                tried += 1
                if tried > cap:
                    return "CAP"
                s2 = sel + [ci]
                if _try(_assign(s2), d_) is None:
                    continue          # ★부분 필요조건 위반 — 가지치기
                r = rec1(s2)
                if r == "CAP":
                    return "CAP"
                if r is not None:
                    return r
            return None

        got1 = rec1([])
        if got1 == "CAP":
            return dict(info, found=False, capped=True, tried=tried)
        if got1 is None:
            continue
        combo = [0] * len(bkeys)
        for pos_, bi in enumerate(order):
            combo[bi] = got1[pos_]
        for _once in (0,):
            cur = _assign(got1)
            ok = True
            for m in range(1, L + 1):            # J^m 보정으로 J^{m+1} 조건 맞추기
                basis, offs = [], []
                for t, (si, sj) in enumerate(blk_of):
                    rows = layers[m][(si, sj)] if m < len(layers) else []
                    offs.append(len(basis))
                    for r in rows:
                        basis.append((t, blk(B, si, sj, [r])[0]))
                res = _residual(A, B, IB, s, WA, KA, cur)
                if not res.any():
                    continue                     # 이미 만족
                cols = []
                for (t, d) in basis:
                    trial = list(cur)
                    trial[t] = F.ADD[trial[t], d]
                    cols.append(F.ADD[_residual(A, B, IB, s, WA, KA, trial),
                                      F.NEG[res]])
                if not cols:
                    ok = False
                    break
                Msys = np.array(cols, dtype=np.int64)
                sol = _solve(F, Msys, F.NEG[res])
                if sol is None:
                    ok = False
                    break
                for t2, (t, d) in enumerate(basis):
                    if sol[t2]:
                        cur[t] = F.ADD[cur[t], F.MUL[sol[t2], d]]
            if not ok:
                continue
            if _residual(A, B, IB, s, WA, KA, cur).any():
                continue
            VB = _wvals(A, B, IB, s, WA, cur)
            if rank(F, VB) != B["n"]:
                continue
            return dict(info, found=True, sigma=[str(x) for x in s],
                        arrow_choice=list(combo), tried=tried,
                        rank_VA=rank(F, VA), rank_VB=B["n"])
    return dict(info, found=False, tried=tried)


def _residual(A, B, IB, s, WA, KA, arB):
    """관계 `KA` 를 B 쪽 단어값에 먹인 잔차 — 0 이면 well-defined."""
    F = A["F"]
    VB = _wvals(A, B, IB, s, WA, arB)
    if not len(KA):
        return np.zeros(0, dtype=np.int64)
    return F.mm(KA, VB).reshape(-1)


def _solve(F, cols, rhs):
    """`Σ x_t cols[t] = rhs` 의 한 해(없으면 None)."""
    m = len(cols)
    Aug = np.concatenate([np.array(cols, dtype=np.int64).T,
                          rhs.reshape(-1, 1)], axis=1)
    R, piv = rref(F, Aug)
    if m in piv:
        return None
    x = np.zeros(m, dtype=np.int64)
    for r, c in zip(R, piv):
        x[c] = r[m]
    return x
