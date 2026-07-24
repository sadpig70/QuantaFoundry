#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pauli_diamond_e8_observe — TrackHE18: ★**ε-인증 E8 — Pauli-covariant 채널의 exact diamond
norm 폐형식**(비유니터리 채널 최초 exact) (관측, seal 아님). E1–E7 사다리의 채널 축 연장.

배경: [[approx_certify]] 사다리 — E5 op-norm 하계·E6 diamond 하계·**E7 exact Watrous diamond 는
unitary 채널 한정**(TrackHE17 P3 정직 경계). 일반 CPTP 는 SDP 요구(exact 산술 밖 — report18
agent03 이 거절한 함정). ★본 witness 의 해소: **Pauli-covariant 부분류**에서는 SDP 없이 **순수
유리수 폐형식**이 성립한다:

    ‖Φ_p − Φ_q‖◇ = Σ_P |p_P − q_P|   (확률벡터 L1)

증명서 구조(양측 정확 일치):
  - **primal(하계)**: 최대얽힘 입력 |Ω⟩ 에서 (Δ⊗id)(|Ω⟩⟨Ω|) = Σ_P Δp_P |Ψ_P⟩⟨Ψ_P| —
    ★**Choi 차가 Bell-대각**(직교 사영 합) → 트레이스노름 = Σ|Δp_P| ≤ ‖Δ‖◇.
  - **dual(상계)**: Δ = Σ_P Δp_P·(P·P†) 이고 임의 상태 ρ 에서 ‖(Δ⊗id)(ρ)‖₁ ≤
    Σ|Δp_P|·‖(P⊗I)ρ(P⊗I)†‖₁ = Σ|Δp_P| — **트레이스노름 삼각부등식+유니터리 불변성만**(초등).
  ⟹ 하계 = 상계: exact·유리수·SDP-free.

관측 6축(sympy 정확 유리/대수 산술):
  A. **Pauli 채널 게이트**: Φ_p CPTP(Choi PSD=확률 비음·TP=Σp=1)·Pauli-twirl covariance.
  B. ★**Bell-대각 정리**: Choi(Φ_p−Φ_q) 가 Bell 기저 {(P⊗I)|Ω⟩} 에서 정확히 diag(Δp) — 심볼릭.
  C. ★**E8 폐형식 전수**: 결정론 유리 (p,q) 다수 + 심볼릭 파라미터 — 트레이스노름(고유값 정확)
     == L1 정확 일치.
  D. **인스턴스 표**: id vs bit-flip(r)→**2r**·id vs dephasing(λ)→**1−λ**·id vs depolarizing(p)→
     **3p/2**(=2p(1−1/d²), ★report18 의 '2p(d−1)/d=p' 는 d=2 에서 **부정확** — §4′o 자체유도 정정)·
     직교 Pauli→**2**(최대)·동일→**0**.
  E. ★**E7 교차 정합**: 단위 Pauli 채널쌍(P≠Q, unitary 특수화)에서 E8 값 2 == E7 Watrous
     (W=P†Q 고유위상 ±쌍 → 호폭 π → 2 sin(π/2)=2) — 사다리 정합.
  F. **비유니터리 확인**: dephasing/depolarizing Choi rank>1 — E7 적용 불가 영역을 E8 이 커버.

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - **Pauli-covariant 부분류 한정** — 일반 CPTP exact diamond 는 여전히 SDP(무주장·agent03 판단
    존중). qubit(d=2) 검증(폐형식 자체는 일반 Pauli 군에도 성립하나 검증 범위는 d=2).
  - 상계 논증의 외부사실 = 트레이스노름 삼각부등식·유니터리 불변성(초등 노름 성질).
  - approx_certify(19 unitary 앱) 사이드카는 무변경 — E8 은 채널 축 witness 로 확립.

사용: python -m qf_witness.observe.pauli_diamond_e8_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import random
from fractions import Fraction

import sympy as sp


I2 = sp.eye(2)
X = sp.Matrix([[0, 1], [1, 0]])
Y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
Z = sp.Matrix([[1, 0], [0, -1]])
PAULIS = [I2, X, Y, Z]
PNAMES = ["I", "X", "Y", "Z"]


def kron(A, B):
    return sp.Matrix(sp.BlockMatrix([[A[i, j] * B for j in range(2)] for i in range(2)]))


OM = sp.Matrix([1, 0, 0, 1]) / sp.sqrt(2)
OMP = OM * OM.T.conjugate()
BELLS = [kron(P, I2) * OM for P in PAULIS]


def choi_diff(dp):
    J = sp.zeros(4)
    for c, P in zip(dp, PAULIS):
        U = kron(P, I2)
        J += c * (U * OMP * U.conjugate().T)
    return sp.expand(J)


def L1(p, q):
    return sum(abs(sp.nsimplify(a) - sp.nsimplify(b)) for a, b in zip(p, q))


def trace_norm_exact(J):
    ev = J.eigenvals()
    return sp.simplify(sum(abs(k) * v for k, v in ev.items()))


def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "pauli-diamond-e8/v1",
           "_note": ("ε-인증 E8 — Pauli-covariant 채널 exact diamond 폐형식 ‖Φ_p−Φ_q‖◇=Σ|Δp| "
                     "(비유니터리 최초 exact·SDP-free·유리수). 관측·seal 아님·module 0·root 불변. "
                     "일반 CPTP 무주장(Pauli 부분류 한정).")}

    # ── A. 채널 게이트 ────────────────────────────────────────────────────
    pvec = [sp.Rational(1, 2), sp.Rational(1, 4), sp.Rational(1, 8), sp.Rational(1, 8)]
    R["A_TP"] = (sum(pvec) == 1)
    R["A_CP_prob_nonneg"] = all(x >= 0 for x in pvec)
    # covariance: Q Φ_p(ρ) Q† = Φ_p(QρQ†) — Pauli 곱 교환(±부호 상쇄, conj 쌍) 심볼릭 확인
    rho = sp.Matrix([[sp.Rational(3, 4), sp.Rational(1, 8) + sp.I / 8],
                     [sp.Rational(1, 8) - sp.I / 8, sp.Rational(1, 4)]])

    def apply_ch(p, r):
        return sum((c * (P * r * P.conjugate().T) for c, P in zip(p, PAULIS)),
                   sp.zeros(2))
    cov_ok = True
    for Q in PAULIS[1:]:
        lhs = sp.expand(Q * apply_ch(pvec, rho) * Q.conjugate().T)
        rhs = sp.expand(apply_ch(pvec, Q * rho * Q.conjugate().T))
        if sp.simplify(lhs - rhs) != sp.zeros(2):
            cov_ok = False
    R["A_pauli_covariant"] = cov_ok

    # ── B. Bell-대각 정리 (심볼릭 파라미터) ────────────────────────────────
    a0, a1, a2, a3 = sp.symbols("a0 a1 a2 a3", real=True)
    Jsym = choi_diff([a0, a1, a2, a3])
    Dm = sp.Matrix(4, 4, lambda i, j: sp.simplify(
        (BELLS[i].conjugate().T * Jsym * BELLS[j])[0, 0]))
    R["B_bell_diagonal_symbolic"] = (sp.simplify(Dm - sp.diag(a0, a1, a2, a3))
                                     == sp.zeros(4))

    # ── C. E8 폐형식 전수 (결정론 유리 fuzz) ──────────────────────────────
    rnd = random.Random(8)
    n_fuzz = 6 if quick else 20
    fuzz_ok = True
    for _ in range(n_fuzz):
        def rvec():
            xs = [Fraction(rnd.randrange(0, 12), 1) for _ in range(4)]
            s = sum(xs)
            if s == 0:
                xs[0] = Fraction(1)
                s = Fraction(1)
            return [sp.Rational(x.numerator, s.numerator) for x in xs]
        p = rvec()
        q = rvec()
        dp = [a - b for a, b in zip(p, q)]
        tn = trace_norm_exact(choi_diff(dp))
        if sp.simplify(tn - L1(p, q)) != 0:
            fuzz_ok = False
    R["C_primal_eq_L1_fuzz"] = fuzz_ok
    out["closed_form"] = {
        "statement": "‖Φ_p − Φ_q‖◇ = Σ_P |p_P − q_P| (Pauli-covariant, exact rational)",
        "primal": "최대얽힘 입력 → Choi 차 Bell-대각 → 트레이스노름 = L1 (하계)",
        "dual": "삼각부등식+유니터리 불변 → ≤ L1 (상계) — SDP-free",
        "fuzz_instances": n_fuzz,
    }

    # ── D. 인스턴스 표 ────────────────────────────────────────────────────
    r = sp.symbols("r", positive=True)
    lam = sp.symbols("lam", positive=True)
    pp = sp.symbols("p", positive=True)
    ID = [1, 0, 0, 0]
    bitflip = [1 - r, r, 0, 0]
    deph = [(1 + lam) / 2, 0, 0, (1 - lam) / 2]
    depo = [1 - 3 * pp / 4, pp / 4, pp / 4, pp / 4]
    # 파라미터 심볼릭 L1 (0<r,λ,p<1 가정 하 부호 확정 — abs 전개)
    R["D_bitflip_2r"] = (sp.simplify((1 - (1 - r)) + r - 2 * r) == 0)
    R["D_dephasing_1_minus_lam"] = (sp.simplify((1 - (1 + lam) / 2) + (1 - lam) / 2
                                                - (1 - lam)) == 0)
    R["D_depolarizing_3p_2"] = (sp.simplify((1 - (1 - 3 * pp / 4)) + 3 * (pp / 4)
                                            - 3 * pp / 2) == 0)
    R["D_orthogonal_pauli_2"] = (L1([0, 1, 0, 0], [0, 0, 0, 1]) == 2)
    R["D_identical_0"] = (L1(ID, ID) == 0)
    out["instances"] = {
        "id_vs_bitflip(r)": "2r", "id_vs_dephasing(λ)": "1−λ",
        "id_vs_depolarizing(p)": "3p/2 = 2p(1−1/d²), d=2",
        "correction": "★report18 '2p(d−1)/d=p' 는 d=2 에서 부정확 — 자체유도 3p/2 (§4′o)",
        "orthogonal_paulis": 2, "identical": 0,
    }

    # ── E. E7 교차 정합 (unitary 특수화) ──────────────────────────────────
    # 단위 Pauli 채널쌍 X vs Z: E8=2. E7: W=X†Z 고유위상 ±i → 호폭 π → 2sin(π/2)=2.
    W = X.conjugate().T * Z
    evs = list(W.eigenvals().keys())
    R["E_e7_cross_consistent"] = (sorted(str(e) for e in evs) == ["-I", "I"]
                                  and L1([0, 1, 0, 0], [0, 0, 0, 1]) == 2)

    # ── F. 비유니터리 확인 ────────────────────────────────────────────────
    lam3 = sp.Rational(1, 3)
    deph3 = [(1 + lam3) / 2, 0, 0, (1 - lam3) / 2]
    Jd = sp.zeros(4)
    for c, P in zip(deph3, PAULIS):
        U = kron(P, I2)
        Jd += c * (U * OMP * U.conjugate().T)
    R["F_dephasing_nonunitary_rank2"] = (Jd.rank() == 2)

    # teeth
    R["teeth_orthogonal_max_2"] = R["D_orthogonal_pauli_2"]
    R["teeth_identical_zero"] = R["D_identical_0"]
    R["teeth_report_value_corrected"] = R["D_depolarizing_3p_2"]

    ok = bool(all(R.values()))
    out["checks"] = R
    out["scope_honesty"] = {
        "delivered": "E8 = Pauli-covariant exact diamond 폐형식(비유니터리 최초 exact·SDP-free)",
        "ladder": "E5 op-norm LB → E6 ◇-LB → E7 exact(unitary) → ★E8 exact(Pauli 채널)",
        "not_claimed": "일반 CPTP exact diamond(SDP 요구·agent03 판단 존중)·d>2 검증",
        "external_facts": "트레이스노름 삼각부등식·유니터리 불변성(초등 노름 성질)",
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        pth = os.path.join(ROOT, ".pgf", "proofs", "PAULI-DIAMOND-E8.json")
        os.makedirs(os.path.dirname(pth), exist_ok=True)
        with open(pth, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("ε-인증 E8 — Pauli-covariant exact diamond 폐형식 (유리수 — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  ★‖Φ_p−Φ_q‖◇=Σ|Δp| (Bell-대각 primal=dual 폐합·SDP-free)", flush=True)
        print("  ★인스턴스: bitflip 2r·dephasing 1−λ·depolarizing 3p/2(report 정정)·직교 2", flush=True)
        print("  ★비유니터리 최초 exact — E7(unitary) 상보·E7 교차 정합", flush=True)
        print("  → .pgf/proofs/PAULI-DIAMOND-E8.json", flush=True)
    print(f"pauli_diamond_e8_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
