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

    def add(self, a, b):
        return self.ADD[a, b]

    def sub(self, a, b):
        return self.ADD[a, self.NEG[b]]

    def mul(self, a, b):
        return self.MUL[a, b]

    def mm(self, A, B):
        """행렬곱."""
        n, m = A.shape[0], B.shape[1]
        R = np.zeros((n, m), dtype=np.int64)
        for t in range(A.shape[1]):
            R = self.ADD[R, self.MUL[A[:, t][:, None], B[t, :][None, :]]]
        return R


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


def amul(alg, x, y):
    F = alg["F"]
    r = np.zeros(alg["n"], dtype=np.int64)
    for u in np.nonzero(x)[0]:
        r = F.ADD[r, F.MUL[int(x[u]), F.mm(y[None, :], alg["MT"][u])[0]]]
    return r


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
            VB = np.array([_wv(A, B, IB, s, WA[u], arB) for u in range(len(WA))],
                          dtype=np.int64)
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

    D2 = np.zeros((len(c3), len(c2)), dtype=np.int64)
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
    k2 = len(nullspace(F, D2)) if len(c3) else len(c2)
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
            if len(c3) and F.mm(D2, u[:, None]).any():
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
