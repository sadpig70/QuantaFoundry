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

- **2026-06-30 · W12.1~M4까지 반영** · **77 모듈 · 147 앱** · root `1134ea04099ea0c16d1681e5a425e4997a53184f1ab85325d4517152be7108db` · second_oracle **71/71** · fingerprint **285/285 intact**
- 외부 3종(README · EXTERNAL-ONBOARDING · Technical-Spec) 전부 최신(stale 검증 완료).
- 반영 서사: **W12 cross-runtime + C12x frontier + external bridge**. W12.1~W12.19는 query/oracle·quantum walk·Suzuki-4·ZNE·`c8x→c9x→c10x→c11x` structural Shor frontier를 반영했고, W12.20~W12.21은 no-seal memory review 후 `c12x` Tier-0 모듈과 exact payoff app `cmul2_mod3683`(`N=3683=29×127`, 13q, gates 1848, max_control 12)을 반영했다. M4는 외부 실행 없이 `EXT_W3_5_CIPilot`, `EXT_W4_2_PoisonPanel`, `EXT_W5_3_RuntimeKeys`, `EXT_SD_BackendEvidence`, `EXT_ServerLink`의 unblock map만 문서화했다.
- ★주의(다음 동기화 시): README/Technical-Spec의 **guarantee-split 단락**과 **검증 명령 기대출력(second_oracle·fingerprint)**, **§8.5 current totals**, **§1 summary 헤드**는 헤드라인과 별도로 갱신 누락되기 쉬움. abstract의 "What changed since vX" 항목은 **버전별 historical 기록이라 보존**(현재값으로 덮지 않음).

---

## 누적 작업 (다음 동기화 시 외부 3종에 반영 후 이 섹션 초기화)

현재 누적 없음.
