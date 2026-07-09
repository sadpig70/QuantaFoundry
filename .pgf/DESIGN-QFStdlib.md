# QFStdlib Design @v:0.1

> 목적: QuantaFoundry의 sealed registry를 외부 사용자가 바로 소비할 수 있는 "검증된 양자 표준 라이브러리" 계층으로 승격한다.
> 이 설계는 새 봉인을 만들지 않는다. 기존 registry 위에 Canon, Import, Proof-Carrying Template sidecar를 얹는다.

## Current Facts

- Source proposal: `_workspace/upgrade-design/qf-stdlib-proposal.md`
- Authoritative live registry at design time: `registry/REGISTRY-MANIFEST.json`
- Current manifest snapshot: 95 modules / 475 unique apps / 550 app files / 75 cached leaf-module files
- Current root anchor: `d177ce9a438a1b2f6a9f9f042e69f5263267148fb3f90930fe611e8ec0a48af7`
- Semantic layer: `registry/SEMANTIC-GUARANTEES.json`
- Existing non-destructive precedent: `semantic_guarantee.py` and generated sidecar JSONs
- Operating invariant: oracle, sealed JSON, fingerprint files, frozen keys, and registry root are consumed, not modified by stdlib.

## Gantree

```text
QFStdlib // verified stdlib layer over the sealed QuantaFoundry registry (done) @v:0.1
    Grounding // current-state and trust-boundary grounding (done)
        RegistrySnapshot // manifest/semantic/dependency facts loaded from current files (done)
            # input: registry/REGISTRY-MANIFEST.json, SEMANTIC-GUARANTEES.json, DEPENDENCY-GRAPH.json
            # output: implementation uses live files, not hard-coded proposal counts
            # criteria: no stale README/proposal count is treated as authority
        NonDestructivePolicy // sidecar-only policy for stdlib (done)
            # rule: no verify_seal mutation, no sealed.json rewrite, no registry root recomputation as a side effect
            # criteria: generated files are additive or reproducible from current registry
    Canon // canonical primitive naming and citation layer (done) @dep:Grounding
        CanonSchema // registry/CANON.json schema and invariants (done)
            # output: schema for primitive_key -> canonical registry object
            # criteria: every canon entry resolves to exactly one sealed module/app and semantic guarantee
        CanonFamilyRules // deterministic family grouping and selection rules (done) @dep:CanonSchema
            # process: classify ids by exact regex/rules, then select by guarantee rank, n_sys scope, resource, stable id
            # criteria: no AI judgement in selection; override reasons explicit
        CanonValidator // deterministic validator for CANON.json (done) @dep:CanonSchema
            # output: scripts/qf_stdlib.py validate-canon
            # criteria: missing id/hash/root/semantic mismatch fails closed
        SeedCanonCatalog // minimal canonical palette v0 (done) @dep:CanonFamilyRules
            # scope: qft/iqft, adder, grover, qpe, trotter, qsp/qsvt, qrom/select-prepare, qec/code, shor-frontier
            # criteria: high-value coverage without pretending every sealed app is stdlib
    Import // lookup and attestation adapter layer (done) @dep:Canon
        InternalLookup // id/u_hash/alias lookup over Canon + registry (done)
            # output: qf_stdlib.lookup(name_or_hash) -> CanonEntry | None
            # criteria: unknown returns None, never nearest-match attestation
        AttestationModel // proof object schema emitted by lookups (done) @dep:InternalLookup
            # output: Attestation JSON with root, id, kind, u_hash, tier, semantic_guarantee, resource, dependencies
            # criteria: self-contained enough for third-party registry-root reproduction
        CircuitHashAdapters // optional external-circuit canonical hash adapters (blocked) #DEFERRED
            # initial: Cirq/PennyLane optional; Qiskit deferred unless dependency added
            # criteria: unsupported framework raises explicit unsupported_framework, not silent approximate hash
        SubcircuitMatcher // bounded exact subcircuit lookup for small circuits (blocked) @dep:CircuitHashAdapters #DEFERRED
            # scope: n_sys <= exact dense bound only, no structural dense materialization
            # criteria: exact hash equality only
    Template // proof-carrying assembly recipes (done) @dep:Canon,Import
        TemplateSchema // recipe schema over canon primitives and assembly grammar (done)
            # output: qf_stdlib/templates/*.json
            # criteria: every primitive reference resolves through Canon
        ExactCertPropagate // exact composition certificate propagation (done) @dep:TemplateSchema
            # process: child attestations + assembly plan -> composite structural certificate
            # criteria: exact children propagate exact/structural class honestly; no dense claim without dense gate
        ApproxCertPropagate // approximation and observation boundary propagation (done) @dep:TemplateSchema
            # process: optional epsilon metadata -> monotone bound; observations stay observations
            # criteria: approximation != exact, backend observation != seal
        RecipeCatalogV0 // first recipes for adoption and FT-compiler motivation (done) @dep:ExactCertPropagate,ApproxCertPropagate
            # recipes: qft_import, qpe_skeleton, trotter_stack, qsvt_consumer, shor_modexp_attest
            # criteria: each recipe produces circuit plan + certificate or fails closed
    Packaging // user-facing import surface and docs (done) @dep:Import,Template
        PythonPackageLayout // qf_stdlib package layout (done)
            # output: qf_stdlib/{canon,registry,attest,adapters,templates}.py
            # criteria: importable without heavy optional quantum frameworks for lookup-only mode
        CLISurface // qf-stdlib command surface (done) @dep:PythonPackageLayout
            # commands: canon, lookup, attest, build-template, validate
            # criteria: every command read-only by default
        DemoImporter // minimal demo: import QF-attested QFT (done) @dep:CLISurface
            # output: docs or notebooks showing lookup and attestation
            # criteria: demo uses current root and fails if root drifts unexpectedly
        Docs // honest public docs (done) @dep:DemoImporter
            # criteria: "stdlib attaches proof; it does not make arbitrary circuits correct"
    Verification // gates for design and implementation (done)
        StaticValidation // schema, reference, and hash validation (done)
            # commands: python scripts/qf_stdlib.py validate-canon; validate-templates
            # criteria: deterministic output, non-zero exit on mismatch
        NonMutationGate // guard against registry/oracle mutation (done)
            # process: hash selected oracle/fingerprint files and registry manifests before/after
            # criteria: stdlib commands do not change registry root or sealed artifacts
        GoldenLookupTests // lookup/attest positive and negative tests (done)
            # positive: qft8_pipeline, iqft8, grover2, qsvt_proj_d3
            # negative: wrong hash, stale root, unknown alias, unsupported framework
            # criteria: false attestation impossible under tested cases
        ArchitectureReview // PGF 3-view review before implementation completion (done)
            # acceptance: design nodes map to files/tests; quality: no over-abstraction; architecture: sidecar-only boundary held
    PGXFBoundary // index policy if the design grows beyond one file (done)
        NodeBudget // use PGXF only if QFStdlib exceeds 30 nodes or decomposes (done)
            # criteria: current design stays single-file; no .pgxf artifact required now
```

## PPR

```python
CanonEntry = dict[
    "key": str,
    "kind": Literal["module", "app"],
    "id": str,
    "u_hash": str,
    "registry_path": str,
    "registry_root": str,
    "tier": int,
    "semantic_guarantee": str,
    "resource": dict,
    "aliases": list[str],
    "convention": str,
    "selection": dict,
    "dependencies": list[dict],
    "honesty_scope": str,
]

Attestation = dict[
    "schema": Literal["qf-attestation-v1"],
    "subject": dict,
    "claim": dict,
    "anchor": dict,
    "proof": dict,
    "limits": list[str],
]

TemplateCert = dict[
    "schema": Literal["qf-template-cert-v1"],
    "template_id": str,
    "steps": list[Attestation],
    "composition_claim": dict,
    "root_anchor": str,
    "limits": list[str],
]
```

```python
def load_registry_snapshot(root: Path) -> RegistrySnapshot:
    """Load manifest, semantic guarantees, dependency graph, and sealed JSON objects."""
    manifest = json_load(root / "registry/REGISTRY-MANIFEST.json")
    semantic = json_load(root / "registry/SEMANTIC-GUARANTEES.json")
    graph = json_load(root / "registry/DEPENDENCY-GRAPH.json")
    sealed = load_all_sealed(root / "registry/modules", root / "registry/apps")
    return RegistrySnapshot(manifest=manifest, semantic=semantic, graph=graph, sealed=sealed)
    # acceptance_criteria:
    #   - registry_root_hash is present
    #   - module/app counts are read live
    #   - cached app-side module files are not treated as unique stdlib apps
```

```python
def build_canon(snapshot: RegistrySnapshot, rules: CanonRules, overrides: dict) -> dict[str, CanonEntry]:
    """Build deterministic primitive canon from live registry and explicit override rules."""
    candidates = group_by_family(snapshot.sealed, rules.family_patterns)
    canon = {}
    for key, items in sorted(candidates.items()):
        ranked = sorted(items, key=lambda item: (
            -guarantee_rank(snapshot.semantic[item.ref]),
            item.n_sys,
            total_resource_cost(item.resource),
            item.id,
        ))
        selected = apply_override_or_default(key, ranked, overrides)
        canon[key] = make_canon_entry(selected, snapshot)
    validate_canon(canon, snapshot)
    return canon
    # acceptance_criteria:
    #   - same snapshot + same rules -> byte-stable CANON.json
    #   - every selected u_hash equals sealed JSON u_hash
    #   - override requires reason and still validates
```

```python
def validate_canon(canon: dict[str, CanonEntry], snapshot: RegistrySnapshot) -> ValidationReport:
    """Fail closed on any dangling, stale, or overclaimed canon entry."""
    errors = []
    seen_aliases = set()
    for key, entry in canon.items():
        sealed = snapshot.resolve(entry["kind"], entry["id"])
        if sealed is None:
            errors.append(("missing_seal", key))
            continue
        if entry["u_hash"] != sealed["u_hash"]:
            errors.append(("u_hash_mismatch", key))
        if entry["registry_root"] != snapshot.manifest["registry_root_hash"]:
            errors.append(("root_mismatch", key))
        sem = snapshot.semantic["guarantees"].get(f"{entry['kind']}:{entry['id']}")
        if sem is None or sem["semantic_guarantee"] != entry["semantic_guarantee"]:
            errors.append(("semantic_mismatch", key))
        for alias in entry.get("aliases", []):
            if alias in seen_aliases:
                errors.append(("alias_collision", alias))
            seen_aliases.add(alias)
    return ValidationReport(ok=not errors, errors=errors)
    # acceptance_criteria:
    #   - invalid canon exits non-zero in CLI
    #   - no warning-only mismatch for proof-bearing fields
```

```python
def qf_lookup(query: str, canon: dict[str, CanonEntry]) -> Optional[CanonEntry]:
    """Lookup by canon key, alias, id, or exact u_hash."""
    indexes = build_lookup_indexes(canon)
    return indexes.by_key.get(query) or indexes.by_alias.get(query) or indexes.by_id.get(query) or indexes.by_hash.get(query)
    # acceptance_criteria:
    #   - exact match only
    #   - ambiguous alias fails validation before lookup
    #   - unknown query returns None
```

```python
def qf_attest(query_or_circuit: object, adapter: str | None, canon: dict[str, CanonEntry]) -> Optional[Attestation]:
    """Emit an attestation if the subject exactly matches a canonical sealed primitive."""
    if adapter is None:
        entry = qf_lookup(str(query_or_circuit), canon)
    else:
        u_hash = canonical_hash_with_adapter(query_or_circuit, adapter)
        entry = qf_lookup(u_hash, canon)
    if entry is None:
        return None
    return {
        "schema": "qf-attestation-v1",
        "subject": {"kind": entry["kind"], "id": entry["id"], "u_hash": entry["u_hash"]},
        "claim": {"semantic_guarantee": entry["semantic_guarantee"], "tier": entry["tier"], "resource": entry["resource"]},
        "anchor": {"registry_root": entry["registry_root"], "registry_path": entry["registry_path"]},
        "proof": {"dependencies": entry["dependencies"], "selection": entry["selection"]},
        "limits": [entry["honesty_scope"]],
    }
    # acceptance_criteria:
    #   - no approximate matching
    #   - unsupported adapters fail with explicit exception
    #   - structural entries do not claim dense unitary equivalence
```

```python
def build_with_proof(plan: TemplatePlan, canon: dict[str, CanonEntry]) -> tuple[AssemblyPlan, TemplateCert]:
    """Assemble a proof-carrying template from canonical primitives."""
    attestations = []
    for step in plan.steps:
        att = qf_attest(step.primitive_key, adapter=None, canon=canon)
        if att is None:
            raise ValueError(f"unsealed_or_noncanonical_primitive:{step.primitive_key}")
        attestations.append(att)
    assembly = derive_assembly_plan(plan, attestations)
    cert = derive_template_cert(plan.template_id, assembly, attestations)
    validate_template_cert(cert)
    return assembly, cert
    # acceptance_criteria:
    #   - all template primitive refs resolve through Canon
    #   - exact composition, structural composition, and approximation scopes are separated
    #   - output certificate is a derived claim, not a new seal
```

## Artifact Plan

| Phase | Artifact | Write Class | Notes |
|---|---|---|---|
| 0 | `.pgf/DESIGN-QFStdlib.md` | design | This file |
| 1 | `registry/CANON.json` | generated sidecar | Root-anchored, rebuildable |
| 1 | `scripts/qf_stdlib.py` | implementation | CLI and validator, read-only by default |
| 1 | `reports/QF-STDLIB-CANON-REPORT.json` | generated report | Validation summary |
| 2 | `qf_stdlib/` | package | Lookup-only imports without optional circuit deps |
| 2 | `tests/test_qf_stdlib.py` | tests | Positive/negative lookup and validation |
| 3 | `qf_stdlib/templates/*.json` | recipe data | Proof-carrying template v0 |
| 3 | `docs/QF-STDLIB.md` | docs | Honest user-facing docs |
| 3 | `_workspace/upgrade-design/qf-stdlib-detailed-design.md` | design companion | Detailed execution notes |

## Canon v1 Schema

```json
{
  "_schema": "qf-canon-v1",
  "_generated_from": {
    "registry_manifest": "registry/REGISTRY-MANIFEST.json",
    "semantic_guarantees": "registry/SEMANTIC-GUARANTEES.json",
    "dependency_graph": "registry/DEPENDENCY-GRAPH.json",
    "registry_root_hash": "<live-root>"
  },
  "selection_rule": [
    "explicit_override_if_valid",
    "highest_semantic_guarantee_rank",
    "smallest_declared_scope",
    "lowest_total_resource_cost",
    "lexicographic_id_tiebreak"
  ],
  "canon": {
    "qft/8": {
      "kind": "app",
      "id": "qft8_pipeline",
      "u_hash": "<sealed-u_hash>",
      "registry_path": "registry/apps/qft8_pipeline.sealed.json",
      "tier": 0,
      "semantic_guarantee": "unitary_equiv",
      "aliases": ["fourier/qft/8", "qft8"],
      "convention": "qualtran-raw; big-endian; global-phase-tolerant hash",
      "resource": {},
      "dependencies": [],
      "selection": {"method": "explicit_seed", "reason": "largest sealed QFT pipeline"},
      "honesty_scope": "Tier-0 exact app seal; no hardware execution claim"
    }
  }
}
```

## Initial Canon Palette

Seed only primitives that a downstream user can name without reading the entire registry.

| Family | Initial keys | Candidate ids |
|---|---|---|
| Fourier | `qft/2..8`, `iqft/2`, `iqft/3`, `iqft/7`, `iqft/8` | `qft*_pipeline`, `iqft*` |
| Arithmetic | `adder/cuccaro/2`, `adder/cuccaro/3`, modular multiply keys | `cuccaro_add*`, `cmul*_mod*` |
| Search | `grover/2`, `grover/3`, iteration variants | `grover*`, `diffusion*` |
| Phase estimation | `qpe/s`, `qpe/t` | `qpe_s`, `qpe_t` |
| Hamiltonian simulation | `trotter/tfim*`, `suzuki4/tfim*` | `tfim*_trotter*`, `tfim*_suzuki4*` |
| QSP/QSVT | `qsp/d1`, `qsp/d3`, `qsp/d5`, `qsvt/*` | `qsp_*`, `qsvt_*`, `be_*` |
| Data oracle | `qrom/2x2`, `select-prepare/4` | `qrom22`, `select_prepare4` |
| Codes/FTQC | code preparation and logical gates | `code*`, `steane_*`, `rm15_*`, `surf*` |
| Shor frontier | attest only, structural/subspace scoped | `shor*`, `cmul*_mod*` |

## Verification Gates

```bash
python scripts/qf_stdlib.py validate-canon
python scripts/qf_stdlib.py lookup qft/8
python scripts/qf_stdlib.py attest qft/8 --json
python scripts/qf_stdlib.py validate-template qpe_skeleton
python -m unittest tests.test_qf_stdlib -v
python scripts/reproduce_all.py --changed-only
```

Expected gate properties:

- `validate-canon` checks schema, root, id, path, u_hash, semantic guarantee, dependencies, aliases.
- `lookup` and `attest` never write.
- Template validation writes only reports when explicitly requested.
- `reproduce_all.py --changed-only` remains `REPRODUCED`; stdlib sidecars must not force new seals.

## Honesty Rules

- Canon is a citation layer, not a new oracle.
- Attestation is a lookup proof, not a re-verification proof.
- Template certificates are derived certificates, not sealed artifacts.
- Structural and subspace guarantees must keep their exact scope.
- Observation-only evidence cannot be promoted by stdlib.
- Qiskit support is deferred unless the dependency is added explicitly; Cirq/PennyLane can be optional adapters because the current lock already contains them.

## Implementation Order

1. Add `scripts/qf_stdlib.py` with snapshot loading, schema validation, and lookup indexes.
2. Generate and validate a small `registry/CANON.json` seed manually or deterministically from rules.
3. Add `qf_stdlib/` package with read-only `load_canon`, `lookup`, and `attest`.
4. Add tests for root mismatch, hash mismatch, alias collision, unknown query, and structural honesty.
5. Add template schema and two minimal recipes: `qft_import` and `qpe_skeleton`.
6. Add proof-carrying template propagation.
7. Add optional circuit adapters after lookup-only mode is stable.
8. Add docs and demo.

## PGXF Decision

Current QFStdlib design is intentionally one PGF file. PGXF becomes load-bearing only if:

- QFStdlib exceeds 30 nodes,
- template catalog becomes decomposed into several PGF files,
- status aggregation across implementation workplans becomes hard to inspect.

Until then, PGF design + direct `rg` lookup is simpler and sufficient.
