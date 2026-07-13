# -*- coding: utf-8 -*-
"""special — manifest 로 표현하기 어려운 코드 스텝 5종 (reproduce_all.py main() 이식, INV-RA3).

각 함수는 (step_id → step_result_dict) 항목들의 OrderedDict 조각을 반환한다 —
runner 가 실행 순서대로 result["steps"] 에 병합(기존 report 키·필드 완전 동일).
"""
import os
import re
import json
from . import context as cx

ROOT = cx.ROOT

# argv 는 `-m qf_witness.<cat>.<name>` 모듈 호출 형태(scripts/ shim 폐기, C안). cx.run 이 앞에 python 을 붙인다.
FRONTIER_STEPS = [
    ("shor_frontier", ["-m", "qf_witness.frontier.shor_frontier"]),
    ("c8x_frontier", ["-m", "qf_witness.frontier.c8x_frontier"]),
    ("shor221_frontier", ["-m", "qf_witness.frontier.shor221_frontier"]),
    ("c9x_shor381_frontier", ["-m", "qf_witness.frontier.c9x_shor381_frontier"]),
    ("c10x_frontier", ["-m", "qf_witness.frontier.c10x_frontier"]),
    ("shor635_frontier", ["-m", "qf_witness.frontier.shor635_frontier"]),
    ("c11x_frontier", ["-m", "qf_witness.frontier.c11x_frontier"]),
    ("c11x_payoff_family", ["-m", "qf_witness.family.c11x_payoff_family"]),
    ("shor1285_frontier", ["-m", "qf_witness.frontier.shor1285_frontier"]),
    ("c12x_frontier", ["-m", "qf_witness.frontier.c12x_frontier"]),
    ("c12x_payoff_family", ["-m", "qf_witness.family.c12x_payoff_family"]),
    ("shor3683_frontier", ["-m", "qf_witness.frontier.shor3683_frontier"]),
]
FACTORY_STEP = ("frontier_factory", ["-m", "qf_witness.frontier.frontier_factory"])


def forge_apps(changed_only):
    """1. 앱 재봉인 + 재발견 교차검증 (regex 캡처 — reproduce_all 이식)."""
    forge_args = [".pgf/autoforge/forge_apps.py"] + (["--changed-only"] if changed_only else [])
    rc, out = cx.run(forge_args)
    m = re.search(r"앱 봉인 (\d+)/(\d+) · 재발견 교차검증 (\d+)/(\d+)", out)
    fa = {"rc": rc, "apps_sealed": f"{m.group(1)}/{m.group(2)}" if m else "?",
          "rediscovery": f"{m.group(3)}/{m.group(4)}" if m else "?", "pass": rc == 0}
    if changed_only:
        cm = re.search(r"재조립 (\d+) · coherence (\d+)", out)
        if cm:
            fa["reassembled"], fa["coherence"] = int(cm.group(1)), int(cm.group(2))
    return {"forge_apps": fa}


def frontier_block(changed_only):
    """1b. frontier/factory — changed-only & 무변경 시 coherence+factory, 그 외 전량 (이식).

    SpeedOpt O1(rework): FRONTIER_STEPS 는 N-가족별 직렬 그룹으로 묶어 그룹 간만 병렬
    (같은 가족은 같은 앱 재봉인 파일을 공유 — 동시 기록 레이스가 실측 재현되어 직렬화).
    factory --reproduce 는 sealed_N(legacy 가족과 disjoint) 청크로 병렬(O1b). 결과 조립은
    원순서 고정(INV-RA2 계열)·report 형태 불변.
    """
    steps = {}
    specs_changed = cx.frontier_specs_changed() if changed_only else True
    if changed_only and not specs_changed:
        steps["frontier_coherence"] = cx.coherence_sweep_frontier()
        fstep_id, fargv = FACTORY_STEP
        rc, out = cx.run([*fargv, "--reproduce"])
        steps[fstep_id] = {"rc": rc, "all_ok": "all_ok=True" in out,
                           "pass": rc == 0 and "all_ok=True" in out}
    else:
        from concurrent.futures import ThreadPoolExecutor
        workers = min(6, max(1, (os.cpu_count() or 2) - 2))
        fstep_id, fargv = FACTORY_STEP
        # ★레이스 경계(SpeedOpt O1 rework): legacy frontier 스크립트는 REPORT 외에 같은 N-가족
        #   앱 재봉인 파일도 기록 → 같은 가족은 직렬 체인, 가족 간(N disjoint)만 병렬.
        groups = [["shor_frontier"],
                  ["c8x_frontier", "shor221_frontier"],
                  ["c9x_shor381_frontier"],
                  ["c10x_frontier", "shor635_frontier"],
                  ["c11x_frontier", "c11x_payoff_family", "shor1285_frontier"],
                  ["c12x_frontier", "c12x_payoff_family", "shor3683_frontier"]]
        argv_of = dict(FRONTIER_STEPS)

        def _run_group(ids):
            return [(sid, cx.run(argv_of[sid])) for sid in ids]

        # SpeedOpt O1b: factory sealed_N(legacy 가족과 disjoint)을 청크 분할 --reproduce --only 병렬
        try:
            db = json.load(open(os.path.join(ROOT, ".pgf", "arith", "FACTORY-FRONTIER.json"),
                                encoding="utf-8"))
            ns = [e["N"] for e in db["sealed_N"]]
        except Exception:
            ns = []
        chunks = [c for c in ([ns[i::workers] for i in range(workers)] if ns else []) if c]
        # ★2상 분리 + 실패분 순차 재시도 1회: 병렬 쓰기는 상주 AV 의 일시 파일잠금으로 간헐
        #   실패할 수 있다(실측). 스크립트는 결정론 재유도라 재실행이 byte-identical 로 수렴 —
        #   transient 는 self-heal, 진짜 실패는 재시도에서도 실패(정직 유지). 최종 판정은 재시도값.
        def _verdict(rc, out):
            return {"rc": rc, "all_ok": "all_ok=True" in out,
                    "pass": rc == 0 and "all_ok=True" in out}

        with ThreadPoolExecutor(max_workers=workers) as pool:
            got = {}
            for f in [pool.submit(_run_group, g) for g in groups]:   # Phase A: legacy 그룹 병렬
                for sid, (rc, out) in f.result():
                    got[sid] = _verdict(rc, out)
            for sid in [s for s, v in got.items() if not v["pass"]]:
                got[sid] = _verdict(*cx.run(argv_of[sid]))           # 순차 재시도 1회
            if chunks:                                               # Phase B: factory 청크 병렬
                cfuts = [pool.submit(cx.run, [*fargv, "--reproduce", "--only",
                                              *map(str, c)]) for c in chunks]
            else:
                cfuts = [pool.submit(cx.run, [*fargv, "--reproduce"])]
            cres = [_verdict(*f.result()) for f in cfuts]
        for i, v in enumerate(cres):
            if not v["pass"] and chunks:                             # 청크 순차 재시도 1회
                cres[i] = _verdict(*cx.run([*fargv, "--reproduce", "--only",
                                            *map(str, chunks[i])]))
        for step_id, _argv in FRONTIER_STEPS:            # 원순서 조립 (INV-RA2 계열)
            steps[step_id] = got[step_id]
        steps[fstep_id] = {"rc": max(v["rc"] for v in cres),         # factory = 합산 단일 항목
                           "all_ok": all(v["all_ok"] for v in cres),
                           "pass": all(v["pass"] for v in cres)}
    return steps


def registry_build(changed_only):
    """2. registry manifest + dependency graph (regex 캡처 — 이식)."""
    rc, out = cx.run(["-m", "qf_witness.registry.registry_tools", "build"])
    mm = re.search(r"modules=(\d+) unique_apps=(\d+) cached=(\d+) root=(\w+)", out)
    return {"registry": {
        "rc": rc, "modules": mm.group(1) if mm else "?", "unique_apps": mm.group(2) if mm else "?",
        "cached": mm.group(3) if mm else "?", "root_hash": mm.group(4) if mm else "?", "pass": rc == 0}}


def second_oracle(changed_only):
    """3. 독립 2차 검증 (rc 판정 + 모듈 N/N 캡처 — 이식)."""
    rc, out = cx.run(["-m", "qf_witness.verify.second_oracle"])
    sm = re.search(r"모듈 독립검증 (\d+)/(\d+)", out)
    return {"second_oracle": {"rc": rc, "modules": f"{sm.group(1)}/{sm.group(2)}" if sm else "?",
                              "pass": rc == 0}}


def behavior(changed_only):
    """4. 행동 검증 — Shor 인수분해 peak + cmul21 orbit (인라인 numpy — 이식)."""
    beh = {}
    import numpy as np

    def golden_of(app):
        src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
        code = re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1)
        ns = {}
        exec(code, ns)  # noqa: S102 — tracked spec (legacy 동일)
        return ns["golden"]

    for app, dim, exp in [("shor15_a2.app.pg", 128, {0, 2, 4, 6}),
                          ("shor15_a7.app.pg", 128, {0, 2, 4, 6})]:
        G = golden_of(app)
        psi = np.zeros(dim, complex)
        psi[1] = 1.0
        out = G @ psi
        pk = {}
        for s in range(dim):
            if abs(out[s]) ** 2 > 1e-9:
                c = (s >> 4) & 7
                pk[c] = pk.get(c, 0) + abs(out[s]) ** 2
        beh[app[:-7]] = {"peaks": sorted(pk), "expected": sorted(exp),
                         "pass": set(k for k in pk if pk[k] > 0.01) == exp}
    G = golden_of("cmul2_mod21.app.pg")
    w = 1
    orbit = [1]
    for _ in range(6):
        w = int(np.argmax(G[:, (1 << 5) | w])) & 31
        orbit.append(w)
    beh["cmul2_mod21_orbit"] = {"orbit": orbit,
                                "period6": orbit[0] == orbit[6] and len(set(orbit[:6])) == 6}
    return {"behavior": {"detail": beh,
                         "pass": all(v.get("pass", v.get("period6")) for v in beh.values())}}


# manifest "special" 필드 → 함수 매핑
REGISTRY = {
    "forge_apps": forge_apps,
    "frontier_block": frontier_block,
    "registry_build": registry_build,
    "second_oracle": second_oracle,
    "behavior": behavior,
}
