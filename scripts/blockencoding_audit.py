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
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

# be_* 앱의 의도 A/α (규약 검증 대상). data 큐빗 수 = n_sys(app) - n_anc.
BE_TARGETS = {
    "be_xz": {"A": (X + Z) / 2, "alpha": 1.0, "n_anc": 1, "desc": "(X+Z)/2 via LCU(½X+½Z)"},
    "be_proj": {"A": np.diag([1, 0]).astype(complex), "alpha": 1.0, "n_anc": 1,
                "desc": "|0><0|=(I+Z)/2 via LCU (스펙트럼 비축퇴 → QSVT non-trivial)"},
    "be_pauli2": {"A": (np.kron(X, X) + np.kron(Z, Z)) / 2, "alpha": 1.0, "n_anc": 1,
                  "desc": "(XX+ZZ)/2 Pauli LCU (2q Hermitian, commuting→비축퇴 고유값 -1,0,0,1)"},
    "be_hop": {"A": (np.kron(X, X) + np.kron(Y, Y)) / 2, "alpha": 1.0, "n_anc": 1,
               "desc": "(XX+YY)/2 fermionic hopping (Jordan-Wigner, 고유값 -1,0,0,1)"},
    "be_num": {"A": np.diag([0, 1]).astype(complex), "alpha": 1.0, "n_anc": 1,
               "desc": "n=(I-Z)/2=|1><1| fermionic number operator (Hubbard interaction 기본블록)"},
    "be_hopz": {"A": (np.kron(np.kron(X, Z), X) + np.kron(np.kron(Y, Z), Y)) / 2, "alpha": 1.0, "n_anc": 1,
                "desc": "(XZX+YZY)/2 비인접 hopping w/ JW Z-string (spinful Hubbard, 고유값 ±1·0)"},
    "select_prepare4": {"A": np.eye(2, dtype=complex) + X + Y + Z, "alpha": 4.0, "n_anc": 2,
                        "desc": "HE H4.2 generic SELECT-PREPARE 템플릿: (I+X+Y+Z)/4 전 4종 Pauli, "
                                "고유값 (1±√3)/4 비축퇴"},
}
QSP_APPS = ["qsp_d1", "qsp_d3", "qsp_d5"]   # 홀수 degree-1/3/5 = amp-amp·matrix-inversion 기본블록
# QSVT family: 같은 be_proj block-encoding + 다른 위상열 → 다른 P(A). "one seal, many algorithms".
# block == P(A) 고유값 변환(observation). data 큐빗 = n_sys - n_anc. expect=sanity(있으면 대조).
QSVT_APPS = {
    "qsvt_proj_d2": {"n_anc": 1, "A_desc": "|0><0|", "phi_desc": "φ=π/8 d=2", "be": "be_proj",
                     "expect": np.diag([np.exp(1j * np.pi / 4) * np.exp(1j * np.pi / 8),
                                        np.exp(1j * np.pi / 4) * np.exp(-1j * np.pi / 8)]).astype(complex)},
    "qsvt_proj_d2b": {"n_anc": 1, "A_desc": "|0><0|", "phi_desc": "φ=π/16 d=2", "be": "be_proj"},
    "qsvt_proj_d3": {"n_anc": 1, "A_desc": "|0><0|", "phi_desc": "φ=π/8 d=3(홀수, projector-like 필터)", "be": "be_proj"},
    "qsvt_pauli2_d2": {"n_anc": 1, "A_desc": "(XX+ZZ)/2", "phi_desc": "φ=π/8 d=2 (2q 짝수 Chebyshev)", "be": "be_pauli2"},
    "qsvt_pauli2_d3": {"n_anc": 1, "A_desc": "(XX+ZZ)/2", "phi_desc": "φ=π/8 d=3 (2q 홀수 Chebyshev: 1→i,-1→-i)", "be": "be_pauli2"},
}


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
    # non-trivial: block 이 스칼라·I 가 아님(고유값을 서로 다르게 변환 → 진짜 QSVT)
    nontrivial = bool(not np.allclose(block, block[0, 0] * np.eye(d_data), atol=1e-9))
    # P(A) 고유값 프로파일 — observation. block 의 고유값(non-diagonal block 대응, 위상·크기 정렬).
    evs = np.linalg.eigvals(block)
    evs = sorted(evs, key=lambda z: (round(float(np.angle(z)), 4), round(float(abs(z)), 4)))
    profile = [[round(float(z.real), 4), round(float(z.imag), 4)] for z in evs]
    r = {"app": app_id, "kind": "qsvt", "observation": True, "A": meta["A_desc"], "phi": meta["phi_desc"],
         "be_source": meta.get("be"), "eigenvalue_profile_P": profile,
         "nontrivial_eigenvalue_transform": nontrivial, "full_unitary": unitary,
         "note": "block-encoding + projector-controlled rotation → P(A) 고유값 변환(Tier-0 봉인). "
                 "다항식 P sweep=observation(INV-Q3)."}
    if "expect" in meta:
        r["block_matches_expected_P(A)"] = bool(np.allclose(block, meta["expect"], atol=1e-9))
        r["ok"] = unitary and nontrivial and r["block_matches_expected_P(A)"]
    else:
        r["ok"] = unitary and nontrivial
    return r


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

    # compounding 요약: 같은 be_source 에 다른 위상열 → 다른 P(A) ("one seal, many algorithms")
    by_be = {}
    for aid, r in results.items():
        if r.get("kind") == "qsvt":
            by_be.setdefault(r["be_source"], []).append(
                {"app": aid, "phi": r["phi"], "P_eigenvalues": r["eigenvalue_profile_P"]})
    compounding = {be: {"n_transforms": len(v),
                        "distinct_P": len({tuple(map(tuple, t["P_eigenvalues"])) for t in v}) == len(v),
                        "transforms": v} for be, v in by_be.items()}
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        report = {"_schema": "blockencoding-audit-v1",
                  "_note": "block-encoding 규약(ancilla=MSB·top-left==A/α·big-endian) 관측 + QSP/QSVT P(A) 관측. "
                           "seal 아님(봉인은 app_assemble composite==golden). sealed/oracle/root 무영향.",
                  "convention": {"ancilla": "MSB(상위)", "block": "(⟨0|_a⊗I)U(|0>_a⊗I)==A/α",
                                 "endian": "big", "alpha": "정규화상수(LCU=Σ|c_i|)"},
                  "one_seal_many_algorithms": compounding, "results": results}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        for aid, r in results.items():
            if r["kind"] == "block-encoding":
                print(f"  {aid}: block==A/α {r['block_matches_A_over_alpha']} · teeth {r['negative_control_teeth']} "
                      f"· {r['desc']}", flush=True)
            elif r["kind"] == "qsvt":
                print(f"  {aid}: QSVT P(A)={r['eigenvalue_profile_P']} · "
                      f"non-trivial {r['nontrivial_eigenvalue_transform']} ({r['phi']}, observation)", flush=True)
            else:
                print(f"  {aid}: QSP ⟨0|U|0>={r['poly_value_<0|U|0>']} (observation)", flush=True)
        for be, c in compounding.items():
            print(f"  ★ one seal '{be}' → {c['n_transforms']} distinct QSVT transforms "
                  f"(distinct_P={c['distinct_P']})", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"blockencoding_audit: all_ok={all_ok}", flush=True)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
