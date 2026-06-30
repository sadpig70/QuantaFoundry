# -*- coding: utf-8 -*-
"""
vqe2_family.py — W10.2 VQEDeepening (MasterRoadmap › TrackSC)

2-layer hardware-efficient ansatz(per-qubit 독립각)를 고정-각 인스턴스로 봉인(Tier-0 EXACT,
신규 모듈 0 — 기존 Ry 복리). 변분 *깊이/표현력*으로 W10.1 경계 심화: backend_adapter 로
봉인 L2 인스턴스 실행→⟨H_TFIM2⟩ 관찰(seal 아님), 4-param sweep min → gap_L2≈0.002 << gap_L1=0.071.
★표현력(독립 파라미터)↑ → 변분 gap↓, 그러나 여전히 >0(변분≠exact 의 깊이 심화).

봉인 앱(전부 Tier-0 EXACT, 2q):
  vqe_he2_L2_pi4  = 2-layer 단일각(π/4×4)
  vqe_he2_L2_mix  = 2-layer 혼합각(π/4,π/2,−π/4,π/4) — ry_pi4/pi2/negpi4 복리

사용:  python scripts/vqe2_family.py
"""
from __future__ import annotations
import os, sys, json
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, ORACLE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import app_assemble as aa        # noqa: E402  (앱 봉인 — 사용만)
import backend_adapter as ba     # noqa: E402  (실행 계층 — 변분 에너지 관찰)

SPECS_APPS = os.path.join(ROOT, "specs", "apps")
APPREG = os.path.join(ROOT, "registry", "apps")
OUT = os.path.join(ROOT, ".pgf", "arith")

_I = np.eye(2, dtype=complex)
_X = np.array([[0, 1], [1, 0]], complex)
_Z = np.diag([1, -1]).astype(complex)
_CNOT = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], complex)

# 각도 → 봉인 Ry 모듈 id (전부 기존 봉인; 신규 모듈 0)
_ANG2MOD = {0.25: "ry_pi4", 0.5: "ry_pi2", 0.75: "ry_3pi4", -0.25: "ry_negpi4", -0.5: "ry_negpi2"}


def _ry(a):
    return np.array([[np.cos(a / 2), -np.sin(a / 2)], [np.sin(a / 2), np.cos(a / 2)]], complex)


def _kron(a, b):
    return np.kron(a, b)


def _l2_unitary(angs):
    a, b, c, d = [x * np.pi for x in angs]
    return _CNOT @ _kron(_ry(c), _ry(d)) @ _CNOT @ _kron(_ry(a), _ry(b))


def _he2_l2_spec(name, angs, desc):
    mods = [_ANG2MOD[x] for x in angs]   # [a,b,c,d]
    golden = (
        "import numpy as np\n"
        "def Ry(al): return np.array([[np.cos(al/2),-np.sin(al/2)],[np.sin(al/2),np.cos(al/2)]],dtype=complex)\n"
        "CNOT=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],dtype=complex)\n"
        "k=np.kron\n"
        f"a,b,c,d=[x*np.pi for x in {tuple(angs)}]\n"
        "golden=CNOT@k(Ry(c),Ry(d))@CNOT@k(Ry(a),Ry(b))\n")
    steps = [
        {"spec": f"../modules/{mods[0]}.pg", "targets": [0]},
        {"spec": f"../modules/{mods[1]}.pg", "targets": [1]},
        {"spec": "../modules/cnot.pg", "targets": [0, 1]},
        {"spec": f"../modules/{mods[2]}.pg", "targets": [0]},
        {"spec": f"../modules/{mods[3]}.pg", "targets": [1]},
        {"spec": "../modules/cnot.pg", "targets": [0, 1]},
    ]
    return (
        f"# {name} — {desc}. 2-layer HE ansatz(per-qubit 독립각)·기존 Ry 복리·MatrixGate 0.\n"
        '```json id=app_meta\n' + json.dumps({"id": name, "n_sys": 2, "n_anc": 0}) + "\n```\n"
        "```python id=app_golden\n" + golden + "```\n"
        '```json id=plan\n' + json.dumps({"steps": steps}) + "\n```\n")


def _forge_app(name, spec):
    sp = os.path.join(SPECS_APPS, f"{name}.app.pg")
    open(sp, "w", encoding="utf-8", newline="\n").write(spec)
    v = aa.assemble(sp, APPREG)
    return {"id": name, "n_sys": v.n_sys, "sealed": bool(v.sealed), "tier": v.tier,
            "u_hash": v.u_hash, "reason": v.reason}


def _h_tfim2():
    return -(_kron(_Z, _Z)) - (_kron(_X, _I) + _kron(_I, _X))


def _energy(U, H):
    z = np.zeros(U.shape[0], complex); z[0] = 1.0
    psi = U @ z
    return float((psi.conj() @ H @ psi).real)


def _depth_observation(sealed_insts):
    H = _h_tfim2(); Eg = float(np.linalg.eigvalsh(H)[0])
    # 봉인 L2 인스턴스 실행(u_hash 게이트)
    samples = []
    for app_id, angs in sealed_insts:
        app = ba.load_sealed_app(app_id)
        e = _energy(app["U"], H)
        samples.append({"app": app_id, "angles": list(angs), "energy": round(e, 6), "above_ground": e >= Eg - 1e-9})
    # gap_L1: 1-layer single-θ sweep
    g = np.linspace(0, np.pi, 600)
    e1 = [_energy(_CNOT @ _kron(_ry(t), _ry(t)), H) for t in g]
    gap1 = min(e1) - Eg
    # gap_L2: 4-param per-qubit grid
    rng = np.linspace(0, np.pi, 22)
    best = 1e9
    for a in rng:
        for b in rng:
            for c in rng:
                for d in rng:
                    e = _energy(_CNOT @ _kron(_ry(c), _ry(d)) @ _CNOT @ _kron(_ry(a), _ry(b)), H)
                    if e < best:
                        best = e
    gap2 = best - Eg
    return {
        "note": "OBSERVATION, NOT A SEAL — variational energy of sealed 2-layer ansatz via backend_adapter; "
                "depth/expressibility sweep. Variational principle <H> >= E_ground holds; richer (per-qubit "
                "independent) parameters shrink the gap (0.071 -> ~0.002, ~30x) but it stays > 0: VQE remains "
                "a bound, not exact (the depth-deepening of variational != exact).",
        "E_ground_exact": round(Eg, 6),
        "sealed_samples": samples,
        "gap_L1_single_theta": round(float(gap1), 6),
        "gap_L2_perqubit": round(float(gap2), 6),
        "gap_shrinks": gap2 < gap1 - 1e-3,
        "gap_L2_still_positive": gap2 > 1e-4,
        "variational_bound_holds": all(s["above_ground"] for s in samples),
    }


def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 84)
    print("W10.2 VQEDeepening — 2-layer per-qubit ansatz 봉인 + 깊이/표현력 gap 관찰(여전히 >0).")
    print("=" * 84)

    insts = [
        ("vqe_he2_L2_pi4", (0.25, 0.25, 0.25, 0.25), "2-layer 단일각 π/4"),
        ("vqe_he2_L2_mix", (0.25, 0.5, -0.25, 0.25), "2-layer 혼합각 (π/4,π/2,−π/4,π/4)"),
    ]
    apps = [_forge_app(n, _he2_l2_spec(n, a, d)) for n, a, d in insts]
    for a in apps:
        print(f"[App] {a['id']:16} n_sys={a.get('n_sys')} sealed={a['sealed']} tier={a.get('tier')} "
              f"u={str(a.get('u_hash'))[:14]}" + ("" if a["sealed"] else f"  reason={a['reason']}"))

    obs = _depth_observation([(n, a) for n, a, _ in insts])
    print(f"[Depth] TFIM2 Eg={obs['E_ground_exact']} | 봉인샘플 "
          + " · ".join(f"{s['app']}→E={s['energy']}" for s in obs["sealed_samples"]))
    print(f"        gap_L1(single-θ)={obs['gap_L1_single_theta']} → gap_L2(per-qubit)={obs['gap_L2_perqubit']} "
          f"(축소={obs['gap_shrinks']}, 여전히>0={obs['gap_L2_still_positive']})")

    all_ok = (all(a["sealed"] and a["tier"] == 0 for a in apps)
              and obs["gap_shrinks"] and obs["gap_L2_still_positive"] and obs["variational_bound_holds"])
    report = {"phase": "W10.2 VQEDeepening", "apps": apps, "depth_observation": obs, "all_ok": bool(all_ok),
              "honesty": "2-layer per-qubit ansatz sealed Tier-0 (zero new modules, reuses Ry). Depth/expressibility "
                         "observation (not a seal): richer parameters shrink the variational gap ~30x but it stays "
                         ">0 — variational != exact, deepened."}
    json.dump(report, open(os.path.join(OUT, "VQE2-FAMILY-REPORT.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("-" * 84)
    print(f"all_ok={all_ok}  →  .pgf/arith/VQE2-FAMILY-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
