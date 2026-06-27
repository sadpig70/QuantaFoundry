# Multi-Model Persona Panel — Operations Protocol (v0.4, R-L)

> 리뷰 합의(Agent 4/5/6/7): 모든 persona(G/B/A)가 동일 base model 에서 돌면 same-weights co-error(b)와
> B4(같은 모델이 같은 default 로 수렴해 임의 봉인)를 원천 차단 못 한다. Persona-A(adversary)도 같은
> weights 면 무용함이 E5'에서 관측됨. → persona 를 **물리적으로 다른 weights** 에 배치하는 정책.

---

## 1. 원칙

- **독립성은 물리 단위(weights)로 센다.** 같은 weights 의 다수 산출 = 1 vote (KeyFreeConsensus
  `independence_unit`). persona 라벨(G/B/A)이 아니라 weights_id 가 독립 단위다.
- answer-key-free regime(정답표 없는 신규 진리)에서는 **최소 3 독립 단위** 강제:
  권장 = `2 distinct model families ⊕ 1 symbolic proof(sympy)`. 또는 `3 distinct model families`.
- Persona-A(adversary)는 **G·B 와 다른 model family** 여야 vote 로서 의미가 있다.

## 2. 배치 (6 런타임 풀에서)

| Persona | 역할 | 권장 weights (예) | 비고 |
|---|---|---|---|
| **G** (golden author) | 의도/유니터리 작성 | openai-gpt-5 | family-1 |
| **B** (bloq author) | 독립 회로 구현 | google-gemini / deepseek | family-2 (G≠B 필수) |
| **A** (adversary) | 반증·다수결 보강 | xai-grok / moonshot-kimi / alibaba-qwen | family-3 (G,B 와 상이) |
| **P** (proof) | sympy 등 symbolic | (모델 아님) | 항상 독립 단위 |

규칙:
1. `weights_id(G) ≠ weights_id(B) ≠ weights_id(A)` — 세 family 모두 상이.
2. answer-key 가 있는 baseline 구간은 anti-swap(u_hash==frozen key)으로 충분 → A off 가능.
3. answer-key 없는 신규 진리 구간은 A on + 최소 3 독립단위(2 model family + proof) 충족 시에만 봉인.
4. grade: `MULTIMODEL` = ≥2 distinct model families 수렴. `PROOF_BACKED` = proof ⊕ ≥1 독립. 둘 다면 최상.

## 3. corpus-correlation 할인 (R-I/F-6 연계)

6 LLM 은 겹치는 공개 코퍼스로 학습 → 교과서 항목 수렴은 "독립 발견"이 아니라 예상된 산물. 그러므로:
- **교과서 항목**: distinct-weights 수렴이라도 vote 가중 하향(예: family 당 0.5), 신뢰 등급 표기에 `corpus-correlated` 플래그.
- **hard/ambiguous 항목**(v04_hard 류): 수렴 시 full credit. 메커니즘 가치는 여기서만 입증된다.
- 이 정책은 grade 계산을 바꾸지 않고(코드 불변) **리포트 해석 가이드**로 둔다. consensus.py 확장 시
  `confidence_grade` 에 corpus_discount 옵션을 추가하는 것은 향후 SC 작업.

## 4. 실행 (이 정책의 적용 지점)

- v04 (app golden/bloq) · v04_hard (divergence) 라운드 제출 시 각 런타임의 `weights_id` 를 위 표대로 지정.
- ingest 는 `weights_id` 로 독립단위를 세므로, 같은 family 중복 제출은 자동 1 vote 병합(B4 차단).
- 신규(정답표 없는) 게이트/앱은 §2 규칙 3 충족 전까지 봉인 보류(escalation).
