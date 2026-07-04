<!-- QuantaFoundry 수평 확장 아이디어 제안 요청 — v3 (2026-07-04). v1/v2 후속. self-contained. -->
<!-- 외부 모델 런타임에게 전달용. 이 문서 하나만 읽고 제안 가능하도록 작성됨. -->

# QuantaFoundry — 수평적 확장(Horizontal Expansion) 아이디어 제안 요청 · v3

> **v2 → v3 변경점**: v2 요청으로 8개 런타임의 제안(23개)을 받아 **통합 6축(P1–P6) + 사람게이트 4축(T1–T4)
> + AKLT(V4)** 를 전부 봉인 구현했다 — 위상적 논리연산(surface/lattice surgery/toric)·MBQC·GF(2ᵏ) 유한체·
> Ising/Majorana braid·Clifford QCA·fermionic swap·Z₂ 격자 게이지·ZX 3차 검증경로·qLDPC 하이퍼그래프곱·
> **Schur-Weyl 변환·AKLT 텐서망 상태준비**. 그 전부를 §3 EXCLUDE 에 **추가**했다. 이제 **그 너머의 새 축**을 구한다.
> §4′에 v2/v3 구현에서 배운 **"직접 닫힌형 구성" 성공 패턴**과 ★**승인-module 사람게이트 프로세스**(신규
> module 이 완전 금지에서 "승인 게이트"로 진화)를 추가했다.

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

현재 **85 modules / 209 sealed apps** (root `3790e617…`). 카테고리:

### 3a. v1 이전 (기존 자산)
- **기초 상태/게이트**: Bell, GHZ(≤16 부분검증·GHZ-9 encoder), cluster/ring/W-state, 표준 1·2·다중제어
  게이트(X/Z/H/S/T/√X, CNOT/CZ/Toffoli/Fredkin/iSWAP, c3x…c12x), 회전/위상(Rz/Rx/Ry 특정각·controlled-Rk).
- **QFT 계열**: QFT(2–8)·역QFT·QPE·amplitude estimation(QAE).
- **검색/증폭**: Grover·diffusion·reflection·amplitude amplification.
- **Hamiltonian 시뮬레이션**: TFIM/Heisenberg Trotter·2차 Suzuki·4차 Yoshida-Suzuki·Pauli-지수 회전(rxx/ryy/rzz).
- **변분**: VQE(다층 hardware-efficient)·QAOA(MaxCut)·parameter-shift gradient(관측).
- **쿼리 알고리즘**: Deutsch-Jozsa·Bernstein-Vazirani·Simon·quantum walk(C4/C8 coined).
- **QEC**: repetition·syndrome·Shor-9 encoder·Steane/stabilizer-tableau(Tier-2)·transversal 논리 Clifford(H/S/CNOT).
- **Shor**: 15=3×5·진짜 21=3×7·distinct-prime structural frontier(shor69…shor3683)·modular multiplier(cmul)·부분공간 순열 강검증.
- **QSVT/block-encoding(완비)**: LCU block-encoding·QSP(d 1/3/5)·QSVT 다항식 변환·consumer trilogy(Ham-sim·amp-amp·matrix inversion).
- **Fermionic**: Jordan-Wigner(반교환·hopping·number·t-V·spinful Fermi-Hubbard) + **Bravyi-Kitaev/parity**
  인코딩·tapering·**fermionic SWAP**.
- **분자/data-oracle/FTQC/비아벨/qudit (v1 6축)**: H₂ dyadic LCU block-encoding · qROM+SELECT-PREPARE ·
  magic state+[[5,1,3]] graph-code 증류 코어+논리 T-injection · S₃/D₄ 비아벨 군 오라클+D₄ Fourier+이면군
  HSP 표본화 · 큐트릿 qubit-임베딩 삼진 산술.
- **채택/경화**: OpenQASM3 export/ingest·CLI·citable root·독립 2차 오라클·규약-독립성·oracle revocation·ed25519·CI seal-gate·발견 superoptimization.

### 3b. ★v2 구현 (P1–P6 — 재제안 금지)
- **위상적 논리연산**: `surf422_encoder`([[4,2,2]] surface-type CSS)·`surf_ls_merge_zz`(lattice surgery
  coherent Z_L⊗Z_L 병합, deferred-측정 우회)·`toric22_gs`(2×2 토릭 ground state, 위상질서/호몰로지)·완전
  FTQC 논리스택 관측(magic→증류→논리T→논리큐빗→surgery). (**d=3 surface·defect braiding·color code·15-to-1 은 아직 없음.**)
- **MBQC**: `cluster3x3_prep`(2D 자원상태)·`mbqc_h`(측정패턴↔회로 coherent 등가). (**gflow 일반론은 아직 없음.**)
- **GF(2ᵏ) 유한체**: `gf4_mul`·`gf4_frob`(Frobenius)·`gf8_mulx`(primitive orbit). 군≠체 구분 실증.
  (**GF(2ᵏ) 역원·다항식 인수분해·Reed-Solomon 류 부호 산술은 아직 없음.**)
- **Anyon braiding**: `ising_braid_b2`(Majorana B₂, Yang-Baxter 검증, Ising=Clifford).
  (**Fibonacci(황금비 위상=게이트)·Jones 다항식·braiding universality 는 아직 없음.**)
- **QCA**: `qca_step`(Clifford brickwork, 병진불변, GNVW/light-cone 관측, exact≠Trotter).
  (**non-Clifford QCA·Floquet 위상은 아직 없음.**)

### 3c. ★v3/V4 구현 (이번 세션 — 재제안 금지)
- **Z₂ 격자 게이지 이론**: `z2gauge3`(1+1D Kogut-Susskind, Gauss law 게이지불변 encoder, H 켤레→반복부호).
  (**U(1)/SU(2)·plaquette 동역학·2+1D·Higgs 상은 아직 없음.**)
- **ZX-calculus 검증경로**: `zx_verify`(Clifford fragment rewrite, dense/tableau 에 이은 **3번째 독립
  오라클 경로**, 봉인 아님·검증 인프라). (**Clifford+T 완전성·다른 형식적 검증(SMT/범주론)은 아직 없음.**)
- **qLDPC**: `qldpc_hgp`([[8,1,2]] 하이퍼그래프곱 CSS encoder, 고전 [3,1]×[2,1]→양자).
  (**더 큰 qLDPC 는 dense 벽 → Tier-2 tableau 경로가 승인돼 있음. decoder 는 범위 밖.**)
- **Schur-Weyl 변환**: `schur3`(3-qubit, 직접 CG cascade, U†J²U·U†JzU 동시대각 + S₃ duality sector 보존
  witness, 승인 module ry_cg_half±). (**n≥4 Schur·S_n irrep 레지스터 명시 분리·quantum Schur sampling
  알고리즘화는 아직 없음.**)
- **텐서망 상태준비(MPS)**: `aklt4`(4-site spin-1 AKLT VBS, OBC norm²=41/81, 순차 조건화 등척, 독립 MPS
  수축 exact + parent-H P⁽²⁾ 소멸 witness, 승인 module ry_ak41/13/7±). (**PEPS·MERA·n>4/PBC·bond>2
  일반 MPS 템플릿은 아직 없음.**)

**핵심: 위 축들의 사소한 변형(사이트 수 늘리기·다른 소군·다른 소형 코드 하나 더)은 원치 않는다. 질적으로
새로운 계층을 제안하라.** 단 괄호의 "아직 없음" 항목이 *질적으로 새 축*을 여는 관문이면 환영한다.

---

## 4. 우리가 원하는 것

§1·§5 를 지키면서 **§3에 없는 새로운 수평 축**. 작은 인스턴스가 Tier-0 EXACT 봉인 가능·compounding 큰 것.
방향 감을 위한 예시(강요 아님):

- **열린 양자계 계층** — CPTP 채널의 Stinespring/유니터리 확장(dilation) exact 봉인(dyadic 감쇠각 선택),
  채널 합성·Kraus 구조. (우리는 유니터리만 있고 **채널 계층이 없다**.)
- **무작위성/설계(designs)** — 정확 unitary 2-design(Clifford 군 구조)·상태 t-design 의 결정론적 준비·
  검증 witness. (pseudo-randomness 의 exact 코어.)
- **Markov 연쇄/Szegedy 걷기** — 이분 반사 구조의 quantized walk(작은 유리수 전이확률), coined walk 와
  질적으로 다른 spectral gap 증폭 계층.
- **Clifford 계층구조(3rd level)** — T 를 넘는 semi-Clifford/diagonal 계층 게이트의 구조적 자산화
  (gate teleportation 소비 연결).
- **양자 산술 심화** — Draper QFT-가산기·Cuccaro ripple-carry·비교기 등 **명시적 가산기 클래스**
  (cmul 내부에 숨은 산술을 1급 자산으로).
- **표현론 알고리즘화** — dihedral HSP full pipeline·quantum Schur sampling(우리 schur3 소비).
- **형식 검증 확장** — SMT/symbolic proof·path-integral(sum-over-paths)·stabilizer-rank 기반의
  4번째 독립 검증 경로.
- 그 밖에 **당신이 더 나은 축을 알면 그것을 제안하라.**

## 4′. ★성공 패턴 힌트 (v1→v3 구현에서 배운 것 — 참고용)

**(a) 게이트 우회 (v1)**: dyadic 계수 선택(H₂ LCU)·군 재선택(S₃→D₄, ω 위상 회피)·코드=그래프 재해석
([[5,1,3]] 오각형)·부분공간 임베딩(큐트릿)·exact-핵심 vs 게이트-부분 명시 분리.

**(b) ★직접 닫힌형 구성 (v3/V4 — 탐색 금지 원칙)**: ansatz 탐색은 실패했고 **수학적 직접 유도**가 성공했다.
- Schur-Weyl: CG 계수를 아는 상태에서 2-level Givens 회전 시퀀스를 **손으로 유도** → 첫 시도 exact.
- AKLT: MPS 우측환경 R_j=E^{4−j}(|0⟩⟨0|) 이 **닫힌형 대각·유리수**임을 먼저 증명 → site 분기 진폭² 전부
  유리수 → 필요한 회전각이 arccos√(유리수) 로 자동 확정.
→ **제안 시**: "회로를 탐색으로 찾는다"가 아니라 **"이 닫힌형 구조 때문에 각도/계수가 유리수·dyadic 으로
떨어진다"는 수학적 근거**를 제시하라. 그런 제안이 즉시 자율 실행된다.

**(c) ★승인-module 사람게이트 (신규 프로세스)**: 신규 module 은 완전 금지가 아니라 **사람 승인 게이트**다.
v3 에서 ry_cg_half±(arccos⅓ 반각), V4 에서 ry_ak41/13/7±(arccos√유리수) 가 승인·봉인됐다. 조건:
exact analytic golden(닫힌형 각도)·독립 2차 오라클 검증 가능·frozen/consensus 무훼손·최소 개수.
→ 신규 module 이 불가피하면 **정확한 닫힌형 각도와 최소 개수**를 명시해 제안하라(승인 확률↑).

## 5. 반드시 지켜야 할 제약

- **결정론 불가침** — byte-identical 재봉인. 동결 합의 키·오라클 지문 파일 재생성/수정 금지.
- **오라클은 사용만** — `verify_seal.py`/`contracts.py` 재구현 금지(해시가 봉인에 baked).
- **honest decomposition** — `MatrixGate`/정답-행렬 shortcut 금지. 실제 회로 분해로 조립.
- **self-contained** — 벤더된 오라클 외 외부 서비스/스킬 의존 금지(예: 화학 계수는 rational hand-code).
- **하드웨어 out** — QPU/노이즈/실행-증거 축은 대상 아님.
- **정직 경계** — 근사(다항식/Trotter)·확률(증류 성공률)·측정후처리는 봉인 아니라 **관측**으로 명시.
  exact ≠ 근사, dense ≠ structural ≠ subspace, 결정론 재현 ≠ 정확성. 상태준비 app 은 정의 열만 물리
  (여타 열=회로-유도 완성) 명시.

## 6. 답변 형식 (제안마다)

**3~5개**를 impact×feasibility 순으로. 각 제안:

1. **proposal** — 새 수평 축 한 줄 + 무엇을 봉인할지(구체적 작은 인스턴스).
2. **rationale** — 왜 지금 가치 있는가(정체성 부합·compounding).
3. **feasibility** — 작은 인스턴스가 Tier-0 EXACT 봉인 가능한가? 어떤 봉인 게이트로 조립되나? 오라클로
   무엇을 검증하나? **§4′(b) 처럼 각도/계수가 exact 로 떨어지는 수학적 근거를 제시.** 신규 module 필요
   시 §4′(c) 형식으로 닫힌형 각도·개수 명시.
4. **risk** — 실패 모드·정직 경계(무엇이 근사/관측, 무엇이 exact).
5. **novelty** — §3 EXCLUDE(특히 3b/3c)와 **명시적으로 대조**해 겹치지 않음을 확인.

## 7. 개념 미니 용어집

- **봉인(seal)**: 오라클이 회로 조립품 == golden 유니터리를 확인하고 registry 에 영구 기록(byte-identical 재현 가능).
- **compounding**: 봉인 자산을 부품으로 재사용해 새 app 을 새 module 0 으로 조립(신뢰 자본 복리).
- **honest boundary**: exact 봉인과 관측(근사/확률/측정)의 명시적 구분 — 과대주장 금지.
- **subspace 강검증**: dense 유니터리 대신 계산기저 순열을 독립 정수산술로 대조(대규모 app 용).
- **witness 관측**: 봉인 자산의 수학/물리 성질(J²/Jz 동시대각·parent-H 소멸 등)을 독립 경로로 검증하되
  봉인으로 주장하지 않는 계층(teeth 포함 — 틀린 상태가 검출됨을 함께 실증).
