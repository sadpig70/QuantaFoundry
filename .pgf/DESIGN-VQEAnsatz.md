# DESIGN — W10.1 VQEAnsatz (PG Gantree + PPR)

> 새 수평 클래스: **변분 양자 고유해법(VQE)** hardware-efficient ansatz. ansatz *구조*를 고정-파라미터
> 인스턴스로 봉인(Tier-0 EXACT), 변분 *에너지* ⟨H(θ)⟩와 파라미터 최적화는 *관찰*(변분≠봉인).
> 새 정직 경계: **변분 상한 ≠ exact 바닥에너지**(approximation≠exact 의 자매). Ry(W9.2)·CNOT 복리.

```
VQEAnsatz // W10.1 (in-progress) @v:10.1 @dep:W9.3
    Ry3Pi4Module // landscape 샘플용 Ry(3π/4) (designing)
        # bloq=YPowGate(0.75); golden=Ry(3π/4); ansatz 각도 샘플(min 너머 상승 포착)
        # criteria: sealed tier=0, second_oracle INDEP+1 (61→62)
    HE2Ansatz // 2큐비트 1-layer hardware-efficient ansatz (designing) @dep:Ry3Pi4Module
        # 1 layer = Ry(θ)^⊗2 · CNOT(0,1). 고정 θ 인스턴스 봉인(구조=ansatz, θ=instance)
        Vqe_he2_pi4 // θ=π/4 (ry_pi4 복리) (designing)
        Vqe_he2_pi2 // θ=π/2 (ry_pi2 복리) (designing)
        Vqe_he2_3pi4 // θ=3π/4 (ry_3pi4) (designing)
        # plan=[ry(0), ry(1), cnot(0,1)]; golden=CNOT·(Ry(θ)⊗Ry(θ))
        # criteria: composite==golden, Tier-0, MatrixGate 0
    HE3Ansatz // 3큐비트 1-layer (designing) @dep:HE2Ansatz
        Vqe_he3_pi4 // θ=π/4, CNOT ladder (0,1),(1,2) (designing)
            # plan=[ry(0),ry(1),ry(2), cnot(0,1), cnot(1,2)]; golden=ladder·(Ry^⊗3)
    VariationalObservation // 변분 에너지 (designing) @dep:HE3Ansatz
        # NOT A SEAL. H_TFIM = -(Σ ZZ) - (Σ X). ⟨H(θ)⟩ = <0|A(θ)† H A(θ)|0>
        # backend_adapter 로 봉인 ansatz 실행(u_hash 게이트)→ψ=A|0>→⟨H⟩=ψ†Hψ
        # ★변분원리: ⟨H(θ)⟩ ≥ E_ground 항상(상한). 연속 sweep min → E_ground 접근 but
        #   ansatz-limited gap>0(exact 미도달). 봉인 인스턴스=곡선 위 샘플점
        # criteria: 봉인 3샘플 에너지 전부 ≥Eg; sweep min∈(Eg, best_sample]; gap>0(정직)
    NonDestructiveVerify // 비파괴 전수검증 (designing) @dep:everything
        # reproduce_all REPRODUCED · second_oracle 62/62(+1) · contested ALL PASS
        # fingerprint/frozen byte-identical · CI PASS · 새 root 문서 동기화
```

## 정직성 경계 (PPR 주석)

```python
# 봉인 = ansatz 회로(분해의 정확성). composite==golden, MatrixGate 0. Ry(ry_pi4/pi2/3pi4)·CNOT 복리.
#   봉인되는 것은 ansatz *구조*(고정 θ 인스턴스); 파라미터는 instance 라벨.
# 봉인 아님 = 변분 *에너지* ⟨H(θ)⟩ + 파라미터 최적화(VariationalObservation):
#   backend_adapter 로 봉인 ansatz 실행→⟨H⟩=ψ†Hψ. 변분원리 ⟨H⟩≥E_ground(상한).
# ★새 정직 경계: 변분 상한 ≠ exact 바닥에너지. ansatz 표현력 한계로 gap>0 — VQE 는 근사/상한이지
#   exact 가 아님(정직 표기). execution≠verification·approximation≠exact 의 변분 버전.
```
