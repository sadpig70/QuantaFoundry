# DESIGN-QFDiscover — Stage 2 QF-Discover (open-ended 발견 엔진)

> PGF design mode · 기반 = `_legacy/roadmap_process_plan.md` Stage 2 (Track A) · 방법 = PG Gantree + PPR.
> 정직성: 분석/제안 전용 비파괴. registry/sealed/frozen/fingerprint 불변. 신규 봉인은 오라클 경유만.
> 소비 자산(사용만): `goal_autonomy`(detect_gaps/FAMILIES) · `registry_tools`(build_graph/dependents) ·
> `resource_report`(_load/resource) · `app_assemble`(오라클 봉인) · `second_oracle`(독립검증).

---

## 0. 문제 (8-agent 수렴 최약가정)

기존 `goal_autonomy.score()` = `reuse × algo_value × 1/difficulty` — known-family 확장만 점수화.
8-agent 비판: (1) **무엇을 만들지** 선택이 빈약(미명명 실패모드, A3) (2) Novelty 객관근거 부재
(3) 분해 최적화 부재(같은 유니터리의 더 싼 회로 미탐색) (4) 목표선택 co-error 무방어.

QF-Discover = 가치함수(W2.1) + 분해최적화(W2.2) + 목표선택가드(W2.3) + 프리미티브 제안(W2.4).

---

## 1. Gantree

```
QFDiscover // open-ended 발견 엔진 (designing) @v:0.1
    W2.1_ValueFunction // 8항 가치함수 + counterfactual fan-in (designing)
        ValueTerms // Novelty/Sealability/Composability/ResourceΔ/ConsensusEst/Ambiguity/Cost (designing)
        CounterfactualFanIn // 모듈 미봉인 가정 → unlock 후보 수 = Composability 객관근거 (designing)
        CandidateRank // detect_gaps × value → 랭킹 산출 (designing) @dep:ValueTerms,CounterfactualFanIn
        RetroValidate // c6x/sx 사례를 사전 상위랭크로 포착 검증 (needs-verify) @dep:CandidateRank
    W2.3_GoalSelectionGuard // 목표선택 co-error 방어 (designing) @dep:W2.1
        CoverageGate // 동일 capability 중복선택 차단 (designing)
        IndependenceGate // 선택근거가 단일 convention/source 의존 시 경고 (designing)
        SelectionLog // 거부/통과 결정 로그 (designing) @dep:CoverageGate,IndependenceGate
    W2.2_ExploitAxis // 분해 최적화기 (오라클=reward) (designing) @dep:W2.1
        SearchSpace // 타깃 유니터리 고정, 분해 후보 공간 정의 (designing)
        HardReward // 봉인=1 못하면 0 (reward-hacking 구조차단) + resource 연속보상 (designing)
        CoverageGateMCTS // trivial 양산 차단(capability-coverage) (designing) @dep:HardReward
        CheaperDecompProbe // 동일 u_hash·낮은 자원 후보 탐색 실증 (needs-verify) @dep:SearchSpace,HardReward
    W2.4_PrimitiveProposalRound // capability-gap → panel 패키지 (designing) @dep:W2.1 [EXT]
        GapToProposal // value 상위 blocked prereq → 제안서 생성 (designing)
        PanelPackage // 6런타임 배포 패키지(self-contained 부분) (designing) @dep:GapToProposal
```

---

## 2. PPR — W2.1 ValueFunction

```python
# acceptance_criteria:
#   - 8항 가중합, 가중치 roadmap 명세 일치(0.25/0.20/0.20/0.15/0.10/−0.20/−0.15)
#   - 각 항 ∈ [0,1], 객관근거(휴리스틱 상수 금지) — 근거 키를 결과 JSON에 동봉
#   - RetroValidate: c6x counterfactual 시 Composability 최상위 → 사전포착 PASS

def value_function(gap: dict, ctx: DiscoverContext) -> dict:
    """gap(detect_gaps 산물) → 8항 점수 + 근거. ctx = {graph, mods, fanin_table, res_table}."""
    nov   = novelty(gap, ctx)          # GenSkill 재현가능 family 확장=낮음, 신규 prereq 요구=높음
    seal  = sealability(gap, ctx)      # buildable & n≤MAX_N → 1.0; blocked → 1/(1+|missing|)
    comp  = composability(gap, ctx)    # = counterfactual fan-in (이 후보/prereq unlock 후보 수)
    resd  = resource_delta(gap, ctx)   # 1/(1+norm_gatecount); 재사용 marginal=0 → 높음
    cons  = consensus_est(gap, ctx)    # 표준게이트(PROOF_BACKED)만 → 높음, 비표준 → 낮음
    amb   = ambiguity(gap, ctx)        # 표준명칭 family → 낮음, 미명 합성 → 높음 (감점)
    cost  = cost_est(gap, ctx)         # norm_gatecount (감점)
    value = 0.25*nov + 0.20*seal + 0.20*comp + 0.15*resd + 0.10*cons - 0.20*amb - 0.15*cost
    return {"value": round(value,4), "terms": {...}, "evidence": {...}}

def counterfactual_fanin(graph, mods) -> dict:
    """각 봉인모듈 m 을 '미봉인'으로 가정 → detect_gaps 재실행 → m 을 missing_prereq 로
    지목하는 후보 수 = m 의 Composability fan-in. c6x 미봉인 시 cmul2_mod33/35 가 지목 → fan-in≥2.
    객관근거: 휴리스틱 상수 아닌 그래프 구조에서 유도."""
    # for each module m in mods: simulate mods'=mods-{m}; count gaps blocked-by m
    # Composability(gap) = max fanin over gap.missing_modules (blocked) or
    #                      dependents-count of gap (buildable, 미래 재사용 잠재)
```

검증(RetroValidate): `c6x`·`c5x` 등 distinct-prime 게이트를 counterfactual 제거 → 해당 게이트가
fan-in 상위에 포착되는지. sx(√X)는 cross-model 수렴 사례 → ConsensusEst 항이 표준게이트 대비
어떻게 평가하는지 사후 일관성. **사후가 아닌 사전 상위랭크 = 발견엔진 정당성.**

---

## 3. PPR — W2.3 GoalSelectionGuard (A3 고유통찰)

```python
# acceptance_criteria:
#   - 동일 capability(u_hash-equivalent 목표/동일 family-n) 중복선택 거부
#   - 선택근거가 단일 convention(big-endian/atol/전역위상)에만 의존 시 경고 플래그
#   - 모든 결정(통과/거부) 사유 로그 — 미명명 실패모드의 명명

def goal_selection_guard(ranked: list[dict], ctx) -> dict:
    """value 상위 후보들에 coverage/independence 게이트 적용 → 선택집합 + 거부로그."""
    selected, rejected = [], []
    seen_capability = set()           # family|target-class 기준
    for g in ranked:
        cap = capability_key(g)       # 예: family + 자원클래스
        if cap in seen_capability:
            rejected.append({**g, "reason": "duplicate-capability(coverage gate)"}); continue
        ind = independence_check(g, ctx)   # 선택근거 다양성(컨벤션/소스)
        if ind["single_convention"]:
            g = {**g, "warn": "single-convention dependence"}
        seen_capability.add(cap); selected.append(g)
    return {"selected": selected, "rejected": rejected}
```

---

## 4. PPR — W2.2 ExploitAxis (분해 최적화기)

```python
# acceptance_criteria:
#   - 타깃 유니터리 고정 → 분해만 탐색. 오라클 봉인 못하면 reward=0 (구조적 reward-hacking 차단)
#   - 봉인된 후보 중 동일 u_hash & 자원감소 1건 이상 발견 OR 정직 음성(미발견 명시)
#   - capability-coverage 게이트: trivial 양산(identity padding 등) 차단

def exploit_axis(target_id: str, ctx, budget: int) -> dict:
    """target 의 봉인 유니터리 고정. 후보 분해 생성→오라클 봉인→동일 u_hash 검증→최소자원 선택.
    reward = 0 if not sealed else (1 + resource_score(resource)). reward-hacking: 봉인 게이트가
    하드제약 — u_hash 불일치/미봉인은 0. cmul4(2-Fredkin) 사례 = 합성 후보 정형화."""
    base = load_sealed(target_id)
    best = base
    for cand in generate_decompositions(target_id, ctx, budget):   # 봉인부품 재조합만(no MatrixGate)
        v = oracle_seal(cand)                                       # app_assemble
        if not v.sealed or v.u_hash != base.u_hash:
            continue                                                # reward 0
        if resource_cost(v) < resource_cost(best):
            best = v                                                # 동일 유니터리·더 싼 분해
    return {"target": target_id, "improved": best.id != base.id, "base": base, "best": best}
```

honest: 새 진리 발명 아님 — 동일 u_hash 유지 하 자원 최소화. 봉인이 하드 게이트라
reward-hacking(가짜 보상) 구조적 불가. 미발견 시 "정직 음성"으로 종결(과장 금지).

---

## 5. 불변 제약 (Stage 공통)

- 비파괴: `.pgf/discover/` · `_workspace/crossmodel/discover_round1/` 만 가산. registry/sealed/frozen/
  fingerprint(verify_seal.py·contracts.py) 불변. 신규 봉인은 오라클(app_assemble) 경유만, MatrixGate 금지.
- 공통 verify: `reproduce_all` root `3dae613d` · `second_oracle` · `verify_contested_guard`(frozen 23키).
- [SC]: W2.1/W2.2/W2.3 혼자 완결. [EXT]: W2.4 는 패키지까지 완성 후 relay 대기.

---

## 6. 실행 순서

W2.1(ValueFunction) → W2.3(Guard, value 소비) → W2.2(ExploitAxis, value 우선순위 소비) → W2.4[EXT].
각 Work: 구현 → 자체 verify → 공통 회귀 그린 → 체크박스 `[~]→[x]`.
