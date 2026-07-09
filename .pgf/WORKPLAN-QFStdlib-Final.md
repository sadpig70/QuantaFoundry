# WORKPLAN-QFStdlib-Final

## POLICY

```python
POLICY = {
    "scope": "QF-STDLIB v1.0 convergence",
    "max_retry_per_node": 3,
    "execution_order": "topological",
    "commit_rule": "commit only after node gates pass",
    "root_policy": "registry root must remain stable; Canon/report sidecars may regenerate",
    "forbidden": [
        "modify_oracle",
        "rewrite_sealed_json",
        "create_new_quantum_seal",
        "approximate_circuit_matching",
        "silent_adapter_normalization",
    ],
}
```

## Execution Tree

```text
QFStdlibFinalWorkplan // finite path from v0.3 to v1.0 (in-progress) @v:1.0
    FinalDesignPlan // freeze v1.0 goal, node order, and gates (done)
        # output: DESIGN-QFStdlib-Final, WORKPLAN-QFStdlib-Final, status-QFStdlib-Final, MasterRoadmap node
        # criteria: JSON status valid; workplan has finite v0.4-v1.0 sequence; no code behavior change required. ✅ done
    V04BaseGateCanon // expand Canon with sealed base gate modules (done) @dep:FinalDesignPlan
        # output: gate/x, gate/z, gate/h, gate/s, gate/t, gate/cnot, gate/swap, gate/cz, gate/toffoli, gate/fredkin, gate/cs, gate/ct, gate/ccz
        # tests: validate-canon, lookup by key/alias/id/hash, no cached app-side exposure
        # gate: unittest + py_compile + changed-only reproduce. ✅ done
    V05CirqBaseCoverage // attest_circuit positive/negative coverage for base gates (done) @dep:V04BaseGateCanon
        # output: Cirq X/H/CNOT/CZ/SWAP/Toffoli/Fredkin tests where conventions match Canon
        # tests: positive hash match, qubit_order mistakes, measurement rejection, unsupported adapter
        # gate: unittest + adapter-info + py_compile. ✅ done
    V06CanonUX // category and summary query surface (done) @dep:V04BaseGateCanon
        # output: Canon category metadata, CLI categories/list --category/summary, API helpers
        # tests: deterministic category ordering, unknown category fail-closed, docs examples
        # gate: validate-canon + unittest. ✅ done
    V07TemplateLibrary // expand proof-carrying recipe catalog (done) @dep:V06CanonUX
        # output: qsvt_consumer, shor_modexp_attest, base_gate_bundle, qpe_minimal templates
        # tests: validate-template/build-template for every template; structural limits preserved
        # gate: unittest + docs examples. ✅ done
    V08AdapterDecisionGate // decide optional non-Cirq adapters (done) @dep:V05CirqBaseCoverage
        # output: implementation for a convention-proven adapter OR explicit deferred decision record
        # tests: if implemented, positive/negative convention tests equivalent to Cirq; if deferred, docs/status record why
        # gate: unittest + py_compile. ✅ done
    V09PackagingPolish // public user surface cleanup (done) @dep:V07TemplateLibrary,V08AdapterDecisionGate
        # output: docs/API/CLI help aligned, README link/status updated if needed, optional dependency note
        # tests: import qf_stdlib without Cirq heavy path; CLI help exits 0; examples smoke test
        # gate: docs/code smoke + unittest. ✅ done
    V10FinalReleaseGate // final deterministic v1.0 verification (pending) @dep:V09PackagingPolish
        # commands: check-root, validate-canon --write-report, unittest, py_compile, second_oracle, contested_guard, reproduce_all --changed-only
        # output: final status done, roadmap done, release report in final answer
        # criteria: all gates PASS; root unchanged; deferred scope explicit
```

## Standard Gates

Run after each implementation node unless a node says otherwise:

```bash
python scripts/qf_stdlib.py check-root
python scripts/qf_stdlib.py validate-canon --write-report
python -m unittest tests.test_qf_stdlib -v
python -m py_compile qf_stdlib/*.py scripts/qf_stdlib.py tests/test_qf_stdlib.py
```

Run before each commit that changes behavior or Canon:

```bash
python scripts/second_oracle.py
python scripts/verify_contested_guard.py
python scripts/reproduce_all.py --changed-only
```

## Next Node Contract

The next executable node is `V10FinalReleaseGate`.

```python
def execute_v10_final_release_gate() -> None:
    """Run the final deterministic QF-STDLIB v1.0 release gate."""
    assert qfstdlib_nodes_done(["FinalDesignPlan", "V04", "V05", "V06", "V07", "V08", "V09"])
    run_release_commands()
    update_final_status_and_roadmap()
    run_standard_gates()
    # acceptance_criteria:
    #   - all stdlib and project gates pass
    #   - root remains unchanged
    #   - final report names deferred adapters honestly
    #   - QF-STDLIB v1.0 status is terminal done
```

## Status Update Rule

After each node:

1. Update `.pgf/status-QFStdlib-Final.json`.
2. Update `.pgf/WORKPLAN-QFStdlib-Final.md` node status.
3. Update `.pgf/DESIGN-MasterRoadmap.md` TrackQFStdlib node if the milestone is externally visible.
4. Run the node gate.
5. Commit and push only when gates pass.
