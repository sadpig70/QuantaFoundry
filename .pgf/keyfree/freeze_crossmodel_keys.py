"""freeze_crossmodel_keys.py — cross-model 검증 완료된 Round B 키를 consensus_keys.json 에 frozen 등록.

입력: _workspace/crossmodel/CONSENSUS-REPORT.json (ingest_crossmodel 산출).
각 Round B gate 에 대해 6개 cross-model 출처(서로 다른 weights) + 독립 ground-truth(proof/formal-spec)
를 establish_truth 로 *재확립* 한 뒤(복사가 아닌 합의), 기존 8개 베이스 키와 병합해 저장한다.

frozen 키는 불변(결정론 신성불가침). 이미 frozen 된 키는 값이 바뀌면 에러로 중단한다.
사용:  python .pgf/keyfree/freeze_crossmodel_keys.py
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
import consensus as C                  # noqa: E402
import ingest_crossmodel as ing        # noqa: E402

REPORT = os.path.join(ROOT, "_workspace", "crossmodel", "CONSENSUS-REPORT.json")
KEYS = os.path.join(HERE, "consensus_keys.json")


def main():
    rep = json.load(open(REPORT, encoding="utf-8"))
    keys = json.load(open(KEYS, encoding="utf-8")) if os.path.exists(KEYS) else {}

    added, kept = [], list(keys)
    for iid, e in rep["intents"].items():
        if e["round"] != "B" or e["status"] != "ESTABLISHED":
            continue
        # cross-model 출처(weights별 독립) + 독립 ground-truth(proof/formal-spec) 재확립
        sources = [C.Source(f"{iid}_{v['runtime']}", "model", v["weights_id"], e["key"])
                   for v in e["votes"] if v.get("agrees")]
        gt = e.get("ground_truth")
        if gt:
            sources.append(C.Source(f"{iid}_gt", "proof", "formal-spec", gt))
        res = C.establish_truth(iid, sources, N=2)
        if res.status != "ESTABLISHED":
            print(f"  ❌ {iid}: 재확립 실패 {res.status} — 건너뜀"); continue
        if res.key != e["key"]:
            print(f"  ❌ {iid}: 재확립 키 불일치 — 중단"); return 1

        entry = {"key": res.key, "status": "ESTABLISHED", "grade": res.grade,
                 "provenance": res.provenance, "key_version": 1, "frozen": True,
                 "source": "cross-model+proof",
                 "n_independent_models": len({v["weights_id"] for v in e["votes"] if v.get("agrees")}),
                 "ground_truth_match": e.get("ground_truth_match")}
        if iid in keys:
            old = keys[iid]
            if old.get("frozen") and old.get("key") != res.key:
                print(f"  ❌ {iid}: 이미 frozen 된 키와 다름 (불변 위반) — 중단"); return 1
            print(f"  ↻ {iid}: 기존 키 갱신(동일 값)")
        else:
            added.append(iid)
        keys[iid] = entry

    json.dump(keys, open(KEYS, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("=" * 78)
    print(f"frozen 등록: 신규 {len(added)}개 {added}")
    print(f"consensus_keys.json 총 {len(keys)}개 키: {sorted(keys)}")
    for iid in added:
        k = keys[iid]
        print(f"  ✅ {iid:9} {k['grade']:12} models={k['n_independent_models']} "
              f"GT={'✓' if k['ground_truth_match'] else '✗'} key={k['key'][:16]}..")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
