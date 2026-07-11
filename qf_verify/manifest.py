# -*- coding: utf-8 -*-
"""manifest — JSON manifest 로더 + 자체 스키마 검증 + witness_batch 전개 (INV-RA4: 외부 라이브러리 0).

manifest 스키마 (qf-verification-manifest/v1):
  {"schema": "...", "group": "...",
   "steps": [ {"id","title","argv","expectations",("special"),("claims"),("severity")...} ... ],
   "witness_batch": {"expectations": {...}, "severity": "...", "steps": [{"id","argv"}...]} }
witness_batch 는 로드 시 개별 스텝으로 전개(공통 expectation 상속) — manifest 비대화 방지.

profile 스키마 (qf-verification-profile/v1):
  {"schema": "...", "id": "full|changed", "manifests": ["core","witness","behavior"],
   "changed_only": bool}
"""
import os
import json

from . import context as cx

MANIFEST_DIR = os.path.join(cx.ROOT, "verification", "manifests")
PROFILE_DIR = os.path.join(cx.ROOT, "verification", "profiles")

_STEP_REQUIRED = ("id",)          # special 스텝은 argv 불요
_VALID_KEYS = {"id", "title", "argv", "expectations", "special", "claims",
               "severity", "cost", "report_key", "inputs"}


class ManifestError(Exception):
    pass


def _check_step(st, src):
    for k in _STEP_REQUIRED:
        if k not in st:
            raise ManifestError(f"{src}: step missing '{k}': {st}")
    unknown = set(st) - _VALID_KEYS
    if unknown:
        raise ManifestError(f"{src}: step '{st['id']}' unknown keys {sorted(unknown)}")
    if "special" not in st and "argv" not in st:
        raise ManifestError(f"{src}: step '{st['id']}' needs argv or special")
    if "special" not in st and "expectations" not in st:
        raise ManifestError(f"{src}: step '{st['id']}' needs expectations")


def load_manifest(name):
    """단일 manifest 로드 → 전개된 스텝 리스트(순서 보존)."""
    path = os.path.join(MANIFEST_DIR, f"{name}.json")
    doc = json.load(open(path, encoding="utf-8"))
    if doc.get("schema") != "qf-verification-manifest/v1":
        raise ManifestError(f"{name}: bad schema {doc.get('schema')!r}")
    steps = []
    for st in doc.get("steps", []):
        _check_step(st, name)
        steps.append(dict(st, _group=doc.get("group", name)))
    wb = doc.get("witness_batch")
    if wb:
        exp = wb["expectations"]
        for st in wb["steps"]:
            merged = {"id": st["id"], "argv": st["argv"], "expectations": exp,
                      "severity": wb.get("severity", "high"),
                      "claims": st.get("claims", wb.get("claims", []))}
            if "inputs" in st:
                merged["inputs"] = st["inputs"]
            _check_step(merged, name)
            merged["_group"] = doc.get("group", name)
            steps.append(merged)
    ids = [s["id"] for s in steps]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        raise ManifestError(f"{name}: duplicate step ids {sorted(dup)}")
    return steps


def load_profile(profile_id):
    """profile 로드 → (steps 전체 순서 리스트, changed_only)."""
    path = os.path.join(PROFILE_DIR, f"{profile_id}.json")
    doc = json.load(open(path, encoding="utf-8"))
    if doc.get("schema") != "qf-verification-profile/v1":
        raise ManifestError(f"profile {profile_id}: bad schema")
    steps = []
    for name in doc["manifests"]:
        steps.extend(load_manifest(name))
    all_ids = [s["id"] for s in steps]
    dup = {i for i in all_ids if all_ids.count(i) > 1}
    if dup:
        raise ManifestError(f"profile {profile_id}: duplicate ids across manifests {sorted(dup)}")
    return steps, bool(doc.get("changed_only", False))
