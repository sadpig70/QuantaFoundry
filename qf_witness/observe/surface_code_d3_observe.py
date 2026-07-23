#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""surface_code_d3_observe — TrackHE17 잔여: 회전 surface code d=3 [[9,1,3]] **물리** 부호
(stabilizer·distance·논리연산·merge=물리 논리측정) (관측, seal 아님).

[[lattice_surgery_observe]](TrackHE10 P5)는 lattice surgery 논리 CNOT 을 **논리 레벨**(2차원/큐빗
dense)로 관측했다. 본 witness 는 그 **물리 부호 기반**을 채운다: 회전 d=3 [[9,1,3]] surface code 를
stabilizer 형식으로 자체유도하고, **distance=3 을 전수 검증**하며, merge 를 물리 논리측정으로 관측한다.
(★기존 논리-CNOT 관측과 상보 — 물리 부호 층.)

관측 4축(전부 GF(2) symplectic — 정수 산술):
  A. **회전 surface code d=3 [[9,1,3]] 자체유도**: 3×3 data grid(9큐빗), 8 stabilizer(4 Z-plaq + 4 X-plaq
     경계 weight-2 + bulk weight-4) 전부 교환·GF(2) rank 8 → **논리큐빗 1**(9−8). 논리 X(가로 weight-3)·
     Z(세로 weight-3) — 전 stab 과 교환·서로 반교환(논리쌍).
  B. **★distance d=3 (전수)**: 최소 weight 논리 = min_{g∈stabilizer group} |L·g|. **2⁸ stabilizer 곱
     전수** → dX=dZ=**3**(정확 3, "≥3" 아님·silent cap 없음). weight≤2 논리 부재 확인.
  C. **merge(ZZ) = 물리 논리 ZZ 측정**: 두 패치 A(0-8)·B(9-17)에서 M=Z̄^A·Z̄^B 측정. M 은 전 물리
     stabilizer(A,B)와 **교환**·X̄^A 와 **반교환** → 측정이 X̄^A→X̄^A·X̄^B **join**(논리큐빗 2→1)·M 이
     새 stabilizer(joint). ⟹ merge=물리 논리 패리티 측정(split=역·XX-merge 쌍대). 논리 CNOT 은
     [[lattice_surgery_observe]] 참조(Horsman: M_ZZ+M_XX+ancilla).
  D. ★**부호 성질**: [[9,1,3]] = CSS(X/Z stabilizer 분리)·k=1·d=3. 논리 X̄·Z̄ 는 코드 경계-경계 string.
     Z̄·X̄ 반교환(단일 논리큐빗 대수). untwisted vs Shor [[9,1,3]](다른 배치) 구분(2D 위상 vs 연접).
  teeth: (i) weight-2 논리 부재 전수(distance 정확 3) (ii) 임의 data qubit 제거 시 논리 손상 안 됨
     (d=3 → 1 오류 정정) (iii) X/Z stabilizer 교환(CSS).

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - stabilizer 형식 **관측**(GF(2)) — 물리 인코더 유니터리 실봉인(Tier-0 dense 9큐빗)은 별도(qec_family
    stance: 측정 제외 유니터리만 봉인). 논리 게이트는 [[lattice_surgery_observe]] 측정 기반 관측.
  - distance=3 은 **전수**(2⁸) — d=5 는 min-weight 탐색(2²⁵ 전수 불가) 별도. 오류문턱/FT=하드웨어 out.
  - CSS·논리연산은 GF(2) 대수 사실 — 봉인 자산 아님.

사용: python -m qf_witness.observe.surface_code_d3_observe [--quick]
"""
from __future__ import annotations
import sys
import json


# ── GF(2) Pauli (x_mask, z_mask) ────────────────────────────────────────────
def P(xs, zs):
    return (sum(1 << q for q in xs), sum(1 << q for q in zs))


def symp(a, b):
    x1, z1 = a
    x2, z2 = b
    return (bin(x1 & z2).count("1") + bin(z1 & x2).count("1")) & 1


def weight(p):
    return bin(p[0] | p[1]).count("1")


def gf2_rank(vs):
    b = []
    for v in vs:
        for x in b:
            v = min(v, v ^ x)
        if v:
            b.append(v); b.sort(reverse=True)
    return len(b)


# 회전 surface code d=3 [[9,1,3]] (3×3 data grid, index 3r+c)
Z_STAB = [[0, 1], [1, 2, 4, 5], [3, 4, 6, 7], [7, 8]]
X_STAB = [[0, 3, 1, 4], [2, 5], [3, 6], [4, 7, 5, 8]]
STABS = [P([], z) for z in Z_STAB] + [P(x, []) for x in X_STAB]
Z_PAULIS = [P([], z) for z in Z_STAB]
X_PAULIS = [P(x, []) for x in X_STAB]
LX = P([0, 1, 2], [])
LZ = P([], [0, 3, 6])


def _stab_group(paulis):
    grp = [(0, 0)]
    for p in paulis:
        grp = grp + [(a[0] ^ p[0], a[1] ^ p[1]) for a in grp]
    return grp


def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "surface-code-d3/v1",
           "_note": ("회전 surface code d=3 [[9,1,3]] 물리 부호 (stabilizer·distance·merge) — "
                     "관측·seal 아님·module 0·root 불변. lattice_surgery_observe(논리 CNOT) 물리층 상보. "
                     "인코더 유니터리 실봉인은 별도(qec_family).")}

    # ── A. 코드 자체유도 ──────────────────────────────────────────────────
    R["A_8_stabilizers"] = (len(STABS) == 8)
    R["A_all_commute"] = all(symp(STABS[i], STABS[j]) == 0 for i in range(8) for j in range(8))
    R["A_rank_8_one_logical"] = (gf2_rank([(x << 9) | z for x, z in STABS]) == 8)
    R["A_logical_commute_stab"] = (all(symp(LX, s) == 0 for s in STABS)
                                   and all(symp(LZ, s) == 0 for s in STABS))
    R["A_logical_pair_anticommute"] = (symp(LX, LZ) == 1)
    out["code"] = {"name": "rotated surface code d=3 [[9,1,3]]", "n_data": 9, "k": 1, "d": 3,
                   "n_stab": 8, "Z_stab": Z_STAB, "X_stab": X_STAB,
                   "logical_X": [0, 1, 2], "logical_Z": [0, 3, 6]}

    # ── B. distance d=3 (전수 min-weight) ─────────────────────────────────
    grp = _stab_group(STABS)
    dX = min(weight((LX[0] ^ g[0], LX[1] ^ g[1])) for g in grp)
    dZ = min(weight((LZ[0] ^ g[0], LZ[1] ^ g[1])) for g in grp)
    R["B_distance_exactly_3"] = (dX == 3 and dZ == 3)
    R["B_no_weight_le2_logical"] = (min(dX, dZ) == 3)
    out["distance"] = {"dX": dX, "dZ": dZ, "distance": min(dX, dZ),
                       "method": "전수 2^8 stabilizer 곱 min-weight — 정확 3(silent cap 없음)"}

    # ── C. merge (ZZ) = 물리 논리 ZZ 측정 ─────────────────────────────────
    def shift(p, off):
        return (p[0] << off, p[1] << off)
    LZ_A, LZ_B, LX_A, LX_B = LZ, shift(LZ, 9), LX, shift(LX, 9)
    M_ZZ = (LZ_A[0] ^ LZ_B[0], LZ_A[1] ^ LZ_B[1])
    XX_join = (LX_A[0] ^ LX_B[0], LX_A[1] ^ LX_B[1])
    STABS_AB = STABS + [shift(s, 9) for s in STABS]
    R["C_MZZ_commute_all_phys_stab"] = all(symp(M_ZZ, s) == 0 for s in STABS_AB)
    R["C_MZZ_anticommute_XA"] = (symp(M_ZZ, LX_A) == 1)       # 측정이 X̄^A join
    R["C_MZZ_commute_XAXB"] = (symp(M_ZZ, XX_join) == 0)
    out["merge"] = {"operator": "M = Z̄^A · Z̄^B (물리 논리 ZZ 측정)",
                    "effect": "X̄^A → X̄^A·X̄^B (join, 논리큐빗 2→1)·M 새 stabilizer",
                    "logical_cnot_ref": "lattice_surgery_observe (Horsman M_ZZ+M_XX+ancilla)"}

    # ── D. 부호 성질 (CSS·논리 string) ────────────────────────────────────
    R["D_css_XZ_separated"] = (all(p[1] == 0 for p in X_PAULIS)      # X-stab: z=0
                               and all(p[0] == 0 for p in Z_PAULIS))  # Z-stab: x=0
    R["D_logical_X_weight3"] = (weight(LX) == 3)
    R["D_logical_Z_weight3"] = (weight(LZ) == 3)
    # 1-오류 정정: 임의 단일 data qubit X/Z 오류가 nontrivial syndrome(전 오류 검출)
    def syndrome(err):
        return tuple(symp(err, s) for s in STABS)
    single_errs = [P([q], []) for q in range(9)] + [P([], [q]) for q in range(9)]
    R["D_single_errors_detected"] = all(any(syndrome(e)) for e in single_errs
                                        if not (symp(e, LX) == 0 and symp(e, LZ) == 0
                                                and e in grp))
    out["code_properties"] = {"type": "CSS", "k": 1, "d": 3,
                              "logical_weights": {"X": weight(LX), "Z": weight(LZ)},
                              "note": "2D 위상 부호 — Shor [[9,1,3]](연접) 와 배치 상이"}

    # ── teeth ─────────────────────────────────────────────────────────────
    R["teeth_distance_exact"] = (dX == 3)
    R["teeth_css_commute"] = all(symp(xp, zp) == 0 for xp in X_PAULIS for zp in Z_PAULIS)
    R["teeth_merge_specificity"] = (symp(M_ZZ, LX_A) == 1 and symp(M_ZZ, XX_join) == 0)

    ok = bool(all(R.values()))
    out["checks"] = R
    out["scope_honesty"] = {
        "covered": ["회전 d=3 [[9,1,3]] stabilizer 자체유도", "distance=3 전수", "merge=물리 논리측정",
                    "CSS·논리 string·1-오류 검출"],
        "not_covered": ["인코더 유니터리 Tier-0 실봉인(qec_family 별도)", "d=5(min-weight 2^25 불가)",
                        "논리 CNOT(=lattice_surgery_observe)", "syndrome 디코딩·오류문턱"],
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "SURFACE-CODE-D3.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("회전 surface code d=3 [[9,1,3]] 물리 부호 관측 (stabilizer — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  ★[[9,1,3]] 8 stab·1 논리·distance {min(dX, dZ)}(전수)·CSS", flush=True)
        print(f"  ★merge = 물리 논리 ZZ 측정(X̄^A→X̄^A·X̄^B join)", flush=True)
        print("  ★정직: 물리 stabilizer 관측·인코더 실봉인/논리 CNOT 은 별도(참조)", flush=True)
        print("  → .pgf/proofs/SURFACE-CODE-D3.json", flush=True)
    print(f"surface_code_d3_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
