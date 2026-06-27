# -*- coding: utf-8 -*-
"""
gated_panel.py — P2a GatedConsensusPanel (task_plan_pg §P2, self-contained)

키-프리/모호/신규-패밀리 intent 에 *물리적 distinct-weights ≥2* 를 강제하는 봉인 게이트.
E5'/B4 결함(같은 모델 격리 페르소나가 같은 default 로 수렴→임의 봉인)을 *구조적*으로 차단한다.
검증은 신규 외부 호출 없이 EXT v05 6런타임 *실데이터 replay* 로 수행한다(B4 차단 정량화, §7 반증).

═══════════════════════════════════════════════════════════════════════════
sub-PG (P2a 분해)
═══════════════════════════════════════════════════════════════════════════
P2a_GatedConsensusPanel
    IntentRiskClassifier // intent → risk {keyed, free_param, convention, new_family, sanity_unkeyed}
    GatedDispatchPolicy  // risk → PanelSpec(required distinct-weights N, grade_floor, personas)
    IndependenceUnitGate // gated_seal: establish_truth(사용만) + grade_floor(MULTIMODEL) 강제
    ReplayValidation     // v05 6런타임 replay → 클래스별 establish_truth 판정 재현
    FalsificationProbe   // naive count(B4취약) vs independence-unit(gated) 검출률 대조
    DeterminismGuard     // frozen 15키 불변(read-only)·비파괴(.pgf/panel/)

정직성 경계:
 - replay ≠ 신규 호출: *이미 ingest된* 6런타임(deepseek/gemini/gpt-5/grok/kimi/qwen) 실데이터를
   재생할 뿐 — 새 외부 호출 0. 신규 intent 라이브 봉인(P2b)만 외부 relay 의존(BLOCKED).
 - consensus.py(establish_truth/independence_unit/confidence_grade)는 *사용만* — 재구현 금지.
 - 게이트는 봉인을 *더 엄격*하게(고위험 거부) 만들 뿐, 기존 봉인을 약화/변경하지 않는다.
 - frozen consensus_keys.json 은 read-only(봉인점검 시 재생성 금지). 비파괴(.pgf/panel/ 만 기록).
"""
from __future__ import annotations

import os
import sys
import json
import glob
import hashlib
from dataclasses import dataclass

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts"))
sys.path.insert(0, os.path.join(ROOT, ".pgf", "keyfree"))
import consensus as cc          # noqa: E402  (Source/establish_truth/independence_unit/uhash 사용만)

KEYS = os.path.join(ROOT, ".pgf", "keyfree", "consensus_keys.json")
V05 = os.path.join(ROOT, "_workspace", "crossmodel", "v05_div", "submissions")
INTENTS = os.path.join(ROOT, "_workspace", "crossmodel", "v05_div", "app_intents.json")
OUT = os.path.join(ROOT, ".pgf", "panel")


# ── IntentRiskClassifier ────────────────────────────────────────────
def _answer_keys():
    return set(json.load(open(KEYS, encoding="utf-8")).keys())


def classify_risk(intent_id, declared_class=None):
    """intent → risk. keyed(답있음)=저위험; free_param/convention/new_family/sanity_unkeyed=고위험."""
    if intent_id in _answer_keys():
        return "keyed"
    if declared_class:                                  # replay: app_intents 의 class 태그
        c = declared_class[0].upper()
        return {"C": "free_param", "D": "convention", "S": "sanity_unkeyed"}.get(c, "new_family")
    return "new_family"                                 # 답키 없는 신규 = 고위험 기본


# ── GatedDispatchPolicy ─────────────────────────────────────────────
@dataclass
class PanelSpec:
    risk: str
    required_units: int          # establish_truth 의 N (독립단위 하한)
    grade_floor: str             # KEYED | MULTIMODEL
    personas: tuple


def dispatch_policy(risk) -> PanelSpec:
    """위험도 → 패널. 답있는 영역은 단일모델(비용↓); 키-프리/모호/신규는 distinct-weights≥2 + 적대자."""
    if risk == "keyed":
        return PanelSpec(risk, 1, "KEYED", ("G", "B"))
    # ambiguous/new_family/free_param/convention/sanity_unkeyed → B4 차단: distinct weights ≥2 + Persona-A
    return PanelSpec(risk, 2, "MULTIMODEL", ("G", "B", "A"))


# ── IndependenceUnitGate ────────────────────────────────────────────
@dataclass
class SealDecision:
    decision: str                # SEAL | REJECT
    status: str                  # establish_truth status
    grade: str
    reason: str = ""


def gated_seal(intent_id, panel: PanelSpec, sources, rho=0.0) -> SealDecision:
    """establish_truth(*사용만*) + 패널 grade_floor 강제. 고위험인데 MULTIMODEL 미달 → 봉인거부."""
    r = cc.establish_truth(intent_id, sources, N=panel.required_units, rho=rho)
    if r.status != "ESTABLISHED":
        return SealDecision("REJECT", r.status, r.grade or "", r.escalation)
    if panel.grade_floor == "MULTIMODEL" and r.grade not in ("MULTIMODEL", "PROOF_BACKED"):
        return SealDecision("REJECT", r.status, r.grade,
                            f"unkeyed/high-risk intent needs ≥2 distinct weights; got grade={r.grade}")
    return SealDecision("SEAL", r.status, r.grade, f"key={r.key[:12]}")


# ── replay 소스 로딩 (v05 6런타임 실데이터) ─────────────────────────
def _golden_uhash(sub):
    re_ = np.array(sub["app_golden_real"], dtype=float)
    im = np.array(sub.get("app_golden_imag", np.zeros_like(re_)), dtype=float)
    return cc.uhash(re_ + 1j * im)


def load_v05():
    """intent_id → {weights_id: Source(model)} (6런타임). + declared class 맵."""
    runtimes = {}
    for f in sorted(glob.glob(os.path.join(V05, "*.app.json"))):
        d = json.load(open(f, encoding="utf-8"))
        runtimes[d["weights_id"]] = d["submissions"]
    classes = {}
    aj = json.load(open(INTENTS, encoding="utf-8"))
    for k, v in aj.items():
        if isinstance(v, list):
            for it in v:
                if isinstance(it, dict) and "id" in it:
                    classes[it["id"]] = it.get("class", "")
    by_intent = {}
    for wid, subs in runtimes.items():
        for s in subs:
            iid = s["id"]
            src = cc.Source(f"{iid}_{wid}", "model", wid, _golden_uhash(s))
            by_intent.setdefault(iid, []).append(src)
    return by_intent, classes


# ── naive count 합의 (B4-취약 baseline: weights 무시, raw 다수결) ────
def naive_count_seal(sources, N=2):
    """독립단위 무시하고 raw 출처 수만 세는 B4-취약 합의. 같은-weights 다수도 봉인(결함)."""
    counts = {}
    for s in sources:
        counts[s.u_hash] = counts.get(s.u_hash, 0) + 1
    top = max(counts.values())
    return "SEAL" if top >= N else "REJECT"


# ── main ────────────────────────────────────────────────────────────
def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 74)
    print("P2a GatedConsensusPanel — distinct-weights 강제 봉인 게이트 (B4 구조 차단)")
    print("정직성: replay(기존 6런타임 실데이터, 신규호출 0). consensus.py 사용만. frozen read-only.")
    print("=" * 74)

    keys_before = hashlib.sha256(open(KEYS, "rb").read()).hexdigest()
    by_intent, classes = load_v05()

    # 문서화된 v05 ingest ground-truth(HANDOFF 5o): free-param=발산, sanity=만장일치,
    # convention 은 균일하지 않음 — rz/csqrtz 4-2 다수(정당한 multi-model 합의→SEAL) vs
    # ry 3-3 동률(plurality 부재→CONTESTED→REJECT). 게이트는 이 nuance 를 정확 재현해야 한다.
    EXPECTED_V05 = {
        "free_cphase": "REJECT",       # C: free-param → DIVERGENT (necessity-NEEDED)
        "free_rz": "REJECT",           # C: free-param → DIVERGENT
        "sanity_cz": "SEAL",           # S: 만장일치 → ESTABLISHED MULTIMODEL
        "split_ry_dir": "REJECT",      # D: 3-3 동률 → CONTESTED (contested guard)
        "split_rz_sign": "SEAL",       # D: 4-2 다수 → ESTABLISHED (다수 convention, 소수=문서화 변형)
        "split_csqrtz_sign": "SEAL",   # D: 4-2 다수 → ESTABLISHED
    }

    # ── ReplayValidation: 실제 distinct-weights 패널 ──
    replay = []
    for iid in sorted(by_intent):
        risk = classify_risk(iid, classes.get(iid))
        panel = dispatch_policy(risk)
        sources = by_intent[iid]
        n_units = len({cc.independence_unit(s) for s in sources})
        dec = gated_seal(iid, panel, sources)
        expect = EXPECTED_V05.get(iid, "?")
        replay.append({"intent": iid, "class": classes.get(iid), "risk": risk,
                       "distinct_weights": n_units, "panel_grade_floor": panel.grade_floor,
                       "gated_decision": dec.decision, "status": dec.status, "grade": dec.grade,
                       "expected_v05_documented": expect,
                       "match": (expect == "?" or dec.decision == expect)})

    print("[ReplayValidation] 6런타임 실데이터 → gated 봉인 판정:")
    for r in replay:
        mk = "✓" if r["match"] else "✗"
        print(f"  {mk} {r['intent']:18} {r['risk']:14} weights={r['distinct_weights']} "
              f"→ {r['gated_decision']:6} ({r['status']}/{r['grade']}) expect={r['expected_v05_documented']}")

    # ── FalsificationProbe: naive(B4) vs gated(independence) ──
    probe = []
    for iid in sorted(by_intent):
        risk = classify_risk(iid, classes.get(iid))
        panel = dispatch_policy(risk)
        one = by_intent[iid][0]                          # 한 모델
        b4_personas = [one, cc.Source(one.sid + "_p2", "model", one.unit, one.u_hash)]  # 같은 weights 2페르소나
        naive = naive_count_seal(b4_personas, N=panel.required_units)   # B4: raw 2개 → seal
        gated = gated_seal(iid, panel, b4_personas).decision           # independence: 1단위 → reject
        probe.append({"intent": iid, "risk": risk,
                      "b4_naive_count": naive, "gated_independence": gated,
                      "b4_blocked": naive == "SEAL" and gated == "REJECT"})

    blocked = sum(1 for p in probe if p["b4_blocked"])
    naive_seals = sum(1 for p in probe if p["b4_naive_count"] == "SEAL")
    print(f"[FalsificationProbe] 단일모델 2페르소나(B4) — naive count vs gated independence:")
    for p in probe:
        print(f"  {p['intent']:18} naive(B4)={p['b4_naive_count']:6} gated={p['gated_independence']:6} "
              f"{'→ B4 차단' if p['b4_blocked'] else ''}")
    print(f"  ⇒ naive 가 임의봉인할 {naive_seals} intent 중 gated 가 {blocked} 차단 "
          f"(B4 구조 차단율 {blocked}/{naive_seals})")

    # ── DeterminismGuard ──
    keys_after = hashlib.sha256(open(KEYS, "rb").read()).hexdigest()
    frozen_intact = keys_before == keys_after

    _dec = {r["intent"]: r["gated_decision"] for r in replay}
    replay_ok = all(r["match"] for r in replay)
    b4_ok = (blocked == naive_seals and naive_seals > 0)
    # 구조적 속성 (P2 thesis 의 핵심 주장):
    free_param_diverge = _dec.get("free_cphase") == "REJECT" and _dec.get("free_rz") == "REJECT"
    tie_contested = _dec.get("split_ry_dir") == "REJECT"                  # 3-3 → CONTESTED guard
    majority_sealed = _dec.get("split_rz_sign") == "SEAL" and _dec.get("split_csqrtz_sign") == "SEAL"  # 4-2 다수
    sanity_seals = _dec.get("sanity_cz") == "SEAL"
    all_ok = (replay_ok and b4_ok and frozen_intact and free_param_diverge
              and tie_contested and majority_sealed and sanity_seals)

    print(f"[DeterminismGuard] frozen 15키 불변={frozen_intact} · 비파괴(.pgf/panel/)")

    report = {
        "phase": "P2a GatedConsensusPanel",
        "honesty": "replay of already-ingested EXT v05 distinct-weights data (no new external "
                   "calls); consensus.py used only; gate only tightens sealing (rejects high-risk "
                   "without ≥2 distinct weights); frozen consensus_keys.json read-only; "
                   "non-destructive (.pgf/panel/). Live new-intent dispatch (P2b) stays BLOCKED.",
        "policy": {"keyed": "1 model (KEYED floor)",
                   "high_risk(free_param/convention/new_family/sanity_unkeyed)":
                   "≥2 distinct weights + Persona-A (MULTIMODEL floor)"},
        "replay_validation": replay,
        "falsification_probe": {
            "method": "단일모델 2페르소나(같은 weights_id) → naive count(B4취약) vs independence-unit(gated)",
            "naive_would_seal": naive_seals, "gated_blocked": blocked,
            "b4_structural_block_rate": f"{blocked}/{naive_seals}",
            "detail": probe,
        },
        "frozen_keys_intact": frozen_intact,
        "structural_properties": {
            "free_param_diverges(necessity)": bool(free_param_diverge),
            "3-3_tie_contested(guard)": bool(tie_contested),
            "4-2_majority_sealed(legit multimodel)": bool(majority_sealed),
            "sanity_seals_multimodel": bool(sanity_seals),
        },
        "convention_nuance": "convention-split 은 균일 거부가 아님 — 4-2 다수(rz/csqrtz)는 정당한 "
                             "multi-model 합의로 SEAL(소수 convention=문서화 변형), 3-3 동률(ry)만 "
                             "CONTESTED→REJECT. EXT v05 ingest(HANDOFF 5o) ground-truth 재현.",
        "all_ok": bool(all_ok),
        "p2b_blocked": "live new-intent distinct-weights dispatch needs external relay (ModelConfigurableDispatch wiring + endpoint).",
    }
    json.dump(report, open(os.path.join(OUT, "PANEL-VALIDATION.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("-" * 74)
    print(f"all_ok={all_ok}  →  .pgf/panel/PANEL-VALIDATION.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
