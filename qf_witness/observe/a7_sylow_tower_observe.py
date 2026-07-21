#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""a7_sylow_tower_observe — TrackHE16 P6: Schur cover Sylow-2 계보 — ★Q₃₂ tower 반증
(closed-negative) + 실제 tower(A₆→A₇ 정체) (관측, seal 아님). 전 과정 순열/정수 정확산술.

[[a5_schur_cocycle_observe]](v14/v15, 2.A₅ Sylow-2=Q₈) + [[a6_schur_cocycle_observe]](v15 P4,
2.A₆=SL(2,9) Sylow-2=Q₁₆)의 계보 확장. report16 agent 가 "Sylow-2 tower **Q₈→Q₁₆→Q₃₂**
(2.A₅→2.A₆→2.A₇)"를 제안했다. 본 witness 는 선검증으로 그 tower 를 **반증**한다(§4′o).

★핵심 관측 — Q₃₂ tower **불가**(closed-negative, agent 제안 반증):
  Aₙ Sylow-2 위수 = |Aₙ| 의 2-part(자체 유도, 순열군 위수):
    A₅: |A₅|=60=2²·15   → Sylow-2 위수 **4**  (V₄=ℤ₂², involution 3)
    A₆: |A₆|=360=2³·45  → Sylow-2 위수 **8**  (D₄, involution 5·위수4 2)
    A₇: |A₇|=2520=2³·315 → Sylow-2 위수 **8** (D₄, ★A₆ 와 **동일** — 2-part 정체)
    A₈: |A₈|=20160=2⁶·315 → Sylow-2 위수 **64** (다음 도약)
  ⟹ Schur cover Sylow-2: 2.A₅=**Q₈**(8)·2.A₆=**Q₁₆**(16)·2.A₇=**Q₁₆**(16, ★A₇ Sylow-2=A₆ 이므로
  spin lift 동형). **Q₃₂(32) 는 A₇ 에서 나오지 않는다** — tower 는 A₆ 에서 Q₁₆ 으로 정체하고
  A₇ 도 동일. 위수 도약은 A₅(4)→A₆(8)→A₈(64) 에서만.

관측 계층 (전부 exact):
  1. Aₙ(n=5,6,7) 순열군 자체구성(짝순열)·Sylow-2 위수·원소위수 다중집합 → 구조 판정
     (V₄/D₄; generalized quaternion 여부 = involution 유일성).
  2. |Aₙ| 2-part 자체 유도(n=5..8): 4,8,8,64 — ★A₆=A₇ 정체.
  3. ★2.A₅=Q₈·2.A₆=Q₁₆ 재확인(v14/v15 모듈 직접 호출) — 계보 복리.
  4. ★2.A₇ Sylow-2 = Q₁₆ 논증: A₇ Sylow-2 ≅ A₆ Sylow-2 = D₄ → spin lift(2-cohomology
     obstruction 동일) ≅ 2.A₆ Sylow-2 = Q₁₆ (구조 논증·관측). Q₃₂ 부재.
  teeth: (i) A₆≠A₇ 라면(반례) tower 도약 — 실제 동일 확인 (ii) A₈ 도약 실측(64≠8).

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - closed-negative(Q₃₂ 부재)는 **위수 자체 유도**로 exact — A₇ Sylow-2 위수 8 ≠ 32.
  - ★2.A₇ Sylow-2=Q₁₆ 은 **구조 논증**(A₇ Sylow-2=A₆=D₄ → lift 동형): 2.A₇ 명시 순열/행렬 구성은
    미착수(A₆≅PSL(2,9) 같은 예외 동형 부재로 dense 구성 무거움) — "논증 관측"으로 정직 표기.
  - 3-torsion(3.A₇·ζ₃)·H²(A₇) full 계산은 미착수(ζ₃ 승인 게이트·규모). 2-part Sylow 만 주장.

사용: python -m qf_witness.observe.a7_sylow_tower_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import itertools
from collections import Counter


def parity(p):
    seen = [False] * len(p); s = 0
    for i in range(len(p)):
        if not seen[i]:
            j, c = i, 0
            while not seen[j]:
                seen[j] = True; j = p[j]; c += 1
            s += c - 1
    return s % 2


def alt_group(n):
    return [p for p in itertools.permutations(range(n)) if parity(p) == 0]


def pm(a, b):
    return tuple(a[b[i]] for i in range(len(a)))


def order(p, e):
    k, x = 1, p
    while x != e:
        x = pm(x, p); k += 1
    return k


def two_part(m):
    tp = 1
    while m % 2 == 0:
        m //= 2; tp *= 2
    return tp


def sylow2_orders(A, n):
    """Sylow-2 부분군(위수 = |A|_2)의 원소 위수 다중집합 (결정론 첫 발견)."""
    e = tuple(range(n))
    tp = two_part(len(A))
    invol = [p for p in A if p != e and pm(p, p) == e]
    for a, b in itertools.product(invol[:50], repeat=2):
        S, fr = {e}, [a, b]
        while fr and len(S) <= tp:
            x = fr.pop()
            if x in S:
                continue
            S.add(x)
            for g in (a, b):
                fr.append(pm(x, g))
        if len(S) == tp:
            return tp, sorted(order(x, e) for x in S)
    return tp, None


def classify_2group(orders, size):
    """위수 size 2-군을 원소위수 다중집합으로 판별(소형)."""
    if orders is None:
        return f"unknown(order {size})"
    c = Counter(orders)
    table = {
        (4, (1, 2, 2, 2)): "V4(Z2^2)",
        (4, (1, 2, 4, 4)): "Z4",
        (8, (1, 2, 2, 2, 2, 2, 2, 2)): "Z2^3",
        (8, (1, 2, 2, 2, 2, 2, 4, 4)): "D4",
        (8, (1, 2, 4, 4, 4, 4, 4, 4)): "Q8",
        (16, (1, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8, 8, 8, 8)): "Q16",
    }
    return table.get((size, tuple(orders)), f"order_multiset={tuple(orders)}")


def is_generalized_quaternion(orders, size):
    if orders is None or len(orders) != size:
        return False
    c = Counter(orders)
    return c.get(size, 0) == 0 and c.get(2, 0) == 1 and c.get(1, 0) == 1


def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "a7-sylow-tower/v1",
           "_note": ("Schur cover Sylow-2 계보 — ★Q₃₂ tower 반증(closed-negative, agent 제안) + "
                     "실제 tower(A₆→A₇ 정체). 관측·seal 아님·신규 module 0·root 불변. "
                     "2.A₇ Sylow-2=Q₁₆ 은 구조 논증(명시 구성 미착수).")}

    # 1. Aₙ Sylow-2 구조 자체유도
    ns = (5, 6) if quick else (5, 6, 7)
    syl = {}
    for n in ns:
        A = alt_group(n)
        tp, orders = sylow2_orders(A, n)
        struct = classify_2group(orders, tp)
        syl[n] = {"order": tp, "element_orders": dict(Counter(orders)) if orders else None,
                  "structure": struct}
    out["An_sylow2"] = {str(n): syl[n] for n in ns}
    R["A5_sylow2_V4_order4"] = (syl[5]["order"] == 4 and syl[5]["structure"] == "V4(Z2^2)")
    R["A6_sylow2_D4_order8"] = (syl[6]["order"] == 8 and syl[6]["structure"] == "D4")
    if not quick:
        R["A7_sylow2_D4_order8"] = (syl[7]["order"] == 8 and syl[7]["structure"] == "D4")
        # ★A₆ = A₇ Sylow-2 (정체)
        R["A6_eq_A7_sylow2"] = (syl[6]["order"] == syl[7]["order"]
                                and syl[6]["structure"] == syl[7]["structure"])

    # 2. |Aₙ| 2-part tower (자체 유도)
    import math
    two_parts = {n: two_part(math.factorial(n) // 2) for n in (5, 6, 7, 8)}
    out["An_2part"] = two_parts
    R["2part_tower_4_8_8_64"] = (two_parts == {5: 4, 6: 8, 7: 8, 8: 64})
    R["A6_A7_2part_stall"] = (two_parts[6] == two_parts[7] == 8)   # ★정체
    R["A8_jumps"] = (two_parts[8] == 64)

    # 3. ★2.A₅=Q₈·2.A₆=Q₁₆ 재확인 (v14/v15 모듈 직접 호출)
    from qf_witness.observe.a5_schur_cocycle_observe import build_E as build_E5, order_of as ord5, IDE as IDE5
    from qf_witness.observe.a5_schur_cocycle_observe import mmul as mmul5
    E5 = build_E5()
    o4 = [M for M in E5 if ord5(M) == 4]
    s8 = None
    for A in o4:
        for B in o4:
            S, fr = {IDE5}, [A, B]
            while fr and len(S) <= 8:
                x = fr.pop()
                if x in S:
                    continue
                S.add(x)
                for g in (A, B):
                    fr.append(mmul5(x, g))
            if len(S) == 8:
                s8 = sorted(ord5(x) for x in S); break
        if s8:
            break
    R["2A5_sylow2_Q8"] = is_generalized_quaternion(s8, 8)
    out["cover_sylow2"] = {"2.A5": {"order": 8, "struct": "Q8",
                                    "gen_quaternion": R["2A5_sylow2_Q8"]}}
    if not quick:
        from qf_witness.observe.a6_schur_cocycle_observe import (
            build_SL29, order_E as ordE6, IDE9, mmul as mmul6, sylow2_orders as syl6)
        E6 = build_SL29()
        s16 = syl6(E6, 16)
        R["2A6_sylow2_Q16"] = is_generalized_quaternion(s16, 16)
        out["cover_sylow2"]["2.A6"] = {"order": 16, "struct": "Q16",
                                       "gen_quaternion": R["2A6_sylow2_Q16"]}

    # 4. ★2.A₇ Sylow-2 = Q₁₆ 논증 + Q₃₂ 반증
    out["closed_negative_Q32"] = {
        "claim_refuted": "Sylow-2 tower Q₈→Q₁₆→Q₃₂ (2.A₅→2.A₆→2.A₇)",
        "reason": ("A₆ Sylow-2 = A₇ Sylow-2 = D₄(위수 8) — |Aₙ|_2 정체(둘 다 2³). ⟹ spin lift "
                   "2.A₇ Sylow-2 ≅ 2.A₆ Sylow-2 = Q₁₆(위수 16), Q₃₂(32) 아님. 위수 도약은 "
                   "A₅(4)→A₆(8)→A₈(64) 에서만."),
        "actual_tower": "Q₈(2.A₅) → Q₁₆(2.A₆) → Q₁₆(2.A₇, 정체) → [A₈ 에서 다음 도약]",
        "scope": "2.A₇ Sylow-2=Q₁₆ 은 구조 논증(A₇ Sylow-2=A₆=D₄ lift)·명시 구성 미착수",
    }
    if not quick:
        R["Q32_refuted"] = (two_parts[7] == 8 and syl[7]["structure"] == "D4")

    # teeth
    R["teeth_A8_jumps_not_stall"] = (two_parts[8] != two_parts[7])
    R["teeth_A5_A6_do_grow"] = (two_parts[5] < two_parts[6])   # 정체 아닌 구간은 증가

    ok = bool(all(R.values()))
    out["checks"] = R
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "A7-SYLOW-TOWER.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("Schur cover Sylow-2 계보 관측 (Q₃₂ tower 반증 — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  ★Aₙ Sylow-2: A₅={syl[5]['structure']}(4)·A₆={syl[6]['structure']}(8)·"
              f"A₇={syl[7]['structure']}(8) — A₆=A₇ 정체", flush=True)
        print(f"  ★|Aₙ|_2 tower: {two_parts} — A₆→A₇ 정체·A₈ 도약", flush=True)
        print(f"  ★Schur cover: 2.A₅=Q₈ → 2.A₆=Q₁₆ → 2.A₇=Q₁₆(정체, Q₃₂ 반증)", flush=True)
        print("  → .pgf/proofs/A7-SYLOW-TOWER.json", flush=True)
    print(f"a7_sylow_tower_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
