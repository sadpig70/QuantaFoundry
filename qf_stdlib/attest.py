"""Attestation objects for canonical QF stdlib entries."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from .adapters import adapter_convention, canonical_hash_with_adapter
from .canon import load_canon, lookup


ATTESTATION_SCHEMA = "qf-attestation-v1"


def _attestation_from_entry(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": ATTESTATION_SCHEMA,
        "subject": {
            "kind": entry["kind"],
            "id": entry["id"],
            "key": entry["key"],
            "u_hash": entry["u_hash"],
        },
        "claim": {
            "semantic_guarantee": entry["semantic_guarantee"],
            "tier": entry["tier"],
            "resource": entry["resource"],
        },
        "anchor": {
            "registry_root": entry["registry_root"],
            "registry_path": entry["registry_path"],
            "semantic_path": "registry/SEMANTIC-GUARANTEES.json",
        },
        "proof": {
            "dependencies": entry.get("dependencies", []),
            "selection": entry.get("selection", {}),
            "sig": entry.get("sig"),
        },
        "limits": [
            entry.get("honesty_scope", ""),
            "Attestation is exact lookup against CANON.json and registry u_hash, not a new oracle run.",
            "No hardware execution claim is implied.",
        ],
    }


def attest(query: str, canon: dict[str, Any] | None = None, root: Path | None = None) -> dict[str, Any] | None:
    data = canon or load_canon(root)
    entry = lookup(query, canon=data, root=root)
    if entry is None:
        return None
    return _attestation_from_entry(entry)


def attest_circuit(
    circuit: object,
    adapter: str,
    *,
    qubit_order: Iterable[object] | None = None,
    canon: dict[str, Any] | None = None,
    root: Path | None = None,
) -> dict[str, Any] | None:
    data = canon or load_canon(root)
    circuit_hash = canonical_hash_with_adapter(circuit, adapter, qubit_order=qubit_order)
    entry = lookup(circuit_hash, canon=data, root=root)
    if entry is None:
        return None
    proof = _attestation_from_entry(entry)
    proof["proof"]["adapter"] = {
        "computed_u_hash": circuit_hash,
        "convention": adapter_convention(adapter),
    }
    proof["limits"].append(
        "Circuit attestation only states that the adapter-computed u_hash is already in CANON.json."
    )
    return proof
