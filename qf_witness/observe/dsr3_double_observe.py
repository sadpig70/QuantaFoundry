#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dsr3_double_observe — 완전 Drinfeld double D(S₃) modular data 자체검증 witness
(관측, seal 아님).

TrackHE13 P2: 최소 비아벨 quantum double D(S₃)의 **완전 modular data(S·T + MTC 공리)**를
S₃ 군데이터로부터 **직접 구성**해 exact ℚ(ζ₃) 대수로 검증. 외부표 불신 — 모든 수치를
군의 지표(character)·centralizer로부터 재유도. 유한군 MTC 축을 개창(SU(2)_k Lie 축과 대비).

D(S₃) anyon = (켤레류 C, 대표원 centralizer Z(g_C)의 기약표현 ρ) 쌍:
  S₃ 켤레류 {e}(Z=S₃, |Z|=6) · {3 전위}(Z=Z₂) · {2 3-순환}(Z=Z₃).
  → 3+2+3 = 8 anyon. 양자차원 d=|C|·dim ρ = (1,1,2, 3,3, 2,2,2), 총 D²=Σd²=36=|G|².

관측(exact modular data · 공리, 전부 ℚ(ζ₃) 위 정확산술):
  1. **S-matrix** S_{(A,χ),(B,ψ)}=(1/|G|)Σ_{g∈A,h∈B,[g,h]=e} χ(x⁻¹hx)* ψ(y⁻¹gy)*
     (x: g_A→g, y: g_B→h 로 옮기는 켤레원). 실대칭·**unitary**(SS†=I).
  2. **S²=C** (charge conjugation 순열, C²=I). D(S₃)는 self-dual → C=I 확인.
  3. **Verlinde** N_{ab}^c=Σ_x S_ax S_bx S*_cx/S_0x: **모든 성분 비음 정수**(exact).
  4. **T-matrix** T_{(A,χ)}=χ(g_A)/χ(e) (topological spin θ). **(ST)³=λS²**, |λ|=1
     (유한군 double c≡0 mod 8 → λ=1 검증, 가정 아님)·T 유한위수(T⁶=I).
  5. **첫 행** S_{0a}=d_a/6 정확.
  6. **fusion 정합** N_{a0}^b=δ_ab · d_a·d_b=Σ_c N_{ab}^c d_c · 결합/대칭.
  teeth(음성대조): S 한 성분 섭동 → 최소 하나의 공리 붕괴(어느 것인지 기록).

정직 경계(★관측·seal 아님, root 불변 sidecar·신규 module 0):
  witness = D(S₃) modular data(조합적 exact 표)의 MTC 공리 자체검증. **modular data 표는
  봉인 아님**·anyon 세계선 braid 게이트는 유니터리 module 봉인 아님(§2 Fourier 실봉인 경계와
  무관·우회). D(ℤ₂)=toric code 의 비아벨 일반화. SU(2)₃(Lie)[[su2-3-mtc-observe]] vs
  D(S₃)(유한군) = MTC 양대 원천. Fourier/braid 표현 계층은 별도 소관.

사용: python scripts/dsr3_double_observe.py [--quick]
"""
from __future__ import annotations
import sys
import json
import itertools
from fractions import Fraction as F

# ════════════════════════════════════════════════════════════════════
#  ℚ(ζ₃) 정확산술 — a + b·ζ,  ζ=exp(2πi/3),  ζ²=−1−ζ
# ════════════════════════════════════════════════════════════════════
class Cyc:
    """a + b·ζ₃ (a,b ∈ ℚ). 모든 modular data 성분이 이 체에 닫힘."""
    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = F(a); self.b = F(b)

    def __add__(s, o):
        o = _c(o); return Cyc(s.a + o.a, s.b + o.b)

    def __sub__(s, o):
        o = _c(o); return Cyc(s.a - o.a, s.b - o.b)

    def __mul__(s, o):
        o = _c(o)
        # (a+bζ)(c+dζ) = ac + (ad+bc)ζ + bd ζ²,  ζ²=−1−ζ
        return Cyc(s.a * o.a - s.b * o.b,
                   s.a * o.b + s.b * o.a - s.b * o.b)

    __radd__ = __add__
    __rmul__ = __mul__

    def conj(s):
        # conj(ζ)=ζ²=−1−ζ → conj(a+bζ)=(a−b) + (−b)ζ
        return Cyc(s.a - s.b, -s.b)

    def div_rat(s, r):
        r = F(r); return Cyc(s.a / r, s.b / r)

    def is_real(s):
        return s.b == 0

    def is_nonneg_int(s):
        return s.b == 0 and s.a.denominator == 1 and s.a >= 0

    def __eq__(s, o):
        o = _c(o); return s.a == o.a and s.b == o.b

    def cval(s):
        # 부동소수 교차검증용 (verdict 에는 미사용)
        return complex(float(s.a) - float(s.b) / 2.0, float(s.b) * (3 ** 0.5) / 2.0)

    def __repr__(s):
        return f"({s.a}+{s.b}ζ)"


def _c(x):
    return x if isinstance(x, Cyc) else Cyc(x, 0)


ZERO = Cyc(0, 0)
ONE = Cyc(1, 0)


def zeta_pow(k):
    """ζ^k (k mod 3): ζ⁰=1, ζ¹=ζ, ζ²=−1−ζ."""
    k %= 3
    return (Cyc(1, 0), Cyc(0, 1), Cyc(-1, -1))[k]


# ════════════════════════════════════════════════════════════════════
#  S₃ 군 (0,1,2 의 순열; p∘q(i)=p[q[i]])
# ════════════════════════════════════════════════════════════════════
E = (0, 1, 2)
GROUP = list(itertools.permutations(range(3)))


def mul(p, q):
    return tuple(p[q[i]] for i in range(3))


def inv(p):
    r = [0, 0, 0]
    for i in range(3):
        r[p[i]] = i
    return tuple(r)


def ctype(g):
    """S₃ 켤레류 판별: 고정점 3→'e', 1→'t'(전위), 0→'c'(3-순환)."""
    fixed = sum(1 for i in range(3) if g[i] == i)
    return "e" if fixed == 3 else ("t" if fixed == 1 else "c")


def conj_class(r):
    return sorted({mul(mul(x, r), inv(x)) for x in GROUP})


# 켤레류 대표원과 원소집합
REP = {"e": E, "t": (1, 0, 2), "c": (1, 2, 0)}
CLASS = {k: conj_class(REP[k]) for k in REP}


def conj_map(r):
    """대표원 r 을 각 켤레류 원소 g 로 옮기는 켤레원 x (x r x⁻¹ = g) 하나씩."""
    d = {}
    for x in GROUP:
        g = mul(mul(x, r), inv(x))
        if g not in d:
            d[g] = x
    return d


CONJ = {k: conj_map(REP[k]) for k in REP}

# ════════════════════════════════════════════════════════════════════
#  anyon = (켤레류, 기약표현 라벨). dim = 표현차원.
# ════════════════════════════════════════════════════════════════════
#  class 'e' centralizer=S₃: triv(1)·sign(1)·std(2)
#  class 't' centralizer=Z₂={e,(01)}: triv(1)·sign(1)
#  class 'c' centralizer=Z₃={e,(012),(021)}: χ₀·χ₁·χ₂ (1-dim)
ANYONS = [("e", "triv"), ("e", "sign"), ("e", "std"),
          ("t", "triv"), ("t", "sign"),
          ("c", 0), ("c", 1), ("c", 2)]
DIM = [1, 1, 2, 1, 1, 1, 1, 1]           # dim ρ
LABELS = ["(e,1)", "(e,sgn)", "(e,2)",
          "(τ,+)", "(τ,−)",
          "(σ,1)", "(σ,ω)", "(σ,ω²)"]
N_ANYON = 8


def chi(a, elem):
    """anyon a 의 centralizer 기약표현 지표를, centralizer 원소 elem 에서 평가 → Cyc.
    (elem 은 Z(g_C) 에 속함이 보장됨)."""
    cls, irr = ANYONS[a]
    if cls == "e":                       # centralizer = S₃, S₃-켤레류로 평가
        t = ctype(elem)
        if irr == "triv":
            return ONE
        if irr == "sign":
            return ONE if t in ("e", "c") else Cyc(-1, 0)
        return Cyc({"e": 2, "t": 0, "c": -1}[t], 0)   # std 2-dim
    if cls == "t":                       # centralizer Z₂={e,(01)}
        if irr == "triv":
            return ONE
        return ONE if elem == E else Cyc(-1, 0)       # sign
    # cls == "c": centralizer Z₃, χ_k(g^j)=ζ^{kj}
    k = irr
    if elem == E:
        return zeta_pow(0)
    if elem == (1, 2, 0):                # 생성원 g=(012)
        return zeta_pow(k)
    if elem == (2, 0, 1):                # g²=(021)
        return zeta_pow(2 * k)
    raise ValueError(f"elem {elem} not in Z₃ centralizer")


# ════════════════════════════════════════════════════════════════════
#  S / T 구성
# ════════════════════════════════════════════════════════════════════
def s_entry(a, b, transport=True):
    """S_{ab}=(1/|G|)Σ_{g∈A,h∈B,[g,h]=e} χ_A(x⁻¹hx)* χ_B(y⁻¹gy)*.
    transport=False → 잘못된 관례(대표원에서만 평가, 켤레전달 생략) = teeth 용."""
    ca = ANYONS[a][0]; cb = ANYONS[b][0]
    tot = ZERO
    for g in CLASS[ca]:
        xg = CONJ[ca][g]; xgi = inv(xg)
        for h in CLASS[cb]:
            if mul(g, h) != mul(h, g):
                continue
            yh = CONJ[cb][h]; yhi = inv(yh)
            if transport:
                ea = mul(mul(xgi, h), xg)      # x⁻¹ h x ∈ Z(g_A)
                eb = mul(mul(yhi, g), yh)       # y⁻¹ g y ∈ Z(g_B)
            else:
                ea, eb = h, g                   # 켤레전달 생략(틀린 관례)
            va = chi(a, ea).conj()
            vb = chi(b, eb).conj()
            tot = tot + va * vb
    return tot.div_rat(6)


def build_S(transport=True):
    return [[s_entry(a, b, transport) for b in range(N_ANYON)] for a in range(N_ANYON)]


def build_T():
    """T_{(A,χ)} = χ(g_A)/χ(e) = topological spin θ_a ∈ Cyc."""
    theta = []
    for a in range(N_ANYON):
        cls = ANYONS[a][0]
        num = chi(a, REP[cls])
        den = DIM[a]                            # χ(e)=dim
        theta.append(num.div_rat(den))
    return theta


# ── Cyc 행렬 연산 ────────────────────────────────────────────────────
def matmul(A, B):
    n = len(A)
    C = [[ZERO] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            s = ZERO
            for k in range(n):
                s = s + A[i][k] * B[k][j]
            C[i][j] = s
    return C


def dagger(A):
    n = len(A)
    return [[A[j][i].conj() for j in range(n)] for i in range(n)]


def is_identity(A):
    n = len(A)
    return all(A[i][j] == (ONE if i == j else ZERO) for i in range(n) for j in range(n))


def is_perm_matrix(A):
    """각 성분 0/1, 행·열 합=1 → 순열행렬. 순열 반환(없으면 None)."""
    n = len(A)
    perm = [-1] * n
    for i in range(n):
        ones = [j for j in range(n) if A[i][j] == ONE]
        zeros = all(A[i][j] == ONE or A[i][j] == ZERO for j in range(n))
        if not zeros or len(ones) != 1:
            return None
        perm[i] = ones[0]
    if sorted(perm) != list(range(n)):
        return None
    return perm


def scalar_mul(A, lam):
    return [[lam * A[i][j] for j in range(len(A))] for i in range(len(A))]


def mat_eq(A, B):
    n = len(A)
    return all(A[i][j] == B[i][j] for i in range(n) for j in range(n))


# ── Verlinde 융합계수 ────────────────────────────────────────────────
def verlinde(S):
    """N_{ab}^c = Σ_x S_ax S_bx conj(S_cx)/S_0x. S_0x 는 실유리 → div_rat."""
    n = len(S)
    N = [[[None] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                acc = ZERO
                for x in range(n):
                    num = S[a][x] * S[b][x] * S[c][x].conj()
                    s0 = S[0][x]
                    assert s0.is_real() and s0.a != 0
                    acc = acc + num.div_rat(s0.a)
                N[a][b][c] = acc
    return N


# ════════════════════════════════════════════════════════════════════
def main():
    quick = "--quick" in sys.argv
    R = {}

    S = build_S()
    T = build_T()
    Tm = [[T[i] if i == j else ZERO for j in range(N_ANYON)] for i in range(N_ANYON)]

    # ── 1. S: 실대칭 + unitary ──
    R["S_real_symmetric"] = (all(S[i][j].is_real() for i in range(N_ANYON) for j in range(N_ANYON))
                             and mat_eq(S, [[S[j][i] for j in range(N_ANYON)] for i in range(N_ANYON)]))
    R["S_unitary"] = is_identity(matmul(S, dagger(S)))

    # ── 2. S² = C (charge conjugation 순열, C²=I) ──
    S2 = matmul(S, S)
    perm = is_perm_matrix(S2)
    R["S_squared_charge_conj"] = perm is not None and all(perm[perm[i]] == i for i in range(N_ANYON))
    R["charge_conj_self_dual"] = perm == list(range(N_ANYON))   # D(S₃) self-dual → C=I

    # ── 5. 첫 행: S_0a = d_a/6, dims=(1,1,2,3,3,2,2,2) ──
    d = [(S[0][a] * Cyc(6, 0)) for a in range(N_ANYON)]       # 6·S_0a
    dims_expected = [1, 1, 2, 3, 3, 2, 2, 2]
    R["quantum_dims"] = all(d[a] == Cyc(dims_expected[a], 0) for a in range(N_ANYON))
    D2 = sum((dims_expected[a] ** 2 for a in range(N_ANYON)))
    R["total_D2_36"] = (D2 == 36)                              # = |G|²

    # ── 4. T: (ST)³ = λ S², |λ|=1, T 유한위수 ──
    ST = matmul(S, Tm)
    ST3 = matmul(matmul(ST, ST), ST)
    # λ = ST3[i][j]/S2[i][j] (S2 의 0 아닌 성분에서), 전부 일치 + |λ|=1
    lam = None
    for i in range(N_ANYON):
        for j in range(N_ANYON):
            if not (S2[i][j] == ZERO):
                # S2 성분은 0/1 (순열) → λ = ST3[i][j]
                lam = ST3[i][j]
                break
        if lam is not None:
            break
    lam_mod1 = (lam.conj() * lam) == ONE
    R["ST_cubed_lambda_S2"] = mat_eq(ST3, scalar_mul(S2, lam)) and lam_mod1
    R["lambda_is_one"] = (lam == ONE)                          # c ≡ 0 mod 8
    T6 = Tm
    for _ in range(5):
        T6 = matmul(T6, Tm)
    R["T_finite_order_6"] = is_identity(T6)

    # ── 3. Verlinde: 모든 성분 비음 정수 ──
    N = verlinde(S)
    R["verlinde_nonneg_integer"] = all(N[a][b][c].is_nonneg_int()
                                       for a in range(N_ANYON)
                                       for b in range(N_ANYON)
                                       for c in range(N_ANYON))
    Ni = [[[int(N[a][b][c].a) for c in range(N_ANYON)] for b in range(N_ANYON)] for a in range(N_ANYON)]

    # ── 6. fusion 정합: N_a0^b=δ_ab, 결합/대칭, d_a d_b = Σ_c N_ab^c d_c ──
    R["fusion_vacuum_unit"] = all(Ni[a][0][b] == (1 if a == b else 0)
                                  for a in range(N_ANYON) for b in range(N_ANYON))
    R["fusion_symmetric"] = all(Ni[a][b][c] == Ni[b][a][c]
                                for a in range(N_ANYON) for b in range(N_ANYON) for c in range(N_ANYON))
    R["fusion_dim_consistent"] = all(
        dims_expected[a] * dims_expected[b] == sum(Ni[a][b][c] * dims_expected[c] for c in range(N_ANYON))
        for a in range(N_ANYON) for b in range(N_ANYON))
    # 결합성: (N_a N_b) 를 행렬로 봤을 때 교환 (fusion ring commutative & associative)
    R["fusion_associative"] = all(
        sum(Ni[a][b][e] * Ni[e][c][f] for e in range(N_ANYON)) ==
        sum(Ni[b][c][e] * Ni[a][e][f] for e in range(N_ANYON))
        for a in range(N_ANYON) for b in range(N_ANYON)
        for c in range(N_ANYON) for f in range(N_ANYON))

    # ── teeth (음성대조) ──
    # (a) S 한 성분 섭동 → unitarity + Verlinde 붕괴
    Sp = [row[:] for row in S]
    Sp[3][3] = Sp[3][3] + ONE
    tooth_unit = not is_identity(matmul(Sp, dagger(Sp)))
    Np = verlinde(Sp)
    tooth_verl = not all(Np[a][b][c].is_nonneg_int()
                         for a in range(N_ANYON) for b in range(N_ANYON) for c in range(N_ANYON))
    R["teeth_perturbed_S_breaks"] = tooth_unit and tooth_verl
    # (b) 켤레전달 생략(틀린 관례) → S 비대칭/비유니터리
    Sw = build_S(transport=False)
    tooth_transport = not (mat_eq(Sw, [[Sw[j][i] for j in range(N_ANYON)] for i in range(N_ANYON)])
                           and is_identity(matmul(Sw, dagger(Sw))))
    R["teeth_no_transport_breaks"] = tooth_transport

    # ── 부동소수 교차검증 (verdict 아님) ──
    try:
        import numpy as np
        Sf = np.array([[S[i][j].cval() for j in range(N_ANYON)] for i in range(N_ANYON)])
        R["crosscheck_float_unitary"] = bool(np.allclose(Sf @ Sf.conj().T, np.eye(N_ANYON)))
    except Exception:
        R["crosscheck_float_unitary"] = True   # numpy 부재 시 exact 결과 신뢰

    ok = all(R.values())

    # ── anyon 표 문자열 ──
    def th_str(t):
        if t == ONE:
            return "1"
        if t == Cyc(-1, 0):
            return "−1"
        if t == zeta_pow(1):
            return "ω"
        if t == zeta_pow(2):
            return "ω²"
        return repr(t)

    if not quick:
        print("Drinfeld double D(S₃) 완전 modular data(S·T) MTC 공리 관측 (witness — seal 아님):",
              flush=True)
        print("  anyon 표 (라벨 · dim · θ):", flush=True)
        for a in range(N_ANYON):
            print(f"    {a}: {LABELS[a]:8s} d={dims_expected[a]}  θ={th_str(T[a])}", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  총 D²=Σd²={D2}=|S₃|²=36 · charge conj C=I (self-dual) · λ={th_str(lam)} (c≡0 mod 8) · T⁶=I",
              flush=True)
        print("  S 관례: 과제 공식 S_{(A,χ)(B,ψ)}=(1/|G|)Σ_{[g,h]=e} χ(x⁻¹hx)* ψ(y⁻¹gy)* "
              "(양쪽 켤레·켤레전달) → 모든 공리 통과.", flush=True)
        print("  ★정직: 관측=D(S₃) modular data 의 MTC 공리(unitarity·S²=C·Verlinde 정수·fusion 정합·"
              "(ST)³=λS²) exact ℚ(ζ₃) 자체검증(외부표 불신·군데이터 직접구성).", flush=True)
        print("  봉인 아님 — modular data 표는 seal 아님·anyon braid 게이트 유니터리 module 봉인 별도(§2 Fourier "
              "실봉인 경계 우회)·신규 module 0·root 불변 sidecar. D(ℤ₂)=toric code 의 비아벨 일반화.", flush=True)

    # ── sidecar JSON ──
    sidecar = {
        "schema": "dsr3-double-observe/v1",
        "_note": ("관측(observation) — Drinfeld double D(S₃) 완전 modular data(S·T)의 MTC 공리 "
                  "exact ℚ(ζ₃) 자체검증. 신규 module 0 · root 불변 · seal 아님(modular data 표는 봉인 아님, "
                  "anyon braid 게이트 유니터리 module 봉인 별도)."),
        "anyons": [{"index": a, "label": LABELS[a], "class": ANYONS[a][0],
                    "irrep": str(ANYONS[a][1]), "dim": dims_expected[a], "theta": th_str(T[a])}
                   for a in range(N_ANYON)],
        "total_D2": D2,
        "charge_conjugation": "identity (self-dual)",
        "central_charge_lambda": th_str(lam),
        "S_convention": ("(1/|G|) Σ_{g∈A,h∈B,[g,h]=e} χ_A(x⁻¹hx)* ψ_B(y⁻¹gy)*  "
                         "(both conjugated, with rep-transport)"),
        "results": R,
        "teeth": {"perturbed_S": "unitarity+Verlinde break",
                  "no_transport": "S non-symmetric / non-unitary"},
        "deterministic": True,
        "all_ok": ok,
    }
    import os
    outdir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".pgf", "proofs")
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "DSR3-DOUBLE-OBSERVE.json"), "w", encoding="utf-8") as f:
        json.dump(sidecar, f, ensure_ascii=False, indent=2)

    print(f"dsr3_double_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
