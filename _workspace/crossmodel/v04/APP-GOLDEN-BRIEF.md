# QuantaFoundry — App-Golden Brief, v0.4 Round 5 (N=21 modular-arithmetic layer)

> **Why this round.** Prior rounds established gate-level truth and the N=15 algorithm layer
> cross-model. But N=15 = 2⁴−1 makes modular multiplication collapse to a cyclic bit-rotation —
> it never exercises real carry / modular reduction. This round lifts cross-model establishment to
> **N=21 (= 3×7, not 2ᵏ−1)**, where `×a mod 21` is genuine modular arithmetic, plus the 7-qubit
> inverse-QFT that Shor-21 needs. When ≥2 different-weights runtimes converge on the same unitary,
> the app's *intent* is established cross-model (no in-house authority).

---

## 1. Mission

For every intent in `app_intents.json`, produce the exact `2^n × 2^n` complex matrix `U` of the whole
application (`n = n_sys`), derived **analytically and independently** from the specification — by your
own method, not by copying any circuit/decomposition/answer. Different runtimes computing the same `U`
via different code paths is the entire point.

## 2. Conventions — STRICT (see `app_intents.json.convention`, restated)

- **Big-endian, qubit 0 = MSB**, and = control for controlled operations.
- `U[out,in] = <out|U|in>`; in a product the **rightmost factor acts first**.
- `dtype=complex`, shape exactly `(2^n_sys, 2^n_sys)`, **no ancilla**.
- Work value: 5-bit register `q1..q5` (q1=MSB) → integer `y = Σ bit·2^(4-i)`.
- **Modular out-of-range rule:** `×a mod 21` is defined for `y` in `0..20`; any `y` in `21..31` is a
  **fixed point** (`y→y`). This makes each controlled map a valid permutation on all 32 work states.
- **QFT:** `QFT_n[j,k] = (1/√(2^n))·exp(2πi·j·k/2^n)`, big-endian, **no bit-reversal**; iQFT = conj-transpose.
- Global phase free; permutations have none. FP noise < 1e-9 free — be accurate to ≫ 1e-9.

## 3. Per-intent output

```json
{
  "id": "cmul2_mod21", "n_sys": 6, "n_anc": 0,
  "app_golden_real": [[...]], "app_golden_imag": [[...]],
  "app_golden_code": "import numpy as np\n... \ngolden = <final 2^n x 2^n ndarray>",
  "construction_method": "how you derived U in your own words (e.g. built the controlled permutation directly from y->(2y mod 21))",
  "self_check": "U@U^H ~ I and shape (2^n_sys) verified"
}
```

- `app_golden_real`/`imag`: nested JSON number arrays — the **primary** artifact.
- `app_golden_code`: self-contained numpy, final statement assigns `golden`; **only numpy/math/cmath, no I/O**.
  Re-run in a sandbox; must reproduce the numbers (up to global phase / 1e-9).
- `iqft7` is 128×128 — build it programmatically inside `app_golden_code` (arrays may be generated there).

## 4. Submission file

One file `submissions/<your-runtime>.app.json`:

```json
{ "runtime": "kimi", "weights_id": "moonshot-kimi", "convention_ack": true,
  "submissions": [ { ...intent 1... }, { ...intent 2... }, ... ] }
```

`weights_id` = your distinct model-weights id (independence unit; same weights = one vote).

## 5. Hard rules

1. Do not view another runtime's submission, any sealed file, or any circuit/decomposition.
2. Author every intent, in order. Derive `U` yourself from the spec.
3. `app_golden_code` defines `golden`; numpy/math/cmath only; no I/O.
4. If a spec reads ambiguous to you, state your reading in `construction_method` rather than guessing
   silently — honest divergence is useful signal (it is exactly what the consensus filter is for).

## 6. Ingest (operator side, after collection)

```
python .pgf/keyfree/ingest_app_golden.py --dir v04
```
→ consensus per app (N=2, weights independence) + comparison to the in-house seal. ESTABLISHED + match
on all four ⇒ the N=21 layer's intent is cross-model established (in-house authorship retired).
