#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bch_observe — TrackHE9-pre: 순환 Hamming/BCH CSS [[15,7,3]] 코드-정확성 witness (오라클 독립).

봉인된 bch15_encoder(|0_L⟩ prep) 위에서 순환-BCH CSS 부호 구조를 관측:
  1. C=[15,11,3] 순환부호(g=x⁴+x+1)·dual-containing(C^⊥⊆C·H·H^T=0) → CSS Hx=Hz=H 직교·[[15,7,3]].
  2. ★거리 3: 논리연산자 최소무게 = C∖C^⊥ 최소무게 = 3(C dmin 3 이 C^⊥(min무게 8)에 없음). 전수(2^11) 확인.
  3. ★**cyclic 대칭**(registry 첫 cyclic CSS 계보 특징): C 가 순환 shift 불변(shift(C)=C)·안정군도 shift 불변.
  4. ★|0_L⟩ prep 정확성: prep 회로 출력 stabilizer(cirq 정준 tableau, 부호 포함)가 모든 X-안정자(Hx)·
     Z-안정자(Hz)를 **+1 부호로 포함**(코드공간 논리-0).
  5. 전-Clifford(H·CNOT) → Tier-2 tableau 봉인 정합.

정직 경계(seal 아님, root 불변 sidecar): 관측 = BCH 순환 CSS 부호 구조·거리·cyclic 대칭·|0_L⟩ stabilized.
  ★봉인(bch_seal)=|0_L⟩ prep Clifford tableau exact(Tier-2). 거리 3 달성·decoder·순환 자기동형 물리·더 큰
  BCH(δ≥5) = 관측/범위밖. 신규 module 0. rm15([[15,1,3]] punctured RM)와 다른 부호 클래스(순환 대수부호).

사용: python -m qf_witness.observe.bch_observe [--quick]
"""
from __future__ import annotations
import os, sys
import numpy as np

from qf_witness.core.paths import ROOT
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from bch_seal import code_matrices, prep_gates, _rref, N   # noqa: E402  (봉인 대상과 동일 소스)


def _rank2(M):
    M = M.copy() % 2
    rows, cols = M.shape
    r = 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if M[i, c]), None)
        if piv is None:
            continue
        M[[r, piv]] = M[[piv, r]]
        for i in range(rows):
            if i != r and M[i, c]:
                M[i] ^= M[r]
        r += 1
    return r


def _in_rowspace(v, M):
    return _rank2(np.vstack([M % 2, v % 2])) == _rank2(M)


def _all_codewords(G):
    k = G.shape[0]
    out = []
    for bits in range(1 << k):
        cw = np.zeros(G.shape[1], dtype=int)
        for i in range(k):
            if (bits >> i) & 1:
                cw ^= G[i]
        out.append(cw % 2)
    return out


def _tableau_stabilizers(gates, n):
    import cirq
    qs = cirq.LineQubit.range(n)
    st = cirq.CliffordTableauSimulationState(tableau=cirq.CliffordTableau(num_qubits=n), qubits=qs)
    for g in gates:
        if g[0] == "h":
            cirq.act_on(cirq.H(qs[g[1]]), st)
        else:
            cirq.act_on(cirq.CNOT(qs[g[1]], qs[g[2]]), st)
    out = []
    for ps in st.tableau.stabilizers():
        x = np.zeros(n, dtype=int)
        z = np.zeros(n, dtype=int)
        for i, p in enumerate(ps.pauli_mask):
            if p in (1, 2):
                x[i] = 1
            if p in (3, 2):
                z[i] = 1
        sign = 1 if abs(ps.coefficient - 1) < 1e-9 else (-1 if abs(ps.coefficient + 1) < 1e-9 else 0)
        out.append((x, z, sign))
    return out


def _member_plus(tx, tz, gens, n):
    if tz.sum() == 0:
        rel = [(g[0], g[2]) for g in gens if g[1].sum() == 0]
        tv = tx
    else:
        rel = [(g[1], g[2]) for g in gens if g[0].sum() == 0]
        tv = tz
    if not rel:
        return False
    A = np.array([v for v, s in rel], dtype=int) % 2
    return _in_rowspace(tv, A) and all(s == 1 for _, s in rel)


def main():
    quick = "--quick" in sys.argv
    R = {}
    G, H = code_matrices()

    # 1. dual-containing → CSS 직교
    R["css_dual_containing"] = bool(np.all((H @ H.T) % 2 == 0) and
                                    all(_in_rowspace(H[i], G) for i in range(H.shape[0])))
    kq = 2 * G.shape[0] - N
    R["params_15_7"] = (N == 15 and kq == 7)

    # 2. 거리 3: 논리 최소무게 = C∖C^⊥ 최소무게 (전수 2^11)
    codes = _all_codewords(G)
    dmin = 99
    for cw in codes:
        w = int(cw.sum())
        if 0 < w and not _in_rowspace(cw, H):        # C 이지만 C^⊥ 아님 = 논리
            dmin = min(dmin, w)
    R["distance_3"] = (dmin == 3)

    # 3. cyclic 대칭: shift(C)=C
    def shift(v):
        return np.roll(v, 1)
    Gshift = np.array([shift(G[i]) for i in range(G.shape[0])], dtype=int)
    R["cyclic_invariant"] = (_rank2(np.vstack([G, Gshift])) == _rank2(G))

    # 4. |0_L⟩ prep 정확성 (cirq tableau, 부호 포함)
    gates, n = prep_gates()
    R["all_clifford"] = all(g[0] in ("h", "cnot") for g in gates)
    try:
        gens = _tableau_stabilizers(gates, n)
        R["gens_all_plus"] = all(s == 1 for _, _, s in gens)
        R["Lzero_stab_by_Hx"] = all(_member_plus(H[i], np.zeros(N, int), gens, N) for i in range(H.shape[0]))
        R["Lzero_stab_by_Hz"] = all(_member_plus(np.zeros(N, int), H[i], gens, N) for i in range(H.shape[0]))
    except Exception as e:
        R["tableau_error"] = False
        print(f"  tableau error: {e}", flush=True)

    # teeth: 오염 X-stab 은 stabilized 되면 안 됨
    bad = H[0].copy()
    bad[int(np.argmax(bad == 0))] ^= 1
    try:
        R["teeth"] = not _member_plus(bad, np.zeros(N, int), gens, N)
    except Exception:
        R["teeth"] = False

    ok = all(v for v in R.values())
    if not quick:
        print("순환 Hamming/BCH CSS [[15,7,3]] 코드-정확성 관측 (§3j cyclic 대수부호 개창, witness — seal 아님):",
              flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  C=[15,11,3] 순환(g=x⁴+x+1)·dual-containing → CSS [[15,{kq},{dmin}]]·|0_L⟩ prep {len(gates)} H+CNOT·cyclic 불변",
              flush=True)
        print("  ★정직: 봉인=|0_L⟩ prep Clifford tableau exact(Tier-2)뿐. 거리 3 달성·decoder·순환 자기동형 "
              "물리·δ≥5 BCH=관측/범위밖. rm15(punctured RM)와 다른 순환 대수부호 클래스. 신규 module 0.", flush=True)
    print(f"bch_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
