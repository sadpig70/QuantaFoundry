# -*- coding: utf-8 -*-
"""
seal_module.py — 인가된 모듈 봉인 입구 (honest-분해 가드 포함, P3d T1 닫기)

raw `verify_seal.py` 는 결정론 코어(C1–C4)만 본다 — honest-분해는 unitary 속성이 아니라
정책이므로 코어가 강제하지 않는다(spec_quality_guard·golden_guard 도 코어 밖 정책 계층).
이 래퍼는 모듈 봉인의 *정책 게이트*를 합성한다:

    spec_quality_guard(오라클)  →  decomposition_honesty_guard(신규)  →  verify_seal(오라클)

세 단계 모두 통과해야 봉인. fingerprinted 파일(verify_seal.py·contracts.py) 무수정 →
기존 48 봉인 byte-identical 보존. 가드는 *사용만*.

사용:  python seal_module.py <spec.pg> --out <registry/modules>
  통과 → verify_seal 위임(sealed.json) · exit 0
  차단 → 구조화 signal(stderr) · exit 1 (봉인 안 함)
"""
from __future__ import annotations

import os
import sys
import json
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, ORACLE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import verify_seal as vs        # noqa: E402  (load_pg_spec 사용만)
import spec_guard as sg         # noqa: E402  (오라클 정책 가드 사용만)
import decomp_guard as dg       # noqa: E402  (신규 honest-분해 가드)


def policy_gate(spec) -> dg.Verdict:
    """모듈 봉인 정책 게이트: 명세충분성 + honest-분해. 통과=Verdict(block=False)."""
    q = sg.spec_quality_guard(spec)
    if q.block:
        return dg.Verdict(True, "spec_quality: " + q.reason)
    h = dg.decomposition_honesty_guard(spec)
    if h.block:
        return dg.Verdict(True, h.reason)
    return dg.Verdict(False)


def seal_module(spec_path: str, out_dir: str) -> int:
    try:
        spec = vs.load_pg_spec(spec_path)
    except Exception as e:
        sys.stderr.write(json.dumps({"block": True, "reason": f"spec_load_fail:{e}"}) + "\n")
        return 1
    v = policy_gate(spec)
    if v.block:
        sys.stderr.write(json.dumps({"block": True, "spec_id": spec.id, "stage": "policy_gate",
                                     "reason": v.reason}, ensure_ascii=False) + "\n")
        return 1
    # 정책 통과 → 오라클 verify_seal 위임(코어 C1–C4 + 봉인 기록).
    # cwd=ORACLE 이므로 spec/out 은 절대경로로(상대경로 미해결 방지, seal_sx.py 와 동일).
    r = subprocess.run([sys.executable, os.path.join(ORACLE, "verify_seal.py"),
                        os.path.abspath(spec_path), "--out", os.path.abspath(out_dir)],
                       capture_output=True, text=True, cwd=ORACLE)
    sys.stdout.write(r.stdout)
    if r.stderr:
        sys.stderr.write(r.stderr)
    return r.returncode


def main(argv) -> int:
    if not argv:
        sys.stderr.write(json.dumps({"block": True,
                                     "reason": "usage: seal_module.py <spec.pg> [--out DIR]"}) + "\n")
        return 1
    out_dir = "."
    if "--out" in argv:
        out_dir = argv[argv.index("--out") + 1]
    return seal_module(argv[0], out_dir)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
