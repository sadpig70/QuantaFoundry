# QuantaFoundry — Current Specification (live state)

> **Role**: the single **current-state** page (QF-0711 U5). It carries no version narrative.
> - Version & milestone history → [`docs/CHANGELOG.md`](CHANGELOG.md)
> - Architecture, trust model, components → [`docs/ARCHITECTURE.md`](ARCHITECTURE.md)
> - Full spec + evidence + review questions → [`docs/QuantaFoundry-Technical-Spec.md`](QuantaFoundry-Technical-Spec.md)
> - Count terminology → [`registry/COUNT-ONTOLOGY.json`](../registry/COUNT-ONTOLOGY.json)

## Counts (authoritative source: `registry/REGISTRY-MANIFEST.json`)

<!-- BEGIN generated:counts src=registry/COUNT-ONTOLOGY.json -->
- **95 sealed modules · 1387 unique applications** · registry root `bfea7d3728a9df24…`
  (1462 app-file entries = 1387 unique + 75 cached app-side re-seals;
  live source [`registry/REGISTRY-MANIFEST.json`](../registry/REGISTRY-MANIFEST.json)).
<!-- END generated:counts -->

## Guarantee split

Authoritative: [`registry/SEMANTIC-GUARANTEES.json`](../registry/SEMANTIC-GUARANTEES.json)
`headline_split` + `guarantee_classes` catalogue.

| class | count (app) | boundary |
|---|---|---|
| `unitary_equiv` | 542 | exact (Tier-0 dense / Tier-2 tableau), global phase ignored |
| `unitary_equiv_column_exact` | 30 | full Shor unitary column-by-column (float-atol), n≤18 |
| `compositionally_verified` | 2 | exhaustive modexp + ring-exact iQFT, composed (n≥19: shor1285/3683) |
| `subspace_permutation_verified` | 1 | modexp core basis permutation only (rs73) |
| `unitary_equiv_sampled` | 1 | sampled-dense two-path (ghz16) |
| `structural_wellformed` | 1 | Merkle structure only (rm15_tt) |

All **95 modules** are `unitary_equiv`. ε-certified (Trotter/Suzuki upper bounds, 9 apps) is an
orthogonal axis in [`registry/APPROX-GUARANTEES.json`](../registry/APPROX-GUARANTEES.json).

## Verification surface

- **One command**: `python scripts/reproduce_all.py` → `REPRODUCED` (byte-identical determinism, not correctness).
- **Claim → command → boundary**: [`docs/EVIDENCE-MAP.md`](EVIDENCE-MAP.md).
- **second_oracle** 83/83 · **10 independent verification paths** · **23 frozen consensus keys**.
- Invocation of any check: `python -m qf_witness.<cat>.<name>` (e.g. `qf_witness.verify.second_oracle`).

## Honest boundaries

`REPRODUCED ≠ correct` · `seal ≠ run ≠ verify` · `approximation ≠ exact` ·
`structural / subspace / column / compositional` are distinct evidence grades · `observation ≠ seal` ·
`float-atol ≠ ring-exact` · `cached leaf re-seal (75) ≠ new unique app`.
