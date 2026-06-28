# -*- coding: utf-8 -*-
"""
decomp_guard.py — honest-decomposition 가드 (P3d T1 공백 닫기)

T1 공백: 봉인 오라클은 `U = bloq.tensor_contract()` 를 진리로 신뢰한다. 커스텀 Bloq 가
tensor_contract 를 리터럴 행렬로 override 하면, golden==literal 이라 C4 가 자명 통과한다 —
*정직한 게이트 분해 없이 답을 박아넣는* hollow seal(P3d 라운드1 에서 6/6 모델이 재현, DOC_GAP).

정직성·비파괴:
 - 오라클(verify_seal/contracts) *사용만*, fingerprinted 파일(verify_seal.py·contracts.py) 무수정.
   → 기존 48 봉인 byte-identical 보존, oracle_code_hash·sig 불변.
 - 이 가드는 *정책 계층*(spec_quality_guard·golden_guard 와 같은 비-fingerprint 계층)에 속한다.
   honest-분해는 unitary 속성이 아니라 정책 — 가드 계층이 올바른 위치.

판정(결정론, AI 아님):
 (1) 정적 AST: spec 정의 클래스가 unitary-주장 메서드를 override 하거나, 라이브러리 인스턴스의
     그 메서드를 monkey-patch(속성할당/setattr) → block.
 (2) 동적: 인스턴스화한 bloq 의 type().__module__ 이 qualtran/cirq 출처가 아니면 = spec 정의
     커스텀(hollow) → block. (실측: 정직 모듈 48개 전부 qualtran/cirq 출처 → 무차단.)
"""
from __future__ import annotations

import os
import sys
import ast

ORACLE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, ORACLE)
import verify_seal as vs        # noqa: E402  (instantiate/load_pg_spec 사용만)

# bloq 의 유효 유니터리를 *직접 주장*하는 메서드(정직 분해 우회 표면).
_UNITARY_ASSERT = {"tensor_contract", "_unitary_", "my_tensors", "_tensors_",
                   "_my_tensors_", "adjoint_tensor"}
_TRUSTED_ROOTS = ("qualtran", "cirq")


class Verdict:
    def __init__(self, block: bool, reason: str = ""):
        self.block = block
        self.reason = reason


def _ast_hollow_reason(bloq_src: str):
    """spec 정의 클래스의 unitary override 또는 monkey-patch 정적 검출. 없으면 None."""
    try:
        tree = ast.parse(bloq_src or "")
    except SyntaxError:
        return None                              # 파싱 불가 → 오라클 instantiate 가 처리
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):       # spec 정의 클래스가 유니터리 메서드 override
            for b in node.body:
                if isinstance(b, (ast.FunctionDef, ast.AsyncFunctionDef)) and b.name in _UNITARY_ASSERT:
                    return (f"spec 정의 클래스 '{node.name}' 가 '{b.name}' override "
                            "— 정직 분해 없이 유니터리 직접 주장")
        if isinstance(node, ast.Assign):         # monkey-patch: x.tensor_contract = ...
            for t in node.targets:
                if isinstance(t, ast.Attribute) and t.attr in _UNITARY_ASSERT:
                    return f"'.{t.attr}' 속성 할당(monkey-patch) — 유니터리 override"
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == "setattr" and len(node.args) >= 2
                and isinstance(node.args[1], ast.Constant) and node.args[1].value in _UNITARY_ASSERT):
            return f"setattr('{node.args[1].value}', ...) — 유니터리 override"
    return None


def decomposition_honesty_guard(spec) -> Verdict:
    """봉인 전 hollow bloq 거부. spec.bloq_src 정적 + 인스턴스 동적 두 축."""
    reason = _ast_hollow_reason(getattr(spec, "bloq_src", "") or "")
    if reason:
        return Verdict(True, "honest-분해 위반(정적): " + reason)
    try:
        bloq = vs.instantiate(spec.bloq_src, "bloq")
    except Exception:
        return Verdict(False)                    # instantiate 실패는 verify_seal 가 신호처리
    mod = type(bloq).__module__ or ""
    if not mod.startswith(_TRUSTED_ROOTS):
        return Verdict(True, f"honest-분해 위반(동적): bloq 타입 '{type(bloq).__name__}'"
                             f"(module='{mod}')이 qualtran/cirq 라이브러리 출처 아님 — "
                             "spec 정의 커스텀(hollow). 정직 모듈은 라이브러리 primitive/composite 사용.")
    return Verdict(False)


def main(argv) -> int:
    import json
    if not argv:
        sys.stderr.write(json.dumps({"block": True, "reason": "usage: decomp_guard.py <spec.pg>"}) + "\n")
        return 1
    try:
        spec = vs.load_pg_spec(argv[0])
    except Exception as e:
        sys.stderr.write(json.dumps({"block": True, "reason": f"spec_load_fail:{e}"}) + "\n")
        return 1
    v = decomposition_honesty_guard(spec)
    if v.block:
        sys.stderr.write(json.dumps({"block": True, "spec_id": spec.id, "reason": v.reason},
                                    ensure_ascii=False) + "\n")
        return 1
    sys.stdout.write(f"decomp_ok: {spec.id}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
