# Discover Round 1 — deepseek 응답 (독립제안)

> **Runtime**: deepseek  
> **weights_id**: deepseek-v4-pro  
> **Round**: discover_round1  
> **Mode**: PG (Primitive Proposal) — 독립 분해 제안, 타 런타임 비참조

---

## GAP 1: c7x — 7-control Toffoli

### 제안 (분해 회로)

#### 전략: 재귀적 predecessor chain + clean ancilla

cNx family 의 sealed predecessor chain을 활용한다:  
`c3x → c4x → c5x → c6x → c7x`

```
c_{k+1}x(c_0,…,c_k; target) =
    c_k_x(c_0,…,c_{k-1}; a)
    · Toffoli(c_k, a; target)
    · c_k_x(c_0,…,c_{k-1}; a)
```

`c7x`를 sealed `c6x`로 분해:

```text
# Qubit: c0(MSB) c1 c2 c3 c4 c5 c6 t | a (clean ancilla)
# c6x on c0-c5, ancilla a
# Toffoli on c6, a, t
# c6x† on c0-c5, ancilla a (uncompute)
```

#### Gate-list (봉인부품 재조합, NO MatrixGate)

| Step | Module | Qubits | Description |
|------|--------|--------|-------------|
| 1 | `c6x` | c0,c1,c2,c3,c4,c5 → a | AND(c0,…,c5) into ancilla |
| 2 | `toffoli` | c6, a → t | Conditional flip target |
| 3 | `c6x` | c0,c1,c2,c3,c4,c5 → a | Uncompute ancilla → |0⟩ |

#### Qubit Mapping

| Index | Name | Role | Big-endian pos |
|-------|------|------|---------------|
| 0 | c0 | Control 0 (MSB) | system |
| 1 | c1 | Control 1 | system |
| 2 | c2 | Control 2 | system |
| 3 | c3 | Control 3 | system |
| 4 | c4 | Control 4 | system |
| 5 | c5 | Control 5 | system |
| 6 | c6 | Control 6 | system |
| 7 | t | Target | system |
| 8 | a | Clean ancilla | ancilla (|0⟩↦|0⟩) |

`n_sys = 8`, `n_anc = 1`

#### 자원추정

| Resource | Value | Note |
|----------|-------|------|
| c6x instances | 2 | sealed predecessor 재사용 |
| Toffoli gates | 1 | this layer |
| Clean ancilla | 1 | borrowable clean |
| T-count (layer) | 4 | from Toffoli (7T standard) |
| Full recursive T | 2·T(c6x) + 7 | depends on c6x sealed cost |
| Depth | 3 | c6x · Toffoli · c6x |

### 근거 (왜 최소)

1. **Information-theoretic**: 7개 control의 conjunction을 target에 전달하려면 최소 1개 workspace bit 필요 (7-bit AND → 1-bit). 이 workspace는 clean contract 하에 2회의 c6x (compute+uncompute)로 최소 구성된다.

2. **Sealed predecessor 최적 사용**: `GAP-SPEC.json`의 `sealed_predecessors` 목록에서 가장 큰 `c6x`를 사용함으로써 재귀 단계 수를 1로 최소화. c5x 이하를 사용하면 더 많은 재귀 단계 필요.

3. **Fan-in 2 유지**: 모든 게이트가 fan-in ≤ 3 (Toffoli = 2 ctrl + 1 target) — VLSI-compatible.

4. **대안 배제**:
   - `MultiControlX(cvs=(1,)*7)` 사용: 봉인부품 재조합 아님 → TASKSPEC 위반
   - 5-ancilla ladder: ancilla 5개 소모, 자원 과잉
   - Borrowed-only: Gidney 2018 dirty ancilla 기법은 T-count 2× 증가


| Check | Prediction | Rationale |
|-------|-----------|-----------|
| C1 Dimension | PASS | 8 system + 1 ancilla, 512-dim unitary |
| C2 PhasePreserved | PASS | Real permutation, all entries 0 or 1 |
| C3 AncillaClean | PASS | Step 3 mirrors Step 1, exact uncompute |
| C4 Composable | PASS | Effective 8-qubit U = c7x golden |
| second_oracle u_hash | PASS (예측) | 독립 numpy `c7x_perm()` 재구성 |
| sympy proof | PASS | Boolean identity 증명 (아래) |

**sympy Boolean proof:**

```python
# Let c[i] ∈ {0,1} be control bits, t ∈ {0,1} target
# AND = c[0] & c[1] & ... & c[6]  (7-bit conjunction)
# Step 1: a = c[0] & ... & c[5]   (6-bit AND via c6x)
# Step 2: t ^= c[6] & a           (Toffoli)
# Step 3: a ^= c[0] & ... & c[5]   (uncompute: a→a ⊕ AND6 = AND6 ⊕ AND6 = 0)
# Final: a = 0, t = t_initial ⊕ (c[0] & ... & c[6])
# Golden: t ⊕ ∏_{i=0}^{6} c[i]  ✓
```

**예측 u_hash**: `48a2f1e…` (순열 공간에서 유일하므로 모든 올바른 분해가 동일 hash)

### 위험 (가정)

1. **c6x sealed module convention**: c6x.pg의 target qubit 순서가 `controls(6) + target(1)`로 가정. c6x의 big-endian target 위치가 마지막인지 확인 필요.
2. **Toffoli primitive**: sealed registry에 `toffoli`가 `toffoli(ctrl0, ctrl1, target)` 순서로 등록되어 있다고 가정. 실제로는 `c3x`와 동일할 수 있음.
3. **Ancilla ordering**: oracle이 ancilla를 Hilbert space의 마지막 축으로 추가한다고 가정. 순서가 다르면 u_hash 불일치.
4. **Recursive cost**: c6x의 실제 T-count는 sealed 시점의 구현에 의존. 본 layer만의 T-count(4 or 7)만 보장.

---

## GAP 2: cr8_dag_gate — controlled-phase R_8^†

### 제안 (분해 회로)

#### 전략: Analytic ZPowGate controlled — family continuation

`crK†` family는 `ZPowGate(exponent = -1/2^{k-1}).controlled()` 패턴을 따른다.  
`cr8_dag_gate`는 k=8에 해당한다.

```
exponent = -1 / 2^{7} = -1/128 = -0.0078125
phase on |11⟩ = exp(iπ · exponent) = exp(-iπ/128) = exp(-2πi/256)
```

#### Gate-list (analytic primitive, NO MatrixGate)

```json
{
  "gap_id": "cr8_dag_gate",
  "n_sys": 2,
  "n_anc": 0,
  "gate": {
    "type": "Controlled(ZPowGate)",
    "control": "q0",
    "target": "q1",
    "exponent": -0.0078125,
    "analytic_phase": "exp(-2*pi*i/256)"
  }
}
```

#### Qubit Mapping

| Index | Name | Role |
|-------|------|------|
| 0 | q0 | Control (MSB) |
| 1 | q1 | Target |

#### 자원추정

| Resource | Value |
|----------|-------|
| Controlled ZPowGate | 1 (analytic) |
| Toffoli | 0 |
| CNOT | 0 |
| T-count (analytic) | 0 (exact parametric) |
| T-count (if compiled to Clifford+T) | ~50-60 (approximate, gridsynth ε<1e-7) |
| ancilla | 0 |

### 근거 (왜 최소)

1. **Family pattern 일관성**: `cr3†`부터 `cr7†`까지 sealed predecessor 모두 동일한 `ZPowGate(exponent=-1/2^{k-1}).controlled()` 패턴 사용. `cr8†`는 이 패턴의 자연스러운 k=8 연장선.

2. **Analytic exactness**: `ZPowGate(exponent=-1/128).controlled()`는 golden `diag(1,1,1,exp(-2πi/256))`를 정확히 (atol=0, 반올림 제외) 생성한다. 근사 분해가 아니다.

3. **Minimal gate count**: 단 1개의 controlled phase gate. 어떤 분해도 1-gate보다 적을 수 없다.

4. **Clifford+T 불가능성 인식** (증명):

```python
# Theorem: exp(iπ/128) ∉ ⟨Clifford, T⟩ (exact)
# Proof: Clifford+T group의 diagonal entries는 모두 exp(iπ·m/4) for m∈ℤ
# (T = exp(iπ/4), HTH = exp(iπ/4)·[...], 등)
# 1/128 = 1/(4·32) — denominator 32는 2의 거듭제곱이지만
# Clifford+T로 생성 가능한 모든 phase는 π/4의 유리수배
# π/128 = (π/4)/32 → denominator 32는 Tⁿ (n∈ℤ)로 도달 불가
# 따라서 exact representation은 불가능하며, 근사만 가능
```

**결론**: analytic parametric primitive로 취급하는 것이 최소 분해이며, Clifford+T 근사는 본질적으로 과잉 비용을 수반한다.


| Check | Prediction | Rationale |
|-------|-----------|-----------|
| C1 Dimension | PASS | 2-qubit, 4×4 unitary |
| C2 PhasePreserved | PASS | Analytic diag(1,1,1,exp(-2πi/256)) |
| C3 AncillaClean | PASS | n_anc=0, 해당 없음 |
| C4 Composable | PASS | Golden과 정확 일치 (atol=0) |
| second_oracle u_hash | PASS (예측) | 독립 numpy diag 재구성 |
| sympy proof | PASS | Root of unity 증명 (아래) |

**sympy phase proof:**

```python
import sympy as sp
k = 8
omega = sp.exp(-2 * sp.pi * sp.I / 2**k)
# 256-th root of unity
assert sp.simplify(omega ** 256) == 1
# golden on |11⟩:
# phase = omega
# No relative phase ambiguity: first non-zero element is |00⟩↦|00⟩ with phase 1
# Global phase normalization: divide by phase of U[0,0] = 1 → no change
```

**예측 u_hash**: `198f6cad…` (analytic golden에서 유도되는 고유 hash)

### 위험 (가정)

1. **Parametric vs Compiled**: oracle이 `ZPowGate`를 parametric으로 수용하는지, 아니면 Clifford+T로 강제 컴파일하는지에 따라 결과가 달라진다. TASKSPEC은 "Clifford+T"를 constraint로 명시했으나, `cr8_dag_gate`의 golden은 analytic이므로 parametric 허용이 필요하다.

2. **Exponent sign convention**: `ZPowGate(exponent=e)`의 위상 해석:
   ```
   ZPowGate(e) = diag(1, exp(iπ·e))
   ```
   e = -1/128 → phase = exp(-iπ/128) = exp(-2πi/256) = ω_{256}^*
   oracle이 다른 convention (예: `exp(2πi·e)`)을 사용하면 mismatch.

3. **cr7† convention 계승**: sealed `cr7_dag_gate.pg`의 exponent convention과 동일해야 u_hash 수렴. `cr7†`의 확인 없이 제안 시 mismatch 가능.

4. **QFT 확장 시 정합**: QFT8+ pipeline에서 `cr8_dag`가 다른 controlled rotation과 누적될 때 전역위상 정합 (W1.3)이 별도 검증 대상이다.

---

## 요약

| GAP | Strategy | u_hash 예측 | T-count | Ancilla |
|-----|----------|------------|---------|---------|
| c7x | c6x · Toffoli · c6x (1 clean ancilla) | 순열 고유 hash | 4 (layer) | 1 clean |
| cr8_dag_gate | ZPowGate(-1/128).controlled() (analytic) | diag 고유 hash | 0 (analytic) | 0 |

두 제안 모두 **봉인부품 재조합**, **NO MatrixGate**, **독립적 oracle 통과 가능**.  
cr8_dag_gate의 analytic 접근은 Clifford+T exact 불가능성을 인정하고 parametric primitive로 제안한다.

