# ROUND-BRIEF — Cross-Runtime Co-Error Measurement (P3d round 3)

You are one of several **independent** model runtimes. This round (like round 2) measures
**genuine cross-runtime co-error** — whether independent models share a *wrong prior* on gates that
are commonly mis-stated. Round 2 used a qubit-ordering probe (all 6 got it right). This round uses
gates with well-documented definitional confusions (half-angle, adjoint sign, phase factors).

> **Author each intent's golden INDEPENDENTLY from its standard definition.** Do not look up an
> "answer key", do not look at any other runtime's output. Recall each gate's *exact* matrix.
> **Honesty over reflex.** If unsure of a definition, state your reading in a `note` rather than
> inventing — a refusal is more useful than a wrong matrix.

## Convention (must follow exactly)

- Return `U` such that `|out> = U @ |in>`, i.e. `U[out_index, in_index]`.
- **Big-endian: first qubit q0 = MSB.** For 2-qubit gates: basis `|q0 q1>`, index = `2*q0 + q1`.
- **Global phase is irrelevant** (verified up to global phase). Author the principal/standard form.
- Real and imaginary parts as separate matrices (`golden_real`, `golden_imag`).

## Intents (author all)

See `intents.json`:

- **`x_gate`** (sanity/calibration): Pauli-X. Known answer — confirms your convention is aligned.
- **`rx_half`**: the single-qubit rotation `Rx(π/2)` — rotation about the X axis by angle π/2.
- **`iswap`**: the two-qubit `iSWAP` gate.
- **`tdag`**: the single-qubit `T†` gate (the adjoint / inverse of the T gate).

## Output

Return one file `<your-model>.submission.json` (format = `SUBMISSION-TEMPLATE.json`):
`runtime`, `weights_id` (unique to your model weights = your independence unit), `convention_ack`,
and `submissions`: one entry per intent (`id`, `n_sys`, `golden_real`, `golden_imag`, optional `note`).
