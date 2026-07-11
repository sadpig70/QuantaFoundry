# DESIGN — QF-0711-Upgrade / P1 EvidenceAutomation

> **모드**: PGF full-cycle (JIT, P0 폐합 후). **상위**: `_workspace/0711-upgrade-plan.md` · MasterRoadmap
> `TrackQF0711Upgrade/P1_EvidenceAutomation`. **범위**: P1 4노드 원자화. root 불변(sidecar/doc/gate).
> **작성**: 2026-07-11.

## 0. 실측 근거 (이미 존재하는 것 — 범위 축소)

```text
U7: ★80% 기구축 — verification/claims.json(11 claims: root/apps/frontier/second_oracle/convention/
    subspace/column_exact/epsilon/resource/behavior/observations) + qf_verify/claims.py(load/status/
    explain/write_claim_map) + cli.py write-claim-map + reports/CLAIM-EVIDENCE-MAP.md(생성물 존재).
    미완=reproduce 미배선(runner 가 write_claim_map 안 부름)·docs/EVIDENCE-MAP.md "planned" 문구 잔존.
U8: 경로별 census sidecar 존재 — .pgf/proofs/{ANF,GROEBNER,MATCHGATE,QMDD,STABRANK,TNCONTRACT}-VERIFY.json
    (+ *.column_proof/*.subspace_proof/*.cuc_proof·RING-COLUMN). 각 verified{}/skipped{reason}. 집계기만 신규.
U9: seal_gate_ci.py = root anchor(EXPECT_DEFAULT="0a6fbab0", root.startswith)·badge. doc_counts --check·
    structure_lint doc_paths 는 이미 witness batch(reproduce)에 有 — seal_gate_ci(CI badge 경로)엔 없음.
U10: DESIGN-MasterRoadmap.md 762줄 · done 144 · active/blocked 24 (85% done) → 아카이빙 시의적절.
비파괴: root 0a6fbab0 불변(전부 sidecar/doc/gate). oracle·seal 무수정.
```

## 1. Gantree (원자 분해)

```text
P1_EvidenceAutomation // 감사 자동화 (sidecar/doc, root 불변) (designing)
    U10_RoadmapArchive // 로드맵 압축 (독립·시의적절, 먼저) #C7
        U10a_HistorySplit // done 트랙 → DESIGN-MasterRoadmap-HISTORY.md(append-only) (atomic)
        U10b_ActiveOnly // 척추엔 active/blocked + 최근 done 요약 1줄만 (atomic)
        U10c_RoadmapLint // roadmap-lint: stale path·done-parent/active-child·노드>10 경고 (atomic)
    U7_ClaimManifestRunner // 기존 claims 인프라 배선·정합 (대부분 기구축) #C2
        U7a_ClaimDriftCheck // claims.py --check(생성물==claims.json 재생성 정합) (atomic)
        U7b_WireReproduce // reproduce/DoD 에 write_claim_map + --check drift gate 등록 (atomic)
        U7c_EvidenceMapReconcile // docs/EVIDENCE-MAP.md "planned"→"done", reports/CLAIM-EVIDENCE-MAP 링크·역할분리 (atomic)
        U7d_ClaimCoverageAudit // 11 claim 이 EVIDENCE-MAP 12행·주요 등급을 커버하는지 감사(누락 시 추가) (atomic)
    U8_VerificationCoverage // app×path 커버리지 매트릭스 #C8
        U8a_CoverageAggregator // qf_witness/registry/coverage.py: 경로 sidecar 합성→registry/VERIFICATION-COVERAGE.json (atomic)
        U8b_SinglePathReport // ★단일경로(dense만) 커버 자산 목록 산출(다음 검증투자 데이터) (atomic)
        U8c_PathsDoc // docs/VERIFICATION-PATHS.md: 10경로 단일표(name·covers·command·boundary·introduced_in) (atomic)
    U9_DriftGate // 드리프트 상시차단 (U1/U3 통합) #C1 #C5
        U9a_SealGateDrift // seal_gate_ci 에 doc_counts --check + structure_lint doc_paths 스텝 추가 (atomic)
        U9b_CoverageDriftCheck // VERIFICATION-COVERAGE.json --check(경로 sidecar 신선도) witness 등록 (atomic)
```

## 2. PPR (노드별)

### U10 · RoadmapArchive (먼저 — 독립·저위험)
```python
# U10a: HANDOFF-HISTORY 규약. done 트랙 서브트리 → .pgf/DESIGN-MasterRoadmap-HISTORY.md(append-only).
#   척추엔 트랙 헤더 1줄(done — 날짜·commit·root) + 상세는 HISTORY.
# U10b: 활성 트리 = ready/in-progress/blocked + P1 같은 진행중 상세. done 144→요약.
# U10c: roadmap-lint(qf_witness/ops 또는 structure_lint 확장): (i) 척추가 참조하는 repo 경로 존재,
#   (ii) done-parent 밑 active-child 불일치 경고, (iii) 트랙 노드>10 → 하위분할 권고(F9). witness 등록 선택.
# acceptance: 척추 가독성 회복(762→~250줄 목표)·done 상세 보존(HISTORY)·규율 판정대상 축소.
# gate: 로드맵 노드 참조 경로 실존·HISTORY append-only·root 무관.
```

### U7 · ClaimManifestRunner (배선·정합)
```python
# U7a: qf_verify claims.py 에 --check(write_claim_map 재생성 == reports/CLAIM-EVIDENCE-MAP.md 정합) 추가.
# U7b: reproduce DoD(또는 runner 후처리·witness contains 스텝)에 write_claim_map + --check drift 등록.
#   ★주의: reproduce 중 write 는 CLAIM-EVIDENCE-MAP.md 갱신(휘발 아님·결정론이면 안정). --check 로 gate.
# U7c: docs/EVIDENCE-MAP.md 상단 "manually maintained v0 · machine-gen planned" → "생성물=reports/
#   CLAIM-EVIDENCE-MAP.md(claims.json 기반), 이 파일=사람 요약". 역할분리 명시(U5 CURRENT-SPEC 패턴).
# U7d: 11 claim vs EVIDENCE-MAP 12행 매핑 감사. 누락 claim(예: ring-exact companion·compositionally 별행) 추가.
# acceptance: 모든 public claim=claims.json 1항목·evidence_steps·boundary. 생성물 idempotent·수동표 드리프트 제거.
# gate: claims.py --check all_ok · CLAIM-EVIDENCE-MAP 재생성 안정 · reproduce REPRODUCED.
```

### U8 · VerificationCoverage (신규 집계 sidecar)
```python
# U8a: coverage.py — .pgf/proofs/*-VERIFY.json + *.{column,subspace,cuc}_proof.json + RING-COLUMN 읽어
#   app_id → {path: covered|skipped(reason)} 매트릭스 → registry/VERIFICATION-COVERAGE.json.
#   경로 목록 = second_oracle(dense)·tableau·zx·column·ring·subspace·cuc·anf·groebner·matchgate·
#   tncontract·stabrank·qmdd·pathsum (EVIDENCE-MAP row11 "10 paths" 의 실체 = O-2 목록).
# U8b: 파생 = 각 자산 커버 경로 수 · ★단일경로(dense C4만) 자산 목록(제11경로 투자 우선순위 데이터).
# U8c: docs/VERIFICATION-PATHS.md — 경로 단일표. README "10 verification paths" 를 이 파일로 역추적 연결.
# acceptance: "10 paths" 주장이 데이터로 역추적 · 중첩분포 정량공시 · root 불변 sidecar.
# gate: coverage.py idempotent · 경로수==README 주장 · witness --check 등록.
```

### U9 · DriftGate (U1/U3 통합·CI화)
```python
# U9a: seal_gate_ci.py 에 스텝 추가 — doc_counts --check + structure_lint doc_paths(둘 다 이미 witness
#   batch 有, seal_gate_ci=CI badge 경로엔 없음). 불일치 시 gate FAIL(root anchor 옆에 doc-drift anchor).
# U9b: VERIFICATION-COVERAGE.json --check(경로 sidecar 신선도) witness 등록.
# acceptance: root 변경/파일이동/수치드리프트가 CI 게이트에서 자동 노출(현재는 reproduce 에서만).
# gate: 의도적 stale 주입 → seal_gate_ci FAIL.
```

## 3. WORKPLAN / POLICY

```text
순서: U10(독립·저위험, 먼저) → U7(claims 배선, 8/8 합의) → U8(커버리지 sidecar) → U9(드리프트 CI 통합).
  근거: U9 는 U8 산출물(COVERAGE)을 게이트에 넣으므로 U8 후. U7/U8 는 독립. U10 은 언제든.
POLICY:
  non_destructive: 검증로직·oracle·seal 무수정. sidecar/doc/gate 만. root 0a6fbab0 불변.
  determinism:     생성물(CLAIM-EVIDENCE-MAP·COVERAGE)은 결정론 재생성·--check idempotent.
  gate_per_node:   해당 --check all_ok · reproduce REPRODUCED · root 불변 · second_oracle 83/83.
  라운드 커밋:      U10 → U7 → U8 → U9. 각 후 게이트.
```

## 4. 정직 경계 (이 설계)

- U7 은 신규구축이 아니라 **기구축 인프라 배선·정합**(claims.json/claims.py 존재). 과대범위 방지.
- U8 "10 paths" 목록은 EVIDENCE-MAP row11·메모리 O-2 추정목록 기반 — U8a 착수 시 실제 sidecar 존재로 **확정**(추정→실측).
- rp_all(_legacy)에도 write-claim-map 이 있었으나 미채택 — U7 은 Python qf_verify 경로로 단일화.
- 잔여(P2/P3): ReleaseRoot·rs73 Tier-2·QualityScorecard·qf inspect — P1 폐합 후 JIT.
```
