# DESIGN — W9.3 QAEDeepening (PG Gantree + PPR)

> W9.2(QAE instance)를 family로: ① 두 번째 QPE-QAE 인스턴스(a=1/2, 신규 모듈 0) — QAE가 다른
> 진폭에도 일반화함을 봉인; ② **iterative/power QAE(QPE-free)** — P_good(m)=sin²((2m+1)θ) 곡선의
> 고전 fit으로 *임의* θ 추정(a=1/4·1/8 등 QPE bin에 안 떨어지는 일반 진폭). backend_adapter 실행 복리.

```
QAEDeepening // W9.3 (in-progress) @v:9.3 @dep:W9.2
    SecondQpeInstance // 두 번째 exact QPE-QAE (designing)
        Qae3Pi2 // a=1/2, t=3, Q=Ry(π) (designing)
            # plan=[ry_pi2(work), h(c0,c1,c2), z_gate(c1)=Q^2, cry_pi(c2,work)=Q^1, iqft3]
            # Q^4=Ry(4π)=I → c0 무게이트(H+iqft만). 신규 모듈 0(전부 봉인 부품 복리)
            # golden=16×16 closed-form. readout y∈{2,6}→a_est=sin²(π/4)=1/2 (관찰)
            # criteria: composite==golden up-to-phase, Tier-0
    IterationFamilyExtend // Grover power m=3 (designing) @dep:W9.1
        Grover2_3iter // G₂³ (2q) (designing)
            # plan=[grover2, grover2, grover2]; golden=G₂³
        Grover3_3iter // G₃³ (3q) (designing)
            # plan=[grover3, grover3, grover3]; golden=G₃³
            # criteria: composite==golden, Tier-0
    IterativeQaeObservation // QPE-free 진폭추정 (designing) @dep:IterationFamilyExtend
        # NOT A SEAL. backend_adapter 로 봉인 Grover power 실행(u_hash 게이트)
        # P_good(m) = |<target|Q^m A|0>|² = sin²((2m+1)θ), m=0..3
        # 고전 least-squares fit θ → a_est=sin²θ. QPE 불필요(곡선이 θ 결정)
        # ★일반 θ: a=1/4(θ=π/6)·a=1/8(θ=arcsin 1/√8) — QPE bin 에 안 떨어지는 진폭도 추정
        # criteria: grover2→a_est≈1/4·grover3→a_est≈1/8 (true 와 1e-3 이내)
    QpeVsIterativeContrast // 두 QAE 패러다임 정직 대비 (designing)
        # QPE-QAE: one-shot exact, 단 2θ/2π=k/2^t 특수진폭만 (a=sin²(π/8)·a=1/2)
        # iterative-QAE: 다중측정+고전fit, 임의 진폭 (a=1/4·1/8) 단 정밀도=측정수 의존
    NonDestructiveVerify // 비파괴 전수검증 (designing) @dep:everything
        # reproduce_all REPRODUCED · second_oracle 61/61 불변(신규 모듈 0) · contested ALL PASS
        # fingerprint/frozen byte-identical · CI PASS · 새 root 문서 동기화 (앱만 +3)
```

## 정직성 경계 (PPR 주석)

```python
# 봉인 = QAE 회로/Grover power(분해의 정확성). composite==golden(up-to-phase), MatrixGate 0.
#   qae3_pi2·grover2/3_3iter 전부 봉인 부품 복리(신규 모듈 0). second_oracle 61/61 불변.
# 봉인 아님 = 진폭 추정 *행동*(IterativeQaeObservation): backend_adapter 로 봉인 Grover power 실행
#   → P_good(m) 곡선 → 고전 fit. execution≠verification([[backend-adapter]]); 추정치는 관찰.
# ★정직 대비: QPE-QAE(W9.2)는 특수진폭만 exact, iterative-QAE는 임의진폭(일반 θ) 추정 — 단
#   정밀도가 측정수에 의존(공짜 아님). 두 패러다임의 trade-off 정직 표기.
```
