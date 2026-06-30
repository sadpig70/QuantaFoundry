# -*- coding: utf-8 -*-
"""
qaoa_family.py — W11.1 QAOA (MasterRoadmap › TrackSC)

변분의 조합최적화 자매(새 수평 클래스): MaxCut QAOA p=1 회로를 고정-각 인스턴스로 봉인
(Tier-0 EXACT, 신규 모듈 0 — cost=cnot·rz_negpi4·cnot, mixer=rx_negpi4, H=h_gate 전부 W8 복리).
근사비 = backend_adapter 관찰(seal 아님). ★p=1 유한층 → 최적각에서도 ratio<1
(P3 0.825·C4 0.75): QAOA 는 근사이지 exact 아님(approximation≠exact 의 조합최적화 형제).

봉인 앱(전부 Tier-0 EXACT, 고정각 γ=π/4·β=−π/8):
  qaoa_p3 = path P3 (n=3, edges 01·12)
  qaoa_c4 = cycle C4 (n=4, edges 01·12·23·03)

사용:  python scripts/qaoa_family.py
"""
from __future__ import annotations
import os, sys, json
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, ORACLE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import app_assemble as aa        # noqa: E402
import backend_adapter as ba     # noqa: E402

SPECS_APPS = os.path.join(ROOT, "specs", "apps")
APPREG = os.path.join(ROOT, "registry", "apps")
OUT = os.path.join(ROOT, ".pgf", "arith")

_Z = np.diag([1, -1]).astype(complex)
_H = np.array([[1, 1], [1, -1]], complex) / np.sqrt(2)
_CNOT = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], complex)
_GAMMA = np.pi / 4      # cost: rz_negpi4 → e^{i(π/8)ZZ}  (γ/2=π/8)
_BETA = -np.pi / 8      # mixer: rx_negpi4 = Rx(-π/4)=e^{i(π/8)X} = e^{-iβX}, β=-π/8


def _rz(a):
    return np.array([[np.exp(-1j * a / 2), 0], [0, np.exp(1j * a / 2)]], complex)


def _rx(a):
    return np.array([[np.cos(a / 2), -1j * np.sin(a / 2)], [-1j * np.sin(a / 2), np.cos(a / 2)]], complex)


def _emb(g, qs, n):
    k = len(qs); G = g.reshape([2] * k + [2] * k)
    T = np.eye(1 << n, dtype=complex).reshape([2] * n + [1 << n])
    T = np.tensordot(G, T, axes=(list(range(k, 2 * k)), qs)); T = np.moveaxis(T, list(range(k)), qs)
    return T.reshape(1 << n, 1 << n)


def _qaoa_spec(name, n, edges, desc):
    golden = (
        "import numpy as np\n"
        "Z=np.diag([1,-1]).astype(complex); H=np.array([[1,1],[1,-1]],dtype=complex)/np.sqrt(2)\n"
        "CNOT=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],dtype=complex)\n"
        "def Rz(a): return np.array([[np.exp(-1j*a/2),0],[0,np.exp(1j*a/2)]],dtype=complex)\n"
        "def Rx(a): return np.array([[np.cos(a/2),-1j*np.sin(a/2)],[-1j*np.sin(a/2),np.cos(a/2)]],dtype=complex)\n"
        "def emb(g,qs):\n"
        f"    n={n}\n"
        "    k=len(qs); G=g.reshape([2]*k+[2]*k)\n"
        "    T=np.eye(1<<n,dtype=complex).reshape([2]*n+[1<<n])\n"
        "    T=np.tensordot(G,T,axes=(list(range(k,2*k)),qs)); T=np.moveaxis(T,list(range(k)),qs)\n"
        "    return T.reshape(1<<n,1<<n)\n"
        f"n={n}; edges={list(map(list, edges))}; g=np.pi/4\n"
        "U=np.eye(1<<n,dtype=complex)\n"
        "for q in range(n): U=emb(H,[q])@U\n"
        "for (i,j) in edges:\n"
        "    C2=emb(CNOT,[i,j]); U=C2@emb(Rz(-g),[j])@C2@U\n"
        "for q in range(n): U=emb(Rx(-np.pi/4),[q])@U\n"
        "golden=U\n")
    steps = [{"spec": "../modules/h_gate.pg", "targets": [q]} for q in range(n)]
    for (i, j) in edges:
        steps += [
            {"spec": "../modules/cnot.pg", "targets": [i, j]},
            {"spec": "../modules/rz_negpi4.pg", "targets": [j]},
            {"spec": "../modules/cnot.pg", "targets": [i, j]},
        ]
    steps += [{"spec": "../modules/rx_negpi4.pg", "targets": [q]} for q in range(n)]
    return (
        f"# {name} — {desc}. QAOA p=1 MaxCut, 고정각 γ=π/4·β=−π/8. cost=cnot·rz_negpi4·cnot·mixer=rx_negpi4·H. MatrixGate 0.\n"
        '```json id=app_meta\n' + json.dumps({"id": name, "n_sys": n, "n_anc": 0}) + "\n```\n"
        "```python id=app_golden\n" + golden + "```\n"
        '```json id=plan\n' + json.dumps({"steps": steps}) + "\n```\n")


def _forge_app(name, spec):
    sp = os.path.join(SPECS_APPS, f"{name}.app.pg")
    open(sp, "w", encoding="utf-8", newline="\n").write(spec)
    v = aa.assemble(sp, APPREG)
    return {"id": name, "n_sys": v.n_sys, "sealed": bool(v.sealed), "tier": v.tier,
            "u_hash": v.u_hash, "reason": v.reason}


def _cost_op(n, edges):
    C = np.zeros((1 << n, 1 << n), complex)
    for (i, j) in edges:
        C += 0.5 * (np.eye(1 << n, dtype=complex) - _emb(_Z, [i], n) @ _emb(_Z, [j], n))
    return C


def _cmax(n, edges):
    best = 0
    for x in range(1 << n):
        bits = [(x >> q) & 1 for q in range(n)]
        best = max(best, sum(1 for (i, j) in edges if bits[i] != bits[j]))
    return best


def _qaoa_U(n, edges, g, b):
    U = np.eye(1 << n, dtype=complex)
    for q in range(n):
        U = _emb(_H, [q], n) @ U
    for (i, j) in edges:
        C2 = _emb(_CNOT, [i, j], n)
        U = C2 @ _emb(_rz(-g), [j], n) @ C2 @ U
    for q in range(n):
        U = _emb(_rx(2 * b), [q], n) @ U
    return U


def _expC(U, C):
    z = np.zeros(U.shape[0], complex); z[0] = 1.0
    psi = U @ z
    return float((psi.conj() @ C @ psi).real)


def _qaoa_observation(insts):
    out = {"note": "OBSERVATION, NOT A SEAL — MaxCut <C> of the sealed QAOA circuit via backend_adapter, "
                   "plus the p=1-optimal approximation ratio over (γ,β). p=1 is a finite-layer approximation: "
                   "even at optimal angles ratio<1 (P3 0.825, C4 0.75) — QAOA != exact (the combinatorial "
                   "sibling of approximation != exact / variational bound != exact).",
           "instances": []}
    ok = True
    for app_id, n, edges in insts:
        C = _cost_op(n, edges); Cmax = _cmax(n, edges)
        app = ba.load_sealed_app(app_id)            # u_hash 게이트 — 봉인된 그 회로 실행
        sealed_exp = _expC(app["U"], C)
        # p1-optimal sweep
        best = -1.0
        for g in np.linspace(0, 2 * np.pi, 90):
            for b in np.linspace(0, np.pi, 90):
                v = _expC(_qaoa_U(n, edges, g, b), C)
                if v > best:
                    best = v
        rec = {"app": app_id, "n": n, "edges": len(edges), "Cmax": Cmax,
               "sealed_expC": round(sealed_exp, 6), "sealed_ratio": round(sealed_exp / Cmax, 6),
               "p1_opt_expC": round(float(best), 6), "p1_opt_ratio": round(float(best) / Cmax, 6),
               "sealed_in_range": 0 - 1e-9 <= sealed_exp <= Cmax + 1e-9,
               "p1_opt_below_1": best / Cmax < 1 - 1e-3}
        ok = ok and rec["sealed_in_range"] and rec["p1_opt_below_1"]
        out["instances"].append(rec)
    out["all_ok"] = ok
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 84)
    print("W11.1 QAOA — MaxCut p=1 회로 봉인 + 근사비 관찰(p=1 최적각에서도 ratio<1).")
    print("=" * 84)
    insts = [("qaoa_p3", 3, [(0, 1), (1, 2)], "path P3"),
             ("qaoa_c4", 4, [(0, 1), (1, 2), (2, 3), (0, 3)], "cycle C4")]
    apps = [_forge_app(n, _qaoa_spec(n, nn, e, d)) for n, nn, e, d in insts]
    for a in apps:
        print(f"[App] {a['id']:10} n_sys={a.get('n_sys')} sealed={a['sealed']} tier={a.get('tier')} "
              f"u={str(a.get('u_hash'))[:14]}" + ("" if a["sealed"] else f"  reason={a['reason']}"))
    obs = _qaoa_observation([(n, nn, e) for n, nn, e, _ in insts])
    for r in obs["instances"]:
        print(f"[Approx] {r['app']}: Cmax={r['Cmax']} sealed⟨C⟩={r['sealed_expC']}(r={r['sealed_ratio']}) "
              f"| p1-opt ⟨C⟩={r['p1_opt_expC']} ratio={r['p1_opt_ratio']} (<1={r['p1_opt_below_1']})")
    all_ok = all(a["sealed"] and a["tier"] == 0 for a in apps) and obs["all_ok"]
    report = {"phase": "W11.1 QAOA", "apps": apps, "qaoa_observation": obs, "all_ok": bool(all_ok),
              "honesty": "MaxCut QAOA p=1 circuit sealed Tier-0 (zero new modules, reuses cnot/rz_negpi4/"
                         "rx_negpi4/h_gate). Approximation ratio is an observation (not a seal): p=1 finite "
                         "layer gives ratio<1 even at optimal angles (P3 0.825, C4 0.75) — QAOA != exact."}
    json.dump(report, open(os.path.join(OUT, "QAOA-FAMILY-REPORT.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("-" * 84)
    print(f"all_ok={all_ok}  →  .pgf/arith/QAOA-FAMILY-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
