# DESIGN — KeyFreeConsensus (인간 seed 없는 첫 진리 확립)

> PGF design mode 산출물 · @v:0.1 · 루트 = `D:\QuantaFoundry`
> 출처: Disruptive Engineer 패러다임 전환 제안 + 실험 E5'(B4)의 실증.
> 목표: answer-key seed(인간 단일 정답표) 의존을 제거하고, **정답을 독립 출처의 u_hash 수렴 사건으로
> 창발**시킨다. 이로써 "자율 파운드리는 인간이 이미 아는 정답만 재생산한다"는 천장(기술서 §8)을 깬다.

---

## 0. 문제 (실증된 근거)

- **answer-key seed = SPOF + 자율 천장.** 신규 모듈마다 인간이 정답 u_hash를 박아야 → 인간이 모르는
  첫 진리는 자율 생성 불가.
- **E5'(B4) 실증**: 같은-모델 두 격리 페르소나가 *둘 다 CZ(default)* 로 수렴 → 의미적으로 임의인
  모듈이 봉인됨. 즉 **격리만으로는 (b) 공유 default 합의를 못 막는다.** 같은 모델 adversary도 분산
  ({π/4,π/2})하여 교정 실패. → 진짜 독립성은 *물리적으로 다른 weights* 또는 *모델-독립 형식증명*에서만.

---

## 1. 핵심 아이디어

정답(consensus_key)을 "인간이 박은 값"이 아니라 **서로 독립인 출처들이 같은 u_hash에 수렴하는 사건**
으로 정의한다. 한 번 창발하면 frozen + provenance(출처 목록) 기록. 미수렴(분산)이면 **정답 없음** —
모호성으로 escalation(정직: 모르면 모른다).

**독립성의 단위가 핵심**(B4 교훈): 같은 weights·같은 컨텍스트에서 나온 다수 산출은 **1 vote로 병합**한다.
같은 모델이 우연히 합의해도 독립도는 1이므로 정답이 창발하지 않는다.

---

## 2. Gantree

```
KeyFreeConsensus // 인간 seed 없는 첫 진리 확립 (in-progress) @v:0.1
    DiversitySource // 독립 출처 풀 (in-progress)
        CrossModelVote // 물리적으로 다른 weights 모델 산출 → u_hash (designing)
        FormalProof // symbolic(sympy) golden ↔ U 동치 — 모델 독립 (in-progress)
        StructuralDerive // 진리표/대칭성에서 독립 구성 → u_hash (in-progress)
    IndependenceWeighting // 물리적 독립도 가중 — 같은 weights/컨텍스트는 1로 병합 (in-progress)
        # input: sources: list[Source]
        # process: group by independence_unit(klass, weights_id) → 단위별 1 vote
        # output: independent_votes: dict[u_hash, set[unit_id]]
    Convergence // u_hash 수렴 판정 (in-progress)
        Collect // 출처별 (id, klass, weights_id, u_hash) 수집 (in-progress)
        Agree // N-of-M 독립 합의 (in-progress) @dep:IndependenceWeighting
        Emerge // 합의 → consensus_key 창발 (answer-key 대체) (needs-verify) @dep:Agree
    ConfidenceGrade // PROOF_BACKED / MULTIMODEL / INSUFFICIENT (in-progress) @dep:Emerge
    Divergence // 미수렴 → 모호성 escalation (정답 없음) (in-progress)
    Integration // autoforge anti_swap 의 key 소스를 합의로 교체 (designing)
```

---

## 3. PPR — 핵심 로직

### 3.1 독립성 가중 (B4 차단의 심장)

```python
def independence_unit(s: Source) -> str:
    """물리적 독립 단위. 같은 weights·같은 컨텍스트 출처는 같은 단위 → 1 vote로 병합."""
    if s.klass == "model":   return f"model:{s.weights_id}"   # 같은 모델 = 같은 단위
    if s.klass == "proof":   return f"proof:{s.tool}"         # sympy/z3 등 도구별
    if s.klass == "structural": return f"struct:{s.method}"
    raise ValueError(s.klass)

def independent_votes(sources: list[Source]) -> dict[str, set[str]]:
    """u_hash → 그것을 지지하는 *독립 단위* 집합. 같은 단위의 중복 산출은 합쳐짐."""
    votes = {}
    for s in sources:
        votes.setdefault(s.u_hash, set()).add(independence_unit(s))
    return votes
    # acceptance_criteria:
    #   - 같은 weights 모델이 4번 같은 답을 내도 그 u_hash의 독립단위는 1 (B4: default 합의 무효화)
```

### 3.2 합의 창발 (answer-key 대체)

```python
def establish_truth(intent_id: str, sources: list[Source], N: int = 2) -> ConsensusResult:
    """독립 출처 ≥N개가 같은 u_hash에 수렴하면 consensus_key 창발. 아니면 escalation."""
    votes = independent_votes(sources)                    # u_hash → {independent units}
    winner, units = max(votes.items(), key=lambda kv: len(kv[1]), default=(None, set()))
    if winner is None or len(units) < N:
        return ConsensusResult(status="DIVERGENT", key=None,    # 정답 없음 → 모호성
                               escalation="independent sources < N; refine intent or add cross-model",
                               distribution={h: len(u) for h, u in votes.items()})
    grade = confidence_grade(units)
    if grade == "INSUFFICIENT":
        return ConsensusResult(status="INSUFFICIENT", key=None, escalation="same-unit agreement only")
    return ConsensusResult(status="ESTABLISHED", key=winner, grade=grade,
                           provenance=sorted(units), key_version=1, frozen=True)
    # acceptance_criteria:
    #   - 명확 intent + proof source 포함 → ESTABLISHED, 인간 seed 0 (key-free)
    #   - B4(같은 모델만 합의) → units={1개} < N → DIVERGENT (임의 default 굳지 않음)
```

### 3.3 신뢰 등급

```python
def confidence_grade(units: set[str]) -> str:
    has_proof = any(u.startswith("proof:") for u in units)
    n_models  = len({u for u in units if u.startswith("model:")})
    if has_proof and len(units) >= 2:      return "PROOF_BACKED"   # 최강: 모델독립 증명 + α
    if n_models >= 2:                       return "MULTIMODEL"     # 다른 weights ≥2 수렴
    return "INSUFFICIENT"                                           # 단일 단위 → 정답 불가
```

### 3.4 기존 통합 (anti_swap 교체)

```python
# autoforge.ANSWER_KEY[id] 를 *고정 인간값* 대신 *합의 산출물*로 대체:
#   establish_truth(id, sources) == ESTABLISHED → ANSWER_KEY[id] = result.key (provenance 부착)
#   이후 anti_swap 은 동일하게 작동하되, 키의 출처가 "human seed" → "independent consensus".
# DIVERGENT/INSUFFICIENT → 그 모듈은 봉인 보류(정답 미확립). 봉인 못 통과 = 미존재(경계 규율 일관).
```

---

## 4. B4가 어떻게 막히는가 (설계 검증 포인트)

| 시나리오 | v0.1 (answer-key seed) | KeyFreeConsensus |
|---|---|---|
| 명확 intent(cnot) | 인간이 키 seed | proof+structural 수렴 → **자동 창발(PROOF_BACKED), 인간 0** |
| B4(같은모델 둘 다 CZ) | 키 없으면 임의 CZ 봉인 | 독립단위=1 → **DIVERGENT, 봉인 보류** (임의 default 거부) |
| 모호 intent(cphase_amb) | 정답 정의 불가 | proof 불가 + 단일 weights → **INSUFFICIENT → escalation** |
| 진짜 신규(cross-model 수렴) | 인간 seed 필요 | 다른 weights ≥2 수렴 → **MULTIMODEL 창발** (인간 0) |

---

## 5. 범위·한계 (정직)

- **현 워크스페이스 제약**: cross-model 실제 호출 불가(단일 모델 환경). 프로토타입은 **FormalProof
  (sympy, 모델 독립)** + **StructuralDerive** + 기존 봉인을 독립 출처로 사용해 합의 엔진을 실증한다.
  cross-model source는 인터페이스만 정의(실배포 시 주입).
- **proof source의 신뢰는 proof checker로 이전**(Qbricks/Z3 철학) — 인간에서 도구로 옮길 뿐 제거 아님.
  단 sympy symbolic은 numpy 부동소수점·LLM 가중치 어느 쪽과도 독립이라 *진짜 다른 출처*.
- **모호 intent는 영원히 정답이 없다** — 이건 버그가 아니라 정직성. intent를 formal하게 정제해야 정답
  창발(Disruptive의 "intent→formal spec 승격"과 연결).

## 6. 완료 기준 (acceptance)

1. consensus.py: independence_votes / establish_truth / confidence_grade 구현.
2. 데모 cnot: sympy proof + structural + 기존봉인 수렴 → ESTABLISHED(PROOF_BACKED), 인간 seed 0.
3. 데모 B4: 같은-모델 다수 합의 → DIVERGENT(독립단위 1) — 임의 default 거부.
4. 데모 cphase_amb: 모호 → INSUFFICIENT → escalation.
5. autoforge 연결 설계 명시(키 출처 = 합의).
