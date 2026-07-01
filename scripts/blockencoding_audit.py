#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""blockencoding_audit — V08_6 ConventionAudit + V08_8 QSP 관측 (QSVT 수평클래스).

block-encoding 규약을 고정·검증한다(관측, seal 아님):
  규약: ancilla = 상위(MSB) 큐빗 · block = (⟨0|_a ⊗ I) U (|0>_a ⊗ I) == A/α · big-endian · α=정규화.
  be_* 앱의 top-left 2^data 블록이 의도한 A/α 와 일치하는지 확인(teeth: 다른 A 는 불일치).

QSP 앱은 ⟨0|U|0> = P(a) 다항식값을 관측한다(observation, INV-Q3 — Trotter 근사경계의 자매, seal 아님).

비파괴: 읽기 전용 + sidecar `.pgf/proofs/BLOCKENCODING-AUDIT.json`. sealed/oracle/frozen/root 무영향.
봉인 자체는 app_assemble(Tier-0 EXACT, composite==golden)이 담당 — 본 스크립트는 block == A/α *의미* 를 관측.

사용: python scripts/blockencoding_audit.py [--quick]
"""
import os, re, sys, json
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPECS_APPS = os.path.join(ROOT, "specs", "apps")
OUT = os.path.join(ROOT, ".pgf", "proofs", "BLOCKENCODING-AUDIT.json")

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

# be_* 앱의 의도 A/α (규약 검증 대상). data 큐빗 수 = n_sys(app) - n_anc.
BE_TARGETS = {
    "be_xz": {"A": (X + Z) / 2, "alpha": 1.0, "n_anc": 1, "desc": "(X+Z)/2 via LCU(½X+½Z)"},
    "be_proj": {"A": np.diag([1, 0]).astype(complex), "alpha": 1.0, "n_anc": 1,
                "desc": "|0><0|=(I+Z)/2 via LCU (스펙트럼 비축퇴 → QSVT non-trivial)"},
}
QSP_APPS = ["qsp_d1"]
# QSVT 결합 앱: block == P(A) 고유값 변환(observation). data 큐빗 = n_sys - n_anc.
QSVT_APPS = {"qsvt_proj_d2": {"n_anc": 1, "A_desc": "|0><0|", "phi_desc": "φ=π/8 d=2",
                              "expect": np.diag([np.exp(1j * np.pi / 4) * np.exp(1j * np.pi / 8),
                                                 np.exp(1j * np.pi / 4) * np.exp(-1j * np.pi / 8)]).astype(complex)}}


def _load_golden(app_id):
    """app.pg 의 app_golden fence 를 exec → golden dense."""
    txt = open(os.path.join(SPECS_APPS, f"{app_id}.app.pg"), encoding="utf-8").read()
    code = re.search(r"```python id=app_golden\s*\n(.*?)\n```", txt, re.S).group(1)
    ns = {}
    exec(code, ns)
    return ns["golden"]


def _n_sys(app_id):
    txt = open(os.path.join(SPECS_APPS, f"{app_id}.app.pg"), encoding="utf-8").read()
    return json.loads(re.search(r"```json id=app_meta\s*\n(.*?)\n```", txt, re.S).group(1))["n_sys"]


def audit_be(app_id):
    """top-left 2^data block == A/α 검증 + negative control(다른 A 불일치)."""
    g = _load_golden(app_id)
    meta = BE_TARGETS[app_id]
    n_sys = _n_sys(app_id)
    d_data = 1 << (n_sys - meta["n_anc"])            # ancilla=MSB=0 → top-left 블록
    block = g[:d_data, :d_data]
    target = meta["A"] / meta["alpha"]
    match = bool(np.allclose(block, target, atol=1e-9))
    # teeth(공허하지 않음): block 이 *다른* 관측가능량(distractor)과는 불일치해야 — 비교가 discriminating.
    Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
    distractor = Y if d_data == 2 else np.roll(np.eye(d_data, dtype=complex), 1, axis=0)
    teeth = bool(not np.allclose(block, distractor, atol=1e-9))
    # unitarity of full U
    unitary = bool(np.allclose(g.conj().T @ g, np.eye(g.shape[0]), atol=1e-9))
    return {"app": app_id, "kind": "block-encoding", "desc": meta["desc"],
            "alpha": meta["alpha"], "n_anc": meta["n_anc"],
            "block_matches_A_over_alpha": match, "negative_control_teeth": teeth,
            "full_unitary": unitary, "ok": match and teeth and unitary}


def audit_qsp(app_id):
    """QSP 앱의 ⟨0|U|0> 다항식값 관측(observation, seal 아님)."""
    g = _load_golden(app_id)
    unitary = bool(np.allclose(g.conj().T @ g, np.eye(g.shape[0]), atol=1e-9))
    p00 = complex(g[0, 0])
    return {"app": app_id, "kind": "qsp", "observation": True,
            "poly_value_<0|U|0>": {"re": round(p00.real, 6), "im": round(p00.imag, 6)},
            "full_unitary": unitary, "ok": unitary,
            "note": "QSP 위상열의 정확 유니터리(Tier-0 봉인). 다항식 P(a) sweep=observation(INV-Q3)."}


def audit_qsvt(app_id):
    """QSVT 결합 앱: top-left block == P(A) 고유값 변환 관측(observation) + non-trivial 확인."""
    g = _load_golden(app_id)
    meta = QSVT_APPS[app_id]
    n_sys = _n_sys(app_id)
    d_data = 1 << (n_sys - meta["n_anc"])
    block = g[:d_data, :d_data]
    unitary = bool(np.allclose(g.conj().T @ g, np.eye(g.shape[0]), atol=1e-9))
    matches_expect = bool(np.allclose(block, meta["expect"], atol=1e-9))
    # non-trivial: block 이 스칼라·I 가 아님(고유값을 서로 다르게 변환 → 진짜 QSVT)
    nontrivial = bool(not np.allclose(block, block[0, 0] * np.eye(d_data), atol=1e-9))
    return {"app": app_id, "kind": "qsvt", "observation": True, "A": meta["A_desc"], "phi": meta["phi_desc"],
            "block_matches_expected_P(A)": matches_expect,
            "nontrivial_eigenvalue_transform": nontrivial, "full_unitary": unitary,
            "ok": unitary and matches_expect and nontrivial,
            "note": "block-encoding + projector-controlled rotation → P(A) 고유값 변환(Tier-0 봉인). "
                    "다항식 P sweep=observation(INV-Q3)."}


def main():
    quick = "--quick" in sys.argv
    results = {}
    all_ok = True
    for aid in BE_TARGETS:
        if not os.path.exists(os.path.join(SPECS_APPS, f"{aid}.app.pg")):
            continue
        r = audit_be(aid); results[aid] = r
        all_ok = all_ok and r["ok"]
    for aid in QSP_APPS:
        if not os.path.exists(os.path.join(SPECS_APPS, f"{aid}.app.pg")):
            continue
        r = audit_qsp(aid); results[aid] = r
        all_ok = all_ok and r["ok"]
    for aid in QSVT_APPS:
        if not os.path.exists(os.path.join(SPECS_APPS, f"{aid}.app.pg")):
            continue
        r = audit_qsvt(aid); results[aid] = r
        all_ok = all_ok and r["ok"]

    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        report = {"_schema": "blockencoding-audit-v1",
                  "_note": "block-encoding 규약(ancilla=MSB·top-left==A/α·big-endian) 관측 + QSP 다항식 관측. "
                           "seal 아님(봉인은 app_assemble composite==golden). sealed/oracle/root 무영향.",
                  "convention": {"ancilla": "MSB(상위)", "block": "(⟨0|_a⊗I)U(|0>_a⊗I)==A/α",
                                 "endian": "big", "alpha": "정규화상수(LCU=Σ|c_i|)"},
                  "results": results}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        for aid, r in results.items():
            if r["kind"] == "block-encoding":
                print(f"  {aid}: block==A/α {r['block_matches_A_over_alpha']} · teeth {r['negative_control_teeth']} "
                      f"· {r['desc']}", flush=True)
            elif r["kind"] == "qsvt":
                print(f"  {aid}: QSVT block==P(A) {r['block_matches_expected_P(A)']} · "
                      f"non-trivial 고유값변환 {r['nontrivial_eigenvalue_transform']} ({r['phi']}, observation)", flush=True)
            else:
                print(f"  {aid}: QSP ⟨0|U|0>={r['poly_value_<0|U|0>']} (observation)", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"blockencoding_audit: all_ok={all_ok}", flush=True)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
