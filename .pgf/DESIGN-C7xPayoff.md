# DESIGN — C7xPayoff (Stage 6, W6.1 ArithFamilyExtend-c7x + DiscoverSelfAdvance)

> PG sub-design. c7x 봉인(W2.4)의 직접 결실을 실현: 7-control이 *실제로 필요한* distinct-prime
> modular multiplier(N∈(64,128])를 Tier-0 EXACT 봉인하고, 발견 루프가 봉인된 frontier를 넘어
> 자동 전진하도록 보강한다. 비파괴 성장(기존 봉인·frozen 23키·fingerprint 불변).

## 핵심 가정 검증 (PG: 가정을 노드로 명시 → 검증시점 포착)

- ⚠ **discover 주장 정정**: discover propose는 c7x가 "mod 39=3×13, mod 51=3×17"을 unlock한다고
  명시했으나 **실측으로 반증됨**. nq=(work bits)+1, nq-qubit MCT의 max control = nq-1 = work bits.
  c7x(7 control)는 work bits≥7 ⟺ **N>64**일 때만 필요.
  - 실측(mmd_synthesize maxc): mod39/51/55/57 (N<64, nq=7) → **maxc=6 = c6x로 이미 충분**.
  - c7x 진짜 unlock(N∈(64,128], nq=8 → maxc=7): mod65=5×13(231g)·mod77=7×11(128g)·
    mod85=5×17(148g)·**mod91=7×13(77g)**. (mod95=5×19는 maxc=5 — 우연한 cheap orbit.)
- 결론: forge 타겟 = **N>64 distinct-prime** (mod91·mod77·mod85). mod39/51은 c7x 무관(별건).

## Gantree

```
C7xPayoff // c7x 활용 distinct-prime 확장 + 발견 자동전진 (in-progress) @v:6.0
    A_EngineEvolve // genskills modmul_synth c7x 지원 (designing)
        # _MCT_MODULE[7]="c7x"; cap (maxc>6 raise) → (maxc>7, c8x 부재 메시지)
        # arith_family._MCT_SET += "c7x"
        # method self-seal 재스탬프: genskills catalog → verify INTACT (root 0367ed64→new)
    B_ForgeDistinctPrime // N>64 distinct-prime cmul 봉인 (designing) @dep:A_EngineEvolve
        # 신규 driver scripts/arith_family_c7x.py — arith_family 함수 재사용(import)
        # 타겟: cmul2_mod91(7×13)·cmul2_mod77(7×11)·cmul2_mod85(5×17)
        # synth → app_assemble 봉인(app_golden 경로, nq=8 dense 256²)
        # IndependentArithVerify: 독립 순열 재구성 → sealed u_hash 대조(삼각측량)
        # EngineRegression: 기존 cmul(≤c6x) genskills 재현 u_hash==registry(불변 증명)
        # BehavioralObserve: ×2 orbit period == ord_N(2) (illustrative only §8.4)
    C_DiscoverSelfAdvance // 발견 루프 봉인 frontier 자동전진 + unlock 정정 (designing) @dep:A_EngineEvolve
        # 근본원인: ctx["modules"]=그래프 *사용* 모듈만(봉인 전체 아님) → 미사용 봉인 gate에 frontier 정체
        # fix1: ctx에 sealed_modules(MODREG 스캔) 추가 → gap_to_proposal이 봉인된 gap 스킵
        # fix2: PRIMITIVE_FAMILIES cNx "unlocks" 텍스트를 실측(N>64) 근거로 정정
        # 결과: c7x/cr8 봉인 인지 → 다음 미봉인(c8x/cr9_dag_gate) 제안
    D_Verify // 결정론 재검증 + 동기화 (needs-verify) @dep:A_EngineEvolve,B_ForgeDistinctPrime,C_DiscoverSelfAdvance
        # acceptance: reproduce_all REPRODUCED · second_oracle 50/50(모듈 불변) · contested_guard ALL PASS
        #   · fingerprint 2파일 무수정 · frozen 23키 불변 · 신규 cmul 독립검증 3/3 · regression 불변
        # 문서/메모리/roadmap 체크박스 동기화(새 root)
```

## acceptance_criteria (D 검증)

- 구조적: 신규 모듈 봉인 0 (c7x/cr8 이미 봉인됨; 앱만 가산). 모듈 50 불변, 앱 59→62.
- 기능적: 3개 cmul SEALED tier=0 · 독립 산술순열 u_hash==sealed 3/3 · ×2 orbit period==ord_N(2) 3/3.
- 결정론: reproduce_all 2회 byte-identical · second_oracle 50/50(모듈) · contested_guard ALL PASS(frozen 23).
- 비파괴: fingerprint(verify_seal/contracts) 무수정 · 기존 cmul(≤c6x) regression u_hash 불변 · genskills verify INTACT.
- 정직: plan=봉인 MCT(toffoli..c7x), MatrixGate 0 · generation≠verification(오라클 봉인) · behavioral=illustrative only.

## 정직성 경계

- 엔진 *진화*(무변경 아님): genskills c7x upstream + self-seal 재스탬프 — P1 c6x 진화와 동형.
  기존 cmul(≤5ctrl·c6x) 산출 byte 불변(EngineRegression).
- c7x payoff는 **앱 성장**(registry root 변경)이나 기존 봉인/frozen/fingerprint는 byte-identical = 순수 비파괴.
- discover의 틀린 unlock 주장을 실측으로 정정(정직한 자기수정) — W2.4 채점 시 발견.
