# -*- coding: utf-8 -*-
"""
p2_live_ingest.py — P2b live relay ingest (task_plan_pg §P2b)

정욱님이 수거한 cross-model 제출물(_workspace/crossmodel/p2_live/submissions/*.json)을 읽어
P2a 봉인 게이트(gated_panel)에 투입한다. distinct-weights 수렴 → SEAL(MULTIMODEL), 발산 → REJECT.
독립 ground-truth(sx=√X, x_gate=X) 대조로 동반오류(co-error) 차단.

═══════════════════════════════════════════════════════════════════════════
정직성 경계
═══════════════════════════════════════════════════════════════════════════
 - 실제 봉인/frozen 등록은 *수행하지 않는다* — 게이트 판정 + GT 대조만 보고(비파괴).
   진짜 수렴 시 봉인은 실제 제출물 확보 + 정욱님 확인 후 별도 단계(consensus_keys 신성).
 - 제출물이 없으면 **dry-run**: mock(같은 정답·다른 weights_id)으로 wiring(SEAL 경로)만 입증 —
   *실제 합의 아님*(제출물을 내가 만들었으므로). 명확히 DRY-RUN 표기.
 - consensus.py/gated_panel/crossmodel_adapter *사용만*. frozen·sealed 무변경.

사용:
  python scripts/p2_live_ingest.py            # submissions/ 있으면 ingest, 없으면 dry-run
  python scripts/p2_live_ingest.py --dry-run  # mock wiring 검증 강제
"""
from __future__ import annotations

import os
import sys
import json
import glob

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts"))
sys.path.insert(0, os.path.join(ROOT, ".pgf", "keyfree"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import verify_seal as vs                      # noqa: E402  (hash_unitary 사용만)
import consensus as cc                        # noqa: E402  (Source/uhash 사용만)
import gated_panel as gp                      # noqa: E402  (P2a 게이트 사용만)

PKG = os.path.join(ROOT, "_workspace", "crossmodel", "p2_live")
SUBS = os.path.join(PKG, "submissions")
OUT = os.path.join(ROOT, ".pgf", "panel")


# ── 독립 ground-truth (formal-spec 축; co-error 차단) ───────────────
def ground_truth():
    X = np.array([[0, 1], [1, 0]], complex)
    SX = 0.5 * np.array([[1 + 1j, 1 - 1j], [1 - 1j, 1 + 1j]], complex)  # √X principal, SX²=X
    return {"x_gate": vs.hash_unitary(X), "sx": vs.hash_unitary(SX)}


# ── FileEndpoint: 수거 제출물을 endpoint.author_golden 으로 ─────────
class FileEndpoint:
    def __init__(self, submission):
        self.weights_id = submission["weights_id"]
        self._by_id = {s["id"]: s for s in submission["submissions"]}

    def u_hash(self, intent_id):
        s = self._by_id.get(intent_id)
        if s is None:
            return None
        re_ = np.array(s["app_golden_real"], dtype=float)
        im = np.array(s.get("app_golden_imag", np.zeros_like(re_)), dtype=float)
        return cc.uhash(re_ + 1j * im)


def _mock_submissions():
    """DRY-RUN: 정답 sx/x 를 distinct weights 3개로 — wiring(SEAL 경로) 검증용. 실제 합의 아님."""
    X = [[0, 1], [1, 0]]
    SX_re = [[0.5, 0.5], [0.5, 0.5]]
    SX_im = [[0.5, -0.5], [-0.5, 0.5]]
    subs = []
    for wid in ["mock-alpha", "mock-beta", "mock-gamma"]:
        subs.append({"weights_id": wid, "submissions": [
            {"id": "x_gate", "app_golden_real": X, "app_golden_imag": [[0, 0], [0, 0]]},
            {"id": "sx", "app_golden_real": SX_re, "app_golden_imag": SX_im}]})
    return subs


def main():
    os.makedirs(OUT, exist_ok=True)
    force_dry = "--dry-run" in sys.argv
    files = sorted(glob.glob(os.path.join(SUBS, "*.json")))
    real = bool(files) and not force_dry
    if real:
        submissions = [json.load(open(f, encoding="utf-8")) for f in files]
        mode = "REAL"
    else:
        submissions = _mock_submissions()
        mode = "DRY-RUN (mock — wiring 검증, 실제 합의 아님)"

    print("=" * 76)
    print(f"P2b live ingest — cross-model 제출물 → P2a 게이트  [{mode}]")
    print("정직성: 게이트 판정+GT 대조만(봉인/frozen 미수행, 비파괴).")
    print("=" * 76)

    GT = ground_truth()
    intents = json.load(open(os.path.join(PKG, "intents.json"), encoding="utf-8"))["intents"]
    endpoints = [FileEndpoint(s) for s in submissions]
    weights = sorted({e.weights_id for e in endpoints})
    print(f"제출 런타임 {len(endpoints)} · distinct weights {len(weights)}: {weights}")

    results = []
    for it in intents:
        iid = it["id"]
        declared = it.get("class")
        # 각 런타임의 u_hash → consensus Source (independence unit = weights_id)
        sources, calib = [], {}
        for e in endpoints:
            uh = e.u_hash(iid)
            if uh is None:
                continue
            sources.append(cc.Source(f"{iid}_{e.weights_id}", "model", e.weights_id, uh))
            calib[e.weights_id] = (uh == GT[iid]) if iid in GT else None
        risk = gp.classify_risk(iid, declared)
        panel = gp.dispatch_policy(risk)
        dec = gp.gated_seal(iid, panel, sources)
        # GT 대조: winner u_hash == 독립 GT?
        gt_match = None
        if dec.decision == "SEAL" and iid in GT:
            winner = max(cc.independent_votes(sources).items(), key=lambda kv: len(kv[1]))[0]
            gt_match = (winner == GT[iid])
        results.append({
            "intent": iid, "class": declared, "risk": risk,
            "distinct_weights": len({s.unit for s in sources}),
            "decision": dec.decision, "status": dec.status, "grade": dec.grade,
            "gt_match": gt_match,
            "calib_per_runtime": calib,
            "would_propose_freeze": (dec.decision == "SEAL" and gt_match is not False
                                     and risk != "keyed"),
        })

    for r in results:
        gt = {True: "GT✓", False: "GT✗", None: "GT—"}[r["gt_match"]]
        print(f"  {r['intent']:8} {r['risk']:13} weights={r['distinct_weights']} "
              f"→ {r['decision']:6} ({r['status']}/{r['grade']}) {gt}"
              + ("  ⇒ 봉인·frozen 제안(실데이터+확인 후)" if r["would_propose_freeze"] else ""))

    sx = next(r for r in results if r["intent"] == "sx")
    x = next(r for r in results if r["intent"] == "x_gate")
    pipeline_ok = (x["decision"] in ("SEAL", "REJECT") and sx["decision"] in ("SEAL", "REJECT"))

    report = {
        "phase": "P2b live ingest (sx round)",
        "mode": mode,
        "honesty": "gate verdict + independent GT match only; NO sealing / NO frozen-key write "
                   "(deferred to real submissions + operator confirmation); dry-run mock is "
                   "wiring-validation only (NOT real consensus); consensus/gated_panel used only; "
                   "frozen/sealed untouched.",
        "ground_truth_u_hash": {k: v[:16] for k, v in GT.items()},
        "distinct_weights": weights,
        "results": results,
        "pipeline_ok": bool(pipeline_ok),
        "operator_next": "정욱님: RUNTIME-BRIEF.md+intents.json+SUBMISSION-TEMPLATE.json 를 ≥2(권장 6) "
                         "distinct-weights 모델 세션에 독립 전달 → <model>.submission.json 수거 → "
                         "_workspace/crossmodel/p2_live/submissions/ 에 저장 → 본 스크립트 재실행(REAL).",
    }
    json.dump(report, open(os.path.join(OUT, "P2-LIVE-INGEST.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("-" * 76)
    if not real:
        print("DRY-RUN: mock distinct-weights 수렴 → sx SEAL 경로 입증(실제 합의 아님).")
    print(f"pipeline_ok={pipeline_ok}  →  .pgf/panel/P2-LIVE-INGEST.json")
    print("정욱님 다음 단계: 패키지 3종 → ≥2 모델 독립 전달 → submissions/ 수거 → 재실행(REAL).")
    return 0 if pipeline_ok else 1


if __name__ == "__main__":
    sys.exit(main())
