#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bmw_kauffman_observe — TrackHE15 P3: BMW 대수 → Kauffman 2변수 매듭 다항식
F(a,z) (관측, seal 아님). 전 과정 정수 Laurent 산술(float 0).

[[homfly_hecke_observe]](v14 P2, A-형 Iwahori-Hecke → HOMFLY-PT)의 **직교 형제**:
Birman-Murakami-Wenzl(BMW) 대수는 B/C/D-형(직교·심플렉틱 양자군 U_q(so/sp))에 대응하며
**unoriented** skein 을 만족한다 — 검증 객체가 Hecke(oriented)·Kauffman bracket(state-sum,
v13)과 모두 상이하다. HOMFLY P 와 Kauffman F 는 서로를 포함하지 않는다(문헌 사실, 본 witness
는 두 다항식 **동시 산출**만 보고하고 포함관계는 무주장).

★규약을 조건에서 **유도**(인용 아님) — 선검증에서 실제로 오규약 1건 검출:
  BMW 표준 표기는 Dubrovnik 형(g−g⁻¹=z(1−e), δ=(a−a⁻¹)/z+1)이나, 이 규약에서는 Jones 특수화
  a=−s⁻³·z=s+s⁻¹ 가 **Laurent 가 되지 않는다**(δ 의 분모가 남음). Kauffman 형
    g + g⁻¹ = z(1 + e) ,  e·g = a⁻¹e ,  e² = δ·e ,  δ = (a+a⁻¹)/z − 1
  에서는 δ|_{Jones} = −(s²+s⁻²) 로 닫힌다 ⟹ **Kauffman 규약 채택**.
  Markov trace 도 유도: tr(1₂)=δ(2 unknot) · tr(g)=a(unknot+양 kink, regular isotopy) ·
  tr(e)=1(unknot). ★자체 정합: tr(g)+tr(g⁻¹) = z(tr(1)+tr(e)) ⟺ a+a⁻¹ = z(δ+1) ✓.

관측 계층 (전부 exact ℤ[a^±,z^±]):
  1. BMW_n 차원 **자체 재유도**: Brauer diagram(2n 점 완전매칭) 전수 카운트 = (2n−1)!!
     (n=1..4 → 1,3,15,105) — report15 의 "dim 15" 주장 자체검증.
  2. BMW₂(dim 3, 기저 {1,g,e}) 정규형: g² = −1 + z·g + z a⁻¹·e (관계식에서 유도) ·
     기저 닫힘·결합법칙 (g^i·g^j = g^{i+j}) 전수 확인.
  3. **T(2,k) 토러스 링크족**(σ₁^k 닫힘, k=0..6): regular-isotopy Λ = A_k δ + B_k a + C_k ·
     writhe 정규화 F = a^{−k}Λ ∈ ℤ[a^±,z^±] exact.
     k=0 unlink₂ · 1 unknot · 2 Hopf · 3 trefoil · 4 T(2,4) · 5 cinquefoil …
  4. ★교차검증 3중:
     (a) F(unknot) = 1 (정규화 자체검증)
     (b) **Jones 특수화** a=−s⁻³, z=s+s⁻¹, t=s⁴ → V(t) ∈ ℤ[t^±] (Laurent 나눗셈 exact) →
         ★v13 [[kauffman_bracket_observe]] 오라클과 **mirror 대조**(본 축은 positive braid =
         right-handed, v13 TREFOIL 은 left-handed → t↔t⁻¹ 경상에서 일치).
     (c) **HOMFLY 동시 산출**: v14 P2 모듈 직접 호출로 같은 링크의 P(a,z) 병기(두 다항식이
         같은 대상의 서로 다른 불변량임을 데이터로 제시 — 포함관계 무주장).
  5. mirror: F(L*)(a,z) = F(L)(a⁻¹,z) — T(2,k) 의 거울상(negative braid)에서 확인.
  teeth: (i) δ 오염 → 규약 정합식 a+a⁻¹=z(δ+1) 붕괴 + Λ(Hopf) 변화(★unknot 은 δ 에 무감 —
     검출력 없음을 실측 확인 후 대상 교체) (ii) tr(g) 규약 오염(a→1) → Jones 특수화 불일치
     (iii) ★Dubrovnik 규약 재현 → Jones 특수화가 Laurent 아님(선검증 재실행).

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - 매듭 다항식·대수 관계식은 **관측**(exact Laurent certificate) — 회로 봉인 아님.
  - ★스코프: **BMW₂(2-braid) 한정** — T(2,k) 토러스 족만 커버. fig-8 등 3-braid 대상은
    BMW₃(dim 15, Kauffman tangle 곱셈 필요)로 **미착수**(차기). "모든 링크" 무주장.
  - HOMFLY 와의 상호 비포함(Red-Hoffman pair)은 **문헌 사실**이며 본 witness 는 재증명하지 않음
    (11-crossing 쌍은 범위 밖) — 동시 산출 데이터만 제시.
  - BMW 대수의 B/C/D-형 양자군 유래는 배경 서술이며 본 witness 는 **관계식 자체**로 자기완결.

사용: python -m qf_witness.observe.bmw_kauffman_observe [--quick]
"""
from __future__ import annotations
import sys
import json


# ── 2변수 정수 Laurent ℤ[a^±,z^±]: dict{(i,j): coeff} ─────────────────────
def lmul(p, q):
    r = {}
    for (i, j), c in p.items():
        for (k, l), d in q.items():
            key = (i + k, j + l)
            r[key] = r.get(key, 0) + c * d
    return {k: v for k, v in r.items() if v}


def ladd(*ps):
    r = {}
    for p in ps:
        for k, v in p.items():
            r[k] = r.get(k, 0) + v
    return {k: v for k, v in r.items() if v}


def lsc(c, p):
    return {k: c * v for k, v in p.items() if c * v}


ONE = {(0, 0): 1}
A = {(1, 0): 1}
AI = {(-1, 0): 1}
Z = {(0, 1): 1}
ZI = {(0, -1): 1}

# ★Kauffman 규약 (선검증으로 확정)
DELTA = ladd(lmul(ladd(A, AI), ZI), lsc(-1, ONE))      # δ = (a+a⁻¹)/z − 1


# ── BMW 차원 자체 재유도: Brauer diagram = 완전매칭 수 = (2n−1)!! ──────────
def perfect_matchings(pts):
    if not pts:
        return 1
    a = pts[0]
    return sum(perfect_matchings([p for p in pts[1:] if p != b]) for b in pts[1:])


def double_factorial_odd(n):
    d = 1
    for k in range(1, 2 * n, 2):
        d *= k
    return d


# ── BMW₂ 정규형: 기저 (1, g, e) ───────────────────────────────────────────
def mul_g(v):
    """v·g — g² = −1 + z g + z a⁻¹ e · e g = a⁻¹ e."""
    a_, b_, c_ = v
    return (lsc(-1, b_),
            ladd(a_, lmul(Z, b_)),
            ladd(lmul(lmul(Z, AI), b_), lmul(AI, c_)))


def mul_ginv(v):
    """v·g⁻¹ — g⁻¹ = z(1+e) − g 에서: 1·g⁻¹ = z·1 + z·e − g."""
    a_, b_, c_ = v
    # (A + Bg + Ce)·g⁻¹ = A g⁻¹ + B + C e g⁻¹ ; e g⁻¹ = a e
    return (ladd(lmul(Z, a_), b_),
            lsc(-1, a_),
            ladd(lmul(Z, a_), lmul(A, c_)))


def gpow(k):
    v = (ONE, {}, {})
    f = mul_g if k >= 0 else mul_ginv
    for _ in range(abs(k)):
        v = f(v)
    return v


def bmw2_mul(u, v):
    """BMW₂ 곱 (결합법칙 검증용): u·v, v 를 (A,B,C) 로 두고 전개."""
    a_, b_, c_ = v
    res = (lsc(0, ONE), {}, {})
    # u·1
    res = (ladd(res[0], lmul(u[0], a_)), ladd(res[1], lmul(u[1], a_)),
           ladd(res[2], lmul(u[2], a_)))
    # u·g
    ug = mul_g(u)
    res = (ladd(res[0], lmul(ug[0], b_)), ladd(res[1], lmul(ug[1], b_)),
           ladd(res[2], lmul(ug[2], b_)))
    # u·e : 1·e = e · g·e = a⁻¹ e · e·e = δ e
    ue = ({}, {}, ladd(u[0], lmul(AI, u[1]), lmul(DELTA, u[2])))
    res = (ladd(res[0], lmul(ue[0], c_)), ladd(res[1], lmul(ue[1], c_)),
           ladd(res[2], lmul(ue[2], c_)))
    return res


def veq(u, v):
    return all(u[i] == v[i] for i in range(3))


# ── Markov trace → Λ, F ───────────────────────────────────────────────────
def Lam(k):
    """Λ(closure σ₁^k) = A·δ + B·a + C·1 (regular isotopy)."""
    a_, b_, c_ = gpow(k)
    return ladd(lmul(a_, DELTA), lmul(b_, A), c_)


def Fpoly(k):
    """F = a^{−w}Λ, w = k (전부 같은 부호 crossing)."""
    return lmul({(-k, 0): 1}, Lam(k))


# ── Jones 특수화: a=−s⁻³, z=s+s⁻¹ → V ∈ ℤ[t^±], t=s⁴ ──────────────────────
def _poly_div(num, den):
    """정수계수 1변수 다항식 나눗셈(리스트, 낮은 차수부터). 나누어떨어지지 않으면 None."""
    num = list(num)
    dn = len(den) - 1
    while den and den[-1] == 0:
        den = den[:-1]; dn -= 1
    q = [0] * max(0, len(num) - dn)
    for i in range(len(num) - 1, dn - 1, -1):
        if num[i] == 0:
            continue
        if num[i] % den[-1]:
            return None
        c = num[i] // den[-1]
        q[i - dn] = c
        for j, d in enumerate(den):
            num[i - dn + j] -= c * d
    return q if all(v == 0 for v in num) else None


def spec_jones(p):
    """F(a,z) → V(s) ∈ ℤ[s^±] (a=−s⁻³, z=s+s⁻¹). z 음수지수는 (s²+1) 나눗셈으로 해소.
    반환 dict{s지수: 계수} 또는 None(Laurent 아님)."""
    mneg = max([-j for (_, j) in p if j < 0] + [0])
    # (s+s⁻¹)^mneg 를 곱한 뒤 (s²+1)^mneg / s^mneg 로 나눔
    acc = {}
    for (i, j), c in p.items():
        term = {-3 * i: c * (1 if i % 2 == 0 else -1)}      # a^i = (−1)^i s^{−3i}
        e = j + mneg                                         # z^{j}·(s+s⁻¹)^{mneg}
        zz = {0: 1}
        for _ in range(e):
            nz = {}
            for k2, v2 in zz.items():
                nz[k2 + 1] = nz.get(k2 + 1, 0) + v2
                nz[k2 - 1] = nz.get(k2 - 1, 0) + v2
            zz = nz
        for k1, v1 in term.items():
            for k2, v2 in zz.items():
                acc[k1 + k2] = acc.get(k1 + k2, 0) + v1 * v2
    acc = {k: v for k, v in acc.items() if v}
    if mneg == 0:
        return acc
    # acc / ((s²+1)^mneg / s^mneg) = acc·s^mneg / (s²+1)^mneg
    acc = {k + mneg: v for k, v in acc.items()}
    lo = min(acc)
    num = [0] * (max(acc) - lo + 1)
    for k, v in acc.items():
        num[k - lo] = v
    den = [1]
    for _ in range(mneg):
        nd = [0] * (len(den) + 2)
        for i2, d in enumerate(den):
            nd[i2] += d; nd[i2 + 2] += d
        den = nd
    q = _poly_div(num, den)
    if q is None:
        return None
    return {lo + i2: v for i2, v in enumerate(q) if v}


def s_to_t(vs):
    """s 지수 → t 지수(t=s⁴). 4의 배수 아니면 None(반정수 → 링크는 t^{1/2} 필요)."""
    if vs is None:
        return None
    if any(k % 4 for k in vs):
        return None
    return {k // 4: v for k, v in vs.items()}


def fmt(p, va="a", vb="z"):
    return " + ".join(f"{v}·{va}^{i}{vb}^{j}" for (i, j), v in sorted(p.items()))


def fmt1(p, v="t"):
    return None if p is None else " + ".join(f"{c}·{v}^{k}" for k, c in sorted(p.items()))


def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "bmw-kauffman/v1",
           "_note": ("BMW 대수 → Kauffman 2변수 F(a,z) (관측·seal 아님·신규 module 0·root 불변). "
                     "★규약 조건유도(Dubrovnik→Kauffman 오규약 선검출)·BMW₂ 한정 스코프"
                     "(T(2,k) 족; BMW₃/fig-8 미착수)·HOMFLY 비포함은 문헌 사실로 무주장.")}

    # 1. BMW 차원 자체 재유도
    dims = {n: perfect_matchings(list(range(2 * n))) for n in (1, 2, 3, 4)}
    out["bmw_dimensions"] = {str(n): dims[n] for n in dims}
    R["bmw_dim_double_factorial"] = all(dims[n] == double_factorial_odd(n) for n in dims)
    R["bmw3_dim_15"] = (dims[3] == 15)          # report15 "dim 15" 주장 자체검증

    # 2. 규약 자체 정합: a + a⁻¹ = z(δ + 1)
    R["convention_consistent"] = (lmul(Z, ladd(DELTA, ONE)) == ladd(A, AI))
    # g·g⁻¹ = 1
    R["g_ginv_identity"] = veq(mul_ginv(gpow(1)), (ONE, {}, {}))
    # 결합법칙/기저 닫힘: g^i·g^j = g^{i+j}
    R["bmw2_assoc_powers"] = all(
        veq(bmw2_mul(gpow(i), gpow(j)), gpow(i + j))
        for i in range(0, 5) for j in range(0, 5))

    # 3. T(2,k) 족
    KS = list(range(0, 5)) if quick else list(range(0, 7))
    NAMES = {0: "unlink2", 1: "unknot", 2: "hopf", 3: "trefoil",
             4: "T(2,4)", 5: "cinquefoil", 6: "T(2,6)"}
    fam = {}
    for k in KS:
        fam[NAMES.get(k, f"T(2,{k})")] = {"k": k, "Lambda": fmt(Lam(k)), "F": fmt(Fpoly(k))}
    out["torus_family"] = fam
    R["F_unknot_is_1"] = (Fpoly(1) == ONE)

    # 4b. Jones 특수화
    jones = {}
    for k in KS:
        vs = spec_jones(Fpoly(k))
        vt = s_to_t(vs)
        jones[NAMES.get(k, f"T(2,{k})")] = {
            "V_in_t": fmt1(vt),
            "V_in_s_halfinteger": None if vt is not None else fmt1(vs, "s"),
        }
    out["jones_specialization"] = jones
    # 매듭(홀수 k)은 ℤ[t^±], 링크(짝수 k)는 t^{1/2} 필요 → s 로 표기
    R["jones_knots_integral_t"] = all(
        s_to_t(spec_jones(Fpoly(k))) is not None for k in KS if k % 2 == 1)
    R["jones_links_need_sqrt_t"] = all(
        s_to_t(spec_jones(Fpoly(k))) is None and spec_jones(Fpoly(k)) is not None
        for k in KS if k % 2 == 0 and k > 0)

    # ★v13 kauffman_bracket 오라클 대조 (mirror 관계)
    vt_tref = s_to_t(spec_jones(Fpoly(3)))
    R["jones_trefoil_right"] = (vt_tref == {1: 1, 3: 1, 4: -1})     # t + t³ − t⁴
    if not quick:
        import sympy as sp
        from qf_witness.observe import kauffman_bracket_observe as kb
        t = sp.symbols("t")
        v_kb = kb.jones_in_t(kb.TREFOIL, -3)                        # v13 left-handed
        ours = sum(c * t ** k for k, c in vt_tref.items())
        R["oracle_cross_v13_mirror"] = bool(
            sp.simplify(v_kb - ours.subs(t, 1 / t)) == 0)
        out["oracle_cross"] = {
            "v13_kauffman_bracket_trefoil": str(sp.simplify(v_kb)),
            "ours_right_handed": fmt1(vt_tref),
            "relation": "mirror (t ↔ 1/t) — 본 축은 positive braid(right), v13 은 left",
        }

    # 4c. HOMFLY 동시 산출 (v14 P2 모듈 직접 호출)
    if not quick:
        from qf_witness.observe import homfly_hecke_observe as hh
        P_tref = hh.homfly(2, [1, 1, 1])
        out["homfly_same_object"] = {
            "trefoil_HOMFLY": str(hh._as_az(P_tref)) if hasattr(hh, "_as_az") else str(P_tref),
            "trefoil_KAUFFMAN_F": fmt(Fpoly(3)),
            "note": ("같은 대상의 서로 다른 불변량 동시 산출 — 상호 비포함(Red-Hoffman)은 "
                     "문헌 사실이며 본 witness 는 재증명하지 않음"),
        }
        R["homfly_module_callable"] = bool(P_tref)

    # 5. mirror: F(L*)(a,z) = F(L)(a⁻¹,z)
    def mirror_a(p):
        return {(-i, j): c for (i, j), c in p.items()}
    R["mirror_relation"] = all(
        Fpoly(-k) == mirror_a(Fpoly(k)) for k in (1, 2, 3, 4))

    # teeth
    # ★(i) δ 오염 — unknot(k=1)은 A-계수가 0 이라 δ 에 무감(검출력 없음, 실측으로 확인)
    #     ⟹ 규약 정합식 + A-계수 비영인 Hopf(k=2) 로 검출
    bad_delta = ladd(DELTA, ONE)

    def Lam_with(k, dlt):
        a_, b_, c_ = gpow(k)
        return ladd(lmul(a_, dlt), lmul(b_, A), c_)

    R["teeth_delta_tamper"] = (
        lmul(Z, ladd(bad_delta, ONE)) != ladd(A, AI)          # 규약 정합 붕괴
        and Lam_with(2, bad_delta) != Lam(2))                 # Hopf 값 변화
    # tr(g)=a → 1 로 오염하면 Jones 대조 붕괴
    a3, b3, c3 = gpow(3)
    lam_bad = ladd(lmul(a3, DELTA), b3, c3)
    R["teeth_trace_tamper"] = (
        s_to_t(spec_jones(lmul({(-3, 0): 1}, lam_bad))) != vt_tref)
    # ★Dubrovnik 규약 재현 → Jones 특수화 Laurent 아님
    delta_dub = ladd(lmul(ladd(A, lsc(-1, AI)), ZI), ONE)
    R["teeth_dubrovnik_not_laurent"] = (spec_jones(delta_dub) is None)

    ok = bool(all(R.values()))
    out["checks"] = R
    out["scope_honesty"] = {
        "covered": "BMW₂(dim 3) · T(2,k) 토러스 링크족 k=0..6",
        "not_covered": ["BMW₃(dim 15) Kauffman tangle 곱셈", "fig-8 등 3-braid 대상",
                        "HOMFLY/Kauffman 상호 비포함 재증명"],
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "BMW-KAUFFMAN.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("BMW → Kauffman 2변수 F(a,z) 관측 (exact Laurent — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  ★BMW 차원 자체유도: {out['bmw_dimensions']} = (2n−1)!!", flush=True)
        print(f"  F(trefoil) = {fam['trefoil']['F']}", flush=True)
        print(f"  ★Jones(trefoil) = {jones['trefoil']['V_in_t']} "
              f"(v13 오라클과 mirror 일치={R.get('oracle_cross_v13_mirror')})", flush=True)
        print("  ★정직: BMW₂/T(2,k) 한정 · BMW₃·fig-8 미착수 · 비포함 무주장", flush=True)
        print("  → .pgf/proofs/BMW-KAUFFMAN.json", flush=True)
    print(f"bmw_kauffman_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
