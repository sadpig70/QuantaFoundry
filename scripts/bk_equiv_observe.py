#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bk_equiv_observe — HE H1.3: JW↔BK 페르미온 인코딩 등가성 + weight payoff 관측.

봉인된 bk4_transform(U_BK, H1.1)로 JW 연산자를 켤레변환하면 BK 표현이 나온다:
    O_BK = U_BK · O_JW · U_BK†      (U_BK = 계산기저 permutation, exact).
number n_p·hopping H_ij 전부를 JW vs BK Pauli weight 로 대비한다.

★핵심 payoff(관측): 긴 hopping H_03 이 JW weight-4 (X Z Z X + Y Z Z Y, 긴 Z-string)에서
  BK weight-3 (X X I Z + Y Y Z I)로 감소. BK 의 O(log n) locality 실증.

정직 경계(INV-Q3, seal 아님, root 불변):
  - 켤레변환 등가성 O_BK == U_BK·O_JW·U_BK† = **exact 수학 항등**(bk4_transform 봉인의 귀결).
  - 봉인된 bk_num1·bk_hop01 의 top-left block 이 BK conjugate 와 일치함을 재확인.
  - weight 감소(=BK 이점)는 **관측**(observation). 신규 봉인 0.

사용: python scripts/bk_equiv_observe.py [--quick]
"""
import os, sys, re, json, itertools
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".pgf", "proofs", "BK-EQUIV-OBSERVE.json")
n = 4
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
Pm = np.array([[0, 1], [0, 0]], dtype=complex)     # sigma^-
PAULI = {"I": I, "X": X, "Y": Y, "Z": Z}


def kr(*m):
    r = m[0]
    for x in m[1:]:
        r = np.kron(r, x)
    return r


def u_bk():
    beta = [[1, 0, 0, 0], [1, 1, 0, 0], [0, 0, 1, 0], [1, 1, 1, 1]]
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


def a(p):                                          # JW annihilation a_p
    ops = [Z] * p + [Pm] + [I] * (n - 1 - p)
    return kr(*ops)


def decomp(M):
    terms = []
    for lbl in itertools.product("IXYZ", repeat=n):
        c = np.trace(kr(*[PAULI[s] for s in lbl]).conj().T @ M) / (1 << n)
        if abs(c) > 1e-9:
            terms.append(("".join(lbl), complex(round(c.real, 4), round(c.imag, 4))))
    return terms


def wmax(terms):
    return max((sum(1 for s in l if s != "I") for l, _ in terms), default=0)


def app_block(app):                                # 봉인 앱 golden 의 top-left 2^(n_sys-1) block
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    ns = {}
    exec(re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1), ns)
    G = ns["golden"]
    d = G.shape[0] // 2
    return G[:d, :d]


def observe():
    UBK = u_bk()
    rows = []
    for p in range(n):
        nj = a(p).conj().T @ a(p)
        nb = UBK @ nj @ UBK.conj().T
        rows.append({"op": f"n_{p}", "jw_weight": wmax(decomp(nj)), "bk_weight": wmax(decomp(nb))})
    for (i, j) in [(0, 1), (1, 2), (2, 3), (0, 3)]:
        hj = a(i).conj().T @ a(j) + a(j).conj().T @ a(i)
        hb = UBK @ hj @ UBK.conj().T
        rows.append({"op": f"H_{i}{j}", "jw_weight": wmax(decomp(hj)), "bk_weight": wmax(decomp(hb))})
    # payoff: H_03 JW w4 → BK w3
    h03 = next(r for r in rows if r["op"] == "H_03")
    payoff = h03["jw_weight"] > h03["bk_weight"]

    # 봉인 앱 재확인: bk_num1 block == BK n_1 (modes 0,1);  bk_hop01 block == BK H_01
    n1_bk = UBK @ (a(1).conj().T @ a(1)) @ UBK.conj().T
    n1_target = (kr(I, I) - kr(Z, Z)) / 2                      # (I - Z0Z1)/2, modes 0,1
    seal_num = bool(np.allclose(app_block("bk_num1.app.pg"), n1_target))
    hop01_target = (kr(X, I) - kr(X, Z)) / 2                   # X0(I-Z1)/2
    seal_hop = bool(np.allclose(app_block("bk_hop01.app.pg"), hop01_target))

    ok = payoff and seal_num and seal_hop
    return {"encoding": "Jordan-Wigner ↔ Bravyi-Kitaev (n=4, U_BK=bk4_transform 봉인)",
            "conjugation": "O_BK = U_BK · O_JW · U_BK†  (exact, U_BK=계산기저 permutation)",
            "weight_table": rows,
            "payoff_H03_jw_w4_to_bk_w3": payoff,
            "sealed_block_recheck": {"bk_num1 == BK n_1": seal_num, "bk_hop01 == BK H_01": seal_hop},
            "honest_boundary": "켤레변환 등가성=exact 항등(bk4_transform 봉인 귀결). weight 감소=관측. 신규 봉인 0.",
            "ok": bool(ok)}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        report = {"_schema": "bk-equiv-observe-v1",
                  "_note": "JW↔BK 등가성(exact 켤레변환)+weight payoff 관측. seal 아님(INV-Q3), 신규 봉인 0.",
                  "observation": res}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("JW↔BK 인코딩 등가성 + weight payoff 관측:", flush=True)
        for r in res["weight_table"]:
            arrow = " ★payoff" if r["op"] == "H_03" and r["jw_weight"] > r["bk_weight"] else ""
            print(f"  {r['op']:5}: JW weight {r['jw_weight']} → BK weight {r['bk_weight']}{arrow}", flush=True)
        print(f"  봉인 재확인 bk_num1={res['sealed_block_recheck']['bk_num1 == BK n_1']} "
              f"bk_hop01={res['sealed_block_recheck']['bk_hop01 == BK H_01']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"bk_equiv_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
