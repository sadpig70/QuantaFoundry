# -*- coding: utf-8 -*-
"""runner — profile 실행 엔진 (순차 고정, INV-RA5) + legacy 호환 report 조립 (INV-RA2).

result["steps"] 의 키 순서 = manifest 실행 순서 = legacy reproduce_all.py 와 동일.
스텝 dict 필드도 legacy 와 동일 (witness: rc/all_ok/pass · special: 각자 고유 필드).
"""
import time
from concurrent.futures import ThreadPoolExecutor

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


def _execute_all(steps, changed_only, jobs):
    """스텝 실행 → results[i]=(frag,meta) 원래 순서 슬롯.
    jobs=1: 완전 순차(기존 불변). jobs>1: 연속 argv(독립 read-only) run 을 ThreadPool 로 병렬,
    special(변경·순서 백본)은 순차 배리어. 결과 조립은 항상 원순서(INV-RA2)."""
    results = [None] * len(steps)
    if jobs <= 1:
        for i, st in enumerate(steps):
            results[i] = execute_step(st, changed_only)
        return results
    i, n = 0, len(steps)
    while i < n:
        if "special" not in steps[i]:                 # 연속 argv run → 병렬
            j = i
            while j < n and "special" not in steps[j]:
                j += 1
            batch = list(range(i, j))
            with ThreadPoolExecutor(max_workers=min(jobs, len(batch))) as pool:
                futs = {pool.submit(execute_step, steps[k], changed_only): k for k in batch}
                for fut, k in futs.items():
                    results[k] = fut.result()
            i = j
        else:                                          # special → 순차(원순서 보존)
            results[i] = execute_step(steps[i], changed_only)
            i += 1
    return results


def run_profile(profile_id, echo=print, jobs=1):
    """profile 전체 실행 → (result dict, evidence list, exit_code).
    jobs>1 이면 독립 argv 스텝을 병렬 실행(root 불변; 결과 조립은 원순서 고정)."""
    steps, changed_only = mf.load_profile(profile_id)
    results = _execute_all(steps, changed_only, jobs)
    result = {"bundle": "UNKNOWN", "steps": {}}
    result["mode"] = "changed-only" if changed_only else "full"
    evidence = []
    for idx, st in enumerate(steps):                    # 조립 = 원래 manifest 순서
        frag, meta = results[idx]
        result["steps"].update(frag)
        evidence.append({"id": st["id"], **meta})
    allpass = all(s.get("pass") for s in result["steps"].values())
    result["bundle"] = "REPRODUCED" if allpass else "FAILED"

    rp.write_reproduce_result(result)
    rp.write_evidence_report(profile_id, result, evidence)
    from . import claims                    # QF-0711 U7b: 방금 완료한 run 기준 CLAIM-EVIDENCE-MAP 자동 생성
    claims.write_claim_map()
    import subprocess as _sp                 # QF-0711 U8: settled sidecar 기준 커버리지 생성(post-run, race 회피)
    _sp.run(["python", "-m", "qf_witness.registry.coverage_matrix"], cwd=cx.ROOT, capture_output=True)
    _sp.run(["python", "-m", "qf_witness.registry.quality_scorecard"], cwd=cx.ROOT, capture_output=True)  # U13

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
