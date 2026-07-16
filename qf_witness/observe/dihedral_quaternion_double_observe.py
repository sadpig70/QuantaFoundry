#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dihedral_quaternion_double_observe — D(D₄) · D(Q₈) 완전 Drinfeld double modular data
자체검증 witness + 쌍 대조 (관측, seal 아님).

TrackHE14 P1: 위수 8 두 비아벨군 D₄(이면체)·Q₈(쿼터니언)의 quantum double modular data를
**군 데이터로부터 직접 구성**(외부표 불신)해 exact ℚ(i) 대수로 검증하고, ★두 double을
**쌍으로 대조**한다. 핵심 통찰(report14 8/8 수렴):

  D₄ 와 Q₈ 는 **동일한 문자표**(character table)를 가진다(고전적 사실). 그럼에도 그 Drinfeld
  double 은 **동형이 아니다** — 22 anyon·D²=64·c≡0(mod 8)·ℚ(i) 는 공유하나 **topological spin
  T 의 다중집합(±i 개수)이 갈라진다**. ⟹ "군 문자표 동치 ≠ double MTC 동치" 를 실증.
  단일 double 관측이 아니라 **쌍 대조(T-스펙트럼 분기)** 가 검증 객체다.

각 군 G(|G|=8, 5 켤레류, irreps dim=(1,1,1,1,2)):
  anyon = (켤레류 C, 대표원 centralizer Z(g_C)의 기약표현 ρ).
    class e   (Z=G,   5 irreps): d=|C|·dimρ=(1,1,1,1,2)          → 5 anyon
    class z   (Z=G,   5 irreps): z=중심원 r²/(−1), 동일             → 5 anyon
    나머지 3 켤레류 (|C|=2, Z=order4 아벨, 4 irreps): d=2·1=2      → 4·3=12 anyon
  총 5+5+12 = 22 anyon. Σd² = (1+1+1+1+4)·2 + 4·(2²)·3 = 16 + 48 = 64 = |G|².

관측(exact modular data·공리, 전부 ℚ(i) 정확산술 — √ 무관, 정수/유리 cyclotomic):
  1. S_{(A,ρ),(B,σ)}=(1/|G|)Σ_{g∈A,h∈B,gh=hg} χ_ρ(x⁻¹hx)* χ_σ(y⁻¹gy)*  (x:g_A→g, y:g_B→h).
     실대칭·unitary(SS†=I).
  2. S²=C (charge conjugation 순열, C²=I).
  3. Verlinde N_{ab}^c=Σ_x S_ax S_bx S*_cx/S_0x: 전부 비음정수.
  4. T_{(A,ρ)}=χ_ρ(g_A)/dimρ (topological spin θ). (ST)³=λS² (유한군 double c≡0 mod 8→λ=1)·T 유한위수.
  5. S_{0a}=d_a/8 정확 · Σd²=64.
  6. ★쌍 대조: D(D₄) vs D(Q₈) — S 스펙트럼/융합/T-다중집합 대조. T 다중집합 상이 = double 비동형 관측.
  teeth: S 한 성분 섭동 → 최소 하나의 공리 붕괴.

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  modular data 표(조합적 exact)는 봉인 아님·anyon braid 게이트는 유니터리 module 아님(§2 Fourier
  실봉인 경계 무관·우회). D(S₃)[[dsr3_double_observe]] 유한군 MTC 축의 심화 — ambivalent S₃(C=I)
  대비 비-ambivalent 여부·비아벨 2-group double. "double 비동형"은 T-다중집합 상이라는 **관측 사실**로만
  보고(braided equivalence 부재의 범주론 증명은 무주장, Mignard-Schauenburg 류 의식).

사용: python -m qf_witness.observe.dihedral_quaternion_double_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import itertools
from fractions import Fraction as F


# ════════════════════════════════════════════════════════════════════
#  ℚ(i) 정확산술 — a + b·i,  i²=−1
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


# ════════════════════════════════════════════════════════════════════
#  군 실현: faithful 2-dim ℚ(i) 행렬 표현.
#    2-dim irrep character = trace(자동). 1-dim irreps = abelianization 부호.
#  D₄: r=rot(π/2), s=refl.   Q₈: i,j,k (Pauli-류).
# ════════════════════════════════════════════════════════════════════
def m_mul(A, B):
    """4-flat 2×2 (a,b,c,d)=[[a,b],[c,d]] 행렬곱 → 4-flat."""
    return (A[0] * B[0] + A[1] * B[2], A[0] * B[1] + A[1] * B[3],
            A[2] * B[0] + A[3] * B[2], A[2] * B[1] + A[3] * B[3])


# D₄ 생성원 (2×2 실행렬, ℚ(i)에 담음): r=[[0,-1],[1,0]], s=[[1,0],[0,-1]]
D4_R = (ZERO, Cyc(-1), ONE, ZERO)
D4_S = (ONE, ZERO, ZERO, Cyc(-1))
# Q₈ 생성원 (SU(2), ℚ(i)): i=[[i,0],[0,-i]], j=[[0,1],[-1,0]]
Q8_I = (I, ZERO, ZERO, Cyc(0, -1))
Q8_J = (ZERO, ONE, Cyc(-1), ZERO)
IDENT = (ONE, ZERO, ZERO, ONE)


def gen_group(gens):
    """생성원 닫힘 → 원소 리스트(2×2 튜플). 결정론(BFS by insertion order)."""
    elems = [IDENT]
    seen = {IDENT}
    i = 0
    while i < len(elems):
        g = elems[i]; i += 1
        for x in gens:
            h = m_mul(g, x)
            if h not in seen:
                seen.add(h); elems.append(h)
    return elems


def build_group(name):
    if name == "D4":
        elems = gen_group([D4_R, D4_S])
    elif name == "Q8":
        elems = gen_group([Q8_I, Q8_J])
    else:
        raise ValueError(name)
    assert len(elems) == 8, f"{name}: |G|={len(elems)}≠8"
    return elems


# ════════════════════════════════════════════════════════════════════
#  군 구조: 곱·역·켤레류·centralizer (원소=2×2 튜플, 인덱스로 취급)
# ════════════════════════════════════════════════════════════════════
class Group:
    def __init__(self, name):
        self.name = name
        self.E = build_group(name)
        self.n = len(self.E)
        self.idx = {g: i for i, g in enumerate(self.E)}
        self.mul = [[self.idx[m_mul(self.E[a], self.E[b])] for b in range(self.n)]
                    for a in range(self.n)]
        self.inv = [next(b for b in range(self.n) if self.mul[a][b] == 0)
                    for a in range(self.n)]
        self.classes = self._conj_classes()
        # 켤레류 대표원(가장 작은 인덱스)·원소집합·centralizer
        self.reps = [c[0] for c in self.classes]

    def _conj_classes(self):
        seen = set(); out = []
        for g in range(self.n):
            if g in seen:
                continue
            cl = sorted({self.mul[self.mul[x][g]][self.inv[x]] for x in range(self.n)})
            out.append(cl); seen.update(cl)
        return out  # 결정론: 최소원소 등장 순

    def centralizer(self, g):
        return [x for x in range(self.n) if self.mul[x][g] == self.mul[g][x]]

    def conj_witness(self, rep):
        """대표원 rep → 켤레류 각 g 로 옮기는 x (x·rep·x⁻¹ = g) 하나."""
        d = {}
        for x in range(self.n):
            g = self.mul[self.mul[x][rep]][self.inv[x]]
            d.setdefault(g, x)
        return d


# ════════════════════════════════════════════════════════════════════
#  기약표현 지표: order≤8 군의 irrep character 를 orthogonality 로 자체계산.
#    1-dim: G/[G,G] 의 지표(= abelianization). 2-dim(존재 시): 나머지(Σdim²=|G|).
#  centralizer 는 G(order8) 또는 order4 아벨 → 아벨은 전부 1-dim.
# ════════════════════════════════════════════════════════════════════
def _subgroup(G, elems):
    """G 의 부분집합 elems(인덱스)를 자기 군으로: (원소리스트, mul, inv, classes)."""
    S = sorted(elems)
    pos = {g: i for i, g in enumerate(S)}
    n = len(S)
    mul = [[pos[G.mul[S[a]][S[b]]] for b in range(n)] for a in range(n)]
    inv = [next(b for b in range(n) if mul[a][b] == 0) for a in range(n)]
    # 켤레류
    seen = set(); classes = []
    for g in range(n):
        if g in seen:
            continue
        cl = sorted({mul[mul[x][g]][inv[x]] for x in range(n)})
        classes.append(cl); seen.update(cl)
    return S, mul, inv, classes


def _commutator_subgroup(n, mul, inv):
    gens = set()
    for a in range(n):
        for b in range(n):
            # aba⁻¹b⁻¹
            gens.add(mul[mul[mul[a][b]][inv[a]]][inv[b]])
    # 닫힘
    sub = {0} | gens
    changed = True
    while changed:
        changed = False
        for x in list(sub):
            for y in list(sub):
                p = mul[x][y]
                if p not in sub:
                    sub.add(p); changed = True
    return sub


def irrep_characters(G, sub_elems):
    """부분군(centralizer) 의 기약표현 지표 테이블.
    반환: list of dict{ global_elem_index -> Cyc } (각 irrep), 원소 인덱스는 G 전역.
    order≤8 · 아벨 또는 D₄/Q₈ 한정 — 1-dim 은 abelianization, 2-dim 은 faithful trace."""
    S, mul, inv, classes = _subgroup(G, sub_elems)
    n = len(S)
    comm = _commutator_subgroup(n, mul, inv)
    # abelianization A = sub/comm, 위수 = n/|comm|
    # 각 코셋 대표 → 1-dim 지표(A 의 pontryagin dual)
    # A 는 아벨 (order n/|comm|). 원소를 코셋으로 그룹핑.
    coset_of = {}
    reps = []
    for g in range(n):
        cg = frozenset(mul[g][c] for c in comm)
        if cg not in coset_of:
            coset_of[cg] = len(reps); reps.append(g)
        # map g→coset id
    gid = {g: coset_of[frozenset(mul[g][c] for c in comm)] for g in range(n)}
    m = len(reps)  # |A|
    # A 의 곱 구조
    Amul = [[gid[mul[reps[a]][reps[b]]] for b in range(m)] for a in range(m)]
    # A 의 순환분해로 1-dim 지표 생성 (A 아벨, order m∈{1,2,4,8})
    chars_A = _abelian_duals(m, Amul)
    onedim = []
    for ch in chars_A:
        onedim.append({G_elem: ch[gid[s_local]]
                       for s_local, G_elem in enumerate(S)})
    n_one = len(onedim)               # = m
    irreps = list(onedim)
    # 2-dim irrep 존재? Σdim² = n → 남은 = n - n_one·1
    remaining = n - n_one
    if remaining == 0:
        return irreps                 # 아벨: 전부 1-dim
    # remaining = 4 → 한 개의 2-dim irrep (D₄/Q₈). faithful 2×2 표현의 trace.
    assert remaining == 4, f"unexpected remaining {remaining} for |H|={n}"
    two = {}
    for s_local, G_elem in enumerate(S):
        M = G.E[G_elem]               # faithful 2-dim rep (군 실현 그대로)
        two[G_elem] = M[0] + M[3]     # trace
    irreps.append(two)
    return irreps


def _abelian_duals(m, Amul):
    """아벨군 A(위수 m, 곱표 Amul, 0=단위원)의 모든 1-dim 지표(값=Cyc).
    각 원소 위수로부터 root-of-unity — order|4 만 등장(ℚ(i) 폐포)."""
    if m == 1:
        return [{0: ONE}]
    # A 의 원소 위수
    order = []
    for g in range(m):
        k = 1; x = g
        while x != 0:
            x = Amul[x][g]; k += 1
        order.append(k)
    # 순환군 곱: A ≅ Z_{d1}×...  — 여기선 m∈{2,4}, 구조 단순.
    # 모든 준동형 A→ℂ* 를 생성: 각 생성원에 root-of-unity 할당.
    # m=2: Z₂ → {±1}, 2 duals. m=4: Z₄ 또는 Z₂².
    # 일반 처리: A 의 생성원 집합 찾고 각 생성원 위수의 root 조합.
    gens, structure = _abelian_gens(m, Amul, order)
    # structure = [d1,d2,...], gens 대응. root 후보 = ζ_{di}^{0..di-1}
    roots = [[_root_of_unity(d, k) for k in range(d)] for d in structure]
    duals = []
    for combo in itertools.product(*[range(d) for d in structure]):
        ch = {}
        for g in range(m):
            exps = _express(g, gens, structure, Amul)
            val = ONE
            for gi, e in enumerate(exps):
                val = val * _powcyc(roots[gi][combo[gi] % structure[gi]], e)
            ch[g] = val
        duals.append(ch)
    assert len(duals) == m
    return duals


def _root_of_unity(d, k):
    """ζ_d^k, d|4 (d∈{1,2,4}) → ℚ(i)."""
    table = {1: [ONE], 2: [ONE, Cyc(-1)], 4: [ONE, I, Cyc(-1), Cyc(0, -1)]}
    return table[d][k % d]


def _powcyc(z, e):
    r = ONE
    for _ in range(e):
        r = r * z
    return r


def _abelian_gens(m, Amul, order):
    """아벨군 A 의 독립 생성원과 구조 [d1,...] (m∈{1,2,4}). 결정론."""
    if m == 2:
        g = next(x for x in range(m) if order[x] == 2)
        return [g], [2]
    # m == 4: Z₄ (원소 위수 4 존재) 또는 Z₂² (전부 위수≤2)
    if any(o == 4 for o in order):
        g = next(x for x in range(m) if order[x] == 4)
        return [g], [4]
    # Z₂²: 두 독립 위수-2 원소
    g1 = next(x for x in range(1, m) if order[x] == 2)
    g2 = next(x for x in range(1, m) if order[x] == 2 and x != g1 and x != _mul_pow(g1, g1, Amul))
    return [g1, g2], [2, 2]


def _mul_pow(a, b, Amul):
    return Amul[a][b]


def _express(g, gens, structure, Amul):
    """g 를 생성원 거듭제곱 조합으로: exps[i] s.t. Π gens[i]^exps[i] = g. brute(m≤4)."""
    ranges = [range(d) for d in structure]
    for combo in itertools.product(*ranges):
        acc = 0  # 단위원
        for gi, e in enumerate(combo):
            x = 0
            for _ in range(e):
                x = Amul[x][gens[gi]]
            acc = Amul[acc][x]
        if acc == g:
            return list(combo)
    raise ValueError(f"cannot express {g}")


# ════════════════════════════════════════════════════════════════════
#  Drinfeld double modular data (군 G)
# ════════════════════════════════════════════════════════════════════
class Double:
    def __init__(self, name):
        self.G = Group(name)
        self.name = name
        self._build_anyons()
        self.S = self._build_S()
        self.T = self._build_T()

    def _build_anyons(self):
        G = self.G
        self.anyons = []          # (class_idx, irrep_idx)
        self.dim = []             # 양자차원 = |C|·dimρ
        self.chi = []             # dict elem->Cyc (centralizer irrep, 전역 인덱스)
        self.class_of = []
        self.rep_of = []
        for ci, cl in enumerate(G.classes):
            rep = G.reps[ci]
            Z = G.centralizer(rep)
            irreps = irrep_characters(G, Z)
            csize = len(cl)
            for ri, ch in enumerate(irreps):
                dimrho = ch[0].a                # dimρ = χ(identity)
                assert dimrho.denominator == 1, f"non-integer dimρ {dimrho}"
                dimrho = int(dimrho)
                self.anyons.append((ci, ri))
                self.dim.append(csize * dimrho)
                self.chi.append(ch)
                self.class_of.append(ci)
                self.rep_of.append(rep)
        self.N = len(self.anyons)

    def _chi_at(self, a, elem):
        """anyon a 의 centralizer 지표를 원소 elem(전역 인덱스)에서. elem∈Z(rep) 보장."""
        return self.chi[a][elem]

    def _build_S(self):
        G = self.G
        N = self.N
        wit = [G.conj_witness(G.reps[ci]) for ci in range(len(G.classes))]
        S = [[ZERO] * N for _ in range(N)]
        for a in range(N):
            ca = self.class_of[a]
            for b in range(N):
                cb = self.class_of[b]
                tot = ZERO
                for g in G.classes[ca]:
                    xg = wit[ca][g]; xgi = G.inv[xg]
                    for h in G.classes[cb]:
                        if G.mul[g][h] != G.mul[h][g]:
                            continue
                        yh = wit[cb][h]; yhi = G.inv[yh]
                        ea = G.mul[G.mul[xgi][h]][xg]   # x⁻¹ h x ∈ Z(g_A)
                        eb = G.mul[G.mul[yhi][g]][yh]   # y⁻¹ g y ∈ Z(g_B)
                        S[a][b] = S[a][b] + self._chi_at(a, ea).conj() * self._chi_at(b, eb).conj()
                        tot = tot + ONE
                S[a][b] = S[a][b].div_rat(G.n)
        return S

    def _build_T(self):
        T = []
        for a in range(self.N):
            rep = self.rep_of[a]
            num = self._chi_at(a, rep)
            den = self.dim[a] // len(self.G.classes[self.class_of[a]])  # dimρ
            T.append(num.div_rat(den))
        return T


# ── Cyc 행렬 유틸 ────────────────────────────────────────────────────
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


def verlinde_ok(S):
    n = len(S)
    for a in range(n):
        for b in range(n):
            for c in range(n):
                acc = ZERO
                for x in range(n):
                    s0 = S[0][x]
                    if not (s0.is_real() and s0.a != 0):
                        return False, (a, b, c, x)
                    acc = acc + (S[a][x] * S[b][x] * S[c][x].conj()).div_rat(s0.a)
                if not acc.is_nonneg_int():
                    return False, (a, b, c)
    return True, None


def st_cubed_lambda(S, T):
    """(ST)³ = λ S². λ 반환(Cyc) 또는 None(형태 불일치)."""
    n = len(S)
    Tm = [[T[i] if i == j else ZERO for j in range(n)] for i in range(n)]
    ST = matmul(S, Tm)
    ST3 = matmul(matmul(ST, ST), ST)
    S2 = matmul(S, S)
    # λ = ST3[i][j]/S2[i][j] (S2 비영 성분에서 일정해야)
    lam = None
    for i in range(n):
        for j in range(n):
            if S2[i][j] != ZERO:
                if ST3[i][j] == ZERO:
                    return None
                # λ = ST3/S2  (ℚ(i) 나눗셈)
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


def _cdiv(x, y):
    """x/y in ℚ(i): x·conj(y)/|y|²."""
    denom = y.a * y.a + y.b * y.b
    if denom == 0:
        return None
    num = x * y.conj()
    return Cyc(num.a / denom, num.b / denom)


def t_multiset(T):
    """T 값 다중집합을 정렬 키 리스트로 (쌍 대조용)."""
    return sorted((str(t.a), str(t.b)) for t in T)


# ════════════════════════════════════════════════════════════════════
#  검증 하네스
# ════════════════════════════════════════════════════════════════════
def verify_double(name):
    D = Double(name)
    S, T = D.S, D.T
    n = D.N
    res = {"group": name, "n_anyon": n, "quantum_dims": [str(d) for d in D.dim]}
    checks = {}
    # 1. anyon 수·Σd²
    Dsq = sum(d * d for d in D.dim)
    checks["n_anyon_22"] = (n == 22)
    checks["total_dim_64"] = (Dsq == 64)
    res["D2"] = Dsq
    # 2. S unitary (SS†=I)
    SS = matmul(S, dagger(S))
    checks["S_unitary"] = is_identity(SS)
    # 3. S symmetric
    checks["S_symmetric"] = all(S[i][j] == S[j][i] for i in range(n) for j in range(n))
    # 4. S² = charge conj (순열, C²=I)
    S2 = matmul(S, S)
    perm = perm_of(S2)
    checks["S2_is_perm"] = perm is not None
    if perm is not None:
        checks["C_squared_I"] = all(perm[perm[i]] == i for i in range(n))
        res["self_dual"] = (perm == list(range(n)))
    # 5. Verlinde 비음정수
    vok, vbad = verlinde_ok(S)
    checks["verlinde_nonneg_int"] = vok
    # 6. S_0a = d_a/8
    checks["first_row_dims"] = all(S[0][a] == Cyc(F(D.dim[a], 8)) for a in range(n))
    # 7. (ST)³ = λ S², λ=1 (c≡0 mod 8)
    lam = st_cubed_lambda(S, T)
    checks["stcubed_lambda1"] = (lam is not None and lam == ONE)
    res["lambda"] = None if lam is None else str(lam)
    # 8. T 유한위수 (T 성분은 root of unity: |value|²=1)
    checks["T_unit_modulus"] = all((t.a * t.a + t.b * t.b) == 1 for t in T)
    res["T_multiset"] = t_multiset(T)
    res["checks"] = checks
    res["all_pass"] = all(checks.values())
    return D, res


def teeth(name):
    """S 한 성분 섭동 → 최소 하나의 공리(unitary/verlinde) 붕괴."""
    D = Double(name)
    S = [row[:] for row in D.S]
    S[0][1] = S[0][1] + ONE            # 섭동
    broke = not is_identity(matmul(S, dagger(S)))
    if not broke:
        vok, _ = verlinde_ok(S)
        broke = not vok
    return broke


def main():
    quick = "--quick" in sys.argv
    out = {"_schema": "dihedral-quaternion-double/v1",
           "_note": ("D(D₄)·D(Q₈) 완전 modular data 자체구성 + 쌍 대조(관측·seal 아님). "
                     "★군 문자표 동치≠double MTC 동치: T 다중집합 분기. root 불변 sidecar·신규 module 0.")}
    D_d4, r_d4 = verify_double("D4")
    D_q8, r_q8 = verify_double("Q8")
    out["D_D4"] = r_d4
    out["D_Q8"] = r_q8
    # ★쌍 대조
    same_S_spectrum = (sorted(str(D_d4.S[0][a]) for a in range(22)) ==
                       sorted(str(D_q8.S[0][a]) for a in range(22)))
    t_d4 = r_d4["T_multiset"]; t_q8 = r_q8["T_multiset"]
    out["pair_contrast"] = {
        "both_22_anyon": r_d4["n_anyon"] == 22 == r_q8["n_anyon"],
        "both_D2_64": r_d4["D2"] == 64 == r_q8["D2"],
        "same_quantum_dims": sorted(r_d4["quantum_dims"]) == sorted(r_q8["quantum_dims"]),
        "T_multiset_differs": t_d4 != t_q8,
        "insight": "동일 문자표/차원/D² 이나 T 다중집합 상이 → double 비동형(관측)"
                   if t_d4 != t_q8 else "T 다중집합 일치(재검토 필요)",
    }
    teeth_d4 = teeth("D4"); teeth_q8 = teeth("Q8")
    out["teeth"] = {"D4_perturbation_breaks": teeth_d4, "Q8_perturbation_breaks": teeth_q8}
    all_ok = (r_d4["all_pass"] and r_q8["all_pass"] and teeth_d4 and teeth_q8
              and out["pair_contrast"]["both_22_anyon"]
              and out["pair_contrast"]["both_D2_64"])
    out["all_ok"] = bool(all_ok)

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "DIHEDRAL-QUATERNION-DOUBLE.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print(f"D(D₄): {r_d4['n_anyon']} anyon · D²={r_d4['D2']} · all_pass={r_d4['all_pass']}", flush=True)
        print(f"D(Q₈): {r_q8['n_anyon']} anyon · D²={r_q8['D2']} · all_pass={r_q8['all_pass']}", flush=True)
        print(f"★쌍 대조: 동일 차원={out['pair_contrast']['same_quantum_dims']} · "
              f"T 다중집합 상이={out['pair_contrast']['T_multiset_differs']} → double 비동형 관측", flush=True)
        print(f"  → .pgf/proofs/DIHEDRAL-QUATERNION-DOUBLE.json", flush=True)
    print(f"dihedral_quaternion_double: all_ok={out['all_ok']}", flush=True)
    return 0 if out["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
