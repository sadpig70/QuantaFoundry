# -*- coding: utf-8 -*-
"""
c9x_shor381_frontier.py - W12.8/W12.9/W12.10 combined frontier.

This closes the 9-control primitive gap, proves payoff with a compact family of
N>=256 modular multipliers, and lifts the family into a Shor-style structural app.

Sealed outputs:
  Tier-0 module: c9x
  Tier-0 apps:   cmul{2,4,16,256}_mod381
  Tier-1 app:    shor381 (17q structural composition)

Honesty boundary:
  - c9x and cmul* are exact Tier-0 permutation seals.
  - shor381 is Tier-1 STRUCTURAL; no dense whole-unitary equivalence is claimed.
  - period/factor readout is illustrative only, not seal evidence.
"""
from __future__ import annotations

import json
import math
import os
import subprocess
import sys
from collections import Counter
from math import gcd

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, ORACLE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import app_assemble as aa  # noqa: E402
import genskills as gs  # noqa: E402
import verify_seal as vs  # noqa: E402

SPECS_MODS = os.path.join(ROOT, "specs", "modules")
SPECS_APPS = os.path.join(ROOT, "specs", "apps")
MODREG = os.path.join(ROOT, "registry", "modules")
APPREG = os.path.join(ROOT, "registry", "apps")
OUT = os.path.join(ROOT, ".pgf", "arith")

N = 381
A = 2
T = 8
WORK = math.ceil(math.log2(N))
NQ = WORK + 1
POWA = [pow(A, 1 << (T - 1 - q), N) for q in range(T)]
UNIQUE_POWERS = sorted(set(POWA) - {1})

_MCT_SET = {"x_gate", "cnot", "toffoli", "c3x", "c4x", "c5x", "c6x", "c7x", "c8x", "c9x"}


def _factor(n: int) -> list[int]:
    out, d, m = [], 2, n
    while d * d <= m:
        while m % d == 0:
            out.append(d)
            m //= d
        d += 1
    if m > 1:
        out.append(m)
    return out


def _c9x_spec() -> str:
    return (
        "```python id=bloq\n"
        "from qualtran.bloqs.mcmt import MultiControlX\n"
        "bloq = MultiControlX(cvs=(1,) * 9)\n"
        "```\n"
        "```python id=golden\n"
        "import numpy as np\n"
        "# c9x: control=first 9 qubits (MSB), target=last (big-endian).\n"
        "golden = np.zeros((1<<10, 1<<10), dtype=complex)\n"
        "for s in range(1<<10):\n"
        "    o = (s ^ 1) if (s >> 1) == ((1<<9) - 1) else s\n"
        "    golden[o, s] = 1\n"
        "```\n"
        "```json id=meta\n"
        "{\"id\": \"c9x\", \"n_sys\": 10, \"n_anc\": 0}\n"
        "```\n"
    )


def _seal_c9x() -> dict:
    os.makedirs(SPECS_MODS, exist_ok=True)
    spec_path = os.path.join(SPECS_MODS, "c9x.pg")
    with open(spec_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(_c9x_spec())
    seal_path = os.path.join(MODREG, "c9x.sealed.json")
    if not os.path.exists(seal_path):
        proc = subprocess.run(
            ["python", os.path.join(ORACLE, "verify_seal.py"), spec_path, "--out", MODREG],
            capture_output=True,
            text=True,
            cwd=ORACLE,
        )
        if proc.returncode != 0 and not os.path.exists(seal_path):
            return {"id": "c9x", "sealed": False, "stderr": proc.stderr[-1000:]}
    sealed = json.load(open(seal_path, encoding="utf-8"))
    return {
        "id": "c9x",
        "sealed": bool(sealed.get("sealed")),
        "tier": sealed.get("tier", 0),
        "n_sys": sealed.get("n_sys"),
        "u_hash": sealed.get("u_hash"),
        "resource": sealed.get("resource", {}),
    }


def _independent_cnx_hash(nc: int) -> str:
    n = nc + 1
    U = np.zeros((1 << n, 1 << n), dtype=complex)
    for s in range(1 << n):
        out = (s ^ 1) if (s >> 1) == ((1 << nc) - 1) else s
        U[out, s] = 1
    return vs.hash_unitary(U)


def _wire_mask(wire: int, nq: int) -> int:
    return 1 << (nq - 1 - wire)


def _simulate_mct_plan(gates: list[tuple[tuple[int, ...], int]], nq: int) -> list[int]:
    perm = list(range(1 << nq))
    masks = [(sum(_wire_mask(c, nq) for c in controls), _wire_mask(target, nq)) for controls, target in gates]
    for control_mask, target_mask in masks:
        for s, v in enumerate(perm):
            if (v & control_mask) == control_mask:
                perm[s] = v ^ target_mask
    return perm


def _perm_hash(perm: list[int]) -> str:
    dim = len(perm)
    U = np.zeros((dim, dim), dtype=complex)
    U[np.asarray(perm, dtype=int), np.arange(dim)] = 1
    return vs.hash_unitary(U)


def _seal_exact_permutation_app(app_id: str, nq: int, gates, target_perm) -> dict:
    plan_perm = _simulate_mct_plan(gates, nq)
    if plan_perm != list(target_perm):
        raise RuntimeError(f"{app_id}: MCT plan permutation does not match arithmetic golden")
    u_hash = _perm_hash(plan_perm)
    resources = []
    for controls, _ in gates:
        mid = gs._MCT_MODULE[len(controls)]
        seal_path = os.path.join(MODREG, f"{mid}.sealed.json")
        resources.append(json.load(open(seal_path, encoding="utf-8"))["resource"])
    resource = aa._aggregate_cost(resources)
    sealed = aa._seal_dict(app_id, nq, "C1-C4(app)", u_hash, resource, 0)
    aa.Registry(APPREG)._admit(sealed)
    disk = json.load(open(os.path.join(APPREG, f"{app_id}.sealed.json"), encoding="utf-8"))
    return {
        "sealed": bool(disk.get("sealed")),
        "tier": disk.get("tier"),
        "u_hash": disk.get("u_hash"),
        "resource": disk.get("resource", {}),
        "reason": "fast_exact_permutation_capp",
    }


def _seal_cmul(a: int) -> dict:
    spec, deps = gs.gen_modmul(a, N, NQ)
    gates = gs.mmd_synthesize(gs._modmul_perm(a, N, NQ), NQ)
    maxc = max((len(c) for c, _ in gates), default=0)
    if not set(deps).issubset(_MCT_SET):
        raise RuntimeError(f"unexpected deps for cmul{a}_mod{N}: {deps}")
    if maxc != 9 or "c9x" not in deps:
        raise RuntimeError(f"cmul{a}_mod{N} did not exercise c9x: deps={deps}, maxc={maxc}")
    spec_path = os.path.join(SPECS_APPS, f"cmul{a}_mod{N}.app.pg")
    with open(spec_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(spec)
    verdict = _seal_exact_permutation_app(f"cmul{a}_mod{N}", NQ, gates, gs._modmul_perm(a, N, NQ))
    return {
        "id": f"cmul{a}_mod{N}",
        "N": N,
        "a": a,
        "nq": NQ,
        "sealed": bool(verdict["sealed"]),
        "tier": verdict["tier"],
        "u_hash": verdict["u_hash"],
        "reason": verdict["reason"],
        "gate_count": len(gates),
        "control_dist": dict(Counter(len(c) for c, _ in gates)),
        "max_control": maxc,
        "deps": deps,
    }


def _independent_cmul_hash(a: int) -> dict:
    dim = 1 << NQ
    U = np.zeros((dim, dim), dtype=complex)
    for s in range(dim):
        if (s >> (NQ - 1)) & 1 == 0:
            U[s, s] = 1
        else:
            w = s & ((1 << (NQ - 1)) - 1)
            nw = (a * w) % N if w < N else w
            U[(1 << (NQ - 1)) | nw, s] = 1
    got = vs.hash_unitary(U)
    sealed = json.load(open(os.path.join(APPREG, f"cmul{a}_mod{N}.sealed.json"), encoding="utf-8"))["u_hash"]
    return {
        "id": f"cmul{a}_mod{N}",
        "independent_u_hash": got[:16],
        "matches_sealed": got == sealed,
    }


def _children_sealed() -> dict[str, bool]:
    need_apps = [f"cmul{a}_mod{N}" for a in UNIQUE_POWERS] + ["iqft8"]
    out = {app: os.path.exists(os.path.join(APPREG, f"{app}.sealed.json")) for app in need_apps}
    out["h_gate"] = os.path.exists(os.path.join(MODREG, "h_gate.sealed.json"))
    return out


def _shor381_spec() -> tuple[str, int]:
    work = list(range(T, T + WORK))
    steps = []
    for q in range(T):
        steps.append({"spec": "../modules/h_gate.pg", "targets": [q]})
    for q, mul in enumerate(POWA):
        if mul == 1:
            continue
        steps.append({"app": f"cmul{mul}_mod{N}.app.pg", "targets": [q] + work})
    steps.append({"app": "iqft8.app.pg", "targets": list(range(T))})
    n_sys = T + WORK
    plan = {"tier": "structural", "steps": steps}
    header = (
        f"# shor381 - Shor period-finding structural frontier (N={N}={'*'.join(map(str, _factor(N)))}, a={A}). "
        f"{n_sys}q: counting={T}, work={WORK}. "
        f"H^{T} controlled-U^(2^j)(powa={POWA}) iqft8. "
        "17q>EXACT_BOUND -> Tier-1 STRUCTURAL only. "
        "Readout illustrative: ord_381(2)=14 -> gcd(2^7+-1,381)=3,127.\n"
    )
    return (
        header
        + "```json id=app_meta\n"
        + json.dumps({"id": "shor381", "n_sys": n_sys, "n_anc": 0})
        + "\n```\n"
        + "```json id=plan\n"
        + json.dumps(plan)
        + "\n```\n"
    ), n_sys


def _assemble_shor381() -> dict:
    spec, n_sys = _shor381_spec()
    spec_path = os.path.join(SPECS_APPS, "shor381.app.pg")
    with open(spec_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(spec)
    plan = json.loads(spec.split("```json id=plan\n", 1)[1].split("```", 1)[0])
    children = []
    for step in plan["steps"]:
        targets = step.get("targets")
        if "app" in step:
            cid = step["app"][:-7]
            seal_path = os.path.join(APPREG, f"{cid}.sealed.json")
        else:
            cid = os.path.basename(step["spec"])[:-3]
            seal_path = os.path.join(MODREG, f"{cid}.sealed.json")
        sealed = json.load(open(seal_path, encoding="utf-8"))
        width = sealed["n_sys"]
        if targets is None:
            if width != n_sys:
                raise RuntimeError(f"interface mismatch for {cid}: width {width} without targets")
        elif len(targets) != width or len(set(targets)) != len(targets) or any(t < 0 or t >= n_sys for t in targets):
            raise RuntimeError(f"interface mismatch for {cid}: targets={targets}, width={width}")
        children.append({"u_hash": sealed["u_hash"], "resource": sealed["resource"],
                         "targets": targets, "n_qubits": width})
    resource = aa._aggregate_cost([c["resource"] for c in children])
    u_hash = aa._structural_hash(children, n_sys)
    sealed_out = aa._seal_dict("shor381", n_sys, "C1-C4(structural)", u_hash, resource, 1)
    aa.Registry(APPREG)._admit(sealed_out)
    disk = json.load(open(os.path.join(APPREG, "shor381.sealed.json"), encoding="utf-8"))
    return {
        "id": "shor381",
        "n_sys": n_sys,
        "sealed": bool(disk.get("sealed")),
        "tier": disk.get("tier"),
        "u_hash": disk.get("u_hash"),
        "contract": disk.get("contract"),
        "reason": "fast_structural_child_seals",
        "deterministic_reassembly": u_hash == aa._structural_hash(children, n_sys) == disk["u_hash"],
    }


def _period_readout() -> dict:
    r = 1
    x = A % N
    while x != 1:
        x = (x * A) % N
        r += 1
    result = {"a": A, "N": N, "order_r": r, "r_even": r % 2 == 0}
    if r % 2 == 0:
        h = pow(A, r // 2, N)
        result["a_r2"] = h
        result["nontrivial"] = h != N - 1
        result["factors"] = sorted({gcd(h - 1, N), gcd(h + 1, N)} - {1, N})
    result["note"] = "illustrative only; period/factor readout is not seal evidence"
    return result


def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    print("=" * 84)
    print("W12.8-W12.10 C9x/Shor381 frontier - N=381=3*127, a=2.")
    print("Honesty: c9x/cmul*=Tier-0 EXACT, shor381=Tier-1 STRUCTURAL, readout=illustrative.")
    print("=" * 84)
    print(f"[Target] N={N} factors={_factor(N)} a={A} T={T} WORK={WORK} powa={POWA} unique={UNIQUE_POWERS}")

    c9x = _seal_c9x()
    c9x_indep = _independent_cnx_hash(9)
    c9x_match = c9x.get("u_hash") == c9x_indep
    print(f"[C9X] sealed={c9x['sealed']} tier={c9x['tier']} n_sys={c9x['n_sys']} match={c9x_match}")

    cmuls = []
    for mul in UNIQUE_POWERS:
        rec = _seal_cmul(mul)
        cmuls.append(rec)
        print(
            f"[Cmul] {rec['id']:14} sealed={rec['sealed']} tier={rec['tier']} "
            f"gates={rec['gate_count']} maxc={rec['max_control']} c9={rec['control_dist'].get(9, 0)} "
            f"u={str(rec['u_hash'])[:14]}"
        )

    indep = [_independent_cmul_hash(mul) for mul in UNIQUE_POWERS]
    indep_ok = sum(1 for row in indep if row["matches_sealed"])
    print(f"[IndependentArith] {indep_ok}/{len(indep)} u_hash matches sealed")

    children = _children_sealed()
    print(f"[Children] {children}")
    shor = _assemble_shor381()
    print(
        f"[Shor381] sealed={shor['sealed']} tier={shor['tier']} n_sys={shor['n_sys']} "
        f"u={str(shor['u_hash'])[:16]} deterministic={shor['deterministic_reassembly']}"
    )

    readout = _period_readout()
    print(
        f"[Readout|illustrative] ord_{N}({A})={readout['order_r']} -> "
        f"2^{readout['order_r']//2} mod {N}={readout.get('a_r2')} -> factors={readout.get('factors')}"
    )

    report = {
        "phase": "W12.8-W12.10 C9xPayoffFamilyToShor381",
        "honesty": "c9x closes the 9-control primitive gap for 9-work-bit modular arithmetic. "
                   "cmul powers are Tier-0 exact permutation app seals; shor381 is Tier-1 structural, "
                   "weaker than dense unitary equivalence; period readout is illustrative only. "
                   "c10x remains a separate feasibility review.",
        "target": {"N": N, "a": A, "factors": _factor(N), "counting_t": T, "work": WORK,
                   "powa": POWA, "unique_powers": UNIQUE_POWERS},
        "c9x_module": c9x,
        "c9x_independent": {"independent_u_hash": c9x_indep[:16], "matches_sealed": c9x_match},
        "cmul_apps": cmuls,
        "independent_arith_verify": indep,
        "children_sealed": children,
        "shor381": shor,
        "period_readout_illustrative": readout,
    }
    all_ok = (
        c9x["sealed"] and c9x.get("tier") == 0 and c9x.get("n_sys") == 10 and c9x_match
        and all(row["sealed"] and row["tier"] == 0 and row["max_control"] == 9 and "c9x" in row["deps"] for row in cmuls)
        and indep_ok == len(indep)
        and all(children.values())
        and shor["sealed"] and shor["tier"] == 1 and shor["deterministic_reassembly"]
        and readout["order_r"] == 14 and readout.get("factors") == [3, 127]
    )
    report["all_ok"] = bool(all_ok)
    out_path = os.path.join(OUT, "C9X-SHOR381-FRONTIER-REPORT.json")
    json.dump(report, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("-" * 84)
    print(f"all_ok={all_ok} -> .pgf/arith/C9X-SHOR381-FRONTIER-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
