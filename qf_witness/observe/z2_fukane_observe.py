#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""z2_fukane_observe — TrackHE10 P6: 3D 위상절연체 ℤ₂ 강불변량 (Fu-Kane parity criterion) witness (관측, seal 아님).

report10 수렴축(3D ℤ₂, 3/8). §3m P3·§4 "3D 위상(ℤ/ℤ₂ 4밴드) 아직 없음" 관문. `chern_higher_observe`(TrackHE9
P3, 2D ℤ Chern·|C|≥2)의 **3D ℤ₂ 상보**: 2D Chern=시간반전 깨짐(TR-broken)·3D ℤ₂=시간반전 보존(TR-preserved)
symmetry-protected topological — 직교 분류축.

3D Fu-Kane-Mele 4-band 모델(σ=spin·τ=orbital Pauli):
  H(k) = sin kx·σx⊗τx + sin ky·σy⊗τx + sin kz·σz⊗τx + (m+cos kx+cos ky+cos kz)·τz
  parity P = τz (inversion). 8 TRIM Λ=(0/π)³ 에서 sin=0 → H=M(Λ)·τz, M=m+Σcos.

두 독립 경로로 강불변량 ν₀:
  path A ★**닫힌형 정수공식**: δ(Λ) = −sign(M(Λ)) (occupied Kramers pair parity), (−1)^{ν₀}=∏_{8 TRIM}δ(Λ).
    M ∈ {m+3, m+1(×3), m−1(×3), m−3} → 위상다이어그램 ν₀=1: m∈(−3,−1)∪(1,3)·ν₀=0: 그 외. 정수 부호만.
  path B **수치 eigenvector parity**(독립): 각 TRIM 에서 H(Λ) 대각화 → occupied(2 최저) 고유벡터의
    ⟨u|τz|u⟩=±1 → δ(Λ) → ν₀. 닫힌형과 무관한 계산(고유벡터 경유). path A==path B exact.
  gap-closing: m∈{−3,−1,1,3}(밴드반전)에서 gap=0, 그 외 gap>0.

정직 경계(★관측·seal 아님, root 불변 sidecar): witness = 3D ℤ₂ 위상불변량(TRIM parity, exact 정수).
  ★위상불변량=정수(부호규약=lower band·occupied parity 고정). 봉인 아님(no-go/불변량). Wilson-loop 전-BZ
  holonomy(inversion 없는 경우)·weak indices·표면상태 = 범위밖. 신규 module 0. [[chern-higher-observe]](2D ℤ)
  상보(TR-broken vs TR-preserved).

사용: python -m qf_witness.observe.z2_fukane_observe [--quick]
"""
from __future__ import annotations
import sys
import numpy as np

sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)
I2 = np.eye(2, dtype=complex)


def kron(a, b):
    return np.kron(a, b)


TAU_Z = kron(I2, sz)                                     # P = τz (orbital), σ⊗τ 순서


def Hk(kx, ky, kz, m):
    return (np.sin(kx) * kron(sx, sx) + np.sin(ky) * kron(sy, sx) + np.sin(kz) * kron(sz, sx)
            + (m + np.cos(kx) + np.cos(ky) + np.cos(kz)) * kron(I2, sz))


TRIM = [(a * np.pi, b * np.pi, c * np.pi) for a in (0, 1) for b in (0, 1) for c in (0, 1)]


def _sign(x):
    return int(x > 1e-12) - int(x < -1e-12)


def nu0_closed(m):
    """path A: δ(Λ)=−sign(M), (−1)^ν₀=∏δ."""
    prod = 1
    for (kx, ky, kz) in TRIM:
        M = m + np.cos(kx) + np.cos(ky) + np.cos(kz)
        prod *= -_sign(M)
    return 0 if prod == 1 else 1


def nu0_numeric(m):
    """path B: 각 TRIM 수치 대각화 → occupied 2밴드 parity ⟨τz⟩ 곱 → ν₀ (독립)."""
    prod = 1
    for (kx, ky, kz) in TRIM:
        H = Hk(kx, ky, kz, m)
        w, v = np.linalg.eigh(H)
        # occupied = 2 최저. Kramers pair parity = 공통 τz 고유값(축약). δ = 한 pair 의 parity.
        occ = v[:, :2]
        par = [np.real(occ[:, j].conj() @ TAU_Z @ occ[:, j]) for j in range(2)]
        # 두 occupied 는 σ-겹침(동일 τz) → δ = round(par[0]) (±1)
        delta = int(round(par[0]))
        prod *= delta
    return 0 if prod == 1 else 1


def min_gap(m, N=12):
    ks = np.linspace(0, 2 * np.pi, N, endpoint=False)
    g = 1e9
    for kx in ks:
        for ky in ks:
            for kz in ks:
                w = np.linalg.eigvalsh(Hk(kx, ky, kz, m))
                g = min(g, w[2] - w[1])                  # occupied(2) 위 gap
    return g


def main():
    quick = "--quick" in sys.argv
    R = {}

    # 1. 위상 다이어그램(닫힌형): ν₀=1 for m∈(−3,−1)∪(1,3), 0 otherwise
    phase = {2.0: 1, -2.0: 1, 1.5: 1, -1.5: 1, 0.0: 0, 0.5: 0, 4.0: 0, -4.0: 0, 2.5: 1}
    R["closed_form_phase_diagram"] = all(nu0_closed(m) == nu for m, nu in phase.items())

    # 2. path A(닫힌형) == path B(수치 eigenvector) 이중 독립경로
    R["closed_form_eq_numeric"] = all(nu0_closed(m) == nu0_numeric(m) for m in phase)

    # 3. 위상(ν₀=1) vs 자명(ν₀=0)
    R["strong_TI_nonzero"] = (nu0_closed(2.0) == 1 and nu0_closed(-2.0) == 1)
    R["trivial_zero"] = (nu0_closed(0.0) == 0 and nu0_closed(4.0) == 0)

    # 4. gap-closing at m∈{−3,−1,1,3}, gap-open in phase
    Ng = 8 if quick else 12
    R["gap_closes_at_transitions"] = all(min_gap(m, Ng) < 0.2 for m in (-3.0, -1.0, 1.0, 3.0))
    R["gap_open_in_phase"] = all(min_gap(m, Ng) > 0.3 for m in (2.0, 0.0))

    # teeth: 닫힌형 판정 nontrivial (strong TI ≠ trivial)
    R["teeth"] = (nu0_closed(2.0) != nu0_closed(0.0) and nu0_closed(-2.0) == 1)

    ok = all(R.values())
    if not quick:
        print("3D 위상절연체 ℤ₂ 강불변량 (Fu-Kane parity criterion) 관측 (2D Chern 상보, witness — seal 아님):",
              flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  위상다이어그램(강불변량 ν₀): m∈(−3,−1)∪(1,3)→ν₀=1(강 TI) · 그 외→ν₀=0(자명) "
              "(TRIM parity 닫힌형 정수 == 수치 eigenvector parity)", flush=True)
        print("  ★2D Chern(TR-broken, ℤ, chern_higher) 상보 = 3D ℤ₂(TR-preserved, symmetry-protected). "
              "위상불변량=정수(부호규약 고정)·봉인 아님·Wilson-loop 전BZ/weak indices=범위밖·신규 module 0·root 불변.",
              flush=True)
    print(f"z2_fukane_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
