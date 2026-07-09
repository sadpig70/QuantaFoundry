"""Optional circuit-framework adapters.

Lookup-only QF stdlib use does not import heavy quantum frameworks. Exact circuit hash
adapters are intentionally deferred until each framework convention is pinned.
"""

from .errors import UnsupportedAdapter


def canonical_hash_with_adapter(_circuit: object, adapter: str) -> str:
    raise UnsupportedAdapter(
        f"adapter '{adapter}' is not enabled; use exact key/id/u_hash lookup or add a convention-pinned adapter"
    )

