# -*- coding: utf-8 -*-
"""citation_gen.py — Stage 3 W3.4 CitableRegistry: CITATION.cff + release 메타 (DOI 인용).

재현성 위기 대응: 논문이 "QPGF-sealed root <hash>"를 인용하면 결정론 봉인 전체가 검증가능한
단일 지문으로 고정된다. 본 스크립트는 REGISTRY-MANIFEST 의 registry_root_hash 를 읽어 표준
CITATION.cff(Citation File Format 1.2.0) + release 메타를 생성한다. Zenodo DOI 는 릴리스 시
정욱님 발급 placeholder.

비파괴: registry/sealed/frozen/fingerprint 불변. CITATION.cff(루트) + `.pgf/adoption/RELEASE-META.json` 가산.

사용:
  python scripts/citation_gen.py [--version X.Y] [--date YYYY-MM-DD]
"""
from __future__ import annotations
import os, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "registry", "REGISTRY-MANIFEST.json")


def main():
    args = sys.argv[1:]
    version = args[args.index("--version") + 1] if "--version" in args else "0.7.0"
    date = args[args.index("--date") + 1] if "--date" in args else "2026-06-28"
    man = json.load(open(MANIFEST, encoding="utf-8"))
    root = man["registry_root_hash"]
    n_mod = man["modules"]["count"]
    n_app = man["apps"]["unique_app_count"]

    cite_key = f"QPGF-sealed root {root[:16]}"
    cff = f"""cff-version: 1.2.0
message: "If you use QuantaFoundry sealed artifacts, please cite this and verify the registry root hash."
title: "QuantaFoundry — deterministic QPGF-sealed quantum circuit foundry"
version: "{version}"
date-released: "{date}"
authors:
  - family-names: "Jung"
    given-names: "Wook"
    alias: "sadpig70"
repository-code: "https://github.com/sadpig70/QuantaFoundry"
abstract: >-
  QuantaFoundry is a self-growing foundry where every artifact must pass a deterministic QPGF
  oracle seal (byte-identical reproduction) to exist. This release seals {n_mod} modules and
  {n_app} unique apps with registry_root_hash {root[:16]}…, independently re-derivable via
  `python scripts/reproduce_all.py` and `scripts/second_oracle.py` ({n_mod}/{n_mod} modules).
keywords:
  - quantum-computing
  - deterministic-verification
  - reproducibility
  - QPGF
identifiers:
  - type: other
    value: "registry-root-sha256:{root}"
    description: "Deterministic registry root hash (sorted id:u_hash sha256). The citable fingerprint."
  - type: doi
    value: "10.5281/zenodo.PLACEHOLDER"
    description: "Zenodo DOI — issued at release time."
preferred-citation:
  type: software
  title: "QuantaFoundry v{version} ({cite_key})"
"""
    cff_path = os.path.join(ROOT, "CITATION.cff")
    open(cff_path, "w", encoding="utf-8", newline="\n").write(cff)

    release = {
        "_schema": "release-meta-v1", "version": version, "date_released": date,
        "registry_root_hash": root, "modules": n_mod, "unique_apps": n_app,
        "citation_string": f"QuantaFoundry v{version}, {cite_key} "
                           f"(verify: python scripts/reproduce_all.py).",
        "verify_commands": ["python scripts/reproduce_all.py",
                            "python scripts/second_oracle.py",
                            f"python scripts/qf_cli.py reproduce --expect-root {root[:16]}"],
        "doi_placeholder": "10.5281/zenodo.PLACEHOLDER (release 시 발급)",
        "_note": "registry_root_hash 가 결정론 봉인 전체의 인용가능 단일지문. 논문/소프트웨어 인용 시 "
                 "이 root 를 명시하면 제3자가 byte-identity 로 재현·검증 가능(재현성 위기 대응)."}
    os.makedirs(os.path.join(ROOT, ".pgf", "adoption"), exist_ok=True)
    json.dump(release, open(os.path.join(ROOT, ".pgf", "adoption", "RELEASE-META.json"), "w",
                            encoding="utf-8"), ensure_ascii=False, indent=2)

    print("=" * 72)
    print("CitableRegistry (W3.4) — CITATION.cff + release 메타 (root 인용)")
    print("=" * 72)
    print(f"  version={version} date={date}")
    print(f"  registry_root_hash={root}")
    print(f"  modules={n_mod} unique_apps={n_app}")
    print(f"  citation: \"{release['citation_string']}\"")
    print("-" * 72)
    print(f"→ CITATION.cff · .pgf/adoption/RELEASE-META.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
