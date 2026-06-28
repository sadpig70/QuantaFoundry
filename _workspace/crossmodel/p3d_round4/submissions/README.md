# submissions (P3d round 4 — contested-definition)

정욱님이 6 distinct-weights 런타임에서 수거한 `<runtime>.submission.json` 을 여기 둡니다.
그다음: `python scripts/cross_runtime_round.py --round p3d_round4`

probe: qft2(스왑/부호 관례)·sqrt_swap(위상 branch)·rz_half(부호 관례)·x_gate sanity.
이번엔 DIVERGENT(분기→봉인 거부=necessity) 또는 CONTESTED(동률→contested guard) 또는
co-error(corpus-지배 관례 수렴) 가 나올 수 있음 — 각 경우가 다른 방어선을 실측.
GT=`_ground_truth.json`(운영자 전용, 미배포, 표준형). 결과: `.pgf/bounty/P3D-ROUND4.json`.
