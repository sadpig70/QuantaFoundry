<!-- QuantaFoundry 수평 확장 아이디어 제안 요청 — v2 (2026-07-02). v1 후속. self-contained. -->
<!-- 외부 모델 런타임에게 전달용. 이 문서 하나만 읽고 제안 가능하도록 작성됨. -->

# QuantaFoundry — 수평적 확장(Horizontal Expansion) 아이디어 제안 요청 · v2

> **v1 → v2 변경점**: v1 요청으로 8개 런타임의 제안을 받아 **17커밋·6개 새 수평 축**을 봉인 구현했다
> (BK/parity 인코딩·분자 Hamiltonian·data-oracle·magic 증류·논리 T-injection·비아벨 군 Fourier+HSP·
> 큐트릿 산술). 그 6축을 §3 EXCLUDE 에 **추가**했다. 이제 **그 너머의 새 축**을 구한다.
> §4′에 v1 구현에서 배운 **"게이트 우회(gate-avoidance)" 성공 패턴**을 힌트로 추가했다 — 참고하되 강요 아님.

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

현재 **77 modules / 194 sealed apps** (root `eedb7aa8…`). 카테고리:

### 3a. v1 이전 (기존 자산)
- **기초 상태/게이트**: Bell, GHZ(≤16 부분검증·GHZ-9 encoder), cluster/ring/W-state, 표준 1·2·다중제어
  게이트(X/Z/H/S/T/√X, CNOT/CZ/Toffoli/Fredkin/iSWAP, c3x…c12x), 회전/위상(Rz/Rx/Ry 특정각·controlled-Rk).
- **QFT 계열**: QFT(2–8)·역QFT·QPE·amplitude estimation(QAE).
- **검색/증폭**: Grover·diffusion·reflection·amplitude amplification.
- **Hamiltonian 시뮬레이션**: TFIM/Heisenberg Trotter·2차 Suzuki·4차 Yoshida-Suzuki·Pauli-지수 회전(rxx/ryy/rzz).
- **변분**: VQE(다층 hardware-efficient)·QAOA(MaxCut)·parameter-shift gradient(관측).
- **쿼리 알고리즘**: Deutsch-Jozsa·Bernstein-Vazirani·Simon·quantum walk(C4/C8).
- **QEC**: repetition·syndrome·Shor-9 encoder·Steane/stabilizer-tableau(Tier-2)·transversal 논리 Clifford(H/S/CNOT).
- **Shor**: 15=3×5·진짜 21=3×7·distinct-prime structural frontier(shor69…shor3683)·modular multiplier(cmul)·부분공간 순열 강검증.
- **QSVT/block-encoding(완비)**: LCU block-encoding·QSP(d 1/3/5)·QSVT 다항식 변환·consumer trilogy(Ham-sim·amp-amp·matrix inversion).
- **Fermionic(Jordan-Wigner)**: 반교환관계·hopping·number·완전 t-V + spinful Fermi-Hubbard(JW Z-string).
- **채택/경화**: OpenQASM3 export/ingest·CLI·citable root·독립 2차 오라클·규약-독립성·oracle revocation·ed25519·CI seal-gate·발견 superoptimization.

### 3b. ★v2 신규 (이번 세션 구현 — 재제안 금지)
- **대체 fermionic 인코딩**: **Bravyi-Kitaev**(`bk4_transform` U_BK=GF(2) 기저변환·`bk_num1`·`bk_hop01`
  block-encoding)·**parity 인코딩**(`parity4_transform`)·입자수 tapering·JW↔BK 등가/weight 관측. → JW 외
  인코딩은 이제 구현됨. (Verstraete-Cirac·fermionic swap network 는 **아직 없음**.)
- **분자 Hamiltonian**: `be_h2`(H₂ 부호구조 dyadic uniform LCU block-encoding). → H₂ *구조*는 구현됨.
  (HeH⁺·LiH·물 등 **다른 분자**, 실계수 정밀 봉인, orbital/point-group 대칭은 **아직 없음**.)
- **Generic data oracle**: `qrom22`(table lookup permutation)·`select_prepare4`(전 4종 Pauli SELECT + dyadic
  PREPARE LCU 템플릿). → qROM/SELECT-PREPARE 기본 계층은 구현됨.
- **FTQC non-Clifford (3부작)**: magic state(`magic_a`)·**magic 증류**(`code513_encoder`=[[5,1,3]] 오각형
  graph code, 5-to-1 coherent-branch 관측)·**논리 T-injection**(Steane gate-teleportation, S^⊗7=S_L†). →
  non-Clifford universality 사슬(물리→공장→논리)은 구현됨. (**lattice surgery·surface code 논리연산·
  15-to-1 증류·color code 는 아직 없음.**)
- **비아벨 표현론**: **첫 비아벨 군 오라클+Fourier**(`s3_mult` S₃·`d4_mult`+`d4_qft` D₄ 군 Fourier)·
  **이면군 Hidden Subgroup 표본화 관측**(coset state→irrep, 비정규 부분군 검출). → 비아벨 HSP 관문은 구현됨.
- **qudit(ternary)**: **큐트릿 qubit-임베딩 삼진 산술**(`qutrit_x3` +1 mod3·`qutrit_sum` (a+b)mod3). →
  qudit 산술 *순열* 계층은 구현됨. (**qutrit QFT₃/Z₃(ω 위상)·qudit 중첩·higher d 는 아직 없음.**)

**핵심: 위 6축의 사소한 변형(다른 분자 하나 더·다른 소군 하나 더·d=4 큐디트)은 원치 않는다. 질적으로 새로운
계층을 제안하라.** 단 위 괄호로 표시한 "아직 없음" 항목이 *질적으로 새 축*을 여는 관문이면 환영한다.

---

## 4. 우리가 원하는 것

§1·§5 를 지키면서 **§3에 없는 새로운 수평 축**. 작은 인스턴스가 Tier-0 EXACT 봉인 가능·compounding 큰 것.
방향 감을 위한 예시(강요 아님):

- **FTQC 위상적 계층** — lattice surgery·surface/color code 논리 연산·격자 결함(defect) 브레이딩·
  MBQC/measurement pattern(gflow) 등. (우리는 magic 증류·논리 T 까지 왔으나 **위상적 코드 연산은 없다**.)
- **차세대 QEC** — qLDPC(hypergraph product)·bosonic code(GKP/cat 의 이산 근사)·subsystem code.
- **표현론 심화** — Schur-Weyl 변환·비아벨 QFT 의 실제 알고리즘화(dihedral HSP full pipeline)·
  Clebsch-Gordan·quantum Schur sampling·anyon/braid 표현.
- **새 대수 구조** — 초대칭/격자 게이지 이론(Z₂ Higgs)·tensor-network 상태(MPS/PEPS/AKLT exact 준비)·
  Clifford 계층구조(third level)·양자 셀룰러 오토마타.
- **새로운 검증 *방법*** — ZX-calculus Tier-3·symbolic/SMT proof·범주론적 semantics·
  path-integral/stabilizer-rank 검증.
- 그 밖에 **당신이 더 나은 축을 알면 그것을 제안하라.**

## 4′. ★게이트 우회 힌트 (v1 구현에서 배운 성공 패턴 — 참고용)

v1 제안 다수가 "임의 각도(비-dyadic 위상)·임의 실수 진폭"을 요구해 honest 봉인이 막혔다. 우리는 이를
**설계 재구성으로 우회**해 신규 module 0·완전 exact 봉인을 달성했다. 좋은 제안은 이런 우회를 내장한다:

- **dyadic 계수 선택**: 임의 계수 LCU 대신 균일/2⁻ᵏ 계수 → PREPARE=Hadamard(정확 봉인각). (H₂ 봉인)
- **군/구조 재선택**: 비-dyadic ω 를 강제하는 S₃ 대신 **D₄**(회전군 Z₄ → 위상 {±1,±i} 팔레트 안)로
  같은 "비아벨 Fourier" 목표 달성.
- **코드=그래프 재해석**: [[5,1,3]] 을 오각형 **graph code** 로 봐 인코더를 GHZ·H·CZ 순수 팔레트로 분해.
- **부분공간 임베딩**: 큐트릿을 qubit 부분공간에 임베딩 → 오라클 "차원≠2ⁿ" 게이트 소멸.
- **계층 분리**: exact 봉인 가능한 부분(순열/산술/Clifford)과 게이트 부분(ω 위상·근사)을 **명시 분리**.

→ **제안 시**: 무엇이 팔레트-exact 봉인 가능하고 무엇이 게이트(신규 module/근사)인지 미리 갈라서 제시하라.
"exact 봉인 가능한 최소 핵심"이 있는 축이 우선순위가 높다.

## 5. 반드시 지켜야 할 제약

- **결정론 불가침** — byte-identical 재봉인. 동결 합의 키·오라클 지문 파일 재생성/수정 금지.
- **오라클은 사용만** — `verify_seal.py`/`contracts.py` 재구현 금지(해시가 봉인에 baked).
- **honest decomposition** — `MatrixGate`/정답-행렬 shortcut 금지. 실제 회로 분해로 조립.
- **self-contained** — 벤더된 오라클 외 외부 서비스/스킬 의존 금지(예: PySCF 계수는 rational hand-code).
- **하드웨어 out** — QPU/노이즈/실행-증거 축은 대상 아님.
- **정직 경계** — 근사(다항식/Trotter)·확률(증류 성공률)·측정후처리는 봉인 아니라 **관측**으로 명시.
  exact ≠ 근사, dense ≠ structural ≠ subspace, 결정론 재현 ≠ 정확성.

## 6. 답변 형식 (제안마다)

**3~5개**를 impact×feasibility 순으로. 각 제안:

1. **proposal** — 새 수평 축 한 줄 + 무엇을 봉인할지(구체적 작은 인스턴스).
2. **rationale** — 왜 지금 가치 있는가(정체성 부합·compounding).
3. **feasibility** — 작은 인스턴스가 Tier-0 EXACT 봉인 가능한가? 어떤 봉인 게이트로 조립되나? 오라클로
   무엇을 검증하나? **§4′ 처럼 exact-핵심 vs 게이트-부분을 갈라서.**
4. **risk** — 실패 모드·정직 경계(무엇이 근사/관측, 무엇이 exact).
5. **novelty** — §3 EXCLUDE(특히 3b v2 신규)와 **명시적으로 대조**해 겹치지 않음을 확인.

## 7. 개념 미니 용어집

- **봉인(seal)**: 오라클이 회로 조립품 == golden 유니터리를 확인하고 registry 에 영구 기록(byte-identical 재현 가능).
- **compounding**: 봉인 자산을 부품으로 재사용해 새 app 을 새 module 0 으로 조립(신뢰 자본 복리).
- **honest boundary**: exact 봉인과 관측(근사/확률/측정)의 명시적 구분 — 과대주장 금지.
- **subspace 강검증**: dense 유니터리 대신 계산기저 순열을 독립 정수산술로 대조(대규모 app 용).
