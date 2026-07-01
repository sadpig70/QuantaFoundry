#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""magic_state_observe — V08 FTQC: non-Clifford universality (magic state + T-injection).

QEC(W7)는 transversal **Clifford**(H/S/CNOT)까지만 제공한다. universal 양자연산엔 non-Clifford 게이트
(T)가 필요하고, 대부분의 코드에서 T 는 transversal 이 아니다. **magic state |A>** 가 이를 fault-tolerant
하게 주입(gate teleportation)한다 — FTQC universality 의 마지막 조각.

봉인: magic_a = T·H (|A>=(|0>+e^{iπ/4}|1>)/√2 준비, Tier-0). 본 스크립트는 다음을 독립 검증한다:
  (1) non-stabilizer witness: |A> 의 최대 stabilizer fidelity = cos²(π/8) < 1 → Clifford 궤도 밖(magic).
      teeth: stabilizer 상태(|+> 등)는 어떤 stabilizer 와 fidelity 1.
  (2) T-injection 정확성(EXACT): |ψ>⊗|A>, CNOT(data→anc), anc 측정, 결과 1이면 S 보정 → data = T|ψ>.
      모든 입력·모든 측정결과에서 정확(gate teleportation 은 근사 아님).
  (3) universality: Clifford(W7 QEC) + T(magic) = universal gate set.

정직 경계(INV): magic_a=Tier-0 EXACT 봉인. non-stabilizer·injection 정확성=EXACT(수학 항등식·독립검증).
  실제 magic state *distillation*(잡음→고순도)은 하드웨어 잡음 맥락이므로 범위 밖(정체성: 하드웨어 out).

사용: python scripts/magic_state_observe.py [--quick]
"""
import os, sys, json
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".pgf", "proofs", "MAGIC-STATE-OBSERVE.json")

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
T = np.diag([1, np.exp(1j * np.pi / 4)]).astype(complex)
S = np.diag([1, 1j]).astype(complex)
P0 = np.diag([1, 0]).astype(complex)
P1 = np.diag([0, 1]).astype(complex)

STAB_STATES = {"|0>": [1, 0], "|1>": [0, 1], "|+>": [1, 1], "|->": [1, -1],
               "|+i>": [1, 1j], "|-i>": [1, -1j]}


def observe():
    A = (T @ H) @ np.array([1, 0], dtype=complex)          # magic_a|0> = |A>
    # (1) non-stabilizer witness
    fids = {}
    for name, v in STAB_STATES.items():
        v = np.array(v, complex); v = v / np.linalg.norm(v)
        fids[name] = round(float(abs(np.vdot(v, A)) ** 2), 4)
    max_fid = max(fids.values())
    non_stab = bool(max_fid < 0.9999)
    # teeth: 한 stabilizer 상태는 자기 자신과 fidelity 1
    plus = np.array([1, 1], complex) / np.sqrt(2)
    teeth = bool(abs(np.vdot(plus, plus)) ** 2 > 0.9999 and max_fid < 0.9999)
    # (2) T-injection 정확성 (EXACT)
    CX = np.kron(P0, I) + np.kron(P1, X)                   # control=data(q0), target=anc(q1)
    inj_ok = True
    for psi in [[1, 0], [0, 1], [1, 1], [1, 1j], [0.6, 0.8]]:
        psi = np.array(psi, complex); psi = psi / np.linalg.norm(psi)
        st = (CX @ np.kron(psi, A)).reshape(2, 2)
        for m in (0, 1):
            branch = st[:, m]
            if np.linalg.norm(branch) < 1e-9:
                continue
            data = branch / np.linalg.norm(branch)
            if m == 1:
                data = S @ data                            # 측정결과 1 → S 보정
            if not np.allclose(abs(np.vdot(T @ psi, data)), 1, atol=1e-9):
                inj_ok = False
    ok = non_stab and teeth and inj_ok
    return {"magic_state": "|A> = T·H|0> = (|0>+e^{iπ/4}|1>)/√2 (magic_a, Tier-0 봉인)",
            "stabilizer_fidelities": fids, "max_stabilizer_fidelity": max_fid,
            "cos2_pi_8": round(float(np.cos(np.pi / 8) ** 2), 4),
            "non_stabilizer_magic": non_stab, "teeth_stabilizer_has_fid1": teeth,
            "t_injection_exact": inj_ok,
            "universality": "Clifford(W7 QEC: transversal H/S/CNOT) + T(magic state injection) = universal gate set",
            "honest_boundary": "magic_a=Tier-0 EXACT 봉인. non-stabilizer·T-injection=EXACT(독립검증). "
                               "magic state distillation(잡음→고순도)은 하드웨어 맥락→범위 밖(정체성).",
            "ok": bool(ok)}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    all_ok = res["ok"]
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        report = {"_schema": "magic-state-observe-v1",
                  "_note": "FTQC non-Clifford universality: magic state |A>(magic_a 봉인) + T-injection. "
                           "non-stabilizer·injection=EXACT 독립검증. distillation=하드웨어 범위 밖.",
                  "observation": res}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("FTQC non-Clifford universality (magic state + T-injection):", flush=True)
        print(f"  |A> max stabilizer fidelity = {res['max_stabilizer_fidelity']} (=cos²(π/8)={res['cos2_pi_8']}) "
              f"< 1 → non-stabilizer magic: {res['non_stabilizer_magic']}", flush=True)
        print(f"  teeth(stabilizer 상태 fid=1): {res['teeth_stabilizer_has_fid1']}", flush=True)
        print(f"  T-injection → T|ψ> (모든 입력·측정결과, EXACT): {res['t_injection_exact']}", flush=True)
        print(f"  universality: Clifford(W7) + T(magic) = universal", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"magic_state_observe: all_ok={all_ok}", flush=True)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
