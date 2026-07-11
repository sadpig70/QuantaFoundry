# DESIGN-QF0711-P3 — ProductSurface (read-only 소비 인터페이스)

> QF-0711 마지막 노드. 제어면(P0 단일출처·P1 sidecar/gate·P2 릴리스 root)이 정합된 신뢰면을
> **외부 검토자가 read-only로 질의**하는 얇은 CLI. **신규 검증로직 0** — 전부 생성 아티팩트 조회·포맷.

## 진단·제약

- **엔진 불변**: 봉인/오라클/frozen/fingerprint/root 무접촉. seal/verify/compose 로직 미추가.
- **단일 진입점 재사용**: 기존 `qf_witness/ops/qf_cli.py`(이미 verify/compose/reproduce/export/ingest/
  discover/explain 보유)에 **가산**. 신규 파일 최소화(별도 모듈 1 + CLI 배선).
- **데이터 소스**(전부 P0~P2 생성물, read-only):
  - `registry/SEMANTIC-GUARANTEES.json` — `guarantees[key]`{tier,semantic_guarantee,method,u_hash} +
    `guarantee_classes` 카탈로그(honest_boundary·coverage_domain·seal_tier)
  - `registry/VERIFICATION-COVERAGE.json` — `by_app[id]`=보조검증경로 리스트, `paths` 카탈로그
  - `verification/claims.json` — 12 claim{title,guarantee_class,boundary,evidence_steps,authoritative_files}
  - `.pgf/DESIGN-MasterRoadmap.md` — 로드맵 Gantree(트랙·상태)
- **기존 `explain` 과 구분**: explain=구조 의존(deps/blast/resource). P3 inspect=검증상태(등급/경로/경계).
  claims=주장↔증거. plan=로드맵. 상호보완, 충돌 없음.

## Gantree

```text
P3_ProductSurface // read-only 소비 CLI (in-progress) @v:1.0 @dep:P1_EvidenceAutomation
    ProductSurfaceModule // qf_witness/ops/product_surface.py — 조회·포맷 순수함수 (in-progress)
        # input: SEMANTIC-GUARANTEES/VERIFICATION-COVERAGE/claims.json/MasterRoadmap (read-only)
        # process: load → lookup/filter → 사람가독 텍스트. 신규 검증 0.
        InspectFn // inspect(asset_id) → 등급·method·honest_boundary·coverage 경로·tier (in-progress)
            # by_kind 우선순위: app:id → module:id. class→GUARANTEE_CLASSES.honest_boundary.
            # coverage=by_app[id] 보조경로(없으면 primary-seal-only 명시). criteria: 미존재 자산=명확 에러.
        ClaimsFn // claims(id=None) → 12 claim 목록 또는 단건: title·class·boundary·evidence cmd·files (in-progress)
            # evidence_steps→'python scripts/reproduce_all.py --changed-only'(해당 step) 안내. criteria: 12건 전수.
        PlanFn // plan(query=None) → MasterRoadmap 트랙·상태 요약 또는 substring 필터 노드 (in-progress)
            # 파싱: '(status)' 정규식 추출. query 없으면 최상위 트랙+집계, 있으면 매칭 노드. criteria: read-only.
    CliWiring // qf_cli.py 에 inspect/claims/plan 서브커맨드 3개 배선 + USAGE 갱신 (in-progress) @dep:ProductSurfaceModule
        # dispatch 추가·기존 커맨드 불변. criteria: qf inspect rs73_encoder → unitary_equiv+affine 경로 출력.
    Verify // 3-스모크: inspect(rs73/모듈/미존재)·claims(전수·단건)·plan(전수·필터) (needs-verify) @dep:CliWiring
        # criteria: 전 서브커맨드 rc=0·핵심필드 출력·미존재 자산 rc≠0. root/봉인 무변경 재확인(git status).
```

## 비검증 정직성 (README/USAGE 반영)

- 이 CLI 는 **검증을 수행하지 않는다** — 이미 봉인·재현된 사실을 **조회·표시**만. 신뢰의 근거는
  여전히 `reproduce_all`(결정론) + oracle 독립검증(정확성). inspect 출력의 honest_boundary 는
  GUARANTEE_CLASSES 카탈로그의 정직 경계를 그대로 노출(과대표시 방지).
- root/second_oracle/frozen 무접촉 — reproduce 게이트 불필요(코드 read-only), 단 스모크로 회귀 확인.

## DoD

- `qf inspect <id>` / `qf claims [id]` / `qf plan [query]` 3커맨드 동작·기존 7커맨드 불변.
- product_surface.py 순수 조회(신규 검증 0)·root 0a6fbab0 불변·git 봉인파일 무변경.
- Verify 스모크 통과 후 커밋. P3 done → **QF-0711 트랙 전체 폐합**.
