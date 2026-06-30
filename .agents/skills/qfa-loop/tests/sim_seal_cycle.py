# -*- coding: utf-8 -*-
"""
sim_seal_cycle.py — DESIGN §8.1 SealCycle / §8.2 MachineGate 정교화 검증.

표준 봉인 사이클의 분기(신규모듈 INDEP·honest 분해·prototype 선확인)와
게이트 순서·short-circuit 을 mock 으로 검증한다.
★ registry/oracle 무접촉. _workspace/loop 안에만.
"""
from __future__ import annotations


# ── §8.1 SealCycle (mock) ──
def seal_cycle(node: dict) -> dict:
    trace = node.setdefault("trace", [])
    if node.get("complex"):
        trace.append("sub_design")
    if not node.get("prototype_ok", True):
        return {"sealed": False, "failure": "prototype-mismatch", "trace": trace}
    trace.append("gen_family")
    if node.get("has_matrixgate"):                        # honest 분해 위반
        return {"sealed": False, "failure": "MatrixGate-detected", "trace": trace}
    trace.append("forge_register")
    if node.get("new_module"):                            # 분기: 신규모듈만 INDEP
        trace.append("second_oracle_indep")
        if not node.get("indep_ok", True):
            return {"sealed": False, "failure": "indep-oracle-mismatch", "trace": trace}
    ok = node.get("seal_ok", True) and node.get("tier") is not None and node.get("deterministic", True)
    return {"sealed": ok, "failure": None, "trace": trace}


# ── §8.2 MachineGate (mock) ──
def machine_gate(results: dict) -> dict:
    calls = []
    for name in ("reproduce_all", "second_oracle", "seal_gate_ci", "contested_guard"):
        calls.append(name)
        if not results.get(name, True):                   # 첫 실패 short-circuit
            return {"machine": False, "failed_at": name, "calls": calls}
    return {"machine": True, "failed_at": None, "calls": calls}


def _assert(name, cond):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    assert cond, name


def main() -> int:
    print("=" * 76)
    print("SealCycle(§8.1) / MachineGate(§8.2) 정교화 검증 — 무접촉")
    print("=" * 76)

    # SC1 신규모듈 → IndepOracle 수행
    print("[SC1] 신규모듈 후보 → second_oracle INDEP 수행")
    r = seal_cycle({"new_module": True, "tier": 0, "complex": True})
    _assert("SC1 sealed=True", r["sealed"])
    _assert("SC1 INDEP 수행됨", "second_oracle_indep" in r["trace"])
    _assert("SC1 복잡후보 sub_design 수행", "sub_design" in r["trace"])

    # SC2 기존부품 재사용(순수 조립, shor1285 류) → INDEP 스킵
    print("[SC2] 기존부품 재사용 → INDEP 스킵")
    r = seal_cycle({"new_module": False, "tier": 1, "complex": False})
    _assert("SC2 sealed=True", r["sealed"])
    _assert("SC2 INDEP 스킵", "second_oracle_indep" not in r["trace"])

    # SC3 prototype mismatch → 거부
    print("[SC3] prototype 불일치 → 봉인 거부")
    r = seal_cycle({"new_module": False, "tier": 0, "prototype_ok": False})
    _assert("SC3 sealed=False·prototype-mismatch", not r["sealed"] and r["failure"] == "prototype-mismatch")

    # SC4 MatrixGate 검출 → 거부(honest 분해 위반)
    print("[SC4] MatrixGate 검출 → 거부(honest 분해)")
    r = seal_cycle({"new_module": True, "tier": 0, "has_matrixgate": True})
    _assert("SC4 sealed=False·MatrixGate-detected", not r["sealed"] and r["failure"] == "MatrixGate-detected")
    _assert("SC4 forge_register 도달 안 함", "forge_register" not in r["trace"])

    # SC5 신규모듈 INDEP 불일치 → 거부
    print("[SC5] 신규모듈 INDEP 불일치 → 거부")
    r = seal_cycle({"new_module": True, "tier": 0, "indep_ok": False})
    _assert("SC5 sealed=False·indep-oracle-mismatch", not r["sealed"] and r["failure"] == "indep-oracle-mismatch")

    # MG1 전 게이트 PASS
    print("[MG1] 전 게이트 PASS → machine=True")
    r = machine_gate({})
    _assert("MG1 machine=True·4게이트 호출", r["machine"] and len(r["calls"]) == 4)

    # MG2 G2 실패 → short-circuit(G3/G4 미호출)
    print("[MG2] second_oracle 실패 → short-circuit")
    r = machine_gate({"second_oracle": False})
    _assert("MG2 machine=False·failed_at=second_oracle", not r["machine"] and r["failed_at"] == "second_oracle")
    _assert("MG2 short-circuit(G3/G4 미호출)", r["calls"] == ["reproduce_all", "second_oracle"])

    print("-" * 76)
    print("ALL PASS — SealCycle 분기(INDEP·honest·prototype) + MachineGate 순서/short-circuit 정확")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
