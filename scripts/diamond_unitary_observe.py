#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""diamond_unitary_observe — TrackHE8 P6: non-Pauli(coherent) 유니터리 채널 diamond-norm exact witness.

report8 수렴축(non-Pauli diamond 3/8). §3k P3·§4 "non-Pauli 채널 exact 부분 아직 없음" 관문 개창 —
TrackHE7 P3 Pauli-diagonal island 의 **상보 island**(coherent 유니터리 채널은 확률혼합과 질적으로 다름).
AKN/Watrous 정리: 두 유니터리 채널 Φ_U, Φ_V 의 diamond 거리 = **닫힌형**(SDP·탐색 불요, §4′b):
  ‖Φ_U − Φ_V‖◇ = 2·sin(min(Θ/2, π/2)),  Θ = U†V 고유위상을 담는 **최소 호(arc) 길이**.
  (동치: 2√(1−ν²), ν = dist(0, convhull(고유값))).

봉인된 게이트 채널(t_gate·s_gate·cs_gate·cz·h_gate 고유위상만 소비)로 관측(오라클 독립):
  Clifford+T 는 θ_j ∈ π·ℚ → diamond 값이 **cyclotomic surd exact**:
    T(Θ=π/4)=2sin(π/8)=√(2−√2) · S(Θ=π/2)=√2 · CS(Θ=π/2)=√2 · CZ(Θ=π)=**정수 2**(최대) · H(Θ=π)=**2**.
  ★**integer-surd 대조쌍 + Θ 분기 비대칭**(§4′h 넷째): Θ≥π → diamond=정수 2(구별 최대) · Θ<π → surd.
  독립 확인: (a) 2√(1−ν²) hull form 일치 (b) 상태공간 수치탐색 max 2√(1−|⟨ψ|(U⊗I)|ψ⟩|²) ≤ AKN(=상한 도달).

정직 경계(seal 아님, root 불변 sidecar): 관측 = diamond **값 자체**(고유위상→호→surd 닫힌형).
  ★Pauli island 과 disjoint(Pauli 채널은 유니터리 아님→dilation 필요; 유니터리 채널=coherent island).
  primal 최적 상태·물리적 구별 프로토콜 = 관측/범위밖. 신규 module 0. TrackHE7 P3(diamond_observe) 상보.

사용: python scripts/diamond_unitary_observe.py [--quick]
"""
from __future__ import annotations
import os, sys, re
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_mod_golden(name):
    src = open(os.path.join(ROOT, "specs", "modules", f"{name}.pg"), encoding="utf-8").read()
    m = re.search(r"```python id=golden\n(.*?)```", src, re.S)
    ns = {}
    exec(m.group(1), ns)
    return np.asarray(ns["golden"], dtype=complex)


def arc_length(phases):
    p = sorted(float(ph) % (2 * np.pi) for ph in phases)
    if len(p) == 1:
        return 0.0
    gaps = [p[i + 1] - p[i] for i in range(len(p) - 1)]
    gaps.append(2 * np.pi - p[-1] + p[0])
    return 2 * np.pi - max(gaps)


def akn_diamond(W):
    Th = arc_length(np.angle(np.linalg.eigvals(W)))
    return 2 * np.sin(min(Th / 2, np.pi / 2)), Th


def nu_hull(W, trials=6000):
    ev = np.linalg.eigvals(W)
    pts = np.c_[ev.real, ev.imag]
    n = len(pts)
    best = 1.0
    rng = np.random.default_rng(12345)          # 결정론 seed
    for _ in range(trials):
        w = rng.dirichlet(np.ones(n))
        best = min(best, float(np.hypot(*(w @ pts))))
    return best


def numeric_diamond(U, trials=6000):
    d = U.shape[0]
    UI = np.kron(U, np.eye(d))
    dim = d * d
    rng = np.random.default_rng(999)
    best = 0.0
    for _ in range(trials):
        v = rng.standard_normal(dim) + 1j * rng.standard_normal(dim)
        v /= np.linalg.norm(v)
        ov = abs(np.vdot(v, UI @ v))
        best = max(best, 2 * np.sqrt(max(0.0, 1 - ov ** 2)))
    return best


def main():
    quick = "--quick" in sys.argv
    R = {}
    T = _load_mod_golden("t_gate")
    Sg = _load_mod_golden("s_gate")
    Hg = _load_mod_golden("h_gate")
    CZ = _load_mod_golden("cz")
    CS = _load_mod_golden("cs_gate")

    surd = {
        "T_vs_I": (T, np.sqrt(2 - np.sqrt(2))),       # 2 sin(π/8)
        "S_vs_I": (Sg, np.sqrt(2)),                    # √2
        "CS_vs_I": (CS, np.sqrt(2)),                   # √2
        "CZ_vs_I": (CZ, 2.0),                          # 정수 2 (Θ=π)
        "H_vs_I": (Hg, 2.0),                           # 정수 2
        "T_vs_S": (Sg.conj().T @ T, np.sqrt(2 - np.sqrt(2))),   # U†V=S†T, Θ=π/4
    }
    trials = 2000 if quick else 6000

    exact_ok = True
    branch_ok = True
    cross_ok = True
    detail = {}
    for name, (W, val) in surd.items():
        d_akn, Th = akn_diamond(W)
        if abs(d_akn - val) > 1e-9:
            exact_ok = False
        # Θ 분기: Θ≥π → 정수 2, Θ<π → surd(<2)
        if Th >= np.pi - 1e-9:
            if abs(d_akn - 2.0) > 1e-9:
                branch_ok = False
        else:
            if d_akn >= 2.0 - 1e-9:
                branch_ok = False
        # 독립 확인: hull form + 상태탐색 ≤ AKN(상한)
        nu = nu_hull(W, trials)
        d_nu = 2 * np.sqrt(max(0.0, 1 - nu ** 2))
        d_num = numeric_diamond(W if W.shape[0] in (2, 4) else W, trials)
        if abs(d_nu - d_akn) > 5e-3 or d_num > d_akn + 2e-2:
            cross_ok = False
        detail[name] = (round(d_akn, 5), round(Th / np.pi, 3))
    R["akn_surd_exact"] = exact_ok
    R["theta_branch_int_vs_surd"] = branch_ok
    R["hull_and_search_consistent"] = cross_ok

    # ★integer-surd 대조쌍 존재
    R["integer_surd_pair"] = (abs(akn_diamond(CZ)[0] - 2.0) < 1e-9 and
                              abs(akn_diamond(T)[0] - np.sqrt(2 - np.sqrt(2))) < 1e-9)
    # teeth: 항등 채널(U=V) → diamond 0
    R["teeth_identity_zero"] = (akn_diamond(np.eye(2, dtype=complex))[0] < 1e-9)

    ok = all(R.values())
    if not quick:
        print("non-Pauli(coherent) 유니터리 채널 diamond-norm exact 관측 (§3k P3 상보 island, witness — seal 아님):",
              flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        for name, (d, thp) in detail.items():
            print(f"    {name}: ‖·‖◇={d}  Θ/π={thp}", flush=True)
        print("  ★값: T=√(2−√2)·S=√2·CS=√2·CZ=2(정수)·H=2 — Θ≥π→정수2(구별최대)·Θ<π→surd. AKN 닫힌형 == "
              "hull form == 상태탐색 상한. Pauli island disjoint(유니터리≠확률혼합)·신규 module 0·root 불변.",
              flush=True)
    print(f"diamond_unitary_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
