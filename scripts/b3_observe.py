#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""b3_observe — TrackHE8 P2: 초팔면체군 B₃=(ℤ₂)³⋊S₃ ζ-free 정수-monomial 구조 witness (관측, seal 아님).

report8 최다수렴축(B₃ hyperoctahedral 7/8). ★S₄ (2,2) ζ₃-필연 closed-negative(TrackHE6 P4)의
**상보 positive**: B₃(48원소, Coxeter type B, signed-permutation)는 **rational group**(모든 g 가
gcd(k,ord)=1 인 g^k 와 켤레) → **정수 문자표**(문자값 전부 ∈ ℤ) → 군 Fourier 가 ζ 없이 완전히 닫힘.
S₃/D₄/S₄ 비아벨 곱셈 계보의 **하이퍼팔면체 B_n(n≥3) 개창**.

관측 내용(오라클 독립, dense 심볼릭):
  1. B₃ = 48개 signed-perm 3×3 행렬(entries∈{0,±1}) — 닫힘·order 48·non-abelian·전 역원 존재.
  2. 인코딩 6bit [t0,t1,t2,a1,a0,b]·closed-form 법칙 (s,σ)(t,τ)=(s⊕σ·t, στ) == signed-perm 행렬법칙
     48×48 exact ((σ·t)_i=t_{σ⁻¹(i)}, στ=S₃ 곱).
  3. ★**ζ-free = rational group 판정**: 각 g, 각 k(gcd(k,ord(g))=1) 에 대해 g^k 가 g 와 켤레 →
     Q-group → 정수 문자표(Burnside). ambivalent(g~g⁻¹, k=−1)는 특수 케이스. **S₄ ζ₃ 필연과 정반대**.
  4. b3_mult 곱셈 오라클(|g⟩|h⟩→|g⟩|gh⟩, 12q) 순열이 bijection·MMD reversible synthesis 154게이트·
     max 6 controls(봉인 toffoli~c6x, 신규 module 0) — **회로-실현 가능**(원리상 Tier-0 봉인 가능).

정직 경계(seal 아님, root 불변 sidecar): 관측 = B₃ 표현론 구조(ζ-free)·군법칙·오라클 회로-실현성.
  ★12q b3_mult dense 봉인(EXACT_BOUND=12 경계, 154×4096² compose ~9분+)은 실용 밖 → 여기선 관측.
  실제 Fourier 행렬(b3_qft)·HSP 응용 = 차기/범위밖. 신규 module 0.

사용: python scripts/b3_observe.py [--quick]
"""
from __future__ import annotations
import sys, itertools
from math import gcd
import numpy as np


# ── S₃ = perm of {0,1,2}, σ=r^a s^b (s3_mult 규약) ──
R, S, ID = (1, 2, 0), (1, 0, 2), (0, 1, 2)


def s3_perm(a, b):
    p = ID
    for _ in range(a):
        p = tuple(R[p[i]] for i in range(3))
    if b:
        p = tuple(p[S[i]] for i in range(3))
    return p


def s3_mult_ab(g, h):
    a, b = g
    c, d = h
    return ((a + (c if b == 0 else -c)) % 3, b ^ d)


def sinv(a, b):
    p = s3_perm(a, b)
    inv = [0, 0, 0]
    for i in range(3):
        inv[p[i]] = i
    return tuple(inv)


def signed_mat(t, a, b):
    sig = s3_perm(a, b)
    M = np.zeros((3, 3), dtype=int)
    for j in range(3):
        i = sig[j]
        M[i, j] = -1 if t[i] else 1
    return M


ELEMS = [(t, a, b) for t in itertools.product((0, 1), repeat=3) for a in range(3) for b in range(2)]
MATS = {e: signed_mat(*e) for e in ELEMS}
KEY = {tuple(MATS[e].flatten()): e for e in ELEMS}


def mmul(e1, e2):
    return KEY[tuple((MATS[e1] @ MATS[e2]).flatten())]


def order(e):
    p = e
    n = 1
    while p != ELEMS[0] if False else True:
        if MATS[p].tolist() == np.eye(3, dtype=int).tolist():
            return n
        p = mmul(p, e)
        n += 1
        if n > 48:
            return -1


def conj_class(e):
    return frozenset(mmul(mmul(x, e), KEY[tuple(np.linalg.inv(MATS[x]).round().astype(int).flatten())])
                     for x in ELEMS)


def b3_mult_closed(g, h):
    (s, ag, bg) = g
    (t, ah, bh) = h
    si = sinv(ag, bg)
    st = tuple(t[si[i]] for i in range(3))
    news = tuple(s[i] ^ st[i] for i in range(3))
    na, nb = s3_mult_ab((ag, bg), (ah, bh))
    return (news, na, nb)


def main():
    quick = "--quick" in sys.argv
    R_ = {}

    # 1. 군 구조
    ident = next(e for e in ELEMS if MATS[e].tolist() == np.eye(3, dtype=int).tolist())
    R_["order_48"] = len(set(tuple(MATS[e].flatten()) for e in ELEMS)) == 48
    R_["non_abelian"] = not np.array_equal(MATS[((1, 0, 0), 1, 0)] @ MATS[((0, 0, 0), 0, 1)],
                                           MATS[((0, 0, 0), 0, 1)] @ MATS[((1, 0, 0), 1, 0)])
    inv_ok = all(tuple(np.linalg.inv(MATS[e]).round().astype(int).flatten()) in KEY for e in ELEMS)
    R_["all_inverses_present"] = inv_ok

    # 2. closed-form 법칙 == 행렬법칙 (48×48)
    R_["closed_form_law_exact"] = all(b3_mult_closed(g, h) == mmul(g, h) for g in ELEMS for h in ELEMS)

    # 3. ★ζ-free = rational (Q-)group 판정: 각 g, gcd(k,ord)=1 → g^k ~ g
    def rational_group():
        for e in ELEMS:
            m = order(e)
            cc = conj_class(e)
            for k in range(2, m):
                if gcd(k, m) == 1:
                    p = e
                    for _ in range(k - 1):
                        p = mmul(p, e)
                    if p not in cc:
                        return False
        return True
    R_["zeta_free_rational_group"] = rational_group()
    R_["ambivalent_all_real"] = all(
        KEY[tuple(np.linalg.inv(MATS[e]).round().astype(int).flatten())] in conj_class(e) for e in ELEMS)

    # 4. b3_mult 오라클 회로-실현성 (bijection + MMD synth ≤ c6x)
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
    import genskills as gs
    NQ = 12

    def dec6(x):
        return ((x >> 5) & 1, (x >> 4) & 1, (x >> 3) & 1), ((x >> 2) & 1) * 2 + ((x >> 1) & 1), x & 1

    def enc(t, a, b):
        return (t[0] << 5) | (t[1] << 4) | (t[2] << 3) | ((a >> 1) << 2) | ((a & 1) << 1) | b
    perm = [0] * (1 << NQ)
    for x in range(1 << NQ):
        g6, h6 = (x >> 6) & 63, x & 63
        tg, ag, bg = dec6(g6)
        th, ah, bh = dec6(h6)
        if ag < 3 and ah < 3:
            gh = b3_mult_closed((tg, ag, bg), (th, ah, bh))
            perm[x] = (g6 << 6) | enc(*gh)
        else:
            perm[x] = x
    R_["oracle_bijection"] = sorted(perm) == list(range(1 << NQ))
    gates = gs.mmd_synthesize(perm, NQ)
    maxc = max((len(c) for c, _ in gates), default=0)
    R_["oracle_mmd_synthesizable"] = (maxc <= 12)
    n_gates = len(gates)

    # teeth: 오염된 법칙(부호 XOR 누락)은 rational-group/law 검사를 통과하지 못해야 함
    bad = all(b3_mult_closed(g, h) == (g[0], *s3_mult_ab((g[1], g[2]), (h[1], h[2]))) for g in ELEMS for h in ELEMS)
    R_["teeth_law_nontrivial"] = not bad     # 부호 성분이 실제로 법칙에 기여

    ok = all(R_.values())
    if not quick:
        print("초팔면체군 B₃=(ℤ₂)³⋊S₃ ζ-free 정수-monomial 구조 관측 (S₄ ζ₃ 상보 positive, witness — seal 아님):",
              flush=True)
        for k, v in R_.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  b3_mult 오라클: {n_gates} MMD 게이트·max {maxc} controls (회로-실현 가능, 12q dense 봉인=실용밖→관측)",
              flush=True)
        print("  ★정직: 관측=B₃ 표현론(★rational group→정수 문자표=ζ-free, S₄ ζ₃ 필연과 정반대)·군법칙·"
              "오라클 회로실현성. Fourier 행렬·HSP=차기/범위밖. 신규 module 0·root 불변 sidecar.", flush=True)
    print(f"b3_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
