# Shor635Frontier Work Plan

## POLICY

```python
POLICY = {
    "max_retry": 2,
    "on_blocked": "halt",
    "design_modify_scope": ["impl", "internal_interface"],
    "completion": "all_done",
    "max_verify_cycles": 2,
}
```

## Execution Tree

```text
Shor635Frontier // W12.15 c10x payoff to Shor-635 structural app (done) @v:1.0
    SealMultiplierFamily // cmul powers for N=635 exact permutation apps (done)
        SealCmul4 // cmul4_mod635 Tier-0 exact app (done)
        SealCmul16 // cmul16_mod635 Tier-0 exact app (done)
        SealCmul131 // cmul131_mod635 Tier-0 exact app (done)
        SealCmul256 // cmul256_mod635 Tier-0 exact app (done)
        ReverifyCmul2 // existing cmul2_mod635 remains exact and c10x-consuming (done)
    AssembleStructuralShor // shor635 Tier-1 structural app (done) @dep:SealMultiplierFamily
    VerifyRegression // registry and global regression gates (done) @dep:AssembleStructuralShor
    UpdateBacklog // HANDOFF/remain/task_record current-state update (done) @dep:VerifyRegression
```
