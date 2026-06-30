# REVIEW-Shor635Frontier

## Scope

- Target: W12.15 Shor635StructuralFrontier
- Mode: PGF full-cycle review
- Date: 2026-06-30

## Summary

The design is bounded to the already-planned W12.15 node: exact N=635 multiplier family plus one structural Shor app. The key risk is overstating `shor635`; it must stay Tier-1 structural, while the five `cmul*_mod635` apps carry the exact Tier-0 claims.

## Findings

### [low][architecture] `shor635` is intentionally not dense exact

- Evidence: 18q total width exceeds the dense exact app path used by small circuits.
- Impact: Whole-unitary equivalence cannot be claimed for the full Shor app.
- Recommendation: Keep `shor635` contract as `C1-C4(structural)` and maintain period readout as illustrative only.

### [low][quality] Multiplier synthesis is expensive but deterministic

- Evidence: `cmul131_mod635` and `cmul256_mod635` synthesize thousands of MCT gates.
- Impact: Reproduction takes longer but remains tractable through permutation-space exact checks.
- Recommendation: Keep fast full-basis permutation C-app path and include W12.15 in `FRONTIER_STEPS`.

## Accepted Deferrals

- `c11x` primitive review is not part of W12.15.
- External docs remain blocked until explicit "동기화".

## Next Actions

- Run `scripts/shor635_frontier.py`.
- Rebuild registry and semantic/citation metadata.
- Run global regression gates and update backlog state.
