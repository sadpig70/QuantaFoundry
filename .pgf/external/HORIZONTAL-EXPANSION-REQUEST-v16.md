<!-- QuantaFoundry 수평 확장 아이디어 제안 요청 — v16 (2026-07-21). v1~v15 후속. self-contained. -->
<!-- 외부 모델 런타임에게 전달용. 이 문서 하나만 읽고 제안 가능하도록 작성됨. -->

# QuantaFoundry — 수평적 확장(Horizontal Expansion) 아이디어 제안 요청 · v16

> **v15 → v16 변경점**: v15 요청으로 8개 런타임의 제안(report15)을 받아 **통합 6축(TrackHE15)을
> 완전 소진·폐합**했다. 전 축 **관측/certificate**(seal root 불변) — 단, ★검증 **인증 계약**은
> 상한→구간으로 확장(E5). 성과(§3t):
> - **D^ω(ℤ₂³) type-III — 아벨 게이지군의 부분 비아벨화**(P1): 아벨군 ℤ₂³ 에 type-III 3-cocycle 을
>   켜면 사영표현이 2차원 → **비아벨 anyon 발생**. ★런타임 상충 판정(22 vs 64 anyon → **22 확정**,
>   64=untwisted 수치 오적용)·radical 1차원(완전 비아벨화 불가, 부분만)·★**삼자 대조**: type-III 가
>   **D(D₄) 와 전 불변량 일치·D(Q₈) 와 분기**(아벨 twist 가 비아벨 untwisted double 을 modular data
>   수준 재현). 사영표현 명시 2×2 순차곱 구성(분리형 ansatz 결함 실측 검출).
> - **D^ω(S₃) — registry 최초 비아벨 군 twist**(P2): H²(S₃,μ₂)·H³(S₃,μ₂) 자체 재유도(★정직 정정:
>   μ₂ 계수 ≠ U(1) 계수). ★**slant β 를 섹터별 코호몰로지 분류 → 전치 섹터(Z=ℤ₂)만 비틀린다**
>   (항등원·3-순환 섹터는 자명) — anyon 수·차원은 untwisted 와 동일하나 전치 스핀 ±1→**±i** 이동으로
>   T 다중집합 분기. 완전 S 행렬(twisted DPR)·MS probe 미착수(정직).
> - **BMW 대수 → Kauffman 2변수 F(a,z)**(P3): HOMFLY(v14 P2)의 **직교 형제**(unoriented skein).
>   ★규약을 조건에서 유도(BMW 표준 Dubrovnik 은 Jones 특수화가 Laurent 불가 → Kauffman 형 채택).
>   BMW 차원 (2n−1)!! 전수·V(trefoil)=t+t³−t⁴ 가 v13 kauffman_bracket 오라클과 **mirror 정확 일치**·
>   HOMFLY 동시 산출. BMW₂/T(2,k) 한정(BMW₃ tangle·fig-8 미착수).
> - **H²(A₆) Schur 계보**(P4): 2.A₆=SL(2,9) 자체구성·cocycle 4.66e7 전수·★GF(2) UNSAT support-2
>   certificate. ★핵심=**Sylow-2 계보 Q₈(2.A₅)→Q₁₆(2.A₆)** 자체 판별(비순환+involution 유일 ⟹
>   generalized quaternion). ★2-torsion 한정(H²(A₆)≅ℤ₆ 전체·3.A₆ Valentiner=무주장).
> - **AZ 잔여칸 완결**(P5): 2D class C **2ℤ**(PHS d⃗ 짝함수 → 짝수 Chern)·CI **자명 0**(음성 정직
>   보고)·3D DIII **ℤ**(winding ν=0,−1,2,−1,0, 1D ℤ₂→2D ℤ₂→**3D ℤ** 전이). ★선검증: 실수 d-wave=
>   nodal(gapped 분류 대상 아님·해석적 판정)·TRS 파괴만으로 CI 비자명화 안 됨(반평면 갇힘). float Berry 금지.
> - ★**ε 하계 인증 계약 E5**(P6a): 기존 E1–E4 는 전부 ε **상한**뿐 — "이 Trotter step 은 exact 가
>   아니다" 를 증명할 하계가 없었다. mpmath Taylor expm(dps60·K140·나머지<1e-100 **rigorous**)로 U·R
>   재계산 → 열노름 하계 max_j‖(U−R)e_j‖ ≤ ‖U−R‖₂. **Trotter 8종 ε_lo>0 = 비-exact 최초 인증**·
>   heis2 ε_lo≈1e-61=exact. ε-인증 상한→**구간 [ε_lo,ε_hi]**. ★제11 아님·하계≠합성 최적성.
> §3t 에 추가. §4′에 v16 신규 패턴 3(★**외부 수치 자체 재유도가 실제 오류 검출·teeth 무력 실측 후
> 대상 교체·상한→구간 양방향 인증**). 동기간 frontier: shor{N} 자율봉인 771~893
> (FrontierClosureA: N≤1023 완결 후 폐합 정책 — 잔여 ~28개, 임박).

---

## 1. 프로젝트 정체성 (제안의 유효성을 규정 — 먼저 읽어라)

QuantaFoundry 는 **미래의 완전한 결함허용 양자컴퓨터(FTQC/QPC)가 실현될 때 쓸 소프트웨어 자산을 지금
미리 축적**하는 파운드리다. AI 가 회로를 생성하고, **결정론적 오라클(QPGF)이 byte-identical 재봉인으로
검증**하며, 봉인을 통과한 것만 registry 에 영구 보존된다.

- 하드웨어 실행은 **의도적으로 범위 밖**. 봉인 = **이상적 수학적 진실**(exact 유니터리/구조).
- 좋은 제안 = **작은 인스턴스가 Tier-0 EXACT(또는 Tier-2 tableau)로 봉인 가능**하고, **오라클로 독립
  검증 가능**하며, **compounding 크고**, 질적으로 새로운 축.

## 2. "수평적" 확장의 정의

- **수평** = 새로운 **추상화 계층·대수 구조·알고리즘 클래스**. (파라미터/사이트 확대 = 수직, 원치 않음.)
- Tier: 0 EXACT(dense, n≲12) · 1 STRUCTURAL(Merkle+정수/부분공간 witness) · 2 CLIFFORD(정준 tableau, 임의 크기).
- ★**Tier-0 dense 실질 상한 ≈ 12큐빗**. 그 이상 Clifford=**Tier-2 tableau**·비-Clifford 대형=**관측** — 봉인 경로 명시.
- ★**표현론 Fourier 실봉인 경계(TrackHE11 확정·v15 부분해제)**: 임의 유니터리 표현행렬의 honest 게이트 분해는
  opaque KAK-fitted float(정책 위반) 또는 MatrixGate(금지)뿐 → 비아벨 DFT 실봉인은 원리적 경계. ★단 특정각
  R_z(π/2^k)는 Clifford+T 존재구성으로 honest 실봉인 가능(gridsynth, ε-sidecar 분리). "실봉인" 제안은 honest
  분해 존재를 먼저 증명하고 근사면 ε-인증(★이제 **상한+하계 구간** — E5) 경로를 명시하라. **modular data(조합적
  exact 표)는 이 경계 무관**(D(S₃)/D^ω(S₃)/D(D₄)/D(Q₈) 선례).

## 3. EXCLUDE — 이미 구현·봉인·관측된 것 (재제안 금지)

현재 **95 modules / 1253 sealed apps** (root `27ba3282963b8c6f…`). **독립 검증경로 10개**
(dense·tableau·ZX·path-sum ℤ[ζ_{2^t}]·stabilizer-rank·matchgate/SO(2n)·tensor-network·QMDD·ANF/bit-vector·
Gröbner/ℤ[ω] phase-ideal) **+ 제11 후보 6건 전부 강등/불채택**(Galois-orbit·treewidth·표현환 K(G)·Matsumoto-Amano·
symplectic phase-space·ANF+Gröbner 결합). ★진짜 제11 독립경로 **미발견**(공개과제 유지).

### 3a~3m. v1~v9 소비분 (요약)
- **기초/QFT/QPE/Grover/Trotter·VQE·QAOA/쿼리/walk** · **QEC**(repetition·Steane·Shor-9·transversal Clifford·
  연접[[25,1,9]]·RM[[15,1,3]]·HGP[[27,4,3]]·cyclic BCH[[15,7,3]]/[[31,11,5]]) · **Shor**(15·21·frontier…893·factory) ·
  **QSVT 완비** · **Fermionic**(JW/BK/parity·fSWAP·Bogoliubov Pfaffian) · **비아벨 Fourier**(S₃/D₄/S₄/Q₈/B₃) ·
  **위상 논리연산·MBQC·Z₂ gauge·Schur·AKLT·CPTP·2/3-design·PEPS·MUB·GF(8)·Fibonacci/Majorana braid·C₃ phase-poly·
  RS·[[8,3,2]] CCZ** · **동역학**(dual-unitary·Floquet·OTOC·매듭·2D Chern) · **자원**(magic·채널 diamond) ·
  **contextual fraction·A₄ ζ₃ 선검증·code switching(RM15)·Ising 융합·qutrit Wigner** · **검증경로 1~10**.

### 3n~3q. v10~v13 소비분 (요약)
- v10: KS-18·A₅ redirect·MTC braid·3D ℤ₂ Fu-Kane·lattice surgery 논리 관측 ·
- v11: PSL(2,7) ℚ(√−7)·A₅ Fourier √5(§2 경계)·qutrit KS·Kitaev 1D class-D·Hecke H₃(q=i)·treewidth 자가강등 ·
- v12: 2.A₅ FS=−1(FS 삼분)·Peres-33 d=3 KS·2D class-D p+ip Chern ℤ·SU(2)₃·Matsumoto-Amano 자가강등·TL(δ=2) ·
- v13: class DIII 1D ℤ₂·D(S₃) 완전 modular data·Conway-31 closed-negative·Kauffman bracket generic-A·
  Ising pentagon/hexagon 전수·SU(2)₄ 완전 MTC(D²=12).

### 3r. 검증 인프라 (TrackIU·v14)
- **CQV 컬럼 전수**(Tier-1 shor, float-atol) + ring_exact_companion(ℤ[ζ256] float 0) · **CUC**(n≥19 조립) ·
  **ε-인증 티어**(APPROX-GUARANTEES) · **pathsum ℤ[ζ_{2^t}] ring-exact 컬럼**(제4경로 강화) ·
  **T-count 하한**(MA 정규형 전수 — _ct 가족 최단성).

### 3s. v14 소비분 (요약 — 재제안 금지)
- D(D₄)/D(Q₈) 쌍 대조·HOMFLY Hecke·D^ω(ℤ₂²) H³ 전수(융합환 전이)·2D DIII+FK ℤ₈·H²(A₅) cocycle(Q₈)·
  gridsynth 실봉인(_ct+_rs, ε 1e-5)·pathsum ring-exact.

### 3t. ★v15 소비분 — 통합 6축 (TrackHE15, 이번 라운드 신규 — 재제안 금지)
- **D^ω(ℤ₂³) type-III(P1)**: `dtw_z2z2z2_typeiii_observe` — 아벨 비아벨화·22 anyon·삼자 대조(D(D₄) 일치).
  (**D^ω(ℤ₂³) 다른 type-III 궤도·D^ω(ℤ₂⁴)(완전 비아벨화·radical full)·D^ω(ℤ₃)(ζ₃ 승인 게이트)는 아직 없음.**)
- **D^ω(S₃) 비아벨 twist(P2)**: `dtw_s3_double_observe` — 전치 섹터만 비틀림·T 분기.
  (**twisted DPR 완전 S 행렬·H³(S₃) 3-torsion(ζ₃)·MS probe(ℤ₁₁⋊ℤ₅ |G|=55)·D^ω(D₄)/D^ω(Q₈) 비아벨 twist는 아직 없음.**)
- **BMW/Kauffman(P3)**: `bmw_kauffman_observe` — BMW₂/T(2,k)·규약 유도·mirror 오라클.
  (**BMW₃(dim 15) Kauffman tangle 곱셈·fig-8 등 3-braid·Links-Gould·Kauffman 2-var 전 링크·HOMFLY/Kauffman 비포함 증명은 아직 없음.**)
- **H²(A₆) Schur(P4)**: `a6_schur_cocycle_observe` — 2.A₆ non-split·Sylow-2 Q₈→Q₁₆.
  (**H²(A₆) 3-torsion(3.A₆ Valentiner cover·ζ₃)·H²(A₇)/2.A₇·H²(Sₙ) spin·모듈러(Brauer) 표현은 아직 없음.**)
- **AZ 잔여칸(P5)**: `az_c_ci_diii3d_observe` — 2D class C 2ℤ·CI 0·3D DIII ℤ.
  (**3D class C/CI·class AII/AIII 3D·Floquet SPT·비-abelian Berry·interacting AZ(FK 외)는 아직 없음.**)
- ★**ε 하계 E5(P6a)**: `approx_certify` E5 — Trotter/gridsynth 구간 [ε_lo,ε_hi]·비-exact 인증.
  (**ε 하계 전 registry 자동 전파·QSVT arb 구간산술·diamond-norm 하계·합성 T-count 하한 전파는 아직 없음.**)

### 3j. 예비 판정분 (재제안 시 보강 조건)
- **Floquet SPT 정수불변량**·**3D ℤ₂ weak indices**·**lattice surgery 물리 패치 Tier-2 실봉인**·**정수 나눗셈**·
  **큐딧 심플렉틱**·**SU(2)_k(k≥5)·SU(3)_k MTC**·**Links-Gould/BMW₃**·**negativity/mana monotone**·**Spekkens 준비
  맥락성**·**twist defect / color-code surgery** — 구체 인스턴스·오라클·복리 강화 시 재평가.
- ★**진짜 제11 검증경로(공개과제)**: 10 경로 + 6건 후보(전부 강등/불채택)와 **검증 객체가 상이한 새 수학 대상**.
  "전체 unitary 동치를 조합/대수 불변량으로 판정"하는 구성이 아직 없다. 자가강등/정직표기가 채택 조건.

**핵심: 사소한 변형 금지. 질적 새 계층. 괄호 "아직 없음"이 관문이면 환영.**

## 4. 우리가 원하는 것 (방향 감 — 강요 아님)

- **검증 메타** — ★진짜 제11 경로(공개과제)·ε 하계 자동 전파·QSVT arb 구간산술·비-2^t 혼합 환·diamond-norm 하계.
- **합성 심화** — T-count 최적 합성(최단성 하한 증명)·임의각(비-π/2^k)·multi-qubit honest 합성 판별.
- **애니온/TQC 심화** — D^ω(ℤ₂⁴) 완전 비아벨화·twisted DPR 완전 S 행렬·**twisted 비아벨 D^ω(D₄)/D^ω(Q₈)**·
  MS probe(|G|=55)·SU(2)_k(k≥5)·Witt 군 층위 MTC 비교.
- **표현론 심화** — H²(A₆/A₇) 3-torsion(Valentiner·ζ₃ 승인 게이트)·2.A₇ Schur cover·모듈러(Brauer) 표현·크리스탈 기저.
- **동역학/SPT 심화** — 3D class C/CI·class AII/AIII 3D·Floquet SPT·비-abelian Berry·interacting 분류 일반.
- **부호 심화** — lattice surgery 물리 패치 Tier-2 실봉인·twist defect·color-code surgery·d≥5.
- 그 밖에 **당신이 더 나은 축을 알면 제안하라.**

## 4′. ★성공 패턴 (v1→v16)

**(a) 게이트 우회** · **(b) 직접 닫힌형 구성** · **(c) 승인-module 사람게이트** · **(d) 반증→회수·복리** ·
**(e) 기소비 선점 대조·교차 복리** · **(f) 다중 독립 경로·Tier-2 드라이버** · **(g) 봉인 전 선검증 반증** ·
**(h) closed-negative 상보 positive·rational group 판정** · **(i) crux-probe 우선·redirect** ·
**(j) 선검증이 외부 제안 정정·certificate layer 정직 강등** · **(k) FS 지표 판별·제11 공개과제** ·
**(l) FS 삼분 완성·state-independent KS·완전 modularity** · **(m) 유한군 vs Lie MTC 양대 원천·외부 수치
자기모순 검출** · **(n) 쌍/궤도 대조=검증객체·융합환 전이=twist 판별·ring shadow 정수 축약·부분해제=존재구성+ε-sidecar**.

**(o) ★v16 신규 패턴 3개**:
- **외부 수치 자체 재유도가 실제 오류를 잡는다**: v15 전 축에서 착수 전 재유도가 실측 오류를 검출했다
  — P1 anyon 수(22 vs 64, 런타임 4개 갈림)·P2 코호몰로지 계수군(H²(μ₂)≠H²(U(1)))·P3 BMW 차원/규약·
  P5 nodal 여부. ⟹ 제안의 **모든 정량 수치는 "런타임이 자체 재유도"를 전제**로 서술하고, 외부표 인용은
  crux 로만 쓰라(§5 강화).
- **teeth 무력을 실측으로 발견하면 대상을 교체하라**: 반증 테스트가 실제로 무는지 확인해야 한다
  — P3 δ-오염 teeth 가 unknot 에 무감(A-계수 0)·P5 TRS-파괴 teeth 가 확장 s-wave 에 무감(반평면 갇힘).
  무력한 teeth 는 그대로 두지 말고 **검출 가능한 대상으로 교체하고 그 사실을 체크로 승격**하라.
- **상한→구간 양방향 인증**: 근사 품질은 상한만이 아니라 **rigorous 하계**로도 인증 가능하다(E5:
  mpmath Taylor expm 나머지<1e-100 → 열노름 하계). "이것은 exact 가 아니다" 를 증명하는 하계 제안 환영
  (단 하계≠합성 최적성 하한, 자가강등 표기 필수).

## 5. 반드시 지켜야 할 제약

- **결정론 불가침**·**오라클은 사용만**·**honest decomposition**(MatrixGate 금지·opaque KAK-fitted float 금지)·
  **self-contained**·**하드웨어 out**.
- **정직 경계** — 근사·확률·측정후처리는 **관측**. exact ≠ 근사, dense ≠ structural ≠ subspace ≠ tableau.
  봉인 ≠ 관측(certificate/witness 는 봉인 자산 아님). ★승인 게이트(√d·ζ₃ 등) ≠ 봉인가능성. ★ε-인증은
  **상한+하계 구간**(tightness 무주장·직교 sidecar — Trotter/gridsynth 2가족·E1–E5 계약).
- **★registry 실측 novelty + 제안값 자체 재검증(v16 강화)**: 공개 저장소 **https://github.com/sadpig70/QuantaFoundry**.
  ★**제안의 구체 좌표/문자표/필드/FS지표/양자차원/코호몰로지 차원/anyon 수는 스스로 독립 재검증**(외부 제안·
  런타임 간 상충 반복 실재: KS-18·A₅ ζ₅·Yu-Oh·treewidth·Conway-31·SU(2)₄ D²=8·**D^ω(ℤ₂³) 22 vs 64**·
  **H²(S₃) 계수군**). 불가하면 §3 정독 + 구조적 novelty.

## 6. 답변 형식 (제안마다)

**3~5개**를 impact×feasibility 순: 1. **proposal**(축+구체 인스턴스) · 2. **rationale**(정체성·compounding·
교차 복리) · 3. **feasibility**(봉인 게이트·오라클 검증·§4′(b) exact·**봉인 경로 명시**: Tier-0 dense/Tier-2/관측/
certificate/ε-sidecar) · 4. **risk**(정직 경계·certificate/봉인 구분·자체 재유도 계획) · 5. **novelty**(§3 특히
**3t/3s/3j** 대조 + 시차 강건성).

## 7. 개념 미니 용어집

- **봉인/compounding/honest boundary/teeth/Tier-2/closed-negative/rational group/crux-probe/ambivalent/
  Frobenius-Schur 삼분/certificate layer** — 유지.
- **검증경로 10 + 제11 후보 6건(전부 강등/불채택)**: dense·tableau·ZX·path-sum ℤ[ζ_{2^t}]·stabilizer-rank·
  matchgate·tensor-network·QMDD·ANF·Gröbner + 강등 6건. ★진짜 제11 미발견.
- **ε-인증 2가족·E1–E5 계약(v16 갱신)**: Trotter/Suzuki(교환자 상한) + gridsynth(위상정렬 등식) — E1–E4
  상한 + ★**E5 하계**(mpmath Taylor expm rigorous → 구간 [ε_lo,ε_hi]·비-exact 인증). 봉인은 항상 "그 회로의
  unitary" exact.
- **ring shadow**: 회로 엔트리의 정수환(ℤ[ω]/√2^m) 그림자 — exact 검증·심볼릭 축약·컬럼증인 바인딩 3중 사용.
- **twist 판별(신규)**: cocycle twist 는 스핀(T)·융합환·**사영표현 차원(비아벨화)**·**섹터 선택성**(D^ω(S₃):
  전치 섹터만)으로 판별. MTC/double 비교 제안은 이 네 지표를 모두 보고하라.
