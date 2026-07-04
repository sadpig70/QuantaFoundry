#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""twodesign_observe — HE2 V8: 1q Clifford 군 = 정확 unitary 2/3-design witness (신규 봉인 0).

봉인된 cliff1_* 24개 앱(C₁ 전 원소, plan=기봉인 h_gate/s_gate word)에 대해:
  1. ★seal 링크: 24개 전부 registry/apps/<id>.sealed.json 존재 + u_hash 보유.
  2. 유니터리성: 각 golden U†U=I exact.
  3. ★군 폐포: 24원소가 mod-phase 로 전부 상이 + 곱셈표가 집합 안에 닫힘(576 곱 전수).
  4. ★frame potential(군 평균): F_t = (1/|G|²) Σ_{g,h} |Tr(U_g†U_h)|^{2t}
       F₁=1 (1-design) · F₂=2 (정확 unitary 2-design, d=2 Haar 필요충분) ·
       F₃=5 (정확 3-design, d=2 Haar ∫|Tr U|⁶=5 일치) — 기계정밀도 exact.
  5. 1-design twirl: (1/24) Σ U|0⟩⟨0|U† = I/2 (완전 스크램블).
  6. teeth: 원소 1개 제거(F₂=2.026…) · S→T 오염(비-Clifford 치환, F₂=2.015…) → 이탈 검출.

정직 경계(INV-Q3, seal 아님, root 성장은 24개 앱 봉인분뿐):
  - 봉인 = 개별 Clifford 유니터리 24개(Tier-0 exact)뿐. 2/3-design *성질* = 군 평균
    (초연산자/모멘트 평균) → 관측(seal 아님). frame potential 은 Haar 적분과의 대조.
  - RB(randomized benchmarking)·shadow tomography 자체는 미구현 — 그 기반(정확 2-design)만 확보.
  - 2q Clifford 군(11520원소)=차기(전수 봉인 비현실 → 표본화/생성원 설계 필요).

사용: python scripts/twodesign_observe.py [--quick]
"""
import os, sys, re, json
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".pgf", "proofs", "TWODESIGN-OBSERVE.json")

WORDS = ["id", "h", "s", "hs", "sh", "ss", "hsh", "hss", "shs", "ssh", "sss",
         "hshs", "hssh", "hsss", "shss", "sshs", "hshss", "hsshs", "shssh",
         "shsss", "sshss", "hshssh", "hshsss", "hsshss"]
HAAR_D2 = {1: 1.0, 2: 2.0, 3: 5.0}   # ∫_{U(2)} |Tr U|^{2t} dU (t=3: d=2 값, t!=6 아님에 주의)


def load_golden(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    ns = {}
    exec(re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1), ns)
    return ns["golden"]


def canon_key(U, tol=1e-9):
    flat = U.flatten()
    idx = np.argmax(np.abs(flat) > tol)
    Un = U * (np.conj(flat[idx]) / np.abs(flat[idx]))
    return tuple(np.round(Un.flatten(), 6).tolist())


def frame_potential(mats, t):
    n = len(mats)
    tot = 0.0
    for A in mats:
        for B in mats:
            tot += abs(np.trace(A.conj().T @ B)) ** (2 * t)
    return float(tot / n ** 2)


def observe():
    # 1. seal 링크 + golden 로드
    Us, seal_ok = [], True
    for w in WORDS:
        app_id = f"cliff1_{w}"
        sealed = os.path.join(ROOT, "registry", "apps", f"{app_id}.sealed.json")
        if not (os.path.exists(sealed) and json.load(open(sealed, encoding="utf-8")).get("u_hash")):
            seal_ok = False
        Us.append(load_golden(f"{app_id}.app.pg"))

    # 2. 유니터리성
    unitary_ok = bool(all(np.allclose(U.conj().T @ U, np.eye(2), atol=1e-12) for U in Us))

    # 3. 군 폐포 (mod phase): 24 상이 + 576 곱 전수 폐쇄
    keys = {canon_key(U) for U in Us}
    distinct_ok = bool(len(keys) == 24)
    closure_ok = bool(all(canon_key(A @ B) in keys for A in Us for B in Us))

    # 4. frame potentials
    fp = {}
    fp_ok = True
    for t in (1, 2, 3):
        F = frame_potential(Us, t)
        fp[f"F{t}"] = {"value": float(F), "haar_d2": HAAR_D2[t], "diff": float(abs(F - HAAR_D2[t]))}
        fp_ok = bool(fp_ok and abs(F - HAAR_D2[t]) < 1e-9)

    # 5. 1-design twirl: (1/24) Σ U|0⟩⟨0|U† == I/2
    rho0 = np.array([[1, 0], [0, 0]], dtype=complex)
    twirl = sum(U @ rho0 @ U.conj().T for U in Us) / 24
    twirl_dev = float(np.abs(twirl - np.eye(2) / 2).max())
    twirl_ok = bool(twirl_dev < 1e-12)

    # 6. teeth: 원소 제거 / S→T 오염 → F₂가 2 에서 이탈해야
    F2_drop = frame_potential(Us[1:], 2)
    T = np.diag([1, np.exp(1j * np.pi / 4)]).astype(complex)
    bad = list(Us)
    bad[WORDS.index("s")] = T
    F2_corrupt = frame_potential(bad, 2)
    teeth_ok = bool(abs(F2_drop - 2) > 1e-6 and abs(F2_corrupt - 2) > 1e-6)

    ok = bool(seal_ok and unitary_ok and distinct_ok and closure_ok and fp_ok and twirl_ok and teeth_ok)
    return {"group": {"order": 24, "generators": "h_gate·s_gate (기봉인)", "max_word_len": 6,
                      "seal_link_24": seal_ok, "unitary": unitary_ok,
                      "distinct_mod_phase": distinct_ok, "closure_576_products": closure_ok},
            "frame_potentials": fp,
            "twirl_rho0_to_maximally_mixed": {"max_dev": twirl_dev, "ok": twirl_ok},
            "teeth": {"drop_one_F2": float(F2_drop), "s_to_t_corrupt_F2": float(F2_corrupt),
                      "detects": teeth_ok},
            "sealed_assets": "cliff1_* 24 apps (C1 전 원소, Tier-0 exact, 신규 module 0)",
            "honest_boundary": "봉인=개별 Clifford 유니터리 24개뿐. 2/3-design 성질=frame potential "
                               "군 평균(Haar 모멘트 대조)→관측(seal 아님, INV-Q3). RB·shadow tomography "
                               "미구현(기반만). 2q Clifford(11520)=차기.",
            "ok": ok}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        report = {"_schema": "twodesign-observe-v1",
                  "_note": "1q Clifford 군(cliff1_* 24 봉인 앱) = 정확 unitary 2/3-design witness. "
                           "봉인=유니터리뿐, design 성질=관측(INV-Q3).",
                  "observation": res}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        g = res["group"]
        print("unitary 2-design witness 관측 (1q Clifford 군 C1):", flush=True)
        print(f"  seal링크 24/24 {g['seal_link_24']} · unitary {g['unitary']} · "
              f"상이 {g['distinct_mod_phase']} · 폐포(576곱) {g['closure_576_products']}", flush=True)
        for t in (1, 2, 3):
            f_ = res["frame_potentials"][f"F{t}"]
            print(f"  F{t} = {f_['value']:.12f} (Haar={f_['haar_d2']}) diff={f_['diff']:.2e}", flush=True)
        print(f"  twirl |0⟩⟨0|→I/2 dev {res['twirl_rho0_to_maximally_mixed']['max_dev']:.2e} · "
              f"teeth drop/corrupt F2 {res['teeth']['drop_one_F2']:.6f}/{res['teeth']['s_to_t_corrupt_F2']:.6f} "
              f"detects={res['teeth']['detects']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"twodesign_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
