#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hubbard_observe — V08 Fermionic: 완전한 t-V Fermi-Hubbard 모델 관측 (be_hop + be_num).

be_hop(hopping) 은 Fermi-Hubbard 의 절반. 여기에 밀도-밀도 상호작용(interaction)을 더해 **완전한
t-V 모델**을 구성한다: H = -t·(a_0†a_1+a_1†a_0) + V·n_0·n_1  --Jordan-Wigner-->
    H = -t·(X⊗X + Y⊗Y)/2 + V·(I-Z_0)(I-Z_1)/4,  n_j=(I-Z_j)/2=|1><1| (be_num 이 block-encode).

봉인 자산: hopping=be_hop(Tier-0), number operator=be_num(Tier-0). full H = Pauli 합 → block-encoding/
QSVT Hamiltonian sim(V08_14) 적용 가능. 본 스크립트는 JW 상호작용 정확성과 스펙트럼을 고전 관측한다.

정직 경계(INV-Q3): number operator JW 성질(commuting projector, n²=n)·interaction=|11><11|=EXACT.
  봉인=be_hop·be_num. 완전 H 의 e^{-iHt} 시간발전=observation. teeth: 잘못된 n=(I+Z)/2 → interaction 오류.

사용: python scripts/hubbard_observe.py [--quick]
"""
import os, sys, json
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".pgf", "proofs", "HUBBARD-OBSERVE.json")

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def _kr(a, b):
    return np.kron(a, b)


def observe():
    n = (I - Z) / 2                       # JW number operator n_j=(I-Z)/2=|1><1|
    N0, N1 = _kr(n, I), _kr(I, n)
    checks = {}
    checks["number_commuting"] = bool(np.allclose(N0 @ N1, N1 @ N0))
    checks["number_projector"] = bool(np.allclose(N0 @ N0, N0) and np.allclose(N1 @ N1, N1))
    interaction = N0 @ N1                  # n_0·n_1 = |11><11|
    checks["interaction_is_double_occupancy"] = bool(np.allclose(interaction, np.diag([0, 0, 0, 1])))
    hopping = (_kr(X, X) + _kr(Y, Y)) / 2  # be_hop block-encodes this
    # teeth: 잘못된 number op (I+Z)/2 → interaction 이 |00><00| 이 되어 double-occupancy 아님
    n_wrong = (I + Z) / 2
    int_wrong = _kr(n_wrong, I) @ _kr(I, n_wrong)
    checks["teeth_wrong_number_op"] = bool(not np.allclose(int_wrong, np.diag([0, 0, 0, 1])))
    # 스펙트럼: t-V 모델 (t,V) sweep
    spectra = []
    for t, V in [(1.0, 0.0), (1.0, 2.0), (1.0, 4.0)]:
        Hub = -t * hopping + V * interaction
        spectra.append({"t": t, "V": V,
                        "eigenvalues": [round(float(x), 4) for x in np.linalg.eigvalsh(Hub)]})
    ok = all([checks["number_commuting"], checks["number_projector"],
              checks["interaction_is_double_occupancy"], checks["teeth_wrong_number_op"]])
    return {"model": "2-site t-V Fermi-Hubbard: H = -t(a0†a1+a1†a0) + V·n0·n1 (Jordan-Wigner)",
            "jw_mapping": "hopping→(XX+YY)/2 [be_hop], n_j=(I-Z_j)/2=|1><1| [be_num], interaction=|11><11|",
            "checks": checks, "spectra": spectra,
            "sealed_assets": {"hopping": "be_hop (Tier-0)", "number_operator": "be_num (Tier-0)"},
            "consumer_link": "full H = Pauli 합 → block-encoding/QSVT Hamiltonian sim(V08_14)",
            "honest_boundary": "JW 성질(commuting projector·interaction=|11><11|)=EXACT. 봉인=be_hop·be_num. "
                               "e^{-iHt} 시간발전=observation(INV-Q3).",
            "ok": bool(ok)}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    all_ok = res["ok"]
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        report = {"_schema": "hubbard-observe-v1",
                  "_note": "완전한 t-V Fermi-Hubbard 모델 = be_hop(hopping) + be_num(number op) 결합 관측. "
                           "JW 성질=EXACT, 봉인=be_hop·be_num, 시간발전=observation(INV-Q3).",
                  "observation": res}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        c = res["checks"]
        print("완전한 t-V Fermi-Hubbard 모델 관측 (be_hop + be_num):", flush=True)
        print(f"  number op: commuting {c['number_commuting']} · projector n²=n {c['number_projector']}", flush=True)
        print(f"  interaction n0·n1=|11><11|(double-occupancy): {c['interaction_is_double_occupancy']} · "
              f"teeth(잘못된 n) {c['teeth_wrong_number_op']}", flush=True)
        for s in res["spectra"]:
            print(f"  t={s['t']} V={s['V']}: eigenvalues {s['eigenvalues']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"hubbard_observe: all_ok={all_ok}", flush=True)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
