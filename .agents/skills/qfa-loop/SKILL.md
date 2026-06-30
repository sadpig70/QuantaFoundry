---
name: qfa-loop
description: "QuantaFoundry Autonomous Loop (QFA-Loop): single-runtime autonomous seal loop that drives discover→seal→verify→commit with deterministic gates and tamper-evident invariants. Provides the real-gate runner (autonomy_loop.py), the parametric frontier factory wiring, and the PG design/persona specs. Triggers: autonomy loop, 자율 루프, QFA-loop, frontier factory, autonomous seal round."
disable-model-invocation: true
---

# qfa-loop — QuantaFoundry Autonomous Loop

A single-runtime (Claude-only) autonomous loop that expands the QuantaFoundry sealed library
by **discover → seal → verify → commit**, where the trust comes not from the agent's judgement
but from **deterministic gates + tamper-evident invariants**.

> ⚠ `disable-model-invocation: true` — this skill **seals, commits, and pushes**. It is invoked
> deliberately (user/operator), never auto-triggered. Loading this SKILL.md is safe (docs only);
> running `autonomy_loop.py` performs real work.

## What it is

The loop's value is **"deterministic gates + explicit stop/invariant guards around a loop"**, not a
clever autonomous agent. The runtime (Claude) is the executor; this bundle supplies the harness.

```
Bootstrap → Round(SelectNext → PlanNode → Implement → VerifyGate → GuardCheck → Record → SyncCheckpoint)
          → StopController → Finalize
```

## Layout

```
.agents/skills/qfa-loop/
    SKILL.md                          # this entry point
    scripts/autonomy_loop.py          # real-gate runner (engine)
    references/
        DESIGN-AutonomyLoop.md        # PG Gantree+PPR + §8 elaboration (4 decomposed)
        DESIGN-FrontierFactory.md     # parametric frontier factory closed-loop design
        persona_contexts.md           # 8-persona diversity spec (PersonaRank)
    tests/
        sim_autonomy_loop_v2.py       # T1~T12 control-flow simulation (deterministic mock)
        sim_persona_diversity.py      # D1~D5
        sim_seal_cycle.py             # SealCycle / MachineGate elaboration
        sim_autonomy_loop.py          # v1
```

The **engine is here (tracked, immutable)**; the **mutable runtime state lives in `_workspace/loop/`**
(`rounds/round-NN.json`, `loop_state.json` — gitignored). The factory's sealing infrastructure is
`scripts/frontier_factory.py` (tracked, repo-level) and is **not** part of this skill — the loop calls
it as a subprocess driver.

## Modes

```bash
# infra (MVP): exercises the real gate chain on current state, no new seal
python .agents/skills/qfa-loop/scripts/autonomy_loop.py --mode infra --budget 1 --gates fast

# frontier-factory: autonomous closed loop — discover an unsealed distinct-semiprime N,
#   seal cmul payoff (Tier-0 exact) + structural shor{N} (Tier-1), verify, commit
python .agents/skills/qfa-loop/scripts/autonomy_loop.py --mode frontier-factory --gates full --commit --push
```

| `--gates` | meaning |
|---|---|
| `full` | reproduce_all re-synthesis (REPRODUCED) — **only mode allowed to commit** (verified-only) |
| `incremental` | registry build + second_oracle + seal_gate_ci + contested_guard (~46s) — commit withheld |
| `fast` | independent gates only, no registry build — inspection |

## Invariants (trust basis, not prohibitions)

```python
# INV1/2  fingerprint 2 files (verify_seal.py·contracts.py) + frozen consensus_keys are READ-ONLY.
#         guard_check re-hashes them byte-identical every round; violation = fatal stop.
# INV3    no self-judge: pass/fail is the machine gate (reproduce_all/second_oracle/seal_gate_ci/
#         contested_guard) only — never the AI's opinion.
# INV5    verified-only commit: only --gates full (reproduce_all REPRODUCED) commits/pushes.
# INV6    runaway guard: bootstrap refuses to start without stop conditions (dry_limit>0 ∧ budget>0).
# INV-F1  factory regression: scripts/frontier_factory.py must reproduce already-sealed N
#         byte-identically before sealing any new N (codegen-safety proof).
```

## Workflow

```text
1. invoke deliberately (this skill is not auto-triggered)
2. python scripts/autonomy_loop.py --mode <infra|frontier-factory> --gates <full|incremental|fast>
3. exit 0 + invariants_held=True + REPRODUCED  <=>  round verified
   commit/push happens only on --gates full --commit (verified-only)
4. runtime artefacts land in _workspace/loop/rounds/ and loop_state.json
```

## Honesty boundaries (inherited)

- single-runtime → **intra-runtime diversity only** (not true cross-runtime independence; H1).
- cmul = Tier-0 EXACT permutation; structural shor{N} = Tier-1 Merkle (no dense whole-unitary claim);
  period/factor readout = illustrative, not seal evidence.
- seal ≠ run ≠ verify; approximation ≠ exact; structural ≠ dense.

## Dependencies

- Python on PATH, NumPy, Qualtran/Cirq (for the repo's seal path; the loop calls repo scripts).
- Runs from the QuantaFoundry repo root (the engine resolves `ROOT` four levels up from `scripts/`).

## Tests

```bash
python .agents/skills/qfa-loop/tests/sim_autonomy_loop_v2.py   # T1~T12 ALL PASS (control flow)
python .agents/skills/qfa-loop/tests/sim_seal_cycle.py         # SealCycle/MachineGate
python .agents/skills/qfa-loop/tests/sim_persona_diversity.py  # D1~D5
```
