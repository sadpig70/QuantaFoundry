<!-- QuantaFoundry 수평 확장 아이디어 제안 요청 — v4 (2026-07-05). v1/v2/v3 후속. self-contained. -->
<!-- 외부 모델 런타임에게 전달용. 이 문서 하나만 읽고 제안 가능하도록 작성됨. -->

# QuantaFoundry — 수평적 확장(Horizontal Expansion) 아이디어 제안 요청 · v4

> **v3 → v4 변경점**: v3 요청으로 8개 런타임의 제안(35개)을 받아 **자율실행 4트랙 + 사람게이트 6건 전부**를
> 종결했다 — 명시적 양자 산술·Szegedy walk·Choi 상태·path-sum 4차 검증경로(자율실행), 그리고
> 2D 텐서망 PEPS·**2q unitary 2-design(★수학적 반증으로 종결)**·π/6 family(채널 γ¼+Szegedy p¼)·
> **UD-POVM Naimark(측정이론)**·Schur n=4·**Fibonacci anyon braid(새 대수체 ℚ(ζ₅,√φ) 승인)**(사람게이트).
> 그 전부를 §3 EXCLUDE 에 **추가**했다(§3d). §4′에 v4 에서 배운 새 성공 패턴 3개(**반증→회수·Kraus
> 자유도 재도출·sub-app 수직 복리**)를 추가했다. 이제 **그 너머의 새 축**을 구한다.

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

현재 **89 modules / 342 sealed apps** (root `4f7e40c1…`). 카테고리:

### 3a. v1 이전 (기존 자산)
- **기초 상태/게이트**: Bell, GHZ(≤16 부분검증·GHZ-9 encoder), cluster/ring/W-state, 표준 1·2·다중제어
  게이트(X/Z/H/S/T/√X, CNOT/CZ/Toffoli/Fredkin/iSWAP, c3x…c12x), 회전/위상(Rz/Rx/Ry 특정각·controlled-Rk).
- **QFT 계열**: QFT(2–8)·역QFT·QPE·amplitude estimation(QAE).
- **검색/증폭**: Grover·diffusion·reflection·amplitude amplification.
- **Hamiltonian 시뮬레이션**: TFIM/Heisenberg Trotter·2차 Suzuki·4차 Yoshida-Suzuki·Pauli-지수 회전(rxx/ryy/rzz).
- **변분**: VQE(다층 hardware-efficient)·QAOA(MaxCut)·parameter-shift gradient(관측).
- **쿼리 알고리즘**: Deutsch-Jozsa·Bernstein-Vazirani·Simon·quantum walk(C4/C8 coined).
- **QEC**: repetition·syndrome·Shor-9 encoder·Steane/stabilizer-tableau(Tier-2)·transversal 논리 Clifford(H/S/CNOT).
- **Shor**: 15=3×5·진짜 21=3×7·distinct-prime structural frontier(**shor69…shor141…shor3683, 부분공간
  순열 강검증 19개**)·modular multiplier(cmul) 자동 factory.
- **QSVT/block-encoding(완비)**: LCU block-encoding·QSP(d 1/3/5)·QSVT 다항식 변환·consumer trilogy(Ham-sim·amp-amp·matrix inversion).
- **Fermionic**: Jordan-Wigner(반교환·hopping·number·t-V·spinful Fermi-Hubbard) + Bravyi-Kitaev/parity
  인코딩·tapering·fermionic SWAP.
- **분자/data-oracle/FTQC/비아벨/qudit (v1 6축)**: H₂ dyadic LCU · qROM+SELECT-PREPARE · magic state+
  [[5,1,3]] graph-code 증류 코어+논리 T-injection · S₃/D₄ 비아벨 군 오라클+D₄ Fourier+HSP 표본화 ·
  큐트릿 qubit-임베딩 삼진 산술.
- **채택/경화**: OpenQASM3 export/ingest·CLI·citable root·독립 2차 오라클·규약-독립성·oracle revocation·ed25519·CI seal-gate·발견 superoptimization.

### 3b. v2 구현
- **위상적 논리연산**: [[4,2,2]] surface-type encoder·lattice surgery coherent 병합·2×2 토릭 ground
  state·완전 FTQC 논리스택 관측. (**d=3 surface·defect braiding·color code·15-to-1 은 아직 없음.**)
- **MBQC**: 3×3 클러스터 자원상태·측정패턴↔회로 등가. (**gflow 일반론은 아직 없음.**)
- **GF(2ᵏ) 유한체**: gf4_mul·gf4_frob·gf8_mulx. (**역원·다항식 인수분해·Reed-Solomon 류는 아직 없음.**)
- **Anyon braiding(Ising)**: ising_braid_b2(Majorana B₂, Clifford).
- **QCA**: Clifford brickwork·GNVW 관측. (**non-Clifford QCA·Floquet 위상은 아직 없음.**)

### 3c. v3 사람게이트(일부)·V4·V6·V8 구현
- **Z₂ 격자 게이지**: z2gauge3(Gauss law encoder). (**U(1)/SU(2)·plaquette 동역학·2+1D 는 아직 없음.**)
- **ZX-calculus 검증경로**(3번째 오라클) · **qLDPC**: [[8,1,2]] 하이퍼그래프곱 encoder.
- **Schur-Weyl**: schur3(직접 CG cascade, S₃ duality witness, 승인 module ry_cg_half±).
- **텐서망(MPS)**: aklt4(순차 조건화 등척, 승인 module ry_ak41/13/7±).
- **열린 양자계(CPTP 채널)**: Stinespring dilation — bitflip/phasedamp/ampdamp(½)·depol(p=1)·
  **γ/p/λ=¼ family**(π/6 승인분)·채널 합성 격자(½∘½=¾·¼∘¼=7/16·교차 ¼∘½=5/8)·채널→QEC 정정 파이프라인
  관측·**Choi–Jamiołkowski 상태 4종**(J==Kraus·CP/TP·duality 재구성). (**일반 감쇠율 연속족·다큐빗
  correlated 채널·GKP 류 연속변수는 아직 없음.**)
- **unitary design**: 1q Clifford 군 **전 24원소**(정확 2/3-design, F₂=2·F₃=5).

### 3d. ★v3 회신 소비분 — 자율실행 4트랙 + 사람게이트 6건 전부 (이번 라운드 신규 — 재제안 금지)
- **명시적 양자 산술**: cuccaro_add2/3(MAJ/UMA ripple-carry)·draper_add2(QFT 위상가산)·cmp2_ge(비교기)
  — ripple==Fourier 교차검증 포함. (**나눗셈/제곱근·부동소수·carry-lookahead 는 아직 없음.**)
- **Szegedy quantized walk**: 2-state p=½(W=X⊗X 수축)·C₄(draper 가산기 복리)·**p=¼ 비대칭 가역 연쇄**
  (일반 discriminant·비균일 정상분포). (**spectral gap 증폭 정리의 알고리즘 소비·hitting time 은 아직 없음.**)
- **Path-sum 검증경로**: ℤ[ω₈] 정수환 sum-over-paths — dense/tableau/ZX 에 이은 **4번째 독립 오라클 경로**.
- **2D 텐서망(PEPS)**: peps22_rvb(2×2 RVB dimer 중첩, S_tot²=0 witness, module 0).
  (**일반 PEPS 템플릿·MERA·PBC 는 아직 없음.**)
- **★2q unitary 2-design — 수학적 반증으로 종결(closed-negative)**: 정확(가중 포함) unitary 2-design 은
  **|X| ≥ d⁴−2d²+2 = 226 (d=4)** [Gross–Audenaert–Eisert 2007; K(d)=span rank 논증이라 가중 설계에도
  유효 — 탈출구 없음]. **"소형(≤수십 원소) 2q exact unitary 2-design" 류 제안은 수학적으로 불가하므로
  제안 금지.** (v3 회신의 "21원소" 주장은 projective **state**-design 과의 혼동으로 판명.)
- **MUB-20 projective state 2-design**: d=4 상호비편향 5기저×4상태 20앱(Clifford word, FP=1/10 exact,
  MUB 완비측정 단층재구성 데모). (**유한샘플 shadow tomography 프로토콜 자체는 미구현 — 기반만.**)
- **측정이론(POVM)**: naimark_ud3 — UD(unambiguous discrimination) POVM 의 Naimark 정방 유니터리 완성
  (E_k 재구성==IDP 정의 exact·오식별 0·성공 ½ 최적). (**SIC-POVM·POVM 정보이론(accessible information)·
  연속 측정은 아직 없음 — 단 SIC 는 비-골든각이라 exact 봉인 불가 판정 기록 있음.**)
- **Schur n=4**: schur4(16×16, spin-2⊕1³⊕0², **schur3 sub-app 수직 복리**, S₄ [4]/[3,1]/[2,2] duality
  witness, module 0). (**n≥5·irrep 레지스터 명시 분리·quantum Schur sampling 알고리즘화는 아직 없음.**)
- **★Fibonacci anyon braid**: fib_braid_s1/s2(σ₁=R·σ₂=FRF, Yang-Baxter exact·B₃ 중심 (σ₁σ₂)³=e^{2πi/5}I·
  비-Clifford witness) — **새 대수체 ℚ(ζ₅,√φ)(차수 8) 승인·도입 완료**, module z5_gate(Z^(1/5))·ry_fib.
  (**Jones 다항식 평가·n≥4 anyon fusion tree·braid weave 컴파일·universality 정량화는 아직 없음.**)

**핵심: 위 축들의 사소한 변형(사이트/차원 늘리기·다른 소군·계수만 다른 채널 하나 더)은 원치 않는다.
질적으로 새로운 계층을 제안하라.** 단 괄호의 "아직 없음" 항목이 *질적으로 새 축*을 여는 관문이면 환영한다.

---

## 4. 우리가 원하는 것

§1·§5 를 지키면서 **§3에 없는 새로운 수평 축**. 작은 인스턴스가 Tier-0 EXACT 봉인 가능·compounding 큰 것.
방향 감을 위한 예시(강요 아님):

- **Clifford 계층구조(3rd level)** — T 를 넘는 semi-Clifford/diagonal 계층 게이트의 구조적 자산화
  (gate teleportation 소비 연결). v3 에서도 예시였으나 아직 아무도 실행 형태로 제안하지 않았다.
- **Jones 다항식/anyon 심화** — 봉인된 Fibonacci braid 를 **소비**하는 질적 새 층(Jones bracket 평가
  회로의 exact 코어·fusion tree 산술). 새 대수체 ℚ(ζ₅,√φ) 는 이미 승인돼 있다 — 그 위에서 쌓아라.
- **표현론 알고리즘화** — quantum Schur sampling(봉인 schur3/schur4 소비)·dihedral HSP 완결 파이프라인.
- **부호이론 심화** — GF(2ᵏ) 역원/Reed-Solomon 산술·flag qubit 증후 추출(1-flag cat)·decoder 의
  가역 코어(범위 내 부분만).
- **일반 텐서망 템플릿** — 임의 χ=2 MPS/작은 PEPS 의 순차 등척 **컴파일러**(인스턴스가 아니라 방법의
  자산화 — genskill 패턴).
- **무작위성 심화** — 유한샘플 classical shadow 프로토콜의 exact 코어(MUB-20/cliff1 기봉인 소비)·
  state t-design(t≥3).
- **형식 검증 확장** — SMT/symbolic proof·stabilizer-rank 기반의 5번째 독립 검증 경로.
- 그 밖에 **당신이 더 나은 축을 알면 그것을 제안하라.**

## 4′. ★성공 패턴 힌트 (v1→v4 구현에서 배운 것 — 참고용)

**(a) 게이트 우회 (v1)**: dyadic 계수 선택(H₂ LCU)·군 재선택(S₃→D₄)·코드=그래프 재해석([[5,1,3]])·
부분공간 임베딩(큐트릿)·exact-핵심 vs 게이트-부분 명시 분리.

**(b) 직접 닫힌형 구성 (v3/V4 — 탐색 금지 원칙)**: ansatz 탐색은 실패했고 **수학적 직접 유도**가 성공했다
(Schur CG cascade·AKLT 우측환경 유리수 증명). → "이 닫힌형 구조 때문에 각도/계수가 유리수·dyadic 으로
떨어진다"는 **수학적 근거**를 제시하라. 그런 제안이 즉시 자율 실행된다.

**(c) 승인-module 사람게이트**: 신규 module 은 완전 금지가 아니라 **사람 승인 게이트**다. 지금까지 승인:
ry_cg_half±(arccos⅓ 반각)·ry_ak41/13/7±·ry_pi6±(π/6)·**z5_gate/ry_fib(새 대수체 ℚ(ζ₅,√φ) 포함)**.
조건: exact analytic golden(닫힌형 각도)·독립 2차 오라클 구성 가능(π-free surd 우대)·frozen 무훼손·
최소 개수. **새 대수체조차 승인 가능**함이 실증됐다 — field 를 정확히 공시하라(축소 보고 금지).

**(d) ★v4 신규 패턴 3개**:
- **반증→회수**: 수학적으로 불가한 목표(2q 소형 unitary 2-design)는 **하한 증명으로 정직 종결**하고,
  그 혼동의 정직한 알맹이(MUB state 2-design)를 회수해 자산화했다. 반증 문서도 1급 산출물이다 —
  제안이 틀렸다면 왜 틀렸는지의 수학이 남는다. 과감히 제안하되 검증 가능한 수학을 담아라.
- **자유도 재도출**: canonical 구성(√E Kraus)이 각도 격자 밖이어도, **게이지 자유도(rank-1 Kraus 선택)**
  로 기존 팔레트 격자에 재도출해 module 0 으로 만들었다(Naimark POVM). "각도가 안 떨어진다"고 포기하기
  전에 표현 자유도를 스캔하라.
- **sub-app 수직 복리**: schur4 = 봉인된 schur3 을 **부품으로 재사용**(plan 에 app 참조) + 새 CG 층만
  추가 — 3회 탐색 실패했던 n=3 위에 n=4 가 1회 통과로 쌓였다. 기봉인 대형 자산을 부품으로 쓰는 제안 우대.

## 5. 반드시 지켜야 할 제약

- **결정론 불가침** — byte-identical 재봉인. 동결 합의 키·오라클 지문 파일 재생성/수정 금지.
- **오라클은 사용만** — `verify_seal.py`/`contracts.py` 재구현 금지(해시가 봉인에 baked).
- **honest decomposition** — `MatrixGate`/정답-행렬 shortcut 금지. 실제 회로 분해로 조립.
- **self-contained** — 벤더된 오라클 외 외부 서비스/스킬 의존 금지(예: 화학 계수는 rational hand-code).
- **하드웨어 out** — QPU/노이즈/실행-증거 축은 대상 아님.
- **정직 경계** — 근사(다항식/Trotter)·확률(증류 성공률)·측정후처리는 봉인 아니라 **관측**으로 명시.
  exact ≠ 근사, dense ≠ structural ≠ subspace, 결정론 재현 ≠ 정확성. 상태준비 app 은 정의 열만 물리
  (여타 열=회로-유도 완성) 명시.
- **★registry 실측 기반 novelty 자체 정정 우대** — v3 회신 8개 중 1개(A8)만 현재 앱 목록을 실측해
  중복을 스스로 걸렀다. §3 를 정독하고 자신의 제안이 EXCLUDE 와 겹치지 않음을 명시적으로 검증하라.

## 6. 답변 형식 (제안마다)

**3~5개**를 impact×feasibility 순으로. 각 제안:

1. **proposal** — 새 수평 축 한 줄 + 무엇을 봉인할지(구체적 작은 인스턴스).
2. **rationale** — 왜 지금 가치 있는가(정체성 부합·compounding).
3. **feasibility** — 작은 인스턴스가 Tier-0 EXACT 봉인 가능한가? 어떤 봉인 게이트로 조립되나? 오라클로
   무엇을 검증하나? **§4′(b) 처럼 각도/계수가 exact 로 떨어지는 수학적 근거를 제시.** 신규 module 필요
   시 §4′(c) 형식으로 닫힌형 각도·개수·field 명시.
4. **risk** — 실패 모드·정직 경계(무엇이 근사/관측, 무엇이 exact).
5. **novelty** — §3 EXCLUDE(특히 **3d**)와 **명시적으로 대조**해 겹치지 않음을 확인.

## 7. 개념 미니 용어집

- **봉인(seal)**: 오라클이 회로 조립품 == golden 유니터리를 확인하고 registry 에 영구 기록(byte-identical 재현 가능).
- **compounding**: 봉인 자산을 부품으로 재사용해 새 app 을 새 module 0 으로 조립(신뢰 자본 복리).
- **honest boundary**: exact 봉인과 관측(근사/확률/측정)의 명시적 구분 — 과대주장 금지.
- **subspace 강검증**: dense 유니터리 대신 계산기저 순열을 독립 정수산술로 대조(대규모 app 용).
- **witness 관측**: 봉인 자산의 수학/물리 성질(J²/Jz 동시대각·Yang-Baxter·frame potential 등)을 독립
  경로로 검증하되 봉인으로 주장하지 않는 계층(teeth 포함 — 틀린 상태가 검출됨을 함께 실증).
- **closed-negative**: 목표가 수학적으로 불가함을 하한/정리로 확정하고 반증 문서를 1급 산출물로 남기는
  정직 종결(예: 2q 소형 unitary 2-design).
