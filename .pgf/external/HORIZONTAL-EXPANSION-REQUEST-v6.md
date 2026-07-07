<!-- QuantaFoundry 수평 확장 아이디어 제안 요청 — v6 (2026-07-07). v1~v5 후속. self-contained. -->
<!-- 외부 모델 런타임에게 전달용. 이 문서 하나만 읽고 제안 가능하도록 작성됨. -->

# QuantaFoundry — 수평적 확장(Horizontal Expansion) 아이디어 제안 요청 · v6

> **v5 → v6 변경점**: v5 요청으로 8개 런타임의 제안(35개)을 받아 **통합 5축 전부를 자율 완주**했다 —
> **사람게이트 0**으로: 정확해 동역학(dual-unitary+Floquet, ★역대 최고 합의 7/8) · magic 자원
> exact 증명서(ℚ(√2) 정확산술 primal-dual-격차0) · **Gaussian/matchgate 제6 독립 검증경로** ·
> **RM [[15,1,3]] 완전 논리-입력 인코더(모듈 90, 7번째 Tier-2)** + transversal T ·
> 매듭 심화(첫 비-토러스 매듭·TL₃ 상태합 제3 Jones 경로·Alexander 정수). 전부 §3 EXCLUDE 에
> **추가**했다(§3g). §4′에 v6 신규 패턴 4(★**다중 독립 경로 대조·Tier-2 드라이버·주기성 역원 회피·
> 오라클 동치 재발견**)를 추가했다. 이제 **그 너머의 새 축**을 구한다.

---

## 1. 프로젝트 정체성 (제안의 유효성을 규정 — 먼저 읽어라)

QuantaFoundry 는 **미래의 완전한 결함허용 양자컴퓨터(FTQC/QPC)가 실현될 때 쓸 소프트웨어 자산을 지금
미리 축적**하는 파운드리다. AI 가 회로를 생성하고, **결정론적 오라클(QPGF)이 byte-identical 재봉인으로
검증**하며, 봉인을 통과한 것만 registry 에 영구 보존된다.

- 하드웨어 실행은 **의도적으로 범위 밖**(노이즈·QPU·실행증거 없음). 봉인 = **이상적 수학적 진실**(exact
  유니터리/구조). 신뢰의 근거는 봉인 시점의 **결정론 + 수학적 독립검증**뿐이다.
- 좋은 제안 = **작은 인스턴스가 Tier-0 EXACT 로 봉인 가능**(또는 Tier-2 Clifford tableau)하고,
  **오라클로 독립 검증 가능**하며, **compounding 이 크고**, 질적으로 새로운 축.

## 2. "수평적(Horizontal)" 확장의 정의

- **수평** = 새로운 **추상화 계층·대수 구조·알고리즘 클래스**. (파라미터/사이트 확대 = 수직, 원치 않음.)
- 봉인 단위: `module`(기본 게이트) 위 `app`(합성 회로) — 이상적으로 **새 module 0**.
  Tier: 0 EXACT(dense, n≲12) · 1 STRUCTURAL(Merkle+정수/부분공간 witness) · 2 CLIFFORD(정준 tableau,
  임의 크기 — 각도 무관 Clifford 대형 자산의 정식 경로).

## 3. EXCLUDE — 이미 구현·봉인된 것 (재제안 금지)

현재 **90 modules / 380 sealed apps** (root `12244b5c…`). **독립 검증경로 6개**
(dense · Clifford tableau · ZX · path-sum ℤ[ω₈] · stabilizer-rank · **matchgate/SO(2n)**). 카테고리:

### 3a. v1 이전 (기존 자산)
- **기초**: Bell/GHZ(≤16)·cluster/ring/W(3~10), 표준 1·2·다중제어 게이트(X/Z/H/S/T/√X, CNOT/CZ/
  Toffoli/Fredkin/iSWAP, c3x…c12x), 회전/위상 특정각·controlled-Rk.
- **QFT/QPE/QAE** 계열 완비 · **Grover/증폭** · **Trotter/Suzuki/Pauli-지수** · **VQE/QAOA** ·
  **쿼리(DJ/BV/Simon)/coined walk**.
- **QEC**: repetition·syndrome·Shor-9·Steane(Tier-2)·transversal 논리 Clifford(H/S/CNOT).
- **Shor**: 15·21 진짜 산술·distinct-prime structural frontier(shor69…3683, 부분공간 순열 강검증)·cmul factory.
- **QSVT/block-encoding 완비** · **Fermionic**: JW/BK/parity·tapering·fSWAP.
- **분자 H₂·qROM+SELECT-PREPARE·magic state+[[5,1,3]] 증류 코어·S₃/D₄ 비아벨 Fourier+HSP 1-shot·
  큐트릿 임베딩 산술** · **채택/경화**(QASM3 round-trip 344·CLI·citable root·revocation·ed25519).

### 3b~3d. v2·v3 소비분
- **위상 논리연산**([[4,2,2]] surface·lattice surgery·토릭) · **MBQC**(3×3 클러스터·게이트 텔레포테이션
  촉매·계층 C₁⊂C₂⊂C₃ witness) · **Ising braid** · **Clifford QCA** · **Z₂ gauge** · **qLDPC [[8,1,2]]** ·
  **Schur-Weyl(schur3/4)** · **AKLT(MPS)** · **CPTP 채널 family+Choi** · **1q Clifford 24 = 정확 2/3-design**
  (★2q 소형 unitary 2-design = closed-negative 하한 226 — 재제안 금지) ·
  **명시적 산술(cuccaro/draper/비교기)** · **Szegedy walk** · **PEPS(2×2 RVB)** · **MUB-20 state
  2-design** · **UD-POVM Naimark** · **1-flag FT 증후 추출** · **GF(8) 역원/Frobenius**.

### 3e. v4 소비분
- **Fibonacci 소비층**(F-move·토러스 word·Jones 두 경로, 대수체 ℚ(ζ₅,√φ)) · **C₃ 대각 phase-polynomial
  정규형**(T/CS/CCZ 사전·강하 사다리) · **GF(8) 일반곱+RS(7,3)**(인코더 subspace 상환·거리-5 MDS) ·
  **Schur sampling**(디코더·대칭 반사자 2P−I·Dicke |D⁴₂⟩) · **MUB shadow 측정측**(V_b†·frame channel) ·
  **stabilizer-rank 제5 검증경로**(130앱 재검증) · **[[8,3,2]] triorthogonal + 첫 비-Clifford 횡단
  논리 CCZ**.

### 3g. ★v5 회신 소비분 — 통합 5축 (이번 라운드 신규 — 재제안 금지)
- **정확해 동역학(P1)**: du_gate_j8(V=iSWAP†·e^{−iπ/8·ZZ}, 비-Clifford dual-unitary)·6q PBC 브릭워크·
  floquet4_uf(CZ링+T킥) — 광원뿔 상관 두 경로(오프레이 전소멸+전달채널 닫힌형)·quasi-energy 관측.
  (**일반 DU 게이트 family·OTOC/스크램블링 witness·2D DU·Floquet SPT 불변량은 아직 없음.**)
- **magic 자원 exact 증명서(P2)**: ξ(|T⟩)=4−2√2·ξ(|T⟩^⊗2)=24−16√2 완전 증명서(primal+dual+격차0,
  ℚ(√2) 정확산술)·ξ(|CS⟩) bounded [8/5,(11+2√10)/9]·R(|T⟩)=√2·T-count 하한 인증(magic_a≥1·
  magic_cs≥3 타이트)·★**T⊗T↛CS Clifford 변환 불가 판정**(F 불변량 — closed-negative급).
  (**n≥3 최적성·robustness 일반화·동적(채널) 자원·catalysis 정량은 아직 없음.**)
- **★Gaussian/matchgate 제6 검증경로(P3)**: plan→Majorana R∈SO(2n) 독립 컴파일 vs golden 켤레
  두 경로·진공 행렬식·커버리지 판정기 + gauss_hop4/braid3(비-Clifford Gaussian 데모).
  (**pairing(비수보존) 게이트·일반 진폭 Pfaffian 공식·2D free-fermion 은 아직 없음.**)
- **RM [[15,1,3]] + transversal T(P4)**: rm15_encoder_t2(★완전 논리-입력 인코더, 모듈 90 —
  7번째 Tier-2)·rm15_tt(T^⊗15==논리 T†, mod-8 정수 witness)·거리-3 전수 — 15-to-1 기판.
  triorthogonal 계보: [[8,3,2]](d2·CCZ)→[[15,1,3]](d3·T).
  (**15-to-1 증류 프로토콜 회로(측정 전 coherent)·code switching·d≥5 부호·색부호 d3 는 아직 없음.**)
- **매듭 심화(P5)**: fib_yb/word5/fig8(첫 비-토러스 매듭, σ⁻¹=z5³)·★TL₃ 상태합 제3 Jones 경로·
  연결합 곱법 exact·amphichiral 1−√5·Alexander 정수 제3불변량(Burau)·반꼬임≅F 재발견.
  (**HOMFLY 특수점·≥5교차 family·2-bridge 일반·Khovanov류 는 아직 없음.**)

### 3h. v5 예비 판정분 (재제안 시 보강 조건 명시)
- **Code switching [[8,3,2]]↔Steane**(2/8): coherent isometry 로 재정식화 필요(측정 본질 분리).
- **A₄ 비아벨 Fourier**(2/8): ★ζ₃(2π/3)는 기존 각도 격자 밖 — 신규 module 사람게이트 필요
  (field ℚ(√−3) 차수 2 — 승인 요건 갖춰 제안하면 게이트 상정 가능).
- **RS/BCH 가역 복호기**(1/8): BM/Chien/Forney 의 uncompute 설계를 소형 코어로 분해해 재제안.
- **d=3 surface+surgery·bosonic/permanent·RSK 조합론·정수 나눗셈**(각 1/8): 구체 인스턴스·오라클
  경로·복리 접점 강화 시 재평가.

**핵심: 위 축들의 사소한 변형은 원치 않는다. 질적으로 새로운 계층을 제안하라.**
괄호의 "아직 없음"이 *질적 새 축*의 관문이면 환영한다.

---

## 4. 우리가 원하는 것

§1·§5 를 지키면서 **§3에 없는 새로운 수평 축**. 방향 감(강요 아님):

- **증류 프로토콜 층** — 15-to-1 의 측정 전 coherent 회로(기봉인 rm15 소비)·[[5,1,3]] 5-to-1 과의
  파이프라인·acceptance 사영자 exact.
- **동적 자원 이론** — 채널의 magic 생성능력·catalysis 정량(기봉인 t_teleport 촉매 소비)·
  자원 증명서의 회로-수준 인증 확장.
- **비아벨/표현론 심화** — A₄(게이트 요건 명시) 또는 **정수 표현만으로 닫히는 새 군**·모듈러 표현·
  Hecke 대수 인스턴스.
- **free-fermion 심화** — pairing(Bogoliubov) 게이트의 닫힌형 각도 제안(제6 경로 확장)·Kitaev chain
  위상 witness·2D 인스턴스.
- **동역학 심화** — OTOC/스크램블링 exact witness(기봉인 DU 소비)·Floquet 위상 불변량 정수 산출·
  dual-unitary 2D 브릭워크.
- **부호 심화** — code switching coherent 판·d=3 색부호·양자 BCH.
- **검증 메타** — 제7 경로(SMT/symbolic·텐서망 수축 인증)·회로 동치 증명서 자산화·T-count 상한 인증.
- 그 밖에 **당신이 더 나은 축을 알면 그것을 제안하라.**

## 4′. ★성공 패턴 힌트 (v1→v6 구현에서 배운 것)

**(a) 게이트 우회**: dyadic 선택·군 재선택·재해석·부분공간 임베딩. **(b) 직접 닫힌형 구성**(탐색 금지):
"이 구조 때문에 각도가 exact 로 떨어진다"는 수학 근거 필수. **(c) 승인-module 사람게이트**: 신규 각도/
대수체는 닫힌형 공시 + π-free surd 우대로 승인 가능(ℚ(ζ₅,√φ) 선례). **(d) v4**: 반증→회수·자유도
재도출·sub-app 수직 복리. **(e) v5**: 기소비 선점 대조(시차 강건 novelty)·교차 트랙 복리·게이트 구조
회피·인프라 즉시 소비.

**(f) ★v6 신규 패턴 4개**:
- **다중 독립 경로 대조**: 매듭 불변량을 가중 trace·TL 상태합·skein·Alexander(Burau 정수) **3~4중**으로
  대조했다 — 같은 값의 서로 다른 수학이 많을수록 witness 가 강하다. 제안에 "이 값을 몇 개의 독립
  수학으로 재계산할 수 있는가"를 명시하라.
- **Tier-2 드라이버**: 각도 무관 Clifford 대형 자산(n>12)은 dense 불가여도 **정준 stabilizer tableau
  모듈 봉인**(rm15 선례 — 15q 완전 인코더)이 정식 경로다. 심볼릭 안정군 전파가 dense-free witness.
- **주기성 역원 회피**: 역생성원이 필요한 word 는 게이트 주기성으로 해소된다(σ⁻¹=z5³, z5¹⁰=I).
  "역원 module 필요" 판정 전에 주기·켤레 구조를 스캔하라.
- **오라클 동치 재발견**: up-to-phase 정준 u_hash 가 자산 간 숨은 동치를 자동 판정한다(반꼬임
  σ₁σ₂σ₁ ≅ F-move 가 동일 u_hash 로 드러남) — 제안 자산이 기존 자산과 동치일 가능성을 예보하라.

## 5. 반드시 지켜야 할 제약

- **결정론 불가침** — byte-identical 재봉인. 동결 합의 키·오라클 지문 파일 재생성/수정 금지.
- **오라클은 사용만** — `verify_seal.py`/`contracts.py` 재구현 금지.
- **honest decomposition** — `MatrixGate`/정답-행렬 shortcut 금지.
- **self-contained** — 벤더된 오라클 외 외부 서비스 의존 금지. **하드웨어 out**.
- **정직 경계** — 근사·확률·측정후처리는 봉인 아니라 **관측**. exact ≠ 근사, dense ≠ structural ≠
  subspace ≠ tableau. 상태준비 app 은 정의 열만 물리.
- **★registry 실측 novelty**: 공개 저장소 **https://github.com/sadpig70/QuantaFoundry**
  (`registry/`·`specs/`·`scripts/` 전부 공개) — 접근 가능한 런타임은 실측 대조를 우대한다
  (v4 에서 실측한 회신이 최고 채택률). 접근 불가하면 §3 정독 + **구조적("계층 부재") novelty** 서술로
  충분하다(§4′(e) 시차 강건성 — 회신 시점과 소비 시점 사이에 자율 트랙이 선점할 수 있음).

## 6. 답변 형식 (제안마다)

**3~5개**를 impact×feasibility 순으로: 1. **proposal**(축 한 줄 + 구체 작은 인스턴스) ·
2. **rationale**(정체성·compounding·교차 복리 접점) · 3. **feasibility**(봉인 게이트 조립·오라클 검증
대상·**§4′(b) exact 수학 근거**·필요 시 §4′(c) 게이트 요건 명시 — 단 §4′(e)(f) 회피 먼저) ·
4. **risk**(실패 모드·정직 경계) · 5. **novelty**(§3 특히 **3g/3h** 명시 대조 + 시차 강건성).

## 7. 개념 미니 용어집

- **봉인(seal)**: 오라클이 회로 == golden 을 확인하고 registry 영구 기록(byte-identical 재현).
- **compounding**: 봉인 자산의 부품 재사용(sub-app)·신뢰 자본 복리.
- **honest boundary**: exact 봉인 vs 관측(근사/확률/측정)의 명시 구분 · **teeth**: 오염이 검출됨을 실증.
- **subspace 강검증**: 계산기저 순열의 독립 정수 대조 · **Tier-2**: 정준 tableau(임의 크기 Clifford).
- **closed-negative**: 불가능성의 하한/정리 확정 — 반증 문서도 1급 산출(2q 2-design·T⊗T↛CS 선례).
- **검증경로 6**: dense·tableau·ZX·path-sum ℤ[ω₈]·stabilizer-rank·matchgate/SO(2n) — 제7을 환영한다.
