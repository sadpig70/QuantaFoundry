# -*- coding: utf-8 -*-
"""
qae_family.py — Stage 9 W9.2 AmplitudeEstimation (QAE)

W9.1(amplitude amplification)을 amplitude estimation으로 상승: Grover/Q 연산자에 QPE를 걸어 진폭 a를
*추정*하는 회로를 봉인. exact instance(θ=π/8 → a=sin²(π/8), t=3 counting이 정확히 읽음). Shor의
controlled-U^{2^j} + 봉인 iqft3 근육 복리. honest 분해(controlled-Ry = 표준 CNOT·Ry 사다리).

봉인 대상(전부 Tier-0 EXACT):
 모듈(analytic Ry, Ry(α)=YPowGate(α/π) up-to-phase, ry_k 패턴):
   ry_pi4=Ry(π/4) · ry_negpi4=Ry(-π/4) · ry_pi2=Ry(π/2) · ry_negpi2=Ry(-π/2).
 앱:
   cry_pi2 (2q) = controlled-Ry(π/2) = (I⊗Ry(π/4))·CNOT·(I⊗Ry(-π/4))·CNOT.
   cry_pi  (2q) = controlled-Ry(π)   = (I⊗Ry(π/2))·CNOT·(I⊗Ry(-π/2))·CNOT.
   qae3_pi8 (4q) = QPE(t=3) on Grover Q=Ry(π/2) → 진폭 a=sin²(π/8) 추정 회로.

정직성 경계:
 - 봉인 = 회로 분해의 정확성. golden=closed-form, composite=봉인 부품(honest CNOT·Ry 사다리, MatrixGate 0).
   Ry 모듈은 전역위상 C4 무시(up-to-phase). 봉인 iqft3·cnot·h_gate·z_gate 복리.
 - 봉인 아님 = 진폭 추정 *행동*(_estimation_observation): 봉인 QAE 실행→counting 측정→a_est.
   exact instance라 양 peak y∈{1,7}이 정확히 a_est=sin²(π/8). W9.1 amplification → W9.2 estimation.
 - QAE 원리: Grover Q 고유위상 ±2θ 를 QPE 가 읽음 → a=sin²θ.

사용:  python scripts/qae_family.py
"""
from __future__ import annotations

import os
import sys
import json
import subprocess

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, ORACLE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import verify_seal as vs        # noqa: E402  (모듈 봉인 CLI — 사용만)
import app_assemble as aa       # noqa: E402  (앱 봉인 — 사용만)

SPECS_MODS = os.path.join(ROOT, "specs", "modules")
SPECS_APPS = os.path.join(ROOT, "specs", "apps")
MODREG = os.path.join(ROOT, "registry", "modules")
APPREG = os.path.join(ROOT, "registry", "apps")
OUT = os.path.join(ROOT, ".pgf", "arith")


# ── 모듈 spec: analytic Ry (YPowGate(α/π) up-to-phase) ──────────────────────────
def _ry_spec(name, exp, ang_expr, desc):
    return (
        f"# {name} — {desc}. Ry(α)=YPowGate(exponent=α/π) up-to-phase(C4). analytic golden.\n"
        "```python id=bloq\n"
        "import numpy as np\n"
        "from qualtran.bloqs.basic_gates import YPowGate\n"
        f"bloq = YPowGate(exponent={exp})\n"
        "```\n"
        "```python id=golden\n"
        "import numpy as np\n"
        f"a = {ang_expr}\n"
        "golden = np.array([[np.cos(a/2), -np.sin(a/2)], [np.sin(a/2), np.cos(a/2)]], dtype=complex)\n"
        "```\n"
        '```json id=meta\n'
        + json.dumps({"id": name, "n_sys": 1, "n_anc": 0}) + "\n"
        "```\n")


def _seal_module(name, spec):
    sp = os.path.join(SPECS_MODS, f"{name}.pg")
    open(sp, "w", encoding="utf-8", newline="\n").write(spec)
    rc = subprocess.run([sys.executable, os.path.join(ORACLE, "verify_seal.py"), sp, "--out", MODREG],
                        capture_output=True, text=True, cwd=ORACLE).returncode
    p = os.path.join(MODREG, f"{name}.sealed.json")
    if rc != 0 or not os.path.exists(p):
        return {"id": name, "sealed": False}
    sealed = json.load(open(p, encoding="utf-8"))
    return {"id": name, "n_sys": sealed["n_sys"], "sealed": True,
            "tier": sealed.get("tier", 0), "u_hash": sealed["u_hash"]}


# ── 앱 spec: controlled-Ry (honest CNOT·Ry 사다리) ───────────────────────────────
def _cry_spec(name, ang_expr, half_pos, half_neg, desc):
    return (
        f"# {name} — {desc}. controlled-Ry = (I⊗Ry(φ/2))·CNOT·(I⊗Ry(-φ/2))·CNOT (표준 항등식). "
        f"plan=봉인 cnot·{half_pos}·{half_neg}, no MatrixGate.\n"
        '```json id=app_meta\n'
        + json.dumps({"id": name, "n_sys": 2, "n_anc": 0}) + "\n"
        "```\n"
        "```python id=app_golden\n"
        "import numpy as np\n"
        f"a = {ang_expr}\n"
        "Ry = np.array([[np.cos(a/2), -np.sin(a/2)], [np.sin(a/2), np.cos(a/2)]], dtype=complex)\n"
        "golden = np.eye(4, dtype=complex); golden[2:, 2:] = Ry   # |1><1|⊗Ry, control=MSB\n"
        "```\n"
        '```json id=plan\n'
        + json.dumps({"steps": [
            {"spec": "../modules/cnot.pg", "targets": [0, 1]},
            {"spec": f"../modules/{half_neg}.pg", "targets": [1]},
            {"spec": "../modules/cnot.pg", "targets": [0, 1]},
            {"spec": f"../modules/{half_pos}.pg", "targets": [1]}]}) + "\n"
        "```\n")


# ── 앱 spec: 전체 QAE 회로 (4q) ──────────────────────────────────────────────────
_QAE3_SPEC = (
    "# qae3_pi8 — QPE(t=3 counting) on Grover Q=Ry(π/2) → 진폭 a=sin²(π/8) 추정 회로 (4q). "
    "Q^4=-I→z_gate(control)·Q^2=Ry(π)→cry_pi·Q^1=Ry(π/2)→cry_pi2. 봉인 iqft3 복리. golden=16×16 closed-form.\n"
    '```json id=app_meta\n'
    '{"id": "qae3_pi8", "n_sys": 4, "n_anc": 0}\n'
    "```\n"
    "```python id=app_golden\n"
    "import numpy as np\n"
    "n=4\n"
    "def Ry(al): return np.array([[np.cos(al/2),-np.sin(al/2)],[np.sin(al/2),np.cos(al/2)]],dtype=complex)\n"
    "I2=np.eye(2,dtype=complex); Z=np.diag([1,-1]).astype(complex)\n"
    "H1=np.array([[1,1],[1,-1]],dtype=complex)/np.sqrt(2)\n"
    "def emb(g,qs):\n"
    "    k=len(qs); G=g.reshape([2]*k+[2]*k)\n"
    "    T=np.eye(1<<n,dtype=complex).reshape([2]*n+[1<<n])\n"
    "    T=np.tensordot(G,T,axes=(list(range(k,2*k)),qs)); T=np.moveaxis(T,list(range(k)),qs)\n"
    "    return T.reshape(1<<n,1<<n)\n"
    "def cU(U):\n"
    "    M=np.eye(4,dtype=complex); M[2:,2:]=U; return M\n"
    "N=8; w=np.exp(2j*np.pi/N)\n"
    "QFT3=np.array([[w**(j*k) for k in range(N)] for j in range(N)],dtype=complex)/np.sqrt(N)\n"
    "iqft3=QFT3.conj().T\n"
    "Q=Ry(np.pi/2)\n"
    "U=np.eye(1<<n,dtype=complex)\n"
    "U=emb(Ry(np.pi/4),[3])@U                                   # A 진폭준비 (a=sin²(π/8))\n"
    "for q in range(3): U=emb(H1,[q])@U                         # H on counting\n"
    "U=emb(cU(np.linalg.matrix_power(Q,4)),[0,3])@U             # controlled-Q^4 (=-I → z on ctrl)\n"
    "U=emb(cU(np.linalg.matrix_power(Q,2)),[1,3])@U             # controlled-Q^2\n"
    "U=emb(cU(np.linalg.matrix_power(Q,1)),[2,3])@U             # controlled-Q^1\n"
    "U=emb(iqft3,[0,1,2])@U                                     # inverse QFT on counting\n"
    "golden=U\n"
    "```\n"
    '```json id=plan\n'
    + json.dumps({"steps": [
        {"spec": "../modules/ry_pi4.pg", "targets": [3]},
        {"spec": "../modules/h_gate.pg", "targets": [0]},
        {"spec": "../modules/h_gate.pg", "targets": [1]},
        {"spec": "../modules/h_gate.pg", "targets": [2]},
        {"spec": "../modules/z_gate.pg", "targets": [0]},
        {"app": "cry_pi.app.pg", "targets": [1, 3]},
        {"app": "cry_pi2.app.pg", "targets": [2, 3]},
        {"app": "iqft3.app.pg", "targets": [0, 1, 2]}]}) + "\n"
    "```\n")


def _forge_app(name, spec):
    sp = os.path.join(SPECS_APPS, f"{name}.app.pg")
    open(sp, "w", encoding="utf-8", newline="\n").write(spec)
    v = aa.assemble(sp, APPREG)
    return {"id": name, "n_sys": v.n_sys, "sealed": bool(v.sealed), "tier": v.tier,
            "u_hash": v.u_hash, "reason": v.reason}


# ── 정직-behavior 관찰 (seal 아님): 진폭 추정 readout ────────────────────────────
def _estimation_observation():
    n = 4
    t = 3
    th = np.pi / 8

    def Ry(al):
        return np.array([[np.cos(al / 2), -np.sin(al / 2)], [np.sin(al / 2), np.cos(al / 2)]], dtype=complex)

    def emb(g, qs):
        k = len(qs)
        G = g.reshape([2] * k + [2] * k)
        T = np.eye(1 << n, dtype=complex).reshape([2] * n + [1 << n])
        T = np.tensordot(G, T, axes=(list(range(k, 2 * k)), qs))
        T = np.moveaxis(T, list(range(k)), qs)
        return T.reshape(1 << n, 1 << n)

    def cU(U):
        M = np.eye(4, dtype=complex)
        M[2:, 2:] = U
        return M

    N = 8
    w = np.exp(2j * np.pi / N)
    QFT3 = np.array([[w ** (j * k) for k in range(N)] for j in range(N)], dtype=complex) / np.sqrt(N)
    iqft3 = QFT3.conj().T
    Q = Ry(np.pi / 2)
    U = np.eye(1 << n, dtype=complex)
    U = emb(Ry(np.pi / 4), [3]) @ U
    for q in range(3):
        U = emb(H1 := np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2), [q]) @ U
    U = emb(cU(np.linalg.matrix_power(Q, 4)), [0, 3]) @ U
    U = emb(cU(np.linalg.matrix_power(Q, 2)), [1, 3]) @ U
    U = emb(cU(np.linalg.matrix_power(Q, 1)), [2, 3]) @ U
    U = emb(iqft3, [0, 1, 2]) @ U

    psi = np.zeros(1 << n, dtype=complex)
    psi[0] = 1.0
    psi = U @ psi
    p = np.abs(psi) ** 2
    marg = {}
    for i in range(1 << n):
        if p[i] > 1e-9:
            c = i >> 1   # counting = top t bits, work = LSB
            marg[c] = marg.get(c, 0.0) + float(p[i])
    a_true = float(np.sin(th) ** 2)
    peaks = []
    for y in sorted(marg, key=lambda k: -marg[k]):
        if marg[y] > 1e-6:
            peaks.append({"y": int(y), "prob": round(marg[y], 6),
                          "a_est": round(float(np.sin(np.pi * y / (1 << t)) ** 2), 6)})
    exact = all(abs(pk["a_est"] - a_true) < 1e-6 for pk in peaks)
    return {"note": "OBSERVATION, NOT A SEAL — the sealed QAE circuit is executed on |0>; the counting "
                    "register measurement y yields a_est=sin^2(pi*y/2^t). This is amplitude ESTIMATION "
                    "behavior (W9.1 was amplification). Exact instance: both peaks recover the true a.",
            "a_true": round(a_true, 6), "t_counting": t, "peaks": peaks, "exact_recovery": bool(exact)}


def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 86)
    print("W9.2 AmplitudeEstimation (QAE) — Grover Q 에 QPE → 진폭 추정. exact a=sin²(π/8) instance.")
    print("=" * 86)

    mods = [
        _seal_module("ry_pi4", _ry_spec("ry_pi4", "0.25", "np.pi/4", "Ry(π/4) 진폭준비/반각")),
        _seal_module("ry_negpi4", _ry_spec("ry_negpi4", "-0.25", "-np.pi/4", "Ry(-π/4) 반각")),
        _seal_module("ry_pi2", _ry_spec("ry_pi2", "0.5", "np.pi/2", "Ry(π/2)=Grover Q/반각")),
        _seal_module("ry_negpi2", _ry_spec("ry_negpi2", "-0.5", "-np.pi/2", "Ry(-π/2) 반각")),
    ]
    for m in mods:
        print(f"[Module] {m['id']:12} n_sys={m.get('n_sys')} sealed={m['sealed']} tier={m.get('tier')} "
              f"u={str(m.get('u_hash'))[:14]}")

    apps = [
        _forge_app("cry_pi2", _cry_spec("cry_pi2", "np.pi/2", "ry_pi4", "ry_negpi4", "controlled-Ry(π/2)")),
        _forge_app("cry_pi", _cry_spec("cry_pi", "np.pi", "ry_pi2", "ry_negpi2", "controlled-Ry(π)")),
        _forge_app("qae3_pi8", _QAE3_SPEC),
    ]
    for a in apps:
        print(f"[App]    {a['id']:12} n_sys={a.get('n_sys')} sealed={a['sealed']} tier={a.get('tier')} "
              f"u={str(a.get('u_hash'))[:14]}" + ("" if a["sealed"] else f"  reason={a['reason']}"))

    obs = _estimation_observation()
    print(f"[Behavior] 진폭 추정 readout(seal 아님): a_true={obs['a_true']} (=sin²(π/8))")
    for pk in obs["peaks"]:
        print(f"   y={pk['y']} (prob {pk['prob']}) → a_est=sin²(π·{pk['y']}/8)={pk['a_est']}")
    print(f"   exact_recovery={obs['exact_recovery']} (양 peak이 진짜 a를 정확 복원)")

    report = {
        "phase": "W9.2 AmplitudeEstimation (QAE)",
        "honesty": "Raises W9.1 (amplitude amplification) to amplitude ESTIMATION: QPE on the Grover Q "
                   "operator estimates the amplitude a. Sealed Tier-0 EXACT (composite==golden up-to-"
                   "phase, no MatrixGate): 4 analytic Ry modules + controlled-Ry apps (honest CNOT·Ry "
                   "ladder) + the QAE circuit qae3_pi8 (reusing sealed iqft3/cnot/h_gate/z_gate). The "
                   "amplitude-ESTIMATION readout (counting measurement -> a_est=sin^2(pi*y/2^t)) is an "
                   "OBSERVATION, NOT a seal: exact instance a=sin^2(pi/8), both peaks y in {1,7} recover "
                   "the true a exactly. modules 63->67, apps 91->94.",
        "modules": mods, "apps": apps, "estimation_observation": obs,
    }
    all_ok = (all(m["sealed"] and m.get("tier", 0) == 0 for m in mods)
              and all(a["sealed"] and a["tier"] == 0 for a in apps)
              and obs["exact_recovery"])
    report["all_ok"] = bool(all_ok)
    json.dump(report, open(os.path.join(OUT, "QAE-FAMILY-REPORT.json"), "w",
                           encoding="utf-8"), ensure_ascii=False, indent=2)
    print("-" * 86)
    print(f"all_ok={all_ok}  →  .pgf/arith/QAE-FAMILY-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
