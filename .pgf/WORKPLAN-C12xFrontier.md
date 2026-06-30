# C12xFrontier Work Plan

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
C12xFrontier // W12.21 c12x primitive + cmul2_mod3683 payoff only (done) @v:1.0
    SealPrimitive // seal c12x Tier-0 exact module (done)
        # target: registry/modules/c12x.sealed.json
        # criteria: tier=0, n_sys=13, independent cnx_perm(12) hash match
    SealPayoff // seal cmul2_mod3683 Tier-0 exact app (done) @dep:SealPrimitive
        # target: registry/apps/cmul2_mod3683.sealed.json
        # criteria: tier=0, max_control=12, deps include c12x, independent arithmetic hash match
    IntegrateRegistry // connect genskills/reproduce/registry layers (done) @dep:SealPayoff
        # target: scripts/genskills.py, scripts/reproduce_all.py, registry generated files
        # criteria: gen_modmul supports c12x; reproduce_all includes c12x_frontier
    VerifyBoundary // full regression and honesty-boundary verification (done) @dep:IntegrateRegistry
        # criteria: reproduce_all/second_oracle/seal_gate_ci/verify_contested_guard/genskills verify pass
    UpdateBacklog // handoff/remain/task_record update and next candidate selection (done) @dep:VerifyBoundary
        # criteria: W12.21 done, next external bridge candidate proposed, external docs remain batch-only
```
