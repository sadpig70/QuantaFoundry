"""test_zx_seal.py — Tier-3 Clifford+T 봉인 검증 (ZX 등가, SmallNBound 탈출 III)."""
import sys, os, json, time, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import zx_seal as zs               # noqa: E402
import verify_seal as vs           # noqa: E402
import cirq                        # noqa: E402

EX = os.path.abspath(os.path.join(HERE, "..", "examples", "clifford_t"))
PASS = 0
FAIL = 0


def check(cond, label):
    global PASS, FAIL
    PASS, FAIL = (PASS + 1, FAIL) if cond else (PASS, FAIL + 1)
    print(f"  {'✅' if cond else '❌'} {label}")


def seal(pg, store):
    return vs.main([os.path.join(EX, pg), "--out", store])


print("=" * 60)
print("zx_seal — Tier-3 Clifford+T (ZX 등가)")
print("=" * 60)
# 코어 ZX 등가 (cirq 두 회로) — dense 미사용
q = cirq.LineQubit.range(2)
g = cirq.Circuit([cirq.H(q[0]), cirq.T(q[0]), cirq.CNOT(q[0], q[1])])
g_eq = cirq.Circuit([cirq.H(q[0]), cirq.T(q[0]), cirq.CNOT(q[0], q[1])] + [cirq.T(q[1])] * 8)   # +T^8=I
g_ne = cirq.Circuit([cirq.H(q[0]), cirq.T(q[0]), cirq.CNOT(q[0], q[1])] + [cirq.T(q[1])] * 3)   # +T^3≠I
zg, zeq, zne = zs.to_pyzx(g), zs.to_pyzx(g_eq), zs.to_pyzx(g_ne)
check(zeq.verify_equality(zg), "ZX: +T^8(=I) ≡ clean (구조다름·증명)")
check(not zne.verify_equality(zg), "ZX: +T^3(≠I) ≢ clean (거부)")
check(zs.circuit_hash(zg) == zs.circuit_hash(zs.to_pyzx(g)), "golden 회로해시 결정론")

print("\n" + "=" * 60)
print("verify_seal Tier-3 경로 (CLI)")
print("=" * 60)
with tempfile.TemporaryDirectory() as d:
    rc = seal("redundant_t.pg", d)
    sd = json.load(open(os.path.join(d, "redundant_t.sealed.json"))) if rc == 0 else {}
    check(rc == 0 and sd.get("tier") == 3 and sd.get("contract") == "C1-C4(zx)",
          "bloq+T^8 ≡ golden → tier=3 봉인")
    check(sd.get("u_hash") == zs.circuit_hash(zg), "u_hash == golden 참조회로 해시")
    # negative: 비등가 → 거부
    rc = seal("bad_t3.pg", d)
    check(rc == 1, "bloq+T^3 ≢ golden → 거부(zx_not_equivalent)")
    # 결정론
    with tempfile.TemporaryDirectory() as d2:
        seal("redundant_t.pg", d2)
        a = open(os.path.join(d, "redundant_t.sealed.json"), "rb").read()
        b = open(os.path.join(d2, "redundant_t.sealed.json"), "rb").read()
        check(a == b, "Tier-3 봉인 결정론 (byte-identical)")

print("\n" + "=" * 60)
print("규모: 16큐비트 Clifford+T 등가 (dense 2^16 미사용)")
print("=" * 60)
n = 16
qs = cirq.LineQubit.range(n)
ops = [cirq.H(qs[i]) for i in range(n)] + [cirq.CNOT(qs[i], qs[i + 1]) for i in range(n - 1)] + [cirq.T(qs[i]) for i in range(n)]
big = cirq.Circuit(ops)
big_eq = cirq.Circuit(ops + [cirq.T(qs[0])] * 8)   # +T^8=I
t0 = time.time()
ok = zs.to_pyzx(big_eq).verify_equality(zs.to_pyzx(big))
dt = time.time() - t0
check(ok, f"16q Clifford+T 등가 증명 ({dt:.2f}s, dense 2^16 미사용)")

print("\n" + "=" * 60)
print("다중전략 폴백 (ZX → dense → QCEC, 전부 sound)")
print("=" * 60)
check(zs.dense_equiv(g, g_eq), "dense: +T^8(=I) ≡ clean (전역위상 무시)")
check(not zs.dense_equiv(g, g_ne), "dense: +T^3(≠I) ≢ clean")
qv = zs.qcec_equiv(g, g_eq)
if qv is None:
    print("  ⏭ QCEC 미설치 — skip (선택 의존성)")
else:
    check(qv is True, "QCEC: +T^8(=I) ≡ clean (증명 등가)")
    check(zs.qcec_equiv(g, g_ne) is not True, "QCEC: +T^3(≠I) 미증명·비등가 → 거부")

print("\n" + "=" * 60)
print(f"결과: {PASS} PASS / {FAIL} FAIL")
print("=" * 60)
sys.exit(1 if FAIL else 0)
