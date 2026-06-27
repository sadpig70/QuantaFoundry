"""formal_spec.py — intent formal-spec 승격 (Disruptive 패러다임 후반).

자연어 intent의 모호성(E5' cphase_amb: "위상 미정")을 *기계검증 가능한 formal spec*으로 대체한다.
formal spec → sympy 컴파일 → 행렬 → u_hash (proof source). **미정 파라미터가 있으면 컴파일 자체가
거부** = 모호성을 봉인 이전에 차단한다(binding 사슬의 앞쪽 절반, v2 §3).

spec 형식:
  {"kind": "diag",   "n_sys": n, "diag": [expr, ... 2^n 개]}
  {"kind": "perm",   "n_sys": n, "perm": [out_index, ... 2^n 개]}
  {"kind": "matrix", "n_sys": n, "rows": [[expr,...],...]}
expr 은 sympy sympify 가능한 문자열. 자유 심볼(미정 파라미터)이 남으면 complex() 변환 실패 → 거부.
"""
import sympy as sp
import numpy as np


class UnderspecifiedIntent(ValueError):
    """formal spec 에 미정 파라미터가 남아 정답이 유일하지 않음 → 봉인 이전 차단."""


def _val(expr):
    e = sp.sympify(expr)
    if e.free_symbols:
        raise UnderspecifiedIntent(f"free symbol(s) {e.free_symbols} in '{expr}' — intent underspecified")
    return complex(e)


def compile_spec(spec: dict) -> np.ndarray:
    n = spec["n_sys"]; N = 2 ** n
    kind = spec["kind"]
    if kind == "diag":
        d = spec["diag"]
        if len(d) != N:
            raise ValueError(f"diag length {len(d)} != 2^{n}")
        return np.diag([_val(x) for x in d])
    if kind == "perm":
        p = spec["perm"]
        if sorted(p) != list(range(N)):
            raise ValueError("perm is not a permutation of range(2^n)")
        M = np.zeros((N, N), dtype=complex)
        for i, j in enumerate(p):
            M[j, i] = 1
        return M
    if kind == "matrix":
        return np.array([[_val(x) for x in row] for row in spec["rows"]], dtype=complex)
    raise ValueError(f"unknown kind {kind}")


def formal_proof_source(intent_id, spec, Source, uhash):
    """formal spec 을 컴파일해 proof 출처로 변환. 미정이면 UnderspecifiedIntent."""
    U = compile_spec(spec)
    return Source(f"{intent_id}_formal", "proof", "formal-spec", uhash(U))
