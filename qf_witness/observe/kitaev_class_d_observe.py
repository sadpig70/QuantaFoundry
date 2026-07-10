#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kitaev_class_d_observe — TrackHE11 P5: 1D Kitaev chain class-D ℤ₂ 위상초전도체 witness (관측, seal 아님).

report11 수렴축(topological superconductor, 3/8). §3n P6·§4 "topological superconductor 아직 없음" 관문.
★**AZ 대칭클래스 신축**: 2D Chern(TrackHE9 P3, class A/TR-broken, ℤ)·3D ℤ₂(TrackHE10 P6, class AII/TR-preserved)
와 달리 **class D**(particle-hole 대칭, BdG 초전도, 1D, ℤ₂) — Majorana zero mode. 기봉인 Bogoliubov Pfaffian(HE)
직접 소비·Majorana braid(HE7)의 위상적 뿌리.

1D Kitaev chain(spinless p-wave SC) BdG Hamiltonian(Nambu τ):
  H(k) = (−2t cos k − μ) τ_z + 2Δ sin k · τ_y,  d_z(k)=−2t cos k−μ · d_y(k)=2Δ sin k.

두 독립 경로로 ℤ₂ 강불변량 ν:
  path A ★**닫힌형 Pfaffian**: TRIM k=0,π 의 BdG Pfaffian 부호. Pf[H_{k=0}]∝(μ+2t)·Pf[H_{k=π}]∝(μ−2t) →
    **(−1)^ν = sign(μ+2t)·sign(μ−2t) = sign(μ²−4t²)**. |μ|<2t ⟺ ν=1(위상, Majorana zero mode)·|μ|>2t ⟺ ν=0.
  path B **수치 winding**(독립): (d_z(k), d_y(k)) 곡선이 원점을 감는 홀짝성(winding parity) → ν. 닫힌형과 무관.
  gap-closing: μ=±2t(위상전이, gap=0).

정직 경계(★관측·seal 아님, root 불변 sidecar): witness = class-D ℤ₂ 위상불변량(Pfaffian 부호, exact 정수).
  ★위상불변량=정수(부호규약 고정)·봉인 아님. free-fermion(2차) 한정(상호작용=ℤ→ℤ₈ 축소 범위밖)·PHS 규약 고정·
  Δ=0 gapless 제외. 신규 module 0. [[chern-higher-observe]](class A)·3D ℤ₂(class AII)와 AZ class 상보.

사용: python -m qf_witness.observe.kitaev_class_d_observe [--quick]
"""
from __future__ import annotations
import sys
import numpy as np


def _sign(x):
    return int(x > 1e-12) - int(x < -1e-12)


def nu_closed(mu, t):
    """path A: (−1)^ν = sign(μ²−4t²) → ν=1 (위상) if |μ|<2t."""
    return 1 if (mu * mu - 4 * t * t) < -1e-12 else 0


def nu_winding(mu, t, Delta=1.0, N=400):
    """path B: (d_z,d_y) 원점 감음수 parity (독립 수치)."""
    ks = np.linspace(0, 2 * np.pi, N, endpoint=False)
    dz = -2 * t * np.cos(ks) - mu
    dy = 2 * Delta * np.sin(ks)
    ang = np.unwrap(np.arctan2(dy, dz))
    w = (ang[-1] - ang[0] + (ang[1] - ang[0])) / (2 * np.pi)
    return int(round(abs(w))) % 2


def min_gap(mu, t, Delta=1.0, N=200):
    ks = np.linspace(0, 2 * np.pi, N, endpoint=False)
    dz = -2 * t * np.cos(ks) - mu
    dy = 2 * Delta * np.sin(ks)
    return float(np.min(np.sqrt(dz ** 2 + dy ** 2)))


def main():
    quick = "--quick" in sys.argv
    R = {}
    t = 1.0
    phase = {0.0: 1, 1.0: 1, -1.5: 1, 3.0: 0, -3.0: 0, 2.5: 0, 1.9: 1}

    # 1. 위상 다이어그램 (닫힌형 Pfaffian): |μ|<2t → ν=1
    R["closed_form_phase_diagram"] = all(nu_closed(m, t) == nu for m, nu in phase.items())

    # 2. path A(닫힌형) == path B(수치 winding)
    R["closed_form_eq_winding"] = all(nu_closed(m, t) == nu_winding(m, t) for m in phase)

    # 3. 위상(ν=1, Majorana) vs 자명(ν=0)
    R["topological_majorana_nonzero"] = (nu_closed(0.0, t) == 1 and nu_closed(1.0, t) == 1)
    R["trivial_zero"] = (nu_closed(3.0, t) == 0 and nu_closed(-3.0, t) == 0)

    # 4. gap-closing at μ=±2t
    R["gap_closes_at_pm_2t"] = (min_gap(2.0, t) < 0.05 and min_gap(-2.0, t) < 0.05)
    R["gap_open_in_phase"] = (min_gap(0.0, t) > 0.3 and min_gap(3.0, t) > 0.3)

    # 5. Pfaffian 부호 = 닫힌형 (TRIM k=0,π)
    R["pfaffian_sign_eq_closed"] = all(
        (1 if _sign(m + 2 * t) * _sign(m - 2 * t) < 0 else 0) == nu_closed(m, t) for m in phase)

    # teeth: 위상 판정 nontrivial (Majorana ≠ trivial)
    R["teeth"] = (nu_closed(0.0, t) != nu_closed(3.0, t) and nu_closed(1.9, t) == 1)

    ok = all(R.values())
    if not quick:
        print("1D Kitaev chain class-D ℤ₂ 위상초전도체 (Pfaffian) 관측 (AZ class 신축, witness — seal 아님):",
              flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  위상다이어그램(ν): |μ|<2t→ν=1(위상·Majorana zero mode) · |μ|>2t→ν=0(자명) "
              "((−1)^ν=sign(μ²−4t²) Pfaffian == 수치 winding)", flush=True)
        print("  ★AZ 대칭클래스: 2D Chern(class A/TR-broken, ℤ)·3D ℤ₂(class AII/TR-preserved) 와 달리 "
              "class D(particle-hole, BdG 초전도, ℤ₂). Bogoliubov Pfaffian 직소비·Majorana braid 위상뿌리.", flush=True)
        print("  ★정직: 위상불변량 정수·봉인 아님·free-fermion 한정·PHS 규약 고정·신규 module 0·root 불변 sidecar.",
              flush=True)
    print(f"kitaev_class_d_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
