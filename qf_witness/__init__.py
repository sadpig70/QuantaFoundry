# -*- coding: utf-8 -*-
"""qf_witness — 검증 로직 본체 패키지 (scripts/ 재구조화, final_scripts_refactoring_plan).

구조: core(경로 상수)·observe·family·verify·frontier·seal·registry·export·ops.
scripts/ 의 각 파일은 이 패키지 본체로 위임하는 shim 으로 잔존(기존 명령 영구 호환, INV-SR1).

★bootstrap: import 시 전 카테고리 디렉토리를 sys.path 에 **append**(stdlib 우선 유지)한다.
  근거: 본체 55개가 동료 스크립트를 flat import(`import genskills` 등) — 카테고리 분산 후에도
  import 문을 무수정(INV-SR2)으로 유지하기 위한 단일 장치. 기존 scripts/ 가 통째로
  sys.path 에 있던 것과 동등한 해석 공간이며 결정론에 영향 없다.
"""
import os as _os
import sys as _sys

_PKG = _os.path.dirname(_os.path.abspath(__file__))
ROOT = _os.path.dirname(_PKG)

CATEGORIES = ("core", "observe", "family", "verify", "frontier",
              "seal", "registry", "export", "ops")

for _cat in CATEGORIES:
    _p = _os.path.join(_PKG, _cat)
    if _os.path.isdir(_p) and _p not in _sys.path:
        _sys.path.append(_p)
