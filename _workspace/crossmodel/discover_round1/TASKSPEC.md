# Discover Round 1 — Primitive Proposal TaskSpec (PG)

> 6런타임 패널 배포용. 각 런타임 독립 제안(상호 비참조). 정욱님 수거 후 봉인.
> 응답 형식: 제안(분해 회로) · 근거(왜 최소) · 봉인가능성(오라클 통과 예측) · 위험(가정).

## GAP: c7x — 7-control Toffoli (multi-controlled X)

```
AI_propose_decomposition // c7x 최소 분해 (needs-verify)
    # target: 7-control Toffoli (multi-controlled X)
    # golden: permutation: |c…c,t⟩ → |c…c, t⊕(c₁∧…∧c_n)⟩, big-endian 첫 레지스터=MSB
    # constraint: Clifford+T, ancilla 허용(borrowed/clean 명시), golden=permutation matrix
    # unlocks: distinct-prime modular-mult 확장 (mod 39=3×13, mod 51=3×17 …) — cmul prereq
    # output: gate-list(봉인부품 재조합, NO MatrixGate) + qubit-mapping + 자원추정(T/Toffoli)
    # acceptance: second_oracle 독립 numpy 재구성 u_hash 일치 + sympy permutation/phase proof
```

## GAP: cr8_dag_gate — controlled-phase R_k† = diag(1, e^{-2πi/2^8})

```
AI_propose_decomposition // cr8_dag_gate 최소 분해 (needs-verify)
    # target: controlled-phase R_k† = diag(1, e^{-2πi/2^8})
    # golden: diag(1,1,1,exp(2πi/2^k)), 전역위상 atol 1e-7 무시 — controlled 합성 시 W1.3 정합 필요
    # constraint: analytic golden, deg=2^k root of unity, no MatrixGate
    # unlocks: 더 깊은 QFT/IQFT (qft8+) — exponent precision 확장
    # output: gate-list(봉인부품 재조합, NO MatrixGate) + qubit-mapping + 자원추정(T/Toffoli)
    # acceptance: second_oracle 독립 numpy 재구성 u_hash 일치 + sympy permutation/phase proof
```

