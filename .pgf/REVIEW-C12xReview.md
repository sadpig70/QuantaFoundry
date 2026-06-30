# REVIEW-C12xReview

## Scope

- Target: W12.20 C12xPrimitiveReview
- Date: 2026-06-30
- Mode: design-review + verify

## Summary

W12.20 is valid as a review-only continuation because it measures the next `c12x` blocker without creating any spec or seal. The result opens only one guarded successor: `c12x` plus `cmul2_mod3683`, not a payoff family or Shor app.

## Findings

### [low][scope] Review-only must keep root unchanged
- Evidence: W12.20 acceptance forbids `c12x` spec/seal creation.
- Impact: accidental sealing would bypass the memory-risk decision gate.
- Resolution: assert no `specs/modules/c12x.pg`, no `registry/modules/c12x.sealed.json`, and unchanged registry root.

### [medium][resource] c12x dense exact path is materially heavier
- Evidence: 13q dense unitary dimension is 8192, complex128 raw matrix is 1024 MiB before temporaries.
- Impact: a blind seal attempt may exceed local memory/time.
- Resolution: W12.21 must start with `c12x` only and abort cleanly if local resources fail.

### [low][boundary] Do not bundle family or full Shor with primitive closure
- Evidence: representative `N=3683` family cost is 79552 gates and c12 count 701.
- Impact: bundling family growth hides the primitive-oracle risk.
- Resolution: W12.21 should attempt only `cmul2_mod3683` after `c12x` seals.

## Verdict

passed
