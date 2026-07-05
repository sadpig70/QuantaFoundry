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

정직 경계(INV-Q3, seal 아님, root 성장은 앱 2 봉인분뿐):
  - 봉인 = 2q 유니터리 2개뿐(정의 부분공간=자원상태 입력만 촉매 물리). 계층 판정·촉매 = 관측.
  - 측정 기반 프로토콜(Clifford-only 소비+고전 조건 보정) = magic_state_observe 기존 관측 —
    본 자산은 measurement-free coherent 판. semi-Clifford 일반론·C₄+ 탑·자원 이론 정량화 = 차기.

사용: python scripts/hierarchy_observe.py [--quick]
"""
import os, sys, re, json
from itertools import product
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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

    ok = bool(links and magic_match and cat_t and cat_s and lv_ok and ladder_ok and teeth_ok)
    return {"axis": "Clifford 계층 C₁⊂C₂⊂C₃ + measurement-free gate teleportation(촉매)",
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
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"hierarchy_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
