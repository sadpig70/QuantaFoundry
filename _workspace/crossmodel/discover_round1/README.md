# Discover Round 1 — Primitive Proposal Package

QF-Discover(Stage 2) W2.4 산출. ValueFunction(W2.1)이 자율 도출한 미봉인 primitive capability-gap 을 6런타임 패널에 위임하는 배포 패키지.

## 파일
- `GAP-SPEC.json` — capability-gap 명세(제약·golden·unlock 근거)
- `TASKSPEC.md` — 6런타임 PG TaskSpec(독립 제안 요청)
- `SCORING.md` — 수렴+독립검증+proof 채점 및 key-free 봉인 스키마
- `responses/` — (relay 후) 런타임 응답 적재 위치

## 상태
self-contained 부분 완성. **[EXT]** — 정욱님 6런타임 배포→수거 대기.
수거 후 `decomp_optimizer`(reward)+`second_oracle`(독립검증)으로 자동 채점→봉인.
