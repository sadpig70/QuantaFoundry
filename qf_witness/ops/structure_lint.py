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

사용: python -m qf_witness.ops.structure_lint [--quick]   (--quick 도 전수 — 검사 자체가 초 단위)
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

# doc-path lint (QF-0711 U3c): 리팩토링(ScriptsRestructure/ShimCleanup)마다 반복된 서술문서의
# repo-경로 참조 파손을 상시 차단. '이사 위험 실재' 경로만 검사 = qf_witness/·qf_verify/ 또는
# full .agents/skills/<skill>/scripts/… (bare scripts/ 는 skill 내부 bundle-relative 라 모호→제외).
DOC_PATH_TARGETS = [
    "README.md", "docs/EVIDENCE-MAP.md", "docs/QuantaFoundry-Technical-Spec.md",
    "docs/ARCHITECTURE.md", ".agents/skills/qfa-loop/SKILL.md",
]
DOC_PATH_RE = re.compile(
    r'(?<![\w./-])((?:qf_witness|qf_verify)/[\w./-]+\.py|\.agents/skills/[\w-]+/scripts/[\w./-]+\.py)')


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


def check_doc_paths():
    bad = []
    for rel in DOC_PATH_TARGETS:
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            continue
        for m in DOC_PATH_RE.finditer(open(p, encoding="utf-8").read()):
            if not os.path.exists(os.path.join(ROOT, m.group(1))):
                bad.append(f"{rel}→{m.group(1)}")
    return bad


def check_roadmap_archive():
    # QF-0711 U10c: 척추(MasterRoadmap)의 done-트랙 상세는 HISTORY 로 이관. 분할 무결성 검사 —
    # HISTORY 파일 존재 + 척추가 그것을 참조(아카이브 규약). 둘 중 하나라도 없으면 위반.
    rm = os.path.join(ROOT, ".pgf", "DESIGN-MasterRoadmap.md")
    hist = os.path.join(ROOT, ".pgf", "DESIGN-MasterRoadmap-HISTORY.md")
    bad = []
    if not os.path.exists(hist):
        bad.append("DESIGN-MasterRoadmap-HISTORY.md 부재")
    elif os.path.exists(rm) and "DESIGN-MasterRoadmap-HISTORY.md" not in open(rm, encoding="utf-8").read():
        bad.append("척추가 HISTORY 미참조(아카이브 규약 누락)")
    return bad


def main():
    checks = {
        "scripts_allowlist_only": check_scripts_allowlist_only(),
        "no_depth_trap": check_no_depth_trap(),
        "no_oracle_copy": check_no_oracle_copy(),
        "doc_paths": check_doc_paths(),
        "roadmap_archive": check_roadmap_archive(),
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
