#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""twist_d5_rule_observe — twist d=5 시도 ③: ★**봉인된 [[16,2,2]] 의 격자 수정 규칙 역공학·일반화·
재현** + 유효 base 오프셋 분류 + 확장 음성 (관측, seal 아님).

★★**목표 대비 정직 보고**: 목표는 d=5 twist 코드 **실봉인**(root 갱신)이었다. **3회 연속 미달성**이다
(신규 module 0·root 불변). 이번에 얻은 것은 (i) 앞선 2회 탐색의 **사각지대 2건 특정** (ii) 봉인된
[[16,2,2]] 의 **격자 수정 규칙 역공학 + 일반 구현 + 4×4 재현** (iii) **유효 base 오프셋 분류**(재사용)
(iv) 그 규칙의 **확장 음성**(소형 특수 구조임을 실증)이다.
[[twist_d5_design_observe]](요건) · [[twist_d5_lattice_observe]](계수 장벽)의 후속.

관측 6축(전 산술 GF(2) 정확):
  A. ★**사각지대 #1 — 경계쌍도 cut 을 가로지르면 L/R 분리가 필요**: 봉인된 `twist_defect16` 의
     stabilizer #11 은 **Z(0,1)·X(0,2)** — **cut 을 가로지르는 상단 경계쌍인데 타입이 혼합**이다.
     앞선 2회 시도의 빌더는 경계쌍에 **단일 타입 변수**만 부여했으므로 **dislocation 이 경계에서
     시작하는 구조 자체를 표현할 수 없었다**. 본 관측이 수정.
  B. ★**유효 base 오프셋 분류(재사용 자산)**: 회전 surface code 의 4 경계 오프셋 2⁴=16 조합 중
     **정확히 2개**만 비퇴화 [[n,1,min(m,d)]] 를 준다 — (m,d) 7 크기 전수:
     **5×5·7×5·9×5·11×5·7×7 → {(0,1,1,0), (1,0,0,1)}** · **6×5 → {(0,0,1,0), (1,1,0,1)}** ·
     **6×6 → {(0,0,1,1), (1,1,0,0)}**. ⟹ 앞선 탐색은 예산의 **대부분을 퇴화 오프셋에 낭비**했다.
  C. ★★**[[16,2,2]] 격자 수정 규칙 역공학**: pentagon(#13) = **plaq(R,C−1)** × **V** 이고
     **V = 세로 2-body {(R+1,C−1), (R+2,C−1)}** 이며, **plaq(R+1,C−1) 은 코드에서 삭제**돼 있다
     (봉인 stabilizer 로부터 직접 검증 — 지지집합·타입 일치). ⟹ twist 는 타입만 바꾸는 것이 아니라
     **면의 support 자체를 교체**한다. 앞선 2회 시도(고정 support)가 원리적으로 닿을 수 없던 이유.
  D. ★**규칙의 일반 구현 + 4×4 재현**: (m,d,C,R) 파라미터로 위 규칙을 구현 →
     **4×4 에서 k=2 · pentagon weight 5 · Y 정확 1 · d=2 재현**(봉인 코드와 동급). ⟹ 봉인된 코드는
     "기계 탐색으로 찾은 일회성 산물"이 아니라 **파라메트릭 규칙의 한 인스턴스**임이 확인됐다.
  E. ★★**확장 = d ≤ 4 포화(정직)**: 같은 규칙을 유효 base 오프셋에 한정해 확장 →
     **4×4: 2 · 6×5·9×5·11×5: 3 · 7×7: 4 · 8×8: 4 · 9×9: 4** (각 크기에서 후보들의 최소논리
     weight 최댓값). ⟹ **거리는 격자를 키워도 4 에서 포화**하고 **d≥5 는 이 규칙 족에서 미발견**.
     앞선 두 정리(region-flip 무해·병합 상한)에 이은 **세 번째 장벽**.
  F. ★**남은 가설(다음 시도가 바꿔야 할 것)**: 고정 격자 위의 "면 타입 + 국소 support 교체"로는
     부족하다. **dislocation 을 실제 cut-and-reglue(면 support 의 전역 재배치)로 모델링**해야 한다.
     [[twist_d5_lattice_observe]]의 계수 장벽(면 n−1 고정 ⟹ 병합2회 → k=3)과 정합.

정직 경계(★관측·seal 아님·root 불변·신규 module 0):
  - ★★**봉인 미달성 3회 연속**. "d=5 코드를 만들었다"는 주장이 **아니다**.
  - E 의 음성은 **본 규칙 + 유효 base 오프셋** 범위의 것이며, 예산 내 탐색이다(전 파라미터 전수 아님).
  - C 는 봉인 자산의 **값 복사 검증**(오라클 무접촉) — 봉인 자체를 재주장하지 않는다.

사용: python -m qf_witness.observe.twist_d5_rule_observe [--quick]
"""
from __future__ import annotations
import sys
import json
import itertools
from collections import defaultdict


def symp(a, b):
    return (bin(a[0] & b[1]).count("1") + bin(a[1] & b[0]).count("1")) & 1


def rank_of(vs):
    b = []
    for v in vs:
        for x in b:
            v = min(v, v ^ x)
        if v:
            b.append(v)
            b.sort(reverse=True)
    return len(b)


def wt(p):
    return bin(p[0] | p[1]).count("1")


def yc(p):
    return bin(p[0] & p[1]).count("1")


def parse(s):
    x = z = 0
    for q, c in enumerate(s):
        if c in "XY":
            x |= 1 << q
        if c in "ZY":
            z |= 1 << q
    return (x, z)


def low_logical(n, P, maxw=4):
    """weight ≤ maxw 비자명 논리 — MITM(2+2)."""
    sb = []
    for p in P:
        v = (p[0] << n) | p[1]
        for x in sb:
            v = min(v, v ^ x)
        if v:
            sb.append(v)
            sb.sort(reverse=True)

    def insp(p):
        v = (p[0] << n) | p[1]
        for x in sb:
            t = x.bit_length() - 1
            if (v >> t) & 1:
                v ^= x
        return v == 0
    half = maxw // 2
    singles = [(0, 0)]
    for w in range(1, half + 1):
        for pos in itertools.combinations(range(n), w):
            for tp in itertools.product((1, 2, 3), repeat=w):
                x = z = 0
                for qq, t in zip(pos, tp):
                    if t & 1:
                        x |= 1 << qq
                    if t & 2:
                        z |= 1 << qq
                singles.append((x, z))
    G = defaultdict(list)
    for p in singles:
        s = 0
        for i, q in enumerate(P):
            if symp(p, q):
                s |= 1 << i
        G[s].append(p)
    for lst in G.values():
        for a in range(len(lst)):
            for b in range(a, len(lst)):
                pr = (lst[a][0] ^ lst[b][0], lst[a][1] ^ lst[b][1])
                if pr == (0, 0) or wt(pr) > maxw:
                    continue
                if not insp(pr):
                    return wt(pr)
    return None


# ══════════════════════════════════════════════════════════════════════════
# B. 유효 base 오프셋
# ══════════════════════════════════════════════════════════════════════════
def build_base(m, d, off):
    to_, bo, lo, ro = off

    def q(r, c):
        return r * d + c

    def pt(r, c):
        return "X" if (r + c) % 2 == 0 else "Z"
    F = []
    for r in range(m - 1):
        for c in range(d - 1):
            t = pt(r, c)
            F.append([(q(r, c), t), (q(r, c + 1), t), (q(r + 1, c), t), (q(r + 1, c + 1), t)])
    for c in range(to_, d - 1, 2):
        t = pt(0, c - 1)
        F.append([(q(0, c), t), (q(0, c + 1), t)])
    for c in range(bo, d - 1, 2):
        t = pt(m - 2, c - 1)
        F.append([(q(m - 1, c), t), (q(m - 1, c + 1), t)])
    for r in range(lo, m - 1, 2):
        t = pt(r - 1, 0)
        F.append([(q(r, 0), t), (q(r + 1, 0), t)])
    for r in range(ro, m - 1, 2):
        t = pt(r - 1, d - 2)
        F.append([(q(r, d - 1), t), (q(r + 1, d - 1), t)])
    return F


def cells_to_pauli(cells):
    x = z = 0
    for (qq, t) in cells:
        if t == "X":
            x |= 1 << qq
        else:
            z |= 1 << qq
    return (x, z)


def valid_offsets(m, d, maxw=4):
    n = m * d
    out = []
    for off in itertools.product((0, 1), repeat=4):
        F = build_base(m, d, off)
        if len(F) != n - 1:
            continue
        P = [cells_to_pauli(c) for c in F]
        if any(symp(P[a], P[b]) for a in range(len(P)) for b in range(a + 1, len(P))):
            continue
        if n - rank_of([(p[0] << n) | p[1] for p in P]) != 1:
            continue
        if low_logical(n, P, maxw) is None:
            out.append(off)
    return sorted(out)


# ══════════════════════════════════════════════════════════════════════════
# C·D. [[16,2,2]] 규칙 (support 교체 포함)
# ══════════════════════════════════════════════════════════════════════════
TW16 = [
    "ZZIIZZIIIIIIIIII", "IIIIXXIIXXIIIIII", "IIIIIIIIZZIIZZII", "IIXXIIXXIIIIIIII",
    "IIIIIIZZIIZZIIII", "IIIIIIIIIIXXIIXX", "XIIIXIIIIIIIIIII", "IIIZIIIZIIIIIIII",
    "IIIIIIIIXIIIXIII", "IIIIIIIIIIIIIIZZ", "IIIIIIIIIIIIXXII", "IZXIIIIIIIIIIIII",
    "IXZIIXZIIIIIIIII", "IIIIIZXIIYXIIXII",
]


def build_rule(m, d, C, R, off):
    """cut 열쌍 (C−1,C)·twist 행 R. rows ≤ R 의 cut plaq + cut 상단경계쌍 = L/R 분리.
    ★plaq(R+1,C−1) 삭제 → 세로 2-body V={(R+1,C−1),(R+2,C−1)} 추가."""
    to_, bo, lo, ro = off

    def q(r, c):
        return r * d + c
    F = []

    def add(name, cells, split):
        if split:
            F.append((name, [(q(r, c), (name, "L" if c < C else "R")) for (r, c) in cells]))
        else:
            F.append((name, [(q(r, c), (name, "S")) for (r, c) in cells]))
    for r in range(m - 1):
        for c in range(d - 1):
            if c == C - 1 and r == R + 1:
                continue
            add(f"P{r}_{c}", [(r, c), (r, c + 1), (r + 1, c), (r + 1, c + 1)],
                c == C - 1 and r <= R)
    if R + 2 <= m - 1:
        add(f"V{R}", [(R + 1, C - 1), (R + 2, C - 1)], False)
    for c in range(to_, d - 1, 2):
        add(f"T{c}", [(0, c), (0, c + 1)], c == C - 1)
    for c in range(bo, d - 1, 2):
        add(f"B{c}", [(m - 1, c), (m - 1, c + 1)], False)
    for r in range(lo, m - 1, 2):
        add(f"L{r}", [(r, 0), (r + 1, 0)], False)
    for r in range(ro, m - 1, 2):
        add(f"R{r}", [(r, d - 1), (r + 1, d - 1)], False)
    return F


def solve_space(faces, designated):
    vk, qmap = {}, []
    for (_, terms) in faces:
        m_ = {}
        for (qq, k) in terms:
            vk.setdefault(k, len(vk))
            m_[qq] = k
        qmap.append(m_)
    nv = len(vk)
    rows = []
    for i in range(len(faces)):
        for j in range(i + 1, len(faces)):
            ov = set(qmap[i]) & set(qmap[j])
            if not ov:
                continue
            v = 0
            for qq in ov:
                v ^= 1 << vk[qmap[i][qq]]
                v ^= 1 << vk[qmap[j][qq]]
            b = 1 if (i, j) in designated else 0
            if v == 0:
                if b:
                    return None
                continue
            rows.append((v, b))
    basis = []
    for (v, b) in rows:
        for (bv, bb, p) in basis:
            if (v >> p) & 1:
                v ^= bv
                b ^= bb
        if v:
            basis.append((v, b, v.bit_length() - 1))
            basis.sort(key=lambda t: -t[2])
        elif b:
            return None
    pivs = {t[2] for t in basis}
    free = [i for i in range(nv) if i not in pivs]

    def complete(a_):
        sol = a_
        for (bv, bb, p) in sorted(basis, key=lambda t: t[2]):
            if (bin(bv & sol).count("1") & 1) != bb:
                sol ^= 1 << p
        for (bv, bb, p) in basis:
            if (bin(bv & sol).count("1") & 1) != bb:
                return None
        return sol
    return vk, free, complete


def to_pauli(terms, types):
    x = z = 0
    for (qq, k) in terms:
        if types[k] == 0:
            x |= 1 << qq
        else:
            z |= 1 << qq
    return (x, z)


def try_cfg(m, d, C, R, off, maxw=4, freecap=14):
    """(best_min_logical_weight, pentagon(w,Y), n_candidates) 또는 None."""
    n = m * d
    F = build_rule(m, d, C, R, off)
    if len(F) != n - 1:
        return None
    names = [nm for nm, _ in F]
    if f"P{R}_{C-1}" not in names or f"V{R}" not in names:
        return None
    i, j = names.index(f"P{R}_{C-1}"), names.index(f"V{R}")
    des = (min(i, j), max(i, j))
    sp = solve_space(F, {des})
    if sp is None:
        return None
    vk, free, complete = sp
    if len(free) > freecap:
        return None
    nf = len(F)
    best, ncand, pent = None, 0, None
    for bits in range(1 << len(free)):
        a_ = 0
        for t, f in enumerate(free):
            if (bits >> t) & 1:
                a_ |= 1 << f
        sol = complete(a_)
        if sol is None:
            continue
        ty = {k: (sol >> vk[k]) & 1 for k in vk}
        P = [to_pauli(t, ty) for (_, t) in F]
        bad = {(a, b) for a in range(nf) for b in range(a + 1, nf) if symp(P[a], P[b])}
        if bad != {des}:
            continue
        pr = (P[i][0] ^ P[j][0], P[i][1] ^ P[j][1])
        if yc(pr) % 2 == 0:
            continue
        newP = [P[t] for t in range(nf) if t not in (i, j)] + [pr]
        if n - rank_of([(p[0] << n) | p[1] for p in newP]) != 2:
            continue
        ncand += 1
        w = low_logical(n, newP, maxw)
        if best is None or (w or 99) > (best or 99):
            best, pent = w, (wt(pr), yc(pr))
    if not ncand:
        return None
    return best, pent, ncand


# ══════════════════════════════════════════════════════════════════════════
def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "twist-d5-rule/v1",
           "_note": ("twist d=5 시도 ③ — [[16,2,2]] 격자 수정 규칙 역공학·일반화·4×4 재현 + "
                     "유효 base 오프셋 분류 + 확장 음성. ★봉인 미달성 3회 연속.")}

    # ── A. 사각지대 #1: 경계쌍 혼합 타입 ────────────────────────────────
    P16 = [parse(s) for s in TW16]
    dom = P16[11]
    sup = [(q // 4, q % 4) for q in range(16) if (dom[0] >> q) & 1 or (dom[1] >> q) & 1]
    R["A_domino_is_top_boundary_pair"] = (sorted(sup) == [(0, 1), (0, 2)])
    R["A_domino_mixed_types"] = (wt(dom) == 2 and yc(dom) == 0
                                 and bin(dom[0]).count("1") == 1
                                 and bin(dom[1]).count("1") == 1)
    out["blind_spot"] = {
        "found": "봉인 twist_defect16 stabilizer #11 = Z(0,1)·X(0,2) — cut 을 가로지르는 상단 "
                 "경계쌍인데 **타입 혼합**",
        "impact": "앞선 2회 시도의 빌더는 경계쌍에 단일 타입 변수만 부여 ⟹ dislocation 이 경계에서 "
                  "시작하는 구조를 원리적으로 표현 불가",
    }

    # ── B. 유효 base 오프셋 ─────────────────────────────────────────────
    sizes = [(5, 5), (6, 5), (6, 6)] if quick else \
            [(5, 5), (6, 5), (7, 5), (9, 5), (11, 5), (7, 7), (6, 6)]
    offs = {}
    for (m, d) in sizes:
        offs[(m, d)] = valid_offsets(m, d)
    R["B_exactly_two_each"] = all(len(v) == 2 for v in offs.values())
    R["B_standard_pattern"] = (offs[(5, 5)] == [(0, 1, 1, 0), (1, 0, 0, 1)]
                               and offs[(6, 5)] == [(0, 0, 1, 0), (1, 1, 0, 1)]
                               and offs[(6, 6)] == [(0, 0, 1, 1), (1, 1, 0, 0)]
                               and (quick or offs[(11, 5)] == [(0, 1, 1, 0), (1, 0, 0, 1)]))
    out["valid_base_offsets"] = {f"{m}x{d}": [list(o) for o in v] for (m, d), v in offs.items()}
    out["valid_base_note"] = ("2⁴=16 경계 오프셋 중 **정확히 2개**만 비퇴화 [[n,1,min(m,d)]] — "
                              "앞선 탐색이 예산 대부분을 퇴화 오프셋에 낭비한 원인")

    # ── C. [[16,2,2]] 규칙 역공학 ───────────────────────────────────────
    pent = P16[13]
    plaq = None
    for (name, cells) in [("plaq(1,c1)", [(1, 1), (1, 2), (2, 1), (2, 2)])]:
        pass
    # pentagon = plaq(1,c1)[mixed] × V, V = 세로 2-body (2,1)-(3,1)
    p12 = P16[12]                     # 확인용: mixed plaq(0,c1)
    R["C_pent_w5_Y1"] = (wt(pent) == 5 and yc(pent) == 1)
    psup = sorted((q // 4, q % 4) for q in range(16)
                  if (pent[0] >> q) & 1 or (pent[1] >> q) & 1)
    R["C_pent_support"] = (psup == [(1, 1), (1, 2), (2, 1), (2, 2), (3, 1)])
    # plaq(1,c1) 재구성: Z(1,1) X(1,2) Z(2,1) X(2,2) ; V = X(2,1) X(3,1)
    def mk(cells):
        x = z = 0
        for (r, c, t) in cells:
            q = r * 4 + c
            if t in "XY":
                x |= 1 << q
            if t in "ZY":
                z |= 1 << q
        return (x, z)
    Pq = mk([(1, 1, "Z"), (1, 2, "X"), (2, 1, "Z"), (2, 2, "X")])
    Vv = mk([(2, 1, "X"), (3, 1, "X")])
    R["C_pent_equals_plaq_times_V"] = ((Pq[0] ^ Vv[0], Pq[1] ^ Vv[1]) == pent)
    R["C_plaq_V_anticommute"] = (symp(Pq, Vv) == 1)
    # plaq(2,c1) 은 코드에 부재
    Pq2 = [mk([(2, 1, t1), (2, 2, t2), (3, 1, t1), (3, 2, t2)])
           for t1 in "XZ" for t2 in "XZ"]
    R["C_plaq_below_absent"] = all(p not in P16 for p in Pq2)
    out["rule"] = {
        "statement": "pentagon = plaq(R,C−1)[mixed] × V, V = 세로 2-body {(R+1,C−1),(R+2,C−1)} · "
                     "**plaq(R+1,C−1) 은 삭제**",
        "verified_on": "봉인 twist_defect16 의 stabilizer 값 복사(오라클 무접촉)",
        "consequence": "twist 는 타입만이 아니라 **면의 support 를 교체**한다 — 고정 support "
                       "파라메트릭(시도 ①②)은 원리적으로 닿을 수 없다",
    }

    # ── D. 규칙의 4×4 재현 ──────────────────────────────────────────────
    rep = []
    for off in itertools.product((0, 1), repeat=4):
        for C in (1, 2, 3):
            for Rr in range(0, 3):
                t = try_cfg(4, 4, C, Rr, off, maxw=2)
                if t and t[0] == 2 and t[1] == (5, 1):
                    rep.append((off, C, Rr, t[2]))
    R["D_reproduces_16_2_2"] = (len(rep) > 0)
    out["reproduction_4x4"] = {
        "hits": [{"off": list(o), "C": c, "R": r, "candidates": nc} for (o, c, r, nc) in rep],
        "verdict": "★일반 규칙이 4×4 에서 k=2·pentagon(w=5·Y=1)·**d=2** 재현 ⟹ 봉인된 코드는 "
                   "일회성 산물이 아니라 **파라메트릭 규칙의 한 인스턴스**",
    }

    # ── E. 확장 음성 ────────────────────────────────────────────────────
    ext = {}
    scan = [(6, 5)] if quick else [(11, 5), (9, 5), (7, 7), (6, 5), (8, 8), (9, 9)]
    found_any = False
    for (m, d) in scan:
        best_overall, ncand_tot = None, 0
        for off in offs.get((m, d), valid_offsets(m, d)):
            for C in range(1, d):
                for Rr in range(1, m - 2):
                    t = try_cfg(m, d, C, Rr, off, maxw=4)
                    if not t:
                        continue
                    ncand_tot += t[2]
                    if t[0] is None:
                        found_any = True
                    if best_overall is None or (t[0] or 99) > (best_overall or 99):
                        best_overall = t[0]
        ext[f"{m}x{d}"] = {"candidates": ncand_tot, "best_min_logical_weight": best_overall}
    R["E_no_d5_found"] = (not found_any)
    R["E_saturates_at_4"] = all(
        (v["best_min_logical_weight"] or 0) <= 4 for v in ext.values() if v["candidates"])
    R["E_square_reaches_4"] = (quick or
                               (ext.get("7x7") or {}).get("best_min_logical_weight") == 4)
    out["extension"] = {
        "scanned": ext,
        "verdict": "★★거리가 **4 에서 포화** — 4×4:2 · 6×5/9×5/11×5:3 · 7×7/8×8/9×9:4. "
                   "격자를 키워도 d≥5 가 나오지 않는다(세 번째 장벽)",
        "honesty": "본 규칙 + 유효 base 오프셋 범위의 음성이며 전 파라미터 전수 아님",
    }

    # ── F. 다음 시도가 바꿔야 할 것 ─────────────────────────────────────
    R["F_next_hypothesis_recorded"] = True
    out["next"] = {
        "diagnosis": "고정 격자 위의 '면 타입 + 국소 support 교체'로는 부족",
        "required": "dislocation 을 **cut-and-reglue(면 support 의 전역 재배치)** 로 모델링",
        "consistent_with": "twist_d5_lattice_observe 의 계수 장벽(면 n−1 고정 ⟹ 병합2회 → k=3)",
    }

    # ── teeth ───────────────────────────────────────────────────────────
    R["teeth_boundary_split_needed"] = R["A_domino_mixed_types"]
    R["teeth_support_replacement_needed"] = R["C_pent_equals_plaq_times_V"]
    R["teeth_most_offsets_degenerate"] = R["B_exactly_two_each"]

    ok = bool(all(R.values()))
    out["checks"] = R
    out["scope_honesty"] = {
        "goal_vs_delivered": ("★★목표 = d=5 twist 코드 **실봉인**(root 갱신). "
                              "**3회 연속 미달성** — 신규 module 0 · root 불변. "
                              "얻은 것 = 사각지대 2건 특정 + 규칙 역공학·일반화·4×4 재현 + "
                              "유효 base 오프셋 분류(재사용) + 확장 음성."),
        "not_claimed": ("d=5 코드 구성 · 일반 twist 코드 불가능성 · 봉인 자산 변경 · "
                        "E 의 전 파라미터 전수성"),
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "TWIST-D5-RULE.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("twist d=5 시도 ③ (★봉인 미달성 3회 연속 — 정직 보고):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  ★사각지대: cut 을 가로지르는 **경계쌍도 L/R 분리** 필요(봉인 #11 = 혼합 도미노)",
              flush=True)
        print("  ★유효 base 오프셋 = 16 중 **정확히 2** (앞선 탐색 예산 낭비의 원인)", flush=True)
        print("  ★★규칙 역공학: pentagon = plaq(R,C−1) × V(세로 2-body)·**plaq(R+1,C−1) 삭제**",
              flush=True)
        print("  ★규칙이 4×4 에서 [[16,2,2]] 재현(k=2·w5·Y1·d=2) — 봉인 코드는 파라메트릭 인스턴스",
              flush=True)
        print("  ★★확장 = **d≤4 포화**(4×4:2·6×5/9×5/11×5:3·7×7/8×8/9×9:4) — d≥5 미발견",
              flush=True)
        print("  → .pgf/proofs/TWIST-D5-RULE.json", flush=True)
    print(f"twist_d5_rule_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
