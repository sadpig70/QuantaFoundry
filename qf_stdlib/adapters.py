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


def adapter_convention(adapter: str) -> dict[str, Any]:
    if adapter.lower() == "cirq":
        return dict(CIRQ_CONVENTION)
    raise UnsupportedAdapter(
        f"adapter '{adapter}' is not enabled; supported adapters: cirq"
    )


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


def canonical_hash_with_adapter(
    circuit: object,
    adapter: str,
    *,
    qubit_order: Iterable[object] | None = None,
) -> str:
    if adapter.lower() == "cirq":
        return _canonical_cirq_hash(circuit, qubit_order)
    raise UnsupportedAdapter(
        f"adapter '{adapter}' is not enabled; use exact key/id/u_hash lookup or the convention-pinned cirq adapter"
    )
