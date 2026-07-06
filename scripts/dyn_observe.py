#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dyn_observe — TrackHE5 P1: 정확해 동역학(dual-unitary + Floquet) witness (신규 봉인 0 관측층).

봉인된 du_gate_j8·du_brick6_t2·floquet4_uf(전부 module 0)에 대해:
  1. seal 링크 3 + golden 유니터리성.
  2. ★dual-unitarity: 시공간 재배열 행렬 Ṽ[(c,a),(d,b)]=V[(a,b),(c,d)] 가 유니터리(Ṽ†Ṽ==I exact)
     — 비-Clifford인데 시공간 양방향 유니터리인 첫 게이트. +비-Clifford 판정(V·X₀·V† ∉ Pauli).
  3. ★광원뿔 상관 두 독립 경로(무한온도 2점 함수, t=2 < n/2 창):
       경로 A(dense): C(a,x;b,0) = tr(U†·a_x·U·b₀)/2⁶ — 봉인 브릭워크 직접.
       경로 B(채널 닫힌형): 광선 위 값 == tr(M₊²(a)·b)/2, M₊(a)=½tr₁[V†(a⊗1)V] — 행렬 지수·
         브릭워크 무관 1q 채널 거듭제곱.
     검증점: ★광선 밖 전소멸(3 Pauli × 오프레이 전 위치, exact 0) + 광선 위 X:½·Y:½·Z:1 두 경로 일치.
  4. Floquet: U_F 비-Clifford 판정 + quasi-energy 스펙트럼(16 고유위상) 기록(관측) —
     Trotter 근사와 다른 '주기 구동 자체' 계층의 첫 자산.
  5. teeth: ①CNOT 재배열 비유니터리(비-DU 검출) ②비-DU 비-Clifford 게이트(YY 각 π/8 로 쌍대성
     파괴) 브릭워크 → 광원뿔 내부 오프레이 상관 생존(DU 소멸성의 이빨 — Clifford 브릭은 상관이
     희소해 부적합 판명) ③T킥 제거(Clifford화) → 비-Clifford 판정 뒤집힘.

정직 경계(INV-Q3, seal 아님, root 성장은 앱 3 봉인분뿐):
  - 봉인 = 유니터리 3개뿐. 쌍대성·상관 소멸/인수분해·quasi-energy = witness 관측.
  - 무한계 정리의 유한 적용 = t<n/2 무랩 창 한정(명시). 열화·연속구동·winding 일반론 = 범위 밖.

사용: python scripts/dyn_observe.py [--quick]
"""
import os, sys, re, json
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".pgf", "proofs", "DYN-OBSERVE.json")

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
PAULI = {"X": X, "Y": Y, "Z": Z}


def load_golden(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    ns = {}
    exec(re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1), ns)
    return ns["golden"]


def seal_link(sid):
    p = os.path.join(ROOT, "registry", "apps", f"{sid}.sealed.json")
    return os.path.exists(p) and bool(json.load(open(p, encoding="utf-8")).get("u_hash"))


def reshuffle(V):
    R = np.zeros((4, 4), dtype=complex)
    for a in range(2):
        for b in range(2):
            for c in range(2):
                for d in range(2):
                    R[(c << 1) | a, (d << 1) | b] = V[(a << 1) | b, (c << 1) | d]
    return R


def emb1(g, i, n):
    M = np.eye(1, dtype=complex)
    for q in range(n):
        M = np.kron(M, g if q == i else I2)
    return M


def emb2(g, i, j, n):
    dim = 2 ** n
    M = np.zeros((dim, dim), dtype=complex)
    for idx in range(dim):
        b = [(idx >> (n - 1 - q)) & 1 for q in range(n)]
        si = (b[i] << 1) | b[j]
        for so in range(4):
            a = g[so, si]
            if abs(a) < 1e-16:
                continue
            nb = list(b)
            nb[i], nb[j] = (so >> 1) & 1, so & 1
            oidx = 0
            for q in range(n):
                oidx = (oidx << 1) | nb[q]
            M[oidx, idx] += a
    return M


def is_pauli_mod_phase2(M):
    for P in [np.kron(a, b) for a in (I2, X, Y, Z) for b in (I2, X, Y, Z)]:
        tr = np.trace(P.conj().T @ M) / 4
        if abs(abs(tr) - 1) < 1e-9 and np.allclose(M, tr * P, atol=1e-9):
            return True
    return False


def corr(U, A, xa, B, xb, n):
    return complex(np.trace(U.conj().T @ emb1(A, xa, n) @ U @ emb1(B, xb, n)) / 2 ** n)


def Mplus(V, a):
    W = V.conj().T @ np.kron(a, I2) @ V
    out = np.zeros((2, 2), dtype=complex)
    for b_ in range(2):
        for bp in range(2):
            out[b_, bp] = sum(W[(a_ << 1) | b_, (a_ << 1) | bp] for a_ in range(2))
    return out / 2


def observe():
    links = all(seal_link(s) for s in ("du_gate_j8", "du_brick6_t2", "floquet4_uf"))
    V = load_golden("du_gate_j8.app.pg")
    U6 = load_golden("du_brick6_t2.app.pg")
    UF = load_golden("floquet4_uf.app.pg")
    unit_ok = all(np.allclose(M.conj().T @ M, np.eye(M.shape[0]), atol=1e-12)
                  for M in (V, U6, UF))

    # 2. dual-unitarity + 비-Clifford
    Rv = reshuffle(V)
    du_ok = bool(np.allclose(Rv.conj().T @ Rv, np.eye(4), atol=1e-12))
    noncliff_V = bool(not is_pauli_mod_phase2(V @ np.kron(X, I2) @ V.conj().T))

    # 3. 광원뿔 두 경로 (t=2, n=6, b 위치=0 · 광선 = x=2)
    n = 6
    ray, offray_max = {}, 0.0
    two_path = True
    for name, A in PAULI.items():
        for x in range(n):
            c = corr(U6, A, x, PAULI[name], 0, n)
            if x == 2:
                ray[name] = c
            else:
                offray_max = max(offray_max, abs(c))
        chan = complex(np.trace(Mplus(V, Mplus(V, A)) @ PAULI[name]) / 2)
        two_path &= bool(abs(ray[name] - chan) < 1e-12)
    lightcone_ok = bool(offray_max < 1e-12 and two_path
                        and abs(ray["X"] - 0.5) < 1e-12 and abs(ray["Z"] - 1.0) < 1e-12)

    # 4. Floquet: 비-Clifford + quasi-energy 기록
    Xc = UF @ emb1(X, 0, 4) @ UF.conj().T
    # 1개 Pauli 켤레가 4q Pauli 군(mod phase)에 속하는지 — 반례 1개면 비-Clifford 충분
    def is_pauli4(M):
        for i0 in "IXYZ":
            for i1 in "IXYZ":
                for i2 in "IXYZ":
                    for i3 in "IXYZ":
                        P = np.eye(1, dtype=complex)
                        for ch in (i0, i1, i2, i3):
                            P = np.kron(P, {"I": I2, "X": X, "Y": Y, "Z": Z}[ch])
                        tr = np.trace(P.conj().T @ M) / 16
                        if abs(abs(tr) - 1) < 1e-9 and np.allclose(M, tr * P, atol=1e-9):
                            return True
        return False
    noncliff_F = bool(not is_pauli4(Xc))
    qe = np.sort(np.mod(-np.angle(np.linalg.eigvals(UF)), 2 * np.pi)).tolist()

    # 5. teeth
    CNOT = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex)
    Rc = reshuffle(CNOT)
    t1 = bool(not np.allclose(Rc.conj().T @ Rc, np.eye(4), atol=1e-9))
    # 비-DU·비-Clifford 게이트: YY 각을 π/8 로 깨면(a≠π/4) 쌍대성 파괴 — e^{−iθP}=cosθ·I−i·sinθ·P
    def expP(theta, P):
        return np.cos(theta) * np.eye(4) - 1j * np.sin(theta) * P
    XX, YY, ZZ = np.kron(X, X), np.kron(Y, Y), np.kron(Z, Z)
    Vbad = expP(np.pi / 4, XX) @ expP(np.pi / 8, YY) @ expP(np.pi / 8, ZZ)
    Rb = reshuffle(Vbad)
    t2a = bool(not np.allclose(Rb.conj().T @ Rb, np.eye(4), atol=1e-9))
    Ubad = (emb2(Vbad, 1, 2, n) @ emb2(Vbad, 3, 4, n) @ emb2(Vbad, 5, 0, n)
            @ emb2(Vbad, 0, 1, n) @ emb2(Vbad, 2, 3, n) @ emb2(Vbad, 4, 5, n))
    t2 = bool(t2a and max(abs(corr(Ubad, A, x, B, 0, n))
                          for A in PAULI.values() for B in PAULI.values()
                          for x in range(n) if x != 2) > 1e-6)
    H1 = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    S1 = np.diag([1, 1j]).astype(complex)
    CZ4 = np.diag([1, 1, 1, -1]).astype(complex)
    Ucl = np.eye(16, dtype=complex)
    for (i, j) in [(0, 1), (1, 2), (2, 3), (3, 0)]:
        Ucl = emb2(CZ4, i, j, 4) @ Ucl
    for q in range(4):
        Ucl = emb1(H1 @ S1 @ H1, q, 4) @ Ucl          # T킥→S킥(Clifford화)
    t3 = bool(is_pauli4(Ucl @ emb1(X, 0, 4) @ Ucl.conj().T))
    teeth_ok = t1 and t2 and t3

    ok = bool(links and unit_ok and du_ok and noncliff_V and lightcone_ok
              and noncliff_F and teeth_ok)
    return {"axis": "정확해 동역학 — dual-unitary(시공간 쌍대) + Floquet(주기 구동) (report5 7/8)",
            "seal_links_3": links, "unitary_3": unit_ok,
            "dual_unitarity": {"reshuffle_unitary_exact": du_ok,
                               "V_nonclifford": noncliff_V,
                               "gate": "V=iSWAP†·e^{−iπ/8·ZZ} (J=π/8 — Clifford 점 회피)"},
            "lightcone_two_path": {
                "offray_all_vanish_max": offray_max,
                "ray_values": {k: [v.real, v.imag] for k, v in ray.items()},
                "channel_match_exact": bool(two_path),
                "note": "경로 A=dense 상관 vs 경로 B=1q 전달채널 M₊² 닫힌형 · t=2<n/2 무랩 창",
                "ok": lightcone_ok},
            "floquet": {"UF_nonclifford": noncliff_F,
                        "quasi_energy_over_pi": [round(q / np.pi, 9) for q in qe],
                        "note": "주기 구동 자체(근사 아님) — 스펙트럼은 관측 기록"},
            "teeth": {"cnot_not_dual_unitary": t1,
                      "nondu_brick_offray_survives": t2,
                      "clifford_kick_flips_judgement": t3},
            "honest_boundary": "봉인=유니터리 3뿐(module 0). 쌍대성·광원뿔·quasi-energy=관측(INV-Q3). "
                               "유한창 t<n/2 명시. 열화·연속구동·winding 일반론=범위 밖.",
            "ok": ok}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"_schema": "dyn-observe-v1",
                       "_note": "dual-unitary+Floquet witness: 쌍대성·광원뿔 두 경로·quasi-energy·"
                                "teeth. 봉인=유니터리뿐(INV-Q3).",
                       "observation": res}, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        d, L, t = res["dual_unitarity"], res["lightcone_two_path"], res["teeth"]
        print("정확해 동역학 witness 관측 (du_gate_j8·du_brick6_t2·floquet4_uf):", flush=True)
        print(f"  seal {res['seal_links_3']} · ★쌍대성 Ṽ†Ṽ=I {d['reshuffle_unitary_exact']} · "
              f"V 비-Clifford {d['V_nonclifford']}", flush=True)
        print(f"  ★광원뿔: 오프레이 전소멸(max {L['offray_all_vanish_max']:.1e}) · 광선 두 경로 "
              f"{L['channel_match_exact']} (X:{L['ray_values']['X'][0]:.2f}·Z:{L['ray_values']['Z'][0]:.2f})",
              flush=True)
        print(f"  Floquet 비-Clifford {res['floquet']['UF_nonclifford']} · quasi-energy 16개 기록",
              flush=True)
        print(f"  teeth: 비-DU/오프레이 생존/Clifford화 {t['cnot_not_dual_unitary']}/"
              f"{t['nondu_brick_offray_survives']}/{t['clifford_kick_flips_judgement']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"dyn_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
