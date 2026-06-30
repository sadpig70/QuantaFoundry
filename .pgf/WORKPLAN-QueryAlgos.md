# QueryAlgos Work Plan

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
W12_1_QueryOracleAlgos // Query/oracle algorithms (done) @v:1.0
    Design // PGF design + review gate (done)
        # criteria: MasterRoadmap node exists; design/review artifacts record Tier vs observation boundary
    AppSeal // implement generator, app specs, forge list (done) @dep:Design
        # criteria: 4 Tier-0 app seals; 신규 모듈 0; specs/apps and registry/apps produced
    Observation // query behavior report (done) @dep:AppSeal
        # criteria: DJ/BV deterministic checks and Simon support check pass; observation != seal
    Verification // regression gates and invariant checks (done) @dep:Observation
        # criteria: reproduce_all, second_oracle, verify_contested_guard, seal_gate_ci pass
    Documentation // HANDOFF/task_record/status update (done) @dep:Verification
        # criteria: internal canonical docs reflect 68 modules, 109 apps, new root
```
