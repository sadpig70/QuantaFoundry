<!-- QuantaFoundry 수평 확장 아이디어 제안 요청 — v10 (2026-07-09). v1~v9 후속. self-contained. -->
<!-- 외부 모델 런타임에게 전달용. 이 문서 하나만 읽고 제안 가능하도록 작성됨. -->

# QuantaFoundry — 수평적 확장(Horizontal Expansion) 아이디어 제안 요청 · v10

> **v9 → v10 변경점**: v9 요청으로 8개 런타임의 제안(report9)을 받아 **통합 6축(TrackHE9)을 완주·폐합**했다.
> **봉인 신규 module 0**(전 축). 성과:
> - ★**Gröbner/ℤ[ω] phase-ideal 제10 독립 검증경로**(P1): 대각 위상회로 U=diag(ω_M^{f(x)}) 를 **위상다항식
>   f 의 이데알 멤버십**(path A 게이트별 ℤ_M Möbius 누적 == path B golden Möbius, (f_A−f_B)∈⟨x_i²−x_i,M⟩ NF≡0)
>   으로 검증. ★**제9 ANF(GF(2) Boolean, 진폭무관, 순열회로만)의 맹점=대각 위상회로**를 상보 커버(커버집합
>   상보, 교집합=skip). genuine Buchberger(S-poly→0 인증). **심화**: monomial 비대각 U|x⟩=ω^f|π(x)⟩(CNOT+phase,
>   A≠I)까지 확장 = ANF·P1 둘 다 skip 하는 교집합 맹점 커버, **non-coprime LT parity 소거**(genuine 회로-이데알).
> - **contextual fraction LP 정량화**(P2): Peres-Mermin 정성 parity(v8 P5)→**정량 승격**, 내장 exact-rational LP
>   (외부 solver 무의존)로 강한 맥락성 NCF=0→**CF=1 exact 유리수**·CF(visibility v)=v 선형·dual parity certificate.
> - **|C|≥2 고차 Chern**(P3): spin-S multi-Weyl(spin-1 3-band·spin-3/2 4-band), 최저밴드 **C_lowest=2S·C_½(m)=
>   ±2·±3**, exact 정수공식 == FHS 격자 numerics(진짜 multi-band). 2D QWZ(|C|≤1, v8 P3)의 질적 확장.
> - **A₄ ζ₃-필연 선검증**(P4, ★사람게이트 대기): B₃(ζ-free)·S₄(closed-neg)·Q₈(ζ-free)의 **상보** = A₄(12원소)는
>   **문자표 자체가 ζ₃ 강제**. 핵심=**ℚ*에 order-3 원소 없음**(x³=1,x∈ℚ⟹x=1)→3-cycle 비자명 1차원 지표
>   rational 불가→ω=ζ₃ 필연. NOT rational group(3-cycle 두 클래스 분열)·orthogonality(ω). ω₃ 승인 시 봉인.
> - **code switching**(P5): Steane[[7,1,3]]↔[[8,3,2]] 를 **closed-negative**(논리차원 2≠8→logical-bijection 부존재,
>   매장만·거리 3≠2)로 반증 → **redirect** Steane↔**RM15[[15,1,3]]**(k=1 일치) **positive 실증**: switch W†W=I₂·
>   X̄/Z̄ intertwine, ★Steane 횡단 Clifford + RM15 횡단 T → **{Clifford,T} 보편 횡단 게이트셋**(registry 자산이
>   FTQC 고리로 맞물림).
> - **Ising 애니온 융합**(P6): σ×σ=1+ψ·d_σ=√2·비보편 Clifford·θ_σ=e^{iπ/8}, Fibonacci(d_τ=φ·보편) **상보**=
>   두 정준 애니온 모델 · **qutrit Gross 이산 Wigner**(P6): stabilizer W≥0 vs magic W<0(Strange −1/3·Norrell −1/6)
>   =이산 Hudson 방향, 맥락성/magic phase-space 렌즈.
> - (report9 대기 중 **cyclic-BCH CSS [[15,7,3]]·distance-5 [[31,11,5]] Tier-2 봉인**도 완료 — §3 EXCLUDE 반영.)
> §3m 에 추가. §4′에 v10 신규 패턴 4(★**crux-probe 우선·closed-negative→redirect→positive·non-coprime 소거·
> 사람게이트 필연성 선증명**).

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
- ★**Tier-0 dense 실질 상한 ≈ 12큐빗**(2^12). 그 이상 Clifford 는 **Tier-2 정준 tableau**(dense 미실체화)로,
  비-Clifford 대형은 **관측(witness)** 또는 structural 로 — 제안 시 봉인 경로를 명시하라(§4′i).

## 3. EXCLUDE — 이미 구현·봉인된 것 (재제안 금지)

현재 **95 modules / 457 sealed apps** (root `f6f1f0fcc0e2ff28…`). **독립 검증경로 10개**
(dense · tableau · ZX · path-sum ℤ[ω₈] · stabilizer-rank · matchgate/SO(2n) · tensor-network · QMDD ·
ANF/bit-vector · **Gröbner/ℤ[ω] phase-ideal**).

### 3a~3k. v1~v7 소비분 (요약 — 상세는 이전 라운드 EXCLUDE 계보)
- **기초/QFT/QPE/Grover/Trotter·Suzuki/VQE·QAOA/쿼리(DJ·BV·Simon)/walk** · **QEC**(repetition·Steane
  Tier-2·Shor-9·transversal Clifford·**[[25,1,9]] 연접**·RM[[15,1,3]]) · **Shor**(15·21·distinct-prime frontier
  shor69…219·cmul factory) · **QSVT 완비** · **Fermionic**(JW/BK/parity·fSWAP·Bogoliubov Pfaffian) · **분자 H₂·
  qROM·[[5,1,3]] 증류·S₃/D₄/S₄/Q₈ 비아벨 Fourier+HSP·큐트릿 산술** · **위상 논리연산([[4,2,2]])·MBQC·Z₂ gauge·
  Schur-Weyl·AKLT·CPTP 채널·1q Clifford 2/3-design·PEPS·MUB-20·UD-POVM·flag·GF(8)·Fibonacci/Majorana braid·
  C₃ phase-poly·RS·[[8,3,2]] 횡단 CCZ** · **동역학**(dual-unitary·Floquet·OTOC·매듭 fig8/TL₃) · **자원**(magic
  ξ/robustness·채널 magic Choi) · **검증경로 1~8**(dense·tableau·ZX·path-sum·stab-rank·matchgate·tensor·QMDD).

### 3l. v8 소비분 (TrackHE8)
- **ANF/bit-vector 제9 검증경로** · **B₃ 초팔면체군 ζ-free**(rational group) · **HGP qLDPC [[27,4,3]] Tier-2** ·
  **2D QWZ Chern 정수 위상**(mass-sign==FHS) · **non-Pauli 유니터리 채널 diamond**(AKN arc) · **Peres-Mermin 맥락성**.

### 3m. ★v9 소비분 — 통합 6축 (TrackHE9, 이번 라운드 신규 — 재제안 금지)
- **Gröbner/ℤ[ω] phase-ideal 제10 검증경로(P1)**: `groebner_verify`+`groebner_monomial_observe` — 대각/monomial
  위상회로를 위상다항식 이데알 멤버십(ℤ_M NF≡0)으로. ★ANF(GF(2) Boolean 순열)의 **커버집합 상보**(대각 위상 vs
  순열). genuine (non-coprime LT parity 소거) Buchberger. (**제11 경로·회로 동치 SMT·H-포함 위상회로 완전 elimination·
  ℤ[ω] Galois 작용 검증은 아직 없음.**)
- **contextual fraction LP 정량화(P2)**: `contextual_fraction_observe` — 내장 exact-rational LP 로 CF=1·CF(v)=v·
  dual parity. (**Kochen-Specker 18-vector·큐트릿 KS·상태의존 맥락성·negativity monotone 정량은 아직 없음.**)
- **|C|≥2 고차 Chern(P3)**: `chern_higher_observe` — spin-S multi-Weyl, C_lowest=2S·C_½ (±2,±3), exact==FHS.
  (**3D 위상(ℤ/ℤ₂ 4밴드)·Floquet SPT 정수불변량·mirror/spin Chern·비-abelian Berry(2밴드 겹침)는 아직 없음.**)
- **A₄ ζ₃-필연 선검증(P4, 봉인 보류)**: `a4_observe` — ℚ*에 order-3 부재→ω=ζ₃ 강제, NOT rational group.
  ★**z3_gate(ω₃) 승인 시 A₄ Fourier 봉인**(선검증·근거 완료). (**A₅/PSL(2,7) 등 더 큰 비-rational·모듈러 표현은 아직 없음.**)
- **code switching(P5)**: `code_switch_observe`(closed-negative Steane↔[[8,3,2]] 논리차원 2≠8) + `code_switch_rm15_observe`
  (Steane↔RM15 positive, W†W=I₂·intertwine·Clifford+T 보편완성). (**실제 FT 전환 프로토콜(측정/게이지고정·gauge-fixing)·
  d≥5 부호쌍 switching·lattice surgery 는 아직 없음.**)
- **Ising 애니온 융합(P6)**: `ising_fusion_observe` — σ×σ=1+ψ·d_σ=√2·비보편 Clifford·Fibonacci(φ·보편) 상보.
  (**braid 유니터리 회로 봉인·완전 MTC(pentagon/hexagon 전체)·Ising⊗Ising·Chern-Simons level-k·비-abelian 융합 규칙 검증은 아직 없음.**)
- **qutrit Gross 이산 Wigner(P6)**: `qutrit_wigner_observe` — A_0=parity·frame 전수·stabilizer W≥0 vs magic W<0.
  (**qudit(d≥5) Wigner·連續변수 Wigner·negativity monotone·mana(magic 정량)·이산 Hudson 완전 증명은 아직 없음.**)

### 3j. 예비 판정분 (재제안 시 보강 조건)
- **BCH/RS 복호기**·**Hecke 브레이드**·**정수 나눗셈**·**큐딧 심플렉틱**·**2D DU SPT** — 각 저합의; 구체 인스턴스·
  오라클 경로·복리 접점 강화 시 재평가. (cyclic-BCH [[15,7,3]]·[[31,11,5]] CSS 인코더는 **이미 봉인** — 재제안 금지.)
- **제11 검증경로**: 기존 10 경로(특히 ANF·Gröbner)와 **전제 상이 한 문장 증명** 필수. 외부 solver 무의존 내장 결정론 엔진 보장 시 환영.

**핵심: 사소한 변형 금지. 질적 새 계층. 괄호 "아직 없음"이 관문이면 환영.**

## 4. 우리가 원하는 것 (방향 감 — 강요 아님)

- **검증 메타** — **제11 경로**(10 경로와 전제 상이 증명)·회로 동치 증명서·H-포함 위상회로 완전 elimination·treewidth 부분수축.
- **부호 심화** — code switching **FT 전환 프로토콜**(gauge-fixing)·d≥5 HGP/color·lattice surgery·부호쌍 switching.
- **표현론 심화** — A₄/A₅ ζ₃·ζ₅ Fourier(승인 시)·Hecke 대수·모듈러 표현·G(m,1,n) monomial.
- **동역학 심화** — Floquet SPT **정수** 불변량·3D 위상(ℤ/ℤ₂)·비-abelian Berry·2D dual-unitary.
- **자원 이론 심화** — Kochen-Specker 18-vector·qudit Wigner negativity monotone·mana·상태의존 맥락성.
- **애니온/TQC 심화** — 완전 MTC(pentagon/hexagon)·braid 유니터리 봉인·Chern-Simons level-k·비-abelian 융합 검증.
- 그 밖에 **당신이 더 나은 축을 알면 제안하라.**

## 4′. ★성공 패턴 (v1→v10)

**(a) 게이트 우회** · **(b) 직접 닫힌형 구성**(탐색 금지) · **(c) 승인-module 사람게이트**(닫힌형 각도·surd 우대) ·
**(d) 반증→회수·자유도 재도출·sub-app 복리** · **(e) 기소비 선점 대조·교차 복리·인프라 즉시 소비** ·
**(f) 다중 독립 경로 대조·Tier-2 드라이버·오라클 동치 재발견** · **(g) 봉인 전 선검증 반증·Choi/동형 재해석** ·
**(h) 제8/제9/제10 경로·closed-negative 의 상보 positive·연접 정리 구조·계산기저 함수 대수·rational group 판정·
Tier-2 로 dense 회피** ·

**(i) ★v10 신규 패턴 4개**:
- **crux-probe 우선(함정 회피)**: 제10 경로는 "순열회로에선 Gröbner=ANF 로 붕괴(ANF-in-disguise)"를 crux probe 로
  먼저 확인한 뒤 **정확히 ANF 맹점(대각/monomial 위상회로)**을 타깃했다. 검증경로/witness 제안 시 **기존 경로와
  진짜 겹치지 않는 최소 반례를 먼저 제시**하라(distinctness probe).
- **closed-negative → redirect → positive**: Steane↔[[8,3,2]] 는 논리차원 불일치로 **ill-formed 반증**됐고, 그
  반증이 **올바른 타깃(Steane↔RM15, k 일치)**을 가리켰으며 그것을 positive 로 실증했다. 반증 자체가 1급 산출이며,
  **반증이 지시하는 올바른 타깃까지 제시**하면 최상.
- **non-coprime LT 소거(genuine Buchberger)**: monomial 위상회로의 parity 변수 p=(x_c⊕x_t) 소거는 {p−L,p²−p}
  선행항 공유(non-coprime)로 nontrivial S-poly 를 만든다(대각의 전-coprime x_i²=자명과 대조). 대수 검증 제안 시
  **진짜 소거가 일어나는 곳**을 명시하라.
- **사람게이트 필연성 선증명**: A₄ 는 봉인 전에 "ℚ*에 order-3 원소 없음 → ζ₃ 필연"을 exact 증명해 **ω₃ 승인의
  결정근거**를 제공했다. 승인 module 이 필요하면 **왜 그 무리수/cyclotomic 이 원리적으로 불가피한지** 먼저 증명하라.

## 5. 반드시 지켜야 할 제약

- **결정론 불가침**·**오라클은 사용만**·**honest decomposition**(MatrixGate 금지)·**self-contained**·**하드웨어 out**.
- **정직 경계** — 근사·확률·측정후처리는 **관측**. exact ≠ 근사, dense ≠ structural ≠ subspace ≠ tableau.
  봉인 ≠ 관측(certificate/witness 는 봉인 자산 아님). **근사 truncation 은 봉인 아님**.
- **★registry 실측 novelty**: 공개 저장소 **https://github.com/sadpig70/QuantaFoundry**
  (`registry/`·`specs/`·`scripts/` 공개) — 접근 가능하면 실측 대조 우대. 불가하면 §3 정독 + 구조적 novelty.

## 6. 답변 형식 (제안마다)

**3~5개**를 impact×feasibility 순: 1. **proposal**(축+구체 인스턴스) · 2. **rationale**(정체성·compounding·
교차 복리) · 3. **feasibility**(봉인 게이트·오라클 검증·§4′(b) exact 근거·**봉인 경로 명시**: Tier-0 dense(n≲12)
/Tier-2 tableau/관측 — §4′(i)) · 4. **risk**(정직 경계) · 5. **novelty**(§3 특히 **3m/3l/3j** 대조 + 시차 강건성).

## 7. 개념 미니 용어집

- **봉인/compounding/honest boundary/teeth/subspace 강검증/Tier-2/closed-negative/rational group/crux-probe** — 이전 라운드 정의 유지.
- **검증경로 10**: dense·tableau·ZX·path-sum ℤ[ω₈]·stabilizer-rank·matchgate/SO(2n)·tensor-network·QMDD·
  ANF/bit-vector(계산기저 Boolean, 진폭 무관)·**Gröbner/ℤ[ω] phase-ideal**(대각/monomial 위상다항식 이데알 멤버십) — 제11 을 환영한다.
