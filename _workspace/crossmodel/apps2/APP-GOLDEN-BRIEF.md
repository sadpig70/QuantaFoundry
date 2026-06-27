# QuantaFoundry — App-Golden Brief, Round 4 (algorithm layer)

> Round 3 cross-model-confirmed the *intents* of the simple apps (bell, GHZ, Grover diffusion, QFT2/3).
> Round 4 lifts this to the **algorithm layer**: inverse-QFT, Quantum Phase Estimation, controlled
> modular multiplication, and **Shor period-finding**. For each app in `app_intents.json` you author
> the **full application unitary** `U` from the precise mathematical specification — independently, no
> peeking at any decomposition, circuit, or answer. When ≥2 different-weights runtimes converge on the
> same `U`, the application's *intent* is established cross-model (no in-house authority), closing the
> last in-house-authored trust gap for these apps.

---

## 1. Mission

For every intent in `app_intents.json`, produce the exact `2^n × 2^n` complex matrix `U` of the whole
application (`n = n_sys`), built analytically from the specification. The specs fix the unitary
uniquely (register layout, controlled-power assignment, QFT convention are all given); your task is to
**derive that unitary yourself**, by your own method. Different runtimes will compute it via different
code paths — that independence is the point.

## 2. Conventions — STRICT (identical to prior rounds; also restated per-intent)

- **Big-endian, qubit 0 = MSB**, and = control for controlled operations.
- `U[out,in] = <out|U|in>`; in a product the **rightmost factor acts first**.
- `dtype=complex`, shape exactly `(2^n_sys, 2^n_sys)`, no ancilla.
- **QFT convention:** `QFT_n[j,k] = (1/sqrt(2^n)) exp(2πi·j·k/2^n)`, big-endian integer indexing, **no
  output bit-reversal** (raw matrix). **inverse QFT = conjugate transpose.**
- **Global phase is free** (normalized away). Relative phases / structure are not.
- Floating-point noise below 1e-9 is free (the verifier quantizes). Be accurate to ≫ 1e-9.

## 3. Per-intent output

```json
{
  "id": "qpe_s", "n_sys": 3, "n_anc": 0,
  "app_golden_real": [[...]], "app_golden_imag": [[...]],
  "app_golden_code": "import numpy as np\n...\ngolden = <final 2^n x 2^n ndarray>",
  "construction_method": "how you derived the app unitary (own words)",
  "self_check": "U unitary (U@U^H ~ I) and shape 2^n_sys verified"
}
```

- `app_golden_real`/`imag`: nested JSON arrays of plain numbers — the **primary** artifact.
- `app_golden_code`: self-contained numpy snippet, final statement assigns to **`golden`**. Only
  `numpy`/`math`/`cmath`, no I/O. Re-run in a sandbox; must reproduce the numbers (up to phase / 1e-9).
- For the larger ones (`qpe_t`, `shor15_a2`) the matrix is big (16×16, 128×128); the `*_real`/`*_imag`
  arrays are still required, but you may build them in `app_golden_code` programmatically.

## 4. Submission file

One file `<your-runtime>.app.json` in `submissions/`:

```json
{ "runtime": "kimi", "weights_id": "moonshot-kimi", "convention_ack": true,
  "submissions": [ { ...intent 1... }, ... ] }
```

`weights_id` = your distinct model-weights id (independence unit; same weights = one vote).

## 5. Hard rules

1. Do not view another runtime's submission, any sealed file, or any circuit/decomposition.
2. Author every intent, in order. Derive the unitary yourself from the spec.
3. `app_golden_code` defines `golden`, numpy/math/cmath only, no I/O.
4. If a spec seems ambiguous to you, state your reading in `construction_method` rather than guessing
   silently — honest divergence is useful signal.
