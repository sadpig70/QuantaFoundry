# -*- coding: utf-8 -*-
"""coverage — 검증경로 커버리지 매트릭스 (QF-0711 U8 VerificationCoverage).

경로별 sidecar(.pgf/proofs/*)를 합성해 app×path 매트릭스를 만든다: 각 봉인 자산이 *몇 개의
독립 검증경로*로 커버되는지, 그리고 ★**primary seal(dense/tableau/zx) 외 보조경로가 전혀 없는
자산 목록**(다음 검증 투자 = 제11경로 우선순위 데이터). "10 verification paths" 주장을 데이터로 역추적.

비파괴: sidecar/oracle/seal 무접촉·읽기만. root 비입력 → registry/VERIFICATION-COVERAGE.json sidecar.
사용: python -m qf_witness.registry.coverage [--check]   (--check: 비변경 정합검사, witness batch)
"""
import glob
import json
import os
import sys

from qf_witness.core.paths import ROOT

PROOFS = os.path.join(ROOT, ".pgf", "proofs")
SPECS_APPS = os.path.join(ROOT, "specs", "apps")
OUT = os.path.join(ROOT, "registry", "VERIFICATION-COVERAGE.json")

# per-app census 경로 → (sidecar 파일, 추출자). 이질적 sidecar 구조를 흡수.
_VERIFY_SOURCES = {
    "anf": ("ANF-VERIFY.json", lambda d: list(d.get("covered_apps", []))),
    "groebner": ("GROEBNER-VERIFY.json", lambda d: list(d.get("covered_apps", []))),
    "matchgate": ("MATCHGATE-VERIFY.json", lambda d: list(d.get("verified", {}))),
    "qmdd": ("QMDD-VERIFY.json", lambda d: list(d.get("verified", {}))),
    "stabrank": ("STABRANK-VERIFY.json", lambda d: list(d.get("verified", {}))),
    "tncontract": ("TNCONTRACT-VERIFY.json", lambda d: list(d.get("verified", {}))),
    "pathsum": ("PATHSUM-VERIFY.json",
                lambda d: [a["app"] for a in d.get("observation", {}).get("apps", [])]),
    "ring": ("RING-COLUMN.json", lambda d: list(d.get("shor_apps_covered", []))),
    "compositional": ("COMPOSITIONAL-VERIFY.json", lambda d: list(d.get("verified", {}))),
}
# per-app proof 파일(app_id = 파일명 prefix)
_GLOB_SOURCES = {
    "column": "*.column_proof.json",
    "subspace": "*.subspace_proof.json",
    "cuc": "*.cuc_proof.json",
    "affine": "*.affine_proof.json",
}
# per-app census 아닌 method/instance 증인(참고 표기)
_INSTANCE_WITNESSES = {
    "zx": "Tier-3 ZX method-level (Clifford reconstruction identities; not a per-app census)",
    "dense_second_oracle": "primary dense C4 (all sealed modules re-derived independently) — the baseline seal path",
}


def _load(fn):
    p = os.path.join(PROOFS, fn)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def compute():
    covered = {}   # path -> sorted set of app_ids
    for name, (fn, extract) in _VERIFY_SOURCES.items():
        d = _load(fn)
        # id 정규화: anf/groebner sidecar 는 'x.app.pg' 파일명 기록 → appid 로 통일(유령 키·과소계상 방지)
        ids = {(i[:-len(".app.pg")] if i.endswith(".app.pg") else i) for i in extract(d)} if d else set()
        covered[name] = sorted(ids)
    deep = _load("COMPOSITIONAL-DEEP.json")   # S1deep: 동일 형식론 → 같은 경로에 union(이중계상 금지)
    if deep:
        covered["compositional"] = sorted(set(covered["compositional"]) | set(deep.get("verified", {})))
    for name, pat in _GLOB_SOURCES.items():
        ids = [os.path.basename(p)[:-len(pat) + 1] for p in glob.glob(os.path.join(PROOFS, pat))]
        covered[name] = sorted(set(ids))

    by_app = {}    # app_id -> sorted [paths]
    for name, apps in covered.items():
        for a in apps:
            by_app.setdefault(a, []).append(name)
    by_app = {a: sorted(ps) for a, ps in sorted(by_app.items())}

    # 히스토그램 + 단일-보조경로 자산
    hist = {}
    single = {}
    for a, ps in by_app.items():
        hist[len(ps)] = hist.get(len(ps), 0) + 1
        if len(ps) == 1:
            single[a] = ps[0]

    # ★primary-seal-only: 봉인 unique 앱 중 보조경로 0개(dense/tableau/zx primary 뿐).
    #   ★"_" prefix 제외 = discovery_superopt 등의 transient 앱(_superopt_cz 등, 봉인 아님) 배제.
    all_apps = sorted(os.path.basename(p)[:-len(".app.pg")]
                      for p in glob.glob(os.path.join(SPECS_APPS, "*.app.pg"))
                      if not os.path.basename(p).startswith("_"))
    primary_only = sorted(a for a in all_apps if a not in by_app)

    return {
        "_schema": "qf-verification-coverage/v1",
        "_note": ("app×path 커버리지 — 각 봉인 자산을 커버하는 *독립 보조 검증경로* 집합(primary "
                  "dense/tableau/zx seal 은 별도 baseline). 경로별 .pgf/proofs sidecar 합성·root 불변. "
                  "primary_seal_only = 보조경로 0개(다음 검증 투자 후보). coverage_note = 'complementary, "
                  "not universal'(EVIDENCE-MAP row 11)의 정량화."),
        "n_supplementary_paths": len(covered),
        "paths": {name: {"covered": len(apps), "sidecar": (_VERIFY_SOURCES.get(name, ("",))[0]
                                                           or _GLOB_SOURCES.get(name, ""))}
                  for name, apps in sorted(covered.items())},
        "instance_witnesses": _INSTANCE_WITNESSES,
        "coverage_histogram": {str(k): hist[k] for k in sorted(hist)},
        "n_apps_with_supplementary": len(by_app),
        "n_primary_seal_only": len(primary_only),
        "single_supplementary_path": single,
        "primary_seal_only": primary_only,
        "by_app": by_app,
    }


def write():
    data = json.dumps(compute(), ensure_ascii=False, indent=2) + "\n"
    open(OUT, "w", encoding="utf-8", newline="\n").write(data)
    return data


def main():
    check = "--check" in sys.argv or "--quick" in sys.argv
    new = json.dumps(compute(), ensure_ascii=False, indent=2) + "\n"
    cur = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else None
    if check:
        ok = cur == new
        print(f"coverage check: all_ok={ok}" + ("" if ok else " · stale(regen 필요)"))
        return 0 if ok else 1
    open(OUT, "w", encoding="utf-8", newline="\n").write(new)
    c = compute()
    print(f"coverage: {c['n_supplementary_paths']} paths · {c['n_apps_with_supplementary']} apps "
          f"covered · {c['n_primary_seal_only']} primary-seal-only · hist={c['coverage_histogram']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
