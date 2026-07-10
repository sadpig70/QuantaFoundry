#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""class_diii_observe — TrackHE13 P1: 1D 시간역전 초전도체(AZ class DIII) ℤ₂ witness (관측, seal 아님).

AZ 대칭클래스 사다리 확장: 1D Kitaev(class D, ℤ₂ Pfaffian, [[kitaev_class_d_observe]])·2D p+ip
(class D, ℤ Chern, [[class_d_2d_chern_observe]])·3D class AII(ℤ₂) 와 상보. **class DIII** = 시간역전
T(T²=−1, Kramers)·particle-hole C(C²=+1)·chiral S=T·C 를 모두 가진 초전도체 — 1D 에서 ℤ₂,
각 끝단에 Majorana **Kramers 쌍**(Kramers-pair of Majoranas). report13 수렴축(8/8 external runtimes).

모델(4-band, spin σ ⊗ Nambu τ). 두 시간역전 켤레 Kitaev chain 을 Rashba 항으로 결합:
  H(k) = (−2t cos k − μ)·σ0⊗τz + Δ sin k·(σz⊗τx) + α sin k·(σy⊗τ0).
대칭 대수(전부 수치검증, 신뢰 없음):
  T = i·σy⊗τ0·K,  T H(k) T⁻¹ = H(−k),  T² = −1  (Kramers).
  C = σz⊗τx·K,     C H(k) C⁻¹ = −H(−k), C² = +1.
  S = T·C ∝ σx⊗τx (unitary chiral),  {S, H(k)} = 0,  S² = +1.
  ★α≠0 이 두 Kitaev 켤레를 결합 — TRS 가 교차를 보호(DIII ℤ₂ ≠ 단순 class-D 두 벌). α=0 이면
    σz 섹터로 분해 = 두 독립 class-D Kitaev(각각 임의변형 가능, ℤ₂ 보호 상실).

두 독립 경로로 ℤ₂ 불변량 ν:
  path A ★**닫힌형 Pfaffian(운동량공간, 정확 정수)**: T-adapted chiral 기저(Vp=S+1 고유공간·
    Vm=T·Vp)에서 H 는 반대각 블록 q(k) — TRIM k=0,π 에서 q 반대칭 → Pfaffian 정의됨. 게이지불변
    불변량 (−1)^ν = ∏_{k*∈{0,π}} Pf[q(k*)]/√det[q(k*)] (연속 branch). H(TRIM)=c·σ0τz,
    c(0)=−2t−μ·c(π)=2t−μ → **(−1)^ν = sign(μ²−4t²)** 닫힌형: |μ|<2t ⟺ ν=1(위상)·|μ|>2t ⟺ ν=0.
  path B **유한 open chain ED(실공간, 독립)**: 4L×4L(L≤20) 정확대각화. 위상상은 각 끝단 Majorana
    Kramers 쌍 → **near-zero mode 4개**(자명상 0). 전 스펙트럼 Kramers 2-겹(open chain T-대칭).
  gap-closing: μ=±2t(위상전이).

정직 경계(★관측·seal 아님, root 불변 sidecar): witness = class-DIII ℤ₂ 위상불변량(Pfaffian 부호, exact
  정수). ★불변량=정수(부호규약 고정)·봉인 아님. spectrum 연속체=관측. free-fermion(BdG 2차) 한정·
  T/C 규약 고정·Δ=0 gapless 제외. ★운동량공간 same-k Kramers 겹침은 TRIM 한정(generic k 는 비겹침,
  Kramers 짝은 k↔−k) — 전-겹침은 실공간 open chain 성질. chiral det-q **winding**=0(양 상) → DIII ℤ₂
  는 AIII winding 아니라 Pfaffian(정직). 신규 module 0.

사용: python scripts/class_diii_observe.py [--quick]
"""
from __future__ import annotations
import os, sys, json
import numpy as np

from qf_witness.core.paths import ROOT
OUT = os.path.join(ROOT, ".pgf", "proofs", "CLASS-DIII-OBSERVE.json")

s0 = np.eye(2, dtype=complex)
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)


def kron(a, b):
    return np.kron(a, b)                        # spin(σ) ⊗ Nambu(τ)


# 대칭 연산자 (antiunit = U·K)
T_U = 1j * kron(sy, s0)                         # T = T_U K, T²=−1
C_U = kron(sz, sx)                             # C = C_U K, C²=+1
S = kron(sx, sx)                               # chiral = T·C (unitary)


def Hk(k, mu, t=1.0, Delta=1.0, alpha=0.5):
    """1D class-DIII BdG Bloch Hamiltonian H(k) (4-band)."""
    return ((-2 * t * np.cos(k) - mu) * kron(s0, sz)
            + Delta * np.sin(k) * kron(sz, sx)
            + alpha * np.sin(k) * kron(sy, s0))


def _anti(U, M):
    """antiunitary 켤레 U·M*·U⁻¹ (= U K M K⁻¹ U⁻¹)."""
    return U @ M.conj() @ np.linalg.inv(U)


# ── path A: T-adapted chiral 기저(k-무관 고정) ──
_w, _v = np.linalg.eigh(S)
_Vp = _v[:, _w > 0]                            # S=+1 고유공간 (4×2)
_Vm = T_U @ _Vp.conj()                         # T·Vp = S=−1 고유공간


def qk(k, mu, t=1.0, Delta=1.0, alpha=0.5):
    """chiral 기저 반대각 블록 q(k) = Vp† H Vm (게이지 고정)."""
    return _Vp.conj().T @ Hk(k, mu, t, Delta, alpha) @ _Vm


def nu_closed(mu, t=1.0):
    """path A 닫힌형: (−1)^ν = sign(μ²−4t²) → ν=1 (위상) if |μ|<2t. 정수 산술."""
    return 1 if (mu * mu - 4 * t * t) < -1e-12 else 0


def nu_pfaffian(mu, t=1.0, Delta=1.0, alpha=0.5, N=2000):
    """path A 수치: (−1)^ν = ∏_{k*} Pf[q(k*)]/√det[q(k*)] (연속 branch). ±1 반환."""
    ks = np.linspace(0, np.pi, N)
    dets = np.array([np.linalg.det(qk(k, mu, t, Delta, alpha)) for k in ks])
    ang = np.unwrap(np.angle(dets))
    sqrtdet = np.sqrt(np.abs(dets)) * np.exp(1j * ang / 2)   # 연속 √det
    pf0 = qk(0.0, mu, t, Delta, alpha)[0, 1]                 # 2×2 반대칭 Pf = q[0,1]
    pfpi = qk(np.pi, mu, t, Delta, alpha)[0, 1]
    val = (pf0 / sqrtdet[0]) * (pfpi / sqrtdet[-1])
    return 1 if val.real < 0 else 0                          # (−1)^ν = −1 → ν=1


def winding_detq(mu, t=1.0, Delta=1.0, alpha=0.5, N=2000):
    """chiral det-q winding (AIII 정수) — DIII 에선 양 상 모두 0(정직: DIII≠AIII)."""
    ks = np.linspace(0, 2 * np.pi, N, endpoint=False)
    dets = np.array([np.linalg.det(qk(k, mu, t, Delta, alpha)) for k in ks])
    ang = np.unwrap(np.angle(dets))
    return int(round((ang[-1] - ang[0] + (ang[1] - ang[0])) / (2 * np.pi)))


# ── path B: 실공간 open chain ──
def H_real(L, mu, t=1.0, Delta=1.0, alpha=0.5, extra=None):
    """유한 open chain BdG (4L×4L). extra=on-site 4×4 추가항(teeth)."""
    onsite = -mu * kron(s0, sz)
    Th = (-t * kron(s0, sz) + (Delta / (2j)) * kron(sz, sx)
          + (alpha / (2j)) * kron(sy, s0))     # hopping j→j+1
    d = 4
    H = np.zeros((d * L, d * L), dtype=complex)
    for j in range(L):
        H[d * j:d * j + d, d * j:d * j + d] = onsite
        if extra is not None:
            H[d * j:d * j + d, d * j:d * j + d] += extra
    for j in range(L - 1):
        H[d * (j + 1):d * (j + 1) + d, d * j:d * j + d] += Th
        H[d * j:d * j + d, d * (j + 1):d * (j + 1) + d] += Th.conj().T
    return H


def zero_mode_count(L, mu, thr=1e-2, **kw):
    E = np.linalg.eigvalsh(H_real(L, mu, **kw))
    return int(np.sum(np.abs(E) < thr))


def max_kramers_split(L, mu, **kw):
    """전 스펙트럼 2-겹 Kramers 여부: 짝 (E[2i],E[2i+1]) 최대 분열."""
    E = np.sort(np.linalg.eigvalsh(H_real(L, mu, **kw)))
    return float(np.max(np.abs(E[1::2] - E[0::2])))


def min_gap(mu, t=1.0, Delta=1.0, alpha=0.5, N=400):
    ks = np.linspace(0, 2 * np.pi, N, endpoint=False)
    return min(float(np.min(np.abs(np.linalg.eigvalsh(Hk(k, mu, t, Delta, alpha)))))
               for k in ks)


def main():
    quick = "--quick" in sys.argv
    t = 1.0
    R = {}
    Lb = 16 if quick else 20
    Npf = 800 if quick else 2000

    # 1. 대칭 대수(전부 수치검증): TRS·PHS·chiral·제곱부호
    ks_sym = np.linspace(-3, 3, 21 if quick else 41)
    R["T_sq_minus1"] = np.allclose(T_U @ T_U.conj(), -np.eye(4))
    R["C_sq_plus1"] = np.allclose(C_U @ C_U.conj(), np.eye(4))
    R["S_sq_plus1"] = np.allclose(S @ S, np.eye(4))
    R["S_eq_TC"] = np.allclose(np.abs(T_U @ C_U.conj()), np.abs(S))    # S ∝ T·C
    R["TRS_holds"] = all(np.allclose(_anti(T_U, Hk(k, 0.7)), Hk(-k, 0.7)) for k in ks_sym)
    R["PHS_holds"] = all(np.allclose(_anti(C_U, Hk(k, 0.7)), -Hk(-k, 0.7)) for k in ks_sym)
    R["chiral_holds"] = all(np.allclose(S @ Hk(k, 0.7) + Hk(k, 0.7) @ S, 0) for k in ks_sym)

    # μ 스캔(단위 t): 위상경계 |μ|=2t. 위상 4점·자명 4점(각 ≥3).
    topo = [0.0, 0.5, 1.0, 1.5]
    triv = [2.5, 3.0, 4.0, -3.0]
    scan = topo + triv

    # 2. path A 닫힌형(sign(μ²−4t²)) == path A 수치 Pfaffian
    R["closed_form_eq_pfaffian"] = all(
        nu_closed(m, t) == nu_pfaffian(m, t, N=Npf) for m in scan)

    # 3. path A(Pfaffian) == path B(open chain zero-mode count): 전 스캔점 일치
    zmc = {m: zero_mode_count(Lb, m) for m in scan}
    R["pathA_eq_pathB"] = all(
        (nu_pfaffian(m, t, N=Npf) == 1) == (zmc[m] == 4) for m in scan)

    # 4. 위상상: Majorana Kramers 쌍 = zero-mode 4개(끝단 2×2) · 자명상 0
    R["topological_4_zero_modes"] = all(zmc[m] == 4 for m in topo)
    R["trivial_0_zero_modes"] = all(zmc[m] == 0 for m in triv)

    # 5. 전 스펙트럼 Kramers 2-겹(open chain T-대칭, T²=−1)
    R["kramers_full_degeneracy"] = all(max_kramers_split(Lb, m) < 1e-9 for m in (0.7, 3.0))
    R["real_chain_TRS"] = np.allclose(
        _anti(np.kron(np.eye(Lb), T_U), H_real(Lb, 0.7)), H_real(Lb, 0.7))

    # 6. gap: 위상전이 μ=±2t 닫힘, 상 내부 열림
    R["gap_closes_at_pm2t"] = (min_gap(2.0) < 0.05 and min_gap(-2.0) < 0.05)
    R["gap_open_in_phase"] = (min_gap(0.0) > 0.3 and min_gap(3.0) > 0.3)

    # 7. ★정직: chiral det-q winding = 0 (양 상) → DIII ℤ₂ 는 AIII winding 아님(Pfaffian)
    R["detq_winding_zero_both"] = (winding_detq(0.0, N=Npf) == 0
                                   and winding_detq(3.0, N=Npf) == 0)

    # teeth (i): TRS 깨기(extra=σx⊗τz) → Kramers 2-겹 붕괴 + 실공간 T-대칭 상실
    ext = 0.5 * kron(sx, sz)
    R["teeth_break_trs_lifts_kramers"] = (
        max_kramers_split(Lb, 0.7, extra=ext) > 1e-3
        and not np.allclose(_anti(np.kron(np.eye(Lb), T_U),
                                  H_real(Lb, 0.7, extra=ext)), H_real(Lb, 0.7, extra=ext)))

    # teeth (ii): α=0 → σz 섹터 분해(두 독립 class-D Kitaev). spin 교차블록 = 0.
    L2 = 6
    H_a0 = H_real(L2, 0.7, alpha=0.0)
    Pup = np.zeros((4 * L2, 4 * L2)); Pdn = np.zeros((4 * L2, 4 * L2))
    for j in range(L2):
        for nam in range(2):
            Pup[4 * j + nam, 4 * j + nam] = 1          # spin↑ (σ index 0)
            Pdn[4 * j + 2 + nam, 4 * j + 2 + nam] = 1  # spin↓ (σ index 1)
    off_a0 = float(np.max(np.abs(Pup @ H_a0 @ Pdn)))
    off_ac = float(np.max(np.abs(Pup @ H_real(L2, 0.7, alpha=0.5) @ Pdn)))
    R["teeth_alpha0_decouples"] = (off_a0 < 1e-12 and off_ac > 1e-3)

    ok = bool(all(R.values()))

    # ── sidecar JSON ──
    res = {
        "ok": ok,
        "deterministic": True,
        "axis": "AZ class DIII — 1D 시간역전 초전도체 ℤ₂ (Majorana Kramers pair), report13 P1 (8/8)",
        "model": ("H(k)=(−2t cos k−μ)σ0τz + Δ sin k·σzτx + α sin k·σyτ0 ; "
                  "T=i σyτ0 K (T²=−1), C=σzτx K (C²=+1), S=T·C∝σxτx (chiral)"),
        "invariant": {
            "path_A_closed_form": "(−1)^ν = sign(μ²−4t²) ; |μ|<2t ⟺ ν=1",
            "path_A_pfaffian": "∏_{k*∈{0,π}} Pf[q(k*)]/√det[q(k*)] (T-adapted chiral basis, 연속 branch)",
            "path_B": "open chain ED — 위상 ν=1 ⟺ near-zero mode 4개(끝단 Majorana Kramers 쌍)",
            "phase_scan": {str(m): {"nu_closed": nu_closed(m, t),
                                    "nu_pfaffian": nu_pfaffian(m, t, N=Npf),
                                    "zero_modes": zmc[m]} for m in scan},
            "detq_winding_both_phases": [winding_detq(0.0, N=Npf), winding_detq(3.0, N=Npf)],
        },
        "checks": R,
        "honest_boundary": (
            "관측(위상불변량 산출) — 회로 봉인 아님. invariant = exact 정수(부호규약 고정)·"
            "spectrum 연속체 = 관측. free-fermion(BdG 2차) 한정·T/C 규약 고정·Δ=0 gapless 제외. "
            "운동량공간 same-k Kramers 겹침은 TRIM 한정(generic k 비겹침, 짝은 k↔−k) — 전-겹침은 "
            "open chain 성질. chiral det-q winding=0(양 상)→DIII ℤ₂=Pfaffian(AIII winding 아님). "
            "신규 module 0·root 불변 sidecar."),
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"_schema": "class-diii-observe-v1",
                   "_note": "1D class-DIII TR 초전도체 ℤ₂ witness: T²=−1 Kramers·C²=+1·chiral S=TC·"
                            "Pfaffian(운동량) == open-chain Majorana Kramers 쌍(실공간)·teeth. "
                            "관측·신규 module 0·root 불변.",
                   "observation": res}, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")

    if not quick:
        print("1D 시간역전 초전도체 class-DIII ℤ₂ 관측 (AZ 대칭클래스 확장, witness — seal 아님):",
              flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  모델: H(k)=(−2t cos k−μ)σ0τz + Δ sin k σzτx + α sin k σyτ0 · "
              "T=i σyτ0 K(T²=−1)·C=σzτx K(C²=+1)·S=T·C∝σxτx(chiral)", flush=True)
        print("  위상다이어그램(ν): " + " · ".join(
            f"μ={m:g}→ν={nu_pfaffian(m, t, N=Npf)}(zm {zmc[m]})" for m in scan), flush=True)
        print("  path A 닫힌형 (−1)^ν=sign(μ²−4t²) == path A Pfaffian(T-adapted chiral) "
              "== path B open-chain Majorana Kramers 쌍(zero-mode 4)", flush=True)
        print("  ★DIII: T²=−1 Kramers → 각 끝단 Majorana **쌍**·α 결합이 TRS 보호(α=0 이면 두 독립 "
              "class-D Kitaev 로 분해). det-q winding=0 → ℤ₂ 는 Pfaffian(AIII winding 아님).", flush=True)
        print("  ★정직: 위상불변량 정수·봉인 아님·spectrum 관측·free-fermion 한정·신규 module 0·root 불변 sidecar.",
              flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"class_diii_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
