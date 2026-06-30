# -*- coding: utf-8 -*-
"""
shor_structural_generalizer.py - W12.12 reusable structural Shor assembler.

Report-only helper. It can build a structural Shor app spec from (N, a, t) and
verify that the already-sealed shor119/shor221/shor381 structural hashes are
reproducible from their committed plans.
"""
from __future__ import annotations

import json
import math
import os
import sys
from math import gcd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, ORACLE)
import app_assemble as aa  # noqa: E402

SPECS_APPS = os.path.join(ROOT, "specs", "apps")
MODREG = os.path.join(ROOT, "registry", "modules")
APPREG = os.path.join(ROOT, "registry", "apps")
OUT = os.path.join(ROOT, ".pgf", "arith")


def factor(n: int) -> list[int]:
    out, d, m = [], 2, n
    while d * d <= m:
        while m % d == 0:
            out.append(d)
            m //= d
        d += 1
    if m > 1:
        out.append(m)
    return out


def multiplicative_order(a: int, n: int) -> int:
    r, x = 1, a % n
    while x != 1:
        x = (x * a) % n
        r += 1
    return r


def build_shor_plan(n: int, a: int, t: int = 8) -> dict:
    work = math.ceil(math.log2(n))
    work_targets = list(range(t, t + work))
    powa = [pow(a, 1 << (t - 1 - q), n) for q in range(t)]
    steps = [{"spec": "../modules/h_gate.pg", "targets": [q]} for q in range(t)]
    for q, mul in enumerate(powa):
        if mul != 1:
            steps.append({"app": f"cmul{mul}_mod{n}.app.pg", "targets": [q] + work_targets})
    steps.append({"app": f"iqft{t}.app.pg", "targets": list(range(t))})
    return {"tier": "structural", "steps": steps}


def build_shor_spec(app_id: str, n: int, a: int, t: int = 8) -> str:
    work = math.ceil(math.log2(n))
    n_sys = t + work
    powa = [pow(a, 1 << (t - 1 - q), n) for q in range(t)]
    r = multiplicative_order(a, n)
    readout = ""
    if r % 2 == 0:
        h = pow(a, r // 2, n)
        fs = sorted({gcd(h - 1, n), gcd(h + 1, n)} - {1, n})
        readout = f" Readout illustrative: ord_{n}({a})={r} -> factors={fs}."
    header = (
        f"# {app_id} - generalized Shor structural app (N={n}={'*'.join(map(str, factor(n)))}, a={a}). "
        f"{n_sys}q: counting={t}, work={work}. H^{t} controlled-U^(2^j)(powa={powa}) iqft{t}. "
        f"{n_sys}q>EXACT_BOUND -> Tier-1 STRUCTURAL only.{readout}\n"
    )
    return (
        header
        + "```json id=app_meta\n"
        + json.dumps({"id": app_id, "n_sys": n_sys, "n_anc": 0})
        + "\n```\n"
        + "```json id=plan\n"
        + json.dumps(build_shor_plan(n, a, t))
        + "\n```\n"
    )


def _extract_plan(spec_path: str) -> tuple[dict, dict]:
    txt = open(spec_path, encoding="utf-8").read()
    meta = json.loads(txt.split("```json id=app_meta\n", 1)[1].split("```", 1)[0])
    plan = json.loads(txt.split("```json id=plan\n", 1)[1].split("```", 1)[0])
    return meta, plan


def structural_hash_from_plan(meta: dict, plan: dict) -> dict:
    n_sys = meta["n_sys"]
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
                raise RuntimeError(f"{meta['id']}: {cid} width {width} requires targets")
        elif len(targets) != width or len(set(targets)) != len(targets) or any(t < 0 or t >= n_sys for t in targets):
            raise RuntimeError(f"{meta['id']}: invalid targets for {cid}: {targets}")
        children.append({"u_hash": sealed["u_hash"], "resource": sealed["resource"],
                         "targets": targets, "n_qubits": width})
    return {
        "u_hash": aa._structural_hash(children, n_sys),
        "resource": aa._aggregate_cost([c["resource"] for c in children]),
        "child_count": len(children),
    }


def verify_existing(app_id: str, n: int, a: int, t: int = 8) -> dict:
    spec_path = os.path.join(SPECS_APPS, f"{app_id}.app.pg")
    meta, plan = _extract_plan(spec_path)
    rebuilt = structural_hash_from_plan(meta, plan)
    sealed = json.load(open(os.path.join(APPREG, f"{app_id}.sealed.json"), encoding="utf-8"))
    generated = build_shor_spec(app_id, n, a, t)
    generated_meta, generated_plan = _extract_plan_from_text(generated)
    plan_matches_generator = generated_plan == plan and generated_meta == meta
    return {
        "id": app_id,
        "N": n,
        "a": a,
        "t": t,
        "n_sys": meta["n_sys"],
        "sealed_u_hash": sealed["u_hash"],
        "rebuilt_u_hash": rebuilt["u_hash"],
        "hash_matches": rebuilt["u_hash"] == sealed["u_hash"],
        "resource_matches": rebuilt["resource"] == sealed["resource"],
        "plan_matches_generator": plan_matches_generator,
        "child_count": rebuilt["child_count"],
    }


def _extract_plan_from_text(txt: str) -> tuple[dict, dict]:
    meta = json.loads(txt.split("```json id=app_meta\n", 1)[1].split("```", 1)[0])
    plan = json.loads(txt.split("```json id=plan\n", 1)[1].split("```", 1)[0])
    return meta, plan


def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    targets = [
        ("shor119", 119, 2, 8),
        ("shor221", 221, 2, 8),
        ("shor381", 381, 2, 8),
        ("shor635", 635, 2, 8),
        ("shor1285", 1285, 2, 8),
    ]
    results = [verify_existing(*row) for row in targets]
    all_ok = all(r["hash_matches"] and r["resource_matches"] and r["plan_matches_generator"] for r in results)
    report = {
        "phase": "W12.12 ShorStructuralGeneralizer",
        "schema": "shor-structural-generalizer/v1",
        "honesty": "Report/helper only. Existing structural seals are not rewritten.",
        "helper": "build_shor_spec(app_id, n, a, t=8)",
        "results": results,
        "all_ok": bool(all_ok),
    }
    out_path = os.path.join(OUT, "SHOR-STRUCTURAL-GENERALIZER-REPORT.json")
    json.dump(report, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("=" * 84)
    print("W12.12 ShorStructuralGeneralizer - structural hash reproduction")
    print("=" * 84)
    for r in results:
        print(f"{r['id']}: hash={r['hash_matches']} resource={r['resource_matches']} "
              f"generator_plan={r['plan_matches_generator']} children={r['child_count']}")
    print("-" * 84)
    print(f"all_ok={all_ok} report={out_path}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
