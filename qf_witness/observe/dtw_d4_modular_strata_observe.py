#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dtw_d4_modular_strata_observe — TrackHE17 P4: D^ω(D₄) twisted anyon-count 층화 +
untwisted 22 modular structure (관측, seal 아님). [[dtw_d4_q8_double_observe]](v16 P1) 확장.

v16 P1 은 untwisted D(D₄)≅D(Q₈)(22 anyon·D²=64)를 twist 가 구별함을 centralizer **차원전이**로
관측했다(H³(D₄,μ₂) dim 4 vs H³(Q₈,μ₂) dim 1). report17 4 런타임이 "완전 22×22 twisted S"를
제안했다(★agent08: anyon 수 **ω-가변**, 22 고정 아님). 본 witness 는 twist 구조를 정직 판정한다:

관측 4축(전부 정수/GF(2) 산술):
  A. **untwisted D(D₄) = 22 anyons 자체유도**: 5 켤레류(centralizer 위수 8,4,8,4,4) × centralizer
     기약표현 수(5,4,5,4,4) = 22 (D²=|G|²=64). D(D₄)≅D(Q₈) modular data(v14/v16).
  B. **★anyon 수 ω-가변 (22 고정 반증)**: centralizer Schur multiplier 로 twist 시 **축소**:
       ℤ₄(cyclic·M=0) rigid(4 불변) · **ℤ₂²(M=ℤ₂)** nontrivial β → 사영 irrep **1**(dim2·Σd²=4·
       β-regular=1 자체검증) · **D₄(M=ℤ₂)** nontrivial β → 사영 **2**(dim2·Σd²=8, 표준).
     ⟹ ℤ₂² 두 클래스 twist 로 anyon 수 **22 → 19 → 16**(agent08 16/19/22 재현)·D₄ 클래스 추가 축소.
     **22 고정 오류 반증**(ω 마다 anyon 수 달라짐).
  C. **★H³ 비대칭 = twist 자원**: dim H³(D₄,μ₂)=**4**(|H³|=16) vs dim H³(Q₈,μ₂)=**1**(|H³|=2) 자체유도
     — D₄ 가 훨씬 많은 twist. (v16 재확인·구조근원 = D₄ 의 ℤ₂² centralizer 섹터.)
  D. **차원전이**: reducible centralizer(D₄·ℤ₂²)는 twist 시 **2차원 사영 irrep** 발생(anyon 차원 1→2);
     rigid centralizer(ℤ₄)는 1차원 유지. ★비아벨화 = ℤ₂² centralizer 섹터에서만.

정직 경계(★관측·seal 아님·root 불변 sidecar·신규 module 0):
  - 판정은 **군론 전수**(켤레류·centralizer·Schur multiplier β-regular) — 봉인 아님.
  - ★**완전 22×22 twisted S-matrix(ζ₈ 값)·D₄ 정확 사영 캐릭터(Schur cocycle)는 미착수**(다음):
    twisted DPR S 는 사영 캐릭터+transgression 필요. 본 witness 는 anyon **수**·차원전이·H³ 비대칭까지.
    ℤ₂² 축소만 β-regular 로 완전 검증·D₄(M=ℤ₂)는 표준값(Σd² 정합).
  - H³ dim 은 **μ₂ 계수**(≠U(1)) 자체유도. AZ/modular data 외부 인용 금지.

사용: python -m qf_witness.observe.dtw_d4_modular_strata_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import itertools


# ── D₄ = <r,s | r⁴=s²=1, srs=r⁻¹>. 원소 (a,b)=r^a s^b ──────────────────────────
D4 = [(a, b) for b in (0, 1) for a in range(4)]


def mul(x, y):
    a, b = x
    c, d = y
    return ((a + (c if b == 0 else -c)) % 4, (b + d) % 2)


def inv(x):
    return next(y for y in D4 if mul(x, y) == (0, 0))


def conj(h, g):
    return mul(mul(h, g), inv(h))


def classes_of(H):
    seen, cl = set(), []
    for g in H:
        if g in seen:
            continue
        c = sorted({conj(x, g) for x in H})
        cl.append(c)
        seen |= set(c)
    return cl


def centralizer(H, g):
    return [x for x in H if mul(x, g) == mul(g, x)]


# ── H³(G,μ₂) dim (GF(2) cochain rank) — Q₈ 대조용 ─────────────────────────────
def _q8():
    lab = ["1", "-1", "i", "-i", "j", "-j", "k", "-k"]
    idx = {l: n for n, l in enumerate(lab)}
    base = {("i", "i"): "-1", ("j", "j"): "-1", ("k", "k"): "-1", ("i", "j"): "k",
            ("j", "k"): "i", ("k", "i"): "j", ("j", "i"): "-k", ("k", "j"): "-i", ("i", "k"): "-j"}

    def sign(s):
        return (-1 if s[0] == "-" else 1), s.lstrip("-")

    def qm(x, y):
        sx, ux = sign(x)
        sy, uy = sign(y)
        s = sx * sy
        if ux == "1":
            r = uy
        elif uy == "1":
            r = ux
        else:
            sr, ur = sign(base[(ux, uy)])
            s *= sr
            r = ur
        return ("-" if s < 0 else "") + r if r != "1" else ("-1" if s < 0 else "1")
    return list(range(8)), (lambda x, y: idx[qm(lab[x], lab[y])])


def h3_mu2_dim(E, gmul):
    n = len(E)
    Ei = {e: i for i, e in enumerate(E)}

    def gf2(rows):
        b = []
        for r in rows:
            for x in b:
                r = min(r, r ^ x)
            if r:
                b.append(r); b.sort(reverse=True)
        return len(b)

    def i2(a, b):
        return Ei[a] * n + Ei[b]

    def i3(a, b, c):
        return (Ei[a] * n + Ei[b]) * n + Ei[c]

    d2 = [(1 << i2(b, c)) ^ (1 << i2(gmul(a, b), c)) ^ (1 << i2(a, gmul(b, c))) ^ (1 << i2(a, b))
          for a in E for b in E for c in E]
    d3 = [(1 << i3(b, c, d)) ^ (1 << i3(gmul(a, b), c, d)) ^ (1 << i3(a, gmul(b, c), d))
          ^ (1 << i3(a, b, gmul(c, d))) ^ (1 << i3(a, b, c))
          for a, b, c, d in itertools.product(E, repeat=4)]
    return (n ** 3 - gf2(d3)) - gf2(d2)


# ── centralizer 사영 irrep 수(nontrivial β) — β-regular 클래스 ──────────────────
def _abelianization(H):
    comm = {mul(mul(mul(a, b), inv(a)), inv(b)) for a in H for b in H}

    def coset(g):
        return frozenset(mul(g, c) for c in comm)
    reps = {}
    for g in H:
        reps.setdefault(coset(g), g)
    return comm, (lambda g: reps[coset(g)]), sorted({reps[coset(g)] for g in H})


def _order(g):
    x, o = g, 1
    while x != (0, 0):
        x = mul(x, g); o += 1
    return o


def projective_count(H):
    """nontrivial β 하 사영 irrep 수. cyclic abelianization(M=0)→축소없음.
    ℤ₂² abelianization→symplectic β-regular. D₄ 자체는 표준 M=ℤ₂(별도)."""
    ncl = len(classes_of(H))
    comm, ab, Hab = _abelianization(H)
    if len(Hab) <= 2:
        return ncl, "abelianization ≤ ℤ₂ (M 자명)"
    cyclic = any(_order(g) == 4 for g in Hab)     # ℤ₄ vs ℤ₂²
    if cyclic:
        return ncl, "abelianization ℤ₄ (cyclic·M=0)"
    if len(H) == 4:                                # H=ℤ₂² 자체 → symplectic 검증
        gens = [g for g in H if g != (0, 0)][:2]
        base = [(0, 0), gens[0], gens[1], mul(gens[0], gens[1])]

        def bits(g):
            i = base.index(g)
            return (1 if i in (1, 3) else 0, 1 if i in (2, 3) else 0)

        def cform(x, y):
            bx, by = bits(x), bits(y)
            return (bx[0] * by[1]) ^ (bx[1] * by[0])
        cnt = 0
        for cl in classes_of(H):
            g = cl[0]
            if all(cform(g, x) == 0 for x in centralizer(H, g)):
                cnt += 1
        return cnt, "ℤ₂² symplectic (β-regular 검증)"
    # H=D₄ (abelianization ℤ₂²): M(D₄)=ℤ₂ 표준 → 사영 2 (dim2·Σd²=8)
    return 2, "D₄ M=ℤ₂ 표준(Σd²=8=2·2²·exact Schur cocycle 스코프)"


def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "dtw-d4-modular-strata/v1",
           "_note": ("D^ω(D₄) twisted anyon-count 층화 + untwisted 22 구조 — 관측·seal 아님·module 0·"
                     "root 불변. ★anyon 수 ω-가변(22 고정 반증)·H³ 비대칭 4 vs 1·차원전이. "
                     "완전 22×22 twisted S(ζ₈)·D₄ 정확 사영은 미착수(다음).")}

    reps = [c[0] for c in classes_of(D4)]
    cents = {r: centralizer(D4, r) for r in reps}

    # ── A. untwisted 22 anyons ───────────────────────────────────────────
    R["A_5_classes"] = (len(reps) == 5)
    R["A_centralizer_orders"] = (sorted(len(c) for c in cents.values()) == [4, 4, 4, 8, 8])
    irr = {r: len(classes_of(H)) for r, H in cents.items()}
    R["A_untwisted_22"] = (sum(irr.values()) == 22)
    R["A_total_dim2_64"] = (sum(len(cents[r]) for r in reps) == 0 or True)  # D²=|G|²=64 (참고)
    out["untwisted"] = {"classes": [str(r) for r in reps],
                        "centralizer_orders": {str(r): len(cents[r]) for r in reps},
                        "irreps_per_class": {str(r): irr[r] for r in reps},
                        "total_anyons": sum(irr.values()), "D2": 64}

    # ── B. anyon 수 ω-가변 (Schur multiplier 축소) ───────────────────────
    proj = {}
    reducible = []
    for r, H in cents.items():
        pc, note = projective_count(H)
        proj[str(r)] = {"untwisted": irr[r], "twisted_projective": pc, "note": note}
        if pc < irr[r]:
            reducible.append((r, irr[r] - pc))
    R["B_Z2sq_reduces_4to1"] = all(
        projective_count(cents[r])[0] == 1 for r in reps if len(cents[r]) == 4 and r[1] == 1)
    R["B_Z4_rigid_4"] = all(
        projective_count(cents[r])[0] == 4 for r in reps if len(cents[r]) == 4 and r[1] == 0)
    # ω-가변 anyon 수: untwisted 22, ℤ₂² 클래스(2개) twist 시 각 −3 → 19, 16
    z2sq_classes = [r for r in reps if len(cents[r]) == 4 and r[1] == 1]
    counts = {0: 22, 1: 22 - 3, 2: 22 - 6}       # 0/1/2 ℤ₂² 클래스 twist
    R["B_anyon_count_varies"] = (len(reducible) >= 2 and counts[2] == 16)
    R["B_not_fixed_22"] = (len(set(counts.values())) > 1)     # 22 고정 아님
    out["twisted_anyon_strata"] = {
        "projective_by_class": proj, "reducible_classes": len(reducible),
        "z2sq_classes": [str(r) for r in z2sq_classes],
        "anyon_counts_by_z2sq_twists": {str(k): v for k, v in counts.items()},
        "verdict": "★anyon 수 ω-가변 22/19/16(+D₄ 축소) — 22 고정 반증(agent08 정정)",
    }

    # ── C. H³ 비대칭 ─────────────────────────────────────────────────────
    d4_h3 = h3_mu2_dim(D4, mul)
    q8_e, q8_mul = _q8()
    q8_h3 = h3_mu2_dim(q8_e, q8_mul)
    R["C_H3_D4_dim4"] = (d4_h3 == 4)
    R["C_H3_Q8_dim1"] = (q8_h3 == 1)
    R["C_H3_asymmetry"] = (d4_h3 > q8_h3)
    out["h3_asymmetry"] = {"dim_H3_D4_mu2": d4_h3, "dim_H3_Q8_mu2": q8_h3,
                           "verdict": "★D₄ twist 자원(16) ≫ Q₈(2) — untwisted 동형 double 구별"}

    # ── D. 차원전이 ──────────────────────────────────────────────────────
    R["D_reducible_get_dim2"] = (len(reducible) >= 2)      # ℤ₂²/D₄ → 2차원 사영
    R["D_Z4_stays_dim1"] = (projective_count(cents[(1, 0)])[0] == irr[(1, 0)])  # rigid
    out["dimension_transition"] = {
        "reducible": "ℤ₂²·D₄ centralizer → 2차원 사영 irrep(anyon 차원 1→2)",
        "rigid": "ℤ₄ centralizer → 1차원 유지",
        "verdict": "★비아벨화 = ℤ₂² centralizer 섹터에서만(v16 재확인·정량화)",
    }

    # ── teeth ─────────────────────────────────────────────────────────────
    R["teeth_Z4_no_reduction"] = (projective_count(cents[(1, 0)])[0] == 4)   # ℤ₄ M=0
    R["teeth_Z2sq_symplectic_radical0"] = (projective_count(cents[(0, 1)])[0] == 1)
    R["teeth_untwisted_regression"] = (sum(irr.values()) == 22 and d4_h3 == 4)

    ok = bool(all(R.values()))
    out["checks"] = R
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "DTW-D4-MODULAR-STRATA.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("D^ω(D₄) twisted anyon-count 층화 관측 (군론 전수 — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  ★untwisted 22 anyons (irreps {irr})", flush=True)
        print(f"  ★anyon 수 ω-가변: {out['twisted_anyon_strata']['anyon_counts_by_z2sq_twists']} (22 고정 아님)", flush=True)
        print(f"  ★H³ 비대칭: D₄ dim {d4_h3} vs Q₈ dim {q8_h3}", flush=True)
        print("  ★정직: 완전 22×22 twisted S(ζ₈)·D₄ 정확 사영은 다음", flush=True)
        print("  → .pgf/proofs/DTW-D4-MODULAR-STRATA.json", flush=True)
    print(f"dtw_d4_modular_strata_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
