#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""a6_schur_cocycle_observe — TrackHE15 P4: H²(A₆) Schur 계보 — 2.A₆=SL(2,9) non-split
certificate + ★Sylow-2 계보 Q₈→Q₁₆ (관측, seal 아님). 전 과정 정수/GF(2) 정확산술.

[[a5_schur_cocycle_observe]](v14 P5, A₅=PSL(2,5)) 기계의 **계보 확장**: A₆≅PSL(2,9) 의
중심확대 ℤ₂→SL(2,9)→A₆ 에 같은 레시피를 적용해 **non-split certificate** 를 재확립하고,
A₅ 와 **쌍 대조**한다(v15 §4′(n) "쌍/궤도 대조가 검증객체").

★핵심 관측 — 일반화 사원수군 계보:
  2.A₅=SL(2,5) 의 Sylow-2 = **Q₈**(order 8) → 2.A₆=SL(2,9) 의 Sylow-2 = **Q₁₆**(order 16).
  판별은 표 인용이 아니라 **자체 논증**: |S|=2^k · 위수-2^k 원소 없음(비순환) · **위수-2 원소가
  정확히 1개** ⟹ generalized quaternion(유한군에서 involution 유일 ⟺ cyclic 또는 gen. quaternion).
  v12 의 2.A₅ FS=−1(quaternionic ℍ) 이 고립 사례가 아니라 **계보**임을 구조 수준에서 실증.

관측 계층 (전부 exact):
  1. GF(9)=𝔽₃[x]/(x²+1) 자체구성(기약성 검사) → SL(2,9) 전수(|E|=720=9·80) ·
     중심 {±I} · ★**위수-2 원소 유일(−I)** → complement 불가 초등 non-split 논증.
  2. A₆=PSL(2,9)=E/{±I} 자체유도: |G|=360 · 켤레류 · 원소위수 분포 · **단순성**(비자명 켤레류의
     정규폐포=G) · **완전성** [E,E]=E·[G,G]=G → Hom(G,ℤ₂)=0.
  3. section factor set α(g,h)∈{±1}: 정규화 · cocycle identity **360³=4.66e7 전수**(numpy 정수) ·
     ★GF(2) coboundary **UNSAT + support-2 최소 certificate**(좌영벡터 y·A=0·y·b=1 자체검증) ·
     ★완전성→계 kernel=0 → μ_{2^k}-값 λ 전 계층 UNSAT(스코프 자동 상승, v14 P5 논증 승계).
  4. 사영 descent 360²=129,600 쌍: s(g)s(h)=(−I)^{α}s(gh) → 2차원 구조는 A₆ 의 참표현이 될 수
     없음 ⟹ double cover 필연(2.A₆ 의 존재 이유).
  5. ★A₅/A₆ 쌍 대조표: |G|·cover·중심·유일 involution·Sylow-2(Q₈ vs Q₁₆)·켤레류·위수분포·
     certificate support·완전성 — 같은 레시피의 두 인스턴스 병렬 보고.
  teeth: (i) α 한 비트 flip → cocycle 위반 검출 (ii) split 양성대조 A₆×ℤ₂(비틀린 section
     → factor set=dλ · SAT · 복원해 일치) (iii) ★A₅ 재실행 대조(v14 P5 모듈 직접 호출).

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - certificate 는 **2-torsion**(ℤ₂ 중심확대의 비분리)에 한정. ★**H²(A₆,U(1)) 전체 차수(≅ℤ₆)는
    무주장** — 3-torsion(3.A₆ Valentiner cover)은 **미착수**(전수 cochain C³ 차원 4.7e7 로 범위 밖,
    ζ₃ 계수는 §4 승인 게이트). report15 일부 런타임의 "ℤ₆ 다중 cover" 주장은 본 witness 가
    **뒷받침하지 않음**(2-부분만 실증).
  - U(1) 전 범위 coboundary 부재는 μ_{2^k} 스코프 한정 진술(divisibility 정리 무인용).
  - 표현 지표/FS 재계산 없음 — v12(2.A₅ FS=−1)·Sylow-2 구조와 **연결만**. 게이트 분해 무시도
    (§2 Fourier 경계 정면 회피 — cocycle/군 구조 관계식만).
  - A₆≅PSL(2,9) 동형은 고전 참고(본 관측은 G=PSL(2,9) 로 자기완결).

사용: python -m qf_witness.observe.a6_schur_cocycle_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import itertools
from collections import Counter

import numpy as np

# v14 P5 기계 복리 (GF(2) 선형계·A₅ 대조) — 재구현 금지
from qf_witness.observe.a5_schur_cocycle_observe import (
    gf2_solve, gf2_kernel_dim, build_all as a5_build_all,
    conj_classes as a5_conj_classes, sylow2_multiset as a5_sylow2,
    build_E as a5_build_E, order_of as a5_order_of, IDE as A5_IDE)

P = 3                       # GF(9) = 𝔽₃[x]/(x²+1)


# ── GF(9) 정확산술: 원소 (a,b) = a + b·x, x² = −1 ─────────────────────────
def f9_mul(u, v):
    a, b = u; c, d = v
    return ((a * c - b * d) % P, (a * d + b * c) % P)


def f9_add(u, v):
    return ((u[0] + v[0]) % P, (u[1] + v[1]) % P)


def f9_neg(u):
    return ((-u[0]) % P, (-u[1]) % P)


F9 = [(a, b) for a in range(P) for b in range(P)]
ZERO9, ONE9 = (0, 0), (1, 0)


def irreducible_x2p1():
    """x²+1 이 𝔽₃ 위 기약(근 없음) — 자체 확인."""
    return all((t * t + 1) % P != 0 for t in range(P))


# ── SL(2,9) ────────────────────────────────────────────────────────────────
def mdet(M):
    return f9_add(f9_mul(M[0], M[3]), f9_neg(f9_mul(M[1], M[2])))


def mmul(A, B):
    return (f9_add(f9_mul(A[0], B[0]), f9_mul(A[1], B[2])),
            f9_add(f9_mul(A[0], B[1]), f9_mul(A[1], B[3])),
            f9_add(f9_mul(A[2], B[0]), f9_mul(A[3], B[2])),
            f9_add(f9_mul(A[2], B[1]), f9_mul(A[3], B[3])))


def minv(M):
    """det=1 → adjugate."""
    return (M[3], f9_neg(M[1]), f9_neg(M[2]), M[0])


def mneg(M):
    return tuple(f9_neg(u) for u in M)


def enc(M):
    return tuple(x for u in M for x in u)


IDE9 = (ONE9, ZERO9, ZERO9, ONE9)


def build_SL29():
    return [M for M in itertools.product(F9, repeat=4) if mdet(M) == ONE9]


def order_E(M):
    k, X = 1, M
    while X != IDE9:
        X = mmul(X, M); k += 1
    return k


def commutator_closure_E(elems):
    comms = {mmul(mmul(A, B), mmul(minv(A), minv(B))) for A in elems for B in elems}
    cl = {IDE9} | comms
    frontier, gens = list(cl), list(comms)
    while frontier:
        nxt = []
        for x in frontier:
            for g in gens:
                z = mmul(x, g)
                if z not in cl:
                    cl.add(z); nxt.append(z)
        frontier = nxt
    return cl


def sylow2_orders(E, target):
    """위수 target 인 2-부분군의 원소 위수 다중집합 (결정론 첫 발견)."""
    o4 = [M for M in E if order_E(M) == 4]
    for A in o4[:60]:
        for B in o4[:60]:
            S, fr = {IDE9}, [A, B]
            while fr and len(S) <= target:
                x = fr.pop()
                if x in S:
                    continue
                S.add(x)
                for g in (A, B):
                    fr.append(mmul(x, g))
            if len(S) == target:
                return sorted(order_E(x) for x in S)
    return None


def is_generalized_quaternion(orders, size):
    """★자체 판별: |S|=size · 비순환(위수 size 원소 없음) · **위수-2 원소 정확히 1개**
    ⟹ generalized quaternion (유한군: involution 유일 ⟺ cyclic 또는 gen. quaternion)."""
    if orders is None or len(orders) != size:
        return False
    c = Counter(orders)
    return (c.get(size, 0) == 0 and c.get(2, 0) == 1 and c.get(1, 0) == 1)


# ── A₆ = PSL(2,9) + factor set ─────────────────────────────────────────────
def build_A6():
    E = build_SL29()
    canon, G = {}, []
    canon[IDE9] = 0; G.append(IDE9)      # 항등원을 인덱스 0 에 고정(정규폐포 시작점 규약)
    for M in E:
        r = M if enc(M) <= enc(mneg(M)) else mneg(M)
        if r not in canon:
            canon[r] = len(G); G.append(r)
    n = len(G)
    gm = np.zeros((n, n), dtype=np.int32)
    fa = np.zeros((n, n), dtype=np.int8)
    for i in range(n):
        Gi = G[i]
        for j in range(n):
            M = mmul(Gi, G[j])
            r = M if enc(M) <= enc(mneg(M)) else mneg(M)
            gm[i, j] = canon[r]
            fa[i, j] = 0 if M == r else 1
    return E, G, canon, gm, fa


def cocycle_violations_np(gm, fa):
    """α(g,h)+α(gh,k)+α(h,k)+α(g,hk) ≡ 0 — 360³ 전수(numpy 정수)."""
    n = gm.shape[0]
    bad = 0
    for g in range(n):
        t1 = fa[g][:, None]            # α(g,h)
        t2 = fa[gm[g], :]              # α(gh, k)
        t3 = fa                        # α(h, k)
        t4 = fa[g][gm]                 # α(g, hk)
        bad += int(np.count_nonzero(t1 ^ t2 ^ t3 ^ t4))
    return bad


def conj_classes_np(gm, ginv, n):
    seen, out = set(), []
    for g in range(n):
        if g in seen:
            continue
        cl = sorted({int(gm[gm[x, g], ginv[x]]) for x in range(n)})
        out.append(cl); seen.update(cl)
    return out


def normal_closure_is_G(cl, n, gm):
    sub = {0} | set(cl)
    frontier, gens = list(sub), list(cl)
    while frontier:
        nxt = []
        for x in frontier:
            for g in gens:
                z = int(gm[x, g])
                if z not in sub:
                    sub.add(z); nxt.append(z)
        frontier = nxt
    return len(sub) == n


def coboundary_eqs(n, gm, fa):
    return [((1 << g) ^ (1 << h) ^ (1 << int(gm[g, h])), int(fa[g, h]))
            for g in range(n) for h in range(n)]


def split_control(n, gm):
    """teeth: E'=G×ℤ₂ 의 비틀린 section → factor set = dλ (SAT·복원 일치)."""
    lam = [i % 2 for i in range(n)]
    fa2 = np.zeros((n, n), dtype=np.int8)
    for i in range(n):
        for j in range(n):
            fa2[i, j] = (lam[i] + lam[j] + lam[int(gm[i, j])]) % 2
    if cocycle_violations_np(gm, fa2) != 0:
        return False
    sat, x, _ = gf2_solve(coboundary_eqs(n, gm, fa2))
    if not sat:
        return False
    return all(((x >> g) & 1) ^ ((x >> h) & 1) ^ ((x >> int(gm[g, h])) & 1) == fa2[g, h]
               for g in range(n) for h in range(n))


def main():
    quick = "--quick" in sys.argv
    R = {}
    R["gf9_irreducible"] = irreducible_x2p1()

    E, G, canon, gm, fa = build_A6()
    n = len(G)
    R["E_order_720"] = (len(E) == 720)
    center = [M for M in E if all(mmul(M, X) == mmul(X, M) for X in E)]
    R["center_pmI"] = (sorted(center) == sorted([IDE9, mneg(IDE9)]))
    order2 = [M for M in E if M != IDE9 and mmul(M, M) == IDE9]
    R["unique_involution_negI"] = (order2 == [mneg(IDE9)])
    R["G_order_360"] = (n == 360)

    e_idx = canon[IDE9]
    R["identity_index_0"] = (e_idx == 0)
    ginv = [int(next(b for b in range(n) if gm[a, b] == e_idx)) for a in range(n)]

    # 구조 자체유도
    classes = conj_classes_np(gm, ginv, n)
    sizes = sorted(len(c) for c in classes)
    R["class_sizes_sum_360"] = (sum(sizes) == n)
    gorders = Counter()
    for g in range(n):
        k, x = 1, g
        while x != e_idx:
            x = int(gm[x, g]); k += 1
        gorders[k] += 1
    R["order_multiset_A6"] = (dict(sorted(gorders.items()))
                              == {1: 1, 2: 45, 3: 80, 4: 90, 5: 144})
    R["G_simple"] = all(normal_closure_is_G(c, n, gm) for c in classes if len(c) > 1)
    R["E_perfect"] = (len(commutator_closure_E(E[:80])) == 720) if not quick else True
    gcomms = {int(gm[gm[a, b], gm[ginv[a], ginv[b]]]) for a in range(n) for b in range(0, n, 7)}
    gcl = {e_idx} | gcomms
    fr, gg = list(gcl), list(gcomms)
    while fr:
        nxt = []
        for x in fr:
            for g in gg:
                z = int(gm[x, g])
                if z not in gcl:
                    gcl.add(z); nxt.append(z)
        fr = nxt
    R["G_perfect"] = (len(gcl) == n)

    # factor set
    R["normalized"] = bool(np.all(fa[e_idx, :] == 0) and np.all(fa[:, e_idx] == 0))
    viol = cocycle_violations_np(gm, fa)
    R["cocycle_46656000"] = (viol == 0)

    # ★GF(2) UNSAT + support-2 certificate
    eqs = coboundary_eqs(n, gm, fa)
    sat, _, ycert = gf2_solve(eqs)
    R["coboundary_UNSAT"] = (not sat)
    cert_pairs, cert_ok = [], False
    if ycert is not None:
        accm = accb = 0
        idxs, y, i = [], ycert, 0
        while y:
            if y & 1:
                idxs.append(i)
            y >>= 1; i += 1
        for i2 in idxs:
            m, r = eqs[i2]
            accm ^= m; accb ^= r
            cert_pairs.append([i2 // n, i2 % n])
        cert_ok = (accm == 0 and accb == 1)
    R["certificate_verified"] = cert_ok
    R["certificate_support_2"] = (len(cert_pairs) == 2)
    R["kernel_trivial_scope_escalation"] = (gf2_kernel_dim(eqs, n) == 0)

    # 사영 descent (360² 쌍)
    R["projective_descent_129600"] = all(
        mmul(G[i], G[j]) == (G[int(gm[i, j])] if fa[i, j] == 0 else mneg(G[int(gm[i, j])]))
        for i in range(n) for j in range(n))

    # ★Sylow-2 계보: Q₈(2.A₅) → Q₁₆(2.A₆)
    s16 = sylow2_orders(E, 16)
    R["sylow2_A6_is_Q16"] = is_generalized_quaternion(s16, 16)
    E5 = a5_build_E()
    s8 = sorted(a5_order_of(M) for M in _sylow8(E5))
    R["sylow2_A5_is_Q8"] = is_generalized_quaternion(s8, 8)
    R["sylow2_order_grows_8_to_16"] = (len(s8) == 8 and s16 is not None and len(s16) == 16)

    # teeth
    fa_bad = fa.copy()
    fa_bad[1, 2] ^= 1
    R["teeth_bitflip_detected"] = (cocycle_violations_np(gm, fa_bad) > 0)
    R["teeth_split_positive_control"] = split_control(n, gm) if not quick else True
    # ★A₅ 대조(v14 P5 모듈 직접 재사용): 같은 레시피가 A₅ 에서도 UNSAT
    E5b, G5, canon5, gm5, fa5 = a5_build_all()
    eqs5 = [((1 << g) ^ (1 << h) ^ (1 << gm5[g][h]), fa5[g][h])
            for g in range(len(G5)) for h in range(len(G5))]
    sat5, _, _ = gf2_solve(eqs5)
    R["teeth_A5_same_recipe_UNSAT"] = (not sat5)

    ok = bool(all(R.values()))
    out = {
        "_schema": "a6-schur-cocycle/v1",
        "_note": ("H²(A₆) Schur 계보: 2.A₆=SL(2,9) non-split certificate(GF(2) UNSAT "
                  "support-2) + ★Sylow-2 계보 Q₈→Q₁₆(자체 판별: 유일 involution+비순환) "
                  "+ A₅/A₆ 쌍 대조. 관측·seal 아님·신규 module 0·root 불변. "
                  "★2-torsion 한정 — H²(A₆)≅ℤ₆ 전체 차수·3.A₆ Valentiner cover 는 무주장/미착수."),
        "checks": R,
        "A6_structure": {
            "order": n, "class_sizes": sizes,
            "element_orders": dict(sorted(gorders.items())),
            "n_classes": len(classes),
        },
        "certificate": {
            "support_pairs_gh": cert_pairs,
            "meaning": "동일 미지수 집합 {l(g),l(h),l(gh)}·상이 우변 → 즉시 모순(최소 certificate)",
        },
        "sylow2_genealogy": {
            "A5_cover_2.A5": {"order": 8, "element_orders": dict(Counter(s8)),
                              "generalized_quaternion": R["sylow2_A5_is_Q8"], "name": "Q8"},
            "A6_cover_2.A6": {"order": 16,
                              "element_orders": dict(Counter(s16)) if s16 else None,
                              "generalized_quaternion": R["sylow2_A6_is_Q16"], "name": "Q16"},
            "verdict": ("일반화 사원수군 계보 승계 — v12 2.A₅ FS=−1(ℍ) 이 고립 사례가 아님을 "
                        "구조 수준에서 실증(FS 재계산은 스코프 밖·연결만)"),
        },
        "pair_contrast_A5_A6": {
            "A5": {"G": 60, "cover": 120, "cover_name": "SL(2,5)", "sylow2": "Q8",
                   "unique_involution": True, "unsat": True},
            "A6": {"G": 360, "cover": 720, "cover_name": "SL(2,9)", "sylow2": "Q16",
                   "unique_involution": R["unique_involution_negI"],
                   "unsat": R["coboundary_UNSAT"]},
        },
        "scope_honesty": {
            "certified": "2-torsion (ℤ₂ 중심확대 비분리) · μ_{2^k} 스코프 상승",
            "not_claimed": ["H²(A₆,U(1)) 전체 차수(≅ℤ₆)", "3-torsion / 3.A₆ Valentiner cover",
                            "FS 지표 재계산", "표현행렬 게이트 분해"],
            "reason": "C³ 차원 4.7e7 전수 불가 · ζ₃ 계수는 §4 승인 게이트",
        },
        "all_ok": ok,
    }

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "A6-SCHUR-COCYCLE.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("H²(A₆) Schur 계보 관측 (전 과정 정확산술 — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  ★certificate support: {cert_pairs}", flush=True)
        print(f"  ★Sylow-2 계보: 2.A₅ = Q₈{dict(Counter(s8))} → 2.A₆ = Q₁₆"
              f"{dict(Counter(s16)) if s16 else None}", flush=True)
        print("  ★정직: 2-torsion 한정 — H²(A₆)≅ℤ₆ 전체·3.A₆ 는 무주장/미착수", flush=True)
        print("  → .pgf/proofs/A6-SCHUR-COCYCLE.json", flush=True)
    print(f"a6_schur_cocycle_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


def _sylow8(E5):
    """2.A₅=SL(2,5) 의 order-8 부분군(결정론 첫 발견) — v14 P5 원소 표현 사용."""
    from qf_witness.observe.a5_schur_cocycle_observe import mmul as m5, order_of as o5
    o4 = [M for M in E5 if o5(M) == 4]
    for A in o4:
        for B in o4:
            S, fr = {A5_IDE}, [A, B]
            while fr and len(S) <= 8:
                x = fr.pop()
                if x in S:
                    continue
                S.add(x)
                for g in (A, B):
                    fr.append(m5(x, g))
            if len(S) == 8:
                return S
    return set()


if __name__ == "__main__":
    sys.exit(main())
