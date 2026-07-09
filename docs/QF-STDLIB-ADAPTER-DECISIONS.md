# QF-STDLIB Adapter Decisions

This record is part of the QF-STDLIB honesty boundary. Adapters are enabled only when the unitary extraction convention is pinned with positive and negative tests.

## Enabled

### Cirq

- Convention: `Circuit.unitary(qubit_order=<explicit order>)`
- Status: enabled
- Evidence: QFT and base gate Canon hash tests, explicit `qubit_order` requirement, measurement rejection, endian/global-phase negative tests.

### PennyLane

- Convention: `qml.matrix(obj, wire_order=<explicit order>)`
- Status: enabled
- Evidence: base gate Canon hash tests for X, H, S, T, CNOT, CZ, SWAP, Toffoli, and Fredkin; explicit wire-order requirement; reversed wire-order mismatch; measurement rejection.
- Boundary: the adapter returns an attestation only when the computed QPGF `u_hash` already exists in Canon.

## Deferred

### Qiskit

- Status: deferred
- Reason: Qiskit is not installed in the current workspace, so no local convention-pinned positive/negative evidence was generated.
- Required before enablement:
  - exact unitary extraction API pinned
  - explicit qubit order pinned
  - global phase normalized through QPGF `hash_unitary`
  - positive Canon hash tests
  - negative ordering/non-unitary tests

