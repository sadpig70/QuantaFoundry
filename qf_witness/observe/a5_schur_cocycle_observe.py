#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""a5_schur_cocycle_observe — TrackHE14 P5: H²(A₅) Schur multiplier cocycle causal layer
(관측, seal 아님). ★전 과정 정수/GF(2) 정확산술(float 0).

v12 에서 2.A₅=SL(2,5) 의 FS=−1(quaternionic, Frobenius 삼분 ℍ)을 관측했다. 본 witness 는 그
**원인층**을 cocycle 수준에서 제시한다: central extension ℤ₂→SL(2,5)→A₅ 의 section factor set
α(g,h)∈{±1} 가 **비-coboundary**(non-split certificate) — 왜 2차원 표현이 double cover 를
필연으로 요구하는가의 §3j 정식화. §2 Fourier 실봉인 경계는 **cocycle 관계식만** 다뤄 정면 회피
(게이트 분해 무접촉).

구성(전부 자체구성, 외부표 불신):
  E = SL(2,5) = {M∈GF(5)²ˣ² : det=1} 전수 나열(|E|=120) · 중심 Z={±I} 계산으로 확인 ·
  G = PSL(2,5) = E/Z (|G|=60; A₅ 와의 동형은 고전 사실 — 참고, 본 witness 는 G 자체로 완결).
  section s: G→E = 코셋 정준대표(enc 최소, 결정론) → s(g)s(h) = (−I)^{a(g,h)} s(gh).

관측 계층 (전부 exact):
  1. 군 구조 자체유도: |E|=120·중심 {±I}·★위수-2 원소 유일(−I) — 초등 non-split 논증:
     complement K≅G(짝수위수)는 involution 을 가져야 하나 E 의 유일 involution −I∉K → 모순.
  2. G 구조: 켤레류 크기 [1,12,12,15,20]·원소위수 {1:1,2:15,3:20,5:24}·★단순성(모든 비자명
     켤레류의 정규폐포 = G)·★완전성 [E,E]=E·[G,G]=G → Hom(G,ℤ₂)=0.
  3. factor set: 정규화(a(e,·)=a(·,e)=0)·★cocycle identity 60³=216,000 triple 전수 위반 0.
  4. ★non-split certificate: coboundary 선형계 a(g,h)=l(g)+l(h)+l(gh) (GF(2), 3600 방정식×
     60 미지수) UNSAT — 좌영벡터 y(y·A=0·y·b=1) 자체검증, ★support 2(두 방정식이 동일
     미지수·상이 우변 → 즉시 모순, 최소 certificate). [α]≠0 ∈ H²(G,ℤ₂) ⟺ 확장 비분리.
  5. ★스코프 상승 무료: 계 kernel = Hom(G,ℤ₂)∪{0} = {0}(완전성) → 2-adic 재귀에서 각 단계
     보정이 kernel 원소 → μ_{2^k}-값 λ 전 계층에서 UNSAT (⟨i⟩·μ₈·… 자동).
  6. causal link: 2차원 GF(5) 자연표현 = section 행렬 자신 — ρ(g)ρ(h) = (−I)^{a} ρ(gh) 를
     전 3600 쌍 확인. UNSAT ⟹ 부호 재배정 g↦±s(g) 로 α 제거 불가 = **2차원 구조는 A₅ 의
     참표현이 될 수 없음** → double cover 2.A₅ 필연 (v12 FS=−1 의 원인).
  7. ★Sylow-2 ≅ Q₈: 위수-8 부분군의 원소위수 다중집합 {1,2,4⁶} — 8차군 5종 다중집합 전수
     판별로 Q₈ 유일 확정. quaternionic(ℍ) 구조의 군론적 발현(v12 FS=−1·P1 D(Q₈) 연결).
  teeth: (i) α 한 비트 flip → cocycle 위반 검출 (ii) ★split 양성대조: E'=G×ℤ₂ 비틀린
     section(s'(g)=(g,λ(g))) → factor set=dλ: cocycle 통과·SAT·복원해가 dλ 재현
     (iii) S₃ 대조: [S₃,S₃]=A₃⊊S₃ — 완전성 판정기의 변별력.

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0): witness = [α]≠0 (비분리 certificate)
  — **M(A₅)=H²(A₅,U(1))=ℤ₂ 전체 차원은 무주장**(고전 사실 참고). U(1) 전 범위 coboundary 는
  μ_{2^k} 스코프 한정 진술(divisibility 정리 무주장). PSL(2,5)≅A₅ 동형은 고전 참고(본 관측은
  G=PSL(2,5) 로 자기완결). 표현 지표/FS 재계산 없음(v12 관측과 연결만).

사용: python -m qf_witness.observe.a5_schur_cocycle_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import itertools

P = 5


# ════════════════════════════════════════════════════════════════════
#  SL(2,5) 정확산술 (GF(5) 2×2, det=1)
# ════════════════════════════════════════════════════════════════════
def mmul(A, B):
    a, b, c, d = A; e, f, g, h = B
    return ((a * e + b * g) % P, (a * f + b * h) % P,
            (c * e + d * g) % P, (c * f + d * h) % P)


def minv(M):
    a, b, c, d = M
    return (d, (-b) % P, (-c) % P, a)          # det=1 → adjugate


def neg(M):
    return tuple((-x) % P for x in M)


def enc(M):
    return ((M[0] * P + M[1]) * P + M[2]) * P + M[3]


IDE = (1, 0, 0, 1)


def build_E():
    return [M for M in itertools.product(range(P), repeat=4)
            if (M[0] * M[3] - M[1] * M[2]) % P == 1]


def order_of(M):
    k = 1; X = M
    while X != IDE:
        X = mmul(X, M); k += 1
    return k


def commutator_closure(elems):
    """[H,H] 정규폐포 아님 — 전체 commutator 집합의 곱-닫힘(부분군)."""
    comms = {mmul(mmul(A, B), mmul(minv(A), minv(B))) for A in elems for B in elems}
    cl = {IDE} | comms
    frontier = list(cl)
    gens = list(comms)
    while frontier:
        nxt = []
        for x in frontier:
            for g in gens:
                z = mmul(x, g)
                if z not in cl:
                    cl.add(z); nxt.append(z)
        frontier = nxt
    return cl


# ════════════════════════════════════════════════════════════════════
#  GF(2) 선형계 (dtw_z2z2_double_observe 기계 재사용)
# ════════════════════════════════════════════════════════════════════
def gf2_solve(eqs):
    """eqs=[(mask,rhs)]. (True, x_mask, None) | (False, None, y_combo_mask)."""
    work = [[m, r, 1 << i] for i, (m, r) in enumerate(eqs)]
    pivots = {}
    for wi, w in enumerate(work):
        r, rb, cm = w
        while r:
            p = r.bit_length() - 1
            if p in pivots:
                pr = work[pivots[p]]
                r ^= pr[0]; rb ^= pr[1]; cm ^= pr[2]
            else:
                pivots[p] = wi
                w[0], w[1], w[2] = r, rb, cm
                break
        else:
            w[0], w[1], w[2] = 0, rb, cm
            if rb:
                return False, None, cm
    x = 0
    for p in sorted(pivots):
        w = work[pivots[p]]
        r, rb = w[0], w[1]
        acc = rb
        rr = r & ~(1 << p)
        while rr:
            q = rr.bit_length() - 1
            acc ^= (x >> q) & 1
            rr &= ~(1 << q)
        if acc:
            x |= 1 << p
    return True, x, None


def gf2_kernel_dim(eqs, ncols):
    basis = []
    for m, _ in eqs:
        r = m
        for b in basis:
            r = min(r, r ^ b)
        if r:
            basis.append(r); basis.sort(reverse=True)
    return ncols - len(basis)


# ════════════════════════════════════════════════════════════════════
#  본 관측
# ════════════════════════════════════════════════════════════════════
def build_all():
    E = build_E()
    canon = {}
    G = []
    for M in E:
        r = M if enc(M) <= enc(neg(M)) else neg(M)
        if r not in canon:
            canon[r] = len(G)
            G.append(r)
    NG = len(G)
    gm = [[0] * NG for _ in range(NG)]
    fa = [[0] * NG for _ in range(NG)]
    for i in range(NG):
        for j in range(NG):
            M = mmul(G[i], G[j])
            r = M if enc(M) <= enc(neg(M)) else neg(M)
            gm[i][j] = canon[r]
            fa[i][j] = 0 if M == r else 1
    return E, G, canon, gm, fa


def conj_classes(NG, gm, ginv):
    seen = set(); out = []
    for g in range(NG):
        if g in seen:
            continue
        cl = sorted({gm[gm[x][g]][ginv[x]] for x in range(NG)})
        out.append(cl); seen.update(cl)
    return out


def normal_closure_is_G(cl, NG, gm):
    sub = {0} | set(cl)
    frontier = list(sub)
    gens = list(cl)
    while frontier:
        nxt = []
        for x in frontier:
            for g in gens:
                z = gm[x][g]
                if z not in sub:
                    sub.add(z); nxt.append(z)
        frontier = nxt
    return len(sub) == NG


def cocycle_violations(NG, gm, fa):
    bad = 0
    for g in range(NG):
        fg = fa[g]; gmg = gm[g]
        for h in range(NG):
            a1 = fg[h]; fgh = fa[gmg[h]]; fh = fa[h]; gmh = gm[h]
            for k in range(NG):
                if a1 ^ fgh[k] ^ fh[k] ^ fg[gmh[k]]:
                    bad += 1
    return bad


def coboundary_eqs(NG, gm, fa):
    eqs = []
    for g in range(NG):
        for h in range(NG):
            m = (1 << g) ^ (1 << h) ^ (1 << gm[g][h])
            eqs.append((m, fa[g][h]))
    return eqs


def sylow2_multiset(E):
    """위수-4 원소쌍 폐포로 order-8 부분군 → 원소위수 다중집합 (결정론 첫 발견)."""
    o4 = [M for M in E if order_of(M) == 4]
    for A in o4:
        for B in o4:
            S = {IDE}
            fr = [A, B]
            while fr and len(S) <= 8:
                x = fr.pop()
                if x in S:
                    continue
                S.add(x)
                for g in (A, B):
                    fr.append(mmul(x, g))
            if len(S) == 8:
                return sorted(order_of(x) for x in S)
    return None


def classify_order8(ms):
    ms = tuple(ms)
    table = {
        (1, 2, 2, 2, 2, 2, 2, 2): "Z2^3",
        (1, 2, 2, 2, 2, 2, 4, 4): "D4",
        (1, 2, 2, 2, 4, 4, 4, 4): "Z4xZ2",
        (1, 2, 4, 4, 4, 4, 4, 4): "Q8",
        (1, 2, 4, 4, 8, 8, 8, 8): "Z8",
    }
    return table.get(ms, f"unknown{ms}")


# ── teeth (ii): split 양성대조 E' = G×ℤ₂, 비틀린 section ──
def split_control(NG, gm):
    lam = [i % 2 for i in range(NG)]           # 결정론 비자명 함수 (λ(e)=0)
    fa2 = [[(lam[i] + lam[j] + lam[gm[i][j]]) % 2 for j in range(NG)] for i in range(NG)]
    bad = 0
    for g in range(NG):
        for h in range(NG):
            for k in range(NG):
                if fa2[g][h] ^ fa2[gm[g][h]][k] ^ fa2[h][k] ^ fa2[g][gm[h][k]]:
                    bad += 1
    eqs = coboundary_eqs(NG, gm, fa2)
    sat, x, _ = gf2_solve(eqs)
    recovered = sat and all(((x >> g) & 1) ^ ((x >> h) & 1) ^ ((x >> gm[g][h]) & 1)
                            == fa2[g][h] for g in range(NG) for h in range(NG))
    return bad == 0 and sat and recovered


# ── teeth (iii): S₃ 완전성 대조 ──
def s3_not_perfect():
    perms = list(itertools.permutations(range(3)))
    def pm(p, q):
        return tuple(p[q[i]] for i in range(3))
    def pinv(p):
        r = [0] * 3
        for i, v in enumerate(p):
            r[v] = i
        return tuple(r)
    comms = {pm(pm(a, b), pm(pinv(a), pinv(b))) for a in perms for b in perms}
    cl = set(comms)
    changed = True
    while changed:
        changed = False
        for x in list(cl):
            for y in list(cl):
                z = pm(x, y)
                if z not in cl:
                    cl.add(z); changed = True
    return len(cl) == 3 and len(cl) < len(perms)


def main():
    quick = "--quick" in sys.argv
    R = {}
    E, G, canon, gm, fa = build_all()
    NG = len(G)
    e_idx = canon[IDE]

    # 1. 군 구조
    R["E_order_120"] = (len(E) == 120)
    center = [M for M in E if all(mmul(M, X) == mmul(X, M) for X in E)]
    R["center_pmI"] = (sorted(center) == sorted([IDE, neg(IDE)]))
    order2 = [M for M in E if M != IDE and mmul(M, M) == IDE]
    R["unique_involution_negI"] = (order2 == [neg(IDE)])
    R["G_order_60"] = (NG == 60)

    # 2. G 구조: 켤레류·위수·단순성·완전성
    ginv = [next(b for b in range(NG) if gm[a][b] == e_idx) for a in range(NG)]
    classes = conj_classes(NG, gm, ginv)
    sizes = sorted(len(c) for c in classes)
    R["class_sizes"] = (sizes == [1, 12, 12, 15, 20])
    gorders = {}
    for g in range(NG):
        k, x = 1, g
        while x != e_idx:
            x = gm[x][g]; k += 1
        gorders[k] = gorders.get(k, 0) + 1
    R["order_multiset"] = (gorders == {1: 1, 2: 15, 3: 20, 5: 24})
    R["G_simple"] = all(normal_closure_is_G(c, NG, gm)
                        for c in classes if len(c) > 1)
    R["E_perfect"] = (len(commutator_closure(E)) == 120)
    # G 완전성: G 의 commutator 폐포 (인덱스 세계)
    gcomms = {gm[gm[a][b]][gm[ginv[a]][ginv[b]]] for a in range(NG) for b in range(NG)}
    gcl = {e_idx} | gcomms
    fr = list(gcl)
    gg = list(gcomms)
    while fr:
        nxt = []
        for x in fr:
            for g in gg:
                z = gm[x][g]
                if z not in gcl:
                    gcl.add(z); nxt.append(z)
        fr = nxt
    R["G_perfect"] = (len(gcl) == NG)

    # 3. factor set: 정규화 + cocycle 전수
    R["normalized"] = all(fa[e_idx][j] == 0 and fa[j][e_idx] == 0 for j in range(NG))
    viol = cocycle_violations(NG, gm, fa)
    R["cocycle_216000"] = (viol == 0)

    # 4. non-split certificate
    eqs = coboundary_eqs(NG, gm, fa)
    sat, _, ycert = gf2_solve(eqs)
    R["coboundary_UNSAT"] = (not sat)
    cert_pairs = []
    cert_ok = False
    if ycert is not None:
        accm = 0; accb = 0
        idxs = []
        i = 0; y = ycert
        while y:
            if y & 1:
                idxs.append(i)
            y >>= 1; i += 1
        for i2 in idxs:
            m, r = eqs[i2]
            accm ^= m; accb ^= r
            cert_pairs.append([i2 // NG, i2 % NG])
        cert_ok = (accm == 0 and accb == 1)
    R["certificate_verified"] = cert_ok

    # 5. 스코프 상승: kernel = {0}
    kdim = gf2_kernel_dim(eqs, NG)
    R["kernel_trivial_scope_escalation"] = (kdim == 0)

    # 6. causal link: 2차원 자연표현의 사영 descent (전 3600 쌍)
    R["projective_descent_3600"] = all(
        mmul(G[i], G[j]) == (G[gm[i][j]] if fa[i][j] == 0 else neg(G[gm[i][j]]))
        for i in range(NG) for j in range(NG))

    # 7. Sylow-2 ≅ Q₈
    ms = sylow2_multiset(E)
    R["sylow2_Q8"] = (ms is not None and classify_order8(ms) == "Q8")

    # teeth
    fa_bad = [row[:] for row in fa]
    fa_bad[1][2] ^= 1
    R["teeth_bitflip_detected"] = (cocycle_violations(NG, gm, fa_bad) > 0)
    R["teeth_split_positive_control"] = split_control(NG, gm)
    R["teeth_s3_not_perfect"] = s3_not_perfect()

    ok = bool(all(R.values()))
    out = {
        "_schema": "a5-schur-cocycle/v1",
        "_note": ("H²(A₅) Schur cocycle causal layer: SL(2,5)→PSL(2,5) factor set "
                  "α — cocycle 216,000 전수·GF(2) UNSAT(support-2 certificate)·"
                  "완전성→μ_{2^k} 스코프 상승·유일 involution 초등 논증·Sylow-2=Q₈. "
                  "v12 2.A₅ FS=−1 의 원인층. 관측·seal 아님·신규 module 0·root 불변. "
                  "M(A₅) 전체 차원 무주장."),
        "checks": R,
        "certificate": {
            "support_pairs_gh": cert_pairs,
            "meaning": "동일 미지수 집합 {l(g),l(h),l(gh)}·상이한 우변 → 즉시 모순(최소 certificate)",
        },
        "sylow2_order_multiset": ms,
        "observation_layers": [
            "unique involution −I → complement 불가(초등)",
            "GF(2) UNSAT + 좌영벡터 → [α]≠0 ∈ H²(G,ℤ₂) (확장 비분리)",
            "kernel=0 (완전성) → μ_{2^k} 전 계층 UNSAT",
            "사영 descent 3600 쌍 → 2차원 구조의 A₅ 참표현 불가 = 2.A₅ 필연(FS=−1 원인)",
            "Sylow-2=Q₈ → quaternionic 발현(v12 ℍ·P1 D(Q₈) 연결)",
        ],
        "all_ok": ok,
    }

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "A5-SCHUR-COCYCLE.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("H²(A₅) Schur cocycle causal layer 관측 (전 과정 정확산술 — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  ★certificate support: {cert_pairs} (동일 미지수·상이 우변 → 최소 모순)", flush=True)
        print(f"  ★Sylow-2 위수 다중집합: {ms} → Q₈ (quaternionic 발현)", flush=True)
        print("  → .pgf/proofs/A5-SCHUR-COCYCLE.json", flush=True)
    print(f"a5_schur_cocycle_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
