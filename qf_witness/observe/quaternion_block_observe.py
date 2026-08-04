#!/usr/bin/env python
"""결손군 **Q₈** 블록 — v23 §4 **Q3″** 착수(파이프라인이 다른 결손군에서도 도는가).

배경: 지금까지 완주한 유도동등류는 결손군이 **`D₈` 하나**뿐이었다(A₇·PSL(2,7)·A₆ 의 p=2 주블록).
v23 §4⁗ 에서 **재사용 자산 4종**(silting mutation 엔진 · `op_algebra` · `find_isomorphism` ·
구조상수판 `hh_struct`)을 계약으로 내걸었으니, **다른 결손군에서 그대로 도는지**가 실제 시험이다.

관측 4축 (정확 GF(2) 선형대수 · seal 아님 · module 0 · root 불변):
  A  `SL(2,3) = Q₈ ⋊ ℤ₃`(위수 24 · 𝔽₃² 비영벡터 8점 순열군) — Sylow-2 지문 **(8,1,6) = Q₈**
     (D₈ 은 (8,5,2)) · `Q₈` 정규(지수 3) · `G/Q₈ ≅ ℤ₃` 준동형 자체유도.
  B  ★**𝔽₄ 실현화** — `G/Q₈ ≅ ℤ₃` 이라 단순가군은 **𝔽₄ 위 1차원 3개**이고 **𝔽₂ 는 분해체가
     아니다**. `J = ω 곱`(J² = J + 1)을 **생성원에 그냥 추가**하는 트릭을 재사용
     (A₆ p=3 GF(9) 와 같은 수법 · 모든 𝔽₂ 차원 = 2 × 𝔽₄ 차원 ⟹ ÷2).
     단순가군이 전부 1차원이라 **블록이 곧 기본대수**: `dim block = ΣC = 24 = |G|`(게이트).
  C  ★`kQ₈` 자체 — 단순가군이 **자명 하나뿐**이라 𝔽₂ 가 분해체이고 **엔진 전 층**
     (`hh_struct`·cup·`mutate_step`·`find_isomorphism`)이 **한 줄도 안 고치고** 돈다.
     독립 게이트 `HH⁰ = dim Z(kQ₈) = |켤레류| = 5`.
  D  ★★종합 — **Q3″ 에 대한 첫 데이터점**과 **엔진의 진짜 전제**.

정직 경계:
  · 실현화 위에서 잰 `HH^*`·cup 은 **𝔽₂-불변량**(realified 대수의)이지 `HH^*_{𝔽₄}` 가 아니다 —
    분리해 기록한다. `dim_{𝔽₄} Z = dim_{𝔽₂} Z / 2` 만 대조 게이트로 쓴다.
  · SL(2,3) 블록의 mutation 폐합·동형 판정은 **하지 않았다** — 엔진이 `End(S) = k`
    (분해체)를 전제하므로 실현화 위에서 돌리면 **𝔽₂-선형 동형**을 재게 되어 의미가 다르다.
  · 외부 분류표(quaternion type 등)와의 대응은 **무주장**.
"""
import json
import os
import random
import sys
import time

import numpy as np

from qf_witness.core.paths import ROOT
from qf_witness.observe.ext1_quiver_observe import enumerate_group
from qf_witness.observe.loewy_series_observe import (
    decompose_regular, subgroup, submodule_action)
from qf_witness.observe.quiver_relations_observe import (
    algebra_table, hom_space_fast)
from qf_witness.observe.tilting_complex_observe import (
    alg_pack, cartan_of, det_int, elem_order, find_isomorphism, hh_struct,
    mutate_step, quiver_of, rad_block, rad_powers, smith, sylow2_fingerprint)

PROOFS = os.path.join(ROOT, ".pgf", "proofs")
MW = np.array([[0, 1], [1, 1]], dtype=np.int64)      # 𝔽₄ 에서 ω 곱(J² = J + 1)


def sl23():
    """`SL(2,3)` 를 𝔽₃² 의 비영벡터 8개 위 순열군으로."""
    vec = [(a, b) for a in range(3) for b in range(3) if (a, b) != (0, 0)]
    ix = {v: i for i, v in enumerate(vec)}

    def pm(M):
        return tuple(ix[((M[0][0] * v[0] + M[0][1] * v[1]) % 3,
                         (M[1][0] * v[0] + M[1][1] * v[1]) % 3)] for v in vec)

    return [pm([[0, 2], [1, 0]]), pm([[1, 1], [0, 1]])]


def quotient_z3(ordG, mul, idp, Q8):
    """`G/Q₈ ≅ ℤ₃` 의 값 v(g) — 코셋 직접 구성 후 생성원 라벨을 1 로 정렬."""
    lab, rem, cos = {}, set(ordG), []
    while rem:
        g = min(rem)
        cs = {mul(h, g) for h in Q8}
        for x in cs:
            lab[x] = len(cos)
        cos.append(g)
        rem -= cs
    gen = next(g for g in sorted(ordG) if lab[g] != 0)
    ren = {lab[idp]: 0, lab[gen]: 1, lab[mul(gen, gen)]: 2}
    return {g: ren[lab[g]] for g in ordG}, len(cos)


def main():
    t0 = time.time()
    quick = "--quick" in sys.argv
    R, out = {}, {}

    # ── A. SL(2,3) 구성 ─────────────────────────────────────────────
    G = sl23()
    mul, idp, ordG = enumerate_group(G, 8)
    fp = sylow2_fingerprint(ordG, mul, idp)
    Q8 = subgroup([g for g in ordG if elem_order(g, mul, idp) in (1, 2, 4)],
                  mul, idp)
    V, ncos = quotient_z3(ordG, mul, idp, Q8)
    R["A_order_24"] = (len(ordG) == 24)
    # ★Q₈ 지문 (8,1,6) — D₈ (8,5,2)·ℤ₂³ (8,7,0)·ℤ₄×ℤ₂ (8,3,4) 와 갈린다
    R["A_sylow2_is_Q8"] = (tuple(fp) == (8, 1, 6))
    R["A_Q8_normal_index3"] = (len(Q8) == 8 and ncos == 3)
    R["A_quotient_is_homomorphism"] = all(
        V[mul(a, b)] == (V[a] + V[b]) % 3 for a in ordG for b in ordG)
    out["A_group"] = {"order": len(ordG), "sylow2_fingerprint": list(fp),
                      "Q8_order": len(Q8), "cosets": ncos,
                      "note": ("Sylow-2 지문 = (위수, involution 수, order-4 수) — "
                               "Q₈ (8,1,6) 는 D₈ (8,5,2) 와 즉시 갈린다")}

    # ── B. 𝔽₄ 실현화 — 단순가군·PIM·Cartan ──────────────────────────
    POW = [np.eye(2, dtype=np.int64), MW, (MW @ MW) % 2]
    GENS = list(G) + ["J"]
    NS = ["S0", "S1", "S2"]
    SIM = {}
    for k in range(3):
        act = {g: POW[(k * V[g]) % 3] for g in ordG}
        act["J"] = MW
        SIM[NS[k]] = act
    endS = [len(hom_space_fast(SIM[a], SIM[b], 2, 2, GENS, 2))
            for a in NS for b in NS]
    # ★End(S) 가 𝔽₂ 위 2차원 = 𝔽₄ ⟹ **𝔽₂ 는 분해체가 아니다**
    R["B_simples_end_is_F4"] = (endS == [2, 0, 0, 0, 2, 0, 0, 0, 2])
    n = len(ordG)
    og = sorted(ordG)
    oix = {g: i for i, g in enumerate(og)}

    def big(M2, left=None, right=None):
        A = np.zeros((2 * n, 2 * n), dtype=np.int64)
        for j, g in enumerate(og):
            i = oix[mul(left, g)] if left is not None else (
                oix[mul(g, right)] if right is not None else j)
            A[2 * i:2 * i + 2, 2 * j:2 * j + 2] = M2
        return A % 2

    ACT = {g: big(np.eye(2, dtype=np.int64), left=g) for g in ordG}
    ACT["J"] = big(MW)
    ENDO = ([big(np.eye(2, dtype=np.int64), right=h) for h in og]
            + [big(MW, right=h) for h in og])
    rng = random.Random(7)

    def _rnd():
        M = np.zeros((2 * n, 2 * n), dtype=np.int64)
        for A_ in rng.sample(ENDO, max(2, len(ENDO) // 3)):
            M = (M + A_) % 2
        return M

    ps = []
    decompose_regular(np.eye(2 * n, dtype=np.int64),
                      np.eye(2 * n, dtype=np.int64), _rnd, 2, rng, ps)
    R["B_regular_splits_three_pims"] = (sorted(len(b) for b in ps)
                                        == [16, 16, 16])
    PIM, dP, heads = {}, {}, []
    for B in sorted(ps, key=len):
        dd = len(B)
        actY, _ = submodule_action(ACT, GENS, B, 2)
        hd = tuple(len(hom_space_fast(actY, SIM[k], dd, 2, GENS, 2))
                   for k in NS)
        nm = next((k for t, k in enumerate(NS)
                   if hd == tuple(2 if j == t else 0 for j in range(3))), None)
        heads.append([dd, list(hd), nm])
        if nm and nm not in PIM:
            PIM[nm], dP[nm] = {g: actY[g] % 2 for g in GENS}, dd
    R["B_all_three_pims"] = (sorted(PIM) == NS)
    HOM = {(i, j): hom_space_fast(PIM[i], PIM[j], dP[i], dP[j], GENS, 2)
           for i in NS for j in NS}
    cf2 = [[len(HOM[(i, j)]) for j in NS] for i in NS]
    cart = [[x // 2 for x in r] for r in cf2]      # 실현화 ⟹ ÷2
    R["B_realification_doubles"] = all(x % 2 == 0 for r in cf2 for x in r)
    R["B_cartan_F4"] = (cart == [[4, 2, 2], [2, 4, 2], [2, 2, 4]])
    # ★단순가군이 전부 1차원 ⟹ 블록이 곧 기본대수 · ΣC = |G|
    R["B_sumC_equals_group_order"] = (sum(map(sum, cart)) == len(ordG) == 24)
    R["B_pim_dims_F4"] = ([dP[k] // 2 for k in NS] == [8, 8, 8])
    meta, MT, _n = algebra_table(NS, HOM, dP, 2)
    algr = alg_pack(NS, meta, MT, 2)
    q2 = quiver_of(algr)
    rp2 = rad_powers(algr)
    R["B_arrows_six_no_selfloop"] = (
        sum(q2.values()) // 2 == 6
        and all(q2["%s->%s" % (k, k)] == 0 for k in NS))
    R["B_rad_powers_F4"] = ([x // 2 for x in rp2] == [21, 15, 9, 3, 0])
    # ★★설계 예측 반증 기록: D₈ 3-단순에서 본 `det C = |D| = 8` 이 Q₈ 에서는 깨진다
    R["B_det_is_32_not_defect_order"] = (det_int(cart) == 32 != len(Q8))
    R["B_snf"] = (smith(cart) == [2, 2, 8])
    hhr = None if quick else hh_struct(algr, cup=True)
    if hhr is not None:
        # ★대조 게이트 — realified 중심의 절반 = |켤레류|
        ncls = len({tuple(sorted({mul(mul(x, g), _inv(x, mul, idp))
                                  for x in ordG})) for g in ordG})
        R["B_center_half_equals_classes"] = (hhr["HH0"] // 2 == ncls == 7)
    out["B_sl23_over_F4"] = {
        "simples": {"count": 3, "dim_F4": 1, "End": "𝔽₄ (𝔽₂ 위 2차원)"},
        "parts_head": heads, "cartan_F4": cart, "cartan_realified_F2": cf2,
        "pim_dims_F4": [dP[k] // 2 for k in NS],
        "block_dim": sum(map(sum, cart)),
        "n_arrows_F4": sum(q2.values()) // 2, "quiver_realified": q2,
        "rad_powers_F4": [x // 2 for x in rp2], "loewy_length": len(rp2),
        "cartan_det": det_int(cart), "cartan_snf": smith(cart),
        "hochschild_realified_F2": hhr,
        "honest": ("`hochschild_realified_F2` 는 **실현화 대수의 𝔽₂-불변량**이지 "
                   "`HH^*_{𝔽₄}` 가 아니다 — 중심 차원의 절반만 |켤레류| 게이트로 쓴다"),
    }

    # ── C. kQ₈ — 𝔽₂ 가 분해체인 최소 Q₈ 인스턴스(엔진 전 층) ─────────
    QG = sorted(Q8)
    qg = next([a, b] for a in QG for b in QG
              if len(subgroup([a, b], mul, idp)) == 8)
    QACT = {h: np.array([[1 if QG[i] == mul(h, QG[j]) else 0
                          for j in range(8)] for i in range(8)],
                        dtype=np.int64) for h in qg}
    QHOM = {("1", "1"): hom_space_fast(QACT, QACT, 8, 8, qg, 2)}
    qmeta, qMT, _q = algebra_table(["1"], QHOM, {"1": 8}, 2)
    qalg = alg_pack(["1"], qmeta, qMT, 2)
    qhh = hh_struct(qalg, cup=True)
    qe, qE = mutate_step(qalg, "1", False)
    R["C_kQ8_is_local_dim8"] = (qalg["n"] == 8
                                and cartan_of(qalg) == [[8]]
                                and len(rad_block(qalg, "1", "1")) == 7)
    R["C_two_selfloops"] = (quiver_of(qalg) == {"1->1": 2})
    R["C_rad_powers"] = (rad_powers(qalg) == [7, 5, 3, 1, 0])
    R["C_det_equals_defect_order"] = (det_int(cartan_of(qalg)) == 8 == len(Q8))
    # ★독립 게이트 — HH⁰ = dim Z(kQ₈) = |Q₈ 의 켤레류| = 5
    R["C_HH0_equals_conj_classes"] = (qhh["HH0"] == 5)
    R["C_cup_correctness"] = (qhh["cup_is_cocycle"]
                              and qhh["graded_commutative"])
    # ★★D₈ 층에서 네 블록 모두 유지되던 `HH¹ = HH⁰ − 2` 가 **깨진다**
    R["C_hh1_pattern_broken"] = (qhh["HH1"] == 7 != qhh["HH0"] - 2)
    # ★1 정점이라 mutation 은 P → 0(= 이동)이고 End 가 자기 자신 — 자명 폐합
    R["C_mutation_trivial_closure"] = (
        qE == [] and qe["tilting"] and qe["cartan"] == [[8]]
        and find_isomorphism(qalg, qe["alg"])["found"])
    out["C_kQ8"] = {
        "dim_A": qalg["n"], "cartan": cartan_of(qalg),
        "n_arrows": sum(quiver_of(qalg).values()),
        "rad_powers": rad_powers(qalg), "loewy_length": 5,
        "cartan_det": 8, "hochschild": qhh,
        "mutation": {"E": qE, "cartan": qe["cartan"], "dim": qe["dim"],
                     "tilting": qe["tilting"]},
        "note": ("단순가군이 자명 하나뿐이라 **𝔽₂ 가 분해체**이고 엔진 4종이 "
                 "**한 줄도 안 고치고** 돈다 — §4⁗ 자산 계약의 실제 통과"),
    }

    # ── D. 종합 — v23 Q3″ 첫 데이터점 · 엔진의 진짜 전제 ────────────
    R["D_two_predictions_refuted"] = (R["B_det_is_32_not_defect_order"]
                                      and R["C_hh1_pattern_broken"])
    out["D_synthesis"] = {
        "question": "v23 §4 Q3″ — 다른 결손군에서 같은 파이프라인이 도는가",
        "answer": ("★**엔진의 전제는 `D₈` 이 아니라 분해체였다**. `kQ₈`(𝔽₂ 가 분해체)에서는 "
                   "HH^*·cup·mutation·동형 판정이 **한 줄도 안 고치고** 돌았고, "
                   "SL(2,3)(3 단순가군)에서는 **𝔽₂ 가 분해체가 아니라** 실현화가 필요해 "
                   "Cartan·화살·rad^n 까지만 같은 의미로 간다"),
        "refutations": [
            ("`det C = |D|` — D₈ 3-단순 블록 4개에서 8 이었으나 "
             "**Q₈ 3-단순(SL(2,3))에서 32**. 일반 법칙이 아니다. "
             "★다만 kQ₈(1 단순)에서는 8 = |D| 로 성립"),
            ("`HH¹ = HH⁰ − 2` — D₈·p=3 네 블록에서 전부 유지됐으나 "
             "**kQ₈ 에서 (5,7) 로 깨진다**. 그 패턴도 그 층 특유였다"),
        ],
        "defect_group_contrast": {
            "D8_3simples": {"det_C": 8, "snf": [1, 1, 8],
                            "source": "TILTING-COMPLEX.json (A₇·PSL(2,7)·A₆)"},
            "Q8_3simples_SL23": {"det_C": det_int(cart), "snf": smith(cart)},
            "Q8_1simple_kQ8": {"det_C": 8, "snf": [8]},
        },
        "open": ("SL(2,3)·SL(2,5) 같은 **비분해체 Q₈ 블록**의 mutation 폐합·동형 판정에는 "
                 "엔진의 **𝔽_q-선형 일반화**가 필요하다(현재는 𝔽₂-선형)"),
    }

    R["all_ok"] = all(v for k, v in R.items() if k != "all_ok")
    out["checks"] = R
    out["all_ok"] = R["all_ok"]
    if not quick:
        with open(os.path.join(PROOFS, "QUATERNION-BLOCK.json"), "w",
                  encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
    bad = [k for k, v in R.items() if not v]
    print("quaternion_block_observe: all_ok=%s checks=%d%s %.1fs"
          % (R["all_ok"], len(R) - 1, " (quick)" if quick else "",
             time.time() - t0))
    if bad:
        print("  실패:", bad)
    return 0 if R["all_ok"] else 1


def _inv(x, mul, idp):
    y = x
    while mul(x, y) != idp:
        y = mul(y, x)
    return y


if __name__ == "__main__":
    sys.exit(main())
