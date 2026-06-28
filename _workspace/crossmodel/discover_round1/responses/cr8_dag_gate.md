# Discover Round 1 Response — cr8_dag_gate

## 모델 정보
- **Runtime ID**: qwen-code
- **Timestamp**: 2026-06-28T00:00:00Z

## 1. 제안 (분해 회로)

### Target

controlled-R₈† = diag(1, 1, 1, e^{-2πi/2⁸}) = diag(1, 1, 1, e^{-iπ/128})

- control qubit = first (MSB), target qubit = second (LSB)
- 2-qubit 게이트, 4×4 행렬

### 분해 전략: Rz-CNOT ladder + Clifford+T 근사 합성

controlled 위상 게이트의 표준 분해:

```
CR_z(θ) = (I ⊗ R_z(θ/2)) · CNOT(c,t) · (I ⊗ R_z(-θ/2)) · CNOT(c,t)
```

θ = -π/128이므로:

```
R_z(θ/2)  = R_z(-π/256)   → Clifford+T 근사 필요
R_z(-θ/2) = R_z(+π/256)   → Clifford+T 근사 필요
```

### Gate-List (봉인부품 재조합, NO MatrixGate)

```
# qubit map: c[0] = control, c[1] = target (big-endian)

Rz_approx(+π/256, c[1])        # 근사: Rz(π/256) ≈ T-서열 합성
CNOT(c[0], c[1])
Rz_approx(-π/256, c[1])        # 근사: Rz(-π/256) ≈ T-서열 합성
CNOT(c[0], c[1])
# 전역 위상 보정 (선택, global phase 무시 시 생략)
```

### Rz 근사 합성 (개념적 구조)

Rz(α)를 Clifford+T 게이트 시퀀스로 근사. α = π/256은 π/4의 배수가 아니므로 정확한 분해 불가능.

```
# 예: Rz(π/256) 근사 시퀀스 (개념적, 실제는 Solovay-Kitaev 또는 그리드 검색으로 생성)
# [T, H, T, H, T, ...] — 길이 ≈ 50-60 gate
```

### Ancilla

- **type**: none
- **count**: 0

### Qubit Mapping

| 인덱스 | 역할 | 비고 |
|--------|------|------|
| c[0]   | control | system qubit (MSB) |
| c[1]   | target | system qubit (LSB) |

### Golden Matrix

```python
import numpy as np
golden = np.diag([1, 1, 1, np.exp(-2j*np.pi/2**8)]).astype(complex)
# = diag(1, 1, 1, e^{-iπ/128})
# 전역 위상 atol 1e-7 무시
```

## 2. 근거 (왜 최소)

### 분해 구조 최소화 논거

1. **CNOT 최소화**: controlled 단일-큐빗 게이트는 최소 2 CNOT 필요 (Barenco et al. 1995). 본 분해는 정확히 2 CNOT = 최소.
2. **Rz 게이트 수**: 2회 (θ/2, -θ/2) = 구조적 최소.
3. **T-count**: Rz(π/256) 근사에 T 게이트 수 의존.

### T-cost 추정

| 항목 | 추정 | 근거 |
|------|------|------|
| CNOT | 2 | 구조적 최소 |
| Rz(π/256) T-cost | ~25-30 | 최적 근사 (ε=1e-7) |
| Rz(-π/256) T-cost | ~25-30 | 동일 (반전) |
| **total T** | **~50-60** | 합산 |

### 최소화 근거

- **Solovay-Kitaev bound**: O(log^{3.97}(1/ε)) 게이트. ε=1e-7 → 이론적 상한 ≈ 수백.
- **실제 최적 근사**: Matsumoto-Amano(2008), Kliuchnikov et al.(2020) 기법으로 ~50-60 T 달성 예상.
- **π/256 각도**: π/4의 1/64. 반복 bisection 관계 활용 가능 — Rz(π/256)은 Rz(π/4)의 6단계 "반-회전" 자손.
- 참고: Rz(π/4) = T (정확), Rz(π/8), Rz(π/16), ..., Rz(π/256) — 각 단계 T-cost 증가.

### sealed 전임자와의 관계

cr7_dag_gate(sealed)도 정확히 Clifford+T로 표현 불가한 각도 (θ = -π/64)를 포함. 따라서 cr7†와 cr8† 모두 근사 분해이며, T-cost가 차별화 요소.

## 3. 봉인가능성 (오라클 통과 예측)

### second_oracle numpy 재구성 예측

```python
# 분해 행렬 = Rz_exact(θ) · CNOT · Rz_exact(-θ) · CNOT
# BUT Rz_exact은 근사 시퀀스로 대체됨
# → 최종 행렬 ≈ golden (with error ε on off-diagonal phases)
# → |U_decomp[i,j] - golden[i,j]| < ε for all i,j
```

**핵심 문제**: 근사 분해는 정확한 golden과 **atol 불일치** 가능. 오라클의 u_hash는 exact golden 기준으로 계산되므로, 근사 분해의 u_hash는 불일치할 수 있음.

### 봉인 통과 조건

- atol 1e-7 이내에서만 통과 가능
- Rz(π/256)을 1e-7 정확도로 근사하려면 ~50-60 T 필요
- 실제 Solovay-Kitaev 구현의 근사 오차가 atol 경계 안에 들어가는지 검증 필요

**예측**: 통과 가능성 보통 (≈60%). 근사 정확도가 관건.

### sympy proof 가능성

- **phase proof**: Rz 시퀀스가 정확히 e^{iπ/256}에 도달하는지 증명 필요. 근사적 분해의 경우 대수적 증명 어려움.
- **전략 변경 필요**: 근사 증명이 아닌 수치 검증(`np.allclose` with atol=1e-7)에 의존 가능.
- cr7_dag_gate의 sealed 상태를 참고하여 동일 증명 전략 사용.

### Qualtran bloq 코드 (proposed)

```python
from qualtran.bloqs.basic_gates import ZPowGate
bloq = ZPowGate(exponent=-1/2**(8-1)).controlled()
```

## 4. 위험 (가정)

1. **Clifford+T 근사 정확도**: Rz(π/256)의 정확한 분해 불가능. 근사 오차가 atol 1e-7 경계를 넘으면 봉인 실패.
2. **u_hash mismatch**: golden이 exact matrix인데 분해가 근사 → u_hash 불일치. 전역 위상 무시는 도움이 되지만, 상대 위상 오차는 문제됨.
3. **sealed 전임자 의존**: cr7_dag_gate가 실제로 통과했는지 불확실 (provenance.json 부재 확인). 동일 전략 사용이 유효한지 검증 필요.
4. **T-cost 불확실성**: 50-60 T 추정은 상한. 실제 Solovay-Kitaev 또는 최적 합성 결과는 다를 수 있음.
5. **Big-endian convention**: c[0]=MSB(control), c[1]=LSB(target). golden 행렬의 대각 성분 순서와 일치해야 함.

## 부록: 분해 불가능성 증명 스케치

**정리**: P(π/128) (controlled 여부는 무관)은 Clifford+T 게이트 집합의 유한 시퀀스로 **정확히** 표현 불가능.

**증명**: Clifford+T가 생성하는 군은 48-order 유한군(C₃ group extended by T)과 U(2)의 dense subgroup. T는 8차 primitive root. P(π/128)은 256차 primitive root. 256 ≠ 8k (k∈ℤ)이므로, P(π/128) ∉ ⟨Clifford, T⟩_exact. QED (sketch).

**실용적 함의**: cr4_dag_gate, cr5_dag_gate, ..., cr8_dag_gate 모두 근사 분해만 가능. cr3_dag_gate(θ=π/4=T, exact)만이 유일한 정확한 분해.
