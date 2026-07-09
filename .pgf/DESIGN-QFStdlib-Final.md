# DESIGN-QFStdlib-Final

> Scope: QF-STDLIB를 QuantaFoundry sealed registry의 안전한 사용자 진입 계층으로 v1.0까지 완성한다.
> 이 트랙은 신규 quantum seal을 만들지 않는다. Oracle, sealed JSON, registry root는 소비만 한다.

## Current Anchor

- Current completed stdlib state: v0.6
- Registry root: `d177ce9a438a1b2f6a9f9f042e69f5263267148fb3f90930fe611e8ec0a48af7`
- Registry counts: 95 modules / 475 unique apps / 550 app files / 75 cached app-side module files
- Canon state: 55 entries
- Implemented surface:
  - `qf_stdlib.lookup`
  - `qf_stdlib.attest`
  - `qf_stdlib.attest_circuit`
  - `qf_stdlib.check_root`
  - `qf_stdlib.canonical_hash_with_adapter`
  - `qf_stdlib.list_categories`
  - `qf_stdlib.filter_canon_entries`
  - `qf_stdlib.summarize_canon`
  - proof-carrying templates: `qft_import`, `qpe_skeleton`, `trotter_stack`
- Implemented adapter: Cirq, explicit `qubit_order`, QPGF `hash_unitary`, fail-closed convention errors.

## Final Goal

```text
QFStdlibV1 // sealed registry consumer stdlib for exact lookup, circuit attestation, and proof-carrying recipes (designing) @v:1.0
    CanonComplete // curated Canon for base gates, algorithms, arithmetic, templates, and structural frontiers (designing)
    AdapterComplete // convention-pinned external circuit hash adapters with fail-closed semantics (designing)
    AttestationComplete // user circuit -> Canon proof flow with no false promotion (designing)
    TemplateComplete // useful proof-carrying recipes over Canon entries, not new seals (designing)
    UserSurfaceComplete // CLI/API/docs/examples stable enough for public consumption (designing)
    VerificationComplete // deterministic v1.0 gate suite and release checklist (designing)
```

QF-STDLIB v1.0 is complete when a downstream user can:

1. Discover canonical primitives by stable names and categories.
2. Lookup any Canon item by key, alias, id, or exact `u_hash`.
3. Attest an external Cirq circuit only when its convention-pinned hash exactly matches Canon.
4. Build proof-carrying templates whose certificates aggregate existing attestations.
5. Run deterministic validation commands that fail on stale root, alias collision, unsupported adapter, unknown circuit hash, or structural overclaim.

## Non-Goals

- No new quantum seal.
- No oracle modification.
- No `registry/modules/*.sealed.json` or `registry/apps/*.sealed.json` rewrite.
- No approximate circuit matching.
- No dense upgrade for structural frontiers.
- No hardware execution claim.
- No Qiskit/PennyLane adapter unless convention pinning is proven with tests.

## Invariants

```python
INVARIANTS = {
    "INV_STDLIB_ROOT": "Canon-generated root must equal REGISTRY-MANIFEST root.",
    "INV_EXACT_ONLY": "Lookup and circuit attestation are exact equality over Canon keys/ids/hashes.",
    "INV_NO_SEAL": "QF-STDLIB emits attestations and certificates only; it never seals.",
    "INV_FAIL_CLOSED": "Unknown, ambiguous, stale, unsupported, or non-unitary inputs fail closed.",
    "INV_STRUCTURAL_HONESTY": "Structural/subspace entries keep their original semantic scope.",
    "INV_OPTIONAL_IMPORTS": "Lookup-only imports do not require heavy quantum frameworks.",
    "INV_REPRODUCIBLE": "Generated Canon/report outputs are deterministic from live registry state.",
}
```

## Gantree

```text
QFStdlibFinal // v1.0 convergence plan for user-facing stdlib (in-progress) @v:1.0
    V04BaseGateCanon // add sealed base modules to Canon (done)
        # input: registry/modules/{x,z,h,s,t,cnot,swap2,cz,toffoli,fredkin,cs,ct,ccz}.sealed.json
        # process: add canonical module keys such as gate/x, gate/h, gate/cnot
        # output: expanded registry/CANON.json and tests
        # criteria: validate-canon PASS; no cached app-side module exposure; base gate lookup/attest tests PASS. ✅ done
    V05CirqBaseCoverage // extend attest_circuit positive tests beyond QFT (done) @dep:V04BaseGateCanon
        # input: base gate Canon entries and Cirq unitary circuits
        # process: test X/H/CNOT/CZ/SWAP/Toffoli/Fredkin where Cirq conventions are exact
        # output: adapter regression suite for base gates
        # criteria: base Cirq hashes match Canon; qubit-order mistake is caught; unsupported or measured circuits fail closed. ✅ done
    V06CanonUX // category/index/query UX (done) @dep:V04BaseGateCanon
        # input: Canon entries with stable categories
        # process: expose list --category, categories, and machine-readable summary
        # output: CLI/API category index
        # criteria: category output is deterministic and validated against Canon. ✅ done
    V07TemplateLibrary // expand proof-carrying recipes (designing) @dep:V06CanonUX
        # input: current Canon and templates
        # process: add qsvt_consumer, shor_modexp_attest, base_gate_bundle, qpe_minimal
        # output: templates + validation tests + docs examples
        # criteria: all refs resolve through Canon; template certs clearly say not new seals
    V08AdapterDecisionGate // decide Qiskit/PennyLane by convention evidence, not desire (designing) @dep:V05CirqBaseCoverage
        # input: installed deps and convention probes
        # process: implement only if exact unitary ordering/global phase can be pinned with positive/negative tests
        # output: either adapter implementation or explicit deferred record
        # criteria: no silent approximate adapter; lookup-only imports remain light
    V09PackagingPolish // stable public import and packaging polish (designing) @dep:V07TemplateLibrary,V08AdapterDecisionGate
        # input: qf_stdlib package, CLI, docs
        # process: API __all__, help text, README doc links, examples, optional dependency notes
        # output: stable v1.0 user surface
        # criteria: python import is lightweight; CLI help covers every supported command
    V10FinalReleaseGate // v1.0 verification and final report (designing) @dep:V09PackagingPolish
        # input: all previous nodes
        # process: run full stdlib + deterministic project gates, update docs/status/roadmap
        # output: QF-STDLIB v1.0 release report and commit
        # criteria: check-root, validate-canon, unittest, py_compile, second_oracle, contested_guard, reproduce_all --changed-only PASS
```

## PPR

```python
def AI_design_qfstdlib_final(current_state: dict) -> dict:
    """Decompose QF-STDLIB v1.0 into finite, verifiable implementation nodes."""
    assert current_state["version"] == "v0.3"
    assert current_state["root"] == "d177ce9a438a1b2f6a9f9f042e69f5263267148fb3f90930fe611e8ec0a48af7"
    plan = {
        "canon": ["base gates", "categories", "current algorithms", "structural frontiers"],
        "adapters": ["cirq complete", "qiskit/pennylane decision gate"],
        "attestation": ["lookup proof", "circuit proof", "template certificate"],
        "verification": ["fail-closed tests", "project gates", "root drift guard"],
    }
    return plan
    # acceptance_criteria:
    #   - every node has a deterministic gate
    #   - every node preserves no-new-seal invariant
    #   - v1.0 is finite and does not depend on external runtime reports
```

```python
def implement_node(node: QFStdlibNode) -> VerificationReport:
    """Execute one v1.0 convergence node and gate it before continuing."""
    before = read_registry_root()
    apply_scoped_changes(node.allowed_files)
    run_node_tests(node.required_tests)
    after = read_registry_root()
    assert before == after or node.allows_canon_sidecar_only
    return run_standard_gates()
    # acceptance_criteria:
    #   - no node leaves tests red
    #   - no node mutates oracle/sealed artifacts
    #   - failures are reported with exact failing gate and next repair
```

```python
def final_release_gate() -> bool:
    """Validate QF-STDLIB v1.0 against both stdlib and project-level gates."""
    commands = [
        "python scripts/qf_stdlib.py check-root",
        "python scripts/qf_stdlib.py validate-canon --write-report",
        "python -m unittest tests.test_qf_stdlib -v",
        "python -m py_compile qf_stdlib/*.py scripts/qf_stdlib.py tests/test_qf_stdlib.py",
        "python scripts/second_oracle.py",
        "python scripts/verify_contested_guard.py",
        "python scripts/reproduce_all.py --changed-only",
    ]
    return all(run(cmd).ok for cmd in commands)
    # acceptance_criteria:
    #   - root remains d177ce9a... unless an unrelated registry seal track intentionally changes it
    #   - stdlib docs match implemented API
    #   - release report names deferred adapters honestly
```

## File Ownership

Allowed v1.0 files:

- `.pgf/DESIGN-QFStdlib-Final.md`
- `.pgf/WORKPLAN-QFStdlib-Final.md`
- `.pgf/status-QFStdlib-Final.json`
- `.pgf/DESIGN-MasterRoadmap.md`
- `registry/CANON.json`
- `reports/QF-STDLIB-CANON-REPORT.json`
- `qf_stdlib/**`
- `scripts/qf_stdlib.py`
- `tests/test_qf_stdlib.py`
- `docs/QF-STDLIB.md`
- `README.md` only for final public doc link/status polish

Forbidden files:

- `.agents/skills/qpgf-oracle/**`
- `registry/modules/*.sealed.json`
- `registry/apps/*.sealed.json`
- `specs/**` unless a future user explicitly changes scope away from stdlib

## Done Definition

QF-STDLIB v1.0 is done only when:

- All final workplan nodes are terminal.
- `status-QFStdlib-Final.json` agrees with the workplan.
- Canon validates against the live registry root.
- Circuit attestation is exact and fail-closed.
- Templates validate and document their non-seal status.
- Full deterministic gates pass.
- Remaining deferred adapters are explicitly listed with reasons.
