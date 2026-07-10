#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""aklt_observe — HE2 V4: AKLT₄ VBS 상태 준비의 독립 검증 witness (신규 봉인 0).

봉인된 aklt4(9q 준비 회로)의 정의 열(U|0⟩⁹)을 표현론/물리로 독립 검증:
  1. ★독립 참조: AKLT MPS 닫힌형 수축(A⁺=√⅔σ⁺·A⁰=−√⅓σz·A⁻=−√⅔σ⁻, OBC ⟨0|·|0⟩,
     norm²=41/81)과 회로 정의 열이 exact 일치 — 회로와 완전 독립 경로(부호 포함).
  2. bond wire(q8) 청정: 정의 열에서 |1⟩_bond 성분 = 0.
  3. parent-H witness: 인접 site spin-2 사영 P⁽²⁾ 가 상태를 소멸(3 bond 전부) — VBS 정의 성질.
  4. site triplet 멤버십: 각 site 2q가 singlet 성분 0 (spin-1 임베딩 유효).
  5. string order ⟨S^z exp(iπΣS^z) S^z⟩ 관측값 보고(Haldane 위상 시그니처, seal 아님).
  6. teeth: 틀린 상태(소회전 섭동)는 1·3이 검출해야. 경계변주 OBC(0,1)=바닥다양체의 다른 edge 상태 —
     parent-H 는 구별 불가(4중 축퇴가 물리적으로 정확), edge 상태 고정은 MPS exact-match(1)만 가능함을 실증.
     (참고: A⁰ 부호규약은 짝수사슬+동일경계에서 #m₀ 짝수 강제로 상태 자체 불변 = 비관측 규약.)

정직 경계(INV-Q3, seal 아님, root 불변):
  - 봉인 = aklt4 회로==golden exact(C-app) 뿐. AKLT-상태 정합·parent-H·string order = 관측 witness.
  - 정의 열만 AKLT 물리; 여타 열 = 회로-유도 완성. n>4·PBC·bond>2 일반 MPS = 차기. 신규 봉인 0.

사용: python -m qf_witness.observe.aklt_observe [--quick]
"""
import os, sys, re, json
from functools import reduce
import numpy as np

from qf_witness.core.paths import ROOT
OUT = os.path.join(ROOT, ".pgf", "proofs", "AKLT-OBSERVE.json")


def load_golden(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    ns = {}
    exec(re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1), ns)
    return ns["golden"]


def aklt_state(bR=0):
    """독립 MPS 수축. bR=우측 경계(0=표준 타겟 OBC(0,0), 1=teeth 용 다른 edge 상태 OBC(0,1))."""
    Ap = np.sqrt(2/3) * np.array([[0, 1], [0, 0]])
    A0 = -np.sqrt(1/3) * np.array([[1, 0], [0, -1]])
    Am = -np.sqrt(2/3) * np.array([[0, 0], [1, 0]])
    A = {1: Ap, 0: A0, -1: Am}
    T = {1: np.array([1., 0, 0, 0]), 0: np.array([0, 1., 1, 0]) / np.sqrt(2),
         -1: np.array([0, 0, 0, 1.])}
    psi = np.zeros(256)
    for m1 in (1, 0, -1):
        for m2 in (1, 0, -1):
            for m3 in (1, 0, -1):
                for m4 in (1, 0, -1):
                    c = (A[m1] @ A[m2] @ A[m3] @ A[m4])[0, bR]
                    if abs(c) > 1e-15:
                        psi += c * np.kron(np.kron(T[m1], T[m2]), np.kron(T[m3], T[m4]))
    n2 = psi @ psi
    return psi / np.sqrt(n2), n2


def spin1_embed():
    """triplet 임베딩 등척(4×3)과 spin-1 연산자."""
    tri = np.zeros((4, 3)); tri[0, 0] = 1; tri[1, 1] = tri[2, 1] = 1/np.sqrt(2); tri[3, 2] = 1
    sx = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]) / np.sqrt(2)
    sy = np.array([[0, -1j, 0], [1j, 0, -1j], [0, 1j, 0]]) / np.sqrt(2)
    sz = np.diag([1., 0, -1]).astype(complex)
    return tri, sx, sy, sz


def witnesses(col):
    """정의 열에 대한 parent-H/triplet witness (col: 256-dim, 실수 기대)."""
    tri, sx, sy, sz = spin1_embed()
    SS = sum(np.kron(a, b) for a, b in [(sx, sx), (sy, sy), (sz, sz)])
    P2 = (SS + np.eye(9)) @ (SS + 2*np.eye(9)) / 6         # spin-2 사영(고유값 1·-1·-2 기반)
    emb2 = np.kron(tri, tri)                                # 16×9
    P2q = emb2 @ P2 @ emb2.conj().T
    p2v = []
    for k in range(3):                                      # bonds (site k+1, k+2) → 큐빗 4k..4k+3
        left = np.eye(2**(2*k)) if k > 0 else np.eye(1)
        right = np.eye(2**(4 - 2*k)) if k < 2 else np.eye(1)
        full = np.kron(np.kron(left, P2q), right)
        p2v.append(float(np.linalg.norm(full @ col)))
    # site triplet 멤버십: singlet 사영 성분 0
    sing = np.array([0, 1., -1, 0]) / np.sqrt(2)
    Ps = np.outer(sing, sing)
    sv = []
    for s in range(4):
        left = np.eye(2**(2*s)) if s > 0 else np.eye(1)
        right = np.eye(2**(6 - 2*s)) if s < 3 else np.eye(1)
        sv.append(float(np.linalg.norm(np.kron(np.kron(left, Ps), right) @ col)))
    return p2v, sv


def string_order(col):
    """⟨S^z_1 exp(iπ(S^z_2+S^z_3)) S^z_4⟩ 관측값 (Haldane 시그니처, 값 보고만)."""
    tri, sx, sy, sz = spin1_embed()
    Szq = tri @ sz @ tri.conj().T
    Expq = tri @ np.diag(np.exp(1j*np.pi*np.array([1., 0, -1]))) @ tri.conj().T \
        + (np.eye(4) - tri @ tri.conj().T)                  # triplet 밖 항등(상태는 triplet 내)
    O = reduce(np.kron, [Szq, Expq, Expq, Szq])
    return float(np.real(col.conj() @ O @ col))


def observe():
    G = load_golden("aklt4.app.pg")
    col9 = np.real(G[:, 0])                                 # U|0⟩⁹ (전 성분 실수 구성)
    im_max = float(np.abs(np.imag(G[:, 0])).max())
    M = col9.reshape(256, 2)
    bond_clean = float(np.linalg.norm(M[:, 1]))             # |1⟩_bond 성분
    col = M[:, 0]                                           # sys 8q 성분

    psi, n2 = aklt_state()
    norm41 = bool(np.isclose(n2, 41/81, atol=1e-12))
    match = float(np.abs(col - psi).max())                  # 부호 포함 exact 비교
    p2v, sv = witnesses(col)
    so = string_order(col)

    # teeth 1: 틀린 상태 — 정의 열을 소폭 회전(첫 site y 큐빗에 Ry(0.05))한 상태는 검출돼야
    ry = np.array([[np.cos(0.025), -np.sin(0.025)], [np.sin(0.025), np.cos(0.025)]])
    R = reduce(np.kron, [np.eye(2), ry] + [np.eye(2)]*6)
    colbad = R @ col
    p2bad, _ = witnesses(colbad)
    teeth1 = (np.abs(colbad - psi).max() > 1e-3) and (max(p2bad) > 1e-3)
    # teeth 2: 경계변주 OBC(0,1) = 바닥다양체의 다른 edge 상태(norm²=40/81) —
    #   parent-H 는 소멸 유지(축퇴가 정직), MPS exact-match 만 edge 상태를 고정함을 실증.
    psi_alt, n2_alt = aklt_state(bR=1)
    p2alt, _ = witnesses(psi_alt)
    teeth2 = (np.abs(col - psi_alt).max() > 1e-3) and (max(p2alt) < 1e-9) \
        and bool(np.isclose(n2_alt, 40/81, atol=1e-12))

    ok = (norm41 and im_max < 1e-12 and bond_clean < 1e-12 and match < 1e-12
          and max(p2v) < 1e-9 and max(sv) < 1e-9 and teeth1 and teeth2)
    return {"axis": "AKLT VBS 상태 준비 (MPS χ=2 텐서망, Haldane 위상)",
            "sealed_asset": "aklt4 (9q 순차 조건화 등척 준비 회로, ry_ak41/13/7± + ry_k5 복리)",
            "norm_sq_41_81": norm41,
            "mps_reference_exact_match": match,
            "bond_wire_clean": bond_clean,
            "parent_H_P2_violations": p2v,
            "site_singlet_components": sv,
            "string_order_value": so,
            "teeth_wrong_angle_detected": bool(teeth1),
            "teeth_edge_state_mps_only": bool(teeth2),
            "degeneracy_note": "OBC(0,1) edge 상태(norm²=40/81)는 parent-H 소멸 유지(바닥다양체 축퇴가 정확) — edge 고정은 MPS exact-match 만 가능",
            "honest_boundary": "봉인=aklt4 회로==golden exact(C-app) 뿐. MPS 정합·parent-H 소멸·string order="
                               "관측 witness. 정의 열만 AKLT 물리(여타 열=회로-유도 완성). "
                               "n>4·PBC·bond>2 일반 MPS=차기. 신규 봉인 0(INV-Q3).",
            "ok": bool(ok)}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        report = {"_schema": "aklt-observe-v1",
                  "_note": "AKLT₄ 정의 열의 독립 MPS 수축 exact 일치 + parent-H/triplet witness. 봉인=aklt4 뿐(INV-Q3). 신규 봉인 0.",
                  "observation": res}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("AKLT₄ VBS witness 관측:", flush=True)
        print(f"  norm²=41/81: {res['norm_sq_41_81']} · MPS 독립수축 exact 일치: {res['mps_reference_exact_match']:.2e} · bond 청정: {res['bond_wire_clean']:.2e}", flush=True)
        print(f"  parent-H P⁽²⁾ 소멸(3 bond): {['%.1e' % v for v in res['parent_H_P2_violations']]} · site singlet 성분: {['%.1e' % v for v in res['site_singlet_components']]}", flush=True)
        print(f"  string order: {res['string_order_value']:.6f} (관측값) · teeth(섭동 검출·edge축퇴 MPS-구별): {res['teeth_wrong_angle_detected']}/{res['teeth_edge_state_mps_only']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"aklt_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
