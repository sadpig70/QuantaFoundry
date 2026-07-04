#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""szegedy_observe — HE3 H3.2: Szegedy 양자화 walk witness (신규 봉인 0).

봉인된 szegedy_2state_p12(2q)·szegedy_c4_p12(4q)에 대해:
  1. seal 링크 + golden == Szegedy 정의식 독립 재유도(P → Π_A → W) exact.
  2. ★스펙트럼 정리: W 의 고유위상 집합 ⊆ {±2·arccos λ : λ = eig(D)} (D=discriminant, 대칭 P 라 D=P)
     — Markov 스펙트럼이 walk 위상으로 양자화되는 Szegedy 핵심 정리의 exact 검증.
  3. ★정상분포 양자화: |π̃⟩ = Σ_x √π_x |x⟩|p_x⟩ 가 W 의 +1 고유벡터 (균일 π).
  4. 구조 관찰: 2-state 균일에서 W가 X⊗X(Clifford)로 닫힘 — 반사 구성의 수축(구조적 사실).
  5. teeth: 오염 P(p=0.3 비대칭화)의 Szegedy W 는 봉인 golden 과 불일치해야.

정직 경계(INV-Q3): 봉인=walk 유니터리 W(Tier-0 exact)뿐. spectral gap 증폭·hitting time 가속 등
  알고리즘 성능 주장=관측/차기(여기선 스펙트럼 관계만 exact witness). 일반(비-dyadic) P=사람게이트.

사용: python scripts/szegedy_observe.py [--quick]
"""
import os, sys, re, json
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".pgf", "proofs", "SZEGEDY-OBSERVE.json")


def load_golden(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    ns = {}
    exec(re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1), ns)
    return ns["golden"]


def seal_link(app_id):
    p = os.path.join(ROOT, "registry", "apps", f"{app_id}.sealed.json")
    return os.path.exists(p) and bool(json.load(open(p, encoding="utf-8")).get("u_hash"))


def szegedy_W(P):
    N = P.shape[0]; dim = N * N
    PI_A = np.zeros((dim, dim), dtype=complex)
    for x in range(N):
        v = np.zeros(dim, dtype=complex)
        for y in range(N):
            v[x * N + y] = np.sqrt(P[x, y])
        PI_A += np.outer(v, v.conj())
    RA = 2 * PI_A - np.eye(dim)
    S = np.zeros((dim, dim), dtype=complex)
    for x in range(N):
        for y in range(N):
            S[y * N + x, x * N + y] = 1
    return (S @ RA @ S) @ RA


def chains():
    P2 = np.full((2, 2), 0.5)
    P4 = np.zeros((4, 4))
    for x in range(4):
        P4[x, (x - 1) % 4] = 0.5
        P4[x, (x + 1) % 4] = 0.5
    return {"szegedy_2state_p12": P2, "szegedy_c4_p12": P4}


def observe():
    rows, all_ok = [], True
    for app_id, P in chains().items():
        U = load_golden(f"{app_id}.app.pg")
        W = szegedy_W(P)
        match = float(np.abs(U - W).max())
        # 스펙트럼 정리
        lam = np.linalg.eigvalsh(P)                       # D=P (대칭)
        pred = set()
        for l in lam:
            th = 2 * np.arccos(np.clip(l, -1, 1))
            pred.add(round(th, 9)); pred.add(round(-th, 9))
        pred = {round(((p + np.pi) % (2 * np.pi)) - np.pi, 6) for p in pred}
        phases = {round(((p + np.pi) % (2 * np.pi)) - np.pi, 6)
                  for p in np.angle(np.linalg.eigvals(U))}
        spectral = phases.issubset({round(x, 6) for x in pred} | {round(-np.pi, 6), round(np.pi, 6)})
        # 정상분포: 균일 π → |π̃> = Σ √(1/N)|x>|p_x>
        N = P.shape[0]
        v = np.zeros(N * N, dtype=complex)
        for x in range(N):
            for y in range(N):
                v[x * N + y] = np.sqrt(P[x, y] / N)
        stationary = float(np.abs(U @ v - v).max())
        link = seal_link(app_id)
        row = {"app": app_id, "seal_link": link, "szegedy_formula_match": match,
               "spectral_phases_subset_pm2arccos": bool(spectral),
               "stationary_plus1_eigvec_dev": stationary}
        row["ok"] = bool(link and match < 1e-12 and spectral and stationary < 1e-12)
        rows.append(row)
        all_ok = all_ok and row["ok"]
    # 구조 관찰: 2-state W == X⊗X
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    clifford_collapse = bool(np.allclose(load_golden("szegedy_2state_p12.app.pg"), np.kron(X, X)))
    # teeth: 오염 P
    Pbad = np.array([[0.7, 0.3], [0.3, 0.7]])
    teeth = bool(np.abs(szegedy_W(Pbad) - load_golden("szegedy_2state_p12.app.pg")).max() > 1e-3)
    ok = bool(all_ok and clifford_collapse and teeth)
    return {"walks": rows, "collapse_2state_to_XX_clifford": clifford_collapse,
            "teeth_wrong_P_detected": teeth,
            "sealed_assets": "szegedy_2state_p12·szegedy_c4_p12 (walk 유니터리 Tier-0 exact, "
                             "★C₄=draper_add2·reflect00 sub-app 복리, 신규 module 0)",
            "honest_boundary": "봉인=W 유니터리뿐. 스펙트럼 정리·정상벡터=witness 관측. gap 증폭/"
                               "hitting-time 성능=차기. 비-dyadic P(π/3 계열)=사람게이트.",
            "ok": ok}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"_schema": "szegedy-observe-v1",
                       "_note": "Szegedy walk witness: 정의식 재유도+스펙트럼 정리+정상벡터+teeth.",
                       "observation": res}, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("Szegedy walk witness 관측:", flush=True)
        for r in res["walks"]:
            print(f"  {r['app']:18}: seal {r['seal_link']} · 정의식 {r['szegedy_formula_match']:.1e} · "
                  f"스펙트럼 {r['spectral_phases_subset_pm2arccos']} · 정상벡터 {r['stationary_plus1_eigvec_dev']:.1e}",
                  flush=True)
        print(f"  2-state→X⊗X 수축 {res['collapse_2state_to_XX_clifford']} · teeth {res['teeth_wrong_P_detected']}",
              flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"szegedy_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
