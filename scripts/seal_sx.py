# -*- coding: utf-8 -*-
"""
seal_sx.py — P2b live finalization: sx(√X) cross-model 봉인 + frozen 키 등록

6 distinct-weights 런타임이 sx golden 에 수렴(P2-LIVE-INGEST: SEAL MULTIMODEL, GT✓)했다.
이를 정식 라이브러리 자산으로 확정한다:
  (1) consensus 재확인(6 model ⊕ proof:algebraic √X) → ESTABLISHED, key.
  (2) sx 모듈 봉인(verify_seal, bloq=XPowGate(0.5) ⊕ golden=√X) → registry/modules/sx.sealed.json.
  (3) frozen 키 가산 등록(기존 15키 byte-identical 보존 — Round 1 의 7키와 동일 패턴).
  (4) 결정론 가드: 기존 키 불변 + sealed u_hash == consensus key == GT.

정직성:
 - golden 진리는 *6 cross-model 수렴*이 확립(human seed 0). proof:algebraic(√X 정의)은 제3축
   삼각측량(동반오류 차단) — GT✓ 가 그 일치를 입증. bloq 는 진리에 *conform*(C4 검증)할 뿐.
 - frozen 등록은 신규 합의의 정당한 freeze(append). 기존 15키 재생성 금지(byte 보존 검증).
 - consensus.py/verify_seal *사용만*. honest 분해(bloq=XPowGate, MatrixGate 아님).
"""
from __future__ import annotations

import os
import sys
import json
import glob
import hashlib

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, ORACLE)
sys.path.insert(0, os.path.join(ROOT, ".pgf", "keyfree"))
import verify_seal as vs        # noqa: E402  (hash_unitary 사용만)
import consensus as cc          # noqa: E402  (Source/establish_truth/uhash 사용만)

PKG = os.path.join(ROOT, "_workspace", "crossmodel", "p2_live")
SUBS = os.path.join(PKG, "submissions")
KEYS = os.path.join(ROOT, ".pgf", "keyfree", "consensus_keys.json")
SPECS_MODS = os.path.join(ROOT, "specs", "modules")
MODREG = os.path.join(ROOT, "registry", "modules")
OUT = os.path.join(ROOT, ".pgf", "panel")

SX_GOLDEN_CODE = ("import numpy as np\n"
                  "# sx = principal sqrt(X): SX² = X. cross-model 합의(6 distinct weights) ⊕ "
                  "proof:algebraic(√X 정의).\n"
                  "golden = 0.5*np.array([[1+1j,1-1j],[1-1j,1+1j]], dtype=complex)")


def _sub_uhash(sub, iid):
    s = {x["id"]: x for x in sub["submissions"]}[iid]
    re_ = np.array(s["app_golden_real"], dtype=float)
    im = np.array(s.get("app_golden_imag", np.zeros_like(re_)), dtype=float)
    return cc.uhash(re_ + 1j * im)


def sx_spec():
    return (
        "# sx — √X (principal sqrt-NOT, SX²=X). cross-model 합의(6 distinct weights, human seed 0) ⊕ "
        "proof:algebraic. 하드웨어 네이티브 게이트.\n"
        "```python id=bloq\n"
        "from qualtran.bloqs.basic_gates import XPowGate\n"
        "bloq = XPowGate(exponent=0.5)   # √X (전역위상은 C4 무시)\n"
        "```\n"
        "```python id=golden\n" + SX_GOLDEN_CODE + "\n```\n"
        '```json id=meta\n{"id": "sx", "n_sys": 1, "n_anc": 0}\n```\n')


def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 74)
    print("P2b finalization — sx(√X) cross-model 봉인 + frozen 키 등록")
    print("=" * 74)

    # (1) consensus 재확인: 6 model ⊕ proof:algebraic
    GT = vs.hash_unitary(0.5 * np.array([[1 + 1j, 1 - 1j], [1 - 1j, 1 + 1j]], complex))
    subs = [json.load(open(f, encoding="utf-8")) for f in sorted(glob.glob(os.path.join(SUBS, "*.json")))]
    sources = [cc.Source(f"sx_{s['weights_id']}", "model", s["weights_id"], _sub_uhash(s, "sx"))
               for s in subs]
    sources.append(cc.Source("sx_proof", "proof", "algebraic_sqrtX", GT))   # 제3축 삼각측량
    res = cc.establish_truth("sx", sources)
    n_models = len({s.unit for s in sources if s.klass == "model"})
    print(f"[consensus] status={res.status} grade={res.grade} key={ (res.key or '')[:16]} "
          f"models={n_models} key==GT={res.key == GT}")
    if res.status != "ESTABLISHED" or res.key != GT:
        print("✗ 합의 미성립 또는 GT 불일치 — 중단"); return 1

    # (2) sx 모듈 봉인
    spec_path = os.path.join(SPECS_MODS, "sx.pg")
    open(spec_path, "w", encoding="utf-8", newline="\n").write(sx_spec())
    import subprocess
    r = subprocess.run([sys.executable, os.path.join(ORACLE, "verify_seal.py"), spec_path,
                        "--out", MODREG], capture_output=True, text=True, cwd=ORACLE)
    seal_path = os.path.join(MODREG, "sx.sealed.json")
    if not os.path.exists(seal_path):
        print("✗ 봉인 실패:", r.stderr.strip()[:200]); return 1
    sealed = json.load(open(seal_path))
    seal_ok = sealed["u_hash"] == GT == res.key
    print(f"[seal] sx tier={sealed.get('tier')} u_hash={sealed['u_hash'][:16]} "
          f"== consensus key == GT: {seal_ok}")

    # (3) frozen 키 가산 등록 (기존 15키 byte 보존)
    keys = json.load(open(KEYS, encoding="utf-8"))
    before = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in keys.items()}
    already = "sx" in keys
    keys["sx"] = {"key": res.key, "status": "ESTABLISHED", "grade": res.grade,
                  "provenance": res.provenance, "n_independent_models": n_models,
                  "key_version": 1, "frozen": True,
                  "round": "P2b-live-sx", "gt_match": True}
    after = {k: json.dumps(v, sort_keys=True, ensure_ascii=False) for k, v in keys.items() if k != "sx"}
    existing_intact = before == after
    if existing_intact:
        json.dump(keys, open(KEYS, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"[freeze] sx 키 등록(grade={res.grade}, models={n_models}) · 기존 {len(before)}키 불변="
          f"{existing_intact}{' (이미 존재했음)' if already else ''}")

    # (4) 결정론 가드
    guard = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "verify_contested_guard.py")],
                           capture_output=True, text=True)
    contested_ok = "ALL PASS" in guard.stdout
    print(f"[guard] contested_guard ALL PASS={contested_ok} (frozen 가드 결정론)")

    all_ok = res.status == "ESTABLISHED" and seal_ok and existing_intact and contested_ok
    report = {
        "phase": "P2b finalization (sx √X)",
        "honesty": "golden truth established by 6-model cross-weights convergence (human seed 0); "
                   "proof:algebraic(√X) = third triangulation axis (GT match blocks co-error); "
                   "bloq=XPowGate(0.5) conforms to truth (C4, no MatrixGate); frozen key APPENDED "
                   "(existing 15 keys byte-preserved); consensus/verify_seal used only.",
        "consensus": {"status": res.status, "grade": res.grade, "key": res.key,
                      "n_independent_models": n_models, "provenance": res.provenance,
                      "key_equals_GT": res.key == GT},
        "seal": {"u_hash": sealed["u_hash"], "tier": sealed.get("tier"),
                 "matches_consensus_and_GT": seal_ok},
        "freeze": {"existing_keys_intact": existing_intact, "total_keys": len(keys)},
        "contested_guard_pass": contested_ok,
        "all_ok": bool(all_ok),
    }
    json.dump(report, open(os.path.join(OUT, "P2-SX-SEAL.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("-" * 74)
    print(f"all_ok={all_ok} · 라이브러리 모듈 +1(sx) · frozen 키 {len(keys)}  →  .pgf/panel/P2-SX-SEAL.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
