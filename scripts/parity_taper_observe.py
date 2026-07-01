#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""parity_taper_observe — HE H1.4: parity 인코딩의 입자수 대칭 tapering 관측.

봉인된 parity4_transform(U_par, H1.4)로 JW 연산자를 켤레변환하면 parity 표현이 나온다.
parity basis 마지막 qubit q_{n-1} 은 **총 occupation parity**(= 입자수 보존량)를 담는다.

★관측 payoff: number·hopping 연산자가 q_{n-1} 에 대해 {I} 또는 {I,Z}(대각)로만 작용하고
  총-parity Z_{n-1} 과 교환(보존)한다 → sector 고정 시 q_{n-1} 을 **taper**(제거)해 qubit 절감.

정직 경계(INV-Q3, seal 아님, root 불변):
  - 켤레변환 O_par = U_par·O_JW·U_par† = exact(parity4_transform 봉인 귀결).
  - taperability(마지막 qubit 자명/대각 + Z_{n-1} 교환) = 관측. sector 물리 선택은 별도 contract.
  - qubit 절감 이점 = 관측. 신규 봉인 0.

사용: python scripts/parity_taper_observe.py [--quick]
"""
import os, sys, json, itertools
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".pgf", "proofs", "PARITY-TAPER-OBSERVE.json")
n = 4
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
Pm = np.array([[0, 1], [0, 0]], dtype=complex)
PAULI = {"I": I, "X": X, "Y": Y, "Z": Z}


def kr(*m):
    r = m[0]
    for x in m[1:]:
        r = np.kron(r, x)
    return r


def a(p):
    return kr(*([Z] * p + [Pm] + [I] * (n - 1 - p)))


def u_par():
    beta = [[1, 0, 0, 0], [1, 1, 0, 0], [1, 1, 1, 0], [1, 1, 1, 1]]
    dim = 1 << n
    U = np.zeros((dim, dim), dtype=complex)
    for f in range(dim):
        fb = [(f >> (n - 1 - i)) & 1 for i in range(n)]
        bb = [sum(beta[i][j] * fb[j] for j in range(n)) % 2 for i in range(n)]
        out = 0
        for i in range(n):
            out |= (bb[i] & 1) << (n - 1 - i)
        U[out, f] = 1.0
    return U


def decomp(M):
    dim = 1 << n
    out = []
    for lbl in itertools.product("IXYZ", repeat=n):
        c = np.trace(kr(*[PAULI[s] for s in lbl]).conj().T @ M) / dim
        if abs(c) > 1e-9:
            out.append("".join(lbl))
    return out


def observe():
    U = u_par()
    Zlast = kr(*([I] * (n - 1) + [Z]))                 # total-parity operator = Z on q_{n-1}
    ops = {}
    ops["n_1"] = U @ (a(1).conj().T @ a(1)) @ U.conj().T
    ops["n_2"] = U @ (a(2).conj().T @ a(2)) @ U.conj().T
    ops["H_12"] = U @ (a(1).conj().T @ a(2) + a(2).conj().T @ a(1)) @ U.conj().T
    ops["H_03"] = U @ (a(0).conj().T @ a(3) + a(3).conj().T @ a(0)) @ U.conj().T
    rows, all_taper = [], True
    for name, M in ops.items():
        last = sorted(set(l[-1] for l in decomp(M)))    # paulis on q_{n-1}
        commutes = bool(np.allclose(M @ Zlast, Zlast @ M))
        taperable = commutes and set(last) <= {"I", "Z"}  # 자명/대각 → sector 치환으로 제거
        all_taper = all_taper and taperable
        rows.append({"op": name, "last_qubit_paulis": last,
                     "commutes_total_parity": commutes, "taperable": taperable})
    ok = all_taper
    return {"encoding": "parity (n=4, U_par=parity4_transform 봉인)",
            "conjugation": "O_par = U_par · O_JW · U_par†  (exact)",
            "total_parity_operator": "Z_{n-1} (q3) = (-1)^{입자수}",
            "tapering_table": rows,
            "all_taperable": ok,
            "honest_boundary": "켤레변환=exact(parity4_transform 봉인 귀결). taperability=관측; "
                               "sector 물리 선택=별도 contract; qubit 절감=관측. 신규 봉인 0.",
            "ok": bool(ok)}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        report = {"_schema": "parity-taper-observe-v1",
                  "_note": "parity 인코딩 입자수-대칭 tapering 관측. seal 아님(INV-Q3), 신규 봉인 0.",
                  "observation": res}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("parity 인코딩 입자수-대칭 tapering 관측:", flush=True)
        for r in res["tapering_table"]:
            print(f"  {r['op']:5}: q3 paulis={r['last_qubit_paulis']} "
                  f"보존={r['commutes_total_parity']} taperable={r['taperable']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"parity_taper_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
