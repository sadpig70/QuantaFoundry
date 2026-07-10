#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""class_d_2d_chern_observe — 2D spinless p+ip 초전도체(AZ class D) ℤ Chern witness (관측, seal 아님).

TrackHE11 1D Kitaev class-D(ℤ₂ Pfaffian, [[kitaev_class_d_observe]])의 **2D 상보**. AZ 차원사다리:
class D 는 1D 에서 ℤ₂(Majorana sign) 이지만 **2D 에서 ℤ**(Chern number) — particle-hole 대칭 초전도체의
차원별 위상분류. 2D spinless p+ip(chiral) 초전도체 BdG Bloch Hamiltonian(Nambu σ):
  H(k) = (M − 2t(cos kx + cos ky)) σ_z + Δ(sin kx σ_x + sin ky σ_y) = d(k)·σ,
  d(k) = (Δ sin kx, Δ sin ky, M − 2t(cos kx + cos ky)).  (t=Δ=1 고정, M 가변)

두 독립 경로로 Chern 정수 C 확립(★lower band 규약 고정 — [[chern_observe]]/hgp 부호정렬 교훈):
  path A ★**닫힌형 Dirac mass-sign**(정수 산술, 부동소수 없음): d_x=d_y=0 인 TRIM k∈{0,π}² 의
    질량 m(k)=M−2t(cos kx+cos ky) ∈ {M−4t, M, M, M+4t} 의 부호합. lower band 규약:
      **C = (2·sgn(M) − sgn(M−4t) − sgn(M+4t))/2**  (skyrmion degree 의 −부호 = FHS-lowest 규약).
    위상 다이어그램: 0<M<4t → C=+1 · −4t<M<0 → C=−1 · |M|>4t → C=0.
  path B **FHS(Fukui-Hatsugai-Suzuki) 격자 numerics**(독립 확인): N×N BZ 격자 lower band(음에너지
    eigenstate) U(1) link variable → plaquette log 합/2π = gauge-invariant 정수. path A 와 정확 일치.
  gap-closing: M∈{0,±4t}(Dirac 전이, gap=0) → C 불연속(상 경계).

정직 경계(★관측·seal 아님, root 불변 sidecar): witness = class-D 2D **ℤ Chern 정수**(mass-sign exact +
  FHS 확인). ★부호규약=lower band 고정(Chern sign convention-dependent). ground-state prep 회로는 일반 k
  에서 무리수 Bogoliubov 각도 → 봉인 아님(신규 module 회피). free-fermion(BdG 2차) 한정·PHS 규약 고정·
  edge mode/임계값=범위밖. 신규 module 0. 1D class-D ℤ₂([[kitaev_class_d_observe]])·QWZ class A
  ([[chern_observe]]) 와 AZ 대칭클래스 상보(1D ℤ₂ → 2D ℤ 차원사다리).

사용: python scripts/class_d_2d_chern_observe.py [--quick]
"""
from __future__ import annotations
import sys
import numpy as np

X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def dvec(kx, ky, M, t=1.0, Delta=1.0):
    return np.array([Delta * np.sin(kx), Delta * np.sin(ky), M - 2 * t * (np.cos(kx) + np.cos(ky))])


def lower_vec(kx, ky, M, t=1.0, Delta=1.0):
    dv = dvec(kx, ky, M, t, Delta)
    w, v = np.linalg.eigh(dv[0] * X + dv[1] * Y + dv[2] * Z)
    return v[:, 0]                              # 최저 고유값(−|d|) 밴드 = lower band


def _sign(x):
    return (x > 0) - (x < 0)


def mass_sign_chern(M, t=1.0):
    """path A: exact 정수공식(lower band). TRIM Dirac 질량 부호합 → C ∈ {0,±1}. 정수 산술만."""
    return (2 * _sign(M) - _sign(M - 4 * t) - _sign(M + 4 * t)) // 2


def fhs_chern(M, N=24, t=1.0, Delta=1.0):
    """path B: FHS 격자 Chern(gauge-invariant 정수). lower band, path A 와 무관 독립."""
    ks = np.linspace(0, 2 * np.pi, N, endpoint=False)
    U = [[lower_vec(kx, ky, M, t, Delta) for ky in ks] for kx in ks]
    F = 0.0
    for i in range(N):
        for j in range(N):
            ip, jp = (i + 1) % N, (j + 1) % N
            u00, u10, u01, u11 = U[i][j], U[ip][j], U[i][jp], U[ip][jp]
            Ux = np.vdot(u00, u10); Ux /= abs(Ux)
            Uy2 = np.vdot(u10, u11); Uy2 /= abs(Uy2)
            Ux2 = np.vdot(u01, u11); Ux2 /= abs(Ux2)
            Uy = np.vdot(u00, u01); Uy /= abs(Uy)
            F += np.angle(Ux * Uy2 / Ux2 / Uy)
    return int(round(F / (2 * np.pi))), F / (2 * np.pi)


def min_gap(M, N=32, t=1.0, Delta=1.0):
    ks = np.linspace(0, 2 * np.pi, N, endpoint=False)
    return min(np.linalg.norm(dvec(kx, ky, M, t, Delta)) for kx in ks for ky in ks)


def main():
    quick = "--quick" in sys.argv
    R = {}
    t = 1.0
    Ngrid = 16 if quick else 24

    # M scan(단위 t): 세 상(0,+1,−1) 을 모두 통과. 0.0001=transition 바로 안쪽(0<M<4t → +1)
    scan = {-5.0: 0, -2.0: -1, 0.0001: 1, 2.0: 1, 5.0: 0}

    # 1. path A 닫힌형 mass-sign 이 M 스캔 위상값과 일치
    R["closed_form_chern_matches_M_scan"] = all(mass_sign_chern(M, t) == c for M, c in scan.items())

    # 2. path B FHS 격자 numerics 가 정수로 양자화(gauge-invariant 격자정리)
    fhs = {M: fhs_chern(M, Ngrid, t) for M in scan}
    R["fhs_lattice_numeric"] = all(abs(cf - ci) < 0.05 for (ci, cf) in fhs.values())

    # 3. 두 경로 정수 일치(★lower band 규약 정렬 → 정확히 같은 부호)
    R["pathA_pathB_agree_integer"] = all(
        fhs[M][0] == mass_sign_chern(M, t) for M in scan)

    # 4. 위상 다이어그램: C ∈ {0,+1,−1} 세 상 모두 실현(ℤ 성격)
    realized = {mass_sign_chern(M, t) for M in scan}
    R["three_phases_0_p1_m1"] = (realized == {0, 1, -1})

    # 5. 1D↔2D 상보(AZ 차원사다리): class D 는 1D=ℤ₂(Pfaffian) · 2D=ℤ(Chern)
    ladder = {"1D_class_D": ("Z2", {0, 1}), "2D_class_D": ("Z", realized)}
    R["class_d_1d_z2_2d_z_ladder"] = (
        ladder["1D_class_D"][0] == "Z2" and ladder["1D_class_D"][1] == {0, 1}
        and ladder["2D_class_D"][0] == "Z" and ladder["2D_class_D"][1] == {-1, 0, 1}
        and realized != {0, 1})            # 2D 는 ℤ₂ 를 넘어선 상들(−1 실현) = 진짜 ℤ

    # 6. gap: 위상전이 M∈{0,±4t} 에서 gap 닫힘, 위상/자명 상 내부는 gap>0
    R["gap_closes_at_transition"] = all(min_gap(M) < 1e-6 for M in (-4.0, 0.0, 4.0))
    R["gap_open_in_phase"] = all(min_gap(M) > 0.1 for M in (-2.0, 2.0, 5.0))

    # teeth: trivial(|M|>4t) 은 반드시 C==0
    R["teeth_trivial_zero"] = (mass_sign_chern(5.0, t) == 0 and mass_sign_chern(-5.0, t) == 0
                               and fhs[5.0][0] == 0 and fhs[-5.0][0] == 0)

    # teeth: gap-closing M=0 에서 두 상 경계(C 불연속) — 바로 아래/위 부호 반대
    R["teeth_gap_closing_discontinuity"] = (
        mass_sign_chern(-0.5, t) == -1 and mass_sign_chern(0.5, t) == 1
        and min_gap(0.0) < 1e-6)

    ok = all(R.values())
    if not quick:
        print("2D spinless p+ip 초전도체 class-D ℤ Chern 정수 관측 (AZ 차원사다리, witness — seal 아님):",
              flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  Chern(M scan, lower band): " + " · ".join(
            f"M={M:g}→C={mass_sign_chern(M, t)}(FHS {fhs[M][0]})" for M in scan), flush=True)
        print("  위상 다이어그램: 0<M<4t→C=+1 · −4t<M<0→C=−1 · |M|>4t→C=0 "
              "(mass-sign exact == FHS 격자 numerics, ★lower band 규약)", flush=True)
        print("  ★AZ 차원사다리: class D 는 1D=ℤ₂(Pfaffian sign, kitaev_class_d) → 2D=ℤ(Chern). "
              "particle-hole 대칭 초전도체의 차원별 위상분류(QWZ class A 와 상보).", flush=True)
        print("  ★정직: Chern **정수**=위상 관측(mass-sign exact + FHS 확인)·부호규약=lower band 고정. "
              "ground-state 회로(무리수 각도)=봉인 아님·free-fermion 한정·edge/임계=범위밖·신규 module 0·root 불변 sidecar.",
              flush=True)
    print(f"class_d_2d_chern_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
