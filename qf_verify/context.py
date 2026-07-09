# -*- coding: utf-8 -*-
"""context — 실행 컨텍스트 + changed-only 판정 (reproduce_all.py 에서 의미 불변 이식, INV-RA3).

ChangeContext 의 각 함수는 scripts/reproduce_all.py 의 동명 로직을 그대로 옮긴 것이다
(정책 변경 금지 — 이식만). frontier/factory/template 앱 구분과 coherence sweep 이 핵심.
"""
import os
import sys
import json
import glob
import hashlib
import subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
REPORTS = os.path.join(ROOT, "reports")
_APPREG = os.path.join(ROOT, "registry", "apps")
_ORACLE_DIR = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")


def run(args, cwd=ROOT):
    """legacy 와 동일한 subprocess 실행 (python + args, stdout+stderr 결합)."""
    p = subprocess.run(["python"] + args, cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def template_app_ids():
    """forge_apps 가 관리하는 템플릿 앱 id 집합 (reproduce_all._template_app_ids 이식)."""
    sys.path.insert(0, os.path.join(ROOT, ".pgf", "autoforge"))
    import forge_apps as fa  # noqa: E402  (APP_LIST 참조만)
    return {fn[:-7] for fn, _ in fa.APP_LIST}


def git_changed_specs():
    """변경된 specs/apps·specs/modules basename 집합. git 불가 시 None (reproduce_all 이식)."""
    try:
        out = subprocess.run(["git", "-C", ROOT, "status", "--porcelain",
                              "--", "specs/apps", "specs/modules"],
                             capture_output=True, text=True, timeout=30)
        if out.returncode != 0:
            return None
    except Exception:
        return None
    return {os.path.basename(l[3:].strip().strip('"'))
            for l in out.stdout.splitlines() if l[3:].strip().endswith((".app.pg", ".pg"))}


def factory_app_ids():
    """FACTORY-FRONTIER.json sealed_N → shor/cmul 앱 id 집합 (reproduce_all 이식)."""
    db = os.path.join(ROOT, ".pgf", "arith", "FACTORY-FRONTIER.json")
    if not os.path.exists(db):
        return set()
    ids = set()
    for e in json.load(open(db, encoding="utf-8")).get("sealed_N", []):
        N = e["N"]
        ids.add(f"shor{N}")
        for mul in e.get("unique_powers", []):
            ids.add(f"cmul{mul}_mod{N}")
    return ids


def frontier_specs_changed():
    """legacy frontier(템플릿·factory 외) 앱/module spec 변경? git 부재 시 True→full 폴백 (이식)."""
    changed = git_changed_specs()
    if changed is None:
        return True
    if any(n.endswith(".pg") and not n.endswith(".app.pg") for n in changed):
        return True                                  # module 변경 → 전 앱 영향
    tmpl = template_app_ids()
    fac = factory_app_ids()
    for n in changed:
        if n.endswith(".app.pg"):
            aid = n[:-7]
            if aid not in tmpl and aid not in fac:
                return True                          # legacy frontier 앱 spec 변경 → 전량 재봉인
    return False


def coherence_sweep_frontier():
    """무변경 frontier/factory 앱 sealed.json coherence 검증 (reproduce_all 이식 — 판정 동일)."""
    cur_oracle = hashlib.sha256(open(os.path.join(_ORACLE_DIR, "verify_seal.py"), "rb").read()).hexdigest()
    cur_contracts = hashlib.sha256(open(os.path.join(_ORACLE_DIR, "contracts.py"), "rb").read()).hexdigest()
    skip = template_app_ids() | factory_app_ids()
    checked, bad = 0, []
    for p in glob.glob(os.path.join(_APPREG, "*.sealed.json")):
        app_id = os.path.basename(p)[:-len(".sealed.json")]
        if app_id in skip:
            continue
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            bad.append(app_id)
            continue
        if (d.get("oracle_code_hash") != cur_oracle or d.get("contracts_code_hash") != cur_contracts
                or not d.get("u_hash")):
            bad.append(app_id)
        else:
            checked += 1
    return {"coherence_checked": checked, "failed": bad[:20], "n_failed": len(bad),
            "pass": len(bad) == 0}
