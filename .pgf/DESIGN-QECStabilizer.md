# DESIGN — QECStabilizerFamily (Stage 6 · W7.1)

> 새 알고리즘 클래스: **양자오류정정(QEC) stabilizer 인코더**.
> gates→QFT→arithmetic→Shor 수직스택 이후 첫 *수평* 확장. 전부 Clifford → **Tier-0 EXACT**.
> 봉인된 base Clifford(h_gate·cnot)만으로 조립. golden = closed-form 독립공식(parity perm + Sylvester-Hadamard).

## 설계 근거 (가정 명시 — [[pg-subdesign-workflow]])

- **가정 A**: app golden은 full 2ⁿ unitary로 대조된다(`app_assemble.py:159` `hash_unitary(golden)==hash_unitary(V_app)`). isometry 경로 없음 → encoder를 full n-qubit unitary로 봉인. ancilla=|0⟩는 *입력 규약*(n_anc=0). ✔ 코드 확인됨.
- **가정 B**: golden 독립성 = "닫힌형식 수학공식 vs 게이트조립" (qft가 golden=DFT공식인 것과 동일 수준). parity-permutation(불리언 인덱스맵)·Sylvester-Hadamard(부호 인덱스맵)는 게이트 bloq 인스턴스화와 무관하게 구성 → 정직한 독립. ⚠ stabilizer-tableau(Tier-2) 검증이 *더 강한* 독립오라클 — 정직성 노트로 명기, future work.
- **가정 C**: cnot 규약 = targets[control,target], big-endian |c,t⟩→|c,t⊕c⟩. ✔ specs/modules/cnot.pg 확인.
- **가정 D**: compose는 plan-순서 = 회로적용순서(g₁ first). ✔ qft 선례(H 먼저 → 표준 QFT).
- **비파괴**: 모듈 0 추가(기존 h_gate·cnot 재사용), 앱 +4. frozen 23키·fingerprint byte-identical 불변.

## Gantree

```
QECStabilizerFamily // QEC 인코더 클래스 (designing) @v:7.1
    RepCode3Bit // [[3,1]] bit-flip 인코더 (designing)
        # circuit: CNOT(0,1)·CNOT(0,2)
        # golden: |abc> -> |a, b^a, c^a>  (순수 parity permutation, 게이트행렬 0)
        # n_sys=3 Tier-0. |0_L>=|000>, |1_L>=|111>. stab=Z0Z1,Z1Z2
    RepCode3Phase // [[3,1]] phase-flip 인코더 (designing) @dep:RepCode3Bit
        # circuit: CNOT(0,1)·CNOT(0,2)·H(0)·H(1)·H(2)
        # golden: H^⊗3 @ P_parity  (Sylvester-Hadamard @ parity perm)
        # n_sys=3 Tier-0. |0_L>=|+++>, |1_L>=|--->. stab=X0X1,X1X2
    Shor9Encoder // [[9,1,3]] Shor 코드 인코더 — CAPSTONE (designing) @dep:RepCode3Phase
        # circuit(순서): CNOT(0,3)·CNOT(0,6) · H(0)·H(3)·H(6) ·
        #   CNOT(0,1)·CNOT(0,2)·CNOT(3,4)·CNOT(3,5)·CNOT(6,7)·CNOT(6,8)
        # golden: P_bitflip @ H_{0,3,6} @ P_phase  (closed-form 합성, 512×512)
        # n_sys=9 Tier-0. 역사적 첫 QEC코드(Shor1995) ↔ Shor 인수분해 서사 연결
        # |0_L>=(|000>+|111>)^⊗3 / 2√2 , |1_L>=(|000>-|111>)^⊗3 / 2√2
    Syndrome3Bit // bit-flip 신드롬 추출 unitary (designing) @dep:RepCode3Bit
        # circuit: CNOT(0,3)·CNOT(1,3) [Z0Z1→anc3] · CNOT(1,4)·CNOT(2,4) [Z1Z2→anc4]
        # golden: anc3 ^= q0^q1, anc4 ^= q1^q2  (순수 parity copy perm)
        # n_sys=5 Tier-0. 측정前 unitary만 봉인(측정=비unitary 제외, 정직 경계)
    VerifyAndForge // 독립검증 + 봉인 + 비파괴 회귀 (designing) @dep:Shor9Encoder,Syndrome3Bit
        # IndependentVerify: golden 닫힌형식 == sealed u_hash (4/4)
        # 봉인: aa.assemble(spec, APPREG) Tier-0, MatrixGate 0
        # 회귀: reproduce_all REPRODUCED·second_oracle 53/53·contested_guard PASS·
        #       fingerprint+frozen byte-identical
```

## 산출물

- `scripts/qec_family.py` — 생성기+forge+독립검증+정직성리포트(qft_family 구조 미러)
- `specs/apps/repcode3_bitflip.app.pg` · `repcode3_phaseflip.app.pg` · `shor9_encoder.app.pg` · `syndrome3_bitflip.app.pg`
- `registry/apps/*.sealed.json` (Tier-0) · `.pgf/arith/QEC-FAMILY-REPORT.json`

## 검증 기준 (acceptance_criteria)

- [ ] 4 앱 전부 sealed·tier=0 (n_sys≤12)
- [ ] golden 닫힌형식 독립재구성 == sealed u_hash 4/4
- [ ] plan = 봉인 h_gate·cnot 만 (MatrixGate/from_unitary 0 — honest guard 통과)
- [ ] reproduce_all REPRODUCED · second_oracle 53/53 · contested_guard ALL PASS
- [ ] frozen consensus 23키·fingerprint(verify_seal·contracts) byte-identical
- [ ] 모듈 53 불변 · 앱 71→75 · root 갱신(순수 비파괴)
```
