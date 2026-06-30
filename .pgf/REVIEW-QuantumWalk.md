# REVIEW-QuantumWalk

## Scope

- Target: `.pgf/DESIGN-QuantumWalk.md`
- Date: 2026-06-29
- Mode: design-review

## Summary

W12.2 is feasible as an app-only Tier-0 extension. The design keeps shift/coin unitaries in the seal and keeps spread/interference behavior in observation.

## Findings

### [low][feasibility] C8 shift uses existing high-control gates
- Evidence: planned C8 conditional increment/decrement uses `c3x`, `toffoli`, `cnot`, `x`.
- Impact: No new module is required, but the plan is more complex than C4.
- Recommendation: Keep C8 at one step plus a three-step repeated app; avoid larger cycles in this work item.

### [low][risk] Dynamics claims are finite-cycle observations
- Evidence: C4/C8 are tiny cycles with periodic boundary conditions.
- Impact: Do not generalize to asymptotic ballistic scaling.
- Recommendation: Report only normalized position marginals and quantum/classical contrast for these instances.

### [pass][architecture] Clean reuse boundary
- Evidence: app specs reuse sealed primitives and sub-app repeated steps.
- Impact: second_oracle module coverage should remain 62/62.
- Recommendation: Proceed to implementation.

## Verdict

APPROVED — proceed to `AppSeal`.
