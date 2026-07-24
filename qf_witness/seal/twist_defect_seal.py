#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""twist_defect_seal.py — TrackHE18 잔여(report18 agent03): twist-defect(dislocation) surface code
[[16,2,2]] |0_L 0_L⟩ prep **Tier-2 CLIFFORD 봉인**.

★첫 non-CSS twist 코드 봉인: 4×4 회전 surface code 격자에 dislocation line(열1|2 사이, 상단 경계→
행1/2 경계)을 삽입한 자체 설계 코드(기계 탐색 + 전수 검증으로 확정):
  - bulk 6면(체커보드 Z/X, 컷 좌 정상·우 색반전) + 경계 5(weight-2)
  - dislocation line: 도미노 mixed Z₁X₂ → 4-body mixed X₁Z₂X₅Z₆ →
    ★**twist 끝점 pentagon Z₅X₆Y₉X₁₀X₁₃ (5-body·Y 1개)** — 문헌 표준 twist stabilizer 형태
  - [[16,2,2]] non-CSS: twist 가 논리큐빗 +1(기준 4×4 회전 [[16,1,?]] k=1 대비 k=2)
  - e↔m: 논리 15 클래스 중 9 가 mixed-필수(순수 X/Z 대표 부재) — twist 를 지나는 string 이 X↔Z 전환
|0_L 0_L⟩ 인코더: 표준형 환원 합성(H/S/CX/CZ) + Aaronson-Gottesman rowsum 부호검증 + Pauli 보정 —
  |0⟩¹⁶ → 안정군 = ⟨S₁..S₁₄, LZ1, LZ2⟩ 전부 +부호 (cirq statevector 교차검증 완료, 스크래치).
봉인: verify_seal tier="clifford" 정준 tableau → registry/modules. 독립 재확인 = canonical_tableau_hash.
정직 경계: 봉인=|0_L0_L⟩ prep Clifford 회로 tableau exact · d=2(detection-only, twist-경계 근접 소형 —
  d≥3 은 대형 격자) · twist-braid 논리 게이트/측정 스케줄=범위밖. witness=twist_defect_observe(오라클 독립).

사용: python -m qf_witness.seal.twist_defect_seal
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

SPECS_MODS = os.path.join(ROOT, "specs", "modules")
MODREG = os.path.join(ROOT, "registry", "modules")

N = 16
# 설계 확정 상수(기계 탐색 + 전수 검증 산출물 — 결정론)
STABS_STR = [
    "ZZIIZZIIIIIIIIII",
    "IIIIXXIIXXIIIIII",
    "IIIIIIIIZZIIZZII",
    "IIXXIIXXIIIIIIII",
    "IIIIIIZZIIZZIIII",
    "IIIIIIIIIIXXIIXX",
    "XIIIXIIIIIIIIIII",
    "IIIZIIIZIIIIIIII",
    "IIIIIIIIXIIIXIII",
    "IIIIIIIIIIIIIIZZ",
    "IIIIIIIIIIIIXXII",
    "IZXIIIIIIIIIIIII",
    "IXZIIXZIIIIIIIII",
    "IIIIIZXIIYXIIXII",      # ★pentagon: 5-body, Y 1개 (twist endpoint)
]
LZ1_STR = "IXZIIXIZIXIIIXII"
LZ2_STR = "IXZIIXIZIIZIIIIZ"


def parse(s):
    x = z = 0
    for q, c in enumerate(s):
        if c in "XY":
            x |= (1 << q)
        if c in "ZY":
            z |= (1 << q)
    return (x, z)


def symp(a, b):
    return (bin(a[0] & b[1]).count("1") + bin(a[1] & b[0]).count("1")) & 1


def weight(p):
    return bin(p[0] | p[1]).count("1")


def ycount(p):
    return bin(p[0] & p[1]).count("1")


def gf2_rank(vs_):
    b = []
    for v in vs_:
        for x in b:
            v = min(v, v ^ x)
        if v:
            b.append(v)
            b.sort(reverse=True)
    return len(b)


def precheck():
    S = [parse(s) for s in STABS_STR]
    LZ1, LZ2 = parse(LZ1_STR), parse(LZ2_STR)
    assert all(symp(a, b) == 0 for a in S for b in S), "stab 교환 실패"
    assert gf2_rank([(p[0] << N) | p[1] for p in S]) == N - 2, "k≠2"
    pent = S[13]
    assert weight(pent) == 5 and ycount(pent) == 1, "pentagon 아님"
    for L in (LZ1, LZ2):
        assert all(symp(L, s) == 0 for s in S), "논리 Z 비교환"
    assert symp(LZ1, LZ2) == 0
    # weight-1 논리 부재(d≥2 필요조건)
    sb = []
    for p in S:
        v = (p[0] << N) | p[1]
        for b in sb:
            v = min(v, v ^ b)
        if v:
            sb.append(v)
            sb.sort(reverse=True)
    for q in range(N):
        for xs, zs in (([q], []), ([q], [q]), ([], [q])):
            p = (sum(1 << i for i in xs), sum(1 << i for i in zs))
            if all(symp(p, s) == 0 for s in S):
                v = (p[0] << N) | p[1]
                for b in sb:
                    v = min(v, v ^ b)
                assert v == 0, f"weight-1 논리 존재 q={q}"
    return S, LZ1, LZ2


def synthesize(S, LZ1, LZ2):
    """표준형 환원 합성 + rowsum 부호검증/보정 → 인코더 게이트 리스트 (결정론)."""
    targets = [tuple(p) for p in S] + [LZ1, LZ2]
    rows = [[p[0], p[1]] for p in targets]
    gates = []

    def apply_H(q):
        for r in rows:
            xb = (r[0] >> q) & 1
            zb = (r[1] >> q) & 1
            if xb != zb:
                r[0] ^= (1 << q)
                r[1] ^= (1 << q)
        gates.append(("h", q))

    def apply_S(q):
        for r in rows:
            if (r[0] >> q) & 1:
                r[1] ^= (1 << q)
        gates.append(("s", q))

    def apply_CX(c, t):
        for r in rows:
            if (r[0] >> c) & 1:
                r[0] ^= (1 << t)
            if (r[1] >> t) & 1:
                r[1] ^= (1 << c)
        gates.append(("cx", c, t))

    def apply_CZ(a, b):
        for r in rows:
            if (r[0] >> a) & 1:
                r[1] ^= (1 << b)
            if (r[0] >> b) & 1:
                r[1] ^= (1 << a)
        gates.append(("cz", a, b))

    for i in range(N):
        pr = next((r_ for r_ in range(i, N) if (rows[r_][0] >> i) & 1), None)
        if pr is None:
            pr = next(r_ for r_ in range(i, N) if (rows[r_][1] >> i) & 1)
            apply_H(i)
        rows[i], rows[pr] = rows[pr], rows[i]
        for j in range(N):
            if j != i and (rows[i][0] >> j) & 1:
                apply_CX(i, j)
        if (rows[i][1] >> i) & 1:
            apply_S(i)
        for j in range(N):
            if j != i and (rows[i][1] >> j) & 1:
                apply_CZ(i, j)
        assert rows[i][0] == (1 << i) and rows[i][1] == 0
        for r_ in range(N):
            if r_ != i and (rows[r_][0] >> i) & 1:
                rows[r_][0] ^= rows[i][0]
                rows[r_][1] ^= rows[i][1]
    assert all(rows[i][0] == (1 << i) and rows[i][1] == 0 for i in range(N))
    for q in range(N):
        apply_H(q)
    # 인코더 = 역순(자기역 h/cx/cz; s → s³)
    enc = []
    for g in reversed(gates):
        enc += [g, g, g] if g[0] == "s" else [g]

    # 부호검증(rowsum) + Pauli 보정
    def sim(gs):
        rows_ = [[0, 1 << q, 0] for q in range(N)]

        def h(q):
            for r in rows_:
                xb = (r[0] >> q) & 1
                zb = (r[1] >> q) & 1
                r[2] ^= xb & zb
                if xb != zb:
                    r[0] ^= (1 << q)
                    r[1] ^= (1 << q)

        def sg(q):
            for r in rows_:
                if (r[0] >> q) & 1:
                    r[2] ^= (r[1] >> q) & 1
                    r[1] ^= (1 << q)

        def cx(c, t):
            for r in rows_:
                xc = (r[0] >> c) & 1
                zt = (r[1] >> t) & 1
                xt = (r[0] >> t) & 1
                zc = (r[1] >> c) & 1
                r[2] ^= xc & zt & (xt ^ zc ^ 1)
                if xc:
                    r[0] ^= (1 << t)
                if zt:
                    r[1] ^= (1 << c)
        for g in gs:
            if g[0] == "h":
                h(g[1])
            elif g[0] == "s":
                sg(g[1])
            elif g[0] == "cx":
                cx(g[1], g[2])
            elif g[0] == "cz":
                h(g[2]); cx(g[1], g[2]); h(g[2])
            elif g[0] == "x":
                for r in rows_:
                    r[2] ^= (r[1] >> g[1]) & 1
            elif g[0] == "z":
                for r in rows_:
                    r[2] ^= (r[0] >> g[1]) & 1
        return rows_

    def g_phase(x1, z1, x2, z2):
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

    def member_sign(final, t):
        basis = []
        for i, r in enumerate(final):
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
        assert v == 0, "목표가 안정군 밖"
        acc = [0, 0, 0]
        for i in range(N):
            if (c >> i) & 1:
                ph = (2 * acc[2] + 2 * final[i][2]
                      + g_phase(acc[0], acc[1], final[i][0], final[i][1])) % 4
                assert ph % 2 == 0
                acc = [acc[0] ^ final[i][0], acc[1] ^ final[i][1], (ph // 2) % 2]
        return acc[2]

    final = sim(enc)
    signs = [member_sign(final, t) for t in targets]
    neg = [i for i, s in enumerate(signs) if s == 1]
    if neg:
        # 보정 Pauli: symp(P,T_i)=neg_i 선형계
        basis = []
        for i, t in enumerate(targets):
            m = (t[1] << N) | t[0]
            bb = 1 if i in neg else 0
            v = m
            for (bv, bbit, piv) in basis:
                if (v >> piv) & 1:
                    v ^= bv
                    bb ^= bbit
            if v:
                basis.append((v, bb, v.bit_length() - 1))
            else:
                assert bb == 0, "부호 보정 불능"
        sol = 0
        for (bv, bbit, piv) in sorted(basis, key=lambda t3: t3[2]):
            if (bin(bv & sol).count("1") & 1) != bbit:
                sol ^= (1 << piv)
        Px, Pz = sol >> N, sol & ((1 << N) - 1)
        for q in range(N):
            if (Px >> q) & 1:
                enc.append(("x", q))
            if (Pz >> q) & 1:
                enc.append(("z", q))
        final = sim(enc)
        signs = [member_sign(final, t) for t in targets]
    assert all(s == 0 for s in signs), "부호 +1 실패"
    return enc


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


HEADER = ("twist_defect16 — twist-defect(dislocation) surface code [[16,2,2]] |0_L 0_L⟩ prep. "
          "★첫 non-CSS twist 코드: 4×4 회전격자 + dislocation line(도미노 mixed → 4-body mixed → "
          "★5-body pentagon Z5X6Y9X10X13, Y 1개=twist endpoint), twist 가 논리 +1(k=2), e↔m(논리 15클래스 중 "
          "9 mixed-필수). 자체 설계(기계 탐색+전수 검증). 인코더=표준형 환원 합성(H/S/CX/CZ)+rowsum 부호보정, "
          "안정군=⟨S1..14,LZ1,LZ2⟩ 전부 +부호(cirq statevector 교차검증). Tier-2 CLIFFORD 정준 tableau. "
          "정직: d=2(detection-only 소형)·twist-braid 게이트=범위밖. witness=twist_defect_observe.")


def gen_spec():
    S, LZ1, LZ2 = precheck()
    enc = synthesize(S, LZ1, LZ2)
    return ("# " + HEADER + "\n"
            "```python id=bloq\n" + _bloq_code(N, enc) + "\n```\n"
            '```json id=meta\n'
            f'{{"id": "twist_defect16", "n_sys": {N}, "n_anc": 0, "tier": "clifford"}}\n'
            "```\n"), len(enc)


def main():
    name = "twist_defect16"
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
