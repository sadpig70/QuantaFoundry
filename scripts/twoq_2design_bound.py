#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""twoq_2design_bound — TrackGate6 G2a: 2q unitary 2-design 소형 부분집합 불가 반증 (closed-negative).

판정(봉인 0·root 불변): 정확(가중 포함) unitary 2-design 의 최소 크기 하한
    |X| ≥ d⁴ − 2d² + 2 = 1 + (d²−1)²      [Gross–Audenaert–Eisert, J.Math.Phys. 48, 052104 (2007)]
이 d=4(2큐빗)에서 226 이므로, "작은 부분집합(≤64) 2q exact 2-design 봉인"은 수학적으로 불가하고
외부 런타임의 "21원소 2q 2-design" 주장은 **하한 위반으로 반증**된다.

수치 근거(전부 결정론, seed 고정):
  1. ★하한의 정체 = K(d) := dim span{vec(U⊗Ū)} — 2-design 조건은 Haar 2차 모멘트 재현이고,
     설계 원소 하나가 기여하는 방향은 vec(U⊗Ū) 하나뿐 → |X| ≥ K(d). K(d)=d⁴−2d²+2 를
     (a) Haar 표본, (b) Clifford 군 원소(2-design 이므로 동일 span) 두 경로로 rank 포화 확인.
     d=2: 10 · d=4: 226. 가중치는 rank 를 늘릴 수 없음 → 가중 설계에도 유효(탈출구 없음).
  2. 1q 캘리브레이션: 24원소 C₁ 전체 F₂=2(V8) + ★12원소 부분군(Pauli⋊C₃, 사면체 2T/±)도 F₂=2
     — 하한 10 ≤ 실제 최소 ≤ 12 정합. (V8 cliff1 24개=군 폐포 봉인이지 최소 2-design 아님 — 정직 기록.)
  3. "21원소" 주장의 정체 추정: d=4 MUB(5기저×4상태=20)는 projective **state** 2-design
     (frame potential = 2/(d(d+1)) = 1/10 exact) — unitary/state design 혼동 개연. state 2-design 은
     별도 대체 payoff 후보(G2b, 규모 게이트).

정직 경계: 이 리포트는 반증 문서(관측/수학)이며 봉인 아님. rank 수치는 float SVD(tol 1e-8) 기반이나
  하한 정리 자체는 해석적 사실 — 수치는 재현 witness. 사용: python scripts/twoq_2design_bound.py
"""
import os, sys, json
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".pgf", "proofs", "TWOQ-2DESIGN-BOUND.json")

H1 = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
S1 = np.diag([1, 1j]).astype(complex)
CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)
I2 = np.eye(2, dtype=complex)


def span_rank(mats, tol=1e-8):
    V = np.array([np.kron(U, U.conj()).flatten() for U in mats])
    s = np.linalg.svd(V, compute_uv=False)
    return int((s > tol * s[0]).sum())


def haar(d, rng):
    Z = (rng.standard_normal((d, d)) + 1j * rng.standard_normal((d, d))) / np.sqrt(2)
    Q, R = np.linalg.qr(Z)
    return Q @ np.diag(np.diag(R) / np.abs(np.diag(R)))


def cliff1_group():
    """1q Clifford 24원소 (V8 BFS 재현, mod phase 정규화 대표)."""
    def canon(U, tol=1e-9):
        f = U.flatten(); i = np.argmax(np.abs(f) > tol)
        return tuple(np.round(U.flatten() * (np.conj(f[i]) / np.abs(f[i])), 6).tolist())
    elems = {canon(np.eye(2)): np.eye(2, dtype=complex)}
    frontier = [np.eye(2, dtype=complex)]
    while frontier:
        nxt = []
        for U in frontier:
            for G in (H1, S1):
                U2 = G @ U
                k = canon(U2)
                if k not in elems:
                    elems[k] = U2; nxt.append(U2)
        frontier = nxt
    return list(elems.values())


def cliff2_samples(n, rng):
    """2q Clifford 표본: {H,S,CNOT} 무작위 word (길이 20)."""
    gates = [np.kron(H1, I2), np.kron(I2, H1), np.kron(S1, I2), np.kron(I2, S1),
             CNOT, np.kron(H1, H1) @ CNOT @ np.kron(H1, H1)]
    out = []
    for _ in range(n):
        U = np.eye(4, dtype=complex)
        for g in rng.integers(0, len(gates), 20):
            U = gates[g] @ U
        out.append(U)
    return out


def frame_potential(mats, t=2):
    n = len(mats)
    return float(sum(abs(np.trace(A.conj().T @ B)) ** (2 * t) for A in mats for B in mats) / n ** 2)


def tetrahedral12(c24):
    """Pauli⋊C₃ 12원소 부분군: order-3 원소 C 로 {P·C^k} 폐포 구성."""
    def canon(U, tol=1e-9):
        f = U.flatten(); i = np.argmax(np.abs(f) > tol)
        return tuple(np.round(U.flatten() * (np.conj(f[i]) / np.abs(f[i])), 6).tolist())
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    Z = np.diag([1, -1]).astype(complex)
    for C in c24:
        k1, k2, k3 = canon(C), canon(C @ C), canon(C @ C @ C)
        if k3 == canon(np.eye(2)) and k1 != canon(np.eye(2)) and k2 != k1:
            subset = {}
            for P in (np.eye(2, dtype=complex), X, Y, Z):
                for k in range(3):
                    M = P @ np.linalg.matrix_power(C, k)
                    subset[canon(M)] = M
            if len(subset) == 12:
                mats = list(subset.values())
                keys = set(subset)
                closed = all(canon(A @ B) in keys for A in mats for B in mats)
                if closed:
                    return mats
    return None


def mub20_frame_potential():
    """d=4 MUB 5기저×4상태 — projective state 2-design witness: Σ|⟨ψ|φ⟩|⁴/N² = 2/(d(d+1))."""
    d = 4
    Zb = [np.eye(d, dtype=complex)[:, i] for i in range(d)]
    P = {"I": I2, "X": np.array([[0, 1], [1, 0]], dtype=complex),
         "Y": np.array([[0, -1j], [1j, 0]], dtype=complex), "Z": np.diag([1, -1]).astype(complex)}
    # 5 MUB = 15개 비항등 Pauli 의 가환 5-분할(각 삼중군의 공통 고유기저) 표준 구성:
    #   {ZI,IZ,ZZ}·{XI,IX,XX}·{YI,IY,YY}·{XZ,ZY,YX}·{ZX,YZ,XY}
    def eig_basis(A, B):
        M = np.kron(P[A[0]], P[A[1]]) + 2 * np.kron(P[B[0]], P[B[1]])
        _, V = np.linalg.eigh(M)
        return [V[:, i] for i in range(d)]
    bases = [Zb, eig_basis("XI", "IX"), eig_basis("YI", "IY"),
             eig_basis("XZ", "ZY"), eig_basis("ZX", "YZ")]
    states = [v for b in bases for v in b]
    # 상호비편향 확인
    mub_ok = True
    for i in range(5):
        for j in range(i + 1, 5):
            for u in bases[i]:
                for v in bases[j]:
                    if abs(abs(np.vdot(u, v)) ** 2 - 1 / d) > 1e-9:
                        mub_ok = False
    N = len(states)
    fp = float(sum(abs(np.vdot(u, v)) ** 4 for u in states for v in states) / N ** 2)
    return N, mub_ok, fp, 2 / (d * (d + 1))


def main():
    rng = np.random.default_rng(0)
    res = {}
    # 1. K(d) rank 포화 (2경로)
    c24 = cliff1_group()
    res["K_d2_haar"] = span_rank([haar(2, rng) for _ in range(40)])
    res["K_d2_clifford24"] = span_rank(c24)
    res["K_d4_haar"] = span_rank([haar(4, rng) for _ in range(400)])
    res["K_d4_clifford_samples"] = span_rank(cliff2_samples(400, rng))
    res["bound_formula_d2"] = 2 ** 4 - 2 * 2 ** 2 + 2
    res["bound_formula_d4"] = 4 ** 4 - 2 * 4 ** 2 + 2
    ok_rank = (res["K_d2_haar"] == res["K_d2_clifford24"] == res["bound_formula_d2"] == 10 and
               res["K_d4_haar"] == res["K_d4_clifford_samples"] == res["bound_formula_d4"] == 226)
    # 2. 1q 캘리브레이션
    res["F2_cliff1_24"] = frame_potential(c24)
    sub12 = tetrahedral12(c24)
    res["F2_tetrahedral_12"] = frame_potential(sub12) if sub12 else None
    ok_cal = abs(res["F2_cliff1_24"] - 2) < 1e-9 and sub12 and abs(res["F2_tetrahedral_12"] - 2) < 1e-9
    # 3. MUB-20 state 2-design
    N, mub_ok, fp, target = mub20_frame_potential()
    res["mub20"] = {"n_states": N, "mutually_unbiased": mub_ok,
                    "state_frame_potential": fp, "target_2_over_d_d1": target,
                    "is_projective_state_2design": bool(mub_ok and abs(fp - target) < 1e-9)}
    verdict = bool(ok_rank and ok_cal)
    report = {
        "_schema": "twoq-2design-bound-v1",
        "_verdict": "CLOSED-NEGATIVE" if verdict else "INCONCLUSIVE",
        "_claim_refuted": "외부 런타임 '21원소 2q exact unitary 2-design' — 하한 226 위반",
        "theorem": "정확(가중 포함) unitary 2-design |X| ≥ d⁴−2d²+2 = 1+(d²−1)² "
                   "[Gross–Audenaert–Eisert 2007]; 하한의 정체=K(d)=dim span{vec(U⊗Ū)} "
                   "(설계 원소당 기여 방향 1개, 가중치는 rank 불증가)",
        "numerics": res,
        "consequence": "2q exact unitary 2-design 봉인은 ≥226 앱 — 등록부 규모상 비현실 → G2 봉인 트랙 "
                       "정직 종결(closed-negative). 대체 payoff=G2b MUB-20 projective state 2-design "
                       "(Clifford, 규모 게이트).",
        "honest_boundary": "반증 문서(봉인 0·root 불변). rank/FP 수치=float(1e-8/1e-9) witness, "
                           "하한 정리=해석적. V8 cliff1 24개=군 폐포 봉인(최소 2-design 아님) 정직 기록.",
        "seed": 0,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    print("2q unitary 2-design 하한 반증 리포트:", flush=True)
    print(f"  K(d): d=2 haar/cliff {res['K_d2_haar']}/{res['K_d2_clifford24']} (공식 10) · "
          f"d=4 haar/cliff {res['K_d4_haar']}/{res['K_d4_clifford_samples']} (공식 226)", flush=True)
    print(f"  1q F₂: 24원소 {res['F2_cliff1_24']:.9f} · 12원소 사면체 {res['F2_tetrahedral_12']:.9f}", flush=True)
    m = res["mub20"]
    print(f"  MUB-20: unbiased {m['mutually_unbiased']} · state-FP {m['state_frame_potential']:.9f} "
          f"(목표 {m['target_2_over_d_d1']:.9f}) · state 2-design {m['is_projective_state_2design']}", flush=True)
    print(f"  판정: {report['_verdict']} → {os.path.relpath(OUT, ROOT)}", flush=True)
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
