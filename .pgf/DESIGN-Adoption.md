# DESIGN-Adoption — Stage 3 Adoption-CI (신뢰자본 외부 소비화)

> PGF design mode · 기반 = `roadmap_process_plan.md` Stage 3 (Track C) · 방법 = PG Gantree + PPR.
> 정직성: 비파괴 가산. registry/sealed/frozen/fingerprint 불변. QASM round-trip 은 second_oracle
> 독립 numpy(INDEP+embed)로 검증 — 봉인 u_hash 재현이 export 정직성의 증명.
> 소비 자산(사용만): second_oracle(INDEP/embed/hash) · registry_tools(parse_plan_deps) ·
> resource_report(_load) · reproduce_all/verify_seal/app_assemble(CLI 래핑).

---

## 0. 문제 (8-agent 채택 수렴)

봉인 신뢰자본이 외부에서 *소비 불가*면 가치가 갇힌다. 채택 경로 = (1) sealed→OpenQASM3 export
(외부도구가 registry 소비) (2) 외부회로→spec ingestion(진입장벽 해소) (3) CLI(단일 진입점)
(4) citable DOI(논문 인용). decomp_guard 가 plan=실회로 보장 → export 정직(hollow 아님).

---

## 1. Gantree

```
Adoption // 신뢰자본 외부 소비화 (designing) @v:0.1
    W3.1_QasmExport // sealed → OpenQASM3 (designing)
        PlanFlatten // app plan 재귀펼침(서브앱 큐빗 remap) → flat_ops (designing)
        QasmEmit // flat_ops → OpenQASM3 텍스트 (gate 매핑테이블) (designing) @dep:PlanFlatten
        RoundTrip // flat_ops INDEP+embed dense → u_hash == sealed (needs-verify) @dep:PlanFlatten
    W3.2_QasmIngestion // OpenQASM3 → spec → 봉인 (designing) @dep:W3.1
        QasmParse // 최소 QASM3 서브셋 파서(h/x/cx/cp/swap…) → ops (designing)
        SpecEmit // ops → .app.pg plan + 오라클 봉인 (needs-verify) @dep:QasmParse
    W3.3_CLI // qf 단일 진입점 (designing) @dep:W3.1
        CliWrap // verify/seal/compose/reproduce/explain/export 기존스크립트 래핑(신규로직 0) (designing)
    W3.4_CitableRegistry // DOI + CITATION.cff (designing)
        CitationMeta // CITATION.cff + release 메타(root_hash 인용) (designing)
    W3.5_SealGateCI // GitHub Action seal-badge (designing) @dep:W3.1,W3.2 [EXT]
```

---

## 2. PPR — W3.1 QasmExport

```python
# acceptance_criteria:
#   - PlanFlatten: 서브앱 재귀펼침, 큐빗 remap 정확(부모 targets[i] ← 서브앱 로컬 i)
#   - QasmEmit: 표준게이트(h/x/z/s/t/sx/cx/cz/swap/ccx/cswap/cp(θ)/ry(θ)) 매핑;
#     미매핑(ccz/mcx 등)은 opaque custom gate decl + 경고(은폐 금지)
#   - RoundTrip: flat_ops 를 second_oracle.INDEP+embed 로 dense 재구성 → hash == sealed u_hash
#     (n≤12 dense; 큰 앱은 정직 skip 표기) → export 가 봉인 유니터리를 표현함을 *증명*

def flatten(app_id, qmap, n_global) -> list[(gate_id, [global_qubits])]:
    """plan 재귀펼침. module step = leaf op; app step = 서브앱 plan 을 qmap remap 후 재귀."""

def to_qasm3(flat_ops, n) -> (qasm_text, unmapped: set):
    """flat_ops → OpenQASM3. QASM_MAP[gate_id]=(name, params). 미매핑은 unmapped 수집."""

def round_trip_u_hash(flat_ops, n) -> str:
    """V=I; for (gid,q) in flat_ops: V = embed(INDEP[gid](), q, n) @ V; return hash_unitary(V)."""
    # == sealed u_hash 이면 export 정직(동일 유니터리)
```

---

## 3. PPR — W3.2 QasmIngestion

```python
# acceptance_criteria:
#   - 최소 QASM3 서브셋(qreg/h/x/z/s/t/cx/cz/swap/cp/ccx) 파싱 → ops
#   - ops → specs/apps/<id>.app.pg(plan) 생성 → app_assemble 봉인 성공
#   - 데모: export(qft3)→ingest→재봉인 u_hash == 원본(round-trip 폐루프)

def ingest_qasm(qasm_text, app_id) -> AppVerdict:
    ops = qasm_parse(qasm_text)              # → [(gate_id, targets)]
    spec = ops_to_app_pg(ops, app_id)        # plan 블록 생성(모듈 참조)
    return app_assemble(spec_path, APPREG)   # 오라클 봉인
```

---

## 4. PPR — W3.3 CLI (신규 로직 0, 래핑만)

```python
# acceptance_criteria: 모든 서브커맨드가 기존 스크립트 위임. 신규 검증로직 0(결정론 단일출처 보존).
#   qf verify <spec> --out <dir>   → verify_seal.py
#   qf reproduce --expect-root <h> → reproduce_all.py (root 대조)
#   qf export <app>                → qasm_export.py
#   qf ingest <qasm> <id>          → qasm_ingest.py
#   qf explain <id>                → registry_tools(dependents) + resource_report(_load)
#   qf compose <spec>              → app_assemble.py
```

---

## 5. PPR — W3.4 CitableRegistry

```python
# acceptance_criteria: CITATION.cff 유효(YAML) + registry_root_hash 포함. release 메타에
#   "QPGF-sealed root <hash>" 인용 문자열. Zenodo DOI 는 placeholder(릴리스 시 정욱님 발급).
```

---

## 6. 불변 제약 / 실행 순서

- 비파괴: `scripts/` 신규 + `.pgf/adoption/`·`CITATION.cff` 가산. registry/sealed/frozen/fingerprint 불변.
  ingestion 데모 봉인은 임시 store(registry 오염 0) 또는 round-trip 후 정리.
- 공통 verify: `reproduce_all` root `3dae613d` · `second_oracle` 48/48 · `verify_contested_guard`.
- 순서: W3.1(export+round-trip) → W3.2(ingest, export 역) → W3.3(CLI 래핑) → W3.4(citation) → W3.5[EXT].
