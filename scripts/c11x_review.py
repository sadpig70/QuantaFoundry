# -*- coding: utf-8 -*-
"""
c11x_review.py - W12.16 c11x feasibility and cost review.

Review-only. It estimates the next primitive frontier after shor635 without
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


def multiplicative_order(a: int, n: int, limit: int = 50000) -> int | None:
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


def pre_candidates(lo: int = 1024, hi: int = 2047, a: int = 2, t: int = 8) -> list[dict]:
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


def cmul2_blocker_signal(row: dict) -> dict:
    n, nq = row["N"], row["nq"]
    start = time.perf_counter()
    try:
        _spec, deps = gs.gen_modmul(2, n, nq)
        return {
            "N": n,
            "status": "within_current_cap",
            "deps": deps,
            "elapsed_s": round(time.perf_counter() - start, 4),
        }
    except Exception as exc:
        msg = str(exc)
        return {
            "N": n,
            "status": "c11x_blocker" if "controls > 10" in msg else "error",
            "error": msg,
            "elapsed_s": round(time.perf_counter() - start, 4),
        }


def synthesize_family_cost(row: dict) -> dict:
    n, nq = row["N"], row["nq"]
    start = time.perf_counter()
    cmuls = []
    total_gates = 0
    total_c11 = 0
    max_control = 0
    for mul in row["unique_powers"]:
        gates = gs.mmd_synthesize(gs._modmul_perm(mul, n, nq), nq)
        dist = Counter(len(c) for c, _ in gates)
        rec = {
            "a": mul,
            "gate_count": len(gates),
            "max_control": max(dist) if dist else 0,
            "c11_count": dist.get(11, 0),
            "control_dist": dict(sorted(dist.items(), reverse=True)),
        }
        cmuls.append(rec)
        total_gates += rec["gate_count"]
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
        "c11_count": total_c11,
        "elapsed_s": round(time.perf_counter() - start, 4),
    }


def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    root_before = manifest_root()
    c11x_spec_path = os.path.join(ROOT, "specs", "modules", "c11x.pg")
    c11x_seal_path = os.path.join(ROOT, "registry", "modules", "c11x.sealed.json")

    candidates = pre_candidates()
    sampled = candidates[:12]
    blocker_signals = [cmul2_blocker_signal(row) for row in sampled]
    blocked_count = sum(1 for row in blocker_signals if row["status"] == "c11x_blocker")

    target = candidates[0] if candidates else None
    representative = synthesize_family_cost(target) if target else None

    dense_dim = 1 << 12
    review = {
        "phase": "W12.16 C11xPrimitiveReview",
        "schema": "c11x-review/v1",
        "honesty": "Review-only. No c11x spec, no c11x seal, no registry/root mutation.",
        "registry_root_before": root_before,
        "dense_cost_estimate": {
            "c11x_n_sys": 12,
            "unitary_dimension": dense_dim,
            "complex128_dense_bytes": dense_dim * dense_dim * 16,
            "complex128_dense_mib": round((dense_dim * dense_dim * 16) / (1024 * 1024), 2),
            "comment": "Standalone c11x exact dense oracle is plausible but materially heavier than c10x; app-family exact path should remain permutation-space.",
        },
        "candidate_scan": {
            "range": [1024, 2047],
            "a": 2,
            "count": len(candidates),
            "ranking": "unique_power_count, then N",
            "top": candidates[:12],
        },
        "cmul2_blocker_sample": {
            "sample_size": len(sampled),
            "c11x_blocked": blocked_count,
            "signals": blocker_signals,
        },
        "representative_payoff": representative,
        "file_guard": {
            "c11x_spec_exists": os.path.exists(c11x_spec_path),
            "c11x_seal_exists": os.path.exists(c11x_seal_path),
        },
        "decision": {
            "go_no_go": "GO_FOR_C11X_FRONTIER_WITH_GUARDS_NOT_NOW",
            "recommended_next": "W12.17 C11xPrimitiveFrontier",
            "recommended_target": representative,
            "guardrails": [
                "Seal c11x module first and verify independent cnx_perm(11) hash.",
                "Keep multiplier payoff to one representative app first, preferably cmul2_mod1285.",
                "Do not attempt shor1285 in the same task.",
                "Use permutation-space exact C-app path for 12q multiplier apps.",
                "Abort if c11x oracle memory/time exceeds local feasibility.",
            ],
        },
    }
    root_after = manifest_root()
    review["registry_root_after"] = root_after
    review["root_unchanged"] = root_before == root_after
    review["all_ok"] = bool(
        candidates
        and representative
        and blocked_count == len(sampled)
        and representative["max_control"] == 11
        and representative["c11_count"] > 0
        and not review["file_guard"]["c11x_spec_exists"]
        and not review["file_guard"]["c11x_seal_exists"]
        and review["root_unchanged"]
    )

    out_path = os.path.join(OUT, "C11X-PRIMITIVE-REVIEW.json")
    json.dump(review, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("=" * 84)
    print("W12.16 C11xPrimitiveReview - review only")
    print("=" * 84)
    print(f"root_unchanged={review['root_unchanged']} candidates={len(candidates)}")
    if representative:
        print(
            f"target N={representative['N']} factors={representative['factors']} "
            f"work={representative['work']} unique={len(representative['unique_powers'])} "
            f"gates={representative['total_gate_count']} c11={representative['c11_count']}"
        )
    print(f"cmul2 blocker sample={blocked_count}/{len(sampled)}")
    print("decision=GO_FOR_C11X_FRONTIER_WITH_GUARDS_NOT_NOW")
    print("-" * 84)
    print(f"all_ok={review['all_ok']} -> .pgf/arith/C11X-PRIMITIVE-REVIEW.json")
    return 0 if review["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
