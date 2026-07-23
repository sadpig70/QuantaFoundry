# QuantaFoundry — CHANGELOG

> Version/milestone history extracted from the Technical Spec header (QF-0711 U5a).
> Live current state is authoritative in `README.md` / `registry/REGISTRY-MANIFEST.json` /
> `registry/COUNT-ONTOLOGY.json`. This file is append-only narrative — not a current-state source.

## Version deltas ("What changed since vX")

> **What changed since v0.3:** (1) Shor extended to **N=21 = 3 × 7 with genuine modular arithmetic**
> (honest reversible synthesis, no MatrixGate) — N=15 was a 2⁴−1 degeneracy; (2) **app-level**
> cross-model corroboration done (EXT v04: app-golden 4/4 + app-bloq 4/4) and consensus **necessity**
> demonstrated by a true-divergence probe (EXT v05: free-parameter intents diverge); (3) a
> **second, Qualtran-independent oracle** re-checks sealed unitaries (62/62); (4) **goal-autonomy**
> extended to multiple families (GHZ + cluster) with autonomous sealing (human seed 0); (5) per-seal
> **semantic_guarantee** layer (Tier-1 ≠ unitary_equiv, made explicit). Library now **46 sealed
> modules → 57 sealed applications**, every primitive established with **zero human answer keys** (§8).
> **What changed since v0.5:** the GenSkill library became *self-extending* (§8.7): (1) an
> **arithmetic-synthesis** skill synthesizes controlled modular multipliers (×a mod N) via MMD
> reversible synthesis into sealed MCTs — reproducing all 6 committed multipliers' sealed unitaries;
> (2) a **continuous-rotation W-state** family — the first algorithm-level states needing irrational
> Ry angles (α_k=arccos√(1/k) primitives, sealed with global-phase-tolerant C4), W₃–W₁₀ autonomously
> sealed; (3) goal-autonomy gained an **unmanned loop-to-frontier** that recomposes sealed modules
> until every gap is done or blocked, then names its own missing prerequisites; (4) an
> **analytic-golden** skill captures the closed-form gate-construction methods (Z^t phase, controlled-R_k,
> DFT) — reproducing 17 committed gate modules' sealed unitaries; (5) the catalog gained a **method
> self-seal** (per-skill source hash + `catalog_root_hash`, tamper-evident — the method-side counterpart
> of `registry_root_hash`). The library grew to **46 sealed modules → 57 sealed applications**
> (24 forged autonomously, human seed 0, zero new modules beyond the Ry primitives).
> **What changed in v0.5:** a **GenSkill library** (`qf_witness/ops/genskills.py`,
> `registry/GENSKILL-CATALOG.json`) promotes generation *methods* — previously ad-hoc code — to a
> first-class, introspectable catalog, the method-side counterpart of the result registry. goal-autonomy
> consumes it. GenSkill mints no trust; its output still must pass the oracle to be sealed (§8.7).
> **Honesty calibration (this version):** several v0.3 claims are scoped down — see §3/§10/§11 and the
> per-section notes. "Non-linear production capacity" is now stated as a **hypothesis** with first
> evidence, not a result.
> **What changed since v0.6 (v0.7, §8.8):** (1) **Clifford Tier-2 routing** — the sole STRUCTURAL
> (Tier-1) app `ghz16` now also carries a stabilizer-tableau Tier-2 seal, closing the one weak-guarantee
> gap (companion seal, not replacement); (2) **distinct-prime arithmetic** — sealing `cmul2_mod33`
> (3×11) and `cmul2_mod35` (5×7) surfaced a missing prerequisite `c6x` (MCT-6), sealed key-free, after
> which the GenSkill engine was *evolved* (honest framing: a new primitive opens a family, not "infinite
> reuse"); (3) **gated multi-model panel** (§8.8) that structurally enforces ≥2 distinct-weights for
> key-free/ambiguous intents (B4 co-error blocked), validated by replaying the EXT v05 6-runtime data;
> (4) **first *live* cross-model truth** — a new intent `sx` (√X) was authored by 6 distinct runtimes
> that converged (MULTIMODEL) and was sealed with a frozen consensus key triangulated by an algebraic
> proof (PROOF_BACKED); (5) a **falsification front** (red-team of the oracle/gate/consensus) + an
> **honest-decomposition guard** that closes the "hollow seal" gap (a custom bloq asserting a literal
> unitary) on both the module and app sealing paths, **without modifying the fingerprinted oracle**
> (existing seals byte-identical); (6) **cross-runtime co-error rounds** that, on a genuinely
> convention-contested intent (2-qubit QFT), exercised the contested near-tie guard on *real* multi-model
> data (it refused to seal an under-specified intent). Library grew to **48 sealed modules → 59 sealed
> applications**; frozen consensus keys: **23**; `registry_root_hash` `3dae613d…` reproduces byte-identical.

> **What changed in v0.7+ (Stage 0–5 process plan):** non-destructive analysis/tool/verification layers
> over the sealed core — **through S5** the registry root `3dae613d…` and all 48/59 seals stay
> **unchanged** (no new seals; the fingerprinted oracle files untouched). **(S0)** `second_oracle`
> independent re-derivation extended to full coverage + a Tier-0/1 headline split (no exact-coverage
> overclaim). **(S1)**
> Tier-1 closure — `ghz16` raised to `unitary_equiv_sampled` (sampled-dense two-path, sealed seed; **zero
> structural-only**), a ZX-routing path (infrastructure self-test 6/6; immediate target 0 — honest
> negative), and a global-phase tracker (controlled-pair composition proven safe). **(S2) QF-Discover** —
> an 8-term value function whose terms derive from registry graph structure (Composability =
> counterfactual dependency fan-in; `c6x`'s leverage captured *before* the fact, validated
> retrospectively), a decomposition optimizer with the oracle as a hard reward (reward-hacking
> structurally blocked; 6/6 cheaper-decomposition groups found), a goal-selection guard, and an
> auto-derived primitive-proposal package (`c7x`, `cr8_dag_gate`). **(S3) Adoption** — OpenQASM3
> export/ingest with round-trip unitary identity (57/57 re-derived by the numpy oracle; closed loop 8/8),
> a `qf` CLI (wrapping existing scripts, zero new verification logic), and a citable `CITATION.cff`
> binding the root hash. **(S4) Consensus close** — a convention-independence audit (unitary
> *construction* = independent → risk(d) closed; endian/phase/atol/hash = **shared assumption**, gap
> named) and ρ-discount validation against *constructed* co-errors (lineage-merge + ρ collapse a poisoned
> consensus to <2 independent; mechanism **live**, natural co-error deferred to EXT). **(S5) Hardening** —
> determinism env-pin (byte-identity robust to FP/BLAS noise; `requirements.lock`), an oracle-revocation
> protocol (fingerprint **145/145 intact**, `docs/EMERGENCY-RESEAL.md`), and ed25519 Sybil defense
> (pubkey-strengthened independence units). **(W2.4 EXT relay, round 1)** a 6-runtime panel converged
> on `c7x` (golden `cnx_perm(7)`) and `cr8_dag_gate` (golden `diag(1,1,1,e^{-2πi/2⁸})`), both sealed
> key-free — growing the registry to **50 modules / root `437efbc3…`** (pure non-destructive growth:
> prior seals, the 23 frozen consensus keys, and the fingerprint files reproduce byte-identical;
> `second_oracle` 50/50). **(W6.1 c7x payoff)** the evolved arithmetic engine (`genskills`
> `_MCT_MODULE[7]=c7x` upstream + self-seal re-stamp INTACT) then spent that `c7x` on three N>64
> distinct-prime modular multipliers — `cmul2_mod91` (7×13), `cmul2_mod77` (7×11), `cmul2_mod85`
> (5×17), all three genuinely using the 7-control gate (independent arithmetic-permutation match 3/3,
> ×2-orbit period = ord_N(2) 3/3) — growing apps **59→62, root `437efbc3…→e64f4970…`** (modules
> still 50; prior seals/keys/fingerprint byte-identical). The discover frontier now auto-advances past
> sealed gates (`c7x→c8x`, round-2 package) and the W2.4 "c7x→mod 39/51" claim was empirically
> corrected (N<64 needs only `c6x`; `c7x` required iff N>64). **(W6.3 cr8 payoff)** the symmetric twin
> spent `cr8_dag_gate` on an 8-qubit inverse-QFT `iqft8` (parametric `gen_iqft_pipeline`; a regression
> gate proves the pattern by regenerating the sealed `iqft7` byte-identically; QFT8† independent match),
> growing apps **62→63, root `e64f4970…→43580b93…`** (modules still 50). **(W6.4 forward-QFT completion)**
> closing the `iqft8` asymmetry, three analytic `cr6/7/8_gate` (non-dag) were sealed, unlocking
> `qft5…8_pipeline` (a regression gate reproduces the sealed `qft4_pipeline` byte-identically) — growing
> **modules 50→53, apps 63→67, root `43580b93…→ea97a877…`** (`second_oracle` extended to 53/53).
> **(W6.5 capstone)** composing those parts — `cmul2_mod91` (W6.1) + `iqft8` (W6.3) — into a genuine
> distinct-prime Shor circuit `shor91` (factors 91=7×13; forge `cmul4/16/74_mod91` first). At 15 qubits
> it exceeds the dense ceiling → **Tier-1 STRUCTURAL** (Merkle of sealed parts, `tier="structural"`):
> the *first algorithm-scale structural-only seal*, honestly weaker than dense `unitary_equiv` — growing
> **apps 67→71, root `ea97a877…→93183bcd…`** (modules still 53).
> **(W7.1 QEC family)** opens the first *horizontal* algorithm class — quantum error-correction stabilizer
> encoders, all Clifford **Tier-0 EXACT**, assembled only from sealed `h_gate`/`cnot`: `repcode3_bitflip`
> and `repcode3_phaseflip` (`[[3,1]]` repetition encoders), `syndrome3_bitflip` (a pre-measurement
> parity-copy syndrome unitary), and the **`shor9_encoder`** (`[[9,1,3]]` Shor code, 1995 — a 9-qubit
> 512×512 encoder, the QEC capstone). Each golden is built from **closed-form parity-permutation /
> Sylvester-Hadamard maps** (a Qualtran-independent code path, matching the qft `golden`=DFT precedent;
> the stronger stabilizer-tableau Tier-2 check is noted as future work). Independent golden==sealed 4/4;
> Shor-9 `|0_L⟩` codeword behaviour verified. Growing **apps 71→75, root `93183bcd…→06ca92d7…`** (modules
> still 53).
> **(W7.2 Clifford-Tier-2 QEC)** closes exactly that future-work gap: a general stabilizer code's encoder
> has a *circuit-specific* full-unitary golden (only two columns are pinned by the code), so the honest
> independent oracle is the **canonical stabilizer tableau** (Tier-2 — dense-free, exact up to global phase).
> Via `verify_seal`'s module-level `tier="clifford"` path it seals the genuinely code-defined Steane
> `[[7,1,3]]` logical-`|0_L⟩`/`|1_L⟩` states (CSS, from the Hamming parity matrix) and a **Tier-2 re-seal of
> the Shor-9 encoder** (cross-validating W7.1: its cirq dense unitary equals the W7.1 closed-form golden —
> the same operator now under the stronger oracle). Code-correctness is an *independent driver witness*:
> the prepared logical states are `+1` eigenstates of all six Steane stabilizers, with logical `Z̄`
> eigenvalue `+1`/`−1`. `second_oracle` (dense reconstruction) covers the 53 Tier-0 modules; these 3
> Tier-2 modules are tableau-sealed (outside dense scope), honestly tracked separately. Growing **modules
> 53→56 (3 Tier-2 Clifford), apps still 75, root `06ca92d7…→36e7014c…`**. Future work: the full
> logical-input Steane encoder and the non-CSS `[[5,1,3]]` code (general stabilizer encoder synthesis).
> **(W7.3 fault-tolerant logical gates)** completes the QEC arc with the actual *point* of error
> correction: **transversal logical Clifford gates** on Steane — logical `H` (`H^⊗7`), `S` (`S†^⊗7`,
> verified to apply the `+i` logical phase), and `CNOT` (`CNOT^⊗7` between two code blocks). Steane is a
> doubly-even self-dual CSS code, so each transversal gate preserves the code space and acts as the named
> logical operation (driver witness: logical action on the code basis states — `H̄` sends `|0_L⟩→|+_L⟩`,
> `CNOT̄` sends `|ab_L⟩→|a,a⊕b_L⟩`). The **14-qubit logical CNOT cannot be a Tier-0 dense seal** (2¹⁴) —
> it is the first artifact to exercise Tier-2's dense-free advantage *at scale* (sealed by canonical
> tableau, witnessed on the four logical basis vectors without materializing the full unitary). Growing
> **modules 56→59 (3 more Tier-2 Clifford), apps still 75, root `36e7014c…→3a85407d…`**.
> **(W8.1 Hamiltonian simulation)** opens a *second* new horizontal class — Trotterized time evolution,
> introducing a new primitive type: **Pauli-exponential rotations** (`Rz`/`Rx`, non-Clifford analytic).
> Sealed: `rz_negpi4`/`rx_negpi4` (single-qubit rotations, analytic golden), `rzz_pi8` (`e^{iθZ⊗Z}` =
> `CNOT·Rz·CNOT`, honest two-qubit decomposition), and `tfim3_trotter_step` (a first-order Trotter step
> of the 3-qubit transverse-field Ising model). The Trotter **step** is sealed *exactly* (composite ==
> closed-form Pauli-exponential golden); its **Trotter error** against the true `e^{-iH dt}` is an
> explicit **observation, not a seal** — the `approximation ≠ exact` boundary (the sister of `execution ≠
> verification`), with the expected O(dt²) first-order scaling confirmed. Growing **modules 59→61 (2 Tier-0
> rotations; `second_oracle` extended to 55/55), apps 75→77, root `3a85407d…→d231fbf4…`**.
> **(W8.2 Trotter deepening)** grows that class from instance to family — completing the Pauli-interaction
> rotation set `{rxx, ryy, rzz}` (via `H`/`S†` basis changes; new `sdg_gate` module), sealing two
> Heisenberg instances (single-bond + 3-qubit chain) and a multi-step compound, all Tier-0 exact. The
> honest boundary deepens into a **convergence observation** (still not a seal): at fixed `T`, the
> first-order global Trotter error scales `O(1/k)` (ratio ≈ 2 per `k`-doubling) for both TFIM and the
> Heisenberg chain, while the **single-bond** Heisenberg step is *exact* (XX, YY, ZZ commute on one bond).
> Growing **modules 61→62 (1 Tier-0 `sdg_gate`; `second_oracle` extended to 56/56), apps 77→82, root
> `d231fbf4…→59b88d50…`**.
> **(W8.3 Suzuki Trotter)** adds **2nd-order (symmetric Suzuki) Trotter steps** (`ΠZZ(dt/2)·ΠX(dt)·ΠZZ(dt/2)`,
> via a new half-angle `rz_negpi8`/`rzz_pi16`) and extends the lattice to **4 qubits** (TFIM4, 1st- and
> 2nd-order). The honest boundary gains *order resolution*: at fixed `T`, the 1st-order error scales
> `O(1/k)` (ratio ≈ 2 per `k`-doubling) while the 2nd-order Suzuki step scales `O(1/k²)` (ratio ≈ 4) —
> where W8.2 showed *approximation converges*, W8.3 shows *approximation quality (order) is quantifiable*
> (still an observation, not a seal; the steps are sealed exactly). Growing **modules 62→63 (1 Tier-0
> `rz_negpi8`; `second_oracle` extended to 57/57), apps 82→86, root `59b88d50…→566b0368…`**.
> **(W8.4 Trotter dynamics)** *executes* those sealed steps (simulator backend, `u_hash`-gated) as `U^k`
> to observe the **time-dynamics** of physical observables against exact diagonalization — an
> observation-only layer that **seals nothing** (registry/oracle/frozen/root unchanged at `566b0368…`),
> closing all three honest boundaries (sealing ≠ execution ≠ verification; approximation ≠ exact) on one
> family. Honest subtlety: 1st/2nd-order Trotter are Z-diagonal conjugate (`s1 = A^{½}·s2·A^{-½}`), so a
> Z-basis measurement is order-blind (identical `⟨Z⟩`/`⟨ZZ⟩`); only transverse `⟨X⟩` shows 2nd-order
> tracking exact ~3× closer.
> **(W9.1 amplitude amplification)** opens another horizontal class generalizing Grover: 3-qubit
> reflection/diffusion/Grover operators + iteration-count apps (`reflect000`, `diffusion3`, `grover3`,
> `grover3_2iter`, `grover2_2iter`), all Tier-0 and built by reusing sealed parts with **zero new
> modules**. The amplitude-amplification profile `P_target(k)` is an observation (not a seal) matching
> `sin²((2k+1)θ)` exactly — optimal-k (N=8 → k=2, P≈0.945) and over-rotation (N=4 → k=2, P=0.25).
> Growing **apps 86→91 (modules unchanged at 63; `second_oracle` stays 57/57), root `566b0368…→3e3d6fe7…`**.
> **(W9.2 amplitude estimation / QAE)** raises amplification to *estimation*: QPE on the Grover operator
> `Q = Ry(π/2)` (4 analytic `Ry` modules — `ry_pi4/negpi4/pi2/negpi2`, `YPowGate(α/π)` up-to-phase — plus
> honest controlled-`Ry` ladders `cry_pi2`/`cry_pi`, and the 4-qubit `qae3_pi8` reusing the sealed
> `iqft3`/`cnot`/`h_gate`/`z_gate`), all Tier-0. The amplitude-estimation readout (`a_est = sin²(πy/2^t)`)
> is an observation, not a seal: for the exact instance `a = sin²(π/8)`, both peaks `y ∈ {1,7}` recover
> the true `a` exactly. Growing **modules 63→67 (4 Tier-0 `Ry`; `second_oracle` to 61/61), apps 91→94,
> root `3e3d6fe7…→a916c8da…`**.
> **(W9.3 QAE deepening)** grows QAE to a family with **zero new modules** and contrasts the two
> estimation paradigms: a second exact QPE-QAE instance `qae3_pi2` (`a = 1/2`), and **iterative/power QAE**
> (QPE-free) — sealed Grover powers (`grover2/3`, `grover2/3_2iter`, new `grover2/3_3iter`) are *executed*
> via `backend_adapter` and `P_good(m) = sin²((2m+1)θ)` is fit classically to estimate **general**
> amplitudes (`a = 1/4`, `1/8`) that small-`t` QPE cannot read, at the cost of precision-vs-measurements.
> Both readouts are observations, not seals. Growing **apps 94→97 (modules unchanged at 67;
> `second_oracle` stays 61/61), root `a916c8da…→2cfe8dc3…`**.
> **(W10.1 VQE ansatz)** opens a new horizontal class — the **variational quantum eigensolver**. A hardware-efficient ansatz (`Ry(θ)^⊗n · CNOT` ladder) is sealed *structurally* at fixed-θ instances (new module `ry_3pi4`=`Ry(3π/4)`; apps `vqe_he2_pi4/pi2/3pi4` (2q) and `vqe_he3_pi4` (3q), all **Tier-0 EXACT**, `composite==golden` up-to-phase, no `MatrixGate`, reusing `ry_pi4/pi2/3pi4`·`cnot`). The honest boundary gains a **variational** sibling of *approximation != exact*: the variational energy `<H_TFIM(θ)>` (computed via `backend_adapter`, an observation — not a seal) obeys the variational principle `<H> >= E_ground`, and a continuous θ-sweep approaches but never reaches the exact ground energy — an **ansatz-limited gap > 0** persists (TFIM2 gap≈0.071, TFIM3 gap≈0.097). VQE is a bound/approximation, not the exact ground. Growing **modules 67→68 (1 Tier-0 `ry_3pi4`; `second_oracle` to 62/62), apps 97→101, root `2cfe8dc3…→1a2a874d…`**.
> **(W10.2 VQE deepening)** seals a **2-layer per-qubit** hardware-efficient ansatz (`vqe_he2_L2_*`, zero new modules); the variational gap shrinks with expressibility (0.071→~0.006) but stays >0 — depth *deepens* `variational != exact`, it does not remove it. **(W11.1 QAOA)** opens the combinatorial-optimization sibling: MaxCut QAOA p=1 sealed Tier-0 at fixed angles (`qaoa_p3`, `qaoa_c4`, **zero new modules** — reuses `cnot`/`rz_negpi4`/`rx_negpi4`/`h_gate`), the approximation ratio an observation that stays <1 even at optimal angles (P3 0.825, C4 0.75). **(W10.3 parameter-shift)** executes sealed `Ry` modules to show the parameter-shift rule yields the *exact* analytic gradient, contrasted with finite-difference (O(h²) approximation) — no new seals. Growing **apps 101→105 (modules unchanged at 68; `second_oracle` stays 62/62), root `1a2a874d…→fa06bd80…`**.
> **(W12 — new horizontal classes + Shor arithmetic frontier; cross-runtime)** the **codex** runtime drove W12.1–W12.18, W12.20, and W12.21, while the **Claude Opus** runtime drove W12.19 + determinism verification — the first byte-identical cross-runtime seals (one runtime's seals re-verified deterministically by the other). **(W12.1 query/oracle)** Deutsch-Jozsa, Bernstein-Vazirani, Simon sealed (`dj2_const1`, `dj2_balanced_xor`, `bv3_s101`, `simon2_s11`, **zero new modules**) — here the quantum advantage itself is *exact* (BV recovers the secret in one query; Simon's measured support is orthogonal to the period), a new honesty type beside approximation/variational. **(W12.2 quantum walk)** coined C4/C8 cycle walks (zero new modules; walk dynamics an observation — C8 3-step TV distance 0.25 vs classical). **(W12.3 Suzuki-4)** 4th-order Yoshida-Suzuki Trotter steps (4 new analytic-coefficient modules `rz_y4_p/rx_y4_p/rz_y4_q/rx_y4_q`; late k-doubling ratio ≈16 vs 1st-order ≈2, 2nd ≈4 — convergence-order observation, not a seal). **(W12.4 ZNE)** a deterministic zero-noise-extrapolation observation layer that **seals nothing** (root unchanged; mitigation ≠ exact recovery, residual bias remains). **(W12.5–W12.19 Shor frontier)** a `c8x→c9x→c10x→c11x` multi-control primitive ladder (4 new Tier-0 MCT modules, `gen_modmul` cap evolved each step) unlocks distinct-prime **Shor structural apps** `shor119`/`shor221`/`shor381`/`shor635`/`shor1285` (N = 7×17, 13×17, 3×127, 5×127, 5×257), each a **Tier-1 STRUCTURAL** Merkle over exact Tier-0 `cmul*` modular-multiplier families (max control 7→11; independent arithmetic `u_hash` matched per multiplier). **(W12.20–W12.23 C12x frontier → payoff → shor3683)** reviewed the memory boundary, sealed `c12x` and the exact payoff app `cmul2_mod3683` (`N=3683=29×127`, 13 qubits, 1848 gates, max-control 12, independent arithmetic `u_hash` matched), then completed the `mod3683` payoff family (`cmul{4,16,256,2925}_mod3683`, Tier-0 exact, independent arithmetic 4/4) and lifted it to the structural Shor app `shor3683` (Tier-1 STRUCTURAL, 20 qubits, deterministic reassembly; readout illustrative ord_3683(2)=28→[29,127]). The W12.22/23 rounds were driven autonomously by the AutonomyLoop runner (real determinism gates, fingerprint+frozen byte-identical, verified-only commit). **(W12.24 FrontierFactory)** packaged that runner as the `qfa-loop` skill and added a **parametric frontier factory** (`qf_witness/frontier/frontier_factory.py`): the verified payoff/structural templates become N-parameter sealing functions, regression-gated to reproduce every prior sealed N byte-identically (INV-F1) before sealing any new N. The loop then auto-discovers the smallest unsealed distinct-semiprime and seals it — `shor69` (3×23) and `shor77` (7×11), both 15q structural with their cmul payoff families, **zero new modules**. Growing **modules 68→77 (4 Suzuki-4 + c8x/c9x/c10x/c11x/c12x; `second_oracle` 62→71), apps 105→166, root `fa06bd80…→a0b4f678…`**.
> The post-W12 bridge maps five external relay items (CI pilot,
> weak-model poison panel, runtime keys, backend evidence, ServerLink scope) but does not execute external work. Companion docs:
> `docs/CONVENTION-AUDIT.md`, `docs/TRUST-MODEL-VALIDATION-REPORT.md`, `docs/EMERGENCY-RESEAL.md`,
> `_workspace/crossmodel/discover_round1/SEAL-RESULT.json`.

> **★ Milestone — Shor frontier complete through N ≤ 1023 (2026-07-23).** The `qfa-loop` frontier
> factory ran to **frontier-exhaustion** over the full 10-bit range: every readout-valid distinct-semiprime
> `N ≤ 1023` now has a sealed Tier-1 STRUCTURAL `shor{N}` app (final `shor1011`) with its exact `cmul*`
> payoff family and auto-redeemed subspace-permutation witnesses — **zero new modules** across the entire
> ladder (the parametric factory reuses the verified templates, INV-F1 regression-gated byte-identical).
> `next_unsealed_target()` returns `None`; re-expansion is a deliberate `hi`-raise only. Registry at closure:
> **95 modules · 1431 unique apps · tier1 142 · root `556d5e97322affa0…`**. Operationally, the nightly
> sealing cron is proposed to transition to a **weekly determinism health-check** (full reproduce) — the
> factory's sealing *capability* is preserved as deterministic code, not a running process.

> **Horizontal-expansion tracks (TrackHE, report-driven).** In parallel, external multi-runtime proposal
> rounds (`report13…17`) were consumed as **observation/certificate** tracks (seal root unchanged): twisted
> Drinfeld doubles `D^ω(D₄)/D^ω(Q₈)/D^ω(S₃)`, closed-negative refutations of over-reaching proposals
> (`D^ω(ℤ₂⁴)` full non-abelianization, `Q₃₂` Sylow tower), the figure-8 knot as the first non-torus
> amphichiral 3-braid (BMW₃ dim-15 context), the Altland-Zirnbauer 3D column completed (class DIII ℤ / AII
> ℤ₂ strong TI / AIII ℤ), and the **ε-certification contract** deepened from upper bounds to **rigorous
> lower bounds** — E5 operator-norm (`ε_lo > 0` ⟹ "this Trotter step is not exact") and E6 diamond-norm
> (channel-level). Independent verification paths held at **10** (an 11th remains an open problem).

> **★ TrackHE17 (report17, 5 of 6 axes, 2026-07-23).** The v18 request round consumed 8-runtime proposals
> into a symmetric deepening of each TrackHE16 axis (observation/certificate tracks, seal root unchanged):
> **AZ 2D class AII (QSH ℤ₂) + CII 3D (2ℤ even winding) + full weak indices + a coarsening graph**
> (DIII ℤ → AII ℤ₂ = winding mod 2; AIII ℤ ⊃ CII 2ℤ); the **ε-certification ladder completed to E7 —
> exact Watrous diamond norm** `2√(1−ν²)` (E6 lower bound promoted to the exact channel value, 3-rung
> bracket `[D_lo, D_exact, 2ε]`, 19 apps); **D^ω(D₄) twisted anyon count is ω-varying (22/19/16)** — the
> "fixed 22" fallacy refuted via centralizer Schur multipliers, with the `H³(D₄,μ₂)` (dim 4) vs
> `H³(Q₈,μ₂)` (dim 1) asymmetry as the twist resource; **D^ω(ℤ₂⁴) radical fully stratified** to `{2,4}`
> — **radical = 1 is impossible by a parity theorem** (the commutator form is GF(2)-alternating so its rank
> is even), refuting the proposed "radical-1 subclass", with the 15 type-III cocycles forming a single
> `GL(4,2)` orbit (`Λ³V* ≅ V`); **A₇ modular (Brauer) structure** self-derived (9 classes, Brauer-irrep
> counts = p-regular classes 6/6/8/7, cyclic-defect at p=5,7, defect-0 blocks). Plus the **rotated d=3
> surface code `[[9,1,3]]`** physical layer (distance 3 exhaustive, CSS, merge = physical logical
> measurement) complementing the earlier logical lattice-surgery CNOT. Registry unchanged at
> **95 modules / 1431 unique apps · root `556d5e97…`** (all observations/certificates, zero new modules).
> The 6th axis — the **2-variable Kauffman polynomial via a BMW₃ Ocneanu Markov trace** — is diagnosed but
> unresolved (the dim-15 multiplication core verifies, but a σ₂-interaction convention error blocks a
> consistent Markov trace) and deferred; it is the headline ask of request v18.

