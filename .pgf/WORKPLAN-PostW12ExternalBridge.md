# PostW12ExternalBridge Work Plan

## POLICY

```python
POLICY = {
    "max_retry": 2,
    "on_blocked": "skip_and_continue",
    "design_modify_scope": ["impl"],
    "completion": "all_done_or_blocked",
    "max_iterations": 20,
}
```

## Execution Tree

```text
PostW12ExternalBridge // M4 design-only bridge from W12.21 evidence to external work (done) @v:1.0
    EvidencePack // freeze W12.21 consumable evidence (done)
        # criteria: current root/counts/checks referenced; no new seal/root mutation
    ExtMap // map each blocked EXT item to value/blocker/unblock condition (done) @dep:EvidencePack
        # criteria: all EXT items have value, blocker, unblock input, first action
    ExecutionOrder // rank external follow-up sequence without starting it (done) @dep:ExtMap
        # criteria: next action depends on explicit trigger/input, no c13x/shor3683 proposal
    BoundaryGuard // keep docs sync and external execution behind explicit triggers (done) @dep:ExecutionOrder
        # criteria: M2 only on "동기화"; EXT only after blocker removed
    BacklogUpdate // update handoff/remain/task_record with bridge result (done) @dep:BoundaryGuard
        # criteria: M4 done; no self-contained frontier task left
```
