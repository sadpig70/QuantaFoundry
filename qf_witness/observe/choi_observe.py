#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""choi_observe — HE3 H3.3: Choi–Jamiołkowski channel-state duality witness (신규 봉인 0).

봉인된 choi_bitflip/phasedamp/ampdamp(3q)·choi_depol(4q)에 대해:
  1. seal 링크 + 준비 유니터리 unitarity.
  2. J(E) = Tr_env[U|0…0⟩⟨0…0|U†] 계산(ref⊗sys 4×4) → ★CP: J⪰0 · TP: Tr_sys J = I_ref/2.
  3. ★duality(채널 재구성): E(|r⟩⟨r'|)[s,s'] = 2·J[(r,s),(r',s')] 로 J→E 재구성 == 목표 Kraus 채널 exact
     — 상태 하나(J)가 채널 전체(E)를 결정하는 CJ 동형의 직접 검증.
  4. depol 극단: J == I₄/4 (최대혼합 Choi ⟺ 완전 망각 채널).
  5. teeth: 틀린 채널(Kraus p=0.3)의 Choi 는 불일치해야.

정직 경계(INV-Q3 상속): 봉인=Choi 상태 *준비 유니터리*(Tier-0 exact)뿐. Choi 행렬 J(부분대각합)·
  채널 재구성·CP/TP=비유니터리 관측(seal 아님). V6 채널 dilation 봉인의 duality 짝 자산화.

사용: python scripts/choi_observe.py [--quick]
"""
import os, sys, re, json
import numpy as np

from qf_witness.core.paths import ROOT
OUT = os.path.join(ROOT, ".pgf", "proofs", "CHOI-OBSERVE.json")

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def load_golden(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    ns = {}
    exec(re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1), ns)
    return ns["golden"]


def seal_link(app_id):
    p = os.path.join(ROOT, "registry", "apps", f"{app_id}.sealed.json")
    return os.path.exists(p) and bool(json.load(open(p, encoding="utf-8")).get("u_hash"))


def kraus(name, p=0.5):
    r = np.sqrt(p)
    q = np.sqrt(1 - p)
    if name == "bitflip":
        return [q * I, r * X]
    if name == "phasedamp":
        return [np.diag([1, q]).astype(complex), np.diag([0, r]).astype(complex)]
    if name == "ampdamp":
        return [np.diag([1, q]).astype(complex), np.array([[0, r], [0, 0]], dtype=complex)]
    if name == "depol":
        return [0.5 * I, 0.5 * X, 0.5 * Y, 0.5 * Z]
    raise ValueError(name)


def choi_from_prep(U, n_env):
    """|0..0⟩ 준비 → env 부분대각합 → J (ref⊗sys 4×4)."""
    n = 2 + n_env
    dim = 2 ** n
    psi = np.zeros(dim, dtype=complex); psi[0] = 1.0
    out = U @ psi
    rho = np.outer(out, out.conj())
    d_env = 2 ** n_env
    J = np.zeros((4, 4), dtype=complex)
    for e in range(d_env):
        P = np.zeros((4, dim), dtype=complex)
        for rs in range(4):
            P[rs, rs * d_env + e] = 1.0
        J += P @ rho @ P.conj().T
    return J


def choi_from_kraus(Ks):
    """J = (I⊗E)(|Φ⁺⟩⟨Φ⁺|), basis (ref,sys): J[(r,s),(r',s')] = <s|E(|r><r'|)|s'>/2."""
    J = np.zeros((4, 4), dtype=complex)
    for r in range(2):
        for rp in range(2):
            Ers = sum(K @ np.outer(np.eye(2)[r], np.eye(2)[rp].conj()) @ K.conj().T for K in Ks)
            for s in range(2):
                for sp in range(2):
                    J[r * 2 + s, rp * 2 + sp] = Ers[s, sp] / 2
    return J


def reconstruct_channel(J):
    """E(|r><r'|)[s,s'] = 2·J[(r,s),(r',s')] — 채널의 기저 작용 재구성."""
    E = {}
    for r in range(2):
        for rp in range(2):
            M = np.zeros((2, 2), dtype=complex)
            for s in range(2):
                for sp in range(2):
                    M[s, sp] = 2 * J[r * 2 + s, rp * 2 + sp]
            E[(r, rp)] = M
    return E


def observe():
    cases = [("choi_bitflip", "bitflip", 1), ("choi_phasedamp", "phasedamp", 1),
             ("choi_ampdamp", "ampdamp", 1), ("choi_depol", "depol", 2)]
    rows, all_ok = [], True
    for app_id, ch, n_env in cases:
        U = load_golden(f"{app_id}.app.pg")
        n = 2 + n_env
        unitary = bool(np.allclose(U.conj().T @ U, np.eye(2 ** n), atol=1e-12))
        J = choi_from_prep(U, n_env)
        Jk = choi_from_kraus(kraus(ch))
        dual = float(np.abs(J - Jk).max())
        cp = float(np.linalg.eigvalsh(J).min())
        tp = float(np.abs(sum(
            np.array([[J[r * 2 + s, rp * 2 + s] for rp in range(2)] for r in range(2)])
            for s in range(2)) - I / 2).max())
        # duality: J→E 재구성 == Kraus 채널 기저 작용
        E = reconstruct_channel(J)
        Ks = kraus(ch)
        recon = 0.0
        for r in range(2):
            for rp in range(2):
                ref = sum(K @ np.outer(np.eye(2)[r], np.eye(2)[rp].conj()) @ K.conj().T for K in Ks)
                recon = max(recon, float(np.abs(E[(r, rp)] - ref).max()))
        link = seal_link(app_id)
        row = {"app": app_id, "channel": ch, "seal_link": link, "unitary": unitary,
               "choi_match_kraus": dual, "CP_min_eig": cp, "TP_dev": tp,
               "duality_reconstruction_dev": recon}
        if ch == "depol":
            row["J_eq_I4_over_4"] = float(np.abs(J - np.eye(4) / 4).max())
        row["ok"] = bool(link and unitary and dual < 1e-12 and cp > -1e-12 and tp < 1e-12
                         and recon < 1e-12 and (ch != "depol" or row["J_eq_I4_over_4"] < 1e-12))
        rows.append(row)
        all_ok = all_ok and row["ok"]
    # teeth: 틀린 p=0.3 Kraus 의 Choi 는 봉인 J 와 불일치해야
    Jgood = choi_from_prep(load_golden("choi_bitflip.app.pg"), 1)
    teeth = bool(np.abs(Jgood - choi_from_kraus(kraus("bitflip", p=0.3))).max() > 1e-3)
    ok = bool(all_ok and teeth)
    return {"chois": rows, "teeth_wrong_p_detected": teeth,
            "sealed_assets": "choi_bitflip/phasedamp/ampdamp/depol (준비 유니터리 Tier-0 exact, "
                             "Bell+기봉인 stinespring_* sub-app 복리, 신규 module 0)",
            "honest_boundary": "봉인=Choi 상태 준비 유니터리뿐. J(부분대각합)·CP/TP·채널 재구성=관측"
                               "(INV-Q3). 일반 p·qubit>1 채널·process tomography=차기.",
            "ok": ok}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"_schema": "choi-observe-v1",
                       "_note": "Choi duality witness: J==Kraus-Choi·CP/TP·J→E 재구성 exact. 봉인=유니터리뿐.",
                       "observation": res}, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("Choi channel-state duality witness 관측:", flush=True)
        for r in res["chois"]:
            extra = f" · J==I/4 {r['J_eq_I4_over_4']:.1e}" if "J_eq_I4_over_4" in r else ""
            print(f"  {r['app']:15}: seal {r['seal_link']} · J==Kraus {r['choi_match_kraus']:.1e} · "
                  f"CP {r['CP_min_eig']:.1e} · TP {r['TP_dev']:.1e} · 재구성 {r['duality_reconstruction_dev']:.1e}{extra}",
                  flush=True)
        print(f"  teeth p=0.3 검출 {res['teeth_wrong_p_detected']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"choi_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
