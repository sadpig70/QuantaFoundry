#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""h2_molecule_observe — V08 Fermionic 응용: 실제 분자 H₂ (양자화학 hello-world).

미래 QPC 의 대표 킬러앱=양자화학. H₂ 분자(STO-3G, 2-qubit 축약 Hamiltonian, O'Malley et al 2016):
    H = g₀·I + g₁·Z₀ + g₂·Z₁ + g₃·Z₀Z₁ + g₄·X₀X₁ + g₅·Y₀Y₁    (Jordan-Wigner)

★핵심: H₂ 는 **이미 봉인된 fermionic 자산의 조합**이다 —
    hopping 항 X₀X₁+Y₀Y₁ = 2·(be_hop 이 block-encode 하는 A=(XX+YY)/2),
    Z 항(밀도) = be_num 류(number operator (I-Z)/2).
즉 be_hop·be_num(봉인) + VQE ansatz(봉인) + QSVT Hamiltonian sim(봉인)으로 실제 분자를 시뮬한다.

본 스크립트는 H₂ ground energy 와 **결합 해리 곡선**(hopping 세기↓ → 에너지↑)을 고전 관측한다.

정직 경계(INV-Q3, seal 아님, root 불변):
  - Pauli 계수 gᵢ = 고전 양자화학 적분(외부 입력, illustrative). Hamiltonian *구조*(Pauli 항)는 봉인
    block-encoding(be_hop·be_num)으로 정확 표현. ground energy·bond curve·e^{-iHt}=고전/관측.
  - 신규 봉인 0 (be_hop·be_num 재사용) — 실제 분자 응용은 봉인 자산의 조합 관측.

사용: python scripts/h2_molecule_observe.py [--quick]
"""
import os, sys, json
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".pgf", "proofs", "H2-MOLECULE-OBSERVE.json")

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def _kr(a, b):
    return np.kron(a, b)


# H₂ STO-3G 2-qubit reduced coefficients (O'Malley et al 2016, R≈0.75Å) — illustrative chemistry input
G = {"I": -0.4804, "Z0": 0.3435, "Z1": -0.4347, "Z0Z1": 0.5716, "X0X1": 0.0910, "Y0Y1": 0.0910}


def h2_hamiltonian(hop_scale=1.0):
    return (G["I"] * _kr(I, I) + G["Z0"] * _kr(Z, I) + G["Z1"] * _kr(I, Z) + G["Z0Z1"] * _kr(Z, Z)
            + hop_scale * G["X0X1"] * _kr(X, X) + hop_scale * G["Y0Y1"] * _kr(Y, Y))


def observe():
    H = h2_hamiltonian()
    ev = np.sort(np.linalg.eigvalsh(H).real)
    # sealed-asset 분해: hopping == 2·be_hop_A, Z terms == be_num 류
    hop_term = G["X0X1"] * _kr(X, X) + G["Y0Y1"] * _kr(Y, Y)
    be_hop_A = (_kr(X, X) + _kr(Y, Y)) / 2
    hop_matches = bool(np.allclose(hop_term, 2 * G["X0X1"] * be_hop_A))
    # 결합 해리 곡선: hopping 세기↓ → ground energy↑ (결합 약화→해리)
    curve = []
    for s in [1.0, 0.6, 0.3, 0.0]:
        g = float(np.sort(np.linalg.eigvalsh(h2_hamiltonian(s)).real)[0])
        curve.append({"hopping_scale": s, "ground_energy": round(g, 4)})
    dissociation = all(curve[i]["ground_energy"] <= curve[i + 1]["ground_energy"] + 1e-9
                       for i in range(len(curve) - 1))
    ok = hop_matches and dissociation
    return {"molecule": "H₂ (STO-3G, 2-qubit reduced, Jordan-Wigner)",
            "hamiltonian": "H = g₀I + g₁Z₀ + g₂Z₁ + g₃Z₀Z₁ + g₄X₀X₁ + g₅Y₀Y₁",
            "coefficients_illustrative": G,
            "eigenvalues_hartree": [round(float(x), 4) for x in ev],
            "ground_energy_hartree": round(float(ev[0]), 4),
            "sealed_asset_decomposition": {
                "hopping_X0X1_plus_Y0Y1": "= 2·be_hop_A (be_hop 봉인 block-encoding)",
                "Z_terms": "= be_num 류 number operator (be_num 봉인)",
                "hopping_matches_be_hop": hop_matches},
            "bond_dissociation_curve": curve, "dissociation_trend_ground_rises": dissociation,
            "consumer_link": "H₂ = Pauli 합 → be_hop·be_num block-encoding + VQE ansatz(봉인) + QSVT Ham-sim(V08_14)",
            "honest_boundary": "계수 gᵢ=고전 양자화학 적분(illustrative). Hamiltonian 구조=봉인 block-encoding 조합. "
                               "ground energy·bond curve·e^{-iHt}=observation(INV-Q3). 신규 봉인 0(자산 재사용).",
            "ok": bool(ok)}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    all_ok = res["ok"]
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        report = {"_schema": "h2-molecule-observe-v1",
                  "_note": "실제 분자 H₂(양자화학) = 봉인 fermionic 자산(be_hop·be_num)+VQE+QSVT Ham-sim 조합 관측. "
                           "계수=고전 적분(illustrative), 구조=봉인 block-encoding. seal 아님(INV-Q3), 신규 봉인 0.",
                  "observation": res}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("실제 분자 H₂ 양자화학 관측 (봉인 fermionic 자산 조합):", flush=True)
        print(f"  ground energy = {res['ground_energy_hartree']} Hartree (illustrative 계수)", flush=True)
        print(f"  hopping X₀X₁+Y₀Y₁ == 2·be_hop_A (봉인 block-encoding): {res['sealed_asset_decomposition']['hopping_matches_be_hop']}", flush=True)
        for c in res["bond_dissociation_curve"]:
            print(f"  hopping×{c['hopping_scale']}: ground energy = {c['ground_energy']}", flush=True)
        print(f"  결합 해리 경향(hopping↓→energy↑): {res['dissociation_trend_ground_rises']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"h2_molecule_observe: all_ok={all_ok}", flush=True)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
