# Shor221StructuralFrontier Design @v:1.0

> W12.7 self-contained frontier. W12.6 `c8x` primitive를 실제 algorithm-scale Shor 구조로 소비한다.
> 목표는 `N=221=13*17`, `a=2`, counting=8, work=8. 전체 `shor221`은 16q이므로
> Tier-1 STRUCTURAL로만 봉인하고 dense whole-unitary exact를 주장하지 않는다.

## Gantree

```
Shor221StructuralFrontier // c8x payoff to Shor-221 structural app (in-progress) @v:1.0
    TargetConfirm // confirm N=221 arithmetic/frontier shape (done)
        # input: c8x-enabled genskills, candidate N>=128 distinct-prime values
        # process: compute powa and MMD gate counts for N=221, a=2
        # output: powa=[35,120,35,120,35,16,4,2], unique=[2,4,16,35,120]
        # criteria: distinct-prime N, unique powers <=5, each multiplier max_control=8
    SealPowerMultipliers // seal required controlled multipliers (in-progress) @dep:TargetConfirm
        # input: gen_modmul(a,221,9) for a in {2,4,16,35,120}
        # process: write app specs and seal exact permutation apps
        # output: cmul{2,4,16,35,120}_mod221 Tier-0 seals
        # criteria: each sealed true, tier=0, deps include c8x, independent arithmetic u_hash matches
    AssembleShor221 // structural Shor circuit assembly (designing) @dep:SealPowerMultipliers
        # input: sealed cmul221 powers, h_gate, iqft8
        # process: H^8 · controlled-U^(2^j)[powa] · iqft8 structural composition
        # output: shor221 Tier-1 structural seal
        # criteria: children sealed, interface placements valid, deterministic structural hash
    RegressionUpdate // deterministic project gates (designing) @dep:AssembleShor221
        # input: registry/semantic/citation/CI/reproduce scripts
        # process: add shor221_frontier to reproduce_all and rebuild generated artifacts
        # output: updated registry root, semantic split, citation, seal badge, reproduce report
        # criteria: reproduce_all REPRODUCED, second_oracle pass, contested guard pass, fingerprints unchanged
```

## PPR

```python
def execute_shor221_frontier() -> FrontierReport:
    """Seal N=221 power multipliers and assemble a structural Shor app."""
    N, a, t, work = 221, 2, 8, 8
    powa = [pow(a, 1 << (t - 1 - q), N) for q in range(t)]
    unique = sorted(set(powa) - {1})
    assert unique == [2, 4, 16, 35, 120]

    for mul in unique:
        spec = gen_modmul(mul, N, nq=9)
        seal = exact_permutation_app_seal(spec)
        assert seal.tier == 0 and "c8x" in seal.deps
        assert independent_hash(controlled_modmul_perm(mul, N, 9)) == seal.u_hash

    shor = structural_compose(
        app_id="shor221",
        steps=["H^8", "controlled cmul powers by powa", "iqft8"],
        n_sys=16,
    )
    assert shor.tier == 1 and shor.contract == "C1-C4(structural)"

    readout = period_readout(N=221, a=2)
    assert readout.order_r == 24 and readout.factors == [13, 17]

    # acceptance_criteria:
    #   - 5 multiplier apps are Tier-0 exact and independently hash-matched.
    #   - shor221 is Tier-1 structural with deterministic reassembly.
    #   - period/factor readout is explicitly illustrative only.
    #   - registry/reproduce/second_oracle/semantic/contested/fingerprint gates pass.
```
