#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bch31_observe — §4 관문: distance-5 순환 BCH CSS [[31,11,5]] 코드-정확성 witness (오라클 독립).

봉인된 bch31_encoder(|0_L⟩ prep) 위에서 distance-5 순환-BCH CSS 부호 구조를 관측:
  1. narrow-sense BCH C=[31,21,5]·dual-containing(H·H^T=0·C^⊥⊆C) → CSS Hx=Hz=H(10×31) 직교·[[31,11,5]].
  2. ★거리 5: **weight≤4 codeword 부재**(H·v=0 전수 C(31,≤4)≈36k) → d(C)≥5; BCH bound δ=5 tight → d=5.
     논리연산자 ⊆ C 이므로 d_CSS ≥5(모든 C 원소 무게 ≥5).
  3. ★cyclic 대칭: C 순환 shift 불변(shift(C)=C).
  4. ★|0_L⟩ prep 출력 stabilizer(cirq 정준 tableau, 부호 포함)가 모든 Hx·Hz 를 +1 stabilized.
  5. 전-Clifford(H·CNOT) → Tier-2 tableau 봉인 정합.

정직 경계(seal 아님, root 불변 sidecar): 관측 = BCH 순환 CSS 구조·거리 5·cyclic 대칭·|0_L⟩ stabilized.
  ★봉인(bch31_seal)=|0_L⟩ prep Clifford tableau exact(Tier-2). 거리 5 달성·decoder(BP)·임계값=관측/범위밖.
  거리 = weight≤4 부재(전수) + BCH bound(정리)로 5 확립(전체 2^21 열거 아님, honest). 신규 module 0.
  bch15([[15,7,3]] d=3)의 거리-5 확장(같은 cyclic 대수부호 계보).

사용: python scripts/bch31_observe.py [--quick]
"""
from __future__ import annotations
import os, sys, itertools
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from bch31_seal import code_matrices, prep_gates, _rref, N   # noqa: E402  (봉인 대상과 동일 소스)


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


def _in_rows(v, M):
    return _rank2(np.vstack([M % 2, v % 2])) == _rank2(M)


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
    return _in_rows(tv, A) and all(s == 1 for _, s in rel)


def main():
    quick = "--quick" in sys.argv
    R = {}
    G, H = code_matrices()          # G:21×31 (C), H:10×31 (C^⊥ = stabilizers)

    R["css_dual_containing"] = bool(np.all((H @ H.T) % 2 == 0) and
                                    all(_in_rows(H[i], G) for i in range(H.shape[0])))
    kq = 2 * G.shape[0] - N
    R["params_31_11"] = (N == 31 and kq == 11)

    # 거리 5: weight≤4 codeword 부재 (C = ker(H), v in C iff H v = 0)
    def is_codeword(v):
        return bool(np.all((H @ v) % 2 == 0))
    found = None
    for w in range(1, 5):
        for supp in itertools.combinations(range(N), w):
            v = np.zeros(N, dtype=int)
            v[list(supp)] = 1
            if is_codeword(v):
                found = w
                break
        if found:
            break
    R["distance_ge_5_no_wt_le4"] = (found is None)

    # cyclic 대칭
    Gshift = np.array([np.roll(G[i], 1) for i in range(G.shape[0])], dtype=int)
    R["cyclic_invariant"] = (_rank2(np.vstack([G, Gshift])) == _rank2(G))

    # |0_L⟩ prep 정확성
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

    # teeth
    bad = H[0].copy()
    bad[int(np.argmax(bad == 0))] ^= 1
    try:
        R["teeth"] = not _member_plus(bad, np.zeros(N, int), gens, N)
    except Exception:
        R["teeth"] = False

    ok = all(v for v in R.values())
    if not quick:
        print("distance-5 순환 BCH CSS [[31,11,5]] 코드-정확성 관측 (§4 d≥5·BCH 관문, witness — seal 아님):",
              flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  narrow-sense BCH C=[31,21,5]·dual-containing → CSS [[31,{kq},5]]·|0_L⟩ prep {len(gates)} H+CNOT·cyclic 불변",
              flush=True)
        print("  ★정직: 봉인=|0_L⟩ prep Clifford tableau exact(Tier-2)뿐. 거리 5=weight≤4 부재(전수)+"
              "BCH bound δ=5. 달성·decoder·임계값=관측/범위밖. bch15(d3)의 거리-5 확장. 신규 module 0.", flush=True)
    print(f"bch31_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
