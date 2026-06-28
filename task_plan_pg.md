# task_plan_pg — QuantaFoundry 차기 작업 계획 (PG/PGF)

> **Version** 0.7-plan · **Status** P0·P1·P2·P3·P4·P5·P9 **done** (48모듈·frozen 23키) · P3d(공개 bounty) blocked(외부 relay) · **Notation** PG(PPR/Gantree) · **Base** QuantaFoundry v0.6 + §5[8](B) backend adapter(b3444ca)
> **실행 결과**: P0=`.pgf/clifford/` · P1=`.pgf/arith/` · P4=`.pgf/resource/` · P5=`.pgf/autonomy/`. 회귀 전수 그린(selftest 52/52·second_oracle 18/18·contested 20/20·backend·reproduce_all). 기존 sealed.json 수정 0·frozen 불변. 상세=HANDOFF §5 [9].
> **Source** `_workspace/QuantaFoundry-v0.6-Direction-PGF.md`(8-agent 방향서)를 **실제 코드 상태로 재정렬**한 실행 척추.
> **Scope 원칙** 이 계획의 척추(P0·P1·P4·P5)는 **self-contained**(외부 cross-model relay 불요) — 혼자 착수·완료 가능. P2·P3은 외부 의존이라 BLOCKED 명시.

---

## 0. 방향서 대비 보정 (이 계획이 방향서와 다른 점)

코드 실측으로 방향서의 stale·과장 지점을 보정했다. 계획은 보정된 사실 위에 선다.

| 방향서 주장 | 실측 | 계획 반영 |
|---|---|---|
| P1 ModMultSynth 미착수 | **이미 구현**(`scripts/genskills.py` `modmul_synth`, MMD) | P1 = *엔진 재사용해 신규 modulus 패밀리 확장*으로 재정의 |
| P5 의존성해결 미착수 | **대부분 실현**(`detect_gaps`+`missing_modules`+loop) | P5 = *standing DEP-GRAPH 산출물*만 잔여 |
| P0 "Tier-2 후 u_hash byte-identical 불변" | **거짓** — 오라클 명시: tableau u_hash ≠ dense u_hash | P0 = *새 Tier-2 봉인 추가*(대체 아님), 보증등급 상승이 acceptance |
| P1 "ShorFamily N=33/35 Tier-0 EXACT seal" | full Shor ≥13q > EXACT_BOUND(12) → **Tier-1만 가능** | P1 = *cmul 모듈(7q) Tier-0 EXACT* + full Shor 는 Tier-1 정직 표기 |
| (B) 실행 계층 | 방향서에 **부재**(직후 커밋) | P1 행동관찰에 backend adapter 통합 |

---

## 1. 로드맵 (Gantree)

```
QuantaFoundryV07Plan // 신뢰 약점 지점으로 가치 이동 — self-contained 척추 (designing) @v:0.7
    P0_CliffordTierClosure // Clifford-only 앱을 Tier-2 tableau로 봉인 — 최약보증 무상 해소 (done)
        DetectCliffordApps // registry 스캔: H·S·CNOT·CZ·X·Y·Z·SWAP 만으로 구성된 sealed app 식별 (designing)
        TableauSealLayer // 해당 app의 plan을 stabilizer tableau로 O(n²) 봉인 (Tier-2) (designing) @dep:DetectCliffordApps
        Ghz16WeakSealClose // 유일 Tier-1(ghz16_structural)을 Tier-2로 승격 — structural→unitary_equiv (designing) @dep:TableauSealLayer
        CliffordRoutingGuard // 결정론·비파괴 검증: dense u_hash 불변, Tier-2 추가, 기존봉인/frozen 무변경 (designing) @dep:Ghz16WeakSealClose
    P1_ArithFamilyExtend // 가역 산술합성 엔진(기존)으로 신규 modulus 패밀리 확장 [8/8 합의] (done)
        SynthNewModuli // modmul_synth → cmul_a_mod{33,35} Tier-0 EXACT 모듈 봉인(7q) (designing)
        IndependentArithVerify // second_oracle 식: 봉인 cmul의 산술순열을 독립 재구성해 u_hash 대조 (designing) @dep:SynthNewModuli
        BehavioralObserve // backend adapter로 신규 cmul orbit/period 행동관찰 (illustrative only) (designing) @dep:SynthNewModuli
        ShorAssemblyHonest // N=35 full Shor 조립 시도 → ≥13q=Tier-1 STRUCTURAL 정직 표기(또는 보류) (designing) @dep:IndependentArithVerify
    P4_ResourceReport // 기존 seal resource 필드 집계 → registry-wide 실예산 산출 (done)
        ResourceAggregator // 전 sealed.json resource{total_t,clifford,toffoli,and_bloq} 결정론 집계 (designing)
        CostAwareNote // 동일 u_hash 다후보 시 최소리소스 선택 정책 문서화(코드는 hook만) (designing) @dep:ResourceAggregator
    P5_DepGraphClosure // goal-autonomy 의존성 그래프를 standing 산출물로 (done)
        DepGraphEmit // detect_gaps + registry DAG → DEPENDENCY-GRAPH.json 결정론 산출 (designing)
        FrontierReport // BLOCKED 노드의 missing-prereq 자가지목 요약 (designing) @dep:DepGraphEmit
    P9_Integrate // HANDOFF/spec 동기화 + 회귀 + 커밋(정욱님 지시 시) (done) @dep:P0_CliffordTierClosure,P1_ArithFamilyExtend,P4_ResourceReport,P5_DepGraphClosure
    P2_GatedConsensusPanel // 다중모델 강제(E5'/B4 봉합) — wiring 완비, 실제 신규모델 호출만 외부 (done)
        P2a_SelfContained // 정책·게이트·v05 replay B4 차단 정량화 (done) — scripts/gated_panel.py
        P2b_LiveDispatchWiring // ModelRegistry+dispatch→gated_seal end-to-end; ReplayEndpoint 검증·미연결 BLOCKED (done) — scripts/live_dispatch.py
        P2b_LiveRound_sx // 신규 sx(√X) 6 distinct-weights relay 수거→SEAL PROOF_BACKED→봉인+frozen (done) — scripts/{p2_live_ingest,seal_sx}.py
    P3_FalsificationFront // 방어선 적대시험 — 단일 vs 합의/오라클 검출률, Tier-1 §7 반증 (done)
        P3a_RedTeamSuite // 6공격: golden-copy·identity·uncompute(C3)·convention·B4 CAUGHT 5/6; matrixgate=문서화공백 (done) — scripts/red_team.py
        P3b_Tier1ScaleFalsify // §7 최고위험: golden없는 Tier-1=오배선 봉인(struct≠unitary)·Tier-0 dense만 거부 (done)
        P3c_SingleVsConsensus // 단일출처 봉인 vs 합의·게이트 거부 매트릭스(convention·B4) (done)
    P3d_CrossModelBounty // 외부 AI 적대 반증(P2b relay 재사용) — 6런타임 라운드 1 완료 (done)
        AutoAdjudicate // 오라클 재검산 자동판정(BREAK/HELD/DOC_GAP/NEW_GAP) (done) — scripts/bounty_adjudicate.py, selftest 5/5
        BountyPackage // BRIEF·targets·template·oracle-rules (done) — _workspace/crossmodel/p3d_bounty/
        Relay // 6런타임(deepseek/gemini/gpt-5/grok/kimi/qwen) 독립 수거 (done) — 정욱님
        Ingest // 라운드1 판정: T2/T3 위조 6/6 HELD(provenance), T1 hollow 6/6 DOC_GAP, BREAK 0 (done)
        SelfVerify // 적대적 자기검증: 초기 18-break=채점기 결함 2건 발견·수정(provenance 바인딩·hollow 패턴) (done)
        T1Closure // honest-분해 공백 닫기(비파괴 정책가드) — 모듈+앱 경로 일괄 강제 (done)
            DecompHonestyGuard // 오라클 decomp_guard.py — 동적(__module__)+정적(AST: override·monkey-patch·MatrixGate) (done)
            WireSpecQualityGuard // spec_guard.spec_quality_guard 에 통합 → 모듈(seal_module)+앱(app_assemble) 양쪽 강제 (done)
            ValidateNonDestructive // 48모듈+59앱 byte-identical(root 3dae613d 불변)·6 hollow+matrixgate+app 거부·fingerprint 무변경 (done) — scripts/verify_t1_closure.py
        Round2_CrossRuntimeCoError // 공통 intent 고정→진짜 독립 동반오류 실측 (done)
            DesignProbe // cnot_std(sanity)+cnot_lower(probe, control=q1≠표준) — 순열차 u_hash 분리 (done)
            RoundPackage // ROUND-BRIEF·intents·template (done) — _workspace/crossmodel/p3d_round2/
            CrossRuntimeAdjudicate // 6 실런타임 풀링→establish_truth→GT대조+ρ할인 시연 (done) — scripts/cross_runtime_round.py, selftest 4/4
            Measure // 라운드2 수거·실측: 6/6 GT수렴(both intent ESTABLISHED MULTIMODEL), 동반오류 0 (done)
            // 정직 음성(한계: probe 1종·정답이라 ρ-방어 실데이터 미검증; 더 모호한 probe 후속 가능)
        Round3_HarderProbe // 강한 공유 오개념 게이트로 co-error 유발·ρ-경로 실측 (done)
            DesignProbe // rx_half(반각)·iswap(i위상/SWAP)·tdag(adjoint부호)+x_gate sanity — GT≠오답 u_hash 확인 (done)
            RoundAgnosticAdjudicate // cross_runtime_round.py --round 일반화, _ground_truth.json 로드 (done)
            RoundPackage // ROUND-BRIEF·intents·template·_ground_truth(운영자전용) (done) — _workspace/crossmodel/p3d_round3/
            Measure // 6런타임 수거·실측: 4/4 intent 전원 GT수렴, 동반오류 0 (done)
            // 2라운드 종합 5 probe 전부 co-error 0 — frontier 모델 표준게이트 cross-runtime 견고(정직 음성). ρ-방어 실데이터 미검증 잔존.
        Round4_ContestedDefinition // 정의 자체가 corpus 분열인 게이트 — 분기 실측 성공 (done)
            DesignProbe // qft2(스왑/부호)·sqrt_swap(위상branch)·rz_half(부호 exp∓)+x_gate — GT≠대안 u_hash 확인 (done)
            OutcomeClassify // measure_intent 에 outcome 분류 추가 (done)
            RoundPackage // ROUND-BRIEF·intents·template·_ground_truth (done) — _workspace/crossmodel/p3d_round4/
            Measure // 실측: qft2→CONTESTED(2-2-1-1, near-tie 가드 실데이터 첫 발동)·sqrt_swap/rz_half→4-2 다수 표준 ESTABLISHED·x_gate sanity (done)
            // 핵심: contested near-tie 가드를 실데이터로 첫 검증(qft2 모호→봉인 거부). 4-2 분열은 표준관례 다수→진리(v05 패턴 재현). co-error 0(다수가 비표준에 수렴한 사례 없음).
```

**임계 경로:** `[parallel] P0 · P1 · P4 · P5 [/parallel]` → `P9_Integrate`.
네 phase는 상호 의존이 없어 동시 착수 가능(공유 자원 = registry read-only 스캔뿐, 쓰기 경로 분리). P9가 최종 통합·회귀.

---

## 2. 핵심 노드 PPR

### 2.1 TableauSealLayer (P0 — 무상 약점 해소의 심장)

```python
def tableau_seal_layer(app_id: str, store: Registry) -> SealResult:
    """Clifford-only 봉인앱의 plan을 stabilizer tableau로 Tier-2 봉인.
    스케일에서 unitary_equiv 보증을 dense 미실체화로 회복한다.
    오라클 clifford_seal.py(canonical_tableau_hash/is_clifford)는 *사용만*."""
    # input: H·S·CNOT·CZ·X·Y·Z·SWAP 만으로 구성된 sealed app (예: ghz16_structural)
    plan = load_sealed_plan(app_id)                  # 봉인된 plan(자식 모듈 참조)
    bloq = build_clifford_bloq(plan)                 # plan → cirq Clifford 회로 (MatrixGate 금지)
    if not is_clifford(bloq):                        # 오라클 판정
        return SealResult("SKIP", reason="non-Clifford")
    t_hash, nq = canonical_tableau_hash(bloq)        # O(n²), 2^n 미실체화
    # acceptance_criteria:
    #   - tableau u_hash 는 dense u_hash 와 *다름*(표현 차이) — byte-identical 주장 금지(정직)
    #   - 소규모(n≤12) 교차검증: dense_unitary(bloq) 의 statevector 거동이 Tier-2 봉인과 일관
    #   - semantic_guarantee 등급: structural_wellformed → unitary_equiv 상승(ghz16)
    #   - 기존 Tier-0/1 sealed.json 파일 *무변경*(Tier-2는 신규 산출물로 별도 기록)
    return write_tier2_seal(app_id, t_hash, nq, tier=2)
```

### 2.2 SynthNewModuli (P1 — 복리 엔진 재사용)

```python
def synth_new_moduli(targets: list[tuple[int,int]]) -> list[SealResult]:
    """기존 modmul_synth(MMD 가역합성)로 신규 modulus 의 controlled-(×a mod N) 모듈 봉인.
    엔진은 이미 존재(genskills.py) — 본 노드는 *신규 N 인스턴스 생성·봉인*만."""
    # targets = [(2,33),(2,35)]  # a=base, N=modulus; cmul_a_modN, 7q Tier-0 EXACT
    results = []
    for a, N in targets:
        spec = genskills.modmul_synth(a, N)          # golden=산술순열, plan=봉인 MCT(MatrixGate 금지)
        assert "MatrixGate" not in spec.bloq_src     # honest 분해 firewall(§8.4)
        res = oracle_seal_app(spec)                  # function 2(C-app) 통과해야 SEALED — 자기인증 불가
        results.append(res)
    # acceptance_criteria:
    #   - cmul2_mod21 등 기존 봉인 u_hash 회귀 재현(엔진 불변 증명)
    #   - cmul2_mod33 / cmul2_mod35 Tier-0 EXACT SEALED (7q, dense 128)
    #   - plan 전 단계가 봉인 MCT(toffoli/c3x/c4x/c5x ≤5 ctrl) — MatrixGate 0
    return results
```

### 2.3 IndependentArithVerify (P1 — 제2 검증축, 봉인 비신뢰)

```python
def independent_arith_verify(app_id: str) -> bool:
    """봉인 cmul 의 산술순열을 second_oracle 방식으로 독립 재구성 → sealed u_hash 대조.
    app_assemble/qualtran 미사용 — 동반오류(co-error) 차단."""
    # input: cmul2_mod33 등 봉인앱
    perm = independent_modmul_permutation(a, N, nq)  # ×a mod N 순열을 *처음부터* 재구성(범위밖 identity)
    U = permutation_to_unitary(perm)                 # 독립 경로(genskills 미사용)
    return vs.hash_unitary(U) == load_sealed(app_id)["u_hash"]
    # acceptance_criteria:
    #   - 독립 재구성 u_hash == 봉인 u_hash (삼각측량: golden ⊕ MMD plan ⊕ 독립순열)
    #   - 검증 도구는 측정만(vs.hash_unitary), 구성은 genskills 와 무관한 코드
```

### 2.4 정직성 게이트 (전 phase 횡단 — 절대 위반 금지)

```python
# 이 게이트는 모든 노드의 acceptance_criteria 에 상속된다.
HONESTY_INVARIANTS = {
    "seal_not_replaced_by_observation":
        "backend adapter(B)의 실행출력은 봉인 증거 아님(illustrative only, §8.4).",
    "determinism_sacred":
        "frozen consensus_keys.json 재생성 금지(메모리 검증), 기존 sealed byte-identical 불변.",
    "honest_decomposition":
        "모든 plan 은 봉인 모듈/MCT 합성 — bloq=MatrixGate 금지.",
    "no_self_certification":
        "생성물은 오라클(function 2) 통과로만 SEALED — 페르소나/엔진 자기성공 선언 불가.",
    "tier_truth":
        "Tier-2 u_hash≠Tier-0 dense u_hash(표현차이) 정직 표기. Tier-1≠unitary proof.",
    "scope_honest":
        "full Shor(≥13q)는 Tier-0 EXACT 불가→Tier-1 STRUCTURAL 명시. 하드웨어 범위 외.",
    "oracle_use_only":
        ".agents/skills/qpgf-oracle 는 사용만 — 재구현 금지.",
}

def assert_honesty(node_result) -> None:
    """노드 완료 전 정직성 불변식 위반 여부 검사. 위반 시 (blocked) + 사용자 보고."""
    for inv, rule in HONESTY_INVARIANTS.items():
        if violates(node_result, inv):
            raise HonestyViolation(inv, rule)
```

---

## 3. 우선순위·정책 (POLICY)

```python
POLICY = {
    "order": ["P0", "P1", "P4", "P5", "P9"],     # 권장 순서(병렬 가능하나 P0 먼저 가시성)
    "parallel_ok": ["P0", "P1", "P4", "P5"],     # 쓰기경로 분리 → 동시 착수 가능
    "max_verify_cycles": 2,
    "commit": "정욱님 지시 시에만. 메시지 끝 Co-Authored-By: Claude Opus 4.8 (1M context).",
    "write_targets": {                            # 경로 분리(충돌 방지)
        "P0": "registry/SEMANTIC-GUARANTEES.json 갱신 + .pgf/clifford/ 신규 Tier-2 기록",
        "P1": "specs/apps/cmul*_mod3{3,5}.app.pg + registry/apps/ + scripts(엔진 불변)",
        "P4": ".pgf/resource/RESOURCE-REPORT.json",
        "P5": ".pgf/autonomy/DEPENDENCY-GRAPH.json",
    },
    "regression": ["second_oracle 18/18", "verify_contested_guard 20/20",
                   "genskills selftest", "backend_adapter all_ok",
                   "frozen 15키 불변", "기존 sealed byte-identical"],
}
```

| P | 작업 | 합의 | 레버리지 | 비용 | self-contained |
|---|---|---|---|---|---|
| **P0** | Clifford → Tier-2 봉인층 | 4/8 | 최고 | 최저 | ✅ |
| **P1** | 산술 패밀리 확장(엔진 재사용) | **8/8** | 최고 | 중 | ✅ |
| **P4** | resource 실예산 집계 | 7/8 | 중 | 저 | ✅ |
| **P5** | dep-graph standing 산출 | 6/8 | 중 | 저 | ✅ |
| **P2** | 다중모델 panel(+sx 라이브 봉인) | 5/8 | 높음 | 중 | ✅ wiring·게이트 (P2b relay만 외부) |
| **P3** | falsification front(P3a/b/c) | 4/8 | 높음 | 중 | ✅ (P3d 공개 bounty만 외부) |

---

## 4. 반증 우선 (honesty-first)

**최고위험 가정:** *Tier-1 structural seal 이 스케일에서 unitary 정확성을 보존한다.*

- **가장 싼 반증:** sealed children + 정상 plan(Merkle 통과)이나 조립 unitary가 app_golden과 다른 합성 1개(예: ancilla 얽힌 채 남기는 잘못된 uncompute)를 구성 → Tier-1에서 봉인되는지, dense/Tier-2 C-app만 거부하는지 확인.
- **P0가 위험 흡수:** Clifford 앱을 Tier-2로 라우팅하면 그 부류는 약한 보증을 떠남 → 반증 표면이 non-Clifford로 좁혀짐. (P0가 이 계획의 1순위인 이유.)

**차상위 위험:** *키-프리 same-weights co-error (B4).* — P2/P3에서만 정량화 가능(외부 relay 필요) → 본 척추에서 BLOCKED 정직 표기.

---

## 5. 실행 규칙 (PG)

1. `[parallel] P0·P1·P4·P5` — 쓰기경로 분리됐으므로 순차/병렬 모두 가능. 가시성 위해 **P0 먼저** 권장.
2. 각 노드 완료 전 `assert_honesty()` 통과 필수 — 위반 시 `(blocked)` + 보고.
3. 봉인 경로는 오라클 `verify_seal`/`app_assemble` *사용만*. 검증 도구(`hash_unitary`)는 측정 전용.
4. 봉인 점검 시 frozen `consensus_keys.json` 재생성 금지(메모리 검증). 앱 재검증=`app_assemble`.
5. 신규 봉인은 byte 결정론 — 2회 실행 byte-identical 확인.
6. P9 통합: 회귀 전수 그린 + HANDOFF/spec 동기화 후, 커밋은 정욱님 지시 시에만.

---

## 6. 한 줄 결론

**P0(Clifford→Tier-2, 무상·단독)로 유일 Tier-1 약점을 닫고, P1(산술 엔진 재사용해 mod33/35 패밀리 확장, 8/8 합의)을 제2검증축·backend 행동관찰로 받치며, P4·P5를 병렬 환류한다. P2·P3(다중모델·공개반증)은 외부 cross-model relay 의존이라 BLOCKED 정직 표기 — 정욱님 relay 시 해제.**

*다음 명령: 이 계획 기반으로 `P0` 부터 착수(또는 `[parallel] P0·P1·P4·P5`).*
