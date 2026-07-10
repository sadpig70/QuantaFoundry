#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mub_observe — TrackGate6 G2b: d=4 MUB-20 projective state 2-design witness (신규 봉인 0).

봉인된 mub4_b{1..5}_s{0..3} 20개 앱(5기저×4상태, plan=기봉인 x/h/s/cz Clifford word)에 대해:
  1. ★seal 링크: 20개 전부 registry/apps/<id>.sealed.json 존재 + u_hash 보유.
  2. 유니터리성: 각 golden U†U=I exact. 정의 열 |ψ_{b,s}⟩ = golden[:,0].
  3. ★회로 독립 검증(라벨 맵): Pauli 정의 직접 — P_{b,s}=(I+(−1)^{s0}A_b)(I+(−1)^{s1}B_b)/4 에서
       P|ψ⟩=|ψ⟩ exact 20/20. (A_b,B_b) = (ZI,IZ)·(XI,IX)·(YI,IY)·(XZ,ZY)·(YZ,ZX).
  4. ★상호비편향 전수: 동일기저 ⟨ψ|φ⟩=δ · 타기저 |⟨ψ|φ⟩|²=1/4 (400쌍).
  5. ★state 2-design witness: frame potential Σ|⟨ψ|φ⟩|⁴/N² = 2/(d(d+1)) = 1/10 exact +
       2차 모멘트 (1/20)Σ|ψ⟩⟨ψ|⊗|ψ⟩⟨ψ| == 2/(d(d+1))·Π_sym exact (등가 정의 이중 확인).
  6. ★소비 데모(state estimation): MUB 완비측정 단층재구성 ρ = Σ_b Σ_s p(s|b)·Π_{b,s} − I —
       순수(seed=0)·혼합(0.7|v⟩⟨v|+0.3·I/4) 상태 exact 복원(확률=해석값, 유한샘플 아님).
  7. teeth: 상태 1개 T-오염(FP·비편향 이탈) · 기저 1개 제거(재구성 붕괴) → 검출.

정직 경계(INV-Q3, seal 아님, root 성장은 20개 앱 봉인분뿐):
  - 봉인 = 개별 상태준비 유니터리 20개(Tier-0 exact)뿐. 정의 열만 MUB 물리(여타 열=회로-유도).
  - ★projective **state** 2-design 이며 unitary 2-design 아님 — G2a 반증(하한 226,
    .pgf/proofs/TWOQ-2DESIGN-BOUND.json)의 대체 payoff. 용어 정직.
  - 단층재구성 데모=해석 확률(유한샘플 shadow tomography 미구현 — 그 기반 자산만 확보).

사용: python -m qf_witness.observe.mub_observe [--quick]
"""
import os, sys, re, json
import numpy as np

from qf_witness.core.paths import ROOT
OUT = os.path.join(ROOT, ".pgf", "proofs", "MUB-OBSERVE.json")

I2 = np.eye(2, dtype=complex)
PAULI = {"I": I2,
         "X": np.array([[0, 1], [1, 0]], dtype=complex),
         "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
         "Z": np.diag([1, -1]).astype(complex)}
STAB = {1: ("ZI", "IZ"), 2: ("XI", "IX"), 3: ("YI", "IY"), 4: ("XZ", "ZY"), 5: ("YZ", "ZX")}


def pp(name):
    return np.kron(PAULI[name[0]], PAULI[name[1]])


def load_golden(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    ns = {}
    exec(re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1), ns)
    return ns["golden"]


def frame_potential(states):
    n = len(states)
    return float(sum(abs(np.vdot(u, v)) ** 4 for u in states for v in states) / n ** 2)


def reconstruct(rho, states):
    """MUB 완비측정 단층: ρ_rec = Σ p·Π − I (d+1=5 기저)."""
    rec = -np.eye(4, dtype=complex)
    for u in states:
        p = float(np.real(np.vdot(u, rho @ u)))
        rec += p * np.outer(u, u.conj())
    return rec


def observe_p5(states):
    """TrackHE4 P5 가산: shadow 측정측 — premeasurement V_b†·frame channel·재구성 witness."""
    links = True
    meas = {}
    for b in (2, 3, 4, 5):
        sealed = os.path.join(ROOT, "registry", "apps", f"mub4_meas_b{b}.sealed.json")
        links &= os.path.exists(sealed) and bool(json.load(open(sealed, encoding="utf-8")).get("u_hash"))
        meas[b] = load_golden(f"mub4_meas_b{b}.app.pg")

    # 측정측 완성: V_b†·V_b == I (기봉인 준비 s0 앱 golden == V_b) + V_b†·|state(b,s)⟩ == |s⟩ 16/16
    inv_ok = all(np.allclose(meas[b] @ load_golden(f"mub4_b{b}_s0.app.pg"), np.eye(4), atol=1e-12)
                 for b in (2, 3, 4, 5))
    pre_ok = True
    for b in (2, 3, 4, 5):
        for s in range(4):
            out = meas[b] @ states[(b - 1) * 4 + s]
            j = int(np.argmax(np.abs(out)))
            pre_ok &= bool(j == s and abs(abs(out[j]) - 1) < 1e-12
                           and abs(np.abs(out).sum() - 1) < 1e-11)

    # shadow exact core: frame channel M(ρ)=(ρ+I)/5 · 역재구성 5M−I==ρ · Bell·Pauli 회복 (유리 대수)
    rng = np.random.default_rng(0)
    A_ = rng.standard_normal((4, 4)) + 1j * rng.standard_normal((4, 4))
    rho_r = A_ @ A_.conj().T; rho_r /= np.trace(rho_r)
    bell = np.zeros(4, dtype=complex); bell[0] = bell[3] = 1 / np.sqrt(2)
    rho_b = np.outer(bell, bell.conj())
    frame_ok = inv_frame_ok = True
    for rho in (rho_r, rho_b):
        M = sum(np.real(np.vdot(u, rho @ u)) * np.outer(u, u.conj()) for u in states) / 5
        frame_ok &= bool(np.allclose(M, (rho + np.eye(4)) / 5, atol=1e-12))
        inv_frame_ok &= bool(np.allclose(5 * M - np.eye(4), rho, atol=1e-12))
    pauli_ok = True
    rec_b = 5 * sum(np.real(np.vdot(u, rho_b @ u)) * np.outer(u, u.conj()) for u in states) / 5 \
        - np.eye(4)
    for nm in ("XX", "YY", "ZZ", "XI", "IZ"):
        P = pp(nm)
        pauli_ok &= bool(abs(np.trace(P @ rec_b) - np.trace(P @ rho_b)) < 1e-12)

    # teeth: sdg→s 교란(수반 부호) → premeasurement 실패
    Sg = np.diag([1, 1j]).astype(complex)
    H1 = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    bad3 = np.kron(H1 @ Sg, I2) @ np.kron(I2, H1 @ Sg)   # sdg 대신 s
    out = bad3 @ states[8]                                # b3_s0
    teeth = bool(not (int(np.argmax(np.abs(out))) == 0 and abs(abs(out[0]) - 1) < 1e-6))

    ok = bool(links and inv_ok and pre_ok and frame_ok and inv_frame_ok and pauli_ok and teeth)
    return {"seal_links_4meas": links,
            "meas_inverts_sealed_prep_word": inv_ok,
            "premeasurement_16of16_states_to_labels": pre_ok,
            "shadow_exact_core": {"frame_channel_rho_plus_I_over5": frame_ok,
                                  "inverse_5M_minus_I": inv_frame_ok,
                                  "bell_pauli_recovery": pauli_ok,
                                  "note": "유리 계수 exact — 유한표본 통계는 범위 밖"},
            "teeth_sdg_sign": teeth,
            "honest_boundary": "봉인=premeasurement 유니터리 4뿐(b1=계산기저 자명). frame channel·"
                               "재구성=관측(INV-Q3). median-of-means·신뢰구간·유한표본=범위 밖.",
            "ok": ok}


def observe():
    ids = [f"mub4_b{b}_s{s}" for b in range(1, 6) for s in range(4)]
    # 1. seal 링크 + golden 로드
    seal_ok = True
    states, basis_of = [], []
    for i, app_id in enumerate(ids):
        sealed = os.path.join(ROOT, "registry", "apps", f"{app_id}.sealed.json")
        if not (os.path.exists(sealed) and json.load(open(sealed, encoding="utf-8")).get("u_hash")):
            seal_ok = False
        U = load_golden(f"{app_id}.app.pg")
        states.append(U[:, 0])
        basis_of.append(i // 4)

    # 2. 유니터리성
    unitary_ok = bool(all(
        np.allclose(load_golden(f"{a}.app.pg").conj().T @ load_golden(f"{a}.app.pg"),
                    np.eye(4), atol=1e-12) for a in ids))

    # 3. 회로 독립 라벨 맵: Pauli 프로젝터 고유상태 20/20
    label_ok = True
    for i, app_id in enumerate(ids):
        b, s = i // 4 + 1, i % 4
        s0, s1 = (s >> 1) & 1, s & 1
        A, B = pp(STAB[b][0]), pp(STAB[b][1])
        P = (np.eye(4) + (-1) ** s0 * A) @ (np.eye(4) + (-1) ** s1 * B) / 4
        if not np.allclose(P @ states[i], states[i], atol=1e-12):
            label_ok = False

    # 4. 상호비편향 전수 (400쌍)
    gram_ok = True
    for i in range(20):
        for j in range(20):
            ov = abs(np.vdot(states[i], states[j])) ** 2
            want = (1.0 if i == j else 0.0) if basis_of[i] == basis_of[j] else 0.25
            if abs(ov - want) > 1e-12:
                gram_ok = False

    # 5. state 2-design witness (이중: FP + 2차 모멘트)
    fp = frame_potential(states)
    fp_ok = bool(abs(fp - 0.1) < 1e-12)
    SW = np.zeros((16, 16), dtype=complex)
    for a in range(4):
        for c in range(4):
            SW[a * 4 + c, c * 4 + a] = 1
    Psym = (np.eye(16) + SW) / 2
    M2 = sum(np.kron(np.outer(u, u.conj()), np.outer(u, u.conj())) for u in states) / 20
    m2_dev = float(np.abs(M2 - 0.1 * Psym).max())
    m2_ok = bool(m2_dev < 1e-12)

    # 6. 소비 데모: MUB 단층재구성 (순수 seed=0 + 혼합)
    rng = np.random.default_rng(0)
    v = rng.standard_normal(4) + 1j * rng.standard_normal(4)
    v /= np.linalg.norm(v)
    rho_p = np.outer(v, v.conj())
    rho_m = 0.7 * rho_p + 0.3 * np.eye(4) / 4
    dev_p = float(np.abs(reconstruct(rho_p, states) - rho_p).max())
    dev_m = float(np.abs(reconstruct(rho_m, states) - rho_m).max())
    tomo_ok = bool(dev_p < 1e-12 and dev_m < 1e-12)

    # 7. teeth: T-오염(b3_s0 에 T 게이트) · 기저 제거(b5 4개)
    T = np.kron(np.diag([1, np.exp(1j * np.pi / 4)]), I2)
    bad = list(states)
    bad[8] = T @ bad[8]                      # b3_s0 오염
    fp_bad = frame_potential(bad)
    unb_bad = bool(max(abs(abs(np.vdot(bad[8], states[j])) ** 2 - 0.25)
                       for j in range(20) if basis_of[j] != 2) > 1e-6)
    drop = states[:16]                       # b5 제거 → 완비성 상실
    dev_drop = float(np.abs(reconstruct(rho_p, drop) - rho_p).max())
    teeth_ok = bool(abs(fp_bad - 0.1) > 1e-6 and unb_bad and dev_drop > 1e-3)

    p5 = observe_p5(states)
    ok = bool(seal_ok and unitary_ok and label_ok and gram_ok and fp_ok and m2_ok
              and tomo_ok and teeth_ok and p5["ok"])
    return {"p5_shadow": p5,
            "ensemble": {"n_states": 20, "bases": 5, "stabilizers": {f"b{b}": list(STAB[b]) for b in STAB},
                         "seal_link_20": seal_ok, "unitary": unitary_ok,
                         "pauli_label_map_20": label_ok, "mutually_unbiased_400": gram_ok},
            "state_2design": {"frame_potential": fp, "target": 0.1, "fp_exact": fp_ok,
                              "second_moment_dev": m2_dev, "second_moment_exact": m2_ok},
            "tomography_demo": {"pure_seed0_dev": dev_p, "mixed_dev": dev_m, "exact": tomo_ok},
            "teeth": {"t_corrupt_fp": float(fp_bad), "unbiased_broken": unb_bad,
                      "drop_basis_recon_dev": dev_drop, "detects": teeth_ok},
            "sealed_assets": "mub4_b{1..5}_s{0..3} 20 apps (Tier-0 exact, 신규 module 0)",
            "honest_boundary": "봉인=개별 상태준비 유니터리 20개뿐(정의 열만 MUB 물리). projective "
                               "state 2-design 이며 unitary 2-design 아님(G2a 하한 226 반증의 대체 "
                               "payoff). witness·단층재구성=관측(seal 아님, INV-Q3). 확률=해석값 — "
                               "유한샘플 shadow tomography 미구현(기반만).",
            "ok": ok}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        report = {"_schema": "mub-observe-v1",
                  "_note": "d=4 MUB-20(봉인 mub4_* 20 앱) = projective state 2-design witness. "
                           "봉인=유니터리뿐, design 성질·단층재구성=관측(INV-Q3).",
                  "observation": res}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        e, d2, td = res["ensemble"], res["state_2design"], res["tomography_demo"]
        print("MUB-20 projective state 2-design witness 관측:", flush=True)
        print(f"  seal링크 20/20 {e['seal_link_20']} · unitary {e['unitary']} · Pauli 라벨맵 "
              f"{e['pauli_label_map_20']} · 비편향(400쌍) {e['mutually_unbiased_400']}", flush=True)
        print(f"  FP = {d2['frame_potential']:.12f} (목표 0.1) · 2차모멘트 dev {d2['second_moment_dev']:.2e}",
              flush=True)
        print(f"  단층재구성: pure {td['pure_seed0_dev']:.2e} · mixed {td['mixed_dev']:.2e}", flush=True)
        t = res["teeth"]
        print(f"  teeth: T-오염 FP {t['t_corrupt_fp']:.6f} · 기저제거 재구성 dev {t['drop_basis_recon_dev']:.3f} "
              f"detects={t['detects']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"mub_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
