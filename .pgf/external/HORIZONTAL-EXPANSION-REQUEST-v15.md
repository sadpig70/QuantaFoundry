<!-- QuantaFoundry 수평 확장 아이디어 제안 요청 — v15 (2026-07-18 작성·07-19 정합 갱신). v1~v14 후속. self-contained. -->
<!-- 외부 모델 런타임에게 전달용. 이 문서 하나만 읽고 제안 가능하도록 작성됨. -->

# QuantaFoundry — 수평적 확장(Horizontal Expansion) 아이디어 제안 요청 · v15

> **v14 → v15 변경점**: v14 요청으로 8개 런타임의 제안(report14)을 받아 **통합 6축(TrackHE14)을
> 선택 항목까지 완전 소진·폐합**했다. 관측 5축(root 불변) + ★**실봉인 1축**(P6a, §2 경계 첫 부분해제).
> 성과(§3s):
> - **D(D₄)·D(Q₈) 쌍 대조**(P1, 8/8 수렴): 각 22 anyon·D²=64·동일 양자차원 — ★**군 문자표 동치 ≠
>   double MTC 동치**(T 다중집합 ±i 개수 분기). 단독 관측이 아닌 **쌍 대조**가 검증 객체.
> - **HOMFLY-PT via Hecke+Ocneanu trace**(P2): 2변수 P(a,z) exact Laurent(trefoil/fig8/Hopf) —
>   ★정규화를 Markov 두 안정화 조건에서 **유도**(인용 아님). Jones 특수화가 kauffman state-sum 과
>   mirror(t↔1/t) 오라클 동치·Alexander·skein 삼중 교차검증. 검증객체=Hecke 정준환원(state-sum 상이).
> - **twisted double D^ω(ℤ₂²) H³ 8클래스 전수**(P3): 비자명 7/7 untwisted(=toric² exact 정합) 비동형 —
>   T 다중집합 4궤도 + ★**n₁₂=1(type-II) 계열은 융합환 자체가 전이 ℤ₂⁴→ℤ₄×ℤ₄**(=D(ℤ₄) 데이터).
>   cocycle certificate 2계층(GF(2) UNSAT 좌영벡터·⟨i⟩-스코프 2-adic 도달공간)·H³ 차원 자체 재유도.
> - **2D class DIII ℤ₂ + Fidkowski-Kitaev ℤ→ℤ₈**(P4): 2D helical TSC 3경로 일치(mass-sign 닫힌형 ==
>   TRS-라인 Pfaffian 차원환원 == cylinder edge Majorana Kramers)·★**edge Dirac 위치 ky\*가 비자명 1D
>   line 을 추적**(모멘텀 분해 bulk-boundary)·★s-wave teeth(닫힌형의 odd-parity 전제 노출). FK ℤ₈:
>   ★전 과정 ℚ(i) 정확산술 — T² mod-8 Bott 시그니처(−1,−1,+1,+1)·quadratic 전면 T-odd·n=4 불가
>   **전수**·n=8 gappable **구성**(W=A⃗⁽¹⁾·A⃗⁽²⁾ 자기쌍대 pseudospin Heisenberg, unique GS·gap=¾ exact)
>   — **상호작용 SPT 최초 진입**(전체 ℤ₈ 분류 무주장).
> - **H²(A₅) Schur cocycle causal layer**(P5): SL(2,5) 전수 자체구성 — cocycle 216,000 전수·★GF(2)
>   UNSAT **support-2 최소 certificate**·완전성→μ_{2^k} 스코프 자동상승·사영 descent 3600쌍(2차원
>   구조의 A₅ 참표현 불가 = 2.A₅ 필연 = v12 FS=−1 의 원인층)·★Sylow-2=Q₈(quaternionic 발현).
> - ★**gridsynth Clifford+T 실봉인**(P6a, **§2 부분해제**): R_z(π/2^k) k=3..7 근사회로 5앱 Tier-0
>   EXACT — 기봉인 h/t 만(신규 module 0)·엔트리 ℤ[ω₈]/√2^m ring shadow 정수 정합. ★**ε-인증 2번째
>   가족**: ε=√(2−|tr(U†R)|)=min_φ‖e^{iφ}U−R‖₂(2×2 등식) sympy exact(ε 0.012~0.056·tightness 무주장
>   — Ross-Selinger 최적 아님, 존재 구성). 봉인="회로의 unitary"/목표 대비 거리=sidecar 분리.
> - **pathsum ℤ[ζ_{2^t}] ring-exact 컬럼**(P6b): 제4경로 상향 — 환 확장(t≤8, cr_k=ζ_{2^k} 포괄→QFT
>   가족 진입)·대조 자체 정수 등식(float-atol 제거, 17,408 엔트리 float 0)·rz_ct 봉인·ε-인증·컬럼증인
>   3자 바인딩. ★정직: 기존 경로 강화(제11 아님).
> §3s 에 추가. §4′에 v15 신규 패턴 4(★**쌍/궤도 대조가 검증객체·융합환 전이=twist 판별지표·
> ring shadow 정수 축약·부분해제=존재구성+ε-sidecar 분리**). 동기간 frontier: shor{N} 자율봉인
> 671~771 (FrontierClosureA: N≤1023 완결 후 폐합 정책 진행 중).
>
> **★07-19 후속(GridsynthDeepen — §3s gridsynth 항목 갱신)**: Ross-Selinger-형 합성기 자체구현
> (ℤ[ω] 격자 후보 σ-이중구속·ℤ[√2] 노름방정식 Tonelli-Shanks·norm-Euclidean gcd·정확합성)으로
> **rz_pi{8..128}_rs 5앱 추가 실봉인 — ε 1.3e-5~7.3e-5**(존재구성 _ct 대비 170~3700×·m=54·
> T-count ~220·★T-count 최적화 무주장). ε-인증 sidecar 19종.

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
- ★**Tier-0 dense 실질 상한 ≈ 12큐빗**. 그 이상 Clifford=**Tier-2 tableau**·비-Clifford 대형=**관측** — 봉인 경로 명시(§4′i).
- ★**표현론 Fourier 실봉인 경계(TrackHE11 확정·v15 부분해제)**: 군 문자/FS 판별은 관측 가능하나, **임의 SO(3)/유니터리
  표현행렬의 honest 게이트 분해는 opaque KAK-fitted float**(정책 위반) 또는 MatrixGate(금지)뿐 → **비아벨 DFT 실봉인은
  원리적 경계**. ★단 v15 부분해제 선례: **특정각 R_z(π/2^k)는 Clifford+T 존재구성으로 honest 실봉인 가능**(gridsynth,
  근사거리=ε-sidecar 분리). ⟹ "실봉인" 제안은 **honest 게이트 분해 존재를 먼저 증명**하고, 근사라면 ε-인증 경로를 명시하라.
  **modular data(조합적 exact 표)는 이 경계 무관**(D(S₃)/D(D₄)/D(Q₈)/SU(2)₄ 선례).

## 3. EXCLUDE — 이미 구현·봉인·관측된 것 (재제안 금지)

현재 **95 modules / 1109 sealed apps** (root `75c23c31d5890a58…`). **독립 검증경로 10개**
(dense·tableau·ZX·path-sum ℤ[ζ_{2^t}]·stabilizer-rank·matchgate/SO(2n)·tensor-network·QMDD·ANF/bit-vector·
Gröbner/ℤ[ω] phase-ideal) **+ 제11 후보 6건 전부 강등/불채택**(Galois-orbit·treewidth·표현환 K(G)·Matsumoto-Amano·
symplectic phase-space·ANF+Gröbner 결합). ★진짜 제11 독립경로 **미발견**(공개과제 유지).

### 3a~3m. v1~v9 소비분 (요약)
- **기초/QFT/QPE/Grover/Trotter·VQE·QAOA/쿼리/walk** · **QEC**(repetition·Steane·Shor-9·transversal Clifford·
  연접[[25,1,9]]·RM[[15,1,3]]·HGP[[27,4,3]]·cyclic BCH[[15,7,3]]/[[31,11,5]]) · **Shor**(15·21·frontier…707·factory) ·
  **QSVT 완비** · **Fermionic**(JW/BK/parity·fSWAP·Bogoliubov Pfaffian) · **비아벨 Fourier**(S₃/D₄/S₄/Q₈/B₃) ·
  **위상 논리연산·MBQC·Z₂ gauge·Schur·AKLT·CPTP·2/3-design·PEPS·MUB·GF(8)·Fibonacci/Majorana braid·C₃ phase-poly·
  RS·[[8,3,2]] CCZ** · **동역학**(dual-unitary·Floquet·OTOC·매듭·2D Chern) · **자원**(magic·채널 diamond) ·
  **contextual fraction·A₄ ζ₃ 선검증·code switching(RM15)·Ising 융합·qutrit Wigner** · **검증경로 1~10**.

### 3n~3p. v10~v12 소비분 (요약)
- **KS-18(d=4)·A₅ redirect·MTC braid·3D ℤ₂ Fu-Kane·lattice surgery 논리 관측** (v10) ·
- **PSL(2,7) ℚ(√−7)·A₅ Fourier √5 실현가능성(실봉인 §2 경계)·qutrit KS(Yu-Oh 정정·KCBS)·Kitaev 1D class-D·
  Hecke H₃(q=i)·treewidth 자가강등** (v11) ·
- **2.A₅ FS=−1(FS 삼분 ℝ/ℂ/ℍ)·Peres-33 진짜 d=3 KS(UNSAT)·2D class-D p+ip Chern ℤ·완전 MTC SU(2)₃·
  Matsumoto-Amano 자가강등·TL(δ=2)** (v12).

### 3q. v13 소비분 (TrackHE13)
- **class DIII 1D ℤ₂**(3경로·Majorana Kramers 쌍) · **D(S₃) 완전 modular data**(유한군 MTC 축·C=I) ·
  **Conway-31 colorable closed-negative**(나이브 궤도≠KS) · **Kauffman bracket generic-A** ·
  **Ising pentagon/hexagon 전수**(F/R 해집합 결정) · **SU(2)₄ 완전 MTC**(D²=12 외부오류 정정·parafermion).

### 3r. 동세션 검증 인프라 (TrackIU)
- **CQV 컬럼 전수**(Tier-1 shor n≤18, float-atol) + ring_exact_companion(iQFT ℤ[ζ256] float 0) ·
  **CUC**(n≥19 조립인증) · **ε-인증 티어**(APPROX-GUARANTEES, E1–E4 계약).

### 3s. ★v14 소비분 — 통합 6축+선택 (TrackHE14, 이번 라운드 신규 — 재제안 금지)
- **D(D₄)·D(Q₈) 쌍 대조(P1)**: `dihedral_quaternion_double_observe` — 문자표 동치≠double 동치(T 분기).
  (**D(A₄)/D(S₄)/D(Q₈)⊗류 비교·Mignard-Schauenburg 류 T-불변량 한계 탐구·twisted D^ω(비아벨 G)는 아직 없음.**)
- **HOMFLY Hecke Ocneanu(P2)**: `homfly_hecke_observe` — 2변수 exact·Markov 유도·Jones/Alexander 특수화.
  (**BMW/Kauffman 2-var·H_n(n≥5) 셀·Links-Gould·quantum A₂ invariant 는 아직 없음.**)
- **D^ω(ℤ₂²) H³ 전수(P3)**: `dtw_z2z2_double_observe` — 8클래스·융합환 전이·certificate 2계층·H³ 자체유도.
  (**D^ω(ℤ₂³) type-III(비아벨화 twist·16 anyon 중 2차원 발생)·D^ω(ℤ₃)(ζ₃ 필요·승인 게이트)·twisted 비아벨
  D^ω(S₃) 는 아직 없음.**)
- **2D DIII + FK ℤ₈(P4)**: `class_diii_2d_observe`·`fidkowski_z8_observe` — 3경로·edge Dirac 추적·T² Bott·
  n=8 gappable 구성. (**3D DIII·class C/CI(AZ 잔여)·FK n=6 보호 구조(비-Kramers)·interacting 분류 ℤ₈ 전체·
  Floquet SPT·비-abelian Berry 는 아직 없음.**)
- **H²(A₅) cocycle(P5)**: `a5_schur_cocycle_observe` — non-split certificate·FS=−1 원인층·Sylow-2=Q₈.
  (**H²(Sₙ) spin 표현 계보·2.A₆/2.A₇ Schur cover·H³(G,U(1)) 비아벨 twist 분류·군 확장 일반론은 아직 없음.**)
- ★**gridsynth 실봉인(P6a + 07-19 GridsynthDeepen)**: `gridsynth_family`+`approx_certify` — 존재구성
  rz_*_ct 5앱 + ★**RS-형 rz_*_rs 5앱(ε 1e-5급, ℤ[√2] Diophantine·노름방정식·정확합성 자체구현)** 전부
  Tier-0·ε-인증 19종. (**T-count 최적 합성(최단성 증명/하한)·임의각(비-π/2^k)·Fallback(probabilistic
  mix 정직 경계)·multi-qubit 합성(KAK honest 판별)은 아직 없음.**)
- **pathsum ring-exact 컬럼(P6b)**: `pathsum_ring_column` — ℤ[ζ₂₅₆]·QFT 가족 정수 등식·3자 바인딩.
  (**전 registry 컬럼 ring-exact 자동 전파·비-2^t 위상(ζ₃·ζ₅ 혼합 환)·Toffoli 경로합 대형 앱은 아직 없음.**)

### 3j. 예비 판정분 (재제안 시 보강 조건)
- **Floquet SPT 정수불변량**·**3D ℤ₂ weak indices**·**lattice surgery 물리 패치 Tier-2 실봉인**·**정수 나눗셈**·
  **큐딧 심플렉틱**·**SU(2)_k(k≥5)·SU(3)_k MTC**·**BMW**·**negativity/mana monotone**·**Spekkens 준비 맥락성** —
  구체 인스턴스·오라클·복리 강화 시 재평가.
- ★**진짜 제11 검증경로(공개과제)**: 10 경로 + 6건 후보(전부 강등/불채택)와 **검증 객체가 상이한 새 수학 대상**.
  "전체 unitary 동치를 조합/대수 불변량으로 판정"하는 구성이 아직 없다. (P6b 는 제4경로 강화이지 제11 아님 —
  자가강등/정직표기가 채택 조건임을 재확인.)

**핵심: 사소한 변형 금지. 질적 새 계층. 괄호 "아직 없음"이 관문이면 환영.**

## 4. 우리가 원하는 것 (방향 감 — 강요 아님)

- **검증 메타** — ★진짜 제11 경로(공개과제)·ring-exact 자동 전파·arb 구간산술(QSVT)·비-2^t 혼합 환.
- **합성 심화** — ★T-count 최적 합성(최단성 하한 증명)·임의각(비-π/2^k)·multi-qubit honest 합성 판별 —
  v15 부분해제+RS-형(07-19 소비)의 심화. (RS-형 ε 1e-5 재제안은 무효 — §3s.)
- **표현론 심화** — H²(Sₙ)/2.A₆/2.A₇ Schur cover·모듈러(Brauer) 표현·크리스탈 기저 — Fourier 실봉인은 §2 경계.
- **애니온/TQC 심화** — D^ω(ℤ₂³) type-III(비아벨화)·twisted 비아벨 D^ω(S₃)·D(A₄)/D(S₄)·SU(2)_k(k≥5)·SO(N)_k·
  Witt 군 층위 MTC 비교·T-불변량의 한계(Mignard-Schauenburg).
- **동역학/SPT 심화** — 3D DIII·class C/CI·FK n=6 보호구조·interacting 분류 일반·Floquet SPT·비-abelian Berry.
- **부호 심화** — lattice surgery 물리 패치 Tier-2 실봉인·twist defect·color-code surgery·d≥5.
- 그 밖에 **당신이 더 나은 축을 알면 제안하라.**

## 4′. ★성공 패턴 (v1→v15)

**(a) 게이트 우회** · **(b) 직접 닫힌형 구성** · **(c) 승인-module 사람게이트** · **(d) 반증→회수·복리** ·
**(e) 기소비 선점 대조·교차 복리** · **(f) 다중 독립 경로·Tier-2 드라이버** · **(g) 봉인 전 선검증 반증** ·
**(h) closed-negative 상보 positive·rational group 판정** · **(i) crux-probe 우선·redirect** ·
**(j) 선검증이 외부 제안 정정·certificate layer 정직 강등** · **(k) FS 지표 판별·제11 공개과제** ·
**(l) FS 삼분 완성·state-independent KS·완전 modularity** · **(m) 유한군 vs Lie MTC 양대 원천·나이브
궤도≠KS·외부 수치 자기모순 검출**.

**(n) ★v15 신규 패턴 4개**:
- **쌍/궤도 대조가 검증객체**: 단독 인스턴스가 아니라 **쌍(D₄/Q₈)·클래스 전수(H³ 8개)의 분기/궤도 구조**가
  관측의 본체 — "같은 X 를 공유하나 Y 가 갈라진다" 형태로 제안하라(문자표/T·untwisted/fusion ring).
- **융합환 전이 = twist 판별지표**: cocycle twist 가 스핀(T)만 아니라 **융합환 자체를 바꿀 수 있다**
  (D^ω(ℤ₂²) type-II → ℤ₄×ℤ₄). MTC 비교 제안은 T-다중집합과 융합군을 **모두** 보고하라.
- **ring shadow 정수 축약**: 대형 심볼릭(sympy) 곱은 폭주한다 — **정수환 shadow(ℤ[ω] 튜플)로 축약 후
  소형 잔여식만 심볼릭 처리**(600s+→2.3s 실증). exact 주장 제안은 산술 경로의 복잡도를 명시하라.
- **부분해제 = 존재구성 + ε-sidecar 분리**: 원리적 경계(§2)는 **특정 인스턴스의 honest 존재구성**으로
  부분해제 가능하되, 근사 품질은 **봉인과 분리된 인증 sidecar**(상한·tightness 무주장)로 정직 유지.

## 5. 반드시 지켜야 할 제약

- **결정론 불가침**·**오라클은 사용만**·**honest decomposition**(MatrixGate 금지·opaque KAK-fitted float 금지)·
  **self-contained**·**하드웨어 out**.
- **정직 경계** — 근사·확률·측정후처리는 **관측**. exact ≠ 근사, dense ≠ structural ≠ subspace ≠ tableau.
  봉인 ≠ 관측(certificate/witness 는 봉인 자산 아님). ★승인 게이트(√d 등) ≠ 봉인가능성. ★ε-인증은 **상한**
  (tightness 무주장·직교 sidecar — Trotter/gridsynth 2가족 선례).
- **★registry 실측 novelty + 제안값 자체 재검증**: 공개 저장소 **https://github.com/sadpig70/QuantaFoundry**.
  ★**제안의 구체 좌표/문자표/필드/FS지표/양자차원/코호몰로지 차원은 스스로 독립 재검증**(외부 제안 오류 반복
  실재: KS-18 좌표·A₅ ζ₅·Yu-Oh·treewidth·Conway-31·SU(2)₄ D²=8 자기모순). 불가하면 §3 정독 + 구조적 novelty.

## 6. 답변 형식 (제안마다)

**3~5개**를 impact×feasibility 순: 1. **proposal**(축+구체 인스턴스) · 2. **rationale**(정체성·compounding·
교차 복리) · 3. **feasibility**(봉인 게이트·오라클 검증·§4′(b) exact·**봉인 경로 명시**: Tier-0 dense/Tier-2/관측/
certificate/ε-sidecar) · 4. **risk**(정직 경계·certificate/봉인 구분) · 5. **novelty**(§3 특히 **3s/3q/3j** 대조
+ 시차 강건성).

## 7. 개념 미니 용어집

- **봉인/compounding/honest boundary/teeth/Tier-2/closed-negative/rational group/crux-probe/ambivalent/
  Frobenius-Schur 삼분/certificate layer** — 유지.
- **검증경로 10 + 제11 후보 6건(전부 강등/불채택)**: dense·tableau·ZX·path-sum ℤ[ζ_{2^t}](★v15 ring-exact
  컬럼 상향)·stabilizer-rank·matchgate·tensor-network·QMDD·ANF·Gröbner + 강등 6건. ★진짜 제11 미발견.
- **ε-인증 2가족(신규)**: Trotter/Suzuki(교환자 상한) + gridsynth(위상정렬 op-norm 등식) — 목표 대비 오차
  **상한**, 직교 sidecar(APPROX-GUARANTEES). 봉인은 항상 "그 회로의 unitary" exact.
- **ring shadow(신규)**: 회로 엔트리의 정수환(ℤ[ω]/√2^m) 그림자 — exact 검증·심볼릭 축약·컬럼증인 바인딩에
  3중 사용(§4′n).
