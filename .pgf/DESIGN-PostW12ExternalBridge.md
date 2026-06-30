# PostW12ExternalBridge Design @v:1.0

## Gantree

```text
PostW12ExternalBridge // M4 design-only bridge from W12.21 evidence to external work (done) @v:1.0
    EvidencePack // freeze W12.21 consumable evidence (done)
    ExtMap // map each blocked EXT item to value/blocker/unblock condition (done) @dep:EvidencePack
    ExecutionOrder // rank external follow-up sequence without starting it (done) @dep:ExtMap
    BoundaryGuard // keep docs sync and external execution behind explicit triggers (done) @dep:ExecutionOrder
    BacklogUpdate // update handoff/remain/task_record with bridge result (done) @dep:BoundaryGuard
```

## PPR

```python
def build_evidence_pack() -> dict:
    """Collect current internal evidence that can be consumed externally."""
    # input:
    #   registry root 1134ea04099ea0c1
    #   c12x Tier-0 module
    #   cmul2_mod3683 Tier-0 app
    #   reproduce_all REPRODUCED, second_oracle 71/71, seal_gate_ci PASS
    # criteria:
    #   - no new seal
    #   - no root mutation
    #   - evidence references are file-backed and reproducible
```

```python
def map_external_queue(evidence: dict) -> list[dict]:
    """Produce a blocker-aware EXT queue map."""
    # process:
    #   EXT_W3_5_CIPilot uses root/seal_gate_ci evidence
    #   EXT_W4_2_PoisonPanel uses consensus/poisoned-lineage validation package
    #   EXT_W5_3_RuntimeKeys uses runtime identity proof schema
    #   EXT_SD_BackendEvidence uses cmul2_mod3683 as an observation candidate
    #   EXT_ServerLink remains scope-gated until 정욱님 defines server-link meaning
    # criteria:
    #   - every EXT has value, blocker, unblock_input, first_action
    #   - no EXT is marked executable without its blocker removed
```

```python
def decide_next_work(ext_map: list[dict]) -> dict:
    """Choose the next action without inventing new internal frontier work."""
    # criteria:
    #   - if 정욱님 says "동기화": run M2_DocSyncBatch
    #   - if external repo is provided: run EXT_W3_5_CIPilot
    #   - if runtime keys are provided: run EXT_W5_3_RuntimeKeys
    #   - if Aer/QPU access is provided: run EXT_SD_BackendEvidence
    #   - if ServerLink scope is defined: design/execute that path
    #   - otherwise stop autonomous expansion and report blocked external queue
```
