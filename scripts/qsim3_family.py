# -*- coding: utf-8 -*-
"""
qsim3_family.py — Stage 8 W8.3 SuzukiTrotter

W8.1/W8.2(1차 Trotter)에 **2차 Suzuki-Trotter(대칭 분할)**를 추가하고 격자를 4큐비트로 확장한다.
정직-근사 경계를 **근사 *차수* 대비**로 심화: 1차 O(1/k) vs 2차 O(1/k²)(고정 T, ratio 2 vs 4).

봉인 대상(전부 Tier-0 EXACT, dt=π/8):
 0. rz_negpi8 (module) = Rz(-π/8) = e^{i(π/16)Z}.  반각 ZZ(rzz_pi16)에 필요.
 1. rzz_pi16 (app)            = e^{i(π/16)Z⊗Z} = CNOT·rz_negpi8·CNOT (2q 반각 ZZ).
 2. tfim3_trotter_step2 (app) = TFIM3 2차 Suzuki step (3q): ΠZZ(d/2)·ΠX(d)·ΠZZ(d/2).
 3. tfim4_trotter_step (app)  = TFIM4 1차 step (4q, 격자 확장).
 4. tfim4_trotter_step2 (app) = TFIM4 2차 Suzuki step (4q).

정직성 경계:
 - 봉인 = Trotter STEP(1차·2차 둘 다 분해의 정확성). golden = closed-form Pauli 지수곱(Qualtran 비의존),
   composite = 봉인 부품(honest, MatrixGate 0). 둘 일치 → EXACT.
 - 봉인 아님 = 진짜 e^{-iHT} 와의 오차 + 그 *수렴 차수*(_order_contrast_observation):
   1차 ratio≈2(O(1/k), per-step O(dt²)) vs 2차 ratio≈4(O(1/k²), per-step O(dt³)). 고정 T=π/4.
   W8.2가 "근사는 수렴"을 보였다면, W8.3은 "근사의 *품질(차수)* 도 정량화"를 보인다.

사용:  python scripts/qsim3_family.py
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


# ── 모듈 spec: 반각 Z 회전 ───────────────────────────────────────────────────────
_RZ8_SPEC = (
    "# rz_negpi8 — Rz(-π/8) = e^{i(π/16)Z}. 반각 Pauli-Z 회전(2차 Suzuki step의 반각 ZZ에 필요). analytic golden.\n"
    "```python id=bloq\n"
    "import numpy as np\n"
    "from qualtran.bloqs.basic_gates import Rz\n"
    "bloq = Rz(-np.pi/8)\n"
    "```\n"
    "```python id=golden\n"
    "import numpy as np\n"
    "golden = np.diag([np.exp(1j*np.pi/16), np.exp(-1j*np.pi/16)]).astype(complex)\n"
    "```\n"
    '```json id=meta\n'
    '{"id": "rz_negpi8", "n_sys": 1, "n_anc": 0}\n'
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
_RZZ16_SPEC = (
    "# rzz_pi16 — e^{i(π/16)Z⊗Z} = CNOT·rz_negpi8·CNOT (반각 2큐비트 ZZ, 2차 Suzuki용). "
    "plan=봉인 cnot·rz_negpi8, no MatrixGate. golden=closed-form Pauli 지수.\n"
    '```json id=app_meta\n'
    '{"id": "rzz_pi16", "n_sys": 2, "n_anc": 0}\n'
    "```\n"
    "```python id=app_golden\n"
    "import numpy as np\n"
    "Z = np.diag([1,-1]).astype(complex); ZZ = np.kron(Z, Z)\n"
    "golden = (np.cos(np.pi/16)*np.eye(4) + 1j*np.sin(np.pi/16)*ZZ).astype(complex)\n"
    "```\n"
    '```json id=plan\n'
    + json.dumps({"steps": [
        {"spec": "../modules/cnot.pg", "targets": [0, 1]},
        {"spec": "../modules/rz_negpi8.pg", "targets": [1]},
        {"spec": "../modules/cnot.pg", "targets": [0, 1]}]}) + "\n"
    "```\n")


def _tfim_golden_code(n, order):
    """closed-form TFIM Trotter step golden (1차 또는 2차 Suzuki), dt=π/8."""
    bonds = [(i, i + 1) for i in range(n - 1)]
    sites = list(range(n))
    lines = [
        "import numpy as np",
        f"n={n}; th=np.pi/8; dim=1<<n",
        "I2=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex); Z=np.diag([1,-1]).astype(complex)",
        "def opn(ps):",
        "    m=np.array([[1]],dtype=complex)",
        "    for q in range(n): m=np.kron(m, ps.get(q,I2))",
        "    return m",
        "def e(P,d): return np.cos(d)*np.eye(dim,dtype=complex)+1j*np.sin(d)*P",
        "golden=np.eye(dim,dtype=complex)",
    ]
    if order == 1:
        for (i, j) in bonds:
            lines.append(f"golden=e(opn({{{i}:Z,{j}:Z}}),th)@golden")
        for i in sites:
            lines.append(f"golden=e(opn({{{i}:X}}),th)@golden")
    else:  # 2차 Strang: ΠZZ(d/2)·ΠX(d)·ΠZZ(d/2)
        for (i, j) in bonds:
            lines.append(f"golden=e(opn({{{i}:Z,{j}:Z}}),th/2)@golden")
        for i in sites:
            lines.append(f"golden=e(opn({{{i}:X}}),th)@golden")
        for (i, j) in bonds:
            lines.append(f"golden=e(opn({{{i}:Z,{j}:Z}}),th/2)@golden")
    return "\n".join(lines) + "\n"


def _tfim_plan(n, order):
    bonds = [(i, i + 1) for i in range(n - 1)]
    sites = list(range(n))
    rzz_full = "rzz_pi8.app.pg"
    rzz_half = "rzz_pi16.app.pg"
    steps = []
    if order == 1:
        for (i, j) in bonds:
            steps.append({"app": rzz_full, "targets": [i, j]})
        for i in sites:
            steps.append({"spec": "../modules/rx_negpi4.pg", "targets": [i]})
    else:
        for (i, j) in bonds:
            steps.append({"app": rzz_half, "targets": [i, j]})
        for i in sites:
            steps.append({"spec": "../modules/rx_negpi4.pg", "targets": [i]})
        for (i, j) in bonds:
            steps.append({"app": rzz_half, "targets": [i, j]})
    return json.dumps({"steps": steps})


def _tfim_spec(name, n, order, desc):
    return (
        f"# {name} — {desc}\n"
        '```json id=app_meta\n'
        + json.dumps({"id": name, "n_sys": n, "n_anc": 0}) + "\n"
        "```\n"
        "```python id=app_golden\n"
        + _tfim_golden_code(n, order)
        + "```\n"
        '```json id=plan\n'
        + _tfim_plan(n, order) + "\n"
        "```\n")


def _forge_app(name, spec):
    sp = os.path.join(SPECS_APPS, f"{name}.app.pg")
    open(sp, "w", encoding="utf-8", newline="\n").write(spec)
    v = aa.assemble(sp, APPREG)
    return {"id": name, "n_sys": v.n_sys, "sealed": bool(v.sealed), "tier": v.tier,
            "u_hash": v.u_hash, "reason": v.reason}


# ── 정직-근사 심화 관찰 (seal 아님): 1차 vs 2차 수렴 차수 대비 ────────────────────
def _order_contrast_observation():
    I2 = np.eye(2, dtype=complex)
    X = np.array([[0, 1], [1, 0]], complex)
    Z = np.diag([1, -1]).astype(complex)
    T = np.pi / 4
    ks = (1, 2, 4, 8, 16)

    def make(n):
        def opn(ps):
            m = np.array([[1]], dtype=complex)
            for q in range(n):
                m = np.kron(m, ps.get(q, I2))
            return m
        bonds = [(i, i + 1) for i in range(n - 1)]
        sites = list(range(n))
        dim = 1 << n
        H = -(sum(opn({i: Z, j: Z}) for i, j in bonds) + sum(opn({i: X}) for i in sites))
        w, V = np.linalg.eigh(H)

        def e(P, d):
            return np.cos(d) * np.eye(dim, dtype=complex) + 1j * np.sin(d) * P

        def s1(d):
            U = np.eye(dim, dtype=complex)
            for (i, j) in bonds:
                U = e(opn({i: Z, j: Z}), d) @ U
            for i in sites:
                U = e(opn({i: X}), d) @ U
            return U

        def s2(d):
            U = np.eye(dim, dtype=complex)
            for (i, j) in bonds:
                U = e(opn({i: Z, j: Z}), d / 2) @ U
            for i in sites:
                U = e(opn({i: X}), d) @ U
            for (i, j) in bonds:
                U = e(opn({i: Z, j: Z}), d / 2) @ U
            return U

        def exact(t):
            return V @ np.diag(np.exp(-1j * w * t)) @ V.conj().T
        return exact, s1, s2, dim

    def sweep(exact, stepf, dim):
        rows = []
        for k in ks:
            d = T / k
            U = np.eye(dim, dtype=complex)
            for _ in range(k):
                U = stepf(d) @ U
            rows.append({"k": k, "dt": round(float(d), 6),
                         "error_2norm": round(float(np.linalg.norm(U - exact(T), 2)), 8)})
        ratios = [round(rows[i]["error_2norm"] / rows[i + 1]["error_2norm"], 3)
                  for i in range(len(rows) - 1)]
        return rows, ratios

    out = {"note": "OBSERVATION, NOT A SEAL — both Trotter steps are sealed EXACTLY; this contrasts "
                   "their approximation-error convergence ORDER vs the true e^{-iH T} at fixed T=π/4. "
                   "1st-order ratio~2 (O(1/k)); 2nd-order Suzuki ratio~4 (O(1/k^2)).",
           "fixed_T": float(T), "systems": {}}
    ok = True
    for n in (3, 4):
        exact, s1, s2, dim = make(n)
        r1, ra1 = sweep(exact, s1, dim)
        r2, ra2 = sweep(exact, s2, dim)
        first_ok = all(1.9 <= r <= 2.1 for r in ra1[-2:])
        second_ok = all(3.8 <= r <= 4.2 for r in ra2[-2:])
        ok = ok and first_ok and second_ok
        out["systems"][f"tfim{n}"] = {
            "first_order": {"sweep": r1, "ratio_k_doubling": ra1, "O(1/k)_confirmed": bool(first_ok)},
            "second_order": {"sweep": r2, "ratio_k_doubling": ra2, "O(1/k^2)_confirmed": bool(second_ok)}}
    out["all_orders_confirmed"] = bool(ok)
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 88)
    print("W8.3 SuzukiTrotter — 2차 대칭 분할 + 4큐비트 격자 + 근사 *차수* 대비(1차 O(1/k) vs 2차 O(1/k²)).")
    print("=" * 88)

    mods = [_seal_module("rz_negpi8", _RZ8_SPEC)]
    for m in mods:
        print(f"[Module] {m['id']:12} n_sys={m.get('n_sys')} sealed={m['sealed']} tier={m.get('tier')} "
              f"u={str(m.get('u_hash'))[:14]}")

    apps = [
        _forge_app("rzz_pi16", _RZZ16_SPEC),
        _forge_app("tfim3_trotter_step2", _tfim_spec(
            "tfim3_trotter_step2", 3, 2,
            "TFIM n=3 (J=h=1) 2차 Suzuki Trotter step, dt=π/8 (3q). "
            "plan=ΠZZ_pi16(d/2)·ΠX(d)·ΠZZ_pi16(d/2)(봉인 부품). golden=대칭곱(EXACT). per-step 오차 O(dt³).")),
        _forge_app("tfim4_trotter_step", _tfim_spec(
            "tfim4_trotter_step", 4, 1,
            "TFIM n=4 (J=h=1) 1차 Trotter step, dt=π/8 (4q, 격자 확장). "
            "plan=rzz_pi8(bonds)·rx(sites)(봉인 부품). golden=Trotter곱(EXACT).")),
        _forge_app("tfim4_trotter_step2", _tfim_spec(
            "tfim4_trotter_step2", 4, 2,
            "TFIM n=4 (J=h=1) 2차 Suzuki Trotter step, dt=π/8 (4q). "
            "plan=ΠZZ_pi16(d/2)·ΠX(d)·ΠZZ_pi16(d/2)(봉인 부품). golden=대칭곱(EXACT).")),
    ]
    for a in apps:
        print(f"[App]    {a['id']:22} n_sys={a.get('n_sys')} sealed={a['sealed']} tier={a.get('tier')} "
              f"u={str(a.get('u_hash'))[:14]}" + ("" if a["sealed"] else f"  reason={a['reason']}"))

    obs = _order_contrast_observation()
    print(f"[Honest-Approx] 고정 T=π/4, 1차 vs 2차 수렴 차수 대비(seal 아님):")
    for nkey, sysd in obs["systems"].items():
        fo = sysd["first_order"]; so = sysd["second_order"]
        print(f"   {nkey}: 1차 ratios={fo['ratio_k_doubling']} O(1/k)={fo['O(1/k)_confirmed']} | "
              f"2차 ratios={so['ratio_k_doubling']} O(1/k²)={so['O(1/k^2)_confirmed']}")

    report = {
        "phase": "W8.3 SuzukiTrotter",
        "honesty": "Adds 2nd-order (symmetric Suzuki) Trotter steps and extends the lattice to 4 qubits. "
                   "The Trotter STEPS (1st and 2nd order) are sealed EXACTLY (composite==golden, "
                   "golden=closed-form Pauli exponentials, no MatrixGate). The Trotter ERROR vs the true "
                   "e^{-iH T} and its CONVERGENCE ORDER are an OBSERVATION, NOT a seal — at fixed T=π/4, "
                   "1st-order error scales O(1/k) (ratio~2 per k-doubling) while 2nd-order Suzuki scales "
                   "O(1/k^2) (ratio~4). Where W8.2 showed 'approximation converges', W8.3 shows "
                   "'approximation QUALITY (order) is also quantifiable'. modules 62->63, apps 82->86.",
        "modules": mods, "apps": apps, "order_contrast_observation": obs,
    }
    all_ok = (all(m["sealed"] and m.get("tier", 0) == 0 for m in mods)
              and all(a["sealed"] and a["tier"] == 0 for a in apps)
              and obs["all_orders_confirmed"])
    report["all_ok"] = bool(all_ok)
    json.dump(report, open(os.path.join(OUT, "QSIM3-FAMILY-REPORT.json"), "w",
                           encoding="utf-8"), ensure_ascii=False, indent=2)
    print("-" * 88)
    print(f"all_ok={all_ok}  →  .pgf/arith/QSIM3-FAMILY-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
