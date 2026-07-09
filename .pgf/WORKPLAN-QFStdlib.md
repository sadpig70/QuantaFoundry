# QFStdlib Work Plan

## POLICY

```python
POLICY = {
    "max_retry": 3,
    "on_blocked": "report_with_failed_gate",
    "design_modify_scope": ["sidecar", "package", "docs", "tests"],
    "completion": "all_done_or_blocked",
    "forbidden": ["modify_oracle", "rewrite_sealed_json", "create_new_quantum_seal"],
}
```

## Execution Tree

```text
QFStdlibImplementation // implement user-facing stdlib sidecar layer (done) @v:0.1
    DesignReview // re-read local canon and confirm sidecar scope (done)
        # output: DESIGN-QFStdlib + detailed design accepted as implementation basis
    CanonMinimal // registry/CANON.json + validator (done) @dep:DesignReview
        # output: qf_stdlib.canon, scripts/qf_stdlib.py build/validate-canon, registry/CANON.json
        # criteria: live manifest root anchored, exact u_hash validation, alias collision fail-closed
    PackageSurface // qf_stdlib lookup/attest package (done) @dep:CanonMinimal
        # output: qf_stdlib registry/canon/attest/errors/adapters modules
        # criteria: lookup-only mode imports without optional circuit frameworks
    TemplateV0 // proof-carrying templates (done) @dep:PackageSurface
        # output: qft_import, qpe_skeleton, trotter_stack templates
        # criteria: template refs resolve through Canon; derived certs are not seals
    TestsDocs // tests and user docs (done) @dep:TemplateV0
        # output: tests/test_qf_stdlib.py, docs/QF-STDLIB.md
        # criteria: positive lookup/attest and negative false-proof tests pass
    VerificationGate // run deterministic gates and update roadmap status (done) @dep:TestsDocs
        # commands: validate-canon, lookup, attest, validate/build-template, unittest, second_oracle, contested_guard, changed-only reproduce
        # criteria: stdlib gates pass; registry/oracle/sealed artifacts are not mutated except CANON sidecar/report. ✅ done
    V01Hardening // root drift guard + expanded Canon palette + docs examples (done) @dep:VerificationGate
        # output: check-root CLI/API, 42-entry Canon, expanded unit tests, concrete docs examples
        # criteria: check-root·validate-canon·lookup·attest·template·unittest·py_compile·changed-only reproduce PASS. ✅ done
    V02CirqAdapter // convention-pinned Cirq circuit hash adapter (done) @dep:V01Hardening
        # output: qf_stdlib.adapters cirq path, adapter-info CLI, docs/tests
        # criteria: explicit qubit_order required; qft/3 Cirq hash matches Canon; endian/global-phase/CLI-fail-closed tests PASS. ✅ done
    V03AttestCircuit // circuit hash → Canon lookup → root-anchored attestation (done) @dep:V02CirqAdapter
        # output: qf_stdlib.attest_circuit API, docs/tests
        # criteria: Cirq qft/3 returns attestation; unknown circuit hash returns None; adapter convention errors propagate. ✅ done
```
