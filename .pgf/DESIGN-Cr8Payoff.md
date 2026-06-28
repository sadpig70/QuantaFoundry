# DESIGN — Cr8Payoff (Stage 6, W6.3 QFTPipelineExtend-cr8 / iqft8)

> PG sub-design. c7x payoff(W6.1)의 **대칭 쌍**. W2.4가 봉인한 다른 primitive `cr8_dag`를 실현 —
> 7큐비트 역-QFT(`iqft7`, cr3~cr7_dag 사다리)를 **8큐비트 `iqft8`**(cr8_dag 추가)로 확장.
> 더 큰 QPE counting register = 위상추정 정밀도. Tier-0(256² ≤ EXACT_BOUND 12), self-contained.

## 분해 패턴 (iqft7에서 도출, 검증된 규칙)

big-endian(qubit0=MSB), n 큐비트 inverse-QFT:
1. **비트반전 swap**: `swap(i, n-1-i)` for i in range(n//2). (n=8 → (0,7)(1,6)(2,5)(3,4))
2. **역-QFT 사다리**: t = n-1 → 0; 각 t에 c = n-1 → t+1 로 `cr_{(c-t)+1}_dag(control=c, target=t)`; 그 후 `H(t)`.
   - 모듈 매핑: k=2 → `cs_dag`(=cr2†), k≥3 → `cr{k}_dag_gate`. n=8 → 최대 k=(7-0)+1=**8 → cr8_dag_gate**.
3. golden = QFT_n† = `DFT(2^n)/√(2^n)` 의 conj().T (app_golden 경로, iqft7과 동일).

## Gantree

```
Cr8Payoff // cr8 활용 깊은 역-QFT (in-progress) @v:6.3
    A_BuildGenerator // gen_iqft_pipeline(n) 작성 (designing)
        # scripts/iqft_family.py — swap+사다리 규칙으로 app spec 생성(파라메트릭 n)
        # 모듈 매핑 k=2→cs_dag, k≥3→cr{k}_dag_gate
    B_RegressionGate // gen_iqft_pipeline(7) == 봉인 iqft7 byte-identical (designing) @dep:A_BuildGenerator
        # ★핵심 정합성: 생성기가 수기 iqft7을 정확 재현하면 패턴 정확 입증
        # u_hash(재생성) == registry/apps/iqft7.sealed.json
    C_ForgeIqft8 // iqft8 봉인 (designing) @dep:B_RegressionGate
        # gen_iqft_pipeline(8) → app_assemble 봉인(cr8_dag 실사용 확인)
        # 독립 검증: QFT8† 독립 재구성 → sealed u_hash 대조
    D_Verify // 결정론 재검증 + 동기화 (needs-verify) @dep:C_ForgeIqft8
        # reproduce_all REPRODUCED · second_oracle 50/50(모듈 불변) · contested_guard ALL PASS
        # fingerprint 무수정 · frozen 23키 불변 · 문서/메모리/roadmap 체크박스
```

## acceptance_criteria

- 구조적: 신규 모듈 0(cr8_dag 이미 봉인). 모듈 50 불변, 앱 62→63.
- 기능적: **regression — gen_iqft_pipeline(7) u_hash == 봉인 iqft7**(패턴 정확성 증명) · iqft8 SEALED tier=0 · cr8_dag 실사용 · 독립 QFT8† u_hash == sealed.
- 결정론: reproduce_all 2회 byte-identical · second_oracle 50/50 · contested_guard ALL PASS(frozen 23).
- 비파괴: fingerprint(verify_seal/contracts) 무수정 · frozen consensus_keys 불변 · 기존 iqft7/shor21 byte 불변.
- 정직: plan=봉인 모듈(h/swap/cs_dag/cr*_dag), MatrixGate 0 · generation≠verification(app_assemble 봉인).

## 정직성 경계

- cr8 payoff = **앱 성장**(root 변경)이나 기존 봉인/frozen/fingerprint byte-identical = 순수 비파괴.
- c7x payoff(W6.1, 산술 frontier)의 대칭 — cr8 payoff(QFT frontier). W2.4 봉인 쌍 완성.
- 정-QFT(qft8_pipeline)는 cr6/7/8_gate(non-dag) 미봉인이라 별건(후속). iqft8가 즉시 가능한 쪽.
