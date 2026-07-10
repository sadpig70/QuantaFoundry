#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""braid_observe — HE2 P4.1: Ising/Majorana 브레이드 Yang-Baxter 관계 관측 (신규 봉인 0).

봉인된 ising_braid_b2(B₂, 유일 entangling 브레이드)와 단일큐빗 브레이드 b₁=S†⊗I·b₃=I⊗S†로
브레이드 군 관계(Yang-Baxter)를 실증한다:
    B₁B₂B₁ == B₂B₁B₂   (인접 생성자, 위상-제거 버전에서 정확 성립 — 전역위상 동일 e^{iπ/4})
    B₂B₃B₂ == B₃B₂B₃

또 Ising 브레이드가 Clifford(Pauli→Pauli 켤레)임을 확인.

정직 경계(INV-Q3, seal 아님, root 불변):
  - 봉인 = ising_braid_b2(Clifford exact)뿐. Yang-Baxter 관계·Clifford 성질 = 관측.
  - Ising anyon = Clifford 만(non-universal). Fibonacci anyon(황금비 진폭)·Jones 다항식·
    universality = 비-dyadic 차기 게이트. 신규 봉인 0.

사용: python -m qf_witness.observe.braid_observe [--quick]
"""
import os, sys, re, json, itertools
import numpy as np

from qf_witness.core.paths import ROOT
OUT = os.path.join(ROOT, ".pgf", "proofs", "BRAID-OBSERVE.json")
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
Sd = np.diag([1, -1j]).astype(complex)
PAULI = {"I": I, "X": X, "Y": Y, "Z": Z}


def load_golden(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    ns = {}
    exec(re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1), ns)
    return ns["golden"]


def observe():
    b2 = load_golden("ising_braid_b2.app.pg")
    b1 = np.kron(Sd, I)                                # B₁ = exp(π/4 γ₁γ₂) up-to-phase = S†⊗I
    b3 = np.kron(I, Sd)                                # B₃ up-to-phase = I⊗S†
    # Yang-Baxter (braid relations)
    yb12 = bool(np.allclose(b1 @ b2 @ b1, b2 @ b1 @ b2))
    yb23 = bool(np.allclose(b2 @ b3 @ b2, b3 @ b2 @ b3))
    # Ising braid Clifford: b2 P b2† is a Pauli (up to sign) for all 2-qubit Paulis
    def is_pauli(M):
        for lbl in itertools.product("IXYZ", repeat=2):
            P = np.kron(PAULI[lbl[0]], PAULI[lbl[1]])
            for s in (1, -1, 1j, -1j):
                if np.allclose(M, s * P):
                    return True
        return False
    clifford = all(is_pauli(b2 @ np.kron(PAULI[a], PAULI[b]) @ b2.conj().T)
                   for a in "IXYZ" for b in "IXYZ")
    # B₂ is genuinely entangling (not a product of single-qubit gates): CNOT-like
    entangling = bool(not np.allclose(np.abs(b2), np.abs(np.kron(b2[:2, :2] if False else I, I))))  # sanity placeholder
    # proper entangling check: operator Schmidt rank > 1
    R = b2.reshape(2, 2, 2, 2).transpose(0, 2, 1, 3).reshape(4, 4)
    entangling = bool(np.linalg.matrix_rank(R, tol=1e-9) > 1)
    ok = yb12 and yb23 and clifford and entangling
    return {"axis": "위상적 양자계산 — Ising/Majorana 브레이드 (JW 표현)",
            "sealed_asset": "ising_braid_b2 (B₂=exp(π/4 γ₂γ₃), entangling)",
            "yang_baxter_B1B2B1==B2B1B2": yb12, "yang_baxter_B2B3B2==B3B2B3": yb23,
            "ising_braid_is_clifford": clifford, "B2_entangling": entangling,
            "honest_boundary": "봉인=ising_braid_b2 Clifford exact 뿐. Yang-Baxter·Clifford성=관측. "
                               "Fibonacci anyon(황금비)·Jones 다항식·universality=비-dyadic 차기 게이트. 신규 봉인 0.",
            "ok": bool(ok)}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        report = {"_schema": "braid-observe-v1",
                  "_note": "Ising/Majorana 브레이드 Yang-Baxter 관계 관측. 봉인=ising_braid_b2 뿐(INV-Q3). 신규 봉인 0.",
                  "observation": res}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("Ising/Majorana 브레이드 Yang-Baxter 관측 (위상적 QC):", flush=True)
        print(f"  B₁B₂B₁==B₂B₁B₂: {res['yang_baxter_B1B2B1==B2B1B2']} · B₂B₃B₂==B₃B₂B₃: {res['yang_baxter_B2B3B2==B3B2B3']}", flush=True)
        print(f"  Ising 브레이드=Clifford: {res['ising_braid_is_clifford']} · B₂ entangling: {res['B2_entangling']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"braid_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
