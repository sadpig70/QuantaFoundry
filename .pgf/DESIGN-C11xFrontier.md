# C11xFrontier Design @v:1.0

## Gantree

```text
C11xFrontier // W12.17 c11x primitive plus representative N=1285 payoff (done) @v:1.0
    SealC11x // c11x Tier-0 exact module (done)
    ExtendModmulCap // gen_modmul cap extended to 11 controls (done) @dep:SealC11x
    SealCmul1285 // cmul2_mod1285 Tier-0 exact app (done) @dep:ExtendModmulCap
    VerifyRegression // registry/global regression gates (done) @dep:SealCmul1285
    UpdateBacklog // record W12.18 finite successor (done) @dep:VerifyRegression
```

## PPR

```python
def seal_c11x_frontier() -> dict:
    """Seal c11x and exactly one representative 12q modular multiplier."""
    # deterministic code path:
    #   specs/modules/c11x.pg -> qpgf verify_seal.py
    #   genskills._MCT_MODULE[11] = "c11x"
    #   gen_modmul(2, 1285, 12) -> full-basis permutation C-app check
    # acceptance_criteria:
    #   - c11x sealed tier 0 and independent cnx_perm(11) hash matches
    #   - cmul2_mod1285 sealed tier 0, max_control == 11, deps includes c11x
    #   - independent arithmetic u_hash matches sealed app
    #   - shor1285 is not attempted
    return {"target": "cmul2_mod1285"}
```
