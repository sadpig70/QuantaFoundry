# -*- coding: utf-8 -*-
"""
live_dispatch.py — P2b LiveDispatch wiring (task_plan_pg §P2b)

P2a 의 봉인 게이트(gated_panel)를 *라이브 디스패치 파이프라인*에 연결한다:
  신규 intent → ModelRegistry 에서 연결된 distinct-weights 어댑터로 디스패치
            → 각 어댑터가 endpoint.author_golden 으로 golden 산출 → consensus Source
            → gated_seal(P2a) 로 봉인/거부.

═══════════════════════════════════════════════════════════════════════════
정직성 경계 (이 스레드의 핵심)
═══════════════════════════════════════════════════════════════════════════
 - **wiring 은 self-contained, 실제 신규 모델 호출만 외부 의존.** 어댑터 endpoint=None 이면
   디스패치가 BLOCKED 를 정직하게 반환(미연결 모델 목록 노출). 실배포 시 endpoint 주입.
 - **ReplayEndpoint 는 wiring 검증용** — 이미 ingest된 v05 golden 을 *재생*할 뿐, 새 모델이
   *새 intent* 의 진리를 저작하는 것이 아니다. 따라서 이 스크립트가 입증하는 것은:
     (1) 디스패치→게이트 파이프라인이 end-to-end 작동한다,
     (2) 미연결 시 정직하게 BLOCKED 된다.
   *새* intent 의 봉인은 여전히 실제 distinct-weights 런타임(외부 relay) 필요.
 - consensus.py / crossmodel_adapter.py / gated_panel.py 는 *사용만*. frozen·sealed 무변경.
   비파괴(.pgf/panel/ 만 기록).

sub-PG:
    ModelRegistry    // 설정가능 CrossModelSource 어댑터 레지스트리(weights_id + endpoint)
    LiveDispatch     // panel_spec → 연결 어댑터 sources 수집; distinct-weights 미달 → BLOCKED
    ReplayEndpoint   // v05 저장 golden 반환 endpoint (wiring 검증; 신규 truth 아님)
    LiveSealPipeline // 신규 intent → dispatch → gated_seal(P2a) end-to-end
    UnwiredHonesty   // endpoint=None → BLOCKED + 미연결 모델 정직 노출
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
import consensus as cc                       # noqa: E402  (Source/uhash 사용만)
from crossmodel_adapter import CrossModelSource  # noqa: E402  (어댑터 골격 — 사용만)
import gated_panel as gp                      # noqa: E402  (P2a 게이트 — 사용만)

V05 = os.path.join(ROOT, "_workspace", "crossmodel", "v05_div", "submissions")
OUT = os.path.join(ROOT, ".pgf", "panel")


# ── ReplayEndpoint (wiring 검증용 — 저장된 golden 재생) ──────────────
class ReplayEndpoint:
    """v05 제출 데이터를 endpoint 인터페이스로 감싼다(author_golden). 신규 모델 호출이 아니라
    *재생* — wiring 이 end-to-end 작동함을 입증할 뿐, 새 intent 의 진리 저작이 아니다."""
    def __init__(self, weights_id, submissions):
        self.weights_id = weights_id
        self._by_id = {s["id"]: s for s in submissions}

    def author_golden(self, intent_id, formal_spec):
        s = self._by_id.get(intent_id)
        if s is None:
            raise KeyError(f"{self.weights_id}: intent '{intent_id}' 미제출 (replay 데이터 없음)")
        re_ = np.array(s["app_golden_real"], dtype=float)
        im = np.array(s.get("app_golden_imag", np.zeros_like(re_)), dtype=float)
        return re_ + 1j * im


# CrossModelSource.generate 는 endpoint.author_golden(intent, spec)→uhash 를 기대하나
# 현재 골격은 NotImplemented stub → 라이브 경로를 위해 generate 를 어댑터에 위임 호출로 래핑.
def _wired_source(adapter: CrossModelSource, intent_id, formal_spec):
    """endpoint 가 연결된 어댑터에서 consensus Source 산출 (라이브 경로)."""
    golden = adapter.endpoint.author_golden(intent_id, formal_spec)
    return cc.Source(f"{intent_id}_{adapter.model_id}", "model", adapter.weights_id, cc.uhash(golden))


# ── ModelRegistry + LiveDispatch ────────────────────────────────────
class ModelRegistry:
    def __init__(self, adapters):
        self.adapters = adapters

    def wired(self):
        return [a for a in self.adapters if a.available()]

    def unwired(self):
        return [a.model_id for a in self.adapters if not a.available()]


def live_dispatch_seal(intent_id, formal_spec, registry: ModelRegistry, declared_class=None):
    """신규 intent → 연결 어댑터로 디스패치 → gated_seal(P2a). 미연결 distinct-weights 부족 시 BLOCKED."""
    risk = gp.classify_risk(intent_id, declared_class)
    panel = gp.dispatch_policy(risk)
    wired = registry.wired()
    distinct = {a.weights_id for a in wired}
    if len(distinct) < panel.required_units:
        return {"intent": intent_id, "risk": risk, "decision": "BLOCKED",
                "reason": f"distinct-weights 연결 {len(distinct)} < 요구 {panel.required_units} "
                          f"(외부 의존: 미연결 {registry.unwired()})", "wired_weights": sorted(distinct)}
    sources = [_wired_source(a, intent_id, formal_spec) for a in wired]
    dec = gp.gated_seal(intent_id, panel, sources)
    return {"intent": intent_id, "risk": risk, "decision": dec.decision, "status": dec.status,
            "grade": dec.grade, "reason": dec.reason, "wired_weights": sorted(distinct),
            "distinct_weights_used": len({s.unit for s in sources})}


# ── main ────────────────────────────────────────────────────────────
def _load_v05_runtimes():
    out = {}
    for f in sorted(glob.glob(os.path.join(V05, "*.app.json"))):
        d = json.load(open(f, encoding="utf-8"))
        out[d["weights_id"]] = d["submissions"]
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 74)
    print("P2b LiveDispatch — 봉인 게이트 라이브 디스패치 wiring (self-contained portion)")
    print("정직성: wiring 검증=ReplayEndpoint(재생). 실제 신규모델 호출만 외부 relay 의존.")
    print("=" * 74)

    runtimes = _load_v05_runtimes()
    classes = {}
    aj = json.load(open(os.path.join(ROOT, "_workspace", "crossmodel", "v05_div", "app_intents.json"),
                        encoding="utf-8"))
    for k, v in aj.items():
        if isinstance(v, list):
            for it in v:
                if isinstance(it, dict) and "id" in it:
                    classes[it["id"]] = it.get("class", "")

    # (A) WIRED 경로: 6 어댑터에 ReplayEndpoint 주입 → 라이브 파이프라인 end-to-end
    wired_adapters = [CrossModelSource(f"m_{wid}", wid, ReplayEndpoint(wid, subs))
                      for wid, subs in runtimes.items()]
    reg_wired = ModelRegistry(wired_adapters)
    intents = sorted({s["id"] for subs in runtimes.values() for s in subs})
    wired_results = [live_dispatch_seal(i, {"id": i}, reg_wired, classes.get(i)) for i in intents]

    print(f"[LiveDispatch WIRED] 6 어댑터(ReplayEndpoint 주입) → 라이브 봉인 파이프라인:")
    for r in wired_results:
        print(f"   {r['intent']:18} {r['risk']:14} → {r['decision']:7} "
              f"({r.get('status','')}/{r.get('grade','')}) weights={r.get('distinct_weights_used')}")

    # WIRED 라이브 경로가 P2a 직접 replay 와 동일 판정인지 (wiring 정확성)
    direct, _cls = gp.load_v05()
    consistent = True
    for r in wired_results:
        panel = gp.dispatch_policy(gp.classify_risk(r["intent"], classes.get(r["intent"])))
        d = gp.gated_seal(r["intent"], panel, direct[r["intent"]]).decision
        if d != r["decision"]:
            consistent = False
    print(f"   ⇒ 라이브 경로 판정 == P2a 직접 replay: {consistent} (디스패치 wiring 정확)")

    # (B) UNWIRED 경로: endpoint=None → 정직한 BLOCKED
    unwired_adapters = [CrossModelSource(f"m_{wid}", wid, None) for wid in runtimes]
    reg_unwired = ModelRegistry(unwired_adapters)
    new_intent = live_dispatch_seal("brand_new_family_intent", {"id": "x"}, reg_unwired, None)
    print(f"[LiveDispatch UNWIRED] 신규 intent, endpoint 전부 None:")
    print(f"   {new_intent['decision']} — {new_intent['reason']}")

    # (C) PARTIAL: distinct-weights 1개만 연결 → 고위험 intent BLOCKED (B4 방어)
    one_wid = next(iter(runtimes))
    partial = [CrossModelSource("m_a", one_wid, ReplayEndpoint(one_wid, runtimes[one_wid])),
               CrossModelSource("m_b", one_wid, ReplayEndpoint(one_wid, runtimes[one_wid]))]  # 같은 weights 2개
    reg_partial = ModelRegistry(partial)
    partial_res = live_dispatch_seal("free_rz", {"id": "free_rz"}, reg_partial, classes.get("free_rz"))
    print(f"[LiveDispatch PARTIAL] 같은-weights 2어댑터(B4 시도) → "
          f"{partial_res['decision']} (distinct={len(partial_res['wired_weights'])}<2)")

    wired_ok = all(r["decision"] in ("SEAL", "REJECT") for r in wired_results)
    unwired_blocked = new_intent["decision"] == "BLOCKED"
    partial_blocked = partial_res["decision"] == "BLOCKED"
    all_ok = wired_ok and consistent and unwired_blocked and partial_blocked

    report = {
        "phase": "P2b LiveDispatch (wiring self-contained; live new-model call = external relay)",
        "honesty": "ReplayEndpoint replays already-ingested v05 golden (proves wiring end-to-end, "
                   "NOT new-model authoring of a new intent); endpoint=None → honest BLOCKED; "
                   "consensus/crossmodel_adapter/gated_panel used only; frozen/sealed untouched; "
                   "non-destructive (.pgf/panel/). A genuinely new intent still needs real "
                   "distinct-weights runtimes (external relay).",
        "wired_live_pipeline": wired_results,
        "live_equals_direct_replay": consistent,
        "unwired_blocked_honestly": new_intent,
        "partial_same_weights_blocked(B4 defense)": partial_res,
        "all_ok": bool(all_ok),
        "remaining_external": "endpoint.author_golden wiring to real distinct-weights model APIs "
                              "(정욱님 relay). 이 스크립트는 그 주입 지점까지 완비.",
    }
    json.dump(report, open(os.path.join(OUT, "LIVE-DISPATCH.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("-" * 74)
    print(f"all_ok={all_ok} (wiring 완비; 실제 신규모델 호출만 외부)  →  .pgf/panel/LIVE-DISPATCH.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
