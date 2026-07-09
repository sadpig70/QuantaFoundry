# DESIGN — IntegratedUpgrade (통합 업그레이드: 검증심화 척추 + 신뢰외부화 백로그)

> **Version** 1.0 · **Status** L1 done (L2~L4 backlog blocked) · **작성** 2026-07-09 (Fable 5) ·
> **폐합** 2026-07-09: CQV 27종 ALL VERIFIED · ε-cert 9종 ALL CERTIFIED · math-crux 5/5 CONFIRMED
> (독립 adversarial 리뷰) · REPRODUCED · root d177ce9a 불변
> **입력**: `_workspace/ex-upgrade-design/upgrade-design01~03.md` 3개 외부 제안 통합
> **Base (실측)**: root `d177ce9a438a1b2f…` · **95 modules / 475 unique apps** (550 files) ·
> 검증경로 10 · Tier-1 = subspace 30 + structural 1 + sampled 1
>
> **통합 판정**: design01(검증 심화·수직) = **척추 L1**(정체성 100% 정합·즉시 실행·최대 지렛대).
> design02(외부 신뢰성·제품화) = L2/L3 백로그. design03(장기 비전) = L4 백로그(non-goal 필터).
> 세 문서는 경쟁이 아니라 **4-레이어 스택** — L1이 만든 새 보증 등급을 L2가 외부화한다.

---

## 0. 실측 검증 결과 (Phase 0 — design01 전제 확인)

| design01 주장 | 실측 판정 |
|---|---|
| 앱 541 | ❌ **475 unique** (550 total files — 저자가 file 수와 혼동 추정). 이하 475 기준 재정합 |
| Tier-1 31 = shor28 + ghz16 + rm15_tt + rs73 | ✅ headline: subspace 30 + structural 1(ghz16) + sampled 1 (shor235/237 가산분 반영) |
| shor plan = H×t + cmul×t + iqft{t} | ✅ shor95 = H×8 · cmul×8 · iqft8 (17 steps) 확인 |
| iqft7/iqft8 Tier-0 `unitary_equiv` | ✅ dense EXACT 봉인 (golden = IQFT 정의행렬, plan = cr*_dag 사다리) |
| subspace proof exhaustive + path A 재사용 가능 | ✅ `.pgf/proofs/shor95.subspace_proof.json` 32768/32768, `perm_subspace_verify.path_a_vec` 재계산 가능 |
| Trotter/QSVT/rz 전부 exact-only (목표 오차 무인증) | ✅ 전부 Tier-0 `unitary_equiv`, spec 헤더에 "진짜 e^{-iHdt} 와의 오차는 별도 관찰(seal 아님)" 명시 |
| semantic_guarantee 레이어 비파괴 격상 선례 | ✅ `*.subspace_proof.json` 소비 → class 격상 패턴 기존재 (V08 P0) |
| tfim3 dt | ⚠ **dt=π/8 무리수** — E1 을 "유리수 × π 닫힌형(sympy symbolic exact)" 로 확장 정의 |

**핵심 재해석 (design01 §1, 실측 승인)**: modexp 코어의 exhaustive 순열 판정은 가역 고전 회로에 대해
**그 자체로 full unitary 확정**(순열 유니터리는 기저 작용으로 완전 결정). shor{N}의 3개 인자
(H-wall Tier-0 자명 · modexp 순열 확정 · iqft{t} Tier-0)가 전부 unitary급 → 남은 갭은 **조립 논증 하나**.

---

## 1. 불변 조건 (INVARIANTS — 전 Phase 공통)

```python
# INV-IU1: registry root d177ce9a… 불변 — 산출물은 .pgf/proofs sidecar + registry/*-GUARANTEES.json 레이어만
# INV-IU2: oracle fingerprint 2파일·frozen consensus 23키 byte-identical 불변 (수정 절대 금지)
# INV-IU3: 기존 sealed 파일 무수정 (읽기 전용 소비)
# INV-IU4: 정직 경계 — column_exact 는 float-atol 계급(Tier-0 dense C4 와 동일)이지 ring-exact 아님.
#          ε 는 상한(upper bound)이지 실제 오차 아님. seal ≠ run ≠ verify 상속.
# INV-IU5: DoD = second_oracle 83/83 불변 · reproduce_all --changed-only REPRODUCED · root 불변 확인
```

---

## 2. Gantree

```
IntegratedUpgrade // 3문서 통합: L1 검증심화 척추 + L2~L4 백로그 (done — L1 폐합, L2~L4 blocked 보존) @v:1.0
    L1_VerifyDepth // 척추 — design01 소비 (검증 수직 심화) (done)
        IU_A_Tier1Uplift // CQV: Tier-1 shor → unitary_equiv_column_exact 상향 (done)
            CqvEngine // scripts/column_verify.py — 행렬-프리 컬럼 전수 검증 엔진 (done)
                PlanWalk // shor plan 파싱(H/cmul/iqft steps) — perm_subspace 파서 재사용 (done)
                IqftCircuitCompose // iqft{t} plan 재합성 → Q_circ (2^t×2^t, 회로 경로) (done)
                    # process: iqft plan 의 모듈 golden(h/swap/cr*_dag)을 t-큐빗 embed 곱으로 합성
                    # criteria: 재합성 Q_circ 는 봉인 golden 무참조(회로가 실제 하는 일) — 이후 A′에 사용
                ColumnStreamA // path A′: plan 배선대로 열 폐형식 계산 (done) @dep:PlanWalk,IqftCircuitCompose
                    # input: c0×w0 전체 기저(전수), f_circ = path_a_vec(회로 MCT 전개 순열)
                    # process: |c0,w0⟩ → H-wall(모듈 golden 부호) → f_circ 재매핑 → Q_circ 열수축
                    # criteria: dense 2^n 미실체화(메모리 < 2GB), w0 배치 스트리밍
                ColumnFormulaB // path B′: Shor 수학 스펙트럼 공식 직접 산술 (done) @dep:PlanWalk
                    # process: 2^{-t/2}·(−1)^{c·c0}·Q_math[c',c]·[w == w0·a^c mod N] — 배선 무참조
                    # criteria: Q_math = (1/√2^t)·ω^{−c'c} 정의행렬, f_math = 순수 정수산술
                ColumnCompare // 전 컬럼 A′==B′ + negative controls (done) @dep:ColumnStreamA,ColumnFormulaB
                    # criteria: max|A′−B′| ≤ 1e-12 전수(n≤18) · teeth 3종(iqft 게이트 제거·배선 교란·a+1 산술) 전부 REJECT
            CqvPilot // shor69 1종 파일럿 실행 (done) @dep:CqvEngine
            CqvFleet // Tier-1 shor n_sys≤18 전종 전수 (done) @dep:CqvPilot
                # criteria: 26종(n15/16) + shor381/635(n17/18) 전수 컬럼 일치, sidecar .column_proof.json
            CqvLargeSampled // shor1285/3683 (n19/20) 표본 컬럼 + CUC 조립 논증 (blocked — 후속)
            GuaranteeUplift // semantic_guarantee.py column_proof 소비 → 등급 상향 (done) @dep:CqvFleet
                # process: subspace 소비 패턴 복제 — *.column_proof.json → class 'unitary_equiv_column_exact'
                # criteria: 비파괴(레이어만) · INV-R5 축소 개정(잔여 = n≥19 표본 2건 + ghz16 + rm15_tt + rs73)
        IU_B_EpsilonTier // ε-bounded 근사 인증 티어 (직교축, exact-only 한계 돌파) (done)
            ApproxSchema // registry/APPROX-GUARANTEES.json (approx-guarantee-v1) + E1–E4 계약 (done)
                # E1: target spec 정준화+hash (유리수/π-닫힌형 sympy symbolic 만 허용)
                # E2: ε_upper 는 sympy exact symbolic (float 단독 금지)
                # E3: 산출 감사추적 (방법·교환자 항·산술 종류·approx_code_hash)
                # E4: negative control — 교란 spec 에서 bound 위반 실검출
            PauliAlgebra // sympy 계수 exact Pauli 문자열 대수 (곱·교환자·삼각 norm 상한) (done)
            BoundAnalytic // 방법(b) 1차 Trotter 교환자 상한 — ε ≤ (t²/2r)·‖[H_A,H_B]‖_Δ (done) @dep:PauliAlgebra
            BoundSuzuki2 // 2차 Suzuki 상한 — Childs et al t³ 중첩교환자 (done) @dep:PauliAlgebra
            EpsPilotTrotter // tfim3/4·heis2/3 계열 8종 인증 실행 (done) @dep:BoundAnalytic,BoundSuzuki2
                # criteria: heis2 single-bond 는 [H_A,H_B]=0 → ε=0 (exact sanity) · 각 인증서 sidecar 기록
            EpsWitnessDense // 독립 2경로: dense 실측 d_op ≤ ε 확인 (관측 witness, 8×8/16×16) (done) @dep:EpsPilotTrotter
            EpsTeeth // E4: t→2t 교란 목표에서 실측 > ε 검출 (done) @dep:EpsPilotTrotter
            EpsPropagate // 준가법 전파 실증 — 합성앱 ε ≤ Σ 자식 ε (2steps 1건) (done) @dep:EpsPilotTrotter
            EpsArbInterval // 방법(a) python-flint arb 구간산술 — QSVT/QSP 9종 (blocked — 후속, 신규 의존성)
            EpsGridsynth // 방법(c) rz_synth ε exact ℤ[1/√2,i] — 신규 module 사람게이트 (blocked — 후속)
        ReproduceRegister // reproduce_all 에 column/approx --quick 스텝 등록 (done) @dep:CqvFleet,EpsPilotTrotter
        DocSync // HANDOFF·README·SEMANTIC-GUARANTEES 문구 동기화 (done) @dep:GuaranteeUplift
    L2_TrustExternalize // design02 A/B/C — 신뢰 외부화 백로그 (blocked — L1 완료 후)
        QfInspectCli // qf inspect/explain-guarantee/diff-root 한 화면 신뢰체인 (blocked)
        RegistryExplorer // 정적 웹 대시보드 (Overview·Seal card·HE map·Obs vs Seal) (blocked)
        GuaranteeMatrix // SEMANTIC/APPROX-GUARANTEES → docs/guarantee-matrix.md 자동생성 (blocked)
        QiskitRoundTrip // Qiskit adapter — 실행 아닌 정규화·왕복검증 (blocked — QF-STDLIB deferred 결정 승계)
    L3_PathHorizontal // design02 D/E — 경로·수평 확장 백로그 (blocked — TrackHE 사이클과 조율)
        PermGroupPath11 // 제11 경로 후보: permutation-group/Schreier-Sims (arithmetic island 한정) (blocked)
            # ⚠ 자가강등 위험 선검증 필수: path_a_vec 순열추출 재인코딩이면 MA/treewidth 류 강등.
            #   독립성 crux = cycle decomposition/orbit-stabilizer 가 ANF(GF(2) Boolean)와 전제 상이한지
        LatticeSurgeryT2 // 물리 patch Tier-2 실봉인 (blocked — REQUEST-v13 잔여 관문에 기등재, 중복 배치 금지)
        MtcVerifier // full MTC consistency (blocked — SU(2)₃ modular data 관측 완료, 봉인섬 분리 필요)
        # A₅ Fourier √5 실봉인(design02 1순위)은 **이미 종결** — 2026-07-09 honest 경계 확정
        #   (KAK opaque float → honestly byte-sealable 아님, 표현론 자산으로 완결). 재착수 금지.
    L4_LongTerm // design03 필터링 흡수 — 장기 백로그 (blocked)
        QmlFamily // 양자 ML (커널/VQC) — VQE/QAOA 계보 연장선만 (blocked)
        ChemistryScale // 더 큰 분자 블록인코딩 (be_h2 계보) (blocked)
        DiscreteLog // Shor 이산로그 확장 (frontier factory 계보) (blocked)
        # 명시 제외(non-goal 충돌): 펄스레벨/하드웨어 실행/양자우위 RCS/실시간 제어
        #   — [[project-identity-future-qpc]] "하드웨어 제외" 방향과 배치. 편입하지 않음.
```

---

## 3. 핵심 PPR

### 3.1 CQV — column_verify

```python
def column_verify(shor_id: str, atol: float = 1e-12) -> ColumnProof:
    """Tier-1 shor 앱 전체 유니터리를 행렬-프리 컬럼 전수로 검증 (조립 논증을 닫는다)"""
    p = load_shor(shor_id)                      # perm_subspace 파서 재사용 (n,t,work,a,N,plan)
    f_circ = path_a_vec(...)                    # 회로 게이트 순열 (MCT 전개 — 봉인 무참조)
    Q_circ = compose_iqft_from_plan(t)          # iqft plan 재합성 (회로 경로, 2^t×2^t)
    Q_math = iqft_definition_matrix(t)          # (1/√2^t)·ω^{−jk} (수학 경로)
    for w0 in range(2**work):                   # w0 스트리밍 (메모리 << 2GB)
        # path A′: H(모듈 golden 부호) → f_circ 그룹 → Q_circ 열수축   [회로가 실제 하는 일]
        # path B′: (−1)^{c·c0} 공식 → f_math=w0·a^c mod N 그룹 → Q_math [수학이 요구하는 것]
        A = batch_columns(Q_circ, group_by(f_circ, w0), signs_H)      # (c',w,c0) 텐서
        B = batch_columns(Q_math, group_by_arith(a, N, w0), signs_formula)
        assert max_abs_diff(A, B) <= atol       # 전 컬럼, 전역위상 자유도 없이 직접 비교
    assert reject(perturbed_iqft())             # teeth1: iqft 게이트 1개 제거 → 불일치
    assert reject(perturbed_wiring())           # teeth2: modexp 배선 교란 → 불일치
    assert reject(perturbed_arith(a + 1))       # teeth3: 틀린 산술 → 불일치
    return write_sidecar(f".pgf/proofs/{shor_id}.column_proof.json")
    # acceptance_criteria:
    #   - 전수 컬럼 일치 (n_sys ≤ 18) — grade 'unitary_equiv_column_exact'
    #   - dense 2^n 미실체화 · registry root 불변 (sidecar 만)
    #   - float-atol 계급 정직 표기 (ring-exact 참칭 금지 — pathsum ℤ[ω_2^t] 는 후속 이종 증인)
```

**비용 실측 추정**: w0당 2×(2^t)³ 복소 MAC → shor(n=15) ≈ 2^31 MAC — numpy zgemm 수 초.
26종(n≤16) + 2종(n=17/18) 전수 = 분 단위~수십 분. 전 기저 2^n 컬럼 전수 달성.

### 3.2 ε-tier — certify_trotter

```python
def certify_trotter(app_id: str) -> ApproxCert:
    """봉인 Trotter 앱의 목표 e^{-iHt} 대비 ε 상한을 sympy symbolic exact 로 인증"""
    spec = parse_target(app_id)                       # H = Σ c_k P_k (sympy Rational), t = q·π
    comm = pauli_commutator(spec.H_A, spec.H_B)       # Pauli 대수 exact ([ZZ,X] = ±2i·YZ …)
    eps = spec.t**2 / (2*spec.r) * triangle_norm(comm)  # 1차; Suzuki2 는 t³ 중첩교환자 공식
    d_obs = dense_phase_inv_distance(app_id, spec)    # 독립 witness: 실측 d_op ≤ eps (float 관측)
    assert d_obs <= float(eps)
    assert dense_distance_to(perturbed(spec, t_mul=2)) > float(eps)   # E4 teeth
    return write_cert("registry/APPROX-GUARANTEES.json", app_id, eps)
    # acceptance_criteria:
    #   - eps 는 sympy exact (π-닫힌형 · 부동소수 산출 0회) · 감사추적 완전 (E1–E3)
    #   - heis2 (single-bond) → 교환자 0 → ε = 0 sanity 통과
    #   - E4 negative control 통과 · registry root 불변 (직교 sidecar 만)
```

**합성 전파(§IU_B EpsPropagate)**: 유니터리 op-norm 준가법성 `‖U₂U₁−V₂V₁‖ ≤ Σ‖Uᵢ−Vᵢ‖` →
합성앱 ε = Σ(자식 ε), exact 자식 = 0. 파일럿에서 1건 실증(tfim3_trotter_2steps), 전 registry
자동 전파는 후속(EpsArbInterval 이후 소비자 증가 시).

---

## 4. 실행 순서 (이번 세션 범위)

| # | 노드 | 산출물 | 비고 |
|---|---|---|---|
| 1 | CqvEngine + CqvPilot | `scripts/column_verify.py` + shor69 proof | 인프라 전부 기존재 — 최저비용 최대효과 |
| 2 | CqvFleet | shor n≤18 전종 `.column_proof.json` | 26+2종 전수 |
| 3 | GuaranteeUplift | SEMANTIC-GUARANTEES 등급 상향 + INV-R5 축소 | 비파괴 레이어 |
| 4 | ApproxSchema~EpsTeeth | `scripts/approx_certify.py` + APPROX-GUARANTEES.json | Trotter 계열 8종, 신규 의존성 0 |
| 5 | ReproduceRegister + DocSync | reproduce_all 스텝 + HANDOFF/README | DoD 체인 |

**이번 세션 제외(blocked)**: CqvLargeSampled(CUC)·EpsArbInterval(arb)·EpsGridsynth(사람게이트)·
pathsum ℤ[ω_2^t] 확장·L2~L4 전체. 전부 Gantree 에 노드로 존재 — 마스터 규율 충족.

## 5. 정직 경계 (설계 고정)

1. `unitary_equiv_column_exact` = **float-atol(1e-12) 계급** — Tier-0 dense C4 와 동일한 증거 계급.
   ring-exact 가 아님을 sidecar `arith` 필드와 legend 에 명시. exact 이종 증인은 후속 pathsum 확장.
2. ε 는 **상한**이지 실제 오차가 아님 (`epsilon_upper` 로만 표기, tightness 무주장).
3. dense witness(E-경로 실측)는 **관측**(float)이며 인증의 주 증거는 symbolic 상한.
4. CQV 이후에도 Tier(숫자)는 불변 — 격상은 semantic_guarantee **레이어**에서만 (subspace 선례).
5. INV-R5 는 폐기가 아니라 **축소 개정**: 잔여 미검증 = shor1285/3683 전체 unitary(표본만) +
   ghz16(sampled) + rm15_tt·rs73(구조/부분상환) — 문구에 정확히 기재.
