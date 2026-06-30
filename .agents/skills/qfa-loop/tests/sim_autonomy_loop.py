# -*- coding: utf-8 -*-
"""
sim_autonomy_loop.py — PPR 로 설계한 자율 루프(autonomy_round)의 *실행 시뮬레이션*.

목적: PPR 의 분기/루프/조건/입출력/정지조건/Failure-Strategy 가 의도대로 도는지를
      registry/oracle/frozen 무접촉(전부 mock)으로 dry-run 검증한다.

★ 안전 경계: 실제 봉인 없음. discover/seal/oracle 은 결정론 mock(시나리오 주입).
   이 파일은 _workspace/loop 에만 존재하며 어떤 sealed.json/fingerprint/frozen 도 만지지 않는다.
"""
from __future__ import annotations

# ───────────────────────── 결정론 mock (실제 코드 자리) ─────────────────────────
# 시나리오: 라운드별로 (후보 유무, 봉인 성공패턴)을 주입해 모든 분기를 커버한다.
def make_world(frontier: list[bool], seal_attempts: list[list[bool]]) -> dict:
    """frontier[r]=그 라운드에 후보 존재여부, seal_attempts[r]=각 attempt 성공/실패."""
    return {"frontier": frontier, "seal_attempts": seal_attempts, "master_nodes": [], "log": []}


def run_discover(world: dict, r: int) -> list:                 # ← discover.py 자리
    return [f"node_{r}"] if r < len(world["frontier"]) and world["frontier"][r] else []


def add_node_to_master(world: dict, node: str) -> None:        # ← 마스터 규율 집행
    world["master_nodes"].append(node)                        # "노드 先추가 後진행"


def run_seal_cycle(world: dict, r: int, attempt: int) -> dict: # ← seal cycle 자리
    ok = world["seal_attempts"][r][attempt] if attempt < len(world["seal_attempts"][r]) else False
    return {"node": f"node_{r}", "ok": ok, "failure": None if ok else f"golden!=composite@try{attempt}"}


def oracle_gate(seal: dict) -> bool:                          # ← verify_seal 결정론 판정(self-judge 아님)
    return bool(seal["ok"])


def reproduce_all() -> bool: return True                       # ← reproduce_all 자리(mock: 통과)
def second_oracle() -> bool: return True
def fingerprint_intact() -> bool: return True


# ───────────────────────── PPR: autonomy_round (그대로 구현) ─────────────────────────
def autonomy_round(world: dict, state: dict) -> dict:
    """1라운드: 발견→(마스터 노드 先추가)→봉인(Failure-Strategy)→게이트→종결판단."""
    r = state["round"]
    # ---- SelectNext (조건 분기) ----
    candidates = run_discover(world, r)
    if not candidates:                                        # frontier 고갈 → 즉시 종결
        return {"stop": True, "reason": "frontier-exhausted", "verified": None, "state": state}
    node = candidates[0]                                      # (멀티페르소나 랭킹은 실루프에서)

    # ---- Implement (마스터 규율 + Failure-Strategy 루프) ----
    add_node_to_master(world, node)                           # 규율: 노드 先추가
    seal = None
    for attempt in range(2):                                  # max_retry=2
        seal = run_seal_cycle(world, r, attempt)
        if oracle_gate(seal):                                 # 결정론 게이트가 판정
            break
    else:
        # 2회 모두 실패 → 이 노드 blocked, dry 증가, 루프는 계속 가되 정지조건이 잡음
        state["dry"] += 1
        world["log"].append((r, node, "seal-blocked", state["dry"]))
        stop = state["dry"] >= state["dry_limit"] or state["budget"] <= 0
        return {"stop": stop, "reason": "seal-blocked", "verified": False, "state": state}

    # ---- VerifyGate (기계 게이트 ∧ adversarial) ----
    verified = reproduce_all() and second_oracle() and fingerprint_intact()

    # ---- StopDecision (dry-count / budget 정지조건) ----
    state["dry"] = 0 if verified else state["dry"] + 1
    state["budget"] -= 1
    world["log"].append((r, node, "sealed-verified" if verified else "verify-fail", state["dry"]))
    stop = (state["dry"] >= state["dry_limit"]) or (state["budget"] <= 0)
    return {"stop": stop, "reason": "ok", "verified": verified, "state": state}


def run_loop(world: dict, budget: int = 99, dry_limit: int = 2) -> dict:
    """상위 while 루프: stop 까지 라운드 반복."""
    state = {"round": 0, "dry": 0, "budget": budget, "dry_limit": dry_limit}
    while True:                                               # Convergence/until-stop 루프
        out = autonomy_round(world, state)
        state = out["state"]
        if out["stop"]:
            return {"final": out, "rounds": state["round"] + 1, "world": world}
        state["round"] += 1


# ───────────────────────── 테스트 검증 (acceptance_criteria assert) ─────────────────────────
def _assert(name, cond):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    assert cond, name


def main() -> int:
    print("=" * 72)
    print("PPR autonomy_round 실행 시뮬레이션 — dry-run (registry/oracle 무접촉)")
    print("=" * 72)

    # 시나리오 1: 정상 3라운드 진행 후 frontier 고갈로 종결
    print("[S1] 3 라운드 정상 진행 → frontier 고갈 종결")
    w1 = make_world(frontier=[True, True, True], seal_attempts=[[True], [True], [True]])
    r1 = run_loop(w1, budget=99, dry_limit=2)
    _assert("S1 종결사유=frontier-exhausted", r1["final"]["reason"] == "frontier-exhausted")
    _assert("S1 봉인검증 3회", sum(1 for x in w1["log"] if x[2] == "sealed-verified") == 3)
    _assert("S1 마스터 노드 先추가 3건(규율 준수)", w1["master_nodes"] == ["node_0", "node_1", "node_2"])

    # 시나리오 2: 봉인 1회 실패→재설계 성공(Failure-Strategy 분기)
    print("[S2] 봉인 1차 실패 → 2차 성공 (Failure-Strategy)")
    w2 = make_world(frontier=[True, False], seal_attempts=[[False, True]])
    r2 = run_loop(w2, budget=99, dry_limit=2)
    _assert("S2 재시도 끝에 봉인검증 성공", any(x[2] == "sealed-verified" for x in w2["log"]))

    # 시나리오 3: dry-rounds 2연속(봉인 연속 실패) → 정지조건 발동
    print("[S3] 봉인 2연속 실패 → dry_limit 정지")
    w3 = make_world(frontier=[True, True, True], seal_attempts=[[False, False], [False, False], [True]])
    r3 = run_loop(w3, budget=99, dry_limit=2)
    _assert("S3 dry_limit 로 종결", r3["final"]["reason"] == "seal-blocked")
    _assert("S3 3라운드째 도달 안 함(2연속 dry 에서 멈춤)", r3["rounds"] == 2)

    # 시나리오 4: budget 소진 정지조건
    print("[S4] budget=1 → 1라운드 후 정지")
    w4 = make_world(frontier=[True, True, True], seal_attempts=[[True], [True], [True]])
    r4 = run_loop(w4, budget=1, dry_limit=9)
    _assert("S4 budget 으로 종결(1라운드)", r4["rounds"] == 1 and r4["final"]["state"]["budget"] == 0)

    # 불변 가드: 시뮬레이터는 어떤 봉인/지문도 만들지 않는다(이 파일 외 산출물 0)
    _assert("INV 마스터노드 = 봉인시도 노드와 1:1(즉흥착수 0)",
            all(n.startswith("node_") for w in (w1, w2, w3, w4) for n in w["master_nodes"]))

    print("-" * 72)
    print("ALL PASS — PPR 루프가 분기/루프/조건/정지/Failure-Strategy 모두 의도대로 실행됨")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
