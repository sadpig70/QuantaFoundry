# DESIGN-ConsensusClose — Stage 4 Consensus 정직종결 (ρ 실데이터)

> PGF design mode · 기반 = `_legacy/roadmap_process_plan.md` Stage 4 (Track B2) · 방법 = PG Gantree + PPR.
> 정직성: 분석/검증 전용 비파괴. registry/sealed/frozen/fingerprint 불변. frozen consensus_keys 재생성 금지.
> 소비 자산(사용만): second_oracle(INDEP/embed/my_canonical_hash) · verify_seal(hash_unitary) ·
> consensus(Source/establish_truth/effective_independent_count) · corpus_discount.

---

## 0. 문제 (8-agent 최약가정 잔여)

(B2) convention 단일문화(big-endian/atol/전역위상)가 *전역 단일실패점*. second_oracle 은 risk(d)
[Qualtran 구성버그]를 닫지만, **convention 버그는 공동 가정**이라 미차단일 수 있다(A3). 또한 ρ-discount
는 *설계*됐으나 표준게이트 co-error 가 4라운드까지 0 → **실가동 미입증**. 두 갭을 정직 종결:
W4.1 = second_oracle 독립성 경계 감사(가정 판정), W4.2 = poisoned 합의 *구성* → ρ-discount 붕괴 검증.

---

## 1. Gantree

```
ConsensusClose // ρ-discount 실가동 또는 미가동 최종확정 (designing) @v:0.1
    W4.1_ConventionIndependenceAudit // second_oracle 독립유도 vs 가정 판정 (designing) [SC]
        EndianAudit // big-endian embed vs qubit-reversed → sealed 의존성 = endian 가정 입증 (designing)
        PhaseAtolAudit // 전역위상/atol 공유 가정 확인 (designing)
        HashIndependenceAudit // vs.hash_unitary vs my_canonical_hash 판정 일치(측정 부분독립 측정) (designing)
        AuditVerdict // 차원별 독립/가정/공유 매트릭스 + 갭 문서화 (needs-verify) @dep:EndianAudit,PhaseAtolAudit,HashIndependenceAudit
    W4.2_PoisonedLineagePanel // co-error 구성 → ρ-discount 붕괴 (designing) [EXT]
        PoisonedUnits // little-endian QFT·conjugate·phase-perturbed (틀린 유니터리, 결정론) (designing)
        LineageMergeTeeth // same-unit 2소스 poisoned 합의 → DIVERGENT(독립단위 병합) (designing) @dep:PoisonedUnits
        RhoDiscountTeeth // distinct-unit poisoned + ρ>0 → CORPUS_CORRELATED escalate (designing) @dep:PoisonedUnits
        ControlEstablished // 정답 2독립소스 → ESTABLISHED 대조 (designing)
        ValidationReport // 메커니즘 실가동 판정 + 자연발생 co-error EXT 구분 (needs-verify) @dep:LineageMergeTeeth,RhoDiscountTeeth,ControlEstablished
```

---

## 2. PPR — W4.1 ConventionIndependenceAudit

```python
# acceptance_criteria:
#   - EndianAudit: 비대칭 게이트(cnot 등) big-endian embed 가 sealed 와 일치하고, qubit-reversed
#     embed 는 불일치 → sealed 가 big-endian convention 에 의존하며 second_oracle 도 동일 가정(독립유도 아님)
#   - PhaseAtolAudit: U vs U·e^{iφ}, U vs U+ε(ε<atol) → 동일 hash (전역위상/atol 공유 가정 확인)
#   - 판정: 유니터리 *구성*=독립(numpy 제1원리), convention(endian/phase/atol)·canonical hash=공유/가정
#   - 가정 차원은 갭으로 문서화(검증 필요 명시) — 과장 제거

def endian_audit(gid, sealed_u_hash):
    U = INDEP[gid]()
    be = hash_unitary(embed(U, targets_forward, n))      # big-endian (현 convention)
    le = hash_unitary(embed(U, targets_reversed, n))     # qubit-reversed
    return {"big_endian_match_sealed": be == sealed_u_hash,   # 현재 True
            "reversed_differs": le != be,                      # 비대칭이면 True
            "verdict": "endian-assumed (shared convention, not independently derived)"}

def phase_atol_audit(gid):
    U = INDEP[gid]()
    phase_inv = hash_unitary(U) == hash_unitary(U * exp(1j*0.7))   # 전역위상 무시 가정
    atol_inv  = hash_unitary(U) == hash_unitary(U + 1e-9)          # atol 가정
    return {"global_phase_invariant": phase_inv, "atol_invariant": atol_inv}
```

판정 매트릭스(차원 × {독립유도 / 공유가정}):
| 차원 | 판정 | 근거 |
| 유니터리 구성 | 독립유도 | numpy 제1원리, no qualtran/no spec-golden |
| endian | 공유가정 | embed big-endian 하드코딩, sealed 가 이에 의존 |
| 전역위상/atol | 공유가정 | hash_unitary 와 동일 canonicalization |
| canonical hash | 공유(부분독립 측정) | vs.hash_unitary; my_canonical_hash 로 교차 |

→ convention 단일문화 = 미차단 단일실패점. 갭 명시(과장 제거).

---

## 3. PPR — W4.2 PoisonedLineagePanel [EXT]

```python
# acceptance_criteria:
#   - PoisonedUnits: little-endian QFT 등 *틀린*(sealed≠) 유니터리를 결정론 구성
#   - LineageMergeTeeth: 같은 independence_unit 2소스가 poisoned u_hash 합의 → establish_truth =
#     DIVERGENT(독립단위 병합으로 w=1<N=2) → 계보공유 차단 입증
#   - RhoDiscountTeeth: distinct-unit 2소스 poisoned + ρ>0 → CORPUS_CORRELATED → INSUFFICIENT escalate
#   - ControlEstablished: 정답 2독립소스 ρ=0 → ESTABLISHED (대조; 메커니즘이 정답까지 막지 않음)
#   - 판정: ρ-discount/lineage-merge 가 *구성된* co-error 를 붕괴 = 메커니즘 실가동.
#     자연발생 co-error(약모델 패널 4라운드 0)는 [EXT] relay 로 구분(과장 금지).

def rho_validation():
    poison = poisoned_units()                  # {little_endian_qft3, conj, phase_perturbed}
    s1 = Source("rt1", "model", "weightsA", poison["le_qft3"])
    s2 = Source("rt2", "model", "weightsA", poison["le_qft3"])   # 같은 lineage
    r_merge = establish_truth("qft3", [s1, s2], N=2, rho=0)      # → DIVERGENT (w=1)
    s3 = Source("rt3", "model", "weightsB", poison["le_qft3"])   # distinct unit
    r_rho = establish_truth("qft3", [s1, s3], N=2, rho=0.5)      # → INSUFFICIENT(CORPUS_CORRELATED)
    # 대조: 정답 2독립
    g = qft3_sealed_u_hash
    r_ok = establish_truth("qft3", [Source("a","model","wA",g), Source("b","model","wB",g)], N=2, rho=0)
```

self-contained(메커니즘 검증) 완료 후, 약모델 패널 패키지(`_workspace/crossmodel/p3d_round5_poison/`)는
relay 대기. 산출: `scripts/rho_validation.py` · `docs/TRUST-MODEL-VALIDATION-REPORT.md`.

---

## 4. 불변 제약 / 실행 순서

- 비파괴: `scripts/{convention_audit,rho_validation}.py` 신규 · `.pgf/consensus/`·`docs/`·패널패키지 가산.
  registry/sealed/frozen/fingerprint 불변. **frozen consensus_keys.json 재생성 금지**(메모리상 검증).
- 공통 verify: `reproduce_all` root `3dae613d` · `second_oracle` · `verify_contested_guard`.
- 순서: W4.1(audit) → W4.2(poisoned, self-contained 부분 → relay 대기).
