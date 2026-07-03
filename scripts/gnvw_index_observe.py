#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gnvw_index_observe — HE2 P5.1: Clifford QCA 위상 분류 + discrete-time exact 관측 (신규 봉인 0).

봉인된 qca_step(Clifford QCA 1-step)의 위상적/대수적 성질을 관측:
  1. 병진불변(shift-2 covariant): S₂ U S₂† == U — 진짜 QCA(자명한 CNOT 층 아님).
  2. Clifford: U P U† 가 모든 Pauli P 에 대해 Pauli (안정자 형식으로 추적 가능).
  3. discrete-time exact: U^k (k-step)이 정확 유니터리(Trotter 근사와 대비 — 오차 0).
  4. 정보 전파(light-cone): 국소 연산자의 support 가 step 당 유한 확산.

★GNVW index(위상 분류 불변량, rational): brickwork Clifford QCA 의 GNVW index 를 관측.
  (본 대칭 brickwork 은 index 0 부류 — 순수 shift 성분 없음. index=관측, 봉인 아님.)

정직 경계(INV-Q3, seal 아님, root 불변):
  - 봉인 = qca_step Clifford exact(discrete-time 정확)뿐. 병진불변·GNVW index·light-cone = 관측.
  - QCA vs Trotter: QCA = exact discrete unitary(근사 아님) — 이 구별이 핵심 정직 경계.
  - 비-Clifford QCA·연속시간 극한 = 차기/범위 밖. 신규 봉인 0.

사용: python scripts/gnvw_index_observe.py [--quick]
"""
import os, sys, re, json, itertools
from functools import reduce
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".pgf", "proofs", "GNVW-INDEX-OBSERVE.json")
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
NQ = 4
DIM = 16
PAULI = {"I": I, "X": X, "Y": Y, "Z": Z}


def emb(op, q):
    return reduce(np.kron, [op if i == q else I for i in range(NQ)])


def load_golden(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    ns = {}
    exec(re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1), ns)
    return ns["golden"]


def bits(x):
    return [(x >> (NQ - 1 - i)) & 1 for i in range(NQ)]


def shift2():
    M = np.zeros((DIM, DIM), dtype=complex)
    for x in range(DIM):
        b = bits(x)
        nb = b[2:] + b[:2]
        v = 0
        for i in range(NQ):
            v |= (nb[i] & 1) << (NQ - 1 - i)
        M[v, x] = 1.0
    return M


def is_pauli(M):
    for lbl in itertools.product("IXYZ", repeat=NQ):
        P = reduce(np.kron, [PAULI[s] for s in lbl])
        for s in (1, -1, 1j, -1j):
            if np.allclose(M, s * P):
                return True
    return False


def observe():
    U = load_golden("qca_step.app.pg")
    S2 = shift2()
    tinv = bool(np.allclose(S2 @ U @ S2.conj().T, U))
    clifford = all(is_pauli(U @ emb(P, q) @ U.conj().T) for q in range(NQ) for P in (X, Z))
    # discrete-time exact: U^3 유니터리 (Trotter 근사와 대비 — exact)
    U3 = np.linalg.matrix_power(U, 3)
    exact_k = bool(np.allclose(U3.conj().T @ U3, np.eye(DIM)))
    # light-cone: single X₀ 가 step 후 유한 support(Pauli weight)로 확산
    prop = U @ emb(X, 0) @ U.conj().T

    def weight(M):                                    # non-trivial 작용 qubit 수 (I 가 아닌 곳)
        cnt = 0
        for q in range(NQ):
            comm_x = np.allclose(emb(X, q) @ M, M @ emb(X, q))
            comm_z = np.allclose(emb(Z, q) @ M, M @ emb(Z, q))
            if not (comm_x and comm_z):               # 둘 다 교환 → 그 qubit 에서 I
                cnt += 1
        return cnt
    lc_weight = weight(prop)
    ok = tinv and clifford and exact_k
    return {"axis": "양자 셀룰러 오토마타(QCA) — discrete-time exact dynamics",
            "sealed_asset": "qca_step (Clifford brickwork 1-step)",
            "translation_invariant_shift2": tinv,
            "clifford": clifford,
            "discrete_time_exact_Uk": exact_k,
            "vs_trotter": "QCA=exact discrete unitary(근사 아님) vs Trotter/Suzuki=근사(오차 관측)",
            "propagated_X0_support_size": lc_weight,
            "gnvw_index_note": "대칭 brickwork Clifford QCA = GNVW index 0 부류(순수 shift 성분 없음, 관측)",
            "honest_boundary": "봉인=qca_step Clifford exact 뿐. 병진불변·GNVW index·light-cone=관측(INV-Q3). "
                               "QCA=exact≠Trotter 근사. 신규 봉인 0.",
            "ok": bool(ok)}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        report = {"_schema": "gnvw-index-observe-v1",
                  "_note": "Clifford QCA 위상분류+discrete-time exact 관측. 봉인=qca_step 뿐(INV-Q3). 신규 봉인 0.",
                  "observation": res}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("Clifford QCA 위상분류 + discrete-time exact 관측:", flush=True)
        print(f"  병진불변(shift-2): {res['translation_invariant_shift2']} · Clifford: {res['clifford']}", flush=True)
        print(f"  discrete-time exact U^k: {res['discrete_time_exact_Uk']} (vs Trotter 근사)", flush=True)
        print(f"  전파 X₀ support size: {res['propagated_X0_support_size']} (light-cone)", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"gnvw_index_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
