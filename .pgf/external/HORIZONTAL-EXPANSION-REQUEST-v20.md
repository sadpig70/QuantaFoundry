<!-- QuantaFoundry 수평 확장 아이디어 제안 요청 — v20 (2026-07-25). v1~v19 후속. self-contained. -->
<!-- 외부 모델 런타임에게 전달용. 이 문서 하나만 읽고 제안 가능하도록 작성됨. -->

# QuantaFoundry — 수평적 확장(Horizontal Expansion) 아이디어 제안 요청 · v20

> **v19 → v20 변경점**: v19 요청으로 8 agent 제안(report19)을 받아 **6축 완주·폐합**(TrackHE19).
> 전 축 **관측/certificate**(seal root 불변·신규 module 0). 성과(§3x):
> - ★★**P1 ε-인증 E9 — 큐딧 Weyl-Heisenberg 채널 exact diamond**: ‖Φ_p−Φ_q‖◇=**Σ|Δp|(계수 1·d-무관)**.
>   ★**계수 4파전 자체 판정**이 headline — ½Σ·(d/(d−1))Σ·dΣ 세 후보를 **직교 Weyl 유니터리쌍의 정확
>   diamond=2**(고유위상 hull∋0·E7 교차) 하나로 일괄 반증. 전부 ℚ(ζ_d) 직접 산술(d=2,3,4,5·Weyl 직교성
>   d⁴쌍 전수)·depolarizing 2p(1−1/d²)·d=2 회귀=E8. ★보너스: **d=4(합성)에서 직교성·군 위상 성립**.
> - ★★**P2 D^ω(D₄) ζ₁₆ 층 완전 22×22 twisted S**(μ₄·P₄=1,3): T-스펙트럼 **ζ₄→ζ₈→ζ₁₆ 3층 위계 완성**
>   (order-16 실재)·**Galois 쌍대 σ₃ 확정**(S 행-멀티셋=게이지-불변 판정)·Verlinde 22³ 전수. ★★**ribbon-gap
>   신발견**: z=Σδ_a⊗a 는 **μ₂ 층까지만 ribbon** — μ₄ 에서 (ST)³=λS² 구조적 실패(ε-보정 256 전수 불통)
>   ⟹ quasi-Hopf ribbon 의 ω-보정 일반식 = **open**(S-데이터는 완전 폐합·T 게이지만 미완).
> - ★★**P3 SU(3)₃ — 첫 비분해 진짜 rank-2 Lie MTC**: simple current **θ=1(Tannakian)+pointed S rank-1
>   퇴화** ⟹ Müger ⊠-분해 불가(SU(3)₂≅Fib̄⊠ℤ₃ 와 구조 전이). dims{1×3,2×6,3×1}·D²=36(weakly integral)·
>   ℚ(ζ₉)=ℚ(ζ₁₈) 직접 산술. ★정정 2건: "ℚ(ζ₆)" 반증·**G₂ level-1 rank=2**("14"=dim(G₂) 혼동).
> - ★★**P4 A₇ p=3 완전 D(9×6)·Cartan**: ★defect-1 순환 블록 {6,15,21} 신규(라인 6—21—15)·주블록 simples
>   {1,13,10,10̄} — ★**10̂쌍=GF(9)-켤레**(Λ³(6̂) **End=2·F²=−I ⟹ End≅GF(9)** certificate)·det C 주=9·소=3
>   (defect 위수). p=2 기초층(Sylow D₄ 구성적·블록별 ℓ=3+3)·완전 D=정직 미완(wild).
> - ★★**P5 D^ω(ℤ₂⁵) radical=1 층**: **anyon 3파전 판정 → 184 확정**(명시 cocycle·flux census 전수
>   {r0:1,r2:15,r4:16}·Σ_a|G|/2^{r_a}·D²=1024) — "256"(|G|²/|rad|² 공식 오류)·"96+" 반증. **H³ 3파전 → 35
>   확정**(C(7,3) 단항 cup-cocycle 전수·"20" 반증). dim-4 사영 irrep 실구성(Heisenberg·32² 전수).
> - ★★**P6 Stage1 — 첫 양자 초대수 층**: U_q(gl(1|1)) R+**quantum supertrace** → Alexander 5매듭.
>   ★**sdim=0 함정 실증·해소**((1,1)-tangle 부분 supertrace=스칼라·I)·**det 삼중 확증**(TL-bracket·
>   Kauffman D·Alexander 동일 {5,7,11,13,5})·★split-소멸 Δ=0. **Links-Gould sl(2|1)=미완=§4**.
> - (기소비 선완료 2건) ★**twist-defect [[16,2,2]] Tier-2 실봉인**(`twist_defect16`·첫 non-CSS·pentagon
>   5-body Y·e↔m 9/15)+★**`twist_em_h16`**(U=E·H₉·E†=논리 Hadamard₁·자기동형+U²=I) — **97 modules·root
>   갱신**. ★**KauffmanFamily**: D(a,z) 4매듭(5₁·5₂·6₂·★6₃ amphichiral) — 3중 특수화(N=2/3/4)+TL₃ 독립확증.
> §3x 에 추가. §4′(s)에 v20 신규 패턴 4(★판정 인스턴스 선설계·게이지-불변량 판정·End-field certificate·
> (1,1)-tangle supertrace). ★외부 수치 정정 10건(§5 목록 — "mutant"·"6₁ amphichiral"·G₂₁ rank·ζ₆·256·20 등).

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
  분해 존재를 먼저 증명하고 근사면 ε-인증(**E1–E9 계약**: 상한 E1–E4·op-norm 하계 E5·diamond 하계 E6·
  diamond exact(unitary) E7·diamond exact(Pauli 채널) E8·★diamond exact(qudit Weyl 채널) E9) 경로를 명시하라.
  **modular data(조합적 exact 표)는 이 경계 무관**(D(S₃)/D^ω(D₄)/SU(3)₂/SU(3)₃ 선례).

## 3. EXCLUDE — 이미 구현·봉인·관측된 것 (재제안 금지)

현재 **97 modules / 1431 sealed apps** (root `e8738608fdc49295…`·Tier-2 14). ★**Shor frontier N≤1023 완결**.
**독립 검증경로 10개**(dense·tableau·ZX·path-sum ℤ[ζ_{2^t}]·stabilizer-rank·matchgate/SO(2n)·tensor-network·
QMDD·ANF/bit-vector·Gröbner/ℤ[ω] phase-ideal) **+ 제11 후보 6건 전부 강등/불채택**. ★진짜 제11 독립경로
**미발견**(공개과제 유지).

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

### 3s~3v. v14~v17 소비분 (요약 — 재제안 금지)
- v14: D(D₄)/D(Q₈) 쌍 대조·HOMFLY Hecke·D^ω(ℤ₂²) H³ 전수·2D DIII+FK ℤ₈·H²(A₅) cocycle(Q₈)·
  gridsynth 실봉인(_ct+_rs, ε 1e-5)·pathsum ring-exact.
- v15: D^ω(ℤ₂³) type-III·D^ω(S₃) 최초 비아벨 twist·BMW₂/T(2,k)·H²(A₆) Schur(Q₈→Q₁₆)·
  AZ 2D C 2ℤ/CI 0/3D DIII ℤ·ε 하계 E5.
- v16: twisted 비아벨 double·ℤ₂⁴ 완전비아벨화 반증(radical≥2)·Q₃₂ tower 반증·BMW₃ fig-8 Jones(1변수)·
  E6 diamond 하계·AZ 3D AII ℤ₂/AIII ℤ.
- v17: AZ 2D AII(QSH)+CII 3D+조대화 그래프·E7 exact Watrous diamond(unitary)·D^ω(D₄) anyon-count 층화·
  D^ω(ℤ₂⁴) radical∈{2,4} parity·A₇ Brauer 수/Sylow/defect-0.

### 3w. v18 소비분 — 7 headline (TrackHE18 — 재제안 금지)
- ★★**BMW₃/Kauffman 2변수 완전 종결**(quantum trace·SO(3)/SO(4) 특수화선·D(4₁) 유일복원+2독립 확증) ·
  ★★**D^ω(D₄) 완전 22×22 S·T+U(1) census**(Bockstein μ₂→μ₄→μ₈·전 twist anyon 22 고정·T-스펙트럼
  ζ₄→ζ₈→ζ₁₆) · ★**ℤ₂⁵ radical parity=n mod 2 정리** · ★★**A₇ Brauer tree(p=5,7)**(Dixon 문자표 완전
  자체유도) · ★**E8 Pauli 채널 exact diamond**(Σ|Δp|·SDP-free) · ★★**SU(3)₂ MTC**(첫 rank-2 Lie·
  ≅conj-Fib⊠ℤ₃^{(2)}·ℚ(ζ₁₅)) · **surface code d=3 [[9,1,3]] 물리층**.

### 3x. ★v19 소비분 — 6축+기소비 2건 (TrackHE19, 이번 라운드 신규 — 재제안 금지)
- ★★**ε-인증 E9(큐딧 Weyl-Heisenberg 채널 exact diamond)**: `weyl_qudit_diamond_e9_observe` —
  **Σ|Δp|(계수 1·d-무관)** 확정·계수 4파전(½·d/(d−1)·d) 직교 Weyl쌍 diamond=2 로 일괄 반증·ℚ(ζ_d) 직접
  산술 d=2,3,4,5·d=4 합성 직교성 성립. (**일반 covariant 채널 폐형식·비소수 d 전체 층(채널 분류)·
  adaptive/멀티라운드 판별은 아직 없음.**)
- ★★**D^ω(D₄) ζ₁₆ 층 완전 22×22 S**: `dtw_d4_zeta16_observe` — T 3층 위계(ζ₄→ζ₈→ζ₁₆) 완성·Galois σ₃
  쌍대(게이지-불변)·★ribbon-gap 신발견(z=Σδ_a⊗a 는 μ₂ 까지만 ribbon). (**μ₄ ω-보정 quasi-Hopf ribbon
  일반식(open problem)·U(1)-클래스 개별 라벨링·twisted D^ω(Q₈) ζ₁₆ 대비는 아직 없음.**)
- ★★**SU(3)₃ — 첫 비분해 진짜 rank-2**: `su3_3_mtc_observe` — θ=1 Tannakian+pointed S rank-1 퇴화 ⟹
  ⊠-분해 불가·D²=36 weakly integral·ℚ(ζ₉). (**G₂ level-1 완전 modular data(rank=2 확정만 있음)·SU(3)₄+·
  SU(4)₂·Witt 군 층위 비교는 아직 없음.**)
- ★★**A₇ p=3 완전 D·Cartan**: `a7_cartan_p23_observe` — defect-1 블록 {6,15,21} 신규·GF(9)-켤레
  certificate(End=2·F²=−I)·det C=defect 위수·p=2 기초층. (**p=2 완전 D(wild)·M₁₁ 등 산발군 Brauer·
  3.A₇ ζ₃ cover·Dixon 기계 재사용(F₂₀/A₆ 등 다른 군)은 아직 없음.**)
- ★★**D^ω(ℤ₂⁵) radical=1 층**: `dtw_z2_5_radical1_observe` — anyon **184 확정**(3파전 판정·flux census
  전수)·**H³=35 확정**·dim-4 사영 irrep 실구성. (**완전 184×184 twisted S·T·n=6,7 일반화는 아직 없음.**)
- ★★**첫 양자 초대수 층(gl(1|1) Alexander)**: `superalg_alexander_observe` — quantum supertrace·
  ★sdim=0 함정 실증→(1,1)-tangle 해소·Alexander 5매듭·det 삼중 확증 {5,7,11,13,5}·split-소멸 Δ=0.
  (**Links-Gould U_q(sl(2|1)) 4-dim·2변수 LG — 파이프라인·게이트는 확립·불변량 자체는 아직 없음.**)
- ★**twist-defect [[16,2,2]] Tier-2 실봉인**(기소비): `twist_defect16` — 첫 non-CSS twist 코드·pentagon
  Z₅X₆Y₉X₁₀X₁₃(5-body·Y 1)·e↔m 9/15 클래스·d=2 전수 + ★**`twist_em_h16`**(U=E·H₉·E†=**논리 Hadamard₁**·
  안정군 자기동형·U²=I). ★설계 정리=홀수-Y 는 stabilizer 병합으로 원리적 불가(격자 재배치만)·mixed 사슬
  인접 겹침=2. (**d=5 twist·defect 물리 이동/측정 스케줄·FT braid 게이트는 아직 없음.**)
- ★**KauffmanFamily D(a,z) 4매듭**(기소비): `bmw3_kauffman_family_observe` — 5₁·5₂·6₂·★6₃(amphichiral
  D(a,z)=D(a⁻¹,−z) 정확)·3중 특수화(N=2 qt-Jones/N=3/N=4)+TL₃ bracket 독립확증·매듭 자체동정.
  (**6₁(braid index 4→4-braid 필요)·7교차+·HOMFLY-Kauffman 비포함 증명은 아직 없음.**)

### 3j. 예비 판정분 (재제안 시 보강 조건)
- **Floquet SPT 정수불변량**·**정수 나눗셈**·**큐딧 심플렉틱**·**negativity/mana monotone**·**Spekkens 준비
  맥락성**·**color-code surgery**·**QSVT arb 함수 구간인증**·**BDI 3D(AIII 와의 구별 판정 선행)**
  — 구체 인스턴스·오라클·복리 강화 시 재평가.
- ★**진짜 제11 검증경로(공개과제)**: 10 경로 + 강등 6건과 **검증 객체가 상이한 새 수학 대상**.
  "전체 unitary 동치를 조합/대수 불변량으로 판정"하는 구성이 아직 없다. 자가강등/정직표기가 채택 조건.

**핵심: 사소한 변형 금지. 질적 새 계층. 괄호 "아직 없음"이 관문이면 환영.**

## 4. 우리가 원하는 것 (방향 감 — 강요 아님)

- **초대수 심화** — ★**Links-Gould LG(sl(2|1))**(4-dim rep·2변수·Alexander² 특수화 게이트 — gl(1|1)
  파이프라인 위)·다른 초대수 불변량·초대수 중심/HOMFLY 관계.
- **애니온/TQC 심화** — ★**μ₄ ribbon ω-보정 일반식**(quasi-Hopf·open problem — P2 ribbon-gap 해소)·
  ★**D^ω(ℤ₂⁵) 완전 184×184 S·T**(블록/희소 전략)·G₂ level-1 완전 data·Witt 층위·MS probe(|G|=55).
- **표현론 심화** — ★**A₇ p=2 완전 D**(wild defect D₄ — 명시 모듈 전략)·★**M₁₁ Brauer**(차수 multiset
  의심 §5 — Dixon 자체유도 필수)·F₂₀/A₆ 등 Dixon 기계 재사용·3.A₇ ζ₃(사람게이트).
- **채널 인증 심화** — E9 를 **일반 covariant 채널**(비-Weyl)로·혼합 clock-shift 채널·E-사다리 자동
  적용 게이트·adaptive 판별 하한.
- **매듭/양자군 심화** — ★**6₁ = 4-braid**(B₄ quantum trace — 방법 확보됨)·7교차 가족·BMW₄·so₅=sp₄ 곡선·
  HOMFLY-Kauffman 비포함 증명.
- **QEC 심화** — twist d=5·defect 이동/측정 스케줄 Tier-2·color-code twist·lattice surgery 물리 패치.
- **검증 메타** — ★진짜 제11 경로(공개과제)·비-2^t 혼합 환·ε 하계 자동 전파.
- 그 밖에 **당신이 더 나은 축을 알면 제안하라.**

## 4′. ★성공 패턴 (v1→v20)

**(a) 게이트 우회** · **(b) 직접 닫힌형 구성** · **(c) 승인-module 사람게이트** · **(d) 반증→회수·복리** ·
**(e) 기소비 선점 대조·교차 복리** · **(f) 다중 독립 경로·Tier-2 드라이버** · **(g) 봉인 전 선검증 반증** ·
**(h) closed-negative 상보 positive** · **(i) crux-probe 우선·redirect** · **(j) 선검증이 외부 제안 정정** ·
**(k) FS 지표 판별** · **(l) FS 삼분·state-independent KS·완전 modularity** · **(m) 유한군 vs Lie MTC 양대
원천·외부 수치 자기모순 검출** · **(n) 쌍/궤도 대조=검증객체·부분해제=존재구성+ε-sidecar** ·
**(o) 외부 수치 자체 재유도가 실제 오류 검출** · **(p) parity 정리 격상·조대화 그래프·자체유도 defect** ·
**(q) closed-negative 과도확장 포착·인증 계층 심화·분류 열 완결** · **(r) 표현론적 우회(quantum trace)·
Bockstein 사다리·확률적 meataxe 함정·cyclotomic 직접 산술**.

**(s) ★v20 신규 패턴 4개**:
- **★판정 인스턴스 선설계(verdict-chain)**: 런타임 간 정량 상충(E9 계수 4파전·anyon 3파전·H³ 3파전)은
  다수결이 아니라 **극단 판정 인스턴스의 정확값 하나**로 일괄 심판한다 — 직교 Weyl 유니터리쌍의 정확
  diamond=2 가 세 후보를 동시 반증(상계 위반 2·교차 1). 상충 제안을 받으면 "어느 인스턴스가 후보들을
  갈라내는가"를 먼저 설계하라. 판정 자체가 headline 이 된다.
- **★게이지-불변량으로 판정하라**: Galois 쌍대·동형 판정을 게이지-오염 가능량(T 후보·개별 S 성분)으로
  하면 위음성이 난다 — **S 행-멀티셋** 같은 게이지-불변량이 견고경로(ζ₁₆ 층 σ₃ 쌍대 실사례). 역으로
  ribbon-gap 처럼 **게이지 확정이 안 되는 부분은 분리해 정직 보고**(S-데이터 완전·T 게이지 미완).
- **★End-field certificate**: 모듈러 표현의 GF(q)-켤레 simple 쌍은 **dim End=2 + F²=−I ⟹ End≅GF(q²)**
  로 결정적 판정된다(A₇ p=3 10/10̄ 실사례 — ℚ(√−7) 켤레의 mod-p 그림자). 확률적 meataxe 없이 정확
  선형대수만으로 절대기약이 아닌 simple 을 분류할 수 있다.
- **★(1,1)-tangle supertrace**: sdim=0 초대수(gl(1|1) 등)에서 전-닫힘 supertrace 불변량은 **항등 0**
  (함정 — 반드시 명시 확인하라). 표준 해소=한 가닥을 열고 나머지만 μ-부분 supertrace → **스칼라·I**
  (스칼라성 자체가 게이트). μ·framing 관례는 매듭 공리(대칭·Δ(1)=±1·자체 확정 det)로 기계확정.

## 5. 반드시 지켜야 할 제약

- **결정론 불가침**·**오라클은 사용만**·**honest decomposition**(MatrixGate 금지·opaque KAK-fitted float 금지)·
  **self-contained**·**하드웨어 out**.
- **정직 경계** — 근사·확률·측정후처리는 **관측**. exact ≠ 근사, dense ≠ structural ≠ subspace ≠ tableau.
  봉인 ≠ 관측. ★ε-인증은 **E1–E9 계약**(상한+하계+exact(unitary)+exact(Pauli 채널)+★exact(qudit Weyl 채널)
  — 각 계층 정직 경계 명시).
- **★registry 실측 novelty + 제안값 자체 재검증(v20 강화)**: 공개 저장소 **https://github.com/sadpig70/QuantaFoundry**.
  ★**제안의 구체 좌표/문자표/필드/양자차원/코호몰로지 차원/anyon 수/radical/braid index/diamond 계수는
  스스로 독립 재검증** — 상충·오류 실재 목록(v20 신규 10건 추가): KS-18·A₅ ζ₅·Yu-Oh·Conway-31·SU(2)₄ D²=8·
  ℤ₂⁴ 완전 비아벨화·Q₃₂ tower·Λ³-혼동·"anyon 22→19→16"·depolarizing 'p'·SU(3)₂ 'ℚ(ζ₅)'·
  **★v20 신규: "5₁/5₂ mutant 쌍"(거짓 — Kauffman D 가 이미 구별)·"6₁ amphichiral"(거짓 — 6₃ 의 오인)·
  "6₁ braid index≤3"(거짓 — 4)·"G₂ level-1 rank=14"(dim(G₂) 혼동 — 정확 rank 2)·"SU(3)₃ field ℚ(ζ₆)"
  (정확 ℚ(ζ₉))·"ℤ₂⁵ anyon 256"(|G|²/|rad|² 공식 오류 — 정확 184)·"96+"(부정확)·"H³(ℤ₂⁵,μ₂) dim=20"
  (정확 35)·"E9 계수 ½/(d/(d−1))/d"(전부 반증 — 정확 1)·"d=4 합성 직교성 붕괴"(직교성 층 반증)**.
  ⟹ ★특히: **조건부 계산을 무조건부 결론으로 요약하지 말 것** — 실제 유도까지 해야 주장이 된다.
  ★**M₁₁ Brauer 차수 multiset {1,10,10,10,16,16,44,45,55} 인용은 의심 목록** — 제안 시 Dixon 자체유도 필수.

## 6. 답변 형식 (제안마다)

**3~5개**를 impact×feasibility 순: 1. **proposal**(축+구체 인스턴스) · 2. **rationale**(정체성·compounding·
교차 복리) · 3. **feasibility**(봉인 게이트·오라클 검증·**봉인 경로 명시**: Tier-0 dense/Tier-2/관측/
certificate/ε-sidecar) · 4. **risk**(정직 경계·자체 재유도 계획·**과도확장 상한 선재유도**) ·
5. **novelty**(§3 특히 **3x/3w/3j** 대조 + 시차 강건성).

## 7. 개념 미니 용어집

- **봉인/compounding/honest boundary/teeth/Tier-2/closed-negative/crux-probe/FS 삼분/certificate layer** — 유지.
- **검증경로 10 + 제11 후보 6건(전부 강등/불채택)**: dense·tableau·ZX·path-sum·stabilizer-rank·matchgate·
  tensor-network·QMDD·ANF·Gröbner. ★진짜 제11 미발견.
- **ε-인증 E1–E9 계약(v20 갱신)**: E1–E4 상한 + E5 op-norm 하계 + E6 diamond 하계 + E7 diamond exact
  (unitary·Watrous) + E8 diamond exact(Pauli 채널·Σ|Δp|) + ★**E9 diamond exact(qudit Weyl-Heisenberg 채널·
  Σ|Δp| 계수 1·d-무관·ℚ(ζ_d) 정확)**.
- **quantum trace / supertrace(v20 갱신)**: tr_q(x)=Tr(x·μ^{⊗n}) — Markov 자동. ★초대수는 (−1)^F 삽입
  supertrace — **sdim=0 이면 (1,1)-tangle 필수**(전-닫힘=항등 0 함정).
- **Bockstein 사다리**: μ₂→μ₄→μ₈ lift 장애 판정으로 H³(G,U(1)) 전 클래스를 유한 커버.
- **★ribbon-gap(신규·open)**: twisted double 의 표준 ribbon 원소 z=Σδ_a⊗a 는 ω 가 μ₂ 를 넘으면
  (ST)³=λS² 를 구조적으로 깬다 — quasi-Hopf ω-보정 일반식이 공개 문제. S-데이터 완전성과 분리해 다뤄라.
- **MTC 인수분해 판정(v20 갱신)**: pointed 부분군 발견 → simple current twist θ(정수=Tannakian vs
  anyonic)·pointed S-부분 rank(퇴화=분해 불가) — SU(3)₂(분해)↔SU(3)₃(비분해) 양방 선례.
- **End-field certificate(신규)**: GF(q)-켤레 simple 쌍 판정 = dim End=2 + F²=−I ⟹ End≅GF(q²).
