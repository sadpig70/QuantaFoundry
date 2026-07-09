# -*- coding: utf-8 -*-
"""qf_verify — manifest-driven verification runner (TrackReproduceUpgrade).

reproduce_all.py 의 검증 오케스트레이션을 구조화한다:
  검증 정의 = verification/manifests/*.json (스텝 추가에 코드 수정 불요)
  실행       = qf_verify.runner (순차 고정 — 결정론 재현 우선, INV-RA5)
  결과       = reports/REPRODUCE-RESULT.json (기존 형식 유지, INV-RA2)
               + reports/EVIDENCE-REPORT.json (가산)
  claim 연결 = verification/claims.json → reports/CLAIM-EVIDENCE-MAP.md

불변 (확정 플랜 _workspace/reproduce_all_upgrade_plan.md):
  INV-RA1 기존 명령 불변 · INV-RA2 REPRODUCE-RESULT 유지 · INV-RA3 판정 의미 동치
  INV-RA4 신규 pip 의존성 0 · INV-RA5 순차 실행 · INV-RA6 registry/oracle 무접촉
  INV-RA7 전환 게이트 = 신구 diff 의미 동치
"""
__version__ = "1.0"
