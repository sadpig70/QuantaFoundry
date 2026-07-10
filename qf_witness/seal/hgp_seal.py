#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hgp_seal.py — TrackHE8 P4: Tillich-Zémor 하이퍼그래프곱 qLDPC [[27,4,3]] |0_L⟩ prep Tier-2 봉인.

HGP(Hamming[7,4,3] × rep[3]) = [[27,4,3]] — §3k P6 "hypergraph-product 대형 아직 없음" 개창.
기봉인 qldpc_hgp([[8,1,2]] Tier-0 소형)의 **거리-3 대형 확장**. 27q → Tier-2 CLIFFORD(정준 stabilizer
tableau, dense 2^27 불필요, concat_513_513 선례).
  ★선검증 확정(scratchpad): CSS(Hx Hz^T=0)·N=27·k=4·**양 transpose 부호 trivial(dim0)→d=3 보존**(Agent8
  d^⊥ 비대칭 함정 회피)·weight≤2 logical 부재→d≥3 명시·|0_L⟩ prep 64 H+CNOT 전-Clifford.
|0_L⟩ = ∏(I+S_X)|0^27⟩: X-안정자 RREF pivot → H(pivot)+CNOT(pivot→support) 확산(qldpc_hgp 패턴).
봉인: verify_seal module-level tier="clifford" 정준 tableau(dense 미사용, n=27 정확) → registry/modules.
  독립 재확인 = clifford_seal.canonical_tableau_hash. 신규 module 0(bloq H/CNOT). 정직 경계: 봉인=|0_L⟩
  prep Clifford 회로 tableau exact; 거리 3 달성·decoder(BP+OSD)·임계값·대형 일반화=관측/범위밖.
witness=hgp_observe(CSS·k·거리·|0_L⟩ 코드공간 stabilized, 오라클 독립).

사용: python -m qf_witness.seal.hgp_seal
"""
from __future__ import annotations
import os, sys, json, subprocess
import numpy as np

from qf_witness.core.paths import ROOT
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, ORACLE)
import verify_seal as vs        # noqa: E402  (Tier-2 봉인 CLI — 사용만)
import clifford_seal as cs      # noqa: E402  (정준 tableau 독립 재확인 — 사용만)

SPECS_MODS = os.path.join(ROOT, "specs", "modules")
MODREG = os.path.join(ROOT, "registry", "modules")

# 고전 시드
H1 = np.array([[1, 1, 0, 1, 1, 0, 0], [1, 0, 1, 1, 0, 1, 0], [0, 1, 1, 1, 0, 0, 1]]) % 2   # Hamming[7,4,3]
H2 = np.array([[1, 1, 0], [0, 1, 1]]) % 2                                                    # rep[3]


def _kron2(A, B):
    return np.kron(A, B) % 2


def hgp_matrices():
    r1, n1 = H1.shape
    r2, n2 = H2.shape
    Hx = np.hstack([_kron2(H1, np.eye(n2, dtype=int)), _kron2(np.eye(r1, dtype=int), H2.T)]) % 2
    Hz = np.hstack([_kron2(np.eye(n1, dtype=int), H2), _kron2(H1.T, np.eye(r2, dtype=int))]) % 2
    N = n1 * n2 + r1 * r2
    return Hx, Hz, N


def _rref(M):
    M = M.copy() % 2
    rows, cols = M.shape
    pivots = []
    r = 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i, c]), None)
        if piv is None:
            continue
        M[[r, piv]] = M[[piv, r]]
        for i in range(rows):
            if i != r and M[i, c]:
                M[i] ^= M[r]
        pivots.append(c)
        r += 1
    return M[:r], pivots


def prep_gates():
    """|0_L⟩ prep = X-안정자 RREF pivot 별 H(pivot)+CNOT(pivot→non-pivot support). 결정론."""
    Hx, _, N = hgp_matrices()
    Rx, pivots = _rref(Hx)
    gates = []
    for row, p in zip(Rx, pivots):
        gates.append(("h", p))
        for j in range(N):
            if row[j] and j != p:
                gates.append(("cnot", p, j))
    return gates, N


def _bloq_code(n, gates):
    L = ["from qualtran import BloqBuilder",
         "from qualtran.bloqs.basic_gates import Hadamard, CNOT",
         "bb = BloqBuilder()",
         f"qs = [bb.add_register(f'q{{i}}', 1) for i in range({n})]"]
    for g in gates:
        if g[0] == "h":
            L.append(f"qs[{g[1]}] = bb.add(Hadamard(), q=qs[{g[1]}])")
        else:
            c, t = g[1], g[2]
            L.append(f"qs[{c}], qs[{t}] = bb.add(CNOT(), ctrl=qs[{c}], target=qs[{t}])")
    L.append(f"bloq = bb.finalize(**{{f'q{{i}}': qs[i] for i in range({n})}})")
    return "\n".join(L)


HEADER = ("hgp_qldpc27 — Tillich-Zémor 하이퍼그래프곱 qLDPC [[27,4,3]] |0_L⟩ prep (HGP(Hamming[7,4,3]×rep[3])). "
          "§3k P6 hypergraph-product 대형 개창, 기봉인 qldpc_hgp([[8,1,2]])의 거리-3 대형 확장. Tier-2 CLIFFORD "
          "(정준 stabilizer tableau, dense 2^27 불필요). ★선검증: CSS(Hx Hz^T=0)·k=4·양 transpose trivial→d=3 "
          "보존(비대칭 회피)·weight≤2 logical 부재. plan=X-안정자 RREF H·CNOT, no MatrixGate, 신규 module 0. "
          "witness=hgp_observe(CSS·거리·|0_L⟩ stabilized, 오라클 독립).")


def gen_spec():
    gates, n = prep_gates()
    return ("# " + HEADER + "\n"
            "```python id=bloq\n" + _bloq_code(n, gates) + "\n```\n"
            '```json id=meta\n'
            f'{{"id": "hgp_qldpc27", "n_sys": {n}, "n_anc": 0, "tier": "clifford"}}\n'
            "```\n")


def main():
    name = "hgp_qldpc27"
    sp = os.path.join(SPECS_MODS, f"{name}.pg")
    open(sp, "w", encoding="utf-8", newline="\n").write(gen_spec())
    rc = subprocess.run([sys.executable, os.path.join(ORACLE, "verify_seal.py"), sp,
                         "--out", MODREG], capture_output=True, text=True, cwd=ORACLE).returncode
    seal_path = os.path.join(MODREG, f"{name}.sealed.json")
    if rc != 0 or not os.path.exists(seal_path):
        print(f"[Seal-T2] {name} FAILED rc={rc}")
        return 1
    sealed = json.load(open(seal_path, encoding="utf-8"))
    bloq = vs.instantiate(open(sp, encoding="utf-8").read()
                          .split("id=bloq\n")[1].split("```")[0], "bloq")
    indep_hash, nq = cs.canonical_tableau_hash(bloq)
    match = indep_hash == sealed["u_hash"]
    print(f"[Seal-T2] {name} n_sys={sealed['n_sys']} tier={sealed['tier']} n_qubits={nq} "
          f"u_hash={sealed['u_hash'][:14]}.. tableau_recompute_match={match}")
    return 0 if match else 1


if __name__ == "__main__":
    sys.exit(main())
