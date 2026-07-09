# DESIGN — MasterRoadmap (잔여 작업 정규화 척추)

> **목적**: 즉흥적 "꼬리물기"(직전 결과물 → 다음 작업 즉석 제시) 차단. 모든 잔여 작업을 단일
> Gantree로 가시화·정규화하고, **유한 집합으로 종결**시킨다.
>
> **규율 (불가침)**:
> 1. 이 트리에 **노드로 존재하지 않는 작업은 착수·제시하지 않는다.**
> 2. 새 작업이 필요하면 *먼저 이 마스터에 노드로 추가(설계)* 한 뒤 진행 — 즉석 착수 금지.
> 3. **Track-SC = 내가 혼자 완료**(self-contained). **Track-EXT = 리스트만**(정욱님 수거/하드웨어 대기, 착수 금지).
>
> **깊이 정책**: SC 작업은 **1–2레벨** 얕은 분해 — 각 작업이 1세션 내 봉인+검증+마무리 가능한 규모.
> 거대 family 확장(W8이 8.1~8.4로 번진 식) 지양. 정직 경계는 기존 패턴 상속(봉인≠실행≠검증·근사≠exact·변분≠exact).
>
> **종결 의도**: Track-SC를 전부 `(done)`으로 소진 → `SC_Closure` 선언 → 이후 잔존은 Track-EXT(외부)뿐.
> 그 시점에 self-contained 확장은 *의도적으로 종료*하고, 신규 방향은 정욱님 지시로만 개시.

---

## Gantree

```
MasterRoadmap // 잔여 작업 정규화·종결 (in-progress) @v:1.0

    TrackSC // 내가 혼자 완료 — 변분/근사 알고리즘 마무리 클러스터 (done)
        W10_2_VQEDeepening // 2-layer ansatz → 표현력↑로 gap 축소 정량 (done) @dep:W10.1
            # input: 봉인 vqe_he2_* (1-layer, gap≈0.071)
            # process: 2-layer ansatz(Ry·CNOT·Ry·CNOT) 1q-θ 인스턴스 봉인 + 연속 sweep min 관찰
            # output: vqe_he2_*_L2 봉인(Tier-0) + gap(L2) < gap(L1) 관찰(여전히 >0)
            # criteria: composite==golden up-to-phase·MatrixGate 0 · gap_L2<gap_L1 · 비파괴(frozen/fingerprint 불변)
        W11_1_QAOA // MaxCut QAOA p=1 — 변분의 조합최적화 자매 (done)
            # input: 봉인 rzz_*·rx_* (W8 복리), 작은 그래프(2~3노드)
            # process: cost e^{-iγΣZZ}(rzz 복리) + mixer e^{-iβΣX}(rx 복리) 1-layer 고정 γ/β 봉인
            # output: qaoa_* 봉인(Tier-0, 신규 모듈 0 목표) + ⟨C⟩ 근사비(β/γ sweep) 관찰
            # criteria: composite==golden · 신규 모듈 ≤1 · 근사비<1 정직표기 · 비파괴
        W10_3_ParamShiftGradient // (옵션·경량) 변분 미분의 정직 관찰 (done) @dep:W10_2_VQEDeepening
            # input: 봉인 ry_* shift 인스턴스
            # process: parameter-shift ∂⟨H⟩/∂θ=(⟨H⟩(θ+π/2)−⟨H⟩(θ−π/2))/2 backend_adapter 관찰
            # output: 수치미분과 대조(exact-gradient 성질) — seal 아님(관찰). 신규 봉인 0~1
            # criteria: parameter-shift==수치미분(atol) · execution≠verification 경계 명시
        SC_Closure // self-contained 트랙 종결 (done) @dep:W10_2_VQEDeepening,W11_1_QAOA,W10_3_ParamShiftGradient
            # ✅ SC 전부 done(root fa06bd80, 68모듈·105앱) → HANDOFF §2 "SC 확장 종결" 기록 + task_record 봉인 델타 누적
            #   외부 3종 동기화는 batch 규칙상 정욱님 "동기화" 지시 시 (task_record 에 보류)
            # 이후 self-contained 신규 작업 없음 → Track-EXT(외부)만 잔존, 신규 방향=정욱님 지시

    TrackW12 // 정욱님 지시로 재개된 신규 self-contained 방향 — guarded c-ladder continuation (in-progress) @dep:SC_Closure
        W12_1_QueryOracleAlgos // Deutsch-Jozsa · Bernstein-Vazirani · Simon query/oracle algorithms (done)
            # input: 봉인 h_gate/x_gate/cnot, existing app_assemble Tier-0 path
            # process: query-oracle app specs + backend_adapter behavior observations
            # output: 4 Tier-0 apps(dj2_const1,dj2_balanced_xor,bv3_s101,simon2_s11) + report
            # criteria: composite==golden up-to-phase · 신규 모듈 0 · query behavior deterministic/support-correct · 비파괴(frozen/fingerprint 불변)
        W12_2_QuantumWalk // coined quantum walk on cycles C4/C8 (done) @dep:W12_1_QueryOracleAlgos
            # input: 봉인 h_gate/x_gate/cnot/toffoli/c3x, existing app_assemble Tier-0 path
            # process: C4/C8 shift+coin step app specs + repeated-step backend observation
            # output: 4 Tier-0 apps(qw_c4_step,qw_c4_2steps,qw_c8_step,qw_c8_3steps) + report
            # criteria: composite==golden up-to-phase · 신규 모듈 0 · position distributions/interference observed · 비파괴(frozen/fingerprint 불변)
        W12_3_Suzuki4 // 4th-order Yoshida-Suzuki Hamiltonian simulation steps (done) @dep:W12_2_QuantumWalk
            # input: W8.3 TFIM first/second-order pattern, QPGF module/app seal path
            # process: p/q coefficient Rz/Rx modules + rzz half-angle apps + TFIM3/4 S4 apps
            # output: 4 Tier-0 modules(rz_y4_p,rx_y4_p,rz_y4_q,rx_y4_q) + 4 Tier-0 apps + order report
            # criteria: composite==golden up-to-phase · MatrixGate 0 · 4th-order ratio≈16 observation · 비파괴(frozen/fingerprint 불변)
        W12_4_ErrorMitigationObservation // zero-noise extrapolation observation (done) @dep:W12_3_Suzuki4
            # input: already sealed Tier-0 apps, backend_adapter u_hash gate
            # process: deterministic depolarizing-noise expectation model + scale=1,3,5 ZNE extrapolation
            # output: observation report only; 신규 봉인 0, registry root unchanged
            # criteria: noisy bias visible · ZNE reduces bias but residual remains · mitigation≠exact boundary explicit · root/fingerprint unchanged
        W12_5_Shor119Frontier // Shor frontier beyond 91: N=119=7×17 (done) @dep:W12_4_ErrorMitigationObservation
            # input: c7x-enabled modular multiplier synthesis, iqft8, h_gate, app_assemble structural tier
            # process: seal cmul{2,4,16,18,86}_mod119 Tier-0 + assemble shor119 Tier-1 structural
            # output: 5 Tier-0 multiplier apps + 1 Tier-1 structural Shor app + frontier report
            # criteria: N>91 distinct-prime · max control≤7 · structural tier honestly marked · period readout illustrative · regression green
        W12_6_C8xPrimitiveFrontier // c8x primitive + N=187 modular multiplier frontier (done) @dep:W12_5_Shor119Frontier
            # input: qpgf-oracle module seal path, genskills MMD modmul synthesis, app_assemble Tier-0 path
            # process: seal c8x Tier-0, extend genskills cap to c8x, seal cmul2_mod187 Tier-0
            # output: 1 Tier-0 module(c8x) + 1 Tier-0 app(cmul2_mod187) + frontier report
            # criteria: c8x independent u_hash matches · cmul uses max control=8 and c8x dep · N>=128 frontier unlocked · regression green
        W12_7_Shor221StructuralFrontier // c8x payoff to Shor-221 structural frontier (done) @dep:W12_6_C8xPrimitiveFrontier
            # input: c8x-enabled modular multiplier synthesis, iqft8, h_gate, app_assemble structural tier
            # process: seal cmul{2,4,16,35,120}_mod221 Tier-0 + assemble shor221 Tier-1 structural
            # output: 5 Tier-0 multiplier apps + 1 Tier-1 structural Shor app + frontier report
            # criteria: N=221=13×17 distinct-prime · max control=8 and c8x used · structural tier honestly marked · period readout illustrative · regression green
        W12_8_C9xPrimitiveFrontier // c9x primitive for 9-work-bit modular arithmetic (done) @dep:W12_7_Shor221StructuralFrontier
            # input: QPGF module oracle, independent cnx_perm(9), c8x frontier blocker
            # process: seal c9x Tier-0 and extend gen_modmul cap to 9-control MCTs
            # output: 1 Tier-0 module(c9x), c9x-enabled modmul_synth
            # criteria: c9x independent u_hash matches · genskills verify INTACT · c10x remains honest blocker
        W12_9_C9xPayoffFamily // c9x-consuming multiplier family (done) @dep:W12_8_C9xPrimitiveFrontier
            # input: N=381=3×127, a=2, powers [2,4,16,256]
            # process: seal cmul{2,4,16,256}_mod381 Tier-0 via exact permutation C-app path
            # output: 4 Tier-0 multiplier apps, all max_control=9 and c9x-consuming
            # criteria: independent arithmetic u_hash 4/4 · no full Shor claim inside this node
        W12_10_ShorN256StructuralFrontier // first N>=256 Shor structural app (done) @dep:W12_9_C9xPayoffFamily
            # input: c9x payoff family, h_gate, iqft8, app_assemble structural tier
            # process: assemble shor381 = H^8 · controlled-U^(2^j)[powa] · iqft8
            # output: 1 Tier-1 structural Shor app(shor381), frontier report
            # criteria: N=381>=256 · all children sealed · structural tier honestly marked · period readout illustrative · regression green
        W12_11_FrontierSelector // deterministic frontier candidate ranking (done) @dep:W12_10_ShorN256StructuralFrontier
            # input: gen_modmul MMD synthesis, semiprime N ranges
            # process: rank candidates by work bits, unique powers, gate count, max control, useful readout
            # output: report-only .pgf/arith/FRONTIER-SELECTOR-REPORT.json
            # criteria: no registry growth · identifies N=635 as next c10x-class candidate · deterministic JSON
        W12_12_ShorStructuralGeneralizer // reusable Shor structural assembler/verifier (done) @dep:W12_11_FrontierSelector
            # input: shor119/shor221/shor381 committed specs and sealed children
            # process: build_shor_spec(app_id,N,a,t) + structural hash/resource reassembly
            # output: helper script + .pgf/arith/SHOR-STRUCTURAL-GENERALIZER-REPORT.json
            # criteria: shor119/shor221/shor381 hashes/resources reproduce byte-identically
        W12_13_C10xPrimitiveReview // c10x feasibility and cost review only (done) @dep:W12_12_ShorStructuralGeneralizer
            # input: W12.11 selector results, 11q dense cost estimate, current c9x cap
            # process: scan c10x-class N range, produce go/no-go and guardrails
            # output: report-only .pgf/arith/C10X-PRIMITIVE-REVIEW.json
            # criteria: no c10x seal · no registry/root change · successor candidate explicit
        W12_14_C10xPrimitiveFrontier // c10x primitive + N=635 modular multiplier frontier (done) @dep:W12_13_C10xPrimitiveReview
            # input: W12.13 recommended target N=635=5×127
            # process: seal c10x Tier-0 if feasible, extend gen_modmul cap to 10, seal one c10x-consuming multiplier
            # output: 1 Tier-0 module(c10x) + 1 Tier-0 app(cmul2_mod635)
            # criteria: independent cnx_perm(10) hash match · c10x dependency proven · no full Shor claim · regression green
        W12_15_Shor635StructuralFrontier // c10x payoff to Shor-635 structural app (done) @dep:W12_14_C10xPrimitiveFrontier
            # input: c10x-enabled modular multiplier synthesis, h_gate, iqft8, app_assemble structural tier
            # process: seal remaining cmul{4,16,131,256}_mod635 Tier-0 + assemble shor635 Tier-1 structural
            # output: 4 more Tier-0 multiplier apps + 1 Tier-1 structural Shor app
            # criteria: N=635=5×127 · all required powers sealed · structural tier honestly marked · period readout illustrative
        W12_16_C11xPrimitiveReview // review-only next primitive frontier after shor635 (done) @dep:W12_15_Shor635StructuralFrontier
            # input: W12.15 gate/control data, current dense-oracle cost envelope, gen_modmul cap=10
            # process: scan whether c11x or an alternate decomposition is worth attempting; no seal by default
            # output: report-only go/no-go and finite successor recommendation
            # criteria: registry root unchanged · c11x feasibility bounded · no new primitive seal without separate task
        W12_17_C11xPrimitiveFrontier // c11x primitive + one representative N=1285 multiplier payoff (done) @dep:W12_16_C11xPrimitiveReview
            # input: W12.16 recommended target N=1285=5×257, current gen_modmul c11x blocker
            # process: seal c11x Tier-0 if feasible, extend gen_modmul cap to 11, seal cmul2_mod1285 only
            # output: 1 Tier-0 module(c11x) + 1 Tier-0 app(cmul2_mod1285)
            # criteria: independent cnx_perm(11) hash match · c11x dependency proven · no full Shor claim · regression green
        W12_18_C11xPayoffFamily // remaining N=1285 multiplier payoff family (done) @dep:W12_17_C11xPrimitiveFrontier
            # input: N=1285=5×257, a=2, c11x-enabled gen_modmul, unique powers [2,4,16,256]
            # process: seal remaining cmul{4,16,256}_mod1285 Tier-0 exact apps
            # output: 3 more Tier-0 multiplier apps for the representative c11x-class family
            # criteria: independent arithmetic u_hash 3/3 · c11x consumed where max_control=11 · no full Shor claim
        W12_19_Shor1285StructuralFrontier // c11x payoff to Shor-1285 structural app (done) @dep:W12_18_C11xPayoffFamily
            # input: complete N=1285 payoff family, h_gate, iqft8, app_assemble structural tier
            # process: assemble shor1285 = H^8 · controlled-U^(2^j)[powa] · iqft8
            # output: 1 Tier-1 structural Shor app(shor1285)
            # criteria: N=1285 · all children sealed · structural tier honestly marked · period readout illustrative
            # ✅ done: shor1285 Tier-1 STRUCTURAL n_sys=19, indep arith 4/4, root df18e3ef→5aee6ef2, 76모듈·146앱
        W12_20_C12xPrimitiveReview // review-only next primitive frontier after shor1285 (done) @dep:W12_19_Shor1285StructuralFrontier
            # input: W12.19 frontier state, current dense-oracle cost envelope, gen_modmul cap=11
            # process: scan c12x feasibility and [2048,4095] semiprime targets; no seal by default
            # output: report-only go/no-go and finite successor recommendation
            # criteria: registry root unchanged · c12x feasibility bounded · no new primitive seal without separate task
        W12_21_C12xPrimitiveFrontier // c12x primitive + one representative N=3683 multiplier payoff (done) @dep:W12_20_C12xPrimitiveReview
            # input: W12.20 recommended target N=3683=29×127, current gen_modmul c12x blocker
            # process: seal c12x Tier-0 if feasible, extend gen_modmul cap to 12, seal cmul2_mod3683 only
            # output: 1 Tier-0 module(c12x) + 1 Tier-0 app(cmul2_mod3683)
            # criteria: independent cnx_perm(12) hash match · c12x dependency proven · no payoff family/full Shor claim · memory guard green
            # ✅ done: c12x Tier-0 n_sys=13, cmul2_mod3683 Tier-0 gates=1848 max_control=12 c12=45, root 5aee6ef2→1134ea04, 77모듈·147앱
        W12_22_C12xPayoffFamily // remaining N=3683 multiplier payoff family (done) @dep:W12_21_C12xPrimitiveFrontier
            # input: c12x primitive (W12.21), gen_modmul cap=12, NEW_POWERS=[4,16,256,2925]
            # process: seal cmul{4,16,256,2925}_mod3683 Tier-0 exact permutation app seals (no new module)
            # output: 4 Tier-0 apps; independent arithmetic hash match 4/4; full Shor-3683 deferred to W12.23
            # criteria: max_control=12 · c12x in deps · independent cmul hash match · no Shor claim
            # ★자율 루프 가동(AutonomyLoop frontier-c12x-payoff). ✅ done: cmul4/16/256/2925_mod3683 Tier-0, indep 4/4.
        W12_23_Shor3683StructuralFrontier // c12x payoff to Shor-3683 structural app (done) @dep:W12_22_C12xPayoffFamily
            # input: complete N=3683 payoff family, h_gate, iqft8, app_assemble structural tier
            # process: assemble shor3683 structural (counting t=8, work=12, 20q); verify children sealed; no re-seal
            # output: 1 Tier-1 STRUCTURAL app (shor3683, 20q); readout illustrative ord_3683(2)=28 -> [29,127]
            # criteria: 20q>EXACT_BOUND -> structural only · deterministic reassembly · cmul children Tier-0 exact · no dense claim
            # ✅ done(자율 루프): shor3683 Tier-1 structural 20q deterministic=True, root 1134ea04->85cdc459, 77모듈·152앱, structural 6->7.

    TrackMaintenance // execution infrastructure and compact handoff maintenance (in-progress)
        M1_ReproduceStepRegistry // reproduce_all frontier steps registry화 (done)
            # process: FRONTIER_STEPS declarative list in scripts/reproduce_all.py
            # criteria: reproduce_all remains REPRODUCED and includes c10x_frontier
        M2_DocSyncBatch // external docs batch sync — 현재 누적 없음, 재발작업 (done) @dep:정욱님_동기화_지시
            # scope: README.md, EXTERNAL-ONBOARDING.md, docs/QuantaFoundry-Technical-Spec.md
            # criteria: only run on explicit "동기화"
            # ✅ 2026-06-30 sync: W12.1~M4 반영(77모듈·147앱·root 1134ea04·second_oracle 71/71·fingerprint 285/285), task_record 초기화. 다음 누적 시 재개.
        M3_BacklogCompactionAudit // HANDOFF/remain/task_record size and stale-state audit (done)
            # process: scripts/backlog_compaction_audit.py
            # output: .pgf/maintenance/BACKLOG-COMPACTION-AUDIT.json
            # criteria: line budget and current-state marker checks pass
        M4_PostW12ExternalBridgeDesign // W12.21 frontier evidence → EXT unblock map (done)
            # process: design-only mapping from c12x/cmul2_mod3683 evidence to CI pilot/runtime keys/backend sidecar/ServerLink
            # criteria: no external execution · no external docs batch sync · unblock conditions explicit
            # ✅ done: .pgf/external/POST-W12-EXT-BRIDGE.json maps all EXT blockers and trigger-based next actions

    TrackInfra // 장기 자율 실행 인프라 — AutonomyLoop (in-progress)
        AutonomyLoop_Design // 단독 자율 루프 PG 설계+시뮬검증 (_workspace/loop) (done)
            # 산출: DESIGN-AutonomyLoop.md(Gantree+PPR+§8 정교화 4 decomposed)·persona_contexts.md·sim×3
            # 검증: sim_autonomy_loop_v2(T1~T12)·sim_persona_diversity(D1~D5)·sim_seal_cycle ALL PASS
            # 신뢰근원=결정론 게이트(INV3 self-judge 금지). 정지조건4+불변가드(INV1/2). H1 cross-runtime 상실 정직표기.
        AutonomyLoop_MVP // mock→실게이트 연결 1라운드 (done) @dep:AutonomyLoop_Design
            # process: run_seal_cycle·reproduce_all·doc_sync·commit·push mock 을 실제 스크립트/git 로 교체
            # frontier·EXT 무관 인프라 자율작업. ★구현=_workspace/loop/autonomy_loop.py.
            # criteria: 1라운드 실제 자율 수행 · 결정론 게이트 통과분만 commit/push(verified-only) · root 불변 or 가산만
            # ✅ done 2026-06-30: autonomy_loop.py 실러너(bootstrap snapshot·machine_gate 4게이트 subprocess·
            #   guard_check fingerprint+frozen byte-identical·verified-only sync_checkpoint 先브랜치). infra 1라운드
            #   실가동 → reproduce_all REPRODUCED·root 1134ea04 불변·invariants_held=True. autonomy-loop/mvp 브랜치 commit/push.
        AutonomyLoop_Activate // 트리거 시 자율 가동 (done) @dep:AutonomyLoop_MVP
            # 트리거=(MVP완료 ✅)or(정욱님 새 방향/frontier 해금)or(EXT unblock). 없으면 frontier-exhausted 정직 종료.
            # ★2026-06-30 정욱님 전면 승인: 구 INV7(NoAutoFrontier) 삭제. frontier·커밋·푸쉬·동기화·방향선택 자율 진행.
            # ✅ 2026-07-01: 2-tier verify(incremental ~46s/full)·EOL 유령 자동복원·출력버퍼링 완화·main 직접 모드 self-improve.
        AutonomyLoop_SelfImprove // 자율 루프 self-improvement (실측 마찰 검토→수정) (done) @dep:AutonomyLoop_Activate
            # process: reproduce_all 450s 병목→GATES_INCREMENTAL(46s) + commit-guard(full만 verified-commit) ·
            #   clean_eol_ghosts(autocrlf 유령 자동복원) · stdout 라인버퍼+progress() · main 직접 push
        W12_24_FrontierFactory // 파라메트릭 Shor frontier 봉인 폐루프 (in-progress) @dep:AutonomyLoop_SelfImprove
            # design: _workspace/loop/DESIGN-FrontierFactory.md (PG Gantree+PPR+3관점 review)
            # impl: scripts/frontier_factory.py — c{11,12}x_payoff/shor{1285,3683} 템플릿을 N-파라미터 함수로 추출
            #   (자유 codegen 아님). seal_payoff_family·seal_structural_shor·factory_seal·verify_against_sealed.
            # ★INV-F1 회귀게이트: factory 가 기존 봉인 7N(91~3683) byte-identical 재현 → 통과 후에만 신규 N 봉인(안전).
            # 자율발견 next_unsealed_target + reproduce_all 데이터-주도 factory-step(INV-F5).
            # ✅ 폐루프 실가동(autonomy_loop --mode frontier-factory): 자율발견 N=69,77 → cmul payoff Tier-0 +
            #   shor{69,77} Tier-1 structural 15q 봉인. 신규 모듈 0(c7x 재사용). 회귀 7/7·independent arith·deterministic.
            # criteria: 회귀 byte-identical · 신규 모듈 0 · structural n_sys≥15(dense-exact 침범 금지) · reproduce REPRODUCED

    TrackV08_ProofCarrying // 8-review 통합 실행 — 부채상환→수평unlock→발견 (in-progress) @dep:W12_24_FrontierFactory
        # 설계: _workspace/integrated_roadmap.md(8-review 통합) + _workspace/execution_plan_v08.md(실행계획).
        # 착수순서(feasibility×독립성): V08_1→V08_4(병행)→V08_5→V08_6/7/8→V08_9→V08_10.
        # 불변 상속: fingerprint 2파일·frozen 23키·기존 sealed byte-identical. 신규검증=sidecar/외부스크립트(oracle 무수정).
        V08_1_PermSubspaceContract // Shor modexp 코어 부분공간 순열 강검증 sidecar (done)
            # input: shor69~3683 9개 structural 앱의 modexp 코어(H·iQFT 제외 controlled-cmul 시퀀스)
            # process: pathA=회로 배선대로 cmul→MCT 게이트 전개 순열 시뮬(비트연산) vs pathB=정수산술 w·a^c mod N(독립)
            # output: scripts/perm_subspace_verify.py(전수/표본 + 2종 teeth + --quick) + .pgf/proofs/<app>.subspace_proof.json
            # criteria: exact 순열 · dense 2^total 미실체화 · negative control reject · root 불변(sidecar만)
            # ✅ done: 9/9 verified. 전수 7개(shor69~635, shor635=262144/262144) + 표본 2개(shor1285 19q·shor3683 20q,
            #   4099/4099). teeth=배선mutation + 틀린산술(a+1) 이중. reproduce_all 에 --quick 스텝 통합(root 무영향).
        V08_2_StructuralAppPromotion // shor69~3683 9개 structural→subspace 강화 (done) @dep:V08_1
            # process: shor 상위앱의 modexp 코어를 직접 부분공간 순열 강검증(자식 cmul은 이미 dense EXACT였음 —
            #   실제 gap=조립된 배선이 올바른 modexp 순열을 내는가; structural=배선기록만, P0=배선의미 확인)
            # criteria: 9개 앱 subspace_permutation_verified · INV-R5 정직표기(H·iQFT 포함 전체 unitary 미검증) · 비파괴
            # ✅ done: 9개 전부 subspace_permutation_verified 격상. structural_wellformed 잔존 app=0.
        V08_3_SemanticGuaranteeSplit // 새 등급(subspace_permutation_verified) 비파괴 레이어 (done) @dep:V08_2
            # criteria: SEMANTIC-GUARANTEES 비파괴 가산 · "structural≠dense≠subspace" 표기 · reproduce REPRODUCED
            # ✅ done: semantic_guarantee.py 격상 로직 추가. headline app subspace_permutation_verified=9.
        V08_4_HonestyHardening // 결정론≠정확성 명시·metric split·resource witness (done)
            # criteria: INV-R1/R7 문서·출력 명시 · seal resource 회로 대조(X_ResourceWitness) · root 불변
            # ✅ done: scripts/resource_witness.py — 조립앱 resource==자식 resource 합 독립재계산(A6).
            #   166/166 consistent(61 golden-only skip), structural Shor 9/9. reproduce_all에 --quick 통합.
            #   INV-R1 배너(reproduce 출력)·README Honest boundaries 갱신(REPRODUCED≠correct, subspace 등급).
        V08_5_InvertedSecondOracle // 규약(전역위상·atol) 변주 하 seal 재현 실증 (done) @dep:V08_2
            # criteria: 규약-변주 하 seal 재현/불일치 명시 · frozen 23키 무수정 · 관측 문서화
            # ✅ done: scripts/inverted_second_oracle.py — 71/71 모듈 규약-독립 재현(전역위상·atol 격자 변주 불변
            #   + teeth: 상대위상·격자밖 섭동은 불일치). endian=규약-고정(big, 정직표기). reproduce_all 통합.
            #   sidecar .pgf/proofs/CONVENTION-INDEPENDENCE.json. A3 최약가정(공유 규약 오류) 직접 타격.
        V08_6_ConventionAuditFirst // block-encoding 규약 감사 선행 (done) @dep:V08_2
            # ✅ done: scripts/blockencoding_audit.py — 규약(ancilla=MSB·top-left block==A/α·big-endian·α정규화)
            #   관측. be_xz top-left block==(X+Z)/2 확인 + teeth(다른 관측가능량 Y 불일치). sidecar
            #   BLOCKENCODING-AUDIT.json. seal 아님(봉인은 app_assemble). reproduce_all 통합.
        V08_7_BlockEncodingLCU // 소형 Hermitian block-encoding + Pauli LCU (Tier-0) (done) @dep:V08_6
            # ✅ done: be_xz.app.pg — block-encoding of (X+Z)/2 via LCU(½X+½Z), 2q(1anc+1sys). U=PREP·SELECT·PREP,
            #   PREP=H, SELECT=|0><0|⊗X+|1><1|⊗Z. plan=봉인 게이트만(h·anti-cX·cz·h), MatrixGate 0. Tier-0 EXACT
            #   u_hash 998b5b8f. 새 module 0(h/x/cnot/cz 재사용). 신규 앱 +1.
        V08_8_QSPPolynomial // QSP 위상열(저차 Chebyshev) — 근사=observation (done) @dep:V08_7
            # ✅ done: qsp_d1.app.pg — QSP degree-1(Wx conv), 1q. U=e^{iπZ/8}·W·e^{iπZ/8}, W=e^{iπX/8}(rx_negpi4).
            #   plan=[rz_negpi4,rx_negpi4,rz_negpi4], 새 module 0(재사용). Tier-0 EXACT u_hash 36cd989b.
            #   ★다항식 P(a) sweep=observation(INV-Q3, seal 아님). 신규 앱 +1. root a0b4f678→480876220a204f6d.
        V08_9_CISealGateAction // GitHub Action: verify+reproduce+root gate (done) @dep:V08_2
            # ✅ done: .github/workflows/seal-gate.yml 강화. ★근본 fix=anchor drift 제거(정적 앵커
            #   d231fbf4 하드코딩 2곳 삭제 → seal_gate_ci EXPECT_DEFAULT=anchor_sync 관리값 사용, CI 영구 최신).
            #   V08 게이트 추가(convention_independence·resource_witness 명시 스텝 + perm_subspace=reproduce 내부).
            #   second_oracle 71/71 라벨 정정. root 대조=seal_gate 스텝 단일화.
        V08_11_QSVTCombination // block-encoding + QSP 결합 = 고유값 변환 (done) @dep:V08_7,V08_8
            # ✅ done: QSVT 최고 compounding("one seal, many algorithms")의 실질 payoff — 분리된 부품(be/qsp)을 결합.
            #   be_proj.app.pg — block-encoding of |0><0|=(I+Z)/2(h·cz·h, Tier-0 2776579e). ★스펙트럼 비축퇴(A²=A)
            #   라 be_xz(A²=I/2 축퇴, 다항식 붕괴)와 달리 QSVT non-trivial. qsvt_proj_d2.app.pg — QSVT d=2:
            #   e^{iφZ_a}·be_proj·e^{iφZ_a}·be_proj·e^{iφZ_a}(projector-controlled rotation=rz_negpi4[ancilla]).
            #   top-left block=P(A) 고유값변환(1→e^{iπ/8}, 0→e^{-iπ/8}), Tier-0 0cad930c, 새 module 0. blockencoding_audit
            #   확장(be_proj block==diag(1,0)·qsvt block==P(A) non-trivial). P sweep=observation(INV-Q3). root 성장.
        V08_21_H2MoleculeChemistry // 실제 분자 H₂ 양자화학 (봉인 fermionic 자산 조합, observation) (done) @dep:V08_19
            # ✅ done: 미래 QPC 킬러앱(양자화학) hello-world. H₂ STO-3G 2-qubit 축약 Hamiltonian(O'Malley 2016)=
            #   g₀I+g₁Z₀+g₂Z₁+g₃Z₀Z₁+g₄X₀X₁+g₅Y₀Y₁. ★H₂=봉인 fermionic 자산 조합: hopping X₀X₁+Y₀Y₁=2·be_hop_A
            #   (봉인 block-encoding)·Z항=be_num 류. h2_molecule_observe.py — ground energy -1.85(illustrative 계수)+
            #   결합 해리 곡선(hopping↓→energy↑). ★계수=고전 양자화학 적분(illustrative), 구조=봉인 block-encoding,
            #   ground/curve/e^{-iHt}=observation(INV-Q3). **신규 봉인 0(be_hop·be_num 재사용), root 4bd59119 불변**.
        V08_20_FTQCMagicState // FTQC non-Clifford universality (magic state + T-injection) (done) @dep:V08_19
            # ✅ done: project-identity 마지막 미완 핵심축(FTQC 자산). QEC(W7)는 transversal Clifford(H/S/CNOT)까지만
            #   → universality 엔 non-Clifford T 필요. magic state 가 T 를 fault-tolerant 주입. magic_a.app.pg —
            #   |A>=T·H|0>=(|0>+e^{iπ/4}|1>)/√2 준비(plan=[h·t], Tier-0 8b8b7d24, 새 module 0). magic_state_observe.py —
            #   (1)non-stabilizer witness: max stab fidelity=cos²(π/8)=0.8536<1→Clifford 궤도 밖(magic)+teeth;
            #   (2)T-injection EXACT: |ψ>⊗|A>·CNOT·측정·S보정→T|ψ>(모든 입력·측정결과); (3)Clifford(W7)+T(magic)=universal.
            #   ★magic_a=Tier-0 EXACT, non-stabilizer·injection=EXACT 독립검증. distillation=하드웨어 범위 밖(정체성).
            #   root a177da0c→4bd5911945ac6dcb(180→181). ★project-identity 4대 방향(structural강검증·독립성·발견자율화·
            #   FTQC자산) 전부 실증 도달.
        V08_19_SpinfulFermiHubbard // 정통 spinful Fermi-Hubbard 2site×2spin (fermionic 축 정점) (done) @dep:V08_17
            # ✅ done: 정통 Fermi-Hubbard(응집물질·양자화학 대표). 4 modes(0↑,0↓,1↑,1↓). H=-t·Σ_σ hopping_σ +
            #   U·Σ_j n_j↑n_j↓. same-spin hopping 비인접(0↑-1↑ 사이 mode)→JW Z-string. be_hopz.app.pg — 비인접
            #   hopping (X⊗Z⊗X+Y⊗Z⊗Y)/2 block-encoding(Z_1=JW Z-string, YZY=(S⊗I⊗S)(XZX)(S†⊗I⊗S†), h·sdg·cnot·cz·s·x,
            #   4q, block==A, Tier-0 b3bea4c4, 새 module 0). spinful_hubbard_observe.py — 4-mode JW 반교환 EXACT +
            #   스펙트럼 vs U + ★Mott 물리(U↑→ground energy↑ -2→-1, 이중점유 억제·국소모멘트). 봉인=be_hopz·be_num.
            #   ★JW=EXACT, e^{-iHt}=observation(INV-Q3). root 848e83d7→a177da0c33f84d8c(179→180).
        V08_17_FermiHubbardModel // 완전한 t-V Fermi-Hubbard (be_hop hopping + be_num interaction) (done) @dep:V08_16
            # ✅ done: fermionic 축을 완전한 물리 모델로. H=-t(a0†a1+a1†a0)+V·n0·n1 --JW--> -t(XX+YY)/2+V(I-Z0)(I-Z1)/4.
            #   be_num.app.pg — number operator n=(I-Z)/2=|1><1| block-encoding((I⊗X)be_proj(I⊗X)=X켤레, x·h·cz·h·x,
            #   Tier-0 5e63b4f5, 새 module 0). hubbard_observe.py — number op JW성질(commuting projector n²=n)·
            #   interaction n0·n1=|11><11|(double-occupancy) EXACT + teeth(잘못된 n=(I+Z)/2). 스펙트럼 {-1,0,1,V}
            #   (V=이중점유 에너지, 물리 정확). 봉인자산=be_hop(hopping)+be_num(number). full H=Pauli합→QSVT Ham-sim.
            #   ★JW성질=EXACT, 봉인=be_hop·be_num, e^{-iHt}=observation(INV-Q3). root 58e5af8e→53f10210f1a134ae(177→178).
        V08_18_QSVTMatrixInversion // QSVT consumer: matrix inversion (선형대수, trilogy 완결) (done) @dep:V08_15
            # ✅ done: QSVT consumer trilogy 완결(물리 Ham-sim + 검색 amp-amp + 선형대수 matrix inversion).
            #   qsp_d5.app.pg — QSP degree-5 홀수(6×rz_negpi4·5×rx_negpi4, Tier-0 cfff54e1, 새 module 0)=1/x 근사
            #   기본블록. matrix_inversion_observe.py — well-conditioned A=(3I+XX+ZZ)/4(고유값 0.25,0.75,1.25 κ=5)
            #   에 odd polynomial P(A)≈c·A⁻¹: degree 1→0.95·3→0.83·5→0.0(고유값3개→degree-5 홀수 3항 보간 exact).
            #   QSP realizes qsp_d1/d3/d5. ★0 고유값 발산→well-conditioned 한정(honest). 봉인=정확 QSP 홀수,
            #   1/x 근사=observation(INV-Q3). root 53f10210→848e83d75ac87f7a(178→179).
        V08_16_FermionicSimJW // Fermionic simulation: Jordan-Wigner mapping (새 수평축) (done) @dep:V08_13
            # ✅ done: 새 수평축(미래 QPC 양자화학). 물리 연산자→Pauli(JW)→block-encoding→QSVT/Trotter Ham-sim 연결.
            #   JW: a_j=(∏_{k<j}Z_k)(X_j+iY_j)/2. be_hop.app.pg — 2-site hopping a_0†a_1+a_1†a_0=(X⊗X+Y⊗Y)/2
            #   block-encoding(YY=(S⊗S)(XX)(S†⊗S†), h·sdg·cnot·s·x 조립), 3q, block==H, Tier-0 7994e80c, 새 module 0.
            #   ★commuting XX·YY→고유값 -1,0,0,1 비축퇴. fermionic_jw_observe.py — 반교환 {a_i,a_j†}=δ_ij·{a_i,a_j}=0
            #   보존 EXACT 검증 + Z-string teeth(잘못된 매핑 위반). ★JW보존=EXACT(항등식), 봉인=be_hop, e^{-iHt}=
            #   observation(INV-Q3). be_hop→QSVT Ham-sim(V08_14 재사용). root 0e0a1e21→58e5af8edf801d96(176→177).
        V08_15_QSVTAmpAmpConsumer // QSVT consumer: amplitude amplification = QSP 홀수 다항식 (done) @dep:V08_8
            # ✅ done: QSVT consumer 축 완결(Ham-sim=물리 + amp-amp=검색). amplitude amplification 의 진폭증폭
            #   a=sinθ→sin((2k+1)θ)=진폭의 홀수다항식(deg 2k+1)=QSP 실현. qsp_d3.app.pg(degree-3 홀수=k=1
            #   기본블록, 4×rz·3×W, Tier-0 942f93e2, 새 module 0). qsvt_ampamp_observe.py — Grover 증폭프로파일
            #   sin²((2k+1)θ) 고전관측(a0=0.5,k=1→P=1.0; qsp_d1=k0/qsp_d3=k1). 기존 W9 amp-amp/qae 를 QSP 로 통합.
            #   ★observation(INV-Q3): 봉인=정확 QSP 홀수 다항식, 증폭프로파일=관측. root 1c748ac0→0e0a1e212c76c701(175→176).
        V08_14_QSVTHamSimConsumer // QSVT consumer: Chebyshev Hamiltonian simulation 관측 (done) @dep:V08_13
            # ✅ done: "QSVT=여러 알고리즘의 통합틀"을 실제 알고리즘(Hamiltonian sim)으로 연결. QSVT 는 block-encoded
            #   A 의 Chebyshev T_k(A) 를 정확 실현: qsvt_pauli2_d3(홀수 Chebyshev, 1→i·-1→-i·0→0, Tier-0 a45c169c;
            #   d2 짝수와 상보=e^{-iAt}=cos(At)-i sin(At) 성분). qsvt_hamsim_observe.py — e^{-iAt}=Chebyshev급수
            #   (Jacobi-Anger) 고전관측: A=(XX+ZZ)/2 고유값3개→degree-2 Chebyshev에서 exact(‖P_d-e^{-iAt}‖ 0→0).
            #   ★observation(INV-Q3, seal 아님): 봉인=정확 Chebyshev블록, e^{-iAt}일치는 관측. 이 A는 commuting→
            #   Trotter도 exact(QSVT이점=일반 비가환A 점근, 정직표기). root 8fcd78→1c748ac02ebb21f0(174→175 apps).
        V08_13_BlockEncoding2Q // 2-qubit Hermitian block-encoding (Pauli LCU) + 2q QSVT (done) @dep:V08_11
            # ✅ done: abstraction layer 상승(1q→2q Hermitian, Hamiltonian 표준표현). be_pauli2.app.pg —
            #   A=(X⊗X+Z⊗Z)/2 Pauli LCU, 3q(1anc+2sys). ★commuting Paulis(XX·ZZ 교환)→A²≠∝I 비축퇴(고유값
            #   -1,0,0,1); anticommuting(예 ZI+XX)은 A²∝I 축퇴로 부적합(numpy 선검증). block==A, Tier-0 4586c515.
            #   plan=h·cz·cz·x·cnot·cnot·x·h, 새 module 0. qsvt_pauli2_d2.app.pg — 2q QSVT d=2, block=P(A)
            #   4고유값을 |λ|별 변환(P(±1)=e^{iπ/4}e^{iπ/8}·P(0)=e^{iπ/4}e^{-iπ/8}), Tier-0 1128aa76. audit
            #   eigenvalue-profile 보강(non-diagonal block 대응). root 6cb370→8fcd78afea65d823(172→174 apps).
        V08_12_QSVTPolynomialFamily // one seal(be_proj) → many algorithms(다른 φ→다른 P(A)) (done) @dep:V08_11
            # ✅ done: "one seal, many algorithms" compounding 실증. 같은 be_proj block-encoding + 다른 위상열:
            #   qsvt_proj_d2b(φ=π/16, P(1)=e^{i3π/16}·P(0)=e^{iπ/16}, Tier-0 bd45eec0)·qsvt_proj_d3(d=3 홀수,
            #   P(1)=i·P(0)=0 projector-like 필터, Tier-0 8ffa3e24). 새 module 0. blockencoding_audit family 확장
            #   (one_seal_many_algorithms: be_proj→3 distinct P(A), distinct_P=True). P profile=observation(INV-Q3).
            #   root 5f89297→6cb370b86f88d33e(170→172 apps). 앵커 동기화.
        V08_10_DiscoverySuperopt // 봉인 golden에 더 싼/새 분해 탐색(oracle-gated) (done) @dep:V08_7
            # ✅ done: scripts/discovery_superopt.py — 기존 decomp_optimizer(reward만)에 **탐색 엔진** 추가.
            #   BFS(깊이제한, visited pruning) over 봉인 primitive 팔레트 → up-to-phase 매칭 → 발견 시퀀스를
            #   decomp_optimizer.oracle_reward(재봉인 u_hash==target 하드게이트)로 검증. cz→h·cnot·h·(len3),
            #   swap2→3×cnot 자동 발견(reward 1.77, nc_fail teeth). 자유 codegen 아님(golden 이미 봉인, INV-S1).
            #   임시 store+specs/apps 임시 spec 정리 → registry/frozen/root 불변(신규 봉인 0). reproduce_all 통합.

    TrackHE // 수평확장 — 외부 8런타임 제안 통합(6축 A–F), he_task_plan 단일지시 자율실행 (in-progress) @dep:TrackV08_ProofCarrying
        # 정본: _workspace/integrated_horizontal_expansion.md(통합설계)·_workspace/he_task_plan.md(PPR 실행계획).
        # 2026-07-02 세션: 10커밋(939e502~591a2b2+체크포인트) · root 4bd59119→36f8bc09 · 181→190 apps · 전 구간 새 module 0.
        H1_BKEncoding // #axis-A 대체 페르미온 인코딩(8/8 합의 최우선) (done)
            # ✅ bk4_transform(BK-2002 U_BK, GF(2) permutation→cnot 4-gate, Tier-0 16×16) ·
            #   bk_num1((I−Z0Z1)/2)·bk_hop01(X0(I−Z1)/2) block-encoding · bk_equiv_observe(★payoff
            #   H_03: JW w4→BK w3, 켤레변환=exact·weight감소=관측) · parity4_transform(cnot 6-gate)+
            #   parity_taper_observe(number/hopping이 총-parity Z_{n-1}과 교환+q3에 I/Z만→taperable).
        H2_MolecularSeal // #axis-B 분자 봉인 pack (in-progress)
            # ✅ H2.1 be_h2: H₂ 부호구조 block-encoding — dyadic uniform LCU(정욱님 승인 방향),
            #   block=(−I+X0X1+Y0Y1+Z0Z1)/4 부호정확, PREPARE=H⊗H·SELECT 4-branch. 봉인=dyadic 계수 하
            #   exact; 실제 계수·ground energy=관측(h2_molecule_observe 유지).
            # 잔여: H2.2 self-contained integral(dyadic 경로로 필요성↓)·H2.3 be_lih.
        H3_FTQCNonClifford // #axis-C non-Clifford 3부작(물리→공장→논리) (done)
            # ✅ H3.1 code513_encoder: ★[[5,1,3]]=C₅ 오각형 graph code 통찰 → GHZ·H^5·CZ(오각간선)
            #   순수 팔레트, Tier-0 32×32. distill5to1_observe(coherent-branch): T-type^⊗5→syndrome-0
            #   출력 |r|=1 순수 exact magic(축 twist 문서화)·p=1/6 닫힌형·teeth.
            # ✅ H3.2 steane_encoded_t_observe(신규 봉인 0): 논리 T-injection — |ψ_L>⊗|T_L>→transversal
            #   CNOT→논리Z branch→S_L 보정((S†)^⊗7=논리S 검증). branch0/1 모두 T_L|ψ_L> exact·p=1/2.
            #   Eastin-Knill: transversal T 부재→magic-injection이 유일 정직 경로. 14q 벡터만(dense 미실체화).
            # H3.3 lattice surgery: surface-code 자산 부재로 연기 판단(선행 자산 필요).
        H4_DataOracle // #axis-D generic data oracle (done)
            # ✅ qrom22(|i>|d>→|i>|d⊕data[i]>, X-켤레 toffoli, perm)·select_prepare4(전 4종 Pauli 단일
            #   SELECT, block=(I+X+Y+Z)/4 비축퇴, Y=S·X·S† 켤레; blockencoding_audit 편입 n_anc=2 일반화).
            #   qROM(하부)+SELECT-PREPARE(상부)로 축 폐합 — be_* 들이 템플릿 인스턴스로 재해석.
        H5_RepnBasis // #axis-E 표현론/비아벨 — 오라클→Fourier→HSP 완결 (done)
            # ✅ H5.1 s3_mult: 첫 비아벨군(S₃) 곱셈 오라클 — 반직접곱 닫힌형(a+(−1)^b c mod3, b⊕d):
            #   CNOT·fredkin(mod-3 부정=비트스왑)·X-켤레 c3x. C4=Cayley·순열합성 독립검증. Tier-0 64×64.
            # ✅ H5.2′ d4_mult+d4_qft: ★게이트 우회 — S₃는 ω(비-dyadic)로 막혔으나 D₄ 회전군=Z₄→위상{±1,±i}
            #   팔레트 안. d4_mult(8원소=3q 정확, cnot·toffoli 5게이트 오버플로 가산기)·d4_qft(첫 비아벨 Fourier,
            #   F=anti-CH∘(QFT_Z4⊗I), 봉인 qft2+ry 재사용). golden=기약표현 공식·Peter-Weyl 블록 검증. 새 module 0.
            # ✅ H5.2′ payoff d4_hsp_observe(봉인 0): 이면군 HSP 소비 — coset state→d4_qft→irrep 분포,
            #   g-불변·문자론 독립참조 일치·비정규{e,s} vs 정규{e,r2} 구별(↔격자문제 연결점).
            # 잔여: H5.3 Schur-Weyl — CG 계수 비-dyadic(√⅔)→신규 module 다수=he_task_plan §4 사람 게이트(승인 대기).
        H6_Exploratory // #axis-F qudit 개창(임베딩 우회)·MPS/bosonic 잔여 (in-progress)
            # ✅ H6.1′ qutrit_x3+qutrit_sum: ★게이트 우회 — qutrit(3레벨)을 qubit 부분공간 {00,01,10}에
            #   임베딩(|11>=sink) → 오라클 표준 2ⁿ 프레임 유지, "차원≠2ⁿ" 진입 게이트 소멸. 삼진 산술(순열)만
            #   exact: X₃(+1 mod3, anti-CX×2)·SUM((a+b)mod3, ctrl-X₃/X₃²=c3x 켤레). qutrit_arith_observe:
            #   X₃ 위수3·궤도·SUM 교환/영원 + 게이트경계(ω=e^{2πi/3}·1/√3: Z₃/QFT₃/Bell₃=차기). C4=정수 삼진산술.
            # 잔여(게이트): qutrit QFT₃/Z₃(ω)·MPS(AKLT χ=2)·bosonic(절단근사) — 신규 module 다수=he_task_plan §4.

    TrackHE2 // 2차 수평확장 — 외부 8런타임 report2(23제안)→통합6축(P1–P6) 자율실행 (in-progress) @dep:TrackHE
        # 정본: _workspace/integrated_horizontal_expansion2.md(통합)·he_task_plan2.md(PPR 실행계획, 회로확정 명세).
        # 2026-07-03: 11커밋 · root eedb7aa8→d5557622 · 194→205 apps · 전 구간 새 module 0. ★시그니처=게이트 우회.
        P1_SurfaceLatticeSurgery // #TOPO 위상적 논리연산 (done)
            # ✅ surf422_encoder([[4,2,2]] CSS)·surf_ls_merge_zz(coherent Z_L⊗Z_L 병합)·toric22_gs(위상질서)·
            #   logical_stack_observe(완전 FTQC 논리스택: magic→증류→논리T→논리큐빗→lattice surgery). v1 H3.3 완성.
        P2_MBQC // #MBQC 측정기반 계산 (done, 최다합의 7)
            # ✅ cluster3x3_prep(2D 자원)·mbqc_h(측정패턴↔회로 등가, H 텔레포트 coherent)·mbqc_observe.
        P3_GF2k // #GF 유한체 특성-2 대수 (done)
            # ✅ gf4_mul(GF(4) 곱셈)·gf4_frob(Frobenius Z₂)·gf8_mulx(GF(8) primitive 7-cycle). 군≠체.
        P4_BraidAnyon // #ANYON 위상적 계산 (done)
            # ✅ ising_braid_b2(Majorana B₂ entangling)·braid_observe(Yang-Baxter B₁B₂B₁==B₂B₁B₂·Clifford).
        P5_QCA // #QCA discrete-time exact (done)
            # ✅ qca_step(Clifford brickwork 병진불변)·gnvw_index_observe(exact≠Trotter 근사·light-cone).
        P6_Exploratory // 탐색 (done)
            # ✅ fswap(fermionic SWAP, VC primitive §3b gap). AKLT=무리수 정규화(√41)→사람게이트(미봉인).
        V3_HumanGateApproved // 사람게이트 승인분(정욱님 2026-07-03: Schur module·ZX·Z2·qLDPC Tier-2) (done)
            # ✅ T2 z2gauge3: Z₂ 격자게이지 Gauss law encoder(H 켤레→반복부호, Clifford). z2gauge_observe.
            # ✅ T3 zx_verify: ZX Clifford fragment 3번째 독립 오라클 경로(rewrite 5종·재구성, 봉인0).
            # ✅ T4 qldpc_hgp: 하이퍼그래프곱 CSS [[8,1,2]]([3,1]×[2,1], Tier-2 승인을 소형 Tier-0로 우회, 새 module 0).
            # ✅ T1 schur3: 3-qubit Schur-Weyl transform 완성 — 탐색 아닌 ★직접 CG cascade(U=V2·G2·G1,
            #   2-level CCRy(arccos⅓) Givens ×2 + pair CG=CH 켤레). 승인 module 2개 봉인(ry_cg_half±,
            #   frozen/consensus 무훼손 재확인). golden=CG 계수 직접(회로 독립)·C-app exact.
            #   schur_observe: U†J²U·U†JzU 동시대각{3.75×4,0.75×4}+S₃ duality sector 보존+teeth.
            #   second_oracle 71→73/73. root c188d733→e6c60258(77→79 modules·207→208 apps).
        V4_AKLT // 사람게이트 승인(정욱님 2026-07-04): AKLT₄ 무리수 정규화(√41) (done)
            # ✅ aklt4: 4-site spin-1 AKLT VBS 준비 회로(9q=8 site+1 bond wire, Tier-0, plan 75스텝).
            #   ★직접 순차 조건화 등척(탐색 아님): 우측환경 R_j=E^{4−j}(|0⟩⟨0|) 전부 대각·유리수
            #   → site 분기 진폭² 유리수 → 신규 module 3각도×2 (ry_ak41/13/7±: arccos√(28/41)·√(8/13)·√(2/7)).
            #   ★복리: site3=ry_k5/ry_pi2/ry_pi4 기봉인 커버(π/2−arccos√(1/5) 합성)·site4=결정론 Clifford.
            #   aklt_observe: 독립 MPS 수축 exact(1e-16)+parent-H P⁽²⁾ 소멸 3/3+triplet+string order 관측
            #   +teeth(edge 축퇴=parent-H 불변이 정직·MPS-match만 edge 고정). second_oracle 73→79/79.
            #   root e6c60258→3790e617(79→85 modules·208→209 apps). n>4·PBC·bond>2 일반 MPS=차기.
        V5_ExtRound3Request // 외부 3차 제안 요청문(v1+v2+v3+V4 EXCLUDE) 작성·배치 (done)
            # ✅ .pgf/external/HORIZONTAL-EXPANSION-REQUEST-v3.md — self-contained, 봉인 0·root 불변.
            #   EXCLUDE 3c(v2 P1–P6·v3 T1–T4·V4 AKLT) 추가, §4′ 직접-구성 성공패턴(닫힌형 CG/환경 유도)
            #   + 승인-module 사람게이트 프로세스 명시. 수거=정욱님(외부 런타임 전달·회신 수집).
        V6_ChannelDilation // 열린 양자계(CPTP 채널) Stinespring dilation — 새 수평 클래스 (done)
            # ✅ 첫 non-unitary 계층: 채널을 확장 유니터리로 실체화(sys+env). ★1/2 감쇠점에서 각도가
            #   전부 dyadic(π/2·π/4) → 신규 module 0(기봉인 ry_pi2/pi4/negpi4·cnot 재사용).
            #   stinespring_bitflip(p½, Ry(π/2)_e·CNOT)·stinespring_phasedamp(λ½, CRY(π/2))·
            #   stinespring_ampdamp(γ½, CRY(π/2)·CNOT). 봉인=dilation 유니터리 Tier-0 exact(2q 4×4).
            #   channel_observe: Tr_env[U(ρ⊗|0⟩⟨0|)U†]==Kraus 채널 exact + CPTP(trace-preserve·ΣK†K=I)
            #   + teeth(틀린각). ★정직 경계: 채널=관측(비유니터리 초연산자, seal 아님).
            #   ★V6.2 심화(5490e8f): stinespring_depol(3q, 완전 depolarizing p=1=균일 Pauli twirl 4-Kraus,
            #   H⊗H env·CZ·CNOT, E=I/2, 신규 module 0) + 합성 compounding 관측(봉인 dilation 직렬→
            #   phase-damp½∘½==λ¾·amp-damp½∘½==γ¾). 일반 p<1(비-dyadic)·다큐빗·하드웨어 노이즈=차기.
        V7_ChannelQEC // 채널→QEC 완결 파이프라인 관측(봉인 자산 3축 결합) (done)
            # ✅ qec_channel_observe(신규 봉인 0·root 불변): repcode3(인코더)→stinespring_bitflip(채널
            #   오류주입)→syndrome3(신드롬)→코히런트 조건-X 정정→decode→논리 복원. ★bit-flip={√(1−p)I,
            #   √p X_i} 두 Kraus weight≤1→거리-3 exact 정정: R(E_i(Encode(ρ)))=ρ, 18 케이스 전부 1e-16.
            #   봉인 채널 링크 확인·전역 teeth(정정필요). 봉인=유니터리뿐, 채널·복원=관측(INV-Q3). 단일큐빗만.
        V8_Unitary2Design // 1q Clifford 군 전체 봉인 → 정확 unitary 2-design (자체 개창) (done)
            # ✅ 요청문 §4 첫 자체-발굴 후보(외부 3차 회신 부재 → 2-B 게이트). RB·shadow tomography 기반.
            #   설계(numpy 선검증): BFS words over {h,s} → C₁ 24원소(mod phase, 최대 word 6) 폐포 확인.
            # ✅ 봉인: cliff1_* 24개 앱(각 2×2 Tier-0 exact, plan=기봉인 h_gate/s_gate word, 항등원=h·h).
            #   ★신규 module 0 (§4′ 직접 닫힌형 — 유한군 전 원소가 기봉인 팔레트 word).
            #   ★재발견 6건 u_hash 일치 단언: h→h_gate·s→s_gate·ss→z_gate·sss→sdg_gate·hsh→sx(HSH=√X)·
            #   hssh→x_gate(HZH=X). 255→279 apps·root 331ba89a→262e0379d3fcbc89.
            # ✅ 관측(seal 아님, INV-Q3): twodesign_observe(3ad) — seal링크 24/24·유니터리·군 폐포(576곱 전수)·
            #   frame potential F₁=1·F₂=2(정확 2-design)·F₃=5(정확 3-design, d=2 Haar ∫|TrU|⁶=5 일치)
            #   기계정밀도 + twirl |0⟩⟨0|→I/2 + teeth(원소 제거 F₂=2.026·S→T 오염 F₂=2.015 검출).
            #   RB·shadow tomography 자체=미구현(기반만). 2q Clifford(11520)=차기(전수 비현실, 표본화 필요).

    TrackHE3 // 3차 수평확장 — 외부 8런타임 report3(35제안)→통합채점(12클러스터)→자율실행 4트랙 (done) @dep:TrackHE2
        # 정본: _workspace/integrated_horizontal_expansion3.md(통합채점)·he_task_plan4.md(PPR 실행계획).
        # 합의: 산술 8/8 만장일치·Szegedy 6/8·채널 6/8(V6 기봉인 중복→잔여 Choi만)·path-sum 3/8.
        # 자율실행분=신규 module 0 확정 4트랙. 사람게이트 6건(Fibonacci·Schur4·γ¼/POVM·Szegedy p¼·PEPS·2q design)=대기.
        H3_1_QuantumArithmetic // 명시적 정수 산술 1급 자산화 (done)
            # ✅ cuccaro_add2(6q 13스텝)/add3(8q 19스텝)(MAJ/UMA {cnot,toffoli})·draper_add2(4q,
            #   qft2+cs/cz 위상가산+iqft2 sub-app)·cmp2_ge(6q 19스텝, 보수 carry, ★정직사양 z⊕=[a≥b+cin]).
            #   golden=정수산술 순열(회로 독립). arithmetic_observe(3ae): 전수 정수 two-path(64/256/64/16)
            #   +★ripple==Fourier 교차-family(16)+합성 b+2a+teeth. 신규 module 0.
        H3_2_SzegedyWalk // Markov 연쇄 양자화 — 새 수평 클래스 (done)
            # ✅ szegedy_2state_p12(2q, R_A=I⊗(HZH), ★W→X⊗X Clifford 수축)·szegedy_c4_p12(4q 30스텝,
            #   ★복리 시그니처: V=ψ0-prep+draper_add2 sub-app, ADD†=X-켤레+increment 정직분해,
            #   reflect00 전역위상 −1이 R_B·R_A 에서 상쇄). golden=Szegedy 정의식(회로 독립).
            #   szegedy_observe(3af): 정의식 exact+스펙트럼 정리(위상⊆±2arccos λ_D)+정상 +1 고유벡터+teeth.
        H3_3_ChoiState // channel-state duality 자산화 (채널축 잔여 novelty) (done)
            # ✅ choi_bitflip/phasedamp/ampdamp(3q)·choi_depol(4q, ★J=I₄/4 극단)=Bell+기봉인
            #   stinespring_* sub-app 복리, 신규 module 0. choi_observe(3ag): J==Kraus-Choi·CP(J⪰0)·
            #   TP(Tr_sys J=I/2)·★duality(J→E 재구성==채널) exact+teeth. INV-Q3 상속(J·채널 성질=관측).
        H3_4_PathSumVerify // 4번째 독립 검증경로 — sum-over-paths 정수환 exact (done)
            # ✅ scripts/pathsum_verify.py(3ah): ℤ[ω₈]·(1/√2)^k 축차 경로합(부동소수 0 정수 연산)→dense
            #   golden 전역위상 정규화 대조. 8개 봉인 앱(bell~szegedy_2state) dev≤2e-16+teeth(T 오염 검출).
            #   봉인 0·oracle 무수정(봉인 판정 불참 sidecar). dense·tableau·ZX 다음의 4번째 수학 기반.
    TrackGate6 // 사람게이트 6건 단계별 개창 — 상세 계획서 .pgf/DESIGN-HumanGate6.md v1.1 (done — 2026-07-05 폐합) @dep:TrackHE3
        # ★v1.1=PGF 3관점 설계리뷰(P5/P7/P8, REVISE: C2·H5) 반영 개정: G1 PEPS RVB(module 0 확정)→
        #   G2 2q 2-design(★하한 226 가중 포함 유효→closed-negative 반증+MUB-20 state-design 대체 payoff)→
        #   G3 π/6 family(승인 1회→채널γ¼·Szegedy p¼ 확정+POVM 조건부 A6)→G4 Schur n=4(★arccos√(2/3)=
        #   ry_cg_half 동일 발견→module 0 가능성, G3b hard-dep)→G5 Fibonacci(★field 정정 ℚ(ζ₅,√φ) 차수 8,
        #   witness (σ₁σ₂)³=e^{2πi/5}I)→G6 종결(@dep=terminal: done/closed-negative/blocked-final).
        # ★승인 게이트=각도 확정 시점 명세 보고(.pgf/approvals/) 후 정욱님 승인(계획서 승인과 분리).
        #   a-노드(설계) 병렬 허용·c-노드(봉인) 직렬. 노드별 status 는 DESIGN-HumanGate6.md 가 정본.
        # ✅G1 폐합(peps22_rvb, root 7293a3de)·✅G2 폐합(2026-07-05): G2a closed-negative 반증
        #   (.pgf/proofs/TWOQ-2DESIGN-BOUND.json)+G2b MUB-20 state 2-design 20앱 봉인(규모 게이트
        #   정욱님 승인, 신규 module 0, mub_observe 3aj) → 310 apps·root b82d79eb24d14ee5.
        # ✅G3 폐합(2026-07-05): 승인 module 2(ry_pi6/negpi6, .pgf/approvals/G3-ry_pi6.md 정욱님 승인)
        #   → 소비 5앱(stinespring_*_g14 3·szegedy_2state_p14·naimark_ud3 = UD-POVM Naimark 완성,
        #   naimark_observe 3ak) 일괄 봉인 → 87 modules·315 apps·root 008e09334c543c7c.
        # ✅G4 폐합(2026-07-05): schur4 16×16(★schur3 sub-app 복리, CG 반각 {π/6,π/4,π/3} 전부 기봉인
        #   → module 0, G4b 스킵) — J²/Jz {6×5,2×9,0×2}+S₄ [4]/[3,1]/[2,2] witness(schur4_observe 3al)
        #   → 316 apps·root 16422fcc4319ea92.
        # ✅G5 폐합+G6 종결(2026-07-05): ★새 대수체 ℚ(ζ₅,√φ) 차수 8 승인(.pgf/approvals/G5-fibonacci.md)
        #   → z5_gate(Z^(1/5), (z5)⁵=z_gate 재발견)·ry_fib(√φ 캐리어) + fib_braid_s1/s2(첫 비-Clifford
        #   anyon braid, Yang-Baxter·B₃중심 e^{2πi/5}I·비-Clifford witness, fib_braid_observe 3am).
        #   **TrackGate6 전체 폐합**: module +4·앱 290→318·반증 1·root 7293a3de→1feeef7e7af4d23d.
    TrackR3Residue // report3 잔여 차기 후보 소화 (done — 2026-07-06 폐합) @dep:TrackHE3
        # integrated_horizontal_expansion3.md 의 ⏸️차기 4건 전부 terminal: C7·C8·C6 done ·
        #   C12 deferred(스킵 판정). ★report3 완전 소진 — 6앱 +(flag 2·hsp 2·gf 2), 전부 module 0.
        R3_C7_FlagSyndrome // ★FT 증후 추출 프리미티브 — 1-flag weight-4 stabilizer (done — 2026-07-06)
            # ✅ flag_synd_zzzz(u_hash c7218f50)·flag_synd_xxxx(48ab83c3, ==H⊗4 켤레 exact) Tier-0 봉인
            #   — 6q coherent 추출, Chao-Reichardt 1-flag 배치(데이터 CNOT 1·3 뒤), 신규 module 0.
            #   flag_syndrome_observe(3an): 증후 정확성(기저 전수)·★flag 정리 exact(Pauli 전파 9위치:
            #   무flag⇒잔여 Z-string≡w≤1 mod ZZZZ, 위험 w_eff=2 fault 는 반드시 flag)·보조 fault 무해·
            #   ★surf422 codeword 4×2 무증후 복리([[4,2,2]] stabilizer 쌍 완성)·teeth 2종(무flag hook·
            #   창 오배치 검출 — flag 층 하중 실증). 342→344앱·root 191287568abd3191.
        R3_C6_GF2k // GF(8) 역원·Frobenius — 체 연산 완결 (done — 2026-07-06)
            # ✅ gf8_inv(a↦a⁻¹=a⁶, 0↦0, u_hash ac2452e6 — ★첫 비선형 체 연산, MMD 6게이트=cmul 동일
            #   합성 인프라)·gf8_frob(a↦a², 5af848a3 — GF(2)-선형→cnot 2개) Tier-0, 신규 module 0.
            #   golden=독립 체 산술 직접. gf8_observe(3ao): a·a⁻¹=1 전수·대합·★Galois 구조(frob³=id Z₃·
            #   자기동형 64곱·고정체 GF(2)·inv 가환)·★mulx 궤도 반전 inv(xᵏ)=x^(7−k)(복리)·teeth 2종
            #   (틀린 poly x³+x²+1·게이트 순서). 346→348앱·root 7e820010c53eb952.
        R3_C8_D4HSP // D₄ HSP 1-shot coset 회로 (done — 2026-07-06)
            # ✅ d4_hsp_shot_s(비정규 {e,s}, u_hash 8934e586)·d4_hsp_shot_r2(정규 {e,r²}, 6edcaa93)
            #   Tier-0 64×64 — HSP 표준 절차 전체(균일중첩·|H⟩·오라클·비아벨 QFT)를 하나의 coherent
            #   회로로 자산화. ★d4_mult+d4_qft 이중 sub-app 복리, 신규 module 0. golden=군론 공식 직접.
            #   d4_hsp_observe 가산 확장: marginal==문자공식·★조건부 y⇒F|yH⟩(8y 전수 위상 포함)·
            #   봉인회로 구동 비정규/정규 구별(ρ ½ vs 0). 344→346앱·root 2602911c9adcf59a.
        R3_C12_LinearOptics // 선형광학 unary Clements (deferred — 스킵 판정 2026-07-06)
            # 판정 근거(정직 기록): 저합의 1/8(A7 단독) + 각도 혼재(π/3 algebraic → 승인 게이트 비용)
            #   + unary 인코딩=기존 자산과 복리 접점 약함. report4 회신이 재제안·보강하면 재평가.
    TrackC3Hierarchy // Clifford 계층구조(3단계) 자체개창 — gate teleportation exact 코어 (done — 2026-07-06)
        # ✅ t_teleport(CS·CNOT, u_hash 6d51b925)·s_teleport(CZ·CNOT, 2cab7bf3) Tier-0 봉인.
        #   hierarchy_observe(3ap): ★촉매 exact 7상태(|A⟩==magic_a 열 복리)·계층 판정 7건(독립 정의:
        #   T/CS/CCZ/U_t∈C₃∖C₂·S/U_s∈C₂)·사다리 재발견 t²==s·s²==z(봉인 golden)·teeth 3종
        #   (자원 오염·Z^{1/8}∉C₃·무보정 CNOT). 348→350앱·root ddeb6079ef8f88b3.
        # V8(2-B) 자체개창 선례. v3·v4 요청문 §4 예시였으나 외부 미제안 축. 새 수평: 계층 C₁⊂C₂⊂C₃
        #   (C_{k+1}={U: UPU†∈C_k})의 구조 자산화. 인스턴스: ★coherent gate teleportation 촉매 회로 —
        #   t_teleport=CS·CNOT: U(|ψ⟩⊗|A⟩)=(T|ψ⟩)⊗|A⟩ (magic_a 복리, |A⟩ 촉매 보존) ·
        #   s_teleport=CZ·CNOT: U(|ψ⟩⊗|Y⟩)=(S|ψ⟩)⊗|Y⟩ — ★사다리: 보정 게이트 계층 = 대상 게이트−1
        #   (S보정↔T·Z보정↔S), coherent 제어 보정 = 대상과 동일 계층. 신규 module 0(cnot·cs_gate·cz).
        #   witness: 촉매 exact·계층 판정(독립 정의: C₂=Pauli保·C₃=Clifford保 — T/CS/CCZ∈C₃∖C₂·
        #   S∈C₂∖C₁·T²=S 재발견·비-C₃ 검출 teeth). 측정 기반 프로토콜(Clifford-only 소비)=관측 경계.
    TrackHE4 // report4 소비 — 수평확장 4차 통합 6축 (done — 2026-07-06 폐합, 350→368앱) @dep:TrackC3Hierarchy
        # 설계 정본: _workspace/integrated_horizontal_expansion4.md (35제안→기소비 4 차감→13클러스터→
        #   자율 6축 P1~P6 + 예비 R1~R7 + 조건부 사람게이트 2. 기본경로 = 신규 module 0·사람게이트 0).
        P1_FibConsume // Fibonacci 소비층 — F-move+매듭 word+Jones 관측 (done — 2026-07-06)
            # ✅ fib_fmove(F=ry_fib·z, u_hash 86782086)·fib_hopf(σ₁²)·fib_trefoil(σ₁³)·fib_solomon(σ₁⁴)·
            #   fib_trefoil_m(σ₁³σ₂ — s2 경로 최초 소비) 전부 Tier-0·module 0(sub-app 복리).
            #   fib_jones_observe(3aq): ★Jones 두 독립 경로 exact(가중 trace (1,φ) vs skein 재귀;
            #   t^½=A⁻² 분지 규약)·unknot==1·T(2,n)⊔O 3건·★Markov 소멸 σ₁³σ₂==V(삼엽)·teeth 2종.
            #   350→355앱·root ddeb6079→4c28b6b8df22e95c. honest: 봉인=word 유니터리뿐·Jones 값=관측.
        P2_C3PhasePoly // C3 대각 phase-polynomial 정규형 + 계층/semi-Clifford witness (done — 2026-07-06)
            # ✅ c3_diag_ladder3(u_hash 20471a17)·c3_diag_full3(f6c81e5c) Tier-0·module 0(T/CS/CCZ 사전).
            #   hierarchy_observe 가산 확장: ★강하 두 경로(행렬 켤레 vs Δ_j f 정수 다항)·2단→Pauli·
            #   멤버십 C₃∖C₂·컴파일러 항등 40표본·semi-Clifford U_t==CS·CNOT(탐색 0)·teeth CT교란.
            #   355→357앱·root 4c28b6b8→4f2a333fa5bbd165. honest: 봉인=인스턴스 2뿐·일반론=관측.
        P3_GF8Field // gf8_mul + RS 신드롬 코어 + rs73 structural capstone (done — 2026-07-06)
            # ✅ gf8_mul(Toffoli 12, u_hash 6595a35e)·rs_synd_core(CNOT 9, 57dc5730)·rs73_encoder
            #   (CNOT 60, 21q Tier-1, af6f688d + ★동일 커밋 subspace 상환 — 첫 비-Shor). 회전 0.
            #   gf8_observe 가산: mul 전수512·inv 교차(mul(frob²,frob))·rs73 두경로 전수512·
            #   신드롬제로 2048·★거리5 MDS 전수511·teeth. semantic method_desc 가산 1건.
            #   357→360앱·root 4f2a333f→6f262232dac41e79.
        P4_SchurSampling // 반사자 R + 디코더 + Dicke k=2 (done — 2026-07-06)
            # ✅ schur3_dag/schur4_dag(역word 디코더=sampling 방향)·dicke4_k2(=[x,x,schur4] —
            #   ry_sqrt23 게이트 회피)·schur_reflect4(R=2P−I, D=ANF 10항 — P2 사전 교차복리,
            #   golden=조합 독립). spectrum 두 경로 exact. label register 는 반사자+디코더가 흡수
            #   (섹터 판독 물리 동일 — 별도 순열 앱 불요 판정).
        P5_MubShadow // MUB 측정 word 4 + frame channel 대수 관측 (done — 2026-07-06)
            # ✅ mub4_meas_b2~b5(V_b†, sdg 소비). 측정측↔기봉인 준비 20앱 역회전 16/16 ·
            #   frame channel (ρ+I)/5·역재구성·Bell Pauli 회복 유리 exact. 360→368앱·root 32a44bfe.
        P6_StabRank // stabilizer-rank 제5 검증경로 인프라 (done — 2026-07-06, ★TrackHE4 폐합)
            # ✅ scripts/stabrank_verify.py: Clifford-합 분기(T/CS/CT 2·CCZ/CCCZ 4) + 아핀/ℤ₄
            #   이차형식 엔진(행렬곱 0). 봉인 앱 128건 재검증·자가시험 24·teeth·skip 314 사유기록.
            #   새 봉인 0·root 32a44bfe 불변·오라클 무접촉. reproduce 3ar=--sample(1s) 계층화.
            # ★TrackHE4 총결: 봉인 +18·인프라 1·첫 비-Shor subspace 상환·사람게이트 0·module 0.
    TrackHE4R2 // [[8,3,2]] triorthogonal + transversal CCZ — TrackHE4 예비 R2 실행 (done — 2026-07-06)
        # ✅ code832_encoder(216565fa)·code832_tccz(101be8d1) Tier-0·module 0. code832_observe(3as):
        #   triorth 정수 (0,0,1)·논리 CCZ 8/8+행렬 exact·거리-2 전수·teeth 2(전부-T→x=100 검출).
        #   ★첫 비-Clifford 횡단 논리 게이트(W7.3 Clifford 횡단 너머). 제5경로 130/130 자동 편입.
        #   368→370앱·root 32a44bfe→9b5964fad827f165. 잔여 예비 R1/R3~R7 = HE4 설계서 §4 보존.
    RequestV5 // 수평확장 5차 요청문 배치 (done — 2026-07-07) @dep:TrackHE4R2
        # ✅ .pgf/external/HORIZONTAL-EXPANSION-REQUEST-v5.md — §3e(v4 소비분 6축+R2 EXCLUDE)·
        #   §3f(예비 보강조건)·§4′(e) 패턴 4(기소비 선점 대조·교차 복리·게이트 구조 회피·인프라 소비)·
        #   검증경로 5개 공시. 회신 정본 규약 = _workspace/HORIZONTAL-EXPANSION-report5.md → TrackHE5.
        #   외부 전달·수집 = 정욱님 액션. 대기 중 자율 대안 = frontier(N=143+)·예비 재정식화.
    TrackHE5 // report5 소비 — 수평확장 5차 통합 5축 (done — 2026-07-07 폐합, 373→380앱·모듈 90) @dep:RequestV5
        # 설계 정본: _workspace/integrated_horizontal_expansion5.md (35제안→기소비 차감 0→12클러스터→
        #   자율 5축 P1~P5 + 예비 S1~S7. 실측 정정 2: A8 cr6≠ζ₃·A5 Burau 비유니터리).
        P1_ExactDynamics // dual-unitary + Floquet — 새 동역학 클래스 (done — 2026-07-07)
            # ✅ du_gate_j8(78626df3, V=iSWAP†·e^{−iπ/8 ZZ})·du_brick6_t2(a0b1603a, sub-app ×6)·
            #   floquet4_uf(93c0ffec, CZ링+T킥). dyn_observe(3at): ★쌍대성 exact·★광원뿔 두 경로
            #   (오프레이 전소멸+광선 X½/Y½/Z1==M₊² 닫힌형)·quasi-energy 기록·teeth 3.
            #   370→373앱·root 9b5964fa→860fdf32460c0110. §3b 관문 개창.
        P2_MagicResource // extent/robustness exact 증명서 + T-count 하한 (done — 2026-07-07)
            # ✅ magic_cs(f9a74799) 봉인 1 + magic_resource_observe(3au): ξ(T)=4−2√2·ξ(T⊗2)=24−16√2
            #   완전 증명서(ℚ(√2) Fraction 정확산술 격차0)·ξ(CS) bounded [8/5,(11+2√10)/9]·R(T)=√2·
            #   T-count 인증 magic_a≥1/magic_cs≥3 타이트·★A6-1 반증(F 불변량: T⊗T↛CS).
            #   373→374앱·root 860fdf32→6871f793fa2d5f0b.
        P3_MatchgatePfaffian // 제6 독립 검증경로 (done — 2026-07-07)
            # ✅ matchgate_verify.py: plan→R∈SO(2n) 독립 컴파일 vs golden 켤레 두 경로·진공 행렬식.
            #   커버 6/6(gauss_hop4·gauss_braid3 신규 봉인 2 + cliff1_s* + code832_tccz 3중커버)·
            #   census 골든/as-written 정직 구분·teeth 3·reproduce 3av. 검증경로 5→6.
            #   374→376앱·root 6871f793→b8ba9989672232fc. ★합성=오른쪽 곱 함정 교정.
        P4_RM15 // RM [[15,1,3]] transversal T (done — 2026-07-07)
            # ✅ rm15_encoder_t2(모듈 90, 7번째 Tier-2, 0052db4c — ★완전 논리-입력 인코더, W7.2
            #   future work 상환)·rm15_tt(T^⊗15 Tier-1, 8cedd324). rm15_observe(3aw, dense-free):
            #   심볼릭 역전파 14안정자·T^15==논리T†(mod-8 정수)·거리=3 전수·teeth 3.
            #   376→377앱·89→90모듈·root b8ba9989→ba32a65cc8bbce81.
        P5_KnotDeepening // 3-strand word family + 다중 불변량 (done — 2026-07-07, ★TrackHE5 폐합)
            # ✅ fib_yb·fib_word5·fib_fig8(첫 비-토러스, σ⁻¹=z5³). fib_jones_observe 가산: TL₃ 상태합
            #   제3경로·연결합 곱법·amphichiral 1−√5·Alexander 정수(Burau)·★반꼬임≅F 재발견.
            #   377→380앱·root ba32a65c→12244b5cc2136f41.
            # ★TrackHE5 총결: 봉인 +13·모듈 90(Tier-2 7)·검증경로 6·자원 증명서·A6-1 반증.
    RequestV6 // 수평확장 6차 요청문 배치 (done — 2026-07-07) @dep:TrackHE5
    TrackHE6 // report6 소비 — 수평확장 6차 통합 6축 (done — 2026-07-07 폐합, 380→386앱·모듈 91·검증경로 7) @dep:RequestV6
        # 설계 정본: _workspace/integrated_horizontal_expansion6.md (33제안→차감0→13클러스터→6축).
        P4_S4Fourier // S₄ 정수표현 비아벨 — 곱셈 오라클 + ζ₃ 반증 (done — 2026-07-07)
            # ✅ s4_mult(b2c8f624, V₄⋊S₃ 곱셈 10q, ★s3_mult sub-app 복리). s4_observe(3ax): 군법칙≅S₄·
            #   ★(3,1) 정팔면체 signed-perm 정수표현 회수·★(2,2) ζ₃ closed-negative(A8 통찰 절반 반증 —
            #   완전 Fourier ζ₃ 필연, rational group ≠ 정수-유니터리). 380→381앱·root c252010e91071e2b.
        P2_Bogoliubov // Kitaev pairing free-fermion — 제6경로 비수보존 확장 (done — 2026-07-07)
            # ✅ bogoliubov_pair(c98a3788, B=exp(iπ/4·XX) 수보존 깸)·kitaev4_gs(860607b8, sweet dimer).
            #   bogoliubov_observe(3ay): R∈SO(4)·Kitaev sweet 바닥·fermion parity·★Pfaffian Z₂ 다중경로.
            #   matchgate_verify census 에 pairing 편입. 381→383앱·root c252010e→62aac895ae906cc3.
        P3_OTOC // OTOC/scrambling + Floquet winding (done — 2026-07-07)
            # ✅ du_gate_dag(35733059, V†)·otoc_du_t1(befbb074, OTOC 연산자 Tr/2⁶=0). dyn_observe(3at)
            #   가산: 봉인 Tr==직접 OTOC·operator growth 광원뿔·Z-basis trivial·Floquet winding Σε/2π=6
            #   정수. du_gate 소비 sub-app 복리. 383→385앱·root 62aac895→c86ced4ea43d3443.
        P6_ChannelMagic // 채널 magic 자원 증명서 (done — 2026-07-07)
            # ✅ chan_magic_t(f977e8bf, T-채널 Choi |J_T⟩). magic_resource_observe(3au) 가산:
            #   ★채널 extent ξ(Φ_T)=4−2√2=게이트 magic(Choi 동형)·catalysis(t_teleport 자원보존).
            #   385→386앱·root c86ced4e→034c36e0175e8146.
        P1_Distill15 // Coherent 15-to-1 증류 프로토콜 (done — 2026-07-07)
            # ✅ rm15_decoder_t2(모듈 91, 8번째 Tier-2 — 인코더 역 = 측정 전 syndrome 추출 코어).
            #   rm15_observe(3aw) 가산: 디코더==인코더†·부호어→syndrome0(accept)·weight-1→syndrome≠0.
            #   봉인=디코더 tableau뿐·증류 성공률=관측. 모듈 90→91·root 034c36e0→60a6de09b237c8b1.
        P5_TNPath // 텐서망 제7 검증경로 (done — 2026-07-07, ★TrackHE6 폐합)
            # ✅ tncontract_verify.py: 게이트 텐서 인덱스 수축(dense 미실체화, 열 벡터). 봉인 360앱
            #   재검증(up-to-phase)·reproduce 3az. 새 봉인 0·root 불변. 검증경로 6→7.
        # ✅ .pgf/external/HORIZONTAL-EXPANSION-REQUEST-v6.md — §3g(v5 5축 EXCLUDE)·§3h(예비 조건)·
        #   §4′(f) 패턴 4·검증경로 6 공시·★공개 저장소 URL(실측 novelty). 회신 규약 = report6 →
        #   TrackHE6. 전달·수집 = 정욱님 액션. 대안 = frontier(N=143+)·예비 S1.
    RequestV7 // 수평확장 7차 요청문 배치 (done — 2026-07-07) @dep:TrackHE6
        # ✅ .pgf/external/HORIZONTAL-EXPANSION-REQUEST-v7.md — §3i(v6 6축)·§3j(예비)·§4′(g) 패턴 4·
        #   검증경로 7·저장소 URL. 회신 규약 report7 → TrackHE7. 대안 = frontier(N=143+)·예비 T2.

    TrackQFStdlib // QF-STDLIB 사용자 진입 계층 설계·구현 (done) @dep:TrackV08_ProofCarrying
        QFStdlib_DetailedDesign // Canon·Import·Proof-Carrying Template 상세 설계 저장 (done)
            # input: _workspace/upgrade-design/qf-stdlib-proposal.md, registry/REGISTRY-MANIFEST.json, SEMANTIC-GUARANTEES.json
            # process: PGF DESIGN + 상세 실행 설계. 신규 봉인 0, oracle/root 불변, sidecar/lookup/template only.
            # output: .pgf/DESIGN-QFStdlib.md + _workspace/upgrade-design/qf-stdlib-detailed-design.md
            # criteria: Canon/Import/Template 노드가 구현 가능한 원자 작업으로 분해되고, 정직 경계/검증 게이트가 명시됨. ✅ done
        QFStdlib_ImplementationV0 // Canon sidecar + lookup/attest package + template v0 (done) @dep:QFStdlib_DetailedDesign
            # output: registry/CANON.json, qf_stdlib/, scripts/qf_stdlib.py, tests/test_qf_stdlib.py, docs/QF-STDLIB.md
            # criteria: validate-canon·lookup·attest·template·unittest·second_oracle·contested_guard·reproduce --changed-only PASS. ✅ done
        QFStdlib_V01Hardening // root drift guard + Canon palette expansion (done) @dep:QFStdlib_ImplementationV0
            # output: check-root CLI/API, 42 canonical entries, expanded unit tests, concrete docs examples
            # criteria: check-root·validate-canon·lookup·attest·template·unittest·py_compile·reproduce --changed-only PASS. ✅ done
        QFStdlib_V02CirqAdapter // convention-pinned Cirq exact circuit hash adapter (done) @dep:QFStdlib_V01Hardening
            # output: canonical_hash_with_adapter(..., "cirq", qubit_order=...), adapter-info CLI, docs/tests
            # criteria: qft/3 Cirq hash==Canon; explicit qubit_order required; endian/global-phase/CLI-fail-closed tests PASS. ✅ done
    TrackEXT // 외부작업 — 리스트만, 착수 금지 (blocked)
        # 전부 self-contained 부분 완성·정욱님 수거 또는 하드웨어 확보 대기. 본 세션에서 착수하지 않는다.
        W2_4_Relay // c7x/cr8 6런타임 패널 수거 (blocked) #EXT
        W3_5_CIpilot // 외부 CI seal-gate 파일럿 (blocked) #EXT
        W4_2_PoisonPanel // 약모델 poisoned-lineage 패널 (blocked) #EXT
        W5_3_RuntimeKeys // ed25519 runtime 실키 (blocked) #EXT
        SD_BackendEvidence // QASM3→Aer/real QPU evidence sidecar (blocked) #EXT @defer:하드웨어
        ServerLink // "서버 연계 작업" — 외부, 의미 정욱님 확정 대기 (blocked) #EXT #ASSUMPTION
            # ⚠ 가정 노드: 범위 미정의(오라클 서버화/백엔드서버/relay서버/외부시스템 중 미확정).
            #   확정 전 착수·세부설계 금지. 리스트 placeholder 로만 보존.
```

---

## 정직성·연동 (PPR 주석)

```python
# 봉인 경계: TrackSC 각 작업은 회로 *구조*만 Tier-0 봉인(composite==golden, MatrixGate 0).
#   변분 에너지/근사비/gradient 는 backend_adapter 관찰(seal 아님) — 기존 정직 경계 상속.
# 비파괴: frozen 23키·fingerprint 2파일 byte-identical 불변. 신규 봉인은 root 성장만(순수 가산).
# 연동(2026-07-01 단일화: task_record/remain_task_list/task_plan_pg 폐기, HANDOFF.md 단일 정본):
#   - 매 작업 완료 → HANDOFF.md(현재상태·backlog·완료요약 단일 정본) 갱신 + 자동생성물 재생성.
#   - 외부 공개 2종(README/Technical-Spec)은 자율 동기화(현재상태 수치, 이력 보존). reading order=AGENTS.md.
#   - 이 마스터의 status 는 본 파일 Gantree 에서 직접 갱신(designing→in-progress→done).
# 종결 규율: SC_Closure 도달 = self-contained 의도적 종료. 그 이후 즉흥 신규 클래스 제시 금지.
```

## 가정 (명시 — 검증 시점 포착용)

- **A1**: "현재 나와있는 self-contained 작업" = 직전 제시 후보(W10.2 VQEDeepening·W11.1 QAOA·W10.3 ParamShift)로 한정. 그 외 수평 클래스(error-mitigation 등)는 *의도적으로 미포함*(무한확장 차단). → 정욱님 가감 가능.
- **A2**: "서버 연계 작업"은 외부작업군(TrackEXT/ServerLink)으로 분류, 의미 확정 전 리스트 placeholder. → 정욱님 정의 대기.
- **A3**: W10.3 은 경량·옵션 — 봉인 성장이 작아 SC 종결을 늦추지 않으려 마지막 배치. 생략 가능.
