# -*- coding: utf-8 -*-
"""
qae2_family.py — Stage 9 W9.3 QAEDeepening

W9.2(QAE instance)를 family로: ① 두 번째 exact QPE-QAE 인스턴스(a=1/2, 신규 모듈 0); ② iterative/
power QAE(QPE-free) — P_good(m)=sin²((2m+1)θ) 곡선의 고전 fit으로 *임의* θ 추정(QPE bin 에 안 떨어지는
일반 진폭 a=1/4·1/8). backend_adapter 실행 계층 복리.

봉인 대상(전부 Tier-0 EXACT, 신규 모듈 0 — 봉인 부품 복리):
 1. qae3_pi2 (app, 4q)      = QPE(t=3) on Q=Ry(π) → a=1/2 추정 (ry_pi2·z_gate·cry_pi·iqft3).
 2. grover2_3iter (app, 2q) = G₂³ (Grover iteration m=3).
 3. grover3_3iter (app, 3q) = G₃³.

정직성 경계:
 - 봉인 = 회로/연산자 분해의 정확성. composite==golden(up-to-phase), MatrixGate 0. 신규 모듈 0 →
   second_oracle 61/61 불변. 봉인 부품(grover2/3·ry_pi2·cry_pi·z_gate·h_gate·iqft3) 복리.
 - 봉인 아님 = 진폭 추정 *행동*(_iterative_qae_observation): backend_adapter 로 봉인 Grover power 실행
   (u_hash 게이트)→P_good(m) 곡선→고전 fit. execution≠verification; 추정치는 관찰.
 - ★QPE-QAE(특수진폭만 exact) vs iterative-QAE(임의진폭, 정밀도=측정수 의존) trade-off 정직 표기.

사용:  python scripts/qae2_family.py
"""
from __future__ import annotations

import os
import sys
import json

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, ORACLE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import app_assemble as aa       # noqa: E402  (앱 봉인 — 사용만)
import backend_adapter as ba    # noqa: E402  (실행 계층 — 사용만, iterative QAE 관찰)

SPECS_APPS = os.path.join(ROOT, "specs", "apps")
APPREG = os.path.join(ROOT, "registry", "apps")
OUT = os.path.join(ROOT, ".pgf", "arith")


# ── 앱 spec ────────────────────────────────────────────────────────────────────
_QAE3_PI2_SPEC = (
    "# qae3_pi2 — QPE(t=3) on Grover Q=Ry(π) → 진폭 a=1/2 추정 (4q). 두 번째 exact QPE-QAE 인스턴스. "
    "Q^4=Ry(4π)=I→c0 무게이트·Q^2=-I→z_gate(c1)·Q^1=Ry(π)→cry_pi(c2,work). 신규 모듈 0(봉인 부품 복리). "
    "golden=16×16 closed-form. readout y∈{2,6}→a_est=sin²(π/4)=1/2.\n"
    '```json id=app_meta\n'
    '{"id": "qae3_pi2", "n_sys": 4, "n_anc": 0}\n'
    "```\n"
    "```python id=app_golden\n"
    "import numpy as np\n"
    "n=4\n"
    "def Ry(al): return np.array([[np.cos(al/2),-np.sin(al/2)],[np.sin(al/2),np.cos(al/2)]],dtype=complex)\n"
    "I2=np.eye(2,dtype=complex); Z=np.diag([1,-1]).astype(complex)\n"
    "H1=np.array([[1,1],[1,-1]],dtype=complex)/np.sqrt(2)\n"
    "def emb(g,qs):\n"
    "    k=len(qs); G=g.reshape([2]*k+[2]*k)\n"
    "    T=np.eye(1<<n,dtype=complex).reshape([2]*n+[1<<n])\n"
    "    T=np.tensordot(G,T,axes=(list(range(k,2*k)),qs)); T=np.moveaxis(T,list(range(k)),qs)\n"
    "    return T.reshape(1<<n,1<<n)\n"
    "def cU(U):\n"
    "    M=np.eye(4,dtype=complex); M[2:,2:]=U; return M\n"
    "N=8; w=np.exp(2j*np.pi/N)\n"
    "QFT3=np.array([[w**(j*k) for k in range(N)] for j in range(N)],dtype=complex)/np.sqrt(N)\n"
    "iqft3=QFT3.conj().T\n"
    "th=np.pi/4; Q=Ry(4*th)   # Q=Ry(π)\n"
    "U=np.eye(1<<n,dtype=complex)\n"
    "U=emb(Ry(2*th),[3])@U                                      # A 진폭준비 (a=sin²(π/4)=1/2)\n"
    "for q in range(3): U=emb(H1,[q])@U\n"
    "U=emb(cU(np.linalg.matrix_power(Q,4)),[0,3])@U             # controlled-Q^4 (=I)\n"
    "U=emb(cU(np.linalg.matrix_power(Q,2)),[1,3])@U             # controlled-Q^2 (=-I → z on ctrl)\n"
    "U=emb(cU(np.linalg.matrix_power(Q,1)),[2,3])@U             # controlled-Q^1 (=Ry(π))\n"
    "U=emb(iqft3,[0,1,2])@U\n"
    "golden=U\n"
    "```\n"
    '```json id=plan\n'
    + json.dumps({"steps": [
        {"spec": "../modules/ry_pi2.pg", "targets": [3]},
        {"spec": "../modules/h_gate.pg", "targets": [0]},
        {"spec": "../modules/h_gate.pg", "targets": [1]},
        {"spec": "../modules/h_gate.pg", "targets": [2]},
        {"spec": "../modules/z_gate.pg", "targets": [1]},
        {"app": "cry_pi.app.pg", "targets": [2, 3]},
        {"app": "iqft3.app.pg", "targets": [0, 1, 2]}]}) + "\n"
    "```\n")


def _grover_iter_spec(name, base_app, n_sys, marked_idx, m):
    """Grover power G^m: golden = (D∘O)^m, plan = [base_app] * m."""
    dim = 1 << n_sys
    return (
        f"# {name} — {n_sys}큐비트 Grover {m}-iterate G^{m} (iterative QAE power). plan=[{base_app}]×{m} 복리.\n"
        '```json id=app_meta\n'
        + json.dumps({"id": name, "n_sys": n_sys, "n_anc": 0}) + "\n"
        "```\n"
        "```python id=app_golden\n"
        "import numpy as np\n"
        f"H1=np.array([[1,1],[1,-1]],dtype=complex)/np.sqrt(2); dim={dim}; nq={n_sys}\n"
        "Hn=np.array([[1]],dtype=complex)\n"
        "for _ in range(nq): Hn=np.kron(Hn,H1)\n"
        "refl=np.full((dim,dim),0.0,dtype=complex); refl[0,0]=1.0\n"
        "refl=2*refl-np.eye(dim)              # 2|0><0|-I\n"
        "D=Hn@refl@Hn                          # diffusion 2|s><s|-I\n"
        "O=np.eye(dim,dtype=complex); O[%d,%d]=-1   # oracle: mark target\n" % (marked_idx, marked_idx)
        + "G=D@O\n"
        f"golden=np.linalg.matrix_power(G,{m})\n"
        "```\n"
        '```json id=plan\n'
        + json.dumps({"steps": [{"app": f"{base_app}.app.pg"} for _ in range(m)]}) + "\n"
        "```\n")


def _forge_app(name, spec):
    sp = os.path.join(SPECS_APPS, f"{name}.app.pg")
    open(sp, "w", encoding="utf-8", newline="\n").write(spec)
    v = aa.assemble(sp, APPREG)
    return {"id": name, "n_sys": v.n_sys, "sealed": bool(v.sealed), "tier": v.tier,
            "u_hash": v.u_hash, "reason": v.reason}


# ── 정직-behavior: QPE-QAE readout (qae3_pi2, a=1/2) ────────────────────────────
def _qpe_qae_observation():
    app = ba.load_sealed_app("qae3_pi2")     # u_hash 게이트
    n = app["n"]
    psi = app["U"] @ ba.zero_state(n)
    p = np.abs(psi) ** 2
    marg = {}
    for i in range(1 << n):
        if p[i] > 1e-9:
            c = i >> 1
            marg[c] = marg.get(c, 0.0) + float(p[i])
    t = 3
    peaks = [{"y": int(y), "prob": round(marg[y], 6),
              "a_est": round(float(np.sin(np.pi * y / (1 << t)) ** 2), 6)}
             for y in sorted(marg, key=lambda k: -marg[k]) if marg[y] > 1e-6]
    return {"note": "QPE-QAE one-shot readout (observation). Exact only for special amplitudes "
                    "(2θ/2π=k/2^t); a=1/2 -> y in {2,6}, a_est=sin^2(pi/4)=0.5.",
            "a_true": 0.5, "peaks": peaks,
            "exact_recovery": all(abs(pk["a_est"] - 0.5) < 1e-6 for pk in peaks)}


# ── 정직-behavior: iterative QAE (QPE-free), backend_adapter 실행 ────────────────
def _iterative_qae_observation():
    results = {}
    # (app_id 시퀀스 m=1..3 = 봉인 Grover power; m=0 = |s> baseline)
    for label, powers, n_sys, target, Ntot in [
        ("grover2", ["grover2", "grover2_2iter", "grover2_3iter"], 2, 3, 4),
        ("grover3", ["grover3", "grover3_2iter", "grover3_3iter"], 3, 7, 8),
    ]:
        s = ba.uniform_state(n_sys)
        a_true = 1.0 / Ntot
        Pm = [float(np.abs(s[target]) ** 2)]   # m=0: |s> baseline = a_true
        for app_id in powers:
            app = ba.load_sealed_app(app_id)    # u_hash 게이트 — 봉인된 그 Grover power 실행
            psi = app["U"] @ s
            Pm.append(float(np.abs(psi[target]) ** 2))
        # 고전 least-squares fit: P_good(m)=sin²((2m+1)θ)
        grid = np.linspace(1e-4, np.pi / 2 - 1e-4, 30000)
        errs = [sum((np.sin((2 * m + 1) * g) ** 2 - Pm[m]) ** 2 for m in range(len(Pm))) for g in grid]
        th_est = float(grid[int(np.argmin(errs))])
        a_est = float(np.sin(th_est) ** 2)
        results[label] = {
            "a_true": round(a_true, 6), "theta_true": round(float(np.arcsin(np.sqrt(a_true))), 6),
            "P_good_m": [round(x, 6) for x in Pm],
            "theta_est": round(th_est, 6), "a_est": round(a_est, 6),
            "matches_true": abs(a_est - a_true) < 1e-3}
    return {"note": "OBSERVATION, NOT A SEAL — iterative/power QAE (QPE-free): sealed Grover powers "
                    "executed via backend_adapter (u_hash gated), P_good(m)=sin^2((2m+1)theta) fit "
                    "classically to estimate theta -> a. Handles GENERAL amplitudes (a=1/4, 1/8) that "
                    "small-t QPE-QAE cannot read exactly. Precision depends on the number of measurements.",
            "systems": results,
            "all_match": all(v["matches_true"] for v in results.values())}


def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 84)
    print("W9.3 QAEDeepening — 2nd QPE-QAE(a=1/2) + iterative QAE(QPE-free, 일반 θ). 신규 모듈 0.")
    print("=" * 84)

    apps = [
        _forge_app("qae3_pi2", _QAE3_PI2_SPEC),
        _forge_app("grover2_3iter", _grover_iter_spec("grover2_3iter", "grover2", 2, 3, 3)),
        _forge_app("grover3_3iter", _grover_iter_spec("grover3_3iter", "grover3", 3, 7, 3)),
    ]
    for a in apps:
        print(f"[App]    {a['id']:14} n_sys={a.get('n_sys')} sealed={a['sealed']} tier={a.get('tier')} "
              f"u={str(a.get('u_hash'))[:14]}" + ("" if a["sealed"] else f"  reason={a['reason']}"))

    qpe = _qpe_qae_observation()
    print(f"[QPE-QAE] a=1/2 readout: " + " · ".join(f"y={pk['y']}→a={pk['a_est']}" for pk in qpe["peaks"])
          + f"  exact={qpe['exact_recovery']}")

    itr = _iterative_qae_observation()
    print(f"[Iterative-QAE] QPE-free, backend_adapter 실행(봉인 Grover power):")
    for lbl, r in itr["systems"].items():
        print(f"   {lbl}: P_good(m=0..3)={r['P_good_m']} → 고전fit θ={r['theta_est']} "
              f"→ a_est={r['a_est']} (true {r['a_true']}) match={r['matches_true']}")
    print(f"   ★일반 θ: QPE bin 에 안 떨어지는 a=1/4·1/8 도 추정(QPE-QAE 불가능, iterative 가능)")

    report = {
        "phase": "W9.3 QAEDeepening",
        "honesty": "Grows QAE from instance to family with ZERO new modules. (1) A second exact "
                   "QPE-QAE instance qae3_pi2 (a=1/2). (2) Grover-power apps grover2/3_3iter extend the "
                   "iteration family. The amplitude-estimation behaviors are OBSERVATIONS, not seals: "
                   "QPE-QAE (one-shot, exact only for special amplitudes 2θ/2π=k/2^t) vs iterative/power "
                   "QAE (sealed Grover powers executed via backend_adapter, P_good(m)=sin^2((2m+1)θ) "
                   "fit classically — handles GENERAL amplitudes a=1/4, 1/8 that small-t QPE cannot read, "
                   "but precision depends on the number of measurements). apps 94->97, modules unchanged.",
        "apps": apps, "qpe_qae_observation": qpe, "iterative_qae_observation": itr,
    }
    all_ok = (all(a["sealed"] and a["tier"] == 0 for a in apps)
              and qpe["exact_recovery"] and itr["all_match"])
    report["all_ok"] = bool(all_ok)
    json.dump(report, open(os.path.join(OUT, "QAE2-FAMILY-REPORT.json"), "w",
                           encoding="utf-8"), ensure_ascii=False, indent=2)
    print("-" * 84)
    print(f"all_ok={all_ok}  →  .pgf/arith/QAE2-FAMILY-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
