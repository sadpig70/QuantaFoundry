# -*- coding: utf-8 -*-
"""
resource_report.py — P4 ResourceReport (task_plan_pg §P4)

봉인 시 오라클이 기록한 resource(qec-gates-cost-v1: total_t/clifford/toffoli/and_bloq/…)를
registry 전수 집계해 FTQC 실예산(T-count·폭·게이트 구성)을 산출한다. 봉인의 산업적 화폐.

sub-PG:
    ResourceAggregator // registry/modules·apps 전 sealed.json resource 결정론 집계
    CostAwareNote      // 동일 u_hash 다후보 시 최소 total_t 선택 정책(분석/문서, 봉인경로 미적용)

정직성:
 - 분석전용 비파괴 레이어 — sealed.json/oracle/frozen 불변. resource 는 오라클이 봉인 시
   기록한 값(재계산 아님) → 근거 있는 집계.
 - app-side 재봉인 캐시(module∩app id) 중복은 namespace 분리로 정직 처리(이중계상 방지).
"""
from __future__ import annotations

import os
import sys
import json
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODREG = os.path.join(ROOT, "registry", "modules")
APPREG = os.path.join(ROOT, "registry", "apps")
SPECS_APPS = os.path.join(ROOT, "specs", "apps")
OUT = os.path.join(ROOT, ".pgf", "resource")

RES_KEYS = ["total_t", "t", "toffoli", "clifford", "and_bloq", "cswap", "rotation", "measurement"]


def _load(path):
    d = json.load(open(path, encoding="utf-8"))
    return {"id": d["id"], "n_sys": d.get("n_sys"), "tier": d.get("tier"),
            "u_hash": d.get("u_hash"), "resource": d.get("resource", {}),
            "schema": d.get("resource_schema_version")}


def _is_unique_app(aid):
    """registry/apps 항목이 진짜 앱(spec 존재)인가 — 아니면 module 재봉인 캐시."""
    return os.path.exists(os.path.join(SPECS_APPS, f"{aid}.app.pg"))


def aggregate(paths, label, filt=None):
    items = []
    for p in sorted(paths):
        it = _load(p)
        if filt and not filt(it["id"]):
            continue
        items.append(it)
    totals = {k: 0 for k in RES_KEYS}
    for it in items:
        for k in RES_KEYS:
            totals[k] += int(it["resource"].get(k, 0))
    # top consumers by total_t
    top = sorted(items, key=lambda x: -int(x["resource"].get("total_t", 0)))[:8]
    return {
        "namespace": label,
        "count": len(items),
        "totals": totals,
        "max_qubit_width": max((it["n_sys"] or 0 for it in items), default=0),
        "top_total_t": [{"id": it["id"], "n_sys": it["n_sys"], "tier": it["tier"],
                         "total_t": int(it["resource"].get("total_t", 0)),
                         "toffoli": int(it["resource"].get("toffoli", 0)),
                         "clifford": int(it["resource"].get("clifford", 0))} for it in top],
        "zero_t_count": sum(1 for it in items if int(it["resource"].get("total_t", 0)) == 0),
    }


def cost_aware_note(mod_items, app_items):
    """동일 u_hash 다후보 탐지 → 최소 total_t 선택 정책 예시(분석/문서, 봉인 미적용)."""
    by_hash = {}
    for it in mod_items + app_items:
        by_hash.setdefault(it["u_hash"], []).append(it)
    multi = {h: v for h, v in by_hash.items() if len(v) > 1}
    examples = []
    for h, cands in list(multi.items())[:6]:
        ranked = sorted(cands, key=lambda x: int(x["resource"].get("total_t", 0)))
        examples.append({
            "u_hash": (h or "")[:14],
            "candidates": [{"id": c["id"], "total_t": int(c["resource"].get("total_t", 0))}
                           for c in ranked],
            "cost_aware_choice": ranked[0]["id"],
        })
    return {
        "policy": "동일 u_hash(=동일 유니터리) 다후보 존재 시 최소 total_t 회로 선택 봉인 권장. "
                  "분석/문서 전용 — 봉인경로 미적용(결정론 보존). 동일 u_hash 후보군은 보통 "
                  "module↔app 재봉인 캐시(같은 합성)이며, 진짜 다른 회로의 동일 u_hash 시 의미 발생.",
        "shared_u_hash_groups": len(multi),
        "examples": examples,
    }


def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 70)
    print("P4 ResourceReport — registry FTQC 실예산 집계 (qec-gates-cost-v1)")
    print("정직성: 분석전용 비파괴. resource=오라클 봉인시 기록값(재계산 아님).")
    print("=" * 70)

    mod_paths = glob.glob(os.path.join(MODREG, "*.sealed.json"))
    app_paths = glob.glob(os.path.join(APPREG, "*.sealed.json"))
    mod_items = [_load(p) for p in mod_paths]
    app_items_all = [_load(p) for p in app_paths]
    app_items_unique = [it for it in app_items_all if _is_unique_app(it["id"])]

    modules = aggregate(mod_paths, "modules")
    apps = aggregate([p for p in app_paths
                      if _is_unique_app(os.path.basename(p).replace(".sealed.json", ""))],
                     "apps (unique, 재봉인 캐시 제외)")
    note = cost_aware_note(mod_items, app_items_unique)

    print(f"[Modules] {modules['count']} · ΣT={modules['totals']['total_t']} · "
          f"max width={modules['max_qubit_width']}q · zero-T={modules['zero_t_count']}")
    print(f"[Apps]    {apps['count']} unique · ΣT={apps['totals']['total_t']} · "
          f"max width={apps['max_qubit_width']}q · zero-T={apps['zero_t_count']}")
    print(f"  (registry/apps 총 {len(app_items_all)} = unique {len(app_items_unique)} + "
          f"재봉인 캐시 {len(app_items_all)-len(app_items_unique)})")
    print("[Top T-count apps]")
    for t in apps["top_total_t"][:5]:
        print(f"   {t['id']:16} {t['n_sys']}q tier={t['tier']} T={t['total_t']} "
              f"toffoli={t['toffoli']} clifford={t['clifford']}")
    print(f"[CostAwareNote] 동일 u_hash 그룹 {note['shared_u_hash_groups']} "
          f"(최소 total_t 선택 정책, 분석전용)")

    report = {
        "phase": "P4 ResourceReport",
        "schema": "qec-gates-cost-v1",
        "honesty": "analysis-only non-destructive; resource values are oracle-recorded at seal "
                   "time (not re-derived); seals/oracle/frozen untouched; app re-seal caches "
                   "excluded from app totals (namespace split, no double-count).",
        "modules": modules,
        "apps_unique": apps,
        "registry_apps_total": len(app_items_all),
        "registry_apps_reseal_cache": len(app_items_all) - len(app_items_unique),
        "cost_aware_note": note,
    }
    json.dump(report, open(os.path.join(OUT, "RESOURCE-REPORT.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("-" * 70)
    print(f"→  .pgf/resource/RESOURCE-REPORT.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
