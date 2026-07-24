#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""su3_2_mtc_observe — TrackHE18: SU(3)₂ MTC 완전 modular data — **첫 rank-2 Lie 준위**
(Kac-Peterson·Weyl S₃)·★Fib⊠ℤ₃ 인수분해·★비자명 charge conjugation (관측, seal 아님).

MTC 계보(SU(2)₂/₃/₄/₅·D(S₃)/D(D₄)/D^ω)는 전부 SU(2)-계열 또는 유한군 double — SU(3)₂ 는
**첫 rank-2**: 6 sectors(λ₁+λ₂≤2), Kac-Peterson S_{λμ} ∝ Σ_{w∈S₃} ε(w)e^{−2πi⟨w(λ+ρ),μ+ρ⟩/5}.
전부 **ℚ(ζ₁₅) 정확 산술 직접 구현**(Φ₁₅ 8차 기저·Fraction — float/simplify 없음).

관측 7축:
  A. **Kac-Peterson 자체유도**: A₂ 내적(⟨ωᵢ,ωⱼ⟩=A⁻¹)·Weyl S₃(6원소·부호)·exp(−2πi q/5)=ζ₁₅^{−3q}
     정확. 6 weights: (0,0),(1,0),(0,1),(2,0),(0,2),(1,1) = {1, 3, 3̄, 6, 6̄, 8}.
  B. **modular 게이트**: S̃=S̃ᵀ·S̃S̃†=75·I·**S̃²=−75·C**(Kac-Peterson 위상 i^{|Δ₊|}=i³ →
     S=−iS̃/√75 에서 S²=C·S₀₀>0) — ★**C=(3↔3̄, 6↔6̄) 비자명 charge conjugation**(C≠I·C²=I,
     Lie-준위 계보 최초 non-self-dual).
  C. **양자차원·D²**: dims={1,φ,φ,1,1,φ}(**1×3·φ×3**·φ=(1+√5)/2)·**D²=3(2+φ)=(15+3√5)/2** —
     ℚ(√5)(dims 는 부분장).
  D. **T·(ST)³**: h=[0,4/15,4/15,2/3,2/3,3/5]·c=2·8/5=**16/5**·T=ζ₃₀ 지수(ζ₃₀=−ζ₁₅⁸ 로 ℚ(ζ₁₅)
     내 표현)·**(S̃T̃)³=σ·S̃²/(−1)**(스칼라 정확).
  E. **Verlinde 216 전수 비음정수** + ℤ₃ pointed 부분군(d=1 sectors {1,6,6̄}: 6⊗6=6̄·6⊗6̄=1 가역).
  F. ★**Fib⊠ℤ₃ 인수분해(modular-data 동치)**: 매핑 1=(1,0)·6=(1,2)·6̄=(1,1)·8=(τ,0)·3=(τ,1)·
     3̄=(τ,2) 에서 **S̃_{ij}=S̃₀₀·S̃^F_{f₁f₂}·ω^{2a₁a₂} 정확 전수** + **T-spins 정확**(conj-Fib
     h_τ=3/5 ⊠ ℤ₃ anyon q=2: h_a=2a²/3). ⟹ SU(3)₂ ≅ Fib̄⊠ℤ₃^{(2)} (S·T 동시).
  G. ★**부호장 판정(§4′o)**: S̃ 는 σ₁₁(Gal/ℚ(ζ₅))·σ₇(Gal/ℚ(ζ₃)) **모두 비불변** → **ℚ(ζ₁₅)
     필요** — agent05 의 "field ℚ(ζ₅)" 는 **부정확**(dims/D² 의 ℚ(√5)⊂ℚ(ζ₅) 와 혼동 추정).

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - modular data = 조합·대수 exact 표(ℚ(ζ₁₅) 유리계수) — braiding 게이트 실봉인 무주장.
  - Fib⊠ℤ₃ 동치 = **S·T(modular data) 수준** — F/R-symbol(범주 동치) 무주장.
  - 단독 제안 축(agent05)이라 전 수치 자체유도(§4′o) — 필드 주장 1건 정정.

사용: python -m qf_witness.observe.su3_2_mtc_observe [--quick]
"""
from __future__ import annotations
import sys
import json
from fractions import Fraction as Fr


# ── ℚ(ζ₁₅) 정확 산술: Φ₁₅(x)=x⁸−x⁷+x⁵−x⁴+x³−x+1 ─────────────────────────────
RED8 = [Fr(-1), Fr(1), Fr(0), Fr(-1), Fr(1), Fr(-1), Fr(0), Fr(1)]
ZPOW = []
for k in range(15):
    if k < 8:
        v = [Fr(0)] * 8
        v[k] = Fr(1)
        ZPOW.append(v)
    else:
        prev = ZPOW[k - 1]
        w = [Fr(0)] + prev[:7]
        ov = prev[7]
        if ov:
            w = [w[i] + ov * RED8[i] for i in range(8)]
        ZPOW.append(w)
MULTAB = [[ZPOW[(i + j) % 15] if (i + j) < 15 or True else None for j in range(8)]
          for i in range(8)]
for i in range(8):
    for j in range(8):
        k = i + j
        MULTAB[i][j] = ZPOW[k] if k < 15 else ZPOW[k - 15]


def czero():
    return [Fr(0)] * 8


def cone():
    v = czero()
    v[0] = Fr(1)
    return v


def cadd(a, b):
    return [x + y for x, y in zip(a, b)]


def csub(a, b):
    return [x - y for x, y in zip(a, b)]


def cscale(a, f):
    return [x * Fr(f) for x in a]


def cmul(a, b):
    r = czero()
    for i, x in enumerate(a):
        if x == 0:
            continue
        for j, y in enumerate(b):
            if y == 0:
                continue
            t = MULTAB[i][j]
            f = x * y
            r = [r[m] + f * t[m] for m in range(8)]
    return r


def zeta(k):
    return ZPOW[k % 15][:]


def cconj(a):
    r = czero()
    for i, x in enumerate(a):
        if x == 0:
            continue
        t = zeta((-i) % 15)
        r = [r[m] + x * t[m] for m in range(8)]
    return r


def ceq(a, b):
    return all(x == y for x, y in zip(a, b))


def ciszero(a):
    return all(x == 0 for x in a)


def cinv(a):
    cols = []
    for j in range(8):
        e = czero()
        e[j] = Fr(1)
        cols.append(cmul(a, e))
    A = [[cols[j][i] for j in range(8)] + [Fr(1) if i == 0 else Fr(0)] for i in range(8)]
    for c in range(8):
        pr = next(r for r in range(c, 8) if A[r][c] != 0)
        A[c], A[pr] = A[pr], A[c]
        f = A[c][c]
        A[c] = [x / f for x in A[c]]
        for r in range(8):
            if r != c and A[r][c] != 0:
                f2 = A[r][c]
                A[r] = [A[r][k] - f2 * A[c][k] for k in range(9)]
    return [A[i][8] for i in range(8)]


def galois(a, t):
    r = czero()
    for i, x in enumerate(a):
        if x == 0:
            continue
        z = zeta((i * t) % 15)
        r = [r[m] + x * z[m] for m in range(8)]
    return r


def cnum(a):
    import cmath
    return sum(complex(x) * cmath.exp(2j * cmath.pi * i / 15) for i, x in enumerate(a))


# ── Kac-Peterson ────────────────────────────────────────────────────────────
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


W = [(comp(), 1), (comp(s1), -1), (comp(s2), -1), (comp(s1, s2), 1),
     (comp(s2, s1), 1), (comp(s1, s2, s1), -1)]
WEIGHTS = [(0, 0), (1, 0), (0, 1), (2, 0), (0, 2), (1, 1)]
SNAMES = ["1", "3", "3b", "6", "6b", "8"]
N6 = 6


def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "su3-2-mtc/v1",
           "_note": ("SU(3)₂ MTC 완전 modular data — 첫 rank-2 Lie 준위(Kac-Peterson·ℚ(ζ₁₅) "
                     "정확 산술)·비자명 C(3↔3̄)·★Fib⊠ℤ₃ 인수분해(S·T 동시)·★부호장 ℚ(ζ₁₅) "
                     "(agent05 'ℚ(ζ₅)' 정정). 관측·seal 아님·module 0·root 불변.")}

    def Stilde(lam, mu):
        lr = (lam[0] + 1, lam[1] + 1)
        mr = (mu[0] + 1, mu[1] + 1)
        acc = czero()
        for w, eps in W:
            q = ip(w(lr), mr)
            m = -3 * q
            t = zeta(int(m))
            acc = cadd(acc, t) if eps > 0 else csub(acc, t)
        return acc
    St = [[Stilde(WEIGHTS[i], WEIGHTS[j]) for j in range(N6)] for i in range(N6)]

    # B. modular 게이트
    R["B_symmetric"] = all(ceq(St[i][j], St[j][i]) for i in range(N6) for j in range(N6))
    N75 = cscale(cone(), 75)
    unit = True
    for i in range(N6):
        for j in range(N6):
            acc = czero()
            for k in range(N6):
                acc = cadd(acc, cmul(St[i][k], cconj(St[j][k])))
            if not ceq(acc, N75 if i == j else czero()):
                unit = False
    R["B_unitary_N75"] = unit
    C = []
    okC = True
    for i in range(N6):
        row = []
        for j in range(N6):
            acc = czero()
            for k in range(N6):
                acc = cadd(acc, cmul(St[i][k], St[k][j]))
            row.append(acc)
        nz = [j for j in range(N6) if not ciszero(row[j])]
        if len(nz) != 1 or not ceq(row[nz[0]], cscale(cone(), -75)):
            okC = False
            break
        C.append(nz[0])
    R["B_S2_minus75C"] = okC
    R["B_C_nontrivial"] = (okC and C == [0, 2, 1, 4, 3, 5])   # 3↔3̄, 6↔6̄
    R["B_C2_id"] = (okC and all(C[C[i]] == i for i in range(N6)))
    s00 = cnum(St[0][0])
    R["B_S00_pos_after_phase"] = ((-1j * s00).real > 0)       # S=−iS̃/√75

    # C. dims·D²
    sqrt5 = cadd(cone(), cadd(cscale(zeta(3), 2), cscale(zeta(12), 2)))
    phi_c = cscale(cadd(cone(), sqrt5), Fr(1, 2))
    inv00 = cinv(St[0][0])
    dims = [cmul(St[0][i], inv00) for i in range(N6)]
    R["C_dims_1_phi"] = (ceq(dims[0], cone()) and ceq(dims[3], cone())
                         and ceq(dims[4], cone()) and ceq(dims[1], phi_c)
                         and ceq(dims[2], phi_c) and ceq(dims[5], phi_c))
    # D² = 75/|S̃00|² == 3(2+φ): |S̃00|² = S̃00·conj(S̃00)
    n00 = cmul(St[0][0], cconj(St[0][0]))
    D2 = cmul(cscale(cone(), 75), cinv(n00))
    target = cscale(cadd(cscale(cone(), 2), phi_c), 3)
    R["C_D2_3_2plusphi"] = ceq(D2, target)
    out["quantum_dims"] = {"pattern": "1×3 (1,6,6̄) · φ×3 (3,3̄,8)",
                           "D2": "3(2+φ) = (15+3√5)/2 ≈ 10.854"}

    # D. T·(ST)³
    hs = [Fr(0), Fr(4, 15), Fr(4, 15), Fr(2, 3), Fr(2, 3), Fr(3, 5)]
    hs_derived = [ip((l[0], l[1]), (l[0] + 2, l[1] + 2)) / 10 for l in WEIGHTS]
    R["D_h_values"] = (hs_derived == hs)
    cc = Fr(16, 5)
    Tm = [int((h - cc / 24) * 30) for h in hs]
    R["D_T_zeta30_integers"] = all((h - cc / 24) * 30 == int((h - cc / 24) * 30) for h in hs)

    def z30(m):
        v = zeta((8 * m) % 15)
        return v if m % 2 == 0 else cscale(v, -1)
    Td = [z30(m) for m in Tm]
    ST = [[cmul(St[i][j], Td[j]) for j in range(N6)] for i in range(N6)]

    def mm(A, B):
        return [[__import__('functools').reduce(cadd, [cmul(A[i][k], B[k][j])
                                                       for k in range(N6)])
                 for j in range(N6)] for i in range(N6)]
    M = mm(mm(ST, ST), ST)
    MC = [[M[i][C[j]] for j in range(N6)] for i in range(N6)]
    sig = MC[0][0]
    R["D_ST3_prop_S2"] = all(ceq(MC[i][j], sig if i == j else czero())
                             for i in range(N6) for j in range(N6))

    # E. Verlinde
    inv0 = [cinv(St[0][L]) for L in range(N6)]
    verl_ok = True
    fus = {}
    for i in range(N6):
        for j in range(N6):
            for k in range(N6):
                acc = czero()
                for L in range(N6):
                    acc = cadd(acc, cmul(cmul(St[i][L], St[j][L]),
                                         cmul(cconj(St[k][L]), inv0[L])))
                acc = [x / 75 for x in acc]
                if any(acc[m] != 0 for m in range(1, 8)) or acc[0].denominator != 1 \
                        or acc[0] < 0:
                    verl_ok = False
                fus[(i, j, k)] = acc[0]
    R["E_verlinde_nonneg_int"] = verl_ok
    R["E_Z3_pointed"] = (fus[(3, 3, 4)] == 1 and fus[(3, 4, 0)] == 1
                         and sum(fus[(3, 3, k)] for k in range(N6)) == 1)

    # F. Fib⊠ℤ₃ 인수분해
    SF = [[cone(), phi_c], [phi_c, cscale(cone(), -1)]]
    mapping = {0: (0, 0), 3: (0, 2), 4: (0, 1), 5: (1, 0), 1: (1, 1), 2: (1, 2)}
    c0 = St[0][0]
    okS = True
    for i in range(N6):
        for j in range(N6):
            (f1, a1) = mapping[i]
            (f2, a2) = mapping[j]
            rhs = cmul(c0, cmul(SF[f1][f2], zeta((2 * a1 * a2 * 5) % 15)))
            if not ceq(St[i][j], rhs):
                okS = False
    R["F_fib_z3_S_match"] = okS
    R["F_fib_z3_T_match"] = all(
        ((hs[i] - ((Fr(3, 5) if mapping[i][0] == 1 else Fr(0))
                   + Fr(2 * mapping[i][1] ** 2, 3))) % 1 == 0) for i in range(N6))
    out["factorization"] = {
        "equivalence": "SU(3)₂ ≅ conj-Fib(h_τ=3/5) ⊠ ℤ₃^(q=2)  [S·T modular data 동시 정확]",
        "mapping": "1=(1,0)·6=(1,2)·6̄=(1,1)·8=(τ,0)·3=(τ,1)·3̄=(τ,2)",
        "not_claimed": "F/R-symbol 범주 동치",
    }

    # G. 부호장
    R["G_not_in_Qzeta5"] = (not all(ceq(galois(St[i][j], 11), St[i][j])
                                    for i in range(N6) for j in range(N6)))
    R["G_not_in_Qzeta3"] = (not all(ceq(galois(St[i][j], 7), St[i][j])
                                    for i in range(N6) for j in range(N6)))
    out["field"] = {"S_matrix": "ℚ(ζ₁₅) 필요(σ₁₁·σ₇ 비불변 — 진부분장 아님)",
                    "correction": "★agent05 'field ℚ(ζ₅)' 부정확 — dims/D² 의 ℚ(√5) 와 혼동 추정 (§4′o)",
                    "dims_field": "ℚ(√5) ⊂ ℚ(ζ₅)"}

    # teeth
    R["teeth_C_nontrivial_first_lie"] = R["B_C_nontrivial"]
    R["teeth_factorization_both_ST"] = (R["F_fib_z3_S_match"] and R["F_fib_z3_T_match"])
    R["teeth_field_corrected"] = R["G_not_in_Qzeta5"]

    ok = bool(all(R.values()))
    out["checks"] = R
    out["scope_honesty"] = {
        "delivered": "첫 rank-2 Lie MTC 완전 modular data·비자명 C·Fib⊠ℤ₃ 동치·부호장 정정",
        "exact": "전부 ℚ(ζ₁₅) Fraction 산술(Φ₁₅ 8차 기저) — float/simplify 없음",
        "not_claimed": "braiding 게이트 실봉인·F/R-symbol 범주 동치",
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "SU3-2-MTC.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("SU(3)₂ MTC 완전 modular data (ℚ(ζ₁₅) 정확 — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  ★첫 rank-2 Lie 준위·C=(3↔3̄,6↔6̄) 비자명·dims{1×3,φ×3}·D²=3(2+φ)", flush=True)
        print("  ★SU(3)₂ ≅ conj-Fib⊠ℤ₃^(2) (S·T 동시 정확)·부호장 ℚ(ζ₁₅)(agent05 정정)", flush=True)
        print("  → .pgf/proofs/SU3-2-MTC.json", flush=True)
    print(f"su3_2_mtc_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
