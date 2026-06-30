# REVIEW-C11xFrontier

## Scope

- Target: W12.17 C11xPrimitiveFrontier
- Date: 2026-06-30
- Mode: design-review + verify

## Summary

W12.17 is valid as a primitive frontier step because it closes exactly one new control primitive (`c11x`) and proves one representative 12q modular multiplier payoff (`cmul2_mod1285`). The full Shor-1285 structure is intentionally excluded.

## Findings

### [low][scope] Full Shor-1285 must stay deferred
- Evidence: W12.17 acceptance is `c11x` plus `cmul2_mod1285` only.
- Impact: adding remaining multipliers or full Shor would mix primitive closure with family/algorithm growth.
- Resolution: add `W12.18 C11xPayoffFamily` as the next finite candidate.

### [low][oracle] `c11x` needs independent dense confirmation
- Evidence: 12q dense module cost is still local-feasible but large enough to merit a separate hash check.
- Impact: a bad primitive would invalidate every 11-control modmul consumer.
- Resolution: compare sealed `c11x` u_hash against independent `cnx_perm(11)`.

### [low][boundary] Period/factor readout is not seal evidence
- Evidence: the report includes `ord_1285(2)=16 -> factors [5,257]` only as illustrative readout.
- Impact: users may overread backend-style arithmetic observations as verification.
- Resolution: keep the seal claim limited to Tier-0 unitary equivalence for `c11x` and `cmul2_mod1285`.

## Verdict

passed
