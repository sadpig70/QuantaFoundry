#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""structure_lint — scripts 재구조화 회귀 방지 상시 검사 (final_scripts_refactoring_plan P3).

검사 3종 (위반 = fail, reproduce witness batch 에 등록되어 상시 실행):
  (i)   scripts/ 의 .py 는 shim 템플릿(runpy 위임) 또는 허용 목록(thin 진입점)만 —
        플랫 구조 재발 차단. 신규 검증 스크립트는 qf_witness/<cat>/ 에 두고 shim 을 생성하라.
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

# thin 진입점 허용 목록 (shim 아님이 정당한 파일)
ALLOW_NON_SHIM = {"reproduce_all.py", "reproduce_all_legacy.py", "qf_stdlib.py"}
SHIM_MARK = "# shim — 본체: qf_witness/"

DEPTH_TRAPS = [
    re.compile(r"ROOT\s*=\s*os\.path\.dirname\(os\.path\.dirname"),
    re.compile(r'ROOT\s*=\s*os\.path\.abspath\(os\.path\.join\(HERE,\s*"\.\."\)\)'),
    re.compile(r"ROOT\s*=\s*Path\(__file__\)\.resolve\(\)\.parents\[1\]"),
]


def check_scripts_shim_only():
    bad = []
    for fn in sorted(os.listdir(SCRIPTS)):
        if not fn.endswith(".py") or fn in ALLOW_NON_SHIM:
            continue
        head = open(os.path.join(SCRIPTS, fn), encoding="utf-8").read(400)
        if SHIM_MARK not in head:
            bad.append(fn)
    return bad


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
        "scripts_shim_only": check_scripts_shim_only(),
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
