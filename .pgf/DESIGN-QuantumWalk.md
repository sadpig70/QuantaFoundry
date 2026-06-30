# DESIGN — W12.2 Quantum Walk

> W12.1 query/oracle 이후의 다음 self-contained 수평 확장. 목표는 coined quantum walk on cycle을
> 작은 exact app으로 봉인하고, 반복 step에서 나타나는 간섭/확산 패턴은 관찰로만 기록하는 것이다.

## Gantree

```
W12_2_QuantumWalk // coined quantum walk on cycles C4/C8 (done) @v:1.0
    Design // PGF design + review gate (done)
        # output: DESIGN-QuantumWalk.md, WORKPLAN-QuantumWalk.md, REVIEW-QuantumWalk.md
        # criteria: W12_2 MasterRoadmap node exists · Tier/observation boundary explicit
    AppSeal // Tier-0 app seals, 신규 모듈 0 (done) @dep:Design
        C4Walk // coin qubit + 2-bit position register (done)
            Qw_c4_step // U=S4·(H_coin) (done)
            Qw_c4_2steps // U^2 via sub-app reuse (done)
        C8Walk // coin qubit + 3-bit position register (done)
            Qw_c8_step // U=S8·(H_coin) (done)
            Qw_c8_3steps // U^3 via sub-app reuse (done)
        # C4 shift: p0 ^= p1 ^ coin; p1 ^= 1.
        # C8 shift: controlled increment/decrement with c3x/toffoli/cnot/x.
        # criteria: all apps Tier-0 EXACT, MatrixGate 0, 신규 모듈 0
    Observation // behavior-only walk dynamics (done) @dep:AppSeal
        # NOT A SEAL. backend_adapter loads sealed apps by u_hash gate.
        # Observe position marginals from |coin=0,pos=0> and compare C8 quantum vs classical spread.
        # criteria: distributions normalized, C4 adjacent support at step1, C8 TV distance from classical > threshold
    Verification // full regression and invariant gates (done) @dep:Observation
        # commands: quantum_walk_family, forge_apps, registry_tools build, semantic_guarantee, citation_gen,
        #           reproduce_all, second_oracle, verify_contested_guard, seal_gate_ci
        # criteria: all pass; fingerprint 2 files unchanged; root growth only
```

## PPR

```python
def w12_quantum_walk() -> dict:
    """Seal coined quantum walk steps and observe dynamics honestly."""
    # acceptance_criteria:
    #   - MasterRoadmap contains W12_2_QuantumWalk before implementation
    #   - DESIGN/WORKPLAN/status artifacts exist under .pgf/
    #   - apps qw_c4_step, qw_c4_2steps, qw_c8_step, qw_c8_3steps are Tier-0 EXACT
    #   - no new module seal is created; plans reuse h_gate, x_gate, cnot, toffoli, c3x only
    #   - behavior report separates position-distribution observations from seal claims
    #   - reproduce_all, second_oracle, verify_contested_guard, seal_gate_ci pass
    design = AI_review_design("coined walk exact steps with observation-only dynamics")
    if design.has_fatal_flaw:
        raise RuntimeError(design.reason)
    apps = seal_walk_apps()
    observations = observe_walk_dynamics(apps)
    regression = run_verification_gates()
    return {"apps": apps, "observations": observations, "regression": regression}
```

## 정직성 경계

```python
# 봉인 = coined quantum walk step / repeated-step unitary decomposition, Tier-0 EXACT.
# walk dynamics = backend_adapter observation, not a seal.
# C4/C8 shift circuits are reversible exact permutations; spread/interference claims are behavior-only.
# 신규 모듈 0: h_gate/x_gate/cnot/toffoli/c3x 복리만 사용한다.
```
