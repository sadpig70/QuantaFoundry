#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""peps_observe — TrackGate6 G1: 2×2 RVB PEPS witness (신규 봉인 0).

봉인된 peps22_rvb(4q, 33스텝, 신규 module 0)에 대해:
  1. seal 링크 + 준비 유니터리 unitarity.
  2. ★정의 열 독립 검증: golden|0000⟩ == dimer covering 합 직접 재구성
     (|cov_H⟩+|cov_V⟩, H={01,23}·V={02,13}, singlet=(|01⟩−|10⟩)/√2 i<j 고정) exact —
     회로와 무관한 RVB *정의*로부터의 두 번째 경로.
  3. ★SU(2) singlet witness: S_tot²|RVB⟩ = 0 exact (총스핀 0 — RVB 의 물리 본질).
  4. 국소 최대혼합: 각 사이트 reduced ρ = I/2 (weight-2 support → 대각, 확률 1/2 균등).
  5. teeth: ①orientation 반전(수직쌍 singlet 방향 flip → ⟨H|V⟩=−1/2·norm²=1 인 *다른* 상태)
     ②각도 오염(ry_k6→0.9배) — 둘 다 정의 열과 불일치 검출.

정직 경계(aklt4 상속, INV-Q3): 봉인=준비 유니터리(Tier-0 exact). RVB 물리는 **정의 열(|0⟩^⊗4 입력)뿐**
  — 여타 열=회로-유도 유니터리 완성. S_tot²·reduced ρ=witness 관측(seal 아님).
  n>2×2 격자·PBC·bond>1 일반 PEPS·parent-H gap=차기.

사용: python -m qf_witness.observe.peps_observe [--quick]
"""
import os, sys, re, json
import numpy as np

from qf_witness.core.paths import ROOT
OUT = os.path.join(ROOT, ".pgf", "proofs", "PEPS-OBSERVE.json")

X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
I2 = np.eye(2, dtype=complex)


def load_golden(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    ns = {}
    exec(re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1), ns)
    return ns["golden"]


def covering_state(pairs, flip=None, n=4):
    """dimer covering = singlet 곱. flip=(i,j)면 그 쌍 orientation 반전(teeth용)."""
    v = np.zeros(2 ** n, dtype=complex)
    for basis in range(2 ** n):
        bits = [(basis >> (n - 1 - q)) & 1 for q in range(n)]
        amp = 1.0
        for (i, j) in pairs:
            bi, bj = bits[i], bits[j]
            if bi == bj:
                amp = 0.0
                break
            s = 1 if (bi, bj) == (0, 1) else -1
            if flip == (i, j):
                s = -s
            amp *= s / np.sqrt(2)
        v[basis] = amp
    return v


def rvb_reference(flip=None):
    v = covering_state([(0, 1), (2, 3)]) + covering_state([(0, 2), (1, 3)], flip=flip)
    return v / np.sqrt(np.vdot(v, v).real)


def total_spin_sq(n=4):
    def emb(op, q):
        ops = [I2] * n; ops[q] = op
        M = ops[0]
        for o in ops[1:]:
            M = np.kron(M, o)
        return M
    S2 = np.zeros((2 ** n, 2 ** n), dtype=complex)
    for P in (X, Y, Z):
        tot = sum(emb(P, q) for q in range(n)) / 2
        S2 += tot @ tot
    return S2


def observe():
    app_id = "peps22_rvb"
    sealed = os.path.join(ROOT, "registry", "apps", f"{app_id}.sealed.json")
    link = os.path.exists(sealed) and bool(json.load(open(sealed, encoding="utf-8")).get("u_hash"))
    U = load_golden(f"{app_id}.app.pg")
    unitary = bool(np.allclose(U.conj().T @ U, np.eye(16), atol=1e-12))
    psi = U[:, 0]

    # 2. 정의 열 독립 재구성 (dimer 정의)
    ref = rvb_reference()
    col_dev = float(np.abs(psi - ref).max())

    # 3. S_tot² = 0
    s2_dev = float(np.abs(total_spin_sq() @ psi).max())

    # 4. 국소 reduced ρ = I/2 (4사이트 전수)
    rho = np.outer(psi, psi.conj())
    red_dev = 0.0
    for q in range(4):
        r = np.zeros((2, 2), dtype=complex)
        for e in range(8):
            # trace out 나머지 3큐빗: 환경 basis e 마다 |s⟩ 성분 추출 후 비간섭 합산
            idx = {}
            for s in range(2):
                bits = []
                ei = 0
                for w in range(4):
                    if w == q:
                        bits.append(s)
                    else:
                        bits.append((e >> (2 - ei)) & 1)
                        ei += 1
                v_ = 0
                for bb in bits:
                    v_ = (v_ << 1) | bb
                idx[s] = v_
            for s in range(2):
                for sp in range(2):
                    r[s, sp] += rho[idx[s], idx[sp]]
        red_dev = max(red_dev, float(np.abs(r - I2 / 2).max()))

    # 5. teeth
    ref_flip = rvb_reference(flip=(0, 2))
    teeth_orient = bool(np.abs(psi - ref_flip).max() > 1e-3)
    # 각도 오염: ry_k6 0.9배로 재합성한 정의 열은 불일치해야
    t6 = 0.9 * np.arccos(np.sqrt(1 / 6))
    bad = psi.copy()
    # site1 분기 진폭만 오염 근사 재구성(관측 teeth 용 독립 모델): P(0|x0=0)=cos²(t6)
    p0 = np.cos(t6) ** 2
    bad_ref = ref.copy()
    scale0 = np.sqrt(p0 / (1 / 6))
    for b in range(16):
        bits = [(b >> (3 - q)) & 1 for q in range(4)]
        if bits[0] == 0 and abs(ref[b]) > 1e-12:
            bad_ref[b] = ref[b] * (scale0 if bits[1] == 0 else np.sqrt((1 - p0) / (5 / 6)))
    teeth_angle = bool(np.abs(psi - bad_ref / np.linalg.norm(bad_ref)).max() > 1e-3)

    ok = bool(link and unitary and col_dev < 1e-12 and s2_dev < 1e-12 and red_dev < 1e-12
              and teeth_orient and teeth_angle)
    return {"app": app_id, "seal_link": link, "unitary": unitary,
            "defining_column_vs_dimer_definition": col_dev,
            "S_tot_sq_annihilation": s2_dev,
            "single_site_reduced_maximally_mixed": red_dev,
            "teeth": {"orientation_flip_detected": teeth_orient, "angle_corruption_detected": teeth_angle},
            "sealed_assets": "peps22_rvb (준비 유니터리 Tier-0 exact, 33스텝, 신규 module 0)",
            "honest_boundary": "봉인=준비 유니터리뿐. RVB 물리=정의 열(|0⟩^⊗4)만 — 여타 열=회로-유도 완성. "
                               "S_tot²·reduced ρ=witness 관측(INV-Q3). n>2×2·PBC·일반 PEPS=차기.",
            "ok": ok}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"_schema": "peps-observe-v1",
                       "_note": "2×2 RVB PEPS witness: dimer 정의 독립 재구성+S_tot²=0+reduced I/2+teeth.",
                       "observation": res}, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("2×2 RVB PEPS witness 관측:", flush=True)
        print(f"  seal {res['seal_link']} · unitary {res['unitary']} · 정의열==dimer정의 "
              f"{res['defining_column_vs_dimer_definition']:.1e} · S_tot² {res['S_tot_sq_annihilation']:.1e} · "
              f"reduced I/2 {res['single_site_reduced_maximally_mixed']:.1e}", flush=True)
        print(f"  teeth: orientation {res['teeth']['orientation_flip_detected']} · "
              f"angle {res['teeth']['angle_corruption_detected']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"peps_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
