<!-- QuantaFoundry 수평 확장 아이디어 제안 요청 — v5 (2026-07-07). v1/v2/v3/v4 후속. self-contained. -->
<!-- 외부 모델 런타임에게 전달용. 이 문서 하나만 읽고 제안 가능하도록 작성됨. -->

# QuantaFoundry — 수평적 확장(Horizontal Expansion) 아이디어 제안 요청 · v5

> **v4 → v5 변경점**: v4 요청으로 8개 런타임의 제안(35개)을 받아 **기소비 선점 대조 → 13클러스터 →
> 통합 6축(P1~P6) + 최우선 예비 1건(R2)을 전부 자율 완주**했다 — **사람게이트 0·신규 module 0**으로:
> Fibonacci 소비층(F-move·매듭 word·Jones 두 독립경로) · C₃ 대각 phase-polynomial 정규형 ·
> GF(8) 체 완결+RS(7,3)(★첫 비-Shor subspace 상환) · Schur sampling 알고리즘화(디코더·반사자·Dicke) ·
> MUB shadow 측정측 · **stabilizer-rank 제5 독립 검증경로(봉인 130앱 재검증)** ·
> **[[8,3,2]] triorthogonal 첫 비-Clifford 횡단 논리 CCZ**. 전부 §3 EXCLUDE 에 **추가**했다(§3e).
> §4′에 v5 에서 배운 새 성공 패턴 4개(★**기소비 선점 대조·교차 트랙 복리·게이트 구조 회피·인프라 즉시
> 소비**)를 추가했다. 이제 **그 너머의 새 축**을 구한다.

---

## 1. 프로젝트 정체성 (제안의 유효성을 규정 — 먼저 읽어라)

QuantaFoundry 는 **미래의 완전한 결함허용 양자컴퓨터(FTQC/QPC)가 실현될 때 쓸 소프트웨어 자산을 지금
미리 축적**하는 파운드리다. AI 가 회로를 생성하고, **결정론적 오라클(QPGF)이 byte-identical 재봉인으로
검증**하며, 봉인을 통과한 것만 registry 에 영구 보존된다.

- 하드웨어 실행은 **의도적으로 범위 밖**(노이즈·QPU·실행증거 없음). 봉인 = **이상적 수학적 진실**(exact
  유니터리/구조). 신뢰의 근거는 봉인 시점의 **결정론 + 수학적 독립검증**뿐이다.
- 따라서 좋은 제안 = **작은 인스턴스가 Tier-0 EXACT 로 봉인 가능**하고, **오라클로 독립 검증 가능**하며,
  **compounding(one seal → many algorithms)**이 크고, FTQC 정체성에 부합하는 **질적으로 새로운 축**.

## 2. "수평적(Horizontal)" 확장의 정의

- **수평** = 새로운 **추상화 계층·대수 구조·알고리즘 클래스**. (다른 파라미터·더 큰 인스턴스 = 수직, 원치 않음.)
- 봉인 단위: `module`(기본 게이트) 위에 `app`(합성 회로)을 조립 — 이상적으로 **새 module 0**(기존 팔레트
  재사용)로 새 app 을 만든다. Tier: 0 EXACT(dense, n≲12) · 1 STRUCTURAL(Merkle) · 2 CLIFFORD(tableau).

## 3. EXCLUDE — 이미 구현·봉인된 것 (재제안 금지)

현재 **89 modules / 370 sealed apps** (root `9b5964fa…`). **독립 검증경로 5개**
(dense · Clifford tableau · ZX · path-sum ℤ[ω₈] · stabilizer-rank 분해). 카테고리:

### 3a. v1 이전 (기존 자산)
- **기초 상태/게이트**: Bell, GHZ(≤16 부분검증·GHZ-9 encoder), cluster/ring/W-state(w3~w10), 표준 1·2·
  다중제어 게이트(X/Z/H/S/T/√X, CNOT/CZ/Toffoli/Fredkin/iSWAP, c3x…c12x), 회전/위상(Rz/Rx/Ry 특정각·controlled-Rk).
- **QFT 계열**: QFT(2–8)·역QFT·QPE·amplitude estimation(QAE).
- **검색/증폭**: Grover·diffusion·reflection·amplitude amplification.
- **Hamiltonian 시뮬레이션**: TFIM/Heisenberg Trotter·2차 Suzuki·4차 Yoshida-Suzuki·Pauli-지수 회전(rxx/ryy/rzz).
- **변분**: VQE(다층 hardware-efficient)·QAOA(MaxCut)·parameter-shift gradient(관측).
- **쿼리 알고리즘**: Deutsch-Jozsa·Bernstein-Vazirani·Simon·quantum walk(C4/C8 coined).
- **QEC**: repetition·syndrome·Shor-9 encoder·Steane/stabilizer-tableau(Tier-2)·transversal 논리 Clifford(H/S/CNOT).
- **Shor**: 15=3×5·진짜 21=3×7·distinct-prime structural frontier(shor69…shor3683, 부분공간 순열 강검증)·
  modular multiplier(cmul) 자동 factory.
- **QSVT/block-encoding(완비)**: LCU block-encoding·QSP·QSVT 다항식 변환·consumer trilogy.
- **Fermionic**: Jordan-Wigner 완비 + Bravyi-Kitaev/parity 인코딩·tapering·fermionic SWAP.
- **분자/data-oracle/FTQC/비아벨/qudit**: H₂ dyadic LCU · qROM+SELECT-PREPARE · magic state+[[5,1,3]]
  graph-code 증류 코어+논리 T-injection · S₃/D₄ 비아벨 군 오라클+D₄ Fourier+HSP 1-shot coset ·
  큐트릿 qubit-임베딩 삼진 산술.
- **채택/경화**: OpenQASM3 export/ingest(round-trip 335)·CLI·citable root·독립 2차 오라클·규약-독립성·
  oracle revocation·ed25519·CI seal-gate·발견 superoptimization.

### 3b. v2 구현
- **위상적 논리연산**: [[4,2,2]] surface-type encoder·lattice surgery coherent 병합·2×2 토릭 ground state.
  (**d=3 surface·defect braiding·15-to-1 은 아직 없음.**)
- **MBQC**: 3×3 클러스터 자원상태·측정패턴↔회로 등가. (**gflow 일반론은 아직 없음.**)
- **Anyon braiding(Ising)**: ising_braid_b2(Majorana B₂, Clifford).
- **QCA**: Clifford brickwork·GNVW 관측. (**non-Clifford QCA·Floquet 위상은 아직 없음.**)

### 3c. v3 소비분
- **Z₂ 격자 게이지**: z2gauge3. (**U(1)/SU(2)·plaquette 동역학·2+1D 는 아직 없음.**)
- **ZX-calculus 검증경로**(3번째) · **qLDPC**: [[8,1,2]] 하이퍼그래프곱 encoder.
- **Schur-Weyl**: schur3(직접 CG cascade, 승인 module ry_cg_half±) · **텐서망(MPS)**: aklt4.
- **열린 양자계(CPTP)**: Stinespring dilation family(bitflip/phasedamp/ampdamp/depol·¼ family·합성 격자)·
  채널→QEC 파이프라인 관측·Choi 상태 4종. (**일반 감쇠율 연속족·correlated 채널·GKP 는 아직 없음.**)
- **unitary design**: 1q Clifford 24원소(정확 2/3-design) · **2q 소형 unitary 2-design =
  closed-negative(하한 226)** — 재제안 금지.
- **명시적 양자 산술**: cuccaro/draper/비교기(ripple==Fourier 교차). (**나눗셈/제곱근·carry-lookahead 없음.**)
- **Szegedy walk**: 2-state·C₄·p=¼ 비대칭. · **Path-sum ℤ[ω₈] 4번째 검증경로** · **PEPS**: peps22_rvb.
- **MUB-20 state 2-design**(준비 20앱) · **UD-POVM Naimark** · **Schur n=4**(schur4) ·
  **Fibonacci braid 생성원**(σ₁/σ₂, 승인 대수체 ℚ(ζ₅,√φ)·module z5_gate/ry_fib).

### 3d. v3 잔여·자체개창 소비분
- **1-flag FT 증후 추출**: flag_synd_zzzz/xxxx(w4 stabilizer, symbolic Pauli propagation witness).
- **GF(8) 역원·Frobenius**: gf8_inv(Fermat a⁶)·gf8_frob(+gf4_mul/frob·gf8_mulx 기존).
- **Clifford 계층 실현층**: t_teleport/s_teleport — measurement-free **coherent gate teleportation 촉매**
  (U(|ψ⟩⊗|A⟩)=(T|ψ⟩)⊗|A⟩, 자원 보존)·계층 판정 C₁⊂C₂⊂C₃ witness·보정 사다리.

### 3e. ★v4 회신 소비분 — 통합 6축 + 예비 R2 (이번 라운드 신규 — 재제안 금지)
- **Fibonacci 소비층(P1)**: fib_fmove(F=ry_fib·z 1급 승격)·매듭 braid word 4(σ₁²/σ₁³/σ₁⁴/σ₁³σ₂)·
  **Jones 다항식 두 독립경로 관측**(양자 가중 trace (d₁,d_τ)=(1,φ) vs 고전 skein 재귀, t=e^{−2πi/5},
  Markov 소멸 witness). (**임의 링크 일반화·braid weave 컴파일·n≥4 fusion tree·controlled-braid
  Hadamard test 는 아직 없음.**)
- **C₃ 대각 phase-polynomial 정규형(P2)**: c3_diag_ladder3/full3(ℤ₈ 위상다항식, T/CS/CCZ 사전)·
  강하 사다리 두 경로(행렬 켤레 vs Δf 정수 다항)·semi-Clifford 인자화 witness·컴파일러 항등 관측.
  (**비대각 C₃ 일반론·C₄+ 탑·T-count 최적 합성은 아직 없음.**)
- **GF(8) 체 완결 + RS(7,3)(P3)**: gf8_mul(일반곱)·rs_synd_core·**rs73_encoder(21q Tier-1 STRUCTURAL +
  subspace 상환 — 첫 비-Shor)**·거리-5 MDS 전수 관측. (**BCH·복호(Berlekamp-Massey) 가역 코어·
  GF(2ᵏ) k≥4·quantum RS 부호는 아직 없음.**)
- **Schur sampling 알고리즘화(P4)**: schur3_dag/schur4_dag(디코더=sampling 실행 방향)·
  schur_reflect4(대칭 부분공간 반사자 2P−I)·dicke4_k2(=[x,x,schur4] — Dicke family 완비)·
  스펙트럼 샘플링 두 경로 관측. (**n≥5·spectrum estimation 프로토콜화·quantum majority vote 는 아직 없음.**)
- **MUB shadow 측정측(P5)**: mub4_meas_b2~b5(premeasurement V_b†)·frame channel M(ρ)=(ρ+I)/5·
  역재구성·Bell Pauli 회복 유리 exact. (**유한샘플 shadow(median-of-means)·다큐빗(n≥3) shadow·
  derandomization 은 아직 없음.**)
- **★stabilizer-rank 제5 독립 검증경로(P6)**: 비-Clifford 대각의 Clifford-합 분기 전개(T/CS/CT 2분기·
  CCZ/CCCZ 4분기) + 아핀 지지대·ℤ₄ 이차형식 엔진(행렬곱 무사용) — **봉인 130앱 재검증**. (**χ-최적
  분해(BSS)·6번째 경로(matchgate/SO(2n) 피복 등)·T-count 상한 인증은 아직 없음.**)
- **★[[8,3,2]] triorthogonal + 첫 비-Clifford 횡단 논리 게이트(R2)**: code832_encoder(정육면체 CSS)·
  code832_tccz(⊗T^{±1} → 논리 CCZ, triorthogonality 정수 witness (0,0,1)·논리행렬 exact·거리-2).
  (**RM [[15,1,3]]·정준 15-to-1 증류·d≥3 색부호·code switching 은 아직 없음.**)

### 3f. v4 예비 판정분 (재제안 시 보강 조건 명시)
아래는 v4 회신에 있었으나 **사유와 함께 보류**된 축 — 재제안하려면 보강 조건을 충족하라:
- **MBQC gflow 컴파일러**(2/8): '일반론 컴파일러'가 인스턴스 봉인 원칙과 긴장 — **구체 인스턴스 재정식화** 필요.
- **U(1) 양자 링크 모델**(2/8): Gauss projector 비유니터리 — **봉인 대상(유니터리)·witness(투영) 분리 설계** 필요.
- **qRAM bucket-brigade**(1/8)·**matchgate SO(2n) witness tier**(1/8)·**qutrit-native Clifford**(1/8):
  저합의 — 구체 인스턴스·오라클 경로·복리 접점을 강화해 재제안하면 재평가.
- **GF(4) [[5,1,3]] decoder·flag 혼합-Pauli(XZZXI)**: 핵심이 기소비 — 잔여 델타의 신규성을 명시하라.

**핵심: 위 축들의 사소한 변형은 원치 않는다. 질적으로 새로운 계층을 제안하라.**
단 괄호의 "아직 없음" 항목이 *질적으로 새 축*을 여는 관문이면 환영한다.

---

## 4. 우리가 원하는 것

§1·§5 를 지키면서 **§3에 없는 새로운 수평 축**. 작은 인스턴스가 Tier-0 EXACT 봉인 가능·compounding 큰 것.
방향 감을 위한 예시(강요 아님):

- **자원 이론(resource theory)의 exact 코어** — magic 단조량(stabilizer extent/robustness)의 소형 exact
  산출 witness·상태 변환 가부의 정수 판정 — 제5 경로(stabilizer-rank 엔진)가 이미 있어 소비 가능.
- **부호 심화** — RM [[15,1,3]]+transversal T(정준 15-to-1 기판)·code switching([[8,3,2]]↔Steane)·
  d≥3 색부호 — [[8,3,2]]·Steane·qLDPC·RS(7,3) 가 기봉인이라 복리 접점이 많다.
- **매듭/위상 심화** — 봉인 Jones 두 경로 위의 새 층(HOMFLY 특수점·2-bridge 링크 family·Burau/Temperley-
  Lieb 표현의 exact 산술) — 대수체 ℚ(ζ₅,√φ) 승인·braid word 자산 기봉인.
- **표현론 심화** — dihedral HSP 완결(1-shot 기봉인 소비)·S₅/A₄ 등 새 군의 오라클+Fourier·
  Kostka/plethysm 류 조합 산술의 가역 코어.
- **동역학 새 클래스** — Floquet 위상(주기 구동 exact 스텝)·non-Clifford QCA·dual-unitary 회로의
  exact 상관함수 witness.
- **검증 메타 확장** — 6번째 독립 경로(matchgate/Pfaffian·SMT/symbolic)·T-count 하한 인증·
  회로 동치의 증명서(certificate) 자산화.
- 그 밖에 **당신이 더 나은 축을 알면 그것을 제안하라.**

## 4′. ★성공 패턴 힌트 (v1→v5 구현에서 배운 것 — 참고용)

**(a) 게이트 우회 (v1)**: dyadic 계수 선택·군 재선택·코드=그래프 재해석·부분공간 임베딩·exact-핵심 분리.

**(b) 직접 닫힌형 구성 (v3 — 탐색 금지 원칙)**: ansatz 탐색은 실패했고 **수학적 직접 유도**가 성공했다.
→ "이 닫힌형 구조 때문에 각도/계수가 유리수·dyadic 으로 떨어진다"는 **수학적 근거**를 제시하라.

**(c) 승인-module 사람게이트**: 신규 module 은 완전 금지가 아니라 **사람 승인 게이트**다. 지금까지 승인:
ry_cg_half±·ry_ak41/13/7±·ry_pi6±·z5_gate/ry_fib(새 대수체 ℚ(ζ₅,√φ)). 조건: exact analytic golden·
독립 2차 오라클 구성 가능(π-free surd 우대)·frozen 무훼손·최소 개수.

**(d) v4 패턴**: 반증→회수(closed-negative 도 1급 산출)·자유도 재도출(Kraus/게이지)·sub-app 수직 복리.

**(e) ★v5 신규 패턴 4개**:
- **★기소비 선점 대조**: v4 회신 35제안 중 4건(flag 증후·GF(8) 역원·gate teleportation·Dicke k=1=W₄)이
  **회신 작성 시점과 소비 시점 사이에 자율 트랙이 이미 봉인**한 것이었다. 회신 기준선(§3 의 root)과
  실제 소비 시점 registry 는 다를 수 있다 — **제안이 이 시차에 강건하도록 novelty 근거를 구조적으로**
  (앱 이름 나열이 아니라 "이 계층 자체가 없다"로) 써라.
- **교차 트랙 복리**: C₃ phase-poly 사전(P2)이 곧바로 Schur 반사자의 D-word(P4)가 됐다 — 제안들이
  서로의 부품이 되는 **묶음 제안** 우대.
- **게이트 구조 회피**: "신규 각도 필요" 판정 전에 구조를 재검토하라 — Dicke |D⁴₂⟩ 는 ry_sqrt23 승인
  없이 **schur4|1010⟩ 3스텝**으로 나왔고(Schur 벡터=Dicke), F-move 는 ry_fib·z 로 이미 분해돼 있었다.
- **인프라 즉시 소비**: 제5 검증경로(P6)는 그 커밋 다음 봉인([[8,3,2]] T-패턴)을 **자동 커버**했다.
  검증 인프라 제안은 "어떤 기봉인/미래 자산이 즉시 수혜하는가"를 명시하면 강하다.

## 5. 반드시 지켜야 할 제약

- **결정론 불가침** — byte-identical 재봉인. 동결 합의 키·오라클 지문 파일 재생성/수정 금지.
- **오라클은 사용만** — `verify_seal.py`/`contracts.py` 재구현 금지(해시가 봉인에 baked).
- **honest decomposition** — `MatrixGate`/정답-행렬 shortcut 금지. 실제 회로 분해로 조립.
- **self-contained** — 벤더된 오라클 외 외부 서비스/스킬 의존 금지.
- **하드웨어 out** — QPU/노이즈/실행-증거 축은 대상 아님.
- **정직 경계** — 근사·확률·측정후처리는 봉인 아니라 **관측**으로 명시. exact ≠ 근사, dense ≠ structural
  ≠ subspace, 결정론 재현 ≠ 정확성. 상태준비 app 은 정의 열만 물리.
- **★registry 실측 기반 novelty 자체 정정** — §3 정독 + 자기 제안이 EXCLUDE 와 겹치지 않음을 명시
  검증하라(§4′(e) 시차 강건성 포함). v4 에서 이를 수행한 회신(A8)이 가장 높은 채택률을 기록했다.

## 6. 답변 형식 (제안마다)

**3~5개**를 impact×feasibility 순으로. 각 제안:

1. **proposal** — 새 수평 축 한 줄 + 무엇을 봉인할지(구체적 작은 인스턴스).
2. **rationale** — 왜 지금 가치 있는가(정체성 부합·compounding·교차 복리 접점).
3. **feasibility** — 작은 인스턴스가 Tier-0 EXACT 봉인 가능한가? 어떤 봉인 게이트로 조립되나? 오라클로
   무엇을 검증하나? **§4′(b) 처럼 각도/계수가 exact 로 떨어지는 수학적 근거를 제시.** 신규 module 필요
   시 §4′(c) 형식으로 닫힌형 각도·개수·field 명시(단 §4′(e) 게이트 구조 회피를 먼저 시도).
4. **risk** — 실패 모드·정직 경계(무엇이 근사/관측, 무엇이 exact).
5. **novelty** — §3 EXCLUDE(특히 **3e/3f**)와 **명시적으로 대조** + 시차 강건성(§4′(e)).

## 7. 개념 미니 용어집

- **봉인(seal)**: 오라클이 회로 조립품 == golden 유니터리를 확인하고 registry 에 영구 기록.
- **compounding**: 봉인 자산을 부품으로 재사용해 새 app 을 새 module 0 으로 조립(신뢰 자본 복리).
- **honest boundary**: exact 봉인과 관측(근사/확률/측정)의 명시적 구분 — 과대주장 금지.
- **subspace 강검증**: dense 대신 계산기저 순열을 독립 정수산술로 대조(rs73·shor ladder).
- **witness 관측**: 봉인 자산의 수학 성질을 독립 경로로 검증하되 봉인으로 주장하지 않는 계층(teeth 포함).
- **closed-negative**: 목표 불가능성을 하한/정리로 확정하고 반증 문서를 1급 산출물로 남기는 정직 종결.
- **제5 검증경로**: dense·tableau·ZX·path-sum 에 이은 stabilizer-rank 분해 재검증(Clifford-합 분기 +
  아핀/이차형식 진폭 — 봉인 130앱 커버).
