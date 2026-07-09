"""Proof-carrying recipe templates over canonical QF entries."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .attest import attest
from .canon import load_canon
from .errors import ValidationError
from .registry import ROOT, json_load


TEMPLATE_SCHEMA = "qf-template-v1"
TEMPLATE_CERT_SCHEMA = "qf-template-cert-v1"


def template_dir(root: Path | None = None) -> Path:
    repo = root or ROOT
    return repo / "qf_stdlib" / "templates"


def load_template(template_id: str, root: Path | None = None) -> dict[str, Any]:
    path = template_dir(root) / f"{template_id}.json"
    return json_load(path)


def validate_template(template: dict[str, Any], canon: dict[str, Any] | None = None, root: Path | None = None) -> list[str]:
    errors: list[str] = []
    if template.get("schema") != TEMPLATE_SCHEMA:
        errors.append("invalid_template_schema")
    if not template.get("template_id"):
        errors.append("missing_template_id")
    data = canon or load_canon(root)
    for req in template.get("requires", []):
        key = req.get("canon_key")
        if not key:
            errors.append("requirement_missing_canon_key")
            continue
        if attest(key, canon=data, root=root) is None:
            errors.append(f"unresolved_canon_key:{key}")
    return errors


def build_with_proof(template_id: str, canon: dict[str, Any] | None = None, root: Path | None = None) -> dict[str, Any]:
    data = canon or load_canon(root)
    template = load_template(template_id, root=root)
    errors = validate_template(template, canon=data, root=root)
    if errors:
        raise ValidationError("; ".join(errors))
    step_attestations = []
    for req in template.get("requires", []):
        att = attest(req["canon_key"], canon=data, root=root)
        if att is None:
            raise ValidationError(f"unresolved_canon_key:{req['canon_key']}")
        step_attestations.append({"name": req["name"], "role": req.get("role", ""), "attestation": att})
    guarantees = {s["attestation"]["claim"]["semantic_guarantee"] for s in step_attestations}
    if guarantees == {"unitary_equiv"}:
        scope = "all referenced primitives are exact registry entries; template certificate remains derived, not sealed"
    else:
        scope = "mixed guarantees; see per-step limits and template certificate_rule"
    return {
        "schema": TEMPLATE_CERT_SCHEMA,
        "template_id": template["template_id"],
        "description": template.get("description", ""),
        "steps": step_attestations,
        "assembly": template.get("assembly", []),
        "composition_claim": {
            "type": template.get("certificate_rule", {}).get("type", "derived_composition"),
            "scope": scope,
            "rule": template.get("certificate_rule", {}),
        },
        "root_anchor": data["_generated_from"]["registry_root_hash"],
        "limits": template.get("limits", []) + [
            "This is a derived template certificate, not a sealed registry artifact."
        ],
    }

