#!/usr/bin/env python
"""결손군 **Q₈** 블록 — v23 §4 **Q3″** 착수(파이프라인이 다른 결손군에서도 도는가).

배경: 지금까지 완주한 유도동등류는 결손군이 **`D₈` 하나**뿐이었다(A₇·PSL(2,7)·A₆ 의 p=2 주블록).
v23 §4⁗ 에서 **재사용 자산 4종**(silting mutation 엔진 · `op_algebra` · `find_isomorphism` ·
구조상수판 `hh_struct`)을 계약으로 내걸었으니, **다른 결손군에서 그대로 도는지**가 실제 시험이다.

관측 8축 (정확 GF(q) 선형대수 · seal 아님 · module 0 · root 불변):
  A  `SL(2,3) = Q₈ ⋊ ℤ₃`(위수 24 · 𝔽₃² 비영벡터 8점 순열군) — Sylow-2 지문 **(8,1,6) = Q₈**
     (D₈ 은 (8,5,2)) · `Q₈` 정규(지수 3) · `G/Q₈ ≅ ℤ₃` 준동형 자체유도.
  B  ★**𝔽₄ 실현화** — `G/Q₈ ≅ ℤ₃` 이라 단순가군은 **𝔽₄ 위 1차원 3개**이고 **𝔽₂ 는 분해체가
     아니다**. `J = ω 곱`(J² = J + 1)을 **생성원에 그냥 추가**하는 트릭을 재사용
     (A₆ p=3 GF(9) 와 같은 수법 · 모든 𝔽₂ 차원 = 2 × 𝔽₄ 차원 ⟹ ÷2).
     단순가군이 전부 1차원이라 **블록이 곧 기본대수**: `dim block = ΣC = 24 = |G|`(게이트).
  C  ★`kQ₈` 자체 — 단순가군이 **자명 하나뿐**이라 𝔽₂ 가 분해체이고 **엔진 전 층**
     (`hh_struct`·cup·`mutate_step`·`find_isomorphism`)이 **한 줄도 안 고치고** 돈다.
     독립 게이트 `HH⁰ = dim Z(kQ₈) = |켤레류| = 5`.
  E  ★**GF(q) 엔진 q=2 회귀**(+ ★제2 판정기 `iso_lift` 대조) — 신규 `gfq_engine` 을 `kQ₈` 에 q=2 로 먼저 돌려
     𝔽₂ 엔진의 값(Cartan·화살·rad^n·`HH^*`·cup·mutation·동형)을 **그대로 재현**하는지 확인.
  F  ★★**SL(2,3) over GF(4)** — 계수를 GF(4) 로 올려 **벽을 뚫는다**. 𝔽₄ 구조상수를
     실물로 뽑고(단위원·결합법칙 게이트) `HH^*_{𝔽₄}`·cup·mutation 을 **𝔽₄-불변량으로** 잰다.
  G  ★★★**dim 36 대표의 정체** — F축이 도달한 대표가 `SL(2,5) = 2.A₅` 의 p=2 **주블록**임을
     Cartan 예측 + **명시 동형**으로 확정 ⟹ **SL(2,3) ~ SL(2,5) 주블록 유도동등**(결손군 Q₈).
  H  ★★★**Q₈ 류 폐합** — 양방향 mutation + **동형 dedup** BFS(가지치기로 값싸졌다) ⟹
     대표 **2개**(`SL(2,3)` dim 24 ↔ `SL(2,5)` dim 36) · 둘 다 `(HH⁰,HH¹,HH²,cup) = (7,5,5,2)`.
  D  ★★종합 — **Q3″ 에 대한 첫 데이터점**과 **엔진의 진짜 전제**.
  I  ★**엔진 순수-최적화 등가성** — `mm`/`amul`/`_wvals` 를 **최적화 이전 정의**와
     여러 체(`q = 2,3,4,5,8,9`)에서 원소별 대조. ★일부러 **`--quick` 안**에 둔다:
     공용 엔진이 바뀌면 무거운 축을 건너뛰는 배치 게이트도 **반드시 울어야** 한다.

정직 경계:
  · 실현화 위에서 잰 `HH^*`·cup 은 **𝔽₂-불변량**(realified 대수의)이지 `HH^*_{𝔽₄}` 가 아니다 —
    분리해 기록한다. `dim_{𝔽₄} Z = dim_{𝔽₂} Z / 2` 만 대조 게이트로 쓴다.
  · F축의 궤도는 **Cartan-canon dedup** 이라 **폐합 주장이 아니다** — GF(4) 에서
    `find_isomorphism` 의 화살 상 열거가 `|rad∖rad²|^{화살수}` 로 커져 동형 dedup 을 못 돌렸다.
  · G축이 dim 36 대표를 `SL(2,5)` 주블록으로 **동일시**했다(F축 유보 해소).
  · H축 폐합은 `dim ≤ 80` · 깊이 ≤ 6 **안에서의** 폐합이다.
  · ★`rank_packed`(GF(2^k) 비트평면)로 dim 36 의 `HH²`·cup 도 계산했다(선행 유보 해소).
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
from qf_witness.observe import gfq_engine as GE
from qf_witness.observe.tilting_complex_observe import (
    alg_pack, canon, cartan_of, det_int, elem_order, find_isomorphism,
    hh_struct, mutate_step, quiver_of, rad_block, rad_powers, smith,
    sylow2_fingerprint)

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


def _engine_equiv_checks():
    """★`gfq_engine` 의 벡터화가 **순수 최적화**인지 — 최적화 이전 정의와 원소별 대조.

    `mm`(축 루프) · `amul`(성분마다 `n×n` 곱) · `_wvals`(단어마다 처음부터)가 옛 정의다.
    ★값싸므로 **`--quick` 안**에서 돈다 — 공용 엔진 회귀를 배치 게이트가 놓치면 안 된다."""
    def mm_ref(F, X, Y):
        R = np.zeros((X.shape[0], Y.shape[1]), dtype=np.int64)
        for t in range(X.shape[1]):
            R = F.ADD[R, F.MUL[X[:, t][:, None], Y[t, :][None, :]]]
        return R

    def amul_ref(alg, x, y):
        F = alg["F"]
        r = np.zeros(alg["n"], dtype=np.int64)
        for u in np.nonzero(x)[0]:
            r = F.ADD[r, F.MUL[int(x[u]),
                               mm_ref(F, y[None, :], alg["MT"][u])[0]]]
        return r

    rng = random.Random(1109)                    # ★고정 시드 — 결정론
    fields = [GE.GF(2), GE.GF(3), GE.GF(5), GE.GF(2, 2, [1, 1]),
              GE.GF(3, 2, [2, 0]), GE.GF(2, 3, [1, 1, 0])]
    ok_mm = ok_am = ok_wv = True
    for F in fields:
        for (n, t, m) in [(1, 1, 1), (0, 3, 4), (3, 0, 4), (3, 4, 0),
                          (5, 7, 3), (13, 11, 9), (4, 60, 300)]:
            X = np.array([rng.randrange(F.q) for _ in range(n * t)],
                         dtype=np.int64).reshape(n, t)
            Y = np.array([rng.randrange(F.q) for _ in range(t * m)],
                         dtype=np.int64).reshape(t, m)
            ok_mm &= np.array_equal(F.mm(X, Y), mm_ref(F, X, Y))
        d = 9
        MT = np.array([rng.randrange(F.q) if rng.random() < .35 else 0
                       for _ in range(d ** 3)],
                      dtype=np.int64).reshape(d, d, d)
        alg = GE.pack(F, [0], {(0, 0): d}, MT)

        def rv(pr, F=F, d=d, rng=rng):
            return np.array([rng.randrange(F.q) if rng.random() < pr else 0
                             for _ in range(d)], dtype=np.int64)

        for _ in range(30):
            x, y = rv(.5), rv(.3)
            ok_am &= np.array_equal(GE.amul(alg, x, y), amul_ref(alg, x, y))
        IB, arB = {0: rv(1.0)}, [rv(.4) for _ in range(3)]
        words = [(0, tuple(rng.randrange(3) for _ in range(rng.randrange(4))))
                 for _ in range(30)]
        Ax = {"names": [0], "F": F}
        ok_wv &= np.array_equal(
            GE._wvals(Ax, alg, IB, [0], words, arB),
            np.array([GE._wv(Ax, alg, IB, [0], w, arB) for w in words],
                     dtype=np.int64))
    return {"I_mm_equals_reference": bool(ok_mm),
            "I_amul_equals_reference": bool(ok_am),
            "I_wvals_equals_per_word": bool(ok_wv)}


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

    # ── I. ★엔진 순수-최적화 등가성 — **quick 안**에 두는 값싼 회귀 ──
    R.update(_engine_equiv_checks())

    # ── E·F 는 full 전용(결합법칙 전수 등 무거운 게이트) ──────────────
    if quick:
        R["all_ok"] = all(v for k, v in R.items() if k != "all_ok")
        print("quaternion_block_observe: all_ok=%s checks=%d (quick) %.1fs"
              % (R["all_ok"], len(R) - 1, time.time() - t0))
        return 0 if R["all_ok"] else 1

    # ── E. ★GF(q) 엔진 **q=2 회귀** — 알려진 답이 정오 판정기 ────────
    F2 = GE.GF(2)
    g8 = GE.pack(F2, qalg["names"], qalg["cnt"], qalg["MT"])
    gq = GE.hh_struct(g8, cup=True)
    ge, gE = GE.mutate_step(g8, "1", False)
    R["E_gf2_field_tables"] = (F2.ADD.tolist() == [[0, 1], [1, 0]]
                               and F2.MUL.tolist() == [[0, 0], [0, 1]]
                               and F2.INV.tolist() == [0, 1])
    R["E_regression_cartan_quiver_rad"] = (
        GE.cartan_of(g8) == cartan_of(qalg)
        and GE.quiver_of(g8) == quiver_of(qalg)
        and GE.rad_powers(g8) == rad_powers(qalg))
    R["E_regression_hochschild"] = all(
        gq[k] == qhh[k] for k in ("C", "ker", "HH0", "HH1", "HH2",
                                  "HH1_reps", "cup_rank", "cup_is_cocycle",
                                  "graded_commutative"))
    R["E_regression_mutation"] = (
        (ge["cartan"], ge["dim"], ge["tilting"], gE)
        == (qe["cartan"], qe["dim"], qe["tilting"], qE)
        and GE.find_isomorphism(g8, ge["alg"])["found"])
    # ★★두 번째 판정기(층별 lifting)와의 대조 — 같은 답이어야 한다
    R["E_iso_lift_agrees_kQ8"] = (
        GE.iso_lift(g8, ge["alg"])["found"]
        == GE.find_isomorphism(g8, ge["alg"])["found"] is True)
    # ★★선 불변량 가지치기의 **완전성 대조** — 상을 지울 뿐이니 판정이 같아야 한다
    R["E_line_prune_verdict_agrees"] = all(
        GE.iso_lift(X, Y, line_prune=True)["found"]
        is GE.iso_lift(X, Y, line_prune=False)["found"]
        for (X, Y) in ((g8, ge["alg"]), (g8, g8), (ge["alg"], ge["alg"])))
    out["E_gfq_regression"] = {
        "target": "kQ₈ (𝔽₂ 분해체)", "gf2_engine": gq,
        "note": ("★일반 엔진을 **q=2 로 먼저 돌려** 𝔽₂ 엔진의 값을 그대로 재현하는지 "
                 "확인한 뒤에만 q=4 로 간다(A6P3HH·HHStructConst 에서 두 번 통한 패턴)")}

    # ── F. ★★SL(2,3) **over GF(4)** — 벽을 뚫는다 ────────────────────
    F4 = GE.GF(2, 2, [1, 1])                      # x² = 1 + x
    R["F_gf4_field_tables"] = (
        F4.MUL.tolist() == [[0, 0, 0, 0], [0, 1, 2, 3],
                            [0, 2, 3, 1], [0, 3, 1, 2]]
        and F4.INV.tolist() == [0, 1, 3, 2])
    Jact = {k: PIM[k]["J"] for k in NS}
    a4 = GE.algebra_table_realified(F4, NS, HOM, Jact, dP)
    one = np.zeros(a4["n"], dtype=np.int64)
    for v in GE.idempotents(a4).values():
        one = F4.ADD[one, v]
    # ★구조상수 정오 게이트 — 단위원·결합법칙
    R["F_struct_const_unit"] = all(
        np.array_equal(GE.amul(a4, one, GE.unit(a4["n"], u)),
                       GE.unit(a4["n"], u))
        and np.array_equal(GE.amul(a4, GE.unit(a4["n"], u), one),
                           GE.unit(a4["n"], u)) for u in range(a4["n"]))
    R["F_struct_const_assoc"] = all(
        np.array_equal(
            GE.amul(a4, GE.amul(a4, GE.unit(a4["n"], x), GE.unit(a4["n"], y)),
                    GE.unit(a4["n"], z)),
            GE.amul(a4, GE.unit(a4["n"], x),
                    GE.amul(a4, GE.unit(a4["n"], y), GE.unit(a4["n"], z))))
        for x in range(a4["n"]) for y in range(a4["n"])
        for z in range(a4["n"]))
    # ★𝔽₄ 층이 B축의 ÷2 결과와 일치해야 한다(독립 재유도)
    R["F_matches_halved_F2"] = (GE.cartan_of(a4) == cart
                                and a4["n"] == 24
                                and GE.rad_powers(a4) == [21, 15, 9, 3, 0]
                                and sum(GE.quiver_of(a4).values()) == 6)
    h4 = GE.hh_struct(a4, cup=True)
    R["F_HH0_equals_classes"] = (h4["HH0"] == 7)
    R["F_cup_correctness"] = (h4["cup_is_cocycle"]
                              and h4["graded_commutative"])
    # ★★예측 확인: 𝔽₄ HH 는 실현화 𝔽₂ 값의 **절반이 아니다**(복합체가 다르다)
    R["F_not_half_of_realified"] = (
        hhr is None or h4["HH2"] * 2 != hhr["HH2"])
    orb, seen = [], {canon(GE.cartan_of(a4)): ""}
    frontier = [("", a4)]
    for d in range(1, 4):
        nxt = []
        for path, a in frontier:
            for kk, k in enumerate(a["names"]):
                for right in (False, True):
                    e, Ev = GE.mutate_step(a, k, right)
                    cc = canon(e["cartan"])
                    orb.append({"path": path + ("-" if right else "+")
                                + str(kk), "E": Ev, "cartan": e["cartan"],
                                "dim": e["dim"], "tilting": e["tilting"],
                                "det": det_int(e["cartan"]),
                                "snf": smith(e["cartan"])})
                    if cc not in seen and e["dim"] <= 80:
                        seen[cc] = orb[-1]["path"]
                        nxt.append((orb[-1]["path"], e["alg"]))
        frontier = nxt
        if not nxt:
            break
    R["F_all_mutations_tilting"] = all(r["tilting"] for r in orb)
    R["F_det_snf_preserved"] = all(r["det"] == 32 and r["snf"] == [2, 2, 8]
                                   for r in orb)
    R["F_two_cartans_reached"] = (len(seen) == 2)
    out["F_sl23_over_GF4"] = {
        "field": "GF(4) = 𝔽₂[x]/(x²+x+1)", "dim_A": a4["n"],
        "cartan": GE.cartan_of(a4), "n_arrows": sum(GE.quiver_of(a4).values()),
        "rad_powers": GE.rad_powers(a4), "hochschild_F4": h4,
        "orbit": orb,
        "reached_canonical_cartans": sorted(
            [list(map(list, c)) for c in seen], key=str),
        "note": ("★★벽을 뚫었다 — 계수를 GF(4) 로 올리자 `HH^*`·cup·mutation 이 "
                 "**𝔽₄-불변량으로** 나온다. `HH^*_{𝔽₄} = (%d,%d,%d)`·cup %d 는 "
                 "실현화 𝔽₂ 값의 단순 절반이 **아니다**(복합체 자체가 다르다)"
                 % (h4["HH0"], h4["HH1"], h4["HH2"], h4["cup_rank"])),
        "honest": ("궤도는 **Cartan-canon dedup** 이라 **폐합 주장이 아니다** — "
                   "GF(4) 에서 `find_isomorphism` 의 화살 상 열거가 "
                   "`|rad∖rad²|^{화살수}` 로 커져 동형 dedup 을 못 돌렸다. "
                   "dim 36 대표의 **군 블록 동일시도 미착수**"),
    }

    # ── G. ★★★dim 36 대표의 정체 — SL(2,5) 의 p=2 주블록 ─────────────
    VEC = [(a, b) for a in range(5) for b in range(5) if (a, b) != (0, 0)]
    IX = {v: t for t, v in enumerate(VEC)}

    def pm5(M):
        return tuple(IX[((M[0][0] * v[0] + M[0][1] * v[1]) % 5,
                         (M[1][0] * v[0] + M[1][1] * v[1]) % 5)] for v in VEC)

    G5 = [pm5([[0, 4], [1, 0]]), pm5([[1, 1], [0, 1]])]
    mul5, id5, ord5 = enumerate_group(G5, 24)
    fp5 = sylow2_fingerprint(ord5, mul5, id5)
    R["G_order_120"] = (len(ord5) == 120)
    R["G_sylow2_is_Q8"] = (tuple(fp5) == (8, 1, 6))
    n5, og5 = len(ord5), sorted(ord5)
    ox5 = {g: t for t, g in enumerate(og5)}
    GN5 = list(G5) + ["J"]

    def big5(M2, left=None, right=None):
        A = np.zeros((2 * n5, 2 * n5), dtype=np.int64)
        for j, g in enumerate(og5):
            t = (ox5[mul5(left, g)] if left is not None
                 else (ox5[mul5(g, right)] if right is not None else j))
            A[2 * t:2 * t + 2, 2 * j:2 * j + 2] = M2
        return A % 2

    A5 = {g: big5(np.eye(2, dtype=np.int64), left=g) for g in G5}
    A5["J"] = big5(MW)
    E5 = ([big5(np.eye(2, dtype=np.int64), right=h) for h in og5]
          + [big5(MW, right=h) for h in og5])
    rng5 = random.Random(7)

    def _rnd5():
        M = np.zeros((2 * n5, 2 * n5), dtype=np.int64)
        for A_ in rng5.sample(E5, max(2, len(E5) // 3)):
            M = (M + A_) % 2
        return M

    p5 = []
    decompose_regular(np.eye(2 * n5, dtype=np.int64),
                      np.eye(2 * n5, dtype=np.int64), _rnd5, 2, rng5, p5)
    # ★예상 조각: P(4)×4(다른 블록) · P(2a)×2 · P(2b)×2 · P(1̂)×1
    R["G_regular_parts"] = (sorted(len(b) for b in p5)
                            == [16, 16, 16, 16, 32, 32, 32, 32, 48])
    acts5, dims5 = [], []
    for B in sorted(p5, key=len):
        a_, _ = submodule_action(A5, GN5, B, 2)
        acts5.append(a_)
        dims5.append(len(B))
    Hm = [[len(hom_space_fast(acts5[x], acts5[y], dims5[x], dims5[y], GN5, 2))
           for y in range(len(acts5))] for x in range(len(acts5))]
    # ★사영가군끼리 dim Hom = C_{S,T} ⟹ **동형이면 8(𝔽₂)·다르면 4** 로 2a·2b 를 가른다
    i2a = 4
    i2b = next(y for y in range(4, 8) if Hm[i2a][y] == 4)
    R["G_hom_separates_2a_2b"] = (Hm[i2a][i2a] == 8 and Hm[i2a][i2b] == 4
                                  and Hm[8][8] == 16)
    NS5 = ["2a", "2b", "1"]
    PIM5 = {"2a": acts5[i2a], "2b": acts5[i2b], "1": acts5[8]}
    dP5 = {"2a": dims5[i2a], "2b": dims5[i2b], "1": dims5[8]}
    HOM5 = {(x, y): hom_space_fast(PIM5[x], PIM5[y], dP5[x], dP5[y], GN5, 2)
            for x in NS5 for y in NS5}
    c5 = [[len(HOM5[(x, y)]) // 2 for y in NS5] for x in NS5]
    dimP5 = [dP5[k] // 2 for k in NS5]
    blkdim = sum(d * s for d, s in zip(dimP5, [2, 2, 1]))
    # ★★설계 예측: Cartan 이 F축이 도달한 dim 36 대표와 **정확히 일치**
    R["G_cartan_prediction"] = (c5 == [[4, 2, 4], [2, 4, 4], [4, 4, 8]])
    R["G_dimP_and_block_dim"] = (dimP5 == [16, 16, 24] and blkdim == 88
                                 and blkdim + 8 * 4 == 120)
    a25 = GE.algebra_table_realified(F4, NS5, HOM5,
                                     {k: PIM5[k]["J"] for k in NS5}, dP5)
    R["G_dim36_arrows_rad"] = (a25["n"] == 36
                               and sum(GE.quiver_of(a25).values()) == 4
                               and GE.rad_powers(a25)
                               == [33, 29, 23, 19, 15, 11, 7, 3, 0])
    tgt = next(a for a in [GE.mutate_step(a4, NS[0], False)[0]["alg"]]
               if a["n"] == 36)
    R["G_target_same_invariants"] = (
        canon(GE.cartan_of(tgt)) == canon(c5)
        and sum(GE.quiver_of(tgt).values()) == 4
        and GE.rad_powers(tgt) == GE.rad_powers(a25))
    isoG = GE.find_isomorphism(tgt, a25, cap=400000)
    # ★★★Cartan 일치는 필요조건 — **명시 동형**까지 간다(세 번째 적용)
    R["G_explicit_isomorphism"] = isoG["found"]
    # ★★독립 제2 판정기(층별 lifting)도 같은 답 — 대각 스케일 몫으로 레벨 1 공간 9
    #   (몫 전에는 81 — ★공간 수치는 **몫 정책에 따라 바뀌므로** 판정 일치를 주 게이트로 둔다)
    isoL = GE.iso_lift(tgt, a25)
    isoL0 = GE.iso_lift(tgt, a25, quotient=False)
    R["G_iso_lift_agrees"] = (isoL["found"] is True is isoL0["found"])
    # ★★양성 사례에서도 선 불변량 가지치기가 답을 잃지 않는가(GF(4)·dim 36)
    R["G_line_prune_keeps_positive"] = (
        GE.iso_lift(tgt, a25, line_prune=False)["found"] is True)
    R["G_iso_lift_quotient_9x"] = (isoL["level1_space"] == 9
                                   and isoL0["level1_space"] == 81)
    out["G_sl25_identification"] = {
        "candidate": "SL(2,5) = 2.A₅ · p=2 주블록",
        "why_this_candidate": ("도달 Cartan 에 단순차원 (2,2,1) 을 넣으면 "
                               "dim P = (16,16,24)·블록 차원 **88**. "
                               "|SL(2,5)| = 120 이고 4차원 단순가군이 든 블록"
                               "(결손군 ℤ₂·dim P = 8)이 8·4 = 32 를 채우므로 "
                               "주블록 = 120 − 32 = 88 — 정확히 일치"),
        "group": {"order": len(ord5), "sylow2_fingerprint": list(fp5),
                  "regular_parts": sorted(len(b) for b in p5),
                  "hom_matrix": Hm},
        "cartan_F4": c5, "dim_P_F4": dimP5, "block_dim": blkdim,
        "dim_A": a25["n"], "n_arrows": sum(GE.quiver_of(a25).values()),
        "rad_powers": GE.rad_powers(a25), "isomorphism": isoG, "isomorphism_lift": isoL,
        "conclusion": ("★★★F축이 SL(2,3) 에서 mutation 으로 도달한 dim 36 대표는 "
                       "**SL(2,5) 의 p=2 주블록**이다 ⟹ **SL(2,3) 과 SL(2,5) 의 "
                       "p=2 주블록이 유도동등**(결손군 Q₈) — D₈ 이야기"
                       "(PSL(2,7)·A₆·A₇)와 나란히 놓이는 **두 번째 사례**"),
        "honest": ("이 대표의 `HH^*_{𝔽₄}` 는 **재지 않았다** — dim 36·GF(4) 에서 "
                   "`C³` 규모가 현재 구현의 범위 밖이다(SL(2,3) dim 24 는 계산됨). "
                   "류의 **폐합**(동형 dedup BFS)도 여전히 미착수"),
    }

    # ── H. ★★★Q₈ 류 **폐합** — 양방향 mutation · 동형 dedup BFS ──────
    qreps = [{"label": "R0", "alg": a4, "path": "",
              "cartan": GE.cartan_of(a4)}]
    qfront, qedges, qsat = [0], [], True
    for dep in range(1, 7):
        nxt = []
        for ri in qfront:
            a = qreps[ri]["alg"]
            for kk, k in enumerate(a["names"]):
                for right in (False, True):
                    e, Ev = GE.mutate_step(a, k, right)
                    if not e["tilting"]:
                        qsat = False
                    tag = None
                    for rr in qreps:
                        if canon(rr["cartan"]) != canon(e["cartan"]):
                            continue
                        iso = GE.find_isomorphism(rr["alg"], e["alg"],
                                                  cap=400000)
                        if iso.get("capped"):
                            qsat = False       # ★상한 도달 = 미판정(폐합 주장 금지)
                        if iso["found"]:
                            tag = rr["label"]
                            break
                    if tag is None:
                        if e["dim"] > 80:
                            qsat = False
                            continue
                        tag = "R%d" % len(qreps)
                        qreps.append({"label": tag, "alg": e["alg"],
                                      "path": qreps[ri]["path"]
                                      + ("-" if right else "+") + str(kk),
                                      "cartan": e["cartan"]})
                        nxt.append(len(qreps) - 1)
                    qedges.append({"from": qreps[ri]["label"], "vertex": str(k),
                                   "dir": "-" if right else "+", "E": Ev,
                                   "to": tag, "dim": e["dim"]})
        qfront = nxt
        print("H depth %d · 신규 %d · 대표 %d · %.1fs"
              % (dep, len(nxt), len(qreps), time.time() - t0), flush=True)
        if not nxt:
            break
    R["H_closed_before_cap"] = qsat and not qfront
    R["H_all_edges_tilting"] = (len(qedges) == 6 * len(qreps))
    # ★★예측: 류가 **정확히 2개**(dim 24 = SL(2,3) · dim 36 = SL(2,5))에서 닫힌다
    R["H_two_representatives"] = (len(qreps) == 2
                                  and sorted(r["alg"]["n"] for r in qreps)
                                  == [24, 36])
    qtbl = {}
    for r in qreps:
        a = r["alg"]
        h = GE.hh_struct(a, cup=True)       # ★비트평면 rank 로 dim 36 도 규모 안
        qtbl[r["label"]] = {
            "path": r["path"] or "(start)", "dim": a["n"],
            "cartan": r["cartan"], "n_arrows": sum(GE.quiver_of(a).values()),
            "rad_powers": GE.rad_powers(a), "loewy_length":
                len(GE.rad_powers(a)), "cochain_dims": h["C"],
            "HH0": h["HH0"], "HH1": h["HH1"], "HH2": h["HH2"],
            "cup_rank": h["cup_rank"],
            "cup_is_cocycle": h["cup_is_cocycle"],
            "graded_commutative": h["graded_commutative"],
            "cartan_det": det_int(r["cartan"]), "cartan_snf":
                smith(r["cartan"])}
    # ★★유도불변량 — 류의 **모든 대표**가 같아야 한다(반증 가능한 게이트)
    R["H_HH_constant_on_class"] = all(
        (v["HH0"], v["HH1"], v["HH2"], v["cup_rank"]) == (7, 5, 5, 2)
        for v in qtbl.values())
    R["H_cup_correctness"] = all(v["cup_is_cocycle"] and v["graded_commutative"]
                                 for v in qtbl.values())
    R["H_det_snf_constant"] = all(v["cartan_det"] == 32
                                  and v["cartan_snf"] == [2, 2, 8]
                                  for v in qtbl.values())
    R["H_members_identified"] = (
        any(v["dim"] == 24 and v["cartan"] == cart for v in qtbl.values())
        and any(v["dim"] == 36 and canon(v["cartan"]) == canon(c5)
                for v in qtbl.values()))
    out["H_q8_class_closure"] = {
        "representatives": qtbl, "mutation_edges": qedges,
        "closed": R["H_closed_before_cap"],
        "identified": {"24": "SL(2,3) p=2 주블록(= 군대수 자체)",
                       "36": "SL(2,5) p=2 주블록(G축 명시 동형)"},
        "conclusion": ("★★★결손군 `Q₈` 의 유도동등류가 **대표 2개**에서 닫힌다 — "
                       "`SL(2,3)`(dim 24) ↔ `SL(2,5)`(dim 36). 두 대표 모두 "
                       "`(HH⁰,HH¹) = (7,5)`·det 32·SNF [2,2,8]"),
        "honest": ("폐합은 `dim ≤ 80` · 깊이 ≤ 6 **안에서의** 폐합이다. "
                   "외부 분류표(quaternion type 등) 대응은 무주장"),
        "note": ("★`rank_packed`(GF(2^k) 비트평면) 덕에 dim 36 의 `C³ = 20648` 도 "
                 "규모 안으로 들어왔다 — 이전 사이클의 유보가 해소됐다"),
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
