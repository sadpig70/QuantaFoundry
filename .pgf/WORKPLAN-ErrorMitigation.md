# ErrorMitigation Work Plan

## POLICY

```python
POLICY = {
    "_version": "2.6",
    "max_retry": 3,
    "on_blocked": "halt",
    "design_modify_scope": ["impl", "internal_interface"],
    "completion": "all_done",
    "max_verify_cycles": 2,
}
```

## Execution Tree

```
W12_4_ErrorMitigationObservation // zero-noise extrapolation observation (done) @v:1.0
    Design // PGF design + review gate (done)
        # criteria: roadmap node exists; boundary says observation only
    NoiseModel // deterministic depolarizing expectation model (done) @dep:Design
        # criteria: no backend_adapter mutation required; no seal/registry writes
    ZNEObservation // run scale=1,3,5 and extrapolate to zero noise (done) @dep:NoiseModel
        # criteria: noisy_error > zne_error > 0 for all cases
    Verification // root-invariant regression gates (done) @dep:ZNEObservation
        # criteria: reproduce_all, second_oracle, seal_gate_ci, root check, fingerprint pass
    Documentation // PGF status and handoff update (done) @dep:Verification
        # criteria: status JSON done; HANDOFF/remain/task_record updated
```
