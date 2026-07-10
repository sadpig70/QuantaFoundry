#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""flag_syndrome_observe — TrackR3Residue C7: 1-flag FT 증후 추출 witness (신규 봉인 0).

봉인된 flag_synd_zzzz/xxxx(6q: d0..3·anc q4·flag q5, [[4,2,2]] stabilizer 쌍, 전부 h/cnot)에 대해:
  1. seal 링크(앱 2 + 복리 대상 surf422_encoder) + golden 유니터리성 + xxxx==H⊗4·zzzz·H⊗4 켤레 exact.
  2. 증후 정확성: 데이터 기저 16 전수 — anc=parity(d)·flag=0 (zzzz) · XXXX 고유상태 표본 (xxxx).
  3. ★flag 정리(Pauli 전파, 기호 exact): 단일 Z_anc fault 를 회로 전 위치(9곳)에 주입 —
     **무flag ⇒ 잔여 데이터 Z-string ≡ weight ≤1 (mod ZZZZ)**. 위험 fault(w_eff=2)는 반드시 flag.
     (X_anc·flag 자체 fault 는 증후/flag 판독 오류로만 전파 — 데이터 무해, 판정에 포함.)
  4. ★복리: surf422_encoder codeword 4/4 → 두 추출 모두 무증후·무flag exact (stabilizer 쌍 완성).
  5. teeth 2종: ①무flag 회로(flag CNOT 제거) — unflagged w_eff=2 hook 존재(flag 층의 하중 실증).
     ②flag 창 오배치(두 flag CNOT 인접) — 위험 fault 가 unflagged 로 새는 것 검출.

정직 경계(INV-Q3, seal 아님, root 성장은 앱 2 봉인분뿐):
  - 봉인 = coherent 추출 유니터리(측정 지연)뿐. flag 정리·hook = Pauli 전파 witness(관측).
  - 실제 측정·decoder(flag 조건부 정정표)·반복 추출 프로토콜·d≥3 코드 = 범위 밖(차기).
  - 기존 syndrome3_bitflip(비-FT 추출)·surf422(인코더)와의 관계: 이 앱들이 FT-추출 층을 새로 개창.

사용: python -m qf_witness.observe.flag_syndrome_observe [--quick]
"""
import os, sys, re, json
import numpy as np

from qf_witness.core.paths import ROOT
OUT = os.path.join(ROOT, ".pgf", "proofs", "FLAG-SYNDROME-OBSERVE.json")

H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)

GATES_Z = [("h", 5), ("cx", 0, 4), ("cx", 5, 4), ("cx", 1, 4),
           ("cx", 2, 4), ("cx", 5, 4), ("cx", 3, 4), ("h", 5)]
GATES_NF = [("cx", 0, 4), ("cx", 1, 4), ("cx", 2, 4), ("cx", 3, 4)]
GATES_BAD = [("h", 5), ("cx", 0, 4), ("cx", 5, 4), ("cx", 5, 4), ("cx", 1, 4),
             ("cx", 2, 4), ("cx", 3, 4), ("h", 5)]      # flag 창 오배치(인접)


def load_golden(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    ns = {}
    exec(re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1), ns)
    return ns["golden"]


def seal_link(sid):
    p = os.path.join(ROOT, "registry", "apps", f"{sid}.sealed.json")
    return os.path.exists(p) and bool(json.load(open(p, encoding="utf-8")).get("u_hash"))


def propagate(x, z, gates):
    x, z = list(x), list(z)
    for g in gates:
        if g[0] == "h":
            q = g[1]; x[q], z[q] = z[q], x[q]
        else:
            c, t = g[1], g[2]
            if x[c]:
                x[t] ^= 1
            if z[t]:
                z[c] ^= 1
    return x, z


def flag_theorem(gates):
    """전 위치 Z_anc fault: (all_safe, hook_exists, rows). trivial=첫 data-CNOT 이전(anc=|0⟩)."""
    first_cx = next(i for i, g in enumerate(gates) if g[0] == "cx" and g[2] == 4)
    all_ok, hook, rows = True, False, []
    for loc in range(len(gates) + 1):
        z0 = [0] * 6; z0[4] = 1
        x, z = propagate([0] * 6, z0, gates[loc:])
        flagged = bool(x[5])
        zw = sum(z[q] for q in range(4))
        w_eff = min(zw, 4 - zw)
        trivial = loc <= first_cx
        safe = trivial or flagged or (w_eff <= 1)
        all_ok &= safe
        if (not trivial) and (not flagged) and w_eff >= 2:
            hook = True
        rows.append({"loc": loc, "state": "triv" if trivial else ("flag" if flagged else "no-flag"),
                     "z_weight": zw, "w_eff_mod_stab": w_eff, "safe": bool(safe)})
    return bool(all_ok), bool(hook), rows


def observe():
    Uz = load_golden("flag_synd_zzzz.app.pg")
    Ux = load_golden("flag_synd_xxxx.app.pg")
    links = all(seal_link(s) for s in ("flag_synd_zzzz", "flag_synd_xxxx", "surf422_encoder"))
    unit = bool(np.allclose(Uz.conj().T @ Uz, np.eye(64), atol=1e-12)
                and np.allclose(Ux.conj().T @ Ux, np.eye(64), atol=1e-12))
    # xxxx == H⊗4 켤레
    H4 = np.eye(1, dtype=complex)
    for _ in range(4):
        H4 = np.kron(H4, H)
    H4 = np.kron(H4, np.eye(4, dtype=complex))
    conj_ok = bool(np.allclose(Ux, H4 @ Uz @ H4, atol=1e-12))

    # 2. 증후 정확성
    synd_ok = True
    for d in range(16):
        out = Uz[:, d << 2]
        j = int(np.argmax(np.abs(out)))
        synd_ok &= bool(abs(abs(out[j]) - 1) < 1e-12 and (j >> 2) == d
                        and ((j >> 1) & 1) == bin(d).count("1") % 2 and (j & 1) == 0)
    plus = np.array([1, 1], dtype=complex) / np.sqrt(2)
    minus = np.array([1, -1], dtype=complex) / np.sqrt(2)
    for signs in [(0, 0, 0, 0), (1, 0, 0, 0), (1, 1, 0, 0), (1, 1, 1, 1)]:
        v = np.array([1], dtype=complex)
        for s in signs:
            v = np.kron(v, minus if s else plus)
        out = Ux @ np.kron(v, np.array([1, 0, 0, 0], dtype=complex))
        par = sum(signs) % 2
        bad = max(abs(out[j]) for j in range(64) if ((j >> 1) & 1) != par or (j & 1) != 0)
        synd_ok &= bool(bad < 1e-12)

    # 3. flag 정리
    thm_ok, _, rows = flag_theorem(GATES_Z)
    # X_anc·flag 자체 fault 무해성(전파상 데이터 성분 0)
    aux_ok = True
    for fq, xz in [(4, "x"), (5, "x"), (5, "z")]:
        for loc in range(len(GATES_Z) + 1):
            p0x, p0z = [0] * 6, [0] * 6
            (p0x if xz == "x" else p0z)[fq] = 1
            x, z = propagate(p0x, p0z, GATES_Z[loc:])
            if any(x[q] or z[q] for q in range(4)):
                aux_ok = False

    # 4. surf422 복리
    ENC = load_golden("surf422_encoder.app.pg")
    comp_ok = True
    for a in range(2):
        for b in range(2):
            psi = np.kron(ENC[:, (a << 2) | (b << 1)], np.array([1, 0, 0, 0], dtype=complex))
            for U in (Uz, Ux):
                out = U @ psi
                bad = max(abs(out[j]) for j in range(64) if (j & 3) != 0)
                comp_ok &= bool(bad < 1e-12)

    # 5. teeth
    _, hook_nf, _ = flag_theorem(GATES_NF)
    bad_ok, hook_bad, _ = flag_theorem(GATES_BAD)
    teeth_ok = bool(hook_nf and (not bad_ok) and hook_bad)

    ok = bool(links and unit and conj_ok and synd_ok and thm_ok and aux_ok and comp_ok and teeth_ok)
    return {"axis": "FT 증후 추출 프리미티브(1-flag) — 비-FT syndrome3 와 대조되는 새 층",
            "seal_links": links, "unitary": unit, "xxxx_eq_H4_conj": conj_ok,
            "syndrome_correct": synd_ok,
            "flag_theorem": {"all_faults_safe": thm_ok, "aux_faults_harmless": aux_ok,
                             "locations": rows},
            "surf422_compounding_4x2_clean": comp_ok,
            "teeth": {"noflag_circuit_has_hook": hook_nf,
                      "misplaced_window_fails": bool(not bad_ok and hook_bad)},
            "honest_boundary": "봉인=coherent 추출 유니터리 2개뿐. flag 정리·hook=Pauli 전파 witness"
                               "(관측, INV-Q3). 측정·decoder·반복 프로토콜·d≥3=차기. 신규 module 0.",
            "ok": ok}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"_schema": "flag-syndrome-observe-v1",
                       "_note": "1-flag FT 증후 추출 witness: flag 정리+hook teeth+surf422 복리. "
                                "봉인=유니터리뿐(INV-Q3).",
                       "observation": res}, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        t = res["teeth"]
        print("1-flag FT 증후 추출 witness 관측 (flag_synd_zzzz/xxxx):", flush=True)
        print(f"  seal {res['seal_links']} · unitary {res['unitary']} · XXXX==H⊗4켤레 "
              f"{res['xxxx_eq_H4_conj']} · 증후 정확성 {res['syndrome_correct']}", flush=True)
        ft = res["flag_theorem"]
        print(f"  ★flag 정리(9위치): {ft['all_faults_safe']} · 보조 fault 무해 {ft['aux_faults_harmless']} "
              f"· surf422 복리 4×2 {res['surf422_compounding_4x2_clean']}", flush=True)
        print(f"  teeth: 무flag hook {t['noflag_circuit_has_hook']} · 창 오배치 검출 "
              f"{t['misplaced_window_fails']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"flag_syndrome_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
