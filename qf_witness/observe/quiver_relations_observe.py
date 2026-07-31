#!/usr/bin/env python
"""블록 대수의 **완전 제시** B ≅ kQ/I — 화살(Ext¹) 다음 층인 **관계식**(Ext²).

관측 7축 (정확 유한체 선형대수 · seal 아님 · module 0 · root 불변):
  A  A₇ p=2 **비주블록 기본대수** A = ⊕_{i,j} Hom_G(P_i,P_j) — dim A = Σ C_{ij} = 18
     (블록 차원 432 를 다루지 않는다) · ★Cartan 를 **Hom 차원으로 제4 재유도** ·
     rad 여과 rad^n 차원열 · ★graded 차원 = **Loewy 층 수와 일치**(게이트)
  B  ★**화살 = rad/rad² 기저** — 전일 Ext¹ 퀴버와 일치(재대조)
  C  ★★**관계식** I = ker(kQ → A) — 화살 리프트 전수 → **균질(homogeneous) 제시** 존재 판정 ·
     최소생성 차수별 · **최종 게이트 dim kQ/I = Σ C_{ij}** (제시의 완전성 인증)
  D  ★**Ext² = head(Ω²)** — Ω²(S_i) = ker(⊕_j P_j^{a_ij} --화살--> P_i).
     ★**화살 자체가 syzygy 의 사영 덮개 사상**이라는 관찰이 열쇠
  E  ★**독립 제2 경로** Ext²(S_i,S_j) ≅ Ext¹(ΩS_i,S_j) = H¹(G,Hom(ΩS_i,S_j)) —
     `ext1_pair_lean` 재사용(상한=하한 인증)
  F  A₆ p=2 **주블록** 동일 파이프라인 — dim A = 34
  G  ★★**종합**: 두 블록은 **퀴버가 동형**(3정점 별·화살 4개)이고 관계식도 **같은 개수(3)·
     같은 타입**(영관계 2 + 가환관계 1)인데 **가환관계의 차수가 4 vs 8** ⟹ dim 18 vs 34 —
     **퀴버만으로는 블록 대수가 결정되지 않는다**는 실례

방법(자체유도):
  ① 기본대수는 **준동형의 합성**으로 실물 계산 — dim Hom(P_i,P_j) = [P_j : S_i] = C_{ij}
  ② rad A ∩ Hom(P_i,P_j) = {φ : im φ ⊆ rad P_j} (i≠j 는 자동 — Nakayama)
  ③ 화살 리프트는 rad² 를 법으로만 정해진다 ⟹ **리프트 선택을 전수**해 균질 제시를 찾는다
  ④ 최소 관계식 개수 = Σ dim Ext²(S_i,S_j) — D·E 두 경로가 서로를 검증

정직 경계:
  · 관계식의 **명시 형태는 리프트 선택에 의존**한다(개수 = dim Ext² 는 불변). 본 관측은
    선택을 전수해 **균질 제시를 실제로 제시**하고 dim kQ/I 로 인증한다.
  · A₆ p=3 · A₇ p=2 **주블록**은 미착수(퀴버에 이중화살·자기고리가 있어 리프트 공간이 커진다).
  · 두 블록 대수가 **동형이 아님**은 dim 이 다름으로 즉시 따르나, 어떤 분류표의 이름인지는
    **주장하지 않는다**(외부 분류 인용 없음).
"""
import itertools
import json
import random
import sys
import time

import numpy as np

from qf_witness.observe.ext1_quiver_observe import (
    enumerate_group, extend_action, fano_gl42_gens, group_elems, heart_gens,
    inv_mod, rref_rows, ext1_pair_lean)
from qf_witness.observe.loewy_series_observe import (
    coset_data, coset_perm_module, decompose_regular, fixed_dim, hecke_endos,
    hom_space, image_basis, loewy_series, nullspace, submodule_action, subgroup)


# ══════════════════════════════════════════════════════════════════════════
# 기본대수 A = ⊕_{i,j} Hom_G(P_i,P_j) — 곱셈 = 준동형 합성
# ══════════════════════════════════════════════════════════════════════════
def quot_proj(Nrows, d, p):
    """π: F^d → F^q 로 π v = 0 ⟺ v ∈ span(Nrows) — head 로의 사영."""
    Nb, piv = rref_rows(Nrows.copy() % p, p)
    free = [c for c in range(d) if c not in set(piv)]
    M = np.eye(d, dtype=np.int64)
    for i, c in enumerate(piv):
        M[:, c] = (M[:, c] - Nb[i]) % p
    return M[free, :] % p, len(free)


def span_basis(mats, di, dj, p):
    """행렬 목록의 생성공간 기저(RREF)."""
    if not mats:
        return []
    return [r.reshape(dj, di) for r in
            rref_rows(np.array([m.reshape(-1) % p for m in mats],
                               dtype=np.int64), p)[0]]


def rad_filtration(names, DP, HOM, RADP, p):
    """rad A ∩ Hom(P_i,P_j) = {φ : im φ ⊆ rad P_j} 와 그 거듭곱."""
    proj = {k: quot_proj(RADP[k], DP[k], p)[0] for k in names}
    rad1 = {}
    for i in names:
        for j in names:
            B = HOM[(i, j)]
            rows = np.array([((proj[j] @ m) % p).reshape(-1) for m in B],
                            dtype=np.int64)
            out = []
            for c in nullspace(rows.T % p, p):
                M = np.zeros((DP[j], DP[i]), dtype=np.int64)
                for t, ct in enumerate(c):
                    if ct:
                        M = (M + B[t]) % p
                out.append(M)
            rad1[(i, j)] = out
    pows, cur = [], rad1
    for _ in range(40):
        pows.append({k: list(v) for k, v in cur.items()})
        if sum(len(v) for v in cur.values()) == 0:
            break
        nxt = {}
        for i in names:
            for j in names:
                nxt[(i, j)] = span_basis(
                    [(b @ a) % p for m in names for a in cur[(i, m)]
                     for b in rad1[(m, j)]], DP[i], DP[j], p)
        cur = nxt
    return rad1, pows


def arrow_lifts(names, DP, rad1, rad2, p):
    """화살 블록과 각 블록의 리프트 후보(rad¹∖rad² 원소) — 리프트는 rad² 법으로만 결정.
    (계수 열거는 비트로 하므로 p=2 전용 — 본 관측의 두 블록은 모두 p=2.)"""
    blocks = [(i, j) for i in names for j in names
              if len(rad1[(i, j)]) > len(rad2[(i, j)])]
    lifts = {}
    for (i, j) in blocks:
        r2 = [m.reshape(-1) % p for m in rad2[(i, j)]]
        Br, piv = (rref_rows(np.array(r2, dtype=np.int64), p) if r2
                   else (np.zeros((0, DP[i] * DP[j]), dtype=np.int64), []))
        cand, d1 = [], rad1[(i, j)]
        for bits in range(1, p ** len(d1)):
            M = np.zeros((DP[j], DP[i]), dtype=np.int64)
            for t in range(len(d1)):
                if bits >> t & 1:
                    M = (M + d1[t]) % p
            w = M.reshape(-1) % p
            for t, c in enumerate(piv):
                if w[c]:
                    w = (w - Br[t]) % p
            if w.any():
                cand.append(M)
        lifts[(i, j)] = cand
    return blocks, lifts


# ══════════════════════════════════════════════════════════════════════════
# 경로대수 kQ (절단) · 관계식 이데알
# ══════════════════════════════════════════════════════════════════════════
def build_paths(names, DP, arrows, maxd, p):
    """차수 ≤ maxd 의 전 경로와 그 행렬(합성)."""
    src = [a[0] for a in arrows]
    tgt = [a[1] for a in arrows]
    mat = [a[2] for a in arrows]
    pl = {0: [((), v) for v in names]}
    info = {((), v): (v, v, np.eye(DP[v], dtype=np.int64)) for v in names}
    for n in range(1, maxd + 1):
        cur = []
        for (t, s) in pl[n - 1]:
            last = tgt[t[-1]] if t else s
            for ai in range(len(arrows)):
                if src[ai] == last:
                    nt = t + (ai,)
                    cur.append((nt, s))
                    info[(nt, s)] = (s, tgt[ai], (mat[ai] @ info[(t, s)][2]) % p)
        pl[n] = cur
    return pl, info


def ker_deg(pl, info, n, p):
    """차수 n 경로들 중 A 에서 0 이 되는 조합(균질 관계식 후보)."""
    out, grp = [], {}
    for key in pl[n]:
        s, t, _M = info[key]
        grp.setdefault((s, t), []).append(key)
    for (_s, _t), keys in sorted(grp.items()):
        M = np.array([info[k][2].reshape(-1) % p for k in keys], dtype=np.int64)
        for c in nullspace(M.T % p, p):
            out.append(frozenset(keys[t] for t in range(len(keys)) if c[t]))
    return out


def ideal_rows(pl, info, gens, m, p):
    """이데알 ⟨gens⟩ 의 차수 m 성분 — q·g·r (q,r 은 경로)."""
    by_tgt, by_src = {}, {}
    for nn in range(m + 1):
        for k in pl[nn]:
            s, t, _M = info[k]
            by_tgt.setdefault((nn, t), []).append(k)
            by_src.setdefault((nn, s), []).append(k)
    ix = {k: t for t, k in enumerate(pl[m])}
    rows = []
    for (nn, g) in gens:
        if nn > m:
            continue
        gs, gt, _ = info[next(iter(g))]
        for a in range(m - nn + 1):
            b = m - nn - a
            for Q in by_tgt.get((a, gs), []):
                for R in by_src.get((b, gt), []):
                    v = np.zeros(len(pl[m]), dtype=np.int64)
                    for (gp, _gsrc) in g:
                        v[ix[(Q[0] + gp + R[0], Q[1])]] ^= 1
                    rows.append(v)
    return (np.array(rows, dtype=np.int64) if rows
            else np.zeros((0, len(pl[m])), dtype=np.int64))


def minimal_relations(pl, info, maxd, p):
    """차수별 **최소** 균질 관계식 — 하위 차수 이데알에 없는 것만 생성원으로."""
    gens, per_deg = [], {}
    for n in range(2, maxd + 1):
        kd = ker_deg(pl, info, n, p)
        idx = {k: t for t, k in enumerate(pl[n])}
        Cur = ideal_rows(pl, info, gens, n, p)
        rk = len(rref_rows(Cur.copy(), p)[0]) if len(Cur) else 0
        newg = []
        for g in kd:
            v = np.zeros(len(pl[n]), dtype=np.int64)
            for k in g:
                v[idx[k]] ^= 1
            st = np.vstack([Cur, v[None, :]]) if len(Cur) else v[None, :]
            nrk = len(rref_rows(st.copy(), p)[0])
            if nrk > rk:
                newg.append(g)
                Cur, rk = st, nrk
        gens.extend((n, g) for g in newg)
        per_deg[n] = newg
    return gens, per_deg


def quotient_dims(pl, info, gens, maxd, p):
    """dim (kQ/⟨gens⟩) 의 차수별 성분."""
    out = []
    for m in range(maxd + 1):
        IR = ideal_rows(pl, info, gens, m, p)
        rk = len(rref_rows(IR.copy(), p)[0]) if len(IR) else 0
        out.append(len(pl[m]) - rk)
    return out


# ══════════════════════════════════════════════════════════════════════════
# 한 블록 전체 — 기본대수 · 화살 · 관계식 · Ext²
# ══════════════════════════════════════════════════════════════════════════
def block_presentation(names, gens_g, PIM, simples, cartan, loewy_len, p,
                       lift_cap=8):
    d = {k: len(PIM[k][gens_g[0]]) for k in names}
    RADP = {}
    for k in names:
        homs = []
        for (_n, aS, dS) in simples:
            homs.extend(hom_space(PIM[k], aS, d[k], dS, gens_g, p))
        RADP[k] = nullspace(np.concatenate(homs, axis=0) % p, p)
    HOM = {(i, j): hom_space(PIM[i], PIM[j], d[i], d[j], gens_g, p)
           for i in names for j in names}
    cart_hom = [[len(HOM[(i, j)]) for j in names] for i in names]
    rad1, pows = rad_filtration(names, d, HOM, RADP, p)
    radpow = [sum(len(v) for v in w.values()) for w in pows]
    dimA = sum(len(v) for v in HOM.values())
    graded = [dimA - radpow[0]] + [radpow[t] - radpow[t + 1]
                                   for t in range(len(radpow) - 1)]
    blocks, lifts = arrow_lifts(names, d, pows[0], pows[1], p)
    nchoice = 1
    for b in blocks:
        nchoice *= len(lifts[b])
    # ★리프트 전수 — 영관계(길이 2 경로가 정확히 0)가 최다인 선택부터 시도하고
    #   **dim kQ/I = Σ C 게이트를 통과하는 첫 선택**을 채택(균질 제시의 실증적 탐색)
    comp = [(t1, t2) for t1, b1 in enumerate(blocks)
            for t2, b2 in enumerate(blocks) if b1[1] == b2[0]]
    ztab = {}
    for (t1, t2) in comp:
        for c1 in range(len(lifts[blocks[t1]])):
            for c2 in range(len(lifts[blocks[t2]])):
                pr = (lifts[blocks[t2]][c2] @ lifts[blocks[t1]][c1]) % p
                ztab[(t1, c1, t2, c2)] = not pr.any()
    ranked = sorted(itertools.product(*[range(len(lifts[b])) for b in blocks]),
                    key=lambda ch: (-sum(ztab[(t1, ch[t1], t2, ch[t2])]
                                         for (t1, t2) in comp), ch))
    maxd = loewy_len + 1
    tried, choice, arrows, pl, info = 0, None, None, None, None
    gens_rel, per_deg, qd = [], {}, []
    for ch in ranked[:lift_cap]:
        tried += 1
        arr = [(b[0], b[1], lifts[b][c]) for b, c in zip(blocks, ch)]
        pl2, info2 = build_paths(names, d, arr, maxd, p)
        g2, pd2 = minimal_relations(pl2, info2, maxd, p)
        q2 = quotient_dims(pl2, info2, g2, maxd, p)
        if sum(q2) == sum(sum(r) for r in cartan):
            choice, arrows, pl, info = ch, arr, pl2, info2
            gens_rel, per_deg, qd = g2, pd2, q2
            break
    mode = ("homogeneous-certified" if choice is not None
            else "not-certified(dim kQ/I ≠ ΣC)")
    if choice is None:                       # 정직 보고 — 첫 후보로 진행
        choice = ranked[0]
        arrows = [(b[0], b[1], lifts[b][c]) for b, c in zip(blocks, choice)]
        pl, info = build_paths(names, d, arrows, maxd, p)
        gens_rel, per_deg = minimal_relations(pl, info, maxd, p)
        qd = quotient_dims(pl, info, gens_rel, maxd, p)
    # 전사성: 차수 < LL 경로들의 상이 A 전체
    allm = {}
    for n in range(loewy_len):
        for key in pl[n]:
            s, t, M = info[key]
            allm.setdefault((s, t), []).append(M)
    img = sum(len(span_basis(v, d[k[0]], d[k[1]], p)) for k, v in allm.items())
    # ★Ext² = head(Ω²) · Ω²(S_i) = ker(⊕_j P_j^{a_ij} --화살--> P_i)
    ext2, om2 = {}, {}
    for i in names:
        ins = [a for a in arrows if a[1] == i]
        srcs = [a[0] for a in ins]
        M = np.concatenate([a[2] for a in ins], axis=1) % p
        dtot = int(M.shape[1])
        act = {}
        for g in gens_g:
            Z = np.zeros((dtot, dtot), dtype=np.int64)
            off = 0
            for s in srcs:
                B_ = PIM[s][g] % p
                Z[off:off + len(B_), off:off + len(B_)] = B_
                off += len(B_)
            act[g] = Z
        ker = nullspace(M, p)
        actO, _b = submodule_action(act, gens_g, ker, p)
        dO = len(ker)
        hd = [len(hom_space(actO, aS, dO, dS, gens_g, p))
              for (_n, aS, dS) in simples]
        lay = loewy_series(actO, dO, gens_g, simples, p)
        ext2[i] = hd
        om2[i] = {"P1_dim": dtot, "image_dim": len(image_basis(M, p)),
                  "rad_P_dim": len(RADP[i]), "Omega2_dim": dO,
                  "head": hd, "loewy_layers": [list(x) for x in lay]}
    return {
        "dim_P": [d[k] for k in names],
        "cartan_via_hom": cart_hom,
        "cartan_expected": cartan,
        "dim_basic_algebra": dimA,
        "cartan_sum": sum(sum(r) for r in cartan),
        "rad_power_dims": radpow,
        "graded_dims": graded,
        "arrow_blocks": [list(b) for b in blocks],
        "n_arrows": len(arrows),
        "lift_candidates": {f"{b[0]}->{b[1]}": len(lifts[b]) for b in blocks},
        "lift_choices_total": nchoice,
        "lift_mode": mode,
        "lift_tried": tried,
        "lift_chosen": list(choice),
        "path_counts": [len(pl[n]) for n in range(maxd + 1)],
        "image_dim_kQ_to_A": img,
        "relations": {str(n): [sorted(tuple(x[0]) for x in g) for g in gg]
                      for n, gg in sorted(per_deg.items()) if gg},
        "relation_srctgt": {str(n): [[info[next(iter(g))][0],
                                     info[next(iter(g))][1]] for g in gg]
                            for n, gg in sorted(per_deg.items()) if gg},
        "n_relations": sum(len(v) for v in per_deg.values()),
        "relation_degrees": sorted(n for n, gg in per_deg.items() for _ in gg),
        "quotient_dims": qd,
        "dim_kQ_over_I": sum(qd),
        "ext2_matrix": [ext2[k] for k in names],
        "ext2_total": sum(sum(ext2[k]) for k in names),
        "omega2": om2,
        "arrow_legend": [[t, arrows[t][0], arrows[t][1]]
                         for t in range(len(arrows))],
    }, arrows, RADP


# ══════════════════════════════════════════════════════════════════════════
def a7_nonprincipal_pims(mul7, id7, ord7, A7G, simples7, N7, syl2_7):
    """지수 크기 사영 운반자에서 P(4̂)·P(4̄̂)·P(6̂) 만 뽑는다."""
    carriers = {"F21": ([(1, 2, 3, 4, 5, 6, 0), (0, 2, 4, 6, 1, 3, 5)], 120),
                "Syl3": ([(1, 2, 0, 3, 4, 5, 6), (0, 1, 2, 4, 5, 3, 6)], 280)}
    want = {"4": 24, "4b": 24, "6": 40}
    PIM, info = {}, {}
    for cn, (hg, idxn) in carriers.items():
        Hl = subgroup(hg, mul7, id7)
        n_, reps_, perms_, mats_ = coset_data(ord7, mul7, id7, A7G, Hl)
        actX = extend_action(A7G, mul7, id7, mats_, 2, ord7)
        alg = hecke_endos(n_, perms_, Hl, reps_)
        rng7 = random.Random(7)                         # 결정론 시드

        def _rnd(alg=alg, rng7=rng7, n_=n_):
            M = np.zeros((n_, n_), dtype=np.int64)
            for A_ in rng7.sample(alg, max(2, len(alg) // 3)):
                M = (M + A_) % 2
            return M

        ps = []
        decompose_regular(np.eye(n_, dtype=np.int64),
                          np.eye(n_, dtype=np.int64), _rnd, 2, rng7, ps)
        info[cn] = {"index": n_, "projective": fixed_dim(actX, syl2_7, n_, 2)
                    == n_ // 8, "parts": sorted(len(b) for b in ps)}
        for B in sorted(ps, key=len):
            dd = len(B)
            if dd not in (24, 40):
                continue
            actY, _ = submodule_action(actX, A7G, B, 2)
            hd = tuple(len(hom_space(actY, aS, dd, dS, A7G, 2))
                       for _, aS, dS in simples7)
            nm = next((k for t, k in enumerate(N7)
                       if hd == tuple(1 if j == t else 0 for j in range(len(N7)))),
                      None)
            if nm in want and nm not in PIM and want[nm] == dd:
                PIM[nm] = {g: actY[g] % 2 for g in A7G}
        if all(k in PIM for k in want):
            break
    return PIM, info


def main():
    quick = "--quick" in sys.argv
    t0 = time.time()
    R = {}
    out = {"_schema": "quiver-relations/v1",
           "_note": ("블록 대수의 완전 제시 B ≅ kQ/I — 화살(Ext¹) 다음 층인 관계식(Ext²). "
                     "관측·seal 아님·module 0·root 불변.")}

    # ── A₆ p=2 주블록 준비(값싼 운반자) ─────────────────────────────────
    A6G = [(1, 2, 0, 3, 4, 5), (0, 1, 2, 4, 5, 3), (1, 0, 3, 2, 4, 5)]
    mul6, id6, ord6 = enumerate_group(A6G, 6)
    R["setup_A6_360"] = (len(ord6) == 360)
    g6 = {"1": [np.eye(1, dtype=np.int64)] * 3,
          "4a": fano_gl42_gens(None, 7, [tuple(list(g) + [6]) for g in A6G]),
          "4b": heart_gens(A6G, 6, 2)}
    N6 = ["1", "4a", "4b"]
    S6 = {k: extend_action(A6G, mul6, id6, v, 2, ord6) for k, v in g6.items()}
    D6 = {"1": 1, "4a": 4, "4b": 4}
    sim6 = [(k, S6[k], D6[k]) for k in N6]
    syl2_6 = subgroup([(1, 0, 3, 2, 4, 5), (2, 3, 0, 1, 4, 5), (0, 1, 3, 2, 5, 4)],
                      mul6, id6)
    syl3_6 = subgroup([(1, 2, 0, 3, 4, 5), (0, 1, 2, 4, 5, 3)], mul6, id6)
    R["F_A6_syl_orders"] = (len(syl2_6) == 8 and len(syl3_6) == 9)
    n40, mats40 = coset_perm_module(ord6, mul6, id6, A6G, syl3_6, 2)
    act40 = extend_action(A6G, mul6, id6, mats40, 2, ord6)
    PIM6 = {"1": {g: act40[g] % 2 for g in A6G}}
    carr6 = {}
    for cn, hgen in (("C3a", [(1, 2, 0, 3, 4, 5)]), ("C3b", [(1, 2, 0, 4, 5, 3)])):
        Hl = subgroup(hgen, mul6, id6)
        mS = {k: fixed_dim(S6[k], Hl, D6[k], 2) for k in N6}
        n_, reps_, perms_, mats_ = coset_data(ord6, mul6, id6, A6G, Hl)
        actX = extend_action(A6G, mul6, id6, mats_, 2, ord6)
        alg = hecke_endos(n_, perms_, Hl, reps_)
        rng = random.Random(7)                          # 결정론 시드

        def _rnd(alg=alg, rng=rng, n_=n_):
            M = np.zeros((n_, n_), dtype=np.int64)
            for A_ in rng.sample(alg, max(2, len(alg) // 3)):
                M = (M + A_) % 2
            return M

        ps = []
        decompose_regular(np.eye(n_, dtype=np.int64),
                          np.eye(n_, dtype=np.int64), _rnd, 2, rng, ps)
        got = {}
        for B in sorted(ps, key=len):
            dd = len(B)
            actY, _ = submodule_action(actX, A6G, B, 2)
            hd = tuple(len(hom_space(actY, aS, dd, dS, A6G, 2))
                       for _n, aS, dS in sim6)
            nm = next((k for t, k in enumerate(N6)
                       if hd == tuple(1 if j == t else 0 for j in range(3))), None)
            got[nm] = got.get(nm, 0) + 1
            if nm in ("4a", "4b") and nm not in PIM6 and dd == 24:
                PIM6[nm] = {g: actY[g] % 2 for g in A6G}
        carr6[cn] = {"index": n_, "hecke_dim": len(alg), "frobenius_m_S": mS,
                     "projective": fixed_dim(actX, syl2_6, n_, 2) == n_ // 8,
                     "parts": sorted(len(b) for b in ps),
                     "identified": {str(k): v for k, v in sorted(
                         got.items(), key=lambda t: (t[0] is None, t[0]))}}
    R["F_A6_carriers_projective"] = all(v["projective"] for v in carr6.values())
    # ★Frobenius 상호율: 두 C₃ 류가 4ₐ·4_b 를 **상보적으로** 준다(m_S 예측 = 실측 중복도)
    R["F_A6_frobenius_complementary"] = (
        carr6["C3a"]["frobenius_m_S"]["4b"] == 2
        and carr6["C3a"]["frobenius_m_S"]["4a"] == 0
        and carr6["C3b"]["frobenius_m_S"]["4a"] == 2
        and carr6["C3b"]["frobenius_m_S"]["4b"] == 0
        and carr6["C3a"]["identified"].get("4b") == 2
        and carr6["C3b"]["identified"].get("4a") == 2)
    R["F_A6_all_three_pims"] = (sorted(PIM6) == ["1", "4a", "4b"])
    R["F_A6_pim_dims"] = ([len(PIM6[k][A6G[0]]) for k in N6] == [40, 24, 24])

    C6 = [[8, 4, 4], [4, 3, 2], [4, 2, 3]]
    B6, _ar6, _rp6 = block_presentation(N6, A6G, PIM6, sim6, C6, 9, 2)
    R["F_A6_cartan_via_hom"] = (B6["cartan_via_hom"] == C6)
    R["F_A6_dim_basic_34"] = (B6["dim_basic_algebra"] == 34
                              == B6["cartan_sum"])
    R["F_A6_graded_matches_loewy"] = (
        B6["graded_dims"] == [3, 4, 4, 4, 4, 4, 4, 4, 3])
    R["F_A6_rad_powers"] = (B6["rad_power_dims"]
                            == [31, 27, 23, 19, 15, 11, 7, 3, 0])
    R["F_A6_lift_certified"] = (B6["lift_mode"] == "homogeneous-certified"
                                and B6["lift_choices_total"] == 4096)
    R["F_A6_four_arrows_star"] = (
        B6["n_arrows"] == 4
        and sorted(tuple(b) for b in B6["arrow_blocks"])
        == [("1", "4a"), ("1", "4b"), ("4a", "1"), ("4b", "1")])
    R["F_A6_surjective"] = (B6["image_dim_kQ_to_A"] == 34)
    R["F_A6_three_relations"] = (B6["n_relations"] == 3)
    R["F_A6_relation_degrees"] = (B6["relation_degrees"] == [2, 2, 8])
    R["F_A6_dim_kQ_over_I_34"] = (B6["dim_kQ_over_I"] == 34)
    R["F_A6_ext2_identity"] = (B6["ext2_matrix"]
                               == [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    R["F_A6_ext2_equals_relations"] = (B6["ext2_total"] == B6["n_relations"] == 3)
    out["F_A6_p2_principal"] = {"carriers": carr6, "presentation": B6,
                               "note": ("P(1̂)=𝔽₂[A₆/Syl₃] · P(4ₐ)·P(4_b) 는 "
                                        "★**두 C₃ 켤레류의 운반자가 상보적으로** 준다"
                                        "(Frobenius m_S 예측=실측)")}

    # ── A₇ p=2 비주블록(운반자 분해 필요 — full 전용) ────────────────────
    if not quick:
        A7G = [(1, 2, 0, 3, 4, 5, 6), (1, 2, 3, 4, 5, 6, 0)]
        mul7, id7, ord7 = enumerate_group(A7G, 7)
        par7, ord7bfs = group_elems(A7G, mul7, id7)
        R["setup_A7_2520"] = (len(ord7) == 2520)
        g4 = fano_gl42_gens(None, 7, A7G)
        g4b = [np.array(np.transpose(inv_mod(m, 2)), dtype=np.int64) % 2
               for m in g4]

        def _w2(M):
            pr = list(itertools.combinations(range(4), 2))
            ix = {t: i for i, t in enumerate(pr)}
            O = np.zeros((6, 6), dtype=np.int64)
            for jc, (a, b) in enumerate(pr):
                for i in range(4):
                    for j in range(4):
                        if i != j and M[i][a] * M[j][b] % 2:
                            O[ix[(min(i, j), max(i, j))]][jc] ^= 1
            return O

        raw7 = {"4": (g4, 4), "4b": (g4b, 4), "6": ([_w2(m) for m in g4], 6)}
        N7 = ["4", "4b", "6"]
        S7 = {k: extend_action(A7G, mul7, id7, gm, 2, ord7)
              for k, (gm, _d) in raw7.items()}
        D7 = {k: dd for k, (_gm, dd) in raw7.items()}
        sim7 = [(k, S7[k], D7[k]) for k in N7]
        syl2_7 = subgroup([(1, 2, 3, 0, 5, 4, 6), (2, 1, 0, 3, 5, 4, 6)],
                          mul7, id7)
        R["A_A7_syl2_order8"] = (len(syl2_7) == 8)
        PIM7, cinfo = a7_nonprincipal_pims(mul7, id7, ord7, A7G, sim7, N7,
                                           syl2_7)
        R["A_A7_all_three_pims"] = (sorted(PIM7) == ["4", "4b", "6"])
        R["A_A7_pim_dims"] = ([len(PIM7[k][A7G[0]]) for k in N7]
                              == [24, 24, 40])
        C7 = [[2, 1, 2], [1, 2, 2], [2, 2, 4]]
        B7, arrows7, RADP7 = block_presentation(N7, A7G, PIM7, sim7, C7, 5, 2)
        R["A_A7_cartan_via_hom"] = (B7["cartan_via_hom"] == C7)
        R["A_A7_dim_basic_18"] = (B7["dim_basic_algebra"] == 18
                                  == B7["cartan_sum"])
        R["A_A7_rad_powers"] = (B7["rad_power_dims"] == [15, 11, 7, 3, 0])
        R["A_A7_graded_matches_loewy"] = (B7["graded_dims"] == [3, 4, 4, 4, 3])
        R["A_A7_block_dim_432_untouched"] = (
            sum(B7["dim_P"][t] * D7[N7[t]] for t in range(3)) == 432)
        R["B_A7_four_arrows_star"] = (
            B7["n_arrows"] == 4
            and sorted(tuple(b) for b in B7["arrow_blocks"])
            == [("4", "6"), ("4b", "6"), ("6", "4"), ("6", "4b")])
        R["B_A7_surjective"] = (B7["image_dim_kQ_to_A"] == 18)
        R["C_A7_lift_certified"] = (B7["lift_mode"] == "homogeneous-certified"
                                    and B7["lift_choices_total"] == 16)
        R["C_A7_three_relations"] = (B7["n_relations"] == 3)
        R["C_A7_relation_degrees"] = (B7["relation_degrees"] == [2, 2, 4])
        R["C_A7_dim_kQ_over_I_18"] = (B7["dim_kQ_over_I"] == 18)
        R["D_A7_ext2_identity"] = (B7["ext2_matrix"]
                                   == [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        R["D_A7_ext2_equals_relations"] = (B7["ext2_total"]
                                           == B7["n_relations"] == 3)
        R["D_A7_omega2_covers_rad"] = all(
            v["image_dim"] == v["rad_P_dim"] for v in B7["omega2"].values())
        out["A_A7_p2_nonprincipal"] = {"carriers": cinfo, "presentation": B7}

        # ── E. 독립 제2 경로 Ext²(S_i,S_j) = H¹(G, Hom(ΩS_i,S_j)) ────────
        e2h, cert_all = {}, True
        for i in N7:
            actR, br = submodule_action(PIM7[i], A7G, RADP7[i], 2)
            dR = len(br)
            full = extend_action(A7G, mul7, id7, [actR[g] for g in A7G], 2, ord7)
            row, cr = [], []
            for j in N7:
                e, cert, _det = ext1_pair_lean(A7G, mul7, id7, ord7bfs, par7,
                                               full, S7[j], dR, D7[j], 2, 60)
                row.append(e)
                cr.append(bool(cert))
            e2h[i] = {"dim_Omega": dR, "ext2_row": row, "certified": cr}
            cert_all = cert_all and all(cr)
        R["E_A7_h1_route_certified"] = cert_all
        R["E_A7_two_routes_agree"] = ([e2h[k]["ext2_row"] for k in N7]
                                      == B7["ext2_matrix"])
        out["E_A7_ext2_via_H1"] = {
            "identity": "Ext²(S_i,S_j) ≅ Ext¹(ΩS_i,S_j) = H¹(G, Hom(ΩS_i,S_j))",
            "rows": e2h,
            "note": "전일 `ext1_pair_lean`(상한/하한 협공) 를 syzygy 에 그대로 적용",
        }

        # ── G. 종합 — 퀴버 동형·대수 비동형 ──────────────────────────────
        same_quiver = (B6["n_arrows"] == B7["n_arrows"] == 4
                       and len(N6) == len(N7) == 3
                       and sorted(B6["graded_dims"][:2])
                       == sorted(B7["graded_dims"][:2]))
        R["G_same_quiver"] = same_quiver
        R["G_same_relation_count_and_types"] = (
            B6["n_relations"] == B7["n_relations"] == 3
            and B6["relation_degrees"][:2] == B7["relation_degrees"][:2] == [2, 2]
            and len(B6["relations"]["2"]) == len(B7["relations"]["2"]) == 2
            and len(B6["relations"]["8"]) == len(B7["relations"]["4"]) == 1)
        R["G_commutativity_degree_differs"] = (
            B6["relation_degrees"][2] == 8 and B7["relation_degrees"][2] == 4)
        R["G_algebras_not_isomorphic"] = (
            B6["dim_kQ_over_I"] == 34 and B7["dim_kQ_over_I"] == 18)
        R["G_ext2_identity_both"] = (B6["ext2_matrix"] == B7["ext2_matrix"]
                                     == [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        out["G_comparison"] = {
            "quiver": ("두 블록 모두 **3 정점 별 + 화살 4개**(중심↔양 끝, 양방향) — "
                       "A₆ p=2 중심 1̂ · A₇ p=2 비주 중심 6̂"),
            "relations": {
                "A6_p2_principal": {"zero_relations_deg2": 2,
                                    "commutativity_degree": 8,
                                    "dim": B6["dim_kQ_over_I"]},
                "A7_p2_nonprincipal": {"zero_relations_deg2": 2,
                                       "commutativity_degree": 4,
                                       "dim": B7["dim_kQ_over_I"]}},
            "headline": ("★★**퀴버가 동형인데 대수는 동형이 아니다** — 관계식 개수(3)와 "
                         "타입(영관계 2 + 가환관계 1)까지 같고 **가환관계의 차수만** "
                         "8 vs 4 로 다른데 그것이 dim 34 vs 18 을 만든다 ⟹ "
                         "**Ext¹ 퀴버만으로는 블록 대수가 결정되지 않는다**(실례)"),
            "ext2": "두 블록 모두 Ext² = 단위행렬(정점마다 관계식 정확히 1개)",
        }
    ok = bool(all(R.values()))
    out["checks"] = R
    out["method"] = {
        "basic_algebra": ("A = ⊕_{i,j} Hom_G(P_i,P_j) · 곱셈 = 준동형 합성 · "
                          "dim Hom(P_i,P_j) = [P_j : S_i] = C_{ij} ⟹ dim A = Σ C_{ij} "
                          "(블록 차원 432/232 를 다루지 않는다)"),
        "radical": "rad A ∩ Hom(P_i,P_j) = {φ : im φ ⊆ rad P_j} — i≠j 는 자동(Nakayama)",
        "arrows": "화살 = rad/rad² 기저 · ★리프트는 rad² 법으로만 정해진다 ⟹ 전수 탐색",
        "relations": ("I = ker(kQ → A) · 최소 균질 생성원을 차수별로 추출하고 "
                      "**dim kQ/I = Σ C_{ij}** 로 제시의 완전성 인증"),
        "ext2": ("★Ω²(S_i) = ker(⊕_j P_j^{a_ij} --화살--> P_i) — **화살 자체가 syzygy 의 "
                 "사영 덮개 사상** · Ext² = head(Ω²) · 제2 경로 = H¹(G,Hom(ΩS_i,S_j))"),
        "determinism": "random.Random(7) 고정 시드 · 리프트 선택 = (최다 균질 관계식, 사전순)",
    }
    out["scope_honesty"] = {
        "delivered": ("★A₇ p=2 비주블록·A₆ p=2 주블록 **두 블록의 완전 제시 B ≅ kQ/I** · "
                      "Cartan 를 Hom 차원으로 제4 재유도 · graded = Loewy 층 게이트 · "
                      "★관계식 3개 명시(영관계 2 + 가환관계 1) · dim kQ/I = Σ C 인증 · "
                      "★Ext² 두 독립 경로 일치(Ω² head · H¹ syzygy) · "
                      "★★퀴버 동형·대수 비동형 실례"),
        "not_yet": ("A₇ p=2 **주블록**(자기고리·리프트 공간 큼)·A₆ p=3(이중화살·GF(9) 융합) · "
                    "관계식의 **기저 무의존 불변량**(본 관측은 개수는 불변·형태는 리프트 의존을 명시)"),
        "not_claimed": ("봉인 게이트 · 외부 분류표의 이름(dihedral/quaternion type 등) · "
                        "두 대수의 유도동등성(derived equivalence) 여부"),
    }
    out["all_ok"] = ok

    if not quick:
        import os
        from qf_witness.core.paths import ROOT
        p_ = os.path.join(ROOT, ".pgf", "proofs", "QUIVER-RELATIONS.json")
        os.makedirs(os.path.dirname(p_), exist_ok=True)
        with open(p_, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("블록 대수 완전 제시 B ≅ kQ/I (정확 — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        for nm, Bx in (("A₇ p=2 비주", B7), ("A₆ p=2 주", B6)):
            print(f"  ★{nm}: dim A = {Bx['dim_basic_algebra']} = ΣC · "
                  f"화살 {Bx['n_arrows']} · graded {Bx['graded_dims']}", flush=True)
            print(f"    관계식 {Bx['n_relations']}개 차수 {Bx['relation_degrees']} · "
                  f"dim kQ/I = {Bx['dim_kQ_over_I']} · Ext² {Bx['ext2_matrix']}",
                  flush=True)
            print(f"    화살 {Bx['arrow_legend']} · 관계식 {Bx['relations']}",
                  flush=True)
        print("  ★★퀴버 동형(3정점 별·화살 4)인데 dim 34 vs 18 — 가환관계 차수 8 vs 4",
              flush=True)
        print("  ★Ext² 두 독립 경로 일치: head(Ω²) · H¹(G,Hom(ΩS,T))", flush=True)
        print("  → .pgf/proofs/QUIVER-RELATIONS.json", flush=True)
        print(f"  (elapsed {time.time() - t0:.1f}s)", flush=True)
    if not ok:
        print("  ✗ 실패 체크:", [k for k, v in R.items() if not v], flush=True)
    print(f"quiver_relations_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
