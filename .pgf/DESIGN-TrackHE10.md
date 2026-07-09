# DESIGN-TrackHE10 — report10 잔여 5축 (PGF design, 2026-07-09)

> baseline: 95 modules / 466 apps / 검증경로 10 / root 6e7d2a70. P1 KS-18 완료(f1aefa1).
> 전 축 공통 정책: 관측/선검증=root 불변 sidecar·봉인=full DoD 체인. crux-probe/좌표 선검증 필수(P1 교훈).

## Gantree

```
TrackHE10_remaining
├─ P2_A5_pre_verify (designing)          # ★redirect showcase: ζ₅-vs-√5 판정
│  ├─ build_A5_group (atomic)            # 60 우치환·켤레류 5(1/15/20/12/12)
│  ├─ ambivalent_test (atomic)           # g~g⁻¹ 전수 → 모든 문자 실수?
│  ├─ char_table_exact (atomic)          # ℚ(√5) 문자표 구성·orthogonality
│  ├─ redirect_verdict (atomic)          # √5 충분 vs ζ₅ 필연 판정
│  └─ witness a5_observe.py + reproduce (atomic)
├─ P3_galois_orbit_verify (designing)    # 제11 검증경로 후보
│  ├─ crux_probe (atomic)                # ℚ-값 회로 붕괴 회피 최소반례(T 게이트)
│  ├─ galois_orbit_impl (atomic)         # ℚ(ζ_M) 진폭 → 전체 Gal 궤도+norm/trace
│  ├─ distinctness_1line (atomic)        # path-sum/Gröbner 와 전제 상이 증명
│  └─ witness galois_orbit_verify.py + reproduce (atomic)
├─ P4_MTC_ising_braid (designing)        # pentagon/hexagon + braid 유니터리
│  ├─ mtc_axioms (atomic)                # Ising/Fibonacci F·R pentagon(5항)·hexagon exact
│  ├─ ising_braid_unitary (atomic)       # B₁B₂B₁=B₂B₁B₂ Yang-Baxter·unitarity·Clifford image
│  ├─ seal_or_observe_decision (atomic)  # Tier-0 봉인 vs 관측 판정(신규 module 0 우선)
│  └─ witness mtc_observe.py + reproduce (atomic)
├─ P6_3D_Z2_fukane (designing)           # 3D 위상 ℤ₂ (chern 사다리 3D)
│  ├─ fukane_model (atomic)              # 3D FKM H(k)·TRIM 8점
│  ├─ parity_product_nu0 (atomic)        # ∏TRIM parity → ν₀ 정수공식
│  ├─ wilson_crosscheck (atomic)         # 독립 numerics 대조(관측)
│  └─ witness z2_fukane_observe.py + reproduce (atomic)
└─ P5_lattice_surgery (designing)        # Tier-2 surface code merge/split
   ├─ surface_patch (atomic)             # distance-2/3 rotated surface [[d²,1,d]] stabilizer
   ├─ merge_split_tableau (atomic)       # joint-stab 측정 merge → split, logical CNOT
   ├─ crux_vs_codeswitch (atomic)        # 동일부호 측정 merge ≠ 다른부호 coherent W
   └─ witness lattice_surgery_observe.py + reproduce (atomic)
```

## PPR (핵심 노드)

```
def P2_A5_pre_verify:
  acceptance_criteria:
    - A₅ 60원소·5 켤레류(크기 1/15/20/12/12) exact
    - ambivalent(모든 g~g⁻¹) → 문자표 전부 실수 ∈ ℚ(√5)
    - ★verdict: √5(실수) 충분 & ζ₅(복소) 불필요 (또는 반대면 정직 보고)
    - orthogonality(Σ|C|χχ*=|G|δ)·|G|=Σχ(1)² 검증
    - NOT rational group(5-cycle 분열=√5) · teeth(가짜 문자표 붕괴)
  AI_build_A5 → AI_test_ambivalent → AI_construct_char_table → AI_verdict_redirect
  # 봉인 아님(√5 승인 대기)·root 불변

def P3_galois_orbit_verify:
  acceptance_criteria:
    - crux: ℚ-값(Clifford) 회로는 Galois 자명→skip; 무리 cyclotomic(T·ζ_M) 진폭만 타깃
    - path A(회로 진폭 ∈ ℚ(ζ_M)) 의 전체 Gal 궤도 {σ_k(a)} == path B(golden 궤도)
    - norm=∏σ(a)∈ℤ · trace=Σσ(a)∈ℤ 정수 certificate
    - 1문장 전제상이(vs path-sum 진폭합·Gröbner 이데알 멤버십)
    - 커버 ≥1 (T 포함 앱)·skip 전수 사유·teeth(위상 오염→궤도 불일치)
  AI_crux_probe → AI_impl_galois → AI_verify_apps
  # 검증 인프라(제11 경로 후보)·신규 module 0·root 불변

def P4_MTC_ising_braid:
  acceptance_criteria:
    - Ising F·R: pentagon(5항 F 곱)·hexagon(R,F) exact ∈ ℚ(√2,ζ₁₆)
    - Fibonacci F·R: pentagon φ²=φ+1·hexagon exact ∈ ℚ(√5,ζ₁₀)
    - Ising braid B₁B₂B₁=B₂B₁B₂ Yang-Baxter·unitary·비보편 Clifford image
    - seal_or_observe: 신규 module 0 이면 Tier-0 봉인, 아니면 관측
    - teeth(가짜 F→pentagon 붕괴)
  AI_verify_mtc_axioms → AI_build_braid → AI_seal_decision

def P6_3D_Z2_fukane:
  acceptance_criteria:
    - 3D FKM H(k)·8 TRIM parity product ν₀∈{0,1} 정수공식(닫힌형)
    - 위상다이어그램·gap-closing 정확
    - Wilson-loop numerics == parity ν₀ (이중경로)
    - chern_higher(2D ℤ) 상보(TR-preserved) · teeth
  AI_build_fukane → AI_parity_nu0 → AI_wilson_crosscheck
  # 관측·root 불변

def P5_lattice_surgery:
  acceptance_criteria:
    - distance-2([[4,1,2]])/3([[9,1,3]]) surface code stabilizer
    - merge(joint-stab 측정)→split → logical CNOT symplectic(X̄₁→X̄₁X̄₂·Z̄₂→Z̄₁Z̄₂)
    - crux: 동일부호 측정 merge ≠ code switching coherent W(다른부호)
    - gauge-fixing(측정 의존 Pauli)=관측·결정론 merge/split=봉인 or Tier-2 tableau
    - teeth(경계 불일치 merge=ill-formed)
  AI_build_surface → AI_merge_split → AI_verify_cnot
```

## 실행 순서 (impact×feasibility)
P2 → P3 → P4 → P6 → P5 (P1 완료). 각 축: prototype 선검증 → witness → test → reproduce → commit.

## POLICY
- max_verify_cycles: 2 · 결정론 불가침·오라클 use-only·honest boundary
- 관측 sidecar(P2/P3/P6/P5-witness): root 불변. 봉인(P4 후보): full DoD(build→semantic→citation→anchor→second_oracle→reproduce).
- 각 축 독립 commit·push (verified-only).
```
