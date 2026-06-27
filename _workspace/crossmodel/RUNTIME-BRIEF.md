# QuantaFoundry — Cross-Model Golden Authoring Brief

> **You are one of several independent AI runtimes** (codex, gemini, grok, kimi, qwen, deepseek)
> being asked the *same* question independently. Your job: author the **golden reference unitary**
> for each quantum gate listed in `intents.json`, from the gate's standard definition, **without
> seeing any other runtime's answer**. Your matrices will be hashed and compared. When ≥2 runtimes
> with different model weights converge on the same hash, that hash becomes an *established truth*
> — no human answer key involved. This is the point of the exercise.

---

## 1. Mission

For every intent in `intents.json`, produce the exact `2^n × 2^n` complex matrix `U` of the gate
(`n = n_sys`), built **analytically from the gate's textbook definition**. Return it as numbers
**and** as the numpy code that generated it. Do not look up QuantaFoundry's repository, do not copy
a matrix from another runtime, do not search for "the answer" — derive it yourself. Independent
derivation is what gives your vote weight.

## 2. Conventions — these are STRICT (a wrong convention = your answer disagrees with everyone)

### 2.1 Basis ordering — **big-endian, first register = most significant bit (MSB)**
For an `n`-qubit gate, basis state index `i` (0 … 2ⁿ−1) corresponds to the bitstring `q0 q1 … q(n-1)`
where **q0 is the MSB**:
```
i = q0·2^(n-1) + q1·2^(n-2) + … + q(n-1)·2^0
```
Example (n=2): index 0=|00⟩, 1=|01⟩, 2=|10⟩, 3=|11⟩. For a **controlled** gate, the **first
register (q0) is the CONTROL**, the last register is the target. (e.g. CNOT: |10⟩→|11⟩, |11⟩→|10⟩.)

### 2.2 Matrix element convention
`U[out, in] = ⟨out| U |in⟩`. Column `j` = image of basis state `|j⟩`. (Standard numpy matrix-vector:
`new_state = U @ old_state`.)

### 2.3 dtype & shape
`numpy.ndarray`, `dtype=complex`, shape exactly `(2^n_sys, 2^n_sys)`. No ancilla for these intents
(`n_anc = 0`): return the system-only unitary.

### 2.4 What is FREE (do not worry about these — they are normalized away before hashing)
- **Global phase.** The verifier divides out the phase of the first non-zero element. `U` and
  `e^{iθ}·U` hash identically. Use whatever global phase your textbook definition gives — don't
  "fix" it.
- **Floating-point noise** below `1e-9`. The verifier quantizes to a `1e-9` lattice. Full
  double-precision is fine; you do **not** need to round. Just be accurate to ≫ 1e-9.

### 2.5 What is NOT free (get these exactly right)
- **Relative phases** between basis states (e.g. the `-1` in CZ, the `i` in S, the `e^{2πi·jk/N}`
  in QFT). These are the content of the gate.
- **Basis ordering** (§2.1). A little-endian or wrong control/target assignment will make your
  answer disagree with the consensus. If unsure about endianness for a controlled/multi-qubit gate,
  re-read §2.1.

## 3. Per-intent output (one object per intent)

```json
{
  "id": "cz",
  "n_sys": 2,
  "n_anc": 0,
  "golden_real": [[...],[...],[...],[...]],   // 2^n × 2^n, real parts
  "golden_imag": [[...],[...],[...],[...]],   // 2^n × 2^n, imag parts
  "golden_code": "import numpy as np\n...\ngolden = <final ndarray>",
  "construction_method": "1-2 sentences: how you derived it (truth table / tensor product / roots of unity / projector decomposition / ...).",
  "self_check": "State that you verified U is unitary (U @ U.conj().T ≈ I) and shape is correct."
}
```

Rules for the fields:
- `golden_real` / `golden_imag`: nested JSON arrays of plain numbers (not strings). These are the
  **primary** artifact that gets hashed.
- `golden_code`: self-contained numpy snippet whose final statement assigns the same matrix to a
  variable named **`golden`**. Must use only `numpy` (alias `np`) and the Python stdlib `math`/
  `cmath`. No I/O, no network, no file access. This will be re-executed in a restricted sandbox and
  must reproduce `golden_real`/`golden_imag` exactly (up to global phase / 1e-9).
- `construction_method`: your *independent* derivation path. Different runtimes deriving the same
  matrix by *different methods* is the strongest evidence; say honestly how you got it.

## 4. Submission file

Return **one JSON file** named `<your-runtime>.submission.json` (e.g. `gemini.submission.json`)
with this top-level shape:

```json
{
  "runtime": "gemini",
  "weights_id": "google-gemini",
  "convention_ack": true,
  "submissions": [ { ...intent 1... }, { ...intent 2... }, ... ]
}
```

- `runtime`: your short name (codex | gemini | grok | kimi | qwen | deepseek).
- `weights_id`: a stable identifier for your model weights (vendor-model). This is your
  **independence unit** — two submissions with the same `weights_id` count as ONE vote, so it must
  honestly reflect distinct weights.
- `convention_ack`: set `true` to confirm you followed §2 (big-endian, `U[out,in]`, n_anc=0).
- `submissions`: array, one object per intent in `intents.json`, **in the same order**.

## 5. Hard rules (independence)

1. **Do not view, request, or incorporate any other runtime's submission.** Derive every matrix yourself.
2. **Do not fetch QuantaFoundry source, sealed.json files, or any "answer key."**
3. If an intent's definition seems ambiguous to you, do **not** guess silently — produce your best
   standard interpretation **and** note the ambiguity in `construction_method`. (Honest divergence
   is useful data; a lucky guess that hides ambiguity is not.)
4. Accuracy over cleverness. A plain, correct, textbook construction is exactly what's wanted.

## 6. Two rounds (see `round` field in each intent)

- **Round A (calibration):** gates whose answer QuantaFoundry already knows (`x_gate, z_gate,
  h_gate, cnot, swap2, toffoli, qft2, qft3`). Used to confirm your conventions are aligned. If your
  Round-A hashes match the known seals, your Round-B votes are trusted.
- **Round B (establishment):** gates with **no** stored answer key (`s_gate, t_gate, cz, iswap,
  cs_gate, ccz, qft4`). Here your converged hash *creates* the truth. Be careful.

You may do both rounds in one submission file (all intents in `submissions`).

---

*Contract reference (for the curious): the verifier computes `sha256` over the phase-normalized,
1e-9-quantized real/imag lattice of `U`. Same gate, any global phase, any sub-1e-9 noise → same
hash. Different basis ordering or relative phase → different hash.*
