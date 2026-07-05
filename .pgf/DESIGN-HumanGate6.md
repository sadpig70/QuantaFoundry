# DESIGN-HumanGate6 — 사람게이트 6건 단계별 개창 작업계획서

> 입력: `_workspace/integrated_horizontal_expansion3.md` §3 (TrackHE3 통합채점의 사람게이트 대기 목록).
> **v1.1 (2026-07-05)**: PGF 3관점 설계리뷰(P5 Feasibility·P7 Risk·P8 Architecture, 판정 REVISE:
> Critical 2·High 5) 반영 전면 개정. 변경 요지는 문서 말미 "리뷰 반영 기록" 참조.
> 원칙: §4′ 직접 닫힌형 구성(탐색 금지) · 신규 module 최소화 · **승인 게이트 = 신규 module 각도가
> *확정되는 시점*에 명세(각도·개수·닫힌형 근거·YPowGate 표현·field 공시)를 보고하고 정욱님 승인 후 봉인**.
> 계획서 승인 ≠ module 승인 — 두 게이트는 분리다. 절대규율(결정론·fingerprint·frozen·honest split) 전부 상속.

---

## 실행 순서 (정책이며 의존 아님 — @dep 는 진짜 의존에만)

| 순서 | 건 | 승인 게이트 | 비고 (리뷰 반영) |
|---|---|---|---|
| G1 | PEPS 2×2 RVB | 없음 — **module 0 판정 완료** | G1c만 잔여 (3분해) |
| G2 | 2q 2-design | 없음 | ★재정의: 하한 226 이 **가중 설계에도 유효**(span rank 논증) → unitary 2-design 소형 부분집합은 **수학적 불가 = closed-negative 반증 문서화**가 1급 산출물 + 대체 payoff(MUB-20 state 2-design, Clifford) 옵션 |
| G3 | π/6·π/3 각도 family | ★승인 1회 → **2축 확정 + 1축 조건부**(채널 γ¼·Szegedy p¼ 확정, POVM 은 A6 검증 후) | G4가 이 family 에 hard-dep |
| G4 | Schur n=4 | ★조건부 — **module 0 가능성 높음**(arccos√(2/3)=ry_cg_half 각도와 동일·√(3/4)→π/6=G3) | G4a 팔레트 환원 검사가 판정 |
| G5 | Fibonacci anyon | ★최대 게이트: **새 대수체 ℚ(ζ₅,√φ) — 차수 8 확장**(정정: ℚ(√5,ζ₅) 아님) + module 2~3 | Euler 분해 확보됨 |
| G6 | 종결 동기화 | — | 각 G가 terminal(done **또는 closed-negative/blocked-final**)이면 충족 |

**병렬 규칙**: a-노드(read-only 설계·numpy 선검증)는 승인 대기 중에도 선행 가능(봉인 0·무위험).
c-노드(봉인·커밋)만 한 번에 하나(순서 정책). — P7 High 반영.

---

## Gantree

```
HumanGate6 // 사람게이트 6건 단계별 개창 (in-progress) @v:1.1
    G1_PepsRvb // 2×2 RVB PEPS — 2D 텐서망 새 클래스, module 0 확정 (done)
        G1a_Analyze // RVB 상태 닫힌형 선분석 (done)
            # ✅ 2026-07-05 numpy: |RVB⟩=|cov_H⟩+|cov_V⟩(H={01,23}·V={02,13}), ⟨H|V⟩=+1/2·norm²=3.
            #   진폭 전부 실수 ±1/√12(4개)·∓1/√3(0110·1001), amp²∈{1/12,1/3}. 순차 분기 확률
            #   {1/2; 1/6·5/6; 1/5·4/5·0·1; 0·1} 전부 유리수. ★S_tot²|RVB⟩=0 exact(singlet witness).
            # ⚠dimer orientation = golden 자유도(수직쌍 방향 반전 시 ⟨H|V⟩=−1/2·norm²=1 인 다른 상태,
            #   P7 검증) → golden 정의에 singlet 방향 (i<j: |01⟩−|10⟩)/√2, covering pair 순서 고정 명시.
        G1b_GateDecision // module 0 ↔ 신규각 분기 (done) @dep:G1a_Analyze
            # ✅판정: **신규 module 0** — Ry 가법성: P=1/2→ry_pi2 · θ(1/6)=2arccos√(1/6)=ry_k6² ·
            #   상보 π−θ=ry_pi2²·(ry_k6_dag)² · CCRy 반각=ry_k5 · multiplexer 보정 θ−π/2=ry_k6²·ry_negpi2 ·
            #   결정 분기=X/CNOT/toffoli · 부호(0110/1001 음)=차수≤2 위상다항식 → Z/CZ 로 GF(2) 가해(P7 확인).
            #   P5·P7 리뷰 수치 재검증 통과(판정 견고). 승인 게이트 불필요.
        G1c1_CircuitDesign // 회로 구성 numpy == RVB golden 선검증 (done) @dep:G1b_GateDecision
            # ✅ 2026-07-05 1회 통과: **33스텝 plan** — site0 ry_pi2 → site1 multiplexer(ry_pi2·CX·
            #   [ry_k6²·ry_negpi2]·CX) → site2 분기 3블록(00→X-켤레 toffoli·01→CCRy 반각=ry_k5·
            #   10→CCRy 반각=ry_pi2·ry_k5_dag, anti-control=X 켤레) → site3 parity(CNOT×3, 전 support
            #   weight=2 강제) → 부호층 f=x0+x0x1+x0x2+x1x2 = Z(0)·CZ(01)·CZ(02)·CZ(12).
            #   ‖U|0000⟩−|RVB⟩‖=3.3e-16 · 유니터리 ✓ · module 10종 전부 기봉인(신규 0 재확인):
            #   {ry_pi2, ry_negpi2, ry_k5±, ry_k6, x, z, cnot, cz, toffoli}. orientation 고정(i<j: |01⟩−|10⟩).
        G1c2_SealForge // peps22_rvb spec + forge 봉인 (done) @dep:G1c1_CircuitDesign
            # ✅ 2026-07-05 1회 통과: specs/apps/peps22_rvb.app.pg(33스텝 plan·honest 주석=정의 열만
            #   RVB 물리) + APP_LIST 등록 → **SEALED Tier-0 u_hash 4d67b986** · 신규 module 0 ·
            #   재발견 교차검증 12/12 불변. 커밋은 G1c3 사이클 완주 후(verified-only).
        G1c3_Observe // peps_observe + 사이클 완주 (done) @dep:G1c2_SealForge
            # ✅ 2026-07-05: peps_observe(3ai) — 정의열==dimer 정의 재구성 3.3e-16 · S_tot²=0 exact ·
            #   각 사이트 reduced ρ=I/2 · teeth 2종(orientation 반전·각도 오염) 검출. 사이클 완주:
            #   registry 290 apps · root e40a8eaf→**7293a3de4baa50ba** · anchor PASS · second_oracle 79/79 ·
            #   guard ALL PASS · reproduce --changed-only REPRODUCED(41스텝 0 fail). G1 폐합.
    G2_TwoQubit2Design // 2q 2-design — ★closed-negative 반증 + 대체 payoff (done)
        # 순서: 문서 순서=실행 순서(정책). G1 과 데이터 의존 없음 — a-노드는 언제든 선행 가능.
        G2a_MathVerify // 하한 정리 판정 + 반증 문서화 (done — ★closed-negative)
            # ✅ 2026-07-05 반증 리포트 고정: scripts/twoq_2design_bound.py → .pgf/proofs/TWOQ-2DESIGN-BOUND.json
            #   (결정론 seed=0). ①K(d)=dim span{vec(U⊗Ū)} 2경로(Haar 표본·Clifford 원소) rank 포화:
            #   **10/10(d=2)·226/226(d=4) = d⁴−2d²+2 공식 일치** — 하한(GAE 2007)은 원소당 기여 방향 1개
            #   논증이라 가중 설계에도 유효. ②1q 캘리브레이션: C₁ 24원소 F₂=2 + ★12원소 사면체(Pauli⋊C₃)
            #   부분군 F₂=2(하한 10≤최소≤12 정합, V8 24개=군 폐포 봉인 정직 기록). ③외부 "21원소" 주장=
            #   하한 226 위반 **반증 확정**; 정체=d=4 MUB 20-state(가환 Pauli 5-분할 {ZI,IZ}·{XI,IX}·
            #   {YI,IY}·{XZ,ZY}·{ZX,YZ})가 projective **state** 2-design(FP=1/10 exact, 상호비편향 전수
            #   확인)임을 실증 — unitary/state design 혼동. 봉인 0·root 불변. **G2 unitary-design 트랙 정직 종결.**
        G2b_StateDesignOption // ★대체 payoff: MUB-20 state 2-design (Clifford, module 0) (done) @dep:G2a_MathVerify
            # ✅ 2026-07-05 규모 게이트 승인(정욱님 "진행") → 완주: mub4_b{1..5}_s{0..3} **20앱 Tier-0
            #   봉인**(신규 module 0 — x/h/s/cz 기봉인 Clifford word). ★닫힌형 직접 구성(탐색 0):
            #   V1=I·V2=H⊗H·V3=(SH)⊗(SH)·**V4=CZ·(H⊗SH){XZ,ZY}·V5=CZ·(SH⊗H){YZ,ZX}** — 스태빌라이저
            #   켤레 V·Z0·V†=+A·V·Z1·V†=+B 부호 포함 정확(numpy 선검증 1회 통과). mub_observe(3aj):
            #   Pauli 라벨맵 20/20(회로 독립)·비편향 400쌍·FP=1/10+2차모멘트==0.1·Πsym(이중 witness)·
            #   ★소비 데모=MUB 완비측정 단층재구성 ρ=Σp·Π−I exact(순수+혼합)·teeth 2종(T-오염·기저제거).
            #   honest: state 2-design(unitary 아님) 용어 정직·확률=해석값(유한샘플 shadow 미구현, 기반만).
            #   290→**310 apps**·root 7293a3de→**b82d79eb24d14ee5**·second_oracle 79/79·guard ALL PASS.
            #   **G2 폐합**: closed-negative 반증(G2a)+정직한 알맹이 회수(G2b) — 반증→회수 패턴 완결.
    G3_AngleFamilyPi6 // π/6·π/3 family 승인 1회 → 2+1축 소비 (done — 2026-07-05 완주)
        # ✅ 승인 module 2(ry_pi6/negpi6) → 소비 5앱(채널 ¼ 3·Szegedy p¼ 1·naimark_ud3 1) 일괄 봉인.
        #   85→87 modules·310→315 apps·root b82d79eb→008e09334c543c7c. G4 hard-dep 해소.
        G3a_DeriveAngles // 3축 필요 각도 정확 도출 (done)
            # ✅ 2026-07-05 numpy 선검증 17항 ALL PASS: ①γ=¼: CRY(π/3)=반각 Ry(±π/6) 분해 exact +
            #   3채널(bitflip/phasedamp/ampdamp) Tr_env==Kraus γ¼ 통과 ②Szegedy p=¼: Ry(2π/3)=ry_pi6⁴
            #   가법 폐포 ③★A6 해소: 리뷰 {2/3,1/24,1/8,3/8} 정체=UD-POVM(|ψ±⟩=Ry(±π/3)|0⟩, overlap ½)
            #   canonical √E 성분 — **rank-1 Kraus 자유도(M=√λ|0⟩⟨χ|)로 V 진폭² {2/3,1/6,1/2} 환원**
            #   = arccos√(2/3)=ry_cg_half(float-identical)+dyadic → POVM 축 신규각 불필요(G3e module 0
            #   전망, 승인 범위 제외). 부수: ④팔레트 도달불가 witness(ℤ-조합 3.9M 스캔, 최근접 3.27e-7
            #   =near-miss) ⑤field=ℚ(√2,√3) 신규 대수체 없음 ⑥seal_module 드라이런 성공(u_hash 예보
            #   ry_pi6 9372e737·ry_negpi6 6cd2dc18, registry 무접촉) ⑦second_oracle surd 제1원리 초안.
        G3b_ApprovalGate // ★정욱님 승인: 신규 module 집합 (done — 승인 2026-07-05) @dep:G3a_DeriveAngles #HUMANGATE
            # ✅ 정욱님 승인("너가 제시한 작업을 진행한다") → **ry_pi6/ry_negpi6 봉인 완료**
            #   (u_hash 9372e737·6cd2dc18 — 드라이런 예보와 byte-identical, 결정론 재현).
            #   second_oracle 제1원리 surd 추가(81/81). frozen 23키/fingerprint 무훼손 재확인.
        G3c_SealChannelG14 // stinespring_*_g14 (γ=¼ family) 봉인+channel_observe 확장 (done) @dep:G3b_ApprovalGate
            # ✅ 3앱 Tier-0: bitflip_g14(Ry(π/3)=ry_pi6², 3스텝)·phasedamp_g14(CRY(π/3) 반각, 4스텝)·
            #   ampdamp_g14(5스텝). channel_observe 가산 확장: Tr_env==Kraus ¼ 3/3 exact·teeth(0.8·π/3)·
            #   ★합성 복리: γ¼∘¼==7/16 + **교차 γ¼∘½==γ½∘¼==5/8**(감쇠 격자 결합) exact. 레거시 ½ 규약 주석.
        G3d_SealSzegedyP14 // szegedy_2state_p14 봉인+szegedy_observe 확장 (done) @dep:G3b_ApprovalGate
            # ✅ Tier-0(12스텝): P=[[¼,¾],[¼,¾]] — ★첫 비대칭(가역) 연쇄. golden=Szegedy 정의식 직접
            #   (회로 독립). R_A=I⊗(VZV†), V=Ry(2π/3)=ry_pi2·ry_pi6. szegedy_observe 가산 확장:
            #   일반 discriminant D=√(P∘Pᵀ) 경로(eig {0,1}→위상{0,±π})·정상분포 π=(¼,¾) 비균일
            #   +1 고유벡터 exact·teeth. p12 관측 무변경.
        G3e_SealNaimark // naimark_ud3 — 정방 유니터리 완성 봉인 + POVM witness 관측 (done) @dep:G3b_ApprovalGate
            # ✅ Tier-0 8×8(23스텝, ★신규 module 0 — G3a rank-1 판정 실현: ry_cg_half±+dyadic+x/cnot/cz/
            #   toffoli). 회로=①anti-ctl CRY(arccos⅓) ②ctl-X ③CRY(π/2) ④CCRy(−π) ⑤★W 간섭층
            #   (B=CH·CNOT, CCX, B†) — 선검증 중 W층 없는 프로토타입이 **대각 POVM 붕괴(UD 실패)**로
            #   반증돼 재설계(sys which-path 코히런트 소거가 가능조건, ⟨t0|t1⟩=0). naimark_observe(3ak):
            #   E_k 재구성==IDP 정의 exact·ΣE=I·오식별 0·성공 ½(최적)·dilation 통계==Tr(Eρ)·teeth 2종
            #   (틀린각+★W층 잘림→대각화+오식별 0.25 검출=간섭층 하중 실증). SIC/trine=봉인불가 정직경계.
    G4_Schur4 // n=4 Schur-Weyl irrep splitter — ★module 0 확정·완주 (done — 2026-07-05)
        # ✅ G3b 승인으로 hard-dep 해소 → 전 노드 1회 통과 완주. 87모듈 불변·316앱.
        G4a1_PaletteReduction // 기존 팔레트 가법성 환원 검사 (done)
            # ✅ 전수 나열 확정: 4번째 스핀 CG 결합 혼합계수 √((j₃+m+½)/(2j₃+1)) ∈ {√¾,√½,√¼}
            #   → Givens 전각 {π/3, π/2, 2π/3} → 반각 {π/6=ry_pi6, π/4=ry_pi4, π/3=ry_pi6²} 전부 기봉인.
            #   라우팅 {x, cnot, c3x} 기봉인 · n=3 단계 각도는 schur3 sub-app 재사용으로 불요.
            #   **신규 module 0 확정 → G4b 스킵.**
        G4a2_CGGoldenDesign // 독립 CG golden(16×16)+j-사다리 설계 (done) @dep:G4a1_PaletteReduction
            # ✅ 16 = j=2(5)⊕j=1(3×3: 3/2경로·A·B)⊕j=0(2: A·B). golden=CG 계수 직접(schur3 라벨 부호
            #   규약 상속: 011=−|½,−½⟩_A → 0111=−|1,−1⟩_A 문서화). label map=|schur3 label⟩|q3⟩ 합성
            #   (spec 헤더 명시). 5 Givens 쌍: (0010,0001)π/3·(1010,0011)π/2·(1110,1011)2π/3·
            #   (0110,1001)π/2·(1100,0101)π/2 — 쌍 전부 서로소(순서 무관).
        G4a3_CascadeRouting // 2-level Givens 라우팅 plan + numpy 전수 일치 (done) @dep:G4a2_CGGoldenDesign
            # ✅ 1회 통과: plan = W(46스텝: 쌍별 CNOT(q3→·) 라우팅+X-켤레+CCCRy=c3x·반각·c3x·반각)
            #   → ★schur3 sub-app(q0,q1,q2) — 합성 == CG golden **exact 16×16 전수(dev 1.7e-16)** ·
            #   MatrixGate 0 · 신규각 0 최종 확정.
        G4b_ApprovalGate // ★조건부 승인 (done: skipped-no-new-module) @dep:G4a3_CascadeRouting #HUMANGATE
            # ✅ G4a1 module 0 확정 → 계획서 규율대로 승인 게이트 스킵 종결(보고서 불요).
        G4c_SealObserve // schur4 봉인 + schur4_observe (done) @dep:G4b_ApprovalGate
            # ✅ schur4 SEALED Tier-0 u_hash 9ec8eb81(★첫 sub-app 복리 Schur: schur3 재사용).
            #   schur4_observe(3al): U†J²U=diag{6×5,2×9,0×2}·U†JzU label map 16 전수·S₄ duality
            #   (섹터보존+[4] P=+1 전수+[3,1] χ(전치)=1(m별 trace 3)+[2,2] χ=0)·teeth 2종(CG 오염
            #   √¾→√0.7 off-diag 검출·label 열교환 j=2↔1 검출). 기존 schur_observe 불변(가산-only).
    G5_Fibonacci // Fibonacci anyon braid — 새 대수체 (in-progress — G5b 승인 대기)
        G5a_DesignBraid // R/F 닫힌형·B₃ 표현 설계 (done)
            # ✅ 2026-07-05 선검증 14항 ALL PASS: R/F 닫힌형(F²=I·F=F†)·σ₁=R·σ₂=FRF ·
            #   ★Yang-Baxter exact · ★B₃ 중심 (σ₁σ₂)³=e^{2πi/5}I(0.4π 정확) · Euler 분해 재현 ·
            #   비-Clifford witness(Clifford-24 overlap σ₁ 0.9877·σ₂ 0.9715 <1).
            # ★module 확정 **2개**(≤3): z5_gate=Z^(1/5)=ZPowGate(t=1/5)(★t_gate 선례 비대칭 표현으로
            #   ζ₂₀ 봉인계수 배제 — e^{iπ/5}=ζ₁₀=−ζ₅³∈ℚ(ζ₅); 전역위상 ζ₂₀=C4 흡수 판정 완료;
            #   (z5)⁵=z_gate 재발견 단언 예정) + ry_fib=Ry(2arccos φ⁻¹)(√φ 캐리어,
            #   ★sin(반각)=φ^{−½} 항등으로 두 계수가 √φ 하나로 닫힘). plan word 환원 선검증:
            #   σ₁=z5⁷·σ₂=[z,ry_fib]z5⁷[z,ry_fib] up-to-phase exact. 드라이런 2/2(u_hash 예보
            #   a60ac94b·25614750, registry 무접촉). second_oracle surd 초안(π-free) 포함.
        G5b_ApprovalGate // ★정욱님 승인: 새 대수체 ℚ(ζ₅,√φ) 도입 + module 집합 (in-progress — 승인 대기) @dep:G5a_DesignBraid #HUMANGATE
            # 보고서 정본 고정: **.pgf/approvals/G5-fibonacci.md** (2026-07-05) — ①새 대수체
            #   ℚ(ζ₅,√φ) 차수 8(N(φ)=−1 수치 확인, 축소 보고 없음) ②module 2(z5_gate·ry_fib).
            #   승인→G5c(fib_braid_s1/s2+observe)→G6 · 부결→blocked terminal(G6 직행).
        G5c_SealObserve // fib_braid_s1/s2 봉인 + fib_braid_observe (designing) @dep:G5b_ApprovalGate
            # witness: Yang-Baxter exact · ★B₃ 중심 **(σ₁σ₂)³=e^{2πi/5}·I**(P5/P7 수치 확정 — ⁵ 아님) ·
            #   비-Clifford witness(stabilizer fidelity<1, magic_a 패턴) · teeth.
            #   universality/근사컴파일 주장=범위 밖 정직경계. 신규 스크립트 fib_braid_observe.py
            #   (기존 braid_observe.py=Ising 불변, 가산-only).
    G6_Closure // 종결 — 정본·외부문서·메모리 동기화 (designing) @dep:G1_PepsRvb,G2_TwoQubit2Design,G3_AngleFamilyPi6,G4_Schur4,G5_Fibonacci
        # @dep 의미(P8/P7): 각 선행 G 가 **terminal**(done 또는 closed-negative/blocked-final+사유)이면 충족.
        #   승인 부결도 정당한 terminal — 오히려 동기화가 더 필요. G7+ 확장=노드 추가+이 @dep 1개 추가로 국소화.
```

## 공통 PPR

```python
def HUMAN_GATE(report) -> bool:
    """외부 게이트(정욱님) — AI_ 아님(판단 주체가 사람인 제3범주, P8 승인 표기).
    해당 #HUMANGATE 노드를 (in-progress)로 전이, 보고서를 .pgf/approvals/에 고정 후 실행 중단·응답 대기.
    승인→True·(done) / 부결→False·(blocked)+사유(=정당한 terminal, G6 @dep 충족)."""

def run_gate_G(node) -> Literal["done", "closed-negative", "blocked"]:
    """각 G 공통 실행자 — 중심 루프(decompose→gate→execute).
    병렬 규칙: a-노드(read-only 설계)는 타 G 승인 대기 중에도 선행 가능. c-노드(봉인·커밋)만 직렬."""
    design = numpy_preverify(node)                    # 닫힌형·각도 전수·golden 독립 유도 (실제 코드)
    if design.mathematically_infeasible:              # G2 경로: 하한 위반 등
        write_refutation_report(design)               # 반증 문서화 = 1급 산출물
        return "closed-negative"                      # 정직 종결 — G6 @dep 충족하는 terminal
    if design.new_modules:
        report = AI_compose_approval_request(design)  # 각도·개수·근거·field 공시·소비처·불변 확인
        if not HUMAN_GATE(report):
            return "blocked"                          # 사유 기록 — terminal
        seal_modules(design.new_modules)              # seal_module.py + second_oracle 제1원리 추가
    seal_apps(design.specs)                           # forge_apps --changed-only
    observe(design.witness)                           # 신규 관측 스크립트(기존 observe 는 가산-only) + reproduce_all 등록
    return standard_cycle_gates()                     # = HANDOFF §Definition-of-done 전체 체인:
    # registry build → semantic_guarantee → citation_gen → seal_gate_ci(anchor) → second_oracle
    # → verify_contested_guard → reproduce_all --changed-only → fingerprint 확인 → 문서 3곳 갱신 → commit·push
    # acceptance_criteria:
    #   - 신규 봉인 전부 Tier-0 exact (dense) · fingerprint/frozen byte-identical
    #   - second_oracle 전수 PASS(신규 module 은 제1원리 구성 포함) · guard ALL PASS
    #   - observe all_ok=True + teeth 검출 · reproduce_all --changed-only REPRODUCED
    #   - verified-commit only · 마스터/HANDOFF/이 문서 3곳 status 동기화
```

## 리스크 / 가정 (검증시점 포착용)

- **A1(G1)**: ~~각도 미확정~~ → 해소(G1b done). 잔여: G1c1 회로==golden 열 일치 실패 시 재설계 1회 후 blocked.
- **A2(G2)**: ~~하한이 맞으면 불가~~ → **확정**(가중 포함 하한 226): G2 정상 종결=closed-negative 반증 문서화.
  대체 payoff(G2b MUB state 2-design)는 규모 게이트(20앱) 1줄 확인 후.
- **A3(G3)**: ~~oracle exact 처리 미확인~~ → **해소**(G3a ⑥): seal_module 드라이런 2/2 성공
  (C1-C4 통과·fingerprint 현행 일치·스크래치 store, registry 무접촉).
- **A4(G4)**: n=4 CG cascade 라우팅 복잡도 — 탐색 금지 유지, G4a3 실패 시 재설계 1회 후 blocked.
- **A5(G5)**: 새 대수체 ℚ(ζ₅,√φ)와 second_oracle float 대조 경로 충돌 — √41(ry_ak41) 선례상 float-경유
  가능성 높으나 제1원리 구성(기호)을 승인 요청서에 포함해 선판정. 전역위상 ζ₂₀ 흡수 여부 포함.
- **A6(G3, 신규 — P7)**: ~~POVM 축 미검증~~ → **해소**(G3a ③): rank-1 Kraus 자유도로 V 진폭²
  {2/3,1/6,1/2} = ry_cg_half+dyadic 격자 재도출 성공 — POVM 축 신규각 불필요, G3e=module 0 전망
  (정방 완성 순차 조건화는 G3e 선검증에서 최종 확정).
- **A7(공통, 신규 — P7)**: frontier factory 무인 라운드 인터럽트 시 root/anchor 이동 —
  각 G 의 c-노드 착수 전 `git log`+`seal_gate_ci` 로 현재 anchor 재확인(선례: factory anchor 버그 수동복구).

## 리뷰 반영 기록 (v1.0 → v1.1, 2026-07-05)

- 3관점 리뷰 판정 REVISE(Critical 2·High 5·Medium 8·Low 8) → 전 이슈 반영:
- **[C, P7]** G5 field ℚ(√5,ζ₅)→**ℚ(ζ₅,√φ) 차수 8** 정정(√φ∉ℚ(√5,ζ₅), N(φ)=−1). Euler 분해·ζ₂₀ 위상 명시.
- **[C, P7]** G2 자기모순 해소: 하한=span rank(가중 포함 유효) → closed-negative 반증=1급 산출물로 재정의
  + 대체 payoff G2b(MUB-20 state 2-design, unitary/state 용어 정직) 신설.
- **[H, P8/P7/P5]** G1~G5 간 순서용 @dep 전면 제거(문서 순서=정책), 진짜 의존만 잔존(G4→G3b hard, 근거 명시).
  G6=multi-dep, terminal(done/closed-negative/blocked-final) 의미 정의. a-노드 병렬 허용(선행설계 금지 조항 삭제).
- **[H, P5]** G3e isometry 봉인 → unitary completion+POVM witness split 재설계, 무선례 문구 정정.
- **[H, P5]** G4 "신규 2쌍" 판정 오류 정정 → G4a1 팔레트 환원 검사 신설(ry_cg_half·ry_pi2·ry_pi4·π/6 환원,
  module 0 시 G4b skip). G4a·G1c 15분 룰 3분해.
- **[M, P8]** (blocked) 선제 부여 → (designing). HUMAN_GATE 정의 블록+생애주기+속성 순서 정정.
  standard_cycle_gates=DoD 전체 체인+acceptance 보강(second_oracle·guard·3곳 동기화).
- **[M, P7]** A6(POVM 각도)·A7(factory anchor) 가정 등재. G1c golden orientation 고정.
- **[L]** G5c witness (σ₁σ₂)⁵→**(σ₁σ₂)³=e^{2πi/5}I** 확정. ry_negpi6 명명 규약. observe 가산-only 원칙.
  승인 보고서 정본=.pgf/approvals/. V8 프레이밍 기록(cliff1 24=군 폐포, 1q 최소 2-design=12원소 부분군).
```
