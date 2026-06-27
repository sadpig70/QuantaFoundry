"""test_contracts.py — contracts.py 검증.

확인 항목:
  T1 Qualtran 게이트 → align="reverse" 정렬 → C1~C4 PASS + qcore golden 일치
  T2 qcore.QModule 과 동등한 verdict (이식 충실성)
  T3 위반 케이스(비유니터리·ancilla 누출·golden 불일치·차원불일치) 거부
  T4 compose: 합성 = 행렬곱, 인터페이스 불일치 거부
"""
import sys, os
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from contracts import (  # noqa: E402
    run_contracts, compose, reverse_qubit_order, matches_golden,
    check_c1_c2, embed_unitary, check_isometry, run_contracts_iso,
    classify_contract, golden_delta, ContractViolation, ATOL,
)

# qcore 동등성 비교용 (테스트 한정 의존; 배포 번들은 self-contained).
# 상대경로: scripts → repo root(.agents/skills/qpgf-oracle/scripts 에서 4단계 상위) → qcore
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "qcore")))
from qcore import build_unitary, QModule, Resource, ContractViolation as QCV  # noqa: E402

import qualtran.bloqs.basic_gates as bg  # noqa: E402

PASS = 0
FAIL = 0


def check(cond, label):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  ✅ {label}")
    else:
        FAIL += 1
        print(f"  ❌ {label}")


def qcore_golden(n, gates):
    U, _ = build_unitary(n, gates)
    return U


def toffoli_golden_le():
    M = np.eye(8, dtype=complex)
    for i in range(8):
        if ((i >> 0) & 1) and ((i >> 1) & 1):
            j = i ^ (1 << 2)
            M[:, i] = 0
            M[j, i] = 1
    return M


# (이름, n, qualtran bloq, qcore 게이트(little-endian) | None=Toffoli특례)
CASES = [
    ("X", 1, bg.XGate(), [("X", 0)]),
    ("H", 1, bg.Hadamard(), [("H", 0)]),
    ("S", 1, bg.SGate(), [("S", 0)]),
    ("T", 1, bg.TGate(), [("T", 0)]),
    ("Z", 1, bg.ZGate(), [("Z", 0)]),
    ("CNOT", 2, bg.CNOT(), [("CX", 0, 1)]),
    ("CZ", 2, bg.CZ(), [("CZ", 0, 1)]),
    ("Toffoli", 3, bg.Toffoli(), None),
]

print("=" * 64)
print("T1 — Qualtran → 정렬 → C1~C4 PASS + golden 일치")
print("=" * 64)
for name, n, bloq, gates in CASES:
    U_q = np.asarray(bloq.tensor_contract())
    golden = toffoli_golden_le() if name == "Toffoli" else qcore_golden(n, gates)
    res = run_contracts(U_q, n_sys=n, n_anc=0, golden=golden,
                        align="reverse", name=name)
    check(res.all_passed, f"[{name}] C1~C4 PASS (golden 포함) — signal={res.signal['contract']}")
    check(res.V is not None and matches_golden(res.V, golden),
          f"[{name}] 추출 V == golden")

print("\n" + "=" * 64)
print("T2 — qcore.QModule 과 동등한 verdict (이식 충실성)")
print("=" * 64)
for name, n, bloq, gates in CASES:
    U_q = np.asarray(bloq.tensor_contract())
    U_aligned = reverse_qubit_order(U_q, n)  # qcore 컨벤션으로 정렬
    # qcore 판정
    try:
        QModule(name, n, 0, U_aligned, Resource())
        qcore_ok = True
    except QCV:
        qcore_ok = False
    # contracts 판정
    res = run_contracts(U_q, n_sys=n, n_anc=0, align="reverse", name=name)
    check(qcore_ok == res.all_passed, f"[{name}] qcore({qcore_ok}) == contracts({res.all_passed})")

print("\n" + "=" * 64)
print("T3 — 위반 케이스 거부")
print("=" * 64)
# (a) 비유니터리 (C1/C2)
bad = np.array([[1, 0], [0, 2]], dtype=complex)
r = run_contracts(bad, 1, 0, name="nonunitary")
check(not r.all_passed and r.signal["contract"] in ("C1", "C2"),
      f"비유니터리 거부 → {r.signal['contract']}")

# (b) 차원 불일치 (C1)
r = run_contracts(np.eye(2, dtype=complex), n_sys=2, n_anc=0, name="dimbad")
check(not r.all_passed and r.signal["contract"] == "C1", f"차원불일치 거부 → {r.signal['contract']}")

# (c) ancilla 누출 (C3): 1 sys + 1 anc, anc를 더럽히는 CX(sys→anc)
# 게이트: ("CX", 0, 1) — q0=sys ctrl, q1=anc tgt. 입력 anc|0>가 sys=1일 때 anc=1로 누출.
U_leak, _ = build_unitary(2, [("H", 0), ("CX", 0, 1)])
r = run_contracts(U_leak, n_sys=1, n_anc=1, name="leak")
check(not r.all_passed and r.signal["contract"] == "C3", f"ancilla 누출 거부 → {r.signal['contract']}")

# (d) golden 불일치 (C4): X 유니터리에 H golden
Ux, _ = build_unitary(1, [("X", 0)])
Hg, _ = build_unitary(1, [("H", 0)])
r = run_contracts(Ux, 1, 0, golden=Hg, name="goldenbad")
check(not r.all_passed and r.signal["contract"] == "C4", f"golden 불일치 거부 → {r.signal['contract']}")

# (d2) 미세 위상왜곡 거부 (리뷰 반영): T의 π/4 위상을 +1e-5 왜곡 → C4 거부 (atol 1e-7 민감도)
T_true = np.diag([1, np.exp(1j * np.pi / 4)]).astype(complex)
T_eps = np.diag([1, np.exp(1j * (np.pi / 4 + 1e-5))]).astype(complex)
r = run_contracts(T_eps, 1, 0, golden=T_true, name="phase_eps")
check(not r.all_passed and r.signal["contract"] == "C4", f"미세 위상왜곡(+1e-5) 거부 → {r.signal['contract']}")

# (e) 정상 ancilla: 1 sys + 1 anc, anc 손대지 않는 회로 → PASS + V 추출
U_clean, _ = build_unitary(2, [("H", 0)])  # anc(q1) 미접촉
r = run_contracts(U_clean, n_sys=1, n_anc=1, name="clean_anc")
check(r.all_passed and r.V.shape == (2, 2), "청정 ancilla PASS + V(2x2) 추출")

print("\n" + "=" * 64)
print("T4 — compose (C4 합성)")
print("=" * 64)
# H 다음 H = I
H, _ = build_unitary(1, [("H", 0)])
V = compose(H, H, "H>>H")
check(matches_golden(V, np.eye(2, dtype=complex)), "H∘H == I")
# 인터페이스 불일치 거부
try:
    compose(np.eye(2, dtype=complex), np.eye(4, dtype=complex), "mismatch")
    check(False, "차원 불일치 합성 거부")
except ContractViolation:
    check(True, "차원 불일치 합성 거부 (C4)")

print("\n" + "=" * 64)
print("T5 — embed_unitary (이종 인터페이스 임베딩)")
print("=" * 64)
SW = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], dtype=complex)


def _swap3(a, b):  # 독립 구성: n=3 big-endian에서 와이어 a,b 교환 순열
    P = np.zeros((8, 8), dtype=complex)
    for i in range(8):
        bits = [(i >> (2 - w)) & 1 for w in range(3)]
        bits[a], bits[b] = bits[b], bits[a]
        j = sum(bit << (2 - w) for w, bit in enumerate(bits))
        P[j, i] = 1
    return P


# (a) Swap2 임베딩 == 독립 3큐비트 swap 순열 (전 와이어쌍)
for tw in ([0, 1], [1, 2], [0, 2]):
    E = embed_unitary(SW, tw, 3)
    check(np.allclose(E, _swap3(*tw)), f"embed Swap2 on {tw} == 독립 3q-swap")
# (b) 유니터리성 보존
check(np.allclose(embed_unitary(SW, [0, 1], 3).conj().T @ embed_unitary(SW, [0, 1], 3),
                  np.eye(8)), "임베딩 결과 유니터리 보존")
# (c) 비대상 와이어 항등: 1q H를 n=2 와이어[0]에 → H⊗I
H1 = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
check(np.allclose(embed_unitary(H1, [0], 2), np.kron(H1, np.eye(2))), "embed H on [0] == H⊗I (big-endian)")
# (d) 오류경로: 중복/범위초과 targets 거부
for bad in ([0, 0], [0, 3]):
    try:
        embed_unitary(SW, bad, 3); check(False, f"비유효 targets {bad} 거부")
    except ContractViolation:
        check(True, f"비유효 targets {bad} 거부")

print("\n" + "=" * 64)
print("T6 — check_isometry / run_contracts_iso (alloc ancilla 비정방)")
print("=" * 64)
from qualtran.bloqs.mcmt.and_bloq import And  # noqa: E402
Vand = np.asarray(And().tensor_contract())   # (8,4) isometry
# (a) And isometry 통과 (n_in=2, n_alloc=1)
check(Vand.shape == (8, 4), "And tensor_contract 비정방 (8,4)")
V = check_isometry(Vand, 2, 1, "and")
check(np.allclose(V.conj().T @ V, np.eye(4)), "check_isometry: V†V == I₄ 통과")
# (b) golden 해석 isometry 일치
gold = np.zeros((8, 4), dtype=complex)
for c0 in (0, 1):
    for c1 in (0, 1):
        gold[(c0 << 2) | (c1 << 1) | (c0 & c1), (c0 << 1) | c1] = 1.0
r = run_contracts_iso(Vand, 2, 1, golden=gold, name="and")
check(r.all_passed and r.signal["contract"] == "C1-C4(iso)", "run_contracts_iso: And+golden 통과")
# (c) 비isometry 거부 (열을 동일하게 만들어 V†V≠I)
bad = Vand.copy(); bad[:, 1] = bad[:, 0]
rb = run_contracts_iso(bad, 2, 1, name="bad")
check(not rb.all_passed and rb.signal["contract"] == "C3iso", f"비isometry 거부 → {rb.signal['contract']}")
# (d) shape 불일치 거부 (n_alloc 틀림)
rs = run_contracts_iso(Vand, 2, 2, name="badshape")
check(not rs.all_passed and rs.signal["contract"] == "C1", f"isometry shape 불일치 거부 → {rs.signal['contract']}")
# (e) golden 불일치 거부
rg = run_contracts_iso(Vand, 2, 1, golden=np.zeros((8, 4), dtype=complex) + np.eye(8, 4), name="badg")
check(not rg.all_passed and rg.signal["contract"] == "C4", f"isometry golden 불일치 거부 → {rg.signal['contract']}")

print("\n" + "=" * 64)
print("T7 — 신호 taxonomy (reason_code·norm_delta·fix_hint, 리뷰 반영)")
print("=" * 64)
# C4 golden 불일치 → reason_code=golden_mismatch + norm_delta + fix_hint
X1, _ = build_unitary(1, [("X", 0)])
H1g, _ = build_unitary(1, [("H", 0)])
r = run_contracts(X1, 1, 0, golden=H1g, name="t7")
s = r.signal
check(s["reason_code"] == "golden_mismatch" and "엔디안" in s["fix_hint"], "C4 reason_code+fix_hint")
check(isinstance(s.get("norm_delta"), float) and s["norm_delta"] > 0.1, f"C4 norm_delta={s.get('norm_delta'):.3f}")
# 비유니터리 → C2 non_unitary (C1/C2 메시지 정확분류)
r = run_contracts(np.array([[1, 0], [0, 2]], dtype=complex), 1, 0, name="t7")
check(r.signal["contract"] == "C2" and r.signal["reason_code"] == "non_unitary", "비유니터리 → C2 non_unitary")
# 차원 불일치 → C1 dimension_mismatch
r = run_contracts(np.eye(2, dtype=complex), 2, 0, name="t7")
check(r.signal["contract"] == "C1" and r.signal["reason_code"] == "dimension_mismatch", "차원불일치 → C1 dimension_mismatch")
# classify: compose 비유니터리는 C4 (오분류 방지)
check(classify_contract("[m] C4 위반: 합성 결과 비유니터리") == "C4", "compose 비유니터리 → C4(오분류 방지)")
check(classify_contract("[m] C3iso 위반: V†V≠I") == "C3iso", "C3iso 분류")
# golden_delta
check(golden_delta(np.eye(2, dtype=complex), np.eye(2, dtype=complex)) < 1e-12, "golden_delta(동일)=0")

print("\n" + "=" * 64)
print(f"결과: {PASS} PASS / {FAIL} FAIL")
print("=" * 64)
sys.exit(1 if FAIL else 0)
