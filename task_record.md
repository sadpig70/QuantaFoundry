# task_record — 외부문서 동기화 델타 버퍼

> **목적**: 매 작업을 아래 "## 누적 작업"에 1항목씩 누적한다. 정욱님이 **"동기화"** 지시 시,
> 이 누적분을 외부소비 3종에 일괄 반영하고 이 파일의 "## 누적 작업"을 **초기화(비움)** + "## 마지막 동기화 시점" 갱신.
>
> **외부소비 3종 (batch 전용 — 매 작업 동기화하지 않음)**:
> `README.md` · `EXTERNAL-ONBOARDING.md` · `docs/QuantaFoundry-Technical-Spec.md`
>
> **별도 갱신(이 버퍼와 무관)**: `HANDOFF.md`(내부 세션 인계 정본, 매 작업 갱신) ·
> 자동생성물(`CITATION.cff`·`SEMANTIC-GUARANTEES.json`, `reproduce_all`/`citation_gen` 스크립트로 생성) ·
> `RELEASE-NOTES.md`(릴리스 태깅 시점에만).

---

## 마지막 동기화 시점

- **2026-07-01 · W12.1~W12.23까지 반영** · **77 모듈 · 152 앱** · root `85cdc459cf98fe1d1abfd863f11048434786662b9cabebf6d314e4ee6c8c26aa` · second_oracle **71/71** · fingerprint **290/290 intact**
- 외부 3종(README · EXTERNAL-ONBOARDING · Technical-Spec) 전부 최신(1134ea04→85cdc459·147→152·structural 6→7 반영, stale 검증 완료). CITATION.cff·RELEASE-META.json·SEMANTIC-GUARANTEES.json 자동재생성.
- guarantee split: app **144 unitary_equiv + 1 sampled + 7 structural**(file-split 205 ue + 1 sampled + 7 structural) · structural apps 7: shor91/119/221/381/635/1285/**shor3683**.
- 반영 서사 추가분: **AutonomyLoop MVP + W12.22/23 frontier**. W12.21까지 반영 후, AutonomyLoop 실러너(자율 루프)가 mock→실게이트 연결로 가동되어 **W12.22 C12xPayoffFamily**(`cmul{4,16,256,2925}_mod3683` Tier-0 exact)와 **W12.23 Shor3683StructuralFrontier**(`shor3683` Tier-1 structural 20q)를 자율 봉인·검증·푸쉬했다. root `1134ea04→85cdc459`, apps `147→152`. (c13x는 2^14 dense 4GB 메모리 한계로 미봉인 — 더 큰 메모리 세션 대기.)
- ★주의(다음 동기화 시): README/Technical-Spec의 **guarantee-split 단락**과 **검증 명령 기대출력(second_oracle·fingerprint·root prefix)**, **§8.5 current totals**, **§1 summary 헤드**, **§8.x file-count(213 files)**는 헤드라인과 별도로 갱신 누락되기 쉬움. abstract의 "What changed since vX"·milestone 리스트(77/147 at W12.21 등)는 **버전별 historical 기록이라 보존**(현재값으로 덮지 않음).

---

## 누적 작업 (다음 동기화 시 외부 3종에 반영 후 이 섹션 초기화)

- **2026-07-01 · W12.24 FrontierFactory 자율 폐루프 (factory-sealed N=69,77)**. 외부 3종 반영 델타:
  - **counts**: 77 모듈 · **152 → 166 앱** (순수 가산, 신규 모듈 0).
  - **root**: `85cdc459…` → `a0b4f67862a265ce…` (full=REGISTRY-MANIFEST.json).
  - **guarantee-split (apps)**: 144 ue + 1 sampled + 7 structural → **156 ue + 1 sampled + 9 structural**.
  - **structural apps 7→9**: +`shor69`(3×23, 15q)·+`shor77`(7×11, 15q). 목록=shor69/77/91/119/221/381/635/1285/3683.
  - **second_oracle 71/71 불변** · **fingerprint 290→304 intact** (신규 14 앱 봉인; 모듈 무변경).
  - **서사**: **W12.24 FrontierFactory** — c{11,12}x_payoff/shor{1285,3683} 템플릿을 N-파라미터 봉인 함수로 추출한 `scripts/frontier_factory.py`(자유 codegen 아님). **INV-F1 회귀게이트**(기존 7N 91~3683 byte-identical 재현) 통과 후에만 신규 N 봉인. autonomy_loop이 `next_unsealed_target`으로 미봉인 distinct-semiprime N을 자율 발견→cmul payoff Tier-0 EXACT + structural shor{N} Tier-1(n_sys≥15)을 봉인→reproduce REPRODUCED→커밋하는 폐루프. reproduce_all에 데이터-주도 factory-step(INV-F5). 자율 루프 self-improvement(2-tier verify incremental ~46s·EOL 유령 자동복원·main 직접 모드)도 동반.
  - ★주의: seal_gate_ci.py `EXPECT_DEFAULT` 앵커는 `a0b4f678`로 갱신. fingerprint intact count 290→304.
  - **README 처리(2026-07-01)**: 507줄→83줄 lean 재구성. 상세 architecture/components/trust/milestone narrative는 `docs/ARCHITECTURE.md`로 보존+링크. **README는 166/a0b4f678로 최신화 완료**. → **다음 batch 동기화는 EXTERNAL-ONBOARDING.md·Technical-Spec.md만**(아직 152, root 85cdc459) 166/a0b4f678/structural 9로 갱신하면 됨.
