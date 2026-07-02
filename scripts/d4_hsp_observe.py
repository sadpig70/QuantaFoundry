#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""d4_hsp_observe — HE H5.2′ payoff: 이면군 D₄ Hidden Subgroup 알고리즘 소비 관측 (신규 봉인 0).

봉인된 d4_mult(곱셈 오라클)·d4_qft(비아벨 Fourier)가 실제로 hidden subgroup 표본화를 구동함을 실증한다.
표준 HSP 절차의 coherent 관측:
    coset state |gH⟩ = (1/√|H|) Σ_{h∈H} |g·h⟩   (d4_mult 로 |g⟩|H⟩→|g⟩|gH⟩ 준비)
    → d4_qft(봉인) 적용 → irrep-label 측정 분포.

★HSP 본질(관측 검증):
  1. **coset 대표 g 불변**: irrep 분포가 g 에 무관(숨은 부분군 H 에만 의존) — 8개 g 전부 동일 분포.
  2. **문자론 독립참조 일치**: P(irrep χ)=(d_χ/|G|)·Σ_{h∈H} χ(h)  — d4_qft golden 없이 D₄ 지표표로 산출.
  3. **부분군 구별**: 비정규 H={e,s}(rho 0.5 포함) vs 정규 H={e,r²}(1차원 균등) 분포 상이
     — 이면군 HSP 가 격자문제와 연결되는 이유(비정규 부분군 검출). teeth: 서로 다른 H → 다른 분포.

정직 경계(INV-Q3, seal 아님, root 불변):
  - 봉인 = d4_mult·d4_qft(exact 유니터리)뿐. HSP 분포·불변성·구별성 = 관측(문자론 참조와 대조).
  - 완전한 HSP 알고리즘(다항 표본→부분군 복원 고전후처리)은 범위 밖. 신규 봉인 0.

사용: python scripts/d4_hsp_observe.py [--quick]
"""
import os, sys, re, json
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".pgf", "proofs", "D4-HSP-OBSERVE.json")

# D₄ 지표표(독립참조): 원소 g=(a,b)=r^a s^b. χ_i(a,b), χ_ρ(a,b)
def chars(a, b):
    return {"chi1": 1.0,
            "chi2": (-1.0) ** b,
            "chi3": (-1.0) ** a,
            "chi4": (-1.0) ** (a + b),
            "rho": (2 * np.cos(a * np.pi / 2) if b == 0 else 0.0)}


DIMS = {"chi1": 1, "chi2": 1, "chi3": 1, "chi4": 1, "rho": 2}
# d4_qft golden 의 행 → irrep 그룹
IRREP_ROWS = {"chi1": [0], "chi2": [1], "chi3": [4], "chi4": [5], "rho": [2, 3, 6, 7]}
ELE = [(a, b) for a in range(4) for b in range(2)]
SUBGROUPS = {"{e,s} (비정규)": [(0, 0), (0, 1)],
             "{e,r2} (정규)": [(0, 0), (2, 0)],
             "{e,r,r2,r3} (회전)": [(0, 0), (1, 0), (2, 0), (3, 0)]}


def enc(a, b):
    return (a << 1) | b


def mult(a, b, c, d):
    return ((a + (c if b == 0 else (-c) % 4)) % 4, b ^ d)


def load_golden(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    ns = {}
    exec(re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1), ns)
    return ns["golden"]


def coset_state(g, H):
    v = np.zeros(8, dtype=complex)
    for (ha, hb) in H:
        na, nb = mult(g[0], g[1], ha, hb)
        v[enc(na, nb)] += 1
    return v / np.linalg.norm(v)


def char_formula(H):
    """독립참조: P(irrep) = (d/|G|)·Σ_{h∈H} χ(h)."""
    out = {}
    for name, d in DIMS.items():
        s = sum(chars(a, b)[name] for (a, b) in H)
        out[name] = float(d / 8 * s)
    return out


def observe():
    F = load_golden("d4_qft.app.pg")
    rows = []
    all_inv, all_match = True, True
    for name, H in SUBGROUPS.items():
        dists = []
        for g in ELE:
            out = F @ coset_state(g, H)
            p = np.abs(out) ** 2
            dists.append({k: float(sum(p[r] for r in rs)) for k, rs in IRREP_ROWS.items()})
        ref = dists[0]
        g_inv = all(all(abs(d[k] - ref[k]) < 1e-9 for k in ref) for d in dists)
        formula = char_formula(H)
        match = all(abs(ref[k] - formula[k]) < 1e-9 for k in ref)
        all_inv = all_inv and g_inv
        all_match = all_match and match
        rows.append({"subgroup": name, "g_invariant": g_inv,
                     "fourier_dist": {k: round(v, 4) for k, v in ref.items()},
                     "character_formula": {k: round(v, 4) for k, v in formula.items()},
                     "matches_character_formula": match})
    # 부분군 구별 + teeth
    ds = rows[0]["fourier_dist"]; dr2 = rows[1]["fourier_dist"]
    distinguish = any(abs(ds[k] - dr2[k]) > 1e-6 for k in ds)
    ok = all_inv and all_match and distinguish
    return {"algorithm": "Dihedral D₄ Hidden Subgroup — coset state Fourier sampling",
            "sealed_assets": "d4_mult(곱셈 오라클)·d4_qft(비아벨 Fourier)",
            "per_subgroup": rows,
            "all_g_invariant": all_inv,
            "all_match_character_formula": all_match,
            "nonnormal_vs_normal_distinguishable": distinguish,
            "honest_boundary": "봉인=d4_mult·d4_qft exact 뿐. HSP 분포·불변성·구별성=관측(문자론 대조). "
                               "완전 HSP 알고리즘(표본→부분군 복원)=범위 밖. 신규 봉인 0(INV-Q3).",
            "ok": bool(ok)}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        report = {"_schema": "d4-hsp-observe-v1",
                  "_note": "이면군 D₄ HSP 소비 관측: 봉인 d4_mult·d4_qft 구동. 문자론 독립참조 대조. "
                           "신규 봉인 0(INV-Q3).",
                  "observation": res}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("이면군 D₄ Hidden Subgroup 관측 (봉인 d4_mult·d4_qft 소비):", flush=True)
        for r in res["per_subgroup"]:
            print(f"  H={r['subgroup']:18} g불변={r['g_invariant']} 문자공식일치={r['matches_character_formula']} "
                  f"dist={r['fourier_dist']}", flush=True)
        print(f"  비정규 vs 정규 구별={res['nonnormal_vs_normal_distinguishable']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"d4_hsp_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
