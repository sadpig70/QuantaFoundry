# G3b 승인 요청 — π/6·π/3 각도 family 신규 module 2개 (ry_pi6 · ry_negpi6)

> TrackGate6 G3 (계획서 `.pgf/DESIGN-HumanGate6.md` v1.1 · G3a 선검증 ALL PASS 2026-07-05).
> **승인 대상**: 신규 module **2개** — `ry_pi6 = Ry(π/6) = YPowGate(exponent=1/6)` ·
> `ry_negpi6 = Ry(−π/6) = YPowGate(exponent=−1/6)` (명명 규약 P8: π-분수 family 는 neg-접두).
> 봉인은 승인 후 G3c 사이클에서만 수행 — 본 보고서 시점 **봉인 0 · root b82d79eb 불변 ·
> fingerprint/frozen 무접촉**.

---

## 1. 각도 도출 (3축, numpy 선검증 ALL PASS)

| 축 | 필요 회전 | π/6 환원 (닫힌형, 탐색 0) | 판정 |
|---|---|---|---|
| ① 채널 γ=¼ (G3c) | bitflip p¼: env `Ry(π/3)` / phase·amp-damp: `CRY(π/3)` | θ=2arcsin√¼=**π/3**; `Ry(π/3)=ry_pi6²`(가법) · `CRY(π/3)=(I⊗Ry(π/6))·CNOT·(I⊗Ry(−π/6))·CNOT`(V6 반각 패턴, exact 1e-14) · 3채널 전부 Tr_env==Kraus γ¼ 선검증 통과 | **ry_pi6·ry_negpi6 로 완결** |
| ② Szegedy p=¼ (G3d) | coin prep `Ry(2π/3)` (amp²={¼,¾}) | `Ry(2π/3)=ry_pi6⁴`(가법, exact) — ry_pi6 만으로 닫힘 | **ry_pi6 로 완결** |
| ③ Naimark POVM (G3e) | UD-POVM {E₊,E₋,E?} Naimark 완성 | **π/6 불필요** — §3 판정 참조 | **승인 범위에서 제외** |

추가 소비처(승인 후 무료 payoff): **G4 Schur n=4** — CG 계수 √(3/4)의 Givens 반각
arccos√(3/4)=**π/6** → ry_pi6 재사용(G4a1 팔레트 환원의 마지막 조각, G4 신규 module 0 가능성 확정에 기여).

## 2. 신규성·field·오라클 처리 (승인 판단 재료)

- **팔레트 도달불가 witness**: 기존 Ry-각 9종(π/2·π/4·3π/4·arccos(⅓)/2·arccos√⅕·arccos√⅙·
  ak41/13/7 반각)의 ℤ-조합 3.9M개(비유리 |n|≤3 × π/4 격자 전체, mod 4π) 스캔 —
  최근접 편차 **3.27e-7 = 통계적 near-miss**(exact 관계라면 ~1e-15 여야; 표본밀도 기대값 ~3e-6 스케일).
  해석적으로도 π/6 은 π/4 격자 밖(π-유리 부분)이고 Niven 정리상 arccos√유리수 각은 π-무리 —
  **기존 팔레트로 exact 도달 불가, 신규 module 정당**.
- **field 공시**: cos(π/12)=(√6+√2)/4 · sin(π/12)=(√6−√2)/4 ∈ **ℚ(√2,√3)** — 등록부 기존
  수체 범위(√2=h/π/4 계열·√6=ry_k6 계열) 안. **새 대수체 도입 없음** (G5 ℚ(ζ₅,√φ)와 대조).
- **YPowGate 표현**: exponent=±1/6 (Ry(α)=YPowGate(α/π) up-to-phase, C4 규약 — ry_cg_half 선례 동일).
- **seal_module 드라이런 (A3 해소)**: 후보 spec 2개를 스크래치 store 로 실봉인 성공 —
  C1-C4 계약 통과, oracle fingerprint 현행 일치, **u_hash 예보**: ry_pi6 `9372e7370911c3a2…` ·
  ry_negpi6 `6cd2dc18b0917761…` (registry 무접촉; 승인 후 동일 spec 재봉인 시 byte-identical 예상).
- **second_oracle 제1원리 구성 초안** (π-free surd, 독립 경로 — 승인 후 G3c 에서 추가):
  ```python
  "ry_pi6": lambda: np.array(
      [[(np.sqrt(6)+np.sqrt(2))/4, -(np.sqrt(6)-np.sqrt(2))/4],
       [(np.sqrt(6)-np.sqrt(2))/4,  (np.sqrt(6)+np.sqrt(2))/4]], dtype=complex),
  "ry_negpi6": lambda: np.array(
      [[(np.sqrt(6)+np.sqrt(2))/4,  (np.sqrt(6)-np.sqrt(2))/4],
       [-(np.sqrt(6)-np.sqrt(2))/4, (np.sqrt(6)+np.sqrt(2))/4]], dtype=complex),
  ```
  (선검증: surd == cos/sin(π/12) 1e-15 일치 — spec golden 의 np.pi 경유와 독립.)

## 3. ★POVM 축 판정 (A6 가정 해소 — 승인 범위 축소)

리뷰(P7)의 canonical √E isometry 성분² **{2/3, 1/24, 1/8, 3/8} 정체를 해석 복원**:
UD-POVM 대상 상태 |ψ±⟩=Ry(±π/3)|0⟩ (overlap=cos(π/3)=½), IDP 3-outcome
E±=⅔|ψ∓^⊥⟩⟨ψ∓^⊥|·E?=⅔|0⟩⟨0| 의 **√E(canonical Kraus) 열 성분과 정확 일치**(numpy 재현 PASS).
→ canonical 경로는 확실히 π/6 격자 밖(arccos√(1/24) 류) — 리뷰 판정 정당.

★그러나 **Kraus 자유도(M_k=U_k√E_k)의 rank-1 선택** M±=√⅔|0⟩⟨ψ∓^⊥|·M?=√⅔|0⟩⟨0| 이
M†M==E 를 보존(검증 PASS)하면서 Naimark isometry V 열 진폭²을 **{2/3, 1/6, 1/2}** 로 환원:
- 분기 2/3 vs 1/3 = arccos√(2/3) = **기봉인 `ry_cg_half` 와 float-identical**(선검증 PASS)
- 잔여 1/2 분할 = dyadic(`ry_pi2`/`ry_pi4`) — 전부 기봉인.

**판정**: POVM 축은 π/6 family 밖 확정(리뷰 유지)이나, **별도 신규각도 불필요 — 기존 팔레트
(ry_cg_half + dyadic)로 재도출 완료**. G3e(naimark_ud3 정방 유니터리 완성)는 이 rank-1 구성으로
**신규 module 0 전망**으로 진행(정방 완성의 순차 조건화는 G3e numpy 선검증에서 확정,
실패 시에만 별도 보고). 본 승인의 범위는 ①②(+G4 재사용)뿐.

## 4. 승인 요청 (1줄 가부)

> **신규 module 2개 — `ry_pi6`(YPowGate t=1/6) · `ry_negpi6`(t=−1/6), field ℚ(√2,√3)
> (신규 대수체 없음) — 봉인을 승인하십니까?**

- **승인 시**: G3c(stinespring_*_g14 3앱+channel_observe 확장) → G3d(szegedy_2state_p14) →
  G3e(naimark_ud3, module 0 경로) 순차 봉인 + G4 Schur4 잠금 해제(hard-dep 해소).
- **부결 시**: G3 (blocked)+사유 기록 = 정당한 terminal(G6 @dep 충족), G4 는 π/6 을
  자체 승인 요청으로 승계(계획서 G4 주석).

*선검증 산출물: 스크래치 `g3a_derive.py` 17항 ALL PASS (본 보고서 수치의 재현 경로;
승인 후 G3c 사이클에서 관측 스크립트에 흡수). 봉인 0 · root b82d79eb24d14ee5 불변.*
