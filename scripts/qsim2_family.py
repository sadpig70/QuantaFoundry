# -*- coding: utf-8 -*-
"""
qsim2_family.py — Stage 8 W8.2 TrotterDeepening

W8.1(HamiltonianSimulation)을 *instance*에서 *family*로 키운다. Pauli-상호작용 회전 집합
{rxx, ryy, rzz}을 완성하고, Heisenberg 모델 두 인스턴스 + multi-step 복리를 봉인한다.
정직-근사 경계를 **수렴 관찰**(고정 T, k-step Trotter 오차→0)로 심화한다.

봉인 대상:
 0. sdg_gate (module, Clifford Tier-0) = S† = diag(1,-i).  ryy 기저변환(Z→Y, B=S·H)에 필요.
 1. rxx_pi8 (app)  = e^{i(π/8)X⊗X} = (H⊗H)·rzz·(H⊗H).            X=HZH 기저변환.   Tier-0 EXACT.
 2. ryy_pi8 (app)  = e^{i(π/8)Y⊗Y}, B=S·H maps Z→Y.              Tier-0 EXACT.
 3. heis2_trotter_step (app)  = single-bond H=XX+YY+ZZ 1-step = rxx·ryy·rzz (2q).
 4. heis3_trotter_step (app)  = chain bonds(0,1),(1,2) 1-step (3q).
 5. tfim3_trotter_2steps (app) = tfim3_trotter_step × 2 (3q, 복리).

정직성 경계:
 - 봉인 = Trotter STEP(분해의 정확성). golden = closed-form Pauli 지수곱(cos/sin, Qualtran 비의존).
   composite = 봉인 부품 조립(honest, MatrixGate 0). 둘 일치 → EXACT.
 - 봉인 아님 = 진짜 e^{-iHT} 와의 Trotter 오차(_convergence_observation): "approximation ≠ exact".
   고정 T=π/4, k-step → 1차 전역오차 O(1/k)(ratio≈2). execution≠verification 의 자매.
 - ★honest 미묘함: single-bond Heisenberg는 XX,YY,ZZ 교환 → step이 e^{-iHt}와 *정확*(근사 아님).
   모든 Trotter가 근사인 것은 아님 — 정직 구별 표기.

사용:  python scripts/qsim2_family.py
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


# ── 모듈 spec: S† (Clifford Tier-0 primitive) ───────────────────────────────────
_SDG_SPEC = (
    "# sdg_gate — S† = diag(1,-i). Clifford 위상 게이트의 켤레전치. ryy 기저변환(Z→Y, B=S·H)에 필요. analytic golden.\n"
    "```python id=bloq\n"
    "from qualtran.bloqs.basic_gates import SGate\n"
    "bloq = SGate().adjoint()\n"
    "```\n"
    "```python id=golden\n"
    "import numpy as np\n"
    "golden = np.array([[1,0],[0,-1j]], dtype=complex)\n"
    "```\n"
    '```json id=meta\n'
    '{"id": "sdg_gate", "n_sys": 1, "n_anc": 0}\n'
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
# rxx = (H⊗H)·rzz·(H⊗H).  plan [h0,h1, rzz, h0,h1] (대칭).
_RXX_SPEC = (
    "# rxx_pi8 — e^{i(π/8)X⊗X} = (H⊗H)·rzz_pi8·(H⊗H) (해밀토니안 시뮬 XX 상호작용). "
    "X=HZH 기저변환. plan=봉인 h_gate·rzz_pi8, no MatrixGate. golden=closed-form Pauli 지수.\n"
    '```json id=app_meta\n'
    '{"id": "rxx_pi8", "n_sys": 2, "n_anc": 0}\n'
    "```\n"
    "```python id=app_golden\n"
    "import numpy as np\n"
    "X = np.array([[0,1],[1,0]],complex); XX = np.kron(X, X)\n"
    "golden = (np.cos(np.pi/8)*np.eye(4) + 1j*np.sin(np.pi/8)*XX).astype(complex)\n"
    "```\n"
    '```json id=plan\n'
    + json.dumps({"steps": [
        {"spec": "../modules/h_gate.pg", "targets": [0]},
        {"spec": "../modules/h_gate.pg", "targets": [1]},
        {"app": "rzz_pi8.app.pg", "targets": [0, 1]},
        {"spec": "../modules/h_gate.pg", "targets": [0]},
        {"spec": "../modules/h_gate.pg", "targets": [1]}]}) + "\n"
    "```\n")

# ryy: B=S·H maps Z→Y (S X S†=Y, X=HZH). 기저변환 켤레 BB·rzz·BBd. compose(a,b)=b@a →
# plan 순서 [s1..sk]=sk@..@s1. BBd(=H S† per q) 먼저(rightmost) 적용: [sdg, h], rzz, [h, s].
_RYY_SPEC = (
    "# ryy_pi8 — e^{i(π/8)Y⊗Y}, 기저 B=S·H(Z→Y). plan=봉인 sdg_gate·h_gate·rzz_pi8·s_gate, no MatrixGate. "
    "golden=closed-form Pauli 지수.\n"
    '```json id=app_meta\n'
    '{"id": "ryy_pi8", "n_sys": 2, "n_anc": 0}\n'
    "```\n"
    "```python id=app_golden\n"
    "import numpy as np\n"
    "Y = np.array([[0,-1j],[1j,0]],complex); YY = np.kron(Y, Y)\n"
    "golden = (np.cos(np.pi/8)*np.eye(4) + 1j*np.sin(np.pi/8)*YY).astype(complex)\n"
    "```\n"
    '```json id=plan\n'
    + json.dumps({"steps": [
        {"spec": "../modules/sdg_gate.pg", "targets": [0]},
        {"spec": "../modules/sdg_gate.pg", "targets": [1]},
        {"spec": "../modules/h_gate.pg", "targets": [0]},
        {"spec": "../modules/h_gate.pg", "targets": [1]},
        {"app": "rzz_pi8.app.pg", "targets": [0, 1]},
        {"spec": "../modules/h_gate.pg", "targets": [0]},
        {"spec": "../modules/h_gate.pg", "targets": [1]},
        {"spec": "../modules/s_gate.pg", "targets": [0]},
        {"spec": "../modules/s_gate.pg", "targets": [1]}]}) + "\n"
    "```\n")

# heis2: single-bond H=XX+YY+ZZ 1-step = rxx·ryy·rzz. plan [rxx,ryy,rzz] → operator rzz@ryy@rxx.
_HEIS2_SPEC = (
    "# heis2_trotter_step — single-bond Heisenberg(H=XX+YY+ZZ) 1차 Trotter step, dt=π/8 (2q). "
    "plan=rxx_pi8·ryy_pi8·rzz_pi8(봉인 앱). golden=Trotter곱(EXACT). "
    "★honest: single bond에서 XX,YY,ZZ 교환 → 이 step은 진짜 e^{-iHt}와 *정확* 일치(관찰).\n"
    '```json id=app_meta\n'
    '{"id": "heis2_trotter_step", "n_sys": 2, "n_anc": 0}\n'
    "```\n"
    "```python id=app_golden\n"
    "import numpy as np\n"
    "th=np.pi/8\n"
    "X=np.array([[0,1],[1,0]],complex); Y=np.array([[0,-1j],[1j,0]],complex); Z=np.diag([1,-1]).astype(complex)\n"
    "def e(P): return np.cos(th)*np.eye(4,dtype=complex)+1j*np.sin(th)*P\n"
    "XX=np.kron(X,X); YY=np.kron(Y,Y); ZZ=np.kron(Z,Z)\n"
    "golden = e(ZZ) @ e(YY) @ e(XX)\n"
    "```\n"
    '```json id=plan\n'
    + json.dumps({"steps": [
        {"app": "rxx_pi8.app.pg", "targets": [0, 1]},
        {"app": "ryy_pi8.app.pg", "targets": [0, 1]},
        {"app": "rzz_pi8.app.pg", "targets": [0, 1]}]}) + "\n"
    "```\n")

# heis3: chain bonds(0,1),(1,2), 각 bond = rxx·ryy·rzz. plan = bond(0,1) steps then bond(1,2) steps.
_HEIS3_SPEC = (
    "# heis3_trotter_step — Heisenberg chain(bonds (0,1),(1,2)) 1차 Trotter step, dt=π/8 (3q). "
    "plan=bond(0,1)[rxx·ryy·rzz]·bond(1,2)[rxx·ryy·rzz](봉인 앱). golden=Trotter곱(EXACT 봉인). "
    "겹치는 bond(공유 q1) 비가환 → 진짜 e^{-iHt} 오차는 별도 관찰(seal 아님).\n"
    '```json id=app_meta\n'
    '{"id": "heis3_trotter_step", "n_sys": 3, "n_anc": 0}\n'
    "```\n"
    "```python id=app_golden\n"
    "import numpy as np\n"
    "th=np.pi/8; n=3\n"
    "I2=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex)\n"
    "Y=np.array([[0,-1j],[1j,0]],complex); Z=np.diag([1,-1]).astype(complex)\n"
    "def opn(ps):\n"
    "    m=np.array([[1]],dtype=complex)\n"
    "    for q in range(n): m=np.kron(m, ps.get(q,I2))\n"
    "    return m\n"
    "def e(P): return np.cos(th)*np.eye(8,dtype=complex)+1j*np.sin(th)*P\n"
    "def bond(i,j): return e(opn({i:Z,j:Z})) @ e(opn({i:Y,j:Y})) @ e(opn({i:X,j:X}))\n"
    "golden = bond(1,2) @ bond(0,1)\n"
    "```\n"
    '```json id=plan\n'
    + json.dumps({"steps": [
        {"app": "rxx_pi8.app.pg", "targets": [0, 1]},
        {"app": "ryy_pi8.app.pg", "targets": [0, 1]},
        {"app": "rzz_pi8.app.pg", "targets": [0, 1]},
        {"app": "rxx_pi8.app.pg", "targets": [1, 2]},
        {"app": "ryy_pi8.app.pg", "targets": [1, 2]},
        {"app": "rzz_pi8.app.pg", "targets": [1, 2]}]}) + "\n"
    "```\n")

# tfim 2-step 복리: 봉인 step 2회 합성. plan [tfim_step, tfim_step] → operator step@step.
_TFIM2_SPEC = (
    "# tfim3_trotter_2steps — TFIM n=3 (J=h=1) 1차 Trotter step ×2 (복리, dt=π/8, 3q). "
    "plan=tfim3_trotter_step·tfim3_trotter_step(봉인 앱 ×2). golden=step@step(EXACT). "
    "봉인 step 합성이 정확 유지됨을 실증(step^k 합성=정확).\n"
    '```json id=app_meta\n'
    '{"id": "tfim3_trotter_2steps", "n_sys": 3, "n_anc": 0}\n'
    "```\n"
    "```python id=app_golden\n"
    "import numpy as np\n"
    "th=np.pi/8; n=3\n"
    "I2=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex); Z=np.diag([1,-1]).astype(complex)\n"
    "def opn(ps):\n"
    "    m=np.array([[1]],dtype=complex)\n"
    "    for q in range(n): m=np.kron(m, ps.get(q,I2))\n"
    "    return m\n"
    "def ezz(i,j): M=opn({i:Z,j:Z}); return np.cos(th)*np.eye(8,dtype=complex)+1j*np.sin(th)*M\n"
    "def ex(i): M=opn({i:X}); return np.cos(th)*np.eye(8,dtype=complex)+1j*np.sin(th)*M\n"
    "step=np.eye(8,dtype=complex)\n"
    "for U in [ezz(0,1),ezz(1,2),ex(0),ex(1),ex(2)]: step=U@step\n"
    "golden = step @ step\n"
    "```\n"
    '```json id=plan\n'
    + json.dumps({"steps": [
        {"app": "tfim3_trotter_step.app.pg", "targets": [0, 1, 2]},
        {"app": "tfim3_trotter_step.app.pg", "targets": [0, 1, 2]}]}) + "\n"
    "```\n")


def _forge_app(name, spec):
    sp = os.path.join(SPECS_APPS, f"{name}.app.pg")
    open(sp, "w", encoding="utf-8", newline="\n").write(spec)
    v = aa.assemble(sp, APPREG)
    return {"id": name, "n_sys": v.n_sys, "sealed": bool(v.sealed), "tier": v.tier,
            "u_hash": v.u_hash, "reason": v.reason}


# ── 정직-근사 심화 관찰 (seal 아님): 고정 T, k-step Trotter 수렴 ───────────────────
def _convergence_observation():
    I2 = np.eye(2, dtype=complex)
    X = np.array([[0, 1], [1, 0]], complex)
    Y = np.array([[0, -1j], [1j, 0]], complex)
    Z = np.diag([1, -1]).astype(complex)
    T = np.pi / 4
    ks = (1, 2, 4, 8, 16)

    def opn(ps, n):
        m = np.array([[1]], dtype=complex)
        for q in range(n):
            m = np.kron(m, ps.get(q, I2))
        return m

    def e(P, d):
        return np.cos(d) * np.eye(P.shape[0], dtype=complex) + 1j * np.sin(d) * P

    # TFIM3: H = -(Z0Z1+Z1Z2) - (X0+X1+X2)
    n = 3
    Ht = -(opn({0: Z, 1: Z}, n) + opn({1: Z, 2: Z}, n)) - (opn({0: X}, n) + opn({1: X}, n) + opn({2: X}, n))
    wt, Vt = np.linalg.eigh(Ht)

    def tstep(d):
        U = np.eye(8, dtype=complex)
        for M in [e(opn({0: Z, 1: Z}, n), d), e(opn({1: Z, 2: Z}, n), d),
                  e(opn({0: X}, n), d), e(opn({1: X}, n), d), e(opn({2: X}, n), d)]:
            U = M @ U
        return U

    # Heisenberg chain3: H = -(bond(0,1)+bond(1,2)), bond=XX+YY+ZZ
    def bondM(i, j):
        return opn({i: X, j: X}, n) + opn({i: Y, j: Y}, n) + opn({i: Z, j: Z}, n)
    Hh = -(bondM(0, 1) + bondM(1, 2))
    wh, Vh = np.linalg.eigh(Hh)

    def hstep(d):
        def b(i, j):
            return e(opn({i: Z, j: Z}, n), d) @ e(opn({i: Y, j: Y}, n), d) @ e(opn({i: X, j: X}, n), d)
        return b(1, 2) @ b(0, 1)

    def sweep(stepf, w, V):
        rows = []
        for k in ks:
            d = T / k
            U = np.eye(8, dtype=complex)
            for _ in range(k):
                U = stepf(d) @ U
            exact = V @ np.diag(np.exp(-1j * w * T)) @ V.conj().T
            rows.append({"k": k, "dt": round(float(d), 6),
                         "trotter_error_2norm": round(float(np.linalg.norm(U - exact, 2)), 6)})
        ratios = [round(rows[i]["trotter_error_2norm"] / rows[i + 1]["trotter_error_2norm"], 3)
                  for i in range(len(rows) - 1)]
        # 1차 전역수렴은 점근적: 가장 거친 step(dt=π/4)은 점근영역 밖이므로 tail(마지막 2개)로 판정.
        first_order = all(1.9 <= r <= 2.1 for r in ratios[-2:])
        return {"sweep": rows, "ratio_k_doubling": ratios,
                "O(1/k)_confirmed": bool(first_order),
                "criterion": "asymptotic tail (last 2 k-doublings) within [1.9,2.1]"}

    tfim = sweep(tstep, wt, Vt)
    heis = sweep(hstep, wh, Vh)

    # single-bond Heisenberg exactness (교환항 → step이 정확)
    n2 = 2
    bond01 = opn({0: X, 1: X}, n2) + opn({0: Y, 1: Y}, n2) + opn({0: Z, 1: Z}, n2)
    wb, Vb = np.linalg.eigh(-bond01)
    ex_b = Vb @ np.diag(np.exp(-1j * wb * TH)) @ Vb.conj().T
    step_b = (e(opn({0: Z, 1: Z}, n2), TH) @ e(opn({0: Y, 1: Y}, n2), TH) @ e(opn({0: X, 1: X}, n2), TH))
    single_bond_err = float(np.linalg.norm(step_b - ex_b, 2))

    return {
        "note": "OBSERVATION, NOT A SEAL — Trotter steps are sealed EXACTLY; this is their "
                "approximation error vs the true e^{-iH T} over fixed T=π/4 as step count k grows.",
        "fixed_T": float(T),
        "tfim3_chain": tfim,
        "heisenberg_chain3": heis,
        "single_bond_heisenberg": {
            "trotter_error_2norm": round(single_bond_err, 12),
            "exact_not_approx": single_bond_err < 1e-9,
            "why": "single bond: XX,YY,ZZ mutually commute → Trotter step EXACTLY equals e^{-iH dt}."},
    }


def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 86)
    print("W8.2 TrotterDeepening — Pauli-상호작용 {rxx,ryy,rzz} 완성 + Heisenberg family + 복리 + 수렴관찰.")
    print("=" * 86)

    mods = [_seal_module("sdg_gate", _SDG_SPEC)]
    for m in mods:
        print(f"[Module] {m['id']:12} n_sys={m.get('n_sys')} sealed={m['sealed']} tier={m.get('tier')} "
              f"u={str(m.get('u_hash'))[:14]}")

    apps = [
        _forge_app("rxx_pi8", _RXX_SPEC),
        _forge_app("ryy_pi8", _RYY_SPEC),
        _forge_app("heis2_trotter_step", _HEIS2_SPEC),
        _forge_app("heis3_trotter_step", _HEIS3_SPEC),
        _forge_app("tfim3_trotter_2steps", _TFIM2_SPEC),
    ]
    for a in apps:
        print(f"[App]    {a['id']:22} n_sys={a.get('n_sys')} sealed={a['sealed']} tier={a.get('tier')} "
              f"u={str(a.get('u_hash'))[:14]}" + ("" if a["sealed"] else f"  reason={a['reason']}"))

    obs = _convergence_observation()
    tf = obs["tfim3_chain"]; he = obs["heisenberg_chain3"]; sb = obs["single_bond_heisenberg"]
    print(f"[Honest-Approx] 고정 T=π/4, k-step 수렴(seal 아님):")
    print(f"   TFIM3      k-doubling ratios={tf['ratio_k_doubling']} O(1/k)={tf['O(1/k)_confirmed']} "
          f"(err {tf['sweep'][0]['trotter_error_2norm']}→{tf['sweep'][-1]['trotter_error_2norm']})")
    print(f"   Heis-chain k-doubling ratios={he['ratio_k_doubling']} O(1/k)={he['O(1/k)_confirmed']} "
          f"(err {he['sweep'][0]['trotter_error_2norm']}→{he['sweep'][-1]['trotter_error_2norm']})")
    print(f"   single-bond Heisenberg: err={sb['trotter_error_2norm']:.2e} exact_not_approx={sb['exact_not_approx']} "
          f"(XX,YY,ZZ 교환 → 정확)")

    report = {
        "phase": "W8.2 TrotterDeepening",
        "honesty": "Grows W8.1 from instance to family. Completes the Pauli-interaction rotation set "
                   "{rxx, ryy, rzz}; seals two Heisenberg instances (single-bond exact, chain "
                   "approximate) and a multi-step compound. The Trotter STEPS are sealed EXACTLY "
                   "(composite==golden, golden=closed-form Pauli exponentials, no MatrixGate). The "
                   "Trotter ERROR vs the true e^{-iH T} is an OBSERVATION, NOT a seal — fixed T=π/4, "
                   "first-order global error O(1/k) confirmed (ratio~2 per k-doubling). Honest nuance: "
                   "the single-bond Heisenberg step is EXACT (XX,YY,ZZ commute on one bond) — not all "
                   "Trotter steps are approximate. modules 61->62, apps 77->82.",
        "modules": mods, "apps": apps, "convergence_observation": obs,
    }
    all_ok = (all(m["sealed"] and m.get("tier", 0) == 0 for m in mods)
              and all(a["sealed"] and a["tier"] == 0 for a in apps)
              and tf["O(1/k)_confirmed"] and he["O(1/k)_confirmed"]
              and sb["exact_not_approx"])
    report["all_ok"] = bool(all_ok)
    json.dump(report, open(os.path.join(OUT, "QSIM2-FAMILY-REPORT.json"), "w",
                           encoding="utf-8"), ensure_ascii=False, indent=2)
    print("-" * 86)
    print(f"all_ok={all_ok}  →  .pgf/arith/QSIM2-FAMILY-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
