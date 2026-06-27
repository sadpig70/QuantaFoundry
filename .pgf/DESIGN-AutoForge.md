# DESIGN — AutoForge (자율 멀티페르소나 봉인 파운드리)

> PGF design mode 산출물 · @v:0.1 · 루트 = `D:\QuantaFoundry`
> 의존: QPGF 오라클(`.agents/skills/qpgf-oracle/`, v0.1.0, 157 green) — **사용만**(복제 금지).
> 정체성: *봉인 못 통과한 산출물은 존재하지 못한다.* 검증은 결정론 오라클에만 맡긴다.

---

## 0. 목적

QuantaFoundry 3대 기능(**생성 → 검증·보관 → 재조립**)을 **사용자 개입 없는 자율 ADP 루프**로
돌린다. 자율화의 마지막 걸림돌이던 CrossGen의 **cross-model 작성자 격리**(사람 Courier 필요)를
**PGF 멀티페르소나(독립 에이전트 컨텍스트) 격리**로 대체한다.

신뢰 근거: 베이스 모듈은 **수학적 정답키**가 존재 → 두 페르소나가 동반오류를 내도 `u_hash ≠ 정답키`
로 오라클이 거부. 따라서 정답키 보증 구간에서 cross-persona 격리는 cross-model 대비 **신뢰 손실 0**.

---

## 1. Gantree

```
AutoForge // 자율 멀티페르소나 봉인 파운드리 (in-progress) @v:0.1
    F1_Generate // 기능1: AI 격리 생성 (in-progress)
        PersonaG // golden 작성자 페르소나 (in-progress)
        PersonaB // bloq 작성자 페르소나 (in-progress)
        PersonaA // adversary (정답키 부재 구간 전용, C에선 비활성) (designing)
        Isolation // Agent 컨텍스트 격리 — G/B 상호 미열람 (in-progress)
    F2_VerifySeal // 기능2: 결정론 검증 + 봉인 + 보관 (in-progress)
        Combine // golden+bloq 결합 → 단일 .pg (in-progress)
        Oracle // verify_seal 호출 (오라클 사용만) (done) @dep:Combine
        AnchorKey // u_hash ↔ 정답키 대조 (anti-swap) (in-progress) @dep:Oracle
        Register // registry INV1~3 등록 (in-progress) @dep:AnchorKey
    F3_Compose // 기능3: 봉인 모듈 재조립 (다음 스레드) (designing)
    ADPLoop // 자율 실행 루프 (AI_SelfAct) (in-progress)
        # input: module_queue: list[IntentCard]
        # process: 각 intent → F1 → F2 → (충분히 쌓이면) F3 → 루프백
        # criteria: 사람 개입 0, 종료는 오라클 exit code로만 결정
    AnswerKeySeed // 8개 베이스 정답키 확정 (사람 1회 seed) (done)
```

> 깊이 5레벨 이내, 순환 @dep 없음. PersonaA·F3_Compose는 (C) 스레드에서 designing(비활성),
> 후속 스레드에서 활성.

---

## 2. PPR — 핵심 노드

### 2.1 F1_Generate — 멀티페르소나 격리 생성

```python
def generate_isolated(intent: IntentCard) -> tuple[Path, Path]:
    """같은 intent로부터 golden·bloq을 서로 못 보는 두 페르소나가 격리 생성.
    격리 = 별도 Agent 컨텍스트(부모만 양쪽을 봄). cross-model의 컨텍스트 격리와 동등."""
    # [parallel]  ← 두 Agent는 독립·상호 미열람
    golden_pg = AI_make_author(persona="persona-golden", intent=intent)  # id=golden + meta
    bloq_pg   = AI_make_author(persona="persona-bloq",   intent=intent)  # id=bloq   + meta
    # [/parallel]
    # acceptance_criteria:
    #   - golden 작성자는 bloq을 미수신, bloq 작성자는 golden을 미수신 (동반오류 차단)
    #   - 각 산출은 정확히 지정 fenced 블록만 포함
    write(f"submissions/golden/{intent.id}.pg", golden_pg)
    write(f"submissions/bloq/{intent.id}.pg",   bloq_pg)
    return golden_pg_path, bloq_pg_path
```

### 2.2 F2_VerifySeal — 결합·봉인·정답키·등록

```python
def verify_and_seal(intent_id: str, gp: Path, bp: Path, store: Path) -> SealResult:
    """결정론 구간 — AI 개입 없음. crossgen 패턴 재사용, 오라클은 사용만."""
    text, cid = combine(gp, bp)          # intent(id/n_sys/n_anc) 정합 검사 포함
    rc = verify_seal.main([tmp(text), "--out", str(store)])   # exit 0 ⟺ sealed.json
    if rc != 0:
        return SealResult(status="REPAIR", signal=oracle_stderr)   # C4 등 → 페르소나 재생성
    sealed = load(store / f"{cid}.sealed.json")
    if ANSWER_KEY.get(cid) and sealed.u_hash != ANSWER_KEY[cid]:
        return SealResult(status="REJECT", stage="anti_swap")      # 바꿔치기 거부
    registry_register(sealed)            # INV1: 검증통과만 등록
    return SealResult(status="SEALED", u_hash=sealed.u_hash)
    # acceptance_criteria:
    #   - exit 0 ⟺ <id>.sealed.json 존재
    #   - 동일 입력 재봉인 → byte-identical (결정론)
    #   - u_hash == 정답키 (신규는 seed가 곧 정답키)
```

### 2.3 ADPLoop — 자율 실행 (AI_SelfAct)

```python
def AI_SelfAct(queue: list[IntentCard], store: Path) -> ForgeReport:
    """사용자 개입 없는 한 사이클. 종료/반복은 오라클 결과로만 결정 — AI 자기선언 없음."""
    results = []
    for intent in queue:
        for attempt in range(MAX_REPAIR):
            gp, bp = generate_isolated(intent)          # F1 (격리)
            res = verify_and_seal(intent.id, gp, bp, store)   # F2 (결정론)
            if res.status == "SEALED":
                break
            if res.status == "REPAIR":
                intent = relay_signal(intent, res.signal)  # C4 신호 중계 → 재생성
        results.append(res)
    # if enough(registry): compose_new(registry)   # F3 (후속 스레드)
    return ForgeReport(results)
    # acceptance_criteria:
    #   - 8/8 SEALED, 전부 cross_independent(golden작성자≠bloq작성자)
    #   - 사람 개입 0
```

---

## 3. 베이스 모듈 8개 (정답키 확정 완료)

| id | n_sys | tier | golden(해석적) | u_hash(정답키, 앞16) | 출처 |
|---|---|---|---|---|---|
| x_gate | 1 | 0 | [[0,1],[1,0]] | 7dc1df52d07dd742 | seed |
| z_gate | 1 | 0 | diag(1,-1) | 1e3c0f2fa747f4fa | seed |
| h_gate | 1 | 0 | [[1,1],[1,-1]]/√2 | 0d6a0b7a9a19ad2e | seed |
| cnot | 2 | 0 | 4×4 CX(big-endian) | 3913bcef764f36b8 | seed |
| swap2 | 2 | 0 | 4×4 swap | e6255e2f105a9782 | QPGF 일치✓ |
| toffoli | 3 | 0 | 8×8 CCX | e663b43043af6b78 | QPGF 일치✓ |
| qft2 | 2 | 0 | 4×4 DFT | 90dbc731bb8c7e80 | seed |
| qft3 | 3 | 0 | 8×8 DFT | 340b5f344fae9b99 | QPGF 일치✓ |

> swap2·toffoli·qft3 = QPGF v0.1.0 정답키와 **byte 일치 재현**(결정론 교차검증). 신규 5개는
> 사람 1회 seed로 확정(`AnswerKeySeed`, done). 컨벤션: Qualtran-native raw big-endian, golden atol 1e-7.

---

## 4. 신뢰 경계 (정직)

- **cross-persona가 막는 것**: 동일 컨텍스트 동반오류 → cross-model과 동등(완전 차단).
- **cross-persona가 약한 것**: 동일 가중치 체계적 오해 → 정답키가 있는 (C)에선 무력화.
- **정답키 없는 구간**(후속, 첫 진리 확정): PersonaA(adversary) 다수결 또는 사람 1회 seed로 보강.
- **경계 규율**: 봉인 못 통과 = 미존재. 검증은 오라클(결정론)에만. 페르소나는 *생성*만, *판정 불가*.

---

## 5. 완료 기준 (acceptance)

1. 8/8 모듈 SEALED, u_hash == 정답키.
2. 전부 cross_independent (golden 작성자 페르소나 ≠ bloq 작성자 페르소나).
3. byte-identical 재봉인 재현.
4. registry/modules/ 에 8개 등록 (INV1~3).
5. 사람 개입 0 (ADPLoop 자율 실행).
