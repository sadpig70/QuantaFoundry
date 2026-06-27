"""ingest_crossmodel.py — cross-model 제출물 수집 → 합의 확립 → ground-truth 교차검증.

실배포 cross-model 합의 파이프라인. 6개 외부 런타임(codex/gemini/grok/kimi/qwen/deepseek)이
RUNTIME-BRIEF.md 규약대로 author 한 golden 행렬을 모아:

  1. 각 (intent, runtime) → u_hash (오라클 hash_unitary; 전역위상·1e-9 흡수)
  2. independence_unit = weights_id (같은 weights 다수 = 1 vote, B4 차단)
  3. establish_truth(N=2): *cross-model 출처만으로* consensus_key 창발 (인간 seed 0)
  4. ground-truth(formal-spec/proof, 모델 독립)와 대조 — 동반오류(co-error) 탐지
  5. Round A: 기존 봉인 키와 대조(calibration). Round B: 신규 진리 확립.

사용:
  python .pgf/keyfree/ingest_crossmodel.py                 # JSON 행렬로 합의 + 코드 재현검증
  python .pgf/keyfree/ingest_crossmodel.py --no-exec       # golden_code 재실행 생략(행렬만)

제출물 위치: _workspace/crossmodel/submissions/*.submission.json
리포트:     _workspace/crossmodel/CONSENSUS-REPORT.json
"""
import sys, os, json, glob, math, cmath
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import consensus as C                 # noqa: E402  (합의 엔진)
import formal_spec as F               # noqa: E402  (formal-spec ground-truth)

SUB_DIR = os.path.join(ROOT, "_workspace", "crossmodel", "submissions")
REG_DIR = os.path.join(ROOT, "registry", "modules")
REPORT = os.path.join(ROOT, "_workspace", "crossmodel", "CONSENSUS-REPORT.json")
INTENTS = os.path.join(ROOT, "_workspace", "crossmodel", "intents.json")

# ── 독립 ground-truth (proof/formal-spec, 모델 비의존) — 동반오류 감사용 ──
#   런타임에는 노출하지 않는다(독립성). qft 계열은 consensus.proof_qft(roots of unity).
_GT_SPEC = {
    "x_gate":  {"kind": "matrix", "n_sys": 1, "rows": [["0", "1"], ["1", "0"]]},
    "z_gate":  {"kind": "diag",   "n_sys": 1, "diag": ["1", "-1"]},
    "h_gate":  {"kind": "matrix", "n_sys": 1, "rows": [["1/sqrt(2)", "1/sqrt(2)"],
                                                       ["1/sqrt(2)", "-1/sqrt(2)"]]},
    "cnot":    {"kind": "perm",   "n_sys": 2, "perm": [0, 1, 3, 2]},
    "swap2":   {"kind": "perm",   "n_sys": 2, "perm": [0, 2, 1, 3]},
    "toffoli": {"kind": "perm",   "n_sys": 3, "perm": [0, 1, 2, 3, 4, 5, 7, 6]},
    "s_gate":  {"kind": "diag",   "n_sys": 1, "diag": ["1", "I"]},
    "t_gate":  {"kind": "diag",   "n_sys": 1, "diag": ["1", "exp(I*pi/4)"]},
    "cz":      {"kind": "diag",   "n_sys": 2, "diag": ["1", "1", "1", "-1"]},
    "iswap":   {"kind": "matrix", "n_sys": 2, "rows": [["1", "0", "0", "0"],
                                                       ["0", "0", "I", "0"],
                                                       ["0", "I", "0", "0"],
                                                       ["0", "0", "0", "1"]]},
    "cs_gate": {"kind": "diag",   "n_sys": 2, "diag": ["1", "1", "1", "I"]},
    "ccz":     {"kind": "diag",   "n_sys": 3, "diag": ["1", "1", "1", "1", "1", "1", "1", "-1"]},
}


def ground_truth_uhash(intent_id):
    """formal-spec/proof 로 계산한 모델-독립 정답 u_hash (없으면 None)."""
    if intent_id.startswith("qft"):
        n = int(intent_id[3:])
        return C.uhash(C.proof_qft(n))
    spec = _GT_SPEC.get(intent_id)
    return C.uhash(F.compile_spec(spec)) if spec else None


def known_seal_uhash(intent_id):
    """Round A calibration: 기존 봉인된 u_hash (registry). 없으면 None."""
    p = os.path.join(REG_DIR, f"{intent_id}.sealed.json")
    if os.path.exists(p):
        return json.load(open(p, encoding="utf-8")).get("u_hash")
    return None


def _matrix_from_json(sub):
    re = np.array(sub["golden_real"], dtype=float)
    im = np.array(sub["golden_imag"], dtype=float)
    return re + 1j * im


def _exec_golden_code(code):
    """golden_code 를 제한 네임스페이스에서 재실행 → `golden` 행렬 (실패 시 예외)."""
    _ALLOWED_MODS = {"numpy": np, "np": np, "math": math, "cmath": cmath}

    def _safe_import(name, *a, **k):
        root = name.split(".")[0]
        if root not in _ALLOWED_MODS:
            raise ImportError(f"import '{name}' 금지 (numpy/math/cmath 만 허용)")
        return __import__(name, *a, **k)

    safe_builtins = {"abs": abs, "range": range, "len": len, "complex": complex,
                     "float": float, "int": int, "list": list, "enumerate": enumerate,
                     "zip": zip, "round": round, "sum": sum, "pow": pow, "min": min, "max": max,
                     "__import__": _safe_import}
    ns = {"__builtins__": safe_builtins, "np": np, "numpy": np, "math": math, "cmath": cmath}
    exec(compile(code, "<golden_code>", "exec"), ns)
    if "golden" not in ns:
        raise ValueError("golden_code 가 `golden` 변수를 정의하지 않음")
    return np.asarray(ns["golden"], dtype=complex)


def main():
    exec_code = "--no-exec" not in sys.argv
    intents = json.load(open(INTENTS, encoding="utf-8"))["intents"]
    intent_order = [it["id"] for it in intents]
    intent_meta = {it["id"]: it for it in intents}

    files = sorted(glob.glob(os.path.join(SUB_DIR, "*.submission.json")))
    print("=" * 84)
    print("QuantaFoundry — Cross-Model Consensus Ingest")
    print("=" * 84)
    if not files:
        print(f"  제출물 없음: {SUB_DIR}\\*.submission.json")
        print("  → RUNTIME-BRIEF.md + intents.json 으로 런타임에 작업 지시 후 제출물을 이 폴더에 배치.")
        return 1
    print(f"  제출 런타임 {len(files)}개: " + ", ".join(os.path.basename(f).split('.')[0] for f in files))
    if not exec_code:
        print("  (golden_code 재실행 생략 — JSON 행렬만 사용)")

    # (intent_id) -> list of (runtime, weights_id, u_hash, self_consistent)
    by_intent = {iid: [] for iid in intent_order}
    load_warn = []
    for f in files:
        sub = json.load(open(f, encoding="utf-8"))
        rt = sub.get("runtime", os.path.basename(f).split(".")[0])
        wid = sub.get("weights_id", rt)
        for s in sub.get("submissions", []):
            iid = s.get("id")
            if iid not in by_intent:
                load_warn.append(f"{rt}: unknown intent {iid}")
                continue
            try:
                U = _matrix_from_json(s)
                uh = C.uhash(U)
            except Exception as e:
                load_warn.append(f"{rt}/{iid}: matrix parse 실패 {e}")
                continue
            sc = None
            if exec_code and s.get("golden_code"):
                try:
                    sc = (C.uhash(_exec_golden_code(s["golden_code"])) == uh)
                except Exception as e:
                    sc = f"exec_err: {str(e)[:40]}"
            by_intent[iid].append({"runtime": rt, "weights_id": wid, "u_hash": uh,
                                   "self_consistent": sc})

    # 합의 + 교차검증
    report = {"runtimes": [os.path.basename(f).split(".")[0] for f in files],
              "exec_code": exec_code, "warnings": load_warn, "intents": {}}
    print("\n" + "-" * 84)
    for iid in intent_order:
        rows = by_intent[iid]
        rnd = intent_meta[iid]["round"]
        gt = ground_truth_uhash(iid)
        sources = [C.Source(f"{iid}_{r['runtime']}", "model", r["weights_id"], r["u_hash"])
                   for r in rows]
        res = C.establish_truth(iid, sources, N=2)

        key = res.key
        gt_match = (key == gt) if (key and gt) else None
        entry = {"round": rnd, "status": res.status, "grade": res.grade, "key": key,
                 "n_runtimes": len(rows), "distribution": res.distribution,
                 "ground_truth": gt, "ground_truth_match": gt_match,
                 "escalation": res.escalation,
                 "votes": [{"runtime": r["runtime"], "weights_id": r["weights_id"],
                            "u_hash": r["u_hash"][:16],
                            "agrees": (r["u_hash"] == key) if key else None,
                            "self_consistent": r["self_consistent"]} for r in rows]}
        if rnd == "A":
            ks = known_seal_uhash(iid)
            entry["known_seal"] = ks
            entry["calibration_pass"] = (key == ks) if (key and ks) else None
        report["intents"][iid] = entry

        # 콘솔
        icon = {"ESTABLISHED": "✅", "DIVERGENT": "⚠️", "INSUFFICIENT": "△"}.get(res.status, "?")
        line = f"  {icon} {iid:9} [{rnd}] {res.status:12}"
        if key:
            line += f" {res.grade:10} key={key[:12]}.. votes={len(rows)}"
            if rnd == "A":
                line += "  calib=" + ("✓" if entry.get("calibration_pass") else "✗")
            line += "  GT=" + ("✓" if gt_match else ("✗" if gt_match is False else "·"))
        else:
            line += f"  {res.escalation[:48]}"
        print(line)
        # 불일치 투표 노출 (진단)
        if key:
            dissent = [v for v in entry["votes"] if v["agrees"] is False]
            for d in dissent:
                print(f"        ✗ dissent {d['runtime']:9} {d['u_hash']}.. (다른 규약/유도 의심)")

    # 요약
    rb = [e for e in report["intents"].values() if e["round"] == "B"]
    ra = [e for e in report["intents"].values() if e["round"] == "A"]
    est_b = sum(1 for e in rb if e["status"] == "ESTABLISHED")
    mm_b = sum(1 for e in rb if e.get("grade") == "MULTIMODEL")
    calib_ok = sum(1 for e in ra if e.get("calibration_pass"))
    gt_ok = sum(1 for e in report["intents"].values() if e.get("ground_truth_match"))
    print("-" * 84)
    print(f"Round A calibration: {calib_ok}/{len(ra)} 기존봉인 일치")
    print(f"Round B 확립: {est_b}/{len(rb)} ESTABLISHED · MULTIMODEL {mm_b} · ground-truth 일치 {gt_ok}/{len(report['intents'])}")
    print("=" * 84)
    report["summary"] = {"round_a": len(ra), "calibration_pass": calib_ok,
                         "round_b": len(rb), "established_b": est_b, "multimodel_b": mm_b,
                         "ground_truth_match_total": gt_ok}
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    json.dump(report, open(REPORT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"리포트: {os.path.relpath(REPORT, ROOT)}")
    # 성공 = calibration 전부 통과 + Round B 발산 없음
    return 0 if calib_ok == len(ra) and est_b == len(rb) else 1


if __name__ == "__main__":
    sys.exit(main())
