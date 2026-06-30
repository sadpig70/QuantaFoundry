# DESIGN — AutonomyLoop @v:1.0

> **목적**: 외부 런타임(codex 등) 개입 없이, Claude 단독(+ 멀티 서브에이전트 + pgf 8페르소나)이
> QuantaFoundry self-contained 작업을 **발견→설계→봉인→검증→기록**까지 자율 루프로 수행한다.
>
> **설계 철학**: 신뢰의 근원은 *내 판단력*이 아니라 **결정론 게이트의 엄격함**이다. 따라서 이 설계의
> 본질은 "똑똑한 자율 에이전트"가 아니라 **"결정론 게이트 + 명시적 정지/불변 가드로 둘러싼 루프"** 이다.
>
> **저장 규율**: 루프 *제어/메타*는 `_workspace/loop/` 에만. 봉인 산출물(registry/specs)은 기존 경로.
> registry 를 loop 폴더로 옮기면 root 가 깨진다.

---

## 0. 정직 경계 & 불변 (설계의 1급 제약)

```python
# INV1 [신뢰기반·금지아님] 결정론: 모든 봉인 byte-identical 재현. frozen 23키 재생성 안 함(자율 루프의 검증 잣대).
# INV2 [신뢰기반·금지아님] fingerprint 2파일(verify_seal.py·contracts.py)은 사용만 — 수정 시 285봉인 무효.
# INV3 self-judge 금지: 합격 판정은 reproduce_all/second_oracle/verify_seal(기계)만. AI 판정 불가.
# INV4 마스터 규율: .pgf/DESIGN-MasterRoadmap.md 에 노드 先추가 後진행. 즉흥착수 0.
# INV5 외부 3종 동기화·커밋·푸쉬 = SyncCheckpoint 가 적정시기(K라운드마다+종결시) 자율 수행
#      (C 위임, 2026-06-30 정욱님 확정). 단 verified-only: reproduce_all REPRODUCED 분만 commit/push.
# INV6 폭주 안전장치(금지 아님): 정지조건(dry/budget/frontier/guard) 없으면 루프 시작 거부.
#      자율 진행을 막지 않음 — 무한루프/자원폭주만 방지하는 자율 루프 자체의 안전장치.
# ★2026-06-30 정욱님 전면 승인: NoAutoFrontier(구 INV7) 삭제. 자율 루프는 c13x/payoff/shor3683/
#   신규클래스/커밋/푸쉬/동기화/방향선택을 스스로 진행. 신뢰기반(INV1/2)만 유지.
# ★H1 cross-runtime 봉인 가치 상실: 단독 루프는 intra-runtime 다양성일 뿐 — B4 same-weights
#     co-error 에 노출. 멀티페르소나를 "독립검증"으로 과대표기 금지. key-free 신규 primitive 는 EXT relay 유지.
# ★H2 게이트가 못 막는 영역(방향·가치·종결)은 정지조건/마스터규율/체크포인트로만 가드.
```

---

## 1. Gantree — Top Level

```
AutonomyLoop // 단독 자율 루프 (designing) @v:1.0
    Bootstrap // 초기화·불변 기준선·정지조건 검증 (designing)
        LoadState // _workspace/loop/loop_state.json 로드 or 초기화 (designing)
        SnapshotInvariants // root·fingerprint·frozen·외부3종 기준해시 스냅샷 (designing)
        StopConfigGuard // 정지조건(dry/budget) 없으면 루프 시작 거부 (designing) @dep:LoadState
    Round // 자율 1라운드 — see Round tree (decomposed) @dep:Bootstrap
    StopController // 정지조건 평가 → 루프 지속/종결 (designing) @dep:Round
    Finalize // 최종 상태 저장·요약 보고 (designing) @dep:StopController
```

## 2. Gantree — Round (decomposed, 5레벨 이내)

```
Round // 자율 1라운드 (designing) @v:1.0
    SelectNext // 후보 발견·랭킹·선택 (designing)
        Discover // discover.py + frontier_selector (결정론) (designing)
        PersonaRank // 8페르소나 blind 병렬평가(직교 lens)→점수+분산 — 다양성명세=persona_contexts.md (designing) @dep:Discover
        PickOne // 최상위 1개 or frontier-exhausted 신호 (designing) @dep:PersonaRank
    PlanNode // 마스터 규율 + 사전검증 (designing) @dep:SelectNext
        AddMasterNode // .pgf master 에 노드 先추가 (INV4) (designing)
        DesignReview // 다관점 사전검증 — Critical=0 게이트 (designing) @dep:AddMasterNode
    Implement // 봉인 사이클 — see SealCycle tree §8.1 (decomposed) @dep:PlanNode
    VerifyGate // 결정론 게이트 ∧ adversarial (designing) @dep:Implement
        MachineGate // 게이트 순서·short-circuit·롤백 — see §8.2 (decomposed)
        AdversarialVerify // N 직교 회의주의자 REFUTE — see §8.3 (decomposed) @dep:MachineGate
    GuardCheck // 불변 재확인: fingerprint 2파일·frozen 23키 byte-identical (designing) @dep:VerifyGate
    Record // HANDOFF·task_record·메모리·status·round 로그 (designing) @dep:GuardCheck
    SyncCheckpoint // 적정시기 동기화·커밋·푸쉬 (C, verified-only) (designing) @dep:Record
        DocSyncBatch // 외부 3종 batch — see §8.4 (decomposed)
        CommitDelta // 봉인 델타 커밋(브랜치·Co-Authored) — verified-only (designing) @dep:DocSyncBatch
        PushRemote // 원격 푸쉬 — 외부공개(C 위임) (designing) @dep:CommitDelta
```

---

## 3. PPR — 핵심 노드 (분기·입출력·루프·조건)

```python
State = dict   # {"round":int,"dry":int,"dry_limit":int,"budget":int,
               #  "frontier_exhausted":bool,"guard_violation":bool}
Base  = dict   # {"root":str,"fp_verify":str,"fp_contracts":str,"frozen":str,"ext_docs":dict}


def bootstrap(paths: dict) -> tuple[State, Base]:
    """루프 시작 전 1회. 불변 기준선 스냅샷 + 정지조건 검증. 실패 시 루프 시작 거부."""
    state: State = load_state(paths) or {"round": 0, "dry": 0, "dry_limit": 2,
                                         "budget": 8, "frontier_exhausted": False,
                                         "guard_violation": False}
    base: Base = {                                      # 결정론 스냅샷(실제 코드)
        "root": read_manifest_root(),
        "fp_verify": sha256(paths["verify_seal"]),
        "fp_contracts": sha256(paths["contracts"]),
        "frozen": sha256(paths["consensus_keys"]),
        "ext_docs": {p: sha256(p) for p in paths["external_three"]},
    }
    # acceptance_criteria (구조적):
    #   - dry_limit>0 and budget>0 (INV6) — 아니면 raise → 루프 시작 거부
    if not (state["dry_limit"] > 0 and state["budget"] > 0):
        raise RuntimeError("정지조건 부재 — 무한확장 위험으로 루프 거부 (INV6)")
    return state, base


def select_next(world: dict) -> Optional[dict]:
    """후보 발견 → 8페르소나 합의 랭킹 → 1개. 없으면 None(frontier-exhausted)."""
    candidates: list = run_discover(world)                       # discover.py (결정론)
    if not candidates:                                           # 분기: 고갈
        return None
    ranked = candidates → persona_rank → pick_top                # → 파이프라인
    return ranked


def persona_rank(candidates: list, common: dict) -> list:
    """후보별 8페르소나 blind 병렬평가 → 점수+분산. 다양성은 persona_contexts.md 에 *미리 고정*.
    (PERSONA_SPEC·build_persona_context·5원칙 상세 = _workspace/loop/persona_contexts.md)"""
    ranked = []
    for c in candidates:
        ctxs = [build_persona_context(c, pid, common) for pid in PERSONA_SPEC]  # 직교 lens·blind 고정
        votes = parallel([AI_assess_value(x) for x in ctxs])    # 멀티 서브에이전트 병렬
        score = AI_make_converge(votes)                         # 사역: 합의 점수
        spread = variance([v["score"] for v in votes])          # 분산: 낮으면 同調(co-error 신호)
        ranked.append({"cand": c, "score": score, "herding_flag": spread < HERDING_EPS})
    # ★H1 완화: lens 직교·blind·편향충돌(P1↔P7)로 의사-독립성↑. 단 진짜 독립 아님 — 과대표기 금지.
    #   herding_flag 선 후보는 PickOne 이 보수적 처리(추가 회의주의자/보류).
    return sorted(ranked, key=lambda r: r["score"], reverse=True)


def implement(node: dict, max_retry: int = 2) -> dict:
    """마스터 노드 先추가 후 봉인. 실패 시 공개인터페이스 보존 재설계(Failure-Strategy)."""
    add_node_to_master(node)                                     # INV4: 先추가
    seal = None
    for attempt in range(max_retry):                            # 루프: 재시도
        seal = run_seal_cycle(node)                             # 결정론 봉인(실제 코드)
        if oracle_gate(seal):                                   # INV3: 기계가 판정
            return {"sealed": True, "seal": seal}
        node = AI_redesign(node, seal["failure"],              # 추론: 내부만 재설계
                           constraint="preserve_public_interface")
    return {"sealed": False, "blocked": node}                   # 분기: 최종 실패


def verify_gate(seal: dict) -> dict:
    """결정론 게이트 ∧ adversarial. 둘 다 통과해야 verified."""
    machine = (reproduce_all() and second_oracle()             # 모두 결정론(실제 코드)
               and seal_gate_ci() and verify_contested_guard())
    votes = [AI_make_refute(seal) for _ in range(3)]           # 사역: 3 회의주의자 반증시도
    survived = sum(1 for v in votes if not v["refuted"]) >= 2   # 다수결 생존
    return {"verified": machine and survived, "machine": machine, "survived": survived}


def guard_check(base: Base, paths: dict) -> bool:
    """봉인 후 불변 재확인. 위반 = 치명 → 라운드 롤백 + 루프 중단(INV1/2).
    ※ 외부 3종은 SyncCheckpoint 관할이므로 불변 대상이 아니다(fingerprint/frozen만)."""
    fp_now = (sha256(paths["verify_seal"]), sha256(paths["contracts"]),
              sha256(paths["consensus_keys"]))
    ok = fp_now == (base["fp_verify"], base["fp_contracts"], base["frozen"])
    if not ok:
        rollback_round()                                        # 비파괴 위반 → 롤백
    return ok


def autonomy_round(world: dict, state: State, base: Base) -> dict:
    """1라운드 합성: SelectNext→PlanNode→Implement→VerifyGate→GuardCheck→Record→Stop."""
    node = select_next(world)
    if node is None:                                            # 분기: frontier 고갈
        state["frontier_exhausted"] = True
        return {"stop": True, "reason": "frontier-exhausted", "state": state}

    if not design_review(node)["critical_zero"]:               # 사전검증 게이트
        state["dry"] += 1
        return {"stop": stop_controller(state), "reason": "design-critical", "state": state}

    impl = implement(node)
    if not impl["sealed"]:                                      # 분기: 봉인 실패
        state["dry"] += 1
        return {"stop": stop_controller(state), "reason": "seal-blocked", "state": state}

    vg = verify_gate(impl["seal"])
    guard_ok = guard_check(base, world["paths"])
    if not guard_ok:                                           # 분기: 불변 위반(치명)
        state["guard_violation"] = True
        return {"stop": True, "reason": "guard-violation", "state": state}

    verified = vg["verified"]
    state["dry"] = 0 if verified else state["dry"] + 1         # dry-count 갱신
    state["budget"] -= 1
    record(node, impl["seal"], verified)                       # HANDOFF·task_record·메모리
    sync_checkpoint(state, world["cfg"], verified)             # 적정시기 동기화·커밋·푸쉬(C)
    return {"stop": stop_controller(state), "reason": "ok",
            "verified": verified, "node": node, "state": state}


def sync_checkpoint(state: State, cfg: dict, verified: bool, final: bool = False) -> dict:
    """C: 적정시기에만 발화(K라운드마다 or 종결). verified-only 로 commit/push."""
    due = final or (state["round"] % cfg["commit_every"] == 0)
    if not due:                                                # 분기: 시기 아님
        return {"synced": False}
    doc_sync_batch()                                           # 외부 3종 batch (INV5 위임)
    if verified and reproduce_all():                          # 안전게이트: verified-only
        ensure_branch()                                        # 기본브랜치면 先브랜치
        commit_delta(message=with_co_authored())              # 봉인 델타 커밋
        push_remote()                                         # 외부공개(C 위임)
    # acceptance_criteria:
    #   - reproduce_all REPRODUCED 인 상태에서만 commit/push (verified-only)
    #   - 커밋메시지 Co-Authored-By 포함 · 기본브랜치 직접커밋 금지
    return {"synced": True, "pushed": bool(verified)}


def stop_controller(state: State) -> bool:
    """정지조건 OR 결합. 하나라도 참이면 루프 종결(INV6)."""
    return (state["dry"] >= state["dry_limit"]
            or state["budget"] <= 0
            or state["frontier_exhausted"]
            or state["guard_violation"])


def run_autonomy_loop(world: dict, paths: dict) -> dict:
    """상위 until-stop 루프. bootstrap → round* → finalize."""
    state, base = bootstrap(paths)
    history: list = []
    while True:                                                # Convergence/until-stop
        out = autonomy_round(world, state, base)
        history.append((state["round"], out["reason"], out.get("verified")))
        state = out["state"]
        if out["stop"]:                                        # 정지조건
            break
        state["round"] += 1
    sync_checkpoint(state, world["cfg"], out.get("verified", False), final=True)  # 종결 시 최종 1회
    save_state(paths, state)
    return {"stopped_by": out["reason"], "rounds": state["round"] + 1, "history": history}
```

---

## 4. 상태 스키마 & 정지조건

```python
# loop_state.json
# {"round":int, "dry":int, "dry_limit":2, "budget":int,
#  "frontier_exhausted":bool, "guard_violation":bool}
# cfg: {"commit_every":int}   # SyncCheckpoint 발화 주기(K). 매라운드 커밋 남발 방지.
#
# 정지조건(4) — OR 결합, 하나라도 참이면 종결:
#   dry >= dry_limit      : 연속 무성과(설계실패/봉인실패/검증실패) — 방향 막힘
#   budget <= 0           : 라운드 예산 소진 — 정욱님 체크포인트로 복귀
#   frontier_exhausted    : discover 후보 0 — 할 일 없음
#   guard_violation       : 불변 위반 — 치명, 즉시 중단(롤백)
```

## 5. `_workspace/loop/` 파일 레이아웃

```text
_workspace/loop/
    DESIGN-AutonomyLoop.md       # 본 설계(PG)
    persona_contexts.md          # PersonaRank 다양성 극대화 명세(8페르소나 직교 컨텍스트) — 미리 고정
    sim_autonomy_loop.py         # v1 — autonomy_round 단위 시뮬(기존)
    sim_autonomy_loop_v2.py      # v2 — 전체 파이프라인 시뮬 + 시나리오 검증
    loop_state.json              # (실가동 시) 루프 상태
    rounds/round-NN.json         # (실가동 시) 라운드 로그
```
※ 봉인 산출물은 절대 여기 두지 않는다(INV: registry 경로 유지).

---

## 6. Review (자체 교차검토 — 3관점 + 리스크)

### 일관성 (내부 모순 없음)
- `stop_controller` 가 4개 정지조건을 OR 결합 — `autonomy_round` 의 모든 early-return 이 이를 호출하거나
  치명(frontier/guard)은 직접 `stop=True`. 모순 없음.
- INV3(기계 판정)이 `implement`/`verify_gate` 양쪽에서 `oracle_gate`/`reproduce_all` 로만 합격 결정 — 일관.

### 완전성 (누락 없음)
- 발견(SelectNext)→설계규율(PlanNode)→봉인(Implement)→검증(VerifyGate)→불변(GuardCheck)→기록(Record)
  →정지(StopController) 전 단계 커버.
- 실패 경로 3종(design-critical / seal-blocked / verify-fail) 모두 dry 증가로 수렴 → 무한루프 방지.
- 치명 경로 2종(frontier-exhausted / guard-violation) 즉시 종결.

### 정확성 (명세=실행 일치) — 테스트로 검증(§7)
- dry-count 가 "연속" 무성과만 카운트(성공 시 0 리셋)하는지 → 시나리오로 검증.
- guard-violation 시 budget 소진과 무관하게 즉시 멈추는지 → 검증.

### 리스크 & 완화
| 리스크 | 완화 |
|---|---|
| R1 병렬 에이전트가 registry 동시쓰기 → root 깨짐 | Implement 는 **단일 에이전트 순차** (병렬은 발견/검증만) |
| R2 self-judge 회귀 | INV3 — 합격은 기계 게이트만. AI_make_refute 는 *추가* 안전망(합격권 없음) |
| R3 무한확장(무의미 c-ladder) | StopController + 마스터 "유한 종결" 규율 + budget 체크포인트 |
| R4 cross-runtime 가치 상실(H1) | 정직 표기. key-free 신규 primitive 는 EXT relay 유지(루프 범위 밖) |
| R5 불변 손상 | GuardCheck 가 매 라운드 fingerprint/frozen byte-identical 재확인, 위반 시 롤백 |
| R6 푸쉬는 외부공개(되돌리기 어려움) | **verified-only**: reproduce_all REPRODUCED 분만 commit/push. 기본브랜치 직접커밋 금지(先브랜치). [[forward-fix-philosophy]] 정욱님 C 위임 |
| R7 매라운드 커밋 남발 | `commit_every=K` 주기 발화(매라운드 아님) + 종결 시 최종 1회 |

---

## 7. 테스트 계획 → `sim_autonomy_loop_v2.py` 매핑

```text
T1 정상 N라운드 → frontier 고갈 종결           (SelectNext 분기)
T2 design-critical → dry 증가                  (PlanNode 게이트)
T3 봉인 1차 실패 → 재설계 2차 성공             (Implement Failure-Strategy)
T4 봉인 연속 실패 → dry_limit 종결             (StopController dry)
T5 budget 소진 종결                            (StopController budget)
T6 guard-violation → budget 무관 즉시 종결     (GuardCheck 치명)
T7 verify-fail(기계OK·adversarial 탈락) → dry  (VerifyGate ∧ 조건)
T8 INV: 마스터노드=봉인시도 1:1(즉흥착수 0)    (INV4)
T9 bootstrap: 정지조건 부재 시 루프 거부        (INV6)
T10 SyncCheckpoint K=2 주기 발화               (sync due 분기)
T11 verify-fail 라운드는 commit/push 안 함     (verified-only 안전게이트)
T12 종결 시 final sync 1회 보장                (final=True)
```
각 T 는 mock world(시나리오 주입)로 `run_autonomy_loop` 를 돌려 종결사유·라운드수·불변을 assert.
registry/oracle/frozen 무접촉(전부 mock).
```

---

## 8. 정교화 — 복잡 노드 깊이 분해 (decomposed)

> 한 줄 노드 중 *실제로 복잡해 실수 위험이 큰* 4개를 원자 단위까지 분해. 검증=`sim_seal_cycle.py`.

### 8.1 SealCycle (Implement 분해) — 표준 봉인 사이클

```
SealCycle // 봉인 사이클 (designing) @v:1.0
    SubDesign // 복잡후보면 PG sub-설계(가정→노드) (designing)
    Prototype // 수치 프로토타입: golden==composite 사전확인 (designing) @dep:SubDesign
    GenFamily // scripts/*.py family generator 작성 (designing) @dep:Prototype
    SealArtifacts // QPGF 경로 봉인(module→app)·honest 분해(MatrixGate 0) (designing) @dep:GenFamily
    ForgeRegister // forge_apps APP_LIST 등록 + registry build → new root (designing) @dep:SealArtifacts
    IndepOracle // 신규모듈이면 second_oracle INDEP 추가(else skip) (designing) @dep:ForgeRegister
    SealVerdict // sealed ∧ tier ∧ deterministic-reassembly 판정 (designing) @dep:IndepOracle
```

```python
def seal_cycle(node: dict) -> dict:
    """표준 봉인 사이클. 신규모듈 분기 + honest 분해 강제. 실패는 상위 Implement for-attempt 가 받음."""
    if node["complex"]:                                   # 분기: 복잡후보 → PG sub-설계
        sub_design(node)                                  # 가정을 노드로 명시(검증시점 포착)
    if not prototype_matches(node):                       # 조건: golden==composite 선확인
        return {"sealed": False, "failure": "prototype-mismatch"}
    gen_family(node)                                      # scripts/*.py generator
    seal = seal_artifacts(node)                           # QPGF 경로(module→app)
    if seal["has_matrixgate"]:                            # honest 분해 위반 → 거부
        return {"sealed": False, "failure": "MatrixGate-detected"}
    forge_register(node)                                  # forge_apps + registry build
    if node["new_module"]:                                # 분기: 신규모듈만 INDEP
        if not second_oracle_indep(node):
            return {"sealed": False, "failure": "indep-oracle-mismatch"}
    ok = seal["sealed"] and seal["tier"] is not None and seal["deterministic"]
    return {"sealed": ok, "seal": seal}
    # acceptance_criteria:
    #   - MatrixGate 0(honest 분해) · prototype==golden 선확인
    #   - 신규모듈은 second_oracle INDEP 필수 · 기존부품 재사용은 skip
    #   - deterministic-reassembly True
```

### 8.2 MachineGate (분해) — 게이트 순서·short-circuit·롤백

```
MachineGate // 결정론 게이트 (designing)
    G1_Reproduce // reproduce_all → REPRODUCED (designing)
    G2_SecondOracle // second_oracle N/N (designing) @dep:G1_Reproduce
    G3_SealGate // seal_gate_ci EXPECT_DEFAULT(root) PASS (designing) @dep:G2_SecondOracle
    G4_Contested // verify_contested_guard ALL PASS·frozen 23 (designing) @dep:G3_SealGate
    GateVerdict // 전부 PASS면 machine=True, 아니면 첫 실패서 중단+사유 (designing) @dep:G4_Contested
```

```python
def machine_gate() -> dict:
    """순차 AND + short-circuit. 첫 실패서 중단하고 사유 반환(롤백은 상위 GuardCheck)."""
    for name, gate in [("reproduce_all", reproduce_all), ("second_oracle", second_oracle),
                       ("seal_gate_ci", seal_gate_ci), ("contested_guard", verify_contested_guard)]:
        if not gate():                                    # 조건: 첫 실패 즉시 중단
            return {"machine": False, "failed_at": name}
    return {"machine": True, "failed_at": None}
```

### 8.3 AdversarialVerify (분해) — N 직교 회의주의자

```
AdversarialVerify // N 직교 회의주의자 (designing)
    RefuteLenses // 직교 반증렌즈 배정(C2-phase·C1-dim·C3-ancilla·composition) (designing)
    SpawnSkeptics // 멀티 서브에이전트 병렬 REFUTE 시도 (designing) @dep:RefuteLenses
    Tally // 다수결 생존(≥과반) → survived (designing) @dep:SpawnSkeptics
```

```python
REFUTE_LENSES = ["C2-phase", "C1-dim", "C3-ancilla", "composition-target"]  # 직교 반증각

def adversarial_verify(seal: dict, n: int = 3) -> dict:
    """N 회의주의자가 *서로 다른* 반증각으로 깨기 시도. 보수적: default refuted=True."""
    lenses = REFUTE_LENSES[:n]
    votes = parallel([AI_make_refute(seal, lens=L) for L in lenses])   # 멀티에이전트·직교
    survived = sum(1 for v in votes if not v["refuted"]) >= (n // 2 + 1)
    # ★ persona_contexts 와 동일정신(직교·blind). seal 은 기계게이트 통과분만 옴(추가 안전망, 합격권 없음).
    return {"survived": survived, "lenses": lenses, "votes": votes}
```

### 8.4 DocSyncBatch (분해) — 외부 3종 체크리스트 (memory 고정)

```
DocSyncBatch // 외부 3종 동기화 (designing)
    ScanStale // grep 전수: 옛 root/counts/second_oracle/fingerprint (designing)
    [parallel]
    UpdateReadme // Status박스·narrative·guarantee-split·fingerprint N/N (designing)
    UpdateOnboarding // Current state·milestone bullet·검증 기대출력 (designing)
    UpdateSpec // milestone로그·§1 summary·guarantee-split·§8.5 totals·결론부 (designing)
    [/parallel]
    PreserveHistorical // abstract "What changed since vX"는 보존(덮지 말 것) (designing)
    ResetBuffer // task_record 누적 비움 + 마지막 동기화 시점 갱신 (designing) @dep:UpdateReadme,UpdateOnboarding,UpdateSpec
```

```python
def doc_sync_batch(delta: dict) -> dict:
    """[[external-docs-batch-sync]] 체크리스트를 노드화. 3문서 병렬 갱신 후 버퍼 초기화."""
    stale = scan_stale(["root", "modules", "apps", "second_oracle", "fingerprint"])  # grep 전수
    update_readme(delta)        # Status박스(48/59식 古수치)·guarantee-split·fingerprint N/N
    update_onboarding(delta)    # Current state 헤드·milestone bullet·§8 기대출력
    update_spec(delta)          # milestone로그·§1 summary·guarantee-split·§8.5 totals·결론부
    # ★ PreserveHistorical: abstract "What changed since vX"는 *현재값으로 덮지 않음*(시점기록)
    reset_task_record()         # 누적 비움 + "마지막 동기화 시점" 갱신
    return {"synced": True, "stale_found": stale}
    # acceptance_criteria: stale 잔여 0(abstract 제외) · task_record 누적 0 · 3문서 수치 일치
