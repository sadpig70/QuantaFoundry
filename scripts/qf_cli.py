# -*- coding: utf-8 -*-
"""qf_cli.py — Stage 3 W3.3: QuantaFoundry 단일 진입점 CLI (기존 스크립트 래핑, 신규 로직 0).

채택 마찰 감소: 분산된 스크립트를 `qf <verb>` 단일 인터페이스로. **신규 검증로직 0** — 모든
서브커맨드는 기존 스크립트에 위임(결정론 단일출처 보존). explain 만 registry 조회(검증 아님) 조합.

  qf verify   <module_spec> --out <dir>  → verify_seal.py (모듈 오라클 봉인)
  qf compose  <app_spec> [--store <dir>] → app_assemble.py (앱 합성 봉인)
  qf reproduce [--expect-root <hash>]    → reproduce_all.py (전수 재현 + root 대조)
  qf export   <app_id>|--all             → qasm_export.py (OpenQASM3 + round-trip)
  qf ingest   <app_id>|--demo            → qasm_ingest.py (QASM→spec→봉인 폐루프)
  qf discover [rank|validate|guard|propose] → discover.py (QF-Discover 발견엔진)
  qf explain  <id>                       → registry 조회: dependents(blast) + resource

비파괴: 래핑만. 봉인/오라클/frozen/fingerprint 불변.
"""
from __future__ import annotations
import os, sys, json, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")

USAGE = """qf — QuantaFoundry CLI (기존 스크립트 단일 진입점, 신규 검증로직 0)

  qf verify   <module_spec> --out <dir>     모듈 spec 오라클 봉인 (verify_seal.py)
  qf compose  <app_spec> [--store <dir>]    앱 합성 봉인 (app_assemble.py)
  qf reproduce [--expect-root <hash>]       전수 재현 + root 대조 (reproduce_all.py)
  qf export   <app_id>|--all                sealed → OpenQASM3 + round-trip (qasm_export.py)
  qf ingest   <app_id>|--demo               QASM → spec → 봉인 폐루프 (qasm_ingest.py)
  qf discover [rank|validate|guard|propose] QF-Discover 발견엔진 (discover.py)
  qf explain  <id>                          의존/재사용/자원 조회 (registry)
"""


def _run(script, args, cwd=ROOT, extra_path=None):
    env = dict(os.environ)
    if extra_path:
        env["PYTHONPATH"] = extra_path + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.call([sys.executable, script] + list(args), cwd=cwd, env=env)


def cmd_reproduce(args):
    """reproduce_all.py 위임(전수 재현 검증) + REGISTRY-MANIFEST root 조회·대조(신규 검증로직 아님)."""
    rc = _run(os.path.join(HERE, "reproduce_all.py"), [])
    if rc != 0:
        print("reproduce_all FAILED"); return rc
    expect = None
    if "--expect-root" in args:
        expect = args[args.index("--expect-root") + 1]
    man = os.path.join(ROOT, "registry", "REGISTRY-MANIFEST.json")
    root = json.load(open(man, encoding="utf-8")).get("registry_root_hash", "")
    print(f"\n[qf] registry_root_hash = {root}")
    if expect:
        ok = root.startswith(expect)
        print(f"[qf] expect-root {expect} → {'MATCH ✓' if ok else 'MISMATCH ✗'}")
        return 0 if ok else 1
    return 0


def cmd_explain(args):
    """registry 조회(검증 아님): app/module 의존 + blast-radius + 자원."""
    if not args:
        print("usage: qf explain <id>"); return 2
    target = args[0]
    sys.path.insert(0, HERE)
    import registry_tools as rt
    import resource_report as rr
    graph = rt.build_graph()
    # 자원
    res = None
    for store in ("modules", "apps"):
        p = os.path.join(ROOT, "registry", store, f"{target}.sealed.json")
        if os.path.exists(p):
            res = rr._load(p); break
    deps = graph.get(target, {}).get("depends_on", []) if target in graph else []
    dependents = rt.dependents(graph, target)
    print("=" * 70)
    print(f"qf explain {target}")
    print("=" * 70)
    if res:
        r = res["resource"]
        print(f"  tier={res['tier']} n_sys={res['n_sys']} u_hash={(res['u_hash'] or '')[:16]}")
        print(f"  resource: T={r.get('total_t',0)} toffoli={r.get('toffoli',0)} clifford={r.get('clifford',0)}")
    if deps:
        print(f"  depends_on ({len(deps)}): " + ", ".join(f"{e['id']}×{e['uses']}" for e in deps))
    print(f"  dependents (blast-radius {len(dependents)}): {dependents if dependents else '(none)'}")
    return 0


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print(USAGE); return 0
    cmd, rest = sys.argv[1], sys.argv[2:]
    if cmd == "verify":
        return _run(os.path.join(ORACLE, "verify_seal.py"), rest)
    if cmd == "compose":
        return _run(os.path.join(ORACLE, "app_assemble.py"), rest)
    if cmd == "reproduce":
        return cmd_reproduce(rest)
    if cmd == "export":
        return _run(os.path.join(HERE, "qasm_export.py"), rest)
    if cmd == "ingest":
        return _run(os.path.join(HERE, "qasm_ingest.py"), rest)
    if cmd == "discover":
        return _run(os.path.join(HERE, "discover.py"), rest)
    if cmd == "explain":
        return cmd_explain(rest)
    print(f"unknown command: {cmd}\n"); print(USAGE); return 2


if __name__ == "__main__":
    sys.exit(main())
