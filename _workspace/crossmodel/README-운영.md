# Cross-Model 합의 — 운영 가이드 (정욱님용)

6개 런타임(codex · gemini · grok · kimi · qwen · deepseek)에게 **독립적으로** golden 행렬을
author 시켜, 서로 다른 weights가 같은 u_hash에 수렴하면 그 해시를 **인간 정답키 없이** 진리로
확립한다. 이것이 KeyFreeConsensus의 마지막 빈칸(진짜 cross-model)을 채운다.

## 무엇을 각 런타임에 주나 (3개 파일)

| 파일 | 역할 | 런타임에 전달 |
|---|---|---|
| `RUNTIME-BRIEF.md` | 작업 지시·규약(영문) | ✅ 그대로 |
| `intents.json` | 만들 게이트 15종 목록 | ✅ 그대로 |
| `SUBMISSION-TEMPLATE.json` | 제출 형식 예시 | ✅ 그대로 |

**6개 런타임 모두에게 같은 3개 파일을 준다.** 단, 서로의 답을 보여주지 말 것(독립성이 핵심).

## 각 런타임에게 줄 한 줄 지시 (복붙용)

> Read `RUNTIME-BRIEF.md` and `intents.json`. For every intent, author the golden unitary
> `U[out,in]` (big-endian, first register = MSB / control) from its standard definition —
> independently, without looking up any answer key or other runtime's output. Return one file
> `<your-model.submission.json` in the format of `SUBMISSION-TEMPLATE.json`, with one entry per
> intent. Honesty over guessing.

(런타임명은 codex / gemini / grok / kimi / qwen / deepseek 중 본인 것)

## 결과 수거 → 합의

1. 각 런타임이 돌려준 `<name>.submission.json` 을 모두
   `_workspace/crossmodel/submissions/` 에 넣는다. (예: `gemini.submission.json`)
2. 합의 실행:
   ```
   python .pgf/keyfree/ingest_crossmodel.py
   ```
   - 행렬 + golden_code 재현까지 검증. 코드 재실행을 건너뛰려면 `--no-exec`.
3. 결과: 콘솔 표 + `_workspace/crossmodel/CONSENSUS-REPORT.json`.

## 결과 읽는 법

- **Round A (calib=✓)**: 그 런타임의 규약(endianness 등)이 우리와 정렬됐다는 증거.
  `calib=✗` 또는 `dissent` 가 뜨면 그 런타임의 Round B 표는 의심.
- **Round B (ESTABLISHED / MULTIMODEL)**: 서로 다른 weights ≥2가 수렴 → **신규 진리 확립**.
  `GT=✓` 는 독립 ground-truth(formal-spec/proof)와도 일치 = 동반오류 아님.
- **dissent 줄**: 다수와 다른 해시를 낸 런타임을 짚어줌(규약 오해/유도 오류 진단).
- **DIVERGENT**: 독립 단위 2개 미만 수렴 — intent 정제 또는 런타임 추가 필요.

## 확립 후 — Round 1 완료 상태 (✅ 2026-06-26)

Round 1(golden) 6런타임 수집·검증 완료: A 8/8 calib · B 7/7 ESTABLISHED · GT 15/15.
7개 신규 키(s·t·cz·iswap·cs·ccz·qft4)를 `consensus_keys.json` 에 **frozen 등록 완료**
(cross-model 6독립 ⊕ proof, PROOF_BACKED). autoforge 가 이 키를 정답키로 자동 사용.

---

## Round 2 — bloq cross-model (다음 차례)

봉인을 완성하려면 같은 게이트의 **Qualtran 구현(bloq)** 이 필요하다. golden 작성자와 *다른*
런타임이 bloq 를 작성해야 동반오류 방화벽이 선다(오라클이 `bloq.tensor_contract()==golden` 검증).

### 런타임에 줄 파일 (Round 2)
| 파일 | 역할 |
|---|---|
| `BLOQ-BRIEF.md` | bloq 작업 지시·규약(영문) — Qualtran 0.7.0 / cirq 1.6.1 |
| `intents.json` | 같은 게이트 15종 (재사용) |

### 한 줄 지시 (복붙)
> Read `BLOQ-BRIEF.md` and `intents.json`. For every intent author a Qualtran bloq whose
> `tensor_contract()` is the gate (big-endian, first register = MSB/control, n_anc=0). Return one
> file `<your-name>.bloq.json` per `BLOQ-BRIEF.md` §6. Do not look at any golden output or answer key.

### 결과 수거 → 봉인
1. 돌아온 `<name>.bloq.json` 을 `_workspace/crossmodel/submissions_bloq/` 에 넣는다.
2. 봉인 실행 (golden작성자 ≠ bloq작성자 자동 짝):
   ```
   python .pgf/keyfree/seal_crossmodel.py
   ```
   → `registry/modules/<gate>.sealed.json` + `specs/modules/<gate>.pg` 생성, 라이브러리 8→15.
   - 스모크(스크래치) 테스트: `--registry <임시> --store <임시> --no-spec`.

> 파이프라인은 mock bloq + 실제 golden 으로 스모크 검증 완료(7/7 SEALED, 교차독립·결정론·anti-swap).
> 실제 bloq 제출만 채우면 곧바로 정식 봉인된다.

---

## Round 3 — 앱 레벨 key-free (app_golden cross-model)

게이트를 넘어 **앱의 의도(app_golden = 앱 전체 유니터리)**까지 cross-model 로 확립한다. 런타임이 앱의
표준 정의로부터 앱 전체 행렬을 독립 author → 합의 → 내가 봉인한 앱(F3) 및 cross-model 게이트와 u_hash
대조. 일치하면 **앱 의도도 사람/orchestrator seed 0** 으로 승격된다.

### 런타임에 줄 파일 (Round 3) — `_workspace/crossmodel/apps/`
| 파일 | 역할 |
|---|---|
| `APP-GOLDEN-BRIEF.md` | 앱 golden 작업 지시·규약(영문) |
| `app_intents.json` | 앱 8종 (bell·ghz3·ghz4·reflect00·diffusion·grover2·qft2·qft3) |
| `SUBMISSION-TEMPLATE.json` | 제출 형식 (bell 예시) |

### 한 줄 지시 (복붙)
> Read `APP-GOLDEN-BRIEF.md` and `app_intents.json`. For every intent author the FULL application
> unitary `U[out,in]` (big-endian, first register = MSB/control, n_anc=0) from its standard
> definition — independently, no peeking at any answer/decomposition. Return one file
> `<your-name>.app.json` per the template. Honesty over guessing.

### 결과 수거 → 합의·대조
1. 돌아온 `<name>.app.json` 을 `_workspace/crossmodel/apps/submissions/` 에 넣는다.
2. 합의 실행:
   ```
   python .pgf/keyfree/ingest_app_golden.py
   ```
   → 합의 확립 + 봉인앱/게이트와 u_hash 대조. 리포트 `apps/APP-CONSENSUS-REPORT.json`.
   - `⟺sealed-app:✓일치` = 내 분해가 cross-model 앱 의도와 일치(앱 key-free 승격).
   - `⟺sealed-gate:✓일치` = qft pipeline 의도가 cross-model 봉인 게이트와 일치(재발견).

> 파이프라인은 mock app-golden(2 정직 + 1 위상오류)으로 스모크 검증 완료: 8/8 ESTABLISHED MULTIMODEL,
> 봉인앱/게이트 8/8 일치, dissent 정확 탐지. 실제 제출만 채우면 곧바로 합의된다.

## 독립성 주의

- `weights_id` 는 런타임별로 **반드시 달라야** 한다(같으면 1 vote로 병합 — B4 방어).
- 6개는 서로 다른 벤더이므로 자연히 6 독립단위. 같은 모델을 두 번 돌리는 건 의미 없음.
- 최소 2개 독립 런타임만 수렴해도 MULTIMODEL 확립. 많을수록 견고.
