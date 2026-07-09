# QF-STDLIB

QF-STDLIB is a user-facing import and attestation layer over the sealed QuantaFoundry registry.

It does not create new quantum seals. It lets downstream users name canonical primitives, look them up by key/alias/id/hash, and receive a root-anchored attestation for the exact sealed artifact.

## What It Adds

- `registry/CANON.json`: canonical names for selected sealed primitives.
- `qf_stdlib.lookup()`: exact lookup by canonical key, alias, registry id, or `u_hash`.
- `qf_stdlib.list_categories()`, `filter_canon_entries()`, `summarize_canon()`: deterministic Canon discovery helpers.
- `qf_stdlib.attest()`: proof object anchored to `registry_root_hash`.
- `qf_stdlib.attest_circuit()`: adapter-computed circuit hash lookup that returns an attestation only on Canon match.
- `qf_stdlib.check_root()`: fast drift guard between Canon and the live registry manifest root.
- `qf_stdlib.canonical_hash_with_adapter()`: convention-pinned circuit hash adapters, currently Cirq only.
- `qf_stdlib.templates`: proof-carrying recipes that compose canonical attestations without pretending to create a new seal.

The current Canon contains 55 entries across base gates, QFT/iQFT, adders, Grover, QPE, Trotter/Suzuki,
block-encoding, QSP/QSVT, qROM, SELECT-PREPARE, RM15 code substrates, and Shor-237 modular multiplier components.

## What It Does Not Claim

- It does not certify arbitrary circuits.
- It does not rerun the QPGF oracle.
- It does not convert observations into seals.
- It does not upgrade `structural_wellformed` or `subspace_permutation_verified` to dense `unitary_equiv`.
- It does not imply hardware execution.

## CLI

```bash
python scripts/qf_stdlib.py validate-canon
python scripts/qf_stdlib.py check-root
python scripts/qf_stdlib.py categories
python scripts/qf_stdlib.py list
python scripts/qf_stdlib.py list --category gate
python scripts/qf_stdlib.py summary
python scripts/qf_stdlib.py lookup qft/8
python scripts/qf_stdlib.py attest qft/8
python scripts/qf_stdlib.py adapter-info cirq
python scripts/qf_stdlib.py validate-template qpe_skeleton
python scripts/qf_stdlib.py build-template qpe_skeleton
```

`build-canon` is the only command that writes `registry/CANON.json`:

```bash
python scripts/qf_stdlib.py build-canon --write-report
```

## Python API

```python
from qf_stdlib import (
    attest,
    attest_circuit,
    build_with_proof,
    canonical_hash_with_adapter,
    filter_canon_entries,
    list_categories,
    load_canon,
    lookup,
    summarize_canon,
)

categories = list_categories(load_canon())
gates = filter_canon_entries(load_canon(), "gate")
entry = lookup("qft/8")
proof = attest("qft/8")
cert = build_with_proof("qpe_skeleton")
summary = summarize_canon(load_canon())
```

Unknown primitives return `None`; they are not approximated or guessed.

## Examples

Root drift guard before using the stdlib:

```bash
python scripts/qf_stdlib.py check-root
python scripts/qf_stdlib.py list
python scripts/qf_stdlib.py categories
python scripts/qf_stdlib.py list --category qsvt
python scripts/qf_stdlib.py summary
```

Exact Fourier lookup and attestation:

```bash
python scripts/qf_stdlib.py lookup qft/7
python scripts/qf_stdlib.py attest fourier/qft/7
python scripts/qf_stdlib.py attest gate/cnot
```

Proof-carrying recipe certificate:

```bash
python scripts/qf_stdlib.py build-template qpe_skeleton
python scripts/qf_stdlib.py build-template trotter_stack
```

These certificates aggregate existing Canon attestations. They are not new registry seals.

Convention-pinned Cirq hash:

```python
import cirq

from qf_stdlib import canonical_hash_with_adapter, lookup

qubits = cirq.LineQubit.range(3)
circuit = cirq.Circuit(cirq.qft(*qubits, without_reverse=False))
circuit_hash = canonical_hash_with_adapter(circuit, "cirq", qubit_order=qubits)

assert circuit_hash == lookup("qft/3")["u_hash"]
```

Root-anchored circuit attestation:

```python
proof = attest_circuit(circuit, "cirq", qubit_order=qubits)
assert proof["subject"]["key"] == "qft/3"
assert proof["proof"]["adapter"]["computed_u_hash"] == proof["subject"]["u_hash"]
```

The Cirq adapter requires explicit `qubit_order`. `without_reverse=True`, omitted qubit order, measurements, and
unsupported frameworks fail closed instead of being normalized silently. CLI `attest --adapter cirq` is intentionally
rejected because arbitrary circuit objects must enter through the Python API.

## Honesty Boundary

An attestation means:

```text
The target exactly matches a canonical registry entry, and that entry is anchored by the current registry root.
```

It does not mean:

```text
This arbitrary user circuit is correct.
This circuit ran on hardware.
This derived template is a new sealed registry artifact.
```

For `attest_circuit()`, a returned proof means only that the adapter-computed `u_hash` exactly matches an existing
Canon entry. Unknown circuit hashes return `None`; they are not approximate-matched or promoted.

For structural Shor entries, QF-STDLIB preserves the existing scope: the modexp core may be `subspace_permutation_verified`, while full dense unitary equivalence including H and iQFT remains unclaimed.
