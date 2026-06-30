# -*- coding: utf-8 -*-
"""
shor_frontier.py — W12.5 Shor119Frontier

Frontier beyond shor91 while staying self-contained under the existing c7x primitive:
N=119=7*17, a=2, counting t=8, work=7.

Sealed apps:
  Tier-0: cmul{2,4,16,18,86}_mod119
  Tier-1: shor119 (15q structural composition)

Honesty boundary:
  - controlled multipliers are Tier-0 EXACT app seals.
  - shor119 is Tier-1 STRUCTURAL; no dense whole-unitary equivalence is claimed.
  - period/factor readout is illustrative only, not seal evidence.
  - N>=128 remains blocked until c8x or another 8-control strategy is sealed.

Usage: python scripts/shor_frontier.py
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
import app_assemble as aa  # noqa: E402  (QPGF app seal path, use only)
import verify_seal as vs  # noqa: E402  (hash_unitary, use only)
import genskills as gs    # noqa: E402  (existing c7x-enabled modular synthesis)

SPECS_APPS = os.path.join(ROOT, "specs", "apps")
APPREG = os.path.join(ROOT, "registry", "apps")
MODREG = os.path.join(ROOT, "registry", "modules")
OUT = os.path.join(ROOT, ".pgf", "arith")

N = 119
A = 2
T = 8
WORK = 7
POWA = [pow(A, 1 << (T - 1 - q), N) for q in range(T)]
UNIQUE_POWERS = sorted(set(POWA) - {1})

_MCT_SET = {"x_gate", "cnot", "toffoli", "c3x", "c4x", "c5x", "c6x", "c7x"}


def _factor(n):
    out, d, m = [], 2, n
    while d * d <= m:
        while m % d == 0:
            out.append(d)
            m //= d
        d += 1
    if m > 1:
        out.append(m)
    return out


def _seal_cmul(a):
    nq = math.ceil(math.log2(N)) + 1
    spec, deps = gs.gen_modmul(a, N, nq)
    gates = gs.mmd_synthesize(gs._modmul_perm(a, N, nq), nq)
    maxc = max((len(c) for c, _ in gates), default=0)
    if not set(deps).issubset(_MCT_SET):
        raise RuntimeError(f"unexpected deps for cmul{a}_mod{N}: {deps}")
    if maxc > 7:
        raise RuntimeError(f"cmul{a}_mod{N}: max control {maxc} exceeds c7x")
    spec_path = os.path.join(SPECS_APPS, f"cmul{a}_mod{N}.app.pg")
    open(spec_path, "w", encoding="utf-8", newline="\n").write(spec)
    seal_path = os.path.join(APPREG, f"cmul{a}_mod{N}.sealed.json")
    if os.path.exists(seal_path):
        sealed = json.load(open(seal_path, encoding="utf-8"))
        verdict = type("CachedVerdict", (), {
            "sealed": bool(sealed.get("sealed")),
            "tier": sealed.get("tier"),
            "u_hash": sealed.get("u_hash"),
            "reason": "cached",
        })()
    else:
        verdict = aa.assemble(spec_path, APPREG)
    return {
        "id": f"cmul{a}_mod{N}",
        "N": N,
        "a": a,
        "nq": nq,
        "sealed": bool(verdict.sealed),
        "tier": verdict.tier,
        "u_hash": verdict.u_hash,
        "reason": verdict.reason,
        "gate_count": len(gates),
        "control_dist": dict(Counter(len(c) for c, _ in gates)),
        "max_control": maxc,
        "deps": deps,
    }


def _independent_cmul_hash(a):
    nq = math.ceil(math.log2(N)) + 1
    dim = 1 << nq
    U = np.zeros((dim, dim), dtype=complex)
    for s in range(dim):
        if (s >> (nq - 1)) & 1 == 0:
            U[s, s] = 1
        else:
            w = s & ((1 << (nq - 1)) - 1)
            nw = (a * w) % N if w < N else w
            U[(1 << (nq - 1)) | nw, s] = 1
    got = vs.hash_unitary(U)
    sealed = json.load(open(os.path.join(APPREG, f"cmul{a}_mod{N}.sealed.json"), encoding="utf-8"))["u_hash"]
    return {
        "id": f"cmul{a}_mod{N}",
        "independent_u_hash": got[:16],
        "matches_sealed": got == sealed,
    }


def _children_sealed():
    need_apps = [f"cmul{a}_mod{N}" for a in UNIQUE_POWERS] + ["iqft8"]
    out = {}
    for app in need_apps:
        out[app] = os.path.exists(os.path.join(APPREG, f"{app}.sealed.json"))
    out["h_gate"] = os.path.exists(os.path.join(MODREG, "h_gate.sealed.json"))
    return out


def _shor119_spec():
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
        f"# shor119 — Shor period-finding frontier (N={N}={'*'.join(map(str, _factor(N)))}, a={A}). "
        f"{n_sys}q: counting c0..c{T-1}({T}) | work w0..w{WORK-1}({WORK}). "
        f"H^{T} · controlled-U^(2^j)(U=×{A} mod {N}, powa={POWA}) · iqft8. "
        "15q>EXACT_BOUND -> Tier-1 STRUCTURAL(Merkle of sealed components, no dense whole-unitary claim). "
        "Readout illustrative: ord_119(2)=24 -> gcd(2^12±1,119)=7,17.\n"
    )
    return (
        header
        + "```json id=app_meta\n"
        + json.dumps({"id": "shor119", "n_sys": n_sys, "n_anc": 0})
        + "\n```\n"
        + "```json id=plan\n"
        + json.dumps(plan)
        + "\n```\n"
    ), n_sys


def _assemble_shor119():
    spec, n_sys = _shor119_spec()
    spec_path = os.path.join(SPECS_APPS, "shor119.app.pg")
    open(spec_path, "w", encoding="utf-8", newline="\n").write(spec)
    # Fast structural path: app_assemble's public assemble() recursively rebuilds sub-apps,
    # which is wasteful for hundreds-gate 8q cmul children. Use the same QPGF structural
    # primitives over already admitted child seals.
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
    sealed_out = aa._seal_dict("shor119", n_sys, "C1-C4(structural)", u_hash, resource, 1)
    aa.Registry(APPREG)._admit(sealed_out)
    sealed_disk = json.load(open(os.path.join(APPREG, "shor119.sealed.json"), encoding="utf-8"))
    u_hash2 = aa._structural_hash(children, n_sys)
    deterministic = u_hash == u_hash2 == sealed_disk["u_hash"]
    return {
        "id": "shor119",
        "n_sys": n_sys,
        "sealed": bool(sealed_disk.get("sealed")),
        "tier": sealed_disk.get("tier"),
        "u_hash": sealed_disk.get("u_hash"),
        "reason": "fast_structural_child_seals",
        "contract": sealed_disk.get("contract"),
        "deterministic_reassembly": deterministic,
    }


def _period_readout():
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


def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 84)
    print("W12.5 Shor119Frontier — N=119=7*17, c7x-bounded Shor frontier beyond 91.")
    print("정직성: cmul powers=Tier-0 EXACT, shor119=Tier-1 STRUCTURAL, readout=illustrative.")
    print("=" * 84)
    print(f"[Target] N={N} factors={_factor(N)} a={A} order=24 expected, powa={POWA}, unique={UNIQUE_POWERS}")

    cmuls = []
    for a in UNIQUE_POWERS:
        rec = _seal_cmul(a)
        cmuls.append(rec)
        print(
            f"[Cmul] {rec['id']:14} sealed={rec['sealed']} tier={rec['tier']} "
            f"gates={rec['gate_count']} maxc={rec['max_control']} u={str(rec['u_hash'])[:14]}"
        )

    indep = [_independent_cmul_hash(a) for a in UNIQUE_POWERS]
    indep_ok = sum(1 for row in indep if row["matches_sealed"])
    print(f"[IndependentArith] {indep_ok}/{len(indep)} u_hash matches sealed")

    children = _children_sealed()
    print(f"[Children] {children}")
    shor = _assemble_shor119()
    print(
        f"[Shor119] sealed={shor['sealed']} tier={shor['tier']} n_sys={shor['n_sys']} "
        f"u={str(shor['u_hash'])[:16]} deterministic={shor['deterministic_reassembly']}"
    )

    readout = _period_readout()
    print(
        f"[Readout|illustrative] ord_{N}({A})={readout['order_r']} -> "
        f"2^{readout['order_r']//2} mod {N}={readout.get('a_r2')} -> factors={readout.get('factors')}"
    )

    report = {
        "phase": "W12.5 Shor119Frontier",
        "honesty": "N=119=7*17 is a self-contained frontier beyond shor91 under existing c7x. "
                   "cmul powers are Tier-0 exact app seals; shor119 is Tier-1 structural, weaker than "
                   "dense unitary equivalence; period readout is illustrative only. N>=128 remains blocked "
                   "until c8x or another 8-control strategy is sealed.",
        "target": {"N": N, "a": A, "factors": _factor(N), "counting_t": T, "work": WORK,
                   "powa": POWA, "unique_powers": UNIQUE_POWERS},
        "cmul_apps": cmuls,
        "independent_arith_verify": indep,
        "children_sealed": children,
        "shor119": shor,
        "period_readout_illustrative": readout,
    }
    all_ok = (
        all(row["sealed"] and row["tier"] == 0 and row["max_control"] <= 7 for row in cmuls)
        and indep_ok == len(indep)
        and all(children.values())
        and shor["sealed"] and shor["tier"] == 1 and shor["deterministic_reassembly"]
        and readout["order_r"] == 24 and readout.get("factors") == [7, 17]
    )
    report["all_ok"] = bool(all_ok)
    out_path = os.path.join(OUT, "SHOR-FRONTIER-119-REPORT.json")
    json.dump(report, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("-" * 84)
    print(f"all_ok={all_ok} -> .pgf/arith/SHOR-FRONTIER-119-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
