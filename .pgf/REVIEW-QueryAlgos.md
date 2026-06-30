# REVIEW-QueryAlgos

## Scope

- Target: `.pgf/DESIGN-QueryAlgos.md`
- Date: 2026-06-29
- Mode: design-review

## Summary

W12.1 is feasible as an app-only Tier-0 extension. The critical boundary is to keep one-query/query-advantage claims in the behavior report, not in the seal.

## Findings

### [low][feasibility] Simon output width kept minimal
- Evidence: `Simon2_s11` uses 2 query qubits and 1 output qubit for `f(x)=x0 xor x1`.
- Impact: It demonstrates the hidden-period support constraint for `s=11`, but not a larger Simon system.
- Recommendation: Accept for W12.1 because it stays inside one-session Tier-0 scope.

### [low][risk] Deutsch-Jozsa uses representative instances
- Evidence: `dj2_const1` and `dj2_balanced_xor` cover constant and balanced behavior.
- Impact: It is not an exhaustive family over all Boolean functions.
- Recommendation: Mark as representative query-algorithm instances, not full function enumeration.

### [pass][architecture] No new primitive dependency
- Evidence: planned apps reuse `h_gate`, `x_gate`, `cnot`.
- Impact: second_oracle module coverage should remain 62/62.
- Recommendation: Proceed to implementation.

## Verdict

APPROVED — proceed to `AppSeal`.
