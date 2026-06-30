# Claude Code Handoff — QuantaFoundry

Date: 2026-06-30

정욱님 credit 한계로 현 시점에서 Claude Code로 인계한다.

## Read Order

1. `AGENTS.md`
2. `.agents/skills/pg/SKILL.md`
3. `.agents/skills/pgf/SKILL.md`
4. `.agents/skills/qpgf-oracle/SKILL.md`
5. `remain_task_list.md`
6. `HANDOFF.md`
7. `.pgf/external/POST-W12-EXT-BRIDGE.json`
8. `_workspace/loop/AUTONOMY-LOOP-HANDOFF.md` (장기 자율 실행 진입점 — AutonomyLoop)

## Current Point

- Registry: 77 modules / 147 unique apps.
- Root: `1134ea04099ea0c16d1681e5a425e4997a53184f1ab85325d4517152be7108db`.
- Latest completed maintenance: `M2_DocSyncBatch`.
- External docs synchronized through W12.1~M4:
  - `README.md`
  - `EXTERNAL-ONBOARDING.md`
  - `docs/QuantaFoundry-Technical-Spec.md`
- `task_record.md` cumulative section is reset to `현재 누적 없음`.
- M2 evidence:
  - `.pgf/REVIEW-DocSyncBatch.md`
  - `.pgf/maintenance/DOCSYNC-M2-REPORT.json`
  - `.pgf/status-DocSyncBatch.json`

## Last Verified

- `python scripts/reproduce_all.py` -> `REPRODUCED`, registry `77/147`, root prefix `1134ea04099ea0c1`, `second_oracle 71/71`
- `python scripts/backlog_compaction_audit.py` -> PASS, stale=0
- `python scripts/seal_gate_ci.py` -> PASS
- `python scripts/second_oracle.py` -> PASS, `71/71`
- JSON parse checks for M2 reports -> PASS
- `git diff --check` -> no whitespace errors; CRLF warnings only

## Next Recommended Work

Priority 1: `EXT_W3_5_CIPilot`

- Status: blocked.
- Blocker: no external repository/path and no CI edit permission yet.
- First action when unblocked: create repo-local CI pilot that runs `seal_gate_ci` or `reproduce_all` with explicit expected root prefix `1134ea04099ea0c1`.
- Acceptance:
  - target repo CI fails on root mismatch;
  - no external seal is trusted without local recomputation;
  - target repo CI config is scoped and does not become a seal authority.

Priority 1b (no external input needed): AutonomyLoop MVP

- Status: ready — frontier·EXT 무관 인프라 자율작업. 진입점 `_workspace/loop/AUTONOMY-LOOP-HANDOFF.md`.
- Location: `_workspace/loop/` — `DESIGN-AutonomyLoop.md`(Gantree+PPR+§8 정교화), `persona_contexts.md`, `sim_autonomy_loop_v2.py`(T1~T12)·`sim_persona_diversity.py`(D1~D5)·`sim_seal_cycle.py` ALL PASS.
- Action: connect mock seams (`run_seal_cycle`·`reproduce_all`·`doc_sync`·`commit`·`push`) to real scripts/git; run one real autonomous round.
- Guard: INV7 NoAutoFrontier blocks `c13x`/payoff/`shor3683` auto-start; commit/push only when verified (`reproduce_all` REPRODUCED); root invariant or additive-only.

## Autonomy Authorization (2026-06-30 정욱님 전면 승인 — 금지 삭제)

정욱님이 **자율 진행을 위해 모든 자율-제약(금지)을 삭제**하고 전면 승인했다. 자율 루프는 다음을
**스스로 판단해 진행**한다(별도 지시 불필요):

- frontier 확장(`c13x`·payoff family·`shor3683`·신규 수평클래스) 자율 착수.
- 커밋·푸쉬 자율 수행(verified-only — `reproduce_all` REPRODUCED 분만).
- 외부 3종 동기화 자율 수행(`task_record` delta 기준 SyncCheckpoint).
- 새 작업 방향 자율 선택.

## Trust Basis (제약 아님 — 자율 루프가 의존하는 신뢰 기반, 유지)

아래는 *금지가 아니라 시스템 존재조건*이라 유지한다(이것이 무너지면 자율 봉인 자체가 무의미):

- 오라클 fingerprint 2파일(`verify_seal.py`·`contracts.py`)은 자율 루프가 **사용만** 한다.
  수정 시 285개 봉인 전부가 무효화되므로 신뢰 기반으로 보존(수정할 이유도 없음).
- 결정론 byte-identical·frozen 23키는 자율 루프의 검증 잣대 그 자체 → 유지.
- 응답 한국어·정욱님 호칭·workspace-local `.agents/skills`.
