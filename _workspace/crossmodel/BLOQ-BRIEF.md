# QuantaFoundry — Cross-Model Bloq Authoring Brief (Round 2)

> Round 1 collected the **golden** (analytic numpy reference) for each gate, by cross-model
> consensus. Round 2 collects the **bloq** — the **Qualtran implementation** of the same gate.
> A different runtime authors the bloq than authored the golden, neither seeing the other. The
> verifier (QPGF oracle) then checks `bloq.tensor_contract() == golden` (equality up to global
> phase, atol 1e-7). A gate is sealed only if an independently-authored implementation matches the
> independently-authored reference. This is the co-error firewall.

---

## 1. Mission

For every intent in `intents.json`, author a **Qualtran bloq** whose `tensor_contract()` is the
gate's unitary. Return the Python snippet that constructs it. Derive it from your own Qualtran
knowledge — **do not look at any golden submission, any answer key, or another runtime's bloq.**

## 2. Conventions (same as golden round — must match or the oracle rejects)

- **Basis ordering: big-endian, first register = MSB.** For controlled gates the **first register
  is the control**, the last is the target. Qualtran's `bloq.tensor_contract()` already returns the
  raw big-endian matrix — do not transpose or reverse qubits.
- **No ancilla.** `n_anc = 0`: the bloq must act on exactly `n_sys` qubits and contract to a
  `2^n_sys × 2^n_sys` unitary. Do not introduce ancilla/measurement.
- **Global phase is free** (normalized away). Relative phases are not — get the `-1`, `i`,
  `e^{2πi jk/N}` exactly right.

## 3. Environment (pinned)

```
python 3.13.x · qualtran 0.7.0 · cirq-core 1.6.1 · numpy 2.4.6
```
Your snippet runs in a restricted namespace with `qualtran`, `cirq`, `numpy`, `math`, `cmath`
importable. **No file/network access.** The final statement must assign the bloq to a variable
named **`bloq`**.

## 4. Building blocks available in Qualtran 0.7.0 (choose / compose yourself)

Directly in `qualtran.bloqs.basic_gates`:
`XGate, YGate, ZGate, Hadamard, SGate, TGate, CNOT, CZ, Toffoli, TwoBitSwap, Swap, CSwap,
XPowGate, ZPowGate, Rz, Identity, GlobalPhase, …` (and `.controlled()` on most bloqs).
QFT: `from qualtran.bloqs.qft.qft_text_book import QFTTextBook; QFTTextBook(bitsize=n)`
(textbook QFT, raw — no bit-reversal swaps).
Cirq interop (for gates without a native bloq): `from qualtran.cirq_interop import CirqGateAsBloq`
wrapping a `cirq` gate, e.g. `CirqGateAsBloq(cirq.ISWAP)`.

Some intents (e.g. controlled-S, doubly-controlled-Z, iSWAP) have **no single native bloq** — build
them by composition (`.controlled()`, `BloqBuilder`) or via `CirqGateAsBloq`. There is more than
one correct construction; pick the one you trust and **state which** in `construction_method`.
The oracle will verify your choice against the golden — a wrong endianness or phase will be caught.

## 5. Per-intent output

```json
{
  "id": "cz",
  "n_sys": 2,
  "n_anc": 0,
  "bloq_code": "from qualtran.bloqs.basic_gates import CZ\nbloq = CZ()",
  "construction_method": "Native CZ bloq from qualtran.bloqs.basic_gates.",
  "self_check": "Stated that bloq.tensor_contract() is 4x4 and diagonal diag(1,1,1,-1)."
}
```

- `bloq_code`: self-contained snippet, final statement `bloq = <Bloq instance>`. Imports allowed
  only from `qualtran`, `cirq`, `numpy`, `math`, `cmath`.
- `construction_method`: your independent construction path (native / `.controlled()` / cirq
  interop / `BloqBuilder` composition).
- `self_check`: confirm you mentally (or actually) checked `bloq.tensor_contract()` has shape
  `2^n_sys` and the right action. Honesty over guessing.

## 6. Submission file

One JSON file named `<your-runtime>.bloq.json`:

```json
{
  "runtime": "kimi",
  "weights_id": "moonshot-kimi",
  "convention_ack": true,
  "submissions": [ { ...intent 1 bloq... }, ... ]
}
```

`weights_id` = your distinct model-weights identifier (your independence unit).

## 7. Hard rules

1. Do not view the golden submissions, any sealed.json, or another runtime's bloq.
2. Author every intent (Round A and Round B in `intents.json`). Round A bloqs double-check that
   your conventions align with the already-known seals.
3. `bloq_code` must use only qualtran/cirq/numpy/math/cmath, define `bloq`, no I/O.
4. A plain correct construction beats a clever one. The oracle is the judge.
