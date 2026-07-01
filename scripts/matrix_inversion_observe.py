#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""matrix_inversion_observe — V08 QSVT Consumer: linear systems (matrix inversion) 관측.

QSVT consumer trilogy 의 3번째(물리=Ham-sim, 검색=amp-amp, **선형대수=matrix inversion**).
QSVT 는 block-encoded Hermitian A 에 홀수 다항식 P(A)≈c·A⁻¹ 을 적용해 선형계 A x=b 를 푼다(HHL 계열).

well-conditioned A=(3I+X⊗X+Z⊗Z)/4 (고유값 {0.25,0.75,1.25}, 0 에서 떨어짐)에 대해, odd polynomial
degree 1,3,5 로 c·A⁻¹ 을 근사할 때의 오차를 **고전 관측**한다. 고유값 3개 → degree-5 홀수(x,x³,x⁵ 3항)에서
exact(보간). QSVT 가 그 홀수 다항식을 실현(qsp_d1/d3/**d5** 봉인 = degree 1/3/5 기본블록).

정직 경계(INV-Q3, seal 아님):
  - 봉인 = 정확한 QSP 홀수 다항식 유니터리(qsp_d1/d3/d5, Tier-0). 1/x 근사 프로파일 = 고전 관측.
  - matrix inversion 은 0 고유값에서 발산 → well-conditioned A 로 한정(honest). c=min λ 로 |P(λ)|≤1 정규화.

사용: python scripts/matrix_inversion_observe.py [--quick]
"""
import os, sys, json
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".pgf", "proofs", "MATRIX-INVERSION-OBSERVE.json")

X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def observe():
    A = (3 * np.eye(4) + np.kron(X, X) + np.kron(Z, Z)) / 4     # well-conditioned Hermitian
    ev = sorted(set(np.round(np.linalg.eigvalsh(A).real, 6)))
    lam = np.array(ev)
    kappa = float(max(lam) / min(lam))                          # condition number
    c = float(min(lam))                                         # scale: |c/λ|<=1
    target = c / lam
    Ainv_scaled = c * np.linalg.inv(A)
    rows = []
    for d in [1, 3, 5]:
        powers = list(range(1, d + 1, 2))                      # odd powers x, x³, x⁵...
        M = np.array([[l ** p for p in powers] for l in lam])
        coef, *_ = np.linalg.lstsq(M, target, rcond=None)
        P = sum(coef[i] * np.linalg.matrix_power(A, powers[i]) for i in range(len(powers)))
        err = float(np.linalg.norm(P - Ainv_scaled))
        rows.append({"odd_degree": d, "frobenius_error": round(err, 6)})
    return {"A": "(3I+X⊗X+Z⊗Z)/4 (well-conditioned Hermitian)",
            "eigenvalues": [round(float(x), 4) for x in ev], "condition_number": round(kappa, 4),
            "target": "c·A⁻¹ (c=min λ, |P(λ)|<=1 정규화)",
            "odd_poly_error_by_degree": rows,
            "exact_at_odd_degree": next((r["odd_degree"] for r in rows if r["frobenius_error"] < 1e-9), None),
            "qsp_realizes": {"degree_1": "qsp_d1", "degree_3": "qsp_d3", "degree_5": "qsp_d5 (모두 봉인 Tier-0)"},
            "consumer_trilogy": "물리(Ham-sim, V08_14) · 검색(amp-amp, V08_15) · 선형대수(matrix inversion, 본 노드)",
            "honest_boundary": "봉인=정확 QSP 홀수 다항식(qsp_d1/d3/d5). 1/x 근사=고전관측(INV-Q3, seal 아님). "
                               "0 고유값 발산→well-conditioned A 한정(honest)."}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    all_ok = res["exact_at_odd_degree"] is not None
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        report = {"_schema": "matrix-inversion-observe-v1",
                  "_note": "QSVT matrix inversion(linear systems): 홀수 다항식 P(A)≈c·A⁻¹ 고전관측. seal 아님(INV-Q3). "
                           "봉인=정확 QSP 홀수 블록(qsp_d1/d3/d5). QSVT consumer trilogy 3번째(선형대수).",
                  "observation": res}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("QSVT matrix inversion 관측 (P(A)≈c·A⁻¹, well-conditioned A):", flush=True)
        print(f"  A eigenvalues={res['eigenvalues']} · condition number κ={res['condition_number']}", flush=True)
        for r in res["odd_poly_error_by_degree"]:
            print(f"  odd degree {r['odd_degree']}: ‖P(A) - c·A⁻¹‖_F = {r['frobenius_error']}", flush=True)
        print(f"  → exact at odd degree {res['exact_at_odd_degree']} (QSP: qsp_d1/d3/d5 봉인)", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"matrix_inversion_observe: all_ok={all_ok}", flush=True)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
