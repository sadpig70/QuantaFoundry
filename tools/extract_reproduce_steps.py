#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""extract_reproduce_steps — Phase0 Inventory (TrackReproduceUpgrade).

scripts/reproduce_all.py 의 모든 스텝 등록을 정적 추출해 inventory JSON 으로 저장한다.
manifest 이식의 단일 기준(1:1 대조용) — 의미 불변(INV-RA3) 검증의 출발점.

추출 대상 패턴:
  rc, out = run([...])  +  result["steps"]["<id>"] = {...}
판정식 분류:
  - witness  : pass = rc==0 and "all_ok=True" in out   (공통 다수 — witness_batch 후보)
  - contains : pass = rc==0 and "<str>" in out          (column_verify 'PASS' 등)
  - rc_only  : pass = rc==0 (+ regex 캡처)
  - special  : 코드 블록(forge/frontier 분기/behavior) — 수동 매핑

사용: python tools/extract_reproduce_steps.py
출력: verification/manifests/_inventory.json
"""
import os
import re
import json

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SRC = os.path.join(ROOT, "scripts", "reproduce_all.py")
OUT_DIR = os.path.join(ROOT, "verification", "manifests")


def main():
    txt = open(SRC, encoding="utf-8").read()
    steps = []

    # 표준 블록: rc, out = run([ ... ]) \n result["steps"]["ID"] = { ... }
    pat = re.compile(
        r'rc, out = run\(\[(?P<argv>[^\]]+)\]\)\s*\n'
        r'\s*result\["steps"\]\["(?P<id>[a-z0-9_]+)"\] = \{(?P<body>.*?)\}\n',
        re.S)
    for m in pat.finditer(txt):
        argv = [a.strip().strip('"\'') for a in m.group("argv").split(",")]
        body = m.group("body")
        entry = {"id": m.group("id"), "argv": argv}
        if '"all_ok=True" in out' in body:
            entry["kind"] = "witness"
            entry["expect"] = {"return_code": 0, "contains": ["all_ok=True"]}
        elif '"PASS" in out' in body:
            entry["kind"] = "contains"
            entry["expect"] = {"return_code": 0, "contains": ["PASS"]}
        else:
            entry["kind"] = "rc_only"
            entry["expect"] = {"return_code": 0}
            caps = re.findall(r're\.search\(r?"([^"]+)"', body)
            if caps:
                entry["regex_in_body"] = caps
        steps.append(entry)

    # 특수 블록(수동 매핑 — 코드 로직): forge_apps / frontier 분기 / registry / second_oracle / behavior
    frontier = re.search(r"FRONTIER_STEPS = \[(.*?)\]\n", txt, re.S).group(1)
    frontier_steps = re.findall(r'\("([a-z0-9_]+)", "([^"]+)"\)', frontier)
    special = {
        "forge_apps": {"kind": "special", "note": "regex 캡처(앱봉인/재발견) + changed-only 캡처(재조립/coherence)"},
        "frontier_block": {"kind": "special",
                           "note": "changed-only & frontier 무변경 → coherence sweep + factory --reproduce; "
                                   "그 외 → FRONTIER_STEPS 전량 + factory --reproduce",
                           "frontier_steps": [{"id": i, "script": s} for i, s in frontier_steps],
                           "factory": {"id": "frontier_factory", "script": "scripts/frontier_factory.py",
                                       "args": ["--reproduce"], "expect_contains": "all_ok=True"}},
        "registry": {"kind": "special", "note": "registry_tools build + regex 캡처(modules/apps/cached/root)"},
        "second_oracle": {"kind": "special", "note": "rc==0 판정 + 모듈 N/N 캡처"},
        "behavior": {"kind": "special", "note": "인라인 numpy — shor15_a2/a7 peak {0,2,4,6} + cmul2_mod21 orbit period 6"},
    }

    inv = {"_schema": "qf-reproduce-inventory/v0",
           "_note": "Phase0 자동 추출 — manifest 이식 1:1 대조 기준. 의미 불변(INV-RA3).",
           "source": "scripts/reproduce_all.py",
           "n_standard_steps": len(steps),
           "standard_steps": steps,
           "special_blocks": special}
    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, "_inventory.json")
    json.dump(inv, open(out_path, "w", encoding="utf-8", newline="\n"),
              ensure_ascii=False, indent=2)
    kinds = {}
    for s in steps:
        kinds[s["kind"]] = kinds.get(s["kind"], 0) + 1
    print(f"standard steps: {len(steps)} → {kinds}")
    print(f"frontier steps in block: {len(frontier_steps)}")
    print(f"→ {os.path.relpath(out_path, ROOT)}")


if __name__ == "__main__":
    main()
