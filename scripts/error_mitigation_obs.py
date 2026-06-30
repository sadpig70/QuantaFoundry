# -*- coding: utf-8 -*-
"""
error_mitigation_obs.py — W12.4 ErrorMitigationObservation

Zero-noise extrapolation (ZNE) over already sealed Tier-0 apps.

Honesty boundary:
  - NOTHING is sealed here. The noise model, noisy expectations, and extrapolated values are
    observations only.
  - Inputs are already sealed apps loaded through backend_adapter's u_hash gate.
  - Mitigation is bias reduction, not exact recovery. The gate requires
    noisy_error > zne_error > 0.
  - registry_root_hash must remain unchanged.

Usage: python scripts/error_mitigation_obs.py
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import backend_adapter as ba  # noqa: E402  (sealed-app execution gate, use only)

OUT = os.path.join(ROOT, ".pgf", "backend")
MANIFEST = os.path.join(ROOT, "registry", "REGISTRY-MANIFEST.json")
EXPECTED_ROOT_PREFIX = "211ef5bb910304d3"

_I2 = np.eye(2, dtype=complex)
_X = np.array([[0, 1], [1, 0]], complex)
_Z = np.diag([1, -1]).astype(complex)


def _registry_root():
    return json.load(open(MANIFEST, encoding="utf-8"))["registry_root_hash"]


def _embed(gate, targets, n):
    """Embed a k-qubit operator into n qubits, big-endian q0..q(n-1)."""
    k = len(targets)
    G = gate.reshape([2] * k + [2] * k)
    T = np.eye(1 << n, dtype=complex).reshape([2] * n + [1 << n])
    T = np.tensordot(G, T, axes=(list(range(k, 2 * k)), targets))
    T = np.moveaxis(T, list(range(k)), targets)
    return T.reshape(1 << n, 1 << n)


def _expect(psi, observable):
    return float((psi.conj() @ observable @ psi).real)


def _trace_mean(observable):
    return float(np.trace(observable).real / observable.shape[0])


def _maxcut_cost(n, edges):
    dim = 1 << n
    C = np.zeros((dim, dim), dtype=complex)
    for i, j in edges:
        C += 0.5 * (np.eye(dim, dtype=complex) - _embed(_Z, [i], n) @ _embed(_Z, [j], n))
    return C


def _observable_case(case_id):
    if case_id == "tfim3_suzuki4_X0":
        app = ba.load_sealed_app("tfim3_suzuki4_step")
        n = app["n"]
        psi = app["U"] @ ba.zero_state(n)
        obs = _embed(_X, [0], n)
        return {
            "case": case_id,
            "app_id": app["id"],
            "n": n,
            "observable": "X0",
            "psi": psi,
            "observable_matrix": obs,
            "u_hash": app["u_hash"],
            "tier": app["tier"],
        }
    if case_id == "qaoa_p3_maxcut":
        app = ba.load_sealed_app("qaoa_p3")
        n = app["n"]
        psi = app["U"] @ ba.zero_state(n)
        obs = _maxcut_cost(n, [(0, 1), (1, 2)])
        return {
            "case": case_id,
            "app_id": app["id"],
            "n": n,
            "observable": "MaxCutCost(P3)",
            "psi": psi,
            "observable_matrix": obs,
            "u_hash": app["u_hash"],
            "tier": app["tier"],
        }
    raise ValueError(f"unknown case: {case_id}")


def _depolarized_expectation(ideal, trace_mean, base_epsilon, scale):
    """Observation-only global depolarizing expectation.

    Repeated noise folding is modeled as alpha=(1-eps)^scale, so a linear ZNE fit is
    intentionally imperfect. That keeps mitigation distinct from exact recovery.
    """
    alpha = (1.0 - base_epsilon) ** float(scale)
    return alpha * ideal + (1.0 - alpha) * trace_mean


def _zne_linear(scales, values):
    slope, intercept = np.polyfit(np.asarray(scales, dtype=float), np.asarray(values, dtype=float), 1)
    return float(intercept), float(slope)


def observe_case(case_id, base_epsilon=0.06, scales=(1, 3, 5)):
    c = _observable_case(case_id)
    ideal = _expect(c["psi"], c["observable_matrix"])
    mean = _trace_mean(c["observable_matrix"])
    noisy = [_depolarized_expectation(ideal, mean, base_epsilon, s) for s in scales]
    zne, slope = _zne_linear(scales, noisy)
    noisy_error = abs(noisy[0] - ideal)
    zne_error = abs(zne - ideal)
    checks = {
        "sealed_gate_passed": c["tier"] == 0 and bool(c["u_hash"]),
        "noisy_bias_visible": noisy_error > 1e-6,
        "zne_reduces_bias": zne_error < noisy_error,
        "zne_not_exact": zne_error > 1e-7,
    }
    return {
        "case": c["case"],
        "app_id": c["app_id"],
        "n": c["n"],
        "observable": c["observable"],
        "u_hash": c["u_hash"],
        "tier": c["tier"],
        "base_epsilon": base_epsilon,
        "noise_scales": list(scales),
        "ideal_expectation": round(ideal, 12),
        "depolarized_trace_mean": round(mean, 12),
        "noisy_expectations": [round(v, 12) for v in noisy],
        "zne_linear_estimate": round(zne, 12),
        "zne_linear_slope": round(slope, 12),
        "scale1_noisy_error": round(noisy_error, 12),
        "zne_error": round(zne_error, 12),
        "error_reduction_factor": round(noisy_error / zne_error, 6) if zne_error else None,
        "expectation_checks": checks,
        "all_expectations_met": all(checks.values()),
    }


def main():
    os.makedirs(OUT, exist_ok=True)
    root_before = _registry_root()
    print("=" * 86)
    print("W12.4 ErrorMitigationObservation — ZNE 관찰(root 불변, 신규 봉인 0).")
    print("정직성: mitigation은 bias reduction estimate이며 exact recovery/verification이 아니다.")
    print("=" * 86)

    cases = ["tfim3_suzuki4_X0", "qaoa_p3_maxcut"]
    results = []
    all_ok = True
    for case_id in cases:
        try:
            row = observe_case(case_id)
        except Exception as e:
            row = {"case": case_id, "error": f"{type(e).__name__}: {e}", "all_expectations_met": False}
        all_ok = all_ok and bool(row.get("all_expectations_met", False))
        results.append(row)
        if "error" in row:
            print(f"  ✗ {case_id}: {row['error']}")
            continue
        print(
            f"  {'✓' if row['all_expectations_met'] else '✗'} {case_id}: "
            f"ideal={row['ideal_expectation']} noisy_err={row['scale1_noisy_error']} "
            f"zne_err={row['zne_error']} reduction={row['error_reduction_factor']}x"
        )

    root_after = _registry_root()
    root_ok = root_before == root_after and root_after.startswith(EXPECTED_ROOT_PREFIX)
    report = {
        "phase": "W12.4 ErrorMitigationObservation",
        "honesty_boundary": "OBSERVATION, NOT A SEAL. Deterministic depolarizing-noise expectations and "
                            "zero-noise extrapolation are simulator-side estimates over already sealed "
                            "Tier-0 apps loaded through backend_adapter. Mitigation reduces bias but is not "
                            "exact recovery or verification.",
        "registry_root_before": root_before,
        "registry_root_after": root_after,
        "root_unchanged": root_ok,
        "new_seals": 0,
        "model": {
            "noise": "global depolarizing expectation",
            "alpha": "(1-base_epsilon)^scale",
            "zne": "linear fit over scales [1,3,5], evaluated at scale=0",
            "base_epsilon": 0.06,
        },
        "cases": results,
        "all_ok": bool(all_ok and root_ok),
    }
    out_path = os.path.join(OUT, "ERROR-MITIGATION-REPORT.json")
    json.dump(report, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("-" * 86)
    print(f"root_unchanged={root_ok} all_ok={report['all_ok']} -> .pgf/backend/ERROR-MITIGATION-REPORT.json")
    return 0 if report["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
