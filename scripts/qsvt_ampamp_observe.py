#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""qsvt_ampamp_observe — V08 QSVT Consumer: amplitude amplification 관측 (observation).

amplitude amplification(Grover)의 핵심: 초기 진폭 a=sinθ 를 k회 반복하면 sin((2k+1)θ) 로 증폭된다.
이는 **진폭 a 의 홀수 다항식(degree 2k+1)** 이고, 그 홀수 다항식이 바로 QSP(Quantum Signal Processing)가
실현하는 것이다 — Grover 반복 = QSP 홀수 다항식의 두 실현. (Ham-sim consumer 의 자매: 검색 ↔ 물리.)

봉인된 QSP 기본블록: qsp_d1(degree-1 = k=0)·qsp_d3(degree-3 = k=1). 고차(k) 는 같은 구조의 반복.
본 스크립트는 여러 초기진폭에서 Grover 증폭 프로파일 sin((2k+1)θ) 과 최적 반복수를 **고전 관측**한다.

정직 경계(INV-Q3, seal 아님):
  - 봉인 = 정확한 QSP 홀수 다항식 유니터리(qsp_d1/d3, Tier-0). 증폭 프로파일 자체는 고전 관측.
  - 기존 W9 amplitude amplification/estimation(grover3·qae) 봉인과 동일 수학(sin((2k+1)θ))을 QSP 로 통합.

사용: python scripts/qsvt_ampamp_observe.py [--quick]
"""
import os, sys, json
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".pgf", "proofs", "QSVT-AMPAMP-OBSERVE.json")


def observe(amps=(0.1, 0.2, 0.3, 0.5), kmax=4):
    rows = []
    for a in amps:
        th = float(np.arcsin(a))
        iters = [{"k": k, "degree": 2 * k + 1,
                  "amplitude": round(float(np.sin((2 * k + 1) * th)), 4),
                  "prob_good": round(float(np.sin((2 * k + 1) * th) ** 2), 4)} for k in range(kmax + 1)]
        # 최적 반복수: (2k+1)θ ≈ π/2 → k ≈ (π/2θ - 1)/2
        k_opt = int(round((np.pi / (2 * th) - 1) / 2))
        rows.append({"a0": a, "theta": round(th, 4), "iterations": iters,
                     "optimal_k": k_opt, "prob_at_optimal": round(float(np.sin((2 * k_opt + 1) * th) ** 2), 4)})
    return {"mechanism": "Grover amplitude amplification: a=sinθ → sin((2k+1)θ) = 진폭의 홀수다항식(deg 2k+1)",
            "profiles": rows,
            "qsp_realizes": {"degree_1_k0": "qsp_d1 (봉인 Tier-0)", "degree_3_k1": "qsp_d3 (봉인 Tier-0)",
                             "note": "고차 k 는 동일 QSP 구조 반복 — Grover 반복 = QSP 홀수 다항식"},
            "unifies_sealed": "W9 amplitude amplification/estimation(grover3·qae3) 와 동일 수학을 QSP 로 통합",
            "honest_boundary": "봉인=정확 QSP 홀수 다항식 유니터리(qsp_d1/d3). 증폭 프로파일=고전관측(INV-Q3, seal 아님). "
                               "검색(amp-amp)과 물리(Ham-sim)가 같은 QSVT/QSP 프레임워크의 두 consumer."}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    # sanity: 각 a 의 최적 반복에서 prob_good 이 향상(증폭)됐는가
    all_ok = all(p["prob_at_optimal"] >= p["a0"] ** 2 for p in res["profiles"])
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        report = {"_schema": "qsvt-ampamp-observe-v1",
                  "_note": "Grover amplitude amplification = QSP 홀수 다항식(deg 2k+1) 고전관측. seal 아님(INV-Q3). "
                           "봉인은 정확 QSP 블록(qsp_d1/d3). Ham-sim consumer 의 자매(검색↔물리).",
                  "observation": res}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("QSVT amplitude amplification 관측 (a → sin((2k+1)θ)):", flush=True)
        for p in res["profiles"]:
            amps = " ".join(f"k{it['k']}={it['prob_good']}" for it in p["iterations"])
            print(f"  a0={p['a0']}: {amps} · 최적 k={p['optimal_k']}(P_good={p['prob_at_optimal']})", flush=True)
        print("  QSP realizes: deg1=qsp_d1(k=0) · deg3=qsp_d3(k=1) [봉인 Tier-0]", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"qsvt_ampamp_observe: all_ok={all_ok}", flush=True)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
