#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""loewy_series_observe — ★**사영 덮개 P(S) 명시 구성 → Loewy 급수** (관측, seal 아님).
[[a6_cartan_p23_observe]]·[[a7_cartan_p2_observe]](분해행렬 D·Cartan C)와
[[ext1_quiver_observe]](Ext¹ 퀴버)가 만든 **세 산출물이 서로를 검증**하는 층.

★**방법 = 원시 멱등원 분해 없이 사영가군을 직접 만든다**(자체유도 규율):
  (i) **|H| 가 p 와 서로소면 k[G/H] 는 사영** — A₆ p=2 의 Sylow-3(위수 9)에서 **dim 40** 치환가군.
  (ii) **정칙가군 kG 를 우측곱 자기준동형(End_G(kG) = kG)의 Fitting 분해**로 쪼갠다 —
       임의 원소 a ∈ kG 의 우측곱 R_a 에 대해 M = R_a^{|M|} 로 ker ⊕ im 분해를 반복.
       ★사영자 e 를 함께 나르면 각 조각의 자기준동형 대수가 **e·kG·e** 로 유지된다.
  (iii) **rad(M) = ∩ ker(M → S)** — J(kG) 를 구성하지 않고 **이미 가진 simple 들로** 계산.
  (iv) **사영성 판정(Higman/Chouinard)**: Y 가 사영 ⟺ Y|_{Syl_p} 가 자유 ⟺
       **dim Y^{Syl_p} = dim Y / |Syl_p|** — p-군의 유일한 단순가군이 자명이므로 socle 이 고정점.

관측 7축(전 산술 GF(2) 정확 — numpy 정수·부동소수 없음):
  A. ★**차원 산술 게이트(분해체 진술)**: 확정된 Cartan 로부터 **dim P(S_i) = Σ_j C_{ji}·dim S_j** ·
     ★**|G|_p 가 dim P(S_i) 를 나눈다** · **Σ_i dim P(S_i)·dim S_i = 블록 차원** ·
     **전 블록 합 = |G|** — A₆ p=2(232+128) · A₆ p=3(279+81) · A₇ p=2(주 2088 + 비주 432 = 2520)
     **4 블록 동시 정합**. 선행 3 관측의 Cartan 를 **한 번에** 교차검증한다.
  B. ★**P(1̂) = 𝔽₂[A₆/Syl₃] 명시 구성**(dim 40) — 사영성 판정 통과 · head = soc = 1̂.
  C. ★★**정칙가군 𝔽₂A₆ 완전 분해**: **17 성분 = {40×1, 24×4, 24×4, 16×8}** ·
     ★**중복도가 dim S 와 일치**(1, 4, 4) ⟹ **주블록에서 End(S) = 𝔽₂**(분해됨).
  D. ★★**𝔽₂ 는 A₆ 의 분해체가 아니다**: defect-0 부분이 **16차원 단순가군 1개(End = 𝔽₄)**로
     나온다 — 분해체 𝔽₄ 위의 **{8}, {8} 두 블록이 𝔽₂ 위에서 융합**. 8 × 16 = 128 = 64 + 64 로
     A 축 산술과 정합. ★**주블록은 𝔽₂ 위에서 이미 분해됨**(C 축) — 필드 의존이 블록마다 다르다.
  E. ★**세 PIM 의 완전 Loewy 급수**(전부 **Loewy 길이 9**·**회문**):
       P(1̂)  : 1 / 4ₐ⊕4_b / 1² / 4ₐ⊕4_b / 1² / 4ₐ⊕4_b / 1² / 4ₐ⊕4_b / 1
       P(4ₐ) : 4ₐ / 1 / 4_b / 1 / 4ₐ / 1 / 4_b / 1 / 4ₐ   ← ★**단열(uniserial)**
       P(4_b): 4_b / 1 / 4ₐ / 1 / 4_b / 1 / 4ₐ / 1 / 4_b   ← ★**단열**
     ★**층 다중도 총합 = Cartan 열** 전수((8,4,4) · (4,3,2) · (4,2,3)) — C 의 **독립 재유도**.
  F. ★★**rad P(S_i)/rad² P(S_i) ≅ ⊕_j S_j^{dim Ext¹(S_i,S_j)}** 전수 —
     퀴버 **[[0,1,1],[1,0,0],[1,0,0]]** 의 **제3 독립 대조**(D·C·Ext¹ 삼중 교차검증 완성).
     추가로 **head = soc = S**(대칭대수 ⟹ P(S) 는 사영 덮개이자 단사 덮개) 전수 실측.

  G. ★★**A₇ p=2 — 6 PIM 전부·자기고리 독립 검증**: 정칙가군(2520차원)을 쓰지 않고
     **지수 크기 사영 운반자** k[G/H](|H| 홀수) 3종으로 간다 —
     **F₂₁ = C₇⋊C₃(지수 120)** · **Syl₃(지수 280)** · **C₇(지수 360)**.
     ★**Frobenius 상호율 `m_S = dim S^H` 로 성분을 먼저 예측**하고(`Σ_S m_S·dim P(S) = [G:H]`
     세 운반자 전부 성립 — dim P 6개를 **동시에** 검증) **Hecke 대수 `End_G(k[G/H]) ≅ X^H`**
     의 멱등원으로 분해(예측↔실측 중복도 대조가 게이트).
     결과 **6 PIM 전부**(72·64·56·24·24·40) — 전부 **Loewy 길이 5**·회문·head = soc = S ·
     ★**층 총합 = Cartan 열 6개 전부**(두 블록) · ★**rad/rad² = Ext¹ 행 6개 전부**(두 퀴버).
     ★★**P(14̂) = 14̂ / 1̂⊕14̂ / 20̂ / 1̂ / 14̂** — **2층에 14̂ 자신**이 나타난다 ⟹
     선행 관측의 **자기고리 Ext¹(14̂,14̂) = 1 을 독립 산출물이 확인**(A₆ 에서는 자기고리가
     없어 자명했던 대조가 여기서 비자명해진다) · 자기고리는 **14̂ 에만**.
     ★**𝔽₂ 는 A₇ 의 분해체다**(6 simple 전부 End = 𝔽₂ · Σ dim P·dim S = 2520 = |A₇|) —
     **D 축의 A₆ 와 정반대**. ★**A₆ LL = 9 vs A₇ LL = 5**(둘 다 defect group 위수 8).

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - A 축의 산술은 **분해체 위의 진술**이다(A₆ p=3 의 3, 3′ 도 End = GF(9) 이므로 𝔽₃ 위에서는
    융합한다 — G 축 [[ext1_quiver_observe]] 참조). D 축이 그 필드 의존을 실측한 것.
  - 16차원 성분의 **단순성**은 rad = 0 과 dim End = 2 로 판정한다(분해불가 + 반단순 ⟹ 단순).
  - 화살의 **관계식**(퀴버 대수 제시)은 여전히 본 관측 밖 — 층과 개수까지가 산출.

사용: python -m qf_witness.observe.loewy_series_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import random
import itertools

import numpy as np

from qf_witness.observe.ext1_quiver_observe import (
    enumerate_group, extend_action, fano_gl42_gens, heart_gens, rref_rows)


# ══════════════════════════════════════════════════════════════════════════
# GF(p) 선형대수
# ══════════════════════════════════════════════════════════════════════════
def nullspace(A, p):
    """A x = 0 의 해공간 기저(행 벡터)."""
    cols = A.shape[1]
    B, piv = rref_rows(A.copy(), p)
    pset = set(piv)
    out = []
    for f in (c for c in range(cols) if c not in pset):
        x = np.zeros(cols, dtype=np.int64)
        x[f] = 1
        for i, c in enumerate(piv):
            x[c] = (-int(np.dot(B[i], x))) % p
        out.append(x)
    return np.array(out, dtype=np.int64) if out else np.zeros((0, cols), dtype=np.int64)


def inv_gf(M, p):
    n = len(M)
    B, piv = rref_rows(np.concatenate([M % p, np.eye(n, dtype=np.int64)], axis=1), p)
    if piv[:n] != list(range(n)):
        raise ValueError("비가역")
    return B[:, n:] % p


def image_basis(M, p):
    """열공간 기저(행 벡터)."""
    B, _ = rref_rows(M.T.copy() % p, p)
    return B


def _pack2(A):
    """GF(2) 행렬 → uint64 비트팩(열 방향, little-endian)."""
    r, c = A.shape
    W = (c + 63) // 64
    B = np.zeros((r, W * 64), dtype=np.uint8)
    B[:, :c] = (A & 1).astype(np.uint8)
    return np.ascontiguousarray(np.packbits(B, axis=1, bitorder="little")).view(np.uint64)


def nullspace_gf2(A):
    """★GF(2) 전용 비트팩 nullspace — Hom 계산의 병목(수천 열)을 위한 고속 경로.
    generic nullspace 와 **같은 부분공간**을 준다(기저 선택도 동일 규약: free 열마다 1개)."""
    rows, cols = A.shape
    P = _pack2(A)
    nr = P.shape[0]
    piv, r = [], 0
    for c in range(cols):
        w, b = c >> 6, np.uint64(c & 63)
        col = (P[r:, w] >> b) & np.uint64(1)
        nz = np.nonzero(col)[0]
        if not len(nz):
            continue
        pr = r + int(nz[0])
        if pr != r:
            P[[r, pr]] = P[[pr, r]]
        allc = (P[:, w] >> b) & np.uint64(1)
        allc[r] = 0
        idx = np.nonzero(allc)[0]
        if len(idx):
            P[idx] ^= P[r]
        piv.append(c)
        r += 1
        if r == nr:
            break
    pset = set(piv)
    out = []
    for f in (c for c in range(cols) if c not in pset):
        x = np.zeros(cols, dtype=np.int64)
        x[f] = 1
        fw, fb = f >> 6, np.uint64(f & 63)
        for i, c in enumerate(piv):
            x[c] = int((P[i, fw] >> fb) & np.uint64(1))
        out.append(x)
    return np.array(out, dtype=np.int64) if out else np.zeros((0, cols), dtype=np.int64)


def hom_space(actA, actB, dA, dB, gens, p):
    """Hom_G(A,B) 기저 — φ(dB×dA) 로 φ·A(g) = B(g)·φ (생성원만으로 충분)."""
    rows = []
    for g in gens:
        A, B = actA[g] % p, actB[g] % p
        rows.append((np.kron(np.eye(dB, dtype=np.int64), A.T)
                     - np.kron(B, np.eye(dA, dtype=np.int64))) % p)
    M = np.concatenate(rows, axis=0) % p
    N = nullspace_gf2(M) if p == 2 else nullspace(M, p)
    return [v.reshape(dB, dA) % p for v in N]


def restrict(M, Br, piv, p):
    """불변부분공간(RREF 행기저 Br·pivot piv)에 M 제한 — 좌표 행렬."""
    d = len(Br)
    img = (Br @ M.T) % p
    C = np.zeros((d, d), dtype=np.int64)
    for r in range(d):
        v = img[r].copy()
        for i, c in enumerate(piv):
            if v[c]:
                C[i, r] = int(v[c]) % p
                v = (v - int(v[c]) * Br[i]) % p
        if v.any():
            raise ValueError("불변 부분공간 아님")
    return C % p


def submodule_action(act, gens, basisrows, p):
    """부분가군의 생성원 작용 행렬."""
    Br, piv = rref_rows(basisrows.copy(), p)
    return {g: restrict(act[g], Br, piv, p) for g in gens}, Br


def fixed_dim(act, elems, d, p):
    """dim M^H — H = elems 가 생성하는 부분군의 고정점."""
    return len(nullspace(np.concatenate(
        [(act[g] - np.eye(d, dtype=np.int64)) % p for g in elems], axis=0), p))


# ══════════════════════════════════════════════════════════════════════════
# 사영가군 구성 · 분해 · Loewy 급수
# ══════════════════════════════════════════════════════════════════════════
def subgroup(gens_of_H, mulf, idp):
    S, fr = {idp}, [idp]
    while fr:
        nf = []
        for x in fr:
            for s in gens_of_H:
                y = mulf(x, s)
                if y not in S:
                    S.add(y)
                    nf.append(y)
        fr = nf
    return sorted(S)


def coset_data(ordG, mulf, idp, gensG, Hlist):
    """k[G/H] — 좌잉여류 치환표현(대표·전 원소 치환·생성원 행렬)."""
    Hs = set(Hlist)
    cos, reps = {}, []
    for g in ordG:
        key = frozenset(mulf(g, h) for h in Hs)
        if key not in cos:
            cos[key] = len(reps)
            reps.append(g)
    idx = {g: cos[frozenset(mulf(g, h) for h in Hs)] for g in ordG}
    n = len(reps)
    perms = {g: [idx[mulf(g, r)] for r in reps] for g in ordG}
    mats = []
    for x in gensG:
        M = np.zeros((n, n), dtype=np.int64)
        for j in range(n):
            M[perms[x][j], j] = 1
        mats.append(M)
    return n, reps, perms, mats


def coset_perm_module(ordG, mulf, idp, gensG, Hlist, p):
    """k[G/H] — 좌잉여류 치환가군의 생성원 행렬."""
    n, _reps, _perms, mats = coset_data(ordG, mulf, idp, gensG, Hlist)
    return n, mats


def hecke_endos(n, perms, Hlist, reps):
    """★End_G(k[G/H]) 완전 기저 — φ_w(gH) = g·w 이고 w 는 **H-궤도 합**(X^H 기저).
    Frobenius 상호율 End_G(Ind_H^G k) ≅ (Ind_H^G k)^H 의 구성적 판본 —
    정칙가군(|G|차원)을 만들지 않고 자기준동형 대수를 **지수 크기**에서 얻는다."""
    seen, orbits = set(), []
    for j in range(n):
        if j in seen:
            continue
        orb = {perms[h][j] for h in Hlist}
        seen |= orb
        orbits.append(sorted(orb))
    mats = []
    for orb in orbits:
        M = np.zeros((n, n), dtype=np.int64)
        for j in range(n):
            pj = perms[reps[j]]
            for t in orb:
                M[pj[t], j] ^= 1
        mats.append(M % 2)
    return mats


def fitting_split(g, p):
    """g^(2^k ≥ d) 의 ker / im — Fitting 분해(반복제곱)."""
    d = len(g)
    gp = g % p
    k = 1
    while k < d:
        gp = (gp @ gp) % p
        k *= 2
    return nullspace(gp, p), image_basis(gp, p)


def decompose_regular(B, E, rand_endo, p, rng, out, tries=40):
    """span(B) 를 분해 — E = 앙비언트 사영자(각 조각의 대수를 e·A·e 로 유지)."""
    Br, piv = rref_rows(B.copy(), p)
    d = len(Br)
    if d == 0:
        return
    W = Br.T % p
    for _ in range(tries):
        g = restrict((E @ rand_endo() % p @ E) % p, Br, piv, p)
        K, I = fitting_split(g, p)
        if not (0 < len(K) < d):
            continue
        Q = np.concatenate([I, K], axis=0).T % p
        Qi = inv_gf(Q, p)
        D = np.zeros((d, d), dtype=np.int64)
        for i in range(len(I)):
            D[i, i] = 1
        e_loc = (Q @ D % p @ Qi) % p
        C = np.zeros((d, len(E)), dtype=np.int64)
        for i, c in enumerate(piv):
            C[i, c] = 1
        EI = (W @ e_loc % p @ C % p @ E) % p
        EK = (W @ ((np.eye(d, dtype=np.int64) - e_loc) % p) % p @ C % p @ E) % p
        decompose_regular((I @ Br) % p, EI, rand_endo, p, rng, out, tries)
        decompose_regular((K @ Br) % p, EK, rand_endo, p, rng, out, tries)
        return
    out.append(Br)


def quotient_action(act, gens, Nrows, d, p):
    """M/N — N 의 RREF pivot 열을 소거한 좌표계의 작용."""
    Nb, piv = rref_rows(Nrows.copy(), p)
    free = [c for c in range(d) if c not in set(piv)]
    q = len(free)
    out = {}
    for g in gens:
        A = act[g] % p
        C = np.zeros((q, q), dtype=np.int64)
        for j, f in enumerate(free):
            v = A[:, f].copy() % p
            for i, c in enumerate(piv):
                if v[c]:
                    v = (v - int(v[c]) * Nb[i]) % p
            C[:, j] = v[free] % p
        out[g] = C
    return out, q


def socle_series(act, d, gens, simples, p, maxlen=30):
    """socle 여과의 층 다중도 — **아래에서 위로**(soc(M), soc(M/soc), …).
    rigid 판정용: radical 급수와 (뒤집어) 같으면 rigid."""
    cur, dcur, layers = act, d, []
    for _ in range(maxlen):
        homs, mult = [], []
        for (_nm, actS, dS) in simples:
            Hs = hom_space(actS, cur, dS, dcur, gens, p)      # Hom(S, M)
            mult.append(len(Hs))
            homs.extend(Hs)
        layers.append(tuple(mult))
        if not homs:
            break
        soc = rref_rows(np.concatenate([h.T for h in homs], axis=0) % p, p)[0]
        if len(soc) >= dcur:
            break
        cur, dcur = quotient_action(cur, gens, soc, dcur, p)
    return layers


def loewy_series(act, d, gens, simples, p, maxlen=30):
    """radical 여과의 층 다중도 목록 — rad(M) = ∩ ker(M → S)."""
    cur, dcur, layers = act, d, []
    for _ in range(maxlen):
        homs, mult = [], []
        for (nm, actS, dS) in simples:
            Hs = hom_space(cur, actS, dcur, dS, gens, p)
            mult.append(len(Hs))
            homs.extend(Hs)
        layers.append(tuple(mult))
        if not homs:
            break
        rad = nullspace(np.concatenate(homs, axis=0) % p, p)
        if len(rad) == 0 or len(rad) == dcur:
            break
        cur, _ = submodule_action(cur, gens, rad, p)
        dcur = len(rad)
    return layers


# ══════════════════════════════════════════════════════════════════════════
# A 축 데이터 — 선행 관측이 확정한 Cartan(분해체 위)
# ══════════════════════════════════════════════════════════════════════════
BLOCKS = {
    "A6_p2_principal": {"G": 360, "p": 2, "pp": 8, "dims": [1, 4, 4],
                        "names": ["1̂", "4ₐ", "4_b"],
                        "C": [[8, 4, 4], [4, 3, 2], [4, 2, 3]]},
    "A6_p3_principal": {"G": 360, "p": 3, "pp": 9, "dims": [1, 4, 3, 3],
                        "names": ["1̂", "4", "3", "3′"],
                        "C": [[5, 4, 1, 1], [4, 5, 2, 2], [1, 2, 2, 1], [1, 2, 1, 2]]},
    "A7_p2_principal": {"G": 2520, "p": 2, "pp": 8, "dims": [1, 14, 20],
                        "names": ["1̂", "14̂", "20̂"],
                        "C": [[4, 2, 2], [2, 3, 1], [2, 1, 2]]},
    "A7_p2_nonprincipal": {"G": 2520, "p": 2, "pp": 8, "dims": [4, 4, 6],
                           "names": ["4̂", "4̄̂", "6̂"],
                           "C": [[2, 1, 2], [1, 2, 2], [2, 2, 4]]},
}
# defect-0 블록(분해체 위) — 블록당 simple 1개·C=[1] ⟹ dim P = dim S
DEFECT0 = {"A6_p2": [8, 8], "A6_p3": [9], "A7_p2": []}


def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "loewy-series/v1",
           "_note": ("사영 덮개 P(S) 명시 구성 → Loewy 급수 — D·Cartan·Ext¹ 삼중 교차검증. "
                     "관측·seal 아님·module 0·root 불변.")}

    # ── A. 차원 산술 게이트 ──────────────────────────────────────────────
    ax = {}
    for key, b in BLOCKS.items():
        dims, Cm = b["dims"], b["C"]
        nb = len(dims)
        dimP = [sum(Cm[j][i] * dims[j] for j in range(nb)) for i in range(nb)]
        ax[key] = {"dim_P": dimP,
                   "block_dim": sum(dimP[i] * dims[i] for i in range(nb))}
        R[f"A_{key}_ppart_divides"] = all(d % b["pp"] == 0 for d in dimP)
    R["A_A6_p2_dimP"] = (ax["A6_p2_principal"]["dim_P"] == [40, 24, 24])
    R["A_A7_p2_dimP"] = (ax["A7_p2_principal"]["dim_P"] == [72, 64, 56]
                         and ax["A7_p2_nonprincipal"]["dim_P"] == [24, 24, 40])
    R["A_A6_p3_dimP"] = (ax["A6_p3_principal"]["dim_P"] == [27, 36, 18, 18])
    tot6_2 = ax["A6_p2_principal"]["block_dim"] + sum(d * d for d in DEFECT0["A6_p2"])
    tot6_3 = ax["A6_p3_principal"]["block_dim"] + sum(d * d for d in DEFECT0["A6_p3"])
    tot7_2 = (ax["A7_p2_principal"]["block_dim"]
              + ax["A7_p2_nonprincipal"]["block_dim"])
    R["A_A6_p2_sums_to_360"] = (tot6_2 == 360)
    R["A_A6_p3_sums_to_360"] = (tot6_3 == 360)
    R["A_A7_p2_sums_to_2520"] = (tot7_2 == 2520)
    out["A_dimension_arithmetic"] = {
        "per_block": ax,
        "totals": {"A6_p2": tot6_2, "A6_p3": tot6_3, "A7_p2": tot7_2},
        "identities": ("dim P(S_i) = Σ_j C_{ji}·dim S_j · |G|_p | dim P(S_i) · "
                       "Σ_i dim P(S_i)·dim S_i = 블록차원 · 전 블록 합 = |G|"),
        "scope": "★분해체 위의 진술 — 𝔽₂/𝔽₃ 위에서는 융합이 일어난다(D 축)",
    }

    # ── A₆ 준비 ─────────────────────────────────────────────────────────
    A6G = [(1, 2, 0, 3, 4, 5), (0, 1, 2, 4, 5, 3), (1, 0, 3, 2, 4, 5)]
    mul6, id6, ord6 = enumerate_group(A6G, 6)
    R["setup_A6_360"] = (len(ord6) == 360)
    triv = extend_action(A6G, mul6, id6, [np.eye(1, dtype=np.int64)] * 3, 2, ord6)
    act4b = extend_action(A6G, mul6, id6, heart_gens(A6G, 6, 2), 2, ord6)
    act4a = extend_action(A6G, mul6, id6,
                          fano_gl42_gens(None, 7, [tuple(list(g) + [6]) for g in A6G]),
                          2, ord6)
    simples = [("1", triv, 1), ("4_a", act4a, 4), ("4_b", act4b, 4)]
    syl2 = subgroup([(1, 0, 3, 2, 4, 5), (2, 3, 0, 1, 4, 5), (0, 1, 3, 2, 5, 4)],
                    mul6, id6)
    R["B_syl2_order8"] = (len(syl2) == 8)
    syl3 = subgroup([(1, 2, 0, 3, 4, 5), (0, 1, 2, 4, 5, 3)], mul6, id6)
    R["B_syl3_order9"] = (len(syl3) == 9)

    # ── B. P(1̂) = 𝔽₂[A₆/Syl₃] ──────────────────────────────────────────
    n40, mats40 = coset_perm_module(ord6, mul6, id6, A6G, syl3, 2)
    R["B_cosets_40"] = (n40 == 40)
    act40 = extend_action(A6G, mul6, id6, mats40, 2, ord6)
    R["B_projective_higman"] = (fixed_dim(act40, syl2, n40, 2) == n40 // 8)
    hd40 = [len(hom_space(act40, aS, n40, dS, A6G, 2)) for _, aS, dS in simples]
    sc40 = [len(hom_space(aS, act40, dS, n40, A6G, 2)) for _, aS, dS in simples]
    R["B_head_is_trivial"] = (hd40 == [1, 0, 0])
    R["B_soc_is_trivial"] = (sc40 == [1, 0, 0])
    L40 = loewy_series(act40, n40, A6G, simples, 2)
    R["B_loewy_length_9"] = (len(L40) == 9)
    out["B_P1_from_coset_module"] = {
        "construction": "P(1̂) = 𝔽₂[A₆/Syl₃(위수 9)] — |H| 가 p 와 서로소 ⟹ 사영",
        "dim": n40, "head": hd40, "soc": sc40,
        "projectivity_test": "Higman/Chouinard: dim Y^{Syl₂} = dim Y/8",
    }

    # ── C·D·E·F. 정칙가군 𝔽₂A₆ 완전 분해 ────────────────────────────────
    if not quick:
        pos = {g: i for i, g in enumerate(ord6)}
        nG = len(ord6)
        Lmats = []
        for x in A6G:
            M = np.zeros((nG, nG), dtype=np.int64)
            for j, g in enumerate(ord6):
                M[pos[mul6(x, g)], j] = 1
            Lmats.append(M)
        actReg = extend_action(A6G, mul6, id6, Lmats, 2, ord6)
        Rmul = {}
        for x in ord6:
            M = np.zeros((nG, nG), dtype=np.int64)
            for j, g in enumerate(ord6):
                M[pos[mul6(g, x)], j] = 1
            Rmul[x] = M
        rng = random.Random(3)                       # 결정론 시드

        def rand_endo():
            M = np.zeros((nG, nG), dtype=np.int64)
            for x in rng.sample(ord6, 12):
                M = (M + Rmul[x]) % 2
            return M

        parts = []
        decompose_regular(np.eye(nG, dtype=np.int64), np.eye(nG, dtype=np.int64),
                          rand_endo, 2, rng, parts)
        dimlist = sorted(len(b) for b in parts)
        R["C_regular_splits_17"] = (len(parts) == 17)
        R["C_dim_multiset"] = (dimlist == [16] * 8 + [24] * 8 + [40])
        R["C_dims_sum_360"] = (sum(dimlist) == 360)
        # 성분 식별
        summ, big16 = {}, None
        series = {}
        for B in sorted(parts, key=len):
            d = len(B)
            actY, _ = submodule_action(actReg, A6G, B, 2)
            hd = tuple(len(hom_space(actY, aS, d, dS, A6G, 2)) for _, aS, dS in simples)
            summ[(d, hd)] = summ.get((d, hd), 0) + 1
            if hd == (0, 0, 0) and big16 is None:
                big16 = (B, actY, d)
            if hd != (0, 0, 0) and (d, hd) not in series:
                sc = tuple(len(hom_space(aS, actY, dS, d, A6G, 2))
                           for _, aS, dS in simples)
                series[(d, hd)] = (loewy_series(actY, d, A6G, simples, 2), sc,
                                   fixed_dim(extend_action(
                                       A6G, mul6, id6, [actY[g] for g in A6G], 2, ord6),
                                       syl2, d, 2))
        R["C_multiplicity_equals_dim"] = (
            summ.get((40, (1, 0, 0))) == 1 and summ.get((24, (0, 1, 0))) == 4
            and summ.get((24, (0, 0, 1))) == 4 and summ.get((16, (0, 0, 0))) == 8)
        out["C_regular_decomposition"] = {
            "parts": len(parts), "dims": dimlist,
            "summary": {f"dim{d}/head{list(h)}": c for (d, h), c in sorted(summ.items())},
            "reading": ("𝔽₂A₆ = P(1̂) ⊕ P(4ₐ)^4 ⊕ P(4_b)^4 ⊕ (16차원)^8 — "
                        "★주블록 중복도(1,4,4)가 dim S 와 일치 ⟹ End(S) = 𝔽₂(분해됨)"),
        }

        # D. 16차원 성분 = 융합 단순가군(End = 𝔽₄)
        B16, act16, d16 = big16
        e16 = len(hom_space(act16, act16, d16, d16, A6G, 2))
        s4 = simples + [("16", act16, d16)]
        homs16 = []
        for (_nm, aS, dS) in s4:
            homs16.extend(hom_space(act16, aS, d16, dS, A6G, 2))
        rad16 = len(nullspace(np.concatenate(homs16, axis=0) % 2, 2))
        R["D_16dim_End_is_GF4"] = (e16 == 2)
        R["D_16dim_radical_zero"] = (rad16 == 0)
        R["D_16dim_x8_is_128"] = (8 * d16 == 128 == sum(d * d for d in DEFECT0["A6_p2"]))
        out["D_field_of_definition"] = {
            "finding": ("★𝔽₂ 는 A₆(p=2)의 분해체가 아니다 — 분해체 𝔽₄ 위의 defect-0 블록 "
                        "{8},{8} 이 𝔽₂ 위에서 **16차원 단순가군 1개(End = 𝔽₄)** 로 융합"),
            "evidence": {"dim": d16, "dim_End": e16, "rad": rad16,
                         "multiplicity": 8, "8x16": 8 * d16},
            "consistency": "8 × 16 = 128 = 8² + 8² — A 축의 분해체 산술과 정합",
            "contrast": ("★주블록은 𝔽₂ 위에서 이미 분해됨(C 축 중복도 1,4,4) — "
                         "필드 의존이 **블록마다 다르다**"),
            "cross_ref": ("A₆ p=3 의 3, 3′ 도 End = GF(9)(ext1_quiver_observe G축) ⟹ "
                          "𝔽₃ 위에서는 6차원으로 융합 — 같은 현상"),
        }

        # E·F. Loewy 급수 + Cartan 열 재유도 + Ext¹ 대조
        EXT1 = {(40, (1, 0, 0)): (0, 1, 1),          # 퀴버 행: 1̂ · 4ₐ · 4_b
                (24, (0, 1, 0)): (1, 0, 0),
                (24, (0, 0, 1)): (1, 0, 0)}
        CART = {(40, (1, 0, 0)): (8, 4, 4),          # Cartan 열
                (24, (0, 1, 0)): (4, 3, 2),
                (24, (0, 0, 1)): (4, 2, 3)}
        pim = {}
        ok_len, ok_pal, ok_cart, ok_ext, ok_hs, ok_proj = [], [], [], [], [], []
        for (d, hd), (lay, sc, fx) in sorted(series.items()):
            tot = tuple(sum(l[i] for l in lay) for i in range(3))
            ok_len.append(len(lay) == 9)
            ok_pal.append(lay == lay[::-1])
            ok_cart.append(tot == CART[(d, hd)])
            ok_ext.append(tuple(lay[1]) == EXT1[(d, hd)])
            ok_hs.append(hd == sc)
            ok_proj.append(fx == d // 8)
            pim[f"P{list(hd)}"] = {
                "dim": d, "head": list(hd), "soc": list(sc),
                "loewy_layers": [list(l) for l in lay],
                "loewy_length": len(lay),
                "composition_total": list(tot),
                "cartan_column": list(CART[(d, hd)]),
                "rad_over_rad2": list(lay[1]),
                "ext1_row": list(EXT1[(d, hd)]),
                "uniserial": all(sum(l) == 1 for l in lay),
            }
        R["E_all_loewy_length_9"] = all(ok_len)
        R["E_all_palindromic"] = all(ok_pal)
        R["E_composition_equals_cartan_column"] = all(ok_cart)
        R["E_P4a_P4b_uniserial"] = (pim["P[0, 1, 0]"]["uniserial"]
                                    and pim["P[0, 0, 1]"]["uniserial"])
        R["E_P1_not_uniserial"] = (not pim["P[1, 0, 0]"]["uniserial"])
        R["F_rad_over_rad2_equals_ext1"] = all(ok_ext)
        R["F_head_equals_soc"] = all(ok_hs)
        R["F_all_projective"] = all(ok_proj)
        out["E_loewy_series"] = {
            "pims": pim,
            "features": ("★전부 Loewy 길이 9·회문 · ★P(4ₐ)·P(4_b) 는 **단열(uniserial)** · "
                         "P(1̂) 만 층 4ₐ⊕4_b 로 비단열 · "
                         "★층 다중도 총합 = Cartan 열(C 의 독립 재유도)"),
        }
        out["F_triple_cross_check"] = {
            "identity": "rad P(S_i)/rad² P(S_i) ≅ ⊕_j S_j^{dim Ext¹(S_i,S_j)}",
            "quiver": [[0, 1, 1], [1, 0, 0], [1, 0, 0]],
            "verified": all(ok_ext),
            "meaning": ("분해행렬 D(→Cartan C) · Ext¹ 퀴버 · Loewy 급수 — "
                        "**세 독립 산출물이 서로를 검증**"),
            "symmetric_algebra": "head P(S) = soc P(S) = S 전수 실측",
        }

    # ── G. A₇ p=2 — 지수 크기 운반자 3종으로 6 PIM 전부 ──────────────────
    if not quick:
        from qf_witness.observe.ext1_quiver_observe import (
            fano_gl42_gens as _fano, inv_mod as _inv, build_a7_principal_gens)
        A7G = [(1, 2, 0, 3, 4, 5, 6), (1, 2, 3, 4, 5, 6, 0)]
        mul7, id7, ord7 = enumerate_group(A7G, 7)
        R["G_A7_2520"] = (len(ord7) == 2520)
        g4 = _fano(None, 7, A7G)
        g4b = [np.array(np.transpose(_inv(m, 2)), dtype=np.int64) % 2 for m in g4]

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
        prn = build_a7_principal_gens(A7G)
        raw7 = {"1": ([np.eye(1, dtype=np.int64)] * 2, 1), "4": (g4, 4),
                "4b": (g4b, 4), "6": ([_w2(m) for m in g4], 6),
                "14": prn["14"], "20": prn["20"]}
        N7 = ["1", "4", "4b", "6", "14", "20"]
        S7 = {k: (extend_action(A7G, mul7, id7, gm, 2, ord7), d)
              for k, (gm, d) in raw7.items()}
        syl2_7 = subgroup([(1, 2, 3, 0, 5, 4, 6), (2, 1, 0, 3, 5, 4, 6)], mul7, id7)
        R["G_A7_syl2_order8"] = (len(syl2_7) == 8)
        # ★End(S) = 𝔽₂ 전수 ⟹ 𝔽₂ 는 A₇ 의 분해체(A₆ 와 대조)
        endS = {k: len(hom_space(a, a, d, d, A7G, 2)) for k, (a, d) in S7.items()}
        R["G_A7_all_End_are_F2"] = all(v == 1 for v in endS.values())
        dimP7 = {"1": 72, "4": 24, "4b": 24, "6": 40, "14": 64, "20": 56}
        R["G_A7_regular_dim_2520"] = (
            sum(dimP7[k] * S7[k][1] for k in N7) == 2520)
        CART7 = {"1": (4, 0, 0, 0, 2, 2), "14": (2, 0, 0, 0, 3, 1),
                 "20": (2, 0, 0, 0, 1, 2), "4": (0, 2, 1, 2, 0, 0),
                 "4b": (0, 1, 2, 2, 0, 0), "6": (0, 2, 2, 4, 0, 0)}
        EXT7 = {"1": (0, 0, 0, 0, 1, 1), "14": (1, 0, 0, 0, 1, 0),
                "20": (1, 0, 0, 0, 0, 0), "4": (0, 0, 0, 1, 0, 0),
                "4b": (0, 0, 0, 1, 0, 0), "6": (0, 1, 1, 0, 0, 0)}
        CARRIERS = {
            "F21": ([(1, 2, 3, 4, 5, 6, 0), (0, 2, 4, 6, 1, 3, 5)], 21, 120),
            "Syl3": ([(1, 2, 0, 3, 4, 5, 6), (0, 1, 2, 4, 5, 3, 6)], 9, 280),
            "C7": ([(1, 2, 3, 4, 5, 6, 0)], 7, 360),
        }
        simples7 = [(k, S7[k][0], S7[k][1]) for k in N7]
        carr, pim7 = {}, {}
        frob_ok, mult_ok, proj_ok = [], [], []
        for cn, (hg, ho, idxn) in CARRIERS.items():
            Hl = subgroup(hg, mul7, id7)
            mS = {k: fixed_dim(a, Hl, d, 2) for k, (a, d) in S7.items()}
            pred = sum(dimP7[k] * mS[k] for k in N7)
            frob_ok.append(len(Hl) == ho and pred == idxn
                           and len(ord7) // len(Hl) == idxn)
            n_, reps_, perms_, mats_ = coset_data(ord7, mul7, id7, A7G, Hl)
            actX = extend_action(A7G, mul7, id7, mats_, 2, ord7)
            proj_ok.append(fixed_dim(actX, syl2_7, n_, 2) == n_ // 8)
            alg = hecke_endos(n_, perms_, Hl, reps_)
            rng7 = random.Random(7)                  # 결정론 시드

            def _rnd(alg=alg, rng7=rng7, n_=n_):
                M = np.zeros((n_, n_), dtype=np.int64)
                for A_ in rng7.sample(alg, max(2, len(alg) // 3)):
                    M = (M + A_) % 2
                return M

            ps = []
            decompose_regular(np.eye(n_, dtype=np.int64),
                              np.eye(n_, dtype=np.int64), _rnd, 2, rng7, ps)
            got = {}
            for B in sorted(ps, key=len):
                d = len(B)
                actY, _ = submodule_action(actX, A7G, B, 2)
                hd = tuple(len(hom_space(actY, aS, d, dS, A7G, 2))
                           for _, aS, dS in simples7)
                nm = next((k for i, k in enumerate(N7)
                           if hd == tuple(1 if j == i else 0 for j in range(6))), None)
                got[nm] = got.get(nm, 0) + 1
                if nm is None or nm in pim7:
                    continue
                sc = tuple(len(hom_space(aS, actY, dS, d, A7G, 2))
                           for _, aS, dS in simples7)
                lay = loewy_series(actY, d, A7G, simples7, 2)
                soc_l = socle_series(actY, d, A7G, simples7, 2)
                tot = tuple(sum(l[i] for l in lay) for i in range(6))
                pim7[nm] = {"dim": d, "head": list(hd), "soc": list(sc),
                            "loewy_layers": [list(l) for l in lay],
                            "socle_layers": [list(l) for l in soc_l],
                            "rigid": (list(lay) == list(soc_l)[::-1]),
                            "palindromic": (list(lay) == list(lay)[::-1]),
                            "loewy_length": len(lay),
                            "composition_total": list(tot),
                            "cartan_column": list(CART7[nm]),
                            "rad_over_rad2": list(lay[1]),
                            "ext1_row": list(EXT7[nm]),
                            "uniserial": all(sum(l) == 1 for l in lay),
                            "carrier": cn}
            mult_ok.append(all(got.get(k, 0) == mS[k] for k in N7))
            carr[cn] = {"index": idxn, "hecke_dim": len(alg),
                        "frobenius_m_S": mS, "parts": len(ps),
                        "dims": sorted(len(b) for b in ps),
                        "identified": {k: v for k, v in sorted(
                            got.items(), key=lambda t: (t[0] is None, t[0]))}}
        R["G_frobenius_predicts_index"] = all(frob_ok)
        R["G_carriers_projective"] = all(proj_ok)
        R["G_multiplicity_matches_frobenius"] = all(mult_ok)
        R["G_all_six_pims_found"] = (sorted(pim7) == sorted(N7))
        R["G_dims_match"] = all(pim7[k]["dim"] == dimP7[k] for k in N7)
        R["G_head_equals_soc"] = all(pim7[k]["head"] == pim7[k]["soc"] for k in N7)
        R["G_all_loewy_length_5"] = all(pim7[k]["loewy_length"] == 5 for k in N7)
        # ★예측 수정: "전부 회문"은 **반증**됐다 — P(14̂) 만 비회문이자 비-rigid
        R["G_palindromic_except_14"] = (
            [k for k in N7 if not pim7[k]["palindromic"]] == ["14"])
        R["G_rigid_except_14"] = ([k for k in N7 if not pim7[k]["rigid"]] == ["14"])
        # 자기쌍대(head=soc=S·대칭대수) ⟹ socle 층(아래→위) = radical 층(위→아래) 원소별 일치
        R["G_socle_layers_match_radical"] = all(
            pim7[k]["socle_layers"] == pim7[k]["loewy_layers"] for k in N7)
        R["G_rigid_iff_palindromic"] = all(
            pim7[k]["rigid"] == pim7[k]["palindromic"] for k in N7)
        R["G_composition_equals_cartan_column"] = all(
            pim7[k]["composition_total"] == pim7[k]["cartan_column"] for k in N7)
        R["G_rad_over_rad2_equals_ext1"] = all(
            pim7[k]["rad_over_rad2"] == pim7[k]["ext1_row"] for k in N7)
        # ★★자기고리 독립 검증: P(14̂) 의 2층에 14̂ 자신이 나타난다
        R["G_selfloop_14_confirmed"] = (
            pim7["14"]["rad_over_rad2"][N7.index("14")] == 1)
        R["G_selfloop_unique"] = ([k for k in N7
                                   if pim7[k]["rad_over_rad2"][N7.index(k)]] == ["14"])
        R["G_A7_LL5_vs_A6_LL9"] = (all(pim7[k]["loewy_length"] == 5 for k in N7)
                                   and R.get("E_all_loewy_length_9", False))
        out["G_A7_p2_loewy"] = {
            "carriers": carr,
            "method": ("정칙가군(2520차원) 대신 **지수 크기 사영 운반자** k[G/H](|H| 홀수) — "
                       "★Frobenius 상호율 m_S = dim S^H 로 성분을 **미리 예측**하고 "
                       "Hecke 대수 End_G = X^H 의 멱등원으로 분해(예측↔실측 대조가 게이트)"),
            "pims": pim7,
            "End_S": endS,
            "splitting_field": ("★**𝔽₂ 는 A₇(p=2)의 분해체다** — 6 simple 전부 End = 𝔽₂ 이고 "
                                "Σ dim P(S)·dim S = 2520 = |A₇| · "
                                "★**A₆ 와 대조**(A₆ 는 defect-0 가 16차원으로 융합)"),
            "features": ("★전부 **Loewy 길이 5**·head=soc=S · 단열(uniserial) = P(4̂)·P(4̄̂)·P(20̂) · "
                         "★★**P(14̂) = 14̂ / 1̂⊕14̂ / 20̂ / 1̂ / 14̂ — 2층에 14̂ 자신** ⟹ "
                         "전일의 **자기고리 Ext¹(14̂,14̂)=1 을 독립 산출물이 확인** · "
                         "★★**P(14̂) 만 비회문 = 비-rigid**(radical 급수 ≠ socle 급수) — "
                         "나머지 5개는 rigid · ★A₆ 는 LL=9 인데 A₇ 는 LL=5"
                         "(둘 다 defect group 위수 8)"),
            "prediction_corrected": ("★설계 시 '전부 회문'을 예상했으나 **반증** — "
                                     "자기고리를 가진 P(14̂) 만 비회문이자 비-rigid. "
                                     "socle 급수를 **직접 계산**해 논증이 아닌 실측으로 판정"),
        }

    ok = bool(all(R.values()))
    out["checks"] = R
    out["method"] = {
        "projective_cover": ("①|H| 가 p 와 서로소면 k[G/H] 사영 · "
                             "②정칙가군 kG 를 우측곱 자기준동형(End_G(kG)=kG)의 "
                             "Fitting 분해로 쪼갠다(사영자 e 를 날라 e·A·e 유지)"),
        "radical": "rad(M) = ∩ ker(M → S) — J(kG) 구성 불필요",
        "projectivity": "Higman/Chouinard: Y 사영 ⟺ dim Y^{Syl_p} = dim Y/|Syl_p|",
        "determinism": "random.Random(3) 고정 시드 — 분해는 결정론적",
    }
    out["scope_honesty"] = {
        "delivered": ("4 블록 차원 산술 게이트 · P(1̂) 치환가군 구성 · 정칙가군 완전 분해(17) · "
                      "★𝔽₂ 비분해체 실측(16차원 융합 단순가군) · A₆ 3 PIM 완전 Loewy 급수 · "
                      "★★A₇ 6 PIM 전부(지수 크기 운반자 3종·Frobenius 예측 게이트) · "
                      "★Cartan 열 9개 독립 재유도 · ★rad/rad² = Ext¹ 9개(삼중 교차검증) · "
                      "★★자기고리 Ext¹(14̂,14̂)=1 독립 확인 · ★A₇ 는 𝔽₂ 분해체(A₆ 와 대조)"),
        "not_yet": ("A₆ p=3 Loewy(𝔽₃ 위 융합 6차원 취급 필요) · 퀴버 대수의 관계식 · "
                    "A₆ LL=9 vs A₇ LL=5 의 **구조적 설명**(관측만·기전 무주장)"),
        "not_claimed": "봉인 게이트 · A 축 산술의 분해체 가정을 넘는 진술",
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p_ = os.path.join(ROOT, ".pgf", "proofs", "LOEWY-SERIES.json")
        os.makedirs(os.path.dirname(p_), exist_ok=True)
        with open(p_, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("사영 덮개 → Loewy 급수 (정확 — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  ★차원 산술: A₆ p=2 {tot6_2} · A₆ p=3 {tot6_3} · A₇ p=2 {tot7_2}",
              flush=True)
        print(f"  ★★𝔽₂A₆ = P(1̂) ⊕ P(4ₐ)^4 ⊕ P(4_b)^4 ⊕ (16차원 융합 단순)^8 — "
              f"성분 {len(parts)}개", flush=True)
        for k, v in sorted(pim.items()):
            print(f"  ★{k} dim={v['dim']} LL={v['loewy_length']} "
                  f"층={v['loewy_layers']} 총합={v['composition_total']}"
                  f"(=Cartan 열) rad/rad²={v['rad_over_rad2']}(=Ext¹ 행)", flush=True)
        for k in N7:
            v = pim7[k]
            print(f"  ★A₇ P({k}) dim={v['dim']} LL={v['loewy_length']} "
                  f"층={v['loewy_layers']} 총합={v['composition_total']}(=Cartan 열) "
                  f"rad/rad²={v['rad_over_rad2']}(=Ext¹ 행) 운반자={v['carrier']}",
                  flush=True)
        print("  ★★자기고리 독립 확인: P(14̂) 의 2층에 14̂ 자신 — Ext¹(14̂,14̂)=1 검증",
              flush=True)
        print(f"  ★비회문·비-rigid = {[k for k in N7 if not pim7[k]['rigid']]} "
              f"(설계 시 '전부 회문' 예상 → 반증·socle 급수 직접 계산으로 판정)", flush=True)
        print("  ★𝔽₂ 는 A₇ 의 분해체(End(S)=𝔽₂ 전수·Σ dim P·dim S = 2520) — A₆ 와 대조",
              flush=True)
        print("  ★삼중 교차검증 성립: 분해행렬 D → Cartan C · Ext¹ 퀴버 · Loewy 급수",
              flush=True)
        print("  → .pgf/proofs/LOEWY-SERIES.json", flush=True)
    print(f"loewy_series_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
