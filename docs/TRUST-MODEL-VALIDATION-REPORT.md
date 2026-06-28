# Trust-Model Validation Report (Stage 4 W4.2)

> ρ-discount 실가동 정직 종결. 분석/검증 전용 비파괴.

## 판정

**MECHANISM LIVE — 구성된 co-error 를 lineage-merge + ρ-discount 가 정확히 붕괴; ρ=0 대조로 discount 존재가치 실증; 정답은 통과(false-positive 0). 자연발생 co-error(약모델 패널)는 [EXT] relay 대기.**

## self-contained 검증 (메커니즘)

| 검증 | 결과 | 의미 |
|---|---|---|
| lineage_merge | DIVERGENT ✓ | 같은 weightsA 2소스 → independence_unit 병합으로 1 vote<2 → DIVERGENT |
| rho_discount | INSUFFICIENT/CORPUS_CORRELATED ✓ | distinct unit 2소스 poisoned + ρ=0.6 → N_eff=1.25<2 → CORPUS_CORRELATED escalate |
| rho0_lets_coerror_pass | ESTABLISHED/MULTIMODEL ✓ | ρ=0 이면 distinct-unit poisoned 합의가 ESTABLISHED — ρ-discount 의 존재가치 실증 |
| control_established | ESTABLISHED/MULTIMODEL ✓ | 정답 2독립소스 → ESTABLISHED (false-positive 아님) |

N_eff(2소스) sweep: `{'rho=0.0': 2.0, 'rho=0.3': 1.538, 'rho=0.6': 1.25, 'rho=1.0': 1.0}`

## 정직 구분

- **메커니즘 실가동**: 구성된 poisoned 합의(little-endian QFT 등)를 independence_unit 병합 + ρ-discount 가 정확히 붕괴(DIVERGENT/CORPUS_CORRELATED). ρ=0 대조에서 co-error 가 ESTABLISHED 되는 위험을 실증해 discount 의 존재가치를 확인. 정답 2독립소스는 통과(false-positive 0).
- **[EXT] 자연발생 co-error**: 표준게이트 4라운드 co-error 0(frontier 모델 견고). 약모델/poisoned 패널이 *자연발생적으로* 같은 틀린 답에 수렴하는지는 실런타임 수급 필요 → `_workspace/crossmodel/p3d_round5_poison/` 패키지 relay.

## 최종 라벨

ρ-discount = **설계+메커니즘 실가동(구성된 co-error 붕괴 입증)**. 자연발생 co-error 통계는 EXT 수급 시 확정. 과장(ρ 만능) 제거, 미가동 오해(설계만)도 제거 — 정직 종결.
