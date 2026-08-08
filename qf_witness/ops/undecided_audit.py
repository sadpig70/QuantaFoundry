#!/usr/bin/env python
"""★한도(cap/budget/limit) 소진 분기가 **답인 척하지 않는지** 전수 감사.

동기: `A6P3ClassClosureDeep` 사이클에서 `iso_lift`·`find_isomorphism` 이
**노드 예산 소진 시 `found=False`(비동형)** 를 돌려주고 있었다 — 못 끝낸 것을
답이라 부르는 거짓이다. 새 게이트가 잡았고, 그 뒤 **같은 패턴이 다른 곳에도 있는지**
기계적으로 훑어 `a5_rep3`(포기 `-1` 이 `!= 60` 을 통과)·`twist_d5_lattice`
(잘린 집합 위의 `all(...)`)에서 **2건 더** 찾았다.

감사 규칙 — 한도를 비교하는 `if`/`while` 의 **탈출 분기**는 셋 중 하나여야 한다:
  (a) 예외를 던진다
  (b) **명시적 미판정/사유 값**을 돌려준다(`None`·`"skip"`·`undecided`·하계 등)
  (c) 산출물에 `capped`/`truncated`/`skipped` 를 **기록**한다
조용한 `False`/`0`/`[]`/`continue` 는 **위반**이다.

정직 경계:
  · 이것은 **정적 감사**다 — 실행 경로가 아니라 **코드 형태**를 본다. 통과가
    "거짓 주장이 없다"의 증명은 아니고, **검토되지 않은 새 한도가 없다**는 뜻이다.
  · 그래서 `REVIEWED` 에 **검토 근거를 사람 말로** 적어 둔다. 새 사이트가 생기면
    목록에 없으므로 **실패**하고, 그때 근거를 적어야 통과한다(검토 강제).
  · `tilting_complex_observe` 는 byte-결정론 확정이라 **읽기만** 한다.
"""
import ast
import json
import os
import re
import sys

from qf_witness.core.paths import ROOT

SCAN = os.path.join(ROOT, "qf_witness")
LIM = re.compile(r"(?i)(^|_)(cap|caps|budget|limit|maxn|maxdim|maxdeg|"
                 r"timeout|depth|cutoff|quota|ceiling)($|_)")
REC = re.compile(r"(?i)(capped|undecided|hit_cap|truncated|skip|blowup|"
                 r"too_large|partial|incomplete|exceeded|abort)")

# ★검토 완료 목록 — (파일, 함수, 근거). 여기 없는 한도 탈출은 **미검토**로 실패한다.
REVIEWED = {
    # ★함수명은 감사기가 보고하는 이름(가장 안쪽 정의)을 그대로 쓴다.
    ("observe/a5_rep3_observe.py", "known"):
        "`group_order` 의 cap 초과 분기. -len(seen) 로 **하계**를 돌려준다(포기 아님). "
        "호출부는 그 하계가 60 을 넘는지로 '위수 60 아님'을 증명한다. "
        "★이번 감사가 잡은 위반 — 예전엔 -1 을 돌려줘 `!= 60` 이 **포기만으로 통과**했다.",
    ("observe/a7_cartan_p2_observe.py", "simple_and_orbits"):
        "cap 이 걸리면 simple 자리에 None(미판정). 반례(False)는 cap 과 무관하게 "
        "확정. 현재 호출부는 cap=None(전수). ★이번 감사가 고친 잠재 위반.",
    ("observe/twist_d5_lattice_observe.py", "enumerate_candidates"):
        "limit 이 걸리면 (out, True) 로 **잘렸음**을 함께 돌려주고, 호출부가 "
        "A_full_run_is_exhaustive 로 full=전수·quick=잘림을 명시 기록한다. "
        "★이번 감사가 잡은 위반 — 잘린 집합 위의 `all(...)` 은 전칭 주장이 아니다.",
    ("observe/tilting_complex_observe.py", "rec"):
        "`isometries` 의 cap. ★byte-결정론 확정 모듈이라 **읽기만** 했다. 호출부 "
        "주장은 전부 **양성**(bool(found) — 잘려도 참)이고, 보고하는 n_isometries "
        "실측 최대값이 16 < cap 64 라 **잘린 적이 없다**. 안전.",
    ("observe/gfq_engine.py", "rec"):
        "`find_isomorphism` 탐색 예산 — 소진 시 found=None + undecided='node_cap'.",
    ("observe/gfq_engine.py", "rec1"):
        "`iso_lift` 노드 예산 — 소진 시 'CAP' 를 올려 보내고 호출부가 "
        "found=None + undecided='node_cap' 로 돌려준다. ★이번 감사의 발단.",
    ("observe/gfq_engine.py", "_line_inv_table"):
        "q^m 이 cap 을 넘으면 None — 가지치기를 **포기**할 뿐 판정을 바꾸지 않는다"
        "(호출부는 None 이면 전수 경로로 가고 그 경로는 gl_cap 으로 미판정).",
    ("observe/gfq_engine.py", "_wvals"):
        "`len(w) < depth` 는 트라이 순회 조건이지 한도가 아니다(오탐).",
    ("ops/discover.py", "goal_selection_guard"):
        "`cap in seen` 의 cap 은 후보 변수명이지 한도가 아니다(오탐).",
    ("verify/matchgate_verify.py", "verify_app"):
        "n>N_CAP 에 (None, 사유) — 명시 미판정.",
    ("verify/qmdd_verify.py", "collect"):
        "`depth == k` 는 재귀 바닥이지 한도가 아니다(오탐).",
    ("verify/qmdd_verify.py", "rebuild"):
        "`depth == k` 는 재귀 바닥이지 한도가 아니다(오탐).",
    ("verify/tncontract_verify.py", "tn_column"):
        "depth>8 에 None — docstring 이 '미지원 시 None' 으로 명시.",
}


def _fnname(tree, node):
    best = None
    for f in ast.walk(tree):
        if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if f.lineno <= node.lineno and (best is None
                                            or f.lineno > best.lineno):
                best = f
    return best.name if best else "<module>"


def _limnames(node):
    out = set()
    for n in ast.walk(node):
        if isinstance(n, ast.Name) and LIM.search(n.id):
            out.add(n.id)
        elif isinstance(n, ast.Attribute) and LIM.search(n.attr):
            out.add(n.attr)
        elif (isinstance(n, ast.Constant) and isinstance(n.value, str)
                and LIM.search(n.value)):
            out.add(n.value)
    return out


def scan():
    sites = []
    for dp, _dn, fn in os.walk(SCAN):
        if "__pycache__" in dp:
            continue
        for f in sorted(fn):
            if not f.endswith(".py") or f == "undecided_audit.py":
                continue
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, SCAN).replace("\\", "/")
            try:
                tree = ast.parse(open(p, encoding="utf-8").read())
            except SyntaxError:
                continue
            for node in ast.walk(tree):
                if not isinstance(node, (ast.If, ast.While)):
                    continue
                if not _limnames(node.test):
                    continue
                seg = "\n".join(ast.unparse(b) for b in node.body)
                exits = [b for b in node.body
                         if isinstance(b, (ast.Return, ast.Break,
                                           ast.Continue))]
                if not exits:
                    continue
                kind = ("RAISES" if any(isinstance(b, ast.Raise)
                                        for b in ast.walk(node)) else
                        "RECORDS" if REC.search(seg) else "NEEDS-REVIEW")
                sites.append({"file": rel, "func": _fnname(tree, node),
                              "line": node.lineno, "kind": kind})
    return sites


def main():
    sites = scan()
    need = [s for s in sites if s["kind"] == "NEEDS-REVIEW"]
    unlisted = sorted({(s["file"], s["func"]) for s in need
                       if (s["file"], s["func"]) not in REVIEWED})
    stale = sorted(k for k in REVIEWED
                   if k not in {(s["file"], s["func"]) for s in sites})
    ok = not unlisted
    out = {"scanned_sites": len(sites),
           "by_kind": {k: sum(1 for s in sites if s["kind"] == k)
                       for k in ("RAISES", "RECORDS", "NEEDS-REVIEW")},
           "needs_review": need, "unlisted": [list(u) for u in unlisted],
           "stale_reviewed_entries": [list(k) for k in stale],
           "reviewed_count": len(REVIEWED), "all_ok": ok,
           "rule": ("한도 소진 탈출은 (a)예외 (b)명시 미판정/사유 (c)capped 기록 "
                    "중 하나여야 한다. 조용한 False/0/[]/continue 는 위반."),
           "honest": ("정적 감사다 — 통과는 '거짓 주장이 없다'의 증명이 아니라 "
                      "'**검토되지 않은 새 한도가 없다**'는 뜻이다.")}
    if "--json" in sys.argv:
        print(json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print("undecided_audit: all_ok=%s · 사이트 %d "
              "(RAISES %d · RECORDS %d · 검토대상 %d) · 검토목록 %d"
              % (ok, out["scanned_sites"], out["by_kind"]["RAISES"],
                 out["by_kind"]["RECORDS"], out["by_kind"]["NEEDS-REVIEW"],
                 len(REVIEWED)))
        for u in unlisted:
            print("  ★미검토 한도 탈출:", u[0], u[1])
        for k in stale:
            print("  · 검토목록에만 있고 코드엔 없음(정리 대상):", k[0], k[1])
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
