# EXT 운영 안내 — v0.5 진짜-발산 라운드 (정욱님용)

> 목적: R5c(v04_hard)가 못 만든 KeyFreeConsensus **necessity-NEEDED** 증거를 확보하고, **정본 corpus-상관 ρ**
> 를 측정한다. 본 진행자가 brief·intents·붙여넣기 프롬프트·preflight·ingest 를 준비·스모크검증(19/19)했고,
> **배포·수급은 정욱님**, 결과 모이면 본 진행자가 preflight→ingest.
> 6런타임 = `gpt-5 · gemini · grok · kimi · qwen · deepseek` (이전 라운드와 동일 distinct-weights).

---

## 왜 이 라운드인가 (한 줄)

R5c의 "모호" 의도는 유일한 Schelling 정답(CZ, control=first, raw)이 있어 6모델이 만장일치 수렴 → 발산 실패.
v0.5 **Class C(free continuous parameter)** 는 의도 자체에 정답이 없어, 단일소스는 임의값을 봉인할 수밖에 없고
consensus 는 정당하게 거부(DIVERGENT) → necessity 가 **구조적으로** 증명된다.

## 패키지 (단일 라운드, golden only)

| 항목 | 경로 |
|---|---|
| 붙여넣기 프롬프트(★ 정욱님 핵심) | `v05_div/PROMPT-v05.md` |
| 브리프(상세) | `v05_div/DIVERGENCE-BRIEF.md` |
| 의도 정의 | `v05_div/app_intents.json` |
| 제출 템플릿 | `v05_div/SUBMISSION-TEMPLATE.json` |
| 제출 위치 | `v05_div/submissions/<runtime>.app.json` |
| 형식검증(수급 후) | `v05_div/preflight.py` |
| 스모크 결과 | `v05_div/SMOKE-CHECK.json` (19/19) |

## 정욱님이 할 일 (3단계)

**1. 배포** — `PROMPT-v05.md` 안의 `=== PROMPT START ===`~`=== PROMPT END ===` 전체를 **6런타임 각각에
그대로** 붙여넣는다(6개 모두 동일 프롬프트). 격리 규칙: 런타임끼리 서로의 응답·sealed 파일을 보이지 말 것.

**2. 수급** — 각 런타임의 JSON 응답을 아래 파일명으로 저장하고, 파일 안 `runtime`/`weights_id` 두 필드를 표대로 확정:

| 저장 파일 (`v05_div/submissions/`) | runtime | weights_id |
|---|---|---|
| `gpt-5.app.json` | `gpt-5` | `openai-gpt-5` |
| `gemini.app.json` | `gemini` | `google-gemini-3.5-flash-high` |
| `grok.app.json` | `grok` | `xai-grok` |
| `kimi.app.json` | `kimi` | `moonshot-kimi` |
| `qwen.app.json` | `qwen` | `alibaba-qwen` |
| `deepseek.app.json` | `deepseek` | `deepseek-v4-pro` |

**3. 자체 형식검증(선택, 권장)** — 배치 후:
```
python _workspace/crossmodel/v05_div/preflight.py
```
"ALL PASS — ingest 가능" 이 나오면 완료. 오류가 나오면 해당 런타임에 재요청(특히 모델이 JSON 외 prose 를
섞었거나 행렬이 비유니터리/모양 불일치인 경우). **5개 이상**(distinct weights ≥2면 동작하나 6 권장) 모이면 충분.

> Class C 강조: 런타임이 free_cphase/free_rz 에서 "안전하게" 표준값(π 등)으로 도망가면 발산 측정이 무력화됨.
> 프롬프트에 이미 "commit to a genuine free pick" 을 강하게 넣어두었으나, 응답이 전부 같은 값이면 본 진행자가
> 보고서에 그대로(=공유 prior 강함) 기록한다.

## 결과 모이면 (본 진행자가 실행)

```
python _workspace/crossmodel/v05_div/preflight.py            # 형식 최종확인
python .pgf/keyfree/ingest_app_golden.py --dir v05_div       # 합의 + READING AUDIT
python scripts/corpus_discount.py --dir v05_div              # 정본 ρ 추정
```

## 기대 판정 (성공 기준)

- **Class C** (`free_cphase`, `free_rz`): **DIVERGENT**(max 독립합의 < 2) → 단일출처면 임의 거짓봉인됐을 것을
  consensus 가 차단 = **necessity-NEEDED 입증**(R5c 가 못한 것). 발산이 곧 성공.
- **Class D** (`split_rz_sign`, `split_ry_dir`, `split_csqrtz_sign`): **실측** — DIVERGENT / ESTABLISHED+dissent
  (실제 분기, 다수확립) / 만장일치(공유 default) 중 무엇이든 데이터. READING AUDIT 가 contested near-tie 와
  prose/matrix 모순(gemini형)을 자동 플래그.
- **Class S** (`sanity_cz`): **만장일치 ESTABLISHED** — 메커니즘이 정상 동작함을 확인(probe 가 무차별 발산 아님).
- **정본 ρ**: Class C 자유선택의 chance-corrected 일치율 → corpus-상관 ρ(R5c 의 상한 1.0 을 정본으로 대체).
