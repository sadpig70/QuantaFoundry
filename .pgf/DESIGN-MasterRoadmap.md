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
