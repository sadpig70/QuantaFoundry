# DESIGN — C10xOps

> W12.14 + M1 + M3 combined PGF full-cycle. Seal `c10x`, prove the first
> c10x-consuming multiplier, make `reproduce_all.py` frontier steps declarative,
> and audit backlog/handoff compaction.

## Gantree

```text
C10xOps // c10x frontier plus reproduction/backlog maintenance (done) @v:1.0
    SealC10x // seal 10-control MultiControlX primitive (done)
        # input: QPGF module oracle, independent cnx_perm(10)
        # process: write specs/modules/c10x.pg and verify_seal
        # output: registry/modules/c10x.sealed.json
        # criteria: Tier-0, n_sys=11, independent u_hash match
    SealCmul635 // seal first c10x-consuming 10-work-bit multiplier (done) @dep:SealC10x
        # input: N=635=5*127, a=2, nq=11
        # process: gen_modmul cap 10 + permutation-space exact C-app check
        # output: cmul2_mod635 Tier-0 app
        # criteria: max_control=10, deps include c10x, independent arithmetic u_hash matches
    ReproduceStepRegistry // make frontier reproduction steps declarative (done) @dep:SealCmul635
        # input: scripts/reproduce_all.py accumulated explicit frontier calls
        # process: introduce FRONTIER_STEPS list and loop over it
        # output: same reproduce_all behavior with c10x_frontier included
        # criteria: reproduce_all remains REPRODUCED
    BacklogCompactionAudit // machine-check handoff/remain/task_record compactness (done) @dep:ReproduceStepRegistry
        # input: HANDOFF.md, remain_task_list.md, task_record.md, registry manifest
        # process: line budgets, current root markers, stale pattern search
        # output: .pgf/maintenance/BACKLOG-COMPACTION-AUDIT.json
        # criteria: all_ok=True after docs update
    RegistryAndDocs // regenerate registry layers and update backlog state (done) @dep:BacklogCompactionAudit
        # process: registry_tools, semantic_guarantee, citation_gen, seal_gate_ci, docs
        # output: root 216169028a05a840..., W12.15 next candidate
        # criteria: CI gates pass, fingerprints unchanged
```

## PPR

```python
def execute_c10x_ops() -> C10xOpsReport:
    """Seal c10x, clean reproduce_all frontier steps, and audit backlog docs."""
    c10x = run_qpgf_oracle("specs/modules/c10x.pg", out="registry/modules")
    assert c10x.tier == 0 and c10x.n_sys == 11
    assert independent_hash(cnx_perm(10)) == c10x.u_hash

    update_genskills_mct_map(max_control=10, new_module="c10x")
    cmul = seal_cmul(N=635, a=2, nq=11)
    assert cmul.max_control == 10 and "c10x" in cmul.deps
    assert independent_arithmetic_match(cmul)

    reproduce_all = refactor_frontier_steps_to_declarative_list()
    assert reproduce_all.bundle == "REPRODUCED"

    audit = run("python scripts/backlog_compaction_audit.py")
    assert audit.all_ok

    # acceptance_criteria:
    #   - c10x Tier-0 exact module seal exists and independent u_hash matches.
    #   - cmul2_mod635 Tier-0 exact app seal consumes c10x and matches independent arithmetic hash.
    #   - reproduce_all frontier steps are declarative and include c10x_frontier.
    #   - backlog compaction audit passes after HANDOFF/remain/task_record updates.
    #   - registry/reproduce/CI/fingerprint/frozen checks pass.
    return C10xOpsReport(status="done")
```
