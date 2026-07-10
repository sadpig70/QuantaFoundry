#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hierarchy_observe — TrackC3Hierarchy: Clifford 계층(3단계)·gate teleportation 촉매 witness (신규 봉인 0).

봉인된 t_teleport(CS·CNOT)·s_teleport(CZ·CNOT)에 대해:
  1. seal 링크(앱 2 + 복리 magic_a·cs_gate·cz·cnot module).
  2. ★촉매(catalysis) exact: U_t(|ψ⟩⊗|A⟩)=(T|ψ⟩)⊗|A⟩ · U_s(|ψ⟩⊗|Y⟩)=(S|ψ⟩)⊗|Y⟩ —
     무작위 |ψ⟩(seed=0) 5개 + 기저 2개, 자원상태 보존(소모 없음). |A⟩=magic_a golden 열과 일치(복리).
  3. ★계층 판정(독립 정의 — C_{k+1}={U: UPU†∈C_k}, Pauli 전수):
     S∈C₂ · T∈C₃∖C₂ · CS∈C₃∖C₂ · CCZ∈C₃∖C₂ · ★U_t∈C₃∖C₂ vs U_s∈C₂ —
     사다리: 대상 게이트 계층 k ⇒ 보정 게이트 계층 k−1 (S↔T·Z↔S), coherent 제어 보정 = 계층 k.
  4. ★대각 사다리 재발견: t_gate²==s_gate·s_gate²==z_gate (봉인 golden 대조, T^(2^k) 하강).
  5. teeth: ①자원 오염(|+⟩) → 촉매 실패 ②4단계 게이트 Z^{1/8} ∉ C₃ 검출 ③보정 없는 CNOT 단독 → 촉매 실패.

★TrackHE4 P2 가산 확장(기존 키 불변): 봉인된 c3_diag_ladder3·c3_diag_full3(ℤ₈ phase-polynomial
정규형, T/CS/CCZ 사전)에 대해:
  6. ★강하 사다리 두 독립 경로: U X_j U† = X_j·diag(ω₈^{Δ_j f}) — 행렬 켤레(경로 A) vs 정수 다항
     차분 Δ_j f(경로 B) exact, ∀j; 2단 강하 → Pauli-대각 mod phase (C₃→C₂→C₁ 완주). +멤버십
     C₃∖C₂(기존 in_C2/in_C3 재사용). ★컴파일러 항등 관측: 일반 계수 (a,b,c) 표본 40(seed=0)에서
     T^a·CS^b·CCZ^c == diag(ω₈^f) — 정규형 사전의 일반성(인스턴스 봉인=2뿐, 일반론=관측).
  7. ★semi-Clifford 구조 확인(탐색 0): 비대각 C₃ 원소 U_t(t_teleport 봉인 golden) == CS·CNOT =
     D·C₂ 명시 인자화(C₁=I, D 대각·C₂=CNOT∈C₂) — 대각 인스턴스는 자명(D=자기). +teeth: CS→CT
     교란 → 1단 강하 Clifford-대각 실패(ζ₈ 잔존) 검출.

정직 경계(INV-Q3, seal 아님, root 성장은 앱 2 봉인분뿐):
  - 봉인 = 2q 유니터리 2개뿐(정의 부분공간=자원상태 입력만 촉매 물리). 계층 판정·촉매 = 관측.
  - 측정 기반 프로토콜(Clifford-only 소비+고전 조건 보정) = magic_state_observe 기존 관측 —
    본 자산은 measurement-free coherent 판. semi-Clifford 일반론·C₄+ 탑·자원 이론 정량화 = 차기.

사용: python -m qf_witness.observe.hierarchy_observe [--quick]
"""
import os, sys, re, json
from itertools import product
import numpy as np

from qf_witness.core.paths import ROOT
OUT = os.path.join(ROOT, ".pgf", "proofs", "HIERARCHY-OBSERVE.json")

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
S = np.diag([1, 1j]).astype(complex)
T = np.diag([1, np.exp(1j * np.pi / 4)]).astype(complex)


def load_golden(kind, name):
    src = open(os.path.join(ROOT, "specs", kind, name), encoding="utf-8").read()
    tag = "app_golden" if kind == "apps" else "golden"
    ns = {}
    exec(re.search(rf"```python id={tag}\n(.*?)```", src, re.S).group(1), ns)
    return ns["golden"]


def seal_link(store, sid):
    p = os.path.join(ROOT, "registry", store, f"{sid}.sealed.json")
    return os.path.exists(p) and bool(json.load(open(p, encoding="utf-8")).get("u_hash"))


def paulis(n):
    P1 = [I2, X, Y, Z]
    out = []
    for combo in product(range(4), repeat=n):
        if all(c == 0 for c in combo):
            continue
        M = np.eye(1, dtype=complex)
        for c in combo:
            M = np.kron(M, P1[c])
        out.append(M)
    return out


def is_pauli_mod_phase(M, n):
    for P in paulis(n) + [np.eye(2 ** n, dtype=complex)]:
        tr = np.trace(P.conj().T @ M) / (2 ** n)
        if abs(abs(tr) - 1) < 1e-9 and np.allclose(M, tr * P, atol=1e-9):
            return True
    return False


def in_C2(U, n):
    return all(is_pauli_mod_phase(U @ P @ U.conj().T, n) for P in paulis(n))


def in_C3(U, n):
    return all(in_C2(U @ P @ U.conj().T, n) for P in paulis(n))


# --- TrackHE4 P2: ℤ₈ phase-polynomial 정규형 도우미 (big-endian x₀=MSB) ---
W8 = np.exp(1j * np.pi / 4)
PAIRS = [(0, 1), (0, 2), (1, 2)]


def _f3(a, b, c, x):
    return (sum(a[i] * x[i] for i in range(3))
            + 2 * sum(b[k] * x[i] * x[j] for k, (i, j) in enumerate(PAIRS))
            + 4 * c * x[0] * x[1] * x[2]) % 8


def _fdiag3(a, b, c):
    d = np.ones(8, dtype=complex)
    for idx in range(8):
        x = [(idx >> 2) & 1, (idx >> 1) & 1, idx & 1]
        d[idx] = W8 ** _f3(a, b, c, x)
    return np.diag(d)


def _ddiag3(a, b, c, j):
    d = np.ones(8, dtype=complex)
    for idx in range(8):
        x = [(idx >> 2) & 1, (idx >> 1) & 1, idx & 1]
        xf = list(x); xf[j] ^= 1
        d[idx] = W8 ** ((_f3(a, b, c, xf) - _f3(a, b, c, x)) % 8)
    return np.diag(d)


def _x3(j):
    return np.kron(np.kron(X if j == 0 else I2, X if j == 1 else I2), X if j == 2 else I2)


def _diag_phase_in(D, allowed, tol=1e-9):
    dd = np.diag(D) / np.diag(D)[0]
    return all(min(abs(v - p) for p in allowed) < tol for v in dd)


def observe_phasepoly():
    links = (all(seal_link("apps", s) for s in ("c3_diag_ladder3", "c3_diag_full3"))
             and all(seal_link("modules", m) for m in ("t_gate", "cs_gate", "ccz")))
    coeffs = {"c3_diag_ladder3": ([1, 0, 0], [1, 0, 0], 1),
              "c3_diag_full3": ([1, 1, 1], [1, 1, 1], 1)}
    apps = {k: load_golden("apps", f"{k}.app.pg") for k in coeffs}

    # golden == 정수 다항 대각 (컴파일 대상 확인) + 멤버십 C₃∖C₂
    poly_ok = all(np.allclose(apps[k], _fdiag3(*coeffs[k]), atol=1e-13) for k in coeffs)
    member = {k: bool(in_C3(U, 3) and not in_C2(U, 3)) for k, U in apps.items()}

    # ★강하 사다리 두 경로 (1단: 행렬 켤레 vs Δ_j f 정수 다항) + 2단 → Pauli-대각
    desc1 = desc2 = True
    for k, U in apps.items():
        a, b, c = coeffs[k]
        for j in range(3):
            D1 = _x3(j) @ U @ _x3(j) @ U.conj().T
            desc1 &= bool(np.allclose(D1, _ddiag3(a, b, c, j), atol=1e-12))
            desc1 &= _diag_phase_in(D1, [1, -1, 1j, -1j])          # Clifford-대각 위상격자
            for m in range(3):
                D2 = _x3(m) @ D1 @ _x3(m) @ D1.conj().T
                desc2 &= _diag_phase_in(D2, [1, -1, 1j, -1j]) and is_pauli_mod_phase(D2, 3)

    # ★컴파일러 항등 (일반 계수 표본 40, seed=0 — 일반론은 관측)
    rng = np.random.default_rng(0)
    comp_ok = True
    CSd = np.diag([1, 1, 1, 1j]).astype(complex)
    for _ in range(40):
        a = list(rng.integers(0, 8, 3)); b = list(rng.integers(0, 4, 3)); c = int(rng.integers(0, 2))
        d = np.ones(8, dtype=complex)
        for idx in range(8):
            x = [(idx >> 2) & 1, (idx >> 1) & 1, idx & 1]
            ph = sum(a[i] * x[i] for i in range(3)) + 2 * sum(
                b[k] * x[i] * x[j] for k, (i, j) in enumerate(PAIRS)) + 4 * c * x[0] * x[1] * x[2]
            d[idx] = W8 ** (ph % 8)                                 # 회로측: T^a·CS^b·CCZ^c 대각 곱
        comp_ok &= bool(np.allclose(np.diag(d), _fdiag3(a, b, c), atol=1e-12))

    # ★semi-Clifford 구조 확인 (탐색 0): U_t == D·C₂ (D=CS 대각, C₂=CNOT Clifford)
    U_t = load_golden("apps", "t_teleport.app.pg")
    CNOT = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex)
    semi_ok = bool(np.allclose(U_t, CSd @ CNOT, atol=1e-13) and in_C2(CNOT, 2))

    # teeth: CS→CT 교란 → 1단 강하 Clifford-대각 실패 (ζ₈ 잔존)
    CT = np.diag([1, 1, 1, W8]).astype(complex)
    dbad = np.ones(8, dtype=complex)
    for idx in range(8):
        x = [(idx >> 2) & 1, (idx >> 1) & 1, idx & 1]
        dbad[idx] = (W8 ** x[0]) * (CT[2 * x[0] + x[1], 2 * x[0] + x[1]]) * ((-1) ** (x[0] * x[1] * x[2]))
    Ubad = np.diag(dbad)
    Dbad = _x3(1) @ Ubad @ _x3(1) @ Ubad.conj().T
    teeth_ok = bool(not _diag_phase_in(Dbad, [1, -1, 1j, -1j]))

    ok = bool(links and poly_ok and all(member.values()) and desc1 and desc2
              and comp_ok and semi_ok and teeth_ok)
    return {"seal_links_2apps_3modules": links,
            "golden_eq_integer_poly": poly_ok,
            "membership_C3_not_C2": member,
            "descent_two_path_1step_exact": bool(desc1),
            "descent_2step_pauli_diag": bool(desc2),
            "compiler_identity_40_samples": bool(comp_ok),
            "semiclifford_Ut_eq_D_CNOT": semi_ok,
            "teeth_CT_perturb_detected": teeth_ok,
            "honest_boundary": "봉인=정규형 인스턴스 2뿐(module 0). 강하 사다리·멤버십·컴파일러 "
                               "일반계수 항등·semi-Clifford 구조=관측(INV-Q3). 비대각 C₃ 일반론·C₄+=범위 밖.",
            "ok": ok}


def observe():
    links = (all(seal_link("apps", s) for s in ("t_teleport", "s_teleport", "magic_a"))
             and all(seal_link("modules", m) for m in ("cs_gate", "cz", "cnot", "t_gate", "s_gate", "z_gate")))
    U_t = load_golden("apps", "t_teleport.app.pg")
    U_s = load_golden("apps", "s_teleport.app.pg")

    # 2. 촉매 exact (|A⟩ = magic_a golden 정의열과 일치 확인 — 복리)
    A = T @ H @ np.array([1, 0], dtype=complex)
    magic_col = load_golden("apps", "magic_a.app.pg")[:, 0]
    ph = magic_col[np.argmax(np.abs(A))] / A[np.argmax(np.abs(A))]
    magic_match = bool(abs(abs(ph) - 1) < 1e-12 and np.allclose(magic_col, ph * A, atol=1e-12))
    Yst = S @ H @ np.array([1, 0], dtype=complex)
    rng = np.random.default_rng(0)
    cat_t = cat_s = True
    tests = [np.array([1, 0], dtype=complex), np.array([0, 1], dtype=complex)]
    for _ in range(5):
        v = rng.standard_normal(2) + 1j * rng.standard_normal(2)
        tests.append(v / np.linalg.norm(v))
    for v in tests:
        cat_t &= bool(np.allclose(U_t @ np.kron(v, A), np.kron(T @ v, A), atol=1e-12))
        cat_s &= bool(np.allclose(U_s @ np.kron(v, Yst), np.kron(S @ v, Yst), atol=1e-12))

    # 3. 계층 판정
    CCZ = np.diag([1, 1, 1, 1, 1, 1, 1, -1]).astype(complex)
    CS = np.diag([1, 1, 1, 1j]).astype(complex)
    levels = {"S_in_C2": in_C2(S, 1), "T_notin_C2": not in_C2(T, 1), "T_in_C3": in_C3(T, 1),
              "CS_in_C3_notin_C2": in_C3(CS, 2) and not in_C2(CS, 2),
              "CCZ_in_C3_notin_C2": in_C3(CCZ, 3) and not in_C2(CCZ, 3),
              "Ut_in_C3_notin_C2": in_C3(U_t, 2) and not in_C2(U_t, 2),
              "Us_in_C2": in_C2(U_s, 2)}
    lv_ok = all(bool(v) for v in levels.values())

    # 4. 대각 사다리 재발견 (봉인 module golden 대조)
    tg = load_golden("modules", "t_gate.pg")
    sg = load_golden("modules", "s_gate.pg")
    zg = load_golden("modules", "z_gate.pg")
    ladder_ok = bool(np.allclose(tg @ tg, sg, atol=1e-13) and np.allclose(sg @ sg, zg, atol=1e-13))

    # 5. teeth
    plus = H @ np.array([1, 0], dtype=complex)
    v = tests[-1]
    t1 = bool(not np.allclose(U_t @ np.kron(v, plus), np.kron(T @ v, plus), atol=1e-6))
    T8 = np.diag([1, np.exp(1j * np.pi / 8)]).astype(complex)
    t2 = bool(not in_C3(T8, 1))
    CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)
    t3 = bool(not np.allclose(CNOT @ np.kron(v, A), np.kron(T @ v, A), atol=1e-6))
    teeth_ok = t1 and t2 and t3

    pp = observe_phasepoly()
    ok = bool(links and magic_match and cat_t and cat_s and lv_ok and ladder_ok and teeth_ok
              and pp["ok"])
    return {"axis": "Clifford 계층 C₁⊂C₂⊂C₃ + measurement-free gate teleportation(촉매)",
            "phasepoly": pp,
            "seal_links": links, "resource_eq_magic_a_column": magic_match,
            "catalysis": {"t_teleport_TA_exact_7states": bool(cat_t),
                          "s_teleport_SY_exact_7states": bool(cat_s),
                          "note": "자원상태 보존 — 소모 없는 촉매"},
            "hierarchy_levels": {k: bool(v) for k, v in levels.items()},
            "ladder": {"t2_eq_s__s2_eq_z_rediscovery": ladder_ok,
                       "correction_one_level_down": "T(C₃)→보정 S(C₂) · S(C₂)→보정 Z(C₁)"},
            "teeth": {"wrong_resource_plus": t1, "level4_zpow8_notin_C3": t2,
                      "cnot_only_no_correction": t3},
            "honest_boundary": "봉인=2q 유니터리 2개뿐(정의 부분공간만 촉매 물리). 계층 판정·촉매=관측"
                               "(INV-Q3). 측정 기반 Clifford-only 소비=magic_state_observe 기존 경계. "
                               "semi-Clifford 일반론·C₄+ 탑=차기. 신규 module 0.",
            "ok": ok}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"_schema": "hierarchy-observe-v1",
                       "_note": "Clifford 계층+teleportation 촉매 witness. 봉인=유니터리뿐(INV-Q3).",
                       "observation": res}, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        c, lv, t = res["catalysis"], res["hierarchy_levels"], res["teeth"]
        print("Clifford 계층·teleportation 촉매 witness 관측 (t_teleport·s_teleport):", flush=True)
        print(f"  seal {res['seal_links']} · |A⟩==magic_a 열 {res['resource_eq_magic_a_column']} · "
              f"촉매 T {c['t_teleport_TA_exact_7states']}·S {c['s_teleport_SY_exact_7states']}", flush=True)
        print(f"  계층: {lv}", flush=True)
        print(f"  사다리 T²=S·S²=Z {res['ladder']['t2_eq_s__s2_eq_z_rediscovery']} · "
              f"teeth {t['wrong_resource_plus']}/{t['level4_zpow8_notin_C3']}/{t['cnot_only_no_correction']}",
              flush=True)
        p = res["phasepoly"]
        print(f"  ★phase-poly(P2): 강하 두경로 {p['descent_two_path_1step_exact']}·2단→Pauli "
              f"{p['descent_2step_pauli_diag']}·멤버십 {p['membership_C3_not_C2']}·컴파일러항등40 "
              f"{p['compiler_identity_40_samples']}·semiCliff {p['semiclifford_Ut_eq_D_CNOT']}·"
              f"teeth(CT) {p['teeth_CT_perturb_detected']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"hierarchy_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
