# DESIGN — W9.2 AmplitudeEstimation (QAE) (PG Gantree + PPR)

> W9.1(amplitude *amplification*)을 amplitude *estimation*으로 상승: Grover/Q 연산자에 **QPE**를 걸어
> 진폭 a를 *추정*하는 회로를 봉인. exact instance(θ=π/8 → a=sin²(π/8), t=3 counting이 정확히 읽음).
> Shor의 controlled-U^{2^j} + 봉인 iqft3 근육 복리. honest 분해(controlled-Ry = CNOT·Ry 사다리).

```
AmplitudeEstimation // W9.2 (in-progress) @v:9.2 @dep:W9.1
    RyAnglePrimitives // 진폭준비/회전 analytic Ry 모듈 (designing)
        # Ry(α)=YPowGate(exponent=α/π) up-to-phase (ry_k 패턴). 전역위상 C4 무시.
        RyPi4 // Ry(π/4) — A=진폭준비(a=sin²(π/8)) & cRy(π/2) 반각 (designing)
        RyNegPi4 // Ry(-π/4) — cRy(π/2) 반각 (designing)
        RyPi2 // Ry(π/2) = Grover Q 연산자(a=1/2 아닌 일반각) & cRy(π) 반각 (designing)
        RyNegPi2 // Ry(-π/2) — cRy(π) 반각 (designing)
        # criteria: 4개 sealed tier=0, second_oracle INDEP+4 (57→61)
    ControlledRy // controlled-Ry = honest CNOT·Ry 사다리 (designing) @dep:RyAnglePrimitives
        CryPi2 // controlled-Ry(π/2) (designing)
            # plan=[cnot, ry_negpi4(t), cnot, ry_pi4(t)]; golden=|0><0|⊗I+|1><1|⊗Ry(π/2)
            # 항등식: C-Ry(φ)=(I⊗Ry(φ/2))·CNOT·(I⊗Ry(-φ/2))·CNOT
        CryPi // controlled-Ry(π) (designing)
            # plan=[cnot, ry_negpi2(t), cnot, ry_pi2(t)]; golden=|0><0|⊗I+|1><1|⊗Ry(π)
            # criteria: composite==golden, Tier-0, MatrixGate 0
    QaeCircuit // QPE on Grover Q (designing) @dep:ControlledRy
        Qae3Pi8 // 4q QAE: counting 3 + work 1, a=sin²(π/8) (designing)
            # Q=Ry(π/2)(eigenphase ±2θ=±π/4). powers: Q^4=-I·Q^2=Ry(π)·Q^1=Ry(π/2)
            # plan=[ry_pi4(work), h(c0,c1,c2), z_gate(c0)=cQ^4, cry_pi(c1,work)=cQ^2,
            #       cry_pi2(c2,work)=cQ^1, iqft3(c0,c1,c2)]
            # golden=full 16×16 closed-form circuit. controlled-Q^4=-I → z_gate(control)
            # criteria: composite==golden up-to-phase, Tier-0(n=4≤12), 봉인 iqft3 복리
    BehaviorObservation // 진폭 *추정* 행동 (designing) @dep:QaeCircuit
        # NOT A SEAL. QAE 회로를 |0>에 실행 → counting 측정 y → a_est=sin²(πy/2^t)
        # criteria: y∈{1,7} 각 0.5, 둘 다 a_est=sin²(π/8)=0.146447 (진짜 a와 정확 일치)
    NonDestructiveVerify // 비파괴 전수검증 (designing) @dep:everything
        # reproduce_all REPRODUCED · second_oracle 61/61(+4) · contested ALL PASS
        # fingerprint/frozen byte-identical · CI PASS · 새 root 문서 동기화
```

## 정직성 경계 (PPR 주석)

```python
# 봉인 = QAE 회로(분해의 정확성). composite==golden(up-to-phase), MatrixGate 0.
#   controlled-Ry = honest CNOT·Ry(±φ/2) 사다리(표준 항등식). golden=closed-form 회로 유니터리.
#   봉인 iqft3·cnot·h_gate·z_gate 복리 재사용. Ry 각도 4개만 신규 모듈.
# 봉인 아님 = 진폭 추정 *행동*(BehaviorObservation): 봉인 QAE 를 실행해 counting 측정→a_est.
#   exact instance라 a_est=sin²(π/8) 정확(양 peak y=1,7). W9.1 amplification → W9.2 estimation.
# QAE 핵심: Grover Q 의 고유위상 ±2θ 를 QPE 가 읽음 → a=sin²θ. amplitude→eigenphase→QPE readout.
```
