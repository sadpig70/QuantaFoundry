# -*- coding: utf-8 -*-
"""
vqe_family.py — Stage 10 W10.1 VQEAnsatz

새 수평 클래스: 변분 양자 고유해법(VQE) hardware-efficient ansatz. ansatz *구조*를 고정-파라미터
인스턴스로 봉인(Tier-0 EXACT), 변분 *에너지* ⟨H(θ)⟩와 파라미터 최적화는 *관찰*(변분≠봉인).
Ry(W9.2)·CNOT 복리. 새 정직 경계: 변분 상한 ≠ exact 바닥에너지(approximation≠exact 의 자매).

봉인 대상(전부 Tier-0 EXACT):
 모듈: ry_3pi4 = Ry(3π/4) (landscape 샘플; YPowGate(0.75) up-to-phase).
 앱:
   vqe_he2_pi4 / vqe_he2_pi2 / vqe_he2_3pi4 (2q 1-layer = Ry(θ)^⊗2·CNOT, θ=π/4·π/2·3π/4).
   vqe_he3_pi4 (3q 1-layer = Ry(π/4)^⊗3 · CNOT(0,1)·CNOT(1,2)).

정직성 경계:
 - 봉인 = ansatz 회로(분해의 정확성). golden=closed-form, composite=봉인 Ry/CNOT(MatrixGate 0).
   봉인되는 건 ansatz 구조(고정 θ 인스턴스); 파라미터는 instance.
 - 봉인 아님 = 변분 에너지 ⟨H(θ)⟩(_variational_observation): backend_adapter 로 봉인 ansatz 실행
   (u_hash 게이트)→ψ=A|0>→⟨H⟩=ψ†Hψ. 변분원리 ⟨H⟩≥E_ground(상한). 연속 sweep min→E_ground
   접근하나 ansatz-limited gap>0(exact 미도달). VQE 는 근사/상한이지 exact 아님.
 - ry_3pi4 1개만 신규 모듈(second_oracle 61→62).

사용:  python scripts/vqe_family.py
"""
from __future__ import annotations

import os
import sys
import json
import subprocess

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, ORACLE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import verify_seal as vs        # noqa: E402  (모듈 봉인 — 사용만)
import app_assemble as aa       # noqa: E402  (앱 봉인 — 사용만)
import backend_adapter as ba    # noqa: E402  (실행 계층 — 사용만, 변분 에너지 관찰)

SPECS_MODS = os.path.join(ROOT, "specs", "modules")
SPECS_APPS = os.path.join(ROOT, "specs", "apps")
MODREG = os.path.join(ROOT, "registry", "modules")
APPREG = os.path.join(ROOT, "registry", "apps")
OUT = os.path.join(ROOT, ".pgf", "arith")

_I2 = np.eye(2, dtype=complex)
_X = np.array([[0, 1], [1, 0]], complex)
_Z = np.diag([1, -1]).astype(complex)


def _ry(a):
    return np.array([[np.cos(a / 2), -np.sin(a / 2)], [np.sin(a / 2), np.cos(a / 2)]], dtype=complex)


# ── 모듈 spec: Ry(3π/4) ─────────────────────────────────────────────────────────
_RY3PI4_SPEC = (
    "# ry_3pi4 — Ry(3π/4) (VQE ansatz 각도 샘플; 변분 landscape min 너머 포착). "
    "Ry(α)=YPowGate(exponent=α/π) up-to-phase(C4). analytic golden.\n"
    "```python id=bloq\n"
    "import numpy as np\n"
    "from qualtran.bloqs.basic_gates import YPowGate\n"
    "bloq = YPowGate(exponent=0.75)\n"
    "```\n"
    "```python id=golden\n"
    "import numpy as np\n"
    "a = 3*np.pi/4\n"
    "golden = np.array([[np.cos(a/2), -np.sin(a/2)], [np.sin(a/2), np.cos(a/2)]], dtype=complex)\n"
    "```\n"
    '```json id=meta\n'
    '{"id": "ry_3pi4", "n_sys": 1, "n_anc": 0}\n'
    "```\n")


def _seal_module(name, spec):
    sp = os.path.join(SPECS_MODS, f"{name}.pg")
    open(sp, "w", encoding="utf-8", newline="\n").write(spec)
    rc = subprocess.run([sys.executable, os.path.join(ORACLE, "verify_seal.py"), sp, "--out", MODREG],
                        capture_output=True, text=True, cwd=ORACLE).returncode
    p = os.path.join(MODREG, f"{name}.sealed.json")
    if rc != 0 or not os.path.exists(p):
        return {"id": name, "sealed": False}
    sealed = json.load(open(p, encoding="utf-8"))
    return {"id": name, "n_sys": sealed["n_sys"], "sealed": True,
            "tier": sealed.get("tier", 0), "u_hash": sealed["u_hash"]}


# ── 앱 spec: hardware-efficient ansatz (Ry layer + CNOT ladder) ──────────────────
def _he_spec(name, n, ry_mod, ang_expr, desc):
    golden = (
        "import numpy as np\n"
        f"n={n}\n"
        "def Ry(al): return np.array([[np.cos(al/2),-np.sin(al/2)],[np.sin(al/2),np.cos(al/2)]],dtype=complex)\n"
        "CNOT=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],dtype=complex)\n"
        "def emb(g,qs):\n"
        "    k=len(qs); G=g.reshape([2]*k+[2]*k)\n"
        "    T=np.eye(1<<n,dtype=complex).reshape([2]*n+[1<<n])\n"
        "    T=np.tensordot(G,T,axes=(list(range(k,2*k)),qs)); T=np.moveaxis(T,list(range(k)),qs)\n"
        "    return T.reshape(1<<n,1<<n)\n"
        f"th={ang_expr}\n"
        "U=np.eye(1<<n,dtype=complex)\n"
        "for q in range(n): U=emb(Ry(th),[q])@U\n"
        "for q in range(n-1): U=emb(CNOT,[q,q+1])@U\n"
        "golden=U\n")
    steps = [{"spec": f"../modules/{ry_mod}.pg", "targets": [q]} for q in range(n)]
    steps += [{"spec": "../modules/cnot.pg", "targets": [q, q + 1]} for q in range(n - 1)]
    return (
        f"# {name} — {desc}. 1-layer HE ansatz = Ry(θ)^⊗{n}·CNOT ladder. plan=봉인 {ry_mod}·cnot, no MatrixGate.\n"
        '```json id=app_meta\n'
        + json.dumps({"id": name, "n_sys": n, "n_anc": 0}) + "\n"
        "```\n"
        "```python id=app_golden\n"
        + golden
        + "```\n"
        '```json id=plan\n'
        + json.dumps({"steps": steps}) + "\n"
        "```\n")


def _forge_app(name, spec):
    sp = os.path.join(SPECS_APPS, f"{name}.app.pg")
    open(sp, "w", encoding="utf-8", newline="\n").write(spec)
    v = aa.assemble(sp, APPREG)
    return {"id": name, "n_sys": v.n_sys, "sealed": bool(v.sealed), "tier": v.tier,
            "u_hash": v.u_hash, "reason": v.reason}


# ── H_TFIM = -(Σ ZZ) - (Σ X) ────────────────────────────────────────────────────
def _h_tfim(n):
    def opn(ps):
        m = np.array([[1]], dtype=complex)
        for q in range(n):
            m = np.kron(m, ps.get(q, _I2))
        return m
    return -sum(opn({i: _Z, i + 1: _Z}) for i in range(n - 1)) - sum(opn({i: _X}) for i in range(n))


# ── 정직-변분 관찰 (seal 아님): ⟨H(θ)⟩ 변분 에너지 ──────────────────────────────
def _ansatz_U(n, th):
    CNOT = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex)

    def emb(g, qs):
        k = len(qs)
        G = g.reshape([2] * k + [2] * k)
        T = np.eye(1 << n, dtype=complex).reshape([2] * n + [1 << n])
        T = np.tensordot(G, T, axes=(list(range(k, 2 * k)), qs))
        T = np.moveaxis(T, list(range(k)), qs)
        return T.reshape(1 << n, 1 << n)
    U = np.eye(1 << n, dtype=complex)
    for q in range(n):
        U = emb(_ry(th), [q]) @ U
    for q in range(n - 1):
        U = emb(CNOT, [q, q + 1]) @ U
    return U


def _energy(U, H):
    psi = U @ np.eye(U.shape[0], dtype=complex)[:, 0]
    return float((psi.conj() @ H @ psi).real)


def _variational_observation():
    out = {"note": "OBSERVATION, NOT A SEAL — variational energy <H(θ)> of the sealed ansatz "
                   "executed via backend_adapter. Variational principle: <H> >= E_ground (upper "
                   "bound). A continuous sweep approaches E_ground but an ansatz-limited gap>0 "
                   "remains: VQE is an approximation/bound, not the exact ground (variational != exact).",
           "hamiltonian": "H_TFIM = -(sum ZZ) - (sum X)", "systems": {}}
    # n=2: 봉인 3샘플 (backend_adapter 실행, u_hash 게이트) + 연속 sweep
    sealed_pts = {2: [("vqe_he2_pi4", np.pi / 4), ("vqe_he2_pi2", np.pi / 2), ("vqe_he2_3pi4", 3 * np.pi / 4)],
                  3: [("vqe_he3_pi4", np.pi / 4)]}
    for n in (2, 3):
        H = _h_tfim(n)
        Eg = float(np.linalg.eigvalsh(H)[0])
        samples = []
        for app_id, th in sealed_pts[n]:
            app = ba.load_sealed_app(app_id)        # u_hash 게이트 — 봉인된 그 ansatz 실행
            e = _energy(app["U"], H)
            samples.append({"app": app_id, "theta": round(float(th), 6),
                            "energy": round(e, 6), "above_ground": e >= Eg - 1e-9})
        grid = np.linspace(0, np.pi, 2000)
        es = [_energy(_ansatz_U(n, t), H) for t in grid]
        imin = int(np.argmin(es))
        out["systems"][f"tfim{n}"] = {
            "E_ground_exact": round(Eg, 6),
            "sealed_samples": samples,
            "sweep_min_energy": round(float(es[imin]), 6),
            "sweep_min_theta": round(float(grid[imin]), 6),
            "ansatz_gap": round(float(es[imin] - Eg), 6),
            "variational_bound_holds": all(s["above_ground"] for s in samples) and es[imin] >= Eg - 1e-9,
            "gap_positive_honest": float(es[imin] - Eg) > 1e-4}
    out["all_ok"] = all(s["variational_bound_holds"] and s["gap_positive_honest"]
                        for s in out["systems"].values())
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 84)
    print("W10.1 VQEAnsatz — 변분 회로(hardware-efficient ansatz) 봉인 + 변분 에너지 관찰(상한≠exact).")
    print("=" * 84)

    mods = [_seal_module("ry_3pi4", _RY3PI4_SPEC)]
    for m in mods:
        print(f"[Module] {m['id']:10} n_sys={m.get('n_sys')} sealed={m['sealed']} tier={m.get('tier')} "
              f"u={str(m.get('u_hash'))[:14]}")

    apps = [
        _forge_app("vqe_he2_pi4", _he_spec("vqe_he2_pi4", 2, "ry_pi4", "np.pi/4", "2q 1-layer θ=π/4")),
        _forge_app("vqe_he2_pi2", _he_spec("vqe_he2_pi2", 2, "ry_pi2", "np.pi/2", "2q 1-layer θ=π/2")),
        _forge_app("vqe_he2_3pi4", _he_spec("vqe_he2_3pi4", 2, "ry_3pi4", "3*np.pi/4", "2q 1-layer θ=3π/4")),
        _forge_app("vqe_he3_pi4", _he_spec("vqe_he3_pi4", 3, "ry_pi4", "np.pi/4", "3q 1-layer θ=π/4")),
    ]
    for a in apps:
        print(f"[App]    {a['id']:14} n_sys={a.get('n_sys')} sealed={a['sealed']} tier={a.get('tier')} "
              f"u={str(a.get('u_hash'))[:14]}" + ("" if a["sealed"] else f"  reason={a['reason']}"))

    obs = _variational_observation()
    print(f"[Variational] H_TFIM 변분 에너지(seal 아님, ⟨H⟩≥E_ground 상한):")
    for nk, sd in obs["systems"].items():
        print(f"   {nk}: E_ground={sd['E_ground_exact']} | 봉인샘플 " +
              " · ".join(f"θ={s['theta']:.3f}→E={s['energy']}" for s in sd["sealed_samples"]))
        print(f"        sweep min E={sd['sweep_min_energy']} @θ={sd['sweep_min_theta']} "
              f"gap={sd['ansatz_gap']} (변분상한 holds={sd['variational_bound_holds']}, gap>0={sd['gap_positive_honest']})")

    report = {
        "phase": "W10.1 VQEAnsatz",
        "honesty": "New horizontal class: variational quantum eigensolver (VQE) hardware-efficient "
                   "ansatz. The ansatz STRUCTURE is sealed Tier-0 EXACT at fixed-parameter instances "
                   "(Ry layer + CNOT ladder; composite==golden, no MatrixGate; reuses ry_pi4/pi2/3pi4 + "
                   "cnot). The variational ENERGY <H(θ)> and parameter optimization are OBSERVATIONS, "
                   "NOT seals: <H> executed via backend_adapter obeys the variational principle "
                   "<H> >= E_ground (upper bound); a continuous sweep approaches E_ground but an "
                   "ansatz-limited gap>0 remains (variational bound != exact ground — the variational "
                   "sibling of approximation != exact). modules 67->68, apps 97->101.",
        "modules": mods, "apps": apps, "variational_observation": obs,
    }
    all_ok = (all(m["sealed"] and m.get("tier", 0) == 0 for m in mods)
              and all(a["sealed"] and a["tier"] == 0 for a in apps)
              and obs["all_ok"])
    report["all_ok"] = bool(all_ok)
    json.dump(report, open(os.path.join(OUT, "VQE-FAMILY-REPORT.json"), "w",
                           encoding="utf-8"), ensure_ascii=False, indent=2)
    print("-" * 84)
    print(f"all_ok={all_ok}  →  .pgf/arith/VQE-FAMILY-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
