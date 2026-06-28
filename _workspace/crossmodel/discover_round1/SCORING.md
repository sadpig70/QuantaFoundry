# Discover Round 1 — Scoring & Seal Schema

## 채점 (수거 후)
1. **수렴**: ≥2 런타임이 동일 u_hash 분해 제출 → cross-model 합의(key-free consensus).
2. **독립검증**: `second_oracle` 제1원리 numpy 재구성 → u_hash 일치(분해≠검증 분리).
3. **proof**: sympy 로 permutation(cNx) 또는 phase(crK) golden 대수 증명.
4. **자원**: 동일 u_hash 다분해 시 ExploitAxis(W2.2) 최소비용 선택.

## 봉인 (key-free)
- 통과 분해를 `specs/modules/<gap_id>.pg` 로 작성 → `verify_seal.py` → `registry/modules`.
- 봉인 후 자동: distinct-prime cmul 확장이 buildable 로 전환(ValueFunction fan-in 재계산).
- standing-loop 승격: 이 라운드가 성공하면 frontier 자동전진(c7x→c8x, cr8→cr9 …).

## relay (정욱님)
- 6런타임 배포 → 응답 수거 → `_workspace/crossmodel/discover_round1/responses/` 적재.
- self-contained 부분(GAP-SPEC·TASKSPEC·SCORING)은 완성. **EXT 의존**: 실 런타임 응답 대기.
