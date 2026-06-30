# REVIEW-Suzuki4

## Scope

- Target: `.pgf/DESIGN-Suzuki4.md`
- Date: 2026-06-29
- Mode: design-review

## Summary

W12.3 is feasible, but unlike W12.1/W12.2 it cannot remain app-only. Yoshida 4th-order coefficients are irrational, so new analytic rotation modules are required for honest exact decomposition.

## Findings

### [medium][feasibility] New modules are necessary
- Evidence: `p=1/(4-4^(1/3))`, `q=1-4p` cannot be built from existing fixed-angle rotations.
- Impact: Module count will grow by 4, and `second_oracle.py` must be updated.
- Recommendation: Accept module growth; reject any approximation or reuse hack that would make the seal dishonest.

### [low][risk] Order observation must use asymptotic ratios
- Evidence: low-k ratios can overshoot before converging to 16 for 4th-order.
- Impact: A naive k=1 to 2 check can misstate the order.
- Recommendation: Gate on late k-doubling ratios, not early transient ratios.

### [pass][architecture] Clean extension of W8.3
- Evidence: S4 is implemented as composition of S2 coefficients, preserving the W8.3 decomposition style.
- Impact: Existing registry/app assembly and second_oracle patterns remain valid.
- Recommendation: Proceed to implementation.

## Verdict

APPROVED — proceed to `ModuleSeal`.
