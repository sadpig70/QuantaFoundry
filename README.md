![QuantaFoundry hero](assets/QuantaFoundry_hero.png)

# QuantaFoundry

**An AI-native quantum software foundry.** It generates quantum modules from high-level intent,
verifies them with a **deterministic contract oracle**, seals only proven outputs, and composes
sealed modules into larger quantum applications — with **no human-asserted answer keys** anywhere
in the trust chain.

```text
AI generates.
Oracle verifies (deterministically).
Registry remembers only sealed modules.
Skills reuse successful generation patterns.
```

The trust comes not from the AI's judgement but from **deterministic gates + tamper-evident seals**.

---

## Status

- **95 sealed modules · 466 sealed applications** · registry root `6e7d2a70ef9e…`
  (live counts are authoritative in [`registry/REGISTRY-MANIFEST.json`](registry/REGISTRY-MANIFEST.json)).
- Verification core is public as **QPGF** → https://github.com/sadpig70/QPGF (157 self-tests green).
- Pure non-destructive growth: every prior seal, the 23 frozen consensus keys, and the oracle
  fingerprint files reproduce **byte-identically**.

### Verify it yourself

```bash
python scripts/reproduce_all.py
# expect: REPRODUCED · root_hash 6e7d2a70ef9e… · second_oracle 83/83 · behavior pass
```

---

## What's real

- **Sealed library**: Bell/GHZ, QFT(2–8), QPE, Grover & amplitude amplification/estimation,
  Trotter/Suzuki Hamiltonian simulation, VQE/QAOA, query algorithms (DJ/BV/Simon), QEC stabilizer
  encoders + transversal logical gates, QSVT (block-encoding → QSP → polynomial transforms),
  fermionic encodings (Jordan-Wigner **and Bravyi-Kitaev/parity**), an H₂ molecular block-encoding,
  a generic qROM + SELECT-PREPARE data-oracle layer, the [[5,1,3]] code as a pentagon graph code
  (5-to-1 magic-state distillation core), the first **non-abelian group oracles + Fourier transform**
  (S₃ and D₄, driving a dihedral hidden-subgroup sampling observation, extended by an **S₄ = V₄⋊S₃
  multiplication oracle** whose companion witness recovers the octahedral integer (3,1) irrep and
  proves — as a closed-negative — that a full S₄ Fourier still needs ζ₃ because its (2,2) irrep
  cannot be an integer unitary, and the **complementary positive** — a full **Q₈ (quaternion group)
  Fourier transform** sealed with no new modules, since Q₈ has no order-3 element so its 2-dim irrep
  closes in ℤ[i] and every 1-dim irrep is real ±1: the minimal non-abelian group whose Fourier needs
  no ζ, built by a coset transform over N={±1} using only sealed H/S/CZ/SWAP/Toffoli/Fredkin gates,
  extended by a witness that the **hyperoctahedral group B₃ = (ℤ₂)³⋊S₃** (48 signed permutations) is a
  **rational group** — every element is conjugate to all its coprime powers, so its entire character
  table is integer and its Fourier closes ζ-free, the ζ-free monomial lineage beyond Q₈; its 12-qubit
  multiplication oracle is shown circuit-realizable by a 154-gate reversible synthesis, observed rather
  than sealed since dense 12-qubit assembly is impractical),
  a **qutrit-embedded
  ternary-arithmetic** layer (qudit axis), a **topological logical-operation stack** (surface-code
  encoder + coherent lattice surgery + 2×2 toric ground state, closing the FTQC logical stack),
  **GF(2ᵏ) finite-field arithmetic** (multiply/inverse/Frobenius/primitive-orbit, completed by a
  general GF(8) product and a **Reed-Solomon RS(7,3) systematic encoder + syndrome core** — the
  21-qubit encoder is structural, repaid to an exhaustively verified message→parity permutation
  with an exhaustive distance-5 MDS observation), **Ising/Majorana braiding**
  (Yang-Baxter — including a **physical 4-Majorana braid word** B₁₂B₂₃B₁₂ over Jordan-Wigner modes,
  whose companion witness confirms the braid-group representation is entirely Clifford, its Majorana
  conjugation an SO(4) signed permutation, and B₂₃ a rediscovery of the sealed Bogoliubov gate — a
  pre-seal check that refuted the external "non-Clifford braid word" claim), a **Fibonacci-anyon braid + knot-word layer** (field ℚ(ζ₅,√φ); F-move basis change
  and 3-strand braid words up to the figure-eight knot — inverse generators realized as z5 powers —
  whose closures feed a **three-path** Jones observation (weighted trace vs Temperley-Lieb state-sum
  vs skein) plus an integer Alexander third invariant; connected-sum multiplicativity and
  amphichirality observed exactly, and the half-twist σ₁σ₂σ₁ rediscovered as the F-move —
  sealed unitaries only, invariant values are observations), **measurement-based computation** (cluster state + coherent gate teleportation),
  a **Clifford quantum cellular automaton** (exact discrete-time dynamics), a **non-Clifford
  dual-unitary brickwork + kicked Floquet unitary** (space-time-dual gate at J=π/8; the
  infinite-temperature two-point function vanishes off the light ray exactly and the on-ray value
  matches a closed-form one-qubit transfer-channel power — two independent paths; plus an OTOC
  operator circuit whose trace reproduces the dense out-of-time-order correlator with light-cone
  operator growth, and an integer Floquet winding Σε/2π; plus an **operator-entanglement witness**
  confirming the dual-unitary gate has a maximally flat operator-Schmidt spectrum (s²=¼ each →
  EE=2 exactly, a dyadic value with no irrational-log ambiguity, unlike EE=1 for CNOT/CZ) — all
  observations), a **fermionic SWAP** and a **Bogoliubov pairing gate** (particle-number-breaking Gaussian —
  exp(iπ/4·XX), extending the sixth matchgate/SO(2n) path to the pairing sector — with a 4-site
  Kitaev sweet-point ground state whose Z₂ topological invariant is read off as a Pfaffian sign,
  lifted to **2D ℤ topology** by a Qi-Wu-Zhang Chern-insulator witness that pins the lower-band Chern
  number as an exact integer two independent ways — a closed-form Dirac mass-sign formula over the
  four high-symmetry points and a gauge-invariant Fukui-Hatsugai-Suzuki lattice sum — recovering the
  phase diagram C=±1 for 0<|m|<2 and C=0 for |m|>2, with the gap closing exactly at the Dirac points
  m∈{−2,0,2}),
  a **Z₂ lattice gauge theory** (Gauss-law encoder), a **ZX-calculus third verification path**
  (Clifford fragment), a **path-sum ℤ[ω₈] fourth, a stabilizer-decomposition fifth, a free-fermion/Majorana SO(2n)
  sixth, a tensor-network exact-contraction seventh, a QMDD reduction-canonical-form eighth, an
  ANF/bit-vector ninth, and a Gröbner/ℤ[ω] phase-ideal tenth verification path** (the fifth expands non-Clifford
  diagonal gates into exact Clifford-sum branches and evolves each branch as an affine-support quadratic form — no
  matrix products; 128 sealed Clifford+T apps re-verified, skips recorded with reasons; the eighth executes circuits
  over a shared-node decision diagram — reduction/merge, not tensor contraction — re-verifying 158 sealed apps
  with observed node compression, e.g. ghz10 in 51 nodes vs dense dim 1024; the ninth represents each
  output bit of a computational-basis permutation circuit as an Algebraic Normal Form polynomial over
  GF(2) and checks the gate sequence against the sealed matrix as a Boolean-function identity — amplitude-free,
  re-verifying 144 permutation apps with the remaining non-permutation apps skipped by recorded reason; the tenth
  targets exactly the ninth's blind spot — diagonal and monomial phase circuits U|x⟩=ω_M^{f(x)}|π(x)⟩ that the
  amplitude-free ANF path skips — verifying the phase polynomial f by ideal membership in ⟨x_i²−x_i, M⟩ over ℤ_M
  with a genuine Buchberger normal form, complementary cover to ANF),
  a **magic resource-theory exact certificate layer**
  (stabilizer extent/robustness with primal + dual + zero-gap certificates in exact ℚ(√2) arithmetic
  — ξ(|T⟩)=4−2√2, R(|T⟩)=√2, bounded ξ(|CS⟩) ∈ [8/5, (11+2√10)/9]; tight T-count lower-bound
  certificates, and a Clifford-invariant proof that |T⟩⊗|T⟩ cannot be deterministically converted
  to |CS⟩; extended to **channel magic** via the T-channel Choi state — ξ(Φ_T)=ξ(|T⟩)=4−2√2 by the
  Choi isomorphism, with catalysis preserving the resource state), a **state-independent contextuality
  certificate** — the Peres-Mermin magic square of nine two-qubit Pauli observables, where every row and
  the first two columns multiply to +I while the last column multiplies to −I, so the product of all nine
  counted by rows (+1) contradicts the count by columns (−1): a purely algebraic parity proof that no
  noncontextual ±1 value assignment exists, independent of any quantum state — a different resource lens
  from magic (extent/robustness), quantified further by an **exact-rational contextual-fraction certificate**
  that lifts the qualitative parity proof to a number: an internal exact-rational linear program (no external
  solver, no floating point) whose noncontextual fraction is 0 because every one of the 512 global ±1
  assignments violates at least one context, giving contextual fraction CF=1, with a depolarizing-visibility
  family CF(v)=v recovered exactly from an explicit uniform primal witness and the parity dual certificate,
  a **hypergraph-product qLDPC code** (generic classical→CSS construction; the small [[8,1,2]] instance plus a **distance-3 [[27,4,3]]** Tillich-Zémor product of the Hamming [7,4,3] and repetition [3] codes, sealed dense-free as a 27-qubit Tier-2 stabilizer tableau — both classical seeds full-rank so the transpose sectors are trivial and the distance stays 3, verified by an explicit weight-≤2 logical-operator search),
  the **[[8,3,2]] triorthogonal colour code with a transversal non-Clifford logical gate** (the
  cube code: T^±1 on all 8 vertices projects to a logical CCZ, witnessed by the integer
  triorthogonality condition and an exact logical-matrix check — the first non-Clifford transversal
  logical gate in the registry), the **[[15,1,3]] punctured Reed-Muller code** (the canonical
  15-to-1 magic-state-distillation substrate: a full logical-input Clifford encoder sealed at
  Tier-2 by canonical stabilizer tableau, plus T^⊗15 whose code-space action equals logical T† —
  proven by the mod-8 codeword-weight integer witness and a dense-free symbolic stabilizer
  back-propagation of all 14 stabilizers; distance exactly 3, exhaustively checked; the encoder's inverse is sealed as a **decoder** that is
  the measurement-free coherent syndrome-extraction core of 15-to-1 distillation — valid codewords
  decode to logic + zero syndrome (accept), weight-1 errors expose a non-zero syndrome; success
  rate is an observation), the registry's first **cyclic algebraic CSS code** — a **[[15,7,3]] quantum
  Hamming/BCH code** built from the dual-containing binary cyclic code [15,11,3] (generator polynomial
  x⁴+x+1), its |0_L⟩ prep sealed dense-free as a 15-qubit Tier-2 stabilizer tableau, with a witness
  confirming the CSS orthogonality (H·Hᵀ=0), the exhaustive distance-3 (minimum weight over C∖C^⊥), the
  cyclic-shift invariance that distinguishes it from the punctured Reed-Muller code, and the |0_L⟩
  stabilization by every X- and Z-check with +1 sign, extended to a **distance-5 [[31,11,5]] quantum BCH
  code** from the dual-containing narrow-sense BCH [31,21,5] over GF(2⁵) (generator m₁·m₃, the first d≥5
  code in the registry), its 31-qubit |0_L⟩ prep sealed as a Tier-2 stabilizer tableau with a witness
  that exhaustively rules out any weight-≤4 codeword (so d(C)≥5, matching the BCH designed distance),
  a **3/4-qubit Schur-Weyl transform pair with decoders** (direct Clebsch-Gordan cascade, J²/Jz
  simultaneous-diagonalization witness + S₃/S₄ duality sector preservation; the decoders make weak
  Schur sampling executable, with a symmetric-subspace reflector 2P−I and a Dicke |D⁴₂⟩ preparation
  as consumers), a **4-site AKLT/VBS state
  preparation** (tensor-network MPS class: sequential conditioned isometries, independent MPS
  contraction match + parent-Hamiltonian annihilation witness), and **open-system CPTP channels**
  (Stinespring dilation of bit-flip / phase-damping / amplitude-damping at the dyadic ½ point plus a
  fully-depolarizing 4-Kraus Pauli-twirl; the sealed dilation unitary's environment partial-trace
  reproduces the target Kraus map exactly, and composing sealed dilations yields the composite channel),
  plus an **exact Pauli-channel diamond-norm distance certificate** (consuming the sealed bit-flip
  dilation by partial trace; the diamond distance between Pauli channels equals the ℓ₁ distance of
  their Pauli spectra — a dyadic exact value — with the maximally-entangled state as the primal
  witness confirmed optimal against a global pure-state search; the exactness is honestly scoped to
  the Pauli-diagonal island, general non-Pauli channels remaining observation-only), complemented by
  an **exact diamond-norm certificate for coherent (unitary) channels** — the complementary non-Pauli
  island — where the Aharonov-Kitaev-Nisan/Watrous arc formula ‖Φ_U−Φ_V‖◇ = 2·sin(min(Θ/2,π/2)) over
  the eigenphase arc Θ of U†V yields cyclotomic-surd exact values (‖Φ_T−Φ_I‖◇ = √(2−√2), ‖Φ_S−Φ_I‖◇ =
  √2, and the integer ‖Φ_CZ−Φ_I‖◇ = 2 at maximal distinguishability), cross-checked three ways (arc
  formula, convex-hull distance, and a doubled-space state search), and the
  registry's first **code-concatenation layer** — `concat_513_513` = [[5,1,3]]∘[[5,1,3]] = [[25,1,9]],
  a 25-qubit Tier-2 Clifford encoder built purely from six [[5,1,3]] encoder blocks (H/CNOT/CZ, no
  new modules), sealed via a canonical stabilizer tableau (no dense 2²⁵); its witness reconstructs
  all 24 stabilizers by symbolic symplectic back-propagation and matches the concatenation-theorem
  structure exactly (20 inner-block + 4 outer-lifted generators), with the distance-9 = 3×3 claim
  honestly scoped as an observation (concatenation theorem + block-local minimum weight, not an
  exhaustive 2²⁴ search; the seal certifies only the encoder's stabilizer structure).
- **Shor period-finding** that factors 15 = 3×5 and **genuinely 21 = 3×7**, up to a distinct-prime
  structural frontier (`shor69 … shor219 … shor3683`, 25 apps, sealed via a `c7x→c12x` multi-control
  ladder; every one subspace-permutation verified against independent integer arithmetic — the newest
  ones discovered and sealed unattended by the autonomous factory loop, then auto-repaid to that grade,
  the latest being `shor219 = 3×73` at 16 qubits with an exhaustive 65536/65536 basis-permutation check).
- **Key-free cross-model establishment**: the first *live* cross-model truth (`sx` = √X) settled by
  six distinct runtimes + an algebraic proof — no answer key.
- **Autonomous loop** (`qfa-loop` skill): discover → seal → verify → commit, gated end-to-end by the
  deterministic oracle. A **parametric frontier factory** seals arbitrary distinct-semiprime Shor
  apps, regression-gated against existing seals (byte-identical).
- **Adoption/hardening**: OpenQASM3 export/ingest (round-trip unitary identity), a `qf` CLI, a citable
  registry root, convention-independence audit, oracle-revocation + ed25519 Sybil defense.

## Honest boundaries (no overclaim)

- **seal ≠ run ≠ verify**, **approximation ≠ exact**, **structural ≠ dense**.
- **`REPRODUCED` ≠ correct**: one-command reproduction proves byte-identical *determinism*, not
  correctness. Correctness comes from the oracle's independent checks (C1–C4, a second dense oracle,
  and the subspace/resource witnesses) — not from the fact that a run reproduces.
- Modules + most apps are `unitary_equiv` (exact). `ghz16` is `unitary_equiv_sampled`. The large Shor
  apps (15–20 qubits) stay Tier-1 (dense infeasible), but their **modexp core is now
  `subspace_permutation_verified`** — exact permutation on the computational basis by *independent*
  integer arithmetic (path A = circuit-gate permutation vs path B = `w·a^c mod N`), with adversarial
  teeth. This is a real strengthening over bare Merkle structure, yet **still weaker than full dense
  unitary equivalence** (H·iQFT are excluded); period/factor readout stays illustrative only.
- Authoritative tier split: [`registry/SEMANTIC-GUARANTEES.json`](registry/SEMANTIC-GUARANTEES.json) `headline_split`.

---

## Learn more

| Doc | What |
|---|---|
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Full architecture, components, trust model, and the milestone narrative |
| [`docs/QuantaFoundry-Technical-Spec.md`](docs/QuantaFoundry-Technical-Spec.md) | Complete technical specification + evidence (for independent design review) |
| [`.pgf/external/REVIEW-REQUEST.md`](.pgf/external/REVIEW-REQUEST.md) | Adversarial review request (proposal questions) for external critique |
| [`.agents/skills/qfa-loop/SKILL.md`](.agents/skills/qfa-loop/SKILL.md) | The autonomous seal loop (engine, modes, invariants) |
| [`.agents/skills/qpgf-oracle/SKILL.md`](.agents/skills/qpgf-oracle/SKILL.md) | The deterministic termination oracle (ContractGate) |

### The autonomous seal loop at a glance

[![QFA-Loop — autonomous seal loop](assets/qfa_loop.svg)](.agents/skills/qfa-loop/SKILL.md)

`Bootstrap → Round(SelectNext → PlanNode → Implement → VerifyGate → GuardCheck → Record → SyncCheckpoint) → Stop`.
The AI *executes* the loop, but **pass/fail is decided only by executable machine gates** (`VerifyGate`,
`GuardCheck`) — never by the AI — and a round **commits only when fully verified**. See
[`qfa-loop`](.agents/skills/qfa-loop/SKILL.md).

Reproduction artifacts live under `specs/`, `registry/`, and `_workspace/crossmodel/`.

## Non-goals

Not a hardware QPU stack, not a speed-optimized simulator, not a claim of dense verification at
arbitrary scale (large apps are explicitly structural). It is a **trust-first** foundry: correctness
and tamper-evidence over coverage breadth.

## License

See [`LICENSE`](LICENSE) and [`CITATION.cff`](CITATION.cff) (the registry root is citable).
