# -*- coding: utf-8 -*-
"""
gridsynth_family.py — TrackHE14 P6a: R_z(π/2^k) Clifford+T 근사회로 실봉인 (§2 부분해제)

§2 "표현론 Fourier 실봉인 경계"(무리수 각 회전은 신규 module 없이 불가)의 **부분 해제**:
특정 각 R_z(π/2^k) (k=3..7) 에 대해 **기봉인 h_gate·t_gate 만으로** 조립되는 Clifford+T
근사회로를 봉인한다. 회로 엔트리는 ℤ[ω]/√2^m (ω=ζ₈) 에 **정확** — MatrixGate/float 아님,
honest 게이트 시퀀스. 신규 module 0.

봉인 대상 (전부 Tier-0 EXACT — "그 회로의 unitary" exact, 목표 근사 품질은 봉인 아님):
  rz_pi8_ct · rz_pi16_ct · rz_pi32_ct · rz_pi64_ct · rz_pi128_ct  (1q, h/t 시퀀스)

시퀀스 출처(생성≠검증): dev-time 결정론 탐색(Matsumoto-Amano 정규형 부분가족
  T^a·(H T^b)*·[H], b∈{1,2}, 블록≤16, 사전순 tie-break)의 고정 결과를 하드코딩.
  ★tightness 무주장: Ross-Selinger 최적 합성 대비 ε 큼(ε ~ 1e-2 급) — 존재 구성이 목적.

정직성 경계:
 - 봉인 = 시퀀스 회로의 unitary 정확성(composite==golden, 오라클 C2 up-to-phase).
 - 봉인 아님 = 목표 R_z(π/2^k) 대비 거리 ε — **ε-인증 sidecar**(approx_certify 확장,
   sympy symbolic exact: ε = √(2−|tr(U†R)|) = min_φ‖e^{iφ}U−R‖₂, 2×2 등식) 로 분리.
 - ★ℤ[ω] 정합 검증: 전 엔트리 √2^{#H}·entry ∈ ℤ[ω] 를 정수산술로 확인(exact ring shadow)
   + float 대조 < 1e-12. Clifford+T 의 대수적 정확성이 "honest 분해" 주장의 근거.
 - 신규 module 0 → second_oracle 불변. 앱만 +5 (root 성장).

사용:  python -m qf_witness.family.gridsynth_family
"""
from __future__ import annotations

import os
import sys
import json

import numpy as np

from qf_witness.core.paths import ROOT
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, ORACLE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import app_assemble as aa       # noqa: E402  (앱 봉인 — 사용만)

SPECS_APPS = os.path.join(ROOT, "specs", "apps")
APPREG = os.path.join(ROOT, "registry", "apps")
OUT = os.path.join(ROOT, ".pgf", "arith")

# ── 고정 시퀀스 (dev-time 결정론 탐색 결과; 시간순 좌→우) ──────────────────
SEQS = {
    "rz_pi8_ct":   (3, "TTTTTTTHTHTHTTHTTHTTHTTHTHTHTHTTHTHTTHTTHTTHTHTT"),
    "rz_pi16_ct":  (4, "HTHTHTHTHTHTHTTHTHTTHTHTTHTHTT"),
    "rz_pi32_ct":  (5, "TTTTTTTHTTHTHTHTHTTHTHTHTHTHTTHTHTHTHTHT"),
    "rz_pi64_ct":  (6, "TTTTTTTHTHTHTHTHTTHTHTHTHTHTTHTHTHTHTTHT"),
    "rz_pi128_ct": (7, "TTTTTTTHTHTTHTTHTTHTTHTTHTTHTTHTTHTHTTHTTHTTHT"),
}

# ── GridsynthDeepen: Ross-Selinger-형 합성 결과 (ε≤1e-4, dev-time 산출 고정) ──
# 방법(생성≠검증): ℤ[ω] 격자 후보(σ-임베딩 이중구속·PSU 반경조건 scale≥1/ε²) →
#   ξ=2^m−u†u ∈ ℤ[√2] 노름방정식(N(ξ) 소수·Tonelli-Shanks·norm-Euclidean gcd·
#   totally-positive unit λ² 보정) → 정확합성(1열 lde 축차감소, m-유지 플래토 BFS 횡단).
# m=54·T-count 198~226. ★T-count 최적화 무주장(R-S 최적 ~3log₂(1/ε) 대비 큼 — ε 달성이 목적).
SEQS_RS = {
    "rz_pi8_rs":   (3, "TTHTTTTHHTTTHTHTTTHTTTHTHTTTHTHTTTHTHTTTHTHTTTHTHTHTTTHTHTTTHTTTHTTTHTHTHTHTHTHTTTHTHTTTHTTTHTHTTTHTTTHTTTHTHTHTTTHTHTHTTTHTTTHTTTHTHTTTHTTTHTHTHTTTHTTTHTHTTTHTTTHTHTHTTTHTTTHTTTHTHTTTHTTTHTHTTTHTTTHTHTHTHTHTHTHTTTHTHTTTHTHTHTTTHTTTHTHTTTHTTTHTTTHTTTHTTTHTHTTTHTTTHTTTHTTTHTHTTTHTHTTTHTHTTTHTTTHTTTHTHTTTHTHTTTHTHTHTHTHTHTHTHTHTH"),
    "rz_pi16_rs":  (4, "TTTTTTHTHTTTHTHTHTHTTTHTHTHTHTTTHTTTHTHTHTHTTTHTHTTTHTTTHTHTTTHTHTTTHTTTHTTTHTTTHTTTHTTTHTHTTTHTTTHTHTHTTTHTTTHTTTHTHTTTHTHTHTHTHTTTHTTTHTTTHTTTHTTTHTHTHTTTHTTTHTTTHTTTHTHTHTTTHTHTHTHTHTHTTTHTHTTTHTHTTTHTHTHTHTHTTTHTTTHTTTHTTTHTHTHTTTHTHTTTHTTTHTHTHTTTHTTTHTHTHTHTTTHTTTHTHTHTTTHTTTHTHTHTTTHTHTHTTTHTTTHTTTHTTTHTHTHTHTTTHTH"),
    "rz_pi32_rs":  (5, "TTTTTHTHTHTHTHTHTTTHTTTHTTTHTHTHTHTTTHTTTHTTTHTHTTTHTHTTTHTHTTTHTTTHTHTTTHTHTHTHTHTHTHTTTHTTTHTTTHTTTHTHTTTHTHTTTHTTTHTTTHTHTTTHTTTHTHTHTHTTTHTHTTTHTHTTTHTTTHTTTHTTTHTHTHTTTHTHTHTTTHTHTHTHTHTHTHTHTHTHTHTTTHTHTHTTTHTHTTTHTHTTTHTHTHTHTHTTTHTHTTTHTHTTTHTTTHTHTHTHTHTHTTTHTHTHTTTHTHTHTTTHTHTTTHTHTHTTTHTTTHTHT"),
    "rz_pi64_rs":  (6, "TTTTTTHTTTHTTTHTTTHTTTHTTTHTHTHTHTHTHTTTHTTTHTHTTTHTHTTTHTTTHTHTTTHTHTHTTTHTHTHTTTHTHTHTHTTTHTTTHTTTHTTTHTTTHTHTHTHTTTHTTTHTHTHTTTHTTTHTTTHTHTTTHTHTTTHTTTHTHTTTHTTTHTHTHTHTHTTTHTTTHTTTHTHTTTHTTTHTHTHTHTHTHTHTHTTTHTHTTTHTHTHTTTHTTTHTTTHTHTHTHTTTHTTTHTTTHTTTHTTTHTTTHTTTHTTTHTTTHTHTTTHTHTHTHTTTHTTTHTHTTTHTHTTTHTTTHTTTHTTTHTTTHTTTHTHTH"),
    "rz_pi128_rs": (7, "TTTTHTHTHTHTTTHTHTHTHTTTHTHTHTTTHTHTHTHTTTHTTTHTHTTTHTTTHTHTTTHTHTTTHTTTHTHTTTHTTTHTHTTTHTTTHTHTTTHTHTHTTTHTHTHTTTHTHTHTTTHTHTHTHTTTHTTTHTTTHTTTHTTTHTHTTTHTHTHTTTHTHTTTHTHTTTHTTTHTHTTTHTHTTTHTTTHTHTHTTTHTHTHTTTHTTTHTHTTTHTHTHTHTTTHTHTHTTTHTTTHTTTHTHTHTTTHTHTTTHTHTHTHTTTHTHTHTTTHTHTTTHTTTHTTTHTTTHTHTTTHTTTHTTTHTTTHTTTHTTTH"),
}

ALL_SEQS = {**SEQS, **SEQS_RS}


# ── ℤ[ω] 정확 ring shadow (ω=ζ₈, ω⁴=−1): 원소 = (a,b,c,d) = a+bω+cω²+dω³ ──
def w_mul(x, y):
    a, b, c, d = x; e, f, g, h = y
    return (a * e - b * h - c * g - d * f,
            a * f + b * e - c * h - d * g,
            a * g + b * f + c * e - d * h,
            a * h + b * g + c * f + d * e)


def w_add(x, y):
    return tuple(p + q for p, q in zip(x, y))


W0 = (0, 0, 0, 0)
W1 = (1, 0, 0, 0)
WOM = (0, 1, 0, 0)


def m2_mul(A, B):
    return ((w_add(w_mul(A[0][0], B[0][0]), w_mul(A[0][1], B[1][0])),
             w_add(w_mul(A[0][0], B[0][1]), w_mul(A[0][1], B[1][1]))),
            (w_add(w_mul(A[1][0], B[0][0]), w_mul(A[1][1], B[1][0])),
             w_add(w_mul(A[1][0], B[0][1]), w_mul(A[1][1], B[1][1]))))


# √2·H, T ∈ ℤ[ω] 행렬 (H 는 √2 분모 1개 지연 — m 이 지수 누적)
H_RING = ((W1, W1), (W1, (-1, 0, 0, 0)))                          # √2·H = [[1,1],[1,−1]]
T_RING = ((W1, W0), (W0, WOM))


def ring_shadow(seq):
    """시퀀스 → (M ∈ ℤ[ω] 2×2, m = √2 지수).  U = M/√2^m."""
    M = ((W1, W0), (W0, W1))
    m = 0
    for g in seq:
        if g == "H":
            M = m2_mul(H_RING, M)
            m += 1
        else:
            M = m2_mul(T_RING, M)
    return M, m


def w_to_complex(x):
    om = np.exp(1j * np.pi / 4)
    return x[0] + x[1] * om + x[2] * om ** 2 + x[3] * om ** 3


def seq_unitary_float(seq):
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    T = np.diag([1, np.exp(1j * np.pi / 4)]).astype(complex)
    U = np.eye(2, dtype=complex)
    for g in seq:
        U = (H if g == "H" else T) @ U
    return U


def verify_ring_exact(seq):
    """ℤ[ω]/√2^m shadow 가 float 곱과 일치(<1e-12) + m == #H."""
    M, m = ring_shadow(seq)
    Uf = seq_unitary_float(seq)
    Ur = np.array([[w_to_complex(M[0][0]), w_to_complex(M[0][1])],
                   [w_to_complex(M[1][0]), w_to_complex(M[1][1])]],
                  dtype=complex) / (np.sqrt(2) ** m)
    return bool(m == seq.count("H") and np.max(np.abs(Ur - Uf)) < 1e-12), m


# ── 앱 spec 생성 ───────────────────────────────────────────────────────────
def make_spec(app_id, k, seq):
    plan = {"steps": [{"spec": f"../modules/{'h_gate' if g == 'H' else 't_gate'}.pg",
                       "targets": [0]} for g in seq]}
    golden_py = (
        "import numpy as np\n"
        "H = np.array([[1,1],[1,-1]],dtype=complex)/np.sqrt(2)\n"
        "T = np.diag([1, np.exp(1j*np.pi/4)]).astype(complex)\n"
        f"seq = {seq!r}\n"
        "U = np.eye(2,dtype=complex)\n"
        "for g in seq:\n"
        "    U = (H if g=='H' else T) @ U\n"
        "golden = U\n")
    return (
        f"# {app_id} — R_z(π/{2**k}) Clifford+T 근사회로(honest h/t 시퀀스, 엔트리 ℤ[ω]/√2^m 정확). "
        f"봉인=회로 unitary EXACT; 목표 대비 ε 는 APPROX-GUARANTEES sidecar(관측·인증 분리). "
        f"§2 부분해제: 신규 module 0.\n"
        '```json id=app_meta\n'
        + json.dumps({"id": app_id, "n_sys": 1, "n_anc": 0}) + "\n"
        "```\n"
        "```python id=app_golden\n" + golden_py + "```\n"
        '```json id=plan\n' + json.dumps(plan) + "\n```\n")


def _forge_app(app_id, spec):
    sp_path = os.path.join(SPECS_APPS, f"{app_id}.app.pg")
    open(sp_path, "w", encoding="utf-8", newline="\n").write(spec)
    v = aa.assemble(sp_path, APPREG)
    return {"id": app_id, "n_sys": v.n_sys, "sealed": bool(v.sealed), "tier": v.tier,
            "u_hash": v.u_hash, "reason": v.reason}


def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 84)
    print("TrackHE14 P6a gridsynth — R_z(π/2^k) Clifford+T 근사회로 실봉인 (§2 부분해제, 신규 module 0)")
    print("=" * 84)

    apps, rings, eps_obs = [], {}, {}
    for app_id, (k, seq) in ALL_SEQS.items():
        ok_ring, m = verify_ring_exact(seq)
        rings[app_id] = {"ring_exact": ok_ring, "sqrt2_denom_exp": m,
                         "t_count": seq.count("T"), "length": len(seq)}
        a = _forge_app(app_id, make_spec(app_id, k, seq))
        apps.append(a)
        # 관찰(seal 아님): 목표 대비 위상정렬 op-norm 거리 (인증은 approx_certify sidecar)
        U = seq_unitary_float(seq)
        R = np.diag([np.exp(-1j * np.pi / 2 ** (k + 1)), np.exp(1j * np.pi / 2 ** (k + 1))])
        eps_obs[app_id] = float(np.sqrt(max(0.0, 2 - abs(np.trace(U.conj().T @ R)))))
        print(f"[App] {app_id:12} sealed={a['sealed']} tier={a.get('tier')} "
              f"T-count={rings[app_id]['t_count']} ring_exact={ok_ring} "
              f"eps_obs={eps_obs[app_id]:.5f} u={str(a.get('u_hash'))[:14]}"
              + ("" if a["sealed"] else f" reason={a['reason']}"))

    report = {
        "phase": "TrackHE14 P6a gridsynth Clifford+T",
        "honesty": ("Seals Clifford+T approximation circuits for R_z(pi/2^k), k=3..7, assembled ONLY "
                    "from sealed h_gate/t_gate (ZERO new modules). Each seal is Tier-0 EXACT for the "
                    "circuit's own unitary (entries exactly in Z[omega]/sqrt(2)^m, ring shadow verified); "
                    "the distance to the TARGET R_z is NOT sealed — it is certified separately in the "
                    "APPROX-GUARANTEES sidecar (phase-aligned op-norm, sympy exact) and observed here as "
                    "eps_obs (~1e-2 grade; Ross-Selinger optimality NOT claimed — existence construction "
                    "partially lifting the Section-2 Fourier real-seal boundary)."),
        "apps": apps, "ring_shadow": rings, "eps_observed_float": eps_obs,
    }
    all_ok = (all(a["sealed"] and a["tier"] == 0 for a in apps)
              and all(r["ring_exact"] for r in rings.values()))
    report["all_ok"] = bool(all_ok)
    json.dump(report, open(os.path.join(OUT, "GRIDSYNTH-FAMILY-REPORT.json"), "w",
                           encoding="utf-8"), ensure_ascii=False, indent=2)
    print("-" * 84)
    print(f"all_ok={all_ok}  →  .pgf/arith/GRIDSYNTH-FAMILY-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
