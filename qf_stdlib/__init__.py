"""QF stdlib: canonical lookup and proof-carrying attestations over QuantaFoundry."""

from .attest import attest, attest_circuit
from .adapters import adapter_convention, canonical_hash_with_adapter
from .canon import (
    build_canon,
    check_root,
    filter_canon_entries,
    list_categories,
    load_canon,
    lookup,
    summarize_canon,
    validate_canon,
)
from .templates import build_with_proof, load_template, validate_template

__all__ = [
    "attest",
    "attest_circuit",
    "adapter_convention",
    "build_canon",
    "build_with_proof",
    "check_root",
    "canonical_hash_with_adapter",
    "filter_canon_entries",
    "list_categories",
    "load_canon",
    "load_template",
    "lookup",
    "summarize_canon",
    "validate_canon",
    "validate_template",
]
