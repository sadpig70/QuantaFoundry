<!-- QuantaFoundry 수평 확장 아이디어 제안 요청 — v18 (2026-07-23). v1~v17 후속. self-contained. -->
<!-- 외부 모델 런타임에게 전달용. 이 문서 하나만 읽고 제안 가능하도록 작성됨. -->

# QuantaFoundry — 수평적 확장(Horizontal Expansion) 아이디어 제안 요청 · v18

> **v17 → v18 변경점**: v17 요청으로 8 agent 제안(report17)을 받아 **통합 6축(TrackHE17) 중 5축 완주**
> (P1 미완). 전 축 **관측/certificate**(seal root 불변). ★수렴 구조: v16 6축을 각각 심화. 성과(§3v):
> - **AZ 2D AII(QSH ℤ₂)+CII 3D(2ℤ)+weak+조대화**(P2): 2D AII Fu-Kane 4-TRIM parity·CII 3D 짝 winding
>   (★C²=−1 이 짝수 강제)·완전 weak (ν₀;ν₁ν₂ν₃)·★**조대화 그래프**(DIII ℤ→AII ℤ₂=winding mod2·
>   AIII ℤ⊃CII 2ℤ 짝수부분군). 대칭 추가=세분·제거=조대화 실증.
> - ★**exact Watrous diamond E7**(P3): E6 하계→**exact 값** 2√(1−ν²)(ν=원점→conv{eig(U†R)} 거리·
>   Watrous 2009). 3-rung bracket [D_lo,D_exact,2ε] 폐합·독립검증 dense 일치·19/19·unitary 한정.
>   ε-인증 사다리 **E5(op-norm 하계)→E6(diamond 하계)→E7(diamond exact)** 완성.
> - **D^ω(D₄) twisted anyon-count 층화**(P4): ★anyon 수 **ω-가변 22/19/16**(centralizer Schur multiplier:
>   ℤ₂² 4→1·D₄ 5→2·ℤ₄ rigid) — **"22 고정" 반증**(agent08 정정 실증). H³ 비대칭 dim 4 vs 1·차원전이.
>   ★완전 22×22 twisted S(ζ₈)·D₄ 정확 사영 캐릭터는 미착수.
> - **D^ω(ℤ₂⁴) radical 완전 층화**(P5): ★**radical=1 원리적 불가(parity 정리)** — commutator form
>   alternating→rank 짝수→radical 짝수→radical∈{0,2,4}, 홀수 불가(제안 'radical=1 부분류' 반증) +
>   radical=0 불가(rank≤2·type-II commutator 0) + **GL(4,2) 단일궤도**(Λ³V*≅V). radical∈{2,4} 정확.
> - **A₇ Brauer 모듈러 표현 구조**(P6): A₇ 9 켤레류 자체유도·**Brauer 기약 수=p-regular**(2→6,3→6,5→8,7→7)·
>   Sylow defect(5,7 cyclic→Brauer tree·2=D₄·3=ℤ₃²)·★**defect-0 block**(p5={10,10,15,35}·p7={14,14,21,35}).
>   ★완전 decomposition matrix D·Cartan C·Brauer tree 구체형은 미착수.
> - ◐**P1 BMW₃ 2변수 Kauffman F 미완**(★8/8 만장일치 최상위): 곱셈코어 검증완료(dim15·결합·braid·
>   ★e_02 관계 g₁e₂g₁=g₂e₁g₂ 자체발견)·Markov trace **σ₂ 상호작용 관계식 버그**로 비일관(§4 crux).
> §3v 에 추가. §4′에 v18 신규 패턴 3(★**closed-negative 를 parity 정리로 격상·조대화 그래프=검증객체·
> 자체유도 Schur/Brauer defect**). frontier: ★**N≤1023(10-bit 전 구간) 완결·폐합**(shor1011 최종).

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
  분해 존재를 먼저 증명하고 근사면 ε-인증(★이제 **상한+하계+exact** — E5 op-norm 하계·E6 diamond 하계·E7 diamond exact) 경로를 명시하라.
  **modular data(조합적 exact 표)는 이 경계 무관**(D(S₃)/D^ω(S₃)/D(D₄)/D(Q₈)/D^ω(D₄) 선례).

## 3. EXCLUDE — 이미 구현·봉인·관측된 것 (재제안 금지)

현재 **95 modules / 1431 sealed apps** (root `556d5e97322affa0…`). ★**Shor frontier N≤1023 완결**(10-bit 전 구간·shor1011까지). **독립 검증경로 10개**
(dense·tableau·ZX·path-sum ℤ[ζ_{2^t}]·stabilizer-rank·matchgate/SO(2n)·tensor-network·QMDD·ANF/bit-vector·
Gröbner/ℤ[ω] phase-ideal) **+ 제11 후보 6건 전부 강등/불채택**(Galois-orbit·treewidth·표현환 K(G)·Matsumoto-Amano·
symplectic phase-space·ANF+Gröbner 결합). ★진짜 제11 독립경로 **미발견**(공개과제 유지).

### 3a~3m. v1~v9 소비분 (요약)
- **기초/QFT/QPE/Grover/Trotter·VQE·QAOA/쿼리/walk** · **QEC**(repetition·Steane·Shor-9·transversal Clifford·
  연접[[25,1,9]]·RM[[15,1,3]]·HGP[[27,4,3]]·cyclic BCH[[15,7,3]]/[[31,11,5]]) · **Shor**(15·21·frontier **N≤1023 완결**·factory) ·
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

### 3t. v15 소비분 (요약 — 재제안 금지)
- D^ω(ℤ₂³) type-III(아벨 비아벨화·22 anyon·삼자 대조)·D^ω(S₃) 최초 비아벨 twist(전치 섹터)·BMW/Kauffman
  BMW₂/T(2,k)·H²(A₆) Schur(Q₈→Q₁₆)·AZ 2D C 2ℤ/CI 0/3D DIII ℤ·ε 하계 E5(op-norm 구간).

### 3u. ★v16 소비분 — 통합 6축 (TrackHE16, 이번 라운드 신규 — 재제안 금지)
- **twisted 비아벨 double(P1)**: `dtw_d4_q8_double_observe` — D^ω(D₄)/D^ω(Q₈), H³(μ₂) 4 vs 1·centralizer 차원전이.
  (**완전 22×22 twisted S 행렬·ζ₈ 구체 스핀·D^ω(D₄) 완전 modular data·twisted 비아벨 범주 동치는 아직 없음.**)
- **D^ω(ℤ₂⁴) closed-negative(P2)**: `dtw_z2_4_typeiii_observe` — 완전 비아벨화 불가(radical≥2)·H³(μ₂)=20.
  (**type-III 외 cocycle 궤도·완전 twisted S·radical=1 부분류 명시·D^ω(ℤ₂⁵ 이상)은 아직 없음.**)
- **2.A₇ Sylow tower closed-negative(P6)**: `a7_sylow_tower_observe` — 2.A₇ Sylow-2=Q₁₆(Q₃₂ 반증).
  (**2.A₇ 명시 Schur cover 구성·H²(A₇) 3-torsion·A₈ 층 Q₃₂·H²(Sₙ) spin·모듈러(Brauer) 표현은 아직 없음.**)
- **BMW₃ 3-braid fig-8(P3)**: `bmw3_fig8_observe` — BMW₃ dim=15·fig-8 Jones(비-토러스 amphichiral).
  (**★2변수 Kauffman F(a,z) via BMW₃ Markov trace(confluent dim-15 곱셈+Ocneanu trace)·다른 3-braid 매듭
  (5₁/5₂/6₁)·Links-Gould·HOMFLY/Kauffman 비포함 증명은 아직 없음.**)
- ★**ε 하계 diamond-norm E6(P4)**: `approx_certify` E6 — 채널 D_lo=2√(1−|Tr(U†R)|²/d²) 양측 bracket.
  (**exact Watrous 고유위상 diamond 값·QSVT arb 구간산술·합성 T-count 하한 전파·비유니터리 채널 diamond 는 아직 없음.**)
- **AZ 3D AII/AIII(P5)**: `az_aiii_aii_3d_observe` — AII ℤ₂ 강한 TI(Fu-Kane parity)·AIII ℤ winding·ℤ₂=winding mod2.
  (**Floquet SPT 정수불변량·비-abelian Berry·interacting AZ(FK 외) 분류·2D AII(QSH ℤ₂)·weak indices 완전 (ν₀;ν₁ν₂ν₃) 세분·CII 3D 2ℤ 는 아직 없음.**)

### 3v. ★v17 소비분 — 통합 6축 중 5 완주 (TrackHE17, 이번 라운드 신규 — 재제안 금지)
- **AZ 2D AII/CII 3D(P2)**: `az_aii2d_cii3d_observe` — 2D AII(QSH ℤ₂)·CII 3D(2ℤ 짝 winding)·완전 weak·조대화.
  (**Floquet SPT 정수불변량·비-abelian Berry·interacting AZ·3D AIII/AII Floquet·BDI 3D ℤ 는 아직 없음.**)
- ★**exact Watrous diamond E7(P3)**: `approx_certify` E7 — diamond 하계→exact 값·3-rung bracket·unitary 한정.
  (**非unitary CPTP diamond exact(SDP rational)·QSVT arb 구간산술·合성 T-count 하한 전파는 아직 없음.**)
- **D^ω(D₄) anyon-count 층화(P4)**: `dtw_d4_modular_strata_observe` — anyon ω-가변 22/19/16·H³ 비대칭·차원전이.
  (**★완전 22×22 twisted S-matrix(ζ₈ 값)·D₄ 정확 사영 캐릭터(Schur cocycle)·twisted DPR 완전 modular data 는 아직 없음.**)
- **D^ω(ℤ₂⁴) radical 층화(P5)**: `dtw_z2_4_radical_strata_observe` — radical∈{2,4}·radical=1 parity 반증·GL(4,2) 단일궤도.
  (**완전 twisted S(radical=2 최대 twist)·D^ω(ℤ₂⁵) radical(parity: n=5 홀→radical 홀 가능?)·twisted 비아벨 anyon 명시 S 는 아직 없음.**)
- **A₇ Brauer(P6)**: `a7_brauer_observe` — 9 켤레류·Brauer 수(p-regular)·Sylow defect·defect-0 block.
  (**★완전 decomposition matrix D(9×ℓ_p)·Cartan C=DᵀD·Brauer tree(p=5,7 cyclic-defect) 구체형·3.A₇ ζ₃ cover 는 아직 없음.**)
- ◐**P1 BMW₃ 2변수 Kauffman F 미완**: `bmw3_fig8_observe`(v16, Jones 1변수만). ★crux=§4 참조.
  (**★2변수 Kauffman F(a,z) via BMW₃ Markov trace 는 여전히 미해결 — §4 최우선 요청.**)

### 3j. 예비 판정분 (재제안 시 보강 조건)
- **Floquet SPT 정수불변량**·**3D ℤ₂ weak indices**·**lattice surgery 물리 패치 Tier-2 실봉인**·**정수 나눗셈**·
  **큐딧 심플렉틱**·**SU(2)_k(k≥5)·SU(3)_k MTC**·**Links-Gould/BMW₃ 2변수**·**negativity/mana monotone**·**Spekkens 준비
  맥락성**·**twist defect / color-code surgery** — 구체 인스턴스·오라클·복리 강화 시 재평가.
- ★**진짜 제11 검증경로(공개과제)**: 10 경로 + 6건 후보(전부 강등/불채택)와 **검증 객체가 상이한 새 수학 대상**.
  "전체 unitary 동치를 조합/대수 불변량으로 판정"하는 구성이 아직 없다. 자가강등/정직표기가 채택 조건.

**핵심: 사소한 변형 금지. 질적 새 계층. 괄호 "아직 없음"이 관문이면 환영.**

## 4. 우리가 원하는 것 (방향 감 — 강요 아님)

- **검증 메타** — ★진짜 제11 경로(공개과제)·ε 하계 자동 전파·QSVT arb 구간산술·비-2^t 혼합 환·exact Watrous diamond.
- **합성 심화** — T-count 최적 합성(최단성 하한 증명)·임의각(비-π/2^k)·multi-qubit honest 합성 판별.
- **애니온/TQC 심화** — D^ω(D₄)/D^ω(Q₈) 완전 twisted S 행렬·twisted DPR 완전 modular data·MS probe(|G|=55)·
  SU(2)_k(k≥5)·Witt 군 층위 MTC 비교·D^ω(ℤ₂⁴) radical=1 부분류.
- **표현론 심화** — H²(A₆/A₇) 3-torsion(Valentiner·ζ₃ 승인 게이트)·2.A₇ Schur cover 명시·모듈러(Brauer) 표현·크리스탈 기저.
- **★매듭 심화 (최우선·P1 crux)** — **2변수 Kauffman F via BMW₃ Markov trace**의 정확한 완성. ★우리 상태:
  BMW₃ dim-15 곱셈 코어 **검증완료**(결합법칙·braid g₁g₂g₁=g₂g₁g₂·역원·e²=δe·e₁e₂e₁=e₁·gᵢeᵢ=a⁻¹eᵢ·
  e_02 관계 g₁e₂g₁=g₂e₁g₂ 자체발견). ★**미해결 crux**: **σ₂ 상호작용 관계식**(g_i e_{j} e_i=g_{j}⁻¹ e_i 계열·
  twist e_i g_{i±1} e_i=a^{±1} e_i)의 정확한 **방향/a-power/부호**가 어긋나, 기본 게이트는 통과하나 올바른
  **Ocneanu Markov trace 를 admit 하지 않음**(cyclicity nullspace 내 g₂/e₂ stabilization 비일관·twist 4변형
  전수 실패). ★요청: **정확한 BMW₃ 상호작용 관례(Kauffman 규약)** 또는 **faithful 참조 표현으로 검증**
  (SO(N) R-matrix on V⊗³: a=q^{N−1}·z=q−q⁻¹·Ř 고유값 q/−q⁻¹/q^{1−N}, E=trivial 사영 — 이걸로 우리 곱셈을
  대조). fig-8(4₁) F(a,z) Jones-특수화(t⁻²−t⁻¹+1−t+t²)·amphichirality F(a,z)=F(a⁻¹,z)·v15 T(2,k) 일치가 게이트.
  Links-Gould·다른 3-braid(5₁/5₂/6₁)는 이 crux 해결 후.
- **동역학/SPT 심화** — 2D AII(QSH ℤ₂)·CII 3D 2ℤ·Floquet SPT·비-abelian Berry·interacting 분류 일반·weak index 세분.
- 그 밖에 **당신이 더 나은 축을 알면 제안하라.**

## 4′. ★성공 패턴 (v1→v18)

**(a) 게이트 우회** · **(b) 직접 닫힌형 구성** · **(c) 승인-module 사람게이트** · **(d) 반증→회수·복리** ·
**(e) 기소비 선점 대조·교차 복리** · **(f) 다중 독립 경로·Tier-2 드라이버** · **(g) 봉인 전 선검증 반증** ·
**(h) closed-negative 상보 positive·rational group 판정** · **(i) crux-probe 우선·redirect** ·
**(j) 선검증이 외부 제안 정정·certificate layer 정직 강등** · **(k) FS 지표 판별·제11 공개과제** ·
**(l) FS 삼분 완성·state-independent KS·완전 modularity** · **(m) 유한군 vs Lie MTC 양대 원천·외부 수치
자기모순 검출** · **(n) 쌍/궤도 대조=검증객체·융합환 전이=twist 판별·ring shadow 정수 축약·부분해제=존재구성+ε-sidecar** ·
**(o) 외부 수치 자체 재유도가 실제 오류 검출·teeth 무력 실측 후 대상 교체·상한→구간 양방향 인증**.

**(q) ★v18 신규 패턴 3개**:
- **closed-negative 를 parity 정리로 격상**: v16 은 "type-III 로 radical=0 불가"(전수 상한)였는데, v17 P5 는
  commutator form 이 **GF(2) alternating → rank 짝수 → radical=n−rank 짝수(n 짝수)** 라는 **구조 정리**로
  "radical=1 부분류 불가"를 원리적으로 증명했다(전수 아닌 parity 논증). ⟹ "부분류 존재" 제안은 먼저 그
  **불변량의 parity/정수성 제약**(rank 짝수·Sylow 위수·차원 정수)을 정리로 세워라. n 홀수(ℤ₂⁵)면 radical 홀수
  **가능** — parity 가 방향을 지시.
- **분류 열 완결 + 조대화 그래프 = 검증객체**: v17 P2 는 AZ 열을 채우며 **조대화 그래프**(DIII ℤ→AII ℤ₂=
  winding mod2·AIII ℤ⊃CII 2ℤ)를 검증객체로 삼았다(대칭 추가=세분·제거=조대화). 분류표 제안은 칸 값뿐 아니라
  **인접 칸 간 군-준동형(조대화/세분) 관계**를 함께 산출하면 복리·자기검증이 크다.
- **자체유도 defect/block 구조**: v17 P6 는 A₇ 를 순열군으로 지어 **Brauer 수(p-regular)·Sylow defect·
  defect-0 block** 을 전부 자체유도했다(문자표 표준값은 Σd² 불변량만 검증). 표현론 제안은 **군을 실제로 지어
  자체유도 가능한 층(클래스·위수·defect·block 개수)** 과 **문헌 의존 층(구체 문자·decomposition matrix)** 을
  명확히 분리하라.

**(q) ★v18 신규 패턴 3개** (아래 (p)=v17 유지):
- **closed-negative 가 과도확장 제안을 잡는다**: report16 의 2개 축(P2 'ℤ₂⁴ 완전 비아벨화 radical=0'·P6
  'Q₈→Q₁₆→Q₃₂ tower')이 **수학적으로 불가능**했고, 착수 전 상한 재유도(radical rank·Sylow 위수)가 정확히
  반증했다. ⟹ 제안이 **"완전/최대/전부/무한 tower"** 를 주장하면, 그 상한(코호몰로지 차원·radical·Sylow 위수·
  차수)을 **먼저 자체 재유도**하라. 불가능이면 **부분 positive(부분 비아벨화·정체 tower)로 정직 재구성**.
- **인증 계약은 계층적으로 심화된다(E5 op-norm → E6 diamond-norm)**: 같은 rigorous U·R 재계산을 재사용해
  **더 강한(연산자→채널) 하계**로 인증할 수 있다(E6: 최대얽힘 Choi 입력 트레이스거리 ≤ diamond norm).
  근사 품질 인증을 **연산자 노름 → 채널 노름 → …** 계층으로 올리는 제안 환영(단 각 계층의 정직 경계 명시:
  하계≠exact 값·유니터리 한정 등).
- **분류 열 완결 + 조대화 관계 실증**: AZ 3D 열에서 DIII(ℤ)·AII(ℤ₂)·AIII(ℤ)를 채우며 **ℤ₂=DIII winding
  mod 2**(PHS 제거 → 불변량군 조대화)를 실증했다. 분류표 칸을 채우는 제안은 **인접 칸과의 조대화/세분 관계**
  (대칭 추가=세분·제거=조대화)를 함께 보고하면 복리가 크다.

## 5. 반드시 지켜야 할 제약

- **결정론 불가침**·**오라클은 사용만**·**honest decomposition**(MatrixGate 금지·opaque KAK-fitted float 금지)·
  **self-contained**·**하드웨어 out**.
- **정직 경계** — 근사·확률·측정후처리는 **관측**. exact ≠ 근사, dense ≠ structural ≠ subspace ≠ tableau.
  봉인 ≠ 관측(certificate/witness 는 봉인 자산 아님). ★승인 게이트(√d·ζ₃ 등) ≠ 봉인가능성. ★ε-인증은
  **상한+하계 구간**(tightness 무주장·직교 sidecar — Trotter/gridsynth 2가족·E1–E7 계약: op-norm 상·하계 + diamond 하계 + ★diamond exact(Watrous)).
- **★registry 실측 novelty + 제안값 자체 재검증(v17 강화)**: 공개 저장소 **https://github.com/sadpig70/QuantaFoundry**.
  ★**제안의 구체 좌표/문자표/필드/FS지표/양자차원/코호몰로지 차원/anyon 수/radical rank/Sylow 위수는 스스로 독립
  재검증**(외부 제안·런타임 간 상충·과도확장 반복 실재: KS-18·A₅ ζ₅·Yu-Oh·treewidth·Conway-31·SU(2)₄ D²=8·
  D^ω(ℤ₂³) 22 vs 64·H²(S₃) 계수군·**ℤ₂⁴ 완전 비아벨화**·**Q₃₂ tower**·**anyon 22-고정**·**radical=1 부분류**). 불가하면 §3 정독 + 구조적 novelty.

## 6. 답변 형식 (제안마다)

**3~5개**를 impact×feasibility 순: 1. **proposal**(축+구체 인스턴스) · 2. **rationale**(정체성·compounding·
교차 복리) · 3. **feasibility**(봉인 게이트·오라클 검증·§4′(b) exact·**봉인 경로 명시**: Tier-0 dense/Tier-2/관측/
certificate/ε-sidecar) · 4. **risk**(정직 경계·certificate/봉인 구분·자체 재유도 계획·**과도확장 상한 선재유도**) ·
5. **novelty**(§3 특히 **3v/3u/3j** 대조 + 시차 강건성).

## 7. 개념 미니 용어집

- **봉인/compounding/honest boundary/teeth/Tier-2/closed-negative/rational group/crux-probe/ambivalent/
  Frobenius-Schur 삼분/certificate layer** — 유지.
- **검증경로 10 + 제11 후보 6건(전부 강등/불채택)**: dense·tableau·ZX·path-sum ℤ[ζ_{2^t}]·stabilizer-rank·
  matchgate·tensor-network·QMDD·ANF·Gröbner + 강등 6건. ★진짜 제11 미발견.
- **ε-인증 2가족·E1–E7 계약(v18 갱신)**: Trotter/Suzuki(교환자 상한) + gridsynth(위상정렬 등식) — E1–E4
  상한 + ★**E5 op-norm 하계**(mpmath Taylor expm rigorous → 구간 [ε_lo,ε_hi]) + ★**E6 diamond-norm 하계**
  (채널 수준 D_lo=2√(1−|Tr(U†R)|²/d²)=Choi 입력 트레이스거리, 양측 bracket [D_lo,2ε]). 봉인은 항상 "그 회로의
  unitary" exact.
- **ring shadow**: 회로 엔트리의 정수환(ℤ[ω]/√2^m) 그림자 — exact 검증·심볼릭 축약·컬럼증인 바인딩 3중 사용.
- **twist 판별**: cocycle twist 는 스핀(T)·융합환·**사영표현 차원(비아벨화)**·**섹터 선택성**(D^ω(S₃) 전치 섹터)·
  **centralizer H²(μ₂) 2-rank**(D^ω(D₄) vs D^ω(Q₈) 차원전이)로 판별. MTC/double 비교 제안은 이 지표들을 보고하라.
- **AZ 조대화(신규)**: 대칭류 간 불변량군 관계 — PHS 제거 시 DIII(ℤ)→AII(ℤ₂)=winding mod 2. 분류표 제안은
  인접 칸 조대화/세분 관계를 함께 보고.
