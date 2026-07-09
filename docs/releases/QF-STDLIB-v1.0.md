# QF-STDLIB v1.0 Release Notes

Release date: 2026-07-09

Tag: `qf-stdlib-v1.0`

Registry root:
`d177ce9a438a1b2f6a9f9f042e69f5263267148fb3f90930fe611e8ec0a48af7`

## Summary

QF-STDLIB v1.0 is the public consumer layer for the sealed QuantaFoundry registry. It provides stable Canon lookup, root-anchored attestation, convention-pinned circuit adapters, and proof-carrying templates without creating or upgrading any quantum seal.

## Public Surface

- `registry/CANON.json` with 55 canonical entries.
- `qf_stdlib.lookup()` for exact lookup by key, alias, registry id, or `u_hash`.
- `qf_stdlib.attest()` for root-anchored proof objects over sealed artifacts.
- `qf_stdlib.attest_circuit()` for adapter-computed circuit hash lookup with fail-closed semantics.
- `qf_stdlib.check_root()` for fast Canon/registry root drift detection.
- `qf_stdlib.canonical_hash_with_adapter()` for convention-pinned Cirq and PennyLane adapters.
- `qf_stdlib.list_categories()`, `filter_canon_entries()`, and `summarize_canon()` for deterministic Canon discovery.
- `qf_stdlib.templates` for proof-carrying recipes over Canon entries.
- `scripts/qf_stdlib.py` CLI for validation, lookup, attestation, adapter inspection, and template construction.

## Canon Coverage

The v1.0 Canon includes base gates, QFT/iQFT, adders, Grover, QPE, Trotter/Suzuki, block-encoding, QSP/QSVT, qROM, SELECT-PREPARE, RM15 substrates, and Shor-237 modular multiplier components.

Base gate Canon entries include `gate/x`, `gate/z`, `gate/h`, `gate/s`, `gate/t`, `gate/cnot`, `gate/swap`, `gate/cz`, `gate/toffoli`, `gate/fredkin`, `gate/cs`, `gate/ct`, and `gate/ccz`.

## Adapter Decisions

- Cirq: enabled with explicit `qubit_order` and QPGF `hash_unitary` convention.
- PennyLane: enabled with explicit `wire_order` through `qml.matrix(..., wire_order=...)` and QPGF `hash_unitary` convention.
- Qiskit: deferred. The workspace does not currently contain positive and negative convention evidence for enabling Qiskit without ambiguity.

## Proof Templates

The v1.0 template catalog contains:

- `qft_import`
- `qpe_skeleton`
- `trotter_stack`
- `base_gate_bundle`
- `qpe_minimal`
- `qsvt_consumer`
- `shor_modexp_attest`

All template references resolve through Canon. Mixed structural scopes remain explicit; for example, `shor_modexp_attest` does not promote a `subspace_permutation_verified` component to dense unitary equivalence.

## Honesty Boundaries

QF-STDLIB v1.0 does not:

- certify arbitrary circuits,
- rerun the QPGF oracle,
- create new quantum seals,
- convert observations into seals,
- upgrade structural or subspace claims to dense equivalence,
- imply hardware execution.

## Verification

The release gate passed with no registry root change:

```bash
python scripts/qf_stdlib.py check-root
python scripts/qf_stdlib.py validate-canon --write-report
python -m unittest tests.test_qf_stdlib -v
python -m py_compile qf_stdlib/*.py scripts/qf_stdlib.py tests/test_qf_stdlib.py
python scripts/second_oracle.py
python scripts/verify_contested_guard.py
python scripts/reproduce_all.py --changed-only
```

Observed gate results:

- Canon: 55 entries, no errors, no warnings.
- Unit tests: 37 passed.
- Second oracle: 83/83 modules plus app check passed.
- Contested guard: pass=20, fail=0.
- Reproduce changed-only: `REPRODUCED`.
- Registry state: 95 sealed modules, 475 sealed applications.
- Root: unchanged at `d177ce9a438a1b2f6a9f9f042e69f5263267148fb3f90930fe611e8ec0a48af7`.

