#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""class_diii_2d_observe — TrackHE14 P4a: 2D 시간역전 초전도체(AZ class DIII) ℤ₂ witness
(관측, seal 아님).

[[class_diii_observe]](1D DIII, v13 8/8 수렴)의 **차원 상승**. 2D class DIII(T²=−1 Kramers·
C²=+1·chiral S=T·C) — helical 위상초전도체(³He-B 2D 유사): 스핀 ↑/↓ 가 반대 chirality p±ip 로
짝짓는 Balian-Werthamer d-vector 모델. AZ 잔여칸 채움: 1D D(Pfaffian ℤ₂)·2D D(Chern ℤ)·
1D DIII(ℤ₂)·2D class-D p+ip 에 이어 **2D DIII ℤ₂**.

모델(4-band BdG, Nambu (c↑,c↓,c†↑,c†↓)):
  H(k) = ξ_k τz⊗σ0 + [[0, Δ(k)],[Δ(k)†, 0]],  ξ_k = −2t(cos kx+cos ky) − μ,
  Δ(k) = (d⃗·σ⃗)(iσy),  d⃗ = Δ(sin kx, sin ky, 0)   (odd-parity spin-triplet, TRS-invariant).
대칭 대수(전부 수치검증, 신뢰 없음): T = τ0⊗(iσy) K (T²=−1) · C = τx⊗σ0 K (C²=+1) ·
  S = i·T·C (Hermitian, S²=+1, {S,H}=0).

ℤ₂ 강불변량 ν — 세 독립 경로:
  path A ★닫힌형 mass-sign(운동량 TRIM, 정확 정수): odd-parity 페어링에서
    (−1)^ν = ∏_{k*∈4 TRIM} sign(ξ(k*)) — 0<|μ|<4t ⟺ ν=1 · |μ|>4t ⟺ ν=0.
  path B ★T-adapted Pfaffian(차원환원): TRS-불변 라인 ky∈{0,π} 각각이 1D DIII —
    ν = ν₁D(ky=0) ⊕ ν₁D(ky=π), 각 라인은 chiral 기저 q 의 TRIM Pfaffian/√det(연속 branch,
    q(TRIM) 반대칭 검증). v13 1D 기계의 직접 재사용(차원 상승 서사).
  path C ★edge Majorana Kramers(실공간 cylinder ED): 위상상은 helical edge 교차 —
    near-zero mode 4개(edge 당 Kramers 쌍)·edge 국소화(>0.9)·자명상 0.
    ★모멘텀 분해 bulk-boundary: edge Dirac 위치 ky*=비자명 1D line 을 정확 추적
    (−4t<μ<0 → ky*=0 · 0<μ<4t → ky*=π).
  ★μ=0 관측: 두 TRIM((π,0),(0,π)) 동시 gap 닫힘 = 짝수 Dirac → Δν=0 (불변량 불변 전이).

teeth: (i) in-plane Zeeman hx·τz⊗σx — TRS 파괴(PHS 유지 → class D 강등)·edge Kramers 분열
  |E|≈hx (out-of-plane σz 는 교차 이동만·gap 못 엶 — helical 구조 확인, QSH 유사).
  (ii) ★s-wave 스코프 teeth: Δ₀(iσy) even-parity 도 DIII 대칭은 만족하나, path A sign 공식을
  오적용하면 ν=1 을 주장(0<μ<4t) — path B Pfaffian·path C edge 는 trivial. ⟹ 닫힌형의
  odd-parity 전제가 load-bearing (공식 적용범위 정직).

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0): 위상불변량 = 정수(부호규약 고정)·
  봉인 아님. ★float Chern/Berry 적분 미사용 — sign 닫힌형·Pfaffian 부호만. spectrum 연속체=관측·
  유한크기 cylinder=국소증거(분류정리 무주장)·free-fermion(BdG 2차) 한정·d-vector 규약 고정.

사용: python -m qf_witness.observe.class_diii_2d_observe [--quick]
"""
from __future__ import annotations
import os, sys, json
import numpy as np

from qf_witness.core.paths import ROOT
OUT = os.path.join(ROOT, ".pgf", "proofs", "CLASS-DIII-2D-OBSERVE.json")

s0 = np.eye(2, dtype=complex)
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
sz = np.array([[1, 0], [0, -1]], dtype=complex)
Z2 = np.zeros((2, 2), dtype=complex)


def blk(A, B, C, D):
    return np.block([[A, B], [C, D]])


TAU_Z = blk(s0, Z2, Z2, -s0)


def Hk(kx, ky, mu, t=1.0, D=1.0):
    xi = -2 * t * (np.cos(kx) + np.cos(ky)) - mu
    Dk = D * (np.sin(kx) * sx + np.sin(ky) * sy) @ (1j * sy)
    return blk(xi * s0, Dk, Dk.conj().T, -xi * s0)


def Hk_swave(kx, ky, mu, t=1.0, D0=1.0):
    """teeth (ii): even-parity s-wave — DIII 대칭 유지·항상 자명."""
    xi = -2 * t * (np.cos(kx) + np.cos(ky)) - mu
    Dk = D0 * (1j * sy)
    return blk(xi * s0, Dk, Dk.conj().T, -xi * s0)


# 대칭 연산자 (antiunit = U·K)
T_U = blk(1j * sy, Z2, Z2, (1j * sy).conj())     # T²=−1
C_U = blk(Z2, s0, s0, Z2)                        # τx⊗σ0, C²=+1
S = 1j * (T_U @ C_U.conj())                      # chiral = i·T·C (Hermitian, S²=+1)


def _anti(U, M):
    return U @ M.conj() @ np.linalg.inv(U)


# ── path A: 닫힌형 mass-sign ──
TRIMS = [(0.0, 0.0), (np.pi, 0.0), (0.0, np.pi), (np.pi, np.pi)]


def nu_closed(mu, t=1.0):
    """(−1)^ν = ∏_TRIM sign(ξ) (odd-parity 전제). μ=0·|μ|=4t 는 gapless 경계."""
    p = 1.0
    for kx, ky in TRIMS:
        p *= np.sign(-2 * t * (np.cos(kx) + np.cos(ky)) - mu)
    return 1 if p < 0 else 0


# ── path B: T-adapted chiral 기저 + 라인 Pfaffian ──
_w, _v = np.linalg.eigh(S)
_Vp = _v[:, _w > 0.5]
_Vm = T_U @ _Vp.conj()                           # S=−1 고유공간


def _qmat(H4):
    return _Vp.conj().T @ H4 @ _Vm


def nu_line(ky, mu, hfun=Hk, N=1000):
    """고정 ky∈{0,π} 라인의 1D DIII ℤ₂ (Pf q(TRIM)/√det, 연속 branch). (ν, q반대칭)."""
    kxs = np.linspace(0, np.pi, N)
    dets = np.array([np.linalg.det(_qmat(hfun(k, ky, mu))) for k in kxs])
    ang = np.unwrap(np.angle(dets))
    sq = np.sqrt(np.abs(dets)) * np.exp(1j * ang / 2)
    q0 = _qmat(hfun(0.0, ky, mu)); qpi = _qmat(hfun(np.pi, ky, mu))
    asym = np.allclose(q0, -q0.T) and np.allclose(qpi, -qpi.T)
    val = (q0[0, 1] / sq[0]) * (qpi[0, 1] / sq[-1])
    return (1 if val.real < 0 else 0), asym


def nu_pfaffian(mu, N=1000, hfun=Hk):
    n0, a0 = nu_line(0.0, mu, hfun, N)
    npi, api = nu_line(np.pi, mu, hfun, N)
    return (n0 + npi) % 2, n0, npi, (a0 and api)


# ── path C: cylinder (open x, periodic ky) ──
def _onsite(ky, mu, t=1.0, D=1.0, hx=0.0):
    xi = -2 * t * np.cos(ky) - mu
    dy = D * np.sin(ky) * blk(Z2, 1j * s0, -1j * s0, Z2)
    zee = blk(hx * sx, Z2, Z2, -hx * sx)
    return xi * TAU_Z + dy + zee


def _hopx(t=1.0, D=1.0):
    txsz = blk(Z2, sz, sz, Z2)
    return -t * TAU_Z + (-D / 2j) * txsz


def H_cyl(L, ky, mu, hx=0.0):
    on = _onsite(ky, mu, hx=hx); Tx = _hopx()
    H = np.zeros((4 * L, 4 * L), dtype=complex)
    for j in range(L):
        H[4 * j:4 * j + 4, 4 * j:4 * j + 4] = on
        if j < L - 1:
            H[4 * (j + 1):4 * (j + 1) + 4, 4 * j:4 * j + 4] = Tx
            H[4 * j:4 * j + 4, 4 * (j + 1):4 * (j + 1) + 4] = Tx.conj().T
    return H


def edge_zero_modes(L, ky, mu, thr=0.05, hx=0.0):
    """(near-zero 개수, 최소 edge 가중치(양끝 4컬럼)) — 없으면 (0, None)."""
    E, V = np.linalg.eigh(H_cyl(L, ky, mu, hx=hx))
    idx = np.where(np.abs(E) < thr)[0]
    if len(idx) == 0:
        return 0, None
    wts = []
    for i in idx:
        p = np.abs(V[:, i]) ** 2
        wts.append(float(p[:16].sum() + p[-16:].sum()))
    return len(idx), min(wts)


def min_gap(mu, hfun=Hk, N=120):
    ks = np.linspace(0, 2 * np.pi, N, endpoint=False)
    return min(float(np.min(np.abs(np.linalg.eigvalsh(hfun(a, b, mu)))))
               for a in ks for b in ks)


def main():
    quick = "--quick" in sys.argv
    R = {}
    L = 24 if quick else 40
    Npf = 400 if quick else 1000
    Ng = 60 if quick else 120

    # 1. 대칭 대수(전부 수치검증)
    ks = np.linspace(-3, 3, 9 if quick else 13)
    R["T_sq_minus1"] = np.allclose(T_U @ T_U.conj(), -np.eye(4))
    R["C_sq_plus1"] = np.allclose(C_U @ C_U.conj(), np.eye(4))
    R["S_hermitian_sq1"] = (np.allclose(S, S.conj().T) and np.allclose(S @ S, np.eye(4)))
    R["TRS_holds"] = all(np.allclose(_anti(T_U, Hk(a, b, 1.3)), Hk(-a, -b, 1.3))
                         for a in ks for b in ks)
    R["PHS_holds"] = all(np.allclose(_anti(C_U, Hk(a, b, 1.3)), -Hk(-a, -b, 1.3))
                         for a in ks for b in ks)
    R["chiral_holds"] = all(np.allclose(S @ Hk(a, b, 1.3) + Hk(a, b, 1.3) @ S, 0)
                            for a in ks for b in ks)
    # Bloch 재구성 == onsite/hop 분해 (cylinder 정합)
    R["bloch_reconstruction"] = all(
        np.allclose(_onsite(b, 1.3) + _hopx() * np.exp(1j * a)
                    + _hopx().conj().T * np.exp(-1j * a), Hk(a, b, 1.3))
        for a in (0.3, 1.1) for b in (0.0, 0.7, np.pi))

    # 2. 위상도 스캔: path A(닫힌형) == path B(라인 Pfaffian 차원환원)
    topo = [-2.0, 2.0, -3.9, 3.9, -0.5, 0.5]
    triv = [5.0, -5.0, 4.5, -4.5]
    scan = topo + triv
    pf = {m: nu_pfaffian(m, N=Npf) for m in scan}
    R["q_antisym_at_trim"] = all(pf[m][3] for m in scan)
    R["pathA_eq_pathB"] = all(nu_closed(m) == pf[m][0] for m in scan)
    R["topo_nu1"] = all(nu_closed(m) == 1 for m in topo)
    R["triv_nu0"] = all(nu_closed(m) == 0 for m in triv)

    # 3. path C: edge Majorana Kramers + ★Dirac 위치 = 비자명 line 추적
    ec = {}
    for m in (-2.0, 2.0, 5.0, -5.0):
        ec[m] = {0.0: edge_zero_modes(L, 0.0, m), np.pi: edge_zero_modes(L, np.pi, m)}
    R["edge_dirac_tracks_line"] = (
        ec[-2.0][0.0][0] == 4 and ec[-2.0][np.pi][0] == 0        # line0=1 → ky*=0
        and ec[2.0][0.0][0] == 0 and ec[2.0][np.pi][0] == 4      # linepi=1 → ky*=π
        and pf[-2.0][1] == 1 and pf[2.0][2] == 1)
    R["trivial_no_edge_modes"] = all(
        ec[m][ky][0] == 0 for m in (5.0, -5.0) for ky in (0.0, np.pi))
    R["edge_localized"] = all(
        w > 0.9 for m in (-2.0, 2.0)
        for _, w in [ec[m][0.0] if m == -2.0 else ec[m][np.pi]] if w is not None)

    # 4. gap: 전이 |μ|=4t·μ=0 닫힘, 상 내부 열림. ★μ=0=짝수 Dirac(Δν=0)
    R["gap_closes_at_transitions"] = (min_gap(4.0, N=Ng) < 0.05
                                      and min_gap(-4.0, N=Ng) < 0.05
                                      and min_gap(0.0, N=Ng) < 0.05)
    R["gap_open_in_phase"] = (min_gap(2.0, N=Ng) > 0.3 and min_gap(5.0, N=Ng) > 0.3)
    R["mu0_even_dirac_nu_unchanged"] = (nu_closed(-0.5) == 1 and nu_closed(0.5) == 1)

    # teeth (i): in-plane Zeeman — TRS 파괴(PHS 유지)·edge Kramers 분열 ≈ hx
    hx = 0.3
    Hh = Hk(0.3, 0.7, -2.0) + blk(hx * sx, Z2, Z2, -hx * sx)
    R["teeth_zeeman_breaks_trs_keeps_phs"] = (
        not np.allclose(_anti(T_U, Hh), Hk(-0.3, -0.7, -2.0)
                        + blk(hx * sx, Z2, Z2, -hx * sx))
        and np.allclose(_anti(C_U, Hh), -(Hk(-0.3, -0.7, -2.0)
                                          + blk(hx * sx, Z2, Z2, -hx * sx))))
    Eh = np.sort(np.abs(np.linalg.eigvalsh(H_cyl(L, 0.0, -2.0, hx=hx))))[:4]
    E0 = np.sort(np.abs(np.linalg.eigvalsh(H_cyl(L, 0.0, -2.0))))[:4]
    R["teeth_zeeman_splits_kramers"] = bool(np.max(E0) < 1e-4
                                            and np.min(Eh) > hx - 0.05)

    # teeth (ii): s-wave 스코프 — DIII 대칭 유지·sign 공식 오적용 ν=1 vs Pfaffian/edge trivial
    mu_s = 2.0
    R["teeth_swave_diii_symmetric"] = (
        np.allclose(_anti(T_U, Hk_swave(0.3, 0.7, mu_s)), Hk_swave(-0.3, -0.7, mu_s))
        and np.allclose(_anti(C_U, Hk_swave(0.3, 0.7, mu_s)), -Hk_swave(-0.3, -0.7, mu_s)))
    nu_s, _, _, asym_s = nu_pfaffian(mu_s, N=Npf, hfun=Hk_swave)
    R["teeth_swave_scope"] = (nu_closed(mu_s) == 1      # 공식 오적용 시 위상 주장
                              and nu_s == 0 and asym_s)  # Pfaffian 은 자명(odd-parity 전제 노출)

    ok = bool(all(R.values()))
    res = {
        "ok": ok,
        "deterministic": True,
        "axis": "AZ class DIII — 2D 시간역전 초전도체 ℤ₂ (helical Majorana edge), "
                "report14 P4a (1D DIII 차원 상승)",
        "model": ("H(k)=ξ_k τzσ0 + (d·σ)(iσy) Nambu, d=Δ(sin kx, sin ky, 0) ; "
                  "T=τ0⊗iσy K (T²=−1), C=τx⊗σ0 K (C²=+1), S=i·T·C"),
        "invariant": {
            "path_A_closed_form": "(−1)^ν = ∏_{4 TRIM} sign(ξ) (odd-parity) ; 0<|μ|<4t ⟺ ν=1",
            "path_B_pfaffian": "ν = ν₁D(ky=0) ⊕ ν₁D(ky=π) — TRS 라인 차원환원, 1D 기계 재사용",
            "path_C_edge": "cylinder ED — near-zero 4(Kramers 쌍/edge)·★Dirac 위치=비자명 line",
            "phase_scan": {str(m): {"nu_closed": nu_closed(m), "nu_pf": pf[m][0],
                                    "lines": [pf[m][1], pf[m][2]]} for m in scan},
            "edge_scan": {str(m): {"ky0": list(ec[m][0.0]), "kypi": list(ec[m][np.pi])}
                          for m in ec},
        },
        "checks": R,
        "honest_boundary": (
            "관측(위상불변량 산출) — 회로 봉인 아님. 불변량=정수 부호(닫힌형·Pfaffian) — "
            "★float Chern/Berry 적분 미사용. spectrum 연속체=관측·cylinder 유한크기=국소증거"
            "(분류정리 무주장)·free-fermion BdG 한정·d-vector/T/C 규약 고정. "
            "s-wave teeth = 닫힌형의 odd-parity 전제 스코프 노출. 신규 module 0·root 불변 sidecar."),
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"_schema": "class-diii-2d-observe-v1",
                   "_note": "2D class-DIII TR 초전도체 ℤ₂: mass-sign 닫힌형 == 라인 Pfaffian "
                            "차원환원 == edge Majorana Kramers(Dirac 위치가 line 추적)·"
                            "Zeeman/s-wave teeth. 관측·신규 module 0·root 불변.",
                   "observation": res}, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")

    if not quick:
        print("2D 시간역전 초전도체 class-DIII ℤ₂ 관측 (1D DIII 차원 상승, witness — seal 아님):",
              flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  위상도(ν): " + " · ".join(f"μ={m:g}→{nu_closed(m)}" for m in scan), flush=True)
        print("  ★edge Dirac 위치: μ=−2→ky*=0 · μ=+2→ky*=π (비자명 1D line 추적 = 모멘텀 분해 "
              "bulk-boundary)", flush=True)
        print("  ★teeth: in-plane Zeeman=Kramers 분열(class D 강등)·s-wave=닫힌형 odd-parity "
              "전제 노출", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"class_diii_2d_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
