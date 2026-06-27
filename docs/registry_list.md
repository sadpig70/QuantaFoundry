# Registry File List

확인 기준: `D:\QuantaFoundry`

## 요약

- 요청 경로 `.registry/`: 존재하지 않음
- 확인한 실제 경로: `registry/`
- 하위 폴더: 2개
- 파일 수: 54개
  - `registry/apps/`: 32개
  - `registry/modules/`: 22개

## 폴더 구조

```text
registry/
  apps/
  modules/
```

## registry/apps

`apps`는 여러 봉인 게이트/모듈을 조합해 만든 **앱 또는 앱 수준 회로의 봉인 결과**입니다. 각 `*.sealed.json`은 해당 앱의 전체 unitary가 app-golden 의도와 일치함을 `C1-C4(app)` 계약으로 검증한 증명 메타데이터이며, `u_hash`, `sig`, `tier`, `resource`, `oracle_code_hash` 등을 포함합니다. 예: `bell`, `ghz3`, `diffusion`, `qpe_s`, `shor15_a2`.

| No. | File | Size | 설명 |
|---:|---|---:|---|
| 1 | `registry/apps/bell.sealed.json` | 602 B | 2-qubit Bell state preparation. `H` on first qubit followed by `CNOT`; `|00>`을 `( |00> + |11> ) / sqrt(2)`로 보내는 entangling primitive. |
| 2 | `registry/apps/ccz_rediscovered.sealed.json` | 632 B | `CCZ`를 기존 sealed gate 조합으로 재발견한 app-level cross-check. 보통 `H`로 target basis를 바꾼 뒤 `Toffoli`를 적용하고 다시 `H`로 되돌리는 구조. |
| 3 | `registry/apps/cmul2_mod15.sealed.json` | 607 B | Shor용 controlled multiply-by-2 modulo 15. q0가 control이고 q1..q4 work register일 때, control=1이면 `y -> 2y mod 15`, `15`는 fixed point. |
| 4 | `registry/apps/cmul4_mod15.sealed.json` | 607 B | Shor용 controlled multiply-by-4 modulo 15. `cmul2_mod15` 두 번과 동등하며 work register를 2칸 cyclic rotation하는 permutation. |
| 5 | `registry/apps/cnot.sealed.json` | 584 B | app registry 쪽에도 등록된 기본 2-qubit `CNOT` gate. 첫 target/control이 1일 때 두 번째 target을 flip. |
| 6 | `registry/apps/cr3_dag_gate.sealed.json` | 645 B | inverse QFT 계열에서 쓰는 controlled phase gate. control=first, target에 `T†`에 해당하는 `R3†` phase를 조건부 적용. |
| 7 | `registry/apps/cr4_gate.sealed.json` | 649 B | QFT4 pipeline 보강용 controlled phase gate. control=first, target에 `R4 = exp(2πi/16)` phase를 조건부 적용. |
| 8 | `registry/apps/cs_dag.sealed.json` | 587 B | inverse QFT용 controlled-`S†` gate. control=first, target의 `|1>`에 `-i` phase를 조건부 적용. |
| 9 | `registry/apps/cs_gate.sealed.json` | 588 B | controlled-`S` gate. QFT/QPE phase ladder에서 사용되며, control=1 및 target=1일 때 `i` phase를 적용. |
| 10 | `registry/apps/ct_gate.sealed.json` | 588 B | controlled-`T` gate. QFT3/QPE-T에서 필요한 `exp(i*pi/4)` 조건부 phase. |
| 11 | `registry/apps/cz.sealed.json` | 582 B | app registry 쪽에도 등록된 기본 `CZ` gate. `|11>`에만 `-1` phase를 적용. |
| 12 | `registry/apps/cz_rediscovered.sealed.json` | 613 B | `CZ`를 `H + CNOT + H` 방식으로 재구성해 원래 `CZ`와 같은 unitary임을 확인한 rediscovery app. |
| 13 | `registry/apps/diffusion.sealed.json` | 607 B | 2-qubit Grover diffusion operator. `H⊗H`, `reflect00`, `H⊗H`로 uniform state에 대한 reflection을 구현. |
| 14 | `registry/apps/fredkin.sealed.json` | 584 B | app registry 쪽에도 등록된 3-qubit controlled-SWAP gate. Shor의 modular multiply rotation 구현에 사용. |
| 15 | `registry/apps/ghz16_structural.sealed.json` | 623 B | 16-qubit GHZ preparation을 dense matrix 없이 Tier-1 structural seal로 봉인한 large-N composition example. |
| 16 | `registry/apps/ghz3.sealed.json` | 602 B | 3-qubit GHZ preparation. `H(q0)` 뒤 `CNOT(0->1)`, `CNOT(1->2)`로 `|000>`을 `( |000> + |111> ) / sqrt(2)`로 보냄. |
| 17 | `registry/apps/ghz4.sealed.json` | 602 B | 4-qubit GHZ preparation. `H(q0)` 이후 CNOT chain으로 entanglement를 네 qubit에 전파. |
| 18 | `registry/apps/grover2.sealed.json` | 606 B | 2-qubit Grover single iterate. `|11>` marking oracle과 `diffusion`을 조합해 uniform superposition에서 marked state `|11>`을 증폭. |
| 19 | `registry/apps/h_gate.sealed.json` | 586 B | app registry 쪽에도 등록된 기본 single-qubit Hadamard gate. superposition 생성과 QFT/QPE/GHZ의 기본 building block. |
| 20 | `registry/apps/iqft2.sealed.json` | 623 B | raw 2-qubit QFT의 conjugate transpose. QPE-S의 counting register 후처리로 사용. |
| 21 | `registry/apps/iqft3.sealed.json` | 676 B | raw 3-qubit QFT의 conjugate transpose. QPE-T와 Shor period-finding의 counting register 후처리로 사용. |
| 22 | `registry/apps/qft2_pipeline.sealed.json` | 631 B | monolithic `qft2`를 `H`, controlled phase, `swap`류 pipeline으로 재구성한 app-level verification. |
| 23 | `registry/apps/qft3_pipeline.sealed.json` | 631 B | monolithic `qft3`를 `H`, controlled phase ladder, `swap` pipeline으로 재구성한 verification target. |
| 24 | `registry/apps/qft4_pipeline.sealed.json` | 672 B | 4-qubit raw QFT pipeline. `cr4_gate`까지 포함한 controlled phase ladder와 bit-order swap을 검증. |
| 25 | `registry/apps/qpe_s.sealed.json` | 623 B | 2-counting-qubit Quantum Phase Estimation for `S=diag(1,i)`. controlled powers와 `iqft2`로 phase `1/4`를 판독. |
| 26 | `registry/apps/qpe_t.sealed.json` | 676 B | 3-counting-qubit Quantum Phase Estimation for `T=diag(1,e^{i*pi/4})`. controlled `T^4/T^2/T`와 `iqft3`로 phase `1/8`을 판독. |
| 27 | `registry/apps/reflect00.sealed.json` | 607 B | `2|00><00| - I` reflection. `|00>`은 `+1`, 나머지 basis states는 `-1`; Grover diffusion의 하위 app. |
| 28 | `registry/apps/shor15_a2.sealed.json` | 696 B | Shor period-finding unitary for `N=15, a=2`. 3 counting qubits, 4 work qubits, controlled modular multiplication과 `iqft3`를 조합. |
| 29 | `registry/apps/swap_via_cnot.sealed.json` | 611 B | `SWAP`을 `CNOT` 조합으로 재발견한 app-level cross-check. sealed `swap2`와 같은 unitary인지 확인. |
| 30 | `registry/apps/swap2.sealed.json` | 585 B | app registry 쪽에도 등록된 기본 2-qubit `SWAP` gate. 두 qubit의 basis 위치를 교환. |
| 31 | `registry/apps/toffoli.sealed.json` | 586 B | app registry 쪽에도 등록된 3-qubit Toffoli/CCNOT gate. 두 control이 모두 1일 때 target flip. |
| 32 | `registry/apps/x_gate.sealed.json` | 586 B | app registry 쪽에도 등록된 기본 single-qubit Pauli-X gate. computational basis `|0>`과 `|1>`을 교환. |

## registry/modules

| No. | File | Size |
|---:|---|---:|
| 1 | `registry/modules/ccz.sealed.json` | 624 B |
| 2 | `registry/modules/cnot.sealed.json` | 584 B |
| 3 | `registry/modules/cr3_dag_gate.sealed.json` | 645 B |
| 4 | `registry/modules/cr4_dag_gate.sealed.json` | 653 B |
| 5 | `registry/modules/cr4_gate.sealed.json` | 649 B |
| 6 | `registry/modules/cr5_gate.sealed.json` | 649 B |
| 7 | `registry/modules/cs_dag.sealed.json` | 587 B |
| 8 | `registry/modules/cs_gate.sealed.json` | 588 B |
| 9 | `registry/modules/ct_gate.sealed.json` | 588 B |
| 10 | `registry/modules/cz.sealed.json` | 582 B |
| 11 | `registry/modules/fredkin.sealed.json` | 584 B |
| 12 | `registry/modules/h_gate.sealed.json` | 586 B |
| 13 | `registry/modules/iswap.sealed.json` | 585 B |
| 14 | `registry/modules/qft2.sealed.json` | 625 B |
| 15 | `registry/modules/qft3.sealed.json` | 638 B |
| 16 | `registry/modules/qft4.sealed.json` | 658 B |
| 17 | `registry/modules/s_gate.sealed.json` | 586 B |
| 18 | `registry/modules/swap2.sealed.json` | 585 B |
| 19 | `registry/modules/t_gate.sealed.json` | 579 B |
| 20 | `registry/modules/toffoli.sealed.json` | 586 B |
| 21 | `registry/modules/x_gate.sealed.json` | 586 B |
| 22 | `registry/modules/z_gate.sealed.json` | 586 B |
