#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dtw_d4_mu4_ribbon_observe — ★**D^ω(D₄) μ₄ 층 ribbon-gap 폐합 — 근본원인 = 켤레 규약**
(관측, seal 아님). [[dtw_d4_zeta16_observe]](TrackHE19 P2)가 정직하게 열어둔 유일한 미결
("z=Σδ_a⊗a 가 μ₄ 층에서 (ST)³=λS² 를 깨뜨림 ⟹ quasi-Hopf ribbon 의 ω-보정 일반식 필요")를
**해소**한다.

★결론(선요약): **ω-보정은 불필요**. ribbon 원소 z=Σδ_a⊗a 는 μ₄ 층에서도 정확하다.
갭의 진범은 **S-행렬 문자공식의 켤레 규약 누락**이었고, 그것이 μ₂ 층에서 보이지 않았던 이유는
**μ₂ 층의 charge conjugation C 가 항등**(전 anyon 자기쌍대)이기 때문이다. μ₄ ζ₁₆ 층은
**첫 비자기쌍대 층**이라 처음으로 규약이 드러났다 — 그 지문이 **결함 순열 = C 자체**다.

관측 7축(전 산술 ℚ(ζ₁₆)/ℚ(ζ₃₆) 정확 Fraction):
  A. ★**balancing 지표 규약을 독립 오라클로 확정**: [[g2_1_mtc_observe]]의 level-k Lie 엔진으로
     **SU(3)₁**(비자기쌍대 C=[0,2,1])를 Kac-Peterson 1차원리 구성 → (ST)³∝S² 를 만족하는 S 는
     **form A** `D·S_ij = Σ_k N_{i,j*}^k d_k θ_k/(θ_iθ_j)` 를 만족하고 **form B**(N_{ij})는
     불성립. ★teeth: **자기쌍대 예제(Fib=(G₂)₁)에서는 A/B 판별 불가** — 규약을 자기쌍대에서
     검증하면 blind 라는 것을 실증.
  B. **μ₄(P₄=1) 층 재구성 + 결함 정밀 측정**: 22 모듈·Σd²=64·S 대칭·유니터리·S²=C·dims{1⁸,2¹⁴}
     — 원 S·θ 에서 **(ST)³·(S²)⁻¹ = C 정확**. 즉 **(ST)³ = I 인데 S² = C ≠ I**.
     결함은 **위상이 아니라 순열**(그것도 charge conjugation) — 대각 ε-위상 탐색이 실패한 이유.
  C. ★★**3중 독립 심판 → 수정 S̄ 확정**(전부 같은 답):
     ① SL(2,ℤ): **(S̄T)³ = λS̄², λ=1** ② **balancing form A**(A축에서 확정한 규약)
     ③ ★**Gauss 합**(S 규약을 전혀 쓰지 않음): p₊=Σd_a²θ_a = **8 = D** · **p₊p₋ = 64 = D²** ·
     **p₊/D = 1 = λ**.
  D. ★**구조적 확증**: Drinfeld double(=Drinfeld center)은 **c ≡ 0 mod 8** — p₊/D=1 이
     정확히 그것. 수정 후 데이터가 double 이어야 할 값을 준다.
  E. ★**blind-spot 정확 국소화**: **S̄ = S∘C** 정확 실증 ⟹ S-단독 게이트(대칭·유니터리·S²=C·
     Verlinde·dims·S_vac)는 **전부 켤레-blind**(S̄ 는 라벨을 C 로 바꾼 같은 표). μ₂ 층 표본
     3 클래스에서 **C = 항등** ⟹ S 실수 ⟹ 규약 무해(그래서 μ₂ 는 통과했다).
  F. **P₄=3 층 동일 폐합** — 수정 규약에서 (ST)³=λS² 성립·λ 일치.
  G. ★**폐합 판정**: z=Σδ_a⊗a 는 μ₄ 층에서도 **스칼라 작용(ribbon)** 전수 — quasi-Hopf ω-보정
     **불필요**. TrackHE19 P2 의 "ribbon-gap = μ₄ 층 구조적 실패" 는 **규약 아티팩트로 판정·철회**.

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - ★**철회 고지**: 본 관측은 선행 관측([[dtw_d4_zeta16_observe]])의 "ribbon-gap 신발견"을
    **정정·철회**한다. 갭은 실재했으나 그 해석("ω-보정 필요")이 틀렸다.
  - balancing 의 지표 규약(form A)은 **문헌 인용이 아니라** SU(3)₁ 에서 **결정**한 것이다.
  - "Drinfeld double 은 c≡0" 은 표준 사실을 **확증용으로 사용**할 뿐 — 이것으로 규약을
    정한 것이 아니다(규약은 ①②③ 이 독립적으로 이미 확정).
  - modular data 수준 관측 — braiding 게이트 실봉인·F/R-symbol 무주장.

사용: python -m qf_witness.observe.dtw_d4_mu4_ribbon_observe [--quick]
"""
from __future__ import annotations
import sys
import json
from fractions import Fraction as Fr

from qf_witness.observe.dtw_d4_zeta16_observe import (
    C16, ZP16, build_cocycles, build_modules16, apply_op16, _dot)
from qf_witness.observe.dtw_d4_u1_census_observe import INV, conj, E
from qf_witness.observe.g2_1_mtc_observe import Cyc, LieLevel


# ══════════════════════════════════════════════════════════════════════════
# A. balancing 지표 규약 — SU(3)₁(비자기쌍대) 독립 오라클
# ══════════════════════════════════════════════════════════════════════════
def _lie_mtc(A, d, k, N):
    """Kac-Peterson modular data → (Ŝ=S̃/S̃₀₀, dims, θ, N_fusion, C, field)."""
    L = LieLevel("probe", A, d, k)
    F = Cyc(N)
    St = L.s_tilde(F)
    m = len(L.weights)
    inv00 = F.inv(St[0][0])
    Shat = [[F.mul(St[i][j], inv00) for j in range(m)] for i in range(m)]
    dims = [Shat[0][i] for i in range(m)]
    hs = [L.h(w) for w in L.weights]
    theta = [F.z(int(h * N) % N) for h in hs]
    norm = F.zero
    for kk in range(m):
        norm = F.add(norm, F.mul(St[0][kk], F.conj(St[0][kk])))
    NORM = norm[0]
    invN = F.inv(F.scale(F.one, NORM))
    inv0 = [F.inv(St[0][Lx]) for Lx in range(m)]
    Nf = {}
    for i in range(m):
        for j in range(m):
            for kk in range(m):
                acc = F.zero
                for Lx in range(m):
                    acc = F.add(acc, F.mul(F.mul(St[i][Lx], St[j][Lx]),
                                           F.mul(F.conj(St[kk][Lx]), inv0[Lx])))
                acc = F.mul(acc, invN)
                Nf[(i, j, kk)] = int(acc[0]) if (all(x == 0 for x in acc[1:])
                                                and acc[0].denominator == 1) else None
    Cc = [next((j for j in range(m) if Nf[(i, j, 0)] == 1), None) for i in range(m)]
    return F, m, Shat, dims, theta, Nf, Cc


def _mat3(F, m, Sh, th):
    """(ŜT)³ 이 Ŝ² 에 비례하는가 → (holds, lam)."""
    def mmul(X, Y):
        return [[_fdot(F, X[i], [Y[t][j] for t in range(m)]) for j in range(m)]
                for i in range(m)]
    T = [[(th[i] if i == j else F.zero) for j in range(m)] for i in range(m)]
    S2 = mmul(Sh, Sh)
    ST = mmul(Sh, T)
    ST3 = mmul(mmul(ST, ST), ST)
    lam = None
    ok = True
    for i in range(m):
        for j in range(m):
            if all(x == 0 for x in S2[i][j]):
                if any(x != 0 for x in ST3[i][j]):
                    ok = False
            else:
                q = F.mul(ST3[i][j], F.inv(S2[i][j]))
                if lam is None:
                    lam = q
                elif q != lam:
                    ok = False
    return ok, lam


def _fdot(F, r, c):
    acc = F.zero
    for a, b in zip(r, c):
        acc = F.add(acc, F.mul(a, b))
    return acc


def _balancing(F, m, Sh, th, dims, Nf, Cc, dualize_j):
    """form A(dualize_j=True): Ŝ_ij = Σ_k N_{i,j*}^k d_k θ_k/(θ_iθ_j)  [Ŝ = D·S]."""
    for i in range(m):
        for j in range(m):
            jj = Cc[j] if dualize_j else j
            acc = F.zero
            for kk in range(m):
                nk = Nf[(i, jj, kk)]
                if nk:
                    acc = F.add(acc, F.scale(F.mul(th[kk], dims[kk]), nk))
            rhs = F.mul(acc, F.mul(F.inv(th[i]), F.inv(th[j])))
            if Sh[i][j] != rhs:
                return False
    return True


# ══════════════════════════════════════════════════════════════════════════
# B–G. μ₄ 층
# ══════════════════════════════════════════════════════════════════════════
def _mm16(n, A, B, conjB=False):
    return [[_dot(A[i], [(B[j][k].conj() if conjB else B[k][j]) for k in range(n)])
             for j in range(n)] for i in range(n)]


def _z16pow(x):
    for k in range(16):
        if x.eq(ZP16[k]):
            return k
    return None


def mu4_layer(th_slant, quick=False):
    """μ₄ 층 modular data 를 원 규약(S)과 수정 규약(S̄=S∘C) 양쪽으로 산출."""
    mods = build_modules16(th_slant)
    n = len(mods)
    TR = []
    for (lab, dim, act) in mods:
        t = {}
        for g in range(8):
            for x in range(8):
                s = C16.zero()
                for col, entries in act[(g, x)].items():
                    for (row, cf) in entries:
                        if row == col:
                            s = s.add(cf)
                t[(g, x)] = s
        TR.append(t)
    S = [[C16.zero() for _ in range(n)] for _ in range(n)]
    for I in range(n):
        for J in range(n):
            acc = C16.zero()
            for g in range(8):
                for h in range(8):
                    a = TR[I][(conj(g, h), h)]
                    if a.is_zero():
                        continue
                    b = TR[J][(h, g)]
                    if b.is_zero():
                        continue
                    acc = acc.add(a.mul(b))
            S[I][J] = acc.scale(Fr(1, 8))
    vac = next(I for I in range(n) if all(
        TR[I][(g, x)].eq(C16.one() if g == E else C16.zero())
        for g in range(8) for x in range(8)))
    # ribbon z = Σ δ_a ⊗ a — 스칼라 작용 전수 확인
    theta = []
    ribbon_scalar = True
    for (lab, dim, act) in mods:
        th0 = None
        for j in range(dim):
            vec = [C16.one() if i == j else C16.zero() for i in range(dim)]
            out = [C16.zero()] * dim
            for a in range(8):
                o = apply_op16(act, a, a, vec, dim)
                out = [p.add(q) for p, q in zip(out, o)]
            if th0 is None:
                th0 = out[j]
            for i in range(dim):
                if not out[i].eq(th0 if i == j else C16.zero()):
                    ribbon_scalar = False
        theta.append(th0)
    dd = [S[vac][I].scale(8) for I in range(n)]
    S2 = _mm16(n, S, S)
    Cperm = []
    for i in range(n):
        nz = [j for j in range(n) if not S2[i][j].is_zero()]
        Cperm.append(nz[0] if (len(nz) == 1 and S2[i][nz[0]].eq(C16.one())) else None)
    Sbar = [[S[i][j].conj() for j in range(n)] for i in range(n)]
    return dict(mods=mods, n=n, TR=TR, S=S, Sbar=Sbar, vac=vac, theta=theta,
                dd=dd, S2=S2, Cperm=Cperm, ribbon_scalar=ribbon_scalar)


def verlinde16(L, Sx, pairs=None):
    """N_{ij}^k. pairs=None 이면 전수. ★balancing 은 (i, C(j), k) 를 참조하므로 부분계산 시
    호출측이 그 쌍을 pairs 에 반드시 포함시켜야 한다(누락하면 0 으로 오독됨)."""
    n, vac = L["n"], L["vac"]
    if pairs is None:
        pairs = [(i, j) for i in range(n) for j in range(n)]
    invS = [C16.one().scale(Fr(1, 1) / Sx[vac][Lx].c[0]) for Lx in range(n)]
    Sc = [[Sx[i][j].conj() for j in range(n)] for i in range(n)]
    Nf = {}
    ok = True
    for (i, j) in pairs:
        pre = [Sx[i][Lx].mul(Sx[j][Lx]).mul(invS[Lx]) for Lx in range(n)]
        for k in range(n):
            acc = C16.zero()
            for Lx in range(n):
                if pre[Lx].is_zero():
                    continue
                acc = acc.add(pre[Lx].mul(Sc[k][Lx]))
            cc = acc.c
            if any(cc[t] != 0 for t in range(1, 8)) or cc[0].denominator != 1 or cc[0] < 0:
                ok = False
            Nf[(i, j, k)] = int(cc[0]) if (all(cc[t] == 0 for t in range(1, 8))
                                           and cc[0].denominator == 1) else None
    return Nf, ok


def st3_16(L, Sx):
    n = L["n"]
    T = [[(L["theta"][i] if i == j else C16.zero()) for j in range(n)] for i in range(n)]
    S2 = _mm16(n, Sx, Sx)
    Cx = []
    for i in range(n):
        nz = [j for j in range(n) if not S2[i][j].is_zero()]
        Cx.append(nz[0] if len(nz) == 1 else None)
    if any(c is None for c in Cx):
        return False, None, None
    ST = _mm16(n, Sx, T)
    ST3 = _mm16(n, _mm16(n, ST, ST), ST)
    X = [[ST3[i][Cx[j]] for j in range(n)] for i in range(n)]   # (ST)³·(S²)⁻¹
    lam = None
    ok = True
    for i in range(n):
        for j in range(n):
            if i == j:
                if lam is None:
                    lam = X[i][j]
                elif not X[i][j].eq(lam):
                    ok = False
            elif not X[i][j].is_zero():
                ok = False
    return ok, lam, X


def defect_perm(L, X):
    """X 가 순열행렬이면 그 순열을 반환."""
    n = L["n"]
    p = []
    for i in range(n):
        nz = [j for j in range(n) if not X[i][j].is_zero()]
        if len(nz) != 1 or not X[i][nz[0]].eq(C16.one()):
            return None
        p.append(nz[0])
    return p


# ══════════════════════════════════════════════════════════════════════════
def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "dtw-d4-mu4-ribbon/v1",
           "_note": ("D^ω(D₄) μ₄ 층 ribbon-gap 폐합 — 근본원인=S 켤레 규약(ω-보정 불필요). "
                     "TrackHE19 P2 'ribbon-gap' 해석 정정·철회. 관측·seal 아님·module 0·root 불변.")}

    # ── A. balancing 지표 규약 확정 (SU(3)₁ 독립 오라클) ──────────────
    F3, m3, Sh3, d3, th3, Nf3, C3 = _lie_mtc([[2, -1], [-1, 2]], [Fr(1), Fr(1)], 1, 36)
    R["A_su31_rank3"] = (m3 == 3)
    R["A_su31_non_selfdual"] = (C3 == [0, 2, 1])
    ok3, _lam3 = _mat3(F3, m3, Sh3, th3)
    R["A_su31_ST3_holds"] = ok3
    R["A_su31_formA_holds"] = _balancing(F3, m3, Sh3, th3, d3, Nf3, C3, True)
    R["A_su31_formB_fails"] = (not _balancing(F3, m3, Sh3, th3, d3, Nf3, C3, False))
    # ★teeth: 자기쌍대(Fib=(G₂)₁)에서는 A/B 판별 불가
    Ff, mf, Shf, df, thf, Nff, Cf = _lie_mtc([[2, -1], [-3, 2]], [Fr(1), Fr(1, 3)], 1, 60)
    R["A_fib_selfdual"] = (Cf == [0, 1])
    fibA = _balancing(Ff, mf, Shf, thf, df, Nff, Cf, True)
    fibB = _balancing(Ff, mf, Shf, thf, df, Nff, Cf, False)
    R["A_teeth_selfdual_blind"] = (fibA and fibB)      # 둘 다 통과 = 판별 불가
    out["convention"] = {
        "determined_on": "SU(3)₁ (Kac-Peterson, 비자기쌍대 C=[0,2,1])",
        "verdict": "form A — D·S_ij = Σ_k N_{i,j*}^k d_k θ_k/(θ_iθ_j)",
        "teeth": "자기쌍대 Fib=(G₂)₁ 에서는 form A/B 둘 다 통과 ⟹ 자기쌍대 검증은 blind",
        "honesty": "문헌 인용 아님 — 독립 구성 MTC 에서 결정",
    }

    # ── B. μ₄(P₄=1) 층 재구성 + 결함 측정 ────────────────────────────
    W4_of, slant, P4_of = build_cocycles()
    thA = slant(W4_of(1))
    R["B_P4_is_1"] = (P4_of(W4_of(1)) == 1)
    L1 = mu4_layer(thA, quick=quick)
    n = L1["n"]
    R["B_n22"] = (n == 22)
    R["B_sumdim2_64"] = (sum(d * d for _, d, _ in L1["mods"]) == 64)
    R["B_ribbon_scalar"] = L1["ribbon_scalar"]
    R["B_S_symmetric"] = all(L1["S"][i][j].eq(L1["S"][j][i]) for i in range(n) for j in range(n))
    SSd = _mm16(n, L1["S"], L1["S"], conjB=True)
    R["B_S_unitary"] = all(SSd[i][j].eq(C16.one() if i == j else C16.zero())
                           for i in range(n) for j in range(n))
    R["B_S2_is_perm_C"] = (all(c is not None for c in L1["Cperm"])
                           and all(L1["Cperm"][L1["Cperm"][i]] == i for i in range(n)))
    R["B_C_nontrivial"] = (L1["Cperm"] != list(range(n)))
    R["B_dims_1_8_2_14"] = (sorted(int(d.c[0]) for d in L1["dd"]) == [1] * 8 + [2] * 14)
    okS, _lamS, XS = st3_16(L1, L1["S"])
    R["B_orig_ST3_fails"] = (not okS)
    pdef = defect_perm(L1, XS)
    R["B_defect_is_permutation"] = (pdef is not None)
    R["B_defect_equals_C"] = (pdef == L1["Cperm"])
    out["defect"] = {
        "measurement": "(ST)³·(S²)⁻¹ = C 정확 — 즉 (ST)³ = I 이고 S² = C ≠ I",
        "nature": "위상(diagonal)이 아니라 **순열**, 그것도 charge conjugation",
        "why_eps_search_failed": "대각 ε-위상 보정은 순열 결함을 만들 수 없다",
    }

    # ── C. 3중 독립 심판 ─────────────────────────────────────────────
    # ① SL(2,ℤ)
    okSb, lamSb, _XSb = st3_16(L1, L1["Sbar"])
    R["C1_corrected_ST3_holds"] = okSb
    R["C1_lam_is_one"] = (lamSb is not None and lamSb.eq(C16.one()))
    # ② balancing form A (N 은 켤레-불변 → S 로 계산해도 동일)
    bal_idx = list(range(n)) if not quick else list(range(0, n, 3))
    need = set()
    for i in bal_idx:
        for j in bal_idx:
            need.add((i, j))
            need.add((i, L1["Cperm"][j]))          # ★balancing 이 참조하는 쌍 필수 포함
    pairs = None if not quick else sorted(need)
    NfL, verl_ok = verlinde16(L1, L1["S"], pairs)
    R["C2_verlinde_nonneg_int"] = verl_ok
    NfLb, _ = verlinde16(L1, L1["Sbar"], pairs)
    R["C2_N_conj_invariant"] = all(NfL[t] == NfLb[t] for t in NfL)

    def bal16(Sx):
        idx = bal_idx
        for i in idx:
            for j in idx:
                jj = L1["Cperm"][j]
                acc = C16.zero()
                for k in range(n):
                    nk = NfL.get((i, jj, k))
                    if nk:
                        acc = acc.add(L1["theta"][k].scale(nk * L1["dd"][k].c[0]))
                ti = ZP16[(-_z16pow(L1["theta"][i])) % 16]
                tj = ZP16[(-_z16pow(L1["theta"][j])) % 16]
                if not Sx[i][j].scale(8).eq(acc.mul(ti).mul(tj)):
                    return False
        return True
    R["C2_formA_selects_corrected"] = (bal16(L1["Sbar"]) and not bal16(L1["S"]))
    # ③ Gauss 합 — S 규약 미사용
    pplus = C16.zero()
    pminus = C16.zero()
    for i in range(n):
        d2 = L1["dd"][i].mul(L1["dd"][i])
        pplus = pplus.add(d2.mul(L1["theta"][i]))
        pminus = pminus.add(d2.mul(L1["theta"][i].conj()))
    R["C3_gauss_pp_pm_D2"] = pplus.mul(pminus).eq(C16.one().scale(64))
    R["C3_gauss_pplus_eq_D"] = pplus.eq(C16.one().scale(8))
    R["C3_gauss_matches_lam"] = (lamSb is not None and pplus.scale(Fr(1, 8)).eq(lamSb))
    out["arbiters"] = {
        "1_SL2Z": "(S̄T)³ = λS̄², λ = 1",
        "2_balancing_formA": "S̄ 선택 (S 는 불성립)",
        "3_gauss_sum": "p₊ = 8 = D · p₊p₋ = 64 = D² · p₊/D = 1 = λ (S 규약 미사용)",
        "verdict": "★3중 독립 심판이 모두 수정 규약 S̄ 를 선택",
    }

    # ── D. 구조적 확증: double ⟹ c ≡ 0 mod 8 ─────────────────────────
    R["D_double_c_zero_mod8"] = (lamSb is not None and lamSb.eq(C16.one())
                                 and pplus.eq(C16.one().scale(8)))
    out["central_charge"] = {
        "p_plus_over_D": "1 = e^{2πi·0/8} ⟹ c ≡ 0 (mod 8)",
        "structural": "Drinfeld double(=center)은 반드시 c≡0 — 수정 데이터가 그 값을 준다",
        "role": "확증용 — 규약은 ①②③ 이 이미 독립 확정(이 사실로 정한 것 아님)",
    }

    # ── E. blind-spot 국소화: S̄ = S∘C ────────────────────────────────
    R["E_Sbar_equals_S_compose_C"] = all(
        L1["Sbar"][i][j].eq(L1["S"][i][L1["Cperm"][j]]) for i in range(n) for j in range(n))
    # S-단독 게이트는 S̄ 에서도 전부 성립 = 켤레-blind 증명
    SSdb = _mm16(n, L1["Sbar"], L1["Sbar"], conjB=True)
    R["E_corrected_passes_all_S_gates"] = (
        all(L1["Sbar"][i][j].eq(L1["Sbar"][j][i]) for i in range(n) for j in range(n))
        and all(SSdb[i][j].eq(C16.one() if i == j else C16.zero())
                for i in range(n) for j in range(n))
        and L1["Sbar"][L1["vac"]][L1["vac"]].eq(C16.one().scale(Fr(1, 8))))
    from qf_witness.observe.dtw_d4_full_modular_observe import (
        build_modules as build_mod2, compute_h3 as ch3, C8, conj as gconj2)
    tri_idx2, _rows2, _dz, _db, h3b = ch3()
    samples = [0, h3b[0]] if quick else [0, h3b[0], h3b[0] ^ h3b[1]]
    mu2_all_identity = True
    for v in samples:
        m2 = build_mod2(v, tri_idx2)
        n2 = len(m2)
        TR2 = []
        for (lab, dim, act) in m2:
            t = {}
            for g in range(8):
                for x in range(8):
                    s = C8.zero()
                    for col, entries in act[(g, x)].items():
                        for (row, cf) in entries:
                            if row == col:
                                s = s + cf
                    t[(g, x)] = s
            TR2.append(t)
        S_2 = [[C8.zero() for _ in range(n2)] for _ in range(n2)]
        for I in range(n2):
            for J in range(n2):
                acc = C8.zero()
                for g in range(8):
                    for h in range(8):
                        acc = acc + TR2[I][(gconj2(g, h), h)] * TR2[J][(h, g)]
                S_2[I][J] = acc.scale(Fr(1, 8))
        # S 실수 ⟺ C = 항등
        sreal = all(S_2[i][j] == S_2[i][j].conj() for i in range(n2) for j in range(n2))
        S2_2 = [[sum((S_2[i][k] * S_2[k][j] for k in range(n2)), C8.zero())
                 for j in range(n2)] for i in range(n2)]
        C2p = [next(j for j in range(n2) if not S2_2[i][j].is_zero()) for i in range(n2)]
        if not (sreal and C2p == list(range(n2))):
            mu2_all_identity = False
    R["E_mu2_C_identity"] = mu2_all_identity
    out["blind_spot"] = {
        "identity": "S̄ = S∘C — 켤레는 charge conjugation 라벨치환과 같다",
        "consequence": "S-단독 게이트(대칭·유니터리·S²=C·Verlinde·dims·S_vac)는 전부 켤레-blind",
        "why_mu2_passed": "μ₂ 층은 C = 항등(전 anyon 자기쌍대) ⟹ S 실수 ⟹ 규약 무해",
        "why_mu4_exposed": "μ₄ ζ₁₆ 층 = 첫 비자기쌍대 층(C 는 6 호환) ⟹ 결함 = C 로 노출",
    }

    # ── F. P₄=3 층 동일 폐합 ─────────────────────────────────────────
    if not quick:
        thB = slant(W4_of(0))
        R["F_P4_is_3"] = (P4_of(W4_of(0)) == 3)
        L3 = mu4_layer(thB)
        okS3, _, _ = st3_16(L3, L3["S"])
        okSb3, lamSb3, _ = st3_16(L3, L3["Sbar"])
        R["F_p3_orig_fails"] = (not okS3)
        R["F_p3_corrected_holds"] = okSb3
        R["F_p3_lam_one"] = (lamSb3 is not None and lamSb3.eq(C16.one()))
        R["F_p3_C_nontrivial"] = (L3["Cperm"] != list(range(L3["n"])))

    # ── G. 폐합 판정 ─────────────────────────────────────────────────
    R["G_ribbon_needs_no_omega_correction"] = (L1["ribbon_scalar"] and okSb
                                               and R["C1_lam_is_one"])
    out["closure"] = {
        "resolved": ("★z = Σδ_a⊗a 는 μ₄ 층에서도 정확한 ribbon — quasi-Hopf ω-보정 **불필요**"),
        "root_cause": "S-행렬 문자공식의 켤레 규약(수정 S = S̄ = S∘C)",
        "retraction": ("TrackHE19 P2 dtw_d4_zeta16_observe 의 'ribbon-gap = μ₄ 구조적 실패' 해석을 "
                       "**규약 아티팩트로 판정·철회** (갭 현상 자체는 실재했음)"),
        "T_gauge": "확정 — T = diag(θ), θ_I = z 의 고윳값(별도 게이지 자유도 불필요)",
    }

    # ── teeth ────────────────────────────────────────────────────────
    R["teeth_orig_convention_breaks"] = R["B_orig_ST3_fails"]
    R["teeth_selfdual_cannot_decide"] = R["A_teeth_selfdual_blind"]
    R["teeth_defect_not_diagonal"] = (pdef is not None and pdef != list(range(n)))

    ok = bool(all(v for v in R.values() if v is not None))
    out["checks"] = R
    out["scope_honesty"] = {
        "delivered": ("μ₄ ribbon-gap 폐합(근본원인=켤레 규약·ω-보정 불필요) + balancing 규약 "
                      "독립 확정 + blind-spot 국소화 + P₄=1,3 양 층 폐합"),
        "retracts": "dtw_d4_zeta16_observe 의 'ω-보정 필요' 해석 (본 관측이 정정)",
        "not_claimed": ("braiding 실봉인·F/R-symbol·μ₈ 층 S·T·"
                        "form A 의 문헌 인용(=SU(3)₁ 에서 결정한 것)"),
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "DTW-D4-MU4-RIBBON.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("D^ω(D₄) μ₄ ribbon-gap 폐합 (exact — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  ★결함 = (ST)³·(S²)⁻¹ = C (순열·charge conjugation) — 위상 보정으로 불가", flush=True)
        print("  ★3중 독립 심판(SL(2,ℤ)·balancing formA·Gauss합) 전부 수정 S̄ 선택·λ=1", flush=True)
        print("  ★blind-spot: S̄=S∘C · μ₂ 층은 C=항등이라 규약 무해 — μ₄ 가 첫 비자기쌍대 층",
              flush=True)
        print("  ★폐합: ω-보정 불필요 — 'ribbon-gap' 해석 철회·정정", flush=True)
        print("  → .pgf/proofs/DTW-D4-MU4-RIBBON.json", flush=True)
    print(f"dtw_d4_mu4_ribbon_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
