# QuantaFoundry — Technical Specification

> **Version:** 0.3 (adds real cross-model key-free establishment, F3 composition, and the full
> algorithm layer up to Shor) · **Date:** 2026-06-27
> **Audience:** AI runtimes and engineers performing an independent design review.
> **Status of claims:** every result in §8 is reproduced from the working tree; "planned" items are marked.
> **What changed since v0.2:** the "remaining external dependency" of v0.2 — real cross-model
> authorship — is now **done** (6 independent runtimes, §8.2). Composition (F3), called "the next
> thread, not yet exercised" in v0.1, is now realized end-to-end: **22 sealed modules → 20 sealed
> applications**, culminating in a **Shor period-finding circuit that factors 15 = 3 × 5**, every
> primitive established with **zero human answer keys** (§8.3–8.4).

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
applications (each re-verified and re-sealed). As of v0.3 all four functions are realized: the library
holds **22 sealed base modules** and **20 sealed applications**, the latter built entirely by
recomposing the former — up to a **Shor period-finding circuit that factors 15 = 3 × 5**.

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
   re-verified against the contract oracle. The library grew from 22 verified gates to 20 verified
   applications including Grover, QFT(2–4), Quantum Phase Estimation, and **Shor period-finding**,
   with every new primitive (controlled-phase family, Fredkin) also established key-free (§8.3–8.4).

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
2. **Verify & seal → store.** A deterministic oracle checks contracts C1–C4, selects a seal tier,
   and emits `<id>.sealed.json` iff the candidate passes. Sealed artifacts are admitted to the
   registry under invariants INV1–3.
3. **Compose → new output.** Sealed modules are assembled into larger apps; the composite is given
   its own reference check (C-app) and must itself pass function 2 to be sealed. Its output re-enters
   function 2, so **the output of 3 becomes new raw material for 1/3** — a self-growing loop.

**The meaning of accumulation.** Sealing is not storage; it is **trust-capital formation**. The
verification cost is paid once and the result is reusable forever (deterministic, byte-identical on
recompute). N sealed modules yield a combinatorially larger space of composable apps, so production
capacity grows *non-linearly* with the registry. This is the economic reason the base-module library
(thread C) is the first deliverable: compounding needs principal first.

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

| Tier | Range | Method | Status |
|---|---|---|---|
| 0 EXACT | small | dense tensor contraction == golden | realized |
| 1 STRUCTURAL | large composition trees | Merkle hash of sealed children (no dense matrix) | realized |
| 2 CLIFFORD | large Clifford | stabilizer tableau, O(n²) | realized |
| 3 CLIFFORD+T | large universal | ZX-calculus equivalence to an independent golden circuit (pyzx) | realized, conservative |

All tiers are **exact, not approximate**. Tier-3 is **sound but conservative**: it seals only when ZX
*proves* equivalence; non-reduction is rejected, never wrongly sealed. (The 8 base modules in §8 are
all Tier-0 EXACT.)

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
| autonomy | blocked (human) | **fully autonomous** |

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

This is **triangulation**: for each new gate, three *independently produced* artifacts — the analytic
golden (runtime A), the Qualtran bloq (runtime B), and a symbolic proof (sympy, no LLM) — all map to
the **same** `u_hash`. A co-error would have to corrupt all three independent paths identically.

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

**20 applications sealed.** Highlights:

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
PROOF_BACKED, zero human seed) and sealed, growing the library to **22 modules**. The controlled-phase
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
primitives, not from a matrix copy of the answer.

The full pipeline: `H×3 · controlled-mult⁴ · controlled-mult² · inverse-QFT3`, where each
controlled-mult is a sub-app of Fredkins and inverse-QFT3 is a sealed sub-app (reusing cs†, ct†).

**Behavioral verification of the *sealed* app** (not a separate simulation — the sealed `app_golden`
re-materialized and applied to the work eigenstate |1⟩):

```
counting register measurement → {0, 2/8, 4/8, 6/8}, each p = 0.25
⇒ estimated period r = 4
⇒ gcd(2^(4/2) − 1, 15) = 3,  gcd(2^(4/2) + 1, 15) = 5
⇒ 15 = 3 × 5
```

The sealed artifact does not merely *type-check*; it **factors 15**. And every gate it rests on —
including the controlled-phase family and Fredkin — was established without a single human-asserted
answer key.

Artifacts: `specs/apps/*.app.pg` (20 manifests), `registry/apps/*.sealed.json`,
`.pgf/autoforge/forge_apps.py`, `.pgf/autoforge/FORGE-APPS-RESULT.json`, `.pgf/status-F3Compose.json`,
`.pgf/keyfree/seal_crk.py`.

### 8.5 Library-wide regression (current totals)

```
modules: 22 sealed · re-verified through the oracle 22/22
apps:    20 sealed · deterministic re-seal (u_hash identical) 20/20
rediscovery cross-checks: 6/6 byte-identical to independently sealed gates
```

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
6. **Single base model for both personas.** All personas are currently the same model family. A real
   multi-model panel would strengthen (b) but reintroduces orchestration cost. Worth it?
7. **Scope of evidence.** *v0.1 proved the loop on 8 small Tier-0 gates. v0.3 now exercises
   composition (F3) end-to-end (20 apps incl. Shor), Tier-1 large-N (ghz16), the cross-model
   establishment, and the controlled-phase parametric family.* What remains **not** done: autonomous
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
- **Goal autonomy (the *what*)** — the system decides which module/app to build next (e.g. by scanning
  the registry for useful compositions). **Not yet built**; this is where the foundry becomes
  self-growing.

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
sealed. The full library (22 modules → 20 apps → Shor) therefore stands on **zero human-asserted
answers**. See `.pgf/DESIGN-KeyFreeConsensus.md`, `consensus.py`, `_workspace/crossmodel/`.

The honest residual is now narrower: (i) *app-level* intents for the most complex apps (QPE, Shor) are
still in-house authored (§9.8), and (ii) the gates exercised are textbook-easy, so consensus is robust
but not yet proven *necessary* on a hard intent.

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
  specs/modules/*.pg                     # 22 sealed base-module specs
  specs/apps/*.app.pg                    # 20 sealed application manifests (app_golden + plan)
  registry/modules/*.sealed.json         # 22 registered gate seals (INV1-3)
  registry/apps/*.sealed.json            # 20 app seals (C-app) + cached leaf-module re-seals
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
    keyfree/consensus_keys.json          # frozen, provenance-tagged keys (22)
  _workspace/crossmodel/                 # cross-model briefs, submissions, consensus reports
  .agents/skills/qpgf-oracle/            # vendored QPGF oracle (used, not modified)
    scripts/{verify_seal,registry,app_assemble,contracts,bundle_manifest,verify_bundle,zx_seal}.py
    references/{contract-spec,oracle-usage,DEPLOYMENT-TRUST}.md ; examples/*.pg
```

Reproduce the evidence:
```
python .agents/skills/qpgf-oracle/scripts/bundle_manifest.py --verify   # bundle_ok: 52 files
python .agents/skills/qpgf-oracle/scripts/test_verify_seal.py           # 11 PASS / 0 FAIL
python .pgf/autoforge/autoforge.py                                      # base gates SEALED
python .pgf/keyfree/ingest_crossmodel.py                                # cross-model consensus (needs submissions/)
python .pgf/autoforge/forge_apps.py                                     # 20/20 apps SEALED · rediscovery 6/6
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
   exercised on 20 apps incl. recursive trees and the 7-qubit Shor (§8.3–8.4). Is re-verification of
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
13. App intents (`app_golden`) for QPE/Shor are in-house authored (§9.8). What is the cheapest protocol
    to make app-level intent cross-model, and does the rediscovery cross-check (§8.3) already provide
    equivalent assurance for the apps that rebuild a separately-sealed gate?

---

*End of specification. Reviews, counterexamples, and falsifications are the desired output.*
