#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""z2gauge_observe — HE2 T2.2: Z₂ 격자 게이지 이론 Gauss law + 정직 경계 관측 (신규 봉인 0).

봉인된 z2gauge3(게이지불변 encoder)의 게이지 대칭 성질을 관측:
  1. Gauss law G₀=Z₀X₁·G₁=X₁Z₂ 가 codespace 고정([G₀,G₁]=0·Gₖ²=I·게이지불변공간 dim 2).
  2. 논리 Z_L=Z₀ (물리 관측가능량).
  3. Kogut-Susskind H = electric(X_link) + matter-gauge coupling 이 Gauss law 와 교환([H,Gₖ]=0, 게이지불변).

정직 경계(INV-Q3, seal 아님, root 불변):
  - 봉인 = z2gauge3 encoder Clifford exact 뿐. Gauss law 대수·게이지불변성 = 관측.
  - H·Trotter 시간진화 = 관측(근사). U(1)/SU(2) 큰 게이지군 = 비-dyadic 차기.
  - QEC-isomorphic 우려: 대수는 stabilizer code 와 유사하나 **gauge 정체성**(Gauss law 제약·link 변수)이 구별점.
  - 신규 봉인 0.

사용: python scripts/z2gauge_observe.py [--quick]
"""
import os, sys, re, json
from functools import reduce
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".pgf", "proofs", "Z2GAUGE-OBSERVE.json")
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
NQ = 3
DIM = 8


def emb(op, q):
    return reduce(np.kron, [op if i == q else I for i in range(NQ)])


def load_golden(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    ns = {}
    exec(re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1), ns)
    return ns["golden"]


def observe():
    U = load_golden("z2gauge3.app.pg")
    V = U[:, [0, 4]]                                 # 논리 입력 |ψ,0,0>
    G0 = emb(Z, 0) @ emb(X, 1)
    G1 = emb(X, 1) @ emb(Z, 2)
    commute = bool(np.allclose(G0 @ G1, G1 @ G0))
    sq = bool(np.allclose(G0 @ G0, np.eye(DIM))) and bool(np.allclose(G1 @ G1, np.eye(DIM)))
    fix = bool(np.allclose(G0 @ V, V)) and bool(np.allclose(G1 @ V, V))
    dim2 = bool(np.allclose(V.conj().T @ V, np.eye(2)))
    zl = bool(np.allclose(V.conj().T @ emb(Z, 0) @ V, Z))
    # Kogut-Susskind H = electric X_link + matter coupling (dyadic 예시); [H,Gk]=0 게이지불변
    H_ks = 0.5 * emb(X, 1) + 0.5 * (emb(Z, 0) @ emb(Z, 2))   # electric + matter-matter (gauge-inv 항)
    gauge_inv_H = bool(np.allclose(H_ks @ G0, G0 @ H_ks)) and bool(np.allclose(H_ks @ G1, G1 @ H_ks))
    ok = commute and sq and fix and dim2 and zl and gauge_inv_H
    return {"axis": "Z₂ 격자 게이지 이론 (1+1D Kogut-Susskind)",
            "sealed_asset": "z2gauge3 (게이지불변 부분공간 encoder)",
            "gauss_law_commute": commute, "gauss_law_sq_I": sq,
            "codespace_fixed_dim2": fix and dim2, "logical_Z_L=Z0": zl,
            "hamiltonian_gauge_invariant": gauge_inv_H,
            "qec_distinction": "대수는 stabilizer code 유사하나 gauge 정체성(Gauss law 제약·link 변수)이 구별점",
            "honest_boundary": "봉인=z2gauge3 Clifford exact 뿐. Gauss law 대수·게이지불변=관측. H·Trotter=근사, "
                               "U(1)/SU(2)=비-dyadic 차기. 신규 봉인 0(INV-Q3).",
            "ok": bool(ok)}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        report = {"_schema": "z2gauge-observe-v1",
                  "_note": "Z₂ 격자 게이지 Gauss law + gauge-invariant H 관측. 봉인=z2gauge3 뿐(INV-Q3). 신규 봉인 0.",
                  "observation": res}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("Z₂ 격자 게이지 이론 Gauss law 관측:", flush=True)
        print(f"  [G₀,G₁]=0: {res['gauss_law_commute']} · Gₖ²=I: {res['gauss_law_sq_I']} · codespace dim2 고정: {res['codespace_fixed_dim2']}", flush=True)
        print(f"  논리 Z_L=Z₀: {res['logical_Z_L=Z0']} · Kogut-Susskind H 게이지불변([H,Gₖ]=0): {res['hamiltonian_gauge_invariant']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"z2gauge_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
