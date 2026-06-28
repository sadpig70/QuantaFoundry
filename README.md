![QuantaFoundry hero](assets/QuantaFoundry_hero.png)

# QuantaFoundry

**QuantaFoundry** is an AI-native quantum software foundry.

It generates quantum software modules from high-level intent, verifies them with deterministic contract oracles, seals only proven outputs, and composes sealed modules into larger quantum applications.

> **Status (v0.7, 2026-06):** the verification core is public as **QPGF** →
> **https://github.com/sadpig70/QPGF** (157 self-verification tests green). The foundry layer
> around it is **substantially realized**: a key-free, cross-model-established library of
> **48 sealed modules** composed into **59 sealed applications** — Grover, QFT(2–4), Quantum Phase
> Estimation, and **Shor period-finding circuits that factor 15 = 3 × 5 and genuinely 21 = 3 × 7**
> (plus distinct-prime modular multipliers mod 33/35) — with **no human-asserted answer keys**
> anywhere in the trust chain, including the first *live* cross-model truth (`sx` = √X, established
> by six distinct runtimes + an algebraic proof). Later layers (self-extending GenSkill library,
> goal-autonomy, a gated multi-model panel, a falsification front, and an honest-decomposition
> guard) are now realized — see the spec's `What changed since v0.6` and §8.8.
>
> **v0.7+ adoption & hardening layer (Stage 0–5, non-destructive):** over the sealed core — a
> **QF-Discover** value function (objective novelty/composability via dependency-graph fan-in;
> c6x's leverage is captured *before* the fact), a decomposition optimizer (oracle-as-reward with
> reward-hacking structurally blocked), **OpenQASM3 export/ingest** with round-trip unitary identity
> (57/57 apps re-derived by an independent numpy oracle), a `qf` CLI, a **citable registry root**
> (`CITATION.cff`), a convention-independence audit, **ρ-discount validation** against constructed
> co-errors, and determinism env-pinning + an oracle-revocation protocol + ed25519 Sybil defense.
> Stages 0–5 are analysis/tool/verification layers; the **W2.4 cross-runtime relay** then grew the
> registry by two key-free primitives (`c7x`, `cr8_dag_gate` — 6-runtime panel convergence), and the
> **W6 payoffs** spent them and completed the QFT family: `c7x` on three N>64 distinct-prime modular
> multipliers (`cmul2_mod91/77/85`), `cr8_dag_gate` on an 8-qubit inverse-QFT (`iqft8`), the forward-QFT
> completion sealing `cr6/7/8_gate` → `qft5…8_pipeline`, and the **W6.5 capstone** composing those parts
> into a genuine distinct-prime Shor circuit `shor91` (factors 91 = 7×13; 15 qubits → Tier-1 STRUCTURAL).
> The **W7.1 QEC family** then opened the first *horizontal* algorithm class — quantum error-correction
> stabilizer encoders, all Clifford Tier-0 EXACT: the `[[3,1]]` bit-flip / phase-flip repetition encoders,
> a bit-flip syndrome-extraction unitary, and the **`[[9,1,3]]` Shor-code (1995) 9-qubit encoder** (512×512,
> golden built from closed-form parity/Sylvester maps independent of the gate library).
> The registry advanced from the v0.7-core root `3dae613d…` to the current **`06ca92d7…` (53 modules,
> 75 apps)**. Pure non-destructive growth: every prior seal, the 23 frozen consensus keys, and the
> fingerprint files reproduce byte-identically.
>
> **Guarantee split** (no exact-coverage overclaim): all **53 modules** are `unitary_equiv` (Tier-0 EXACT);
> the **75 apps** are 73 `unitary_equiv` + **1 `unitary_equiv_sampled`** (`ghz16`, sampled-dense two-path
> verified with a sealed seed, also Tier-2 sealed) + **1 `structural_wellformed`** (`shor91`, the W6.5
> Tier-1 capstone — a Merkle of sealed parts at 15 qubits, *weaker* than dense `unitary_equiv`, honestly
> labelled). The W7.1 QEC encoders are all `unitary_equiv` Tier-0. Authoritative tally:
> `registry/SEMANTIC-GUARANTEES.json` `headline_split`.
>
> **Full technical specification + evidence:** [`docs/QuantaFoundry-Technical-Spec.md`](docs/QuantaFoundry-Technical-Spec.md)
> (written for independent design review). Reproduction artifacts under `specs/`, `registry/`,
> `_workspace/crossmodel/`.

## Core Idea

Most AI coding tools can generate plausible quantum code. QuantaFoundry is built around a stricter rule:

```text
AI generates.
Oracle verifies (deterministically).
Registry remembers only sealed modules.
Skills reuse successful generation patterns.
```

The project combines QPGF-style PG/PPR specifications, reusable skill packs, multi-runtime AI generation, and deterministic quantum verification.

## QuantaFoundry vs QPGF (what is built today)

| Layer | Scope | Status |
|---|---|---|
| **QPGF** (core) | Deterministic verification termination oracle (ContractGate): contracts, seal tiers, registry, composition, multi-runtime, trust model | **Realized & public** |
| **QuantaFoundry** (foundry) | Key-free cross-model establishment, autonomous multi-persona generation, sealed-module → application composition, the gate→QFT→QPE→Shor library, self-extending GenSkill library, goal-autonomy, gated multi-model panel, falsification front | **Realized (v0.7)** — 48 modules · 59 apps |
| QuantaFoundry (remaining) | Intent UX, multi-backend adapters (Qiskit/Cirq/CUDA-Q), open-ended discovery of genuinely new methods/families | **Planned** |

The honest framing: QuantaFoundry does **not** introduce a new verification algorithm. The
deterministic, phase-aware verification it relies on reuses **established techniques** (exact
tensor contraction; stabilizer-tableau equivalence; ZX-calculus equivalence — see *Prior Art*).
Its contribution is the **systems integration**: turning that verification into an *AI-loop
termination oracle* with a binary tamper-evident seal, a sealed registry, and FTQC resource
accounting — wired so that **only what is proven can exist downstream**.

## What's built (v0.7)

The foundry layer is now exercised end-to-end. Every result below is reproduced from the working
tree; details and evidence are in [`docs/QuantaFoundry-Technical-Spec.md`](docs/QuantaFoundry-Technical-Spec.md) §8 (v0.7 work in §8.8).

- **Key-free, cross-model truth.** Six independent AI runtimes (gpt-5, gemini, grok, kimi, qwen,
  deepseek — six distinct model weights) independently authored each gate's reference *and*
  implementation; agreement is counted per physical weight-set, and each converged hash is also
  corroborated by a stack-independent **symbolic proof**. No gate's correctness rests on a human
  answer key. The same was done at the **application level** (intents *and* implementations), and
  v0.7 added the first *live* round: a new gate `sx` (√X) authored by six distinct runtimes that
  converged (MULTIMODEL) and was sealed against an algebraic proof (PROOF_BACKED).
- **48 sealed base modules** → **59 sealed applications**, the latter composed *only* from sealed
  parts, each re-verified by the oracle (C-app) and re-sealable byte-identically (`registry_root_hash`
  reproduces).
- **Algorithm layer:** Bell/GHZ (incl. a 16-qubit seal now carrying both a Tier-1 structural and a
  Tier-2 Clifford-tableau certificate), Grover, QFT(2–4) pipelines, Quantum Phase Estimation
  (2- and 3-bit), and **Shor period-finding** — sealed circuits measurably **factor 15 = 3 × 5 and
  genuinely 21 = 3 × 7** (distinct-prime arithmetic, not the N=15 special case; mod 33/35 multipliers
  also sealed), with modular arithmetic honestly decomposed into sealed primitives (not a matrix copy
  of the answer) — a discipline now **code-enforced** by the honest-decomposition guard.
- **Self-extending + autonomous:** a GenSkill library promotes generation *methods* to first-class
  assets, and a goal-autonomy loop recomposes sealed modules to the frontier (24 apps forged at human
  seed 0). A **gated multi-model panel** structurally requires ≥2 distinct weights for key-free
  intents (blocking same-weights co-error), and a **falsification front** red-teams the oracle/gate/
  consensus (documented gaps closed).
- **Internal consistency:** apps that rebuild a separately-sealed gate (e.g. `H·CNOT·H` = CZ)
  reproduce its hash **byte-for-byte** (6/6), and for every algorithm app the independent
  app-intent consensus, the independent app-circuit consensus, and the in-house seal **all agree**.
- **Adoption & hardening (v0.7+, non-destructive).** A **QF-Discover** value function ranks *what to
  build next* from objective dependency-graph fan-in (retrospectively capturing `c6x`'s leverage
  *before* the fact), and a decomposition optimizer searches cheaper sealed decompositions with the
  oracle as a hard reward (reward-hacking structurally blocked). Sealed apps **export to OpenQASM3**
  and re-import with round-trip unitary identity (57/57 re-derived by an independent numpy oracle),
  exposed through a single `qf` CLI and a citable `registry_root_hash` (`CITATION.cff`). A
  convention-independence audit scopes what `second_oracle` *derives* vs *assumes*; **ρ-discount is
  validated against constructed co-errors** (it collapses poisoned consensus to <2 independent); and
  determinism is env-pinned with an oracle-revocation protocol (fingerprint **145/145 intact**) and
  ed25519 Sybil defense. All non-destructive — the registry root is unchanged.

## Positioning

QuantaFoundry is not just a code assistant.

| Category | Main role | Relation to QuantaFoundry |
|---|---|---|
| Qiskit / Cirq / CUDA-Q | Quantum programming and execution frameworks | Backends to target |
| Classiq-style tools | High-level quantum synthesis | Adjacent (synthesis, not sealing) |
| VOQC/SQIR, Qbricks, MQT QCEC | Deterministic/phase-aware quantum verification | **Verification techniques QPGF reuses** |
| LLM coding assistants (QUASAR, Agent-Q) | Quantum code generation (simulator/RL reward) | Generators, *without* a binary seal/registry |
| **QuantaFoundry** | Verified AI quantum module generation, sealing, registry, and composition | This project |

## System Architecture

```text
User Intent
  -> PG/PPR QuantumSpec
  -> Generator Runtime (AI, may iterate; cannot self-declare success)
  -> Backend Adapter
       Qualtran          [realized]
       Qiskit            [planned]
       Cirq (standalone) [planned]
       CUDA-Q            [planned]
  -> Deterministic Oracle (ContractGate)
       matrix shape (C1)
       unitarity / phase preservation (C2)
       ancilla cleanliness / isometry (C3, C3-iso)
       golden equivalence up to global phase (C4)
       resource accounting (Qualtran QECGatesCost)
       deterministic signature
  -> Seal Tier selection (exact / structural / Clifford / Clifford+T)
  -> Sealed Registry (INV1-3: register-only-if-verified, seal-only compose, re-verify)
  -> Composable Quantum Apps (C-app: composed == app golden)
```

## Key Components

### 1. Quantum Intent Layer

Transforms natural language or PG/PPR documents into explicit quantum module specifications.

Example:

```text
Generate a 3-qubit QFT module.
Use direct decomposition.
Do not call a built-in QFT implementation.
Verify against an independently-authored analytical QFT matrix.
```

Output (`QuantumSpec.pg`): a `bloq`/code implementation block, a `golden` mathematical
reference, and metadata (`id`, `n_sys`, `n_anc`, `convention`).

### 2. Generator Runtime

An AI runtime generates candidate implementations. Multiple runtimes can compete or cooperate
(Codex, Claude, Gemini, Qwen, Kimi, Grok, GLM, Deepseek, …). The runtime is allowed to iterate,
but **it cannot declare success by itself** — only the oracle can.

### 3. Backend Adapters

- `Qualtran` — exact tensor contraction + resource accounting. **[realized]** (cirq and pyzx
  are used internally for the Clifford and Clifford+T seal tiers).
- `Qiskit`, `Cirq` (standalone), `CUDA-Q`, OpenQASM export. **[planned]**

### 4. Deterministic Oracle (ContractGate)

The oracle is the **termination condition** for the AI loop:

```text
exit 0  <=>  <id>.sealed.json exists  <=>  loop terminates
```

Contracts checked: matrix shape (C1), unitarity `U†U = I` and phase preservation (C2), ancilla
cleanliness / faithful isometry `V†V = I` (C3, C3-iso), golden equivalence up to global phase
(C4), compute-uncompute cleanliness (C4-uncompute), resource cost, and a deterministic
signature. Verification is **exact symbolic/numeric on the dense or structural representation —
never probabilistic measurement statistics.** Only oracle-passing modules become sealed artifacts.

### 5. Seal Tiers (scaling beyond the exact bound)

Exact dense verification is exponential (`2^n`) — this is the oracle's trust ceiling
("SmallNBound"). Seal Tiers extend trustworthy sealing to large circuits **without** building a
dense `2^n` matrix, by reusing established equivalence techniques:

| Tier | Range | Method | Status |
|---|---|---|---|
| **0 EXACT** | small | dense tensor contraction == golden | realized |
| **1 STRUCTURAL** | large composition trees | Merkle hash of sealed children (no dense) | realized |
| **2 CLIFFORD** | large Clifford | stabilizer tableau, O(n²) | realized (20q GHZ encoder) |
| **3 CLIFFORD+T** | large universal | ZX-calculus equivalence to an independent golden circuit (pyzx) | realized (16–30q) |

All tiers are **exact (not approximate)**. Tier-3 is **sound but conservative**: it seals only
when ZX *proves* equivalence; non-reduction is rejected, never wrongly sealed.

### 6. Sealed Registry

Stores only verified modules and enforces composition invariants (INV1: registration requires a
passing `verify_seal`; INV2: only sealed modules compose; INV3: every composition is re-verified
and re-sealed).

Each sealed artifact includes:

```text
id, sealed, convention, n_sys, n_anc, contract, tier, u_hash, resource, sig,
oracle_code_hash, contracts_code_hash, resource_schema_version
```

### 7. GenSkill System  *[realized, v0.5–0.7]*

Reusable generation **methods** are promoted to a first-class, introspectable catalog
(`scripts/genskills.py`, `registry/GENSKILL-CATALOG.json`): named, parametrized GenSkills, each with
metadata (kind, params, required sealed modules, golden-construction method) and a deterministic
`make_spec(n)`. The catalog is tamper-evident via a per-skill source hash + `catalog_root_hash` (the
method-side counterpart of `registry_root_hash`). The boundary stays sharp — **generation ≠
verification**: a GenSkill mints no trust; its output is a *candidate* spec that still must pass the
oracle to be sealed. *(Open-ended discovery of genuinely new methods/families remains research-stage —
the loop recomposes known methods, it does not invent new mathematics.)*

## Trust & Security Model

A sealing system is only as trustworthy as its trust boundary. QuantaFoundry/QPGF is explicit
about what the seal does and does **not** guarantee.

### What a seal is

The signature is a **sha256 of canonical fields** — i.e. a **tamper-evident** signature, **not**
a secret-key cryptographic forgery-proof. "Proven" is therefore **conditional** on three things:

1. **Verifier integrity** — the oracle code that produced the seal is genuine.
2. **Golden legitimacy** — the reference the implementation is checked against is itself correct
   and independent.
3. **Central recomputation** — a trusted party re-runs `verify_seal` rather than trusting a
   submitted seal blindly.

### Mechanisms (realized in QPGF)

- **Provenance binding** — `oracle_code_hash` and `contracts_code_hash` are folded into the
  signature; `verify_provenance` detects seals produced by a different bundle.
- **Recompute policy** — registration always re-computes centrally; externally-submitted seals
  are never trusted directly. Demonstrated: external-runtime seals are byte-identical to the
  central recomputation.
- **Bundle integrity** — `BUNDLE.sha256` manifest hashes every bundle file; tamper is detected.
- **Deployment-trust gate** — `verify_bundle` checks bundle integrity **and** a signature before
  any seal is trusted, returning `TRUSTED / INTEGRITY_ONLY / UNTRUSTED_SIGNATURE / TAMPERED`.
  Release signing (GPG, or keyless **Sigstore** via CI) moves the trust root *outside* the local
  files. Honest limit: signing **relocates** trust to a public key / transparency log — it does
  not eliminate it.

### Golden legitimacy (the subtle attack)

If the *same* AI writes both the implementation and the golden in one context, both can converge
on the *same wrong* target and the check passes vacuously. Mitigations:

- **golden_guard** — statically blocks self-reference (golden copying the implementation's output)
  and trivial/identity goldens.
- **CrossGen** — *author isolation*: the golden and the implementation are produced by **separate,
  isolated runtimes** from the same intent, neither seeing the other. Agreement then means the
  implementation passed an *independently authored* golden. Demonstrated on real runtimes
  (golden by Qwen, implementation by Codex → sealed, hashes matching the answer key).

## Verification Principle

QuantaFoundry never treats generated code as complete because it looks reasonable.

```text
spec_guard exit 0
golden is independent (golden_guard / CrossGen)
verify_seal exit 0  ->  sealed artifact exists
deterministic rerun is byte-identical
(for deployment) verify_bundle = TRUSTED
```

## MVP Scope & status

### MVP-1: Sealed module generation — *realized*
**48 modules sealed** (the core gate set `X, Z, H, CNOT, Toffoli, Swap, QFT2–4`, the phase/rotation
gates `S, T, CZ, iSWAP, CS, CCZ`, the controlled-phase family `controlled-T/S†/T†` and `CRₖ`/`CRₖ†`,
`Fredkin`, the multi-controlled-X family up to `c6x`/MCT-6, `sx`/√X, and ±α_k Ry primitives k=2..10).
Every module has a `.pg` spec, passes `verify_seal`, and re-seals byte-identically.

### MVP-2: Composition — *realized*
**59 applications sealed** from sealed parts (Bell, GHZ-3/4, 16-qubit GHZ with Tier-1+Tier-2 seals,
Grover, QFT2–4 pipelines, inverse-QFT, QPE, controlled modular multiplication incl. distinct-prime
mod 33/35, and Shor factoring 15 and genuinely 21). Each gets its own C-app golden check and sealed
artifact. Recursive trees (Shor → modular-mult → Fredkin; QPE → inverse-QFT) and rediscovery
cross-checks (6/6 byte-identical) demonstrated.

### MVP-3: Multi-runtime / key-free establishment — *realized*
Six distinct-weight runtimes establish gate truth, gate implementation, app intent, and app
implementation by cross-model consensus + symbolic proof — **zero human answer keys**. Dissent
(a runtime's wrong submission) is detected and outvoted; independent runtimes sometimes find
*shorter* correct decompositions than the in-house one. v0.7 added a **gated panel** that enforces
≥2 distinct weights for key-free intents, the first **live** cross-model round (`sx`), and
cross-runtime co-error probes (on a convention-contested QFT the consensus correctly refused to seal).

## Directory Layout

```text
QuantaFoundry/
├── README.md                     # this file
├── RELEASE-NOTES.md              # v0.7 + v0.3 milestone summaries + reproduce commands
├── NOTICE.md                     # vendored-component (QPGF) provenance & attribution
├── LICENSE                       # MIT
│
├── docs/
│   └── QuantaFoundry-Technical-Spec.md   # full spec + evidence + review questions (START HERE)
│
├── specs/                        # human/AI-readable PG specifications (the "source")
│   ├── modules/*.pg   (48)       #   one gate per file: bloq impl + golden ref + meta
│   └── apps/*.app.pg   (59)      #   one application per file: app_golden + decomposition plan
│
├── registry/                     # the sealed library (the "trust capital")
│   ├── modules/*.sealed.json (48)#   tamper-evident gate seals (u_hash, contract, provenance, sig)
│   ├── apps/*.sealed.json (59+)  #   application seals (C-app) + cached leaf re-seals
│   └── {REGISTRY-MANIFEST,DEPENDENCY-GRAPH,SEMANTIC-GUARANTEES,GENSKILL-CATALOG}.json
│
├── scripts/                      # foundry-layer tooling (v0.4–0.7)
│   ├── genskills.py, goal_autonomy.py        #   GenSkill library + goal-autonomy loop
│   ├── gated_panel.py, live_dispatch.py, seal_sx.py   #   multi-model panel + live cross-model
│   ├── red_team.py, bounty_adjudicate.py, cross_runtime_round.py  #   falsification front
│   ├── seal_module.py, verify_t1_closure.py  #   honest-decomposition closure (decomp guard)
│   ├── arith_family.py, clifford_routing.py, resource_report.py, dep_graph.py, second_oracle.py
│   ├── sampled_dense_verify.py, zx_routing.py, global_phase_tracker.py   #   S1: Tier-1 trust-closure
│   ├── discover.py, decomp_optimizer.py      #   S2: QF-Discover value function + decomposition optimizer
│   ├── qasm_export.py, qasm_ingest.py, qf_cli.py, citation_gen.py, seal_gate_ci.py  #   S3: OpenQASM3 + qf CLI + citable + CI
│   └── convention_audit.py, rho_validation.py, determinism_env_check.py, oracle_rollback_protocol.py, runtime_identity.py  #   S4–S5: consensus audit + hardening
│
├── .pgf/                         # the foundry implementation (PG/PGF orchestration)
│   ├── autoforge/
│   │   ├── autoforge.py          #   F2: seal base gates (combine → verify → anti-swap → register)
│   │   └── forge_apps.py         #   F3: compose sealed modules → apps, with rediscovery cross-check
│   ├── keyfree/                  #   KeyFreeConsensus engine + cross-model pipelines
│   │   ├── consensus.py          #     independence-unit voting + source generators
│   │   ├── consensus_keys.json   #     frozen, provenance-tagged answer keys (no human seed)
│   │   ├── ingest_crossmodel.py  #     Round 1/2: gate golden+bloq consensus
│   │   ├── ingest_app_golden.py  #     Round 3/4: app-intent consensus
│   │   ├── ingest_app_bloq.py    #     Round 4: app-implementation (circuit) consensus
│   │   ├── seal_crk.py           #     parametric controlled-Rₖ / Rₖ† gate family sealing
│   │   ├── formal_spec.py        #     symbolic-proof source (sympy, stack-independent)
│   │   └── freeze_/seal_crossmodel.py, crossmodel_adapter.py, build_consensus_keys.py
│   ├── personas/                 #   isolated-author persona prompts (golden / bloq / adversary)
│   ├── DESIGN-*.md               #   PG/PGF designs (AutoForge, KeyFreeConsensus)
│   └── status-*.json             #   per-thread execution state + results
│
├── _workspace/crossmodel/        # cross-model reproduction EVIDENCE (cited by spec §8.2–8.6)
│   ├── *-BRIEF.md, intents.json  #   the briefs/intents handed to each runtime
│   ├── submissions*/             #   raw independent submissions from 6 external runtimes
│   ├── apps/, apps2/             #   Round 3 (apps) and Round 4 (algorithm-layer) rounds
│   └── *-REPORT.json             #   consensus results (who agreed, dissent, hashes)
│
└── .agents/skills/qpgf-oracle/   # vendored QPGF verification oracle — USED, never modified
    ├── scripts/                  #   verify_seal.py, registry.py, app_assemble.py, contracts.py, …
    ├── references/               #   contract spec, oracle usage, deployment-trust docs
    ├── examples/                 #   example .pg / .app.pg specs
    └── BUNDLE.sha256, DEPENDENCIES.lock   # integrity manifest + pinned deps
```

The generator-skill library (GenSkill) and goal-autonomy are now realized (see `scripts/`);
multi-backend adapters (Qiskit/Cirq/CUDA-Q) and open-ended discovery of genuinely new
methods/families remain the planned next foundry steps.

## Non-Goals

Early versions should not attempt:

- large-N quantum simulation
- hardware execution
- probabilistic measurement-only validation
- unconstrained natural-language-to-hardware deployment
- trusting AI self-evaluation as a correctness proof
- **treating the seal signature as cryptographic forgery-proof without the deployment-trust chain**

## Prior Art & Honest Positioning

Deterministic, phase-aware quantum verification is **not new** — it exists in
**VOQC/SQIR** and **Qbricks** (Coq matrix / path-sum semantics) and in **MQT QCEC**
(decision-diagram + ZX-calculus equivalence checking). QPGF's seal tiers **reuse** the tableau /
ZX techniques rather than inventing new ones. What has no single-tool precedent is the
**combination**: an AI-autonomous-loop **termination oracle** + binary tamper-evident
**seal/registry** + **FTQC resource** accounting, integrated as one system. Generation-side work
(QUASAR, Agent-Q) uses simulator/RL reward with no binary seal or registry. This honest framing
is the project's defensible position. *(Detailed comparison with citations lives in the QPGF
repo.)*

## Design Motto

```text
Generate boldly.
Verify deterministically.
Seal only what survives.
Compose only what is sealed.
```

## First Build Target — realized

```text
Qualtran backend + QPGF-style PG specs + deterministic seal oracle + sealed registry.
```

This narrow-but-strong foundation is **done and public** (https://github.com/sadpig70/QPGF):
AI-generated quantum software that can *deterministically prove its unitary matches an
independent reference, conditional on a stated and auditable trust chain*. The foundry layer
(key-free establishment, composition, GenSkill library, goal-autonomy, multi-model panel —
realized; intent UX and multi-backend adapters still planned) builds outward from there.

## License

QuantaFoundry is released under the **MIT License** — see [`LICENSE`](LICENSE).
© 2026 Jung Wook Yang.

The vendored verification oracle under `.agents/skills/qpgf-oracle/` is from the public
[QPGF](https://github.com/sadpig70/QPGF) project (also MIT) and is used as-is, not modified.
Provenance and third-party notes are in [`NOTICE.md`](NOTICE.md).
