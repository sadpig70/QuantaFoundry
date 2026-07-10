# Evidence Map — which claim is backed by which executable check

> **Purpose**: an external reviewer should be able to pick any claim the project makes,
> run one command, and see the evidence — without reading the codebase.
> Every claim comes with its **honest boundary** (what the evidence does *not* prove).
>
> *Status: manually maintained v0 (2026-07-10). A machine-generated successor
> (`reports/CLAIM-EVIDENCE-MAP.md`, driven by a manifest runner) is planned — see
> `_workspace/reproduce_all_upgrade_plan.md` Phase 4.*

| # | Claim | Command | Expected | Artifact / authority | Honest boundary |
|---|---|---|---|---|---|
| 1 | The whole registry (95 modules / 484 apps) reproduces byte-identically | `python scripts/reproduce_all.py` | `REPRODUCED`, root `cf7a8ca801c7f4c9…` | `reports/REPRODUCE-RESULT.json`, `registry/REGISTRY-MANIFEST.json` | **Determinism, not correctness** (INV-R1). Correctness comes from rows 2–8. |
| 2 | Every sealed module passes an independent dense oracle | `python scripts/second_oracle.py` | `83/83` + app pass | script output | Independent *implementation*, shared conventions (endian/phase/atol) — see convention audit (row 3). |
| 3 | Verification does not hinge on one convention choice | `python scripts/inverted_second_oracle.py --quick` | `all_ok=True` | script output | Audits the shared-assumption gap; does not eliminate it. |
| 4 | Frozen consensus keys & oracle fingerprints are intact | `python scripts/verify_contested_guard.py` + `sha256sum` of the two oracle files | `ALL PASS · pass=20 fail=0`; hashes in `HANDOFF.md` | `consensus_keys.json`, oracle skill files | Tamper-*evidence* (SHA-256), not cryptographic non-forgeability. |
| 5 | Structural Shor apps compute the right modular arithmetic | `python scripts/perm_subspace_verify.py` | exhaustive basis match per app | `.pgf/proofs/*.subspace_proof.json` | Modexp core only; computational-basis permutation, not the full unitary. |
| 6 | 28 Shor apps (n≤18) match the Shor spectral formula on **every column of the full unitary** (H·iQFT included) | `python scripts/column_verify.py` | `ALL VERIFIED`, max_dev ≤ 1e-12 | `.pgf/proofs/*.column_proof.json`, `registry/SEMANTIC-GUARANTEES.json` (`unitary_equiv_column_exact`) | **float-atol grade** (same evidence class as Tier-0 dense C4) — *not* ring-exact. n≥19 apps stay subspace-grade. |
| 7 | Sealed Trotter/Suzuki circuits carry certified error **upper bounds** vs their target `e^{-iHt}` | `python scripts/approx_certify.py` | `ALL CERTIFIED` (9 apps; heis2 ε=0) | `registry/APPROX-GUARANTEES.json` | ε is an **upper bound** (no tightness claim); unitary channels only; the seals themselves are unchanged. |
| 8 | Tier/guarantee labels match what was actually proven | `python scripts/semantic_guarantee.py` | headline split regenerated identically | `registry/SEMANTIC-GUARANTEES.json` | A labeling layer — it cannot make a weak check strong; it prevents overclaim. |
| 9 | Sealed circuits survive OpenQASM3 export → re-import | `python scripts/qasm_export.py` / `qasm_ingest.py` (see scripts) | round-trip unitary identity | round-trip reports | Format fidelity, not new verification. |
| 10 | The user-facing stdlib is anchored to the sealed registry root | `python scripts/qf_stdlib.py check-root && python scripts/qf_stdlib.py validate-canon` | both `ok` | `registry/CANON.json` | Only Canon entries are attested; arbitrary user circuits are not certified. |
| 11 | Ten *independent* verification paths agree on their covered fragments | (each path's script; e.g. `python scripts/anf_verify.py`, `python scripts/groebner_verify.py`) | per-path `all_ok=True` with recorded skips | `.pgf/proofs/` sidecars | Each path covers a fragment (permutation / diagonal-phase / Clifford / …) — coverage sets are complementary, not universal. |
| 12 | Observation witnesses (topology, contextuality, MTC, knots, …) re-verify deterministically | `python scripts/reproduce_all.py --changed-only` (runs every `*_observe.py --quick`) | `REPRODUCED`, all witnesses `all_ok=True` | `.pgf/proofs/*-OBSERVE.json` | **Observations, not seals** — exact math checks recorded as sidecars; they add no new sealed circuits. |

## Reading the boundaries

The project's trust story is deliberately layered:

```text
REPRODUCED  ≠ correct      (row 1 vs rows 2–8)
seal        ≠ run ≠ verify
approximation ≠ exact       (row 7: bounds, not errors)
structural  ≠ dense         (rows 5–6: subspace / column grades vs Tier-0)
observation ≠ seal          (row 12)
```

If any row's command stops producing its expected output, the corresponding claim —
and only that claim — is no longer supported. That is the intended failure semantics.
