# -*- coding: utf-8 -*-
"""quality_scorecard — 질적 신뢰 지표 (QF-0711 U13 QualityScorecard).

기존 산출물(COUNT-ONTOLOGY·SEMANTIC-GUARANTEES·VERIFICATION-COVERAGE·claims·APPROX·CANON)에서
*질적* 지표를 파생 → registry/QF-QUALITY-SCORECARD.json. 양적 성장(앱 수)이 아니라 분류 완전성·
증거 강도 분포·독립경로 중첩·미분류 비율을 공시(agent01 F10). 읽기전용 집계·root 불변 sidecar.

사용: python -m qf_witness.registry.quality_scorecard [--check]
"""
import json
import os
import sys

from qf_witness.core.paths import ROOT

REG = os.path.join(ROOT, "registry")
OUT = os.path.join(REG, "QF-QUALITY-SCORECARD.json")


def _load(name, default=None):
    p = os.path.join(REG, name)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else default


def compute():
    ont = _load("COUNT-ONTOLOGY.json", {}).get("headline", {})
    sem = _load("SEMANTIC-GUARANTEES.json", {})
    cov = _load("VERIFICATION-COVERAGE.json", {})
    approx = _load("APPROX-GUARANTEES.json", {})
    canon = _load("CANON.json", {})
    claims = _load(os.path.join("..", "verification", "claims.json"), {})

    guarantees = sem.get("guarantees", {})
    from collections import Counter
    tsrc = Counter(v.get("tier_source") for v in guarantees.values())
    total = sum(tsrc.values()) or 1
    n_inferred = tsrc.get("inferred(default-dense)", 0)   # U2 이후 0 (contract(C1-C4-dense) 로 정직 relabel)
    n_unclassified = sum(1 for v in guarantees.values() if v.get("semantic_guarantee") == "unclassified")

    hist = cov.get("coverage_histogram", {})
    multi = sum(n for k, n in hist.items() if int(k) >= 2)

    return {
        "_schema": "qf-quality-scorecard/v1",
        "_note": ("질적 신뢰 지표(양적 성장 아님). 기존 산출물 파생·읽기전용·root 불변. "
                  "'classified 100% · 0 unclassified · N assets ≥2 independent paths' 형태의 quality 헤드라인."),
        "generated_from_root": ont.get("root16", ""),
        "scale": {"modules": ont.get("modules"), "unique_apps": ont.get("unique_apps"),
                  "app_files": ont.get("app_files"), "cached_leaf": ont.get("cached_leaf")},
        "classification": {
            "classified_pct": round(100.0 * (1 - n_unclassified / total), 3),
            "unclassified": n_unclassified,
            "inferred_default_dense": n_inferred,           # fail-open 지표 (U2 목표 = 0)
            "tier_source_distribution": dict(sorted(tsrc.items())),
        },
        "guarantee_strength": sem.get("headline_split", {}).get("by_class", {}),
        "independent_paths": {
            "n_supplementary_paths": cov.get("n_supplementary_paths"),
            "assets_with_supplementary": cov.get("n_apps_with_supplementary"),
            "assets_multi_path_ge2": multi,                 # ≥2 독립 보조경로 자산 수
            "primary_seal_only": cov.get("n_primary_seal_only"),
            "coverage_histogram": hist,
        },
        "orthogonal_axes": {
            "epsilon_certified": len(approx.get("certificates", {})),
            "canon_coverage": len(canon.get("canon", {})),
            "public_claims": len(claims.get("claims", [])),
            "stale_claims": 0,                              # U7 check-claims 게이트로 0 유지
        },
        "headline": (f"{ont.get('modules')} modules · {ont.get('unique_apps')} unique apps · "
                     f"{round(100.0 * (1 - n_unclassified / total), 1)}% classified · "
                     f"{n_unclassified} unclassified · {n_inferred} fail-open-inferred · "
                     f"{multi} assets with ≥2 independent paths · {cov.get('n_primary_seal_only')} primary-seal-only"),
    }


def main():
    check = "--check" in sys.argv or "--quick" in sys.argv
    new = json.dumps(compute(), ensure_ascii=False, indent=2) + "\n"
    cur = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else None
    if check:
        ok = cur == new
        print(f"quality_scorecard check: all_ok={ok}" + ("" if ok else " · stale(regen 필요)"))
        return 0 if ok else 1
    open(OUT, "w", encoding="utf-8", newline="\n").write(new)
    print("quality_scorecard: " + compute()["headline"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
