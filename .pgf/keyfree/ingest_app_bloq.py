"""ingest_app_bloq.py — 앱 구현(회로) cross-model 수급 → 조립 → 봉인앱과 대조.

각 런타임이 sealed-gate 어휘로 앱의 *독립 회로*를 작성. 파이프라인은 회로를 봉인 게이트 행렬로
조립해 u_hash 계산 → (1) 런타임 간 수렴(독립단위 ≥2) (2) 봉인 앱/골든과 일치 를 확인한다.
서로 *다른* 회로가 같은 u_hash 로 수렴 = 구현의 독립 교차검증(동반오류 방화벽의 구현 측).

사용:  python .pgf/keyfree/ingest_app_bloq.py            # 코드 재현 등 전체
       python .pgf/keyfree/ingest_app_bloq.py --dir apps2
"""
import sys, os, json, glob
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts"))
import consensus as C                  # noqa: E402
import verify_seal as vs               # noqa: E402
import contracts                       # noqa: E402

_DIRNAME = "apps2"
if "--dir" in sys.argv:
    _DIRNAME = sys.argv[sys.argv.index("--dir") + 1]
CM = os.path.join(ROOT, "_workspace", "crossmodel", _DIRNAME)
SUB_DIR = os.path.join(CM, "submissions_bloq")
INTENTS = os.path.join(CM, "app_intents.json")
VOCAB = os.path.join(CM, "GATE-VOCABULARY.json")
REPORT = os.path.join(CM, "APP-BLOQ-REPORT.json")
APP_REG = os.path.join(ROOT, "registry", "apps")
MOD_REG = os.path.join(ROOT, "registry", "modules")


def load_gate_matrices():
    """어휘집 게이트명 -> 봉인 모듈 유니터리 (registry 사용만)."""
    vocab = json.load(open(VOCAB, encoding="utf-8"))["gates"]
    mats = {}
    for name, meta in vocab.items():
        sp = vs.load_pg_spec(os.path.join(ROOT, "specs", "modules", f"{meta['module']}.pg"))
        mats[name] = (np.asarray(vs.instantiate(sp.bloq_src, "bloq").tensor_contract()), meta["n_qubits"])
    return mats


def assemble_circuit(circuit, n, mats):
    """회로(step 리스트)를 n-qubit 유니터리로 조립. 잘못된 게이트/타깃은 예외."""
    V = np.eye(1 << n, dtype=complex)
    for step in circuit:
        g = step["gate"]; t = step["targets"]
        if g not in mats:
            raise ValueError(f"unknown gate '{g}'")
        U, nq = mats[g]
        if len(t) != nq:
            raise ValueError(f"gate '{g}' expects {nq} targets, got {t}")
        if len(set(t)) != len(t) or any(w < 0 or w >= n for w in t):
            raise ValueError(f"bad targets {t} for n={n}")
        V = contracts.embed_unitary(U, t, n) @ V   # step 순서대로 좌측 누적
    return V


def reference_uhash(iid):
    for reg, kind in ((APP_REG, "sealed-app"), (MOD_REG, "sealed-gate")):
        p = os.path.join(reg, f"{iid}.sealed.json")
        if os.path.exists(p):
            return json.load(open(p, encoding="utf-8"))["u_hash"], kind
    return None, None


def main():
    intents = json.load(open(INTENTS, encoding="utf-8"))["intents"]
    order = [it["id"] for it in intents]
    nsys = {it["id"]: it["n_sys"] for it in intents}
    mats = load_gate_matrices()
    files = sorted(glob.glob(os.path.join(SUB_DIR, "*.bloq.json")))
    print("=" * 88)
    print(f"App-Bloq Cross-Model Ingest (독립 회로 분해, dir={_DIRNAME})")
    print("=" * 88)
    if not files:
        print(f"  제출물 없음: {SUB_DIR}\\*.bloq.json")
        print("  → APP-BLOQ-BRIEF.md + GATE-VOCABULARY.json + app_intents.json 로 런타임 지시 후 배치.")
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
                V = assemble_circuit(s["circuit"], nsys[iid], mats)
                uh = vs.hash_unitary(V)
                depth = len(s["circuit"])
            except Exception as e:
                warn.append(f"{rt}/{iid}: assemble 실패 {e}"); by[iid].append(
                    {"runtime": rt, "weights_id": wid or rt, "u_hash": None, "err": str(e)[:50], "depth": None}); continue
            by[iid].append({"runtime": rt, "weights_id": wid or rt, "u_hash": uh, "depth": depth})

    report = {"runtimes": [os.path.basename(f).split('.')[0] for f in files], "warnings": warn, "apps": {}}
    print("\n" + "-" * 88)
    est = match_n = 0
    for iid in order:
        rows = [r for r in by[iid] if r["u_hash"]]
        srcs = [C.Source(f"{iid}_{r['runtime']}", "model", r["weights_id"], r["u_hash"]) for r in rows]
        res = C.establish_truth(iid, srcs, N=2)
        ref, kind = reference_uhash(iid)
        match = (res.key == ref) if (res.key and ref) else None
        if res.status == "ESTABLISHED":
            est += 1
        if match:
            match_n += 1
        depths = sorted({r["depth"] for r in rows})
        report["apps"][iid] = {"status": res.status, "grade": res.grade, "key": res.key,
                               "n_runtimes": len(rows), "distinct_circuits_depths": depths,
                               "reference": ref, "reference_kind": kind, "reference_match": match,
                               "distribution": res.distribution, "escalation": res.escalation,
                               "votes": [{"runtime": r["runtime"], "u_hash": (r["u_hash"] or "ERR")[:16],
                                          "depth": r["depth"], "agrees": (r["u_hash"] == res.key) if res.key else None}
                                         for r in by[iid]]}
        icon = {"ESTABLISHED": "✅", "DIVERGENT": "⚠️", "INSUFFICIENT": "△"}.get(res.status, "?")
        line = f"  {icon} {iid:12} {res.status:12}"
        if res.key:
            line += f" {res.grade:10} votes={len(rows)} depths={depths}  ⟺{kind}:" + ("✓일치" if match else "✗불일치")
        else:
            line += f"  {res.escalation[:44]}"
        print(line)
        if res.key:
            for v in report["apps"][iid]["votes"]:
                if v["agrees"] is False:
                    print(f"        ✗ dissent {v['runtime']:10} {v['u_hash']}.. (회로가 잘못된 유니터리 산출)")

    print("-" * 88)
    print(f"앱 구현 확립 {est}/{len(order)} · 봉인앱/게이트 일치 {match_n}/{len(order)}")
    print("  (서로 다른 회로가 같은 u_hash 로 수렴 = 구현 독립 교차검증)")
    print("=" * 88)
    report["summary"] = {"total": len(order), "established": est, "reference_match": match_n}
    json.dump(report, open(REPORT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"리포트: {os.path.relpath(REPORT, ROOT)}")
    return 0 if est == len(order) and match_n == len(order) else 1


if __name__ == "__main__":
    sys.exit(main())
