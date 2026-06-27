# -*- coding: utf-8 -*-
"""
bounty_adjudicate.py — P3d ReproBounty AutoAdjudicate (cross-model adversarial)

외부 *독립 AI 런타임*(P2b 와 동일한 6 distinct-weights)을 반증 주체로 삼아, 봉인/게이트/오라클을
적대적으로 깨라고 의뢰한 제출물을 **결정론적으로 자동 판정**한다. 핵심 원칙:

  - 모델의 *주장*은 절대 신뢰하지 않는다. 제출된 후보 산출물을 **우리 오라클이 재실행**해서
    판정한다(적대적 모델조차 거짓말 불가 — 오라클이 검산).
  - 비파괴: 모든 실행은 temp store. registry/specs/frozen 무변경. consensus/gate/verify_seal 사용만.
  - 정직 라벨: 외부 *AI* 반증 통과 ≠ 공개 *인간* bounty 통과. 등급 = "cross-model adversarial".

3 표적(P3a CAUGHT 방어선을 외부 시선으로 재시험):
  T1_hollow        // honest-분해 우회(=matrixgate 문서화 공백) — 내부정합·의미공허 봉인
  T2_independence  // B4 독립위장 — co-error 를 MULTIMODEL ESTABLISHED 로 속이기
  T3_convention    // convention/GT 함정 — 의미 틀린 행렬을 ESTABLISHED 진리로

판정 코드:
  BREAK     // 방어선이 뚫림(공격자 승) — 최우선 보고
  HELD      // 방어선이 공격을 거부(정직한 음성 = §7 신뢰자본)
  DOC_GAP   // 이미 문서화된 경계 재현(matrixgate 등) — 새 버그 아님
  NEW_GAP   // 플래그 안 된 봉인 통과 — 신규 의심, 인간 검토 escalate
  INVALID   // 제출물 malformed

결정론은 신성불가침: 봉인 byte-identical·정답키 불변. 본 스크립트는 *판정만* 한다(봉인 안 함).
"""
from __future__ import annotations

import os
import re
import sys
import json
import glob
import argparse
import tempfile
import subprocess

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, ORACLE)
sys.path.insert(0, os.path.join(ROOT, ".pgf", "keyfree"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import verify_seal as vs        # noqa: E402  (hash_unitary 사용만)
import consensus as cc          # noqa: E402  (Source/establish_truth/uhash 사용만)
import gated_panel as gp        # noqa: E402  (dispatch_policy/gated_seal 사용만)

PKG = os.path.join(ROOT, "_workspace", "crossmodel", "p3d_bounty")
SUBS = os.path.join(PKG, "submissions")
OUT = os.path.join(ROOT, ".pgf", "bounty")

# honest-분해 위반 정적 시그니처(T1): bloq 가 primitive 분해 대신 답을 직접 주입한 흔적.
_DISHONEST_PAT = [
    r"MatrixGate", r"cirq_gate_to_bloq", r"from_unitary", r"unitary\s*=",
    r"np\.array\(\s*\[\s*\[", r"\.reshape\(", r"GenericGate", r"as_matrix",
]


# ── 제출물 → 행렬 ───────────────────────────────────────────────────
def _mat(entry):
    re_ = np.array(entry["golden_real"], dtype=float)
    im = np.array(entry.get("golden_imag", np.zeros_like(re_)), dtype=float)
    return re_ + 1j * im


# ── T1: HollowSeal (honest-분해 우회) ───────────────────────────────
def adj_t1_hollow(sub, exec_specs=False):
    """spec(bloq+golden)이 봉인되나? bloq 가 정직 분해인가? 기본=정적 스캔, --exec-specs=실봉인."""
    spec = sub.get("spec_text", "")
    m = re.search(r"id=bloq\n(.*?)```", spec, re.S)
    bloq_src = m.group(1) if m else ""
    flags = [p for p in _DISHONEST_PAT if re.search(p, bloq_src)]
    if not exec_specs:
        verdict = "DOC_GAP" if flags else "NEEDS_EXEC"
        return {"target": "T1_hollow", "verdict": verdict, "dishonest_flags": flags,
                "note": ("정적: 정직분해 위반 시그니처 검출(=matrixgate 문서화 공백 재현)" if flags
                         else "정적: 시그니처 미검출 — --exec-specs 로 sandbox 봉인 필요(신규 의심)")}
    # exec: temp store 봉인(spec_guard import 화이트리스트가 1차 샌드박스). registry 무오염.
    tmp = tempfile.mkdtemp(prefix="bounty_t1_")
    name = sub.get("id", "atk_hollow")
    p = os.path.join(tmp, f"{name}.pg")
    open(p, "w", encoding="utf-8", newline="\n").write(spec)
    r = subprocess.run([sys.executable, os.path.join(ORACLE, "verify_seal.py"), p, "--out", tmp],
                       capture_output=True, text=True, cwd=ORACLE)
    sealed = os.path.exists(os.path.join(tmp, f"{name}.sealed.json"))
    if not sealed:
        verdict = "HELD"      # 봉인 거부 = 공격 실패
    elif flags:
        verdict = "DOC_GAP"   # 봉인됐고 부정직 시그니처 = 알려진 공백 재현
    else:
        verdict = "NEW_GAP"   # 봉인됐는데 시그니처 없음 = 신규 hollow-seal 의심 → 인간검토
    last = (r.stdout + r.stderr).strip().splitlines()[-1:] or [""]
    return {"target": "T1_hollow", "verdict": verdict, "sealed": sealed,
            "dishonest_flags": flags, "oracle_tail": last[0][:120]}


# ── T2: IndependenceForgery (B4 위장) ───────────────────────────────
def adj_t2_independence(sub):
    """주장한 sources 로 gated_seal 재실행. co-error(같은 u_hash)를 SEAL 시키면 BREAK."""
    intent = sub.get("intent", "atk_t2")
    srcs = [cc.Source(s["sid"], s["klass"], s["unit"], s["u_hash"]) for s in sub["sources"]]
    panel = gp.dispatch_policy("new_family")           # 고위험: distinct-weights ≥2 강제
    dec = gp.gated_seal(intent, panel, srcs)
    uhash_set = {s.u_hash for s in srcs}
    real_units = {cc.independence_unit(s) for s in srcs}
    is_co_error = len(uhash_set) == 1                  # 모두 같은(틀린) 답 = 진짜 co-error
    if dec.decision == "SEAL" and is_co_error:
        # 게이트가 단일 진리에 SEAL — 단위가 ≥2 로 집계됐다는 뜻 = 라벨 위조로 독립 가장 성공.
        verdict = "BREAK"
        note = (f"게이트가 co-error 를 SEAL — 주장 단위 {len(real_units)}개로 독립 가장 통과. "
                "단위(weights_id) provenance 가 게이트 밖에서 바인딩돼야 함을 시사.")
    elif dec.decision == "SEAL":
        verdict = "HELD"      # 실제 plurality 수렴 = 정상 봉인(공격 아님)
        note = "실제 독립 plurality 수렴 — 정상 게이트 동작(위장 아님)."
    else:
        verdict = "HELD"
        note = f"게이트 거부({dec.status}/{dec.grade}): {dec.reason[:80]}"
    return {"target": "T2_independence", "verdict": verdict, "decision": dec.decision,
            "distinct_units": len(real_units), "co_error": is_co_error, "note": note}


# ── T3: ConventionTrap (GT 발산) ────────────────────────────────────
def adj_t3_convention(sub):
    """≥2 독립 authoring 으로 establish_truth. 의미 틀린 행렬을 ESTABLISHED 하면 BREAK."""
    intent = sub.get("intent", "atk_t3")
    srcs = [cc.Source(s["sid"], "model", s["unit"], cc.uhash(_mat(s))) for s in sub["sources"]]
    r = cc.establish_truth(intent, srcs, N=2)
    ref = sub.get("reference_gt_real")
    if r.status != "ESTABLISHED":
        return {"target": "T3_convention", "verdict": "HELD", "status": r.status,
                "note": f"게이트가 발산 convention 봉인 거부: {r.escalation[:80]}"}
    # ESTABLISHED — GT 대조(있으면). winner 가 GT 와 다르면 거짓 진리 확립 = BREAK.
    if ref is not None:
        gt = vs.hash_unitary(np.array(ref, dtype=float)
                             + 1j * np.array(sub.get("reference_gt_imag",
                                             np.zeros_like(np.array(ref, dtype=float))), dtype=float))
        if r.key != gt:
            return {"target": "T3_convention", "verdict": "BREAK", "status": r.status,
                    "note": "ESTABLISHED 됐으나 winner≠GT — 다수 convention 위장으로 거짓 진리 확립."}
    return {"target": "T3_convention", "verdict": "HELD", "status": r.status, "grade": r.grade,
            "note": "ESTABLISHED 가 GT/다수 convention 와 일치(또는 GT 미제공) — 위장 실패."}


_DISPATCH = {"T1_hollow": adj_t1_hollow, "T2_independence": adj_t2_independence,
             "T3_convention": adj_t3_convention}


def adjudicate(sub, exec_specs=False):
    t = sub.get("target")
    fn = _DISPATCH.get(t)
    if fn is None:
        return {"target": t, "verdict": "INVALID", "note": "알 수 없는 target"}
    try:
        return fn(sub, exec_specs=exec_specs) if t == "T1_hollow" else fn(sub)
    except Exception as e:                                  # malformed 제출물 = INVALID(크래시 아님)
        return {"target": t, "verdict": "INVALID", "note": f"{type(e).__name__}: {str(e)[:80]}"}


# ── selftest: 합성 적대샘플로 엔진 결정론 입증(외부 제출 없이) ───────
def _selftest():
    """알려진 결과의 합성 공격으로 adjudicator 가 결정론적으로 분류하는지 검증(P2a replay 정신)."""
    bad = cc.uhash(np.eye(2, dtype=complex))               # co-error 답(틀린 X=I)
    cases = [
        # T1: MatrixGate 우회 → DOC_GAP(정적)
        ({"target": "T1_hollow", "id": "st_hollow",
          "spec_text": "```python id=bloq\nbloq = cirq_gate_to_bloq(cirq.MatrixGate(U))\n```\n"},
         "DOC_GAP"),
        # T2-a: 같은 답·같은 unit 2개 → 게이트가 1단위로 붕괴 → REJECT → HELD
        ({"target": "T2_independence", "intent": "st_b4_sameunit",
          "sources": [{"sid": "a", "klass": "model", "unit": "w1", "u_hash": bad},
                      {"sid": "b", "klass": "model", "unit": "w1", "u_hash": bad}]}, "HELD"),
        # T2-b: 같은 답·라벨만 다른 2 unit → 게이트가 SEAL → BREAK(라벨 위조)
        ({"target": "T2_independence", "intent": "st_b4_labelforge",
          "sources": [{"sid": "a", "klass": "model", "unit": "w1", "u_hash": bad},
                      {"sid": "b", "klass": "model", "unit": "w2", "u_hash": bad}]}, "BREAK"),
        # T3: 두 모델이 서로 다른 convention(발산) → DIVERGENT → HELD
        ({"target": "T3_convention", "intent": "st_conv",
          "sources": [{"sid": "a", "unit": "w1", "golden_real": [[0, 1], [1, 0]]},
                      {"sid": "b", "unit": "w2", "golden_real": [[1, 0], [0, 1]]}]}, "HELD"),
        # INVALID: 알 수 없는 target
        ({"target": "T9_bogus"}, "INVALID"),
    ]
    ok = 0
    print("[selftest] 합성 적대샘플 → adjudicator 결정론 검증:")
    for sub, expect in cases:
        got = adjudicate(sub)["verdict"]
        mark = "✓" if got == expect else "✗"
        ok += got == expect
        print(f"  {mark} {sub['target']:16} expect={expect:8} got={got}")
    print(f"[selftest] {ok}/{len(cases)} 통과")
    return ok == len(cases)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true", help="합성 적대샘플로 엔진 검증")
    ap.add_argument("--exec-specs", action="store_true",
                    help="T1 제출 spec 을 temp store 에서 실제 봉인(샌드박스 주의)")
    args = ap.parse_args()

    os.makedirs(OUT, exist_ok=True)
    print("=" * 78)
    print("P3d ReproBounty — AutoAdjudicate (cross-model adversarial)")
    print("정직성: 모델 주장 불신·오라클 재검산·비파괴(temp store). 외부 AI 반증≠공개 인간 bounty.")
    print("=" * 78)

    selftest_ok = _selftest()

    # 실제 제출물 수거(없으면 relay 대기 = 정직한 BLOCKED)
    files = sorted(glob.glob(os.path.join(SUBS, "*.submission.json")))
    results = []
    for f in files:
        d = json.load(open(f, encoding="utf-8"))
        rt = d.get("runtime", os.path.basename(f))
        for sub in d.get("attacks", []):
            v = adjudicate(sub, exec_specs=args.exec_specs)
            v["runtime"] = rt
            results.append(v)
            print(f"  [{rt:10}] {v['target']:16} → {v['verdict']}")

    n_break = sum(1 for r in results if r["verdict"] == "BREAK")
    n_newgap = sum(1 for r in results if r["verdict"] == "NEW_GAP")
    relay_pending = len(files) == 0
    # 정직한 음성: 외부 제출이 있고 BREAK/NEW_GAP 0 → 방어선 생존(§7 신뢰자본)
    defenses_survived = (not relay_pending) and n_break == 0 and n_newgap == 0

    report = {
        "phase": "P3d ReproBounty AutoAdjudicate (cross-model adversarial)",
        "grade_label": "cross-model adversarial (NOT public human bounty — complement, honest label)",
        "honesty": "model claims untrusted; oracle re-runs deterministically; temp store only; "
                   "registry/specs/frozen unchanged; engine validated by selftest before real ingest.",
        "engine_selftest_passed": selftest_ok,
        "submissions_ingested": len(files),
        "relay_pending": relay_pending,
        "results": results,
        "n_break": n_break, "n_new_gap": n_newgap,
        "defenses_survived_external_round": defenses_survived,
        "note": ("RELAY PENDING: bounty 패키지 준비 완료, 정욱님 6런타임 전달·수거 대기. "
                 "selftest 로 엔진 결정론만 self-contained 입증." if relay_pending else
                 ("외부 cross-model 적대 라운드 — 방어선 생존(정직한 음성)" if defenses_survived
                  else f"BREAK={n_break} NEW_GAP={n_newgap} — 인간 검토 escalate")),
    }
    json.dump(report, open(os.path.join(OUT, "P3D-ADJUDICATION.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("-" * 78)
    print(f"engine_selftest={selftest_ok} · 제출={len(files)}"
          f"{' (relay 대기 — 정직 BLOCKED)' if relay_pending else ''} · "
          f"BREAK={n_break} NEW_GAP={n_newgap}  →  .pgf/bounty/P3D-ADJUDICATION.json")
    return 0 if selftest_ok else 1


if __name__ == "__main__":
    sys.exit(main())
