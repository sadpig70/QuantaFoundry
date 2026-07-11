# -*- coding: utf-8 -*-
"""release_root — 릴리스 단위 3층 root (QF-0711 U11 ReleaseRoot).

seal_root(기존 registry_root, 불변) 위에 evidence/toolchain/claim 을 묶어 release_root 를 산출.
외부 인용 시 "봉인만"(seal_root) vs "봉인+증거+툴체인+claim"(release_root)을 구분 가능하게 한다
(agent01 F8·agent07 A2). 신규 상위 해시 — seal_root 는 그대로, 기존 봉인/root 불변.

  seal_root      = REGISTRY-MANIFEST.registry_root_hash (봉인 id:u_hash sha256)
  evidence_root  = H(정렬된 name:sha256 over 집계 evidence: SEMANTIC/APPROX/COVERAGE/COUNT-ONTOLOGY/SCORECARD)
  toolchain_hash = H(requirements.lock + qpgf-oracle DEPENDENCIES.lock + BUNDLE.sha256)
  claim_hash     = H(verification/claims.json)
  release_root   = H(seal|evidence|toolchain|claim)

사용: python -m qf_witness.registry.release_root [--check]
"""
import hashlib
import json
import os
import sys

from qf_witness.core.paths import ROOT

OUT = os.path.join(ROOT, ".pgf", "adoption", "RELEASE-ROOT.json")
_EVIDENCE = ["registry/SEMANTIC-GUARANTEES.json", "registry/APPROX-GUARANTEES.json",
             "registry/VERIFICATION-COVERAGE.json", "registry/COUNT-ONTOLOGY.json",
             "registry/QF-QUALITY-SCORECARD.json"]
_TOOLCHAIN = ["requirements.lock", ".agents/skills/qpgf-oracle/DEPENDENCIES.lock",
              ".agents/skills/qpgf-oracle/BUNDLE.sha256"]
_CLAIMS = "verification/claims.json"


def _sha(b):
    return hashlib.sha256(b).hexdigest()


def _file_sha(rel):
    p = os.path.join(ROOT, rel)
    return _sha(open(p, "rb").read()) if os.path.exists(p) else "MISSING"


def _group_root(rels):
    return _sha("\n".join(f"{r}:{_file_sha(r)}" for r in sorted(rels)).encode())


def compute():
    man = json.load(open(os.path.join(ROOT, "registry", "REGISTRY-MANIFEST.json"), encoding="utf-8"))
    seal_root = man["registry_root_hash"]
    evidence_root = _group_root(_EVIDENCE)
    toolchain_hash = _group_root(_TOOLCHAIN)
    claim_hash = _file_sha(_CLAIMS)
    release_root = _sha(f"seal:{seal_root}\nevidence:{evidence_root}\n"
                        f"toolchain:{toolchain_hash}\nclaim:{claim_hash}".encode())
    return {
        "_schema": "release-root/v1",
        "_note": ("릴리스 3층 root. seal_root=기존 registry_root(봉인 unitary 정체성, 불변). "
                  "release_root=seal+evidence+toolchain+claim 을 함께 인용하는 상위 해시. "
                  "qf_stdlib attest 는 seal_root 까지만 보장(anchor.attested_up_to). 신규 가산·기존 봉인 불변."),
        "seal_root": seal_root,
        "evidence_root": evidence_root,
        "evidence_inputs": _EVIDENCE,
        "toolchain_hash": toolchain_hash,
        "toolchain_inputs": _TOOLCHAIN,
        "claim_manifest_hash": claim_hash,
        "release_root": release_root,
    }


def main():
    check = "--check" in sys.argv or "--quick" in sys.argv
    new = json.dumps(compute(), ensure_ascii=False, indent=2) + "\n"
    cur = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else None
    if check:
        ok = cur == new
        print(f"release_root check: all_ok={ok}" + ("" if ok else " · stale(regen 필요)"))
        return 0 if ok else 1
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8", newline="\n").write(new)
    c = compute()
    print(f"release_root: seal={c['seal_root'][:16]}… evidence={c['evidence_root'][:16]}… "
          f"→ release={c['release_root'][:16]}…")
    return 0


if __name__ == "__main__":
    sys.exit(main())
