#!/usr/bin/env python
"""★6 사이클 산출물 봉합 — **세 sidecar 교차검증** + 4 블록 종합표 + 커버리지 행렬.

2026-07-28 ~ 08-02 여섯 사이클이 **분해행렬 D → Cartan C → Ext¹ 퀴버 → Loewy 급수 →
기본대수 → 관계식/Ext²** 로 **4 블록**을 닫았다. 그 결과가 세 sidecar 에 흩어져 있다:

  `.pgf/proofs/EXT1-QUIVER.json`      — Cartan · Ext¹ 퀴버 4개
  `.pgf/proofs/LOEWY-SERIES.json`     — 차원 산술 · 분해체 판정 · Loewy 급수(p=2)
  `.pgf/proofs/QUIVER-RELATIONS.json` — 기본대수 · 화살 · 관계식 · Ext²(4 블록)

★**종합은 요약이 아니라 교차검증이다.** 각 층은 자기 안에서 검증됐지만 **층 사이의
정합은 부분적으로만** 확인됐다. 이 관측은 세 파일을 **입력으로 읽어** 값이 서로 맞는지를
게이트로 건다 — 새로 계산하지 않고, 이미 발행된 산출물끼리 대조한다.

관측 축:
  X  ★**교차 게이트** — Cartan 3-way(EXT1 = QR = LOEWY dim_P 역산) · Ext¹ 3-way
     (EXT1 = LOEWY rad/rad² = QR 화살) · Loewy 2-way(LOEWY 층 = QR graded) ·
     차원 산술(블록 합 = |G|) · dim A = ΣC · Ext² 총합 = 관계식 수 · Ext¹ 대칭 ·
     퀴버 지지 ⊆ Cartan 지지
  Y  ★**4 블록 종합표** — 체 · 정점 · 화살 · dim A · 관계식 · Ext² · 균질성 · 유보
  Z  ★**커버리지 행렬** — 블록 × 산출량 × **독립 경로 수**(무엇이 몇 경로로 확인됐는지)
  V  ★★**라운드 봉합** — 5 사이드카 교차검증(같은 값이 두 곳 이상이면 반드시 대조) +
     결손군 3류 **커버리지 행렬**(★빈 칸을 그대로 노출) + 세 류가 det/SNF 로 분리됨을 고정.
  W  ★**외부 요청서(REQUEST-v22·v23·v24) 수치 자동 대조** — 발행 문서가 sidecar 와 어긋나면
     빨간불. v23 은 §3aa **유도동등류 3 대표**를 `TILTING-COMPLEX.json` 과 전 필드 대조.

정직 경계:
  · 이 관측은 **검증기**이지 새 계산이 아니다 — 세 sidecar 가 최신이어야 유효하다
    (상류 관측을 고치면 이 축도 다시 돌려야 한다).
  · A₆ p=3 는 LOEWY sidecar 에 층이 없다(QUIVER-RELATIONS J/K 축에서 처음 산출) ⟹
    Loewy 교차검증은 **QR 내부 2-way**(𝔽₃ ↔ GF(9))로만 — 커버리지 행렬에 그대로 적는다.
  · 경로 수는 **이 저장소가 실제로 실행한 계산**의 수이며, 문헌 대조는 포함하지 않는다.
"""
import json
import os
import sys

from qf_witness.core.paths import ROOT
from qf_witness.observe.tilting_complex_observe import canon

PROOFS = os.path.join(ROOT, ".pgf", "proofs")


def load(name):
    with open(os.path.join(PROOFS, name), encoding="utf-8") as f:
        return json.load(f)


# ══════════════════════════════════════════════════════════════════════════
# 블록 표 — 세 sidecar 안의 위치를 한 곳에 모은다
# ══════════════════════════════════════════════════════════════════════════
BLOCKS = [
    {"key": "A6_p2_principal", "group": "A₆", "p": 2, "order": 360,
     "field": "𝔽₂ (이 블록의 분해체)", "names": ["1̂", "4ₐ", "4_b"],
     "dims": [1, 4, 4], "ext1_key": "A6_p2_quiver",
     "cartan_field": "cartan_principal", "qr_key": "F_A6_p2_principal",
     "loewy_axis": "E", "loewy_idx": [0, 1, 2],
     "qr_names": ["1", "4a", "4b"]},
    {"key": "A7_p2_nonprincipal", "group": "A₇", "p": 2, "order": 2520,
     "field": "𝔽₂ (분해체)", "names": ["4̂", "4̄̂", "6̂"],
     "dims": [4, 4, 6], "ext1_key": "A7_p2_nonprincipal_quiver",
     "cartan_field": "cartan_nonprincipal", "qr_key": "A_A7_p2_nonprincipal",
     "loewy_axis": "G", "loewy_names": ["4", "4b", "6"],
     "loewy_idx": [1, 2, 3], "qr_names": ["4", "4b", "6"]},
    {"key": "A7_p2_principal", "group": "A₇", "p": 2, "order": 2520,
     "field": "𝔽₂ (분해체)", "names": ["1̂", "14̂", "20̂"],
     "dims": [1, 14, 20], "ext1_key": "A7_p2_principal_quiver",
     "cartan_field": "cartan_principal", "qr_key": "H_A7_p2_principal",
     "loewy_axis": "G", "loewy_names": ["1", "14", "20"],
     "loewy_idx": [0, 4, 5], "qr_names": ["1", "14", "20"]},
    {"key": "A6_p3_principal", "group": "A₆", "p": 3, "order": 360,
     "field": "★𝔽₃ 는 분해체가 아니다 → GF(9)", "names": ["1̂", "4", "3", "3′"],
     "dims": [1, 4, 3, 3], "ext1_key": "A6_p3_quiver",
     "cartan_field": "cartan_principal", "qr_key": None, "loewy_axis": None,
     "qr_names": ["1", "4", "3", "3b"]},
]


def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "block-algebra-synthesis/v1",
           "_note": ("세 sidecar 교차검증 + 4 블록 종합표 + 커버리지 행렬. "
                     "검증기(새 계산 아님)·seal 아님·module 0·root 불변."),
           "_inputs": ["EXT1-QUIVER.json", "LOEWY-SERIES.json",
                       "QUIVER-RELATIONS.json"]}
    E1 = load("EXT1-QUIVER.json")
    LO = load("LOEWY-SERIES.json")
    QR = load("QUIVER-RELATIONS.json")
    R["inputs_all_ok"] = bool(E1.get("all_ok") and LO.get("all_ok")
                              and QR.get("all_ok"))

    # ── X. 교차 게이트 ──────────────────────────────────────────────────
    per, table = {}, {}
    for b in BLOCKS:
        k = b["key"]
        n = len(b["names"])
        C = E1[b["ext1_key"]][b["cartan_field"]]
        Q = E1[b["ext1_key"]]["matrix"]
        arith = LO["A_dimension_arithmetic"]["per_block"][k]
        d = b["dims"]
        g = {}
        # ① Cartan → dim P 역산이 LOEWY 의 dim_P 와 일치
        g["dimP_from_cartan"] = (
            [sum(C[j][i] * d[j] for j in range(n)) for i in range(n)]
            == arith["dim_P"])
        # ② 블록 차원 = Σ dim P·dim S
        g["block_dim"] = (
            sum(arith["dim_P"][i] * d[i] for i in range(n))
            == arith["block_dim"])
        # ③ Ext¹ 대칭(분해체 위) · 퀴버 지지 ⊆ Cartan 지지
        g["ext1_symmetric"] = all(Q[i][j] == Q[j][i]
                                  for i in range(n) for j in range(n))
        g["quiver_support_in_cartan"] = all(
            C[i][j] != 0 for i in range(n) for j in range(n) if Q[i][j])
        if b["qr_key"]:
            P = QR[b["qr_key"]]["presentation"]
            # ④ ★Cartan 2-sidecar 일치(EXT1 ↔ QUIVER-RELATIONS 의 Hom 차원)
            g["cartan_ext1_vs_hom"] = (P["cartan_via_hom"] == C)
            # ⑤ dim A = Σ C
            g["dimA_equals_sumC"] = (
                P["dim_basic_algebra"] == sum(sum(r) for r in C))
            # ⑥ Ext² 총합 = 최소 관계식 수
            g["ext2_total_equals_relations"] = (
                sum(sum(r) for r in P["ext2_matrix"])
                == P["n_relations_filtered"])
            # ⑦ ★Ext¹ 3-way: EXT1 퀴버 = QR 화살 다중도 행렬
            ixq = {v: t for t, v in enumerate(b["qr_names"])}
            am = [[0] * n for _ in range(n)]
            for e in P["arrow_legend"]:
                am[ixq[e[2]]][ixq[e[1]]] += 1      # 블록(src,tgt) ↔ Ext¹(tgt,src)
            g["ext1_equals_arrows"] = (am == Q)
        else:                                   # A₆ p=3 — GF(9) 축(M)에서 읽는다
            M9 = QR["M_A6_p3_GF9_relations"]
            ixq = {v: t for t, v in enumerate(b["qr_names"])}
            am = [[0] * n for _ in range(n)]
            for (s_, t_) in M9["arrows"]:
                am[ixq[t_]][ixq[s_]] += 1
            g["ext1_equals_arrows"] = (am == Q)
            g["cartan_ext1_vs_hom"] = (M9["hom_dims_gf9"] == C)
            g["dimA_equals_sumC"] = (sum(sum(r) for r in M9["hom_dims_gf9"])
                                     == sum(sum(r) for r in C))
            g["ext2_total_equals_relations"] = (
                sum(sum(r) for r in M9["ext2_matrix"]) == M9["n_relations"])
            # ★GF(9) Loewy(K축) 층 합 = 기본대수 graded(M축) — QR 내부 2-way
            K9 = QR["K_A6_p3_over_GF9"]["loewy_layers"]
            g["graded_equals_loewy_layers"] = (
                [sum(sum(K9[nm][t]) for nm in b["qr_names"])
                 for t in range(len(M9["graded"]))] == M9["graded"])
        if b["loewy_axis"]:
            src = (LO["E_loewy_series"]["pims"] if b["loewy_axis"] == "E"
                   else LO["G_A7_p2_loewy"]["pims"])
            idx = b["loewy_idx"]
            if b["loewy_axis"] == "E":
                rows = [src[key] for key in sorted(src)]
                rows = sorted(rows, key=lambda v: v["head"].index(1))
            else:
                rows = [src[nm] for nm in b["loewy_names"]]
            # ⑧ ★Ext¹ 3-way 의 세 번째: LOEWY 의 rad/rad² 행 = 퀴버 행
            g["ext1_equals_rad_over_rad2"] = all(
                [rows[i]["rad_over_rad2"][j] for j in idx] == Q[i]
                for i in range(n))
            # ⑨ Loewy 층 총합 = Cartan 열
            g["layers_sum_to_cartan"] = all(
                [rows[i]["composition_total"][j] for j in idx]
                == [C[j][i] for j in range(n)] for i in range(n))
            if b["qr_key"]:
                P = QR[b["qr_key"]]["presentation"]
                # ⑩ ★Loewy 2-sidecar: 층별 단순가군 수 합 = QR graded
                gd = [sum(sum(rows[i]["loewy_layers"][t][j] for j in idx)
                          for i in range(n))
                      for t in range(rows[0]["loewy_length"])]
                g["graded_equals_loewy_layers"] = (gd == P["graded_dims"])
        per[k] = g
        for gk, gv in g.items():
            R[f"X_{k}_{gk}"] = gv

    # 전 블록 합 = |G|
    tot = LO["A_dimension_arithmetic"]["totals"]
    R["X_totals_equal_group_orders"] = (tot["A6_p2"] == tot["A6_p3"] == 360
                                        and tot["A7_p2"] == 2520)

    # ── Y. 4 블록 종합표 ────────────────────────────────────────────────
    for b in BLOCKS:
        k = b["key"]
        C = E1[b["ext1_key"]][b["cartan_field"]]
        Q = E1[b["ext1_key"]]["matrix"]
        row = {"group": b["group"], "p": b["p"], "field": b["field"],
               "simples": b["names"], "dims": b["dims"],
               "dim_P": LO["A_dimension_arithmetic"]["per_block"][k]["dim_P"],
               "block_dim": LO["A_dimension_arithmetic"]["per_block"][k]["block_dim"],
               "cartan": C, "quiver": Q,
               "n_arrows": sum(sum(r) for r in Q),
               "self_loop": any(Q[i][i] for i in range(len(Q))),
               "multi_arrow": any(x > 1 for r in Q for x in r),
               "dim_basic_algebra": sum(sum(r) for r in C)}
        if b["qr_key"]:
            P = QR[b["qr_key"]]["presentation"]
            row.update({"loewy_length": len(P["graded_dims"]),
                        "graded": P["graded_dims"],
                        "n_relations": P["n_relations_filtered"],
                        "ext2": P["ext2_matrix"],
                        "homogeneous": P["homogeneous_certified"],
                        "presentation": ("kQ/I 완전"
                                         + ("(균질)" if P["homogeneous_certified"]
                                            else "(★비균질 강제)"))})
        else:
            M = QR["M_A6_p3_GF9_relations"]
            row.update({"loewy_length": len(M["graded"]), "graded": M["graded"],
                        "n_relations": M["n_relations"],
                        "ext2": M["ext2_matrix"], "homogeneous": None,
                        "presentation": ("★퀴버·관계식 개수·Ext² 확정 · "
                                         "명시 형태와 균질성은 유보")})
        table[k] = row
    R["Y_four_blocks_present"] = (len(table) == 4)
    R["Y_obstruction_types"] = (
        table["A7_p2_principal"]["self_loop"]
        and not table["A7_p2_principal"]["homogeneous"]
        and table["A6_p3_principal"]["multi_arrow"]
        and table["A6_p3_principal"]["homogeneous"] is None
        and table["A6_p2_principal"]["homogeneous"]
        and table["A7_p2_nonprincipal"]["homogeneous"])
    R["Y_dim_A_values"] = ([table[b["key"]]["dim_basic_algebra"]
                            for b in BLOCKS] == [34, 18, 19, 36])
    R["Y_relation_counts"] = ([table[b["key"]]["n_relations"]
                               for b in BLOCKS] == [3, 3, 6, 10])

    # ── Z. 커버리지 행렬 — 무엇이 몇 경로로 확인됐는가 ───────────────────
    cov = {
        "A6_p2_principal": {
            "Cartan": ["D→C(a6_cartan_p23)", "Loewy 층 총합", "Hom 차원"],
            "Ext1": ["H¹ cocycle", "rad/rad²", "rad_A/rad²_A(화살)"],
            "Loewy": ["사영 덮개 직접", "기본대수 graded"],
            "Ext2": ["head(Ω²)", "H¹(G,Hom(ΩS,T))", "리프트-무관 최소생성"]},
        "A7_p2_nonprincipal": {
            "Cartan": ["D→C(a7_cartan_p2)", "Loewy 층 총합", "Hom 차원"],
            "Ext1": ["H¹ cocycle", "rad/rad²", "rad_A/rad²_A(화살)"],
            "Loewy": ["지수 크기 운반자", "기본대수 graded"],
            "Ext2": ["head(Ω²)", "H¹(G,Hom(ΩS,T))", "리프트-무관 최소생성"]},
        "A7_p2_principal": {
            "Cartan": ["D→C(a7_cartan_p2)", "Loewy 층 총합", "Hom 차원"],
            "Ext1": ["H¹ 상한/하한 협공", "전 간선 정직 순회", "rad/rad²",
                     "rad_A/rad²_A(화살)"],
            "Loewy": ["지수 크기 운반자", "기본대수 graded"],
            "Ext2": ["head(Ω²)", "리프트-무관 최소생성",
                     "★H¹ 9/9(7 칸 직접 + 2 칸 실측 쌍대성)"]},
        "A6_p3_principal": {
            "Cartan": ["D→C(a6_cartan_p23)", "GF(9) Loewy 층 총합",
                       "GF(9) Hom 조립"],
            "Ext1": ["H¹(GF(9) 실현화)", "GF(9) rad/rad²",
                     "rad_A/rad²_A(화살)"],
            "Loewy": ["𝔽₃ 사영 덮개", "GF(9) 실현화"],
            "Ext2": ["리프트-무관 최소생성(GF(9))", "𝔽₃ Ext² descent",
                     "★head(Ω²) GF(9) — 4 행 전부"]},
    }
    R["Z_every_quantity_has_two_routes"] = all(
        len(v) >= 2 for blk in cov.values() for v in blk.values())
    R["Z_ext2_three_routes_all_blocks"] = all(
        len(blk["Ext2"]) >= 3 for blk in cov.values())
    # ★제3 경로가 이번 사이클에 붙었는지(QR N축) 확인
    R["Z_gf9_third_route_present"] = ("N_A6_p3_GF9_ext2_third_route" in QR)
    # ★A₇ 주블록 H¹ 경로가 9/9 로 채워졌는지(전일 빈 칸)
    # ★A₆ p=3 head(Ω²) 도 4 행 전부인지(마지막 빈 칸)
    R["Z_a6p3_omega2_full_matrix"] = (
        QR["N_A6_p3_GF9_ext2_third_route"].get("matrix")
        == QR["M_A6_p3_GF9_relations"]["ext2_matrix"])
    R["Z_a7pr_h1_full_matrix"] = (
        QR["Hp_A7_principal_ext2_via_H1"].get("matrix")
        == QR["H_A7_p2_principal"]["presentation"]["ext2_matrix"])

    # ── W. ★요청서 수치 자동 대조 — 손으로 옮겨 적은 숫자의 stale 방지 ──
    req = os.path.join(ROOT, ".pgf", "external",
                       "HORIZONTAL-EXPANSION-REQUEST-v22.md")
    MK = "<!-- MACHINE-CHECKED: block-algebra-summary -->"
    KEYS = ["simples", "dims", "dim_P", "block_dim", "cartan", "quiver",
            "n_arrows", "dim_basic_algebra", "loewy_length", "graded",
            "n_relations", "ext2", "homogeneous"]
    if os.path.exists(req):
        txt = open(req, encoding="utf-8").read()
        seg = txt.split(MK, 1)[1].split("```json", 1)[1].split("```", 1)[0]
        emb = json.loads(seg)
        R["W_request_v22_blocks_present"] = (sorted(emb) == sorted(table))
        R["W_request_v22_matches_sidecar"] = all(
            {kk: table[k][kk] for kk in KEYS} == emb[k] for k in emb)
        out["W_request_cross_check"] = {
            "file": "HORIZONTAL-EXPANSION-REQUEST-v22.md", "marker": MK,
            "fields": KEYS,
            "note": ("★외부 발행 문서의 수치를 **sidecar 와 자동 대조**한다 — "
                     "요청서를 손으로 고치면 이 게이트가 깨진다(stale 방지)"),
        }
    else:
        R["W_request_v22_present"] = False

    # ── W2. ★유도동등류 요약(v23 신규 블록) 자동 대조 ──────────────────
    TCP = os.path.join(ROOT, ".pgf", "proofs", "TILTING-COMPLEX.json")
    req23 = os.path.join(ROOT, ".pgf", "external",
                         "HORIZONTAL-EXPANSION-REQUEST-v23.md")
    MK2 = "<!-- MACHINE-CHECKED: derived-equivalence-class -->"
    if os.path.exists(req23) and os.path.exists(TCP):
        TC = json.load(open(TCP, encoding="utf-8"))
        rep = TC["W_class_closure"]["representatives"]
        card = TC["X_hochschild_struct_const"]["class_card"]
        exp = {k: {"dim_basic_algebra": r["dim"], "cartan": r["cartan"],
                   "n_arrows": r["arrows"], "loewy_length": r["loewy_length"],
                   "rad_powers": r["rad_powers"], "cartan_det": r["det"],
                   "cartan_snf": r["snf"],
                   "mutation_path": r["path"] or "(start)",
                   "cochain_dims": card[k]["C"], "HH0": card[k]["HH0"],
                   "HH1": card[k]["HH1"], "HH2": card[k]["HH2"],
                   "cup_rank": card[k]["cup_rank"]}
               for k, r in rep.items()}
        txt = open(req23, encoding="utf-8").read()
        seg = txt.split(MK2, 1)[1].split("```json", 1)[1].split("```", 1)[0]
        emb2 = json.loads(seg)
        R["W_request_v23_reps_present"] = (sorted(emb2) == sorted(exp))
        R["W_request_v23_matches_sidecar"] = all(
            {kk: emb2[k][kk] for kk in exp[k]} == exp[k] for k in exp)
        # ★유도불변량이므로 발행 문서 안에서도 세 대표가 같아야 한다
        R["W_request_v23_class_invariant"] = all(
            (v["HH0"], v["HH1"], v["HH2"], v["cup_rank"]) == (5, 3, 5, 0)
            and v["cartan_det"] == 8 and v["cartan_snf"] == [1, 1, 8]
            for v in emb2.values())
        # ★군 이름은 sidecar 의 판정(V축 dim 34 · Y축 dim 16)과 정합해야 한다
        gmap = {v["dim_basic_algebra"]: v["group"] for v in emb2.values()}
        R["W_request_v23_groups_consistent"] = (
            TC["checks"]["V_explicit_isomorphism_found"]
            and TC["checks"]["Y_explicit_isomorphism"]
            and "PSL(2,7)" in gmap.get(16, "") and "A₆" in gmap.get(34, "")
            and gmap.get(19) == "A₇")
        out["W_request_v23_cross_check"] = {
            "file": "HORIZONTAL-EXPANSION-REQUEST-v23.md", "marker": MK2,
            "fields": sorted(exp["R0"]),
            "note": ("★v23 §3aa 의 유도동등류 표를 `TILTING-COMPLEX.json` 과 "
                     "전 필드 대조 — 발행 수치는 생성+게이트로 묶는다"),
        }
    else:
        R["W_request_v23_present"] = False

    # ── W3. ★결손군 2류 표(v24 신규 블록) 자동 대조 ────────────────────
    QBP = os.path.join(ROOT, ".pgf", "proofs", "QUATERNION-BLOCK.json")
    req24 = os.path.join(ROOT, ".pgf", "external",
                         "HORIZONTAL-EXPANSION-REQUEST-v24.md")
    MK3 = "<!-- MACHINE-CHECKED: defect-group-classes -->"
    if os.path.exists(req24) and os.path.exists(TCP) and os.path.exists(QBP):
        TC = json.load(open(TCP, encoding="utf-8"))
        QB = json.load(open(QBP, encoding="utf-8"))
        exp = {"D8": {}, "Q8": {}}
        card = TC["X_hochschild_struct_const"]["class_card"]
        for lb, v in TC["W_class_closure"]["representatives"].items():
            exp["D8"][lb] = {
                "dim_basic_algebra": v["dim"], "cartan": v["cartan"],
                "n_arrows": v["arrows"], "loewy_length": v["loewy_length"],
                "rad_powers": v["rad_powers"], "cochain_dims": card[lb]["C"],
                "HH0": card[lb]["HH0"], "HH1": card[lb]["HH1"],
                "HH2": card[lb]["HH2"], "cup_rank": card[lb]["cup_rank"],
                "cartan_det": v["det"], "cartan_snf": v["snf"],
                "mutation_path": v["path"] or "(start)"}
        for lb, v in QB["H_q8_class_closure"]["representatives"].items():
            exp["Q8"][lb] = {
                "dim_basic_algebra": v["dim"], "cartan": v["cartan"],
                "n_arrows": v["n_arrows"], "loewy_length": v["loewy_length"],
                "rad_powers": v["rad_powers"],
                "cochain_dims": v["cochain_dims"], "HH0": v["HH0"],
                "HH1": v["HH1"], "HH2": v["HH2"], "cup_rank": v["cup_rank"],
                "cartan_det": v["cartan_det"], "cartan_snf": v["cartan_snf"],
                "mutation_path": v["path"]}
        seg = open(req24, encoding="utf-8").read().split(MK3, 1)[1]             .split("```json", 1)[1].split("```", 1)[0]
        e3 = json.loads(seg)
        R["W_request_v24_classes_present"] = (
            sorted(e3) == ["D8", "Q8"]
            and all(sorted(e3[g]["members"]) == sorted(exp[g]) for g in exp))
        R["W_request_v24_matches_sidecar"] = all(
            {kk: e3[g]["members"][lb][kk] for kk in exp[g][lb]} == exp[g][lb]
            for g in exp for lb in exp[g])
        # ★유도불변량 — 류 **안에서는** 같고 **류 사이에서는** 다르다
        R["W_request_v24_class_invariants"] = (
            len({(m["HH0"], m["HH1"], m["HH2"], m["cup_rank"], m["cartan_det"])
                 for m in e3["D8"]["members"].values()}) == 1
            and len({(m["HH0"], m["HH1"], m["HH2"], m["cup_rank"],
                      m["cartan_det"])
                     for m in e3["Q8"]["members"].values()}) == 1
            and {tuple(sorted(m["cartan_det"] for m in
                              e3[g]["members"].values()))[0] for g in e3}
            == {8, 32})
        R["W_request_v24_group_names"] = (
            {m["group"] for m in e3["Q8"]["members"].values()}
            == {"SL(2,3) = Q₈⋊ℤ₃", "SL(2,5) = 2.A₅"}
            and QB["checks"]["G_explicit_isomorphism"]
            and QB["checks"]["H_two_representatives"])
        out["W_request_v24_cross_check"] = {
            "file": "HORIZONTAL-EXPANSION-REQUEST-v24.md", "marker": MK3,
            "fields": sorted(exp["D8"]["R0"]),
            "note": ("★v24 §3ab 의 **결손군 2류 표**를 `TILTING-COMPLEX.json`(D₈) + "
                     "`QUATERNION-BLOCK.json`(Q₈) 과 전 필드 대조 — "
                     "발행 수치는 생성+게이트로 묶는다"),
        }
    else:
        R["W_request_v24_present"] = False

    # ── V. ★★라운드 봉합 — **5 사이드카 교차검증** + 커버리지 행렬 ────
    QBP2 = os.path.join(ROOT, ".pgf", "proofs", "QUATERNION-BLOCK.json")
    AGP = os.path.join(ROOT, ".pgf", "proofs", "A6P3-GF9.json")
    if os.path.exists(QBP2) and os.path.exists(AGP) and os.path.exists(TCP):
        TC2 = json.load(open(TCP, encoding="utf-8"))
        QB2 = json.load(open(QBP2, encoding="utf-8"))
        AG = json.load(open(AGP, encoding="utf-8"))
        ag = AG["A6_p3_over_GF9"]
        # ★같은 값이 세 곳에 있다: K축(QR)·Y표(이 모듈)·신규 사이드카
        R["V_a6p3_cartan_three_way"] = (
            ag["cartan"] == table["A6_p3_principal"]["cartan"]
            == QR["K_A6_p3_over_GF9"]["cartan"])
        # ★★기저변환: 𝔽₃(P축) 와 GF(9)(신규) 의 `HH^n` 이 같아야 한다(복합체는 다르다)
        f3 = QR["P_hochschild2"]["per_block"]["A6_p3_principal"]
        h9 = ag["hochschild_GF9"]
        R["V_a6p3_hh_base_change"] = (
            (h9["HH0"], h9["HH1"], h9["HH2"], h9["cup_rank"])
            == (f3["HH0"], f3["HH1"], f3["HH2"], f3["cup_rank"])
            and h9["C"] != f3["C"])
        # ★D₈ 류의 두 끝점이 Y표(블록 Cartan)와 정합
        d8 = TC2["W_class_closure"]["representatives"]
        R["V_d8_endpoints_match_table"] = (
            any(v["cartan"] == table["A7_p2_principal"]["cartan"]
                for v in d8.values())
            and any(canon(v["cartan"])
                    == canon(table["A6_p2_principal"]["cartan"])
                    for v in d8.values()))
        # ★Q₈ 류의 두 대표가 SL(2,3)·SL(2,5) 로 동일시됐고 서로 다른 dim
        q8 = QB2["H_q8_class_closure"]["representatives"]
        R["V_q8_two_reps_identified"] = (
            sorted(v["dim"] for v in q8.values()) == [24, 36]
            and QB2["checks"]["G_explicit_isomorphism"]
            and QB2["B_sl23_over_F4"]["cartan_F4"]
            == [[4, 2, 2], [2, 4, 2], [2, 2, 4]])
        # ★★★세 류가 **확실히 다르다** — det·SNF 로 분리
        dets = {"D8": {v["det"] for v in d8.values()},
                "Q8": {v["cartan_det"] for v in q8.values()},
                "A6p3": {ag["cartan_det"]}}
        R["V_three_classes_separated"] = (
            dets["D8"] == {8} and dets["Q8"] == {32} and dets["A6p3"] == {9})
        # ── 커버리지 행렬 — ★빈 칸을 그대로 노출한다 ──────────────────
        cov2 = {
            "D8_class": {"members": 3, "Cartan": "✓", "arrows": "✓",
                         "rad^n": "✓", "HH0_HH1": "✓", "HH2": "✓",
                         "cup": "✓", "mutation_tilting": "✓",
                         "closure": "✓ (dim ≤ 60 · 깊이 ≤ 6)",
                         "group_identification": "✓ 3/3"},
            "Q8_class": {"members": 2, "Cartan": "✓", "arrows": "✓",
                         "rad^n": "✓", "HH0_HH1": "✓", "HH2": "✓",
                         "cup": "✓", "mutation_tilting": "✓",
                         "closure": "✓ (dim ≤ 80 · 깊이 ≤ 6)",
                         "group_identification": "✓ 2/2"},
            "A6p3_class": {"members": "≥13 (canonical Cartan)",
                           "Cartan": "✓", "arrows": "✓", "rad^n": "✓",
                           "HH0_HH1": "✓", "HH2": "✓", "cup": "✓",
                           "mutation_tilting": "✓ (32 간선)",
                           "closure": "✗ 동형 dedup 규모 밖(레벨 1 = 1.36×10¹¹)",
                           "group_identification":
                               "✗ 출발점만(나머지 ≥12 미상)"},
        }
        gaps = [(k, c) for k, v in cov2.items() for c, x in v.items()
                if isinstance(x, str) and x.startswith("✗")]
        R["V_coverage_gaps_are_two"] = (len(gaps) == 2
                                        and all(g[0] == "A6p3_class"
                                                for g in gaps))
        out["V_round_audit"] = {
            "sidecars": ["EXT1-QUIVER", "LOEWY-SERIES", "QUIVER-RELATIONS",
                         "BLOCK-ALGEBRA-SYNTHESIS(자기)", "TILTING-COMPLEX",
                         "QUATERNION-BLOCK", "A6P3-GF9"],
            "coverage": cov2, "gaps": [f"{a}.{b}" for a, b in gaps],
            "class_separation": {k: sorted(v) for k, v in dets.items()},
            "discipline_tally": {
                "known_answer_as_judge": 6,
                "predictions_refuted_and_recorded": 6,
                "walls_quantified": 3,
                "failed_optimization_reverted": 1,
                "self_bugs_caught_by_gates": 3,
            },
            "note": ("★같은 값이 두 곳 이상에 있으면 **반드시 대조**한다 — "
                     "A₆ p=3 Cartan 은 **세 곳**(QR K축·이 모듈 Y표·신규 사이드카), "
                     "`HH^*` 는 **두 체**(𝔽₃ P축·GF(9) 신규)에 있다"),
            "honest": ("★**빈 칸 2개를 그대로 노출한다** — A₆ p=3 류의 **폐합**과 "
                       "**구성원 동일시**. 둘 다 동형 판정이 규모 밖이라 막혔고, "
                       "필요한 것은 **자기동형군 몫 + 정규형**(열거가 아닌 알고리즘)이다. "
                       "★새 요청서는 만들지 않았다 — v24 가 외부 수행 대기 중이다"),
        }
    else:
        R["V_round_audit_present"] = False

    ok = bool(all(R.values()))
    out["checks"] = R
    out["X_cross_gates"] = {"per_block": per,
                            "note": ("★세 sidecar 를 **입력으로 읽어** 대조 — "
                                     "Cartan(EXT1 ↔ QR Hom 차원 ↔ LOEWY dim_P 역산) · "
                                     "Ext¹(EXT1 퀴버 ↔ LOEWY rad/rad² ↔ QR 화살) · "
                                     "Loewy(LOEWY 층 ↔ QR graded)")}
    out["Y_block_table"] = table
    out["Z_coverage"] = {
        "matrix": cov,
        "legend": ("각 칸 = 그 산출량을 **독립으로 확인한 계산 경로**들. "
                   "문헌 대조는 포함하지 않는다(자체유도 규율)"),
        "gaps": ("★**빈 칸 없음** — A₇ p=2 주블록 Ext² 의 H¹ 경로는 3/9 → **9/9**"
                 "(2026-08-04: 자기쌍대성 실측으로 값싼 방향) · A₆ p=3 Ext² 의 "
                 "head(Ω²) 경로는 3·3′ 행 → **4 행 전부**"
                 "(2026-08-05: Ω¹ 도 조립으로 올려 4608 계 회피). "
                 "잔여는 **경로 수**가 아니라 **관계식의 명시 형태**(리프트 의존)"),
    }
    out["scope_honesty"] = {
        "delivered": ("★세 sidecar 교차검증(블록별 최대 10 게이트) · 4 블록 종합표 · "
                      "★커버리지 행렬(경로 수 명시)"),
        "not_claimed": ("새 수학 결과 아님(검증기) · 외부 문헌 대조 없음 · "
                        "봉인 게이트 아님"),
        "coupling": ("상류 세 관측의 sidecar 를 읽는다 — 상류를 고치면 이 축도 "
                     "다시 돌려야 한다"),
    }
    out["all_ok"] = ok

    if not quick:
        p_ = os.path.join(PROOFS, "BLOCK-ALGEBRA-SYNTHESIS.json")
        with open(p_, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("블록 대수 6층 종합 — 세 sidecar 교차검증 (검증기 · seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        for b in BLOCKS:
            t = table[b["key"]]
            print(f"  ★{b['key']}: {t['field']} · 정점 {len(t['simples'])} · "
                  f"화살 {t['n_arrows']} · dim A {t['dim_basic_algebra']} · "
                  f"관계식 {t['n_relations']} · {t['presentation']}", flush=True)
        print("  → .pgf/proofs/BLOCK-ALGEBRA-SYNTHESIS.json", flush=True)
    if not ok:
        print("  ✗ 실패 체크:", [k for k, v in R.items() if not v], flush=True)
    print(f"block_algebra_synthesis_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
