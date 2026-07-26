#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""g2_1_mtc_observe — ★**(G₂)₁ 완전 modular data + Fibonacci 동형 판정**
(관측, seal 아님). v20 §4 잔여 후보 — [[su3_3_mtc_observe]]의 "G₂ level-1 rank=2 정정"
(agent07 'rank=14'=dim(G₂) 혼동)을 **완전 modular data + 어느 Fib 인지의 판정**으로 승격.

핵심 물음: Fibonacci **융합환**(τ×τ=1+τ)을 갖는 MTC 는 정확히 **4개**(Galois 궤도) —
  (d_τ, θ_τ) ∈ {(φ, ζ₅²)=Fib, (φ, ζ₅³)=conj-Fib, (−1/φ, ζ₅⁴)=Yang-Lee, (−1/φ, ζ₅)=conj-YL}.
[[su2_3_mtc_observe]]는 "Fibonacci fusion"까지만, [[su3_2_mtc_observe]]는 "Fib̄⊠ℤ₃"를 확립했다.
본 관측은 **(G₂)₁ 이 그중 정확히 어느 것인가**를 gauge-불변 인증서로 판정한다.

관측 7축 (전부 ℚ(ζ₆₀)/ℚ(ζ₄₀) 정확 Fraction 산술 — float/simplify 없음):
  A. ★**일반 level-1 Lie 엔진 자체유도**: Cartan A + d_i=(αᵢ,αᵢ)/2 만 입력 →
     근계 반사폐포 · dim𝔤 = #근 + rank · 장단비 · highest root marks → **comarks
     a∨ᵢ=aᵢdᵢ/d_θ** → h∨ · level-k 적분가중치 · Weyl 군 행렬 폐포(부호=길이 패리티) ·
     **Weyl 차원공식** · Gram(ω) · h_λ=(λ,λ+2ρ)/2(k+h∨) · c=k·dim𝔤/(k+h∨).
     G₂: 12근·dim 14·장단비 3·θ=2α₁+3α₂·marks (2,3)·**comarks (2,1)**·h∨=4 →
     **level-1 primaries = {0, ω₂}(rank 2)** · ω₂ = **7차원 표현**(Weyl 차원공식 자체확인,
     ω₁=14=adjoint) · **c=14/5** · **h_τ=2/5**.
  B. **완전 modular data**: Kac-Peterson 2×2 S̃ (|W(G₂)|=12) exact — S̃ 대칭 ·
     S̃S̃†=|N|·I · **S̃²=κ·C, C=I(self-dual)** · dims **(1, φ)** · **D²=2+φ=(5+√5)/2** ·
     T̃=diag(e^{2πi(h−c/24)}) · **(S̃T̃)³ ∝ S̃²**.
  C. **Verlinde → Fibonacci 융합환**: N 전수 비음정수 · **N_ττ^1=N_ττ^τ=1, τ×τ=1+τ** ·
     d_τ²=1+d_τ(황금비 방정식).
  D. ★**c mod 8 exact 인증(Gauss 합)**: p₊=Σd_a²θ_a · **p₊·p₋=D²** · **p₊ = D·ζ₂₀^{7}**
     ⟺ e^{2πi c/8}, c=14/5 — CFT 공식 c=k·dim𝔤/(k+h∨) 과 **독립** 경로로 일치.
  E. ★★**Fibonacci 동형 판정(crux)**: 인증서 (d_τ,θ_τ)=(φ, ζ₅²) → **(G₂)₁ ≅ Fib 확정**
     (conj-Fib 아님·YL 아님). + **Galois 4-궤도 자체유도**: σ_t(ζ₅→ζ₅^t) 를 modular data
     에 적용 → t=1:Fib · t=4:**conj-Fib** · t=2,3:**Yang-Lee 계열(d<0 비유니터리)** —
     네 해가 정확히 Fib 융합환의 전 실현.
  F. ★**SU(2)₃ ⊠-분해 인증서**: SU(2)₃(A₁ level 3) modular data 를 **같은 엔진으로 재유도**
     → 라벨사상 0↔(0,1)·1↔(g,τ)·2↔(0,τ)·3↔(g,1) 에서
     **Ŝ^{SU(2)₃} = Ŝ^{anti-semion} ⊗ Ŝ^{(G₂)₁}** 16성분 정확 · **h 가법 mod 1 정확** ·
     c: 9/5 = (−1) + 14/5. ⟹ **(G₂)₁ ≅ SU(2)₃ 의 Fib 인수**(modular data 수준).
     ★대조: pointed {0,3/2} 부분 S 는 **비퇴화(rank 2)** → Müger ⊠-분해 **가능** —
     [[su3_3_mtc_observe]]의 SU(3)₃ pointed 완전퇴화(분해 불가)와 **정반대 극**.
  G. ★**(F₄)₁ 켤레 실증**: 같은 엔진으로 F₄(48근·dim 52·comarks (2,3,2,1)·h∨=9) →
     level-1 primaries 2 · ω₄=**26차원** · c=**26/5** · h=**3/5** · d=φ ⟹ **conj-Fib**
     이고 **(F₄)₁ = σ₄((G₂)₁)** (Galois 켤레) 정확 일치. SU(3)₂ 의 Fib̄ 인수(h_τ=3/5)와
     같은 쪽 — 즉 **(G₂)₁ ≇ SU(3)₂ 의 Fib 인수**(서로 복소켤레).

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - modular data = 조합·대수 exact 표 — braiding 게이트 실봉인·F/R-symbol 무주장.
  - "동형" = **S·T(modular data) 수준** 동치 — 범주 동치(F/R-symbol pentagon/hexagon)는
    [[fib_braid_observe]]/[[mtc_braid_observe]] 소관·무주장.
  - "Fib 융합환 MTC = 정확히 4개"는 인용된 분류정리가 아니라 **본 관측이 산출한 Galois
    궤도 4해**(같은 Verlinde 방정식의 전 해집합 주장 아님 — 궤도 크기 4 자체유도).
  - (F₄)₁·SU(2)₃ 는 대조축 — 각각의 완전 MTC 공리 전수는 본 관측 범위 밖.

사용: python -m qf_witness.observe.g2_1_mtc_observe [--quick]
"""
from __future__ import annotations
import sys
import json
from fractions import Fraction as Fr


# ══════════════════════════════════════════════════════════════════════════
# 1. 일반 ℚ(ζ_N) 정확 산술 (Φ_N 자체유도 — 표 하드코딩 없음)
# ══════════════════════════════════════════════════════════════════════════
def _polydiv(num, den):
    """오름차순 계수 다항식 정확 나눗셈(나머지 0 가정)."""
    num = list(num)
    q = [Fr(0)] * (len(num) - len(den) + 1)
    for i in range(len(num) - len(den), -1, -1):
        c = num[i + len(den) - 1] / den[-1]
        q[i] = c
        if c:
            for j in range(len(den)):
                num[i + j] -= c * den[j]
    return q


_CYC_CACHE = {}


def cyclotomic(n):
    """Φ_n(x) 오름차순 계수 — x^n−1 = Π_{d|n} Φ_d 로 재귀 유도."""
    if n in _CYC_CACHE:
        return _CYC_CACHE[n]
    p = [Fr(-1)] + [Fr(0)] * (n - 1) + [Fr(1)]
    for d in range(1, n):
        if n % d == 0:
            p = _polydiv(p, cyclotomic(d))
    _CYC_CACHE[n] = p
    return p


class Cyc:
    """ℚ(ζ_N) — 원소 = 길이 deg(=φ(N)) Fraction 튜플(기저 1,ζ,…,ζ^{deg−1})."""

    def __init__(self, N):
        self.N = N
        phi = cyclotomic(N)
        self.deg = len(phi) - 1
        self.phi = phi
        M = 2 * self.deg + N + 2
        XP = []
        for m in range(M):
            if m < self.deg:
                v = [Fr(0)] * self.deg
                v[m] = Fr(1)
            else:
                prev = XP[m - 1]
                v = [Fr(0)] * self.deg
                for i in range(self.deg - 1):
                    v[i + 1] = prev[i]
                ov = prev[self.deg - 1]
                if ov:
                    for i in range(self.deg):
                        v[i] -= ov * phi[i]          # x^deg = −Σ φ_i x^i (monic)
            XP.append(tuple(v))
        self.XP = XP
        self.zero = tuple([Fr(0)] * self.deg)
        self.one = XP[0]

    def z(self, k):
        return self.XP[k % self.N]

    def add(self, a, b):
        return tuple(x + y for x, y in zip(a, b))

    def sub(self, a, b):
        return tuple(x - y for x, y in zip(a, b))

    def scale(self, a, f):
        f = Fr(f)
        return tuple(x * f for x in a)

    def mul(self, a, b):
        r = [Fr(0)] * self.deg
        for i, x in enumerate(a):
            if not x:
                continue
            for j, y in enumerate(b):
                if not y:
                    continue
                p = x * y
                t = self.XP[i + j]
                for m in range(self.deg):
                    if t[m]:
                        r[m] += p * t[m]
        return tuple(r)

    def gal(self, a, t):
        """σ_t : ζ_N → ζ_N^t (t coprime N)."""
        r = [Fr(0)] * self.deg
        for i, x in enumerate(a):
            if not x:
                continue
            t2 = self.XP[(i * t) % self.N]
            for m in range(self.deg):
                if t2[m]:
                    r[m] += x * t2[m]
        return tuple(r)

    def conj(self, a):
        return self.gal(a, self.N - 1)

    def iszero(self, a):
        return all(x == 0 for x in a)

    def inv(self, a):
        n = self.deg
        cols = []
        for j in range(n):
            e = [Fr(0)] * n
            e[j] = Fr(1)
            cols.append(self.mul(a, tuple(e)))
        A = [[cols[j][i] for j in range(n)] + [Fr(1) if i == 0 else Fr(0)] for i in range(n)]
        for c in range(n):
            pr = next(r for r in range(c, n) if A[r][c] != 0)
            A[c], A[pr] = A[pr], A[c]
            f = A[c][c]
            A[c] = [x / f for x in A[c]]
            for r in range(n):
                if r != c and A[r][c] != 0:
                    f2 = A[r][c]
                    A[r] = [A[r][kk] - f2 * A[c][kk] for kk in range(n + 1)]
        return tuple(A[i][n] for i in range(n))

    # ── ℚ(√5) 좌표(교차-필드 비교용) ────────────────────────────────────
    def sqrt5(self):
        assert self.N % 5 == 0
        q = self.N // 5
        return self.add(self.one, self.scale(self.add(self.z(q), self.z(4 * q)), 2))

    def q5coords(self, s5, x):
        """x = a·1 + b·√5 의 (a,b) — 아니면 None."""
        u, v = self.one, s5
        n = self.deg
        for i in range(n):
            for j in range(i + 1, n):
                det = u[i] * v[j] - u[j] * v[i]
                if det == 0:
                    continue
                a = (x[i] * v[j] - x[j] * v[i]) / det
                b = (u[i] * x[j] - u[j] * x[i]) / det
                if all(a * u[m] + b * v[m] == x[m] for m in range(n)):
                    return (a, b)
                return None
        return None


# ══════════════════════════════════════════════════════════════════════════
# 2. 일반 level-k Lie 엔진 (Cartan A + d 만 입력)
#    관례: A[i][j] = 2(αᵢ,αⱼ)/(αᵢ,αᵢ) ,  dᵢ = (αᵢ,αᵢ)/2
# ══════════════════════════════════════════════════════════════════════════
def mat_inv(A):
    n = len(A)
    M = [[Fr(A[i][j]) for j in range(n)] + [Fr(1) if i == j else Fr(0) for j in range(n)]
         for i in range(n)]
    for c in range(n):
        pr = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[pr] = M[pr], M[c]
        f = M[c][c]
        M[c] = [x / f for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f2 = M[r][c]
                M[r] = [M[r][k] - f2 * M[c][k] for k in range(2 * n)]
    return [[M[i][n + j] for j in range(n)] for i in range(n)]


class LieLevel:
    def __init__(self, name, A, d, k):
        self.name = name
        self.n = n = len(A)
        self.A = A
        self.d = [Fr(x) for x in d]
        self.k = k
        # 대칭성 게이트: A[i][j]dᵢ = A[j][i]dⱼ
        self.symmetrizable = all(Fr(A[i][j]) * self.d[i] == Fr(A[j][i]) * self.d[j]
                                 for i in range(n) for j in range(n))
        # ── 근계 = 단순근의 반사 폐포 ──────────────────────────────────
        simple = [tuple(1 if j == i else 0 for j in range(n)) for i in range(n)]
        roots = set(simple)
        frontier = list(simple)
        while frontier:
            nf = []
            for r in frontier:
                for i in range(n):
                    pair = sum(r[j] * A[i][j] for j in range(n))
                    nr = tuple(r[j] - (pair if j == i else 0) for j in range(n))
                    if nr not in roots:
                        roots.add(nr)
                        nf.append(nr)
            frontier = nf
        self.roots = roots
        self.pos = sorted([r for r in roots if all(x >= 0 for x in r)],
                          key=lambda r: (sum(r), r))
        self.dim_g = len(roots) + n
        # ── 대칭 쌍선형형(단순근 좌표) ────────────────────────────────
        self.bil = lambda r, s: sum(Fr(r[i]) * Fr(s[j]) * Fr(A[i][j]) * self.d[i]
                                    for i in range(n) for j in range(n))
        self.lens = sorted(set(self.bil(r, r) for r in roots))
        # ── highest root · marks · comarks · h∨ ───────────────────────
        self.theta = max(self.pos, key=lambda r: (sum(r), self.bil(r, r)))
        self.marks = list(self.theta)
        d_theta = self.bil(self.theta, self.theta) / 2
        self.d_theta = d_theta
        self.comarks = [Fr(self.marks[i]) * self.d[i] / d_theta for i in range(n)]
        self.h_dual = 1 + sum(self.comarks)
        # ── level-k 적분가중치(ω-좌표) ────────────────────────────────
        self.weights = []
        cur = [0] * n

        def rec(i, rem):
            if i == n:
                self.weights.append(tuple(cur))
                return
            ci = self.comarks[i]
            m = 0
            while ci * m <= rem:
                cur[i] = m
                rec(i + 1, rem - ci * m)
                m += 1
            cur[i] = 0
        rec(0, Fr(k))
        self.weights.sort(key=lambda w: (sum(w), w))
        # ── Gram(ω) : G[i][j] = (ωᵢ,ωⱼ) = (A⁻¹)[j][i]·dⱼ ─────────────
        Ainv = mat_inv(A)
        self.G = [[Ainv[j][i] * self.d[j] for j in range(n)] for i in range(n)]
        self.gram_symmetric = all(self.G[i][j] == self.G[j][i]
                                  for i in range(n) for j in range(n))
        self.rho = tuple([1] * n)
        # ── Weyl 군(ω-좌표 행렬) + 부호=길이 패리티 ────────────────────
        gens = []
        for i in range(n):
            M = tuple(tuple(Fr(1 if j == kk else 0) - (Fr(A[j][i]) if kk == i else Fr(0))
                            for kk in range(n)) for j in range(n))
            gens.append(M)
        idm = tuple(tuple(Fr(1 if a == b else 0) for b in range(n)) for a in range(n))
        W = {idm: 0}
        frontier = [idm]
        while frontier:
            nf = []
            for w in frontier:
                lw = W[w]
                for g in gens:
                    nw = tuple(tuple(sum(g[a][c] * w[c][b] for c in range(n))
                                     for b in range(n)) for a in range(n))
                    if nw not in W:
                        W[nw] = (lw + 1) % 2
                        nf.append(nw)
            frontier = nf
        self.W = W
        self.kh = k + self.h_dual

    # 가중치(ω-좌표) 내적
    def ipw(self, u, v):
        return sum(Fr(u[i]) * Fr(v[j]) * self.G[i][j]
                   for i in range(self.n) for j in range(self.n))

    def act(self, w, lam):
        return tuple(sum(w[a][b] * Fr(lam[b]) for b in range(self.n)) for a in range(self.n))

    def weyl_dim(self, lam):
        """Weyl 차원공식 Π_{α>0} (λ+ρ,α)/(ρ,α) — (ω_i,α_j)=δ_ij d_j 사용."""
        num = Fr(1)
        for a in self.pos:
            top = sum((Fr(lam[i]) + 1) * Fr(a[i]) * self.d[i] for i in range(self.n))
            bot = sum(Fr(a[i]) * self.d[i] for i in range(self.n))
            num *= top / bot
        return num

    def h(self, lam):
        lr = tuple(Fr(lam[i]) + 2 for i in range(self.n))   # λ+2ρ
        return self.ipw(lam, lr) / (2 * self.kh)

    def c(self):
        return Fr(self.k) * self.dim_g / self.kh

    def s_tilde(self, F, kh_override=None):
        """Kac-Peterson S̃_{λμ} = Σ_w ε(w) ζ_N^{−e}, e = N(w(λ+ρ),μ+ρ)/(k+h∨).

        kh_override = 고의로 틀린 level 분모(teeth 음성대조 전용).
        """
        kh = self.kh if kh_override is None else Fr(kh_override)
        m = len(self.weights)
        St = [[F.zero] * m for _ in range(m)]
        shifted = [tuple(x + 1 for x in lam) for lam in self.weights]
        for i in range(m):
            for j in range(m):
                acc = F.zero
                for w, sgn in self.W.items():
                    q = self.ipw(self.act(w, shifted[i]), shifted[j]) / kh
                    e = q * F.N
                    assert e.denominator == 1, f"{self.name}: exponent {e} not integral in ζ_{F.N}"
                    t = F.z(int(-e) % F.N)
                    acc = F.add(acc, t) if sgn == 0 else F.sub(acc, t)
                St[i][j] = acc
        return St


# ── 표준 입력 데이터 (Cartan + d) ────────────────────────────────────────
G2_A = [[2, -1], [-3, 2]]                      # α₁ long, α₂ short
G2_D = [Fr(1), Fr(1, 3)]
F4_A = [[2, -1, 0, 0], [-1, 2, -1, 0], [0, -2, 2, -1], [0, 0, -1, 2]]
F4_D = [Fr(1), Fr(1), Fr(1, 2), Fr(1, 2)]
A1_A = [[2]]
A1_D = [Fr(1)]


# ══════════════════════════════════════════════════════════════════════════
def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "g2-1-mtc/v1",
           "_note": ("(G₂)₁ 완전 modular data + Fibonacci 동형 판정 — 일반 level-1 Lie 엔진 "
                     "자체유도·Gauss 합 c mod 8 exact·Galois 4-궤도·SU(2)₃ ⊠-분해 인증서·"
                     "(F₄)₁=σ₄((G₂)₁) 켤레. 관측·seal 아님·module 0·root 불변.")}

    F60 = Cyc(60)
    S5_60 = F60.sqrt5()
    R["z_field_sqrt5_squared_5"] = (F60.mul(S5_60, S5_60) == F60.scale(F60.one, 5))
    PHI60 = F60.scale(F60.add(F60.one, S5_60), Fr(1, 2))
    R["z_phi_golden_eq"] = (F60.mul(PHI60, PHI60) == F60.add(F60.one, PHI60))

    # ═══ A. G₂ 근계·level-1 스펙트럼 자체유도 ══════════════════════════
    g2 = LieLevel("G2", G2_A, G2_D, 1)
    R["A_symmetrizable"] = g2.symmetrizable
    R["A_g2_12_roots"] = (len(g2.roots) == 12)
    R["A_g2_dim14"] = (g2.dim_g == 14)
    R["A_two_lengths_ratio3"] = (len(g2.lens) == 2 and g2.lens[1] / g2.lens[0] == 3)
    R["A_highest_marks_23"] = (g2.marks == [2, 3])
    R["A_comarks_21"] = (g2.comarks == [Fr(2), Fr(1)])
    R["A_h_dual_4"] = (g2.h_dual == 4)
    R["A_level1_rank2"] = (len(g2.weights) == 2 and g2.weights == [(0, 0), (0, 1)])
    R["A_gram_symmetric"] = g2.gram_symmetric
    R["A_weyl_order_12"] = (len(g2.W) == 12)
    R["A_weyl_dim_7_and_14"] = (g2.weyl_dim((0, 1)) == 7 and g2.weyl_dim((1, 0)) == 14)
    c_g2 = g2.c()
    h_g2 = [g2.h(w) for w in g2.weights]
    R["A_central_charge_14_5"] = (c_g2 == Fr(14, 5))
    R["A_h_tau_2_5"] = (h_g2 == [Fr(0), Fr(2, 5)])
    out["G2_level1"] = {"roots": 12, "dim_g": 14, "marks": g2.marks,
                        "comarks": [str(x) for x in g2.comarks], "h_dual": 4,
                        "primaries": ["0 (vacuum, dim 1)", "ω₂ (dim 7, short-node comark 1)"],
                        "c": str(c_g2), "h": [str(x) for x in h_g2],
                        "note": "★agent07 'rank=14' = dim(G₂) 혼동 — 정확 rank 2 (su3_3 정정 승격)"}

    # ═══ B. 완전 modular data ═════════════════════════════════════════
    St = g2.s_tilde(F60)
    R["B_S_symmetric"] = (St[0][1] == St[1][0])
    # S̃S̃† = Norm·I
    def gram(F, M, m):
        out_ = []
        for i in range(m):
            row = []
            for j in range(m):
                acc = F.zero
                for kk in range(m):
                    acc = F.add(acc, F.mul(M[i][kk], F.conj(M[j][kk])))
                row.append(acc)
            out_.append(row)
        return out_
    GG = gram(F60, St, 2)
    norm = GG[0][0]
    nrat = F60.q5coords(S5_60, norm)
    R["B_S_unitary_scalar"] = (GG[1][1] == norm and F60.iszero(GG[0][1])
                               and nrat is not None and nrat[1] == 0)
    NORM = nrat[0] if nrat else None
    R["B_norm_rational_positive"] = (NORM is not None and NORM > 0)
    # S̃² = κ·C  (self-dual → C = I)
    S2 = [[F60.add(F60.mul(St[i][0], St[0][j]), F60.mul(St[i][1], St[1][j]))
           for j in range(2)] for i in range(2)]
    R["B_S2_scalar_C_identity"] = (S2[0][0] == S2[1][1] and F60.iszero(S2[0][1])
                                   and F60.iszero(S2[1][0]) and not F60.iszero(S2[0][0]))
    # dims
    inv00 = F60.inv(St[0][0])
    dims = [F60.mul(St[0][i], inv00) for i in range(2)]
    R["B_dims_1_phi"] = (dims[0] == F60.one and dims[1] == PHI60)
    D2 = F60.add(F60.mul(dims[0], dims[0]), F60.mul(dims[1], dims[1]))
    R["B_D2_2_plus_phi"] = (D2 == F60.add(F60.scale(F60.one, 2), PHI60))
    d2c = F60.q5coords(S5_60, D2)
    R["B_D2_field_Qsqrt5"] = (d2c == (Fr(5, 2), Fr(1, 2)))          # (5+√5)/2
    # KP 정규화가 MTC-정합: S₀₀ = S̃₀₀/√Norm = ±1/D  ⟺  S̃₀₀²·D² = Norm
    R["B_S00_normalization_inv_D"] = (
        NORM is not None and F60.conj(St[0][0]) == St[0][0]
        and F60.mul(F60.mul(St[0][0], St[0][0]), D2) == F60.scale(F60.one, NORM))
    # T̃ = diag(e^{2πi(h − c/24)}) — 지수 분모 60
    Tm = []
    okT = True
    for hh in h_g2:
        e = (hh - c_g2 / 24) * 60
        if e.denominator != 1:
            okT = False
        Tm.append(F60.z(int(e) % 60))
    R["B_T_zeta60_integral"] = okT
    ST = [[F60.mul(St[i][j], Tm[j]) for j in range(2)] for i in range(2)]

    def mm(Aa, Bb):
        return [[F60.add(F60.mul(Aa[i][0], Bb[0][j]), F60.mul(Aa[i][1], Bb[1][j]))
                 for j in range(2)] for i in range(2)]
    ST3 = mm(mm(ST, ST), ST)
    # (S̃T̃)³ = κ·S̃²  (C=I 이므로 S̃² 는 스칼라행렬)
    R["B_ST3_prop_S2"] = (ST3[0][0] == ST3[1][1] and F60.iszero(ST3[0][1])
                          and F60.iszero(ST3[1][0]))
    out["modular_data"] = {
        "rank": 2, "S_norm": str(NORM), "dims": ["1", "φ=(1+√5)/2"],
        "D2": "2+φ = (5+√5)/2", "T": "diag(e^{−2πi·7/60}, e^{2πi·17/60})",
        "field": "S̃ ∈ ℚ(ζ₁₅) ⊂ ℚ(ζ₆₀) · Ŝ=S̃/S̃₀₀ ∈ ℚ(√5) · θ ∈ ℚ(ζ₅)"}

    # ═══ C. Verlinde → Fibonacci 융합환 ══════════════════════════════
    inv0 = [F60.inv(St[0][L]) for L in range(2)]
    invN = F60.inv(F60.scale(F60.one, NORM))
    fus = {}
    verl_ok = True
    for i in range(2):
        for j in range(2):
            for kk in range(2):
                acc = F60.zero
                for L in range(2):
                    t = F60.mul(F60.mul(St[i][L], St[j][L]),
                                F60.mul(F60.conj(St[kk][L]), inv0[L]))
                    acc = F60.add(acc, t)
                acc = F60.mul(acc, invN)
                cc = F60.q5coords(S5_60, acc)
                if cc is None or cc[1] != 0 or cc[0].denominator != 1 or cc[0] < 0:
                    verl_ok = False
                    fus[(i, j, kk)] = None
                else:
                    fus[(i, j, kk)] = int(cc[0])
    R["C_verlinde_nonneg_int"] = verl_ok
    R["C_fibonacci_fusion"] = (fus.get((1, 1, 0)) == 1 and fus.get((1, 1, 1)) == 1
                               and fus.get((0, 1, 1)) == 1 and fus.get((0, 0, 0)) == 1)
    R["C_dtau_golden"] = (F60.mul(dims[1], dims[1]) == F60.add(F60.one, dims[1]))
    out["fusion"] = {"rule": "τ×τ = 1 + τ (Fibonacci)",
                     "N_tau_tau": {"1": fus.get((1, 1, 0)), "tau": fus.get((1, 1, 1))}}

    # ═══ D. Gauss 합 → c mod 8 exact ═════════════════════════════════
    theta = [F60.z(int(hh * 60) % 60) for hh in h_g2]         # θ_a = e^{2πi h_a}
    R["D_theta_tau_zeta5_sq"] = (theta[1] == F60.z(24))       # ζ₆₀^24 = ζ₅²
    pplus = F60.zero
    pminus = F60.zero
    for a in range(2):
        da2 = F60.mul(dims[a], dims[a])
        pplus = F60.add(pplus, F60.mul(da2, theta[a]))
        pminus = F60.add(pminus, F60.mul(da2, F60.conj(theta[a])))
    R["D_gauss_pp_pm_eq_D2"] = (F60.mul(pplus, pminus) == D2)
    # D = √5 / (2 sin(π/5)) ,  2 sin(π/5) = ζ₆₀⁹ − ζ₆₀²¹
    twosin = F60.sub(F60.z(9), F60.z(21))
    Dtot = F60.mul(S5_60, F60.inv(twosin))
    R["D_total_dim_sq_matches"] = (F60.mul(Dtot, Dtot) == D2)
    # p₊ = D · e^{2πi c/8} , c=14/5 → c/8 = 7/20 = 21/60
    R["D_central_charge_mod8_exact"] = (pplus == F60.mul(Dtot, F60.z(21)))
    out["anomaly"] = {"p_plus_over_D": "e^{2πi·7/20} = e^{2πi(14/5)/8}",
                      "c_mod_8": "14/5 — Gauss 합 경로가 CFT 공식 k·dim𝔤/(k+h∨) 와 독립 일치"}

    # ═══ E. ★Fibonacci 동형 판정 + Galois 4-궤도 ═════════════════════
    # 인증서 = (d_τ, θ_τ). Fib := (φ, ζ₅²) · conj-Fib := (φ, ζ₅³)
    #          YL := (−1/φ, ζ₅⁴) · conj-YL := (−1/φ, ζ₅)
    dt = F60.q5coords(S5_60, dims[1])
    R["E_dtau_is_phi_positive"] = (dt == (Fr(1, 2), Fr(1, 2)))
    R["E_verdict_is_Fib_not_conj"] = (dt == (Fr(1, 2), Fr(1, 2)) and theta[1] == F60.z(24)
                                      and theta[1] != F60.z(36))
    # Galois 궤도: σ_t (t coprime 60, ζ₅→ζ₅^{t mod 5}) 를 (d_τ, θ_τ) 에 적용
    orbit = {}
    for t in (1, 7, 13, 19):        # t mod 5 = 1,2,3,4 · 전부 gcd(t,60)=1
        dtau_t = F60.gal(dims[1], t)
        th_t = F60.gal(theta[1], t)
        cc = F60.q5coords(S5_60, dtau_t)
        # θ 를 ζ₅^m 로 동정
        m = next((mm_ for mm_ in range(5) if th_t == F60.z(12 * mm_)), None)
        orbit[t] = (cc, m)
    R["E_orbit_t1_Fib"] = (orbit[1] == ((Fr(1, 2), Fr(1, 2)), 2))
    R["E_orbit_t19_conjFib"] = (orbit[19] == ((Fr(1, 2), Fr(1, 2)), 3))
    R["E_orbit_t7_YangLee"] = (orbit[7] == ((Fr(1, 2), Fr(-1, 2)), 4))
    R["E_orbit_t13_conjYangLee"] = (orbit[13] == ((Fr(1, 2), Fr(-1, 2)), 1))
    R["E_orbit_size_4_distinct"] = (len(set(orbit.values())) == 4)
    # −1/φ 확인: (1−√5)/2 = −1/φ
    neginv = F60.scale(F60.sub(F60.one, S5_60), Fr(1, 2))
    R["E_YL_dim_is_neg_inv_phi"] = (F60.mul(neginv, PHI60) == F60.scale(F60.one, -1))
    out["fib_verdict"] = {
        "certificate": "(d_τ, θ_τ) = (φ, ζ₅²)",
        "verdict": "★(G₂)₁ ≅ **Fib** (conj-Fib 아님 · Yang-Lee 계열 아님)",
        "galois_orbit": {"σ₁": "(φ, ζ₅²) = Fib = (G₂)₁",
                         "σ₄(t=19)": "(φ, ζ₅³) = conj-Fib = (F₄)₁",
                         "σ₂(t=7)": "(−1/φ, ζ₅⁴) = Yang-Lee (비유니터리)",
                         "σ₃(t=13)": "(−1/φ, ζ₅) = conj-Yang-Lee (비유니터리)"},
        "honesty": "궤도 크기 4 = 본 관측 자체유도 — 'Fib 융합환 MTC 는 정확히 4개' 분류정리 인용 아님"}

    # ═══ F. SU(2)₃ ⊠-분해 인증서 ═════════════════════════════════════
    F40 = Cyc(40)
    S5_40 = F40.sqrt5()
    R["F_sqrt5_in_z40"] = (F40.mul(S5_40, S5_40) == F40.scale(F40.one, 5))
    su23 = LieLevel("A1k3", A1_A, A1_D, 3)
    R["F_su23_rank4"] = (len(su23.weights) == 4 and su23.h_dual == 2)
    R["F_su23_c_9_5"] = (su23.c() == Fr(9, 5))
    h23 = [su23.h(w) for w in su23.weights]
    R["F_su23_h"] = (h23 == [Fr(0), Fr(3, 20), Fr(2, 5), Fr(3, 4)])
    St23 = su23.s_tilde(F40)
    inv23 = F40.inv(St23[0][0])
    Sh23 = [[F40.q5coords(S5_40, F40.mul(St23[i][j], inv23)) for j in range(4)]
            for i in range(4)]
    R["F_su23_Shat_in_Qsqrt5"] = all(Sh23[i][j] is not None for i in range(4) for j in range(4))
    # (G₂)₁ 의 Ŝ (ℚ(√5) 좌표)
    ShF = [[F60.q5coords(S5_60, F60.mul(St[i][j], inv00)) for j in range(2)] for i in range(2)]
    R["F_g2_Shat_matrix"] = (ShF == [[(Fr(1), Fr(0)), (Fr(1, 2), Fr(1, 2))],
                                     [(Fr(1, 2), Fr(1, 2)), (Fr(-1), Fr(0))]])
    # anti-semion: Ŝ = [[1,1],[1,−1]] · h = (0, 3/4) · c = −1
    Shs = [[Fr(1), Fr(1)], [Fr(1), Fr(-1)]]
    hs = [Fr(0), Fr(3, 4)]
    # 라벨사상 a → (semion, fib)
    LMAP = {0: (0, 0), 1: (1, 1), 2: (0, 1), 3: (1, 0)}

    def q5mul(x, y):
        """(a+b√5)(c+e√5)"""
        return (x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])
    tensor_ok = True
    for a in range(4):
        for b in range(4):
            sa, fa = LMAP[a]
            sb, fb = LMAP[b]
            want = q5mul((Shs[sa][sb], Fr(0)), ShF[fa][fb])
            if Sh23[a][b] != want:
                tensor_ok = False
    R["F_S_kronecker_exact"] = tensor_ok
    R["F_h_additive_mod1"] = all(
        (h23[a] - (hs[LMAP[a][0]] + h_g2[LMAP[a][1]])) % 1 == 0 for a in range(4))
    R["F_c_additive"] = (su23.c() == Fr(-1) + c_g2)
    # 대조: pointed {0, 3/2} 부분 S 비퇴화(rank 2) — SU(3)₃ 완전퇴화와 정반대
    P = (0, 3)
    sub = [[Sh23[i][j] for j in P] for i in P]
    det_sub = (sub[0][0][0] * sub[1][1][0] + 5 * sub[0][0][1] * sub[1][1][1]
               - sub[0][1][0] * sub[1][0][0] - 5 * sub[0][1][1] * sub[1][0][1])
    R["F_pointed_nondegenerate"] = (det_sub != 0)
    out["su2_3_factorization"] = {
        "map": "0↔(1,1) · 1↔(g,τ) · 2↔(1,τ) · 3↔(g,1)",
        "S": "Ŝ^{SU(2)₃} = Ŝ^{anti-semion} ⊗ Ŝ^{(G₂)₁} — 16성분 정확",
        "T": "h_{SU(2)₃} = h_semion + h_{(G₂)₁} (mod 1) 정확 · c: 9/5 = (−1) + 14/5",
        "verdict": "★(G₂)₁ ≅ SU(2)₃ 의 Fib 인수 (modular data 수준)",
        "contrast": ("pointed {0,3/2} 부분 S 는 **비퇴화(det≠0)** → Müger ⊠-분해 가능 — "
                     "su3_3_mtc_observe 의 SU(3)₃ pointed 완전퇴화(분해 불가)와 정반대 극")}

    # ═══ G. (F₄)₁ 켤레 실증 ═══════════════════════════════════════════
    if not quick:
        f4 = LieLevel("F4", F4_A, F4_D, 1)
        R["G_f4_symmetrizable"] = f4.symmetrizable
        R["G_f4_48_roots"] = (len(f4.roots) == 48)
        R["G_f4_dim52"] = (f4.dim_g == 52)
        R["G_f4_marks_2342"] = (f4.marks == [2, 3, 4, 2])
        R["G_f4_comarks_2321"] = (f4.comarks == [Fr(2), Fr(3), Fr(2), Fr(1)])
        R["G_f4_h_dual_9"] = (f4.h_dual == 9)
        R["G_f4_weyl_1152"] = (len(f4.W) == 1152)
        R["G_f4_level1_rank2"] = (len(f4.weights) == 2
                                  and f4.weights == [(0, 0, 0, 0), (0, 0, 0, 1)])
        R["G_f4_dim26"] = (f4.weyl_dim((0, 0, 0, 1)) == 26)
        c_f4 = f4.c()
        h_f4 = [f4.h(w) for w in f4.weights]
        R["G_f4_c_26_5"] = (c_f4 == Fr(26, 5))
        R["G_f4_h_3_5"] = (h_f4 == [Fr(0), Fr(3, 5)])
        St4 = f4.s_tilde(F60)
        inv4 = F60.inv(St4[0][0])
        d4 = F60.mul(St4[0][1], inv4)
        R["G_f4_dim_tau_phi"] = (d4 == PHI60)
        th4 = F60.z(int(h_f4[1] * 60) % 60)
        R["G_f4_theta_zeta5_cubed"] = (th4 == F60.z(36))
        # (F₄)₁ = σ₄((G₂)₁) : t=19 (ζ₅→ζ₅⁴)
        R["G_f4_is_galois_sigma4_of_g2"] = (d4 == F60.gal(dims[1], 19)
                                            and th4 == F60.gal(theta[1], 19))
        # Gauss 합: c=26/5 → c/8 = 13/20 = 39/60
        pp4 = F60.add(F60.one, F60.mul(F60.mul(d4, d4), th4))
        R["G_f4_anomaly_26_5"] = (pp4 == F60.mul(Dtot, F60.z(39)))
        out["F4_level1"] = {
            "roots": 48, "dim_g": 52, "marks": f4.marks,
            "comarks": [str(x) for x in f4.comarks], "h_dual": 9,
            "primaries": ["0 (vacuum)", "ω₄ (dim 26, comark 1)"],
            "c": str(c_f4), "h_tau": str(h_f4[1]),
            "verdict": "★(F₄)₁ ≅ conj-Fib = σ₄((G₂)₁) — Galois 켤레 정확 일치",
            "cross": ("su3_2_mtc_observe 의 SU(3)₂ ≅ Fib̄⊠ℤ₃ 인수(h_τ=3/5)와 같은 쪽 ⟹ "
                      "★(G₂)₁ ≇ SU(3)₂ 의 Fib 인수(서로 복소켤레)")}

    # ═══ teeth (음성 대조) ════════════════════════════════════════════
    # (a) comark 2 노드로 level-1 가중치를 잘못 취하면 적분가중치가 아님
    R["teeth_comark2_not_level1"] = (g2.comarks[0] * 1 > 1)
    # (b) 잘못된 level 분모(k+h∨=5 대신 6) → 같은 2×2 자리에서 Verlinde 비정수
    Fw = Cyc(18)                                  # 지수 분모 3·6 = 18
    Stw = g2.s_tilde(Fw, kh_override=6)
    GGw = gram(Fw, Stw, 2)
    normw = GGw[0][0]
    # 실제 파손 지점: S̃S̃† 가 스칼라행렬이 아님(정상 level 에서는 Norm·I)
    R["teeth_wrong_level_not_unitary"] = not (Fw.iszero(GGw[0][1]) and GGw[1][1] == normw
                                              and all(x == 0 for x in normw[1:]))
    # (b') 실제 level-2 는 rank 4(≠2) — Fibonacci 아님
    g2k2 = LieLevel("G2k2", G2_A, G2_D, 2)
    R["teeth_level2_rank4_not_fib"] = (len(g2k2.weights) == 4)
    # (c) θ 를 ζ₅³ 로 바꾸면 Gauss 합이 c=14/5 를 주지 않음
    th_bad = F60.z(36)
    pp_bad = F60.add(F60.one, F60.mul(F60.mul(dims[1], dims[1]), th_bad))
    R["teeth_conj_theta_breaks_anomaly"] = (pp_bad != F60.mul(Dtot, F60.z(21)))

    ok = bool(all(R.values()))
    out["checks"] = R
    out["scope_honesty"] = {
        "delivered": ("(G₂)₁ 완전 modular data(S·T·dims·D²·Verlinde·c mod 8) + "
                      "★Fibonacci 동형 판정(Fib 확정) + Galois 4-궤도 + SU(2)₃ ⊠-분해 인증서 + "
                      "(F₄)₁=σ₄((G₂)₁) 켤레"),
        "verdict_level": "S·T(modular data) 수준 동치 — F/R-symbol 범주동치 무주장",
        "not_claimed": ("braiding 게이트 실봉인 · pentagon/hexagon · "
                        "'Fib 융합환 MTC = 정확히 4개' 분류정리 인용 · "
                        "(F₄)₁/SU(2)₃ 의 전 MTC 공리 전수"),
        "engine": "일반 level-k Lie 엔진 — 입력은 Cartan A 와 dᵢ 뿐(표 하드코딩 없음)",
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "G2-1-MTC.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("(G₂)₁ 완전 modular data + Fibonacci 동형 판정 (exact — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  ★G₂: 12근·dim 14·marks(2,3)→comarks(2,1)·h∨=4 → level-1 primaries {1, 7} (rank 2)",
              flush=True)
        print("  ★modular data: dims(1,φ)·D²=2+φ·c=14/5·h_τ=2/5·τ×τ=1+τ", flush=True)
        print("  ★★동형 판정: (d_τ,θ_τ)=(φ,ζ₅²) ⟹ (G₂)₁ ≅ **Fib** (conj-Fib/Yang-Lee 아님)",
              flush=True)
        print("  ★Galois 4-궤도: σ₁=Fib · σ₄=conj-Fib=(F₄)₁ · σ₂,σ₃=Yang-Lee 계열(d=−1/φ)",
              flush=True)
        print("  ★SU(2)₃ = anti-semion ⊠ (G₂)₁ 정확(Ŝ Kronecker 16성분·h 가법·c 가법)", flush=True)
        print("  → .pgf/proofs/G2-1-MTC.json", flush=True)
    print(f"g2_1_mtc_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
