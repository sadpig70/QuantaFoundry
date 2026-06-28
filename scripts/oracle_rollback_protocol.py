# -*- coding: utf-8 -*-
"""oracle_rollback_protocol.py — Stage 5 W5.2: fingerprint 변경 → revocation 프로토콜.

blind-spot: fingerprint 2파일(verify_seal.py·contracts.py)의 sha256 가 모든 sealed.json 의
oracle_code_hash·contracts_code_hash 와 sig 에 결합돼 있다. 이 2파일이 버그수정/업그레이드로
바뀌면 *전 봉인의 sig 가 깨진다* — 그 순간 무엇을 revoke 하고 어떻게 재봉인하는지 절차가 필요.

본 모듈(분석/검증/문서 전용 비파괴):
  FingerprintAudit — 현 verify_seal/contracts 의 sha256 == 전 sealed 의 기록값인지 전수대조.
                     전부 일치 = fingerprint intact → revocation_list 빈배열이 정당.
  RevocationList   — manifest.revocation_list 현황 + 운영 규약.
  EmergencyReseal  — fingerprint 변경 시 rollback + 재봉인 절차 문서(docs/EMERGENCY-RESEAL.md).

**fingerprint 2파일 절대 무수정** — 본 모듈은 *읽기*만 하고 sha256 대조만 한다(재봉인 안 함).

비파괴: registry/sealed/frozen 불변. `.pgf/hardening/`·`docs/` 가산.

사용:  python scripts/oracle_rollback_protocol.py
"""
from __future__ import annotations
import os, sys, json, glob, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
MODREG = os.path.join(ROOT, "registry", "modules")
APPREG = os.path.join(ROOT, "registry", "apps")
MANIFEST = os.path.join(ROOT, "registry", "REGISTRY-MANIFEST.json")
OUT = os.path.join(ROOT, ".pgf", "hardening")
DOC = os.path.join(ROOT, "docs", "EMERGENCY-RESEAL.md")


def _file_sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def fingerprint_audit():
    """현 verify_seal.py/contracts.py sha256 == 전 sealed 의 oracle/contracts_code_hash."""
    cur_oracle = _file_sha256(os.path.join(ORACLE, "verify_seal.py"))
    cur_contracts = _file_sha256(os.path.join(ORACLE, "contracts.py"))
    checked, intact, mismatched = 0, 0, []
    for store in (MODREG, APPREG):
        for p in glob.glob(os.path.join(store, "*.sealed.json")):
            d = json.load(open(p, encoding="utf-8"))
            if "oracle_code_hash" not in d:
                continue
            checked += 1
            ok = (d.get("oracle_code_hash") == cur_oracle and
                  d.get("contracts_code_hash") == cur_contracts)
            if ok:
                intact += 1
            else:
                mismatched.append(os.path.basename(p))
    return {"current_oracle_code_hash": cur_oracle, "current_contracts_code_hash": cur_contracts,
            "checked": checked, "intact": intact, "mismatched": mismatched[:20],
            "n_mismatched": len(mismatched), "all_intact": len(mismatched) == 0}


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.dirname(DOC), exist_ok=True)
    print("=" * 82)
    print("OracleRevocationProtocol (W5.2) — fingerprint 무결성 전수대조 + revocation 절차")
    print("=" * 82)

    fa = fingerprint_audit()
    print(f"  현 oracle_code_hash    = {fa['current_oracle_code_hash'][:24]}…")
    print(f"  현 contracts_code_hash = {fa['current_contracts_code_hash'][:24]}…")
    _tag = "(ALL INTACT ✅)" if fa["all_intact"] else f"· 불일치 {fa['n_mismatched']}"
    print(f"  fingerprint 무결성: {fa['intact']}/{fa['checked']} sealed 일치 {_tag}")
    if not fa["all_intact"]:
        print(f"  ⚠ 불일치 봉인: {fa['mismatched']}")

    man = json.load(open(MANIFEST, encoding="utf-8"))
    revlist = man.get("revocation_list", [])
    print(f"  manifest.revocation_list: {len(revlist)}건 "
          f"{'(빈배열 — fingerprint intact 이므로 정당)' if not revlist else revlist}")

    out = {"_schema": "oracle-revocation-v1", "fingerprint_audit": fa,
           "revocation_list": revlist, "revocation_list_justified_empty": fa["all_intact"] and not revlist,
           "protocol": {
               "trigger": "verify_seal.py 또는 contracts.py 의 sha256 변경(버그수정/업그레이드)",
               "detection": "본 스크립트 fingerprint_audit — intact<checked 면 변경 감지",
               "on_change": ["1. git 으로 fingerprint 2파일 변경 검토(의도/버그 여부)",
                             "2. 변경이 정당하면: 영향 sealed 를 revocation_list 에 등재",
                             "3. reproduce_all 로 전 모듈/앱 재봉인 → 새 oracle_code_hash 로 갱신",
                             "4. 새 registry_root_hash 발행 + CITATION 갱신(W3.4) + revocation_list 비움",
                             "5. 변경이 버그면: git revert 로 rollback → fingerprint 복원(재봉인 불필요)"]},
           "_note": "fingerprint 2파일은 읽기만(sha256 대조). 전 intact = revocation 불필요. 변경 시 "
                    "EMERGENCY-RESEAL 절차로 rollback 또는 전수 재봉인. 분석/검증/문서 전용 비파괴."}
    json.dump(out, open(os.path.join(OUT, "ORACLE-REVOCATION.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    doc = [
        "# Emergency Re-seal & Oracle Revocation Protocol (Stage 5 W5.2)\n",
        "> fingerprint 2파일(verify_seal.py·contracts.py) 변경 시 전 봉인 sig 무효화 대응 절차.\n",
        "## 배경\n",
        "모든 `sealed.json` 의 `sig` 는 `oracle_code_hash`(=sha256(verify_seal.py)) + "
        "`contracts_code_hash`(=sha256(contracts.py)) 를 포함해 산출된다. 이 2파일이 1바이트라도 "
        "바뀌면 전 봉인의 sig 가 깨진다(설계된 결합 — 오라클 무결성 보증).\n",
        "## 무결성 점검\n",
        "```\npython scripts/oracle_rollback_protocol.py\n```",
        "현 sha256 == 전 sealed 의 기록값이면 `ALL INTACT`. 하나라도 불일치 = fingerprint 변경 감지.\n",
        "## 변경 감지 시 절차\n",
        "1. **검토** — `git diff` 로 fingerprint 2파일 변경이 의도(업그레이드)인지 버그인지 판정.\n",
        "2. **버그면 rollback** — `git revert`/`git checkout` 으로 2파일 복원 → 재봉인 불필요(sig 복원).\n",
        "3. **정당한 업그레이드면 재봉인**:\n"
        "   - 영향 sealed 를 `registry/REGISTRY-MANIFEST.json` 의 `revocation_list` 에 등재.\n"
        "   - `python scripts/reproduce_all.py` 로 전 모듈·앱 재봉인(새 oracle_code_hash 기록).\n"
        "   - 새 `registry_root_hash` 확인 → `python scripts/citation_gen.py` 로 CITATION 갱신.\n"
        "   - 재봉인 완료 후 `revocation_list` 비움(전 봉인이 새 fingerprint 로 유효).\n",
        "## revocation_list 규약\n",
        "- 빈배열 = 전 봉인이 현 fingerprint 로 유효(정상). 본 점검이 ALL INTACT 일 때만 정당.\n",
        "- 비어있지 않음 = 재봉인 진행 중 또는 폐기된 봉인 존재. blast-radius 는 "
        "`python scripts/registry_tools.py dependents <id>` 로 계산.\n",
        "## 불변 제약\n",
        "- fingerprint 2파일은 **절대 임의 수정 금지**. 변경은 오직 의도된 오라클 업그레이드에서만, "
        "위 재봉인 절차를 전수 수행할 때.\n"]
    open(DOC, "w", encoding="utf-8", newline="\n").write("\n".join(doc))

    print("-" * 82)
    print(f"판정: fingerprint {'ALL INTACT — revocation 불필요' if fa['all_intact'] else 'CHANGED — 재봉인 절차 필요'}")
    print(f"→ .pgf/hardening/ORACLE-REVOCATION.json · docs/EMERGENCY-RESEAL.md")
    return 0 if fa["all_intact"] else 1


if __name__ == "__main__":
    sys.exit(main())
