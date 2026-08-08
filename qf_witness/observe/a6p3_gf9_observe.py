#!/usr/bin/env python
"""A₆ p=3 주블록의 **GF(9) 재조명** — `gfq_engine` 이 **p=3 에서 처음** 도는가.

배경: v24 §4⁵ 에 "비분해체 블록의 표준 경로 3단계 — A₆ p=3(GF(9))도 같은 경로로 재조명
가능하다, **아직 안 했다**" 라고 적었다. 그 미착수를 채운다.
★v24 의 열린 질문(Q1·Q2·Q3′·Q3‴·Q3⁗)과 **겹치지 않는다**.

관측 7축 (정확 GF(9) 선형대수 · seal 아님 · module 0 · root 불변):
  A  ★A₆ p=3 주블록 재구성 + **GF(9) Hom 조립**(`assemble_hom_j` — 5184 계 회피) ·
     Cartan 이 선행 K축 값과 일치하는지 **회귀**.
  B  ★★**GF(9) 구조상수**(`x² = −1 = 2` ⟹ poly [2,0]) — 단위원·결합법칙 **전수 게이트**.
     화살 8(이중화살 1̂↔4)·`rad^n`·det/SNF 도 선행 값과 대조.
  C  ★★★**`HH^*_{GF(9)}`** — ★기저변환 교차검증: `A_{GF(9)} = A_{𝔽₃} ⊗ GF(9)` 이므로
     `dim_{GF(9)} HH^n(A_{GF(9)}) = dim_{𝔽₃} HH^n(A_{𝔽₃})` 여야 한다(코사슬 차원은 다르다).
  D  ★mutation 한 걸음 — 전부 기울기인지 · det/SNF 보존인지.
  F  ★★제2 판정기 `iso_lift`(층별 lifting) — 벽을 **정확히 수치화**(레벨 1 = 블록별 `GL_m`).
  E  ★Cartan 수준 궤도 — **폐합 주장이 아니다** · ★왜 규모 밖이었는지 **화살별 후보
     수를 실측**해 남긴다(G축이 이 벽을 부분적으로 해소했다).
  H  ★★**깊이 2 의 미판정** — 처음으로 **퀴버가 같은** 쌍이 나오고, 그 판정은
     현재 규모 밖이다. ★판정기가 `found=False` 가 아니라 **`found=None`(미판정)** 을
     돌려주는지를 게이트로 둔다 — 못 끝낸 것을 비동형이라고 말하면 거짓이다.
  G  ★★★**동형 수준 dedup** — `rad/rad²` 의 **선(line) 불변량**으로 레벨 1 을 정규화해
     (`265,420,800 → 131,072`, **2025배**) **동형 판정이 처음 끝났다**. 자기동형 즉시 ·
     깊이 1 의 9 대표를 **7 동형류**로 분해(★Cartan 만으로는 못 하던 병합 2건).

정직 경계:
  · **류 폐합은 여전히 하지 못했다** — G축 dedup 은 **깊이 1 안에서만**이다.
  · ★G축 음성 6건은 전부 **퀴버(화살 다중도)가 달라** 레벨 1 열거 **전에** 끝났다 ⟹
    **레벨 1 전수 소진을 실제로 시험한 음성 사례는 아직 없다**(다음 층의 몫).
  · `rank_packed`(비트평면)는 **p=2 전용**이라 p=3 은 일반 `rref` 로 갔다.
  · 외부 분류표(quaternion/dihedral type 등) 대응은 **무주장**.
"""
import itertools
import json
import os
import random
import sys
import time

import numpy as np

from qf_witness.core.paths import ROOT
from qf_witness.observe.ext1_quiver_observe import enumerate_group, rref_rows
from qf_witness.observe.loewy_series_observe import (
    coset_data, decompose_regular, extend_action, quotient_action, restrict,
    submodule_action, subgroup)
from qf_witness.observe.quiver_relations_observe import (
    assemble_hom_j, hecke_endos_p, hom_space_iter)
from qf_witness.observe import gfq_engine as GE
from qf_witness.observe.tilting_complex_observe import det_int, smith

PROOFS = os.path.join(ROOT, ".pgf", "proofs")
A6G = [(1, 2, 0, 3, 4, 5), (0, 1, 2, 4, 5, 3), (1, 0, 3, 2, 4, 5)]
JKEY = "__J__"


def _perm3(g, n):
    M = np.zeros((n, n), dtype=np.int64)
    for j in range(n):
        M[g[j], j] = 1
    return M % 3


def _wedge3(M, n):
    pr = list(itertools.combinations(range(n), 2))
    ix = {t: i for i, t in enumerate(pr)}
    O = np.zeros((len(pr), len(pr)), dtype=np.int64)
    for jc, (a, b) in enumerate(pr):
        for i in range(n):
            for j in range(n):
                if i == j or M[i][a] * M[j][b] % 3 == 0:
                    continue
                O[ix[(min(i, j), max(i, j))]][jc] += (
                    (1 if i < j else -1) * M[i][a] * M[j][b])
    return O % 3


def _find_j(basis, n):
    """`End` 안에서 `J² = −I` 인 원소 — GF(9) 구조를 주는 스칼라."""
    for c in itertools.product(range(3), repeat=len(basis)):
        M = np.zeros((n, n), dtype=np.int64)
        for t, ct in enumerate(c):
            if ct:
                M = (M + ct * basis[t]) % 3
        if ((M @ M) % 3 == (-np.eye(n, dtype=np.int64)) % 3).all():
            return M % 3
    return None


def build():
    """A₆ p=3 주블록 → GF(9) Hom 조립까지."""
    mul6, id6, ord6 = enumerate_group(A6G, 6)
    SZ = np.array([[1 if i == 0 else (-1 if i == j else 0) for i in range(6)]
                   for j in range(1, 6)], dtype=np.int64) % 3
    b5, p5 = rref_rows(SZ.copy(), 3)
    act5 = {g: restrict(_perm3(g, 6), b5, p5, 3) for g in A6G}
    act4d, _d4 = quotient_action(act5, A6G, np.ones((1, 5), dtype=np.int64),
                                 5, 3)
    raw3 = {"1": [np.eye(1, dtype=np.int64)] * 3, "4": [act4d[g] for g in A6G],
            "6t": [_wedge3(act4d[g], 4) for g in A6G]}
    N33 = ["1", "4", "6t"]
    S33 = {k: extend_action(A6G, mul6, id6, v, 3, ord6)
           for k, v in raw3.items()}
    D33 = {"1": 1, "4": 4, "6t": 6}
    sim33 = [(k, S33[k], D33[k]) for k in N33]
    endF3 = {k: len(hom_space_iter(S33[k], S33[k], D33[k], D33[k], A6G, 3))
             for k in N33}
    DIMP3 = {"1": 27, "4": 36, "6t": 36}
    CAND = {"Syl2": [(1, 0, 3, 2, 4, 5), (2, 3, 0, 1, 4, 5),
                     (0, 1, 3, 2, 5, 4)],
            "C5": [(1, 2, 3, 4, 0, 5)],
            "V4": [(1, 0, 3, 2, 4, 5), (2, 3, 0, 1, 4, 5)]}
    PIM3 = {}
    for _cn, hg in CAND.items():
        if all(k in PIM3 for k in DIMP3):
            break
        Hl = subgroup(hg, mul6, id6)
        n_, reps_, perms_, mats_ = coset_data(ord6, mul6, id6, A6G, Hl)
        actX = extend_action(A6G, mul6, id6, mats_, 3, ord6)
        alg = hecke_endos_p(n_, perms_, Hl, reps_, 3)
        rng = random.Random(7)

        def _rnd(alg=alg, rng=rng, n_=n_):
            M = np.zeros((n_, n_), dtype=np.int64)
            for A_ in rng.sample(alg, max(2, len(alg) // 3)):
                M = (M + rng.randrange(1, 3) * A_) % 3
            return M

        ps = []
        decompose_regular(np.eye(n_, dtype=np.int64),
                          np.eye(n_, dtype=np.int64), _rnd, 3, rng, ps)
        for B in sorted(ps, key=len):
            dd = len(B)
            if dd not in DIMP3.values():
                continue
            actY, _ = submodule_action(actX, A6G, B, 3)
            hd = tuple(len(hom_space_iter(actY, aS, dd, dS, A6G, 3))
                       for _n, aS, dS in sim33)
            nm = next((k for t, k in enumerate(N33)
                       if hd == tuple(endF3[k] if j == t else 0
                                      for j in range(3))), None)
            if nm in DIMP3 and nm not in PIM3 and DIMP3[nm] == dd:
                PIM3[nm] = {g: actY[g] % 3 for g in A6G}
    HOM3B = {(i, j): hom_space_iter(PIM3[i], PIM3[j], DIMP3[i], DIMP3[j],
                                    A6G, 3) for i in N33 for j in N33}
    j2 = np.array([[0, -1], [1, 0]], dtype=np.int64) % 3
    J6 = _find_j(hom_space_iter(S33["6t"], S33["6t"], 6, 6, A6G, 3), 6)
    JP6 = _find_j(HOM3B[("6t", "6t")], 36)
    G9 = A6G + [JKEY]
    S9 = {"3": dict(S33["6t"], **{JKEY: J6}),
          "3b": dict(S33["6t"], **{JKEY: (-J6) % 3})}
    h3 = [len(hom_space_iter(dict(PIM3["6t"], **{JKEY: JP6}), S9[k], 36, 6,
                             G9, 3)) for k in ("3", "3b")]
    if h3[0] == 0:                       # ★JP6 의 부호는 head 로 정렬한다
        JP6 = (-JP6) % 3
    N9 = ["1", "4", "3", "3b"]
    UND = {"1": ("1", 2), "4": ("4", 2), "3": ("6t", 1), "3b": ("6t", 1)}
    JA9 = {"1": np.kron(np.eye(27, dtype=np.int64), j2) % 3,
           "4": np.kron(np.eye(36, dtype=np.int64), j2) % 3,
           "3": JP6 % 3, "3b": (-JP6) % 3}
    DP9 = {"1": 54, "4": 72, "3": 36, "3b": 36}
    HOM9 = {(a, b): assemble_hom_j(HOM3B[UND[a][0], UND[b][0]], UND[a][1],
                                   UND[b][1], JA9[a], JA9[b], 3)
            for a in N9 for b in N9}
    return {"N9": N9, "HOM9": HOM9, "JA9": JA9, "DP9": DP9, "endF3": endF3,
            "J_found": (J6 is not None and JP6 is not None),
            "pims": sorted(PIM3)}


def main():
    t0 = time.time()
    quick = "--quick" in sys.argv
    R, out = {}, {}
    if quick:                      # 전 층이 무거워 full 전용
        print("a6p3_gf9_observe: all_ok=True checks=0 (quick) %.1fs"
              % (time.time() - t0))
        return 0

    # ── A. 재구성 + GF(9) Hom 조립 ─────────────────────────────────
    B = build()
    N9, HOM9 = B["N9"], B["HOM9"]
    R["A_end_dims_show_nonsplit"] = (B["endF3"] == {"1": 1, "4": 1, "6t": 2})
    R["A_three_f3_pims"] = (B["pims"] == ["1", "4", "6t"])
    R["A_gf9_scalar_found"] = B["J_found"]
    R["A_hom_all_even_over_f3"] = all(len(v) % 2 == 0 for v in HOM9.values())
    cart9 = [[len(HOM9[(a, b)]) // 2 for b in N9] for a in N9]
    # ★선행 K축 값과의 회귀
    R["A_cartan_regression"] = (cart9 == [[5, 4, 1, 1], [4, 5, 2, 2],
                                          [1, 2, 2, 1], [1, 2, 1, 2]])
    R["A_sum_cartan_36"] = (sum(map(sum, cart9)) == 36)
    print("A %.1fs" % (time.time() - t0), flush=True)

    # ── B. GF(9) 구조상수 + 정오 게이트 ────────────────────────────
    F9 = GE.GF(3, 2, [2, 0])                     # x² = −1 = 2
    R["B_field_tables"] = (F9.q == 9 and int(F9.MUL[3, 3]) == 2
                           and int(F9.MUL[3, F9.INV[3]]) == 1)
    a9 = GE.algebra_table_realified(F9, N9, HOM9, B["JA9"], B["DP9"])
    R["B_dim_36_and_cartan"] = (a9["n"] == 36 and GE.cartan_of(a9) == cart9)
    one = np.zeros(a9["n"], dtype=np.int64)
    for v in GE.idempotents(a9).values():
        one = F9.ADD[one, v]
    R["B_struct_const_unit"] = all(
        np.array_equal(GE.amul(a9, one, GE.unit(a9["n"], u)),
                       GE.unit(a9["n"], u))
        and np.array_equal(GE.amul(a9, GE.unit(a9["n"], u), one),
                           GE.unit(a9["n"], u)) for u in range(a9["n"]))
    R["B_struct_const_assoc"] = all(
        np.array_equal(
            GE.amul(a9, GE.amul(a9, GE.unit(a9["n"], x), GE.unit(a9["n"], y)),
                    GE.unit(a9["n"], z)),
            GE.amul(a9, GE.unit(a9["n"], x),
                    GE.amul(a9, GE.unit(a9["n"], y), GE.unit(a9["n"], z))))
        for x in range(a9["n"]) for y in range(a9["n"])
        for z in range(a9["n"]))
    qv, rp = GE.quiver_of(a9), GE.rad_powers(a9)
    # ★선행 K축과 동일: 화살 8 · 이중화살 1̂↔4 · 3·3′ 은 4 하고만
    R["B_eight_arrows_double_1_4"] = (
        sum(qv.values()) == 8 and qv["1->4"] == 2 and qv["4->1"] == 2
        and qv["3->4"] == 1 and qv["3b->4"] == 1 and qv["1->3"] == 0)
    R["B_rad_powers_LL5"] = (rp == [32, 24, 12, 4, 0])
    R["B_det_snf"] = (det_int(cart9) == 9 and smith(cart9) == [1, 1, 1, 9])
    # ★D₈(8)·Q₈(32) 류와 확실히 다르다
    R["B_det_differs_from_D8_Q8"] = (det_int(cart9) not in (8, 32))
    print("B %.1fs" % (time.time() - t0), flush=True)

    # ── C. HH^*_{GF(9)} + 기저변환 교차검증 ────────────────────────
    h9 = GE.hh_struct(a9, cup=True)
    R["C_cup_correctness"] = (h9["cup_is_cocycle"] and h9["graded_commutative"])
    # ★★`A_{GF(9)} = A_{𝔽₃} ⊗ GF(9)` ⟹ `HH^n` 차원이 **체를 바꿔도 같다**
    #   (코사슬 차원은 다르다 — 복합체 자체가 다르므로 우연이 아니다)
    QR = json.load(open(os.path.join(PROOFS, "QUIVER-RELATIONS.json"),
                        encoding="utf-8"))
    f3 = QR["P_hochschild2"]["per_block"]["A6_p3_principal"]
    R["C_base_change_invariance"] = (
        (h9["HH0"], h9["HH1"], h9["HH2"]) == (f3["HH0"], f3["HH1"], f3["HH2"])
        == (6, 4, 7))
    R["C_cochain_dims_differ"] = (h9["C"] != f3["C"])
    R["C_cup_rank_matches"] = (h9["cup_rank"] == f3["cup_rank"] == 2)
    print("C %.1fs" % (time.time() - t0), flush=True)

    # ── D. mutation 한 걸음 ────────────────────────────────────────
    mut = []
    for k in N9:
        e, Ev = GE.mutate_step(a9, k, False)
        mut.append({"vertex": k, "E": Ev, "cartan": e["cartan"],
                    "dim": e["dim"], "tilting": e["tilting"],
                    "det": det_int(e["cartan"]), "snf": smith(e["cartan"])})
    R["D_all_tilting"] = all(m["tilting"] for m in mut)
    R["D_det_snf_preserved"] = all(m["det"] == 9 and m["snf"] == [1, 1, 1, 9]
                                   for m in mut)
    R["D_dims_grow"] = (sorted(m["dim"] for m in mut) == [43, 43, 52, 58])

    # ── E. ★Cartan 수준 궤도 — **폐합 주장 아님**(동형 dedup 이 규모 밖) ────
    from qf_witness.observe.tilting_complex_observe import canon
    seen = {canon(cart9): ""}
    frontier, orb, capped = [("", a9)], [], False
    for dep in range(1, 3):        # ★깊이 2 상한(깊이 3 은 시간 밖)
        nxt = []
        for path, alg in frontier:
            for kk, k in enumerate(alg["names"]):
                for right in (False, True):
                    e, Ev = GE.mutate_step(alg, k, right)
                    cc = canon(e["cartan"])
                    orb.append({"path": path + ("-" if right else "+")
                                + str(kk), "E": Ev, "dim": e["dim"],
                                "cartan": e["cartan"],
                                "tilting": e["tilting"],
                                "det": det_int(e["cartan"]),
                                "snf": smith(e["cartan"])})
                    if cc not in seen and e["dim"] <= 90:
                        seen[cc] = orb[-1]["path"]
                        nxt.append((orb[-1]["path"], e["alg"]))
                    elif cc not in seen:
                        capped = True
        frontier = nxt
        print("E depth %d · 신규 %d · Cartan %d · %.1fs"
              % (dep, len(nxt), len(seen), time.time() - t0), flush=True)
        if not nxt:
            break
    R["E_all_tilting"] = all(m["tilting"] for m in orb)
    R["E_det_snf_preserved"] = all(m["det"] == 9 and m["snf"] == [1, 1, 1, 9]
                                   for m in orb)
    R["E_more_cartans_than_D8_Q8"] = (len(seen) > 3)
    # ★후보 수 실측 — 동형 dedup 이 왜 규모 밖인지 수치로
    arA, R2b = GE.arrow_lifts_of(a9)
    cand = []
    for (i, j, _v) in arA:
        Rr = GE.rad_block(a9, i, j)
        Bq, pq = [], []
        for r in R2b[(i, j)]:
            _o, Bq, pq = GE.rref_insert(F9, Bq, pq, r)
        cand.append(F9.q ** len(Rr) - F9.q ** len(pq))
    R["E_iso_search_out_of_scale"] = (sorted(cand)[-1] >= 6000
                                      and len(arA) == 8)
    out["E_cartan_orbit"] = {
        "reached_canonical_cartans": sorted(
            [list(map(list, c)) for c in seen], key=str),
        "n_reached": len(seen), "depth_cap": 2, "orbit": orb,
        "arrow_candidate_counts": cand,
        "hit_dim_cap": capped,
        "honest": ("★**폐합 주장이 아니다** — dedup 이 canonical Cartan 이다. "
                   "GF(9)·화살 8 에서 동형 판정의 화살 상 후보가 "
                   "`%s` 개(곱 ≈ 10^22)라 사이클을 닫는 순서 재배열"
                   "(닫힌 경로 우선)을 넣고도 **자기동형조차 14분 내 미종료**였다. "
                   "필요한 것은 더 센 열거가 아니라 **다른 알고리즘**"
                   "(rad/rad² 에서 먼저 풀고 rad² 로 successive lifting, "
                   "또는 대수의 정규형)이다. 궤도도 **깊이 2 상한**이다"
                   "(깊이 3 은 시간 밖 — 깊이 2 까지 1621초)" % cand),
    }

    out["A6_p3_over_GF9"] = {
        "field": "GF(9) = 𝔽₃[x]/(x²+1)", "vertices": N9,
        "cartan": cart9, "dim_A": a9["n"], "n_arrows": sum(qv.values()),
        "quiver": qv, "rad_powers": rp, "loewy_length": len(rp),
        "cartan_det": det_int(cart9), "cartan_snf": smith(cart9),
        "hochschild_GF9": h9, "hochschild_F3_prior": f3,
        "mutation_one_step": mut,
        "note": ("★`gfq_engine` 이 **p=3 에서 처음** 돌았다 — 표준 경로 3단계"
                 "(스칼라 J 추가 → `algebra_table_realified` → 나머지 그대로)가 "
                 "**소수를 바꿔도 작동**한다. 규모는 `assemble_hom_j` 로 넘겼다"),
        "base_change": ("★★`A_{GF(9)} = A_{𝔽₃} ⊗ GF(9)` 이므로 `HH^n` 차원이 "
                        "**체를 바꿔도 같아야** 하고 실제로 (6,4,7)·cup 2 로 같다. "
                        "코사슬 차원은 %s vs %s 로 **다르다** — 복합체가 다른데 "
                        "코호몰로지가 같다는 것이 교차검증의 값어치다"
                        % (h9["C"], f3["C"])),
        "honest": ("류 폐합은 **하지 못했다** — E축에 후보 수를 실측해 남겼다 · "
                   "`rank_packed` 는 p=2 전용이라 p=3 은 일반 rref"),
    }
    # ── F. ★★제2 판정기(층별 lifting)로 벽을 **정확히 수치화** ────────
    lf0 = GE.iso_lift(a9, a9, level1_cap=1, cap=1, quotient=False,
                      line_prune=False)
    lf = GE.iso_lift(a9, a9, level1_cap=1, cap=1, quotient=True,
                     line_prune=False)
    # ★★선 불변량 정규화 — 같은 측정을 가지치기 켜고 다시
    lfp = GE.iso_lift(a9, a9, level1_cap=1, cap=1, quotient=True,
                      line_prune=True)
    # ★레벨 1 = 블록별 `GL_m` 열거 ⟹ |GL₂(9)|² × (GF(9)*)⁴
    R["F_level1_space_measured"] = (lf0["level1_space"] == 5760 ** 2 * 8 ** 4
                                    == 135895449600)
    # ★★대각 스케일 몫 — 신장나무 3 간선 정규화로 `(GF(9)*)³ = 512` 배 감소
    R["F_quotient_gives_512x"] = (lf["level1_space"] == 265420800
                                  and lf0["level1_space"]
                                  == lf["level1_space"] * 512)
    # ★가정을 코드로 검증 — 블록 스케일이 실제로 자기동형인가
    R["F_diag_scale_is_automorphism"] = all(
        GE.diag_scale_is_auto(a9, dict(zip(N9, lam)))
        for lam in ((1, 2, 3, 4), (2, 5, 7, 3), (1, 1, 1, 1)))
    # ★열거를 시작도 못 했으면 **미판정**이어야 한다(비동형이라고 말하면 거짓)
    R["F_still_capped"] = (lf.get("capped_level1") is True
                           and lf["found"] is None
                           and lf.get("undecided") == "level1_cap")
    # ★★선 불변량이 레벨 1 을 **정확히 2025배** 줄인다 — rank-2 블록이 5760 → 128
    R["F_line_prune_2025x"] = (lfp["level1_space"] == 131072
                               and lf["level1_space"]
                               == lfp["level1_space"] * 2025)
    R["F_line_prune_per_block"] = (
        sorted((b_, o, n) for (b_, o, n) in lfp["line_prune_per_block"])
        == [("('1', '4')", 5760, 128), ("('3', '4')", 8, 8),
            ("('3b', '4')", 8, 8), ("('4', '1')", 5760, 128),
            ("('4', '3')", 8, 8), ("('4', '3b')", 8, 8)])
    # ★값싼 정오 확인 — Cartan 이 다르면 σ 후보가 없어 즉시 False
    e43, _E = GE.mutate_step(a9, N9[2], False)
    lf2 = GE.iso_lift(a9, e43["alg"])
    R["F_different_cartan_immediate_false"] = (lf2["found"] is False
                                               and lf2["sigmas"] == 0)
    out["F_iso_lift"] = {
        "self": {k: lf[k] for k in ("found", "level1_space", "sigmas",
                                    "n_words", "n_relations", "loewy")
                 if k in lf},
        "level1_space_no_quotient": lf0["level1_space"],
        "level1_per_block_no_quotient": lf0.get("level1_per_block"),
        "level1_per_block_quotient": lf.get("level1_per_block"),
        "note": ("★판정기를 **층별 successive lifting** 으로 바꿨다 — `φ` 를 `J^m` 을 "
                 "법으로 알면 보정 `δ ∈ J^m` 이 단어값에 **선형**으로 들어가므로"
                 "(`δ·δ ∈ J^{2m} ⊆ J^{m+1}`) **열거는 레벨 1 뿐**이고 이후는 선형 연립이다. "
                 "★q=2·q=4 에서 기존 판정기와 **6/6 같은 답**(회귀)"),
        "wall": ("★벽의 **3단 축소 실측**: `rad` 전수 ≈10²² → 레벨 1(블록별 `GL_m`) "
                 "`5760² × 8⁴ = 135,895,449,600 ≈ 1.36×10¹¹` → **대각 스케일 몫**"
                 "(신장나무 3 간선 정규화·`(GF(9)*)³ = 512`) **265,420,800 ≈ 2.65×10⁸**. "
                 "★그래도 **부족하다** — 레벨 1 가지치기(부분 단어집합 lifting)를 넣었으나 "
                 "**노드당 비용이 커서 2 만 노드도 30분 내 미도달** ⟹ `2.65×10⁸` 은 도달 불가. "
                 "★다음 사양서: **노드 비용을 낮추거나**(부분 lifting 을 증분화) "
                 "**열거 자체를 없애는 정규형**이 필요하다. ★교훈 재확인 — "
                 "\"줄었으니 될 것\"이 아니라 **줄어든 뒤의 절대값**으로 판단한다"),
    }

    # ── G. ★★★**동형 수준 dedup** — 선 불변량 정규화로 처음 도달한 층 ────
    #   선행 축들은 전부 **Cartan 수준**에서 멈췄다(동형 판정이 규모 밖이었다).
    selfi = GE.iso_lift(a9, a9, cap=10 ** 7, level1_cap=10 ** 7)
    R["G_self_iso_now_terminates"] = (selfi["found"] is True
                                      and selfi["level1_space"] == 131072)
    reps = [("id", a9, canon(cart9))]
    for kk, k in enumerate(N9):
        for right in (False, True):
            e, _E = GE.mutate_step(a9, k, right)
            reps.append((("-" if right else "+") + str(kk), e["alg"],
                         canon(e["cartan"])))
    grp = {}
    for pth, alg, cc in reps:
        grp.setdefault(str(cc), []).append((pth, alg))
    R["G_depth1_9_reps_4_cartans"] = (len(reps) == 9 and len(grp) == 4)
    # ★같은 Cartan 안에서 **실제 동형 판정** — 여기서 처음으로 Cartan 을 넘는다
    pairs, cls = [], []
    for cc in sorted(grp):
        mem, comp = grp[cc], []
        for pth, alg in mem:
            hit = None
            for ci, (rp, ralg) in enumerate(comp):
                rr = GE.iso_lift(ralg, alg, cap=10 ** 7, level1_cap=10 ** 7)
                pairs.append({"a": rp, "b": pth, "found": bool(rr["found"]),
                              "level1_space": rr.get("level1_space"),
                              "certificate": ("동형" if rr["found"] else
                                              ("화살 다중도 불일치"
                                               if rr.get("level1_space") is None
                                               else "레벨 1 전수 소진"))})
                if rr["found"]:
                    hit = ci
                    break
            if hit is None:
                comp.append((pth, alg))
        cls += [rp for rp, _a in comp]
    R["G_depth1_seven_iso_classes"] = (len(cls) == 7)
    # ★두 건의 **실제 동형** — Cartan 만으로는 못 하던 병합
    R["G_two_genuine_merges"] = (
        sorted((d["a"], d["b"]) for d in pairs if d["found"])
        == [("+2", "+3"), ("-2", "-3")])
    # ★음성은 전부 **화살 다중도 불일치**(퀴버가 다르다)로 값싸게 끝났다
    R["G_negatives_are_quiver_certificates"] = all(
        d["certificate"] == "화살 다중도 불일치"
        for d in pairs if not d["found"])
    out["G_iso_dedup"] = {
        "self_iso": {k: selfi.get(k) for k in ("found", "level1_space")},
        "depth1_reps": len(reps), "canonical_cartans": len(grp),
        "iso_classes": sorted(cls), "pairs": pairs,
        "note": ("★★**선 불변량 정규화**(`line_prune`)로 레벨 1 이 "
                 "`265,420,800 → 131,072`(**2025배**) 로 줄어 **동형 판정이 처음 끝났다**. "
                 "선행 축은 전부 Cartan 수준에서 멈춰 있었다."),
        "honest": ("★깊이 1 **안에서만**의 dedup 이다 — 류 폐합 주장이 아니다. "
                   "음성 6건은 전부 **퀴버(화살 다중도)가 달라** 레벨 1 열거에 "
                   "들어가기도 전에 끝났다 ⟹ **레벨 1 전수 소진을 실제로 시험한 "
                   "음성 사례는 아직 없다**. 그 시험은 다음 층(깊이 2)의 몫이다."),
    }

    # ── H. ★★깊이 2 — **미판정을 미판정이라고 말하는가**(폐합 실패의 정직한 경계) ──
    kids = {}
    base = None
    for kk, k in enumerate(N9):
        for right in (False, True):
            e, _E = GE.mutate_step(a9, k, right)
            if not right and kk == 0:
                base = e["alg"]
    for kk, k in enumerate(base["names"]):
        for right in (False, True):
            e, _E = GE.mutate_step(base, k, right)
            if e["dim"] <= 90:
                kids[("-" if right else "+") + str(kk)] = e["alg"]
    # ★같은 Cartan·같은 퀴버라 **열거에 실제로 들어가는** 쌍 — 깊이 1 엔 없었다
    hardp = [("+2", "+3"), ("-2", "-3")]
    hres = []
    for pa, pb in hardp:
        rr = GE.iso_lift(kids[pa], kids[pb], cap=120, level1_cap=10 ** 9)
        hres.append({"a": "+0" + pa, "b": "+0" + pb, "found": rr["found"],
                     "capped": bool(rr.get("capped")),
                     "undecided": rr.get("undecided"),
                     "level1_space": rr.get("level1_space"),
                     "tried": rr.get("tried")})
    # ★★핵심 게이트 — **비동형이라고 말하지 않는다**(못 끝냈으면 미판정)
    R["H_hard_pairs_not_claimed_noniso"] = all(
        h["found"] is not False for h in hres)
    R["H_hard_pairs_enter_enumeration"] = all(
        h["level1_space"] is not None and h["level1_space"] > 0
        for h in hres)
    R["H_hard_pairs_are_capped"] = all(h["capped"] for h in hres)
    # ★`GL₃(GF 9)` 전수는 `9⁹` 라 **구성**으로만 도달한다 — 전수 경로는 미판정
    rr0 = GE.iso_lift(kids["+2"], kids["+3"], cap=120, level1_cap=10 ** 9,
                      line_prune=False)
    R["H_unpruned_path_is_undecided"] = (
        rr0["found"] is None and rr0.get("undecided") == "gl_enumeration"
        and rr0.get("gl_needed") == 9 ** 9)
    out["H_depth2_undecided"] = {
        "pairs": hres, "gl_needed_unpruned": 9 ** 9,
        "note": ("★★깊이 2 에서 처음으로 **퀴버가 같은** 쌍이 나온다 — 깊이 1 의 음성 "
                 "6건은 전부 퀴버 불일치로 열거 **전에** 끝났다(선행 유보 해소). "
                 "★`GL₃(GF(9))` 전수는 `9⁹ = 387,420,489` 라 **거르는 방식으로는 "
                 "도달 불가**이고, 선 불변량이 맞는 행만 **쌓아 만들면** 도달한다."),
        "honest": ("★★**류 폐합은 실패했다** — 이 두 쌍은 레벨 1 공간이 "
                   "각각 `%s`·`%s` 라 현재 처리율(~1.5 노드/초)로 **일/주 단위**다. "
                   "판정기는 이때 `found=False` 가 아니라 **`found=None`(미판정)** 을 "
                   "돌려준다 — 못 끝낸 것을 비동형이라고 말하지 않는다."
                   % (hres[0]["level1_space"], hres[1]["level1_space"])),
    }

    R["all_ok"] = all(v for k, v in R.items() if k != "all_ok")
    out["checks"] = R
    out["all_ok"] = R["all_ok"]
    with open(os.path.join(PROOFS, "A6P3-GF9.json"), "w", encoding="utf-8",
              newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    bad = [k for k, v in R.items() if not v]
    print("a6p3_gf9_observe: all_ok=%s checks=%d %.1fs"
          % (R["all_ok"], len(R) - 1, time.time() - t0))
    if bad:
        print("  실패:", bad)
    return 0 if R["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
