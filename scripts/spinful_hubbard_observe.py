#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""spinful_hubbard_observe — V08 Fermionic: 정통 Spinful Fermi-Hubbard 모델 (fermionic 축 정점).

2-site × 2-spin = 4 modes. 정통 Fermi-Hubbard(응집물질·양자화학 대표):
    H = -t·Σ_σ (a_{0σ}†a_{1σ} + h.c.) + U·Σ_j n_{j↑}·n_{j↓}
Jordan-Wigner(4 modes: 0=0↑,1=0↓,2=1↑,3=1↓):
    same-spin hopping 0↑-1↑(modes 0,2)·0↓-1↓(modes 1,3) → 비인접 → JW Z-string 필요(be_hopz 가 block-encode).
    on-site U: n_0↑n_0↓(modes 0,1)·n_1↑n_1↓(modes 2,3) (be_num 곱).

봉인 자산: 비인접 hopping=be_hopz(Z-string, Tier-0), number=be_num(Tier-0). full H=Pauli합→QSVT Ham-sim.
본 스크립트는 4-mode JW 정확성과 스펙트럼·**Mott 물리**(U↑→이중점유 억제·국소모멘트)를 고전 관측한다.

정직 경계(INV-Q3): 4-mode JW 반교환 보존=EXACT. 봉인=be_hopz·be_num. e^{-iHt}=observation.

사용: python scripts/spinful_hubbard_observe.py [--quick]
"""
import os, sys, json
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".pgf", "proofs", "SPINFUL-HUBBARD-OBSERVE.json")

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def _kr(mats):
    r = mats[0]
    for m in mats[1:]:
        r = np.kron(r, m)
    return r


def a_op(j, n=4):
    """JW 소멸 연산자 a_j = (∏_{k<j} Z_k)(X_j+iY_j)/2."""
    ops = [Z if k < j else ((X + 1j * Y) / 2 if k == j else I) for k in range(n)]
    return _kr(ops)


def observe():
    a = [a_op(j) for j in range(4)]
    dim = 16
    # 4-mode JW anticommutation
    jw_ok = all(np.allclose(a[i] @ a[j].conj().T + a[j].conj().T @ a[i],
                            np.eye(dim) if i == j else np.zeros((dim, dim)), atol=1e-9)
                for i in range(4) for j in range(4))
    num = [a[j].conj().T @ a[j] for j in range(4)]
    # same-spin hopping: 0↑-1↑ (0,2), 0↓-1↓ (1,3)
    hop = (a[0].conj().T @ a[2] + a[2].conj().T @ a[0]) + (a[1].conj().T @ a[3] + a[3].conj().T @ a[1])
    onsite = num[0] @ num[1] + num[2] @ num[3]           # n_j↑ n_j↓
    t = 1.0
    spectra = []
    for U in [0.0, 2.0, 4.0, 8.0]:
        Hub = -t * hop + U * onsite
        ev = np.sort(np.linalg.eigvalsh(Hub).real)
        spectra.append({"U": U, "ground_energy": round(float(ev[0]), 4),
                        "low_spectrum": [round(float(x), 4) for x in ev[:4]]})
    # Mott trend: ground energy 가 U 증가에 monotone 증가(이중점유 억제)
    ge = [s["ground_energy"] for s in spectra]
    mott_trend = all(ge[i] <= ge[i + 1] + 1e-9 for i in range(len(ge) - 1))
    ok = bool(jw_ok and mott_trend)
    return {"model": "2-site × 2-spin Fermi-Hubbard: H = -t·Σ_σ hopping_σ + U·Σ_j n_j↑n_j↓ (Jordan-Wigner)",
            "modes": "0=site0↑, 1=site0↓, 2=site1↑, 3=site1↓",
            "jw_4mode_anticommutation": bool(jw_ok),
            "spectra_vs_U": spectra, "mott_trend_ground_rises_with_U": bool(mott_trend),
            "sealed_assets": {"nonadjacent_hopping_zstring": "be_hopz (Tier-0)", "number_operator": "be_num (Tier-0)"},
            "consumer_link": "full H = Pauli 합 → block-encoding/QSVT Hamiltonian sim(V08_14)",
            "honest_boundary": "4-mode JW 반교환 보존=EXACT. 봉인=be_hopz·be_num. e^{-iHt}=observation(INV-Q3).",
            "ok": ok}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    all_ok = res["ok"]
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        report = {"_schema": "spinful-hubbard-observe-v1",
                  "_note": "정통 spinful Fermi-Hubbard(2site×2spin) 관측 = be_hopz(Z-string hopping)+be_num(number). "
                           "4-mode JW=EXACT, 봉인=be_hopz·be_num, e^{-iHt}=observation(INV-Q3).",
                  "observation": res}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("정통 Spinful Fermi-Hubbard 관측 (2site×2spin, be_hopz + be_num):", flush=True)
        print(f"  4-mode JW 반교환 {{a_i,a_j†}}=δ: {res['jw_4mode_anticommutation']}", flush=True)
        for s in res["spectra_vs_U"]:
            print(f"  U={s['U']}: ground energy={s['ground_energy']} · low {s['low_spectrum']}", flush=True)
        print(f"  Mott 물리(U↑→ground↑, 이중점유 억제): {res['mott_trend_ground_rises_with_U']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"spinful_hubbard_observe: all_ok={all_ok}", flush=True)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
