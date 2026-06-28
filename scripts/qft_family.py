# -*- coding: utf-8 -*-
"""
qft_family.py — Stage 6 W6.4 ForwardQFTPipelineComplete

iqft8(W6.3, 역-QFT) 비대칭 닫기. 정-QFT pipeline이 cr6/7/8_gate(non-dag) 미봉인으로 막혀 있던 것을
3개 analytic 게이트 봉인으로 잠금해제 → forward QFT pipeline을 n=8까지 완결. self-contained·Tier-0.

분해 패턴(qft4_pipeline에서 도출, big-endian qubit0=MSB):
 1. t=0→n-1: H(t); 그 후 c=t+1→n-1 로 controlled-phase(control=c, target=t), k=(c-t)+1.
    모듈 매핑: k=2→cs_gate, k=3→ct_gate, k≥4→cr{k}_gate.
 2. 비트반전 swap(i, n-1-i) for i<n//2.
 3. golden = raw QFT = DFT(2^n)/√(2^n) (w=exp(2πi/N)).

cr_k_gate(non-dag) 봉인: bloq=ZPowGate(exponent=1/2**(k-1)).controlled(), golden=diag(1,1,1,exp(2πi/2^k)).

정직성 경계:
 - ★RegressionGate: gen_qft_pipeline(4) 가 봉인된 qft4_pipeline 로 재봉인(composite==golden + u_hash 일치)
   되면 패턴 정확성 입증.
 - 생성≠검증: 오라클(verify_seal 모듈·app_assemble 앱) 통과로만 SEALED. plan=봉인 모듈, MatrixGate 0.
 - 비파괴 성장: 모듈 3+앱 4 가산, 기존 봉인(qft2/3/4_pipeline)/frozen 23키/fingerprint byte-identical.
 - second_oracle INDEP 에 cr6/7/8_gate(=cphase(k)) 추가 필요(coverage 50→53 유지) — 별도 편집.

사용:  python scripts/qft_family.py
"""
from __future__ import annotations

import os
import sys
import json
import subprocess

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, ORACLE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import verify_seal as vs        # noqa: E402  (hash_unitary 사용만)
import app_assemble as aa       # noqa: E402  (앱 봉인 — 사용만)

SPECS_MODS = os.path.join(ROOT, "specs", "modules")
SPECS_APPS = os.path.join(ROOT, "specs", "apps")
MODREG = os.path.join(ROOT, "registry", "modules")
APPREG = os.path.join(ROOT, "registry", "apps")
OUT = os.path.join(ROOT, ".pgf", "arith")


def _cr_gate_spec(k):
    """cr{k}_gate(non-dag) 모듈 spec — controlled-R_k = diag(1,1,1,exp(2πi/2^k))."""
    return (
        "```python id=bloq\n"
        "from qualtran.bloqs.basic_gates import ZPowGate\n"
        f"bloq = ZPowGate(exponent=1/2**({k}-1)).controlled()\n"
        "```\n"
        "```python id=golden\n"
        "import numpy as np\n"
        f"# controlled-R{k} (control=first, big-endian): diag(1,1,1, exp(2*pi*i/2**{k}))\n"
        f"golden = np.diag([1, 1, 1, np.exp(2j*np.pi/2**{k})]).astype(complex)\n"
        "```\n"
        '```json id=meta\n'
        f'{{"id": "cr{k}_gate", "n_sys": 2, "n_anc": 0}}\n'
        "```\n")


def seal_cr_gate(k):
    """cr{k}_gate 모듈 봉인 → registry/modules (canonical 성장). 독립 cphase(k) u_hash 대조."""
    sp = os.path.join(SPECS_MODS, f"cr{k}_gate.pg")
    open(sp, "w", encoding="utf-8", newline="\n").write(_cr_gate_spec(k))
    subprocess.run([sys.executable, os.path.join(ORACLE, "verify_seal.py"), sp, "--out", MODREG],
                   capture_output=True, text=True, cwd=ORACLE)
    seal_path = os.path.join(MODREG, f"cr{k}_gate.sealed.json")
    if not os.path.exists(seal_path):
        return {"id": f"cr{k}_gate", "sealed": False}
    sealed = json.load(open(seal_path))
    indep = vs.hash_unitary(np.diag([1, 1, 1, np.exp(2j * np.pi / 2 ** k)]).astype(complex))
    return {"id": f"cr{k}_gate", "sealed": True, "tier": sealed.get("tier"),
            "u_hash": sealed["u_hash"], "independent_match": indep == sealed["u_hash"]}


def _qft_phase_module(k):
    return {2: "cs_gate", 3: "ct_gate"}.get(k, f"cr{k}_gate")


def gen_qft_pipeline(n):
    """n-큐비트 forward-QFT decomposed pipeline app spec. golden=raw QFT, plan=봉인 모듈 사다리."""
    steps = []
    deps = set()
    for t in range(n):
        steps.append({"spec": "../modules/h_gate.pg", "targets": [t]})
        for c in range(t + 1, n):
            k = (c - t) + 1
            mod = _qft_phase_module(k)
            deps.add(mod)
            steps.append({"spec": f"../modules/{mod}.pg", "targets": [c, t]})
    for i in range(n // 2):
        steps.append({"spec": "../modules/swap2.pg", "targets": [i, n - 1 - i]})
    deps.update({"h_gate", "swap2"})

    N = 1 << n
    header = (f"# qft{n}_pipeline — forward QFT on {n} qubits (decomposed pipeline). "
              f"H + controlled-R_m 사다리 + 비트반전 swap. raw QFT{n} 재발견. "
              f"genskill-free generator(qft_family). 봉인 모듈 {sorted(deps)}, no MatrixGate.\n")
    spec = (
        header +
        '```json id=app_meta\n'
        f'{{"id": "qft{n}_pipeline", "n_sys": {n}, "n_anc": 0}}\n'
        "```\n"
        "```python id=app_golden\n"
        "import numpy as np\n"
        f"N={N}; w=np.exp(2j*np.pi/N)\n"
        "golden = np.array([[w**(j*k) for k in range(N)] for j in range(N)],dtype=complex)/np.sqrt(N)\n"
        "```\n"
        "```json id=plan\n"
        f"{json.dumps({'steps': steps})}\n"
        "```\n")
    return spec, sorted(deps)


def _independent_qft(n):
    N = 1 << n
    i = np.arange(N).reshape(N, 1); j = np.arange(N).reshape(1, N)
    return vs.hash_unitary((np.exp(2j * np.pi * (i * j) / N) / np.sqrt(N)).astype(complex))


def regression_gate(n=4):
    """★ gen_qft_pipeline(n) 이 봉인된 qft{n}_pipeline 로 재봉인 → composite==golden + u_hash 일치?"""
    spec, deps = gen_qft_pipeline(n)
    tmp_store = os.path.join(OUT, "_qftreg")
    os.makedirs(tmp_store, exist_ok=True)
    sp = os.path.join(SPECS_APPS, f"_qftreg_qft{n}_pipeline.app.pg")
    open(sp, "w", encoding="utf-8", newline="\n").write(spec)
    try:
        v = aa.assemble(sp, tmp_store)
        reg_path = os.path.join(APPREG, f"qft{n}_pipeline.sealed.json")
        reg = json.load(open(reg_path))["u_hash"] if os.path.exists(reg_path) else None
        return {"n": n, "sealed": bool(v.sealed), "regenerated_u_hash": (v.u_hash or "")[:16],
                "registry_u_hash": (reg or "")[:16],
                "matches_registry": bool(v.sealed) and reg is not None and v.u_hash == reg,
                "deps": deps, "reason": v.reason}
    finally:
        try:
            os.remove(sp)
        except OSError:
            pass


def forge_qft(n):
    spec, deps = gen_qft_pipeline(n)
    sp = os.path.join(SPECS_APPS, f"qft{n}_pipeline.app.pg")
    open(sp, "w", encoding="utf-8", newline="\n").write(spec)
    v = aa.assemble(sp, APPREG)
    used = sorted(d for d in deps if d.startswith("cr") and d.endswith("_gate"))
    return {"id": f"qft{n}_pipeline", "n_sys": n, "sealed": bool(v.sealed), "tier": v.tier,
            "u_hash": v.u_hash, "deps": deps, "cr_gates_used": used}


def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 74)
    print("W6.4 ForwardQFTPipelineComplete — cr6/7/8_gate 봉인 → 정-QFT pipeline n=8 완결")
    print("정직성: 생성≠검증(오라클). iqft8(W6.3) 정-방향 대칭. 모듈3+앱4 가산.")
    print("=" * 74)

    # A. SealCrGates (cr6/7/8_gate)
    cr = [seal_cr_gate(k) for k in (6, 7, 8)]
    for c in cr:
        print(f"[SealCrGate] {c['id']:10} sealed={c['sealed']} tier={c.get('tier')} "
              f"indep_match={c.get('independent_match')} u={str(c.get('u_hash'))[:14]}")

    # C. RegressionGate (B 생성기 정확성)
    reg = regression_gate(4)
    print(f"[RegressionGate] gen_qft_pipeline(4) 재봉인 sealed={reg['sealed']} "
          f"u={reg['regenerated_u_hash']} vs qft4_pipeline={reg['registry_u_hash']} "
          f"→ MATCH={reg['matches_registry']}")
    if not reg["matches_registry"]:
        print(f"   ✗ 패턴 불일치 — reason={reg['reason']}")

    # D. ForgeQft (qft5/6/7/8_pipeline)
    forged = [forge_qft(n) for n in (5, 6, 7, 8)]
    for f in forged:
        print(f"[ForgeQft] {f['id']:16} sealed={f['sealed']} tier={f['tier']} "
              f"cr_gates={f['cr_gates_used']} u={str(f['u_hash'])[:14]}")

    # 독립 검증: QFT_n 독립 재구성 → sealed u_hash 대조
    indep = []
    for n in (5, 6, 7, 8):
        sealed = json.load(open(os.path.join(APPREG, f"qft{n}_pipeline.sealed.json")))["u_hash"]
        m = _independent_qft(n) == sealed
        indep.append({"n": n, "matches_sealed": m})
        print(f"[IndependentVerify] QFT{n} 독립 재구성 u_hash=={('sealed' if m else 'MISMATCH')}")

    report = {
        "phase": "W6.4 ForwardQFTPipelineComplete",
        "honesty": "cr_k_gate(non-dag) analytic golden (ZPowGate ctrl); generation != verification "
                   "(verify_seal modules / app_assemble apps); regression gate proves pattern "
                   "(gen(4)==qft4_pipeline); modules+apps additive (frozen keys/fingerprint byte-identical).",
        "seal_cr_gates": cr, "regression_gate_qft4": reg,
        "forge_qft": forged, "independent_verify": indep,
    }
    all_ok = (all(c["sealed"] and c.get("independent_match") for c in cr)
              and reg["matches_registry"]
              and all(f["sealed"] and f["tier"] == 0 for f in forged)
              and all(f["cr_gates_used"] for f in forged if f["n_sys"] >= 6)
              and all(x["matches_sealed"] for x in indep))
    report["all_ok"] = bool(all_ok)
    json.dump(report, open(os.path.join(OUT, "QFT-FORWARD-REPORT.json"), "w",
                           encoding="utf-8"), ensure_ascii=False, indent=2)
    print("-" * 74)
    print(f"all_ok={all_ok}  →  .pgf/arith/QFT-FORWARD-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
