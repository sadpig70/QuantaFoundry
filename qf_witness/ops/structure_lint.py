#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""structure_lint — scripts 재구조화 회귀 방지 상시 검사 (final_scripts_refactoring_plan P3).

검사 3종 (위반 = fail, reproduce witness batch 에 등록되어 상시 실행):
  (i)   scripts/ 의 .py 는 허용 목록(thin 진입점 3개)만 — 플랫 구조·shim 재발 차단.
        신규 검증 스크립트는 qf_witness/<cat>/ 에 두고 `python -m qf_witness.<cat>.<name>` 로 호출하라
        (C안 2026-07-11: shim 186 제거·내부호출 -m 전환 이후, scripts/ 는 진입점 전용).
  (ii)  qf_witness/ 본체에 ROOT 깊이 함정 패턴(dirname(dirname / join(HERE,"..")) 잔존 금지 —
        codemod 감사와 동일 규칙 (§2-b).
  (iii) qpgf-oracle 코드 사본 금지(INV-SR4) — qf_witness/ 에 oracle 모듈명 파일 존재 불가.

사용: python scripts/structure_lint.py [--quick]   (--quick 도 전수 — 검사 자체가 초 단위)
"""
import os
import re
import sys

from qf_witness.core.paths import ROOT, ORACLE_DIR

SCRIPTS = os.path.join(ROOT, "scripts")
WITNESS = os.path.join(ROOT, "qf_witness")

# thin 진입점 허용 목록 (scripts/ 에 정당하게 존재하는 유일한 .py 3개)
ALLOW_SCRIPTS = {"reproduce_all.py", "reproduce_all_legacy.py", "qf_stdlib.py"}

DEPTH_TRAPS = [
    re.compile(r"ROOT\s*=\s*os\.path\.dirname\(os\.path\.dirname"),
    re.compile(r'ROOT\s*=\s*os\.path\.abspath\(os\.path\.join\(HERE,\s*"\.\."\)\)'),
    re.compile(r"ROOT\s*=\s*Path\(__file__\)\.resolve\(\)\.parents\[1\]"),
]


def check_scripts_allowlist_only():
    # scripts/ 의 .py 는 허용 진입점 3개만 — 그 외(shim 포함) 전부 위반.
    return [fn for fn in sorted(os.listdir(SCRIPTS))
            if fn.endswith(".py") and fn not in ALLOW_SCRIPTS]


def check_no_depth_trap():
    bad = []
    for dp, _, fns in os.walk(WITNESS):
        for fn in fns:
            if not fn.endswith(".py") or fn == "paths.py":
                continue
            t = open(os.path.join(dp, fn), encoding="utf-8").read()
            if any(p.search(t) for p in DEPTH_TRAPS):
                bad.append(os.path.relpath(os.path.join(dp, fn), ROOT))
    return bad


def check_no_oracle_copy():
    oracle_mods = {fn for fn in os.listdir(ORACLE_DIR) if fn.endswith(".py")}
    bad = []
    for dp, _, fns in os.walk(WITNESS):
        for fn in fns:
            if fn in oracle_mods and fn != "__init__.py":
                bad.append(os.path.relpath(os.path.join(dp, fn), ROOT))
    return bad


def main():
    checks = {
        "scripts_allowlist_only": check_scripts_allowlist_only(),
        "no_depth_trap": check_no_depth_trap(),
        "no_oracle_copy": check_no_oracle_copy(),
    }
    ok = True
    for name, bad in checks.items():
        flag = "OK " if not bad else "FAIL"
        print(f"  [{flag}] {name}" + (f": {bad[:8]}" if bad else ""))
        ok &= not bad
    print(f"structure_lint: all_ok={ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
