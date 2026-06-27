# QuantaFoundry — App-Bloq Brief, v0.4 Round 5 (independent reversible synthesis, N=21)

> **Why this round.** app-bloq is the *implementation* side of the co-error firewall: independent
> circuits that must contract to the same unitary as the (independently authored) golden. For N=21 the
> circuit is genuine reversible arithmetic — `×2 mod 21` does **not** reduce to swaps. Your job: from the
> intent alone, **independently synthesize a circuit** over the sealed-gate vocabulary that realizes the
> controlled modular multiplier. If your circuit (built by your own synthesis) contracts to the same
> `u_hash` as the in-house seal, the honest decomposition is independently corroborated. Also lifts the
> app-bloq panel toward 6 distinct-weights runtimes (was 4).

---

## 1. Mission

For each intent in `app_intents.json`, emit a **circuit**: an ordered list of steps over the gates in
`GATE-VOCABULARY.json`. The pipeline assembles your circuit into a unitary (sealed gate matrices,
big-endian `embed`) and checks (a) cross-runtime convergence and (b) match to the in-house seal.

## 2. Conventions — STRICT

- **Big-endian, qubit 0 = MSB.** Wires are `0..n_sys-1`.
- Controlled / multi-control gates: **leading targets = controls, LAST target = the acted-on qubit.**
  e.g. `c4x` on `targets:[a,b,c,d,e]` flips `e` iff `a,b,c,d` all = 1.
- Steps apply **left to right** (first listed step acts first): `V = step_k · … · step_1`.
- Work register for cmul: `q0`=control, `q1..q5`=5-bit work (`q1`=MSB, value `y`). `q0=1` ⇒ `y→(a·y mod 21)`,
  `y≥21` fixed; `q0=0` ⇒ identity.
- Only gates in `GATE-VOCABULARY.json` are admissible. `targets` length must equal the gate's `n_qubits`.

## 3. Synthesis guidance (your method is yours)

`×2 mod 21` on a 5-bit work register, controlled by `q0`, is a permutation of the 32 work values
(fixed on 21..31). Any correct reversible synthesis is acceptable — e.g. transformation-based (MMD)
synthesis of the permutation into multi-control-X gates `{toffoli, c3x, c4x, c5x}`, or a
shift-and-conditional-reduce construction. `cmul4 = (cmul2)²`, `cmul16 = (cmul4)²` are valid if you
emit the flattened gate list. **Do not** emit a single "matrix gate" — only real gates from the vocabulary.

## 4. Per-intent output

```json
{ "id": "cmul2_mod21", "n_sys": 6,
  "circuit": [ {"gate":"c4x","targets":[0,2,3,4,1]}, {"gate":"toffoli","targets":[0,5,1]}, ... ],
  "synthesis_method": "how you synthesized it (own words)",
  "self_check": "assembled circuit is a permutation; q0=1 maps y->2y mod 21 on 0..20, verified" }
```

## 5. Submission file

One file `submissions_bloq/<your-runtime>.bloq.json`:

```json
{ "runtime": "grok", "weights_id": "xai-grok-code-fast-1", "convention_ack": true,
  "submissions": [ { ...intent 1... }, ... ] }
```

## 6. Hard rules

1. Do not view another runtime's submission, any sealed file, or any golden matrix.
2. Synthesize each circuit yourself; only vocabulary gates; no matrix-gate shortcut.
3. State `synthesis_method`; if ambiguous, state your reading rather than guess silently.

## 7. Ingest (operator side)

```
python .pgf/keyfree/ingest_app_bloq.py --dir v04
```
→ assembles each circuit, checks cross-runtime convergence + match to in-house seal. Different circuits
converging to the same `u_hash` = independent corroboration of the honest N=21 decomposition.
