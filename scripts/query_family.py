# -*- coding: utf-8 -*-
"""
query_family.py — W12.1 Query/Oracle Algorithms

Deutsch-Jozsa, Bernstein-Vazirani, Simon query/oracle algorithms as app-only Tier-0 seals.
No new modules: every circuit reuses sealed h_gate, x_gate, cnot.

Sealed apps:
  dj2_const1       = Deutsch-Jozsa n=2, f(x)=1
  dj2_balanced_xor = Deutsch-Jozsa n=2, f(x)=x0 xor x1
  bv3_s101         = Bernstein-Vazirani n=3, secret s=101
  simon2_s11       = Simon n=2, hidden period s=11 via f(x)=x0 xor x1

Honesty boundary:
  - seal = exact unitary decomposition of the oracle algorithm circuit (Tier-0 C-app)
  - query advantage / readout = backend_adapter observation, not a seal

Usage: python scripts/query_family.py
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
    spec = {"h": "../modules/h_gate.pg", "x": "../modules/x_gate.pg", "cnot": "../modules/cnot.pg"}
    steps = []
    for gate, targets in ops:
        step = {"spec": spec[gate]}
        if targets is not None:
            step["targets"] = targets
        steps.append(step)
    return {"steps": steps}


def _app_spec(name, n_sys, ops, desc):
    ops_json = json.dumps(ops)
    golden = (
        "import numpy as np\n"
        "H=np.array([[1,1],[1,-1]],dtype=complex)/np.sqrt(2)\n"
        "X=np.array([[0,1],[1,0]],dtype=complex)\n"
        "CNOT=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],dtype=complex)\n"
        "def emb(g,qs):\n"
        f"    n={n_sys}\n"
        "    k=len(qs); G=g.reshape([2]*k+[2]*k)\n"
        "    T=np.eye(1<<n,dtype=complex).reshape([2]*n+[1<<n])\n"
        "    T=np.tensordot(G,T,axes=(list(range(k,2*k)),qs)); T=np.moveaxis(T,list(range(k)),qs)\n"
        "    return T.reshape(1<<n,1<<n)\n"
        f"ops={ops_json}\n"
        f"U=np.eye(1<<{n_sys},dtype=complex)\n"
        "for gate,qs in ops:\n"
        "    G={'h':H,'x':X,'cnot':CNOT}[gate]\n"
        "    U=emb(G,qs)@U\n"
        "golden=U\n"
    )
    return (
        f"# {name} — {desc}. W12.1 query/oracle algorithm, app-only Tier-0, 신규 모듈 0.\n"
        "```json id=app_meta\n" + json.dumps({"id": name, "n_sys": n_sys, "n_anc": 0}) + "\n```\n"
        "```python id=app_golden\n" + golden + "```\n"
        "```json id=plan\n" + json.dumps(_ops_to_plan(ops)) + "\n```\n"
    )


def _dj_ops(n_query, oracle_ops):
    out = n_query
    ops = [("x", [out]), ("h", [out])]
    ops += [("h", [q]) for q in range(n_query)]
    ops += oracle_ops
    ops += [("h", [q]) for q in range(n_query)]
    return ops


def _bv_ops(n_query, secret_ones):
    out = n_query
    oracle = [("cnot", [q, out]) for q in secret_ones]
    return _dj_ops(n_query, oracle)


def _simon_ops(n_query, oracle_ops):
    ops = [("h", [q]) for q in range(n_query)]
    ops += oracle_ops
    ops += [("h", [q]) for q in range(n_query)]
    return ops


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


def _run_zero(app_id):
    app = ba.load_sealed_app(app_id)
    return app, app["U"] @ ba.zero_state(app["n"])


def _rounded_marginal(psi, n, qubits):
    return {format(k, f"0{len(qubits)}b"): round(float(v), 6)
            for k, v in sorted(ba.marginal_register(psi, n, qubits).items()) if v > 1e-9}


def _query_observation():
    obs = {
        "note": "OBSERVATION, NOT A SEAL — sealed query/oracle circuits executed from |0...0>. "
                "Deutsch-Jozsa/BV one-query readout and Simon support constraints are behavior claims over "
                "sealed Tier-0 unitaries; the seal itself only certifies composite==golden.",
        "instances": {},
    }

    checks = []

    app, psi = _run_zero("dj2_const1")
    q = _rounded_marginal(psi, app["n"], [0, 1])
    rec = {"algorithm": "Deutsch-Jozsa", "function": "constant_one", "query_marginal": q,
           "expected": {"00": 1.0}, "deterministic_constant": q == {"00": 1.0}}
    obs["instances"]["dj2_const1"] = rec
    checks.append(rec["deterministic_constant"])

    app, psi = _run_zero("dj2_balanced_xor")
    q = _rounded_marginal(psi, app["n"], [0, 1])
    rec = {"algorithm": "Deutsch-Jozsa", "function": "x0_xor_x1", "query_marginal": q,
           "expected": {"11": 1.0}, "deterministic_balanced_nonzero": q == {"11": 1.0}}
    obs["instances"]["dj2_balanced_xor"] = rec
    checks.append(rec["deterministic_balanced_nonzero"])

    app, psi = _run_zero("bv3_s101")
    q = _rounded_marginal(psi, app["n"], [0, 1, 2])
    rec = {"algorithm": "Bernstein-Vazirani", "secret": "101", "query_marginal": q,
           "expected": {"101": 1.0}, "secret_recovered_one_query": q == {"101": 1.0}}
    obs["instances"]["bv3_s101"] = rec
    checks.append(rec["secret_recovered_one_query"])

    app, psi = _run_zero("simon2_s11")
    q = _rounded_marginal(psi, app["n"], [0, 1])
    support = sorted(q)
    orthogonal = all(((int(bits[0]) ^ int(bits[1])) == 0) for bits in support)
    rec = {"algorithm": "Simon", "hidden_period": "11", "query_marginal": q,
           "expected_support": ["00", "11"], "all_y_dot_s_zero": orthogonal,
           "support_correct": support == ["00", "11"] and all(abs(q[b] - 0.5) < 1e-6 for b in support)}
    obs["instances"]["simon2_s11"] = rec
    checks.append(rec["all_y_dot_s_zero"] and rec["support_correct"])

    obs["all_ok"] = all(checks)
    return obs


def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 84)
    print("W12.1 Query/Oracle Algorithms — DJ · BV · Simon, app-only Tier-0, 신규 모듈 0.")
    print("=" * 84)

    specs = [
        ("dj2_const1", _app_spec(
            "dj2_const1", 3,
            _dj_ops(2, [("x", [2])]),
            "Deutsch-Jozsa n=2 constant f(x)=1; |-> output makes oracle a global phase")),
        ("dj2_balanced_xor", _app_spec(
            "dj2_balanced_xor", 3,
            _dj_ops(2, [("cnot", [0, 2]), ("cnot", [1, 2])]),
            "Deutsch-Jozsa n=2 balanced f(x)=x0 xor x1")),
        ("bv3_s101", _app_spec(
            "bv3_s101", 4,
            _bv_ops(3, [0, 2]),
            "Bernstein-Vazirani n=3 secret s=101")),
        ("simon2_s11", _app_spec(
            "simon2_s11", 3,
            _simon_ops(2, [("cnot", [0, 2]), ("cnot", [1, 2])]),
            "Simon n=2 hidden period s=11 with f(x)=x0 xor x1")),
    ]

    apps = [_forge_app(name, spec) for name, spec in specs]
    for app in apps:
        print(f"[App] {app['id']:18} n_sys={app.get('n_sys')} sealed={app['sealed']} "
              f"tier={app.get('tier')} u={str(app.get('u_hash'))[:14]}"
              + ("" if app["sealed"] else f" reason={app['reason']}"))

    obs = _query_observation()
    for app_id, rec in obs["instances"].items():
        print(f"[Obs] {app_id:18} query={rec['query_marginal']} ok="
              f"{rec.get('deterministic_constant', rec.get('deterministic_balanced_nonzero', rec.get('secret_recovered_one_query', rec.get('support_correct'))))}")

    all_ok = all(a["sealed"] and a["tier"] == 0 for a in apps) and obs["all_ok"]
    report = {
        "phase": "W12.1 Query/Oracle Algorithms",
        "apps": apps,
        "query_observation": obs,
        "all_ok": bool(all_ok),
        "honesty": "The four query/oracle algorithm circuits are sealed as Tier-0 app unitaries "
                   "(composite==golden, up-to-global-phase, zero new modules; only h_gate/x_gate/cnot). "
                   "Deutsch-Jozsa one-query distinction, Bernstein-Vazirani one-query secret recovery, "
                   "and Simon y·s=0 support are backend_adapter observations over sealed outputs, not seals.",
    }
    json.dump(report, open(os.path.join(OUT, "QUERY-FAMILY-REPORT.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("-" * 84)
    print(f"all_ok={all_ok}  ->  .pgf/arith/QUERY-FAMILY-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
