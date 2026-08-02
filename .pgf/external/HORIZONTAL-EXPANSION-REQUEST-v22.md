<!-- QuantaFoundry 수평 확장 아이디어 제안 요청 — v22 (2026-08-06). v1~v21 후속. self-contained. -->
<!-- 외부 모델 런타임에게 전달용. 이 문서 하나만 읽고 제안 가능하도록 작성됨. -->

# QuantaFoundry — 수평적 확장(Horizontal Expansion) 아이디어 제안 요청 · v22

> **v21 → v22 변경점**: v21 §4 의 "**A₆·A₇ 모듈 구조 심화 — Loewy 층·사영 분해가능 모듈·Ext¹ 퀴버**"
> 후보를 **자율 라운드 8 사이클(2026-07-28 ~ 08-05)로 완주**했다. 전 건 **관측**(seal root
> `e8738608…` 불변·신규 module 0). ★**이번 라운드의 성격**: 하나의 대상(유한군 블록 대수)을
> **한 층씩 끝까지** 밀어 올려 **4 블록을 완전히 적어냈다** — D·Cartan → Ext¹ 퀴버 → Loewy 급수 →
> 기본대수 → 관계식 → Ext². 그리고 마지막 두 사이클은 **새 대상이 아니라 커버리지의 빈 칸**을 채웠다.
> 성과 요약(§3z):
> - ★★**4 블록 완전 제시 `B ≅ kQ/I`** — 블록 차원(232·432·2088·279)을 **다루지 않고**
>   **기본대수 `A = ⊕Hom_G(P_i,P_j)`**(34·18·19·36)만으로. `dim Hom(P_i,P_j) = C_{ij}` 이므로
>   **Cartan 이 곧 크기**다.
> - ★★**퀴버 동형인데 대수 비동형**: A₆ p=2 주와 A₇ p=2 비주는 **퀴버·관계식 개수·타입·Ext² 가 전부
>   같은데** 가환관계의 **차수만 8 vs 4** 이고 그것이 dim 34 vs 18 을 만든다 ⟹ **Ext¹ 퀴버만으로는
>   블록 대수가 결정되지 않는다**(실례).
> - ★★**제시를 막는 이유가 두 종류이고 서로 독립**: ①**자기고리**(A₇ p=2 주 — 분해체인데도
>   **균질 제시가 존재하지 않는다**; 리프트 32 **전수**로 부재 확인; 정체는 **γ² = 길이-4 경로**)
>   ②**비분해체**(A₆ p=3 — `End(6̃)=GF(9)` 라 𝔽₃ 위에서는 **퀴버 자체가 성립하지 않고**(species)
>   GF(9) 로 올라가야 4 정점 8 화살이 나온다).
> - ★★**규모를 구조로 환원**(두 번 재사용): 큰 체 가군의 **소체 밑가군이 이미 가진 소체 가군의 직합**
>   이면 `Hom_큰체(A,B) = {φ ∈ Hom_소체 : φ∘J_A = J_B∘φ}` 를 **소체 Hom 텐서 조립 + J-가환 하나**로
>   얻는다 — **dim 5184 계 16 쌍이 0.1 초**(PIM), 같은 수법이 **Ω¹ 에도 그대로** 통해 4608 계를 회피.
> - ★**세 sidecar 교차검증 43 게이트**: 종합을 **요약표가 아니라 검증기**로 만들었다 —
>   Cartan 3-way(퀴버 sidecar = Hom 차원 = dim_P 역산) · Ext¹ 3-way(퀴버 = rad/rad² = 화살) ·
>   Loewy 2-sidecar · dim A = ΣC · Ext² 총합 = 관계식 수.
> - ★**커버리지 행렬 빈 칸 0**: 무엇이 **몇 독립 경로**로 확인됐는지를 표로 적고 **빈 칸도 적었더니**,
>   그 빈 칸이 **다음 두 사이클의 목표를 그대로 지정**했다(H¹ 3/9 → 9/9 · head Ω² 3·3′ → 4 행).
> - ★**우리가 틀린 것 3건을 그대로 보고**: (a) "전부 회문" 예측 반증(P(14̂)만 비회문·비-rigid)
>   (b) `γ²=0` 예측 반증(실제 γ² = 길이-4 경로) (c) ★**GF(2) 전용 표현(XOR·집합)을 p=3 에 재사용해
>   관계식 18개(오답)** — **독립 제2 경로(descent)와의 불일치가 잡아냈고** 10개로 정정.
>
> §3z 에 추가. §4 를 **이 트랙이 남긴 열린 질문 3개**로 갱신. §4‴ 에 **재사용 자산 4종**.
> §4′(u) 에 v22 신규 패턴 4개.

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

### 3y. ★v21 소비분 — TrackHE20 8건 (이번 라운드 신규 — 재제안 금지)

- **G2Level1Fib** — (G₂)₁ 완전 modular data + **Fib 동형 판정**. 일반 level-k Lie 엔진(Cartan+d 만)·
  dims(1,φ)·D²=2+φ·c=14/5·h_τ=2/5·**Gauss 합 c mod 8 exact**·인증서 (d_τ,θ_τ)=(φ,ζ₅²)⟹**Fib 확정**·
  **Galois 4-궤도**·**SU(2)₃=anti-semion⊠(G₂)₁**·**(F₄)₁=σ₄((G₂)₁)**. 69/69.
- **Mu4RibbonClosure** — μ₄ ribbon-gap **폐합**. ★**ω-보정 불필요**(z=Σδ_a⊗a 정확) — 진범=S 켤레 규약.
  결함=(ST)³(S²)⁻¹=**C 순열**·3중 독립 심판(SL(2,ℤ)·balancing formA·**Gauss 합**)·**S̄=S∘C**·
  μ₂ 층은 C=항등이라 무해. **v20 §4·§7 의 "ribbon-gap open problem" 은 이로써 철회**. 40/40.
- **Z25FullModular** — D^ω(ℤ₂⁵) **완전 184×184 S·T**. 구조 환원(χ=d·μ·[∈R_a])·**유도표현 명시 구성으로
  공식 검증**(사영관계 1024쌍)·**Verlinde 184³ 전수**·C=항등·**c≡0 mod 8**·**Rep(ℤ₂⁵) Tannakian**. 32/32.
- **A7CartanP2** — A₇ p=2 **완전 D(9×6)·Cartan**. **A₇⊂GL(4,2) 자체 구성**·6 simple 명시·**기약성 전수**·
  Brauer 표(위수 7만 무리 α)·**C(주) det 8=|A₇|₂·C(비주) det 4·det C=32**·게이지=4̂↔4̄̂ 열교환. 40/40.
- **DixonF20A6** — **일반 Dixon 엔진 승격**(A₇ 재현 교차검증)·F₂₀ **첫 비아벨 Frobenius** p=5/p=2 완전 D·C
  (det=|G|_p)·A₆ 무리성 (1±√5)/2·**엄밀 𝔭-환원 블록**·★**A₆ p=5 Brauer tree 1—9—[8,8]^exc**. 58/58.
- **A6CartanP23** — A₆ p=2·3 **완전 D(7×5)·Cartan**. simples p=2 {1,4_a,4_b,8,8}(★**두 4차원=외부
  자기동형 쌍**·dual 쌍 아님)·p=3 {1,4,3,3′,9}(**Λ²4 End≅GF(9)**)·**det C=8·9=|A₆|_p**·
  ★**defect-0 d=1 을 대수적 정수성으로 검증**. 46/46.
- ⚠️**TwistD5Design / TwistD5Lattice** — twist d=5 **봉인 미달성(2회 연속·그대로 기록)**. 얻은 것 =
  회전 surface code 빌더+**MITM 거리 인증기**·**타입 GF(2) 아핀 연립**(홀수-Y 자동 보장)·
  **region-flip 무해 정리(16/16)**·**병합 상한 정리(4416/4416)**·★**계수 장벽**(면 n−1 고정 ⟹ 병합2→k=3
  ⟹ twist 논리 ≤⌊m/2⌋ ⟹ **d=5 는 m≥10**)·**6×5 전수 음성**. 대형 격자 음성은 **전수 아님**(예산 제한).

### 3j. 예비 판정분 (재제안 시 보강 조건)
- **Floquet SPT 정수불변량**·**정수 나눗셈**·**큐딧 심플렉틱**·**negativity/mana monotone**·**Spekkens 준비
  맥락성**·**color-code surgery**·**QSVT arb 함수 구간인증**·**BDI 3D(AIII 와의 구별 판정 선행)**
  — 구체 인스턴스·오라클·복리 강화 시 재평가.
- ★**진짜 제11 검증경로(공개과제)**: 10 경로 + 강등 6건과 **검증 객체가 상이한 새 수학 대상**.
  "전체 unitary 동치를 조합/대수 불변량으로 판정"하는 구성이 아직 없다. 자가강등/정직표기가 채택 조건.

**핵심: 사소한 변형 금지. 질적 새 계층. 괄호 "아직 없음"이 관문이면 환영.**


### 3z. ★유한군 블록 대수 완전 제시 (TrackQuiver, 2026-07-28 ~ 08-05 · 8 사이클)

**대상**: `A₆`(360)·`A₇`(2520) 의 modular 블록 4개. 전부 **관측**(봉인 아님)·신규 module 0·
root `e8738608fdc49295` 불변. sidecar = `.pgf/proofs/{EXT1-QUIVER,LOEWY-SERIES,QUIVER-RELATIONS,
BLOCK-ALGEBRA-SYNTHESIS}.json`.

| 블록 | 체 | 정점 | 화살 | dim A | LL | 관계식 | 제시 |
|---|---|---|---|---|---|---|---|
| A₆ p=2 주 | 𝔽₂ (이 블록의 분해체) | 3 | 4 | 34 | 9 | 3 | 균질 |
| A₇ p=2 비주 | 𝔽₂ (분해체) | 3 | 4 | 18 | 5 | 3 | 균질 |
| A₇ p=2 주 | 𝔽₂ (분해체) | 3 | 5 | 19 | 5 | 6 | ★비균질 강제 |
| A₆ p=3 주 | ★𝔽₃ 는 분해체가 아니다 → GF(9) | 4 | 8 | 36 | 5 | 10 | ★미결(전수 불가) |

**독립 경로 수**(커버리지 행렬 — 빈 칸 0):

| 블록 | Cartan | Ext¹ | Loewy | Ext² |
|---|---|---|---|---|
| A₆ p=2 주 | 3 | 3 | 2 | 3 |
| A₇ p=2 비주 | 3 | 3 | 2 | 3 |
| A₇ p=2 주 | 3 | 4 | 2 | 3 |
| A₆ p=3 주 | 3 | 3 | 2 | 3 |

**방법(자체유도 · 외부 문헌 행렬 인용 없음)**:
1. **기본대수만 다룬다** — `dim Hom_G(P_i,P_j) = [P_j : S_i] = C_{ij}` ⟹ `dim A = ΣC_{ij}`.
   곱셈은 **준동형의 합성**(실물 행렬곱). 블록 차원 2088 대신 19.
2. **PIM 은 지수 크기 운반자에서** — `|H|` 가 `p` 와 서로소면 `k[G/H]` 는 사영이고,
   **Frobenius 상호율 `m_S = dim S^H`** 로 성분을 **먼저 예측**한 뒤 **Hecke 대수
   `End_G(k[G/H]) ≅ X^H`** 의 멱등원으로 분해한다(`Σ_S m_S·dim P(S) = [G:H]` 가 게이트).
3. **화살 = rad/rad² 기저** · `rad A ∩ Hom(P_i,P_j) = {φ : im φ ⊆ rad P_j}`(i≠j 는 Nakayama).
4. **관계식은 리프트 의존** — 화살은 `rad²` 를 법으로만 정해진다. **개수(= dim Ext²)만 불변량**이므로
   `kQ/J^N` 안에서 `I` 와 `J·I + I·J` 를 직접 계산하는 **리프트-무관 최소생성**을 따로 만들었다.
5. **Ext² 는 세 경로** — `head(Ω²)`(★화살이 곧 syzygy 의 사영 덮개 사상) ·
   `H¹(G, Hom(ΩS_i,S_j))`(상한/하한 협공) · 리프트-무관 최소생성.

**★기계 대조용 요약**(이 블록은 `block_algebra_synthesis_observe` 가 sidecar 와 **자동 대조**한다 —
숫자를 손으로 고치면 게이트가 깨진다):

<!-- MACHINE-CHECKED: block-algebra-summary -->
```json
{
  "A6_p2_principal": {"block_dim": 232, "cartan": [[8, 4, 4], [4, 3, 2], [4, 2, 3]], "dim_P": [40, 24, 24], "dim_basic_algebra": 34, "dims": [1, 4, 4], "ext2": [[1, 0, 0], [0, 1, 0], [0, 0, 1]], "graded": [3, 4, 4, 4, 4, 4, 4, 4, 3], "homogeneous": true, "loewy_length": 9, "n_arrows": 4, "n_relations": 3, "quiver": [[0, 1, 1], [1, 0, 0], [1, 0, 0]], "simples": ["1̂", "4ₐ", "4_b"]},
  "A7_p2_nonprincipal": {"block_dim": 432, "cartan": [[2, 1, 2], [1, 2, 2], [2, 2, 4]], "dim_P": [24, 24, 40], "dim_basic_algebra": 18, "dims": [4, 4, 6], "ext2": [[1, 0, 0], [0, 1, 0], [0, 0, 1]], "graded": [3, 4, 4, 4, 3], "homogeneous": true, "loewy_length": 5, "n_arrows": 4, "n_relations": 3, "quiver": [[0, 0, 1], [0, 0, 1], [1, 1, 0]], "simples": ["4̂", "4̄̂", "6̂"]},
  "A7_p2_principal": {"block_dim": 2088, "cartan": [[4, 2, 2], [2, 3, 1], [2, 1, 2]], "dim_P": [72, 64, 56], "dim_basic_algebra": 19, "dims": [1, 14, 20], "ext2": [[1, 1, 0], [1, 2, 0], [0, 0, 1]], "graded": [3, 5, 4, 4, 3], "homogeneous": false, "loewy_length": 5, "n_arrows": 5, "n_relations": 6, "quiver": [[0, 1, 1], [1, 1, 0], [1, 0, 0]], "simples": ["1̂", "14̂", "20̂"]},
  "A6_p3_principal": {"block_dim": 279, "cartan": [[5, 4, 1, 1], [4, 5, 2, 2], [1, 2, 2, 1], [1, 2, 1, 2]], "dim_P": [27, 36, 18, 18], "dim_basic_algebra": 36, "dims": [1, 4, 3, 3], "ext2": [[1, 0, 1, 1], [0, 3, 0, 0], [1, 0, 1, 0], [1, 0, 0, 1]], "graded": [4, 8, 12, 8, 4], "homogeneous": null, "loewy_length": 5, "n_arrows": 8, "n_relations": 10, "quiver": [[0, 2, 0, 0], [2, 0, 1, 1], [0, 1, 0, 0], [0, 1, 0, 0]], "simples": ["1̂", "4", "3", "3′"]}
}
```

**정직 경계**: 관계식의 **명시 형태**는 리프트 선택에 의존한다(개수만 불변). A₆ p=3 의 **균질 제시
존재 여부는 미결**(이중화살 블록의 리프트 공간이 `GL₂(GF(9))` 궤도라 **전수 불가** — 부재 주장은
전수로만 할 수 있다). 외부 분류표(dihedral/quaternion type 등)와의 대응·유도동등성은 **무주장**.
"자기고리 ⟹ 비균질"의 **기전도 무주장**(4 블록 관측일 뿐).

---

## 4. 우리가 원하는 것 (방향 감 — 강요 아님)

★**v21 §4 의 "A₆·A₇ 모듈 구조 심화"가 §3z 로 완주**됐다. **그 트랙이 남긴 열린 질문 3개가 최우선**이다.

- ★★**Q1. 자기고리 ⟹ 비균질 제시 부재는 필연인가?** 우리는 4 블록에서 **자기고리가 있는 블록에서만
  균질 제시가 깨진다**를 관측했고(A₇ p=2 주: 리프트 **32 전수**에서 전부 `dim kQ/I = 20 ≠ 19`),
  정체는 **γ² = 길이-4 경로**였다. 하지만 **기전은 주장하지 않았다**. 반례(자기고리가 있는데 균질)
  또는 기전(왜 자기고리가 비균질을 강제하는가)을 **작은 인스턴스로** 제시할 수 있는가?
- ★★**Q2. A₆ p=3 GF(9) 블록에 균질 제시가 존재하는가?** 우리는 **한 리프트에서 비균질**(차수 2·4 혼합)임을
  확인했지만, **이중화살 블록의 리프트 공간이 `GL₂(GF(9))` 궤도라 전수가 불가**해 **존재 여부를 미결**로
  남겼다. 전수 없이 존재/부재를 결정하는 **불변량**이 있는가?
- ★★**Q3. 네 블록 대수의 분류·유도동등성**: 우리는 외부 분류 인용 없이 `kQ/I` 를 적었다. 이 넷은
  알려진 분류표의 무엇에 해당하는가? 특히 **퀴버가 같은데 dim 34 vs 18** 인 두 블록은 **유도동등한가**?
  (우리 산출물만으로 판정 가능한 **계산 가능한 판별식**을 제시하면 최고다.)
- ★**다음 층 — Hochschild·안정 범주**: `HH^*(B)`·`Ω`-주기성·안정 Auslander-Reiten quiver 는
  **이미 가진 `kQ/I`(4개) 위에 바로 얹힌다**. 작은 인스턴스로 봉인/관측 가능한 축인가?
- ★**다른 군·다른 p 로 수평 확장**: sporadic(M₁₁ p=11 은 이미 tree 확보)·`SL(2,q)`·대칭군 `S_n` —
  **자기고리·이중화살·비분해체가 동시에** 나오는 최소 인스턴스가 있는가?
- ⚠️★**twist d=5 — 경로가 확정된 미완**(이월): cut 을 따라 **면 1개 추가 후 2회 병합** →
  k=2 유지 + bulk twist 2개. 격자 m≥10 필요. **실봉인이 목표**(root 갱신). 3회 미달성.
- ★**채널 인증 E10 후보** — E9 를 **일반 covariant 채널**(비-Weyl)로·E-사다리 자동 적용 게이트.
- ★**H³(ℤ₂⁵,μ₂) 35 클래스 전체 modular data** · **D^ω(D₄) μ₈ 층** · **Q₈ 완전 μ₄ 사다리**.
- ★**검증 메타** — 진짜 **제11 경로**(공개과제·후보 6건 전부 강등)·비-2^t 혼합 환·ε 하계 자동 전파.
- 그 밖에 **당신이 더 나은 축을 알면 제안하라.**


## 4″. ★재사용 자산 계약 (v21 신규 — 제안 시 이것들 위에 쌓아라)

이번 라운드가 만든 **일반 도구 4종**. 새 대상을 제안할 때 **이 위에 얹히는지**를 feasibility 에 밝혀라.

| 자산 | 입력 | 산출 | 위치 |
|---|---|---|---|
| **level-k Lie 엔진** | Cartan A·dᵢ·k **뿐** | 근계·dim𝔤·comark·h∨·적분가중치·Weyl·Gram·h_λ·c·Kac-Peterson S̃ | `g2_1_mtc_observe.LieLevel` |
| **`Cyc(N)` 정확 산술** | N | ℚ(ζ_N) 정확 벡터(**Φ_N 자체유도**)·Galois·√5 좌표 | `g2_1_mtc_observe.Cyc` |
| **일반 Dixon 엔진** | 생성원·점수·q(≡1 mod exp G) | 켤레류·문자표 다중도(+`table_in` → `Cyc` 정확표) | `dixon_f20_a6_observe.dixon` |
| **MITM 거리 인증기 · 타입 GF(2) 아핀 연립** | 안정군 / 면 집합 | weight≤4 논리 판정(n=77 즉시) / **홀수-Y 자동 보장** 타입 해 | `twist_d5_lattice_observe` |

★**모듈 간 재사용이 실제로 작동했다**: Dixon 엔진이 `Cyc` 를 쓰고, μ₄ ribbon 심판이 level-k Lie 엔진으로
SU(3)₁ 을 구성해 규약을 결정했다. **당신의 제안도 이 결합을 노려라.**

## 4‴. ★재사용 자산 계약 (v22 신규 — 제안 시 이것들 위에 쌓아라)

| 자산 | 입력 | 산출 | 위치 |
|---|---|---|---|
| **소체 밑가군 조립** | 소체 Hom 블록 · 텐서 중복도 · 두 J | 큰 체 `Hom_{GF(q²)}`(계수공간 ≤ 수십 차원) | `quiver_relations_observe.assemble_hom_j` |
| **리프트-무관 최소생성** | 절단 경로대수 · 화살 · (선택)스칼라 J | **비균질 포함** 최소 관계식 개수·대표원 | `…minimal_generators_filtered` |
| **탐욕 사영 덮개** | 가군 · PIM 목록 · (선택)미리 계산한 Hom | `Ω = ker(P₁ ↠ M)`·중복도 — **비분해체에서도 동작** | `…greedy_cover` |
| **p-일반 대형 Hom** | 두 작용 · 생성원 · p | kron 없이 **생성원별 순차 교차**로 `Hom_G` | `…hom_space_iter` / `hom_space_fast`(GF(2) 비트팩) |

★**스칼라를 생성원으로 넣는 트릭**: `GF(q²)`-가군을 `(소체 가군, J)`(J²=−1, G 와 가환)로 실현화하고
**J 를 `gens` 리스트에 그냥 추가**하면 `Hom_{GF(q²)}` = "J 와 가환하는 `Hom_소체`" 가 되어
**기존 파이프라인 전체를 새로 짜지 않고 재사용**한다(모든 차원이 2배 → ÷2).


## 4′. ★성공 패턴 (v1→v22)

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

**(t) ★v21 신규 패턴 4개**:
- **★결함의 *종류* 를 먼저 측정하라**: 게이트가 깨질 때 "무엇이 부족한가"를 추측하지 말고 **결함행렬의
  구조**(위상/대각인가, 순열인가)를 먼저 잰다. μ₄ ribbon 에서 (ST)³(S²)⁻¹ = **C(순열)** 임을 재고 나니
  선행 시도의 **ε-위상 보정 256 전수가 원리적으로 실패할 수밖에 없던 이유**가 즉시 나왔다 — 대각 보정은
  순열 결함을 만들 수 없다. 새 이론을 요청하기 전에 **규약 아티팩트 가능성을 배제**하라.
- **★심판은 대상을 쓰지 않는 것으로**: 수정 후보를 "게이트가 통과하는 쪽"으로 고르면 자기적합이다.
  반드시 **문제의 대상을 전혀 쓰지 않는 독립 심판**을 포함하라 — μ₄ 에서는 **Gauss 합 p₊=Σd²θ**(S 미사용)가
  결정적이었고, balancing 지표 규약은 **SU(3)₁(비자기쌍대)** 에서 결정했다. ★**자기쌍대 예제에서 규약을
  검증하면 blind** 다(Fib 에서는 form A/B 가 둘 다 통과 — 실제로 반대 결론을 냈다가 이 teeth 로 포착).
- **★"규모 유보"는 브루트포스 대신 구조 환원 먼저**: 184×184·Verlinde 184³ 이 **8초**에 끝났다. 병목은
  규모가 아니라 **표현**이었다(radical 위 스칼라화). 규모를 이유로 유보된 축을 보면 **대상 구조에서 오는
  환원**(중심/radical/등방 부분군/궤도 분해)을 먼저 찾고, 그 환원 공식은 **가정하지 말고 명시 구성으로
  검증**하라(유도표현 사영관계 전수).
- **★"이론이 없어 불가"는 목표 재정의로 우회**: wild 블록에서 D 가 유일하지 않다는 것은 **basic set 만
  쓸 때**다. **Φ 가 확정되면 D=X·Φ⁺ 가 유일** ⟹ 목표를 "D 추론"에서 **"simples 전부 명시 구성"** 으로
  바꾸면 난점이 사라진다(A₇ p=2·A₆ p=2,3). 필요한 표현은 **문헌 행렬 없이** 만들 수 있는 경우가 많다
  (Fano 안정화군 → GL(4,2) · 순열 heart · Λ²·sl/⟨I⟩·ker(V⊗Λ²V→Λ³V)). 기약성은 **궤도 축약으로 전수**.
  ★단 해소 시 **원 유보 이유를 부정하지 말 것** — "일반론으로는 여전히 옳고 명시 구성이 있었기에 유일성이
  따라왔다"는 경계를 명시하라.


**(u) ★v22 신규 패턴 4개**:
- **★커버리지 행렬에 빈 칸을 적어라 — 그것이 다음 작업 지시다**: 여러 사이클이 쌓은 산출물은
  **봉합하지 않으면 자산이 아니다**. 봉합할 때 **요약표가 아니라 상류 sidecar 를 읽는 검증기**를
  만들면 종합 자체가 **새 교차 게이트 43 개**가 되어 상류 회귀를 잡는다. 그리고 "무엇이 몇 독립
  경로로 확인됐는가 · **무엇이 비었는가**"를 표로 적으면 **빈 칸이 백로그보다 정확한 작업 지시**가
  된다 — 실제로 두 사이클 연속으로 목표를 지정했고 이제 0 이 됐다.
- **★대칭을 쓰려면 먼저 재라(그리고 실측은 성능을 준다)**: 자기쌍대성을 "알려진 사실"로 넘어갈 수
  있었지만 `dim Hom_G(S,S*) = 1`(S* = `(ρ(g)⁻¹)ᵀ`)을 **전수 실측**하니 `Ext²(i,j)=Ext²(j,i)` 를
  **쓸 자격**이 생기면서 동시에 **계산 규모가 m = 1420 → 36** 으로 줄었다(값싼 방향 선택).
  ★대칭 자체도 한 쌍은 **양방향 다 계산해 재확인**하라.
- **★소수 체 전용 표현은 p>2 로 재사용하면 조용히 틀린다**: `if c[i]` 로 계수를 버리고 `^=` 로
  누적하는 코드가 GF(2) 에서는 정확하고 GF(3) 에서는 **오답**(관계식 18 vs 10)을 낸다. 예외도
  경고도 없다. ★**그 오답을 잡은 것은 독립 제2 경로와의 불일치**였다 — 교차검증은 "한 번 맞으면
  끝"이 아니라 **새 체·새 파라미터로 넘어갈 때마다** 값을 한다. 확장 전에 소체 산출물의
  **byte-identity 회귀**를 잡아두면 고칠 때 안전망이 된다.
- **★불변량과 표현을 산출물에서 분리하라**: 관계식의 **개수**(= dim Ext²)는 불변량이지만 **명시
  형태**는 화살 리프트(rad² 를 법으로만 결정) 선택에 의존한다. 둘을 섞어 적으면 **없는 비대칭을
  주장**하게 된다(대칭적 블록에서 비대칭 결과가 나오면 먼저 **기저 선택을 의심**하라). 그리고
  ★**선택-무관 경로를 미리 하나 확보**해 두어라 — 선택 의존 경로만 있으면 그 선택이 실패하는
  대상에서 아무것도 말할 수 없다(A₆ p=3 이 정확히 그 경우였다). ★**부재 주장("균질 제시가 없다")은
  전수로만** 할 수 있다 — 전수가 불가한 곳에서는 **같은 문장을 쓰지 마라**.

## 5. 반드시 지켜야 할 제약

- **결정론 불가침**·**오라클은 사용만**·**honest decomposition**(MatrixGate 금지·opaque KAK-fitted float 금지)·
  **self-contained**·**하드웨어 out**.
- **정직 경계** — 근사·확률·측정후처리는 **관측**. exact ≠ 근사, dense ≠ structural ≠ subspace ≠ tableau.
  봉인 ≠ 관측. ★ε-인증은 **E1–E9 계약**(상한+하계+exact(unitary)+exact(Pauli 채널)+★exact(qudit Weyl 채널)
  — 각 계층 정직 경계 명시).
- **★registry 실측 novelty + 제안값 자체 재검증(v21 강화)**: 공개 저장소 **https://github.com/sadpig70/QuantaFoundry**.
  ★**제안의 구체 좌표/문자표/필드/양자차원/코호몰로지 차원/anyon 수/radical/braid index/diamond 계수는
  스스로 독립 재검증** — 상충·오류 실재 목록(v20 신규 10건 추가): KS-18·A₅ ζ₅·Yu-Oh·Conway-31·SU(2)₄ D²=8·
  ℤ₂⁴ 완전 비아벨화·Q₃₂ tower·Λ³-혼동·"anyon 22→19→16"·depolarizing 'p'·SU(3)₂ 'ℚ(ζ₅)'·
  **★v20 신규: "5₁/5₂ mutant 쌍"(거짓 — Kauffman D 가 이미 구별)·"6₁ amphichiral"(거짓 — 6₃ 의 오인)·
  "6₁ braid index≤3"(거짓 — 4)·"G₂ level-1 rank=14"(dim(G₂) 혼동 — 정확 rank 2)·"SU(3)₃ field ℚ(ζ₆)"
  (정확 ℚ(ζ₉))·"ℤ₂⁵ anyon 256"(|G|²/|rad|² 공식 오류 — 정확 184)·"96+"(부정확)·"H³(ℤ₂⁵,μ₂) dim=20"
  (정확 35)·"E9 계수 ½/(d/(d−1))/d"(전부 반증 — 정확 1)·"d=4 합성 직교성 붕괴"(직교성 층 반증)**.
  ⟹ ★특히: **조건부 계산을 무조건부 결론으로 요약하지 말 것** — 실제 유도까지 해야 주장이 된다.
  ★**M₁₁ 차수 multiset 은 §3x 후속에서 {1,10,10,10,11,16,16,44,45,55} 로 확정**(Dixon 자체유도) — 인용 대신 재유도.

★**v21 신규 — 우리 자신의 정정 2건(자기정정도 기록한다)**:
- ★**"μ₄ ribbon-gap = quasi-Hopf ω-보정 필요"(v20 §4·§7)는 우리 해석이 틀렸다** — 진범은 S-문자공식의
  **켤레 규약 누락**이었고 ω-보정은 불필요하다(§3y Mu4RibbonClosure). 갭 현상 자체는 실재했으므로
  **삭제가 아니라 해석 정정**으로 남겼다. ⟹ **"새 이론이 필요하다"는 결론 전에 규약을 의심하라.**
- ★**"A₆ 의 두 4차원(p=2)은 dual 쌍"이라는 우리 가정은 틀렸다** — 4_a 는 **자기쌍대**이고 실제 쌍은
  **외부 자기동형** 쌍이다(§3y A6CartanP23). A₇ 에서 맞던 패턴이 A₆ 에서 깨진 사례.

★**v21 신규 — 계산 함정 2건**:
- **sympy `simplify` 로 cyclotomic 합의 유리/무리를 판정하지 말 것** — 미환원으로 **전 성분이 "무리"로
  오판**된다(A₆ 실사례). `Cyc` 같은 **정확 벡터 표현**에서 판정하라.
- **블록 계산에서 "무리 성분을 0으로 두는" 휴리스틱을 쓰지 말 것** — A₇ 에선 우연히 통했다. 엄밀하게는
  ω_χ(K) 를 ℤ[ζ_N] **정수좌표**로 계산한 뒤 **𝔭=(p, Φ_N mod p 의 기약인수)** 로 환원해 비교하라.

## 6. 답변 형식 (제안마다)

**3~5개**를 impact×feasibility 순(★v21: **6번 항목 추가**): 1. **proposal**(축+구체 인스턴스) · 2. **rationale**(정체성·compounding·
교차 복리) · 3. **feasibility**(봉인 게이트·오라클 검증·**봉인 경로 명시**: Tier-0 dense/Tier-2/관측/
certificate/ε-sidecar) · 4. **risk**(정직 경계·자체 재유도 계획·**과도확장 상한 선재유도**) ·
5. **novelty**(§3 특히 **3y/3x/3j** 대조 + 시차 강건성) · 6. **reuse**(§4″ 재사용 자산 중 무엇 위에 얹히는가).

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
- **~~ribbon-gap(v20 open)~~ → ★철회(v21)**: twisted double 의 z=Σδ_a⊗a 는 **μ₄ 층에서도 정확한 ribbon**
  이다. v20 이 "구조적 실패"로 본 것은 **S-문자공식의 켤레 규약 누락**이 만든 아티팩트였다(§3y).
- **★켤레-blind 게이트(신규)**: modular data 에서 **S̄ = S∘C**(켤레 = charge conjugation 라벨치환)이므로
  **S-단독 게이트(대칭·유니터리·S²=C·Verlinde·dims·S_vac)는 전부 켤레-blind** 다. **C=항등인 층에서는
  규약이 원리적으로 무해**하므로, 규약 판별은 **반드시 비자기쌍대 예제**에서 하라.
- **★계수 장벽(신규·QEC)**: [[n,1,·]] 격자에서 면 수는 n−1 로 고정이라 **병합 1회 → k=2**(정상)이지만
  **병합 2회 → k=3** 이다. 그래서 단일 병합 족에서는 **두 번째 twist 가 반드시 경계에 흡수**되고
  twist 논리 weight ≤ ⌊m/2⌋ 로 묶인다 — **d 를 올리려면 면을 추가**해야 한다.
- **★Brauer 트리 실산출 조건(신규)**: Sylow 가 **순환(defect 1)** 이면 tree 는 "적용 가능"에서 멈추지 말고
  **실제로 산출**할 수 있다 — ℓ=e=rank(블록|p-regular)·예외중복 m=(p^d−1)/e·정점 배치 전수 →
  D → Φ 정수성·양수성으로 판정(A₆ p=5: **1—9—[8,8]^exc**·det C=5).
- **MTC 인수분해 판정(v20 갱신)**: pointed 부분군 발견 → simple current twist θ(정수=Tannakian vs
  anyonic)·pointed S-부분 rank(퇴화=분해 불가) — SU(3)₂(분해)↔SU(3)₃(비분해) 양방 선례.
- **End-field certificate(신규)**: GF(q)-켤레 simple 쌍 판정 = dim End=2 + F²=−I ⟹ End≅GF(q²).
