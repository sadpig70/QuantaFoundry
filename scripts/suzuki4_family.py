# -*- coding: utf-8 -*-
"""
suzuki4_family.py — W12.3 Suzuki4

4th-order Yoshida-Suzuki Hamiltonian simulation steps for TFIM chains.

Sealed modules (Tier-0):
  rz_y4_p = Rz(-p*pi/8), rx_y4_p = Rx(-p*pi/4)
  rz_y4_q = Rz(-q*pi/8), rx_y4_q = Rx(-q*pi/4)
  where p=1/(4-4^(1/3)), q=1-4p.

Sealed apps (Tier-0):
  rzz_y4_p_half       = exp(i p*pi/16 ZZ)
  rzz_y4_q_half       = exp(i q*pi/16 ZZ)
  tfim3_suzuki4_step  = S2(p dt)^2 S2(q dt) S2(p dt)^2, dt=pi/8
  tfim4_suzuki4_step  = same for n=4

Honesty boundary:
  - seal = exact decomposition of the 4th-order Suzuki step
  - approximation error vs true exp(-iHT) and order ratios = observation, not a seal

Usage: python scripts/suzuki4_family.py
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
import app_assemble as aa       # noqa: E402  (oracle app seal path, use only)

SPECS_MODS = os.path.join(ROOT, "specs", "modules")
SPECS_APPS = os.path.join(ROOT, "specs", "apps")
MODREG = os.path.join(ROOT, "registry", "modules")
APPREG = os.path.join(ROOT, "registry", "apps")
OUT = os.path.join(ROOT, ".pgf", "arith")


def _coeff_src():
    return "p=1/(4-4**(1/3)); q=1-4*p\n"


def _module_spec(name, gate, coeff_name):
    angle_expr = f"-{coeff_name}*np.pi/8" if gate == "rz" else f"-{coeff_name}*np.pi/4"
    if gate == "rz":
        golden = (
            "golden = np.diag([np.exp(1j*{c}*np.pi/16), "
            "np.exp(-1j*{c}*np.pi/16)]).astype(complex)\n").format(c=coeff_name)
        bloq_class = "Rz"
        desc = f"Rz(-{coeff_name}·π/8), Yoshida-4 half-ZZ coefficient rotation"
    else:
        golden = (
            "X = np.array([[0,1],[1,0]], complex)\n"
            "golden = (np.cos({c}*np.pi/8)*np.eye(2) + "
            "1j*np.sin({c}*np.pi/8)*X).astype(complex)\n").format(c=coeff_name)
        bloq_class = "Rx"
        desc = f"Rx(-{coeff_name}·π/4), Yoshida-4 X-field coefficient rotation"
    return (
        f"# {name} — {desc}. analytic golden.\n"
        "```python id=bloq\n"
        "import numpy as np\n"
        f"from qualtran.bloqs.basic_gates import {bloq_class}\n"
        + _coeff_src()
        + f"bloq = {bloq_class}({angle_expr})\n"
        "```\n"
        "```python id=golden\n"
        "import numpy as np\n"
        + _coeff_src()
        + golden
        + "```\n"
        "```json id=meta\n"
        + json.dumps({"id": name, "n_sys": 1, "n_anc": 0}) + "\n```\n"
    )


def _seal_module(name, spec):
    sp = os.path.join(SPECS_MODS, f"{name}.pg")
    open(sp, "w", encoding="utf-8", newline="\n").write(spec)
    p = subprocess.run(["python", os.path.join(ORACLE, "verify_seal.py"), sp, "--out", MODREG],
                       capture_output=True, text=True, cwd=ROOT)
    seal_path = os.path.join(MODREG, f"{name}.sealed.json")
    if p.returncode != 0 or not os.path.exists(seal_path):
        return {"id": name, "sealed": False, "reason": (p.stdout + p.stderr)[-1000:]}
    sealed = json.load(open(seal_path, encoding="utf-8"))
    return {"id": name, "n_sys": sealed["n_sys"], "sealed": True,
            "tier": sealed.get("tier", 0), "u_hash": sealed["u_hash"]}


def _rzz_half_spec(name, coeff_name, rz_module):
    return (
        f"# {name} — exp(i {coeff_name}·π/16 ZZ) = CNOT·{rz_module}·CNOT. "
        "Yoshida-4 half-ZZ rotation, app-only Tier-0.\n"
        "```json id=app_meta\n"
        + json.dumps({"id": name, "n_sys": 2, "n_anc": 0}) + "\n```\n"
        "```python id=app_golden\n"
        "import numpy as np\n"
        + _coeff_src()
        + "Z=np.diag([1,-1]).astype(complex); ZZ=np.kron(Z,Z)\n"
        f"theta={coeff_name}*np.pi/16\n"
        "golden=(np.cos(theta)*np.eye(4)+1j*np.sin(theta)*ZZ).astype(complex)\n"
        "```\n"
        "```json id=plan\n"
        + json.dumps({"steps": [
            {"spec": "../modules/cnot.pg", "targets": [0, 1]},
            {"spec": f"../modules/{rz_module}.pg", "targets": [1]},
            {"spec": "../modules/cnot.pg", "targets": [0, 1]},
        ]}) + "\n```\n"
    )


def _s2_steps(n, tag):
    rzz = f"rzz_y4_{tag}_half.app.pg"
    rx = f"rx_y4_{tag}.pg"
    steps = []
    for i in range(n - 1):
        steps.append({"app": rzz, "targets": [i, i + 1]})
    for i in range(n):
        steps.append({"spec": f"../modules/{rx}", "targets": [i]})
    for i in range(n - 1):
        steps.append({"app": rzz, "targets": [i, i + 1]})
    return steps


def _tfim4_plan(n):
    steps = []
    for tag in ("p", "p", "q", "p", "p"):
        steps.extend(_s2_steps(n, tag))
    return {"steps": steps}


def _tfim4_golden_src(n):
    return (
        "import numpy as np\n"
        + _coeff_src()
        + f"n={n}; dt=np.pi/8; dim=1<<n\n"
        "I2=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex); Z=np.diag([1,-1]).astype(complex)\n"
        "def opn(ps):\n"
        "    m=np.array([[1]],dtype=complex)\n"
        "    for qbit in range(n): m=np.kron(m, ps.get(qbit,I2))\n"
        "    return m\n"
        "def e(P,d): return np.cos(d)*np.eye(dim,dtype=complex)+1j*np.sin(d)*P\n"
        "bonds=[(i,i+1) for i in range(n-1)]\n"
        "def S2(d):\n"
        "    U=np.eye(dim,dtype=complex)\n"
        "    for i,j in bonds: U=e(opn({i:Z,j:Z}),d/2)@U\n"
        "    for i in range(n): U=e(opn({i:X}),d)@U\n"
        "    for i,j in bonds: U=e(opn({i:Z,j:Z}),d/2)@U\n"
        "    return U\n"
        "golden=np.eye(dim,dtype=complex)\n"
        "for c in [p,p,q,p,p]: golden=S2(c*dt)@golden\n"
    )


def _tfim4_spec(name, n):
    return (
        f"# {name} — TFIM{n} 4th-order Yoshida-Suzuki step S2(pdt)^2·S2(qdt)·S2(pdt)^2, dt=π/8.\n"
        "```json id=app_meta\n"
        + json.dumps({"id": name, "n_sys": n, "n_anc": 0}) + "\n```\n"
        "```python id=app_golden\n" + _tfim4_golden_src(n) + "```\n"
        "```json id=plan\n" + json.dumps(_tfim4_plan(n)) + "\n```\n"
    )


def _forge_app(name, spec):
    sp = os.path.join(SPECS_APPS, f"{name}.app.pg")
    open(sp, "w", encoding="utf-8", newline="\n").write(spec)
    v = aa.assemble(sp, APPREG)
    return {"id": name, "n_sys": v.n_sys, "sealed": bool(v.sealed), "tier": v.tier,
            "u_hash": v.u_hash, "reason": v.reason}


def _order_observation():
    I2 = np.eye(2, dtype=complex)
    X = np.array([[0, 1], [1, 0]], complex)
    Z = np.diag([1, -1]).astype(complex)
    p = 1 / (4 - 4 ** (1 / 3))
    q = 1 - 4 * p
    T = np.pi / 4
    ks = (1, 2, 4, 8, 16, 32)

    def make(n):
        def opn(ps):
            m = np.array([[1]], dtype=complex)
            for r in range(n):
                m = np.kron(m, ps.get(r, I2))
            return m
        bonds = [(i, i + 1) for i in range(n - 1)]
        dim = 1 << n
        H = -(sum(opn({i: Z, j: Z}) for i, j in bonds) + sum(opn({i: X}) for i in range(n)))
        w, V = np.linalg.eigh(H)

        def e(P, d):
            return np.cos(d) * np.eye(dim, dtype=complex) + 1j * np.sin(d) * P

        def s1(d):
            U = np.eye(dim, dtype=complex)
            for i, j in bonds:
                U = e(opn({i: Z, j: Z}), d) @ U
            for i in range(n):
                U = e(opn({i: X}), d) @ U
            return U

        def s2(d):
            U = np.eye(dim, dtype=complex)
            for i, j in bonds:
                U = e(opn({i: Z, j: Z}), d / 2) @ U
            for i in range(n):
                U = e(opn({i: X}), d) @ U
            for i, j in bonds:
                U = e(opn({i: Z, j: Z}), d / 2) @ U
            return U

        def s4(d):
            U = np.eye(dim, dtype=complex)
            for c in (p, p, q, p, p):
                U = s2(c * d) @ U
            return U

        def exact(t):
            return V @ np.diag(np.exp(-1j * w * t)) @ V.conj().T
        return exact, s1, s2, s4, dim

    def sweep(exact, stepf, dim):
        rows = []
        for k in ks:
            d = T / k
            U = np.eye(dim, dtype=complex)
            for _ in range(k):
                U = stepf(d) @ U
            rows.append({"k": k, "dt": round(float(d), 8),
                         "error_2norm": round(float(np.linalg.norm(U - exact(T), 2)), 10)})
        ratios = [round(rows[i]["error_2norm"] / rows[i + 1]["error_2norm"], 3)
                  for i in range(len(rows) - 1)]
        return rows, ratios

    out = {"note": "OBSERVATION, NOT A SEAL — sealed S4 steps are exact decompositions of the "
                   "Yoshida formula. Approximation order is measured against true exp(-iHT) at fixed "
                   "T=pi/4: first ratio~2, second ratio~4, fourth ratio~16 under k doubling.",
           "coefficients": {"p": p, "q": q}, "fixed_T": float(T), "systems": {}}
    ok = True
    for n in (3, 4):
        exact, s1, s2, s4, dim = make(n)
        r1, ra1 = sweep(exact, s1, dim)
        r2, ra2 = sweep(exact, s2, dim)
        r4, ra4 = sweep(exact, s4, dim)
        first_ok = all(1.9 <= r <= 2.1 for r in ra1[-2:])
        second_ok = all(3.8 <= r <= 4.2 for r in ra2[-2:])
        fourth_ok = all(15.0 <= r <= 17.1 for r in ra4[-3:])
        ok = ok and first_ok and second_ok and fourth_ok
        out["systems"][f"tfim{n}"] = {
            "first_order": {"sweep": r1, "ratio_k_doubling": ra1, "O(1/k)_confirmed": bool(first_ok)},
            "second_order": {"sweep": r2, "ratio_k_doubling": ra2, "O(1/k^2)_confirmed": bool(second_ok)},
            "fourth_order": {"sweep": r4, "ratio_k_doubling": ra4, "O(1/k^4)_confirmed": bool(fourth_ok)}}
    out["all_orders_confirmed"] = bool(ok)
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 88)
    print("W12.3 Suzuki4 — Yoshida 4th-order TFIM steps + order observation.")
    print("=" * 88)

    module_specs = [
        ("rz_y4_p", _module_spec("rz_y4_p", "rz", "p")),
        ("rx_y4_p", _module_spec("rx_y4_p", "rx", "p")),
        ("rz_y4_q", _module_spec("rz_y4_q", "rz", "q")),
        ("rx_y4_q", _module_spec("rx_y4_q", "rx", "q")),
    ]
    modules = [_seal_module(name, spec) for name, spec in module_specs]
    for m in modules:
        print(f"[Module] {m['id']:8} n_sys={m.get('n_sys')} sealed={m['sealed']} "
              f"tier={m.get('tier')} u={str(m.get('u_hash'))[:14]}"
              + ("" if m["sealed"] else f" reason={m.get('reason')}"))

    app_specs = [
        ("rzz_y4_p_half", _rzz_half_spec("rzz_y4_p_half", "p", "rz_y4_p")),
        ("rzz_y4_q_half", _rzz_half_spec("rzz_y4_q_half", "q", "rz_y4_q")),
        ("tfim3_suzuki4_step", _tfim4_spec("tfim3_suzuki4_step", 3)),
        ("tfim4_suzuki4_step", _tfim4_spec("tfim4_suzuki4_step", 4)),
    ]
    apps = [_forge_app(name, spec) for name, spec in app_specs]
    for a in apps:
        print(f"[App]    {a['id']:20} n_sys={a.get('n_sys')} sealed={a['sealed']} "
              f"tier={a.get('tier')} u={str(a.get('u_hash'))[:14]}"
              + ("" if a["sealed"] else f" reason={a['reason']}"))

    obs = _order_observation()
    for label, rec in obs["systems"].items():
        print(f"[Order] {label}: "
              f"r1_last={rec['first_order']['ratio_k_doubling'][-2:]} "
              f"r2_last={rec['second_order']['ratio_k_doubling'][-2:]} "
              f"r4_last={rec['fourth_order']['ratio_k_doubling'][-3:]}")

    all_ok = (all(m["sealed"] and m.get("tier", 0) == 0 for m in modules)
              and all(a["sealed"] and a["tier"] == 0 for a in apps)
              and obs["all_orders_confirmed"])
    report = {
        "phase": "W12.3 Suzuki4",
        "modules": modules,
        "apps": apps,
        "order_observation": obs,
        "all_ok": bool(all_ok),
        "honesty": "The modules and apps seal the exact Yoshida-Suzuki 4th-order formula "
                   "for fixed coefficient rotations. Approximation error and order ratios "
                   "against true exp(-iHT) are observations, not seals.",
    }
    json.dump(report, open(os.path.join(OUT, "SUZUKI4-FAMILY-REPORT.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("-" * 88)
    print(f"all_ok={all_ok}  ->  .pgf/arith/SUZUKI4-FAMILY-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
