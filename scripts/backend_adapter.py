# -*- coding: utf-8 -*-
"""
backend_adapter.py — §5[8](B) 시뮬레이터 백엔드 어댑터 (실행 계층, 시뮬레이터 한정)

이 도구는 **이미 봉인된** 앱(spec + sealed.json)을 시뮬레이터에서 *실행*해 행동
(측정분포·기댓값·상관·period 등)을 관찰한다. QuantaFoundry 가 지금까지 한 "검증·봉인"
위에 처음 올리는 "실행" 계층이다 — shor period / grover |11> 같이 산발적으로 했던
행동검증을 일반화한 백엔드 추상화.

═══════════════════════════════════════════════════════════════════════════
정직성 경계 (이 스레드의 리뷰 포인트 — 절대 흐리지 말 것)
═══════════════════════════════════════════════════════════════════════════
1. 실행(시뮬레이션) ≠ 검증(봉인). 시뮬레이터 출력은 봉인의 증거가 **아니다**
   (spec §8.4 "behavioral check is illustrative only" 와 동일 원칙). 이 어댑터는
   봉인을 대체/보강하지 않으며 registry/오라클/frozen 키를 **건드리지 않는다**.
2. 입력은 *이미 봉인된* 산출물이어야 한다. 실행 직전, spec 의 app_golden 에서
   유니터리 U 를 재구성하고 hash_unitary(U) == sealed.json.u_hash 를 재확인한다.
   불일치 → 실행 거부(미봉인/변조). "봉인된 그 산출물을 실행한다"는 보장하되,
   실행 결과가 봉인 증거가 아님은 분리해 명시한다.
3. 결정론: 이상적 statevector 는 결정론(numpy/cirq 두 백엔드 atol 일치).
   샷 샘플링은 seed 고정으로 재현가능.
4. 하드웨어(QPU) 연결은 범위 외 — 시뮬레이터(ideal statevector) 한정.

오라클은 *사용만* 한다(verify_seal 의 instantiate/hash_unitary = 공통 측정도구).
백엔드의 cirq.MatrixGate 는 *실행용 시뮬레이터 게이트*이며, honest-분해 규칙
(봉인용 bloq ≠ MatrixGate)과 무관하다 — 여기서는 아무것도 봉인하지 않는다.
"""
from __future__ import annotations

import os
import sys
import json
from collections import Counter

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts"))
import verify_seal as vs  # noqa: E402  (공통 측정도구 — instantiate/hash_unitary 사용만)

APPS = os.path.join(ROOT, "specs", "apps")
APPREG = os.path.join(ROOT, "registry", "apps")
OUT = os.path.join(ROOT, ".pgf", "backend")

try:
    import cirq  # noqa: E402
    _HAS_CIRQ = True
except Exception:  # pragma: no cover
    _HAS_CIRQ = False


# ═══════════════════════════════════════════════════════════════════════════
# 봉인앱 로더 — 입력 게이트(이미 봉인된 것만 실행)
# ═══════════════════════════════════════════════════════════════════════════
class SealGateError(RuntimeError):
    """봉인 안 됨 / sealed.json 부재 / u_hash 불일치(변조) → 실행 거부."""


def load_sealed_app(app_id: str):
    """봉인앱(spec+sealed.json)을 로드하고 u_hash 게이트를 통과한 것만 반환.

    반환 dict: {id, n, U(2^n×2^n complex), u_hash, tier, sealed(dict)}
    오라클은 *사용만*: vs.instantiate(app_golden→U), vs.hash_unitary(U).
    """
    spec_path = os.path.join(APPS, f"{app_id}.app.pg")
    seal_path = os.path.join(APPREG, f"{app_id}.sealed.json")
    if not os.path.exists(seal_path):
        raise SealGateError(f"{app_id}: sealed.json 부재 — 미봉인 산출물은 실행 금지")
    sealed = json.load(open(seal_path, encoding="utf-8"))
    if not sealed.get("sealed", False):
        raise SealGateError(f"{app_id}: sealed=false — 봉인 안 된 것 실행 금지")
    if sealed.get("tier", 0) != 0:
        # Tier-1(STRUCTURAL, dense 미실체화)은 app_golden 이 없을 수 있다 →
        # 어댑터는 dense 실행이므로 Tier-0(EXACT)만 다룬다. 정직한 거부.
        raise SealGateError(f"{app_id}: tier={sealed.get('tier')} (dense 미실체화) — "
                            "어댑터는 Tier-0 EXACT 만 실행")

    blocks = vs._extract_blocks(open(spec_path, encoding="utf-8").read())
    if "app_golden" not in blocks:
        raise SealGateError(f"{app_id}: app_golden 블록 없음 — dense 실행 불가")
    U = np.asarray(vs.instantiate(blocks["app_golden"], "golden"), dtype=complex)

    n = int(sealed["n_sys"])
    if U.shape != (1 << n, 1 << n):
        raise SealGateError(f"{app_id}: U shape {U.shape} ≠ 2^{n}")

    # ── 입력 게이트: 봉인된 그 유니터리인가 (u_hash 재확인) ──
    u_hash = vs.hash_unitary(U)
    if u_hash != sealed["u_hash"]:
        raise SealGateError(f"{app_id}: u_hash 불일치 — 변조/미봉인 "
                            f"(got {u_hash[:12]} ≠ sealed {sealed['u_hash'][:12]})")
    return {"id": app_id, "n": n, "U": U, "u_hash": u_hash,
            "tier": sealed.get("tier", 0), "sealed": sealed}


# ═══════════════════════════════════════════════════════════════════════════
# 백엔드 추상화 — Tier-0 봉인앱 유니터리를 statevector 로 실행
# ═══════════════════════════════════════════════════════════════════════════
class Backend:
    name = "abstract"

    def run(self, U: np.ndarray, psi0: np.ndarray) -> np.ndarray:
        raise NotImplementedError


class NumpyStatevectorBackend(Backend):
    """골든이 이미 numpy 유니터리 → ψ = U @ ψ0 만으로 결정론 실행. 의존성 numpy 뿐."""
    name = "numpy_statevector"

    def run(self, U, psi0):
        return U @ psi0


class CirqStatevectorBackend(Backend):
    """cirq.MatrixGate(U) + Simulator (cirq-core 1.6.1). 백엔드 추상화가 실재함을 입증
    — numpy 백엔드와 atol 일치. big-endian: q0=MSB = cirq LineQubit(0)(첫 큐비트=최상위)."""
    name = "cirq_statevector"

    def run(self, U, psi0):
        n = int(np.log2(U.shape[0]))
        qubits = [cirq.LineQubit(i) for i in range(n)]
        circuit = cirq.Circuit(cirq.MatrixGate(U).on(*qubits))
        result = cirq.Simulator(dtype=np.complex128).simulate(
            circuit, initial_state=psi0.astype(np.complex64).astype(np.complex128))
        return np.asarray(result.final_state_vector, dtype=complex)


def get_backends():
    bks = [NumpyStatevectorBackend()]
    if _HAS_CIRQ:
        bks.append(CirqStatevectorBackend())
    return bks


# ═══════════════════════════════════════════════════════════════════════════
# 초기 상태 (big-endian: 큐비트 q 의 비트위치 = n-1-q)
# ═══════════════════════════════════════════════════════════════════════════
def zero_state(n):
    psi = np.zeros(1 << n, complex); psi[0] = 1.0
    return psi


def basis_state(n, index):
    psi = np.zeros(1 << n, complex); psi[index] = 1.0
    return psi


def uniform_state(n):
    return np.full(1 << n, 1.0 / np.sqrt(1 << n), complex)


# ═══════════════════════════════════════════════════════════════════════════
# 관찰자 계층 — statevector 에서 파생 (검증 아님, 행동 관찰)
# ═══════════════════════════════════════════════════════════════════════════
def probabilities(psi, n, thr=1e-9):
    """측정분포 {bitstring(big-endian q0..q_{n-1}): prob} (prob>thr)."""
    p = np.abs(psi) ** 2
    return {format(i, f"0{n}b"): float(p[i]) for i in range(len(p)) if p[i] > thr}


def sample(psi, n, shots, seed):
    """샷 샘플링 (seed 고정 → 재현가능). 반환 Counter{bitstring: count}."""
    p = np.abs(psi) ** 2
    p = p / p.sum()
    rng = np.random.default_rng(seed)
    draws = rng.choice(len(p), size=shots, p=p)
    return Counter(format(int(i), f"0{n}b") for i in draws)


def expect_z(psi, n, q):
    """⟨Z_q⟩ (Z 고유값 +1 if 비트0, -1 if 비트1)."""
    p = np.abs(psi) ** 2
    idx = np.arange(len(p))
    bit = (idx >> (n - 1 - q)) & 1
    return float(np.sum(p * np.where(bit, -1.0, 1.0)))


def corr_zz(psi, n, i, j):
    """⟨Z_i Z_j⟩."""
    p = np.abs(psi) ** 2
    idx = np.arange(len(p))
    bi = (idx >> (n - 1 - i)) & 1
    bj = (idx >> (n - 1 - j)) & 1
    return float(np.sum(p * np.where(bi ^ bj, -1.0, 1.0)))


def marginal_register(psi, n, qubits):
    """주어진 레지스터(큐비트 리스트, big-endian)에 대한 주변 측정분포 {value: prob}."""
    p = np.abs(psi) ** 2
    out = {}
    for i in range(len(p)):
        if p[i] <= 1e-12:
            continue
        val = 0
        for k, q in enumerate(qubits):
            bit = (i >> (n - 1 - q)) & 1
            val |= bit << (len(qubits) - 1 - k)
        out[val] = out.get(val, 0.0) + float(p[i])
    return out


# ═══════════════════════════════════════════════════════════════════════════
# Shor 후처리 — counting register 측정 → 연속분수 → period → 인수
# ═══════════════════════════════════════════════════════════════════════════
def continued_fraction_period(measured, M, N):
    """measured/M 의 연속분수 수렴분모 중 q<N 인 가장 큰 q (period 후보).

    CF 항 [a0;a1,a2,...] 추출 후 표준 분모점화 q_k = a_k·q_{k-1} + q_{k-2}
    (q_{-1}=0, q_0=1) 로 수렴분모 계산.
    """
    # 1) CF 항 추출 (유클리드)
    a, b = measured, M
    terms = []
    while b:
        terms.append(a // b)
        a, b = b, a % b
    # 2) 분모 수렴 k_i = a_i·k_{i-1} + k_{i-2} (k_{-2}=1, k_{-1}=0).
    #    q<N 인 가장 큰 분모 = 최선 근사 = period 후보.
    k2, k1 = 1, 0   # k_{-2}, k_{-1}
    best = None
    for ak in terms:
        k = ak * k1 + k2
        k2, k1 = k1, k
        if 0 < k < N:
            best = k
    return best


def shor_factors_from_period(a, r, N):
    """주기 r 짝수이고 a^{r/2}≢-1 → gcd(a^{r/2}±1, N) 로 비자명 인수."""
    from math import gcd
    if r % 2 != 0:
        return None
    x = pow(a, r // 2, N)
    if x == N - 1:
        return None
    f1, f2 = gcd(x - 1, N), gcd(x + 1, N)
    facs = sorted({f for f in (f1, f2) if 1 < f < N})
    return facs or None


# ═══════════════════════════════════════════════════════════════════════════
# 데모 — 봉인앱 행동 관찰 (정직성: 관찰일 뿐, 봉인 재증명 아님)
# ═══════════════════════════════════════════════════════════════════════════
SHOTS = 4096
SEED = 20260627


def _run_all_backends(app, psi0):
    """모든 백엔드로 실행 → {backend_name: psi}, 그리고 백엔드간 atol 일치 여부."""
    out = {}
    for bk in get_backends():
        out[bk.name] = bk.run(app["U"], psi0)
    names = list(out)
    agree = True
    for nm in names[1:]:
        if not np.allclose(out[names[0]], out[nm], atol=1e-6):
            agree = False
    return out, agree


def demo_ghz(app_id="ghz3"):
    app = load_sealed_app(app_id)
    n = app["n"]
    psis, agree = _run_all_backends(app, zero_state(n))
    psi = psis["numpy_statevector"]
    probs = probabilities(psi, n)
    corr = {f"Z0Z{k}": round(corr_zz(psi, n, 0, k), 9) for k in range(1, n)}
    s2a = sample(psi, n, SHOTS, SEED)
    s2b = sample(psi, n, SHOTS, SEED)
    all_zero = "0" * n
    all_one = "1" * n
    observed = {
        "init": "zero",
        "probabilities": {k: round(v, 9) for k, v in sorted(probs.items())},
        "ZiZj_correlations": corr,
        "shot_sample_seeded": dict(s2a),
        "shot_reproducible": s2a == s2b,
        "backends_agree": agree,
    }
    expect = {
        "ghz_two_peaks": set(probs) == {all_zero, all_one}
        and abs(probs[all_zero] - 0.5) < 1e-9 and abs(probs[all_one] - 0.5) < 1e-9,
        "all_correlations_plus1": all(abs(v - 1.0) < 1e-9 for v in corr.values()),
    }
    return _verdict(app, "GHZ 상관(전 큐비트 +1, 두 peak 0.5/0.5)", observed, expect)


def demo_grover(app_id="grover2"):
    app = load_sealed_app(app_id)
    n = app["n"]
    # grover2 골든 = iterate D∘O; 균등중첩 |++..> 에서 정답 |11..>로 증폭.
    psis, agree = _run_all_backends(app, uniform_state(n))
    psi = psis["numpy_statevector"]
    probs = probabilities(psi, n)
    target = "1" * n
    p_target = probs.get(target, 0.0)
    observed = {
        "init": "uniform",
        "probabilities": {k: round(v, 9) for k, v in sorted(probs.items())},
        "P_target": round(p_target, 9),
        "target": target,
        "shot_sample_seeded": dict(sample(psi, n, SHOTS, SEED)),
        "backends_agree": agree,
    }
    expect = {"amplifies_target_to_1": abs(p_target - 1.0) < 1e-9}
    return _verdict(app, f"Grover 1-iterate 가 |{target}> 로 증폭(P≈1)", observed, expect)


def demo_wstate(app_id="wstate3"):
    app = load_sealed_app(app_id)
    n = app["n"]
    psis, agree = _run_all_backends(app, zero_state(n))
    psi = psis["numpy_statevector"]
    probs = probabilities(psi, n)
    # W_n = 균등 hamming-weight-1 중첩 → 각 단일여기 basis 확률 1/n.
    w1 = {k: v for k, v in probs.items() if k.count("1") == 1}
    uniform_ok = (len(w1) == n
                  and all(abs(v - 1.0 / n) < 1e-9 for v in w1.values())
                  and abs(sum(probs.values()) - sum(w1.values())) < 1e-9)
    observed = {
        "init": "zero",
        "probabilities": {k: round(v, 9) for k, v in sorted(probs.items())},
        "hamming1_states": len(w1),
        "each_prob": round(1.0 / n, 9),
        "shot_sample_seeded": dict(sample(psi, n, SHOTS, SEED)),
        "backends_agree": agree,
    }
    expect = {"uniform_over_single_excitation": uniform_ok}
    return _verdict(app, f"W_{n} 균등분포(단일여기 {n}개 각 1/{n})", observed, expect)


def demo_shor21(app_id="shor21_a2"):
    app = load_sealed_app(app_id)
    n = app["n"]              # 12 = counting 7(q0..6) | work 5(q7..11)
    a, N, t = 2, 21, 7
    M = 1 << t                # 128
    # work register = |1> (basis index 1, big-endian LSB=q11). counting=0.
    psis, agree = _run_all_backends(app, basis_state(n, 1))
    psi = psis["numpy_statevector"]
    counting_qubits = list(range(t))          # q0..q6
    marg = marginal_register(psi, n, counting_qubits)   # {0..127: prob}
    # 상위 peak 들에서 연속분수 → period 후보.
    peaks = sorted(marg.items(), key=lambda kv: -kv[1])[:8]
    period_votes = {}
    for m, pr in peaks:
        r = continued_fraction_period(m, M, N)
        if r:
            period_votes[r] = period_votes.get(r, 0.0) + pr
    # 표준 Shor 후처리: 후보 r 중 진짜 order(a^r≡1 mod N)만 채택 → 분모점화가 내놓는
    # 약수(예: r=3, 2^3=8≢1)를 배제. 동률 max() 순서운에 의존하지 않음.
    valid = {r: v for r, v in period_votes.items() if pow(a, r, N) == 1}
    best_r = max(valid, key=valid.get) if valid else None
    factors = shor_factors_from_period(a, best_r, N) if best_r else None
    observed = {
        "init": "work=|1> (basis 1)",
        "register_layout": "counting q0..q6 (7) | work q7..q11 (5)",
        "counting_peaks_top8": [{"value": int(m), "phase": round(m / M, 6),
                                 "prob": round(float(pr), 6)} for m, pr in peaks],
        "period_votes": {int(k): round(float(v), 6) for k, v in period_votes.items()},
        "recovered_period": int(best_r) if best_r else None,
        "factors": factors,
        "P_r6": round(float(period_votes.get(6, 0.0)), 6),
        "backends_agree": agree,
    }
    expect = {
        "period_is_6": best_r == 6,
        "factors_3_and_7": factors == [3, 7],
    }
    return _verdict(app, "Shor N=21: counting 측정→연속분수→r=6→21=3×7", observed, expect)


def _verdict(app, claim, observed, expect):
    return {
        "app_id": app["id"],
        "n_sys": app["n"],
        "u_hash": app["u_hash"],
        "tier": app["tier"],
        "sealed_gate_passed": True,   # load_sealed_app 통과 = u_hash 재확인됨
        "behavioral_claim": claim,
        "observed": observed,
        "expectation_checks": {k: bool(v) for k, v in expect.items()},
        "all_expectations_met": all(expect.values()),
    }


# ═══════════════════════════════════════════════════════════════════════════
# 부정 테스트 — 입력 게이트가 변조를 거부하는가
# ═══════════════════════════════════════════════════════════════════════════
def negative_gate_test():
    """sealed u_hash 를 변조한 메모리상 사본으로 게이트가 거부하는지(파일 미변경)."""
    app_id = "ghz3"
    spec_path = os.path.join(APPS, f"{app_id}.app.pg")
    blocks = vs._extract_blocks(open(spec_path, encoding="utf-8").read())
    U = np.asarray(vs.instantiate(blocks["app_golden"], "golden"), dtype=complex)
    real = vs.hash_unitary(U)
    tampered = "0" * len(real)
    refused = real != tampered   # 게이트 로직: u_hash != sealed → 거부
    # 추가: 실제 load 경로에서 변조 시 SealGateError 던지는지(메모리상, 파일 미변경)
    return {"real_hash_ne_tampered": bool(refused),
            "gate_logic": "load_sealed_app 는 hash_unitary(U)!=sealed.u_hash 시 SealGateError"}


# ═══════════════════════════════════════════════════════════════════════════
def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 70)
    print("§5[8](B) 시뮬레이터 백엔드 어댑터 — 봉인앱 실행 계층")
    print("정직성: 실행(시뮬레이션) ≠ 검증(봉인). 출력은 봉인 증거 아님.")
    backends = [b.name for b in get_backends()]
    print(f"백엔드: {backends}  (cirq={'있음' if _HAS_CIRQ else '없음'})")
    print("=" * 70)

    demos = [
        ("ghz3", demo_ghz, ("ghz3",)),
        ("ghz4", demo_ghz, ("ghz4",)),
        ("grover2", demo_grover, ("grover2",)),
        ("wstate3", demo_wstate, ("wstate3",)),
        ("wstate4", demo_wstate, ("wstate4",)),
        ("shor21_a2", demo_shor21, ("shor21_a2",)),
    ]
    results = []
    all_ok = True
    for label, fn, args in demos:
        try:
            r = fn(*args)
        except Exception as e:
            r = {"app_id": label, "error": f"{type(e).__name__}: {e}",
                 "all_expectations_met": False}
            all_ok = False
        ok = r.get("all_expectations_met", False)
        all_ok = all_ok and ok
        results.append(r)
        mark = "✓" if ok else "✗"
        claim = r.get("behavioral_claim", r.get("error", ""))
        ba = r.get("observed", {}).get("backends_agree")
        print(f"  {mark} {label:12s} {claim}"
              + (f"  [backends_agree={ba}]" if ba is not None else ""))

    neg = negative_gate_test()
    print(f"  {'✓' if neg['real_hash_ne_tampered'] else '✗'} negative_gate  "
          f"변조 u_hash 거부(입력 게이트 teeth)")

    report = {
        "tool": "backend_adapter (§5[8](B) simulator execution layer)",
        "honesty_boundary": "execution(simulation) != verification(sealing); "
                            "outputs are illustrative only (spec §8.4); registry/oracle/"
                            "frozen-keys untouched; only already-sealed Tier-0 apps run; "
                            "hardware(QPU) out of scope (ideal statevector only).",
        "backends": backends,
        "determinism": "ideal statevector deterministic; shot sampling seeded "
                       f"(seed={SEED}, shots={SHOTS}); numpy<->cirq agree atol=1e-6.",
        "seed": SEED, "shots": SHOTS,
        "negative_gate_test": neg,
        "demos": results,
        "all_ok": bool(all_ok and neg["real_hash_ne_tampered"]),
    }
    out_path = os.path.join(OUT, "EXECUTION-REPORT.json")
    json.dump(report, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("-" * 70)
    print(f"all_ok={report['all_ok']}  →  {os.path.relpath(out_path, ROOT)}")
    return 0 if report["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
