# DESIGN — W10.2 VQEDeepening (MasterRoadmap › TrackSC › W10_2)

> 마스터 노드 W10_2_VQEDeepening 의 1-2레벨 세부설계. W10.1(1-layer)의 변분 경계를 *깊이/표현력*으로 정량 심화.
> ★프로토타입 검증: 2-layer **shared-θ는 gap 무개선**(0.071→0.071), **per-qubit 독립각(4 param)은 0.071→0.0023**(≈30×↓).
> → 정직 메시지: "ansatz 표현력(독립 파라미터)↑ → 변분 gap↓, **그러나 여전히 >0**"(변분≠exact 의 *깊이* 심화).

```
W10_2_VQEDeepening // 2-layer per-qubit ansatz (in-progress) @dep:W10.1
    L2Ansatz // 2-layer HE = Ry(θa,θb)·CNOT·Ry(θc,θd)·CNOT, per-qubit 독립각 (designing)
        # 봉인 인스턴스(고정각, 기존 Ry 모듈 복리; 신규 모듈 0):
        Vqe_he2_L2_pi4 // (π/4,π/4,π/4,π/4) 단일각 baseline (designing)
        Vqe_he2_L2_mix // (π/4,π/2,−π/4,π/4) 혼합각 — ry_pi4/pi2/negpi4 복리 (designing)
        # plan=[ry_a(0),ry_b(1),cnot(0,1),ry_c(0),ry_d(1),cnot(0,1)]
        # golden=CNOT·(Ry_c⊗Ry_d)·CNOT·(Ry_a⊗Ry_b); composite==golden up-to-phase, MatrixGate 0
        # criteria: Tier-0 EXACT · 신규 모듈 0 · 비파괴(frozen/fingerprint 불변)
    DepthObservation // gap 축소 관찰 (designing) @dep:L2Ansatz
        # NOT A SEAL. backend_adapter 로 봉인 L2 인스턴스 실행→⟨H_TFIM2⟩ (변분상한 ≥Eg)
        # 4-param 그리드 sweep min → gap_L2 ≈ 0.002 << gap_L1 = 0.071 (관찰)
        # criteria: 봉인샘플 ≥Eg · gap_L2 < gap_L1 · gap_L2 > 1e-4(여전히 >0, 정직)
```

## 정직성 경계 (PPR)
```python
# 봉인 = 2-layer ansatz 구조(고정각 인스턴스). 변분 에너지/gap = 관찰(seal 아님).
# 핵심: 깊이만으론 부족(shared-θ gap 무변) — 표현력=독립 파라미터 수가 gap 결정.
#   per-qubit 독립각 2-layer 가 1-layer 대비 gap 30×↓(0.071→0.002) 하나 0 아님 → 변분≠exact 불변.
# 비파괴: 신규 모듈 0, 앱 +2, frozen 23키·fingerprint byte-identical, root 성장만.
```
