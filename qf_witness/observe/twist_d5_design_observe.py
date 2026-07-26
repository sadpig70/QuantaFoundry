#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""twist_d5_design_observe — ★twist-defect surface code **d=5 설계 요건 확정 + 잘못된 접근
2종 원리적 배제** (관측, seal 아님).

★**목표 대비 정직 보고**: 착수 목표는 **d=5 twist 코드 실봉인**(root 갱신)이었다. 도달한 것은
**설계 단계까지**이며 **봉인은 미달성**이다(신규 module 0·root 불변). 대신 아래 두 정리를
**전수 검증**으로 확정해 잘못된 접근 2종을 원리적으로 배제하고, d=5 가 요구하는 조건을 확정했다.
[[twist_defect_observe]]([[16,2,2]] d=2) 의 후속 설계 층.

관측 5축(전 산술 GF(2) symplectic 전수):
  A. **일반 회전 surface code 빌더 + 거리 인증기**(재사용 자산):
     bulk 체커보드 (d−1)² + 4경계 weight-2 — **경계 타입은 자체유도**(경계쌍은 인접 plaquette 와
     정확히 1 큐빗을 공유하므로 **동일 타입이어야 교환** ⟹ 타입 확정) →
     **[[25,1,5]]**(비교환 0·rank 24·k=1·**최소 논리 weight 정확 5** + witness) ·
     **[[9,1,3]]** 교차확인. ★함정 기록: 우측 경계는 인접 plaquette 열 **c=d−2** 기준 —
     c=d−1 로 잡으면 3쌍 비교환(실제 초기 오류·검증기가 즉시 포착).
  B. ★**region-flip 무해 정리(전수 16/16)**: F={(r,c): r≤R, c≥C} 의 X↔Z flip 은 **항상**
     전-교환·rank 24·**k=1** ⟹ region flip 은 **Hadamard 켤레**이므로 **twist 를 만들 수 없다**
     (도메인 벽의 양 끝이 코드 경계에 닿아 bulk twist 부재).
  C. ★★**병합 상한 정리(전수 4416/4416)**: 서로 **교환**하는 두 생성원 S_i,S_j 를 곱으로 병합
     (둘 제거·곱 추가)하면 k=2 가 되지만 **S_i 가 비자명 논리 연산자**가 된다
     (symp(S_i, S_iS_j)=symp(S_i,S_j)=0 이고 S_i ∉ 새 군) — **반례 0** ·
     그런 논리의 **최대 weight = 4** 실측 ⟹ **전 후보 d ≤ 4 < 5**.
     ⟹ ★**d=5 twist 코드는 flip+병합으로 원리적으로 불가**.
  D. ★**기존 [[16,2,2]] 독립 재확인**: 봉인된 twist_defect16 의 코드에 대해 본 인증기로
     **k=2·최소 논리 weight 정확 2**·**pentagon 홀수 Y(=1)** 재도출 — 인증기 자체의 교차검증.
  E. ★**d=5 설계 요건 명문화**(A–D 에서 유도): ① cut 길이 ≥ 5 · 격자 ≥ 6행
     ② cut 을 따라 **mixed 교대 사슬**(각 측 2 큐빗은 동일 타입 T_L≠T_R — 인접 1-큐빗 겹침
     제약에서 유도) ③ **cut 끝에서 mixed 와 정상 plaquette 가 정확히 1 큐빗에서 타입 불일치
     ⟹ 반교환** → 병합 시 **홀수-Y pentagon** 발생, 그리고 이때 병합된 생성원은 **곱과 반교환**
     하므로 논리가 되지 않는다 — **C 의 상한을 피하는 유일한 경로**.

정직 경계(★관측·seal 아님·root 불변·신규 module 0):
  - ★**봉인 미달성**을 명시한다. "d=5 코드를 만들었다"는 주장이 아니다.
  - B·C 는 **본 관측이 정의한 후보 공간**(회전 격자 d=5 · 우상 region flip · 교환쌍 1회 병합)
    안에서의 전수 배제다 — 일반 twist 코드 불가능성 주장이 **아니다**.
  - E 는 A–D 에서 **유도한 요건**이며, 그 요건을 만족하는 격자의 실구성은 **미완**(다음 작업).

사용: python -m qf_witness.observe.twist_d5_design_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import itertools


# ══════════════════════════════════════════════════════════════════════════
# GF(2) symplectic 도구
# ══════════════════════════════════════════════════════════════════════════
def to_pauli(terms):
    x = z = 0
    for (q, t) in terms:
        if t in 'XY':
            x |= 1 << q
        if t in 'ZY':
            z |= 1 << q
    return (x, z)


def parse(s):
    return to_pauli([(q, c) for q, c in enumerate(s) if c != 'I'])


def symp(a, b):
    return (bin(a[0] & b[1]).count("1") + bin(a[1] & b[0]).count("1")) & 1


def wt(p):
    return bin(p[0] | p[1]).count("1")


def yc(p):
    return bin(p[0] & p[1]).count("1")


def rank_of(vs):
    b = []
    for v in vs:
        for x in b:
            v = min(v, v ^ x)
        if v:
            b.append(v)
            b.sort(reverse=True)
    return len(b)


def span_basis(n, P):
    sb = []
    for p in P:
        v = (p[0] << n) | p[1]
        for x in sb:
            v = min(v, v ^ x)
        if v:
            sb.append(v)
            sb.sort(reverse=True)
    return sb


def in_span(n, sb, p):
    v = (p[0] << n) | p[1]
    for x in sb:
        top = x.bit_length() - 1
        if (v >> top) & 1:
            v ^= x
    return v == 0


def pstr(n, p):
    out = []
    for i in range(n):
        xb, zb = (p[0] >> i) & 1, (p[1] >> i) & 1
        out.append('Y' if xb and zb else ('X' if xb else ('Z' if zb else 'I')))
    return ''.join(out)


def min_logical(n, P, maxw):
    """weight ≤ maxw 비자명 논리 전수 탐색 → (최소 weight, witness) 또는 (None, None)."""
    sb = span_basis(n, P)
    for w in range(1, maxw + 1):
        for pos in itertools.combinations(range(n), w):
            for types in itertools.product('XYZ', repeat=w):
                p = to_pauli(list(zip(pos, types)))
                if all(symp(p, s) == 0 for s in P) and not in_span(n, sb, p):
                    return w, pstr(n, p)
    return None, None


# ══════════════════════════════════════════════════════════════════════════
# A. 회전 surface code 빌더 (경계 타입 자체유도)
# ══════════════════════════════════════════════════════════════════════════
def build_rotated(d):
    """[[d²,1,d]] 회전 surface code. 경계쌍 타입 = 1-큐빗 겹침 plaquette 의 타입(교환 제약)."""
    def q(r, c):
        return r * d + c

    def ptype(r, c):
        return 'X' if (r + c) % 2 == 0 else 'Z'
    S = []
    for r in range(d - 1):
        for c in range(d - 1):
            t = ptype(r, c)
            S.append((f"P{r}{c}", [(q(r, c), t), (q(r, c + 1), t),
                                   (q(r + 1, c), t), (q(r + 1, c + 1), t)]))
    for c in range(1, d - 1, 2):                    # 상단: 인접 plaquette (0, c−1)
        t = ptype(0, c - 1)
        S.append((f"T{c}", [(q(0, c), t), (q(0, c + 1), t)]))
    for c in range(0, d - 1, 2):                    # 하단: 인접 (d−2, c−1)
        t = ptype(d - 2, c - 1)
        S.append((f"B{c}", [(q(d - 1, c), t), (q(d - 1, c + 1), t)]))
    for r in range(0, d - 1, 2):                    # 좌: 인접 (r−1, 0)
        t = ptype(r - 1, 0)
        S.append((f"L{r}", [(q(r, 0), t), (q(r + 1, 0), t)]))
    for r in range(1, d - 1, 2):                    # 우: 인접 (r−1, d−2)  ★c=d−2 (함정)
        t = ptype(r - 1, d - 2)
        S.append((f"R{r}", [(q(r, d - 1), t), (q(r + 1, d - 1), t)]))
    return d * d, S


def flip_region(d, S, R, C):
    F = {r * d + c for r in range(R + 1) for c in range(C, d)}
    out = []
    for (nm, terms) in S:
        out.append((nm, [(qq, ('Z' if t == 'X' else 'X') if qq in F else t)
                         for (qq, t) in terms]))
    return out


# 봉인된 twist_defect16 코드(독립 재확인용 — 값 복사, 오라클 무접촉)
TW16 = [
    "ZZIIZZIIIIIIIIII", "IIIIXXIIXXIIIIII", "IIIIIIIIZZIIZZII", "IIXXIIXXIIIIIIII",
    "IIIIIIZZIIZZIIII", "IIIIIIIIIIXXIIXX", "XIIIXIIIIIIIIIII", "IIIZIIIZIIIIIIII",
    "IIIIIIIIXIIIXIII", "IIIIIIIIIIIIIIZZ", "IIIIIIIIIIIIXXII", "IZXIIIIIIIIIIIII",
    "IXZIIXZIIIIIIIII", "IIIIIZXIIYXIIXII",
]


# ══════════════════════════════════════════════════════════════════════════
def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "twist-d5-design/v1",
           "_note": ("twist-defect d=5 설계 요건 확정 + 잘못된 접근 2종 전수 배제. "
                     "★봉인 미달성(관측·module 0·root 불변) — 정직 보고.")}

    # ── A. 빌더 + 거리 인증기 ───────────────────────────────────────────
    n3, S3 = build_rotated(3)
    P3 = [to_pauli(t) for (_, t) in S3]
    R["A_d3_commute"] = all(symp(P3[i], P3[j]) == 0
                            for i in range(len(P3)) for j in range(i + 1, len(P3)))
    R["A_d3_k1"] = (n3 - rank_of([(p[0] << n3) | p[1] for p in P3]) == 1)
    w3, wit3 = min_logical(n3, P3, 3)
    R["A_d3_distance3"] = (w3 == 3)

    n5, S5 = build_rotated(5)
    P5 = [to_pauli(t) for (_, t) in S5]
    R["A_d5_stab24"] = (len(S5) == 24)
    R["A_d5_commute"] = all(symp(P5[i], P5[j]) == 0
                            for i in range(len(P5)) for j in range(i + 1, len(P5)))
    R["A_d5_rank24_k1"] = (n5 - rank_of([(p[0] << n5) | p[1] for p in P5]) == 1)
    w5, wit5 = min_logical(n5, P5, 5)
    R["A_d5_distance5_exact"] = (w5 == 5)
    R["A_d5_no_weight4_logical"] = (w5 is not None and w5 > 4)
    # ★함정 재현: 우측 경계를 c=d−1 로 잡으면 비교환 발생
    S5w = []
    for (nm, terms) in S5:
        if nm.startswith("R"):
            r = int(nm[1:])
            t = 'X' if (r - 1 + 5 - 1) % 2 == 0 else 'Z'
            S5w.append((nm, [(qq, t) for (qq, _) in terms]))
        else:
            S5w.append((nm, terms))
    P5w = [to_pauli(t) for (_, t) in S5w]
    nbad = sum(1 for i in range(len(P5w)) for j in range(i + 1, len(P5w))
               if symp(P5w[i], P5w[j]))
    R["A_teeth_wrong_right_boundary"] = (nbad == 3)
    out["builder"] = {
        "rule": "bulk 체커보드 X iff (r+c) even · 경계쌍 타입 = 1-큐빗 겹침 plaquette 타입(교환 제약)",
        "verified": {"[[9,1,3]]": "k=1·d=3", "[[25,1,5]]": f"k=1·d=5 witness={wit5}"},
        "pitfall": "우측 경계 인접 plaquette 열은 c=d−2 (c=d−1 로 잡으면 비교환 3쌍)",
    }

    # ── B. region-flip 무해 정리 ────────────────────────────────────────
    flip_cases, flip_ok = 0, True
    for Rr in range(4):
        for Cc in range(1, 5):
            Sf = flip_region(5, S5, Rr, Cc)
            Pf = [to_pauli(t) for (_, t) in Sf]
            flip_cases += 1
            comm = all(symp(Pf[i], Pf[j]) == 0
                       for i in range(len(Pf)) for j in range(i + 1, len(Pf)))
            k = n5 - rank_of([(p[0] << n5) | p[1] for p in Pf])
            if not (comm and k == 1):
                flip_ok = False
    R["B_flip_cases_16"] = (flip_cases == 16)
    R["B_flip_always_k1_commuting"] = flip_ok
    out["theorem_region_flip"] = {
        "statement": "F={(r,c): r≤R, c≥C} 의 X↔Z flip 은 항상 전-교환·k=1",
        "evidence": "16/16 전수",
        "reason": "region flip = Hadamard 켤레 — 도메인 벽 양 끝이 코드 경계에 닿아 bulk twist 부재",
        "consequence": "★region flip 만으로는 twist 를 만들 수 없다",
    }

    # ── C. 병합 상한 정리 ───────────────────────────────────────────────
    cand, viol, worst = 0, 0, 0
    regions = [(Rr, Cc) for Rr in range(4) for Cc in range(1, 5)]
    if quick:
        regions = regions[:4]
    for (Rr, Cc) in regions:
        Sf = flip_region(5, S5, Rr, Cc)
        Pf = [to_pauli(t) for (_, t) in Sf]
        for i, j in itertools.combinations(range(len(Pf)), 2):
            prod = (Pf[i][0] ^ Pf[j][0], Pf[i][1] ^ Pf[j][1])
            newP = [Pf[t] for t in range(len(Pf)) if t not in (i, j)] + [prod]
            if n5 - rank_of([(p[0] << n5) | p[1] for p in newP]) != 2:
                continue
            cand += 1
            sb = span_basis(n5, newP)
            is_log = (all(symp(Pf[i], s) == 0 for s in newP)
                      and not in_span(n5, sb, Pf[i]))
            if not is_log:
                viol += 1
            else:
                worst = max(worst, wt(Pf[i]))
    R["C_candidates"] = (cand == (4416 if not quick else 1104))
    R["C_no_counterexample"] = (viol == 0)
    R["C_max_logical_weight_4"] = (worst == 4)
    R["C_d5_impossible_by_merge"] = (viol == 0 and worst < 5)
    out["theorem_merge_bound"] = {
        "statement": ("교환하는 S_i,S_j 를 곱으로 병합(둘 제거·곱 추가)하면 k=2 이나 "
                      "S_i 가 비자명 논리가 된다 ⟹ d ≤ wt(S_i)"),
        "proof_sketch": "symp(S_i, S_iS_j) = symp(S_i,S_j) = 0 이고 S_i ∉ 새 안정군",
        "evidence": f"후보 {cand} 전수 · 반례 0 · 그런 논리 최대 weight = {worst}",
        "consequence": "★d=5 는 flip+병합으로 원리적 불가 — 진짜 dislocation 필요",
    }

    # ── D. 기존 [[16,2,2]] 독립 재확인 ──────────────────────────────────
    n16 = 16
    P16 = [parse(s) for s in TW16]
    R["D_tw16_commute"] = all(symp(P16[i], P16[j]) == 0
                              for i in range(len(P16)) for j in range(i + 1, len(P16)))
    R["D_tw16_k2"] = (n16 - rank_of([(p[0] << n16) | p[1] for p in P16]) == 2)
    w16, wit16 = min_logical(n16, P16, 3)
    R["D_tw16_distance2_exact"] = (w16 == 2)
    pent = P16[13]
    R["D_tw16_pentagon_odd_Y"] = (wt(pent) == 5 and yc(pent) == 1)
    out["cross_check_tw16"] = {
        "code": "봉인 twist_defect16 의 안정군(값 복사·오라클 무접촉)",
        "reproduced": f"k=2 · d=2 정확(witness={wit16}) · pentagon weight 5·Y 1",
        "role": "본 거리 인증기의 독립 교차검증 + 정리와의 정합(twist 분리 2 ⟹ d=2)",
    }

    # ── E. d=5 설계 요건 ────────────────────────────────────────────────
    R["E_requirements_recorded"] = True
    out["d5_requirements"] = {
        "1_cut_length": "cut(dislocation) 길이 ≥ 5 · 격자 ≥ 6행 — twist 쌍 분리거리가 d 를 제한",
        "2_mixed_chain": ("cut 을 따라 mixed 교대 사슬: 각 측 2 큐빗은 **동일** 타입이고 "
                          "T_L ≠ T_R (인접 plaquette 와의 1-큐빗 겹침 교환 제약에서 유도)"),
        "3_twist_endpoint": ("cut 끝에서 mixed 와 정상 plaquette 가 **정확히 1 큐빗에서 타입 불일치 "
                             "⟹ 반교환** → 병합 시 홀수-Y pentagon 발생. 이때 병합된 생성원은 "
                             "곱과 **반교환**하므로 논리가 되지 않는다 — C 의 상한을 피하는 유일 경로"),
        "4_status": "★위 요건을 만족하는 격자의 실구성 = 미완(다음 작업)",
    }

    # ── teeth ───────────────────────────────────────────────────────────
    R["teeth_wrong_boundary_detected"] = R["A_teeth_wrong_right_boundary"]
    R["teeth_flip_cannot_twist"] = R["B_flip_always_k1_commuting"]
    R["teeth_merge_bounded"] = R["C_d5_impossible_by_merge"]

    ok = bool(all(R.values()))
    out["checks"] = R
    out["scope_honesty"] = {
        "goal_vs_delivered": ("★착수 목표 = d=5 twist 코드 **실봉인**(root 갱신). "
                              "도달 = **설계 단계**(요건 확정 + 잘못된 접근 2종 전수 배제). "
                              "**봉인 미달성** — 신규 module 0 · root 불변."),
        "delivered": ("회전 surface code 빌더 + 거리 인증기(재사용) · [[25,1,5]]/[[9,1,3]] 검증 · "
                      "region-flip 무해 정리(16/16) · 병합 상한 정리(4416/4416) · "
                      "[[16,2,2]] 독립 재확인 · d=5 요건 명문화"),
        "not_claimed": ("d=5 코드 구성 · 일반 twist 코드 불가능성(B·C 는 정의된 후보 공간 내 배제) · "
                        "봉인 자산 변경"),
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "TWIST-D5-DESIGN.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("twist d=5 설계 요건 + 접근 배제 (전수 — seal 아님·★봉인 미달성):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  ★[[25,1,5]] 기저 확정(d=5 witness {wit5})·[[9,1,3]] 교차확인", flush=True)
        print("  ★region-flip 무해 정리 16/16 · ★병합 상한 정리 4416/4416(최대 weight 4)",
              flush=True)
        print("  ⟹ d=5 는 flip+병합 원리적 불가 — twist 쌍 ≥5 분리한 진짜 dislocation 필요",
              flush=True)
        print("  ★정직: 봉인 미달성(module 0·root 불변) — 요건 명문화까지", flush=True)
        print("  → .pgf/proofs/TWIST-D5-DESIGN.json", flush=True)
    print(f"twist_d5_design_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
