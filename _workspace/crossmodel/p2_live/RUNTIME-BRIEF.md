# RUNTIME-BRIEF — Cross-Model Golden Authoring (P2b live, round sx)

You are one of several **independent** model runtimes. Author golden unitary matrices for the
intents in `intents.json`, **from each intent's standard mathematical definition only** — do not
look up any "answer key", and do not look at any other runtime's output. Independence is the
entire point: distinct-weights models converging on the same matrix is what establishes truth
without a human key.

## Convention (must follow exactly)

- **Unitary form**: return the matrix `U` such that `|out> = U @ |in>`, i.e. `U[out_index, in_index]`.
- **Endianness**: big-endian, **first register = most significant bit (MSB)**. For a 1-qubit gate
  this is just the standard 2×2 matrix in basis order `|0>, |1>`.
- **Global phase**: irrelevant (verified up to global phase). Author the natural/principal form.
- **Complex numbers**: provide real and imaginary parts as separate matrices
  (`app_golden_real`, `app_golden_imag`), same shape `2^n_sys × 2^n_sys`.
- **Honesty over guessing**: if you are unsure of an intent's standard definition, say so in a
  `note` field rather than inventing a value. A refusal is more useful than a wrong matrix.

## Output

Return exactly one file `<your-model>.submission.json` in the format of
`SUBMISSION-TEMPLATE.json`, with:
- `runtime`: your runtime name (e.g. `gpt-5`, `gemini`, `grok`, `kimi`, `qwen`, `deepseek`).
- `weights_id`: a stable id **unique to your model weights** (e.g. `openai-gpt-5`). This must
  differ between different models — it is the independence unit.
- `convention_ack`: `true` once you have read and followed the convention above.
- `submissions`: one entry per intent in `intents.json` (`id`, `n_sys`,
  `app_golden_real`, `app_golden_imag`).

## Notes on this round

- `x_gate` is a **sanity/calibration control** with a universally known answer — it lets the
  operator confirm your endianness/convention is aligned. Author it too.
- `sx` is the **new intent** (no existing key). Author it independently from its definition.
