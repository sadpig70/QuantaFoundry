# QuantaFoundry — 통합 향후 로드맵 (8-Agent 외부제안 통합)

> 작성 2026-06-28 · 입력 = `_workspace/프로젝트향후방향제안.md`(8 외부 AI 런타임의 §2 7질문 응답)
> 방법 = PG/PGF로 8제안을 분해·수렴분석·충돌해소·통합 설계.
> 파일명 주: 정욱님 지시의 `integrated_loadmap.md`는 `roadmap` 오타로 판단해 `integrated_roadmap.md`로 저장. 다르면 알려주세요.
> 권위 현재상태: 53모듈·75앱·root `06ca92d7`·frozen 23키 (REGISTRY-MANIFEST.json). ※성장 이력(순수 비파괴): v0.7-core 48모듈·`3dae613d` → W2.4 c7x·cr8 50모듈·`437efbc3` → W6.1 cmul(mod91/77/85) → W6.3 iqft8 → W6.4 cr6/7/8_gate+qft5~8 53모듈·67앱 → W6.5 capstone **shor91(7×13, Tier-1 STRUCTURAL)**+cmul4/16/74_mod91 71앱·`93183bcd` → W7.1 QEC stabilizer 인코더(repcode3 bit/phase·syndrome3·**shor9_encoder [[9,1,3]]** Clifford Tier-0) 75앱·`06ca92d7`.

---

## 0. 한 문장 통합 방향

8 에이전트 만장일치의 결론:

> **오라클(검증 알고리즘)은 견고하다. 다음 6개월의 전장은 검증 알고리즘이 아니라
> ① 오라클이 검증하는 *대상(intent/golden)*의 정당성, ② 그 보증이 *스케일(Tier-1 대형회로)*에서
> 유지됨, ③ *합의 방어선(ρ-discount)*의 실데이터 가동, ④ 신뢰 자본의 *외부 소비화(adoption)*다.**

핵심 경계(8/8 합의): **봉인은 구현→golden 동등성을 증명하지, intent→golden 정당성을 증명하지 않는다.**
그리고 **실행 ≠ 검증** — QPU/노이즈 산출물은 영원히 seal이 아니라 evidence다.

---

## 1. 수렴 분석 — 7질문 × 8에이전트 (합의 매트릭스)

| 질문 | 수렴 결론 | 지지 에이전트 |
|---|---|---|
| Q1 최약가정 | **intent/golden legitimacy** (봉인=합의지 증명 아님); Tier-1이 스케일에서 보증상실; 복리곡선 미측정 | A1·A2·A3·A4·A6 / A5·A8 |
| Q2 발견 | **별도 Discovery 계층**; 가치함수=Novelty+Sealability+Composability+Resource−Ambiguity−Cost; exploit(분해최적화)+explore(unblock-leverage/MCTS over sealed DAG); Primitive Proposal Round(sx/c6x가 PoC) | 8/8 |
| Q3 Backend 8c | **execution≠verification 절대경계**; QASM export→noise sidecar→QPU; QPU=evidence "OBSERVATION—NOT A SEAL" | 8/8 (우선순위만 분기) |
| Q4 합의/ρ | 표준게이트 co-error 유발 불가(종료); **poisoned/lineage-correlated 패널만이 ρ 실가동 직접경로**; 미가동 정직라벨 | A3·A8 핵심 / A4·A5·A6·A7 |
| Q5 adoption | **QPGF↔Foundry 분리**; CI seal-gate/GitHub Action/Badge; **ingestion 우선**(기존회로 봉인); citable DOI; bounty 개방 | 8/8 |
| Q6 blind spot | oracle 단일실패점(second_oracle 18/48만); 결정론 env취약(BLAS/FP); global-phase floating; revocation 부재; Sybil; bus factor 1 | 통합 |
| Q7 Top-3 | **Discover + Trust-closure(Tier-1보증↑ & ρ실검증) + Adoption-via-CI**; QPU defer | 집계 |

**충돌(소수의견) 및 해소:**
- *Backend 8c 우선순위*: A3 "defer/낮음(자원이탈)" ↔ A7 "Tier-4 Shadow Tomography 야심". → **해소: export+sidecar까지만(저비용), 실QPU·Tier-4는 defer**(다수의견·정직경계 우선).
- *Tier-1 접근*: A5 "ZX-routing(Tier-3)" ↔ A8 "sampled dense verification". → **해소: 상보적 — 둘 다 채택**(Clifford계열=ZX/tableau 라우팅, non-Clifford 대형=sampled-dense 신규 보증등급).

**고유 통찰(단일 에이전트, 통합에 흡수):**
- A2: **Global-Phase Tracker** — C4가 무시한 전역위상이 controlled-U 하위블록 합성 시 상대위상 버그로 변모.
- A8: **sampled-dense verification**(`unitary_equiv_sampled` 신규등급, seed를 seal에 포함=결정론 유지); **Sybil 암호증명**; **TLA+ trust-boundary 형식모델**.
- A3: **목표선택 co-error**(생성·확립엔 cross-model 체크 있으나 *무엇을 만들지* 선택엔 없음); **convention 단일문화**(second_oracle가 endian/위상을 독립유도하는가 vs 가정하는가 — 검증 필요).
- A5: **oracle rollback/revocation 프로토콜**; **cost-audit**(자율루프 비용 대비 봉인성공률).

---

## 2. PG Gantree — 통합 로드맵 척추

```
IntegratedRoadmap // 8-agent 통합 6개월 방향 (designing) @v:1.0
    [parallel]
    TrackA_QFDiscover // open-ended 발견 엔진 (designing) #priority:1
    TrackB_TrustClosure // 신뢰 미검증영역 닫기 (designing) #priority:1
    TrackC_AdoptionCI // 신뢰자본 외부 소비화 (designing) #priority:2
    [/parallel]
    TrackE_Hardening // blind-spot 비파괴 방어 (designing) #priority:cross @dep:none
    TrackD_BackendEvidence // QPU evidence sidecar (blocked) #priority:defer

TrackA_QFDiscover // 별도 discover.py 계층 (designing)
    ValueFunction // 후보 점수화 (designing)
    ExploitAxis // 분해 최적화기 (designing) @dep:ValueFunction
    ExploreAxis // unblock-leverage 탐색 (designing) @dep:ValueFunction
    PrimitiveProposalRound // capability-gap→panel→seal (designing) @dep:ExploreAxis
    GoalSelectionGuard // 목표선택 co-error 방어 (designing) @dep:ValueFunction

TrackB_TrustClosure // Tier-1 보증↑ + ρ 실검증 (designing)
    Tier1Closure // 대형회로 보증 상승 (designing)
        SampledDenseVerify // unitary_equiv_sampled 신규등급 (designing)
        ZXRouting // Clifford+T 대형 라우팅 (designing)
    ConsensusValidation // ρ/co-error 실데이터 (designing)
        PoisonedLineagePanel // 상관오류 강제유발 (designing)
        ConventionIndependenceAudit // second_oracle 독립유도 검증 (designing)

TrackC_AdoptionCI // QPGF↔Foundry 분리 (designing)
    QasmIngestionExport // OpenQASM3 ↔ spec 양방향 (designing)
    SealGateCI // GitHub Action seal-badge (designing) @dep:QasmIngestionExport
    CitableRegistry // Zenodo DOI + CITATION.cff (designing)
    CLI // qf verify/seal/compose/reproduce/explain/export (designing)

TrackE_Hardening // 횡단 방어 (designing)
    SecondOracleFullCoverage // 18/48 → 48/48 (designing)
    DeterminismEnvPin // BLAS/FP/platform lockfile+container (designing)
    GlobalPhaseTracker // 전역위상 명시기록+합성검사 (designing)
    OracleRevocationProtocol // rollback+revocation_list 운영 (designing)
    RuntimeIdentityProof // Sybil 암호증명 (designing)
```

---

## 3. 트랙별 PPR (정직 경계 내장)

### Track A — QF-Discover (우선순위 #1, 2–3개월)

```python
def qf_discover(registry: Registry, dep_graph: DAG) -> list[SealedPrimitive]:
    """known-family 소진 너머 새 method/primitive 자율 발견. HANDOFF 남은일 #1."""
    # value(candidate) = 0.25*Novelty + 0.20*Sealability + 0.20*Composability
    #                  + 0.15*ResourceΔ + 0.10*ConsensusEstablishability
    #                  - 0.20*AmbiguityRisk - 0.15*VerificationCost
    #   · Composability = dep_graph 의 fan-in(이 후보를 prereq로 요구하는 BLOCKED 노드 수)  ← c6x 패턴
    #   · Novelty 는 LLM 주장 불가 → "기존 GenSkill 재현불가 + sealed 조합 표현불가" 객관근거 강제
    cands = AI_propose_method_hypotheses(registry, sources=["gap","compression","parametric-closure"])
    ranked = sorted(cands, key=value, reverse=True)
    sealed = []
    for c in ranked:
        if not goal_selection_guard(c):   # A3: 목표선택 co-error 방어 — 무엇을 만들지도 cross-model 체크
            continue
        # exploit: 타깃 고정, 분해만 탐색(MCTS/진화) → 오라클=하드보상(봉인=1, resource=연속). reward-hacking 구조차단
        # explore: capability-gap → Primitive Proposal Round(panel 수렴+sympy proof → key-free seal). sx/c6x=PoC
        r = seal_attempt(c)               # 오라클 사용만(재구현 금지)
        if r.sealed: sealed.append(r)
    return sealed
    # acceptance_criteria:
    #   - human seed 0 으로 최소 1개 *새 family* 봉인(기존 GenSkill 재현불가 + 독립 semantics 확립 + downstream 합성가능)
    #   - capability-coverage 게이트로 trivial gate(c7x,c8x…) 양산 차단
    #   - 정직경계: 생성≠검증(산출물은 여전히 오라클 봉인), 결정론 byte-identical 불변
```

지지: A1(discover.py)·A3(exploit/explore 2축)·A4(DiscoverySkill)·A5(Hypothesis-Driven)·A6·A7(MCTS)·A8(Primitive Proposal Round). **위험**: novelty 보상해킹 → coverage 게이트 필수. 목표선택 co-error(A3).

### Track B — Trust-Closure (우선순위 #1, 1–2개월)

```python
def tier1_closure(app: SealedApp) -> SemanticGuarantee:
    """복리테제 최약가정(Tier-1=structural_wellformed≠unitary_equiv)을 스케일에서 직격."""
    if is_clifford_T(app):
        return zx_routing(app)            # A5: pyzx full_reduce vs independent golden → Tier-3 equiv
    # A8: K개 random basis-state 샘플 → column dense materialize → app_golden 대조
    #     신규 보증등급 unitary_equiv_sampled (structural ↔ unitary_equiv 사이)
    #     sample seed 를 seal 에 포함 → 결정론 재현 보존(determinism 위반 0)
    return sampled_dense_verify(app, K=expected_K, seed=fixed)
    # acceptance_criteria:
    #   - ghz16/ghz20·distinct-prime Shor(≥13q) 가 즉시 보증등급 상승
    #   - 헤드라인 수치 항상 (Tier-0 exact / Tier-1 structural / sampled) 분리표기(A3 #3 blind-spot)
    #   - 비파괴: registry/sealed/frozen 무변경, fingerprint 2파일 무수정

def consensus_validation() -> RhoReport:
    """ρ-discount 를 synthetic 너머 *실데이터*로 가동(가장 정직히 인정된 단일 갭)."""
    # 표준게이트 co-error 유발시도 중단(4라운드 정직음성). 대신 co-error 를 *구성*:
    panel = base_runtimes + [poisoned_or_lineage_correlated_unit]   # A3·A8: 직접경로
    probes = ["little-endian QFT(corpus default 위배)", "conjugate-but-stated-standard",
              "corpus-sparse non-Clifford phase"]                   # corpus 자체가 틀린 intent
    # 계보공유 2소스가 *틀리게* 합의할 때 ρ-discount 가 joint vote 를 <2 independent unit 으로 붕괴시키는가?
    return measure(panel, probes, metrics=["N_eff","wrong_majority_rate","contested_refusal_rate","false_establish_rate"])
    # acceptance_criteria:
    #   - 실 상관오류 1건 산출 → ρ-discount 실가동 입증, 또는
    #   - 여전히 0 이면 라벨을 "설계됨·미가동"으로 최종확정(과장위험 제거) — 어느 쪽이든 정직 종결
    #   - ConventionIndependenceAudit: second_oracle 가 endian/위상을 *독립유도*하는가 *가정*하는가 판정(A3)
```

지지: B1=A5(ZX)·A8(sampled-dense). B2=A3·A4·A5·A6·A7·A8. **위험**: 패널이 모든 probe를 CONTESTED 거부하면(올바른 동작) ρ는 여전히 미가동 → poisoned-model만이 직접경로(A8).

### Track C — Adoption-via-CI (우선순위 #2, 1개월~)

```python
def adoption_via_ci():
    """단일 repo → 외부 소비. 이주 강요 대신 '기존 워크플로에 seal-gate 삽입'."""
    # 1. ingestion 우선(A3): OpenQASM3/Qiskit → spec 변환 → *남이 이미 쓴 회로*를 봉인. decomp_guard 가 정직 보장
    # 2. SealGateCI: GitHub Action — PR 회로를 QPGF 검증 → Seal Badge(Tier+ResourceCost). QPGF↔Foundry 분리
    # 3. CitableRegistry: release 마다 Zenodo DOI + CITATION.cff → 논문이 "QPGF-sealed root X" 인용(재현성 위기 대응)
    # 4. CLI: qf verify/seal/compose/reproduce --expect-root 3dae613d/explain/export
    # acceptance_criteria:
    #   - 외부 라이브러리 1곳에 QPGF-CI-gate 파일럿 채택(friendly 양자 라이브러리)
    #   - 제출 CI gate: "로컬 deterministic seal 재현 성공해야 제출 가능"(trust-root 오염 방어)
    #   - export 는 정직(decomp_guard 가 plan=실회로 보장). registry=citable infra
```

지지: A1(QPGF-CI)·A3(ingestion 우선)·A4(SDK)·A5(plugin)·A6(API/dashboard)·A7(Seal Badge)·A8(DOI/bounty). **위험**: Sybil(runtime 자기식별) → Track E RuntimeIdentityProof 의존.

### Track E — Hardening (횡단, 비파괴 우선)

| 노드 | 대응 blind-spot | 정직경계 |
|---|---|---|
| SecondOracleFullCoverage | oracle 단일실패점(현재 18/48) → 48/48 CI | 독립 numpy 축 확장, sealed 무변경 |
| DeterminismEnvPin | BLAS/FP/platform → byte-identity 위협 | lockfile + container hash + cross-platform 시험 |
| GlobalPhaseTracker | 전역위상 floating(A2) → 합성 상대위상 버그 | C4 통과 시 무시된 전역위상을 sealed 메타에 명시기록 + 합성 정적검사 |
| OracleRevocationProtocol | fingerprint 버그/업그레이드 시 전봉인 무효 | rollback + revocation_list 운영(현재 빈 배열), emergency re-seal 별도문서 |
| RuntimeIdentityProof | Sybil(Tier-3 service 시) | API key fingerprint / signed submission bundle |

### Track D — Backend Evidence (defer, gated)

```python
# 다수의견 = defer. 착수 시에도 봉인경계 절대 불가침.
def backend_evidence(app: SealedApp) -> EvidenceSidecar:   # NOT a Seal
    # QASM3 export → Aer noise replay → (선택)real QPU. 산출물 watermark="OBSERVATION — NOT A SEAL"
    # 유일 정당용도(A3): QECGatesCost(P4) 예측 vs 실하드웨어 비용 = resource 모델 신빙성 보정(정확성 검증 아님)
    # 2026 Tier-1 대형회로 실하드웨어 = 깊이·노이즈상 비현실적, 정직히 범위 밖
```

---

## 4. 권고 실행 순서 (impact × feasibility)

1. **즉시·저비용 고레버리지** (1개월): Track C `QasmIngestionExport` + `CitableRegistry`(DOI) — export는 decomp_guard 덕에 정직, 외부 채택 funnel 최상단. 병행 Track E `SecondOracleFullCoverage`(48/48).
2. **#1 핵심** (1–2개월): Track B `Tier1Closure`(sampled-dense + ZX) — 복리테제 최약가정 직격, 외부의존 0, 즉시 인용가능 결과(헤드라인 수치 질적 정직화).
3. **#1 핵심** (2–3개월): Track A `QF-Discover`(value function + Primitive Proposal Round) — open-ended autonomy, sx/c6x가 PoC.
4. **정직 종결** (병행 8주): Track B `ConsensusValidation`(poisoned/lineage 패널) — 최대 과장위험(ρ "미가동") 제거.
5. **defer**: Track D QPU 8c, 표준게이트 추가 frontier 라운드(수확체감).

---

## 5. 불변 제약 (모든 트랙 공통)

- **결정론 신성불가침** — 봉인 byte-identical, frozen 23키 불변. 신규 보증등급도 seed를 seal에 포함해 재현 보존.
- **오라클 사용만** — `verify_seal.py`·`contracts.py`(fingerprinted) 절대 무수정. 가드/신규검증은 비-fingerprint 계층.
- **honest 분해** — MatrixGate 금지(decomp_guard). **실행 ≠ 검증** — evidence는 seal 아님.
- **비파괴 우선** — registry/specs/sealed 순수성장, 분석·보증 레이어는 가산만.
- self-contained · 한국어응답/식별자영어 · git은 정욱님 지시 시에만.

---

## 6. 다음 단계 선택지

위 트랙 중 하나를 **PGF 실행 척추**(DESIGN→WORKPLAN→execute)로 전개 가능:
- **(권장 첫걸음)** Track B `SampledDenseVerify` — 최약가정 직격·외부의존 0·결정론 보존 설계가 명확.
- Track A `QF-Discover` value function 정식 스펙 + dep-graph fan-in 측정.
- Track C `QasmIngestionExport` API 설계.

어느 트랙을 먼저 상세 설계할지 지시 주시면 PG/PGF로 전개하겠습니다.
