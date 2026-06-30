# ShorFrontier Work Plan

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
W12_5_Shor119Frontier // Shor frontier beyond 91: N=119=7×17 (done) @v:1.0
    Design // PGF design + review gate (done)
        # criteria: target N=119 selected for N>91 while staying within c7x
    MultiplierSeal // seal cmul powers for N=119 (done) @dep:Design
        # criteria: 5 Tier-0 apps; independent arithmetic checks pass
    ShorStructural // assemble shor119 structural app (done) @dep:MultiplierSeal
        # criteria: Tier-1 structural, n=15, deterministic structural reassembly
    ReadoutObservation // illustrative period/factor readout (done) @dep:ShorStructural
        # criteria: ord_119(2)=24 -> factors [7,17]
    Verification // regression gates and invariant checks (done) @dep:ReadoutObservation
        # criteria: reproduce_all, second_oracle, verify_contested_guard, seal_gate_ci pass
    Documentation // PGF status and handoff update (done) @dep:Verification
        # criteria: status JSON done; HANDOFF/remain/task_record updated
```
