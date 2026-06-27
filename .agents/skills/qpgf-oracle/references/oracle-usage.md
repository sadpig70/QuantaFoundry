# oracle-usage — Using the Oracle as a Runtime Stop Condition

QPGF does not implement the repair loop. The loop is native to the runtime: Codex, Claude Code, or another agent repeatedly generates, runs, reads failure signals, and revises.

This document specifies how that loop uses `qpgf-oracle` as its deterministic stop condition.

## Termination Contract

```text
exit 0  <=>  <id>.sealed.json exists  <=>  verified module accepted
exit 1  <=>  no seal + structured stderr signal  <=>  continue repair loop
```

The loop only needs the exit code and the existence of the seal file.

## Standard Wiring

```bash
# 0) Write a spec.pg file.
#    Required blocks:
#      ```python id=bloq```   -> binds `bloq`
#      ```python id=golden``` -> binds `golden`
#      ```json id=meta```     -> id, n_sys, n_anc

# 1) Preflight guard
python scripts/spec_guard.py spec.pg

# 2) Verification and sealing
python scripts/verify_seal.py spec.pg --out ./sealed
```

Success:

```text
sealed: ./sealed/<id>.sealed.json
exit code 0
```

Failure:

```text
exit code 1
structured JSON on stderr
```

## Structured Failure Signals

| Signal | Meaning | Next Action |
|---|---|---|
| `spec_load_fail` | malformed spec, missing block, bad meta | fix fenced blocks or JSON |
| `instantiate_fail` | `bloq` construction failed | fix imports or construction code |
| `golden_fail` | `golden` construction failed | fix analytical reference code |
| `cost_fail` | resource counting failed | inspect unsupported bloq/resource path |
| `C1` | dimension or characterization mismatch | check `n_sys`, `n_anc`, shape |
| `C2` | non-unitary/non-isometric candidate | fix circuit logic |
| `C3` | ancilla leakage | add or repair uncompute |
| `C3iso` | invalid isometry | fix alloc-style ancilla behavior |
| `C4` | mismatch with `golden` | check endian, gate order, phase, or reference |

The oracle may also include machine-readable `reason_code`, `fix_hint`, or `norm_delta` fields where supported.

## Registry Integration

Registry admission should be based on verification, not trust in arbitrary files.

Recommended policy:

```text
register(spec) -> internally run verify_seal -> admit only local seal
```

For external seals, verify provenance against a trusted local bundle before relying on them.

## Runtime Notes

- **Codex / Claude Code**: run the scripts directly in the terminal and revise the spec until `exit 0`.
- **MCP wrapper**: acceptable as a thin transport layer only. It must call the same scripts and preserve the same seal fields.
- **Human courier workflows**: acceptable for collecting candidate specs, but the central oracle remains the authority.

## Limits

The dense exact path is small-N bounded. For larger modules, use the supported seal tiers where applicable:

- structural app composition;
- Clifford tableau sealing;
- ZX equivalence sealing for Clifford+T reference circuits.

Weak specs can still produce wrong-but-valid behavior if the independent `golden` is wrong. `spec_guard` and `golden_guard` reduce this risk but do not remove the responsibility of writing a correct intent reference.
