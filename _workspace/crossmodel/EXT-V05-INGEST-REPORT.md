# EXT v0.5 Ingest Report — TRUE-Divergence 라운드 (necessity-NEEDED 입증)

> 작성 2026-06-27 · 수급: 정욱님 relay (6런타임) · 분석: 진행자(Claude)
> 입력: `_workspace/crossmodel/v05_div/submissions/` (6/6 preflight PASS, distinct weights 6)
> 재현: `preflight.py` → `ingest_app_golden.py --dir v05_div` → `corpus_discount.py --dir v05_div`

---

## 0. 한 줄 결론

**R5c의 음성을 닫았다.** Class C(자유 파라미터) 6런타임이 전부 다른 값을 골라 **DIVERGENT** →
단일출처면 임의 거짓봉인됐을 것을 consensus 가 정당 거부 = **necessity-NEEDED 입증(airtight)**.
부수로 (1) **정본 corpus-상관 ρ = 0.0** (R5c 의 오염된 상한 1.0 을 정정), (2) Class D 의 **3-3 convention
split**(`split_ry_dir`) 이 `establish_truth` 의 near-tie 임의봉인 결함을 **실증** → 이번 턴에 추가한
**contested guard** 가 이를 CONTESTED 로 정확히 차단.

> **정정(2026-06-27)**: 본 보고서 초판은 `split_csqrtz_sign` 을 3-3 으로 잘못 기재했다. 직접 hash 검증
> (gemini M[3,3]=+i, declared 6/6 일치) 결과 실제는 **4-2**(ESTABLISHED). 진짜 3-3 동률은
> `split_ry_dir` 하나다. 오라클 hash 결정성은 10/10 재확인(결정론 이상 없음).

---

## 1. Class C — free parameter: DIVERGENT (necessity *NEEDED*) ✅

| intent | 6런타임 선택 | distinct | 판정 |
|---|---|---|---|
| free_cphase | φ = 1.885, 0.449, 2.718(e), 2.847, 1.942, 1.414(√2) | **6/6** | **DIVERGENT** |
| free_rz | θ = 1.732(√3), 1.618(φ), 2.718(e), 1.047(π/3), 0.898, 1.156 | **6/6** | **DIVERGENT** |

- 의도에 유일 정답이 없으므로(자유 연속각) 6 weights 가 전부 다른 값 → max 독립합의 1 < N=2 → DIVERGENT.
- **의미**: 단일-소스 파이프라인이라면 6개 서로 다른 임의 유니터리 중 하나를 "정답"으로 봉인했을 것.
  consensus 는 수렴 없음을 감지하고 봉인 거부 → escalate-to-clarify. **R5c 가 못 만든 necessity 증거를
  구조적으로 확보**(의도가 under-determined → 발산은 우연이 아니라 설계 귀결).
- skeptical 감사: 값들이 e·√2·√3·φ·π/3 등 "그럴듯한" 상수지만 **서로 다른** 상수 = 담합 없는 독립 자유선택.
  6/6 충돌 0.

## 2. Class S — sanity_cz: ESTABLISHED 만장일치 ✅

- 6/6 수렴, key=`8d39767cd8c3` (= cross-model 봉인 `cz` 게이트 키와 동일값). probe 가 무차별 발산이 아니라
  **잘 정의된 의도엔 정상 수렴**함을 확인. (id 가 등록앱이 아니라 reference-match 표기는 "없음".)

## 3. Class D — convention split: 진짜 분기 실측 + 엔진 결함 실증 ⚑

| intent | 분포(독립단위) | 캠프 | guard 적용 후 | 비고 |
|---|---|---|---|---|
| split_rz_sign | 4-2 | "−": gemini,gpt-5,kimi,qwen / "+": deepseek,grok | ESTABLISHED("−") + dissent 2 | 정당 다수 |
| split_ry_dir | **3-3** | "+": deepseek,kimi,qwen / "−": gemini,gpt-5,grok | **CONTESTED** (guard 차단) | 진짜 동률 |
| split_csqrtz_sign | 4-2 | "+": gemini,gpt-5,grok,qwen / "−": deepseek,kimi | ESTABLISHED("+") + dissent 2 | 정당 다수 |

- distinct-weight 모델들이 회전 부호·controlled-√Z 근 **convention 에서 실제로 분기**(R5c 의 만장일치
  Schelling 과 대조). 캠프 구성이 의도마다 달라(예: ry_dir 의 "+"={deepseek,kimi,qwen} ≠ csqrtz 의
  "+"={gemini,gpt-5,grok,qwen}) **고정 계보가 아님** = 의도별 독립 convention 선택. declared_reading 6/6 정직.
- **엔진 결함 실증(중요)**: `split_ry_dir` 의 **3-3 동률**에서 (guard 이전) `establish_truth` 가 `max()` 로
  한쪽을 임의 선택해 ESTABLISHED 로 봉인했다 — v0.5 스모크가 예측한 near-tie 맹점이 **가설이 아니라 실제로
  발생**. → 이번 턴에 **contested guard 정식화**(top-2 독립단위 동률 → CONTESTED). 재ingest 결과
  `split_ry_dir` 가 정확히 **CONTESTED** 로 차단됨(4-2 들은 정당히 ESTABLISHED 유지). frozen 15키 불변
  (`scripts/verify_contested_guard.py` 20/20).

## 4. 정본 corpus-상관 ρ = 0.0 (R5c 상한 1.0 정정) ✅

- 추정 대상(정답부재) 5의도: free 2개 distinct=6, split 3개 distinct=2(3-3/4-2). chance-corrected
  pairwise agreement → **ρ = 0.0**.
- **R5c(ρ=1.0, 상한) vs v0.5(ρ=0.0, 정본)** — 이 대비가 핵심 발견:
  R5c 의 "완전 상관"은 **정확성에 의한 수렴(Schelling 정답)** 이 corpus 상관으로 *오인*된 것.
  정답이 진짜 없을 때 frontier 모델들은 **독립적으로 선택(ρ≈0)** 한다 → cross-model 독립성 가정이
  (적어도 자유선택 축에서) **실측으로 옹호됨**. R-I 의 corpus-상관 우려는 깨끗이 측정하면 작다.
- 효과: ρ=0 이므로 model-only 합의는 강등 없음(MULTIMODEL 유지). corpus-discount 메커니즘은 정확히
  구현됐고, **자유선택 축에선 할인할 상관이 없음**을 정량 확인. (단, Class D 는 상관이 아니라 *bimodal
  분기* — 다른 문제이며 contested guard 로 다룸.)

---

## 5. 종합 — 무엇이 입증/실측/정정되었나

1. **입증**: KeyFreeConsensus necessity-NEEDED (Class C 발산). R5c 음성 종결.
2. **실측**: distinct-weight 모델의 convention 분기(Class D: rz 4-2, ry 3-3, csqrtz 4-2) — 텍스트북-인접이라도 부호 convention 은 갈린다.
3. **실증→해결**: `establish_truth` near-tie 임의봉인 결함(split_ry_dir 3-3) 실증 → **contested guard 정식화**로 CONTESTED 차단. frozen 키 불변 보증(20/20).
4. **정정**: corpus-상관 ρ = 0.0 (정본). R5c 의 1.0 은 정확성 혼입 상한이었음.
5. **자가정정**: 초판 csqrtz 3-3 오기 → 실제 4-2 (직접 hash 검증). 오라클 hash 결정성 10/10 재확인.

## 6. contested guard — 이번 턴 구현 (정욱님 승인 완료)

- `consensus.py establish_truth`: top-2 독립단위 동률(runner_up==winner) → `CONTESTED`(봉인 거부, escalate).
  단일-그룹 수렴(frozen 키 빌드 경로 runner_up=0)은 미발동 → **결정론 불변**.
- 검증: `scripts/verify_contested_guard.py` — frozen 15키 status/key/grade 불변 + guard 단위테스트
  (단일/4-2/3-2-1→ESTABLISHED, 3-3/2-2→CONTESTED) **20/20 PASS**. 회귀: smoke 19/19·second_oracle 18/18·
  v04 4/4·v04_hard 6/6 불변. (frozen 파일 재생성 없이 메모리상 보증 — 봉인점검 교훈 준수.)
- corpus-discount: ρ=0 정본이므로 봉인경로 적용 불요(현 분석전용 유지가 정직).

## 7. 산출/재현

- 리포트: `v05_div/APP-CONSENSUS-REPORT.json` (audit 포함) · `v05_div/CORPUS-RHO.json`.
- 봉인 불변: registry 무변경(probe 는 대조/측정만). 결정론 유지.
