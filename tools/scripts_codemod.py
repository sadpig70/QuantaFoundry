#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scripts_codemod — ROOT 정의 치환 codemod (final_scripts_refactoring_plan §3.2, 결정론·재실행 안전).

qf_witness/<cat>/ 로 이동한 본체의 ROOT 계산(깊이 함정 §2-b)을 paths 정본으로 치환한다.
규칙 A (유일 규칙 — bootstrap 이 상호 import·oracle 경로를 흡수하므로 단일화):
  ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))      (133)
  ROOT = os.path.abspath(os.path.join(HERE, ".."))                        (25, HERE 정의는 유지)
  ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  (1)
    → from qf_witness.core.paths import ROOT
  ROOT = Path(__file__).resolve().parents[1]                              (1)
    → from qf_witness.core.paths import ROOT as _QF_ROOT / ROOT = Path(_QF_ROOT)
치환 불일치 파일은 건드리지 않고 보고(INV-SR6). ROOT 정의가 없는 파일(self-contained)은 무수정.

사용: python tools/scripts_codemod.py qf_witness   # 이동된 본체 전체에 적용
"""
import os
import re
import sys

ANCHORS = [
    "ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))",
    'ROOT = os.path.abspath(os.path.join(HERE, ".."))',
    'ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))',
]
REPLACEMENT = "from qf_witness.core.paths import ROOT"
PATHLIB_ANCHOR = "ROOT = Path(__file__).resolve().parents[1]"
PATHLIB_REPL = ("from qf_witness.core.paths import ROOT as _QF_ROOT\n"
                "ROOT = Path(_QF_ROOT)")


def process(path):
    txt = open(path, encoding="utf-8").read()
    orig = txt
    hit = None
    for a in ANCHORS:
        if a in txt:
            txt = txt.replace(a, REPLACEMENT, 1)
            hit = "std"
            break
    if hit is None and PATHLIB_ANCHOR in txt:
        txt = txt.replace(PATHLIB_ANCHOR, PATHLIB_REPL, 1)
        hit = "pathlib"
    if hit is None:
        if re.search(r"^ROOT\s*=", txt, re.M):
            return "MISMATCH"                      # 미지 변형 — 수동 처리 대상
        return "NOROOT"                            # self-contained — 무수정
    if txt != orig:
        open(path, "w", encoding="utf-8", newline="\n").write(txt)
    return hit


def audit(base):
    """치환 후 잔여 위험 패턴 감사 — 깊이 함정이 남아있으면 실패."""
    bad = []
    for dp, _, fns in os.walk(base):
        for fn in fns:
            if not fn.endswith(".py") or fn == "paths.py":
                continue
            p = os.path.join(dp, fn)
            t = open(p, encoding="utf-8").read()
            if re.search(r"ROOT\s*=\s*os\.path\.dirname\(os\.path\.dirname", t) or \
               re.search(r'ROOT\s*=\s*os\.path\.abspath\(os\.path\.join\(HERE,\s*"\.\."\)\)', t):
                bad.append(p)
    return bad


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "qf_witness"
    stats = {}
    mismatches = []
    for dp, _, fns in os.walk(base):
        for fn in sorted(fns):
            if not fn.endswith(".py") or fn in ("__init__.py", "paths.py"):
                continue
            r = process(os.path.join(dp, fn))
            stats[r] = stats.get(r, 0) + 1
            if r == "MISMATCH":
                mismatches.append(os.path.join(dp, fn))
    bad = audit(base)
    print(f"codemod: {stats}")
    if mismatches:
        print("MISMATCH (수동 처리 필요):")
        for m in mismatches:
            print("  ", m)
    print(f"depth-trap audit: {'CLEAN' if not bad else 'RESIDUAL ' + str(bad)}")
    return 0 if (not mismatches and not bad) else 1


if __name__ == "__main__":
    sys.exit(main())
