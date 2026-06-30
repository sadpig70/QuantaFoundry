# -*- coding: utf-8 -*-
"""
sim_autonomy_loop_v2.py — DESIGN-AutonomyLoop.md 전체 파이프라인의 실행 시뮬레이션.

설계의 PPR(bootstrap→select_next→design_review→implement→verify_gate→guard_check→
stop_controller)을 mock 으로 충실히 구현하고, §7 테스트계획 T1~T9 를 assert 로 검증한다.

★ 안전: registry/verify_seal.py/contracts.py/frozen 무접촉. 전부 결정론 mock(시나리오 주입).
   산출물은 _workspace/loop 안에만.
"""
from __future__ import annotations


# ── world: 라운드별 시나리오 주입 (mock 결정론) ──
def make_world(discover, design_critical, seal_attempts, adversarial, guard, commit_every=1):
    return {"discover": discover, "design_critical": design_critical,
            "seal_attempts": seal_attempts, "adversarial": adversarial, "guard": guard,
            "cfg": {"commit_every": commit_every},
            "master_nodes": [], "implemented": [], "log": [],
            "syncs": [], "doc_syncs": [], "commits": [], "pushes": []}


def _get(seq, r, default):
    return seq[r] if r < len(seq) else default


# ── 설계 PPR 의 mock 구현 ──
def bootstrap(state):                                   # INV6: 정지조건 부재 시 거부
    if not (state["dry_limit"] > 0 and state["budget"] > 0):
        raise RuntimeError("정지조건 부재 — 루프 거부 (INV6)")
    base = {"fp": ("V0", "C0", "F0"), "ext": ("R0", "E0", "T0")}   # mock 기준선 스냅샷
    return state, base


def select_next(world, r):                              # SelectNext (+ persona_rank 합의)
    cands = _get(world["discover"], r, False)
    return f"node_{r}" if cands else None               # None = frontier-exhausted


def design_review(world, r):                            # PlanNode: Critical=0 게이트
    return {"critical_zero": _get(world["design_critical"], r, True)}


def implement(world, r, max_retry=2):                   # Implement: Failure-Strategy 루프
    world["master_nodes"].append(f"node_{r}")           # INV4: 先추가
    world["implemented"].append(f"node_{r}")
    attempts = _get(world["seal_attempts"], r, [True])
    for attempt in range(max_retry):
        if attempt < len(attempts) and attempts[attempt]:
            return {"sealed": True, "seal": f"seal_{r}"}  # oracle_gate(기계) 통과
    return {"sealed": False, "blocked": f"node_{r}"}


def verify_gate(world, r):                              # VerifyGate: 기계 ∧ adversarial
    machine = True                                      # mock: reproduce_all 등 통과
    survived = _get(world["adversarial"], r, True)      # 회의주의자 다수 생존?
    return {"verified": machine and survived}


def guard_check(world, r, base):                        # GuardCheck: 불변 byte-identical
    return _get(world["guard"], r, True)                # False = 불변 위반(치명)


def sync_checkpoint(world, state, verified, final=False):  # SyncCheckpoint (C, verified-only)
    cfg = world["cfg"]
    due = final or (state["round"] % cfg["commit_every"] == 0)
    if not due:
        return
    world["syncs"].append((state["round"], "final" if final else "periodic"))
    world["doc_syncs"].append(state["round"])           # 외부 3종 batch (INV5 위임)
    if verified:                                        # verified-only: reproduce_all 통과분만
        world["commits"].append(state["round"])
        world["pushes"].append(state["round"])          # 외부공개(C 위임)


def stop_controller(state):                             # 정지조건 OR 결합 (INV6)
    return (state["dry"] >= state["dry_limit"] or state["budget"] <= 0
            or state["frontier_exhausted"] or state["guard_violation"])


def autonomy_round(world, state, base):
    r = state["round"]
    node = select_next(world, r)
    if node is None:
        state["frontier_exhausted"] = True
        world["log"].append((r, "frontier-exhausted"))
        return {"stop": True, "reason": "frontier-exhausted", "state": state}

    if not design_review(world, r)["critical_zero"]:
        state["dry"] += 1
        world["log"].append((r, "design-critical"))
        return {"stop": stop_controller(state), "reason": "design-critical", "state": state}

    impl = implement(world, r)
    if not impl["sealed"]:
        state["dry"] += 1
        world["log"].append((r, "seal-blocked"))
        return {"stop": stop_controller(state), "reason": "seal-blocked", "state": state}

    vg = verify_gate(world, r)
    if not guard_check(world, r, base):                 # 치명: budget 무관 즉시 종결
        state["guard_violation"] = True
        world["log"].append((r, "guard-violation"))
        return {"stop": True, "reason": "guard-violation", "state": state}

    verified = vg["verified"]
    state["dry"] = 0 if verified else state["dry"] + 1
    state["budget"] -= 1
    world["log"].append((r, "sealed-verified" if verified else "verify-fail"))
    sync_checkpoint(world, state, verified)             # 적정시기 동기화·커밋·푸쉬(C)
    return {"stop": stop_controller(state), "reason": "ok", "verified": verified, "state": state}


def run_autonomy_loop(world, budget=8, dry_limit=2):
    state = {"round": 0, "dry": 0, "dry_limit": dry_limit, "budget": budget,
             "frontier_exhausted": False, "guard_violation": False}
    state, base = bootstrap(state)
    while True:
        out = autonomy_round(world, state, base)
        state = out["state"]
        if out["stop"]:
            sync_checkpoint(world, state, out.get("verified", False), final=True)  # 종결 최종 1회
            return {"stopped_by": out["reason"], "rounds": state["round"] + 1, "world": world}
        state["round"] += 1


# ── 검증 (T1~T9) ──
def _assert(name, cond):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    assert cond, name


def main() -> int:
    print("=" * 76)
    print("AutonomyLoop 전체 파이프라인 시뮬레이션 — T1~T9 (registry/oracle 무접촉)")
    print("=" * 76)
    T = lambda n: True

    # T1 정상 3라운드 → frontier 고갈
    print("[T1] 정상 3라운드 → frontier-exhausted")
    w = make_world([True]*3, [], [[True]]*3, [True]*3, [True]*3)
    r = run_autonomy_loop(w)
    _assert("T1 종결=frontier-exhausted", r["stopped_by"] == "frontier-exhausted")
    _assert("T1 봉인검증 3회", sum(1 for x in w["log"] if x[1] == "sealed-verified") == 3)

    # T2 design-critical → dry 증가
    print("[T2] design-critical 2연속 → dry_limit 종결")
    w = make_world([True]*3, [False, False, True], [[True]]*3, [True]*3, [True]*3)
    r = run_autonomy_loop(w, dry_limit=2)
    _assert("T2 종결=design-critical(dry)", r["stopped_by"] == "design-critical")
    _assert("T2 2라운드에서 멈춤", r["rounds"] == 2)
    _assert("T2 봉인시도 0(설계서 막힘)", w["implemented"] == [])

    # T3 봉인 1차 실패 → 2차 성공
    print("[T3] 봉인 1차 실패 → 2차 성공 (Failure-Strategy)")
    w = make_world([True, False], [True], [[False, True]], [True], [True])
    r = run_autonomy_loop(w)
    _assert("T3 재시도 끝 봉인검증", any(x[1] == "sealed-verified" for x in w["log"]))

    # T4 봉인 연속 실패 → dry_limit
    print("[T4] 봉인 2연속 실패 → dry_limit 종결")
    w = make_world([True]*3, [True]*3, [[False, False], [False, False], [[True]]], [True]*3, [True]*3)
    r = run_autonomy_loop(w, dry_limit=2)
    _assert("T4 종결=seal-blocked", r["stopped_by"] == "seal-blocked")
    _assert("T4 2라운드에서 멈춤", r["rounds"] == 2)

    # T5 budget 소진
    print("[T5] budget=1 → 1라운드 후 종결")
    w = make_world([True]*3, [True]*3, [[True]]*3, [True]*3, [True]*3)
    r = run_autonomy_loop(w, budget=1, dry_limit=9)
    _assert("T5 종결=ok(budget 소진)", r["rounds"] == 1)

    # T6 guard-violation → budget 무관 즉시 종결
    print("[T6] guard-violation(2라운드째) → budget 무관 즉시 종결")
    w = make_world([True]*5, [True]*5, [[True]]*5, [True]*5, [True, False, True, True, True])
    r = run_autonomy_loop(w, budget=99, dry_limit=9)
    _assert("T6 종결=guard-violation", r["stopped_by"] == "guard-violation")
    _assert("T6 2라운드에서 즉시 멈춤(budget 남아도)", r["rounds"] == 2)

    # T7 verify-fail(adversarial 탈락) → dry
    print("[T7] verify-fail 2연속(기계OK·adversarial 탈락) → dry_limit")
    w = make_world([True]*3, [True]*3, [[True]]*3, [False, False, True], [True]*3)
    r = run_autonomy_loop(w, dry_limit=2)
    _assert("T7 종결=ok/verify-fail 누적 dry", r["rounds"] == 2 and
            sum(1 for x in w["log"] if x[1] == "verify-fail") == 2)

    # T8 INV: 마스터노드 = 봉인시도 1:1 (즉흥착수 0)
    print("[T8] 마스터노드 = 봉인시도 노드 1:1 (즉흥착수 0)")
    w = make_world([True]*3, [True, False, True], [[True]]*3, [True]*3, [True]*3)
    r = run_autonomy_loop(w, dry_limit=9)
    _assert("T8 master_nodes == implemented (1:1)", w["master_nodes"] == w["implemented"])
    _assert("T8 design-critical 노드는 마스터 추가 안 됨", "node_1" not in w["master_nodes"])

    # T9 bootstrap: 정지조건 부재 → 루프 거부
    print("[T9] 정지조건 부재(dry_limit=0) → 루프 거부 (INV6)")
    refused = False
    try:
        run_autonomy_loop(make_world([True], [], [[True]], [True], [True]), dry_limit=0)
    except RuntimeError:
        refused = True
    _assert("T9 정지조건 부재 시 RuntimeError 로 거부", refused)

    # T10 SyncCheckpoint K=2 주기 발화
    print("[T10] SyncCheckpoint commit_every=2 → round 0,2,4 주기 발화")
    w = make_world([True]*9, [True]*9, [[True]]*9, [True]*9, [True]*9, commit_every=2)
    r = run_autonomy_loop(w, budget=5, dry_limit=9)
    periodic = [s[0] for s in w["syncs"] if s[1] == "periodic"]
    _assert("T10 주기 발화 round 0,2,4", periodic == [0, 2, 4])
    _assert("T10 종결 시 final sync 1회", sum(1 for s in w["syncs"] if s[1] == "final") == 1)

    # T11 verified-only: verify-fail 라운드는 commit/push 제외
    print("[T11] verify-fail 라운드는 commit/push 제외 (doc_sync 는 수행)")
    w = make_world([True, True, True, False], [True]*3, [[True]]*3, [True, False, True], [True]*3, commit_every=1)
    r = run_autonomy_loop(w, budget=99, dry_limit=9)
    _assert("T11 commit 은 verified 라운드만(0,2)", w["commits"] == [0, 2])
    _assert("T11 push==commit (verified-only)", w["pushes"] == [0, 2])
    _assert("T11 doc_sync 는 verify-fail(1) 포함", 1 in w["doc_syncs"])

    # T12 종결 시 final sync 보장
    print("[T12] 종결 시 final sync 1회 보장 (commit_every 커도)")
    w = make_world([True, True, False], [True]*2, [[True]]*2, [True]*2, [True]*2, commit_every=99)
    r = run_autonomy_loop(w, budget=99, dry_limit=9)
    _assert("T12 final sync 존재", any(s[1] == "final" for s in w["syncs"]))

    print("-" * 76)
    print("ALL PASS — 설계 PPR 의 분기·루프·조건·정지·불변가드 전부 의도대로 실행됨")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
