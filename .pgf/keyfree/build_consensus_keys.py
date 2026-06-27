"""build_consensus_keys.py — 베이스 8모듈의 ANSWER_KEY 를 합의로 자동 생성.

각 모듈: model 출처(기존 페르소나 봉인 u_hash) + proof 출처(독립 대수 유도) 가 수렴하면
consensus_key 창발. 인간 seed 였던 키가 독립 수렴으로 재확립된다.
"""
import os, sys, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(ROOT)
import consensus as C

MODULES = ["x_gate", "z_gate", "h_gate", "cnot", "swap2", "toffoli", "qft2", "qft3"]
keys = {}
print("=" * 78)
print("KeyFreeConsensus — 베이스 8모듈 키 자동 확립 (model ⊕ proof 수렴)")
print("=" * 78)
for m in MODULES:
    sealed = json.load(open(f"registry/modules/{m}.sealed.json"))["u_hash"]
    proof_u = C.uhash(C.PROOF_GENERATORS[m]())
    sources = [
        C.Source(f"{m}_model", "model", "claude", sealed),       # 페르소나(LLM) 봉인
        C.Source(f"{m}_proof", "proof", "algebraic", proof_u),   # 독립 대수 유도
    ]
    r = C.establish_truth(m, sources, N=2)
    keys[m] = {"key": r.key, "status": r.status, "grade": r.grade, "provenance": r.provenance,
               "key_version": 1, "frozen": r.status == "ESTABLISHED"}
    icon = "✅" if r.status == "ESTABLISHED" else "❌"
    match = "수렴" if sealed == proof_u else f"분기(model={sealed[:8]} proof={proof_u[:8]})"
    print(f"  {icon} {m:9} {r.status:11} {r.grade or '':12} [{match}] key={(r.key or '')[:16]}")

out_path = os.path.join(ROOT, ".pgf", "keyfree", "consensus_keys.json")
json.dump(keys, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
n_ok = sum(1 for v in keys.values() if v["status"] == "ESTABLISHED")
print("=" * 78)
print(f"확립 {n_ok}/{len(MODULES)} (인간 seed 0 — 전부 model⊕proof 독립 수렴) → {out_path}")
print("=" * 78)
