#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""qec_channel_observe — HE2 V7: 채널→QEC 완결 파이프라인 관측 (신규 봉인 0).

봉인 자산 3종을 하나의 FTQC 오류정정 고리로 맞물린다(전부 기봉인, 신규 봉인 0):
  ① repcode3_bitflip (인코더 U_enc: |ψ⟩→α|000⟩+β|111⟩)
  ② stinespring_bitflip (bit-flip 채널 dilation → 한 data 큐빗에 오류 주입)
  ③ syndrome3_bitflip (parity-copy: ancilla q3=P(d0,d1)·q4=P(d1,d2))

★핵심 사실(exact, p 무관): bit-flip 채널 = {√(1−p)I, √p X_i} 혼합, 두 Kraus 전부 weight≤1 →
  거리-3 반복코드가 신드롬으로 구별·정정 → 복원사상 R 이 R(E_i(Encode(ρ)))=ρ 를 **정확히** 만족.

관측 내용:
  1. 채널을 봉인 dilation 에서 Kraus 로 추출(sealed asset 사용) → data 큐빗 i∈{0,1,2}에 주입.
  2. 신드롬 추출(봉인 syndrome3 golden) + 코히런트 조건-X 정정 → decode → 논리 큐빗 복원.
  3. 복원 논리상태 == 원 ρ (i=0,1,2·여러 ρ·p∈{½, ¼} 전부 exact).
  4. teeth: 정정 생략 시 논리상태 훼손(복원 실패)해야.

정직 경계(INV-Q3, seal 아님, root 불변):
  - 봉인 = 인코더/dilation/syndrome 유니터리(각 Tier-0 exact)뿐. 채널·복원·측정후처리 = 관측.
  - 단일큐빗 채널만 거리-3로 exact 정정. 2큐빗 동시오류·측정 실측·decoder threshold = 차기. 신규 봉인 0.

사용: python scripts/qec_channel_observe.py [--quick]
"""
import os, sys, re, json
from functools import reduce
import numpy as np

from qf_witness.core.paths import ROOT
OUT = os.path.join(ROOT, ".pgf", "proofs", "QEC-CHANNEL-OBSERVE.json")
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)


def load_golden(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    ns = {}
    exec(re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1), ns)
    return ns["golden"]


def emb(op, q, n):
    return reduce(np.kron, [op if i == q else I for i in range(n)])


def bitflip_kraus_from_seal(p):
    """봉인 stinespring_bitflip dilation(p=½)에서 채널 구조를 확인하고, 일반 p 의 Kraus 를 반환.
    dilation 은 p=½ 를 봉인 — 그 Tr_env 가 {√½I,√½X} 임을 검증(sealed asset 연결)한 뒤,
    같은 채널족의 일반 p Kraus {√(1−p)I, √p X} 를 관측용으로 사용."""
    U = load_golden("stinespring_bitflip.app.pg")            # 2q: sys q0, env q1
    env0 = np.array([[1, 0], [0, 0]], dtype=complex)
    def E_half(rho):
        out = U @ np.kron(rho, env0) @ U.conj().T
        res = np.zeros((2, 2), dtype=complex)
        for e in range(2):
            P = np.zeros((2, 4), dtype=complex)
            for s in range(2):
                P[s, (s << 1) | e] = 1.0
            res += P @ out @ P.conj().T
        return res
    r2 = 1/np.sqrt(2)
    ref = lambda rho: r2*r2*(rho) + r2*r2*(X@rho@X)          # {√½I,√½X}
    basis = [np.array([[1,0],[0,0]],complex), np.array([[0,1],[0,0]],complex),
             np.array([[0,0],[1,0]],complex), np.array([[0,0],[0,1]],complex)]
    seal_ok = bool(max(np.abs(E_half(b) - ref(b)).max() for b in basis) < 1e-9)
    return [np.sqrt(1-p)*I, np.sqrt(p)*X], seal_ok


def apply_channel_qubit(rho, Ks, q, n):
    Es = [emb(K, q, n) for K in Ks]
    return sum(E @ rho @ E.conj().T for E in Es)


def correction_unitary():
    """5q(3 data + 2 anc) 코히런트 정정: 신드롬(q3,q4)→ data X.
      (1,0)→X_0 · (1,1)→X_1 · (0,1)→X_2 · (0,0)→I. 봉인 아님(관측용 numpy 유니터리)."""
    n = 5
    dim = 1 << n
    U = np.zeros((dim, dim), dtype=complex)
    synd_to_data = {(1, 0): 0, (1, 1): 1, (0, 1): 2}         # syndrome → 정정할 data 큐빗
    for s in range(dim):
        b = [(s >> (n - 1 - i)) & 1 for i in range(n)]
        s3, s4 = b[3], b[4]
        o = b[:]
        if (s3, s4) in synd_to_data:
            o[synd_to_data[(s3, s4)]] ^= 1                    # X on the data qubit
        j = sum(o[i] << (n - 1 - i) for i in range(n))
        U[j, s] = 1.0
    return U


def logical_recover(rho1, Ks, err_q, correct=True):
    """Encode → 채널(err_q) → syndrome → (정정) → decode → 논리 큐빗 밀도행렬 반환."""
    U_enc = load_golden("repcode3_bitflip.app.pg")           # 3q encoder
    U_syn = load_golden("syndrome3_bitflip.app.pg")          # 5q parity copy
    # 1. encode: rho1 ⊗ |0>_d1 ⊗ |0>_d2 (3q)
    enc_in = reduce(np.kron, [rho1, np.array([[1,0],[0,0]],complex), np.array([[1,0],[0,0]],complex)])
    rho3 = U_enc @ enc_in @ U_enc.conj().T
    # 2. channel on err_q (3q)
    rho3 = apply_channel_qubit(rho3, Ks, err_q, 3)
    # 3. append 2 ancilla |00>, syndrome extract (5q)
    anc = np.zeros((4, 4), dtype=complex); anc[0, 0] = 1.0
    rho5 = np.kron(rho3, anc)
    rho5 = U_syn @ rho5 @ U_syn.conj().T
    # 4. coherent correction
    if correct:
        C = correction_unitary()
        rho5 = C @ rho5 @ C.conj().T
    # 5. decode: inverse encoder on the 3 data qubits (⊗ I on 2 anc)
    U_dec = np.kron(U_enc.conj().T, np.eye(4, dtype=complex))
    rho5 = U_dec @ rho5 @ U_dec.conj().T
    # 6. trace out data-anc(q1,q2) + syndrome(q3,q4) → keep logical q0
    return _ptrace_keep0(rho5, 5)


def _ptrace_keep0(rho, n):
    """q0 만 남기고 나머지 trace out."""
    keep = 1 << (n - 1)
    res = np.zeros((2, 2), dtype=complex)
    for r in range(keep):
        Pr = np.zeros((2, 1 << n), dtype=complex)
        for a in range(2):
            Pr[a, (a << (n - 1)) | r] = 1.0
        res += Pr @ rho @ Pr.conj().T
    return res


def observe():
    states = {
        "|0>": np.array([[1, 0], [0, 0]], dtype=complex),
        "|+>": np.array([[0.5, 0.5], [0.5, 0.5]], dtype=complex),
        "| psi>": np.array([[0.7, 0.3-0.2j], [0.3+0.2j, 0.3]], dtype=complex),
    }
    rows, corrected_ok, teeth_any_fail = [], True, False
    n_cases = 0
    seal_link = None
    for p in (0.5, 0.25):
        Ks, seal_ok = bitflip_kraus_from_seal(p)
        seal_link = seal_ok if seal_link is None else (seal_link and seal_ok)
        for err_q in (0, 1, 2):
            for sname, rho in states.items():
                n_cases += 1
                rec = logical_recover(rho, Ks, err_q, correct=True)
                fid = float(np.abs(rec - rho).max())
                good = fid < 1e-9
                corrected_ok = corrected_ok and good
                # 전역 teeth: 정정 없으면 이 케이스가 훼손되나? (계산기저×ancilla-매핑 오류는 자연보호 —
                #   최소 1 케이스가 실패하면 '정정이 실제로 일하고 있음'을 실증)
                bad = logical_recover(rho, Ks, err_q, correct=False)
                if float(np.abs(bad - rho).max()) > 1e-6:
                    teeth_any_fail = True
                if not good:
                    rows.append({"p": p, "err_q": err_q, "state": sname, "recover_err": fid})
    ok = corrected_ok and teeth_any_fail
    return {"axis": "채널→QEC 완결 파이프라인 (오류 주입→신드롬→정정→복원)",
            "sealed_assets": "repcode3_bitflip(인코더)·stinespring_bitflip(채널)·syndrome3_bitflip(신드롬)",
            "sealed_channel_link_verified": bool(seal_link),
            "exact_recovery_all": bool(corrected_ok),
            "n_cases": n_cases,
            "teeth_uncorrected_fails": bool(teeth_any_fail),
            "cases": "p∈{½,¼} × err_q∈{0,1,2} × 3 상태 = 18 케이스 전부 R(E_i(Encode(ρ)))=ρ exact "
                     "(정정 생략 시 최소 1 케이스 훼손=teeth). ★계산기저×비-q0 오류는 코드가 자연보호.",
            "failures": rows,
            "honest_boundary": "봉인=인코더/dilation/syndrome 유니터리뿐(각 Tier-0 exact). 채널·복원·측정후처리"
                               "=관측. 단일큐빗 채널만 거리-3 exact 정정; 2큐빗 동시오류·측정 실측·decoder"
                               " threshold=차기. 신규 봉인 0(INV-Q3).",
            "ok": bool(ok)}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        report = {"_schema": "qec-channel-observe-v1",
                  "_note": "봉인 채널로 오류 주입 → 봉인 QEC 로 정정 → 논리상태 exact 복원. 신규 봉인 0(INV-Q3).",
                  "observation": res}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("채널→QEC 완결 파이프라인 관측:", flush=True)
        print(f"  봉인 채널 링크(stinespring_bitflip=Tr_env→{{√½I,√½X}}): {res['sealed_channel_link_verified']}", flush=True)
        print(f"  exact 복원({res['n_cases']} 케이스 p∈{{½,¼}}×err_q×상태): {res['exact_recovery_all']} · 실패 {len(res['failures'])}건 · teeth(정정필요): {res['teeth_uncorrected_fails']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"qec_channel_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
