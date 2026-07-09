<!-- QuantaFoundry 수평 확장 아이디어 제안 요청 — v12 (2026-07-09). v1~v11 후속. self-contained. -->
<!-- 외부 모델 런타임에게 전달용. 이 문서 하나만 읽고 제안 가능하도록 작성됨. -->

# QuantaFoundry — 수평적 확장(Horizontal Expansion) 아이디어 제안 요청 · v12

> **v11 → v12 변경점**: v11 요청으로 8개 런타임의 제안(report11)을 받아 **통합 6축(TrackHE11)을 완주·폐합**했다.
> 전 축 **관측/선검증**(신규 봉인 module 0·root 불변). 성과(§3o):
> - **PSL(2,7) ambivalent 선검증**(P2): SL(2,𝔽₇)/{±I} 168원소·6 켤레류·★**order-7 2 클래스 분열 → non-ambivalent
>   → 복소 문자 필연**. 문자체 = **ℚ(√−7)**(Gauss period (−1±i√7)/2, **허수 이차체 차수 2** — 요청서 "ζ₇"(차수 6)
>   보다 경량 redirect). ★**A₅(ambivalent→ℚ(√5) 실수)의 허수 쌍** = ambivalent 판정이 real/imaginary 이차체 쌍을 가른다.
> - ★**A₅ Fourier ℚ(√5) 실현가능성**(P1): ★**Frobenius-Schur 지표 FS(ρ)=+1 (전 5 기약표현)** → 표현행렬(문자뿐
>   아니라)까지 ℝ=ℚ(√5) 위 실현 → 비아벨 DFT 가 **복소 ζ₅ 없이 √5 만**으로 exact. A₄(복소 1-dim FS=0 → ζ₃ 필연)
>   대조. 봉인은 **√5 승인 module** 대기(FS 근거 확보).
> - **qutrit(d=3) 맥락성**(P4): ★**자체 검증이 외부 제안 정정**(3번째) — agent 의 Yu-Oh 13 "uncolorable(KS)" 주장이
>   **KS-COLORABLE**(부등식형, uncolorable 아님)임을 자체 검증으로 정정. 대신 **KCBS pentagon** Σ⟨P_i⟩=√5>2
>   (noncontextual 상한) = state-dependent d=3 맥락성(exact ℚ(√5)).
> - **1D Kitaev chain class-D ℤ₂ 위상초전도체**(P5): Pfaffian (−1)^ν=sign(μ²−4t²)·|μ|<2t→Majorana zero mode.
>   ★**AZ 대칭클래스 D**(particle-hole) — 2D Chern(class A)·3D ℤ₂(class AII) 상보. 닫힌형==수치 winding.
> - **Hecke 대수 H₃(q=i) Burau**(P6): 2×2 ∈ ℤ[i]⊂ℤ[ζ₈](★승인 게이트 0)·Hecke 이차식·braid Yang-Baxter·
>   Ising(k=2) 대수 뼈대. ★**정직 정정**: q+q⁻¹=0 → Markov trace 정규화 특이(비정규화만 exact).
> - **treewidth "제11 경로" 정직 판정**(P3): ★**자가강등** — treewidth 부분수축 = variable elimination =
>   tensor-network(제7) 동일 연산·검증객체=진폭 겹침 → certificate layer(진짜 제11 독립경로 **아님**). 진짜 제11
>   독립경로는 **여전히 미발견**.
> §3o 에 추가. §4′에 v12 신규 패턴 3(★**Frobenius-Schur=전체 Fourier 실현판별·ambivalent 이차체 real/imaginary
> 쌍·진짜 제11 경로 미발견 공개과제**).

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
- ★**Tier-0 dense 실질 상한 ≈ 12큐빗**. 그 이상 Clifford=**Tier-2 tableau**·비-Clifford 대형=**관측** — 봉인 경로 명시(§4′i).

## 3. EXCLUDE — 이미 구현·봉인·관측된 것 (재제안 금지)

현재 **95 modules / 466 sealed apps** (root `6e7d2a70ef9e1790…`). **독립 검증경로 10개**
(dense·tableau·ZX·path-sum ℤ[ω₈]·stabilizer-rank·matchgate/SO(2n)·tensor-network·QMDD·ANF/bit-vector·
Gröbner/ℤ[ω] phase-ideal) **+ 제11 후보/certificate layer**(Galois-orbit·treewidth 자가강등, §3o). ★진짜 제11 미발견.

### 3a~3m. v1~v9 소비분 (요약 — 상세는 이전 라운드 EXCLUDE 계보)
- **기초/QFT/QPE/Grover/Trotter·VQE·QAOA/쿼리/walk** · **QEC**(repetition·Steane·Shor-9·transversal Clifford·
  연접[[25,1,9]]·RM[[15,1,3]]·HGP[[27,4,3]]·cyclic BCH[[15,7,3]]/[[31,11,5]]) · **Shor**(15·21·frontier…235·factory) ·
  **QSVT 완비** · **Fermionic**(JW/BK/parity·fSWAP·Bogoliubov Pfaffian) · **비아벨 Fourier**(S₃/D₄/S₄/Q₈/B₃) ·
  **위상 논리연산·MBQC·Z₂ gauge·Schur·AKLT·CPTP·2/3-design·PEPS·MUB·GF(8)·Fibonacci/Majorana braid·C₃ phase-poly·
  RS·[[8,3,2]] CCZ** · **동역학**(dual-unitary·Floquet·OTOC·매듭·2D Chern) · **자원**(magic·채널 diamond) ·
  **contextual fraction·A₄ ζ₃ 선검증·code switching(RM15)·Ising 융합·qutrit Wigner** · **검증경로 1~10**.

### 3n. v10 소비분 (TrackHE10)
- **KS-18 맥락성**(d=4) · **A₅ ζ₅-vs-√5 redirect** · **Galois-orbit 제11 후보** · **MTC braid**(Ising/Fibonacci) ·
  **3D ℤ₂ Fu-Kane** · **lattice surgery merge/split CNOT**(논리 관측).

### 3o. ★v11 소비분 — 통합 6축 (TrackHE11, 이번 라운드 신규 — 재제안 금지)
- **PSL(2,7) ambivalent 선검증(P2)**: `psl27_observe` — non-ambivalent→ℚ(√−7) 복소(Gauss period). A₅ 실수쌍의
  허수쌍. (**PSL(2,7) Fourier 실봉인(DFT-realization field √−7 or ζ₇ 미확정)·PSL(2,q) family·2.A₅ 이중피복은 아직 없음.**)
- **A₅ Fourier ℚ(√5) 실현가능성(P1)**: `a5_fourier_observe` — Frobenius-Schur FS=+1 전 irrep→√5 만으로 전체 DFT.
  (**A₅ Fourier 실봉인(√5 승인 module)·A₆·정규화 스칼라 √(dim/60) 처리는 아직 없음.**)
- **qutrit 맥락성(P4)**: `ks_qutrit_observe` — Yu-Oh 13 colorable(자체정정)·KCBS √5 state-dependent. (**진짜
  uncolorable d=3 KS(Peres-33·Conway-31)·qudit d≥5 KS·negativity monotone 은 아직 없음.**)
- **Kitaev class-D(P5)**: `kitaev_class_d_observe` — 1D BdG ℤ₂ Pfaffian. (**2D class D(p+ip Chern)·class DIII·
  다중밴드·Fidkowski-Kitaev ℤ₈ 상호작용 축소는 아직 없음.**)
- **Hecke H₃(q=i)(P6)**: `hecke_h3_observe` — Burau ℤ[i]·gate 0·Ising 뼈대. (**일반 q Jones·Hₙ(n>3)·knot 불변량·
  HOMFLY·Temperley-Lieb(q=−1) 정수는 아직 없음.**)
- **treewidth 정직 판정(P3)**: `treewidth_verdict_observe` — 자가강등(tensor-net 겹침). (**진짜 제11 독립경로=미발견 공개과제.**)

### 3j. 예비 판정분 (재제안 시 보강 조건)
- **full MTC**(S-matrix modularity·SU(2)₃·CS level-k)·**Floquet SPT 정수불변량**·**3D ℤ₂ weak indices**·
  **lattice surgery 물리 패치 Tier-2 실봉인**·**정수 나눗셈**·**큐딧 심플렉틱** — 구체 인스턴스·오라클·복리 강화 시 재평가.
- ★**진짜 제11 검증경로(공개과제)**: 10 경로 + Galois/treewidth 후보(전부 자가강등)와 **검증 객체가 상이한 새 수학
  대상**. dense/진폭·stabilizer·ZX·위상다항식·ANF·Gröbner·텐서·QMDD·Galois 궤도·treewidth 어느 것과도 안 겹쳐야 함.
  "전체 unitary 동치를 조합/대수 불변량으로 판정"하는 구성이 아직 없다.

**핵심: 사소한 변형 금지. 질적 새 계층. 괄호 "아직 없음"이 관문이면 환영.**

## 4. 우리가 원하는 것 (방향 감 — 강요 아님)

- **검증 메타** — ★**진짜 제11 경로**(위 §3j 공개과제, certificate layer 강등 아닌)·회로 동치 증명서.
- **표현론 심화** — A₅ Fourier **√5 실봉인**(FS 근거 완료)·PSL(2,7) Fourier(√−7/ζ₇)·2.A₅ 이중피복·Hₙ Hecke·모듈러 표현.
- **부호 심화** — lattice surgery **물리 패치 Tier-2 실봉인**·twist defect·color-code surgery·d≥5.
- **동역학 심화** — Floquet SPT 정수불변량·2D class D(p+ip)·class DIII·3D ℤ₂ weak indices·비-abelian Berry.
- **자원 이론 심화** — 진짜 uncolorable d=3 KS(Peres-33)·qudit KS·negativity monotone·mana.
- **애니온/TQC 심화** — 완전 MTC(S-matrix modularity·pentagon/hexagon 전체)·SU(2)₃·CS level-k·knot 불변량.
- 그 밖에 **당신이 더 나은 축을 알면 제안하라.**

## 4′. ★성공 패턴 (v1→v12)

**(a) 게이트 우회** · **(b) 직접 닫힌형 구성** · **(c) 승인-module 사람게이트**(닫힌형·surd 우대) · **(d) 반증→회수·
복리** · **(e) 기소비 선점 대조·교차 복리·인프라 즉시 소비** · **(f) 다중 독립 경로·Tier-2 드라이버·오라클 동치
재발견** · **(g) 봉인 전 선검증 반증·Choi/동형 재해석** · **(h) 제8~10 경로·closed-negative 상보 positive·계산기저
함수 대수·rational group 판정·Tier-2 로 dense 회피** · **(i) crux-probe 우선·closed-negative→redirect→positive·
non-coprime LT 소거·사람게이트 필연성 선증명** · **(j) 선검증이 외부 제안 정정·ambivalent=실수/복소 판별·
certificate layer 정직 강등**.

**(k) ★v12 신규 패턴 3개**:
- **Frobenius-Schur 지표 = 전체 Fourier 실현 판별**: ambivalent(문자 실수) 는 필요조건일 뿐 — ★FS(ρ)=+1(실수형)
  이라야 **표현행렬(문자뿐 아니라 전체 DFT)까지** ℝ=ℚ(√d) 위 실현(복소 불필요). FS=−1(quaternionic)·FS=0(복소형).
  군 Fourier 실봉인 제안 시 **ambivalent + FS 지표**를 함께 제시하라(A₅ FS=+1→√5 전체 DFT 실현 실증).
- **ambivalent 이차체 real/imaginary 쌍**: A₅(ambivalent→ℚ(√5) 실수) ↔ PSL(2,7)(non-ambivalent→ℚ(√−7) 허수)
  = 이차체 쌍. non-ambivalent 라도 **문자체가 이차 허수체(경량)** 일 수 있음 — full cyclotomic ζ_k 는 상한(과대).
  Gauss period 로 **최소 문자체(√±d)**를 먼저 구하라(ζ₇→√−7 정정처럼).
- **진짜 제11 경로 = 미발견 공개과제**: Galois-orbit·treewidth 모두 자가강등(진폭/tensor-net 겹침). 진짜 제11 은
  **검증 객체가 10 경로 어느 것과도 상이한 새 수학 대상**을 요구한다 — 억지 제안 대신, "전체 unitary 동치를 dense
  와 무관한 조합/대수 불변량으로 판정"하는 구성을 확보한 뒤 제출하라(§4′j 셋째 규율 준수).

## 5. 반드시 지켜야 할 제약

- **결정론 불가침**·**오라클은 사용만**·**honest decomposition**(MatrixGate 금지)·**self-contained**·**하드웨어 out**.
- **정직 경계** — 근사·확률·측정후처리는 **관측**. exact ≠ 근사, dense ≠ structural ≠ subspace ≠ tableau.
  봉인 ≠ 관측(certificate/witness 는 봉인 자산 아님). **근사 truncation 은 봉인 아님**.
- **★registry 실측 novelty + 제안값 자체 재검증**: 공개 저장소 **https://github.com/sadpig70/QuantaFoundry**.
  ★**제안의 구체 좌표/문자표/필드/주장은 스스로 독립 재검증**(v12 §4′j·k — 외부 제안 오류가 반복 실재: KS-18
  좌표·A₅ ζ₅·Yu-Oh 13 colorable·treewidth 강등). 불가하면 §3 정독 + 구조적 novelty.

## 6. 답변 형식 (제안마다)

**3~5개**를 impact×feasibility 순: 1. **proposal**(축+구체 인스턴스) · 2. **rationale**(정체성·compounding·
교차 복리) · 3. **feasibility**(봉인 게이트·오라클 검증·§4′(b) exact·**봉인 경로 명시**: Tier-0 dense/Tier-2/관측/
certificate) · 4. **risk**(정직 경계·certificate/봉인 구분) · 5. **novelty**(§3 특히 **3o/3n/3j** 대조 + 시차 강건성).

## 7. 개념 미니 용어집

- **봉인/compounding/honest boundary/teeth/Tier-2/closed-negative/rational group/crux-probe/ambivalent(문자 실수)/
  Frobenius-Schur(FS=+1 실수형→√d 전체 DFT 실현)/certificate layer(진폭/부분 동일성, 봉인·제11 독립경로 아님)** — 유지.
- **검증경로 10 + 제11 후보(강등)**: …ANF·Gröbner/ℤ[ω] + Galois-orbit·treewidth(자가강등). ★진짜 제11 독립경로 미발견 —
  검증 객체가 10 경로 어느 것과도 상이한 구성을 환영한다.
