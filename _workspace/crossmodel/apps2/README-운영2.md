# Cross-Model Round 4 — 앱 의도(golden) + 앱 구현(bloq) 운영 가이드

게이트(Round 1-2)에 이어 **앱 계층까지** cross-model로 닫는다. 두 갈래:
- **app-golden**: 런타임이 앱의 *전체 유니터리*(의도)를 독립 작성 → 봉인 앱과 대조 (§9.8 in-house 의도 갭 해소)
- **app-bloq**: 런타임이 봉인 게이트로 *독립 회로*(구현)를 작성 → 조립 유니터리가 봉인 앱과 일치하는지 (구현 측 동반오류 방화벽)

대상(알고리즘 계층 7앱): `iqft2 · iqft3 · cmul2_mod15 · cmul4_mod15 · qpe_s · qpe_t · shor15_a2`
(나머지 앱은 골든이 이미 cross-model된 게이트/QFT와 동일하거나 Tier-1 structural이라 제외.)

---

## A. app-golden 라운드

### 런타임에 줄 파일 (`_workspace/crossmodel/apps2/`)
| 파일 | 역할 |
|---|---|
| `APP-GOLDEN-BRIEF.md` | 앱 전체 유니터리 작성 지시(영문) |
| `app_intents.json` | 7앱 정밀 사양 |
| `SUBMISSION-TEMPLATE-golden.json` | 제출 형식(iqft2 예시) |

### 한 줄 지시 (복붙)
> Read `APP-GOLDEN-BRIEF.md` and `app_intents.json`. For each app author the full unitary `U[out,in]`
> from the spec (big-endian, qubit0=MSB/control), independently. Return `<your-name>.app.json` per the
> template. No peeking at decompositions/answers.

### 수거 → 합의
1. `<name>.app.json` → `_workspace/crossmodel/apps2/submissions/`
2. `python .pgf/keyfree/ingest_app_golden.py --dir apps2`
   → `⟺sealed-app:✓일치` = 내 앱 의도가 cross-model 합의와 byte 일치 (앱 의도 key-free).

## B. app-bloq 라운드

### 런타임에 줄 파일
| 파일 | 역할 |
|---|---|
| `APP-BLOQ-BRIEF.md` | 봉인 게이트로 독립 회로 작성 지시 |
| `GATE-VOCABULARY.json` | 사용 가능한 봉인 게이트 15종(이름·큐비트수·규약) |
| `app_intents.json` | 같은 7앱 사양(재사용) |
| `SUBMISSION-TEMPLATE-bloq.json` | 회로 제출 형식 |

### 한 줄 지시 (복붙)
> Read `APP-BLOQ-BRIEF.md`, `GATE-VOCABULARY.json`, `app_intents.json`. For each app author an
> independent circuit (gate list with targets) using ONLY the vocabulary gates (first target =
> control). Return `<your-name>.bloq.json` per the template. No copying any decomposition.

### 수거 → 검증
1. `<name>.bloq.json` → `_workspace/crossmodel/apps2/submissions_bloq/`
2. `python .pgf/keyfree/ingest_app_bloq.py --dir apps2`
   → 각 회로를 봉인 게이트로 조립 → u_hash. *서로 다른 회로*가 같은 u_hash·봉인 앱 일치면 구현 독립 확립.
   `dissent` = 그 회로가 잘못된 유니터리 산출(구현 오류 탐지).

## 검증 상태
- 두 파이프라인 mock 스모크 통과: app-golden 7/7 일치, app-bloq 7/7 일치 + 오류회로 dissent 정확 탐지.
- 실제 6런타임 제출만 채우면 곧바로 합의. weights_id 는 런타임별로 달라야 함(독립단위).

## 의미
완료 시 **게이트(진리+구현) + 앱(의도+구현)** 전 계층이 cross-model — 사람/orchestrator 단독 작성이
체인 어디에도 남지 않는다.
