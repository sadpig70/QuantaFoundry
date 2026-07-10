#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""op_ee_observe — TrackHE7 P4: dual-unitary operator entanglement exact witness (동역학 심화).

기봉인 dual-unitary 게이트(du_gate_j8·du_gate_dag)를 소비해 **operator entanglement EE(U)** 를 관측:
  2q 게이트 U 를 (A|B) bipartition 으로 operator Schmidt 분해 U=Σ_k s_k A_k⊗B_k (reshape+SVD),
  EE = −Σ_k s̃_k² log₂ s̃_k² (s̃=정규화 Schmidt 계수).
  ★dual-unitary 정의적 성질: operator Schmidt 스펙트럼이 **평탄(최대)** → EE = log₂(d²) = 2(2q).
  du_gate_j8: s²=[¼,¼,¼,¼] → EE=2.0 정확(dyadic — Agent8 의 "무리수 log" 우려 긍정 해소).
  대비(비-DU): CNOT EE=1.0·CZ EE=1.0(비최대) — DU 판별식으로 작동.

정직 경계(INV-Q3, seal 아님, root 불변): 봉인 = du_gate 유니터리뿐(P1 v5 기봉인). EE 값·스펙트럼
  = 관측. ★DU 는 s² 가 정확히 dyadic(¼) → EE 정확; 일반 게이트는 Schmidt 계수가 무리수일 수
  있어 EE **값** 은 근사/관측(봉인 아님). scrambling/광원뿔 연결 = 관측. 신규 module 0.

사용: python scripts/op_ee_observe.py [--quick]
"""
import os, sys, re
import numpy as np

from qf_witness.core.paths import ROOT


def _load_app_golden(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    m = re.search(r"```python id=app_golden\n(.*?)```", src, re.S)
    if not m:
        return None
    ns = {}
    exec(m.group(1), ns)
    return ns["golden"]


def operator_schmidt(U, d=2):
    """2q 게이트 U(d²×d²) → operator Schmidt 계수(정규화 s̃²) + EE."""
    R = U.reshape(d, d, d, d).transpose(0, 2, 1, 3).reshape(d * d, d * d)  # (a c)(b d)
    s = np.linalg.svd(R, compute_uv=False)
    s2 = s ** 2 / np.sum(s ** 2)
    EE = float(-sum(x * np.log2(x) for x in s2 if x > 1e-12))
    return s2, EE


def main():
    quick = "--quick" in sys.argv
    R = {}

    # DU 게이트 소비: 평탄 스펙트럼·EE=2 정확
    du_names = ["du_gate_j8.app.pg", "du_gate_dag.app.pg"]
    du = {}
    for nm in du_names:
        U = _load_app_golden(nm)
        if U is None or U.shape != (4, 4):
            continue
        s2, EE = operator_schmidt(U)
        du[nm[:-7]] = {"schmidt_sq": [round(float(x), 6) for x in s2],
                       "EE": round(EE, 9),
                       "flat_max": bool(np.allclose(s2, 0.25) and abs(EE - 2.0) < 1e-9)}
    R["dual_unitary"] = du

    # 대비: 비-DU 게이트 (EE < 2). ★SWAP 은 perfect tensor=DU(EE=2)라 별도 관측(대비 아님).
    CX = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex)
    CZ = np.diag([1, 1, 1, -1]).astype(complex)
    contrast = {}
    for nm, U in [("cnot", CX), ("cz", CZ)]:
        s2, EE = operator_schmidt(U)
        contrast[nm] = {"EE": round(EE, 6), "is_max": bool(abs(EE - 2.0) < 1e-9)}
    R["non_dual_unitary_contrast"] = contrast
    # SWAP: perfect tensor → 역시 DU(EE=2) 관측
    _, EE_sw = operator_schmidt(np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], dtype=complex))
    R["swap_also_dual_unitary"] = {"EE": round(EE_sw, 6), "is_max": bool(abs(EE_sw - 2.0) < 1e-9)}

    du_all_max = bool(du) and all(v["flat_max"] for v in du.values())
    # SWAP 은 실제로 EE=0(product A⊗B, 최대 아님) · CNOT/CZ EE=1 — 전부 비최대
    contrast_all_nonmax = all(not v["is_max"] for v in contrast.values())
    ok = bool(du_all_max and contrast_all_nonmax)

    if not quick:
        print("dual-unitary operator entanglement exact witness (동역학, seal 아님):", flush=True)
        for nm, v in du.items():
            print(f"  {nm}: s²={v['schmidt_sq']} EE={v['EE']} 평탄최대(DU)={v['flat_max']}", flush=True)
        for nm, v in contrast.items():
            print(f"  [비-DU 대비] {nm}: EE={v['EE']} (최대={v['is_max']})", flush=True)
        print(f"  [관측] swap: EE={R['swap_also_dual_unitary']['EE']} (perfect tensor → 역시 DU)", flush=True)
        print("  ★정직: DU s²=¼ 정확 dyadic→EE=2 exact(무리수 log 우려 해소)·일반게이트 EE값=관측·"
              "scrambling 연결=관측·root 불변·module 0.", flush=True)
    print(f"op_ee_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
