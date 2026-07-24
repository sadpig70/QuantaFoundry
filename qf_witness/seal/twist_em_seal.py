#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""twist_em_seal.py — TrackHE18 잔여(report18 agent03 후반): twist 코드의 **e↔m 교환 논리 게이트**
(논리 Hadamard) 물리 Clifford 실현 `twist_em_h16` Tier-2 봉인.

[[twist_defect_seal]](twist_defect16, [[16,2,2]])의 payoff: twist-braid 가 유도하는 e↔m anyon 교환의
**대수적 내용 = 논리 X↔Z 교환 = 논리 Hadamard** 를 물리 16-큐빗 Clifford 회로로 실현:

    U = E · H(q_L1) · E†    (E = twist_defect16 인코더, q_L1=9: E Z₉E† ≡ LZ1·S — 논리1 방향)

검증(봉인 전 driver 자체 게이트, 전부 exact tableau conjugation):
  - **U S_i U† ∈ +S군 전수**(14 stabilizer·부호 포함) — 코드 보존 자기동형
  - **U LZ1 U† ≡ LX1 · U LX1 U† ≡ LZ1**(mod S·부호 정확) — ★e↔m 교환의 논리 사상(논리 H₁)
  - **논리2 완전 불변** · **U² = I**(involution — e↔m 교환 order 2)
봉인: verify_seal tier="clifford" 정준 tableau → registry/modules. 독립 재확인 = canonical_tableau_hash.
정직 경계: **인코더-conjugation 실현**(twist defect 물리 이동/측정 스케줄 아님 — fault-tolerant braid
  스케줄=범위밖) · e↔m 서사의 대수 내용(tableau 사상)만 봉인. witness=twist_em_observe(오라클 독립).

사용: python -m qf_witness.seal.twist_em_seal
"""
from __future__ import annotations
import os
import sys
import json
import subprocess

from qf_witness.core.paths import ROOT
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, ORACLE)
import verify_seal as vs        # noqa: E402
import clifford_seal as cs      # noqa: E402

from qf_witness.seal.twist_defect_seal import (precheck, synthesize, N)   # noqa: E402

SPECS_MODS = os.path.join(ROOT, "specs", "modules")
MODREG = os.path.join(ROOT, "registry", "modules")
QL1 = 9         # 논리1 방향 물리 큐빗 (E Z9 E† ≡ LZ1·S — driver 에서 검증)


def conj_track(gates, init):
    r = list(init)
    for g in gates:
        if g[0] == "h":
            q = g[1]
            xb = (r[0] >> q) & 1
            zb = (r[1] >> q) & 1
            r[2] ^= xb & zb
            if xb != zb:
                r[0] ^= (1 << q)
                r[1] ^= (1 << q)
        elif g[0] == "s":
            q = g[1]
            if (r[0] >> q) & 1:
                r[2] ^= (r[1] >> q) & 1
                r[1] ^= (1 << q)
        elif g[0] == "cx":
            c, t = g[1], g[2]
            xc = (r[0] >> c) & 1
            zt = (r[1] >> t) & 1
            xt = (r[0] >> t) & 1
            zc = (r[1] >> c) & 1
            r[2] ^= xc & zt & (xt ^ zc ^ 1)
            if xc:
                r[0] ^= (1 << t)
            if zt:
                r[1] ^= (1 << c)
        elif g[0] == "cz":
            a, b = g[1], g[2]
            for gg in [("h", b), ("cx", a, b), ("h", b)]:
                r = conj_track([gg], r)
        elif g[0] == "x":
            r[2] ^= (r[1] >> g[1]) & 1
        elif g[0] == "z":
            r[2] ^= (r[0] >> g[1]) & 1
    return r


def _g_phase(x1, z1, x2, z2):
    tot = 0
    for q in range(N):
        a = (x1 >> q) & 1
        b = (z1 >> q) & 1
        c = (x2 >> q) & 1
        d = (z2 >> q) & 1
        if a == 0 and b == 0:
            g = 0
        elif a == 1 and b == 1:
            g = d - c
        elif a == 1 and b == 0:
            g = d * (2 * c - 1)
        else:
            g = c * (1 - 2 * d)
        tot += g
    return tot


def build_and_verify():
    S, LZ1, LZ2 = precheck()
    enc = synthesize(S, LZ1, LZ2)
    enc_inv = []
    for g in reversed(enc):
        enc_inv += [g, g, g] if g[0] == "s" else [g]
    U = enc_inv + [("h", QL1)] + enc

    # 부호 포함 S군 멤버십
    def member_sign(t):
        basis = []
        fin = [[s[0], s[1], 0] for s in S]
        for i, r in enumerate(fin):
            v = (r[0] << N) | r[1]
            c = 1 << i
            for (bv, bc) in basis:
                top = bv.bit_length() - 1
                if (v >> top) & 1:
                    v ^= bv
                    c ^= bc
            if v:
                basis.append((v, c))
                basis.sort(key=lambda p: -p[0].bit_length())
        v = (t[0] << N) | t[1]
        c = 0
        for (bv, bc) in basis:
            top = bv.bit_length() - 1
            if (v >> top) & 1:
                v ^= bv
                c ^= bc
        if v:
            return None
        acc = [0, 0, 0]
        for i in range(14):
            if (c >> i) & 1:
                ph = (2 * acc[2] + 2 * fin[i][2]
                      + _g_phase(acc[0], acc[1], fin[i][0], fin[i][1])) % 4
                acc = [acc[0] ^ fin[i][0], acc[1] ^ fin[i][1], (ph // 2) % 2]
        return acc

    # 1) stab 보존
    for s in S:
        r = conj_track(U, [s[0], s[1], 0])
        acc = member_sign((r[0], r[1]))
        assert acc is not None and (acc[2] ^ r[2]) == 0, "stab 비보존"
    # 2) 논리 사상 (교환·부호)
    LZ1e = conj_track(enc, [0, 1 << QL1, 0])
    LX1e = conj_track(enc, [1 << QL1, 0, 0])
    LZ2e = conj_track(enc, [0, 1 << 15, 0])
    LX2e = conj_track(enc, [1 << 15, 0, 0])

    def maps(src, dst):
        r = conj_track(U, list(src))
        acc = member_sign((r[0] ^ dst[0], r[1] ^ dst[1]))
        if acc is None:
            return False
        ph = (2 * dst[2] + 2 * acc[2] + _g_phase(dst[0], dst[1], acc[0], acc[1])) % 4
        return r[2] == (ph // 2) % 2
    assert maps(LZ1e, LX1e) and maps(LX1e, LZ1e), "논리1 e↔m 교환 실패"
    assert maps(LZ2e, LZ2e) and maps(LX2e, LX2e), "논리2 불변 실패"
    # 3) U²=I
    for q in range(N):
        assert conj_track(U + U, [1 << q, 0, 0]) == [1 << q, 0, 0]
        assert conj_track(U + U, [0, 1 << q, 0]) == [0, 1 << q, 0]
    return U


def _bloq_code(n, gates):
    L = ["from qualtran import BloqBuilder",
         "from qualtran.bloqs.basic_gates import Hadamard, SGate, CNOT, CZ, XGate, ZGate",
         "bb = BloqBuilder()",
         f"qs = [bb.add_register(f'q{{i}}', 1) for i in range({n})]"]
    for g in gates:
        if g[0] == "h":
            L.append(f"qs[{g[1]}] = bb.add(Hadamard(), q=qs[{g[1]}])")
        elif g[0] == "s":
            L.append(f"qs[{g[1]}] = bb.add(SGate(), q=qs[{g[1]}])")
        elif g[0] == "cx":
            c, t = g[1], g[2]
            L.append(f"qs[{c}], qs[{t}] = bb.add(CNOT(), ctrl=qs[{c}], target=qs[{t}])")
        elif g[0] == "cz":
            a, b = g[1], g[2]
            L.append(f"qs[{a}], qs[{b}] = bb.add(CZ(), q1=qs[{a}], q2=qs[{b}])")
        elif g[0] == "x":
            L.append(f"qs[{g[1]}] = bb.add(XGate(), q=qs[{g[1]}])")
        elif g[0] == "z":
            L.append(f"qs[{g[1]}] = bb.add(ZGate(), q=qs[{g[1]}])")
    L.append(f"bloq = bb.finalize(**{{f'q{{i}}': qs[i] for i in range({n})}})")
    return "\n".join(L)


HEADER = ("twist_em_h16 — twist-defect [[16,2,2]] 의 e↔m 교환 논리 게이트(논리 Hadamard₁) 물리 Clifford "
          "실현: U=E·H(9)·E† (E=twist_defect16 인코더). 검증(driver 게이트, exact tableau): U S_i U† ∈ "
          "+S군 전수·U LZ1↔LX1 교환(mod S·부호 정확)=★e↔m 논리 사상·논리2 불변·U²=I(involution). "
          "Tier-2 CLIFFORD 정준 tableau. 정직: 인코더-conjugation 실현(defect 물리 이동/측정 스케줄 "
          "아님·FT braid=범위밖). witness=twist_em_observe.")


def gen_spec():
    U = build_and_verify()
    return ("# " + HEADER + "\n"
            "```python id=bloq\n" + _bloq_code(N, U) + "\n```\n"
            '```json id=meta\n'
            f'{{"id": "twist_em_h16", "n_sys": {N}, "n_anc": 0, "tier": "clifford"}}\n'
            "```\n"), len(U)


def main():
    name = "twist_em_h16"
    spec, ngates = gen_spec()
    sp = os.path.join(SPECS_MODS, f"{name}.pg")
    open(sp, "w", encoding="utf-8", newline="\n").write(spec)
    rc = subprocess.run([sys.executable, os.path.join(ORACLE, "verify_seal.py"), sp,
                        "--out", MODREG], capture_output=True, text=True, cwd=ORACLE).returncode
    seal_path = os.path.join(MODREG, f"{name}.sealed.json")
    if rc != 0 or not os.path.exists(seal_path):
        print(f"[Seal-T2] {name} FAILED rc={rc}")
        return 1
    sealed = json.load(open(seal_path, encoding="utf-8"))
    bloq = vs.instantiate(open(sp, encoding="utf-8").read()
                          .split("id=bloq\n")[1].split("```")[0], "bloq")
    indep_hash, nq = cs.canonical_tableau_hash(bloq)
    match = indep_hash == sealed["u_hash"]
    print(f"[Seal-T2] {name} n_sys={sealed['n_sys']} tier={sealed['tier']} gates={ngates} "
          f"u_hash={sealed['u_hash'][:14]}.. tableau_recompute_match={match}")
    return 0 if match else 1


if __name__ == "__main__":
    sys.exit(main())
