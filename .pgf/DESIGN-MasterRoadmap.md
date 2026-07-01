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
