# REVIEW-Shor1285Frontier

## Scope

- Target: W12.19 Shor1285StructuralFrontier
- Mode: PGF full-cycle review
- Date: 2026-06-30

## Summary

The design is bounded to the already-planned W12.19 node: assemble one structural Shor
app from the complete, already-sealed N=1285 multiplier family. Unlike W12.15 (shor635),
no multiplier sealing happens here — the `cmul{2,4,16,256}_mod1285` family was already
sealed Tier-0 exact in W12.17/W12.18. The key risk is overstating `shor1285`; it must stay
Tier-1 structural while the multipliers retain the exact Tier-0 claims.

## Findings

### [low][architecture] `shor1285` is intentionally not dense exact

- Evidence: 19q total width (counting=8, work=11) far exceeds the dense exact app path.
- Impact: Whole-unitary equivalence cannot be claimed for the full Shor app.
- Recommendation: Keep `shor1285` contract as `C1-C4(structural)` and maintain period
  readout as illustrative only (`ord_1285(2)=16 -> factors [5, 257]`).

### [low][quality] No re-seal of multipliers avoids redundant heavy synthesis

- Evidence: `cmul*_mod1285` synthesis is thousands of MCT gates; it is already reproduced
  deterministically by `c11x_frontier` and `c11x_payoff_family` in `FRONTIER_STEPS`.
- Impact: `shor1285_frontier.py` only does independent-arithmetic re-verification (dim 2^12)
  plus structural assembly, keeping the step cheap and deterministic.
- Recommendation: Order `shor1285_frontier` after the c11x steps in `FRONTIER_STEPS` so the
  children exist at assembly time.

## Accepted Deferrals

- The next primitive blocker (`c12x` / N in [2048,4095]) is not part of W12.19.
- External docs are outside W12.19 itself; current workspace state records a later batch sync through W12.19.

## Next Actions

- Run `scripts/shor1285_frontier.py`.
- Rebuild registry and semantic/citation metadata; bump `seal_gate_ci` EXPECT_DEFAULT.
- Run global regression gates and update backlog state.
- Note: W12.19 exhausts TrackW12's planned self-contained queue — the next direction
  (continue the c-ladder vs. declare TrackW12 closure) is a 정욱님 decision point.
