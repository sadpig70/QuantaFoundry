"""ingest_app_golden.py — 앱 레벨 cross-model app_golden 수급 → 합의 → 봉인앱/게이트 대조.

Round 3: 6개 런타임이 *앱 전체 유니터리*(app_golden = 앱 의도)를 독립 author한 것을 모아:
  1. 각 (app, runtime) → u_hash (오라클 hash_unitary; 전역위상·1e-9 흡수)
  2. independence_unit = weights_id (같은 weights = 1 vote, B4 차단)
  3. establish_truth(N=2): cross-model 합의로 app_golden 확립 (orchestrator-authored golden 대체)
  4. 대조: registry/apps/<id>(내가 봉인한 앱) 또는 registry/modules/<id>(cross-model 게이트)와 u_hash 일치?
     일치 = 앱 의도까지 key-free 승격 (앱 분해가 cross-model 의도와 byte 일치).

사용:
  python .pgf/keyfree/ingest_app_golden.py            # 행렬 + 코드재현 검증
  python .pgf/keyfree/ingest_app_golden.py --no-exec  # 행렬만
"""
import sys, os, json, glob, math, cmath
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import consensus as C                  # noqa: E402

# 기본 디렉토리는 Round 3 (apps). --dir <name> 으로 다른 라운드(예: apps2) 지정 가능.
_DIRNAME = "apps"
if "--dir" in sys.argv:
    _DIRNAME = sys.argv[sys.argv.index("--dir") + 1]
CM = os.path.join(ROOT, "_workspace", "crossmodel", _DIRNAME)
SUB_DIR = os.path.join(CM, "submissions")
INTENTS = os.path.join(CM, "app_intents.json")
REPORT = os.path.join(CM, "APP-CONSENSUS-REPORT.json")
APP_REG = os.path.join(ROOT, "registry", "apps")
MOD_REG = os.path.join(ROOT, "registry", "modules")


def reference_uhash(iid):
    """대조 기준: 봉인 앱(registry/apps) 우선, 없으면 cross-model 게이트(registry/modules)."""
    for reg, kind in ((APP_REG, "sealed-app"), (MOD_REG, "sealed-gate")):
        p = os.path.join(reg, f"{iid}.sealed.json")
        if os.path.exists(p):
            return json.load(open(p, encoding="utf-8"))["u_hash"], kind
    return None, None


def _matrix(sub):
    return np.array(sub["app_golden_real"], float) + 1j * np.array(sub["app_golden_imag"], float)


def _exec_golden(code):
    _ALLOWED = {"numpy": np, "np": np, "math": math, "cmath": cmath}

    def _imp(name, *a, **k):
        if name.split(".")[0] not in _ALLOWED:
            raise ImportError(f"import '{name}' 금지 (numpy/math/cmath 만)")
        return __import__(name, *a, **k)
    sb = {"abs": abs, "range": range, "len": len, "complex": complex, "float": float,
          "int": int, "list": list, "enumerate": enumerate, "zip": zip, "round": round,
          "sum": sum, "pow": pow, "min": min, "max": max, "__import__": _imp}
    ns = {"__builtins__": sb, "np": np, "numpy": np, "math": math, "cmath": cmath}
    exec(compile(code, "<app_golden_code>", "exec"), ns)
    if "golden" not in ns:
        raise ValueError("golden 미정의")
    return np.asarray(ns["golden"], complex)


def main():
    exec_code = "--no-exec" not in sys.argv
    intents = json.load(open(INTENTS, encoding="utf-8"))["intents"]
    order = [it["id"] for it in intents]
    files = sorted(glob.glob(os.path.join(SUB_DIR, "*.app.json")))
    print("=" * 88)
    print("QuantaFoundry — App-Golden Cross-Model Ingest (Round 3: 앱 의도 key-free)")
    print("=" * 88)
    if not files:
        print(f"  제출물 없음: {SUB_DIR}\\*.app.json")
        print("  → APP-GOLDEN-BRIEF.md + app_intents.json 로 런타임 지시 후 제출물 배치.")
        return 1
    print(f"  제출 런타임 {len(files)}개: " + ", ".join(os.path.basename(f).split('.')[0] for f in files))

    by = {iid: [] for iid in order}
    warn = []
    for f in files:
        d = json.load(open(f, encoding="utf-8"))
        rt, wid = d.get("runtime", os.path.basename(f).split(".")[0]), d.get("weights_id")
        for s in d.get("submissions", []):
            iid = s.get("id")
            if iid not in by:
                warn.append(f"{rt}: unknown app {iid}"); continue
            try:
                uh = C.uhash(_matrix(s))
            except Exception as e:
                warn.append(f"{rt}/{iid}: matrix 실패 {e}"); continue
            sc = None
            if exec_code and s.get("app_golden_code"):
                try:
                    sc = (C.uhash(_exec_golden(s["app_golden_code"])) == uh)
                except Exception as e:
                    sc = f"exec_err:{str(e)[:35]}"
            by[iid].append({"runtime": rt, "weights_id": wid or rt, "u_hash": uh, "self_consistent": sc})

    report = {"runtimes": [os.path.basename(f).split('.')[0] for f in files],
              "warnings": warn, "apps": {}}
    print("\n" + "-" * 88)
    est = mm = match_n = 0
    for iid in order:
        rows = by[iid]
        sources = [C.Source(f"{iid}_{r['runtime']}", "model", r["weights_id"], r["u_hash"]) for r in rows]
        res = C.establish_truth(iid, sources, N=2)
        ref, kind = reference_uhash(iid)
        match = (res.key == ref) if (res.key and ref) else None
        if res.status == "ESTABLISHED":
            est += 1
            if res.grade == "MULTIMODEL":
                mm += 1
        if match:
            match_n += 1
        report["apps"][iid] = {"status": res.status, "grade": res.grade, "key": res.key,
                               "n_runtimes": len(rows), "distribution": res.distribution,
                               "reference": ref, "reference_kind": kind, "reference_match": match,
                               "escalation": res.escalation,
                               "votes": [{"runtime": r["runtime"], "u_hash": r["u_hash"][:16],
                                          "agrees": (r["u_hash"] == res.key) if res.key else None,
                                          "self_consistent": r["self_consistent"]} for r in rows]}
        icon = {"ESTABLISHED": "✅", "DIVERGENT": "⚠️", "INSUFFICIENT": "△"}.get(res.status, "?")
        line = f"  {icon} {iid:11} {res.status:12}"
        if res.key:
            line += f" {res.grade:10} key={res.key[:12]}.. votes={len(rows)}  ⟺{kind or 'none'}:"
            line += ("✓일치" if match else ("✗불일치" if match is False else "·없음"))
        else:
            line += f"  {res.escalation[:46]}"
        print(line)
        if res.key:
            for v in report["apps"][iid]["votes"]:
                if v["agrees"] is False:
                    print(f"        ✗ dissent {v['runtime']:10} {v['u_hash']}..")

    print("-" * 88)
    print(f"앱 의도 확립 {est}/{len(order)} ESTABLISHED · MULTIMODEL {mm} · 봉인앱/게이트 일치 {match_n}/{len(order)}")
    print("=" * 88)
    report["summary"] = {"total": len(order), "established": est, "multimodel": mm, "reference_match": match_n}
    json.dump(report, open(REPORT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"리포트: {os.path.relpath(REPORT, ROOT)}")
    return 0 if est == len(order) and match_n == len(order) else 1


if __name__ == "__main__":
    sys.exit(main())
