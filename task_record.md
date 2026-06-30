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

현재 누적 없음. (2026-07-01 AutonomyLoop MVP + W12.22/23 frontier 일괄 동기화 완료 → 위 "마지막 동기화 시점" 참조.)
