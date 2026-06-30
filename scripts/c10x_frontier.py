# -*- coding: utf-8 -*-
"""
c10x_frontier.py - W12.14 C10xPrimitiveFrontier.

Close the 10-control primitive gap for 10-work-bit modular arithmetic.

Sealed outputs:
  Tier-0 module: c10x
  Tier-0 app:    cmul2_mod635 (N=635=5*127, 11q, uses c10x)

Honesty boundary:
  - c10x is an exact 11q MultiControlX module.
  - cmul2_mod635 is an exact controlled modular multiplier app sealed through a
    full-basis permutation C-app check.
  - Full Shor-635 is not claimed here.
"""
from __future__ import annotations

import json
import math
import os
import subprocess
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

SPECS_MODS = os.path.join(ROOT, "specs", "modules")
SPECS_APPS = os.path.join(ROOT, "specs", "apps")
MODREG = os.path.join(ROOT, "registry", "modules")
APPREG = os.path.join(ROOT, "registry", "apps")
OUT = os.path.join(ROOT, ".pgf", "arith")

N = 635
A = 2
WORK = math.ceil(math.log2(N))
NQ = WORK + 1

_MCT_SET = {
    "x_gate", "cnot", "toffoli", "c3x", "c4x", "c5x",
    "c6x", "c7x", "c8x", "c9x", "c10x",
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


def _c10x_spec() -> str:
    return (
        "```python id=bloq\n"
        "from qualtran.bloqs.mcmt import MultiControlX\n"
        "bloq = MultiControlX(cvs=(1,) * 10)\n"
        "```\n"
        "```python id=golden\n"
        "import numpy as np\n"
        "# c10x: control=first 10 qubits (MSB), target=last (big-endian).\n"
        "golden = np.zeros((1<<11, 1<<11), dtype=complex)\n"
        "for s in range(1<<11):\n"
        "    o = (s ^ 1) if (s >> 1) == ((1<<10) - 1) else s\n"
        "    golden[o, s] = 1\n"
        "```\n"
        "```json id=meta\n"
        "{\"id\": \"c10x\", \"n_sys\": 11, \"n_anc\": 0}\n"
        "```\n"
    )


def _seal_c10x() -> dict:
    os.makedirs(SPECS_MODS, exist_ok=True)
    spec_path = os.path.join(SPECS_MODS, "c10x.pg")
    with open(spec_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(_c10x_spec())
    seal_path = os.path.join(MODREG, "c10x.sealed.json")
    if not os.path.exists(seal_path):
        proc = subprocess.run(
            ["python", os.path.join(ORACLE, "verify_seal.py"), spec_path, "--out", MODREG],
            capture_output=True,
            text=True,
            cwd=ORACLE,
        )
        if proc.returncode != 0 and not os.path.exists(seal_path):
            return {"id": "c10x", "sealed": False, "stderr": proc.stderr[-1000:]}
    sealed = json.load(open(seal_path, encoding="utf-8"))
    return {
        "id": "c10x",
        "sealed": bool(sealed.get("sealed")),
        "tier": sealed.get("tier", 0),
        "n_sys": sealed.get("n_sys"),
        "u_hash": sealed.get("u_hash"),
        "resource": sealed.get("resource", {}),
    }


def _independent_cnx_hash(nc: int) -> str:
    n = nc + 1
    U = np.zeros((1 << n, 1 << n), dtype=complex)
    for s in range(1 << n):
        out = (s ^ 1) if (s >> 1) == ((1 << nc) - 1) else s
        U[out, s] = 1
    return vs.hash_unitary(U)


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


def _seal_cmul635() -> dict:
    spec, deps = gs.gen_modmul(A, N, NQ)
    gates = gs.mmd_synthesize(gs._modmul_perm(A, N, NQ), NQ)
    maxc = max((len(c) for c, _ in gates), default=0)
    if not set(deps).issubset(_MCT_SET):
        raise RuntimeError(f"unexpected deps for cmul{A}_mod{N}: {deps}")
    if maxc != 10 or "c10x" not in deps:
        raise RuntimeError(f"cmul{A}_mod{N} did not exercise c10x: deps={deps}, maxc={maxc}")
    spec_path = os.path.join(SPECS_APPS, f"cmul{A}_mod{N}.app.pg")
    with open(spec_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(spec)
    verdict = _seal_exact_permutation_app(f"cmul{A}_mod{N}", NQ, gates, gs._modmul_perm(A, N, NQ))
    return {
        "id": f"cmul{A}_mod{N}",
        "N": N,
        "a": A,
        "factors": _factor(N),
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


def _independent_cmul_hash() -> dict:
    dim = 1 << NQ
    U = np.zeros((dim, dim), dtype=complex)
    for s in range(dim):
        if (s >> (NQ - 1)) & 1 == 0:
            U[s, s] = 1
        else:
            w = s & ((1 << (NQ - 1)) - 1)
            nw = (A * w) % N if w < N else w
            U[(1 << (NQ - 1)) | nw, s] = 1
    got = vs.hash_unitary(U)
    sealed = json.load(open(os.path.join(APPREG, f"cmul{A}_mod{N}.sealed.json"), encoding="utf-8"))["u_hash"]
    return {
        "id": f"cmul{A}_mod{N}",
        "independent_u_hash": got[:16],
        "matches_sealed": got == sealed,
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
    print("W12.14 C10xPrimitiveFrontier - c10x + cmul2_mod635.")
    print("Honesty: c10x/cmul2_mod635=Tier-0 EXACT, full Shor deferred.")
    print("=" * 84)
    print(f"[Target] N={N} factors={_factor(N)} a={A} WORK={WORK} nq={NQ}")

    c10x = _seal_c10x()
    c10x_indep = _independent_cnx_hash(10)
    c10x_match = c10x.get("u_hash") == c10x_indep
    print(f"[C10X] sealed={c10x['sealed']} tier={c10x['tier']} n_sys={c10x['n_sys']} match={c10x_match}")

    cmul = _seal_cmul635()
    print(
        f"[Cmul] {cmul['id']} sealed={cmul['sealed']} tier={cmul['tier']} "
        f"gates={cmul['gate_count']} maxc={cmul['max_control']} c10={cmul['control_dist'].get(10, 0)}"
    )
    cmul_indep = _independent_cmul_hash()
    print(f"[IndependentArith] cmul hash match={cmul_indep['matches_sealed']}")

    readout = _period_readout()
    print(
        f"[Readout|illustrative] ord_{N}({A})={readout['order_r']} -> "
        f"2^{readout['order_r']//2} mod {N}={readout.get('a_r2')} -> factors={readout.get('factors')}"
    )

    report = {
        "phase": "W12.14 C10xPrimitiveFrontier",
        "honesty": "c10x closes the 10-control primitive gap for 10-work-bit modular arithmetic. "
                   "c10x and cmul2_mod635 are Tier-0 exact seals; full Shor is deferred.",
        "target": {"N": N, "a": A, "factors": _factor(N), "work": WORK, "nq": NQ},
        "c10x_module": c10x,
        "c10x_independent": {"independent_u_hash": c10x_indep[:16], "matches_sealed": c10x_match},
        "cmul_app": cmul,
        "independent_arith_verify": cmul_indep,
        "period_readout_illustrative": readout,
    }
    all_ok = (
        c10x["sealed"] and c10x.get("tier") == 0 and c10x.get("n_sys") == 11 and c10x_match
        and cmul["sealed"] and cmul["tier"] == 0 and cmul["max_control"] == 10
        and "c10x" in cmul["deps"] and cmul_indep["matches_sealed"]
        and readout["order_r"] == 28 and readout.get("factors") == [5, 127]
    )
    report["all_ok"] = bool(all_ok)
    out_path = os.path.join(OUT, "C10X-FRONTIER-635-REPORT.json")
    json.dump(report, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("-" * 84)
    print(f"all_ok={all_ok} -> .pgf/arith/C10X-FRONTIER-635-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
