#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""chern_observe — TrackHE8 P3: 2D free-fermion Chern 정수 위상 불변량 witness (관측, seal 아님).

report8 수렴축(2D Chern 5/8). §3k P2·§4 "2D Chern 은 아직 없음" 관문 개창 — 1D Kitaev/Bogoliubov Z₂
(기봉인)에서 **2D ℤ 위상**으로의 질적 도약. Qi-Wu-Zhang 2-band Chern insulator:
  H(k) = sin(kx) X + sin(ky) Y + (m + cos kx + cos ky) Z = d(k)·σ.

두 독립 경로로 Chern 정수 C 확립(lower band, 규약 고정):
  1. ★**exact mass-sign 정수공식**(§4′b, 부동소수 없음): TRIM(고대칭점 Γ/X/Y/M) Dirac 질량
     M = m+cos kx+cos ky ∈ {m+2, m, m, m−2} 의 부호로 **C = (2·sign(m) − sign(m−2) − sign(m+2))/2**
     — 정수 산술만으로 exact. 위상 다이어그램: 0<m<2 → C=+1 · −2<m<0 → C=−1 · |m|>2 → C=0.
  2. **FHS(Fukui-Hatsugai-Suzuki) 격자 numerics**(독립 확인): BZ 격자 U(1) link variable →
     plaquette field strength(주분지) 합/2π = **gauge-invariant 정수**(격자 정리로 정수 보장). path 1 과 일치.
  3. gap-closing: m∈{−2,0,2}(Dirac 점)에서 min|d|=0, 그 외 gap>0.

정직 경계(seal 아님, root 불변 sidecar): 관측 = Chern **정수**(위상 불변량, mass-sign exact + FHS 확인).
  ★부호 규약 = lower band(고정 명시, Agent 경고 = Chern sign convention-dependent). ground-state prep
  회로는 일반 k 에서 무리수 Bogoliubov 각도 → 봉인 아님(신규 module 회피). 유한격자 Berry sum·edge mode·
  임계값 = 관측/범위밖. 신규 module 0. 기봉인 제6경로(matchgate)·bogoliubov_pair 와 교차(다른 층=위상 관측).

사용: python scripts/chern_observe.py [--quick]
"""
from __future__ import annotations
import sys
import numpy as np

X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def dvec(kx, ky, m):
    return np.array([np.sin(kx), np.sin(ky), m + np.cos(kx) + np.cos(ky)])


def lower_vec(kx, ky, m):
    dv = dvec(kx, ky, m)
    w, v = np.linalg.eigh(dv[0] * X + dv[1] * Y + dv[2] * Z)
    return v[:, 0]                              # 최저 고유값(−|d|) 밴드


def _sign(x):
    return (x > 0) - (x < 0)


def mass_sign_chern(m):
    """exact 정수공식(lower band): TRIM Dirac 질량 부호 → C ∈ {0,±1}. 정수 산술만."""
    return (2 * _sign(m) - _sign(m - 2) - _sign(m + 2)) // 2


def fhs_chern(m, N=24):
    """FHS 격자 Chern(gauge-invariant 정수). 독립 경로."""
    ks = np.linspace(0, 2 * np.pi, N, endpoint=False)
    U = [[lower_vec(kx, ky, m) for ky in ks] for kx in ks]
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


def min_gap(m, N=32):
    ks = np.linspace(0, 2 * np.pi, N, endpoint=False)
    return min(np.linalg.norm(dvec(kx, ky, m)) for kx in ks for ky in ks)


def main():
    quick = "--quick" in sys.argv
    R = {}
    Ngrid = 16 if quick else 24

    # 1. 위상 다이어그램: exact mass-sign 정수공식
    phase = {0.5: 1, 1.0: 1, 1.5: 1, -0.5: -1, -1.0: -1, -1.5: -1, 3.0: 0, -3.0: 0, 2.5: 0}
    R["mass_sign_phase_diagram"] = all(mass_sign_chern(m) == c for m, c in phase.items())

    # 2. FHS 격자 numerics == mass-sign (독립 경로 일치)
    fhs_match = True
    fhs_int = True
    for m in phase:
        ci, cf = fhs_chern(m, Ngrid)
        if ci != mass_sign_chern(m):
            fhs_match = False
        if abs(cf - ci) > 0.05:                # 격자 합이 정수에 스냅(gauge-invariant 정리)
            fhs_int = False
    R["fhs_matches_mass_sign"] = fhs_match
    R["fhs_integer_quantized"] = fhs_int

    # 3. topological(±1) vs trivial(0) 구별 + gap
    R["topological_nonzero"] = (mass_sign_chern(1.0) == 1 and mass_sign_chern(-1.0) == -1)
    R["trivial_zero"] = (mass_sign_chern(3.0) == 0 and mass_sign_chern(-3.0) == 0)

    # 4. gap-closing at Dirac points m∈{−2,0,2}, gap-open at topological/trivial
    R["gap_closes_at_dirac"] = all(min_gap(m) < 1e-6 for m in (-2.0, 0.0, 2.0))
    R["gap_open_in_phase"] = all(min_gap(m) > 0.1 for m in (1.0, -1.0, 3.0))

    # teeth: trivial 은 0, topological 은 ±1 (혼동 불가)
    R["teeth"] = (mass_sign_chern(1.0) != 0 and mass_sign_chern(3.0) == 0)

    ok = all(R.values())
    if not quick:
        print("2D QWZ Chern 정수 위상 불변량 관측 (§3k P2 2D Chern 개창, witness — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  위상 다이어그램(lower band): 0<m<2→C=+1 · −2<m<0→C=−1 · |m|>2→C=0 "
              "(mass-sign exact 정수 == FHS 격자 numerics)", flush=True)
        print("  ★정직: Chern **정수**=위상 관측(mass-sign exact + FHS 확인)·부호규약=lower band 고정. "
              "ground-state 회로(무리수 각도)=봉인 아님·edge mode/임계값=범위밖·신규 module 0·root 불변 sidecar.",
              flush=True)
    print(f"chern_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
