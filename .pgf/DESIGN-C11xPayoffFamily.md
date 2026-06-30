# C11xPayoffFamily Design @v:1.0

## Gantree

```text
C11xPayoffFamily // W12.18 remaining N=1285 payoff multipliers (done) @v:1.0
    SealRemainingCmul1285 // cmul4/16/256_mod1285 Tier-0 exact apps (done)
    VerifyIndependentArithmetic // independent arithmetic u_hash checks (done) @dep:SealRemainingCmul1285
    UpdateRegistryArtifacts // registry/semantic/citation root refresh (done) @dep:VerifyIndependentArithmetic
    UpdateBacklog // record W12.19 finite successor (done) @dep:UpdateRegistryArtifacts
```

## PPR

```python
def seal_c11x_payoff_family() -> dict:
    """Seal the remaining N=1285 controlled modular multipliers without claiming full Shor."""
    # deterministic code path:
    #   for a in [4,16,256]:
    #       gen_modmul(a, 1285, 12) -> MMD plan -> exact full-basis permutation C-app seal
    #       compare sealed u_hash with independent arithmetic matrix hash
    # acceptance_criteria:
    #   - cmul4_mod1285, cmul16_mod1285, cmul256_mod1285 are Tier-0 exact
    #   - each max_control == 11 and deps include c11x
    #   - independent arithmetic u_hash matches 3/3
    #   - cmul2_mod1285 remains present from W12.17
    #   - no shor1285 structural or dense claim in this node
    return {"new_powers": [4, 16, 256]}
```
