<!-- External adversarial review request — for a fresh external AI runtime asked to critique QuantaFoundry
     and propose directions. Distilled from the former EXTERNAL-ONBOARDING.md (2026-07-01).
     Reading order below points to tracked docs only (AGENTS.md/HANDOFF.md are local, not in a clone). -->
# QuantaFoundry — External Review & Direction Request

**Role:** external reviewer of a quantum-verification + autonomous-AI architecture. Be adversarial about
assumptions; prioritize actionable next steps over validation. We do **not** want praise — we want the
sharpest critique of the weakest assumptions and concrete, feasible directions.

## Project scope (this shapes what counts as a valid proposal — read first)

QuantaFoundry is **software prepared *in advance* for a future fault-tolerant quantum computer (QPC)**.
Every artifact seals **ideal, noiseless mathematical truth** (exact unitary, or structural Merkle for
large circuits) via a deterministic oracle. It is **not** meant to run on present-day noisy hardware —
so **QPU backends / noise models / real-hardware execution are permanently deferred and out of scope**.
Do **not** propose "run it on a real QPU" or "add a noise model." The seal is a **permanent contract**:
because there is no post-hoc hardware check, the *seal-time* mathematical verification is the entire
basis of trust — which makes verification *strength* and *independence* unusually load-bearing.

**Already considered — critique or go beyond these, don't re-propose them as if new:**

- **Vertical scale is a wall, not a goal.** Larger dense circuits (e.g. the 14-qubit `c13x` primitive)
  are blocked by the dense-matrix memory ceiling. This is an honest, accepted boundary — *not* a target.
- **Horizontal / abstraction-layer expansion is the intended growth axis** (small *exact* instances, higher
  abstraction, not more qubits). Candidates under weighing: **QSVT/QSP + block-encoding/LCU** (a unifying
  framework where one seal yields many algorithms) · **fermionic simulation** (Jordan-Wigner / Bravyi-Kitaev
  — the FTQC chemistry app) · **FTQC-native logical layers** (surface/color codes, magic-state distillation,
  lattice surgery, logical-level algorithms) · **structural→strong verification** (ZX Tier-3 / partial-subspace
  / symbolic proof, to pay down the "structural is weaker than dense" debt) · **genuine discovery autonomy**
  (AI proposing *unknown* decompositions/primitives, oracle-gated).

## Reading order (tracked files; a clone has these)

`README.md` (identity · trust model · current status · one-command verify) → `.pgf/DESIGN-MasterRoadmap.md`
(execution roadmap spine, PG notation; a node's `(status)` = built vs planned) → `docs/QuantaFoundry-Technical-Spec.md`
(full spec + evidence + **limitations** + version history). Authoritative current numbers/root live in
`registry/REGISTRY-MANIFEST.json`; the tier split in `registry/SEMANTIC-GUARANTEES.json`.

## Your task — answer in priority order

Each answer as `proposal / rationale / feasibility / risk`, citing the file that informs it:

1. Is the core identity (an **AI-terminating oracle** + binary seal, where no AI judges its own output)
   convincing? What is the **single weakest assumption**, and how would you stress it?
2. **Open-ended goal-autonomy:** the loop (`qfa-loop`) now auto-discovers and seals frontier families via a
   regression-gated parametric factory, but still seals *known* structure. Design the **value function +
   search** for discovering *genuinely new* methods/decompositions/primitives (oracle-gated) — not just
   re-parameterizing known families.
3. **Horizontal expansion (the main open question):** given that vertical scale is walled off by identity,
   what is the **strongest abstraction-layer expansion**? Critique the candidate framing above (QSVT/LCU,
   fermionic, FTQC-native, structural→strong verification) and propose the highest impact × feasibility path
   — or a better axis we missed.
4. **Verification strength for large circuits:** big apps are Tier-1 *structural* (Merkle, no unitary
   guarantee) because dense is infeasible. Since there is no hardware to re-check them later, how would you
   make large-circuit seals *strong* (ZX / partial-subspace / symbolic) without breaking determinism?
5. **Unproven consensus:** cross-model co-error never materialized (4 rounds) and the ρ-correlation discount
   is validated only by *constructed* co-errors. How would you exercise the defense with *real* divergence?
6. **Adoption (software, not hardware):** a self-contained single repo. Credible path to external adoption —
   interoperability (QASM/Qiskit/Cirq/PennyLane), citation/consumption of the sealed registry, CI seal-gate?
7. What **risks or blind spots** are missed, and your **top-3 six-month roadmap** ranked by impact × feasibility.

## Concept mini-glossary

- **QPGF oracle** — deterministic checker. `verify_seal.py <spec.pg> --out <dir>` → `exit 0 ⟺ <id>.sealed.json
  ⟺ passed`. Checks dimension (C1), unitarity/phase (C2), ancilla/isometry (C3), agreement with an
  *independent* reference (C4). **Used, never reimplemented.**
- **Seal** — tamper-evident SHA-256 record embedding a fingerprint of the oracle's own code (altering the
  oracle invalidates every seal).
- **Seal Tier** — `0 EXACT` (dense, n≤12) · `1 STRUCTURAL` (Merkle, *no* unitary guarantee) · `2 CLIFFORD`
  (tableau) · `3 CLIFFORD+T` (ZX). Higher tiers trade exact equivalence for scale.
- **Cross-model consensus** — a new gate's truth is established when ≥2 *physically distinct* model weights
  converge on the same unitary hash; same-weights duplicates collapse to one vote (defeats B4 "both default
  to the same wrong answer"); a near-tie among top-2 independent units → `CONTESTED` → sealing refused.

## Hard constraints a proposal must respect

- **Determinism inviolable** — byte-identical re-seal; frozen consensus keys never regenerated.
- **Oracle used, not reimplemented** — `verify_seal.py`/`contracts.py` never modified (hashes baked into seals).
- **Honest decomposition** — no `MatrixGate`/literal-answer shortcut; a real circuit decomposition.
- **Self-contained** — no external skills/services beyond the vendored oracle.

Verify everything yourself: `python scripts/reproduce_all.py` → `REPRODUCED · root a0b4f678… · second_oracle
71/71 · 77 modules / 166 apps`. Honest limitations are in `docs/QuantaFoundry-Technical-Spec.md` and README's
"Honest boundaries".
