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
   sub-app 스텝은 targets 합성으로 재귀 인라인(S1ext, 2026-07-11) — 모듈 환원 불가·n>13 은
   제외(전부 명시 카운트, silent cap 없음).

메모리 안전(S1fix_MemSafety, 2026-07-11 OOM 사후):
 - 파싱은 lazy — _parse_app 은 (gid, targets, k)만 보유, 모듈 유니터리는 **검증 시점에** 앱 단위
   캐시로 구성 후 해제(전 버전은 전 앱×전 스텝 dense 를 파싱 시 실체화 → 커밋 59GB·시스템 OOM).
 - MEM_BUDGET: 예측 peak(4·(2^n)^2·16B + Σ distinct 모듈 dense) > MEM_BUDGET 앱은 결정론적으로
   skip["mem_guard"] (환경 비의존 상수 — 커버리지 재현성 보존, silent cap 없음).

사용:  python -m qf_witness.verify.compositional_verify [--quick | --deep [--max-hours H]]
  (full=BUDGET_FULL 커버·sidecar 기록 / --quick=BUDGET_QUICK 빠른 부분집합·sidecar 미기록[reproduce]
   / --deep=over_budget 1회 심층 검증 → COMPOSITIONAL-DEEP.json, 앱 단위 resumable·cost 오름차순·
     soft 시간상한 graceful stop(잔여 명시). reproduce 스텝 아님 — CUC 류 오프라인 영구 기록.)
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
BUDGET_DEEP = 100_000_000_000   # --deep 기본 상한 1e11 (--budget 으로 확장 가능 — 몬스터 청크용)
N_MAX = 13
MEM_BUDGET = 6 * 2**30          # 예측 peak 상한 6GB (물리 16GB 머신 안전 마진, 결정론적 상수)
DEEP_SIDECAR = os.path.join(PROOFS, "COMPOSITIONAL-DEEP.json")
CKPT_DIR = os.path.join(ROOT, "_workspace", "deep_ckpt")   # gitignored 머신로컬
CKPT_MIN_COST = 50_000_000_000  # 이 cost 이상 앱만 intra-app 체크포인트 (오버헤드 회피)
CKPT_INTERVAL = 600             # 초 — 체크포인트 주기 (V 1GB 저장 ~수 초)

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


MAX_INLINE_DEPTH = 8            # sub-app 재귀 인라인 안전 상한 (실측 최대 깊이 << 8)

_PLAN_CACHE: dict = {}          # appid → (n, steps) 원본 plan (행렬 미구성)


def _app_plan(appid):
    """app.pg → (n, steps) 원본 plan (캐시)."""
    if appid not in _PLAN_CACHE:
        src = open(os.path.join(APPS, f"{appid}.app.pg"), encoding="utf-8").read()
        meta = json.loads(re.search(r"```json id=app_meta\n(.*?)```", src, re.S).group(1))
        plan = json.loads(re.search(r"```json id=plan\n(.*?)```", src, re.S).group(1))
        _PLAN_CACHE[appid] = (meta.get("n_sys", 0) + meta.get("n_anc", 0), plan.get("steps", []))
    return _PLAN_CACHE[appid]


def _flat_steps(appid, targets, depth):
    """plan 을 모듈 스텝으로 재귀 인라인. targets=이 앱 큐빗→최상위 좌표 remap. → (steps, inlined).

    sub-app 스텝 {"app": ..., "targets": [...]} 은 그 앱의 plan 을 targets 합성으로 전개한다
    (스텝 targets t → parent targets[t] — remap 의 remap). 모듈조립으로 환원 불가면 ValueError.
    """
    if depth > MAX_INLINE_DEPTH:
        raise ValueError("sub-app inline depth exceeded")
    n, steps = _app_plan(appid)
    if len(targets) != n:
        raise ValueError(f"sub-app '{appid}' targets arity {len(targets)} != n {n}")
    out, inlined = [], False
    for s in steps:
        if not isinstance(s, dict):
            raise ValueError("non-dict step")
        if "spec" in s:
            gid = os.path.basename(s["spec"])[:-3]
            if gid not in INDEP:
                raise ValueError(f"module '{gid}' not in INDEP")
            k = _module_k(gid)
            tg = s.get("targets", list(range(k)))
            out.append((gid, [targets[t] for t in tg], k))
        elif "app" in s:
            sub = os.path.basename(s["app"])
            if sub.endswith(".app.pg"):
                sub = sub[:-7]
            sub_n = _app_plan(sub)[0]
            sub_tg = s.get("targets", list(range(sub_n)))
            sub_steps, _ = _flat_steps(sub, [targets[t] for t in sub_tg], depth + 1)
            out.extend(sub_steps)
            inlined = True
        else:
            raise ValueError(f"unknown step keys: {sorted(s)}")
    return out, inlined


def _parse_app(appid):
    """app.pg → (n, steps, inlined). steps=[(gid, targets, k)] — sub-app 재귀 인라인·행렬 미구성."""
    n, _ = _app_plan(appid)
    parsed, inlined = _flat_steps(appid, list(range(n)), 0)
    return n, parsed, inlined


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
    """모듈환원앱 → [(appid, n, steps, cost, pred, inlined)]. cost=(2^n)^2·steps(인라인 후). 스킵 카운트 동반."""
    elig, skip = [], {"unflattenable": 0, "n_gt_max": 0}
    for f in sorted(os.listdir(APPS)):
        if not f.endswith(".app.pg"):
            continue
        appid = f[:-7]
        try:
            n, parsed, inlined = _parse_app(appid)
        except ValueError:
            skip["unflattenable"] += 1
            continue
        if n > N_MAX:
            skip["n_gt_max"] += 1
            continue
        cost = (1 << n) * (1 << n) * len(parsed)
        elig.append((appid, n, parsed, cost, _mem_pred(n, parsed), inlined))
    return elig, skip


def run(quick=False):
    budget = BUDGET_QUICK if quick else BUDGET_FULL
    elig, skip = _eligible()
    skip["mem_guard"] = sum(1 for e in elig if e[3] <= budget and e[4] > MEM_BUDGET)
    covered = sorted([e for e in elig if e[3] <= budget and e[4] <= MEM_BUDGET],
                     key=lambda e: e[3])
    over_budget = [e for e in elig if e[3] > budget]
    verified, failed = {}, []
    for appid, n, parsed, cost, pred, inlined in covered:
        sealed = json.load(open(os.path.join(APPREG, f"{appid}.sealed.json"), encoding="utf-8"))["u_hash"]
        got = _reassemble(n, parsed)
        if got == sealed:
            verified[appid] = {"n": n, "steps": len(parsed), "inlined": inlined}
        else:
            failed.append(appid)

    def _teeth(pool):
        """pool 첫 앱 중 targets 가 서로 다른 같은-크기 2 스텝을 골라 swap → mismatch 여야."""
        for appid, n, parsed, cost, pred, inlined in pool:
            idxs = [(i, tuple(t)) for i, (_, t, _) in enumerate(parsed)]
            pair = next(((i, j) for i, ti in idxs for j, tj in idxs
                         if i < j and ti != tj and len(ti) == len(tj)), None)
            if pair is None:
                continue
            sealed = json.load(open(os.path.join(APPREG, f"{appid}.sealed.json"), encoding="utf-8"))["u_hash"]
            perturbed = _reassemble(n, parsed, swap=pair)
            return {"app": appid, "swap": list(pair), "mismatch": perturbed != sealed}
        return None

    teeth = _teeth(covered)
    # teeth_inline: sub-app 인라인(remap 합성)을 거친 앱에서도 교란이 잡히는지 별도 확인
    teeth_inline = _teeth([e for e in covered if e[5]])
    all_ok = ((not failed) and bool(teeth and teeth["mismatch"]) and len(verified) > 0
              and (teeth_inline is None or teeth_inline["mismatch"]))
    payload = {
        "_schema": "compositional-verify/v1",
        "_note": ("앱 조립 독립 재구성 — app_assemble/qualtran/spec-golden 미사용. second_oracle 제1원리 "
                  "모듈 유니터리를 app.pg 배선(plan.steps)대로 embed·compose → sealed u_hash 대조. "
                  "sub-app 스텝은 targets 합성으로 재귀 인라인(모듈 환원). dense-가능 부분집합"
                  "(cost=(2^n)^2·steps≤budget)만; 초과·환원불가·n>13·mem_guard 는 명시 스킵."),
        "budget": budget,
        "mem_budget": MEM_BUDGET,
        "n_verified": len(verified),
        "n_eligible": len(elig),
        "n_over_budget": len(over_budget),
        "skipped": skip,
        "over_budget_note": (f"{len(over_budget)} 앱 cost>budget → column/ring/cuc/subspace 경로 커버; "
                             "본 경로는 dense-가능 조립에 한함(정직 경계)."),
        "teeth": teeth,
        "teeth_inline": teeth_inline,
        "failed": sorted(failed),
        "verified": {k: verified[k] for k in sorted(verified)},
        "all_ok": all_ok,
    }
    return payload


def _teeth_one(appid, n, parsed):
    """단일 앱 teeth: targets 가 다른 같은-크기 2 스텝 swap → mismatch 여야. 불가하면 None."""
    idxs = [(i, tuple(t)) for i, (_, t, _) in enumerate(parsed)]
    pair = next(((i, j) for i, ti in idxs for j, tj in idxs
                 if i < j and ti != tj and len(ti) == len(tj)), None)
    if pair is None:
        return None
    sealed = json.load(open(os.path.join(APPREG, f"{appid}.sealed.json"), encoding="utf-8"))["u_hash"]
    perturbed = _reassemble(n, parsed, swap=pair)
    return {"app": appid, "swap": list(pair), "mismatch": perturbed != sealed}


def _ckpt_paths(appid, idx=None):
    meta = os.path.join(CKPT_DIR, f"{appid}.meta.json")
    arr = None if idx is None else os.path.join(CKPT_DIR, f"{appid}.V.{idx}.npy")
    return meta, arr


def _reassemble_ckpt(appid, n, parsed, deadline=None):
    """intra-app 체크포인트 재조립(몬스터용): V+idx 주기 저장·재개. 결정론 — 재개 == 무중단.

    deadline(epoch 초) 초과 시 체크포인트 저장 후 None(미완, 다음 run 이 이어감).
    저장 순서(크래시 안전): V.{idx}.npy 기록 → meta 원자 교체 → 옛 V 파일 삭제.
    완료 시 체크포인트 삭제 후 u_hash 반환.
    """
    import time
    os.makedirs(CKPT_DIR, exist_ok=True)
    meta_p, _ = _ckpt_paths(appid)
    V, start = None, 0
    if os.path.exists(meta_p):
        try:
            m = json.load(open(meta_p, encoding="utf-8"))
            _, arr_p = _ckpt_paths(appid, m["idx"])
            if (m.get("n") == n and m.get("n_steps") == len(parsed)
                    and arr_p and os.path.exists(arr_p)):
                V = np.load(arr_p)
                start = m["idx"]
        except Exception:
            V, start = None, 0
    if V is None:
        V = np.eye(1 << n, dtype=complex)
        start = 0

    def save(idx):
        _, arr_new = _ckpt_paths(appid, idx)
        tmp = arr_new + ".tmp.npy"
        np.save(tmp, V)
        os.replace(tmp, arr_new)
        mtmp = meta_p + ".tmp"
        with open(mtmp, "w", encoding="utf-8") as f:
            json.dump({"appid": appid, "n": n, "n_steps": len(parsed), "idx": idx}, f)
        os.replace(mtmp, meta_p)
        for old in glob.glob(os.path.join(CKPT_DIR, f"{appid}.V.*.npy")):
            if old != arr_new:
                try:
                    os.remove(old)
                except OSError:
                    pass

    cache, last = {}, time.time()
    for idx in range(start, len(parsed)):
        gid, tg, _k = parsed[idx]
        if gid not in cache:
            cache[gid] = INDEP[gid]()
        V = apply_left(cache[gid], tg, n, V)
        now = time.time()
        if now - last >= CKPT_INTERVAL or (deadline is not None and now > deadline):
            save(idx + 1)
            last = now
            if deadline is not None and now > deadline:
                return None
    h = vs.hash_unitary(V)
    for p in glob.glob(os.path.join(CKPT_DIR, f"{appid}.V.*.npy")) + [meta_p]:
        try:
            os.remove(p)
        except OSError:
            pass
    return h


def _write_deep(payload):
    """앱 단위 원자적 재기록 — kill 시에도 진행분 보존(resumable)."""
    os.makedirs(PROOFS, exist_ok=True)
    tmp = DEEP_SIDECAR + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    os.replace(tmp, DEEP_SIDECAR)


def run_deep(max_hours=None, budget=None):
    """over_budget(BUDGET_FULL<cost≤budget·mem 통과) 앱 심층 검증 — cost 오름차순·resumable.

    budget 기본=BUDGET_DEEP(1e11). --budget 확장 시 몬스터가 target 에 들어오며, cost≥CKPT_MIN_COST
    앱은 intra-app 체크포인트로 세션 청크(--max-hours) 를 넘어 이어진다. 이전 sidecar 의 verified 는
    현재 budget 과 무관하게 sealed 불변이면 단조 보존(예산 축소 rerun 이 기록을 지우지 않음).
    """
    import time
    t0 = time.time()
    deadline = None if max_hours is None else t0 + max_hours * 3600
    budget = BUDGET_DEEP if budget is None else int(budget)
    elig, _skip = _eligible()
    targets = sorted([e for e in elig if BUDGET_FULL < e[3] <= budget and e[4] <= MEM_BUDGET],
                     key=lambda e: e[3])
    excluded = sorted(e[0] for e in elig if e[3] > budget)
    mem_excluded = sorted(e[0] for e in elig
                          if BUDGET_FULL < e[3] <= budget and e[4] > MEM_BUDGET)
    prev = {}
    if os.path.exists(DEEP_SIDECAR):
        try:
            doc = json.load(open(DEEP_SIDECAR, encoding="utf-8"))
            if doc.get("_schema") == "compositional-deep/v1":
                prev = doc.get("verified", {})
        except Exception:
            prev = {}
    verified, failed, remaining = {}, [], []
    teeth = None
    target_ids = {e[0] for e in targets}
    for appid, pv in prev.items():                     # 단조 보존: 예산 밖 기존 기록도 sealed 불변이면 유지
        if appid in target_ids:
            continue
        sp = os.path.join(APPREG, f"{appid}.sealed.json")
        if os.path.exists(sp) and json.load(open(sp, encoding="utf-8"))["u_hash"] == pv.get("u_hash"):
            verified[appid] = pv

    def payload():
        return {
            "_schema": "compositional-deep/v1",
            "_note": ("compositional 의 over_budget 잔여 1회 심층 검증(오프라인, reproduce 스텝 아님). "
                      "동일 형식론·동일 제1원리 재조립 — coverage 는 compositional 경로에 union(이중계상 "
                      "금지). cost>budget 몬스터=deep_excluded — 정직 표기: cmul*_mod1285 는 "
                      "tncontract 경로 보유, cmul*_mod3683 5앱은 앱 자체 보조경로 없음(부모 shor3683 의 "
                      "CUC 인증은 부모 앱 단위이지 이 sub-app 들의 per-app census 가 아님). "
                      "cost≥CKPT_MIN_COST 앱은 intra-app 체크포인트(결정론: 재개==무중단)로 청크 소화."),
            "budget_low": BUDGET_FULL, "budget_high": budget, "mem_budget": MEM_BUDGET,
            "n_verified": len(verified), "n_targets": len(targets),
            "deep_excluded": excluded, "mem_excluded": mem_excluded,
            "remaining": sorted(remaining), "teeth": teeth,
            "failed": sorted(failed),
            "verified": {k: verified[k] for k in sorted(verified)},
            "all_ok": ((not failed) and len(verified) > 0
                       and (teeth is None or teeth["mismatch"])),
        }

    stopped = False
    for appid, n, parsed, cost, pred, inlined in targets:
        sealed = json.load(open(os.path.join(APPREG, f"{appid}.sealed.json"),
                                encoding="utf-8"))["u_hash"]
        pv = prev.get(appid)
        if pv and pv.get("u_hash") == sealed and pv.get("steps") == len(parsed):
            verified[appid] = pv                       # resume: sealed·배선 불변 → 보존
            continue
        if stopped or (deadline is not None and time.time() > deadline):
            stopped = True
            remaining.append(appid)
            continue
        t1 = time.time()
        if cost >= CKPT_MIN_COST:
            got = _reassemble_ckpt(appid, n, parsed, deadline=deadline)
            if got is None:                            # 청크 소진 — ckpt 보존, 다음 run 이 이어감
                print(f"deep: {appid} checkpointed (chunk limit) — resume next run", flush=True)
                stopped = True
                remaining.append(appid)
                _write_deep(payload())
                continue
        else:
            got = _reassemble(n, parsed)
        entry = {"n": n, "steps": len(parsed), "inlined": inlined, "cost": cost,
                 "u_hash": sealed, "seconds": round(time.time() - t1, 1)}
        if got == sealed:
            verified[appid] = entry
        else:
            failed.append(appid)
        print(f"deep: {appid} n={n} steps={len(parsed)} cost={cost:.1e} "
              f"{entry['seconds']}s {'OK' if got == sealed else 'FAIL'} "
              f"[{len(verified)}/{len(targets)}]", flush=True)
        _write_deep(payload())
    # teeth: 최저 cost 대상 1건 교란 (resume 시에도 재확인 — 수 초)
    for appid, n, parsed, cost, pred, inlined in targets:
        if appid in verified:
            t = _teeth_one(appid, n, parsed)
            if t is not None:
                teeth = t
                break
    _write_deep(payload())
    return payload()


def main():
    argv = sys.argv[1:]
    if "--deep" in argv:
        hours = None
        if "--max-hours" in argv:
            hours = float(argv[argv.index("--max-hours") + 1])
        budget = None
        if "--budget" in argv:
            budget = float(argv[argv.index("--budget") + 1])
        p = run_deep(max_hours=hours, budget=budget)
        print(f"compositional_deep: verified={p['n_verified']}/{p['n_targets']} "
              f"remaining={len(p['remaining'])} excluded={len(p['deep_excluded'])} "
              f"mem_excluded={len(p['mem_excluded'])} failed={p['failed']} "
              f"teeth={p['teeth']['mismatch'] if p['teeth'] else None}")
        print(f"compositional_deep: all_ok={p['all_ok']}")
        return 0 if p["all_ok"] else 1
    quick = "--quick" in argv
    payload = run(quick=quick)
    if not quick:                       # full 만 authoritative sidecar 기록(--quick 클로버 방지)
        os.makedirs(PROOFS, exist_ok=True)
        with open(SIDECAR, "w", encoding="utf-8", newline="\n") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
    print(f"compositional_verify: verified={payload['n_verified']} eligible={payload['n_eligible']} "
          f"over_budget={payload['n_over_budget']} skip={payload['skipped']} "
          f"teeth={payload['teeth']['mismatch'] if payload['teeth'] else None} "
          f"teeth_inline={payload['teeth_inline']['mismatch'] if payload['teeth_inline'] else None}")
    print(f"compositional_verify: all_ok={payload['all_ok']}")
    return 0 if payload["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
