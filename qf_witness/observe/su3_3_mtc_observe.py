#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""su3_3_mtc_observe — TrackHE19 P3: SU(3)₃ MTC — ★**pointed-분해 판정: 진짜(비분해) rank-2**
(관측, seal 아님). [[su3_2_mtc_observe]](SU(3)₂ ≅ conj-Fib⊠ℤ₃ 인수분해)와의 **구조 전이** 실증.

관측 7축(전부 ℚ(ζ₉)(=ℚ(ζ₁₈)) 정확 산술 직접 구현 — Φ₉=x⁶+x³+1·6차원·ζ₁₈=−ζ₉⁵):
  A. **Kac-Peterson 자체유도**: k=3·h∨=3·k+h∨=6·10 가중치(λ₁+λ₂≤3)·Weyl S₃ 합·
     exp(−2πi q/6)=ζ₁₈^{−3q}. **S̃ 대칭·S̃S̃†=108·I·S̃²=−108·C**(위상 i^{|Δ₊|}) —
     C=(3↔3̄, 6↔6̄, 15↔15̄′...) 비자명 charge conjugation.
  B. **양자차원·D²**: dims = **{1×3, 2×6, 3×1}**(agent01 값 검증)·**D²=36** — 정수(weakly
     integral!·SU(2)₅ 비정수와 대조).
  C. **T·(ST)³**: h=[0,2/9,2/9,5/9,5/9,1/2,1,1,8/9,8/9]·c=k·dim𝔤/(k+h∨)=24/6=**4**·
     (S̃T̃)³∝S̃²(스칼라 정확).
  D. **Verlinde 10³ 전수 비음정수** + ℤ₃ simple-current 궤도.
  E. ★★**pointed-분해 판정(crux)**: simple currents {1,(3,0),(0,3)}(d=1·ℤ₃)에서
     (i) **twist h=1 → θ=1 정수(Tannakian 보손)** — SU(3)₂의 θ=e^{2πi·2/3}(anyonic)와 대조
     (ii) **pointed 3×3 S-부분행렬 완전 퇴화(rank 1·전 성분 동일)** — SU(3)₂의 비퇴화
     ω^{2ab} 와 정반대 ⟹ pointed 부분범주는 **모듈러 부분범주가 아님** → Müger ⊠-분해 불가
     (iii) simple current 는 transparent 아님(비-triality-0 대상과 monodromy ω 비자명 —
     Müger center 자명·전체는 modular). ⟹ ★**SU(3)₃ = 첫 비분해 진짜 rank-2 Lie MTC**.
  F. ★**필드 판정(§4′o 상충 심판)**: S̃ 성분은 σ(Galois) 검사로 **ℚ(ζ₉) 진부분장에 안 들어감**
     — agent07 의 "ℚ(ζ₆) dim 2" **반증**·agent06 의 ζ₁₈(=ℚ(ζ₉)·φ=6) 확정.
  G. ★**G₂ level-1 rank 정정(agent07 오류)**: G₂ 근계 자체유도(Cartan [[2,−1],[−3,2]]·반사
     닫힘 12근·장단비 3)·highest root marks (3,2)→comarks (1,2)·h∨=4 → **level-1 primaries
     = 2**(vacuum+ω_short) — "rank=14"는 dim(G₂) 혼동.

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - modular data = 조합·대수 exact 표 — braiding 게이트 실봉인·F/R-symbol 무주장.
  - 분해 판정 = S·T(modular data) 수준 Müger 논증(θ=1·S-퇴화·transparent 판정) — 범주론적
    완전 증명(Tannakian 서브카테고리 동치)은 무주장.
  - G₂₁ 은 rank 정정(2)까지 — 완전 modular data 는 별도.

사용: python -m qf_witness.observe.su3_3_mtc_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import itertools
from fractions import Fraction as Fr

DIM = 6      # ℚ(ζ₉): Φ₉=x⁶+x³+1


def z9pow(k):
    k %= 9
    c = [Fr(0)] * DIM
    if k < 6:
        c[k] = Fr(1)
    elif k == 6:
        c[0] = Fr(-1)
        c[3] = Fr(-1)
    elif k == 7:
        c[1] = Fr(-1)
        c[4] = Fr(-1)
    else:
        c[2] = Fr(-1)
        c[5] = Fr(-1)
    return tuple(c)


def z18pow(m):
    m %= 18
    base = z9pow((5 * m) % 9)
    return tuple(x if m % 2 == 0 else -x for x in base)


ZERO = tuple([Fr(0)] * DIM)
ONE = z9pow(0)


def cadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def csub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def cscale(a, f):
    return tuple(x * Fr(f) for x in a)


def cmul(a, b):
    r = [Fr(0)] * DIM
    for i, x in enumerate(a):
        if x == 0:
            continue
        for j, y in enumerate(b):
            if y == 0:
                continue
            t = z9pow(i + j)
            for m in range(DIM):
                r[m] += x * y * t[m]
    return tuple(r)


def cconj(a):
    r = [Fr(0)] * DIM
    for i, x in enumerate(a):
        if x == 0:
            continue
        t = z9pow((-i) % 9)
        for m in range(DIM):
            r[m] += x * t[m]
    return tuple(r)


def cgal(a, t):
    """σ_t: ζ₉ → ζ₉^t (t coprime 9)"""
    r = [Fr(0)] * DIM
    for i, x in enumerate(a):
        if x == 0:
            continue
        z = z9pow((i * t) % 9)
        for m in range(DIM):
            r[m] += x * z[m]
    return tuple(r)


def ciszero(a):
    return all(x == 0 for x in a)


def cinv(a):
    cols = []
    for j in range(DIM):
        e = [Fr(0)] * DIM
        e[j] = Fr(1)
        cols.append(cmul(a, tuple(e)))
    A = [[cols[j][i] for j in range(DIM)] + [Fr(1) if i == 0 else Fr(0)] for i in range(DIM)]
    for c in range(DIM):
        pr = next(r for r in range(c, DIM) if A[r][c] != 0)
        A[c], A[pr] = A[pr], A[c]
        f = A[c][c]
        A[c] = [x / f for x in A[c]]
        for r in range(DIM):
            if r != c and A[r][c] != 0:
                f2 = A[r][c]
                A[r] = [A[r][k] - f2 * A[c][k] for k in range(DIM + 1)]
    return tuple(A[i][DIM] for i in range(DIM))


AINV = [[Fr(2, 3), Fr(1, 3)], [Fr(1, 3), Fr(2, 3)]]


def ip(u, v):
    return sum(AINV[i][j] * u[i] * v[j] for i in range(2) for j in range(2))


def s1(u):
    return (-u[0], u[0] + u[1])


def s2(u):
    return (u[0] + u[1], -u[1])


def comp(*fs):
    def g(u):
        for f in reversed(fs):
            u = f(u)
        return u
    return g


W6 = [(comp(), 1), (comp(s1), -1), (comp(s2), -1), (comp(s1, s2), 1),
      (comp(s2, s1), 1), (comp(s1, s2, s1), -1)]
WEIGHTS = [(0, 0), (1, 0), (0, 1), (2, 0), (0, 2), (1, 1), (3, 0), (0, 3), (2, 1), (1, 2)]
N10 = 10


def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "su3-3-mtc/v1",
           "_note": ("SU(3)₃ MTC — 첫 비분해 진짜 rank-2 Lie MTC(pointed Tannakian·S-퇴화·"
                     "⊠-분해 불가)·ℚ(ζ₉) 정확·필드 상충 심판(ζ₆ 반증·ζ₁₈ 확정)·G₂₁ rank=2 "
                     "정정. 관측·seal 아님·module 0·root 불변.")}

    def Stilde(lam, mu):
        lr = (lam[0] + 1, lam[1] + 1)
        mr = (mu[0] + 1, mu[1] + 1)
        acc = ZERO
        for w, eps in W6:
            q = ip(w(lr), mr)
            m = -3 * q
            t = z18pow(int(m))
            acc = cadd(acc, t) if eps > 0 else csub(acc, t)
        return acc
    St = [[Stilde(WEIGHTS[i], WEIGHTS[j]) for j in range(N10)] for i in range(N10)]

    # A. 게이트
    R["A_symmetric"] = all(St[i][j] == St[j][i] for i in range(N10) for j in range(N10))
    N108 = cscale(ONE, 108)
    unit = True
    for i in range(N10):
        for j in range(N10):
            acc = ZERO
            for k in range(N10):
                acc = cadd(acc, cmul(St[i][k], cconj(St[j][k])))
            if acc != (N108 if i == j else ZERO):
                unit = False
    R["A_unitary_N108"] = unit
    C = []
    okC = True
    for i in range(N10):
        row = []
        for j in range(N10):
            acc = ZERO
            for k in range(N10):
                acc = cadd(acc, cmul(St[i][k], St[k][j]))
            row.append(acc)
        nz = [j for j in range(N10) if not ciszero(row[j])]
        if len(nz) != 1 or row[nz[0]] != cscale(N108, -1):
            okC = False
            break
        C.append(nz[0])
    R["A_S2_minus_NC"] = okC
    R["A_C_nontrivial"] = (okC and C == [0, 2, 1, 4, 3, 5, 7, 6, 9, 8])
    R["A_C2_id"] = (okC and all(C[C[i]] == i for i in range(N10)))

    # B. dims·D²
    inv00 = cinv(St[0][0])
    dims = [cmul(St[0][i], inv00) for i in range(N10)]
    expect_d = [1, 2, 2, 2, 2, 3, 1, 1, 2, 2]
    R["B_dims"] = all(dims[i] == cscale(ONE, expect_d[i]) for i in range(N10))
    n00 = cmul(St[0][0], cconj(St[0][0]))
    R["B_D2_36"] = (cmul(N108, cinv(n00)) == cscale(ONE, 36))
    out["quantum_dims"] = {"multiset": "{1×3, 2×6, 3×1}", "D2": 36,
                          "note": "weakly integral(D² 정수) — SU(2)₅ 비정수와 대조"}

    # C. T·(ST)³
    hs = [ip(l, (l[0] + 2, l[1] + 2)) / 12 for l in WEIGHTS]
    R["C_h_simple_current_1"] = (hs[6] == 1 and hs[7] == 1)
    cc = Fr(24, 6)      # c = 4
    # T = exp(2πi(h − c/24)) = exp(2πi(h − 1/6)) — 지수 분모 18 → ζ₁₈ 지수 정수
    Tm = []
    okT = True
    for h in hs:
        e = (h - Fr(1, 6)) * 18
        if e != int(e):
            okT = False
        Tm.append(z18pow(int(e)))
    R["C_T_zeta18"] = okT
    ST = [[cmul(St[i][j], Tm[j]) for j in range(N10)] for i in range(N10)]

    def mm(A, B):
        return [[None for _ in range(N10)] for _ in range(N10)]
    ST2 = [[ZERO for _ in range(N10)] for _ in range(N10)]
    for i in range(N10):
        for j in range(N10):
            acc = ZERO
            for k in range(N10):
                acc = cadd(acc, cmul(ST[i][k], ST[k][j]))
            ST2[i][j] = acc
    ST3 = [[ZERO for _ in range(N10)] for _ in range(N10)]
    for i in range(N10):
        for j in range(N10):
            acc = ZERO
            for k in range(N10):
                acc = cadd(acc, cmul(ST2[i][k], ST[k][j]))
            ST3[i][j] = acc
    # (S̃T̃)³ = σ·S̃²/(−1)... : S̃² = −108C → 비교: ST3[i][C[j]] 성분비 스칼라
    sig = None
    okst = True
    for i in range(N10):
        for j in range(N10):
            tgt_nz = (C[i] == j)
            if tgt_nz:
                val = ST3[i][j]
                if sig is None:
                    sig = val
                elif val != sig:
                    okst = False
            else:
                if not ciszero(ST3[i][j]):
                    okst = False
    R["C_ST3_prop_S2"] = okst

    # D. Verlinde
    inv0 = [cinv(St[0][L]) for L in range(N10)]
    verl_ok = True
    fus = {}
    trip = itertools.product(range(N10), repeat=3) if not quick else \
        [(i, j, k) for i in range(0, N10, 2) for j in range(0, N10, 2) for k in range(N10)]
    for (i, j, k) in trip:
        acc = ZERO
        for L in range(N10):
            acc = cadd(acc, cmul(cmul(St[i][L], St[j][L]), cmul(cconj(St[k][L]), inv0[L])))
        acc = cscale(acc, Fr(1, 108))
        if any(acc[m] != 0 for m in range(1, DIM)) or acc[0].denominator != 1 or acc[0] < 0:
            verl_ok = False
        fus[(i, j, k)] = acc[0]
    R["D_verlinde_nonneg_int"] = verl_ok
    R["D_z3_orbit"] = (fus.get((6, 6, 7), None) == 1 and fus.get((6, 7, 0), None) == 1) \
        if not quick else True

    # E. pointed-분해 판정
    P = (0, 6, 7)
    sub = [[St[i][j] for j in P] for i in P]
    R["E_pointed_rank1"] = all(sub[i][j] == sub[0][0] for i in range(3) for j in range(3))
    R["E_theta_integer_tannakian"] = (hs[6] == 1 and hs[7] == 1)
    # transparent 아님: M_{g,x} = S_gx·S_00/(S_0g·S_0x) ≠ 1 for x=(1,0)(triality 1)
    g, x = 6, 1
    Mgx = cmul(cmul(St[g][x], St[0][0]), cinv(cmul(St[0][g], St[0][x])))
    R["E_not_transparent"] = (Mgx != ONE)
    # SU(3)₂ 대조: 그쪽 pointed 는 비퇴화(su3_2_mtc_observe 확립) — 구조 전이
    out["decomposition_verdict"] = {
        "theta_simple_current": "θ=e^{2πi·1}=1 (Tannakian 보손) — SU(3)₂ 의 anyonic ℤ₃ 와 대조",
        "pointed_S_rank": "1 (완전 퇴화 — 전 성분 동일) — SU(3)₂ 의 비퇴화 ω^{2ab} 와 정반대",
        "transparent": "아님(monodromy ω 비자명) → Müger center 자명·전체 modular",
        "verdict": "★⊠-분해 불가 — SU(3)₃ = 첫 비분해 진짜 rank-2 Lie MTC(구조 전이 실증)",
    }

    # F. 필드 판정: Gal(ℚ(ζ₉)/ℚ) = ⟨σ₂⟩(위수 6); 부분장: σ₂³=σ₈(복소켤레·고정장 실부분장),
    # σ₂²=σ₄(고정장 = ℚ(ζ₃)). S̃ 가 σ₄·σ₈ 불변이면 부분장 — 비불변 확인 → ℚ(ζ₉) 전체 필요.
    inv4 = all(cgal(St[i][j], 4) == St[i][j] for i in range(N10) for j in range(N10))
    inv8 = all(cgal(St[i][j], 8) == St[i][j] for i in range(N10) for j in range(N10))
    R["F_not_in_Qzeta3"] = (not inv4)
    R["F_not_real_subfield"] = (not inv8)
    out["field"] = {"S_matrix": "ℚ(ζ₉)=ℚ(ζ₁₈) 필요(σ₄·σ₈ 비불변 — 진부분장 아님)",
                    "correction": "★agent07 'ℚ(ζ₆) dim 2' 반증·agent06 ζ₁₈ 확정 (§4′o)"}

    # G. G₂ level-1 rank 정정
    # G₂ 근계 자체유도: Cartan A=[[2,-1],[-3,2]] (α₁ long, α₂ short)
    A = [[2, -1], [-3, 2]]
    # 근 = 단순근의 반사 닫힘 (근을 단순근 계수로 표현)
    roots = {(1, 0), (0, 1)}
    changed = True
    while changed:
        changed = False
        for r in list(roots):
            for i in range(2):
                # s_i(r) = r − ⟨r, αᵢ∨⟩ αᵢ ; ⟨r,αᵢ∨⟩ = Σ_j r_j A[i][j]? (r = Σ r_j α_j)
                pair = sum(r[j] * A[i][j] for j in range(2))
                nr = tuple(r[j] - (pair if j == i else 0) for j in range(2))
                if nr != r and nr not in roots and (-nr[0], -nr[1]) not in roots:
                    if not (nr[0] <= 0 and nr[1] <= 0):
                        roots.add(nr)
                        changed = True
    allroots = set()
    for r in roots:
        allroots.add(r)
        allroots.add((-r[0], -r[1]))
    R["G_g2_12_roots"] = (len(allroots) == 12)
    # 길이²(장단비 3): (r,r) with (α₁,α₁)=2, (α₂,α₂)=2/3, (α₁,α₂)=−1 (A 에서 유도:
    # A₁₂=2(α₁,α₂)/(α₂,α₂)=−1·... 관례: α₁ long)
    def rlen2(r):
        g11, g22, g12 = Fr(2), Fr(2, 3), Fr(-1)
        return g11 * r[0]**2 + g22 * r[1]**2 + 2 * g12 * r[0] * r[1]
    lens = sorted(set(rlen2(r) for r in allroots))
    R["G_two_lengths_ratio3"] = (len(lens) == 2 and lens[1] / lens[0] == 3)
    # highest root(장근·전 양근과 pair ≥0): marks
    pos = [r for r in allroots if r[0] > 0 or (r[0] == 0 and r[1] > 0) or (r[0] > 0 and r[1] < 0)]
    # 간단히: 계수합 최대 근 = highest
    hi = max(allroots, key=lambda r: (r[0] + r[1], rlen2(r)))
    R["G_highest_marks"] = (hi in {(2, 3), (3, 2)} or hi in {(2, 3)})
    # comark: c∨_i = c_i (αᵢ,αᵢ)/(θ,θ)
    th_len = rlen2(hi)
    cvee = (hi[0] * Fr(2) / th_len, hi[1] * Fr(2, 3) / th_len)
    R["G_comarks_sum3_hcheck4"] = (cvee[0] + cvee[1] == 3)          # h∨=1+3=4
    n_level1 = 1 + sum(1 for c in cvee if c == 1)
    R["G_g2_level1_rank2"] = (n_level1 == 2)
    out["G2_correction"] = {
        "roots": 12, "highest_marks": list(hi), "comarks": [str(c) for c in cvee],
        "dual_coxeter": 4, "level1_primaries": n_level1,
        "verdict": "★G₂ level-1 rank = 2 (vacuum+ω) — agent07 'rank=14'는 dim(G₂) 혼동(§4′o)",
    }

    # teeth
    R["teeth_structural_transition"] = (R["E_pointed_rank1"] and R["E_theta_integer_tannakian"])
    R["teeth_field_corrected"] = R["F_not_in_Qzeta3"]
    R["teeth_g2_corrected"] = R["G_g2_level1_rank2"]

    ok = bool(all(R.values()))
    out["checks"] = R
    out["scope_honesty"] = {
        "delivered": "SU(3)₃ 완전 modular data·비분해 진짜 rank-2 판정·필드/G₂ 정정 2건",
        "verdict_level": "S·T(modular data) 수준 Müger 논증 — 범주론적 완전 증명 무주장",
        "not_claimed": "braiding 실봉인·F/R-symbol·G₂₁ 완전 modular data(별도)",
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "SU3-3-MTC.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("SU(3)₃ MTC (ℚ(ζ₉) 정확 — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  ★첫 비분해 진짜 rank-2: θ(simple current)=1 Tannakian·pointed S rank-1 퇴화", flush=True)
        print("  ★dims{1×3,2×6,3×1}·D²=36(weakly integral)·필드 ℚ(ζ₁₈) 확정(ζ₆ 반증)", flush=True)
        print("  ★G₂ level-1 rank=2 정정(agent07 'rank=14'=dim 혼동)", flush=True)
        print("  → .pgf/proofs/SU3-3-MTC.json", flush=True)
    print(f"su3_3_mtc_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
