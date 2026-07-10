#!/usr/bin/env python3
# shim — 본체: qf_witness/observe/h2_molecule_observe.py (scripts 재구조화 2026-07, 기존 명령 영구 호환)
import os, sys
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)
import qf_witness  # noqa: F401  (bootstrap: 카테고리 디렉토리 sys.path 등록)
if __name__ == "__main__":
    import runpy
    runpy.run_path(os.path.join(_ROOT, "qf_witness", "observe", "h2_molecule_observe.py"),
                   run_name="__main__")
else:
    # 동료 스크립트가 구경로로 `import h2_molecule_observe` 한 경우 — 본체 모듈로 자기 대체(완전 호환)
    import importlib
    sys.modules[__name__] = importlib.import_module("qf_witness.observe.h2_molecule_observe")
