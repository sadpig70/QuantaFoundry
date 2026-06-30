# -*- coding: utf-8 -*-
"""
paramshift_obs.py — W10.3 ParamShiftGradient (MasterRoadmap › TrackSC, 경량·옵션)

변분 미분의 정직 관찰. parameter-shift rule 이 봉인 Ry 모듈 실행으로 *exact* analytic gradient 를
줌을 시연하고, finite-difference(O(h²) 근사)와 대비. **신규 봉인 0 · root 불변**(관찰 전용).

state Ry(θ)|0>, observable Z: ⟨Z⟩=cosθ, exact ∂⟨Z⟩/∂θ=−sinθ.
봉인 모듈 실행(u_hash 게이트): θ=π/4 → ry_pi4 · θ+π/2=3π/4 → ry_3pi4 · θ−π/2=−π/4 → ry_negpi4.
param-shift = (⟨Z⟩(3π/4) − ⟨Z⟩(−π/4))/2 == −sin(π/4).

사용:  python scripts/paramshift_obs.py
"""
from __future__ import annotations
import os, sys, json
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, ORACLE)
import verify_seal as vs        # noqa: E402  (오라클 — 사용만: instantiate/hash_unitary)

MODS = os.path.join(ROOT, "specs", "modules")
MODREG = os.path.join(ROOT, "registry", "modules")
OUT = os.path.join(ROOT, ".pgf", "arith")
_Z = np.diag([1, -1]).astype(complex)


def _load_sealed_module(mid):
    """봉인 모듈을 u_hash 게이트 통과 후 dense 로 로드(load_sealed_app 의 모듈판; 오라클 사용만)."""
    seal_path = os.path.join(MODREG, f"{mid}.sealed.json")
    sealed = json.load(open(seal_path, encoding="utf-8"))
    if not sealed.get("sealed", False) or sealed.get("tier", 0) != 0:
        raise RuntimeError(f"{mid}: 미봉인/비-Tier0 — 실행 금지")
    blocks = vs._extract_blocks(open(os.path.join(MODS, f"{mid}.pg"), encoding="utf-8").read())
    U = np.asarray(vs.instantiate(blocks["golden"], "golden"), dtype=complex)
    if vs.hash_unitary(U) != sealed["u_hash"]:
        raise RuntimeError(f"{mid}: u_hash 불일치 — 변조/미봉인")
    return U


def _expect_z(U):
    z = np.zeros(U.shape[0], complex); z[0] = 1.0
    psi = U @ z
    return float((psi.conj() @ _Z @ psi).real)


def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 84)
    print("W10.3 ParamShiftGradient — 봉인 Ry 모듈 실행으로 parameter-shift(=exact gradient) 관찰.")
    print("=" * 84)

    theta = np.pi / 4
    # 봉인 모듈 실행 (u_hash 게이트)
    ez_t = _expect_z(_load_sealed_module("ry_pi4"))       # ⟨Z⟩(π/4)
    ez_plus = _expect_z(_load_sealed_module("ry_3pi4"))   # ⟨Z⟩(π/4+π/2)
    ez_minus = _expect_z(_load_sealed_module("ry_negpi4"))  # ⟨Z⟩(π/4−π/2)

    grad_ps = (ez_plus - ez_minus) / 2.0                  # parameter-shift
    grad_exact = -np.sin(theta)                            # 해석 미분 ∂cosθ/∂θ

    # finite-difference (근사, O(h²)) — 비-봉인 보조 평가로 대비
    h = 1e-2
    def ez_at(a):
        U = np.array([[np.cos(a / 2), -np.sin(a / 2)], [np.sin(a / 2), np.cos(a / 2)]], complex)
        return _expect_z(U)
    grad_fd = (ez_at(theta + h) - ez_at(theta - h)) / (2 * h)

    ps_exact = abs(grad_ps - grad_exact) < 1e-9
    fd_err = abs(grad_fd - grad_exact)
    print(f"θ=π/4 | ⟨Z⟩(π/4)={ez_t:.6f}  ⟨Z⟩(3π/4)={ez_plus:.6f}  ⟨Z⟩(−π/4)={ez_minus:.6f}")
    print(f"  parameter-shift grad = {grad_ps:.9f}  (exact −sin(π/4) = {grad_exact:.9f})  → exact? {ps_exact}")
    print(f"  finite-difference grad = {grad_fd:.9f}  → 오차 {fd_err:.2e} (>0, 근사)")

    all_ok = ps_exact and fd_err > 1e-6
    report = {
        "phase": "W10.3 ParamShiftGradient",
        "note": "OBSERVATION, NOT A SEAL. Sealed Ry modules executed via u_hash gate. parameter-shift rule "
                "gives the EXACT analytic gradient (-sin θ), contrasted with finite-difference (O(h^2) "
                "approximation). Zero new seals; registry/root unchanged.",
        "theta": "pi/4",
        "expect_z": {"theta": round(ez_t, 6), "theta_plus": round(ez_plus, 6), "theta_minus": round(ez_minus, 6)},
        "grad_parameter_shift": round(float(grad_ps), 9),
        "grad_exact": round(float(grad_exact), 9),
        "grad_finite_diff": round(float(grad_fd), 9),
        "param_shift_is_exact": bool(ps_exact),
        "finite_diff_error": float(fd_err),
        "all_ok": bool(all_ok),
        "seals_added": 0,
    }
    json.dump(report, open(os.path.join(OUT, "PARAMSHIFT-OBS-REPORT.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("-" * 84)
    print(f"all_ok={all_ok} (param-shift exact·finite-diff 근사)  신규 봉인 0·root 불변  →  PARAMSHIFT-OBS-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
