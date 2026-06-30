# DESIGN — W12.5 Shor119Frontier

> `shor91` 이후의 self-contained Shor frontier. c8x 없이 가능한 최대권역(N<128)에서
> `N=119=7×17`을 선택한다. 새 primitive는 만들지 않고, c7x-enabled modular multiplier 합성으로
> 필요한 controlled multipliers를 Tier-0로 봉인한 뒤 `shor119`를 Tier-1 STRUCTURAL로 조립한다.

## Gantree

```
W12_5_Shor119Frontier // Shor frontier beyond 91: N=119=7×17 (done) @v:1.0
    Design // PGF design + review gate (done)
        # output: DESIGN-ShorFrontier.md, WORKPLAN-ShorFrontier.md, REVIEW-ShorFrontier.md
        # criteria: MasterRoadmap node exists · frontier target justified
    MultiplierSeal // cmul powers for N=119 (done) @dep:Design
        Cmul2Mod119 // existing-family style controlled ×2 mod119, 8q (done)
        Cmul4Mod119 // controlled ×4 mod119, 8q (done)
        Cmul16Mod119 // controlled ×16 mod119, 8q (done)
        Cmul18Mod119 // controlled ×18 mod119, 8q (done)
        Cmul86Mod119 // controlled ×86 mod119, 8q (done)
        # criteria: all Tier-0 EXACT, deps subset sealed MCT up to c7x, independent arithmetic u_hash matches
    ShorStructural // shor119 app (done) @dep:MultiplierSeal
        # process: H^8 · controlled-U^(2^j) using powa=[18,86,18,86,18,16,4,2] · iqft8
        # criteria: Tier-1 STRUCTURAL, n_sys=15, deterministic reassembly same structural hash
    ReadoutObservation // period readout only, not a seal (done) @dep:ShorStructural
        # criteria: ord_119(2)=24, gcd(2^12±1,119) -> 7,17
    Verification // full regression and invariant gates (done) @dep:ReadoutObservation
        # commands: shor_frontier, forge_apps, registry_tools build, semantic_guarantee, citation_gen,
        #           reproduce_all, second_oracle, verify_contested_guard, seal_gate_ci
        # criteria: all pass; root growth only; fingerprint unchanged
    Documentation // handoff/task/status update (done) @dep:Verification
        # criteria: internal docs reflect new counts/root; external docs batch-only
```

## PPR

```python
def w12_shor119_frontier() -> dict:
    """Seal the N=119 Shor frontier without adding a new primitive."""
    # acceptance_criteria:
    #   - target N=119 is distinct-prime and >91
    #   - all generated modular multipliers use sealed MCT deps with max control <= 7
    #   - shor119 is Tier-1 STRUCTURAL, not advertised as dense exact
    #   - period readout is illustrative only
    #   - reproduce_all, second_oracle, seal_gate_ci, contested_guard pass
    design = AI_review_design("N=119 frontier under existing c7x primitive")
    if design.has_fatal_flaw:
        raise RuntimeError(design.reason)
    multipliers = seal_modmul_powers(N=119, powers=[2, 4, 16, 18, 86])
    shor = assemble_structural_shor(N=119, a=2, t=8, work=7)
    readout = observe_period_readout(N=119, a=2)
    regression = run_verification_gates()
    return {"multipliers": multipliers, "shor": shor, "readout": readout, "regression": regression}
```

## 정직성 경계

```python
# cmul*_mod119 = Tier-0 EXACT dense app seals.
# shor119 = Tier-1 STRUCTURAL: dense whole-unitary proof is not claimed.
# period/factor readout = illustrative observation, not seal evidence.
# N>=128 remains blocked until c8x or another 8-control strategy is sealed.
```
