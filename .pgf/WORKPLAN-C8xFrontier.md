# C8xPrimitiveFrontier Work Plan

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
C8xPrimitiveFrontier // 8-control primitive gap closure (done) @v:1.0
    FrontierSelect // choose concrete N>=128 app target (done)
        # criteria: target is distinct-prime, N>=128, max_control=8, modest gate count
    SealC8x // seal 8-control X primitive as Tier-0 module (done) @dep:FrontierSelect
        # criteria: sealed true, tier=0, independent cnx_perm(8) u_hash matches
    ExtendModmulEngine // allow c8x in MMD modular synthesis (done) @dep:SealC8x
        # criteria: existing <=7 targets remain representable; >8 still blocks honestly as c9x missing
    SealCmul187 // seal actual N>=128 multiplier consuming c8x (done) @dep:ExtendModmulEngine
        # criteria: sealed true, tier=0, max_control=8, deps include c8x, independent arithmetic u_hash matches
    RegressionUpdate // integrate deterministic reproduction gates (done) @dep:SealCmul187
        # criteria: reproduce_all REPRODUCED, second_oracle full pass, contested guard pass, fingerprint unchanged
```
