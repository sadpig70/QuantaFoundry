<!-- QuantaFoundry 수평 확장 아이디어 제안 요청 — v13 (2026-07-09). v1~v12 후속. self-contained. -->
<!-- 외부 모델 런타임에게 전달용. 이 문서 하나만 읽고 제안 가능하도록 작성됨. -->

# QuantaFoundry — 수평적 확장(Horizontal Expansion) 아이디어 제안 요청 · v13

> **v12 → v13 변경점**: v12 요청으로 8개 런타임의 제안(report12)을 받아 **통합 6축(TrackHE12)을 완주·폐합**했다.
> 전 축 **관측**(신규 봉인 module 0·root 불변). 성과(§3p):
> - ★**2.A₅ 이중피복 FS=−1 quaternionic**(P1): binary icosahedral 120 quaternion **자체구성**, 2-dim spinor
>   FS=(1/120)Σ(4w²−2)=**−1**(quaternionic) → ★**Frobenius-Schur 삼분 완성**: A₅ FS=+1(ℝ 실수)·**2.A₅ FS=−1(ℍ 사원수)**·
>   PSL(2,7) FS=0(ℂ 복소) = **Frobenius 3대 나눗셈대수 완전 대응**. 문자체 ℚ(√5).
> - **Peres-33 진짜 uncolorable d=3 KS**(P2): O_h pool(성분 {0,±1,±√2}) **자체생성**(외부좌표 불신)→직교 triad 16
>   참여 ray=정확히 33, 규칙 (a)직교쌍 not-both-1 + (b)triad≥1 **전수 백트래킹 UNSAT** = **state-independent** KS.
>   ★Yu-Oh 13 colorable(v11)이 남긴 "진짜 uncolorable d=3" 공백을 메움. state-independent vs KCBS state-dependent 구분.
> - **2D class-D p+ip Chern ℤ**(P3): BdG H(k)=(M−2t Σcos)σz+Δ(sin·σx,σy), path A 닫힌형(mass-sign)==path B FHS
>   격자 numeric, 3상 {0,±1} 실현 → ★1D Kitaev ℤ₂(v11) → **2D ℤ Chern** AZ 차원사다리.
> - **완전 MTC SU(2)₃**(P4): modular data S unitary·S²=C·Verlinde 비음정수·N₂₂=(1,0,1,0) **τ×τ=1+τ Fibonacci**·
>   d=(1,φ,φ,1)·**D²=5+√5**·(ST)³=S²(c=9/5), exact ℚ(√5)/ζ₂₀. ★개별 Ising/Fib braid(v10) → **완전 modularity** 승격.
> - ★**Matsumoto-Amano 정규형 = 제11 경로 honest verdict**(P5): 검증객체=syntactic canonical word(표면상 독립)이나
>   recognition 이 unitary 를 ℤ[1/√2,i]=ℤ[ω] exact 산술로 다룸 + word↔unitary 전단사(1q) → **자가강등(재인코딩)**
>   (treewidth→tensor-net 과 동형). ★**진짜 제11 경로 = 여전히 미발견 공개과제**(4번째 후보 강등).
> - **Temperley-Lieb TL(δ=2) 정수 뼈대**(P6): singlet 블록 e²=2e·e_i e_{i±1} e_i=e_i·far-commute·Kauffman σ=A+A⁻¹e
>   braid, δ=−(q+q⁻¹)=2 q=−1 → **순수 ℤ**. ★Hecke H₃(q=i, q+q⁻¹=0 Markov특이)(v11) **정수층 상보**.
> §3p 에 추가. §4′에 v13 신규 패턴 3(★**FS 삼분 ℝ/ℂ/ℍ 완성·state-independent vs state-dependent KS·완전 MTC
> modularity vs 개별 braid**). ★제11 경로 후보 4건(Galois-orbit·treewidth·표현환 K(G)·MA 정규형) **전부 자가강등**.

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

## 3. EXCLUDE — 이미 구현·봉인·관측된 것 (재제안 금지)

현재 **95 modules / 475 sealed apps** (root `d177ce9a438a1b2f…`). **독립 검증경로 10개**
(dense·tableau·ZX·path-sum ℤ[ω₈]·stabilizer-rank·matchgate/SO(2n)·tensor-network·QMDD·ANF/bit-vector·
Gröbner/ℤ[ω] phase-ideal) **+ 제11 후보 4건 전부 자가강등**(Galois-orbit·treewidth·표현환 K(G)·Matsumoto-Amano,
§3o/3p). ★진짜 제11 독립경로 **미발견**.

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

### 3p. ★v12 소비분 — 통합 6축 (TrackHE12, 이번 라운드 신규 — 재제안 금지)
- **2.A₅ FS=−1 quaternionic(P1)**: `2a5_fs_observe` — FS 삼분 ℝ/ℂ/ℍ 완성. (**2.Sₙ spin·2.A₆·2.A₇ Schur cover·
  ℍ 위 quaternionic DFT 실봉인(honest 게이트 분해 필요, §2 경계)은 아직 없음.**)
- **Peres-33 진짜 uncolorable d=3 KS(P2)**: `peres33_ks_observe` — state-independent UNSAT. (**Conway-31·Cabello-18·
  qudit d≥5 KS·negativity/mana monotone·준비 맥락성(Spekkens)은 아직 없음.**)
- **2D class-D p+ip Chern(P3)**: `class_d_2d_chern_observe` — ℤ Chern(닫힌형==FHS). (**class DIII(TRS Kramers)·
  Floquet SPT 정수불변량·Fidkowski-Kitaev ℤ₈·2D class C·비-abelian Berry 는 아직 없음.**)
- **완전 MTC SU(2)₃(P4)**: `su2_3_mtc_observe` — S·T·Verlinde·τ×τ=1+τ·D²=5+√5. (**SU(2)_k (k≥4)·SU(3)_k·
  Drinfeld double·pentagon/hexagon F/R 완전 일관성 봉인·anyon 조건부 게이트는 아직 없음.**)
- **Matsumoto-Amano 제11 verdict(P5)**: `matsumoto_amano_verdict_observe` — 자가강등(ℤ[ω] 재인코딩). (**진짜 제11
  독립경로=미발견 공개과제 유지.**)
- **Temperley-Lieb TL(δ=2)(P6)**: `temperley_lieb_observe` — 정수 뼈대. (**일반 δ Jones-Wenzl·TL_n(n≥5) 셀·
  Kauffman bracket knot 불변량·BMW 대수는 아직 없음.**)

### 3j. 예비 판정분 (재제안 시 보강 조건)
- **class DIII·Floquet SPT 정수불변량**·**3D ℤ₂ weak indices**·**lattice surgery 물리 패치 Tier-2 실봉인**·
  **정수 나눗셈**·**큐딧 심플렉틱**·**SU(2)_k(k≥4) MTC**·**knot 불변량(Jones/HOMFLY)** — 구체 인스턴스·오라클·복리 강화 시 재평가.
- ★**진짜 제11 검증경로(공개과제)**: 10 경로 + Galois/treewidth/표현환 K(G)/Matsumoto-Amano 후보(**전부 자가강등**)와
  **검증 객체가 상이한 새 수학 대상**. dense/진폭·stabilizer·ZX·위상다항식·ANF·Gröbner·텐서·QMDD·Galois 궤도 어느
  것과도 안 겹쳐야 함. "전체 unitary 동치를 조합/대수 불변량으로 판정"하는 구성이 아직 없다.

**핵심: 사소한 변형 금지. 질적 새 계층. 괄호 "아직 없음"이 관문이면 환영.**

## 4. 우리가 원하는 것 (방향 감 — 강요 아님)

- **검증 메타** — ★**진짜 제11 경로**(§3j 공개과제, certificate/재인코딩 강등 아닌)·회로 동치 증명서.
- **표현론 심화** — 2.Sₙ Schur cover·모듈러(Brauer) 표현·크리스탈 기저 — 단 Fourier "실봉인"은 §2 경계(honest 분해 선증명).
- **부호 심화** — lattice surgery **물리 패치 Tier-2 실봉인**·twist defect·color-code surgery·d≥5.
- **동역학 심화** — class DIII·Floquet SPT 정수불변량·3D ℤ₂ weak indices·Fidkowski-Kitaev ℤ₈·비-abelian Berry.
- **자원 이론 심화** — Conway-31·qudit d≥5 KS·negativity/mana monotone·준비 맥락성.
- **애니온/TQC 심화** — SU(2)_k(k≥4)·Drinfeld double·pentagon/hexagon 완전 일관성·knot 불변량(Jones/HOMFLY)·BMW.
- 그 밖에 **당신이 더 나은 축을 알면 제안하라.**

## 4′. ★성공 패턴 (v1→v13)

**(a) 게이트 우회** · **(b) 직접 닫힌형 구성** · **(c) 승인-module 사람게이트**(닫힌형·surd 우대) · **(d) 반증→회수·
복리** · **(e) 기소비 선점 대조·교차 복리·인프라 즉시 소비** · **(f) 다중 독립 경로·Tier-2 드라이버·오라클 동치
재발견** · **(g) 봉인 전 선검증 반증·Choi/동형 재해석** · **(h) 제8~10 경로·closed-negative 상보 positive·계산기저
함수 대수·rational group 판정·Tier-2 로 dense 회피** · **(i) crux-probe 우선·closed-negative→redirect→positive·
사람게이트 필연성 선증명** · **(j) 선검증이 외부 제안 정정·ambivalent=실수/복소 판별·certificate layer 정직 강등** ·
**(k) FS 지표=전체 Fourier 실현 판별·ambivalent 이차체 real/imaginary 쌍·제11 미발견 공개과제**.

**(l) ★v13 신규 패턴 3개**:
- **Frobenius-Schur 삼분 완성 (ℝ/ℂ/ℍ)**: FS(ρ)=+1(실수형→√d DFT)·FS=−1(quaternionic→ℍ, 실수화 불가)·FS=0(복소형→ζ_k).
  A₅(+1)·2.A₅(−1)·PSL(2,7)(0) 로 **Frobenius 3대 나눗셈대수 완전 대응**. 군 표현 제안 시 FS 지표로 실현체(ℝ/ℂ/ℍ)를
  먼저 분류하라. ★**단 "실봉인"은 별개**: 문자/FS 는 관측 가능하나 임의 표현행렬의 honest 게이트 분해는 §2 경계(opaque KAK).
- **state-independent vs state-dependent 맥락성**: Peres-33(uncolorable=모든 상태 valuation 부재, 전수 UNSAT) vs
  KCBS/Yu-Oh(부등식형, 특정 상태만 위배). d=3 KS 제안 시 **어느 유형인지 명시**하고 uncolorable 은 전수 조합증명(SAT-free)
  으로, state-dependent 는 exact 부등식으로 구분하라. 외부 "uncolorable" 주장은 반드시 자체 coloring 탐색으로 검증(Yu-Oh 정정 실재).
- **완전 modularity vs 개별 braid**: 개별 F/R-symbol(anyon 국소 연산) ≠ 완전 MTC(S·T·Verlinde·pentagon/hexagon 전역
  일관성). MTC 제안 시 **modular data 전체 공리**(S unitary·S²=C·(ST)³·Verlinde 정수·total dim)를 exact 로 제시하고,
  개별 braid(기소비)와의 질적 차이를 명시하라.

## 5. 반드시 지켜야 할 제약

- **결정론 불가침**·**오라클은 사용만**·**honest decomposition**(MatrixGate 금지·opaque KAK-fitted float 금지)·
  **self-contained**·**하드웨어 out**.
- **정직 경계** — 근사·확률·측정후처리는 **관측**. exact ≠ 근사, dense ≠ structural ≠ subspace ≠ tableau.
  봉인 ≠ 관측(certificate/witness 는 봉인 자산 아님). **근사 truncation 은 봉인 아님**. ★**승인 게이트(√d) ≠ 봉인가능성**
  (honest 게이트 분해 존재가 별도 관문 — §2 표현론 Fourier 경계).
- **★registry 실측 novelty + 제안값 자체 재검증**: 공개 저장소 **https://github.com/sadpig70/QuantaFoundry**.
  ★**제안의 구체 좌표/문자표/필드/FS지표/주장은 스스로 독립 재검증**(외부 제안 오류 반복 실재: KS-18 좌표·A₅ ζ₅·
  Yu-Oh 13 colorable·treewidth 강등·Peres 3+6+4+20 분해 불재현). 불가하면 §3 정독 + 구조적 novelty.

## 6. 답변 형식 (제안마다)

**3~5개**를 impact×feasibility 순: 1. **proposal**(축+구체 인스턴스) · 2. **rationale**(정체성·compounding·
교차 복리) · 3. **feasibility**(봉인 게이트·오라클 검증·§4′(b) exact·**봉인 경로 명시**: Tier-0 dense/Tier-2/관측/
certificate) · 4. **risk**(정직 경계·certificate/봉인 구분) · 5. **novelty**(§3 특히 **3p/3o/3j** 대조 + 시차 강건성).

## 7. 개념 미니 용어집

- **봉인/compounding/honest boundary/teeth/Tier-2/closed-negative/rational group/crux-probe/ambivalent(문자 실수)/
  Frobenius-Schur(FS=+1 ℝ/−1 ℍ/0 ℂ 삼분)/certificate layer(진폭/부분/재인코딩, 봉인·제11 독립경로 아님)** — 유지.
- **검증경로 10 + 제11 후보 4건(전부 강등)**: …ANF·Gröbner/ℤ[ω] + Galois-orbit·treewidth·표현환 K(G)·Matsumoto-Amano
  (자가강등). ★진짜 제11 독립경로 미발견 — 검증 객체가 10 경로 어느 것과도 상이한 구성을 환영한다.
