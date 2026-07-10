#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bch_seal.py — TrackHE9-pre(§3j 관문 선행): cyclic-BCH CSS [[15,7,3]] |0_L⟩ prep Tier-2 봉인.

이진 순환 Hamming/BCH 부호 C=[15,11,3](생성다항식 g(x)=x⁴+x+1)가 **dual-containing**(C^⊥⊆C)임을
이용한 양자 CSS [[15,7,3]] — registry 첫 **cyclic algebraic CSS 계보**(cyclic shift 대칭·생성다항식
witness). rm15([[15,1,3]] punctured RM)·concat·surface·HGP 와 다른 부호 클래스. 15q>EXACT_BOUND →
Tier-2 CLIFFORD(정준 stabilizer tableau, dense 2^15 불필요, HGP 선례).
  ★선검증 확정(scratchpad): C=[15,11,3] rank 11·dmin 3·**dual-containing**(C^⊥⊆C rowspace & H·H^T=0 mod2)
  → CSS Hx=Hz=H(4×15, C^⊥ 생성) 직교·[[15,2·11−15,3]]=[[15,7,3]].
|0_L⟩ = ∏(I+S_X)|0^15⟩: X-안정자(Hx=H) RREF pivot → H(pivot)+CNOT(pivot→support) 확산.
봉인: verify_seal module tier="clifford" 정준 tableau(dense 미사용, n=15 정확) → registry/modules.
  독립 재확인 = clifford_seal.canonical_tableau_hash. 신규 module 0(bloq H/CNOT). 정직: 봉인=|0_L⟩ prep
  Clifford tableau exact; 거리 3 달성·decoder·cyclic 자기동형 물리 = 관측/범위밖. witness=bch_observe.

사용: python scripts/bch_seal.py
"""
from __future__ import annotations
import os, sys, json, subprocess
import numpy as np

from qf_witness.core.paths import ROOT
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, ORACLE)
import verify_seal as vs        # noqa: E402
import clifford_seal as cs      # noqa: E402

SPECS_MODS = os.path.join(ROOT, "specs", "modules")
MODREG = os.path.join(ROOT, "registry", "modules")

N = 15
GPOLY = [1, 1, 0, 0, 1]         # g(x)=1+x+x^4 (low→high), degree 4 → C=[15,11]


def _cyclic_gen(g, n):
    k = n - (len(g) - 1)
    G = np.zeros((k, n), dtype=int)
    for i in range(k):
        for j, c in enumerate(g):
            G[i, i + j] = c
    return G % 2


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


def _nullspace(G):
    Mr, pivots = _rref(G)
    cols = G.shape[1]
    free = [c for c in range(cols) if c not in pivots]
    basis = []
    for f in free:
        v = np.zeros(cols, dtype=int)
        v[f] = 1
        for ri, pc in enumerate(pivots):
            if Mr[ri, f]:
                v[pc] = Mr[ri, f]
        basis.append(v % 2)
    return np.array(basis, dtype=int)


def code_matrices():
    G = _cyclic_gen(GPOLY, N)       # 11×15 generator of C
    H = _nullspace(G)               # 4×15, generates C^⊥ = X/Z stabilizers (dual-containing)
    return G, H


def prep_gates():
    """|0_L⟩ prep: X-안정자(H) RREF pivot 별 H(pivot)+CNOT(pivot→support)."""
    _, H = code_matrices()
    Rx, pivots = _rref(H)
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


HEADER = ("bch15_encoder — 순환 Hamming/BCH CSS [[15,7,3]] |0_L⟩ prep (dual-containing C=[15,11,3], "
          "g(x)=x⁴+x+1). registry 첫 cyclic algebraic CSS 계보(cyclic shift 대칭·생성다항식 witness), "
          "rm15([[15,1,3]] punctured RM)와 다른 부호 클래스. Tier-2 CLIFFORD(정준 tableau, dense 2^15 불필요). "
          "★선검증: C dmin 3·dual-containing(C^⊥⊆C·H·H^T=0)→CSS [[15,7,3]] 직교. plan=X-안정자 RREF H·CNOT, "
          "no MatrixGate, 신규 module 0. witness=bch_observe(CSS·dual-containing·거리·cyclic·|0_L⟩ stabilized).")


def gen_spec():
    gates, n = prep_gates()
    return ("# " + HEADER + "\n"
            "```python id=bloq\n" + _bloq_code(n, gates) + "\n```\n"
            '```json id=meta\n'
            f'{{"id": "bch15_encoder", "n_sys": {n}, "n_anc": 0, "tier": "clifford"}}\n'
            "```\n")


def main():
    name = "bch15_encoder"
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
