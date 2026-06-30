# C11xReview Design @v:1.0

## Gantree

```text
C11xReview // W12.16 review-only next primitive frontier after shor635 (done) @v:1.0
    BoundDenseCost // estimate standalone c11x exact dense oracle cost (done)
    ScanPayoffCandidates // scan N>=1024 Shor payoff candidates without seals (done)
    SelectRepresentative // choose bounded representative target (done) @dep:ScanPayoffCandidates
    VerifyNoSealMutation // prove root/spec/seal unchanged (done) @dep:SelectRepresentative
    UpdateBacklog // record finite next action (done) @dep:VerifyNoSealMutation
```

## PPR

```python
def review_c11x_frontier() -> dict:
    """Bound c11x feasibility without creating specs or seals."""
    # deterministic code path:
    #   scan distinct semiprimes N in [1024, 2047]
    #   rank by unique Shor powers then N
    #   sample top candidates through gen_modmul blocker signal
    #   synthesize one representative power-family cost with mmd_synthesize
    # acceptance_criteria:
    #   - registry_root_before == registry_root_after
    #   - specs/modules/c11x.pg absent
    #   - registry/modules/c11x.sealed.json absent
    #   - decision is explicit and successor is finite
    return {"mode": "review-only"}
```
