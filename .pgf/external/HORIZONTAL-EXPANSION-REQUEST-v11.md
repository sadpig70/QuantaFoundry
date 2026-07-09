<!-- QuantaFoundry 수평 확장 아이디어 제안 요청 — v11 (2026-07-09). v1~v10 후속. self-contained. -->
<!-- 외부 모델 런타임에게 전달용. 이 문서 하나만 읽고 제안 가능하도록 작성됨. -->

# QuantaFoundry — 수평적 확장(Horizontal Expansion) 아이디어 제안 요청 · v11

> **v10 → v11 변경점**: v10 요청으로 8개 런타임의 제안(report10)을 받아 **통합 6축(TrackHE10)을 완주·폐합**했다.
> 전 축 **관측/선검증**(신규 봉인 module 0·root 불변). 성과:
> - **KS-18 state-independent 맥락성**(P1): Cabello 18-ray/9-orthogonal-basis(ℝ⁴) {0,1}-coloring 불가능 —
>   ★**계산 탐색으로 CEGA-등가 구조 구성·검증**(외부 제안 좌표가 basis 와 불일치→기억 의존 배제). path A parity
>   (2·Σc=9 홀수 모순) + path B exhaustive 백트래킹. Peres-Mermin(operator-product)·contextual fraction(정량)
>   상보(ray-coloring 계층).
> - ★**A₅ ζ₅-vs-√5 redirect 선검증**(P2): ★**report10 긴장 해소**. A₅(60원소, 최소 비가해 단순군)는 **ambivalent**
>   (모든 g~g⁻¹) → **모든 기약문자값 실수 ∈ ℚ(√5)** → **√5 실수 surd 로 충분·복소 ζ₅ 불필요**. 요청서(v10 §4)
>   와 일부 제안의 "A₅ ζ₅ Fourier"는 **과대 게이트**였음을 선검증이 정정(ambivalent→실수형 표현). NOT rational
>   group(5-cycle 2 클래스 분열). 대조: A₄ NOT ambivalent(3-cycle g≁g⁻¹)→ζ₃ 복소 필연.
> - **Galois-orbit ℤ[ω] 검증**(P3, ★제11 경로 **후보**/certificate layer): 회로 진폭을 ℚ(ζ₈) 대수수로 exact
>   표현→전체 Galois 궤도 {σ_k(a):k∈(ℤ/8)*}+정수 norm/trace+**equivariance**(σ_k(⟨y|C|x⟩)==⟨y|C^{σ_k}|x⟩).
>   covered 76 Clifford+T(전역 ζ₈ 위상까지). ★진폭 동일성 검증이라 **제11 '경로 후보'로 정직 표기**(dense 겹침
>   시 audit layer 강등). ζ₁₆+ 위상 앱 skip(ℚ(ζ₈)-scope 밖).
> - **MTC pentagon/hexagon 핵심 + Ising/Fibonacci braid 유니터리**(P4): Ising(F=Hadamard/√2·F²=I·braid
>   Yang-Baxter·Clifford image·비보편) vs Fibonacci(φ²=φ+1·non-Clifford·보편) = 두 정준 애니온 braid. (관측·
>   braid=전역 ζ₁₆ 위상.)
> - **3D 위상절연체 ℤ₂**(P6, Fu-Kane): 3D FKM 4-band TRIM 8점 parity 닫힌형 ν₀ == 수치 eigenvector parity
>   (이중경로). 2D Chern(TR-broken)의 3D ℤ₂(TR-preserved) 상보.
> - **surface-code lattice surgery merge/split logical CNOT**(P5): Horsman 프로토콜 8 측정 branch = CNOT
>   up to Pauli 보정(X̄_t·Z̄_c frame). code switching(coherent W, 다른 부호)의 측정-기반(동일 부호) 상보.
> §3n 에 추가. §4′에 v11 신규 패턴 3(★**선검증이 외부 제안 정정·ambivalent=실수/복소 게이트 판별·certificate
> layer 정직 강등**).

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
- ★**Tier-0 dense 실질 상한 ≈ 12큐빗**(2^12). 그 이상 Clifford 는 **Tier-2 정준 tableau**, 비-Clifford 대형은
  **관측(witness)** 또는 structural — 제안 시 봉인 경로 명시(§4′i).

## 3. EXCLUDE — 이미 구현·봉인·관측된 것 (재제안 금지)

현재 **95 modules / 466 sealed apps** (root `6e7d2a70ef9e1790…`). **독립 검증경로 10개**
(dense · tableau · ZX · path-sum ℤ[ω₈] · stabilizer-rank · matchgate/SO(2n) · tensor-network · QMDD ·
ANF/bit-vector · Gröbner/ℤ[ω] phase-ideal) **+ 제11 경로 후보**(Galois-orbit certificate layer, §3n).

### 3a~3l. v1~v8 소비분 (요약 — 상세는 이전 라운드 EXCLUDE 계보)
- **기초/QFT/QPE/Grover/Trotter·Suzuki/VQE·QAOA/쿼리/walk** · **QEC**(repetition·Steane·Shor-9·transversal
  Clifford·[[25,1,9]] 연접·RM[[15,1,3]]·HGP[[27,4,3]]·BCH cyclic [[15,7,3]]·[[31,11,5]]) · **Shor**(15·21·
  distinct-prime frontier …235·cmul factory) · **QSVT 완비** · **Fermionic**(JW/BK/parity·fSWAP·Bogoliubov) ·
  **분자 H₂·비아벨 Fourier**(S₃/D₄/S₄/Q₈/B₃) · **위상 논리연산·MBQC·Z₂ gauge·Schur·AKLT·CPTP·2/3-design·PEPS·
  MUB·GF(8)·Fibonacci/Majorana braid·C₃ phase-poly·RS·[[8,3,2]] CCZ** · **동역학**(dual-unitary·Floquet·OTOC·
  매듭·2D Chern) · **자원**(magic·채널 Choi·Peres-Mermin·diamond) · **검증경로 1~9**(…ANF).

### 3m. v9 소비분 (TrackHE9)
- **Gröbner/ℤ[ω] phase-ideal 제10 검증경로**(대각/monomial 위상회로) · **contextual fraction LP** · **|C|≥2 고차
  Chern**(spin-S) · **A₄ ζ₃-필연 선검증**(ω₃ 대기) · **code switching**(closed-neg Steane↔[[8,3,2]] + RM15 positive) ·
  **Ising 융합** · **qutrit Gross-Wigner**.

### 3n. ★v10 소비분 — 통합 6축 (TrackHE10, 이번 라운드 신규 — 재제안 금지)
- **KS-18 state-independent 맥락성(P1)**: `ks18_observe` — Cabello 18-ray/9-basis(ℝ⁴) {0,1}-coloring 불가능
  (parity 2·Σc=9 + exhaustive 백트래킹). (**qutrit(d=3) KS·더 큰 KS(24/33-vector)·상태의존 맥락성·negativity
  monotone 정량은 아직 없음.**)
- ★**A₅ ζ₅-vs-√5 redirect 선검증(P2)**: `a5_observe` — A₅ ambivalent→문자표 ℚ(√5) 실수→√5 충분·ζ₅ 불필요.
  ★**봉인 보류**: A₅ Fourier 는 **√5 실수-surd 승인 module**(ζ₅ 복소보다 경량) 필요. (**A₅ Fourier 실봉인(√5
  승인)·2.A₅ 이중피복·A₆·PSL(2,7) ζ₇(진짜 복소 필연)·Hecke·모듈러 표현은 아직 없음.**)
- **Galois-orbit ℤ[ω] 검증(P3, 제11 경로 후보)**: `galois_orbit_verify` — ℚ(ζ₈) 진폭 Galois 궤도+norm/trace+
  equivariance. certificate layer(진폭 동일성). (**ζ₁₆/ζ₃₂ 고차 cyclotomic·전체 unitary Galois 봉인·dense 와
  겹치지 않는 진짜 제11 독립경로(예: treewidth/그래프-조합)는 아직 없음.**)
- **MTC braid(P4)**: `mtc_braid_observe` — Ising(비보편 Clifford)·Fibonacci(보편) braid Yang-Baxter·pentagon
  핵심(F²=I·φ²=φ+1). (**braid 유니터리 실봉인(ζ₁₆ 승인)·완전 MTC(전 F/R symbol pentagon/hexagon)·Chern-Simons
  level-k·Ising⊗Ising·S-matrix modularity 는 아직 없음.**)
- **3D ℤ₂ Fu-Kane(P6)**: `z2_fukane_observe` — TRIM parity ν₀ 닫힌형==수치, TR-preserved SPT. (**weak indices
  (ν₁ν₂ν₃)·Wilson-loop 전BZ(inversion 없음)·표면상태·crystalline TI·topological superconductor 는 아직 없음.**)
- **lattice surgery(P5)**: `lattice_surgery_observe` — merge/split CNOT 8 branch up to Pauli. (**distance-d
  물리 패치 Tier-2 tableau 실봉인·twist defect·d≥5·multi-patch·color-code surgery 는 아직 없음.**)

### 3j. 예비 판정분 (재제안 시 보강 조건)
- **Hecke 브레이드**(H₃(q=i) Burau·Markov trace)·**정수 나눗셈**·**큐딧 심플렉틱**·**Floquet SPT 정수불변량**·
  **treewidth 그래프-조합 제11경로**(agent07, tensor-net 겹침 정직 대조 필수) — 각 구체 인스턴스·오라클 경로·복리 강화 시 재평가.
- **제11 검증경로(진짜 독립)**: 기존 10 경로 + Galois 후보와 **전제 상이 한 문장 증명** 필수. dense 와 겹치면 강등.

**핵심: 사소한 변형 금지. 질적 새 계층. 괄호 "아직 없음"이 관문이면 환영.**

## 4. 우리가 원하는 것 (방향 감 — 강요 아님)

- **검증 메타** — **진짜 제11 경로**(10 경로+Galois 후보와 전제 상이·dense 안 겹침, 예: treewidth 그래프-조합·회로 동치)·treewidth 부분수축.
- **부호 심화** — lattice surgery **물리 패치 Tier-2 실봉인**·twist defect·d≥5 surgery·color-code·twist.
- **표현론 심화** — A₅ Fourier **√5 실봉인**(경량 승인)·PSL(2,7) ζ₇(진짜 복소 필연)·Hecke·모듈러 표현·2.A₅ 이중피복.
- **동역학 심화** — Floquet SPT 정수불변량·3D ℤ₂ weak indices·topological superconductor·비-abelian Berry.
- **자원 이론 심화** — qutrit/qudit KS·더 큰 KS 집합·상태의존 맥락성·negativity monotone·mana.
- **애니온/TQC 심화** — 완전 MTC(전 F/R pentagon/hexagon·S-matrix modularity)·braid 유니터리 실봉인·CS level-k.
- 그 밖에 **당신이 더 나은 축을 알면 제안하라.**

## 4′. ★성공 패턴 (v1→v11)

**(a) 게이트 우회** · **(b) 직접 닫힌형 구성** · **(c) 승인-module 사람게이트**(닫힌형·surd 우대) · **(d) 반증→회수·
복리** · **(e) 기소비 선점 대조·교차 복리·인프라 즉시 소비** · **(f) 다중 독립 경로·Tier-2 드라이버·오라클 동치
재발견** · **(g) 봉인 전 선검증 반증·Choi/동형 재해석** · **(h) 제8~10 경로·closed-negative 상보 positive·계산기저
함수 대수·rational group 판정·Tier-2 로 dense 회피** · **(i) crux-probe 우선·closed-negative→redirect→positive·
non-coprime LT 소거·사람게이트 필연성 선증명**.

**(j) ★v11 신규 패턴 3개**:
- **선검증이 외부 제안을 정정**: agent07 KS-18 좌표가 basis 와 불일치→**계산 탐색으로 재구성**(기억 의존 배제);
  A₅ "ζ₅ 필연" 주장→**ambivalent 판정으로 √5 충분(ζ₅ 과대) 정정**. 제안의 **구체 좌표/게이트를 봉인 전 반드시
  독립 재검증**하라 — 제안이 틀려도 선검증이 올바른 값을 복원한다.
- **ambivalent 판정 = 실수-vs-복소 게이트 판별**: 군 Fourier 제안 시 **ambivalent(모든 g~g⁻¹)** 여부를 스스로
  점검하라 — ambivalent→모든 문자 실수(√d surd 충분, 복소 ζ 불필요) vs non-ambivalent→복소 ζ 필연. rational
  group 판정(정수 vs surd)의 상위 판별(실수 vs 복소). A₄(ζ₃ 복소)·A₅(√5 실수)가 정반대 실증.
- **certificate layer 정직 강등**: Galois-orbit 은 진폭 **동일성**만 검증하므로 "제11 독립 경로"가 아니라
  "제11 경로 **후보**/certificate layer"로 표기했다. 검증경로 제안 시 **전체 unitary 동치를 주장하는지, 진폭/
  부분 certificate 인지**를 명확히 구분하고, dense 와 겹치면 audit layer 로 스스로 강등하라.

## 5. 반드시 지켜야 할 제약

- **결정론 불가침**·**오라클은 사용만**·**honest decomposition**(MatrixGate 금지)·**self-contained**·**하드웨어 out**.
- **정직 경계** — 근사·확률·측정후처리는 **관측**. exact ≠ 근사, dense ≠ structural ≠ subspace ≠ tableau.
  봉인 ≠ 관측(certificate/witness 는 봉인 자산 아님). **근사 truncation 은 봉인 아님**.
- **★registry 실측 novelty**: 공개 저장소 **https://github.com/sadpig70/QuantaFoundry**
  (`registry/`·`specs/`·`scripts/` 공개) — 접근 가능하면 실측 대조 우대. ★**제안의 구체 좌표/게이트/문자표는
  스스로 독립 재검증**(v11 §4′j 첫째 — 외부 제안 오류가 실재했다). 불가하면 §3 정독 + 구조적 novelty.

## 6. 답변 형식 (제안마다)

**3~5개**를 impact×feasibility 순: 1. **proposal**(축+구체 인스턴스) · 2. **rationale**(정체성·compounding·
교차 복리) · 3. **feasibility**(봉인 게이트·오라클 검증·§4′(b) exact 근거·**봉인 경로 명시**: Tier-0 dense(n≲12)
/Tier-2 tableau/관측·certificate — §4′(i)) · 4. **risk**(정직 경계·certificate/봉인 구분) · 5. **novelty**(§3 특히
**3n/3m/3j** 대조 + 시차 강건성).

## 7. 개념 미니 용어집

- **봉인/compounding/honest boundary/teeth/subspace 강검증/Tier-2/closed-negative/rational group/crux-probe/
  ambivalent(모든 g~g⁻¹→문자 실수)/certificate layer(진폭 동일성, 봉인/제11 독립경로 아님)** — 이전 라운드 정의 유지.
- **검증경로 10 + 제11 후보**: dense·tableau·ZX·path-sum·stab-rank·matchgate·tensor·QMDD·ANF·Gröbner/ℤ[ω]
  phase-ideal **+ Galois-orbit(certificate layer, 진짜 제11 독립경로를 환영한다 — dense 안 겹침 증명 필수).**
