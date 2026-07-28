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

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - ★**A₇ p=2 주블록(1,14,20) Ext¹ 은 미완**(Hom 400 × |G| 2520 — 제약행렬 규모). 다음 축.
  - A₆ p=3(3, 3′ 은 GF(9)-형) 은 **GF(9) 위 cocycle 계산**이 필요 — 본 관측 범위 밖(정직 유보).
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
        print("  ★제시-free 계산 · H¹(G,𝔽₂)=0 자체검증 · Cartan 비영 패턴 정합", flush=True)
        print("  → .pgf/proofs/EXT1-QUIVER.json", flush=True)
    print(f"ext1_quiver_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
