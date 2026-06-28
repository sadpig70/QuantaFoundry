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

- [ ] **W2.1 ValueFunction** `[SC][ND]`
  - 목표: `value=0.25·Novelty+0.20·Sealability+0.20·Composability+0.15·ResourceΔ+0.10·ConsensusEst−0.20·Ambiguity−0.15·Cost`. Composability=dep-graph fan-in(BLOCKED 노드 prereq 수, c6x 패턴). Novelty는 객관근거(GenSkill 재현불가+sealed 조합 표현불가) 강제.
  - 산출: `scripts/discover.py`(value 함수) · `.pgf/discover/CANDIDATE-RANK.json`.
  - verify: c6x/sx 사례를 *사후*가 아닌 *사전* 상위랭크로 포착(retrospective 검증).
- [ ] **W2.2 ExploitAxis (분해 최적화기)** `[SC][ND]`
  - 목표: 타깃 유니터리 고정, 분해만 MCTS/진화 탐색 → 오라클=하드보상(봉인=1, resource=연속). reward-hacking 구조차단(봉인 못하면 0). cmul4(2-Fredkin) 사례 정형화.
  - 산출: `scripts/decomp_optimizer.py` · 더 싼 봉인 분해 후보(동일 u_hash, 낮은 T/Toffoli).
  - verify: 기존 봉인과 동일 u_hash 유지하며 자원 감소 1건 이상 · capability-coverage 게이트(trivial 양산 차단).
- [ ] **W2.3 GoalSelectionGuard** `[SC][ND]` (A3 고유통찰)
  - 목표: 생성·확립엔 cross-model 체크 있으나 *무엇을 만들지* 선택엔 부재(미명명 실패모드). 목표선택에 coverage/independence 게이트.
  - 산출: `scripts/discover.py`(guard) · 선택 거부 로그.
- [ ] **W2.4 PrimitiveProposalRound** `[EXT]`
  - 목표: capability-gap("6-control 필요, 제약 X") → 6런타임 패널 decomposition 제안 → 수렴+sympy proof → key-free 봉인. sx/c6x가 template를 standing loop로 승격.
  - 산출: `_workspace/crossmodel/discover_round1/` 패키지 · 수거 후 봉인.
  - relay: 정욱님 6런타임 배포→수거. **EXT 의존.**

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

- [ ] **W3.1 QasmExport** `[SC][ND]`
  - 목표: sealed app/module → OpenQASM3. decomp_guard가 plan=실회로 보장 → export 정직. 외부도구가 registry 소비 가능.
  - 산출: `scripts/qasm_export.py` · 샘플 export(shor21_a2·qft3).
  - verify: export 회로 재시뮬 == sealed u_hash(round-trip 일관) · registry 무변경.
- [ ] **W3.2 QasmIngestion** `[SC]`
  - 목표(A3 우선): OpenQASM3/Qiskit → spec 변환 → *기존 회로* 봉인. 진입장벽(이미 가진 회로 봉인) 해소.
  - 산출: `scripts/qasm_ingest.py` · 외부회로→.pg→seal 데모.
- [ ] **W3.3 CLI** `[SC]`
  - 목표: `qf verify/seal/compose/reproduce --expect-root 3dae613d/explain/export`.
  - 산출: `scripts/qf_cli.py`(기존 스크립트 래핑, 신규 로직 0).
- [ ] **W3.4 CitableRegistry** `[SC]`
  - 목표: release 마다 Zenodo DOI + `CITATION.cff` → 논문 "QPGF-sealed root X" 인용(재현성 위기 대응).
  - 산출: `CITATION.cff` · release 메타.
- [ ] **W3.5 SealGateCI** `[EXT]`
  - 목표: GitHub Action — PR 회로 QPGF 검증 → Seal Badge(Tier+ResourceCost). friendly 외부 라이브러리 1곳 파일럿. CI gate="로컬 재현 성공해야 제출".
  - relay: 외부 라이브러리 협업 필요. **EXT 의존.**

---

## Stage 4 — Consensus 정직종결: ρ 실데이터 (Track B2) `[EXT]`

```
Stage4 // ρ-discount 실가동 또는 "미가동" 최종확정 (designing)
    W4.1_ConventionIndependenceAudit // second_oracle 독립유도 검증 (designing) [SC]
    W4.2_PoisonedLineagePanel // 상관오류 강제유발 (designing) [EXT]
```

- [ ] **W4.1 ConventionIndependenceAudit** `[SC][ND]` (A3 고유통찰)
  - 목표: convention 단일문화(big-endian/atol/전역위상)가 전역 단일실패점. `second_oracle`가 endian/위상을 *독립유도*하는가 *가정*하는가 판정.
  - 산출: `scripts/convention_audit.py` · 판정 리포트.
  - verify: 가정이면 갭 문서화(검증 필요 명시).
- [ ] **W4.2 PoisonedLineagePanel** `[EXT]`
  - 목표: 표준게이트 co-error 유발 불가(4라운드 종료) → co-error를 *구성*. poisoned/lineage-correlated unit을 패널에 투입(little-endian QFT·conjugate-stated-standard·corpus-sparse phase). 계보공유 2소스가 *틀리게* 합의 시 ρ-discount가 joint vote를 <2 independent로 붕괴시키는가?
  - 산출: `_workspace/crossmodel/p3d_round5_poison/` · `scripts/rho_validation.py` · `docs/TRUST-MODEL-VALIDATION-REPORT.md`.
  - 결과: 실 상관오류 1건 → ρ 실가동 입증 / 여전히 0 → "설계됨·미가동" 최종라벨(과장위험 제거). **어느 쪽이든 정직 종결.**
  - relay: poisoned/약모델 패널 구성 필요. **EXT 의존.**

---

## Stage 5 — Hardening 잔여 (Track E) `[SC]`

```
Stage5 // blind-spot 비파괴 방어 (designing)
    W5.1_DeterminismEnvPin // BLAS/FP/platform lockfile+container (designing)
    W5.2_OracleRevocationProtocol // rollback+revocation_list 운영 (designing)
    W5.3_RuntimeIdentityProof // Sybil 암호증명 (designing) [EXT]
```

- [ ] **W5.1 DeterminismEnvPin** `[SC]`
  - 목표: numpy/BLAS/platform/FP가 byte-identity 위협(외부 재검증 신뢰조건). lockfile + container hash + cross-platform 재현 시험.
  - 산출: `requirements.lock` · `scripts/determinism_env_check.py` · 컨테이너 fingerprint.
- [ ] **W5.2 OracleRevocationProtocol** `[SC]`
  - 목표: fingerprint 버그/업그레이드 시 전봉인 무효 + revocation_list 빈배열. rollback + emergency re-seal 절차 문서화.
  - 산출: `scripts/oracle_rollback_protocol.py` · `docs/EMERGENCY-RESEAL.md` · revocation_list 운영.
- [ ] **W5.3 RuntimeIdentityProof** `[EXT]`
  - 목표: gated panel이 "≥2 distinct weights"를 runtime 자기식별으로 검증 → Sybil. API key fingerprint/signed submission bundle.
  - 산출: `scripts/runtime_identity.py` · signed bundle 스키마.

---

## Stage D — Backend Evidence (defer, gated) `[EXT]`

- [ ] **WD.1 BackendEvidenceSidecar** `[EXT]` (다수의견 defer)
  - 목표: QASM3 export → Aer noise replay → (선택)real QPU. 산출물 watermark="OBSERVATION — NOT A SEAL". 유일 정당용도=QECGatesCost 예측 vs 실비용 보정.
  - **착수조건**: Stage 1~3 완료 후 + 하드웨어 접근 확보 시에만. 봉인경계 절대 불가침.

---

## 진행 규약

- 각 Work 착수 시: HANDOFF.md 해당 체크박스 `[ ]→[~]`(진행중), 완료 시 `[x]` + 본 파일 동기화.
- Work 완료 정의: 산출물 생성 + 자체 verify PASS + 공통 회귀 그린(root 3dae613d 불변) + 비파괴 확인.
- **[EXT] Work**는 self-contained 부분(패키지·채점기·스키마)까지 완성 후 `[~]`로 두고 relay 대기.
- Stage 경계마다 전수 회귀 그린 확인.
- git은 정욱님 지시 시에만.

---

## 권장 착수: **W1.1 SampledDenseVerify** (Stage 1)

이유: 8-agent 최약가정(Tier-1=structural≠unitary)을 직격 · 외부의존 0(`[SC]`) · 결정론 보존 설계 명확 · 즉시 인용가능 결과(헤드라인 질적 정직화). Stage 0(W0.1/W0.2)을 선행 또는 병행.
