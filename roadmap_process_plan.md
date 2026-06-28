# QuantaFoundry — 단계별 작업 실행계획 (Process Plan)

> 작성 2026-06-28 · 기반 = `integrated_roadmap.md`(8-agent 통합 5트랙 A/B/C/D/E) · 방법 = PGF WORKPLAN.
> 용도: 이 plan의 Stage·Work 단위로 **단계별 실제 작업을 진행**한다. 진행 체크박스는 HANDOFF.md(간략) ↔ 본 파일(상세) 양쪽.
> 태그: **[SC]** self-contained(혼자 완결) · **[EXT]** 외부 런타임 relay 의존(정욱님 수거) · **[ND]** 비파괴(registry/sealed/frozen 무변경).
> 공통 verify(모든 Work): `reproduce_all` root `3dae613d` 불변 · `second_oracle` · `verify_contested_guard`(frozen 23키) · fingerprint 2파일 무수정.

---

## 실행 순서 원칙

1. **[SC] 우선** — 외부 relay 없이 완결되는 것부터(즉시 진행 가능).
2. **저비용 고레버리지 → 최약가정 직격 → open-ended → 정직종결** (roadmap §4).
3. **비파괴 가산** — 신규 보증등급·레이어는 기존 봉인에 가산만. 헤드라인 수치는 질적 정직화(분리표기).
4. 각 Stage 완료 시 회귀 전수 그린 확인 후 다음 Stage.

---

## Stage 0 — 즉시·저비용 정직화 (Track C·E 일부) `[SC][ND]`

```
Stage0 // 저비용 고레버리지 (designing)
    W0.1_SecondOracleFullCoverage // 18/48 → 48/48 독립검증 (designing)
    W0.2_TierHeadlineSplit // 수치 (Tier-0/1/sampled) 분리표기 (designing)
```

- [x] **W0.1 SecondOracleFullCoverage** `[SC][ND]` ✅ 2026-06-28
  - 목표: oracle 단일실패점(second_oracle 18/48 모듈만 독립 numpy) → 48/48.
  - 산출: `scripts/second_oracle.py` 확장(ry_k/qft_n 헬퍼 + 30 신규 제1원리 구성기) · `SECOND-ORACLE-RESULT.json`.
  - 결과: **48/48 u_hash 일치**, 기존 18 byte 불변, reproduce_all root 3dae613d 불변, sealed 무변경.
- [x] **W0.2 TierHeadlineSplit** `[SC][ND]` ✅ 2026-06-28
  - 산출: `semantic_guarantee.py` `headline_split` 집계 + README/HANDOFF/기술서 분리표기.
  - 결과: 모듈 48=전부 unitary_equiv(Tier-0) · 앱 59=58 unitary_equiv + 1 structural(ghz16, 부분검증). 분류합==총계, 비파괴.

---

## Stage 1 — Trust-Closure: Tier-1 보증 상승 (Track B1) `[SC]` #최약가정직격

```
Stage1 // 복리테제 최약가정(Tier-1≠unitary_equiv) 직격 (designing)
    W1.1_SampledDenseVerify // unitary_equiv_sampled 신규등급 (designing)
    W1.2_ZXRouting // Clifford+T 대형 Tier-3 라우팅 (designing) @dep:none
    W1.3_GlobalPhaseTracker // 전역위상 명시기록+합성검사 (designing)
```

- [x] **W1.1 SampledDenseVerify** `[SC][ND]` ✅ 2026-06-28
  - 산출: `scripts/sampled_dense_verify.py`(path A=second_oracle.INDEP 제1원리 일반게이트 statevector tensordot, path B=canonical 의도 plan-무관) · `registry/SAMPLED-DENSE-REPORT.json` · `semantic_guarantee.py` 등급 격상 연동.
  - 결과: **ghz16 anchor·basis 48/48·random 16/16·negative ✅ → `unitary_equiv_sampled` 격상**. seed 20260628 봉인 → **2회 byte-identical**. **라이브러리 structural-only 0개 달성**(최약가정 직격). sealed/root 3dae613d 불변.
- [x] **W1.2 ZXRouting** `[SC][ND]` ✅ 2026-06-28
  - 산출: `scripts/zx_routing.py`(pyzx 0.10.3) · `.pgf/zx/ZX-ROUTING-REPORT.json`.
  - 결과: **non-Clifford 대형 Tier-1 대상 0**(정직 음성 — 유일 Tier-1 ghz16=Clifford→P0 tableau+W1.1 sampled). ZX-equivalence 인프라 **self-test 6/6**(sound: T·T==S·T⁴==Z·H²==I·CNOT²==I; teeth: T≠S·H≠S). 대형 non-Clifford 봉인 시 Tier-3 활성. 비파괴.
- [x] **W1.3 GlobalPhaseTracker** `[SC][ND]` (A2 고유통찰) ✅ 2026-06-28
  - 산출: `scripts/global_phase_tracker.py` · `registry/GLOBAL-PHASE.json`(비파괴; sealed 메타는 fingerprint 결합이라 불가→가산 레이어).
  - 결과: **controlled-pair 정합 4/4 ALL EXACT**(cnot/cz/cs/ct == base의 정확한 controlled, 전역위상까지)·base 전역위상 canonical(0) → **controlled 합성 안전 실증**. wrapping 위험 0. 미래 goal-autonomy/discover 가드 명시.

---

## Stage 2 — QF-Discover: open-ended 발견 엔진 (Track A) 일부 `[EXT]`

```
Stage2 // known-family 너머 발견 (designing)
    W2.1_ValueFunction // dep-graph fan-in 기반 점수화 (designing)
    W2.2_ExploitAxis // 분해 최적화기(오라클=reward) (designing) @dep:W2.1
    W2.3_GoalSelectionGuard // 목표선택 co-error 방어 (designing) @dep:W2.1
    W2.4_PrimitiveProposalRound // capability-gap→panel→seal (designing) @dep:W2.1
```

- [x] **W2.1 ValueFunction** `[SC][ND]` ✅ 2026-06-28
  - 목표: `value=0.25·Novelty+0.20·Sealability+0.20·Composability+0.15·ResourceΔ+0.10·ConsensusEst−0.20·Ambiguity−0.15·Cost`. Composability=dep-graph fan-in(c6x 패턴). Novelty 객관근거 강제.
  - 산출: `scripts/discover.py`(rank/validate/guard/propose) · `.pgf/discover/CANDIDATE-RANK.json` · `RETRO-VALIDATE.json` · `.pgf/DESIGN-QFDiscover.md`(PG 설계).
  - 결과: 8항 가중합(각 항 registry 그래프구조 유도, 근거 동봉). **RetroValidate ALL PASS**: c6x fan-in=2(cmul2_mod33/35) *사전*포착 · counterfactual 미봉인 시 정확히 BLOCKED 재구성 · specialized 게이트(c3x~c6x) 전부 median 위 · novelty 발견판별(distinct-prime 0.8 > genskill family 0.2). 분석전용 비파괴.
- [x] **W2.2 ExploitAxis (분해 최적화기)** `[SC][ND]` ✅ 2026-06-28
  - 목표: 타깃 유니터리 고정, 분해만 탐색 → 오라클=하드보상(봉인=1, resource=연속). reward-hacking 구조차단(봉인 못하면 0).
  - 산출: `scripts/decomp_optimizer.py`(probe/reward) · `.pgf/discover/EXPLOIT-AXIS-PROBE.json` · `EXPLOIT-AXIS-REWARD.json`.
  - 결과: **CheaperDecompProbe 6/6 그룹 자원감소 실존**(동일 u_hash, qft4 save=32.2·ccz=10.0·qft2/3·cz·swap2 — 직접 모듈이 _rediscovered/_pipeline 보다 쌈). **HardReward teeth PASS**: cz_rediscovered reward=1.77(정답) · bell/swap_via_cnot reward=0(봉인돼도 u_hash≠target → 유니터리 변조 가짜보상 **구조적 불가**). 임시 store 재봉인(registry 불변).
- [x] **W2.3 GoalSelectionGuard** `[SC][ND]` (A3 고유통찰) ✅ 2026-06-28
  - 목표: *무엇을 만들지* 선택의 co-error 방어(미명명 실패모드 명명). coverage/independence 게이트.
  - 산출: `scripts/discover.py guard` · `.pgf/discover/SELECTION-LOG.json`.
  - 결과: coverage gate 작동(app 24선택/35거부 — 동일 family-capability 중복 거부) · independence gate(단일 convention 의존 경고, consensus_est<0.6). 모든 결정 사유 로그.
- [x] **W2.4 PrimitiveProposalRound** `[EXT]` ✅ 2026-06-28 (relay 1라운드 수거·채점·봉인 완료)
  - 목표: capability-gap → 6런타임 패널 decomposition 제안 → 수렴+sympy proof → key-free 봉인.
  - 산출: `scripts/discover.py propose` → `_workspace/crossmodel/discover_round1/`(GAP-SPEC.json·TASKSPEC.md·SCORING.md·README.md·responses/·**SEAL-RESULT.json**).
  - 결과: ValueFunction+family 확장규칙이 **미봉인 capability-gap 자율도출**: `c7x`(7-control, predecessor c6x fan-in=2 → distinct-prime mod39/51 unlock) · `cr8_dag_gate`(qft8+ unlock). PG TaskSpec+채점/봉인 스키마 완성.
  - **relay 수거/채점**: 6런타임(codex·deepseek·gemini-3.5-flash·grok·kimi·qwen) 패널 응답 → **수렴 확인**. `c7x` golden=`cnx_perm(7)` 256×256 permutation(≥4/6 일치), bloq=`MultiControlX(cvs=(1,)*7)`. `cr8_dag_gate` golden=`diag(1,1,1,e^{-2πi/2⁸})` **6/6 만장일치**, bloq=`ZPowGate(exponent=-1/2⁷).controlled()` 5/6 analytic. kimi의 정직한 음성(P(π/128)=256차 root → Clifford+T 정확분해 불가)이 c3~c7과 동형인 **analytic golden 직접봉인**이 정답임을 입증.
  - **봉인**: 두 모듈 verify_seal(C1–C4) 통과 → registry **48→50 modules**, root `3dae613d…→437efbc3…` (byte-identity 재현). second_oracle **50/50** 독립검증(c7x=`cnx_perm(7)`·cr8=`cphase(8).conj()`) · contested_guard frozen **23키 불변** · fingerprint 2파일 무수정. c7x가 distinct-prime modular-mult(mod39=3×13, mod51=3×17) 확장 prereq 잠금해제.

---

## Stage 3 — Adoption: 신뢰자본 외부 소비화 (Track C) `[SC]` 우선

```
Stage3 // QPGF↔Foundry 분리 · CI 소비 (designing)
    W3.1_QasmExport // sealed → OpenQASM3 (designing)
    W3.2_QasmIngestion // OpenQASM3/Qiskit → spec (designing)
    W3.3_CLI // qf verify/seal/compose/reproduce/explain/export (designing)
    W3.4_CitableRegistry // Zenodo DOI + CITATION.cff (designing)
    W3.5_SealGateCI // GitHub Action seal-badge (designing) @dep:W3.1,W3.2 [EXT]
```

- [x] **W3.1 QasmExport** `[SC][ND]` ✅ 2026-06-28
  - 산출: `scripts/qasm_export.py`(PlanFlatten 재귀펼침+서브앱 큐빗 remap → QasmEmit → RoundTrip) · `.pgf/adoption/qasm/*.qasm` · `QASM-EXPORT-REPORT.json` · `.pgf/DESIGN-Adoption.md`(PG 설계).
  - 결과: **round-trip 57/57 일치**(n≤10 dense, second_oracle INDEP+embed 제1원리 재구성 u_hash==sealed → export 가 봉인 유니터리 정직표현 입증, hollow 아님). n>12 2개(ghz16/shor21) 정직 skip. 미매핑 c3x~c6x 는 opaque custom gate 노출(은폐 금지). 2회 byte-identical.
- [x] **W3.2 QasmIngestion** `[SC]` ✅ 2026-06-28
  - 산출: `scripts/qasm_ingest.py`(QASM3 서브셋 파서 + cp/ry 봉인값 역매핑 → ops_to_app_pg(tier=exact) → app_assemble).
  - 결과: **export→ingest 폐루프 8/8 일치**(재봉인 u_hash==원본 → QASM↔spec 왕복 유니터리 보존, 진입장벽 해소). 임시 store 봉인(registry 불변, MatrixGate 없음).
- [x] **W3.3 CLI** `[SC]` ✅ 2026-06-28
  - 산출: `scripts/qf_cli.py`(verify/compose/reproduce/export/ingest/discover/explain).
  - 결과: 기존 스크립트 위임(신규 검증로직 0). `reproduce --expect-root` root 대조 · `explain` 의존/blast-radius/자원 조회(c6x dependents=2 ← W2.1 fan-in 일치).
- [x] **W3.4 CitableRegistry** `[SC]` ✅ 2026-06-28
  - 산출: `scripts/citation_gen.py` → `CITATION.cff`(유효 YAML 1.2.0) · `.pgf/adoption/RELEASE-META.json`.
  - 결과: registry_root_hash 를 인용가능 단일지문으로(identifiers registry-root-sha256). "QuantaFoundry v0.7.0, QPGF-sealed root 3dae613d". Zenodo DOI placeholder(릴리스 시 발급).
- [~] **W3.5 SealGateCI** `[EXT]` (self-contained 부분 ✅ 2026-06-28, 외부 파일럿 relay 대기)
  - 산출: `scripts/seal_gate_ci.py`(게이트+seal-badge) · `.github/workflows/seal-gate.yml` · `requirements-ci.txt`.
  - 결과: CI gate=로컬 재현(root byte-identity) 성공해야 제출. seal-badge(shields.io endpoint, tier0=144·tier1=1·ΣT=21827·ΣToffoli=312). workflow=second_oracle+reproduce(root대조)+contested_guard+export round-trip. **EXT 의존**: friendly 외부 라이브러리 파일럿 협업 relay.

---

## Stage 4 — Consensus 정직종결: ρ 실데이터 (Track B2) `[EXT]`

```
Stage4 // ρ-discount 실가동 또는 "미가동" 최종확정 (designing)
    W4.1_ConventionIndependenceAudit // second_oracle 독립유도 검증 (designing) [SC]
    W4.2_PoisonedLineagePanel // 상관오류 강제유발 (designing) [EXT]
```

- [x] **W4.1 ConventionIndependenceAudit** `[SC][ND]` (A3 고유통찰) ✅ 2026-06-28
  - 산출: `scripts/convention_audit.py` · `.pgf/consensus/CONVENTION-AUDIT.json` · `docs/CONVENTION-AUDIT.md` · `.pgf/DESIGN-ConsensusClose.md`(PG 설계).
  - 결과: **판정 매트릭스** — 유니터리 *구성*=INDEPENDENT(numpy 제1원리 → risk(d) 구성버그 차단), endian/전역위상/atol/canonical-hash=**SHARED ASSUMPTION**(공유가정). 근거: endian-sensitive 10/24·big-endian 전부 sealed 일치(sealed 가 big-endian 의존)·전역위상 48/48 불변·atol(QUANT 1e-9) 48/48 불변·vs↔my_canonical_hash 판정일치 388/388. **갭 명시**: convention 단일문화는 미차단 단일실패점(little-endian 재유도/형식증명 필요) — 과장 제거.
- [~] **W4.2 PoisonedLineagePanel** `[EXT]` (self-contained 메커니즘검증 ✅ 2026-06-28, 자연발생 co-error relay 대기)
  - 산출: `scripts/rho_validation.py` · `.pgf/consensus/RHO-VALIDATION.json` · `docs/TRUST-MODEL-VALIDATION-REPORT.md` · `_workspace/crossmodel/p3d_round5_poison/`(PANEL-SPEC).
  - 결과: co-error 결정론 *구성*(little-endian QFT·conjugate·phase-perturbed, 정답≠ 3종). **MECHANISM LIVE** — lineage_merge(같은 unit→DIVERGENT)·rho_discount(distinct-unit+ρ=0.6→N_eff=1.25<2→CORPUS_CORRELATED)·rho0 대조(ρ=0이면 co-error ESTABLISHED=존재가치 실증)·control(정답 2독립→ESTABLISHED, false-positive 0). frozen consensus_keys 불변(인메모리). **정직 라벨**: ρ-discount=설계+메커니즘 실가동(구성 co-error 붕괴 입증). 자연발생 co-error 통계는 **EXT** 약모델 패널 relay.

---

## Stage 5 — Hardening 잔여 (Track E) `[SC]`

```
Stage5 // blind-spot 비파괴 방어 (designing)
    W5.1_DeterminismEnvPin // BLAS/FP/platform lockfile+container (designing)
    W5.2_OracleRevocationProtocol // rollback+revocation_list 운영 (designing)
    W5.3_RuntimeIdentityProof // Sybil 암호증명 (designing) [EXT]
```

- [x] **W5.0 GuardKeyCountFix** `[SC]` ✅ 2026-06-28
  - 산출: `scripts/verify_contested_guard.py` 출력문 명확화(비-fingerprint, 검증로직 불변) · `.pgf/DESIGN-Hardening.md`(PG 설계).
  - 결과: "frozen 15키"→"frozen 전체 23키·본 검증대상 15키(base 8+cross-model 7)" 명확화. 모호표현(15가 전체로 오해) 제거. pass=20 불변.
- [x] **W5.1 DeterminismEnvPin** `[SC]` ✅ 2026-06-28
  - 산출: `scripts/determinism_env_check.py` · `requirements.lock`(178패키지) · `.pgf/hardening/ENV-FINGERPRINT.json`.
  - 결과: 환경지문(numpy 2.4.6·py 3.13.14·scipy-openblas·Win10) 캡처. **byte-identity ROBUST** — hash_unitary 격자양자화(QUANT 1e-9+PREQUANT 1e-12)가 FP잡음(1e-13) 7/7 흡수·결합순서 (A·B)·C==A·(B·C)(Δ=1.4e-14 흡수)·BLAS 합산순서 무관. lockfile로 재검증 신뢰조건 명시.
- [x] **W5.2 OracleRevocationProtocol** `[SC]` ✅ 2026-06-28
  - 산출: `scripts/oracle_rollback_protocol.py` · `docs/EMERGENCY-RESEAL.md` · `.pgf/hardening/ORACLE-REVOCATION.json`.
  - 결과: **fingerprint 무결성 145/145 sealed 일치**(현 verify_seal/contracts sha256==전 봉인 기록값, ALL INTACT) → revocation_list 빈배열 정당. fingerprint 변경 시 rollback(버그)/전수 재봉인(업그레이드) 절차 문서화. **2파일 읽기만**(무수정).
- [~] **W5.3 RuntimeIdentityProof** `[EXT]` (self-contained 메커니즘 ✅ 2026-06-28, 실키 수급 relay)
  - 산출: `scripts/runtime_identity.py`(ed25519) · `.pgf/hardening/RUNTIME-IDENTITY.json` · `_workspace/crossmodel/identity_round/`.
  - 결과: signed bundle{weights_id,pubkey,u_hash,nonce,sig}. **Sybil 방어 LIVE** — 서명무결성(위변조 거부)·Sybil 붕괴(같은 pubkey 다중 weights 가장→pubkey-unit 병합 1<2→DIVERGENT)·진짜 2런타임(다른 pubkey→ESTABLISHED, FN=0). independence_unit을 pubkey로 강화. 실 런타임 공개키/서명 수급은 **EXT** relay.

---

## Stage 6 — c7x Realization: distinct-prime 산술 frontier + 발견 자동전진 (Track A 연장) `[SC]`

```
Stage6 // W2.4 봉인 primitive(c7x·cr8)의 직접 결실 실현 (done)
    W6.1_ArithFamilyExtendC7x // c7x 활용 N>64 distinct-prime cmul 봉인 (done)
    W6.2_DiscoverSelfAdvance // 발견 frontier 봉인 gate 자동전진 + unlock 정정 (done)
    W6.3_QFTPipelineExtendCr8 // cr8 활용 8큐비트 역-QFT(iqft8) 봉인 (done)
    W6.4_ForwardQFTPipelineComplete // cr6/7/8_gate 봉인 → 정-QFT pipeline n=8 완결 (done)
    W6.5_ShorCapstone // 부품 조립 → genuine distinct-prime Shor-91(7×13) Tier-1 STRUCTURAL (done)

Stage7 // 새 알고리즘 클래스 — 수직스택 이후 수평 확장 (in-progress)
    W7.1_QECStabilizerFamily // QEC stabilizer 인코더(Clifford Tier-0): repcode3·syndrome3·shor9_encoder[[9,1,3]] (done)
```

- [x] **W6.1 ArithFamilyExtend-c7x** `[SC][ND]` ✅ 2026-06-28
  - 목표: 봉인된 c7x(7-control)를 *실제로 요구하는* distinct-prime modular multiplier(N>64) 봉인 → genuine-Shor 산술 frontier 전진.
  - ⚠ **가정 검증(정정)**: discover propose의 "c7x→mod39/51" 주장을 실측 반증 — nq-qubit MCT의 maxc=nq-1=work bits. c7x는 work bits≥7 ⟺ **N>64**일 때만 필요. mod39/51/55/57(N<64)은 maxc=6=c6x로 충분(c7x 무관).
  - 산출: `scripts/arith_family_c7x.py`(arith_family 함수 재사용)·`.pgf/DESIGN-C7xPayoff.md`(PG 설계)·`.pgf/arith/ARITH-FAMILY-C7X-REPORT.json`.
  - 엔진 진화: `genskills._MCT_MODULE[7]="c7x"`·cap `maxc>6`→`>7`(c8x 부재)·`arith_family._MCT_SET`+c7x → method self-seal 재스탬프(catalog_root 0367ed64→01c5b88e, verify **INTACT**). 기존 cmul(≤c6x) regression 불변 2/2.
  - 결과: **`cmul2_mod91`(7×13, 77g)·`cmul2_mod77`(7×11, 128g)·`cmul2_mod85`(5×17, 148g)** Tier-0 EXACT 봉인 — 전부 c7x 실사용(3/3). 독립 산술순열 u_hash==sealed 3/3·×2 orbit period==ord_N(2) 3/3(12/30/8). **앱 59→62, root 437efbc3→e64f4970**(순수 비파괴: 모듈 50·frozen 23·fingerprint byte-identical, 2회 byte-identity).
- [x] **W6.2 DiscoverSelfAdvance** `[SC][ND]` ✅ 2026-06-28
  - 목표: 발견 루프가 봉인된 frontier를 넘어 자동전진(진짜 self-extending) + 틀린 unlock 주장 정정.
  - 근본원인: `discover.py` `ctx["modules"]`=그래프 *사용* 모듈만(봉인 전체 아님) → 미사용 봉인 gate에 frontier 정체.
  - 산출: `discover.py` 보강 — ctx에 `sealed_modules`(MODREG 스캔) 추가·`gap_to_proposal`이 봉인 gap 스킵·`_round_pkg`(라운드 분리, idempotent)·cNx unlock 텍스트 실측 정정.
  - 결과: forge 후 c7x 그래프 진입(fan-in=3) → propose가 **c8x·cr9_dag_gate** 제안(round2 분리, W2.4 round1 보존). 재실행 시 round2 재사용.
- [x] **W6.3 QFTPipelineExtend-cr8 (iqft8)** `[SC][ND]` ✅ 2026-06-28
  - 목표: W6.1의 대칭 쌍 — 봉인된 cr8_dag(W2.4)를 *실제로 요구하는* 8큐비트 역-QFT 봉인 → QPE counting register 확장.
  - 산출: `scripts/iqft_family.py`(`gen_iqft_pipeline(n)` 파라메트릭 생성기)·`.pgf/DESIGN-Cr8Payoff.md`(PG 설계)·`.pgf/arith/IQFT-FAMILY-REPORT.json`.
  - 분해 패턴(iqft7 도출): 비트반전 swap(i,n-1-i) + 역-QFT 사다리(t=n-1→0, c=n-1→t+1로 cr_{(c-t)+1}_dag(c,t) 후 H(t)). golden=QFT_n† (app_golden 경로).
  - ★**RegressionGate**: `gen_iqft_pipeline(7)`이 봉인 `iqft7` byte-identical 재현(composite==golden 통과 + u_hash `10da0070…` 일치) → 분해 패턴 정확성 입증.
  - 결과: **`iqft8`**(8큐비트, cr8_dag 실사용) Tier-0 EXACT 봉인. QFT8† 독립 재구성 u_hash==sealed(`99f0e17d…`). **앱 62→63, root e64f4970→43580b93**(순수 비파괴: 모듈 50·frozen 23·fingerprint byte-identical, 2회 byte-identity). ※정-QFT(qft8_pipeline)는 cr6/7/8_gate(non-dag) 미봉인 — 후속 후보.
- [x] **W6.4 ForwardQFTPipelineComplete** `[SC][ND]` ✅ 2026-06-28
  - 목표: W6.3(iqft8) 정-방향 대칭 닫기 — 정-QFT pipeline이 cr6/7/8_gate(non-dag) 미봉인으로 막혀 있던 것 잠금해제 → forward QFT pipeline n=8 완결.
  - 산출: `scripts/qft_family.py`(`gen_qft_pipeline(n)` 파라메트릭 생성기 + cr_k_gate 봉인)·`.pgf/DESIGN-QftForward.md`(PG 설계)·`.pgf/arith/QFT-FORWARD-REPORT.json`. `second_oracle`에 cr6/7/8_gate(=cphase(k)) INDEP 추가.
  - 분해 패턴(qft4_pipeline 도출): t=0→n-1로 H(t) 후 c=t+1→n-1로 cr_{(c-t)+1}(c,t)(k2→cs_gate·k3→ct_gate·k≥4→cr{k}_gate), 마지막 비트반전 swap. golden=raw QFT.
  - ★**RegressionGate**: `gen_qft_pipeline(4)`이 봉인 `qft4_pipeline` byte-identical 재현(u_hash `d997d21f…` 일치) → 패턴 정확성 입증.
  - 결과: `cr6/7/8_gate` 봉인(독립 cphase(k) 일치 3/3)·`qft5/6/7/8_pipeline` Tier-0 봉인(qft6/7/8이 cr6/7/8_gate 실사용)·독립 QFT_n u_hash==sealed 4/4. **모듈 50→53·앱 63→67, root 43580b93→ea97a877**(순수 비파괴: frozen 23키·fingerprint byte-identical, second_oracle 53/53, 2회 byte-identity).
- [x] **W6.5 ShorCapstone — genuine distinct-prime Shor-91 (7×13)** `[SC][ND]` ✅ 2026-06-28
  - 목표: W6.1~W6.4가 만든 부품을 완전한 Shor 인수분해 회로로 조립하는 capstone. N=91=7×13(둘 다 >5, 진짜 distinct-prime).
  - 산출: `scripts/shor_capstone.py`(조립 드라이버)·`.pgf/DESIGN-ShorCapstone.md`(PG 설계)·`specs/apps/shor91.app.pg`.
  - 구조: 15q(counting 8 + work 7). H^8 · controlled-U^(2^j)(cmul{2,4,16,74}_mod91, powa=[74,16,74,16,74,16,4,2]) · iqft8. 부품 cmul4/16/74_mod91 신규 forge(c7x-engine, Tier-0 8q, 독립순열 일치).
  - **봉인**: 15q > EXACT_BOUND(12) → **Tier-1 STRUCTURAL**(plan.tier="structural", u_hash=Merkle(자식 sealed u_hash + 배선), dense 미실체화). u_hash `ea39b003…`. 자식 전부 sealed. period readout(illustrative §8.4): ord_91(2)=12 → 2^6=64 → gcd(63,91)=7·gcd(65,91)=13 → 91=7×13.
  - **앱 67→71**(cmul4/16/74_mod91 + shor91), **root ea97a877→93183bcd**(순수 비파괴: 모듈 53·frozen 23·fingerprint byte-identical, reproduce_all REPRODUCED). ⚠ **정직성**: shor91은 *첫 algorithm-scale structural-only 봉인* — dense Tier-0(shor15/21)보다 약한 보증(SEMANTIC-GUARANTEES structural_wellformed=1). t=8 counting(2^8<2r²)는 readout 확률에만 영향(구조봉인 t 무관). 정-QFT(qft9/iqft9)·t=9는 cr9_dag 선행 필요(별건).
- [x] **W7.1 QECStabilizerFamily — 새 알고리즘 클래스(양자오류정정)** `[SC][ND]` ✅ 2026-06-29
  - 목표: gates→QFT→arith→Shor 수직스택 이후 첫 *수평* 확장. QEC stabilizer 인코더 — 전부 Clifford → **Tier-0 EXACT**, 봉인된 base Clifford(`h_gate`·`cnot`)만으로 조립.
  - 산출: `scripts/qec_family.py`(생성기+forge+독립검증)·`.pgf/DESIGN-QECStabilizer.md`(PG 설계)·`specs/apps/{repcode3_bitflip,repcode3_phaseflip,syndrome3_bitflip,shor9_encoder}.app.pg`. forge_apps.py APP_LIST 등록(재현 커버리지).
  - 봉인 4개: `repcode3_bitflip`([[3,1]] bit-flip, 3q, golden=parity perm)·`repcode3_phaseflip`([[3,1]] phase-flip, 3q, golden=H^⊗3@parity)·`syndrome3_bitflip`(신드롬 추출 측정前 parity-copy unitary, 5q)·**`shor9_encoder`**([[9,1,3]] Shor 코드 1995, 9q 512×512 — QEC capstone, golden=P_bitflip@H_{0,3,6}@P_phase).
  - **정직성**: golden=closed-form parity-permutation/Sylvester-Hadamard(Qualtran 비의존 독립경로, qft golden=DFT 선례와 동일 수준). 독립 golden u_hash==sealed **4/4**. 생성≠검증(app_assemble 오라클). plan=봉인 모듈, MatrixGate 0. 측정=비unitary 제외(syndrome=측정前 unitary). ⚠ stabilizer-tableau(Tier-2)가 *더 강한* 독립오라클 — future work. Shor9 `|0_L>`=8 코드워드(블록∈{000,111}, amp=1/2√2) 행동검증 통과.
  - **모듈 53 불변·앱 71→75, root 93183bcd→`06ca92d7`**(순수 비파괴: frozen 23키·fingerprint byte-identical, reproduce_all REPRODUCED, second_oracle 53/53, contested_guard ALL PASS).

---

## Stage D — Backend Evidence (defer, gated) `[EXT]`

- [ ] **WD.1 BackendEvidenceSidecar** `[EXT]` (다수의견 defer)
  - 목표: QASM3 export → Aer noise replay → (선택)real QPU. 산출물 watermark="OBSERVATION — NOT A SEAL". 유일 정당용도=QECGatesCost 예측 vs 실비용 보정.
  - **착수조건**: Stage 1~3 완료 후 + 하드웨어 접근 확보 시에만. 봉인경계 절대 불가침.

---

## 진행 규약

- 각 Work 착수 시: HANDOFF.md 해당 체크박스 `[ ]→[~]`(진행중), 완료 시 `[x]` + 본 파일 동기화.
- Work 완료 정의: 산출물 생성 + 자체 verify PASS + 공통 회귀 그린(reproduce_all REPRODUCED·기존 봉인 byte-identical) + 비파괴 확인. ※성장 Work(신규 봉인)는 root 변경 허용하되 기존 봉인·frozen 23키·fingerprint byte-identical(순수 성장). 현재 root=`e64f4970`.
- **[EXT] Work**는 self-contained 부분(패키지·채점기·스키마)까지 완성 후 `[~]`로 두고 relay 대기.
- Stage 경계마다 전수 회귀 그린 확인.
- git은 정욱님 지시 시에만.

---

## 권장 착수: **W1.1 SampledDenseVerify** (Stage 1)

이유: 8-agent 최약가정(Tier-1=structural≠unitary)을 직격 · 외부의존 0(`[SC]`) · 결정론 보존 설계 명확 · 즉시 인용가능 결과(헤드라인 질적 정직화). Stage 0(W0.1/W0.2)을 선행 또는 병행.
