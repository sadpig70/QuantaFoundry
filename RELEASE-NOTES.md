# Release Notes

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
