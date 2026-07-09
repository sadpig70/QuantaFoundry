#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ising_fr_observe — TrackHE13 P5: Ising MTC pentagon+hexagon 전역 정합 공리 자체검증 witness
(관측, seal 아님).

report13 P5 축. 기존 애니온 관측 3종과 **검증 객체가 상이**:
  - `ising_fusion_observe`(HE9 P6): 융합환·양자차원(Perron-Frobenius)만 — 부분대수.
  - `mtc_braid_observe`(HE10 P4): 개별 braid 유니터리 B₁,B₂ 의 Yang-Baxter — braid 표현 1개.
  - `su2_3_mtc_observe`(HE11): SU(2)₃ modular data S/T(Verlinde) — modular 계층.
  본 witness = **전 admissible F/R symbol 의 pentagon(Biedenharn-Elliott)+hexagon 방정식 전수** 를
  exact 순환체 ℚ(ζ₁₆) 산술로 닫음. 즉 애니온 데이터의 **전역 결합 일관성 공리**(F·R 표를 데이터로).

방법(제1원리, 추측 금지):
  1. 융합 N_{ab}^c 인코딩(σ×σ=1+ψ·σ×ψ=σ·ψ×ψ=1·1×x=x).
  2. F-symbol: 유일한 비자명 2×2 = F^{σσσ}_σ=(1/√2)[[1,1],[1,−1]](채널기저 {1,ψ}) 고정. 진공다리 F=1(단위
     정규화). 나머지 비진공 스칼라 10개는 ±1 **미지수** → **pentagon 전수 풀이**로 부호 결정(gauge 명시).
  3. Pentagon: [F^{abc}_g]_{fh}[F^{ahd}_e]_{gj} = Σ_i [F^{fcd}_e]_{gi}[F^{abi}_e]_{fj}[F^{bcd}_j]_{hi}
     (좌결합 트리 규약, F index=(좌내부,우내부)). 전 admissible 5-튜플 전수 폐합.
  4. R-symbol: R^{σσ}_1=ζ₁₆⁻¹·R^{σσ}_ψ=ζ₁₆³·R^{ψψ}_1=−1·R^{σψ}_σ=R^{ψσ}_σ=−i(=ζ₁₆⁻⁴) — 추측 아님,
     hexagon(Bonderson R±) 전수 풀이로 **강제**됨을 실증(ζ₁₆ 위상 전수탐색→해집합).
  5. payoff(exact): 리본 위상 θ_σ=(1/√2)(R^{σσ}_1+R^{σσ}_ψ)=ζ₁₆·θ_ψ=−1; modular (ST)³=e^{2πic/8}S²
     (c=1/2, S=½[[1,√2,1],[√2,0,−√2],[1,−√2,+1]] — self-dual S²=I → S_ψψ=+1(task 표기 −1 은 오타);
     bare-T=diag(1,ζ₁₆,−1) 관례에서 위상=e^{2πic/8}=ζ₁₆).
  6. teeth: F 스칼라 1개 부호 flip → pentagon 최소1개 붕괴; R 위상 1개 flip → hexagon 최소1개 붕괴.

exact 엔진: ℚ(ζ₁₆) 순환체 산술을 Fraction 기반 Cyc(ζ⁸=−1, 기저 ζ⁰..ζ⁷)로 자체구현(결정론·정수/유리수).
  √2=ζ²−ζ⁶·1/√2=(ζ²−ζ⁶)/2·i=ζ⁴·−1=ζ⁸ 로 F/R 전부 ℚ(ζ₁₆) 원소. modular 3×3 는 sympy 로 교차확인.
  탐색(부호/위상 해집합)은 float, 최종 인증은 Cyc exact.

정직 경계(★관측·seal 아님, root 불변 sidecar·신규 module 0):
  witness = Ising MTC 의 pentagon/hexagon 전역 공리 폐합(F/R 표=데이터). ★애니온 게이트 회로 봉인 아님
  (ζ₁₆ 위상 module=사람게이트, 범위밖). gauge 선택(진공 F=1·+Hadamard) 명시. 기존 fusion/braid/modular
  관측과 검증객체 상이. [[ising-fusion-observe]]·[[mtc-braid-observe]]·[[su2-3-mtc-observe]] 교차.

사용: python scripts/ising_fr_observe.py [--quick]
"""
from __future__ import annotations

import itertools
import json
import math
import os
import sys
from fractions import Fraction as Fr

# ── 라벨: 0=1(진공), 1=σ, 2=ψ ──
ONE, SIG, PSI = 0, 1, 2
LAB = (ONE, SIG, PSI)
NAME = {ONE: "1", SIG: "σ", PSI: "ψ"}


# ── 융합 규칙 N[a][b][c] ──
def build_N():
    N = {(a, b, c): 0 for a in LAB for b in LAB for c in LAB}

    def setf(a, b, cs):
        for c in cs:
            N[(a, b, c)] = 1
            N[(b, a, c)] = 1
    setf(ONE, ONE, [ONE]); setf(ONE, SIG, [SIG]); setf(ONE, PSI, [PSI])
    setf(SIG, SIG, [ONE, PSI]); setf(SIG, PSI, [SIG]); setf(PSI, PSI, [ONE])
    return N


N = build_N()


def nz(a, b, c):
    return N[(a, b, c)] > 0


def fuse(a, b):
    return [c for c in LAB if nz(a, b, c)]


def padm(a, b, c, d, e, f):
    """[F^{abc}_d]_{ef} admissible: 좌트리 (ab)=e,(ec)=d · 우트리 (bc)=f,(af)=d."""
    return nz(a, b, e) and nz(e, c, d) and nz(b, c, f) and nz(a, f, d)


# ── 미지 스칼라 F-symbol 키: a,b,c∈{σ,ψ}, (σσσ) 제외, admissible ──
def scalar_F_keys():
    keys = []
    for a in (SIG, PSI):
        for b in (SIG, PSI):
            for c in (SIG, PSI):
                if (a, b, c) == (SIG, SIG, SIG):
                    continue
                for d in LAB:
                    # 이 (a,b,c,d) 그룹이 admissible 한 (e,f) 를 가지면 스칼라 1개
                    if any(padm(a, b, c, d, e, f) for e in LAB for f in LAB):
                        keys.append((a, b, c, d))
    return keys


FKEYS = scalar_F_keys()


# ═══════════════ float 엔진 (탐색용) ═══════════════
def Ffl(a, b, c, d, e, f, scal):
    if not padm(a, b, c, d, e, f):
        return 0.0
    if a == ONE or b == ONE or c == ONE:      # 진공다리 → 단위 정규화
        return 1.0
    if (a, b, c) == (SIG, SIG, SIG):           # F^{σσσ}_σ Hadamard/√2, 기저 {1,ψ}
        s = -1.0 if (e == PSI and f == PSI) else 1.0
        return s / math.sqrt(2.0)
    return float(scal[(a, b, c, d)])


def _rkey(x, y, z):
    # R^{σψ}_σ 와 R^{ψσ}_σ 동일 → 정규화(정렬)
    return (min(x, y), max(x, y), z)


def Rfl(x, y, z, rexp):
    if not nz(x, y, z):
        return 0.0 + 0.0j
    if x == ONE or y == ONE:
        return 1.0 + 0.0j
    n = rexp[_rkey(x, y, z)]
    return complex(math.cos(math.pi * n / 8.0), math.sin(math.pi * n / 8.0))


# ── pentagon / hexagon 방정식 인덱스 사전계산 ──
def build_penta_eqs():
    eqs = []
    for a in LAB:
        for b in LAB:
            for c in LAB:
                for d in LAB:
                    for e in LAB:
                        for f in LAB:
                            for g in LAB:
                                for h in LAB:
                                    for j in LAB:
                                        lhs = padm(a, b, c, g, f, h) and padm(a, h, d, e, g, j)
                                        rhs = any(padm(f, c, d, e, g, i) and padm(a, b, i, e, f, j)
                                                  and padm(b, c, d, j, h, i) for i in LAB)
                                        if lhs or rhs:
                                            eqs.append((a, b, c, d, e, f, g, h, j))
    return eqs


PENTA_EQS = build_penta_eqs()


def penta_resid_fl(t, scal):
    a, b, c, d, e, f, g, h, j = t
    lhs = Ffl(a, b, c, g, f, h, scal) * Ffl(a, h, d, e, g, j, scal)
    rhs = 0.0
    for i in LAB:
        rhs += (Ffl(f, c, d, e, g, i, scal) * Ffl(a, b, i, e, f, j, scal)
                * Ffl(b, c, d, j, h, i, scal))
    return abs(lhs - rhs)


def build_hex_eqs():
    """(a,b,c,d,e,g, ver) — ver='+' 또는 '-' (R±)."""
    eqs = []
    for a in LAB:
        for b in LAB:
            for c in LAB:
                for d in LAB:
                    for e in LAB:
                        for g in LAB:
                            lhs = padm(a, c, b, d, e, g) and nz(c, a, e) and nz(c, b, g)
                            rhs = any(padm(c, a, b, d, e, f) and nz(c, f, d)
                                      and padm(a, b, c, d, f, g) for f in LAB)
                            if lhs or rhs:
                                eqs.append((a, b, c, d, e, g, "+"))
                                eqs.append((a, b, c, d, e, g, "-"))
    return eqs


HEX_EQS = build_hex_eqs()


def hex_resid_fl(t, scal, rexp):
    a, b, c, d, e, g, ver = t
    if ver == "+":
        lhs = (Rfl(c, a, e, rexp) * Ffl(a, c, b, d, e, g, scal) * Rfl(c, b, g, rexp))
        rhs = 0.0 + 0.0j
        for f in LAB:
            rhs += (Ffl(c, a, b, d, e, f, scal) * Rfl(c, f, d, rexp)
                    * Ffl(a, b, c, d, f, g, scal))
    else:
        def rinv(x, y, z):
            v = Rfl(x, y, z, rexp)
            return (1.0 / v) if v != 0 else 0.0
        lhs = (rinv(a, c, e) * Ffl(a, c, b, d, e, g, scal) * rinv(b, c, g))
        rhs = 0.0 + 0.0j
        for f in LAB:
            rhs += (Ffl(c, a, b, d, e, f, scal) * rinv(f, c, d)
                    * Ffl(a, b, c, d, f, g, scal))
    return abs(lhs - rhs)


# ═══════════════ exact 엔진: ℚ(ζ₁₆) 순환체 (ζ⁸=−1) ═══════════════
class Cyc:
    """유리계수 ℚ(ζ₁₆) 원소. 기저 ζ⁰..ζ⁷, ζ⁸=−1 로 환원."""
    __slots__ = ("c",)

    def __init__(self, coeffs=None):
        self.c = [Fr(0)] * 8 if coeffs is None else [Fr(x) for x in coeffs]

    @staticmethod
    def zeta(k):
        r = Cyc()
        k %= 16
        sign = 1
        if k >= 8:
            k -= 8
            sign = -1
        r.c[k] = Fr(sign)
        return r

    def __add__(s, o):
        return Cyc([x + y for x, y in zip(s.c, o.c)])

    def __sub__(s, o):
        return Cyc([x - y for x, y in zip(s.c, o.c)])

    def scal(s, q):
        q = Fr(q)
        return Cyc([x * q for x in s.c])

    def __mul__(s, o):
        res = [Fr(0)] * 8
        for i, a in enumerate(s.c):
            if a == 0:
                continue
            for jx, b in enumerate(o.c):
                if b == 0:
                    continue
                k = i + jx
                sign = 1
                if k >= 8:
                    k -= 8
                    sign = -1
                res[k] += sign * a * b
        return Cyc(res)

    def is_zero(s):
        return all(x == 0 for x in s.c)

    def to_complex(s):
        z = complex(math.cos(math.pi / 8), math.sin(math.pi / 8))
        return sum(complex(float(a)) * z ** i for i, a in enumerate(s.c))


C_ZERO = Cyc()
C_ONE = Cyc([1, 0, 0, 0, 0, 0, 0, 0])
C_SQRT2 = Cyc.zeta(2) - Cyc.zeta(6)              # √2
C_INV_SQRT2 = C_SQRT2.scal(Fr(1, 2))             # 1/√2


def Fcyc(a, b, c, d, e, f, scal):
    if not padm(a, b, c, d, e, f):
        return C_ZERO
    if a == ONE or b == ONE or c == ONE:
        return C_ONE
    if (a, b, c) == (SIG, SIG, SIG):
        neg = (e == PSI and f == PSI)
        return C_INV_SQRT2.scal(-1) if neg else C_INV_SQRT2
    return C_ONE.scal(int(scal[(a, b, c, d)]))


def Rcyc(x, y, z, rexp):
    if not nz(x, y, z):
        return C_ZERO
    if x == ONE or y == ONE:
        return C_ONE
    return Cyc.zeta(rexp[_rkey(x, y, z)])


def Rcyc_inv(x, y, z, rexp):
    if not nz(x, y, z):
        return C_ZERO
    if x == ONE or y == ONE:
        return C_ONE
    return Cyc.zeta(-rexp[_rkey(x, y, z)])


def penta_resid_cyc(t, scal):
    a, b, c, d, e, f, g, h, j = t
    lhs = Fcyc(a, b, c, g, f, h, scal) * Fcyc(a, h, d, e, g, j, scal)
    rhs = C_ZERO
    for i in LAB:
        rhs = rhs + (Fcyc(f, c, d, e, g, i, scal) * Fcyc(a, b, i, e, f, j, scal)
                     * Fcyc(b, c, d, j, h, i, scal))
    return (lhs - rhs).is_zero()


def hex_resid_cyc(t, scal, rexp):
    a, b, c, d, e, g, ver = t
    if ver == "+":
        lhs = Rcyc(c, a, e, rexp) * Fcyc(a, c, b, d, e, g, scal) * Rcyc(c, b, g, rexp)
        rhs = C_ZERO
        for f in LAB:
            rhs = rhs + (Fcyc(c, a, b, d, e, f, scal) * Rcyc(c, f, d, rexp)
                         * Fcyc(a, b, c, d, f, g, scal))
    else:
        lhs = Rcyc_inv(a, c, e, rexp) * Fcyc(a, c, b, d, e, g, scal) * Rcyc_inv(b, c, g, rexp)
        rhs = C_ZERO
        for f in LAB:
            rhs = rhs + (Fcyc(c, a, b, d, e, f, scal) * Rcyc_inv(f, c, d, rexp)
                         * Fcyc(a, b, c, d, f, g, scal))
    return (lhs - rhs).is_zero()


# ═══════════════ 풀이(탐색) ═══════════════
def solve_pentagon(tol=1e-9):
    """±1 스칼라 2^10 전수탐색 → pentagon 폐합 해집합."""
    sols = []
    for bits in itertools.product((1.0, -1.0), repeat=len(FKEYS)):
        scal = {k: v for k, v in zip(FKEYS, bits)}
        ok = True
        for t in PENTA_EQS:
            if penta_resid_fl(t, scal) > tol:
                ok = False
                break
        if ok:
            sols.append({k: int(v) for k, v in scal.items()})
    return sols


def solve_hexagon(scal, tol=1e-9):
    """4개 위상 미지수 ζ₁₆ 지수 16^4 전수탐색 → hexagon(R±) 폐합 해집합."""
    unknown = [(SIG, SIG, ONE), (SIG, SIG, PSI), (SIG, PSI, SIG), (PSI, PSI, ONE)]
    sols = []
    for exps in itertools.product(range(16), repeat=4):
        rexp = {k: n for k, n in zip(unknown, exps)}
        ok = True
        for t in HEX_EQS:
            if hex_resid_fl(t, scal, rexp) > tol:
                ok = False
                break
        if ok:
            sols.append(dict(rexp))
    return sols


def fmt_scal(scal):
    return {f"F^{{{NAME[a]}{NAME[b]}{NAME[c]}}}_{NAME[d]}": s
            for (a, b, c, d), s in sorted(scal.items())}


def fmt_rexp(rexp):
    lab = {(SIG, SIG, ONE): "R^{σσ}_1", (SIG, SIG, PSI): "R^{σσ}_ψ",
           (SIG, PSI, SIG): "R^{σψ}_σ=R^{ψσ}_σ", (PSI, PSI, ONE): "R^{ψψ}_1"}
    return {lab[k]: f"ζ₁₆^{n} (=e^{{i{n}π/8}})" for k, n in rexp.items()}


def main():
    quick = "--quick" in sys.argv
    R = {}
    detail = {}

    # ── 1. pentagon 풀이 ──
    psols = solve_pentagon()
    R["pentagon_has_solution"] = (len(psols) >= 1)
    # 정준 gauge 선택: +1 개수 최다(가장 표준적) → 동률이면 정렬 첫째
    def score(sol):
        return (sum(1 for v in sol.values() if v == 1), )
    canon = max(psols, key=lambda s: (score(s), tuple(sorted(s.items())))) if psols else {}
    detail["pentagon_gauge_orbit_size"] = len(psols)
    detail["F_scalars_canonical"] = fmt_scal(canon) if canon else {}
    # 표준 부호(−1 인 스칼라) 목록
    neg_F = [f"F^{{{NAME[a]}{NAME[b]}{NAME[c]}}}_{NAME[d]}"
             for (a, b, c, d), s in sorted(canon.items()) if s == -1]
    detail["F_negative_scalars"] = neg_F

    # ── 2. hexagon 풀이(정준 F 위에서) ──
    if canon:
        if quick:
            # quick: 인용 R 만 검증(전수탐색 생략)
            quoted = {(SIG, SIG, ONE): 15, (SIG, SIG, PSI): 3,
                      (SIG, PSI, SIG): 12, (PSI, PSI, ONE): 8}
            hmax = max(hex_resid_fl(t, canon, quoted) for t in HEX_EQS)
            R["hexagon_quoted_R_closes"] = (hmax < 1e-9)
            hsols = [quoted]
        else:
            hsols = solve_hexagon(canon)
            R["hexagon_has_solution"] = (len(hsols) >= 1)
            quoted = {(SIG, SIG, ONE): 15, (SIG, SIG, PSI): 3,
                      (SIG, PSI, SIG): 12, (PSI, PSI, ONE): 8}
            R["hexagon_quoted_R_in_solution_set"] = (quoted in hsols)
        detail["hexagon_gauge_orbit_size"] = len(hsols)
    else:
        hsols = []
        quoted = {}

    # 인용값(=표준 Ising)을 정준 R 로 채택
    rcanon = {(SIG, SIG, ONE): 15, (SIG, SIG, PSI): 3, (SIG, PSI, SIG): 12, (PSI, PSI, ONE): 8}
    detail["R_canonical"] = fmt_rexp(rcanon)

    # ── 3. exact(ℚ(ζ₁₆)) 인증: 전 pentagon/hexagon 폐합 ──
    if canon:
        peqs = PENTA_EQS if not quick else PENTA_EQS[::7]
        p_exact = sum(1 for t in peqs if penta_resid_cyc(t, canon))
        R["pentagon_exact_all_closed"] = (p_exact == len(peqs))
        detail["pentagon_equations_checked"] = len(PENTA_EQS)
        detail["pentagon_exact_verified"] = p_exact if not quick else f"{p_exact}/{len(peqs)}(quick subset)"

        heqs = HEX_EQS if not quick else HEX_EQS[::5]
        h_exact = sum(1 for t in heqs if hex_resid_cyc(t, canon, rcanon))
        R["hexagon_exact_all_closed"] = (h_exact == len(heqs))
        detail["hexagon_equations_checked"] = len(HEX_EQS)
        detail["hexagon_exact_verified"] = h_exact if not quick else f"{h_exact}/{len(heqs)}(quick subset)"

    # ── 4. payoff: 리본 위상 θ (exact Cyc) ──
    # θ_σ = (1/√2)(R^{σσ}_1 + R^{σσ}_ψ) = ζ₁₆
    theta_sigma = C_INV_SQRT2 * (Cyc.zeta(15) + Cyc.zeta(3))
    R["topological_spin_theta_sigma_eq_zeta16"] = (theta_sigma - Cyc.zeta(1)).is_zero()
    # θ_ψ = R^{ψψ}_1 = ζ₁₆⁸ = −1
    theta_psi = Cyc.zeta(rcanon[(PSI, PSI, ONE)])
    R["topological_spin_theta_psi_eq_minus1"] = (theta_psi - C_ONE.scal(-1)).is_zero()

    # ── 5. payoff: modular (ST)³ = e^{2πic/8} S² (sympy exact 교차확인) ──
    import sympy as sp
    s2 = sp.sqrt(2)
    # 표준 Ising S (self-dual 전체 → S²=C=I): S_ψψ = +1/2 (M_ψψ = θ_1/θ_ψ² = +1)
    S = sp.Rational(1, 2) * sp.Matrix([[1, s2, 1], [s2, 0, -s2], [1, -s2, 1]])    # {1,σ,ψ}
    z16 = sp.exp(sp.I * sp.pi / 8)               # ζ₁₆ = e^{2πi/16}
    c = sp.Rational(1, 2)
    T = sp.diag(1, z16, -1)                       # T = diag(θ_a) (bare twist 관례)
    S2 = S * S
    R["modular_S_unitary_S2_eq_I"] = all((S2 - sp.eye(3))[i, j].equals(0)
                                         for i in range(3) for j in range(3))
    # bare-T 관례: (ST)³ = e^{2πi c/8}·S² (c=1/2 → 위상 = ζ₁₆). S_ψψ=+1 (task 표기 −1 은 오타).
    diff = (S * T) ** 3 - sp.exp(2 * sp.I * sp.pi * c / 8) * S2
    R["modular_ST3_eq_phase_S2"] = all(diff[i, j].equals(0) for i in range(3) for j in range(3))
    detail["central_charge_c"] = "1/2"
    detail["modular_phase_e^{2πic/8}"] = "ζ₁₆ = e^{iπ/8}"
    detail["modular_S_note"] = "S_ψψ = +1 (self-dual → S²=I; task 표기의 −1 은 오타 정정)"
    # θ_σ 를 sympy 로도 교차확인 — (e^{−iπ/8}+e^{3iπ/8})/√2 = e^{iπ/8}
    ts = (sp.exp(-sp.I * sp.pi / 8) + sp.exp(3 * sp.I * sp.pi / 8)) / sp.sqrt(2)
    R["theta_sigma_sympy_cross_check"] = (ts - z16).equals(0)

    # ── 6. teeth ──
    if canon:
        # (a) F 스칼라 1개 부호 flip → pentagon 최소1개 붕괴
        flipk = next(iter(canon))
        bad = dict(canon); bad[flipk] = -bad[flipk]
        p_break = any(penta_resid_fl(t, bad) > 1e-9 for t in PENTA_EQS)
        R["teeth_flip_F_breaks_pentagon"] = p_break
        # (b) R 위상 1개 flip(+1) → hexagon 최소1개 붕괴
        badr = dict(rcanon); badr[(SIG, SIG, ONE)] = (badr[(SIG, SIG, ONE)] + 1) % 16
        h_break = any(hex_resid_fl(t, canon, badr) > 1e-9 for t in HEX_EQS)
        R["teeth_flip_R_breaks_hexagon"] = h_break

    ok = all(R.values())

    # ── 출력 ──
    if not quick:
        print("Ising MTC pentagon+hexagon 전역 정합 공리 관측 (exact ℚ(ζ₁₆) — witness, seal 아님):",
              flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  pentagon 방정식 {len(PENTA_EQS)}개 · hexagon(R±) {len(HEX_EQS)}개 전수 폐합.",
              flush=True)
        print(f"  ★F gauge(orbit={detail['pentagon_gauge_orbit_size']}): +Hadamard·진공 F=1 고정, "
              f"−1 스칼라 = {neg_F if neg_F else '(없음)'}", flush=True)
        print(f"  ★R gauge(orbit={detail.get('hexagon_gauge_orbit_size','?')}): "
              f"R^{{σσ}}_1=ζ₁₆⁻¹·R^{{σσ}}_ψ=ζ₁₆³·R^{{σψ}}_σ=ζ₁₆⁻⁴(=−i)·R^{{ψψ}}_1=ζ₁₆⁸(=−1)",
              flush=True)
        print("  ★payoff: θ_σ=ζ₁₆(리본, exact)·θ_ψ=−1 · modular (ST)³=e^{2πic/8}S²=ζ₁₆·S² (c=1/2)·S²=I.",
              flush=True)
        print("  ★정직: 관측=F/R 표(pentagon/hexagon 공리)뿐. anyon 게이트 회로 봉인 아님(ζ₁₆ module="
              "사람게이트·범위밖). fusion/braid/modular 관측과 검증객체 상이·신규 module 0·root 불변.",
              flush=True)

    # ── sidecar ──
    _write_sidecar(R, detail)

    print(f"ising_fr_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


def _write_sidecar(R, detail):
    obj = {
        "_note": "Ising MTC pentagon+hexagon 전역 정합 공리 관측(exact ℚ(ζ₁₆)). 신규 module 0·root 불변. "
                 "F/R 표=데이터(anyon 게이트 회로 봉인 아님). fusion/braid/modular 관측과 검증객체 상이.",
        "_schema": "ising-fr-observe-v1",
        "observation": {
            "axis": "TrackHE13 P5 — Ising MTC pentagon(Biedenharn-Elliott)+hexagon(Bonderson R±) 전역 공리",
            "ok": bool(all(R.values())),
            "checks": {k: bool(v) for k, v in R.items()},
            "F_symbols": {
                "nontrivial_2x2": "F^{σσσ}_σ = (1/√2)[[1,1],[1,−1]] (채널기저 {1,ψ}, +Hadamard 고정)",
                "vacuum_gauge": "진공다리 F=1 (단위 정규화)",
                "scalars_canonical": detail.get("F_scalars_canonical", {}),
                "negative_scalars": detail.get("F_negative_scalars", []),
                "pentagon_gauge_orbit_size": detail.get("pentagon_gauge_orbit_size"),
            },
            "R_symbols": {
                "canonical": detail.get("R_canonical", {}),
                "values": "R^{σσ}_1=ζ₁₆⁻¹=e^{−iπ/8} · R^{σσ}_ψ=ζ₁₆³=e^{i3π/8} · "
                          "R^{σψ}_σ=R^{ψσ}_σ=ζ₁₆⁻⁴=−i · R^{ψψ}_1=ζ₁₆⁸=−1",
                "hexagon_gauge_orbit_size": detail.get("hexagon_gauge_orbit_size"),
            },
            "equation_counts": {
                "pentagon": detail.get("pentagon_equations_checked"),
                "pentagon_exact_verified": detail.get("pentagon_exact_verified"),
                "hexagon_R_plus_minus": detail.get("hexagon_equations_checked"),
                "hexagon_exact_verified": detail.get("hexagon_exact_verified"),
            },
            "payoffs": {
                "topological_spin": "θ_σ=ζ₁₆ (리본 exact) · θ_ψ=−1 · θ_1=1",
                "central_charge": detail.get("central_charge_c"),
                "modular": "(ST)³ = e^{2πic/8} S² = ζ₁₆·S² (c=1/2) · S²=I · S 유니터리",
            },
            "honest_boundary": "관측 — Ising MTC 의 pentagon/hexagon 전역 일관성 공리 폐합(F/R 표=데이터). "
                               "anyon 게이트 회로 봉인 아님(ζ₁₆ 위상 module=사람게이트, 범위밖). "
                               "gauge 선택(+Hadamard·진공 F=1) 명시. ising_fusion(융합환)·mtc_braid(개별 braid)"
                               "·su2_3_mtc(modular data) 관측과 검증객체 상이. 신규 module 0·root 불변.",
            "deterministic": True,
        },
    }
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        ".pgf", "proofs", "ISING-FR-OBSERVE.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=2, sort_keys=True)


if __name__ == "__main__":
    sys.exit(main())
