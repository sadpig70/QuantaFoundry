# -*- coding: utf-8 -*-
"""
backlog_compaction_audit.py - M3 BacklogCompactionAudit.

Audit HANDOFF/remain/task_record size and current-state drift. This is a
report-only maintenance gate; it does not change registry state.
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, ".pgf", "maintenance")
TARGETS = ["HANDOFF.md", "remain_task_list.md", "task_record.md"]
LINE_BUDGETS = {
    "HANDOFF.md": 140,
    "remain_task_list.md": 270,
    "task_record.md": 120,
}
STALE_PATTERNS = [
    r"73 modules / 130",
    r"second_oracle 67/67",
    r"0945ed9e",
    r"75 modules / 136 unique apps",
    r"216169028a05a840",
    r"W12_14_C10xPrimitiveFrontier // .* \(ready\)",
    r"W12\.14 .*`\[ready\]`",
    r"W12_15_Shor635StructuralFrontier // .* \(ready\)",
    r"W12\.15 .*`\[ready\]`",
    r"W12_16_C11xPrimitiveReview // .* \(ready\)",
    r"W12\.16 .*`\[ready\]`",
    r"09f62bf3f5584619",
    r"W12_17_C11xPrimitiveFrontier // .* \(ready\)",
    r"W12\.17 .*`\[ready\]`",
    r"76 modules / 142",
    r"138acc5a4d720de1",
    r"W12_18_C11xPayoffFamily // .* \(ready\)",
    r"W12\.18 .*`\[ready\]`",
    r"W12_19_Shor1285StructuralFrontier // .* \(ready\)",
    r"W12\.19 .*`\[ready\]`",
    r"W12_20_C12xPrimitiveReview // .* \(ready\)",
    r"W12\.20 .*`\[ready\]`",
    r"W12_21_C12xPrimitiveFrontier // .* \(ready\)",
    r"W12\.21 .*`\[ready\]`",
    r"M4_PostW12ExternalBridgeDesign // .* \(ready\)",
    r"M4 .*`\[ready\]`",
]


def line_count(path: str) -> int:
    with open(path, encoding="utf-8") as f:
        return sum(1 for _ in f)


def find_patterns(path: str, patterns: list[str]) -> list[dict]:
    txt = open(path, encoding="utf-8").read()
    hits = []
    for pat in patterns:
        for m in re.finditer(pat, txt):
            line = txt.count("\n", 0, m.start()) + 1
            hits.append({"pattern": pat, "line": line})
    return hits


def main() -> int:
    os.makedirs(OUT_DIR, exist_ok=True)
    manifest = json.load(open(os.path.join(ROOT, "registry", "REGISTRY-MANIFEST.json"), encoding="utf-8"))
    root = manifest["registry_root_hash"]
    current_markers = [
        root,
        f"{manifest['modules']['count']} modules / {manifest['apps']['unique_app_count']} unique apps",
    ]
    files = {}
    ok = True
    for rel in TARGETS:
        path = os.path.join(ROOT, rel)
        lines = line_count(path)
        budget = LINE_BUDGETS[rel]
        stale_hits = find_patterns(path, STALE_PATTERNS)
        marker_hits = {marker: (marker in open(path, encoding="utf-8").read()) for marker in current_markers}
        # task_record is cumulative history, so old roots may appear as history; do not fail it for stale historical text.
        if rel == "task_record.md":
            stale_hits = [
                h for h in stale_hits
                if h["pattern"].startswith("W12_14") or h["pattern"].startswith("W12_15")
                or h["pattern"].startswith("W12_16") or h["pattern"].startswith("W12_17")
                or h["pattern"].startswith("W12_18") or h["pattern"].startswith("W12_19")
                or h["pattern"].startswith("W12_20") or h["pattern"].startswith("W12_21")
                or h["pattern"].startswith("M4")
            ]
        file_ok = lines <= budget and not stale_hits
        if rel in ("HANDOFF.md", "remain_task_list.md"):
            file_ok = file_ok and all(marker_hits.values())
        ok = ok and file_ok
        files[rel] = {
            "lines": lines,
            "line_budget": budget,
            "line_budget_ok": lines <= budget,
            "current_marker_hits": marker_hits,
            "stale_hits": stale_hits,
            "ok": file_ok,
        }
    report = {
        "phase": "M3 BacklogCompactionAudit",
        "schema": "backlog-compaction-audit/v1",
        "registry_root_hash": root,
        "files": files,
        "all_ok": bool(ok),
        "note": "task_record.md may contain old roots as cumulative history; stale root checks are enforced on handoff/remain.",
    }
    out_path = os.path.join(OUT_DIR, "BACKLOG-COMPACTION-AUDIT.json")
    json.dump(report, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("=" * 84)
    print("M3 BacklogCompactionAudit")
    print("=" * 84)
    for rel, info in files.items():
        print(f"{rel}: lines={info['lines']}/{info['line_budget']} ok={info['ok']} stale={len(info['stale_hits'])}")
    print("-" * 84)
    print(f"all_ok={ok} -> .pgf/maintenance/BACKLOG-COMPACTION-AUDIT.json")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
