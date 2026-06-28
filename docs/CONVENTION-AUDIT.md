# Convention Independence Audit (Stage 4 W4.1)

> second_oracle 의 독립성 경계 정직 판정. 분석전용 비파괴.

## 판정 매트릭스

| 차원 | 판정 | 근거 |
|---|---|---|
| 유니터리 구성 | **INDEPENDENT** | numpy 제1원리 (qualtran/spec-golden 미실행) — risk(d) 구성버그 차단 |
| endian convention | **SHARED ASSUMPTION** | embed big-endian 하드코딩; sealed 의존; endian-sensitive 10건 |
| 전역위상 | **SHARED ASSUMPTION** | vs+my 모두 전역위상 제거 (48/48) |
| atol(1e-7) | **SHARED ASSUMPTION** | 양 측정 동일 round (48/48) |
| canonical hash | **SHARED (부분독립 측정)** | vs↔my 판정일치 388/388; 구현분리·철학공유 |

## 갭 (검증 필요 — 과장 제거)

second_oracle 은 *유니터리 구성*을 독립화해 risk(d)[Qualtran 구성/canonicalization 버그]를 닫는다. 그러나 endian·전역위상·atol·hash canonicalization 은 verify_seal 과 **공유 가정**이다. 따라서 convention 단일문화(big-endian/atol/전역위상)에 *공통 버그*가 있으면 second_oracle 도 같이 통과한다 — 이 축은 미차단 단일실패점. 닫으려면 독립 convention(예: little-endian 재유도 + 교차대조) 또는 형식증명(consensus.proof_*)이 필요. 현재는 명시된 갭(검증 필요).

## 닫는 경로

- 독립 convention 재유도: little-endian 으로 재구성 후 big-endian 과 교차대조.
- 형식증명 축: `consensus.proof_*`(corpus 무관 독립축)로 PROOF_BACKED 보강.
- 본 감사는 risk(d) *구성버그* 차단은 유효함을 확인하고, *convention 버그* 축만 갭으로 남긴다.
