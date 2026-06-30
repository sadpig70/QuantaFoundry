# DESIGN — W12.1 Query/Oracle Algorithms

> 정욱님 지시로 `SC_Closure` 이후 새 W12.x self-contained 방향을 재개한다. 목표는 query model의
> 대표 알고리즘 Deutsch-Jozsa, Bernstein-Vazirani, Simon을 봉인 앱으로 추가하고, query advantage는
> `backend_adapter` 관찰로만 표기한다.

## Gantree

```
W12_1_QueryOracleAlgos // Query/oracle algorithms (done) @v:1.0
    Design // PGF design + review gate (done)
        # output: DESIGN-QueryAlgos.md, WORKPLAN-QueryAlgos.md, REVIEW-QueryAlgos.md
        # criteria: W12_1 MasterRoadmap node exists · Tier/observation boundary explicit
    AppSeal // Tier-0 app seals, 신규 모듈 0 (done) @dep:Design
        DeutschJozsa // n=2 constant/balanced one-query exact distinction (designing)
            Dj2_const1 // f(x)=1, oracle=X on output (done)
            Dj2_balanced_xor // f(x)=x0 xor x1, oracle=CNOT0y·CNOT1y (done)
        BernsteinVazirani // n=3 secret string exact recovery (designing)
            Bv3_s101 // secret s=101, oracle=CNOT0y·CNOT2y (done)
        Simon // n=2 hidden xor period support constraint (designing)
            Simon2_s11 // f(x)=x0 xor x1, hidden period s=11 (done)
        # plan: write specs/apps/*.app.pg, seal with app_assemble, add to forge_apps APP_LIST
        # criteria: all apps Tier-0 EXACT, MatrixGate 0, composite==golden, 신규 모듈 0
    Observation // behavior-only query advantage evidence (done) @dep:AppSeal
        # NOT A SEAL. backend_adapter loads sealed apps by u_hash gate, runs |0...0> input.
        # DJ: constant -> query 00, balanced -> nonzero 11.
        # BV: query register -> 101 with prob 1.
        # Simon: query support subset {00,11}, every y satisfies y·s=0 mod 2 for s=11.
        # criteria: deterministic/support checks pass; report marks observation != seal.
    Verification // full regression and invariant gates (done) @dep:Observation
        # commands: query_family, forge_apps, registry_tools build, semantic_guarantee, citation_gen,
        #           reproduce_all, second_oracle, verify_contested_guard, seal_gate_ci
        # criteria: all pass; fingerprint 2 files unchanged; root growth only
```

## PPR

```python
def w12_query_oracle_algorithms() -> dict:
    """Seal small query/oracle algorithms and observe query advantage honestly."""
    # acceptance_criteria:
    #   - MasterRoadmap contains W12_1_QueryOracleAlgos before implementation
    #   - DESIGN/WORKPLAN/status artifacts exist under .pgf/
    #   - apps dj2_const1, dj2_balanced_xor, bv3_s101, simon2_s11 are Tier-0 EXACT
    #   - no new module seal is created; all plans use h_gate, x_gate, cnot only
    #   - behavior report separates query advantage observations from seal claims
    #   - reproduce_all, second_oracle, verify_contested_guard, seal_gate_ci pass
    design = AI_review_design("Tier-0 query circuits with observation-only behavior")
    if design.has_fatal_flaw:
        raise RuntimeError(design.reason)
    apps = seal_query_apps()
    observations = observe_query_behavior(apps)
    regression = run_verification_gates()
    return {"apps": apps, "observations": observations, "regression": regression}
```

## 정직성 경계

```python
# 봉인 = oracle algorithm circuit unitary decomposition, Tier-0 EXACT.
# query advantage = backend_adapter observation, not a seal.
# Deutsch-Jozsa/BV one-query exact recovery and Simon support constraint are behavior claims over sealed U.
# 신규 모듈 0: h_gate/x_gate/cnot 복리만 사용한다.
```
