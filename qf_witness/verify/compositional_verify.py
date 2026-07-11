# -*- coding: utf-8 -*-
"""compositional_verify.py — 앱 조립 독립 재구성 검증 (TrackQF0711Strategic S1).

second_oracle 는 83 **모듈**을 제1원리(numpy만)로 독립 재구성해 sealed u_hash 와 대조한다.
그러나 **앱**은 단 1개(cmul2_mod21)만 손으로 재조립 검증돼 왔다(502 앱 중 1). 이 모듈은 그
단일 사례를 **일반 compositional 검증기**로 확장한다 — 봉인 app.pg 의 배선(plan.steps)을 따라
second_oracle 의 제1원리 모듈 유니터리를 embed·compose 로 재조립하고, 결과 u_hash 를 sealed 와
대조한다. **app_assemble / qualtran / spec-golden 미사용** — 앱-레벨 조립·배선 버그를 독립 차단.

효율: embed(U)@V 대신 apply_left(U, targets, V)=U 를 V 의 row 축에 직접 tensordot((2^n)^2·2^k) —
전 dense matmul((2^n)^3) 대비 수십배 빠름. apply_left ≡ embed(U,targets,n)@V (선형·row 작용 동일).

honest 한계(second_oracle 와 동일 계열):
 - 측정도구 vs.hash_unitary 는 공유(공통 canonicalization). 독립성은 *유니터리를 어떻게 구성했나* —
   본 검증기는 qualtran bloq 도 spec 의 golden 코드도 app_assemble 도 실행하지 않고 재조립한다.
 - 배선 plan(steps) 을 의도 명세로 신뢰하고 **그 조립이 sealed unitary 를 산출함**을 검증한다
   (알고리즘 의미 정당성은 별개 — Shor 는 column/subspace/cuc 경로가 담당).
 - dense-가능 부분집합만: cost=(2^n)^2·steps ≤ BUDGET. 초과 대형앱은 column/ring/cuc/subspace 커버.
   n>13 및 sub-app(모듈 아닌 앱 조립) 스텝 포함 앱은 제외(전부 명시 카운트, silent cap 없음).

메모리 안전(S1fix_MemSafety, 2026-07-11 OOM 사후):
 - 파싱은 lazy — _parse_app 은 (gid, targets, k)만 보유, 모듈 유니터리는 **검증 시점에** 앱 단위
   캐시로 구성 후 해제(전 버전은 전 앱×전 스텝 dense 를 파싱 시 실체화 → 커밋 59GB·시스템 OOM).
 - MEM_BUDGET: 예측 peak(4·(2^n)^2·16B + Σ distinct 모듈 dense) > MEM_BUDGET 앱은 결정론적으로
   skip["mem_guard"] (환경 비의존 상수 — 커버리지 재현성 보존, silent cap 없음).

사용:  python -m qf_witness.verify.compositional_verify [--quick]
  (full=BUDGET_FULL 커버·sidecar 기록 / --quick=BUDGET_QUICK 빠른 부분집합·sidecar 미기록[reproduce])
"""
from __future__ import annotations
import glob
import json
import os
import re
import sys

import numpy as np

from qf_witness.core.paths import ROOT
from qf_witness.verify import second_oracle as so

sys.path.insert(0, os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts"))
import verify_seal as vs  # noqa: E402  (공통 측정도구 — hash. 구성은 독립)

APPS = os.path.join(ROOT, "specs", "apps")
MODS = os.path.join(ROOT, "specs", "modules")
APPREG = os.path.join(ROOT, "registry", "apps")
PROOFS = os.path.join(ROOT, ".pgf", "proofs")
SIDECAR = os.path.join(PROOFS, "COMPOSITIONAL-VERIFY.json")

INDEP = so.INDEP
BUDGET_FULL = 100_000_000       # (2^n)^2·steps ≤ 1e8 (1회 sidecar 생성)
BUDGET_QUICK = 20_000_000       # reproduce witness 스모크 (sidecar 미기록)
N_MAX = 13
MEM_BUDGET = 6 * 2**30          # 예측 peak 상한 6GB (물리 16GB 머신 안전 마진, 결정론적 상수)

_MOD_K: dict = {}               # gid → qubit 수 k (spec meta, 행렬 미구성)


def _module_k(gid):
    """모듈 스펙 meta 에서 k=n_sys+n_anc — dense 구성 없이 크기만 취득 (캐시)."""
    if gid not in _MOD_K:
        src = open(os.path.join(MODS, f"{gid}.pg"), encoding="utf-8").read()
        meta = json.loads(re.search(r"```json id=meta\n(.*?)```", src, re.S).group(1))
        _MOD_K[gid] = meta.get("n_sys", 0) + meta.get("n_anc", 0)
    return _MOD_K[gid]


def apply_left(U, targets, n, V):
    """U 를 V(2^n×2^n)의 row 축(targets)에 직접 작용. ≡ so.embed(U,targets,n) @ V (검증필)."""
    k = len(targets)
    g = U.reshape([2] * k + [2] * k)
    D = 1 << n
    T = V.reshape([2] * n + [D])
    T = np.tensordot(g, T, axes=(list(range(k, 2 * k)), targets))
    T = np.moveaxis(T, list(range(k)), targets)
    return T.reshape(D, D)


def _parse_app(appid):
    """app.pg → (n, steps). steps=[(gid, targets, k)] — 행렬 미구성(lazy). 모듈조립 아니면 ValueError."""
    src = open(os.path.join(APPS, f"{appid}.app.pg"), encoding="utf-8").read()
    meta = json.loads(re.search(r"```json id=app_meta\n(.*?)```", src, re.S).group(1))
    plan = json.loads(re.search(r"```json id=plan\n(.*?)```", src, re.S).group(1))
    n = meta.get("n_sys", 0) + meta.get("n_anc", 0)
    steps = plan.get("steps", [])
    parsed = []
    for s in steps:
        if not isinstance(s, dict) or "spec" not in s:
            raise ValueError("sub-app or non-module step")
        gid = os.path.basename(s["spec"])[:-3]
        if gid not in INDEP:
            raise ValueError(f"module '{gid}' not in INDEP")
        k = _module_k(gid)
        parsed.append((gid, s.get("targets", list(range(k))), k))
    return n, parsed


def _reassemble(n, parsed, drop=None, swap=None):
    """제1원리 모듈로 재조립. drop=스텝 인덱스 제거 / swap=(i,j) targets 교란(teeth).

    모듈 유니터리는 여기서 lazy 구성 — 앱당 distinct 모듈 1회, 반환 시 캐시 해제.
    """
    V = np.eye(1 << n, dtype=complex)
    cache = {}
    for idx, (gid, tg, _k) in enumerate(parsed):
        if drop is not None and idx == drop:
            continue
        if swap is not None and idx == swap[0]:
            tg = parsed[swap[1]][1] if len(parsed[swap[1]][1]) == len(tg) else tg
        if gid not in cache:
            cache[gid] = INDEP[gid]()
        V = apply_left(cache[gid], tg, n, V)
    return vs.hash_unitary(V)


def _mem_pred(n, parsed):
    """예측 peak bytes: 4·dense(V·hash 정준화 사본들) + Σ distinct 모듈 dense(캐시)."""
    dense = (1 << n) * (1 << n) * 16
    mods = sum((1 << k) * (1 << k) * 16 for k in {k for _, _, k in parsed})
    return 4 * dense + mods


def _eligible():
    """모듈조립앱 → [(appid, n, steps, cost, pred)]. cost=(2^n)^2·steps. 스킵 사유 카운트 동반."""
    elig, skip = [], {"sub_app": 0, "n_gt_max": 0}
    for f in sorted(os.listdir(APPS)):
        if not f.endswith(".app.pg"):
            continue
        appid = f[:-7]
        try:
            n, parsed = _parse_app(appid)
        except ValueError:
            skip["sub_app"] += 1
            continue
        if n > N_MAX:
            skip["n_gt_max"] += 1
            continue
        cost = (1 << n) * (1 << n) * len(parsed)
        elig.append((appid, n, parsed, cost, _mem_pred(n, parsed)))
    return elig, skip


def run(quick=False):
    budget = BUDGET_QUICK if quick else BUDGET_FULL
    elig, skip = _eligible()
    skip["mem_guard"] = sum(1 for e in elig if e[3] <= budget and e[4] > MEM_BUDGET)
    covered = sorted([e for e in elig if e[3] <= budget and e[4] <= MEM_BUDGET],
                     key=lambda e: e[3])
    over_budget = [e for e in elig if e[3] > budget]
    verified, failed = {}, []
    for appid, n, parsed, cost, pred in covered:
        sealed = json.load(open(os.path.join(APPREG, f"{appid}.sealed.json"), encoding="utf-8"))["u_hash"]
        got = _reassemble(n, parsed)
        if got == sealed:
            verified[appid] = {"n": n, "steps": len(parsed)}
        else:
            failed.append(appid)
    # teeth: 커버된 앱 중 targets 가 서로 다른 2 스텝을 가진 첫 앱을 골라 swap → mismatch 여야
    teeth = None
    for appid, n, parsed, cost, pred in covered:
        idxs = [(i, tuple(t)) for i, (_, t, _) in enumerate(parsed)]
        pair = next(((i, j) for i, ti in idxs for j, tj in idxs
                     if i < j and ti != tj and len(ti) == len(tj)), None)
        if pair is None:
            continue
        sealed = json.load(open(os.path.join(APPREG, f"{appid}.sealed.json"), encoding="utf-8"))["u_hash"]
        perturbed = _reassemble(n, parsed, swap=pair)
        teeth = {"app": appid, "swap": list(pair), "mismatch": perturbed != sealed}
        break
    all_ok = (not failed) and bool(teeth and teeth["mismatch"]) and len(verified) > 0
    payload = {
        "_schema": "compositional-verify/v1",
        "_note": ("앱 조립 독립 재구성 — app_assemble/qualtran/spec-golden 미사용. second_oracle 제1원리 "
                  "모듈 유니터리를 app.pg 배선(plan.steps)대로 embed·compose → sealed u_hash 대조. "
                  "dense-가능 부분집합(cost=(2^n)^2·steps≤budget)만; 초과·sub-app·n>13·mem_guard "
                  "(예측 peak>MEM_BUDGET) 는 명시 스킵."),
        "budget": budget,
        "mem_budget": MEM_BUDGET,
        "n_verified": len(verified),
        "n_eligible": len(elig),
        "n_over_budget": len(over_budget),
        "skipped": skip,
        "over_budget_note": (f"{len(over_budget)} 앱 cost>budget → column/ring/cuc/subspace 경로 커버; "
                             "본 경로는 dense-가능 조립에 한함(정직 경계)."),
        "teeth": teeth,
        "failed": sorted(failed),
        "verified": {k: verified[k] for k in sorted(verified)},
        "all_ok": all_ok,
    }
    return payload


def main():
    quick = "--quick" in sys.argv[1:]
    payload = run(quick=quick)
    if not quick:                       # full 만 authoritative sidecar 기록(--quick 클로버 방지)
        os.makedirs(PROOFS, exist_ok=True)
        with open(SIDECAR, "w", encoding="utf-8", newline="\n") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
    print(f"compositional_verify: verified={payload['n_verified']} eligible={payload['n_eligible']} "
          f"over_budget={payload['n_over_budget']} skip={payload['skipped']} "
          f"teeth={payload['teeth']['mismatch'] if payload['teeth'] else None}")
    print(f"compositional_verify: all_ok={payload['all_ok']}")
    return 0 if payload["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
