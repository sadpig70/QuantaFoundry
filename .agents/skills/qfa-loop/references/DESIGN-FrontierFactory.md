# DESIGN — FrontierFactory @v:1.0

> **목적**: 자율 루프가 *발견→봉인→검증→커밋*을 사람 개입 없이 폐루프로 돌리도록, Shor
> arithmetic frontier(cmul payoff family + structural shor)를 **임의 distinct-prime N**에 대해
> 봉인하는 **파라메트릭 봉인 함수**를 만든다.
>
> **안전 철학 (핵심)**: 이것은 "자유 codegen"이 **아니다**. `c11x_payoff_family.py`/
> `shor1285_frontier.py` 의 로직은 N만 상수인 검증된 템플릿이므로, 그 로직을 N-파라미터 함수로
> *추출*한다. 새 코드를 생성하지 않으므로 봉인 안전성 우려가 없다. 추가로 **회귀 게이트**(factory가
> 기존 봉인을 byte-identical 재현)가 템플릿 동등성을 결정론적으로 증명한다.
>
> **정직 경계 (상속)**: cmul = Tier-0 EXACT permutation app · shor{N} = Tier-1 STRUCTURAL Merkle
> (dense 동등 아님) · period/factor readout = illustrative. 신규 모듈 0(기존 c8x~c12x primitive 재사용).

---

## 0. 불변 & 정직 경계 (1급 제약)

```python
# INV-F1 회귀: factory_seal(N) 은 기존 봉인된 N(1285,3683 등)을 byte-identical u_hash 로 재현해야
#         한다(템플릿 정확성 증명). 불일치 → factory 신뢰 불가 → 봉인 거부.
# INV-F2 신규 모듈 0: factory 는 기존 primitive(c8x~c12x)만 소비. 필요 primitive 부재(c13x 등)면
#         "primitive-missing" 으로 skip(메모리/codegen 무관 — 정직한 비가용).
# INV-F3 결정론: 모든 봉인은 _perm_hash/_structural_hash(기존 oracle 경로)로 산출. fingerprint
#         2파일·frozen 불변. factory 는 verify_seal/contracts/consensus_keys 를 *수정하지 않는다*.
# INV-F4 honest 분해: cmul = MCT permutation(MatrixGate 0) · shor = structural child Merkle.
#         dense whole-unitary 동등 주장 금지.
# INV-F5 재현 통합: factory 봉인 N 목록은 데이터(.pgf/arith/FACTORY-FRONTIER.json)로 누적되고,
#         reproduce_all 의 단일 factory-step 이 전체를 재봉인(byte-identical)한다. 새 N 추가가
#         reproduce_all 코드 수정을 요구하지 않는다.
# INV-F6 무한확장 가드: 라운드당 N 1개. 자율 루프 budget/dry 정지조건이 폭주를 막는다. 목적은
#         "임의 N 커버리지 실증"이지 무의미 대량생산이 아니다.
```

---

## 1. Gantree — Top Level

```
FrontierFactory // 파라메트릭 Shor frontier 봉인 (designing) @v:1.0
    ParamSeal // (N) → cmul payoff family + structural shor 봉인 (designing)
        ResolvePrimitive // N → work·nq·max_control → 필요 c{maxc}x 존재확인 (designing)
        SealPayoffFamily // cmul{unique_powers}_mod{N} Tier-0 exact (designing) @dep:ResolvePrimitive
        SealStructuralShor // shor{N} Tier-1 structural Merkle (designing) @dep:SealPayoffFamily
    RegressionGate // 기존 봉인 N byte-identical 재현 검증 (designing) @dep:ParamSeal
    FactoryRegistry // FACTORY-FRONTIER.json 누적 + reproduce_all factory-step (designing) @dep:RegressionGate
    LoopWiring // autonomy_loop select_next ← frontier_selector 미봉인 N (designing) @dep:FactoryRegistry
```

---

## 2. PPR — 핵심 함수

```python
# 기존 템플릿(c11x_payoff_family.py·shor1285_frontier.py)의 N-상수를 인자로 승격.
# genskills.gen_modmul/_modmul_perm/mmd_synthesize, app_assemble._seal_dict/_structural_hash/
# _aggregate_cost, verify_seal.hash_unitary 는 *그대로 재사용*(검증된 oracle 경로).

def resolve_primitive(N: int, a: int = 2, t: int = 8) -> dict:
    """N → work·nq·unique_powers·max_control. 필요 c{maxc}x 봉인 존재확인."""
    work = ceil(log2(N)); nq = work + 1
    powa = [pow(a, 1 << (t-1-q), N) for q in range(t)]
    unique = sorted(set(powa) - {1})
    # 각 power 의 modmul synthesis max control 산출
    maxc = 0
    for mul in unique:
        gates = gs.mmd_synthesize(gs._modmul_perm(mul, N, nq), nq)
        maxc = max(maxc, max((len(c) for c, _ in gates), default=0))
    prim = gs._MCT_MODULE.get(maxc)                       # 예: 11→'c11x'
    prim_ok = prim is not None and exists(MODREG/f"{prim}.sealed.json")
    # acceptance_criteria: prim_ok=False → "primitive-missing" (INV-F2, 정직 skip)
    return {"N": N, "a": a, "t": t, "work": work, "nq": nq, "powa": powa,
            "unique_powers": unique, "max_control": maxc, "primitive": prim,
            "primitive_ok": prim_ok}


def seal_payoff_family(meta: dict, only_new: bool = True) -> dict:
    """cmul{unique_powers}_mod{N} 봉인(c11x_payoff_family 일반화). 이미 봉인된 power 는 skip.
    각 cmul = MCT permutation → _perm_hash → app_assemble seal(Tier-0). independent arith 재검증."""
    for mul in meta["unique_powers"]:
        if only_new and exists(APPREG/f"cmul{mul}_mod{N}.sealed.json"): continue
        gates = gs.mmd_synthesize(gs._modmul_perm(mul, N, nq), nq)
        assert max control == meta["max_control"] or <= ; deps ⊆ MCT_SET   # INV-F4
        write spec; seal via _seal_exact_permutation_app                    # 기존 함수
        assert independent_cmul_hash(mul) == sealed u_hash                  # INV-F1 부분
    # acceptance_criteria: 전 unique_power 봉인·tier=0·MatrixGate 0·independent arith 일치


def seal_structural_shor(meta: dict) -> dict:
    """shor{N} 봉인(shor1285_frontier 일반화). 모든 cmul child + h_gate + iqft8 존재확인 →
    structural plan → _structural_hash → app_assemble seal(Tier-1). deterministic reassembly."""
    assert children_sealed(meta)                                           # cmul*·iqft8·h_gate
    spec = structural_plan(meta)   # H^t · controlled-U^(2^j)(powa) · iqft8
    u_hash = aa._structural_hash(children, n_sys=t+work)
    seal via aa._seal_dict(tier=1); assert deterministic_reassembly        # INV-F4
    # acceptance_criteria: tier=1·n_sys=t+work·deterministic·readout 정보성


def factory_seal(N: int, a: int = 2, t: int = 8) -> dict:
    """폐루프 1-N 봉인. primitive 확인 → payoff → structural → registry 등록."""
    meta = resolve_primitive(N, a, t)
    if not meta["primitive_ok"]:
        return {"N": N, "sealed": False, "reason": "primitive-missing",
                "needs": meta["primitive"]}                                 # INV-F2 정직 skip
    seal_payoff_family(meta)
    shor = seal_structural_shor(meta)
    register_factory_N(N, meta)                                            # INV-F5 데이터 누적
    return {"N": N, "sealed": shor["sealed"], "meta": meta, "shor": shor}


def verify_against_sealed(N: int) -> dict:
    """INV-F1 회귀: 기존 봉인 N 을 factory 로 재계산 → u_hash byte-identical 비교(재봉인 없이).
    factory 의 payoff/structural u_hash 가 disk 봉인과 일치해야 신뢰."""
    meta = resolve_primitive(N)
    ok = True
    for mul in meta["unique_powers"]:
        recomputed = _perm_hash(simulate(mmd_synthesize(modmul_perm(mul,N,nq))))
        ok &= recomputed == disk_uhash(f"cmul{mul}_mod{N}")
    recomputed_shor = _structural_hash(rebuild_children(meta), t+work)
    ok &= recomputed_shor == disk_uhash(f"shor{N}")
    return {"N": N, "byte_identical": ok}
    # acceptance_criteria: 봉인된 모든 N 에 대해 byte_identical=True (아니면 factory 봉인 전면 거부)
```

---

## 3. reproduce_all 통합 (INV-F5)

```python
# scripts/frontier_factory.py main():  --reproduce 모드
#   FACTORY-FRONTIER.json 의 모든 N 을 seal_payoff_family+seal_structural_shor 재실행 →
#   기존 봉인과 byte-identical(=재현). all_ok=True 출력.
# reproduce_all.FRONTIER_STEPS += ("frontier_factory", "scripts/frontier_factory.py --reproduce")
#   → 새 N 추가가 reproduce_all 코드 수정 불요(데이터-주도).
```

## 4. 자율 루프 연동 (LoopWiring)

```python
# autonomy_loop.build_queue("frontier-factory"):
#   미봉인 N = frontier_selector 후보 ∩ (primitive 존재) ∩ (아직 shor{N} 미봉인)
#   → Candidate(kind="frontier", driver=factory, dense_safe=True)
# implement(frontier-factory): factory_seal(N) 호출(스크립트 driver 아닌 함수)
# verify_gate: incremental(per-round) → 종결 full reproduce(factory-step 포함)
# select_next: 1 라운드 1 N (INV-F6)
```

---

## 5. Review — 3관점 교차검토

### 일관성 (내부 모순 없음)
- factory_seal 은 기존 oracle 함수(_seal_exact_permutation_app·_structural_hash·_seal_dict)만
  호출 → 봉인 의미가 기존 frontier 스크립트와 **정의상 동일**. 새 봉인 경로 0.
- INV-F1 회귀가 "동일"을 byte 수준에서 강제 → 일관성이 테스트로 보장.

### 완전성 (누락 없음)
- 발견(frontier_selector)→primitive확인→payoff→structural→재현통합→루프연동 전 단계 커버.
- 실패 경로: primitive-missing(c13x), independent-arith mismatch, regression mismatch — 모두
  명시적 거부.

### 정확성 (명세=구현) — 회귀 테스트로 검증(§6)
- 핵심 리스크: 템플릿 추출 시 미묘한 N-의존 상수(예: t=8 고정, powa 계산, plan step 순서)를
  놓치면 u_hash 불일치 → **INV-F1 회귀가 즉시 포착**(1285·3683 재현 실패로 드러남).

### 리스크 & 완화
| 리스크 | 완화 |
|---|---|
| R1 템플릿 추출 오류 → 잘못된 봉인 | INV-F1 회귀(기존 4-N byte-identical) 필수 통과 |
| R2 codegen 안전성 | 코드생성 없음 — 파라메트릭 함수. 자유 코드 0 |
| R3 무의미 대량생산 | 라운드당 1 N + budget/dry 정지 + 커버리지 목적 명시 |
| R4 primitive 부재(c13x) | primitive-missing 정직 skip(메모리 무관) |
| R5 reproduce_all 비대 | factory-step 1개가 데이터-주도 전체 재현(코드 불변) |
| R6 큰 N dense 메모리 | cmul _perm_hash 는 2^nq dense — nq≤13(work≤12)만 자동대상. work≥13은 primitive 부재로 자동 제외 |

---

## 6. 테스트 계획

```text
RG1 회귀: verify_against_sealed(1285) byte_identical=True (c11x payoff+structural)
RG2 회귀: verify_against_sealed(3683) byte_identical=True (c12x payoff+structural)
RG3 회귀: verify_against_sealed(635/381/221/119/91) 전부 byte_identical=True
F1  primitive-missing: factory_seal(N, work=13) → reason=primitive-missing(c13x 부재)
F2  신규 N 봉인: factory_seal(미봉인 N) → payoff+structural sealed·tier 정확·independent arith 일치
F3  결정론: factory_seal(N) 2회 → u_hash 동일 byte-identical
F4  reproduce: frontier_factory --reproduce → 등록 N 전체 all_ok=True
F5  fingerprint/frozen 불변(INV-F3) · second_oracle N/N 불변(신규 모듈 0)
```

> RG1~RG3 가 factory 신뢰의 1급 게이트. **통과 전 어떤 신규 N 도 봉인하지 않는다.**

---

## 7. 파일 레이아웃

```text
scripts/frontier_factory.py              # 파라메트릭 봉인 + --reproduce + --verify-regression
.pgf/arith/FACTORY-FRONTIER.json         # factory 봉인 N 목록(데이터, INV-F5)
.pgf/arith/FACTORY-REGRESSION.json       # 회귀 결과(RG1~RG3)
_workspace/loop/DESIGN-FrontierFactory.md# 본 설계
```
※ autonomy_loop.py(로컬) build_queue/implement 에 frontier-factory 모드 추가.
```
