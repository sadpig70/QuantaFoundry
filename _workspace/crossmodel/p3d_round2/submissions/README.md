# submissions (P3d round 2)

정욱님이 6 distinct-weights 런타임에서 수거한 `<runtime>.submission.json` 을 여기 둡니다.
그다음: `python scripts/cross_runtime_round.py`

채점기는 6 실런타임을 weights_id(=독립단위)로 풀링해 establish_truth 를 돌리고:
 - cnot_std(sanity): GT 수렴 확인(convention 정렬 calibration)
 - cnot_lower(probe): 진짜 독립 동반오류 측정 — 다수가 *틀린* 표준 CNOT 으로 수렴하면
   ESTABLISHED-wrong = corpus-상관 BREAK. ρ-할인이 그것을 방어하는지도 시연.
결과: `.pgf/bounty/P3D-ROUND2.json` (비파괴).
