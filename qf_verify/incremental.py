# -*- coding: utf-8 -*-
"""incremental — 스텝 지문 캐시 (S1inc, 2026-07-12).

부가 모드다: **authoritative 는 언제나 full 재실행**(INV-INC1). incremental 은 자율 루프의
중간 라운드 가속용이며, verified-only 커밋 게이트·최종보증은 full 만 인정한다.

지문 = sha256( 스텝 정체(argv|special) + 정렬된 [(relpath, sha256(file))] leaf 리스트 ).
입력 집합 = COMMON(봉인 데이터·코어 코드·오라클·manifest·docs) ∪ 스텝 코드의 정적
import 폐쇄(qf_witness/qf_verify 내부 한정) ∪ manifest 선택 키 "inputs"(glob, 가산).

safe-by-default:
 - 해석 불가 스텝(-m 대상 미해석·미지 special) → 지문 None = 상시 실행.
 - fail 스텝은 캐시하지 않는다(재실행 강제). 캐시 적중은 report 에 "from_cache": true 명시
   (registry 스텝의 고유 필드 "cached"(빌드 캐시 카운트)와 이름 충돌 회피).
 - 입력 과대포함은 허용(불필요 재실행=안전), 과소포함만이 위험 — COMMON 은 봉인 데이터
   전체(specs/registry sealed/sidecars/oracle)를 포함해 데이터 변경 시 전면 무효화.

캐시 = _workspace/incremental_cache.json (gitignored, 머신 로컬 — 저장소 산출물 아님).
"""
import glob as _glob
import hashlib
import json
import os
import re

from . import context as cx

CACHE_PATH = os.path.join(cx.ROOT, "_workspace", "incremental_cache.json")
CACHE_SCHEMA = "qf-incremental-cache/v1"

# 봉인 데이터·공유 코드·문서 — 어느 하나라도 변하면 전 스텝 무효 (과대포함=안전 방향)
COMMON_GLOBS = [
    "specs/apps/*.app.pg",
    "specs/modules/*.pg",
    "registry/modules/*.sealed.json",
    "registry/apps/*.sealed.json",
    "registry/REGISTRY-MANIFEST.json",
    "registry/SEMANTIC-GUARANTEES.json",
    "registry/APPROX-GUARANTEES.json",
    "registry/COUNT-ONTOLOGY.json",
    "registry/CANON.json",
    "registry/GLOBAL-PHASE.json",
    ".pgf/keyfree/consensus_keys.json",
    ".pgf/proofs/*.json",
    ".pgf/consensus/*.json",
    ".agents/skills/qpgf-oracle/scripts/*.py",
    ".agents/skills/qpgf-oracle/BUNDLE.sha256",
    "verification/manifests/*.json",
    "verification/profiles/*.json",
    "verification/claims.json",
    "qf_verify/*.py",
    "qf_witness/__init__.py",
    "qf_witness/core/*.py",
    "qf_stdlib/*.py",
    "README.md",
    "docs/*.md",
    "CHANGELOG.md",
    "CITATION.cff",
]

_FROM_RE = re.compile(r"^\s*from\s+((?:qf_witness|qf_verify)[\w.]*)\s+import\s+([\w ,*]+)", re.M)
_IMP_RE = re.compile(r"^\s*import\s+((?:qf_witness|qf_verify)[\w.]*)", re.M)


def _hash_file(path, hcache):
    if path not in hcache:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        hcache[path] = h.hexdigest()
    return hcache[path]


def _glob_files(pattern):
    out = set()
    for p in _glob.glob(os.path.join(cx.ROOT, pattern), recursive=True):
        if os.path.isfile(p):
            out.add(os.path.abspath(p))
    return out


def _mod_file(dotted):
    rel = dotted.replace(".", os.sep)
    for cand in (rel + ".py", os.path.join(rel, "__init__.py")):
        p = os.path.join(cx.ROOT, cand)
        if os.path.isfile(p):
            return os.path.abspath(p)
    return None


def _closure(dotted, seen):
    """정적 import 폐쇄 (qf_witness/qf_verify 내부만) → 파일 집합. 미해석 루트면 None."""
    root = _mod_file(dotted)
    if root is None:
        return None
    files, todo = set(), [dotted]
    while todo:
        mod = todo.pop()
        if mod in seen:
            continue
        seen.add(mod)
        f = _mod_file(mod)
        if f is None:
            continue
        files.add(f)
        src = open(f, encoding="utf-8", errors="replace").read()
        for m in _FROM_RE.finditer(src):
            base = m.group(1)
            todo.append(base)
            for name in m.group(2).split(","):
                name = name.strip().split(" as ")[0].strip()
                if name.isidentifier():
                    todo.append(base + "." + name)
        for m in _IMP_RE.finditer(src):
            todo.append(m.group(1))
    return files


def _special_targets(name):
    """special 스텝의 (추가 glob, 모듈 리스트). 미지 special → None (상시 실행)."""
    from . import special as sp
    if name == "forge_apps":
        return [".pgf/autoforge/*.py"], []
    if name == "frontier_block":
        return [], [argv[1] for _, argv in sp.FRONTIER_STEPS + [sp.FACTORY_STEP]]
    if name == "registry_build":
        return [], ["qf_witness.registry.registry_tools"]
    if name == "second_oracle":
        return [], ["qf_witness.verify.second_oracle"]
    if name == "behavior":
        return [], []          # golden 은 specs(COMMON) 에서 exec
    return None


def fingerprint(step, hcache, common_files):
    """스텝 지문. None = 캐시 불가(상시 실행)."""
    globs, mods = [], []
    if "special" in step:
        tg = _special_targets(step["special"])
        if tg is None:
            return None
        globs, mods = tg
        key = ["special", step["special"]]
    else:
        argv = list(step["argv"])
        if "-m" in argv:
            mods = [argv[argv.index("-m") + 1]]
        elif argv and str(argv[0]).endswith(".py"):
            globs = [argv[0]]
        else:
            return None
        key = ["argv", argv]
    files = set(common_files)
    for g in list(globs) + list(step.get("inputs", [])):
        files |= _glob_files(g)
    seen = set()
    for mod in mods:
        cl = _closure(mod, seen)
        if cl is None:
            return None        # -m 대상 미해석 → 상시 실행
        files |= cl
    leaves = sorted((os.path.relpath(f, cx.ROOT).replace(os.sep, "/"), _hash_file(f, hcache))
                    for f in files)
    blob = json.dumps([key, step.get("expectations"), leaves], sort_keys=True)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def _load():
    try:
        doc = json.load(open(CACHE_PATH, encoding="utf-8"))
        if doc.get("schema") == CACHE_SCHEMA:
            return doc
    except Exception:
        pass
    return {"schema": CACHE_SCHEMA, "entries": {}}


def _save(cache):
    os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
    with open(CACHE_PATH, "w", encoding="utf-8", newline="\n") as f:
        json.dump(cache, f, ensure_ascii=False, indent=1, sort_keys=True)


def execute_with_cache(steps, changed_only, jobs, execute_all):
    """지문 일치 스텝은 캐시 frag 재사용(cached=true), 나머지만 실행 → (results, stats)."""
    hcache = {}
    common_files = set()
    for g in COMMON_GLOBS:
        common_files |= _glob_files(g)
    cache = _load()
    entries = cache["entries"]
    fps = [fingerprint(st, hcache, common_files) for st in steps]
    run_idx = [i for i, (st, fp) in enumerate(zip(steps, fps))
               if fp is None or entries.get(st["id"], {}).get("fp") != fp]
    ran = execute_all([steps[i] for i in run_idx], changed_only, jobs)
    results = [None] * len(steps)
    for slot, res in zip(run_idx, ran):
        results[slot] = res
    n_cached = 0
    for i, st in enumerate(steps):
        if results[i] is None:                          # 캐시 적중
            ent = entries[st["id"]]
            frag = {k: dict(v, from_cache=True) for k, v in ent["frag"].items()}
            meta = dict(ent["meta"], from_cache=True, duration_ms=0)
            results[i] = (frag, meta)
            n_cached += 1
        elif fps[i] is not None:                        # 실행됨 → pass 만 캐시 갱신
            frag, meta = results[i]
            if meta.get("status") == "pass":
                entries[st["id"]] = {"fp": fps[i], "frag": frag,
                                     "meta": {k: meta.get(k) for k in
                                              ("ids", "status", "severity", "claims", "group")}}
            else:
                entries.pop(st["id"], None)
    _save(cache)
    return results, {"cached": n_cached, "executed": len(run_idx),
                     "uncacheable": sum(1 for fp in fps if fp is None)}
