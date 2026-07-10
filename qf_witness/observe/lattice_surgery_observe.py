#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lattice_surgery_observe — TrackHE10 P5: surface-code lattice surgery merge/split logical CNOT witness
(관측, seal 아님).

report10 수렴축(lattice surgery, 6/8). §3m P5·§4 "code switching FT 전환 프로토콜(gauge-fixing)·lattice
surgery 아직 없음" 관문. code switching(TrackHE9 P5, **다른** 부호 Steane↔RM15 coherent isometry W)의 상보:
lattice surgery = **동일 surface-code 패밀리** 논리큐빗 간 **측정 기반 merge/split** = 측정 채널(joint Pauli
측정), 다른 수학적 대상.

관측(stabilizer·측정 기반 exact):
  Horsman lattice-surgery CNOT: ancilla 논리큐빗 a=|+⟩, ★**ZZ-merge**(joint Z̄_c Z̄_a 측정)·**XX-merge**
  (joint X̄_a X̄_t 측정)·a Z-측정. 측정 결과 (m1,m2,m3) 별 branch:
  1. ★**postselected branch(000)** = CNOT / (2√2) (정규화=측정확률) → 구조 정확히 논리 CNOT(c→t).
  2. ★**모든 유효 측정 branch = CNOT up to Pauli 보정**(X̄_t^{m}·Z̄_c^{m}, gauge-fixing Pauli frame) →
     결정론적 논리 CNOT. 8 branch 전수(불가능 outcome 제외).
  3. crux(§4′i): lattice surgery = **joint Pauli 측정**(projective·동일 부호) ≠ code_switch coherent
     unitary W(다른 부호). 논리작용은 X̄_c→X̄_cX̄_t·Z̄_t→Z̄_cZ̄_t(CNOT Heisenberg).
  4. teeth: XX-merge 누락(ZZ만)은 CNOT 아님.

정직 경계(★관측·seal 아님, root 불변 sidecar): witness = lattice-surgery CNOT 의 **논리 회로 항등**(측정 기반,
  stabilizer exact). ★**측정 결과 의존 Pauli 보정=gauge-fixing=관측**(§5 측정후처리)·결정론 논리작용만 검증.
  물리 surface-code 패치(distance-d [[d²,1,d]]) 실현=Tier-2 tableau(범위밖·dense 미실체화)·오류문턱/FT=하드웨어
  out. 신규 module 0. [[code-switch-rm15-observe]](다른 부호 coherent) 상보(동일 부호 측정).

사용: python -m qf_witness.observe.lattice_surgery_observe [--quick]
"""
from __future__ import annotations
import sys, itertools
import numpy as np

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
PL1 = {"I": I, "X": X, "Y": Y, "Z": Z}


def op(*mats):
    r = np.array([[1]], dtype=complex)
    for m in mats:
        r = np.kron(r, m)
    return r


III = op(I, I, I)
PLUS = np.array([1, 1], dtype=complex) / np.sqrt(2)
CNOT = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex)  # c=MSB→t


def branch_map(m1, m2, m3):
    """(c,a,t) 3큐빗 측정기반 CNOT branch → (c,t) 2큐빗 유효 연산."""
    Pzz = (III + (-1) ** m1 * op(Z, Z, I)) / 2          # Z_c Z_a = (−1)^m1
    Pxx = (III + (-1) ** m2 * op(I, X, X)) / 2          # X_a X_t = (−1)^m2
    M = np.zeros((4, 4), dtype=complex)
    for ci in range(2):
        for ti in range(2):
            psi = np.zeros(8, dtype=complex)
            for ai in range(2):
                psi[(ci << 2) | (ai << 1) | ti] = PLUS[ai]
            psi = Pxx @ Pzz @ psi
            for co in range(2):
                for to in range(2):
                    M[(co << 1) | to, (ci << 1) | ti] = psi[(co << 2) | (m3 << 1) | to]
    return M


def cnot_up_to_pauli(M):
    """M ∝ s·P·CNOT (P∈2큐빗 Pauli, s∈±1)? 보정 Pauli 이름 or None."""
    if np.allclose(M, 0):
        return "null"
    Mn = M * 2 * np.sqrt(2)                              # 정규화 복원
    for n1 in "IXYZ":
        for n2 in "IXYZ":
            P = op(PL1[n1], PL1[n2])
            for s in (1, -1):
                if np.allclose(s * P @ CNOT, Mn) or np.allclose(s * CNOT @ P, Mn):
                    return f"{'+' if s > 0 else '-'}{n1}{n2}"
    return None


def main():
    quick = "--quick" in sys.argv
    R = {}

    # 1. postselected branch(000) = CNOT/(2√2)
    M0 = branch_map(0, 0, 0)
    R["postselected_branch_is_cnot"] = np.allclose(M0 * 2 * np.sqrt(2), CNOT)

    # 2. 모든 유효 branch = CNOT up to Pauli 보정
    corrections = {}
    all_cnot = True
    for m1, m2, m3 in itertools.product((0, 1), repeat=3):
        c = cnot_up_to_pauli(branch_map(m1, m2, m3))
        corrections[f"{m1}{m2}{m3}"] = c
        if c is None:
            all_cnot = False
    R["all_branches_cnot_up_to_pauli"] = all_cnot
    R["correction_is_Xt_Zc_frame"] = all(
        c in ("null", "+II", "-II") or set(c[1:]) <= set("IXZ")   # 보정 = X_t·Z_c frame(Y 없음)
        for c in corrections.values())

    # 3. 논리 CNOT Heisenberg 작용(postselected M ∝ CNOT → X̄_c→X̄_cX̄_t·Z̄_t→Z̄_cZ̄_t)
    U = CNOT
    R["logical_X_c_to_XcXt"] = np.allclose(U @ op(X, I) @ U.conj().T, op(X, X))
    R["logical_Z_t_to_ZcZt"] = np.allclose(U @ op(I, Z) @ U.conj().T, op(Z, Z))

    # 4. crux: lattice surgery = 측정(projective) ≠ code switching coherent W(유니터리)
    #    joint 측정 연산자는 사영자(P²=P), 유니터리 아님
    Pzz = (III + op(Z, Z, I)) / 2
    R["crux_merge_is_projective_not_unitary"] = (np.allclose(Pzz @ Pzz, Pzz)
                                                 and not np.allclose(Pzz @ Pzz.conj().T, III))

    # teeth: XX-merge 누락(ZZ만·a 측정)은 CNOT 아님
    def zz_only(m1, m3):
        Pz = (III + (-1) ** m1 * op(Z, Z, I)) / 2
        M = np.zeros((4, 4), dtype=complex)
        for ci in range(2):
            for ti in range(2):
                psi = np.zeros(8, dtype=complex)
                for ai in range(2):
                    psi[(ci << 2) | (ai << 1) | ti] = PLUS[ai]
                psi = Pz @ psi
                for co in range(2):
                    for to in range(2):
                        M[(co << 1) | to, (ci << 1) | ti] = psi[(co << 2) | (m3 << 1) | to]
        return M
    R["teeth_zz_only_not_cnot"] = (cnot_up_to_pauli(zz_only(0, 0)) is None
                                   or not np.allclose(zz_only(0, 0) * 2 * np.sqrt(2), CNOT))

    ok = all(R.values())
    if not quick:
        print("surface-code lattice surgery merge/split logical CNOT 관측 (code switching 상보, witness — seal 아님):",
              flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  8 branch 보정: {corrections}", flush=True)
        print("  ★postselected(000)=CNOT/(2√2)·모든 유효 branch=CNOT up to Pauli 보정(X̄_t·Z̄_c frame, gauge-fixing) "
              "= 결정론 논리 CNOT. crux: joint Pauli 측정(projective·동일 부호) ≠ code_switch coherent W(다른 부호).",
              flush=True)
        print("  ★정직: 관측=측정기반 논리 CNOT 항등(stabilizer exact). Pauli 보정=gauge-fixing=관측·물리 패치 "
              "Tier-2 tableau·FT/문턱=범위밖·신규 module 0·root 불변 sidecar.", flush=True)
    print(f"lattice_surgery_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
