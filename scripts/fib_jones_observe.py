#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fib_jones_observe — TrackHE4 P1: Fibonacci 소비층 Jones 다항식 witness (봉인=word 유니터리뿐).

봉인된 fib_fmove·fib_hopf·fib_trefoil·fib_solomon·fib_trefoil_m(braid word, module 0)에 대해:
  1. seal 링크: 신규 앱 5 + 부품 fib_braid_s1/s2.
  2. ★F-move 교차 witness: sealed fib_braid_s2 == F·(sealed fib_braid_s1)·F — fmove golden 소비,
     회로 독립(σ₂ 정의의 재구성 경로).
  3. ★Jones 두 독립 경로 exact 일치 (규약 명시 — 닫힌형):
       경로 A(양자): 폐포 불변량 = (−A³)^{−w} · (d₁·Tr ρ₁ + d_τ·Tr ρ_τ)(word)/φ,
         ρ_τ = 봉인 word 유니터리(2차원 fusion 섹터), ρ₁(σᵢ)=A (1차원 섹터), d₁=1·d_τ=φ.
       경로 B(고전): Jones skein 재귀 t⁻¹V(L₊)−tV(L₋)=(t^½−t^{−½})V(L₀) — T(2,n) family,
         행렬 무관 순수 다항 재귀 (독립).
       규약: A=e^{3πi/5}·t=A⁻⁴=e^{−2πi/5}·★t^½=A⁻² 분지(주분지 √t 아님)·δ=φ.
     검증점: unknot(σ₁σ₂)==1 · T(2,2/3/4)⊔O == V[n]·(−t^½−t^{−½}) · ★Markov 소멸:
       V(σ₁³σ₂ 폐포, B₃) == V(σ₁³ 폐포, B₂) == skein V(삼엽) (분리 unknot 없이 직접 일치).
  4. 닫힌형 대조: V(삼엽) == t+t³−t⁴ (본 방향성 규약; 경상=t↔t⁻¹ 명시).
  5. teeth: 섹터 가중 오염(d_τ→1) → unknot≠1 · word 교란(z5 1스텝) → 삼엽값 이탈.

정직 경계(INV-Q3, seal 아님, root 성장은 앱 5 봉인분뿐):
  - 봉인 = braid word 유니터리 5개뿐. Jones 값·Markov 정리 일반론·매듭 동치판정 = 관측.
  - 대형 링크는 표본 근사 영역 = 범위 밖. universality 정량화 = 범위 밖(기존 경계 상속).

사용: python scripts/fib_jones_observe.py [--quick]
"""
import os, sys, re, json
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".pgf", "proofs", "FIB-JONES-OBSERVE.json")

A = np.exp(3j * np.pi / 5)          # Kauffman 변수 (R 고유값 {A, −A⁻³} 와 정합)
T = A ** (-4.0)                     # Jones 변수 t = e^{−2πi/5}
ST = A ** (-2.0)                    # ★t^{1/2} 분지 = A⁻²
PHI = (1 + np.sqrt(5)) / 2


def load_golden(kind, name):
    src = open(os.path.join(ROOT, "specs", kind, name), encoding="utf-8").read()
    tag = "app_golden" if kind == "apps" else "golden"
    ns = {}
    exec(re.search(rf"```python id={tag}\n(.*?)```", src, re.S).group(1), ns)
    return ns["golden"]


def seal_link(store, sid):
    p = os.path.join(ROOT, "registry", store, f"{sid}.sealed.json")
    return os.path.exists(p) and bool(json.load(open(p, encoding="utf-8")).get("u_hash"))


def jones_quantum(word_u, n_cross, dtau=PHI):
    """경로 A: (−A³)^{−w}·(d₁·A^w + d_τ·Tr U)/φ — 섹터 가중 Markov trace."""
    br = (1.0 * A ** n_cross + dtau * np.trace(word_u)) / PHI
    return (-A ** 3) ** (-float(n_cross)) * br


def jones_skein(n):
    """경로 B: T(2,n) skein 재귀 (행렬 무관 독립). V[0]=unlink₂, V[1]=unknot."""
    V = {0: -ST - 1 / ST, 1: 1.0 + 0j}
    for k in range(2, n + 1):
        V[k] = T * ((ST - 1 / ST) * V[k - 1] + T * V[k - 2])
    return V[n]


def observe():
    apps = ["fib_fmove", "fib_hopf", "fib_trefoil", "fib_solomon", "fib_trefoil_m"]
    seal_ok = all(seal_link("apps", a) for a in apps) and all(
        seal_link("apps", a) for a in ["fib_braid_s1", "fib_braid_s2"])

    s1 = load_golden("apps", "fib_braid_s1.app.pg")
    s2 = load_golden("apps", "fib_braid_s2.app.pg")
    F = load_golden("apps", "fib_fmove.app.pg")
    G = {a: load_golden("apps", f"{a}.app.pg") for a in apps[1:]}

    # 2. F-move 교차 witness (σ₂ 재구성 — fmove 소비)
    fmove_ok = bool(np.allclose(F @ s1 @ F, s2, atol=1e-13)
                    and np.allclose(F @ F, np.eye(2), atol=1e-13))

    # word 골든의 부품 정합 (sub-app 복리 확인)
    comp_ok = bool(np.allclose(G["fib_hopf"], s1 @ s1, atol=1e-13)
                   and np.allclose(G["fib_trefoil"], s1 @ s1 @ s1, atol=1e-13)
                   and np.allclose(G["fib_solomon"], np.linalg.matrix_power(s1, 4), atol=1e-13)
                   and np.allclose(G["fib_trefoil_m"], s2 @ np.linalg.matrix_power(s1, 3), atol=1e-13))

    # 3. Jones 두 독립 경로
    unknot = jones_quantum(s2 @ s1, 2)                       # σ₁σ₂ 폐포 = unknot
    unknot_ok = bool(abs(unknot - 1) < 1e-10)
    split = -ST - 1 / ST                                     # ⊔O 인자 = δ (분지 규약상 +φ)
    links = {}
    for n, key in [(2, "fib_hopf"), (3, "fib_trefoil"), (4, "fib_solomon")]:
        qa = jones_quantum(G[key], n)
        qb = jones_skein(n) * split
        links[key] = {"quantum": [qa.real, qa.imag], "skein_x_split": [qb.real, qb.imag],
                      "match": bool(abs(qa - qb) < 1e-10)}
    links_ok = all(v["match"] for v in links.values())
    # Markov 소멸: σ₁³σ₂ (w=4, B₃) == 삼엽 직접
    markov = jones_quantum(G["fib_trefoil_m"], 4)
    v3 = jones_skein(3)
    markov_ok = bool(abs(markov - v3) < 1e-10)

    # 4. 닫힌형 대조
    closed_ok = bool(abs(v3 - (T + T ** 3 - T ** 4)) < 1e-12)

    # 5. teeth
    bad_w = jones_quantum(s2 @ s1, 2, dtau=1.0)              # 가중 오염 → unknot 실패
    pert = jones_quantum(np.diag([1, np.exp(1j * np.pi / 5)]) @ G["fib_trefoil"], 3)
    teeth_ok = bool(abs(bad_w - 1) > 1e-3 and abs(pert - v3) > 1e-3)

    ok = bool(seal_ok and fmove_ok and comp_ok and unknot_ok and links_ok
              and markov_ok and closed_ok and teeth_ok)
    return {"axis": "Fibonacci 소비층 — braid word → Jones 다항식 (report4 최고 합의축 6/8)",
            "seal_links_7apps": seal_ok,
            "fmove_cross_sigma2": fmove_ok,
            "word_composition_exact": comp_ok,
            "convention": {"A": "e^{3πi/5}", "t": "A⁻⁴=e^{−2πi/5}", "sqrt_t_branch": "A⁻²(주분지 아님)",
                           "weights": "(d₁,d_τ)=(1,φ) — 양자차원, /φ 정규화", "chirality": "V(삼엽)=t+t³−t⁴ (경상=t↔t⁻¹)"},
            "unknot_sigma12_eq_1": unknot_ok,
            "torus_links_quantum_vs_skein": links,
            "markov_destab_trefoil": {"quantum": [markov.real, markov.imag],
                                      "skein_V3": [v3.real, v3.imag], "match": markov_ok},
            "closed_form_V3": closed_ok,
            "teeth": {"weight_corrupt_unknot_fails": bool(abs(bad_w - 1) > 1e-3),
                      "word_perturb_trefoil_deviates": bool(abs(pert - v3) > 1e-3), "detects": teeth_ok},
            "honest_boundary": "봉인=braid word 유니터리 5개뿐(module 0). Jones 값·Markov 일반론·"
                               "매듭 동치판정=관측(INV-Q3). 대형 링크 근사·universality=범위 밖.",
            "ok": ok}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"_schema": "fib-jones-observe-v1",
                       "_note": "Fibonacci 소비층: F-move 교차 + Jones 두 독립 경로(가중 trace vs skein) "
                                "+ Markov 소멸 + teeth. 봉인=word 유니터리뿐(INV-Q3).",
                       "observation": res}, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        L, M = res["torus_links_quantum_vs_skein"], res["markov_destab_trefoil"]
        print("Fibonacci Jones 소비층 관측 (fib_fmove + word 4):", flush=True)
        print(f"  seal(7앱) {res['seal_links_7apps']} · F-move 교차 σ₂==F·σ₁·F {res['fmove_cross_sigma2']} · "
              f"word 합성 exact {res['word_composition_exact']}", flush=True)
        print(f"  unknot(σ₁σ₂)==1 {res['unknot_sigma12_eq_1']} · T(2,n)⊔O 양자↔skein "
              f"{[v['match'] for v in L.values()]}", flush=True)
        print(f"  ★Markov 소멸(σ₁³σ₂)==V(삼엽) {M['match']} · 닫힌형 t+t³−t⁴ {res['closed_form_V3']}",
              flush=True)
        print(f"  teeth: 가중오염/word교란 검출 {res['teeth']['detects']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"fib_jones_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
