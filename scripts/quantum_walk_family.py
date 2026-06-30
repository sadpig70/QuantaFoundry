# -*- coding: utf-8 -*-
"""
quantum_walk_family.py — W12.2 Quantum Walk

Coined quantum walk on cycles C4/C8 as app-only Tier-0 seals.
No new modules: every circuit reuses sealed h_gate, x_gate, cnot, toffoli, c3x.

Sealed apps:
  qw_c4_step    = one coined walk step on C4
  qw_c4_2steps  = two repeated C4 steps via sub-app reuse
  qw_c8_step    = one coined walk step on C8
  qw_c8_3steps  = three repeated C8 steps via sub-app reuse

Honesty boundary:
  - seal = exact unitary decomposition of the coin+shift circuit (Tier-0 C-app)
  - position distributions / interference / quantum-vs-classical contrast = backend_adapter observation, not a seal

Usage: python scripts/quantum_walk_family.py
"""
from __future__ import annotations

import os
import sys
import json

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, ORACLE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import app_assemble as aa       # noqa: E402  (oracle app seal path, use only)
import backend_adapter as ba    # noqa: E402  (behavior observation, not a seal)

SPECS_APPS = os.path.join(ROOT, "specs", "apps")
APPREG = os.path.join(ROOT, "registry", "apps")
OUT = os.path.join(ROOT, ".pgf", "arith")


def _ops_to_plan(ops):
    spec = {
        "h": "../modules/h_gate.pg",
        "x": "../modules/x_gate.pg",
        "cnot": "../modules/cnot.pg",
        "toffoli": "../modules/toffoli.pg",
        "c3x": "../modules/c3x.pg",
    }
    steps = []
    for gate, targets in ops:
        step = {"spec": spec[gate]}
        if targets is not None:
            step["targets"] = targets
        steps.append(step)
    return {"steps": steps}


def _c4_step_ops():
    # qubits: coin=0, p0=1, p1=2. Shift: p0 ^= p1 ^ coin; p1 ^= 1.
    return [("h", [0]), ("cnot", [2, 1]), ("cnot", [0, 1]), ("x", [2])]


def _c8_step_ops():
    # qubits: coin=0, p0=1, p1=2, p2=3.
    # If coin=0: increment position. If coin=1: decrement position.
    return [
        ("h", [0]),
        ("x", [0]),
        ("c3x", [0, 2, 3, 1]),
        ("toffoli", [0, 3, 2]),
        ("cnot", [0, 3]),
        ("x", [0]),
        ("cnot", [0, 3]),
        ("toffoli", [0, 3, 2]),
        ("c3x", [0, 2, 3, 1]),
    ]


def _walk_golden_src(npos, power):
    return (
        "import numpy as np\n"
        "H=np.array([[1,1],[1,-1]],dtype=complex)/np.sqrt(2)\n"
        f"npos={npos}; power={power}; n=1+npos; N=1<<npos; dim=1<<n\n"
        "S=np.zeros((dim,dim),dtype=complex)\n"
        "for s in range(dim):\n"
        "    coin=(s>>npos)&1; pos=s&(N-1)\n"
        "    newpos=(pos+(1 if coin==0 else -1))%N\n"
        "    out=(coin<<npos)|newpos\n"
        "    S[out,s]=1\n"
        "Hc=np.kron(H,np.eye(N,dtype=complex))\n"
        "step=S@Hc\n"
        "golden=np.linalg.matrix_power(step,power)\n"
    )


def _step_spec(name, npos, ops, desc):
    return (
        f"# {name} — {desc}. W12.2 coined quantum walk step, app-only Tier-0, 신규 모듈 0.\n"
        "```json id=app_meta\n" + json.dumps({"id": name, "n_sys": 1 + npos, "n_anc": 0}) + "\n```\n"
        "```python id=app_golden\n" + _walk_golden_src(npos, 1) + "```\n"
        "```json id=plan\n" + json.dumps(_ops_to_plan(ops)) + "\n```\n"
    )


def _power_spec(name, base_app, npos, power, desc):
    return (
        f"# {name} — {desc}. W12.2 repeated coined quantum walk via {base_app}^{power} sub-app reuse.\n"
        "```json id=app_meta\n" + json.dumps({"id": name, "n_sys": 1 + npos, "n_anc": 0}) + "\n```\n"
        "```python id=app_golden\n" + _walk_golden_src(npos, power) + "```\n"
        "```json id=plan\n"
        + json.dumps({"steps": [{"app": f"{base_app}.app.pg"} for _ in range(power)]}) + "\n```\n"
    )


def _forge_app(name, spec):
    sp = os.path.join(SPECS_APPS, f"{name}.app.pg")
    open(sp, "w", encoding="utf-8", newline="\n").write(spec)
    v = aa.assemble(sp, APPREG)
    return {
        "id": name,
        "n_sys": v.n_sys,
        "sealed": bool(v.sealed),
        "tier": v.tier,
        "u_hash": v.u_hash,
        "reason": v.reason,
    }


def _rounded_position_marginal(app_id, npos):
    app = ba.load_sealed_app(app_id)
    psi = app["U"] @ ba.zero_state(app["n"])
    qubits = list(range(1, 1 + npos))
    marg = ba.marginal_register(psi, app["n"], qubits)
    return {format(k, f"0{npos}b"): round(float(v), 6) for k, v in sorted(marg.items()) if v > 1e-9}


def _classical_cycle_distribution(npos, steps):
    N = 1 << npos
    dist = {0: 1.0}
    for _ in range(steps):
        nxt = {}
        for pos, p in dist.items():
            nxt[(pos + 1) % N] = nxt.get((pos + 1) % N, 0.0) + 0.5 * p
            nxt[(pos - 1) % N] = nxt.get((pos - 1) % N, 0.0) + 0.5 * p
        dist = nxt
    return {format(k, f"0{npos}b"): round(float(v), 6) for k, v in sorted(dist.items()) if v > 1e-9}


def _tv_distance(a, b):
    keys = set(a) | set(b)
    return 0.5 * sum(abs(a.get(k, 0.0) - b.get(k, 0.0)) for k in keys)


def _walk_observation():
    obs = {
        "note": "OBSERVATION, NOT A SEAL — sealed coined-walk circuits executed from |coin=0,pos=0>. "
                "Position distributions and quantum-vs-classical contrast are behavior claims over sealed "
                "Tier-0 unitaries; the seal itself only certifies composite==golden.",
        "instances": {},
    }

    c4_1 = _rounded_position_marginal("qw_c4_step", 2)
    c4_2 = _rounded_position_marginal("qw_c4_2steps", 2)
    c8_1 = _rounded_position_marginal("qw_c8_step", 3)
    c8_3 = _rounded_position_marginal("qw_c8_3steps", 3)
    c8_classical_3 = _classical_cycle_distribution(3, 3)
    tv = round(_tv_distance(c8_3, c8_classical_3), 6)

    obs["instances"]["qw_c4_step"] = {
        "position_marginal": c4_1,
        "expected_adjacent_support": {"01": 0.5, "11": 0.5},
        "adjacent_support_ok": c4_1 == {"01": 0.5, "11": 0.5},
    }
    obs["instances"]["qw_c4_2steps"] = {
        "position_marginal": c4_2,
        "normalized": abs(sum(c4_2.values()) - 1.0) < 1e-6,
    }
    obs["instances"]["qw_c8_step"] = {
        "position_marginal": c8_1,
        "expected_adjacent_support": {"001": 0.5, "111": 0.5},
        "adjacent_support_ok": c8_1 == {"001": 0.5, "111": 0.5},
    }
    obs["instances"]["qw_c8_3steps"] = {
        "position_marginal": c8_3,
        "classical_unbiased_3steps": c8_classical_3,
        "total_variation_vs_classical": tv,
        "interference_contrast_ok": tv > 0.1,
        "normalized": abs(sum(c8_3.values()) - 1.0) < 1e-6,
    }
    obs["all_ok"] = all([
        obs["instances"]["qw_c4_step"]["adjacent_support_ok"],
        obs["instances"]["qw_c4_2steps"]["normalized"],
        obs["instances"]["qw_c8_step"]["adjacent_support_ok"],
        obs["instances"]["qw_c8_3steps"]["interference_contrast_ok"],
        obs["instances"]["qw_c8_3steps"]["normalized"],
    ])
    return obs


def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 84)
    print("W12.2 Quantum Walk — coined walks on C4/C8, app-only Tier-0, 신규 모듈 0.")
    print("=" * 84)

    specs = [
        ("qw_c4_step", _step_spec("qw_c4_step", 2, _c4_step_ops(), "C4 one-step U=S4·H_coin")),
        ("qw_c4_2steps", _power_spec("qw_c4_2steps", "qw_c4_step", 2, 2, "C4 two-step walk")),
        ("qw_c8_step", _step_spec("qw_c8_step", 3, _c8_step_ops(), "C8 one-step U=S8·H_coin")),
        ("qw_c8_3steps", _power_spec("qw_c8_3steps", "qw_c8_step", 3, 3, "C8 three-step walk")),
    ]

    apps = [_forge_app(name, spec) for name, spec in specs]
    for app in apps:
        print(f"[App] {app['id']:14} n_sys={app.get('n_sys')} sealed={app['sealed']} "
              f"tier={app.get('tier')} u={str(app.get('u_hash'))[:14]}"
              + ("" if app["sealed"] else f" reason={app['reason']}"))

    obs = _walk_observation()
    for app_id, rec in obs["instances"].items():
        print(f"[Obs] {app_id:14} pos={rec['position_marginal']}")
    print(f"[Obs] C8 3-step TV vs classical = "
          f"{obs['instances']['qw_c8_3steps']['total_variation_vs_classical']}")

    all_ok = all(a["sealed"] and a["tier"] == 0 for a in apps) and obs["all_ok"]
    report = {
        "phase": "W12.2 Quantum Walk",
        "apps": apps,
        "walk_observation": obs,
        "all_ok": bool(all_ok),
        "honesty": "The four coined-walk circuits are sealed as Tier-0 app unitaries "
                   "(composite==golden, up-to-global-phase, zero new modules; only h_gate/x_gate/"
                   "cnot/toffoli/c3x). Position marginals, interference, and quantum-vs-classical "
                   "contrast are backend_adapter observations over sealed outputs, not seals.",
    }
    json.dump(report, open(os.path.join(OUT, "QUANTUM-WALK-REPORT.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("-" * 84)
    print(f"all_ok={all_ok}  ->  .pgf/arith/QUANTUM-WALK-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
