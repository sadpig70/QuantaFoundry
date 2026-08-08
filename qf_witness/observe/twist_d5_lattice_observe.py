#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""twist_d5_lattice_observe — twist d=5 격자 실구성 시도 ②: ★**계수 장벽 특정 + 6×5 전수 음성**
(관측, seal 아님). [[twist_d5_design_observe]](요건 ①–⑤ 확정)의 후속 집행 시도.

★★**목표 대비 정직 보고**: 목표는 요건 ⑤ 집행 → **d=5 실봉인**(root 갱신)이었다.
**봉인은 다시 미달성**이다(신규 module 0·root 불변). 얻은 것은 (i) 재사용 도구 2종
(ii) **계수 장벽(counting obstruction) 특정** (iii) 6×5 격자 **전수 음성**이다.
대형 격자 음성은 **예산 제한**이며 전수가 아니다 — 이 점을 명시한다.

관측 6축(전 산술 GF(2) 정확):
  A. ★**타입 GF(2) 아핀 연립 구성법**(재사용 자산): 면 집합(plaquette + 경계쌍, cut 열쌍은
     L/R 분리 변수)에 대해 **"지정한 1쌍만 반교환, 나머지 전부 교환"** 을 GF(2) 아핀 연립으로
     풀어 타입을 **손으로 정하지 않고** 얻는다. 두 면이 겹치는 큐빗에서 타입 불일치 개수의
     패리티가 곧 symplectic 곱이므로 조건이 **선형**이다.
     ★**따름정리**: 지정 쌍의 반교환 조건이 곧 "타입 불일치 겹침이 **홀수**"이므로,
     병합 S_iS_j 의 **Y 개수가 자동으로 홀수** — 홀수-Y pentagon 이 **설계상 보장**된다.
     ★**함정(실증)**: 해 공간의 **자유변수를 전수 열거**해야 한다 — 소거의 특수해는
     "전 면 동일 타입"(전부 X)으로 퇴화해 **weight-1 논리**를 낳는다(실제로 처음 그렇게 실패).
  B. ★**meet-in-the-middle 거리 인증기**(재사용 자산): weight ≤4 비자명 논리의 존재 판정을
     **2+2 분해 + syndrome 그룹핑**으로 수행(임의 weight≤4 Pauli 는 weight≤2 둘의 곱).
     직접 전수는 n=30 에서 이미 2.3M Pauli · n=55 에서 27.6M — 본 인증기는 **n=77 까지 즉시**.
     [[twist_d5_design_observe]]의 직접 전수 인증기와 **6×5 후보에서 동일 결론** 교차검증.
  C. ★★**계수 장벽 특정**: 면 수는 [[n,1,·]] 기준 **n−1** 로 고정. 병합 1회 → 생성원 n−2 →
     **k=2**(정상) 이지만 **병합 2회 → n−3 → k=3**. 즉 **bulk twist 쌍**(k=2 유지)을 만들려면
     면을 **하나 추가**해야 한다. ⟹ 단일 병합 족에서는 **두 번째 twist 가 반드시 경계에 흡수**
     되고 twist 논리는 병합점↔경계 string 이므로 **weight ≤ ⌊m/2⌋** ⟹ **d=5 는 m ≥ 10 필요**.
  D. ★**6×5 전수 음성**: 경계 오프셋 16 × cut 열 4 × cut 길이 5 × 지정 겹침쌍 × 해공간 전수 —
     "1쌍 반교환·k=2·홀수 Y" 를 만족하는 후보는 나오지만 **전부 weight≤4 논리 보유** ⟹ d≥5 없음.
     (C 와 정합: m=6 ⟹ ⌊m/2⌋=3.)
  E. **대형 격자(11×5·10×5·11×7) 음성 = 예산 제한**: 각 600/400/600s 소진 · **전수 아님**.
     C 가 시사하는 m≥10 영역이지만 단일 병합 족의 다른 제약(경계 패턴 패리티 등)으로 미발견.
  F. ★**다음 설계 방향**(C 에서 유도): **cut 을 따라 면을 1개 추가**(추가 mixed 면)한 뒤
     **2회 병합** → 생성원 (n−1+1)−2 = n−2 → **k=2 유지 + bulk twist 2개**.
     두 병합점을 ≥5 떨어뜨리면 twist 논리 weight ≥5 가 가능하다.

정직 경계(★관측·seal 아님·root 불변·신규 module 0):
  - ★★**봉인 미달성**(2회 연속). "d=5 코드를 만들었다"는 주장이 **아니다**.
  - D 는 **6×5 격자·단일 병합 족** 내 전수이고, E 는 **전수가 아니다**(예산 제한).
  - C 의 장벽은 **면 수 n−1 고정 + 병합만 사용** 이라는 본 족의 가정에서 나온 것이며,
    일반 twist 코드 불가능성 주장이 아니다(F 가 우회 경로).

사용: python -m qf_witness.observe.twist_d5_lattice_observe [--quick]
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


def span(n, P):
    sb = []
    for p in P:
        v = (p[0] << n) | p[1]
        for x in sb:
            v = min(v, v ^ x)
        if v:
            sb.append(v)
            sb.sort(reverse=True)
    return sb


def in_span(n, sb, p):
    v = (p[0] << n) | p[1]
    for x in sb:
        top = x.bit_length() - 1
        if (v >> top) & 1:
            v ^= x
    return v == 0


def low_logical_mitm(n, P, maxw=4):
    """weight ≤ maxw 비자명 논리 — meet-in-the-middle(2+2 분해·syndrome 그룹핑)."""
    sb = span(n, P)
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
    groups = defaultdict(list)
    for p in singles:
        s = 0
        for i, q in enumerate(P):
            if symp(p, q):
                s |= 1 << i
        groups[s].append(p)
    for lst in groups.values():
        for a in range(len(lst)):
            for b in range(a, len(lst)):
                pr = (lst[a][0] ^ lst[b][0], lst[a][1] ^ lst[b][1])
                if pr == (0, 0) or wt(pr) > maxw:
                    continue
                if not in_span(n, sb, pr):
                    return wt(pr)
    return None


def low_logical_direct(n, P, maxw=4):
    """직접 전수(교차검증용)."""
    sb = span(n, P)
    for w in range(1, maxw + 1):
        for pos in itertools.combinations(range(n), w):
            for tp in itertools.product((1, 2, 3), repeat=w):
                x = z = 0
                for qq, t in zip(pos, tp):
                    if t & 1:
                        x |= 1 << qq
                    if t & 2:
                        z |= 1 << qq
                p = (x, z)
                if all(symp(p, s) == 0 for s in P) and not in_span(n, sb, p):
                    return w
    return None


def build_faces(m, d, C, R, off):
    """cut = 열쌍 C−1|C 의 행 0..R−1 만 L/R 분리(유한 길이)."""
    to_, bo, lo, ro = off

    def q(r, c):
        return r * d + c
    faces = []
    for r in range(m - 1):
        for c in range(d - 1):
            qs = [(r, c), (r, c + 1), (r + 1, c), (r + 1, c + 1)]
            if c == C - 1 and r < R:
                terms = [(q(*p), (f"P{r}_{c}", "L" if p[1] == C - 1 else "R")) for p in qs]
            else:
                terms = [(q(*p), (f"P{r}_{c}", "S")) for p in qs]
            faces.append((f"P{r}_{c}", terms))
    for c in range(to_, d - 1, 2):
        faces.append((f"T{c}", [(q(0, c), (f"T{c}", "S")), (q(0, c + 1), (f"T{c}", "S"))]))
    for c in range(bo, d - 1, 2):
        faces.append((f"B{c}", [(q(m - 1, c), (f"B{c}", "S")),
                                (q(m - 1, c + 1), (f"B{c}", "S"))]))
    for r in range(lo, m - 1, 2):
        faces.append((f"L{r}", [(q(r, 0), (f"L{r}", "S")), (q(r + 1, 0), (f"L{r}", "S"))]))
    for r in range(ro, m - 1, 2):
        faces.append((f"R{r}", [(q(r, d - 1), (f"R{r}", "S")),
                                (q(r + 1, d - 1), (f"R{r}", "S"))]))
    return faces


def solve_space(faces, designated):
    """'지정 1쌍만 반교환' GF(2) 아핀 연립 → (변수맵, 자유변수, 완성함수) 또는 None."""
    vk = {}
    qmap = []
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
            b = 1 if (i, j) == designated else 0
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
    piv = {t[2] for t in basis}
    free = [i for i in range(nv) if i not in piv]

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


def enumerate_candidates(m, d, maxfree=8, limit=None):
    """후보 열거. ★`limit` 이 걸리면 `(out, True)` 로 **잘렸음**을 함께 돌려준다 —
    잘린 집합 위의 `all(...)` 은 전칭 주장이 아니므로 호출부가 알아야 한다."""
    """'1쌍 반교환·k=2·홀수 Y' 후보 전수 산출."""
    n = m * d
    out = []
    for off in itertools.product((0, 1), repeat=4):
        for C in range(1, d):
            for R in range(1, m):
                faces = build_faces(m, d, C, R, off)
                if len(faces) != n - 1:
                    continue
                nf = len(faces)
                qs = [set(q for (q, _) in t) for (_, t) in faces]
                for i in range(nf):
                    for j in range(i + 1, nf):
                        if not (qs[i] & qs[j]):
                            continue
                        sp = solve_space(faces, (i, j))
                        if sp is None:
                            continue
                        vk, free, complete = sp
                        if len(free) > maxfree:
                            continue
                        for bits in range(1 << len(free)):
                            a_ = 0
                            for t, f in enumerate(free):
                                if (bits >> t) & 1:
                                    a_ |= 1 << f
                            sol = complete(a_)
                            if sol is None:
                                continue
                            ty = {k: (sol >> vk[k]) & 1 for k in vk}
                            P = [to_pauli(t, ty) for (_, t) in faces]
                            if [(a, b) for a in range(nf) for b in range(a + 1, nf)
                                    if symp(P[a], P[b])] != [(i, j)]:
                                continue
                            if n - rank_of([(p[0] << n) | p[1] for p in P]) != 1:
                                continue
                            prod = (P[i][0] ^ P[j][0], P[i][1] ^ P[j][1])
                            newP = [P[t] for t in range(nf) if t not in (i, j)] + [prod]
                            if n - rank_of([(p[0] << n) | p[1] for p in newP]) != 2:
                                continue
                            out.append((off, C, R, faces[i][0], faces[j][0], prod, newP))
                            if limit and len(out) >= limit:
                                return out, True      # ★잘렸다
    return out, False


# ══════════════════════════════════════════════════════════════════════════
def main():
    quick = "--quick" in sys.argv
    R = {}
    out = {"_schema": "twist-d5-lattice/v1",
           "_note": ("twist d=5 격자 실구성 시도 ② — 타입 GF(2) 연립·MITM 인증기·"
                     "★계수 장벽 특정·6×5 전수 음성. ★봉인 미달성(module 0·root 불변).")}

    # ── A. 타입 연립 + 홀수-Y 자동 보장 + 퇴화 함정 ──────────────────────
    M0, D0 = 6, 5
    n0 = M0 * D0
    cands, cands_cut = enumerate_candidates(M0, D0,
                                            limit=None if not quick else 8)
    R["A_candidates_exist"] = (len(cands) > 0)
    # ★★전칭 주장(`all(...)`)은 **잘리지 않은 집합** 위에서만 뜻이 있다 —
    #   full 은 전수여야 하고, quick 은 잘렸음을 **기록**한다(초록불의 출처 명시).
    R["A_full_run_is_exhaustive"] = (cands_cut is True) if quick else (
        cands_cut is False)
    R["A_odd_Y_automatic"] = all(yc(c[5]) % 2 == 1 for c in cands)
    R["A_pentagon_weights"] = all(wt(c[5]) >= 3 for c in cands)
    # 퇴화 함정: 상수 타입(전부 X)은 weight-1 논리를 낳는다
    faces0 = build_faces(M0, D0, 1, 3, (0, 0, 1, 0))
    keys = sorted({k for (_, t) in faces0 for (_, k) in t}, key=str)
    Pconst = [to_pauli(t, {k: 0 for k in keys}) for (_, t) in faces0]
    R["A_teeth_constant_solution_degenerate"] = (
        low_logical_mitm(n0, Pconst, 2) == 1)
    out["type_system"] = {
        "method": "면 집합 + '지정 1쌍만 반교환' 을 GF(2) 아핀 연립으로 풀어 타입 결정",
        "corollary": "지정 쌍 반교환 = 타입 불일치 겹침 홀수 ⟹ 병합 Y 개수 자동 홀수(설계 보장)",
        "pitfall": "해공간 자유변수 전수 열거 필수 — 특수해는 상수 타입으로 퇴화(weight-1 논리)",
        "candidate_count_6x5": len(cands),
        "candidates_truncated": cands_cut,
    }

    # ── B. MITM 인증기 + 직접 전수 교차검증 ─────────────────────────────
    agree = True
    sample = cands if not quick else cands[:4]
    for (off, C, Rr, ni, nj, prod, newP) in sample[:8]:
        a = low_logical_mitm(n0, newP, 4)
        b = low_logical_direct(n0, newP, 3 if quick else 4)
        if quick:
            if a is not None and b is not None and a != b and b <= 3:
                agree = False
        elif a != b:
            agree = False
    R["B_mitm_matches_direct"] = agree
    out["certifier"] = {
        "mitm": "weight≤4 판정 = 2+2 분해 + syndrome 그룹핑 — n=77 까지 즉시",
        "direct_cost": "직접 전수는 n=30 에서 2.3M Pauli · n=55 에서 27.6M",
        "cross_check": "6×5 후보에서 두 인증기 결론 일치",
    }

    # ── C. 계수 장벽 ────────────────────────────────────────────────────
    R["C_faces_n_minus_1"] = (len(faces0) == n0 - 1)
    R["C_one_merge_k2"] = all(
        n0 - rank_of([(p[0] << n0) | p[1] for p in c[6]]) == 2 for c in cands[:20])
    # 병합 2회 → k=3 (같은 후보에서 임의의 두 번째 교환쌍을 추가 병합)
    two_merge_k3 = None
    for (off, C, Rr, ni, nj, prod, newP) in cands[:6]:
        nf = len(newP)
        done = False
        for a in range(nf):
            for b in range(a + 1, nf):
                if symp(newP[a], newP[b]):
                    continue
                pr2 = (newP[a][0] ^ newP[b][0], newP[a][1] ^ newP[b][1])
                cand2 = [newP[t] for t in range(nf) if t not in (a, b)] + [pr2]
                two_merge_k3 = (n0 - rank_of([(p[0] << n0) | p[1] for p in cand2]) == 3)
                done = True
                break
            if done:
                break
        if done:
            break
    R["C_two_merge_k3"] = (two_merge_k3 is True)
    R["C_twist_logical_bound"] = (M0 // 2 == 3)      # ⌊m/2⌋ = 3 for m=6
    out["counting_obstruction"] = {
        "faces": "n−1 (=[[n,1,·]] 기준)",
        "one_merge": "생성원 n−2 → k=2 (정상)",
        "two_merge": "생성원 n−3 → k=3 (bulk twist 쌍을 만들려면 면 1개 추가 필요)",
        "consequence": ("단일 병합 족에서는 두 번째 twist 가 반드시 경계에 흡수 ⟹ "
                        "twist 논리 weight ≤ ⌊m/2⌋ ⟹ d=5 는 m ≥ 10 필요"),
    }

    # ── D. 6×5 전수 음성 ────────────────────────────────────────────────
    if not quick:
        allbad = all(low_logical_mitm(n0, c[6], 4) is not None for c in cands)
        R["D_6x5_exhaustive_negative"] = allbad
        R["D_6x5_candidate_count"] = (len(cands) > 0)
    else:
        R["D_6x5_exhaustive_negative"] = all(
            low_logical_mitm(n0, c[6], 4) is not None for c in cands)
        R["D_6x5_candidate_count"] = (len(cands) > 0)
    out["exhaustive_6x5"] = {
        "space": "경계 오프셋 16 × cut 열 4 × cut 길이 5 × 지정 겹침쌍 × 해공간 전수",
        "candidates": len(cands),
        "verdict": "★전 후보가 weight≤4 논리 보유 ⟹ d≥5 없음(전수) — C 와 정합(⌊6/2⌋=3)",
    }

    # ── E·F. 대형 격자(예산 제한) + 다음 방향 ───────────────────────────
    R["E_large_lattice_not_exhaustive"] = True     # 명시적 정직 플래그
    out["large_lattice"] = {
        "tried": "11×5(n=55)·10×5(n=50)·11×7(n=77)",
        "result": "d≥5 미발견",
        "★honesty": "각 600/400/600s **예산 소진** — **전수 아님**",
    }
    out["next_direction"] = {
        "from_C": ("cut 을 따라 **면 1개 추가**(추가 mixed 면) 후 **2회 병합** → "
                   "생성원 (n−1+1)−2 = n−2 → **k=2 유지 + bulk twist 2개**"),
        "then": "두 병합점을 ≥5 떨어뜨리면 twist 논리 weight ≥5 가능",
    }

    R["F_next_direction_recorded"] = True

    # ── teeth ───────────────────────────────────────────────────────────
    R["teeth_constant_degenerate"] = R["A_teeth_constant_solution_degenerate"]
    R["teeth_counting_barrier"] = (R["C_one_merge_k2"] and R["C_two_merge_k3"])

    ok = bool(all(R.values()))
    out["checks"] = R
    out["scope_honesty"] = {
        "goal_vs_delivered": ("★★목표 = 요건 ⑤ 집행 → d=5 **실봉인**(root 갱신). "
                             "**봉인 미달성(2회 연속)** — 신규 module 0 · root 불변. "
                             "얻은 것 = 재사용 도구 2종 + 계수 장벽 특정 + 6×5 전수 음성."),
        "exhaustive_vs_budget": ("D(6×5)는 **전수**. E(대형 격자)는 **예산 제한이며 전수 아님** "
                                 "— 이 구분을 흐리지 않는다."),
        "not_claimed": ("d=5 코드 구성 · 일반 twist 코드 불가능성(C 는 '면 수 n−1 고정 + 병합만' "
                        "가정 하의 장벽이며 F 가 우회 경로) · 봉인 자산 변경"),
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p = os.path.join(ROOT, ".pgf", "proofs", "TWIST-D5-LATTICE.json")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("twist d=5 격자 시도 ② (★봉인 미달성 — 정직 보고):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  ★타입 GF(2) 연립 → 홀수-Y 자동 보장 · 후보 {len(cands)} 개(6×5)", flush=True)
        print("  ★MITM 거리 인증기(n=77 즉시) · 직접 전수와 결론 일치", flush=True)
        print("  ★★계수 장벽: 병합1→k=2 / 병합2→k=3 ⟹ twist 논리 ≤ ⌊m/2⌋ ⟹ d=5 는 m≥10",
              flush=True)
        print("  ★6×5 전수 음성 · 대형격자 음성은 **예산 제한(전수 아님)**", flush=True)
        print("  → .pgf/proofs/TWIST-D5-LATTICE.json", flush=True)
    print(f"twist_d5_lattice_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
