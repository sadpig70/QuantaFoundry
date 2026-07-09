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

FRONTIER_STEPS = [
    ("shor_frontier", "scripts/shor_frontier.py"),
    ("c8x_frontier", "scripts/c8x_frontier.py"),
    ("shor221_frontier", "scripts/shor221_frontier.py"),
    ("c9x_shor381_frontier", "scripts/c9x_shor381_frontier.py"),
    ("c10x_frontier", "scripts/c10x_frontier.py"),
    ("shor635_frontier", "scripts/shor635_frontier.py"),
    ("c11x_frontier", "scripts/c11x_frontier.py"),
    ("c11x_payoff_family", "scripts/c11x_payoff_family.py"),
    ("shor1285_frontier", "scripts/shor1285_frontier.py"),
    ("c12x_frontier", "scripts/c12x_frontier.py"),
    ("c12x_payoff_family", "scripts/c12x_payoff_family.py"),
    ("shor3683_frontier", "scripts/shor3683_frontier.py"),
]
FACTORY_STEP = ("frontier_factory", "scripts/frontier_factory.py")


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
    """1b. frontier/factory — changed-only & 무변경 시 coherence+factory, 그 외 전량 (이식)."""
    steps = {}
    specs_changed = cx.frontier_specs_changed() if changed_only else True
    if changed_only and not specs_changed:
        steps["frontier_coherence"] = cx.coherence_sweep_frontier()
        fstep_id, fscript = FACTORY_STEP
        rc, out = cx.run([fscript, "--reproduce"])
        steps[fstep_id] = {"rc": rc, "all_ok": "all_ok=True" in out,
                           "pass": rc == 0 and "all_ok=True" in out}
    else:
        for step_id, script in FRONTIER_STEPS:
            rc, out = cx.run([script])
            steps[step_id] = {"rc": rc, "all_ok": "all_ok=True" in out,
                              "pass": rc == 0 and "all_ok=True" in out}
        fstep_id, fscript = FACTORY_STEP
        rc, out = cx.run([fscript, "--reproduce"])
        steps[fstep_id] = {"rc": rc, "all_ok": "all_ok=True" in out,
                           "pass": rc == 0 and "all_ok=True" in out}
    return steps


def registry_build(changed_only):
    """2. registry manifest + dependency graph (regex 캡처 — 이식)."""
    rc, out = cx.run(["scripts/registry_tools.py", "build"])
    mm = re.search(r"modules=(\d+) unique_apps=(\d+) cached=(\d+) root=(\w+)", out)
    return {"registry": {
        "rc": rc, "modules": mm.group(1) if mm else "?", "unique_apps": mm.group(2) if mm else "?",
        "cached": mm.group(3) if mm else "?", "root_hash": mm.group(4) if mm else "?", "pass": rc == 0}}


def second_oracle(changed_only):
    """3. 독립 2차 검증 (rc 판정 + 모듈 N/N 캡처 — 이식)."""
    rc, out = cx.run(["scripts/second_oracle.py"])
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
