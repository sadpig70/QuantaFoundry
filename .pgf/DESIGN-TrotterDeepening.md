# DESIGN — W8.2 TrotterDeepening (PG Gantree + PPR)

> W8.1(HamiltonianSimulation)을 *instance*에서 *family*로 키운다. Pauli-상호작용 회전 집합
> {rxx, ryy, rzz}을 완성하고, Heisenberg 모델 두 인스턴스(single-bond·chain) + multi-step 복리를
> 봉인한다. 정직-근사 경계를 **수렴 관찰**로 심화한다(고정 T, k-step Trotter 오차→0).

```
TrotterDeepening // W8.2 (in-progress) @v:8.2 @dep:W8.1
    SdgModule // S† = diag(1,-i) Clifford Tier-0 primitive (designing)
        # bloq=SGate().adjoint(); golden=diag(1,-1j); ryy basis-change(Z→Y, B=S·H)에 필요
        # criteria: sealed tier=0, u_hash 결정론, second_oracle INDEP+1 (55→56)
    PauliInteractionSet // {rxx, ryy} 앱 — rzz와 함께 상호작용 회전 완성 (designing) @dep:SdgModule
        Rxx // e^{i(π/8)X⊗X} = (H⊗H)·rzz·(H⊗H) (designing)
            # plan=[h0,h1, rzz, h0,h1]; golden=cos·I + i sin·XX; X=HZH 기저변환
            # criteria: composite==golden EXACT, Tier-0, MatrixGate 0
        Ryy // e^{i(π/8)Y⊗Y}, basis B=S·H maps Z→Y (designing) @dep:SdgModule
            # plan=[sdg0,sdg1, h0,h1, rzz, h0,h1, s0,s1]; golden=cos·I + i sin·YY
            # B Z B† = Y (S X S†=Y, X=HZH). compose 재정렬: BBd 먼저(rightmost) 적용
            # criteria: composite==golden EXACT, Tier-0
    HeisenbergFamily // Heisenberg 모델 두 인스턴스 (designing) @dep:PauliInteractionSet
        Heis2 // single-bond H=XX+YY+ZZ 1-step = rxx·ryy·rzz (2q) (designing)
            # plan=[rxx, ryy, rzz](앱 ref); golden=rzz@ryy@rxx
            # ★honest 발견: single bond에서 XX,YY,ZZ 교환 → step이 e^{-iHt}와 *정확* 일치(err~1e-16)
            # criteria: step EXACT 봉인 + 관찰: single-bond exactness(근사 아님)
        Heis3 // chain bonds(0,1),(1,2) 1-step (3q) (designing)
            # plan=[heis-bond(0,1), heis-bond(1,2)]; bond=rxx·ryy·rzz; golden=step(π/8)
            # 겹치는 bond(공유 q1) 비가환 → 진짜 Trotter 오차
            # criteria: step EXACT 봉인; 오차=관찰(seal 아님)
    MultiStepCompound // 복리: 봉인 step 2회 합성 (designing) @dep:W8.1
        Tfim3TwoSteps // tfim3_trotter_step × 2 (3q) (designing)
            # plan=[tfim3_trotter_step, tfim3_trotter_step](앱 ref ×2); golden=step@step
            # criteria: 봉인 step 합성이 EXACT 유지 — "step^k 합성=정확" 실증
    ConvergenceObservation // 정직-근사 심화: 고정 T, k-step 수렴 (designing) @dep:HeisenbergFamily
        # NOT A SEAL. fixed T=π/4, k∈{1,2,4,8,16}, dt=T/k
        # TFIM3·Heis3-chain: 1차 전역오차 O(1/k) → k 2배 시 오차 절반(ratio≈2)
        # Heis2 single-bond: err~1e-16 (교환항 → 정확, 수렴 불필요)
        # criteria: ratio≈2.0(±0.2) 확인 + single-bond exactness 기록
    NonDestructiveVerify // 비파괴 전수검증 (designing) @dep:everything
        # reproduce_all REPRODUCED · second_oracle 56/56 · contested_guard ALL PASS
        # fingerprint/frozen byte-identical · CI gate PASS · 새 root 문서 동기화
```

## 정직성 경계 (PPR 주석)

```python
# 봉인되는 것 = Trotter STEP(분해의 정확성). composite==golden EXACT.
#   golden = closed-form Pauli 지수곱(cos/sin, Qualtran 비의존). plan = 봉인 부품(honest, MatrixGate 0).
# 봉인 아닌 것 = 진짜 e^{-iHT} 와의 Trotter 오차(ConvergenceObservation).
#   "approximation ≠ exact"(execution≠verification 의 자매). O(1/k) 1차 전역수렴.
# 미묘함(honest): single-bond Heisenberg는 교환항 → step이 *정확*(근사 아님). 모든 Trotter가
#   근사인 것은 아니다 — 정직하게 구별 표기.
```
