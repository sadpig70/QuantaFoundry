#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bmw3_kauffman_family_observe — TrackHE18 후속(v19 §4 예고 축): 2변수 Dubrovnik D(a,z) 를
**매듭 가족**으로 확장 — 5₁(torus)·5₂(twist)·6₂·★6₃(amphichiral) (관측, seal 아님).
[[bmw3_kauffman_2var_observe]](fig-8 단일)의 가족화.

★방법(3중 특수화 구성 + 완전 독립 확증):
  - 구성(선형계): **N=3**(spin-1, 27차원)·**N=4**(so₄=sl₂×sl₂, 64차원)·**N=2**(spin-½ qt-Jones,
    8차원 — Jones 는 Dubrovnik 특수화선 a=i·t^{−3/4} 이므로 정당한 제3 곡선) quantum trace →
    ansatz Σc_{ij}a^i z^j 유일해(free=0)·**계수 전부 정수**.
  - 확증(복원에 완전 독립): ★**TL₃ Kauffman-bracket 상태합 엔진**(quantum trace 와 무관한 별도
    조합 엔진)의 Jones 와 **정확 유리 25점 일치**(t=r⁴ ⇒ ℚ(i) 정확 산술·차수 상한 논증으로 항등)
    + **det=|V(−1)|**{5,7,11,13} + **chirality**(D(a,z) vs D(a⁻¹,−z)).

★매듭 동정(문헌 braid 좌표 인용 없이 자체):
  - 3-braid 워드 소전수(길이 5·6) → 1-성분 필터 → bracket det 판정 + 교차수 상한 논증:
    det∈{5,7,11,13} 은 해당 교차수 이하에서 5₁/5₂/6₂/6₃ 유일(소수 매듭).
  - ★함정 2건 자체 포착: (i) det=9 후보는 **granny/square knot(3₁#3₁, 합성)** — 합성매듭 배제
    (ii) **6₁ 은 braid index 4** → 3-braid 에 부재(가족을 6₂/6₃ 로 구성한 이유).
  - words: 5₁=σ₁⁵(T(2,5)·⊔unknot δ-보정)·5₂=σ₁σ₂⁻¹σ₁⁻³σ₂⁻¹·6₂=σ₁³σ₂⁻¹σ₁σ₂⁻¹·6₃=σ₁²σ₂⁻¹σ₁σ₂⁻².

★규약 정리(교훈·§4′): spin-½ quantum trace 는 TL-bracket 의 **전면 mirror**(σ 방향 관례차),
  Dubrovnik→Jones 치환이 그 mirror 를 되돌림(상쇄) — 6₃(amphichiral) 대질로 검출·5₁/5₂ 로 확정.
  또 sympy simplify 는 t^{1/4} 급 검증에 취약 → **t=r⁴ 정확 유리 다점**이 견고경로.

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - Jones 25점(N=2 구성)과 확증 25점은 **다른 엔진**(quantum trace vs bracket 상태합) — 순환 아님.
  - 매듭 이름 라벨은 det+교차수 상한 논증(합성 배제 포함) — 완전 매듭 동정표 무주장.
  - 6₁(braid index 4)은 4-braid quantum trace 확장 필요=다음.

사용: python -m qf_witness.observe.bmw3_kauffman_family_observe [--quick]
"""
from __future__ import annotations
import sys
import json

import sympy as sp

Q = sp.Symbol("Q")
a, z = sp.symbols("a z")
t = sp.symbols("t", positive=True)
q = sp.symbols("q")
A = sp.symbols("A")

WORDS = {
    "5_1": [(1, 1)] * 5,
    "5_2": [(1, 1), (-1, 2), (-1, 1), (-1, 1), (-1, 1), (-1, 2)],
    "6_2": [(1, 1), (1, 1), (1, 1), (-1, 2), (1, 1), (-1, 2)],
    "6_3": [(1, 1), (1, 1), (-1, 2), (1, 1), (-1, 2), (-1, 2)],
}
TWO_STRAND = {"5_1"}
DET = {"5_1": 5, "5_2": 7, "6_2": 11, "6_3": 13}
AMPHI = {"5_1": False, "5_2": False, "6_2": False, "6_3": True}


def kron(Am, Bm):
    return sp.Matrix(sp.BlockMatrix([[Am[i, j] * Bm for j in range(Am.cols)]
                                     for i in range(Am.rows)]))


# ── TL₃ bracket 엔진 (독립 확증용) ──────────────────────────────────────────
_MUL = {
    (0, 0): (0, 0), (0, 1): (1, 0), (0, 2): (2, 0), (0, 3): (3, 0), (0, 4): (4, 0),
    (1, 0): (1, 0), (1, 1): (1, 1), (1, 2): (3, 0), (1, 3): (3, 1), (1, 4): (1, 0),
    (2, 0): (2, 0), (2, 1): (4, 0), (2, 2): (2, 1), (2, 3): (2, 0), (2, 4): (4, 1),
    (3, 0): (3, 0), (3, 1): (1, 0), (3, 2): (3, 1), (3, 3): (3, 0), (3, 4): (1, 1),
    (4, 0): (4, 0), (4, 1): (4, 1), (4, 2): (2, 0), (4, 3): (2, 1), (4, 4): (4, 0),
}
_CLOOPS = {0: 3, 1: 2, 2: 2, 3: 1, 4: 1}


def bracket_jones(word):
    delta = -A**2 - A**-2
    vec = {0: sp.Integer(1)}
    w = 0
    for (sgn, i) in word:
        w += sgn
        ei = 1 if i == 1 else 2
        newv = {}
        for b, c in vec.items():
            for (factor, gb) in ([(A, 0), (A**-1, ei)] if sgn > 0
                                 else [(A**-1, 0), (A, ei)]):
                if gb == 0:
                    kk, dp = b, 0
                else:
                    kk, dp = _MUL[(b, gb)]
                newv[kk] = sp.expand(newv.get(kk, 0) + c * factor * delta**dp)
        vec = newv
    br = sp.expand(sum(c * delta**(_CLOOPS[b] - 1) for b, c in vec.items()))
    V = sp.expand(sp.simplify(((-A**3)**(-w)) * br))
    return sp.expand(sp.powsimp(V.subs(A, t**sp.Rational(-1, 4)), force=True))


# ── quantum trace 빌더들 ────────────────────────────────────────────────────
def build_gen(dimv, Rc, mu):
    Rci = sp.simplify(Rc.inv())
    Iv = sp.eye(dimv)
    return ({(1, 1): kron(Rc, Iv), (-1, 1): kron(Rci, Iv),
             (1, 2): kron(Iv, Rc), (-1, 2): kron(Iv, Rci)},
            kron(kron(mu, mu), mu))


def build_so3():
    def qn(n):
        return sp.simplify((q**n - q**(-n)) / (q - 1 / q))
    s2 = sp.sqrt(qn(2))
    E = sp.zeros(3)
    F = sp.zeros(3)
    E[0, 1] = s2
    E[1, 2] = s2
    F[1, 0] = s2
    F[2, 1] = s2
    mm = [1, 0, -1]
    Dg = sp.zeros(9)
    for i, mi in enumerate(mm):
        for j, mj in enumerate(mm):
            Dg[3 * i + j, 3 * i + j] = q**(2 * mi * mj)

    def En(M, n):
        R = sp.eye(3)
        for _ in range(n):
            R = R * M
        return R

    def qfact(n):
        r = sp.Integer(1)
        for k in range(1, n + 1):
            r *= qn(k)
        return r
    Rsum = sp.zeros(9)
    for n in range(0, 3):
        Rsum += (q - 1 / q)**n / qfact(n) * q**sp.Rational(n * (n - 1), 2) * kron(En(E, n), En(F, n))
    R = sp.simplify(Dg * Rsum)
    P = sp.zeros(9)
    for i in range(3):
        for j in range(3):
            P[3 * i + j, 3 * j + i] = 1
    Rc = sp.simplify(P * R)
    return build_gen(3, Rc, sp.diag(q**2, 1, q**-2)) + (q**4, q**2 + 1 + q**-2)


def _spin_half_R():
    E = sp.Matrix([[0, 1], [0, 0]])
    F = sp.Matrix([[0, 0], [1, 0]])
    mm = [sp.Rational(1, 2), sp.Rational(-1, 2)]
    Dg = sp.zeros(4)
    for i, mi in enumerate(mm):
        for j, mj in enumerate(mm):
            Dg[2 * i + j, 2 * i + j] = q**(2 * mi * mj)
    Rm = sp.simplify(Dg * (sp.eye(4) + (q - 1 / q) * kron(E, F)))
    P2 = sp.Matrix([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
    return sp.simplify(P2 * Rm)


def build_so4():
    Rh = _spin_half_R()

    def Rh_el(x, y, xp, yp):
        return Rh[2 * xp + yp, 2 * x + y]
    Rso4 = sp.zeros(16)
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for l in range(2):
                    row = 8 * i + 4 * j + 2 * k + l
                    for ip in range(2):
                        for jp in range(2):
                            for kp in range(2):
                                for lp in range(2):
                                    v = Rh_el(i, k, ip, kp) * Rh_el(j, l, jp, lp)
                                    if v != 0:
                                        Rso4[8 * ip + 4 * jp + 2 * kp + lp, row] += v
    Rso4 = sp.simplify(Rso4)
    # N=4 BMW 파라미터(x=q 기준): a=x³·δ=x²+2+x⁻²·μ=diag(x²,1,1,x⁻²) — 적합 변수 Q=x(치환 없음)
    return build_gen(4, Rso4, sp.diag(q**2, 1, 1, q**-2)) + (q**3, q**2 + 2 + q**-2)


def qtrace_F(gen, mu3, abmw, delta, word, two_strand, dim):
    M = sp.eye(dim**3)
    w = 0
    for g in word:
        M = M * gen[g]
        w += g[0]
    val = sp.together((M * mu3).trace())
    F = sp.simplify(abmw**(-w) * val / delta)
    if two_strand:
        F = sp.simplify(sp.cancel(F / delta))
    return F, w


def qt_jones(word, two_strand):
    Rh = _spin_half_R()
    gen, mu3 = build_gen(2, Rh, sp.diag(q, 1 / q))
    d2 = q + 1 / q
    M = sp.eye(8)
    w = 0
    for g in word:
        M = M * gen[g]
        w += g[0]
    raw = sp.simplify(sp.together((M * mu3).trace()) / d2)
    if two_strand:
        raw = sp.simplify(sp.cancel(raw / d2))
    return sp.expand(sp.cancel((raw * (q**sp.Rational(-3, 2))**w).subs(q, sp.sqrt(t))))


def n_components(word):
    perm = [0, 1, 2]
    for (sgn, i) in word:
        perm[i - 1], perm[i] = perm[i], perm[i - 1]
    seen = set()
    nc = 0
    for s in range(3):
        if s in seen:
            continue
        nc += 1
        x = s
        while x not in seen:
            seen.add(x)
            x = perm[x]
    return nc


def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "bmw3-kauffman-family/v1",
           "_note": ("2변수 Dubrovnik D(a,z) 매듭 가족(5₁·5₂·6₂·6₃) — 3중 특수화 구성"
                     "(N=2/3/4 quantum trace)+독립 확증(TL₃ bracket·det·chirality). "
                     "관측·seal 아님·module 0·root 불변.")}
    names = ["5_2", "6_3"] if quick else ["5_1", "5_2", "6_2", "6_3"]
    npts_c = 40
    npts_v = 10 if quick else 25

    gen3, mu33, ab3, dl3 = build_so3()
    gen4, mu34, ab4, dl4 = build_so4()
    Ds = {}
    for name in names:
        wd = WORDS[name]
        R[f"{name}_one_component"] = (n_components(wd) == (2 if name in TWO_STRAND else 1))   # σ₁⁵=5₁⊔unknot
        F3, _ = qtrace_F(gen3, mu33, ab3, dl3, wd, name in TWO_STRAND, 3)
        F4, _ = qtrace_F(gen4, mu34, ab4, dl4, wd, name in TWO_STRAND, 4)
        F3 = sp.expand(sp.cancel(F3.subs(q, sp.sqrt(Q))))     # N=3: Q=q² (a=Q²)
        F4 = sp.expand(sp.cancel(F4.subs(q, Q)))              # N=4: Q=q (a=Q³)
        Vqt = qt_jones(wd, name in TWO_STRAND)
        Vqt_m = sp.expand(sp.cancel(Vqt.subs(t, 1 / t)))      # D-치환 = mirror(qt)
        zc = Q - 1 / Q
        ilo, ihi, jm = -10, 8, 6
        terms = [(i, j, sp.Symbol(f"c_{i - ilo}_{j}"))
                 for i in range(ilo, ihi + 1) for j in range(0, jm + 1)]
        eqs = []
        for (Fc, ap) in [(F3, 2), (F4, 3)]:
            expr = sum(c * Q**(ap * i) * zc**j for (i, j, c) in terms)
            eqs += list(sp.Poly(sp.expand((expr - Fc) * Q**150), Q).all_coeffs())
        for k in range(2, 2 + npts_c):
            r = sp.Rational(k, k + 1)
            lhs = sum(c * (sp.I * r**-3)**i * (sp.I * (r + 1 / r))**j for (i, j, c) in terms)
            eqs.append(sp.expand(lhs - Vqt_m.subs(t, r**4)))
        sol = list(sp.linsolve(eqs, [c for (_, _, c) in terms]))
        R[f"{name}_solution"] = bool(sol)
        freev = set()
        if sol:
            for v in sol[0]:
                freev |= v.free_symbols
        R[f"{name}_unique"] = (len(freev) == 0)
        cmap = {terms[k][2]: sol[0][k] for k in range(len(terms))}
        D = sp.expand(sum(cmap[c] * a**i * z**j for (i, j, c) in terms))
        R[f"{name}_integer_coeffs"] = all(sp.Rational(v).q == 1 for v in cmap.values() if v != 0)
        # 독립 확증 1: bracket Jones
        br = bracket_jones(wd)
        if name in TWO_STRAND:
            br = sp.expand(sp.simplify(sp.cancel(
                br / (-(t**sp.Rational(1, 2) + t**sp.Rational(-1, 2))))))
        okJ = True
        for k in range(2, 2 + npts_v):
            r = sp.Rational(k, k + 1)
            if sp.simplify(D.subs({a: sp.I * r**-3, z: sp.I * (r + 1 / r)})
                           - br.subs(t, r**4)) != 0:
                okJ = False
                break
        R[f"{name}_jones_bracket_independent"] = okJ
        # 독립 확증 2·3: det·chirality
        R[f"{name}_det"] = (abs(br.subs(t, -1)) == DET[name])
        amphi = sp.simplify(D - sp.expand(D.subs({a: 1 / a, z: -z}))) == 0
        R[f"{name}_chirality"] = (amphi == AMPHI[name])
        Ds[name] = D
        out[f"D_{name}"] = str(D)

    # 동정 함정 기록(재검증): granny(σ₁³σ₂³) det=9·합성
    br_granny = bracket_jones([(1, 1)] * 3 + [(1, 2)] * 3)
    R["trap_granny_det9_composite"] = (abs(br_granny.subs(t, -1)) == 9)
    out["identification"] = {
        "method": "3-braid 워드 자체 동정 — det+교차수 상한(합성 배제)",
        "traps": "det=9=granny/square(3₁#3₁ 합성) 포착·6₁=braid index 4 → 3-braid 부재",
        "dets": {k: DET[k] for k in names},
    }
    out["convention"] = {
        "lesson": ("spin-½ quantum trace = TL-bracket 의 전면 mirror(σ 관례차)·Dubrovnik→Jones "
                   "치환이 상쇄 — 6₃ amphichiral 대질로 검출. sympy simplify 는 t^{1/4} 급 취약 → "
                   "t=r⁴ 정확 유리 다점이 견고경로"),
    }

    ok = bool(all(R.values()))
    out["checks"] = R
    out["scope_honesty"] = {
        "construction": "N=2/3/4 quantum trace 3중 특수화(선형계·유일해·정수 계수)",
        "independent": "TL₃ bracket 상태합(별도 엔진) 25점 정확 + det + chirality — 순환 아님",
        "next": "6₁(braid index 4 — 4-braid quantum trace 확장)·HOMFLY-Kauffman 비포함",
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "BMW3-KAUFFMAN-FAMILY.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("2변수 Dubrovnik 매듭 가족 (3중 특수화+독립 확증 — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  ★5₁·5₂·6₂·6₃ D(a,z) 정수 유일복원·bracket 독립확증·det{5,7,11,13}·6₃ amphichiral",
              flush=True)
        print("  → .pgf/proofs/BMW3-KAUFFMAN-FAMILY.json", flush=True)
    print(f"bmw3_kauffman_family_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
