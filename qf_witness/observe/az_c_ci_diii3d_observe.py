#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""az_c_ci_diii3d_observe — TrackHE15 P5: AZ 잔여칸 완결 — 2D class C(2ℤ)·CI(자명)
+ 3D class DIII(winding ℤ) (관측, seal 아님).

기존 AZ 계보([[class_d_2d_chern_observe]] v12 2D class D=ℤ · [[class_diii_observe]] v13 1D DIII
· [[class_diii_2d_observe]] v14 2D DIII=ℤ₂)의 **잔여 칸**을 채워 2D 행을 완성하고, DIII 를
d=2(ℤ₂) → d=3(ℤ) 로 올려 **분류 전이**를 관측한다.

관측 3축:
  A. **2D class C** (PHS C²=−1 · TRS 부재 · SU(2) spin) — 스핀 단일항 d+id 짝짓기:
     H(k) = ξ_k σz + Δ(cos kx−cos ky) σx + 2Δ sin kx sin ky σy  (Nambu 2×2)
     ★**2ℤ(짝수) 강제 논증**: PHS C=iσ_y K 는 d⃗(k)=d⃗(−k)(전 성분 짝함수)를 요구 →
     d̂ 가 ℤ₂ 몫 T²/{k∼−k} 를 통해 인자분해 → degree 짝수. μ 전 구간 스캔으로 실증.
  B. **2D class CI** (TRS T²=+1 · PHS C²=−1 · chiral) — 실수 갭(허수부 제거):
     ★TRS 가 d_y≡0 을 강제 → d⃗ 가 S² 의 **대원(great circle)에 갇힘** → 상수 아닌 정칙값의
     preimage 가 없음 ⟹ degree = 0. **자명 결과를 음성으로 정직 보고**(억지 비자명 탐색 금지).
     ★선검증 발견: 표준 실수 d-wave(d_{x²−y²})는 **nodal**(d⃗=0 점 존재)이라 gapped 분류의
     대상이 아니다 — FHS 가 허위 정수를 내던 원인. 부호가 바뀌지 않는 실수 갭
     Δ(2−cos kx−cos ky)로 교체해 gapped class CI 를 구성하고, nodal 사실도 함께 기록.
  C. **3D class DIII** (T²=−1 · C²=+1 · chiral) — Wilson-Dirac 4-band:
     H(k) = Σᵢ sin kᵢ Γᵢ + (m+Σᵢ cos kᵢ) Γ₄,  Γ = (τx σx, τx σy, τx σz, τz σ0)
     ★대칭 연산자를 **Γ 대수에서 유도**(선검증에서 초기 후보 오류 검출·교체):
       T = τ0⊗(iσy)K (T²=−1) · C = τy⊗(iσy)K (C²=+1) · S = τy⊗σ0 (S²=+1, {S,H}=0)
     ★winding **닫힌형 정수**: ν(m) = −½ Σ_{8 TRIM} (−1)^{#π} sign(m+Σcos k*)
       → ν = 0, −1, 2, −1, 0 (|ν| = 0,1,2,1,0) · gap 닫힘 |m| ∈ {1,3} 과 정합.
  D. ★**AZ 2D 행 완성 대조표**: D(ℤ, v12) · DIII(ℤ₂, v14) · C(2ℤ, 본) · CI(0, 본)
     + DIII 차원 전이 1D ℤ₂(v13) → 2D ℤ₂(v14) → 3D ℤ(본).
  teeth: (i) ★CI 에 d_y 복원(TRS 파괴)해도 **여전히 0** — 확장 s-wave 는 d_x≥0(반평면 갇힘)이라
     degree 0 의 두 번째 독립 원인이 존재(무력한 teeth 를 실측으로 발견 → 사실을 체크로 승격);
     비자명화의 실제 조건은 d⃗ 가 S² 전체를 덮는 것(class C d+id 대조로 실증)
     (ii) class C 에 홀수-winding 짝짓기(p+ip) 주입 → 홀수 Chern 등장(2ℤ 가 대칭의 결과임을 실증)
     (iii) 3D ν 부호 규약 오염 검출.

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - 불변량은 **정수**: 3D winding = mass-sign 닫힌형(정수 산술) · 2D Chern = FHS 격자 공식
    (Fukui-Hatsugai-Suzuki, **gauge-invariant 정수 산출** — 연속 Berry 적분의 float 근사가 아님;
    v12 class-D 선례 상속). ★float Chern/Berry 적분 금지 규약 유지.
  - 밴드 스펙트럼·gap 값은 **관측**(sidecar) — 봉인 아님.
  - free-fermion(BdG 2차) 한정 · 특정 격자 모델 한정 · AZ 분류표 자체는 **외부 인용 금지**
    (본 witness 는 모델별 불변량 값만 산출; "class C = 2ℤ" 는 우리 모델에서의 관측 + 대칭 논증).
  - 회로 unitary honest 분해는 범위 밖(§2 무관).

사용: python -m qf_witness.observe.az_c_ci_diii3d_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import itertools

import numpy as np

s0 = np.eye(2, dtype=complex)
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.diag([1, -1]).astype(complex)


def kr(a, b):
    return np.kron(a, b)


def anti(U, M):
    return U @ M.conj() @ np.linalg.inv(U)


def _sign(x):
    return (x > 0) - (x < 0)


# ══ A. 2D class C — 단일항 d+id ═══════════════════════════════════════════
def H_C(kx, ky, mu, t=1.0, D=1.0, px=0.0):
    """d_{x²−y²}+i d_{xy} (짝함수 → PHS C²=−1). px≠0 은 teeth 용 p+ip 혼입(홀수 winding)."""
    xi = -2 * t * (np.cos(kx) + np.cos(ky)) - mu
    dx = D * (np.cos(kx) - np.cos(ky)) + px * np.sin(kx)
    dy = 2 * D * np.sin(kx) * np.sin(ky) + px * np.sin(ky)
    return xi * sz + dx * sx + dy * sy


C_PHS = 1j * sy                      # C = iσ_y K, C² = −1


def d_vector(kx, ky, mu, t=1.0, D=1.0, px=0.0):
    H = H_C(kx, ky, mu, t, D, px)
    return np.array([H[0, 1].real, -H[0, 1].imag, H[0, 0].real])


def lower_vec(H):
    w, v = np.linalg.eigh(H)
    return v[:, 0]


def fhs_chern(hfun, N=24, **kw):
    """Fukui-Hatsugai-Suzuki 격자 Chern — ★gauge-invariant **정수** 산출
    (plaquette 별 주분지 log 합; 연속 적분의 float 근사가 아님). v12 class-D 선례."""
    ks = np.linspace(0, 2 * np.pi, N, endpoint=False)
    U = [[lower_vec(hfun(kx, ky, **kw)) for ky in ks] for kx in ks]
    tot = 0.0
    for i in range(N):
        for j in range(N):
            i2, j2 = (i + 1) % N, (j + 1) % N
            u1 = np.vdot(U[i][j], U[i2][j])
            u2 = np.vdot(U[i2][j], U[i2][j2])
            u3 = np.vdot(U[i2][j2], U[i][j2])
            u4 = np.vdot(U[i][j2], U[i][j])
            prod = u1 * u2 * u3 * u4
            if abs(prod) < 1e-12:
                return None
            tot += np.angle(prod)
    c = tot / (2 * np.pi)
    ci = int(round(c))
    return ci if abs(c - ci) < 1e-6 else None      # 정수 아니면 실패(격자 부족)


# ══ B. 2D class CI — 실수 d-wave ══════════════════════════════════════════
def H_CI(kx, ky, mu, t=1.0, D=1.0, dy_restore=0.0, nodal=False):
    """class CI. ★nodal=True 는 표준 실수 d-wave(d_{x²−y²}) — **노드를 갖는다**(gapless).
    gapped 분류의 대상이 되려면 부호가 바뀌지 않는 실수 갭이 필요 → 확장 s-wave 형
    d_x = Δ(2−cos kx−cos ky) ≥ 0 을 기본으로 사용(TRS/PHS/chiral 동일하게 유지)."""
    xi = -2 * t * (np.cos(kx) + np.cos(ky)) - mu
    dx = (D * (np.cos(kx) - np.cos(ky)) if nodal
          else D * (2 - np.cos(kx) - np.cos(ky)))
    dy = dy_restore * 2 * D * np.sin(kx) * np.sin(ky)     # teeth: TRS 파괴
    return xi * sz + dx * sx + dy * sy


def ci_nodal_analytic(mu, t=1.0):
    """★실수 d-wave 의 노드 존재를 **해석적으로** 판정(격자 이산화 무관).
    d⃗=0 ⟺ cos kx = cos ky = c (d_x=0) 이고 ξ = −4tc − μ = 0 → c = −μ/(4t).
    |c| ≤ 1 이면 그런 (kx,ky) 가 실제로 존재 ⟹ gapless. (격자 gap 스캔은 노드가 샘플점에
    걸리지 않으면 0 을 못 내므로 판정 근거로 쓰지 않는다 — 선검증에서 실측 확인.)"""
    return abs(-mu / (4 * t)) <= 1.0


def min_gap_2d(hfun, N=24, **kw):
    ks = np.linspace(0, 2 * np.pi, N, endpoint=False)
    return min(float(np.min(np.abs(np.linalg.eigvalsh(hfun(a, b, **kw)))))
               for a in ks for b in ks)


T_CI = s0                                                  # T = K, T² = +1


# ══ C. 3D class DIII — Wilson-Dirac ═══════════════════════════════════════
GAMMA = [kr(sx, sx), kr(sx, sy), kr(sx, sz), kr(sz, s0)]
T_3D = kr(s0, 1j * sy)               # T² = −1
C_3D = kr(sy, 1j * sy)               # C² = +1
S_3D = kr(sy, s0)                    # chiral, S² = +1


def H_3D(kx, ky, kz, m):
    M = m + np.cos(kx) + np.cos(ky) + np.cos(kz)
    return (np.sin(kx) * GAMMA[0] + np.sin(ky) * GAMMA[1]
            + np.sin(kz) * GAMMA[2] + M * GAMMA[3])


def nu_closed_3d(m, sign_conv=1):
    """★닫힌형 정수: ν = −½ Σ_{8 TRIM} (−1)^{#π} sign(m + Σcos k*). 전부 정수 산술."""
    tot = 0
    for bits in itertools.product((0, 1), repeat=3):
        mass = m + sum(1 if b == 0 else -1 for b in bits)
        tot += ((-1) ** sum(bits)) * _sign(mass) * sign_conv
    return -tot // 2


def min_gap_3d(m, N=8):
    ks = np.linspace(0, 2 * np.pi, N, endpoint=False)
    return min(float(np.min(np.abs(np.linalg.eigvalsh(H_3D(a, b, c, m)))))
               for a in ks for b in ks for c in ks)


def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "az-c-ci-diii3d/v1",
           "_note": ("AZ 잔여칸: 2D class C(2ℤ)·CI(자명 0)·3D DIII(winding ℤ) — 관측·seal 아님·"
                     "신규 module 0·root 불변. 불변량=정수(3D 닫힌형·2D FHS gauge-invariant 정수, "
                     "float Berry 적분 아님). AZ 분류표 외부 인용 금지 — 모델별 산출값만.")}
    ksym = np.linspace(-3, 3, 7 if quick else 11)

    # ── A. class C ───────────────────────────────────────────────────────
    R["C_PHS_squared_minus1"] = np.allclose(C_PHS @ C_PHS.conj(), -np.eye(2))
    R["C_PHS_holds"] = all(np.allclose(anti(C_PHS, H_C(a, b, 1.0)), -H_C(-a, -b, 1.0))
                           for a in ksym for b in ksym)
    R["C_TRS_absent"] = not all(np.allclose(H_C(a, b, 1.0).conj(), H_C(-a, -b, 1.0))
                                for a in ksym for b in ksym)
    R["C_dvector_even"] = all(
        np.allclose(d_vector(a, b, 1.0), d_vector(-a, -b, 1.0))
        for a in ksym for b in ksym)                     # ★2ℤ 강제의 근거
    NC = 16 if quick else 24
    mus_C = [-5.0, -3.0, -1.0, 1.0, 3.0, 5.0]
    chern_C = {}
    for mu in mus_C:
        c = fhs_chern(H_C, N=NC, mu=mu)
        chern_C[str(mu)] = c
    R["C_chern_all_even"] = all(c is not None and c % 2 == 0 for c in chern_C.values())
    R["C_chern_nontrivial_exists"] = any(c not in (None, 0) for c in chern_C.values())
    out["class_C"] = {"model": "ξ σz + Δ(cos kx−cos ky) σx + 2Δ sin kx sin ky σy (singlet d+id)",
                      "chern_by_mu": chern_C,
                      "verdict": "PHS 짝함수 d⃗ → degree 짝수 (2ℤ) — 모델 전 구간 실증"}

    # ── B. class CI ──────────────────────────────────────────────────────
    R["CI_TRS_squared_plus1"] = np.allclose(T_CI @ T_CI.conj(), np.eye(2))
    R["CI_TRS_holds"] = all(np.allclose(anti(T_CI, H_CI(a, b, 1.0)), H_CI(-a, -b, 1.0))
                            for a in ksym for b in ksym)
    R["CI_PHS_holds"] = all(np.allclose(anti(C_PHS, H_CI(a, b, 1.0)), -H_CI(-a, -b, 1.0))
                            for a in ksym for b in ksym)
    R["CI_dy_identically_zero"] = all(
        abs(H_CI(a, b, 1.0)[0, 1].imag) < 1e-12 for a in ksym for b in ksym)
    # ★표준 실수 d-wave 는 nodal — gapped 분류 대상이 아님을 먼저 실측(선검증에서 검출)
    gap_nodal = {str(mu): round(min_gap_2d(H_CI, N=NC, mu=mu, nodal=True), 6)
                 for mu in (-1.0, 1.0)}
    R["CI_real_dwave_is_nodal"] = all(ci_nodal_analytic(mu) for mu in (-1.0, 1.0))
    gap_CI = {str(mu): round(min_gap_2d(H_CI, N=NC, mu=mu), 6)
              for mu in (-3.0, -1.0, 1.0, 3.0)}
    R["CI_gapped_model_has_gap"] = all(v > 1e-3 for v in gap_CI.values())
    chern_CI = {str(mu): fhs_chern(H_CI, N=NC, mu=mu) for mu in (-3.0, -1.0, 1.0, 3.0)}
    R["CI_chern_all_zero"] = all(c == 0 for c in chern_CI.values())
    out["class_CI"] = {"model": "ξ σz + Δ(2−cos kx−cos ky) σx (실수 갭, TRS 회복·gapped)",
                       "chern_by_mu": chern_CI, "min_gap_by_mu": gap_CI,
                       "nodal_variant": {
                           "model": "ξ σz + Δ(cos kx−cos ky) σx (표준 d_{x²−y²})",
                           "nodal_condition": "d⃗=0 ⟺ cos kx=cos ky=−μ/(4t), |−μ/(4t)|≤1 (해석적)",
                           "lattice_gap_scan_by_mu": gap_nodal,
                           "lattice_caveat": ("격자 gap 스캔은 노드가 샘플점에 걸리지 않으면 "
                                              "0 을 못 냄(실측 0.035) — 판정은 해석적 조건으로"),
                           "finding": ("★표준 실수 d-wave 는 **nodal**(d⃗=0 점 존재) — gapped "
                                       "위상 분류의 대상이 아님. 선검증에서 FHS 가 허위 정수를 "
                                       "낸 원인이었고, gapped 모델로 교체해 확정")},
                       "teeth_finding": ("★TRS 파괴(d_y 복원)만으로는 비자명화되지 않음 — "
                                         "확장 s-wave 는 d_x≥0(반평면 갇힘)이라 degree 0 의 "
                                         "두 번째 독립 원인이 있다(실측). 비자명 Chern 은 d⃗ 가 "
                                         "S² 전체를 덮어야 가능 — class C d+id 가 그 예"),
                       "verdict": ("★자명(0) — TRS 가 d_y≡0 을 강제 → d⃗ 가 S² 대원에 갇힘 → "
                                   "degree 0. 음성 결과를 그대로 보고(억지 비자명 탐색 없음)")}

    # ── C. 3D class DIII ─────────────────────────────────────────────────
    R["DIII3_gamma_clifford"] = all(
        np.allclose(GAMMA[a] @ GAMMA[b] + GAMMA[b] @ GAMMA[a], 2 * (a == b) * np.eye(4))
        for a in range(4) for b in range(4))
    R["DIII3_T_squared_minus1"] = np.allclose(T_3D @ T_3D.conj(), -np.eye(4))
    R["DIII3_C_squared_plus1"] = np.allclose(C_3D @ C_3D.conj(), np.eye(4))
    R["DIII3_S_squared_plus1"] = np.allclose(S_3D @ S_3D, np.eye(4))
    k3 = np.linspace(-3, 3, 4 if quick else 5)
    R["DIII3_TRS"] = all(np.allclose(anti(T_3D, H_3D(a, b, c, 1.5)), H_3D(-a, -b, -c, 1.5))
                         for a in k3 for b in k3 for c in k3)
    R["DIII3_PHS"] = all(np.allclose(anti(C_3D, H_3D(a, b, c, 1.5)), -H_3D(-a, -b, -c, 1.5))
                         for a in k3 for b in k3 for c in k3)
    R["DIII3_chiral"] = all(
        np.allclose(S_3D @ H_3D(a, b, c, 1.5) + H_3D(a, b, c, 1.5) @ S_3D, 0)
        for a in k3 for b in k3 for c in k3)
    nus = {str(m): nu_closed_3d(m) for m in (-4, -2, 0, 2, 4)}
    R["DIII3_winding_pattern"] = ([abs(nu_closed_3d(m)) for m in (-4, -2, 0, 2, 4)]
                                  == [0, 1, 2, 1, 0])
    R["DIII3_Z_not_Z2"] = (max(abs(nu_closed_3d(m)) for m in (-4, -2, 0, 2, 4)) >= 2)
    Ng = 6 if quick else 8
    gaps = {str(m): round(min_gap_3d(m, Ng), 6) for m in (-4, -3, -1, 0, 1, 3, 4)}
    R["DIII3_gap_closes_at_transitions"] = all(gaps[str(m)] < 1e-9 for m in (-3, -1, 1, 3))
    R["DIII3_gap_open_in_phase"] = all(gaps[str(m)] > 0.5 for m in (-4, 0, 4))
    out["class_DIII_3D"] = {
        "model": "Σ sin kᵢ Γᵢ + (m+Σcos kᵢ) Γ₄ ; Γ=(τxσx, τxσy, τxσz, τzσ0)",
        "symmetry": "T=τ0⊗(iσy)K (T²=−1) · C=τy⊗(iσy)K (C²=+1) · S=τy⊗σ0 (S²=+1)",
        "winding_closed_form": "ν = −½ Σ_{8 TRIM} (−1)^{#π} sign(m+Σcos k*)  (정수 산술)",
        "nu_by_m": nus, "min_gap_by_m": gaps,
        "verdict": "|ν| = 0,1,2,1,0 — ★ℤ 분류(|ν|=2 존재 ⟹ ℤ₂ 아님)",
    }

    # ── D. AZ 대조표 ─────────────────────────────────────────────────────
    out["az_table"] = {
        "2D_row": {"class_D": "ℤ (Chern, v12)", "class_DIII": "ℤ₂ (Pfaffian, v14)",
                   "class_C": f"2ℤ (짝수 Chern, 본 — 관측값 {sorted(set(v for v in chern_C.values() if v is not None))})",
                   "class_CI": "0 (자명, 본)"},
        "DIII_dimension_transition": {"1D": "ℤ₂ (v13)", "2D": "ℤ₂ (v14)",
                                      "3D": f"ℤ (winding, 본 — {sorted(set(nu_closed_3d(m) for m in (-4,-2,0,2,4)))})"},
        "honesty": "각 칸은 **본 프로젝트 모델에서 산출한 값** — AZ 분류표 인용 아님",
    }

    # ── teeth ────────────────────────────────────────────────────────────
    # ★teeth 재정의(선검증 발견): TRS 파괴(d_y 복원)만으로는 비자명화되지 않는다 —
    #   확장 s-wave 갭은 d_x ≥ 0 (반평면 갇힘)이라 **degree 0 의 두 번째 독립 원인**이 있다.
    #   무력한 teeth 를 그대로 두지 않고, 실측 사실을 체크로 승격한다.
    c_ci_broken = fhs_chern(H_CI, N=NC, mu=1.0, dy_restore=1.0)
    R["teeth_CI_halfplane_blocks_alone"] = (c_ci_broken == 0)
    #   비자명화의 진짜 조건 = d⃗ 가 S² 전체를 덮는 것(class C d+id 가 그 예) — 대조로 실증
    R["teeth_CI_vs_C_contrast"] = (
        c_ci_broken == 0 and chern_C["1.0"] not in (None, 0))
    c_odd = fhs_chern(H_C, N=NC, mu=1.0, D=0.0, px=1.0)          # 순수 p+ip
    R["teeth_C_odd_winding_possible"] = (c_odd is not None and c_odd % 2 == 1)
    R["teeth_3d_sign_tamper"] = (
        [abs(nu_closed_3d(m, sign_conv=-1) - nu_closed_3d(m)) for m in (-2, 0, 2)]
        != [0, 0, 0])

    ok = bool(all(R.values()))
    out["checks"] = R
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "AZ-C-CI-DIII3D.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("AZ 잔여칸 관측 (2D class C/CI + 3D DIII — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  ★class C Chern(μ별): {chern_C} → 전부 짝수(2ℤ)", flush=True)
        print(f"  ★class CI: {chern_CI} → 자명 0 (음성 정직 보고)", flush=True)
        print(f"  ★3D DIII winding ν(m): {nus} → |ν|=0,1,2,1,0 (ℤ 분류)", flush=True)
        print("  → .pgf/proofs/AZ-C-CI-DIII3D.json", flush=True)
    print(f"az_c_ci_diii3d_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
