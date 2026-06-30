# -*- coding: utf-8 -*-
"""
c10x_review.py - W12.13 c10x feasibility and cost review.

Review-only. It estimates the next primitive frontier without writing specs or
seals. The goal is a go/no-go decision and successor plan, not registry growth.
"""
from __future__ import annotations

import json
import math
import os
import sys
from math import gcd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import genskills as gs  # noqa: E402

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


def is_distinct_semiprime(n: int) -> bool:
    f = factor(n)
    return len(f) == 2 and f[0] != f[1]


def order(a: int, n: int, limit: int = 20000) -> int | None:
    if gcd(a, n) != 1:
        return None
    r, x = 1, a % n
    while x != 1 and r < limit:
        x = (x * a) % n
        r += 1
    return r if x == 1 else None


def useful_readout(a: int, n: int, r: int | None) -> list[int]:
    if not r or r % 2:
        return []
    h = pow(a, r // 2, n)
    if h == n - 1:
        return []
    return sorted({gcd(h - 1, n), gcd(h + 1, n)} - {1, n})


def candidate(n: int, a: int = 2, t: int = 8) -> dict | None:
    if not is_distinct_semiprime(n) or gcd(a, n) != 1:
        return None
    r = order(a, n)
    fs = useful_readout(a, n, r)
    if len(fs) != 2:
        return None
    work = math.ceil(math.log2(n))
    nq = work + 1
    if nq < 11:
        return None
    powa = [pow(a, 1 << (t - 1 - q), n) for q in range(t)]
    unique = sorted(set(powa) - {1})
    total_gates = 0
    c10_count = 0
    max_control = 0
    cmuls = []
    for mul in unique:
        gates = gs.mmd_synthesize(gs._modmul_perm(mul, n, nq), nq)
        mc = max((len(c) for c, _ in gates), default=0)
        c10 = sum(1 for c, _ in gates if len(c) == 10)
        total_gates += len(gates)
        c10_count += c10
        max_control = max(max_control, mc)
        cmuls.append({"a": mul, "gate_count": len(gates), "max_control": mc, "c10_count": c10})
    if max_control < 10 or c10_count == 0:
        return None
    score = len(unique) * 10000 + total_gates - c10_count
    return {
        "N": n,
        "a": a,
        "factors": factor(n),
        "order_r": r,
        "readout_factors": fs,
        "work": work,
        "nq": nq,
        "powa": powa,
        "unique_powers": unique,
        "unique_power_count": len(unique),
        "total_gate_count": total_gates,
        "max_control": max_control,
        "c10_count": c10_count,
        "cmul_stats": cmuls,
        "score": score,
    }


def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    rows = []
    for n in range(512, 768):
        row = candidate(n)
        if row:
            rows.append(row)
    rows.sort(key=lambda r: (r["score"], r["total_gate_count"], r["N"]))
    best = rows[0] if rows else None
    review = {
        "phase": "W12.13 C10xPrimitiveReview",
        "schema": "c10x-review/v1",
        "honesty": "Review-only. No c10x spec, no seal, no registry/root mutation.",
        "dense_cost_estimate": {
            "c10x_n_sys": 11,
            "unitary_dimension": 2048,
            "complex128_dense_bytes": 2048 * 2048 * 16,
            "comment": "Standalone c10x exact dense oracle is likely feasible; 11q app-family exact dense is heavier and should keep permutation fast path.",
        },
        "candidate_scan": {
            "range": [512, 767],
            "a": 2,
            "count": len(rows),
            "top": rows[:10],
        },
        "decision": {
            "go_no_go": "GO_FOR_REVIEWED_NEXT_STEP_NOT_NOW",
            "recommended_next": "W12.14 C10xPrimitiveFrontier",
            "recommended_target": best,
            "guardrails": [
                "Seal c10x module first and verify independent cnx_perm(10) hash.",
                "Do not attempt full Shor in the same task.",
                "Use permutation-space exact C-app path for 11q multipliers.",
                "Keep c11x as the next honest blocker.",
            ],
        },
    }
    out_path = os.path.join(OUT, "C10X-PRIMITIVE-REVIEW.json")
    json.dump(review, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("=" * 84)
    print("W12.13 C10xPrimitiveReview - review only")
    print("=" * 84)
    if best:
        print(f"best N={best['N']} factors={best['factors']} work={best['work']} "
              f"unique={best['unique_power_count']} gates={best['total_gate_count']} c10={best['c10_count']}")
    print("decision=GO_FOR_REVIEWED_NEXT_STEP_NOT_NOW")
    print("-" * 84)
    print(f"report={out_path}")
    return 0 if best else 1


if __name__ == "__main__":
    sys.exit(main())
