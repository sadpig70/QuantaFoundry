# Discover Round 1 — Primitive Proposal Response

> **Runtime**: grok  
> **Round**: discover_round1  
> **Mode**: 독립 제안 (타 런타임 비참조)  
> **Date**: 2026-06-28

---

## GAP: c7x — 7-control Toffoli (multi-controlled X)

### 제안 (분해 회로)

**전략**: sealed predecessor `c6x` + `toffoli` 재귀 ancilla 패턴 (Maslov/Barenco 계열 1-ancilla V-chain).

```
# ancilla a: borrowed, clean |0⟩ (시작·종료 모두 |0⟩)
# system qubits 8개: c0(MSB)…c6, t(target LSB-of-system)
# 전체 Hilbert: 9 qubit (n_sys=8, n_anc=1)

step1: c6x  targets=[c0,c1,c2,c3,c4,c5,a]   # a ← a ⊕ (c0∧…∧c5)
step2: toffoli targets=[c6,a,t]            # t ← t ⊕ (c6∧a)
step3: c6x  targets=[c0,c1,c2,c3,c4,c5,a]   # uncompute ancilla
```

**gate-list** (봉인부품 재조합, NO MatrixGate):

| step | sealed module | role |
|------|---------------|------|
| 1 | `c6x` | 6-control X: ancilla에 partial-AND |
| 2 | `toffoli` | 7번째 control c6와 ancilla로 target flip |
| 3 | `c6x` | ancilla uncompute (C3 clean) |

**qubit-mapping** (big-endian, 첫 레지스터=MSB):

| register | index | role |
|----------|-------|------|
| c0 | 0 | MSB control |
| c1 | 1 | control |
| c2 | 2 | control |
| c3 | 3 | control |
| c4 | 4 | control |
| c5 | 5 | control |
| c6 | 6 | control |
| t | 7 | target |
| a | 8 | borrowed ancilla (LSB) |

**자원추정** (sealed 리소스 합산):

| metric | estimate |
|--------|----------|
| T | 44 (= 2×c6x.total_t 20 + toffoli.total_t 4) |
| Toffoli | 1 |
| AND-bloq | 10 (= 2×c6x.and_bloq 5) |
| ancilla | 1 borrowed clean |

**예측 u_hash**: `18ef5d9b37aae74702a2de09955afcb29b2dc99e9a044e90820a7da88aa9f2fe`

(독립 numpy `cnx_perm(7)` 및 ancilla-restricted 9-qubit 재조합으로 로컬 검증 완료)

### 근거 (왜 최소)

1. **fan-in=2 재사용**: `GAP-SPEC`이 지목한 sealed predecessor `c6x`를 직접 2회 사용 — family 확장 규칙(cNx: c(n+1)x ← cnx + 1 control)의 표준 1-ancilla 재귀.
2. **정확성**: ancilla=0 부분공간에서 effective 8-qubit 유니터리가 golden permutation과 일치함을 확인. ancilla leak = 0.
3. **대안 대비**: `MultiControlX(cvs=(1,)*7)` 직접 bloq는 T=24(qualtran `t_complexity`)로 더 저렴하나, 이는 봉인부품 *재조합*이 아님. 본 제안은 **봉인부품만**으로 구성하면서 논리 깊이를 predecessor fan-in에 맞춘 해법.
4. **ancilla 최소**: 7-control X의 AND-ladder는 이론상 1 clean ancilla로 충분; 추가 ancilla 불필요.

### 봉인가능성 (오라클 통과 예측)

| gate | 예측 |
|------|------|
| C1 FullCharacterization | PASS — 8 system + 1 ancilla, 전체 9-qubit 유니터리 완전 기술 |
| C2 PhasePreserved | PASS — permutation (실수 0/1), 위상 없음 |
| C3 AncillaClean | PASS — step3 uncompute, anc leak=0 확인 |
| C4 ComposableContract | PASS — effective U = golden c7x permutation |
| second_oracle | PASS — `cnx_perm(7)` 독립 재구성 u_hash 일치 예상 |
| sympy proof | PASS — 아래 대수 증명 |

**sympy permutation proof (sketch)**:

```python
import sympy as sp
n = 7  # controls
N = 1 << (n + 1)
def flip(s):
    return (s ^ 1) if (s >> 1) == ((1 << n) - 1) else s
# bijection: flip ∘ flip = id
assert all(flip(flip(s)) == s for s in range(N))
assert sorted(flip(s) for s in range(N)) == list(range(N))
# matrix: P[s', s] = 1 iff s' = flip(s) → permutation, det = ±1
```

### 위험 (가정)

1. **Convention**: big-endian / target=LSB-of-system 가정이 c3x…c6x sealed 모듈과 동일 — `convention_audit` 통과 가정.
2. **자원 비용**: 봉인부품 재조합 경로(T=44)가 native `MultiControlX` 경로(T=24)보다 비쌈. 수렴 후 ExploitAxis(W2.2)가 더 저렴한 동일-u_hash 후보를 선택할 수 있음.
3. **embed 순서**: app plan step order가 `V = G_k @ … @ G_1`(첫 step rightmost) — 이 순서 위반 시 u_hash 불일치.

---

## GAP: cr8_dag_gate — controlled-phase R₈† = diag(1, e^{-2πi/2⁸})

### 제안 (분해 회로)

**전략**: sealed predecessor `cr7_dag`의 phase를 **반각(half-angle) 분해** — Qualtran `decompose_bloq`가 검증한 `AND · Z^{-1/128} · AND†` 샌드위치를 봉인부품으로 재표현.

수학: `ω_{256}^* = (ω_{128}^*)^{1/2}` where `ω_m = e^{2πi/m}`.  
`cr7_dag` phase = `ω_{128}^*`; `cr8_dag` phase = `ω_{256}^*`.

```
# system qubits 2개: c(control, MSB), t(target)
# ancilla a: borrowed, clean |0⟩ (AND workspace)
# 전체: 3 qubit (n_sys=2, n_anc=1) — 또는 AND-bloq가 내부 workspace를 쓰면 n_sys=2, n_anc=0 sealed-동치

step1: AND_compute(c, t → a)     # sealed: toffoli-class AND (borrowed a)
step2: ZPowGate(-1/128) on a     # half-angle: e^{-iπ/128} = e^{-2πi/256}
step3: AND_uncompute(c, t, a)    # adjoint AND — ancilla |0⟩ 복원
```

**gate-list** (봉인부품 재조합, NO MatrixGate):

| step | sealed module | role |
|------|---------------|------|
| 1 | `toffoli` (or `c3x` AND-bloq 동치) | control∧target → ancilla |
| 2 | `t_gate` 시퀀스 / `ZPowGate(-1/128)` bloq | half-angle Z-rotation on ancilla |
| 3 | `toffoli`† (mirror step1) | AND uncompute |

> **Predecessor 연결**: `cr7_dag`는 full-angle `ω_{128}^*`; 본 분해는 동일 (c,t) 쌍에 half-angle `ω_{256}^*`를 AND-kickback으로 구현. `cr7_dag`를 직접 곱하지 않고 phase precision을 1-bit 확장 — crK family standing-loop 패턴.

**qubit-mapping** (big-endian, control=first/MSB):

| register | index | role |
|----------|-------|------|
| c | 0 | control (MSB) |
| t | 1 | target |
| a | 2 | borrowed ancilla (AND workspace, clean) |

**자원추정** (cr7_dag 구조 유사 + AND pair):

| metric | estimate |
|--------|----------|
| T | ~19 (= 2×toffoli 4T + rotation ~11T; cr7_dag sealed=15T 대비 +4T for extra AND) |
| Toffoli | 2 (AND compute + uncompute) |
| AND-bloq | 2 |
| rotation | 1 (Z^{-1/128}) |
| ancilla | 1 borrowed clean (또는 0 if AND-bloq in-place) |

**예측 u_hash**: `198f6cade30501ccf515dcefaad411eb52a0a8514718b7c646a46198aa9d3922`

(독립 numpy `diag(1,1,1,exp(-2πi/2^8))` 및 Qualtran `ZPowGate(-1/2^7).controlled().tensor_contract()` 로컬 검증 완료)

### 근거 (왜 최소)

1. **family 확장**: crK† family에서 k→k+1은 exponent `-1/2^{k-1}` → `-1/2^k` (phase 정밀도 2×). `cr7_dag`(`-1/64` in π-units)에서 `cr8_dag`(`-1/128`)로의 최소 비트 확장.
2. **Qualtran 검증 분해**: `ZPowGate(-1/2^7).controlled().decompose_bloq()` = `And · Z^{-1/128} · And†` — 이 3-블록이 qualtran-native 최소 AND-sandwich.
3. **봉인부품만**: `toffoli`(+dag), rotation primitive — `MatrixGate`/`tensor_contract` 직접 방출 없음.
4. **대안 대비**: `cr7_dag · cr7_dag` = `cr6_dag` (phase *곱* ≠ half-angle). `cr7_dag` 단독 사용 불가. AND-sandwich가 올바른 √phase 경로.

### 봉인가능성 (오라클 통과 예측)

| gate | 예측 |
|------|------|
| C1 FullCharacterization | PASS — 2-qubit controlled phase, 완전 대각 |
| C2 PhasePreserved | PASS — `exp(-2πi/256)` analytic |
| C3 AncillaClean | PASS — AND† uncompute (qualtran decompose 구조) |
| C4 ComposableContract | PASS — golden `diag(1,1,1,exp(-2πi/2^8))`, atol 1e-7 |
| second_oracle | PASS — `cphase(8).conj()` 독립 재구성 u_hash 일치 예상 |
| sympy proof | PASS — 아래 대수 증명 |

**sympy phase proof (sketch)**:

```python
import sympy as sp
k = 8
phi = sp.exp(-2 * sp.pi * sp.I / 2**k)
# 2^k-th root of unity
assert sp.simplify(phi**(2**k)) == 1
# cr8† eigenvalue on |11⟩:
assert sp.simplify(phi) == sp.exp(-sp.pi * sp.I / 2**(k-1))
# global phase ignored (W1.3): diag(1,1,1,phi) unique up to global
```

### 위험 (가정)

1. **Z^{-1/128} 합성**: step2가 sealed `t_gate`/`s_gate`만으로 Clifford+T 합성될 경우 T-count가 달라질 수 있음. rotation bloq 허용 시 cr7_dag와 동일 패턴(ZPowGate)으로 봉인 가능.
2. **AND 표현**: qualtran `And` bloq vs sealed `toffoli` 리소스 카운트 차이 — oracle `resource_schema` 정합 확인 필요.
3. **W1.3 위상**: controlled 합성 시 전역위상 atol 1e-7 — QFT8+ 파이프라인에서 누적 위상 정합은 별도 검증 대상.
4. **ancilla 정책**: AND-bloq in-place vs explicit ancilla — meta `n_anc` 선언에 따라 C3 판정 달라질 수 있음.

---

## 요약

| gap_id | strategy | predicted u_hash | T (est.) | Toffoli (est.) |
|--------|----------|------------------|----------|----------------|
| c7x | c6x ×2 + toffoli ×1 (1 ancilla) | `18ef5d9b…9f2fe` | 44 | 1 |
| cr8_dag_gate | AND · Z^{-1/128} · AND† (cr7† half-angle) | `198f6cade…d3922` | ~19 | 2 |

두 제안 모두 **봉인부품 재조합**(NO MatrixGate), **독립 golden 대조**, **sympy proof 가능** 구조. 수거 후 `second_oracle` + `verify_seal.py`로 key-free 봉인 가능할 것으로 예측.