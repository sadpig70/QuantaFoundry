"""QF stdlib: canonical lookup and proof-carrying attestations over QuantaFoundry."""

from .attest import attest
from .adapters import adapter_convention, canonical_hash_with_adapter
from .canon import build_canon, check_root, load_canon, lookup, validate_canon
from .templates import build_with_proof, load_template, validate_template

__all__ = [
    "attest",
    "adapter_convention",
    "build_canon",
    "build_with_proof",
    "check_root",
    "canonical_hash_with_adapter",
    "load_canon",
    "load_template",
    "lookup",
    "validate_canon",
    "validate_template",
]
