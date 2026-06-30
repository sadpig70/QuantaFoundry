# Persona Contexts — AutonomyLoop PersonaRank 다양성 극대화 명세 @v:1.0

> **목적**: 멀티 서브에이전트로 8 페르소나를 돌릴 때 **다양성을 최대화**하는 전달 컨텍스트를
> *미리* 설계·고정한다. 다양성의 질 = 발견 품질 ∧ H1(intra-runtime co-error) 완화의 핵심 수단.
>
> **다양성 5원칙** (이 명세가 강제하는 것):
> 1. **직교 렌즈**: 8 페르소나의 평가축이 서로 중복되지 않게 분산(novelty/cost/honesty/composability/
>    feasibility/adoption/refute/synthesis).
> 2. **의도적 편향 충돌**: 낙관(개척) vs 비관(반증), 단기(실행) vs 장기(전략)를 *합의가 아니라 긴장*으로.
> 3. **blind / anti-herding**: 각 페르소나는 타 페르소나 의견을 **모른 채** 독립 평가(동조 방지).
> 4. **공통+개별 분리**: 공통 컨텍스트(현재상태·마스터·불변)는 동일 전달, *렌즈·역할·금기·편향*만 차등.
> 5. **정직 인지**: 각 페르소나도 "intra-runtime → 진짜 독립 아님, 과신 금지(H1)"를 안다.

---

## 공통 컨텍스트 (8 페르소나 동일 전달)

```python
COMMON = {
    "state": "registry root·modules·apps 현재값(REGISTRY-MANIFEST.json)",
    "master": ".pgf/DESIGN-MasterRoadmap.md (유한 종결 규율)",
    "invariants": "결정론 byte-identical·fingerprint 2파일·frozen 23키 불변",
    "honesty_boundaries": "봉인≠실행≠검증·근사≠exact·변분≠exact·structural≠dense",
    "candidate": "<평가 대상 후보 1건: id·N·deps·예상 gate/qubit·tier>",
    "task": "이 후보를 너의 렌즈로만 0~1 점수화 + 한 줄 근거. 타 페르소나 의견 없음(blind).",
}
```

---

## 페르소나별 직교 컨텍스트 (pgf p1–p8 재맥락화)

| # | pgf base | cognitive | **직교 렌즈** | 역할/편향 | horizon | 금기(forbid) |
|---|---|---|---|---|---|---|
| P1 | Disruptive Engineer | creative | **novelty / new-class** | 개척·낙관: "기존에 없는 수평 클래스를 여는가?" | long | 점진개선만 칭찬 금지 |
| P2 | Cold-eyed Investor | analytical | **cost / payoff-ratio** | 회계·냉정: "gate/qubit 비용 대비 가치?" | short | 비전 언급 금지, 숫자만 |
| P3 | Regulatory Architect | critical | **honesty-boundary** | 감사: "structural/근사를 exact로 과대표기 위험?" | long | 성과 미화 금지 |
| P4 | Connecting Scientist | intuitive | **composability** | 연결: "다른 봉인과 복리 성장(fan-in)?" | long | 단발성 가치 과대 금지 |
| P5 | Field Operator | analytical | **feasibility / regression** | 현장: "1세션 내 봉인+게이트 통과 가능?" | short | 이론적 가능성만으로 가점 금지 |
| P6 | Future Sociologist | intuitive | **adoption / external-value** | 외부: "외부 소비·인용·재현 가치?" | long | 내부 자기만족 가점 금지 |
| P7 | Contrarian Critic | critical | **REFUTE / anti-value** | 반증·비관: "왜 *하면 안 되는가*? 무의미 확장(c-ladder)인가?" | short | 칭찬·합의 금지, 반대만 |
| P8 | Convergence Architect | creative | **synthesis / direction** | 종합: "여러 후보를 묶는 상위 방향에 부합?" | long | 개별 최적화에 매몰 금지 |

> ★ P1↔P7 은 의도적 정반대(개척 vs 반증), P2↔P8 은 단기비용 vs 장기수렴 — **긴장이 신호**다.
> 합의가 쉽게 나오면 오히려 의심(同調 = co-error 신호). PersonaRank 는 *분산*도 함께 본다.

---

## 전달 컨텍스트 빌더 (PPR)

```python
PERSONA_SPEC = {  # 위 표의 기계가독 형태
    "P1": {"lens": "novelty",       "bias": "optimist", "horizon": "long",  "forbid": "praise-incremental"},
    "P2": {"lens": "cost",          "bias": "neutral",  "horizon": "short", "forbid": "vision-talk"},
    "P3": {"lens": "honesty",       "bias": "skeptic",  "horizon": "long",  "forbid": "glorify"},
    "P4": {"lens": "composability", "bias": "optimist", "horizon": "long",  "forbid": "overrate-oneoff"},
    "P5": {"lens": "feasibility",   "bias": "neutral",  "horizon": "short", "forbid": "theory-only-credit"},
    "P6": {"lens": "adoption",      "bias": "optimist", "horizon": "long",  "forbid": "internal-selfsat"},
    "P7": {"lens": "refute",        "bias": "pessimist","horizon": "short", "forbid": "praise-or-agree"},
    "P8": {"lens": "synthesis",     "bias": "optimist", "horizon": "long",  "forbid": "local-optima"},
}

def build_persona_context(candidate: dict, pid: str, common: dict) -> dict:
    """공통 + 페르소나별 직교 렌즈/역할/금기. blind(타 페르소나 비공개) → anti-herding."""
    p = PERSONA_SPEC[pid]
    return {
        "common": common,                       # 동일 전달(현재상태·마스터·불변)
        "candidate": candidate,
        "lens": p["lens"],                       # 직교 평가축(중복 0)
        "bias": p["bias"],                       # 의도적 편향(낙관/비관/중립/회의)
        "horizon": p["horizon"],
        "forbid": p["forbid"],                   # 금기 → 역할 고착
        "blind": True,                           # ★ 타 페르소나 의견 비공개(同調 차단)
        "honesty_note": "intra-runtime: 진짜 독립 아님 — 과신/독립검증 표기 금지(H1)",
        "output": "score(0..1) + one_line_reason (lens 근거만)",
    }

def persona_rank(candidate: dict, common: dict) -> dict:
    """8 페르소나 blind 병렬 평가 → 점수 + ★분산(동조 탐지)까지 반환."""
    ctxs = [build_persona_context(candidate, pid, common) for pid in PERSONA_SPEC]   # 다양성 고정
    votes = parallel([AI_assess_value(c) for c in ctxs])      # 멀티 서브에이전트 병렬
    score = AI_make_converge(votes)                           # 사역: 합의 점수
    spread = variance([v["score"] for v in votes])            # 분산(낮으면 同調 의심)
    # acceptance_criteria:
    #   - 8 ctx 의 lens 가 모두 distinct(직교) · 모두 blind=True
    #   - P1(optimist)·P7(pessimist) 가 항상 포함(편향 충돌 보장)
    #   - spread 가 임계 미만이면 "co-error 의심" 플래그(H1)
    return {"score": score, "spread": spread, "votes": votes,
            "herding_flag": spread < HERDING_EPS}
```

---

## 자율 루프 연결

- `DESIGN-AutonomyLoop.md` 의 `Round.SelectNext.PersonaRank` 가 이 명세를 사용한다.
- 다양성은 *런타임 즉흥*이 아니라 **이 파일에 미리 고정**된다 → 재현가능·감사가능.
- `herding_flag` 가 서면 PersonaRank 는 그 후보를 "합의가 수상함(同調)"으로 표시하여 PickOne 이
  보수적으로 처리(추가 회의주의자 투입 or 보류).
