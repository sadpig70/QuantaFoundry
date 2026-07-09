# QF-STDLIB

QF-STDLIB is a user-facing import and attestation layer over the sealed QuantaFoundry registry.

Status: v1.0 complete. Release gate: `check-root`, `validate-canon`, `unittest`, `py_compile`, `second_oracle`,
`contested_guard`, and `reproduce_all --changed-only` pass at registry root `d177ce9a438a1b2f6a9f9f042e69f5263267148fb3f90930fe611e8ec0a48af7`.

It does not create new quantum seals. It lets downstream users name canonical primitives, look them up by key/alias/id/hash, and receive a root-anchored attestation for the exact sealed artifact.

## What It Adds

- `registry/CANON.json`: canonical names for selected sealed primitives.
- `qf_stdlib.lookup()`: exact lookup by canonical key, alias, registry id, or `u_hash`.
- `qf_stdlib.list_categories()`, `filter_canon_entries()`, `summarize_canon()`: deterministic Canon discovery helpers.
- `qf_stdlib.attest()`: proof object anchored to `registry_root_hash`.
- `qf_stdlib.attest_circuit()`: adapter-computed circuit hash lookup that returns an attestation only on Canon match.
- `qf_stdlib.check_root()`: fast drift guard between Canon and the live registry manifest root.
- `qf_stdlib.canonical_hash_with_adapter()`: convention-pinned circuit hash adapters, currently Cirq and PennyLane.
- `qf_stdlib.templates`: proof-carrying recipes that compose canonical attestations without pretending to create a new seal.

The current Canon contains 55 entries across base gates, QFT/iQFT, adders, Grover, QPE, Trotter/Suzuki,
block-encoding, QSP/QSVT, qROM, SELECT-PREPARE, RM15 code substrates, and Shor-237 modular multiplier components.
The template library contains `qft_import`, `qpe_skeleton`, `trotter_stack`, `base_gate_bundle`, `qpe_minimal`,
`qsvt_consumer`, and `shor_modexp_attest`.
Importing `qf_stdlib` itself does not import Cirq or PennyLane; optional framework imports happen only inside
adapter calls. Adapter enable/defer rationale is tracked in [`QF-STDLIB-ADAPTER-DECISIONS.md`](QF-STDLIB-ADAPTER-DECISIONS.md).

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
python scripts/qf_stdlib.py adapter-info pennylane
python scripts/qf_stdlib.py adapter-decision qiskit
python scripts/qf_stdlib.py validate-template qpe_skeleton
python scripts/qf_stdlib.py build-template qpe_skeleton
python scripts/qf_stdlib.py build-template base_gate_bundle
python scripts/qf_stdlib.py build-template qsvt_consumer
python scripts/qf_stdlib.py build-template shor_modexp_attest
python scripts/qf_stdlib.py --help
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
gate_bundle = build_with_proof("base_gate_bundle")
qsvt = build_with_proof("qsvt_consumer")
shor = build_with_proof("shor_modexp_attest")
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
python scripts/qf_stdlib.py build-template base_gate_bundle
python scripts/qf_stdlib.py build-template qpe_minimal
python scripts/qf_stdlib.py build-template qsvt_consumer
python scripts/qf_stdlib.py build-template shor_modexp_attest
```

These certificates aggregate existing Canon attestations. They are not new registry seals. `shor_modexp_attest`
intentionally preserves the `subspace_permutation_verified` scope of `shor/237/structural`; it does not upgrade
the frontier to dense unitary equivalence or claim hardware execution.

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

Convention-pinned PennyLane hash:

```python
import pennylane as qml

from qf_stdlib import canonical_hash_with_adapter, lookup

circuit = qml.tape.QuantumScript([qml.CNOT(wires=[0, 1])])
circuit_hash = canonical_hash_with_adapter(circuit, "pennylane", qubit_order=[0, 1])

assert circuit_hash == lookup("gate/cnot")["u_hash"]
```

The PennyLane adapter uses `qml.matrix(obj, wire_order=<explicit order>)`, rejects measurements, and normalizes global
phase through the same QPGF `hash_unitary` path. Qiskit is recorded as deferred until a local install and equivalent
positive/negative convention evidence exist. See [`QF-STDLIB-ADAPTER-DECISIONS.md`](QF-STDLIB-ADAPTER-DECISIONS.md).

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
