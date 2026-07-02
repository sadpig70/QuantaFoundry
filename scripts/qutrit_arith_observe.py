#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""qutrit_arith_observe — HE H6.1′: 큐트릿 삼진 산술 관측 + qudit 게이트 경계 문서화 (신규 봉인 0).

봉인된 qutrit_x3(순환 +1)·qutrit_sum(삼진 가산기)의 대수 성질을 관측한다:
  1. X₃ 위수 3: X₃³ == I (큐트릿 부분공간 {0,1,2}), sink |11> 고정.
  2. SUM 교환성: (a+b) mod 3 == (b+a) mod 3 (전 a,b∈{0,1,2}).
  3. SUM 결합/영원: 0 + b == b.
  4. C4 독립참조: golden 순열 == 정수 삼진 산술.

★qudit 축 게이트 경계(정직 문서화, seal 아님):
  - 봉인 계층 = **큐트릿 삼진 산술(계산기저 permutation)** exact — X₃·SUM.
  - 게이트 계층(차기) = ω=e^{2πi/3}·1/√3 비-dyadic 위상: Z₃=diag(1,ω,ω²)·큐트릿 QFT₃·Bell₃
    (|00⟩+|11⟩+|22⟩)/√3 — 신규 module 필요, 산술 계층과 **분리 명시**(INV-Q3).
  - 임베딩(|11> sink)은 해석 — 오라클은 표준 2ⁿ 유니터리로만 검증.

사용: python scripts/qutrit_arith_observe.py [--quick]
"""
import os, sys, re, json
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".pgf", "proofs", "QUTRIT-ARITH-OBSERVE.json")
VAL = {(0, 0): 0, (0, 1): 1, (1, 0): 2, (1, 1): 3}


def load_golden(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    ns = {}
    exec(re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1), ns)
    return ns["golden"]


def observe():
    X3 = load_golden("qutrit_x3.app.pg")            # 4×4
    SUM = load_golden("qutrit_sum.app.pg")          # 16×16
    # 1) X₃ 위수 3 (부분공간 {0,1,2} + sink 3 고정)
    X3cubed = np.linalg.matrix_power(X3, 3)
    order3 = bool(np.allclose(X3cubed, np.eye(4)))
    sink_fixed = bool(abs(X3[3, 3] - 1) < 1e-12)
    # 2) X₃ 궤도
    orbit = []
    v = 0
    for _ in range(3):
        v = int(np.argmax(np.abs(X3[:, v])))
        orbit.append(v)
    orbit_ok = orbit == [1, 2, 0]
    # 3) SUM 삼진 산술: golden == 정수 (a+b) mod 3, 교환성
    def sum_out(a, b):                               # a,b in {0,1,2}; q0q1=a, q2q3=b (big-endian)
        x = (a << 2) | b
        o = int(np.argmax(np.abs(SUM[:, x])))
        return VAL[((o >> 1) & 1, o & 1)]            # b' = q2q3 = 하위 2비트
    arith_ok, comm_ok = True, True
    for a in range(3):
        for b in range(3):
            got = sum_out(a, b)
            if got != (a + b) % 3:
                arith_ok = False
            if sum_out(a, b) != sum_out(b, a):
                comm_ok = False
    ident_ok = all(sum_out(0, b) == b for b in range(3))
    ok = order3 and sink_fixed and orbit_ok and arith_ok and comm_ok and ident_ok
    return {"axis": "qudit (#F) — 큐트릿 qubit-임베딩 삼진 산술",
            "sealed_assets": "qutrit_x3(+1 mod3)·qutrit_sum((a+b) mod3)",
            "X3_order_3": order3, "X3_orbit_0": orbit, "sink_11_fixed": sink_fixed,
            "SUM_matches_integer_ternary": arith_ok, "SUM_commutative": comm_ok,
            "SUM_zero_identity": ident_ok,
            "gate_boundary": {"sealed_exact": "ternary arithmetic (permutation): X₃·SUM",
                              "gated_next": "ω=e^{2πi/3}·1/√3 phases — Z₃·QFT₃·Bell₃ (신규 module 필요)"},
            "honest_boundary": "봉인=삼진 산술 순열 exact 뿐(INV-Q3). qudit Fourier/중첩=게이트 계층(분리). "
                               "임베딩 |11> sink=해석, 오라클은 표준 2ⁿ 검증. 신규 봉인 0.",
            "ok": bool(ok)}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        report = {"_schema": "qutrit-arith-observe-v1",
                  "_note": "큐트릿 삼진 산술 관측 + qudit 게이트 경계. 봉인=순열 exact 뿐(INV-Q3). 신규 봉인 0.",
                  "observation": res}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("큐트릿 삼진 산술 관측 (qudit 축 개창):", flush=True)
        print(f"  X₃ 위수3={res['X3_order_3']} 궤도0→{res['X3_orbit_0']} sink고정={res['sink_11_fixed']}", flush=True)
        print(f"  SUM 삼진산술일치={res['SUM_matches_integer_ternary']} 교환={res['SUM_commutative']} 영원={res['SUM_zero_identity']}", flush=True)
        print(f"  게이트 경계: 봉인={res['gate_boundary']['sealed_exact']}", flush=True)
        print(f"              차기(게이트)={res['gate_boundary']['gated_next']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"qutrit_arith_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
