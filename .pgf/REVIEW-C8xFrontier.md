# REVIEW-C8xFrontier

## Scope
- Target: W12.6 c8x primitive frontier design before execution
- Date: 2026-06-30
- Mode: design-review

## Summary
The task is self-contained and correctly scoped if it stops at one primitive and one consuming N>=128 app. `c8x` is still within Tier-0 dense feasibility at 9 qubits, and `cmul2_mod187` is a modest 9q app that actually uses 8-control MCT gates.

## Findings

### [medium][scope] Do not jump directly to full Shor N>=128
- Evidence: W12.5 `shor119` was already 15q Tier-1 structural; N=187 full Shor would require larger counting/work composition and likely new QFT/control frontier work.
- Impact: A full Shor attempt would mix primitive closure with algorithm-scale structural growth and obscure the c8x proof.
- Recommendation: Seal `c8x` and `cmul2_mod187` only, then propose Shor143/187 as a separate follow-up.

### [low][honesty] The app must demonstrate actual c8x use
- Evidence: Some N>=128 values can have low-control coincidences; max control must be measured from the MMD plan.
- Impact: A multiplier that does not include `c8x` would not prove the primitive payoff.
- Recommendation: Gate success on `max_control == 8`, deps containing `c8x`, and independent arithmetic u_hash match.

## Accepted Deferrals
- Full `shor187` structural assembly is deferred to the next task because this task's acceptance is primitive closure and first app consumption.

## Next Actions
- Execute `scripts/c8x_frontier.py`.
- Rebuild registry/semantic/citation artifacts and run the full reproduction gate.
