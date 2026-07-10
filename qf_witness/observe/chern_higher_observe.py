#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""chern_higher_observe — TrackHE9 P3: |C|≥2 고차 Chern 정수 위상 불변량 witness (관측, seal 아님).

report9 수렴축(|C|≥2 고차 Chern 3/8). TrackHE8 P3(2D QWZ, |C|≤1)의 질적 확장 — spin-½ Pauli 를
**spin-S multi-Weyl**(3-band S=1 · 4-band S=3/2)로 승격하여 최저밴드 Chern 수를 |C|=2,3 으로 끌어올린다:
  H(k) = sin(kx) S_x + sin(ky) S_y + (m + cos kx + cos ky) S_z,  S = spin-S 행렬(2S+1 밴드).

두 독립 정수 경로로 고차 Chern C_lowest 확립(최저밴드, 규약 = [[chern_observe]] 와 동일 lower band):
  1. ★**exact 정수공식**(부동소수 없음): 스핀-코히런트 밴드 Berry 곡률 = 2·m_S·(d̂ 감음수) →
     최저밴드(m_S=−S) **C_lowest = 2S · C_½(m)** — 여기서 C_½ = mass_sign_chern(TRIM Dirac 질량 부호,
     [[chern_observe]] 재사용). 정수 산술만: S=1 → C∈{0,±2} · S=3/2 → C∈{0,±3}.
  2. **FHS(Fukui-Hatsugai-Suzuki) 격자 numerics**(독립 확인): 진짜 multi-band(3×3/4×4) 최저밴드 U(1)
     link → plaquette field strength 합/2π = gauge-invariant **정수** — path 1 과 일치(|C|=2,3 재현).
  3. teeth: |C|=2(spin-1)·|C|=3(spin-3/2) ≠ |C|=1(spin-½) ≠ 0(자명) — 고차성이 단위 Chern 과 혼동 불가.

정직 경계(seal 아님, root 불변 sidecar): 관측 = 고차 Chern **정수**(위상 불변량, 2S·C_½ exact + FHS 확인).
  ★부호 규약 = lower band(고정 명시). ground-state prep 회로는 일반 k 에서 무리수 각도 → 봉인 아님
  (신규 module 회피). C_lowest=2S·C_½ 는 H=d·S 의 밴드가 정확한 회전 |m_S⟩ 상태라 exact(격자 FHS 확인).
  유한격자 Berry sum·edge mode·bulk-boundary = 관측/범위밖. 신규 module 0. [[chern_observe]](|C|≤1)와
  교차(같은 d-벡터, 밴드/스핀만 확장 = 고차 위상 관측).

사용: python scripts/chern_higher_observe.py [--quick]
"""
from __future__ import annotations
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chern_observe import mass_sign_chern            # 기존 witness 재사용(제1 경로 스핀-½ 코어)


def spin_matrices(S):
    """spin-S 행렬 (S_x, S_y, S_z), 밴드 순서 |S>, |S−1>, ..., |−S> (index 0 = 최고 m_S)."""
    dim = int(round(2 * S + 1))
    ms = np.array([S - i for i in range(dim)])         # S, S-1, ..., -S
    Sz = np.diag(ms).astype(complex)
    Sp = np.zeros((dim, dim), dtype=complex)           # S+ |m> = c |m+1>
    for i in range(1, dim):
        m = ms[i]
        Sp[i - 1, i] = np.sqrt(S * (S + 1) - m * (m + 1))
    Sm = Sp.conj().T
    return (Sp + Sm) / 2, (Sp - Sm) / (2j), Sz


def _Hk(kx, ky, m, Sx, Sy, Sz):
    return np.sin(kx) * Sx + np.sin(ky) * Sy + (m + np.cos(kx) + np.cos(ky)) * Sz


def _lowest_vec(kx, ky, m, Sx, Sy, Sz):
    w, v = np.linalg.eigh(_Hk(kx, ky, m, Sx, Sy, Sz))
    return v[:, 0]                                      # 최저 고유값 밴드(m_S = −S)


def exact_higher_chern(m, S):
    """exact 정수공식(최저밴드): C_lowest = 2S · C_½(m). 정수 산술만."""
    return int(round(2 * S)) * mass_sign_chern(m)


def fhs_higher_chern(m, S, N=24):
    """FHS 격자 Chern(gauge-invariant 정수) — 진짜 multi-band 최저밴드. 독립 경로."""
    Sx, Sy, Sz = spin_matrices(S)
    ks = np.linspace(0, 2 * np.pi, N, endpoint=False)
    U = [[_lowest_vec(kx, ky, m, Sx, Sy, Sz) for ky in ks] for kx in ks]
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


def min_gap(m, S, N=24):
    Sx, Sy, Sz = spin_matrices(S)
    ks = np.linspace(0, 2 * np.pi, N, endpoint=False)
    g = []
    for kx in ks:
        for ky in ks:
            w = np.linalg.eigvalsh(_Hk(kx, ky, m, Sx, Sy, Sz))
            g.append(w[1] - w[0])                       # 최저밴드 위 gap
    return min(g)


def main():
    quick = "--quick" in sys.argv
    R = {}
    Ngrid = 16 if quick else 24
    ms_topo = (0.5, 1.0, 1.5, -0.5, -1.0, -1.5)
    ms_triv = (3.0, -3.0, 2.5)
    ms_all = ms_topo + ms_triv

    # 1. exact 정수공식: spin-1 → |C|=2, spin-3/2 → |C|=3 (2S·C_½)
    R["spin1_exact_C2"] = all(exact_higher_chern(m, 1.0) == 2 * mass_sign_chern(m) for m in ms_all)
    R["spin32_exact_C3"] = all(exact_higher_chern(m, 1.5) == 3 * mass_sign_chern(m) for m in ms_all)

    # 2. FHS 격자 numerics == exact 정수공식 (독립 경로 일치) + 정수 양자화
    fhs_match = True
    fhs_int = True
    for S in (1.0, 1.5):
        for m in ms_all:
            ci, cf = fhs_higher_chern(m, S, Ngrid)
            if ci != exact_higher_chern(m, S):
                fhs_match = False
            if abs(cf - ci) > 0.05:                     # 격자 합이 정수에 스냅(gauge-invariant)
                fhs_int = False
    R["fhs_matches_exact"] = fhs_match
    R["fhs_integer_quantized"] = fhs_int

    # 3. 고차성: |C|=2,3 실제 달성(단위 Chern 초과)
    R["higher_chern_2_achieved"] = (exact_higher_chern(1.0, 1.0) == 2 and exact_higher_chern(-1.0, 1.0) == -2)
    R["higher_chern_3_achieved"] = (exact_higher_chern(1.0, 1.5) == 3 and exact_higher_chern(-1.0, 1.5) == -3)
    R["trivial_still_zero"] = (exact_higher_chern(3.0, 1.0) == 0 and exact_higher_chern(3.0, 1.5) == 0)

    # 4. gap: 위상상 gap-open, Dirac 점 m∈{−2,0,2} 에서 최저밴드 닫힘
    R["gap_open_in_phase"] = all(min_gap(m, 1.0) > 0.1 for m in (1.0, -1.0, 3.0))
    R["gap_closes_at_dirac"] = min_gap(0.0, 1.0) < 1e-6

    # teeth: |C|(spin-1)=2 ≠ |C|(spin-½)=1 ≠ 0; 자명은 여전히 0
    R["teeth"] = (exact_higher_chern(1.0, 1.0) == 2 and mass_sign_chern(1.0) == 1
                  and exact_higher_chern(3.0, 1.0) == 0)

    ok = all(R.values())
    if not quick:
        print("|C|≥2 고차 Chern 정수 위상 불변량 관측 (§3l P3 spin-S multi-Weyl 확장, witness — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  고차 위상(lower band): spin-1(3-band) 0<m<2→C=+2 · spin-3/2(4-band) 0<m<2→C=+3 "
              "(C_lowest = 2S·C_½ exact == FHS 격자 numerics)", flush=True)
        print("  ★정직: 고차 Chern **정수**=위상 관측(2S·C_½ exact + FHS 확인)·부호규약=lower band 고정. "
              "ground-state 회로(무리수 각도)=봉인 아님·edge mode/임계=범위밖·신규 module 0·root 불변 sidecar.",
              flush=True)
    print(f"chern_higher_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
