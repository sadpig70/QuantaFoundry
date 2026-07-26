#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dtw_z2_5_full_modular_observe — ★**D^ω(ℤ₂⁵) 완전 184×184 twisted S·T**
(관측, seal 아님). [[dtw_z2_5_radical1_observe]](TrackHE19 P5)가 "완전 184×184 twisted S·T =
미완(규모)"으로 명시 유보한 축을 **완결**한다. v20 §4·§143 명시 후보.

★규모 돌파의 열쇠 = **구조 환원**(전 행렬 브루트포스 회피). G 아벨이므로 C(a)=G 이고, flux a 의
slant β_a 의 commutator form B_a(교대형)의 **radical R_a** 위에서 사영 irrep 이 스칼라가 된다:
  **χ_{(a,μ)}(h) = d_a·μ(h)·[h ∈ R_a], 그 외 0** (d_a = 2^{r_a/2}, r_a = rank B_a)
⟹ 184×184 S 가 **32개 flux 의 μ₄-값 사영문자만으로** 닫힌 형태로 결정된다.
★이 문자공식은 **가정하지 않고 C축에서 유도표현 명시 구성으로 검증**한다.

관측 7축(전 산술 GF(2)/ℤ[i] 정확 — int64, 부동소수 없음):
  A. **census 독립 재계산**: agent01 cocycle ω(x,y,z)=(−1)^{x₅y₁z₂+x₅y₃z₄} 의 d³ω=0 ·
     rank 분포 **{0:1, 2:15, 4:16}** · |R_a| 분포 {32:1, 8:15, 2:16} · anyon **184** · Σd²=**1024**.
  B. ★**구조 사실 자체검증(가정 배제)**: **a ∈ R_a 전수 32**(T-행렬 well-defined 의 전제) ·
     ★**b ∈ R_a ⟺ a ∈ R_b 전수 1024 쌍**(S 대칭·지지집합 정합의 전제) · |R_a|=|G|/2^{r_a} 전수.
  C. ★★**유도표현 명시 구성 → 문자공식 교차검증**: 극대 등방 L ⊇ R_a 기계탐색 ·
     β_a|_L 사영문자 ψ 전수 · **ρ(g)_{t',t} = i^{2β(g,t)+2β(t',l)}ψ(l), l=g+t+t'** ·
     **사영관계 ρ(g)ρ(h)=(−1)^{β(g,h)}ρ(g+h) 를 32²=1024 쌍 전수**(rank 0/2/4 대표) ·
     **전 32 flux 에서 χ(g)=d·μ(g)·[g∈R_a]·그 외 0 정확 일치** · **서로 다른 문자 = |R_a| 개**.
  D. ★★**완전 184×184 S·T**: S̃_{(a,μ),(b,ν)} = χ̄_{(a,μ)}(b)·χ̄_{(b,ν)}(a) (S=S̃/32) —
     S 대칭 · **S̃S̃† = 1024·I**(유니터리) · **S̃² = 1024·C** · **C = 항등(전 anyon 자기쌍대)** ·
     S̃ vacuum 행 = 양자차원 · dims **{1×32, 2×120, 4×32}** ·
     **Verlinde 184³ = 6,229,504 전수 비음정수** · T=diag(θ), θ=μ(a) ·
     **(S̃T)³ = 32·S̃² ⟹ λ = 1**.
  E. ★**켤레 규약 — [[dtw_d4_mu4_ribbon_observe]] 기준의 예측 검증**: 그 관측이 확립한
     "켤레 규약이 문제되는 것은 **C ≠ 항등**일 때뿐(S̄ = S∘C)"이 여기서 **C=항등 ⟹ S 실수**를
     **예측**한다 — 실제로 **S̃ 허수부 전부 0** 확인. ⟹ 본 층은 규약-무해(blind)이고,
     그 사실이 **기준의 독립 예측 성공**이다.
  F. ★**Gauss 합·중심전하**: p₊ = Σd²θ = **32 = D** · p₊p₋ = **1024 = D²** · **p₊/D = 1 = λ**
     ⟹ **c ≡ 0 (mod 8)** — Drinfeld double 필연값과 일치(구조적 확증).
  G. ★**Rep(ℤ₂⁵) Tannakian 부분범주 실증**: flux-0 섹터 32개는 전부 **d=1·θ=1(보손)** 이고
     **S-부분행렬이 전 성분 동일(rank 1·완전 퇴화)** ⟹ Tannakian. pointed/부분범주 퇴화
     스펙트럼에 배치: [[su3_3_mtc_observe]] SU(3)₃(완전 퇴화·⊠-분해 불가) ↔
     [[dtw_d4_mu4_ribbon_observe]] 경유 [[g2_1_mtc_observe]] SU(2)₃(비퇴화·분해 가능).

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - **cocycle 은 agent01 명시 대표 1개** — H³(ℤ₂⁵,μ₂) 35 클래스 전체의 modular data 는 범위 밖.
  - H³ 차원 35 판정은 선행 [[dtw_z2_5_radical1_observe]] 소관(여기서 재주장하지 않음).
  - modular data 수준 관측 — braiding 게이트 실봉인·F/R-symbol 무주장.
  - numpy 는 **int64 정확 산술**로만 사용(부동소수 없음) — |S̃|≤16·Verlinde 중간값 <10⁶.

사용: python -m qf_witness.observe.dtw_z2_5_full_modular_observe [--quick]
"""
from __future__ import annotations
import sys
import json
from collections import Counter

import numpy as np

from qf_witness.observe.dtw_z2_5_radical1_observe import N, NG, omega, slant, comm_rank

IR = (1, 0, -1, 0)          # Re(i^k)
II = (0, 1, 0, -1)          # Im(i^k)


# ══════════════════════════════════════════════════════════════════════════
# 구조 유틸
# ══════════════════════════════════════════════════════════════════════════
def bform(av):
    b = slant(av)
    return lambda g, h: (b(g, h) ^ b(h, g)) & 1


def radical(av):
    Bf = bform(av)
    return [h for h in range(NG) if all(Bf(h, k) == 0 for k in range(NG))]


def gf2_basis(elems):
    gens = []
    for h in elems:
        v = h
        for b0 in gens:
            v = min(v, v ^ b0)
        if v:
            gens.append(v)
            gens.sort(reverse=True)
    return gens


def span(gens):
    S = {0}
    for g in gens:
        S |= {s ^ g for s in S}
    return sorted(S)


def max_isotropic(av):
    """R_a 를 포함하는 극대 등방 부분군 L (B_a|_L ≡ 0) — 탐욕 확장(기계탐색)."""
    Bf = bform(av)
    gens = gf2_basis(radical(av))
    cur = set(span(gens))
    changed = True
    while changed:
        changed = False
        for g in range(1, NG):
            if g in cur:
                continue
            if all(Bf(g, x) == 0 for x in cur):
                gens.append(g)
                cur = set(span(gens))
                changed = True
                break
    return sorted(cur)


def proj_characters(av, sub):
    """β_a|_sub(대칭) 위의 μ₄-값 사영문자 ψ 전수: ψ(x+y)=i^{2β(x,y)}ψ(x)ψ(y).

    ★생성원 제약: x+x=0 ⟹ 2ψ(x)+2β(x,x) ≡ 0 (mod 4) ⟹ ψ(x) ≡ β(x,x) (mod 2)
    → 생성원당 2 선택(4 아님). 구성 후 **전 쌍 정합성 재확인**(자체검증).
    """
    beta = slant(av)
    gens = gf2_basis(sub)
    k = len(gens)
    out = []
    for mask in range(1 << k):
        vals = [(beta(g, g) + 2 * ((mask >> i) & 1)) % 4 for i, g in enumerate(gens)]
        m = {0: 0}
        for idx, g in enumerate(gens):
            new = {}
            for h, mh in m.items():
                new[h ^ g] = (mh + vals[idx] + 2 * beta(h, g)) % 4
            m.update(new)
        if all((m[x ^ y] - m[x] - m[y] - 2 * beta(x, y)) % 4 == 0 for x in sub for y in sub):
            out.append(m)
    return out


def induced_rep(av, L, psi):
    """유도표현 ρ = Ind_L^G ψ (ℤ[i] 행렬)."""
    beta = slant(av)
    T = []
    seen = set()
    for g in range(NG):
        if g not in seen:
            T.append(g)
            seen |= {g ^ x for x in L}
    d = len(T)
    idx = {}
    for ti, t in enumerate(T):
        for x in L:
            idx[t ^ x] = ti

    def rho(g):
        M = [[(0, 0)] * d for _ in range(d)]
        for tj, t in enumerate(T):
            gt = g ^ t
            ti = idx[gt]
            tp = T[ti]
            l = gt ^ tp
            e = (2 * beta(g, t) + 2 * beta(tp, l) + psi[l]) % 4
            row = list(M[ti])
            row[tj] = (IR[e], II[e])
            M[ti] = row
        return M
    return d, rho


def _mmul(A, B, d):
    C = []
    for i in range(d):
        row = []
        for j in range(d):
            sr = si = 0
            for k in range(d):
                ar, ai = A[i][k]
                br, bi = B[k][j]
                if (ar or ai) and (br or bi):
                    sr += ar * br - ai * bi
                    si += ar * bi + ai * br
            row.append((sr, si))
        C.append(row)
    return C


# ══════════════════════════════════════════════════════════════════════════
def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "dtw-z2-5-full-modular/v1",
           "_note": ("D^ω(ℤ₂⁵) 완전 184×184 twisted S·T — 구조 환원(radical 위 스칼라)으로 "
                     "규모 돌파·문자공식은 유도표현 명시 구성으로 검증. "
                     "관측·seal 아님·module 0·root 불변.")}

    # ── A. census 독립 재계산 ────────────────────────────────────────────
    step = 2 if quick else 1
    ok = True
    for a in range(0, NG, step):
        for b in range(0, NG, step):
            for c in range(NG):
                for d in range(NG):
                    if (omega(b, c, d) ^ omega(a ^ b, c, d) ^ omega(a, b ^ c, d)
                            ^ omega(a, b, c ^ d) ^ omega(a, b, c)):
                        ok = False
                        break
                if not ok:
                    break
            if not ok:
                break
        if not ok:
            break
    R["A_cocycle"] = ok
    RAD = [radical(a) for a in range(NG)]
    ranks = [comm_rank(a) for a in range(NG)]
    rdist = Counter(ranks)
    R["A_rank_dist"] = (rdist.get(0) == 1 and rdist.get(2) == 15 and rdist.get(4) == 16)
    R["A_radical_size_matches"] = all(len(RAD[a]) == (NG >> ranks[a]) for a in range(NG))
    n_anyon = sum(len(RAD[a]) for a in range(NG))
    R["A_anyons_184"] = (n_anyon == 184)

    # ── B. 구조 사실 자체검증 ────────────────────────────────────────────
    R["B_a_in_rad_a"] = all(a in RAD[a] for a in range(NG))
    RS = [set(r) for r in RAD]
    R["B_rad_reciprocity"] = all((b in RS[a]) == (a in RS[b])
                                 for a in range(NG) for b in range(NG))

    # ── anyon 목록 ───────────────────────────────────────────────────────
    ANY = []          # (flux, {h: μ 지수}, d)
    for a in range(NG):
        mus = proj_characters(a, RAD[a])
        d = 1 << (ranks[a] // 2)
        mus.sort(key=lambda m: tuple(m[h] for h in RAD[a]))
        for m in mus:
            ANY.append((a, m, d))
    n = len(ANY)
    R["B_mu_count_matches_radical"] = (n == 184 and all(
        sum(1 for x in ANY if x[0] == a) == len(RAD[a]) for a in range(NG)))
    dims = [x[2] for x in ANY]
    R["B_dims_multiset"] = (Counter(dims) == Counter({1: 32, 2: 120, 4: 32}))
    R["B_sum_d2_1024"] = (sum(d * d for d in dims) == 1024)
    out["census"] = {"anyons": n, "rank_dist": dict(sorted(rdist.items())),
                     "dims": {"1": 32, "2": 120, "4": 32}, "D2": 1024,
                     "formula": "Σ_a |G|/2^{r_a} = 32 + 15·8 + 16·2 = 184"}

    # ── C. 유도표현 명시 구성 → 문자공식 교차검증 ────────────────────────
    reps = [next(a for a in range(NG) if ranks[a] == r) for r in (0, 2, 4)]
    proj_ok = True
    for a in reps:
        L = max_isotropic(a)
        beta = slant(a)
        for psi in proj_characters(a, L):
            d, rho = induced_rep(a, L, psi)
            RH = [rho(g) for g in range(NG)]
            for g in range(NG):
                for h in range(NG):
                    lhs = _mmul(RH[g], RH[h], d)
                    s = (2 * beta(g, h)) % 4
                    sr, si = IR[s], II[s]
                    rhs = [[(sr * x - si * y, sr * y + si * x) for (x, y) in row]
                           for row in RH[g ^ h]]
                    if lhs != rhs:
                        proj_ok = False
    R["C_projective_relation_exhaustive"] = proj_ok

    # 전 32 flux: 유도 문자 집합 == 공식 문자 집합
    formula_ok = True
    count_ok = True
    flux_iter = reps if quick else range(NG)
    for a in flux_iter:
        L = max_isotropic(a)
        d_exp = 1 << (ranks[a] // 2)
        chars = set()
        for psi in proj_characters(a, L):
            d, rho = induced_rep(a, L, psi)
            ch = []
            for g in range(NG):
                M = rho(g)
                ch.append((sum(M[i][i][0] for i in range(d)),
                           sum(M[i][i][1] for i in range(d))))
            chars.add(tuple(ch))
        want = set()
        for (fa, m, dd_) in ANY:
            if fa != a:
                continue
            ch = []
            for g in range(NG):
                if g in m:
                    e = m[g]
                    ch.append((dd_ * IR[e], dd_ * II[e]))
                else:
                    ch.append((0, 0))
            want.add(tuple(ch))
        if chars != want:
            formula_ok = False
        if len(chars) != len(RAD[a]) or d_exp != (1 << (ranks[a] // 2)):
            count_ok = False
    R["C_character_formula_matches"] = formula_ok
    R["C_distinct_chars_eq_radical"] = count_ok
    out["character_formula"] = {
        "claim": "χ_{(a,μ)}(h) = d_a·μ(h)·[h ∈ R_a], 그 외 0",
        "status": "★가정 아님 — 유도표현 Ind_L^G ψ 명시 구성으로 검증(사영관계 1024 쌍 전수)",
        "scale_key": "이 환원이 184×184 를 32 flux 의 μ₄ 사영문자로 닫는다",
    }

    # ── D. 완전 184×184 S·T ──────────────────────────────────────────────
    Sre = np.zeros((n, n), dtype=np.int64)
    Sim = np.zeros((n, n), dtype=np.int64)
    for i, (a, mu, da) in enumerate(ANY):
        for j, (b, nu, db) in enumerate(ANY):
            if b not in mu:
                continue
            e = (-(mu[b] + nu[a])) % 4
            Sre[i, j] = da * db * IR[e]
            Sim[i, j] = da * db * II[e]
    R["D_S_symmetric"] = (np.array_equal(Sre, Sre.T) and np.array_equal(Sim, Sim.T))
    vac = next(i for i, (a, mu, d) in enumerate(ANY)
               if a == 0 and all(v == 0 for v in mu.values()))
    R["D_vac_row_is_dims"] = (np.array_equal(Sre[vac], np.array(dims, dtype=np.int64))
                              and not Sim[vac].any())

    def cmm(Ar, Ai, Br, Bi):
        return Ar @ Br - Ai @ Bi, Ar @ Bi + Ai @ Br
    Hr, Hi = cmm(Sre, Sim, Sre.T, -Sim.T)
    R["D_S_unitary"] = (np.array_equal(Hr, 1024 * np.eye(n, dtype=np.int64)) and not Hi.any())
    S2r, S2i = cmm(Sre, Sim, Sre, Sim)
    Cperm = []
    okC = True
    for i in range(n):
        nz = np.nonzero(S2r[i] | S2i[i])[0]
        if len(nz) != 1 or S2r[i, nz[0]] != 1024 or S2i[i, nz[0]] != 0:
            okC = False
            break
        Cperm.append(int(nz[0]))
    R["D_S2_is_1024C"] = okC
    R["D_C_involution"] = (okC and all(Cperm[Cperm[i]] == i for i in range(n)))
    R["D_C_identity_all_selfdual"] = (okC and Cperm == list(range(n)))
    theta = [mu[a] for (a, mu, d) in ANY]
    Tr = np.array([IR[t] for t in theta], dtype=np.int64)
    Ti = np.array([II[t] for t in theta], dtype=np.int64)
    STr, STi = Sre * Tr - Sim * Ti, Sre * Ti + Sim * Tr
    Ar, Ai = cmm(STr, STi, STr, STi)
    Ar, Ai = cmm(Ar, Ai, STr, STi)
    kr = int(Ar[vac, Cperm[vac]]) // 1024
    ki = int(Ai[vac, Cperm[vac]]) // 1024
    R["D_ST3_prop_S2"] = (np.array_equal(Ar, kr * S2r - ki * S2i)
                          and np.array_equal(Ai, kr * S2i + ki * S2r))
    R["D_lambda_one"] = (kr == 32 and ki == 0)      # λ = κ/32 = 1
    # Verlinde 전수(quick=부분표집)
    dvec = np.array(dims, dtype=np.int64)
    verl_ok = True
    vidx = range(n) if not quick else range(0, n, 8)
    for i in vidx:
        Pr = Sre * Sre[i] - Sim * Sim[i]
        Pi = Sre * Sim[i] + Sim * Sre[i]
        Pr, Pi = Pr // dvec, Pi // dvec
        Nr = Pr @ Sre.T + Pi @ Sim.T
        Ni = Pi @ Sre.T - Pr @ Sim.T
        if Ni.any() or (Nr % 1024).any() or (Nr < 0).any():
            verl_ok = False
    R["D_verlinde_nonneg_int"] = verl_ok
    out["modular_data"] = {
        "rank": 184, "D": 32, "S_normalization": "S = S̃/32 (S_vac,vac = 1/32)",
        "gates": "S=Sᵀ · S̃S̃†=1024I · S̃²=1024C · C=항등 · Verlinde 184³ 비음정수 · (S̃T)³=32S̃²",
        "verlinde_triples": n ** 3,
        "theta_multiset": {str(k): v for k, v in sorted(Counter(theta).items())},
    }

    # ── E. 켤레 규약 — 기준의 예측 검증 ─────────────────────────────────
    R["E_S_real"] = (not Sim.any())
    R["E_criterion_prediction"] = (R["D_C_identity_all_selfdual"] and R["E_S_real"])
    out["convention"] = {
        "criterion": "S̄ = S∘C — 켤레 규약이 문제되는 것은 C ≠ 항등일 때뿐 "
                     "(dtw_d4_mu4_ribbon_observe 에서 확립)",
        "here": "C = 항등(전 184 anyon 자기쌍대) ⟹ S 실수 예측 → 실제 S̃ 허수부 전부 0",
        "verdict": "★본 층은 규약-무해(blind) — 기준의 독립 예측 성공",
    }

    # ── F. Gauss 합·중심전하 ────────────────────────────────────────────
    pr = pi = 0
    qr = qi = 0
    for d, t in zip(dims, theta):
        pr += d * d * IR[t]
        pi += d * d * II[t]
        qr += d * d * IR[(-t) % 4]
        qi += d * d * II[(-t) % 4]
    R["F_pplus_eq_D"] = (pr == 32 and pi == 0)
    R["F_pp_pm_D2"] = (pr * qr - pi * qi == 1024 and pr * qi + pi * qr == 0)
    R["F_c_zero_mod8"] = (R["F_pplus_eq_D"] and R["D_lambda_one"])
    out["central_charge"] = {"p_plus": "32 = D", "p_plus_over_D": "1 = e^{2πi·0/8}",
                             "c_mod_8": 0, "structural": "Drinfeld double 필연값과 일치"}

    # ── G. Rep(ℤ₂⁵) Tannakian 부분범주 ──────────────────────────────────
    P = [i for i, (a, mu, d) in enumerate(ANY) if a == 0]
    R["G_flux0_32_sectors"] = (len(P) == 32)
    R["G_flux0_all_dim1_boson"] = all(dims[i] == 1 and theta[i] == 0 for i in P)
    sub = Sre[np.ix_(P, P)]
    R["G_pointed_S_rank1_degenerate"] = bool((sub == sub[0, 0]).all() and sub[0, 0] == 1)
    out["tannakian"] = {
        "subcategory": "flux-0 섹터 32개 = Rep(ℤ₂⁵)",
        "evidence": "전부 d=1·θ=1(보손) + S-부분행렬 전 성분 동일(rank 1·완전 퇴화)",
        "verdict": "★Tannakian — 모듈러 부분범주 아님",
        "spectrum": ("완전 퇴화 극(SU(3)₃·본 층) ↔ 비퇴화 극(SU(2)₃ pointed, ⊠-분해 가능) — "
                     "같은 판정기준의 양 끝"),
    }

    # ── teeth ───────────────────────────────────────────────────────────
    R["teeth_256_refuted"] = (n_anyon != 256)          # flux-무관 rank 가정 오류
    R["teeth_rank_varies"] = (len(set(ranks)) > 1)
    R["teeth_T_needs_a_in_rad"] = R["B_a_in_rad_a"]

    ok_all = bool(all(R.values()))
    out["checks"] = R
    out["scope_honesty"] = {
        "delivered": ("완전 184×184 S·T + 전 modular 게이트(유니터리·S²=C·Verlinde 184³ 전수) + "
                      "문자공식 유도표현 검증 + Tannakian 부분범주 실증"),
        "completes": "dtw_z2_5_radical1_observe 의 '완전 184×184 S = 미완' 유보 해소",
        "not_claimed": ("H³ 35 클래스 전체의 modular data(본 관측=agent01 대표 cocycle 1개) · "
                        "braiding 실봉인 · F/R-symbol · H³ 차원 판정(선행 관측 소관)"),
        "arithmetic": "GF(2)/ℤ[i] 정확 — numpy int64 만 사용(부동소수 없음)",
    }
    out["all_ok"] = ok_all

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "DTW-Z2-5-FULL-MODULAR.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("D^ω(ℤ₂⁵) 완전 184×184 twisted S·T (exact — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  ★규모 돌파 = 구조 환원(χ = d·μ·[∈R_a]) — 유도표현 명시 구성으로 **검증**", flush=True)
        print("  ★S̃S̃†=1024I · S̃²=1024C(C=항등) · Verlinde 184³=6,229,504 전수 · (S̃T)³=32S̃²",
              flush=True)
        print("  ★c≡0 mod 8(p₊=32=D) · Rep(ℤ₂⁵) Tannakian(pointed S rank-1 완전 퇴화)", flush=True)
        print("  → .pgf/proofs/DTW-Z2-5-FULL-MODULAR.json", flush=True)
    print(f"dtw_z2_5_full_modular_observe: all_ok={ok_all}", flush=True)
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
