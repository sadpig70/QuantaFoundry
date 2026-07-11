# DESIGN — QF-0711-Upgrade / P0 TruthSurface

> **모드**: PGF full-cycle (design→plan→execute→verify). 본 문서 = DESIGN + WORKPLAN + POLICY.
> **상위**: `_workspace/0711-upgrade-plan.md` (전략) · MasterRoadmap `TrackQF0711Upgrade/P0_TruthSurface`.
> **범위**: P0 6노드만 원자화(execution-ready). P1~P3 = P0 폐합 후 JIT.
> **작성**: 2026-07-11 · Opus 4.8.

---

## 0. 확정 전제 (2026-07-11 실측 해소)

```text
A1  root = sha256(정렬된 module/app "id:u_hash")  [registry_tools.build_manifest L96–102]
    → SEMANTIC-GUARANTEES.json · consensus_keys.json 은 root 비입력.
    ∴ U1/U2/U5 의 이 파일 변경은 root 불변(sidecar). 기존 seal u_hash 도 무변경.
A2  rs73_encoder = 60 cnot + 8 x · total_t=0 = 순수 Clifford → Tier-2 tableau 성립 (P2/U12 용, P0 아님)
A3  qfa-loop commit-policy: 런타임(autonomy_loop GATES_CHANGED)이 changed 커밋 허용
    → 표/L67 이 truth, INV5 L76("only full") 이 stale → INV5 텍스트 정정 (U4)
비파괴 불변: oracle fingerprint 2파일 · frozen consensus 23키 · 기존 sealed byte-identical (INV1/2)
```

## 1. 실측 근거 (편집 대상 확정)

| 대상 | 실측 | 노드 |
|---|---|---|
| README:55 | `python scripts/qf_stdlib.py categories \| lookup gate/h \| attest gate/h` (broken pipe) | U6c |
| README:62 | `95 modules + 518 app entries` (518 무근거; 실제 app unitary_equiv=542) | U6a |
| README:64 | subspace row `shor1285/3683, rs73` (shor1285/3683 은 compositionally_verified 로 이동됨) + compositionally_verified 행 **부재** | U6b |
| SEMANTIC tier_legend | `TIER_GUARANTEE` 상수(L252) = tier 0~3 만. class 4종(sampled/subspace/column_exact/compositionally) 미등재 | U2a |
| headline 생성 | semantic_guarantee.py L253–326 (by_class/by_kind_class) | U1c/U2 |
| seal_gate_ci | anchor(EXPECT_DEFAULT) 패턴 기존재 → doc-drift 게이트 확장 지점 | U9(P1) 참고 |
| qfa-loop SKILL | L44 `_workspace/loop/`·L46/78 `scripts/frontier_factory.py`·L32/86 `scripts/autonomy_loop.py`·L89 rounds | U3a |

---

## 2. Gantree (원자 분해)

```text
P0_TruthSurface // 사실·계약 정합 (doc/sidecar, root 불변) (in-progress)
    [parallel-safe: U3, U4 는 상호·U1 무의존]
    U3_SkillPathFix // 스킬 경로 정합 (designing) #quickwin
        U3a_QfaLoopPaths // qfa-loop SKILL.md 4치환 (atomic)
        U3b_OraclePathNote // qpgf-oracle SKILL.md bundle-root 노트 (atomic)
        U3c_DocPathLint // structure_lint 에 doc-path 존재검사 추가 (atomic)
    U4_AutonomyContractFix // commit 계약 정합 (designing) #quickwin
        U4a_Inv5Fix // SKILL.md INV5 텍스트 {full,changed} 정정 (atomic)
        U4b_DescribeContract // autonomy_loop.py --describe-contract --json (atomic)
        U4c_TableReconcile // SKILL 표 == describe-contract 출력 확인 (atomic)
    U1_CountOntology // 수치 단일출처 (designing) @dep:없음
        U1a_OntologyJson // registry/COUNT-ONTOLOGY.json (5-튜플 용어정의) (atomic)
        U1b_GenMarkers // README/ARCH/Spec 수치블록 <!-- BEGIN generated:counts --> 마커 (atomic)
        U1c_CountGenerator // doc_counts 생성기(headline_split→마커 치환) (atomic)
    U6_ReadmeFix // README 정합 (designing) @dep:U1
        U6a_CountFix // L62 518→정본 (atomic)
        U6b_GradeTableFix // subspace row→rs73 + compositionally_verified 행 추가 (atomic)
        U6c_CliFix // L55 broken pipe→3 서브커맨드 (atomic)
        U6d_ReviewerPath // External Reviewer 경로 표 (atomic)
    U2_SemanticGuaranteeV2 // proof-carrying + fail-closed (designing) @dep:U1
        U2a_ClassCatalogue // TIER_GUARANTEE→class catalogue(7종·seal_tier⊥guarantee) (atomic)
        U2b_FailClosed // inferred(default-dense)→unclassified 기본값 (atomic)
        U2c_LegendGuard // class∉legend → semantic_guarantee fail (atomic)
    U5_DocCurrentHistorySplit // 현재↔이력 분리 (designing) @dep:U1
        U5a_Changelog // docs/CHANGELOG.md ← Technical-Spec "What changed" 체인 (atomic)
        U5b_CurrentSpec // docs/CURRENT-SPEC.md (manifest 생성 현재수치) (atomic)
        U5c_ArchTrim // ARCHITECTURE.md 불변component+snapshot@root 배너+Layout 현행화 (atomic)
        U5d_SpecHeader // Technical-Spec §1 truncation 재작성 + generated_from_root/as_of (atomic)
```

---

## 3. PPR (노드별 명세)

### U3 · SkillPathFix (quick-win)
```python
def u3a_qfa_loop_paths():
    """qfa-loop/SKILL.md 실측 stale 경로 4종 치환."""
    # process: _workspace/loop/ → .agents/skills/qfa-loop/.runtime/
    #          scripts/frontier_factory.py → qf_witness/frontier/frontier_factory.py
    #          scripts/autonomy_loop.py → .agents/skills/qfa-loop/scripts/autonomy_loop.py (전체경로)
    #          _workspace/loop/rounds/ → .runtime/rounds/
    # acceptance_criteria:
    #   - grep "scripts/frontier_factory|_workspace/loop|^scripts/autonomy_loop" SKILL.md == 0
    #   - 모든 잔여 scripts/ 참조는 reproduce_all 진입점뿐

def u3b_oracle_path_note():
    """qpgf-oracle/SKILL.md 상단에 '경로는 skill bundle root 기준' 노트."""
    # ★INV: qpgf-oracle 는 vendored oracle — 코드/fingerprint 무수정. SKILL.md(문서)만 편집 가능?
    #   확인: SKILL.md 가 fingerprint 대상인지. 대상이면 편집 금지 → 대신 상위 docs 에 주석.
    # acceptance_criteria: 경로 모호성 제거. oracle fingerprint 2파일 byte-identical 불변.

def u3c_doc_path_lint():
    """structure_lint 에 check_doc_paths 추가."""
    # process: SKILL.md·README·EVIDENCE-MAP 등이 참조하는 repo-내 경로(정규식 추출) 존재검사.
    #   위반=fail. witness batch 등록.
    # acceptance_criteria: 현 상태에서 all_ok=True(U3a/b 수정 후). 의도적 stale 주입 시 fail.
```

### U4 · AutonomyContractFix (quick-win)
```python
def u4a_inv5_fix():
    """SKILL.md INV5 L76 텍스트를 런타임과 일치(full+changed)."""
    # "only --gates full ... commits/pushes" → "--gates full 또는 changed (둘 다 byte-identical
    #  재합성 verified-commit); incremental/fast 는 commit 보류"
    # acceptance_criteria: INV5 == 표(L62–67) == 런타임 GATES_CHANGED 정책

def u4b_describe_contract():
    """autonomy_loop.py --describe-contract --json: commit-allowed gates·engine path·정책 출력."""
    # process: 정적 dict(GATES 매핑·엔진경로·INV) 를 JSON 출력하는 argparse 분기 추가(부작용 0).
    # acceptance_criteria: 출력 JSON 의 commit_allowed==["full","changed"], engine_path 실존

def u4c_table_reconcile():
    """SKILL 표를 describe-contract 출력에서 생성/검증."""
    # acceptance_criteria: 표 값 == --describe-contract 출력(수동 대조 또는 U9 게이트로 자동화)
```

### U1 · CountOntology
```python
def u1a_ontology_json():
    """registry/COUNT-ONTOLOGY.json — 용어 5-튜플 단일 정의."""
    # 정의: unique_apps=502(distinct id) · app_files=577(=502+75 cached re-seal) ·
    #   app_unitary_equiv=542 · modules=95. 각 항목 {entity,namespace,population,guarantee,count,source}.
    # source = REGISTRY-MANIFEST.json / SEMANTIC-GUARANTEES.headline_split (파생 경로 명시)
    # acceptance_criteria: 모든 공개 수치가 이 파일의 항목으로 역추적 가능

def u1b_gen_markers():
    """README/ARCH/Spec 수치 블록을 생성마커로 감쌈."""
    # <!-- BEGIN generated:counts src=COUNT-ONTOLOGY.json --> … <!-- END generated:counts -->
    # acceptance_criteria: 마커 내부만 생성기 관할, 외부 산문 불변

def u1c_count_generator():
    """qf_witness 에 doc_counts 생성기 — headline_split→마커 치환(anchor_sync 패턴 확장)."""
    # process: semantic_guarantee 재생성 시 함께 실행하거나 별도 -m 엔트리. idempotent.
    # acceptance_criteria: 재실행 시 diff 0(고정점). 마커 밖 텍스트 무변경
```

### U6 · ReadmeFix @dep:U1
```python
# U6a: L62 "518 app entries" → COUNT-ONTOLOGY 정본("95 modules + 502 unique apps; 577 app-file entries")
# U6b: L64 subspace row "shor1285/3683, rs73"→"rs73" + 신규 행
#      "| compositionally_verified | exhaustive modexp perm + ring-exact iQFT (n≥19) | shor1285/3683 |"
# U6c: L55 파이프 → 3줄(python scripts/qf_stdlib.py {categories|lookup gate/h|attest gate/h})
# U6d: 상단 "For external reviewers" 표(REVIEW-REQUEST·EVIDENCE-MAP·Spec §13)
# acceptance_criteria: README 등급표 == headline_split · CLI 예시 실행가능 · 진입점 3개 명령 보존
```

### U2 · SemanticGuaranteeV2 @dep:U1
```python
def u2a_class_catalogue():
    """TIER_GUARANTEE → semantic_guarantee class catalogue."""
    # 7 class 각각: {class_name, seal_tier(독립축), method_en, coverage_domain
    #   (full_unitary|sampled_columns|basis_subspace|composition|structure|observation),
    #   honest_boundary, introduced_in_track}. tier_legend 키를 class 명으로 확장.
    # acceptance_criteria: headline by_class 의 7 class 전부 legend 에 존재
def u2b_fail_closed():
    """메타 누락 기본값 inferred(default-dense) → 'unclassified'(headline 제외)."""
    # process: resolve_tier/default 로직 위치 확인 후 기본값 교체. unclassified 는 headline 카운트 제외.
    # acceptance_criteria: inferred(default-dense) 발생 0. 미분류는 별도 카운트로 가시화
def u2c_legend_guard():
    """semantic_guarantee.py 재생성 시 class∉legend → SystemExit(1)."""
    # acceptance_criteria: 신규 미등재 class 주입 시 fail
# gate(U2): 재생성 idempotent · root 0a6fbab0 불변(A1) · 기존 seal u_hash 무변경 · reproduce REPRODUCED
```

### U5 · DocCurrentHistorySplit @dep:U1
```python
# U5a docs/CHANGELOG.md: Technical-Spec 헤더 "What changed since vX"(~185줄) 이관(HANDOFF-HISTORY 규약)
# U5b docs/CURRENT-SPEC.md: manifest/headline 생성 현재수치·보증분포·실행 surface(U1 마커 재사용)
# U5c ARCHITECTURE.md: 불변 component/data-flow/trust-boundary 유지 + 상단 "snapshot @root <hash> as_of <date>"
#     배너 + Directory Layout 을 실제 트리(qf_witness/ 8카테고리 + scripts/ 3진입점)로 현행화
# U5d Technical-Spec §1: truncation(L213) 재작성(표 형식) + generated_from_root/as_of/spec_version 표시
# acceptance_criteria: 살아있는 문서에 generated_from_root 표시 · 본문 수치 == manifest · 진입 이력 통과비용 제거
```

---

## 4. WORKPLAN (실행 순서 + POLICY)

```text
실행 순서 (의존·위험 기준):
  1. U3 (a→b→c)   # quick-win, U1 무의존, 저위험 문자열 — 신뢰 빌드
  2. U4 (a→b→c)   # quick-win, 안전계약 봉합
  3. U1 (a→b→c)   # 온톨로지 — U6/U2/U5 의 전제
  4. U6 (a→b→c→d) # README, U1 소비
  5. U2 (a→b→c)   # 최고위험(생성 스키마) — 단독 게이트
  6. U5 (a→b→c→d) # 문서 대분리 — 마지막(비파괴, 대량 텍스트)
라운드 커밋: U3+U4(quick-win 배치) → U1+U6 → U2 → U5. 각 배치 후 게이트.
```

```text
POLICY:
  non_destructive: oracle fingerprint 2파일·frozen 23키·기존 sealed byte-identical 불변(매 게이트 확인)
  root_invariant:  root 0a6fbab0 불변(A1 근거 — P0 전체 sidecar/doc). 위반 시 즉시 중단(치명)
  gate_per_batch:  registry build root 대조 + structure_lint(+doc-path) all_ok + second_oracle 83/83
  gate_p0_close:   full reproduce REPRODUCED (background-buffering 인지: 추적 태스크로 완주 대기)
  max_verify_cycles: 2
  oracle_edit_guard: qpgf-oracle SKILL.md 가 fingerprint 대상이면 편집 금지 → 상위 docs 로 우회(U3b)
```

---

## 5. 검증 게이트 (P0 종료조건)

```text
Gate_Counts:     README/ARCH/Spec/CURRENT-SPEC/EVIDENCE-MAP 공개수치 == COUNT-ONTOLOGY 재생성값
Gate_FailClosed: SEMANTIC v2 에서 inferred(default-dense)==0 · class∉legend → fail 동작
Gate_Contract:   qfa-loop 표 == INV5 == autonomy_loop --describe-contract
Gate_Paths:      structure_lint doc-path all_ok (SKILL/docs 참조 경로 실존)
Gate_NonDestruct: fingerprint 2파일·frozen 23·기존 seal byte-identical · root 0a6fbab0 불변
Gate_Reproduce:  full reproduce REPRODUCED · second_oracle 83/83
```

## 6. 정직 경계 (이 설계)

- P0 는 **검증 로직 무수정** — 문서·메타데이터·생성기·lint 만. 봉인/root 불변.
- U2 fail-closed 전환은 **정책 강화**(fail-open→closed)이지 기존 등급 격하가 아니다. 기존 봉인의
  semantic_guarantee 값은 불변(재분류 아님, 누락-기본값만 변경).
- U3b/oracle_edit_guard: qpgf-oracle 는 vendored — SKILL.md 편집 가능여부를 fingerprint 대상성으로
  먼저 판정(착수 전 확인 태스크).
- 남은 미확인: U1c 생성기를 semantic_guarantee 에 통합할지 별도 -m 엔트리로 둘지 = U1 착수 시 결정.
```
