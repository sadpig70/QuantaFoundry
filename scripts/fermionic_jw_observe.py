#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fermionic_jw_observe — V08 Fermionic Simulation: Jordan-Wigner correctness (새 수평축).

fermionic 연산자 a_j (소멸)·a_j† (생성)를 Jordan-Wigner 로 Pauli 로 매핑:
    a_j = (∏_{k<j} Z_k) · (X_j + i Y_j)/2
이 매핑이 **fermionic 반교환관계**를 정확히 보존함을 독립 검증한다(EXACT proof, 근사 아님):
    {a_i, a_j†} = δ_ij · I ,  {a_i, a_j} = 0.
2-site hopping a_0†a_1 + a_1†a_0 --JW--> (X⊗X + Y⊗Y)/2 = be_hop 이 block-encode 하는 H.
→ fermionic Hamiltonian 을 Pauli LCU 로 봉인(be_hop, Tier-0) → QSVT/Trotter Ham-sim(V08_14) 적용.

teeth(공허하지 않음): Z-string 을 뺀 *잘못된* 매핑은 반교환관계를 위반해야 한다(JW 의 Z-string 필연성).

정직 경계: JW 반교환 보존은 EXACT(수학 항등식). 봉인 = be_hop(fermionic hopping block-encoding).
  시간발전 e^{-iHt} 근사는 observation(INV-Q3, qsvt_hamsim_observe 와 동일 경계).

사용: python scripts/fermionic_jw_observe.py [--quick]
"""
import os, sys, json
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".pgf", "proofs", "FERMIONIC-JW-OBSERVE.json")
SPECS_APPS = os.path.join(ROOT, "specs", "apps")

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def _kr(mats):
    r = mats[0]
    for m in mats[1:]:
        r = np.kron(r, m)
    return r


def jw_annihilation(j, n_modes, z_string=True):
    """a_j = (∏_{k<j} Z_k)(X_j+iY_j)/2. z_string=False → 잘못된 매핑(teeth)."""
    ops = []
    for k in range(n_modes):
        if k < j:
            ops.append(Z if z_string else I)
        elif k == j:
            ops.append((X + 1j * Y) / 2)
        else:
            ops.append(I)
    return _kr(ops)


def _acomm(A, B):
    return A @ B + B @ A


def verify(n_modes=2):
    dim = 1 << n_modes
    a = [jw_annihilation(j, n_modes) for j in range(n_modes)]
    checks = {}
    # {a_i, a_j†} = δ_ij I
    ok_dagger = True
    for i in range(n_modes):
        for j in range(n_modes):
            expect = np.eye(dim) if i == j else np.zeros((dim, dim))
            if not np.allclose(_acomm(a[i], a[j].conj().T), expect, atol=1e-9):
                ok_dagger = False
    checks["anticomm_a_adag"] = bool(ok_dagger)
    # {a_i, a_j} = 0
    ok_aa = all(np.allclose(_acomm(a[i], a[j]), 0, atol=1e-9)
                for i in range(n_modes) for j in range(n_modes))
    checks["anticomm_a_a"] = bool(ok_aa)
    # hopping a_0†a_1 + a_1†a_0 == (XX+YY)/2 (be_hop 이 block-encode)
    Hhop = a[0].conj().T @ a[1] + a[1].conj().T @ a[0]
    Hpauli = (_kr([X, X]) + _kr([Y, Y])) / 2
    checks["hopping_maps_to_pauli"] = bool(np.allclose(Hhop, Hpauli))
    # teeth: Z-string 뺀 잘못된 매핑은 {a_0, a_1†}=0 을 위반해야
    a1_wrong = jw_annihilation(1, n_modes, z_string=False)
    teeth = bool(not np.allclose(_acomm(a[0], a1_wrong.conj().T), 0, atol=1e-9))
    checks["zstring_teeth"] = teeth
    # be_hop block == H (봉인된 block-encoding 과 대조)
    be_block_ok = None
    spec = os.path.join(SPECS_APPS, "be_hop.app.pg")
    if os.path.exists(spec):
        import re
        code = re.search(r"```python id=app_golden\s*\n(.*?)\n```",
                         open(spec, encoding="utf-8").read(), re.S).group(1)
        ns = {}
        exec(code, ns)
        be_block_ok = bool(np.allclose(ns["golden"][:dim, :dim], Hpauli))
    checks["be_hop_block_equals_H"] = be_block_ok
    eig = sorted(set(np.round(np.linalg.eigvalsh(Hpauli), 6)))
    ok = ok_dagger and ok_aa and checks["hopping_maps_to_pauli"] and teeth and (be_block_ok in (True, None))
    return {"n_modes": n_modes, "checks": checks,
            "H_hop_eigenvalues": [round(float(x), 4) for x in eig],
            "sealed_block_encoding": "be_hop (Tier-0, fermionic hopping (XX+YY)/2)",
            "consumer_link": "be_hop → QSVT/Trotter Hamiltonian sim(V08_14, e^{-iHt} 근사=observation)",
            "honest_boundary": "JW 반교환 보존=EXACT(수학 항등식). 봉인=be_hop. e^{-iHt} 시간발전=observation(INV-Q3).",
            "ok": bool(ok)}


def main():
    quick = "--quick" in sys.argv
    res = verify(n_modes=2)
    all_ok = res["ok"]
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        report = {"_schema": "fermionic-jw-observe-v1",
                  "_note": "Jordan-Wigner 반교환관계 보존 독립검증(EXACT) + Z-string teeth + be_hop 대조. "
                           "봉인=be_hop(fermionic hopping block-encoding). 시간발전=observation(INV-Q3).",
                  "observation": res}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        c = res["checks"]
        print("Fermionic Jordan-Wigner correctness (2-site):", flush=True)
        print(f"  {{a_i,a_j†}}=δ_ij: {c['anticomm_a_adag']} · {{a_i,a_j}}=0: {c['anticomm_a_a']}", flush=True)
        print(f"  hopping → (XX+YY)/2: {c['hopping_maps_to_pauli']} · be_hop block==H: {c['be_hop_block_equals_H']}", flush=True)
        print(f"  Z-string teeth(잘못된 매핑 위반): {c['zstring_teeth']} · H_hop eig={res['H_hop_eigenvalues']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"fermionic_jw_observe: all_ok={all_ok}", flush=True)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
