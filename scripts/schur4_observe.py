#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""schur4_observe — TrackGate6 G4: 4-qubit Schur-Weyl transform witness (신규 봉인 0).

봉인된 schur4(16×16 Tier-0, plan=★기봉인 schur3 sub-app ⊗ I · W 5-Givens, 신규 module 0)에 대해:
  1. seal 링크(schur4 + sub-app schur3 복리) + golden 유니터리성.
  2. ★동시대각: U†J²U = diag — 고유값 분포 {6×5, 2×9, 0×2} (spin-2 ⊕ spin-1×3 ⊕ spin-0×2)
     + U†JzU = diag — label map m 값 전수 일치(16). J²·Jz 는 Pauli 합으로 독립 구성(회로·golden 무관).
  3. ★S₄ duality: 인접 전치 (01)(12)(23) 순열 연산자가 (j,m) 섹터 보존 + 표현 지표 —
     j=2→자명표현(P=+1 전수) · j=1→[3,1](m별 3×3, χ(전치)=1 → trace 3) · j=0→[2,2](χ(전치)=0).
  4. teeth 2종: ①CG 계수 오염(√¾→√0.7, 유니터리 유지) → J² 동시대각 붕괴 검출.
     ②label 열 교환(0010↔0001: j=2↔j=1) → J² 대각값이 label map 과 불일치 검출.

정직 경계(INV-Q3, seal 아님, root 성장은 schur4 봉인분뿐):
  - 봉인 = 회로==CG golden exact 뿐. J²/Jz 동시대각·S₄ duality = witness 관측.
  - n≥5 Schur·irrep 레지스터 분리(경로 라벨 재배열)=차기. 부호 규약(0111=−|1,−1⟩_A 등)=문서화 자유.

사용: python scripts/schur4_observe.py [--quick]
"""
import os, sys, re, json
from collections import Counter
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".pgf", "proofs", "SCHUR4-OBSERVE.json")

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)

# label map: |q0q1q2q3⟩ 인덱스 → (j, m)  (부호 자유 문서화 — spec 헤더와 동일)
LABELS = {0b0000: (2, 2), 0b0010: (2, 1), 0b1010: (2, 0), 0b1110: (2, -1), 0b1111: (2, -2),
          0b0001: (1, 1), 0b0011: (1, 0), 0b1011: (1, -1),
          0b1000: (1, 1), 0b1001: (1, 0), 0b0111: (1, -1),
          0b0100: (1, 1), 0b1100: (1, 0), 0b1101: (1, -1),
          0b0110: (0, 0), 0b0101: (0, 0)}


def load_golden_code():
    src = open(os.path.join(ROOT, "specs", "apps", "schur4.app.pg"), encoding="utf-8").read()
    return re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1)


def exec_golden(code):
    ns = {}
    exec(code, ns)
    return ns["golden"]


def total_ops():
    def tot(op):
        T = np.zeros((16, 16), dtype=complex)
        for q in range(4):
            M = np.eye(1, dtype=complex)
            for i in range(4):
                M = np.kron(M, op if i == q else I2)
            T += M
        return T
    Jx, Jy, Jz = tot(X / 2), tot(Y / 2), tot(Z / 2)
    return Jx @ Jx + Jy @ Jy + Jz @ Jz, Jz


def perm_op(p):
    M = np.zeros((16, 16), dtype=complex)
    for b in range(16):
        bits = [(b >> (3 - q)) & 1 for q in range(4)]
        nb = [bits[p[q]] for q in range(4)]
        M[int("".join(map(str, nb)), 2), b] = 1
    return M


def diag_checks(U, J2, Jz):
    cJ2 = U.conj().T @ J2 @ U
    cJz = U.conj().T @ Jz @ U
    off = float(max(np.abs(cJ2 - np.diag(np.diag(cJ2))).max(),
                    np.abs(cJz - np.diag(np.diag(cJz))).max()))
    d2 = np.real(np.diag(cJ2))
    dz = np.real(np.diag(cJz))
    dist = dict(Counter(np.round(d2, 9).tolist()))
    label_ok = all(abs(d2[i] - j * (j + 1)) < 1e-9 and abs(dz[i] - m) < 1e-9
                   for i, (j, m) in LABELS.items())
    return off, dist, label_ok


def observe():
    seal_ok = True
    for app in ("schur4", "schur3"):
        p = os.path.join(ROOT, "registry", "apps", f"{app}.sealed.json")
        seal_ok &= os.path.exists(p) and bool(json.load(open(p, encoding="utf-8")).get("u_hash"))
    code = load_golden_code()
    U = exec_golden(code)
    unitary_ok = bool(np.allclose(U.conj().T @ U, np.eye(16), atol=1e-12))

    J2, Jz = total_ops()
    off, dist, label_ok = diag_checks(U, J2, Jz)
    dist_ok = dist == {6.0: 5, 2.0: 9, 0.0: 2}

    # S₄ duality
    sectors = {}
    for i, (j, m) in LABELS.items():
        sectors.setdefault(j, []).append(i)
    s4_ok = True
    chars = {}
    for name, p in [("t01", [1, 0, 2, 3]), ("t12", [0, 2, 1, 3]), ("t23", [0, 1, 3, 2])]:
        cP = U.conj().T @ perm_op(p) @ U
        for j, idxs in sectors.items():
            other = [i for i in range(16) if i not in idxs]
            s4_ok &= bool(np.abs(cP[np.ix_(idxs, other)]).max() < 1e-12)
        s4_ok &= bool(np.allclose(cP[np.ix_(sectors[2], sectors[2])], np.eye(5), atol=1e-12))
        tr1 = float(np.real(np.trace(cP[np.ix_(sectors[1], sectors[1])])))
        tr0 = float(np.real(np.trace(cP[np.ix_(sectors[0], sectors[0])])))
        chars[name] = {"trace_j1_expect_3": tr1, "trace_j0_expect_0": tr0}
        s4_ok &= abs(tr1 - 3.0) < 1e-9 and abs(tr0) < 1e-9

    # teeth ①: CG 오염(√¾→√0.7) — 유니터리 유지, J² 동시대각 붕괴해야
    Ubad = exec_golden(code.replace("np.sqrt(3/4)", "np.sqrt(0.7)"))
    cbad = Ubad.conj().T @ J2 @ Ubad
    teeth_angle = bool(np.abs(cbad - np.diag(np.diag(cbad))).max() > 1e-3)
    # teeth ②: label 열 교환(0010↔0001, j=2↔j=1) — J² 대각값 label map 불일치해야
    Uswap = U.copy()
    Uswap[:, [0b0010, 0b0001]] = Uswap[:, [0b0001, 0b0010]]
    _, _, swap_label_ok = diag_checks(Uswap, J2, Jz)
    teeth_swap = bool(not swap_label_ok)

    ok = bool(seal_ok and unitary_ok and off < 1e-12 and dist_ok and label_ok
              and s4_ok and teeth_angle and teeth_swap)
    return {"app": "schur4",
            "decomposition": "2^⊗4 = spin-2(5) ⊕ spin-1(3×3) ⊕ spin-0(1×2) · S₄ [4]/[3,1]/[2,2]",
            "seal_links_schur4_schur3": seal_ok, "unitary": unitary_ok,
            "simultaneous_diag": {"offdiag_max": off, "J2_distribution": {str(k): v for k, v in dist.items()},
                                  "distribution_ok": dist_ok, "label_map_16": label_ok},
            "s4_duality": {"sector_preserving_and_characters": s4_ok, "characters": chars},
            "teeth": {"cg_corrupt_offdiag_detected": teeth_angle,
                      "label_swap_detected": teeth_swap},
            "compounding": "plan = 기봉인 schur3 sub-app ⊗ I · W(5 Givens, 반각 π/6·π/4·π/3 전부 기봉인)",
            "honest_boundary": "봉인=회로==CG golden exact 뿐. J²/Jz·S₄ duality=witness 관측(INV-Q3). "
                               "신규 module 0(G4b 승인 게이트 스킵). n≥5·irrep 레지스터 분리=차기.",
            "ok": ok}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"_schema": "schur4-observe-v1",
                       "_note": "4-qubit Schur-Weyl witness: J²/Jz 동시대각+S₄ duality+teeth. "
                                "봉인=유니터리뿐(INV-Q3).",
                       "observation": res}, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        d, s = res["simultaneous_diag"], res["s4_duality"]
        print("4-qubit Schur-Weyl witness 관측 (schur4):", flush=True)
        print(f"  seal(schur4+schur3) {res['seal_links_schur4_schur3']} · unitary {res['unitary']} · "
              f"동시대각 off {d['offdiag_max']:.1e} · J² 분포 {d['J2_distribution']} · label map {d['label_map_16']}",
              flush=True)
        print(f"  S₄ duality(섹터보존+[4]자명+[3,1]χ=1+[2,2]χ=0): {s['sector_preserving_and_characters']}",
              flush=True)
        print(f"  teeth: CG오염 {res['teeth']['cg_corrupt_offdiag_detected']} · "
              f"label교환 {res['teeth']['label_swap_detected']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"schur4_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
