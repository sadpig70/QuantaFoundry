"""test_clifford_seal.py — Tier-2 Clifford 기호 봉인 검증 (SmallNBound 탈출 II)."""
import sys, os, json, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clifford_seal as cs          # noqa: E402
import verify_seal as vs            # noqa: E402
from qualtran.bloqs.basic_gates import CNOT, Hadamard, TwoBitSwap, Toffoli, TGate  # noqa: E402

EX = os.path.abspath(os.path.join(HERE, "..", "examples", "clifford"))
PASS = 0
FAIL = 0


def check(cond, label):
    global PASS, FAIL
    PASS, FAIL = (PASS + 1, FAIL) if cond else (PASS, FAIL + 1)
    print(f"  {'✅' if cond else '❌'} {label}")


def seal(pg, store):
    return vs.main([os.path.join(EX, pg), "--out", store])


print("=" * 60)
print("clifford_seal — Tier-2 기호 봉인")
print("=" * 60)
# Clifford 판정
check(cs.is_clifford(CNOT())[0] and cs.is_clifford(Hadamard())[0] and cs.is_clifford(TwoBitSwap())[0],
      "Clifford 판정: CNOT·H·SWAP = True")
check(not cs.is_clifford(Toffoli())[0] and not cs.is_clifford(TGate())[0],
      "non-Clifford 판정: Toffoli·T = False")
# tableau 해시 결정론 + 구별
h1, n1 = cs.canonical_tableau_hash(CNOT())
h2, _ = cs.canonical_tableau_hash(CNOT())
hs, _ = cs.canonical_tableau_hash(TwoBitSwap())
check(h1 == h2 and n1 == 2, "tableau 해시 결정론(2회 동일)")
check(h1 != hs, "CNOT ≠ SWAP tableau 해시 (구별)")

print("\n" + "=" * 60)
print("verify_seal Tier-2 경로 (CLI)")
print("=" * 60)
with tempfile.TemporaryDirectory() as d:
    # 소규모 (advisory 교차검증)
    rc = seal("cnot_t2.pg", d)
    sd = json.load(open(os.path.join(d, "cnot_clifford.sealed.json"))) if rc == 0 else {}
    check(rc == 0 and sd.get("tier") == 2 and sd.get("contract") == "C1-C4(clifford)",
          "소규모 Clifford → tier=2 봉인")
    # 대형 (dense 2^20 미사용)
    rc = seal("ghz20.pg", d)
    sd = json.load(open(os.path.join(d, "ghz20.sealed.json"))) if rc == 0 else {}
    check(rc == 0 and sd.get("n_sys") == 20 and sd.get("tier") == 2,
          "20큐비트 Clifford → 봉인 (Tier-0이면 2^20 불가)")
    check(sd.get("resource", {}).get("clifford") == 20, "자원 clifford:20 (H+19 CNOT)")
    # 결정론 (2폴더 byte-identical)
    with tempfile.TemporaryDirectory() as d2:
        seal("ghz20.pg", d2)
        a = open(os.path.join(d, "ghz20.sealed.json"), "rb").read()
        b = open(os.path.join(d2, "ghz20.sealed.json"), "rb").read()
        check(a == b, "Tier-2 봉인 결정론 (byte-identical)")
    # non-Clifford 거부
    rc = seal("bad_nonclifford.pg", d)
    check(rc == 1, "tier=clifford인데 Toffoli → 거부 (non_clifford)")

print("\n" + "=" * 60)
print(f"결과: {PASS} PASS / {FAIL} FAIL")
print("=" * 60)
sys.exit(1 if FAIL else 0)
