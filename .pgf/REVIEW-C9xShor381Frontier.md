# REVIEW-C9xShor381Frontier

## Scope

- Target: W12.8-W12.10 combined c9x payoff and Shor-381 structural frontier
- Date: 2026-06-30
- Mode: design-review + verify

## Summary

The combined task is valid only if it includes W12.8, because W12.9 and W12.10 depend on a sealed `c9x`. `N=381=3*127` is the selected target: it is the lowest-cost useful candidate found with four unique powers and all required multipliers exercising max control 9.

## Findings

### [medium][dependency] W12.9/W12.10 require W12.8
- Evidence: `remain_task_list.md` marked W12.9 and W12.10 blocked by W12.8.
- Impact: running W12.9 directly would fail under the previous `gen_modmul` cap.
- Resolution: include W12.8 in this execution batch and seal `c9x` first.

### [low][honesty] shor381 must remain structural
- Evidence: `shor381` is 17q, beyond the dense exact frontier used for Tier-0 apps.
- Impact: claiming whole-unitary exact equivalence would overstate the seal.
- Resolution: seal `shor381` as Tier-1 structural and keep period readout illustrative only.

### [low][scope] iqft9 is not required for this frontier
- Evidence: existing Shor frontier apps use `iqft8`; `iqft9` would require a separate QFT frontier.
- Impact: trying to add `iqft9` would mix two frontiers.
- Resolution: use `T=8`, `iqft8`, and document that the c9x blocker was modular arithmetic.

## Accepted Deferrals

- `c10x` feasibility is deferred to W12.13.
- `iqft9` / `cr9_dag` is not part of this task.

## Verdict

passed
