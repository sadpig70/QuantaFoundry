# EXT 운영 안내 — v0.4 외부 6런타임 라운드 (정욱님용)

> 외부 리뷰(7 AI)의 self-contained 항목은 본 진행자가 완료(`status-V04Review.json`).
> 남은 **외부 의존(EXT)** 항목 = 6런타임 cross-model 호출이 필요한 것들. 본 진행자가 brief·intents·
> 템플릿·ingest 파이프라인을 준비·스모크검증했고, **배포·수급은 정욱님**, 결과 모이면 본 진행자가 ingest.
> 6런타임 = `gpt-5 · gemini · grok · kimi · qwen · deepseek` (이전 라운드와 동일 distinct-weights).

---

## 패키지 구성 (3 라운드 + 1 정책)

| 라운드 | 목적 (리뷰 대응) | 브리프 | intents | 제출 위치 | ingest |
|---|---|---|---|---|---|
| **R5a app-golden** | N=21 layer 의도 cross-model 확립 (R-B) | `v04/APP-GOLDEN-BRIEF.md` | `v04/app_intents.json` | `v04/submissions/<rt>.app.json` | `ingest_app_golden.py --dir v04` |
| **R5b app-bloq** | N=21 multiplier 독립 회로 합성 + 6런타임 (R-B) | `v04/APP-BLOQ-BRIEF.md` + `v04/GATE-VOCABULARY.json` | `v04/app_intents.json` | `v04/submissions_bloq/<rt>.bloq.json` | `ingest_app_bloq.py --dir v04` |
| **R5c hard-intent** | KeyFreeConsensus *necessity* 발산 측정 (R-D/F-1) | `v04_hard/HARD-INTENT-BRIEF.md` | `v04_hard/app_intents.json` | `v04_hard/submissions/<rt>.app.json` | `ingest_app_golden.py --dir v04_hard` |
| **R5d persona panel** | 이종 weights 배치 정책 (R-L) | `v04/PERSONA-PANEL-PROTOCOL.md` | — (정책) | — | — (운영 규칙) |

## 각 런타임에 전달할 것

**R5a/R5b (한 번에 가능)** — 각 런타임에게:
1. `v04/APP-GOLDEN-BRIEF.md` + `v04/app_intents.json` + `v04/SUBMISSION-TEMPLATE-golden.json`
2. (회로도 받을 거면) `v04/APP-BLOQ-BRIEF.md` + `v04/GATE-VOCABULARY.json` + `v04/SUBMISSION-TEMPLATE-bloq.json`
3. 산출: golden → `v04/submissions/<runtime>.app.json`, bloq → `v04/submissions_bloq/<runtime>.bloq.json`
4. `weights_id` 는 `PERSONA-PANEL-PROTOCOL.md §2` 표대로 distinct 지정.

**R5c** — 각 런타임에게: `v04_hard/HARD-INTENT-BRIEF.md` + `v04_hard/app_intents.json` +
`v04_hard/SUBMISSION-TEMPLATE.json` → 산출 `v04_hard/submissions/<runtime>.app.json`.
**중요**: R5c 의 Class B(모호) intent 는 "정답 맞히기"가 아니라 **각 모델의 기본값을 관찰**하는 것 —
런타임에게 *서로 상의 금지, 명확화 질문 금지, 자연스러운 default 로 commit* 을 반드시 전달.

## 격리 규칙 (모든 라운드 공통, 신뢰 핵심)

- 런타임끼리 **서로의 제출물·sealed 파일·decomposition 을 보면 안 됨** (독립성 = 신뢰 근거).
- golden 작성자 ≠ bloq 작성자 권장 (동반오류 방화벽). 최소 한 명은 G, 다른 한 명은 B.
- 같은 weights 다중 제출은 1 vote 로 병합되므로(자동), 진짜 distinct 6개가 핵심.

## 결과 수급 후 (본 진행자가 실행)

"결과 모였다" 하시면:
```
python .pgf/keyfree/ingest_app_golden.py --dir v04        # R5a 합의 + 봉인앱 대조
python .pgf/keyfree/ingest_app_bloq.py   --dir v04        # R5b 회로 조립 + 대조
python .pgf/keyfree/ingest_app_golden.py --dir v04_hard   # R5c 발산 측정
```
→ 리포트: `v04/APP-CONSENSUS-REPORT.json`, `v04/APP-BLOQ-REPORT.json`, `v04_hard/APP-CONSENSUS-REPORT.json`.

## 기대 판정 (성공 기준)

- **R5a**: 4개 앱(iqft7, cmul2/4/16_mod21) ≥2 distinct-weights 수렴 → ESTABLISHED + 봉인앱 u_hash 일치
  → N=21 layer 의도가 in-house authorship 에서 cross-model 로 승격.
- **R5b**: 서로 다른 회로가 같은 u_hash 로 수렴 + 봉인앱 일치 → 본 진행자의 honest reversible synthesis
  를 독립 합성이 교차확인. dissent(틀린 회로)는 자동 탐지·기각(구현측 방화벽 실증).
- **R5c**: Class A 수렴(ESTABLISHED) = 메커니즘이 비교과서에서 동작. Class B 발산(DIVERGENT) =
  단일출처면 거짓봉인됐을 것을 consensus 가 차단 → **necessity 입증**(F-1). 발산율이 측정값.

## 스모크검증 상태 (본 진행자)

- intents/conventions 가 봉인된 in-house golden 과 일치함을 확인(아래 SMOKE 결과 참조): 라운드가
  well-posed(=의도가 유일한 유니터리를 고정). 파이프라인 `--dir` 경로·스키마 정상.
- 자세한 스모크 로그: `v04/SMOKE-CHECK.json`.
