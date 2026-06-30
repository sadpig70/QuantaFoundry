# DESIGN — W11.1 QAOA (MasterRoadmap › TrackSC › W11_1)

> 변분의 *조합최적화* 자매(새 수평 클래스). MaxCut QAOA p=1 회로를 고정-각 인스턴스로 봉인(Tier-0 EXACT,
> 신규 모듈 0 — cost=cnot·rz_negpi4·cnot, mixer=rx_negpi4, H=h_gate 전부 복리). 근사비 = 관찰(seal 아님).
> ★프로토타입: 작은 그래프(K3·2-node)는 p=1로 풀림(ratio≈1, 부적합) → **P3(0.825)·C4(0.75)** 채택(p=1 최적각에서도 <1).

```
W11_1_QAOA // MaxCut QAOA p=1 (in-progress)
    QAOAInstance // U = Πrx · Π[cnot·rz·cnot] · H^⊗n, 고정각 γ=π/4·β=−π/8 (designing)
        Qaoa_p3 // path P3 (n=3, edges 01·12) — p1-opt ratio 0.825 (designing)
        Qaoa_c4 // cycle C4 (n=4, edges 01·12·23·03) — p1-opt ratio 0.75 (designing)
        # plan=[h(0..n), {cnot(i,j),rz_negpi4(j),cnot(i,j)}_edges, rx_negpi4(0..n)]
        # golden=Πrx_negpi4 · Π(cnot·rz_negpi4·cnot) · ΠH ; composite==golden up-to-phase, MatrixGate 0
        # criteria: Tier-0 EXACT · 신규 모듈 0 · n≤4(EXACT_BOUND 내)
    ApproxObservation // 근사비 관찰 (designing) @dep:QAOAInstance
        # NOT A SEAL. backend_adapter 로 봉인 인스턴스 실행→⟨C⟩(MaxCut cost), C=Σ(1−ZiZj)/2
        # (γ,β) sweep → p1-optimal ⟨C⟩/Cmax = 0.825(P3)·0.75(C4) < 1 (관찰)
        # criteria: 봉인 인스턴스 ⟨C⟩∈[0,Cmax] · p1-opt ratio<1(정직: p=1 유한층=근사)
```

## 정직성 경계 (PPR)
```python
# 봉인 = QAOA 회로 *구조*(고정각 인스턴스). 근사비 = backend_adapter 관찰(seal 아님).
# ★p=1 유한층 → 최적각에서도 ratio<1(P3 0.825·C4 0.75): QAOA 는 근사이지 exact 아님
#   (approximation≠exact·변분 상한≠exact 의 조합최적화 형제). 봉인 부품 전부 W8 복리 → 신규 모듈 0.
# 비파괴: 신규 모듈 0, 앱 +2, frozen 23키·fingerprint byte-identical, root 성장만.
```
