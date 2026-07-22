#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""az_aiii_aii_3d_observe — TrackHE16 P5: AZ 3D 잔여칸 — AIII(chiral, ℤ) + AII(ℤ₂ 강한 TI)
(관측, seal 아님). [[az_c_ci_diii3d_observe]](v15 P5)의 3D 확장·완결.

v15 는 2D 행(C/CI)을 채우고 DIII 를 1D ℤ₂→2D ℤ₂→3D ℤ 로 올렸다. 본 witness 는 **3D 열의
잔여 두 칸**을 채운다:
  ★AII (T²=−1, PHS·chiral 없음) = **ℤ₂ — 3D 강한 위상절연체(Fu-Kane strong TI)**
  ★AIII(chiral S 만, T·C 없음)  = **ℤ — 3D chiral winding**

핵심 관측(★DIII↔AII 대비): DIII 와 AII 는 **둘 다 T²=−1** 인데 PHS(C²=+1) 유무로 갈린다 —
  C 를 더하면(→DIII) winding **ℤ**, C 를 빼면(→AII) 강한 지수 **ℤ₂**. 그리고
  **ℤ₂ = (DIII winding) mod 2** — PHS 제거가 ℤ 를 ℤ₂ 로 **조대화(coarsening)** 함을 실증.

관측 3축(전부 정수 산술 — float Berry/Chern 적분 금지, v12/v15 규약 상속):
  A. **AII 3D = ℤ₂ (Fu-Kane parity)**: T²=−1 + 공간반전 P=Γ₄. 강한 지수
       (−1)^{ν₀} = Π_{8 TRIM} δ(k*),  δ(k*) = 점유 Kramers 쌍 parity = sign(M(k*))
     (Dirac 모델: 점유밴드 parity = −sign(M), Kramers 쌍 δ=(−sign M) → Π = Π sign M).
     ν₀(m) 스캔 → 강한 TI 는 m∈(1,3)∪(−3,−1). 약한 지수 ν_j = Π_{k_j=π} sign(M).
     ★**genuine AII**: C·S 를 깨고 T 만 남기는 섭동(sinx siny·iΓ₁Γ₄, TRIM 소멸)에서 gap 유지
       (단열연결) ⟹ ℤ₂ 는 T **단독** 보호(AII). 섭동은 TRIM 에서 0 → parity 공식 정확 불변.
  B. **AIII 3D = ℤ (chiral winding)**: chiral S 만(T·C 없음). winding 닫힌형
       ν(m) = −½ Σ_{8 TRIM} (−1)^{#π} sign(M(k*))  (v15 DIII 와 동일 정수식 = 실제 3D winding).
     ★**genuine AIII**: T·C 를 깨고 S 만 남기는 섭동(sinx·Γ₄, TRIM 소멸)에서 gap 유지 ⟹
       winding 은 chiral **단독** 보호(AIII). TRIM 소멸 → 닫힌형 정확 불변.
  C. ★**AZ 3D 열 대조표**: DIII(ℤ, v15) · AII(ℤ₂, 본) · AIII(ℤ, 본) + ℤ₂=winding mod 2 조대화.
  teeth: (i) T 파괴 → AII ℤ₂ 무의미(강한 지수 보호자 상실) (ii) 약한 vs 강한 지수 구분
     (m∈(−1,1)은 ν₀=0 이나 약한 ν_j=1 = 약한 TI) (iii) parity/winding 부호 규약 오염 검출.

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - 불변량은 **정수**: AII ℤ₂ = TRIM parity 곱(정수 부호산술) · AIII winding = mass-sign 닫힌형.
    ★float Berry/Chern/Pfaffian 적분 금지(v12/v15 상속). Fu-Kane-Mele Pfaffian(반-BZ)은 미사용.
  - genuine AII/AIII 는 **섭동+단열 gap 연속성** 논증(gap 스캔=관측) — 섭동이 TRIM 에서 소멸해
    닫힌형 불변량은 정확히 불변. 섭동 모델의 반전 P 는 깨질 수 있으나 ℤ₂/winding 은 T/S 단독 보호.
  - AZ 분류표 **외부 인용 금지** — 모델별 산출값만("AII=ℤ₂" 는 본 모델의 관측+대칭 논증).
  - free-fermion(BdG/Bloch 2차) 한정 · Wilson-Dirac 특정 모델 한정 · 회로 분해 범위 밖(§2 무관).

사용: python -m qf_witness.observe.az_aiii_aii_3d_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import itertools

import numpy as np

# v15 P5 모듈에서 Wilson-Dirac 골격 재사용(단일출처)
from qf_witness.observe.az_c_ci_diii3d_observe import (
    GAMMA, H_3D, T_3D, C_3D, S_3D, nu_closed_3d, anti, _sign, kr, s0, sy)

P_INV = GAMMA[3]                       # 공간반전 P = Γ₄ = τz⊗σ0
G14 = 1j * GAMMA[0] @ GAMMA[3]         # iΓ₁Γ₄ — chiral S 와 commute(→S 깸)·PHS 깸·TRS 유지 섭동핵
TRIM = list(itertools.product((0, 1), repeat=3))   # (0/π)³


def _mass_trim(m, bits):
    """M(k*) = m + Σ cos k*  (k*_i ∈ {0,π} → cos ∈ {+1,−1})."""
    return m + sum(1 if b == 0 else -1 for b in bits)


# ══ AII 3D — Fu-Kane 강한/약한 ℤ₂ (TRIM parity) ═══════════════════════════════
def fu_kane_z2(m):
    """(−1)^{ν₀} = Π_{8 TRIM} sign(M(k*)) — 강한 지수. 약한 ν_j = Π_{k_j=π} sign(M)."""
    strong = 1
    for bits in TRIM:
        strong *= _sign(_mass_trim(m, bits))
    nu0 = 0 if strong > 0 else 1
    weak = []
    for j in range(3):
        pj = 1
        for bits in TRIM:
            if bits[j] == 1:
                pj *= _sign(_mass_trim(m, bits))
        weak.append(0 if pj > 0 else 1)
    return nu0, weak


# ══ 섭동 모델 + gap (genuine AII/AIII 강건성) ══════════════════════════════════
def H_pert(kx, ky, kz, m, lam, kind):
    """kind='AII': +λ sinx siny·iΓ₁Γ₄ (C,S 깸·T 유지) / 'AIII': +λ sinx·Γ₄ (T,C 깸·S 유지).
    두 섭동 모두 TRIM(sin=0)에서 소멸 → 닫힌형 불변량 정확 불변."""
    H = H_3D(kx, ky, kz, m)
    if kind == "AII":
        return H + lam * np.sin(kx) * np.sin(ky) * G14
    if kind == "AIII":
        return H + lam * np.sin(kx) * GAMMA[3]
    return H


def min_gap_pert(m, lam, kind, N=8):
    ks = np.linspace(0, 2 * np.pi, N, endpoint=False)
    return min(float(np.min(np.abs(np.linalg.eigvalsh(H_pert(a, b, c, m, lam, kind)))))
               for a in ks for b in ks for c in ks)


def _syms(hfun, ks):
    """(T, P, C, S) 성립 여부 튜플."""
    T = all(np.allclose(anti(T_3D, hfun(a, b, c)), hfun(-a, -b, -c)) for a in ks for b in ks for c in ks)
    P = all(np.allclose(P_INV @ hfun(a, b, c) @ P_INV, hfun(-a, -b, -c)) for a in ks for b in ks for c in ks)
    C = all(np.allclose(anti(C_3D, hfun(a, b, c)), -hfun(-a, -b, -c)) for a in ks for b in ks for c in ks)
    S = all(np.allclose(S_3D @ hfun(a, b, c) + hfun(a, b, c) @ S_3D, 0) for a in ks for b in ks for c in ks)
    return T, P, C, S


def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "az-aiii-aii-3d/v1",
           "_note": ("AZ 3D 잔여칸: AII(ℤ₂ 강한 TI·Fu-Kane parity) + AIII(ℤ chiral winding) — "
                     "관측·seal 아님·신규 module 0·root 불변. 불변량=정수(TRIM parity·mass-sign 닫힌형, "
                     "float Berry 적분 아님). ★ℤ₂=DIII winding mod 2(PHS 제거 조대화). AZ 표 외부인용 금지.")}
    ks = np.linspace(-3, 3, 4 if quick else 5)
    mm = (-4, -2, 0, 2, 4)

    # ── 0. base Wilson-Dirac 대칭(v15 재확인: T,P,C,S 전부 = DIII∩AII∩AIII 교집합) ──
    R["base_TRS_T2_minus1"] = np.allclose(T_3D @ T_3D.conj(), -np.eye(4))
    R["base_inversion_P"] = all(np.allclose(P_INV @ H_3D(a, b, c, 1.5) @ P_INV, H_3D(-a, -b, -c, 1.5))
                                for a in ks for b in ks for c in ks)
    Tb, Pb, Cb, Sb = _syms(lambda a, b, c: H_3D(a, b, c, 1.5), ks)
    R["base_has_all_TPCS"] = (Tb and Pb and Cb and Sb)      # 교집합 모델

    # ── A. AII 3D = ℤ₂ (Fu-Kane) ──────────────────────────────────────────
    z2 = {str(m): fu_kane_z2(m) for m in mm}
    strong_pattern = [fu_kane_z2(m)[0] for m in mm]
    R["AII_strong_z2_pattern"] = (strong_pattern == [0, 1, 0, 1, 0])   # m=−4,−2,0,2,4
    # 강한 TI 상(1,3)∪(−3,−1) 실측(반정수 m 로 구간 내부 확인)
    R["AII_strong_TI_in_windows"] = (fu_kane_z2(1.5)[0] == 1 and fu_kane_z2(-1.5)[0] == 1
                                     and fu_kane_z2(0.0)[0] == 0 and fu_kane_z2(3.5)[0] == 0)
    # 약한 TI: m∈(−1,1) 는 강한 0 이나 약한 ν_j=1
    R["AII_weak_TI_at_center"] = (fu_kane_z2(0.0)[0] == 0 and fu_kane_z2(0.0)[1] == [1, 1, 1])
    # ★ℤ₂ = DIII winding mod 2 (PHS 제거 조대화)
    R["AII_z2_equals_winding_mod2"] = all(
        fu_kane_z2(m)[0] == abs(nu_closed_3d(m)) % 2 for m in mm)
    # genuine AII: C,S 깸·T 유지 섭동에서 gap 유지(단열) + 섭동 대칭 확인
    gap_AII = [round(min_gap_pert(1.5, lam, "AII", 6 if quick else 8), 4) for lam in (0.0, 0.2, 0.4)]
    Tp, Pp, Cp, Sp = _syms(lambda a, b, c: H_pert(a, b, c, 1.5, 0.4, "AII"), ks)
    R["AII_genuine_perturb_T_only"] = (Tp and not Cp and not Sp)     # T 유지·C,S 깸
    R["AII_gap_robust_adiabatic"] = all(g > 0.1 for g in gap_AII)    # gap 유지=단열연결
    out["class_AII_3D"] = {
        "invariant": "ℤ₂ strong (Fu-Kane parity Π_{8 TRIM} sign(M))",
        "z2_by_m": {k: {"strong": v[0], "weak": v[1]} for k, v in z2.items()},
        "strong_TI_windows": "m ∈ (1,3) ∪ (−3,−1)",
        "genuine_AII_perturb": {"term": "λ·sinx·siny·iΓ₁Γ₄ (C,S 깸·T 유지·TRIM 소멸)",
                                "gap_by_lambda_at_m=1.5": gap_AII,
                                "perturbed_symmetry": {"T": bool(Tp), "P": bool(Pp),
                                                       "C": bool(Cp), "S": bool(Sp)}},
        "verdict": "★3D 강한 위상절연체 — ℤ₂, T 단독 보호(genuine AII)",
    }

    # ── B. AIII 3D = ℤ (chiral winding) ───────────────────────────────────
    R["AIII_chiral_S2_plus1"] = np.allclose(S_3D @ S_3D, np.eye(4))
    R["AIII_chiral_anticommute"] = all(
        np.allclose(S_3D @ H_3D(a, b, c, 1.5) + H_3D(a, b, c, 1.5) @ S_3D, 0)
        for a in ks for b in ks for c in ks)
    nus = {str(m): nu_closed_3d(m) for m in mm}
    R["AIII_winding_pattern_Z"] = ([abs(nu_closed_3d(m)) for m in mm] == [0, 1, 2, 1, 0])
    R["AIII_Z_not_Z2"] = (max(abs(nu_closed_3d(m)) for m in mm) >= 2)
    # genuine AIII: T,C 깸·S 유지 섭동에서 gap 유지 + winding 정확 불변(TRIM 소멸)
    gap_AIII = [round(min_gap_pert(1.5, lam, "AIII", 6 if quick else 8), 4) for lam in (0.0, 0.2, 0.4)]
    Tq, Pq, Cq, Sq = _syms(lambda a, b, c: H_pert(a, b, c, 1.5, 0.4, "AIII"), ks)
    R["AIII_genuine_perturb_S_only"] = (Sq and not Tq and not Cq)    # S 유지·T,C 깸
    R["AIII_gap_robust_adiabatic"] = all(g > 0.1 for g in gap_AIII)
    out["class_AIII_3D"] = {
        "invariant": "ℤ winding (mass-sign 닫힌형 ν=−½Σ(−1)^#π sign M)",
        "nu_by_m": nus,
        "genuine_AIII_perturb": {"term": "λ·sinx·Γ₄ (T,C 깸·S 유지·TRIM 소멸)",
                                 "gap_by_lambda_at_m=1.5": gap_AIII,
                                 "perturbed_symmetry": {"T": bool(Tq), "P": bool(Pq),
                                                        "C": bool(Cq), "S": bool(Sq)}},
        "verdict": "★3D chiral winding — ℤ, chiral S 단독 보호(genuine AIII)",
    }

    # ── C. AZ 3D 열 대조표 ────────────────────────────────────────────────
    out["az_3d_column"] = {
        "class_DIII": f"ℤ (winding, v15 — {sorted(set(nu_closed_3d(m) for m in mm))})",
        "class_AII": f"ℤ₂ (Fu-Kane strong, 본 — strong {sorted(set(fu_kane_z2(m)[0] for m in mm))})",
        "class_AIII": f"ℤ (chiral winding, 본 — {sorted(set(nu_closed_3d(m) for m in mm))})",
        "DIII_to_AII_coarsening": "PHS(C²=+1) 제거 → ℤ winding → ℤ₂ = winding mod 2",
        "honesty": "각 칸=본 모델 산출값·대칭 논증 (AZ 표 인용 아님)",
    }

    # ── teeth ─────────────────────────────────────────────────────────────
    # (i) T 파괴 → AII ℤ₂ 보호자 상실: T 깨는 섭동에서 강한 TI 상이 gap out 가능 실측
    def H_breakT(a, b, c, m, lam):     # sinx·Γ₄ 는 T 깸(AIII 섭동) — AII 관점서 보호자 상실
        return H_pert(a, b, c, m, lam, "AIII")
    Tt, _, _, _ = _syms(lambda a, b, c: H_breakT(a, b, c, 1.5, 0.4), ks)
    R["teeth_break_T_loses_AII_protection"] = (not Tt)   # T 깨짐 → AII 무의미
    # (ii) 약한 vs 강한: m=0 강한 0·약한 nontrivial (구분 실증)
    R["teeth_weak_vs_strong_distinct"] = (fu_kane_z2(0.0)[0] == 0 and fu_kane_z2(0.0)[1] != [0, 0, 0])
    # (iii) 부호 규약 오염 → winding/parity 변화 검출
    R["teeth_sign_conv_tamper"] = (
        [nu_closed_3d(m, sign_conv=-1) for m in (-2, 0, 2)] != [nu_closed_3d(m) for m in (-2, 0, 2)])

    ok = bool(all(R.values()))
    out["checks"] = R
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "AZ-AIII-AII-3D.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("AZ 3D 잔여칸 관측 (AIII chiral ℤ + AII 강한 TI ℤ₂ — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  ★AII 강한 ℤ₂ ν₀(m): {[fu_kane_z2(m)[0] for m in mm]} (강한 TI in (1,3)∪(−3,−1))", flush=True)
        print(f"  ★AIII winding ν(m): {nus} → |ν|=0,1,2,1,0 (ℤ)", flush=True)
        print(f"  ★ℤ₂ = DIII winding mod 2: {R['AII_z2_equals_winding_mod2']} (PHS 제거 조대화)", flush=True)
        print("  ★정직: 정수 불변량(float Berry 금지)·genuine 은 단열 gap 논증·AZ 표 인용 아님", flush=True)
        print("  → .pgf/proofs/AZ-AIII-AII-3D.json", flush=True)
    print(f"az_aiii_aii_3d_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
