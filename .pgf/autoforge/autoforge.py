"""autoforge.py — QuantaFoundry 자율 멀티페르소나 봉인 오케스트레이터.

F1(멀티페르소나 격리 생성)은 부모 에이전트가 Agent 도구로 수행해 submissions/{golden,bloq}/
*.pg 에 떨궈둔다. 이 스크립트는 F2(결정론 검증·봉인·보관)를 담당한다 — AI 개입 없음.

흐름:  submissions/golden/<id>.pg + submissions/bloq/<id>.pg
   → combine(intent 정합 검사) → verify_seal(오라클, 사용만) → 정답키 대조(anti-swap)
   → registry.register(INV1~3) → byte-identical 재봉인 재현 검증.

경계 규율: 오라클(verify_seal/registry)은 *사용만*, 복제하지 않는다. 봉인 못 통과 = 미존재.

사용:  python autoforge.py
"""
import sys, os, io, json, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.abspath(os.path.join(HERE, "..", "..", ".agents", "skills", "qpgf-oracle", "scripts"))
sys.path.insert(0, SCRIPTS)
import verify_seal as vs        # noqa: E402  (오라클 — 사용만)
from registry import Registry   # noqa: E402

# 정답 u_hash 출처: KeyFreeConsensus 합의(consensus_keys.json) 우선, 없으면 아래 fallback.
#   합의 = model(페르소나 봉인) ⊕ proof(독립 대수) 수렴으로 자율 확립 (인간 seed 0).
_FALLBACK_KEY = {
    "x_gate":  "7dc1df52d07dd7428a4c2ab9ba2e3f982b6dea78d0ee6eb2f7ea865faa19ba5a",
    "z_gate":  "1e3c0f2fa747f4fac16a11dd3959f83cc23b71b26e66528032c6223af01846e4",
    "h_gate":  "0d6a0b7a9a19ad2e65004d4811b3907a5f1c8f4edbde59c0fefd9d3ff260b90c",
    "cnot":    "3913bcef764f36b8b170748f1fe1641d3aa3d06e9e317cb0b553bd9bc58fd4a5",
    "swap2":   "e6255e2f105a97829f59ec648c92ef42d7fb19bd952f0c8534371e352e77153e",
    "toffoli": "e663b43043af6b78ca6b8fae14b5f38d2ae902d96db3aeafa16ce89efdf8f17d",
    "qft2":    "90dbc731bb8c7e80f8ff62b9be6975bf453dbbb3dc645a25960cfba3477dad82",
    "qft3":    "340b5f344fae9b997d17883cd1bc10bbcbd4c1c37252ce889c26d0e4adc74bed",
}


def _load_answer_key():
    """KeyFreeConsensus 합의 키(consensus_keys.json) 우선 로드, 없으면 fallback(인간 seed)."""
    ck = os.path.join(HERE, "..", "keyfree", "consensus_keys.json")
    if os.path.exists(ck):
        data = json.load(open(ck, encoding="utf-8"))
        keys = {m: v["key"] for m, v in data.items() if v.get("key") and v.get("frozen")}
        if keys:
            return keys
    return _FALLBACK_KEY


ANSWER_KEY = _load_answer_key()


def _meta(blocks):
    return json.loads(blocks["meta"]) if "meta" in blocks else None


def combine(golden_path, bloq_path):
    """격리 두 제출(golden 작성자 ≠ bloq 작성자)을 단일 .pg로 결합."""
    gb = vs._extract_blocks(open(golden_path, encoding="utf-8").read())
    bb = vs._extract_blocks(open(bloq_path, encoding="utf-8").read())
    if "golden" not in gb:
        raise ValueError(f"golden 제출에 id=golden 블록 없음: {golden_path}")
    if "bloq" not in bb:
        raise ValueError(f"bloq 제출에 id=bloq 블록 없음: {bloq_path}")
    gm, bm = _meta(gb), _meta(bb)
    if gm is None or bm is None:
        raise ValueError("양쪽 제출에 id=meta 필요")
    for k in ("id", "n_sys", "n_anc"):   # intent 정합: 두 페르소나가 같은 의도를 받았는가
        if str(gm.get(k)) != str(bm.get(k)):
            raise ValueError(f"intent_mismatch: golden.meta[{k}]={gm.get(k)} ≠ bloq.meta[{k}]={bm.get(k)}")
    meta = {"id": bm["id"], "n_sys": bm["n_sys"], "n_anc": bm.get("n_anc", 0)}
    text = (f"```python id=bloq\n{bb['bloq'].strip()}\n```\n"
            f"```python id=golden\n{gb['golden'].strip()}\n```\n"
            f"```json id=meta\n{json.dumps(meta)}\n```\n")
    return text, meta["id"], gm.get("author", "A"), bm.get("author", "B")


def _seal(text, cid, store):
    """결합 텍스트를 봉인하고 sealed.json 경로 반환 (없으면 None)."""
    tmp = os.path.join(store, f"{cid}.combined.pg")
    os.makedirs(store, exist_ok=True)
    open(tmp, "w", encoding="utf-8").write(text)
    err = io.StringIO()
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
        rc = vs.main([tmp, "--out", store])
    sealed = os.path.join(store, f"{cid}.sealed.json")
    return (sealed, "") if rc == 0 and os.path.exists(sealed) else (None, err.getvalue().strip())


def verify_one(intent_id, gp, bp, store, reg):
    out = {"id": intent_id}
    try:
        text, cid, ga, ba = combine(gp, bp)
    except Exception as e:
        return {**out, "status": "REJECT", "stage": "combine", "signal": str(e)}
    if cid != intent_id:                                  # C-bind: meta.id ↔ intent id 결박
        return {**out, "status": "REJECT", "stage": "c_bind",
                "signal": f"id_mismatch: meta.id={cid} != intent={intent_id}"}
    out["cross_independent"] = (ga != ba)
    out["golden_author"], out["bloq_author"] = ga, ba

    sealed_path, sig = _seal(text, cid, store)
    if sealed_path is None:
        return {**out, "status": "REPAIR", "stage": "verify_seal", "signal": sig}
    sealed = json.load(open(sealed_path, encoding="utf-8"))

    exp = ANSWER_KEY.get(cid)                    # anti-swap / 동반오류 탐지
    if exp and sealed["u_hash"] != exp:
        return {**out, "status": "REJECT", "stage": "anti_swap",
                "signal": f"u_hash≠expected", "got": sealed["u_hash"][:16]}

    # byte-identical 재봉인 재현 (결정론)
    rep_store = os.path.join(store, "_rerun")
    s2, _ = _seal(text, cid, rep_store)
    a = open(sealed_path, "rb").read()
    b = open(s2, "rb").read() if s2 else b""
    out["deterministic"] = (a == b)

    # registry 등록 (INV1: 재검증 후 admit)
    rr = reg.register(os.path.join(store, f"{cid}.combined.pg"))
    out["registered"] = bool(rr.admitted)
    if not rr.admitted:
        return {**out, "status": "REPAIR", "stage": "register", "signal": rr.reason}

    return {**out, "status": "SEALED", "u_hash": sealed["u_hash"],
            "tier": sealed.get("tier"), "resource": sealed.get("resource")}


def main():
    sub = os.path.join(HERE, "submissions")
    gdir, bdir = os.path.join(sub, "golden"), os.path.join(sub, "bloq")
    store = os.path.join(HERE, "_store")
    reg = Registry(os.path.join(HERE, "..", "..", "registry", "modules"))
    results = []
    print("=" * 76)
    print("QuantaFoundry AutoForge — 자율 멀티페르소나 봉인 (golden 페르소나 ≠ bloq 페르소나)")
    print("=" * 76)
    intents = sorted(f[:-3] for f in os.listdir(gdir)) if os.path.isdir(gdir) else []
    for iid in intents:
        gp, bp = os.path.join(gdir, f"{iid}.pg"), os.path.join(bdir, f"{iid}.pg")
        if not os.path.exists(bp):
            print(f"  ⏳ {iid:10} bloq 제출 미도착"); continue
        res = verify_one(iid, gp, bp, store, reg)
        results.append(res)
        icon = {"SEALED": "✅", "REPAIR": "🔧", "REJECT": "❌"}.get(res["status"], "?")
        line = f"  {icon} {iid:10} {res['status']:7}"
        if res["status"] == "SEALED":
            xi = "✓독립" if res.get("cross_independent") else "✗동일"
            det = "✓재현" if res.get("deterministic") else "✗재현"
            rg = "✓reg" if res.get("registered") else "✗reg"
            line += f" u_hash={res['u_hash'][:12]}.. [{xi} {det} {rg}] tier={res.get('tier')}"
        else:
            line += f" @{res.get('stage')} {res.get('signal','')[:44]}"
        print(line)

    print("\n" + "=" * 76)
    sealed_n = sum(1 for r in results if r["status"] == "SEALED")
    xind = sum(1 for r in results if r["status"] == "SEALED" and r.get("cross_independent"))
    det_n = sum(1 for r in results if r.get("deterministic"))
    reg_n = sum(1 for r in results if r.get("registered"))
    print(f"봉인 {sealed_n}/{len(results)} · 교차독립 {xind} · 결정론재현 {det_n} · registry등록 {reg_n}")
    print("=" * 76)
    # 리포트 저장
    rep = os.path.join(HERE, "FORGE-RESULT.json")
    json.dump({"results": results, "sealed": sealed_n, "total": len(results),
               "cross_independent": xind, "deterministic": det_n, "registered": reg_n},
              open(rep, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return 0 if sealed_n == len(results) and len(results) > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
