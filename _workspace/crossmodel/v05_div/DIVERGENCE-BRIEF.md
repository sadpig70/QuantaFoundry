# QuantaFoundry — TRUE-Divergence Brief, v0.5 Round 5e

> **Why this round exists.** Round 5c (v04_hard) tried to demonstrate that KeyFreeConsensus is *needed*
> (not just that it *works*) by showing cross-model **divergence** on "ambiguous" intents. It failed:
> all distinct-weight runtimes converged unanimously, because the chosen "ambiguities" still had a unique
> **Schelling default** (unnamed controlled-phase → CZ; unnamed CNOT → control=first; iQFT2 → raw). A
> probe whose ambiguity has a unique natural answer cannot diverge. **This round fixes the design:**
> Class C intents are **under-determined by construction** (a free continuous parameter — *no* unique
> answer exists), so divergence is forced by the intent itself, not by hoping models disagree.

---

## 1. Mission

For each intent in `app_intents.json`, return the `2^n × 2^n` complex matrix `U`, plus a **structured
`declared_reading`** so the operator can reconstruct your intended matrix and auto-audit prose-vs-matrix
consistency. **Do not coordinate. Do not peek at any sealed file.**

## 2. Three classes (what each measures)

| class | intents | what you do | expected |
|---|---|---|---|
| **S** sanity | `sanity_cz` | fully specified gate | unanimous ESTABLISHED (mechanism still works) |
| **C** free-parameter | `free_cphase`, `free_rz` | **pick your own** angle (no canonical fallback) | DIVERGENT — proves consensus is *needed* |
| **D** convention-split | `split_rz_sign`, `split_ry_dir`, `split_csqrtz_sign` | use **your standard** sign convention, declare it | measured: split or shared default |

- **Class C is the point.** The angle is yours to choose freely; there is intentionally no correct value.
  A single-source pipeline would seal whatever you happened to pick — an arbitrary truth. We want to see
  6 runtimes seal 6 *different* matrices → consensus refuses (DIVERGENT) → escalate-to-clarify. Do **not**
  default to π / CZ / a "nice" value to be safe; that defeats the measurement. Commit to a genuine free pick.
- **Class D** measures whether real convention splits (rotation sign) actually split across weights, or
  whether you all share a Schelling default (as in R5c). Both outcomes are valid data. These splits are
  deliberately **phase-inequivalent** (the verifier ignores global phase, so phase-only "splits" wouldn't
  register — these don't have that problem).

## 3. Output per intent

```json
{ "id": "free_cphase", "n_sys": 2,
  "app_golden_real": [[...]], "app_golden_imag": [[...]],
  "app_golden_code": "import numpy as np\n...\ngolden = <2^n x 2^n ndarray>",
  "declared_reading": { "phi": 1.2345 },
  "construction_method": "free choice phi=1.2345 rad; no canonical fallback",
  "self_check": "unitary, shape ok" }
```

**`declared_reading` schema by intent** (REQUIRED — this is the v0.5 addition):

| intent | declared_reading |
|---|---|
| `sanity_cz` | `{ "kind": "fixed" }` |
| `free_cphase` | `{ "phi": <your radians, 0<phi<2π, phi≠π> }` |
| `free_rz` | `{ "theta": <your radians, 0<theta<2π, theta∉{0,π}> }` |
| `split_rz_sign` | `{ "sign": "-" }` or `{ "sign": "+" }` |
| `split_ry_dir` | `{ "sign": "-" }` or `{ "sign": "+" }` |
| `split_csqrtz_sign` | `{ "sign": "+" }` (controlled-S) or `{ "sign": "-" }` (controlled-S†) |

The operator reconstructs the matrix your `declared_reading` implies and checks it equals your submitted
matrix. A mismatch (you declare one reading but submit another — the *gemini/iQFT2* failure mode) is
auto-flagged. So make `declared_reading` honestly match your matrix.

- numpy/math/cmath only in `app_golden_code`; final statement assigns `golden`.
- `app_golden_real` / `imag` are primary; matrix conventions same as other rounds (U[out,in], big-endian).

## 4. Submission file

`submissions/<your-runtime>.app.json`:
```json
{ "runtime": "qwen", "weights_id": "alibaba-qwen", "convention_ack": true,
  "submissions": [ {...}, ... ] }
```

## 5. Hard rules

1. No coordination, no peeking at sealed files.
2. Answer **every** intent. For Class C, **commit to a free pick** — do not ask for clarification, do not
   default to a canonical value. The whole experiment is observing that your free pick differs from others'.
3. `declared_reading` must honestly describe the matrix you actually submit.

## 6. Operator analysis (after relay)

```
python .pgf/keyfree/ingest_app_golden.py --dir v05_div
```

- **Class C** → expect **DIVERGENT** (`max independent agreement < 2`). Each runtime's lone answer would
  have been falsely sealed by a single-source pipeline; consensus rejects → escalate. This is the
  **necessity-NEEDED** evidence R5c failed to produce — now airtight because the intent has no unique answer.
- **Class D** → **measured**: DIVERGENT, ESTABLISHED-with-dissent (real split, majority wins), or unanimous
  (shared Schelling default). The **READING AUDIT** section flags `contested_tie` (e.g. a 3-3 deadlock that
  `establish_truth` would otherwise seal to an arbitrary side) and any `prose_matrix_mismatch`.
- **Class S** → must **ESTABLISH unanimously**; confirms the probe isn't just breaking everything.
- Pre-flight (`smoke.py`, self-contained) already proved: every Class-C/D reading is distinct &
  phase-inequivalent, the engine judges as designed, and the audit auto-flags gemini-type mismatch & 3-3 ties.
