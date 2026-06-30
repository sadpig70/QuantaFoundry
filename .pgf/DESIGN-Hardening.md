# DESIGN-Hardening — Stage 5 Hardening 잔여 (blind-spot 비파괴 방어)

> PGF design mode · 기반 = `_legacy/roadmap_process_plan.md` Stage 5 (Track E) · 방법 = PG Gantree + PPR.
> 정직성: 분석/검증/문서 전용 비파괴. registry/sealed/frozen/fingerprint(verify_seal.py·contracts.py) 불변.
> 소비 자산(사용만): verify_seal(hash_unitary/fingerprint) · second_oracle(INDEP) · registry_tools(manifest).

---

## 0. 문제 (잔여 blind-spot)

(E) byte-identity 재현은 *환경 조건부*다 — numpy/BLAS/platform/FP 가 바뀌면 깨질 수 있다(외부
재검증 신뢰의 숨은 전제). 또 fingerprint 2파일(verify_seal/contracts) 버그·업그레이드 시 전봉인
무효화 절차가 미문서화(revocation_list 빈배열만). gated panel 의 "≥2 distinct weights"는 Sybil
(한 런타임이 다중 가장)에 무방비. 세 갭을 비파괴로 방어:
W5.1 환경 핀, W5.2 revocation 프로토콜, W5.3 런타임 신원증명[EXT]. + verify_contested_guard "15키"→23키 정정.

---

## 1. Gantree

```
Hardening // blind-spot 비파괴 방어 (designing) @v:0.1
    W5.0_GuardKeyCountFix // verify_contested_guard "15키"→23키 출력 정정 (designing) [SC]
    W5.1_DeterminismEnvPin // BLAS/FP/platform byte-identity 위협 핀 (designing) [SC]
        EnvFingerprint // numpy/BLAS/py/platform 환경지문 캡처 (designing)
        FpRobustnessCheck // hash_unitary 가 FP 잡음(~1e-13)·연산순서 무관 byte-identity (needs-verify) @dep:EnvFingerprint
        Lockfile // requirements.lock(핵심 패키지 핀) (designing)
    W5.2_OracleRevocationProtocol // fingerprint 변경→revocation 절차 (designing) [SC]
        FingerprintAudit // 현 verify_seal/contracts sha256 == sealed 의 oracle/contracts_code_hash (needs-verify)
        RevocationList // manifest revocation_list 운영(현재 빈=정당) (designing) @dep:FingerprintAudit
        EmergencyReseal // rollback + 재봉인 절차 문서 (designing)
    W5.3_RuntimeIdentityProof // Sybil 방어 (designing) [EXT]
        SignedBundleSchema // API key fingerprint + signed submission 스키마 (designing)
        IdentityVerify // 서명검증 로직(self-contained) + 키 수급 relay (designing) @dep:SignedBundleSchema
```

---

## 2. PPR — W5.1 DeterminismEnvPin

```python
# acceptance_criteria:
#   - EnvFingerprint: numpy/BLAS/py/platform 결정론 캡처 → ENV-FINGERPRINT.json
#   - FpRobustnessCheck: hash_unitary 가 (a) ε<QUANT/2 잡음 (b) 행렬곱 결합순서 변경 (c) BLAS
#     누적순서 차이를 흡수해 byte-identical u_hash 산출 → byte-identity 의 환경강건성 실증
#   - Lockfile: 핵심 패키지(numpy 등) 정확버전 핀 → 외부 재검증 신뢰조건 명시

def fp_robustness_check():
    U = INDEP["qft3"]()
    h0 = hash_unitary(U)
    h_noise = hash_unitary(U + 1e-13*random)        # FP 잡음 흡수
    h_reassoc = hash_unitary((A@B)@C) == hash_unitary(A@(B@C))  # 결합순서 무관
    return all byte-identical → 격자 양자화(QUANT 1e-9 + PREQUANT 1e-12)가 환경잡음 차단
```

---

## 3. PPR — W5.2 OracleRevocationProtocol

```python
# acceptance_criteria:
#   - FingerprintAudit: 현 verify_seal.py/contracts.py 의 sha256 가 sealed.json 의
#     oracle_code_hash/contracts_code_hash 와 일치(전 봉인) → fingerprint intact, revocation 불필요
#   - RevocationList: manifest.revocation_list 운영 규약(현재 빈배열 = 정당 명시)
#   - EmergencyReseal: fingerprint 버그/업그레이드 시 rollback + 재봉인 절차 문서(docs/EMERGENCY-RESEAL.md)

def fingerprint_audit():
    cur_oracle = sha256(verify_seal.py)      # finalize_sealed 와 동일 계산
    cur_contracts = sha256(contracts.py)
    for sealed in registry:
        intact = sealed.oracle_code_hash in cur_oracle and sealed.contracts_code_hash in cur_contracts
    # 전부 intact → revocation_list 빈 정당. 하나라도 불일치 → 해당 봉인 revoke 후보
```

---

## 4. PPR — W5.3 RuntimeIdentityProof [EXT]

```python
# acceptance_criteria:
#   - SignedBundleSchema: 제출 bundle = {weights_id, runtime_pubkey, signature, u_hash, nonce}
#     → 한 런타임이 다중 weights_id 가장(Sybil) 시 동일 pubkey 노출로 탐지
#   - IdentityVerify: 서명검증 로직(self-contained, 합성키로 데모) + 실 런타임 키 수급 relay
#   - independence_unit 을 pubkey 로 강화: 같은 pubkey = 같은 독립단위(distinct weights 가장 차단)
```

---

## 5. 불변 제약 / 실행 순서

- 비파괴: `scripts/{determinism_env_check,oracle_rollback_protocol,runtime_identity}.py` 신규 ·
  `requirements.lock`·`docs/EMERGENCY-RESEAL.md`·`.pgf/hardening/` 가산. **fingerprint 2파일 절대 무수정**.
  verify_contested_guard 출력문 정정은 비-fingerprint 파일(안전).
- 공통 verify: `reproduce_all` root `3dae613d` · `second_oracle` · `verify_contested_guard`(frozen 23키).
- 순서: W5.0(정정) → W5.1(env) → W5.2(revocation) → W5.3(identity, self-contained → relay).
