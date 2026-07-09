# -*- coding: utf-8 -*-
"""expectations — manifest expectation 판정 (legacy 문자열 판정과 의미 동치, INV-RA3).

지원 종류 (확정 플랜 §1 #7 — 1차 범위):
  return_code   : int — rc 일치
  contains      : [str] — stdout+stderr 에 전부 포함
  regex         : [{"pattern","capture_as",("assert_equal_groups")}] — 캡처(판정 아님, 단
                  assert_equal_groups=true 면 그룹 전원 일치가 판정에 참여)
legacy witness 판정 `rc==0 and "all_ok=True" in out` == {return_code:0, contains:["all_ok=True"]}.
"""
import re


def evaluate(expect, rc, out):
    """→ (passed: bool, extra_fields: dict) — extra 는 report 스텝 dict 에 병합."""
    passed = True
    extra = {}
    if "return_code" in expect:
        passed = passed and (rc == expect["return_code"])
    for s in expect.get("contains", []):
        found = s in out
        passed = passed and found
        if s == "all_ok=True":                    # legacy report 필드 호환
            extra["all_ok"] = found
    for spec in expect.get("regex", []):
        m = re.search(spec["pattern"], out)
        cap = spec.get("capture_as")
        if m:
            if len(m.groups()) >= 2 and not isinstance(cap, dict):
                extra[cap] = f"{m.group(1)}/{m.group(2)}"
            elif isinstance(cap, dict):
                for k, gi in cap.items():
                    extra[k] = m.group(gi)
            elif cap:
                extra[cap] = m.group(1)
            if spec.get("assert_equal_groups"):
                passed = passed and len(set(m.groups())) == 1
        else:
            if cap and not isinstance(cap, dict):
                extra[cap] = "?"
    return passed, extra
