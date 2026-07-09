#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""su2_4_mtc_observe — 완전 Modular Tensor Category SU(2)₄ modular data 자체검증 witness
(관측, seal 아님).

TrackHE13 P6: su2_3_mtc_observe(k=3, Fibonacci τ 포함 ℚ(√5)/ζ₂₀)의 **k=4 형제**. SU(2)₄의
전체 modular data(S·T + 공리)를 exact ℚ(√3)/ζ₂₄ (sympy)로 검증.

★외부 정정(선검증): 두 외부 런타임이 SU(2)₄의 quantum dims를 "d=(1,√2,√3,√2,1), D²=8"로 주장.
표준 공식 d_j = sin((2j+1)π/6)/sin(π/6) 로 자체 재유도하면 실제는 **d=(1,√3,2,√3,1), D²=12**.
(더구나 외부가 든 dims (1,√2,√3,√2,1)의 제곱합은 1+2+3+2+1=9 로 자기 주장 D²=8 과도 불일치.) 정정 기록.

SU(2)₄ anyon: j∈{0,1/2,1,3/2,2} → label a=2j∈{0,1,2,3,4}(5개). k=4, k+2=6.

관측(exact modular data · 공리):
  1. **S-matrix** S_{ab}=√(2/6)·sin((2a+1)(2b+1)π/6): 실대칭·**unitary**(SS†=I)·**S²=C**(charge conj;
     SU(2)_k self-dual → C=I 확인).
  2. **quantum dims** d_a=S_{0a}/S_{00}=sin((2a+1)π/6)/sin(π/6) → (1, √3, 2, √3, 1).
     **total D²=Σd_a²=12**(=6/(2sin²(π/6)), 양수). ★j=1 anyon(label 2)의 d=2 = **정수**
     → fusion 1×1=0+1+2 = **비-Fibonacci**(SU(2)₄ = ℤ₃-parafermion/metaplectic 구조).
  3. **T-matrix** T_{ab}=δ_{ab}exp(2πi(h_a−c/24)), h_a=j(j+1)/6, c=3k/(k+2)=2. topological spin
     θ_a=exp(2πi h_a) ∈ ζ₂₄. **(ST)³=S²**(sibling 관례: c/24 보정으로 위상 상쇄→exact)·T 유한위수(T²⁴=I).
     별도로 **미보정 (ST̃)³=e^{2πi c/8}S²=i·S²** 로 중심전하 c=2 명시.
  4. **Verlinde 융합** N_{ab}^c=Σ_x S_{ax}S_{bx}S*_{cx}/S_{0x}: **모든 N 비음 정수**. k=4 절단:
     ½×½=0+1 · 1×1=0+1+2 · 3/2×3/2=0+1 · **2×2=0**(최고스핀 self-fusion 절단).
  5. **field**: S/S_{00} 전 성분 ∈ ℚ(√3); θ_a ∈ 24차 cyclotomic. exact.
     대비: SU(2)₃ = ℚ(√5)/ζ₂₀ vs **SU(2)₄ = ℚ(√3)/ζ₂₄**.
  6. teeth: (a) 외부 오류값 d=(1,√2,√3,√2,1) → fusion 고유벡터 관계 d_a d_b=Σ_c N_{ab}^c d_c
     **위배**(외부오류 실증) · (b) S 한 성분 섭동 → unitarity 붕괴 · (c) 잘못된 level(분모 7)→Verlinde
     비정수 · (d) 정규화 제거→S²≠C.

정직 경계(★관측·seal 아님, root 불변 sidecar·신규 module 0):
  witness = SU(2)₄ modular data(S/T)의 MTC 공리(unitarity·S²=C·Verlinde 정수·k=4 fusion 절단·
  total dimension·modular (ST)³=S²·중심전하 c=2)를 exact 대수(ℚ(√3)/ζ₂₄)로 자체검증. F/R symbol
  pentagon·hexagon 열거는 braid 표현 계층 소관(범위 밖). 위상값의 module 봉인(ζ₂₄ 등)은 범위밖(사람게이트).
  [[su2-3-mtc-observe]](HE12 P4, k=3 형제)·[[mtc-braid-observe]]·[[ising-fusion-observe]] 교차.

사용: python scripts/su2_4_mtc_observe.py [--quick]
"""
from __future__ import annotations
import json
import os
import sys
import sympy as sp

I = sp.I
PI = sp.pi
LABELS = (0, 1, 2, 3, 4)        # a = 2j, j∈{0,1/2,1,3/2,2}
K = 4
KK = K + 2                      # = 6
DENOM = KK                      # S-matrix 분모


def _m(a):
    """label a → 2j+1 = a+1 (∈ {1,...,5})."""
    return a + 1


def s_matrix(denom):
    """S_{ab}=√(2/denom)·sin((a+1)(b+1)π/denom) (exact sympy)."""
    return sp.Matrix(5, 5, lambda a, b:
                     sp.sqrt(sp.Rational(2, denom)) * sp.sin(_m(a) * _m(b) * PI / denom))


def czero(z):
    """복소 수식이 0 인지: 우선 exact simplify, 실패 시 고정밀 evalf(35)로 판정
    (입력이 exact 대수수이므로 evalf 비교는 엄밀)."""
    zs = sp.simplify(z)
    if zs == 0:
        return True
    return abs(complex(zs.evalf(35))) < sp.Float("1e-28")


def mat_zero(M):
    """행렬이 영행렬인지 entrywise czero."""
    return all(czero(M[i, j]) for i in range(M.rows) for j in range(M.cols))


def verlinde_entry(S, a, b, c):
    """N_{ab}^c = Σ_x S_ax S_bx S*_cx / S_0x (exact)."""
    return sp.simplify(sum(S[a, x] * S[b, x] * sp.conjugate(S[c, x]) / S[0, x] for x in LABELS))


def main():
    quick = "--quick" in sys.argv
    R = {}
    sqrt3 = sp.sqrt(3)

    # ── 1. S-matrix + unitarity + S² = charge conjugation ──
    S = sp.simplify(s_matrix(DENOM))
    R["S_real_symmetric"] = bool(S == S.T and all(sp.im(S[i, j]) == 0 for i in range(5) for j in range(5)))
    R["S_unitary"] = bool(mat_zero(S * S.conjugate().T - sp.eye(5)))
    S2 = S * S
    # charge conjugation C = S² (정수행렬로 반올림 후 exact 재확인)
    C = sp.Matrix(5, 5, lambda i, j: sp.Integer(round(float(S2[i, j].evalf(35).as_real_imag()[0]))))
    R["S_squared_charge_conj"] = bool(mat_zero(S2 - C) and mat_zero(C * C - sp.eye(5)))
    R["charge_conj_identity_selfdual"] = bool(C == sp.eye(5))     # SU(2)_k self-dual → C=I

    # ── 2. quantum dimensions + total dimension ──
    d = [sp.simplify(S[0, a] / S[0, 0]) for a in LABELS]
    R["quantum_dims_sqrt3"] = bool(d == [sp.Integer(1), sqrt3, sp.Integer(2), sqrt3, sp.Integer(1)])
    D2 = sp.simplify(sum(x ** 2 for x in d))
    R["total_D2_eq_12"] = bool(D2 == 12 and sp.simplify(D2 - KK / (2 * sp.sin(PI / KK) ** 2)) == 0)
    R["d_j1_integer_nonfibonacci"] = bool(d[2] == 2)             # ★j=1 anyon d=2 (정수, 비-Fibonacci)

    # ── 3. T-matrix / topological spin / modular (ST)³ = S² / 중심전하 c=2 ──
    h = [sp.Rational(0), sp.Rational(1, 8), sp.Rational(1, 3), sp.Rational(5, 8), sp.Integer(1)]  # h_a=j(j+1)/6
    c = sp.Integer(3) * K / KK                                   # 중심전하 = 12/6 = 2
    theta = [sp.exp(2 * I * PI * hh) for hh in h]                # topological spin θ_a
    Tu = sp.diag(*theta)                                         # 미보정 T̃
    T = sp.diag(*[sp.exp(2 * I * PI * (hh - c / 24)) for hh in h])  # c/24 보정 (sibling 관례)
    R["topological_spin_cyclotomic"] = bool(mat_zero(Tu ** 24 - sp.eye(5)))   # θ_a ∈ ζ₂₄
    R["ST_cubed_modular"] = bool(mat_zero((S * T) ** 3 - S2))    # (ST)³ = S²
    R["central_charge_c2"] = bool(mat_zero((S * Tu) ** 3 - sp.exp(2 * I * PI * c / 8) * S2))  # (ST̃)³=e^{2πic/8}S²=iS²
    R["T_finite_order"] = bool(mat_zero(T ** 24 - sp.eye(5)))    # T²⁴ = I

    # ── 4. Verlinde 융합: 비음 정수 + k=4 절단 규칙 ──
    Nr = {}
    all_int_nonneg = True
    for a in LABELS:
        for b in LABELS:
            for cc in LABELS:
                val = verlinde_entry(S, a, b, cc)
                iv = sp.nsimplify(val, rational=True)
                is_int = iv.is_integer and iv >= 0
                all_int_nonneg = all_int_nonneg and bool(is_int)
                Nr[(a, b, cc)] = int(iv) if iv.is_integer else None
    R["verlinde_nonneg_integer"] = bool(all_int_nonneg)
    # ½×½ = 0+1 (labels {0,2}) · 1×1 = 0+1+2 (labels {0,2,4}) · 3/2×3/2 = 0+1 (labels {0,2}) · 2×2 = 0
    R["fusion_half_half"] = bool(Nr[(1, 1, 0)] == 1 and Nr[(1, 1, 2)] == 1
                                 and all(Nr[(1, 1, x)] == 0 for x in (1, 3, 4)))
    R["fusion_one_one"] = bool(Nr[(2, 2, 0)] == 1 and Nr[(2, 2, 2)] == 1 and Nr[(2, 2, 4)] == 1
                               and all(Nr[(2, 2, x)] == 0 for x in (1, 3)))
    R["fusion_threehalf"] = bool(Nr[(3, 3, 0)] == 1 and Nr[(3, 3, 2)] == 1
                                 and all(Nr[(3, 3, x)] == 0 for x in (1, 3, 4)))
    R["fusion_two_two_truncation"] = bool(Nr[(4, 4, 0)] == 1
                                          and all(Nr[(4, 4, x)] == 0 for x in (1, 2, 3, 4)))
    R["fusion_identity_symmetric"] = bool(all(Nr[(0, a, a)] == 1 for a in LABELS)
                                          and all(Nr[(a, b, cc)] == Nr[(b, a, cc)]
                                                  for a in LABELS for b in LABELS for cc in LABELS))

    # ── 5. field: S/S₀₀ ∈ ℚ(√3), θ ∈ ζ₂₄ ──
    M = sp.simplify(S / S[0, 0])
    allowed = [sp.Integer(0), sp.Integer(1), sp.Integer(-1), sp.Integer(2), sp.Integer(-2), sqrt3, -sqrt3]
    R["field_Q_sqrt3_cyclotomic"] = bool(
        all(sp.simplify(M[i, j]) in allowed for i in range(5) for j in range(5))
        and mat_zero(Tu ** 24 - sp.eye(5)))

    # ── 6. teeth ──
    # (a) 외부 오류값 d=(1,√2,√3,√2,1): fusion 고유벡터 관계 d_a d_b = Σ_c N_{ab}^c d_c 위배
    #     (정상 d 는 전부 만족 → 외부 dims 가 실제 MTC 와 불일치함을 실증)
    def fusion_consistent(dv):
        return all(sp.simplify(dv[a] * dv[b] - sum(Nr[(a, b, cc)] * dv[cc] for cc in LABELS)) == 0
                   for a in LABELS for b in LABELS)
    d_ext = [sp.Integer(1), sp.sqrt(2), sqrt3, sp.sqrt(2), sp.Integer(1)]  # 외부 주장(오류)
    R["teeth_external_dims_fail"] = bool(fusion_consistent(d) and not fusion_consistent(d_ext))
    # (b) S 한 성분 섭동 → unitarity 붕괴 (control)
    Sp = sp.Matrix(S)                       # mutable 사본
    Sp[0, 1] = Sp[0, 1] + sp.Rational(1, 10)
    R["teeth_perturbed_S_breaks_unitarity"] = bool(not mat_zero(Sp * Sp.conjugate().T - sp.eye(5)))
    # (c) 잘못된 level(분모 7) → Verlinde 비정수
    Sw = sp.simplify(s_matrix(7))
    Nw = verlinde_entry(Sw, 1, 1, 1)
    R["teeth_wrong_level_noninteger"] = bool(not sp.nsimplify(Nw, rational=True).is_integer)
    # (d) 정규화 제거(√(2/6) 없음) → S² ≠ C
    Su = sp.Matrix(5, 5, lambda a, b: sp.sin(_m(a) * _m(b) * PI / DENOM))
    R["teeth_unnormalized_breaks_S2"] = bool(not mat_zero(Su * Su - C))

    ok = all(R.values())

    # ── 관측 요약 / 출력 ──
    theta_str = "(1, e^(iπ/4), e^(2πi/3), e^(-3πi/4), 1) ∈ ζ₂₄"
    if not quick:
        print("SU(2)₄ 완전 MTC modular data(S·T) 공리 관측 (witness — seal 아님):", flush=True)
        for kk_, v in R.items():
            print(f"  {kk_}: {v}", flush=True)
        print(f"  quantum dims d=(1,√3,2,√3,1) · total D²={D2}=12 (=6/(2sin²(π/6))) · "
              f"θ={theta_str} · c={c}", flush=True)
        print("  fusion(k=4 절단): ½×½=0+1 · 1×1=0+1+2 · 3/2×3/2=0+1 · 2×2=0 "
              "(★j=1 anyon d=2 정수 → 비-Fibonacci·ℤ₃-parafermion/metaplectic)", flush=True)
        print("  ★외부정정: 외부 주장 d=(1,√2,√3,√2,1)·D²=8 (⇒제곱합 9, 자기모순) vs 진실 "
              "d=(1,√3,2,√3,1)·D²=12 (teeth_external_dims_fail 로 실증)", flush=True)
        print("  대비 field: SU(2)₃ = ℚ(√5)/ζ₂₀ vs SU(2)₄ = ℚ(√3)/ζ₂₄", flush=True)
        print("  ★정직: 관측=SU(2)₄ modular data의 MTC 공리(unitarity·S²=C·Verlinde 정수·k=4 fusion 절단·"
              "total dim·(ST)³=S²·중심전하 c=2) exact ℚ(√3)/ζ₂₄ 자체검증.", flush=True)
        print("  봉인 아님 — F/R symbol pentagon/hexagon=braid 계층 소관·위상값 module(ζ₂₄)=범위밖(사람게이트)"
              "·신규 module 0·root 불변 sidecar.", flush=True)

    # ── sidecar JSON ──
    fusion_table = {
        "half_x_half": "½×½ = 0 + 1",
        "one_x_one": "1×1 = 0 + 1 + 2 (★비-Fibonacci)",
        "threehalf_x_threehalf": "3/2×3/2 = 0 + 1",
        "two_x_two": "2×2 = 0 (최고스핀 self-fusion 절단)",
    }
    sidecar = {
        "_note": "SU(2)₄ 완전 MTC modular data(S·T + 공리) exact ℚ(√3)/ζ₂₄ 자체검증 witness. "
                 "관측 — 신규 module 0 · root 불변. 봉인 아님(F/R pentagon/hexagon=범위 밖).",
        "_schema": "su2-4-mtc-observe-v1",
        "observation": {
            "anyons": "j∈{0,1/2,1,3/2,2} → label a=2j∈{0,1,2,3,4} (5개), k=4, k+2=6",
            "quantum_dims": "d=(1,√3,2,√3,1)",
            "total_quantum_dimension_D2": 12,
            "d_j1_integer": "★j=1 anyon(label 2) d=2 = 정수 → 1×1=0+1+2 = 비-Fibonacci "
                            "(SU(2)₄ = ℤ₃-parafermion/metaplectic 구조)",
            "central_charge_c": 2,
            "topological_spin": "θ=(1, e^(iπ/4), e^(2πi/3), e^(-3πi/4), 1) ∈ ζ₂₄",
            "charge_conjugation": "C = S² = I (SU(2)_k self-dual)",
            "fusion_rules": fusion_table,
            "field": "S/S₀₀ ∈ ℚ(√3) · θ ∈ ζ₂₄",
            "field_contrast": "SU(2)₃ = ℚ(√5)/ζ₂₀ vs SU(2)₄ = ℚ(√3)/ζ₂₄",
            "external_error_corrected": {
                "선검증_정정": "외부 두 런타임의 quantum-dims 주장 정정",
                "external_claim": "d=(1,√2,√3,√2,1), D²=8",
                "external_self_inconsistency": "주장 dims (1,√2,√3,√2,1)의 제곱합 = 1+2+3+2+1 = 9 ≠ "
                                               "자기 주장 D²=8 (외부 주장 내부 모순)",
                "truth": "d=(1,√3,2,√3,1), D²=12 (표준 공식 d_j=sin((2j+1)π/6)/sin(π/6) 자체 재유도)",
                "demonstrated_by": "teeth_external_dims_fail — 외부 dims 가 exact Verlinde N 의 "
                                   "fusion 고유벡터 관계 d_a d_b=Σ_c N_{ab}^c d_c 를 위배",
            },
            "axioms_verified": {k: v for k, v in R.items() if not k.startswith("teeth")},
            "teeth": {k: v for k, v in R.items() if k.startswith("teeth")},
            "honest_boundary": "관측 — SU(2)₄ modular data(S/T)의 MTC 공리를 exact ℚ(√3)/ζ₂₄ 로 "
                               "자체검증. 게이트 봉인 아님 · F/R symbol pentagon/hexagon=braid 표현 계층 "
                               "소관(범위 밖) · 위상값 module 봉인=사람게이트 · 신규 module 0 · root 불변.",
            "seal_links": "[[su2-3-mtc-observe]] (k=3 형제) · [[mtc-braid-observe]] · [[ising-fusion-observe]]",
            "ok": bool(ok),
        },
        "deterministic": True,
    }
    out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            ".pgf", "proofs", "SU2-4-MTC-OBSERVE.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(sidecar, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")

    print(f"su2_4_mtc_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
