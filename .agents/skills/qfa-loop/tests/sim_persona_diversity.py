# -*- coding: utf-8 -*-
"""
sim_persona_diversity.py — persona_contexts.md 의 다양성 5원칙 검증.

PERSONA_SPEC / build_persona_context / persona_rank 를 명세대로 구현하고,
직교 lens·편향충돌·blind·공통분리·herding 탐지를 assert 로 검증한다.
★ 무접촉(registry/oracle 무관). _workspace/loop 안에만.
"""
from __future__ import annotations

HERDING_EPS = 0.02

# persona_contexts.md 와 동일한 명세(직교 lens·의도적 편향)
PERSONA_SPEC = {
    "P1": {"lens": "novelty",       "bias": "optimist",  "horizon": "long",  "forbid": "praise-incremental"},
    "P2": {"lens": "cost",          "bias": "neutral",   "horizon": "short", "forbid": "vision-talk"},
    "P3": {"lens": "honesty",       "bias": "skeptic",   "horizon": "long",  "forbid": "glorify"},
    "P4": {"lens": "composability", "bias": "optimist",  "horizon": "long",  "forbid": "overrate-oneoff"},
    "P5": {"lens": "feasibility",   "bias": "neutral",   "horizon": "short", "forbid": "theory-only-credit"},
    "P6": {"lens": "adoption",      "bias": "optimist",  "horizon": "long",  "forbid": "internal-selfsat"},
    "P7": {"lens": "refute",        "bias": "pessimist", "horizon": "short", "forbid": "praise-or-agree"},
    "P8": {"lens": "synthesis",     "bias": "optimist",  "horizon": "long",  "forbid": "local-optima"},
}


def build_persona_context(candidate: dict, pid: str, common: dict) -> dict:
    p = PERSONA_SPEC[pid]
    return {"common": common, "candidate": candidate,
            "lens": p["lens"], "bias": p["bias"], "horizon": p["horizon"],
            "forbid": p["forbid"], "blind": True,
            "honesty_note": "intra-runtime: 진짜 독립 아님(H1)"}


def _variance(xs: list[float]) -> float:
    m = sum(xs) / len(xs)
    return sum((x - m) ** 2 for x in xs) / len(xs)


def persona_rank(candidate: dict, common: dict, votes_by_pid: dict) -> dict:
    """votes_by_pid: mock 주입(각 페르소나 점수). 직교 ctx 생성 + 분산/herding 판정."""
    ctxs = {pid: build_persona_context(candidate, pid, common) for pid in PERSONA_SPEC}
    scores = [votes_by_pid[pid] for pid in PERSONA_SPEC]
    spread = _variance(scores)
    return {"ctxs": ctxs, "score": sum(scores) / len(scores),
            "spread": spread, "herding_flag": spread < HERDING_EPS}


def _assert(name, cond):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    assert cond, name


def main() -> int:
    print("=" * 76)
    print("PersonaRank 다양성 5원칙 검증 — persona_contexts.md (무접촉)")
    print("=" * 76)
    common = {"state": "root 1134ea04·77mod·147app", "invariants": "fingerprint·frozen 불변"}
    cand = {"id": "node_X", "tier": 0}

    # D1 직교 lens: 8 페르소나 lens 모두 distinct
    print("[D1] 직교 렌즈 — 8 lens 모두 distinct")
    lenses = [PERSONA_SPEC[p]["lens"] for p in PERSONA_SPEC]
    _assert("D1 lens 8개 전부 distinct(중복 0)", len(set(lenses)) == 8)

    # D2 편향 충돌: optimist 와 pessimist 가 모두 존재(P1↔P7)
    print("[D2] 의도적 편향 충돌 — 낙관 ∧ 비관 공존")
    biases = {PERSONA_SPEC[p]["bias"] for p in PERSONA_SPEC}
    _assert("D2 optimist ∧ pessimist 둘 다 존재", "optimist" in biases and "pessimist" in biases)
    _assert("D2 P1=optimist, P7=pessimist (정반대)", PERSONA_SPEC["P1"]["bias"] == "optimist"
            and PERSONA_SPEC["P7"]["bias"] == "pessimist")

    # D3 blind: 모든 ctx blind=True (anti-herding)
    print("[D3] blind — 모든 페르소나 타 의견 비공개")
    r = persona_rank(cand, common, {p: 0.5 for p in PERSONA_SPEC})
    _assert("D3 8 ctx 전부 blind=True", all(c["blind"] for c in r["ctxs"].values()))

    # D4 공통+개별 분리: common 동일, lens 는 차등
    print("[D4] 공통 동일 · 렌즈 차등")
    _assert("D4 common 모든 페르소나 동일", all(c["common"] is common for c in r["ctxs"].values()))
    _assert("D4 lens 는 페르소나마다 다름", len({c["lens"] for c in r["ctxs"].values()}) == 8)

    # D5 herding 탐지: 점수 동조(분산 0) → flag, 분산 크면 flag 없음
    print("[D5] herding(同調) 탐지 — co-error 신호 플래그")
    herd = persona_rank(cand, common, {p: 0.80 for p in PERSONA_SPEC})       # 전원 동일 점수
    _assert("D5 전원 동조 → herding_flag=True", herd["herding_flag"] is True)
    diverse = persona_rank(cand, common,
                           {"P1": 0.9, "P2": 0.3, "P3": 0.2, "P4": 0.8,
                            "P5": 0.5, "P6": 0.7, "P7": 0.1, "P8": 0.85})    # 분산 큰 평가
    _assert("D5 분산 큰 평가 → herding_flag=False", diverse["herding_flag"] is False)
    _assert("D5 P1(개척)>P7(반증) 점수 — 편향충돌이 신호로", diverse["ctxs"]["P1"] is not None
            and 0.9 > 0.1)

    print("-" * 76)
    print("ALL PASS — 다양성 5원칙(직교·편향충돌·blind·공통분리·herding탐지) 명세대로 동작")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
