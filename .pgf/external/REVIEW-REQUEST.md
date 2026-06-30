<!-- External adversarial review request — for a fresh external AI runtime asked to critique QuantaFoundry.
     Distilled from the former EXTERNAL-ONBOARDING.md §2–§3 (2026-07-01). Entry/reading order: AGENTS.md. -->
# QuantaFoundry — External Review Request

**Role:** external reviewer of a quantum-verification + autonomous-AI architecture. Be adversarial about
assumptions; prioritize actionable next steps over validation. We do **not** want praise — we want the
sharpest critique of the weakest assumptions and concrete, feasible directions.

First read, in order: `README.md` (identity, trust model, current status) → `.pgf/DESIGN-MasterRoadmap.md`
(execution roadmap spine, PG notation) → `docs/QuantaFoundry-Technical-Spec.md` (full spec + evidence +
limitations + version history). Then answer these in priority order, each as `proposal / rationale /
feasibility / risk`, citing the file that informs each point:

1. Is the core identity (an **AI-terminating oracle** + binary seal, where no AI judges its own output)
   convincing? What is the **single weakest assumption**, and how would you stress it?
2. **Open-ended goal-autonomy:** the loop (`qfa-loop`) now auto-discovers and seals frontier families via a
   regression-gated parametric factory, but still seals *known* structure. How would you design the **value
   function + search** for discovering *genuinely new methods/families* and autonomously generating *unsealed
   primitives*?
3. **Backend (real hardware):** QPU backends, noise models, and Tier-1 large-circuit execution are unstarted.
   Priority and approach?
4. **Unproven consensus areas:** cross-model co-error never materialized (4 rounds) and the ρ-correlation
   discount is validated only by *constructed* co-errors. How would you actually exercise the defense with
   real divergence on weak-model panels?
5. **Adoption / ecosystem:** currently a self-contained single repo. A credible path to external adoption?
6. What **risks or blind spots** are missed?
7. Your **top-3 six-month roadmap** items, ranked by impact × feasibility.

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
71/71`. Honest limitations are in `docs/QuantaFoundry-Technical-Spec.md` (limitations sections) and README's
"Honest boundaries".
