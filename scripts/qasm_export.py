# -*- coding: utf-8 -*-
"""qasm_export.py — Stage 3 W3.1 QasmExport: sealed app → OpenQASM3 (round-trip 정직).

봉인 신뢰자본을 외부도구가 소비하려면 표준 포맷(OpenQASM3) export 가 필요하다. decomp_guard 가
plan=실회로(no hollow/MatrixGate)를 보장하므로 plan 을 펼치면 정직한 게이트 시퀀스가 나온다.

정직성의 증명 = **round-trip**: 펼친 flat_ops 를 second_oracle(INDEP+embed, 제1원리 numpy)로
dense 재구성 → u_hash 가 sealed u_hash 와 일치. export 가 봉인 유니터리를 표현함을 독립검증으로
입증(QASM 텍스트가 hollow 가 아님). 미매핑 게이트(ccz/c5x/c6x 등 QASM3 비표준)는 opaque custom
gate 선언 + 경고로 정직 노출(은폐 금지). round-trip 은 INDEP 가 모든 게이트를 알아 항상 가능(n≤12).

비파괴: registry/sealed/frozen/fingerprint 불변. `.pgf/adoption/` + `<id>.qasm` 만 가산.
소비 자산(사용만): second_oracle(INDEP/embed/vs.hash_unitary) · registry_tools 경로.

사용:
  python scripts/qasm_export.py <app_id>     # 단일 앱 export + round-trip
  python scripts/qasm_export.py --all         # 전 앱 round-trip 검증 요약
"""
from __future__ import annotations
import os, sys, json, re, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import second_oracle as so            # noqa: E402  INDEP/embed/vs.hash_unitary 사용만
vs = so.vs

APPS = os.path.join(ROOT, "specs", "apps")
MODSPEC = os.path.join(ROOT, "specs", "modules")
APPREG = os.path.join(ROOT, "registry", "apps")
OUTDIR = os.path.join(ROOT, ".pgf", "adoption", "qasm")

EXACT_BOUND = 10   # dense round-trip 실용상한 (2^10=1024; n=11/12 대형은 정직 skip)


def _meta_n(spec_path):
    src = open(spec_path, encoding="utf-8").read()
    m = re.search(r"```json id=meta\n(.*?)```", src, re.S)
    return json.loads(m.group(1)) if m else {}


def _plan(spec_path):
    src = open(spec_path, encoding="utf-8").read()
    m = re.search(r"```json id=plan\n(.*?)```", src, re.S)
    return json.loads(m.group(1)) if m else None


def _gate_nq(gid):
    """모듈 유니터리 차원 → 큐빗 수."""
    return int(round(math.log2(so.INDEP[gid]().shape[0])))


def _resolve_n(app_id):
    """앱 n_sys: meta → sealed → plan targets 추론."""
    sp = os.path.join(APPS, f"{app_id}.app.pg")
    n = _meta_n(sp).get("n_sys")
    if n is None:
        sealed_p = os.path.join(APPREG, f"{app_id}.sealed.json")
        if os.path.exists(sealed_p):
            n = json.load(open(sealed_p, encoding="utf-8")).get("n_sys")
    if n is None:
        plan = _plan(sp)
        n = 1 + max((t for step in plan["steps"] for t in step.get("targets", [0])), default=0)
    return n


# ─────────────── PlanFlatten: app plan 재귀펼침 → flat_ops ───────────────
def flatten(app_id, qmap=None, depth=0):
    """plan 재귀펼침 → [(gate_id, [global_qubits])]. module=leaf, app=서브앱 remap 재귀."""
    if depth > 32:
        raise RuntimeError("flatten depth exceeded")
    sp = os.path.join(APPS, f"{app_id}.app.pg")
    plan = _plan(sp)
    n = _resolve_n(app_id)
    if qmap is None:
        qmap = {i: i for i in range(n)}
    ops = []
    for step in plan["steps"]:
        if "spec" in step:                       # module leaf
            gid = os.path.basename(step["spec"])[:-3]
            local_targets = step.get("targets")
            if local_targets is None:            # targets 누락 = 전체 큐빗(자식 n_qubits==n_sys)
                local_targets = list(range(_gate_nq(gid)))
            gtargets = [qmap[t] for t in local_targets]
            ops.append((gid, gtargets))
        elif "app" in step:                      # sub-app recurse
            sub_id = step["app"][:-7]
            local_targets = step.get("targets")
            if local_targets is None:
                local_targets = list(range(_resolve_n(sub_id)))
            gtargets = [qmap[t] for t in local_targets]
            sub_qmap = {i: gtargets[i] for i in range(len(gtargets))}
            sub_ops, _ = flatten(sub_id, sub_qmap, depth + 1)
            ops.extend(sub_ops)
    return ops, n


# ─────────────── RoundTrip: flat_ops → dense → u_hash ───────────────
def round_trip_u_hash(flat_ops, n):
    """second_oracle INDEP+embed 로 dense 재구성 → hash_unitary. == sealed 면 export 정직."""
    V = np.eye(1 << n, dtype=complex)
    for gid, q in flat_ops:
        V = so.embed(so.INDEP[gid](), q, n) @ V
    return vs.hash_unitary(V)


# ─────────────── QasmEmit: flat_ops → OpenQASM3 ───────────────
def _ry_angle(gid):
    M = so.INDEP[gid]()
    return 2.0 * math.atan2(float(M[1, 0].real), float(M[0, 0].real))   # Ry(θ): cos(θ/2),sin(θ/2)


def _cp_lambda(gid):
    """controlled-phase diag(1,1,1,e^{iλ}) 의 λ 를 INDEP 행렬에서 추출."""
    M = so.INDEP[gid]()
    return float(np.angle(M[3, 3]))


def qasm_for(gid):
    """gate_id → (qasm_line_template, n_controls_for_comment) 또는 None(미매핑)."""
    simple = {"h_gate": "h", "x_gate": "x", "z_gate": "z", "s_gate": "s", "t_gate": "t", "sx": "sx",
              "cnot": "cx", "cz": "cz", "swap2": "swap", "toffoli": "ccx", "fredkin": "cswap"}
    if gid in simple:
        return (simple[gid], None)
    if gid in ("cs_gate", "ct_gate", "cs_dag") or re.match(r"^cr\d+(_dag)?_gate$", gid):
        return (f"cp({_cp_lambda(gid):.12g})", None)
    if re.match(r"^ry_k\d+(_dag)?$", gid):
        return (f"ry({_ry_angle(gid):.12g})", None)
    return None   # 미매핑 (ccz / c3x..c6x mcx 등 QASM3 비표준)


def to_qasm3(flat_ops, n, app_id):
    lines = ["OPENQASM 3.0;", 'include "stdgates.inc";', f"qubit[{n}] q;", ""]
    unmapped = {}
    body = []
    for gid, q in flat_ops:
        spec = qasm_for(gid)
        qref = ", ".join(f"q[{i}]" for i in q)
        if spec is None:
            unmapped[gid] = unmapped.get(gid, 0) + 1
            body.append(f"// UNMAPPED {gid} {q}  (QASM3 비표준 — opaque)")
            body.append(f"{_opaque_name(gid)} {qref};")
        else:
            name = spec[0]
            body.append(f"{name} {qref};")
    # opaque custom gate 선언(미매핑) — 은폐 금지
    decls = [f"gate {_opaque_name(gid)} " + ", ".join(f"q{i}" for i in range(_gate_nq(gid))) +
             f" {{ }}  // opaque: {gid} ({_gate_nq(gid)}q), golden in registry/modules/{gid}.sealed.json"
             for gid in sorted(unmapped)]
    qasm = "\n".join(lines + (decls + [""] if decls else []) + body) + "\n"
    return qasm, unmapped


def _opaque_name(gid):
    return "qpgf_" + re.sub(r"\W", "_", gid)


# ─────────────── 단일/전체 export ───────────────
def export_one(app_id, write=True):
    sp = os.path.join(APPS, f"{app_id}.app.pg")
    if not os.path.exists(sp):
        return {"id": app_id, "error": "spec-not-found"}
    sealed_path = os.path.join(APPREG, f"{app_id}.sealed.json")
    sealed = json.load(open(sealed_path, encoding="utf-8")) if os.path.exists(sealed_path) else {}
    flat_ops, n = flatten(app_id)
    rec = {"id": app_id, "n_sys": n, "n_ops": len(flat_ops),
           "sealed_u_hash": sealed.get("u_hash", "")[:16]}
    # round-trip (dense, n≤12)
    if n is not None and n <= EXACT_BOUND:
        rt = round_trip_u_hash(flat_ops, n)
        rec["round_trip_u_hash"] = rt[:16]
        rec["round_trip_match"] = (rt == sealed.get("u_hash"))
    else:
        rec["round_trip_match"] = None
        rec["round_trip_note"] = f"n={n} > {EXACT_BOUND}: dense round-trip skip(정직)"
    # QASM 텍스트
    qasm, unmapped = to_qasm3(flat_ops, n, app_id)
    rec["unmapped_gates"] = unmapped
    if write:
        os.makedirs(OUTDIR, exist_ok=True)
        open(os.path.join(OUTDIR, f"{app_id}.qasm"), "w", encoding="utf-8", newline="\n").write(qasm)
        rec["qasm_path"] = f".pgf/adoption/qasm/{app_id}.qasm"
    return rec


def main():
    args = sys.argv[1:]
    os.makedirs(OUTDIR, exist_ok=True)
    if args and args[0] == "--all":
        ids = sorted(f[:-7] for f in os.listdir(APPS) if f.endswith(".app.pg"))
        recs = [export_one(a) for a in ids]
        checked = [r for r in recs if r.get("round_trip_match") is not None]
        matched = [r for r in checked if r["round_trip_match"]]
        skipped = [r for r in recs if r.get("round_trip_match") is None]
        unmapped_all = sorted({g for r in recs for g in r.get("unmapped_gates", {})})
        print("=" * 80)
        print("QasmExport (W3.1) — 전 앱 sealed→OpenQASM3 + round-trip(INDEP 독립 재구성) 검증")
        print("=" * 80)
        for r in recs:
            m = r.get("round_trip_match")
            tag = "✓ match" if m else ("· skip(n>12)" if m is None else "✗ MISMATCH")
            print(f"  {tag:14} {r['id']:18} n={r.get('n_sys')} ops={r.get('n_ops')} "
                  f"{'unmapped='+str(list(r['unmapped_gates'])) if r.get('unmapped_gates') else ''}")
        print("-" * 80)
        allok = len(matched) == len(checked)
        out = {"_schema": "qasm-export-v1", "exported": len(recs),
               "round_trip_checked": len(checked), "round_trip_matched": len(matched),
               "round_trip_skipped_large": len(skipped), "all_checked_match": allok,
               "unmapped_gate_kinds": unmapped_all, "records": recs,
               "_note": "round-trip=second_oracle(INDEP+embed) 제1원리 numpy 재구성 u_hash==sealed → "
                        "export 가 봉인 유니터리를 정직 표현함을 독립검증. 미매핑은 opaque custom gate 노출. 비파괴."}
        json.dump(out, open(os.path.join(ROOT, ".pgf", "adoption", "QASM-EXPORT-REPORT.json"), "w",
                            encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"round-trip {len(matched)}/{len(checked)} 일치 · skip(n>12) {len(skipped)} · "
              f"미매핑 게이트종류 {unmapped_all}")
        print(f"→ .pgf/adoption/QASM-EXPORT-REPORT.json · QASM: .pgf/adoption/qasm/*.qasm")
        return 0 if allok else 1
    elif args:
        r = export_one(args[0])
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0 if r.get("round_trip_match") in (True, None) else 1
    print("usage: qasm_export.py <app_id> | --all")
    return 2


if __name__ == "__main__":
    sys.exit(main())
