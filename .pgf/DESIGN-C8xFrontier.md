# C8xPrimitiveFrontier Design @v:1.0

> W12.6 self-contained frontier. W12.5가 명시한 `N>=128` modular arithmetic blocker를
> `c8x` primitive 봉인으로 닫고, 실제 8-work-bit multiplier `cmul2_mod187`로 소비를 증명한다.

## Gantree

```
C8xPrimitiveFrontier // 8-control primitive gap closure (in-progress) @v:1.0
    FrontierSelect // choose concrete N>=128 app target (done)
        # input: current genskills max control cap, candidate N values
        # process: measure MMD gate count/max control without changing oracle contracts
        # output: N=187=11*17, a=2, nq=9, gates=105, c8x count=3
        # criteria: target is distinct-prime, N>=128, max_control=8, modest gate count
    SealC8x // seal 8-control X primitive as Tier-0 module (in-progress) @dep:FrontierSelect
        # input: Qualtran MultiControlX(cvs=(1,)*8), independent permutation golden
        # process: verify_seal -> registry/modules/c8x.sealed.json
        # output: c8x module seal, n_sys=9
        # criteria: sealed true, tier=0, independent cnx_perm(8) u_hash matches
    ExtendModmulEngine // allow c8x in MMD modular synthesis (in-progress) @dep:SealC8x
        # input: scripts/genskills.py _MCT_MODULE and cap
        # process: add _MCT_MODULE[8]="c8x", raise cap to >8, update method metadata
        # output: c8x-enabled gen_modmul
        # criteria: existing <=7 targets remain representable; >8 still blocks honestly as c9x missing
    SealCmul187 // seal actual N>=128 multiplier consuming c8x (in-progress) @dep:ExtendModmulEngine
        # input: gen_modmul(2,187,9), app_assemble Tier-0 exact path
        # process: write specs/apps/cmul2_mod187.app.pg, assemble to registry/apps
        # output: cmul2_mod187 Tier-0 app seal
        # criteria: sealed true, tier=0, max_control=8, deps include c8x, independent arithmetic u_hash matches
    RegressionUpdate // integrate deterministic reproduction gates (designing) @dep:SealCmul187
        # input: registry tools, semantic guarantee, second_oracle, seal_gate_ci, reproduce_all
        # process: add c8x checks, rebuild generated registry artifacts, update EXPECT root
        # output: green reproduction and updated manifest/badge/citation
        # criteria: reproduce_all REPRODUCED, second_oracle full pass, contested guard pass, fingerprint unchanged
```

## PPR

```python
def execute_c8x_frontier() -> FrontierReport:
    """Seal c8x and prove it unlocks N>=128 modular arithmetic."""
    target = AI_review_design("candidate N>=128 modular multipliers")
    assert target.N == 187 and target.max_control == 8

    c8x = run_oracle("specs/modules/c8x.pg", out="registry/modules")
    assert c8x.sealed and c8x.tier == 0 and c8x.n_sys == 9
    assert independent_hash(cnx_perm(8)) == c8x.u_hash

    update_genskills_mct_map(max_control=8, new_module="c8x")
    cmul = app_assemble("specs/apps/cmul2_mod187.app.pg", out="registry/apps")
    assert cmul.sealed and cmul.tier == 0
    assert cmul.max_control == 8 and "c8x" in cmul.deps
    assert independent_hash(controlled_modmul_perm(2, 187, 9)) == cmul.u_hash

    # acceptance_criteria:
    #   - c8x Tier-0 exact module seal exists and independent u_hash matches.
    #   - cmul2_mod187 Tier-0 exact app seal exists and actually uses c8x.
    #   - N>=128 blocker is closed honestly; N>=256 remains c9x-blocked.
    #   - registry/reproduce/second_oracle/semantic/contested/fingerprint gates pass.
```
