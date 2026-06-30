# Shor635Frontier Design @v:1.0

## Gantree

```text
Shor635Frontier // W12.15 c10x payoff to Shor-635 structural app (done) @v:1.0
    SealMultiplierFamily // cmul powers for N=635 exact permutation apps (done)
        SealCmul4 // cmul4_mod635 Tier-0 exact app (done)
        SealCmul16 // cmul16_mod635 Tier-0 exact app (done)
        SealCmul131 // cmul131_mod635 Tier-0 exact app (done)
        SealCmul256 // cmul256_mod635 Tier-0 exact app (done)
        ReverifyCmul2 // existing cmul2_mod635 remains exact and c10x-consuming (done)
    AssembleStructuralShor // shor635 Tier-1 structural app (done) @dep:SealMultiplierFamily
    VerifyRegression // registry and global regression gates (done) @dep:AssembleStructuralShor
    UpdateBacklog // HANDOFF/remain/task_record current-state update (done) @dep:VerifyRegression
```

## PPR

```python
def seal_multiplier_family() -> dict:
    """Seal all required N=635 controlled modular multiplier powers."""
    powers = [2, 4, 16, 131, 256]
    # deterministic code path:
    #   genskills.gen_modmul(a, 635, 11)
    #   mmd_synthesize(full permutation)
    #   full-basis permutation C-app check
    # acceptance_criteria:
    #   - each app has tier == 0 and sealed == true
    #   - each app max_control == 10 and deps includes c10x
    #   - independent arithmetic u_hash matches sealed u_hash for 5/5 powers
    return {"powers": powers}


def assemble_structural_shor() -> dict:
    """Assemble H^8 · controlled-U^(2^j) · iqft8 as Tier-1 structural."""
    powa = [131, 256, 16, 131, 256, 16, 4, 2]
    # acceptance_criteria:
    #   - all h_gate/iqft8/cmul children are sealed
    #   - target widths and placements match n_sys=18
    #   - structural hash is deterministic on reassembly
    #   - period/factor readout is explicitly illustrative, not seal evidence
    return {"powa": powa, "tier": 1}
```
