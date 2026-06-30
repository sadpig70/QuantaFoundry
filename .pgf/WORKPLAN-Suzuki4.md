# Suzuki4 Work Plan

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
W12_3_Suzuki4 // 4th-order Yoshida-Suzuki Hamiltonian simulation steps (done) @v:1.0
    Design // PGF design + review gate (done)
        # criteria: MasterRoadmap node exists; design/review artifacts record Tier vs observation boundary
    ModuleSeal // implement coefficient modules and second_oracle formulas (done) @dep:Design
        # criteria: 4 Tier-0 module seals; second_oracle coverage updated
    AppSeal // implement rzz half apps and TFIM3/4 S4 apps (done) @dep:ModuleSeal
        # criteria: 4 Tier-0 app seals; specs/apps and registry/apps produced
    Observation // 1st/2nd/4th-order scaling report (done) @dep:AppSeal
        # criteria: ratio~2,4,16 asymptotically for TFIM3 and TFIM4; observation != seal
    Verification // regression gates and invariant checks (done) @dep:Observation
        # criteria: reproduce_all, second_oracle, verify_contested_guard, seal_gate_ci pass
    Documentation // HANDOFF/task_record/status update (done) @dep:Verification
        # criteria: internal canonical docs reflect updated module/app count and root
```
