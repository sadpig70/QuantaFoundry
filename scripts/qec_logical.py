# -*- coding: utf-8 -*-
"""
qec_logical.py — Stage 7 W7.3 FaultTolerantLogicalGates

QEC 서사의 클라이맥스: Steane [[7,1,3]] 의 **transversal 논리 Clifford 게이트**(fault-tolerance 실체).
전부 Clifford → Tier-2 stabilizer-tableau 봉인(dense-free). 특히 논리 CNOT(14q)=2^14 dense 불가 →
Tier-2 의 dense-free 강점을 *처음으로 스케일*에서 실증.

봉인 대상(Tier-2 CLIFFORD 모듈):
 1. steane_logical_h    논리 H = H^⊗7         (7q). 코드보존, 논리 H 중첩.
 2. steane_logical_s    논리 S = S†^⊗7        (7q). transversal S†가 논리 S(+i)를 구현.
 3. steane_logical_cnot 논리 CNOT = CNOT^⊗7   (14q, 블록 A=0..6 control, B=7..13 target).

정직성 경계:
 - Steane=doubly-even self-dual CSS → transversal {H,S,CNOT} 전부 코드보존 valid 논리연산.
 - 명명=봉인 게이트가 *구현하는* 논리연산(transversal S=논리 S† 이므로 논리 S는 S†^⊗7로 봉인).
 - Tier-2 seal=정준 tableau(표현무관, dense-free). 논리-정확성은 **드라이버 witness(오라클 독립)**:
   n=7 dense 작용 / n=14 논리기저 벡터(2^14, full unitary 미실체화) 작용. W7.2 |0_L>/|1_L> prep 재사용.
 - second_oracle(dense)=Tier-0 53 범위 → 이 Tier-2 모듈은 tableau+witness(정직 분리).
 - plan=Clifford(H·CNOT·ZPowGate(-0.5)), MatrixGate 0. 비파괴: 모듈 56→59, 앱 75 불변.

사용:  python scripts/qec_logical.py
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
import verify_seal as vs        # noqa: E402  (Tier-2 봉인 CLI — 사용만)
import clifford_seal as cs      # noqa: E402  (정준 tableau 독립 재확인 — 사용만)
import qec_clifford as qc       # noqa: E402  (Steane |0_L>/|1_L> prep 회로 재사용)

SPECS_MODS = os.path.join(ROOT, "specs", "modules")
MODREG = os.path.join(ROOT, "registry", "modules")
OUT = os.path.join(ROOT, ".pgf", "arith")


# 게이트 단계: ("h",q)·("sdg",q)=S†·("cnot",c,t)
SPECS = {
    "steane_logical_h": dict(n=7, gates=[("h", i) for i in range(7)],
                             note="논리 H = H^⊗7 (Steane transversal)."),
    "steane_logical_s": dict(n=7, gates=[("sdg", i) for i in range(7)],
                             note="논리 S = S†^⊗7 (transversal S†가 논리 S 구현)."),
    "steane_logical_cnot": dict(n=14, gates=[("cnot", i, i + 7) for i in range(7)],
                                note="논리 CNOT = CNOT^⊗7 (블록 A=0..6 → B=7..13). 14q Tier-2 dense-free."),
}


def _bloq_code(n, gates):
    L = ["from qualtran import BloqBuilder",
         "from qualtran.bloqs.basic_gates import Hadamard, CNOT, ZPowGate",
         "bb = BloqBuilder()",
         f"qs = [bb.add_register(f'q{{i}}', 1) for i in range({n})]"]
    for g in gates:
        if g[0] == "h":
            L.append(f"qs[{g[1]}] = bb.add(Hadamard(), q=qs[{g[1]}])")
        elif g[0] == "sdg":
            L.append(f"qs[{g[1]}] = bb.add(ZPowGate(exponent=-0.5), q=qs[{g[1]}])")
        else:
            c, t = g[1], g[2]
            L.append(f"qs[{c}], qs[{t}] = bb.add(CNOT(), ctrl=qs[{c}], target=qs[{t}])")
    L.append(f"bloq = bb.finalize(**{{f'q{{i}}': qs[i] for i in range({n})}})")
    return "\n".join(L)


def gen_spec(name):
    s = SPECS[name]
    header = (f"# {name} — {s['note']} Tier-2 CLIFFORD(정준 stabilizer tableau, dense 미사용). "
              f"plan=Clifford 게이트, no MatrixGate. 논리-정확성 witness=qec_logical 드라이버.\n")
    return (header +
            "```python id=bloq\n" + _bloq_code(s["n"], s["gates"]) + "\n```\n"
            '```json id=meta\n'
            f'{{"id": "{name}", "n_sys": {s["n"]}, "n_anc": 0, "tier": "clifford"}}\n'
            "```\n")


# ── 논리상태 (W7.2 prep 재사용) ────────────────────────────────────────────────
def _logical_states():
    psi0 = qc._state(7, qc._steane_zero_gates())
    psi1 = qc._state(7, qc._steane_one_gates())
    return psi0, psi1


def _kron_single(single, nq, qubits):
    U = np.array([[1.0 + 0j]])
    qs = set(qubits)
    for q in range(nq):
        U = np.kron(U, single if q in qs else np.eye(2, dtype=complex))
    return U


def _witness_h(psi0, psi1):
    H1 = np.array([[1, 1], [1, -1]], complex) / np.sqrt(2)
    HL = _kron_single(H1, 7, range(7))
    ok0 = np.allclose(HL @ psi0, (psi0 + psi1) / np.sqrt(2))
    ok1 = np.allclose(HL @ psi1, (psi0 - psi1) / np.sqrt(2))
    return {"logical": "H", "zero_to_plus": bool(ok0), "one_to_minus": bool(ok1),
            "pass": bool(ok0 and ok1)}


def _witness_s(psi0, psi1):
    Sd = np.array([[1, 0], [0, -1j]], complex)        # S† = diag(1,-i)
    SL = _kron_single(Sd, 7, range(7))
    a0 = SL @ psi0
    a1 = SL @ psi1
    i0 = int(np.argmax(np.abs(psi0))); i1 = int(np.argmax(np.abs(psi1)))
    r0 = a0[i0] / psi0[i0]; r1 = a1[i1] / psi1[i1]
    preserve = np.allclose(a0, r0 * psi0) and np.allclose(a1, r1 * psi1)
    rel = r1 / r0
    is_logical_s = np.isclose(rel, 1j)               # +i ⟺ 논리 S
    return {"logical": "S", "code_preserving": bool(preserve),
            "relative_phase": [float(np.real(rel)), float(np.imag(rel))],
            "is_logical_S(+i)": bool(is_logical_s), "pass": bool(preserve and is_logical_s)}


def _witness_cnot(psi0, psi1):
    """14q transversal CNOT: |ab_L>=psi_a⊗psi_b → |a,a⊕b_L>. 논리기저 4개(벡터작용, dense unitary 미실체화)."""
    nq = 14
    P = {0: psi0, 1: psi1}

    def lstate(a, b):
        return np.kron(P[a], P[b])

    def cnot_trans(vec):
        out = vec.copy()
        for i in range(7):
            t = i + 7
            new = np.zeros_like(out)
            ctrl_pos = nq - 1 - i
            tgt_pos = nq - 1 - t
            for s in range(1 << nq):
                if (s >> ctrl_pos) & 1:
                    new[s ^ (1 << tgt_pos)] += out[s]
                else:
                    new[s] += out[s]
            out = new
        return out

    ok = all(np.allclose(cnot_trans(lstate(a, b)), lstate(a, a ^ b))
             for a in (0, 1) for b in (0, 1))
    return {"logical": "CNOT", "basis_4of4": bool(ok), "n_qubits": nq,
            "dense_free": "2^14 dense 불가 → Tier-2 tableau (dense-free) 실증", "pass": bool(ok)}


def seal(name):
    spec = gen_spec(name)
    sp = os.path.join(SPECS_MODS, f"{name}.pg")
    open(sp, "w", encoding="utf-8", newline="\n").write(spec)
    rc = subprocess.run([sys.executable, os.path.join(ORACLE, "verify_seal.py"), sp, "--out", MODREG],
                        capture_output=True, text=True, cwd=ORACLE).returncode
    seal_path = os.path.join(MODREG, f"{name}.sealed.json")
    if rc != 0 or not os.path.exists(seal_path):
        return {"id": name, "sealed": False}
    sealed = json.load(open(seal_path, encoding="utf-8"))
    bloq = vs.instantiate(spec.split("id=bloq\n")[1].split("```")[0], "bloq")
    indep_hash, _ = cs.canonical_tableau_hash(bloq)
    return {"id": name, "n_sys": sealed["n_sys"], "sealed": True, "tier": sealed["tier"],
            "u_hash": sealed["u_hash"], "tableau_recompute_match": indep_hash == sealed["u_hash"]}


def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 82)
    print("W7.3 FaultTolerantLogicalGates — Steane transversal 논리 Clifford(QEC 클래스 완성)")
    print("Tier-2 dense-free. 논리 CNOT 14q = 2^14 dense 불가 → Tier-2 스케일 강점 실증.")
    print("=" * 82)

    sealed = [seal(n) for n in ("steane_logical_h", "steane_logical_s", "steane_logical_cnot")]
    for s in sealed:
        print(f"[Seal-T2] {s['id']:21} n_sys={s.get('n_sys'):2} sealed={s['sealed']} "
              f"tier={s.get('tier')} tableau_recompute={s.get('tableau_recompute_match')} "
              f"u={str(s.get('u_hash'))[:14]}")

    psi0, psi1 = _logical_states()
    wh = _witness_h(psi0, psi1)
    ws = _witness_s(psi0, psi1)
    wc = _witness_cnot(psi0, psi1)
    print(f"[Witness] H̄   : |0_L>→|+_L>={wh['zero_to_plus']} |1_L>→|-_L>={wh['one_to_minus']} → {wh['pass']}")
    print(f"[Witness] S̄   : code보존={ws['code_preserving']} 상대위상={np.round(ws['relative_phase'][0]+1j*ws['relative_phase'][1],3)} "
          f"논리S(+i)={ws['is_logical_S(+i)']} → {ws['pass']}")
    print(f"[Witness] CNOT̄: 논리기저 |ab_L>→|a,a⊕b_L> 4/4={wc['basis_4of4']} (14q dense-free) → {wc['pass']}")

    report = {
        "phase": "W7.3 FaultTolerantLogicalGates",
        "honesty": "Steane doubly-even self-dual CSS → transversal {H,S,CNOT} are code-preserving valid "
                   "logical operations. Named by the logical op they implement (transversal S = logical "
                   "S†, so logical S is sealed as S†^⊗7). Tier-2 seal = canonical stabilizer tableau "
                   "(dense-free); logical correctness is an INDEPENDENT driver witness (n=7 dense action / "
                   "n=14 logical-basis vector action, full unitary not materialized). The 14-qubit logical "
                   "CNOT cannot be Tier-0 dense (2^14) — it demonstrates Tier-2's dense-free advantage at "
                   "scale. second_oracle (dense) covers the 53 Tier-0 modules; these are tableau-sealed.",
        "seals": sealed,
        "witness": {"H": wh, "S": ws, "CNOT": wc},
    }
    all_ok = (all(s["sealed"] and s["tier"] == 2 and s["tableau_recompute_match"] for s in sealed)
              and wh["pass"] and ws["pass"] and wc["pass"])
    report["all_ok"] = bool(all_ok)
    json.dump(report, open(os.path.join(OUT, "QEC-LOGICAL-REPORT.json"), "w",
                           encoding="utf-8"), ensure_ascii=False, indent=2)
    print("-" * 82)
    print(f"all_ok={all_ok}  →  .pgf/arith/QEC-LOGICAL-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
