#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""maj_observe — TrackHE7 P2: 4-Majorana braiding 구조 관측 witness (§3i "아직 없음" 축 개창).

봉인된 braid-word 앱(maj_braid_ybe) + 기봉인 bogoliubov_pair 위에서 Majorana braid 표현의
대수적/위상적 성질을 관측(오라클 독립, dense 심볼릭):
  JW 2큐빗 4-Majorana: γ1=X⊗I, γ2=Y⊗I, γ3=Z⊗X, γ4=Z⊗Y. braid B_ij=exp(π/4·γ_iγ_j)=(I+γ_iγ_j)/√2.
  1. Majorana 대수 {γi,γj}=2δij (정준 반교환).
  2. ★봉인 전 선검증이 반증한 것(정직): 개별 braid·braid word 전부 **Clifford**(π/4 quadratic Majorana)
     — 외부 제안의 "braid word=non-Clifford matchgate" 주장은 거짓. Majorana braiding ⊂ Clifford.
  3. Majorana conjugation: B_ij γ_k B_ij† = ±γ_l (braid = SO(4) 부호순열 — 제6 matchgate 경로 정합).
  4. Yang-Baxter(braid 관계): B12·B23·B12 == B23·B12·B23 (up-to-phase).
  5. §4′(f) 동치 재발견: B_23 = exp(iπ/4·X⊗X) == 기봉인 bogoliubov_pair (γ2γ3 = i·X⊗X).
  6. 4-Majorana 위상큐빗: fermion parity P=γ1γ2γ3γ4 = −Z⊗Z, 두 parity 섹터 = 논리 큐빗.
  7. 비아벨성: [B12,B23] ≠ 0.

정직 경계(INV-Q3, seal 아님, root 불변): 봉인 = maj_braid_ybe 회로 == golden exact(Clifford)뿐.
  위상 보호·에너지 갭·실제 Majorana 물리·anyon 통계 = 관측/범위 밖. non-Clifford universality
  없음(Ising anyon = Clifford only, 정직). braid word 는 기봉인 primitive(S/bogoliubov/CNOT·H·CNOT)로
  환원 — 새 게이트 불요(정수-Clifford 닫힌 영역). 신규 module 0.

사용: python scripts/maj_observe.py [--quick]
"""
import os, sys, re, itertools
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)


def kron(*a):
    r = a[0]
    for m in a[1:]:
        r = np.kron(r, m)
    return r


G = {1: kron(X, I), 2: kron(Y, I), 3: kron(Z, X), 4: kron(Z, Y)}   # JW 4-Majorana


def braid(i, j):
    return (np.eye(4) + G[i] @ G[j]) / np.sqrt(2)


def word(seq):
    U = np.eye(4, dtype=complex)
    for (i, j) in seq:
        U = braid(i, j) @ U
    return U


def phase_eq(U, V):
    idx = int(np.argmax(np.abs(V.flatten())))
    r = U.flatten()[idx] / V.flatten()[idx]
    return bool(abs(abs(r) - 1) < 1e-9 and np.allclose(U, r * V, atol=1e-9))


def _paulis():
    return [kron(a, b) for a, b in itertools.product([I, X, Y, Z], repeat=2)]


def is_clifford(U):
    P = _paulis()
    for p in P:
        C = U @ p @ U.conj().T
        if not any(np.allclose(C, ph * q, atol=1e-9) for q in P for ph in (1, -1, 1j, -1j)):
            return False
    return True


def _load_app_golden(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    m = re.search(r"```python id=app_golden\n(.*?)```", src, re.S)
    ns = {}
    exec(m.group(1), ns)
    return ns["golden"]


def main():
    quick = "--quick" in sys.argv
    R = {}

    # 1. Majorana 대수
    R["majorana_algebra"] = all(
        np.allclose(G[i] @ G[j] + G[j] @ G[i], 2 * (i == j) * np.eye(4))
        for i in G for j in G)

    # 2. 개별 braid·word 전부 Clifford (선검증 반증 기록)
    all_clifford = all(is_clifford(braid(i, j)) for i, j in [(1, 2), (2, 3), (3, 4), (1, 3), (1, 4), (2, 4)])
    all_clifford &= is_clifford(word([(1, 2), (2, 3), (1, 2)]))
    all_clifford &= is_clifford(word([(2, 3), (3, 4), (2, 3)]))
    R["braids_all_clifford"] = bool(all_clifford)

    # 3. Majorana conjugation = SO(4) 부호순열
    def conj_signed_perm(B):
        for k in range(1, 5):
            C = B @ G[k] @ B.conj().T
            if not any(np.allclose(C, s * G[l], atol=1e-9) for l in range(1, 5) for s in (1, -1)):
                return False
        return True
    R["so4_signed_perm"] = all(conj_signed_perm(braid(i, j)) for i, j in [(1, 2), (2, 3), (3, 4)])

    # 4. Yang-Baxter
    R["yang_baxter"] = phase_eq(word([(1, 2), (2, 3), (1, 2)]), word([(2, 3), (1, 2), (2, 3)]))

    # 5. §4′(f): B_23 == bogoliubov_pair
    bog = _load_app_golden("bogoliubov_pair.app.pg")
    R["b23_eq_bogoliubov"] = phase_eq(braid(2, 3), bog)

    # 6. 4-Majorana 위상큐빗 parity
    P = G[1] @ G[2] @ G[3] @ G[4]
    R["parity_minus_ZZ"] = bool(np.allclose(P, -kron(Z, Z)))

    # 7. 비아벨
    R["non_abelian"] = bool(not np.allclose(braid(1, 2) @ braid(2, 3), braid(2, 3) @ braid(1, 2)))

    # 8. 봉인 braid-word 앱 검증 (있으면): maj_braid_ybe == B12·B23·B12
    try:
        gy = _load_app_golden("maj_braid_ybe.app.pg")
        R["ybe_app_matches_braid_word"] = phase_eq(gy, word([(1, 2), (2, 3), (1, 2)]))
    except Exception:
        R["ybe_app_matches_braid_word"] = None

    ok = all(v for k, v in R.items() if v is not None)
    if not quick:
        print("4-Majorana braiding 구조 관측 (§3i 축 개창, witness — seal 아님):", flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  ★정직: 모든 braid=Clifford(외부 non-Clifford 주장 선검증 반증)·B23=bogoliubov(§4′f)·"
              "위상보호/anyon 물리=관측·신규 module 0·root 불변", flush=True)
    print(f"maj_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
