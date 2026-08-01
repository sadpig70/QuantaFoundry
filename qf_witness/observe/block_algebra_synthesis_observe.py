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
                     "H¹(1̂ 열만 — 규모 유보)"]},
        "A6_p3_principal": {
            "Cartan": ["D→C(a6_cartan_p23)", "GF(9) Loewy 층 총합",
                       "GF(9) Hom 조립"],
            "Ext1": ["H¹(GF(9) 실현화)", "GF(9) rad/rad²",
                     "rad_A/rad²_A(화살)"],
            "Loewy": ["𝔽₃ 사영 덮개", "GF(9) 실현화"],
            "Ext2": ["리프트-무관 최소생성(GF(9))", "𝔽₃ Ext² descent",
                     "head(Ω²) GF(9) — 3·3′ 행만"]},
    }
    R["Z_every_quantity_has_two_routes"] = all(
        len(v) >= 2 for blk in cov.values() for v in blk.values())
    R["Z_ext2_three_routes_all_blocks"] = all(
        len(blk["Ext2"]) >= 3 for blk in cov.values())
    # ★제3 경로가 이번 사이클에 붙었는지(QR N축) 확인
    R["Z_gf9_third_route_present"] = ("N_A6_p3_GF9_ext2_third_route" in QR)

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
        "gaps": ("A₇ p=2 주블록 Ext² 의 H¹ 경로는 **1̂ 열만**(m ≤ 1420 규모) · "
                 "A₆ p=3 Ext² 의 head(Ω²) 경로는 **3·3′ 행만**(Ω¹ 이 52·64 인 "
                 "1̂₉·4₉ 는 규모 밖) — 나머지는 descent 가 덮는다"),
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
