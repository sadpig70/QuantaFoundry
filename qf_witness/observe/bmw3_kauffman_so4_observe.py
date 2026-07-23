#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bmw3_kauffman_so4_observe — TrackHE18 P1(2변수화): **두 번째 SO(4) 특수화 곡선** —
so₄≅sl₂×sl₂ 벡터표현(스핀-½⊗스핀-½) R-matrix + quantum trace 로 figure-8 / trefoil 의
Kauffman 다항식(N=4 특수화선)을 관측 (seal 아님). [[bmw3_kauffman_so3_observe]] 의 다음 N.

배경: bmw3_kauffman_so3 이 quantum-trace 방법으로 crux 를 해결하고 **N=3 특수화선**(a=q⁴)을 냈다.
완전 2변수 Kauffman F(a,z) 를 향해 **두 번째 곡선 N=4**(a=q³)를 낸다. 핵심=Ř 고유값 q^{1−N}=a⁻¹
이라 **a 는 N 을 통해서만 들어오는 독립변수** — 여러 N 곡선을 모아 2변수 복원.

관측 5축(sympy 심볼릭 p=q^{1/2} — exact):
  A. **so₄=sl₂×sl₂ R-matrix**: V=(½)_a⊗(½)_b(4차원). Ř_{so4}[(i,j)(k,l)] = Ř_a[(i,k)]·Ř_b[(j,l)]
     (범주 곱 braiding c^a⊠c^b). spin-½ Ř 는 universal R(n≤1 절단)로 자체구성.
  B. **★so₄ BMW 고유값**: Ř_{so4} 고유값 = **q(×9, sym-tl)·−q⁻¹(×6, antisym)·q⁻³(×1, singlet)**
     = {Q,−Q⁻¹,Q^{1−N}}(Q=q, N=4). ⟹ **a=q³·z=q−q⁻¹·δ=q²+2+q⁻²=[2]_q²=qdim(V)** 정확일치.
  C. **braid 관계(64차원)**: σ₁=Ř⊗I₄, σ₂=I₄⊗Ř 로 σ₁σ₂σ₁=σ₂σ₁σ₂ 심볼릭 검증.
  D. **quantum trace(Markov 자동)**: μ=diag(q²,1,1,q⁻²)=μ_a⊗μ_b. F=a^{−w}tr_q(ρ(β))/δ.
     **figure-8**(w=0): F(4₁)|N=4 = t⁴−2t³+3t²−4t+5−4t⁻¹+3t⁻²−2t⁻³+t⁻⁴(t=q²) **palindromic**
     (amphichiral)·**trefoil**(w=3) **chiral**.
  E. **★2변수 복원 현황(관측)**: N=3(a=Q²)·N=4(a=Q³) 두 곡선(공통 z=Q−Q⁻¹)은 **단일 2변수 F(a,z)로
     동시 적합 가능**(linsolve 해 존재)하나 **6-파라미터 pure-a 족까지만 결정**(a^{1,2,3}z^{0,1} 미결).
     ★정직 발견: naive a^{−w}·RT/δ 를 여러 N 에 결합하면 매듭 정리 **F(a,0)=1 과 충돌**(곡선은 z=0 에서
     a=1 만 통과 → 국소검증만) ⟹ **N-의존 정규화 미해결**. 완전 2변수 = 3번째 곡선(so₅=sp₄/so₆=sl₄)
     또는 **도식적 Dubrovnik skein**(정의적 2변수)로 완성 = 다음 단계.

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - 각 N 곡선은 exact 검증(고유값·braid·palindromic·δ=qdim) — **정당한 특수화점**. 하지만 완전 2변수
    F(a,z) 는 **미완**(정규화 미묘성·6-파라미터 잔여). 틀린 2변수 봉인 금지 — 곡선만 관측.
  - so₄=sl₂×sl₂ 는 범주 곱 braiding(exact) — 게이트 실봉인 무주장.
  - N=3([[bmw3_kauffman_so3_observe]])·N=4 는 **두 검증된 특수화선** — 방법 일반성 실증(N=3 우연 아님).

사용: python -m qf_witness.observe.bmw3_kauffman_so4_observe [--quick]
"""
from __future__ import annotations
import sys
import json

import sympy as sp


def _build():
    p = sp.symbols("p")               # p = q^{1/2}
    q = p**2
    # spin-1/2 U_q(sl2): |↑>=0,|↓>=1
    E = sp.Matrix([[0, 1], [0, 0]]); F = sp.Matrix([[0, 0], [1, 0]])
    I2 = sp.eye(2)

    def kron(A, B):
        return sp.Matrix(sp.BlockMatrix([[A[i, j] * B for j in range(A.cols)]
                                         for i in range(A.rows)]))
    mm = [sp.Rational(1, 2), sp.Rational(-1, 2)]
    D = sp.zeros(4)
    for i, mi in enumerate(mm):
        for j, mj in enumerate(mm):
            D[2 * i + j, 2 * i + j] = q**(2 * mi * mj)
    Rmat = sp.simplify(D * (sp.eye(4) + (q - 1 / q) * kron(E, F)))
    P2 = sp.Matrix([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
    Rh = sp.simplify(P2 * Rmat)       # spin-½ braiding

    # so_4 Ř on V⊗V (V=4dim, index (i,j)); Ř[(i,j,k,l)->(i',j',k',l')]=Rh[(i,k)]·Rh[(j,l)]
    def Rh_el(x, y, xp, yp):
        return Rh[2 * xp + yp, 2 * x + y]
    Rso4 = sp.zeros(16)
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    row = 8 * i + 4 * j + 2 * k + l
                    for ip in range(2):
                        for jp in range(2):
                            for kp in range(2):
                                for lp in range(2):
                                    v = Rh_el(i, k, ip, kp) * Rh_el(j, l, jp, lp)
                                    if v != 0:
                                        Rso4[8 * ip + 4 * jp + 2 * kp + lp, row] += v
    Rso4 = sp.simplify(Rso4)
    return p, q, kron, Rso4


def main():
    quick = "--quick" in sys.argv
    p, q, kron, Rso4 = _build()
    I4 = sp.eye(4)
    R = {}
    out = {"_schema": "bmw3-kauffman-so4/v1",
           "_note": ("두 번째 SO(4) 특수화 곡선(so₄=sl₂×sl₂) — bmw3_kauffman_so3(N=3) 다음 N. "
                     "fig-8 palindromic/trefoil chiral. 완전 2변수 F(a,z)=미완(정규화 미묘·6-파라미터 "
                     "잔여). 관측·seal 아님·module 0·root 불변.")}
    t = sp.symbols("t")

    # ── B. 고유값 + a,z,δ ─────────────────────────────────────────────────
    ev = {sp.simplify(v): m for v, m in Rso4.eigenvals().items()}
    exp_ev = {sp.simplify(q): 9, sp.simplify(-1 / q): 6, sp.simplify(q**-3): 1}
    R["B_eigenvalues_so4"] = all(any(sp.simplify(kk - ek) == 0 and mm == em for kk, mm in ev.items())
                                 for ek, em in exp_ev.items())
    a_bmw = q**3; z_bmw = q - 1 / q
    delta = q**2 + 2 + q**-2
    R["B_delta_eq_qdim"] = (sp.simplify((a_bmw - 1 / a_bmw) / z_bmw + 1 - delta) == 0)
    R["B_delta_qdim2"] = (sp.simplify(delta - (q + 1 / q)**2) == 0)
    out["bmw_params"] = {"a": "q^3 = Q^(N-1), N=4", "z": "q - q^-1 = Q - Q^-1",
                         "delta": "q^2+2+q^-2 = [2]_q^2 = qdim(V=(1/2)⊗(1/2))",
                         "eigenvalues": "q (x9, sym-tl), -q^-1 (x6, antisym), q^-3 (x1, singlet)"}

    # ── C. braid (64차원) ─────────────────────────────────────────────────
    Rso4i = sp.simplify(Rso4.inv())
    s1 = kron(Rso4, I4); s2 = kron(I4, Rso4)
    s1i = kron(Rso4i, I4); s2i = kron(I4, Rso4i)

    def MM(*Ms):
        r = Ms[0]
        for M in Ms[1:]:
            r = r * M
        return r
    R["C_braid_relation"] = (sp.simplify(MM(s1, s2, s1) - MM(s2, s1, s2)) == sp.zeros(64, 64))

    # ── D. quantum trace + F ──────────────────────────────────────────────
    muV = sp.diag(q**2, 1, 1, q**-2)
    mu3 = kron(kron(muV, muV), muV)
    gen = {(1, 1): s1, (-1, 1): s1i, (1, 2): s2, (-1, 2): s2i}

    def Fpoly(word):
        M = sp.eye(64); w = 0
        for (sgn, i) in word:
            M = M * gen[(sgn, i)]; w += sgn
        val = sp.together((M * mu3).trace())
        return sp.simplify(a_bmw**(-w) * val / delta), w

    def laurent_t(Fexpr):
        return sp.expand(sp.cancel(Fexpr.subs(p, t**sp.Rational(1, 4))))   # t=q²=p⁴

    F_unlink, _ = Fpoly([])
    R["D_unlink_delta2"] = (sp.simplify(F_unlink - delta**2) == 0)
    F8, w8 = Fpoly([(1, 1), (-1, 2), (1, 1), (-1, 2)])
    R["D_fig8_writhe0"] = (w8 == 0)
    R["D_fig8_amphichiral"] = (sp.simplify(F8 - F8.subs(p, 1 / p)) == 0)
    F8t = laurent_t(F8)
    R["D_fig8_palindromic"] = (sp.simplify(F8t - F8t.subs(t, 1 / t)) == 0)
    Ft, wt = Fpoly([(1, 1), (1, 1), (1, 1)])
    Ftm, _ = Fpoly([(-1, 1), (-1, 1), (-1, 1)])
    R["D_trefoil_chiral"] = (sp.simplify(Ft - Ftm) != 0)
    out["curves_N4"] = {"fig8_F_in_t=q^2": str(F8t), "trefoil_F_in_t=q^2": str(laurent_t(Ft)),
                        "fig8": "palindromic (amphichiral)", "trefoil": "chiral"}

    # ── E. 2변수 복원 현황 (N=3 곡선 하드코드 vs N=4) ────────────────────────
    Q = sp.symbols("Q"); a, z = sp.symbols("a z")
    F3Q = (Q**6 - Q**5 - Q**4 + 2 * Q**3 - Q**2 - Q + 3 - Q**-1 - Q**-2
           + 2 * Q**-3 - Q**-4 - Q**-5 + Q**-6)                     # N=3 (bmw3_kauffman_so3, t→Q)
    F4Q = sp.expand(F8t.subs(t, Q**2))                              # N=4 in Q (t=Q²)
    zc = Q - Q**-1
    terms = [(i, j, sp.Symbol(f"c_{i+3}_{j}")) for i in range(-3, 4) for j in range(0, 7)]
    eqs = []
    for (Fc, ap) in [(F3Q, 2), (F4Q, 3)]:
        expr = sum(c * Q**(ap * i) * zc**j for (i, j, c) in terms)
        eqs += list(sp.Poly(sp.expand((expr - Fc) * Q**40), Q).all_coeffs())
    sol = list(sp.linsolve(eqs, [c for (_, _, c) in terms]))
    R["E_two_curves_consistent"] = bool(sol)
    freev = set()
    if sol:
        for v in sol[0]:
            freev |= v.free_symbols
    R["E_underdetermined_6param"] = (len(freev) == 6)
    # F(a,0)=1 제약을 추가하면 비일관(정규화 미묘성 증거)
    eqs2 = eqs + [dict((tt[:2], tt[2]) for tt in terms)[(i, 0)] - (1 if i == 0 else 0)
                  for i in range(-3, 4)]
    R["E_Fa0_incompatible"] = (len(list(sp.linsolve(eqs2, [c for (_, _, c) in terms]))) == 0)
    out["reconstruction"] = {
        "status": "미완 — 2곡선 동시적합 가능하나 6-파라미터 pure-a 족 잔여",
        "free_params": sorted(str(x) for x in freev),
        "normalization_puzzle": "naive a^-w·RT/δ 결합이 매듭 정리 F(a,0)=1 과 충돌(z=0 곡선상 a=1만 통과)",
        "next": "3번째 곡선(so₅=sp₄/so₆=sl₄) or 도식적 Dubrovnik skein(정의적 2변수)",
    }

    # ── teeth ─────────────────────────────────────────────────────────────
    R["teeth_fig8_palindromic"] = R["D_fig8_palindromic"]
    R["teeth_trefoil_chiral"] = R["D_trefoil_chiral"]
    R["teeth_delta_qdim"] = R["B_delta_eq_qdim"]

    ok = bool(all(R.values()))
    out["checks"] = R
    out["scope_honesty"] = {
        "delivered": "두 번째 검증된 SO(4) 특수화선(a=q³) — 방법 일반성(N=3 우연 아님)",
        "not_yet": "완전 2변수 Kauffman F(a,z) — 정규화 미묘성·6-파라미터 잔여(3번째 곡선/skein 다음)",
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        pth = os.path.join(ROOT, ".pgf", "proofs", "BMW3-KAUFFMAN-SO4.json")
        os.makedirs(os.path.dirname(pth), exist_ok=True)
        with open(pth, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("BMW₃ Kauffman 두 번째 SO(4) 곡선 — so₄=sl₂×sl₂ quantum trace (심볼릭 — seal 아님):",
              flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  ★F(4_1)|N=4 = {F8t}", flush=True)
        print("  ★고유값{q,−q⁻¹,q⁻³}=N=4 BMW·braid 64차원·fig-8 palindromic·trefoil chiral·δ=qdim",
              flush=True)
        print("  ★2변수 복원 미완: 2곡선→6-파라미터 잔여·F(a,0)=1 정규화 미묘성(3번째 곡선/skein 다음)",
              flush=True)
        print("  → .pgf/proofs/BMW3-KAUFFMAN-SO4.json", flush=True)
    print(f"bmw3_kauffman_so4_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
