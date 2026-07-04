# DESIGN-HumanGate6 — 사람게이트 6건 단계별 개창 작업계획서

> 입력: `_workspace/integrated_horizontal_expansion3.md` §3 (TrackHE3 통합채점의 사람게이트 대기 목록).
> 원칙: §4′ 직접 닫힌형 구성(탐색 금지) · 신규 module 최소화 · **승인 게이트 = 신규 module 각도가
> *확정되는 시점*에 명세(각도·개수·닫힌형 근거·YPowGate 표현)를 보고하고 정욱님 승인 후 봉인**.
> 계획서 승인 ≠ module 승인 — 두 게이트는 분리다. 절대규율(결정론·fingerprint·frozen·honest split) 전부 상속.
> 실행: 각 G는 표준 PGF 사이클(numpy 선검증 → 마스터 노드 갱신 → spec → forge → observe → anchor →
> changed reproduce → verified commit). 매 G 완료 후 HANDOFF/이 문서 status 갱신.

---

## 실행 순서 근거 (승인 부담 오름차순 × payoff)

| 순서 | 건 | 승인 게이트 | 근거 |
|---|---|---|---|
| G1 | PEPS 2×2 RVB | **없을 가능성** (module 0 도전) | 선분석만으로 판정 가능, 2D 텐서망 새 클래스 |
| G2 | 2q 2-design 부분집합 | 없음(module 0) — 단 **실행가능성 게이트** | 수학 선검증이 관건(하한 정리 리스크) |
| G3 | π/6·π/3 각도 family | ★승인 1회 → **3축 소비**(채널 γ¼·Szegedy p¼·POVM) | 승인 효율 최대 |
| G4 | Schur n=4 | ★승인 module 2 (arccos√(2/3)·√(1/3) 계열) | schur3 직접 CG cascade 선례 연장 |
| G5 | Fibonacci anyon | ★최대 게이트: 새 대수체 ℚ(√5)+ζ₅, module 2~3 | impact 최대(비Clifford universal braid) |
| G6 | 종결 동기화 | — | 정본·외부문서·메모리 |

---

## Gantree

```
HumanGate6 // 사람게이트 6건 단계별 개창 (in-progress) @v:1.0 @dep:TrackHE3
    G1_PepsRvb // 2×2 RVB PEPS — 2D 텐서망 새 클래스, module 0 도전 (in-progress)
        G1a_Analyze // RVB 상태 닫힌형 선분석 (done)
            # ✅ 2026-07-05 numpy 선검증: |RVB⟩=|cov_H⟩+|cov_V⟩(H={01,23}·V={02,13} singlet 곱),
            #   ⟨H|V⟩=+1/2·norm²=3. 진폭 전부 실수: ±1/√12(4개)·∓1/√3(0110·1001), amp²∈{1/12,1/3}.
            #   순차 분기 확률(site0→3): {1/2, 1/6·5/6, 1/5·4/5·0·1, 0·1} — 전부 유리수.
            #   ★S_tot²|RVB⟩=0 exact(총스핀 0 singlet witness — parent-H급 물리 witness 확보).
        G1b_GateDecision // module 0 ↔ 신규각 분기 (done) @dep:G1a_Analyze
            # ✅판정: **신규 module 0** — Ry 가법성으로 전부 기봉인 조합: P=1/2→ry_pi2 ·
            #   θ(1/6)=2arccos√(1/6)=ry_k6² · 상보 π−θ=ry_pi2²·(ry_k6_dag)² · CCRy(2arccos√(1/5))의
            #   반각=ry_k5 그대로 · multiplexer 보정각 θ−π/2=ry_k6²·ry_negpi2 · 결정 분기=X/CNOT/toffoli ·
            #   부호(0110/1001 음)=조건 Z/CZ. 승인 게이트 불필요 → G1c 자율 진행 허용.
        G1c_SealObserve // peps22_rvb 봉인 + 관측 (designing) @dep:G1b_GateDecision
            # 봉인=준비 유니터리(4q Tier-0). golden=RVB 상태 열 독립 유도(dimer 정의). 관측=peps_observe:
            #   독립 텐서수축 일치·SU(2) singlet 총스핀 witness(S_tot²=0 여부는 RVB 구조상 관찰)·teeth.
    G2_TwoQubit2Design // 2q 2-design 최소 부분집합 (designing) @dep:G1_PepsRvb
        G2a_MathVerify // 실행가능성 수학 선검증 (designing)
            # process: ★탐색 아닌 닫힌형 후보군만: (i) 하한 정리 |X|≥d⁴−2d²+2=226(d=4, 균일) 확인
            #   (ii) 후보 부분군(Clifford 부분군, 예: C₁⊗C₁·대칭군 확장·sp(4,2) 부분군) frame potential
            #   F₂ 수치 계산 → 2와 비교 (iii) 외부 주장 "21원소"는 하한 위반 여부 판정
            # criteria: 균일 exact 2-design 부분집합 크기 ≤ 64 발견 → G2b / 아니면 blocked 정직 보고
            #   (앱 226개+ 봉인은 비현실 — cliff1 24개와 달리 등록부 오염 수준)
        G2b_SealObserve // cliff2_* 부분집합 봉인 + F₂ witness (blocked) @dep:G2a_MathVerify
            # blocked 사유: G2a 판정 대기. 통과 시 V8 패턴 그대로(word 봉인+twodesign_observe 확장).
    G3_AngleFamilyPi6 // π/6·π/3 family 승인 1회 → 3축 소비 (designing) @dep:G2_TwoQubit2Design
        G3a_DeriveAngles // 3축 필요 각도 정확 도출 (designing)
            # process(numpy): ①채널 γ=¼: θ=2arcsin√γ=π/3 → CRY(π/3)=반각 Ry(π/6)± 분해(V6 CRY 패턴)
            #   ②Szegedy p=¼/¾: |p_x⟩ prep cos(θ/2)=½ → θ=2π/3=Ry(π/3)·Ry(π/3)? → 반각 집합 확정
            #   ③Naimark POVM(π/3 겹침 unambiguous discrimination): isometry 열 도출 → 각도 확정
            # criteria: 최소 module 집합(목표 ry_pi6/ry_pi6_dag 2개, 필요 시 ry_pi3± 추가) + YPowGate
            #   표현(t=1/6=비-dyadic exact 유리 지수) + second_oracle 제1원리 구성 초안
        G3b_ApprovalGate // ★정욱님 승인: 신규 module 집합 (blocked) #HUMANGATE @dep:G3a_DeriveAngles
            # 보고 양식: 각도·개수·닫힌형 근거·소비처 3축·frozen/fingerprint 무영향 확인
        G3c_SealChannelG14 // stinespring_*_g14 (γ=¼ family) 봉인+channel_observe 확장 (blocked) @dep:G3b_ApprovalGate
        G3d_SealSzegedyP14 // szegedy_2state_p14 봉인+szegedy_observe 확장 (blocked) @dep:G3b_ApprovalGate
        G3e_SealNaimark // naimark_ud3 (3-outcome POVM isometry) 봉인+povm witness (blocked) @dep:G3b_ApprovalGate
            # C3-iso 경로(isometry 봉인 선례: 코드 인코더). SIC/trine 비-골든=봉인불가 정직경계 명시.
    G4_Schur4 // n=4 Schur-Weyl irrep splitter (designing) @dep:G3_AngleFamilyPi6
        G4a_DesignCascade // 직접 CG cascade 설계 (designing)
            # process: schur3(U=V2·G2·G1) 패턴 연장 — j 사다리 2⊗½ 단계별: j=2(5)⊕j=1(3×3)⊕j=0(2×1)
            #   16차원. CG 계수 √(1/2)·√(3/4)·√(2/3)·√(1/3) → 2-level Givens 라우팅(CCRy=반각+CCX).
            #   numpy 전체 16×16 == 독립 CG golden(회로 무관) 선검증 필수. label map 명시.
            # criteria: 신규각 = arccos√(2/3)·arccos√(1/3) 반각 2개(ry_sch4_a/b±)로 닫힘 확인
        G4b_ApprovalGate // ★정욱님 승인: module 2쌍 (blocked) #HUMANGATE @dep:G4a_DesignCascade
        G4c_SealObserve // schur4 봉인 + schur_observe 확장 (blocked) @dep:G4b_ApprovalGate
            # witness: U†J²U·U†JzU 동시대각(고유값 {6,2,0}·multiplicity {5,9,2})+S₄ duality sector+teeth
    G5_Fibonacci // Fibonacci anyon braid — 새 대수체 (designing) @dep:G4_Schur4
        G5a_DesignBraid // R/F 닫힌형·B₃ 표현 설계 (designing)
            # process: 3-anyon fusion space=2차원(1q!). R=diag(e^{−4πi/5}, e^{3πi/5}),
            #   F=[[φ⁻¹,φ^{−1/2}],[φ^{−1/2},−φ⁻¹}]] (φ=황금비, ℚ(√5)). σ₁=R·σ₂=F·R·F 2×2 exact.
            #   module 후보 최소화: rz_2pi5±(ZPowGate t=2/5 계열)·ry_fib(arccos(φ⁻¹) 계열) — numpy 로
            #   정확 분해(σ₂=F R F 를 Rz·Ry·Rz 오일러로) 도출·개수 확정. second_oracle 제1원리 구성 포함.
            # criteria: 승인 요청 module ≤3 · 전 계수 ℚ(√5,ζ₅) 닫힌형 · Yang-Baxter σ₁σ₂σ₁==σ₂σ₁σ₂ 수치확인
        G5b_ApprovalGate // ★정욱님 승인: 새 대수체 ℚ(√5)+ζ₅ 도입 + module 집합 (blocked) #HUMANGATE @dep:G5a_DesignBraid
            # 판단 재료: 기존 field(dyadic·√2·√3·arccos√유리수)에 √5·5차 단위근 추가가 등록부 대수 지평 확장
        G5c_SealObserve // fib_braid_s1/s2 봉인 + braid witness (blocked) @dep:G5b_ApprovalGate
            # 관측: Yang-Baxter exact·비-Clifford witness(stabilizer fidelity<1, magic_a 패턴)·
            #   (σ₁σ₂)⁵? braid 군 관계·universality 주장은 근사컴파일=범위 밖 정직경계. teeth.
    G6_Closure // 종결 — 정본·외부문서·메모리 동기화 (designing) @dep:G5_Fibonacci
        # HANDOFF·마스터·PROJECT_STATUS·README 수치·메모리·이 문서 전 노드 terminal 확인.
```

## 공통 PPR (매 G 게이트)

```python
def run_gate_G(node) -> Literal["done", "blocked"]:
    """각 G 공통 실행자 — 중심 루프(decompose→gate→execute) 그대로"""
    design = numpy_preverify(node)                    # 닫힌형·각도 집합·golden 독립 유도 (실제 코드)
    if design.new_modules:
        report = AI_compose_approval_request(design)  # 각도·개수·근거·소비처·불변 확인
        approval = HUMAN_GATE(report)                 # ★정욱님 — 대기 중 다음 독립 G 선행 금지(순서 유지)
        if not approval:
            return "blocked"                          # 사유 기록, 후속 노드 blocked 유지
        seal_modules(design.new_modules)              # seal_module.py + second_oracle 제1원리 추가
    seal_apps(design.specs)                           # forge_apps --changed-only
    observe(design.witness)                           # 관측 스크립트 + reproduce_all 등록
    return standard_cycle_gates()                     # registry build→anchor→changed reproduce→commit
    # acceptance_criteria:
    #   - 신규 봉인 전부 Tier-0 exact (dense) · fingerprint/frozen byte-identical
    #   - observe all_ok=True + teeth 검출 · reproduce_all --changed-only REPRODUCED
    #   - verified-commit only · HANDOFF/이 문서 status 갱신
```

## 리스크 / 가정 (검증시점 포착용)

- **A1(G1)**: RVB 각도가 팔레트로 닫힌다는 보장 없음 — G1a가 판정. 신규각이면 G1도 승인 게이트化.
- **A2(G2)**: 균일 exact 2-design 하한(≈226, d=4)이 맞으면 "작은 부분집합" 자체가 불가능할 수 있음
  → blocked 정직 보고가 정상 종결일 수 있다(외부 주장 반증도 성과).
- **A3(G3)**: Ry(π/6) 등이 YPowGate 유리 지수로 oracle에서 exact 처리되는지 — ry_k*/ry_cg 선례상 가능,
  G3a에서 실제 seal_module 드라이런으로 확인.
- **A4(G4)**: n=4 CG cascade 라우팅 복잡도 — 탐색 금지 원칙 유지, 실패 시 재설계 1회 후 blocked.
- **A5(G5)**: 새 대수체가 second_oracle 유리수 대조 경로와 충돌 가능 — 제1원리 구성(√5 기호)을
  승인 요청서에 포함해 선판정.
- **공통**: 각 G 사이에 frontier 무인 라운드·외부 회신 등 인터럽트 가능 — 이 문서 status가 재개점.
```
