# Honesty boundaries — one page

> **Purpose** (QF-0711 U14): the project's core discipline is stating what the evidence does *not*
> prove. These boundaries are asserted inline throughout the codebase; this page collects them in one
> view — each with what it means, a concrete violation scenario, and how to check it. (agent06 §11.)

| Boundary | Means | Violation scenario (what it would look like) | Verify |
|---|---|---|---|
| `REPRODUCED ≠ correct` | byte-identical reproduction proves *determinism*, not that the math is right | claiming "REPRODUCED, therefore Shor is correct" | correctness comes from rows below: `second_oracle`, column/subspace/ring/cuc, contracts |
| `seal ≠ run ≠ verify` | a seal is a certificate the unitary matches a golden; running the circuit and re-verifying it are distinct acts | presenting a *run* (e.g. a measured peak) as if it were the *seal* | `python -m qf_verify check-claims`; each claim names its evidence step |
| `approximation ≠ exact` | ε-certified Trotter/Suzuki circuits carry an **upper bound** on distance to `e^{-iHt}`, not zero error | quoting an ε app as an exact seal | `registry/APPROX-GUARANTEES.json` (ε is a bound, no tightness claim) |
| `structural ≠ dense` | a Merkle/structural seal proves well-formed composition, not the whole 2ⁿ unitary | claiming a 20-qubit structural Shor app is dense-verified | `registry/SEMANTIC-GUARANTEES.json` grade; `structural_wellformed` |
| `subspace / column / compositional ≠ dense` | each is a distinct, weaker-than-dense evidence grade on a fragment | conflating `subspace_permutation_verified` with full `unitary_equiv` | `SEMANTIC-GUARANTEES.json` `guarantee_classes` catalogue |
| `observation ≠ seal` | exact math witnesses (topology, contextuality, MTC, knots, dynamics) are recorded, not sealed | listing an observation among the sealed apps | `.pgf/proofs/*-OBSERVE.json`; not counted in the seal registry |
| `float-atol ≠ ring-exact` | `column_exact` is a float-atol grade (Tier-0 dense class), not integer-exact | claiming column verification is ring-exact | `RING-COLUMN.json` supplies the ℤ[ζ₂₅₆] float-0 companion where it applies |
| `cached leaf re-seal ≠ new unique app` | 75 app-side module re-seals are not distinct applications | counting 577 app-files as 577 unique apps | `registry/COUNT-ONTOLOGY.json` glossary (unique 502 vs files 577) |

## Reading the ladder

```text
observation → REPRODUCED → structural → subspace → compositional → column_exact → dense/tableau (unitary_equiv)
(math witness) (byte-match)  (Merkle)    (basis)     (composed n≥19)  (full cols,float) (full unitary, exact)
```

A stronger grade is never *inferred* from a missing tag: a seal with no explicit weaker-tier contract
is the recognized dense `C1-C4` contract (sound, not a guess); a genuinely unknown/empty contract is
**`unclassified`** and excluded from the headline (fail-closed). See `SEMANTIC-GUARANTEES.json`.

Related: [`docs/EVIDENCE-MAP.md`](EVIDENCE-MAP.md) (claim→command→boundary),
[`docs/VERIFICATION-PATHS.md`](VERIFICATION-PATHS.md) (the independent paths),
[`docs/INVARIANTS.md`](INVARIANTS.md) (the INV namespaces).
