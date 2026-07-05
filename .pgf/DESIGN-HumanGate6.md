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
    G2_TwoQubit2Design // 2q 2-design — ★closed-negative 반증 + 대체 payoff (designing)
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
        G2b_StateDesignOption // ★대체 payoff: MUB-20 state 2-design (Clifford, module 0) (designing) @dep:G2a_MathVerify
            # P7 부수 발견의 정직한 회수: d=4 MUB 5기저×4상태=20 상태준비 앱(전부 Clifford word) 봉인 +
            #   state 2-design witness(frame potential 2/(d(d+1))=1/10 exact) 관측. unitary design 아님을
            #   명시(용어 정직). numpy 선검증 → 규모(20앱) 대비 가치 판단 보고 후 진행/스킵 결정.
            #   ※진행 결정은 봉인 규모 게이트(module 아님): 20앱 추가가 등록부 오염인지 payoff 인지 정욱님 1줄 확인.
    G3_AngleFamilyPi6 // π/6·π/3 family 승인 1회 → 2+1축 소비 (designing)
        G3a_DeriveAngles // 3축 필요 각도 정확 도출 (designing)
            # process(numpy): ①채널 γ=¼: θ=2arcsin√γ=π/3 → CRY(π/3)=반각 Ry(π/6)± 분해(V6 CRY 패턴) ✓리뷰 확인
            #   ②Szegedy p=¼/¾: prep Ry(2π/3)=ry_pi6⁴ — ry_pi6 만으로 닫힘 ✓P5 확인
            #   ③Naimark POVM: ⚠A6 — canonical √E isometry 성분²={2/3,1/24,1/8,3/8}(P7)로 π/6 family 밖.
            #     Kraus/기저 선택 자유도로 π/6·π/3 격자 재도출 시도 → 실패 시 POVM 축을 G4 family(√(2/3)=
            #     ry_cg_half 계열)로 이동 또는 별도 각도 승인으로 분리(G3b 보고서에 판정 결과 명시).
            # criteria: 확정 module 집합(목표 ry_pi6/ry_negpi6 2개 — 명명 규약: π-분수 family 는 neg-접두,
            #   _dag 는 ry_k*/ak*/cg 전용, P8) + YPowGate 표현(t=1/6) + seal_module 드라이런 +
            #   second_oracle 제1원리 구성 초안 + POVM 축 판정
        G3b_ApprovalGate // ★정욱님 승인: 신규 module 집합 (designing) @dep:G3a_DeriveAngles #HUMANGATE
            # 보고서 정본 위치: .pgf/approvals/G3-ry_pi6.md (각도·개수·닫힌형 근거·소비처·POVM 판정·불변 확인)
        G3c_SealChannelG14 // stinespring_*_g14 (γ=¼ family) 봉인+channel_observe 확장 (designing) @dep:G3b_ApprovalGate
            # 기존 자산 의존: scripts/channel_observe.py(확장은 가산-only 비파괴). 무접미사 기존 4앱=γ½ 레거시 규약 주석.
        G3d_SealSzegedyP14 // szegedy_2state_p14 봉인+szegedy_observe 확장 (designing) @dep:G3b_ApprovalGate
            # 기존 자산 의존: specs/apps/szegedy_2state_p12.app.pg·scripts/szegedy_observe.py(가산-only).
        G3e_SealNaimark // naimark_ud3 — 정방 유니터리 완성 봉인 + POVM witness 관측 (designing) @dep:G3b_ApprovalGate
            # ★재설계(P5 High): app 경로 isometry 미지원·C1-C4(iso) production 선례 0건 →
            #   **unitary completion**: Naimark isometry 를 정방 유니터리로 완성해 Tier-0 봉인,
            #   POVM 작용(ancilla-|0⟩ 열 제한)=witness 관측(aklt4 "정의 열" honest split, INV-Q3).
            #   SIC/trine 비-골든=봉인불가 정직경계 명시. (module-level alloc-bloq isometry 봉인은
            #   별도 결정사항 — 이번 트랙 범위 밖.)
    G4_Schur4 // n=4 Schur-Weyl irrep splitter — ★module 0 가능성 높음 (designing) @dep:G3b_ApprovalGate
        # ★hard dep 근거(P5): CG 계수 √(3/4)의 Givens 반각=arccos√(3/4)=π/6 → G3 승인 module ry_pi6 재사용.
        #   G3b 부결 시 G4 는 π/6 을 자체 승인 요청으로 승계(축 이동).
        G4a1_PaletteReduction // 기존 팔레트 가법성 환원 검사 (designing)
            # ✅리뷰 중 선판정(P5 수치): arccos√(2/3)=arccos(1/3)/2=**기봉인 ry_cg_half 와 float-identical** ·
            #   arccos√(1/3)=π/2−arccos√(2/3)=ry_pi2·ry_cg_half_dag 합성 ✓ · √(1/2)→π/4=ry_pi4 ✓ ·
            #   √(3/4)→π/6(G3) · 3-control=c3x 기봉인 ✓. 잔여: 전체 CG cascade 필요 각도 전수 나열 후
            #   환원 완결 확인 → **신규 module 0 이면 G4b 스킵**(조건부).
        G4a2_CGGoldenDesign // 독립 CG golden(16×16)+j-사다리 설계 (designing) @dep:G4a1_PaletteReduction
            # j=2(5)⊕j=1(3×3)⊕j=0(2×1)=16 ✓(P5). golden=CG 계수 직접(회로 독립, schur3 패턴). label map 명시.
        G4a3_CascadeRouting // 2-level Givens 라우팅 plan + numpy 전수 일치 (designing) @dep:G4a2_CGGoldenDesign
            # criteria: plan 합성 == CG golden exact(16×16 전수) · MatrixGate 0 · 신규각 최종 판정
        G4b_ApprovalGate // ★조건부 승인: G4a1 에서 신규각 잔존 시만 (designing) @dep:G4a3_CascadeRouting #HUMANGATE
            # module 0 확정 시 이 노드는 (done: skipped-no-new-module) 로 종결. 보고서: .pgf/approvals/G4-schur4.md
        G4c_SealObserve // schur4 봉인 + schur4_observe (designing) @dep:G4b_ApprovalGate
            # witness: U†J²U·U†JzU 동시대각(고유값 {6,2,0}·mult {5,9,2} ✓P5)+S₄ duality sector+teeth.
            #   신규 스크립트 schur4_observe.py (기존 schur_observe.py 는 불변 — 가산-only 원칙, P8).
    G5_Fibonacci // Fibonacci anyon braid — 새 대수체 (designing)
        G5a_DesignBraid // R/F 닫힌형·B₃ 표현 설계 (designing)
            # process: 3-anyon fusion space=2차원(1q). R=diag(e^{−4πi/5}, e^{3πi/5}) ·
            #   F=[[φ⁻¹,φ^{−1/2}],[φ^{−1/2},−φ⁻¹]] (F²=I ✓) · σ₁=R·σ₂=FRF.
            #   ★field 정정(P7 Critical): N(φ)=−1 → √φ∉ℚ(√5,ζ₅) — 실제 계수체=**ℚ(ζ₅,√φ), 차수 8 확장**.
            #   ★Euler 분해 확보(P7 수치 exact): σ₂=e^{−iπ/10}·Rz(−7π/5)·Ry(2arccos φ⁻¹)·Rz(−2π/5)
            #   → module 후보: rz_pi5 계열(ZPowGate t=k/5)+ry_fib(YPowGate, cos(반각)=φ⁻¹∈ℚ(√5))
            #   +전역위상 ζ₂₀ 처리(전역위상 흡수 규약으로 소화 가능 여부 확인). F=Ry(2arccos φ⁻¹)·Z ✓P5.
            # criteria: 승인 요청 module ≤3 · **field 공시=ℚ(ζ₅,√φ) 차수 8**(축소 보고 금지) ·
            #   Yang-Baxter σ₁σ₂σ₁==σ₂σ₁σ₂ ✓(수치 통과) · second_oracle 제1원리(√5·√φ 기호) 초안
        G5b_ApprovalGate // ★정욱님 승인: 새 대수체 ℚ(ζ₅,√φ) 도입 + module 집합 (designing) @dep:G5a_DesignBraid #HUMANGATE
            # 판단 재료: 기존 field(dyadic·√2·√3·arccos√유리수·√41)에 5차 단위근+√φ(차수 8) 추가 —
            #   등록부 대수 지평 최대 확장. 보고서: .pgf/approvals/G5-fibonacci.md
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
- **A3(G3)**: Ry(π/6)=YPowGate(t=1/6) oracle exact 처리 — seal_module 드라이런으로 G3a 에서 확인.
- **A4(G4)**: n=4 CG cascade 라우팅 복잡도 — 탐색 금지 유지, G4a3 실패 시 재설계 1회 후 blocked.
- **A5(G5)**: 새 대수체 ℚ(ζ₅,√φ)와 second_oracle float 대조 경로 충돌 — √41(ry_ak41) 선례상 float-경유
  가능성 높으나 제1원리 구성(기호)을 승인 요청서에 포함해 선판정. 전역위상 ζ₂₀ 흡수 여부 포함.
- **A6(G3, 신규 — P7)**: "승인 1회→3축"은 POVM 축에서 미검증(canonical isometry 성분²={2/3,1/24,1/8,3/8}
  — π/6 family 밖). G3a ③ Kraus 자유도 재도출로 판정, 실패 시 POVM=G4 family 이동 또는 별도 승인.
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
