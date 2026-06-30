# REVIEW-ShorFrontier

## Scope

- Target: `.pgf/DESIGN-ShorFrontier.md`
- Date: 2026-06-29
- Mode: design-review

## Summary

W12.5 is feasible if it stays below the c8x boundary. `N=119=7×17` is a clean frontier because it is greater than 91, uses 7 work qubits, and requires no primitive beyond c7x.

## Findings

### [medium][boundary] N>=128 is not self-contained yet
- Evidence: `genskills.gen_modmul` rejects max controls greater than 7.
- Impact: larger work registers would require c8x or a different decomposition strategy.
- Recommendation: choose `N=119` now and record c8x as the next primitive frontier.

### [medium][honesty] shor119 must remain Tier-1 structural
- Evidence: counting 8 + work 7 = 15 qubits, above `EXACT_BOUND=12`.
- Impact: dense whole-unitary equivalence is not claimed.
- Recommendation: keep `plan.tier="structural"` and report readout as illustrative only.

### [pass][coverage] Multiplier apps can be exact
- Evidence: each controlled multiplier is 8q and uses sealed MCT deps up to c7x.
- Impact: the Shor structural tree is built on Tier-0 children.
- Recommendation: seal all required powers independently and add arithmetic u_hash checks.

## Verdict

APPROVED — proceed to implementation.
