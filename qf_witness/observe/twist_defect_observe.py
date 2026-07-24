#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""twist_defect_observe — TrackHE18 잔여: twist-defect surface code [[16,2,2]] **코드 성질 완전
검증**(관측 — 봉인 twist_defect16 의 오라클-독립 witness).

봉인([[twist_defect_seal]] → registry/modules/twist_defect16)은 |0_L0_L⟩ prep 회로의 Tier-2 tableau.
본 witness 는 **코드 자체의 수학 성질**을 독립 검증한다(GF(2) symplectic 전수):

관측 5축:
  A. **코드 게이트**: 14 stabilizer 전부 교환·rank 14 → **k=2**·전 큐빗 X/Z 양-타입 커버.
  B. ★**pentagon twist stabilizer**: Z₅X₆Y₉X₁₀X₁₃ — **5-body·Y 정확 1개**(홀수 Y 는 CSS 불가능 —
     stabilizer 쌍 병합으로는 원리적 불가(교환쌍=짝수 겹침=짝수 Y): 격자 재배치(dislocation)에서만) +
     mixed 사슬(Z₁X₂ 도미노·X₁Z₂X₅Z₆)로 dislocation line 실현. **non-CSS**(X/Z 분리 불가) 확인.
  C. ★**distance=2 정확**(전수): 논리 15 클래스 × stab 군 2¹⁴ 코셋 최소 weight = 2 (weight-1 논리
     부재 전수·d=2 달성 witness 명시).
  D. ★**e↔m 전환**: 15 논리 클래스 중 **9 가 mixed-필수**(코셋 전수에서 순수-X·순수-Z 대표 부재)
     — dislocation line 을 가로지르는 string 이 X↔Z 타입을 바꿔야만 닫힘 = twist 의 e↔m 교환 실증.
  E. **기준 대비 논리 +1**: 동일 4×4 격자의 정상 회전 surface code(체커보드 9면+경계 6, 자체 구성·
     교환·rank 15) → **k=1** vs twist 코드 k=2 — **twist 쌍(경계 진입점+bulk pentagon)이 논리큐빗
     +1**(stabilizer rank 결손) 실증.

정직 경계(★관측·봉인과 분리):
  - 봉인 자산 = |0_L0_L⟩ prep Clifford 회로의 정준 tableau(exact) — 본 witness 는 코드 성질 검증.
  - **d=2 = detection-only**(소형·twist-경계 근접) — d≥3 twist 코드·twist-braid 논리 게이트·측정
    스케줄은 대형 격자/별도.
  - e↔m 은 string-타입 강제(코셋 전수)로 실증 — 애니온 동역학 시뮬 아님.

사용: python -m qf_witness.observe.twist_defect_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import itertools

N = 16

STABS_STR = [
    "ZZIIZZIIIIIIIIII",
    "IIIIXXIIXXIIIIII",
    "IIIIIIIIZZIIZZII",
    "IIXXIIXXIIIIIIII",
    "IIIIIIZZIIZZIIII",
    "IIIIIIIIIIXXIIXX",
    "XIIIXIIIIIIIIIII",
    "IIIZIIIZIIIIIIII",
    "IIIIIIIIXIIIXIII",
    "IIIIIIIIIIIIIIZZ",
    "IIIIIIIIIIIIXXII",
    "IZXIIIIIIIIIIIII",
    "IXZIIXZIIIIIIIII",
    "IIIIIZXIIYXIIXII",
]


def parse(s):
    x = z = 0
    for q, c in enumerate(s):
        if c in "XY":
            x |= (1 << q)
        if c in "ZY":
            z |= (1 << q)
    return (x, z)


def symp(a, b):
    return (bin(a[0] & b[1]).count("1") + bin(a[1] & b[0]).count("1")) & 1


def weight(p):
    return bin(p[0] | p[1]).count("1")


def ycount(p):
    return bin(p[0] & p[1]).count("1")


def pack(p):
    return (p[0] << N) | p[1]


def unpack(v):
    return (v >> N, v & ((1 << N) - 1))


def gf2_basis(vs):
    b = []
    for v in vs:
        for x in b:
            v = min(v, v ^ x)
        if v:
            b.append(v)
            b.sort(reverse=True)
    return b


def logicals(stabs):
    def Jswap(v):
        a, b = unpack(v)
        return (b << N) | a
    checks = [Jswap(pack(s)) for s in stabs]
    piv = {}
    for c in checks:
        r = c
        while r:
            p = r.bit_length() - 1
            if p in piv:
                r ^= piv[p]
            else:
                piv[p] = r
                break
    cols = sorted(piv, reverse=True)
    for p in cols:
        rr = piv[p]
        for p2 in cols:
            if p2 > p and ((piv[p2] >> p) & 1):
                piv[p2] ^= rr
    pivset = set(piv)
    ker = []
    for f in range(2 * N):
        if f in pivset:
            continue
        v = 1 << f
        for p, rr in piv.items():
            if (rr >> f) & 1:
                v |= (1 << p)
        ker.append(v)
    sb = gf2_basis([pack(s) for s in stabs])
    logis = []
    ext = list(sb)
    for v in ker:
        w = v
        for b in ext:
            w = min(w, w ^ b)
        if w:
            logis.append(v)
            ext.append(w)
            ext.sort(reverse=True)
    return logis, sb


def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "twist-defect-observe/v1",
           "_note": ("twist-defect [[16,2,2]] 코드 성질 완전 검증 — 봉인 twist_defect16 의 "
                     "오라클-독립 witness. d=2 전수·e↔m mixed-필수 9/15·pentagon 5-body Y1·"
                     "기준 [[16,1,·]] 대비 논리 +1.")}
    S = [parse(s) for s in STABS_STR]

    # A. 게이트
    R["A_all_commute"] = all(symp(a, b) == 0 for a in S for b in S)
    sb = gf2_basis([pack(s) for s in S])
    R["A_rank14_k2"] = (len(sb) == 14)
    R["A_covers"] = all(any((p[0] >> q) & 1 for p in S) and any((p[1] >> q) & 1 for p in S)
                        for q in range(N))

    # B. pentagon·non-CSS
    pent = S[13]
    R["B_pentagon_5body_Y1"] = (weight(pent) == 5 and ycount(pent) == 1)
    R["B_mixed_chain"] = (ycount(S[11]) == 0 and weight(S[11]) == 2
                          and weight(S[12]) == 4)     # Z1X2 도미노·4-body mixed
    # non-CSS: 순수-X 성분/순수-Z 성분으로 분리 불가(=stab basis 에 mixed 필수):
    css_split = True
    for v in sb:
        p = unpack(v)
        if p[0] != 0 and p[1] != 0:
            css_split = False    # 어떤 기저원소는 mixed — 필요조건
    # 진짜 판정: X-부분/Z-부분 사영이 군을 보존하는가 → stab 군의 X-성분만 모은 것이 부분군인지
    xparts = gf2_basis([p[0] for p in S if p[0]])
    zparts = gf2_basis([p[1] for p in S if p[1]])
    # CSS 라면 rank(x)+rank(z)=14 인 순수 생성계 존재. mixed 필수 판정: 순수 원소 dim 확인
    grp = [0]
    for b in sb:
        grp = grp + [g ^ b for g in grp]
    pure_cnt = sum(1 for g in grp if g and (unpack(g)[0] == 0 or unpack(g)[1] == 0))
    pure_basis = gf2_basis([g for g in grp if g and (unpack(g)[0] == 0 or unpack(g)[1] == 0)])
    R["B_nonCSS"] = (len(pure_basis) < 14)      # 순수 원소만으론 stab 군 생성 불가
    out["pentagon"] = {"stab": STABS_STR[13], "body": 5, "Y": 1,
                       "nonCSS_pure_rank": len(pure_basis)}

    # C. distance 전수
    logis, _ = logicals(S)
    R["C_4_logicals"] = (len(logis) == 4)
    dmin = 99
    mixed_only = 0
    for mask in range(1, 16):
        v = 0
        for i in range(4):
            if (mask >> i) & 1:
                v ^= logis[i]
        wmin = 99
        pure = False
        for g in grp:
            p = unpack(v ^ g)
            wmin = min(wmin, weight(p))
            if p[0] == 0 or p[1] == 0:
                pure = True
        dmin = min(dmin, wmin)
        if not pure:
            mixed_only += 1
    R["C_distance_2_exact"] = (dmin == 2)

    # D. e↔m
    R["D_mixed_required_9_15"] = (mixed_only == 9)
    out["code"] = {"n": N, "k": 2, "d": dmin, "mixed_required_classes": mixed_only,
                   "verdict": "twist 를 지나는 string 이 X↔Z 전환 필수 = e↔m 실증"}

    # E. 기준 [[16,1,·]] (정상 4×4 회전) — 자체 구성: 체커보드 9면 + 경계 6
    def Pm(xs, zs):
        return (sum(1 << q for q in xs), sum(1 << q for q in zs))
    base = []
    for r in range(3):
        for c in range(3):
            sup = [4 * r + c, 4 * r + c + 1, 4 * r + c + 4, 4 * r + c + 5]
            base.append(Pm(sup, []) if (r + c) % 2 else Pm([], sup))
    # 경계 6 (기계 확인 배치): 상 X{0,1},X{2,3} 하 X{13,14}? — 교환 만족 조합을 결정론 소전수로
    slots = [([0, 1], "X"), ([2, 3], "X"), ([12, 13], "X"), ([14, 15], "X"),
             ([13, 14], "X"), ([0, 4], "Z"), ([4, 8], "Z"), ([8, 12], "Z"),
             ([3, 7], "Z"), ([7, 11], "Z"), ([11, 15], "Z")]
    found_base = None
    for combo in itertools.combinations(slots, 6):
        cand = base + [Pm(s, []) if t == "X" else Pm([], s) for s, t in combo]
        if any(symp(a, b) for a, b in itertools.combinations(cand, 2)):
            continue
        if len(gf2_basis([pack(p) for p in cand])) == 15:
            found_base = cand
            break
    R["E_baseline_k1"] = (found_base is not None)
    R["E_twist_adds_logical"] = (found_base is not None and len(sb) == 14)
    out["baseline"] = {"found": found_base is not None,
                      "verdict": "정상 4×4 k=1 vs twist k=2 — twist 가 논리 +1(rank 결손)"}

    # teeth
    R["teeth_pentagon_odd_Y_nonmergeable"] = (ycount(pent) % 2 == 1)   # 병합 불가(짝수-Y 정리) 산물
    R["teeth_d2_not_d1"] = (dmin == 2)
    R["teeth_em_nontrivial"] = (0 < mixed_only < 15)

    ok = bool(all(R.values()))
    out["checks"] = R
    out["scope_honesty"] = {
        "sealed_asset": "twist_defect16 (Tier-2 tableau, registry/modules) — 본 witness 는 성질 검증",
        "d2": "detection-only(소형·twist-경계 근접) — d≥3·twist-braid 게이트·측정 스케줄=대형/별도",
        "em": "string-타입 강제(코셋 전수) 실증 — 애니온 동역학 아님",
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "TWIST-DEFECT-OBSERVE.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("twist-defect [[16,2,2]] 코드 성질 (GF(2) 전수 — witness):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  ★pentagon Z5X6Y9X10X13(5-body·Y1)·non-CSS·d=2 전수·e↔m 9/15·twist 논리+1", flush=True)
        print("  → .pgf/proofs/TWIST-DEFECT-OBSERVE.json", flush=True)
    print(f"twist_defect_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
