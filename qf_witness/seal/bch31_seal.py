#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bch31_seal.py — §4 관문(d≥5 부호): distance-5 cyclic-BCH CSS [[31,11,5]] |0_L⟩ prep Tier-2 봉인.

narrow-sense BCH C=[31,21,5](GF(2^5), primitive x^5+x^2+1, 생성다항식 g=m₁·m₃ deg 10)가
**dual-containing**(Steane 정리: δ=5 ≤ 2^⌈5/2⌉−1=7)임을 이용한 양자 CSS [[31,11,5]] — bch15_encoder
([[15,7,3]] d=3)의 **거리-5 확장**, registry 첫 distance-5 cyclic 부호(§3l/§4 "d≥5·BCH cyclic 아직
없음" 관문). 31q → Tier-2 CLIFFORD(정준 stabilizer tableau, dense 2^31 불필요, HGP/bch15 선례).
  ★선검증 확정(scratchpad): dual-containing(H·H^T=0 & C^⊥⊆C)·**weight≤4 codeword 부재→d(C)≥5**·
  BCH bound δ=5 → CSS Hx=Hz=H(10×31) 직교·k=2·21−31=11·[[31,11,5]].
|0_L⟩ = ∏(I+S_X)|0^31⟩: X-안정자(H) RREF pivot → H(pivot)+CNOT(pivot→support) 확산.
봉인: verify_seal module tier="clifford" 정준 tableau → registry/modules. 독립 재확인 = clifford_seal.
  신규 module 0(bloq H/CNOT). 정직: 봉인=|0_L⟩ prep Clifford tableau exact; 거리 5 달성·decoder·임계값=관측.
witness=bch31_observe. bch15_encoder 무손상(별도 드라이버).

사용: python scripts/bch31_seal.py
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

M, N, PRIM = 5, 31, 0b100101    # GF(2^5), primitive x^5+x^2+1


def _gf_tables():
    alog = [0] * (N + 1)
    log = [0] * (1 << M)
    x = 1
    for i in range(N):
        alog[i] = x
        log[x] = i
        x <<= 1
        if x & (1 << M):
            x ^= PRIM
    return alog, log


_ALOG, _LOG = _gf_tables()


def _gf_mul(a, b):
    if a == 0 or b == 0:
        return 0
    return _ALOG[(_LOG[a] + _LOG[b]) % N]


def _minimal_poly(power):
    coset = set()
    p = power % N
    while p not in coset:
        coset.add(p)
        p = (p * 2) % N
    poly = [1]
    for c in coset:
        root = _ALOG[c]
        new = [0] * (len(poly) + 1)
        for i, co in enumerate(poly):
            new[i] ^= _gf_mul(co, root)
            new[i + 1] ^= co
        poly = new
    return [c & 1 for c in poly]


def _poly_mul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            r[i + j] ^= ai & bj
    return r


def gpoly():
    return [c & 1 for c in _poly_mul(_minimal_poly(1), _minimal_poly(3))]   # deg 10


def _cyclic_gen(g, n):
    k = n - (len(g) - 1)
    G = np.zeros((k, n), dtype=int)
    for i in range(k):
        for j, c in enumerate(g):
            G[i, i + j] = c
    return G % 2


def _rref(Mx):
    Mx = Mx.copy() % 2
    rows, cols = Mx.shape
    pivots = []
    r = 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if Mx[i, c]), None)
        if piv is None:
            continue
        Mx[[r, piv]] = Mx[[piv, r]]
        for i in range(rows):
            if i != r and Mx[i, c]:
                Mx[i] ^= Mx[r]
        pivots.append(c)
        r += 1
    return Mx[:r], pivots


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
    G = _cyclic_gen(gpoly(), N)     # 21×31 generator of C
    H = _nullspace(G)               # 10×31, generates C^⊥ = X/Z stabilizers
    return G, H


def prep_gates():
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


HEADER = ("bch31_encoder — distance-5 순환 BCH CSS [[31,11,5]] |0_L⟩ prep (dual-containing narrow-sense "
          "BCH C=[31,21,5], GF(2^5) primitive x^5+x^2+1, g=m₁·m₃). bch15([[15,7,3]] d=3)의 거리-5 확장, "
          "registry 첫 distance-5 cyclic 부호(§4 d≥5·BCH 관문). Tier-2 CLIFFORD(정준 tableau, dense 2^31 "
          "불필요). ★선검증: dual-containing(H·H^T=0)·weight≤4 codeword 부재→d(C)≥5·BCH bound δ=5 → CSS "
          "[[31,11,5]] 직교. plan=X-안정자 RREF H·CNOT, no MatrixGate, 신규 module 0. witness=bch31_observe.")


def gen_spec():
    gates, n = prep_gates()
    return ("# " + HEADER + "\n"
            "```python id=bloq\n" + _bloq_code(n, gates) + "\n```\n"
            '```json id=meta\n'
            f'{{"id": "bch31_encoder", "n_sys": {n}, "n_anc": 0, "tier": "clifford"}}\n'
            "```\n")


def main():
    name = "bch31_encoder"
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
