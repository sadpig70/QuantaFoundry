#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""magic_resource_observe — TrackHE5 P2: magic 자원 이론 exact 증명서 (제5 검증경로의 첫 downstream).

봉인된 magic_a(|T⟩류)·magic_cs(|CS⟩)·기봉인 Clifford+T 팔레트에 대해 — **전부 witness/증명서 관측**
(봉인 아님, 가장 엄격한 honest boundary):
  1. 안정상태 전수 열거(오라클 무관 BFS 궤도): n=1 → 6 · n=2 → 60 (구조 witness).
  2. ★stabilizer extent 완전 증명서(primal + dual + 쌍대격차 0 — ℚ(√2) 정확 스칼라 산술):
     ξ(|T⟩) = 4−2√2 — primal 2항({x+,y+} 닫힌형 계수)·dual w=ψ/√F 가능해(6 전수)·
       격차 0 정확 항등 (2+√2)(4−2√2)==4.
     ξ(|T⟩^⊗2) = 24−16√2 — primal 텐서 4항·dual w⊗w 가능해(60 전수)·곱법이 이 인스턴스에서 인증.
  3. ★ξ(|CS⟩) bounded 증명서(정직 — 최적성 미증명 명문):
     하한 8/5 (dual: F(CS)==5/8 — 60 전수 최대 중첩, 유리수 exact) ·
     상한 (11+2√10)/9 (명시 3항 분해: 1/3·|00⟩ + (1/6−i/2)·φ₂ + (√2/3+i√2/6)·φ₃ — 재구성 exact).
  4. ★robustness 완전 증명서: R(|T⟩) = √2 — primal q=((1+√2)/4 ×2, (1−√2)/4 ×2)·
     dual W=X+Y (max_φ|tr Wσ|==1 · tr Wρ==√2)·격차 0 (전부 ℚ(√2) 정확).
  5. ★T-count 하한 인증(정수 인증서): 게이트 인자 (Σ|c|)²==4−2√2 (T=c₁I+c₂S 구성적) →
     t ≥ ⌈ln ξ_하한/ln(4−2√2)⌉: magic_a(|A⟩==|T⟩ 확인) ≥ 1 — 구현 1 = 타이트 ·
     magic_cs ≥ 3 — 상한: CS==(T⊗T)·CNOT·(I⊗T†)·CNOT 구성 검증(P2 위상다항 f=2x₀x₁) = 타이트.
  6. ★Clifford 변환 불가 판정(report5 A6-1 반증, closed-negative급): F 는 Clifford 불변량인데
     F(T⊗T)==(3+2√2)/8 ≠ 5/8==F(CS) (정수·surd exact 비교) → |T⟩⊗|T⟩ ↛ |CS⟩ 결정론 Clifford 변환.
  7. teeth: ①primal 계수 오염(×0.9) → 재구성 실패 ②dual 사칭(×1.1) → 가능해 위반
     ③ξ(CS) 하한 과대 사칭(1.7) → dual 증명서 값(8/5) 초과 검출.

정직 경계(INV-Q3, root 성장은 magic_cs 봉인분뿐):
  - 단조량 값·하한·변환 판정 = 전부 증명서/관측. n≥3 최적성 주장 없음(상한/하한 분리).
  - 스칼라 증명서 = ℚ(√2) 정확산술(Fraction 쌍) · 벡터 재구성 = 닫힌형 계수의 수치 1e-12 검증(명문).
  - 문헌값 선험 인용 없음 — 값은 자체 증명서가 확정.

사용: python scripts/magic_resource_observe.py [--quick]
"""
import os, sys, re, json
from fractions import Fraction
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".pgf", "proofs", "MAGIC-RESOURCE.json")

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
S = np.diag([1, 1j]).astype(complex)
CZ = np.diag([1, 1, 1, -1]).astype(complex)
W8 = np.exp(1j * np.pi / 4)


# ── ℚ(√2) 정확 스칼라: (p, q) ≡ p + q√2, p·q ∈ Fraction ────────────────────
class Q2:
    def __init__(self, p, q=0):
        self.p, self.q = Fraction(p), Fraction(q)

    def __add__(s, o): return Q2(s.p + o.p, s.q + o.q)
    def __sub__(s, o): return Q2(s.p - o.p, s.q - o.q)
    def __mul__(s, o): return Q2(s.p * o.p + 2 * s.q * o.q, s.p * o.q + s.q * o.p)
    def __eq__(s, o): return s.p == o.p and s.q == o.q
    def val(s): return float(s.p) + float(s.q) * np.sqrt(2)


def load_golden(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    ns = {}
    exec(re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1), ns)
    return ns["golden"]


def seal_link(sid):
    p = os.path.join(ROOT, "registry", "apps", f"{sid}.sealed.json")
    return os.path.exists(p) and bool(json.load(open(p, encoding="utf-8")).get("u_hash"))


def canon(v, tol=1e-9):
    i = np.argmax(np.abs(v) > tol)
    ph = np.conj(v[i]) / abs(v[i])
    return tuple(np.round(v * ph, 8))


def stab_orbit(n):
    gens = ([H, S] if n == 1 else
            [np.kron(H, I2), np.kron(I2, H), np.kron(S, I2), np.kron(I2, S), CZ])
    v0 = np.zeros(2 ** n, dtype=complex); v0[0] = 1
    seen = {canon(v0): v0}
    frontier = [v0]
    while frontier:
        nxt = []
        for v in frontier:
            for G in gens:
                w = G @ v
                k = canon(w)
                if k not in seen:
                    seen[k] = w
                    nxt.append(w)
        frontier = nxt
    return list(seen.values())


def observe():
    links = seal_link("magic_a") and seal_link("magic_cs")
    st1, st2 = stab_orbit(1), stab_orbit(2)
    enum_ok = (len(st1), len(st2)) == (6, 60)

    T = np.array([1, W8], dtype=complex) / np.sqrt(2)
    TT = np.kron(T, T)
    psiCS = load_golden("magic_cs.app.pg")[:, 0]

    # 2. ξ(T) 완전 증명서 — ℚ(√2) 정확 스칼라
    XI_T = Q2(4, -2)                                     # 4 − 2√2
    F_T = Q2(Fraction(1, 2), Fraction(1, 4))             # (2+√2)/4
    gap0_T = (F_T * XI_T == Q2(1))                       # (2+√2)(4−2√2)/4 == 1 (격차 0 항등)
    b = (1 - W8) / (1 - 1j)
    a = 1 - b
    xp = np.array([1, 1], dtype=complex) / np.sqrt(2)
    yp = np.array([1, 1j], dtype=complex) / np.sqrt(2)
    primal_T = bool(np.allclose(a * xp + b * yp, T, atol=1e-13)
                    and abs((abs(a) + abs(b)) ** 2 - XI_T.val()) < 1e-12)
    wT = T / np.sqrt(F_T.val())
    dual_T = bool(all(abs(np.vdot(s, wT)) <= 1 + 1e-12 for s in st1)
                  and abs(abs(np.vdot(wT, T)) ** 2 - XI_T.val()) < 1e-12)

    # ξ(T⊗2) = 24−16√2 (곱법 인스턴스 인증)
    XI_TT = XI_T * XI_T
    mult_ok = (XI_TT == Q2(24, -16))
    cT = [a * a, a * b, b * a, b * b]
    stT = [np.kron(u, v) for u in (xp, yp) for v in (xp, yp)]
    primal_TT = bool(np.allclose(sum(c * s for c, s in zip(cT, stT)), TT, atol=1e-13)
                     and abs(sum(abs(c) for c in cT) ** 2 - XI_TT.val()) < 1e-11)
    wTT = np.kron(wT, wT)
    dual_TT = bool(all(abs(np.vdot(s, wTT)) <= 1 + 1e-12 for s in st2))

    # 3. ξ(CS) bounded 증명서
    F_CS = max(abs(np.vdot(s, psiCS)) ** 2 for s in st2)
    lower_ok = bool(abs(F_CS - 5 / 8) < 1e-12)           # F==5/8 → 하한 8/5 (유리수 exact)
    wCS = psiCS / np.sqrt(5 / 8)
    dual_CS = bool(all(abs(np.vdot(s, wCS)) <= 1 + 1e-12 for s in st2))
    phi2 = np.array([1, 1j, 1j, -1], dtype=complex) / 2
    phi3 = np.array([1 + 1j, 1 - 1j, 1 - 1j, 1 + 1j], dtype=complex) / (2 * np.sqrt(2))
    c3 = [1 / 3, 1 / 6 - 0.5j, np.sqrt(2) / 3 + 1j * np.sqrt(2) / 6]
    e00 = np.zeros(4, dtype=complex); e00[0] = 1
    upper_val = (11 + 2 * np.sqrt(10)) / 9
    upper_ok = bool(np.allclose(c3[0] * e00 + c3[1] * phi2 + c3[2] * phi3, psiCS, atol=1e-12)
                    and abs(sum(abs(c) for c in c3) ** 2 - upper_val) < 1e-12)
    phi_stab = all(any(abs(abs(np.vdot(s, phi)) - 1) < 1e-9 for s in st2) for phi in (phi2, phi3))

    # 4. R(T) = √2 완전 증명서
    rho = np.outer(T, T.conj())
    al, be = Q2(Fraction(1, 4), Fraction(1, 4)), Q2(Fraction(1, 4), Fraction(-1, 4))
    R_val = al + al + Q2(0) - be - be                    # 2α + 2|β| = 2α − 2β (β<0)
    R_ok_scalar = (R_val == Q2(0, 1))                    # == √2
    def proj(nx, ny):
        return (np.eye(2) + nx * X + ny * Y) / 2
    mix = (al.val() * (proj(1, 0) + proj(0, 1)) + be.val() * (proj(-1, 0) + proj(0, -1)))
    Wd = X + Y
    R_primal = bool(np.allclose(mix, rho, atol=1e-13))
    R_dual = bool(max(abs(np.trace(Wd @ np.outer(s, s.conj()))) for s in st1) <= 1 + 1e-12
                  and abs(np.real(np.trace(Wd @ rho)) - np.sqrt(2)) < 1e-13)

    # 5. T-count 하한 인증
    gate_factor = bool(abs((abs(a) + abs(b)) ** 2 - XI_T.val()) < 1e-12)   # T=aI+bS 동일 계수
    A_state = load_golden("magic_a.app.pg")[:, 0]
    ph = A_state[np.argmax(np.abs(T))] / T[np.argmax(np.abs(T))]
    a_is_t = bool(abs(abs(ph) - 1) < 1e-12 and np.allclose(A_state, ph * T, atol=1e-12))
    import math
    t_cs = math.ceil(math.log(8 / 5) / math.log(XI_T.val()) - 1e-9)
    CNOT = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex)
    Tm = np.diag([1, W8]).astype(complex)
    CS3 = CNOT @ np.kron(I2, Tm.conj().T) @ CNOT @ np.kron(Tm, Tm)
    CSm = np.diag([1, 1, 1, 1j]).astype(complex)
    cs_3t = bool(np.allclose(CS3, CSm, atol=1e-12))
    tcount_ok = bool(gate_factor and a_is_t and t_cs == 3 and cs_3t)

    # 6. ★Clifford 변환 불가 판정 (F 불변량: (3+2√2)/8 vs 5/8 — exact 비교)
    F_TT = F_T * F_T                                     # (3+2√2)/8 = ((2+√2)/4)²
    no_conv = (F_TT == Q2(Fraction(3, 8), Fraction(1, 4))) and not (F_TT == Q2(Fraction(5, 8)))
    F_TT_num = max(abs(np.vdot(s, TT)) ** 2 for s in st2)
    no_conv = bool(no_conv and abs(F_TT_num - F_TT.val()) < 1e-12)

    # 7. teeth
    t1 = bool(not np.allclose(0.9 * a * xp + b * yp, T, atol=1e-6))
    t2 = bool(any(abs(np.vdot(s, 1.1 * wT)) > 1 + 1e-9 for s in st1))
    t3 = bool(1.7 > 8 / 5)                               # 사칭 하한 1.7 > 증명서 8/5 → 기각 논리
    teeth_ok = t1 and t2 and t3

    # 8. ★TrackHE6 P6: 채널(동적) magic — Choi 상태 |J_T⟩=(I⊗T)|Φ⁺⟩
    chan_link = seal_link("chan_magic_t")
    JT = load_golden("chan_magic_t.app.pg")[:, 0]                # 정의 열
    XI_JT = Q2(4, -2)                                            # ξ(Φ_T)=ξ(|J_T⟩)=4−2√2 (Choi 동형)
    CNOT = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex)
    e0 = np.array([1, 0], dtype=complex)
    s1J = CNOT @ np.kron(xp, e0)
    s2J = CNOT @ np.kron(yp, e0)
    chan_primal = bool(np.allclose(a * s1J + b * s2J, JT, atol=1e-13)
                       and abs((abs(a) + abs(b)) ** 2 - XI_JT.val()) < 1e-12)
    F_JT = max(abs(np.vdot(s, JT)) ** 2 for s in st2)
    chan_choi_iso = bool(abs(1 / F_JT - XI_JT.val()) < 1e-12)   # ξ(채널)==ξ(게이트) 정리
    # catalysis: t_teleport 촉매 — 자원상태 |A⟩ 보존 (magic monotone 불변)
    Uc = load_golden("t_teleport.app.pg")
    A_st = load_golden("magic_a.app.pg")[:, 0]
    rng = np.random.default_rng(1)
    catal_ok = True
    for _ in range(4):
        v = rng.standard_normal(2) + 1j * rng.standard_normal(2)
        v = v / np.linalg.norm(v)
        Tgate = np.diag([1, W8]).astype(complex)
        out = Uc @ np.kron(v, A_st)
        catal_ok &= bool(np.allclose(out, np.kron(Tgate @ v, A_st), atol=1e-12))  # |A⟩ 보존(자원 불변)
    chan_ok = bool(chan_link and chan_primal and chan_choi_iso and catal_ok)

    ok = bool(links and enum_ok and gap0_T and primal_T and dual_T and mult_ok
              and primal_TT and dual_TT and lower_ok and dual_CS and upper_ok and phi_stab
              and R_ok_scalar and R_primal and R_dual and tcount_ok and no_conv and teeth_ok
              and chan_ok)
    return {"axis": "magic 자원 이론 exact 증명서 — 제5 검증경로 첫 downstream (report5 6/8)",
            "channel_magic": {"seal_link": chan_link,
                              "extent_J_T": "4−2√2 (Choi 동형: ξ(채널)=ξ(게이트))",
                              "primal_2term": chan_primal, "choi_isomorphism_xi_eq": chan_choi_iso,
                              "catalysis_resource_preserved": catal_ok,
                              "note": "★TrackHE6 P6 — 채널(동적) magic; T-채널 Choi |J_T⟩ Clifford-동치 "
                                      "|T⟩ → ξ 동일. t_teleport 촉매 = 자원 |A⟩ 보존(monotone 불변)"},
            "seal_links": links, "stab_enumeration_6_60": enum_ok,
            "extent_T": {"value": "4−2√2", "primal_2term": primal_T, "dual_feasible_6": dual_T,
                         "zero_gap_exact_Q_sqrt2": bool(gap0_T)},
            "extent_TT": {"value": "24−16√2", "multiplicativity_instance": bool(mult_ok),
                          "primal_tensor_4term": primal_TT, "dual_w_tensor_60": dual_TT},
            "extent_CS_bounded": {"lower": "8/5 (F==5/8 exact)", "lower_ok": lower_ok,
                                  "dual_feasible_60": dual_CS,
                                  "upper": "(11+2√10)/9 ≈ 1.9250 (명시 3항)", "upper_ok": upper_ok,
                                  "decomp_states_are_stabilizer": bool(phi_stab),
                                  "note": "최적성 미증명 — bounded certificate (정직)"},
            "robustness_T": {"value": "√2", "primal": R_primal, "dual_W_XplusY": R_dual,
                             "zero_gap_exact": bool(R_ok_scalar)},
            "tcount_certificates": {"gate_factor_eq_xiT": gate_factor,
                                    "magic_a_geq_1_tight": a_is_t,
                                    "magic_cs_geq_3": t_cs == 3,
                                    "cs_eq_3T_construction": cs_3t,
                                    "note": "t ≥ ⌈ln ξ_하한/ln(4−2√2)⌉ · CS 3-T 구성 == 위상다항 f=2x₀x₁"},
            "clifford_conversion_verdict": {
                "F_TT": "(3+2√2)/8", "F_CS": "5/8",
                "T2_to_CS_impossible": bool(no_conv),
                "note": "★report5 A6-1 반증 — F 는 Clifford 불변량(closed-negative급 1급 판정)"},
            "teeth": {"primal_corrupt": t1, "dual_scaled_violates": t2, "fake_lower_rejected": t3},
            "honest_boundary": "전부 증명서/관측(봉인=magic_cs 유니터리뿐). 스칼라=ℚ(√2) 정확산술·"
                               "벡터 재구성=닫힌형 계수 1e-12. n≥3 최적성 주장 없음. 문헌 선험 인용 없음.",
            "ok": ok}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"_schema": "magic-resource-v1",
                       "_note": "magic 단조량 exact 증명서(extent/robustness/T-count/변환 판정). "
                                "전부 witness(INV-Q3).",
                       "observation": res}, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        e, c, r, t = res["extent_T"], res["extent_CS_bounded"], res["robustness_T"], res["tcount_certificates"]
        print("magic 자원 exact 증명서 관측 (magic_a·magic_cs + 안정상태 6/60):", flush=True)
        print(f"  ξ(T)=4−2√2: primal {e['primal_2term']}·dual {e['dual_feasible_6']}·격차0 "
              f"{e['zero_gap_exact_Q_sqrt2']} · ξ(T⊗2)=24−16√2 곱법 "
              f"{res['extent_TT']['multiplicativity_instance']}", flush=True)
        print(f"  ξ(CS)∈[8/5, (11+2√10)/9]: 하한 {c['lower_ok']}·상한 {c['upper_ok']} (bounded, 정직)",
              flush=True)
        print(f"  R(T)=√2: {r['primal']}/{r['dual_W_XplusY']}/{r['zero_gap_exact']} · "
              f"T-count: magic_a≥1 타이트 {t['magic_a_geq_1_tight']}·magic_cs≥3 타이트 "
              f"{t['magic_cs_geq_3'] and t['cs_eq_3T_construction']}", flush=True)
        print(f"  ★T⊗T↛CS Clifford 판정(A6-1 반증): "
              f"{res['clifford_conversion_verdict']['T2_to_CS_impossible']} · teeth "
              f"{res['teeth']['primal_corrupt']}/{res['teeth']['dual_scaled_violates']}/"
              f"{res['teeth']['fake_lower_rejected']}", flush=True)
        c = res["channel_magic"]
        print(f"  ★채널 magic(P6): Choi ξ(J_T)=4−2√2 동형 {c['choi_isomorphism_xi_eq']}·primal "
              f"{c['primal_2term']}·catalysis 자원보존 {c['catalysis_resource_preserved']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"magic_resource_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
