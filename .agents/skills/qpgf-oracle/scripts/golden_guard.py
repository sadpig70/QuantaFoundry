"""golden_guard.py — golden 독립성 강제 (통합수정설계 v1.1 P0-GOLDEN, 7리뷰 수렴).

문제: C4·C-app은 golden 대조로 정확성을 본다. 그러나 golden 정당성은 명세 작성자에 전가된다.
AI가 `bloq.tensor_contract()`를 golden에 복사하면 **자기참조 검증**(무의미)이 되고, 비자명
모듈에 **항등(identity) golden**을 두면 빈 모듈도 통과(reward-hacking)한다. spec_guard는 golden
*부재*만 막을 뿐 *독립성*은 못 막는다 → 이 게이트가 정적 AST + 의미 검사로 기계적 차단한다.

검사(결정론, AI 판단 아님):
  1. 자기참조: golden 블록이 `bloq` 변수 또는 `.tensor_contract()`를 참조 → 차단
  2. 항등: 비자명(n_sys≥1) 정방 모듈에 항등 golden(전역위상 무시) → 차단

사용:  python golden_guard.py <spec.pg>   (exit0 ok / exit1 차단)
"""
from __future__ import annotations
import sys, os, ast
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_seal import load_pg_spec, instantiate, emit_signal  # noqa: E402
from contracts import ContractViolation, _norm_phase             # noqa: E402


class Verdict:
    def __init__(self, block: bool, reason: str = ""):
        self.block = block
        self.reason = reason


# golden 자기참조로 간주하는 토큰
_FORBIDDEN_ATTR = {"tensor_contract"}
_FORBIDDEN_NAME = {"bloq"}


def golden_independence_guard(spec) -> Verdict:
    """golden이 bloq 출력에 자기참조하지 않고 독립 구성됐는지 검사 (결정론)."""
    src = spec.golden_src or ""
    if not src.strip():
        return Verdict(False)            # 부재는 spec_quality_guard 담당

    # 1) 정적: golden 블록이 bloq / tensor_contract 참조 → 자기참조
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return Verdict(True, f"golden_parse_fail:{e}")
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and node.attr in _FORBIDDEN_ATTR:
            return Verdict(True, "golden_self_reference: golden에 .tensor_contract() 복사 금지 "
                                 "(bloq 출력이 아니라 수학적으로 독립 구성)")
        if isinstance(node, ast.Name) and node.id in _FORBIDDEN_NAME:
            return Verdict(True, "golden_self_reference: golden이 `bloq` 변수 참조 금지")

    # 2) 의미: 비자명 정방 모듈에 항등 golden 금지 (전역위상 무시)
    if spec.n_sys >= 1:
        try:
            G = np.asarray(instantiate(src, "golden"), dtype=complex)
        except Exception:
            G = None
        if G is not None and G.ndim == 2 and G.shape[0] == G.shape[1]:
            d = G.shape[0]
            if np.allclose(_norm_phase(G), np.eye(d), atol=1e-7):
                return Verdict(True, "identity_golden: 비자명 모듈(n_sys>=1)에 항등 golden 금지 "
                                     "(빈/무동작 모듈 reward-hacking)")
    return Verdict(False)


def main(argv) -> int:
    if not argv:
        emit_signal({"block": True, "reason": "usage: golden_guard.py <spec.pg>"})
        return 1
    try:
        spec = load_pg_spec(argv[0])
    except (ContractViolation, Exception) as e:
        emit_signal({"block": True, "reason": f"spec_load_fail:{e}"})
        return 1
    v = golden_independence_guard(spec)
    if v.block:
        emit_signal({"block": True, "spec_id": spec.id, "reason": v.reason})
        return 1
    sys.stdout.write(f"golden_ok: {spec.id}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
