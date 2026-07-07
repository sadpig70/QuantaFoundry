<!-- QuantaFoundry 수평 확장 아이디어 제안 요청 — v7 (2026-07-07). v1~v6 후속. self-contained. -->
<!-- 외부 모델 런타임에게 전달용. 이 문서 하나만 읽고 제안 가능하도록 작성됨. -->

# QuantaFoundry — 수평적 확장(Horizontal Expansion) 아이디어 제안 요청 · v7

> **v6 → v7 변경점**: v6 요청으로 8개 런타임의 제안(33개)을 받아 **통합 6축 전부를 자율 완주**했다 —
> **사람게이트 0**으로: S₄ 비아벨 곱셈(★봉인 전 선검증이 "S₄ 정수 Fourier" 제안의 절반을 반증 —
> (2,2) irrep ζ₃ 필연) · Bogoliubov/Kitaev pairing(제6 검증경로 비수보존 확장 + Pfaffian Z₂) ·
> OTOC/scrambling + Floquet winding(du_gate 소비 삼중경로) · 채널 magic 자원(Choi 동형: 채널
> magic=게이트 magic + catalysis) · 15-to-1 coherent 증류(RM 디코더=측정 전 syndrome 추출 코어,
> 8번째 Tier-2) · **텐서망 정확 수축 제7 독립 검증경로**. 전부 §3 EXCLUDE 에 추가(§3i). §4′에 v7
> 신규 패턴 4(★**봉인 전 선검증 반증·sub-app 대량 복리·Choi/동형 재해석·제7 경로**)를 추가했다.

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

현재 **91 modules / 386 sealed apps** (root `60a6de09…`). **독립 검증경로 7개**
(dense · Clifford tableau · ZX · path-sum ℤ[ω₈] · stabilizer-rank · matchgate/SO(2n) · **tensor-network**).

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

### 3i. ★v6 소비분 — 통합 6축 (이번 라운드 신규 — 재제안 금지)
- **S₄ 비아벨 곱셈(P4)**: s4_mult(V₄⋊S₃, s3_mult 복리). ★**closed-negative**: 완전 S₄ Fourier 는
  (2,2) irrep 이 order-3 원소 trace=−1=ζ₃ 고유값 → 정수-유니터리 불가 → **ζ₃ 필연**(rational group ≠
  정수-유니터리 실현). (3,1)/(2,1,1) 는 정팔면체 signed-perm 정수표현 회수.
  (**A₄·S₅·PSL 등 ζ 필요 군의 Fourier 는 ζ₃ 사람게이트 승인 시만 — 정수-유니터리 완전 군은 미개척.**)
- **Bogoliubov/Kitaev pairing(P2)**: bogoliubov_pair(exp(iπ/4·XX) 수보존 깸)·kitaev4_gs(sweet-point
  even-parity dimer)·제6 경로 pairing 확장·Pfaffian Z₂. (**일반 BdG 각도·2D free-fermion·Majorana
  braiding 위상 게이트는 아직 없음.**)
- **OTOC/scrambling + Floquet winding(P3)**: otoc_du_t1(OTOC 연산자, du 소비)·삼중 경로·Z-basis
  trivial·winding Σε/2π 정수. (**Floquet SPT 완전 불변량·2D DU·operator entanglement 는 아직 없음.**)
- **채널 magic 자원(P6)**: chan_magic_t(T-채널 Choi)·ξ(Φ_T)=게이트 magic(Choi 동형)·catalysis.
  (**noisy channel robustness·diamond norm·채널 조합 자원·asymptotic 은 아직 없음.**)
- **15-to-1 coherent 증류(P1)**: rm15_decoder_t2(8번째 Tier-2, 측정 전 syndrome 추출 코어)·
  부호어→syndrome0(accept)·오류→syndrome≠0. (**code switching·d≥5 증류·concatenation 은 아직 없음.**)
- **★텐서망 제7 검증경로(P5)**: tncontract_verify(게이트 텐서 인덱스 수축, dense 미실체화 열 벡터,
  360앱 재검증). (**대형 treewidth 부분수축·PEPS 경계 MPS·근사 없는 2D 수축은 아직 없음.**)

### 3j. 예비 판정분 (재제안 시 보강 조건)
- **A₄/큐딧 Fourier**: ζ₃ 신규 module 사람게이트 필요(field ℚ(√−3) 차수 2 — 승인 요건 갖춰 제안).
- **code switching [[8,3,2]]↔Steane·d=3 surface+surgery·RS/BCH 복호기·정수 나눗셈·맥락성 증명서·
  큐딧 심플렉틱·Hecke 브레이드·2D DU SPT** — 각 1~2/8 저합의; 구체 인스턴스·오라클 경로·복리 접점
  강화 시 재평가.

**핵심: 사소한 변형 금지. 질적 새 계층. 괄호 "아직 없음"이 관문이면 환영.**

## 4. 우리가 원하는 것 (방향 감 — 강요 아님)

- **자원 이론 심화** — 채널 robustness(noisy 밖 exact 부분)·자원 조합·catalysis 계층·magic spectrum.
- **부호 심화** — code switching coherent·d=3 색부호/surface·양자 BCH·concatenation.
- **동역학 심화** — Floquet SPT 정수 불변량·2D dual-unitary·operator entanglement exact.
- **free-fermion 심화** — 일반 BdG 각도(닫힌형)·Majorana braiding 위상 게이트·2D Chern.
- **표현론 심화** — 정수-유니터리로 완전히 닫히는 군(signed-permutation/monomial 군)·모듈러 표현.
- **검증 메타** — 제8 경로(SMT/symbolic·decision diagram)·회로 동치 증명서·treewidth 부분수축 확장.
- 그 밖에 **당신이 더 나은 축을 알면 제안하라.**

## 4′. ★성공 패턴 (v1→v7)

**(a) 게이트 우회** · **(b) 직접 닫힌형 구성**(탐색 금지) · **(c) 승인-module 사람게이트**(닫힌형 각도·
π-free surd 우대) · **(d) 반증→회수·자유도 재도출·sub-app 복리** · **(e) 기소비 선점 대조·교차 복리·
게이트 구조 회피·인프라 즉시 소비** · **(f) 다중 독립 경로 대조·Tier-2 드라이버·주기성 역원 회피·
오라클 동치 재발견**.

**(g) ★v7 신규 패턴 4개**:
- **봉인 전 선검증 반증**: S₄ "정수 Fourier" 제안이 (2,2) irrep 에서 ζ₃ 필연임을 봉인 전 numpy
  선검증이 밝혀 closed-negative 로 전환했다. 제안이 "이 각도가 exact 로 떨어진다"고 주장하면 그
  **반례 가능성(특정 irrep/원소가 무리수 강제)을 스스로 점검**하라. 틀린 절반의 정직한 회수(3,1 정수
  표현)도 1급 산출이다.
- **sub-app 대량 복리**: OTOC 회로는 봉인 du_gate_j8·du_gate_dag 를 **24개 sub-app 으로** 조립했다.
  기봉인 소형 자산을 대량 재사용하는 큰 회로 제안 우대(신규 module 0 유지).
- **Choi/동형 재해석**: 채널 magic 을 Choi 상태로, Kitaev 위상을 Pfaffian 부호로 — **동형사상으로
  새 축을 기존 인프라(state magic·제6 경로)에 얹었다**. "이 대상을 어떤 동형으로 기존 자산에
  환원하는가"를 제시하면 즉시 소비된다.
- **제7 경로(텐서망)**: dense·tableau·ZX·path-sum·stab-rank·matchgate 에 텐서망 수축이 더해졌다.
  제8 경로(SMT·decision diagram 등)를 환영한다 — "다른 6+1 경로와 수학적 전제가 다른가"를 명시하라.

## 5. 반드시 지켜야 할 제약

- **결정론 불가침**·**오라클은 사용만**(verify_seal/contracts 재구현 금지)·**honest decomposition**
  (MatrixGate 금지)·**self-contained**·**하드웨어 out**.
- **정직 경계** — 근사·확률·측정후처리는 **관측**. exact ≠ 근사, dense ≠ structural ≠ subspace ≠
  tableau. 상태준비 app 은 정의 열만 물리. **근사 truncation(텐서망 등)은 봉인 아님**.
- **★registry 실측 novelty**: 공개 저장소 **https://github.com/sadpig70/QuantaFoundry**
  (`registry/`·`specs/`·`scripts/` 공개) — 접근 가능하면 실측 대조 우대(v4·v6 에서 실측한 회신이
  최고 채택률). 불가하면 §3 정독 + **구조적("계층 부재") novelty**(§4′(e) 시차 강건성).

## 6. 답변 형식 (제안마다)

**3~5개**를 impact×feasibility 순: 1. **proposal**(축+구체 인스턴스) · 2. **rationale**(정체성·
compounding·교차 복리) · 3. **feasibility**(봉인 게이트·오라클 검증·**§4′(b) exact 근거**·필요 시
§4′(c) 게이트 요건 — 단 §4′(e)(f)(g) 회피 먼저) · 4. **risk**(정직 경계) · 5. **novelty**(§3 특히
**3i/3j** 대조 + 시차 강건성).

## 7. 개념 미니 용어집

- **봉인/compounding/honest boundary/teeth/subspace 강검증/Tier-2/closed-negative** — 이전 라운드 정의 유지.
- **검증경로 7**: dense·tableau·ZX·path-sum ℤ[ω₈]·stabilizer-rank·matchgate/SO(2n)·tensor-network
  (그래프 텐서 수축, dense 미실체화) — 제8을 환영한다.
