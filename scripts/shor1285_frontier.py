# -*- coding: utf-8 -*-
"""
shor1285_frontier.py - W12.19 Shor1285StructuralFrontier.

Lift the complete c11x payoff family into a Shor-style structural app:
N=1285=5*257, a=2, counting t=8, work=11.

The cmul{2,4,16,256}_mod1285 multiplier family is already sealed Tier-0 exact
by W12.17 (cmul2) and W12.18 (cmul4/16/256). This step does not re-seal them;
it verifies them as sealed children, re-checks each against an independent
arithmetic permutation hash, and assembles the structural Shor app.

Sealed outputs:
  Tier-1 app:  shor1285 (19q structural composition)

Honesty boundary:
  - controlled multipliers are already Tier-0 exact permutation app seals.
  - shor1285 is Tier-1 STRUCTURAL; no dense whole-unitary equivalence is claimed.
  - period/factor readout is illustrative only, not seal evidence.
"""
from __future__ import annotations

import json
import math
import os
import sys
from math import gcd

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, ORACLE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import app_assemble as aa  # noqa: E402
import verify_seal as vs  # noqa: E402

SPECS_APPS = os.path.join(ROOT, "specs", "apps")
APPREG = os.path.join(ROOT, "registry", "apps")
MODREG = os.path.join(ROOT, "registry", "modules")
OUT = os.path.join(ROOT, ".pgf", "arith")

N = 1285
A = 2
T = 8
WORK = math.ceil(math.log2(N))
NQ = WORK + 1
POWA = [pow(A, 1 << (T - 1 - q), N) for q in range(T)]
UNIQUE_POWERS = sorted(set(POWA) - {1})


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


def _independent_cmul_hash(a: int) -> dict:
    """Rebuild the controlled modular-multiplier permutation from arithmetic and
    compare its unitary hash against the already-sealed app (no re-seal)."""
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
    sealed = json.load(open(os.path.join(APPREG, f"cmul{a}_mod{N}.sealed.json"), encoding="utf-8"))
    return {
        "id": f"cmul{a}_mod{N}",
        "tier": sealed.get("tier"),
        "n_sys": sealed.get("n_sys"),
        "independent_u_hash": got[:16],
        "matches_sealed": got == sealed["u_hash"],
    }


def _children_sealed() -> dict[str, bool]:
    need_apps = [f"cmul{a}_mod{N}" for a in UNIQUE_POWERS] + ["iqft8"]
    out = {app: os.path.exists(os.path.join(APPREG, f"{app}.sealed.json")) for app in need_apps}
    out["h_gate"] = os.path.exists(os.path.join(MODREG, "h_gate.sealed.json"))
    return out


def _shor1285_spec() -> tuple[str, int]:
    work = list(range(T, T + WORK))
    steps = [{"spec": "../modules/h_gate.pg", "targets": [q]} for q in range(T)]
    for q, mul in enumerate(POWA):
        if mul != 1:
            steps.append({"app": f"cmul{mul}_mod{N}.app.pg", "targets": [q] + work})
    steps.append({"app": "iqft8.app.pg", "targets": list(range(T))})
    n_sys = T + WORK
    plan = {"tier": "structural", "steps": steps}
    header = (
        f"# shor1285 - Shor period-finding structural frontier (N={N}={'*'.join(map(str, _factor(N)))}, a={A}). "
        f"{n_sys}q: counting={T}, work={WORK}. "
        f"H^{T} controlled-U^(2^j)(powa={POWA}) iqft8. "
        f"{n_sys}q>EXACT_BOUND -> Tier-1 STRUCTURAL only. "
        "Readout illustrative: ord_1285(2)=16 -> gcd(2^8+-1,1285)=5,257.\n"
    )
    return (
        header
        + "```json id=app_meta\n"
        + json.dumps({"id": "shor1285", "n_sys": n_sys, "n_anc": 0})
        + "\n```\n"
        + "```json id=plan\n"
        + json.dumps(plan)
        + "\n```\n"
    ), n_sys


def _assemble_shor1285() -> dict:
    spec, n_sys = _shor1285_spec()
    spec_path = os.path.join(SPECS_APPS, "shor1285.app.pg")
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
    sealed_out = aa._seal_dict("shor1285", n_sys, "C1-C4(structural)", u_hash, resource, 1)
    aa.Registry(APPREG)._admit(sealed_out)
    disk = json.load(open(os.path.join(APPREG, "shor1285.sealed.json"), encoding="utf-8"))
    return {
        "id": "shor1285",
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
    print("W12.19 Shor1285StructuralFrontier - N=1285=5*257, c11x payoff Shor frontier.")
    print("Honesty: cmul family=Tier-0 EXACT (already sealed), shor1285=Tier-1 STRUCTURAL, "
          "readout=illustrative.")
    print("=" * 84)
    print(f"[Target] N={N} factors={_factor(N)} a={A} T={T} WORK={WORK} powa={POWA} unique={UNIQUE_POWERS}")

    indep = [_independent_cmul_hash(mul) for mul in UNIQUE_POWERS]
    indep_ok = sum(1 for row in indep if row["matches_sealed"])
    for row in indep:
        print(f"[IndependentArith] {row['id']:16} tier={row['tier']} n_sys={row['n_sys']} "
              f"matches_sealed={row['matches_sealed']} u={row['independent_u_hash']}")
    print(f"[IndependentArith] {indep_ok}/{len(indep)} u_hash matches sealed")

    children = _children_sealed()
    print(f"[Children] {children}")
    shor = _assemble_shor1285()
    print(
        f"[Shor1285] sealed={shor['sealed']} tier={shor['tier']} n_sys={shor['n_sys']} "
        f"u={str(shor['u_hash'])[:16]} deterministic={shor['deterministic_reassembly']}"
    )

    readout = _period_readout()
    print(
        f"[Readout|illustrative] ord_{N}({A})={readout['order_r']} -> "
        f"2^{readout['order_r']//2} mod {N}={readout.get('a_r2')} -> factors={readout.get('factors')}"
    )

    report = {
        "phase": "W12.19 Shor1285StructuralFrontier",
        "honesty": "N=1285=5*257 is the c11x payoff Shor structural frontier. "
                   "cmul powers are already Tier-0 exact permutation app seals (W12.17/W12.18); "
                   "shor1285 is Tier-1 structural, weaker than dense unitary equivalence; "
                   "period readout is illustrative only.",
        "target": {"N": N, "a": A, "factors": _factor(N), "counting_t": T, "work": WORK,
                   "powa": POWA, "unique_powers": UNIQUE_POWERS},
        "independent_arith_verify": indep,
        "children_sealed": children,
        "shor1285": shor,
        "period_readout_illustrative": readout,
    }
    all_ok = (
        indep_ok == len(indep)
        and all(row["tier"] == 0 for row in indep)
        and all(children.values())
        and shor["sealed"] and shor["tier"] == 1 and shor["deterministic_reassembly"]
        and readout["order_r"] == 16 and readout.get("factors") == [5, 257]
    )
    report["all_ok"] = bool(all_ok)
    out_path = os.path.join(OUT, "SHOR-FRONTIER-1285-REPORT.json")
    json.dump(report, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("-" * 84)
    print(f"all_ok={all_ok} -> .pgf/arith/SHOR-FRONTIER-1285-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
