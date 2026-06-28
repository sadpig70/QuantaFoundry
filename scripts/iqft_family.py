# -*- coding: utf-8 -*-
"""
iqft_family.py — Stage 6 W6.3 QFTPipelineExtend-cr8 (iqft8)

W2.4가 봉인한 cr8_dag(controlled-R8†)의 직접 결실. c7x payoff(W6.1, 산술 frontier)의 **대칭 쌍** —
7큐비트 역-QFT(`iqft7`, cr3~cr7_dag 사다리)를 **8큐비트 `iqft8`**(cr8_dag 추가)로 확장. 더 큰 QPE
counting register = 위상추정 정밀도. Tier-0(256² ≤ EXACT_BOUND 12), self-contained(relay 불필요).

분해 패턴(봉인된 iqft7에서 도출, big-endian qubit0=MSB, n 큐비트):
 1. 비트반전 swap(i, n-1-i) for i<n//2.
 2. 역-QFT 사다리: t=n-1→0; 각 t에 c=n-1→t+1 로 cr_{(c-t)+1}_dag(control=c, target=t); 그 후 H(t).
    모듈 매핑: k=2→cs_dag(=cr2†), k≥3→cr{k}_dag_gate. n=8 → 최대 k=8 → cr8_dag_gate.
 3. golden = QFT_n† = DFT(2^n)/√(2^n) 의 conj().T (app_golden 경로).

정직성 경계:
 - ★핵심 정합성(RegressionGate): gen_iqft_pipeline(7) 이 봉인된 iqft7 로 *재봉인*(composite==golden
   통과 + u_hash 일치)되면 분해 패턴 정확성 입증. composite≠golden 이면 app_assemble 이 봉인 거부.
 - 생성≠검증: 오라클(app_assemble) 통과로만 SEALED. plan=봉인 모듈(h/swap/cs_dag/cr*_dag), MatrixGate 0.
 - 비파괴 성장: 앱만 가산(모듈 50 불변), 기존 봉인(iqft7/shor21)/frozen 23키/fingerprint byte-identical.

사용:  python scripts/iqft_family.py
"""
from __future__ import annotations

import os
import sys
import json

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, ORACLE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import verify_seal as vs        # noqa: E402  (hash_unitary 사용만)
import app_assemble as aa       # noqa: E402  (앱 봉인 — 사용만)

SPECS_APPS = os.path.join(ROOT, "specs", "apps")
APPREG = os.path.join(ROOT, "registry", "apps")
OUT = os.path.join(ROOT, ".pgf", "arith")


def _crk_dag_module(k):
    """역-QFT 사다리 위상 모듈명. k=2 → cs_dag(=cr2†), k≥3 → cr{k}_dag_gate."""
    return "cs_dag" if k == 2 else f"cr{k}_dag_gate"


def gen_iqft_pipeline(n):
    """n-큐비트 inverse-QFT decomposed pipeline app spec 생성. golden=QFT_n†, plan=봉인 모듈 사다리."""
    steps = []
    # 1. 비트반전 swap
    for i in range(n // 2):
        steps.append({"spec": "../modules/swap2.pg", "targets": [i, n - 1 - i]})
    # 2. 역-QFT 사다리 (t = n-1 → 0)
    deps = set()
    for t in range(n - 1, -1, -1):
        for c in range(n - 1, t, -1):
            k = (c - t) + 1
            mod = _crk_dag_module(k)
            deps.add(mod)
            steps.append({"spec": f"../modules/{mod}.pg", "targets": [c, t]})
        steps.append({"spec": "../modules/h_gate.pg", "targets": [t]})
    deps.update({"swap2", "h_gate"})

    plan = {"steps": steps}
    N = 1 << n
    header = (f"# iqft{n} — inverse QFT on {n} qubits (decomposed pipeline). "
              f"비트반전 swap + controlled-R_m† 사다리 + H. QFT{n}†와 전수 일치. "
              f"genskill-free generator(iqft_family). 봉인 모듈 {sorted(deps)}, no MatrixGate.\n")
    spec = (
        header +
        '```json id=app_meta\n'
        f'{{"id": "iqft{n}", "n_sys": {n}, "n_anc": 0}}\n'
        "```\n"
        "```python id=app_golden\n"
        "import numpy as np\n"
        f"N={N}; w=np.exp(2j*np.pi/N)\n"
        "QFT=np.array([[w**(j*k) for k in range(N)] for j in range(N)],dtype=complex)/np.sqrt(N)\n"
        "golden=QFT.conj().T\n"
        "```\n"
        "```json id=plan\n"
        f"{json.dumps(plan)}\n"
        "```\n")
    return spec, sorted(deps)


def _independent_iqft(n):
    """QFT_n† 독립 재구성(spec golden 코드 미사용) → hash_unitary."""
    N = 1 << n
    i = np.arange(N).reshape(N, 1)
    j = np.arange(N).reshape(1, N)
    qft = np.exp(2j * np.pi * (i * j) / N) / np.sqrt(N)
    return vs.hash_unitary(qft.conj().T.astype(complex))


def regression_gate(n=7):
    """★ gen_iqft_pipeline(n) 이 봉인된 iqft{n} 로 재봉인 → composite==golden 통과 + u_hash 일치?
    임시 store 봉인(registry 불변). 패턴 정확성의 결정적 게이트."""
    spec, deps = gen_iqft_pipeline(n)
    tmp_store = os.path.join(OUT, "_iqftreg")
    os.makedirs(tmp_store, exist_ok=True)
    sp = os.path.join(SPECS_APPS, f"_iqftreg_iqft{n}.app.pg")
    open(sp, "w", encoding="utf-8", newline="\n").write(spec)
    try:
        v = aa.assemble(sp, tmp_store)
        reg_path = os.path.join(APPREG, f"iqft{n}.sealed.json")
        reg = json.load(open(reg_path))["u_hash"] if os.path.exists(reg_path) else None
        return {"n": n, "sealed": bool(v.sealed), "tier": v.tier,
                "regenerated_u_hash": (v.u_hash or "")[:16],
                "registry_u_hash": (reg or "")[:16],
                "matches_registry": bool(v.sealed) and reg is not None and v.u_hash == reg,
                "deps": deps, "reason": v.reason}
    finally:
        try:
            os.remove(sp)
        except OSError:
            pass


def forge_iqft(n):
    """gen_iqft_pipeline(n) → specs/apps + app_assemble 봉인(registry 성장)."""
    spec, deps = gen_iqft_pipeline(n)
    sp = os.path.join(SPECS_APPS, f"iqft{n}.app.pg")
    open(sp, "w", encoding="utf-8", newline="\n").write(spec)
    v = aa.assemble(sp, APPREG)
    return {"id": f"iqft{n}", "n_sys": n, "sealed": bool(v.sealed), "tier": v.tier,
            "u_hash": v.u_hash, "deps": deps, "uses_cr8": "cr8_dag_gate" in deps,
            "reason": v.reason}


def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 74)
    print("W6.3 QFTPipelineExtend-cr8 — cr8_dag 활용 8큐비트 역-QFT(iqft8)")
    print("정직성: 생성≠검증(오라클). 앱만 가산(모듈 불변). c7x payoff의 QFT-frontier 대칭.")
    print("=" * 74)

    # 0. cr8_dag 봉인 전제(W2.4)
    cr8 = os.path.exists(os.path.join(ROOT, "registry", "modules", "cr8_dag_gate.sealed.json"))
    print(f"[Prereq] cr8_dag_gate 봉인 존재(W2.4): {cr8}  (신규 모듈봉인 0 — 앱만 forge)")
    assert cr8, "cr8_dag_gate.sealed.json 부재 — W2.4 봉인 선행 필요"

    # 1. ★ RegressionGate: 생성기가 수기 iqft7 정확 재현?
    reg = regression_gate(7)
    print(f"[RegressionGate] gen_iqft_pipeline(7) 재봉인 sealed={reg['sealed']} tier={reg['tier']} "
          f"u={reg['regenerated_u_hash']} vs iqft7={reg['registry_u_hash']} "
          f"→ MATCH={reg['matches_registry']}")
    if not reg["matches_registry"]:
        print(f"   ✗ 패턴 불일치 — reason={reg['reason']}");
    print(f"   deps(n=7): {reg['deps']}")

    # 2. ForgeIqft8
    f8 = forge_iqft(8)
    print(f"[ForgeIqft8] {f8['id']} sealed={f8['sealed']} tier={f8['tier']} "
          f"cr8_dag 실사용={f8['uses_cr8']} u={str(f8['u_hash'])[:16]}")
    print(f"   deps(n=8): {f8['deps']}")

    # 3. 독립 검증: QFT8† 독립 재구성 → sealed u_hash 대조
    indep = _independent_iqft(8)
    sealed8 = json.load(open(os.path.join(APPREG, "iqft8.sealed.json")))["u_hash"] if f8["sealed"] else None
    indep_match = sealed8 is not None and indep == sealed8
    print(f"[IndependentVerify] QFT8† 독립 재구성 u_hash=={('sealed' if indep_match else 'MISMATCH')} "
          f"({indep[:16]})")

    report = {
        "phase": "W6.3 QFTPipelineExtend-cr8 (iqft8)",
        "honesty": "cr8_dag(W2.4 sealed) consumed by inverse-QFT ladder; generation != verification "
                   "(app_assemble composite==golden seals); regression gate proves pattern (gen(7)==iqft7); "
                   "apps additive (modules unchanged, frozen keys/fingerprint byte-identical).",
        "regression_gate_iqft7": reg,
        "forge_iqft8": f8,
        "independent_verify": {"qft8_dag_u_hash": indep[:16], "matches_sealed": bool(indep_match)},
    }
    all_ok = (reg["matches_registry"] and f8["sealed"] and f8["tier"] == 0
              and f8["uses_cr8"] and indep_match)
    report["all_ok"] = bool(all_ok)
    json.dump(report, open(os.path.join(OUT, "IQFT-FAMILY-REPORT.json"), "w",
                           encoding="utf-8"), ensure_ascii=False, indent=2)
    print("-" * 74)
    print(f"all_ok={all_ok}  →  .pgf/arith/IQFT-FAMILY-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
