"""Attestation objects for canonical QF stdlib entries."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .canon import load_canon, lookup


ATTESTATION_SCHEMA = "qf-attestation-v1"


def attest(query: str, canon: dict[str, Any] | None = None, root: Path | None = None) -> dict[str, Any] | None:
    data = canon or load_canon(root)
    entry = lookup(query, canon=data, root=root)
    if entry is None:
        return None
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

