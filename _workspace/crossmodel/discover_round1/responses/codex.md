# Discover Round 1 Response — codex

## PGF 실행 노드

DiscoverRound1Codex // primitive gap 독립 제안 (needs-verify)
    C7XCleanAncillaLadder // c7x 분해 제안 (needs-verify)
        # output: 2*c6x + 1*toffoli, clean ancilla 1
        # criteria: golden permutation, ancilla restored to |0>
    CR8DagAnalyticPhase // cr8_dag_gate 분해 제안 (needs-verify)
        # output: controlled ZPowGate exponent=-1/2**7
        # criteria: diag(1,1,1,exp(-2*pi*i/2**8))

## 1. c7x — 7-control Toffoli

### 제안(분해 회로)

목표 qubit mapping:

- controls: `c0,c1,c2,c3,c4,c5,c6`
- target: `t`
- clean ancilla: `a=|0>`
- big-endian system order for oracle hashing: `[c0,c1,c2,c3,c4,c5,c6,t]`; ancilla is workspace and must be traced only after restored.

Gate-list, using sealed predecessor components and no `MatrixGate`:

```json
{
  "gap_id": "c7x",
  "n_sys": 8,
  "n_anc": 1,
  "ancilla": [{"name": "a", "kind": "clean", "initial": 0, "final": 0}],
  "steps": [
    {"spec": "../modules/c6x.pg", "targets": ["c0", "c1", "c2", "c3", "c4", "c5", "a"]},
    {"spec": "../modules/toffoli.pg", "targets": ["a", "c6", "t"]},
    {"spec": "../modules/c6x.pg", "targets": ["c0", "c1", "c2", "c3", "c4", "c5", "a"]}
  ]
}
```

PPR proof sketch:

```python
def c7x_ladder(c: list[int], t: int, a: int = 0) -> tuple[int, int]:
    # c has length 7; a is clean.
    a ^= c[0] & c[1] & c[2] & c[3] & c[4] & c[5]
    t ^= a & c[6]
    a ^= c[0] & c[1] & c[2] & c[3] & c[4] & c[5]
    return t, a
```

Result:

```text
a_final = 0
t_final = t XOR (c0 & c1 & c2 & c3 & c4 & c5 & c6)
```

### 근거(왜 최소)

이 제안은 `c6x` 봉인부품을 frontier predecessor로 쓰는 최소 ladder다. `c7x`를 직접 쓰지 않고 7개 control의 conjunction을 target에 전달하려면, 적어도 한 번은 6-control partial conjunction을 workspace에 써야 한다. clean ancilla 계약에서는 그 workspace를 원상복구해야 하므로 동일 partial compute의 역연산이 필요하다. 남은 control `c6`와 partial bit를 target에 결합하는 최소 reversible step은 `toffoli` 1개다.

따라서 clean-ancilla, predecessor-reuse cost model에서는 `2*c6x + 1*toffoli`가 자연 최소 후보이며, 더 짧은 `1*c6x + ...` 형태는 ancilla를 dirty 상태로 남기거나 7-control condition을 실제로 target에 결합하지 못한다.

### 봉인가능성(오라클 통과 예측)

높음. 회로는 순열 전용이고 phase-free다. `second_oracle`은 9-qubit unitary를 구성한 뒤 clean ancilla in/out `0` block을 8-qubit effective permutation으로 축약하면 `c7x` golden과 일치할 것이다. `sympy` proof도 위 Boolean 등식으로 충분하다.

예상 hash 수렴성: 높음. canonical predecessor decomposition을 쓰면 gate sequence가 짧고 대칭성이 낮아 다른 런타임도 같은 `c6x,toffoli,c6x` 후보로 수렴할 가능성이 크다.

### 자원추정(T/Toffoli)

- sealed-module cost: `2*c6x + 1*toffoli`
- explicit Toffoli primitive count at this layer: `1`
- exact Clifford+T canonical Toffoli assumption: `T = 2*T(c6x) + 7`
- ancilla: `1 clean`
- depth at sealed-module layer: `3`

### 위험(가정)

- `toffoli.pg`가 module registry에 없고 basic gate name만 허용된다면 step 2를 local primitive `Toffoli(c=["a","c6"], target="t")`로 표기해야 한다.
- oracle이 ancilla 포함 full unitary hash만 요구하면 `n_sys=8,n_anc=1` 메타를 명시해야 한다. effective system-only hash를 요구하면 clean block projection 규칙이 필요하다.
- 순서 관례는 `c6x.pg`와 동일하게 마지막 target, 앞쪽 controls로 가정했다.

## 2. cr8_dag_gate — controlled-phase R8 dagger

### 제안(분해 회로)

목표 qubit mapping:

- control: `q0`
- target: `q1`
- big-endian basis: `|q0 q1>`
- golden: `diag(1,1,1,exp(-2*pi*i/2**8))`

Gate-list, analytic primitive and no `MatrixGate`:

```python
from qualtran.bloqs.basic_gates import ZPowGate

bloq = ZPowGate(exponent=-1/2**(8-1)).controlled()
```

Equivalent module payload:

```json
{
  "gap_id": "cr8_dag_gate",
  "n_sys": 2,
  "n_anc": 0,
  "steps": [
    {"gate": "Controlled(ZPowGate)", "control": "q0", "target": "q1", "exponent": -0.0078125}
  ]
}
```

### 근거(왜 최소)

기존 `crK` family의 sealed predecessor pattern은 `ZPowGate(exponent=-1/2**(k-1)).controlled()`다. Qualtran `ZPowGate(exponent=e)`의 target phase는 `exp(i*pi*e)`이므로 controlled form의 `|11>` entry는:

```text
exp(i*pi*(-1/2**7)) = exp(-2*pi*i/2**8)
```

따라서 하나의 analytic controlled phase gate가 정확히 target golden을 생성한다. No-`MatrixGate` 조건도 만족하며, decomposition을 여러 lower-angle controlled phase로 풀 이유가 없다. `cr7_dag_gate`에서 `cr8_dag_gate`로 exponent denominator만 한 단계 증가시키는 family-continuation이므로 canonical성이 높다.

### 봉인가능성(오라클 통과 예측)

높음. `second_oracle`은 독립적으로 4x4 diagonal을 만들면 된다:

```python
golden = np.diag([1, 1, 1, np.exp(-2j*np.pi/2**8)]).astype(complex)
```

전역위상 무시 `atol=1e-7` 조건에서도 비대상 basis `[00,01,10]`은 1이고 `[11]`만 음의 256분근 phase를 갖는다. `sympy` proof는 `exp(I*pi*(-1/128)) == exp(-2*pi*I/256)`의 지수 동치로 닫힌다.

### 자원추정(T/Toffoli)

- analytic gate layer: `1 controlled ZPowGate`
- Toffoli count: `0`
- ancilla: `0`
- if treated as exact parametric phase primitive: `T = 0`
- if forcibly compiled to finite Clifford+T only: exact representation is not finite for denominator 128 under ordinary Clifford+T; then this must be approximate synthesis and should not be used for exact seal hashing.

### 위험(가정)

- `TASKSPEC.md`의 prose target은 dagger 음수 phase인데, 한 줄 golden 설명에는 `exp(2πi/2^k)` 양수 부호가 섞여 있다. 이 응답은 sealed predecessor `cr7_dag_gate`와 dagger 명칭에 맞춰 음수 phase를 선택한다.
- oracle이 `ZPowGate` convention을 다르게 해석하면 exponent sign/scale mismatch가 날 수 있다. 현재 repo의 `cr7_dag_gate.pg` convention과 동일한 `exponent=-1/2**(k-1)`을 기준으로 한다.

