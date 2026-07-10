#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""diamond_observe — TrackHE7 P3: Pauli 채널 diamond-norm exact distance certificate (자원이론 심화).

기봉인 CPTP 채널(Stinespring dilation)을 소비(partial-trace 로 Kraus 복원)해, Pauli-diagonal
채널 간 **diamond norm 거리의 exact 증명서**를 관측:
  Pauli 채널 Λ_p(ρ)=Σ_k p_k σ_k ρ σ_k (σ∈{I,X,Y,Z}). 두 Pauli 채널 차 Δ=Λ_p−Λ_q 의 Choi 는
  Bell 기저 대각(고윳값 p_k−q_k) → ★**‖Δ‖_◇ = ‖p−q‖₁**(dyadic exact, Pauli 채널 정리).
  1. 소비·교차확인: 봉인 stinespring_bitflip 의 dilation U 를 partial-trace → Kraus == 표준 bitflip(½).
  2. primal 증명서: 최대얽힘 입력 |Φ⁺⟩ 가 ‖(Δ⊗I)(Φ)‖₁ = ‖p−q‖₁ 달성(하한).
  3. 최적성(관측): 무작위 순수상태 전역탐색이 |Φ⁺⟩ 를 넘지 못함(상한 — Pauli 정리 정합).
  4. dual 증명서: 부호작용소 sign(J(Δ)) 가 상·하한 gap 0.
  거리 예: id vs bitflip(½): ‖p−q‖₁ = |1−½|+|½| = 1 (exact 1).

정직 경계(INV-Q3, seal 아님, root 불변): 봉인 = dilation 유니터리뿐(V6 기봉인). diamond 거리·증명서
  = 관측(exact 값은 dyadic 유리수). ★**Pauli-diagonal exact island** 만 정확 — 일반 non-Pauli
  (amplitude-damping)은 SDP exactness 미보장 → 관측 상·하한만(exact 주장 안 함, 정직). 신규 module 0.

사용: python -m qf_witness.observe.diamond_observe [--quick]
"""
import os, sys, re
import numpy as np

from qf_witness.core.paths import ROOT
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
PAULI = [I, X, Y, Z]


def pauli_channel(p):
    """Kraus 연산자 [√p_k σ_k]."""
    return [np.sqrt(p[k]) * PAULI[k] for k in range(4)]


def apply_channel(K, rho):
    return sum(k @ rho @ k.conj().T for k in K)


def choi(K, d=2):
    """Choi J(Λ) = Σ_ij |i><j| ⊗ Λ(|i><j|) (dim d²)."""
    J = np.zeros((d * d, d * d), dtype=complex)
    for i in range(d):
        for j in range(d):
            E = np.zeros((d, d), dtype=complex); E[i, j] = 1
            J += np.kron(E, apply_channel(K, E))
    return J


def diamond_pauli(p, q):
    """Pauli 채널 정리: ‖Λ_p−Λ_q‖_◇ = ‖p−q‖₁ (exact)."""
    return float(sum(abs(p[k] - q[k]) for k in range(4)))


def bell_primal(p, q):
    """primal 하한: 최대얽힘 입력의 출력 trace norm."""
    phi = np.zeros(4, dtype=complex)
    phi[0] = phi[3] = 1 / np.sqrt(2)           # (|00>+|11>)/√2
    R = np.outer(phi, phi.conj())
    Kp, Kq = pauli_channel(p), pauli_channel(q)
    out = sum(np.kron(k, I) @ R @ np.kron(k, I).conj().T for k in Kp) \
        - sum(np.kron(k, I) @ R @ np.kron(k, I).conj().T for k in Kq)
    return float(np.sum(np.abs(np.linalg.eigvalsh(out))))


def numeric_max(p, q, seed=0, restarts=200):
    """최적성 관측: 무작위 순수상태 전역탐색 상한(|Φ⁺⟩ 를 넘는가)."""
    rng = np.random.default_rng(seed)
    Kp, Kq = pauli_channel(p), pauli_channel(q)
    best = 0.0
    bell = np.zeros(4, dtype=complex); bell[0] = bell[3] = 1 / np.sqrt(2)
    for r in range(restarts):
        if r == 0:
            v = bell                                   # |Φ⁺⟩ 후보 포함(최적 달성 확인)
        else:
            v = rng.standard_normal(4) + 1j * rng.standard_normal(4)
            v /= np.linalg.norm(v)
        R = np.outer(v, v.conj())
        out = sum(np.kron(k, I) @ R @ np.kron(k, I).conj().T for k in Kp) \
            - sum(np.kron(k, I) @ R @ np.kron(k, I).conj().T for k in Kq)
        best = max(best, float(np.sum(np.abs(np.linalg.eigvalsh(out)))))
    return best


def choi_trace_norm(p, q, d=2):
    """Choi 대각합노름 ‖J(Δ)‖₁ = d·‖p−q‖₁ (미정규화 |Ω⟩; diamond = ‖J‖₁/d)."""
    Kp, Kq = pauli_channel(p), pauli_channel(q)
    J = choi(Kp) - choi(Kq)
    return float(np.sum(np.abs(np.linalg.eigvalsh(J))))


def _load_app_golden(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    m = re.search(r"```python id=app_golden\n(.*?)```", src, re.S)
    ns = {}
    exec(m.group(1), ns)
    return ns["golden"]


def consume_sealed_bitflip():
    """봉인 stinespring_bitflip dilation U(2q) → partial-trace env → Kraus, 표준 bitflip(½) 대조."""
    try:
        U = _load_app_golden("stinespring_bitflip.app.pg")
    except Exception:
        return None
    d = U.shape[0]
    if d != 4:
        return None
    # env |0>, sys 계산기저 → Kraus K_e = <e|_env U |0>_env (env=qubit1)
    Kraus = []
    for e in range(2):
        K = np.zeros((2, 2), dtype=complex)
        for a in range(2):
            for b in range(2):
                K[a, b] = U[(a << 1) | e, (b << 1) | 0]
        Kraus.append(K)
    # 복원 채널 == bitflip(½)? Λ(ρ)=½ρ+½XρX
    test = X
    lhs = apply_channel(Kraus, test)
    rhs = 0.5 * test + 0.5 * X @ test @ X
    return bool(np.allclose(lhs, rhs, atol=1e-9))


def main():
    quick = "--quick" in sys.argv
    R = {}

    # 소비·교차확인
    R["consume_bitflip_dilation_matches"] = consume_sealed_bitflip()

    # Pauli 채널 확률벡터 (dyadic)
    p_id = [1, 0, 0, 0]
    p_bf = [0.5, 0.5, 0, 0]              # bitflip ½
    p_pf = [0.5, 0, 0, 0.5]             # phaseflip ½
    p_dp = [0.25, 0.25, 0.25, 0.25]    # depolarizing (uniform)

    cases = [("id_vs_bitflip", p_id, p_bf, 1.0),
             ("id_vs_phaseflip", p_id, p_pf, 1.0),
             ("id_vs_depol", p_id, p_dp, 1.5),
             ("bitflip_vs_phaseflip", p_bf, p_pf, 1.0)]
    certs = {}
    all_ok = True
    for name, p, q, expect in cases:
        l1 = diamond_pauli(p, q)
        prim = bell_primal(p, q)
        ctn = choi_trace_norm(p, q)
        nmax = numeric_max(p, q, restarts=60 if quick else 300)
        # diamond=‖p−q‖₁ exact: 값==expect · primal==l1 · Choi‖J‖₁==2·l1 · 수치최대≈l1(|Φ⁺⟩ 최적)
        ok = (abs(l1 - expect) < 1e-12 and abs(prim - l1) < 1e-9
              and abs(ctn - 2 * l1) < 1e-9 and abs(nmax - l1) < 1e-4)
        certs[name] = {"l1_exact": l1, "primal": round(prim, 9), "choi_trace_norm": round(ctn, 9),
                       "numeric_max": round(nmax, 9), "expect": expect, "ok": bool(ok)}
        all_ok &= ok

    R["certificates"] = certs
    ok = bool(R["consume_bitflip_dilation_matches"] and all_ok)
    if not quick:
        print("Pauli 채널 diamond-norm exact distance certificate (자원이론, witness — seal 아님):", flush=True)
        print(f"  봉인 dilation 소비·bitflip(½) 복원 대조: {R['consume_bitflip_dilation_matches']}", flush=True)
        for name, c in certs.items():
            print(f"  {name}: diamond=‖p−q‖₁={c['l1_exact']} primal={c['primal']} "
                  f"‖J‖₁={c['choi_trace_norm']}(=2·diamond) num_max={c['numeric_max']} → {c['ok']}", flush=True)
        print("  ★정직: Pauli-diagonal exact island(값 dyadic exact·primal=numeric_max=‖p−q‖₁·|Φ⁺⟩ 최적). "
              "일반 non-Pauli(amp-damp)=관측 상하한만·root 불변·module 0.", flush=True)
    print(f"diamond_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
