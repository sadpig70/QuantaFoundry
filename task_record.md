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

- **2026-07-01 · W12.1~W12.24까지 반영** · **77 모듈 · 166 앱** · root `a0b4f67862a265ce…`(full=REGISTRY-MANIFEST.json) · second_oracle **71/71** · fingerprint **304/304 intact**
- 외부 3종(README · EXTERNAL-ONBOARDING · Technical-Spec) 전부 최신(85cdc459→a0b4f678·152→166·structural 7→9 반영, stale 검증 완료). README는 lean 재구성(507→83줄, 상세=docs/ARCHITECTURE.md). CITATION.cff·RELEASE-META.json·SEMANTIC-GUARANTEES.json 자동재생성.
- guarantee split: app **156 unitary_equiv + 1 sampled + 9 structural**(file-split 217 ue + 1 sampled + 9 structural = 227 app-files) · structural apps 9: shor69/77/91/119/221/381/635/1285/3683.
- 반영 서사 추가분: **W12.24 FrontierFactory + qfa-loop 스킬화**. 파라메트릭 봉인 폐루프(`scripts/frontier_factory.py`, INV-F1 회귀게이트)가 자율 발견한 N=69·77을 factory-sealed(신규 모듈 0). 자율 루프는 `.agents/skills/qfa-loop` 스킬로 자족화(`_workspace/loop` 폐기). root `85cdc459→a0b4f678`, apps `152→166`. (c13x는 2^14 dense 메모리 한계로 primitive-missing 자동 skip.)
- ★주의(다음 동기화 시): README/Technical-Spec의 **guarantee-split 단락**과 **검증 명령 기대출력(second_oracle·fingerprint·root prefix)**, **§8.5 current totals**, **§1 summary 헤드**, **§8.x file-count(213 files)**는 헤드라인과 별도로 갱신 누락되기 쉬움. abstract의 "What changed since vX"·milestone 리스트(77/147 at W12.21 등)는 **버전별 historical 기록이라 보존**(현재값으로 덮지 않음).

---

## 누적 작업 (다음 동기화 시 외부 3종에 반영 후 이 섹션 초기화)

현재 누적 없음. (2026-07-01 W12.24 + qfa-loop 스킬화 일괄 동기화 완료 → 위 "마지막 동기화 시점" 참조.)
