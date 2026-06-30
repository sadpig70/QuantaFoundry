# -*- coding: utf-8 -*-
"""
frontier_factory.py - Parametric Shor arithmetic frontier sealer.

Generalizes the verified templates c{11,12}x_payoff_family.py + shor{1285,3683}_frontier.py
into N-parameter functions so the autonomy loop can seal an arbitrary distinct-prime N
(cmul payoff family + structural Shor) without hand-writing a generator per N.

This is NOT free code generation. It reuses the exact oracle paths
(genskills.mmd_synthesize / app_assemble._seal_dict / _structural_hash / verify_seal.hash_unitary).
Template correctness is proven deterministically by the regression gate (INV-F1): the factory must
reproduce already-sealed N (1285, 3683, ...) byte-identically before any new N is sealed.

Honesty (inherited): cmul = Tier-0 EXACT permutation app; shor{N} = Tier-1 STRUCTURAL Merkle
(no dense whole-unitary claim); period/factor readout illustrative. Zero new modules
(reuses sealed c8x..c12x primitives).

Usage:
  python scripts/frontier_factory.py --verify-regression          # INV-F1 gate (must pass)
  python scripts/frontier_factory.py --reproduce                  # re-seal all FACTORY-FRONTIER N
  python scripts/frontier_factory.py --seal N [N ...]             # seal new N(s)
  python scripts/frontier_factory.py --resolve N                  # primitive feasibility report
"""
from __future__ import annotations

import argparse
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
import app_assemble as aa  # noqa: E402
import genskills as gs  # noqa: E402
import verify_seal as vs  # noqa: E402

SPECS_APPS = os.path.join(ROOT, "specs", "apps")
APPREG = os.path.join(ROOT, "registry", "apps")
MODREG = os.path.join(ROOT, "registry", "modules")
OUT = os.path.join(ROOT, ".pgf", "arith")
FACTORY_DB = os.path.join(OUT, "FACTORY-FRONTIER.json")

DEFAULT_A = 2
DEFAULT_T = 8

# every MCT module the factory may consume (zero new modules — INV-F2)
_MCT_SET = {
    "x_gate", "cnot", "toffoli", "c3x", "c4x", "c5x",
    "c6x", "c7x", "c8x", "c9x", "c10x", "c11x", "c12x",
}


# ─────────────────────────────────────────────────────────────────────────────
# shared helpers (extracted verbatim from the verified templates)
# ─────────────────────────────────────────────────────────────────────────────
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


def _simulate_mct_plan(gates, nq: int) -> list[int]:
    perm = list(range(1 << nq))
    masks = [(sum(_wire_mask(c, nq) for c in controls), _wire_mask(target, nq))
             for controls, target in gates]
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


def _independent_cmul_uhash(a: int, N: int, nq: int) -> str:
    dim = 1 << nq
    U = np.zeros((dim, dim), dtype=complex)
    for s in range(dim):
        if (s >> (nq - 1)) & 1 == 0:
            U[s, s] = 1
        else:
            w = s & ((1 << (nq - 1)) - 1)
            nw = (a * w) % N if w < N else w
            U[(1 << (nq - 1)) | nw, s] = 1
    return vs.hash_unitary(U)


# ─────────────────────────────────────────────────────────────────────────────
# resolve / payoff / structural  (N-parameterized)
# ─────────────────────────────────────────────────────────────────────────────
def resolve_primitive(N: int, a: int = DEFAULT_A, t: int = DEFAULT_T) -> dict:
    """N → work·nq·unique_powers·max_control; required c{maxc}x existence."""
    work = math.ceil(math.log2(N))
    nq = work + 1
    powa = [pow(a, 1 << (t - 1 - q), N) for q in range(t)]
    unique = sorted(set(powa) - {1})
    maxc = 0
    deps_all = set()
    synthesizable = True
    for mul in unique:
        try:
            gates = gs.mmd_synthesize(gs._modmul_perm(mul, N, nq), nq)
        except Exception:  # noqa: BLE001  # genskills 합성 한계(f≠identity 등) → 비가용으로 정직 처리
            synthesizable = False
            break
        maxc = max(maxc, max((len(c) for c, _ in gates), default=0))
        deps_all |= {gs._MCT_MODULE[len(c)] for c, _ in gates}
    prim = gs._MCT_MODULE.get(maxc)
    prim_ok = (synthesizable and prim is not None
               and os.path.exists(os.path.join(MODREG, f"{prim}.sealed.json"))
               and deps_all.issubset(_MCT_SET)
               and all(os.path.exists(os.path.join(MODREG, f"{d}.sealed.json")) for d in deps_all))
    return {"N": N, "a": a, "t": t, "work": work, "nq": nq, "powa": powa,
            "factors": _factor(N), "unique_powers": unique, "max_control": maxc,
            "primitive": prim, "primitive_ok": bool(prim_ok), "synthesizable": synthesizable,
            "deps": sorted(deps_all)}


def _seal_exact_permutation_app(app_id: str, nq: int, gates, target_perm) -> dict:
    plan_perm = _simulate_mct_plan(gates, nq)
    if plan_perm != list(target_perm):
        raise RuntimeError(f"{app_id}: MCT plan permutation does not match arithmetic golden")
    u_hash = _perm_hash(plan_perm)
    resources = []
    for controls, _ in gates:
        mid = gs._MCT_MODULE[len(controls)]
        resources.append(json.load(open(os.path.join(MODREG, f"{mid}.sealed.json"),
                                         encoding="utf-8"))["resource"])
    resource = aa._aggregate_cost(resources)
    sealed = aa._seal_dict(app_id, nq, "C1-C4(app)", u_hash, resource, 0)
    aa.Registry(APPREG)._admit(sealed)
    disk = json.load(open(os.path.join(APPREG, f"{app_id}.sealed.json"), encoding="utf-8"))
    return {"sealed": bool(disk.get("sealed")), "tier": disk.get("tier"),
            "u_hash": disk.get("u_hash"), "resource": disk.get("resource", {})}


def seal_payoff_family(meta: dict, only_new: bool = True, write_specs: bool = True) -> list[dict]:
    """cmul{unique_powers}_mod{N} Tier-0 exact (generalized c11x_payoff_family)."""
    N, a, nq = meta["N"], meta["a"], meta["nq"]
    recs = []
    for mul in meta["unique_powers"]:
        app_id = f"cmul{mul}_mod{N}"
        seal_path = os.path.join(APPREG, f"{app_id}.sealed.json")
        if only_new and os.path.exists(seal_path):
            recs.append({"id": app_id, "sealed": True, "skipped": "exists"})
            continue
        spec, deps = gs.gen_modmul(mul, N, nq)
        if not set(deps).issubset(_MCT_SET):
            raise RuntimeError(f"unexpected deps for {app_id}: {deps}")
        gates = gs.mmd_synthesize(gs._modmul_perm(mul, N, nq), nq)
        maxc = max((len(c) for c, _ in gates), default=0)
        if write_specs:
            with open(os.path.join(SPECS_APPS, f"{app_id}.app.pg"), "w",
                      encoding="utf-8", newline="\n") as f:
                f.write(spec)
        v = _seal_exact_permutation_app(app_id, nq, gates, gs._modmul_perm(mul, N, nq))
        indep = _independent_cmul_uhash(mul, N, nq)
        recs.append({"id": app_id, "a": mul, "sealed": bool(v["sealed"]), "tier": v["tier"],
                     "u_hash": v["u_hash"], "gate_count": len(gates), "max_control": maxc,
                     "control_dist": dict(Counter(len(c) for c, _ in gates)),
                     "independent_match": indep == v["u_hash"], "deps": deps})
    return recs


def _structural_spec(meta: dict) -> tuple[str, int, dict]:
    N, a, t, work = meta["N"], meta["a"], meta["t"], meta["work"]
    powa = meta["powa"]
    work_wires = list(range(t, t + work))
    steps = [{"spec": "../modules/h_gate.pg", "targets": [q]} for q in range(t)]
    for q, mul in enumerate(powa):
        if mul != 1:
            steps.append({"app": f"cmul{mul}_mod{N}.app.pg", "targets": [q] + work_wires})
    steps.append({"app": f"iqft{t}.app.pg", "targets": list(range(t))})
    n_sys = t + work
    plan = {"tier": "structural", "steps": steps}
    header = (
        f"# shor{N} - Shor period-finding structural frontier "
        f"(N={N}={'*'.join(map(str, meta['factors']))}, a={a}). "
        f"{n_sys}q: counting={t}, work={work}. H^{t} controlled-U^(2^j)(powa={powa}) iqft{t}. "
        f"{n_sys}q>EXACT_BOUND -> Tier-1 STRUCTURAL only.\n"
    )
    spec = (header
            + "```json id=app_meta\n" + json.dumps({"id": f"shor{N}", "n_sys": n_sys, "n_anc": 0})
            + "\n```\n```json id=plan\n" + json.dumps(plan) + "\n```\n")
    return spec, n_sys, plan


def _structural_children(plan: dict, n_sys: int) -> list[dict]:
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
        elif (len(targets) != width or len(set(targets)) != len(targets)
              or any(t < 0 or t >= n_sys for t in targets)):
            raise RuntimeError(f"interface mismatch for {cid}: targets={targets}, width={width}")
        children.append({"u_hash": sealed["u_hash"], "resource": sealed["resource"],
                         "targets": targets, "n_qubits": width})
    return children


def seal_structural_shor(meta: dict, write_spec: bool = True) -> dict:
    """shor{N} Tier-1 structural Merkle (generalized shor1285_frontier)."""
    N = meta["N"]
    spec, n_sys, plan = _structural_spec(meta)
    if write_spec:
        with open(os.path.join(SPECS_APPS, f"shor{N}.app.pg"), "w",
                  encoding="utf-8", newline="\n") as f:
            f.write(spec)
    children = _structural_children(plan, n_sys)
    resource = aa._aggregate_cost([c["resource"] for c in children])
    u_hash = aa._structural_hash(children, n_sys)
    sealed_out = aa._seal_dict(f"shor{N}", n_sys, "C1-C4(structural)", u_hash, resource, 1)
    aa.Registry(APPREG)._admit(sealed_out)
    disk = json.load(open(os.path.join(APPREG, f"shor{N}.sealed.json"), encoding="utf-8"))
    return {"id": f"shor{N}", "n_sys": n_sys, "sealed": bool(disk.get("sealed")),
            "tier": disk.get("tier"), "u_hash": disk.get("u_hash"),
            "deterministic_reassembly": u_hash == aa._structural_hash(children, n_sys) == disk["u_hash"]}


def _period_readout(N: int, a: int) -> dict:
    r, x = 1, a % N
    while x != 1:
        x = (x * a) % N
        r += 1
    res = {"a": a, "N": N, "order_r": r, "r_even": r % 2 == 0}
    if r % 2 == 0:
        h = pow(a, r // 2, N)
        res["a_r2"] = h
        res["factors"] = sorted({gcd(h - 1, N), gcd(h + 1, N)} - {1, N})
    res["note"] = "illustrative only; not seal evidence"
    return res


# ─────────────────────────────────────────────────────────────────────────────
# factory_seal / regression / DB
# ─────────────────────────────────────────────────────────────────────────────
def is_distinct_semiprime(n: int) -> bool:
    f = _factor(n)
    return len(f) == 2 and f[0] != f[1]


def next_unsealed_target(lo: int = 33, hi: int = 4096, a: int = DEFAULT_A, t: int = DEFAULT_T):
    """결정론적 자율 발견: 가장 작은 distinct-semiprime · 미봉인 shor{N} · structural-eligible
    (n_sys≥15) · primitive_ok · readout-valid N 을 반환. 없으면 (None, None) (frontier-exhausted)."""
    for N in range(lo, hi):
        if not is_distinct_semiprime(N) or gcd(a, N) != 1:
            continue
        if os.path.exists(os.path.join(APPREG, f"shor{N}.sealed.json")):
            continue
        m = resolve_primitive(N, a, t)
        if m["t"] + m["work"] >= 15 and m["primitive_ok"]:
            r = _period_readout(N, a)
            if r.get("factors") and len(r["factors"]) == 2:
                return N, m
    return None, None


def _load_db() -> dict:
    if os.path.exists(FACTORY_DB):
        return json.load(open(FACTORY_DB, encoding="utf-8"))
    return {"schema": "factory-frontier/v1", "sealed_N": []}


def _register_N(N: int, meta: dict) -> None:
    db = _load_db()
    entry = {"N": N, "a": meta["a"], "t": meta["t"], "factors": meta["factors"],
             "work": meta["work"], "nq": meta["nq"], "max_control": meta["max_control"],
             "primitive": meta["primitive"], "unique_powers": meta["unique_powers"]}
    by_n = {e["N"]: e for e in db["sealed_N"]}
    by_n[N] = entry
    db["sealed_N"] = [by_n[k] for k in sorted(by_n)]
    os.makedirs(OUT, exist_ok=True)
    json.dump(db, open(FACTORY_DB, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def factory_seal(N: int, a: int = DEFAULT_A, t: int = DEFAULT_T) -> dict:
    meta = resolve_primitive(N, a, t)
    # honesty (INV-F4): structural Merkle only above the dense-exact ceiling. n_sys=t+work.
    # shor91 (15q, work=7) is the first structural seal; smaller n_sys belongs to dense-exact path.
    if meta["t"] + meta["work"] < 15:
        return {"N": N, "sealed": False, "reason": "too-small-for-structural",
                "n_sys": meta["t"] + meta["work"], "meta": meta}
    if not meta["primitive_ok"]:
        return {"N": N, "sealed": False, "reason": "primitive-missing",
                "needs": meta["primitive"], "max_control": meta["max_control"], "meta": meta}
    iqft = os.path.join(APPREG, f"iqft{t}.sealed.json")
    if not os.path.exists(iqft):
        return {"N": N, "sealed": False, "reason": f"iqft{t}-missing", "meta": meta}
    payoff = seal_payoff_family(meta)
    if not all(r["sealed"] for r in payoff):
        return {"N": N, "sealed": False, "reason": "payoff-failed", "payoff": payoff, "meta": meta}
    if not all(r.get("independent_match", True) for r in payoff):
        return {"N": N, "sealed": False, "reason": "independent-arith-mismatch",
                "payoff": payoff, "meta": meta}
    shor = seal_structural_shor(meta)
    if not (shor["sealed"] and shor["tier"] == 1 and shor["deterministic_reassembly"]):
        return {"N": N, "sealed": False, "reason": "structural-failed", "shor": shor, "meta": meta}
    _register_N(N, meta)
    return {"N": N, "sealed": True, "meta": meta, "payoff": payoff, "shor": shor,
            "readout": _period_readout(N, a)}


def verify_against_sealed(N: int, a: int = DEFAULT_A, t: int = DEFAULT_T) -> dict:
    """INV-F1 regression: recompute u_hash from factory logic; compare to disk seal (no re-admit)."""
    meta = resolve_primitive(N, a, t)
    rows = []
    ok = True
    for mul in meta["unique_powers"]:
        app_id = f"cmul{mul}_mod{N}"
        disk_path = os.path.join(APPREG, f"{app_id}.sealed.json")
        if not os.path.exists(disk_path):
            rows.append({"id": app_id, "present": False})
            ok = False
            continue
        gates = gs.mmd_synthesize(gs._modmul_perm(mul, N, meta["nq"]), meta["nq"])
        recomputed = _perm_hash(_simulate_mct_plan(gates, meta["nq"]))
        disk = json.load(open(disk_path, encoding="utf-8"))["u_hash"]
        match = recomputed == disk
        ok &= match
        rows.append({"id": app_id, "present": True, "byte_identical": match})
    shor_path = os.path.join(APPREG, f"shor{N}.sealed.json")
    shor_row = {"id": f"shor{N}", "present": os.path.exists(shor_path)}
    if shor_row["present"]:
        _, n_sys, plan = _structural_spec(meta)
        children = _structural_children(plan, n_sys)
        recomputed = aa._structural_hash(children, n_sys)
        disk = json.load(open(shor_path, encoding="utf-8"))["u_hash"]
        shor_row["byte_identical"] = recomputed == disk
        ok &= shor_row["byte_identical"]
    else:
        ok = False
    rows.append(shor_row)
    return {"N": N, "byte_identical_all": bool(ok), "rows": rows}


# ─────────────────────────────────────────────────────────────────────────────
# CLI modes
# ─────────────────────────────────────────────────────────────────────────────
REGRESSION_N = [91, 119, 221, 381, 635, 1285, 3683]


def _run_regression() -> int:
    results = [verify_against_sealed(N) for N in REGRESSION_N]
    all_ok = all(r["byte_identical_all"] for r in results)
    report = {"phase": "FrontierFactory regression (INV-F1)",
              "honesty": "Factory must reproduce sealed N byte-identically before sealing any new N.",
              "results": results, "all_ok": bool(all_ok)}
    os.makedirs(OUT, exist_ok=True)
    json.dump(report, open(os.path.join(OUT, "FACTORY-REGRESSION.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("=" * 84)
    print("FrontierFactory regression gate (INV-F1) — factory u_hash == sealed u_hash")
    print("=" * 84)
    for r in results:
        print(f"  N={r['N']:5} byte_identical_all={r['byte_identical_all']}")
    print("-" * 84)
    print(f"all_ok={all_ok}")
    return 0 if all_ok else 1


def _run_reproduce() -> int:
    db = _load_db()
    ns = [e["N"] for e in db["sealed_N"]]
    if not ns:
        print("frontier_factory --reproduce: no factory N registered yet. all_ok=True")
        return 0
    ok = True
    for N in ns:
        meta = resolve_primitive(N)
        seal_payoff_family(meta, only_new=False)
        shor = seal_structural_shor(meta)
        v = verify_against_sealed(N)
        ok &= shor["sealed"] and v["byte_identical_all"]
        print(f"  reproduce N={N} sealed={shor['sealed']} byte_identical={v['byte_identical_all']}")
    print(f"all_ok={ok}")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Parametric Shor frontier factory")
    ap.add_argument("--verify-regression", action="store_true")
    ap.add_argument("--reproduce", action="store_true")
    ap.add_argument("--resolve", type=int, default=None)
    ap.add_argument("--seal", type=int, nargs="+", default=None)
    args = ap.parse_args()

    if args.verify_regression:
        return _run_regression()
    if args.reproduce:
        return _run_reproduce()
    if args.resolve is not None:
        print(json.dumps(resolve_primitive(args.resolve), ensure_ascii=False, indent=2))
        return 0
    if args.seal:
        # safety: regression must pass before sealing any new N (INV-F1)
        if _run_regression() != 0:
            print("ABORT: regression gate failed — refusing to seal new N (INV-F1)")
            return 1
        rc = 0
        for N in args.seal:
            res = factory_seal(N)
            print(f"[seal] N={N} sealed={res['sealed']} reason={res.get('reason', 'ok')}")
            rc |= 0 if res["sealed"] else 1
        return rc
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
