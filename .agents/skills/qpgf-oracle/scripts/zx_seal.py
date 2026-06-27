"""zx_seal.py — Tier-3 비-Clifford(Clifford+T) 봉인 (SmallNBound 탈출 III, 통합수정설계 §5·§20).

Clifford+T는 universal — FTQC의 본령(T 게이트·magic state)이다. dense 2^n으로는 큰 회로를
검증 못 한다. ZX-calculus(pyzx)는 두 회로의 **등가를 dense 없이 증명**한다(많은 구조적 회로에서
O(다항) — 30큐비트 0.05s 실증). Tier-3는 bloq가 **독립 golden 참조회로와 등가**임을 증명하면 봉인한다.

다중전략(전부 sound — 등가를 *증명*했을 때만 봉인, 미증명은 보수적 거부, 위양성 0):
  1) ZX-calculus (pyzx full_reduce) — 기본, dense 없음, 대형 회로.
  2) dense 폴백 (소규모 n ≤ DENSE_BOUND) — cirq 유니터리 직접 비교(전역위상 무시). 결정론·항상 가용.
  3) MQT QCEC (선택) — DD+ZX+시뮬 결합. 설치 시 커버리지 확대. 'equivalent'만 수용(probably_* 거부).

★ 정직한 한계: 양자회로 등가검증은 일반적으로 QMA-hard라 **완전(complete) 해소가 수학적으로 불가능**.
다중전략은 커버리지를 넓힐 뿐, 잔여(어느 전략으로도 미증명)는 거부된다 — 이것이 이론적 상한이다.
봉인 산출물은 *어느 sound 전략이 증명했는지와 무관하게 byte-identical*(seal = "golden과 등가 증명됨",
방법 비의존). QCEC는 선택 의존성(없어도 1·2로 동작). 정확(근사 아님).
"""
import hashlib
import json
import cirq
import numpy as np
import pyzx as zx

DENSE_BOUND = 12   # n ≤ 이 값이면 dense(2^n) 폴백 비교가 싸다


def bloq_to_cirq(bloq):
    return bloq.as_composite_bloq().to_cirq_circuit()


def to_pyzx(cirq_circuit):
    return zx.Circuit.from_qasm(cirq.qasm(cirq_circuit))


def circuit_hash(zc) -> str:
    """golden 참조회로의 결정론 정준 게이트리스트 해시 (Tier-3 봉인 정체성)."""
    bg = zc.to_basic_gates()
    items = [(type(g).__name__, getattr(g, "target", None),
              getattr(g, "control", None), str(getattr(g, "phase", "")))
             for g in bg.gates]
    return hashlib.sha256(json.dumps(items, sort_keys=True).encode()).hexdigest()


def dense_equiv(cb, cg) -> bool:
    """소규모: cirq 유니터리 직접 비교(전역위상 무시, atol=1e-7 rtol=0 — C4 컨벤션).

    표준법: Ub†·Ug 가 e^{iθ}·I 이면 전역위상만 다른 동일 유니터리. (동률원소 argmax 오정렬 회피.)
    """
    Ub, Ug = cirq.unitary(cb), cirq.unitary(cg)
    if Ub.shape != Ug.shape:
        return False
    d = Ub.shape[0]
    M = Ub.conj().T @ Ug
    phase = np.trace(M) / d
    if abs(abs(phase) - 1.0) > 1e-7:
        return False
    return bool(np.allclose(M, phase * np.eye(d), atol=1e-7, rtol=0))


def qcec_equiv(cb, cg):
    """선택: MQT QCEC. 반환 True(증명 등가)/False(미증명·비등가)/None(QCEC 미가용)."""
    try:
        from mqt import qcec
    except Exception:
        return None
    import tempfile
    import os
    pb = pg = None
    try:
        pb = tempfile.NamedTemporaryFile(suffix=".qasm", delete=False)
        pb.write(cirq.qasm(cb).encode()); pb.close()
        pg = tempfile.NamedTemporaryFile(suffix=".qasm", delete=False)
        pg.write(cirq.qasm(cg).encode()); pg.close()
        r = qcec.verify(pb.name, pg.name)
        name = str(r.equivalence).rsplit(".", 1)[-1]
        return name in ("equivalent", "equivalent_up_to_global_phase")
    except Exception:
        return None
    finally:
        for p in (pb, pg):
            try:
                if p is not None:
                    os.unlink(p.name)
            except Exception:
                pass


def verify_equivalent(bloq, golden_circuit):
    """bloq ≡ golden_circuit 를 다중 sound 전략으로 증명. 반환 (ok, reason, golden_uhash, n)."""
    try:
        cb = bloq_to_cirq(bloq)
        zb = to_pyzx(cb)
        zg = to_pyzx(golden_circuit)
    except Exception as e:
        return False, f"zx_convert_fail:{e}", None, None
    if zb.qubits != zg.qubits:
        return False, f"qubit_count_mismatch: bloq {zb.qubits} ≠ golden {zg.qubits}", None, zb.qubits
    n = zb.qubits
    uhash = circuit_hash(zg)
    # 1) ZX (기본, dense 없음) — 기존 봉인 경로 불변
    try:
        if bool(zb.verify_equality(zg)):
            return True, "", uhash, n
    except Exception:
        pass
    # 2) dense 폴백 (소규모, sound·결정론)
    if n <= DENSE_BOUND:
        try:
            if dense_equiv(cb, golden_circuit):
                return True, "", uhash, n
        except Exception:
            pass
    # 3) MQT QCEC (선택, sound)
    if qcec_equiv(cb, golden_circuit) is True:
        return True, "", uhash, n
    return False, "not_equivalent (ZX/dense/QCEC 어느 전략으로도 미증명 — 보수적 거부)", None, n
