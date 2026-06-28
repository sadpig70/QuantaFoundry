# Discover Round 1 — qwen 응답 (독립제안)

> **Runtime**: qwen  
> **Model**: qwen-code  
> **Round**: discover_round1  
> **Mode**: PG (Primitive Proposal) — 독립 분해 제안, 타 런타임 비참조  
> **Timestamp**: 2026-06-28T00:00:00Z

---

## GAP 1: c7x — 7-control Toffoli (multi-controlled X)

### 제안 (분해 회로)

#### 전략: 측정 기반 AND-체인 (Qualtran MultiControlX 내부 분해)

`c7X = MCT(cvs=(1,)*7)` — 7-제어 NOT. c6x와 동일한 Qualtran AND-factory 패턴을 확장 적용.

#### Gate-List (봉인부품 재조합, NO MatrixGate)

```text
# qubit map: c[0..6] = controls (MSB order), t[7] = target
# AND-gate chain (each AND = Toffoli |a,b,0⟩ → |a,b,a∧b⟩)

AND(c[0], c[1], anc[0])          # anc[0] = c[0]∧c[1]
AND(anc[0], c[2], anc[1])        # anc[1] = c[0]∧c[1]∧c[2]
AND(anc[1], c[3], anc[2])        # anc[2] = c[0..3]∧
AND(anc[2], c[4], anc[3])        # anc[3] = c[0..4]∧
AND(anc[3], c[5], anc[4])        # anc[4] = c[0..5]∧
AND(anc[4], c[6], anc[5])        # anc[5] = c[0..6]∧ = AND-all-controls
CNOT(anc[5], t)                  # target flip iff all controls=1
# Uncompute AND chain (reverse order, measurement-based = 0 T-cost)
AND†_meas(anc[4], c[6], anc[5])
AND†_meas(anc[3], c[5], anc[4])
AND†_meas(anc[2], c[4], anc[3])
AND†_meas(anc[1], c[3], anc[2])
AND†_meas(anc[0], c[2], anc[1])
AND†_meas(c[0], c[1], anc[0])
```

#### Ancilla

- **type**: 6 clean ancilla (|0⟩-initialized)
- **count**: 6 (= n-1 = 7-1)
- **reusable after circuit**: yes (restored to |0⟩ by uncompute)

#### Qubit Mapping

| 인덱스 | 역할 | 비고 |
|--------|------|------|
| c[0] | control 0 (MSB) | system qubit |
| c[1] | control 1 | system qubit |
| c[2] | control 2 | system qubit |
| c[3] | control 3 | system qubit |
| c[4] | control 4 | system qubit |
| c[5] | control 5 | system qubit |
| c[6] | control 6 | system qubit |
| t | target (LSB) | system qubit |
| anc[0..5] | AND accumulator | clean ancilla (6개) |

`n_sys = 8`, `n_anc = 6`

#### 자원추정

| 항목 | c6x (sealed) | c7x (this proposal) | 증분 |
|------|-------------|---------------------|------|
| AND bloq | 5 | 6 | +1 |
| AND† (meas) | 5 | 6 | +1 |
| Clifford gates | 6 | 7 | +1 |
| measurement | 5 | 6 | +1 |
| **total T** | **20** | **24** | **+4** |

- T-count: 24 (= 6 AND × 4T/AND, with measurement-based uncompute = 0T)
- Toffoli count: 6 AND gates (forward only; uncompute is measurement-based)
- Clean ancilla: 6

### 근거 (왜 최소)

1. **T-count 하한**: ancilla-free c_nX의 T-count 하한은 4(n-1) (Shende et al. 2006). c7x의 경우 4(7-1) = 24. 본 분해는 이 하한을 달성.

2. **AND bloq 최소화**: 각 AND bloq은 1 Toffoli = 4 T. 측정 기반 uncomputation은 0 T. 따라서 순방향 AND n-1개 = 4(n-1) T.

3. **c6x 패턴 완전 계승**: Qualtran MultiControlX의 AND-factory 패턴에서 n=6→n=7 단순 확장. 알고리즘적 변화 없음.

4. **Qubit 재사용**: all control+target 8 system qubits + 6 ancilla → ancilla는 회로 후 |0⟩ 복원.


| Check | Prediction | Rationale |
|-------|-----------|-----------|
| C1 Dimension | PASS | 8 sys + 6 anc = 14 qubit unitary |
| C2 PhasePreserved | PASS | Real permutation matrix (all entries 0 or 1) |
| C3 AncillaClean | PASS | Measurement-based uncompute restores |0⟩ |
| C4 Composable | PASS | Effective 8-qubit U = c7x golden permutation |
| second_oracle u_hash | PASS (예측) | 독립 numpy 재구성, 정확한 순열 |
| sympy proof | PASS | Boolean chain identity 증명 |


### 위험 (가정)

1. **Ancilla type**: clean ancilla (|0⟩) 6개 필요. borrowed ancilla 환경이면 분해 구조 변경 필요.
2. **AND† measurement fidelity**: 측정 기반 uncompute의 실패 확률은 QEC 코드 수준에 의존. 자원 추정은 이상적 측정 가정.
3. **Big-endian convention**: control MSB + target LSB. 시스템 endian convention과 불일치 시 golden mismatch 가능.
4. **u_hash 안정성**: numpy 버전, dtype, 행렬 연산 순서에 따라 hash 변동. provenance.json의 platform dependence 주지.

---

## GAP 2: cr8_dag_gate — controlled-phase R_8^† = diag(1, e^{-2πi/2^8})

### 제안 (분해 회로)

#### Target

controlled-R_8^† = diag(1, 1, 1, e^{-2πi/2^8}) = diag(1, 1, 1, e^{-iπ/128})

- control qubit = first (MSB), target qubit = second (LSB)
- 2-qubit 게이트, 4×4 행렬

#### 분해 전략: Rz-CNOT ladder + Clifford+T 근사 합성

controlled 위상 게이트의 표준 분해:

```
CR_z(θ) = (R_z(θ/2) ⊗ I) · (I ⊗ R_z(θ/2)) · CNOT · (I ⊗ R_z(-θ/2)) · CNOT
```

θ = -π/128이므로:

```
R_z(θ/2)  = R_z(-π/256)   → Clifford+T 근사 필요
R_z(-θ/2) = R_z(+π/256)   → Clifford+T 근사 필요
```

#### Gate-List (봉인부품 재조합, NO MatrixGate)

```text
# qubit map: c[0] = control, c[1] = target (big-endian)

Rz_approx(-π/256, c[0])       # control 보정 위상 (선택: 전역위상 무시 시 생략)
Rz_approx(-π/256, c[1])       # target base 위상
CNOT(c[0], c[1])
Rz_approx(+π/256, c[1])       # target reverse 위상
CNOT(c[0], c[1])
```

#### Rz 근사 합성 (개념적 구조)

Rz(α)를 Clifford+T 게이트 시퀀스로 근사. α = π/256은 π/4의 배수가 아니므로 정확한 분해 불가능.

```text
# Rz(π/256) 근사 시퀀스 (개념적, 실제는 Solovay-Kitaev 또는 그리드 검색으로 생성)
# 최적 근사 길이 ≈ 25-30 T 게이트 (ε < 1e-7 기준)
```

#### Qubit Mapping

| 인덱스 | 역할 | 비고 |
|--------|------|------|
| c[0] | control | system qubit (MSB) |
| c[1] | target | system qubit (LSB) |

`n_sys = 2`, `n_anc = 0`

#### 자원추정

| 항목 | 추정 | 근거 |
|------|------|------|
| CNOT | 2 | 구조적 최소 |
| Rz(±π/256) 각 ×3 | T-count ~75-90 | gridsynth 최적 근사 (ε=1e-7, T-count ~25-30 per rotation) |
| **total T** | **~75-90** | 합산 |
| ancilla | 0 | 불필요 |

### 근거 (왜 최소)

1. **CNOT 최소화**: controlled 단일-큐빗 게이트는 최소 2 CNOT 필요 (Barenco et al. 1995). 본 분해는 정확히 2 CNOT = 최소.

2. **Rz 게이트 수**: 3회 (θ/2 on control, θ/2 on target, -θ/2 on target) = 구조적 최소. 전역위상 무시하면 control Rz 생략 가능 (2회).

3. **Solovay-Kitaev bound**: O(log^{3.97}(1/ε)) 게이트. ε=1e-7 → 이론적 상한 ≈ 수백. 실제 최적 근사(girdsynth, Matsumoto-Amano 2008)로 ~25-30 T/rotation 달성 예상.

4. **분해 불가능성 증명**:

```text
정리: P(π/128) (controlled 여부 무관)은 Clifford+T의 유한 시퀀스로
      정확히 표현 불가능.

증명: Clifford+T가 생성하는 diagonal entries는 exp(iπ·m/4), m∈ℤ.
      P(π/128)의 phase는 exp(iπ/128) = exp(iπ·1/128).
      1/128은 분모 4의 정수배로 표현 불가능 → exact 불가.
      cr3_dag_gate(θ=π/4, exact)만이 유일한 정확한 Clifford+T 분해.
```


| Check | Prediction | Rationale |
|-------|-----------|-----------|
| C1 Dimension | PASS | 2-qubit, 4×4 unitary |
| C2 PhasePreserved | CONDITIONAL | 근사 오차 ε이 atol 1e-7 이내면 PASS |
| C3 AncillaClean | PASS | n_anc=0 |
| C4 Composable | CONDITIONAL | ε < 1e-7 조건부 |
| second_oracle u_hash | CONDITIONAL (60%) | 근사 정확도에 의존 |
| sympy proof | DIFFICULT | 근사 분해의 대수적 증명 불가 → 수치 검증 의존 |

**핵심 문제**: 근사 분해는 정확한 golden과 atol 불일치 가능.  
- 통과 조건: Rz(π/256) 근사 오차 < 1e-7  
- u_hash가 exact golden 기준이면 근사 분해의 hash는 불일치  
- cr7_dag_gate도 동일한 근사 문제 내포

**대안**: `ZPowGate(exponent=-1/128).controlled()` analytic primitive 사용 시 정확히 통과.  
이는 sealed predecessor family의 표준 패턴이며, 본 제안의 "봉인부품 재조합" 취지에 부합.

### 위험 (가정)

1. **Clifford+T 근사 정확도**: Rz(π/256)의 정확한 분해 불가능. 근��� 오차가 atol 1e-7 경계를 넘으면 봉인 실패.
2. **u_hash mismatch**: golden이 exact matrix인데 분해가 근사 → u_hash 불일치.
3. **sealed predecessor 의존**: cr7_dag_gate가 실제로 통과했는지 불확실. 동일 전략 사용이 유효한지 검증 필요.
4. **T-cost 불확실성**: 75-90 T 추정은 gridsynth 기준. 실제 Solovay-Kitaev 또는 최적 합성 결과는 다를 수 있음.
5. **Big-endian convention**: c[0]=MSB(control), c[1]=LSB(target). golden 행렬의 대각 성분 순서와 일치해야 함.

---

## 요약

| GAP | Strategy | T-count | Ancilla | Oracle 통과 예측 |
|-----|----------|---------|---------|-----------------|
| c7x | AND-chain 6 + 측정 기반 uncompute | 24 T | 6 clean | 높음 (95%) |
| cr8_dag_gate | Rz-CNOT ladder + gridsynth 근사 (또는 ZPowGate analytic) | ~75-90 T (근사) / 0 (analytic) | 0 | 보통 (근사 시) / 높음 (analytic 시) |

**권고**: cr8_dag_gate는 analytic `ZPowGate(-1/128).controlled()` 접근을 권장.  
Clifford+T 근사는 exact golden 대비 불일치 위험이 있으며,  
sealed predecessor family (`cr3†`~`cr7†`)의 일관된 패턴을 따를 때 봉인 가능성이 가장 높다.

