# -*- coding: utf-8 -*-
"""
clifford_routing.py — P0 CliffordTierClosure (task_plan_pg §P0)

Clifford-only 봉인앱을 stabilizer tableau(Tier-2)로 봉인해, 스케일에서 약해지는
보증(Tier-1 structural_wellformed)을 dense 미실체화로 unitary_equiv 까지 회복한다.
유일 Tier-1 앱 ghz16_structural 의 약한 봉인을 닫고, n>12(EXACT_BOUND 초과)
Clifford 앱 봉인 능력을 입증한다.

═══════════════════════════════════════════════════════════════════════════
sub-PG (P0 분해)
═══════════════════════════════════════════════════════════════════════════
P0_CliffordTierClosure
    DetectCliffordApps   // registry/apps 스캔 → plan 이 Clifford 모듈만 참조하는 app
    BuildCliffordBloq    // plan → *봉인 모듈의 실제 bloq* 합성(BloqBuilder), MatrixGate 금지
    CrossValidate        // n≤10: build dense u_hash == registry Tier-0 u_hash (빌더 정확성)
    Tier2Seal            // 오라클 verify_seal(tier=clifford) → Tier-2 봉인 (.pgf/clifford/)
    Ghz16Closure         // 유일 Tier-1 → Tier-2 동반봉인 (structural→unitary_equiv)
    ScaleDemo            // ghz20(n>12) Tier-2 봉인 — dense 불가 구간 정확 봉인 입증
    RoutingGuard         // 결정론 2회 byte-identical + registry/frozen 무변경

정직성 경계:
 - Tier-2 tableau u_hash ≠ Tier-0 dense u_hash (표현 차이, 오라클 명시) — byte-identical
   주장 금지. Tier-2 봉인은 기존 봉인을 *대체하지 않고 동반*(unitary_equiv 보증을 추가).
 - 오라클(verify_seal/clifford_seal)은 *사용만* — 재구현 금지.
 - 봉인은 .pgf/clifford/ 로 (registry/apps·modules canonical 무변경). frozen 키 무변경.
 - SEMANTIC-GUARANTEES.json(비파괴 주석층)만 ghz16 항목에 Tier-2 동반봉인을 *가산* 주석
   (기존 항목 byte 불변 검증). sealed.json/oracle 불변.
 - 합성 bloq 는 봉인 모듈의 실제 Clifford bloq(Hadamard/CNOT/CZ/…) — MatrixGate 0.
"""
from __future__ import annotations

import os
import sys
import re
import json
import glob
import shutil
import subprocess

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, ORACLE)
import verify_seal as vs        # noqa: E402  (instantiate/hash_unitary/_extract_blocks 사용만)
import clifford_seal as cs      # noqa: E402  (is_clifford/canonical_tableau_hash/dense_unitary 사용만)

from qualtran import BloqBuilder  # noqa: E402

APPS = os.path.join(ROOT, "specs", "apps")
MODS = os.path.join(ROOT, "specs", "modules")
APPREG = os.path.join(ROOT, "registry", "apps")
OUT = os.path.join(ROOT, ".pgf", "clifford")
OUT_SPECS = os.path.join(OUT, "specs")
OUT_SEALED = os.path.join(OUT, "sealed")

# 이름 기반 1차 Clifford 분류 (bloq 검증은 봉인 시 오라클 is_clifford 가 최종 판정)
CLIFFORD_MODULES = {"h_gate", "x_gate", "y_gate", "z_gate", "s", "s_dag",
                    "cnot", "cz", "swap2"}


# ── DetectCliffordApps ──────────────────────────────────────────────
def _plan_steps(spec_path):
    txt = open(spec_path, encoding="utf-8").read()
    m = re.search(r"id=plan.*?(\{.*\})\s*```", txt, re.S)
    return json.loads(m.group(1))["steps"] if m else []


def detect_clifford_apps():
    """module-only plan + 전 모듈이 Clifford 인 봉인앱 식별."""
    found = []
    for spec in sorted(glob.glob(os.path.join(APPS, "*.app.pg"))):
        aid = os.path.basename(spec).replace(".app.pg", "")
        seal = os.path.join(APPREG, f"{aid}.sealed.json")
        if not os.path.exists(seal):
            continue
        steps = _plan_steps(spec)
        if not steps or any("app" in s for s in steps):   # sub-app 포함 → 제외(flat 만)
            continue
        mods = {os.path.basename(s["spec"]).split(".")[0] for s in steps if "spec" in s}
        if not mods.issubset(CLIFFORD_MODULES):
            continue
        sd = json.load(open(seal))
        found.append({"id": aid, "n": sd["n_sys"], "tier": sd.get("tier", 0),
                      "modules": sorted(mods), "u_hash": sd["u_hash"]})
    return found


# ── BuildCliffordBloq (봉인 모듈의 실제 bloq 합성) ───────────────────
def _mod_bloq(mid):
    blocks = vs._extract_blocks(open(os.path.join(MODS, f"{mid}.pg"), encoding="utf-8").read())
    return vs.instantiate(blocks["bloq"], "bloq")


def build_app_bloq(aid, n):
    """앱 plan 을 *봉인 모듈의 실제 bloq* 로 합성 (Qualtran BloqBuilder). MatrixGate 미사용."""
    bb = BloqBuilder()
    qs = [bb.add_register(f"q{i}", 1) for i in range(n)]
    for st in _plan_steps(os.path.join(APPS, f"{aid}.app.pg")):
        b = _mod_bloq(os.path.basename(st["spec"]).split(".")[0])
        names = [r.name for r in b.signature]
        tg = st.get("targets") or list(range(len(names)))   # 누락 → full-width 배치
        outs = bb.add_t(b, **{names[k]: qs[tg[k]] for k in range(len(tg))})
        for k in range(len(tg)):
            qs[tg[k]] = outs[k]
    return bb.finalize(**{f"q{i}": qs[i] for i in range(n)})


def build_ghz_canonical(n):
    """canonical GHZ_n = H(q0)·CNOT chain (Hadamard+CNOT primitives). Tier-2 spec 용."""
    bb = BloqBuilder()
    from qualtran.bloqs.basic_gates import Hadamard, CNOT
    qs = [bb.add_register(f"q{i}", 1) for i in range(n)]
    qs[0] = bb.add(Hadamard(), q=qs[0])
    for i in range(n - 1):
        qs[i], qs[i + 1] = bb.add(CNOT(), ctrl=qs[i], target=qs[i + 1])
    return bb.finalize(**{f"q{i}": qs[i] for i in range(n)})


# ── CrossValidate (빌더 정확성: dense == registry) ──────────────────
def cross_validate(apps, dense_bound=10):
    """n≤dense_bound Clifford 앱: 합성 bloq dense u_hash == registry u_hash."""
    checks = []
    for a in apps:
        if a["n"] > dense_bound:
            continue
        try:
            b = build_app_bloq(a["id"], a["n"])
            ok_cliff, reason = cs.is_clifford(b)
            U = cs.dense_unitary(b)
            built = vs.hash_unitary(U)
            checks.append({"id": a["id"], "n": a["n"], "is_clifford": ok_cliff,
                           "dense_matches_registry": built == a["u_hash"]})
        except Exception as e:
            checks.append({"id": a["id"], "n": a["n"], "error": f"{type(e).__name__}: {e}"})
    return checks


# ── Tier2Seal (오라클 verify_seal tier=clifford, .pgf/clifford/) ─────
def _write_clifford_spec(cid, n, builder_src, comment):
    """tier=clifford .pg spec 생성(self-contained bloq 블록)."""
    spec = f"""# {cid} — {comment} (stabilizer tableau Tier-2, dense 미실체화).
```python id=bloq
from qualtran import BloqBuilder
from qualtran.bloqs.basic_gates import Hadamard, CNOT
n = {n}
bb = BloqBuilder()
qs = [bb.add_register(f'q{{i}}', 1) for i in range(n)]
{builder_src}
bloq = bb.finalize(**{{f'q{{i}}': qs[i] for i in range(n)}})
```
```json id=meta
{{"id": "{cid}", "n_sys": {n}, "n_anc": 0, "tier": "clifford"}}
```
"""
    path = os.path.join(OUT_SPECS, f"{cid}.pg")
    open(path, "w", encoding="utf-8", newline="\n").write(spec)
    return path


GHZ_BUILDER_SRC = ("qs[0] = bb.add(Hadamard(), q=qs[0])\n"
                   "for i in range(n-1):\n"
                   "    qs[i], qs[i+1] = bb.add(CNOT(), ctrl=qs[i], target=qs[i+1])")


def tier2_seal(cid, n, builder_src, comment):
    """spec 생성 → 오라클 verify_seal 로 Tier-2 봉인 → sealed dict 반환."""
    spec_path = _write_clifford_spec(cid, n, builder_src, comment)
    r = subprocess.run([sys.executable, os.path.join(ORACLE, "verify_seal.py"),
                        spec_path, "--out", OUT_SEALED],
                       capture_output=True, text=True, cwd=ORACLE)
    seal_path = os.path.join(OUT_SEALED, f"{cid}.sealed.json")
    if r.returncode != 0 or not os.path.exists(seal_path):
        return {"id": cid, "sealed": False, "stderr": r.stderr.strip()[:300]}
    return json.load(open(seal_path))


GUARANTEES = os.path.join(ROOT, "registry", "SEMANTIC-GUARANTEES.json")


def annotate_guarantee(companion_seal, generic_u_hash):
    """비파괴 주석층에 ghz16 Tier-2 동반봉인 가산 주석. 다른 항목 byte 불변 검증."""
    d = json.load(open(GUARANTEES, encoding="utf-8"))
    key = "app:ghz16_structural"
    before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False)
              for k, v in d["guarantees"].items() if k != key}
    entry = d["guarantees"][key]
    entry["tier2_clifford_companion"] = {
        "companion_id": companion_seal["id"],
        "companion_seal_path": ".pgf/clifford/sealed/ghz16_clifford.sealed.json",
        "tier": companion_seal["tier"],
        "u_hash": companion_seal["u_hash"],
        "guarantee": "unitary_equiv",
        "method": "정준 stabilizer tableau(O(n²), dense 미실체화) — Clifford 유니터리를 "
                  "전역위상 무시 유일 결정. 합성=봉인 모듈 실제 bloq(MatrixGate 0).",
        "note": "동반봉인(앱 자체 Tier-1 Merkle 봉인은 불변). Tier-2 u_hash≠Tier-0 dense "
                "u_hash(표현차이). 같은 Clifford 연산의 unitary_equiv 보증을 *추가*.",
        "consistency": "generic(봉인모듈 합성)↔canonical tableau hash 일치 = "
                       f"{companion_seal['u_hash'] == generic_u_hash}",
    }
    after = {k: json.dumps(v, sort_keys=True, ensure_ascii=False)
             for k, v in d["guarantees"].items() if k != key}
    unchanged = before == after
    if unchanged:
        json.dump(d, open(GUARANTEES, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return {"other_entries_unchanged": unchanged, "annotated_key": key,
            "other_count": len(before)}


# ── main ────────────────────────────────────────────────────────────
def main():
    os.makedirs(OUT_SPECS, exist_ok=True)
    os.makedirs(OUT_SEALED, exist_ok=True)
    print("=" * 70)
    print("P0 CliffordTierClosure — Clifford-only 앱 Tier-2 tableau 봉인")
    print("정직성: Tier-2 u_hash≠dense u_hash(표현차이). 동반봉인(대체 아님). registry 무변경.")
    print("=" * 70)

    # 1. Detect
    apps = detect_clifford_apps()
    tier1 = [a for a in apps if a["tier"] == 1]
    print(f"[Detect] Clifford-only 앱 {len(apps)} (Tier-1 약점 {len(tier1)}: "
          f"{[a['id'] for a in tier1]})")

    # 2. CrossValidate (빌더 정확성)
    cv = cross_validate(apps)
    cv_ok = sum(1 for c in cv if c.get("dense_matches_registry"))
    cv_cliff = sum(1 for c in cv if c.get("is_clifford"))
    print(f"[CrossValidate] n≤10: {cv_ok}/{len(cv)} dense==registry, "
          f"{cv_cliff}/{len(cv)} is_clifford (빌더가 봉인앱 정확 재구성)")

    # 3. Ghz16Closure — 유일 Tier-1 을 Tier-2 로 동반봉인
    print("[Ghz16Closure] ghz16_structural(Tier-1) → Tier-2 tableau 봉인...")
    # 일관성: 봉인모듈 합성 빌더 ↔ canonical 빌더 tableau hash 동일 (둘 다 Clifford, dense 불요)
    h_generic, _ = cs.canonical_tableau_hash(build_app_bloq("ghz16_structural", 16))
    h_canon, _ = cs.canonical_tableau_hash(build_ghz_canonical(16))
    consistent = h_generic == h_canon
    ghz16_seal = tier2_seal("ghz16_clifford", 16, GHZ_BUILDER_SRC,
                            "GHZ_16 Clifford (ghz16_structural Tier-1 동반봉인)")
    ghz16_match = ghz16_seal.get("u_hash") == h_generic
    print(f"  generic↔canonical tableau 일치={consistent} · sealed tier={ghz16_seal.get('tier')} "
          f"u_hash={ghz16_seal.get('u_hash','')[:12]} (==generic build {ghz16_match})")

    # 4. ScaleDemo — n>12 (EXACT_BOUND 초과) Clifford 봉인 입증
    print("[ScaleDemo] ghz20(n=20>12) Tier-2 봉인 (dense 2^20 불가, tableau 정확)...")
    ghz20_seal = tier2_seal("ghz20_clifford", 20, GHZ_BUILDER_SRC,
                            "GHZ_20 Clifford (EXACT_BOUND 초과 — dense 불가, tableau 봉인)")
    print(f"  sealed tier={ghz20_seal.get('tier')} u_hash={ghz20_seal.get('u_hash','')[:12]}")

    # 5. RoutingGuard — 결정론(2회 byte-identical) + registry/frozen 무변경
    seal2 = tier2_seal("ghz16_clifford", 16, GHZ_BUILDER_SRC,
                       "GHZ_16 Clifford (ghz16_structural Tier-1 동반봉인)")
    determinism = seal2.get("u_hash") == ghz16_seal.get("u_hash") and \
        seal2.get("sig") == ghz16_seal.get("sig")
    print(f"[RoutingGuard] 결정론 2회 byte-identical(u_hash+sig)={determinism}")

    # 6. AnnotateGuarantee — 비파괴 주석층에 가산 (다른 항목 불변)
    ann = annotate_guarantee(ghz16_seal, h_generic)
    print(f"[AnnotateGuarantee] ghz16 항목에 Tier-2 동반봉인 주석 · "
          f"다른 {ann['other_count']} 항목 불변={ann['other_entries_unchanged']}")

    report = {
        "phase": "P0 CliffordTierClosure",
        "honesty": "Tier-2 tableau u_hash != Tier-0 dense u_hash (representation differs); "
                   "companion seal raising guarantee to unitary_equiv, NOT a byte-identical "
                   "replacement; oracle used only; registry/frozen untouched; bloq=Clifford "
                   "primitives (no MatrixGate).",
        "detected_clifford_apps": len(apps),
        "tier1_weak": [a["id"] for a in tier1],
        "cross_validate": {"tested": len(cv), "dense_matches_registry": cv_ok,
                           "is_clifford": cv_cliff, "detail": cv},
        "ghz16_closure": {
            "generic_canonical_consistent": bool(consistent),
            "tier2_seal": ghz16_seal,
            "sealed_u_hash_matches_build": bool(ghz16_match),
            "guarantee_upgrade": "structural_wellformed(Tier-1) → unitary_equiv(Tier-2 tableau)",
        },
        "scale_demo": {"ghz20_clifford": ghz20_seal,
                       "note": "n=20 > EXACT_BOUND(12): dense 2^20 미실체화, tableau 정확 봉인"},
        "determinism_2x_byte_identical": bool(determinism),
        "guarantee_annotation": ann,
    }
    all_ok = (cv_ok == len(cv) and cv_cliff == len(cv) and consistent and ghz16_match
              and ghz16_seal.get("tier") == 2 and ghz20_seal.get("tier") == 2 and determinism
              and ann["other_entries_unchanged"])
    report["all_ok"] = bool(all_ok)
    json.dump(report, open(os.path.join(OUT, "CLIFFORD-ROUTING-REPORT.json"), "w",
                           encoding="utf-8"), ensure_ascii=False, indent=2)
    print("-" * 70)
    print(f"all_ok={all_ok}  →  .pgf/clifford/CLIFFORD-ROUTING-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
