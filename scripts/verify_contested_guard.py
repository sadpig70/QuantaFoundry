"""verify_contested_guard.py — contested near-tie guard 의 결정론 안전성 보증 (파일 미변경).

establish_truth 에 추가된 contested guard(top-2 독립단위 동률 → CONTESTED)가 기존 frozen 키를
바꾸지 않음을 *메모리상* 증명한다(consensus_keys.json 재생성 금지 — 봉인점검 교훈).
주의: frozen consensus_keys.json 은 전체 23키이며, 본 guard 가 출처를 재구성해 검증하는 대상은
그 중 15키(base 8 + cross-model 7)다 — 나머지 8키(P0 등)는 재구성 출처가 본 스크립트 범위 밖.
  1. 검증대상 15키(base 8 + cross-model 7)의 출처를 build/freeze 와 동일하게 재구성 → 신규
     establish_truth 재확립 → status==ESTABLISHED & key==저장값 & grade==저장값 대조 (단일-그룹 수렴 = runner_up 0 = guard 미발동).
  2. guard 동작 단위테스트: 단일그룹→ESTABLISHED, 4-2→ESTABLISHED, 3-3→CONTESTED, 2-2→CONTESTED.

사용:  python scripts/verify_contested_guard.py
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, ".pgf", "keyfree"))
import consensus as C  # noqa: E402

KEYS = os.path.join(ROOT, ".pgf", "keyfree", "consensus_keys.json")
XREPORT = os.path.join(ROOT, "_workspace", "crossmodel", "CONSENSUS-REPORT.json")
BASE = ["x_gate", "z_gate", "h_gate", "cnot", "swap2", "toffoli", "qft2", "qft3"]
PASS, FAIL = [], []


def chk(c, m):
    (PASS if c else FAIL).append(m)
    print(("  PASS " if c else "  FAIL ") + m)


def base_sources(m):
    sealed = json.load(open(os.path.join(ROOT, "registry", "modules", f"{m}.sealed.json")))["u_hash"]
    proof_u = C.uhash(C.PROOF_GENERATORS[m]())
    return [C.Source(f"{m}_model", "model", "claude", sealed),
            C.Source(f"{m}_proof", "proof", "algebraic", proof_u)]


def xmodel_sources(iid, e):
    s = [C.Source(f"{iid}_{v['runtime']}", "model", v["weights_id"], e["key"])
         for v in e["votes"] if v.get("agrees")]
    if e.get("ground_truth"):
        s.append(C.Source(f"{iid}_gt", "proof", "formal-spec", e["ground_truth"]))
    return s


def main():
    keys = json.load(open(KEYS, encoding="utf-8"))
    print("=" * 80)
    print(f"contested guard 결정론 보증 — frozen 키 불변 (전체 {len(keys)}키 · 본 검증대상 15키=base 8+cross-model 7)")
    print("=" * 80)

    # 1. base 8키
    for m in BASE:
        if m not in keys:
            chk(False, f"{m}: consensus_keys 에 없음"); continue
        r = C.establish_truth(m, base_sources(m), N=2)
        good = (r.status == "ESTABLISHED" and r.key == keys[m]["key"] and r.grade == keys[m]["grade"])
        chk(good, f"{m:9} status={r.status} key={'==' if r.key==keys[m]['key'] else '≠'} grade={r.grade}")

    # 2. cross-model 7키 (CONSENSUS-REPORT.json 출처 재구성)
    if os.path.exists(XREPORT):
        rep = json.load(open(XREPORT, encoding="utf-8"))
        for iid, e in rep.get("intents", {}).items():
            if e.get("round") != "B" or e.get("status") != "ESTABLISHED" or iid not in keys:
                continue
            r = C.establish_truth(iid, xmodel_sources(iid, e), N=2)
            good = (r.status == "ESTABLISHED" and r.key == keys[iid]["key"] and r.grade == keys[iid]["grade"])
            chk(good, f"{iid:9} status={r.status} key={'==' if r.key==keys[iid]['key'] else '≠'} grade={r.grade}")
    else:
        print(f"  (참고) {XREPORT} 없음 — cross-model 재구성 생략")

    # 3. guard 단위테스트 (model 출처 N개)
    print("\n  guard 단위테스트:")

    def mk(splits):  # splits=[(hash,count)...] count=distinct weights
        src = []
        for h, n in splits:
            for i in range(n):
                src.append(C.Source(f"{h}_{i}", "model", f"w_{h}_{i}", h))
        return src
    cases = [("단일그룹 6", [("A", 6)], "ESTABLISHED"),
             ("4-2", [("A", 4), ("B", 2)], "ESTABLISHED"),
             ("3-3", [("A", 3), ("B", 3)], "CONTESTED"),
             ("2-2", [("A", 2), ("B", 2)], "CONTESTED"),
             ("3-2-1", [("A", 3), ("B", 2), ("C", 1)], "ESTABLISHED")]
    for name, sp, exp in cases:
        r = C.establish_truth(name, mk(sp), N=2)
        chk(r.status == exp, f"{name:9} -> {r.status} (expect {exp}) dist={r.distribution}")

    print("=" * 80)
    ok = not FAIL
    print(f"{f'ALL PASS — guard 결정론 안전(frozen 전체 {len(keys)}키 불변·검증대상 15)' if ok else 'FAIL 있음'} · pass={len(PASS)} fail={len(FAIL)}")
    print("=" * 80)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
