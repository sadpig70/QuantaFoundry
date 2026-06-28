# -*- coding: utf-8 -*-
"""rho_validation.py — Stage 4 W4.2 [EXT]: poisoned 합의 *구성* → ρ-discount 붕괴 검증.

리뷰 잔여: ρ-discount(corpus 상관 할인)는 *설계*됐으나 표준게이트 co-error 가 4라운드까지 0 →
**실가동 미입증**(과장 위험). 본 모듈은 co-error 를 결정론적으로 *구성*한다: little-endian QFT 등
*틀린*(sealed≠) 유니터리를 2소스가 합의하게 만들고, 설계된 메커니즘(independence_unit 병합 +
ρ-discount)이 그 joint vote 를 <2 independent 로 붕괴시키는지 검증한다.

정직 구분(과장 금지):
  - self-contained: *구성된* poisoned 합의를 메커니즘이 올바로 붕괴 = 메커니즘 실가동(본 모듈 완결).
  - [EXT] relay: 약모델 패널이 *자연발생적으로* co-error 를 내는지(4라운드 0)는 실런타임 수급 필요.

비파괴: 분석/검증 전용. registry/sealed/frozen 불변. **frozen consensus_keys.json 재생성 금지**
(인메모리 establish_truth 만 호출). `.pgf/consensus/`·`docs/`·패널패키지 가산.
소비 자산(사용만): consensus(Source/establish_truth/effective_independent_count) · second_oracle(INDEP/perm_gate).

사용:  python scripts/rho_validation.py
"""
from __future__ import annotations
import os, sys, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, ".pgf", "keyfree"))
import second_oracle as so            # noqa: E402  INDEP/perm_gate 사용만
import consensus as C                 # noqa: E402  Source/establish_truth 사용만

MODREG = os.path.join(ROOT, "registry", "modules")
OUT = os.path.join(ROOT, ".pgf", "consensus")
PKG = os.path.join(ROOT, "_workspace", "crossmodel", "p3d_round5_poison")
DOC = os.path.join(ROOT, "docs", "TRUST-MODEL-VALIDATION-REPORT.md")


def _bitrev_perm(n):
    N = 1 << n
    return so.perm_gate([int(format(i, f"0{n}b")[::-1], 2) for i in range(N)])


def poisoned_units():
    """*틀린*(sealed≠) 유니터리를 결정론 구성 — co-error 의 재료. 정답=big-endian qft3."""
    qft3 = so.qft_n(3)
    R = _bitrev_perm(3)
    le = R @ qft3 @ R                       # little-endian QFT (비트순서 반대 = 틀린 유니터리)
    conj = qft3.conj()                      # conjugate-stated-standard
    phase = qft3 @ np.diag([1, 1, 1, 1, 1, 1, 1, np.exp(1j * 0.3)])   # corpus-sparse phase
    return {"little_endian_qft3": C.uhash(le), "conjugate_qft3": C.uhash(conj),
            "phase_perturbed_qft3": C.uhash(phase)}, C.uhash(qft3)


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(PKG, exist_ok=True)
    os.makedirs(os.path.dirname(DOC), exist_ok=True)
    print("=" * 86)
    print("PoisonedLineagePanel (W4.2 [EXT]) — co-error 구성 → ρ-discount 붕괴 검증")
    print("=" * 86)

    poison, correct_uh = poisoned_units()
    le = poison["little_endian_qft3"]
    sealed_qft3 = None
    p = os.path.join(MODREG, "qft3.sealed.json")
    if os.path.exists(p):
        sealed_qft3 = json.load(open(p, encoding="utf-8"))["u_hash"]

    # poisoned 가 정답과 다른지(틀린 유니터리) + 정답이 sealed 와 일치하는지 확인
    poison_is_wrong = all(h != correct_uh for h in poison.values())
    correct_matches_sealed = (sealed_qft3 is None) or (correct_uh == sealed_qft3)
    print(f"\n구성: 정답 qft3 u={correct_uh[:14]} (sealed 일치={correct_matches_sealed}) · "
          f"poisoned {len(poison)}종 모두 정답≠ {poison_is_wrong}")

    checks = []

    # 1) LineageMergeTeeth: 같은 independence_unit 2소스 poisoned 합의 → DIVERGENT (독립단위 병합 w=1)
    s_same = [C.Source("rt1", "model", "weightsA", le), C.Source("rt2", "model", "weightsA", le)]
    r1 = C.establish_truth("qft3_poison", s_same, N=2, rho=0.0)
    checks.append({"name": "lineage_merge", "status": r1.status, "dist": r1.distribution,
                   "pass": r1.status == "DIVERGENT",
                   "detail": "같은 weightsA 2소스 → independence_unit 병합으로 1 vote<2 → DIVERGENT"})

    # 2) RhoDiscountTeeth: distinct-unit 2소스 poisoned + ρ>0 → CORPUS_CORRELATED escalate
    s_dist = [C.Source("rt1", "model", "weightsA", le), C.Source("rt3", "model", "weightsB", le)]
    r2 = C.establish_truth("qft3_poison", s_dist, N=2, rho=0.6)
    checks.append({"name": "rho_discount", "status": r2.status, "grade": r2.grade,
                   "pass": r2.status == "INSUFFICIENT" and r2.grade == "CORPUS_CORRELATED",
                   "detail": f"distinct unit 2소스 poisoned + ρ=0.6 → N_eff="
                             f"{C.effective_independent_count(2, 0.6):.2f}<2 → CORPUS_CORRELATED escalate"})

    # 3) NoDiscountBaseline: 같은 poisoned, ρ=0 → MULTIMODEL ESTABLISHED (ρ 없으면 co-error 통과 = 위험 실증)
    r3 = C.establish_truth("qft3_poison", s_dist, N=2, rho=0.0)
    checks.append({"name": "rho0_lets_coerror_pass", "status": r3.status, "grade": r3.grade,
                   "pass": r3.status == "ESTABLISHED",
                   "detail": "ρ=0 이면 distinct-unit poisoned 합의가 ESTABLISHED — ρ-discount 의 존재가치 실증"})

    # 4) ControlEstablished: 정답 2독립소스 ρ=0 → ESTABLISHED (메커니즘이 정답까지 막지 않음)
    s_ok = [C.Source("a", "model", "wA", correct_uh), C.Source("b", "model", "wB", correct_uh)]
    r4 = C.establish_truth("qft3", s_ok, N=2, rho=0.0)
    checks.append({"name": "control_established", "status": r4.status, "grade": r4.grade,
                   "pass": r4.status == "ESTABLISHED",
                   "detail": "정답 2독립소스 → ESTABLISHED (false-positive 아님)"})

    # 5) ρ sweep — N_eff 곡선
    sweep = {f"rho={r}": round(C.effective_independent_count(2, r), 3) for r in (0.0, 0.3, 0.6, 1.0)}

    for c in checks:
        print(f"  {'✓' if c['pass'] else '✗'} {c['name']:24} → {c['status']}"
              f"{'/' + c['grade'] if c.get('grade') else ''}")
        print(f"      {c['detail']}")
    print(f"\n  N_eff(2소스) sweep: {sweep}  (ρ→1 이면 2소스가 1 유효독립으로 붕괴)")

    mech_ok = all(c["pass"] for c in checks) and poison_is_wrong and correct_matches_sealed
    verdict = ("MECHANISM LIVE — 구성된 co-error 를 lineage-merge + ρ-discount 가 정확히 붕괴; ρ=0 "
               "대조로 discount 존재가치 실증; 정답은 통과(false-positive 0). "
               "자연발생 co-error(약모델 패널)는 [EXT] relay 대기." if mech_ok else
               "MECHANISM CHECK FAILED — 점검 필요")

    out = {"_schema": "rho-validation-v1", "mechanism_live": mech_ok, "verdict": verdict,
           "correct_u_hash": correct_uh, "correct_matches_sealed": correct_matches_sealed,
           "poisoned_units": poison, "poison_all_wrong": poison_is_wrong,
           "checks": checks, "n_eff_sweep": sweep,
           "_note": "self-contained: 구성된 poisoned 합의를 메커니즘이 붕괴=실가동. [EXT]: 자연발생 "
                    "co-error 수급은 약모델 패널 relay. frozen consensus_keys 재생성 없음(인메모리)."}
    json.dump(out, open(os.path.join(OUT, "RHO-VALIDATION.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    # 패널 패키지(self-contained 부분) + 보고서
    panel = {"_schema": "poison-panel-v1", "round": "p3d_round5_poison",
             "instruction": "약모델/poisoned 런타임에 표준회로(qft3 등)를 의뢰하되, little-endian 해석·"
                            "conjugate-state·corpus-sparse phase 를 유도하는 모호 프롬프트로 co-error 유발 시도. "
                            "2소스가 *같은 틀린* u_hash 로 수렴하면 lineage/corpus 상관 실측.",
             "poisoned_reference_uhashes": poison, "correct_uhash": correct_uh,
             "scoring": "수거 후 rho_validation 으로 establish_truth(ρ 추정=corpus_discount) → "
                        "joint vote 가 <2 independent 로 붕괴하는지 실데이터 확인.",
             "relay": "정욱님 약모델 패널 배포→수거→responses/ 적재. EXT 의존."}
    json.dump(panel, open(os.path.join(PKG, "PANEL-SPEC.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    os.makedirs(os.path.join(PKG, "responses"), exist_ok=True)

    doc = [
        "# Trust-Model Validation Report (Stage 4 W4.2)\n",
        "> ρ-discount 실가동 정직 종결. 분석/검증 전용 비파괴.\n",
        "## 판정\n", f"**{verdict}**\n",
        "## self-contained 검증 (메커니즘)\n",
        "| 검증 | 결과 | 의미 |", "|---|---|---|"]
    for c in checks:
        doc.append(f"| {c['name']} | {c['status']}{'/' + c['grade'] if c.get('grade') else ''} "
                   f"{'✓' if c['pass'] else '✗'} | {c['detail']} |")
    doc += [
        f"\nN_eff(2소스) sweep: `{sweep}`\n",
        "## 정직 구분\n",
        "- **메커니즘 실가동**: 구성된 poisoned 합의(little-endian QFT 등)를 independence_unit 병합 + "
        "ρ-discount 가 정확히 붕괴(DIVERGENT/CORPUS_CORRELATED). ρ=0 대조에서 co-error 가 ESTABLISHED 되는 "
        "위험을 실증해 discount 의 존재가치를 확인. 정답 2독립소스는 통과(false-positive 0).",
        "- **[EXT] 자연발생 co-error**: 표준게이트 4라운드 co-error 0(frontier 모델 견고). 약모델/poisoned "
        "패널이 *자연발생적으로* 같은 틀린 답에 수렴하는지는 실런타임 수급 필요 → `_workspace/crossmodel/"
        "p3d_round5_poison/` 패키지 relay.\n",
        "## 최종 라벨\n",
        "ρ-discount = **설계+메커니즘 실가동(구성된 co-error 붕괴 입증)**. 자연발생 co-error 통계는 EXT "
        "수급 시 확정. 과장(ρ 만능) 제거, 미가동 오해(설계만)도 제거 — 정직 종결.\n"]
    open(DOC, "w", encoding="utf-8", newline="\n").write("\n".join(doc))

    print("\n" + "-" * 86)
    print(f"판정: {'MECHANISM LIVE ✅' if mech_ok else 'CHECK FAILED ✗'}")
    print(f"→ .pgf/consensus/RHO-VALIDATION.json · docs/TRUST-MODEL-VALIDATION-REPORT.md · "
          f"패널패키지 _workspace/crossmodel/p3d_round5_poison/ [EXT]")
    return 0 if mech_ok else 1


if __name__ == "__main__":
    sys.exit(main())
