# WORKPLAN — V04Review (외부 리뷰 self-contained 대응)

> 설계 출처: `_workspace/V0.4-REVIEW-RESPONSE-DESIGN.md`. 모드: execute (loop 수동).
> 원칙: 결정론 신성불가침 · honest 분해(no MatrixGate) · self-contained · 봉인만이 존재.

## POLICY
```json
{ "max_verify_cycles": 2, "determinism": "sacred", "human_seed": 0,
  "verify": ["acceptance", "determinism_byte_identical", "firewall_no_matrixgate"] }
```

## Gantree (실행 순서 = @dep)

```text
V04Review  // 리뷰 대응 SC 작업 (execute)
    P5_RegistryIntegrity  // 레지스트리 1급화 — P2 토대 (in-progress)
        gen_dependency_graph    // 각 app .pg plan 파싱 → registry/DEPENDENCY-GRAPH.json + .md (atomic)
        gen_registry_manifest   // REGISTRY-MANIFEST.json: modules/apps 분류 + cached vs canonical + root hash (atomic)
        seal_schema_note        // semantic_guarantee(tier) 개념 문서화 (기존 seal 불변, 비파괴) (atomic)
    P2_GoalAutonomy  // "무엇을 만들지" 자율 결정 [@dep:P5_RegistryIntegrity]
        registry_scanner        // 의존그래프 스캔 → 미봉인 composable gap 후보 생성 (atomic)
        value_scorer            // 점수 = 재사용성 × 알고리즘가치 × (1/난이도) (atomic)
        forge_scheduler         // 최고점 후보 자동 빌드 시도 (human seed 0) (atomic)
        compounding_curve       // N sealed → 신규 유효 app 수 곡선 측정 (§4 비선형 실증) (atomic)
    P4_SecondOracle  // 신뢰근원 다변화 — Qualtran 비의존 검증기
        pure_python_verifier    // 순수 perm/dense 재계산으로 sealed u_hash 샘플 교차대조 (atomic)
    P3_NecessityProof_SC  // KeyFreeConsensus necessity (혼자 가능 부분)
        hard_intent_proof_demo  // ambiguous/hard intent에 proof⊕structural → ESTABLISHED vs escalation (atomic)
    P1_HonestCapstone_Shor21  // N=15 특수성 완전 탈피 [@dep:P5,P2 optional]
        iqft_substrate          // cr5_dag·cr6_dag 봉인 → iqft6 app (atomic)
        shor21_assembly         // H^6 · c-{cmul2,4,16}_mod21 · iqft6 → shor21_a2 봉인 (atomic)
        probabilistic_readout   // 연속분수 후처리로 r=6 복원 → 21=3×7 검증 (atomic)
    P6_ReproPack  // one-command 재현 [@dep:P5]
        reproduce_all_py        // 모듈+앱+재발견+결정론+행동 통합 1커맨드 (atomic)
    P7_DocHonesty  // 정직성 패치
        claim_calibration_doc   // _workspace에 청구 보정·정합성 패치 노트 (spec 반영 권고) (atomic)
```
