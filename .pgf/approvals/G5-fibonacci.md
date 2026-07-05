# G5b 승인 요청 — Fibonacci anyon braid: 새 대수체 ℚ(ζ₅,√φ) 도입 + 신규 module 2개

> TrackGate6 G5 (계획서 `.pgf/DESIGN-HumanGate6.md` v1.1 · G5a 선검증 14항 ALL PASS 2026-07-05).
> **★트랙 최대 승인 게이트** — 판단 대상이 둘입니다:
> ① **새 대수체**: 등록부 수체(현재 dyadic·√2·√3·arccos√유리수·√41)에 **ℚ(ζ₅,√φ) — ℚ 위 차수 8
> 확장**(5차 단위근 + 황금비 제곱근) 추가. 등록부 대수 지평의 최대 확장입니다.
> ② **신규 module 2개**: `z5_gate = Z^(1/5) = ZPowGate(t=1/5)` · `ry_fib = Ry(2arccos φ⁻¹)`
> (계획서 한도 ≤3 이내). 봉인은 승인 후 G5c 에서만 — 본 시점 **봉인 0 · root 16422fcc 불변**.

---

## 1. 대상 물리 (닫힌형, 탐색 0)

Fibonacci anyon 3개의 fusion space = 2차원(1 qubit). Braid 군 B₃ 표현:

- **R**(교환 위상) = diag(e^{−4πi/5}, e^{3πi/5}) — fusion 채널 1/τ 별 topological spin.
- **F**(fusion 재결합) = [[φ⁻¹, φ^{−½}], [φ^{−½}, −φ⁻¹]], φ=(1+√5)/2 — **F²=I·F=F† 수치 확인**.
- 생성원: **σ₁ = R · σ₂ = F·R·F** (전부 정의식 직접 — 닫힌형).

수치 검증(ALL PASS, 기계정밀도):
- ★**Yang-Baxter**: σ₁σ₂σ₁ == σ₂σ₁σ₂ exact — braid 관계의 핵심.
- ★**B₃ 중심**: (σ₁σ₂)³ = e^{2πi/5}·I exact (위상 0.4π 정확, 리뷰 P5/P7 확정치 재현).
- **Euler 분해**(P7 재현): σ₂ = e^{−iπ/10}·Rz(−7π/5)·Ry(2arccos φ⁻¹)·Rz(−2π/5) exact.
- ★**비-Clifford witness**: 1q Clifford 24원소 대비 max |Tr(C†σ)|/2 = σ₁ 0.9877 · σ₂ 0.9715 (<1)
  — Fibonacci braid 는 Clifford 밖(위상적 보편성의 원천, 봉인 아닌 관측 예정).

## 2. 승인 대상 ① — field 공시 (축소 보고 금지 규율)

- σ₁·σ₂ 성분의 계수체 = **ℚ(ζ₅, √φ)**, ℚ 위 **차수 8** ([ℚ(ζ₅):ℚ]=4 × √φ 2차).
- ★√φ ∉ ℚ(√5): **N(φ) = φ·φ′ = −1 수치 확인**(φ′=(1−√5)/2) — norm 음수라 √φ 는 실 2차
  부분체에 없음 → ℚ(√5,ζ₅)(=ℚ(ζ₅), 차수 4)로는 부족, 진짜 차수 8 (P7 Critical 정정 그대로).
- module 별 캐리어 분담(합성 지평 최소화):
  - `z5_gate` 계수 {1, e^{iπ/5}}: **e^{iπ/5} = ζ₁₀ = −ζ₅³ ∈ ℚ(ζ₅)** — ★대칭 Rz 표현(ζ₂₀ 도입,
    차수 8 순환체) 대신 t_gate 선례의 ZPowGate 비대칭 표현을 채택해 **ζ₂₀ 를 봉인 계수에서 배제**.
    Euler 분해의 전역위상 e^{−iπ/10}(ζ₂₀)는 **C4 up-to-phase 규약으로 흡수**(봉인 계수에 미등장) — 판정 완료.
  - `ry_fib` 계수 {φ⁻¹, φ^{−½}}: **√φ 캐리어**, ℚ(√φ) 차수 4.
  - 두 module 합성(= braid 앱 골든)의 지평이 정확히 ℚ(ζ₅,√φ) 차수 8 — 그 이상 확장 없음.

## 3. 승인 대상 ② — 신규 module 명세

| module | 표현 | golden 계수 (π-free surd 가능) | 드라이런 u_hash 예보 |
|---|---|---|---|
| `z5_gate` | ZPowGate(exponent=1/5) | diag(1, (1+√5)/4 + i·√(10−2√5)/4) | `a60ac94b41b84ac4…` |
| `ry_fib` | YPowGate(exponent=2arccos(φ⁻¹)/π) | [[(√5−1)/2, −√((√5−1)/2)], [√((√5−1)/2), (√5−1)/2]] | `256147502bcb8da3…` |

- **seal_module 드라이런 2/2 성공**(C1-C4 통과·fingerprint 현행 일치·스크래치 store, registry 무접촉).
- ★**재발견 단언 예정**: (z5_gate)⁵ = z_gate — 수치 exact 확인(diag(1,−1)). 봉인 시 u_hash 일치 단언.
- ★surd 항등 확인: sin(arccos φ⁻¹) = φ^{−½} exact (φ²=φ+1 ⟹ 1−φ⁻² = φ⁻¹) — ry_fib 의
  두 계수가 같은 √φ 하나로 닫힘.
- **second_oracle 제1원리 초안**(π-free, cos(π/5)=(1+√5)/4·sin(π/5)=√(10−2√5)/4 수치 확인):
  ```python
  "z5_gate": lambda: np.diag([1.0, (1 + np.sqrt(5)) / 4 + 1j * np.sqrt(10 - 2 * np.sqrt(5)) / 4]).astype(complex),
  "ry_fib": lambda: np.array(
      [[(np.sqrt(5) - 1) / 2, -np.sqrt((np.sqrt(5) - 1) / 2)],
       [np.sqrt((np.sqrt(5) - 1) / 2), (np.sqrt(5) - 1) / 2]], dtype=complex),
  ```
  (A5 판정: ry_ak41 선례처럼 float-경유 대조 가능 — 기호 √5·√φ 구성이 위 초안 그대로.)

## 4. 소비처 (승인 후 G5c)

- `fib_braid_s1` = σ₁: plan = z5_gate⁷ (7스텝, up-to-phase). `fib_braid_s2` = σ₂: plan =
  [z, ry_fib]·z5⁷·[z, ry_fib] (11스텝, **F = ry_fib·z_gate 수치 확인**) — ★plan==σ up-to-phase
  exact 선검증 완료. 두 앱 전부 신규 module 은 위 2개뿐.
- `fib_braid_observe`(신규, 기존 braid_observe=Ising 불변): Yang-Baxter exact · B₃ 중심
  (σ₁σ₂)³=e^{2πi/5}I(정의행렬 관측 — 전역위상은 seal 아닌 observe 소관) · 비-Clifford
  witness(stabilizer fidelity<1, magic_a 패턴) · teeth. **universality/근사 컴파일 주장 = 범위 밖**
  (정직 경계): 봉인=braid 생성원 유니터리 2개뿐.
- 의의: 위상적 양자컴퓨팅(Fibonacci=보편 anyon 모델)의 braid 생성원이 등록부 1급 자산화 —
  Ising braid(`ising_braid_b2`, Clifford 한계)와 달리 **첫 비-Clifford anyon braid**. FTQC 방향 정합.

## 5. 승인 요청 (1줄 가부)

> **새 대수체 ℚ(ζ₅,√φ)(차수 8) 도입 + module 2개(`z5_gate`·`ry_fib`) 봉인을 승인하십니까?**

- **승인 시**: module 2 봉인(+second_oracle 제1원리·(z5)⁵=z 재발견 단언) → G5c
  `fib_braid_s1/s2` 봉인 + `fib_braid_observe` → G6 종결 동기화로 TrackGate6 전체 폐합.
- **부결 시**: G5 (blocked)+사유 = 정당한 terminal — G6 @dep 충족, 동기화로 직행.

*선검증 산출물: 스크래치 `g5a_design.py` 14항 ALL PASS. 봉인 0 · root 16422fcc4319ea92 불변 ·
fingerprint/frozen 무접촉.*
