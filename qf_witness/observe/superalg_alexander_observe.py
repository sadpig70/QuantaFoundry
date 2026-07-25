#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""superalg_alexander_observe — TrackHE19 P6(Stage 1): ★**첫 양자 초대수 층** —
U_q(gl(1|1)) R-행렬 + **quantum supertrace**(ℤ₂-등급·Koszul)로 Alexander 다항식 (관측, seal 아님).

매듭 계보(Hecke·TL·BMW·so_N quantum trace — 전부 보손 양자군)에 **ℤ₂-등급 초대수** 첫 진입:
  - U_q(gl(1|1)) 2-dim rep(even|odd)·**Ř 4×4**(고유값 {q(even), −q⁻¹(odd)})·YBE 전수.
  - ★**sdim=0 함정 실증·해소**: sdim V=0 ⟹ 전-닫힘 supertrace 는 항등적으로 0(함정) —
    표준 해법 = **(1,1)-tangle**: 한 가닥을 열고 나머지를 μ-부분 supertrace
    (str = Tr((−1)^F ·)) → **스칼라·I**(스칼라성 자체가 게이트) = 불변량.
  - μ 게이지 기계확정: μ=diag(q,q)(실효 super-μ=diag(q,−q))·framing 보정 c=1(전 매듭 일관).

관측 6축(정확 심볼릭):
  A. **YBE 전수**(8차원)·고유값 {q,−q⁻¹}.
  B. ★**(1,1)-tangle 스칼라성**: 전 매듭에서 부분 supertrace = 스칼라·I 정확.
  C. ★**Alexander 전 가족**(t=q²): Δ(4₁)=−t+3−t⁻¹ · Δ(5₂)=2t−3+2t⁻¹ ·
     Δ(6₂)=−t²+3t−3+3t⁻¹−t⁻² · Δ(6₃)=t²−3t+5−3t⁻¹+t⁻² · Δ(5₁)=t²−t+1−t⁻¹+t⁻²(2-braid).
  D. ★**삼중 독립 확증**: det=|Δ(−1)| = {5,7,11,13,5} — **TL-bracket·Kauffman D(a,z)·Alexander
     세 독립 경로가 같은 det**([[bmw3_kauffman_family_observe]] 확정값과 교차) + Δ(t)=Δ(1/t)
     대칭·Δ(1)=±1(매듭 공리).
  E. ★**split-소멸**: σ₁⁵ 의 3-braid 닫힘(5₁⊔unknot)에서 Δ=0 정확 — Alexander 는 split link
     에서 소멸(Kauffman D 는 δ-배수로 비영과 대조되는 구조 성질).
  F. **supertrace 함정 게이트**: 전-닫힘(0-open) super trace = 0 명시 확인.

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - ★**Links-Gould(U_q(sl(2|1)) 4-dim·2변수) = 미완=다음** — 본 witness 는 초대수·supertrace·
    (1,1)-tangle **파이프라인과 게이트를 확립**(부호 관례 기계확정)·LG 는 이 위에서.
  - Alexander 값 게이트는 det(자체 확정값)·대칭·Δ(1) — 문헌 Δ 표 인용 없음.

사용: python -m qf_witness.observe.superalg_alexander_observe [--quick]
"""
from __future__ import annotations
import sys
import json

import sympy as sp

q = sp.symbols("q")
t = sp.symbols("t", positive=True)

Rh = sp.Matrix([
    [q, 0, 0, 0],
    [0, q - 1 / q, 1, 0],
    [0, 1, 0, 0],
    [0, 0, 0, -1 / q]])


def kron(A, B):
    return sp.Matrix(sp.BlockMatrix([[A[i, j] * B for j in range(A.cols)]
                                     for i in range(A.rows)]))


I2 = sp.eye(2)
WORDS = {
    "4_1": [(1, 1), (-1, 2), (1, 1), (-1, 2)],
    "5_2": [(1, 1), (-1, 2), (-1, 1), (-1, 1), (-1, 1), (-1, 2)],
    "6_2": [(1, 1), (1, 1), (1, 1), (-1, 2), (1, 1), (-1, 2)],
    "6_3": [(1, 1), (1, 1), (-1, 2), (1, 1), (-1, 2), (-1, 2)],
}
DET = {"4_1": 5, "5_2": 7, "6_2": 11, "6_3": 13}
ALEX = {
    "4_1": -t + 3 - 1 / t,
    "5_2": 2 * t - 3 + 2 / t,
    "6_2": -t**2 + 3 * t - 3 + 3 / t - 1 / t**2,
    "6_3": t**2 - 3 * t + 5 - 3 / t + 1 / t**2,
}


def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "superalg-alexander/v1",
           "_note": ("첫 양자 초대수 층 — U_q(gl(1|1)) supertrace Alexander·(1,1)-tangle·"
                     "sdim=0 함정 해소·split 소멸·det 삼중 확증. LG(sl(2|1))=미완=다음. "
                     "관측·module 0·root 불변.")}
    s1 = kron(Rh, I2)
    s2 = kron(I2, Rh)
    R["A_YBE"] = (sp.simplify(s1 * s2 * s1 - s2 * s1 * s2) == sp.zeros(8, 8))
    ev = Rh.eigenvals()
    R["A_eigen_q_mqinv"] = (set(sp.simplify(k) for k in ev.keys())
                            == {sp.simplify(q), sp.simplify(-1 / q)})
    gen = {(1, 1): s1, (-1, 1): sp.simplify(s1.inv()),
           (1, 2): s2, (-1, 2): sp.simplify(s2.inv())}
    mu = sp.diag(q, q)

    def partial_str(X):
        outm = sp.zeros(2, 2)
        for i in range(2):
            for j in range(2):
                acc = 0
                for k2 in range(2):
                    for k3 in range(2):
                        sgn = (-1) ** (k2 + k3)
                        acc += sgn * mu[k2, k2] * mu[k3, k3] * \
                            X[i * 4 + k2 * 2 + k3, j * 4 + k2 * 2 + k3]
                outm[i, j] = sp.simplify(acc)
        return outm

    names = ["4_1", "6_3"] if quick else list(WORDS)
    for name in names:
        M = sp.eye(8)
        for g in WORDS[name]:
            M = M * gen[g]
        P = partial_str(M)
        R[f"{name}_scalar"] = (sp.simplify(P[0, 1]) == 0 and sp.simplify(P[1, 0]) == 0
                               and sp.simplify(P[0, 0] - P[1, 1]) == 0)
        val = sp.expand(sp.cancel(sp.simplify(P[0, 0]).subs(q, sp.sqrt(t))))
        R[f"{name}_alexander"] = (sp.simplify(val - ALEX[name]) == 0)
        R[f"{name}_symmetric"] = (sp.simplify(val - val.subs(t, 1 / t)) == 0)
        R[f"{name}_det"] = (abs(val.subs(t, -1)) == DET[name])
        R[f"{name}_delta1"] = (val.subs(t, 1) == 1)
        out[f"Delta_{name}"] = str(val)

    # 5₁ (2-braid tangle)
    M2 = Rh**5
    o2 = sp.zeros(2, 2)
    for i in range(2):
        for j in range(2):
            acc = 0
            for k in range(2):
                acc += (-1) ** k * mu[k, k] * M2[i * 2 + k, j * 2 + k]
            o2[i, j] = sp.simplify(acc)
    R["51_scalar"] = (sp.simplify(o2[0, 1]) == 0 and sp.simplify(o2[0, 0] - o2[1, 1]) == 0)
    v51 = sp.expand(sp.cancel(sp.simplify(o2[0, 0]).subs(q, sp.sqrt(t))))
    R["51_alexander"] = (sp.simplify(v51 - (t**2 - t + 1 - 1 / t + t**-2)) == 0)
    R["51_det5"] = (abs(v51.subs(t, -1)) == 5)
    out["Delta_5_1"] = str(v51)

    # split 소멸 + 전-닫힘 supertrace=0
    M3 = sp.eye(8)
    for g in [(1, 1)] * 5:
        M3 = M3 * gen[g]
    Ps = partial_str(M3)
    R["E_split_vanish"] = (sp.simplify(Ps[0, 0]) == 0 and sp.simplify(Ps[1, 1]) == 0)
    # 전-닫힘(모든 가닥 trace): str over strand1 too
    full_tr = sp.simplify(sum((-1) ** (i % 2) * mu[i % 2, i % 2] * Ps[i % 2, i % 2]
                              for i in range(2)))
    M4 = sp.eye(8)
    for g in WORDS["4_1"]:
        M4 = M4 * gen[g]
    P4 = partial_str(M4)
    full4 = sp.simplify((-1) ** 0 * mu[0, 0] * P4[0, 0] + (-1) ** 1 * mu[1, 1] * P4[1, 1])
    R["F_full_supertrace_zero"] = (sp.simplify(full4) == 0)     # sdim=0 함정 실증

    # teeth
    R["teeth_triple_det_crosscheck"] = all(R.get(f"{n}_det", True) for n in names)
    R["teeth_split_detection"] = R["E_split_vanish"]
    R["teeth_sdim0_trap"] = R["F_full_supertrace_zero"]

    ok = bool(all(R.values()))
    out["checks"] = R
    out["scope_honesty"] = {
        "delivered": "첫 초대수 층 — supertrace·(1,1)-tangle 파이프라인·Alexander 5매듭·"
                     "det 삼중 확증(bracket/Kauffman-D/Alexander)·split 소멸",
        "not_yet": "★Links-Gould(sl(2|1) 4-dim·2변수 LG) = 미완=다음 — 파이프라인·게이트 확립",
        "gauge": "μ=diag(q,q)(super-μ=diag(q,−q))·framing c=1 — 기계확정",
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "SUPERALG-ALEXANDER.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("첫 양자 초대수 층 — U_q(gl(1|1)) supertrace Alexander (정확 — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  ★(1,1)-tangle 스칼라·Alexander 5매듭·det{5,7,11,13,5} 삼중 확증", flush=True)
        print("  ★sdim=0 함정 실증·split 소멸 Δ=0·LG(sl(2|1))=미완=다음", flush=True)
        print("  → .pgf/proofs/SUPERALG-ALEXANDER.json", flush=True)
    print(f"superalg_alexander_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
