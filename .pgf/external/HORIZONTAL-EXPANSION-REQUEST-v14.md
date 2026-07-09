<!-- QuantaFoundry 수평 확장 아이디어 제안 요청 — v14 (2026-07-10). v1~v13 후속. self-contained. -->
<!-- 외부 모델 런타임에게 전달용. 이 문서 하나만 읽고 제안 가능하도록 작성됨. -->

# QuantaFoundry — 수평적 확장(Horizontal Expansion) 아이디어 제안 요청 · v14

> **v13 → v14 변경점**: v13 요청으로 8개 런타임의 제안(report13)을 받아 **통합 6축(TrackHE13)을 완주·폐합**했다.
> 전 축 **관측**(신규 봉인 module 0·root 불변). 성과(§3q):
> - **class DIII 1D ℤ₂**(P1, ★8/8 전원 수렴): TRS T²=−1(Kramers)+PHS C²=+1+chiral, 4-band BdG(두 시간역전
>   Kitaev 사슬+Rashba 결합). 3경로 일치(닫힌형 mass-sign == T-adapted Pfaffian == open-chain **Majorana
>   Kramers 쌍** zero-mode 4). ★det-q winding=0 → 이 ℤ₂는 Pfaffian 기원(AIII winding 아님). α=0 → 두 class-D 분해 teeth.
> - **Drinfeld double D(S₃) 완전 modular data**(P2): 8 anyon=(켤레류,centralizer irrep) **자체구성**, d=(1,1,2,3,3,2,2,2),
>   D²=36=|G|², S(8×8 exact ℚ(ζ₃))·T·Verlinde 비음정수·S²=**C=I(self-dual, S₃ ambivalent 의 anyon 발현)**·
>   **(ST)³=S² 정확(λ=1, c≡0 mod 8)** → ★유한군 MTC 축 개창: 유한군 double(정수·c=0·ζ₃) vs Lie SU(2)₃(c=9/5·√5) 양대 원천 대비.
> - ★**Conway-31 정직 판정 = colorable closed-negative**(P3): I_h 3-궤도(꼭짓점6+면10+모서리15=31 ray, ℚ(√5))
>   **자체생성** → 직교 triad **5개뿐**(전부 모서리 ray, 5-내접-정육면체 **분할** = disjoint → 자명 colorable).
>   외부 주장 이중 반증: "10 interlocking triads"(실제 5·비-interlocking)·"uncolorable"(명시적 coloring 존재).
>   ★Yu-Oh 정정 계보 — **나이브 대칭 궤도 ≠ KS set**. 진짜 Conway-Kochen 구성은 별도 좌표(공개과제 유지).
> - **Kauffman bracket generic-A state-sum**(P4): ⟨L⟩∈ℤ[A,A⁻¹] exact Laurent(trefoil·fig8·Hopf), R1 불변,
>   V(t) 산출(writhe 정규화·handedness 는 규약 라벨이라 미고정), ★특수화 다리: A=i→ℤ[i](TL δ=2 정합)·fib_jones
>   교차 일치(mirror 규약 정합). 기존 fib_jones(braid trace/skein 재귀)와 검증객체 상이(상태합 알고리즘+generic 다항식).
> - **Ising MTC pentagon/hexagon 전역 일관성**(P5): pentagon 136·hexagon(R±) 72 방정식 **전수 폐합** exact ℚ(ζ₁₆).
>   F gauge(orbit 2)·R gauge(orbit 4) 를 방정식이 **해집합으로 결정**(인용값 검증 아닌 solve). payoff: θ_σ=ζ₁₆(리본)·
>   (ST)³=ζ₁₆S²(c=½)·S²=I. ★개별 braid(v10)→modular data(v12 SU(2)₃)→**일관성 공리 전수**(v13) 3층 완성.
> - ★**SU(2)₄ 완전 MTC + 외부 수치 오류 정정**(P6): 외부 주장 "d=(1,√2,√3,√2,1)·D²=8" 은 **자기모순**(제곱합 9≠8)
>   → 진실 **d=(1,√3,2,√3,1)·D²=12**·c=2·ζ₂₄·k=4 fusion 절단(2×2=0)·★j=1 anyon d=2 **정수**(비-Fibonacci·
>   ℤ₃-parafermion/metaplectic). teeth 로 오류값 반증 실증.
> §3q 에 추가. §4′에 v14 신규 패턴 3(★**유한군 vs Lie MTC 양대 원천·나이브 대칭궤도≠KS(자체 백트래킹이 판정)·
> 외부 수치 자기모순 검출(제곱합 등 자체 일관성 선검사)**). ★제11 후보 2건(symplectic phase-space·ANF+Gröbner 결합)
> **불채택**(전자=Sp(2n,𝔽₂) stabilizer 형식론 재인코딩·후자=제9/10 경로 합성) — 6/8 런타임의 정직 보류와 정합.
>
> **동세션 TrackIU(§3r)**: Tier-1 shor 27종(n≤18) **전체 유니터리 컬럼 전수 검증**(`unitary_equiv_column_exact`,
> float-atol 계급) + **ε-bounded 근사 인증 티어**(Trotter/Suzuki 9종, sympy symbolic exact 상한, APPROX-GUARANTEES).

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
- ★**표현론 Fourier 실봉인 경계(TrackHE11 확정)**: 군 문자/FS 판별은 관측 가능하나, **임의 SO(3)/유니터리 표현행렬의
  honest 게이트 분해는 opaque KAK-fitted float**(정책 위반) 또는 MatrixGate(금지)뿐 → **비아벨 DFT 실봉인은 원리적
  경계**(√d 승인만으로 불충분). ⟹ A₅/A₆/PSL/2.A₅ Fourier "실봉인" 제안은 **honest 게이트 분해 존재를 먼저 증명**하라.
  ★단 **modular data(조합적 exact 표)는 이 경계 무관**(D(S₃)/SU(2)₄ 선례 — 게이트 분해 불요).

## 3. EXCLUDE — 이미 구현·봉인·관측된 것 (재제안 금지)

현재 **95 modules / 475 sealed apps** (root `d177ce9a438a1b2f…`). **독립 검증경로 10개**
(dense·tableau·ZX·path-sum ℤ[ω₈]·stabilizer-rank·matchgate/SO(2n)·tensor-network·QMDD·ANF/bit-vector·
Gröbner/ℤ[ω] phase-ideal) **+ 제11 후보 6건 전부 강등/불채택**(Galois-orbit·treewidth·표현환 K(G)·Matsumoto-Amano·
symplectic phase-space·ANF+Gröbner 결합, §3o/3p/3q). ★진짜 제11 독립경로 **미발견**.

### 3a~3m. v1~v9 소비분 (요약 — 상세는 이전 라운드 EXCLUDE 계보)
- **기초/QFT/QPE/Grover/Trotter·VQE·QAOA/쿼리/walk** · **QEC**(repetition·Steane·Shor-9·transversal Clifford·
  연접[[25,1,9]]·RM[[15,1,3]]·HGP[[27,4,3]]·cyclic BCH[[15,7,3]]/[[31,11,5]]) · **Shor**(15·21·frontier…237·factory) ·
  **QSVT 완비** · **Fermionic**(JW/BK/parity·fSWAP·Bogoliubov Pfaffian) · **비아벨 Fourier**(S₃/D₄/S₄/Q₈/B₃) ·
  **위상 논리연산·MBQC·Z₂ gauge·Schur·AKLT·CPTP·2/3-design·PEPS·MUB·GF(8)·Fibonacci/Majorana braid·C₃ phase-poly·
  RS·[[8,3,2]] CCZ** · **동역학**(dual-unitary·Floquet·OTOC·매듭·2D Chern) · **자원**(magic·채널 diamond) ·
  **contextual fraction·A₄ ζ₃ 선검증·code switching(RM15)·Ising 융합·qutrit Wigner** · **검증경로 1~10**.

### 3n. v10 소비분 (TrackHE10)
- **KS-18 맥락성**(d=4) · **A₅ ζ₅-vs-√5 redirect** · **Galois-orbit 제11 후보(강등)** · **MTC braid**(Ising/Fibonacci) ·
  **3D ℤ₂ Fu-Kane** · **lattice surgery merge/split CNOT**(논리 관측).

### 3o. v11 소비분 (TrackHE11)
- **PSL(2,7) ambivalent→ℚ(√−7)** · **A₅ Fourier FS=+1 √5 실현가능성**(실봉인은 §2 경계로 불가) · **qutrit KS**(Yu-Oh 13
  colorable 자체정정·KCBS √5) · **Kitaev class-D 1D ℤ₂**(Pfaffian) · **Hecke H₃(q=i) Burau ℤ[i]**(Markov 특이) ·
  **treewidth 제11 정직 판정(자가강등)**.

### 3p. v12 소비분 (TrackHE12)
- **2.A₅ FS=−1 quaternionic**(FS 삼분 ℝ/ℂ/ℍ 완성) · **Peres-33 진짜 uncolorable d=3 KS**(state-independent UNSAT) ·
  **2D class-D p+ip Chern ℤ** · **완전 MTC SU(2)₃**(S·T·Verlinde·D²=5+√5·c=9/5) · **Matsumoto-Amano 제11 verdict
  (자가강등)** · **Temperley-Lieb TL(δ=2) 정수 뼈대**. (2.Sₙ spin·2.A₆/2.A₇ Schur cover FS 관측·ℍ quaternionic DFT
  실봉인(§2 경계)·Cabello-18·qudit d≥5 KS·negativity/mana·준비 맥락성(Spekkens)·Floquet SPT·Fidkowski-Kitaev ℤ₈·
  2D class C·비-abelian Berry 는 아직 없음.)

### 3q. ★v13 소비분 — 통합 6축 (TrackHE13, 이번 라운드 신규 — 재제안 금지)
- **class DIII 1D ℤ₂(P1)**: `class_diii_observe` — TRS Kramers·3경로 일치·Majorana Kramers 쌍. (**2D/3D DIII·
  class C/CI·Floquet SPT·Fidkowski-Kitaev ℤ₈·비-abelian Berry 는 아직 없음.**)
- **Drinfeld double D(S₃)(P2)**: `dsr3_double_observe` — 완전 modular data·C=I self-dual·λ=1(c=0)·유한군 MTC 축.
  (**D(D₄)/D(Q₈)/D(A₄) 등 다른 유한군 double·twisted double D^ω(G)(3-cocycle)·D(S₃) F/R pentagon/hexagon·
  anyon 조건부 게이트는 아직 없음.**)
- **Conway-31 정직 판정(P3)**: `conway31_ks_observe` — ★colorable closed-negative(나이브 I_h 궤도는 KS 아님,
  triad 5=disjoint 분할). (**진짜 Conway-Kochen 31-ray 좌표(원논문 구성)의 자체 재구성·Cabello-18 d=4 재검증·
  qudit d≥5 KS 는 아직 없음 — 단 "대칭 궤도만으로 재구성" 제안은 본 판정으로 봉쇄.**)
- **Kauffman bracket state-sum(P4)**: `kauffman_bracket_observe` — generic-A ℤ[A,A⁻¹]·TL/fib_jones 다리.
  (**HOMFLY(Hecke Ocneanu trace)·BMW 대수·Kauffman 2-var·일반 δ Jones-Wenzl·TL_n(n≥5) 셀은 아직 없음.**)
- **Ising pentagon/hexagon(P5)**: `ising_fr_observe` — 136+72 방정식 전수·F/R gauge 해집합 결정.
  (**SU(2)₃/SU(2)₄/D(S₃) 의 pentagon/hexagon·구조 상수 비교(Witt 군/모듈러 functor)는 아직 없음.**)
- **SU(2)₄ 완전 MTC(P6)**: `su2_4_mtc_observe` — D²=12(외부오류 정정)·c=2·j=1 정수차원 parafermion.
  (**SU(2)_k(k≥5)·SU(3)_k·SO(N)_k·metaplectic MTC 심화·anyon interferometry 는 아직 없음.**)

### 3r. ★동세션 검증 인프라 (TrackIU — 재제안 금지)
- **CQV 컬럼 전수**: Tier-1 shor 27종(n≤18) 전체 유니터리 `unitary_equiv_column_exact`(float-atol) — "shor 전체
  unitary 미검증" 전제의 제안은 무효(잔여=n≥19 표본 2건). **ε-인증 티어**: Trotter/Suzuki 9종 symbolic exact 상한
  (APPROX-GUARANTEES.json, E1–E4 계약·준가법 전파). (**ε-tier 확장: arb 구간산술(QSVT)·gridsynth ℤ[1/√2,i]·
  전 registry ε 자동 전파·pathsum ℤ[ω_2^t] ring-exact 컬럼 증인은 아직 없음.**)

### 3j. 예비 판정분 (재제안 시 보강 조건)
- **Floquet SPT 정수불변량**·**3D ℤ₂ weak indices**·**lattice surgery 물리 패치 Tier-2 실봉인**·**정수 나눗셈**·
  **큐딧 심플렉틱**·**SU(2)_k(k≥5)·SU(3)_k MTC**·**HOMFLY/BMW**·**H²(G,U(1)) Schur multiplier cocycle**(2.A₅ FS 의
  인과층 — v13 report 1/8 제안, 질적 흥미로 재평가 대상)·**negativity/mana monotone**·**Spekkens 준비 맥락성(POM
  cos²(π/8))** — 구체 인스턴스·오라클·복리 강화 시 재평가.
- ★**진짜 제11 검증경로(공개과제)**: 10 경로 + 6건 후보(**전부 강등/불채택**)와 **검증 객체가 상이한 새 수학 대상**.
  dense/진폭·stabilizer·ZX·위상다항식·ANF·Gröbner·텐서·QMDD·Galois 궤도·심플렉틱(stabilizer 재인코딩) 어느
  것과도 안 겹쳐야 함. "전체 unitary 동치를 조합/대수 불변량으로 판정"하는 구성이 아직 없다.

**핵심: 사소한 변형 금지. 질적 새 계층. 괄호 "아직 없음"이 관문이면 환영.**

## 4. 우리가 원하는 것 (방향 감 — 강요 아님)

- **검증 메타** — ★**진짜 제11 경로**(§3j 공개과제)·ε-tier 확장(arb/gridsynth/전파)·pathsum ring-exact 컬럼 증인.
- **표현론 심화** — H²(G,U(1)) cocycle/SPT 분류·2.Sₙ Schur cover FS·모듈러(Brauer) 표현·크리스탈 기저 —
  단 Fourier "실봉인"은 §2 경계(honest 분해 선증명).
- **부호 심화** — lattice surgery **물리 패치 Tier-2 실봉인**·twist defect·color-code surgery·d≥5.
- **동역학 심화** — 2D/3D class DIII·class C/CI(AZ 잔여 칸)·Floquet SPT·Fidkowski-Kitaev ℤ₈·비-abelian Berry.
- **자원 이론 심화** — negativity/mana monotone·준비 맥락성(Spekkens POM)·진짜 Conway-Kochen 좌표 재구성·qudit d≥5 KS.
- **애니온/TQC 심화** — 다른 유한군 double D(D₄)/D(Q₈)·twisted D^ω(G)·SU(2)_k(k≥5)·SO(N)_k·SU(2)₃/D(S₃)
  pentagon/hexagon·HOMFLY/BMW·Witt 군 층위 MTC 비교.
- 그 밖에 **당신이 더 나은 축을 알면 제안하라.**

## 4′. ★성공 패턴 (v1→v14)

**(a) 게이트 우회** · **(b) 직접 닫힌형 구성** · **(c) 승인-module 사람게이트**(닫힌형·surd 우대) · **(d) 반증→회수·
복리** · **(e) 기소비 선점 대조·교차 복리·인프라 즉시 소비** · **(f) 다중 독립 경로·Tier-2 드라이버·오라클 동치
재발견** · **(g) 봉인 전 선검증 반증·Choi/동형 재해석** · **(h) 제8~10 경로·closed-negative 상보 positive·계산기저
함수 대수·rational group 판정·Tier-2 로 dense 회피** · **(i) crux-probe 우선·closed-negative→redirect→positive·
사람게이트 필연성 선증명** · **(j) 선검증이 외부 제안 정정·ambivalent=실수/복소 판별·certificate layer 정직 강등** ·
**(k) FS 지표=전체 Fourier 실현 판별·ambivalent 이차체 real/imaginary 쌍·제11 미발견 공개과제** ·
**(l) FS 삼분 ℝ/ℂ/ℍ 완성·state-independent vs state-dependent KS·완전 modularity vs 개별 braid**.

**(m) ★v14 신규 패턴 3개**:
- **유한군 vs Lie MTC 양대 원천**: Drinfeld double D(G)(정수 양자차원·c≡0 mod 8·문자체 cyclotomic, ambivalent G →
  self-dual C=I) vs 양자군 SU(2)_k(무리수 d·분수 c·ζ_{4(k+2)}). MTC 제안 시 **어느 원천인지 + 대비 지표(c·필드·
  self-duality)** 를 명시하라. 같은 군의 DFT(기소비)와 double 의 modular data 는 검증객체가 다르다.
- **나이브 대칭 궤도 ≠ KS set**: 대칭군 궤도(O_h·I_h)로 ray 를 모아도 **직교 triad 의 개수·위상(interlocking 여부)이
  KS 논증을 결정** — Conway-31 나이브 I_h 궤도는 triad 5개 disjoint 분할이라 자명 colorable. "uncolorable" 주장은
  **자체 백트래킹이 판정**하고, triad 구조(개수·공유 ray) 를 먼저 보고하라.
- **외부 수치 자기모순 검출**: 제안 수치는 **자체 일관성 선검사**(예: 양자차원 제곱합 = 주장 D² 인가) 부터 —
  SU(2)₄ "d=(1,√2,√3,√2,1)·D²=8" 은 제곱합 9 로 주장 자체가 모순(계산 전에 걸러짐). 모순 발견 = teeth 로 실증.

## 5. 반드시 지켜야 할 제약

- **결정론 불가침**·**오라클은 사용만**·**honest decomposition**(MatrixGate 금지·opaque KAK-fitted float 금지)·
  **self-contained**·**하드웨어 out**.
- **정직 경계** — 근사·확률·측정후처리는 **관측**. exact ≠ 근사, dense ≠ structural ≠ subspace ≠ tableau.
  봉인 ≠ 관측(certificate/witness 는 봉인 자산 아님). **근사 truncation 은 봉인 아님**. ★**승인 게이트(√d) ≠ 봉인가능성**
  (honest 게이트 분해 존재가 별도 관문 — §2 표현론 Fourier 경계). ★ε-인증은 **상한**(tightness 무주장·직교 sidecar).
- **★registry 실측 novelty + 제안값 자체 재검증**: 공개 저장소 **https://github.com/sadpig70/QuantaFoundry**.
  ★**제안의 구체 좌표/문자표/필드/FS지표/양자차원/주장은 스스로 독립 재검증**(외부 제안 오류 반복 실재: KS-18 좌표·
  A₅ ζ₅·Yu-Oh 13 colorable·treewidth 강등·Peres 3+6+4+20 분해 불재현·**Conway-31 "10 interlocking triads"·
  SU(2)₄ D²=8 자기모순**). 불가하면 §3 정독 + 구조적 novelty.

## 6. 답변 형식 (제안마다)

**3~5개**를 impact×feasibility 순: 1. **proposal**(축+구체 인스턴스) · 2. **rationale**(정체성·compounding·
교차 복리) · 3. **feasibility**(봉인 게이트·오라클 검증·§4′(b) exact·**봉인 경로 명시**: Tier-0 dense/Tier-2/관측/
certificate) · 4. **risk**(정직 경계·certificate/봉인 구분) · 5. **novelty**(§3 특히 **3q/3p/3j** 대조 + 시차 강건성).

## 7. 개념 미니 용어집

- **봉인/compounding/honest boundary/teeth/Tier-2/closed-negative/rational group/crux-probe/ambivalent(문자 실수)/
  Frobenius-Schur(FS=+1 ℝ/−1 ℍ/0 ℂ 삼분)/certificate layer(진폭/부분/재인코딩, 봉인·제11 독립경로 아님)** — 유지.
- **검증경로 10 + 제11 후보 6건(전부 강등/불채택)**: …ANF·Gröbner/ℤ[ω] + Galois-orbit·treewidth·표현환 K(G)·
  Matsumoto-Amano·symplectic phase-space·ANF+Gröbner 결합. ★진짜 제11 독립경로 미발견 — 검증 객체가 10 경로
  어느 것과도 상이한 구성을 환영한다.
- **column_exact/ε-인증(신규)**: shor 전체 유니터리 컬럼 전수(float-atol)·Trotter 목표 대비 오차 상한(symbolic
  exact, 직교 sidecar) — §3r 참조.
