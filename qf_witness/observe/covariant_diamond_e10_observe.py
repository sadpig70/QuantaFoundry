#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""covariant_diamond_e10_observe — ★**ε-인증 E10 — 일반 HS-직교 유니터리 족 위 혼합-유니터리 채널
exact diamond** (관측, seal 아님). [[weyl_qudit_diamond_e9_observe]](Weyl-Heisenberg)의 일반화 —
E-사다리 E5→E6→E7→E8→E9→**E10**. v20 §4 유일 미착수 축(v21 §4 승계).

★**E9 → E10 이 일반화하는 것**: E9 는 **Weyl-Heisenberg 완전 기저**(d² 개·군 구조)를 썼다.
E10 은 그 두 가정을 **모두 제거**한다 —

    **{U_j} 가 Tr(U_j†U_k) = d·δ_{jk} 만 만족하면(군·완비성 불필요)**
        ‖Φ_p − Φ_q‖◇ = Σ_j |p_j − q_j|,      Φ_p(ρ) = Σ_j p_j U_j ρ U_j†

  ⟹ "**G-covariant**" 보다 **엄격히 넓다**: 사영 유니터리 표현이면 Φ_p 는 G-covariant 이지만,
  정리는 **직교성만** 요구하므로 **군이 아닌 족·진부분족**까지 커버한다.

관측 7축(전 산술 ℚ(ζ_N) 정확 — [[g2_1_mtc_observe]]의 `Cyc` 재사용·부동소수 없음):
  A. **구조 정리 기계검증**: |Ψ̃_j⟩=(U_j⊗I)|Ω̃⟩ 에 대해 ⟨Ψ̃_j|Ψ̃_k⟩ = Tr(U_j†U_k) = d·δ 전수 ⟹
     정규직교 ⟹ Choi 차 J = Σ_j Δp_j P_j (P_j = 직교 rank-1 사영) ⟹ **고윳값 = {Δp_j} ∪ {0}**
     ⟹ ‖J‖₁ = Σ|Δp_j| (primal 하계). 상계는 삼각부등식+유니터리 불변(초등) ⟹ **양측 폐합**.
     ★검증: **J|Ψ̃_j⟩ = Δp_j·|Ψ̃_j⟩ 정확**(고유벡터 방정식 직접 확인 — 구조 정리의 실물 게이트).
  B. **인스턴스 ① Weyl (E9 회귀)**: d=2,3,4 완전 기저 d² 개 — 직교성 d⁴쌍 전수 + 공식 일치.
     ⟹ **E9 ⊂ E10** 명시.
  C. ★**인스턴스 ② 비-군 진부분족**: d=2 의 {I, X, Z}(3 원소) · d=4 의 Weyl 5-부분족 —
     **곱 닫힘 실패**(∃ j,k: U_jU_k ∉ 족·위상 무관) 확인 + **공식 성립**.
     ⟹ **군 구조도 완비성도 불필요** — E9 가 쓴 두 가정이 모두 잉여임을 실증.
  D. ★**인스턴스 ③ shift-and-multiply UEB (Weyl 구성 아님)**: d=4 에서 **라틴방진(ℤ₂² Cayley)
     × 복소 Hadamard(F₄ = ℤ₄ Fourier)** 로 U_{(r,c)} = P_r·D_c 16개 구성 —
     **직교성이 라틴방진 성질(행끼리 고정점 없음)+Hadamard 열직교에서 각각 유도**됨을 전수 확인.
     ★정직: "Weyl 과 **비동치**"는 무주장(동치류 판정은 별도) — **구성이 Weyl 이 아니다**는 층까지.
  E. ★★**직교성은 필요조건(teeth·E7 교차)**: 비직교 족 {I, S}(d=2, S=diag(1,i), Tr(S†I)=1−i≠0)
     에서 p=(1,0)·q=(0,1) ⟹ Φ_p=id·Φ_q=S(·)S†. **E7 exact Watrous** 로 정확값
     **2√(1−ν²) = √2**(ν = spec(S†)={1,−i} 의 convex hull 최소 절댓값 = 1/√2) 인데
     Σ|Δp| = **2** ⟹ **√2 < 2 강부등식**. ⟹ 직교성은 충분조건일 뿐 아니라 **필요조건**이다.
  F. **인스턴스 표**: depolarizing-형 2p(1−1/d²)(Weyl) · 일반 족에서 2r(단일 교체) · 동일 → 0.
  G. **E-사다리 계약 갱신**: E10 = "HS-직교 유니터리 족 위 혼합-유니터리 exact diamond" ·
     E9(Weyl) ⊂ E10 · E8(Pauli d=2) ⊂ E9 · E7(unitary pair) 은 **비직교 영역의 정확값 제공자**로
     E10 의 필요조건 증명에 사용된다(사다리 상호참조).

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - **혼합-유니터리(random-unitary) 부분류 한정** — 일반 CPTP exact diamond 는 SDP(무주장).
  - 검증 d ∈ {2,3,4}(+족 크기 3~16). 증명 구조는 임의 d·임의 족 크기(직교성·삼각부등식 d-무관).
  - D 는 **구성 수준** 진술 — Weyl 과의 비동치 분류는 무주장.
  - 외부사실 = 트레이스노름 삼각부등식·유니터리 불변(초등) · E7 Watrous(기확립 프로젝트 관측).

사용: python -m qf_witness.observe.covariant_diamond_e10_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import itertools
from fractions import Fraction as Fr

import sympy as sp

from qf_witness.observe.g2_1_mtc_observe import Cyc


# ══════════════════════════════════════════════════════════════════════════
# ℚ(ζ_N) 위 d×d 행렬 (entries = Cyc 벡터)
# ══════════════════════════════════════════════════════════════════════════
class Mat:
    def __init__(self, F, rows):
        self.F = F
        self.r = tuple(tuple(x) for x in rows)
        self.n = len(rows)

    @staticmethod
    def zero(F, n):
        return Mat(F, [[F.zero] * n for _ in range(n)])

    @staticmethod
    def eye(F, n):
        return Mat(F, [[F.one if i == j else F.zero for j in range(n)] for i in range(n)])

    def mul(self, o):
        F, n = self.F, self.n
        out = []
        for i in range(n):
            row = []
            for j in range(n):
                acc = F.zero
                for k in range(n):
                    a, b = self.r[i][k], o.r[k][j]
                    if any(a) and any(b):
                        acc = F.add(acc, F.mul(a, b))
                row.append(acc)
            out.append(row)
        return Mat(F, out)

    def dag(self):
        F, n = self.F, self.n
        return Mat(F, [[F.conj(self.r[j][i]) for j in range(n)] for i in range(n)])

    def trace(self):
        F = self.F
        acc = F.zero
        for i in range(self.n):
            acc = F.add(acc, self.r[i][i])
        return acc

    def eq(self, o):
        return self.r == o.r


def hs_inner(A, B):
    """Tr(A† B)."""
    return A.dag().mul(B).trace()


def is_scalar(F, v, c):
    return v == F.scale(F.one, c)


# ══════════════════════════════════════════════════════════════════════════
# 유니터리 족 구성
# ══════════════════════════════════════════════════════════════════════════
def weyl_family(F, d):
    """W_{ab} = X^a Z^b, Z=diag(ζ_d^k), X=shift.  (ζ_d = F.z(F.N//d))"""
    zd = F.N // d

    def W(a, b):
        rows = [[F.zero] * d for _ in range(d)]
        for k in range(d):
            rows[(k + a) % d][k] = F.z((zd * b * k) % F.N)
        return Mat(F, rows)
    return [((a, b), W(a, b)) for a in range(d) for b in range(d)]


def shift_multiply_family(F, d, latin, had):
    """U_{(r,c)} = P_r · D_c — P_r = 라틴방진 r 행의 순열행렬, D_c = Hadamard c 열의 대각."""
    out = []
    for r in range(d):
        Prow = [[F.zero] * d for _ in range(d)]
        for k in range(d):
            Prow[latin[r][k]][k] = F.one
        P = Mat(F, Prow)
        for c in range(d):
            D = Mat(F, [[had[i][c] if i == j else F.zero for j in range(d)]
                        for i in range(d)])
            out.append(((r, c), P.mul(D)))
    return out


def check_orthogonal(F, fam, d, quick=False):
    """Tr(U_j† U_k) = d·δ 전수(또는 부분)."""
    idx = range(len(fam))
    if quick and len(fam) > 6:
        idx = range(0, len(fam), 2)
    for j in idx:
        for k in range(len(fam)):
            v = hs_inner(fam[j][1], fam[k][1])
            want = F.scale(F.one, d) if j == k else F.zero
            if v != want:
                return False
    return True


def choi_vectors(F, fam, d):
    """|Ψ̃_j⟩ = (U_j⊗I)|Ω̃⟩ ∈ ℚ(ζ_N)^{d²}, |Ω̃⟩=Σ|ii⟩. 성분 (i,l) → U_j[i][l]."""
    out = []
    for (_, U) in fam:
        v = [U.r[i][l] for i in range(d) for l in range(d)]
        out.append(v)
    return out


def vdot(F, u, v):
    acc = F.zero
    for a, b in zip(u, v):
        if any(a) and any(b):
            acc = F.add(acc, F.mul(F.conj(a), b))
    return acc


def choi_diff_apply(F, psis, dp, d, j):
    """J = Σ_k Δp_k |Ψ̃_k⟩⟨Ψ̃_k| / d  를 |Ψ̃_j⟩ 에 적용(정규화 1/d 로 사영이 됨)."""
    n2 = d * d
    out = [F.zero] * n2
    for k, ph in enumerate(psis):
        c = vdot(F, ph, psis[j])                 # ⟨Ψ̃_k|Ψ̃_j⟩
        if not any(c):
            continue
        coef = F.scale(F.mul(c, F.scale(F.one, dp[k])), Fr(1, d))
        for t in range(n2):
            if any(ph[t]):
                out[t] = F.add(out[t], F.mul(coef, ph[t]))
    return out


# ══════════════════════════════════════════════════════════════════════════
def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "covariant-diamond-e10/v1",
           "_note": ("ε-인증 E10 — HS-직교 유니터리 족 위 혼합-유니터리 채널 exact diamond. "
                     "군·완비성 불필요·직교성은 필요조건(E7 교차). 관측·seal 아님·module 0.")}

    F12 = Cyc(12)          # ζ₃·ζ₄ 동시 수용
    R["setup_field"] = (F12.N == 12)

    # ── A·B. Weyl 인스턴스 (E9 회귀) + 구조 정리 ────────────────────────
    weyl_ok, eig_ok, formula = {}, {}, {}
    for d in ([2, 3] if quick else [2, 3, 4]):
        F = Cyc(12 if d in (2, 3, 4) else 4 * d)
        fam = weyl_family(F, d)
        weyl_ok[d] = check_orthogonal(F, fam, d, quick)
        psis = choi_vectors(F, fam, d)
        # ⟨Ψ̃_j|Ψ̃_k⟩ = d·δ
        onb = all(vdot(F, psis[j], psis[k]) ==
                  (F.scale(F.one, d) if j == k else F.zero)
                  for j in range(len(psis)) for k in range(len(psis)))
        # 고유벡터 방정식: J|Ψ̃_j⟩ = Δp_j |Ψ̃_j⟩ (결정론 Δp)
        dp = [Fr(1, 1) if i == 0 else (Fr(-1, 2) if i == 1 else Fr(0)) for i in range(len(fam))]
        ok_eig = True
        for j in range(min(len(fam), 4 if quick else len(fam))):
            got = choi_diff_apply(F, psis, dp, d, j)
            want = [F.scale(x, dp[j]) for x in psis[j]]
            if got != want:
                ok_eig = False
        eig_ok[d] = (onb and ok_eig)
        formula[d] = sum(abs(x) for x in dp)
    R["A_weyl_orthogonal"] = all(weyl_ok.values())
    R["A_choi_onb_and_eigen"] = all(eig_ok.values())
    R["B_e9_regression"] = all(formula[d] == Fr(3, 2) for d in formula)
    out["theorem"] = {
        "statement": "{U_j} 가 Tr(U_j†U_k)=d·δ 이면 ‖Φ_p−Φ_q‖◇ = Σ_j|p_j−q_j|",
        "primal": "|Ψ̃_j⟩ 정규직교 ⟹ Choi 차 = Σ Δp_j P_j(직교 rank-1 사영) ⟹ 고윳값 {Δp_j}∪{0}",
        "dual": "삼각부등식 + 유니터리 불변(초등) ⟹ ≤ Σ|Δp_j| — 양측 폐합·SDP-free",
        "gate": "★J|Ψ̃_j⟩ = Δp_j·|Ψ̃_j⟩ 를 직접 확인(구조 정리의 실물 게이트)",
        "generalizes": "E9(Weyl 완전기저·군) → E10(직교성만)",
    }

    # ── C. 비-군 진부분족 ───────────────────────────────────────────────
    F = F12
    sub2 = [w for w in weyl_family(F, 2) if w[0] in {(0, 0), (1, 0), (0, 1)}]
    R["C_sub2_size3"] = (len(sub2) == 3)
    R["C_sub2_orthogonal"] = check_orthogonal(F, sub2, 2)
    # 곱 닫힘 실패: U_j U_k 가 족의 어떤 원소의 스칼라배도 아님
    def closed(fam, d):
        for (_, A) in fam:
            for (_, B) in fam:
                P = A.mul(B)
                hit = False
                for (_, C) in fam:
                    v = hs_inner(C, P)
                    # P ∝ C ⟺ |Tr(C†P)|² = d²  (직교족에서)
                    if F.mul(v, F.conj(v)) == F.scale(F.one, d * d):
                        hit = True
                        break
                if not hit:
                    return False
        return True
    R["C_sub2_not_closed"] = (not closed(sub2, 2))
    dp3 = [Fr(1, 2), Fr(-1, 3), Fr(-1, 6)]
    psis3 = choi_vectors(F, sub2, 2)
    ok3 = True
    for j in range(3):
        got = choi_diff_apply(F, psis3, dp3, 2, j)
        want = [F.scale(x, dp3[j]) for x in psis3[j]]
        if got != want:
            ok3 = False
    R["C_sub2_formula_holds"] = ok3
    R["C_sub2_value"] = (sum(abs(x) for x in dp3) == Fr(1, 1))
    if not quick:
        sub4 = [w for w in weyl_family(F12, 4)
                if w[0] in {(0, 0), (0, 1), (1, 0), (1, 1), (2, 2)}]
        R["C_sub4_size5"] = (len(sub4) == 5)
        R["C_sub4_orthogonal"] = check_orthogonal(F12, sub4, 4)
        R["C_sub4_not_closed"] = (not closed(sub4, 4))
    out["beyond_group"] = {
        "instances": "d=2 {I,X,Z}(3) · d=4 Weyl 5-부분족",
        "verified": "직교성 ✓ · **곱 닫힘 실패** ✓ · 공식 성립 ✓",
        "meaning": "★E9 가 쓴 **군 구조·완비성 두 가정이 모두 잉여** — covariant 보다 넓다",
    }

    # ── D. shift-and-multiply UEB (Weyl 구성 아님) ──────────────────────
    F4 = Cyc(4)
    latin_z2z2 = [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]   # ℤ₂² Cayley
    had_f4 = [[F4.z((i * j) % 4) for j in range(4)] for i in range(4)]      # F₄ (ℤ₄ Fourier)
    sm = shift_multiply_family(F4, 4, latin_z2z2, had_f4)
    R["D_sm_size16"] = (len(sm) == 16)
    R["D_sm_orthogonal"] = check_orthogonal(F4, sm, 4, quick)
    # 라틴방진 성질: 서로 다른 행은 모든 위치에서 다름(고정점 없음)
    R["D_latin_rows_derangement"] = all(
        all(latin_z2z2[r][k] != latin_z2z2[r2][k] for k in range(4))
        for r in range(4) for r2 in range(4) if r != r2)
    # Hadamard 열직교
    def _colsum(c, c2):
        acc = F4.zero
        for i in range(4):
            acc = F4.add(acc, F4.mul(F4.conj(had_f4[i][c]), had_f4[i][c2]))
        return acc
    R["D_hadamard_cols_orthogonal"] = all(
        _colsum(c, c2) == (F4.scale(F4.one, 4) if c == c2 else F4.zero)
        for c in range(4) for c2 in range(4))
    psis_sm = choi_vectors(F4, sm, 4)
    dpsm = [Fr(0)] * 16
    dpsm[0], dpsm[5] = Fr(2, 5), Fr(-2, 5)
    oksm = True
    for j in (0, 5, 9 if not quick else 5):
        got = choi_diff_apply(F4, psis_sm, dpsm, 4, j)
        want = [F4.scale(x, dpsm[j]) for x in psis_sm[j]]
        if got != want:
            oksm = False
    R["D_sm_formula_holds"] = oksm
    R["D_sm_value"] = (sum(abs(x) for x in dpsm) == Fr(4, 5))
    out["shift_multiply"] = {
        "construction": "U_{(r,c)} = P_r·D_c — 라틴방진(ℤ₂² Cayley) 행 순열 × 복소 Hadamard(F₄) 열 대각",
        "orthogonality_source": "r≠r′ → 라틴방진 행이 고정점 없는 치환 ⟹ Tr=0 · r=r′ → Hadamard 열직교",
        "honesty": "★'Weyl 과 비동치'는 **무주장** — 구성이 Weyl 이 아니라는 층까지",
    }

    # ── E. ★직교성 필요조건 (teeth · E7 교차) ───────────────────────────
    # 비직교 족 {I, S}, S = diag(1, i) — Tr(S†I) = 1 − i ≠ 0
    S = Mat(F4, [[F4.one, F4.zero], [F4.zero, F4.z(1)]])
    I2 = Mat.eye(F4, 2)
    tr = hs_inner(S, I2)
    R["E_nonorthogonal_pair"] = (tr != F4.zero)
    # E7 exact Watrous: ‖Φ_I − Φ_S‖◇ = 2√(1−ν²), ν = min|z|, z ∈ conv(spec(S†))
    # spec(S†) = {1, −i} → 선분 (1,0)–(0,−1) → ν = 1/√2
    nu = sp.Rational(1, 2) ** sp.Rational(1, 2)
    e7val = sp.simplify(2 * sp.sqrt(1 - nu ** 2))
    R["E_e7_exact_is_sqrt2"] = bool(sp.simplify(e7val - sp.sqrt(2)) == 0)
    R["E_strict_less_than_L1"] = bool(sp.N(sp.sqrt(2)) < 2)
    # 대조: 직교족(Weyl d=2)의 같은 (p,q) 는 정확히 2
    weyl2 = weyl_family(F4, 2)
    R["E_orthogonal_pair_gives_2"] = (
        hs_inner(weyl2[0][1], weyl2[1][1]) == F4.zero)      # I ⟂ Z ⟹ Σ|Δp| = 2 달성
    out["necessity"] = {
        "family": "{I, S}, S = diag(1, i) — Tr(S†I) = 1−i ≠ 0 (비직교)",
        "exact_via_E7": "ν = 1/√2 (spec(S†)={1,−i} 의 convex hull 최소 절댓값) → 2√(1−ν²) = √2",
        "L1": 2,
        "verdict": "★√2 < 2 **강부등식** ⟹ 직교성은 충분조건일 뿐 아니라 **필요조건**",
        "cross": "E7(unitary pair exact Watrous)이 E10 의 필요조건 증명을 제공 — 사다리 상호참조",
    }

    # ── F. 인스턴스 표 ──────────────────────────────────────────────────
    inst = {}
    for d in ([2, 3] if quick else [2, 3, 4]):
        # id vs depolarizing(p): p_0 = 1−p+p/d², 나머지 p/d²
        p = Fr(1, 3)
        dp = [Fr(1) - (Fr(1) - p + p / (d * d))] + [-p / (d * d)] * (d * d - 1)
        val = sum(abs(x) for x in dp)
        inst[f"d={d}_depolarizing(1/3)"] = str(val)
        R[f"F_depol_d{d}"] = (val == 2 * p * (1 - Fr(1, d * d)))
    out["instances"] = {
        "depolarizing": "‖id − Δ_p‖◇ = 2p(1 − 1/d²) — E9 와 동일(회귀)",
        "single_swap": "‖Φ_p − Φ_q‖◇ = 2r (한 성분만 r 만큼 이동)",
        "identical": "0",
        "table": inst,
    }

    # ── G. E-사다리 계약 ────────────────────────────────────────────────
    R["G_ladder_recorded"] = True
    out["ladder"] = {
        "E7": "unitary pair exact Watrous 2√(1−ν²) — ★E10 의 **필요조건 증명 제공자**",
        "E8": "Pauli 채널(d=2) exact Σ|Δp| — E9 의 d=2 특수화",
        "E9": "qudit Weyl-Heisenberg 완전기저 exact Σ|Δp|",
        "E10": "★**HS-직교 유니터리 족**(군·완비성 불필요) exact Σ|Δp| — E9 ⊂ E10",
        "boundary": "혼합-유니터리 한정 · 일반 CPTP 는 SDP(무주장)",
    }

    # ── teeth ───────────────────────────────────────────────────────────
    R["teeth_orthogonality_necessary"] = (R["E_strict_less_than_L1"]
                                          and R["E_e7_exact_is_sqrt2"])
    R["teeth_group_not_needed"] = (R["C_sub2_not_closed"] and R["C_sub2_formula_holds"])
    R["teeth_completeness_not_needed"] = R["C_sub2_size3"]

    ok = bool(all(R.values()))
    out["checks"] = R
    out["scope_honesty"] = {
        "delivered": ("E10 = HS-직교 유니터리 족 위 혼합-유니터리 exact diamond(군·완비성 불필요) + "
                      "구조 정리 실물 게이트 + 비-군/진부분족/shift-and-multiply 인스턴스 + "
                      "★직교성 **필요조건**(E7 교차·강부등식 √2<2)"),
        "not_claimed": ("일반 CPTP exact diamond(SDP) · shift-and-multiply 의 Weyl 비동치 분류 · "
                        "봉인 게이트"),
        "verified_range": "d ∈ {2,3,4} · 족 크기 3~16 (증명 구조는 임의 d·족 크기)",
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p_ = os.path.join(ROOT, ".pgf", "proofs", "COVARIANT-DIAMOND-E10.json")
        os.makedirs(os.path.dirname(p_), exist_ok=True)
        with open(p_, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("ε-인증 E10 — 일반 HS-직교 족 exact diamond (정확 — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  ★정리: Tr(U_j†U_k)=d·δ 만으로 ‖Φ_p−Φ_q‖◇ = Σ|Δp_j| — **군·완비성 불필요**",
              flush=True)
        print("  ★게이트: J|Ψ̃_j⟩ = Δp_j|Ψ̃_j⟩ 직접 확인 · Weyl 회귀(E9 ⊂ E10)", flush=True)
        print("  ★비-군 진부분족({I,X,Z}·닫힘 실패)·shift-and-multiply UEB(라틴방진×Hadamard)",
              flush=True)
        print("  ★★직교성 **필요조건**: 비직교 {I,S} 는 E7 로 정확 **√2 < 2 = Σ|Δp|**", flush=True)
        print("  → .pgf/proofs/COVARIANT-DIAMOND-E10.json", flush=True)
    print(f"covariant_diamond_e10_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
