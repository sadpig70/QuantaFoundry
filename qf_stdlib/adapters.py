"""Optional circuit-framework adapters.

Lookup-only QF stdlib use does not import heavy quantum frameworks. Adapter imports
are lazy and fail closed unless the framework convention is pinned.
"""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Any, Iterable

import numpy as np

from .errors import AdapterConventionError, UnsupportedAdapter


CIRQ_CONVENTION: dict[str, Any] = {
    "adapter": "cirq",
    "version": "cirq-circuit-unitary-v1",
    "basis_order": "Circuit.unitary(qubit_order=<explicit order>)",
    "qubit_order_required": True,
    "qid_dimension": 2,
    "global_phase": "normalized by QPGF hash_unitary",
    "measurements": "rejected",
    "qf_reference": "LineQubit.range(n) with cirq.qft(..., without_reverse=False) matches qft/n Canon entries",
}

PENNYLANE_CONVENTION: dict[str, Any] = {
    "adapter": "pennylane",
    "version": "pennylane-qml-matrix-v1",
    "basis_order": "qml.matrix(obj, wire_order=<explicit order>)",
    "wire_order_required": True,
    "qid_dimension": 2,
    "global_phase": "normalized by QPGF hash_unitary",
    "measurements": "rejected",
    "qf_reference": "qml.tape.QuantumScript over base gates matches gate/* Canon entries when wire_order is explicit",
}

DEFERRED_ADAPTERS: dict[str, dict[str, Any]] = {
    "qiskit": {
        "adapter": "qiskit",
        "status": "deferred",
        "reason": "qiskit is not installed in the current workspace; no convention-pinned positive/negative evidence was generated",
        "required_before_enable": [
            "exact unitary extraction API pinned",
            "explicit qubit order pinned",
            "global phase normalized through QPGF hash_unitary",
            "positive Canon hash tests",
            "negative ordering/non-unitary tests",
        ],
    }
}


def adapter_convention(adapter: str) -> dict[str, Any]:
    name = adapter.lower()
    if name == "cirq":
        return dict(CIRQ_CONVENTION)
    if name == "pennylane":
        return dict(PENNYLANE_CONVENTION)
    if name in DEFERRED_ADAPTERS:
        decision = DEFERRED_ADAPTERS[name]
        raise UnsupportedAdapter(
            f"adapter '{adapter}' is deferred: {decision['reason']}"
        )
    raise UnsupportedAdapter(
        f"adapter '{adapter}' is not enabled; supported adapters: cirq, pennylane"
    )


def adapter_decision(adapter: str) -> dict[str, Any]:
    name = adapter.lower()
    if name == "cirq":
        return {"adapter": "cirq", "status": "enabled", "convention": adapter_convention("cirq")}
    if name == "pennylane":
        return {"adapter": "pennylane", "status": "enabled", "convention": adapter_convention("pennylane")}
    if name in DEFERRED_ADAPTERS:
        return dict(DEFERRED_ADAPTERS[name])
    raise UnsupportedAdapter(f"adapter '{adapter}' is not enabled and has no recorded decision")


def _hash_unitary(unitary: np.ndarray) -> str:
    root = Path(__file__).resolve().parents[1]
    oracle_scripts = root / ".agents" / "skills" / "qpgf-oracle" / "scripts"
    if str(oracle_scripts) not in sys.path:
        sys.path.insert(0, str(oracle_scripts))
    import verify_seal as vs  # noqa: PLC0415

    return vs.hash_unitary(np.asarray(unitary, dtype=complex))


def _canonical_cirq_hash(circuit: object, qubit_order: Iterable[object] | None) -> str:
    try:
        import cirq  # noqa: F401, PLC0415
    except Exception as exc:  # pragma: no cover - depends on optional environment
        raise UnsupportedAdapter(f"cirq adapter requested but cirq import failed: {exc}") from exc

    if qubit_order is None:
        raise AdapterConventionError("cirq adapter requires explicit qubit_order")
    order = list(qubit_order)
    if not order:
        raise AdapterConventionError("cirq adapter requires at least one qubit in qubit_order")
    if len(set(order)) != len(order):
        raise AdapterConventionError("cirq adapter qubit_order contains duplicate qids")
    bad_dims = [q for q in order if getattr(q, "dimension", 2) != 2]
    if bad_dims:
        raise AdapterConventionError(f"cirq adapter supports only qubits, got non-2D qids: {bad_dims!r}")
    if not hasattr(circuit, "unitary") or not hasattr(circuit, "all_qubits"):
        raise AdapterConventionError("cirq adapter expects a cirq.Circuit-like object")
    missing = set(circuit.all_qubits()) - set(order)
    if missing:
        raise AdapterConventionError(f"cirq adapter qubit_order is missing circuit qids: {sorted(map(str, missing))}")
    try:
        unitary = circuit.unitary(
            qubit_order=order,
            qubits_that_should_be_present=order,
            ignore_terminal_measurements=False,
            dtype=np.complex128,
        )
    except Exception as exc:
        raise AdapterConventionError(f"cirq circuit is not an exact unitary under the pinned convention: {exc}") from exc
    dim = 1 << len(order)
    if unitary.shape != (dim, dim):
        raise AdapterConventionError(f"cirq unitary shape mismatch: got {unitary.shape}, expected {(dim, dim)}")
    return _hash_unitary(unitary)


def _canonical_pennylane_hash(circuit: object, wire_order: Iterable[object] | None) -> str:
    try:
        import pennylane as qml  # noqa: PLC0415
    except Exception as exc:  # pragma: no cover - depends on optional environment
        raise UnsupportedAdapter(f"pennylane adapter requested but pennylane import failed: {exc}") from exc

    if wire_order is None:
        raise AdapterConventionError("pennylane adapter requires explicit wire_order via qubit_order")
    order = list(wire_order)
    if not order:
        raise AdapterConventionError("pennylane adapter requires at least one wire in wire_order")
    if len(set(order)) != len(order):
        raise AdapterConventionError("pennylane adapter wire_order contains duplicate wires")
    if hasattr(circuit, "measurements") and getattr(circuit, "measurements"):
        raise AdapterConventionError("pennylane adapter rejects measurements")
    if hasattr(circuit, "wires"):
        missing = set(circuit.wires) - set(order)
        if missing:
            raise AdapterConventionError(f"pennylane adapter wire_order is missing circuit wires: {sorted(map(str, missing))}")
    try:
        unitary = qml.matrix(circuit, wire_order=order)
    except Exception as exc:
        raise AdapterConventionError(f"pennylane object is not an exact unitary under the pinned convention: {exc}") from exc
    dim = 1 << len(order)
    if unitary.shape != (dim, dim):
        raise AdapterConventionError(f"pennylane unitary shape mismatch: got {unitary.shape}, expected {(dim, dim)}")
    return _hash_unitary(unitary)


def canonical_hash_with_adapter(
    circuit: object,
    adapter: str,
    *,
    qubit_order: Iterable[object] | None = None,
) -> str:
    name = adapter.lower()
    if name == "cirq":
        return _canonical_cirq_hash(circuit, qubit_order)
    if name == "pennylane":
        return _canonical_pennylane_hash(circuit, qubit_order)
    if name in DEFERRED_ADAPTERS:
        decision = DEFERRED_ADAPTERS[name]
        raise UnsupportedAdapter(
            f"adapter '{adapter}' is deferred: {decision['reason']}"
        )
    raise UnsupportedAdapter(
        f"adapter '{adapter}' is not enabled; use exact key/id/u_hash lookup or a convention-pinned adapter"
    )
