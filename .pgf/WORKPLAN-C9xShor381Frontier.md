# C9xShor381Frontier Work Plan

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

```text
C9xShor381Frontier // c9x payoff family to Shor-381 structural frontier (done) @v:1.0
    SelectTarget // choose compact N>=256 distinct-prime target (done)
    SealC9x // seal 9-control MultiControlX primitive (done) @dep:SelectTarget
    ExtendModmulEngine // allow c9x in MMD modular synthesis (done) @dep:SealC9x
    SealPayoffFamily // seal c9x-consuming cmul family (done) @dep:ExtendModmulEngine
    AssembleShor381 // lift family to structural Shor app (done) @dep:SealPayoffFamily
    UpdateRegistryAndDocs // regenerate registry layers and backlog state (done) @dep:AssembleShor381
```
