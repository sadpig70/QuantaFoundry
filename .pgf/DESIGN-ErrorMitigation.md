# DESIGN — W12.4 ErrorMitigationObservation

> Zero-noise extrapolation(ZNE)을 관찰 전용 계층으로 추가한다. 봉인은 추가하지 않는다. 입력은 이미 봉인된
> Tier-0 앱이고, `backend_adapter.load_sealed_app`의 u_hash gate를 통과한 유니터리만 실행한다.

## Gantree

```
W12_4_ErrorMitigationObservation // zero-noise extrapolation observation (done) @v:1.0
    Design // PGF design + review gate (done)
        # output: DESIGN-ErrorMitigation.md, WORKPLAN-ErrorMitigation.md, REVIEW-ErrorMitigation.md
        # criteria: MasterRoadmap node exists · mitigation boundary explicit
    NoiseModel // deterministic observation-only noise model (done) @dep:Design
        # input: sealed app statevector expectation
        # process: global depolarizing expectation E_s = a_s E_ideal + (1-a_s) Tr(O)/d, a_s=(1-eps)^s
        # criteria: deterministic, no registry/oracle mutation, seed-free exact arithmetic
    ZNEObservation // zero-noise extrapolation (done) @dep:NoiseModel
        # input: noise scales 1,3,5
        # process: linear fit vs scale, evaluate at scale=0
        # criteria: noisy bias visible, extrapolation reduces error, residual remains
    Verification // invariant checks (done) @dep:ZNEObservation
        # commands: error_mitigation_obs, registry_tools build, reproduce_all, seal_gate_ci, second_oracle, fingerprint
        # criteria: root unchanged at 211ef5bb..., all regression gates pass
    Documentation // handoff/task/status update (done) @dep:Verification
        # criteria: HANDOFF/remain/task_record updated; external docs batch-only
```

## PPR

```python
def w12_error_mitigation_observation() -> dict:
    """Observe ZNE over sealed circuits without creating seals."""
    # acceptance_criteria:
    #   - MasterRoadmap contains W12_4 before implementation
    #   - no new specs/modules/apps or registry seals are created
    #   - each observation loads an already sealed Tier-0 app through backend_adapter
    #   - ZNE reduces scale-1 noisy bias but does not claim exact recovery
    #   - registry_root_hash remains 211ef5bb...
    design = AI_review_design("ZNE as observation, not seal")
    if design.has_fatal_flaw:
        raise RuntimeError(design.reason)
    report = run_zne_observation(apps=["tfim3_suzuki4_step", "qaoa_p3"])
    gates = run_regression_gates(expect_root="211ef5bb910304d3")
    return {"report": report, "regression": gates}
```

## 정직성 경계

```python
# 봉인 아님: noise model, noisy expectation, ZNE extrapolation은 모두 observation.
# mitigation은 exact reconstruction이 아니라 bias reduction estimate.
# root 불변이 핵심 acceptance: registry_root_hash가 바뀌면 실패.
```
