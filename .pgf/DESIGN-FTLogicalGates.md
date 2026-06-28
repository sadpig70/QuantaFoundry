# DESIGN — FaultTolerantLogicalGates (Stage 7 · W7.3)

> QEC 서사의 클라이맥스: **transversal 논리 Clifford 게이트**(fault-tolerance의 실체).
> 전부 Clifford → Tier-2 stabilizer-tableau 봉인. 특히 **논리 CNOT(14q)=2^14 dense 불가** →
> Tier-2 dense-free 강점을 *처음으로 스케일*에서 실증.

## 설계 근거 (가정 명시 — [[pg-subdesign-workflow]])

- **가정 A (검증완료)**: Steane [[7,1,3]]는 doubly-even self-dual CSS → transversal {H, S, CNOT} 전부 코드보존 valid 논리연산. scratch 확인: H^⊗7=논리 H, S^⊗7=논리 S†(상대위상 −i), CNOT^⊗7(14q)=논리 CNOT 4/4.
- **가정 B**: 봉인할 논리 S는 **S†^⊗7**(=ZPowGate(-0.5)^⊗7) → 논리 S(+i). transversal S(=S^⊗7)는 논리 S†. 둘 다 valid FT; 명명은 봉인하는 게이트가 *구현하는* 논리연산으로(정직).
- **가정 C (검증완료)**: 3 bloq 전부 `is_clifford`=True, `canonical_tableau_hash` 산출. 14q는 dense 미사용(Tier-2). ✔ scratch.
- **witness(오라클 독립, 드라이버)**: n=7은 dense 작용; n=14는 논리기저 벡터(2^14=16384) 작용만(full unitary 미실체화). W7.2 |0_L>/|1_L> prep 재사용([[qec-stabilizer-family]]).
- **비파괴**: 모듈 56→59(Tier-2 +3)·앱 75 불변. frozen 23키·fingerprint byte-identical.

## Gantree

```
FaultTolerantLogicalGates // Steane transversal 논리 Clifford (designing) @v:7.3
    SteaneLogicalH // 논리 H = H^⊗7, Tier-2 7q (designing)
        # witness: H^⊗7|0_L>=(|0_L>+|1_L>)/√2, |1_L>→(|0_L>-|1_L>)/√2
    SteaneLogicalS // 논리 S = S†^⊗7, Tier-2 7q (designing)
        # witness: S̄|0_L>=|0_L>(코드보존), S̄|1_L>=+i|1_L> (논리 S 위상)
    SteaneLogicalCNOT // 논리 CNOT = CNOT^⊗7 블록간, Tier-2 14q (designing)
        # ★ 2^14 dense 불가 → Tier-2 dense-free 스케일 실증
        # witness: 4 논리기저 |ab_L>=psi_a⊗psi_b → |a,a⊕b_L> (16384벡터)
    VerifyAndSeal // 봉인 + 독립 witness + 비파괴 회귀 (designing) @dep:SteaneLogicalCNOT
        # seal: verify_seal tier=clifford → tier=2. tableau 재계산==sealed 3/3.
        # witness: H̄/S̄(n=7 dense)·CNOT̄(n=14 논리기저). reproduce REPRODUCED·
        #          second_oracle 53/53·contested ALL PASS·fingerprint+frozen byte-identical
```

## 산출물

- `scripts/qec_logical.py` — 생성기+Tier-2 봉인+독립 논리작용 witness
- `specs/modules/{steane_logical_h,steane_logical_s,steane_logical_cnot}.pg`
- `registry/modules/*.sealed.json`(tier=2) · `.pgf/arith/QEC-LOGICAL-REPORT.json`

## 검증 기준 (acceptance_criteria)

- [ ] 3 모듈 sealed·tier=2, 정준 tableau 재계산==sealed 3/3
- [ ] H̄: H^⊗7 가 |0_L>/|1_L> → 올바른 논리 H 중첩 (dense n=7)
- [ ] S̄: S†^⊗7 코드보존 + |1_L> 위상 +i (논리 S)
- [ ] CNOT̄: 14q transversal 이 4 논리기저를 |a,a⊕b_L>로 (Tier-2 dense-free)
- [ ] plan=Clifford(H·CNOT·ZPowGate(-0.5)), MatrixGate 0
- [ ] reproduce_all REPRODUCED · second_oracle 53/53(dense) · contested ALL PASS
- [ ] frozen 23키·fingerprint byte-identical · 모듈 56→59 · 앱 75 불변 · root 갱신
```
