<!-- QuantaFoundry 수평 확장 아이디어 제안 요청 — v17 (2026-07-22). v1~v16 후속. self-contained. -->
<!-- 외부 모델 런타임에게 전달용. 이 문서 하나만 읽고 제안 가능하도록 작성됨. -->

# QuantaFoundry — 수평적 확장(Horizontal Expansion) 아이디어 제안 요청 · v17

> **v16 → v17 변경점**: v16 요청으로 8개 런타임의 제안(report16)을 받아 **통합 6축(TrackHE16)을
> 완전 소진·폐합**했다. 전 축 **관측/certificate**(seal root 불변). 성과(§3u):
> - **twisted 비아벨 double D^ω(D₄)/D^ω(Q₈)**(P1): untwisted D(D₄)≅D(Q₈)(v14 동일 22 anyon·D²=64)를
>   **twist 가 구별**한다 — dim H³(D₄,μ₂)=4(|16|) vs H³(Q₈,μ₂)=1(|2|), 자원 비대칭. 구조근원=D₄ 의
>   **ℤ₂² centralizer 섹터 → 사영 2차원 irrep(차원전이 2섹터)** vs Q₈ 전부 ℤ₄ 순환→차원전이 0. 차원전이
>   판정=centralizer H²(μ₂)·2-rank(cocycle 무관). ★정직: 완전 22×22 S·ζ₈ 스핀 미착수(ℚ(i) 밖).
> - **D^ω(ℤ₂⁴) 완전 비아벨화 — closed-negative**(P2): report16 제안 'radical=0 완전 비아벨화'를 **반증**.
>   type-III slant commutator rank ≤ 2 전수(15 삼중항×15 a) → radical ≥ 2 → 완전(d=4) 불가. ★코호몰로지
>   계수군 함정 재검출: dim H³(ℤ₂⁴,μ₂)=**20**(𝔽₂ degree-3, C(6,3)) ≠ 제안 'ℤ₂¹⁴'(U(1)). positive=최대
>   twist 88 anyon·D²=256.
> - **2.A₇ Sylow tower Q₃₂ — closed-negative**(P6): 제안 'Sylow-2 tower Q₈→Q₁₆→Q₃₂'를 **반증**. Aₙ Sylow-2
>   위수=|Aₙ| 2-part 자체유도: A₅=4·A₆=8·**A₇=8(A₆와 동일 D₄)**·A₈=64 → 2.A₇ Sylow-2 ≅ 2.A₆ = **Q₁₆**,
>   Q₃₂ 아님. 실제 tower Q₈→Q₁₆→Q₁₆(정체). (Q₃₂ 는 A₈ 층에서.)
> - **BMW₃(dim 15) 3-braid figure-8**(P3): v15 BMW₂/T(2,k) 토러스족을 **3-braid 로 확장**. ★fig-8(4₁)=3-braid
>   (σ₁σ₂⁻¹)² 폐포 = 트랙 **최초 비-토러스·amphichiral 매듭**(토러스는 전부 chiral→불가). BMW₃ dim=15
>   자체유도 + 부호정확 Kauffman bracket 으로 폐포 Jones V(4₁)=t⁻²−t⁻¹+1−t+t²·amphichirality V(t)=V(1/t)·
>   det=5. ★정직: **Jones(1변수)까지** — 2변수 Kauffman F via BMW₃ Markov trace 는 미착수.
> - ★**ε 하계 diamond-norm 인증 E6**(P4): E5(op-norm 하계)를 **채널 수준**으로 확장. 유니터리 채널쌍
>   Φ_U,Φ_R 의 최대얽힘(Choi) 입력 트레이스거리 D_lo=2√(1−|Tr(U†R)|²/d²) ≤ ‖Φ_U−Φ_R‖_◇ (sup 중 한
>   입력=엄밀 하계·global-phase 불변·E5 mpmath U·R 재사용). 양측 bracket [D_lo,2ε]·Trotter 8종 채널
>   비-exact. ★독립검증: D_lo ≤ exact Watrous 고유위상값 ≤ 2ε. ★E6≠exact Watrous 값·유니터리 채널 한정.
> - **AZ 3D 열 완결 — AII(ℤ₂ 강한 TI)·AIII(ℤ)**(P5): v15 3D DIII(ℤ)에 잔여 2칸 추가. ★AII 3D=**ℤ₂ 강한
>   위상절연체**(Fu-Kane parity (−1)^ν₀=Π_{8TRIM} sign(M)·정수 부호산술·강한 TI m∈(1,3)∪(−3,−1))·AIII
>   3D=**ℤ chiral winding**. ★핵심=DIII/AII 둘 다 T²=−1인데 PHS 유무로 **ℤ↔ℤ₂** 且 **ℤ₂=DIII winding
>   mod 2**(PHS 제거 조대화). genuine=단열 gap 논증(TRIM 소멸 섭동→닫힌형 정확 불변). float Berry 금지.
> §3u 에 추가. §4′에 v17 신규 패턴 3(★**closed-negative 가 과도확장 제안 포착·인증 계약 계층적 심화
> E5→E6·분류 열 완결+조대화 관계**). 동기간 frontier: shor{N} 자율봉인 893~959
> (FrontierClosureA: N≤1023 완결 후 폐합 정책 — 잔여 ~16개, 임박).

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
  분해 존재를 먼저 증명하고 근사면 ε-인증(★이제 **상한+하계 구간** — E5 op-norm·E6 diamond-norm) 경로를 명시하라.
  **modular data(조합적 exact 표)는 이 경계 무관**(D(S₃)/D^ω(S₃)/D(D₄)/D(Q₈)/D^ω(D₄) 선례).

## 3. EXCLUDE — 이미 구현·봉인·관측된 것 (재제안 금지)

현재 **95 modules / 1361 sealed apps** (root `0bb516a76f4feebc…`). **독립 검증경로 10개**
(dense·tableau·ZX·path-sum ℤ[ζ_{2^t}]·stabilizer-rank·matchgate/SO(2n)·tensor-network·QMDD·ANF/bit-vector·
Gröbner/ℤ[ω] phase-ideal) **+ 제11 후보 6건 전부 강등/불채택**(Galois-orbit·treewidth·표현환 K(G)·Matsumoto-Amano·
symplectic phase-space·ANF+Gröbner 결합). ★진짜 제11 독립경로 **미발견**(공개과제 유지).

### 3a~3m. v1~v9 소비분 (요약)
- **기초/QFT/QPE/Grover/Trotter·VQE·QAOA/쿼리/walk** · **QEC**(repetition·Steane·Shor-9·transversal Clifford·
  연접[[25,1,9]]·RM[[15,1,3]]·HGP[[27,4,3]]·cyclic BCH[[15,7,3]]/[[31,11,5]]) · **Shor**(15·21·frontier…959·factory) ·
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
- **매듭/TQC 심화** — ★**2변수 Kauffman F via BMW₃ Markov trace**·다른 3-braid 매듭·Links-Gould·매듭 불변량 계보 확장.
- **동역학/SPT 심화** — 2D AII(QSH ℤ₂)·CII 3D 2ℤ·Floquet SPT·비-abelian Berry·interacting 분류 일반·weak index 세분.
- 그 밖에 **당신이 더 나은 축을 알면 제안하라.**

## 4′. ★성공 패턴 (v1→v17)

**(a) 게이트 우회** · **(b) 직접 닫힌형 구성** · **(c) 승인-module 사람게이트** · **(d) 반증→회수·복리** ·
**(e) 기소비 선점 대조·교차 복리** · **(f) 다중 독립 경로·Tier-2 드라이버** · **(g) 봉인 전 선검증 반증** ·
**(h) closed-negative 상보 positive·rational group 판정** · **(i) crux-probe 우선·redirect** ·
**(j) 선검증이 외부 제안 정정·certificate layer 정직 강등** · **(k) FS 지표 판별·제11 공개과제** ·
**(l) FS 삼분 완성·state-independent KS·완전 modularity** · **(m) 유한군 vs Lie MTC 양대 원천·외부 수치
자기모순 검출** · **(n) 쌍/궤도 대조=검증객체·융합환 전이=twist 판별·ring shadow 정수 축약·부분해제=존재구성+ε-sidecar** ·
**(o) 외부 수치 자체 재유도가 실제 오류 검출·teeth 무력 실측 후 대상 교체·상한→구간 양방향 인증**.

**(p) ★v17 신규 패턴 3개**:
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
  **상한+하계 구간**(tightness 무주장·직교 sidecar — Trotter/gridsynth 2가족·E1–E6 계약: op-norm 상·하계 + diamond 하계).
- **★registry 실측 novelty + 제안값 자체 재검증(v17 강화)**: 공개 저장소 **https://github.com/sadpig70/QuantaFoundry**.
  ★**제안의 구체 좌표/문자표/필드/FS지표/양자차원/코호몰로지 차원/anyon 수/radical rank/Sylow 위수는 스스로 독립
  재검증**(외부 제안·런타임 간 상충·과도확장 반복 실재: KS-18·A₅ ζ₅·Yu-Oh·treewidth·Conway-31·SU(2)₄ D²=8·
  D^ω(ℤ₂³) 22 vs 64·H²(S₃) 계수군·**ℤ₂⁴ 완전 비아벨화**·**Q₃₂ tower**). 불가하면 §3 정독 + 구조적 novelty.

## 6. 답변 형식 (제안마다)

**3~5개**를 impact×feasibility 순: 1. **proposal**(축+구체 인스턴스) · 2. **rationale**(정체성·compounding·
교차 복리) · 3. **feasibility**(봉인 게이트·오라클 검증·§4′(b) exact·**봉인 경로 명시**: Tier-0 dense/Tier-2/관측/
certificate/ε-sidecar) · 4. **risk**(정직 경계·certificate/봉인 구분·자체 재유도 계획·**과도확장 상한 선재유도**) ·
5. **novelty**(§3 특히 **3u/3t/3j** 대조 + 시차 강건성).

## 7. 개념 미니 용어집

- **봉인/compounding/honest boundary/teeth/Tier-2/closed-negative/rational group/crux-probe/ambivalent/
  Frobenius-Schur 삼분/certificate layer** — 유지.
- **검증경로 10 + 제11 후보 6건(전부 강등/불채택)**: dense·tableau·ZX·path-sum ℤ[ζ_{2^t}]·stabilizer-rank·
  matchgate·tensor-network·QMDD·ANF·Gröbner + 강등 6건. ★진짜 제11 미발견.
- **ε-인증 2가족·E1–E6 계약(v17 갱신)**: Trotter/Suzuki(교환자 상한) + gridsynth(위상정렬 등식) — E1–E4
  상한 + ★**E5 op-norm 하계**(mpmath Taylor expm rigorous → 구간 [ε_lo,ε_hi]) + ★**E6 diamond-norm 하계**
  (채널 수준 D_lo=2√(1−|Tr(U†R)|²/d²)=Choi 입력 트레이스거리, 양측 bracket [D_lo,2ε]). 봉인은 항상 "그 회로의
  unitary" exact.
- **ring shadow**: 회로 엔트리의 정수환(ℤ[ω]/√2^m) 그림자 — exact 검증·심볼릭 축약·컬럼증인 바인딩 3중 사용.
- **twist 판별**: cocycle twist 는 스핀(T)·융합환·**사영표현 차원(비아벨화)**·**섹터 선택성**(D^ω(S₃) 전치 섹터)·
  **centralizer H²(μ₂) 2-rank**(D^ω(D₄) vs D^ω(Q₈) 차원전이)로 판별. MTC/double 비교 제안은 이 지표들을 보고하라.
- **AZ 조대화(신규)**: 대칭류 간 불변량군 관계 — PHS 제거 시 DIII(ℤ)→AII(ℤ₂)=winding mod 2. 분류표 제안은
  인접 칸 조대화/세분 관계를 함께 보고.
