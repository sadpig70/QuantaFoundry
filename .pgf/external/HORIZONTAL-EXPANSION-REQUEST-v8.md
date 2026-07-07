<!-- QuantaFoundry 수평 확장 아이디어 제안 요청 — v8 (2026-07-08). v1~v7 후속. self-contained. -->
<!-- 외부 모델 런타임에게 전달용. 이 문서 하나만 읽고 제안 가능하도록 작성됨. -->

# QuantaFoundry — 수평적 확장(Horizontal Expansion) 아이디어 제안 요청 · v8

> **v7 → v8 변경점**: v7 요청으로 8개 런타임의 제안(report7)을 받아 **통합 6축(TrackHE7)을 자율 완주**했다 —
> **봉인 신규 module 2 이하**로: **QMDD 제8 독립 검증경로**(reduction-canonical decision diagram, 텐서망과
> 전제 다름) · **Q₈ 쿼터니언 군 완전 Fourier**(★v6 의 "S₄ (2,2) ζ₃ 필연" closed-negative 의 **상보 positive**
> — Q₈ 는 order-3 원소 전무 → Fourier 가 ℤ[i] 에서 완전히 닫힘, 신규 module 0) · **Majorana braiding 위상
> 게이트**(maj_braid_ybe, ★선검증이 "braid word=non-Clifford" 제안을 반증: 4-Majorana π/4 braid ⊂ Clifford) ·
> **Pauli 채널 diamond-norm exact 증명서**(‖Δ‖◇=‖p−q‖₁ dyadic, Bell primal 최적) · **dual-unitary operator
> entanglement exact**(EE=2 평탄 스펙트럼) · **부호 연접 [[5,1,3]]∘[[5,1,3]]=[[25,1,9]] Tier-2**(★선검증이
> 순진한 설계 [[5,1,3]]∘repcode3(위상거리 1) 반증→자기연접 재설계, 9번째 Tier-2, code513 sub-app ×6 복리).
> 전부 §3 EXCLUDE 에 추가(§3k). §4′에 v8 신규 패턴 4(★**제8 경로·closed-negative 의 상보 positive·연접 정리
> 구조 대조·선검증이 순진설계 반증**)를 추가했다. frontier 도 무인 연속(shor143/155/159/183 자율봉인).

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

## 3. EXCLUDE — 이미 구현·봉인된 것 (재제안 금지)

현재 **92 modules / 418 sealed apps** (root `e2068a001f23…`). **독립 검증경로 8개**
(dense · Clifford tableau · ZX · path-sum ℤ[ω₈] · stabilizer-rank · matchgate/SO(2n) · tensor-network · **QMDD**).

### 3a~3f. v1~v4 소비분 (요약 — 상세는 이전 라운드 EXCLUDE 계보)
- **기초/QFT/QPE/Grover/Trotter·Suzuki/VQE·QAOA/쿼리(DJ·BV·Simon)/walk** · **QEC**(repetition·Steane
  Tier-2·Shor-9·transversal Clifford) · **Shor**(15·21·distinct-prime frontier·cmul factory) ·
  **QSVT 완비** · **Fermionic**(JW/BK/parity·fSWAP) · **분자 H₂·qROM·[[5,1,3]] 증류코어·S₃/D₄ 비아벨
  Fourier+HSP·큐트릿 산술** · **위상 논리연산([[4,2,2]])·MBQC·Z₂ gauge·qLDPC·Schur-Weyl(schur3/4)·
  AKLT·CPTP 채널·1q Clifford 2/3-design**(★2q unitary 2-design=하한 226 closed-negative) ·
  **명시적 산술·Szegedy walk·PEPS·MUB-20·UD-POVM·flag 증후·GF(8) 역원/Frobenius** ·
  **Fibonacci 소비층(F-move·매듭 word·Jones 두 경로, ℚ(ζ₅,√φ))·C₃ phase-poly 정규형·GF(8)+RS(7,3)·
  Schur sampling·MUB shadow·stabilizer-rank 제5 검증경로·[[8,3,2]] triorthogonal 횡단 CCZ**.

### 3g. v5 소비분
- **정확해 동역학**(dual-unitary du_gate_j8·Floquet floquet4_uf·광원뿔 두 경로) · **magic 자원 증명서**
  (ξ(|T⟩)=4−2√2·R(|T⟩)=√2·T-count·★T⊗T↛CS 반증) · **matchgate 제6 검증경로** ·
  **RM [[15,1,3]] 인코더(Tier-2)+transversal T** · **매듭 심화**(첫 비-토러스·TL₃ 상태합·Alexander).

### 3i. v6 소비분 — 통합 6축 (재제안 금지)
- **S₄ 비아벨 곱셈**: s4_mult(V₄⋊S₃). ★**closed-negative**: 완전 S₄ Fourier 는 (2,2) irrep order-3
  원소 trace=−1=ζ₃ → 정수-유니터리 불가 → **ζ₃ 필연**. (3,1)/(2,1,1) 정팔면체 signed-perm 회수.
- **Bogoliubov/Kitaev pairing**: bogoliubov_pair·kitaev4_gs·제6 경로 pairing 확장·Pfaffian Z₂.
- **OTOC/scrambling + Floquet winding**: otoc_du_t1·삼중 경로·winding Σε/2π 정수.
- **채널 magic 자원**: chan_magic_t(T-채널 Choi)·ξ(Φ_T)=게이트 magic(Choi 동형)·catalysis.
- **15-to-1 coherent 증류**: rm15_decoder_t2(8번째 Tier-2, 측정 전 syndrome 추출 코어).
- **텐서망 제7 검증경로**: tncontract_verify(게이트 텐서 인덱스 수축, dense 미실체화).

### 3k. ★v7 소비분 — 통합 6축 (TrackHE7, 이번 라운드 신규 — 재제안 금지)
- **QMDD 제8 독립 검증경로(P1)**: qmdd_verify — 회로를 **Quantum Multi-valued Decision Diagram**(변수순서
  고정 + reduction rule: 중복노드 병합·zero 억제·leading-nonzero 정규화) canonical DAG 위 재귀 rewrite
  로 실행 → golden 열 독립 재산출(dense 미실체화). ★**공유-노드 정규형(reduction) ≠ 텐서망(수축·treewidth)**
  — ghz10 을 51 노드로 압축. 인프라·신규 봉인 0. (**SMT/symbolic 제9 경로·근사 없는 대형 부분수축은 아직 없음.**)
- **Q₈ 쿼터니언 군 완전 Fourier(P5)**: q8_qft(Tier-0, coset Fourier over N={±1}, 신규 module 0).
  ★**S₄ (2,2) ζ₃-필연 closed-negative 의 상보 positive** — Q₈ 는 order-3 원소 전무 → ζ₃ 강제 원인 부재 →
  Fourier 가 ℤ[i](ω₄)에서 완전히 닫힘(2-dim irrep ∈{0,±1,±i}·1-dim 실수 ±1). **ζ 없이 닫히는 최소 비아벨 군.**
  (**A₄·S₅·PSL 등 ζ 필요 군은 여전히 사람게이트 승인 시만. 정수-유니터리 완전 monomial 군 계보는 미개척.**)
- **Majorana braiding 위상 게이트(P2)**: maj_braid_ybe(YBE word B12·B23·B12==CNOT·H·CNOT, 2q Tier-0,
  module 0) + maj_observe. ★**선검증이 "braid word=non-Clifford matchgate" 제안을 반증** — 4-Majorana(JW)
  π/4 braid B_ij=exp(π/4 γ_iγ_j) 전부 Clifford, SO(4) 부호순열·B23==bogoliubov(§4′f). (**Ising anyon 은
  Clifford-only 라 universality 없음(정직). 비아벨 Fibonacci braid 는 이미 소비(3f). 2D Chern 은 아직 없음.**)
- **Pauli 채널 diamond-norm exact 증명서(P3)**: diamond_observe(기봉인 bitflip dilation 을 partial-trace
  로 소비) — ‖Δ‖◇=‖p−q‖₁(dyadic exact)·Bell primal 최적·전역 순수상태 탐색 상한. 인프라·신규 봉인 0.
  (**non-Pauli 채널 diamond·채널 조합 자원·asymptotic·CB-norm 은 아직 없음(Pauli-diagonal island 만 exact).**)
- **dual-unitary operator entanglement exact(P4)**: op_ee_observe(du_gate_j8/dag 소비, operator Schmidt
  reshape+SVD) — DU 정의적 평탄 스펙트럼 s²=[¼×4]·EE=2.0 정확(dyadic). (**Floquet SPT 완전 정수 불변량·2D
  dual-unitary·tripartite operator entanglement 은 아직 없음.**)
- **부호 연접 [[25,1,9]](P6)**: concat_513_513 = [[5,1,3]]∘[[5,1,3]](25q Tier-2 CLIFFORD, 9번째 Tier-2,
  code513_encoder 게이트 시퀀스 ×6 복리, 신규 module 0). ★**선검증이 순진한 설계 반증** — [[5,1,3]]∘repcode3
  (내부 bit-flip 반복=위상거리 1=비대칭)는 "거리 9" 거짓 → **자기연접**(대칭·양자완전부호, d=9=3×3, 연접
  정리)로 재설계. witness concat_observe(symplectic 안정군 역전파, 20 inner-block + 4 outer-lift 구조 exact
  대조). (**code switching coherent·d≥5 색부호/surface concat·양자 BCH·hypergraph-product 대형은 아직 없음.**)

### 3j. 예비 판정분 (재제안 시 보강 조건 — 일부는 3k 에서 소비됨)
- **A₄/큐딧 Fourier**: ζ₃ 신규 module 사람게이트 필요(field ℚ(√−3) 차수 2 — 승인 요건 갖춰 제안).
  ★Q₈(3k)이 "ζ-free 최소 비아벨"을 채웠으니, 다음은 **정수-monomial 완전 군 계보**(hyperoctahedral B_n·
  일반화 대칭군 G(m,1,n)) 또는 **ζ₃ 승인 하 A₄** 로 명확히 갈라 제안하라.
- **code switching [[8,3,2]]↔Steane·d=3 surface+surgery·RS/BCH 복호기·정수 나눗셈·맥락성 증명서·
  큐딧 심플렉틱·Hecke 브레이드·2D DU SPT** — 각 1~2/8 저합의; 구체 인스턴스·오라클 경로·복리 접점
  강화 시 재평가. (★2D DU 는 3k P4 로 operator entanglement 만 소비 — SPT 불변량은 여전히 열림.)

**핵심: 사소한 변형 금지. 질적 새 계층. 괄호 "아직 없음"이 관문이면 환영.**

## 4. 우리가 원하는 것 (방향 감 — 강요 아님)

- **부호 심화** — code switching coherent(측정 전)·d≥5 색부호/surface concatenation·양자 BCH·
  hypergraph-product qLDPC 대형(Tier-2 tableau 로 임의 크기 가능).
- **동역학 심화** — Floquet SPT **정수** 불변량·2D dual-unitary(perfect tensor 격자)·tripartite/multipartite
  operator entanglement.
- **free-fermion 심화** — 일반 BdG 각도(닫힌형)·2D Chern number(정수 위상)·Majorana **fusion 규칙**(braid 넘어).
- **표현론 심화** — 정수-유니터리로 완전히 닫히는 monomial 군 계보(B_n·G(m,1,n))·모듈러 표현·Hecke 대수.
- **자원 이론 심화** — non-Pauli 채널 exact 부분·채널 조합/asymptotic 자원·맥락성(contextuality) 증명서·
  magic spectrum 세분.
- **검증 메타** — **제9 경로**(SMT/symbolic solver·회로 동치 증명서·근사 없는 treewidth 부분수축)·
  QMDD 확장(대형 부분 DAG). "다른 8 경로와 수학적 전제가 어떻게 다른가"를 명시하라.
- 그 밖에 **당신이 더 나은 축을 알면 제안하라.**

## 4′. ★성공 패턴 (v1→v8)

**(a) 게이트 우회** · **(b) 직접 닫힌형 구성**(탐색 금지) · **(c) 승인-module 사람게이트**(닫힌형 각도·
π-free surd 우대) · **(d) 반증→회수·자유도 재도출·sub-app 복리** · **(e) 기소비 선점 대조·교차 복리·
게이트 구조 회피·인프라 즉시 소비** · **(f) 다중 독립 경로 대조·Tier-2 드라이버·주기성 역원 회피·
오라클 동치 재발견** · **(g) 봉인 전 선검증 반증·sub-app 대량 복리·Choi/동형 재해석·제7 경로**.

**(h) ★v8 신규 패턴 4개**:
- **제8 경로(QMDD)**: dense·tableau·ZX·path-sum·stab-rank·matchgate·텐서망에 **decision-diagram
  reduction** 이 더해졌다 — 핵심은 "**공유 노드 정규형(병합/억제) ≠ 텐서 수축(treewidth)**"의 전제 차이.
  제9 경로 제안 시 **기존 8 경로 어느 것과도 수학적 전제가 겹치지 않음**을 한 문장으로 증명하라.
- **closed-negative 의 상보 positive**: v6 이 "S₄ (2,2)=ζ₃ 필연"을 negative 로 닫자, v7 은 **같은 질문의
  positive 쌍**(Q₈=ζ-free 최소 비아벨)을 찾아 대칭을 완성했다. 어떤 대상이 "불가능"으로 닫혔다면 **그
  경계 바로 옆의 가능 인스턴스**를 제시하라(negative-positive 쌍이 최고 채택).
- **연접 정리 구조 대조**: [[25,1,9]] 봉인은 전수(2²⁴) 대신 **정리(연접 d=d₁d₂) + 블록-국소 최소무게 +
  symplectic 안정군 구조 exact 대조**로 정직하게 검증했다. 대형 구조물은 "**어떤 정리로 전수를 대체하고,
  무엇이 exact 이고 무엇이 관측인가**"를 스스로 분리해 제시하라.
- **선검증이 순진 설계 반증**: "concat=거리 9" 순진 제안이 위상-비트 비대칭으로 반증됐다(→자기연접 재설계).
  거리·보호·차수를 주장하면 **비대칭/특수 원소가 그 주장을 깨는지 봉인 전 스스로 점검**하라(§4′d·g 연장).

## 5. 반드시 지켜야 할 제약

- **결정론 불가침**·**오라클은 사용만**(verify_seal/contracts 재구현 금지)·**honest decomposition**
  (MatrixGate 금지)·**self-contained**·**하드웨어 out**.
- **정직 경계** — 근사·확률·측정후처리는 **관측**. exact ≠ 근사, dense ≠ structural ≠ subspace ≠
  tableau. 상태준비 app 은 정의 열만 물리. **근사 truncation(텐서망 등)은 봉인 아님**.
- **★registry 실측 novelty**: 공개 저장소 **https://github.com/sadpig70/QuantaFoundry**
  (`registry/`·`specs/`·`scripts/` 공개) — 접근 가능하면 실측 대조 우대(v4·v6·v7 에서 실측한 회신이
  최고 채택률). 불가하면 §3 정독 + **구조적("계층 부재") novelty**(§4′(e) 시차 강건성).

## 6. 답변 형식 (제안마다)

**3~5개**를 impact×feasibility 순: 1. **proposal**(축+구체 인스턴스) · 2. **rationale**(정체성·
compounding·교차 복리) · 3. **feasibility**(봉인 게이트·오라클 검증·**§4′(b) exact 근거**·필요 시
§4′(c) 게이트 요건 — 단 §4′(e)(f)(g)(h) 회피 먼저) · 4. **risk**(정직 경계) · 5. **novelty**(§3 특히
**3i/3k/3j** 대조 + 시차 강건성).

## 7. 개념 미니 용어집

- **봉인/compounding/honest boundary/teeth/subspace 강검증/Tier-2/closed-negative** — 이전 라운드 정의 유지.
- **검증경로 8**: dense·tableau·ZX·path-sum ℤ[ω₈]·stabilizer-rank·matchgate/SO(2n)·tensor-network·
  **QMDD**(reduction-canonical decision diagram, 공유 노드 정규형 — 텐서 수축과 전제 다름) — 제9를 환영한다.
