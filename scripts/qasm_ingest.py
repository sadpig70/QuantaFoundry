# -*- coding: utf-8 -*-
"""qasm_ingest.py — Stage 3 W3.2 QasmIngestion: OpenQASM3 → spec → 오라클 봉인.

진입장벽 해소(A3 우선): 외부가 *이미 가진* 회로(OpenQASM3)를 spec(.app.pg)으로 변환 → 오라클
봉인 → registry 편입. export(W3.1)의 역방향. 정직성 증명 = **폐루프**: export(app)→ingest→재봉인
u_hash == 원본 sealed u_hash. 즉 QASM↔spec 왕복이 유니터리를 보존.

최소 QASM3 서브셋(stdgates + cp(θ)/ry(θ)) 파서. 게이트 역매핑은 export 의 QASM_MAP 역 —
cp(λ)/ry(θ) 는 INDEP 봉인 게이트의 실제 λ/θ 와 대조해 gate_id 복원(휴리스틱 아님, 봉인값 일치).

비파괴: 임시 store(.pgf/adoption/_ingest)로만 봉인 → registry/sealed/frozen/fingerprint 불변.
소비 자산(사용만): second_oracle(INDEP) · app_assemble(assemble) · qasm_export(역검증용).

사용:
  python scripts/qasm_ingest.py <app_id>   # export→ingest→재봉인 폐루프 데모(단일)
  python scripts/qasm_ingest.py --demo      # 대표 앱 폐루프 요약
"""
from __future__ import annotations
import os, sys, json, re, math, shutil
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts"))
import second_oracle as so            # noqa: E402  INDEP 사용만
import qasm_export as qe              # noqa: E402  export(역검증)/_resolve_n 사용만
import app_assemble as aa             # noqa: E402  assemble(오라클) 사용만

APPREG = os.path.join(ROOT, "registry", "apps")
INGEST_STORE = os.path.join(ROOT, ".pgf", "adoption", "_ingest")

# 단순 stdgate 역매핑 (qasm name → module gate_id)
SIMPLE_REV = {"h": "h_gate", "x": "x_gate", "z": "z_gate", "s": "s_gate", "t": "t_gate", "sx": "sx",
              "cx": "cnot", "cz": "cz", "swap": "swap2", "ccx": "toffoli", "cswap": "fredkin"}


def _build_param_tables():
    """INDEP 봉인 게이트의 실제 cp-λ / ry-θ 테이블 → 파라미터 게이트 역매핑(봉인값 일치)."""
    cp_table, ry_table = {}, {}
    for gid in so.INDEP:
        if gid in ("cs_gate", "ct_gate", "cs_dag") or re.match(r"^cr\d+(_dag)?_gate$", gid):
            cp_table[round(qe._cp_lambda(gid), 9)] = gid
        elif re.match(r"^ry_k\d+(_dag)?$", gid):
            ry_table[round(qe._ry_angle(gid), 9)] = gid
    return cp_table, ry_table


CP_TABLE, RY_TABLE = _build_param_tables()


def _match_param(val, table, tol=1e-6):
    for k, gid in table.items():
        if abs(((val - k + math.pi) % (2 * math.pi)) - math.pi) < tol:
            return gid
    return None


def parse_qasm(qasm_text):
    """최소 QASM3 서브셋 → [(gate_id, [qubits])]. 미지원/opaque 라인은 예외."""
    ops, n = [], None
    for raw in qasm_text.splitlines():
        line = raw.split("//")[0].strip().rstrip(";").strip()
        if not line or line.startswith(("OPENQASM", "include", "gate ")):
            continue
        m = re.match(r"^qubit\[(\d+)\]\s+\w+$", line)
        if m:
            n = int(m.group(1)); continue
        m = re.match(r"^(\w+)(\(([^)]*)\))?\s+(.+)$", line)
        if not m:
            raise ValueError(f"unparseable: {raw}")
        name, _, param, qargs = m.groups()
        qubits = [int(x) for x in re.findall(r"q\[(\d+)\]", qargs)]
        if name in SIMPLE_REV:
            gid = SIMPLE_REV[name]
        elif name == "cp":
            gid = _match_param(float(eval(param, {"pi": math.pi, "__builtins__": {}})), CP_TABLE)
        elif name == "ry":
            gid = _match_param(float(eval(param, {"pi": math.pi, "__builtins__": {}})), RY_TABLE)
        else:
            raise ValueError(f"unsupported gate (opaque/non-stdgate): {name}")
        if gid is None:
            raise ValueError(f"param gate unresolved: {name}({param})")
        ops.append((gid, qubits))
    return ops, n


def ops_to_app_pg(ops, app_id, n):
    """ops → .app.pg 텍스트(plan + app_meta). 모듈 참조(no MatrixGate, no app_golden).
    tier='exact'(n≤EXACT_BOUND): golden 없이 자식 dense 합성으로 Tier-0 봉인 → 원본 dense u_hash 재현."""
    steps = ",\n           ".join(
        json.dumps({"spec": f"../modules/{gid}.pg", "targets": q}) for gid, q in ops)
    plan = {"steps": "@@STEPS@@"}
    if n <= qe.EXACT_BOUND:
        plan["tier"] = "exact"
    plan_json = json.dumps(plan).replace('"@@STEPS@@"', f"[{steps}]")
    return (f"# {app_id} — ingested from OpenQASM3 (W3.2 QasmIngestion)\n\n"
            f"```json id=plan\n{plan_json}\n```\n\n"
            f"```json id=app_meta\n{json.dumps({'id': app_id, 'n_sys': n, 'n_anc': 0})}\n```\n")


def ingest_one(app_id):
    """export(app_id) → QASM → parse → spec → 임시봉인. 폐루프 u_hash 대조."""
    qasm_path = os.path.join(qe.OUTDIR, f"{app_id}.qasm")
    if not os.path.exists(qasm_path):
        qe.export_one(app_id)   # 없으면 생성
    qasm = open(qasm_path, encoding="utf-8").read()
    try:
        ops, n = parse_qasm(qasm)
    except ValueError as e:
        return {"id": app_id, "ingested": False, "reason": str(e)}
    os.makedirs(INGEST_STORE, exist_ok=True)
    ing_id = f"{app_id}_ingested"
    spec_txt = ops_to_app_pg(ops, ing_id, n)
    # 모듈 참조 경로 위해 specs/apps 임시 spec 필요 → 임시로 작성 후 제거
    tmp_spec = os.path.join(ROOT, "specs", "apps", f"{ing_id}.app.pg")
    open(tmp_spec, "w", encoding="utf-8", newline="\n").write(spec_txt)
    try:
        v = aa.assemble(tmp_spec, INGEST_STORE)
        orig = json.load(open(os.path.join(APPREG, f"{app_id}.sealed.json"), encoding="utf-8"))
        loop_match = bool(v.sealed and v.u_hash == orig["u_hash"])
        rec = {"id": app_id, "ingested": bool(v.sealed), "n_ops": len(ops), "n_sys": n,
               "ingested_u_hash": (v.u_hash or "")[:16], "original_u_hash": orig["u_hash"][:16],
               "closed_loop_match": loop_match, "tier": v.tier}
    finally:
        os.remove(tmp_spec)
    return rec


def main():
    args = sys.argv[1:]
    # 폐루프 데모 대상: 표준게이트만 쓰는 대표 앱(미매핑 c_kx 없는 것)
    demo_ids = ["qft3_pipeline", "iqft3", "qpe_t", "ghz5", "ring6", "wstate4", "shor15_a2", "cmul7_mod15"]
    targets = demo_ids if (args and args[0] == "--demo") else (args or demo_ids)
    os.makedirs(INGEST_STORE, exist_ok=True)
    print("=" * 82)
    print("QasmIngestion (W3.2) — OpenQASM3 → spec → 오라클 봉인 (export→ingest 폐루프)")
    print("=" * 82)
    recs = [ingest_one(a) for a in targets]
    ok = [r for r in recs if r.get("closed_loop_match")]
    for r in recs:
        if r.get("ingested"):
            mark = "✓" if r["closed_loop_match"] else "✗"
            print(f"  {mark} {r['id']:16} ingest→seal u={r['ingested_u_hash']} == orig {r['original_u_hash']} "
                  f"(폐루프 {'일치' if r['closed_loop_match'] else 'MISMATCH'}) ops={r['n_ops']}")
        else:
            print(f"  · {r['id']:16} skip — {r.get('reason','')[:50]}")
    # 임시 store 정리(registry 오염 0)
    ing_files = sorted(os.path.basename(f) for f in os.listdir(INGEST_STORE)) if os.path.isdir(INGEST_STORE) else []
    if os.path.isdir(INGEST_STORE):
        shutil.rmtree(INGEST_STORE)
    allok = len(ok) == len([r for r in recs if r.get("ingested")])
    out = {"_schema": "qasm-ingest-v1", "closed_loop_checked": len([r for r in recs if r.get("ingested")]),
           "closed_loop_matched": len(ok), "all_match": allok, "records": recs,
           "ingest_store_sealed_files": ing_files, "ingest_store_cleaned": True,
           "_note": "export(W3.1)→QASM→parse→spec→app_assemble 봉인. 폐루프 u_hash==원본 = QASM↔spec 왕복 "
                    "유니터리 보존(진입장벽: 외부 회로를 봉인 가능). 임시 store 봉인(registry 불변). MatrixGate 없음."}
    json.dump(out, open(os.path.join(ROOT, ".pgf", "adoption", "QASM-INGEST-REPORT.json"), "w",
                        encoding="utf-8"), ensure_ascii=False, indent=2)
    print("-" * 82)
    print(f"폐루프 {len(ok)}/{len([r for r in recs if r.get('ingested')])} 일치 · "
          f"임시 store 정리({len(ing_files)}건 봉인→삭제) · → .pgf/adoption/QASM-INGEST-REPORT.json")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
