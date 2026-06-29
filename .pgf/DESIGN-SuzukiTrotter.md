# DESIGN — W8.3 SuzukiTrotter (PG Gantree + PPR)

> W8.1/W8.2(1차 Trotter)에 **2차 Suzuki-Trotter(대칭 분할)**를 추가하고, 격자를 4큐비트로 확장한다.
> 정직-근사 경계를 **근사 *차수* 대비**로 심화: 1차 O(1/k) vs 2차 O(1/k²)(고정 T, ratio 2 vs 4).
> 분해는 EXACT 봉인, 차수는 관찰 — "approximation *quality* 도 정량화 가능".

```
SuzukiTrotter // W8.3 (in-progress) @v:8.3 @dep:W8.2
    HalfAngleModule // 반각 ZZ 회전에 필요한 primitive (designing)
        RzNegPi8 // Rz(-π/8) = e^{i(π/16)Z} = diag(e^{iπ/16}, e^{-iπ/16}) Tier-0 (designing)
            # bloq=Rz(-np.pi/8); golden=diag(e^{iπ/16},e^{-iπ/16}); rzz_pi16(반각 ZZ)에 필요
            # criteria: sealed tier=0, second_oracle INDEP+1 (56→57)
    HalfAngleZZ // e^{i(π/16)Z⊗Z} = CNOT·rz_negpi8·CNOT (designing) @dep:RzNegPi8
        RzzPi16 // 반각 ZZ 상호작용 (2q) (designing)
            # plan=[cnot, rz_negpi8, cnot]; golden=cos(π/16)I + i sin(π/16)ZZ
            # criteria: composite==golden EXACT, Tier-0
    SecondOrderStep // 2차 Suzuki step: 대칭 분할 (designing) @dep:HalfAngleZZ
        Tfim3Step2 // TFIM3 2차 step (3q) (designing)
            # plan=ΠZZ(d/2)·ΠX(d)·ΠZZ(d/2) = rzz_pi16(0,1),rzz_pi16(1,2), rx(0,1,2), rzz_pi16(0,1),rzz_pi16(1,2)
            # golden=대칭곱(EXACT 봉인); per-step 오차 O(dt³) → 전역 O(dt²)
            # criteria: composite==golden EXACT, Tier-0
    LatticeExtension // 4큐비트 격자 확장 (designing) @dep:SecondOrderStep
        Tfim4Step // TFIM4 1차 step (4q) (designing)
            # plan=rzz_pi8(0,1),rzz_pi8(1,2),rzz_pi8(2,3), rx(0..3); n=4 ≤ EXACT_BOUND(12)
        Tfim4Step2 // TFIM4 2차 step (4q) (designing) @dep:Tfim3Step2
            # plan=ΠZZ_pi16(bonds)·ΠX(sites)·ΠZZ_pi16(bonds)
            # criteria: 둘 다 composite==golden EXACT, Tier-0
    OrderContrastObservation // 정직-근사 심화: 차수 대비 (designing) @dep:LatticeExtension
        # NOT A SEAL. fixed T=π/4, k∈{1,2,4,8,16}
        # 1차 ratio≈2 (O(1/k), per-step O(dt²)) vs 2차 ratio≈4 (O(1/k²), per-step O(dt³))
        # TFIM3·TFIM4 둘 다. criterion: 1차 tail ratio∈[1.9,2.1], 2차 tail ratio∈[3.8,4.2]
    NonDestructiveVerify // 비파괴 전수검증 (designing) @dep:everything
        # reproduce_all REPRODUCED · second_oracle 57/57 · contested_guard ALL PASS
        # fingerprint/frozen byte-identical · CI gate PASS · 새 root 문서 동기화
```

## 정직성 경계 (PPR 주석)

```python
# 봉인 = Trotter STEP(1차·2차 둘 다 분해의 정확성). composite==golden EXACT, MatrixGate 0.
#   golden = closed-form Pauli 지수곱(cos/sin, Qualtran 비의존). plan = 봉인 부품.
# 봉인 아님 = 진짜 e^{-iHT} 와의 오차 + 그 *수렴 차수*(OrderContrastObservation).
#   W8.2가 "근사는 수렴한다"(O(1/k))를 보였다면, W8.3은 "근사의 *품질(차수)* 도 정량화된다"
#   (1차 O(1/k) vs 2차 O(1/k²))를 보인다. approximation≠exact 경계의 차수-해상도 심화.
```
