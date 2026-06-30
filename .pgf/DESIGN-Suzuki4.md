# DESIGN — W12.3 Suzuki4

> W8.3의 2차 Suzuki를 4차 Yoshida composition으로 심화한다. 봉인은 `S4(dt)` 회로 구조의 exact
> decomposition이고, 1차/2차/4차 수렴 차수 비교는 관찰로만 기록한다.

## Gantree

```
W12_3_Suzuki4 // 4th-order Yoshida-Suzuki Hamiltonian simulation steps (done) @v:1.0
    Design // PGF design + review gate (done)
        # output: DESIGN-Suzuki4.md, WORKPLAN-Suzuki4.md, REVIEW-Suzuki4.md
        # criteria: W12_3 MasterRoadmap node exists · Tier/observation boundary explicit
    ModuleSeal // coefficient rotations for Yoshida-4 (done) @dep:Design
        Rz_y4_p // Rz(-p·π/8), p=1/(4-4^(1/3)) (done)
        Rx_y4_p // Rx(-p·π/4), X step for S2(p·dt) (done)
        Rz_y4_q // Rz(-q·π/8), q=1-4p (done)
        Rx_y4_q // Rx(-q·π/4), X step for S2(q·dt) (done)
        # criteria: module seals Tier-0, second_oracle independent formulas added
    AppSeal // 4th-order apps (done) @dep:ModuleSeal
        Rzz_y4_p_half // e^{i(pπ/16)ZZ}=CNOT·rz_y4_p·CNOT (done)
        Rzz_y4_q_half // e^{i(qπ/16)ZZ}=CNOT·rz_y4_q·CNOT (done)
        Tfim3_suzuki4_step // S2(pdt)^2·S2(qdt)·S2(pdt)^2, n=3 (done)
        Tfim4_suzuki4_step // same for n=4 (done)
        # criteria: all apps Tier-0 EXACT, MatrixGate 0
    Observation // order contrast only, not a seal (done) @dep:AppSeal
        # NOT A SEAL. Compare true e^{-iHT} at fixed T=π/4:
        # first-order ratio≈2, second-order ratio≈4, fourth-order ratio≈16 under k doubling.
        # criteria: asymptotic ratios pass for TFIM3 and TFIM4.
    Verification // full regression and invariant gates (done) @dep:Observation
        # commands: suzuki4_family, forge_apps, registry_tools build, semantic_guarantee, citation_gen,
        #           reproduce_all, second_oracle, verify_contested_guard, seal_gate_ci
        # criteria: all pass; fingerprint 2 files unchanged; root growth only
```

## PPR

```python
def w12_suzuki4() -> dict:
    """Seal Yoshida 4th-order Suzuki steps and observe convergence order honestly."""
    # acceptance_criteria:
    #   - MasterRoadmap contains W12_3_Suzuki4 before implementation
    #   - coefficient modules and apps are Tier-0 EXACT
    #   - no MatrixGate or hollow decomposition appears in W12.3 specs
    #   - second_oracle includes independent formulas for new modules
    #   - order observation confirms ratio ~16 for 4th-order on TFIM3/TFIM4
    #   - reproduce_all, second_oracle, verify_contested_guard, seal_gate_ci pass
    design = AI_review_design("Yoshida 4th-order Suzuki exact step with observation-only scaling")
    if design.has_fatal_flaw:
        raise RuntimeError(design.reason)
    modules = seal_yoshida_coefficients()
    apps = seal_suzuki4_apps(modules)
    observation = observe_order_scaling(apps)
    regression = run_verification_gates()
    return {"modules": modules, "apps": apps, "observation": observation, "regression": regression}
```

## 정직성 경계

```python
# 봉인 = 4th-order Suzuki step structure, not the true e^{-iHdt}.
# convergence order = backend/numpy observation, not a seal.
# p/q coefficient modules are necessary because Yoshida coefficients are irrational and cannot be represented
# exactly by existing fixed-angle modules.
```
