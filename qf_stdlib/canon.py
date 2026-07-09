"""Canonical stdlib surface over the sealed registry."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .errors import NotFoundError, ValidationError
from .registry import RegistrySnapshot, json_dump_stable, json_load, load_snapshot


CANON_SCHEMA = "qf-canon-v1"
REPORT_SCHEMA = "qf-stdlib-canon-report-v1"

SELECTION_RULE = [
    "explicit_seed_if_valid",
    "highest_semantic_guarantee_rank",
    "smallest_declared_scope",
    "lowest_total_resource_cost",
    "lexicographic_id_tiebreak",
]

HONESTY_LIMITS = [
    "seal != hardware run",
    "attestation is lookup, not new verification",
    "derived template certificates are not new sealed artifacts",
]

GUARANTEE_RANK = {
    "unitary_equiv": 50,
    "unitary_equiv_sampled": 40,
    "subspace_permutation_verified": 30,
    "structural_wellformed": 20,
}


SEED_ENTRIES: list[dict[str, Any]] = [
    {"key": "gate/x", "kind": "module", "id": "x_gate", "aliases": ["x", "pauli/x", "x_gate"], "reason": "canonical Pauli-X base gate"},
    {"key": "gate/z", "kind": "module", "id": "z_gate", "aliases": ["z", "pauli/z", "z_gate"], "reason": "canonical Pauli-Z base gate"},
    {"key": "gate/h", "kind": "module", "id": "h_gate", "aliases": ["h", "hadamard", "h_gate"], "reason": "canonical Hadamard base gate"},
    {"key": "gate/s", "kind": "module", "id": "s_gate", "aliases": ["s", "phase/s", "s_gate"], "reason": "canonical S phase base gate"},
    {"key": "gate/t", "kind": "module", "id": "t_gate", "aliases": ["t", "phase/t", "t_gate"], "reason": "canonical T phase base gate"},
    {"key": "gate/cnot", "kind": "module", "id": "cnot", "aliases": ["cnot", "cx"], "reason": "canonical controlled-X base gate"},
    {"key": "gate/swap", "kind": "module", "id": "swap2", "aliases": ["swap", "swap2"], "reason": "canonical two-qubit SWAP base gate"},
    {"key": "gate/cz", "kind": "module", "id": "cz", "aliases": ["cz", "controlled-z"], "reason": "canonical controlled-Z base gate"},
    {"key": "gate/toffoli", "kind": "module", "id": "toffoli", "aliases": ["toffoli", "ccx"], "reason": "canonical Toffoli base gate"},
    {"key": "gate/fredkin", "kind": "module", "id": "fredkin", "aliases": ["fredkin", "cswap"], "reason": "canonical Fredkin base gate"},
    {"key": "gate/cs", "kind": "module", "id": "cs_gate", "aliases": ["cs", "controlled-s", "cs_gate"], "reason": "canonical controlled-S base gate"},
    {"key": "gate/ct", "kind": "module", "id": "ct_gate", "aliases": ["ct", "controlled-t", "ct_gate"], "reason": "canonical controlled-T base gate"},
    {"key": "gate/ccz", "kind": "module", "id": "ccz", "aliases": ["ccz", "controlled-controlled-z"], "reason": "canonical controlled-controlled-Z base gate"},
    {"key": "qft/2", "kind": "app", "id": "qft2_pipeline", "aliases": ["qft2", "fourier/qft/2"], "reason": "small QFT pipeline"},
    {"key": "qft/3", "kind": "app", "id": "qft3_pipeline", "aliases": ["qft3", "fourier/qft/3"], "reason": "small QFT pipeline"},
    {"key": "qft/4", "kind": "app", "id": "qft4_pipeline", "aliases": ["qft4", "fourier/qft/4"], "reason": "baseline QFT pipeline"},
    {"key": "qft/5", "kind": "app", "id": "qft5_pipeline", "aliases": ["qft5", "fourier/qft/5"], "reason": "5-qubit QFT pipeline"},
    {"key": "qft/6", "kind": "app", "id": "qft6_pipeline", "aliases": ["qft6", "fourier/qft/6"], "reason": "6-qubit QFT pipeline"},
    {"key": "qft/7", "kind": "app", "id": "qft7_pipeline", "aliases": ["qft7", "fourier/qft/7"], "reason": "7-qubit QFT pipeline"},
    {"key": "qft/8", "kind": "app", "id": "qft8_pipeline", "aliases": ["qft8", "fourier/qft/8"], "reason": "largest sealed QFT pipeline"},
    {"key": "iqft/2", "kind": "app", "id": "iqft2", "aliases": ["iqft2", "fourier/iqft/2"], "reason": "small inverse QFT"},
    {"key": "iqft/3", "kind": "app", "id": "iqft3", "aliases": ["iqft3", "fourier/iqft/3"], "reason": "small inverse QFT"},
    {"key": "iqft/7", "kind": "app", "id": "iqft7", "aliases": ["iqft7", "fourier/iqft/7"], "reason": "7-qubit inverse QFT"},
    {"key": "iqft/8", "kind": "app", "id": "iqft8", "aliases": ["iqft8", "fourier/iqft/8"], "reason": "QPE-ready inverse QFT"},
    {"key": "adder/cuccaro/2", "kind": "app", "id": "cuccaro_add2", "aliases": ["cuccaro_add2"], "reason": "small canonical reversible adder"},
    {"key": "adder/cuccaro/3", "kind": "app", "id": "cuccaro_add3", "aliases": ["cuccaro_add3"], "reason": "larger canonical reversible adder"},
    {"key": "grover/search2/1iter", "kind": "app", "id": "grover2", "aliases": ["grover2"], "reason": "minimal Grover application"},
    {"key": "grover/search3/1iter", "kind": "app", "id": "grover3", "aliases": ["grover3"], "reason": "3-qubit Grover application"},
    {"key": "qpe/s", "kind": "app", "id": "qpe_s", "aliases": ["qpe_s"], "reason": "phase estimation over S gate"},
    {"key": "qpe/t", "kind": "app", "id": "qpe_t", "aliases": ["qpe_t"], "reason": "phase estimation over T gate"},
    {"key": "trotter/tfim3/first_order", "kind": "app", "id": "tfim3_trotter_step", "aliases": ["tfim3_trotter_step"], "reason": "canonical first-order TFIM step"},
    {"key": "suzuki4/tfim3/step", "kind": "app", "id": "tfim3_suzuki4_step", "aliases": ["tfim3_suzuki4_step"], "reason": "canonical fourth-order Suzuki TFIM step"},
    {"key": "block-encoding/xz", "kind": "app", "id": "be_xz", "aliases": ["be_xz"], "reason": "block-encoding seed for QSVT"},
    {"key": "block-encoding/proj", "kind": "app", "id": "be_proj", "aliases": ["be_proj"], "reason": "projector block-encoding seed for QSVT"},
    {"key": "block-encoding/pauli2", "kind": "app", "id": "be_pauli2", "aliases": ["be_pauli2"], "reason": "two-qubit Pauli block-encoding seed"},
    {"key": "block-encoding/h2", "kind": "app", "id": "be_h2", "aliases": ["be_h2"], "reason": "molecular block-encoding seed"},
    {"key": "block-encoding/hop", "kind": "app", "id": "be_hop", "aliases": ["be_hop"], "reason": "fermionic hopping block-encoding seed"},
    {"key": "block-encoding/num", "kind": "app", "id": "be_num", "aliases": ["be_num"], "reason": "fermionic number block-encoding seed"},
    {"key": "qsp/d1", "kind": "app", "id": "qsp_d1", "aliases": ["qsp_d1"], "reason": "degree-1 QSP primitive"},
    {"key": "qsp/d3", "kind": "app", "id": "qsp_d3", "aliases": ["qsp_d3"], "reason": "degree-3 QSP primitive"},
    {"key": "qsp/d5", "kind": "app", "id": "qsp_d5", "aliases": ["qsp_d5"], "reason": "degree-5 QSP primitive"},
    {"key": "qsvt/proj/d2", "kind": "app", "id": "qsvt_proj_d2", "aliases": ["qsvt_proj_d2"], "reason": "degree-2 projector QSVT consumer"},
    {"key": "qsvt/proj/d2b", "kind": "app", "id": "qsvt_proj_d2b", "aliases": ["qsvt_proj_d2b"], "reason": "alternate degree-2 projector QSVT consumer"},
    {"key": "qsvt/proj/d3", "kind": "app", "id": "qsvt_proj_d3", "aliases": ["qsvt_proj_d3"], "reason": "projector QSVT consumer"},
    {"key": "qsvt/pauli2/d2", "kind": "app", "id": "qsvt_pauli2_d2", "aliases": ["qsvt_pauli2_d2"], "reason": "degree-2 Pauli QSVT consumer"},
    {"key": "qsvt/pauli2/d3", "kind": "app", "id": "qsvt_pauli2_d3", "aliases": ["qsvt_pauli2_d3"], "reason": "degree-3 Pauli QSVT consumer"},
    {"key": "qrom/2x2", "kind": "app", "id": "qrom22", "aliases": ["qrom22"], "reason": "canonical qROM data oracle"},
    {"key": "select-prepare/4", "kind": "app", "id": "select_prepare4", "aliases": ["select_prepare4"], "reason": "canonical SELECT-PREPARE layer"},
    {"key": "code/rm15/encoder", "kind": "module", "id": "rm15_encoder_t2", "aliases": ["rm15_encoder_t2"], "reason": "punctured Reed-Muller encoder substrate"},
    {"key": "code/rm15/decoder", "kind": "module", "id": "rm15_decoder_t2", "aliases": ["rm15_decoder_t2"], "reason": "coherent RM15 decoder substrate"},
    {"key": "cmul/237/a2", "kind": "app", "id": "cmul2_mod237", "aliases": ["cmul2_mod237"], "reason": "frontier Shor-237 modular multiplier component"},
    {"key": "cmul/237/a4", "kind": "app", "id": "cmul4_mod237", "aliases": ["cmul4_mod237"], "reason": "frontier Shor-237 modular multiplier component"},
    {"key": "cmul/237/a16", "kind": "app", "id": "cmul16_mod237", "aliases": ["cmul16_mod237"], "reason": "frontier Shor-237 modular multiplier component"},
    {"key": "cmul/237/a124", "kind": "app", "id": "cmul124_mod237", "aliases": ["cmul124_mod237"], "reason": "frontier Shor-237 modular multiplier component"},
    {"key": "shor/237/structural", "kind": "app", "id": "shor237", "aliases": ["shor237"], "reason": "latest root-synced structural Shor frontier"},
]


@dataclass(frozen=True)
class ValidationReport:
    ok: bool
    errors: list[str]
    warnings: list[str]
    entries: int
    registry_root_hash: str

    def to_json(self) -> dict[str, Any]:
        return {
            "_schema": REPORT_SCHEMA,
            "ok": self.ok,
            "errors": self.errors,
            "warnings": self.warnings,
            "entries": self.entries,
            "registry_root_hash": self.registry_root_hash,
        }


def canon_path(root: Path) -> Path:
    return root / "registry" / "CANON.json"


def load_canon(root: Path | None = None) -> dict[str, Any]:
    snapshot = load_snapshot(root)
    return json_load(canon_path(snapshot.root))


def _tier(sealed: dict[str, Any], sem: dict[str, Any] | None) -> int:
    if sem and "tier" in sem:
        return int(sem["tier"])
    if sealed.get("tier") is None:
        return 0
    return int(sealed["tier"])


def _honesty_scope(semantic_guarantee: str, method: str) -> str:
    if semantic_guarantee == "unitary_equiv":
        return "Tier-0/Tier-2 exact registry guarantee as stated by semantic layer; no hardware execution claim"
    if semantic_guarantee == "unitary_equiv_sampled":
        return "Sampled dense equivalence only; not full dense unitary equivalence"
    if semantic_guarantee == "subspace_permutation_verified":
        return method
    if semantic_guarantee == "structural_wellformed":
        return "Structural Merkle/wiring guarantee only; not dense unitary equivalence"
    return "Unknown guarantee class; do not promote beyond registry semantic layer"


def _entry_from_seed(seed: dict[str, Any], snapshot: RegistrySnapshot) -> dict[str, Any]:
    kind = seed["kind"]
    ident = seed["id"]
    sealed = snapshot.resolve(kind, ident)
    if sealed is None:
        raise ValidationError(f"seed target missing: {kind}:{ident}")
    sem = snapshot.semantic_entry(kind, ident)
    if sem is None:
        raise ValidationError(f"semantic entry missing: {kind}:{ident}")
    rel_path = f"registry/{'modules' if kind == 'module' else 'apps'}/{ident}.sealed.json"
    guarantee = sem["semantic_guarantee"]
    method = sem.get("method", "")
    return {
        "aliases": sorted(set(seed.get("aliases", []))),
        "convention": sealed.get("convention", "qualtran-raw"),
        "dependencies": snapshot.dependencies(kind, ident),
        "honesty_scope": _honesty_scope(guarantee, method),
        "id": ident,
        "kind": kind,
        "n_sys": sealed.get("n_sys"),
        "registry_path": rel_path,
        "registry_root": snapshot.registry_root_hash,
        "resource": sealed.get("resource", {}),
        "selection": {"method": "explicit_seed", "reason": seed["reason"]},
        "semantic_guarantee": guarantee,
        "sig": sealed.get("sig"),
        "tier": _tier(sealed, sem),
        "u_hash": sealed["u_hash"],
    }


def build_canon(snapshot: RegistrySnapshot | None = None) -> dict[str, Any]:
    snap = snapshot or load_snapshot()
    canon = {seed["key"]: _entry_from_seed(seed, snap) for seed in SEED_ENTRIES}
    return {
        "_schema": CANON_SCHEMA,
        "_generated_from": {
            "dependency_graph": "registry/DEPENDENCY-GRAPH.json",
            "registry_manifest": "registry/REGISTRY-MANIFEST.json",
            "registry_root_hash": snap.registry_root_hash,
            "semantic_guarantees": "registry/SEMANTIC-GUARANTEES.json",
        },
        "_note": "Canonical user-facing stdlib surface. This sidecar creates no new seals and does not modify registry artifacts.",
        "selection_rule": SELECTION_RULE,
        "honesty_limits": HONESTY_LIMITS,
        "canon": dict(sorted(canon.items())),
    }


def _semantic_rank(guarantee: str) -> int:
    return GUARANTEE_RANK.get(guarantee, -1)


def validate_canon(canon: dict[str, Any], snapshot: RegistrySnapshot | None = None) -> ValidationReport:
    snap = snapshot or load_snapshot()
    errors: list[str] = []
    warnings: list[str] = []
    if canon.get("_schema") != CANON_SCHEMA:
        errors.append("invalid_schema")
    generated = canon.get("_generated_from", {})
    if generated.get("registry_root_hash") != snap.registry_root_hash:
        errors.append("generated_root_mismatch")
    entries = canon.get("canon")
    if not isinstance(entries, dict) or not entries:
        errors.append("canon_entries_missing")
        entries = {}

    seen_aliases: dict[str, str] = {}
    seen_hashes: dict[str, str] = {}
    for key, entry in sorted(entries.items()):
        for field in (
            "kind",
            "id",
            "u_hash",
            "registry_path",
            "registry_root",
            "tier",
            "semantic_guarantee",
            "aliases",
            "convention",
            "resource",
            "dependencies",
            "selection",
            "honesty_scope",
        ):
            if field not in entry:
                errors.append(f"{key}:missing_field:{field}")
        kind = entry.get("kind")
        ident = entry.get("id")
        if kind not in ("module", "app"):
            errors.append(f"{key}:invalid_kind:{kind}")
            continue
        if kind == "app" and ident in snap.cached_leaf_modules:
            errors.append(f"{key}:cached_leaf_module_exposed_as_app:{ident}")
        sealed = snap.resolve(kind, ident)
        if sealed is None:
            errors.append(f"{key}:missing_seal:{kind}:{ident}")
            continue
        if sealed.get("id") != ident:
            errors.append(f"{key}:sealed_id_mismatch")
        if entry.get("u_hash") != sealed.get("u_hash"):
            errors.append(f"{key}:u_hash_mismatch")
        if entry.get("registry_root") != snap.registry_root_hash:
            errors.append(f"{key}:root_mismatch")
        expected_rel = f"registry/{'modules' if kind == 'module' else 'apps'}/{ident}.sealed.json"
        if entry.get("registry_path") != expected_rel:
            errors.append(f"{key}:registry_path_mismatch")
        if not (snap.root / expected_rel).exists():
            errors.append(f"{key}:registry_path_missing")
        sem = snap.semantic_entry(kind, ident)
        if sem is None:
            errors.append(f"{key}:semantic_missing")
        else:
            if entry.get("semantic_guarantee") != sem.get("semantic_guarantee"):
                errors.append(f"{key}:semantic_guarantee_mismatch")
            if int(entry.get("tier", -999)) != _tier(sealed, sem):
                errors.append(f"{key}:tier_mismatch")
            if _semantic_rank(entry.get("semantic_guarantee", "")) < 0:
                errors.append(f"{key}:unknown_semantic_guarantee")
        if entry.get("semantic_guarantee") in ("structural_wellformed", "subspace_permutation_verified"):
            scope = str(entry.get("honesty_scope", "")).lower()
            if "unitary" in scope and "not" not in scope and "미검증" not in scope:
                errors.append(f"{key}:structural_scope_overclaim")
        for alias in entry.get("aliases", []):
            if alias in seen_aliases:
                errors.append(f"{key}:alias_collision:{alias}:with:{seen_aliases[alias]}")
            seen_aliases[alias] = key
        h = entry.get("u_hash")
        if h in seen_hashes and seen_hashes[h] != key:
            warnings.append(f"{key}:u_hash_also_exposed_by:{seen_hashes[h]}")
        seen_hashes[h] = key
    return ValidationReport(
        ok=not errors,
        errors=errors,
        warnings=warnings,
        entries=len(entries),
        registry_root_hash=snap.registry_root_hash,
    )


def check_root(canon: dict[str, Any], snapshot: RegistrySnapshot | None = None) -> ValidationReport:
    """Check only root drift between CANON.json and the live manifest."""
    snap = snapshot or load_snapshot()
    errors: list[str] = []
    generated = canon.get("_generated_from", {})
    if generated.get("registry_root_hash") != snap.registry_root_hash:
        errors.append("generated_root_mismatch")
    for key, entry in sorted(canon.get("canon", {}).items()):
        if entry.get("registry_root") != snap.registry_root_hash:
            errors.append(f"{key}:root_mismatch")
    return ValidationReport(
        ok=not errors,
        errors=errors,
        warnings=[],
        entries=len(canon.get("canon", {})),
        registry_root_hash=snap.registry_root_hash,
    )


def write_canon(root: Path | None = None) -> ValidationReport:
    snapshot = load_snapshot(root)
    canon = build_canon(snapshot)
    report = validate_canon(canon, snapshot)
    if not report.ok:
        raise ValidationError("; ".join(report.errors))
    json_dump_stable(canon, canon_path(snapshot.root))
    return report


def write_report(report: ValidationReport, root: Path | None = None) -> Path:
    snapshot = load_snapshot(root)
    path = snapshot.root / "reports" / "QF-STDLIB-CANON-REPORT.json"
    json_dump_stable(report.to_json(), path)
    return path


@dataclass(frozen=True)
class LookupIndexes:
    by_key: dict[str, dict[str, Any]]
    by_alias: dict[str, dict[str, Any]]
    by_id: dict[str, dict[str, Any]]
    by_hash: dict[str, dict[str, Any]]


def build_lookup_indexes(canon: dict[str, Any]) -> LookupIndexes:
    entries = canon.get("canon", {})
    by_key: dict[str, dict[str, Any]] = {}
    by_alias: dict[str, dict[str, Any]] = {}
    by_id: dict[str, dict[str, Any]] = {}
    by_hash: dict[str, dict[str, Any]] = {}
    for key, entry in entries.items():
        with_key = dict(entry)
        with_key["key"] = key
        by_key[key] = with_key
        by_id[entry["id"]] = with_key
        by_hash[entry["u_hash"]] = with_key
        for alias in entry.get("aliases", []):
            by_alias[alias] = with_key
    return LookupIndexes(by_key=by_key, by_alias=by_alias, by_id=by_id, by_hash=by_hash)


def lookup(query: str, canon: dict[str, Any] | None = None, root: Path | None = None) -> dict[str, Any] | None:
    data = canon or load_canon(root)
    indexes = build_lookup_indexes(data)
    return (
        indexes.by_key.get(query)
        or indexes.by_alias.get(query)
        or indexes.by_id.get(query)
        or indexes.by_hash.get(query)
    )


def require_lookup(query: str, canon: dict[str, Any] | None = None, root: Path | None = None) -> dict[str, Any]:
    entry = lookup(query, canon=canon, root=root)
    if entry is None:
        raise NotFoundError(query)
    return entry
