# DESIGN — FrontierOps

> W12.11-W12.13 combined PGF full-cycle. Convert frontier selection from manual
> judgment into deterministic reports, generalize Shor structural assembly, and
> review the next `c10x` primitive without sealing it.

## Gantree

```text
FrontierOps // selector + structural generalizer + c10x review (done) @v:1.0
    FrontierSelector // rank semiprime frontier candidates deterministically (done)
        # input: gen_modmul MMD synthesis, semiprime N ranges
        # process: scan by work bits, unique powers, MMD gate count, max control, readout usefulness
        # output: .pgf/arith/FRONTIER-SELECTOR-REPORT.json
        # criteria: deterministic report, no registry writes, identifies N=635 as next c10x-class candidate
    ShorStructuralGeneralizer // reusable structural Shor builder and verifier (done) @dep:FrontierSelector
        # input: existing shor119/shor221/shor381 specs and sealed children
        # process: build_shor_spec(app_id,N,a,t) + structural hash/resource reassembly
        # output: .pgf/arith/SHOR-STRUCTURAL-GENERALIZER-REPORT.json
        # criteria: shor119/shor221/shor381 hash+resource reproduce exactly
    C10xPrimitiveReview // feasibility review for 10-control frontier (done) @dep:ShorStructuralGeneralizer
        # input: W12.11 selector signal and 11q dense cost estimate
        # process: scan N in [512,767], review c10x module/app cost and guardrails
        # output: .pgf/arith/C10X-PRIMITIVE-REVIEW.json
        # criteria: no seals, no root change, clear go/no-go and successor task
    BacklogUpdate // mark W12.11-W12.13 done and add W12.14 candidate (done) @dep:C10xPrimitiveReview
        # output: HANDOFF/remain/task_record/master updated
        # criteria: root unchanged, reproduce_all remains REPRODUCED
```

## PPR

```python
def execute_frontier_ops() -> FrontierOpsReport:
    """Run W12.11-W12.13 without registry growth."""
    selector = run("python scripts/frontier_selector.py")
    assert selector.report.best_512_767.N == 635
    assert selector.report.honesty == "report-only"

    generalizer = run("python scripts/shor_structural_generalizer.py")
    assert generalizer.all_ok
    assert all(row.hash_matches and row.resource_matches for row in generalizer.results)

    c10x = run("python scripts/c10x_review.py")
    assert c10x.decision.recommended_next == "W12.14 C10xPrimitiveFrontier"
    assert c10x.decision.recommended_target.N == 635

    # acceptance_criteria:
    #   - FrontierSelector ranks candidates deterministically and writes a JSON report.
    #   - ShorStructuralGeneralizer reproduces shor119/shor221/shor381 structural hashes byte-identically.
    #   - C10xPrimitiveReview does not seal c10x and emits go/no-go guardrails.
    #   - registry_root_hash remains unchanged.
    #   - reproduce_all remains REPRODUCED.
    return FrontierOpsReport(status="done", root_changed=False)
```
