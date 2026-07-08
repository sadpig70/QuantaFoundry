#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hgp_observe — TrackHE8 P4: 하이퍼그래프곱 qLDPC [[27,4,3]] 코드-정확성 witness (오라클 독립).

봉인된 hgp_qldpc27 (|0_L⟩ prep) 회로 위에서 Tillich-Zémor HGP 부호 구조를 관측:
  1. HGP(Hamming[7,4,3]×rep[3]) CSS: Hx·Hz^T=0 mod2 · N=27 · k=N−rank(Hx)−rank(Hz)=4.
  2. ★거리 d≥3(비대칭 회피): 양 transpose 부호 trivial(dim0) + weight≤2 X/Z-logical 부재(전수 소규모).
     정리 d=min(d1,d2)=min(3,3)=3(Hamming·rep 둘 다 d=3, transpose sector 무 logical). d=3 명시.
  3. ★|0_L⟩ prep 정확성: prep 회로(H+CNOT)의 출력 stabilizer(cirq 정준 tableau, 부호 포함)가
     모든 X-안정자(Hx) 와 Z-안정자(Hz) 를 **+1 부호로 포함** — |0_L⟩ 이 코드공간 논리-0 상태.
  4. 전-Clifford(H·CNOT) → Tier-2 tableau 봉인 정합.

정직 경계(seal 아님, root 불변 sidecar): 관측 = HGP 부호 구조·거리·|0_L⟩ 코드공간 stabilized.
  ★봉인(hgp_seal)=|0_L⟩ prep Clifford tableau exact(Tier-2). 거리 3 달성·decoder(BP+OSD)·임계값·
  더 큰 HGP 일반화 = 관측/범위밖. 신규 module 0. 기봉인 qldpc_hgp([[8,1,2]])의 거리-3 대형 확장.

사용: python scripts/hgp_observe.py [--quick]
"""
from __future__ import annotations
import os, sys, itertools
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from hgp_seal import hgp_matrices, prep_gates, _rref   # noqa: E402  (봉인 대상과 동일 소스)


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


def _min_logical(Hstab, Hcheck, N, maxw=2):
    for w in range(1, maxw + 1):
        for supp in itertools.combinations(range(N), w):
            v = np.zeros(N, dtype=int)
            v[list(supp)] = 1
            if np.all((Hcheck @ v) % 2 == 0) and not _in_rowspace(v, Hstab):
                return w
    return None


def _tableau_stabilizers(gates, n):
    """prep 회로(H·CNOT)를 |0^n⟩에 적용한 상태의 stabilizer 생성자 (cirq 정준 tableau, 부호 포함).
       반환: 리스트 [(x_vec, z_vec, sign∈{+1,−1})]."""
    import cirq
    qs = cirq.LineQubit.range(n)
    st = cirq.CliffordTableauSimulationState(tableau=cirq.CliffordTableau(num_qubits=n), qubits=qs)
    for g in gates:
        if g[0] == "h":
            cirq.act_on(cirq.H(qs[g[1]]), st)
        else:
            cirq.act_on(cirq.CNOT(qs[g[1]], qs[g[2]]), st)
    out = []
    for ps in st.tableau.stabilizers():          # DensePauliString 리스트(부호 포함)
        x = np.zeros(n, dtype=int)
        z = np.zeros(n, dtype=int)
        for i, p in enumerate(ps.pauli_mask):     # 0=I,1=X,2=Y,3=Z
            if p in (1, 2):
                x[i] = 1
            if p in (3, 2):
                z[i] = 1
        sign = 1 if abs(ps.coefficient - 1) < 1e-9 else (-1 if abs(ps.coefficient + 1) < 1e-9 else 0)
        out.append((x, z, sign))
    return out


def _member_plus(target_x, target_z, gens, n):
    """target Pauli(x,z)가 gens(순수 X 또는 순수 Z 부분)로 +1 부호 생성되는가.
       CSS: X-target은 gens 의 X-support(z=0 인 것) 로, Z-target은 Z-support(x=0) 로 각각 span."""
    # 관련 생성자만: X-target(z=0)이면 z-part=0 인 gens, Z-target(x=0)이면 x-part=0 인 gens
    if target_z.sum() == 0:                       # X-type target
        rel = [(g[0], g[2]) for g in gens if g[1].sum() == 0]     # (x_vec, sign)
        vecs = [x for x, s in rel]
        A = np.array(vecs, dtype=int) % 2 if vecs else np.zeros((0, n), dtype=int)
        tv = target_x
    else:                                         # Z-type target
        rel = [(g[1], g[2]) for g in gens if g[0].sum() == 0]
        vecs = [z for z, s in rel]
        A = np.array(vecs, dtype=int) % 2 if vecs else np.zeros((0, n), dtype=int)
        tv = target_z
    if A.shape[0] == 0:
        return False
    # 멤버십: tv 가 rowspace(A) 안 + 모든 관련 생성자 부호 +1(CSS 순수형 곱은 +1 유지)
    signs_ok = all(s == 1 for _, s in rel)
    return _in_rowspace(tv, A) and signs_ok


def main():
    quick = "--quick" in sys.argv
    R = {}
    Hx, Hz, N = hgp_matrices()
    R["css_orthogonal"] = bool(np.all((Hx @ Hz.T) % 2 == 0))
    rx, rz = _rank2(Hx), _rank2(Hz)
    k = N - rx - rz
    R["params_27_4"] = (N == 27 and k == 4)
    lx = _min_logical(Hx, Hz, N, 2)
    lz = _min_logical(Hz, Hx, N, 2)
    R["distance_ge_3"] = (lx is None and lz is None)

    gates, n = prep_gates()
    R["all_clifford"] = all(g[0] in ("h", "cnot") for g in gates)
    try:
        gens = _tableau_stabilizers(gates, n)
        R["gens_count_27"] = (len(gens) == n)
        R["gens_all_plus"] = all(s == 1 for _, _, s in gens)
        R["Lzero_stabilized_by_Hx"] = all(_member_plus(Hx[i], np.zeros(N, int), gens, N)
                                          for i in range(Hx.shape[0]))
        R["Lzero_stabilized_by_Hz"] = all(_member_plus(np.zeros(N, int), Hz[i], gens, N)
                                          for i in range(Hz.shape[0]))
    except Exception as e:
        R["tableau_error"] = False
        print(f"  tableau extraction error: {e}", flush=True)

    # teeth: 오염된 X-stab(임의 비트 뒤집기)은 |0_L⟩ 에 stabilized 되면 안 됨
    bad = Hx[0].copy()
    bad[np.argmax(bad == 0)] ^= 1
    try:
        R["teeth"] = not _member_plus(bad, np.zeros(N, int), gens, N)
    except Exception:
        R["teeth"] = False

    ok = all(v for v in R.values())
    if not quick:
        print("하이퍼그래프곱 qLDPC [[27,4,3]] 코드-정확성 관측 (§3k P6 대형 HGP 개창, witness — seal 아님):",
              flush=True)
        for kk, v in R.items():
            print(f"  {kk}: {v}", flush=True)
        print(f"  HGP(Hamming[7,4,3]×rep[3]): N={N}·k={k}·rank(Hx)={rx}·rank(Hz)={rz}·|0_L⟩ prep {len(gates)} H+CNOT",
              flush=True)
        print("  ★정직: 봉인=|0_L⟩ prep Clifford tableau exact(Tier-2)뿐. 거리 3 달성·decoder·임계값·대형 "
              "일반화=관측/범위밖. 양 transpose trivial→비대칭 회피(Agent8). 신규 module 0·root 봉인가산.", flush=True)
    print(f"hgp_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
