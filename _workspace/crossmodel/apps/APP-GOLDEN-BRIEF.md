# QuantaFoundry — Cross-Model App-Golden Authoring Brief (Round 3)

> Rounds 1–2 established the **gates** (golden + bloq) by cross-model consensus. Round 3 lifts the
> same idea to **applications**: for each app in `app_intents.json` you author the **full application
> unitary** `U` (the app's *intent*) from its standard definition — independently, no peeking. When
> ≥2 different-weights runtimes converge on the same `U`, that hash becomes the app's established
> intent, with **no human/orchestrator-authored golden**. QuantaFoundry then checks that its
> decomposition of the app into already-sealed modules reproduces exactly this hash.

---

## 1. Mission

For every intent in `app_intents.json`, produce the exact `2^n × 2^n` complex matrix `U` of the
**whole application** (`n = n_sys`), built analytically from the application's textbook definition.
Return it as numbers **and** as the numpy code that generated it. Do not look up QuantaFoundry
sources, sealed files, another runtime's answer, or any decomposition — derive the application's
overall unitary yourself.

## 2. Conventions — STRICT (identical to the gate round)

- **Basis ordering: big-endian, first register = MSB.** For controlled operations the **first
  register is the control**, the last is the target. Index `i = q0·2^(n-1) + … + q(n-1)`.
- **Matrix element**: `U[out, in] = <out|U|in>`. Column `j` = image of `|j>`.
- **dtype/shape**: `numpy.ndarray`, `dtype=complex`, exactly `(2^n_sys, 2^n_sys)`. No ancilla.
- **Global phase is FREE** (normalized away before hashing). For `reflect00` in particular,
  `diag(1,-1,-1,-1)` and `diag(-1,1,1,1)` hash identically — author whichever your definition gives.
- **Floating-point noise below 1e-9 is free** (the verifier quantizes). Just be accurate to ≫ 1e-9.
- **Relative phases / structure are NOT free** — the `-1` in reflect00, the `i`/roots-of-unity in
  QFT, the entangling structure of GHZ. Get these exactly right.

## 3. Composition order (so everyone builds the same matrix)

Where a definition is given as a product like `G = D * O` or `U = CNOT * (H tensor I)`, read it as
standard matrix multiplication acting on a column state: the **rightmost factor is applied first**.
E.g. `bell = CNOT @ (H tensor I)` means "Hadamard first, then CNOT". Apply this consistently.

## 4. Per-intent output

```json
{
  "id": "bell",
  "n_sys": 2,
  "n_anc": 0,
  "app_golden_real": [[...],[...],[...],[...]],
  "app_golden_imag": [[...],[...],[...],[...]],
  "app_golden_code": "import numpy as np\n...\ngolden = <final 2^n x 2^n ndarray>",
  "construction_method": "1-2 sentences: how you derived the app unitary (matrix product / tensor of gates / direct definition / roots of unity).",
  "self_check": "Confirm U is unitary (U @ U.conj().T ~ I) and shape is 2^n_sys."
}
```

- `app_golden_real`/`app_golden_imag`: nested JSON arrays of plain numbers — the **primary** artifact.
- `app_golden_code`: self-contained numpy snippet, final statement assigns the matrix to **`golden`**.
  Only `numpy`/`math`/`cmath`, no I/O. It is re-run in a restricted sandbox and must reproduce the
  numbers (up to global phase / 1e-9).
- `construction_method`: your independent derivation path (honesty over guessing).

## 5. Submission file

One JSON file named `<your-runtime>.app.json`:

```json
{
  "runtime": "kimi",
  "weights_id": "moonshot-kimi",
  "convention_ack": true,
  "submissions": [ { ...intent 1... }, ... ]
}
```

`weights_id` = your distinct model-weights identifier (your independence unit; same-weights = 1 vote).

## 6. Hard rules

1. Do not view another runtime's submission, any sealed.json, any decomposition, or an answer key.
2. Author every intent in `app_intents.json`, in order.
3. `app_golden_code` defines `golden`, uses only numpy/math/cmath, no I/O.
4. A plain correct construction beats a clever one. The oracle is the judge.
