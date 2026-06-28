# Discover Round 1 — Primitive Proposals (Kimi)

> 응답 형식: 제안(분해 회로) · 근거(왜 최소) · 봉인가능성(오라클 통과 예측) · 위험(가정)

---

## GAP 1: `c7x` — 7-control Toffoli (multi-controlled X)

### 제안 분해 회로

**타겟:** 7개 제어 큐비트 `c0 … c6`, 타겟 큐비트 `t`, 클린 보조 큐비트 5개 `a0 … a4`.

게이트 리스트(총 11개 Toffoli):

```text
# forward AND-chain
Toffoli(c0, c1, a0)
Toffoli(c2, a0, a1)
Toffoli(c3, a1, a2)
Toffoli(c4, a2, a3)
Toffoli(c5, a3, a4)
Toffoli(c6, a4, t)      # 최종 제어 곱을 타겟에 XOR

# reverse uncompute
Toffoli(c5, a3, a4)
Toffoli(c4, a2, a3)
Toffoli(c3, a1, a2)
Toffoli(c2, a0, a1)
Toffoli(c0, c1, a0)
```

**큐비트 매핑:**

| 레지스터 | 역할 | 수 |
|---|---|---|
| `c0 … c6` | 제어 | 7 |
| `t` | 타겟 | 1 |
| `a0 … a4` | clean ancilla | 5 |
| **합계** | | **13** |

**자원 추정:**

| 항목 | 값 |
|---|---|
| Toffoli 개수 | 11 |
| Clean ancilla | 5 |
| Clifford+T 기준 T-count (표준 7T/Toffoli) | 77 T |
| Clifford+T 기준 T-depth (Toffoli depth 3 기준) | 33 |
| 측정 기반 Toffoli 사용 시 (Jones 2013) | 44 T, 고전 피드포워드 필요 |

### 근거: 왜 최소

- Barenco et al. (1995) Lemma 7.3에 따르면 `n`-제어 Toffoli는 `n‑2`개 clean ancilla로 `2n‑3`개 Toffoli로 분해되며, 이는 ancilla 사용 분해의 이론적 하한과 일치합니다.
- `n = 7`이면 `2·7 − 3 = 11`이며, ancilla 개수 `7 − 2 = 5`입니다.
- Toffoli를 더 이상 분해하지 않고 원자 게이트로 취급하면 게이트 수 11은 최소의 재귀적 AND-chain 구조입니다.

### 봉인가능성 예측

- **second_oracle numpy `u_hash` 일치:** 높음. 위 회로는 순열 행렬이며, golden permutation `|c…c,t⟩ → |c…c, t⊕(c0∧…∧c6)⟩`와 동일합니다.
- **sympy 증명:** AND-chain의 언컴퓨트가 완전하면 ancilla가 |0⟩로 복원되고, 타겟에만 `c0∧…∧c6` XOR이 적용됩니다. 증명은 부울 대수 `a_i = c_{2i} ∧ a_{i-1}`의 재귀 전개로 가능합니다.
- 예상 통과: `u_hash` 일치 + sympy 부울 동치 증명.

### 위험 / 가정

1. **Clean ancilla 가정:** 보조 큐비트가 |0⟩로 초기화되고 최종 |0⟩로 복원됩니다. Borrowed ancilla 사용 시 회로가 달라집니다.
2. **Toffoli primitive 가정:** 본 제안은 Toffoli를 sealed primitive로 재사용합니다. 만약 오라클이 Toffoli를 강제로 Clifford+T로展開해야 한다면 T-count 77, T-depth 33을 기준으로 검증해야 합니다.
3. **big-endian MSB:** 첫 제어 레지스터가 MSB라고 가정합니다. 큐비트 매핑은 순열에 불과하므로 실제 인덱스는 오라클의 매핑에 따라 달라질 수 있습니다.

---

## GAP 2: `cr8_dag_gate` — controlled-phase `R_8† = diag(1, e^{-2πi/2^8})`

### 제안 분해 회로

**타겟:** 2큐비트 제어 위상 게이트 `CR_8† = diag(1, 1, 1, e^{-2πi/2^8})`.

일반 controlled-U 공식(Nielsen & Chuang Box 4.1)을 적용합니다.

```text
# U = R_8† = diag(1, e^{-iθ}), θ = 2π/2^8
# U = e^{-iθ/2} · R_z(-θ),  R_z(φ) = diag(e^{-iφ/2}, e^{iφ/2})
# A = R_z(-θ/2), B = R_z(θ/2), C = I, α = -θ/2

(R_z(-θ/2) ⊗ I)     # 제어 큐비트 보정 위상
(I ⊗ R_z(-θ/2))     # 타겟 위상
CNOT(control, target)
(I ⊗ R_z(θ/2))      # 타겟 위상
CNOT(control, target)
```

`R_z(±θ/2)`는 `R_9^{±1}`과 전역 위상 차이만 있습니다. 봉인부품 관점에서는 다음과 같이 재표현할 수 있습니다:

```text
# 동등 표현 (R_9 primitive 사용, 제어에 상대 위상 보정 포함)
(I ⊗ R_9†)
CNOT(control, target)
(I ⊗ R_9)
CNOT(control, target)
+ 필요 시 제어 큐비트에 R_z(-θ/2) 보정
```

**큐비트 매핑:**

| 레지스터 | 역할 | 수 |
|---|---|---|
| `c` | control | 1 |
| `t` | target | 1 |
| **합계** | | **2** |

**자원 추정:**

| 항목 | 값 |
|---|---|
| CNOT | 2 |
| 단일 큐비트 위상 회전 (`R_9`/`R_9†`) | 3 |
| ancilla | 0 |
| T-count (R_9를 Clifford+T로 정확 합성 시) | 유한한 정확 합성 불가; ε=2^{-9} 근사 시 약 수백~수천 T |

### 근거: 왜 최소

- 임의 단일 큐비트 U에 대한 2-CNOT controlled-U 분해는 이론적으로 최소(CNOT 하한 2)입니다.
- `R_8†`는 단일 큐비트 위상 게이트이므로 2-CNOT + 3단일 위상 회전 구조가 자연스럽습니다.
- CNOT을 1개로 줄이려면 U가 대각(제어 위상)이어도 일반적으로 불가능하며, 2개 CNOT이 필요합니다.

### 봉인가능성 예측

- **second_oracle numpy `u_hash` 일치:** 높음. golden `diag(1,1,1,exp(2πi/2^8))`의 adjoint는 `diag(1,1,1,exp(-2πi/2^8))`이며, 위 분해가 동일한 4×4 대각 행렬을 생성합니다.
- **sympy 증명:** controlled-U 공식 `U = e^{iα} A X B X C, ABC = I`를 대입하면 `A = R_z(-θ/2), B = R_z(θ/2), C = I, α = -θ/2`가 `R_8†`를 정확히 재구성함을 확인할 수 있습니다.
- 예상 통과: `u_hash` 일치 + sympy 부호/위상 검증.

### 위험 / 가정

1. **전역 위상 처리:** `R_z(φ)`와 `R_9`는 전역 위상 차이가 있습니다. 오라클이 `atol=1e-7`로 전역 위상을 무시하므로 문제 없습니다.
2. **Clifford+T 합성:** `R_9`는 Clifford+T 군에 정확히 속하지 않습니다. 봉인부품으로 `R_9`를 그대로 사용하거나, 허용 오차 내 근사 합성(Solovay–Kitaev / 최적화 검색)이 필요합니다. 제안서는 전자를 가정합니다.
3. **제어/타겟 규칙:** CNOT이 `control → target` 기준으로 작동한다고 가정합니다. 오라클의 큐비트 순서가 다르면 위상 보정 항의 부호가 바뀔 수 있습니다.

---

## 요약

| GAP | 핵심 아이디어 | 핵심 자원 | 예상 봉인 |
|---|---|---|---|
| `c7x` | Barenco AND-chain + uncompute | 11 Toffoli, 5 clean ancilla | 높음 |
| `cr8_dag_gate` | 2-CNOT controlled-U 분해 | 2 CNOT, 3×`R_9` 위상 | 높음 |
