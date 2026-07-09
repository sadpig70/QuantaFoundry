# DESIGN — TrackHE13 (report13 소비: 8런타임 6축 통합)

> **Version** 1.0 · **Status** done (2026-07-10 폐합: 6축 전수 검증·REPRODUCED·v14 배치) · **작성** 2026-07-10 (Fable 5)
> **입력**: `_workspace/ex-report13/agent01~08_report13.md` (8런타임, REQUEST-v13 응답)
> **Base**: root `d177ce9a` · 95 modules / 475 apps · 검증경로 10 · TrackIU 폐합 직후
> **선례**: TrackHE12 (PGF full-cycle · 병렬 subagent 구현 · 전 축 관측 · root 불변)

---

## 0. 수렴 집계 (8런타임)

| 축 | 제안 agents | 수렴 | 판정 |
|---|---|---|---|
| **class DIII** (TRS Kramers ℤ₂) | 01·02·03·04·05·06·07·08 | **8/8 ★전원** | P1 채택 |
| **Drinfeld double D(S₃)** modular data | 01·03·05·06·07·08 | **6/8** | P2 채택 |
| **Conway-31 KS** (d=3 state-indep) | 01·02·04·05·06·08 | **6/8** | P3 채택 |
| SU(2)₄ 완전 MTC | 01·02·04 | 3/8 | P6 채택 (★외부 수치 오류 검출: D²=8 아닌 **12**) |
| Kauffman bracket/Jones | 03·04·08 | 3/8 | P4 채택 (fib_jones 와 차별 스코프 한정) |
| Ising pentagon/hexagon F/R | 05·08 | 2/8 | P5 채택 (§4′l 완전-일관성 패턴 정합) |
| HOMFLY/BMW | 03·06 | 2/8 | 백로그 (P4 선행 후) |
| H²(G,U(1)) SPT cocycle | 07 | 1/8 | 백로그 (질적 흥미 — 2.A₅ FS 인과층) |
| Negativity/Mana·Spekkens POM·Floquet SPT·TL₅ JW | 각 1/8 | 1/8 | 백로그 |
| 제11 경로 | 02(symplectic)·05(ANF+Gröbner 결합) | 2/8 | ★불채택 — 02 는 Sp(2n,𝔽₂)=stabilizer 형식론 재인코딩(자가강등 확실), 05 는 자인(自認) 강등 위험. 6/8 이 정직 보류 — 공개과제 유지 |

**★선검증 정정 (§4′ 패턴 계속)**: agent02·06 의 SU(2)₄ "D²=8, d=(1,√2,√3,√2,1)" 은 오류.
자체 재계산: d_j = sin((2j+1)π/6)/sin(π/6) → **d=(1,√3,2,√3,1), D²=12**. P6 은 정정값으로 진행.

## 1. 불변 조건

```python
# INV-HE13-1: 전 축 관측(observe) sidecar — 신규 module 0 · 봉인 0 · root d177ce9a 불변
# INV-HE13-2: 외부 좌표/수치/공식 전면 불신 — 전부 자체생성·자체유도 (Peres-33·KS-18 선례)
# INV-HE13-3: colorable/consistency 판정은 결과 그대로 — closed-negative 도 정직한 산출 (Yu-Oh 선례)
# INV-HE13-4: §2 Fourier 실봉인 경계 준수 — modular data 는 조합적 exact 표(게이트 분해 불요) 로 우회
# INV-HE13-5: DoD = 각 witness --quick all_ok=True · reproduce --changed-only REPRODUCED · second_oracle 83/83
```

## 2. Gantree

```
TrackHE13 // report13 6축 소비 (done — 2026-07-10 폐합) @v:1.0
    [parallel]
    P1_ClassDIII // class DIII 1D ℤ₂ (TRS T²=−1 Kramers + PHS) — AZ 사다리 3계단 (done)
        # scripts/class_diii_observe.py — BdG 4-band(TRS 두 Kitaev 사슬+Rashba형 결합)
        # path A 닫힌형(TRIM Pfaffian/sewing 부호곱) == path B 격자 numeric · 3상 · Kramers 축퇴 exact
        # teeth: TRS 깨기 → class D 강등 검출 · α=0 분해(두 class-D 복사본) 명시
    P2_DrinfeldDouble // D(S₃) 양자이중 완전 modular data — 유한군 MTC 축 개창 (done)
        # scripts/dsr3_double_observe.py — 8 anyon=(켤레류,centralizer irrep) 자체구성
        # d=(1,1,2,3,3,2,2,2)·D²=36=|G|²·S(8×8 exact ℚ(ζ₃))·T(θ=χ(g)/dim)·Verlinde 비음정수·S²=C·(ST)³
        # §2 우회: modular data=조합 표(DFT 회로 아님) · SU(2)₃(Lie) vs D(S₃)(유한군) 양대 원천
    P3_Conway31 // Conway-31 d=3 state-independent KS — I_h 궤도 자체생성 (done)
        # scripts/conway31_ks_observe.py — icosahedron 6 정점축+10 면축+15 모서리축=31 rays ℚ(√5)
        # 직교 triad 자체식별 → 전수 백트래킹 (a)not-both-1+(b)triad≥1 — UNSAT 이면 uncolorable,
        # colorable 이면 정직 closed-negative 그대로 보고 · teeth: 부분집합 colorable(비-vacuous)
    P4_KauffmanBracket // Kauffman bracket state-sum → Jones — 특수화 허브 (done)
        # scripts/kauffman_bracket_observe.py — 2^n smoothing 전수 state-sum, ⟨L⟩∈ℤ[A,A⁻¹] exact(sympy)
        # trefoil·fig8·Hopf · V(t)=(−A)^{−3w}⟨L⟩|_{t=A⁻⁴} · ★차별(기존 fib_jones=braid trace/skein 재귀):
        # state-sum 알고리즘 + generic-A Laurent + 특수화 다리(A=i→δ=2 TL 정합·fig8 amphichiral 대칭)
    P5_IsingFR // Ising MTC pentagon/hexagon 전역 일관성 — 개별 braid→공리 승격 (done)
        # scripts/ising_fr_observe.py — F^{σσσ}_σ=(1/√2)[[1,1],[1,−1]]·R∈ℚ(ζ₁₆) 자체구성
        # pentagon(Biedenharn-Elliott) 전 채널 + hexagon(F-R 호환) 잔차=0 exact · θ_σ=ζ₁₆·c=½
        # 기존 mtc_braid(개별 braid)·ising_fusion(융합환)과 검증객체 상이(일관성 공리)
    P6_SU24MTC // SU(2)₄ 완전 MTC modular data — k-family 확장 (done)
        # scripts/su2_4_mtc_observe.py — d=(1,√3,2,√3,1)·D²=12(★외부 D²=8 오류 정정)·
        # S_{ab}=√(2/6)sin((2a+1)(2b+1)π/6)·T=e^{2πi h_j}, h_j=j(j+1)/6·c=2 · Verlinde·S²=C·(ST)³
        # su2_3_mtc_observe 템플릿 재사용 · 필드 ℚ(ζ₂₄)
    [/parallel]
    Verify // 직접 스크립트 정독 + 실행 검증 (done) @dep:P1_ClassDIII,P2_DrinfeldDouble,P3_Conway31,P4_KauffmanBracket,P5_IsingFR,P6_SU24MTC
    ReproduceRegister // reproduce_all 3abr~3abw 등록 + --changed-only (done) @dep:Verify
    RequestV14 // REQUEST-v14 배치 (§3q EXCLUDE·백로그 반영) (done) @dep:ReproduceRegister
    DocSync // HANDOFF·메모리 갱신 + 커밋 (done) @dep:RequestV14
```

## 3. 정직 경계 (설계 고정)

1. 전 축 **관측**(sidecar witness) — 봉인 아님. modular data/불변량/다항식 = exact 산술이나 회로 봉인과 구분.
2. P3 Conway-31: uncolorable 여부는 **자체 백트래킹이 판정** — 문헌 주장 불신, colorable 산출 시 그대로 보고.
3. P4: Jones 값 자체는 fib_jones(TrackHE4) 기관측 — 신규성은 **state-sum 알고리즘·generic-A Laurent·특수화 다리**로 한정 표기.
4. P2·P6: modular data 표 봉인이지 **anyon 게이트 유니터리 아님**(§2 경계) — "topological gate 봉인" 주장 금지.
5. 제11 경로: 후보 2건(symplectic·ANF+Gröbner 결합) 불채택 사유 기록 — 공개과제 유지.
