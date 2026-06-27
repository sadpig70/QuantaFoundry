# contract-spec — QPGF Contract Definitions

This document defines the deterministic contracts enforced by `qpgf-oracle`.
The implementation lives in `scripts/contracts.py`; the original prototype engine is `qcore/qcore.py`.

Notation:

- `U`: full candidate unitary or isometry
- `V`: effective system operation
- `n = n_sys + n_anc`
- `ATOL = 1e-9`
- canonical convention: Qualtran-native raw big-endian `tensor_contract()` output

## C1 — FullCharacterization

A module must describe the complete action, not samples.

```text
square unitary path:
  U.shape == (2^n, 2^n)

alloc/isometry path:
  U.shape == (2^(n_sys+n_anc), 2^n_sys)
```

Violation:

```text
ContractViolation("C1 ...")
```

Partial characterization hides silent bugs. QPGF checks the full basis for the active tier.

## C2 — PhasePreserved

The operation must preserve complex amplitudes and phase through unitarity or faithful isometry.

Square unitary path:

```text
|| U†U - I || <= ATOL
```

Isometry path:

```text
|| V†V - I || <= ATOL
```

C2 proves validity of the operation class. It does not prove the operation is the intended one; that is C4.

## C3 — AncillaClean

For THRU-style ancilla, input ancilla `|0>` must return to output ancilla `|0>` and must not remain entangled with the system.

Definition:

```text
input columns with ancilla = |0> must have support only on output rows with ancilla = |0>
leak = || U[2^n_sys:, :2^n_sys] || <= ATOL
V = U[:2^n_sys, :2^n_sys] must be unitary
```

This path corresponds to the original `qcore` convention and is not the main Qualtran alloc/free path.

## C3-iso — Alloc Ancilla Isometry

Qualtran alloc-style ancilla may produce a rectangular isometry:

```text
V.shape == (2^(n_sys+n_anc), 2^n_sys)
V†V == I
```

Meaning:

- norms are preserved;
- inner products are preserved;
- the allocated ancilla is deterministic;
- no information is lost.

Violation:

```text
ContractViolation("C3iso ...")
```

Seal label:

```text
contract = "C1-C4(iso)"
```

The hash includes shape, so rectangular isometries are deterministic and distinct.

## C4 — ComposableContract

The verified operation must match the independent mathematical intent.

Golden comparison:

```text
|| norm_phase(V) - norm_phase(golden) || <= 1e-7
```

Global phase is ignored. Relative phase is preserved.

Composition:

```text
compose(V1, V2) = V2 @ V1
```

Interface dimensions must match. The result is re-verified and resource counts are accumulated.

C4 is the contract that rejects a valid but unintended unitary.

## C4-uncompute — Compute-Uncompute Cleanliness

For an alloc isometry `V`, an intermediate operation `M`, and the dagger uncompute:

```text
R = V† M V
```

`R` must be a valid square unitary. This checks that the ancilla has returned cleanly.

Examples:

```text
And† · Z · And = CZ
MultiAnd† · Z · MultiAnd = CCZ
```

## C-app — DecompositionCorrectness

For application manifests, the composed sealed children must implement the application-level intent.

Definition:

```text
hash_unitary(compose(sealed children)) == hash_unitary(app_golden)
```

Violation:

```text
decomposition_mismatch
```

INV3 proves that the composed circuit is valid. C-app proves that it is the intended application.

## Seal Tiers

Dense exact verification is exponential. QPGF supports explicit sealing tiers.

### Tier 0 — EXACT

```text
dense V_app -> compare to app_golden -> u_hash = hash_unitary(V_app)
```

Use for small modules and small apps with available dense references.

### Tier 1 — STRUCTURAL

No dense materialization.

```text
app_u_hash = sha256(child u_hashes + composition structure)
```

The claim is correct-by-construction under:

- every child is sealed;
- interface placement is valid;
- the decomposition plan is the intended app.

Small cases may additionally run dense advisory checks.

### Tier 2 — CLIFFORD

Large Clifford modules are sealed by stabilizer tableau canonicalization.

```text
meta tier = "clifford"
u_hash = sha256(canonical tableau)
```

Non-Clifford operations are rejected.

### Tier 3 — CLIFFORD+T

Universal Clifford+T circuits are sealed by ZX-calculus equivalence against an independent reference circuit.

```text
meta tier = "clifford+t"
golden = independent cirq.Circuit reference
```

If equivalence is proved, the module is sealed. If equivalence is not proved, the oracle refuses to seal.

## Tier Invariants

```text
INV-TIER: every seal declares its tier
INV-IFACE: structural composition checks widths and placements
probabilistic validation is advisory only and cannot become a seal
```

## Deterministic Signature Fields

The seal records:

```text
id
sealed = true
convention = "qualtran-raw"
n_sys
n_anc
contract
atol
u_hash
resource
sig
```

Newer seals may also bind:

```text
oracle_code_hash
contracts_code_hash
resource_schema_version
```

`u_hash` is based on phase normalization, real/imaginary quantization, shape inclusion, and SHA-256.

`sig` is SHA-256 over canonical JSON fields. There is no timestamp, so repeated seals are byte-identical when the inputs and bundle are identical.

## Resource Accounting

FTQC cost is dominated by T gates and magic-state distillation. The seal records deterministic resource data from Qualtran `QECGatesCost`, such as:

```text
t
total_t
toffoli
and_bloq
clifford
measurement
rotation
```

Resource data is part of the seal integrity surface.
