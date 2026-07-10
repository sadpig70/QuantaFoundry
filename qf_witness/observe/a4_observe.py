#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""a4_observe — TrackHE9 P4: 교대군 A₄ ζ₃-필연 문자표 witness (선검증·관측, seal 아님).

report9 수렴축(A₄ ζ₃ Fourier 4/8). ★비-rational 군-Fourier 계보의 **닫힘 조각**: B₃(ζ-free 정수 문자표,
[[b3_observe]])·S₄(정수 문자표, ζ₃는 Fourier 행렬에만=closed-negative)·Q₈(ζ-free)의 **상보** — A₄(12원소)는
**문자표 자체가 ζ₃ 를 강제**하는 비-rational 군이다. 이 계보에서 ζ₃ 가 지표값에 필연으로 등장하는 최초 사례.

핵심 논증(오라클 독립, 정수·대수 exact):
  1. A₄ = {0,1,2,3} 의 우치환 12개, 켤레류 4개(크기 1/3/4/4) — 8개 3-cycle 이 **두 클래스로 분열**.
  2. ★**NOT rational group**: 3-cycle g(order 3)·k=2(gcd=1) 에서 g²=g⁻¹ 가 g 와 **비켤레** →
     Q-group 아님 → 정수 문자표 불가(Burnside). B₃/S₄ 의 g^k~g 와 **정반대**([[b3_observe]] 대조).
  3. 아벨화 A₄/[A₄,A₄]=A₄/V₄ ≅ ℤ₃ (V₄=정규 Klein-4) → 1차원 기약표현 정확히 3개(ℤ₃ 쌍대).
  4. ★**ζ₃ 필연 = ℚ* 에 order-3 원소 없음**: x³=1, x∈ℚ ⟹ x=1 (유일 유리 root-of-unity=±1, order 1/2).
     3-cycle 은 order 3 → 비자명 1차원 지표는 order-3 근을 가져야 함 → **rational 불가 → χ₁(3-cycle)=ω=ζ₃**.
  5. 문자표(χ_triv·χ_ω·χ_ω²·χ₃=[3,−1,0,0]) 전체 orthogonality(Σ|C|χ_iχ_j*=12δ)가 ω 포함 시 exact 성립.
     teeth: χ₁(3-cycle) 을 rational(±1) 로 강제하면 orthogonality **붕괴**(정수 문자표 반증).

정직 경계(★선검증·seal 아님, root 불변 sidecar): 관측 = A₄ 표현론(ζ₃ 필연)·비-rational 판정·문자표 구조.
  ★**봉인은 여기서 멈춤** — A₄ Fourier(DFT over A₄)는 ω₃=e^{2πi/3} 대각 위상을 실체화하는 **z3_gate 신규
  승인 module 이 필요**(정욱님 사람게이트). 본 witness 는 "ω₃ 게이트를 열 가치가 있는가"의 **결정 근거**를
  제공할 뿐 신규 module 0·봉인 0. 실제 a4_qft·HSP 응용 = 승인 후/범위밖.

사용: python -m qf_witness.observe.a4_observe [--quick]
"""
from __future__ import annotations
import sys, itertools
from math import gcd
import numpy as np


def parity(p):
    return sum(1 for i in range(len(p)) for j in range(i + 1, len(p)) if p[i] > p[j]) % 2


def comp(p, q):
    return tuple(p[q[i]] for i in range(len(p)))              # (p∘q)[i]=p[q[i]]


def inv(p):
    r = [0] * len(p)
    for i in range(len(p)):
        r[p[i]] = i
    return tuple(r)


def order(p):
    idp = tuple(range(len(p)))
    n, x = 1, p
    while x != idp:
        x = comp(x, p); n += 1
    return n


def conj_class(g, elems):
    return frozenset(comp(comp(x, g), inv(x)) for x in elems)


def is_rational_group(elems):
    """b3_observe 규약: 각 g, gcd(k,ord)=1 → g^k ~ g. 반환 (bool, 반례)."""
    for g in elems:
        m = order(g); cc = conj_class(g, elems)
        for k in range(2, m):
            if gcd(k, m) == 1:
                p = g
                for _ in range(k - 1):
                    p = comp(p, g)
                if p not in cc:
                    return False, (g, k)
    return True, None


def classes_of(elems):
    seen, cls = set(), []
    for g in elems:
        c = conj_class(g, elems)
        if c not in seen:
            seen.add(c); cls.append(c)
    return cls


def main():
    quick = "--quick" in sys.argv
    R = {}
    A4 = [p for p in itertools.permutations(range(4)) if parity(p) == 0]
    ID = (0, 1, 2, 3)

    # 1. 군 구조
    R["a4_order_12"] = (len(A4) == 12)
    R["a4_closure"] = all(comp(a, b) in A4 for a in A4 for b in A4)
    cls = classes_of(A4)
    R["a4_four_classes_1_3_4_4"] = (sorted(len(c) for c in cls) == [1, 3, 4, 4])

    # 2. ★NOT rational group + 3-cycle 분열
    rg, wit = is_rational_group(A4)
    R["a4_not_rational_group"] = (rg is False)
    g = wit[0]; g2 = comp(g, g)
    R["threecycles_split"] = (order(g) == 3 and g2 not in conj_class(g, A4))

    # 3. 아벨화 A₄/V₄ ≅ ℤ₃
    V4 = frozenset(p for p in A4 if order(p) <= 2)
    R["v4_normal_order4"] = (len(V4) == 4)
    c3 = (1, 2, 0, 3)                                         # (012)

    def coset(x):
        for j, rep in enumerate((ID, c3, comp(c3, c3))):
            if comp(inv(rep), x) in V4:
                return j
        return -1
    R["abelianization_z3_hom"] = all(coset(comp(a, b)) == (coset(a) + coset(b)) % 3 for a in A4 for b in A4)
    R["z3_cosets_balanced"] = (sorted(sum(1 for x in A4 if coset(x) == j) for j in range(3)) == [4, 4, 4])

    # 4. ★ζ₃ 필연: ℚ 의 order-3 root of unity 부재
    rational_roots_of_unity = [1, -1]                        # ℚ*∩μ_∞ = {±1} (Kronecker)
    R["no_rational_order3"] = ([x for x in rational_roots_of_unity
                                if abs(x ** 3 - 1) < 1e-12 and abs(x - 1) > 1e-12] == [])

    # 5. 문자표 orthogonality (ω 포함 exact) + teeth
    w = np.exp(2j * np.pi / 3)
    reps = [min(cc, key=lambda p: (order(p), p)) for cc in
            sorted(cls, key=lambda cc: (len(cc), min(cc)))]
    reps = sorted(reps, key=lambda r: (len(conj_class(r, A4)), coset(r)))
    sizes = [len(conj_class(r, A4)) for r in reps]

    def fix(p): return sum(1 for i in range(4) if p[i] == i)
    table = [[1] * 4,
             [w ** (1 * coset(r)) for r in reps],
             [w ** (2 * coset(r)) for r in reps],
             [fix(r) - 1 for r in reps]]

    def orthogonal(tbl):
        for i in range(4):
            for j in range(4):
                s = sum(sizes[k] * tbl[i][k] * np.conj(tbl[j][k]) for k in range(4))
                if abs(s - (12 if i == j else 0)) > 1e-9:
                    return False
        return True
    R["char_table_orthogonal_with_omega"] = orthogonal(table)
    # ω 가 x²+x+1=0 근 (비-rational, ℚ(ζ₃)=ℚ(√−3))
    R["omega_satisfies_cyclotomic"] = (abs(w ** 2 + w + 1) < 1e-12 and abs(w.imag) > 1e-9)

    # teeth: 3-cycle 지표를 rational(±1)로 강제 → orthogonality 붕괴(정수 문자표 불가)
    def forced_breaks(val):
        t = [row[:] for row in table]
        ci = [k for k in range(4) if sizes[k] == 4]           # 3-cycle 열
        for k in ci:
            t[1][k] = val
        return not orthogonal(t)
    R["teeth_rational_forcing_breaks"] = (forced_breaks(1) and forced_breaks(-1))

    # 6. 대조: S₄ 는 rational group(정수 문자표) — A₄ 와 정반대
    S4 = list(itertools.permutations(range(4)))
    rg_s4, _ = is_rational_group(S4)
    R["contrast_s4_rational_true"] = (rg_s4 is True)

    ok = all(R.values())
    if not quick:
        print("교대군 A₄ ζ₃-필연 문자표 관측 (★선검증·비-rational 군-Fourier 계보 닫힘, witness — seal 아님):",
              flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  문자표(class reps {reps}, sizes {sizes}):", flush=True)
        for i, row in enumerate(table):
            print(f"    χ_{i}: {[complex(np.round(v, 3)) if isinstance(v, complex) else v for v in row]}", flush=True)
        print("  ★핵심: ℚ* 에 order-3 원소 없음 → 3-cycle(order 3)의 비자명 1차원 지표는 rational 불가 → "
              "χ₁(3-cycle)=ω=ζ₃ **강제**. S₄ rational(정수 문자표)와 정반대·B₃/Q₈(ζ-free) 상보.", flush=True)
        print("  ★정직(선검증): 봉인 아님 — A₄ Fourier 는 ω₃ 대각 위상 z3_gate **신규 승인 module 필요**"
              "(사람게이트). 본 witness=결정근거 제공·신규 module 0·봉인 0·root 불변 sidecar.", flush=True)
    print(f"a4_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
