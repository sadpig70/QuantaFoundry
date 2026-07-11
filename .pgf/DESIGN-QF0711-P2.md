# DESIGN — QF-0711-Upgrade / P2 TrustPackaging

> **모드**: PGF full-cycle (JIT, P1 폐합 후). **상위**: MasterRoadmap `TrackQF0711Upgrade/P2_TrustPackaging`.
> **범위**: P2 4노드 원자화. 대부분 root 불변(sidecar/doc); U12 만 순수성장(격상 companion).
> **작성**: 2026-07-11.

## 0. 실측 근거 + 제약 (착수 전 확인)

```text
U11: root = registry_root_hash(sha256 id:u_hash). evidence 후보 = registry/{SEMANTIC,APPROX,COUNT-ONTOLOGY,
     VERIFICATION-COVERAGE}.json + .pgf/proofs/{*-VERIFY,*.{column,subspace,cuc}_proof,RING-COLUMN,*-OBSERVE}.
     toolchain lock = requirements.lock + .agents/skills/qpgf-oracle/{DEPENDENCIES.lock,BUNDLE.sha256}.
     claim manifest = verification/claims.json. → evidence_root/release_root 는 신규 해시(가산, seal_root 불변).
U12: rs73 = 60 clifford(cnot)+8 x · total_t=0 = 순수 Clifford. 현 등급 subspace_permutation_verified
     (512/512 = RS(7,3) message space 2^9 전수, 전체 2^21 unitary 아님). Tier-2 tableau 로 전체 Clifford
     unitary 검증 시 unitary_equiv 격상 → INV-R5 잔여 0. ★no-new-pip: stim 불가 → hand-rolled stabilizer
     tableau 또는 기존 Clifford 인프라 재사용. companion(ghz16 선례, 비파괴 sidecar) → root 불변.
U13: 지표 소스 = COUNT-ONTOLOGY + VERIFICATION-COVERAGE + SEMANTIC headline + APPROX + check_claims.
     coverage_matrix/doc_counts 패턴 재사용(집계 sidecar).
★U14: consensus_keys.json 은 **FROZEN**(guard_check byte-identical, INV1/2) — `_meta` 추가 **금지**
     (guard 파손). 메타는 별도 sidecar. cached_canonical_map(75) 설명은 registry_tools 생성 시 _note.
비파괴: oracle fingerprint 2·frozen 23키·기존 sealed byte-identical 불변. root 0a6fbab0 (U12 성사 시만 격상 sidecar, u_hash 불변→root 여전 불변).
```

## 1. Gantree (원자 분해)

```text
P2_TrustPackaging // 릴리스 외부화·잔여 폐합 (designing)
    U13_QualityScorecard // 양적→질적 지표 (독립·저위험, 먼저) #C12
        U13a_ScorecardGen // qf_witness/registry/quality_scorecard.py → QF-QUALITY-SCORECARD.json (atomic)
        U13b_ReadmeQuality // README 첫 수치를 quality 중심 1줄(선택) + --check witness/CI (atomic)
    U14_MetadataHygiene // 메타 위생 (doc/sidecar, frozen 무접촉) #C13
        U14a_ConsensusMetaSidecar // consensus-keys-meta.json(count/last/root) — ★frozen 원본 무편집 (atomic)
        U14b_CachedMapNote // registry_tools 가 cached_canonical_map 에 _note(75 leaf 설명) 생성 (atomic)
        U14c_InvariantsDoc // docs/INVARIANTS.md — INV-REG/INV-LOOP/INV-R 통합 색인 (atomic)
        U14d_HonestyDoc // docs/HONESTY-BOUNDARIES.md — 정직 경계 1페이지(경계·의미·위반·검증) (atomic)
    U11_ReleaseRoot // seal_root/evidence_root/release_root 3층 #C10
        U11a_EvidenceRoot // evidence 산출물 정렬 해시 → evidence_root (atomic)
        U11b_ReleaseRoot // release_root = H(seal_root, evidence_root, toolchain_lock, claim_manifest) (atomic)
        U11c_Attestation // .pgf/adoption/RELEASE-ROOT.json + qf_stdlib attest 가 보장 root 필드 반환 (atomic)
    U12_Rs73Tier2 // rs73 Clifford tableau 격상 → INV-R5 잔여 0 (최고효율, 마지막) #C11
        U12a_TableauVerify // rs73 60-gate CNOT+X 를 hand-rolled stabilizer tableau 로 전체 unitary 검증 (atomic)
        U12b_Companion // companion sidecar(ghz16 선례) → semantic subspace→unitary_equiv 격상 (atomic)
        U12c_ResidueClose // INV-R5 잔여 서술(subspace 1→0) 정합·EVIDENCE-MAP/README (atomic)
```

## 2. PPR (노드별)

### U13 · QualityScorecard (먼저)
```python
# U13a: quality_scorecard.py — {unique_canonical_coverage, guarantee_strength_dist(headline),
#   asset별 독립경로 분포(VERIFICATION-COVERAGE histogram), inferred/unclassified 비율(=0, U2),
#   primary_seal_only 수, QF-STDLIB Canon coverage, stale_claim(=0, U7 check), n_verification_paths}
#   → registry/QF-QUALITY-SCORECARD.json. --check idempotent.
# U13b: README quality 지표 1줄(선택). ★race 없음(읽기전용 집계) → witness batch --check 가능.
# acceptance: 모든 지표가 기존 산출물 파생·재추적 가능. root 불변.
```

### U14 · MetadataHygiene (frozen 무접촉)
```python
# U14a: .pgf/keyfree/consensus-keys-meta.json(신규) = {count:23, last_added_key, last_added_root, note}.
#   ★consensus_keys.json 원본은 절대 무편집(guard byte-identical). 메타는 파생 sidecar.
# U14b: registry_tools build 가 cached_canonical_map 에 _note("75 = app-side module re-seal, NOT 새 unique app;
#   나머지 20 module 은 인프라/타 module 경유") 삽입 → DEPENDENCY 재생성 정합(root 불변, MANIFEST note 필드).
# U14c: docs/INVARIANTS.md — 3 네임스페이스(INV-REG oracle·INV-LOOP qfa·INV-R rigor) 색인(F8 충돌해소).
# U14d: docs/HONESTY-BOUNDARIES.md — 경계 표(seal≠run≠verify·approx≠exact·structural≠dense·REPRODUCED≠correct·
#   observation≠seal·float-atol≠ring-exact·cached≠unique) + 위반 시나리오 + 검증 명령. README 링크.
# acceptance: frozen/root 불변. INV/경계 단일 참조.
```

### U11 · ReleaseRoot
```python
# U11a: evidence_root = sha256(정렬된 "path:sha256(content)" over evidence 산출물). 결정론.
# U11b: release_root = sha256(seal_root|evidence_root|toolchain_lock_hash|claims_hash).
# U11c: .pgf/adoption/RELEASE-ROOT.json = {seal_root, evidence_root, toolchain_lock_hash, claim_manifest_hash,
#   release_root, as_of}. qf_stdlib attest 응답에 "attested_up_to": which root 필드.
# acceptance: 3 root 결정론 재생성 · seal_root==기존 registry_root(불변) · release_root=clean checkout 재현.
# gate: --check idempotent · 기존 seal/root 불변.
```

### U12 · Rs73Tier2 (최고효율·마지막)
```python
# U12a: rs73_encoder spec(60 cnot + 8 x, 21q) 파싱 → hand-rolled stabilizer tableau(X/Z 전파, no dense,
#   no new pip) 로 전체 Clifford unitary 를 golden(독립 구성)과 비교. 512 message space 가 아닌 전체 2^21.
#   ★검증: 순수 Clifford 라 tableau 가 전체 unitary 포착(위상 포함). 실패 시 U12 보류(subspace 유지).
# U12b: companion sidecar .pgf/proofs/rs73_encoder.tableau_proof.json → semantic_guarantee override
#   (subspace_permutation_verified → unitary_equiv, Tier-2). ghz16 companion 선례.
# U12c: INV-R5 잔여 subspace 1→0. EVIDENCE-MAP row·README grade 표·CURRENT-SPEC 정합.
# acceptance: rs73 전체 unitary tableau 검증 통과 → 격상. subspace headline 잔여 0. u_hash 불변(root 불변).
# gate: reproduce REPRODUCED · root 0a6fbab0 · second_oracle 83/83 · tableau_proof idempotent.
# ★리스크: hand-rolled tableau 구현 부담. 과하면 U12 는 P2 에서 분리(별도 트랙)하고 U11/U13/U14 로 P2 폐합.
```

## 3. WORKPLAN / POLICY

```text
순서: U13(독립·저위험)→U14(doc/sidecar)→U11(release root)→U12(tableau, 최고효율·최고효율=INV-R5 0, 마지막).
POLICY:
  non_destructive: oracle fingerprint 2·frozen consensus 23키(★consensus_keys 원본 무편집)·기존 sealed byte-identical.
  root_invariant:  U11/U13/U14 = sidecar/doc(root 불변). U12 = 격상 companion(u_hash 불변 → root 여전 불변).
  gate_per_node:   해당 --check · reproduce REPRODUCED · root 0a6fbab0 · second_oracle 83/83.
  U12 escape:      hand-rolled tableau 가 과대하면 U12 를 별도 트랙으로 분리, U11/U13/U14 로 P2 폐합.
```

## 4. 정직 경계 (이 설계)

- ★**U14 consensus_keys FROZEN**: 원본 무편집(guard 파손 방지). 메타는 파생 sidecar.
- **U12 는 등급 flip 아님**: 실제 stabilizer tableau 로 전체 unitary 검증해야 격상(512 message space 검증만으론 불충분). no-new-pip 제약 = hand-rolled. 성립 확인 실패 시 subspace 유지(정직).
- **U11 seal_root 불변**: evidence_root/release_root 는 가산 상위 해시. 기존 registry_root 는 seal_root 로 그대로.
- 잔여(P3): qf inspect/explain/plan — P2 폐합 후 JIT.
```
