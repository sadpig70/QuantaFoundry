"""spec_guard.py — 명세 충분성 사전점검 (R2, reward-hacking 차단).

자율 루프는 '계약은 통과하나 의도와 다른 것'(빈 모듈·항등)에 수렴할 수 있다.
오라클이 신뢰가능하려면 통과 ≡ 정확성이어야 하고, 그러려면 비자명 모듈에
판별기준(golden)이 있어야 한다. 이 게이트는 verify_seal 호출 *전에* 명세가
그 조건을 갖췄는지 결정론 휴리스틱으로 점검한다 (AI 판단 아님).

사용:  python spec_guard.py <spec.pg>
  충분 → exit 0
  부실 → exit 1 + stderr 구조화 signal (봉인 시도 차단)
"""
from __future__ import annotations
import sys, os, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_seal import load_pg_spec, emit_signal  # noqa: E402
from contracts import ContractViolation  # noqa: E402


class Verdict:
    def __init__(self, block: bool, reason: str = ""):
        self.block = block
        self.reason = reason


def spec_quality_guard(spec) -> Verdict:
    """비자명 모듈은 golden 필수. (결정론 휴리스틱)

    - 자명(n_sys <= 0): 점검 생략 (검증할 시스템 작용 없음)
    - 비자명(n_sys >= 1) + golden 부재: block (reward-hacking 위험)
        근거: golden 없으면 항등/빈 모듈도 C1~C3을 통과해버린다.
    """
    if spec.n_sys <= 0:
        return Verdict(False)
    if not spec.golden_src or not spec.golden_src.strip():
        return Verdict(True, "비자명 모듈(n_sys>=1)에 golden 부재 — "
                             "항등/빈 모듈도 통과 가능(reward-hacking)")
    # golden 독립성 강제 (v1.1 P0-GOLDEN): 자기참조·항등 golden 차단
    import golden_guard
    gi = golden_guard.golden_independence_guard(spec)
    if gi.block:
        return Verdict(True, gi.reason)
    # honest-분해 강제 (P3d T1): bloq 가 tensor_contract 를 리터럴로 override 하는 hollow seal 차단.
    # 모듈/앱(app_assemble) 양쪽 봉인 경로가 이 게이트를 거치므로 일괄 강제됨.
    import decomp_guard
    hd = decomp_guard.decomposition_honesty_guard(spec)
    if hd.block:
        return Verdict(True, hd.reason)
    return Verdict(False)


def main(argv) -> int:
    if not argv:
        emit_signal({"block": True, "reason": "usage: spec_guard.py <spec.pg>"})
        return 1
    try:
        spec = load_pg_spec(argv[0])
    except (ContractViolation, Exception) as e:
        emit_signal({"block": True, "reason": f"spec_load_fail:{e}"})
        return 1
    v = spec_quality_guard(spec)
    if v.block:
        emit_signal({"block": True, "spec_id": spec.id, "reason": v.reason})
        return 1
    sys.stdout.write(f"spec_ok: {spec.id}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
