# DESIGN — W8.4 TrotterDynamics (PG Gantree + PPR)

> 봉인된 Trotter step(W8.1~8.3)을 `backend_adapter`로 **반복 실행**해 물리 관측량의 시간 동역학을
> 관찰하고 exact 대각화와 대조한다. **신규 봉인 0 — registry/오라클/frozen/root 불변**(관찰 전용 계층).
> 정직성 3경계 완결: 봉인(분해 정확) ≠ 실행(시뮬레이션) ≠ 검증, 그리고 근사 ≠ exact.

```
TrotterDynamics // W8.4 (in-progress) @v:8.4 @dep:W8.3
    SealedStepGate // 봉인된 그 step 을 실행 (designing)
        # backend_adapter.load_sealed_app(u_hash 게이트) → 봉인 Tier-0 step U 만 실행
        # tfim3_trotter_step(1차)·tfim3_trotter_step2(2차)·tfim4_trotter_step(·_step2)
        # criteria: u_hash 재확인 통과한 것만 반복적용. 변조 시 SealGateError(teeth)
    TimeEvolution // U^k 반복 → 시간 동역학 (designing) @dep:SealedStepGate
        # psi_k = U^k |0...0>, t=k·dt (dt=π/8), k=0..8 (t=0..π). numpy+cirq 두 백엔드
        # criteria: 백엔드간 atol 일치(backends_agree), k별 결정론
    ObservableTrajectory // 물리 관측량 궤적 (designing) @dep:TimeEvolution
        # <Z_0(t)>, <X_0(t)>, <Z_0 Z_1(t)>. backend_adapter.expect_z/corr_zz 재사용 + 로컬 expect_x
        # criteria: 각 관측량 trajectory 산출
    ExactContrast // exact e^{-iHt} 대조 (designing) @dep:ObservableTrajectory
        # 독립 대각화 e^{-iHt}|0> 에서 동일 관측량 → Trotter 오차(관측량 공간)
        # criteria: Trotter 편차가 t 증가에 따라 성장(관찰, seal 아님)
    OrderBasisDependence // ★차수의 basis-의존 (designing) @dep:ExactContrast
        # 항등식: s1 = A^{1/2}·s2·A^{-1/2} (A=ΠZZ(dt), A^{1/2}=ΠZZ(dt/2)) → 1·2차는 Z-대각 켤레
        # ⇒ Z-basis 초기상태에서 <Z>·<ZZ> 관측량은 1차==2차 (측정통계가 차수 구별 불가!)
        #   <X>(transverse)에서만 차수 드러남: 2차가 exact 를 ~3× 더 정확 추종
        # criteria: max|<Z0>_1st - <Z0>_2nd| < 1e-9 (동일) AND <X0> 편차 2nd < 1st (2차 우월)
    NonDestructiveVerify // 비파괴 확인 (designing) @dep:everything
        # registry/root/frozen/fingerprint 전부 불변(신규 봉인 0) — git 으로 registry 무변경 확인
        # reproduce_all REPRODUCED(root 566b0368 그대로) · contested_guard ALL PASS
```

## 정직성 경계 (PPR 주석)

```python
# 이 계층은 아무것도 봉인하지 않는다 — registry/oracle/frozen 키 무수정. root 566b0368 불변.
# 입력 = 이미 봉인된 Tier-0 step(u_hash 게이트). 그것을 U^k 로 *실행*해 동역학을 관찰.
# 3경계 완결:
#   ① 봉인 ≠ 실행: 봉인은 step 분해의 정확성(W8.1~8.3). 실행은 시뮬레이터 동역학(여기). 출력은 봉인 증거 아님.
#   ② 실행 ≠ 검증: spec §8.4 "behavioral check is illustrative only".
#   ③ 근사 ≠ exact: Trotter 궤적 vs e^{-iHt} 편차 = Trotter 오차(관측량 공간 가시화).
# ★ 차수의 basis-의존(honest, 비자명): 1·2차 Trotter가 Z-대각 유니터리로 켤레 → Z-측정은 차수
#   를 구별 못함(동일 통계). 차수 우월(2차)은 transverse <X> 에서만 관측. 측정 basis 가 무엇을
#   드러내는지에 정직.
```
