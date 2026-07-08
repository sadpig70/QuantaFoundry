<!-- QuantaFoundry 수평 확장 아이디어 제안 요청 — v9 (2026-07-08). v1~v8 후속. self-contained. -->
<!-- 외부 모델 런타임에게 전달용. 이 문서 하나만 읽고 제안 가능하도록 작성됨. -->

# QuantaFoundry — 수평적 확장(Horizontal Expansion) 아이디어 제안 요청 · v9

> **v8 → v9 변경점**: v8 요청으로 8개 런타임의 제안(report8)을 받아 **통합 6축(TrackHE8)을 완주·폐합**했다.
> **봉인 신규 module 0**(전 축): **ANF/bit-vector 제9 독립 검증경로**(계산기저 Boolean 함수 GF(2) 다항식
> 항등, 진폭무관, 커버 144 순열앱) · **B₃ 초팔면체군 ζ-free**(★S₄ (2,2) ζ₃-필연 closed-negative 의 상보
> positive — B₃ 가 **rational group**(모든 g~g^k, coprime k)임을 판정→정수 문자표→Fourier ζ-free) ·
> **HGP qLDPC [[27,4,3]] Tier-2 봉인**(Tillich-Zémor Hamming[7,4,3]×rep[3], 거리-3 대형, ★27q 를 정준
> stabilizer tableau 로 dense-free 봉인=12q 그룹 dense 실패의 우회) · **2D QWZ Chern 정수 위상**(mass-sign
> 닫힌형 정수공식 == FHS 격자 numerics) · **non-Pauli 유니터리 채널 diamond**(AKN arc 닫힌형, cyclotomic
> surd/정수) · **Peres-Mermin 맥락성**(state-independent parity 모순). §3l 에 추가. §4′에 v9 신규 패턴 5
> (★**Tier-2 로 dense 회피·rational group 판정·이중 독립경로 exact·parity 모순 certificate·계산기저 함수 대수**).

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
  비-Clifford 대형은 **관측(witness)** 또는 structural 로 — 제안 시 봉인 경로를 명시하라(§4′i 첫째).

## 3. EXCLUDE — 이미 구현·봉인된 것 (재제안 금지)

현재 **93 modules / 418 sealed apps** (root `b5df121bed7e3527…`). **독립 검증경로 9개**
(dense · tableau · ZX · path-sum ℤ[ω₈] · stabilizer-rank · matchgate/SO(2n) · tensor-network · QMDD · **ANF/bit-vector**).

### 3a~3f. v1~v4 소비분 (요약 — 상세는 이전 라운드 EXCLUDE 계보)
- **기초/QFT/QPE/Grover/Trotter·Suzuki/VQE·QAOA/쿼리(DJ·BV·Simon)/walk** · **QEC**(repetition·Steane
  Tier-2·Shor-9·transversal Clifford) · **Shor**(15·21·distinct-prime frontier shor69…183·cmul factory) ·
  **QSVT 완비** · **Fermionic**(JW/BK/parity·fSWAP) · **분자 H₂·qROM·[[5,1,3]] 증류코어·S₃/D₄ 비아벨
  Fourier+HSP·큐트릿 산술** · **위상 논리연산([[4,2,2]])·MBQC·Z₂ gauge·qLDPC([[8,1,2]] 소형)·Schur-Weyl·
  AKLT·CPTP 채널·1q Clifford 2/3-design** · **명시적 산술·Szegedy walk·PEPS·MUB-20·UD-POVM·flag 증후·
  GF(8)·Fibonacci 소비층·C₃ phase-poly·RS(7,3)·stabilizer-rank 제5경로·[[8,3,2]] 횡단 CCZ**.

### 3g. v5 소비분
- **정확해 동역학**(dual-unitary du_gate_j8·Floquet floquet4_uf) · **magic 자원 증명서**(ξ(|T⟩)=4−2√2·
  T⊗T↛CS 반증) · **matchgate 제6 검증경로** · **RM [[15,1,3]] 인코더(Tier-2)** · **매듭 심화**(fig8·TL₃).

### 3i. v6 소비분
- **S₄ 비아벨 곱셈**(★closed-negative: (2,2) irrep ζ₃ 필연) · **Bogoliubov/Kitaev pairing**(Pfaffian Z₂) ·
  **OTOC/Floquet winding** · **채널 magic Choi** · **15-to-1 coherent 증류(rm15_decoder)** · **텐서망 제7경로**.

### 3k. v7 소비분 (TrackHE7)
- **QMDD 제8 검증경로** · **Q₈ 완전 Fourier**(ζ-free 최소 비아벨) · **Majorana braiding**(⊂Clifford) ·
  **Pauli 채널 diamond-norm**(Pauli-diagonal island) · **dual-unitary operator entanglement**(1D bipartite) ·
  **부호 연접 [[25,1,9]]**(자기연접 Tier-2).

### 3l. ★v8 소비분 — 통합 6축 (TrackHE8, 이번 라운드 신규 — 재제안 금지)
- **ANF/bit-vector 제9 독립 검증경로(P1)**: `anf_verify` — 계산기저 permutation 회로를 각 출력비트
  **Algebraic Normal Form over GF(2)** 다항식으로 표현, path A(게이트순서 symbolic ANF 전파, 진폭무관) vs
  path B(golden 진리표 Möbius) 다항식 항등. 커버 144 순열앱. **진폭 무관 Boolean 함수 대수** — 8경로(진폭/
  구조)와 검증객체 상이·perm_subspace(정수순열값)와도 상이. (**SMT/Gröbner/CVE 제10 경로·decision-diagram
  변형은 아직 없음.**)
- **B₃ 초팔면체군 ζ-free 정수-monomial(P2)**: `b3_observe` — B₃=(ℤ₂)³⋊S₃(48원소, Coxeter type B)가
  **rational group**(모든 g 가 gcd(k,ord)=1 인 g^k 와 켤레)임을 판정 → **정수 문자표** → Fourier ζ-free.
  ★S₄ (2,2) ζ₃-필연 closed-negative 의 상보 positive. b3_mult 곱셈오라클(12q) 회로실현성(MMD 154게이트).
  (**A₄/S₅ 등 ζ 필요 군은 ζ₃ 승인 시만·G(m≥3,1,n) monomial·B_n(n≥4) 대형·모듈러 표현은 아직 없음.**)
- **HGP qLDPC [[27,4,3]] Tier-2 봉인(P4)**: `hgp_qldpc27` — Tillich-Zémor 하이퍼그래프곱(Hamming[7,4,3]×
  rep[3]), 거리-3 대형, |0_L⟩ prep 정준 tableau(dense 미실체화, 27q). ★양 고전시드 full-rank→transpose
  trivial→d=3 보존(비대칭 회피). (**BCH cyclic CSS·code switching coherent·더 큰 HGP(d≥5)·surface+surgery는
  아직 없음.**)
- **2D QWZ Chern 정수 위상(P3)**: `chern_observe` — Qi-Wu-Zhang 2-band, **mass-sign 닫힌형 정수공식** C=
  (2sign(m)−sign(m−2)−sign(m+2))/2 == **FHS 격자 numerics**. 위상다이어그램 C=±1/0·gap-closing m∈{−2,0,2}.
  (**|C|≥2 고차 Chern·3D 위상(ℤ₂/ℤ)·Floquet SPT 정수불변량·spin/mirror Chern 은 아직 없음.**)
- **non-Pauli 유니터리 채널 diamond(P6)**: `diamond_unitary_observe` — AKN/Watrous arc 닫힌형 ‖Φ_U−Φ_V‖◇=
  2sin(min(Θ/2,π/2)), Clifford+T cyclotomic surd/정수(T=√(2−√2)·CZ=2). Pauli island(3k P3)의 상보.
  (**non-unitary CPTP(amplitude-damping) diamond=SDP·채널 조합/asymptotic·CB-norm 은 아직 없음.**)
- **Peres-Mermin 맥락성(P5)**: `peres_mermin_observe` — 3×3 magic square, row/col product parity 모순
  (Π_row=+1 vs Π_col=−1) → state-independent KS. (**contextual fraction LP 정량화·큐트릿 Gross-Wigner
  negativity·Hardy paradox·더 큰 KS 집합(18-vector 등)은 아직 없음.**)

### 3j. 예비 판정분 (재제안 시 보강 조건)
- **code switching**(Steane↔[[8,3,2]] coherent isometry)·**BCH/RS 복호기**·**Hecke 브레이드**·**정수 나눗셈**·
  **큐딧 심플렉틱**·**Floquet SPT/2D DU SPT** — 각 저합의; 구체 인스턴스·오라클 경로·복리 접점 강화 시 재평가.
- **제10 검증경로**: SMT/Gröbner/CVE(solver 기반, v8 에서 결정론·재현성 리스크로 ANF 우선) — 내장 결정론
  엔진(외부 solver 무의존) 보장 시 환영.

**핵심: 사소한 변형 금지. 질적 새 계층. 괄호 "아직 없음"이 관문이면 환영.**

## 4. 우리가 원하는 것 (방향 감 — 강요 아님)

- **검증 메타** — **제10 경로**(기존 9 경로와 전제 상이 한 문장 증명)·회로 동치 증명서·treewidth 부분수축.
- **부호 심화** — BCH/RS **cyclic algebraic CSS**·code switching coherent·d≥5 HGP/color·surface+surgery.
- **표현론 심화** — G(m,1,n) monomial(ζ_m 승인)·B_n(n≥4) 대형(Tier-2)·모듈러 표현·Hecke 대수·A₄(ζ₃ 승인).
- **동역학 심화** — Floquet SPT **정수** 불변량·2D dual-unitary·|C|≥2 고차 Chern·3D 위상.
- **자원 이론 심화** — non-unitary 채널 exact 부분·**contextual fraction LP**·큐트릿 Wigner negativity·magic spectrum.
- **free-fermion 심화** — 일반 BdG 각도 닫힌형·Majorana fusion 규칙·2D Chern superconductor.
- 그 밖에 **당신이 더 나은 축을 알면 제안하라.**

## 4′. ★성공 패턴 (v1→v9)

**(a) 게이트 우회** · **(b) 직접 닫힌형 구성**(탐색 금지) · **(c) 승인-module 사람게이트**(닫힌형 각도·
π-free surd 우대) · **(d) 반증→회수·자유도 재도출·sub-app 복리** · **(e) 기소비 선점 대조·교차 복리·
게이트 구조 회피·인프라 즉시 소비** · **(f) 다중 독립 경로 대조·Tier-2 드라이버·오라클 동치 재발견** ·
**(g) 봉인 전 선검증 반증·sub-app 대량 복리·Choi/동형 재해석·제7 경로** · **(h) 제8 경로·closed-negative
의 상보 positive·연접 정리 구조 대조·선검증이 순진설계 반증**.

**(i) ★v9 신규 패턴 5개**:
- **Tier-2 tableau 로 dense 회피**: 12q B₃ 곱셈 오라클은 dense compose(154×4096³)가 실용 밖이었으나,
  27q HGP 인코더는 **Clifford → 정준 stabilizer tableau**(dense 미실체화)로 봉인 성공했다. 큰 대상이
  Clifford 면 **Tier-2 경로**를, 아니면 **관측**을 명시하라. (Tier-0 dense 는 n≲12 만.)
- **rational group 판정 = ζ-free 증명**: B₃ 가 Q-group(모든 g~g^k, coprime k)임을 판정해 정수 문자표를
  결론했다. 군 Fourier 제안 시 **rational group 여부를 selection criterion**으로 스스로 점검하라(ζ 필요 여부 예보).
- **이중 독립 경로로 exact 확립**: 2D Chern = mass-sign 닫힌형 정수공식 == FHS 격자 numerics; unitary
  diamond = AKN 닫힌형 == convex-hull 거리 == 상태공간 탐색. **닫힌형(exact) + 독립 수치확인** 쌍을 제시하라.
- **parity/모순 certificate**: Peres-Mermin 은 대수적 parity 모순(Π_row≠Π_col)으로 맥락성을 exact 증명했다.
  회로 아닌 **combinatorial/대수 certificate**(정수 witness)도 1급 산출 — "무엇이 모순의 정수 핵인가"를 제시하라.
- **계산기저 함수 대수(제9 경로)**: ANF 는 진폭이 아니라 **GF(2) Boolean 함수 항등**을 본다. 제10 경로는
  "다른 9 경로와 수학적 전제가 겹치지 않음"을 한 문장으로 증명하라(계산 vs 증명, 함수 vs 진폭 등).

## 5. 반드시 지켜야 할 제약

- **결정론 불가침**·**오라클은 사용만**·**honest decomposition**(MatrixGate 금지)·**self-contained**·**하드웨어 out**.
- **정직 경계** — 근사·확률·측정후처리는 **관측**. exact ≠ 근사, dense ≠ structural ≠ subspace ≠ tableau.
  봉인 ≠ 관측(certificate/witness 는 봉인 자산 아님). **근사 truncation 은 봉인 아님**.
- **★registry 실측 novelty**: 공개 저장소 **https://github.com/sadpig70/QuantaFoundry**
  (`registry/`·`specs/`·`scripts/` 공개) — 접근 가능하면 실측 대조 우대. 불가하면 §3 정독 + 구조적 novelty.

## 6. 답변 형식 (제안마다)

**3~5개**를 impact×feasibility 순: 1. **proposal**(축+구체 인스턴스) · 2. **rationale**(정체성·compounding·
교차 복리) · 3. **feasibility**(봉인 게이트·오라클 검증·§4′(b) exact 근거·**봉인 경로 명시**: Tier-0 dense(n≲12)
/Tier-2 tableau/관측 — §4′(i) 첫째) · 4. **risk**(정직 경계) · 5. **novelty**(§3 특히 **3l/3k/3j** 대조 + 시차 강건성).

## 7. 개념 미니 용어집

- **봉인/compounding/honest boundary/teeth/subspace 강검증/Tier-2/closed-negative/rational group** — 이전 라운드 정의 유지.
- **검증경로 9**: dense·tableau·ZX·path-sum ℤ[ω₈]·stabilizer-rank·matchgate/SO(2n)·tensor-network·QMDD·
  **ANF/bit-vector**(계산기저 Boolean 함수 GF(2) 다항식 항등, 진폭 무관) — 제10 을 환영한다.
