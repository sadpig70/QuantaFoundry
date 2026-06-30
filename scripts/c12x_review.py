# -*- coding: utf-8 -*-
"""
c12x_review.py - W12.20 c12x feasibility and cost review.

Review-only. It estimates the next primitive frontier after shor1285 without
writing specs or seals. The goal is a bounded go/no-go decision, not registry
growth.
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
from collections import Counter
from math import gcd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import genskills as gs  # noqa: E402

OUT = os.path.join(ROOT, ".pgf", "arith")
REGISTRY_MANIFEST = os.path.join(ROOT, "registry", "REGISTRY-MANIFEST.json")


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


def is_distinct_semiprime(n: int) -> bool:
    f = factor(n)
    return len(f) == 2 and f[0] != f[1]


def multiplicative_order(a: int, n: int, limit: int = 200000) -> int | None:
    if gcd(a, n) != 1:
        return None
    r, x = 1, a % n
    while x != 1 and r < limit:
        x = (x * a) % n
        r += 1
    return r if x == 1 else None


def readout_factors(a: int, n: int, r: int | None) -> list[int]:
    if not r or r % 2:
        return []
    h = pow(a, r // 2, n)
    if h == n - 1:
        return []
    return sorted({gcd(h - 1, n), gcd(h + 1, n)} - {1, n})


def manifest_root() -> str:
    return json.load(open(REGISTRY_MANIFEST, encoding="utf-8"))["registry_root_hash"]


def pre_candidates(lo: int = 2048, hi: int = 4095, a: int = 2, t: int = 8) -> list[dict]:
    rows = []
    for n in range(lo, hi + 1):
        if not is_distinct_semiprime(n) or gcd(a, n) != 1:
            continue
        r = multiplicative_order(a, n)
        fs = readout_factors(a, n, r)
        if len(fs) != 2:
            continue
        work = math.ceil(math.log2(n))
        nq = work + 1
        powa = [pow(a, 1 << (t - 1 - q), n) for q in range(t)]
        unique = sorted(set(powa) - {1})
        rows.append({
            "N": n,
            "a": a,
            "factors": factor(n),
            "order_r": r,
            "readout_factors": fs,
            "counting_t": t,
            "work": work,
            "nq": nq,
            "powa": powa,
            "unique_powers": unique,
            "unique_power_count": len(unique),
        })
    rows.sort(key=lambda r: (r["unique_power_count"], r["N"]))
    return rows


def synthesize_family_cost(row: dict) -> dict:
    n, nq = row["N"], row["nq"]
    start = time.perf_counter()
    cmuls = []
    total_gates = 0
    total_c12 = 0
    total_c11 = 0
    max_control = 0
    for mul in row["unique_powers"]:
        sub_start = time.perf_counter()
        gates = gs.mmd_synthesize(gs._modmul_perm(mul, n, nq), nq)
        dist = Counter(len(c) for c, _ in gates)
        rec = {
            "a": mul,
            "gate_count": len(gates),
            "max_control": max(dist) if dist else 0,
            "c12_count": dist.get(12, 0),
            "c11_count": dist.get(11, 0),
            "control_dist": dict(sorted(dist.items(), reverse=True)),
            "elapsed_s": round(time.perf_counter() - sub_start, 4),
        }
        cmuls.append(rec)
        total_gates += rec["gate_count"]
        total_c12 += rec["c12_count"]
        total_c11 += rec["c11_count"]
        max_control = max(max_control, rec["max_control"])
    return {
        "N": n,
        "a": row["a"],
        "factors": row["factors"],
        "order_r": row["order_r"],
        "readout_factors": row["readout_factors"],
        "work": row["work"],
        "nq": nq,
        "powa": row["powa"],
        "unique_powers": row["unique_powers"],
        "cmul_stats": cmuls,
        "total_gate_count": total_gates,
        "max_control": max_control,
        "c12_count": total_c12,
        "c11_count": total_c11,
        "elapsed_s": round(time.perf_counter() - start, 4),
    }


def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    root_before = manifest_root()
    c12x_spec_path = os.path.join(ROOT, "specs", "modules", "c12x.pg")
    c12x_seal_path = os.path.join(ROOT, "registry", "modules", "c12x.sealed.json")

    candidates = pre_candidates()
    shortlist = candidates[:3]
    family_costs = [synthesize_family_cost(row) for row in shortlist]
    family_costs.sort(key=lambda r: (r["total_gate_count"], r["c12_count"], r["N"]))
    representative = family_costs[0] if family_costs else None

    dense_dim = 1 << 13
    review = {
        "phase": "W12.20 C12xPrimitiveReview",
        "schema": "c12x-review/v1",
        "honesty": "Review-only. No c12x spec, no c12x seal, no registry/root mutation.",
        "registry_root_before": root_before,
        "dense_cost_estimate": {
            "c12x_n_sys": 13,
            "unitary_dimension": dense_dim,
            "complex128_dense_bytes": dense_dim * dense_dim * 16,
            "complex128_dense_mib": round((dense_dim * dense_dim * 16) / (1024 * 1024), 2),
            "comment": "Standalone c12x exact dense oracle is about 1 GiB raw matrix, before tensor/normalization temporaries; attempt only with memory guards.",
        },
        "candidate_scan": {
            "range": [2048, 4095],
            "a": 2,
            "count": len(candidates),
            "ranking": "unique_power_count, then N; top-3 family costs measured",
            "top": candidates[:12],
        },
        "family_cost_shortlist": family_costs,
        "representative_payoff": representative,
        "file_guard": {
            "c12x_spec_exists": os.path.exists(c12x_spec_path),
            "c12x_seal_exists": os.path.exists(c12x_seal_path),
        },
        "decision": {
            "go_no_go": "GO_FOR_C12X_FRONTIER_WITH_MEMORY_GUARDS_NOT_NOW",
            "recommended_next": "W12.21 C12xPrimitiveFrontier",
            "recommended_target": {
                "N": representative["N"] if representative else None,
                "a": 2,
                "first_payoff_app": f"cmul2_mod{representative['N']}" if representative else None,
                "target": representative,
            },
            "guardrails": [
                "Seal c12x module first and verify independent cnx_perm(12) hash.",
                "Attempt only one representative payoff app first: cmul2_mod3683.",
                "Do not attempt payoff family or shor3683 in the same task.",
                "Use permutation-space exact C-app path for 13q multiplier apps.",
                "Abort and pivot to TrackW12 closure if c12x dense oracle exceeds local memory/time.",
                "Do not extend beyond c12x without another review-only gate.",
            ],
        },
    }
    root_after = manifest_root()
    review["registry_root_after"] = root_after
    review["root_unchanged"] = root_before == root_after
    review["all_ok"] = bool(
        candidates
        and len(family_costs) == len(shortlist) == 3
        and representative
        and representative["N"] == 3683
        and representative["max_control"] == 12
        and representative["c12_count"] > 0
        and not review["file_guard"]["c12x_spec_exists"]
        and not review["file_guard"]["c12x_seal_exists"]
        and review["root_unchanged"]
    )

    out_path = os.path.join(OUT, "C12X-PRIMITIVE-REVIEW.json")
    json.dump(review, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("=" * 84)
    print("W12.20 C12xPrimitiveReview - review only")
    print("=" * 84)
    print(f"root_unchanged={review['root_unchanged']} candidates={len(candidates)}")
    if representative:
        first = next(row for row in representative["cmul_stats"] if row["a"] == 2)
        print(
            f"target N={representative['N']} factors={representative['factors']} "
            f"work={representative['work']} unique={len(representative['unique_powers'])} "
            f"family_gates={representative['total_gate_count']} family_c12={representative['c12_count']} "
            f"cmul2_gates={first['gate_count']} cmul2_c12={first['c12_count']}"
        )
    print("decision=GO_FOR_C12X_FRONTIER_WITH_MEMORY_GUARDS_NOT_NOW")
    print("-" * 84)
    print(f"all_ok={review['all_ok']} -> .pgf/arith/C12X-PRIMITIVE-REVIEW.json")
    return 0 if review["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
