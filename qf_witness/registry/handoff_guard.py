# -*- coding: utf-8 -*-
"""handoff_guard — `HANDOFF.md` 최근목록의 **불변식 게이트 + 원자적 회전**.

동기: "Recently Completed (최신 N건)" 목록을 손으로 잘라 넣다가 **세 사이클 연속으로
한 칸씩 더 지웠다**. 매번 개수 확인에서 잡혔지만 잡히지 않았다면 **조용한 이력 손실**이고,
`HANDOFF.md`·`HANDOFF-HISTORY.md` 는 gitignore 대상이라 **git 복구도 불가**하다.
고칠 것은 조심성이 아니라 **경로 자체**다 — 손자르기를 없애고 게이트를 세운다.

불변식 3종:
  I1  항목 수가 정확히 N (N 은 제목의 "최신 N건" 에서 파싱)
  I2  날짜가 **엄격 내림차순**(중복 날짜도 위반)
  I3  각 항목이 `HANDOFF-HISTORY.md` 의 `## 이름 날짜` 절과 **1:1 대응**
      (목록에만 있는 고아 없음 · 이름/날짜 불일치 없음)

사용:
  python -m qf_witness.registry.handoff_guard --check          # 게이트(all_ok)
  python -m qf_witness.registry.handoff_guard --add FILE       # 원자적 회전(추가 + 최고령 제거)

★두 파일이 없으면(clean clone·CI) **skip 하고 all_ok=True** — 있을 때만 검사한다.
★`--add` 는 **쓰기 전에** 불변식을 검사해 깨지면 쓰지 않는다(부분 편집 상태를 남기지 않음).
"""
import os
import re
import sys

from qf_witness.core.atomic_io import atomic_write_text
from qf_witness.core.paths import ROOT

HANDOFF = os.path.join(ROOT, "HANDOFF.md")
HISTORY = os.path.join(ROOT, "HANDOFF-HISTORY.md")

HEAD_RE = re.compile(r"^### Recently Completed \(최신 (\d+)건")
ITEM_RE = re.compile(r"^- \*\*(.+?)\*\* \((\d{4}-\d{2}-\d{2})\)")
HIST_RE = re.compile(r"^## (\S+) (\d{4}-\d{2}-\d{2})")


def _clean(name):
    """제목 장식(★·~~취소선~~·공백) 제거 → HISTORY 절 이름과 대조할 순수 이름."""
    return name.replace("~~", "").lstrip("★ ").strip()


def parse_section(text):
    """(헤딩 줄 index, N, 항목 목록, 섹션 끝 index) — 끝은 다음 `---` 줄."""
    lines = text.split("\n")
    hi = next((i for i, l in enumerate(lines) if HEAD_RE.match(l)), None)
    if hi is None:
        return None
    n = int(HEAD_RE.match(lines[hi]).group(1))
    end = next((i for i in range(hi + 1, len(lines)) if lines[i].strip() == "---"),
               len(lines))
    items, cur = [], None
    for i in range(hi + 1, end):
        m = ITEM_RE.match(lines[i])
        if m:
            if cur:
                items.append(cur)
            cur = {"name": _clean(m.group(1)), "raw_name": m.group(1),
                   "date": m.group(2), "start": i, "lines": [lines[i]]}
        elif cur is not None:
            if lines[i].strip() == "":
                continue
            cur["lines"].append(lines[i])
    if cur:
        items.append(cur)
    return {"lines": lines, "head": hi, "n": n, "items": items, "end": end}


def history_sections(text):
    return {(m.group(1), m.group(2))
            for m in (HIST_RE.match(l) for l in text.split("\n")) if m}


def check():
    """불변식 3종 — (all_ok, 상세 dict)."""
    if not (os.path.exists(HANDOFF) and os.path.exists(HISTORY)):
        return True, {"skipped": "HANDOFF*.md 부재(gitignore) — 있을 때만 검사"}
    sec = parse_section(open(HANDOFF, encoding="utf-8").read())
    if sec is None:
        return False, {"error": "Recently Completed 섹션을 찾지 못함"}
    hist = history_sections(open(HISTORY, encoding="utf-8").read())
    dates = [it["date"] for it in sec["items"]]
    names = [(it["name"], it["date"]) for it in sec["items"]]
    det = {
        "expected": sec["n"], "found": len(sec["items"]),
        "entries": [f"{a} {b}" for a, b in names],
        "I1_count": len(sec["items"]) == sec["n"],
        "I2_dates_strictly_descending": all(dates[i] > dates[i + 1]
                                            for i in range(len(dates) - 1)),
        "I3_all_have_history": [f"{a} {b}" for a, b in names if (a, b) not in hist],
        "history_sections": len(hist),
    }
    det["I3_one_to_one"] = not det["I3_all_have_history"]
    ok = det["I1_count"] and det["I2_dates_strictly_descending"] \
        and det["I3_one_to_one"]
    return ok, det


def add(block):
    """★원자적 회전 — 새 항목을 맨 위에 넣고 **최고령 1건만** 제거한다.

    쓰기 전에 결과를 파싱해 불변식을 검사하고, 깨지면 **쓰지 않는다**."""
    ok, det = check()
    if not ok:
        return False, {"refused": "현재 파일이 이미 불변식 위반 — 덮지 않는다",
                       "detail": det}
    text = open(HANDOFF, encoding="utf-8").read()
    sec = parse_section(text)
    blines = [l for l in block.rstrip("\n").split("\n")]
    m = ITEM_RE.match(blines[0])
    if not m:
        return False, {"refused": "새 블록의 첫 줄이 `- **이름** (YYYY-MM-DD)` 형식이 아님"}
    if sec["items"] and m.group(2) <= sec["items"][0]["date"]:
        return False, {"refused": "새 항목 날짜가 기존 최신 이하 — 내림차순 위반"}
    keep = sec["items"][:sec["n"] - 1]                      # 최고령 1건만 탈락
    body = list(blines)
    for it in keep:
        body.extend(it["lines"])
    lines = sec["lines"][:sec["head"] + 1] + [""] + body + [""] \
        + sec["lines"][sec["end"]:]
    new = "\n".join(lines)
    sec2 = parse_section(new)
    if sec2 is None or len(sec2["items"]) != sec["n"]:
        return False, {"refused": "회전 결과가 항목 수 불변식 위반",
                       "got": None if sec2 is None else len(sec2["items"])}
    atomic_write_text(HANDOFF, new, newline="\n")
    ok2, det2 = check()
    return ok2, {"rotated_in": m.group(1), "dropped": sec["items"][-1]["name"]
                 if len(sec["items"]) == sec["n"] else None, "detail": det2}


def main():
    if "--add" in sys.argv:
        p = sys.argv[sys.argv.index("--add") + 1]
        ok, det = add(open(p, encoding="utf-8").read())
        print(f"handoff_guard add: all_ok={ok} · {det}")
        return 0 if ok else 1
    ok, det = check()
    if "skipped" in det:
        print(f"handoff_guard check: all_ok={ok} · {det['skipped']}")
        return 0
    print(f"handoff_guard check: all_ok={ok} · "
          f"{det.get('found')}/{det.get('expected')}건 · "
          f"HISTORY {det.get('history_sections')}절")
    if not ok:
        print("  실패:", [k for k in ("I1_count", "I2_dates_strictly_descending",
                                     "I3_one_to_one") if det.get(k) is False],
              det)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
