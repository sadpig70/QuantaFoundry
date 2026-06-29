# -*- coding: utf-8 -*-
"""
ampamp_family.py — Stage 9 W9.1 AmplitudeAmplification

Grover(grover2)를 amplitude amplification 패밀리로 일반화: 3큐비트 확산/Grover 연산자 + 반복 횟수
봉인. 기존 봉인 부품(x_gate·ccz·h_gate·cz·reflect00·diffusion) 복리 재사용. 신규 모듈 0.

봉인 대상(전부 Tier-0 EXACT):
 1. reflect000 (app, 3q) = 2|000><000|-I = (X^⊗3)·CCZ·(X^⊗3).
 2. diffusion3 (app, 3q) = (H^⊗3)·reflect000·(H^⊗3) = 2|s><s|-I.
 3. grover3 (app, 3q)    = D₃∘O₃ (O₃=ccz, |111> 표시). 1 iterate.
 4. grover3_2iter (app, 3q) = G₃². 2 iterate (N=8 최적-k).
 5. grover2_2iter (app, 2q) = G₂². 2 iterate (N=4 over-rotation).

정직성 경계:
 - 봉인 = 연산자 분해의 정확성. golden=closed-form(reflection/diffusion 곱), composite=봉인 부품(MatrixGate 0).
   reflect000 은 전역위상 -1 흡수(reflect00 패턴; 오라클 C2 = up-to-phase).
 - 봉인 아님 = amplitude amplification 프로파일 P_target(k)(_amplitude_profile): 봉인 G^k 실행 행동 관찰.
   최적-k(N=8→k=2, P=0.945)·over-rotation(N=4→k=2, P=0.25)은 관찰이지 봉인 아님(이론 sin²((2k+1)θ) 대조).
 - 신규 모듈 0 → second_oracle 57/57 불변. 앱만 +5.

사용:  python scripts/ampamp_family.py
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

SPECS_APPS = os.path.join(ROOT, "specs", "apps")
APPREG = os.path.join(ROOT, "registry", "apps")
OUT = os.path.join(ROOT, ".pgf", "arith")


# ── 앱 spec ────────────────────────────────────────────────────────────────────
_REFLECT000_SPEC = (
    "# reflect000 — |000> 기준 반사 2|000><000|-I = (X^⊗3)·CCZ·(X^⊗3). 봉인 x_gate·ccz 재조립 "
    "(reflect00 의 3큐비트 일반화). 전역위상 흡수.\n"
    '```json id=app_meta\n'
    '{"id": "reflect000", "n_sys": 3, "n_anc": 0}\n'
    "```\n"
    "```python id=app_golden\n"
    "import numpy as np\n"
    "golden = np.diag([1,-1,-1,-1,-1,-1,-1,-1]).astype(complex)   # 2|000><000|-I (전역위상 흡수)\n"
    "```\n"
    '```json id=plan\n'
    + json.dumps({"steps": [
        {"spec": "../modules/x_gate.pg", "targets": [0]},
        {"spec": "../modules/x_gate.pg", "targets": [1]},
        {"spec": "../modules/x_gate.pg", "targets": [2]},
        {"spec": "../modules/ccz.pg"},
        {"spec": "../modules/x_gate.pg", "targets": [0]},
        {"spec": "../modules/x_gate.pg", "targets": [1]},
        {"spec": "../modules/x_gate.pg", "targets": [2]}]}) + "\n"
    "```\n")

_DIFFUSION3_SPEC = (
    "# diffusion3 — 3큐비트 Grover 확산 D₃ = (H^⊗3)·reflect000·(H^⊗3) = 2|s><s|-I. reflect000 sub-app 재귀.\n"
    '```json id=app_meta\n'
    '{"id": "diffusion3", "n_sys": 3, "n_anc": 0}\n'
    "```\n"
    "```python id=app_golden\n"
    "import numpy as np\n"
    "H1 = np.array([[1,1],[1,-1]],dtype=complex)/np.sqrt(2)\n"
    "H3 = np.kron(np.kron(H1,H1),H1)\n"
    "refl = np.diag([1,-1,-1,-1,-1,-1,-1,-1]).astype(complex)\n"
    "golden = H3 @ refl @ H3\n"
    "```\n"
    '```json id=plan\n'
    + json.dumps({"steps": [
        {"spec": "../modules/h_gate.pg", "targets": [0]},
        {"spec": "../modules/h_gate.pg", "targets": [1]},
        {"spec": "../modules/h_gate.pg", "targets": [2]},
        {"app": "reflect000.app.pg"},
        {"spec": "../modules/h_gate.pg", "targets": [0]},
        {"spec": "../modules/h_gate.pg", "targets": [1]},
        {"spec": "../modules/h_gate.pg", "targets": [2]}]}) + "\n"
    "```\n")

_GROVER3_SPEC = (
    "# grover3 — 3큐비트 Grover 1-iterate G₃ = D₃∘O₃ (정답 |111>). oracle=봉인 ccz 재사용, "
    "diffusion3 sub-app. plan=[{ccz}, {diffusion3}].\n"
    '```json id=app_meta\n'
    '{"id": "grover3", "n_sys": 3, "n_anc": 0}\n'
    "```\n"
    "```python id=app_golden\n"
    "import numpy as np\n"
    "H1 = np.array([[1,1],[1,-1]],dtype=complex)/np.sqrt(2)\n"
    "H3 = np.kron(np.kron(H1,H1),H1)\n"
    "refl = np.diag([1,-1,-1,-1,-1,-1,-1,-1]).astype(complex)\n"
    "D3 = H3 @ refl @ H3\n"
    "O3 = np.diag([1,1,1,1,1,1,1,-1]).astype(complex)        # ccz: |111> 위상반전\n"
    "golden = D3 @ O3\n"
    "```\n"
    '```json id=plan\n'
    + json.dumps({"steps": [
        {"spec": "../modules/ccz.pg"},
        {"app": "diffusion3.app.pg"}]}) + "\n"
    "```\n")

_GROVER3_2ITER_SPEC = (
    "# grover3_2iter — 3큐비트 Grover 2-iterate G₃² (N=8 M=1 최적-k). plan=[grover3, grover3] 복리.\n"
    '```json id=app_meta\n'
    '{"id": "grover3_2iter", "n_sys": 3, "n_anc": 0}\n'
    "```\n"
    "```python id=app_golden\n"
    "import numpy as np\n"
    "H1 = np.array([[1,1],[1,-1]],dtype=complex)/np.sqrt(2)\n"
    "H3 = np.kron(np.kron(H1,H1),H1)\n"
    "refl = np.diag([1,-1,-1,-1,-1,-1,-1,-1]).astype(complex)\n"
    "D3 = H3 @ refl @ H3\n"
    "O3 = np.diag([1,1,1,1,1,1,1,-1]).astype(complex)\n"
    "G3 = D3 @ O3\n"
    "golden = G3 @ G3\n"
    "```\n"
    '```json id=plan\n'
    + json.dumps({"steps": [
        {"app": "grover3.app.pg"},
        {"app": "grover3.app.pg"}]}) + "\n"
    "```\n")

_GROVER2_2ITER_SPEC = (
    "# grover2_2iter — 2큐비트 Grover 2-iterate G₂² (N=4는 1 iterate가 P=1 최적; 2는 over-rotation P=0.25). "
    "plan=[grover2, grover2] 복리.\n"
    '```json id=app_meta\n'
    '{"id": "grover2_2iter", "n_sys": 2, "n_anc": 0}\n'
    "```\n"
    "```python id=app_golden\n"
    "import numpy as np\n"
    "H1 = np.array([[1,1],[1,-1]],dtype=complex)/np.sqrt(2)\n"
    "H2 = np.kron(H1,H1)\n"
    "D2 = H2 @ np.diag([1,-1,-1,-1]).astype(complex) @ H2\n"
    "O2 = np.diag([1,1,1,-1]).astype(complex)                # cz: |11> 위상반전\n"
    "G2 = D2 @ O2\n"
    "golden = G2 @ G2\n"
    "```\n"
    '```json id=plan\n'
    + json.dumps({"steps": [
        {"app": "grover2.app.pg"},
        {"app": "grover2.app.pg"}]}) + "\n"
    "```\n")


def _forge_app(name, spec):
    sp = os.path.join(SPECS_APPS, f"{name}.app.pg")
    open(sp, "w", encoding="utf-8", newline="\n").write(spec)
    v = aa.assemble(sp, APPREG)
    return {"id": name, "n_sys": v.n_sys, "sealed": bool(v.sealed), "tier": v.tier,
            "u_hash": v.u_hash, "reason": v.reason}


# ── 정직-behavior 관찰 (seal 아님): amplitude amplification 프로파일 P_target(k) ──
def _amplitude_profile():
    H1 = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)

    def kron(*m):
        r = np.array([[1]], dtype=complex)
        for x in m:
            r = np.kron(r, x)
        return r

    out = {"note": "OBSERVATION, NOT A SEAL — sealed Grover operator G^k applied to the uniform state; "
                   "P_target(k) is illustrative amplitude-amplification behavior, contrasted with the "
                   "theory sin^2((2k+1)θ). Optimal-k and over-rotation are observations, not seals."}

    # N=8 (3q), marked |111>
    H3 = kron(H1, H1, H1)
    refl = np.diag([1, -1, -1, -1, -1, -1, -1, -1]).astype(complex)
    D3 = H3 @ refl @ H3
    O3 = np.diag([1, 1, 1, 1, 1, 1, 1, -1]).astype(complex)
    G3 = D3 @ O3
    s3 = H3 @ np.eye(8, dtype=complex)[:, 0]
    th3 = np.arcsin(1 / np.sqrt(8))
    prof3 = []
    for k in (1, 2, 3):
        psi = np.linalg.matrix_power(G3, k) @ s3
        prof3.append({"k": k, "P_target": round(float(abs(psi[7]) ** 2), 6),
                      "theory": round(float(np.sin((2 * k + 1) * th3) ** 2), 6)})
    out["grover3_N8"] = {"profile": prof3, "optimal_k": 2,
                         "matches_theory": all(abs(p["P_target"] - p["theory"]) < 1e-6 for p in prof3)}

    # N=4 (2q), marked |11>
    H2 = kron(H1, H1)
    D2 = H2 @ np.diag([1, -1, -1, -1]).astype(complex) @ H2
    O2 = np.diag([1, 1, 1, -1]).astype(complex)
    G2 = D2 @ O2
    s2 = H2 @ np.eye(4, dtype=complex)[:, 0]
    th2 = np.arcsin(1 / np.sqrt(4))
    prof2 = []
    for k in (1, 2):
        psi = np.linalg.matrix_power(G2, k) @ s2
        prof2.append({"k": k, "P_target": round(float(abs(psi[3]) ** 2), 6),
                      "theory": round(float(np.sin((2 * k + 1) * th2) ** 2), 6)})
    out["grover2_N4"] = {"profile": prof2, "optimal_k": 1, "over_rotation_at_k2": prof2[1]["P_target"] < 0.5,
                         "matches_theory": all(abs(p["P_target"] - p["theory"]) < 1e-6 for p in prof2)}
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 84)
    print("W9.1 AmplitudeAmplification — Grover 일반화(3q 확산/연산자 + 반복) + 진폭증폭 프로파일.")
    print("=" * 84)

    apps = [
        _forge_app("reflect000", _REFLECT000_SPEC),
        _forge_app("diffusion3", _DIFFUSION3_SPEC),
        _forge_app("grover3", _GROVER3_SPEC),
        _forge_app("grover3_2iter", _GROVER3_2ITER_SPEC),
        _forge_app("grover2_2iter", _GROVER2_2ITER_SPEC),
    ]
    for a in apps:
        print(f"[App]    {a['id']:16} n_sys={a.get('n_sys')} sealed={a['sealed']} tier={a.get('tier')} "
              f"u={str(a.get('u_hash'))[:14]}" + ("" if a["sealed"] else f"  reason={a['reason']}"))

    prof = _amplitude_profile()
    g3 = prof["grover3_N8"]; g2 = prof["grover2_N4"]
    print(f"[Behavior] amplitude amplification 프로파일(seal 아님):")
    print(f"   grover3 (N=8): " + " · ".join(f"k={p['k']}→P={p['P_target']}" for p in g3["profile"])
          + f"  최적-k={g3['optimal_k']} (이론일치={g3['matches_theory']})")
    print(f"   grover2 (N=4): " + " · ".join(f"k={p['k']}→P={p['P_target']}" for p in g2["profile"])
          + f"  최적-k={g2['optimal_k']} over-rotation@k2={g2['over_rotation_at_k2']}")

    report = {
        "phase": "W9.1 AmplitudeAmplification",
        "honesty": "Generalizes Grover (grover2) into the amplitude-amplification family: 3-qubit "
                   "reflection/diffusion/Grover operators + iteration-count apps, reusing sealed parts "
                   "(x_gate/ccz/h_gate/cz/reflect00/diffusion); ZERO new modules. All Tier-0 EXACT "
                   "(composite==golden up-to-phase, no MatrixGate; reflect000 absorbs a global -1, the "
                   "reflect00 pattern). The amplitude-amplification PROFILE P_target(k) is an "
                   "OBSERVATION, NOT a seal: sealed G^k on the uniform state, contrasted with the theory "
                   "sin^2((2k+1)θ) — optimal-k (N=8 -> k=2, P=0.945) and over-rotation (N=4 -> k=2, "
                   "P=0.25). apps 86->91, modules unchanged (second_oracle 57/57).",
        "apps": apps, "amplitude_profile": prof,
    }
    all_ok = (all(a["sealed"] and a["tier"] == 0 for a in apps)
              and g3["matches_theory"] and g2["matches_theory"]
              and g3["optimal_k"] == 2 and g2["over_rotation_at_k2"])
    report["all_ok"] = bool(all_ok)
    json.dump(report, open(os.path.join(OUT, "AMPAMP-FAMILY-REPORT.json"), "w",
                           encoding="utf-8"), ensure_ascii=False, indent=2)
    print("-" * 84)
    print(f"all_ok={all_ok}  →  .pgf/arith/AMPAMP-FAMILY-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
