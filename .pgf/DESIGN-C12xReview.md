# C12xReview Design @v:1.0

## Gantree

```text
C12xReview // W12.20 c12x feasibility and cost review only (done) @v:1.0
    ScanCandidates // scan useful semiprime N in [2048,4095] (done)
    MeasureShortlistCost // synthesize top-3 family costs without sealing (done) @dep:ScanCandidates
    DecideNextFrontier // bounded go/no-go with guardrails (done) @dep:MeasureShortlistCost
    UpdateBacklog // record W12.21 finite successor (done) @dep:DecideNextFrontier
```

## PPR

```python
def review_c12x_frontier() -> dict:
    """Review the next 12-control primitive blocker without creating seals."""
    # deterministic code path:
    #   scan N in [2048,4095], a=2, distinct semiprime, useful readout
    #   rank by unique power count, then N
    #   measure top-3 family MMD costs directly; do not call oracle seal
    # acceptance_criteria:
    #   - no specs/modules/c12x.pg and no registry/modules/c12x.sealed.json
    #   - registry root unchanged
    #   - representative target is finite and has max_control == 12
    #   - decision includes memory guard and no payoff-family/full-Shor claim
    return {"recommended_next": "W12.21 C12xPrimitiveFrontier"}
```
