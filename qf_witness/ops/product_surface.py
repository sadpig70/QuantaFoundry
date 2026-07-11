# -*- coding: utf-8 -*-
"""product_surface.py — QF-0711 P3: read-only 소비 조회 계층 (신규 검증로직 0).

제어면(P0 단일출처·P1 sidecar·P2 릴리스 root)이 정합한 **신뢰면을 조회·표시**만 한다.
검증/봉인/재현을 수행하지 않는다 — 이미 생성된 아티팩트를 사람가독 텍스트로 포맷할 뿐이다.
신뢰의 근거는 여전히 reproduce_all(결정론) + oracle 독립검증(정확성)이며, 본 계층은 그것을
**조회**한다. 등급 출력에는 GUARANTEE_CLASSES 의 정직 경계(honest_boundary)를 그대로 노출한다.

조회 소스(전부 read-only):
  registry/SEMANTIC-GUARANTEES.json   — 자산별 등급·method·u_hash + guarantee_classes 카탈로그
  registry/VERIFICATION-COVERAGE.json — 자산별 보조검증경로(by_app) + paths 카탈로그
  verification/claims.json            — 12 claim(주장↔증거↔정직경계)
  .pgf/DESIGN-MasterRoadmap.md        — 로드맵 Gantree(트랙·상태)

비파괴: 봉인/오라클/frozen/fingerprint/root 무접촉. qf_cli.py 가 inspect/claims/plan 으로 배선.
"""
from __future__ import annotations
import json
import os
import re

from qf_witness.core.paths import ROOT

_SEMANTIC = os.path.join(ROOT, "registry", "SEMANTIC-GUARANTEES.json")
_COVERAGE = os.path.join(ROOT, "registry", "VERIFICATION-COVERAGE.json")
_CLAIMS = os.path.join(ROOT, "verification", "claims.json")
_ROADMAP = os.path.join(ROOT, ".pgf", "DESIGN-MasterRoadmap.md")

_STATUSES = ("done", "in-progress", "designing", "blocked", "decomposed",
             "needs-verify", "ready", "delegated", "awaiting-return", "returned")


def _load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ───────────────────────── inspect ─────────────────────────

def inspect(asset_id: str) -> int:
    """자산(app/module) 검증상태 조회: 등급·method·honest_boundary·보조검증경로·tier. 검증 아님."""
    sem = _load(_SEMANTIC)
    guarantees = sem["guarantees"]
    classes = sem.get("guarantee_classes", {})
    # by_kind 우선순위: app:id → module:id → bare
    entry = None
    for key in (f"app:{asset_id}", f"module:{asset_id}", asset_id):
        if key in guarantees:
            entry = guarantees[key]
            break
    if entry is None:
        print(f"qf inspect: 봉인 자산 '{asset_id}' 을(를) SEMANTIC-GUARANTEES 에서 찾을 수 없음.")
        print("  (app id 또는 module id 를 확인하세요. `qf explain <id>` 로 의존/자원 조회 가능.)")
        return 2
    gclass = entry.get("semantic_guarantee", "unclassified")
    cinfo = classes.get(gclass, {})
    cov = _load(_COVERAGE)
    paths = cov.get("by_app", {}).get(asset_id)
    print("=" * 72)
    print(f"qf inspect {asset_id}")
    print("=" * 72)
    print(f"  kind={entry.get('kind')}  tier={entry.get('tier')}  u_hash={(entry.get('u_hash') or '')[:16]}")
    print(f"  guarantee     : {gclass}")
    if cinfo:
        print(f"  coverage_domain: {cinfo.get('coverage_domain', '?')}  (seal_tier {cinfo.get('seal_tier')})")
    if entry.get("method"):
        print(f"  method        : {entry['method']}")
    print(f"  honest_boundary: {cinfo.get('honest_boundary', '(카탈로그 미등재)')}")
    if paths:
        print(f"  supplementary paths ({len(paths)}): {', '.join(paths)}")
    elif entry.get("kind") == "app":
        print("  supplementary paths (0): primary-seal-only (다음 독립검증 투자 후보)")
    print("  ─ 이 출력은 조회이지 검증이 아니다. 근거=reproduce_all(결정론)+oracle 독립검증. ─")
    return 0


# ───────────────────────── claims ─────────────────────────

def claims(claim_id: str | None = None) -> int:
    """주장↔증거↔정직경계 조회. id 없으면 12건 목록, 있으면 단건 상세."""
    data = _load(_CLAIMS)
    items = data["claims"] if isinstance(data, dict) and "claims" in data else data
    if isinstance(items, dict):
        items = list(items.values())
    if claim_id is None:
        print("=" * 72)
        print(f"qf claims — {len(items)} 주장 (verification/claims.json)")
        print("=" * 72)
        for c in items:
            print(f"  [{c.get('guarantee_class','?'):22}] {c.get('id')}")
            print(f"      {c.get('title','')}")
        print("  ─ 단건 상세: qf claims <id>. 드리프트 게이트=qf_verify check-claims(별도). ─")
        return 0
    match = [c for c in items if c.get("id") == claim_id or claim_id in c.get("id", "")]
    if not match:
        print(f"qf claims: '{claim_id}' 매칭 주장 없음. `qf claims` 로 전체 목록 확인.")
        return 2
    for c in match:
        print("=" * 72)
        print(f"qf claims {c.get('id')}")
        print("=" * 72)
        print(f"  title        : {c.get('title')}")
        print(f"  guarantee    : {c.get('guarantee_class')}")
        print(f"  honest_bound : {c.get('boundary')}")
        steps = c.get("evidence_steps", [])
        print(f"  evidence step: {', '.join(steps) if steps else '(none)'}")
        print("  command      : python scripts/reproduce_all.py --changed-only  "
              "(위 step 이 배치로 재현됨)")
        files = c.get("authoritative_files", [])
        if files:
            print(f"  authority    : {', '.join(files)}")
    return 0


# ───────────────────────── plan ─────────────────────────

def _parse_status(line: str) -> str | None:
    """라인의 마지막 status 그룹 추출. '(status — detail)' 중 status 토큰만."""
    found = None
    for m in re.finditer(r"\(([^()]*)\)", line):
        head = m.group(1).strip().split()[0].split("—")[0].strip() if m.group(1).strip() else ""
        if head in _STATUSES:
            found = head
    return found


def _roadmap_nodes():
    """MasterRoadmap 파싱 → [(indent_level, name, desc, status)]. read-only."""
    out = []
    with open(_ROADMAP, encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n")
            m = re.match(r"^(\s*)([A-Za-z][A-Za-z0-9_]+)\s*//\s*(.*)$", line)
            if not m:
                continue
            indent = len(m.group(1)) // 4
            out.append((indent, m.group(2), m.group(3), _parse_status(line)))
    return out


def plan(query: str | None = None) -> int:
    """로드맵 read-only 조회. query 없으면 최상위 트랙+상태 집계, 있으면 substring 매칭 노드."""
    nodes = _roadmap_nodes()
    if query is None:
        tracks = [n for n in nodes if n[0] == 1]           # 최상위 트랙(루트=0)
        from collections import Counter
        tally = Counter(n[3] or "?" for n in tracks)
        print("=" * 72)
        print(f"qf plan — MasterRoadmap 최상위 트랙 {len(tracks)}개")
        print("=" * 72)
        for indent, name, desc, status in tracks:
            print(f"  ({status or '?':12}) {name}")
        print("  ─ 상태 집계: " + " · ".join(f"{k}={v}" for k, v in sorted(tally.items())))
        print("  ─ 노드 검색: qf plan <substring>. (read-only 조회, 설계는 .pgf/DESIGN-MasterRoadmap.md) ─")
        return 0
    q = query.lower()
    hits = [n for n in nodes if q in n[1].lower() or q in n[2].lower()]
    print("=" * 72)
    print(f"qf plan '{query}' — 매칭 노드 {len(hits)}개")
    print("=" * 72)
    for indent, name, desc, status in hits:
        pad = "  " * indent
        print(f"  {pad}({status or '?':12}) {name} // {desc[:80]}")
    if not hits:
        print("  (매칭 없음. qf plan 으로 트랙 목록 확인.)")
    return 0
