# DESIGN — QftForward (Stage 6, W6.4 ForwardQFTPipelineComplete)

> PG sub-design. iqft8(W6.3, 역-QFT) 비대칭 닫기 — 정-QFT pipeline이 `cr6/7/8_gate`(non-dag)
> 미봉인으로 qft5 이상에서 막혀 있음(cr4/cr5_gate만 봉인). 3개 analytic 게이트 봉인 → forward QFT
> pipeline을 n=8까지 완결. self-contained·Tier-0·비파괴.

## 분해 패턴 (qft4_pipeline에서 도출)

big-endian(qubit0=MSB), n 큐비트 forward-QFT:
1. t = 0 → n-1 (오름차순): `H(t)`; 그 후 c = t+1 → n-1 로 controlled-phase(control=c, target=t), k=(c-t)+1.
   - 모듈 매핑: k=2 → `cs_gate`, k=3 → `ct_gate`, k≥4 → `cr{k}_gate`.
2. 비트반전 swap(i, n-1-i) for i in range(n//2).
3. golden = raw QFT = `DFT(2^n)/√(2^n)` (w=exp(2πi/N)). (iqft의 conj().T 없음.)

cr_k_gate(non-dag) 봉인: `bloq=ZPowGate(exponent=1/2**(k-1)).controlled()`, golden=diag(1,1,1,exp(2πi/2^k)),
meta n_sys=2. cr5_gate 봉인과 동형(k만 변경). qft8은 ladder k 최대=8 → cr6/7/8_gate 필요.

## Gantree

```
QftForward // 정-QFT pipeline 완성 (in-progress) @v:6.4
    A_SealCrGates // cr6/7/8_gate(non-dag) 봉인 (designing)
        # ZPowGate(exponent=1/2**(k-1)).controlled() · golden=diag(1,1,1,exp(2πi/2^k)) · k=6,7,8
        # 신규 모듈 3개 (50→53). 독립 cphase(k) u_hash 대조.
    B_BuildGenerator // gen_qft_pipeline(n) 작성 (designing)
        # scripts/qft_family.py — forward 사다리 규칙(k2→cs_gate,k3→ct_gate,k≥4→cr{k}_gate)
    C_RegressionGate // gen_qft_pipeline(4) == 봉인 qft4_pipeline byte-identical (designing) @dep:B_BuildGenerator
        # ★패턴 정확성: 재봉인 composite==golden 통과 + u_hash == registry/apps/qft4_pipeline
    D_ForgeQft // qft5/6/7/8_pipeline 봉인 (designing) @dep:A_SealCrGates,C_RegressionGate
        # gen_qft_pipeline(5..8) → app_assemble. qft6/7/8은 cr6/7/8_gate 실사용 확인.
        # 독립 QFT_n 재구성 → sealed u_hash 대조.
    E_Verify // 결정론 재검증 + 동기화 (needs-verify) @dep:A_SealCrGates,D_ForgeQft
        # reproduce_all REPRODUCED · second_oracle (50→53 모듈 전부) · contested_guard ALL PASS
        # fingerprint 무수정 · frozen 23키 불변 · 문서/메모리/roadmap 체크박스
```

## acceptance_criteria

- 구조적: cr6/7/8_gate 신규 모듈 3 (50→53), qft5/6/7/8_pipeline 신규 앱 4 (63→67).
- 기능적: cr6/7/8_gate SEALED tier=0·독립 cphase(k) u_hash 일치 3/3 · **regression gen_qft_pipeline(4)==qft4_pipeline** · qft5-8_pipeline SEALED · qft6/7/8은 cr6/7/8_gate 실사용 · 독립 QFT_n u_hash 일치.
- 결정론: reproduce_all 2회 byte-identical · **second_oracle 53/53**(신규 cr6/7/8_gate INDEP 추가) · contested_guard ALL PASS(frozen 23).
- 비파괴: fingerprint(verify_seal/contracts) 무수정 · frozen consensus_keys 불변 · 기존 qft2/3/4_pipeline byte 불변.
- 정직: plan=봉인 모듈(h/swap/cs/ct/cr*_gate), MatrixGate 0 · generation≠verification.

## 정직성 경계

- cr_k_gate(non-dag)는 cr_k_dag와 동형 analytic golden(deg 2^k root, no MatrixGate). second_oracle INDEP에 cphase(k) 추가 필요(50→53 coverage 유지).
- W6.4는 **모듈+앱 성장**(root 변경)이나 기존 봉인/frozen/fingerprint byte-identical = 순수 비파괴.
- iqft8(W6.3)의 정-방향 대칭 완성 — QFT 분해 스토리 정/역 양방향 n=8 완결.
