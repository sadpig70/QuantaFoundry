#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bmw3_kauffman_so3_observe — TrackHE18 P1: BMW₃ Markov-trace crux **방법 해결** —
U_q(sl₂) spin-1(=so₃ 벡터표현) universal R-matrix + **ribbon pivotal quantum trace**
로 figure-8 / trefoil 의 Kauffman 다항식(SO(3) 특수화선)을 관측 (seal 아님).

배경(crux): [[bmw3_fig8_observe]](TrackHE16 P3)가 fig-8 Jones(1변수)를 Kauffman bracket 으로
관측하고 "2변수 Kauffman F via BMW₃ Markov trace"를 다음으로 남겼다. TrackHE17 P1 은 **추상 BMW₃**
곱셈(dim 15·결합)까지 성공했으나 **Markov trace 를 cyclicity-nullspace 풀이로 얻는 데 실패**(핀 선택이
아니라 상호작용 관계식 미확정). report18 agent08 이 (Q1) g−g⁻¹=z(1−e) 가 trace 섹터를 위반한다고
진단(정확 (Q1′)), 그러나 상호작용 관계식은 여전히 미확인 → **SO(N) R-matrix 완전구현** 요구.

★**본 witness 의 해결**: 추상 cyclicity-solve 를 **버리고**, so₃ 벡터표현의 **구체 R-matrix + ribbon
pivotal μ 로 quantum trace 를 구성**한다. quantum trace 는 **Markov 성질이 자동**(pivotal 대각가중
tr_q(x)=Tr(x·μ^{⊗n}))이라 cyclicity-풀이가 원천적으로 불필요 — crux 우회.

관측 6축(sympy 심볼릭 q — exact):
  A. **U_q(sl₂) spin-1 universal R-matrix**: E,F,K 3×3 자체구성·[E,F]=(K−K⁻¹)/(q−q⁻¹)·KEK⁻¹=q²E
     검증. universal R=q^{H⊗H/2}Σ_{n≤2}(q−q⁻¹)ⁿ/[n]!·q^{n(n−1)/2}Eⁿ⊗Fⁿ → Ř=flip∘R(9×9).
  B. **★so₃ BMW 고유값**: Ř 고유값 = **q²(×5, sym-traceless), −q⁻²(×3, antisym), q⁻⁴(×1, singlet)**
     = BMW 표준 {Q, −Q⁻¹, Q^{1−N}} (Q:=q², N=3). ⟹ BMW 파라미터 **a=Q^{N−1}=q⁴, z=Q−Q⁻¹=q²−q⁻²**.
     ★일관성: δ=(a−a⁻¹)/z+1 = q²+1+q⁻² = **qdim(V₁)=[3]_q** (loop value == 양자차원, 정확 일치).
  C. **braid 관계(27차원)**: σ₁=Ř⊗I, σ₂=I⊗Ř 로 **σ₁σ₂σ₁=σ₂σ₁σ₂** 심볼릭 검증(Yang-Baxter).
  D. **★quantum trace(Markov 자동)**: μ=diag(q²,1,q⁻²)(pivotal K_{2ρ})·tr_q(x)=Tr(x·μ^{⊗3}).
     Kauffman F(L)=a^{−w}·tr_q(ρ(β))/δ (w=writhe). **3-unlink=δ²**(보정)·**F(unknot)=1**.
  E. **★figure-8 = closure (σ₁σ₂⁻¹)²** (w=0): F(4₁)|_{SO(3)} = t⁶−t⁵−t⁴+2t³−t²−t+3−t⁻¹−t⁻²
     +2t⁻³−t⁻⁴−t⁻⁵+t⁻⁶ (t=q²) — **완전 palindromic(t↔1/t) ⟺ amphichiral F(a,z)=F(a⁻¹,z)**
     (fig-8 = 트랙 최초 amphichiral 매듭·[[bmw3_fig8_observe]] Jones-amphichiral 의 Kauffman 승격).
     진짜 Laurent(분모 monomial) 확인.
  F. **trefoil = closure σ₁³**(w=3) **chiral**: F(3₁)≠F(3₁의 거울=σ₁⁻³)(정량)·Laurent.
  teeth: (i) fig-8 palindromic vs trefoil 비대칭(amphichiral↔chiral 판별) (ii) δ==qdim (iii) braid.

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - ★**crux 는 방법(quantum trace)으로 해결**했으나 결과는 **SO(3) 특수화선 F|_{a=q⁴,z=q²−q⁻²}**
    (단일 q 의 1변수 Laurent) — **완전 2변수 Kauffman F(a,z) 아님**. 완전 2변수는 다중 N(so_N 벡터표현)
    보간 또는 추상 BMW₃ Markov trace 필요 = **다음 단계**(본 witness 로 방법·N=3 검증 앵커 확보).
  - Ř·quantum trace 는 exact 심볼릭(sympy) — braid/amphichiral/chiral 은 대수 항등식(관측). 게이트
    유니터리 실봉인 무주장(Kauffman 다항식은 불변량 관측).
  - spin-1 invariant = SO(3) colored — ordinary Jones([[bmw3_fig8_observe]])와 다른 특수화(별개 앵커).

사용: python -m qf_witness.observe.bmw3_kauffman_so3_observe [--quick]
"""
from __future__ import annotations
import sys
import json

import sympy as sp


def _build():
    q = sp.symbols("q")

    def qn(n):
        return sp.simplify((q**n - q**(-n)) / (q - 1 / q))

    s2 = sp.sqrt(qn(2))
    # spin-1 U_q(sl2): 기저 |1>,|0>,|-1> (m=1,0,-1)
    E = sp.zeros(3); F = sp.zeros(3)
    E[0, 1] = s2; E[1, 2] = s2          # raise: <1|E|0>, <0|E|-1>
    F[1, 0] = s2; F[2, 1] = s2          # lower
    K = sp.diag(q**2, 1, q**-2)         # K=q^H, H=diag(2,0,-2)
    I3 = sp.eye(3)

    def kron(A, B):
        return sp.Matrix(sp.BlockMatrix([[A[i, j] * B for j in range(A.cols)]
                                         for i in range(A.rows)]))

    def En(M, n):
        R = sp.eye(3)
        for _ in range(n):
            R = R * M
        return R

    def qfact(n):
        r = sp.Integer(1)
        for kk in range(1, n + 1):
            r *= qn(kk)
        return r

    # universal R = q^{H⊗H/2} Σ_{n=0}^{2} (q−q⁻¹)ⁿ/[n]! q^{n(n−1)/2} Eⁿ⊗Fⁿ
    mm = [1, 0, -1]
    D = sp.zeros(9)
    for i, mi in enumerate(mm):
        for j, mj in enumerate(mm):
            D[3 * i + j, 3 * i + j] = q**(2 * mi * mj)
    Rsum = sp.zeros(9)
    for n in range(0, 3):
        Rsum += (q - 1 / q)**n / qfact(n) * q**sp.Rational(n * (n - 1), 2) * kron(En(E, n), En(F, n))
    R = sp.simplify(D * Rsum)
    P = sp.zeros(9)
    for i in range(3):
        for j in range(3):
            P[3 * i + j, 3 * j + i] = 1
    Rc = sp.simplify(P * R)             # 9×9 braiding Ř
    return q, E, F, K, I3, kron, Rc


def main():
    quick = "--quick" in sys.argv
    q, E, F, K, I3, kron, Rc = _build()
    R = {}
    out = {"_schema": "bmw3-kauffman-so3/v1",
           "_note": ("BMW₃ Markov-trace crux 방법 해결 — U_q(sl₂) spin-1 R-matrix + ribbon pivotal "
                     "quantum trace(Markov 자동). fig-8 amphichiral/trefoil chiral Kauffman(SO(3) "
                     "특수화선). 관측·seal 아님·module 0·root 불변. 완전 2변수 F(a,z)=다중 N 다음단계.")}
    t = sp.symbols("t")

    # ── A. quantum group 관계 ─────────────────────────────────────────────
    R["A_EF_relation"] = (sp.simplify(E * F - F * E - (K - K.inv()) / (q - 1 / q)) == sp.zeros(3))
    R["A_KEK_q2E"] = (sp.simplify(K * E * K.inv() - q**2 * E) == sp.zeros(3))

    # ── B. so₃ BMW 고유값 + a,z,δ ─────────────────────────────────────────
    ev = Rc.eigenvals()
    evset = {sp.simplify(v): m for v, m in ev.items()}
    exp_ev = {sp.simplify(q**2): 5, sp.simplify(-q**-2): 3, sp.simplify(q**-4): 1}
    R["B_eigenvalues_so3"] = all(any(sp.simplify(k - ek) == 0 and m == em for k, m in evset.items())
                                 for ek, em in exp_ev.items())
    a_bmw = q**4; z_bmw = q**2 - q**-2
    delta = q**2 + 1 + q**-2
    R["B_delta_eq_qdim"] = (sp.simplify((a_bmw - 1 / a_bmw) / z_bmw + 1 - delta) == 0)
    out["bmw_params"] = {"a": "q^4 = Q^(N-1), N=3", "z": "q^2 - q^-2 = Q - Q^-1",
                         "delta": "q^2+1+q^-2 = [3]_q = qdim(V_1)",
                         "eigenvalues": "q^2 (x5, sym), -q^-2 (x3, antisym), q^-4 (x1, singlet)"}

    # ── C. braid (27차원) ─────────────────────────────────────────────────
    Rci = sp.simplify(Rc.inv())
    s1 = kron(Rc, I3); s2 = kron(I3, Rc)
    s1i = kron(Rci, I3); s2i = kron(I3, Rci)

    def MM(*Ms):
        r = Ms[0]
        for M in Ms[1:]:
            r = r * M
        return r
    R["C_braid_relation"] = (sp.simplify(MM(s1, s2, s1) - MM(s2, s1, s2)) == sp.zeros(27, 27))

    # ── D. quantum trace + F ──────────────────────────────────────────────
    mu = sp.diag(q**2, 1, q**-2)
    mu3 = kron(kron(mu, mu), mu)
    gen = {(1, 1): s1, (-1, 1): s1i, (1, 2): s2, (-1, 2): s2i}

    def Fpoly(word):
        M = sp.eye(27); w = 0
        for (sgn, i) in word:
            M = M * gen[(sgn, i)]; w += sgn
        val = sp.simplify((M * mu3).trace())
        return sp.simplify(a_bmw**(-w) * val / delta), w

    def laurent_t(Fexpr):
        ft = sp.cancel(sp.together(Fexpr.subs(q, sp.sqrt(t))))
        return sp.expand(sp.cancel(ft))

    F_unlink, _ = Fpoly([])                         # B3 identity = 3-unlink
    R["D_unlink_delta2"] = (sp.simplify(F_unlink - delta**2) == 0)   # 보정: F(unknot)=1 ⟹ 3-unlink=δ²

    # ── E. figure-8 (amphichiral) ─────────────────────────────────────────
    F8, w8 = Fpoly([(1, 1), (-1, 2), (1, 1), (-1, 2)])
    R["E_fig8_writhe0"] = (w8 == 0)
    R["E_fig8_amphichiral"] = (sp.simplify(F8 - F8.subs(q, 1 / q)) == 0)    # F(a,z)=F(a^-1,z)
    F8t = laurent_t(F8)
    n8, d8 = sp.fraction(sp.cancel(sp.together(F8.subs(q, sp.sqrt(t)))))
    R["E_fig8_laurent"] = (not d8.free_symbols) or sp.Poly(d8, t).is_monomial
    R["E_fig8_palindromic"] = (sp.simplify(F8t - F8t.subs(t, 1 / t)) == 0)
    out["fig8"] = {"knot": "4_1 = closure (σ1 σ2^-1)^2", "writhe": w8,
                   "F_so3_in_t=q^2": str(F8t),
                   "amphichiral": "palindromic t↔1/t ⟺ F(a,z)=F(a^-1,z)"}

    # ── F. trefoil (chiral) ───────────────────────────────────────────────
    Ft, wt = Fpoly([(1, 1), (1, 1), (1, 1)])
    Ftm, _ = Fpoly([(-1, 1), (-1, 1), (-1, 1)])
    R["F_trefoil_chiral"] = (sp.simplify(Ft - Ftm) != 0)
    ntf, dtf = sp.fraction(sp.cancel(sp.together(Ft.subs(q, sp.sqrt(t)))))
    R["F_trefoil_laurent"] = (not dtf.free_symbols) or sp.Poly(dtf, t).is_monomial
    R["F_amphichiral_vs_chiral"] = (R["E_fig8_amphichiral"] and R["F_trefoil_chiral"])
    out["trefoil"] = {"knot": "3_1 = closure σ1^3", "writhe": wt,
                      "F_so3_in_t=q^2": str(laurent_t(Ft)),
                      "mirror_F": str(laurent_t(Ftm)), "chiral": "F ≠ F(mirror)"}

    # ── teeth ─────────────────────────────────────────────────────────────
    R["teeth_amphichiral_chiral_discriminate"] = (R["E_fig8_amphichiral"] and R["F_trefoil_chiral"])
    R["teeth_delta_qdim"] = R["B_delta_eq_qdim"]
    R["teeth_braid"] = R["C_braid_relation"]

    ok = bool(all(R.values()))
    out["checks"] = R
    out["scope_honesty"] = {
        "resolved": "crux 방법 = ribbon pivotal quantum trace(Markov 자동), cyclicity-solve 우회",
        "delivered": "SO(3) 특수화선 F|_{a=q^4,z=q^2-q^-2} — fig-8 amphichiral·trefoil chiral 검증",
        "not_yet": "완전 2변수 Kauffman F(a,z) = 다중 N(so_N) 보간 or 추상 BMW₃ trace (다음 단계)",
        "distinct_from": "spin-1 SO(3) colored — ordinary Jones(bmw3_fig8_observe)와 별개 특수화",
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "BMW3-KAUFFMAN-SO3.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("BMW₃ Kauffman crux 방법 해결 — U_q(sl₂) spin-1 quantum trace (심볼릭 — seal 아님):",
              flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  ★F(4_1)|SO(3) = {F8t}", flush=True)
        print("  ★fig-8 palindromic(amphichiral)·trefoil chiral·braid·δ=qdim·quantum trace Markov 자동",
              flush=True)
        print("  ★crux 방법 해결(cyclicity-solve 우회)·완전 2변수는 다중 N 다음단계", flush=True)
        print("  → .pgf/proofs/BMW3-KAUFFMAN-SO3.json", flush=True)
    print(f"bmw3_kauffman_so3_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
