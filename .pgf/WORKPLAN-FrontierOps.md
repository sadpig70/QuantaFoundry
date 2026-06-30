# FrontierOps Work Plan

## POLICY

```python
POLICY = {
    "_version": "2.6",
    "max_retry": 2,
    "on_blocked": "halt",
    "design_modify_scope": ["impl", "internal_interface"],
    "completion": "all_done",
    "max_verify_cycles": 2,
}
```

## Execution Tree

```text
FrontierOps // selector + structural generalizer + c10x review (done) @v:1.0
    FrontierSelector // rank semiprime frontier candidates deterministically (done)
    ShorStructuralGeneralizer // reusable structural Shor builder and verifier (done) @dep:FrontierSelector
    C10xPrimitiveReview // feasibility review for 10-control frontier (done) @dep:ShorStructuralGeneralizer
    BacklogUpdate // mark W12.11-W12.13 done and add W12.14 candidate (done) @dep:C10xPrimitiveReview
```
