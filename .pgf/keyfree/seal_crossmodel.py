"""seal_crossmodel.py — cross-model golden(Round1) + bloq(Round2) 결합 → 봉인 → registry.

흐름 (gate 별):
  golden_code (런타임 G)  +  bloq_code (런타임 B, G≠B)
   → golden.pg(id=golden,id=meta author=G) + bloq.pg(id=bloq,id=meta author=B)
   → autoforge.verify_one (오라클 봉인 + anti-swap[frozen consensus key] + 결정론 + registry)
   → SEALED 시 specs/modules/<id>.pg 기록.

golden 작성 런타임 ≠ bloq 작성 런타임 (cross_independent) — 동반오류 방화벽.
정답키는 consensus_keys.json(frozen, cross-model⊕proof) 을 autoforge 가 자동 로드.

사용:
  python .pgf/keyfree/seal_crossmodel.py                       # 실봉인 → registry/modules
  python .pgf/keyfree/seal_crossmodel.py --registry <dir> --store <dir> --no-spec   # 스모크(스크래치)
"""
import os, sys, json, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, ".pgf", "autoforge"))
import autoforge as af                 # noqa: E402  (verify_one, combine — 재사용)
from registry import Registry          # noqa: E402

CM = os.path.join(ROOT, "_workspace", "crossmodel")
GOLD_DIR = os.path.join(CM, "submissions")          # *.submission.json (golden_code)
BLOQ_DIR = os.path.join(CM, "submissions_bloq")     # *.bloq.json (bloq_code)
INTENTS = os.path.join(CM, "intents.json")
SPECS = os.path.join(ROOT, "specs", "modules")


def _load(dir_, pat, code_field):
    """{gate: [(runtime, weights_id, code), ...]} 로드."""
    out = {}
    for f in sorted(glob.glob(os.path.join(dir_, pat))):
        d = json.load(open(f, encoding="utf-8"))
        rt, wid = d.get("runtime", os.path.basename(f).split(".")[0]), d.get("weights_id")
        for s in d.get("submissions", []):
            if s.get(code_field):
                out.setdefault(s["id"], []).append((rt, wid or rt, s[code_field]))
    return out


def _pick_pair(golds, bloqs):
    """golden 작성자 ≠ bloq 작성자(다른 weights) 한 쌍 선택. 없으면 None."""
    for g in golds:
        for b in bloqs:
            if g[1] != b[1]:                      # 다른 weights_id
                return g, b
    return None, None


def _rel(p):
    try:
        return os.path.relpath(p, ROOT)
    except ValueError:
        return p


def _write_pg(path, code_block_id, code, meta):
    txt = (f"```python id={code_block_id}\n{code.strip()}\n```\n"
           f"```json id=meta\n{json.dumps(meta)}\n```\n")
    open(path, "w", encoding="utf-8").write(txt)


def main():
    args = sys.argv[1:]
    reg_dir = (args[args.index("--registry") + 1] if "--registry" in args
               else os.path.join(ROOT, "registry", "modules"))
    store = (args[args.index("--store") + 1] if "--store" in args
             else os.path.join(HERE, "_seal_store"))
    write_spec = "--no-spec" not in args
    only = [a for a in args if not a.startswith("--") and a not in (reg_dir, store)]

    intents = json.load(open(INTENTS, encoding="utf-8"))["intents"]
    meta_by = {it["id"]: it for it in intents}
    targets = [it["id"] for it in intents if it["round"] == "B"]
    if only:
        targets = [t for t in targets if t in only]

    golds = _load(GOLD_DIR, "*.submission.json", "golden_code")
    bloqs = _load(BLOQ_DIR, "*.bloq.json", "bloq_code")
    os.makedirs(store, exist_ok=True)
    os.makedirs(reg_dir, exist_ok=True)
    work = os.path.join(store, "_pg")
    os.makedirs(os.path.join(work, "golden"), exist_ok=True)
    os.makedirs(os.path.join(work, "bloq"), exist_ok=True)
    reg = Registry(reg_dir)

    print("=" * 84)
    print(f"Cross-Model Seal — golden(R1) ⊕ bloq(R2), 정답키=consensus_keys.json(frozen)")
    print(f"  registry: {_rel(reg_dir)}  | spec쓰기: {write_spec}")
    print("=" * 84)
    if not bloqs:
        print(f"  bloq 제출 없음: {_rel(BLOQ_DIR)}\\*.bloq.json")
        print("  → BLOQ-BRIEF.md + intents.json 로 런타임에 bloq 작업 지시 후 제출물 배치.")
        return 1

    results = []
    for iid in targets:
        g_list, b_list = golds.get(iid, []), bloqs.get(iid, [])
        if not g_list or not b_list:
            print(f"  ⏳ {iid:9} golden={len(g_list)} bloq={len(b_list)} — 제출 부족"); continue
        g, b = _pick_pair(g_list, b_list)
        if g is None:
            g, b = g_list[0], b_list[0]          # 같은 weights뿐 → cross_independent=False 로 진행
        m = meta_by[iid]
        meta_g = {"id": iid, "n_sys": m["n_sys"], "n_anc": 0, "author": g[0]}
        meta_b = {"id": iid, "n_sys": m["n_sys"], "n_anc": 0, "author": b[0]}
        gp = os.path.join(work, "golden", f"{iid}.pg")
        bp = os.path.join(work, "bloq", f"{iid}.pg")
        _write_pg(gp, "golden", g[2], meta_g)
        _write_pg(bp, "bloq", b[2], meta_b)

        res = af.verify_one(iid, gp, bp, store, reg)
        res["golden_by"], res["bloq_by"] = g[0], b[0]
        results.append(res)

        icon = {"SEALED": "✅", "REPAIR": "🔧", "REJECT": "❌"}.get(res["status"], "?")
        line = f"  {icon} {iid:9} {res['status']:7} golden={g[0]:9}≠bloq={b[0]:9}"
        if res["status"] == "SEALED":
            xi = "✓독립" if res.get("cross_independent") else "✗동일"
            det = "✓재현" if res.get("deterministic") else "✗재현"
            line += f" [{xi} {det}] u_hash={res['u_hash'][:12]}.."
            if write_spec:
                src = os.path.join(store, f"{iid}.combined.pg")
                if os.path.exists(src):
                    os.makedirs(SPECS, exist_ok=True)
                    open(os.path.join(SPECS, f"{iid}.pg"), "w", encoding="utf-8").write(
                        open(src, encoding="utf-8").read())
                    line += " spec✓"
        else:
            line += f" @{res.get('stage')} {res.get('signal','')[:40]}"
        print(line)

    sealed = sum(1 for r in results if r["status"] == "SEALED")
    print("=" * 84)
    print(f"봉인 {sealed}/{len(results)} (cross-model golden⊕bloq, 사람 seed 0)")
    print("=" * 84)
    json.dump({"results": results, "sealed": sealed, "total": len(results)},
              open(os.path.join(CM, "SEAL-RESULT.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    return 0 if sealed == len(results) and results else 1


if __name__ == "__main__":
    sys.exit(main())
