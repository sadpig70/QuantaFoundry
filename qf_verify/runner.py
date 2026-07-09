# -*- coding: utf-8 -*-
"""runner — profile 실행 엔진 (순차 고정, INV-RA5) + legacy 호환 report 조립 (INV-RA2).

result["steps"] 의 키 순서 = manifest 실행 순서 = legacy reproduce_all.py 와 동일.
스텝 dict 필드도 legacy 와 동일 (witness: rc/all_ok/pass · special: 각자 고유 필드).
"""
import time

from . import context as cx
from . import special as sp
from . import manifest as mf
from . import expectations as ex
from . import report as rp


def execute_step(st, changed_only):
    """단일 스텝 실행 → (steps_fragment: dict, meta: dict)."""
    t0 = time.time()
    if "special" in st:
        frag = sp.REGISTRY[st["special"]](changed_only)
        ok = all(v.get("pass") for v in frag.values())
        meta = {"ids": list(frag), "status": "pass" if ok else "fail"}
    else:
        rc, out = cx.run(list(st["argv"]))
        passed, extra = ex.evaluate(st["expectations"], rc, out)
        entry = {"rc": rc}
        entry.update(extra)
        entry["pass"] = passed
        frag = {st.get("report_key", st["id"]): entry}
        meta = {"ids": [st["id"]], "status": "pass" if passed else "fail"}
    meta["duration_ms"] = int((time.time() - t0) * 1000)
    meta["severity"] = st.get("severity", "high")
    meta["claims"] = st.get("claims", [])
    meta["group"] = st.get("_group", "?")
    return frag, meta


def run_profile(profile_id, echo=print):
    """profile 전체 실행 → (result dict, evidence list, exit_code)."""
    steps, changed_only = mf.load_profile(profile_id)
    result = {"bundle": "UNKNOWN", "steps": {}}
    result["mode"] = "changed-only" if changed_only else "full"
    evidence = []
    for st in steps:
        frag, meta = execute_step(st, changed_only)
        result["steps"].update(frag)
        evidence.append({"id": st["id"], **meta})
    allpass = all(s.get("pass") for s in result["steps"].values())
    result["bundle"] = "REPRODUCED" if allpass else "FAILED"

    rp.write_reproduce_result(result)
    rp.write_evidence_report(profile_id, result, evidence)

    # legacy 와 동일한 콘솔 출력
    echo("=" * 70)
    echo(f"REPRODUCE-ALL → {result['bundle']}")
    for k, v in result["steps"].items():
        echo(f"  {'✓' if v.get('pass') else '✗'} {k}: " +
             ", ".join(f"{kk}={vv}" for kk, vv in v.items() if kk not in ("detail", "rc")))
    echo("-" * 70)
    echo("INV-R1: 'REPRODUCED'=결정론적 byte-identical 재현이지 correctness 증명이 아니다.")
    echo("  정확성은 오라클의 독립검증(C1-C4·second_oracle·subspace/resource witness)에서 온다.")
    echo("=" * 70)
    return result, evidence, (0 if allpass else 1)
