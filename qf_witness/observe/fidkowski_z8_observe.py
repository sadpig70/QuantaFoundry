#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fidkowski_z8_observe — TrackHE14 P4b: Fidkowski-Kitaev ℤ→ℤ₈ 붕괴 (상호작용 SPT 최초 진입,
관측, seal 아님). ★전 과정 ℚ(i) 정확산술(float 0).

1D class BDI(T²=+1) 자유페르미온 분류 ℤ(Majorana chain winding) 가 상호작용 하에서 ℤ₈ 로
붕괴한다는 Fidkowski-Kitaev 구조의 **관측 코어**를 edge Majorana 유효이론(0D, n Majorana)에서
정확산술로 실증한다:

  γ_a: Jordan-Wigner 정확행렬(성분 ∈ {0,±1,±i}), n Majorana = ⌈n/2⌉ qubit (dim 2^⌈n/2⌉).
  T = U_n K,  U_n = ∏(짝수번 γ) — T γ_a T⁻¹ = +γ_a ∀a (BDI edge 작용, 전부 정확검증).

관측 4계층 (전부 exact):
  1. ★T² mod-8 시그니처: T² = U_n U_n* = ±1 이 n=2,4,6,8 에서 (−1,−1,+1,+1) —
     n=2,4 는 **Kramers**(T²=−1) → 어떤 T-불변 H 도 전 스펙트럼 짝수겹.
  2. ★자유(비상호작용) 장벽: 2차항 iγ_aγ_b 전부(28개) T-odd — 어떤 quadratic mass 도
     T 를 깨지 않고는 불가 = 자유 분류 ℤ 의 이유.
  3. ★n=4 quartic 불가 **전수**: 짝수 연산자 기저(1·2차·4차 전수 판정)에서 T-불변 span =
     {1, γ₁γ₂γ₃γ₄} 뿐 → 임의 T-불변 H = a+bΓ, 스펙트럼 {a±b} 각 2겹(Γ²=1·trΓ=0·Γ≠±1) —
     상호작용(quartic)으로도 축퇴 해소 불가(Kramers 정합).
  4. ★n=8 gappable **구성**: 두 quartet 의 so(4)=su(2)⊕su(2) 자기쌍대 pseudospin
     A⃗⁽¹⁾·A⃗⁽²⁾ Heisenberg (A_i=½(M_bc+M_ad), M_ab=−(i/2)γ_aγ_b):
       W = Σ_i A_i⁽¹⁾A_i⁽²⁾ — T-불변·★순수 4차(γ-기저 256 성분 전수: |S|=4 만 비영)·
       소멸다항식 W(W+¾)(W−¼)=0 + 모멘트(tr W·tr W²)로 중복도 (1,12,3) 유일해 →
       **unique GS(E=−¾)·gap=¾ 정확**. GS projector P₀=W(W−¼)·(4/3): P₀²=P₀·tr=1·
       T-불변 → GS 는 T-singlet(대칭 자발깨짐 없음).
  ⟹ 8 = 최초 gappable: ℤ→ℤ₈ 붕괴의 관측 코어(4 불가 전수 + 8 가능 구성 + 2차 전면 금지).

teeth (전부 exact): (i) W+iγ₁γ₂ → T-불변 붕괴 검출 (ii) n=4 에 T-깨는 2차 H=iγ₁γ₂+2iγ₃γ₄ →
  4준위 전부 비축퇴(projector trace 1) — 보호는 T 가 load-bearing (iii) W 섭동(+⅛γ₁γ₂γ₃γ₄) →
  소멸다항식 위반 검출(스펙트럼 certificate 의 이빨).

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0): 관측 = "n=4 불가(전수)·n=8 가능
  (구성)·quadratic 전면 금지·T² mod-8 시그니처" — **전체 ℤ₈ 분류(n=1..7 모든 보호·8k 주기성)는
  무주장**(n=6 비전수·1D 격자 전체 무주장, 0D edge 유효이론 한정). W 구성은 존재증명
  (구성≠유일성). 상호작용 SPT 축 최초 진입.

사용: python -m qf_witness.observe.fidkowski_z8_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import itertools
from fractions import Fraction as F


# ════════════════════════════════════════════════════════════════════
#  ℚ(i) 정확산술 (dtw_z2z2_double_observe 와 동일 Cyc)
# ════════════════════════════════════════════════════════════════════
class Cyc:
    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = F(a); self.b = F(b)

    def __add__(s, o):
        o = _c(o); return Cyc(s.a + o.a, s.b + o.b)

    def __sub__(s, o):
        o = _c(o); return Cyc(s.a - o.a, s.b - o.b)

    def __mul__(s, o):
        o = _c(o)
        return Cyc(s.a * o.a - s.b * o.b, s.a * o.b + s.b * o.a)

    __radd__ = __add__
    __rmul__ = __mul__

    def conj(s):
        return Cyc(s.a, -s.b)

    def __eq__(s, o):
        o = _c(o); return s.a == o.a and s.b == o.b

    def __hash__(s):
        return hash((s.a, s.b))

    def __repr__(s):
        return f"({s.a}{'+' if s.b >= 0 else ''}{s.b}i)"


def _c(x):
    return x if isinstance(x, Cyc) else Cyc(x, 0)


ZERO = Cyc(0, 0)
ONE = Cyc(1, 0)
I = Cyc(0, 1)


# ── 행렬 유틸 (list-of-list Cyc) ─────────────────────────────────────
def mat(rows):
    return [[_c(x) for x in r] for r in rows]


def eye(n):
    return [[ONE if i == j else ZERO for j in range(n)] for i in range(n)]


def mzero(n):
    return [[ZERO] * n for _ in range(n)]


def madd(A, B):
    n = len(A); return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]


def msub(A, B):
    n = len(A); return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]


def smul(c, A):
    c = _c(c); return [[c * x for x in r] for r in A]


def mmul(A, B):
    n = len(A); C = [[ZERO] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            aik = A[i][k]
            if aik == ZERO:
                continue
            for j in range(n):
                if B[k][j] != ZERO:
                    C[i][j] = C[i][j] + aik * B[k][j]
    return C


def kron(A, B):
    na, nb = len(A), len(B)
    C = [[ZERO] * (na * nb) for _ in range(na * nb)]
    for i in range(na):
        for j in range(na):
            if A[i][j] == ZERO:
                continue
            for k in range(nb):
                for l in range(nb):
                    C[i * nb + k][j * nb + l] = A[i][j] * B[k][l]
    return C


def dag(A):
    n = len(A); return [[A[j][i].conj() for j in range(n)] for i in range(n)]


def conj_m(A):
    return [[x.conj() for x in r] for r in A]


def meq(A, B):
    n = len(A)
    return all(A[i][j] == B[i][j] for i in range(n) for j in range(n))


def is_zero(A):
    return all(x == ZERO for r in A for x in r)


def tr(A):
    t = ZERO
    for i in range(len(A)):
        t = t + A[i][i]
    return t


def tr_prod(A, B):
    """tr(A·B) — O(n²)."""
    n = len(A); t = ZERO
    for i in range(n):
        for j in range(n):
            if A[i][j] != ZERO and B[j][i] != ZERO:
                t = t + A[i][j] * B[j][i]
    return t


PX = mat([[0, 1], [1, 0]])
PY = [[ZERO, Cyc(0, -1)], [I, ZERO]]
PZ = mat([[1, 0], [0, -1]])
I2 = eye(2)


def gammas(n):
    """n Majorana (n 짝수) on ⌈n/2⌉ qubits — JW: γ_{2j+1}=Z..ZX, γ_{2j+2}=Z..ZY (1-based)."""
    nq = n // 2
    gs = []
    for j in range(nq):
        for P in (PX, PY):
            M = eye(1)
            for l in range(nq):
                M = kron(M, PZ if l < j else (P if l == j else I2))
            gs.append(M)
    return gs


def U_T(gs):
    """U = ∏(짝수번 γ) — T=U·K 가 모든 γ 를 +γ 로 고정."""
    U = eye(len(gs[0]))
    for i in range(1, len(gs), 2):
        U = mmul(U, gs[i])
    return U


def Uinv(U):
    """U 는 γ 곱 = 유니터리·모노미얼 → U⁻¹ = U†."""
    return dag(U)


def T_conj(U, M):
    return mmul(mmul(U, conj_m(M)), Uinv(U))


def T_sq_sign(U):
    """T² = U·U* = ±1 판정. ±1 아니면 None."""
    S = mmul(U, conj_m(U))
    n = len(S)
    if meq(S, eye(n)):
        return 1
    if meq(S, smul(Cyc(-1), eye(n))):
        return -1
    return None


# ════════════════════════════════════════════════════════════════════
#  검증 계층
# ════════════════════════════════════════════════════════════════════
def check_clifford(gs):
    n = len(gs); d = len(gs[0])
    for a in range(n):
        if not meq(gs[a], dag(gs[a])):
            return False
        if not meq(mmul(gs[a], gs[a]), eye(d)):
            return False
        for b in range(a + 1, n):
            if not is_zero(madd(mmul(gs[a], gs[b]), mmul(gs[b], gs[a]))):
                return False
    return True


def quadratics_T_odd(gs, U):
    """모든 iγ_aγ_b 가 T-odd (T q T⁻¹ = −q)."""
    n = len(gs)
    for a in range(n):
        for b in range(a + 1, n):
            q = smul(I, mmul(gs[a], gs[b]))
            if not meq(T_conj(U, q), smul(Cyc(-1), q)):
                return False
    return True


def n4_exhaustive(gs4, U4):
    """n=4 (dim 4): 짝수 연산자 기저 전수 → T-불변 span = {1, Γ₄}. 결과 dict."""
    d = 4
    basis = [("1", eye(d))]
    for a in range(4):
        for b in range(a + 1, 4):
            basis.append((f"ig{a+1}g{b+1}", smul(I, mmul(gs4[a], gs4[b]))))
    G4 = mmul(mmul(gs4[0], gs4[1]), mmul(gs4[2], gs4[3]))
    basis.append(("g1234", G4))
    inv_flags = {name: meq(T_conj(U4, M), M) for name, M in basis}
    invariant_names = sorted(n for n, f in inv_flags.items() if f)
    # Γ₄ 스펙트럼: Γ²=1·trΓ=0·Γ≠±1 → 고유값 ±1 각 2 → 임의 a+bΓ 는 2겹
    g_ok = (meq(mmul(G4, G4), eye(d)) and tr(G4) == ZERO
            and not meq(G4, eye(d)) and not meq(G4, smul(Cyc(-1), eye(d))))
    return {
        "invariant_span": invariant_names,
        "span_is_1_and_g1234": invariant_names == ["1", "g1234"],
        "gamma1234_pm1_twofold": g_ok,
        "hermitian_g1234": meq(G4, dag(G4)),
    }


def build_W(gs):
    """W = Σ_i A_i⁽¹⁾A_i⁽²⁾ — 두 quartet 자기쌍대 su(2) Heisenberg."""
    half = Cyc(F(1, 2))

    def M(a, b):
        return smul(Cyc(0, F(-1, 2)), mmul(gs[a], gs[b]))

    def spin(q):
        a, b, c, d = q
        return [smul(half, madd(M(b, c), M(a, d))),
                smul(half, madd(M(c, a), M(b, d))),
                smul(half, madd(M(a, b), M(c, d)))]

    A1 = spin([0, 1, 2, 3])
    A2 = spin([4, 5, 6, 7])
    W = mzero(len(gs[0]))
    for i in range(3):
        W = madd(W, mmul(A1[i], A2[i]))
    return W, A1, A2


def su2_check(A):
    """[A1,A2]=iA3 (+순환)."""
    for i in range(3):
        j, k = (i + 1) % 3, (i + 2) % 3
        comm = msub(mmul(A[i], A[j]), mmul(A[j], A[i]))
        if not meq(comm, smul(I, A[k])):
            return False
    return True


def annihilating_ok(W):
    """W(W+¾)(W−¼) = 0 exact."""
    n = len(W)
    P = mmul(mmul(W, madd(W, smul(Cyc(F(3, 4)), eye(n)))),
             msub(W, smul(Cyc(F(1, 4)), eye(n))))
    return is_zero(P)


def multiplicities(W):
    """고유값 {−¾,0,¼} 중복도 — Σm=16·Σmλ=trW·Σmλ²=trW² 유일해(정확)."""
    t1 = tr(W); t2 = tr_prod(W, W)
    if not (t1.b == 0 and t2.b == 0):
        return None
    lams = [F(-3, 4), F(0), F(1, 4)]
    # 3원 1차계 풀이 (Cramer, 정확)
    import fractions
    a = [[F(1), F(1), F(1)], [lams[0], lams[1], lams[2]],
         [lams[0] ** 2, lams[1] ** 2, lams[2] ** 2]]
    b = [F(16), t1.a, t2.a]
    det = (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
           - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
           + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))
    if det == 0:
        return None
    ms = []
    for col in range(3):
        aa = [[b[r] if c == col else a[r][c] for c in range(3)] for r in range(3)]
        dc = (aa[0][0] * (aa[1][1] * aa[2][2] - aa[1][2] * aa[2][1])
              - aa[0][1] * (aa[1][0] * aa[2][2] - aa[1][2] * aa[2][0])
              + aa[0][2] * (aa[1][0] * aa[2][1] - aa[1][1] * aa[2][0]))
        ms.append(dc / det)
    return ms                                   # [m(−¾), m(0), m(¼)]


def subset_support(W, gs):
    """γ-기저 256 성분 전수: tr(W γ_S†)/16 비영인 |S| 집합. (γ_S = ∏_{a∈S}γ_a, 오름차순)"""
    d = len(W)
    sizes = set()
    for r in range(9):
        for S in itertools.combinations(range(8), r):
            G = eye(d)
            for a in S:
                G = mmul(G, gs[a])
            c = tr_prod(W, dag(G))
            if c != ZERO:
                sizes.add(r)
    return sorted(sizes)


def gs_projector_checks(W, U):
    """P₀ = W(W−¼)·(4/3): P₀²=P₀·tr=1·T-불변 → unique GS 는 T-singlet."""
    n = len(W)
    P0 = smul(Cyc(F(4, 3)), mmul(W, msub(W, smul(Cyc(F(1, 4)), eye(n)))))
    return {
        "idempotent": meq(mmul(P0, P0), P0),
        "rank_1": tr(P0) == ONE,
        "T_invariant": meq(T_conj(U, P0), P0),
        "hermitian": meq(P0, dag(P0)),
    }


def main():
    quick = "--quick" in sys.argv
    out = {"_schema": "fidkowski-z8-observe/v1",
           "_note": ("Fidkowski-Kitaev ℤ→ℤ₈ 붕괴 관측 코어(0D edge 유효이론, 전 과정 ℚ(i) "
                     "정확산술): T² mod-8 시그니처·quadratic 전면 T-odd·n=4 불가 전수·"
                     "n=8 gappable 구성(unique GS·gap=¾ exact). 관측·seal 아님·"
                     "신규 module 0·root 불변. 전체 ℤ₈ 분류는 무주장.")}
    R = {}

    # γ 대수 (n=8) + T 작용
    gs8 = gammas(8)
    U8 = U_T(gs8)
    R["clifford_n8"] = check_clifford(gs8)
    R["T_fixes_all_gammas"] = all(meq(T_conj(U8, g), g) for g in gs8)

    # 1. T² mod-8 시그니처
    tsq = {}
    for n in (2, 4, 6, 8):
        gs_n = gammas(n)
        tsq[n] = T_sq_sign(U_T(gs_n))
    out["T_sq_pattern"] = {str(n): tsq[n] for n in (2, 4, 6, 8)}
    R["Tsq_bott_signature"] = (tsq[2] == -1 and tsq[4] == -1
                               and tsq[6] == 1 and tsq[8] == 1)

    # 2. 자유 장벽: 2차항 전면 T-odd
    R["all_quadratics_T_odd"] = quadratics_T_odd(gs8, U8)

    # 3. n=4 전수
    gs4 = gammas(4)
    U4 = U_T(gs4)
    n4 = n4_exhaustive(gs4, U4)
    out["n4_exhaustive"] = n4
    R["n4_protected"] = all(n4.values()) and tsq[4] == -1

    # 4. n=8 구성 W
    W, A1, A2 = build_W(gs8)
    R["su2_algebra"] = su2_check(A1) and su2_check(A2)
    R["W_hermitian"] = meq(W, dag(W))
    R["W_T_invariant"] = meq(T_conj(U8, W), W)
    R["W_annihilating_poly"] = annihilating_ok(W)
    ms = multiplicities(W)
    out["W_multiplicities"] = None if ms is None else [str(m) for m in ms]
    R["W_unique_gs_gap_3_4"] = (ms == [F(1), F(12), F(3)])
    if not quick:
        supp = subset_support(W, gs8)
        out["W_gamma_support_sizes"] = supp
        R["W_pure_quartic"] = (supp == [4])
    pj = gs_projector_checks(W, U8)
    out["gs_projector"] = pj
    R["gs_T_singlet"] = all(pj.values())

    # teeth
    q12 = smul(I, mmul(gs8[0], gs8[1]))
    R["teeth_quadratic_breaks_T"] = not meq(T_conj(U8, madd(W, q12)), madd(W, q12))
    # n=4 T-깨는 2차 → 4준위 전부 비축퇴 (projector trace 전수)
    h4 = madd(smul(I, mmul(gs4[0], gs4[1])), smul(Cyc(2), smul(I, mmul(gs4[2], gs4[3]))))
    ok4 = meq(mmul(smul(I, mmul(gs4[0], gs4[1])), smul(I, mmul(gs4[2], gs4[3]))),
              mmul(smul(I, mmul(gs4[2], gs4[3])), smul(I, mmul(gs4[0], gs4[1]))))
    nondeg = True
    for s1 in (1, -1):
        for s2 in (1, -1):
            P = smul(Cyc(F(1, 4)),
                     mmul(madd(eye(4), smul(Cyc(s1), smul(I, mmul(gs4[0], gs4[1])))),
                          madd(eye(4), smul(Cyc(s2), smul(I, mmul(gs4[2], gs4[3]))))))
            nondeg = nondeg and (tr(P) == ONE)
    R["teeth_T_breaking_gaps_n4"] = (ok4 and nondeg
                                     and not meq(T_conj(U4, h4), h4))
    # W 섭동 → 소멸다항식 위반 검출
    Wp = madd(W, smul(Cyc(F(1, 8)),
                      mmul(mmul(gs8[0], gs8[1]), mmul(gs8[2], gs8[3]))))
    R["teeth_perturbed_W_detected"] = not annihilating_ok(Wp)

    ok = bool(all(R.values()))
    out["checks"] = R
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "FIDKOWSKI-Z8-OBSERVE.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("Fidkowski-Kitaev ℤ→ℤ₈ 붕괴 관측 (상호작용 SPT 최초, 전 과정 정확산술 — seal 아님):",
              flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  ★T² 시그니처 n=2,4,6,8: {tsq[2]},{tsq[4]},{tsq[6]},{tsq[8]} (mod-8 Bott)",
              flush=True)
        print("  ★n=4: T-불변 span={1,Γ₄} 전수 → 항상 2겹(Kramers) · n=8: W=A⃗⁽¹⁾·A⃗⁽²⁾ → "
              "unique GS·gap=¾ exact(중복도 1,12,3)", flush=True)
        print("  → .pgf/proofs/FIDKOWSKI-Z8-OBSERVE.json", flush=True)
    print(f"fidkowski_z8_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
