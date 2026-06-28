# QuantaFoundry — Technical Specification

> **Version:** 0.7 (v0.6 + Clifford Tier-2 routing, distinct-prime arithmetic, multi-model gated
> panel with first *live* cross-model truth, falsification front, honest-decomposition closure) ·
> **Date:** 2026-06-28
> *(v0.5: GenSkill library — generation *methods* as a first-class catalog. v0.4: honesty calibration +
> genuine N=21 modular arithmetic, app-level cross-model, second-oracle, goal-autonomy family extension,
> semantic_guarantee.)*
> **Audience:** AI runtimes and engineers performing an independent design review.
> **Status of claims:** every result in §8 is reproduced from the working tree; "planned"/"hypothesis" items are marked.
> **What changed since v0.3:** (1) Shor extended to **N=21 = 3 × 7 with genuine modular arithmetic**
> (honest reversible synthesis, no MatrixGate) — N=15 was a 2⁴−1 degeneracy; (2) **app-level**
> cross-model corroboration done (EXT v04: app-golden 4/4 + app-bloq 4/4) and consensus **necessity**
> demonstrated by a true-divergence probe (EXT v05: free-parameter intents diverge); (3) a
> **second, Qualtran-independent oracle** re-checks sealed unitaries (48/48); (4) **goal-autonomy**
> extended to multiple families (GHZ + cluster) with autonomous sealing (human seed 0); (5) per-seal
> **semantic_guarantee** layer (Tier-1 ≠ unitary_equiv, made explicit). Library now **46 sealed
> modules → 57 sealed applications**, every primitive established with **zero human answer keys** (§8).
> **What changed since v0.5:** the GenSkill library became *self-extending* (§8.7): (1) an
> **arithmetic-synthesis** skill synthesizes controlled modular multipliers (×a mod N) via MMD
> reversible synthesis into sealed MCTs — reproducing all 6 committed multipliers' sealed unitaries;
> (2) a **continuous-rotation W-state** family — the first algorithm-level states needing irrational
> Ry angles (α_k=arccos√(1/k) primitives, sealed with global-phase-tolerant C4), W₃–W₁₀ autonomously
> sealed; (3) goal-autonomy gained an **unmanned loop-to-frontier** that recomposes sealed modules
> until every gap is done or blocked, then names its own missing prerequisites; (4) an
> **analytic-golden** skill captures the closed-form gate-construction methods (Z^t phase, controlled-R_k,
> DFT) — reproducing 17 committed gate modules' sealed unitaries; (5) the catalog gained a **method
> self-seal** (per-skill source hash + `catalog_root_hash`, tamper-evident — the method-side counterpart
> of `registry_root_hash`). The library grew to **46 sealed modules → 57 sealed applications**
> (24 forged autonomously, human seed 0, zero new modules beyond the Ry primitives).
> **What changed in v0.5:** a **GenSkill library** (`scripts/genskills.py`,
> `registry/GENSKILL-CATALOG.json`) promotes generation *methods* — previously ad-hoc code — to a
> first-class, introspectable catalog, the method-side counterpart of the result registry. goal-autonomy
> consumes it. GenSkill mints no trust; its output still must pass the oracle to be sealed (§8.7).
> **Honesty calibration (this version):** several v0.3 claims are scoped down — see §3/§10/§11 and the
> per-section notes. "Non-linear production capacity" is now stated as a **hypothesis** with first
> evidence, not a result.
> **What changed since v0.6 (v0.7, §8.8):** (1) **Clifford Tier-2 routing** — the sole STRUCTURAL
> (Tier-1) app `ghz16` now also carries a stabilizer-tableau Tier-2 seal, closing the one weak-guarantee
> gap (companion seal, not replacement); (2) **distinct-prime arithmetic** — sealing `cmul2_mod33`
> (3×11) and `cmul2_mod35` (5×7) surfaced a missing prerequisite `c6x` (MCT-6), sealed key-free, after
> which the GenSkill engine was *evolved* (honest framing: a new primitive opens a family, not "infinite
> reuse"); (3) **gated multi-model panel** (§8.8) that structurally enforces ≥2 distinct-weights for
> key-free/ambiguous intents (B4 co-error blocked), validated by replaying the EXT v05 6-runtime data;
> (4) **first *live* cross-model truth** — a new intent `sx` (√X) was authored by 6 distinct runtimes
> that converged (MULTIMODEL) and was sealed with a frozen consensus key triangulated by an algebraic
> proof (PROOF_BACKED); (5) a **falsification front** (red-team of the oracle/gate/consensus) + an
> **honest-decomposition guard** that closes the "hollow seal" gap (a custom bloq asserting a literal
> unitary) on both the module and app sealing paths, **without modifying the fingerprinted oracle**
> (existing seals byte-identical); (6) **cross-runtime co-error rounds** that, on a genuinely
> convention-contested intent (2-qubit QFT), exercised the contested near-tie guard on *real* multi-model
> data (it refused to seal an under-specified intent). Library grew to **48 sealed modules → 59 sealed
> applications**; frozen consensus keys: **23**; `registry_root_hash` `3dae613d…` reproduces byte-identical.

> **What changed in v0.7+ (Stage 0–5 process plan):** non-destructive analysis/tool/verification layers
> over the sealed core — the registry root `3dae613d…` and all 48/59 seals are **unchanged** (no new
> seals; the fingerprinted oracle files untouched). **(S0)** `second_oracle` independent re-derivation
> extended to **48/48 modules** + a Tier-0/1 headline split (no exact-coverage overclaim). **(S1)**
> Tier-1 closure — `ghz16` raised to `unitary_equiv_sampled` (sampled-dense two-path, sealed seed; **zero
> structural-only**), a ZX-routing path (infrastructure self-test 6/6; immediate target 0 — honest
> negative), and a global-phase tracker (controlled-pair composition proven safe). **(S2) QF-Discover** —
> an 8-term value function whose terms derive from registry graph structure (Composability =
> counterfactual dependency fan-in; `c6x`'s leverage captured *before* the fact, validated
> retrospectively), a decomposition optimizer with the oracle as a hard reward (reward-hacking
> structurally blocked; 6/6 cheaper-decomposition groups found), a goal-selection guard, and an
> auto-derived primitive-proposal package (`c7x`, `cr8_dag_gate`). **(S3) Adoption** — OpenQASM3
> export/ingest with round-trip unitary identity (57/57 re-derived by the numpy oracle; closed loop 8/8),
> a `qf` CLI (wrapping existing scripts, zero new verification logic), and a citable `CITATION.cff`
> binding the root hash. **(S4) Consensus close** — a convention-independence audit (unitary
> *construction* = independent → risk(d) closed; endian/phase/atol/hash = **shared assumption**, gap
> named) and ρ-discount validation against *constructed* co-errors (lineage-merge + ρ collapse a poisoned
> consensus to <2 independent; mechanism **live**, natural co-error deferred to EXT). **(S5) Hardening** —
> determinism env-pin (byte-identity robust to FP/BLAS noise; `requirements.lock`), an oracle-revocation
> protocol (fingerprint **145/145 intact**, `docs/EMERGENCY-RESEAL.md`), and ed25519 Sybil defense
> (pubkey-strengthened independence units). EXT relay packages are prepared for the four cross-runtime
> items; backend evidence remains gated/deferred. Companion docs: `docs/CONVENTION-AUDIT.md`,
> `docs/TRUST-MODEL-VALIDATION-REPORT.md`, `docs/EMERGENCY-RESEAL.md`.

---

## 0. How to read and review this document

This spec is **self-contained**: you should be able to review the design, the trust model, the
implementation, and the verification evidence **without reading the source code**. Where code is
load-bearing for the argument, the relevant snippet or interface is inlined.

The goal of this review is to **raise the project's correctness and honesty**. We are explicitly
soliciting adversarial critique. The most useful review targets are in **§9 (Limitations & threats)**
and the concrete questions in **§13**. If you find a flaw not listed there, that is the highest-value
outcome.

Terminology: a **seal** is a deterministic, tamper-evident certificate that a generated quantum
module's unitary matches an independently authored mathematical reference. "**Proven**" in this
document always means *conditionally proven* — the conditions are stated in §5.

---

## 1. Summary

QuantaFoundry is an **AI-native quantum software foundry**. It turns high-level intent into quantum
software modules, **verifies them with a deterministic contract oracle**, **seals only what is
proven**, accumulates sealed modules in a registry, and **composes** sealed modules into larger
applications (each re-verified and re-sealed). All four functions are realized: the library
holds **48 sealed base modules** and **59 sealed applications** (v0.7; 46 → 57 at v0.6), the latter
built entirely by recomposing the former — up to **Shor period-finding circuits that factor
15 = 3 × 5 and 21 = 3 × 7** (the latter with genuine modular arithmetic, not the N=15 special case).
Guarantee split (no exact-coverage overclaim): all 48 modules are `unitary_equiv` (Tier-0 EXACT); the
59 apps are 58 `unitary_equiv` + **1 `unitary_equiv_sampled`** (`ghz16`, sampled-dense two-path verified
with a sealed seed via `sampled_dense_verify.py`, also Tier-2 sealed) — **zero structural-only seals**.
Authoritative tally in `registry/SEMANTIC-GUARANTEES.json` `headline_split`.

The single non-negotiable rule:

```
AI generates.
Oracle verifies (deterministically).
Registry remembers only sealed modules.
Composition uses only sealed modules.
```

The verification core is a separate, already-public project, **QPGF**
(github.com/sadpig70/QPGF, v0.1.0, MIT, Sigstore-signed, 157 self-verification checks green).
QuantaFoundry is the foundry layer built *around* that core. The spec's contributions, in order of
strength:

1. **AutoForge** — an autonomous generation→seal loop in which cross-author isolation is provided by
   isolated AI personas (sub-agent contexts) (§7).
2. **KeyFreeConsensus, realized with real cross-model authorship** — truth (the correct unitary) is
   established when **independent sources of different physical weights converge on the same hash**,
   with **no human answer key**. Six independent runtimes (gpt-5, gemini, grok, kimi, qwen, deepseek)
   authored every base gate's reference and implementation; all converged, and each converged hash was
   independently corroborated by a stack-independent symbolic proof (§8.2).
3. **Compounding via composition (F3)** — sealed modules recompose into sealed applications, each
   re-verified against the contract oracle. The library grew to 48 verified gates and 59 verified
   applications including Grover, QFT(2–4), Quantum Phase Estimation, **Shor period-finding (N=15 and
   genuine N=21)**, distinct-prime modular multipliers (mod 33, 35), and autonomously-discovered
   families (GHZ, cluster), with every new primitive (controlled-phase family, Fredkin, modular
   multipliers, MCT-6) also established key-free (§8.3–8.4, §8.8).

The single load-bearing fact for a reviewer: **no result in this library rests on a human-asserted
answer.** Every gate's truth came from independent cross-model convergence + symbolic proof; every
application's correctness came from the deterministic oracle checking the composition against an
independently-authored intent.

---

## 2. Problem and positioning

Most AI coding tools can emit plausible quantum code. The hard part is not generation; it is
**knowing, deterministically, that the generated circuit is correct** — and making that knowledge
*accumulate* rather than being re-established by a human every time.

QuantaFoundry does **not** introduce a new verification algorithm. The deterministic, phase-aware
verification it relies on reuses established techniques:

| Technique | Prior art reused |
|---|---|
| Exact dense unitary equivalence | tensor contraction (Qualtran) |
| Stabilizer-tableau equivalence | Gottesman–Knill / standard tableau |
| ZX-calculus equivalence | pyzx; cf. MQT QCEC |
| Phase-aware matrix/path-sum semantics | VOQC/SQIR, Qbricks (as positioning reference) |

The contribution is **systems integration**: turning verification into an **AI-loop termination
oracle** with a **binary tamper-evident seal**, a **sealed registry with composition invariants**,
and **FTQC resource accounting**, wired so that *only what is proven can exist downstream*. Generation
-side LLM work (e.g. QUASAR, Agent-Q) typically uses simulator/RL reward and has **no binary seal or
registry**. That gap is the defensible position.

---

## 3. Identity and the boundary discipline

**Identity:** QuantaFoundry is *"a foundry where everything is sealed,"* not *"one more code
generator."* The QPGF oracle is the load-bearing differentiator.

**Boundary discipline (must hold at every point in the system):**

1. A generator (AI) may iterate but **can never declare its own success.** Only the oracle, via a
   deterministic exit code, terminates the loop.
2. **An artifact that fails to seal does not exist** downstream. It is never registered, never
   composed, never reported as a result.
3. Verification is delegated **only** to deterministic code (the oracle). Personas *generate*; they
   **do not judge**.
4. The oracle is **used, never re-implemented**, inside the foundry (it is vendored as a skill bundle
   and called as-is). This keeps the trust root singular and auditable.

If this discipline blurs, QuantaFoundry degrades into just another AI code generator. Reviewers
should watch for any path that lets an unsealed artifact influence a downstream result.

---

## 4. The three core functions

```
        intent
          │
   ┌──────▼───────┐  candidate.pg  ┌────────────────────┐  sealed.json  ┌──────────────┐
   │ 1. GENERATE  │ ─────────────▶ │ 2. VERIFY & SEAL   │ ───────────▶ │  REGISTRY     │
   │ (AI, isolated)│   ◀─REPAIR──── │ (oracle, determ.)  │              │ (sealed only) │
   └──────────────┘  (C4 signal)   └────────────────────┘              └──────┬───────┘
                                          ▲                                    │ sealed inputs
                                          │ re-verify                ┌─────────▼──────────┐
                                          └──────────────────────────│ 3. COMPOSE → app.pg│
                                                                      └────────────────────┘
```

1. **Generate.** An AI runtime turns an intent into a candidate `.pg` (a `bloq` implementation, an
   independently authored `golden` reference, and `meta`). It may retry; it cannot self-certify.
   *Generation methods themselves are now a reusable library (GenSkill, v0.5):* recurring construction
   recipes (e.g. linear-CNOT entangler, graph-state synthesis) are catalogued as named, parametrized
   skills that emit candidate specs deterministically — but the boundary holds, a GenSkill cannot
   self-certify either; its output re-enters function 2 (§8.7).
2. **Verify & seal → store.** A deterministic oracle checks contracts C1–C4, selects a seal tier,
   and emits `<id>.sealed.json` iff the candidate passes. Sealed artifacts are admitted to the
   registry under invariants INV1–3.
3. **Compose → new output.** Sealed modules are assembled into larger apps; the composite is given
   its own reference check (C-app) and must itself pass function 2 to be sealed. Its output re-enters
   function 2, so **the output of 3 becomes new raw material for 1/3** — a self-growing loop.

**The meaning of accumulation.** Sealing is not storage; it is **trust-capital formation**. The
verification cost is paid once and the result is reusable forever (deterministic, byte-identical on
recompute). N sealed modules yield a combinatorially larger space of composable apps, so production
capacity *should* grow super-linearly with the registry. **This non-linearity is a hypothesis, not yet
a proven result.** The first measured evidence is `COMPOUNDING-CURVE.json`: a fixed pair of modules
(h+cnot, and h+cz) generates an unbounded family (GHZ_n, cluster_n) at **marginal new-module cost 0**,
and goal-autonomy selects those extensions itself (§8.6). General super-linearity across arbitrary apps
is unmeasured. This is the economic reason the base-module library (thread C) is the first deliverable:
compounding needs principal first.

---

## 5. Trust model (review this most carefully)

A sealing system is only as trustworthy as its trust boundary. We state ours explicitly.

### 5.1 What a seal is — and is not

A seal's signature is a **sha256 over canonical fields** of the sealed artifact. It is therefore
**tamper-evident**, **not** a secret-key cryptographic forgery proof. Anyone who recomputes with the
genuine oracle gets the same hash; nobody is prevented from *fabricating* a seal — they are only
prevented from fabricating one that **survives central recomputation**.

### 5.2 The three conditions of "proven"

A seal means "proven" **only** conditional on:

1. **Verifier integrity** — the oracle code that produced the seal is genuine
   (mechanism: `oracle_code_hash`/`contracts_code_hash` folded into the signature;
   `verify_provenance` detects seals from a different bundle; `BUNDLE.sha256` hashes every file).
2. **Golden legitimacy** — the reference the implementation is checked against is itself correct and
   *independent* of the implementation (mechanisms in §5.3).
3. **Central recomputation** — a trusted party re-runs `verify_seal` rather than trusting a submitted
   seal. Registration always recomputes; external seals are never trusted directly.

For deployment, `verify_bundle` gates on integrity **and** a release signature
(GPG, or keyless **Sigstore** via CI), returning `TRUSTED / INTEGRITY_ONLY / UNTRUSTED_SIGNATURE /
TAMPERED`. Honest limit: signing **relocates** the trust root to a public key / transparency log; it
does not eliminate it.

### 5.3 The golden-legitimacy attack (the subtle one)

If the **same** AI, in the **same context**, writes both the implementation and the golden, both can
converge on the **same wrong target** and the check passes vacuously. Mitigations, in increasing
strength:

- **golden_guard** — *static* defense: blocks self-reference (golden copying the implementation's
  tensor output) and trivial/identity goldens. Does **not** stop semantic co-error.
- **CrossGen (author isolation)** — *structural* defense: golden and implementation are produced by
  **separate, isolated authors** from the same intent, neither seeing the other. Agreement then means
  the implementation passed an *independently authored* golden.

§7 explains how AutoForge realizes CrossGen with isolated **personas**, and the precise limit of that
substitution (§7.1, §9).

---

## 6. QPGF oracle — the load-bearing core

This section documents the oracle as a **black box with a precise contract**, sufficient to review
AutoForge. Full source is in `.agents/skills/qpgf-oracle/`.

### 6.1 `.pg` specification format

A spec is plain text with three fenced, labeled blocks (the oracle machine-extracts them):

````
```python id=bloq
from qualtran.bloqs.basic_gates import CNOT
bloq = CNOT()
```
```python id=golden
import numpy as np
golden = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)
```
```json id=meta
{"id": "cnot", "n_sys": 2, "n_anc": 0}
```
````

- `bloq` — a Qualtran construction; the oracle computes `bloq.tensor_contract()` → U.
- `golden` — an **independently authored** analytic reference matrix (numpy) or `cirq.Circuit`.
- `meta` — `id`, `n_sys`, `n_anc`, optional `tier`, `convention`.
- **Convention:** Qualtran-native raw **big-endian** (first register = basis MSB). golden is compared
  directly to U.

### 6.2 Contracts

| Contract | Check |
|---|---|
| **C1** | matrix shape = 2^n_sys × 2^n_sys |
| **C2** | unitarity `U†U = I` and phase preservation |
| **C3 / C3-iso** | ancilla cleanliness / faithful isometry `V†V = I` (n_anc > 0) |
| **C4** | `golden` equals U **up to global phase** (atol 1e-7) |
| **C4-uncompute** | compute–uncompute cleanliness |
| **C-app** | composed app equals app-level golden |

Verification is **exact symbolic/numeric** on the dense or structural representation — **never**
probabilistic measurement statistics.

### 6.3 Seal tiers (scaling past the 2^n bound)

| Tier | Range | Method | `semantic_guarantee` | Status |
|---|---|---|---|---|
| 0 EXACT | small | dense tensor contraction == golden | **unitary_equiv** | realized |
| 1 STRUCTURAL | large composition trees | Merkle hash of sealed children (no dense matrix) | **structural_wellformed** (⚠ *not* unitary_equiv) | realized |
| 2 CLIFFORD | large Clifford | stabilizer tableau, O(n²) | **unitary_equiv** | realized |
| 3 CLIFFORD+T | large universal | ZX-calculus equivalence to an independent golden circuit (pyzx) | **unitary_equiv** | realized, conservative |

All tiers are **exact, not approximate**. Tier-3 is **sound but conservative**: it seals only when ZX
*proves* equivalence; non-reduction is rejected, never wrongly sealed. (The 8 base modules in §8 are
all Tier-0 EXACT.)

**`semantic_guarantee` (v0.4, honesty).** A Tier-1 seal proves *structural* well-formedness — "these
sealed children, wired this way" via a Merkle hash — but does **not** prove the resulting 2ⁿ unitary
equals the intended one (no dense materialization, no C4). Conflating it with Tier-0/2/3
`unitary_equiv` would over-state. The guarantee class is recorded per seal in a non-destructive registry
layer `registry/SEMANTIC-GUARANTEES.json` (the oracle's `sealed.json` is never modified). For the one
large Tier-1 artifact (`ghz16_structural`), a **partial verification** raises the guarantee: a 2¹⁶
state-vector executes the sealed plan and is checked to (i) produce the exact GHZ₁₆ state on |0…0⟩, and
(ii) match a plan-independent GHZ unitary on 48 basis + 16 random inputs, with a negative control
confirming a mutated plan is rejected. This is a *partial* (sampled) semantic check, not full unitary
equivalence — and is labelled as such (`scripts/semantic_guarantee.py`).

### 6.4 Registry invariants and provenance

`Registry(store_dir).register(spec_path)` recomputes the seal and admits under:

- **INV1** — registration requires a passing `verify_seal`.
- **INV2** — only sealed modules may compose.
- **INV3** — every composition is re-verified and re-sealed.

Each sealed artifact carries: `id, sealed, convention, n_sys, n_anc, contract, tier, u_hash,
resource, sig, oracle_code_hash, contracts_code_hash, resource_schema_version`. Environment-dependent
fields are written to a **separate** provenance sidecar so the sealed JSON stays deterministic.

### 6.5 Determinism (a hard requirement)

The same spec, sealed twice, must produce **byte-identical** `sealed.json`. The `u_hash` (a hash of
the canonicalized unitary) is the module's stable identity. Known fixed answer keys include
qft3 `340b5f34…`, toffoli `e663b430…`, swap2 `e6255e2f…`. Breaking byte-identity (e.g. via CRLF in a
bundle file, or changing ATOL) is treated as a defect.

---

## 7. AutoForge — autonomous multi-persona CrossGen (the new work)

### 7.1 Substitution: cross-model → multi-persona

The proven CrossGen pattern in QPGF used **cross-model** author isolation: e.g. the golden written by
one runtime (Qwen), the implementation by another (Codex), with a **human courier** physically
keeping the two submissions apart. That human step blocks autonomy.

AutoForge replaces cross-model isolation with **cross-persona** isolation:

| | QPGF CrossGen | AutoForge |
|---|---|---|
| golden author | runtime A (e.g. Qwen) | **Persona-G** (an isolated sub-agent) |
| bloq author | runtime B (e.g. Codex) | **Persona-B** (an isolated sub-agent) |
| isolation | human courier | **sub-agent context isolation** (parent dispatches separately) |
| autonomy | blocked (human) | **operationally autonomous** (no human in the gen→seal loop) |

**Decompose the co-error risk into two kinds** — this is the crux of the review:

- **(a) Same-context co-error** — one chat writing both golden and bloq, dragged by prior output.
  Cross-persona **fully blocks this** (independent contexts): *equivalent to cross-model.*
- **(b) Same-weights systematic misconception** — the same base model shares pretraining biases and
  may misread the same intent the same way. Cross-persona is **weaker** here than cross-model, because
  weights are shared even though reasoning paths diverge.

**Why this is acceptable for thread C:** for base modules a **mathematical answer key exists**. Even
if both personas commit error (b) identically, the seal's `u_hash` will not match the answer key and
the oracle **rejects** it. Therefore, *in the answer-key-backed regime, cross-persona isolation incurs
**no additional** trust loss relative to cross-model **with respect to (b)*** — the answer key acts as
a post-hoc filter on the unitary; it does **not** by itself bind the intent→key legitimacy (that is a
separate condition, §5.2). Cross-model retains real value where **no answer key exists** (first-time
establishment of a new truth). Empirically (§8.1, E5'/B4) cross-persona alone seals a *semantically
arbitrary* module when no key exists and both same-model personas pick the same default — which is why
the answer-key-free path needs cross-model or proof-backed consensus (§9 item 2, §10).

### 7.2 The three personas (two active in thread C)

The persona count is derived from trust boundaries, not chosen arbitrarily:

| Persona | Role | Cognitive stance | Active in C? |
|---|---|---|---|
| **Persona-G** | author the analytic `golden` only; never sees/writes bloq | reductionist / first-principles math | yes |
| **Persona-B** | author the Qualtran `bloq` only; never sees/writes golden | pragmatic implementer | yes |
| **Persona-A** | adversary: independently re-derive golden, vote vs G (2-of-2) | skeptic / paranoid | **no** (only when no answer key) |

Definitions live in `.pgf/personas/`. Persona-A is the mitigation for risk (b) in the answer-key-free
regime; it is intentionally **off** for base modules because the answer key already closes (b).

### 7.3 Isolation mechanism

The parent orchestrator dispatches Persona-G and Persona-B as **separate sub-agent invocations**.
Each runs in its own context; the parent is the only entity that sees both outputs and **does not pass
G's golden to B or vice versa**. This is exactly the context isolation cross-model provides via a
courier — without the human. Each persona writes only its two fenced blocks to
`submissions/{golden,bloq}/<id>.pg`.

### 7.4 Answer-key anchoring (anti-swap / anti-co-error)

The orchestrator `autoforge.py` holds a fixed `ANSWER_KEY: {id → u_hash}`. After sealing, it rejects
any module whose `u_hash` differs from its key (`stage: anti_swap`). This catches both module
swapping and silent co-error. For the 3 modules that already exist in QPGF (swap2, toffoli, qft3) the
keys are the **published QPGF v0.1.0 values**; for the 5 new modules (x, z, h, cnot, qft2) the key was
**seeded once by a human-trusted deterministic computation** and is now frozen (DESIGN §3).

### 7.5 The autonomous loop (ADP / AI_SelfAct)

```
def AI_SelfAct(queue, store):                 # one autonomous cycle
    for intent in queue:
        for attempt in range(MAX_REPAIR):
            gp, bp = generate_isolated(intent)        # F1: two isolated personas
            res    = verify_and_seal(intent.id, gp, bp, store)  # F2: deterministic
            if res.status == "SEALED": break
            if res.status == "REPAIR":
                intent = relay_signal(intent, res.signal)  # C4 → re-generate
        # termination decided ONLY by oracle exit code; AI never self-certifies
    # if enough(registry): compose_new(registry)   # F3 (realized — see §8.3, forge_apps.py)
```

`verify_and_seal` = combine (with intent-consistency check on id/n_sys/n_anc) → `verify_seal` →
answer-key check → byte-identical re-seal check → `registry.register`. No human in the loop.

---

## 8. What was actually built and verified (evidence)

Thread C target: seal `x, z, h, cnot, swap, toffoli, qft2, qft3` via autonomous multi-persona
CrossGen, then admit to the registry.

**Procedure actually run:** 16 isolated sub-agents (8 Persona-G + 8 Persona-B) generated
golden/bloq submissions independently; `autoforge.py` combined, sealed, answer-key-checked,
re-sealed for determinism, and registered each module.

**Result: 8/8 SEALED · cross-independent 8 · deterministic-rerun 8 · registry-admitted 8.**

| id | n_sys | tier | u_hash (full) | answer-key source |
|---|---|---|---|---|
| x_gate | 1 | 0 EXACT | `7dc1df52d07dd7428a4c2ab9ba2e3f982b6dea78d0ee6eb2f7ea865faa19ba5a` | seeded |
| z_gate | 1 | 0 EXACT | `1e3c0f2fa747f4fac16a11dd3959f83cc23b71b26e66528032c6223af01846e4` | seeded |
| h_gate | 1 | 0 EXACT | `0d6a0b7a9a19ad2e65004d4811b3907a5f1c8f4edbde59c0fefd9d3ff260b90c` | seeded |
| cnot | 2 | 0 EXACT | `3913bcef764f36b8b170748f1fe1641d3aa3d06e9e317cb0b553bd9bc58fd4a5` | seeded |
| swap2 | 2 | 0 EXACT | `e6255e2f105a97829f59ec648c92ef42d7fb19bd952f0c8534371e352e77153e` | **QPGF match** |
| toffoli | 3 | 0 EXACT | `e663b43043af6b78ca6b8fae14b5f38d2ae902d96db3aeafa16ce89efdf8f17d` | **QPGF match** |
| qft2 | 2 | 0 EXACT | `90dbc731bb8c7e80f8ff62b9be6975bf453dbbb3dc645a25960cfba3477dad82` | seeded |
| qft3 | 3 | 0 EXACT | `340b5f344fae9b997d17883cd1bc10bbcbd4c1c37252ce889c26d0e4adc74bed` | **QPGF match** |

**Cross-check (independent corroboration):** swap2, toffoli, qft3 reproduced the **published QPGF
v0.1.0 answer keys byte-for-byte**, despite golden/bloq being authored here by isolated personas. This
is independent evidence that (i) the oracle is deterministic across environments and (ii) the personas
produced genuinely correct artifacts, not artifacts fitted to a known key (the personas never saw the
keys).

**Independence sample (cnot):** Persona-G derived the 4×4 matrix analytically as a permutation
operator from `|c,t> → |c, t⊕c>` with explicit big-endian reasoning; Persona-B wrote
`from qualtran.bloqs.basic_gates import CNOT; bloq = CNOT()`. Different authors, different
representations, agreement enforced by C4.

Artifacts: `specs/modules/*.pg` (8 sealed specs), `registry/modules/*.sealed.json` (8 registered),
`.pgf/DESIGN-AutoForge.md`, `.pgf/status-AutoForge.json`, `.pgf/autoforge/autoforge.py`,
`.pgf/autoforge/FORGE-RESULT.json`.

### 8.1 Empirical validation (post-review falsification experiments)

After the first review round, we ran experiments designed to *break* the trust claims rather than
confirm them. Summary:

| Exp | Claim under test | Result |
|---|---|---|
| E1 | answer-key anti-swap rejects a tampered key | **PASS** — flipping one hex nibble of a key → `REJECT@anti_swap` (the sealed unitary is correct, `got` = real hash, yet rejected because it no longer matches the key) |
| E3a | signed-zero does not perturb the hash | **PASS** — injecting `-0.0j` into the golden leaves `u_hash` bit-identical |
| E3b | hash-seed independence | **PASS** — `PYTHONHASHSEED` 0 vs 99991 → byte-identical `sealed.json` |
| E5/E7 (clear intent) | isolation under a well-specified trap (`cnot_rev`: control on the *second* register) | single model is robust — both same-context and isolated authors reached the intended unitary 3/3; isolation advantage did **not** appear (the trap was too explicit) |
| E5'/E7' (ambiguous intent) | isolation under an *under-specified* intent (`cphase_amb`: phase on \|11⟩, **value unspecified**) | **DECISIVE — see below** |

**E5' is the central empirical finding for the trust model.** With an intent that leaves a free
parameter (the phase value), authors diverged across {π/4, π/2, π}:

- **Same-context author: 4/4 sealed.** Each author is internally self-consistent at an *arbitrary*
  phase, so the ambiguity is silently hidden and everything seals.
- **Isolated authors: 3/4 REPAIR (sealing failed).** The golden author and the bloq author picked
  *different* phases → C4 mismatch → the ambiguity was **exposed** as a sealing failure.
- **But 1/4 sealed (case B4): both isolated same-model personas independently defaulted to CZ
  (phase = π).** A semantically arbitrary module sealed because both halves shared the same default.

Two conclusions, both load-bearing:
1. **Author isolation works** — it surfaces intent ambiguity that same-context generation hides
   (3/4 caught vs 0/4 for same-context).
2. **Isolation alone is insufficient in the answer-key-free regime** — when two *same-model*
   personas converge on the same default, isolation cannot tell them apart (the B4 case). Only
   physically distinct weights (multi-model authorship) would diverge there. This is direct evidence
   that, without an answer key, **multi-model authorship is necessary, not optional**. With a clear
   intent or an answer key, a single model is sufficient (E5/E7). Risk therefore scales inversely
   with intent-specification quality.

Full data: `_workspace/EXPERIMENT-RESULTS.md` (internal).

### 8.2 Real cross-model key-free establishment (the v0.2 "remaining external dependency", now closed)

v0.2 left one honest gap: genuinely new unitaries with no pre-existing key needed **real cross-model**
authorship (physically distinct weights) to reach `MULTIMODEL` grade, and that injection had not been
done. It has now been done, in two independent rounds, with **six external runtimes**:
`openai-gpt-5 · google-gemini-3.5-flash-high · xai-grok-code-fast-1 · moonshot-kimi · alibaba-qwen ·
deepseek-v4-pro` (six distinct weight sets = six independence units).

Each runtime was given identical briefs and intent lists and asked to **independently** author, with
no sight of any other runtime's output or of any answer key:
- **Round 1 (golden):** the analytic reference unitary `U[out,in]` of each gate.
- **Round 2 (bloq):** the Qualtran *implementation* of each gate (a different runtime than the golden
  author, so a wrong implementation cannot match a wrong reference by shared origin).

The ingest pipeline hashes each submission with the oracle and counts agreement **per independence
unit** (same weights = one vote). Results (15 gates; 8 calibration gates with a known answer, 7 new
gates with none):

| Round | Check | Result |
|---|---|---|
| Golden, calibration (8) | converged hash == previously-sealed hash | **8/8** |
| Golden, new (7: s, t, cz, iswap, cs, ccz, qft4) | ESTABLISHED, MULTIMODEL grade (≥2 distinct weights) | **7/7** |
| Golden, all (15) | converged hash == stack-independent symbolic proof (`formal_spec`/sympy) | **15/15** |
| Golden code reproduction | each runtime's `golden_code` re-executed in a sandbox reproduces its own matrix | **90/90** (6×15) |
| Bloq | `bloq.tensor_contract()` == frozen consensus key, all 6 runtimes | **6/6 per gate, dissent 0** |
| Seal | golden(author G) ⊕ bloq(author B≠G) → oracle seal == frozen key | **7/7 SEALED** |

This is **triangulation — stated precisely (v0.4 calibration).** For each new gate there are **two
independent axes** (the LLM-authored analytic golden, runtime A ⊕ the Qualtran bloq, runtime B) **plus
one consistency check** (sympy symbolic proof, no LLM). The golden and the symbolic proof share the
same mathematical definition (endianness / phase convention), so a *convention* error could in
principle corrupt both at once — they are not a fully independent third axis. The genuine third axis is
recomputing the unitary on a **Qualtran-independent path**: `scripts/second_oracle.py` reconstructs each
sealed unitary in pure numpy (using neither Qualtran, nor the spec's golden code, nor the oracle's
internals) and re-checks the `u_hash` — **48/48 modules + cmul2_mod21**, closing the shared-stack risk
on the dense path. Corpus note: six LLMs agreeing on a *textbook* primitive is partly a shared-training
artifact (see the corpus-correlation analysis, §8.6), so textbook convergence is discounted and the
load-bearing credit is on hard/ambiguous intents.

**Independence was audited, not assumed:** the 6 runtimes' `construction_method` notes and
`golden_code` snippets were all textually distinct (no copy-paste), yet converged. A deliberately
endianness-broken submission injected during pipeline testing was correctly flagged as `dissent` and
outvoted, confirming the detector is live.

Honesty note on what this does and does not show: the gates here are textbook primitives that a single
competent model rarely gets wrong, so consensus is *robust* but not yet *necessary* — the decisive
stress is an ambiguous or genuinely-hard intent (E5', §8.1). What §8.2 does establish is that the
**mechanism is real and end-to-end**: six different companies' weights, plus an independent proof,
agree, and the seal is anchored to that agreement rather than to a human.

Artifacts: `_workspace/crossmodel/{RUNTIME-BRIEF,BLOQ-BRIEF,intents.json}.*`,
`_workspace/crossmodel/CONSENSUS-REPORT.json`, `.pgf/keyfree/{ingest_crossmodel,freeze_crossmodel_keys,seal_crossmodel}.py`,
`.pgf/keyfree/consensus_keys.json`.

### 8.3 Composition (F3) and the algorithm layer

With the gate library key-free, sealed modules were **recomposed** into applications using the oracle's
`app_assemble` path: a manifest declares an `app_golden` (the application's intended unitary) and a
`plan` (an ordered list of sealed sub-modules / sub-apps with wire placements); the oracle re-seals
**only if** the composition's unitary equals `app_golden` (C-app, up to global phase / 1e-9) and every
input is itself sealed (INV2). Tier-0 realizes the dense unitary; Tier-1 (structural Merkle) seals
arbitrarily large compositions without materializing 2ⁿ.

**59 applications sealed (35 algorithm-layer incl. mod 33/35 + 24 autonomously forged).** Highlights (a representative subset):

| App | n | Built from (sealed modules / sub-apps) | What it demonstrates |
|---|---|---|---|
| bell, ghz3, ghz4 | 2–4 | h, cnot | entangling primitives, scaling |
| cz/ccz/swap "rediscovered" | 2–3 | h+cnot, h+toffoli, cnot×3 | **rediscovery cross-check** (see below) |
| ghz16_structural | 16 | h, cnot | Tier-1 seal of a 2¹⁶ circuit without dense materialization |
| grover2 | 2 | cz (oracle) + diffusion → reflect00 | first real algorithm; 3-level recursive tree |
| qft2/qft3/qft4 pipeline | 2–4 | h, cs, ct, cr4, swap | textbook QFT circuit == sealed monolithic QFT |
| qpe_s, qpe_t | 3–4 | h, cz, cs, ct + inverse-QFT sub-app | Quantum Phase Estimation, 2- and 3-bit precision |
| shor15_a2 | 7 | Fredkin → cmul → iqft3 | **Shor period-finding** (see §8.4) |

**Rediscovery cross-check (a strong internal consistency proof).** Several apps reconstruct a gate that
was *independently* sealed via cross-model: e.g. `cz_rediscovered = H·CNOT·H`, `ccz_rediscovered =
H·Toffoli·H`, `swap_via_cnot = CNOT·CNOT⁻¹·CNOT`, and `qft{2,3,4}_pipeline` rebuilt from H + controlled
phases + swaps. In **6/6** such cases the composed unitary's `u_hash` equals the byte-for-byte hash of
the separately cross-model-sealed gate. The whole stack — cross-model gate truth, the composition
engine, and the oracle — is mutually consistent.

**Capability gaps were filled key-free, on demand.** Building these apps required gates not in the base
15 (controlled-T, controlled-S†, the controlled-Rₖ phase family, controlled-Rₖ†, Fredkin). Each was
established by the **same key-free mechanism** (independent `proof ⊕ structural` convergence, graded
PROOF_BACKED, zero human seed) and sealed, growing the library to **28 modules** (at the algorithm-layer
milestone; 34 after the W-state Ry primitives, §8.7). The controlled-phase
rotations are exposed as a *parametric family* `CRₖ = diag(1,1,1, e^{2πi/2^k})` (with cz=CR₁, cs=CR₂,
ct=CR₃), so arbitrary-precision QFT/QPE is a matter of sealing the next k.

### 8.4 Shor's algorithm — the capstone, with an honest decomposition

`shor15_a2` is a 7-qubit Shor period-finding circuit (3 counting + 4 work qubits) for N=15, a=2.

The critical design choice was **honesty of decomposition**. The naive way to "seal Shor" is to make
the modular-multiplication bloq a `MatrixGate` equal to its own golden — but that makes bloq ≡ golden
and **defeats the co-error firewall** (the entire point of independent author + reference). Instead we
used the structural fact that **15 = 2⁴ − 1**, so multiplication by 2 mod 15 is a **cyclic bit
rotation**, which decomposes into **sealed SWAP gates**; the controlled version is a chain of **sealed
Fredkin (controlled-SWAP)** gates. So the modular arithmetic is built from genuinely independent sealed
primitives, not from a matrix copy of the answer. *(v0.7: this discipline is now **code-enforced** — a
hollow `MatrixGate`/literal-unitary bloq is rejected by the honest-decomposition guard on both sealing
paths, §8.8 — so it is no longer only a convention.)*

The full pipeline: `H×3 · controlled-mult⁴ · controlled-mult² · inverse-QFT3`, where each
controlled-mult is a sub-app of Fredkins and inverse-QFT3 is a sealed sub-app (reusing cs†, ct†).

**Behavioral check (illustrative only — not load-bearing).** Re-materializing the sealed `app_golden`
and applying it to |1⟩ gives:

```
counting register measurement → {0, 2/8, 4/8, 6/8}, each p = 0.25  ⇒  r = 4  ⇒  15 = 3 × 5
```

⚠ **This is a sanity-check, not evidence of the seal.** `app_golden` *is* the intended unitary, so
applying it to an eigenstate only re-confirms the author wrote a correct Shor circuit — it is
circular w.r.t. the seal. The **load-bearing** checks are C-app (composition == `app_golden`, Tier-0
dense) + cross-model app consensus (§8.6). The decomposition is honest: the modular multiplication is
built from independently sealed primitives (SWAP / Fredkin chains), never a `MatrixGate` copy of the
answer.

**v0.4 capstone — N=21 = 3 × 7 with genuine modular arithmetic.** N=15 is a degenerate case: 15 = 2⁴−1
makes ×2 mod 15 a mere cyclic bit-rotation, so *every* base is cheap (NOT∘rotate). The real
quantum-hard work — a controlled modular multiplier — only appears for N ≠ 2ᵏ−1. So `shor21_a2` was
built for **N=21**: `cmul2/4/16_mod21` are honest **reversible-synthesis** multipliers (c3x/c4x/c5x
chains, ~66 gates, no MatrixGate), and `shor21_a2` is a 12-qubit Tier-0 seal where the composite
unitary equals `app_golden` over the full 2¹²=4096 dimension. The (illustrative) behavioral readout
gives continued-fraction P(r=6) ⇒ 21 = 3 × 7. This escapes the N=15 special case entirely.

Artifacts: `specs/apps/*.app.pg`, `registry/apps/*.sealed.json` (incl. `shor15_a2`, `shor15_a7`,
`shor21_a2`, `cmul*_mod21`), `.pgf/autoforge/forge_apps.py`, `.pgf/status-F3Compose.json`,
`.pgf/keyfree/seal_crk.py`, `scripts/second_oracle.py`.

### 8.5 Library-wide regression (current totals)

```
modules: 48 sealed · re-verified through the oracle (30 gates incl. c6x/MCT-6 + sx/√X; 18 ±α_k Ry
         primitives k=2..10, §8.7)
apps:    59 sealed (unique) · deterministic re-seal (u_hash identical) · 24 forged autonomously
         registry/apps holds 97 files = 59 unique app seals + 38 cached app-side module re-seals
         (canonical copy lives in registry/modules; single source of truth = REGISTRY-MANIFEST.json
          registry_root_hash 3dae613d… reproduces byte-identical; blast-radius via registry_tools.py)
rediscovery cross-checks: 6/6 byte-identical to independently sealed gates
second oracle (Qualtran-independent numpy): 48/48 modules + cmul2_mod21
frozen consensus keys: 23 (22 prior + sx live cross-model round; existing keys byte-preserved,
         contested-tie guard re-checks determinism every run)
```

### 8.6 v0.4 evidence — app-level cross-model, necessity, second oracle, goal-autonomy

**App-level cross-model corroboration (EXT v04).** Six runtimes independently authored the *application*
unitaries (not just gates). App-golden: `iqft7, cmul2/4/16_mod21` → **4/4 ESTABLISHED, MULTIMODEL**, all
byte-matching the in-house sealed apps. App-bloq (independent circuit decompositions): **4/4 ESTABLISHED**,
different circuit depths converging to the same `u_hash`; two runtimes' wrong circuits were correctly
out-voted (B4-resistance shown end-to-end). This closes the v0.3 residual that app-level intents were
in-house authored.

**Consensus *necessity* (EXT v05, true-divergence probe).** v0.3 noted consensus was *robust* but not
shown *necessary* (textbook gates rarely diverge). v0.4 probes intents that are **under-determined by
construction** (a free continuous phase / rotation angle — no unique answer): all six runtimes pick
different values → **DIVERGENT**. A single-source pipeline would have sealed one arbitrary answer;
consensus correctly refuses → escalate. This is the necessity evidence. Convention-split intents
(rotation-sign) produced genuine 3-3 / 4-2 splits; a real 3-3 tie exposed that the engine's plurality
rule would silently seal an arbitrary side, now fixed by a **contested-tie guard** (`establish_truth`
returns `CONTESTED` on a top-2 independence tie; frozen keys unaffected — all converge cleanly).
Honest negative from the earlier v04 ambiguous probe: textbook-adjacent "ambiguous" intents did **not**
diverge (shared Schelling defaults), which is why v05 uses free parameters.

**Corpus-correlation (R-I).** Distinct model weights can still share training priors, so "N models
agree" ≠ N independent confirmations. A discount `N_eff = N/(1+(N−1)ρ)` is implemented
(`scripts/corpus_discount.py`); ρ is estimated only on answer-free intents (clean signal). Measured
ρ ≈ **0.0** on v05 free-parameter intents (frontier models choose independently when there is no
correct answer), correcting an earlier contaminated upper-bound of 1.0 on textbook-ambiguous intents.
It is **analysis-only** (default ρ=0; the sealing path is unchanged, determinism preserved).

**Goal-autonomy — multi-family (R-C/F-10).** The foundry scans the registry, detects composable gaps
(including interior gaps and **new families it can bootstrap**), scores them, and seals the top
candidates autonomously (human seed 0, no new modules). v0.4 extends it beyond GHZ: a new **cluster-state**
family (h+cz, MBQC resource) was bootstrapped and `cluster3/4`, `ghz7/8` sealed autonomously, each
independently checked (cluster = stabilizer +1 eigenstate; GHZ = state anchor). A blocked family
(W-state) is honestly reported as needing an unsealed Ry primitive — the system names its own missing
prerequisite. `COMPOUNDING-CURVE.json`: 2 compounding families at marginal-new-module-cost 0; the
post-forge scan proposes the next members itself (self-growing loop). Artifacts:
`scripts/goal_autonomy.py`, `.pgf/autoforge/{GOAL-SCAN,GOAL-FORGE-RESULT,COMPOUNDING-CURVE}.json`,
`_workspace/crossmodel/EXT-V0{4,5}-INGEST-REPORT.md`, `_workspace/CORPUS-DISCOUNT-NOTE.md`.

### 8.7 v0.5–0.6 evidence — GenSkill library (generation *methods* as first-class assets)

Until v0.4 the foundry libraried only *results* (sealed unitaries); the *methods* that produced them
lived as one-off code (e.g. `goal_autonomy.gen_ghz/gen_cluster`). v0.5 promotes generation methods to a
first-class catalog (`scripts/genskills.py`): named, parametrized **GenSkills**, each with metadata
(kind, params, required sealed modules, golden-construction method) and a deterministic `make_spec(n)`.
`registry/GENSKILL-CATALOG.json` serializes the catalog as data — the method-side counterpart of
`REGISTRY-MANIFEST.json`. Eight skills ship (v0.6): `ghz_linear`, `cluster_line` (byte-frozen — they
authored already-sealed families), `cluster_ring`, `wstate_cascade`, `modmul_synth`, and the
analytic-golden `zpow_phase`/`crk_phase`/`qft_dft` (detailed under *v0.6 additions* below).

**The boundary is explicit: generation ≠ verification.** A GenSkill mints no trust — its output is a
*candidate* spec that still must pass the `app_assemble` oracle (C-app) to be sealed. The library is a
reuse / introspection / provenance layer only.

**Determinism is enforced as the acceptance test** (`python scripts/genskills.py selftest` → 50/50):
(i) *byte-identity* — frozen skills regenerate committed specs byte-for-byte (16 skill-authored
members); two legacy-format members (`ghz3/4`, authored by an earlier generator) are byte-exempt and
instead verified by (ii); (ii) *reproduce-seal* — every family member reassembles (temp store) to a
`u_hash` **identical to the registry seal**, proving the library reproduces the foundry's actual sealed
output regardless of spec-text format; (iii) *new-method/new-synth seals* — `cluster_ring ring4`,
`cmul8_mod21`, and the W-state apps all seal Tier-0 EXACT through the oracle. The registry, seals, and
frozen keys are untouched (temp store, scratch specs removed). `goal_autonomy.py` was rewired to
*consume* genskills (inline generators removed → import), confirming behavior preservation.

**v0.6 additions — the library became self-extending.**

- **Arithmetic-synthesis (`modmul_synth`).** Given `(a, N, nq)` it builds the controlled-(×a mod N)
  permutation (arithmetic, identity out-of-range — no MatrixGate) and synthesizes it via **MMD
  transformation-based reversible synthesis** into sealed multi-controlled-Toffolis (`toffoli/c3x/c4x/c5x`,
  ≤5 controls, q0 automatically in every control because the off-control block is identity). It
  reproduces all six committed multipliers' sealed unitaries (`cmul2/4/16_mod21`, `cmul2/4_mod15`
  exactly; `cmul7_mod15`'s committed artifact used an N=15-degeneracy `NOT∘rot3` decomposition that
  differs only on the two *unused* boundary states {0, 2⁴−1} — algorithm-equivalent on the orbit
  1..N−1, an honest documented variant) and synthesizes new ones on demand. This is the controlled-U
  *generation method* behind Shor, captured as a reusable skill.
- **Continuous-rotation W-states (`wstate_cascade`, prerequisite `gen_ry_module`).** The first
  algorithm-level states requiring **irrational rotation angles**. A parametrized Ry primitive
  `ry_k{k}(±α_k)`, α_k = arccos√(1/k), is sealed as a normal gate: bloq = `YPowGate`, golden = standard
  `Ry`; the YPowGate↔Ry global phase is a *scalar* so a cascade of them factors to a single global
  phase that C4 ignores. `gen_wstate(n)` prepares |W_n⟩ by an `X · CRy(α_k) · CNOT` cascade
  (CRy decomposed into the sealed ±α_k Ry + CNOT). W₃–W₁₀ sealed Tier-0 and independently verified
  (uniform 1/√n amplitudes). The Ry primitives are **family-reused**: W_{n+1} = W_n's modules + the two
  new ±α_{n+1} gates — marginal cost 2 modules/n, the system naming `ry_k{n+1}` as the prerequisite.
- **Analytic-golden gate methods (`zpow_phase`, `crk_phase`, `qft_dft`).** Capture the closed-form
  *construction methods* behind gate modules: Z^t phase = diag(1, e^{iπt}) (z/s/t), controlled-R_k =
  diag(1,1,1, e^{±2πi/2^k}) (cz/cs/ct/cr4–7 + daggers), and the n-qubit DFT (qft2–4). Each pairs an
  analytic golden with a qualtran bloq; the skill reproduces **17 committed gate modules' sealed
  u_hashes** (bloq==golden under C4), capturing the result-library's gate generation as data.
- **Method self-seal.** `GENSKILL-CATALOG.json` now carries a per-skill `source_hash` (sha256 of the
  generator's source + metadata), a `catalog_root_hash`, and a `library_file_hash` — the **method-side
  counterpart of `registry_root_hash`**. `genskills.py verify` recomputes and flags any drift
  (tamper-evident generation methods, not just tamper-evident results).
- **Goal-autonomy unmanned loop-to-frontier (`goal_autonomy.py loop`).** Repeats scan→forge until a
  round seals nothing new, then reports the frontier blockers. From the GenSkill-supplied methods it
  autonomously sealed **24 applications** (ghz9/10, cluster5–10, ring3–10, wstate3–10) at **human seed 0,
  zero new modules** beyond the Ry primitives, halting honestly when every family reaches MAX_N=10 (no
  blockers left after the ry_k5–10 primitives were sealed). This is the self-growing loop reaching the
  edge of its current methods; *open-ended discovery of genuinely new methods/families remains
  research-stage* (the loop recomposes known methods, it does not invent new mathematics).

**Scope (honest).** Still not captured as skills: permutation/arbitrary-isometry golden recipes, and
autonomous *creation* of new primitive modules (the loop names missing prerequisites but a
human/next-autonomy-level still seals them — preserving the loop's "zero new modules" invariant).
Artifacts: `scripts/genskills.py`, `registry/GENSKILL-CATALOG.json`,
`.pgf/autoforge/{GOAL-SCAN,GOAL-FORGE-RESULT,GOAL-LOOP-RESULT,COMPOUNDING-CURVE}.json`,
`_workspace/GENSKILL-LIBRARY-NOTE.md`.

### 8.8 v0.7 evidence — tier routing, distinct-prime arithmetic, live panel, falsification, closure

Every item below is reproduced from the working tree; all are **non-destructive** (existing
`sealed.json` byte-identical, frozen keys append-only, `registry_root_hash 3dae613d…` unchanged) and
use the oracle/consensus **only** (no reimplementation). Each sub-phase was re-designed as its own
sub-PG before execution.

- **P0 — Clifford → Tier-2 routing** (`scripts/clifford_routing.py`, `.pgf/clifford/`). The one app
  that previously held only a STRUCTURAL (Tier-1) seal, `ghz16`, now also carries a stabilizer-tableau
  **Tier-2** seal (via the oracle's `clifford_seal`), closing the sole weak-guarantee gap. The Tier-2
  `u_hash` ≠ the dense `u_hash` by construction (the oracle says so); this is a **companion** seal, not
  a replacement, added additively to `SEMANTIC-GUARANTEES.json` (other entries byte-unchanged). 28/28
  Clifford-only apps cross-validated dense == registry; `ghz20` (n>EXACT_BOUND) tableau-sealed as a
  scale demonstration.

- **P1 — distinct-prime arithmetic** (`scripts/arith_family.py`, `.pgf/arith/`). Sealing the Shor
  targets 33 = 3×11 and 35 = 5×7 required a 6-control multiply-controlled-X (`c6x`/MCT-6) that the
  prior library (≤ MCT-5) lacked. **Honest finding:** "infinite reuse of one engine" has a limit — a
  new primitive opens a family. Resolution: seal `c6x` key-free, then *evolve* the GenSkill engine
  (`modmul_synth` gains the MCT-6 path) and re-stamp the method self-seal. `cmul2_mod33`/`cmul2_mod35`
  sealed Tier-0 EXACT; behavioral orbit period == ord_N; full Shor at these N (≥14 qubits) is honestly
  labelled Tier-1.

- **P2 — gated multi-model panel + first *live* cross-model truth** (`scripts/{gated_panel,
  live_dispatch,seal_sx}.py`, `.pgf/panel/`). A dispatch policy classifies intent risk and **structurally
  requires ≥2 distinct-weights model units** (grade floor MULTIMODEL) for key-free/ambiguous intents,
  closing the B4 same-weights co-error defect; validated by **replaying the EXT v05 6-runtime data**
  (free-parameter → DIVERGENT, sanity → SEAL, convention 4-2 → SEAL / 3-3 ry → CONTESTED) with zero new
  calls, plus a falsification probe (naive count SEALs a B4 block; the gated path REJECTs). Then the
  **first genuinely live** key-free truth: a *new* intent `sx` (√X) was authored independently by the
  six runtimes, all converged (MULTIMODEL), and the converged hash — triangulated by an algebraic
  proof (PROOF_BACKED) — was sealed as module `sx` (Tier-0, `XPowGate(0.5)`) with a frozen consensus
  key appended (existing keys byte-preserved).

- **P3 — falsification front** (`scripts/red_team.py`, `.pgf/redteam/`). The oracle/gate/consensus are
  attacked adversarially: golden self-reference, identity golden, ancilla-leak (C3), convention-split
  (DIVERGENT), and B4 co-error are all caught (5/6); the §7-flagged top risk is confirmed by a true
  falsification — a mis-wired but structurally-valid app **does** seal at Tier-1 STRUCTURAL while the
  golden-bearing Tier-0 C-app rejects it (so the teeth live in dense/Tier-0 and Clifford/Tier-2, exactly
  as `semantic_guarantee` labels). The one documented gap — **honest decomposition is a social
  convention, not code-enforced** — was then closed (next bullet).

- **Honest-decomposition closure** (`.agents/skills/qpgf-oracle/scripts/decomp_guard.py`,
  `scripts/{seal_module,verify_t1_closure}.py`, `.pgf/bounty/T1-CLOSURE.json`). A "hollow seal" — a
  custom bloq that asserts a *literal* unitary (overriding `tensor_contract`, or building from a raw
  matrix via `MatrixGate`/`from_unitary`) instead of honestly decomposing into primitives — passes C4
  because golden == the asserted matrix. A policy-layer guard rejects it (dynamic: the bloq's type must
  originate from `qualtran`/`cirq`, not a spec-defined class; static AST: no unitary-method override /
  monkey-patch / literal-matrix gate). Wired into `spec_quality_guard`, it enforces on **both** the
  module-seal and the app-seal (`app_assemble`) paths. Critically, it lives **outside the fingerprinted
  oracle** (`verify_seal.py`/`contracts.py` are the only files hashed into each seal's signature), so
  all 48 modules + 59 apps re-seal **byte-identical** (`reproduce_all` root unchanged) while 6
  independently-authored hollow attacks and the original MatrixGate vector are rejected.

- **Cross-model adversarial + cross-runtime co-error rounds** (`scripts/{bounty_adjudicate,
  cross_runtime_round}.py`, `_workspace/crossmodel/p3d_*`). Re-using the six-runtime relay as an
  *adversarial* panel: round-1 attack submissions, re-adjudicated deterministically by the oracle,
  reduced to **zero real breaks** once independence units are provenance-bound to the submitting runtime
  (forged "peer" labels collapse) and the hollow-decomposition pattern is recognized. Then a sequence of
  cross-runtime rounds tested genuine corpus-correlation co-error: on five convention-sensitive but
  well-defined gates (qubit-ordering, half-angle, adjoint sign, iSWAP phase) all six runtimes converged
  on the *correct* answer (no co-error). On a genuinely **convention-contested** intent (2-qubit QFT,
  where the bit-reversal-swap convention legitimately splits the literature) the six runtimes split
  2-2-1-1 → top-2 tie → **CONTESTED**: the near-tie guard refused to seal an under-specified intent —
  the **first real multi-model exercise** of that guard (previously only self-tested). `√SWAP` and
  `Rz(π/2)` split 4-2 and the majority landed on the *standard* convention → ESTABLISHED MULTIMODEL with
  the minority recorded as a documented variant (mirroring the v05 convention-split pattern).

---

## 9. Honest limitations & threats (please attack these)

1. **Same-weights co-error (b) in the answer-key-free regime.** For genuinely *new* unitaries with no
   pre-existing key, cross-persona isolation does **not** fully protect against both personas (same
   base model) misreading the intent identically. Persona-A (adversary vote) and/or a one-time human
   seed and/or a real cross-model author are the proposed mitigations — **none is proven yet.** Is the
   adversary-vote sufficient? How would you measure its residual risk?
   *Now empirically confirmed (experiment E5', case B4, §8.1): two isolated same-model personas both
   defaulted to CZ and sealed a semantically arbitrary `cphase_amb` module. A same-model Persona-A
   also diverged ({π/4, π/2}) rather than correcting the golden — so a same-model adversary vote is
   demonstrably insufficient here; cross-model divergence is what's needed.*
   ***Resolved for the library (v0.3, §8.2): real cross-model authorship is now in place — 6 distinct
   weight sets plus a stack-independent symbolic proof must converge before a key is frozen. Same-model
   defaults can no longer freeze a key (they are one independence unit). The open part is purely about
   harder intents, not about the mechanism.***
1b. **Dependency-level co-error (d).** Both personas use the same Qualtran/numpy stack. A shared
   library bug or convention could make a wrong unitary pass C4 vacuously — and the answer key itself,
   if seeded on the same stack, would be co-contaminated. Mitigation: the proof source in
   KeyFreeConsensus is **sympy-symbolic (stack-independent)**, so `model ⊕ proof` convergence is
   strictly stronger evidence than `model ⊕ model`.
2. **Answer-key seeding is a human trust anchor.** The 5 new base keys were originally fixed by a
   human-trusted deterministic computation. For trivial textbook gates this is defensible; it does
   **not** generalize to non-trivial new modules.
   *Update (v0.2): the 8 base keys are re-established **autonomously** by independent-source consensus
   (`model ⊕ proof` convergence, KeyFreeConsensus — §10), matching the human seed byte-for-byte.*
   ***Update (v0.3): the "remaining external dependency" — real cross-model injection — is now done
   (§8.2). All 22 library modules are anchored to either a known QPGF key, or cross-model consensus +
   symbolic proof, or (for the controlled-phase/Fredkin family) independent `proof ⊕ structural`
   convergence. No library module's key is a bare human assertion.***
3. **Seal ≠ cryptographic forgery proof.** Trust is conditional on verifier integrity + central
   recomputation (§5). A compromised oracle bundle that still passes `BUNDLE.sha256` (e.g. a coordinated
   tamper) would defeat this. Sigstore relocates but does not remove the trust root.
4. **Intent ambiguity.** Both personas receive the same intent text. A wrong-but-shared interpretation
   of the *intent* (e.g. endianness, phase convention) is not caught unless it changes the `u_hash`
   away from the key. For keyed modules this is closed; for unkeyed modules it is open.
5. **Tier-3 conservatism.** ZX-based sealing may *fail to seal* correct circuits (false negatives).
   This is safe (never a false positive) but limits coverage; the boundary is not characterized here.
6. **Single base model for both personas.** AutoForge's personas are the same model family. *v0.7
   addresses this for truth establishment:* a gated multi-model panel structurally requires ≥2
   distinct-weights units, and the live `sx` round established a new truth from six genuinely distinct
   runtimes (§8.8). The residual question is whether AutoForge's *generation* personas (vs the
   *establishment* panel) should also be multi-model — orchestration cost vs marginal benefit.
7. **Scope of evidence.** *v0.1 proved the loop on 8 small Tier-0 gates. v0.4–0.7 now exercise
   composition (F3) end-to-end (59 apps incl. genuine N=21 Shor and distinct-prime mod 33/35),
   Tier-1 large-N (ghz16) plus its Tier-2 closure, app-level cross-model establishment, consensus
   necessity, live multi-model truth, falsification/red-team, and goal-autonomy family extension.*
   What remains **not** done: autonomous
   *goal* selection (the system deciding what to build next), Tier-3 (Clifford+T / ZX) sealing of the
   apps, and a multi-model panel for *app-level* bloqs (app implementations are still authored
   in-house even though gate implementations are cross-model). Hard-intent stress (beyond E5') is also
   still thin — the algorithm library is correct but the gates are textbook-easy.
8. **App-golden legitimacy.** *Closed for the current library (v0.3, Round 4).* Gate goldens are
   cross-model (§8.2); app *intents* (`app_golden`) were cross-model corroborated for the simple apps
   (Round 3, 8 apps) and for the **algorithm layer** (Round 4: iqft2/3, qpe_s/t, cmul2/4_mod15,
   **shor15_a2**) — 6 independent runtimes authored each full app unitary, **7/7 ESTABLISHED MULTIMODEL**,
   matching the sealed apps. App *implementations* were also cross-model'd in the same round (app-bloq:
   4 runtimes authored independent circuits from the sealed-gate vocabulary; **7/7** converged on the
   sealed unitary; for every app **app-golden consensus = app-bloq consensus = sealed u_hash**, a
   three-path agreement). Two honest signals worth noting: (i) a real runtime's wrong circuits (an
   `iqft2`/`qpe_s` control-qubit slip) were caught as `dissent` and outvoted — the implementation-side
   firewall is live; (ii) three runtimes independently found a **shorter** `cmul4` decomposition
   (2 Fredkins vs the in-house 6) computing the identical unitary — independent implementations, not
   copies. The residual gap is narrow: the bloq round had 4 distinct weights (two runtimes skipped it),
   and the gates remain textbook-easy.

---

## 10. Autonomy: how far it can and should go

Two distinct levels:

- **Operational autonomy (the *how*)** — generate → verify → seal → register with no human. **Achieved**
  for base modules (§8). The oracle's deterministic termination is the safety belt: an autonomous loop
  cannot emit an unverified artifact, because sealing is the only exit.
- **Goal autonomy (the *what*)** — the system decides which module/app to build next by scanning the
  registry for useful compositions. **MVP built (v0.4)**, scoped honestly: it does *family extension*
  over known composition rules (GHZ, cluster), not open-ended discovery of new mathematics. It detects
  gaps (incl. bootstrapping new families and naming missing prerequisites), scores them, and seals the
  top candidates with zero human seed (§8.6). This is the foundry starting to become self-growing — not
  a "fully autonomous quantum scientist." As of v0.5 goal-autonomy draws its construction methods from
  the **GenSkill library** (§8.7) rather than embedding them, so a method added to the catalog becomes
  available to the autonomous loop — coupling the *what* (goal autonomy) to a reusable *how*. v0.6 adds an
  **unmanned loop-to-frontier** (`goal_autonomy.py loop`): it recomposes sealed modules round after round
  until every gap is done or blocked (18 apps forged autonomously, human seed 0), then halts and names its
  own missing prerequisites. The honest boundary stays sharp: the loop *exhausts known methods*; inventing
  new methods/families (or autonomously sealing new primitive modules) is the next, research-stage step.

**Key-free truth establishment (v0.2, prototyped).** The v0.1 recommendation was "human seeds the
first key, machine compounds after." v0.2 replaces the human seed with **KeyFreeConsensus**: a truth
is established when **independent sources converge on the same `u_hash`**, where independence is
counted per *physical unit* — same-weights / same-tool sources collapse to **one** vote. Demonstrated:

- The 8 base keys are re-established autonomously by `model ⊕ proof` convergence (sympy-symbolic proof
  is stack- and model-independent), grading **PROOF_BACKED**, with **zero human seed** — and they
  match the prior human seeds byte-for-byte.
- The **B4 failure is structurally rejected**: two same-model personas that both default to CZ count
  as one independence unit (< N) → `DIVERGENT`, so an arbitrary default never freezes into a key.
- Ambiguous intent (`cphase_amb`) returns `DIVERGENT` / escalation rather than a false key — "if it
  doesn't converge, there is no truth yet."

**Update (v0.3): this is no longer a prototype.** Real cross-model injection has been performed — 6
independent runtimes authored every base gate's golden and bloq, all reaching `MULTIMODEL` grade and
corroborated by symbolic proof (§8.2). The on-demand gates needed for the algorithm layer
(controlled-phase family, Fredkin) were each established by `proof ⊕ structural` convergence and
sealed. The full library (48 modules → 59 apps → genuine N=21 Shor) therefore stands on **zero
human-asserted answers**, including the first *live* cross-model truth `sx` (√X, §8.8). See
`.pgf/DESIGN-KeyFreeConsensus.md`, `consensus.py`, `_workspace/crossmodel/`.

**Update (v0.4): both residuals are now addressed.** (i) App-level intents are cross-model corroborated
(EXT v04: app-golden 4/4 + app-bloq 4/4, §8.6). (ii) Consensus *necessity* is demonstrated by the
true-divergence probe (EXT v05): free-parameter intents diverge, so a single source would have sealed an
arbitrary answer (§8.6). What remains genuinely open: first-principles *intent-text-only* app
establishment at scale, and broader hard-intent coverage beyond the probe set.

The reason this architecture is unusually *safe* for autonomy: the classic failure mode of autonomous
AI loops — "the AI declares victory and runs away" — is structurally impossible here, because the AI
**cannot** declare success; only deterministic code can.

---

## 11. Prior art and honest positioning

**Novelty, narrowed to a feature matrix** (so reviewers can attack the exact claim, not a vague one):

| Capability | VOQC/Qbricks | MQT QCEC | LLM gen (QUASAR/Agent-Q) | QuantaFoundry |
|---|---|---|---|---|
| Deterministic phase-aware equivalence | ✓ | ✓ | ✗ | ✓ (reused) |
| AI-loop **termination oracle** (exit-code = loop end) | ✗ | ✗ | ✗ (RL/sim reward) | ✓ |
| Binary **tamper-evident seal** | ✗ | ✗ | ✗ | ✓ |
| **Sealed registry** with compose invariants | ✗ | ✗ | ✗ | ✓ |
| FTQC **resource** accounting in the seal | ✗ | partial | ✗ | ✓ (field present; schema WIP) |
| **Autonomous author isolation** (persona/cross-model) | ✗ | ✗ | ✗ | ✓ |
| **Key-free consensus** truth establishment | ✗ | ✗ | ✗ | ✓ (realized, 6 runtimes + proof) |
| **Sealed compose → algorithm** (Grover/QFT/QPE/Shor from sealed parts) | ✗ | ✗ | ✗ | ✓ |

The claim is **not** a new verification algorithm; it is the **combination** in the last six rows as
one system. No single prior tool occupies that combination.

Deterministic, phase-aware quantum verification is **not new**: VOQC/SQIR and Qbricks (Coq matrix /
path-sum semantics), MQT QCEC (decision-diagram + ZX equivalence). QPGF **reuses** the tableau / ZX
techniques. What has no single-tool precedent is the **combination**: an AI-autonomous-loop
**termination oracle** + binary tamper-evident **seal/registry** + **FTQC resource** accounting as one
system. Generation-side LLM work (QUASAR, Agent-Q) uses simulator/RL reward with no binary seal or
registry. AutoForge adds **autonomous author isolation via personas** on top of that.

---

## 12. Repository layout (what a reviewer can open)

```
QuantaFoundry/
  docs/QuantaFoundry-Technical-Spec.md   # this document
  README.md                              # vision + trust model (English)
  specs/modules/*.pg                     # 48 sealed base-module specs (incl. c6x/MCT-6, sx/√X, ±α_k Ry k=2..10)
  specs/apps/*.app.pg                    # 59 sealed application manifests (app_golden + plan)
  registry/modules/*.sealed.json         # 48 registered module seals (INV1-3)
  registry/apps/*.sealed.json            # 59 app seals (C-app) + 38 cached leaf-module re-seals (97 files)
  registry/{REGISTRY-MANIFEST,DEPENDENCY-GRAPH,SEMANTIC-GUARANTEES}.json  # registry as first-class data (v0.4)
  registry/GENSKILL-CATALOG.json         # generation-method library as first-class data (v0.5)
  .pgf/
    DESIGN-AutoForge.md / DESIGN-KeyFreeConsensus.md   # PG/PGF designs
    status-AutoForge.json / status-KeyFreeConsensus.json / status-F3Compose.json
    personas/{persona-golden,persona-bloq,persona-adversary}.md
    autoforge/autoforge.py               # F2 gate orchestrator
    autoforge/forge_apps.py              # F3 composition driver (apps + rediscovery cross-check)
    keyfree/consensus.py                 # KeyFreeConsensus engine + source generators
    keyfree/ingest_crossmodel.py         # Round 1/2 gate consensus ingest
    keyfree/ingest_app_golden.py         # Round 3 app-intent consensus ingest
    keyfree/{freeze_crossmodel_keys,seal_crossmodel,seal_crk}.py
    keyfree/consensus_keys.json          # frozen, provenance-tagged keys (15: 8 base + 7 cross-model)
  scripts/                               # v0.4 tooling (NOT the oracle; analysis/autonomy)
    second_oracle.py                     # Qualtran-independent re-check (48/48)
    goal_autonomy.py                     # registry scan → gap detect → autonomous seal (consumes genskills)
    genskills.py                         # GenSkill library: generation *methods* as a catalog (v0.5)
    semantic_guarantee.py                # per-seal guarantee layer + ghz16 partial verification
    corpus_discount.py / verify_contested_guard.py
    sync_qpgf.py                         # QPGF vendor: stamp/check (provenance + seal-invariance gate)
  _workspace/crossmodel/                 # cross-model briefs, submissions, consensus reports (v04, v05)
  .agents/skills/qpgf-oracle/            # vendored QPGF oracle (used, not modified)
    VENDOR.json                          # consumption=vendored; upstream v0.1.0/commit, bundle root, deps, fingerprint
    scripts/{verify_seal,registry,app_assemble,contracts,bundle_manifest,verify_bundle,zx_seal}.py
    references/{contract-spec,oracle-usage,DEPLOYMENT-TRUST}.md ; examples/*.pg
```

> **QPGF consumption = vendored** (decided 2026-06-27). The oracle source is copied into the repo, not a
> submodule or pip dependency, so a sealed artifact and the exact oracle code that sealed it live in the
> same commit — reproducible by checkout, no environment reconstruction. Because `oracle_fingerprint` is
> bound into every seal signature, an oracle/dependency change can alter seal u_hashes; automatic syncing
> would risk that silently, so syncing is deliberate and gated. `VENDOR.json` records provenance (upstream
> tag/commit, `BUNDLE.sha256` root, `DEPENDENCIES.lock`, fingerprint); `scripts/sync_qpgf.py check`
> verifies vendor integrity, dependency match, and **seal-u_hash invariance** before any oracle upgrade is
> committed (a semver-gated event).

Reproduce the evidence:
```
python .agents/skills/qpgf-oracle/scripts/bundle_manifest.py --verify   # bundle_ok: 52 files
python .agents/skills/qpgf-oracle/scripts/test_verify_seal.py           # 11 PASS / 0 FAIL
python .pgf/autoforge/autoforge.py                                      # base gates SEALED
python .pgf/keyfree/ingest_crossmodel.py                                # cross-model consensus (needs submissions/)
python .pgf/autoforge/forge_apps.py                                     # apps SEALED · rediscovery 6/6
python scripts/second_oracle.py                                        # Qualtran-independent 48/48
python scripts/goal_autonomy.py scan                                   # autonomous gap detection (families)
python scripts/goal_autonomy.py loop                                   # unmanned forge-to-frontier (self-growing)
python scripts/genskills.py verify                                     # method self-seal (tamper-evident)
python scripts/genskills.py selftest                                   # GenSkill library determinism 50/50
python scripts/semantic_guarantee.py                                   # per-seal guarantees + ghz16 partial verify
```

---

## 13. Review questions (what we want answered)

Please address as many as you can, and add flaws we did not anticipate.

**Trust model**
1. Is the decomposition of co-error into (a) same-context and (b) same-weights correct and complete?
   Is there a third failure mode we are missing?
2. In the answer-key-backed regime, do you agree cross-persona has *zero* trust loss vs cross-model?
   If not, give a concrete counterexample where a wrong module gets sealed.
3. How would you defeat the answer-key anti-swap check? Assume you control both personas but not the
   oracle bundle.

**Autonomy & golden legitimacy**
4. For an *unkeyed* new unitary, is the Persona-A adversary vote (independent re-derivation, 2-of-2)
   strong enough? Propose a measurable acceptance bound for "independent enough."
5. Is the "human seeds the first key, machine compounds after" policy a sound trust boundary, or a
   hidden single point of failure? Is there a key-free first-establishment protocol?
6. Should the personas be a true multi-model panel rather than one base model? Quantify the expected
   benefit vs cost.

**Oracle & determinism**
7. Are there inputs for which byte-identical reproduction could silently break (locale, numpy version,
   complex-zero sign, ordering)? How would you test for it adversarially?
8. Is folding `oracle_code_hash`/`contracts_code_hash` into the signature sufficient provenance, or
   can a tampered-but-self-consistent bundle pass? What would you add?

**Architecture & scope**
9. The compounding thesis (§4) assumes composition (F3) preserves correctness via C-app + INV3, now
   exercised on 59 apps incl. recursive trees and the 12-qubit N=21 Shor (§8.3–8.4). Is re-verification of
   every composition sufficient, or are there composition patterns (heterogeneous, recursive,
   uncompute) where C-app could pass while the app is semantically wrong?
10. Given only this spec, what is the single highest-risk assumption in the whole design, and what
    one experiment would most cheaply falsify it?

**Cross-model & algorithm layer (v0.3)**
11. §8.2 triangulates each gate via golden(model A) ⊕ bloq(model B) ⊕ proof(sympy). Is three
    independent paths to one hash a sound definition of "established truth," or can you construct a
    correlated failure across all three (e.g. a shared numerical convention in numpy/Qualtran/sympy)?
12. The Shor decomposition (§8.4) deliberately avoids a `MatrixGate` modular-multiplier so that bloq ≠
    golden. But it exploits 15 = 2⁴−1 (mult-by-2 = bit rotation). Is this a fair demonstration of
    "compose Shor from sealed parts," or does the special structure of N=15 hide the real difficulty
    (general modular arithmetic)? What is the smallest N that would make this honest *and* hard?
    *(v0.7 partial answer, §8.8: distinct-prime multipliers `cmul2_mod33` (3×11) and `cmul2_mod35`
    (5×7) were sealed via genuine reversible synthesis — which forced a new MCT-6 primitive `c6x` —
    so the N=15 cyclic shortcut no longer carries the arithmetic; full distinct-prime Shor at these N
    is ≥14 qubits and currently Tier-1.)*
13. App intents (`app_golden`) for QPE/Shor are in-house authored (§9.8). What is the cheapest protocol
    to make app-level intent cross-model, and does the rediscovery cross-check (§8.3) already provide
    equivalent assurance for the apps that rebuild a separately-sealed gate?

---

*End of specification. Reviews, counterexamples, and falsifications are the desired output.*
