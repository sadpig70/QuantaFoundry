# -*- coding: utf-8 -*-
"""
shor221_frontier.py — W12.7 Shor221StructuralFrontier

c8x payoff to a full Shor-style structural frontier:
N=221=13*17, a=2, counting t=8, work=8.

Sealed apps:
  Tier-0: cmul{2,4,16,35,120}_mod221
  Tier-1: shor221 (16q structural composition)

Honesty boundary:
  - controlled multipliers are Tier-0 EXACT permutation app seals.
  - shor221 is Tier-1 STRUCTURAL; no dense whole-unitary equivalence is claimed.
  - period/factor readout is illustrative only, not seal evidence.
  - N>=256 remains blocked until c9x or another 9-control strategy is sealed.

Usage: python scripts/shor221_frontier.py
"""
from __future__ import annotations

import json
import math
import os
import sys
from collections import Counter
from math import gcd

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, ORACLE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import app_assemble as aa  # noqa: E402  (QPGF app seal primitives, use only)
import verify_seal as vs  # noqa: E402  (hash_unitary/finalize path, use only)
import genskills as gs    # noqa: E402  (c8x-enabled modular synthesis)

SPECS_APPS = os.path.join(ROOT, "specs", "apps")
APPREG = os.path.join(ROOT, "registry", "apps")
MODREG = os.path.join(ROOT, "registry", "modules")
OUT = os.path.join(ROOT, ".pgf", "arith")

N = 221
A = 2
T = 8
WORK = math.ceil(math.log2(N))
NQ = WORK + 1
POWA = [pow(A, 1 << (T - 1 - q), N) for q in range(T)]
UNIQUE_POWERS = sorted(set(POWA) - {1})

_MCT_SET = {"x_gate", "cnot", "toffoli", "c3x", "c4x", "c5x", "c6x", "c7x", "c8x"}


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


def _wire_mask(wire: int, nq: int) -> int:
    return 1 << (nq - 1 - wire)


def _simulate_mct_plan(gates: list[tuple[tuple[int, ...], int]], nq: int) -> list[int]:
    """Compose a pure-MCT plan exactly on every basis state."""
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
    """Fast Tier-0 exact path for permutation-only MCT app plans.

    This performs the full-basis C-app check in permutation space, then emits the
    same deterministic QPGF app seal fields. It avoids dense matrix multiplication
    through hundreds of 9q MCT steps.
    """
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
    if maxc != 8 or "c8x" not in deps:
        raise RuntimeError(f"cmul{a}_mod{N} did not exercise c8x: deps={deps}, maxc={maxc}")
    spec_path = os.path.join(SPECS_APPS, f"cmul{a}_mod{N}.app.pg")
    with open(spec_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(spec)
    seal_path = os.path.join(APPREG, f"cmul{a}_mod{N}.sealed.json")
    if os.path.exists(seal_path):
        sealed = json.load(open(seal_path, encoding="utf-8"))
        verdict = {
            "sealed": bool(sealed.get("sealed")),
            "tier": sealed.get("tier"),
            "u_hash": sealed.get("u_hash"),
            "resource": sealed.get("resource", {}),
            "reason": "cached",
        }
    else:
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


def _shor221_spec() -> tuple[str, int]:
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
        f"# shor221 — Shor period-finding frontier (N={N}={'*'.join(map(str, _factor(N)))}, a={A}). "
        f"{n_sys}q: counting c0..c{T-1}({T}) | work w0..w{WORK-1}({WORK}). "
        f"H^{T} · controlled-U^(2^j)(U=×{A} mod {N}, powa={POWA}) · iqft8. "
        "16q>EXACT_BOUND -> Tier-1 STRUCTURAL(Merkle of sealed components, no dense whole-unitary claim). "
        "Readout illustrative: ord_221(2)=24 -> gcd(2^12±1,221)=13,17.\n"
    )
    return (
        header
        + "```json id=app_meta\n"
        + json.dumps({"id": "shor221", "n_sys": n_sys, "n_anc": 0})
        + "\n```\n"
        + "```json id=plan\n"
        + json.dumps(plan)
        + "\n```\n"
    ), n_sys


def _assemble_shor221() -> dict:
    spec, n_sys = _shor221_spec()
    spec_path = os.path.join(SPECS_APPS, "shor221.app.pg")
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
    sealed_out = aa._seal_dict("shor221", n_sys, "C1-C4(structural)", u_hash, resource, 1)
    aa.Registry(APPREG)._admit(sealed_out)
    sealed_disk = json.load(open(os.path.join(APPREG, "shor221.sealed.json"), encoding="utf-8"))
    u_hash2 = aa._structural_hash(children, n_sys)
    deterministic = u_hash == u_hash2 == sealed_disk["u_hash"]
    return {
        "id": "shor221",
        "n_sys": n_sys,
        "sealed": bool(sealed_disk.get("sealed")),
        "tier": sealed_disk.get("tier"),
        "u_hash": sealed_disk.get("u_hash"),
        "reason": "fast_structural_child_seals",
        "contract": sealed_disk.get("contract"),
        "deterministic_reassembly": deterministic,
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
    print("W12.7 Shor221StructuralFrontier — N=221=13*17, c8x-enabled Shor frontier.")
    print("정직성: cmul powers=Tier-0 EXACT permutation seals, shor221=Tier-1 STRUCTURAL.")
    print("=" * 84)
    print(f"[Target] N={N} factors={_factor(N)} a={A} powa={POWA}, unique={UNIQUE_POWERS}")

    cmuls = []
    for mul in UNIQUE_POWERS:
        rec = _seal_cmul(mul)
        cmuls.append(rec)
        print(
            f"[Cmul] {rec['id']:14} sealed={rec['sealed']} tier={rec['tier']} "
            f"gates={rec['gate_count']} maxc={rec['max_control']} c8={rec['control_dist'].get(8, 0)} "
            f"u={str(rec['u_hash'])[:14]}"
        )

    indep = [_independent_cmul_hash(mul) for mul in UNIQUE_POWERS]
    indep_ok = sum(1 for row in indep if row["matches_sealed"])
    print(f"[IndependentArith] {indep_ok}/{len(indep)} u_hash matches sealed")

    children = _children_sealed()
    print(f"[Children] {children}")
    shor = _assemble_shor221()
    print(
        f"[Shor221] sealed={shor['sealed']} tier={shor['tier']} n_sys={shor['n_sys']} "
        f"u={str(shor['u_hash'])[:16]} deterministic={shor['deterministic_reassembly']}"
    )

    readout = _period_readout()
    print(
        f"[Readout|illustrative] ord_{N}({A})={readout['order_r']} -> "
        f"2^{readout['order_r']//2} mod {N}={readout.get('a_r2')} -> factors={readout.get('factors')}"
    )

    report = {
        "phase": "W12.7 Shor221StructuralFrontier",
        "honesty": "N=221=13*17 is the first Shor-scale payoff after c8x. "
                   "cmul powers are Tier-0 exact permutation app seals; shor221 is Tier-1 structural, "
                   "weaker than dense unitary equivalence; period readout is illustrative only. "
                   "N>=256 remains blocked until c9x or another 9-control strategy is sealed.",
        "target": {"N": N, "a": A, "factors": _factor(N), "counting_t": T, "work": WORK,
                   "powa": POWA, "unique_powers": UNIQUE_POWERS},
        "cmul_apps": cmuls,
        "independent_arith_verify": indep,
        "children_sealed": children,
        "shor221": shor,
        "period_readout_illustrative": readout,
    }
    all_ok = (
        all(row["sealed"] and row["tier"] == 0 and row["max_control"] == 8 and "c8x" in row["deps"] for row in cmuls)
        and indep_ok == len(indep)
        and all(children.values())
        and shor["sealed"] and shor["tier"] == 1 and shor["deterministic_reassembly"]
        and readout["order_r"] == 24 and readout.get("factors") == [13, 17]
    )
    report["all_ok"] = bool(all_ok)
    out_path = os.path.join(OUT, "SHOR-FRONTIER-221-REPORT.json")
    json.dump(report, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("-" * 84)
    print(f"all_ok={all_ok} -> .pgf/arith/SHOR-FRONTIER-221-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
