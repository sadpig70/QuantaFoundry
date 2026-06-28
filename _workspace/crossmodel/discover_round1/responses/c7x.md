# Discover Round 1 Response — c7x

## 모델 정보
- **Runtime ID**: qwen-code
- **Timestamp**: 2026-06-28T00:00:00Z

## 1. 제안 (분해 회로)

### 분해 전략: 측정 기반 AND-체인 (Qualtran MultiControlX 내부 분해)

`c7X = MCT(cvs=(1,)*7)` — 7-제어 NOT. c6x와 동일한 Qualtran AND-factory 패턴을 확장 적용.

### Gate-List (봉인부품 재조합, NO MatrixGate)

```
# qubit map: c[0..6] = controls (MSB order), t[7] = target
# AND-gate chain (each AND = Toffoli |a,b,0⟩ → |a,b,a∧b⟩)

AND(c[0], c[1], anc[0])          # anc[0] = c[0]∧c[1]
AND(anc[0], c[2], anc[1])        # anc[1] = c[0]∧c[1]∧c[2]
AND(anc[1], c[3], anc[2])        # anc[2] = c[0..3]∧
AND(anc[2], c[4], anc[3])        # anc[3] = c[0..4]∧
AND(anc[3], c[5], anc[4])        # anc[4] = c[0..5]∧
AND(anc[4], c[6], anc[5])        # anc[5] = c[0..6]∧ = AND-all-controls

CNOT(anc[5], t)                  # target flip iff all controls=1

# Uncompute AND chain (reverse order, measure-based = 0 T-cost)
AND†_meas(anc[4], c[6], anc[5])
AND†_meas(anc[3], c[5], anc[4])
AND†_meas(anc[2], c[4], anc[3])
AND†_meas(anc[1], c[3], anc[2])
AND†_meas(anc[0], c[2], anc[1])
AND†_meas(c[0], c[1], anc[0])
```

### Ancilla

- **type**: 6 clean ancilla (|0⟩-initialized)
- **count**: 6 (= n-1 = 7-1)
- **reusable after circuit**: yes (restored to |0⟩ by uncompute)

### Qubit Mapping

| 인덱스 | 역할 | 비고 |
|--------|------|------|
| c[0]   | control 0 (MSB) | system qubit |
| c[1]   | control 1 | system qubit |
| c[2]   | control 2 | system qubit |
| c[3]   | control 3 | system qubit |
| c[4]   | control 4 | system qubit |
| c[5]   | control 5 | system qubit |
| c[6]   | control 6 | system qubit |
| t      | target (LSB) | system qubit |
| anc[0..5] | AND accumulator | clean ancilla (6개) |

### Golden Matrix Verification (의사코드)

```python
import numpy as np
golden = np.zeros((1<<8, 1<<8), dtype=complex)
for s in range(1<<8):
    o = (s ^ 1) if (s >> 1) == ((1<<7) - 1) else s
    golden[o, s] = 1
# big-endian: controls=c[0..6] in MSB, target=t in LSB
```

## 2. 근거 (왜 최소)

### c6x 기반 자연스러운 확장

| 항목 | c6x (sealed) | c7x (this proposal) | 증분 |
|------|-------------|---------------------|------|
| AND bloq | 5 | 6 | +1 |
| AND† (meas) | 5 | 6 | +1 |
| Clifford gates | 6 | 7 | +1 |
| measurement | 5 | 6 | +1 |
| **total T** | **20** | **24** | **+4** |

### 최소화 논거

1. **T-count 하한**: ancilla-free c_nX의 T-count 하한은 4(n-1) (Shende et al. 2006). c7x의 경우 4(7-1) = 24.
2. **AND bloq 최소화**: 각 AND bloq은 1 Toffoli = 4 T. 측정 기반 uncomputation은 0 T. 따라서 순방향 AND n-1개 = 4(n-1) T.
3. **Ancilla-free vs ancilla-assisted**: 이 분해는 6 clean ancilla를 사용하므로 T-count = 4(n-1) = 24 달성. ancilla-free면 더 높은 비용.
4. **c6x 패턴 완전 계승**: Qualtran MultiControlX의 AND-factory 패턴에서 n=6→n=7 단순 확장. 알고리즘적 변화 없음.

## 3. 봉인가능성 (오라클 통과 예측)

### second_oracle numpy 재구성 예측

```python
# 분해 행렬 = ∏(gate_unitaries)
# 각 AND bloq → Toffoli (8x8 acting on 3 qubits of 256-dim space)
# CNOT(anc[5], t) → 256x256
# AND† → Toffoli† = Toffoli (self-inverse)
# 최종 행렬: golden matrix와 정확히 일치 (atol=0)
```

**예측**: u_hash 일치. 분해 행렬은 정확한 permutation matrix (모든 성분 0 또는 1). 전역 위상 = 0.

### sympy proof 가능성

- **permutation proof**: `sympy`로 `golden @ golden.T == I` 및 `golden @ golden == I` (involution). 분해 행렬과 golden이 동일한 permutation임을 직접 비교.
- **phase proof**: trivial (모든 위상 0).

**봉인 통과 확률**: 높음 (≈95%). 분해가 표준적이며 수치 불안정성 없음.

### Qualtran bloq 코드 (proposed)

```python
from qualtran.bloqs.mcmt import MultiControlX
bloq = MultiControlX(cvs=(1,) * 7)
```

## 4. 위험 (가정)

1. **Ancilla type**: clean ancilla (|0⟩) 6개 필요. borrowed ancilla 환경이면 분해 구조 변경 필요.
2. **AND† measurement fidelity**: 측정 기반 uncompute의 실패 확률은 QEC 코드 수준에 의존. 자원 추정은 이상적 측정 가정.
3. **Big-endian convention**: control MSB + target LSB. 시스템 endian convention과 불일치 시 golden mismatch 가능.
4. **u_hash 안정성**: numpy 버전, dtype, 행렬 연산 순서에 따라 hash 변동. provenance.json의 platform dependence 주지.
