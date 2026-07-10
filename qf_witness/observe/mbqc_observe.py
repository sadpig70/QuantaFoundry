#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mbqc_observe — HE2 P2.2: MBQC 측정패턴↔회로 등가 관측 (신규 봉인 0).

봉인된 cluster3x3_prep(자원 상태)·mbqc_h(coherent H 텔레포트)로 측정기반 계산 의미론을 실증:
  1. mbqc_h 가 임의 입력 |ψ>₀|+>₁ 를 |+>₀ (H|ψ>)₁ 로 결정론적 텔레포트(H 게이트 == 측정패턴).
  2. cluster3x3 자원 상태가 stabilizer 그래프로 well-formed(9 stabilizer 고정 재확인).

정직 경계(INV-Q3, seal 아님, root 불변):
  - 봉인 = mbqc_h·cluster3x3 (coherent Clifford exact)뿐.
  - 실측정(사영=비유니터리)·byproduct Pauli·gflow 의존구조·비-Clifford(π/4 T-텔레포트) = 관측.
  - 신규 봉인 0.

사용: python scripts/mbqc_observe.py [--quick]
"""
import os, sys, re, json
from functools import reduce
import numpy as np

from qf_witness.core.paths import ROOT
OUT = os.path.join(ROOT, ".pgf", "proofs", "MBQC-OBSERVE.json")
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
Hd = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)


def load_golden(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    ns = {}
    exec(re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1), ns)
    return ns["golden"]


def observe():
    U = load_golden("mbqc_h.app.pg")
    plus = np.array([1, 1], dtype=complex) / np.sqrt(2)
    # 1. H-텔레포트: 여러 입력에서 |ψ>|+> → |+> (H|ψ>)
    tele_ok = True
    for a, b in [(1, 0), (0, 1), (1, 1j), (0.6, 0.8), (0.5, 0.5 + 0.5j)]:
        psi = np.array([a, b], dtype=complex)
        psi /= np.linalg.norm(psi)
        out = U @ np.kron(psi, plus)
        exp = np.kron(plus, Hd @ psi)
        if not np.allclose(out, exp):
            tele_ok = False
    # 2. cluster3x3 자원 stabilizer well-formed
    C = load_golden("cluster3x3_prep.app.pg")
    gs = C[:, 0]                                    # |+>^9 는 |0>에서 시작? golden|0..0>=cluster state? 아님.
    # cluster prep golden|0^9> = H^9|0>후 CZ = cluster state. 그래서 gs=golden@|0^9>=golden[:,0]
    NQ = 9

    def emb(op, q):
        return reduce(np.kron, [op if i == q else I for i in range(NQ)])
    edges = [(0, 1), (1, 2), (3, 4), (4, 5), (6, 7), (7, 8),
             (0, 3), (3, 6), (1, 4), (4, 7), (2, 5), (5, 8)]

    def neigh(i):
        return [j for (a, b) in edges for j in ((b,) if a == i else (a,) if b == i else ())]
    stab_ok = True
    for i in range(9):
        S = emb(X, i)
        for j in neigh(i):
            S = S @ emb(Z, j)
        if not np.allclose(S @ gs, gs):
            stab_ok = False
    ok = tele_ok and stab_ok
    return {"axis": "측정기반 양자계산(MBQC) — 측정패턴↔회로 등가",
            "sealed_assets": "cluster3x3_prep(자원)·mbqc_h(coherent H 텔레포트)",
            "H_teleport_deterministic": tele_ok,
            "cluster_resource_stabilizer_wellformed": stab_ok,
            "honest_boundary": "봉인=coherent Clifford exact 뿐(mbqc_h·cluster). 실측정(비유니터리)·byproduct·"
                               "gflow·비-Clifford(π/4 T-텔레포트)=관측(INV-Q3). 신규 봉인 0.",
            "ok": bool(ok)}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        report = {"_schema": "mbqc-observe-v1",
                  "_note": "MBQC 측정패턴↔회로 등가 관측. 봉인=cluster3x3·mbqc_h 뿐(INV-Q3). 신규 봉인 0.",
                  "observation": res}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("MBQC 측정패턴↔회로 등가 관측:", flush=True)
        print(f"  H 게이트 결정론적 텔레포트(|ψ>|+>→|+>H|ψ>): {res['H_teleport_deterministic']}", flush=True)
        print(f"  cluster3x3 자원 stabilizer well-formed: {res['cluster_resource_stabilizer_wellformed']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"mbqc_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
