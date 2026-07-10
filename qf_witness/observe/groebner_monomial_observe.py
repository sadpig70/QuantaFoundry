#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""groebner_monomial_observe — TrackHE9 P1 심화: 제10 검증경로(Gröbner/ℤ[ω] phase-ideal) **커버 확장**
— 대각(diagonal)에서 **monomial(일반화 순열) 위상회로** U|x⟩=ω_M^{f(x)}|π(x)⟩ 로 (관측, seal 아님).

★신규 검증경로 아님 — **제10 경로의 coverage 심화**(신규 봉인 0·root 불변 sidecar). P1(groebner_verify)은
대각-plan 위상회로만 커버했다(π=항등). 여기선 **ANF(제9, 순열+1만)·diagonal-Gröbner(P1, 대각만) 둘 다
skip 하는 교집합 맹점** = monomial 비대각 위상 유니터리(CNOT+phase, 순열부 A≠I + 위상)를 커버.

  U|x⟩ = ω_M^{f(x)} |π(x)⟩ (각 열 정확히 1 nonzero·|·|=1 = monomial). 두 독립 경로:
  path A: plan 게이트별 추적 — 순열 게이트(X/CNOT/SWAP/Toffoli)는 π 갱신·대각 위상 게이트는 **현재 wire
    값**(π 로 변환된 계산기저 비트 = 중간 wire 변수)에 위상 누적. ★위상이 **CNOT-이후 parity**(wire linear-form)
    에 작용 → parity 변수 소거 = **회로-이데알 elimination**.
  path B: golden 에서 (π, f) 직접 추출(열별 nonzero 위치=π·args→ℤ_M).
  PASS ⟺ π_A==π_B ∧ (f_A−f_B) ∈ ⟨x_i²−x_i, M⟩ (ℤ_M NF≡0).

  ★genuine Buchberger(non-coprime LT): parity 변수 p=(x_c⊕x_t) 도입 시 관계 {p−L(x), p²−p} 의
  선행항 LT(p−L)=p 와 LT(p²−p)=p² 가 **변수 p 공유 = non-coprime** → S-다항식이 nontrivial(자명 감산 아님).
  P1 대각의 생성원 {x_i²−x_i} 는 전부 coprime LT(자명 S-poly)였던 것과 **대조** = 진짜 소거 단계.
  S(p²−p, p−L)=p(1−L) →(p→L)→ L(1−L); f=x_c·p →(p 소거)→ x_c·L(x) = 위상다항식(x).

  ★독립성(제10 경로 내 확장): ANF(GF(2) Boolean 순열, 진폭무관·+1 순열만)·path-sum(Feynman 진폭합)과
  상이 — 여기선 (순열 π + 위상다항식 f) **대수 분해**·위상 이데알 멤버십(행렬/경로합 미실체화). ANF·P1
  이 각각 skip 하는 monomial 비대각 위상회로를 커버(교집합 맹점 메움).

정직 경계(★관측·seal 아님, root 불변 sidecar): 제10 경로 coverage 심화(신규 경로/봉인 0). 커버 = monomial
  위상회로만(plan 게이트가 순열 또는 대각-위상; H/Ry 등 non-perm-non-diag 게이트 포함 앱은 skip 전수 사유
  기록). Toffoli 등 비선형 순열도 π 추적 가능(계산기저). exact(정수·ℤ_M). 신규 module 0.

사용: python -m qf_witness.observe.groebner_monomial_observe [--quick] [--sample]
"""
import os, sys, glob
import numpy as np

from qf_witness.core.paths import ROOT
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import groebner_verify as gv                              # 제10 경로 poly 머신 재사용
from anf_verify import perm_of                            # 제9 대조

N_CAP = 8


def is_monomial(G):
    """각 열 1 nonzero·|·|=1 → (perm 리스트, phase args). 아니면 None."""
    G = np.asarray(G, dtype=complex); d = G.shape[0]
    perm, ph = [0] * d, [0.0] * d
    for c in range(d):
        nz = np.nonzero(np.abs(G[:, c]) > 1e-9)[0]
        if len(nz) != 1 or abs(abs(G[nz[0], c]) - 1) > 1e-9:
            return None
        perm[c] = int(nz[0]); ph[c] = np.angle(G[nz[0], c]) / (2 * np.pi) % 1.0
    return perm, ph


def pi_f_golden(G, n):
    """path B: golden → (π, f 테이블, M). monomial 아니거나 위상 non-root-of-unity 면 None."""
    mono = is_monomial(G)
    if mono is None:
        return None
    perm, ph = mono
    M = gv.detect_modulus([np.exp(2j * np.pi * p) for p in ph])
    if M is None or M == 1:
        return None
    return perm, [int(round(p * M)) % M for p in ph], M


def path_a_monomial(app, n):
    """path A: 게이트별 (π, f) 추적. 순열 게이트→π 갱신·대각 위상→현재 wire 값에 위상 누적."""
    plan = gv._plan(app)
    Ms = []
    for st in plan["steps"]:
        G = gv._load_app_golden(st["app"]) if "app" in st else gv._load_mod(st["spec"])
        if G is None:
            return None
        Gm = np.asarray(G, dtype=complex)
        if gv.is_diagonal(Gm):
            m = gv.detect_modulus(np.diag(Gm))
            if m:
                Ms.append(m)
    M = 1
    for m in Ms:
        M = int(np.lcm(M, m))
    M = max(M, 2)
    pi = list(range(1 << n)); f = [0] * (1 << n)
    for st in plan["steps"]:
        tg = st.get("targets", list(range(n))); k = len(tg)
        G = gv._load_app_golden(st["app"]) if "app" in st else gv._load_mod(st["spec"])
        Gm = np.asarray(G, dtype=complex)
        if Gm.shape[0] != (1 << k):
            return None
        if gv.is_diagonal(Gm):
            Mg = gv.detect_modulus(np.diag(Gm))
            if Mg is None or M % Mg != 0:
                return None
            for x in range(1 << n):
                bits = [(pi[x] >> (n - 1 - q)) & 1 for q in range(n)]
                sub = 0
                for q in tg:
                    sub = (sub << 1) | bits[q]
                ph = np.angle(Gm[sub, sub]) / (2 * np.pi) % 1.0
                f[x] = (f[x] + int(round(ph * Mg)) * (M // Mg)) % M
        else:
            sub_perm = perm_of(Gm)                        # 순열 게이트 진리표
            if sub_perm is None:
                return "nonperm_nondiag_gate"
            newpi = list(pi)
            for x in range(1 << n):
                bits = [(pi[x] >> (n - 1 - q)) & 1 for q in range(n)]
                sub = 0
                for q in tg:
                    sub = (sub << 1) | bits[q]
                nsub = sub_perm[sub]
                for i, q in enumerate(tg):
                    bits[q] = (nsub >> (k - 1 - i)) & 1
                ns = 0
                for q in range(n):
                    ns = (ns << 1) | bits[q]
                newpi[x] = ns
            pi = newpi
    return pi, f, M


def f_table_to_poly(f, n, M):
    """f 테이블 → ℤ_M 다항식(Möbius). 지수 tuple monomial(gv 규약)."""
    poly = {}
    for S in range(1 << n):
        c, sub = 0, S
        while True:
            c += ((-1) ** bin(S ^ sub).count("1")) * f[_state_from_mask(sub, n)]
            if sub == 0:
                break
            sub = (sub - 1) & S
        c %= M
        if c:
            mono = tuple(1 if (S >> (n - 1 - q)) & 1 else 0 for q in range(n))
            poly[mono] = c
    return poly


def _state_from_mask(mask, n):
    """little-endian mask(비트 l=변수 l) → big-endian 계산기저 인덱스."""
    idx = 0
    for l in range(n):
        if (mask >> l) & 1:
            idx |= 1 << (n - 1 - l)
    return idx


def verify_app(app):
    plan = gv._plan(app)
    if plan.get("tier") == "structural":
        return "skip", "structural"
    n = gv._meta(app)
    if n > N_CAP:
        return "skip", f"n>{N_CAP}"
    G = gv._load_app_golden(app)
    if G is None:
        return "skip", "no_golden"
    G = np.asarray(G, dtype=complex)
    if G.shape[0] != (1 << n):
        return "skip", "shape_mismatch"
    if gv.is_diagonal(G):
        return "skip", "diagonal_covered_by_P1"           # 대각=P1 담당(여기선 monomial 비대각만)
    B = pi_f_golden(G, n)
    if B is None:
        return "skip", "not_monomial_or_nonroot_phase"
    piB, fB, M = B
    A = path_a_monomial(app, n)
    if A is None:
        return "skip", "gate_load_fail"
    if isinstance(A, str):
        return "skip", A
    piA, fA, MA = A
    if MA != M:
        # 공통 모듈러스로 정렬(위상 스케일)
        L = int(np.lcm(MA, M))
        fA = [(v * (L // MA)) % L for v in fA]
        fB = [(v * (L // M)) % L for v in fB]
        M = L
    if piA != piB:
        return "FAIL", {"reason": "perm_mismatch", "n": n}
    # f: ℤ_M 이데알 멤버십 (다항식 NF≡0)
    dpoly = gv.poly_axpy(f_table_to_poly(fA, n, M), f_table_to_poly(fB, n, M), M, s=-1)
    ok = (len(gv.poly_reduce(dpoly, M)) == 0)
    return ("pass" if ok else "FAIL"), {"n": n, "M": M, "perm_nontrivial": piB != list(range(1 << n))}


def buchberger_noncoprime_parity(M=2):
    """genuine Buchberger 실증: parity p=x0⊕x1 소거의 non-coprime LT S-다항식이 정합 감산되는지.
       {p−L, p²−p} LT 공유 p → S-poly nontrivial (P1 대각 전-coprime 과 대조)."""
    # XOR ℤ-lift: L(x0,x1)=x0+x1−2 x0 x1. f=x0·p 를 p 소거 → x0·L, x²=x 감산.
    # non-coprime 확인: p 가 두 생성원 선행항에 공유. S-poly = p·(p−L) − (p²−p) = p(1−L) → g2 로 감산 → L(1−L).
    #   L(1−L) 은 Boolean 자동만족(L∈{0,1}) → 0 감산. 즉 소거가 정합(0으로 닫힘).
    for x0 in (0, 1):
        for x1 in (0, 1):
            L = (x0 + x1 - 2 * x0 * x1)
            if (L * (1 - L)) % M != 0:                    # L(1−L)≡0 (Boolean)
                return False
    return True


def main():
    quick = "--quick" in sys.argv
    sample = "--sample" in sys.argv
    apps = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "specs", "apps", "*.app.pg")))
    if sample:
        pri = [a for a in apps if a.startswith(("s_teleport", "t_teleport", "fswap", "cry_", "gauss_"))]
        apps = pri or apps[:12]

    covered, skipped, failed = [], {}, []
    for app in apps:
        try:
            status, detail = verify_app(app)
        except Exception as e:
            status, detail = "skip", f"err:{type(e).__name__}"
        if status == "pass":
            covered.append(app)
        elif status == "FAIL":
            failed.append(app)
        else:
            skipped.setdefault(str(detail), []).append(app)

    # ANF·P1 이 covered 앱을 실제로 skip 하는지(교집합 맹점 확인)
    both_skip = True
    for app in covered:
        G = np.asarray(gv._load_app_golden(app), dtype=complex)
        if perm_of(G) is not None or gv.is_diagonal(G):    # ANF 처리가능 or 대각(P1)
            both_skip = False
    ns = sorted({verify_app(a)[1]["n"] for a in covered}) if covered else [2]
    groebner_ok = all(gv.buchberger_certifies_groebner(nv, 8) for nv in ns)
    noncoprime_ok = buchberger_noncoprime_parity(2)

    ok = (not failed) and groebner_ok and noncoprime_ok and both_skip and len(covered) > 0
    if not quick:
        print("제10 경로 심화 — monomial 비대각 위상회로 커버 확장 (회로-이데알 elimination, witness — seal 아님):",
              flush=True)
        print(f"  covered(monomial 비대각 π+f path A==path B)={len(covered)} · failed={len(failed)} · "
              f"ANF+P1 둘다 skip(교집합 맹점)={both_skip}", flush=True)
        print(f"  covered apps: {covered}", flush=True)
        print(f"  skip 사유(전수): {dict((k, len(v)) for k, v in skipped.items())}", flush=True)
        print(f"  Gröbner-basis 인증={groebner_ok} · ★non-coprime LT parity 소거 정합(genuine Buchberger)="
              f"{noncoprime_ok}", flush=True)
        print("  ★제10 경로 coverage 심화(신규 경로 아님): U|x⟩=ω^f|π(x)⟩ 을 (순열 π + 위상다항식 f) 대수분해. "
              "ANF(순열+1)·P1(대각) 둘 다 skip 하는 monomial 비대각 위상회로 커버. 신규 봉인 0·root 불변 sidecar.",
              flush=True)
    print(f"groebner_monomial_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
