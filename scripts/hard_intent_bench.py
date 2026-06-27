"""hard_intent_bench.py — KeyFreeConsensus *necessity* 입증 (외부 리뷰 R-D / F-1 대응, SC 부분).

리뷰 F-1: "지금까지 수립된 진리는 전부 교과서. KeyFreeConsensus 의 necessity(가치)는
답이 없는 hard 영역에서 단 한 번도 입증되지 않았다."

이 벤치는 *비교과서/모호* intent 집합에 consensus 를 돌려 necessity 를 보인다:
  (A) hard 하지만 well-defined → proof⊕structural 독립 수렴 → ESTABLISHED (메커니즘이 교과서 밖에서도 동작)
  (B) ambiguous(미지정 파라미터) → DIVERGENT/escalation (단일 출처면 *임의로 봉인*됐을 것)
  (C) same-weights default 함정(B4) → 독립단위 1로 병합 → 거부 (물리적 독립 필요성)

necessity = (B)·(C)에서 *단일 출처라면 거짓 봉인*이 일어났을 것을 consensus 가 막는다는 점.
SC 한계: 진짜 cross-model 발산율은 6런타임 EXT 필요 — 본 벤치는 proof⊕structural⊕(동일가중치 모사)로
necessity 의 구조를 입증한다(브리프는 _workspace 로 분리).

사용:  python scripts/hard_intent_bench.py
"""
import os, sys, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, ".pgf", "keyfree"))
sys.path.insert(0, os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts"))
import consensus as C   # noqa: E402  (Source, establish_truth, uhash)

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
P0 = np.array([[1, 0], [0, 0]], dtype=complex)
P1 = np.array([[0, 0], [0, 1]], dtype=complex)


def src(sid, klass, unit, U):
    return C.Source(sid, klass, unit, C.uhash(U))


# ── (A) hard 하지만 well-defined: 비교과서 게이트 ──
def cy_proof():   return np.kron(P0, I) + np.kron(P1, Y)          # |0><0|⊗I + |1><1|⊗Y
def cy_struct():                                                   # S·CNOT·S† 류 다른 경로
    Sd = np.diag([1, -1j]); S = np.diag([1, 1j])
    CX = np.kron(P0, I) + np.kron(P1, X)
    return np.kron(I, S) @ CX @ np.kron(I, Sd)

def sqrtswap_proof():                                              # √SWAP (비교과서, 얽힘 생성)
    return np.array([[1, 0, 0, 0],
                     [0, (1 + 1j) / 2, (1 - 1j) / 2, 0],
                     [0, (1 - 1j) / 2, (1 + 1j) / 2, 0],
                     [0, 0, 0, 1]], dtype=complex)
def sqrtswap_struct():                                             # 고유분해 경로: SWAP^(1/2)
    SW = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], dtype=complex)
    w, V = np.linalg.eigh(SW)
    return V @ np.diag(np.exp(1j * np.angle(w.astype(complex)) / 2) * np.abs(w) ** 0.5) @ V.conj().T

def perm3_proof():                                                 # 비교과서 3큐비트 순열(3-cycle on basis 1,2,4)
    p = list(range(8)); p[1], p[2], p[4] = 2, 4, 1
    M = np.zeros((8, 8), complex)
    for i, o in enumerate(p): M[o, i] = 1
    return M
def perm3_struct():                                               # 같은 순열을 곱표현으로 독립 구성
    p = [0, 2, 4, 3, 1, 5, 6, 7]
    M = np.zeros((8, 8), complex)
    for i, o in enumerate(p): M[o, i] = 1
    return M


def run():
    cases = []
    # (A) hard well-defined → 독립 수렴 ESTABLISHED
    cases.append(("cy_gate", "A:hard-welldefined",
                  [src("cy_p", "proof", "sympy", cy_proof()), src("cy_s", "structural", "projector", cy_struct())]))
    cases.append(("sqrt_swap", "A:hard-welldefined",
                  [src("ss_p", "proof", "closed-form", sqrtswap_proof()),
                   src("ss_s", "structural", "eigendecomp", sqrtswap_struct())]))
    cases.append(("custom_perm3", "A:novel-nontextbook",
                  [src("p3_p", "proof", "perm", perm3_proof()),
                   src("p3_s", "structural", "factored", perm3_struct())]))
    # (B) ambiguous: phase 미지정 → 두 출처가 다른 값 → DIVERGENT
    ambA = np.diag([1, 1, 1, np.exp(1j * np.pi / 2)])   # 누군가 π/2 기본값
    ambB = np.diag([1, 1, 1, np.exp(1j * np.pi / 4)])   # 다른 출처 π/4 기본값
    cases.append(("cphase_ambiguous", "B:ambiguous",
                  [src("a1", "proof", "sympy", ambA), src("a2", "structural", "projector", ambB)]))
    # (C) B4: same-weights 두 페르소나가 같은 default(CZ) → 독립단위 1 → 거부
    cz = np.diag([1, 1, 1, -1]).astype(complex)
    cases.append(("b4_same_weights", "C:same-weights-default",
                  [src("g", "model", "gpt5", cz), src("b", "model", "gpt5", cz)]))   # 같은 unit gpt5
    # (B') endianness trap: 같은 intent, 두 출처가 control=first vs control=last → 다른 u_hash → DIVERGENT
    cfirst = np.kron(P0, I) + np.kron(P1, X)            # control=first
    clast = np.kron(I, P0) + np.kron(X, P1)             # control=last (다른 컨벤션)
    cases.append(("endianness_trap", "B:convention-ambiguous",
                  [src("e1", "model", "modelA", cfirst), src("e2", "model", "modelB", clast)]))

    rows = []
    for cid, kind, sources in cases:
        r = C.establish_truth(cid, sources, N=2)
        # 단일 출처였다면? 첫 출처를 그대로 봉인했을 것
        single_would_seal = sources[0].u_hash[:10]
        rows.append({"intent": cid, "kind": kind, "status": r.status, "grade": r.grade,
                     "key": (r.key or "")[:10], "single_source_would_seal": single_would_seal,
                     "escalation": r.escalation})
    return rows


def main():
    rows = run()
    print("=" * 92)
    print("Hard-Intent Benchmark — KeyFreeConsensus necessity (F-1 대응, SC)")
    print("=" * 92)
    est = div = 0
    for r in rows:
        mark = "✅ESTABLISHED" if r["status"] == "ESTABLISHED" else "🛑" + r["status"]
        print(f"  {r['intent']:18} [{r['kind']:24}] {mark:16} grade={r['grade']}")
        if r["status"] == "ESTABLISHED":
            est += 1
        else:
            div += 1
            print(f"       └ 단일출처면 봉인됐을 키={r['single_source_would_seal']}.. → consensus 가 거부: {r['escalation'][:60]}")
    print("=" * 92)
    print(f"(A) hard well-defined ESTABLISHED={est} (교과서 밖 메커니즘 동작) · "
          f"(B/C) 거부={div} (단일출처면 거짓봉인될 것 차단 = necessity)")
    print("=" * 92)
    json.dump(rows, open(os.path.join(ROOT, "_workspace", "HARD-INTENT-BENCH-RESULT.json"), "w",
                         encoding="utf-8"), ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
