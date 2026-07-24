#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""twist_em_observe — TrackHE18 잔여: twist 코드 e↔m 교환 논리 게이트(twist_em_h16)의
**오라클-독립 witness** (관측).

봉인([[twist_em_seal]] → twist_em_h16)은 U=E·H(9)·E† 회로의 Tier-2 tableau. 본 witness 는 U 의
**대수 성질**을 독립 재검증한다(exact Pauli-conjugation 추적·부호 포함):

관측 4축:
  A. **코드 보존 자기동형**: U S_i U† ∈ +S군(14 stabilizer 전수·부호 포함) — U 는 [[16,2,2]]
     twist 코드의 자기동형.
  B. ★**e↔m 교환의 논리 사상**: U LZ1 U† ≡ LX1·U LX1 U† ≡ LZ1(mod S·부호 정확) — twist-braid 가
     유도하는 **e↔m anyon 교환의 대수 내용 = 논리 X↔Z 교환 = 논리 Hadamard₁**. 논리2 완전 불변
     (U LZ2 U†≡LZ2·U LX2 U†≡LX2).
  C. **involution**: U² = I(전 X_q·Z_q conjugation 전수) — e↔m 교환은 order 2.
  D. **논리 방향 식별의 견고성**: E Z₉ E† 의 target-군 분해가 LZ1 성분 포함(q9=논리1 방향)·
     E Z₁₅ E† 가 LZ2 성분 포함(q15=논리2 방향) — 인코더 표준형 환원의 행-스왑으로 논리 방향이
     마지막 큐빗이 아닐 수 있음(★교훈: 가정 대신 군 분해로 식별).

정직 경계(★관측·봉인과 분리):
  - U 는 **인코더-conjugation 실현** — twist defect 의 물리 이동(code deformation 측정 스케줄)이
    아니다. fault-tolerant braid 스케줄·defect 이동 중간 코드=범위밖.
  - "e↔m" 은 tableau 사상 수준의 대수 내용(논리 X↔Z 교환) — 애니온 동역학/통계 시뮬 아님.

사용: python -m qf_witness.observe.twist_em_observe [--quick]
"""
from __future__ import annotations
import sys
import json

from qf_witness.seal.twist_defect_seal import precheck, synthesize, N
from qf_witness.seal.twist_em_seal import conj_track, _g_phase, QL1


def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "twist-em-observe/v1",
           "_note": ("twist_em_h16(U=E·H(9)·E†) 오라클-독립 witness — 코드 자기동형·"
                     "e↔m 논리 사상(논리 H₁)·U²=I. 인코더-conjugation 실현(정직 경계).")}
    S, LZ1, LZ2 = precheck()
    enc = synthesize(S, LZ1, LZ2)
    enc_inv = []
    for g in reversed(enc):
        enc_inv += [g, g, g] if g[0] == "s" else [g]
    U = enc_inv + [("h", QL1)] + enc
    out["gates"] = len(U)

    def member_sign(t):
        basis = []
        fin = [[s[0], s[1], 0] for s in S]
        for i, r in enumerate(fin):
            v = (r[0] << N) | r[1]
            c = 1 << i
            for (bv, bc) in basis:
                top = bv.bit_length() - 1
                if (v >> top) & 1:
                    v ^= bv
                    c ^= bc
            if v:
                basis.append((v, c))
                basis.sort(key=lambda p: -p[0].bit_length())
        v = (t[0] << N) | t[1]
        c = 0
        for (bv, bc) in basis:
            top = bv.bit_length() - 1
            if (v >> top) & 1:
                v ^= bv
                c ^= bc
        if v:
            return None
        acc = [0, 0, 0]
        for i in range(14):
            if (c >> i) & 1:
                ph = (2 * acc[2] + 2 * fin[i][2]
                      + _g_phase(acc[0], acc[1], fin[i][0], fin[i][1])) % 4
                acc = [acc[0] ^ fin[i][0], acc[1] ^ fin[i][1], (ph // 2) % 2]
        return acc

    # A. 자기동형
    okS = True
    for s in S:
        r = conj_track(U, [s[0], s[1], 0])
        acc = member_sign((r[0], r[1]))
        if acc is None or (acc[2] ^ r[2]) != 0:
            okS = False
    R["A_stab_automorphism"] = okS

    # B. 논리 사상
    LZ1e = conj_track(enc, [0, 1 << QL1, 0])
    LX1e = conj_track(enc, [1 << QL1, 0, 0])
    LZ2e = conj_track(enc, [0, 1 << 15, 0])
    LX2e = conj_track(enc, [1 << 15, 0, 0])

    def maps(src, dst):
        r = conj_track(U, list(src))
        acc = member_sign((r[0] ^ dst[0], r[1] ^ dst[1]))
        if acc is None:
            return False
        ph = (2 * dst[2] + 2 * acc[2] + _g_phase(dst[0], dst[1], acc[0], acc[1])) % 4
        return r[2] == (ph // 2) % 2
    R["B_em_swap_L1"] = (maps(LZ1e, LX1e) and maps(LX1e, LZ1e))
    R["B_L2_invariant"] = (maps(LZ2e, LZ2e) and maps(LX2e, LX2e))
    # 비자명성: LZ1 ↛ LZ1 (진짜 교환인지)
    R["B_nontrivial"] = (not maps(LZ1e, LZ1e))

    # C. involution
    rng = range(0, N, 2) if quick else range(N)
    R["C_U2_identity"] = all(
        conj_track(U + U, [1 << q, 0, 0]) == [1 << q, 0, 0]
        and conj_track(U + U, [0, 1 << q, 0]) == [0, 1 << q, 0] for q in rng)

    # D. 논리 방향 식별
    def decompose_uses(p):
        basis = []
        tg = [*S, LZ1, LZ2]
        for i, t in enumerate(tg):
            v = (t[0] << N) | t[1]
            c = 1 << i
            for (bv, bc) in basis:
                top = bv.bit_length() - 1
                if (v >> top) & 1:
                    v ^= bv
                    c ^= bc
            if v:
                basis.append((v, c))
                basis.sort(key=lambda pp: -pp[0].bit_length())
        v = (p[0] << N) | p[1]
        c = 0
        for (bv, bc) in basis:
            top = bv.bit_length() - 1
            if (v >> top) & 1:
                v ^= bv
                c ^= bc
        return None if v else [i for i in range(16) if (c >> i) & 1]
    u9 = decompose_uses(tuple(conj_track(enc, [0, 1 << 9, 0])[:2]))
    u15 = decompose_uses(tuple(conj_track(enc, [0, 1 << 15, 0])[:2]))
    R["D_q9_is_L1"] = (u9 is not None and 14 in u9 and 15 not in u9)
    R["D_q15_is_L2"] = (u15 is not None and 15 in u15 and 14 not in u15)

    # teeth
    R["teeth_swap_not_identity"] = R["B_nontrivial"]
    R["teeth_automorphism_sign"] = R["A_stab_automorphism"]

    ok = bool(all(R.values()))
    out["checks"] = R
    out["logical_action"] = {"L1": "LZ1 ↔ LX1 (논리 Hadamard₁ = e↔m 교환의 대수 내용)",
                             "L2": "불변", "order": "U² = I"}
    out["scope_honesty"] = {
        "realization": "인코더-conjugation(U=E·H·E†) — defect 물리 이동/측정 스케줄 아님",
        "em_meaning": "tableau 사상 수준(논리 X↔Z 교환) — 애니온 동역학 아님",
        "lesson": "논리 방향은 가정 대신 군 분해로 식별(합성 행-스왑이 순서를 바꿈)",
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "TWIST-EM-OBSERVE.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("twist e↔m 논리 게이트 witness (exact conjugation):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  ★U=E·H(9)·E†: 자기동형·LZ1↔LX1(논리 H₁)·논리2 불변·U²=I", flush=True)
        print("  → .pgf/proofs/TWIST-EM-OBSERVE.json", flush=True)
    print(f"twist_em_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
