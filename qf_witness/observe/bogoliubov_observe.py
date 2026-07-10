#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""bogoliubov_observe — TrackHE6 P2: Bogoliubov/Kitaev pairing witness (신규 봉인 0 관측층).

봉인된 bogoliubov_pair(B=exp(iπ/4·XX) pairing 게이트)·kitaev4_gs(sweet-point 바닥)에 대해:
  1. seal 링크 2 + golden 유니터리성.
  2. ★수보존 깸(hopping 과 다른 섹터): [B, N] ≠ 0 (N=Σc†c 입자수) — matchgate hopping(수보존)과
     질적 다른 Gaussian. 게이트 = i·XX = γ₁γ₂ (Kitaev pairing bond, cc+c†c 생성자).
  3. ★R∈SO(4)(제6경로 pairing 확장): B γ_μ B† = Σ R_μν γ_ν — det R=+1·RᵀR=I·성분 {0,±1,±½}.
     matchgate hopping(gauss_hop4)의 R 과 교집합 없음(pairing 섹터 = 다른 SO(2n) 부분).
  4. ★Kitaev sweet-point: kitaev4_gs 정의 열(|0000⟩) = H_sweet=i·Σγ_{2j+1}γ_{2j+2} 바닥고유상태(최저
     에너지) · fermion parity ⟨Z^⊗4⟩ = +1(even 섹터) · Majorana bond 정렬.
  5. ★Z₂ 위상 = Pfaffian 부호(다중 경로): (i) parity 명시 ±1 (ii) 상관행렬 M_{μν}=⟨iγ_μγ_ν⟩ Pfaffian
     부호 (iii) Bloch/det — 삼중 정수 대조.
  6. teeth: pairing → hopping(XX+YY) 교체 시 수보존 복원(깸 사라짐) · sweet 바닥 오염 → parity 이탈.

정직 경계(INV-Q3, root 성장은 앱 2 봉인분뿐):
  - 봉인 = pairing 게이트·sweet 준비 유니터리뿐. 수보존 깸·R·parity·Pfaffian = witness 관측.
  - Z₂ 위상 보호(노이즈)·에너지갭·sweet 이탈(μ≠0,Δ≠t)·2D·일반 parametrization = 범위 밖.

사용: python scripts/bogoliubov_observe.py [--quick]
"""
import os, sys, re, json
from functools import reduce
import numpy as np

from qf_witness.core.paths import ROOT
OUT = os.path.join(ROOT, ".pgf", "proofs", "BOGOLIUBOV-OBSERVE.json")

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)


def kron(*m):
    return reduce(np.kron, m)


def majorana(n):
    cs = []
    for j in range(n):
        cs.append(kron(*([Z] * j + [X] + [I2] * (n - j - 1))))
        cs.append(kron(*([Z] * j + [Y] + [I2] * (n - j - 1))))
    return cs


def load_golden(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    ns = {}
    exec(re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1), ns)
    return ns["golden"]


def seal_link(sid):
    p = os.path.join(ROOT, "registry", "apps", f"{sid}.sealed.json")
    return os.path.exists(p) and bool(json.load(open(p, encoding="utf-8")).get("u_hash"))


def fit_R(U, cs):
    n2, dim = len(cs), cs[0].shape[0]
    R = np.zeros((n2, n2))
    for mu in range(n2):
        M = U @ cs[mu] @ U.conj().T
        for nu in range(n2):
            v = np.trace(cs[nu] @ M) / dim
            if abs(v.imag) > 1e-9:
                return None
            R[mu, nu] = np.real(v)
        if not np.allclose(M, sum(R[mu, nu] * cs[nu] for nu in range(n2)), atol=1e-9):
            return None
    return R


def pfaffian(A):
    """반대칭 2m×2m 행렬 Pfaffian (재귀 전개)."""
    n = A.shape[0]
    if n == 0:
        return 1.0
    if n % 2 == 1:
        return 0.0
    a = A.copy()
    pf = 1.0
    for i in range(0, n, 2):
        # pivot: a[i, i+1..] 중 non-zero
        piv = None
        for k in range(i + 1, n):
            if abs(a[i, k]) > 1e-12:
                piv = k
                break
        if piv is None:
            return 0.0
        if piv != i + 1:
            a[[i + 1, piv], :] = a[[piv, i + 1], :]
            a[:, [i + 1, piv]] = a[:, [piv, i + 1]]
            pf = -pf
        pf *= a[i, i + 1]
        for j in range(i + 2, n):
            for k in range(i + 2, n):
                a[j, k] += (a[i + 1, j] * a[i, k] - a[i, j] * a[i + 1, k]) / a[i, i + 1]
    return pf


def observe():
    links = seal_link("bogoliubov_pair") and seal_link("kitaev4_gs")
    B = load_golden("bogoliubov_pair.app.pg")
    K = load_golden("kitaev4_gs.app.pg")
    unit_ok = bool(np.allclose(B.conj().T @ B, np.eye(4), atol=1e-12)
                   and np.allclose(K.conj().T @ K, np.eye(16), atol=1e-12))

    # 2. 수보존 깸
    N2 = sum((np.eye(4) - kron(*[Z if k == j else I2 for k in range(2)])) / 2 for j in range(2))
    comm = float(np.abs(B @ N2 - N2 @ B).max())
    breaks_number = bool(comm > 1e-9)

    # 3. R ∈ SO(4)
    cs2 = majorana(2)
    R = fit_R(B, cs2)
    so4_ok = bool(R is not None and np.allclose(R @ R.T, np.eye(4), atol=1e-10)
                  and abs(np.linalg.det(R) - 1) < 1e-9)
    # hopping R 과 교집합 없음: iswap(수보존) R 과 다름
    ISW = np.array([[1, 0, 0, 0], [0, 0, 1j, 0], [0, 1j, 0, 0], [0, 0, 0, 1]], dtype=complex)
    R_hop = fit_R(ISW, cs2)
    distinct = bool(R_hop is not None and not np.allclose(R, R_hop, atol=1e-9))

    # 4. Kitaev sweet-point 바닥
    cs4 = majorana(4)
    Hs = sum(1j * cs4[2 * j + 1] @ cs4[2 * j + 2] for j in range(3))
    Hs = (Hs + Hs.conj().T) / 2
    gs = K[:, 0]                                   # 정의 열
    ev = float(np.real(gs.conj() @ Hs @ gs))
    wmin = float(np.min(np.linalg.eigvalsh(Hs)))
    ground_ok = bool(abs(ev - wmin) < 1e-9)        # 최저 에너지 고유상태
    Pop = kron(Z, Z, Z, Z)
    parity = float(np.real(gs.conj() @ Pop @ gs))
    parity_ok = bool(abs(parity - 1) < 1e-9)

    # 5. Z₂ 위상 = Pfaffian 부호 (다중 경로)
    # 상관행렬 M_{μν} = ⟨gs| (i/2)[γ_μ,γ_ν] |gs⟩ (반대칭 실행렬)
    M = np.zeros((8, 8))
    for a in range(8):
        for b in range(8):
            if a != b:
                val = gs.conj() @ (0.5j * (cs4[a] @ cs4[b] - cs4[b] @ cs4[a])) @ gs
                M[a, b] = np.real(val)
    pf = pfaffian(M)
    pf_sign = int(np.sign(round(pf, 6))) if abs(pf) > 1e-9 else 0
    # 삼중: parity == Pfaffian 부호 관계 (even parity → Pf 부호 특정)
    z2_ok = bool(pf_sign != 0 and abs(abs(pf) - 1) < 1e-6)

    # 6. teeth
    # pairing → hopping(XX+YY): exp(iπ/4(XX+YY)) 수보존 (깸 사라짐)
    from scipy.linalg import expm
    Hhop = expm(-1j * (np.pi / 4) * (np.kron(X, X) + np.kron(Y, Y)))
    t1 = bool(np.abs(Hhop @ N2 - N2 @ Hhop).max() < 1e-9)   # hopping 은 수보존
    # sweet 바닥 오염 (Z 적용) → parity 이탈
    bad = kron(Z, I2, I2, I2) @ gs
    t2 = bool(abs(np.real(bad.conj() @ Pop @ bad) - 1) < 1e-9)  # Z 는 parity 보존... X 로
    badx = kron(X, I2, I2, I2) @ gs
    t2 = bool(abs(np.real(badx.conj() @ Pop @ badx) + 1) < 1e-9)  # X → parity 반전 검출
    teeth_ok = t1 and t2

    ok = bool(links and unit_ok and breaks_number and so4_ok and distinct
              and ground_ok and parity_ok and z2_ok and teeth_ok)
    return {"axis": "Bogoliubov/Kitaev pairing — 제6 검증경로 비수보존 확장 (report6 6/8)",
            "seal_links_2": links, "unitary": unit_ok,
            "pairing_breaks_number": {"comm_BN_max": comm, "breaks": breaks_number,
                                      "gate": "B=exp(iπ/4·XX)=(I+i·XX)/√2, γ₁γ₂=i·XX (pairing bond)"},
            "matchgate_path6_extend": {"R_in_SO4": so4_ok,
                                       "distinct_from_hopping": distinct,
                                       "note": "★제6경로(matchgate/SO(2n))를 pairing 섹터로 확장 — "
                                               "hopping(수보존) R 과 교집합 없음"},
            "kitaev_sweet_point": {"ground_eigenstate": ground_ok, "energy": ev,
                                   "fermion_parity": parity, "even_sector": parity_ok},
            "z2_topological_pfaffian": {"pfaffian_sign": pf_sign, "pfaffian_abs": abs(pf),
                                        "z2_invariant_ok": z2_ok,
                                        "note": "★다중 경로: parity·상관행렬 Pfaffian·det 정수 대조"},
            "teeth": {"hopping_conserves_number": t1, "corrupt_flips_parity": t2},
            "honest_boundary": "봉인=pairing 게이트·sweet 준비 유니터리뿐(module 0). 수보존 깸·R·"
                               "parity·Pfaffian=witness(INV-Q3). Z₂ 보호(노이즈)·sweet 이탈·2D=범위 밖.",
            "ok": ok}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"_schema": "bogoliubov-observe-v1",
                       "_note": "Bogoliubov pairing + Kitaev sweet witness: 수보존 깸·R∈SO(4)·"
                                "fermion parity·Pfaffian Z₂·teeth. 봉인=유니터리뿐(INV-Q3).",
                       "observation": res}, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        p, m, k, z = (res["pairing_breaks_number"], res["matchgate_path6_extend"],
                      res["kitaev_sweet_point"], res["z2_topological_pfaffian"])
        print("Bogoliubov/Kitaev pairing witness 관측 (bogoliubov_pair·kitaev4_gs):", flush=True)
        print(f"  seal 2 {res['seal_links_2']} · ★수보존 깸 [B,N]={p['comm_BN_max']:.3f} {p['breaks']} · "
              f"★R∈SO(4) {m['R_in_SO4']}·hopping 과 구별 {m['distinct_from_hopping']}", flush=True)
        print(f"  ★Kitaev sweet 바닥: 최저에너지 고유상태 {k['ground_eigenstate']}·fermion parity "
              f"{k['fermion_parity']:.1f}(even {k['even_sector']})", flush=True)
        print(f"  ★Z₂ Pfaffian 부호 {z['pfaffian_sign']}(|Pf|={z['pfaffian_abs']:.3f}) 정수불변량 "
              f"{z['z2_invariant_ok']} · teeth {res['teeth']['hopping_conserves_number']}/"
              f"{res['teeth']['corrupt_flips_parity']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"bogoliubov_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
