#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""qsvt_hamsim_observe — V08 QSVT Consumer: Hamiltonian simulation 관측 (맛보기, observation).

QSVT 는 block-encoded Hermitian A 의 **Chebyshev 다항식 T_k(A) 를 정확히 실현**한다(봉인 예:
qsvt_pauli2_d2=짝수 Chebyshev, qsvt_pauli2_d3=홀수 Chebyshev). Hamiltonian simulation e^{-iAt}
는 그 Chebyshev 급수(Jacobi-Anger)다: e^{-ixt}=J₀(t)T₀(x)+2Σ_{k≥1}(-i)^k J_k(t)T_k(x).

본 스크립트는 A=(X⊗X+Z⊗Z)/2(be_pauli2 가 block-encode)에 대해, QSVT 가 제공하는 Chebyshev 기저로
e^{-iAt} 를 근사할 때의 **오차(차수↑→오차↓)를 고전 관측**한다 — seal 아님(INV-Q3, Trotter 근사경계의 자매).

정직 경계:
  - 봉인된 것 = 정확한 Chebyshev-of-A 블록(qsvt_pauli2_d2/d3, Tier-0). e^{-iAt} 자체는 봉인 아님.
  - e^{-iAt} = Chebyshev 급수(고전 사실). QSVT 블록을 LCU 로 합치면 e^{-iAt} 근사(양자회로는 future work).
  - A 는 commuting Paulis(비축퇴 위해) → 이 A 는 Trotter 도 exact(e^{-iXXt/2}e^{-iZZt/2}); QSVT 의
    이점은 일반(비가환) A 의 점근 스케일링(알려진 이론)이며, 여기선 Chebyshev 수렴을 관측한다.

사용: python scripts/qsvt_hamsim_observe.py [--quick]
"""
import os, sys, json
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".pgf", "proofs", "QSVT-HAMSIM-OBSERVE.json")

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def _kr(*m):
    r = m[0]
    for x in m[1:]:
        r = np.kron(r, x)
    return r


def cheb_T(A, kmax):
    """Chebyshev 다항식 T_0..T_kmax of matrix A (T0=I, T1=A, T_{k+1}=2A T_k - T_{k-1})."""
    n = A.shape[0]
    Ts = [np.eye(n, dtype=complex), A.copy()]
    for _ in range(2, kmax + 1):
        Ts.append(2 * A @ Ts[-1] - Ts[-2])
    return Ts


def observe(t=1.0, dmax=4):
    A = (_kr(X, X) + _kr(Z, Z)) / 2                  # be_pauli2 가 block-encode 하는 A
    w, V = np.linalg.eigh(A)                          # Hermitian eigen-decomp
    exact = V @ np.diag(np.exp(-1j * w * t)) @ V.conj().T   # e^{-iAt} (정확)
    eig_distinct = sorted(set(np.round(w, 6)))
    Ts = cheb_T(A, dmax)
    # 각 차수 d: 고유값에서 e^{-iλt} 를 Chebyshev T_0..T_d 로 최소제곱 적합 → P_d(A) 재구성 → 오차
    lam = np.array(eig_distinct)
    target = np.exp(-1j * lam * t)
    rows = []
    for d in range(0, dmax + 1):
        M = np.array([[np.cos(k * np.arccos(np.clip(l, -1, 1))) for k in range(d + 1)] for l in lam])
        c, *_ = np.linalg.lstsq(M, target, rcond=None)   # Chebyshev 계수(고유값 적합)
        Pd = sum(c[k] * Ts[k] for k in range(d + 1))
        err = float(np.linalg.norm(Pd - exact))
        rows.append({"degree": d, "frobenius_error": round(err, 6)})
    return {"A": "(X⊗X+Z⊗Z)/2 (be_pauli2 block-encoded)", "t": t,
            "eigenvalues": [round(float(x), 4) for x in eig_distinct],
            "target": "e^{-iAt} (Hamiltonian simulation)",
            "chebyshev_error_by_degree": rows,
            "exact_at_degree": next((r["degree"] for r in rows if r["frobenius_error"] < 1e-9), None),
            "qsvt_realizes": {"even_chebyshev": "qsvt_pauli2_d2 (T_0,T_2 성분)",
                              "odd_chebyshev": "qsvt_pauli2_d3 (T_1,T_3 성분)"},
            "honest_boundary": "봉인=정확 Chebyshev-of-A 블록(Tier-0). e^{-iAt}=Chebyshev 급수(고전관측, "
                               "seal 아님, INV-Q3). QSVT 블록 LCU 합성=future work. 이 A 는 commuting→Trotter도 exact."}


def main():
    quick = "--quick" in sys.argv
    res = observe(t=1.0, dmax=4)
    all_ok = res["exact_at_degree"] is not None      # 유한 고유값이면 유한 차수에서 exact 도달
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        report = {"_schema": "qsvt-hamsim-observe-v1",
                  "_note": "QSVT=Chebyshev-of-A 실현 → e^{-iAt} Hamiltonian sim 의 Chebyshev 급수 근사 고전관측. "
                           "seal 아님(INV-Q3). 봉인은 정확 Chebyshev 블록(qsvt_pauli2_d2/d3).",
                  "observation": res}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("QSVT Hamiltonian-sim 관측 (e^{-iAt}, A=(XX+ZZ)/2, t=1.0):", flush=True)
        for r in res["chebyshev_error_by_degree"]:
            print(f"  Chebyshev degree {r['degree']}: ‖P_d(A) - e^{{-iAt}}‖_F = {r['frobenius_error']}", flush=True)
        print(f"  → exact at degree {res['exact_at_degree']} (고유값 {len(res['eigenvalues'])}개 → 유한차수 정확)", flush=True)
        print(f"  QSVT realizes: even={res['qsvt_realizes']['even_chebyshev']} · odd={res['qsvt_realizes']['odd_chebyshev']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"qsvt_hamsim_observe: all_ok={all_ok}", flush=True)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
