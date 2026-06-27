---
name: qpgf-oracle
description: "QPGF termination oracle (ContractGate): deterministically verifies quantum-module PG specs and writes a tamper-evident *.sealed.json only when the contract passes. Provides the stop condition for runtime-native AI repair loops: generate, verify, revise, repeat. Triggers: quantum module verification, seal, verify_seal, ContractGate, termination oracle, qpgf oracle."
---

# qpgf-oracle — QPGF Termination Oracle

Quantum bugs can be silent. A compiler will not usually tell you that a generated quantum module has the wrong phase, endian convention, ancilla behavior, or FTQC resource profile.

This skill provides a deterministic stop condition for AI-native repair loops:

```text
exit 0  <=>  <id>.sealed.json exists  <=>  loop terminates
```

If verification fails, the oracle does not seal.

## What It Is

`qpgf-oracle` is a process-free skill bundle. An agent writes a `.pg` module spec and runs:

```bash
python scripts/verify_seal.py <spec.pg> --out <dir>
```

The script:

1. loads the fenced PG blocks;
2. instantiates the Qualtran `bloq`;
3. computes `bloq.tensor_contract()`;
4. checks the deterministic contracts;
5. counts FTQC resources;
6. writes `<id>.sealed.json` only on success.

The seal authority comes from deterministic verification code and tamper-evident fields, not from the caller, MCP wrapper, or AI runtime.

## Workflow

```text
1. design
   Write a module spec with:
   - ```python id=bloq```
   - ```python id=golden```
   - ```json id=meta```

2. guard
   python scripts/spec_guard.py spec.pg
   Non-trivial modules require an independent golden reference.

3. loop
   python scripts/verify_seal.py spec.pg --out <dir>
     exit 0 -> sealed module accepted
     exit 1 -> read structured signal, revise spec, repeat
```

The loop is not implemented by QPGF. The loop belongs to the runtime. This bundle supplies the oracle.

## Scripts

| File | Role |
|---|---|
| `verify_seal.py` | termination oracle: spec -> tensor -> contracts -> resources -> seal |
| `contracts.py` | C1-C4, isometry, composition, embedding checks |
| `spec_guard.py` | spec sufficiency gate; blocks missing `golden` for non-trivial modules |
| `golden_guard.py` | independence gate; blocks self-referential or trivial `golden` patterns |
| `registry.py` | seal admission, composition, provenance, INV1-INV3 |
| `app_assemble.py` | recursive app assembly, heterogeneous placement, seal tiers, C-app |
| `bundle_manifest.py` | creates and verifies `BUNDLE.sha256` |
| `clifford_seal.py` | Tier 2 Clifford sealing by stabilizer tableau |
| `zx_seal.py` | Tier 3 Clifford+T sealing by ZX equivalence (+ dense / optional MQT QCEC fallback) |
| `verify_bundle.py` | deployment trust gate: manifest plus signature (Sigstore/cosign or GPG) |
| `test_*.py` | self-tests; current public target is 157 green checks |

## Core Contracts

- **C1 FullCharacterization**: complete unitary/isometry shape is required.
- **C2 PhasePreserved**: complex amplitudes and phases are preserved through unitarity/isometry.
- **C3 AncillaClean / C3-iso**: ancilla behavior is clean or faithfully embedded.
- **C4 ComposableContract**: the effective operation matches an independent `golden` reference, or a composition is re-verified.
- **C-app**: a decomposed application matches the application-level intent.

See `references/contract-spec.md`.

## Canonical Convention

The seal path uses:

```text
Qualtran-native raw tensor_contract()
big-endian basis order
first register = MSB
no automatic alignment search
```

`golden` must use the same convention.

## Trust Boundary

AI may generate and repair candidate specs.
The oracle performs verification deterministically.

The `*.sealed.json` signature is tamper-evident, not a private-key signature.
Release trust requires bundle manifest verification and, for distribution, a maintainer signature or equivalent trust anchor.
See `references/DEPLOYMENT-TRUST.md`.

## Dependencies

- Python on `PATH`
- NumPy
- Qualtran and Cirq
- PyZX for Tier 3 ZX checks

Run a smoke test:

```bash
python scripts/test_verify_seal.py
```
