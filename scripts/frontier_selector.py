# -*- coding: utf-8 -*-
"""
frontier_selector.py - W12.11 deterministic frontier candidate selector.

Report-only. It ranks semiprime Shor frontier candidates by work bits, unique
powers, MMD gate count, max control, and whether the classical period readout is
useful. It does not write specs or seals.
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


def multiplicative_order(a: int, n: int, limit: int = 10000) -> int | None:
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


def candidate_stats(n: int, a: int = 2, t: int = 8) -> dict | None:
    if not is_distinct_semiprime(n) or gcd(a, n) != 1:
        return None
    work = math.ceil(math.log2(n))
    nq = work + 1
    r = multiplicative_order(a, n)
    factors = readout_factors(a, n, r)
    if len(factors) != 2:
        return None
    powa = [pow(a, 1 << (t - 1 - q), n) for q in range(t)]
    unique = sorted(set(powa) - {1})
    cmuls = []
    total_gates = 0
    max_control = 0
    total_frontier_controls = 0
    for mul in unique:
        gates = gs.mmd_synthesize(gs._modmul_perm(mul, n, nq), nq)
        gate_count = len(gates)
        mc = max((len(c) for c, _ in gates), default=0)
        frontier_controls = sum(1 for c, _ in gates if len(c) == mc)
        total_gates += gate_count
        max_control = max(max_control, mc)
        total_frontier_controls += frontier_controls
        cmuls.append({
            "a": mul,
            "gate_count": gate_count,
            "max_control": mc,
            "frontier_control_count": frontier_controls,
        })
    score = (
        max_control * 1_000_000
        + work * 100_000
        + len(unique) * 10_000
        + total_gates
        - total_frontier_controls
    )
    return {
        "N": n,
        "a": a,
        "factors": factor(n),
        "order_r": r,
        "readout_factors": factors,
        "counting_t": t,
        "work": work,
        "nq": nq,
        "powa": powa,
        "unique_powers": unique,
        "unique_power_count": len(unique),
        "total_gate_count": total_gates,
        "max_control": max_control,
        "frontier_control_count": total_frontier_controls,
        "cmul_stats": cmuls,
        "score": score,
    }


def select_frontiers(ranges: list[tuple[int, int]], top_k: int = 10) -> dict:
    buckets = {}
    for lo, hi in ranges:
        rows = []
        for n in range(lo, hi + 1):
            row = candidate_stats(n)
            if row:
                rows.append(row)
        rows.sort(key=lambda r: (r["score"], r["total_gate_count"], r["N"]))
        buckets[f"{lo}_{hi}"] = rows[:top_k]
    return buckets


def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    buckets = select_frontiers([(15, 127), (128, 255), (256, 511), (512, 767)], top_k=10)
    report = {
        "phase": "W12.11 FrontierSelector",
        "schema": "frontier-selector/v1",
        "honesty": "Report-only. No specs, seals, registry writes, or root changes.",
        "ranking": "score=(max_control, work, unique_power_count, total_gate_count, -frontier_control_count, N)",
        "buckets": buckets,
        "current_frontier_observations": {
            "best_256_511": buckets["256_511"][0] if buckets["256_511"] else None,
            "best_512_767": buckets["512_767"][0] if buckets["512_767"] else None,
        },
    }
    out_path = os.path.join(OUT, "FRONTIER-SELECTOR-REPORT.json")
    json.dump(report, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    best = report["current_frontier_observations"]["best_512_767"]
    print("=" * 84)
    print("W12.11 FrontierSelector - deterministic candidate ranking")
    print("=" * 84)
    for key, rows in buckets.items():
        if rows:
            r = rows[0]
            print(f"[{key}] best N={r['N']} factors={r['factors']} work={r['work']} "
                  f"maxc={r['max_control']} unique={r['unique_power_count']} gates={r['total_gate_count']}")
    print("-" * 84)
    print(f"report={out_path}")
    return 0 if best is not None else 1


if __name__ == "__main__":
    sys.exit(main())
