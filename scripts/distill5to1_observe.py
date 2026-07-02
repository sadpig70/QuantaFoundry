#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""distill5to1_observe — HE H3.1: [[5,1,3]] 5-to-1 magic state distillation 관측 (coherent-branch).

봉인된 code513_encoder(U_enc, 오각형 graph code)로 Bravyi-Kitaev(2005) 5-to-1 증류를 관측한다:
    5개 이상적 T-type magic state → U_enc†(decoder) → syndrome(q1..q4)=0000 branch 로 사영
    → 출력 qubit = **정확히 T-type magic state** (fixed-point).

T-type magic state: ρ=(I + (X+Y+Z)/√3)/2 의 순수상태 — Bloch 축 (±1,±1,±1)/√3 (8종, Clifford 동치).
측정→coherent branch 치환: 사영측정 대신 decoder 유니터리 적용 후 계산기저 branch 진폭을 관측.

★관측 결과(설계 검증 완료):
  - 입력 축 (1,1,1)/√3 → 출력 축 (−1,−1,1)/√3 **|r|=1 순수, fid=1.0 exact** (축 관계=encoder 논리
    twist V†X⁵V=−Z·V†Z⁵V=X 의 귀결, Clifford 동치).
  - 성공확률 p = 1/6 (이상적 입력, 닫힌형).
  - teeth: 비-magic 입력(|0⟩⁵)은 출력이 T-축 어느 것과도 fid<1.

정직 경계(INV-Q3, seal 아님, root 불변):
  - 봉인 = code513_encoder 의 exact Clifford 유니터리(이상적 증류 회로의 핵심)뿐.
  - fixed-point·성공확률·post-selection 확률적 성격·(잡음 입력의) fidelity 향상 = **관측**.
  - T-type 상태 자체(β=½arccos(1/√3) 비-dyadic 각) = 봉인 불가 → 관측에서 수학적 정의로만 사용.
  - 신규 봉인 = code513_encoder 1개(Clifford). distillation *프로토콜*은 봉인 아님.

사용: python scripts/distill5to1_observe.py [--quick]
"""
import os, sys, re, json
from functools import reduce
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".pgf", "proofs", "DISTILL5TO1-OBSERVE.json")
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def load_encoder():
    src = open(os.path.join(ROOT, "specs", "apps", "code513_encoder.app.pg"), encoding="utf-8").read()
    ns = {}
    exec(re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1), ns)
    return ns["golden"]


def pstr(s):
    return reduce(np.kron, [{"I": I, "X": X, "Y": Y, "Z": Z}[c] for c in s])


def bloch(psi):
    return np.array([np.real(np.vdot(psi, P @ psi)) for P in (X, Y, Z)])


def t_axes():
    from itertools import product
    return [np.array(v) / np.sqrt(3) for v in product([1, -1], repeat=3)]


def observe():
    U = load_encoder()
    V = U[:, [0, 16]]                                  # isometry columns |0 0000>, |1 0000>
    # 1) 봉인 재확인: 4 stabilizer 가 V 고정 + 논리 twist
    stabs = ["XZZXI", "IXZZX", "XIXZZ", "ZXIXZ"]
    stab_ok = all(bool(np.allclose(pstr(s) @ V, V)) for s in stabs)
    twist_ok = bool(np.allclose(V.conj().T @ pstr("XXXXX") @ V, -Z)) and \
               bool(np.allclose(V.conj().T @ pstr("ZZZZZ") @ V, X))
    # 2) T-type magic state (축 (1,1,1)/√3 +1 고유상태)
    w, vv = np.linalg.eigh((X + Y + Z) / np.sqrt(3))
    tplus = vv[:, np.argmax(w)]
    inp = reduce(np.kron, [tplus] * 5)
    out = U.conj().T @ inp                             # decoder = U†
    amp = np.array([out[0], out[16]])                  # syndrome q1..q4 = 0000 branch
    p_succ = float(np.linalg.norm(amp) ** 2)
    cond = amp / np.linalg.norm(amp)
    r = bloch(cond)
    pure = bool(abs(np.linalg.norm(r) - 1.0) < 1e-9)
    hit = [ax for ax in t_axes() if (1 + r @ ax) / 2 > 1 - 1e-9]
    fixed_point = pure and len(hit) == 1
    # 3) teeth: 비-magic 입력 |0>^5 → 어느 T-축과도 fid<1
    inp0 = np.zeros(32, dtype=complex); inp0[0] = 1.0
    out0 = U.conj().T @ inp0
    a0 = np.array([out0[0], out0[16]])
    c0 = a0 / np.linalg.norm(a0)
    r0 = bloch(c0)
    teeth = bool(all((1 + r0 @ ax) / 2 < 1 - 1e-6 for ax in t_axes()))
    ok = stab_ok and twist_ok and fixed_point and abs(p_succ - 1 / 6) < 1e-9 and teeth
    return {"protocol": "Bravyi-Kitaev 2005 5-to-1 T-type distillation (coherent-branch)",
            "sealed_asset": "code513_encoder ([[5,1,3]] 오각형 graph code, Clifford Tier-0)",
            "stabilizers_fix_isometry": stab_ok,
            "logical_twist": {"V†X⁵V==−Z": True, "V†Z⁵V==X": True, "ok": twist_ok},
            "input_axis": "(1,1,1)/√3", "output_axis": str(np.round(r * np.sqrt(3), 6).tolist()),
            "output_pure_exact_magic": fixed_point,
            "success_probability": round(p_succ, 9), "success_probability_closed_form": "1/6",
            "teeth_nonmagic_input_not_T": teeth,
            "honest_boundary": "봉인=encoder Clifford exact. fixed-point·성공확률·post-selection 확률성="
                               "관측(INV-Q3). T-type 상태(비-dyadic 각)=수학 정의로만 사용, 봉인 아님.",
            "ok": bool(ok)}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        report = {"_schema": "distill5to1-observe-v1",
                  "_note": "5-to-1 magic distillation coherent-branch 관측. 봉인=code513_encoder 뿐. "
                           "프로토콜 자체=관측(INV-Q3).",
                  "observation": res}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("[[5,1,3]] 5-to-1 magic state distillation 관측 (coherent-branch):", flush=True)
        print(f"  stabilizer 고정={res['stabilizers_fix_isometry']} · 논리 twist={res['logical_twist']['ok']}", flush=True)
        print(f"  입력축 (1,1,1)/√3 → 출력축 {res['output_axis']}/√3 · 순수 exact magic={res['output_pure_exact_magic']}", flush=True)
        print(f"  성공확률 p={res['success_probability']} (=1/6 닫힌형)", flush=True)
        print(f"  teeth(비-magic 입력≠T-type)={res['teeth_nonmagic_input_not_T']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"distill5to1_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
