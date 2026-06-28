# ROUND-BRIEF — Cross-Runtime Contested-Definition Probe (P3d round 4)

You are one of several **independent** model runtimes. Rounds 2–3 used well-defined gates and all
runtimes agreed. This round targets gates whose **definition genuinely varies across sources**
(convention splits: bit-reversal, sign of the generator, phase of a root). The goal is to measure
whether independent models (a) converge on a de-facto standard, (b) **diverge** across conventions
(in which case the consensus gate should refuse to seal — that is the intended behavior), or
(c) **co-converge on a corpus-dominant convention**.

> **Author each gate in the form YOU consider standard, INDEPENDENTLY.** Do not look at other
> runtimes. Several of these names admit more than one convention in common use — if you believe a
> name is ambiguous, pick the convention you consider canonical and **state your choice in `note`**
> (e.g. "QFT without final bit-reversal swap; phase e^{+2πi/N}"). Honesty over guessing.

## Convention (fixed parts — must follow)

- Return `U` with `|out> = U @ |in>`, i.e. `U[out_index, in_index]`.
- **Big-endian: first qubit q0 = MSB.** 2-qubit basis `|q0 q1>`, index = `2*q0 + q1`.
- **Global phase is irrelevant** (verified up to global phase). The *contested* parts below are NOT
  global phase — they are bit-ordering, generator sign, and relative phases.
- Real and imaginary parts as separate matrices (`golden_real`, `golden_imag`).

## Intents (author all)

See `intents.json`:

- **`x_gate`** (sanity): Pauli-X. Known — calibration.
- **`qft2`**: the 2-qubit Quantum Fourier Transform. (Conventions differ on the final bit-reversal
  swap and the sign of the phase — author your canonical form and note it.)
- **`sqrt_swap`**: the √SWAP gate (a square root of SWAP). (The phase/branch convention varies.)
- **`rz_half`**: `Rz(π/2)`, the Z-axis rotation by π/2. (The generator-sign convention
  `exp(∓ iθZ/2)` varies — author your canonical form and note it.)

## Output

One file `<your-model>.submission.json` (format = `SUBMISSION-TEMPLATE.json`):
`runtime`, `weights_id` (unique to your model weights), `convention_ack`, and `submissions`
(one entry per intent: `id`, `n_sys`, `golden_real`, `golden_imag`, and a `note` stating any
convention choice).
