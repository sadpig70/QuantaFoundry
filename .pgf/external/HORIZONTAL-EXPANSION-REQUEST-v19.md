<!-- QuantaFoundry 수평 확장 아이디어 제안 요청 — v19 (2026-07-24). v1~v18 후속. self-contained. -->
<!-- 외부 모델 런타임에게 전달용. 이 문서 하나만 읽고 제안 가능하도록 작성됨. -->

# QuantaFoundry — 수평적 확장(Horizontal Expansion) 아이디어 제안 요청 · v19

> **v18 → v19 변경점**: v18 요청으로 8 agent 제안(report18)을 받아 **7 headline 완주·폐합**(TrackHE18).
> 전 축 **관측/certificate**(seal root 불변·신규 module 0). 성과(§3w):
> - ★★**P1 BMW₃ 2변수 Kauffman/Dubrovnik D(a,z) 완전 종결**(v16~v18 3라운드 crux): 해법=추상 Markov
>   trace 가 아니라 **표현론적 우회** — U_q(sl₂) spin-1(=so₃)/so₄=sl₂×sl₂ universal R-matrix +
>   **ribbon pivotal quantum trace(Markov 자동)**. 두 특수화선(N=3 a=Q²·N=4 a=Q³)+a-span 한계로
>   **D(4₁)=a²z²+a²−az³−az−2z²−1+z³/a+z/a+z²/a²+a⁻² 유일 복원**, ★복원에 안 쓴 2독립 불변량(Jones
>   특수화=t⁻²−t⁻¹+1−t+t²·Dubrovnik amphichirality D(a,z)=D(a⁻¹,−z))이 정확 확증. 트랙 최초 완전 2변수.
> - ★★**D^ω(D₄) 완전 22×22 twisted S·T + U(1) 완전 census**(P2): 관례 전부 기계확정(slant θ_a 결합법칙
>   64³ 전수·모듈 κ 공리·Verlinde 22³ 비음정수·S 유니터리·S²=C·(ST)³∝S²)·★**Bockstein lift 사다리**
>   (μ₂→μ₄→μ₈=U(1) 전체)로 **전 twist 에서 anyon 수 22 고정** ⟹ **"22→19→16 ω-가변"(v17 P4·report17/18)
>   완전 반증** — 진짜 가변 지표는 **T-스펙트럼 ζ₄→ζ₈→ζ₁₆**(P=2,6 에서 ζ₁₆ spins 필요 발견).
> - ★**D^ω(ℤ₂⁵) radical parity 일반 정리**: radical parity = n mod 2(commutator form 은 **군 ℤ₂ⁿ 위
>   n×n** alternating — Λ³ 혼동 반증)·n=5 → radical{1,3,5}·**radical=1 존재**(최대 비아벨화).
> - ★★**A₇ Brauer tree·D·Cartan 완결(p=5,7)**(P3): ★**문자표 완전 자체유도**(Dixon: GF(421) 중심문자→
>   cyclotomic lift·문헌 인용 0)·p=7 **라인 1—6—15—(10,10̄)ₑₓ꜀**(m=2·simples{1,5,10}·det C=7)·p=5
>   **라인 1—14′—21—14—6**(simples{1,13,8,6}·det C=5) — 판정=GF(p) 결정적 선형대수(trace·고정공간·Hom).
> - ★**ε-인증 E8**(P4): **Pauli-covariant 채널 exact diamond 폐형식** ‖Φ_p−Φ_q‖◇=Σ|Δp_P|(Choi 차
>   Bell-대각·primal=dual·SDP-free·유리수) — **비유니터리 최초 exact**(E7 unitary 한정 해소).
> - ★★**SU(3)₂ MTC — 첫 rank-2 Lie 준위**(P5): Kac-Peterson(ℚ(ζ₁₅) 정확 산술)·★C=(3↔3̄,6↔6̄) 비자명·
>   dims{1×3,φ×3}·D²=3(2+φ)·★**SU(3)₂ ≅ conj-Fib(h_τ=3/5)⊠ℤ₃^{(q=2)}**(S·T 동시 정확 매칭).
> §3w 에 추가. §4′에 v19 신규 패턴 4(★표현론적 우회·Bockstein 사다리·확률적 meataxe 함정·cyclotomic
> 직접 산술). ★외부 수치 정정 4건: agent08 Λ³-혼동·22/19/16 ω-가변·depolarizing diamond 'p'(정확 3p/2)·
> SU(3)₂ field 'ℚ(ζ₅)'(정확 ℚ(ζ₁₅)).

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
  분해 존재를 먼저 증명하고 근사면 ε-인증(**E1–E8 계약**: 상한 E1–E4·op-norm 하계 E5·diamond 하계 E6·
  diamond exact(unitary) E7·★diamond exact(Pauli 채널) E8) 경로를 명시하라.
  **modular data(조합적 exact 표)는 이 경계 무관**(D(S₃)/D^ω(D₄)/SU(3)₂ 선례).

## 3. EXCLUDE — 이미 구현·봉인·관측된 것 (재제안 금지)

현재 **95 modules / 1431 sealed apps** (root `556d5e97322affa0…`). ★**Shor frontier N≤1023 완결**(10-bit 전 구간). **독립 검증경로 10개**
(dense·tableau·ZX·path-sum ℤ[ζ_{2^t}]·stabilizer-rank·matchgate/SO(2n)·tensor-network·QMDD·ANF/bit-vector·
Gröbner/ℤ[ω] phase-ideal) **+ 제11 후보 6건 전부 강등/불채택**. ★진짜 제11 독립경로 **미발견**(공개과제 유지).

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

### 3s~3t. v14~v15 소비분 (요약 — 재제안 금지)
- v14: D(D₄)/D(Q₈) 쌍 대조·HOMFLY Hecke·D^ω(ℤ₂²) H³ 전수·2D DIII+FK ℤ₈·H²(A₅) cocycle(Q₈)·
  gridsynth 실봉인(_ct+_rs, ε 1e-5)·pathsum ring-exact.
- v15: D^ω(ℤ₂³) type-III·D^ω(S₃) 최초 비아벨 twist·BMW₂/T(2,k)·H²(A₆) Schur(Q₈→Q₁₆)·
  AZ 2D C 2ℤ/CI 0/3D DIII ℤ·ε 하계 E5.

### 3u~3v. v16~v17 소비분 (요약 — 재제안 금지)
- v16: twisted 비아벨 double(D^ω(D₄)/D^ω(Q₈) H³ 비대칭)·ℤ₂⁴ 완전비아벨화 반증(radical≥2)·Q₃₂ tower 반증·
  BMW₃ fig-8 Jones(1변수)·E6 diamond 하계·AZ 3D AII ℤ₂/AIII ℤ.
- v17: AZ 2D AII(QSH)+CII 3D+조대화 그래프·E7 exact Watrous diamond(unitary)·D^ω(D₄) anyon-count 층화·
  D^ω(ℤ₂⁴) radical∈{2,4} parity·A₇ Brauer 수/Sylow/defect-0.

### 3w. ★v18 소비분 — 7 headline (TrackHE18, 이번 라운드 신규 — 재제안 금지)
- ★★**BMW₃/Kauffman 2변수 완전 종결**: `bmw3_kauffman_so3/so4/2var_observe` — quantum trace(Markov 자동)·
  SO(3)/SO(4) 특수화선·**D(4₁)(a,z) 유일 복원+2독립 확증**(Jones·Dubrovnik amphichirality). crux 폐합.
  (**다른 매듭(5₁/5₂/6₁)의 2변수·Links-Gould sl(2|1)·BMW₄+·HOMFLY-Kauffman 비포함 증명은 아직 없음.**)
- ★★**D^ω(D₄) 완전 22×22 twisted S·T + U(1) census**: `dtw_d4_full_modular_observe`·`dtw_d4_u1_census_observe` —
  기계확정 관례·Verlinde 전수·**Bockstein μ₂→μ₄→μ₈ 사다리로 U(1) 전체 anyon 22 고정**(22/19/16 반증)·
  **T-스펙트럼 ζ₄→ζ₈→ζ₁₆ 이 진짜 twist 지표**. (**ζ₁₆ spins(P=2,6)의 완전 twisted S·T 실현·twisted D^ω(Q₈)
  대비·비아벨 G 의 U(1)-클래스 개별 라벨링은 아직 없음.**)
- ★**D^ω(ℤ₂⁵) radical parity 정리**: `dtw_z2_5_radical_parity_observe` — radical parity=n mod 2·
  radical=1 존재(사영 irrep 차원 4). (**radical=1 층 완전 twisted S(ℤ₂⁵ 96+ anyons)·n=6,7 일반화는 아직 없음.**)
- ★★**A₇ Brauer tree·D·Cartan(p=5,7)**: `a7_brauer_trees_observe` — Dixon 문자표 완전 자체유도·양 트리
  유일 확정·det C=p. (**p=2,3 비순환 defect(D₄·ℤ₃²)의 D·C·3.A₇ ζ₃ cover·다른 Aₙ/Sₙ Brauer tree 는 아직 없음.**)
- ★**ε-인증 E8(Pauli 채널 exact diamond)**: `pauli_diamond_e8_observe` — ‖Φ_p−Φ_q‖◇=Σ|Δp|(Bell-대각·
  SDP-free). (**일반 CPTP exact(비-Pauli)·d>2 Pauli(qudit Weyl-Heisenberg 채널)·adaptive/멀티라운드 판별은 아직 없음.**)
- ★★**SU(3)₂ MTC(첫 rank-2 Lie)**: `su3_2_mtc_observe` — Kac-Peterson ℚ(ζ₁₅)·비자명 C·
  **≅conj-Fib⊠ℤ₃^{(q=2)}**(S·T 동시). (**SU(3)₃+(비-pointed 분해 없는 진짜 rank-2)·G₂ level 1(Fib 단독?)·
  Witt 군 층위 MTC 비교·F/R-symbol 범주 동치는 아직 없음.**)
- **surface code d=3 [[9,1,3]] 물리층**(v17 잔여): `surface_code_d3_observe` — distance-3 전수·merge=논리측정.
  (**twist-defect/dislocation(5-body stab·e↔m)·d=5 min-weight·lattice surgery Tier-2 실봉인은 아직 없음.**)

### 3j. 예비 판정분 (재제안 시 보강 조건)
- **Floquet SPT 정수불변량**·**정수 나눗셈**·**큐딧 심플렉틱**·**negativity/mana monotone**·**Spekkens 준비
  맥락성**·**twist defect / color-code surgery**·**QSVT arb 함수 구간인증**·**BDI 3D(AIII 와의 구별 판정 선행)**
  — 구체 인스턴스·오라클·복리 강화 시 재평가.
- ★**진짜 제11 검증경로(공개과제)**: 10 경로 + 강등 6건과 **검증 객체가 상이한 새 수학 대상**.
  "전체 unitary 동치를 조합/대수 불변량으로 판정"하는 구성이 아직 없다. 자가강등/정직표기가 채택 조건.

**핵심: 사소한 변형 금지. 질적 새 계층. 괄호 "아직 없음"이 관문이면 환영.**

## 4. 우리가 원하는 것 (방향 감 — 강요 아님)

- **검증 메타** — ★진짜 제11 경로(공개과제)·비-2^t 혼합 환·ε 하계 자동 전파·합성 T-count 하한 전파.
- **매듭/양자군 심화** — ★2변수 D(a,z)를 **다른 3-braid 매듭(5₁/5₂/6₁)** 으로(방법 확보됨: 다중 N quantum
  trace + a-span 한계 + 독립 특수화 확증)·Links-Gould sl(2|1)(4×4 R-matrix·supertrace)·BMW₄·so₅=sp₄ 곡선.
- **애니온/TQC 심화** — ★ζ₁₆ spins 층(P=2,6)의 완전 twisted S·T·D^ω(ℤ₂⁵) radical=1 층 완전 S·
  SU(3)₃/G₂ 준위·Witt 군 층위·MS probe(|G|=55).
- **표현론 심화** — ★p=2,3 비순환 defect 의 D·C(A₇)·3.A₇/Valentiner ζ₃(사람게이트)·다른 Aₙ Brauer tree·
  Dixon 기계 재사용(다른 유한군 문자표 자체유도).
- **채널 인증 심화** — ★E8 을 **qudit Weyl-Heisenberg 채널**(d 소수)로·일반 covariant 채널 폐형식·
  E-사다리 자동 적용 게이트.
- **QEC 심화** — twist-defect/dislocation surface code(5-body stabilizer·e↔m 교환) Tier-2 실봉인·
  lattice surgery 물리 패치 Tier-2·d=5 distance 인증.
- 그 밖에 **당신이 더 나은 축을 알면 제안하라.**

## 4′. ★성공 패턴 (v1→v19)

**(a) 게이트 우회** · **(b) 직접 닫힌형 구성** · **(c) 승인-module 사람게이트** · **(d) 반증→회수·복리** ·
**(e) 기소비 선점 대조·교차 복리** · **(f) 다중 독립 경로·Tier-2 드라이버** · **(g) 봉인 전 선검증 반증** ·
**(h) closed-negative 상보 positive** · **(i) crux-probe 우선·redirect** · **(j) 선검증이 외부 제안 정정** ·
**(k) FS 지표 판별** · **(l) FS 삼분·state-independent KS·완전 modularity** · **(m) 유한군 vs Lie MTC 양대
원천·외부 수치 자기모순 검출** · **(n) 쌍/궤도 대조=검증객체·부분해제=존재구성+ε-sidecar** ·
**(o) 외부 수치 자체 재유도가 실제 오류 검출** · **(p) parity 정리 격상·조대화 그래프·자체유도 defect** ·
**(q) closed-negative 과도확장 포착·인증 계층 심화·분류 열 완결**.

**(r) ★v19 신규 패턴 4개**:
- **★표현론적 우회(quantum trace)**: 3라운드 미해결이던 BMW₃ Markov trace crux 를 추상 대수 관례
  (cyclicity-solve)가 아니라 **구체 표현(universal R-matrix)+ribbon pivotal quantum trace(Markov 자동)**
  로 해결했다. ⟹ 추상 대수 구조가 "관례 미확정"으로 막히면, **그 대수를 표현하는 구체 양자군 표현**을
  지어 불변량을 직접 계산하라 — 관례가 표현에서 자동 결정된다. 복수 표현(다중 N)의 특수화선 + 유한
  a-span + **복원에 쓰지 않은 독립 불변량 확증**이 완결 패턴.
- **★Bockstein lift 사다리 = U(1) 완전 census**: H³(G,U(1)) 전 클래스는 |G|-torsion(transfer) → μ₂→μ₄→μ₈
  사다리(각 단계 GF(2) 장애 판정·lift 코셋 전사)로 **유한 계산이 U(1) 전체를 커버**한다. "계수 제한" 정직
  경계를 사다리로 해소·과도확장 주장(anyon 가변)을 **전 계수에서** 반증. 코호몰로지 제안은 계수 사다리
  전략을 명시하라.
- **★확률적 meataxe 함정**: uniserial 모듈의 socle 은 랜덤 spin 이 찾지 못해 "simple" 오판을 낳는다
  (pairs-perm(21) mod 5 실사례). 모듈러 표현 판정은 **정확 선형대수**(trace·고정공간 dim·Hom(S,Q)/Hom(Q,S)
  rank)로 — 2-layer 구조는 Hom 양방향이 결정적으로 갈라낸다.
- **★cyclotomic 직접 산술**: sympy simplify 는 ζ₁₅ 급에서 지수폭발한다. Φ_n 기저의 **Fraction 계수 벡터
  직접 구현**(mul 테이블·conj·역원=선형계)이 견고경로 — ℤ[ζ₈](D^ω(D₄) 22×22 Verlinde)·ℚ(ζ₁₅)(SU(3)₂)
  실증. 수백 원소 행렬 게이트도 초 단위.

## 5. 반드시 지켜야 할 제약

- **결정론 불가침**·**오라클은 사용만**·**honest decomposition**(MatrixGate 금지·opaque KAK-fitted float 금지)·
  **self-contained**·**하드웨어 out**.
- **정직 경계** — 근사·확률·측정후처리는 **관측**. exact ≠ 근사, dense ≠ structural ≠ subspace ≠ tableau.
  봉인 ≠ 관측. ★ε-인증은 **E1–E8 계약**(상한+하계+exact(unitary)+★exact(Pauli 채널) — 각 계층 정직 경계 명시).
- **★registry 실측 novelty + 제안값 자체 재검증(v19 강화)**: 공개 저장소 **https://github.com/sadpig70/QuantaFoundry**.
  ★**제안의 구체 좌표/문자표/필드/양자차원/코호몰로지 차원/anyon 수/radical/Sylow/diamond 값은 스스로 독립
  재검증** — 상충·오류 실재 목록(v19 신규 4건 추가): KS-18·A₅ ζ₅·Yu-Oh·Conway-31·SU(2)₄ D²=8·SU(2)₅ D² factor-2·
  ℤ₂⁴ 완전 비아벨화·Q₃₂ tower·**agent08 Λ³-혼동(radical parity)**·**"anyon 22→19→16 ω-가변"(→U(1) 전체에서
  22 고정으로 완전 반증)**·**depolarizing diamond 'p'(정확 3p/2)**·**SU(3)₂ field 'ℚ(ζ₅)'(정확 ℚ(ζ₁₅))**.
  ⟹ ★특히: **조건부 계산(Schur collapse "만약 β nontrivial 이면")을 무조건부 결론으로 요약하지 말 것** —
  실제 slant/cocycle 유도까지 해야 주장이 된다(v17 P4 자기정정 사례).

## 6. 답변 형식 (제안마다)

**3~5개**를 impact×feasibility 순: 1. **proposal**(축+구체 인스턴스) · 2. **rationale**(정체성·compounding·
교차 복리) · 3. **feasibility**(봉인 게이트·오라클 검증·**봉인 경로 명시**: Tier-0 dense/Tier-2/관측/
certificate/ε-sidecar) · 4. **risk**(정직 경계·자체 재유도 계획·**과도확장 상한 선재유도**) ·
5. **novelty**(§3 특히 **3w/3v/3j** 대조 + 시차 강건성).

## 7. 개념 미니 용어집

- **봉인/compounding/honest boundary/teeth/Tier-2/closed-negative/crux-probe/FS 삼분/certificate layer** — 유지.
- **검증경로 10 + 제11 후보 6건(전부 강등/불채택)**: dense·tableau·ZX·path-sum·stabilizer-rank·matchgate·
  tensor-network·QMDD·ANF·Gröbner. ★진짜 제11 미발견.
- **ε-인증 E1–E8 계약(v19 갱신)**: E1–E4 상한 + E5 op-norm 하계 + E6 diamond 하계 + E7 diamond exact
  (unitary·Watrous 2√(1−ν²)) + ★**E8 diamond exact(Pauli-covariant 채널·Σ|Δp|·SDP-free)**.
- **quantum trace(신규)**: ribbon pivotal μ 의 tr_q(x)=Tr(x·μ^{⊗n}) — Markov 성질 자동. 매듭 불변량은
  cyclicity-solve 없이 표현에서 직접.
- **Bockstein 사다리(신규)**: μ₂→μ₄→μ₈ lift 장애 판정으로 H³(G,U(1)) 전 클래스를 유한 커버.
- **twist 판별(v19 갱신)**: 스핀(T-스펙트럼 ζ₄→ζ₈→ζ₁₆)·융합환·사영표현 차원·섹터 선택성·centralizer
  H²(μ₂). ★anyon **수**는 불변일 수 있다(D₄ 전 twist 22 고정) — 수 가변 주장은 slant 유도까지 자체 검증.
- **MTC 인수분해(신규)**: pointed 부분군(d=1 sectors) 발견 → S·T 동시 텐서 분해 확인(SU(3)₂≅Fib̄⊠ℤ₃ 선례).
  rank-2 준위 제안은 pointed 분해 여부를 먼저 판정하라.
