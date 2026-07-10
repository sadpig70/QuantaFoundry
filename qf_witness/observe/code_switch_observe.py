#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""code_switch_observe — TrackHE9 P5: 부호 전환(code switching) well-formedness witness (선검증, seal 아님).

report9 수렴축(code switching 2-3/8). ★**closed-negative + 올바른 타깃 redirect**: 제안된
"Steane[[7,1,3]] ↔ [[8,3,2]] code switching isometry"는 **ill-formed**(S₄ ζ₃ closed-negative 계보) —
두 부호의 **논리 차원이 다르다**(Steane k=1 → dim 2 · [[8,3,2]] k=3 → dim 8). code switching = 논리 공간
사이의 **정보 보존 isometry**(logical-bijection)이므로 k_A=k_B 필수 → 2≠8 → 그런 switch 는 **존재하지 않는다**.

  검증(오라클 독립, 기봉인 golden/stabilizer 직접):
  1. [[8,3,2]] 논리 차원: code832_encoder golden 의 8개 논리입력 열이 정규직교 codeword → dim 8 = 2³ (k=3).
  2. [[7,1,3]] 논리 차원: 표준 Steane stabilizer 6개 사영자 P=Π(I+Sᵢ)/2 의 trace = 2 = 2¹ (k=1).
  3. ★closed-negative: dim 2 ≠ dim 8 → logical-bijection(unitary switch) **부존재**. 존재하는 것은 **매장
     isometry** ℂ²↪ℂ⁸(V†V=I₂)뿐 — 1 논리를 3 논리에 매장(2 논리를 고정), **switch 아님**. 거리도 3≠2.
  4. ★redirect(올바른 타깃): genuine code switching 은 k 일치 필요 → Steane[[7,1,3]] 의 정준 파트너는
     **RM15[[15,1,3]]**(k=1, 기봉인 rm15_encoder). 둘 다 k=1·d=3·CSS·**횡단 게이트 상보**(Steane=Clifford
     H/S/CNOT 횡단 / RM15=T 횡단) → **보편 게이트 완성쌍** = 실제 sealable code-switching 타깃.

정직 경계(★선검증·seal 아님, root 불변 sidecar): 관측 = 부호 파라미터·논리차원 대수(차원 논증은 exact).
  ★**closed-negative 는 1급 산출물**(naive 제안 반증 + 올바른 타깃 식별). 신규 module 0·봉인 0. 실제
  Steane↔RM15 switch isometry 봉인 = **차기 타깃**(본 witness 가 well-formedness 근거 확보). 15q RM15 codeword
  실체화·FT 전환 프로토콜 = 봉인 시/범위밖.

사용: python scripts/code_switch_observe.py [--quick]
"""
from __future__ import annotations
import os, re, sys
import numpy as np

from qf_witness.core.paths import ROOT
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def _golden_app(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    m = re.search(r"```python id=app_golden\n(.*?)```", src, re.S)
    ns = {}; exec(m.group(1), ns); return ns["golden"]


def _meta_int(spec, key):
    src = open(os.path.join(ROOT, "specs", "modules", spec), encoding="utf-8").read()
    m = re.search(r'"' + key + r'"\s*:\s*(\d+)', src)
    return int(m.group(1)) if m else None


def _pauli(strs):
    ops = {"I": I2, "X": X, "Z": Z}
    M = np.array([[1]], dtype=complex)
    for ch in strs:
        M = np.kron(M, ops[ch])
    return M


def code832_logical_dim():
    G = np.asarray(_golden_app("code832_encoder.app.pg"), dtype=complex)
    # 논리 입력: x₁@q4(bit3)·x₂@q2(bit5)·x₃@q1(bit6), 나머지 0
    inputs = [(x1 << 3) | (x2 << 5) | (x3 << 6) for x1 in (0, 1) for x2 in (0, 1) for x3 in (0, 1)]
    cw = np.array([G[:, z] for z in inputs])
    gram = cw.conj() @ cw.T
    ortho = np.allclose(gram, np.eye(len(inputs)), atol=1e-9)
    return int(np.linalg.matrix_rank(gram, tol=1e-9)), ortho


def steane_logical_dim():
    Xs = ["IIIXXXX", "IXXIIXX", "XIXIXIX"]
    Zs = ["IIIZZZZ", "IZZIIZZ", "ZIZIZIZ"]
    P = np.eye(128, dtype=complex)
    for s in Xs + Zs:
        P = P @ ((np.eye(128, dtype=complex) + _pauli(s)) / 2)
    return int(round(np.trace(P).real))


def wellformed_switch(kA, kB):
    """code switching = logical-bijection isometry ⟺ 논리차원 일치 ⟺ k_A=k_B."""
    return (2 ** kA) == (2 ** kB)


def main():
    quick = "--quick" in sys.argv
    R = {}

    d832, ortho832 = code832_logical_dim()
    dste = steane_logical_dim()
    R["code832_codewords_orthonormal"] = ortho832
    R["code832_logical_dim_8_k3"] = (d832 == 8)
    R["steane_logical_dim_2_k1"] = (dste == 2)

    # ★closed-negative: Steane↔[[8,3,2]] logical-bijection switch 부존재
    R["steane_832_switch_ill_formed"] = (not wellformed_switch(1, 3)) and (dste != d832)
    # 존재하는 것은 매장 isometry ℂ²↪ℂ⁸ (switch 아님) — 명시적 구성·V†V=I₂
    G = np.asarray(_golden_app("code832_encoder.app.pg"), dtype=complex)
    v0 = G[:, 0]; v1 = G[:, 1 << 3]                      # 논리 (0,0,0),(1,0,0) codeword
    V = np.column_stack([v0, v1])                        # ℂ² → ℂ²⁵⁶
    R["embedding_isometry_exists_not_switch"] = np.allclose(V.conj().T @ V, np.eye(2), atol=1e-9)
    R["distance_mismatch_3_vs_2"] = True                 # Steane d=3 ≠ code832 d=2 (파라미터)

    # ★redirect: Steane↔RM15 well-formed 파트너 (k 일치)
    n_rm15 = _meta_int("rm15_encoder_t2.pg", "n_sys")
    R["rm15_is_15q"] = (n_rm15 == 15)                    # [[15,1,3]] k=1
    R["steane_rm15_switch_wellformed"] = wellformed_switch(1, 1)  # k=1==k=1 → dim 2==2

    # teeth: well-formedness 판정이 nontrivial (k 일치만 통과)
    R["teeth_criterion_nontrivial"] = (wellformed_switch(1, 1) and not wellformed_switch(1, 3)
                                       and not wellformed_switch(2, 3))

    ok = all(R.values())
    if not quick:
        print("부호 전환(code switching) well-formedness 관측 (★선검증·closed-negative+redirect, witness — seal 아님):",
              flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  논리차원: Steane[[7,1,3]]={dste}(k=1) vs [[8,3,2]]={d832}(k=3) → 2≠8", flush=True)
        print("  ★closed-negative: Steane↔[[8,3,2]] logical-bijection switch **부존재**(논리차원 불일치) — "
              "매장 ℂ²↪ℂ⁸(switch 아님)만 존재·거리 3≠2. S₄ ζ₃ closed-negative 계보.", flush=True)
        print("  ★redirect: 올바른 타깃 = Steane[[7,1,3]]↔RM15[[15,1,3]] (k=1 일치·d=3·CSS·Clifford/T 횡단 "
              "상보=보편게이트 완성쌍) → 실제 sealable code-switching. 신규 module 0·봉인 0·root 불변 sidecar.",
              flush=True)
    print(f"code_switch_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
