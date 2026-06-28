# ROUND-BRIEF — Cross-Runtime Co-Error Measurement (P3d round 2)

You are one of several **independent** model runtimes. This round measures **genuine cross-runtime
co-error**: whether independent models, given the *same* intent, share a *wrong* prior and converge
on the same incorrect matrix (corpus correlation). P3d round 1 could not test this — each runtime
chose a different intent. This round fixes a **common intent set** for everyone.

> **Author each intent's golden INDEPENDENTLY from its stated definition and convention.** Do not
> look up an "answer key", do not look at any other runtime's output. Read the convention exactly —
> the trap, if any, is in defaulting to a textbook reflex instead of the stated wiring.
> **Honesty over reflex.** If unsure, state your reading in a `note` rather than inventing.

## Convention (must follow exactly)

- Return `U` such that `|out> = U @ |in>`, i.e. `U[out_index, in_index]`.
- **Big-endian: first qubit q0 = most significant bit (MSB).** For a 2-qubit gate the basis order is
  `|q0 q1>` = indices `00,01,10,11` and `index = 2*q0 + q1`.
- Global phase irrelevant (verified up to global phase).
- Real and imaginary parts as separate matrices (`golden_real`, `golden_imag`).

## Intents (author all)

See `intents.json`. Summary:

- **`cnot_std`** (sanity/calibration): the **standard** CNOT, **control = q0 (MSB)**, target = q1.
  Known answer — confirms your endianness/convention is aligned.
- **`cnot_lower`** (probe): CNOT with **control = q1 (LSB)**, target = q0 (MSB). Note: this is the
  *control-on-the-second-qubit* CNOT, **not** the standard one. Author it from the stated wiring,
  not from the reflex "CNOT = standard control-MSB matrix."

## Output

Return exactly one file `<your-model>.submission.json` (format = `SUBMISSION-TEMPLATE.json`):
- `runtime`, `weights_id` (unique to your model weights — your independence unit), `convention_ack`.
- `submissions`: one entry per intent (`id`, `n_sys`, `golden_real`, `golden_imag`, optional `note`).
