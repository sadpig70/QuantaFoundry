# DESIGN — W10.3 ParamShiftGradient (MasterRoadmap › TrackSC › W10_3, 경량·옵션)

> 변분 미분의 정직 관찰. parameter-shift rule ∂⟨Z⟩/∂θ = (⟨Z⟩(θ+π/2)−⟨Z⟩(θ−π/2))/2 를
> 봉인 Ry 모듈 실행으로 시연. **신규 봉인 0 · root 불변**(관찰 전용, registry/오라클/frozen 무변).

```
W10_3_ParamShiftGradient // 변분 미분 관찰 (in-progress) @dep:W10_2
    ShiftObservation // single-Ry parameter-shift (designing)
        # state Ry(θ)|0>, observable Z → ⟨Z⟩=cosθ, exact ∂/∂θ=−sinθ
        # 봉인 모듈 실행(u_hash 게이트): θ=π/4(ry_pi4)·θ+π/2=3π/4(ry_3pi4)·θ−π/2=−π/4(ry_negpi4)
        # param-shift = (⟨Z⟩(3π/4)−⟨Z⟩(−π/4))/2 == −sin(π/4) (exact)
        # ★대비: param-shift = **exact** analytic gradient vs finite-difference = **근사**(O(h²))
        # criteria: param-shift==exact(atol 1e-9) · finite-diff 오차>0(근사 정직) · 신규 봉인 0·root 불변
```

## 정직성 경계 (PPR)
```python
# 봉인 아님 — 봉인된 Ry 모듈을 u_hash 게이트 통과 후 실행(observation). 신규 seal 0, root fa06bd80 불변.
# ★param-shift rule 은 *exact* analytic gradient(근사 아님) — finite-difference(O(h²) 근사)와 대비.
#   execution≠verification 경계: 실행으로 gradient 를 관찰하나, 봉인은 회로뿐.
```
