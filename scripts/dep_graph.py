# -*- coding: utf-8 -*-
"""
dep_graph.py — P5 DepGraphClosure (task_plan_pg §P5)

goal-autonomy 의 gap 탐지(detect_gaps)와 registry DAG(registry_tools)를 결합해
**standing 의존성 그래프 산출물**(DEPENDENCY-GRAPH.json)을 만든다. BLOCKED 노드는
누락 prereq 를 스스로 지목(self-identification) — 자율루프의 frontier 입력이 된다.

sub-PG:
    DepGraphEmit   // build_graph(DAG) + build_manifest(root_hash) + detect_gaps(frontier) 결합
    FrontierReport // BLOCKED 노드의 missing-prereq 자가지목 + buildable frontier 요약

정직성: 분석전용 비파괴(.pgf/autonomy/ 만 기록). registry/seal/frozen 불변.
registry_tools·goal_autonomy 는 *사용만*(인메모리 호출, canonical manifest 미덮어씀).
신규 봉인(P1 의 c6x·cmul2_mod3{3,5})이 DAG·frontier 에 자동 반영된다.
"""
from __future__ import annotations

import os
import sys
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import registry_tools as rt     # noqa: E402  (build_graph/build_manifest/dependents 사용만)
import goal_autonomy as ga      # noqa: E402  (detect_gaps/score 사용만)

OUT = os.path.join(ROOT, ".pgf", "autonomy")


def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 72)
    print("P5 DepGraphClosure — 의존 DAG + frontier gap standing 산출")
    print("정직성: 분석전용 비파괴. registry_tools/goal_autonomy 사용만(canonical 미변경).")
    print("=" * 72)

    # 1. DepGraphEmit — DAG + manifest(root_hash)
    graph = rt.build_graph()
    manifest = rt.build_manifest(graph)
    root = manifest["registry_root_hash"]
    print(f"[DepGraphEmit] DAG {len(graph)} apps · modules {manifest['modules']['count']} · "
          f"root_hash={root[:12]}")

    # 2. detect_gaps — frontier (buildable / BLOCKED-with-missing self-pointing)
    gaps = ga.detect_gaps()
    ranked = sorted(({**g, "score": ga.score(g)} for g in gaps), key=lambda x: -x["score"])
    buildable = [g for g in ranked if g["buildable"]]
    blocked = [g for g in ranked if (not g["buildable"]) and g["missing_modules"]]

    # 3. FrontierReport — family별 frontier
    families = {}
    for g in ranked:
        fam = g["family"]
        families.setdefault(fam, {"buildable_next": [], "blocked_next": []})
        if g["buildable"]:
            families[fam]["buildable_next"].append({"id": g["id"], "score": g["score"]})
        elif g["missing_modules"]:
            families[fam]["blocked_next"].append(
                {"id": g["id"], "missing_prereq": g["missing_modules"]})

    print(f"[Frontier] gap {len(ranked)} · buildable {len(buildable)} · "
          f"blocked(자가지목 prereq) {len(blocked)}")
    for g in buildable[:6]:
        print(f"   BUILD   {g['id']:12} score={g['score']} reuse={g['required_modules']}")
    for g in blocked[:6]:
        print(f"   BLOCKED {g['id']:12} → 누락 prereq 자가지목: {g['missing_modules']}")

    out = {
        "phase": "P5 DepGraphClosure",
        "honesty": "analysis-only non-destructive; registry_tools/goal_autonomy used in-memory "
                   "(canonical manifest not overwritten); registry/seal/frozen untouched.",
        "registry_root_hash": root,
        "module_count": manifest["modules"]["count"],
        "unique_app_count": manifest["apps"]["unique_app_count"],
        "cached_app_side_module_count": manifest["apps"]["cached_app_side_module_count"],
        "dag": {app: {"u_hash": (g["u_hash"] or "")[:16],
                      "depends_on": [{"kind": e["kind"], "id": e["id"], "uses": e["uses"]}
                                     for e in g["depends_on"]]}
                for app, g in sorted(graph.items())},
        "frontier": {
            "total_gaps": len(ranked),
            "buildable": [{"id": g["id"], "family": g["family"], "score": g["score"],
                           "reuse_modules": g["required_modules"]} for g in buildable],
            "blocked_self_identified_prereq": [
                {"id": g["id"], "family": g["family"], "missing_modules": g["missing_modules"]}
                for g in blocked],
        },
        "by_family": families,
        "note": "frontier.blocked 의 missing_modules = 자율루프가 스스로 지목하는 선행조건. "
                "이 prereq 를 먼저 봉인하면 해당 멤버가 buildable 로 전환(W→Ry→W 패턴). "
                "P1 에서 c6x 봉인으로 distinct-prime cmul 패밀리가 잠금해제된 것과 동형.",
    }
    json.dump(out, open(os.path.join(OUT, "DEPENDENCY-GRAPH.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("-" * 72)
    print(f"→  .pgf/autonomy/DEPENDENCY-GRAPH.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
