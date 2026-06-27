# QuantaFoundry — App-Bloq Brief, Round 4 (independent decomposition)

> The app-golden round establishes *what* each application computes. This round establishes *how*:
> you author an **independent circuit (decomposition)** that implements each application using only
> QuantaFoundry's **already-sealed gates**. There are many correct circuits; we do not check that your
> circuit matches anyone else's — we check that **its unitary equals the established app unitary**. When
> several runtimes' *different* circuits all compute the same unitary, the implementation is
> corroborated independently — catching a decomposition that silently computes the wrong thing.

---

## 1. Mission

For every app in `app_intents.json`, author a **circuit**: an ordered list of gate applications drawn
from the sealed-gate vocabulary in `GATE-VOCABULARY.json`, with explicit qubit targets. Derive the
circuit yourself from the application's specification. Do **not** copy an existing decomposition or look
at another runtime's circuit.

## 2. The gate vocabulary (`GATE-VOCABULARY.json`)

Each entry is a sealed gate you may use, with its name, qubit count, and convention. Examples:
`h`(1), `x`(1), `s`(1), `t`(1), `cnot`(2, control=first), `cz`(2), `swap`(2), `cs`(2, controlled-S
control=first), `ct`(2), `cs_dag`(2, controlled-S†), `cr4`(2), `cr3_dag`(2, controlled-T†),
`fredkin`(3, controlled-SWAP control=first), `toffoli`(3). **You may only use these names.** For any
controlled gate, the **first target is the control**.

If an app needs an operation not directly in the vocabulary, **build it from the vocabulary** (e.g.
controlled modular multiplication on N=15 is a chain of `fredkin`s because ×2 mod 15 is a bit
rotation; inverse-QFT is `swap` + `h` + `cs_dag`/`cr3_dag`).

## 3. Conventions

- Big-endian, qubit 0 = MSB. Wires are indexed `0 .. n_sys-1`.
- A circuit step is `{"gate": "<name>", "targets": [w0, w1, ...]}` where `len(targets)` = the gate's
  qubit count, and for controlled gates `targets[0]` is the control wire.
- Steps are applied **in list order** (first step first). The resulting unitary is
  `U = step_last ∘ … ∘ step_first`.
- No ancilla: the circuit acts on exactly `n_sys` wires and must realize the full app unitary.

## 4. Per-intent output

```json
{
  "id": "qpe_s", "n_sys": 3,
  "circuit": [
    {"gate": "h", "targets": [0]},
    {"gate": "h", "targets": [1]},
    {"gate": "cz", "targets": [0,2]},
    {"gate": "cs", "targets": [1,2]},
    {"gate": "swap", "targets": [0,1]},
    {"gate": "h", "targets": [1]},
    {"gate": "cs_dag", "targets": [1,0]},
    {"gate": "h", "targets": [0]}
  ],
  "construction_method": "how you derived the circuit (own words)",
  "self_check": "Stated you believe this circuit's unitary equals the app spec."
}
```

(The example above is one valid `qpe_s` circuit — author your own for every app; do not assume it is
optimal or unique.)

## 5. Submission file

One file `<your-runtime>.bloq.json` in `submissions_bloq/`:

```json
{ "runtime": "grok", "weights_id": "xai-grok-code-fast-1", "convention_ack": true,
  "submissions": [ { ...intent 1 circuit... }, ... ] }
```

## 6. How it is checked

Each circuit is assembled from the sealed gates' matrices (with your wire placements) into a unitary,
hashed by the oracle, and compared to the established app unitary (cross-model app-golden / sealed app).
A circuit that computes the right unitary **passes regardless of its length or gate choice**; a circuit
that computes the wrong unitary is flagged. Honesty over cleverness — a plain correct circuit is ideal.

## 7. Hard rules

1. Use only vocabulary gate names; first target of a controlled gate is the control.
2. Author every app; derive each circuit yourself; no copying.
3. If you cannot realize an app from the vocabulary, say so in `construction_method` rather than
   inventing a gate name.
