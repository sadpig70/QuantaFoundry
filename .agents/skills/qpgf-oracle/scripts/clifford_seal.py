"""clifford_seal.py — Tier-2 Clifford 기호 봉인 (SmallNBound 탈출 II, 통합수정설계 §5).

Clifford 회로(H·S·CNOT·CZ·X·Y·Z·SWAP)는 **stabilizer tableau**로 O(n²)에 정준화된다 —
dense 2^n 유니터리 없이 임의 크기를 *정확*(근사 아님) 봉인 가능. QEC 인코더·신드롬추출·
logical Clifford 게이트가 대부분 Clifford → SmallNBound 탈출 범위가 극적으로 넓어진다.

경계: 검증은 결정론 코드(cirq stabilizer)로 — QPGF는 게이트만. 비-Clifford(T/Toffoli 포함)는
이 경로 밖(Tier-0 dense 소규모 / Tier-3 DD·ZX 후속).

봉인 정체성: 정준 tableau는 Clifford 유니터리를 전역위상 무시 *유일하게* 결정 → 그 해시가
"이 Clifford 연산"의 결정론 지문(u_hash). dense u_hash와는 표현이 달라 일치하지 않는다(tier 구분).
"""
import hashlib
import numpy as np
import cirq


def to_cirq_circuit(bloq):
    return bloq.as_composite_bloq().to_cirq_circuit()


def is_clifford(bloq):
    """bloq의 모든 게이트가 Clifford인가. 반환 (bool, reason)."""
    try:
        circ = to_cirq_circuit(bloq)
    except Exception as e:
        return False, f"cirq_convert_fail:{e}"
    for op in circ.all_operations():
        if not cirq.has_stabilizer_effect(op):
            return False, f"non_clifford_gate:{op.gate}"
    return True, ""


def canonical_tableau_hash(bloq):
    """Clifford bloq → 정준 stabilizer tableau의 sha256 (dense 미사용). 반환 (hash, n_qubits)."""
    circ = to_cirq_circuit(bloq)
    qubits = sorted(circ.all_qubits())          # 결정론 큐비트 순서
    n = len(qubits)
    state = cirq.CliffordTableauSimulationState(
        tableau=cirq.CliffordTableau(num_qubits=n), qubits=qubits)
    for op in circ.all_operations():
        cirq.act_on(op, state)
    t = state.tableau
    h = hashlib.sha256()
    h.update(repr((n,)).encode())
    h.update(np.ascontiguousarray(t.matrix()).tobytes())   # 2n×2n 심플렉틱
    h.update(np.ascontiguousarray(np.asarray(t.rs)).tobytes())  # 위상
    return h.hexdigest(), n


def dense_unitary(bloq):
    """소규모 advisory용: cirq 회로의 dense 유니터리 (2^n — 소규모만)."""
    return cirq.unitary(to_cirq_circuit(bloq))
