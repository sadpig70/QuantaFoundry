#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""naimark_observe — TrackGate6 G3e: UD-POVM Naimark 완성 witness (신규 봉인 0).

봉인된 naimark_ud3(3q: sys q0 · outcome anc q1q2, Tier-0 8×8)에 대해:
  1. seal 링크 + golden 유니터리성.
  2. ★회로 독립 E_k 재구성: M_k = (I_s⊗⟨k|_anc)·U·(I_s⊗|00⟩_anc) → E_k = M_k†M_k 가
     IDP 정의(|ψ±⟩=Ry(±π/3)|0⟩, overlap ½: E±=⅔|ψ∓^⊥⟩⟨ψ∓^⊥| · E?=⅔|0⟩⟨0| · E₃=0)와 exact 일치.
  3. POVM 완비성 ΣE_k=I + 양성 E_k⪰0.
  4. ★UD 성질: 오식별 ⟨ψ∓|E±|ψ∓⟩=0 exact · 성공확률 ⟨ψ±|E±|ψ±⟩=1−|⟨ψ₊|ψ₋⟩|=½ (IDP 최적).
  5. 통계 일치: 임의 상태(seed=0)에서 dilation anc-marginal 확률 == Tr(E_kρ) exact.
  6. teeth 2종: ①틀린각(0.9·arccos⅓) 준비층 → E_k 불일치 검출.
     ②★W 간섭층 제거(잘림 회로) → E± off-diagonal 소실(대각 POVM 붕괴, UD 실패) 검출
       — sys which-path 코히런트 소거가 하중을 받는 층임을 실증.

정직 경계(INV-Q3, seal 아님, root 성장은 naimark_ud3 봉인분뿐):
  - 봉인 = 정방 유니터리 완성(Tier-0 exact)뿐. 정의 열(anc|00⟩ 입력 2열)만 Naimark isometry —
    여타 열=회로-유도 완성(peps/aklt honest split). POVM·측정통계=관측(비유니터리 개념).
  - rank-1 Kraus 자유도(G3a 판정)로 기존 팔레트(ry_cg_half+dyadic) 격자 실현 — 신규 module 0.
  - SIC/trine 등 비-골든각 POVM=봉인불가 정직경계. 유한샘플 측정=미구현(해석 확률만).

사용: python scripts/naimark_observe.py [--quick]
"""
import os, sys, re, json
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".pgf", "proofs", "NAIMARK-OBSERVE.json")


def load_golden(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    ns = {}
    exec(re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1), ns)
    return ns["golden"]


def ry(a):
    return np.array([[np.cos(a/2), -np.sin(a/2)], [np.sin(a/2), np.cos(a/2)]], dtype=complex)


def idp_targets():
    """IDP UD-POVM 정의 직접(회로 독립): |ψ±⟩=Ry(±π/3)|0⟩ → E 3종+null."""
    c, s = np.cos(np.pi / 6), np.sin(np.pi / 6)
    psi_p = np.array([c, s], dtype=complex)
    psi_m = np.array([c, -s], dtype=complex)
    perp_m = np.array([s, c], dtype=complex)      # ⊥ψ₋
    perp_p = np.array([s, -c], dtype=complex)     # ⊥ψ₊
    lam = 1 / (1 + abs(np.vdot(psi_p, psi_m)))    # 1/(1+s)=2/3
    E = {0: lam * np.outer(np.array([1, 0]), np.array([1, 0])),   # E? (inconclusive)
         1: lam * np.outer(perp_m, perp_m.conj()),                # E₊ (ψ₊ 검출)
         2: lam * np.outer(perp_p, perp_p.conj()),                # E₋ (ψ₋ 검출)
         3: np.zeros((2, 2), dtype=complex)}                      # null
    return psi_p, psi_m, E


def extract_E(U):
    """M_k[so,s] = U[(so,k),(s,00)] → E_k = M_k†M_k (anc 값 k = 측정 결과)."""
    Es = {}
    for k in range(4):
        M = np.zeros((2, 2), dtype=complex)
        for s in range(2):
            for so in range(2):
                M[so, s] = U[so * 4 + k, s * 4]
        Es[k] = M.conj().T @ M
    return Es


def observe():
    app_id = "naimark_ud3"
    sealed = os.path.join(ROOT, "registry", "apps", f"{app_id}.sealed.json")
    seal_ok = os.path.exists(sealed) and bool(json.load(open(sealed, encoding="utf-8")).get("u_hash"))
    U = load_golden(f"{app_id}.app.pg")
    unitary_ok = bool(np.allclose(U.conj().T @ U, np.eye(8), atol=1e-12))

    psi_p, psi_m, E_t = idp_targets()
    Es = extract_E(U)
    match = float(max(np.abs(Es[k] - E_t[k]).max() for k in range(4)))
    complete = float(np.abs(sum(Es.values()) - np.eye(2)).max())
    positive = bool(all(np.linalg.eigvalsh(Es[k]).min() > -1e-12 for k in range(4)))

    # UD 성질 (재구성 E 로 판정 — 회로가 실제 실현한 측정)
    err_p = float(np.real(psi_m.conj() @ Es[1] @ psi_m))     # ψ₋ 를 ψ₊ 로 오식별
    err_m = float(np.real(psi_p.conj() @ Es[2] @ psi_p))
    suc_p = float(np.real(psi_p.conj() @ Es[1] @ psi_p))
    suc_m = float(np.real(psi_m.conj() @ Es[2] @ psi_m))
    ud_ok = bool(max(abs(err_p), abs(err_m)) < 1e-12
                 and abs(suc_p - 0.5) < 1e-12 and abs(suc_m - 0.5) < 1e-12)

    # 통계 일치: dilation anc-marginal == Tr(E_k ρ) (seed=0 무작위 순수상태 3개)
    rng = np.random.default_rng(0)
    stat_dev = 0.0
    for _ in range(3):
        v = rng.standard_normal(2) + 1j * rng.standard_normal(2)
        v /= np.linalg.norm(v)
        full = U @ np.kron(v, np.array([1, 0, 0, 0], dtype=complex))
        for k in range(4):
            p_dil = float(sum(abs(full[so * 4 + k]) ** 2 for so in range(2)))
            p_povm = float(np.real(v.conj() @ Es[k] @ v))
            stat_dev = max(stat_dev, abs(p_dil - p_povm))
    stat_ok = bool(stat_dev < 1e-12)

    # teeth ①: 틀린각 준비층 — golden 재구성에서 cg → 0.9·cg 치환 재합성
    src = open(os.path.join(ROOT, "specs", "apps", f"{app_id}.app.pg"), encoding="utf-8").read()
    code = re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1)
    ns = {}
    exec(code.replace("np.arccos(1.0/3.0) / 2.0", "0.9 * np.arccos(1.0/3.0) / 2.0"), ns)
    E_bad = extract_E(ns["golden"])
    teeth_angle = bool(max(np.abs(E_bad[k] - E_t[k]).max() for k in range(4)) > 1e-3)
    # teeth ②: W 간섭층 제거(SEQ 마지막 8스텝 잘림) → E± off-diag 소실(UD 붕괴)
    ns2 = {}
    exec(code.replace("for G, tg in SEQ:", "for G, tg in SEQ[:-8]:"), ns2)
    E_cut = extract_E(ns2["golden"])
    offdiag_cut = float(max(abs(E_cut[k][0, 1]) for k in (1, 2)))
    err_cut = float(np.real(psi_m.conj() @ E_cut[1] @ psi_m))
    teeth_w = bool(offdiag_cut < 1e-12 and err_cut > 1e-3)   # 대각 붕괴 + 오식별 발생

    ok = bool(seal_ok and unitary_ok and match < 1e-12 and complete < 1e-12 and positive
              and ud_ok and stat_ok and teeth_angle and teeth_w)
    return {"app": app_id,
            "ensemble": {"states": "|ψ±⟩=Ry(±π/3)|0⟩ (overlap ½)", "seal_link": seal_ok,
                         "unitary": unitary_ok},
            "povm": {"E_reconstruction_vs_IDP": match, "completeness_dev": complete,
                     "positive": positive, "null_outcome_E3": "0 (anc |11⟩ 도달 불가)"},
            "ud": {"misidentify_p": err_p, "misidentify_m": err_m,
                   "success_p": suc_p, "success_m": suc_m,
                   "optimal_1_minus_overlap": 0.5, "ok": ud_ok},
            "statistics": {"dilation_marginal_vs_trace_dev": stat_dev, "ok": stat_ok},
            "teeth": {"wrong_angle_detects": teeth_angle,
                      "w_layer_cut_offdiag": offdiag_cut, "w_layer_cut_misidentify": err_cut,
                      "w_layer_loadbearing": teeth_w},
            "honest_boundary": "봉인=정방 유니터리 완성뿐(정의 열만 Naimark isometry). POVM·통계="
                               "관측(INV-Q3). rank-1 Kraus 자유도로 기존 팔레트 실현(신규 module 0). "
                               "SIC/trine 비-골든각=봉인불가. 유한샘플 측정=미구현(해석 확률).",
            "ok": ok}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"_schema": "naimark-observe-v1",
                       "_note": "UD-POVM Naimark 완성 witness: E_k 재구성==IDP 정의+UD 성질+통계+teeth. "
                                "봉인=유니터리뿐(INV-Q3).",
                       "observation": res}, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        p, u, t = res["povm"], res["ud"], res["teeth"]
        print("UD-POVM Naimark 완성 witness 관측 (naimark_ud3):", flush=True)
        print(f"  seal {res['ensemble']['seal_link']} · unitary {res['ensemble']['unitary']} · "
              f"E_k==IDP {p['E_reconstruction_vs_IDP']:.1e} · ΣE=I {p['completeness_dev']:.1e} · "
              f"E⪰0 {p['positive']}", flush=True)
        print(f"  UD: 오식별 {u['misidentify_p']:.1e}/{u['misidentify_m']:.1e} · "
              f"성공 {u['success_p']:.3f}/{u['success_m']:.3f} (최적 ½) · 통계 "
              f"{res['statistics']['dilation_marginal_vs_trace_dev']:.1e}", flush=True)
        print(f"  teeth: 틀린각 {t['wrong_angle_detects']} · W층 잘림→대각화 {t['w_layer_cut_offdiag']:.1e}"
              f"+오식별 {t['w_layer_cut_misidentify']:.3f} → 검출 {t['w_layer_loadbearing']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"naimark_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
