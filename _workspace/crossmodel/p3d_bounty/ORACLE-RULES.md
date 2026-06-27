# ORACLE-RULES — what you are attacking (P3d)

The exact deterministic rules. Adjudication re-runs *these*; nothing else is trusted.

## Contracts (single module unitary U, n_sys system + n_anc ancilla qubits)

- **C1 FullCharacterization** — `U` is a full-basis unitary of dimension `2^(n_sys+n_anc)`.
- **C2 Unitarity** — `U† U = I` (exact, atol 1e-9).
- **C3 AncillaClean** — ancilla enters `|0>` and returns `|0>` (no leak). Convention: **system =
  low bits (0..n_sys-1), ancilla = high bits**. The effective system unitary `V` is extracted from
  the `anc=|0>` block. A leak (`U` maps `anc=0` input to `anc≠0` output) is a C3 violation.
- **C4 GoldenMatch** — the extracted `V` equals the `golden` matrix **up to global phase**.
  `u_hash = hash_unitary(V)` is stored in the seal.

Convention everywhere: big-endian (first register = MSB), `U[out_index, in_index]`, global phase
ignored. `run_contracts` returns a `ContractResult(all_passed, V, signal)` — it does **not** raise.

## KeyFreeConsensus gate (establish truth without an answer key)

- A `Source` = `(sid, klass, unit, u_hash)`. **independence_unit = `klass:unit`** — sources sharing
  a unit collapse to **one** vote (this is the B4 defense).
- `establish_truth(intent, sources, N)`: the `u_hash` supported by the most *distinct units* wins.
  - `< N` distinct units → **DIVERGENT** (no seal).
  - top-2 distinct-unit counts tie → **CONTESTED** (no seal — no plurality).
  - else → **ESTABLISHED**, `key = winning u_hash`, with a confidence `grade`.
- `grade`: `MULTIMODEL` needs ≥2 distinct **model** units; `PROOF_BACKED` if a `proof:` unit plus
  ≥2 total; otherwise `INSUFFICIENT`.
- High-risk / unkeyed intents are dispatched with `required_units = 2`, `grade_floor = MULTIMODEL`:
  `gated_seal` **REJECTs** anything below that floor.

## What this means for your attacks

- **T1**: C1–C4 only check that `golden == bloq's actual unitary`. They do **not** check that `bloq`
  is an *honest decomposition*. That gap is the target — but note `golden == bloq` means `u_hash` is
  still correct, so this is "decomposition-effort evasion," not hash forgery.
- **T2**: the gate trusts the `unit` labels you supply. It collapses *same-unit* sources to one vote.
  Your attack must make the gate *count ≥2 distinct units* for what is really one co-erroneous source.
- **T3**: divergent conventions produce *different* `u_hash` → DIVERGENT. To seal a wrong matrix you
  must manufacture a *plurality of distinct units* agreeing on the wrong convention.
