# REVIEW-ErrorMitigation

## Scope

- Target: `.pgf/DESIGN-ErrorMitigation.md`
- Date: 2026-06-29
- Mode: design-review

## Summary

W12.4 is feasible only as an observation layer. It must not add seals, specs, or oracle contract changes.

## Findings

### [medium][honesty] ZNE must not be reported as exact recovery
- Evidence: deterministic depolarizing scale model is a simulator-side assumption, not a hardware fact.
- Impact: exact-looking extrapolation would blur mitigation and verification.
- Recommendation: gate on `noisy_error > zne_error > 0`, not on `zne_error == 0`.

### [medium][architecture] Keep noise outside the seal path
- Evidence: `backend_adapter` is currently a sealed-app execution gate; adding noise there could confuse execution with verification.
- Impact: registry/oracle semantics stay clearer if noise lives in an observation script.
- Recommendation: implement `scripts/error_mitigation_obs.py` as a consumer of `backend_adapter`.

### [pass][root-invariant] No new artifact type is needed
- Evidence: the output is a `.pgf/backend/*.json` report only.
- Impact: `registry_root_hash` should remain `211ef5bb...`.
- Recommendation: explicitly check root before and after.

## Verdict

APPROVED — proceed to observation implementation.
