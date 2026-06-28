<!-- EXTERNAL-ONBOARDING.md · for a fresh external AI runtime · written 2026-06-28 -->
# QuantaFoundry — External Onboarding & Proposal Request

You are a **fresh external runtime** seeing this project for the first time. This single
document is your entry point. Read it fully, then read the attached files in the order given
in §4, then answer the proposal request in §2.

We are **not** asking for praise. We want your sharpest critique of the weakest assumptions
and concrete, feasible directions for what to build next.

---

## 1. What this is (identity)

**QuantaFoundry** is a quantum-circuit *foundry*: every artifact (a quantum gate, a composed
algorithm) must pass a **deterministic verification oracle (QPGF)** to be *sealed*. Unsealed
artifacts do not exist in the library — there is no "trust me, it works." The seal is a
tamper-evident SHA-256 record; sealed modules compound into larger sealed apps, which can be
recomposed again. The thesis: **trust capital accrues with compound interest** — verification
is paid once, reused forever.

The three functions form a self-growth loop:
**① Generate** (an isolated AI persona writes the artifact; it *cannot* declare its own success)
→ **② Verify & store** (the deterministic oracle seals it → accumulates in a registry)
→ **③ Recompose** (seal modules into apps → back to ②).

**Honest novelty claim:** the *verification techniques* are not new (we reuse the ideas behind
VOQC/Qbricks, MQT QCEC). What is new is the **system integration**: an AI-terminating oracle +
binary seal/registry + fault-tolerant-resource accounting, where no AI is ever the judge of its
own output.

---

## 2. Your task (the proposal request)

**Role:** Act as an external reviewer of a quantum-verification + autonomous-AI architecture.
Be adversarial about assumptions; prioritize actionable next steps over validation.

Answer these, **in priority order**, each with `proposal / rationale / feasibility / risk`:

1. Is the core identity (an *AI-terminating oracle* + binary seal) convincing? What is the
   **single weakest assumption**, and how would you stress it?
2. **Open-ended goal-autonomy:** today the autonomous loop seals known families up to a
   frontier and then honestly stops ("0 new modules"). How would you design the **value
   function + search strategy** for *discovering genuinely new methods/families* and
   autonomously generating *unsealed primitives*?
3. **Backend 8c:** real-hardware (QPU) backend, noise models, and Tier-1 large-circuit
   execution are unstarted. Priority and approach?
4. **Unproven consensus areas:** cross-model co-error never materialized (4 rounds) and the
   ρ-correlation discount is validated only by synthetic self-tests. How would you *close*
   these — i.e. actually exercise the defense with real divergence?
5. **Adoption / ecosystem:** the project is currently a self-contained single repo. What is a
   credible path to external adoption?
6. What **risks or blind spots** have we missed?
7. Your **top-3 six-month roadmap** items, ranked by impact × feasibility.

**Answer format:** structured, one block per proposal. Cite which attached file informs each
point. If you think a claim is overstated, say so and point to the evidence.

---

## 3. Concept mini-glossary (read before the attachments)

- **QPGF oracle** — a deterministic checker. Contract: `verify_seal.py <spec.pg> --out <dir>`
  → `exit 0 ⟺ <id>.sealed.json ⟺ passed`. It checks dimension (C1), unitarity/phase (C2),
  ancilla/isometry (C3), and agreement with an *independent* reference matrix (C4). The oracle
  is **used, never reimplemented** by the foundry.
- **Seal** — a tamper-evident SHA-256 record proving an artifact passed the oracle. It embeds a
  fingerprint of the oracle's own code, so altering the oracle invalidates every existing seal.
- **Seal Tier** — `0 EXACT` (dense matrix, n≤12) · `1 STRUCTURAL` (Merkle, *no* unitary
  guarantee) · `2 CLIFFORD` (tableau) · `3 CLIFFORD+T` (ZX). Higher-tier seals trade exact
  equivalence for scalability; Tier-1 guarantees *well-formedness*, not unitary equivalence.
- **cross-model consensus** — truth for a new gate is established when ≥2 *physically distinct*
  model runtimes (different weights) independently converge on the same unitary hash. Same-weights
  duplicates collapse to one vote (this defeats the "both models default to the same wrong answer"
  failure, called B4). A near-tie among top-2 independent units → `CONTESTED` → sealing refused.
- **PG / PGF notation** — the project's design files (e.g. `task_plan_pg.md`) use *PG*: an
  indentation tree (Gantree) + Python-like pseudocode where `AI_`-prefixed calls denote cognitive
  steps. **You do not need to parse it — just comprehend it.** A node's `(status)` tag
  (`done`/`in-progress`/…) tells you what is built vs planned.

---

## 4. Reading order (the attachments)

Read in this order. Tier 1 is enough to give a first proposal; Tier 2/3 are for depth.

**Tier 1 — required**
1. `README.md` — vision, architecture, trust model, honest positioning. *Start here.*
2. `HANDOFF.md` — current-state digest (canonical numbers, remaining work, invariants).
3. `task_plan_pg.md` — the roadmap "spine" in PG notation; the direct starting point for §2.

**Tier 2 — for deeper proposals**
4. `docs/QuantaFoundry-Technical-Spec.md` — full technical spec + evidence + limitations (large).
5. `.agents/skills/qpgf-oracle/SKILL.md` — the oracle's contract (how sealing actually works).
6. `registry/REGISTRY-MANIFEST.json` — authoritative counts and the registry root hash.

**Tier 3 — evidence, only if you are skeptical of a claim**
7. `_workspace/crossmodel/EXT-V04-INGEST-REPORT.md`, `EXT-V05-INGEST-REPORT.md` — real
   6-runtime cross-model results.
8. `.pgf/bounty/P3D-ROUND2.json … ROUND4.json` — adversarial falsification rounds.

> Not included on purpose: the Python under `scripts/` and `.pgf/keyfree/`, the raw
> `registry/modules/*.sealed.json`, and `specs/`. They are for *execution*, not comprehension,
> and would only burn your context. Ask if you need a specific one.

---

## 5. Current state (canonical, as of 2026-06-28)

Authoritative source = `registry/REGISTRY-MANIFEST.json`. Reproducible via §8.

- **61 sealed modules (55 Tier-0 dense + 6 Tier-2 Clifford) · 77 sealed apps.** (`registry/apps` holds 123 files = 77 unique +
  46 app-side re-seal caches; canonical modules live in `registry/modules`.)
- **registry_root_hash = `d231fbf4…`** · **23 frozen consensus keys.**
- Re-discovery cross-check **6/6** · independent second-oracle **55/55** (Tier-0 dense full coverage; the 6 Tier-2 Clifford modules — Steane/Shor-9 QEC + transversal logical H/S/CNOT — are tableau-sealed + stabilizer-witnessed, outside dense scope) · triple-agreement **7/7**.

Completed milestones (so you don't re-propose them):
- Base gates sealed; **first live cross-model truth** = `sx` (√X), 6 distinct-weights runtimes
  converged → PROOF_BACKED seal.
- Gate → QFT → QPE → **Shor** stack: **N=15** (special, 2⁴−1 degeneracy — every base is cheap)
  · **N=21** (*genuine* modular arithmetic, `shor21_a2` Tier-0 12-qubit, 21=3×7)
  · **distinct-prime** family (`cmul2_mod33`=3×11, `cmul2_mod35`=5×7).
- **F3 compose** — sealed modules recomposed into higher apps (Bell/GHZ/Grover/QPE…).
- **GenSkill self-extending library** (8 generation *methods* as first-class skills); all
  families (ghz/cluster/ring/wstate) reach MAX_N=10 via an unattended forge-to-frontier loop.
- **Backend adapter v0.1** (simulator: numpy + cirq) — runs sealed apps to *observe behavior*
  (execution ≠ verification, explicitly).
- **Honest-decomposition guard** — blocks "hollow" seals (custom bloq with a literal matrix,
  MatrixGate/from_unitary) on both module- and app-seal paths, without touching the
  fingerprinted oracle.
- **Falsification (P3) + 4-round cross-model adversarial (P3d):** co-error 0 across 4 rounds;
  the `CONTESTED` near-tie guard fired on **real** data for the first time (qft2, a 2-2-1-1
  convention split).
- **v0.7+ Stage 0–5 (non-destructive analysis/tool/verification layers; registry root and all
  48/59 seals unchanged):** QF-Discover value function (objective fan-in-based ranking; `c6x`'s
  leverage captured *before* the fact) + decomposition optimizer + goal-selection guard; OpenQASM3
  export/ingest with round-trip identity (57/57) + a `qf` CLI + a citable `CITATION.cff`; a
  convention-independence audit; ρ-discount validation against *constructed* co-errors; and
  determinism env-pin + oracle-revocation (fingerprint 145/145 intact) + ed25519 Sybil defense.
  Auto-derived primitive proposals (`c7x`, `cr8`) and four EXT relay packages await cross-runtime
  dispatch. **Don't re-propose these as if missing — but improvements/critiques are welcome.**

---

## 6. Honest limitations (please factor these in)

We hold ourselves to this; proposals that ignore it will read as naive.

- Cross-model **co-error "did not occur" ≠ "is impossible"** (4 rounds, frontier models robust
  on standard gates — but that is empirical, not a proof). *Natural-occurrence* co-error on real
  weak-model panels is still unmeasured (an EXT relay package is prepared).
- The **ρ-correlation discount defense is now mechanism-validated** against *constructed* co-errors
  (S4 W4.2 — it collapses a poisoned consensus to <2 independent), but **natural-occurrence**
  corpus correlation on real weak-model panels is still pending (EXT). Don't overclaim ρ as proven
  in the wild.
- A **value function now exists** (S2 QF-Discover — objective dependency-fan-in ranking), but
  continuous *unattended* discovery is still **manually triggered**; there is no always-on loop
  driving it yet.
- **Tier-1 unitary-equivalence: one deliberate structural-only seal** — `ghz16` was raised to
  `unitary_equiv_sampled` (S1, sampled-dense two-path + sealed seed); the **W6.5 `shor91` capstone**
  re-introduces exactly **one `structural_wellformed` seal** (15 qubits > dense ceiling — a Merkle of
  sealed parts, honestly weaker than dense equivalence, by design). Sampled-dense is *probabilistic-complete*, not full dense equivalence; a
  future large non-Clifford app would re-open the gap (a ZX Tier-3 path is staged for it).
- **Convention is a shared assumption, not independently derived** (S4 W4.1 audit): `second_oracle`
  re-derives the *unitary* independently, but endian/global-phase/atol/canonical-hash are shared
  with the oracle — a common convention bug would pass both. Named as a gap, not yet closed.
- Verification techniques themselves are **reused, not invented** (see §1).

---

## 7. Hard constraints (a proposal must respect these)

- **Determinism is inviolable** — seals are byte-identical on re-run; frozen consensus keys are
  never regenerated during inspection.
- **The oracle is used, not reimplemented or copied.** Two fingerprinted files
  (`verify_seal.py`, `contracts.py`) are *never* modified — their hashes are baked into every
  seal. Policy guards live in non-fingerprinted files only.
- **Honest decomposition** — a bloq may not smuggle in a literal answer matrix (no MatrixGate
  shortcut); the artifact must be a real circuit decomposition.
- **Self-contained** — the project depends on no external skills/services beyond a vendored copy
  of the oracle.

---

## 8. How to verify our claims yourself

Don't take the numbers on faith. The whole library re-seals deterministically:

```
python scripts/reproduce_all.py
# expect: REPRODUCED · root_hash=d231fbf4… · second_oracle 55/55 · behavior pass
```

If `root_hash` matches `d231fbf4…`, the 61 modules + 77 apps reproduced byte-for-byte.

---

*End of onboarding. Proceed to `README.md` → `HANDOFF.md` → `task_plan_pg.md`, then answer §2.*
