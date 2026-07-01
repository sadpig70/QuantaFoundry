<!-- 외부 런타임 대상: QuantaFoundry 의 *수평적 확장* 아이디어 제안 요청.
     이미 구현·봉인된 것은 §3 EXCLUDE 카탈로그에 있으니 재제안 금지. 정체성·제약을 지키는
     *새로운 수평 축*을 제안하라. 이 문서 하나만으로 판단 가능하도록 프로젝트 핵심을 자기완결로 담았다. -->
# QuantaFoundry — 수평적 확장(Horizontal Expansion) 아이디어 제안 요청

**당신의 역할**: AI-native 양자 소프트웨어 파운드리의 **다음 수평 확장 축**을 제안하는 외부 설계자.
칭찬이 아니라 **새롭고 실현 가능한 방향**을 원한다. §3의 이미 구현된 목록은 **재제안 금지**.

---

## 1. 프로젝트 정체성 (제안의 유효성을 규정 — 먼저 읽어라)

QuantaFoundry 는 **미래의 완전한 결함허용 양자컴퓨터(FTQC/QPC)가 왔을 때 그대로 신뢰하고 쓸
소프트웨어를 *지금 미리* 축적**하는 프로젝트다. 모든 산출물(artifact)은 **이상적·무잡음(noiseless)
수학적 진실**(정확한 유니터리, 또는 대형 회로에 대한 구조적 Merkle)을 **결정론적 오라클**로 검증하고,
통과한 것만 **봉인(seal)**된다.

- **하드웨어는 영구적으로 범위 밖.** 현재의 잡음 있는 NISQ 장치에서 돌리는 것은 이 프로젝트에서
  의미가 없다. **"실제 QPU에서 돌려라" / "노이즈 모델을 넣어라" 류 제안은 무효.**
- **봉인 = 영구 계약.** 하드웨어로 사후 검증할 수 없으므로, **봉인 시점의 수학적 검증 강도와 독립성이
  신뢰의 전부**다. 그래서 검증 가능성이 제안의 핵심 잣대다.
- **AI가 생성하고, 결정론적 오라클이 판정한다.** 어떤 AI도 자기 출력을 스스로 합격시키지 못한다
  (self-judge 금지). 합격/불합격은 실행 가능한 기계 게이트만 결정한다.

---

## 2. "수평적(Horizontal)" 확장의 정의

- **수직(vertical) 확장 = 벽.** 더 큰 밀집(dense) 회로(예: 14-큐빗 dense primitive)는 밀집행렬
  메모리 한계로 막혀 있다. 이는 **의도된·정직한 경계**이며 목표가 아니다.
- **수평 확장 = 추상화 계층을 넓히는 것.** 큐빗 수가 아니라 **새로운 알고리즘 클래스·추상화·표현**을
  더한다(작은 *정확한* 인스턴스, 더 높은 추상화). 예: 기존에 순열→block-encoding→QSVT→fermionic 으로
  계층을 올려 왔다. 우리가 원하는 것은 **이 축에서의 새로운 방향**이다.

우선순위 잣대(높을수록 선호):
1. **오라클로 검증 가능**한가 — 특히 작은 인스턴스를 **Tier-0 EXACT**(정확한 유니터리)로 봉인 가능한가.
2. **compounding** — 하나의 봉인이 여러 알고리즘/응용을 낳는가("one seal, many algorithms").
3. **미래 FTQC/QPC 정체성 부합** — 완전 환경에서 실제로 쓸 자산인가.
4. **honest decomposition** — 봉인 게이트의 실제 회로 분해로 조립 가능한가(정답을 행렬로 심는 shortcut 아님).

---

## 3. EXCLUDE — 이미 구현·봉인된 것 (재제안 금지)

현재 **77 modules / 180 sealed apps** (root `a177da0c…`). 카테고리:

- **기초 상태/게이트**: Bell, GHZ(최대 GHZ-16 부분검증·GHZ-9 encoder), cluster/ring/W-state, 표준
  1·2·다중제어 게이트(X/Z/H/S/T/√X, CNOT/CZ/Toffoli/Fredkin/iSWAP, c3x…c12x 다중제어), 회전/위상
  게이트(Rz/Rx/Ry 특정각·controlled-Rk).
- **QFT 계열**: QFT(2–8)·역QFT·QPE·amplitude estimation(QAE).
- **검색/증폭**: Grover·diffusion·reflection·amplitude amplification.
- **Hamiltonian 시뮬레이션**: TFIM/Heisenberg Trotter·2차 Suzuki·4차 Yoshida-Suzuki·Pauli-지수 회전
  (rxx/ryy/rzz). (근사오차는 관측이며 봉인 아님.)
- **변분**: VQE(hardware-efficient ansatz, 다층)·QAOA(MaxCut)·parameter-shift gradient(관측).
- **쿼리 알고리즘**: Deutsch-Jozsa·Bernstein-Vazirani·Simon·quantum walk(C4/C8).
- **양자오류정정(QEC)**: repetition code(bit/phase)·syndrome·Shor-9 encoder·Steane/stabilizer-tableau
  (Tier-2 Clifford)·**transversal 논리 Clifford 게이트(H/S/CNOT)**. ※ **Clifford 계층까지만**.
- **Shor 인수분해**: 15=3×5·**진짜 21=3×7**·distinct-prime structural frontier(shor69…shor3683,
  c8x→c12x 다중제어 사다리)·modular multiplier(cmul) 계열·**부분공간 순열 강검증**(계산기저 정수산술).
- **QSVT / block-encoding 프레임워크 (완비)**: LCU block-encoding(be_xz/be_proj/be_pauli2 2q/be_num/
  be_hop·be_hopz), QSP(degree 1/3/5), QSVT 다항식 변환(projector family·2q Pauli), **consumer trilogy —
  Hamiltonian simulation(Chebyshev/Jacobi-Anger)·amplitude amplification·matrix inversion(linear systems)**.
- **Fermionic 시뮬레이션(Jordan-Wigner)**: 반교환관계 정확 검증·hopping·number operator·**완전 t-V 및
  정통 spinful Fermi-Hubbard 모델**(Mott 물리 관측·JW Z-string block-encoding).
- **발견 자율화**: decomposition superoptimization(봉인 팔레트로 더 짧은/새 분해 자동 탐색, 오라클 하드게이트).
- **채택/경화**: OpenQASM3 export/ingest·CLI·citable registry root·독립 2차 오라클·규약-독립성 감사·
  oracle revocation·ed25519 Sybil 방어·CI seal-gate.

**핵심: Clifford QEC·QSVT·JW-fermionic·Shor·변분·검색·QFT 계열은 이미 있다. 이것들의 사소한 변형(다른
파라미터·더 큰 인스턴스)은 원하지 않는다. 질적으로 새로운 축을 제안하라.**

---

## 4. 우리가 원하는 것

정체성·제약(§1, §5)을 지키면서, **§3에 없는 새로운 수평 축**. 가능하면 작은 인스턴스가 Tier-0 EXACT 로
봉인 가능하고 compounding 이 있는 것. 자유롭게 제안하되, 방향 감을 위한 예시(강요 아님, 이 중 아닌 것도 환영):

- **FTQC-native 상위 계층** — 우리는 Clifford 계층(QEC 인코더·transversal Clifford)까지만 있다.
  non-Clifford universality(magic state·T-gate injection·distillation)·lattice surgery·논리 알고리즘·
  color/surface code 논리 연산 등은 **미구현**.
- **대체 fermionic 인코딩** — Bravyi-Kitaev·parity·Verstraete-Cirac 등(우리는 Jordan-Wigner 만).
- **양자화학 실제 분자** — 실제 Hamiltonian(H₂ 등)·오비탈·point-group 대칭.
- 그 밖에: 새로운 대수적 구조(bosonic/qudit)·tensor-network 상태·양자 계측/센싱 프로토콜·
  새로운 검증 *방법*(ZX-calculus Tier-3·symbolic proof) 등 — **당신이 더 나은 축을 알면 그것을 제안하라.**

---

## 5. 반드시 지켜야 할 제약

- **결정론 불가침** — byte-identical 재봉인. 동결된 합의 키·오라클 지문 파일은 재생성/수정 금지.
- **오라클은 사용만** — 검증기(`verify_seal.py`/`contracts.py`)는 재구현하지 않는다(해시가 봉인에 baked).
- **honest decomposition** — `MatrixGate`/정답-행렬 shortcut 금지. 실제 회로 분해로 조립.
- **self-contained** — 벤더된 오라클 외의 외부 서비스/스킬 의존 금지.
- **하드웨어 out** — QPU/노이즈/실행-증거 축은 제안 대상 아님.
- **정직 경계** — 근사(다항식/Trotter)는 봉인이 아니라 관측(observation)으로 명시. exact ≠ 근사, dense ≠
  structural ≠ subspace, 결정론 재현 ≠ 정확성.

---

## 6. 답변 형식 (제안마다)

각 제안을 다음 형식으로. **3~5개**를 impact×feasibility 순으로:

1. **proposal** — 새 수평 축 한 줄 + 무엇을 봉인할지(구체적 작은 인스턴스).
2. **rationale** — 왜 지금 이 프로젝트에 가치 있는가(정체성 부합·compounding).
3. **feasibility** — 작은 인스턴스가 **Tier-0 EXACT 봉인 가능한가**? 어떤 봉인 게이트로 조립되나?
   오라클로 무엇을 검증하나? (검증 불가면 왜, 대안 검증은?)
4. **risk** — 실패 모드·정직 경계(무엇이 근사/관측이고 무엇이 exact 봉인인가).
5. **novelty** — §3 EXCLUDE 목록과 **명시적으로 대조**해 겹치지 않음을 확인.

---

## 7. 현황 파악용 문서 (레포에 있음, 필요 시 참고)

- `README.md` — 정체성·신뢰모델·현재 상태·one-command 검증·정직 경계.
- `.pgf/DESIGN-MasterRoadmap.md` — 실행 로드맵 척추(PG 표기; 노드 `(status)` = 구현/계획). **TrackV08 에
  최근 QSVT·fermionic 확장 상세**.
- `docs/QuantaFoundry-Technical-Spec.md` — 전체 명세 + 증거 + **한계(limitations)** + 버전 이력.
- `registry/REGISTRY-MANIFEST.json` — 권위 있는 현재 수치/root. `registry/SEMANTIC-GUARANTEES.json` — tier/
  보증 등급 분리(`headline_split`).
- 스스로 검증: `python scripts/reproduce_all.py` → `REPRODUCED · root a177da0c… · 77 modules / 180 apps ·
  second_oracle 71/71`.

## 8. 개념 미니 용어집

- **QPGF 오라클** — 결정론적 검사기. `verify_seal.py <spec.pg> --out <dir>` → `exit 0 ⟺ 봉인`. 차원(C1)·
  유니터리성/위상(C2)·ancilla/isometry(C3)·독립 참조와의 일치(C4)를 검사. **사용만, 재구현 금지.**
- **Seal Tier** — `0 EXACT`(dense, n≤12) · `1 STRUCTURAL`(Merkle, unitary 미보증) · `2 CLIFFORD`(tableau) ·
  `3 CLIFFORD+T`(ZX). 높은 tier 는 정확 동등성 대신 규모를 얻는다.
- **block-encoding / LCU / QSVT** — 행렬 A 를 더 큰 유니터리의 블록에 인코딩하고(⟨0|U|0⟩=A/α), 위상열로
  다항식 P(A) 를 유도. 하나의 봉인이 여러 알고리즘을 낳는 통합틀(우리가 이미 구현).
- **subspace 강검증** — 대형 순열 회로를 dense 없이 계산기저 정수산술로 exact 검증(Shor 자식에 적용).
