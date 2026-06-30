# -*- coding: utf-8 -*-
"""
c8x_frontier.py — W12.6 C8xPrimitiveFrontier

Close the 8-control primitive gap that blocked N>=128 modular arithmetic.

Sealed outputs:
  Tier-0 module: c8x
  Tier-0 app:    cmul2_mod187 (N=187=11*17, 9q, uses c8x)

Honesty boundary:
  - c8x is an exact 9q MultiControlX module, verified against an independent
    permutation golden.
  - cmul2_mod187 is an exact controlled modular multiplier app; period/factor
    behavior is illustrative only.
  - This unlocks 8-work-bit modular arithmetic. N>=256 remains blocked until
    c9x or another 9-control strategy is sealed.

Usage: python scripts/c8x_frontier.py
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
import app_assemble as aa  # noqa: E402  (QPGF app seal path, use only)
import verify_seal as vs  # noqa: E402  (hash_unitary, use only)
import genskills as gs    # noqa: E402  (modmul synthesis, now c8x-enabled)

SPECS_MODS = os.path.join(ROOT, "specs", "modules")
SPECS_APPS = os.path.join(ROOT, "specs", "apps")
MODREG = os.path.join(ROOT, "registry", "modules")
APPREG = os.path.join(ROOT, "registry", "apps")
OUT = os.path.join(ROOT, ".pgf", "arith")

N = 187
A = 2
WORK = math.ceil(math.log2(N))
NQ = WORK + 1

_MCT_SET = {"x_gate", "cnot", "toffoli", "c3x", "c4x", "c5x", "c6x", "c7x", "c8x"}


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


def _c8x_spec() -> str:
    return (
        "```python id=bloq\n"
        "from qualtran.bloqs.mcmt import MultiControlX\n"
        "bloq = MultiControlX(cvs=(1,) * 8)\n"
        "```\n"
        "```python id=golden\n"
        "import numpy as np\n"
        "# c8x: control=first 8 qubits (MSB), target=last (big-endian).\n"
        "# Flip target iff all controls are 1.\n"
        "golden = np.zeros((1<<9, 1<<9), dtype=complex)\n"
        "for s in range(1<<9):\n"
        "    o = (s ^ 1) if (s >> 1) == ((1<<8) - 1) else s\n"
        "    golden[o, s] = 1\n"
        "```\n"
        "```json id=meta\n"
        "{\"id\": \"c8x\", \"n_sys\": 9, \"n_anc\": 0}\n"
        "```\n"
    )


def _seal_c8x() -> dict:
    os.makedirs(SPECS_MODS, exist_ok=True)
    spec_path = os.path.join(SPECS_MODS, "c8x.pg")
    with open(spec_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(_c8x_spec())
    seal_path = os.path.join(MODREG, "c8x.sealed.json")
    if not os.path.exists(seal_path):
        proc = subprocess.run(
            ["python", os.path.join(ORACLE, "verify_seal.py"), spec_path, "--out", MODREG],
            capture_output=True,
            text=True,
            cwd=ORACLE,
        )
        if proc.returncode != 0 and not os.path.exists(seal_path):
            return {"id": "c8x", "sealed": False, "stderr": proc.stderr[-500:]}
    sealed = json.load(open(seal_path, encoding="utf-8"))
    return {
        "id": "c8x",
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


def _seal_cmul187() -> dict:
    spec, deps = gs.gen_modmul(A, N, NQ)
    gates = gs.mmd_synthesize(gs._modmul_perm(A, N, NQ), NQ)
    maxc = max((len(c) for c, _ in gates), default=0)
    if not set(deps).issubset(_MCT_SET):
        raise RuntimeError(f"unexpected deps for cmul{A}_mod{N}: {deps}")
    if "c8x" not in deps or maxc != 8:
        raise RuntimeError(f"cmul{A}_mod{N} did not exercise c8x: deps={deps}, maxc={maxc}")
    spec_path = os.path.join(SPECS_APPS, f"cmul{A}_mod{N}.app.pg")
    with open(spec_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(spec)
    verdict = aa.assemble(spec_path, APPREG)
    return {
        "id": f"cmul{A}_mod{N}",
        "N": N,
        "a": A,
        "factors": _factor(N),
        "nq": NQ,
        "sealed": bool(verdict.sealed),
        "tier": verdict.tier,
        "u_hash": verdict.u_hash,
        "reason": verdict.reason,
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
    print("W12.6 C8xPrimitiveFrontier — c8x + N=187 modular multiplier frontier.")
    print("정직성: c8x/cmul2_mod187=Tier-0 EXACT, readout=illustrative.")
    print("=" * 84)

    c8x = _seal_c8x()
    c8x_indep = _independent_cnx_hash(8)
    c8x_match = c8x.get("u_hash") == c8x_indep
    print(f"[C8X] sealed={c8x['sealed']} tier={c8x['tier']} n_sys={c8x['n_sys']} match={c8x_match}")

    cmul = _seal_cmul187()
    print(
        f"[Cmul] {cmul['id']} sealed={cmul['sealed']} tier={cmul['tier']} "
        f"gates={cmul['gate_count']} maxc={cmul['max_control']} c8={cmul['control_dist'].get(8, 0)}"
    )
    cmul_indep = _independent_cmul_hash()
    print(f"[IndependentArith] cmul hash match={cmul_indep['matches_sealed']}")

    readout = _period_readout()
    print(
        f"[Readout|illustrative] ord_{N}({A})={readout['order_r']} -> "
        f"2^{readout['order_r']//2} mod {N}={readout.get('a_r2')} -> factors={readout.get('factors')}"
    )

    report = {
        "phase": "W12.6 C8xPrimitiveFrontier",
        "honesty": "c8x closes the 8-control primitive gap for 8-work-bit modular arithmetic. "
                   "c8x and cmul2_mod187 are Tier-0 exact seals; period/factor readout is illustrative only. "
                   "N>=256 remains blocked until c9x or another 9-control strategy is sealed.",
        "target": {"N": N, "a": A, "factors": _factor(N), "work": WORK, "nq": NQ},
        "c8x_module": c8x,
        "c8x_independent": {"independent_u_hash": c8x_indep[:16], "matches_sealed": c8x_match},
        "cmul_app": cmul,
        "independent_arith_verify": cmul_indep,
        "period_readout_illustrative": readout,
    }
    all_ok = (
        c8x["sealed"] and c8x.get("tier") == 0 and c8x.get("n_sys") == 9 and c8x_match
        and cmul["sealed"] and cmul["tier"] == 0 and cmul["max_control"] == 8
        and "c8x" in cmul["deps"] and cmul_indep["matches_sealed"]
        and readout["order_r"] > 1
    )
    report["all_ok"] = bool(all_ok)
    out_path = os.path.join(OUT, "C8X-FRONTIER-187-REPORT.json")
    json.dump(report, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("-" * 84)
    print(f"all_ok={all_ok} -> .pgf/arith/C8X-FRONTIER-187-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
