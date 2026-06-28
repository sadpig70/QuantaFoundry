# Release Notes

## v0.7 — Foundry realized + adoption & hardening (2026-06-28)

The foundry layer around QPGF is substantially realized: **50 sealed modules → 62 sealed applications**,
`registry_root_hash` `e64f4970…` (byte-identical reproduction). Intermediate milestones v0.4–v0.6
(genuine Shor N=21, the GenSkill library, self-extending goal-autonomy) are documented in the technical
spec's *What changed* sections; v0.3 — the first public milestone — is below.

**v0.7 highlights:** genuine **Shor 21 = 3 × 7** with honestly-decomposed modular arithmetic,
distinct-prime multipliers (mod 33/35), the first *live* cross-model truth (`sx` = √X), a gated
multi-model panel (≥2 distinct weights), a falsification front, and a code-enforced
honest-decomposition guard. Frozen consensus keys: **23**.

**v0.7+ Stage 0–5 — adoption & hardening (non-destructive analysis/tool/verification layers; all prior
seals, the frozen consensus keys, and the fingerprint files unchanged). The W2.4 cross-runtime relay
then grew the registry by two key-free primitives (`c7x`, `cr8_dag_gate`), and the W6.1 c7x payoff spent
`c7x` on three N>64 distinct-prime multipliers (`cmul2_mod91`/`77`/`85`), advancing the root
`3dae613d…→437efbc3…→e64f4970…` (50 modules, 59→62 apps) — pure non-destructive growth:**

- **S0–S1 Trust-Closure:** `second_oracle` independent re-derivation to **48/48 modules**; `ghz16`
  raised to `unitary_equiv_sampled` (zero structural-only seals); ZX-routing infrastructure (self-test
  6/6); global-phase tracker (controlled composition safe).
- **S2 QF-Discover:** an 8-term value function (Composability = counterfactual dependency fan-in;
  `c6x`'s leverage captured *before* the fact), a decomposition optimizer with the oracle as a hard
  reward (reward-hacking structurally blocked; 6/6 cheaper decompositions), a goal-selection guard, and
  auto-derived primitive proposals (`c7x`, `cr8_dag_gate`).
- **S3 Adoption:** OpenQASM3 export/ingest with round-trip unitary identity (57/57; closed loop 8/8), a
  `qf` CLI, and a citable `CITATION.cff` binding the root hash.
- **S4 Consensus close:** a convention-independence audit (construction = independent; endian/phase/atol
  = shared assumption, gap named) and **ρ-discount validation against constructed co-errors** (collapses
  poisoned consensus to <2 independent; mechanism live, natural co-error deferred to EXT).
- **S5 Hardening:** determinism env-pin (`requirements.lock`), an oracle-revocation protocol
  (fingerprint **145/145 intact**), and ed25519 Sybil defense.

Four EXT relay packages are prepared for cross-runtime items (c7x/cr8 primitives, a CI pilot, a poisoned
panel, runtime identity keys); backend hardware evidence remains gated/deferred.

---

## v0.3 — Key-free cross-model library + algorithm layer (2026-06-27)

The first public milestone of the QuantaFoundry foundry layer. The full trust chain — gate truth,
gate implementation, application intent, application implementation — is established by **cross-model
consensus + symbolic proof**, with **no human-asserted answer keys** anywhere.

### Highlights

- **22 sealed base gates** established key-free. Six independent AI runtimes (GPT-5, Gemini, Grok,
  Kimi, Qwen, DeepSeek — six distinct model weights) independently authored each gate's analytic
  reference (golden) and Qualtran implementation (bloq); consensus is counted per physical
  weight-set and corroborated by a stack-independent sympy proof. Calibration: 8/8 matched known
  QPGF keys; new gates: 7/7 ESTABLISHED; symbolic-proof agreement: 15/15; code reproduction: 90/90.
- **20 sealed applications** composed *only* from sealed parts, each re-verified by the oracle
  (C-app) and re-sealable byte-identically:
  - Bell, GHZ-3/4, and a **16-qubit Tier-1 (structural) GHZ** sealed without dense materialization.
  - **Grover** (recursive 3-level tree), **QFT(2–4)** pipelines, **Quantum Phase Estimation**
    (2-bit on S, 3-bit on T), inverse-QFT, controlled modular multiplication.
  - **Shor period-finding** that measurably **factors 15 = 3 × 5** — modular arithmetic honestly
    decomposed into sealed Fredkin gates (not a `MatrixGate` copy of the answer).
- **Application-level cross-model (Round 3–4):** app *intents* and app *implementations* were also
  established by independent runtimes. For every algorithm app, the independent app-intent
  consensus, the independent app-circuit consensus, and the in-house seal **all agree** (triple
  consistency). A real runtime's wrong circuits were detected as dissent and outvoted; some runtimes
  found *shorter* correct decompositions than the in-house one.
- **Rediscovery cross-checks (6/6):** apps that rebuild a separately-sealed gate (e.g. `H·CNOT·H` =
  CZ, `H·Toffoli·H` = CCZ, `CNOT³` = SWAP, the QFT pipelines) reproduce its hash byte-for-byte.

### Trust posture (honest)

- Every library key is anchored to a known QPGF key, or cross-model consensus + proof, or
  independent `proof ⊕ structural` convergence — never a bare human assertion.
- Open, by design: the gates exercised are textbook-easy (consensus is robust but not yet proven
  *necessary* on a hard intent); the app-bloq round had 4 distinct weights (two runtimes skipped
  it); goal-autonomy (deciding *what* to build) and Tier-3 sealing of apps are not yet done.

### Reproduce

```
python .agents/skills/qpgf-oracle/scripts/bundle_manifest.py --verify   # bundle_ok
python .pgf/autoforge/forge_apps.py                                     # 20/20 apps · rediscovery 6/6
python .pgf/keyfree/ingest_crossmodel.py                                # gate consensus (needs submissions/)
```

Full spec, evidence, and review questions: [`docs/QuantaFoundry-Technical-Spec.md`](docs/QuantaFoundry-Technical-Spec.md).

### Components

- Verification core: vendored QPGF oracle (`.agents/skills/qpgf-oracle/`, MIT) — see `NOTICE.md`.
- Dependency pins: python 3.13, numpy 2.4.6, qualtran 0.7.0, cirq-core 1.6.1, pyzx 0.10.3, sympy 1.14.0.
