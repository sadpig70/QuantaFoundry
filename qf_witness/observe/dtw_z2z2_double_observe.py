#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dtw_z2z2_double_observe — D^ω(ℤ₂×ℤ₂) twisted Drinfeld double: H³ 3-cocycle 축 개창
(관측, seal 아님).

TrackHE14 P3: 비자명 ω∈H³(ℤ₂×ℤ₂,U(1)) twisted quantum double 의 modular data 를 **cocycle
데이터로부터 직접 구성**(외부표 불신)해 exact ℚ(i) 대수로 검증하고, untwisted
D(ℤ₂×ℤ₂)=toric-code² 대비 ★비동형을 관측한다. H³ 비틀림이 registry 계보 최초 입력 구조.

H³(ℤ₂², U(1)) = ℤ₂³ — 대표 cocycle(±1-값, exponent GF(2)):
  ω_{(n₁,n₂,n₁₂)}(a,b,c) = (−1)^{n₁·a₁b₁c₁ + n₂·a₂b₂c₂ + n₁₂·a₁b₂c₂}
8개 클래스 전부에 대해:
  1. cocycle identity(256 quadruples) 검증 + ★비-coboundary certificate 2계층:
     (i) GF(2) 스코프: dμ=ω_exp 선형계 UNSAT + 좌영벡터 witness(y·D₂=0, y·ω=1).
     (ii) ⟨i⟩(ℤ₄-값 2-cochain) 스코프: μ=μ₀+2μ₁ 2-adic 분해로 D₂μ≡2ω (mod 4)
          가해성 판정 — 도달가능 부분공간 R=span(cols(A₂) ∪ h(ker A₂ lifts)) 소속 검사.
     (iii) ★H³ 재유도(외부표 불신): dim H³(G,𝔽₂)=4 (rank 계산) · ⟨i⟩-스코프 ±1-cocycle
          클래스 수 = 2^{dim Z³(𝔽₂)−dim R} = 8 자체 유도.
  2. twisted double 구성: β_a(h,k)=ω(a,h,k)ω(h,k,a)/ω(h,a,k) slant → ε_a: G→⟨i⟩
     자명화(브루트포스, 결정론) → 16 pointed anyon (a, χ̃=ε_a·χ_s) →
     S_{(a,χ̃),(b,ψ̃)} = (1/4)·χ̃(b)*·ψ̃(a)* (직접식) · θ_{(a,χ̃)} = χ̃(a).
  3. 공리 전량: SS†=I·S 대칭·S²=C(순열,C²=I)·Verlinde 비음정수+pointed(→융합군
     원소위수 다중집합→아벨군형)·(ST)³=λS²(λ=1: Drinfeld center c≡0 mod 8)·
     Gauss 합 Στθ=4·T unit modulus. 전부 ℚ(i) 정확산술(float 0).
  4. ★crux 대조: 비자명 7클래스 전부 untwisted 대비 T-다중집합 또는 융합군 분기 →
     twisted double 비동형 관측(⟹ ω ∉ 자명류 — 범주 불변량에 의한 무조건 certificate).
     untwisted (0,0,0)은 S==S_TC⊗S_TC exact 확인(toric-code² 정합).
  teeth 3종: (a) S 성분 섭동→공리 붕괴 (b) 가짜 비-cocycle 검출
     (c) ★양성대조: coboundary ω=dμ twist → cochain 계층 SAT 판정 + double 이
        untwisted 와 동일 T-다중집합/융합군(범주 불변성 일관성).

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  modular data 표는 봉인 아님. "비동형"은 T-다중집합/융합군 상이라는 **관측 사실**로만
  보고(범주론적 동치 분류 전체는 무주장). cochain certificate (ii)의 스코프는
  ⟨i⟩=μ₄-값 2-cochain 범위로 정직 한정(U(1) 전체 나눗셈성 정리는 인용하지 않고 무주장).
  D^ω(ℤ₃) 등 ζ₃ 필요 사례는 ℚ(i) 밖 — 미착수(범위 정직). D(D₄)/D(Q₈)
  [[dihedral_quaternion_double_observe]] 유한군 double 축 위의 twist 계층 개창.

사용: python -m qf_witness.observe.dtw_z2z2_double_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import itertools
from fractions import Fraction as F


# ════════════════════════════════════════════════════════════════════
#  ℚ(i) 정확산술 — a + b·i, i²=−1  (dihedral_quaternion_double_observe 와 동일)
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

    def div_rat(s, r):
        r = F(r); return Cyc(s.a / r, s.b / r)

    def is_real(s):
        return s.b == 0

    def is_nonneg_int(s):
        return s.b == 0 and s.a.denominator == 1 and s.a >= 0

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
IPOW = [ONE, I, Cyc(-1), Cyc(0, -1)]      # i^k, k mod 4


# ════════════════════════════════════════════════════════════════════
#  G = ℤ₂×ℤ₂ : 원소 g∈{0..3}, 비트 (g₁,g₂)=(g>>1, g&1), 곱=XOR, e=0
# ════════════════════════════════════════════════════════════════════
NG = 4


def bits(g):
    return ((g >> 1) & 1, g & 1)


def sdot(s, h):
    """GF(2) 내적 s·h = s₁h₁+s₂h₂."""
    return (((s >> 1) & (h >> 1)) ^ (s & h)) & 1


# ════════════════════════════════════════════════════════════════════
#  3-cocycle 대표: 클래스 (n₁,n₂,n₁₂) → exponent 테이블 e[a][b][c] ∈ GF(2)
# ════════════════════════════════════════════════════════════════════
def omega_exp(n1, n2, n12):
    e = [[[0] * NG for _ in range(NG)] for _ in range(NG)]
    for a in range(NG):
        a1, a2 = bits(a)
        for b in range(NG):
            b1, b2 = bits(b)
            for c in range(NG):
                c1, c2 = bits(c)
                e[a][b][c] = (n1 * (a1 & b1 & c1)
                              + n2 * (a2 & b2 & c2)
                              + n12 * (a1 & b2 & c2)) & 1
    return e


def is_cocycle(e):
    """pentagon: ω(b,c,d)ω(a,bc,d)ω(a,b,c) = ω(ab,c,d)ω(a,b,cd) — exponent 합 ≡ 0 (256 quadruples)."""
    for a, b, c, d in itertools.product(range(NG), repeat=4):
        s = (e[b][c][d] ^ e[a ^ b][c][d] ^ e[a][b ^ c][d]
             ^ e[a][b][c ^ d] ^ e[a][b][c])
        if s:
            return False
    return True


def evec_of(e):
    """exponent 테이블 → 64-bit 벡터(int), idx3(a,b,c)=16a+4b+c."""
    v = 0
    for a, b, c in itertools.product(range(NG), repeat=3):
        if e[a][b][c]:
            v |= 1 << (16 * a + 4 * b + c)
    return v


# ════════════════════════════════════════════════════════════════════
#  cochain 선형대수 — D₂: C²(16)→C³(64) 정수행렬, d₃: C³(64)→C⁴(256) GF(2)
# ════════════════════════════════════════════════════════════════════
def build_D2():
    """정수 D₂: dμ(a,b,c) = μ(b,c) − μ(ab,c) + μ(a,bc) − μ(a,b).  64행×16열 계수."""
    rows = []
    for a, b, c in itertools.product(range(NG), repeat=3):
        coeff = [0] * 16
        coeff[4 * b + c] += 1
        coeff[4 * (a ^ b) + c] -= 1
        coeff[4 * a + (b ^ c)] += 1
        coeff[4 * a + b] -= 1
        rows.append(coeff)
    return rows           # 순서 = idx3 오름차순


def d2_mod2_rows(D2):
    """A₂ = D₂ mod 2 — 각 행을 16-bit 마스크로."""
    out = []
    for coeff in D2:
        m = 0
        for j, v in enumerate(coeff):
            if v % 2:
                m |= 1 << j
        out.append(m)
    return out


def build_d3_rows():
    """GF(2) d₃ 행(256): dω(a,b,c,d)=ω(b,c,d)+ω(ab,c,d)+ω(a,bc,d)+ω(a,b,cd)+ω(a,b,c)."""
    rows = []
    for a, b, c, d in itertools.product(range(NG), repeat=4):
        m = 0
        for (x, y, z) in ((b, c, d), (a ^ b, c, d), (a, b ^ c, d),
                          (a, b, c ^ d), (a, b, c)):
            m ^= 1 << (16 * x + 4 * y + z)
        rows.append(m)
    return rows


def gf2_rank(rows):
    basis = []
    for r in rows:
        for b in basis:
            r = min(r, r ^ b)
        if r:
            basis.append(r)
            basis.sort(reverse=True)
    return len(basis)


def gf2_solve(rows, rhs_vec, ncols):
    """A x = b over GF(2). rows: int 마스크 리스트(미지수 비트), rhs_vec: 행별 0/1 (int 비트벡터).
    반환 (True, x_mask, None) 또는 (False, None, y_mask) — y: 좌영 certificate(y·A=0, y·b=1)."""
    n = len(rows)
    work = []                       # [row_mask, rhs_bit, combo_mask]
    for i, r in enumerate(rows):
        work.append([r, (rhs_vec >> i) & 1, 1 << i])
    pivots = {}                     # col -> work index
    for wi, w in enumerate(work):
        r, rb, cm = w
        while r:
            p = r.bit_length() - 1
            if p in pivots:
                pr = work[pivots[p]]
                r ^= pr[0]; rb ^= pr[1]; cm ^= pr[2]
            else:
                pivots[p] = wi
                w[0], w[1], w[2] = r, rb, cm
                break
        else:
            w[0], w[1], w[2] = 0, rb, cm
            if rb:
                return False, None, cm          # 0 = 1 모순 → certificate
    # 해 구성(자유변수 0): 행의 비-피벗 비트는 전부 자기 피벗보다 작음 → 피벗 오름차순
    x = 0
    for p in sorted(pivots):
        w = work[pivots[p]]
        r, rb = w[0], w[1]
        acc = rb
        rr = r & ~(1 << p)
        while rr:
            q = rr.bit_length() - 1
            acc ^= (x >> q) & 1
            rr &= ~(1 << q)
        if acc:
            x |= 1 << p
    return True, x, None


def gf2_kernel_basis(rows, ncols):
    """ker(A) 기저(ncols-bit 마스크): 자유변수당 하나. 결정론."""
    # 전방 소거로 피벗열 파악
    mat = list(rows)
    basis_rows = []
    pivcols = []
    for r in mat:
        for br, pc in zip(basis_rows, pivcols):
            if (r >> pc) & 1:
                r ^= br
        if r:
            pc = r.bit_length() - 1
            basis_rows.append(r); pivcols.append(pc)
    free = [c for c in range(ncols) if c not in pivcols]
    kers = []
    for fc in free:
        x = 1 << fc
        # 후진 대입: 행의 비-피벗 비트 < 자기 피벗 → 피벗 오름차순으로 전부 해소
        order = sorted(range(len(pivcols)), key=lambda i: pivcols[i])
        for i in order:
            br, pc = basis_rows[i], pivcols[i]
            acc = 0
            rr = br & ~(1 << pc)
            while rr:
                q = rr.bit_length() - 1
                acc ^= (x >> q) & 1
                rr &= ~(1 << q)
            if acc:
                x |= 1 << pc
        kers.append(x)
    return kers


class Span:
    """F₂^64 부분공간 — 소속검사/차원."""

    def __init__(self):
        self.basis = []

    def reduce(self, v):
        for b in self.basis:
            v = min(v, v ^ b)
        return v

    def add(self, v):
        v = self.reduce(v)
        if v:
            self.basis.append(v)
            self.basis.sort(reverse=True)

    def contains(self, v):
        return self.reduce(v) == 0

    @property
    def dim(self):
        return len(self.basis)


def cochain_layer():
    """cochain 계층 전체: (A₂행, R-span(⟨i⟩ 도달공간), dim Z³, dim B³_F2, dim H³_F2, i-scope 클래스수)."""
    D2 = build_D2()
    A2 = d2_mod2_rows(D2)
    # GF(2) 이미지 공간 B³_F2 = span{A₂ 열벡터를 방정식축으로 본 이미지} = {A₂·μ : μ}
    imgF2 = Span()
    for j in range(16):
        v = 0
        for i, row in enumerate(A2):
            if (row >> j) & 1:
                v |= 1 << i
        imgF2.add(v)
    # ⟨i⟩ 도달공간 R = span( B³_F2 ∪ h(ker A₂ lifts) ), h(k) = (D₂k)/2 mod 2
    R = Span()
    for b in imgF2.basis:
        R.add(b)
    kers = gf2_kernel_basis(A2, 16)
    for k in kers:
        kvec = [(k >> j) & 1 for j in range(16)]
        v = 0
        for i, coeff in enumerate(D2):
            w = sum(cf * kv for cf, kv in zip(coeff, kvec))
            assert w % 2 == 0, "kernel lift 짝수성 위반"
            if (w // 2) % 2:
                v |= 1 << i
        R.add(v)
    d3rows = build_d3_rows()
    dimZ3 = 64 - gf2_rank(d3rows)
    # sanity: R ⊆ Z³ (coboundary 는 cocycle)
    for v in R.basis:
        for i, m in enumerate(d3rows):
            acc = 0
            mm = m
            while mm:
                q = mm.bit_length() - 1
                acc ^= (v >> q) & 1
                mm &= ~(1 << q)
            assert acc == 0, "R ⊄ Z³"
    return {
        "A2": A2, "R": R, "imgF2": imgF2, "d3rows": d3rows,
        "dim_Z3_F2": dimZ3,
        "dim_B3_F2": imgF2.dim,
        "dim_H3_F2": dimZ3 - imgF2.dim,               # 기대 4 (𝔽₂ 계수)
        "iscope_classes": 2 ** (dimZ3 - R.dim),        # 기대 8 = |H³(G,U(1))| (⟨i⟩ 스코프)
    }


# ════════════════════════════════════════════════════════════════════
#  twisted double 구성 (일반 ω exponent 테이블 입력)
# ════════════════════════════════════════════════════════════════════
def slant_beta(e):
    """β_a(h,k) exponent = e(a,h,k)+e(h,k,a)+e(h,a,k) mod 2 (아벨 G)."""
    beta = []
    for a in range(NG):
        t = [[(e[a][h][k] ^ e[h][k][a] ^ e[h][a][k]) for k in range(NG)]
             for h in range(NG)]
        # 2-cocycle 확인: t(k,l)+t(hk,l)+t(h,kl)+t(h,k) ≡ 0
        for h, k, l in itertools.product(range(NG), repeat=3):
            assert (t[k][l] ^ t[h ^ k][l] ^ t[h][k ^ l] ^ t[h][k]) == 0, "β_a not 2-cocycle"
        beta.append(t)
    return beta


def trivialize(beta_a):
    """ε: G→⟨i⟩, ε(e)=1, dε=β_a — exponent E:G→ℤ₄ 브루트포스(결정론 사전순 첫 해).
    E(h)+E(k)−E(h⊕k) ≡ 2·β_a(h,k) (mod 4). 없으면 None (honest abort 용)."""
    for E1 in range(4):
        for E2 in range(4):
            for E3 in range(4):
                E = [0, E1, E2, E3]
                if all((E[h] + E[k] - E[h ^ k]) % 4 == (2 * beta_a[h][k]) % 4
                       for h in range(NG) for k in range(NG)):
                    return E
    return None


class TwistedDouble:
    """D^ω(ℤ₂²): 16 pointed anyon (a,s) — χ̃_{a,s}(h)=i^{E_a(h)}·(−1)^{s·h}."""

    def __init__(self, e):
        self.beta = slant_beta(e)
        self.E = []
        for a in range(NG):
            Ea = trivialize(self.beta[a])
            assert Ea is not None, "β_a not ⟨i⟩-trivializable (honest abort — ℚ(i) 밖)"
            self.E.append(Ea)
        self.anyons = [(a, s) for a in range(NG) for s in range(NG)]  # idx=4a+s
        self.N = 16

    def chi(self, x, h):
        a, s = self.anyons[x]
        v = IPOW[self.E[a][h] % 4]
        return v * Cyc(-1) if sdot(s, h) else v

    def build_S_T(self):
        S = [[ZERO] * self.N for _ in range(self.N)]
        for x in range(self.N):
            ax, _ = self.anyons[x]
            for y in range(self.N):
                ay, _ = self.anyons[y]
                S[x][y] = (self.chi(x, ay).conj() * self.chi(y, ax).conj()).div_rat(NG)
        T = [self.chi(x, self.anyons[x][0]) for x in range(self.N)]
        return S, T


# ── Cyc 행렬 유틸 (P1 과 동일) ───────────────────────────────────────
def matmul(A, B):
    n = len(A); C = [[ZERO] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            aik = A[i][k]
            if aik == ZERO:
                continue
            for j in range(n):
                C[i][j] = C[i][j] + aik * B[k][j]
    return C


def dagger(A):
    n = len(A); return [[A[j][i].conj() for j in range(n)] for i in range(n)]


def is_identity(A):
    n = len(A)
    return all(A[i][j] == (ONE if i == j else ZERO) for i in range(n) for j in range(n))


def perm_of(A):
    n = len(A); perm = [-1] * n
    for i in range(n):
        ones = [j for j in range(n) if A[i][j] == ONE]
        if len(ones) != 1 or any(A[i][j] not in (ZERO, ONE) for j in range(n)):
            return None
        perm[i] = ones[0]
    return perm if sorted(perm) == list(range(n)) else None


def _cdiv(x, y):
    denom = y.a * y.a + y.b * y.b
    if denom == 0:
        return None
    num = x * y.conj()
    return Cyc(num.a / denom, num.b / denom)


def st_cubed_lambda(S, T):
    n = len(S)
    Tm = [[T[i] if i == j else ZERO for j in range(n)] for i in range(n)]
    ST = matmul(S, Tm)
    ST3 = matmul(matmul(ST, ST), ST)
    S2 = matmul(S, S)
    lam = None
    for i in range(n):
        for j in range(n):
            if S2[i][j] != ZERO:
                if ST3[i][j] == ZERO:
                    return None
                cand = _cdiv(ST3[i][j], S2[i][j])
                if cand is None:
                    return None
                if lam is None:
                    lam = cand
                elif not (lam == cand):
                    return None
            elif ST3[i][j] != ZERO:
                return None
    return lam


def t_multiset(T):
    return sorted((str(t.a), str(t.b)) for t in T)


def verlinde_pointed(S):
    """N_{ab}^c 전부 비음정수 + pointed(행마다 정확히 c 하나 N=1) → 융합표 반환."""
    n = len(S)
    fus = [[None] * n for _ in range(n)]
    for a in range(n):
        for b in range(n):
            hits = []
            for c in range(n):
                acc = ZERO
                for x in range(n):
                    s0 = S[0][x]
                    if not (s0.is_real() and s0.a != 0):
                        return False, None
                    acc = acc + (S[a][x] * S[b][x] * S[c][x].conj()).div_rat(s0.a)
                if not acc.is_nonneg_int():
                    return False, None
                if acc == ONE:
                    hits.append(c)
                elif not (acc == ZERO):
                    return False, None
            if len(hits) != 1:
                return False, None
            fus[a][b] = hits[0]
    return True, fus


def fusion_group_type(fus):
    """융합군(pointed, 단위원=0) 원소위수 다중집합 → 아벨군형 이름."""
    n = len(fus)
    orders = []
    for x in range(n):
        k, acc = 1, x
        while acc != 0:
            acc = fus[acc][x]; k += 1
        orders.append(k)
    key = tuple(sorted(orders))
    names = {
        tuple([1] + [2] * 15): "Z2^4",
        tuple([1] + [2] * 7 + [4] * 8): "Z4xZ2^2",
        tuple([1] + [2] * 3 + [4] * 12): "Z4xZ4",
        tuple([1] + [2] * 3 + [4] * 4 + [8] * 8): "Z8xZ2",
        tuple([1, 2] + [4] * 2 + [8] * 4 + [16] * 8): "Z16",
    }
    return names.get(key, f"order_multiset={key}"), sorted(orders)


# ════════════════════════════════════════════════════════════════════
#  클래스 검증 하네스
# ════════════════════════════════════════════════════════════════════
def verify_class(e, label):
    D = TwistedDouble(e)
    S, T = D.build_S_T()
    n = D.N
    res = {"class": label, "n_anyon": n}
    checks = {}
    checks["S_unitary"] = is_identity(matmul(S, dagger(S)))
    checks["S_symmetric"] = all(S[i][j] == S[j][i] for i in range(n) for j in range(n))
    S2 = matmul(S, S)
    perm = perm_of(S2)
    checks["S2_is_perm"] = perm is not None
    if perm is not None:
        checks["C_squared_I"] = all(perm[perm[i]] == i for i in range(n))
        res["self_dual"] = (perm == list(range(n)))
    checks["first_row_quarter"] = all(S[0][x] == Cyc(F(1, 4)) for x in range(n))
    vok, fus = verlinde_pointed(S)
    checks["verlinde_pointed"] = vok
    if vok:
        gname, orders = fusion_group_type(fus)
        res["fusion_group"] = gname
        res["fusion_order_multiset"] = orders
    lam = st_cubed_lambda(S, T)
    checks["stcubed_lambda1"] = (lam is not None and lam == ONE)
    res["lambda"] = None if lam is None else str(lam)
    gauss = ZERO
    for t in T:
        gauss = gauss + t
    checks["gauss_sum_4_c0mod8"] = (gauss == Cyc(4))
    res["gauss_sum"] = str(gauss)
    checks["T_unit_modulus"] = all((t.a * t.a + t.b * t.b) == 1 for t in T)
    res["T_multiset"] = t_multiset(T)
    res["checks"] = checks
    res["all_pass"] = all(checks.values())
    return S, T, res


def untwisted_is_tc_squared(S):
    """untwisted S == ¼(−1)^{s·b+t·a} (toric-code S ⊗ toric-code S) exact."""
    for x in range(16):
        a, s = divmod(x, 4)
        for y in range(16):
            b, t = divmod(y, 4)
            exp = sdot(s, b) ^ sdot(t, a)
            want = Cyc(F(-1 if exp else 1, 4))
            if not (S[x][y] == want):
                return False
    return True


def teeth_S_perturb(e):
    """S 한 성분 섭동 → unitary 또는 Verlinde 붕괴."""
    D = TwistedDouble(e)
    S, _ = D.build_S_T()
    S = [row[:] for row in S]
    S[0][1] = S[0][1] + ONE
    if not is_identity(matmul(S, dagger(S))):
        return True
    vok, _ = verlinde_pointed(S)
    return not vok


def teeth_fake_cocycle():
    """단일 지점 exponent → pentagon 위반 검출."""
    e = [[[0] * NG for _ in range(NG)] for _ in range(NG)]
    e[1][1][1] = 1
    return not is_cocycle(e)


def coboundary_exp():
    """μ(a,b)=a₁b₁b₂ 의 dμ — 비영 GF(2) coboundary (양성대조용)."""
    mu = [[bits(a)[0] & bits(b)[0] & bits(b)[1] for b in range(NG)] for a in range(NG)]
    e = [[[0] * NG for _ in range(NG)] for _ in range(NG)]
    for a, b, c in itertools.product(range(NG), repeat=3):
        e[a][b][c] = (mu[b][c] ^ mu[a ^ b][c] ^ mu[a][b ^ c] ^ mu[a][b]) & 1
    assert any(e[a][b][c] for a, b, c in itertools.product(range(NG), repeat=3)), "dμ=0 (테스트 무의미)"
    return e


def main():
    quick = "--quick" in sys.argv
    out = {"_schema": "dtw-z2z2-double/v1",
           "_note": ("D^ω(ℤ₂×ℤ₂) twisted double — H³ 8클래스 전수 modular data 자체구성 "
                     "+ cocycle 2계층 certificate + untwisted(toric²) 대비 비동형 관측"
                     "(관측·seal 아님·root 불변 sidecar·신규 module 0). "
                     "⟨i⟩-스코프 정직 한정·ζ₃ 필요 사례(D^ω(ℤ₃)) 미착수.")}

    # ── cochain 계층 (자체 유도: H³ 차원 외부표 불신) ──
    lay = cochain_layer()
    out["cohomology"] = {
        "dim_Z3_F2": lay["dim_Z3_F2"], "dim_B3_F2": lay["dim_B3_F2"],
        "dim_H3_F2": lay["dim_H3_F2"],
        "iscope_pm1_cocycle_classes": lay["iscope_classes"],
        "note": "H³(G,𝔽₂)=𝔽₂⁴(다항환 3차) vs ⟨i⟩-스코프 ±1-cocycle 클래스 8=|H³(G,U(1))|(=ℤ₂³) 자체 유도",
    }
    checks_global = {
        "H3_F2_dim_4": lay["dim_H3_F2"] == 4,
        "iscope_classes_8": lay["iscope_classes"] == 8,
    }

    # ── 8 클래스 전수 ──
    classes = {}
    tms = {}
    fgs = {}
    for n1, n2, n12 in itertools.product((0, 1), repeat=3):
        label = f"{n1}{n2}{n12}"
        e = omega_exp(n1, n2, n12)
        cls = {"cocycle_identity": is_cocycle(e)}
        ev = evec_of(e)
        nontrivial = (n1, n2, n12) != (0, 0, 0)
        # GF(2) coboundary 판정 + certificate
        rhs = ev
        sat, x, ycert = gf2_solve(lay["A2"], rhs, 16)
        cls["gf2_coboundary"] = bool(sat)
        if not sat:
            cls["gf2_uncobound_certificate_y"] = f"{ycert:016x}"  # y·D₂=0, y·ω=1 (64-bit 행조합)
        # ⟨i⟩ 스코프
        cls["iscope_coboundary"] = lay["R"].contains(ev)
        # twisted double
        _, _, res = verify_class(e, label)
        cls.update(res)
        cls["expected_certs"] = (cls["cocycle_identity"]
                                 and (cls["gf2_coboundary"] == (not nontrivial))
                                 and (cls["iscope_coboundary"] == (not nontrivial)))
        classes[label] = cls
        tms[label] = tuple(map(tuple, res["T_multiset"]))
        fgs[label] = res.get("fusion_group")
    out["classes"] = classes

    # untwisted 정합: S == TC⊗TC
    e0 = omega_exp(0, 0, 0)
    S0, _, _ = verify_class(e0, "000")
    checks_global["untwisted_eq_toric_squared"] = untwisted_is_tc_squared(S0)

    # ── ★crux 대조: 비자명 7클래스 전부 untwisted 와 분기 ──
    t0, f0 = tms["000"], fgs["000"]
    crux = {}
    for label in classes:
        if label == "000":
            continue
        crux[label] = {
            "T_multiset_differs": tms[label] != t0,
            "fusion_group_differs": fgs[label] != f0,
            "nonequiv_witnessed": (tms[label] != t0) or (fgs[label] != f0),
        }
    out["crux_contrast"] = crux
    out["distinct_T_multisets"] = len(set(tms.values()))
    out["fusion_groups"] = fgs
    checks_global["crux_all7_nonequiv"] = all(c["nonequiv_witnessed"] for c in crux.values())
    checks_global["untwisted_fusion_Z2_4"] = (f0 == "Z2^4")

    # ── teeth ──
    e_tw = omega_exp(0, 0, 1)
    teeth = {
        "S_perturbation_breaks": teeth_S_perturb(e_tw),
        "fake_cocycle_detected": teeth_fake_cocycle(),
    }
    # ★양성대조: coboundary twist → SAT + untwisted 동일 데이터
    e_cb = coboundary_exp()
    cb = {"cocycle_identity": is_cocycle(e_cb)}
    ev = evec_of(e_cb)
    sat, _, _ = gf2_solve(lay["A2"], ev, 16)
    cb["gf2_coboundary"] = bool(sat)
    cb["iscope_coboundary"] = lay["R"].contains(ev)
    _, _, res_cb = verify_class(e_cb, "coboundary_dmu")
    cb["all_pass"] = res_cb["all_pass"]
    cb["T_multiset_eq_untwisted"] = tuple(map(tuple, res_cb["T_multiset"])) == t0
    cb["fusion_eq_untwisted"] = res_cb.get("fusion_group") == f0
    teeth["coboundary_positive_control"] = cb
    out["teeth"] = teeth
    out["checks_global"] = checks_global

    all_ok = (all(c["all_pass"] and c["expected_certs"] and c["cocycle_identity"]
                  for c in classes.values())
              and all(checks_global.values())
              and teeth["S_perturbation_breaks"] and teeth["fake_cocycle_detected"]
              and cb["cocycle_identity"] and cb["gf2_coboundary"] and cb["iscope_coboundary"]
              and cb["all_pass"] and cb["T_multiset_eq_untwisted"] and cb["fusion_eq_untwisted"])
    out["all_ok"] = bool(all_ok)

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "DTW-Z2Z2-DOUBLE.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print(f"H³ 자체유도: dim H³(𝔽₂)={lay['dim_H3_F2']} · ⟨i⟩-스코프 클래스={lay['iscope_classes']}", flush=True)
        for label, cls in classes.items():
            print(f"D^ω[{label}]: fusion={cls.get('fusion_group')} · λ={cls['lambda']} · "
                  f"all_pass={cls['all_pass']}", flush=True)
        print(f"★crux: 비자명 7/7 untwisted 비동형 관측={checks_global['crux_all7_nonequiv']} · "
              f"distinct T-multiset={out['distinct_T_multisets']}", flush=True)
        print("  → .pgf/proofs/DTW-Z2Z2-DOUBLE.json", flush=True)
    print(f"dtw_z2z2_double: all_ok={out['all_ok']}", flush=True)
    return 0 if out["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
