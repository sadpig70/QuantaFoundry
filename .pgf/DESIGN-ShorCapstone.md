# DESIGN — ShorCapstone (Stage 6, W6.5 genuine distinct-prime Shor-91)

> PG sub-design. W6.1~W6.4가 만든 조각을 **완전한 Shor 인수분해 회로로 조립** — capstone.
> N=91=7×13 (둘 다 >5, 진짜 distinct-prime). 부품: cmul{2,4,16,74}_mod91(W6.1 c7x-engine)
> + iqft8(W6.3) + H. 15큐비트 > EXACT_BOUND(12) → **Tier-1 STRUCTURAL**(dense 미봉인, Merkle).

## 구조 (shor21 mirror, big-endian)

- 15 큐비트: counting c0..c7 (8) | work w0..w6 (7, 값 mod 91).
- ord_91(2)=12. controlled-U^(2^j), U=×2 mod 91. counting qubit (t-1-j) → 2^(2^j) mod 91:
  - q7→2, q6→4, q5→16, q4→74(=2^8), q3→16(2^16), q2→74(2^32), q1→16(2^64), q0→74(2^128).
  - powa[q0..q7] = [74, 16, 74, 16, 74, 16, 4, 2]. distinct multiplier = {2,4,16,74}.
- plan: H(c0..c7) · controlled-cmul_{powa[q]}_mod91(q, w0..w6) · iqft8(c0..c7).
- 판독(illustrative §8.4): counting/256 연속분수 → r=12 → 2^6=64, gcd(64−1,91)=7·gcd(64+1,91)=13 → 91=7×13.

## Tier 메커니즘 (app_assemble)

- n_sys=15 > EXACT_BOUND(12) → `exact=False` → **Tier-1 STRUCTURAL** 자동.
- u_hash = `_structural_hash(children, n_sys)` = sha256(자식 u_hash + 합성구조 Merkle). dense V 미실체화(2^15 불가).
- plan.tier="structural" 명시(golden 생략 — 2^15 golden 작성 불가). 자식(cmul·iqft8·h)은 전부 Tier-0 봉인.

## Gantree

```
ShorCapstone // genuine distinct-prime Shor-91 (in-progress) @v:6.5
    A_ForgeMultipliers // cmul4/16/74_mod91 봉인 (designing)
        # arith_family.synth_distinct_prime([(4,91),(16,91),(74,91)]) — c7x-engine, Tier-0 8q
        # 독립 산술순열 u_hash==sealed · 전부 c7x 실사용
    B_AssembleShor91 // shor91.app.pg 조립 + 봉인 (designing) @dep:A_ForgeMultipliers
        # plan(H^8 + controlled-cmul + iqft8, tier="structural", golden 생략) → app_assemble Tier-1
        # 자식 전부 sealed 확인 → structural u_hash 결정론
    C_StructuralVerify // 구조·결정론·행동(illustrative) (designing) @dep:B_AssembleShor91
        # children 전부 sealed · structural u_hash 2회 동일 · period r=12→gcd(2^6±1,91)=7,13
    D_Verify // 결정론 재검증 + 동기화 (needs-verify) @dep:B_AssembleShor91
        # reproduce_all REPRODUCED · second_oracle 53/53 · contested_guard ALL PASS
        # fingerprint 무수정 · frozen 23키 불변 · 문서/메모리/roadmap 체크박스
```

## acceptance_criteria

- 구조적: cmul4/16/74_mod91 신규앱 3 + shor91 신규앱 1 (67→71). 모듈 53 불변.
- 기능적: cmul 3개 SEALED tier=0·c7x 실사용·독립순열 일치 · **shor91 SEALED tier=1(STRUCTURAL)** · 자식 전부 sealed · period r=12→7×13.
- 결정론: reproduce_all 2회 byte-identical · second_oracle 53/53 · contested_guard ALL PASS(frozen 23).
- 비파괴: fingerprint(verify_seal/contracts) 무수정 · frozen consensus_keys 불변 · 기존 봉인 byte-identical.
- 정직: plan=봉인 부품, MatrixGate 0 · **Tier-1=structural(dense보다 약한 보증) 명시** · period readout=illustrative(§8.4).

## 정직성 경계 (중요)

- **Tier-1 STRUCTURAL은 dense Tier-0보다 약한 봉인**: 전체 유니터리를 dense 검증하지 않고, 봉인된 부품들이
  계획된 구조로 조립됨을 Merkle로 인증. shor15/21(Tier-0 dense)과 보증 등급이 다름 — 명시 표기.
- t=8 counting(iqft8): 2^8=256 < 2r²=288(textbook sufficiency 약간 미달). period readout 확률에만 영향,
  **구조적 봉인은 t 무관**. t=9(iqft9)는 cr9_dag 선행봉인 필요 = 별건(c8x/cr9 frontier).
- period readout(r=12→7,13)은 **illustrative only(§8.4)** — 봉인 증거 아님.
- ghz16에 이은 두 번째 Tier-1이자 훨씬 복잡 = 알고리즘 규모 structural-composition 검증 입증.
