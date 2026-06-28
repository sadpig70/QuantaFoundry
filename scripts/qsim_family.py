# -*- coding: utf-8 -*-
"""
qsim_family.py — Stage 8 W8.1 HamiltonianSimulation

새 *수평* 알고리즘 클래스: 해밀토니안 시뮬레이션(Trotter). 새 primitive 타입 = Pauli-exponential
회전(non-Clifford analytic). **정직-근사 showcase**: 1차 Trotter step은 EXACT 봉인, 전체 진화의
Trotter 오차는 *관찰*(seal 아님) — "approximation ≠ exact" 정직 경계(execution≠verification 의 자매).

봉인 대상(전부 Tier-0 EXACT, dt=π/8 인스턴스):
 1. rz_negpi4 (module) = Rz(-π/4) = e^{i(π/8)Z}      analytic golden diag(e^{iπ/8},e^{-iπ/8}).
 2. rx_negpi4 (module) = Rx(-π/4) = e^{i(π/8)X}      analytic golden cos·I + i sin·X.
 3. rzz_pi8 (app)       = e^{i(π/8)Z⊗Z} = CNOT·rz_negpi4·CNOT (2q).
 4. tfim3_trotter_step (app) = TFIM n=3 (J=h=1) 1차 Trotter step (3q):
      plan = rzz(0,1)·rzz(1,2)·rx(0)·rx(1)·rx(2). golden=Trotter곱(EXACT).

정직성 경계:
 - golden = closed-form Pauli-exponential(cos/sin 공식, Qualtran 비의존 독립경로). composite=Rz/Rx/CNOT
   bloq 조립. 둘 일치 → honest 분해(MatrixGate 0).
 - 봉인되는 것은 *Trotter step*(=정확히 그 지수곱). 진짜 e^{-iHdt} 와의 **Trotter 오차는 관찰(seal 아님)**:
   ||U_trot - exact||₂ + O(dt²) 스케일링(dt 반감 시 오차 ¼). 근사 정직 표기.
 - compose(a,b)=b@a → plan순서 [s₁..sₖ]=sₖ@…@s₁. golden 동일순서 구성.
 - second_oracle INDEP 에 rz/rx 추가(dense 53→55 full coverage 유지). 비파괴: 모듈 59→61·앱 75→77.

사용:  python scripts/qsim_family.py
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

TH = np.pi / 8   # dt = π/8 인스턴스


# ── 모듈 spec (analytic 회전, golden=closed form) ───────────────────────────────
_RZ_SPEC = (
    "# rz_negpi4 — Rz(-π/4) = e^{i(π/8)Z}. Pauli-Z 지수 회전(해밀토니안 시뮬 primitive). analytic golden.\n"
    "```python id=bloq\n"
    "import numpy as np\n"
    "from qualtran.bloqs.basic_gates import Rz\n"
    "bloq = Rz(-np.pi/4)\n"
    "```\n"
    "```python id=golden\n"
    "import numpy as np\n"
    "golden = np.diag([np.exp(1j*np.pi/8), np.exp(-1j*np.pi/8)]).astype(complex)\n"
    "```\n"
    '```json id=meta\n'
    '{"id": "rz_negpi4", "n_sys": 1, "n_anc": 0}\n'
    "```\n")

_RX_SPEC = (
    "# rx_negpi4 — Rx(-π/4) = e^{i(π/8)X}. Pauli-X 지수 회전(TFIM 가로장 항). analytic golden.\n"
    "```python id=bloq\n"
    "import numpy as np\n"
    "from qualtran.bloqs.basic_gates import Rx\n"
    "bloq = Rx(-np.pi/4)\n"
    "```\n"
    "```python id=golden\n"
    "import numpy as np\n"
    "X = np.array([[0,1],[1,0]], complex)\n"
    "golden = (np.cos(np.pi/8)*np.eye(2) + 1j*np.sin(np.pi/8)*X).astype(complex)\n"
    "```\n"
    '```json id=meta\n'
    '{"id": "rx_negpi4", "n_sys": 1, "n_anc": 0}\n'
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


# ── 앱 spec ────────────────────────────────────────────────────────────────────
_RZZ_SPEC = (
    "# rzz_pi8 — e^{i(π/8)Z⊗Z} = CNOT·rz_negpi4·CNOT (해밀토니안 시뮬 2큐비트 ZZ 상호작용). "
    "plan=봉인 cnot·rz_negpi4, no MatrixGate. golden=closed-form Pauli 지수.\n"
    '```json id=app_meta\n'
    '{"id": "rzz_pi8", "n_sys": 2, "n_anc": 0}\n'
    "```\n"
    "```python id=app_golden\n"
    "import numpy as np\n"
    "Z = np.diag([1,-1]).astype(complex); ZZ = np.kron(Z, Z)\n"
    "golden = (np.cos(np.pi/8)*np.eye(4) + 1j*np.sin(np.pi/8)*ZZ).astype(complex)\n"
    "```\n"
    '```json id=plan\n'
    + json.dumps({"steps": [
        {"spec": "../modules/cnot.pg", "targets": [0, 1]},
        {"spec": "../modules/rz_negpi4.pg", "targets": [1]},
        {"spec": "../modules/cnot.pg", "targets": [0, 1]}]}) + "\n"
    "```\n")

_TFIM_SPEC = (
    "# tfim3_trotter_step — TFIM n=3 (H=-J ΣZZ - h ΣX, J=h=1) 1차 Trotter step, dt=π/8. "
    "plan=rzz(0,1)·rzz(1,2)·rx(0,1,2), 봉인 부품. golden=Trotter곱(EXACT 봉인). "
    "진짜 e^{-iHdt} 와의 Trotter 오차는 별도 관찰(seal 아님).\n"
    '```json id=app_meta\n'
    '{"id": "tfim3_trotter_step", "n_sys": 3, "n_anc": 0}\n'
    "```\n"
    "```python id=app_golden\n"
    "import numpy as np\n"
    "n=3; th=np.pi/8\n"
    "I2=np.eye(2,dtype=complex); Z=np.diag([1,-1]).astype(complex); X=np.array([[0,1],[1,0]],complex)\n"
    "def opn(ps):\n"
    "    m=np.array([[1]],dtype=complex)\n"
    "    for q in range(n): m=np.kron(m, ps.get(q,I2))\n"
    "    return m\n"
    "def ezz(i,j): M=opn({i:Z,j:Z}); return np.cos(th)*np.eye(8,dtype=complex)+1j*np.sin(th)*M\n"
    "def ex(i): M=opn({i:X}); return np.cos(th)*np.eye(8,dtype=complex)+1j*np.sin(th)*M\n"
    "golden=np.eye(8,dtype=complex)\n"
    "for U in [ezz(0,1),ezz(1,2),ex(0),ex(1),ex(2)]: golden=U@golden\n"
    "```\n"
    '```json id=plan\n'
    + json.dumps({"steps": [
        {"app": "rzz_pi8.app.pg", "targets": [0, 1]},
        {"app": "rzz_pi8.app.pg", "targets": [1, 2]},
        {"spec": "../modules/rx_negpi4.pg", "targets": [0]},
        {"spec": "../modules/rx_negpi4.pg", "targets": [1]},
        {"spec": "../modules/rx_negpi4.pg", "targets": [2]}]}) + "\n"
    "```\n")


def _forge_app(name, spec):
    sp = os.path.join(SPECS_APPS, f"{name}.app.pg")
    open(sp, "w", encoding="utf-8", newline="\n").write(spec)
    v = aa.assemble(sp, APPREG)
    return {"id": name, "n_sys": v.n_sys, "sealed": bool(v.sealed), "tier": v.tier,
            "u_hash": v.u_hash, "reason": v.reason}


# ── 정직-근사 관찰 (seal 아님): Trotter step vs exact e^{-iH dt} ────────────────
def _trotter_error_observation():
    n = 3
    I2 = np.eye(2, dtype=complex); Z = np.diag([1, -1]).astype(complex); X = np.array([[0, 1], [1, 0]], complex)

    def opn(ps):
        m = np.array([[1]], dtype=complex)
        for q in range(n):
            m = np.kron(m, ps.get(q, I2))
        return m

    H = -(opn({0: Z, 1: Z}) + opn({1: Z, 2: Z})) - (opn({0: X}) + opn({1: X}) + opn({2: X}))
    w, V = np.linalg.eigh(H)

    def ezz(i, j, d): M = opn({i: Z, j: Z}); return np.cos(d) * np.eye(8, dtype=complex) + 1j * np.sin(d) * M
    def ex(i, d): M = opn({i: X}); return np.cos(d) * np.eye(8, dtype=complex) + 1j * np.sin(d) * M

    def step(d):
        U = np.eye(8, dtype=complex)
        for M in [ezz(0, 1, d), ezz(1, 2, d), ex(0, d), ex(1, d), ex(2, d)]:
            U = M @ U
        return U

    scaling = []
    for d in (np.pi / 8, np.pi / 16, np.pi / 32):
        exact = V @ np.diag(np.exp(-1j * w * d)) @ V.conj().T
        err = float(np.linalg.norm(step(d) - exact, 2))
        scaling.append({"dt": float(d), "trotter_error_2norm": round(err, 6)})
    # O(dt^2): dt 반감 시 오차 ≈ ¼
    r1 = scaling[0]["trotter_error_2norm"] / scaling[1]["trotter_error_2norm"]
    r2 = scaling[1]["trotter_error_2norm"] / scaling[2]["trotter_error_2norm"]
    second_order = 3.0 < r1 < 5.0 and 3.0 < r2 < 5.0
    return {"note": "OBSERVATION, NOT A SEAL — Trotter step is sealed EXACTLY; this is its "
                    "approximation error vs the true e^{-iH dt}.",
            "scaling": scaling, "ratio_dt_halving": [round(r1, 3), round(r2, 3)],
            "O(dt^2)_confirmed": bool(second_order)}


def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 82)
    print("W8.1 HamiltonianSimulation — Trotter(새 수평 클래스). Pauli-exp 회전 + 정직-근사 showcase.")
    print("=" * 82)

    mods = [_seal_module("rz_negpi4", _RZ_SPEC), _seal_module("rx_negpi4", _RX_SPEC)]
    for m in mods:
        print(f"[Module] {m['id']:12} n_sys={m.get('n_sys')} sealed={m['sealed']} tier={m.get('tier')} "
              f"u={str(m.get('u_hash'))[:14]}")
    apps = [_forge_app("rzz_pi8", _RZZ_SPEC), _forge_app("tfim3_trotter_step", _TFIM_SPEC)]
    for a in apps:
        print(f"[App]    {a['id']:20} n_sys={a.get('n_sys')} sealed={a['sealed']} tier={a.get('tier')} "
              f"u={str(a.get('u_hash'))[:14]}" + ("" if a["sealed"] else f"  reason={a['reason']}"))

    obs = _trotter_error_observation()
    print(f"[Honest-Approx] Trotter 오차(seal 아님): " +
          " · ".join(f"dt={s['dt']:.4f}→{s['trotter_error_2norm']}" for s in obs["scaling"]))
    print(f"                O(dt²) 스케일링(dt 반감→오차 ¼) ratios={obs['ratio_dt_halving']} "
          f"confirmed={obs['O(dt^2)_confirmed']}")

    report = {
        "phase": "W8.1 HamiltonianSimulation",
        "honesty": "New horizontal class: Trotterized Hamiltonian simulation. New primitive type = "
                   "Pauli-exponential rotations (Rz/Rx, non-Clifford analytic). golden = closed-form "
                   "Pauli exponentials (cos/sin, Qualtran-independent); composite = Rz/Rx/CNOT bloqs "
                   "(honest decomposition, no MatrixGate). The Trotter STEP is sealed EXACTLY "
                   "(composite==golden). The Trotter ERROR vs the true e^{-iH dt} is an OBSERVATION, "
                   "NOT a seal — the 'approximation != exact' boundary (sister of 'execution != "
                   "verification'); O(dt^2) scaling confirmed. modules 59->61, apps 75->77.",
        "modules": mods, "apps": apps, "trotter_error_observation": obs,
    }
    all_ok = (all(m["sealed"] and m.get("tier", 0) == 0 for m in mods)
              and all(a["sealed"] and a["tier"] == 0 for a in apps)
              and obs["O(dt^2)_confirmed"])
    report["all_ok"] = bool(all_ok)
    json.dump(report, open(os.path.join(OUT, "QSIM-FAMILY-REPORT.json"), "w",
                           encoding="utf-8"), ensure_ascii=False, indent=2)
    print("-" * 82)
    print(f"all_ok={all_ok}  →  .pgf/arith/QSIM-FAMILY-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
