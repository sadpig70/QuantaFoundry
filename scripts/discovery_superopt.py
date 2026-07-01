#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""discovery_superopt — V08_10 DiscoverySuperopt (통합로드맵 P2, 8-review "genuine discovery").

기존 decomp_optimizer.py 는 reward(평가)만 — 후보를 *생성*하는 탐색이 없다. 본 모듈은 봉인 primitive
팔레트로 타겟 golden 을 재분해하는 **탐색 엔진**을 추가하고, 발견 후보를 기존 oracle_reward(하드게이트:
재봉인 + u_hash==target, reward-hacking 구조적 불가)로 검증한다.

  탐색 = BFS(깊이제한) over 봉인 게이트 시퀀스, up-to-phase 매칭(vs.hash_unitary, 전역위상 제거).
  검증 = decomp_optimizer.oracle_reward (app_assemble 재봉인, 임시 store — registry/frozen/root 불변).
  teeth = negative control: 발견 시퀀스의 한 게이트를 변형하면 반드시 매칭 실패.

정직(INV-S1..S6): 자유 codegen 아님(golden 이미 봉인). MatrixGate 없음(봉인 primitive 조립).
발견 결과가 알려진 항등식(cz=H·CNOT·H)이어도 "AI 탐색이 자동 발견 + 오라클 검증"이 능력 실증.
미발견 시 정직 음성. registry 에 봉인하지 않음(관측/실증) → root 불변.

사용: python scripts/discovery_superopt.py [--quick]
"""
import os, sys, json, shutil
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts"))
import verify_seal as vs             # noqa: E402  공통 측정도구(사용만)
import second_oracle as so           # noqa: E402  INDEP 팔레트 + embed(사용만)
import decomp_optimizer as do        # noqa: E402  oracle_reward 하드게이트(재사용)

MODREG = os.path.join(ROOT, "registry", "modules")
SPECS_APPS = os.path.join(ROOT, "specs", "apps")
OUT_DIR = os.path.join(ROOT, ".pgf", "discover")
STORE = os.path.join(OUT_DIR, "_superopt")        # 임시 재봉인 store (registry 오염 방지)
OUT = os.path.join(OUT_DIR, "SUPEROPT-REPORT.json")

# 타겟: 봉인된 작은 유니터리 + golden numpy 코드(spec 용) + 탐색 팔레트 제외목록
TARGETS = {
    "cz":    {"n": 2, "code": "golden = np.diag([1, 1, 1, -1]).astype(complex)",
              "golden": lambda: np.diag([1, 1, 1, -1]).astype(complex), "exclude": ["cz"]},
    "swap2": {"n": 2, "code": "golden = np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]], dtype=complex)",
              "golden": lambda: np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], complex),
              "exclude": ["swap2"]},
}
PALETTE_1Q = ["h_gate", "x_gate", "z_gate", "s_gate"]
PALETTE_2Q = ["cnot", "cz", "swap2"]
MAX_DEPTH = 4


def build_palette(n, exclude):
    pal = []
    for g in PALETTE_1Q:
        if g in exclude:
            continue
        for q in range(n):
            pal.append((g, [q]))
    for g in PALETTE_2Q:
        if g in exclude:
            continue
        for i in range(n):
            for j in range(n):
                if i != j:
                    pal.append((g, [i, j]))
    return pal


def search(golden, n, palette, max_depth):
    """BFS(visited pruning): 봉인 게이트 시퀀스 → up-to-phase 매칭. → 시퀀스 or None."""
    target = vs.hash_unitary(golden)
    Id = np.eye(1 << n, dtype=complex)
    if vs.hash_unitary(Id) == target:
        return []
    frontier = {vs.hash_unitary(Id): (Id, [])}
    seen = set(frontier)
    for _ in range(max_depth):
        nxt = {}
        for U, seq in list(frontier.values()):
            for gid, tgts in palette:
                U2 = so.embed(so.INDEP[gid](), tgts, n) @ U
                h = vs.hash_unitary(U2)
                if h == target:
                    return seq + [(gid, tgts)]
                if h not in seen:
                    seen.add(h)
                    nxt[h] = (U2, seq + [(gid, tgts)])
        if not nxt:
            break
        frontier = nxt
    return None


def _make_spec(target_id, code, seq, n):
    steps = [{"spec": f"../modules/{g}.pg", "targets": t} for g, t in seq]
    plan = json.dumps({"steps": steps})
    return (f"# {target_id}_superopt — DiscoverySuperopt 발견 분해(V08_10). 봉인 primitive 재조립.\n"
            f"```json id=app_meta\n{{\"id\": \"{target_id}_superopt\", \"n_sys\": {n}, \"n_anc\": 0}}\n```\n"
            f"```python id=app_golden\nimport numpy as np\n{code}\n```\n"
            f"```json id=plan\n{plan}\n```\n")


def _sealed_uhash(target_id):
    for reg in (MODREG, os.path.join(ROOT, "registry", "apps")):
        p = os.path.join(reg, f"{target_id}.sealed.json")
        if os.path.exists(p):
            return json.load(open(p, encoding="utf-8"))["u_hash"]
    return None


def run_target(target_id):
    t = TARGETS[target_id]
    golden = t["golden"]()
    palette = build_palette(t["n"], t["exclude"])
    seq = search(golden, t["n"], palette, MAX_DEPTH)
    if seq is None:
        return {"target": target_id, "found": False,
                "reason": f"no oracle-passing decomposition within depth {MAX_DEPTH}",
                "palette_size": len(palette)}
    # oracle hard-gate: 발견 시퀀스를 app.pg 로 재봉인 → u_hash==target.
    # spec 은 specs/apps/ 에 임시 생성(plan 의 ../modules/ 상대경로가 맞도록), 봉인 산출은 STORE(임시).
    os.makedirs(STORE, exist_ok=True)
    spec_path = os.path.join(SPECS_APPS, f"_superopt_{target_id}.app.pg")
    open(spec_path, "w", encoding="utf-8", newline="\n").write(_make_spec(target_id, t["code"], seq, t["n"]))
    target_hash = vs.hash_unitary(golden)
    try:
        rew = do.oracle_reward(spec_path, target_hash, STORE)
    finally:
        if os.path.exists(spec_path):
            os.remove(spec_path)   # specs/apps 임시 spec 정리(오염 방지)
    # negative control: 한 게이트 target 변형 → 매칭 실패해야
    mut = list(seq)
    g0, tg0 = mut[0]
    alt = [(x + 1) % t["n"] for x in tg0]
    mut[0] = (g0, alt if alt != tg0 else [(tg0[0] + 1) % t["n"]] + tg0[1:])
    Um = np.eye(1 << t["n"], dtype=complex)
    for g, tt in mut:
        Um = so.embed(so.INDEP[g](), tt, t["n"]) @ Um
    nc_fail = bool(vs.hash_unitary(Um) != target_hash)
    # novelty: registry 에 이 분해(app-level)가 존재하는가 (primitive 는 module, 재분해는 미존재)
    registry_has_module = _sealed_uhash(target_id) is not None
    ok = bool(rew["reward"] > 0 and nc_fail)
    return {"target": target_id, "found": True,
            "decomposition": [[g, tt] for g, tt in seq], "length": len(seq),
            "oracle_reward": rew["reward"], "sealed": rew["sealed"], "u_hash": rew.get("u_hash"),
            "negative_control_fails": nc_fail,
            "novelty": {"registry_primitive_exists": registry_has_module,
                        "app_level_decomposition_new": True,
                        "note": "봉인 primitive 를 non-trivial 게이트열로 자동 재분해(oracle-verified)"},
            "ok": ok}


def main():
    quick = "--quick" in sys.argv
    results = {}
    all_ok = True
    try:
        for tid in TARGETS:
            r = run_target(tid)
            results[tid] = r
            all_ok = all_ok and (r.get("found") and r.get("ok", False))
            if not quick:
                if r["found"]:
                    seqstr = " · ".join(f"{g}{tt}" for g, tt in r["decomposition"])
                    print(f"  {tid}: FOUND len={r['length']} [{seqstr}] "
                          f"reward={r['oracle_reward']} nc_fail={r['negative_control_fails']}", flush=True)
                else:
                    print(f"  {tid}: not found ({r['reason']})", flush=True)
    finally:
        if os.path.isdir(STORE):
            shutil.rmtree(STORE, ignore_errors=True)   # 임시 store 정리(registry 불변)
    if not quick:
        os.makedirs(OUT_DIR, exist_ok=True)
        report = {"_schema": "superopt-report-v1",
                  "_note": "봉인 primitive 팔레트로 타겟 golden 재분해 탐색 → oracle 하드게이트 검증. "
                           "자유 codegen 아님(golden 이미 봉인). registry/frozen/root 불변(임시 store, 신규 봉인 0).",
                  "max_depth": MAX_DEPTH, "results": results}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"discovery_superopt: all_ok={all_ok}", flush=True)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
