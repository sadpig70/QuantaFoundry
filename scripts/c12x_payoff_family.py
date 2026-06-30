# -*- coding: utf-8 -*-
"""
c12x_payoff_family.py - W12.22 C12xPayoffFamily.

Seal the remaining N=3683 payoff multipliers unlocked by c12x.

Sealed outputs:
  Tier-0 apps: cmul{4,16,256,2925}_mod3683

Honesty boundary:
  - controlled multipliers are Tier-0 exact permutation app seals.
  - cmul2_mod3683 was sealed in W12.21 and is checked as an existing child.
  - Full Shor-3683 is not claimed here (see W12.23 shor3683_frontier).
"""
from __future__ import annotations

import json
import math
import os
import sys
from collections import Counter

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, ORACLE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import app_assemble as aa  # noqa: E402
import genskills as gs  # noqa: E402
import verify_seal as vs  # noqa: E402

SPECS_APPS = os.path.join(ROOT, "specs", "apps")
APPREG = os.path.join(ROOT, "registry", "apps")
MODREG = os.path.join(ROOT, "registry", "modules")
OUT = os.path.join(ROOT, ".pgf", "arith")

N = 3683
A = 2
T = 8
WORK = math.ceil(math.log2(N))
NQ = WORK + 1
POWA = [pow(A, 1 << (T - 1 - q), N) for q in range(T)]
UNIQUE_POWERS = sorted(set(POWA) - {1})
NEW_POWERS = [p for p in UNIQUE_POWERS if p != 2]

_MCT_SET = {
    "x_gate", "cnot", "toffoli", "c3x", "c4x", "c5x",
    "c6x", "c7x", "c8x", "c9x", "c10x", "c11x", "c12x",
}


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
    if maxc != 12 or "c12x" not in deps:
        raise RuntimeError(f"cmul{a}_mod{N} did not exercise c12x: deps={deps}, maxc={maxc}")
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


def _existing_family_seals() -> dict[str, bool]:
    return {f"cmul{a}_mod{N}": os.path.exists(os.path.join(APPREG, f"cmul{a}_mod{N}.sealed.json"))
            for a in UNIQUE_POWERS}


def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    print("=" * 84)
    print("W12.22 C12xPayoffFamily - remaining N=3683 payoff multipliers.")
    print("Honesty: cmul powers=Tier-0 EXACT, full Shor-3683 deferred (W12.23).")
    print("=" * 84)
    print(f"[Target] N={N} factors={_factor(N)} a={A} T={T} WORK={WORK} powa={POWA} unique={UNIQUE_POWERS}")

    cmuls = []
    for mul in NEW_POWERS:
        rec = _seal_cmul(mul)
        cmuls.append(rec)
        print(
            f"[Cmul] {rec['id']:18} sealed={rec['sealed']} tier={rec['tier']} "
            f"gates={rec['gate_count']} maxc={rec['max_control']} c12={rec['control_dist'].get(12, 0)} "
            f"u={str(rec['u_hash'])[:14]}"
        )

    indep = [_independent_cmul_hash(mul) for mul in NEW_POWERS]
    indep_ok = sum(1 for row in indep if row["matches_sealed"])
    print(f"[IndependentArith] {indep_ok}/{len(indep)} u_hash matches sealed")

    family = _existing_family_seals()
    print(f"[FamilySeals] {family}")
    total_gates = sum(row["gate_count"] for row in cmuls)
    total_c12 = sum(row["control_dist"].get(12, 0) for row in cmuls)

    report = {
        "phase": "W12.22 C12xPayoffFamily",
        "honesty": "N=3683=29*127 payoff family completion. New cmul powers are Tier-0 exact "
                   "permutation app seals; full Shor-3683 remains deferred to W12.23.",
        "target": {"N": N, "a": A, "factors": _factor(N), "counting_t": T, "work": WORK,
                   "powa": POWA, "unique_powers": UNIQUE_POWERS, "new_powers": NEW_POWERS},
        "cmul_apps": cmuls,
        "independent_arith_verify": indep,
        "family_seals": family,
        "totals": {"new_gate_count": total_gates, "new_c12_count": total_c12},
    }
    all_ok = (
        len(cmuls) == 4
        and all(row["sealed"] and row["tier"] == 0 and row["max_control"] == 12 and "c12x" in row["deps"]
                for row in cmuls)
        and indep_ok == len(indep)
        and all(family.values())
    )
    report["all_ok"] = bool(all_ok)
    out_path = os.path.join(OUT, "C12X-PAYOFF-3683-REPORT.json")
    json.dump(report, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("-" * 84)
    print(f"all_ok={all_ok} -> .pgf/arith/C12X-PAYOFF-3683-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
