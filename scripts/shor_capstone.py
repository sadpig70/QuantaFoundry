# -*- coding: utf-8 -*-
"""
shor_capstone.py — Stage 6 W6.5 ShorCapstone (genuine distinct-prime Shor-91 = 7×13)

W6.1~W6.4가 만든 조각을 완전한 Shor 주기발견 회로로 조립하는 capstone. N=91=7×13(둘 다 >5,
진짜 distinct-prime). 부품: cmul{2,4,16,74}_mod91(W6.1 c7x-engine) + iqft8(W6.3) + H. 15큐비트 >
EXACT_BOUND(12) → Tier-1 STRUCTURAL(dense 미봉인, 봉인부품의 Merkle 합성).

구조(shor21 mirror, big-endian): counting c0..c7(8) | work w0..w6(7). ord_91(2)=12.
  controlled-U^(2^j), U=×2 mod 91. counting qubit (t-1-j) → 2^(2^j) mod 91.
  powa[q0..q7] = [74,16,74,16,74,16,4,2] (distinct multiplier {2,4,16,74}).
  plan: H(c0..c7) · controlled-cmul_{powa[q]}(q, w0..w6) · iqft8(c0..c7).

정직성 경계(중요):
 - Tier-1 STRUCTURAL은 dense Tier-0보다 *약한* 봉인 — 전체 유니터리 dense 검증 아님, 봉인부품이
   계획대로 조립됨을 Merkle 인증. shor15/21(Tier-0 dense)과 보증 등급 다름.
 - t=8 counting(iqft8): 2^8=256 < 2r²=288(textbook sufficiency 약간 미달). period readout 확률에만
   영향, 구조적 봉인은 t 무관. t=9는 cr9_dag 선행봉인 필요(별건).
 - period readout(r=12→7,13)은 illustrative only(§8.4) — 봉인 증거 아님.
 - 생성≠검증: app_assemble Tier-1 통과로만 SEALED. plan=봉인부품, MatrixGate 0.

사용:  python scripts/shor_capstone.py
"""
from __future__ import annotations

import os
import sys
import json
from math import gcd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, ORACLE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import app_assemble as aa       # noqa: E402  (앱 봉인 — 사용만)

SPECS_APPS = os.path.join(ROOT, "specs", "apps")
APPREG = os.path.join(ROOT, "registry", "apps")
OUT = os.path.join(ROOT, ".pgf", "arith")

N = 91
A = 2
T = 8          # counting qubits (iqft8)
WORK = 7       # work qubits (91 < 128 = 2^7)
# counting qubit q (big-endian, q0=MSB) → 2^(2^(T-1-q)) mod N
POWA = [pow(A, 1 << (T - 1 - q), N) for q in range(T)]   # [74,16,74,16,74,16,4,2]


def _shor91_spec():
    work = list(range(T, T + WORK))                       # [8..14]
    steps = []
    for q in range(T):                                    # H on counting
        steps.append({"spec": "../modules/h_gate.pg", "targets": [q]})
    for q in range(T):                                    # controlled-U^(2^j)
        steps.append({"app": f"cmul{POWA[q]}_mod{N}.app.pg", "targets": [q] + work})
    steps.append({"app": "iqft8.app.pg", "targets": list(range(T))})   # iQFT on counting

    n_sys = T + WORK
    header = (f"# shor91 — genuine Shor period-finding (N={N}={'×'.join(map(str,_factor(N)))}, a={A}). "
              f"{n_sys}q: counting c0..c{T-1}({T}) | work w0..w{WORK-1}({WORK}). "
              f"H^{T} · controlled-U^(2^j)(U=×{A} mod {N}, powa={POWA}) · iqft8. "
              f"15q>EXACT_BOUND → Tier-1 STRUCTURAL(Merkle of 봉인부품, dense 미봉인). "
              f"판독(illustrative §8.4): counting/{1<<T} 연속분수 → r=12 → gcd(2^6±1,91)=7,13.\n")
    plan = {"tier": "structural", "steps": steps}
    spec = (
        header +
        '```json id=app_meta\n'
        f'{{"id": "shor91", "n_sys": {n_sys}, "n_anc": 0}}\n'
        "```\n"
        "```json id=plan\n"
        f"{json.dumps(plan)}\n"
        "```\n")
    return spec, n_sys


def _factor(n):
    fs, d, m = [], 2, n
    while d * d <= m:
        while m % d == 0:
            fs.append(d); m //= d
        d += 1
    if m > 1:
        fs.append(m)
    return fs


def _children_sealed():
    need = [f"cmul{m}_mod{N}" for m in sorted(set(POWA))] + ["iqft8", "h_gate"]
    out = {}
    for c in need:
        store = APPREG if c.startswith(("cmul", "iqft", "shor")) else os.path.join(ROOT, "registry", "modules")
        out[c] = os.path.exists(os.path.join(store, f"{c}.sealed.json"))
    return out


def _period_readout():
    """illustrative only (§8.4): ord_N(a) → 인수. 봉인 증거 아님."""
    r, x = 1, A % N
    while x != 1:
        x = (x * A) % N; r += 1
    res = {"a": A, "N": N, "order_r": r, "r_even": r % 2 == 0}
    if r % 2 == 0:
        h = pow(A, r // 2, N)
        res["a_r2"] = h
        res["nontrivial"] = h != N - 1
        res["factors"] = sorted({gcd(h - 1, N), gcd(h + 1, N)} - {1, N})
    return res


def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 76)
    print("W6.5 ShorCapstone — genuine distinct-prime Shor-91 (7×13), Tier-1 STRUCTURAL")
    print("정직성: Tier-1=structural(dense보다 약한 보증). period readout=illustrative(§8.4).")
    print("=" * 76)

    # A. children 봉인 확인
    ch = _children_sealed()
    print(f"[Children] {ch}")
    assert all(ch.values()), f"부품 미봉인: {[k for k,v in ch.items() if not v]}"

    # B. AssembleShor91
    spec, n_sys = _shor91_spec()
    sp = os.path.join(SPECS_APPS, "shor91.app.pg")
    open(sp, "w", encoding="utf-8", newline="\n").write(spec)
    v = aa.assemble(sp, APPREG)
    print(f"[AssembleShor91] sealed={v.sealed} tier={v.tier} n_sys={v.n_sys} "
          f"u={str(v.u_hash)[:16]} reason={v.reason or '(ok)'}")

    # C. StructuralVerify — 결정론(재조립 u_hash 동일)
    v2 = aa.assemble(sp, os.path.join(OUT, "_shorreg"))
    det = v.sealed and v2.sealed and v.u_hash == v2.u_hash
    print(f"[StructuralVerify] 재조립 u_hash 결정론 일치: {det}")
    sealed_disk = json.load(open(os.path.join(APPREG, "shor91.sealed.json")))
    print(f"   tier={sealed_disk.get('tier')} (1=STRUCTURAL) · contract={sealed_disk.get('contract')}")

    # period readout (illustrative)
    pr = _period_readout()
    print(f"[PeriodReadout|illustrative §8.4] ord_{N}({A})={pr['order_r']} → 2^{pr['order_r']//2}={pr.get('a_r2')} "
          f"→ factors={pr.get('factors')} (봉인 증거 아님)")

    report = {
        "phase": "W6.5 ShorCapstone (Shor-91 = 7×13)",
        "honesty": "Tier-1 STRUCTURAL (weaker than Tier-0 dense — Merkle of sealed components, "
                   "no dense unitary verify); t=8 counting (period readout illustrative, seal t-independent); "
                   "period readout illustrative only (§8.4); generation != verification (app_assemble Tier-1).",
        "n_sys": n_sys, "counting_t": T, "work": WORK, "powa": POWA,
        "children_sealed": ch,
        "sealed": bool(v.sealed), "tier": v.tier, "u_hash": v.u_hash,
        "deterministic_reassembly": bool(det),
        "period_readout_illustrative": pr,
    }
    all_ok = (v.sealed and v.tier == 1 and det
              and pr["order_r"] == 12 and pr.get("factors") == [7, 13])
    report["all_ok"] = bool(all_ok)
    json.dump(report, open(os.path.join(OUT, "SHOR-CAPSTONE-REPORT.json"), "w",
                           encoding="utf-8"), ensure_ascii=False, indent=2)
    print("-" * 76)
    print(f"all_ok={all_ok}  →  .pgf/arith/SHOR-CAPSTONE-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
