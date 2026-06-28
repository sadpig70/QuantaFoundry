# -*- coding: utf-8 -*-
"""
verify_t1_closure.py — T1 honest-분해 공백 닫힘 회귀 (빠른 재현)

decomposition_honesty_guard 가:
  (A) 정직 모듈 48개를 전부 통과시키고(=오탐 0, 기존 봉인 불변),
  (B) P3d 라운드1 의 hollow 공격 6개를 전부 거부하는지(=공백 닫힘)
결정론적으로 확인한다. (전체 byte-identical 재봉인은 1회 입증됨 — 여기선 가드 단위 회귀.)

비파괴: 가드 *사용만*. 오라클/registry/frozen 무변경.
"""
from __future__ import annotations

import os
import sys
import json
import glob
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, ORACLE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import verify_seal as vs        # noqa: E402
import decomp_guard as dg       # noqa: E402

OUT = os.path.join(ROOT, ".pgf", "bounty")
SUBS = os.path.join(ROOT, "_workspace", "crossmodel", "p3d_bounty", "submissions")


def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 74)
    print("T1 closure 회귀 — honest-분해 가드: 정직 48 통과 · hollow 6 거부")
    print("=" * 74)

    # (A) 정직 모듈 48: 가드 통과(오탐 0)
    honest_specs = sorted(glob.glob(os.path.join(ROOT, "specs", "modules", "*.pg")))
    false_block = []
    for f in honest_specs:
        spec = vs.load_pg_spec(f)
        if dg.decomposition_honesty_guard(spec).block:
            false_block.append(spec.id)
    honest_ok = len(false_block) == 0
    print(f"[A] 정직 모듈 {len(honest_specs)}개 가드 통과 · 오탐(false-block)={len(false_block)} "
          f"→ {'OK' if honest_ok else 'FAIL: ' + str(false_block[:8])}")

    # (B) hollow 공격 6: 가드 거부
    tmp = tempfile.mkdtemp(prefix="t1cl_")
    rejected, total, slipped = 0, 0, []
    for sf in sorted(glob.glob(os.path.join(SUBS, "*.submission.json"))):
        d = json.load(open(sf, encoding="utf-8"))
        for a in d.get("attacks", []):
            if a.get("target") != "T1_hollow":
                continue
            total += 1
            p = os.path.join(tmp, f"atk_{d.get('runtime', total)}.pg")
            open(p, "w", encoding="utf-8", newline="\n").write(a["spec_text"])
            spec = vs.load_pg_spec(p)
            if dg.decomposition_honesty_guard(spec).block:
                rejected += 1
            else:
                slipped.append(d.get("runtime"))
    hollow_ok = total > 0 and rejected == total
    print(f"[B] hollow 공격 {total}개 가드 거부={rejected} · slip={slipped} "
          f"→ {'OK' if hollow_ok else 'FAIL'}")

    all_ok = honest_ok and hollow_ok
    report = {
        "phase": "T1 honest-decomposition gap closure (P3d)",
        "approach": "policy-layer guard (scripts/decomp_guard.py + seal_module.py); fingerprinted "
                    "oracle (verify_seal.py/contracts.py) UNCHANGED → existing 48 seals byte-identical.",
        "honest_modules_checked": len(honest_specs),
        "honest_false_blocks": false_block,
        "hollow_attacks_checked": total,
        "hollow_rejected": rejected,
        "hollow_slipped": slipped,
        "byte_identical_reseal_verified_once": True,
        "all_ok": bool(all_ok),
        "note": "raw verify_seal 직접 호출은 코어(C1-C4)만 본다(기존 posture); honest-분해는 인가된 "
                "입구 seal_module.py 의 정책 게이트가 강제. app 경로 동일 강제는 오라클 spec_guard "
                "수정 필요(별도 승인) — 본 작업은 모듈 경로(데모된 T1 벡터)만 비파괴로 닫음.",
    }
    json.dump(report, open(os.path.join(OUT, "T1-CLOSURE.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("-" * 74)
    print(f"all_ok={all_ok}  →  .pgf/bounty/T1-CLOSURE.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
