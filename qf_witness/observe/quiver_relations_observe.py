#!/usr/bin/env python
"""블록 대수의 **완전 제시** B ≅ kQ/I — 화살(Ext¹) 다음 층인 **관계식**(Ext²).

관측 12축 (정확 유한체 선형대수 · seal 아님 · module 0 · root 불변):
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
  H  ★★A₇ p=2 **주블록**(1̂·14̂·20̂ · dim A = 19) — **자기고리를 품은 첫 제시**.
     ★★**균질 제시가 존재하지 않는다**(리프트 32 **전수** 실패) ⟹ **비균질 관계식 강제** ·
     정체는 **γ² ≠ 0**(자기고리의 제곱 = 길이-4 경로) · ★**Ext² 에 처음 다중도 2**
  I  ★★3 블록 종합 — **자기고리가 있는 블록에서만 균질 제시가 깨진다**(실측·기전 무주장)
  J  ★★A₆ p=3 주블록 **over 𝔽₃** — ★**𝔽₃ 는 분해체가 아니다**(End(6̃)=GF(9) 실측) ⟹
     화살이 GF(9)-이중가군이라 `kQ/I` 틀이 성립하지 않는다(**species**) ·
     ★**A₆ p=3 Loewy 급수 최초 산출**(전부 LL=5·회문) · dim A = 36 · Ext²(리프트-무관)
  K  ★★**GF(9) 로 올라간다** — J(=√−1)를 **추가 생성원**으로 넣어 실현화하면 기존
     파이프라인이 그대로 돈다 · 4 정점·**화살 8개(이중화살 1̂↔4)**·Cartan·Loewy 완전 재유도
  L  ★★4 블록 종합 — **제시를 막는 이유가 두 종류**(자기고리 / 비분해체)이고 서로 **독립**

방법(자체유도):
  ① 기본대수는 **준동형의 합성**으로 실물 계산 — dim Hom(P_i,P_j) = [P_j : S_i] = C_{ij}
  ② rad A ∩ Hom(P_i,P_j) = {φ : im φ ⊆ rad P_j} (i≠j 는 자동 — Nakayama)
  ③ 화살 리프트는 rad² 를 법으로만 정해진다 ⟹ **리프트 선택을 전수**해 균질 제시를 찾는다
  ④ ★**리프트-무관 경로**: kQ/J^maxd 안에서 I 와 J·I + I·J 를 직접 계산해
     **비균질 관계식까지** 최소 생성원을 센다(`minimal_generators_filtered`) —
     균질 제시가 있는 두 블록에서는 ③의 결과를 **그대로 재현**(기계 자체검증)
  ⑤ 최소 관계식 개수 = Σ dim Ext²(S_i,S_j) — 두 경로가 서로를 검증

정직 경계:
  · 관계식의 **명시 형태는 리프트 선택에 의존**한다(개수 = dim Ext² 는 불변).
  · A₇ **주블록**의 H¹ 경로는 **부분만**(1̂ 열) — m = dim ΩS_i·dim S_j 가 최대 1420
    (비주블록은 204)이라 `ext1_pair_lean` 의 m×m 캐시가 규모 밖. 총 개수는 head(Ω²) 와
    리프트-무관 최소생성 **두 경로가 이미 대조**한다.
  · A₆ p=3 의 **GF(9) 관계식은 정직 유보** — GF(9) PIM 사이의 Hom 이 dim_{𝔽₃} 최대
    72×72 = 5184 계 16 쌍이라 규모 밖(퀴버까지는 완전 재유도·𝔽₃ 축 Ext² 는 산출).
  · 대수가 **동형이 아님**은 dim 이 다름으로 즉시 따르나, 어떤 분류표의 이름인지는
    **주장하지 않는다**(외부 분류 인용 없음). "자기고리 ⟹ 비균질"의 **기전도 무주장**.
"""
import itertools
import json
import random
import sys
import time

import numpy as np

from qf_witness.observe.ext1_quiver_observe import (
    build_a7_principal_gens, enumerate_group, extend_action, fano_gl42_gens,
    group_elems, heart_gens, inv_mod, rref_rows, ext1_pair_lean)
from qf_witness.observe.loewy_series_observe import (
    coset_data, coset_perm_module, decompose_regular, fixed_dim, hecke_endos,
    hom_space, image_basis, loewy_series, nullspace, nullspace_gf2,
    quotient_action, restrict, submodule_action, subgroup)


# ══════════════════════════════════════════════════════════════════════════
# 기본대수 A = ⊕_{i,j} Hom_G(P_i,P_j) — 곱셈 = 준동형 합성
# ══════════════════════════════════════════════════════════════════════════
def hom_space_fast(actA, actB, dA, dB, gens, p):
    """★대형 Hom_G(A,B) — `np.kron` 없이 uint8 블록으로 제약행렬 구성(GF(2) 전용).

    `hom_space` 는 kron(I_dB, A^T) − kron(B, I_dA) 를 **int64** 로 만든다:
    dA=dB=72 면 5184×5184×8B = 215MB/생성원 → 개수 곱하면 GB 급이 되어 막힌다.
    같은 행렬을 (dB,dA,dB,dA) uint8 텐서의 두 슬라이스 대입으로 직접 쓰면 27MB.
    ★행 순서·부호(GF(2) 에서 − = XOR)가 동일하므로 **기저도 byte-identical**."""
    if p != 2:
        return hom_space(actA, actB, dA, dB, gens, p)
    m = dA * dB
    rows = np.zeros((len(gens) * m, m), dtype=np.uint8)
    for t, g in enumerate(gens):
        A = (actA[g] % 2).astype(np.uint8)
        B = (actB[g] % 2).astype(np.uint8)
        T = np.zeros((dB, dA, dB, dA), dtype=np.uint8)
        At = np.ascontiguousarray(A.T)
        for r in range(dB):
            T[r, :, r, :] ^= At                  # kron(I_dB, A^T)
        for c in range(dA):
            T[:, c, :, c] ^= B                   # − kron(B, I_dA)  (GF(2) ⟹ XOR)
        rows[t * m:(t + 1) * m] = T.reshape(m, m)
    return [v.reshape(dB, dA) % 2 for v in nullspace_gf2(rows)]


def hom_space_iter(actA, actB, dA, dB, gens, p):
    """★p-일반 대형 Hom_G(A,B) — kron 없이 + **생성원별 순차 교차**.

    한 번에 (|gens|·m)×m 를 RREF 하는 대신 첫 생성원의 커널로 공간을 좁히고
    다음 생성원 제약을 **좁혀진 좌표에서** 푼다(둘째부터 열 수가 급감).
    GF(2) 는 비트팩 경로가 더 빠르므로 `hom_space_fast` 로 위임."""
    if p == 2:
        return hom_space_fast(actA, actB, dA, dB, gens, p)
    m = dA * dB
    K = None
    for g in gens:
        A = actA[g] % p
        B = actB[g] % p
        T = np.zeros((dB, dA, dB, dA), dtype=np.int64)
        At = np.ascontiguousarray(A.T)
        for r in range(dB):
            T[r, :, r, :] = At
        for c in range(dA):
            T[:, c, :, c] = (T[:, c, :, c] - B) % p
        C = T.reshape(m, m) % p
        if K is None:
            N = nullspace(C, p)
        else:
            N = nullspace((C @ K.T) % p, p)
            N = (N @ K) % p if len(N) else N
        K = N
        if len(K) == 0:
            return []
    return [v.reshape(dB, dA) % p for v in K]


def hecke_endos_p(n, perms, Hlist, reps, p):
    """`hecke_endos` 의 p-일반 판본 — End_G(k[G/H]) 기저 = H-궤도 합."""
    seen, orbits = set(), []
    for j in range(n):
        if j in seen:
            continue
        orb = {perms[h][j] for h in Hlist}
        seen |= orb
        orbits.append(sorted(orb))
    mats = []
    for orb in orbits:
        M = np.zeros((n, n), dtype=np.int64)
        for j in range(n):
            pj = perms[reps[j]]
            for t in orb:
                M[pj[t], j] += 1
        mats.append(M % p)
    return mats


def greedy_cover(actM, dM, PIM, dimP, names, simples, gens, p):
    """★리프트-무관 사영 덮개 — head 로의 상이 전사가 될 때까지 Hom(P_j,M) 에서
    준동형을 **탐욕적으로** 고른다. 화살·리프트 선택을 전혀 쓰지 않으므로
    비분해체(species) 상황에서도 그대로 동작한다. 반환 (Ω 작용, dimΩ, 사용 중복도)."""
    homs = []
    for (_n, aS, dS) in simples:
        homs.extend(hom_space_iter(actM, aS, dM, dS, gens, p))
    radM = nullspace(np.concatenate(homs, axis=0) % p, p)
    proj = quot_proj(radM, dM, p)[0]                 # M ↠ head(M)
    q = proj.shape[0]
    picked, mult = [], {k: 0 for k in names}
    acc = np.zeros((0, q), dtype=np.int64)           # head(M) 안에서 덮은 부분공간
    rk = 0
    for j in names:
        if rk >= q:
            break
        for phi in hom_space_iter(PIM[j], actM, dimP[j], dM, gens, p):
            cols = ((proj @ phi) % p).T % p          # (dimP[j], q) — 상의 생성벡터
            st = np.vstack([acc, cols]) % p
            nrk = len(rref_rows(st.copy(), p)[0])
            if nrk > rk:
                acc = rref_rows(st.copy(), p)[0]
                rk = nrk
                picked.append((j, phi))
                mult[j] += 1
            if rk >= q:
                break
    dtot = sum(dimP[j] for (j, _f) in picked)
    Mmap = np.concatenate([f for (_j, f) in picked], axis=1) % p
    act = {}
    for g in gens:
        Z = np.zeros((dtot, dtot), dtype=np.int64)
        off = 0
        for (j, _f) in picked:
            Bm = PIM[j][g] % p
            Z[off:off + len(Bm), off:off + len(Bm)] = Bm
            off += len(Bm)
        act[g] = Z
    ker = nullspace(Mmap, p)
    actO, _b = submodule_action(act, gens, ker, p)
    return actO, len(ker), mult, dtot, len(image_basis(Mmap, p))


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


def minimal_generators_filtered(names, pl, info, arrows, maxd, p):
    """★**비균질 관계식까지** 다루는 최소 생성원 — kQ/J^maxd 안에서 I 와 J·I + I·J 를 직접.

    균질 제시가 존재하지 않는 블록(자기고리 등)에서는 차수별 커널만으로는 I 를 못 만든다.
    rad^{maxd−1} A = 0 이면 J^{maxd−1} ⊆ I 이고 J^maxd ⊆ J·I 이므로 **절단이 정확**하다.
    또 J·I = span{α·y : α 화살, y ∈ I}(I 가 양쪽 이데알이므로) — 화살만으로 충분.
    ★생성원 **개수는 리프트 선택과 무관한 불변량**(= Σ dim Ext²)."""
    keys = [k for n in range(maxd) for k in pl[n]]
    grp = {}
    for k in keys:
        s, t, _M = info[k]
        grp.setdefault((s, t), []).append(k)
    idx = {st: {k: i for i, k in enumerate(kk)} for st, kk in grp.items()}
    K = {}
    for st, kk in grp.items():
        M = np.array([info[k][2].reshape(-1) % p for k in kk], dtype=np.int64)
        K[st] = [c % p for c in nullspace(M.T % p, p)]
    JK = {st: [] for st in grp}
    for st, kk in grp.items():
        s, t = st
        for c in K[st]:
            terms = [kk[i] for i in range(len(kk)) if c[i]]
            for ai, a in enumerate(arrows):
                cand = []
                if a[0] == t:                       # α 를 뒤에 — α∘x
                    cand.append(((s, a[1]),
                                 [(pt + (ai,), ps) for (pt, ps) in terms]))
                if a[1] == s:                       # α 를 앞에 — x∘α
                    cand.append(((a[0], t),
                                 [((ai,) + pt, a[0]) for (pt, _ps) in terms]))
                for st2, newk in cand:
                    if st2 not in grp:
                        continue
                    v = np.zeros(len(grp[st2]), dtype=np.int64)
                    hit = False
                    for nk in newk:
                        if len(nk[0]) < maxd:       # J^maxd 는 0 (절단)
                            v[idx[st2][nk]] ^= 1
                            hit = True
                    if hit:
                        JK[st2].append(v)
    counts, reps = {}, {}
    for st, kk in grp.items():
        rows = (np.array(JK[st], dtype=np.int64) if JK[st]
                else np.zeros((0, len(kk)), dtype=np.int64))
        Cur = rows.copy()
        rk = len(rref_rows(Cur.copy(), p)[0]) if len(Cur) else 0
        picked = []
        for c in K[st]:
            st_ = np.vstack([Cur, c[None, :]]) if len(Cur) else c[None, :]
            nrk = len(rref_rows(st_.copy(), p)[0])
            if nrk > rk:
                picked.append(sorted(tuple(kk[i][0]) for i in range(len(kk)) if c[i]))
                Cur, rk = st_, nrk
        if picked:
            counts[st] = len(picked)
            reps[st] = picked
    return counts, reps, {st: len(v) for st, v in K.items()}


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
            homs.extend(hom_space_fast(PIM[k], aS, d[k], dS, gens_g, p))
        RADP[k] = nullspace(np.concatenate(homs, axis=0) % p, p)
    HOM = {(i, j): hom_space_fast(PIM[i], PIM[j], d[i], d[j], gens_g, p)
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
    # ★리프트와 무관한 불변 경로 — 비균질 관계식까지 포함한 최소 생성원
    fcnt, freps, _kd = minimal_generators_filtered(names, pl, info, arrows,
                                                   maxd, p)
    e2rel = [[fcnt.get((names[j], names[i]), 0) for j in range(len(names))]
             for i in range(len(names))]
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
        hd = [len(hom_space_fast(actO, aS, dO, dS, gens_g, p))
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
        "homogeneous_certified": (mode == "homogeneous-certified"),
        "filtered_relations": {f"{k[0]}->{k[1]}": v for k, v in sorted(freps.items())},
        "n_relations_filtered": sum(fcnt.values()),
        "ext2_from_relations": e2rel,
        "ext2_matrix": [ext2[k] for k in names],
        "ext2_total": sum(sum(ext2[k]) for k in names),
        "omega2": om2,
        "arrow_legend": [[t, arrows[t][0], arrows[t][1]]
                         for t in range(len(arrows))],
    }, arrows, RADP


# ══════════════════════════════════════════════════════════════════════════
def a7_pims(mul7, id7, ord7, A7G, simples7, N7, syl2_7, want):
    """지수 크기 사영 운반자(|H| 홀수)에서 원하는 P(S) 들을 뽑는다 —
    F₂₁(120) → P(1̂)·P(4̂)·P(4̄̂) · Syl₃(280) → P(6̂)·P(14̂) · C₇(360) → P(20̂)."""
    carriers = {"F21": ([(1, 2, 3, 4, 5, 6, 0), (0, 2, 4, 6, 1, 3, 5)], 120),
                "Syl3": ([(1, 2, 0, 3, 4, 5, 6), (0, 1, 2, 4, 5, 3, 6)], 280),
                "C7": ([(1, 2, 3, 4, 5, 6, 0)], 360)}
    PIM, info = {}, {}
    for cn, (hg, idxn) in carriers.items():
        if all(k in PIM for k in want):
            break
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
            if dd not in want.values():
                continue
            actY, _ = submodule_action(actX, A7G, B, 2)
            hd = tuple(len(hom_space(actY, aS, dd, dS, A7G, 2))
                       for _, aS, dS in simples7)
            nm = next((k for t, k in enumerate(N7)
                       if hd == tuple(1 if j == t else 0 for j in range(len(N7)))),
                      None)
            if nm in want and nm not in PIM and want[nm] == dd:
                PIM[nm] = {g: actY[g] % 2 for g in A7G}
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
    R["F_A6_filtered_reproduces"] = (
        B6["n_relations_filtered"] == B6["n_relations"] == 3
        and B6["ext2_from_relations"] == B6["ext2_matrix"])
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

        prn = build_a7_principal_gens(A7G)
        raw7 = {"1": ([np.eye(1, dtype=np.int64)] * 2, 1), "4": (g4, 4),
                "4b": (g4b, 4), "6": ([_w2(m) for m in g4], 6),
                "14": prn["14"], "20": prn["20"]}
        ALL7 = ["1", "4", "4b", "6", "14", "20"]
        N7 = ["4", "4b", "6"]
        S7 = {k: extend_action(A7G, mul7, id7, gm, 2, ord7)
              for k, (gm, _d) in raw7.items()}
        D7 = {k: dd for k, (_gm, dd) in raw7.items()}
        simALL = [(k, S7[k], D7[k]) for k in ALL7]
        sim7 = [(k, S7[k], D7[k]) for k in N7]
        syl2_7 = subgroup([(1, 2, 3, 0, 5, 4, 6), (2, 1, 0, 3, 5, 4, 6)],
                          mul7, id7)
        R["A_A7_syl2_order8"] = (len(syl2_7) == 8)
        DIMP7 = {"1": 72, "4": 24, "4b": 24, "6": 40, "14": 64, "20": 56}
        PIMA, cinfo = a7_pims(mul7, id7, ord7, A7G, simALL, ALL7, syl2_7, DIMP7)
        R["A_A7_all_six_pims"] = (sorted(PIMA) == sorted(ALL7))
        PIM7 = {k: PIMA[k] for k in N7}
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
        # ★리프트-무관 경로가 균질 결과를 그대로 재현(기계 자체검증)
        R["D_A7_filtered_reproduces"] = (
            B7["n_relations_filtered"] == B7["n_relations"] == 3
            and B7["ext2_from_relations"] == B7["ext2_matrix"])
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

        # ── H. ★A₇ p=2 **주블록** — 자기고리를 품은 첫 제시 ──────────────
        NPr = ["1", "14", "20"]
        simPr = [(k, S7[k], D7[k]) for k in NPr]
        PIMPr = {k: PIMA[k] for k in NPr}
        R["H_A7pr_pim_dims"] = ([len(PIMPr[k][A7G[0]]) for k in NPr]
                                == [72, 64, 56])
        CPr = [[4, 2, 2], [2, 3, 1], [2, 1, 2]]
        BP, arrPr, RADPr = block_presentation(NPr, A7G, PIMPr, simPr, CPr, 5, 2,
                                              lift_cap=32)
        R["H_A7pr_cartan_via_hom"] = (BP["cartan_via_hom"] == CPr)
        R["H_A7pr_dim_basic_19"] = (BP["dim_basic_algebra"] == 19
                                    == BP["cartan_sum"])
        R["H_A7pr_rad_powers"] = (BP["rad_power_dims"] == [16, 11, 7, 3, 0])
        R["H_A7pr_graded_matches_loewy"] = (BP["graded_dims"] == [3, 5, 4, 4, 3])
        R["H_A7pr_block_dim_2088_untouched"] = (
            sum(BP["dim_P"][t] * D7[NPr[t]] for t in range(3)) == 2088)
        # ★화살 5개 — 선행 Ext¹ 퀴버(자기고리 포함)와 일치
        R["H_A7pr_five_arrows_with_selfloop"] = (
            BP["n_arrows"] == 5
            and sorted(tuple(b) for b in BP["arrow_blocks"])
            == [("1", "14"), ("1", "20"), ("14", "1"), ("14", "14"), ("20", "1")])
        R["H_A7pr_surjective"] = (BP["image_dim_kQ_to_A"] == 19)
        # ★★균질 제시가 **존재하지 않는다** — 리프트 32 전수 확인(예측 반증)
        R["H_A7pr_no_homogeneous_presentation"] = (
            not BP["homogeneous_certified"]
            and BP["lift_choices_total"] == 32 and BP["lift_tried"] == 32
            and BP["dim_kQ_over_I"] == 20)
        R["H_A7pr_six_relations"] = (BP["n_relations_filtered"] == 6)
        R["H_A7pr_ext2"] = (BP["ext2_matrix"]
                            == [[1, 1, 0], [1, 2, 0], [0, 0, 1]])
        R["H_A7pr_two_routes_agree"] = (BP["ext2_from_relations"]
                                        == BP["ext2_matrix"])
        R["H_A7pr_ext2_equals_relations"] = (
            BP["ext2_total"] == BP["n_relations_filtered"] == 6)
        R["H_A7pr_omega2_covers_rad"] = all(
            v["image_dim"] == v["rad_P_dim"] for v in BP["omega2"].values())
        # ★첫 다중도-2 Ext² 성분이 **자기고리를 가진 14̂** 자리
        R["H_A7pr_multiplicity2_at_selfloop"] = (
            BP["ext2_matrix"][NPr.index("14")][NPr.index("14")] == 2
            and max(max(r) for r in B7["ext2_matrix"]) == 1
            and max(max(r) for r in B6["ext2_matrix"]) == 1)
        # ★비균질의 정체: 자기고리 제곱 γ² 가 0 이 아니라 길이-4 경로와 같다
        selfl = next(t for t, a in enumerate(arrPr) if a[0] == a[1] == "14")
        rel1414 = BP["filtered_relations"].get("14->14", [])
        R["H_A7pr_selfloop_square_not_zero"] = any(
            [selfl, selfl] in [list(x) for x in rel] and len(rel) == 2
            for rel in rel1414)
        out["H_A7_p2_principal"] = {
            "presentation": BP,
            "note": ("★A₇ p=2 **주블록**(1̂·14̂·20̂ · dim P 72·64·56 · ΣC=19) — "
                     "**자기고리 Ext¹(14̂,14̂)=1 을 가진 첫 제시** · "
                     "★★**균질 제시가 존재하지 않는다**(리프트 32 전수: 균질 이데알은 "
                     "dim kQ/I = 20 ≠ 19) ⟹ **비균질 관계식이 강제**된다 · "
                     "정체는 **γ² ≠ 0** — 자기고리의 제곱이 길이-4 경로와 같다"),
            "prediction_corrected": ("★설계 시 γ²=0 을 포함한 **차수 2 영관계 5개**를 "
                                     "예측했으나 **반증** — 실제로는 영관계 4개이고 "
                                     "γ² 는 길이-4 경로와 같은 **비균질 관계식**"),
        }

        # ── H′. 주블록 Ext² 의 H¹ 부분 독립 확인(규모 정직 경계) ─────────
        e2p, cert_p, scope = {}, True, {}
        for i in NPr:
            actR, br = submodule_action(PIMPr[i], A7G, RADPr[i], 2)
            dR = len(br)
            full = None
            row, cr = [], []
            for j in NPr:
                m = dR * D7[j]
                if m > 128:                     # 규모 밖 — 정직 유보
                    row.append(None)
                    cr.append(None)
                    continue
                if full is None:
                    full = extend_action(A7G, mul7, id7,
                                         [actR[g] for g in A7G], 2, ord7)
                e, cert, _det = ext1_pair_lean(A7G, mul7, id7, ord7bfs, par7,
                                               full, S7[j], dR, D7[j], 2, 60)
                row.append(e)
                cr.append(bool(cert))
            e2p[i] = {"dim_Omega": dR, "ext2_row": row, "certified": cr}
            cert_p = cert_p and all(c for c in cr if c is not None)
        R["Hp_A7pr_h1_column_certified"] = cert_p
        R["Hp_A7pr_h1_column_agrees"] = all(
            e2p[NPr[i]]["ext2_row"][j] in (None, BP["ext2_matrix"][i][j])
            for i in range(3) for j in range(3))
        R["Hp_A7pr_h1_column_covered"] = (
            [e2p[k]["ext2_row"][0] for k in NPr] == [1, 1, 0])
        out["Hp_A7_principal_ext2_via_H1"] = {
            "rows": e2p,
            "scope": ("★**부분 확인**: m = dim ΩS_i · dim S_j 가 최대 1420 이라 "
                      "(비주블록은 204) `ext1_pair_lean` 의 m×m 캐시가 규모 밖 — "
                      "**1̂ 열(m = 71·50·36)만** 독립 확인하고 나머지는 **정직 유보**. "
                      "총 개수는 head(Ω²) 와 리프트-무관 최소생성 두 경로가 이미 대조"),
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

        # ── J. ★A₆ p=3 주블록 over 𝔽₃ — ★★분해체가 아니다(species) ──────
        def _perm3(g, n):
            M = np.zeros((n, n), dtype=np.int64)
            for j in range(n):
                M[g[j], j] = 1
            return M % 3

        SZ = np.array([[1 if i == 0 else (-1 if i == j else 0) for i in range(6)]
                       for j in range(1, 6)], dtype=np.int64) % 3
        _b5, _p5 = rref_rows(SZ.copy(), 3)
        act5 = {g: restrict(_perm3(g, 6), _b5, _p5, 3) for g in A6G}
        act4d, _d4 = quotient_action(act5, A6G,
                                     np.ones((1, 5), dtype=np.int64), 5, 3)

        def _wedge3(M, n):
            pr = list(itertools.combinations(range(n), 2))
            ix = {t: i for i, t in enumerate(pr)}
            O = np.zeros((len(pr), len(pr)), dtype=np.int64)
            for jc, (a, b) in enumerate(pr):
                for i in range(n):
                    for j in range(n):
                        if i == j or M[i][a] * M[j][b] % 3 == 0:
                            continue
                        O[ix[(min(i, j), max(i, j))]][jc] += (
                            (1 if i < j else -1) * M[i][a] * M[j][b])
            return O % 3

        raw3 = {"1": [np.eye(1, dtype=np.int64)] * 3,
                "4": [act4d[g] for g in A6G],
                "6t": [_wedge3(act4d[g], 4) for g in A6G]}
        N33 = ["1", "4", "6t"]
        S33 = {k: extend_action(A6G, mul6, id6, v_, 3, ord6)
               for k, v_ in raw3.items()}
        D33 = {"1": 1, "4": 4, "6t": 6}
        sim33 = [(k, S33[k], D33[k]) for k in N33]
        endF3 = {k: len(hom_space_iter(S33[k], S33[k], D33[k], D33[k], A6G, 3))
                 for k in N33}
        # ★★End(6̃) 의 𝔽₃-차원이 2 ⟹ GF(9) ⟹ 𝔽₃ 는 분해체가 아니다
        R["J_A6p3_end_dims"] = (endF3 == {"1": 1, "4": 1, "6t": 2})
        DIMP3 = {"1": 27, "4": 36, "6t": 36}
        # ★블록 차원: Σ dim P·(dim S / dim End S) = 279
        R["J_A6p3_block_279"] = (
            sum(DIMP3[k] * D33[k] // endF3[k] for k in N33) == 279)
        CAND3 = {"Syl2": [(1, 0, 3, 2, 4, 5), (2, 3, 0, 1, 4, 5),
                          (0, 1, 3, 2, 5, 4)],
                 "C5": [(1, 2, 3, 4, 0, 5)],
                 "V4": [(1, 0, 3, 2, 4, 5), (2, 3, 0, 1, 4, 5)]}
        PIM3, carr3 = {}, {}
        for cn, hg in CAND3.items():
            if all(k in PIM3 for k in DIMP3):
                break
            Hl = subgroup(hg, mul6, id6)
            n_, reps_, perms_, mats_ = coset_data(ord6, mul6, id6, A6G, Hl)
            actX = extend_action(A6G, mul6, id6, mats_, 3, ord6)
            alg = hecke_endos_p(n_, perms_, Hl, reps_, 3)
            rng3 = random.Random(7)                       # 결정론 시드

            def _rnd3(alg=alg, rng3=rng3, n_=n_):
                M = np.zeros((n_, n_), dtype=np.int64)
                for A_ in rng3.sample(alg, max(2, len(alg) // 3)):
                    M = (M + rng3.randrange(1, 3) * A_) % 3
                return M

            ps = []
            decompose_regular(np.eye(n_, dtype=np.int64),
                              np.eye(n_, dtype=np.int64), _rnd3, 3, rng3, ps)
            carr3[cn] = {"order": len(Hl), "index": n_, "hecke_dim": len(alg),
                         "projective": fixed_dim(actX, syl3_6, n_, 3) == n_ // 9,
                         "parts": sorted(len(b) for b in ps),
                         "frobenius_m_S": {
                             k: fixed_dim(S33[k], Hl, D33[k], 3) // endF3[k]
                             for k in N33}}
            for B in sorted(ps, key=len):
                dd = len(B)
                if dd not in DIMP3.values():
                    continue
                actY, _ = submodule_action(actX, A6G, B, 3)
                hd = tuple(len(hom_space_iter(actY, aS, dd, dS, A6G, 3))
                           for _n, aS, dS in sim33)
                nm = next((k for t, k in enumerate(N33)
                           if hd == tuple(endF3[k] if j == t else 0
                                          for j in range(3))), None)
                if nm in DIMP3 and nm not in PIM3 and DIMP3[nm] == dd:
                    PIM3[nm] = {g: actY[g] % 3 for g in A6G}
        R["J_A6p3_all_three_pims"] = (sorted(PIM3) == sorted(DIMP3))
        R["J_A6p3_carriers_projective"] = all(v["projective"]
                                              for v in carr3.values())
        lo3 = {k: loewy_series(PIM3[k], DIMP3[k], A6G, sim33, 3) for k in N33}
        HOM3 = {(i, j): len(hom_space_iter(PIM3[i], PIM3[j], DIMP3[i],
                                           DIMP3[j], A6G, 3))
                for i in N33 for j in N33}
        cart3 = [[HOM3[(i, j)] for j in N33] for i in N33]
        # ★기본대수 차원 = 분해체 위 Σ C = 36 (A^{𝔽₃} ⊗ GF(9) ≅ A^{GF(9)})
        R["J_A6p3_dim_basic_36"] = (sum(HOM3.values()) == 36)
        R["J_A6p3_cartan_via_hom"] = (cart3 == [[5, 4, 2], [4, 5, 4], [2, 4, 6]])
        R["J_A6p3_loewy_length_5"] = all(len(v) == 5 for v in lo3.values())
        R["J_A6p3_palindromic"] = all(list(v) == list(v)[::-1]
                                      for v in lo3.values())
        R["J_A6p3_layers_sum_to_cartan"] = all(
            [sum(l[i] for l in lo3[k]) for i in range(3)]
            == [cart3[i][N33.index(k)] for i in range(3)] for k in N33)
        # ★화살 다중도 비대칭 = species 서명: 4→6̃ 은 2 인데 6̃→4 은 1
        arr3 = {k: [lo3[k][1][i] // endF3[N33[i]] for i in range(3)] for k in N33}
        R["J_A6p3_arrow_asymmetry"] = (arr3["6t"][1] == 2 and arr3["4"][2] == 1)
        R["J_A6p3_double_arrow"] = (arr3["1"][1] == 2 and arr3["4"][0] == 2)
        # ★Ext² — 리프트-무관 탐욕 사영 덮개(Ω² = ker(P₁ ↠ rad P_i))
        ext2_3, om3 = {}, {}
        for k in N33:
            radb = nullspace(np.concatenate(
                [h for (_n, aS, dS) in sim33
                 for h in hom_space_iter(PIM3[k], aS, DIMP3[k], dS, A6G, 3)],
                axis=0) % 3, 3)
            actR, _br = submodule_action(PIM3[k], A6G, radb, 3)
            d1_ = len(radb)
            aO, dO, mult1, dt1, im1 = greedy_cover(actR, d1_, PIM3, DIMP3, N33,
                                                   sim33, A6G, 3)
            hd = [len(hom_space_iter(aO, aS, dO, dS, A6G, 3)) // endF3[nm]
                  for (nm, aS, dS) in sim33]
            ext2_3[k] = hd
            om3[k] = {"rad_dim": d1_, "P1_dim": dt1, "image_dim": im1,
                      "Omega2_dim": dO, "P1_mult": mult1, "head": hd}
        R["J_A6p3_cover_exact"] = all(v["image_dim"] == v["rad_dim"]
                                      for v in om3.values())
        # ★Ext² 에서도 같은 비대칭(1̂→6̃ 은 1, 6̃→1̂ 은 2) — species 서명이 2층에도
        R["J_A6p3_ext2_asymmetric"] = (ext2_3["1"][2] == 1
                                       and ext2_3["6t"][0] == 2)
        R["J_A6p3_ext2_total_8"] = (
            sum(sum(v) for v in ext2_3.values()) == 8)
        out["J_A6_p3_over_F3"] = {
            "carriers": carr3, "end_dims": endF3,
            "cartan_via_hom": cart3, "dim_basic_algebra": sum(HOM3.values()),
            "loewy_layers": {k: [list(x) for x in lo3[k]] for k in N33},
            "arrow_multiplicities": arr3,
            "ext2_matrix": [ext2_3[k] for k in N33],
            "omega2": om3,
            "note": ("★★**𝔽₃ 는 A₆ p=3 주블록의 분해체가 아니다** — 3·3′ 이 융합해 "
                     "**6̃ = Λ²(4)** 하나가 되고 **End(6̃) 의 𝔽₃-차원 = 2 ⟹ GF(9)** · "
                     "따라서 화살이 **GF(9)-이중가군**이라 `B ≅ kQ/I`(퀴버+관계식) 틀이 "
                     "그대로 적용되지 않는다 — **modulated quiver(species)** 가 필요. "
                     "★서명: **4→6̃ 다중도 2 vs 6̃→4 다중도 1**(분해체 위라면 대칭)"),
            "loewy_note": ("★**A₆ p=3 Loewy 급수 최초 산출** — 전부 LL=5·회문 · "
                           "층 다중도는 𝔽₃-Hom 차원(6̃ 성분은 실제 다중도의 2배)"),
        }

        # ── K. ★GF(9) 로 올라간다 — J(=√−1)를 추가 생성원으로 실현화 ──────
        j2 = np.array([[0, -1], [1, 0]], dtype=np.int64) % 3
        JKEY = "__J__"
        G9 = A6G + [JKEY]

        def _tensor9(act, d):
            a = {g: np.kron(act[g] % 3, np.eye(2, dtype=np.int64)) % 3
                 for g in A6G}
            a[JKEY] = np.kron(np.eye(d, dtype=np.int64), j2) % 3
            return a, 2 * d

        # 6̃ 위의 GF(9) 구조 J₆ — End 안에서 J² = −I 를 만족하는 원소
        def _find_j(basis, n):
            for c in itertools.product(range(3), repeat=len(basis)):
                M = np.zeros((n, n), dtype=np.int64)
                for t, ct in enumerate(c):
                    if ct:
                        M = (M + ct * basis[t]) % 3
                if ((M @ M) % 3 == (-np.eye(n, dtype=np.int64)) % 3).all():
                    return M % 3
            return None

        J6 = _find_j(hom_space_iter(S33["6t"], S33["6t"], 6, 6, A6G, 3), 6)
        JP6 = _find_j(hom_space_iter(PIM3["6t"], PIM3["6t"], 36, 36, A6G, 3), 36)
        R["K_gf9_structure_found"] = (J6 is not None and JP6 is not None)
        S9, D9 = {}, {}
        for nm in ("1", "4"):
            S9[nm], D9[nm] = _tensor9(S33[nm], D33[nm])
        S9["3"] = dict(S33["6t"], **{JKEY: J6})
        S9["3b"] = dict(S33["6t"], **{JKEY: (-J6) % 3})
        D9["3"] = D9["3b"] = 6
        N9 = ["1", "4", "3", "3b"]
        sim9 = [(k, S9[k], D9[k]) for k in N9]
        P9, DP9 = {}, {}
        for nm in ("1", "4"):
            P9[nm], DP9[nm] = _tensor9(PIM3[nm], DIMP3[nm])
        # ★JP6 의 부호는 단순가군 쪽 J₆ 와 독립으로 정해지므로 **head 로 정렬**한다
        _h3 = [len(hom_space_iter(dict(PIM3["6t"], **{JKEY: JP6}), aS, 36, dS,
                                  G9, 3)) for (_n, aS, dS) in
               [("3", S9["3"], 6), ("3b", S9["3b"], 6)]]
        if _h3[0] == 0:
            JP6 = (-JP6) % 3
        P9["3"] = dict(PIM3["6t"], **{JKEY: JP6})
        P9["3b"] = dict(PIM3["6t"], **{JKEY: (-JP6) % 3})
        DP9["3"] = DP9["3b"] = 36
        end9 = {k: len(hom_space_iter(S9[k], S9[k], D9[k], D9[k], G9, 3))
                for k in N9}
        # 절대기약: End_{GF(9)} = GF(9) ⟹ 𝔽₃-차원 2
        R["K_all_absolutely_irreducible"] = all(v == 2 for v in end9.values())
        R["K_3_and_3b_not_isomorphic"] = (
            len(hom_space_iter(S9["3"], S9["3b"], 6, 6, G9, 3)) == 0)
        R["K_pim_dims_over_gf9"] = ([DP9[k] // 2 for k in N9] == [27, 36, 18, 18])
        lo9 = {k: [tuple(x // 2 for x in lay)
                   for lay in loewy_series(P9[k], DP9[k], G9, sim9, 3)]
               for k in N9}
        cart9 = [[sum(l[i] for l in lo9[k]) for k in N9] for i in range(4)]
        R["K_cartan_recovered"] = (
            cart9 == [[5, 4, 1, 1], [4, 5, 2, 2], [1, 2, 2, 1], [1, 2, 1, 2]])
        R["K_sum_cartan_36"] = (sum(sum(r) for r in cart9) == 36)
        R["K_loewy_length_5"] = all(len(v) == 5 for v in lo9.values())
        R["K_block_dim_279"] = (
            sum((DP9[N9[t]] // 2) * (D9[N9[t]] // 2) for t in range(4)) == 279)
        arr9 = {k: list(lo9[k][1]) for k in N9}
        R["K_eight_arrows"] = (sum(sum(v) for v in arr9.values()) == 8)
        # ★이중화살 1̂↔4 재현 · 3·3′ 은 4 하고만 연결 · Frobenius σ 대칭
        R["K_double_arrow_1_4"] = (arr9["1"][1] == 2 and arr9["4"][0] == 2)
        R["K_3_only_meets_4"] = (arr9["3"] == [0, 1, 0, 0]
                                 and arr9["3b"] == [0, 1, 0, 0]
                                 and arr9["4"][2] == 1 and arr9["4"][3] == 1)
        R["K_frobenius_sigma_symmetry"] = (
            [list(l) for l in lo9["3"]]
            == [[l[t] for t in (0, 1, 3, 2)] for l in lo9["3b"]])
        out["K_A6_p3_over_GF9"] = {
            "method": ("★**J(=√−1)를 추가 생성원**으로 넣어 GF(9)-가군을 (𝔽₃-가군, J) 로 "
                       "실현화 — Hom_{GF(9)} = J 와 가환하는 Hom_{𝔽₃} 이므로 "
                       "**기존 파이프라인이 그대로 재사용**되고 모든 차원이 2배로 나온다. "
                       "1̂₉·4₉ = ⊗GF(9)(J = I⊗j₂) · 3·3′ = **같은 6̃ 에 J₆ 와 −J₆**"
                       "(J₆ ∈ End 는 J²=−I 로 탐색)"),
            "pim_dims_gf9": {k: DP9[k] // 2 for k in N9},
            "cartan": cart9,
            "loewy_layers": {k: [list(x) for x in lo9[k]] for k in N9},
            "arrow_multiplicities": arr9,
            "note": ("★**분해체 위 Cartan·Loewy·퀴버(화살 8개·이중화살 1̂↔4) 완전 재유도** — "
                     "3·3′ 은 **4 하고만** 연결되고 Frobenius σ 로 서로 교환된다"),
            "not_yet": ("★**관계식(Ext²)은 정직 유보** — GF(9) PIM 사이의 Hom 은 "
                        "dim_{𝔽₃} 최대 72×72 = 5184 계의 GF(3) 커널 16 쌍이라 규모 밖"
                        "(𝔽₃ 축의 Ext² 는 산출·GF(9) 분해는 미확정)"),
        }

        # ── I. ★3 블록 종합 — 자기고리가 제시를 질적으로 바꾼다 ──────────
        R["I_selfloop_only_in_principal"] = (
            BP["n_arrows"] == 5 and B7["n_arrows"] == B6["n_arrows"] == 4
            and any(b[0] == b[1] for b in BP["arrow_blocks"])
            and not any(b[0] == b[1] for b in B7["arrow_blocks"])
            and not any(b[0] == b[1] for b in B6["arrow_blocks"]))
        R["I_homogeneous_iff_no_selfloop"] = (
            B6["homogeneous_certified"] and B7["homogeneous_certified"]
            and not BP["homogeneous_certified"])
        R["I_relation_counts"] = (
            [B7["n_relations_filtered"], B6["n_relations_filtered"],
             BP["n_relations_filtered"]] == [3, 3, 6])
        R["I_dims"] = ([B7["dim_basic_algebra"], B6["dim_basic_algebra"],
                        BP["dim_basic_algebra"]] == [18, 34, 19])
        out["I_three_block_synthesis"] = {
            "table": {
                "A7_p2_nonprincipal": {"vertices": 3, "arrows": 4,
                                       "self_loop": False, "dim_A": 18,
                                       "relations": B7["n_relations_filtered"],
                                       "homogeneous": True,
                                       "ext2": B7["ext2_matrix"]},
                "A6_p2_principal": {"vertices": 3, "arrows": 4,
                                    "self_loop": False, "dim_A": 34,
                                    "relations": B6["n_relations_filtered"],
                                    "homogeneous": True,
                                    "ext2": B6["ext2_matrix"]},
                "A7_p2_principal": {"vertices": 3, "arrows": 5,
                                    "self_loop": True, "dim_A": 19,
                                    "relations": BP["n_relations_filtered"],
                                    "homogeneous": False,
                                    "ext2": BP["ext2_matrix"]}},
            "headline": ("★★**자기고리가 있는 블록에서만 균질 제시가 깨진다**(3 블록 실측) — "
                         "자기고리 없는 두 블록은 리프트를 고르면 균질 제시가 존재하는데, "
                         "A₇ 주블록은 **리프트 32 전수에서 전부 실패**하고 **γ² = (길이-4 경로)** "
                         "라는 비균질 관계식이 강제된다 · ★**Ext² 에 처음으로 다중도 2**가 "
                         "나타나고 그 자리가 정확히 **자기고리 정점 14̂**"),
            "caveat": ("3 블록 관측 · **일반 정리 주장 아님**(자기고리 ⟹ 비균질의 기전은 "
                       "무주장)"),
        }

        # ── L. ★4 블록 종합 — 제시를 막는 두 가지 서로 다른 이유 ──────────
        R["L_four_blocks"] = (
            [B7["dim_basic_algebra"], B6["dim_basic_algebra"],
             BP["dim_basic_algebra"], sum(HOM3.values())] == [18, 34, 19, 36])
        R["L_two_obstructions"] = (
            B7["homogeneous_certified"] and B6["homogeneous_certified"]
            and not BP["homogeneous_certified"]
            and endF3["6t"] == 2)
        out["L_four_block_synthesis"] = {
            "table": {
                "A7_p2_nonprincipal": {"field": "𝔽₂(분해체)", "vertices": 3,
                                       "arrows": 4, "dim_A": 18,
                                       "presentation": "kQ/I 완전(균질)"},
                "A6_p2_principal": {"field": "𝔽₂(분해체)", "vertices": 3,
                                    "arrows": 4, "dim_A": 34,
                                    "presentation": "kQ/I 완전(균질)"},
                "A7_p2_principal": {"field": "𝔽₂(분해체)", "vertices": 3,
                                    "arrows": 5, "dim_A": 19,
                                    "presentation": "kQ/I 완전(★비균질 강제)"},
                "A6_p3_principal": {"field": "★𝔽₃ 는 분해체 아님 / GF(9) 위 4 정점",
                                    "vertices": "3(𝔽₃) → 4(GF(9))",
                                    "arrows": "★8(이중화살 포함)", "dim_A": 36,
                                    "presentation": "★퀴버까지 · 관계식 정직 유보"}},
            "headline": ("★★**제시를 막는 이유가 두 종류**임이 드러났다 — "
                         "①**자기고리**(A₇ 주블록): 분해체인데도 **균질 제시가 없다**"
                         "(γ² = 길이-4 경로) · ②**비분해체**(A₆ p=3): 𝔽₃ 위에서는 "
                         "**퀴버 자체가 성립하지 않고**(End(6̃)=GF(9) ⟹ species) "
                         "GF(9) 로 올라가야 4 정점 8 화살의 퀴버가 나온다. "
                         "★두 장애는 **독립**이다(A₇ 주블록은 분해체·A₆ p=3 은 자기고리 없음)"),
            "caveat": "4 블록 관측 · 일반 정리 무주장",
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
        "delivered": ("★A₇ p=2 비주·A₆ p=2 주·★★A₇ p=2 **주블록** — **세 블록의 완전 제시** · "
                      "Cartan 를 Hom 차원으로 제4 재유도 · graded = Loewy 층 게이트 · "
                      "★관계식 명시(비주·A₆ 는 3개 = 영관계 2 + 가환 1 / 주블록은 6개) · "
                      "dim kQ/I = Σ C 인증(균질 두 블록) · ★Ext² 두 독립 경로 일치 · "
                      "★★퀴버 동형·대수 비동형 실례 · ★★자기고리 블록에서 **균질 제시 부재**"
                      "(리프트 32 전수)와 **γ² ≠ 0** 실측"),
        "not_yet": ("A₆ p=3(이중화살·GF(9) 융합) · 주블록 Ext² 의 **H¹ 전 성분**"
                    "(m ≤ 1420 규모 — 1̂ 열만 확인) · 관계식의 **기저 무의존 표현**"),
        "not_claimed": ("봉인 게이트 · 외부 분류표의 이름(dihedral/quaternion type 등) · "
                        "대수들의 유도동등성(derived equivalence) · "
                        "\"자기고리 ⟹ 비균질\"의 **기전**(3 블록 관측일 뿐)"),
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
        for nm, Bx in (("A₇ p=2 비주", B7), ("A₆ p=2 주", B6), ("A₇ p=2 주", BP)):
            print(f"  ★{nm}: dim A = {Bx['dim_basic_algebra']} = ΣC · "
                  f"화살 {Bx['n_arrows']} · graded {Bx['graded_dims']} · "
                  f"균질 {Bx['homogeneous_certified']}", flush=True)
            print(f"    관계식 {Bx['n_relations_filtered']}개(리프트-무관) · "
                  f"dim kQ/I = {Bx['dim_kQ_over_I']} · Ext² {Bx['ext2_matrix']}",
                  flush=True)
            print(f"    화살 {Bx['arrow_legend']} · "
                  f"관계식 {Bx['filtered_relations']}", flush=True)
        print("  ★★퀴버 동형(3정점 별·화살 4)인데 dim 34 vs 18 — 가환관계 차수 8 vs 4",
              flush=True)
        print("  ★★A₇ 주블록: 리프트 32 전수에서 **균질 제시 없음**(20≠19) — "
              "γ² = 길이-4 경로(비균질 강제)·Ext² 에 첫 다중도 2(자기고리 14̂)", flush=True)
        print("  ★Ext² 두 독립 경로 일치: head(Ω²) · 리프트-무관 최소생성"
              "(비주블록은 H¹ 까지 3경로)", flush=True)
        print("  → .pgf/proofs/QUIVER-RELATIONS.json", flush=True)
        print(f"  (elapsed {time.time() - t0:.1f}s)", flush=True)
    if not ok:
        print("  ✗ 실패 체크:", [k for k, v in R.items() if not v], flush=True)
    print(f"quiver_relations_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
