# REVIEW-C10xOps

## Scope

- Target: W12.14 C10xPrimitiveFrontier, M1 ReproduceStepRegistry, M3 BacklogCompactionAudit
- Date: 2026-06-30
- Mode: design-review + verify

## Summary

The combined batch is valid because W12.14 creates the next frontier script that M1 must include in the reproduction step registry, and M3 then audits the updated handoff/backlog state. Full Shor-635 is intentionally deferred.

## Findings

### [low][scope] Full Shor-635 must stay out of W12.14
- Evidence: W12.14 acceptance says one c10x-consuming multiplier and no full Shor claim.
- Impact: sealing the whole family here would mix primitive closure with algorithm-scale growth.
- Resolution: seal only `c10x` and `cmul2_mod635`; add `W12.15 Shor635StructuralFrontier` as the next candidate.

### [low][maintenance] M1 should not change step semantics
- Evidence: `reproduce_all.py` previously ran four explicit frontier scripts.
- Impact: refactor could accidentally skip a heavy frontier gate.
- Resolution: use a `FRONTIER_STEPS` list and the same all_ok gate for every script, including `c10x_frontier`.

### [low][audit] task_record may contain old roots by design
- Evidence: `task_record.md` is cumulative history.
- Impact: naive stale-root matching would false-fail M3.
- Resolution: enforce stale current-state roots on `HANDOFF.md` and `remain_task_list.md`; allow historical roots in `task_record.md`.

## Verdict

passed
