# remain_task_list — QuantaFoundry 작업 백로그 정본

> 갱신 2026-06-30 · 목적: 앞으로 이어서 할 작업이 산으로 가지 않도록, 완료/후보/외부의존 작업을
> 하나의 짧은 실행 목록으로 고정한다.
>
> 운영 원칙: 상세 작업 로그는 `task_record.md`에만 누적한다. `HANDOFF.md`는 현재상태 인계용으로
> 짧게 유지한다. 외부 소비 3종(`README.md`, `EXTERNAL-ONBOARDING.md`,
> `docs/QuantaFoundry-Technical-Spec.md`)은 정욱님이 "동기화"라고 지시할 때만 batch 갱신한다.
>
> Claude Code 인계 시점: `M2_DocSyncBatch` 완료 직후. 상세 인계서는
> `.pgf/maintenance/CLAUDE-CODE-HANDOFF.md`. 다음 최우선 후보는 `EXT_W3_5_CIPilot`이지만 외부
> repository/path와 CI 수정 권한이 제공되기 전까지는 blocked 상태를 유지한다.

---

## 0. Canonical State

- Registry: **77 modules / 147 unique apps**
- Root: `1134ea04099ea0c16d1681e5a425e4997a53184f1ab85325d4517152be7108db`
- Unique-app split: modules `77 unitary_equiv`; apps `140 unitary_equiv + 1 sampled + 6 structural`
- Semantic headline file split: modules `77 unitary_equiv`; app seal-files `201 unitary_equiv + 1 sampled + 6 structural`
- Structural apps: `shor91`, `shor119`, `shor221`, `shor381`, `shor635`, `shor1285`
- Frozen consensus keys: **23**
- Independent dense module oracle: `second_oracle 71/71`
- One-command verification: `python scripts/reproduce_all.py` -> `REPRODUCED`

---

## 1. 작업 규칙

1. **작업 선택은 이 파일을 기준으로 한다.** 새 self-contained 작업은 먼저 이 목록에 후보로 기록한다.
2. **실행 직전에는 `.pgf/DESIGN-MasterRoadmap.md`에 실행 노드를 추가한다.** 기존 마스터 규율을 유지한다.
3. **한 번에 한 작업만 진행한다.** 한 작업 완료 후 다음 후보를 재평가하고 이 파일을 갱신한다.
4. **완료 이력은 `task_record.md`에 누적한다.** 이 파일에는 긴 로그를 쓰지 않는다.
5. **`HANDOFF.md`는 현재상태와 다음 후보만 유지한다.** 긴 milestone 서사는 금지한다.
6. **오라클은 사용만 한다.** `verify_seal.py`, `contracts.py`는 절대 수정하지 않는다.
7. **growth 작업은 root 변경 허용, 불변 확인 필수.** frozen keys와 oracle fingerprint는 byte-identical이어야 한다.
8. **관찰은 seal이 아니다.** backend/noise/energy/readout은 `OBSERVATION` 또는 illustrative로 분리한다.

---

## 2. PGF Backlog

```text
QuantaFoundryBacklog // 진행 후보 정규화 (in-progress) @v:2026-06-30
    CompletedTrack // 완료된 self-contained 작업 요약 (done)
        W12_1_QueryOracleAlgos // DJ/BV/Simon query apps (done)
        W12_2_QuantumWalk // C4/C8 coined quantum walk apps (done)
        W12_3_Suzuki4 // Yoshida 4th-order Suzuki modules/apps (done)
        W12_4_ErrorMitigationObservation // ZNE observation, seal 0 (done)
        W12_5_Shor119Frontier // shor119 structural frontier (done)
        W12_6_C8xPrimitiveFrontier // c8x + cmul2_mod187 (done)
        W12_7_Shor221StructuralFrontier // shor221 structural frontier (done)
        W12_8_C9xPrimitiveFrontier // c9x primitive + gen_modmul cap 9 (done)
        W12_9_C9xPayoffFamily // cmul{2,4,16,256}_mod381 (done)
        W12_10_ShorN256StructuralFrontier // shor381 structural frontier (done)
        W12_11_FrontierSelector // deterministic frontier candidate ranking (done)
        W12_12_ShorStructuralGeneralizer // reusable Shor structural assembler/verifier (done)
        W12_13_C10xPrimitiveReview // c10x feasibility review only (done)
        W12_14_C10xPrimitiveFrontier // c10x + cmul2_mod635 (done)
        W12_15_Shor635StructuralFrontier // shor635 structural frontier (done)
        W12_16_C11xPrimitiveReview // c11x feasibility review only (done)
        W12_17_C11xPrimitiveFrontier // c11x + cmul2_mod1285 primitive payoff (done)
        W12_18_C11xPayoffFamily // remaining N=1285 payoff multipliers (done)
        W12_19_Shor1285StructuralFrontier // shor1285 Tier-1 structural app (done)
        W12_20_C12xPrimitiveReview // c12x feasibility review only (done)
        W12_21_C12xPrimitiveFrontier // c12x + cmul2_mod3683 primitive payoff (done)
        M4_PostW12ExternalBridgeDesign // W12.21 evidence to EXT unblock map, design-only (done)

    SelfContainedQueue // frontier 자율 확장 — 전면 승인 (2026-06-30) (in-progress)
        AutoFrontier // c13x/payoff/shor3683/신규클래스 자율 착수 가능 — 정욱님 전면 승인, 금지 삭제 (designing)

    MaintenanceQueue // 실행 인프라/문서 정리 후보 (designing)
        M1_ReproduceStepRegistry // reproduce_all frontier steps registry화 (done)
        M2_DocSyncBatch // external docs batch sync — 현재 누적 없음, 다음 delta 누적 후 정욱님 "동기화" 시 재개 (done)
        M3_BacklogCompactionAudit // HANDOFF/remain/task_record size audit (done)

    InfraQueue // 장기 자율 실행 인프라 (designing)
        AutonomyLoop_Design // 단독 자율 루프 PG 설계+시뮬검증 (_workspace/loop) (done)
        AutonomyLoop_MVP // mock→실게이트 연결 1라운드 — 다음 권장 자율작업 (designing) @dep:AutonomyLoop_Design
        AutonomyLoop_Activate // MVP 후 자율 가동(frontier 확장·검증·동기화·커밋·푸쉬 자율) (designing) @dep:AutonomyLoop_MVP

    ExternalQueue // 외부 입력 없이는 착수 금지 (blocked)
        EXT_W3_5_CIPilot // external repository seal-gate pilot (blocked)
        EXT_W4_2_PoisonPanel // weak-model poisoned-lineage real data (blocked)
        EXT_W5_3_RuntimeKeys // runtime ed25519 real keys/signatures (blocked)
        EXT_SD_BackendEvidence // Aer noise or real QPU evidence sidecar (blocked)
        EXT_ServerLink // server-link scope undefined (blocked)
```

---

## 3. Self-Contained Queue Details

### W12.8 — C9xPrimitiveFrontier `[done]`

- Completed: `c9x` Tier-0 module sealed, `gen_modmul` cap raised to 9-control MCTs.
- Evidence: `.pgf/arith/C9X-SHOR381-FRONTIER-REPORT.json`, `registry/modules/c9x.sealed.json`.
- Boundary: `c10x` remains the next primitive blocker.

### W12.9 — C9xPayoffFamily `[done]`

- Completed: `cmul2_mod381`, `cmul4_mod381`, `cmul16_mod381`, `cmul256_mod381`.
- Evidence: all four are Tier-0 exact, max_control=9, deps include `c9x`, independent arithmetic u_hash match 4/4.
- Boundary: no full Shor claim in this node.

### W12.10 — ShorN256StructuralFrontier `[done]`

- Completed: `shor381` Tier-1 structural app, `N=381=3×127`, `a=2`, `T=8`, `WORK=9`.
- Evidence: deterministic structural hash, all children sealed, period readout illustrative only (`ord_381(2)=14 -> factors 3,127`).
- Boundary: 17q structural seal is weaker than dense whole-unitary equivalence.

### W12.11 — FrontierSelector `[done]`

- Completed: deterministic candidate ranking script/report.
- Evidence: `scripts/frontier_selector.py`, `.pgf/arith/FRONTIER-SELECTOR-REPORT.json`.
- Result: best `512..767` c10x-class candidate is `N=635=5×127` (`work=10`, `max_control=10`, unique powers 5, total gates 17250).
- Boundary: report-only; no registry growth.

### W12.12 — ShorStructuralGeneralizer `[done]`

- Completed: reusable `build_shor_spec(app_id, N, a, t=8)` helper path plus verification report.
- Evidence: `scripts/shor_structural_generalizer.py`, `.pgf/arith/SHOR-STRUCTURAL-GENERALIZER-REPORT.json`.
- Result: `shor119`, `shor221`, `shor381` structural hashes/resources and generated plans reproduce exactly.

### W12.13 — C10xPrimitiveReview `[done]`

- Completed: no-seal feasibility/cost review for `c10x`.
- Evidence: `scripts/c10x_review.py`, `.pgf/arith/C10X-PRIMITIVE-REVIEW.json`.
- Result: `GO_FOR_REVIEWED_NEXT_STEP_NOT_NOW`; recommended next target `N=635=5×127`.
- Boundary: no `c10x` spec/seal created; registry root unchanged.

### W12.14 — C10xPrimitiveFrontier `[done]`

- Completed: `c10x` Tier-0 module and `cmul2_mod635` Tier-0 app.
- Evidence: `scripts/c10x_frontier.py`, `.pgf/arith/C10X-FRONTIER-635-REPORT.json`.
- Result: `c10x` independent `cnx_perm(10)` hash matched; `cmul2_mod635` has 638 gates, max_control=10, c10x count 23, independent arithmetic u_hash matched.
- Boundary: full Shor-635 intentionally deferred.

### W12.15 — Shor635StructuralFrontier `[done]`

- Completed: remaining `cmul4_mod635`, `cmul16_mod635`, `cmul131_mod635`, `cmul256_mod635` plus `shor635`.
- Evidence: `scripts/shor635_frontier.py`, `.pgf/arith/SHOR-FRONTIER-635-REPORT.json`.
- Result: all five `N=635` multiplier powers are Tier-0 exact, max_control=10, c10x-consuming, independent arithmetic u_hash 5/5; `shor635` is Tier-1 structural with deterministic reassembly.
- Boundary: full dense `shor635` unitary equivalence is not claimed; period/factor readout remains illustrative.

### W12.16 — C11xPrimitiveReview `[done]`

- Completed: review-only c11x feasibility/cost scan; no `c11x` spec/seal created.
- Evidence: `scripts/c11x_review.py`, `.pgf/arith/C11X-PRIMITIVE-REVIEW.json`.
- Result: 144 useful distinct-semiprime candidates in `[1024,2047]`; top 12 `cmul2` signals all hit the c11x blocker. Representative `N=1285=5×257`, powers `[2,4,16,256]`, total gates 30359, c11 count 493.
- Boundary: registry root unchanged; no primitive seal attempted.

### W12.17 — C11xPrimitiveFrontier `[done]`

- Completed: `c11x` Tier-0 module and `cmul2_mod1285` Tier-0 app.
- Evidence: `scripts/c11x_frontier.py`, `.pgf/arith/C11X-FRONTIER-1285-REPORT.json`.
- Result: `c11x` independent `cnx_perm(11)` hash matched; `cmul2_mod1285` has 4088 gates, max_control=11, c11x count 79, independent arithmetic u_hash matched.
- Boundary: full Shor-1285 intentionally deferred.

### W12.18 — C11xPayoffFamily `[done]`

- Completed: `cmul4_mod1285`, `cmul16_mod1285`, `cmul256_mod1285`.
- Evidence: `scripts/c11x_payoff_family.py`, `.pgf/arith/C11X-PAYOFF-1285-REPORT.json`.
- Result: gates `6815/9126/10330`, max_control=11, c11x counts `120/160/134`, independent arithmetic u_hash 3/3 matched.
- Boundary: full Shor-1285 intentionally deferred.

### W12.19 — Shor1285StructuralFrontier `[done]`

- Completed: `shor1285` Tier-1 STRUCTURAL app, `N=1285=5×257`, `a=2`, `T=8`, `WORK=11`, `n_sys=19`, powa `[1,1,1,1,256,16,4,2]`.
- Evidence: `scripts/shor1285_frontier.py`, `.pgf/arith/SHOR-FRONTIER-1285-REPORT.json`. Multiplier family `cmul{2,4,16,256}_mod1285` already sealed (W12.17/W12.18) — independent arithmetic u_hash 4/4 re-verified, no re-seal. Deterministic structural reassembly; period readout illustrative `ord₁₂₈₅(2)=16 → 2^8 mod 1285=256 → factors [5,257]`.
- Boundary: 19q structural seal is weaker than dense whole-unitary equivalence; period/factor readout is illustrative only.
- Result: root `df18e3ef→5aee6ef2`, 76 모듈 · 146 앱.

### W12.20 — C12xPrimitiveReview `[done]`

- Completed: review-only c12x feasibility/cost scan; no `c12x` spec/seal created.
- Evidence: `scripts/c12x_review.py`, `.pgf/arith/C12X-PRIMITIVE-REVIEW.json`.
- Result: 288 useful distinct-semiprime candidates in `[2048,4095]`; representative `N=3683=29×127`, powers `[2,4,16,256,2925]`, family gates 79552, c12 count 701; `cmul2_mod3683` 1848 gates, c12 count 45.
- Boundary: registry root unchanged; c12x dense estimate is 13q/8192-dim/1024MiB raw matrix, so next attempt needs memory guards.

### W12.21 — C12xPrimitiveFrontier `[done]`

- Completed: guarded attempt closed the 12-control primitive blocker.
- Outputs: `c12x` Tier-0 module plus `cmul2_mod3683` Tier-0 exact app.
- Candidate details: `N=3683=29×127`, `a=2`, `WORK=12`, `NQ=13`, powers `[2,4,16,256,2925]`.
- Evidence: `scripts/c12x_frontier.py`, `.pgf/arith/C12X-FRONTIER-3683-REPORT.json`, `registry/modules/c12x.sealed.json`, `registry/apps/cmul2_mod3683.sealed.json`.
- Result: `c12x` independent `cnx_perm(12)` hash matched; `cmul2_mod3683` has 1848 gates, max_control=12, c12x count 45, independent arithmetic u_hash matched. Root `5aee6ef2→1134ea04`, 77 modules · 147 apps.
- Boundary: payoff family and `shor3683` intentionally deferred; period readout remains illustrative only.

### M4 — PostW12ExternalBridgeDesign `[done]`

- Completed: design-only bridge from W12.21 frontier evidence into blocked external work.
- Scope: map `c12x/cmul2_mod3683` evidence to `EXT_W3_5_CIPilot`, `EXT_W4_2_PoisonPanel`, `EXT_W5_3_RuntimeKeys`, `EXT_SD_BackendEvidence`, and `EXT_ServerLink`.
- Evidence: `.pgf/external/POST-W12-EXT-BRIDGE.json`, `.pgf/DESIGN-PostW12ExternalBridge.md`, `.pgf/REVIEW-PostW12ExternalBridge.md`.
- Result: all EXT items now have value, blocker, unblock input, first action, and trigger-based next decision.
- Boundary: no external execution, no external docs batch sync unless 정욱님 says "동기화", no c13x/review expansion.
- Next: external bridge items only after corresponding unblock input; `M2_DocSyncBatch` repeats only after new `task_record.md` deltas accumulate.

---

## 4. Maintenance Queue Details

### M1 — ReproduceStepRegistry `[done]`

- Completed: `scripts/reproduce_all.py` now uses `FRONTIER_STEPS`.
- Evidence: includes `shor_frontier`, `c8x_frontier`, `shor221_frontier`, `c9x_shor381_frontier`, `c10x_frontier`, `shor635_frontier`, `c11x_frontier`, `c11x_payoff_family`, `shor1285_frontier`, `c12x_frontier`.
- Acceptance: `reproduce_all.py` remains `REPRODUCED`.

### M2 — DocSyncBatch `[done 2026-06-30 · 반복작업, 현재 누적 없음]`

- Trigger: 정욱님 says "동기화" (재발 작업 — 다음 누적분이 쌓이면 다시 대기 상태가 된다).
- Goal: use `task_record.md` to update `README.md`, `EXTERNAL-ONBOARDING.md`, and `docs/QuantaFoundry-Technical-Spec.md` together.
- Last sync: **2026-06-30**, W12.1~M4 누적분 반영(77 모듈·147 앱·root `1134ea04099ea0c16d1681e5a425e4997a53184f1ab85325d4517152be7108db`·second_oracle 71/71·fingerprint 285/285). `task_record.md` 누적 섹션 초기화 완료.
- Pending sync delta: none.
- Acceptance: external docs reflect cumulative state; `task_record.md` cumulative section reset. ✅

### M3 — BacklogCompactionAudit `[done]`

- Completed: machine-check audit script/report.
- Evidence: `scripts/backlog_compaction_audit.py`, `.pgf/maintenance/BACKLOG-COMPACTION-AUDIT.json`.
- Acceptance: line/size budget and current-state marker checks pass.

---

## 5. External Queue

| ID | Status | Blocker | Close Condition |
|---|---|---|---|
| `EXT_W3_5_CIPilot` | blocked | external repository access | run seal-gate CI pilot in real external repo |
| `EXT_W4_2_PoisonPanel` | blocked | real weak-model lineage data | collect panel data and verify rho-discount behavior |
| `EXT_W5_3_RuntimeKeys` | blocked | real runtime keys/signatures | register and verify ed25519 runtime identity proofs |
| `EXT_SD_BackendEvidence` | blocked | Aer noise or real QPU access | create `OBSERVATION` sidecar, not a seal |
| `EXT_ServerLink` | blocked | scope undefined | 정욱님 defines server-link meaning |

---

## 6. 완료 정의

For seal/growth work:

```text
DESIGN/WORKPLAN/REVIEW/status created or updated
implementation script added or updated
seals admitted only through QPGF paths
registry_tools build
semantic_guarantee
citation_gen
seal_gate_ci
second_oracle
verify_contested_guard
reproduce_all
fingerprint hash check
HANDOFF.md + remain_task_list.md + task_record.md updated
```

For observation-only work:

```text
no new seals unless explicitly planned
registry root unchanged
report has OBSERVATION/illustrative boundary
reproduce_all remains REPRODUCED
HANDOFF.md + remain_task_list.md + task_record.md updated
```
