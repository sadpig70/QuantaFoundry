# -*- coding: utf-8 -*-
"""
arith_family_c7x.py — Stage 6 W6.1 ArithFamilyExtend-c7x

W2.4가 봉인한 c7x(7-control Toffoli)의 직접 결실. 7-control이 *실제로 필요한* distinct-prime
modular multiplier(N∈(64,128], nq=8)를 Tier-0 EXACT 봉인한다. P1(arith_family.py, c6x→N<64)의
자연스러운 다음 칸 — 같은 엔진(genskills.modmul_synth, c7x upstream 진화)·같은 검증 골격을 *재사용*.

핵심 발견(정직): discover propose는 c7x가 mod39/51을 unlock한다 명시했으나 실측 반증 —
nq-qubit MCT의 max control = nq-1 = work bits. c7x는 work bits≥7 ⟺ N>64일 때만 필요.
  - mod39/51/55/57 (N<64, nq=7): maxc=6 → c6x로 이미 충분(c7x 무관).
  - c7x 진짜 unlock(N∈(64,128], nq=8): mod91=7×13·mod77=7×11·mod85=5×17 (maxc=7).

정직성 경계(arith_family.py 계승):
 - 엔진 *진화*: genskills _MCT_MODULE[7]=c7x, cap>7(c8x 부재) + self-seal 재스탬프(catalog INTACT).
   기존 cmul(≤c6x) 산출 byte 불변(EngineRegression).
 - 생성≠검증: 오라클(app_assemble) 통과로만 SEALED. plan=봉인 MCT(toffoli..c7x), MatrixGate 0.
 - 행동관찰(BehavioralObserve)=illustrative only(§8.4) — 봉인 증거 아님.
 - 비파괴 성장: 앱만 가산(모듈 50 불변), 기존 봉인/frozen 23키/fingerprint byte-identical.

사용:  python scripts/arith_family_c7x.py
"""
from __future__ import annotations

import os
import sys
import json
import math

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import arith_family as af        # noqa: E402  (synth/verify/regression 함수 *재사용*)
import genskills as gs           # noqa: E402  (진화된 엔진 — c7x upstream)

OUT = os.path.join(ROOT, ".pgf", "arith")

# c7x가 *실제로 필요한* distinct-prime 타겟 (N∈(64,128], nq=8, maxc=7) — a=2 coprime
TARGETS = [(2, 91), (2, 77), (2, 85)]   # 7×13, 7×11, 5×17


def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 74)
    print("W6.1 ArithFamilyExtend-c7x — c7x 활용 distinct-prime(N>64) modular multiplier")
    print("정직성: 생성≠검증(오라클). 엔진 c7x 진화+self-seal 재스탬프. 앱만 가산(모듈 불변).")
    print("=" * 74)

    # 0. c7x 봉인 전제 확인 (이미 W2.4에서 봉인됨 — 신규 모듈봉인 0)
    c7x_sealed = os.path.exists(os.path.join(af.MODREG, "c7x.sealed.json"))
    print(f"[Prereq] c7x 봉인 존재(W2.4): {c7x_sealed}  (신규 모듈봉인 0 — 앱만 forge)")
    assert c7x_sealed, "c7x.sealed.json 부재 — W2.4 봉인 선행 필요"

    # 1. SynthDistinctPrime (진화 엔진 gs.gen_modmul, c7x 포함)
    synth = af.synth_distinct_prime(TARGETS)
    for s in synth:
        print(f"[Synth] {s['id']:14} ({'×'.join(map(str,s['factors']))}) sealed={s['sealed']} "
              f"tier={s['tier']} {s['gates']}gates ctrl={s['control_dist']} u={str(s['u_hash'])[:14]}")
    used_c7x = [s for s in synth if 7 in (s["control_dist"] or {})]
    print(f"   → c7x(7-control)를 실제 사용한 타겟: {[s['id'] for s in used_c7x]} "
          f"({len(used_c7x)}/{len(synth)})")

    # 2. EngineRegression (genskills 진화 후에도 기존 cmul ≤c6x u_hash 불변)
    reg = af.engine_regression()
    reg_ok = sum(1 for c in reg if c.get("matches_registry"))
    print(f"[EngineRegression] 진화엔진으로 기존 cmul(≤c6x) 재현 u_hash==registry: {reg_ok}/{len(reg)} "
          f"(golden 순열 불변)")

    # 3. IndependentArithVerify (제2 검증축 — 봉인 비신뢰, 독립 산술순열)
    indep = [af.independent_arith_verify(a, N) for a, N in TARGETS]
    indep_ok = sum(1 for c in indep if c["matches_sealed"])
    print(f"[IndependentArithVerify] 신규 cmul 독립순열 u_hash==sealed: {indep_ok}/{len(indep)}")
    for c in indep:
        print(f"   {c['id']:14} indep_u={c['independent_u_hash']} match={c['matches_sealed']}")

    # 4. BehavioralObserve (illustrative only §8.4 — ×2 orbit period == ord_N(2))
    beh = [af.behavioral_observe(a, N) for a, N in TARGETS]
    for b in beh:
        print(f"[BehavioralObserve] {b['id']}: ×2 orbit period={b['observed_period']} "
              f"==ord_N(2)={b['ord_N_a']} ({b['matches']}) [illustrative only]")

    # 5. ShorScopeHonest (full Shor 규모 → Tier 정직표기)
    shor_scope = []
    for a, N in TARGETS:
        r = beh[[t[1] for t in TARGETS].index(N)]["ord_N_a"]
        t_need = 2 * math.ceil(math.log2(r)) if r > 1 else 1
        work = math.ceil(math.log2(N))
        total = t_need + work
        shor_scope.append({"N": N, "period": r, "counting_t": t_need, "work": work,
                           "total_qubits": total, "tier0_exact_feasible": total <= 12,
                           "honest_tier": "Tier-0 EXACT" if total <= 12 else "Tier-1 STRUCTURAL"})
    print("[ShorScopeHonest] full Shor 조립 규모:")
    for s in shor_scope:
        print(f"   N={s['N']}: period r={s['period']} → ~{s['total_qubits']}q "
              f"({s['counting_t']}counting+{s['work']}work) → {s['honest_tier']}")

    report = {
        "phase": "W6.1 ArithFamilyExtend-c7x",
        "honesty": "c7x(W2.4 sealed) consumed by evolved genskills.gen_modmul (c7x upstream + "
                   "self-seal re-stamp INTACT); generation != verification (oracle app_assemble seals); "
                   "behavioral observe illustrative only (§8.4); plan=sealed MCT incl c7x, no MatrixGate; "
                   "apps additive (modules unchanged, frozen keys/fingerprint byte-identical).",
        "correction": "discover propose claimed c7x unlocks mod39/51 — empirically false (N<64 needs only "
                      "c6x). c7x genuinely required iff N>64 (work bits>=7). Targets corrected to N in (64,128].",
        "targets": [f"cmul{a}_mod{N}" for a, N in TARGETS],
        "synth_distinct_prime": synth,
        "c7x_used_by": [s["id"] for s in used_c7x],
        "engine_regression": {"matches": reg_ok, "total": len(reg), "detail": reg},
        "independent_arith_verify": indep,
        "behavioral_observe": beh,
        "shor_scope_honest": shor_scope,
    }
    synth_ok = all(s["sealed"] and s["tier"] == 0 for s in synth)
    c7x_ok = len(used_c7x) == len(synth)         # 전 타겟이 c7x 사용(진짜 unlock 입증)
    all_ok = (synth_ok and c7x_ok and reg_ok == len(reg)
              and indep_ok == len(indep) and all(b["matches"] for b in beh))
    report["all_ok"] = bool(all_ok)
    json.dump(report, open(os.path.join(OUT, "ARITH-FAMILY-C7X-REPORT.json"), "w",
                           encoding="utf-8"), ensure_ascii=False, indent=2)
    print("-" * 74)
    print(f"all_ok={all_ok}  →  .pgf/arith/ARITH-FAMILY-C7X-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
