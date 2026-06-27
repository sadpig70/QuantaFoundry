# submissions (P3d)

정욱님이 6 distinct-weights 런타임에서 수거한 `<runtime>.submission.json` 을 이 디렉토리에 둡니다.
그다음 판정:

```
python scripts/bounty_adjudicate.py            # T2/T3 순수데이터 + T1 정적 스캔(안전 기본)
python scripts/bounty_adjudicate.py --exec-specs   # T1 spec 을 temp store 에서 실제 봉인(샌드박스)
```

제출이 없으면 adjudicator 는 selftest(엔진 결정론)만 돌리고 `relay_pending=True` 로 정직하게
BLOCKED 표기한다. 판정은 `.pgf/bounty/P3D-ADJUDICATION.json`. 비파괴(registry/specs/frozen 무변경).
