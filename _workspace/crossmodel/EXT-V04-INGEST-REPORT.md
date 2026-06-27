# EXT v0.4 Ingest Report — Cross-Model 6런타임 수급 결과

> 작성 2026-06-27 · 수급: 정욱님 relay (golden 6 · bloq 6 · hard 5) · 분석: 진행자(Claude)
> 입력: `_workspace/crossmodel/v04/submissions{,_bloq}/` · `v04_hard/submissions/`
> 재현: `ingest_app_golden.py --dir v04` · `ingest_app_bloq.py --dir v04` · `ingest_app_golden.py --dir v04_hard`

---

## 0. 한 줄 결론

R5a/R5b는 **완전 성공**(앱 의도·구현 양층 key-free, 봉인 8/8 byte 일치). R5c는 **부분 성공이자 정직한
음성 결과**: Class A(hard well-defined) 3/3 확립으로 *off-textbook 동작*을 입증했으나, Class B(ambiguous)는
설계 기대였던 **발산이 일어나지 않았다** — 5개 이종 weights가 공유하는 Schelling default 때문. 발산-필요성
논증은 미입증으로 남기고, 그 원인 자체를 발견으로 기록한다.

---

## 1. R5a — App-Golden (v04), 앱 의도 key-free

| app | status | grade | votes | 봉인앱 대조 |
|---|---|---|---|---|
| iqft7 | ESTABLISHED | MULTIMODEL | 6 | ✓ 일치 |
| cmul2_mod21 | ESTABLISHED | MULTIMODEL | 6 | ✓ 일치 |
| cmul4_mod21 | ESTABLISHED | MULTIMODEL | 6 | ✓ 일치 |
| cmul16_mod21 | ESTABLISHED | MULTIMODEL | 6 | ✓ 일치 |

- **4/4 ESTABLISHED · MULTIMODEL · 봉인앱 일치 4/4.** 6개 이종 런타임(deepseek·gemini·gpt-5·grok·kimi·qwen)이
  앱 전체 유니터리를 독립 author → 동일 u_hash 수렴 → 내가 봉인한 분해와 byte 일치.
- 의미: 게이트뿐 아니라 **앱 의도(iqft7, N=21 modular multiplier 3종)까지 key-free 승격**. golden·proof·
  cross-model 삼중 삼각측량 성립.

## 2. R5b — App-Bloq (v04), 구현 독립 교차검증

| app | status | votes | 수렴 회로 depths | 봉인앱 대조 |
|---|---|---|---|---|
| iqft7 | ESTABLISHED MULTIMODEL | 4 | [31] | ✓ 일치 |
| cmul2_mod21 | ESTABLISHED MULTIMODEL | 6 | [36, 255, 297, 403, 2996] | ✓ 일치 |
| cmul4_mod21 | ESTABLISHED MULTIMODEL | 6 | [0, 30, 218, 252, 332, 806] | ✓ 일치 |
| cmul16_mod21 | ESTABLISHED MULTIMODEL | 6 | [0, 30, 184, 252, 332, 1612] | ✓ 일치 |

- **4/4 ESTABLISHED · 봉인앱 일치 4/4.** 서로 다른 깊이의 독립 회로가 같은 u_hash로 수렴 = 구현 독립 검증.
- **B4 저항 실증**: deepseek·qwen이 cmul2/4/16에서 잘못된 유니터리를 산출했으나(dissent), 올바른 4개
  distinct-weights가 다수로 MULTIMODEL 확립 → 오구현이 합의를 오염시키지 못함. (잘못된 소수 배제가 정상 동작.)

## 3. R5c — Hard-Intent Divergence Probe (v04_hard), 5런타임 (qwen 미제출)

분포는 **6/6 전부 ESTABLISHED MULTIMODEL, 만장일치(votes=5, 단일 u_hash)**.

### 3A. Class A — hard-but-well-defined (필요성: *작동함*) ✅ 입증

| intent | dist | 판정 |
|---|---|---|
| hard_cy (controlled-Y) | {key:5} | ESTABLISHED |
| hard_sqrtswap (√SWAP) | {key:5} | ESTABLISHED |
| hard_perm3 (비교과서 3q 순열 (1 2 4)(3 6)) | {key:5} | ESTABLISHED |

→ 교과서에 없는 커스텀 순열·√SWAP·controlled-Y를 5개 이종 weights가 만장일치 확립.
**메커니즘이 off-textbook 진리를 세운다는 필요성(WORKS)은 입증됨.**

### 3B. Class B — deliberately under-specified (필요성: *필요함*) ✗ 미입증 (정직한 음성)

설계 기대 = **발산**(DIVERGENT). 실제 = **전부 만장일치 수렴**. 원인은 construction_method가 드러낸다:

| intent | 5개 모델이 고른 default | 발산 여부 |
|---|---|---|
| amb_cphase | **전원 CZ** (θ=π, diag(1,1,1,-1)) | 없음 |
| amb_cnot_endianness | **전원 control=q0/MSB** big-endian | 없음 |
| amb_iqft2_bitrev | **전원 RAW (no bit-reversal)** | 없음 (단, 주석 참조) |

- **핵심 음성 결과**: 내가 고른 "모호함"은 사실 **이종 weights가 공유하는 강한 Schelling default**를 가져,
  단일 모델이 임의 default를 봉인하는 위험을 *재현하지 못했다*. 따라서 "발산이 필요성을 증명한다"는 논증은
  **이 라운드로 입증되지 않았다.** (음성을 그대로 기록 — 스핀 금지.)

- **주목할 단일 데이터포인트 (gemini, amb_iqft2_bitrev)**: gemini는 construction_method에서 *말로는*
  "swap/bit-reversal 포함"(발산 reading)이라 선언했으나, **실제 제출 행렬은 RAW(no-swap)** 로 나머지 4개와
  동일했다 (직접 대조 검증: raw≠swap 확인, gemini matrix==raw). → **prose/matrix 모순**. 봉인 대상인
  *행렬*은 수렴했고 *서술된 추론*만 갈렸다. 단일-소스 파이프라인이 prose를 읽었다면 다른 것을 봉인했을 것 —
  consensus가 matrix를 본다는 점이 오히려 안전 쪽으로 작동.

---

## 4. 정직한 해석 (skeptical audit)

1. **입증된 것**: (a) 앱 의도·구현 양층의 cross-model key-free (R5a/R5b 8/8 byte 일치), (b) B4 오구현
   배제(R5b deepseek/qwen), (c) 메커니즘의 off-textbook 작동(R5c Class A 3/3).
2. **미입증된 것**: KeyFreeConsensus의 **divergence-기반 necessity** (R5c Class B). 발산이 안 났으므로
   "합의가 임의 default를 잡아낸다"는 주장은 이 데이터로 뒷받침되지 않는다.
3. **발견(원인)**: distinct-weight 모델들은 **강한 공유 convention prior(Schelling point)** 를 가져,
   교과서-인접 under-specified 의도조차 수렴한다. 이는 임의 거짓봉인을 유도하기가 probe 가정보다 *어렵다*는
   점에서 cross-model 봉인 강건성에 유리하지만, "necessity-NEEDED" 논증과는 별개다.
4. **후속 제안**: 진짜 발산을 보려면 Class-B 의도가 **공유 prior가 없는 선택**을 겨냥해야 한다 — 자유
   연속 파라미터, 또는 학습 코퍼스가 실제로 ~50/50 갈리는 convention. 이것이 어렵다는 사실 자체가 본 발견.
   추가로 gemini 사례는 **prose vs matrix 일관성 점검**을 ingest에 비파괴 필드로 추가할 가치를 시사한다.

---

## 5. 산출/재현

- 리포트(자동): `v04/APP-CONSENSUS-REPORT.json` · `v04/APP-BLOQ-REPORT.json` · `v04_hard/APP-CONSENSUS-REPORT.json`
- 봉인 불변: registry/apps·modules 무변경(대조만). 결정론 유지.
