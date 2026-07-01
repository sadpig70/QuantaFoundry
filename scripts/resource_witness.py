#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""resource_witness — V08 P0/HonestyHardening (X_ResourceWitness, A6 리뷰 대응).

봉인 resource 필드(t·toffoli·clifford·rotation·and_bloq·measurement·total_t)가 회로 구조와
일관됨을 독립 재계산으로 검증한다. 조립 앱(plan 보유)의 resource == 자식(module/app) resource 합.

  A6 우려: "seal resource 필드가 검증되지 않는다 — 회로와 결정론 대조해야 FTQC 자원계약을 신뢰".
  → plan 을 독립 파싱해 자식 sealed resource 를 합산하고 app sealed resource 와 대조(오라클 무관).

비파괴: 읽기 전용 + 리포트 `.pgf/proofs/RESOURCE-WITNESS.json`. sealed/oracle/frozen/root 무영향.
teeth: 임의 자식 resource 를 변조하면 합이 어긋나 witness 실패(공허하지 않음).

사용: python scripts/resource_witness.py [--quick]
"""
import os, re, sys, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPREG = os.path.join(ROOT, "registry", "apps")
MODREG = os.path.join(ROOT, "registry", "modules")
APPS = os.path.join(ROOT, "specs", "apps")
OUT = os.path.join(ROOT, ".pgf", "proofs", "RESOURCE-WITNESS.json")

STRUCTURAL_SHOR = ["shor69", "shor77", "shor91", "shor119", "shor221",
                   "shor381", "shor635", "shor1285", "shor3683"]


def _sealed(reg, id_):
    p = os.path.join(reg, f"{id_}.sealed.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def _plan_steps(app_id):
    """app.pg 의 id=plan fence → steps (없으면 None)."""
    spec = os.path.join(APPS, f"{app_id}.app.pg")
    if not os.path.exists(spec):
        return None
    m = re.search(r"```json id=plan\s*\n(.*?)\n```", open(spec, encoding="utf-8").read(), re.S)
    return json.loads(m.group(1))["steps"] if m else None


def witness(app_id):
    """→ dict. app resource == Σ 자식 resource 이면 consistent."""
    app = _sealed(APPREG, app_id)
    steps = _plan_steps(app_id)
    if app is None or steps is None or "resource" not in app:
        return {"id": app_id, "status": "skip", "reason": "no plan/resource"}
    agg = {}
    for st in steps:
        if "spec" in st:
            cid = os.path.basename(st["spec"]).split(".")[0]; child = _sealed(MODREG, cid)
        else:
            cid = os.path.basename(st["app"]).split(".")[0]; child = _sealed(APPREG, cid)
        if child is None or "resource" not in child:
            return {"id": app_id, "status": "skip", "reason": f"child {cid} no resource"}
        for k, v in child["resource"].items():
            agg[k] = agg.get(k, 0) + v
    consistent = (agg == app["resource"])
    return {"id": app_id, "status": "checked", "consistent": bool(consistent),
            "sealed_resource": app["resource"], "children_sum": agg,
            "n_children": len(steps)}


def main():
    quick = "--quick" in sys.argv
    ids = [os.path.basename(p).split(".")[0]
           for p in sorted(glob.glob(os.path.join(APPREG, "*.sealed.json")))]
    checked = skipped = consistent = 0
    inconsistencies = []
    results = {}
    for aid in ids:
        w = witness(aid)
        results[aid] = w
        if w["status"] == "skip":
            skipped += 1
        else:
            checked += 1
            if w["consistent"]:
                consistent += 1
            else:
                inconsistencies.append(aid)
    # structural Shor 는 반드시 consistent (teeth on the load-bearing seals)
    shor_ok = all(results.get(s, {}).get("consistent") for s in STRUCTURAL_SHOR)
    all_ok = (not inconsistencies) and shor_ok

    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        report = {"_schema": "resource-witness-v1",
                  "_note": "조립 앱 resource == 자식 resource 합 독립 재계산(A6). sealed/oracle/root 무영향.",
                  "checked": checked, "consistent": consistent, "skipped": skipped,
                  "structural_shor_all_consistent": shor_ok,
                  "inconsistencies": inconsistencies, "results": results}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print(f"resource_witness: checked={checked} consistent={consistent} skipped={skipped}", flush=True)
        print(f"  structural Shor all consistent: {shor_ok}", flush=True)
        if inconsistencies:
            print(f"  ⚠ inconsistent: {inconsistencies}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"resource_witness: all_ok={all_ok}", flush=True)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
