# -*- coding: utf-8 -*-
"""seal_gate_ci.py — Stage 3 W3.5 [EXT] SealGateCI: 봉인 게이트 + seal-badge 생성.

채택 CI: PR 이 registry 결정론을 깨면 머지 차단. CI gate = "로컬 재현 성공해야 제출"(root
byte-identity). 통과 시 seal-badge(Tier 분포 + ResourceCost + root) 생성 → shields.io endpoint.

self-contained 부분(본 스크립트 + .github/workflows/seal-gate.yml)은 완성. **[EXT]**: friendly
외부 라이브러리 1곳 파일럿 협업은 relay 의존(정욱님).

비파괴: 검증/조회만. `.pgf/adoption/seal-badge.json` 가산. registry/sealed/frozen 불변.

사용:
  python scripts/seal_gate_ci.py [--expect-root <hash>]   # 게이트 통과 시 badge 생성
"""
from __future__ import annotations
import os, sys, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "registry", "REGISTRY-MANIFEST.json")
EXPECT_DEFAULT = "58e5af8edf801d96"


def _tier_distribution():
    dist, total_t, total_toff = {}, 0, 0
    for store in ("modules", "apps"):
        for p in glob.glob(os.path.join(ROOT, "registry", store, "*.sealed.json")):
            d = json.load(open(p, encoding="utf-8"))
            t = d.get("tier")
            t = t if t is not None else (1 if "structural" in d.get("contract", "") else 0)
            dist[f"tier{t}"] = dist.get(f"tier{t}", 0) + 1
            r = d.get("resource", {})
            total_t += int(r.get("total_t", 0)); total_toff += int(r.get("toffoli", 0))
    return dist, total_t, total_toff


def main():
    args = sys.argv[1:]
    expect = args[args.index("--expect-root") + 1] if "--expect-root" in args else EXPECT_DEFAULT
    man = json.load(open(MANIFEST, encoding="utf-8"))
    root = man["registry_root_hash"]
    gate_ok = root.startswith(expect)

    dist, total_t, total_toff = _tier_distribution()
    print("=" * 72)
    print("SealGateCI (W3.5 [EXT]) — 봉인 게이트 + seal-badge")
    print("=" * 72)
    print(f"  registry_root_hash = {root[:16]}…")
    print(f"  expect-root {expect} → {'PASS ✓' if gate_ok else 'FAIL ✗ (결정론 위반 — 머지 차단)'}")
    print(f"  tier 분포: {dist} · ΣT={total_t} ΣToffoli={total_toff}")

    # shields.io endpoint 형식 badge
    badge = {"schemaVersion": 1, "label": "QPGF seal",
             "message": f"root {root[:12]} · {man['modules']['count']}mod/{man['apps']['unique_app_count']}app",
             "color": "brightgreen" if gate_ok else "red"}
    out = {"_schema": "seal-badge-v1", "gate_pass": gate_ok, "registry_root_hash": root,
           "expect_root": expect, "tier_distribution": dist,
           "total_t": total_t, "total_toffoli": total_toff,
           "modules": man["modules"]["count"], "unique_apps": man["apps"]["unique_app_count"],
           "shields_endpoint": badge,
           "_note": "CI gate=로컬 재현(root byte-identity) 성공해야 제출. 통과 시 seal-badge 노출. "
                    "외부 라이브러리 파일럿 협업은 [EXT] relay 의존."}
    os.makedirs(os.path.join(ROOT, ".pgf", "adoption"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, ".pgf", "adoption", "seal-badge.json"), "w",
                        encoding="utf-8"), ensure_ascii=False, indent=2)
    print("-" * 72)
    print(f"→ .pgf/adoption/seal-badge.json (shields.io endpoint)")
    return 0 if gate_ok else 1


if __name__ == "__main__":
    sys.exit(main())
