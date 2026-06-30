# DESIGN — C9xShor381Frontier

> W12.8-W12.10 combined full-cycle. Close the `c9x` primitive gap, prove a
> c9x-consuming payoff family, then assemble the first `N>=256` Shor-style
> structural app.

## Gantree

```text
C9xShor381Frontier // c9x payoff family to Shor-381 structural frontier (done) @v:1.0
    SelectTarget // choose compact N>=256 distinct-prime target (done)
        # input: c8x frontier blocker, gen_modmul MMD synthesis
        # process: scan N in [257,511], a=2, distinct-prime, useful period, small unique powers
        # output: N=381=3*127, T=8, WORK=9, unique powers [2,4,16,256]
        # criteria: all required multipliers require max_control=9 and have nontrivial readout
    SealC9x // seal 9-control MultiControlX primitive (done) @dep:SelectTarget
        # input: QPGF module oracle, independent cnx_perm(9)
        # process: write specs/modules/c9x.pg and verify_seal
        # output: registry/modules/c9x.sealed.json
        # criteria: Tier-0, n_sys=10, independent u_hash match
    ExtendModmulEngine // allow c9x in MMD modular synthesis (done) @dep:SealC9x
        # input: scripts/genskills.py
        # process: add _MCT_MODULE[9]="c9x" and cap >9 as c10x blocker
        # output: c9x-enabled gen_modmul and catalog self-seal
        # criteria: genskills verify INTACT
    SealPayoffFamily // seal c9x-consuming cmul family (done) @dep:ExtendModmulEngine
        # input: N=381, powers [2,4,16,256]
        # process: permutation-space exact C-app check + QPGF app seal fields
        # output: cmul{2,4,16,256}_mod381 Tier-0 apps
        # criteria: all max_control=9, deps include c9x, independent arithmetic u_hash matches 4/4
    AssembleShor381 // lift family to structural Shor app (done) @dep:SealPayoffFamily
        # input: cmul family, h_gate, iqft8
        # process: H^8 · controlled-U^(2^j)[powa] · iqft8 structural composition
        # output: shor381 Tier-1 structural app
        # criteria: deterministic structural hash, all children sealed, readout illustrative only
    UpdateRegistryAndDocs // regenerate registry layers and backlog state (done) @dep:AssembleShor381
        # process: registry_tools, semantic_guarantee, citation_gen, seal_gate_ci, task docs
        # output: root fc9c2184c32281a3..., reports and handoff updated
        # criteria: reproduce_all, second_oracle, seal_gate_ci, contested guard pass
```

## PPR

```python
def execute_c9x_shor381_frontier() -> FrontierReport:
    """Close c9x and lift it to the first N>=256 structural Shor app."""
    target = AI_select_target(
        range_N=(257, 511),
        constraints=["distinct_prime", "a=2", "small_unique_powers", "max_control=9"],
    )
    assert target.N == 381 and target.unique_powers == [2, 4, 16, 256]

    c9x = run_qpgf_oracle("specs/modules/c9x.pg", out="registry/modules")
    assert c9x.tier == 0 and c9x.n_sys == 10
    assert independent_hash(cnx_perm(9)) == c9x.u_hash

    update_genskills_mct_map(max_control=9, new_module="c9x")

    cmuls = seal_cmul_family(N=381, powers=[2, 4, 16, 256])
    assert all(c.tier == 0 and c.max_control == 9 and "c9x" in c.deps for c in cmuls)
    assert independent_arithmetic_match(cmuls) == 4

    shor = assemble_structural_shor(N=381, a=2, T=8, iqft="iqft8")
    assert shor.tier == 1 and shor.deterministic_reassembly

    # acceptance_criteria:
    #   - c9x Tier-0 exact module seal exists and independent u_hash matches.
    #   - four cmul*_mod381 Tier-0 exact app seals consume c9x and match independent arithmetic hashes.
    #   - shor381 is Tier-1 structural with all children sealed; no dense whole-unitary claim.
    #   - period/factor readout is labelled illustrative only.
    #   - registry/reproduce/CI/fingerprint/frozen checks pass.
    return FrontierReport(status="done")
```
