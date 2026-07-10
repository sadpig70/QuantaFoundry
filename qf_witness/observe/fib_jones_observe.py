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

★TrackHE5 P5 가산 확장(기존 키 불변): 봉인된 fib_yb(σ₁σ₂σ₁)·fib_word5(σ₁²σ₂²)·
fib_fig8(σ₁σ₂⁻¹σ₁σ₂⁻¹ — 첫 비-토러스 매듭, σ⁻¹=z5³ module 0)에 대해:
  6. ★TL₃ 상태합 제3경로: Temperley-Lieb 다이어그램 대수(δ=φ, σ=A+A⁻¹e) 상태합 bracket —
     행렬·재귀 무관 순수 조합 경로. 3중 대조: 가중 trace == 상태합 == skein/닫힌형 (4 word).
  7. 값 판정: yb 폐포==V(Hopf)(Markov 소거) · ★word5 폐포==V(Hopf)² (연결합 곱법 관측!) ·
     fig8==t⁻²−t⁻¹+1−t+t² = 1−√5 (실수 — amphichiral witness).
  8. ★Alexander 정수 제3불변량(Burau reduced, 로랑 정수 산술): Δ(4₁)=−t+3−t⁻¹ ·
     Δ(삼엽, σ₁³σ₂)=t−1+t⁻¹ — Jones 와 독립 불변량 교차.
  9. ★재발견: σ₁σ₂σ₁ ≅ F (up-to-phase — 반꼬임 Δ = F-move; Δ²∝I·Δσ₁Δ⁻¹=σ₂ 정합. 오라클이
     fib_yb·fib_fmove 에 동일 u_hash 부여로 독립 확인).
  10. teeth: fig8 word 교란 → V 이탈 · δ 오염(φ→1.5) → 상태합 vs trace 불일치.

정직 경계(INV-Q3, seal 아님, root 성장은 앱 5+3 봉인분뿐):
  - 봉인 = braid word 유니터리뿐. Jones/Alexander 값·Markov 정리 일반론·매듭 동치판정 = 관측.
  - 대형 링크는 표본 근사 영역 = 범위 밖. universality 정량화 = 범위 밖(기존 경계 상속).

사용: python scripts/fib_jones_observe.py [--quick]
"""
import os, sys, re, json
import numpy as np

from qf_witness.core.paths import ROOT
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


# ── TrackHE5 P5: TL₃ 다이어그램 대수·Alexander 도우미 ─────────────────────
def _mk(*pairs):
    return frozenset(frozenset(p) for p in pairs)


TL_ID = _mk((0, 3), (1, 4), (2, 5))
TL_E1 = _mk((0, 1), (3, 4), (2, 5))
TL_E2 = _mk((1, 2), (4, 5), (0, 3))


def _tl_compose(d1, d2):
    adj = {}
    def add(u, v):
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)
    for s in d1:
        u, v = sorted(s)
        add(("a", u) if u < 3 else ("m", u - 3), ("a", v) if v < 3 else ("m", v - 3))
    for s in d2:
        u, v = sorted(s)
        add(("m", u) if u < 3 else ("b", u - 3), ("m", v) if v < 3 else ("b", v - 3))
    seen, match, loops = set(), [], 0
    for node in list(adj):
        if node in seen:
            continue
        comp, stack = [], [node]
        seen.add(node)
        while stack:
            u = stack.pop()
            comp.append(u)
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        exts = [x for x in comp if x[0] in ("a", "b")]
        if len(exts) == 0:
            loops += 1
        else:
            match.append(exts)
    enc = lambda x: x[1] if x[0] == "a" else x[1] + 3
    return _mk(*[(enc(u), enc(v)) for u, v in match]), loops


def _tl_closure_loops(d):
    adj = {}
    def add(u, v):
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)
    for s in d:
        u, v = sorted(s)
        add(u, v)
    for i in range(3):
        add(i, i + 3)
    seen, loops = set(), 0
    for node in list(adj):
        if node in seen:
            continue
        stack = [node]
        seen.add(node)
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        loops += 1
    return loops


def tl_bracket(word, delta=PHI):
    """상태합 bracket(⟨O⟩=1): σ=A·id+A⁻¹·e · σ⁻¹=A⁻¹·id+A·e — 행렬·재귀 무관 제3경로."""
    vec = {TL_ID: 1.0 + 0j}
    for c in word:
        e = TL_E1 if c in "1a" else TL_E2
        ca, cb = (A, 1 / A) if c in "12" else (1 / A, A)
        new = {}
        for d, coef in vec.items():
            for g, cc in [(TL_ID, ca), (e, cb)]:
                nd, lp = _tl_compose(d, g)
                new[nd] = new.get(nd, 0) + coef * cc * (delta ** lp)
        vec = new
    return sum(coef * delta ** (_tl_closure_loops(d) - 1) for d, coef in vec.items())


def jones_word(word, U):
    """가중 trace 경로 (역생성원 포함): w=부호합, ρ₁(σ^±)=A^±."""
    w = sum(1 if c in "12" else -1 for c in word)
    tr1 = np.prod([A if c in "12" else 1 / A for c in word])
    return (-A ** 3) ** (-float(w)) * (tr1 + PHI * np.trace(U)) / PHI


def jones_statesum(word):
    w = sum(1 if c in "12" else -1 for c in word)
    return (-A ** 3) ** (-float(w)) * tl_bracket(word)


def _lp_mul(p, q):
    r = {}
    for e1, c1 in p.items():
        for e2, c2 in q.items():
            r[e1 + e2] = r.get(e1 + e2, 0) + c1 * c2
    return {e: c for e, c in r.items() if c}


def _lp_add(p, q):
    r = dict(p)
    for e, c in q.items():
        r[e] = r.get(e, 0) + c
    return {e: c for e, c in r.items() if c}


def alexander(word):
    """reduced Burau(정수 로랑 다항) → Δ(t) 대칭 정규화 — Jones 독립 제3불변량."""
    ONE, ZERO = {0: 1}, {}
    B = {"1": [[{1: -1}, ONE], [ZERO, ONE]], "2": [[ONE, ZERO], [{1: 1}, {1: -1}]],
         "a": [[{-1: -1}, {-1: 1}], [ZERO, ONE]], "b": [[ONE, ZERO], [ONE, {-1: -1}]]}
    M = [[ONE, ZERO], [ZERO, ONE]]
    for c in word:
        N = B[c]
        M = [[_lp_add(_lp_mul(M[i][0], N[0][j]), _lp_mul(M[i][1], N[1][j]))
              for j in range(2)] for i in range(2)]
    det = _lp_add(_lp_mul(_lp_add(M[0][0], {0: -1}), _lp_add(M[1][1], {0: -1})),
                  {e: -c for e, c in _lp_mul(M[0][1], M[1][0]).items()})
    num, quo = dict(det), {}
    while num:                                    # ÷(1+t+t²) 정수 나눗셈
        lo = min(num)
        c = num[lo]
        quo[lo] = c
        for k in (0, 1, 2):
            num[lo + k] = num.get(lo + k, 0) - c
            if num[lo + k] == 0:
                del num[lo + k]
    es = sorted(quo)
    mid = -(es[0] + es[-1]) // 2
    quo = {e + mid: c for e, c in quo.items()}
    if sum(quo.values()) < 0:
        quo = {e: -c for e, c in quo.items()}
    return quo


def observe_p5(G_words):
    apps5 = ["fib_yb", "fib_word5", "fib_fig8"]
    links = all(seal_link("apps", a) for a in apps5)
    U = {a: load_golden("apps", f"{a}.app.pg") for a in apps5}

    # 9. 재발견: σ₁σ₂σ₁ ≅ F up-to-phase
    F = load_golden("apps", "fib_fmove.app.pg")
    i = np.unravel_index(np.argmax(np.abs(F)), F.shape)
    ph = U["fib_yb"][i] / F[i]
    halftwist = bool(abs(abs(ph) - 1) < 1e-12 and np.allclose(U["fib_yb"], ph * F, atol=1e-12))

    # 6. 3중 대조 (가중 trace vs TL₃ 상태합) — 신규 3 + 기봉인 삼엽 재확인
    words = {"fib_yb": "121", "fib_word5": "1122", "fib_fig8": "1b1b"}
    triple = {}
    for a, w in words.items():
        qa, qb = jones_word(w, U[a]), jones_statesum(w)
        triple[a] = bool(abs(qa - qb) < 1e-9)
    qa, qb = jones_word("1112", G_words["fib_trefoil_m"]), jones_statesum("1112")
    triple["fib_trefoil_m"] = bool(abs(qa - qb) < 1e-9)
    triple_ok = all(triple.values())

    # 7. 값 판정
    v2 = jones_skein(2)
    yb_ok = bool(abs(jones_word("121", U["fib_yb"]) - v2) < 1e-9)
    chain_ok = bool(abs(jones_word("1122", U["fib_word5"]) - v2 * v2) < 1e-9)
    v41 = T ** -2 - T ** -1 + 1 - T + T ** 2
    fig8_v = jones_word("1b1b", U["fib_fig8"])
    fig8_ok = bool(abs(fig8_v - v41) < 1e-9 and abs(fig8_v.imag) < 1e-9
                   and abs(fig8_v.real - (1 - np.sqrt(5))) < 1e-9)

    # 8. Alexander 정수 제3불변량
    alex_ok = bool(alexander("1b1b") == {-1: -1, 0: 3, 1: -1}
                   and alexander("1112") == {-1: 1, 0: -1, 1: 1})

    # 10. teeth
    zp = np.diag([1, np.exp(1j * np.pi / 5)]).astype(complex)
    t1 = bool(abs(jones_word("1b1b", zp @ U["fib_fig8"]) - v41) > 1e-3)
    t2 = bool(abs(jones_word("121", U["fib_yb"])
                  - (-A ** 3) ** (-3.0) * tl_bracket("121", delta=1.5)) > 1e-3)
    teeth5 = t1 and t2

    ok = bool(links and halftwist and triple_ok and yb_ok and chain_ok
              and fig8_ok and alex_ok and teeth5)
    return {"seal_links_3": links,
            "rediscovery_halftwist_eq_fmove": halftwist,
            "triple_path_trace_vs_statesum": triple,
            "values": {"yb_eq_hopf": yb_ok, "chain_eq_hopf_squared_connectedsum": chain_ok,
                       "fig8_closed_form_amphichiral_real": fig8_ok,
                       "fig8_value": [fig8_v.real, fig8_v.imag]},
            "alexander_integer": {"fig8": {str(k): v for k, v in alexander("1b1b").items()},
                                  "trefoil": {str(k): v for k, v in alexander("1112").items()},
                                  "ok": alex_ok},
            "teeth": {"word_perturb_V_shifts": t1, "delta_corrupt_statesum_mismatch": t2},
            "honest_boundary": "봉인=word 유니터리 3뿐(σ⁻¹=z5³ module 0). 불변량 값·연결합 곱법·"
                               "amphichirality=관측(INV-Q3).",
            "ok": ok}


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

    p5 = observe_p5(G)
    ok = bool(seal_ok and fmove_ok and comp_ok and unknot_ok and links_ok
              and markov_ok and closed_ok and teeth_ok and p5["ok"])
    return {"axis": "Fibonacci 소비층 — braid word → Jones 다항식 (report4 최고 합의축 6/8)",
            "p5_knot_deepening": p5,
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
        p5 = res["p5_knot_deepening"]
        print(f"  ★P5: 반꼬임≅F {p5['rediscovery_halftwist_eq_fmove']} · 3중경로(상태합) "
              f"{all(p5['triple_path_trace_vs_statesum'].values())} · 연결합곱법 "
              f"{p5['values']['chain_eq_hopf_squared_connectedsum']} · fig8(1−√5) "
              f"{p5['values']['fig8_closed_form_amphichiral_real']} · Alexander 정수 "
              f"{p5['alexander_integer']['ok']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"fib_jones_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
