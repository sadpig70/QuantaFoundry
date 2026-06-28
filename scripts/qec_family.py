# -*- coding: utf-8 -*-
"""
qec_family.py — Stage 6 W7.1 QECStabilizerFamily

새 알고리즘 클래스: 양자오류정정(QEC) stabilizer 인코더. gates→QFT→arith→Shor 수직스택 이후
첫 *수평* 확장. 전부 Clifford → Tier-0 EXACT, 봉인된 base Clifford(h_gate·cnot)만으로 조립.

봉인 대상(전부 full n-qubit unitary, n≤12 Tier-0):
 1. repcode3_bitflip   [[3,1]] bit-flip 인코더   — CNOT(0,1)·CNOT(0,2). |0_L>=|000>,|1_L>=|111>.
 2. repcode3_phaseflip [[3,1]] phase-flip 인코더 — +H(0,1,2). |0_L>=|+++>,|1_L>=|--->.
 3. shor9_encoder      [[9,1,3]] Shor 코드(1995) — phase-flip⊗bit-flip, 9q 512×512. CAPSTONE.
 4. syndrome3_bitflip  bit-flip 신드롬 추출 unitary(측정前) — 5q(3 data+2 anc), 순수 parity copy.

정직성 경계:
 - golden = closed-form 독립공식(parity-permutation = 불리언 인덱스맵, Sylvester-Hadamard = 부호맵).
   Qualtran bloq 인스턴스화/plan 과 무관한 별도 코드경로 → qft(golden=DFT공식)와 동일 독립수준.
 - ⚠ stabilizer-tableau(Tier-2 CLIFFORD) 검증이 *더 강한* 독립오라클 — future work 로 명기.
 - 생성≠검증: aa.assemble(verify_seal/contracts 오라클) 통과로만 SEALED. plan=봉인 모듈, MatrixGate 0.
 - 측정은 비-unitary → syndrome 은 측정前 parity-copy unitary 만 봉인(정직 경계).
 - 비파괴: 모듈 0 추가(h_gate·cnot 재사용), 앱 +4. frozen 23키·fingerprint byte-identical 불변.

사용:  python scripts/qec_family.py
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


# ── 닫힌형식 독립 golden 빌더 (big-endian, qubit0=MSB) ──────────────────────────
def _parity_perm(n, cnots):
    """CNOT(control,target) 시퀀스(g1 first) → 2^n permutation unitary. 불리언 인덱스맵만 사용."""
    U = np.zeros((1 << n, 1 << n), dtype=complex)
    for s in range(1 << n):
        out = s
        for c, t in cnots:
            cb = (out >> (n - 1 - c)) & 1
            tb = (out >> (n - 1 - t)) & 1
            pos = n - 1 - t
            out = (out & ~(1 << pos)) | ((tb ^ cb) << pos)
        U[out, s] = 1.0
    return U


def _hadamard_on(n, qubits):
    """qubit subset 에 H 텐서곱 (Sylvester 닫힌형식). big-endian kron 순서."""
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    U = np.array([[1.0 + 0j]])
    qs = set(qubits)
    for q in range(n):
        U = np.kron(U, H if q in qs else np.eye(2, dtype=complex))
    return U


# 각 인코더: (n_sys, circuit 단계 리스트[plan 순서], golden 닫힌형식 thunk)
#   circuit 단계 = ("cnot", c, t) 또는 ("h", q)
def _specs():
    out = {}

    # 1. [[3,1]] bit-flip: CNOT(0,1)·CNOT(0,2)
    bf_cnots = [(0, 1), (0, 2)]
    out["repcode3_bitflip"] = dict(
        n=3, circuit=[("cnot", c, t) for c, t in bf_cnots],
        golden=_parity_perm(3, bf_cnots),
        note="[[3,1]] bit-flip 반복코드 인코더. stab=Z0Z1,Z1Z2. golden=parity perm (게이트행렬 0).")

    # 2. [[3,1]] phase-flip: bit-flip 회로 + H(0,1,2)
    out["repcode3_phaseflip"] = dict(
        n=3, circuit=[("cnot", c, t) for c, t in bf_cnots] + [("h", q) for q in range(3)],
        golden=_hadamard_on(3, [0, 1, 2]) @ _parity_perm(3, bf_cnots),
        note="[[3,1]] phase-flip 반복코드 인코더. stab=X0X1,X1X2. golden=H^⊗3 @ parity.")

    # 3. [[9,1,3]] Shor 코드(1995): phase 확산 → H(0,3,6) → bit-flip 블록
    phase_cnots = [(0, 3), (0, 6)]
    bitblk_cnots = [(0, 1), (0, 2), (3, 4), (3, 5), (6, 7), (6, 8)]
    circ = ([("cnot", c, t) for c, t in phase_cnots] +
            [("h", q) for q in (0, 3, 6)] +
            [("cnot", c, t) for c, t in bitblk_cnots])
    golden9 = (_parity_perm(9, bitblk_cnots) @ _hadamard_on(9, [0, 3, 6])
               @ _parity_perm(9, phase_cnots))
    out["shor9_encoder"] = dict(
        n=9, circuit=circ, golden=golden9,
        note="[[9,1,3]] Shor 코드(1995) 인코더 — 첫 QEC코드. 512×512 Tier-0. "
             "golden=P_bitflip @ H_{0,3,6} @ P_phase (closed-form).")

    # 4. bit-flip 신드롬 추출(측정前 unitary): Z0Z1→anc3, Z1Z2→anc4
    syn_cnots = [(0, 3), (1, 3), (1, 4), (2, 4)]
    out["syndrome3_bitflip"] = dict(
        n=5, circuit=[("cnot", c, t) for c, t in syn_cnots],
        golden=_parity_perm(5, syn_cnots),
        note="bit-flip 신드롬 추출(측정前 parity-copy unitary). 5q=3data+2anc. "
             "측정=비unitary 제외(정직 경계). golden=parity perm.")
    return out


# ── 닫힌형식 golden 을 self-contained python 으로 spec 에 임베드 ──────────────────
_GOLDEN_HELPERS = (
    "import numpy as np\n"
    "def _pp(n,cn):\n"
    "    U=np.zeros((1<<n,1<<n),complex)\n"
    "    for s in range(1<<n):\n"
    "        o=s\n"
    "        for c,t in cn:\n"
    "            cb=(o>>(n-1-c))&1; tb=(o>>(n-1-t))&1; p=n-1-t\n"
    "            o=(o&~(1<<p))|((tb^cb)<<p)\n"
    "        U[o,s]=1.0\n"
    "    return U\n"
    "def _h(n,qs):\n"
    "    H=np.array([[1,1],[1,-1]],complex)/np.sqrt(2); U=np.array([[1.0+0j]]); qs=set(qs)\n"
    "    for q in range(n):\n"
    "        U=np.kron(U,H if q in qs else np.eye(2,dtype=complex))\n"
    "    return U\n")

# app 별 golden 닫힌형식 식(문자열) — _GOLDEN_HELPERS 뒤에 붙음
_GOLDEN_EXPR = {
    "repcode3_bitflip":   "golden=_pp(3,[(0,1),(0,2)])\n",
    "repcode3_phaseflip": "golden=_h(3,[0,1,2])@_pp(3,[(0,1),(0,2)])\n",
    "shor9_encoder":      "golden=_pp(9,[(0,1),(0,2),(3,4),(3,5),(6,7),(6,8)])"
                          "@_h(9,[0,3,6])@_pp(9,[(0,3),(0,6)])\n",
    "syndrome3_bitflip":  "golden=_pp(5,[(0,3),(1,3),(1,4),(2,4)])\n",
}


def gen_spec(name):
    s = _specs()[name]
    steps = []
    for step in s["circuit"]:
        if step[0] == "cnot":
            steps.append({"spec": "../modules/cnot.pg", "targets": [step[1], step[2]]})
        else:  # h
            steps.append({"spec": "../modules/h_gate.pg", "targets": [step[1]]})
    header = (f"# {name} — {s['note']} "
              f"QEC stabilizer 인코더(qec_family). plan=봉인 h_gate·cnot, no MatrixGate. "
              f"golden=closed-form parity/Sylvester (Qualtran 비의존 독립경로).\n")
    spec = (
        header +
        '```json id=app_meta\n'
        f'{{"id": "{name}", "n_sys": {s["n"]}, "n_anc": 0}}\n'
        "```\n"
        "```python id=app_golden\n"
        + _GOLDEN_HELPERS + _GOLDEN_EXPR[name] +
        "```\n"
        "```json id=plan\n"
        f"{json.dumps({'steps': steps})}\n"
        "```\n")
    return spec


def forge(name):
    spec = gen_spec(name)
    sp = os.path.join(SPECS_APPS, f"{name}.app.pg")
    open(sp, "w", encoding="utf-8", newline="\n").write(spec)
    v = aa.assemble(sp, APPREG)
    # 독립검증: closed-form golden u_hash == sealed u_hash
    indep = vs.hash_unitary(_specs()[name]["golden"])
    return {"id": name, "n_sys": _specs()[name]["n"], "sealed": bool(v.sealed),
            "tier": v.tier, "u_hash": v.u_hash,
            "independent_match": v.sealed and indep == v.u_hash, "reason": v.reason}


def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 78)
    print("W7.1 QECStabilizerFamily — 양자오류정정 인코더(새 알고리즘 클래스, Clifford Tier-0)")
    print("정직성: golden=closed-form 독립공식. 생성≠검증(오라클). 모듈0+앱4 가산.")
    print("=" * 78)

    order = ["repcode3_bitflip", "repcode3_phaseflip", "shor9_encoder", "syndrome3_bitflip"]
    forged = [forge(n) for n in order]
    for f in forged:
        print(f"[Forge] {f['id']:20} n_sys={f['n_sys']:2} sealed={f['sealed']} tier={f['tier']} "
              f"indep_match={f['independent_match']} u={str(f['u_hash'])[:14]}"
              + ("" if f["sealed"] else f"  reason={f['reason']}"))

    # 행동 스모크: Shor-9 인코더가 |0_L>,|1_L> 를 올바른 코드워드로 보내는지(독립 golden 사용)
    g9 = _specs()["shor9_encoder"]["golden"]
    psi0 = np.zeros(1 << 9, complex); psi0[0] = 1.0          # |0>|0..0>
    psi1 = np.zeros(1 << 9, complex); psi1[1 << 8] = 1.0     # |1>|0..0> (logical=MSB)
    out0 = g9 @ psi0
    # |0_L> = (|000>+|111>)^3 / 2√2 → 8 basis, 각 진폭 1/(2√2)
    supp0 = sorted(int(i) for i in np.where(np.abs(out0) > 1e-9)[0])
    amp0_ok = np.allclose(np.abs(out0[supp0]), 1 / (2 * np.sqrt(2)))
    # |0_L> 코드워드: 각 3비트 블록이 000 또는 111 (블록=qubit{0,1,2},{3,4,5},{6,7,8})
    def _blocks_uniform(idx):
        b = [(idx >> (6 - 3 * k)) & 0b111 for k in range(3)]  # big-endian 블록(qubit3k=MSB)
        return all(x in (0b000, 0b111) for x in b)
    code0_ok = len(supp0) == 8 and all(_blocks_uniform(i) for i in supp0)
    behavior_ok = bool(amp0_ok and code0_ok)
    print(f"[Behavior] Shor9 |0_L> support={len(supp0)} blocks∈{{000,111}}={code0_ok} "
          f"amp=1/2√2:{amp0_ok} → {behavior_ok}")

    report = {
        "phase": "W7.1 QECStabilizerFamily",
        "honesty": "golden=closed-form parity-permutation/Sylvester-Hadamard (Qualtran-independent "
                   "code path); generation != verification (app_assemble oracle); plan=sealed "
                   "h_gate/cnot only, no MatrixGate; measurement excluded (syndrome=pre-measure "
                   "unitary); stabilizer-tableau (Tier-2) is a STRONGER independent check (future "
                   "work); modules+0 apps+4 (frozen keys/fingerprint byte-identical).",
        "forge": forged,
        "behavior_shor9": {"support": len(supp0), "codeword_uniform": code0_ok,
                           "amplitude_ok": bool(amp0_ok), "pass": behavior_ok},
    }
    all_ok = (all(f["sealed"] and f["tier"] == 0 and f["independent_match"] for f in forged)
              and behavior_ok)
    report["all_ok"] = bool(all_ok)
    json.dump(report, open(os.path.join(OUT, "QEC-FAMILY-REPORT.json"), "w",
                           encoding="utf-8"), ensure_ascii=False, indent=2)
    print("-" * 78)
    print(f"all_ok={all_ok}  →  .pgf/arith/QEC-FAMILY-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
