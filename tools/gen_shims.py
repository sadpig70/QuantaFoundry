#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_shims — scripts/ 위임 shim 자동 생성 (final_scripts_refactoring_plan §3.3, 단일 템플릿).

runpy.run_path(run_name="__main__") 채택: argv·SystemExit·종료코드 완전 보존, main() 반환
규약 불문 — 189개 스크립트의 실행 의미가 그대로다. shim 은 영구 호환층(INV-SR1).

사용: python tools/gen_shims.py <name> [<name> ...]   # _move_map.json 기준 카테고리 자동
"""
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
MOVE_MAP = json.load(open(os.path.join(ROOT, "verification", "manifests", "_move_map.json"),
                          encoding="utf-8"))["map"]

TEMPLATE = '''#!/usr/bin/env python3
# shim — 본체: qf_witness/{cat}/{name}.py (scripts 재구조화 2026-07, 기존 명령 영구 호환)
import os, runpy, sys
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)
import qf_witness  # noqa: F401  (bootstrap: 카테고리 디렉토리 sys.path 등록)
runpy.run_path(os.path.join(_ROOT, "qf_witness", "{cat}", "{name}.py"), run_name="__main__")
'''


def write_shim(name):
    cat = MOVE_MAP[name]
    body = os.path.join(ROOT, "qf_witness", cat, f"{name}.py")
    assert os.path.exists(body), f"body missing: {body}"
    shim = os.path.join(ROOT, "scripts", f"{name}.py")
    open(shim, "w", encoding="utf-8", newline="\n").write(
        TEMPLATE.format(cat=cat, name=name))
    return shim


def main():
    names = sys.argv[1:]
    if not names:
        print("usage: gen_shims.py <name> [...]")
        return 2
    for n in names:
        print("shim →", os.path.relpath(write_shim(n), ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
