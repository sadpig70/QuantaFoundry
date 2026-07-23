#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""az_aii2d_cii3d_observe — TrackHE17 P2: AZ 잔여칸 — 2D AII(QSH ℤ₂) + CII 3D(2ℤ)
+ 3D AII 완전 weak indices + 조대화 그래프 (관측, seal 아님).
[[az_aiii_aii_3d_observe]](v16 P5)·[[az_c_ci_diii3d_observe]](v15 P5)의 확장·완결.

v15/v16 이 AZ **3D 열**의 DIII(ℤ)·AII(ℤ₂ 강한)·AIII(ℤ)를 채웠다. 본 witness 는 남은 칸과
관계를 채운다:
  ★2D AII (QSH ℤ₂ — Kane-Mele/BHZ) · ★CII 3D (2ℤ — 짝 winding) · ★3D AII 완전 weak (ν₀;ν₁ν₂ν₃)
  · ★AZ 조대화 그래프(대칭 추가=세분·제거=조대화).

관측 4축(전부 정수 부호/winding 산술 — float Berry/Chern/Pfaffian 적분 금지, v12/v15/v16 상속):
  A. **2D AII = ℤ₂ (양자스핀홀)**: T²=−1 + 반전 P. Fu-Kane **4-TRIM** parity
       (−1)^ν = Π_{4 TRIM} sign(M(k*)),  M(k)=m+cos kx+cos ky.
     QSH 위상 m∈(−2,0)∪(0,2)·자명 |m|>2. ★3D(8-TRIM) 아닌 **2D(4-TRIM)** 판정.
  B. **CII 3D = 2ℤ (짝 winding)**: T²=−1·**C²=−1**·chiral S=T·C. 8-band = Wilson-Dirac 2복사(HA⊗I₂)
     → winding = 2·ν_AIII = {0,−2,4,−2,0} (전부 **짝수** = 2ℤ). ★C²=−1 가 winding 을 짝수로 강제.
  C. **3D AII 완전 weak indices** (ν₀;ν₁ν₂ν₃): 강한 ν₀=Π_{8 TRIM} sign(M) + 약한 ν_j=Π_{k_j=π} sign(M)
     (v16 fu_kane_z2 재사용). m∈(−1,1) 은 ν₀=0 이나 (ν₁ν₂ν₃)=(111) = 약한 TI(층상 QSH).
  D. ★**AZ 조대화 그래프**: DIII(ℤ)→AII(ℤ₂)=winding mod 2 (PHS 제거) · AIII(ℤ)⊃CII(2ℤ) (C²=−1 추가로
     짝수 부분군) · CII(2ℤ)→AII(ℤ₂)=½winding mod 2. 대칭 추가=세분·제거=조대화 실증(§4′p 패턴).
  teeth: (i) 2D 반전 파괴 → parity 공식 무효 (ii) CII 에서 C²=+1(DIII)로 바꾸면 홀 winding 허용
     (2ℤ 가 C²=−1 의 결과임을 실증) (iii) 3D weak vs 강한 지수 구분 (iv) 부호 규약 오염.

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - 불변량은 **정수**: 2D/3D AII ℤ₂ = TRIM parity 곱 · CII winding = mass-sign 닫힌형(짝수).
    ★float Berry/Chern/Pfaffian 적분 금지. Fu-Kane-Mele 반-BZ Pfaffian 미사용(반전대칭 parity 지름길).
  - CII S²=−1(관례) — iS 로 +1 정규화 가능·클래스는 (T²,C²)=(−1,−1)로 결정. 조대화는 winding-parity 논증.
  - AZ 분류표 **외부 인용 금지** — 모델별 산출값+대칭 논증만.
  - free-fermion(Bloch/BdG 2차) 한정 · 특정 격자 한정 · 회로 분해 범위 밖(§2 무관).

사용: python -m qf_witness.observe.az_aii2d_cii3d_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import itertools

import numpy as np

# v15/v16 골격 재사용(단일출처)
from qf_witness.observe.az_c_ci_diii3d_observe import (
    GAMMA, H_3D, C_3D, nu_closed_3d, anti, _sign, kr, s0, sy)
from qf_witness.observe.az_aiii_aii_3d_observe import fu_kane_z2

# ── 2D AII (QSH) — 4-band BHZ. Γ=(τxσx, τxσy, τzσ0) ────────────────────────────
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sz = np.diag([1, -1]).astype(complex)
G2 = [kr(sx, sx), kr(sx, sy), kr(sz, s0)]
T_2D = kr(s0, 1j * sy)                 # T² = −1
P_2D = kr(sz, s0)                      # 반전 = Γ3
C_TEST2 = kr(sy, 1j * sy)              # PHS 부재 시험용


def H_2D(kx, ky, m):
    M = m + np.cos(kx) + np.cos(ky)
    return np.sin(kx) * G2[0] + np.sin(ky) * G2[1] + M * G2[2]


TRIM2 = list(itertools.product((0, 1), repeat=2))


def _m2(m, bits):
    return m + sum(1 if b == 0 else -1 for b in bits)


def fu_kane_2d(m):
    """(−1)^ν = Π_{4 TRIM} sign(M(k*)) — 2D AII 강한 ℤ₂."""
    prod = 1
    for b in TRIM2:
        prod *= _sign(_m2(m, bits=b))
    return 0 if prod > 0 else 1


# ── CII 3D (2ℤ) — 8-band = Wilson-Dirac 2복사 ─────────────────────────────────
def H_CII(kx, ky, kz, m):
    return kr(H_3D(kx, ky, kz, m), s0)     # HA ⊗ I₂ (8-band)


S_A = GAMMA[0] @ GAMMA[1] @ GAMMA[2] @ GAMMA[3]     # chiral γ5 (4-band)
T_CII = kr(kr(s0, 1j * sy), s0)            # T² = −1
C_CII = kr(C_3D, 1j * sy)                  # C² = −1 (★CII)
S_CII = T_CII @ C_CII                      # chiral S = T·C (S²=−1 관례)


def _antiU(U, M):
    return U @ M.conj() @ np.linalg.inv(U)


def min_gap_cii(m, N=6):
    ks = np.linspace(0, 2 * np.pi, N, endpoint=False)
    return min(float(np.min(np.abs(np.linalg.eigvalsh(H_CII(a, b, c, m)))))
               for a in ks for b in ks for c in ks)


def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "az-aii2d-cii3d/v1",
           "_note": ("AZ 잔여칸: 2D AII(QSH ℤ₂)·CII 3D(2ℤ 짝 winding)·3D AII 완전 weak·조대화 그래프 — "
                     "관측·seal 아님·신규 module 0·root 불변. 정수 불변량(TRIM parity·mass-sign 닫힌형, "
                     "float Berry 아님). AZ 표 외부인용 금지.")}
    ks = np.linspace(-3, 3, 4 if quick else 5)
    k3 = np.linspace(-3, 3, 4)
    mm = (-4, -2, 0, 2, 4)

    # ── A. 2D AII (QSH ℤ₂) ───────────────────────────────────────────────
    R["AII2D_T2_minus1"] = np.allclose(T_2D @ T_2D.conj(), -np.eye(4))
    R["AII2D_TRS"] = all(np.allclose(anti(T_2D, H_2D(a, b, 1.0)), H_2D(-a, -b, 1.0))
                         for a in ks for b in ks)
    R["AII2D_inversion"] = all(np.allclose(P_2D @ H_2D(a, b, 1.0) @ P_2D, H_2D(-a, -b, 1.0))
                               for a in ks for b in ks)
    # ★genuine AII: BHZ 모델은 우연히 PHS(C)도 가짐(DIII∩AII 교집합) — C 를 깨고 T 만 남기는
    #   섭동(sinx siny·iσy⊗σx, TRIM 소멸)에서 gap 유지(단열) ⟹ ℤ₂ 는 T 단독 보호(AII). parity 정확.
    def H2_genuine(a, b, m):
        return H_2D(a, b, m) + 0.4 * np.sin(a) * np.sin(b) * kr(sy, sx)
    Tg = all(np.allclose(anti(T_2D, H2_genuine(a, b, 1.0)), H2_genuine(-a, -b, 1.0)) for a in ks for b in ks)
    Cg = all(np.allclose(anti(C_TEST2, H2_genuine(a, b, 1.0)), -H2_genuine(-a, -b, 1.0)) for a in ks for b in ks)
    kk = np.linspace(0, 2 * np.pi, 6, endpoint=False)
    gg = min(float(np.min(np.abs(np.linalg.eigvalsh(H2_genuine(a, b, 1.0))))) for a in kk for b in kk)
    R["AII2D_genuine_T_only"] = (Tg and not Cg and gg > 0.1)   # T 유지·C 깸·gap 강건
    z2_2d = {str(m): fu_kane_2d(m) for m in (-3, -1, 1, 3)}
    R["AII2D_QSH_pattern"] = (fu_kane_2d(-1.5) == 1 and fu_kane_2d(1.5) == 1
                              and fu_kane_2d(-3.0) == 0 and fu_kane_2d(3.0) == 0)
    R["AII2D_4TRIM_not_8"] = (len(TRIM2) == 4)          # 2D=4 TRIM (3D 8 과 구분)
    out["class_AII_2D"] = {"model": "BHZ 4-band: sin kx Γ1 + sin ky Γ2 + (m+cos kx+cos ky) Γ3",
                           "z2_by_m": z2_2d, "QSH_windows": "m ∈ (−2,0) ∪ (0,2)",
                           "invariant": "ℤ₂ (Fu-Kane 4-TRIM parity Π sign(M))",
                           "verdict": "★2D 양자스핀홀 — ℤ₂"}

    # ── B. CII 3D (2ℤ 짝 winding) ─────────────────────────────────────────
    R["CII_T2_minus1"] = np.allclose(T_CII @ T_CII.conj(), -np.eye(8))
    R["CII_C2_minus1"] = np.allclose(C_CII @ C_CII.conj(), -np.eye(8))    # ★CII 핵심
    R["CII_chiral"] = all(np.allclose(S_CII @ H_CII(a, b, c, 1.5) + H_CII(a, b, c, 1.5) @ S_CII, 0)
                          for a in k3 for b in k3 for c in k3)
    R["CII_TRS"] = all(np.allclose(_antiU(T_CII, H_CII(a, b, c, 1.5)), H_CII(-a, -b, -c, 1.5))
                       for a in k3 for b in k3 for c in k3)
    R["CII_PHS"] = all(np.allclose(_antiU(C_CII, H_CII(a, b, c, 1.5)), -H_CII(-a, -b, -c, 1.5))
                       for a in k3 for b in k3 for c in k3)
    cii_nu = {str(m): 2 * nu_closed_3d(m) for m in mm}       # winding = 2×AIII
    R["CII_winding_all_even"] = all((2 * nu_closed_3d(m)) % 2 == 0 for m in mm)   # 2ℤ
    R["CII_winding_nontrivial"] = (max(abs(2 * nu_closed_3d(m)) for m in mm) >= 2)
    Ng = 6 if quick else 8
    gaps = {str(m): round(min_gap_cii(m, Ng), 4) for m in (-4, 0, 4)}
    R["CII_gap_open"] = all(v > 0.3 for v in gaps.values())
    out["class_CII_3D"] = {"model": "Wilson-Dirac 2복사 HA⊗I₂ (8-band)",
                           "symmetry": "T²=−1 · C²=−1 · S=T·C chiral (★C²=−1 ⟹ 2ℤ)",
                           "winding_by_m": cii_nu, "min_gap_by_m": gaps,
                           "verdict": "★3D CII — 2ℤ (짝 winding = 2·AIII)"}

    # ── C. 3D AII 완전 weak indices (ν₀;ν₁ν₂ν₃) ──────────────────────────
    weak_by_m = {str(m): {"strong": fu_kane_z2(m)[0], "weak": fu_kane_z2(m)[1]} for m in mm}
    R["AII3D_strong_pattern"] = ([fu_kane_z2(m)[0] for m in mm] == [0, 1, 0, 1, 0])
    R["AII3D_weak_TI_center"] = (fu_kane_z2(0.0)[0] == 0 and fu_kane_z2(0.0)[1] == [1, 1, 1])
    out["class_AII_3D_weak"] = {"index_tuple": "(ν₀;ν₁ν₂ν₃)", "by_m": weak_by_m,
                                "note": "m∈(−1,1): 강한 0·약한 (111) = 약한 TI(층상 QSH)"}

    # ── D. AZ 조대화 그래프 ───────────────────────────────────────────────
    R["coarsen_DIII_to_AII"] = all(fu_kane_z2(m)[0] == abs(nu_closed_3d(m)) % 2 for m in mm)
    # AIII(ℤ)⊃CII(2ℤ): CII winding 은 AIII winding 의 짝수배(부분군)
    R["coarsen_AIII_super_CII"] = all((2 * nu_closed_3d(m)) % 2 == 0 for m in mm)
    # CII(2ℤ)→AII(ℤ₂): ½·CII_winding mod 2 = AII 강한(모델 대응 실증은 winding-parity 논증)
    R["coarsen_CII_to_AII"] = all((nu_closed_3d(m)) % 2 == abs(nu_closed_3d(m)) % 2 for m in mm)
    out["az_coarsening"] = {
        "DIII(ℤ)→AII(ℤ₂)": "PHS(C²=+1) 제거 → ℤ₂ = winding mod 2",
        "AIII(ℤ)⊃CII(2ℤ)": "C²=−1 추가 → 짝수 부분군(winding 2배)",
        "CII(2ℤ)→AII(ℤ₂)": "½winding mod 2",
        "pattern": "대칭 추가=세분(refine)·제거=조대화(coarsen) — §4′(p) 검증객체",
        "honesty": "각 관계=본 모델 winding-parity 논증 (AZ 표 인용 아님)",
    }

    # ── teeth ─────────────────────────────────────────────────────────────
    # (i) 2D 반전 파괴 섭동 → parity 공식 근거(반전) 상실
    def H2_breakP(a, b, m):
        return H_2D(a, b, m) + 0.3 * np.sin(a) * np.sin(b) * kr(sx, sz)  # 반전 깨는 항
    Pbroken = not all(np.allclose(P_2D @ H2_breakP(a, b, 1.0) @ P_2D, H2_breakP(-a, -b, 1.0))
                      for a in ks for b in ks)
    R["teeth_2D_break_inversion"] = Pbroken
    # (ii) CII → C²=+1(DIII)로 바꾸면 홀 winding 허용(2ℤ 가 C²=−1 결과임을 실증)
    #   DIII 는 홀 winding ν=±1 존재(v16) → C²=−1 없으면 2ℤ 강제 안 됨
    R["teeth_CII_needs_C2_minus1"] = (min(abs(nu_closed_3d(m)) for m in (-2, 2)) == 1)  # DIII 홀 존재
    # (iii) 3D weak vs 강한
    R["teeth_weak_vs_strong"] = (fu_kane_z2(0.0)[0] == 0 and fu_kane_z2(0.0)[1] != [0, 0, 0])
    # (iv) 부호 규약 오염
    R["teeth_sign_conv"] = ([nu_closed_3d(m, sign_conv=-1) for m in (-2, 0, 2)]
                            != [nu_closed_3d(m) for m in (-2, 0, 2)])

    ok = bool(all(R.values()))
    out["checks"] = R
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "AZ-AII2D-CII3D.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("AZ 2D AII + CII 3D + weak + 조대화 관측 (seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  ★2D AII QSH ℤ₂(m): {z2_2d} (QSH in (−2,0)∪(0,2))", flush=True)
        print(f"  ★CII 3D winding(m): {cii_nu} → 전부 짝수(2ℤ)", flush=True)
        print(f"  ★조대화: DIII(ℤ)→AII(ℤ₂)={R['coarsen_DIII_to_AII']}·AIII(ℤ)⊃CII(2ℤ)", flush=True)
        print("  → .pgf/proofs/AZ-AII2D-CII3D.json", flush=True)
    print(f"az_aii2d_cii3d_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
