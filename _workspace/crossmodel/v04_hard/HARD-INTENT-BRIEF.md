# QuantaFoundry — Hard-Intent Divergence Brief, v0.4 Round 5c

> **Why.** Reviewers (F-1) noted every truth established so far is textbook, so KeyFreeConsensus's
> *necessity* — its value where answers are NOT pre-agreed — was never demonstrated. This probe measures
> it directly. It mixes **hard-but-well-defined** intents (the mechanism should still converge → it works
> off-textbook) with **deliberately under-specified** intents (cross-model should diverge → a single
> model would have sealed an arbitrary default; consensus catches it). **Divergence here is success**, not
> failure: it is the evidence.

---

## 1. Mission

For each intent in `app_intents.json`, return the `2^n × 2^n` complex matrix `U` you believe the intent
denotes. For **Class B** intents the convention/phase is intentionally omitted — pick your most natural
reading and **state it** in `construction_method`. **Do not coordinate with other runtimes.**

## 2. Output (per intent)

```json
{ "id": "amb_cnot_endianness", "n_sys": 2,
  "app_golden_real": [[...]], "app_golden_imag": [[...]],
  "app_golden_code": "import numpy as np\n...\ngolden = <2^n x 2^n ndarray>",
  "construction_method": "your reading + convention chosen (esp. for Class B: control=first? phase=? bit-reversal?)",
  "self_check": "unitary, shape ok" }
```

- numpy/math/cmath only in `app_golden_code`; final statement assigns `golden`.
- `app_golden_real`/`imag` primary.

## 3. Submission file

`submissions/<your-runtime>.app.json`:
```json
{ "runtime": "qwen", "weights_id": "alibaba-qwen", "convention_ack": true,
  "submissions": [ {...}, ... ] }
```

## 4. Hard rules

1. No coordination, no peeking at any sealed file.
2. Answer **every** intent. For Class B, do **not** ask for clarification — commit to your natural
   default and record it. (The whole point is to observe which default each model picks.)
3. Be honest in `construction_method`: it lets the operator see *why* answers diverge.

## 5. Expected outcome (operator analysis)

`python .pgf/keyfree/ingest_app_golden.py --dir v04_hard` →

- **Class A** (`hard_cy`, `hard_sqrtswap`, `hard_perm3`): expect **ESTABLISHED** (≥2 weights converge).
  Confirms the mechanism establishes genuine non-textbook truth (necessity: it *works*).
- **Class B** (`amb_cphase`, `amb_cnot_endianness`, `amb_iqft2_bitrev`): expect **DIVERGENT**
  (distribution spread across defaults). Each model's lone answer would have been falsely sealed by a
  single-source pipeline; consensus rejects → escalate-to-clarify. Confirms necessity: it is *needed*.
- Metric: `cross_model_divergence_rate` (Class B) and `cross_model_convergence_rate` (Class A) in the
  report's distribution. Contrast with the single-model baseline (any one submission would "seal" its own).
