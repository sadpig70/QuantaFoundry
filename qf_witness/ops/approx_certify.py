#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""approx_certify — ε-bounded 근사 인증 티어 (TrackIU IU_B, DESIGN-IntegratedUpgrade).

registry 는 exact-only 다: Trotter/Suzuki 앱은 "그 회로의 unitary" 를 exact 봉인했을 뿐,
목표 e^{-iHt} 와의 오차는 어떤 인증도 없다. 이 스크립트는 그 오차의 **수학적 상한 ε** 을
부동소수 산출 없이(sympy symbolic exact) 인증하고, 직교 sidecar 에 기록한다.

방법 (b) analytic-commutator — 전부 float-free:
  1차 Lie-Trotter :  ‖Π_j e^{-iH_j t} − e^{-iHt}‖ ≤ (t²/2)·Σ_{j<k} ‖[H_j,H_k]‖Δ
  2차 Suzuki (S₂) :  ‖e^{-iA t/2}e^{-iB t}e^{-iA t/2} − e^{-iHt}‖
                       ≤ (t³/12)‖[B,[B,A]]‖Δ + (t³/24)‖[A,[A,B]]‖Δ   (CSTWZ 2021)
  4차 Yoshida     :  S₂(pt)²·S₂(qt)·S₂(pt)² — 삼각부등식으로 Σᵢ ε_S₂(|τᵢ|) 상한
                       (4차 tightness 무주장 — 유효한 upper bound 만)
  합성 전파        :  ‖U₂U₁ − V₂V₁‖ ≤ Σ‖Uᵢ−Vᵢ‖ (유니터리 준가법) → step^k 앱 ε = k·ε_step
  ‖·‖Δ = Pauli 전개 |계수| 합(삼각 상한) ≥ 실제 op-norm — 순수 유리수/π-닫힌형 산술.

계약 E1–E5 (E1–E4=C1–C4 대응; ★E5=TrackHE15 P6a):
  E1  target spec 정준화 + hash (유리수 계수 · π-닫힌형 t 만 허용)
  E2  ε_upper 는 sympy exact symbolic (float 단독 산출 금지; float 표시는 병기 표기)
  E3  감사추적: 방법·교환자 Pauli 전개·산술 종류 기록
  E4  negative control: 교란 spec(t→2t)에서 bound 위반 실검출
  ★E5  ε **하계**(rigorous interval [ε_lo,ε_hi]): mpmath Taylor expm(dps=60·K=140·나머지<1e-100)로
       U(회로곱)·R(=e^{-iHt}) 재계산 → 열노름 하계 max_j‖(U−R)e_j‖ ≤ ‖U−R‖₂. ε_lo>1e-9 ⟹
       **"이 Trotter step 은 exact 가 아니다" 최초 인증**(heis2 ε_lo≈1e-61=exact). E1–E4 는 상한뿐이었다.
       ★제11 검증경로 아님(자가강등)·하계≠합성 최적성(TcountLowerBound 와 구분).

독립 witness (관측·float): dense 실측 d_op = ‖U_seal − e^{-iHt}‖₂ ≤ ε 확인 (소형 8×8/16×16).
  witness 는 관측이며 인증의 주 증거는 symbolic 상한 — seal ≠ run ≠ verify 상속.

정직 경계: ε 는 **상한**이지 실제 오차가 아님(tightness 무주장). 유니터리 채널 한정.
비파괴: registry/APPROX-GUARANTEES.json (직교축 sidecar) 만 생성 — root/oracle/frozen 무영향.

사용:
  python -m qf_witness.ops.approx_certify            # 카탈로그 전체 인증
  python -m qf_witness.ops.approx_certify --quick    # reproduce_all 용 경량 재검증
"""
import os
import re
import sys
import json
import hashlib
import numpy as np
import sympy as sp
import mpmath as mp

from qf_witness.core.paths import ROOT
SPECS_APPS = os.path.join(ROOT, "specs", "apps")
OUT = os.path.join(ROOT, "registry", "APPROX-GUARANTEES.json")

PI = sp.pi
HALF = sp.Rational(1, 2)

# ── E5 계약(TrackHE15 P6a): ε 하계 인증 — rigorous interval [ε_lo, ε_hi] ────
# 기존 E1–E4 는 전부 ε **상한**만: "이 Trotter step 은 exact 가 아니다" 를 증명할 하계가 없다.
# E5 = mpmath Taylor expm(고정밀·rigorous 나머지 한계)으로 U(회로곱)·R(=e^{-iHt}) 재계산 →
#   열노름 하계 ‖(U−R)e_j‖ ≤ ‖U−R‖₂ 로 ε_lo. ε_lo>0 ⟹ **비-exact 최초 인증**(heis2 는 ε_lo≈0).
# ★제11 검증경로 아님(agent03 자가강등 승계). ★하계≠합성 최적성 하한(TcountLowerBound 와 구분).
_MP_DPS = 60
_MP_TAYLOR_K = 140          # (‖H‖t≲2) → 나머지 (‖H‖t)^{K+1}/(K+1)!·e^{‖H‖t} ≪ 1e-100 (rigorous)
_E5_NONEXACT_THRESHOLD = mp.mpf("1e-9")   # ε_lo > 이 값 ⟹ 확실히 비-exact(나머지·반올림 ≪)


# ── Pauli 문자열 대수 (sympy 계수 exact) ───────────────────────────────────
_MUL = {  # (a,b) → (phase, c): a·b = phase·c  (1큐빗)
    ("I", "I"): (1, "I"), ("I", "X"): (1, "X"), ("I", "Y"): (1, "Y"), ("I", "Z"): (1, "Z"),
    ("X", "I"): (1, "X"), ("Y", "I"): (1, "Y"), ("Z", "I"): (1, "Z"),
    ("X", "X"): (1, "I"), ("Y", "Y"): (1, "I"), ("Z", "Z"): (1, "I"),
    ("X", "Y"): (sp.I, "Z"), ("Y", "X"): (-sp.I, "Z"),
    ("Y", "Z"): (sp.I, "X"), ("Z", "Y"): (-sp.I, "X"),
    ("Z", "X"): (sp.I, "Y"), ("X", "Z"): (-sp.I, "Y"),
}


def p_mul(s1, s2):
    """두 Pauli 문자열 곱 → (phase, string)."""
    phase, out = sp.Integer(1), []
    for a, b in zip(s1, s2):
        ph, c = _MUL[(a, b)]
        phase *= ph
        out.append(c)
    return phase, "".join(out)


def commutator(A, B):
    """[A,B] — A,B: dict{pauli_string: sympy coeff} → 같은 형식."""
    out = {}
    for sa, ca in A.items():
        for sb, cb in B.items():
            ph1, s1 = p_mul(sa, sb)
            ph2, s2 = p_mul(sb, sa)
            out[s1] = sp.simplify(out.get(s1, 0) + ca * cb * ph1)
            out[s2] = sp.simplify(out.get(s2, 0) - ca * cb * ph2)
    return {s: c for s, c in out.items() if c != 0}


def triangle_norm(A):
    """‖A‖Δ = Σ|coeff| (Pauli 문자열 op-norm = 1, 삼각부등식 상한) — exact."""
    return sp.simplify(sum(sp.Abs(c) for c in A.values())) if A else sp.Integer(0)


def h_sum(*hs):
    out = {}
    for h in hs:
        for s, c in h.items():
            out[s] = sp.simplify(out.get(s, 0) + c)
    return {s: c for s, c in out.items() if c != 0}


# ── 상한 공식 ──────────────────────────────────────────────────────────────
def eps_trotter1(terms, t):
    """1차: (t²/2)·Σ_{j<k}‖[H_j,H_k]‖Δ. terms = [dict, ...] (곱 순서 무관 상한)."""
    total = sp.Integer(0)
    for j in range(len(terms)):
        for k in range(j + 1, len(terms)):
            total += triangle_norm(commutator(terms[j], terms[k]))
    return sp.simplify(t**2 * HALF * total)


def eps_suzuki2(H_A, H_B, t):
    """2차 S₂(t)=e^{-iA t/2}e^{-iB t}e^{-iA t/2}: (|t|³/12)‖[B,[B,A]]‖Δ + (|t|³/24)‖[A,[A,B]]‖Δ."""
    c1 = triangle_norm(commutator(H_B, commutator(H_B, H_A)))
    c2 = triangle_norm(commutator(H_A, commutator(H_A, H_B)))
    return sp.simplify(sp.Abs(t)**3 * (c1 / 12 + c2 / 24))


# ── 대상 카탈로그 (E1 target spec — 유리수 계수 · π-닫힌형 t) ─────────────────
def _tfim_terms(n):
    """TFIM chain: H = −Σ Z_iZ_{i+1} − Σ X_i (J=h=1). 항별 dict 목록."""
    terms = []
    for i in range(n - 1):
        s = ["I"] * n
        s[i], s[i + 1] = "Z", "Z"
        terms.append({"".join(s): sp.Integer(-1)})
    for i in range(n):
        s = ["I"] * n
        s[i] = "X"
        terms.append({"".join(s): sp.Integer(-1)})
    return terms


def _tfim_split(n):
    """S₂ 용 A/B 그룹: A = ZZ 그룹, B = X 그룹."""
    terms = _tfim_terms(n)
    return h_sum(*terms[:n - 1]), h_sum(*terms[n - 1:])


def _heis_terms(n):
    """Heisenberg chain: H = −Σ_bond (XX+YY+ZZ) (golden e^{+iθP} 관례 → 계수 −1). 항=본드별 P."""
    terms = []
    for i in range(n - 1):
        for P in ("X", "Y", "Z"):
            s = ["I"] * n
            s[i], s[i + 1] = P, P
            terms.append({"".join(s): sp.Integer(-1)})
    return terms


T8 = PI / 8   # 전 카탈로그 공통 dt (spec 헤더 실측)

CATALOG = {
    # ── 1차 Lie-Trotter ──
    "tfim3_trotter_step":  dict(order=1, n=3, terms=lambda: _tfim_terms(3), t=T8,
                                target="H = -sum ZZ(chain) - sum X; J=h=1; t=pi/8"),
    "tfim4_trotter_step":  dict(order=1, n=4, terms=lambda: _tfim_terms(4), t=T8,
                                target="H = -sum ZZ(chain) - sum X; J=h=1; t=pi/8"),
    "heis2_trotter_step":  dict(order=1, n=2, terms=lambda: _heis_terms(2), t=T8,
                                target="H = -(XX+YY+ZZ) single bond; t=pi/8"),
    "heis3_trotter_step":  dict(order=1, n=3, terms=lambda: _heis_terms(3), t=T8,
                                target="H = -sum_bond (XX+YY+ZZ) chain(0,1),(1,2); t=pi/8"),
    # ── 2차 Suzuki S₂ ──
    "tfim3_trotter_step2": dict(order=2, n=3, split=lambda: _tfim_split(3), t=T8,
                                target="H = -sum ZZ - sum X; J=h=1; t=pi/8 (S2 symmetric)"),
    "tfim4_trotter_step2": dict(order=2, n=4, split=lambda: _tfim_split(4), t=T8,
                                target="H = -sum ZZ - sum X; J=h=1; t=pi/8 (S2 symmetric)"),
    # ── 합성 전파 (준가법): step ×2 → ε = 2·ε_step, 목표 e^{-iH·2t} ──
    "tfim3_trotter_2steps": dict(order="compose", n=3, base="tfim3_trotter_step", k=2,
                                 terms=lambda: _tfim_terms(3), t=T8,
                                 target="H = -sum ZZ - sum X; J=h=1; t=2*(pi/8) (step^2)"),
    # ── 4차 Yoshida (S₂ 삼각 분해 상한 — 4차 tightness 무주장) ──
    "tfim3_suzuki4_step":  dict(order=4, n=3, split=lambda: _tfim_split(3), t=T8,
                                target="H = -sum ZZ - sum X; J=h=1; t=pi/8 (Yoshida S2^5)"),
    "tfim4_suzuki4_step":  dict(order=4, n=4, split=lambda: _tfim_split(4), t=T8,
                                target="H = -sum ZZ - sum X; J=h=1; t=pi/8 (Yoshida S2^5)"),
}


# ── gridsynth Clifford+T 가족 (TrackHE14 P6a — Trotter 밖 2번째 ε-가족) ────
# 시퀀스·ring shadow 단일출처 = gridsynth_family (봉인 앱과 인증의 바인딩).
from qf_witness.family.gridsynth_family import (  # noqa: E402
    ALL_SEQS as GRID_SEQS, ring_shadow, w_mul)


def _w_conj(x):
    """ℤ[ω] 켤레: ω̄=−ω³ → conj(a,b,c,d)=(a,−d,−c,−b)."""
    return (x[0], -x[3], -x[2], -x[1])


def _w_sym(x):
    """ℤ[ω] 4-튜플 → sympy exact (ω=e^{iπ/4})."""
    om = sp.exp(sp.I * PI / 4)
    return x[0] + x[1] * om + x[2] * om ** 2 + x[3] * om ** 3


def certify_gridsynth(app_id):
    """ε = √(2−|tr(U†R)|) = min_φ‖e^{iφ}U−R_z‖₂ (2×2 유니터리 등식 — 위상정렬 op-norm).
    sympy exact — |tr|² 는 ℤ[ω] ring shadow 로 정수 축약 후 소형 잔여식만 simplify
    (U=M/√2^m: tr(U†R)=z/√2^m, z=w̄₀e^{−iθ/2}+w̄₁e^{iθ/2}, |z|²=A+2Re(B·e^{−iθ}),
     A=|w₀|²+|w₁|²·B=w₀conj(w₁) ∈ ℤ[ω] — 전부 정수산술).
    ★시퀀스 합성 tightness 무주장(Ross-Selinger 최적 아님 — 존재 구성)."""
    k, seq = GRID_SEQS[app_id]
    theta = PI / 2 ** k
    M, m = ring_shadow(seq)
    w0 = _w_conj(M[0][0])                     # conj(M00)
    w1 = _w_conj(M[1][1])                     # conj(M11)
    A = tuple(p + q for p, q in
              zip(w_mul(w0, _w_conj(w0)), w_mul(w1, _w_conj(w1))))
    B = w_mul(w0, _w_conj(w1))
    As, Bs = _w_sym(A), _w_sym(B)
    z2 = As + Bs * sp.exp(-sp.I * theta) + sp.conjugate(Bs) * sp.exp(sp.I * theta)
    tr2 = sp.simplify(sp.expand_complex(z2)) / 2 ** m             # |tr(U†R)|² exact
    eps = sp.sqrt(2 - sp.sqrt(tr2))
    eps_f = float(sp.N(eps, 40))          # 2−√tr2 상쇄 대비 고정밀 평가 (표시용)

    # 독립 witness (관측·float): 봉인 spec golden == 시퀀스 float 곱, 거리 재계산 일치
    U_seal = app_golden(app_id)
    Hf = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    Tf = np.diag([1, np.exp(1j * np.pi / 4)]).astype(complex)
    Uf = np.eye(2, dtype=complex)
    for g in seq:
        Uf = (Hf if g == "H" else Tf) @ Uf
    Rf = np.diag([np.exp(-1j * np.pi / 2 ** (k + 1)), np.exp(1j * np.pi / 2 ** (k + 1))])
    d_obs = float(np.sqrt(max(0.0, 2 - abs(np.trace(Uf.conj().T @ Rf)))))
    _tol = 1e-9 + 1e-3 * eps_f          # float64 2−|tr| 상쇄오차 대비 (주 증거=symbolic)
    witness_ok = (op_norm(U_seal - Uf) < 1e-12 and abs(d_obs - eps_f) < _tol)

    # E4 teeth: 시퀀스 변조(마지막 게이트 제거) → ε 상이 검출 (certificate 는 시퀀스에 바인딩)
    Up = np.eye(2, dtype=complex)
    for g in seq[:-1]:
        Up = (Hf if g == "H" else Tf) @ Up
    d_pert = float(np.sqrt(max(0.0, 2 - abs(np.trace(Up.conj().T @ Rf)))))
    teeth_ok = abs(d_pert - eps_f) > 1e-6

    spec_str = f"R_z(pi/{2 ** k}) target; Clifford+T sequence len={len(seq)} T-count={seq.count('T')}"
    return {
        "id": app_id,
        "kind": "gate_synthesis_clifford_t",
        "target_spec": spec_str,
        "spec_hash": hashlib.sha256((spec_str + seq).encode()).hexdigest()[:16],
        "sequence": seq,
        "epsilon_upper_symbolic": str(eps),
        "epsilon_upper_float_display": eps_f,
        # ★E5: gridsynth metric 은 위상정렬 op-norm **등식**(exact) → 하계=상한, 구간 degenerate
        "epsilon_lower_rigorous_float": eps_f,
        "epsilon_interval_float": [eps_f, eps_f],
        "nonexact_certified": bool(eps_f > 1e-9),       # 합성 회로 ≠ 목표(당연) — exact 등식 기반
        "e5_audit": ("phase-aligned metric is EXACT equality (sqrt(2-|tr|)) → lower=upper=symbolic; "
                     "interval degenerate. NOT synthesis optimality (cf TcountLowerBound)."),
        "e5_interval_valid": True,
        "metric": ("phase-aligned op_norm: min_phi ||e^{i phi} U - R_z||_2 = sqrt(2-|tr(U^dag R)|) "
                   "(equality for 2x2 unitaries; synthesis tightness NOT claimed — existence construction)"),
        "diamond_upper_note": "<= 2*epsilon for the unitary channel pair",
        "audit": {"arith": "sympy_exact_symbolic (zeta8-algebraic entries; no float in bound)",
                  "method": "exact_trace_distance_on_PSU2 (|tr|^2 via expand_complex, exact radical)"},
        "witness": {"kind": "sealed-golden == sequence product (float, <1e-12) + d_obs recompute",
                    "d_obs": d_obs, "d_obs_eq_eps": bool(abs(d_obs - eps_f) < _tol)},
        "negative_control": {"perturbation": "sequence tamper (drop final gate)",
                             "bound_violated_detected": bool(teeth_ok)},
        "exact_trotter": False,
        "certified": bool(witness_ok and teeth_ok),
    }


# ── dense witness (관측·float — 주 증거 아님) ──────────────────────────────
_P1 = {"I": np.eye(2, dtype=complex),
       "X": np.array([[0, 1], [1, 0]], dtype=complex),
       "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
       "Z": np.diag([1, -1]).astype(complex)}


def dense_H(terms_or_sum, n):
    H = np.zeros((1 << n, 1 << n), dtype=complex)
    items = []
    if isinstance(terms_or_sum, list):
        for t_ in terms_or_sum:
            items += list(t_.items())
    else:
        items = list(terms_or_sum.items())
    for s, c in items:
        M = np.array([[1.0]], dtype=complex)
        for ch in s:
            M = np.kron(M, _P1[ch])
        H += float(c) * M
    return H


def expm_iHt(H, t_float):
    lam, V = np.linalg.eigh(H)
    return (V * np.exp(-1j * lam * t_float)) @ V.conj().T


# ── E5 하계: mpmath Taylor expm (rigorous) + 열노름 하계 ────────────────────
def _mp_matrix(Hnp):
    n = Hnp.shape[0]
    M = mp.zeros(n)
    for i in range(n):
        for j in range(n):
            M[i, j] = mp.mpc(Hnp[i, j].real, Hnp[i, j].imag)
    return M


def _mp_expm_iHt(Hmp, t):
    """e^{-iHt} = Σ_k (-iHt)^k/k! — Taylor(mpmath, dps=%d, K=%d). 나머지 rigorous 소멸.
    H Hermitian·‖H‖t≲2 → K=140 나머지 ≪ 1e-100.""" % (_MP_DPS, _MP_TAYLOR_K)
    n = Hmp.rows
    x = mp.mpc(0, -1) * t
    term = mp.eye(n)
    acc = mp.eye(n)
    for k in range(1, _MP_TAYLOR_K + 1):
        term = (term * Hmp) * (x / k)
        acc += term
    return acc


def _mp_expm_terms(terms_list, t, n):
    """1차 Trotter U = Π_j e^{-iH_j t} (terms 순서, mpmath)."""
    U = mp.eye(1 << n)
    for tm in terms_list:
        U = _mp_expm_iHt(_mp_matrix(dense_H(tm, n)), t) * U
    return U


def _mp_s2(A_mp, B_mp, s, n):
    """2차 Suzuki S₂(s) = e^{-iA s/2} e^{-iB s} e^{-iA s/2}."""
    eA = _mp_expm_iHt(A_mp, s / 2)
    eB = _mp_expm_iHt(B_mp, s)
    return eA * eB * eA


def _col_norm_lower(U, R):
    """max_j ‖(U−R)e_j‖₂ ≤ ‖U−R‖₂ — rigorous 하계(mpmath)."""
    n = U.rows
    best = mp.mpf(0)
    for j in range(n):
        s = mp.mpf(0)
        for i in range(n):
            d = U[i, j] - R[i, j]
            s += mp.re(d) ** 2 + mp.im(d) ** 2
        c = mp.sqrt(s)
        if c > best:
            best = c
    return best


def epsilon_lower_trotter(c, t, t_target, n):
    """E5: Trotter/Suzuki step 의 rigorous ε 하계. U 회로곱·R=e^{-iH_full t_target} 재계산."""
    order = c["order"]
    if order == 1:
        terms = c["terms"]()
        U = _mp_expm_terms(terms, t, n)
        Hf = h_sum(*terms)
    elif order == 2:
        A, B = c["split"]()
        Amp, Bmp = _mp_matrix(dense_H(A, n)), _mp_matrix(dense_H(B, n))
        U = _mp_s2(Amp, Bmp, t, n)
        Hf = h_sum(A, B)
    elif order == 4:
        A, B = c["split"]()
        Amp, Bmp = _mp_matrix(dense_H(A, n)), _mp_matrix(dense_H(B, n))
        pf = mp.mpf(1) / (4 - mp.cbrt(4))
        qf = 1 - 4 * pf
        U = mp.eye(1 << n)
        for tau in (pf, pf, qf, pf, pf):        # Yoshida τ=[p,p,q,p,p]
            U = _mp_s2(Amp, Bmp, tau * t, n) * U
        Hf = h_sum(A, B)
    elif order == "compose":
        base = CATALOG[c["base"]]
        terms = c["terms"]()
        Ustep = _mp_expm_terms(base["terms"](), t, n)
        U = Ustep ** c["k"]
        Hf = h_sum(*terms)
    else:
        raise ValueError(order)
    R = _mp_expm_iHt(_mp_matrix(dense_H(Hf, n)), t_target)
    return _col_norm_lower(U, R)


def app_golden(app_id):
    """spec 의 app_golden 블록 exec → U_seal (Tier-0 봉인이 composite==golden 확정한 회로 unitary)."""
    txt = open(os.path.join(SPECS_APPS, f"{app_id}.app.pg"), encoding="utf-8").read()
    m = re.search(r"```python id=app_golden\s*\n(.*?)\n```", txt, re.S)
    ns = {}
    exec(m.group(1), ns)  # noqa: S102 — tracked spec, 봉인 시 검증된 소스
    return np.asarray(ns["golden"], dtype=complex)


def op_norm(M):
    return float(np.linalg.norm(M, 2))


# ── 인증 ──────────────────────────────────────────────────────────────────
def certify(app_id):
    c = CATALOG[app_id]
    n, t = c["n"], c["t"]
    audit = {"arith": "sympy_exact_symbolic (pi-closed form; no float in bound)"}

    if c["order"] == 1:
        terms = c["terms"]()
        eps = eps_trotter1(terms, t)
        H_full = h_sum(*terms)
        t_target = t
        audit["method"] = "analytic_commutator_first_order (t^2/2 * sum_{j<k} ||[Hj,Hk]||_tri)"
    elif c["order"] == 2:
        H_A, H_B = c["split"]()
        eps = eps_suzuki2(H_A, H_B, t)
        H_full = h_sum(H_A, H_B)
        t_target = t
        audit["method"] = "analytic_nested_commutator_suzuki2 (CSTWZ 2021: t^3/12·||[B,[B,A]]|| + t^3/24·||[A,[A,B]]||)"
    elif c["order"] == 4:
        H_A, H_B = c["split"]()
        p = 1 / (4 - sp.cbrt(4))
        q = 1 - 4 * p
        eps = sp.simplify(4 * eps_suzuki2(H_A, H_B, p * t) + eps_suzuki2(H_A, H_B, q * t))
        H_full = h_sum(H_A, H_B)
        t_target = t
        audit["method"] = ("triangle_decomposition_of_yoshida (sum_i eps_S2(|tau_i|), tau=[p,p,q,p,p]*t, "
                           "p=1/(4-4^(1/3)); valid upper bound, 4th-order tightness NOT claimed)")
    elif c["order"] == "compose":
        base = certify(c["base"])
        eps = sp.simplify(c["k"] * sp.sympify(base["epsilon_upper_symbolic"]))
        H_full = h_sum(*c["terms"]())
        t_target = c["k"] * t
        audit["method"] = f"subadditive_composition (||U^k - V^k|| <= k·||U-V||; base={c['base']})"
    else:
        raise ValueError(c["order"])

    eps_f = float(eps)

    # 독립 witness (관측): dense 실측 ≤ ε
    U_seal = app_golden(app_id)
    Hd = dense_H(H_full, n)
    U_exact = expm_iHt(Hd, float(t_target))
    d_obs = op_norm(U_seal - U_exact)
    witness_ok = d_obs <= eps_f + 1e-12

    # E4 teeth: 교란 target (t→2t, 필요시 4t) 에서 bound 위반이 실제로 검출돼야
    teeth_mul, teeth_ok = None, False
    for mul in (2, 4, 8):
        d_pert = op_norm(U_seal - expm_iHt(Hd, float(t_target) * mul))
        if d_pert > eps_f:
            teeth_mul, teeth_ok = mul, True
            break

    # ── E5: rigorous ε 하계 (mpmath Taylor expm) ──  t=π/8 를 mpmath 고정밀로
    with mp.workdps(_MP_DPS):
        t_mp = mp.pi / 8
        t_target_mp = (c["k"] * t_mp) if c["order"] == "compose" else t_mp
        eps_lo = epsilon_lower_trotter(c, t_mp, t_target_mp, n)
    eps_lo_f = float(eps_lo)
    nonexact = bool(eps_lo > _E5_NONEXACT_THRESHOLD)
    # E5 정합: 하계 ≤ 상한 (구간 유효성) · d_obs 관측이 구간 안
    e5_interval_valid = bool(eps_lo <= mp.mpf(eps_f) + mp.mpf("1e-30"))
    e5_dobs_in_interval = bool(eps_lo_f - 1e-9 <= d_obs <= eps_f + 1e-9)

    spec_str = c["target"]
    return {
        "id": app_id,
        "kind": "hamiltonian_evolution",
        "target_spec": spec_str,
        "spec_hash": hashlib.sha256(spec_str.encode()).hexdigest()[:16],
        "trotter_order": c["order"],
        "epsilon_upper_symbolic": str(eps),
        "epsilon_upper_float_display": eps_f,          # 표시용 병기 (E2: 주 산출은 symbolic)
        "epsilon_lower_rigorous_float": eps_lo_f,       # ★E5 (주 산출은 mpmath 고정밀)
        "epsilon_interval_float": [eps_lo_f, eps_f],
        "nonexact_certified": nonexact,                # ★ε_lo>1e-9 ⟹ exact 아님 rigorous
        "metric": "op_norm (no phase alignment needed: golden is the literal circuit product)",
        "diamond_upper_note": "<= 2*epsilon for the unitary channel pair",
        "audit": audit,
        "e5_audit": ("column-norm lower bound max_j ||(U-R)e_j||_2 <= ||U-R||_2 ; "
                     "U(circuit product) & R=e^{-iHt} via mpmath Taylor expm (dps=%d, K=%d, "
                     "remainder<1e-100 rigorous). NOT an 11th verification path; "
                     "lower bound != synthesis optimality (cf TcountLowerBound)." % (_MP_DPS, _MP_TAYLOR_K)),
        "witness": {
            "kind": "dense_exact_diagonalization (observation, float)",
            "d_obs": d_obs,
            "d_obs_le_eps": bool(witness_ok),
            "d_obs_in_e5_interval": e5_dobs_in_interval,
        },
        "negative_control": {
            "perturbation": f"target t -> {teeth_mul}*t" if teeth_ok else "not detected up to 8t",
            "bound_violated_detected": bool(teeth_ok),
        },
        "exact_trotter": bool(eps == 0),
        "e5_interval_valid": e5_interval_valid,
        "certified": bool(witness_ok and teeth_ok and e5_interval_valid and e5_dobs_in_interval),
    }


def _write(certs):
    payload = {
        "_schema": "approx-guarantee-v1",
        "_note": ("ε-bounded 근사 인증 sidecar (TrackIU IU_B). 직교축 — 기존 tier/seal/root 불변. "
                  "ε 는 목표 e^{-iHt} 대비 op-norm 오차 — E1–E4=**상한**(sympy symbolic exact) + "
                  "★E5=**하계**(rigorous interval [ε_lo,ε_hi]): mpmath Taylor expm(dps=60,K=140,"
                  "나머지<1e-100)로 U·R 재계산→열노름 하계. ε_lo>1e-9 ⟹ **비-exact 최초 인증**"
                  "(heis2 ε_lo≈0=exact). ★제11 검증경로 아님·하계≠합성 최적성. "
                  "봉인 앱 자체는 여전히 '그 회로의 unitary' exact — 이 파일은 목표 대비 근사 품질만 인증."),
        "certificates": certs,
    }
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def quick_recheck():
    """reproduce_all 용: sidecar 존재 + 대표 2종(heis2 exact / tfim3 1차) 재인증 일치."""
    if not os.path.exists(OUT):
        return False
    saved = json.load(open(OUT, encoding="utf-8"))["certificates"]
    for app_id in ("heis2_trotter_step", "tfim3_trotter_step"):
        r = certify(app_id)
        s = saved.get(app_id)
        if not (s and r["certified"] and
                r["epsilon_upper_symbolic"] == s["epsilon_upper_symbolic"]):
            return False
        # ★E5: heis2=exact(하계≈0)·tfim3=비-exact(하계>0) rigorous 재확인
        if r["nonexact_certified"] != s.get("nonexact_certified"):
            return False
    # E5 계약 실증: heis2 exact(nonexact=False) · tfim3 nonexact 인증
    if saved["heis2_trotter_step"].get("nonexact_certified") is not False:
        return False
    if saved["tfim3_trotter_step"].get("nonexact_certified") is not True:
        return False
    # gridsynth 대표 2종 (2번째 ε-가족: 존재구성 _ct + RS 심화 _rs)
    for rep in ("rz_pi64_ct", "rz_pi64_rs"):
        rg = certify_gridsynth(rep)
        sg = saved.get(rep)
        if not (sg and rg["certified"] and
                rg["epsilon_upper_symbolic"] == sg["epsilon_upper_symbolic"]):
            return False
    return bool(saved["heis2_trotter_step"]["exact_trotter"])


def main():
    if "--quick" in sys.argv[1:]:
        ok = quick_recheck()
        print(f"approx_certify quick: {'PASS' if ok else 'FAIL'}")
        sys.exit(0 if ok else 1)
    certs, all_ok = {}, True
    for app_id in CATALOG:
        r = certify(app_id)
        certs[app_id] = r
        flag = "OK " if r["certified"] else "FAIL"
        extra = " (exact: eps=0)" if r["exact_trotter"] else ""
        print(f"[{flag}] {app_id}: eps∈[{r['epsilon_lower_rigorous_float']:.3g}, "
              f"{r['epsilon_upper_float_display']:.4g}] nonexact={r['nonexact_certified']} "
              f"d_obs={r['witness']['d_obs']:.4g} teeth={r['negative_control']['bound_violated_detected']}{extra}")
        all_ok &= r["certified"]
    for app_id in GRID_SEQS:
        r = certify_gridsynth(app_id)
        certs[app_id] = r
        flag = "OK " if r["certified"] else "FAIL"
        print(f"[{flag}] {app_id}: eps~{r['epsilon_upper_float_display']:.4g} "
              f"(exact radical) d_obs={r['witness']['d_obs']:.4g} "
              f"teeth={r['negative_control']['bound_violated_detected']} [gridsynth]")
        all_ok &= r["certified"]
    _write(certs)
    print(f"approx_certify: {'ALL CERTIFIED' if all_ok else 'SOME FAILED'} "
          f"({len(certs)} apps) → {os.path.relpath(OUT, ROOT)}")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
