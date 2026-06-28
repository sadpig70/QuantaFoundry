# DESIGN — HamiltonianSimulation (Stage 8 · W8.1)

> 새 *수평* 알고리즘 클래스: 해밀토니안 시뮬레이션(Trotter). 새 primitive 타입 = Pauli-exponential
> 회전(non-Clifford analytic, cr_k 근육 재사용). **정직-근사 showcase**: per-step는 EXACT 봉인,
> 전체 진화의 Trotter 오차는 *관찰*(seal 아님) — "approximation ≠ exact" 정직 경계.

## 설계 근거 (가정 명시 — [[pg-subdesign-workflow]])

- **가정 A (검증완료)**: Qualtran `Rz(θ)`/`Rx(θ)` bloq의 tensor_contract == closed-form analytic golden(diag·cos/sin) 정확 일치(u_hash까지). ✔ scratch.
- **가정 B (검증완료)**: e^{iθ Z⊗Z} = CNOT·(I⊗Rz(-2θ))·CNOT (CNOT Z₁ CNOT = Z₀Z₁ 항등). e^{iθX}=Rx(-2θ). ✔ scratch(dt=π/8, θ=π/8 → Rz(-π/4)·Rx(-π/4)).
- **가정 C (검증완료)**: compose(a,b)=b@a(`contracts.py:277`) → plan순서 [s₁..sₖ]=sₖ@…@s₁. golden을 동일순서 좌측곱으로 구성.
- **정직-근사**: TFIM n=3(J=h=1) 1차 Trotter step은 봉인 golden=Trotter곱(EXACT). 진짜 e^{-iHdt} 와의 오차 ||·||₂=0.39(dt=π/8)·**O(dt²) 스케일링**(0.39→0.106→0.027) = *관찰*(seal 아님). ✔ scratch.
- **비파괴**: 모듈 59→61(rz/rx Tier-0 dense, second_oracle INDEP 추가 → dense 55/55)·앱 75→77. frozen 23키·fingerprint byte-identical.

## Gantree

```
HamiltonianSimulation // Trotter 해밀토니안 시뮬 (designing) @v:8.1
    PauliRotationModules // 새 primitive: Pauli-exponential 회전 (designing)
        # rz_negpi4 = Rz(-π/4) = e^{i(π/8)Z}; rx_negpi4 = Rx(-π/4) = e^{i(π/8)X}. analytic golden.
    RzzInteraction // e^{i(π/8)Z⊗Z} = CNOT·rz_negpi4·CNOT, Tier-0 2q app (designing) @dep:PauliRotationModules
        # golden = cos(π/8)I⊗I + i sin(π/8)Z⊗Z (closed form)
    TfimTrotterStep // TFIM n=3 1차 Trotter step, Tier-0 3q app (designing) @dep:RzzInteraction
        # plan = rzz(0,1)·rzz(1,2)·rx(0)·rx(1)·rx(2). golden = Trotter곱(EXACT 봉인)
    TrotterErrorObservation // 정직-근사: step vs exact e^{-iHdt} (designing) @dep:TfimTrotterStep
        # ||U_trot - exact||₂ + O(dt²) 스케일링. OBSERVATION, NOT a seal.
    VerifyAndForge // 봉인 + 비파괴 회귀 (designing) @dep:TrotterErrorObservation
        # 모듈 verify_seal·앱 app_assemble Tier-0. second_oracle INDEP+2(55/55)·forge_apps APP_LIST+2.
        # reproduce REPRODUCED·contested ALL PASS·fingerprint+frozen byte-identical
```

## 산출물

- `scripts/qsim_family.py` — 생성기+forge+Trotter오차 관찰
- `specs/modules/{rz_negpi4,rx_negpi4}.pg` · `specs/apps/{rzz_pi8,tfim3_trotter_step}.app.pg`
- `registry/...` (Tier-0) · `.pgf/arith/QSIM-FAMILY-REPORT.json` · second_oracle/forge_apps 편집

## 검증 기준 (acceptance_criteria)

- [ ] 모듈 2 sealed Tier-0(analytic golden==bloq), 앱 2 sealed Tier-0(composite==golden)
- [ ] rzz = CNOT·rz·CNOT == e^{i(π/8)ZZ}; trotter step composite==golden
- [ ] 정직-근사: Trotter 오차>0 관찰 + O(dt²) 스케일링(seal 아님 명시)
- [ ] plan=봉인 Rz/Rx/CNOT, MatrixGate 0
- [ ] reproduce_all REPRODUCED · second_oracle 55/55(dense+2) · contested ALL PASS
- [ ] frozen 23키·fingerprint byte-identical · 모듈 59→61 · 앱 75→77 · root 갱신
```
