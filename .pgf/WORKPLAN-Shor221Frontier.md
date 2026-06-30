# Shor221StructuralFrontier Work Plan

## POLICY

```python
POLICY = {
    "_version": "2.6",
    "max_retry": 3,
    "on_blocked": "halt",
    "design_modify_scope": ["impl", "internal_interface"],
    "completion": "all_done",
    "max_verify_cycles": 2,
    "max_iterations": 20,
}
```

## Execution Tree

```
Shor221StructuralFrontier // c8x payoff to Shor-221 structural app (done) @v:1.0
    TargetConfirm // confirm N=221 arithmetic/frontier shape (done)
        # criteria: distinct-prime N, unique powers <=5, each multiplier max_control=8
    SealPowerMultipliers // seal required controlled multipliers (done) @dep:TargetConfirm
        # criteria: each sealed true, tier=0, deps include c8x, independent arithmetic u_hash matches
    AssembleShor221 // structural Shor circuit assembly (done) @dep:SealPowerMultipliers
        # criteria: children sealed, interface placements valid, deterministic structural hash
    RegressionUpdate // deterministic project gates (done) @dep:AssembleShor221
        # criteria: reproduce_all REPRODUCED, second_oracle pass, contested guard pass, fingerprints unchanged
```
