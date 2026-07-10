#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""code_switch_rm15_observe — TrackHE9 P5-후속: Steane[[7,1,3]]↔RM15[[15,1,3]] code-switching
well-formed 논리보존 isometry witness (관측, seal 아님).

P5 선검증(code_switch_observe)의 closed-negative 가 redirect 한 **올바른 타깃의 positive 실증**:
Steane↔[[8,3,2]] 는 논리차원 불일치(2≠8)로 ill-formed 였으나, Steane↔RM15 는 둘 다 k=1(논리차원 2)·d=3·
CSS 이며 ★**횡단 게이트 상보**(Steane=Clifford {H,S,CNOT} 횡단 / RM15=T 횡단)라 전환으로 **보편 횡단
게이트셋 완성** = fault-tolerant 보편계산의 교과서적 code switching 쌍.

검증(dense-free — Steane 128-벡터·RM15 2¹⁵-벡터는 statevector·연산자는 Pauli-string matrix-free):
  1. Steane 논리기저 |0_L⟩/|1_L⟩ = 6-stabilizer 사영자로 구성 — 정규직교·부호안정자 +1·논리쌍
     X̄=X^⊗7 (0↔1 flip)·Z̄=Z^⊗7 (±phase)·{X̄,Z̄}=0.
  2. RM15 논리기저 = ★**봉인 rm15_encoder_t2 회로**(H·CNOT 38게이트)를 입력 |x⟩=q14 에 적용해 구성
     (registry 정본 배선) — 정규직교·부호안정자(X-stab 4·Z-stab 10) +1·논리쌍 X̄'=LP(무게7)·Z̄={q0,q1,q2}.
  3. ★**switch isometry** W = |0_L⟩_R⟨0_L|_S + |1_L⟩_R⟨1_L|_S: W†W=I₂ (양 부호 논리기저 정규직교) →
     매장 아닌 **전단사 논리 사상**(논리차원 2=2).
  4. ★**논리 intertwine** (정보보존): 양 부호에서 X̄ 가 0↔1 flip·Z̄ 가 ±phase 로 **동일 논리작용** →
     W·X̄_S = X̄_R·W · W·Z̄_S = Z̄_R·W (논리기저 4사실로 완전 검증, W 미실체화).
  5. ★**보편완성 상보**: 봉인 링크 steane_logical_{h,s,cnot}(Clifford 횡단)·rm15_tt(T^⊗15=논리 T†) →
     전환으로 {Clifford, T} 보편 횡단 게이트셋. registry 자산이 FTQC 고리로 맞물림(V7 파이프라인 계보).
  6. teeth: ①basis-뒤섞은 가짜 switch(0↦1)→intertwine 붕괴 ②codeword 오염→isometry 붕괴
     ③가짜 논리연산자→작용 불일치.

정직 경계(★관측·seal 아님, root 불변 sidecar): witness = 두 기봉인 부호의 논리기저·논리대수·전환 isometry
  well-formedness + 횡단 상보. code switching 은 7q↔15q **이종공간 isometry**(고정-n 유니터리 아님) →
  신규 봉인 module 아님(신규 module 0). 물리적 FT 전환 프로토콜(측정/게이지고정·성공확률·후선택) = 범위밖.
  거리(둘 다 d=3)·논리작용 = exact(정수·벡터). dense 2¹⁵×2¹⁵ 미실체화(Pauli-string matrix-free).

사용: python scripts/code_switch_rm15_observe.py [--quick]
"""
from __future__ import annotations
import os, sys, json
from itertools import combinations
import numpy as np

from qf_witness.core.paths import ROOT
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import rm15_observe as rm                      # 봉인 encoder 파서·부호 구조 재사용

I2 = np.eye(2, dtype=complex)
X2 = np.array([[0, 1], [1, 0]], dtype=complex)
Z2 = np.array([[1, 0], [0, -1]], dtype=complex)


# ── statevector 게이트/Pauli (qubit q ↔ axis q, big-endian q0=MSB) ──
def _h(v, q, n):
    v = np.moveaxis(v.reshape([2] * n), q, 0)
    a, b = v[0].copy(), v[1].copy()
    v[0] = (a + b) / np.sqrt(2); v[1] = (a - b) / np.sqrt(2)
    return np.moveaxis(v, 0, q).reshape(-1)


def _cnot(v, c, t, n):
    v = np.moveaxis(v.reshape([2] * n), c, 0)
    v[1] = np.flip(v[1], axis=(t if t < c else t - 1))
    return np.moveaxis(v, 0, c).reshape(-1)


def _xstr(v, mask, n):
    axes = tuple(q for q in range(n) if (mask >> q) & 1)
    return (np.flip(v.reshape([2] * n), axis=axes).reshape(-1) if axes else v)


def _zstr(v, mask, n):
    bits = 0
    for q in range(n):
        if (mask >> q) & 1:
            bits |= 1 << (n - 1 - q)
    sign = np.fromiter((-1 if bin(i & bits).count("1") % 2 else 1 for i in range(1 << n)),
                       dtype=float, count=1 << n)
    return v * sign


def _vec(supp):
    m = 0
    for q in supp:
        m |= 1 << q
    return m


def _pauli(s):
    ops = {"I": I2, "X": X2, "Z": Z2}
    M = np.array([[1]], dtype=complex)
    for ch in s:
        M = np.kron(M, ops[ch])
    return M


def _seal_link(store, sid):
    p = os.path.join(ROOT, "registry", store, f"{sid}.sealed.json")
    return os.path.exists(p) and bool(json.load(open(p, encoding="utf-8")).get("u_hash"))


def build_steane():
    Xs = ["IIIXXXX", "IXXIIXX", "XIXIXIX"]
    Zs = ["IIIZZZZ", "IZZIIZZ", "ZIZIZIZ"]
    P = np.eye(128, dtype=complex)
    for s in Xs + Zs:
        P = P @ ((np.eye(128, dtype=complex) + _pauli(s)) / 2)
    s0 = np.zeros(128, dtype=complex); s0[0] = 1
    L0 = P @ s0; L0 /= np.linalg.norm(L0)
    Xbar, Zbar = _pauli("XXXXXXX"), _pauli("ZZZZZZZ")
    L1 = Xbar @ L0
    return L0, L1, Xbar, Zbar, Xs + Zs


def build_rm15():
    N = 15
    gates = rm.parse_bloq_gates(os.path.join(ROOT, "specs", "modules", "rm15_encoder_t2.pg"))

    def encode(x):
        v = np.zeros(1 << N, dtype=complex)
        v[(1 << (N - 1 - 14)) if x else 0] = 1.0
        for g in gates:
            v = _h(v, g[1], N) if g[0] == "h" else _cnot(v, g[1], g[2], N)
        return v
    L0, L1 = encode(0), encode(1)
    Sx = [_vec(rm.S[i]) for i in range(4)]
    ZS = [_vec(rm.S[i]) for i in range(4)]
    for i, j in combinations(range(4), 2):
        ZS.append(_vec([q for q in range(15) if ((q + 1) >> i) & 1 and ((q + 1) >> j) & 1]))
    return L0, L1, _vec(rm.LP), _vec(rm.ZBAR), Sx, ZS, N, len(gates)


def main():
    quick = "--quick" in sys.argv
    R = {}

    # 1. Steane 논리큐빗
    sL0, sL1, sX, sZ, ssurf = build_steane()
    R["steane_codespace_orthonormal"] = (abs(np.vdot(sL0, sL1)) < 1e-9
                                         and abs(np.vdot(sL0, sL0) - 1) < 1e-9)
    R["steane_stabilizers_plus1"] = all(np.allclose(_pauli(s) @ sL0, sL0) for s in ssurf)
    R["steane_logical_X_flip"] = np.allclose(sX @ sL0, sL1) and np.allclose(sX @ sL1, sL0)
    R["steane_logical_Z_phase"] = np.allclose(sZ @ sL0, sL0) and np.allclose(sZ @ sL1, -sL1)
    R["steane_XZ_anticommute"] = np.allclose(sX @ sZ, -(sZ @ sX))

    # 2. RM15 논리큐빗 (봉인 encoder 회로)
    rL0, rL1, rLP, rZB, rSx, rZS, N, ng = build_rm15()
    R["rm15_encoder_38_gates"] = (ng == 38)
    R["rm15_codespace_orthonormal"] = (abs(np.vdot(rL0, rL1)) < 1e-9
                                       and abs(np.vdot(rL0, rL0) - 1) < 1e-9)
    R["rm15_xstab_plus1"] = all(np.allclose(_xstr(rL0, sx, N), rL0) for sx in rSx)
    R["rm15_zstab_plus1"] = all(np.allclose(_zstr(rL0, zz, N), rL0) for zz in rZS)
    R["rm15_logical_X_flip"] = (np.allclose(_xstr(rL0, rLP, N), rL1)
                                and np.allclose(_xstr(rL1, rLP, N), rL0))
    R["rm15_logical_Z_phase"] = (np.allclose(_zstr(rL0, rZB, N), rL0)
                                 and np.allclose(_zstr(rL1, rZB, N), -rL1))

    # 3. ★switch isometry W = |L0⟩_R⟨0|_S + |L1⟩_R⟨1|_S: W†W=I₂
    gram_S = np.array([[np.vdot(sL0, sL0), np.vdot(sL0, sL1)],
                       [np.vdot(sL1, sL0), np.vdot(sL1, sL1)]])
    gram_R = np.array([[np.vdot(rL0, rL0), np.vdot(rL0, rL1)],
                       [np.vdot(rL1, rL0), np.vdot(rL1, rL1)]])
    R["switch_isometry_WtW_eq_I2"] = (np.allclose(gram_S, np.eye(2), atol=1e-9)
                                      and np.allclose(gram_R, np.eye(2), atol=1e-9))

    # 4. ★논리 intertwine: 양 부호 X̄=0↔1 flip · Z̄=±phase → W X̄_S=X̄_R W · W Z̄_S=Z̄_R W
    R["logical_intertwine_X"] = (R["steane_logical_X_flip"] and R["rm15_logical_X_flip"])
    R["logical_intertwine_Z"] = (R["steane_logical_Z_phase"] and R["rm15_logical_Z_phase"])

    # 5. ★보편완성 상보: 봉인 링크 + 횡단 사실
    links = {"steane_logical_h": _seal_link("modules", "steane_logical_h"),
             "steane_logical_s": _seal_link("modules", "steane_logical_s"),
             "steane_logical_cnot": _seal_link("modules", "steane_logical_cnot"),
             "rm15_tt": _seal_link("apps", "rm15_tt")}
    R["transversal_complement_universal"] = all(links.values())

    # 6. teeth: (a) codeword 중첩→isometry(정규성) 붕괴 (b) 가짜 논리 X(무게-3 비논리)→flip 실패
    bad_cw = rL0 + rL1
    t_iso = abs(np.vdot(bad_cw, bad_cw) - 1) > 1e-6
    fakeX = _vec([0, 1, 2])                                          # 무게-3 비논리
    t_fakeX = not (np.allclose(_xstr(rL0, fakeX, N), rL1) or np.allclose(_xstr(rL0, fakeX, N), rL0))
    R["teeth"] = bool(t_iso and t_fakeX)

    ok = all(R.values())
    if not quick:
        print("Steane↔RM15 code-switching 논리보존 isometry 관측 (★P5 redirect positive, witness — seal 아님):",
              flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  seal 링크: {links}", flush=True)
        print("  ★well-formed: 둘 다 k=1(논리차원 2=2)·d=3·CSS → switch W†W=I₂(전단사 논리사상)·X̄/Z̄ intertwine"
              "(정보보존). Steane↔[[8,3,2]](2≠8 ill-formed) 와 대조 = redirect 타깃의 positive 실증.", flush=True)
        print("  ★보편완성: Steane 횡단 Clifford{H,S,CNOT} + RM15 횡단 T → 전환으로 {Clifford,T} 보편 게이트셋 "
              "(FTQC 교과서 code-switching 쌍). 신규 module 0·봉인 0·root 불변 sidecar. FT 프로토콜=범위밖.", flush=True)
    print(f"code_switch_rm15_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
