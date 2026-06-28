# -*- coding: utf-8 -*-
"""decomp_optimizer.py — Stage 2 W2.2 ExploitAxis: 분해 최적화기 (오라클=reward).

발견(W2.1)이 *무엇을* 만들지라면, ExploitAxis 는 *어떻게* 더 싸게 만들지다. 타깃 유니터리를
**고정**하고 분해만 탐색한다. 오라클 봉인이 하드 보상 게이트:
    reward(cand) = 0                        if (not sealed) or (u_hash != target_u_hash)
                 = 1 + resource_score(res)  otherwise
봉인+동일 u_hash 가 하드 제약이라 reward-hacking(가짜 보상)이 **구조적으로 불가** — 자원만
줄이고 유니터리를 바꾸면 u_hash 불일치로 reward=0. capability-coverage 게이트가 trivial
양산(identity-padding 등 자원증가 분해)을 추가 차단한다.

본 모듈(분석/실증 전용 비파괴):
  CheaperDecompProbe — registry 의 동일 u_hash 다분해 그룹 → 최소 자원 분해 선택(자원감소 실증).
                       모든 후보는 이미 오라클 봉인됨(reward≥1). cz vs cz_rediscovered 등.
  HardRewardOracle   — 한 타깃에 실제 app_assemble 재봉인으로 reward 계산(동적). reward-hacking
                       teeth: u_hash≠target 후보(봉인되더라도)는 reward=0 실증.

정직성: 임시 store(.pgf/discover/_probe)로만 재봉인 → registry/sealed/frozen/fingerprint 불변.
새 진리 발명 아님 — 동일 u_hash 하 자원 최소화. 미발견 시 정직 음성. MatrixGate 없음(봉인부품 재조합).
소비 자산(사용만): app_assemble(assemble) · resource_report(_load).

사용:
  python scripts/decomp_optimizer.py probe     # registry 동일 u_hash 최소자원 선택(자원감소 실증)
  python scripts/decomp_optimizer.py reward     # HardReward 오라클 동적 + reward-hacking teeth
"""
from __future__ import annotations
import os, sys, json, glob, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts"))
import resource_report as rr          # noqa: E402  _load 사용만
import app_assemble as aa             # noqa: E402  assemble(오라클) 사용만

MODREG = os.path.join(ROOT, "registry", "modules")
APPREG = os.path.join(ROOT, "registry", "apps")
SPECS_APPS = os.path.join(ROOT, "specs", "apps")
OUT = os.path.join(ROOT, ".pgf", "discover")
PROBE_STORE = os.path.join(OUT, "_probe")   # 임시 재봉인 store (registry 오염 방지)


def resource_cost(res):
    """연속 자원비용: Toffoli(비싸다)·T·Clifford 가중합. 낮을수록 좋음(FTQC 화폐)."""
    return (int(res.get("toffoli", 0)) * 10 + int(res.get("total_t", 0)) * 1
            + int(res.get("clifford", 0)) * 0.1)


def resource_score(res):
    """reward 의 연속항: 자원비용 역수 정규화 ∈ (0,1]."""
    return round(1.0 / (1.0 + resource_cost(res)), 6)


# ─────────────── CheaperDecompProbe (정적, registry 동일 u_hash) ───────────────
def _all_sealed():
    items = []
    for store, ns in ((MODREG, "module"), (APPREG, "app")):
        for f in glob.glob(os.path.join(store, "*.sealed.json")):
            it = rr._load(f)
            it["ns"] = ns
            it["is_unique_app"] = (ns == "app" and os.path.exists(
                os.path.join(SPECS_APPS, f"{it['id']}.app.pg")))
            items.append(it)
    return items


def cmd_probe():
    os.makedirs(OUT, exist_ok=True)
    items = _all_sealed()
    by_hash = {}
    for it in items:
        by_hash.setdefault(it["u_hash"], []).append(it)

    groups = []
    for h, cands in by_hash.items():
        # 자원비용이 서로 다른 분해가 ≥2 종류일 때만 최적화 의미
        costs = {round(resource_cost(c["resource"]), 4) for c in cands}
        if len(costs) < 2:
            continue
        ranked = sorted(cands, key=lambda c: resource_cost(c["resource"]))
        cheapest, dearest = ranked[0], ranked[-1]
        # base = 가장 비싼(보통 명시적 분해 _rediscovered/_pipeline/_via_), best = 최소
        saving = round(resource_cost(dearest["resource"]) - resource_cost(cheapest["resource"]), 4)
        groups.append({
            "u_hash": h[:16],
            "candidates": [{"id": c["id"], "ns": c["ns"], "cost": round(resource_cost(c["resource"]), 4),
                            "resource": {k: c["resource"].get(k, 0) for k in ("total_t", "toffoli", "clifford")}}
                           for c in ranked],
            "cheapest_decomposition": cheapest["id"], "dearest_decomposition": dearest["id"],
            "resource_saving": saving,
            "reward_cheapest": round(1 + resource_score(cheapest["resource"]), 6),
            "reward_dearest": round(1 + resource_score(dearest["resource"]), 6)})
    groups.sort(key=lambda g: -g["resource_saving"])

    print("=" * 86)
    print("ExploitAxis CheaperDecompProbe (W2.2) — 동일 u_hash 고정, 분해만 최소자원 선택")
    print("=" * 86)
    print(f"동일 유니터리·다자원 분해 그룹 {len(groups)} (모든 후보 오라클 봉인됨 = reward≥1):")
    for g in groups:
        chain = " | ".join(f"{c['id']}(cost={c['cost']})" for c in g["candidates"])
        print(f"  u={g['u_hash']}  save={g['resource_saving']:.2f}  최소={g['cheapest_decomposition']}")
        print(f"      {chain}")
    improved = [g for g in groups if g["resource_saving"] > 0]
    out = {"_schema": "exploit-axis-probe-v1",
           "_note": "타깃 유니터리(u_hash) 고정, 분해만 탐색 → 최소 자원비용 선택. cost=Toffoli·10+T+Cliff·0.1. "
                    "모든 후보가 이미 오라클 봉인(reward≥1)이라 동일 유니터리 보장 — reward-hacking 불가. "
                    "자원감소>0 = 더 싼 봉인 분해 실존. 분석전용 비파괴.",
           "groups": groups, "n_groups": len(groups), "n_with_saving": len(improved)}
    json.dump(out, open(os.path.join(OUT, "EXPLOIT-AXIS-PROBE.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("-" * 86)
    print(f"자원감소 실존 {len(improved)}/{len(groups)} 그룹 · → .pgf/discover/EXPLOIT-AXIS-PROBE.json")
    return 0 if improved else 1


# ─────────────── HardRewardOracle (동적, reward-hacking teeth) ───────────────
def oracle_reward(spec_path, target_u_hash, store):
    """실제 app_assemble 재봉인 → reward. 하드게이트: 미봉인 OR u_hash≠target → 0."""
    try:
        v = aa.assemble(spec_path, store)
    except Exception as e:
        return {"reward": 0.0, "sealed": False, "reason": f"assemble-error: {e}", "u_hash": None}
    if not v.sealed:
        return {"reward": 0.0, "sealed": False, "reason": "not-sealed (oracle reject)", "u_hash": None}
    if v.u_hash != target_u_hash:
        return {"reward": 0.0, "sealed": True, "reason": "u_hash != target (different unitary)",
                "u_hash": v.u_hash[:16]}
    return {"reward": round(1 + resource_score(v.resource), 6), "sealed": True,
            "reason": "sealed & u_hash match", "u_hash": v.u_hash[:16], "resource": v.resource}


def cmd_reward():
    """타깃 cz 의 분해 후보들을 실제 오라클 재봉인으로 reward 계산. reward-hacking teeth 포함."""
    if os.path.isdir(PROBE_STORE):
        shutil.rmtree(PROBE_STORE)
    os.makedirs(PROBE_STORE, exist_ok=True)
    target_id = "cz"
    target_uh = rr._load(os.path.join(MODREG, "cz.sealed.json"))["u_hash"]

    trials = [
        # 정답 분해: cz_rediscovered(H·CNOT·H) — 봉인 & u_hash==cz → reward>0
        ("cz_rediscovered", "valid-decomposition", "cz_rediscovered.app.pg"),
        # reward-hacking teeth: bell — 봉인되지만 u_hash≠cz(다른 유니터리) → reward=0
        ("bell", "reward-hack(different unitary, still seals)", "bell.app.pg"),
        # teeth 2: swap_via_cnot — 봉인되지만 u_hash≠cz → reward=0
        ("swap_via_cnot", "reward-hack(different unitary)", "swap_via_cnot.app.pg"),
    ]
    results = []
    for cand_id, kind, spec_file in trials:
        sp = os.path.join(SPECS_APPS, spec_file)
        if not os.path.exists(sp):
            results.append({"candidate": cand_id, "kind": kind, "reward": None, "reason": "spec-missing"})
            continue
        r = oracle_reward(sp, target_uh, PROBE_STORE)
        results.append({"candidate": cand_id, "kind": kind, **r})

    # 정답은 reward>0, reward-hack 후보(다른 유니터리)는 전부 reward==0 이어야 함
    valid = next(r for r in results if r["candidate"] == "cz_rediscovered")
    hacks = [r for r in results if "reward-hack" in r["kind"]]
    teeth_ok = (valid["reward"] > 0) and all(h["reward"] == 0.0 for h in hacks)

    print("=" * 86)
    print("ExploitAxis HardRewardOracle (W2.2) — 실제 오라클 reward + reward-hacking 구조차단 teeth")
    print("=" * 86)
    print(f"타깃 유니터리 = cz (u_hash={target_uh[:16]})")
    for r in results:
        mark = "✓" if (("reward-hack" in r["kind"] and r["reward"] == 0.0) or
                       ("valid" in r["kind"] and r["reward"] > 0)) else "✗"
        print(f"  {mark} {r['candidate']:16} reward={r['reward']} sealed={r.get('sealed')} "
              f"u={r.get('u_hash')} — {r['reason']}")
    print(f"\n  reward-hacking 차단: 봉인되어도 u_hash≠target 이면 reward=0 "
          f"(가짜 자원절감으로 유니터리 변조 불가)")

    # 임시 store 정리 (registry 오염 0 확인)
    probe_files = sorted(os.path.basename(f) for f in glob.glob(os.path.join(PROBE_STORE, "*.sealed.json")))
    shutil.rmtree(PROBE_STORE)
    out = {"_schema": "exploit-axis-reward-v1", "target": target_id, "target_u_hash": target_uh,
           "trials": results, "reward_hacking_teeth_pass": teeth_ok,
           "probe_store_files": probe_files, "probe_store_cleaned": True,
           "_note": "HardReward=오라클 봉인 하드게이트. 정답분해(cz_rediscovered)는 봉인&u_hash==cz→reward>0. "
                    "reward-hack 후보(bell/swap_via_cnot)는 봉인되더라도 u_hash≠cz→reward=0 → 유니터리 변조로 "
                    "자원만 줄이는 가짜보상 구조적 불가. 임시 store 재봉인(registry 불변)."}
    json.dump(out, open(os.path.join(OUT, "EXPLOIT-AXIS-REWARD.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("-" * 86)
    print(f"reward-hacking teeth {'PASS ✅' if teeth_ok else 'FAIL ✗'} · "
          f"임시 store 정리완료({len(probe_files)}건 재봉인→삭제) · → .pgf/discover/EXPLOIT-AXIS-REWARD.json")
    return 0 if teeth_ok else 1


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "probe"
    fn = {"probe": cmd_probe, "reward": cmd_reward}.get(cmd, cmd_probe)
    return fn()


if __name__ == "__main__":
    sys.exit(main())
