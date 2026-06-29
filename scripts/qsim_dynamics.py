# -*- coding: utf-8 -*-
"""
qsim_dynamics.py — Stage 8 W8.4 TrotterDynamics (관찰 전용 계층, 봉인 0)

봉인된 Trotter step(W8.1~8.3)을 backend_adapter 로 **반복 실행**해 물리 관측량의 시간 동역학을
관찰하고 exact 대각화와 대조한다. 신규 봉인 0 — registry/오라클/frozen/root **불변**.

═══════════════════════════════════════════════════════════════════════════
정직성 경계 (절대 흐리지 말 것)
═══════════════════════════════════════════════════════════════════════════
 ① 봉인 ≠ 실행: 봉인은 step *분해*의 정확성(W8.1~8.3). 여기서는 봉인된 그 step(u_hash 게이트)을
    U^k 로 *실행*해 동역학을 관찰. 시뮬레이터 출력은 봉인의 증거가 아니다.
 ② 실행 ≠ 검증: spec §8.4 "behavioral check is illustrative only".
 ③ 근사 ≠ exact: Trotter 궤적 vs 진짜 e^{-iHt} 의 편차 = Trotter 오차(관측량 공간 가시화).
 ★ 차수의 basis-의존(honest, 비자명): s1 = A^{1/2}·s2·A^{-1/2} (A=ΠZZ(dt)) → 1·2차 Trotter 는
    Z-대각 유니터리로 켤레. Z-basis 초기상태에서 ⟨Z⟩·⟨ZZ⟩ 관측량은 1차==2차(측정통계가 차수를
    구별 못함). 차수 우월(2차)은 transverse ⟨X⟩ 에서만 드러난다.

이 도구는 backend_adapter(load_sealed_app·get_backends·expect_z·corr_zz)를 *사용만* 한다.
exact 참조는 독립 대각화(봉인 아님, 명시적 대조용).

사용:  python scripts/qsim_dynamics.py
"""
from __future__ import annotations

import os
import sys
import json
import warnings

import numpy as np

# cirq MatrixGate 를 8회 반복 적용하면 statevector norm 이 ~1e-8 수준 float drift 를 일으켜
# cirq 가 "skipping renormalization" 경고를 낸다(무해 — 백엔드간 일치는 atol=1e-6 로 별도 확인).
warnings.filterwarnings("ignore", message=".*norm.*too far from 1.*")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import backend_adapter as ba  # noqa: E402  (실행 계층 — 사용만)

OUT = os.path.join(ROOT, ".pgf", "backend")

DT = np.pi / 8     # 봉인된 step 의 dt (W8.1~8.3 인스턴스와 동일)
KMAX = 8           # k=0..8 → t=0..π

_I2 = np.eye(2, dtype=complex)
_X = np.array([[0, 1], [1, 0]], complex)
_Z = np.diag([1, -1]).astype(complex)


# ── 독립 관측자: ⟨X_q⟩ (backend_adapter 에 없는 transverse 관측량) ────────────────
def _expect_x(psi, n, q):
    """⟨X_q⟩ = Σ_i conj(psi_i)·psi_{i⊕bit_q} (big-endian)."""
    out = 0j
    flip = 1 << (n - 1 - q)
    for i in range(len(psi)):
        out += np.conj(psi[i]) * psi[i ^ flip]
    return float(out.real)


# ── 독립 exact 참조: TFIM H = -(Σ ZZ + Σ X), e^{-iHt} (봉인 아님, 대조용) ─────────
def _tfim_exact_propagator(n):
    def opn(ps):
        m = np.array([[1]], dtype=complex)
        for q in range(n):
            m = np.kron(m, ps.get(q, _I2))
        return m
    bonds = [(i, i + 1) for i in range(n - 1)]
    H = -(sum(opn({i: _Z, j: _Z}) for i, j in bonds) + sum(opn({i: _X}) for i in range(n)))
    w, V = np.linalg.eigh(H)

    def exact(t):
        return V @ np.diag(np.exp(-1j * w * t)) @ V.conj().T
    return exact


def _trajectory(U, n, kmax, backends):
    """psi_k = U^k |0...0> 를 모든 백엔드로 실행 → 관측량 궤적 + 백엔드 일치."""
    psi0 = ba.zero_state(n)
    traj = {bk.name: psi0.copy() for bk in backends}
    rows = []
    agree = True
    for k in range(kmax + 1):
        ref = traj[backends[0].name]
        for bk in backends[1:]:
            if not np.allclose(ref, traj[bk.name], atol=1e-6):
                agree = False
        rows.append({"k": k, "t": round(k * DT, 6),
                     "Z0": round(ba.expect_z(ref, n, 0), 6),
                     "X0": round(_expect_x(ref, n, 0), 6),
                     "Z0Z1": round(ba.corr_zz(ref, n, 0, 1), 6)})
        for bk in backends:
            traj[bk.name] = bk.run(U, traj[bk.name])
    return rows, agree


def _exact_trajectory(exact, n, kmax):
    psi0 = ba.zero_state(n)
    rows = []
    for k in range(kmax + 1):
        psi = exact(k * DT) @ psi0
        rows.append({"k": k, "t": round(k * DT, 6),
                     "Z0": round(ba.expect_z(psi, n, 0), 6),
                     "X0": round(_expect_x(psi, n, 0), 6),
                     "Z0Z1": round(ba.corr_zz(psi, n, 0, 1), 6)})
    return rows


def _max_dev(a, b, key):
    return round(max(abs(a[i][key] - b[i][key]) for i in range(len(a))), 6)


def observe_tfim(n, app1, app2):
    """1차(app1)·2차(app2) 봉인 step 을 실행해 동역학 관찰 + exact 대조 + 차수 basis-의존."""
    backends = ba.get_backends()
    s1 = ba.load_sealed_app(app1)   # u_hash 게이트 — 봉인된 그 step 만
    s2 = ba.load_sealed_app(app2)
    exact = _tfim_exact_propagator(n)

    t1, ag1 = _trajectory(s1["U"], n, KMAX, backends)
    t2, ag2 = _trajectory(s2["U"], n, KMAX, backends)
    te = _exact_trajectory(exact, n, KMAX)

    # ③ 근사≠exact: Trotter 편차(관측량 공간). t 증가에 따라 성장.
    dev1_X = _max_dev(t1, te, "X0")
    dev2_X = _max_dev(t2, te, "X0")
    dev1_Z = _max_dev(t1, te, "Z0")

    # ★ 차수 basis-의존: Z-관측량은 1차==2차, X-관측량은 2차가 exact 더 근접.
    z_blind = max(abs(t1[k]["Z0"] - t2[k]["Z0"]) for k in range(KMAX + 1))
    zz_blind = max(abs(t1[k]["Z0Z1"] - t2[k]["Z0Z1"]) for k in range(KMAX + 1))

    # ③ 근사≠exact: Trotter 편차가 관측량 공간에 *실재*(가시적, 비영). 단일 관측량의 편차는
    #    단조롭지 않음(진동) → "성장" 주장 대신 "관측가능하게 존재"를 정직하게 검사.
    checks = {
        "backends_agree": bool(ag1 and ag2),
        "Z_observables_order_blind": z_blind < 1e-6 and zz_blind < 1e-6,
        "X_reveals_order_2nd_closer": dev2_X < dev1_X,
        "trotter_error_observable_in_X": dev1_X > 1e-3,
    }
    return {
        "system": f"tfim{n}",
        "sealed_steps": {"first_order": {"id": app1, "u_hash": s1["u_hash"], "tier": s1["tier"]},
                         "second_order": {"id": app2, "u_hash": s2["u_hash"], "tier": s2["tier"]}},
        "dt": round(DT, 6), "k_range": [0, KMAX], "t_range": [0.0, round(KMAX * DT, 6)],
        "trajectory_first_order": t1,
        "trajectory_second_order": t2,
        "trajectory_exact": te,
        "observable_space_trotter_error": {
            "max_dev_X0_first_order": dev1_X, "max_dev_X0_second_order": dev2_X,
            "max_dev_Z0_first_order": dev1_Z,
            "note": "Trotter error is visible in <X0> (dev>1e-3); a single observable's deviation "
                    "oscillates (not monotone in t), so we assert it is observably present, not 'growing'."},
        "order_basis_dependence": {
            "Z0_1st_vs_2nd_maxdiff": round(z_blind, 9),
            "Z0Z1_1st_vs_2nd_maxdiff": round(zz_blind, 9),
            "X0_max_dev_vs_exact_1st": dev1_X, "X0_max_dev_vs_exact_2nd": dev2_X,
            "note": "s1=A^{1/2}·s2·A^{-1/2} (A=ΠZZ(dt)) → Z-diagonal conjugacy. From a Z-basis "
                    "initial state, <Z>/<ZZ> are identical for 1st/2nd order (measurement is "
                    "order-blind); only transverse <X> reveals that 2nd-order tracks exact closer."},
        "expectation_checks": checks,
        "all_expectations_met": all(checks.values()),
    }


def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 78)
    print("W8.4 TrotterDynamics — 봉인 Trotter step 반복 실행 → 시간 동역학 관찰(봉인 0, root 불변).")
    print("정직성: 봉인 ≠ 실행 ≠ 검증; Trotter 궤적 vs exact 편차 = 근사오차(관찰).")
    print(f"백엔드: {[b.name for b in ba.get_backends()]}")
    print("=" * 78)

    cases = [(3, "tfim3_trotter_step", "tfim3_trotter_step2"),
             (4, "tfim4_trotter_step", "tfim4_trotter_step2")]
    results = []
    all_ok = True
    for n, a1, a2 in cases:
        try:
            r = observe_tfim(n, a1, a2)
        except Exception as e:
            r = {"system": f"tfim{n}", "error": f"{type(e).__name__}: {e}", "all_expectations_met": False}
            all_ok = False
        ok = r.get("all_expectations_met", False)
        all_ok = all_ok and ok
        results.append(r)
        if "error" in r:
            print(f"  ✗ tfim{n}: {r['error']}")
            continue
        ose = r["observable_space_trotter_error"]; ck = r["expectation_checks"]
        print(f"  {'✓' if ok else '✗'} tfim{n}: 봉인 step 실행 → ⟨X₀⟩ max Trotter오차 "
              f"1차={ose['max_dev_X0_first_order']} 2차={ose['max_dev_X0_second_order']} (2차 우월)")
        print(f"      ★차수 basis-의존: ⟨Z₀⟩ 1차-2차 차이={r['order_basis_dependence']['Z0_1st_vs_2nd_maxdiff']} "
              f"(Z-측정 차수-blind) · ⟨X₀⟩ 2차 우월={ck['X_reveals_order_2nd_closer']} · "
              f"backends_agree={ck['backends_agree']}")

    # 부정 테스트: 봉인 게이트가 변조 거부(backend_adapter teeth 재사용)
    neg = ba.negative_gate_test()

    report = {
        "phase": "W8.4 TrotterDynamics",
        "honesty_boundary": "Observation-only layer; NOTHING is sealed (registry/oracle/frozen/root "
                            "untouched, root stays 566b0368). Input = already-sealed Tier-0 Trotter "
                            "steps (u_hash gated); executed as U^k for time dynamics. Three boundaries "
                            "closed: sealing(decomposition) != execution(simulation) != verification; "
                            "and approximation != exact (Trotter error visible in observable space). "
                            "Honest subtlety: 1st/2nd order Trotter are Z-diagonal conjugate "
                            "(s1=A^{1/2} s2 A^{-1/2}), so from a Z-basis state <Z>/<ZZ> are "
                            "order-blind; only transverse <X> shows 2nd-order tracking exact closer.",
        "backends": [b.name for b in ba.get_backends()],
        "negative_gate_test": neg,
        "systems": results,
    }
    report["all_ok"] = bool(all_ok and neg["real_hash_ne_tampered"])
    json.dump(report, open(os.path.join(OUT, "TROTTER-DYNAMICS-REPORT.json"), "w",
                           encoding="utf-8"), ensure_ascii=False, indent=2)
    print("-" * 78)
    print(f"all_ok={report['all_ok']}  →  .pgf/backend/TROTTER-DYNAMICS-REPORT.json")
    return 0 if report["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
