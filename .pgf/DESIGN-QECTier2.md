# DESIGN — CliffordTier2QEC (Stage 7 · W7.2)

> W7.1 정직성 갭 닫기. 일반 stabilizer 코드는 인코더 full-unitary golden이 회로-특정 →
> *더 강한* 독립오라클 = **stabilizer tableau(Tier-2)**. 그 경로를 실가동해 QEC를 심화.

## 설계 근거 (가정 명시 — [[pg-subdesign-workflow]])

- **가정 A (검증완료)**: Tier-2 CLIFFORD는 `verify_seal.py` module-level `tier="clifford"`로 가용 — `clifford_seal.canonical_tableau_hash`(cirq stabilizer, dense 미사용, 임의크기 정확, 전역위상 무시 유일결정). `app_assemble.py`엔 Tier-2 없음(exact/structural만) → 이들은 **모듈** 봉인. ✔ VerifyTier2Path.
- **가정 B (검증완료)**: Tier-2 advisory(n≤10)는 cirq-dense vs qualtran tensor_contract 변환충실성 체크 — **golden 대조가 아님**. 따라서 "올바른 코드" 증거는 **드라이버의 stabilizer 고유값 witness**(dense numpy, n≤10, cirq 회로=Qualtran spec와 별도 경로)로 독립 확보. ✔
- **가정 C (검증완료)**: Steane=CSS(Hamming [7,4,3]), H H^T=0(자기직교) → |0_L>=(1/√8)Σ_{rowspace(H)}|c>가 6 stabilizer +1. prep 회로=H on pivots{0,1,3}+CNOT(pivot→nonpivot, systematic gen). ✔ scratch 검증(stab 6/6, Z̄ ±1).
- **second_oracle 경계**: dense 재구성 기반 → Tier-2(tableau u_hash) 범위 밖. 53 Tier-0 dense는 53/53 유지(정직 분리; coverage 강제 gate 없음).
- **비파괴**: 모듈 53→56(Tier-2 +3)·앱 75 불변. frozen 23키·fingerprint byte-identical.

## Gantree

```
CliffordTier2QEC // stabilizer-tableau로 QEC 심화 (designing) @v:7.2
    VerifyTier2Path // Tier-2 경로 가용성 점검 — 선행 (done)
        # verify_seal tier=clifford → canonical_tableau_hash. app_assemble 불가 → 모듈경로.
    SteaneZeroT2 // [[7,1,3]] |0_L> 상태준비, Tier-2 (done)
        # CSS(Hamming): H{0,1,3} + CNOT systematic. witness: 6 stab +1, Z̄=+1
    SteaneOneT2 // [[7,1,3]] |1_L>=X^⊗7|0_L>, Tier-2 (done) @dep:SteaneZeroT2
        # witness: 6 stab +1, Z̄=-1
    Shor9EncoderT2 // W7.1 Shor-9 인코더 Tier-2 재봉인 (done)
        # 동일연산 cross-validation: cirq dense == W7.1 closed-form golden(512×512)
    VerifyAndSeal // 봉인 + 독립 witness + 비파괴 회귀 (done) @dep:Shor9EncoderT2
        # seal: verify_seal tier=clifford → tier=2. tableau 재계산==sealed 3/3.
        # witness: Steane stab/logical + shor9 dense==golden. reproduce REPRODUCED·
        #          second_oracle 53/53·contested ALL PASS·fingerprint+frozen byte-identical
```

## 산출물

- `scripts/qec_clifford.py` — 생성기+Tier-2 봉인+독립 stabilizer witness
- `specs/modules/{steane_zero_t2,steane_one_t2,shor9_encoder_t2}.pg`
- `registry/modules/*.sealed.json`(tier=2) · `.pgf/arith/QEC-CLIFFORD-REPORT.json`

## 검증 기준 (acceptance_criteria)

- [x] 3 모듈 sealed·tier=2, 정준 tableau 재계산==sealed 3/3
- [x] Steane witness: 6 stabilizer +1, 논리 Z̄ 고유값 ±1 (zero=+1, one=−1)
- [x] shor9_t2: cirq dense == W7.1 closed-form golden (동일연산)
- [x] plan=Clifford(H·CNOT·X), MatrixGate 0
- [x] reproduce_all REPRODUCED · second_oracle 53/53(dense) · contested ALL PASS
- [x] frozen 23키·fingerprint byte-identical · 모듈 53→56 · 앱 75 불변 · root 갱신
```
