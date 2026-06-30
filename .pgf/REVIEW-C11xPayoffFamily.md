# REVIEW-C11xPayoffFamily

## Scope

- Target: W12.18 C11xPayoffFamily
- Date: 2026-06-30
- Mode: design-review + verify

## Summary

W12.18 is valid as a payoff-family completion step because it seals only the remaining `N=1285` controlled multipliers unlocked by `c11x`. `shor1285` is intentionally left for a separate structural task.

## Findings

### [low][scope] Full Shor-1285 must stay out of W12.18
- Evidence: W12.18 acceptance covers `cmul4_mod1285`, `cmul16_mod1285`, `cmul256_mod1285` only.
- Impact: assembling `shor1285` here would mix exact payoff seals with a weaker structural claim.
- Resolution: add `W12.19 Shor1285StructuralFrontier` as the next finite candidate.

### [low][verification] Existing `cmul2_mod1285` must remain part of family closure
- Evidence: W12.17 sealed `cmul2_mod1285`; W12.18 seals the other unique powers `[4,16,256]`.
- Impact: a complete payoff family requires all four powers to exist before structural assembly.
- Resolution: report `family_seals` for all `cmul{2,4,16,256}_mod1285`.

### [low][boundary] Arithmetic readout remains out of scope
- Evidence: this node does not produce period/factor readout or a Shor app.
- Impact: keeps the exact seal claim narrow and auditable.
- Resolution: no backend/readout claim in W12.18; defer to W12.19 as illustrative only.

## Verdict

passed
