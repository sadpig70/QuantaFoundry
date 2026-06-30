# REVIEW-Shor221Frontier

## Scope
- Target: W12.7 Shor221 structural frontier design before execution
- Date: 2026-06-30
- Mode: design-review

## Summary
`N=221=13*17` is a suitable first Shor-scale payoff for `c8x`: it has only five unique powers for `t=8`, all required multipliers exercise max control 8, and the final 16q algorithm must be honestly Tier-1 structural.

## Findings

### [medium][scope] The multiplier set must include cmul2_mod221
- Evidence: `powa=[35,120,35,120,35,16,4,2]`; unique powers are `[2,4,16,35,120]`.
- Impact: Reusing `cmul2_mod187` would be mathematically wrong because the modulus is part of the permutation.
- Recommendation: Seal all five `cmul{2,4,16,35,120}_mod221` apps for this task.

### [medium][performance] Public dense app_assemble may be wasteful for 9q permutation plans
- Evidence: `cmul120_mod221` has 921 MCT gates over 9 qubits.
- Impact: Dense matrix composition through every step is correct but unnecessarily slow for pure permutation MCT plans.
- Recommendation: Use an exact permutation-composition fast path that checks the full basis against the arithmetic golden, then emits the same QPGF Tier-0 seal fields.

### [low][honesty] shor221 must remain structural
- Evidence: `shor221` is 16q, exceeding the exact dense bound.
- Impact: Claiming full dense unitary equivalence would overstate the guarantee.
- Recommendation: Seal `shor221` as Tier-1 structural and keep period readout as observation only.

## Accepted Deferrals
- `N>=256` Shor/frontier work is deferred until `c9x` or another 9-control strategy exists.

## Next Actions
- Execute `scripts/shor221_frontier.py`.
- Rebuild registry/semantic/citation artifacts and run full reproduction gates.
