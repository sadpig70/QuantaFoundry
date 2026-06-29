# DESIGN — W9.1 AmplitudeAmplification (PG Gantree + PPR)

> Grover(grover2)를 **amplitude amplification 패밀리**로 일반화: 3큐비트 확산/Grover 연산자 +
> 반복 횟수(iteration) 봉인. 정직-behavior: amplitude amplification 프로파일(최적-k·over-rotation).
> 기존 봉인 부품(x_gate·ccz·h_gate·cz·reflect00·diffusion) 복리 재사용. 신규 모듈 0.

```
AmplitudeAmplification // W9.1 (in-progress) @v:9.1 @dep:grover2
    Reflect3 // 3큐비트 |000> 반사 (designing)
        Reflect000 // 2|000><000|-I = (X^⊗3)·CCZ·(X^⊗3) (designing)
            # plan=[x0,x1,x2, ccz, x0,x1,x2]; golden=diag(1,-1,...,-1) (전역위상 흡수, reflect00 패턴)
            # criteria: composite==golden up-to-phase, Tier-0, 봉인 x_gate·ccz 재사용
    Diffusion3 // 3큐비트 확산 D₃ = 2|s><s|-I (designing) @dep:Reflect000
        # plan=[h0,h1,h2, reflect000, h0,h1,h2]; golden=H^⊗3·reflect000·H^⊗3
        # criteria: == 2|s><s|-I (uniform 중첩 반사), Tier-0
    Grover3 // 3큐비트 Grover 1-iterate (designing) @dep:Diffusion3
        # G₃ = D₃∘O₃, O₃=ccz(|111> 표시). plan=[{ccz}, {diffusion3}]; golden=D₃@O₃
        # behavior(관찰): P(|111>)=0.781 (1 iterate, N=8 M=1 sub-optimal)
        # criteria: composite==golden, Tier-0
    IterationFamily // 반복 횟수 = amplitude amplification (designing) @dep:Grover3
        Grover3_2iter // G₃² (designing)
            # plan=[grover3, grover3]; golden=(D₃@O₃)²
            # ★behavior: P(|111>)=0.945 (2 iterate = N=8 최적-k). 최적성 실증
        Grover2_2iter // G₂² (designing) @dep:grover2
            # plan=[grover2, grover2]; golden=(D₂@O₂)²
            # ★behavior: P(|11>)=0.25 (over-rotation; N=4는 1 iterate가 P=1 최적, 2는 과회전)
    BehaviorObservation // amplitude amplification 프로파일 (designing) @dep:IterationFamily
        # NOT A SEAL. 봉인 G^k 를 |s>에 적용 → P_target(k). 이론 sin²((2k+1)θ) 대조
        # criteria: grover3 k=1/2/3 → 0.781/0.945/0.330; grover2 k=1/2 → 1.0/0.25 (이론 일치)
    NonDestructiveVerify // 비파괴 전수검증 (designing) @dep:everything
        # reproduce_all REPRODUCED · second_oracle 불변(57/57, 신규 모듈 0) · contested ALL PASS
        # fingerprint/frozen byte-identical · CI PASS · 새 root 문서 동기화 (앱만 +5)
```

## 정직성 경계 (PPR 주석)

```python
# 봉인 = Grover/amplitude-amplification 연산자(분해의 정확성). composite==golden(up-to-phase), MatrixGate 0.
#   골든=closed-form(reflection/diffusion 곱), plan=봉인 부품(x_gate·ccz·h_gate·diffusion3·grover3 복리).
# 봉인 아님 = amplitude amplification 프로파일 P_target(k)(BehaviorObservation): 봉인 G^k 를 실행한
#   행동 관찰. 최적-k(N=8→k=2, P=0.945)와 over-rotation(N=4→k=2, P=0.25)은 *관찰*이지 봉인 아님.
# 신규 모듈 0 — second_oracle(57/57) 불변. 앱만 +5(Tier-0). 순수 비파괴 가산.
```
