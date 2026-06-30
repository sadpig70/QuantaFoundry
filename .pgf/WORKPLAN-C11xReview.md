# C11xReview Work Plan

## POLICY

```python
POLICY = {
    "max_retry": 2,
    "on_blocked": "halt",
    "design_modify_scope": ["impl"],
    "completion": "all_done",
    "max_verify_cycles": 2,
}
```

## Execution Tree

```text
C11xReview // W12.16 review-only next primitive frontier after shor635 (done) @v:1.0
    BoundDenseCost // estimate standalone c11x exact dense oracle cost (done)
    ScanPayoffCandidates // scan N>=1024 Shor payoff candidates without seals (done)
    SelectRepresentative // choose bounded representative target (done) @dep:ScanPayoffCandidates
    VerifyNoSealMutation // prove root/spec/seal unchanged (done) @dep:SelectRepresentative
    UpdateBacklog // record finite next action (done) @dep:VerifyNoSealMutation
```
