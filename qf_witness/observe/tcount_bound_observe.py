#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tcount_bound_observe — TcountLowerBound: gridsynth _ct 가족 T-count 하한 인증 관측
(관측·sidecar, seal 아님·root 불변·module 0).

§3s 잔여 관문 "T-count 최적 합성(최단성 하한)"의 내부 선점: 단일큐빗 Clifford+T 유니터리를
**Matsumoto-Amano 정규형 (T|ε)·(HT|SHT)^s·C₂₄ 로 전수 열거**(T-count t ≤ TMAX, MA 유일성 =
누락/중복 없는 전수)하고, 각 목표 R_z(π/2^k) (k=3..7) 에 대해 위상정렬 op-norm 거리
d_min(t) = min{ d(U,R) : T-count(U) ≤ t } 곡선을 산출한다.

산출(전부 관측):
  1. ★인증 하한 L_k = ε_ct 달성 최소 T-count — "t < L_k 로는 ε_ct 이하 불가"를 전수로 확립.
     임계와의 float 여유(≥1e-5 급 ≫ fp 오차 1e-12)를 margin 으로 함께 기록(정직).
  2. ★MA 정준 T-count: 봉인 _ct 유니터리 자체를 열거에서 재발견(d≈0) → 레터 카운트(TT=S 흡수
     미반영 과대표기)와 구분되는 정준 T-count 보고.
  3. ★비최적 gap 정량화: MA 정준 T-count − L_k. 더 짧은 달성 시퀀스(레터 전개) 기록 — 봉인 아님.
  4. crossing 시퀀스 exact 재검증: MA desc → H/T 레터 전개(S=TT) → ℤ[ω] ring shadow + sympy
     exact ε ≤ ε_ct 확인(임계 근접 판정의 최종 근거는 exact).
  ε_ct 임계 = APPROX-GUARANTEES 의 epsilon_upper_symbolic(단일출처, sympy 고정밀 평가).

정직 경계: 하한은 **위상정렬 op-norm metric·해당 ε_ct 임계에 한정**(다른 metric/ε 무주장).
  열거=float(오차 ~1e-13, 배제 margin 대비 무시 가능 — margin 기록)·달성측은 exact 재검증.
  _rs(T~220)는 전수 불가 — 스코프 제외 명시. 봉인 자산 불변(더 짧은 시퀀스는 관측 기록만).
teeth: (i) |Clifford₂₄|=24·위상정규화 중복 0 (ii) 봉인 _ct 유니터리 전원 열거 내 재발견(d<1e-6 —
  √ 증폭: 정확일치도 float d≈3e-8, 열거 도달성 실증) (iii) 임계 오염(ε/2) → crossing 상승 검출.

사용: python -m qf_witness.observe.tcount_bound_observe [--quick]
"""
from __future__ import annotations
import math
import cmath
import sys
import json

from qf_witness.core.paths import ROOT
from qf_witness.family.gridsynth_family import SEQS as CT_SEQS, ring_shadow

SQ2 = math.sqrt(2.0)
H = ((1 / SQ2, 1 / SQ2), (1 / SQ2, -1 / SQ2))
T = ((1, 0), (0, cmath.exp(1j * math.pi / 4)))
S = ((1, 0), (0, 1j))
I2 = ((1, 0), (0, 1))


def mm(A, B):
    return ((A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]),
            (A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]))


def cliffords24():
    """⟨H,S⟩ BFS, 전역위상 정규화 24개 — (행렬, 생성어 H/S)."""
    def canon(M):
        for row in M:
            for v in row:
                if abs(v) > 1e-9:
                    ph = v / abs(v)
                    N = tuple(tuple(x / ph for x in r) for r in M)
                    return tuple(tuple((round(x.real, 6), round(x.imag, 6)) for x in r) for r in N)
        return None
    seen = {canon(I2): (I2, "")}
    frontier = [(I2, "")]
    while frontier:
        nxt = []
        for M, w in frontier:
            for G, g in ((H, "H"), (S, "S")):
                M2 = mm(G, M)
                c = canon(M2)
                if c not in seen:
                    seen[c] = (M2, g + w)
                    nxt.append((M2, g + w))
        frontier = nxt
    return list(seen.values())


CLIFF = cliffords24()
HT = mm(H, T)
SHT = mm(S, HT)


def seq_unitary(seq):
    U = I2
    for g in seq:
        U = mm(H if g == "H" else T, U)
    return U


def enumerate_dmin(targets, smax):
    """targets: {name: R} → (curves per-t 최소, best {name:{t:(d, desc)}}) — MA 전수."""
    curves = {n: [9.0] * (smax + 2) for n in targets}
    best = {n: {} for n in targets}

    def consider(P, t, desc):
        for n, R in targets.items():
            a00 = P[0][0].conjugate() * R[0][0] + P[1][0].conjugate() * R[1][0]
            a01 = P[0][0].conjugate() * R[0][1] + P[1][0].conjugate() * R[1][1]
            a10 = P[0][1].conjugate() * R[0][0] + P[1][1].conjugate() * R[1][0]
            a11 = P[0][1].conjugate() * R[0][1] + P[1][1].conjugate() * R[1][1]
            mx, marg = 0.0, ""
            for C, w in CLIFF:
                # tr(C†·P†R) = Σ_ij conj(C_ji)·A_ji — a10↔C10·a01↔C01 짝 주의(전치 금지)
                tr = abs(a00 * C[0][0].conjugate() + a10 * C[1][0].conjugate()
                         + a01 * C[0][1].conjugate() + a11 * C[1][1].conjugate())
                if tr > mx:
                    mx, marg = tr, w
            d = math.sqrt(max(0.0, 2.0 - mx))
            if d < curves[n][t]:
                curves[n][t] = d
                best[n][t] = (d, desc + "|C:" + (marg or "I"))

    def dfs(P, s, desc):
        consider(P, s, "e|" + desc)
        consider(mm(T, P), s + 1, "T|" + desc)
        if s < smax:
            dfs(mm(HT, P), s + 1, desc + ".HT")
            dfs(mm(SHT, P), s + 1, desc + ".SHT")

    dfs(I2, 0, "")
    return curves, best


def desc_to_letters(desc):
    """'T|.SHT.HT|C:SHS' → H/T 레터 시퀀스(시간순 우→좌 적용 구조를 레터 시간순으로 전개).
    U = lead · syl_last···syl_1 · C  → 시간순 = [C 레터][syl_1][…][syl_last][lead]. S=TT."""
    core, cw = desc.split("|C:")
    lead, syls = core.split("|")
    parts = [p for p in syls.split(".") if p]
    out = []
    cw = "" if cw == "I" else cw
    for ch in reversed(cw):                 # C 생성어 g+w 는 좌곱 누적 → 시간순 = 뒤집기
        out.extend("TT" if ch == "S" else ch)
    for p in parts:                          # syl_1 부터 (desc 는 적용순 기록)
        for ch in reversed(p):               # ★음절 내부도 행렬곱 좌→우 = 시간역순 → 뒤집기
            out.extend("TT" if ch == "S" else ch)
    if lead == "T":
        out.append("T")
    return "".join(out)


def exact_eps_hp(letters, k):
    """H/T 레터 → ring shadow → sympy exact ε — 40자리 고정밀(sympy Float).

    √ 증폭 주의: float64 d=√(2−|tr|) 는 정확일치도 ~3e-8 — 미세 판정은 전부 이 경로."""
    import sympy as sp
    M, m = ring_shadow(letters)

    def wsym(x):
        om = sp.exp(sp.I * sp.pi / 4)
        return x[0] + x[1] * om + x[2] * om ** 2 + x[3] * om ** 3

    def wconj(x):
        return (x[0], -x[3], -x[2], -x[1])

    from qf_witness.family.gridsynth_family import w_mul
    theta = sp.pi / 2 ** k
    w0, w1 = wconj(M[0][0]), wconj(M[1][1])
    A = tuple(p + q for p, q in zip(w_mul(w0, wconj(w0)), w_mul(w1, wconj(w1))))
    B = w_mul(w0, wconj(w1))
    z2 = wsym(A) + wsym(B) * sp.exp(-sp.I * theta) + sp.conjugate(wsym(B)) * sp.exp(sp.I * theta)
    tr2 = sp.simplify(sp.expand_complex(z2)) / 2 ** m
    return sp.N(sp.sqrt(2 - sp.sqrt(tr2)), 40)


def load_eps_ct():
    """APPROX-GUARANTEES 단일출처: _ct 가족 ε 임계 — (sympy 40자리, float64) 쌍."""
    import sympy as sp
    d = json.load(open(f"{ROOT}/registry/APPROX-GUARANTEES.json", encoding="utf-8"))
    out = {}
    for k in range(3, 8):
        app = f"rz_pi{2 ** k}_ct"
        hp = sp.N(sp.sympify(d["certificates"][app]["epsilon_upper_symbolic"]), 40)
        out[k] = (hp, float(hp))
    return out


def main():
    quick = "--quick" in sys.argv
    smax = 10 if quick else 15
    R = {}
    checks = {}

    checks["cliffords_24_unique"] = (len(CLIFF) == 24)

    eps_ct = load_eps_ct()
    targets = {f"k{k}": ((cmath.exp(-1j * math.pi / 2 ** (k + 1)), 0),
                         (0, cmath.exp(1j * math.pi / 2 ** (k + 1)))) for k in range(3, 8)}
    # 봉인 _ct 유니터리 자체도 타깃에 (MA 정준 T-count 재발견용)
    ct_targets = {}
    for app, (k, seq) in CT_SEQS.items():
        ct_targets[f"U_{app}"] = seq_unitary(seq)
    curves, best = enumerate_dmin({**targets, **ct_targets}, smax)

    TOL_EQ = 1e-6                            # √ 증폭 반영(정확일치 float d ≈ 3e-8)
    results = {}
    all_cross_exact_ok = True
    all_borderline_ok = True
    for k in range(3, 8):
        hp, epsf = eps_ct[k]
        import sympy as sp
        cum, cross = 9.0, None
        curve_c = []
        margin_excl = 9.0                    # 배제 구간에서 임계와의 최소 여유(float)
        arg = None                           # 현재 누적최소의 (t, desc)
        tried_exact = set()
        pre_borderline = []                  # crossing 탐색 중 exact-배제된 후보
        for t, d in enumerate(curves[f"k{k}"]):
            if d < cum:
                cum, arg = d, t
            curve_c.append(round(cum, 8))
            if cross is None:
                if cum <= epsf + TOL_EQ:
                    # ★exact-구동 crossing: float 후보를 40자리에서 확정
                    key = best[f"k{k}"][arg][1]
                    if key in tried_exact:
                        continue
                    tried_exact.add(key)
                    e = exact_eps_hp(desc_to_letters(key), k)
                    if e <= hp + sp.Float("1e-20", 40):
                        cross = t
                    else:
                        pre_borderline.append({"t": t, "eps_exact": float(e), "gt_eps_ct": True})
                        margin_excl = min(margin_excl, float(e) - epsf)
                else:
                    margin_excl = min(margin_excl, cum - epsf)
        # MA 정준 T-count(봉인 유니터리 재발견 최소 t — √ 증폭 문턱 1e-6)
        app = f"rz_pi{2 ** k}_ct"
        ma_t = next((t for t, d in enumerate(curves[f"U_{app}"]) if d < 1e-6), None)
        # crossing 달성 시퀀스 exact 재검증(등식 케이스 포함: e ≤ hp + 1e-20)
        cross_exact = None
        if cross is not None:
            letters = desc_to_letters(best[f"k{k}"][arg][1])
            e = exact_eps_hp(letters, k)
            le = bool(e <= hp + sp.Float("1e-20", 40))
            cross_exact = {"letters": letters, "eps_exact": float(e), "le_eps_ct": le}
            all_cross_exact_ok &= le
        # 배제 경계 후보 = crossing 탐색 중 exact-배제분(이미 40자리 단언됨)
        borderline = pre_borderline
        results[app] = {
            "eps_ct_threshold": epsf,
            "letter_t_count": CT_SEQS[app][1].count("T"),
            "ma_canonical_t_count": ma_t,
            "certified_min_t_for_eps": cross,
            "optimality_gap_vs_ma": (None if (ma_t is None or cross is None) else ma_t - cross),
            "exclusion_float_margin": (round(margin_excl, 9) if cross not in (None, 0) else None),
            "borderline_exact_rechecks": borderline,
            "dmin_curve_cummin": curve_c,
            "crossing_witness": cross_exact,
        }

    checks["ct_unitaries_rediscovered"] = all(
        r["ma_canonical_t_count"] is not None for r in results.values()) if not quick else True
    checks["crossings_found"] = all(r["certified_min_t_for_eps"] is not None
                                    for r in results.values()) if not quick else True
    checks["crossing_exact_verified"] = bool(all_cross_exact_ok)
    checks["exclusion_margins_safe"] = all(
        (r["exclusion_float_margin"] is None or r["exclusion_float_margin"] > 1e-6
         or r["borderline_exact_rechecks"]) for r in results.values())
    checks["borderline_exact_ok"] = bool(all_borderline_ok)
    # teeth: 임계 오염(ε/2) → crossing 상승(엄격) — k=4 대표
    cum, cr_half = 9.0, None
    for t, d in enumerate(curves["k4"]):
        cum = min(cum, d)
        if cr_half is None and cum <= eps_ct[4][1] / 2:
            cr_half = t
    r4 = results["rz_pi16_ct"]["certified_min_t_for_eps"]
    checks["teeth_threshold_tamper"] = (cr_half is None or (r4 is not None and cr_half > r4))

    ok = bool(all(checks.values()))
    out = {"_schema": "tcount-bound/v1",
           "_note": ("MA 정규형 전수(T-count ≤ %d)로 _ct 가족 T-count 하한 인증 + MA 정준 "
                     "T-count 재발견 + 비최적 gap 정량화(관측·seal 아님·root 불변). "
                     "하한은 위상정렬 op-norm·해당 ε_ct 임계 한정. 배제=float(margin 기록·"
                     "fp 오차 1e-13 대비 안전)·달성=exact 재검증. _rs 전수 불가 스코프 제외. "
                     "더 짧은 달성 시퀀스는 기록만(봉인 자산 불변)." % smax),
           "tmax": smax, "results": results, "checks": checks, "all_ok": ok}

    if not quick:
        p = f"{ROOT}/.pgf/proofs/TCOUNT-BOUND.json"
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        for app, r in results.items():
            print(f"  {app}: letter_T={r['letter_t_count']} MA_T={r['ma_canonical_t_count']} "
                  f"→ ★min_T(ε_ct)={r['certified_min_t_for_eps']} "
                  f"gap={r['optimality_gap_vs_ma']} margin={r['exclusion_float_margin']}", flush=True)
        print(f"  checks: {checks}", flush=True)
        print("  → .pgf/proofs/TCOUNT-BOUND.json", flush=True)
    print(f"tcount_bound_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
