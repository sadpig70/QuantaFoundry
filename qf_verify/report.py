# -*- coding: utf-8 -*-
"""report — REPRODUCE-RESULT.json (legacy 형식, INV-RA2) + EVIDENCE-REPORT.json (가산)."""
import os
import json

from . import context as cx

RESULT_PATH = os.path.join(cx.REPORTS, "REPRODUCE-RESULT.json")
EVIDENCE_PATH = os.path.join(cx.REPORTS, "EVIDENCE-REPORT.json")


def write_reproduce_result(result):
    """legacy 와 동일한 직렬화 (ensure_ascii=False, indent=2)."""
    os.makedirs(cx.REPORTS, exist_ok=True)
    json.dump(result, open(RESULT_PATH, "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)


def write_evidence_report(profile_id, result, evidence):
    """신규 상세 리포트 — severity/duration/claims/그룹 동반 (결정론 무관 부가 정보)."""
    os.makedirs(cx.REPORTS, exist_ok=True)
    sev_failed = {}
    claims_status = {}
    for e in evidence:
        if e["status"] != "pass":
            sev_failed[e["severity"]] = sev_failed.get(e["severity"], 0) + 1
        for c in e.get("claims", []):
            cur = claims_status.setdefault(c, {"status": "pass", "evidence_steps": []})
            cur["evidence_steps"].append(e["id"])
            if e["status"] != "pass":
                cur["status"] = "fail"
    doc = {
        "schema": "qf-evidence-report/v1",
        "run": {"profile": profile_id, "mode": result.get("mode"),
                "bundle": result.get("bundle")},
        "summary": {
            "status": "pass" if result.get("bundle") == "REPRODUCED" else "fail",
            "steps_total": len(evidence),
            "steps_failed": sum(1 for e in evidence if e["status"] != "pass"),
            "failed_by_severity": sev_failed,
            "duration_ms": sum(e.get("duration_ms", 0) for e in evidence),
        },
        "steps": evidence,
        "claims": claims_status,
        "_note": "가산 리포트 — 정본 판정은 REPRODUCE-RESULT.json(REPRODUCED ≠ correct, INV-R1). "
                 "실패 시 어떤 claim 이 무효화되는지 claims 필드가 표시한다.",
    }
    json.dump(doc, open(EVIDENCE_PATH, "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
