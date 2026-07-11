# Invariants — the three INV namespaces

> **Purpose** (QF-0711 U14): the codebase uses the `INV` prefix in three different scopes. The same
> label (e.g. `INV3`) means different things in different files. This index disambiguates them by
> namespace so a reviewer never conflates them. (agent08 F8.)

## `INV-REG-*` — registry composition (qpgf-oracle)

Defined in `.agents/skills/qpgf-oracle/SKILL.md`. The seal/compose contract of the oracle.

| Label | Meaning |
|---|---|
| `INV-REG1` (oracle INV1) | register = verify: a module enters the registry only if the oracle seals it |
| `INV-REG2` (oracle INV2) | sealed-only compose: applications may only compose already-sealed modules |
| `INV-REG3` (oracle INV3) | re-verify: every composition is re-verified, not trusted transitively |

## `INV-LOOP-*` — autonomous loop trust (qfa-loop)

Defined in `.agents/skills/qfa-loop/SKILL.md`. The trust basis of unattended sealing.

| Label | Meaning |
|---|---|
| `INV-LOOP1/2` | fingerprint 2 files (`verify_seal.py`·`contracts.py`) + frozen consensus keys are **READ-ONLY**; guard_check re-hashes byte-identical every round (violation = fatal stop) |
| `INV-LOOP3` | no self-judge: pass/fail is the machine gate only, never the AI's opinion |
| `INV-LOOP5` | verified-only commit: only `--gates full` or `changed` commit/push (both re-synthesize byte-identically) |
| `INV-LOOP6` | runaway guard: bootstrap refuses to start without stop conditions (`dry_limit>0 ∧ budget>0`) |
| `INV-F1` | factory regression: the parametric factory must reproduce every already-sealed N byte-identically before sealing a new one |

## `INV-R*` — rigor / honesty (spec + docs)

Defined in `docs/QuantaFoundry-Technical-Spec.md` and the reproduce runner. The honesty discipline.

| Label | Meaning |
|---|---|
| `INV-R1` | `REPRODUCED` = deterministic byte-identical reproduction, **not** a correctness proof |
| `INV-R5` | structural / subspace / column / compositional grades ≠ dense whole-unitary (per-app boundary; residue tracked) |
| `INV-R7` | (see spec) honesty-scoping of claims |
| `INV-RA1..7` | reproduce-runner invariants (command compat, report byte-identity, sequential-or-order-preserving, manifest-driven, oracle untouched, legacy escape) |

## The collision, made explicit

`INV3` alone is ambiguous: in the **oracle** namespace it means "every composition is re-verified";
in the **loop** namespace it means "no self-judge (machine gate only)". Always qualify: `INV-REG3`
vs `INV-LOOP3`. When a file writes bare `INV3`, read it in that file's namespace (oracle SKILL →
`INV-REG`, qfa-loop SKILL → `INV-LOOP`, spec/docs → `INV-R`).
