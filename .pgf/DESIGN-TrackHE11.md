# DESIGN-TrackHE11 — report11 6축 (PGF full-cycle, 2026-07-09)

> report11 = 8런타임(`_workspace/ex-report11/agent01~08`). baseline: 95 modules / 466 apps / root 6e7d2a70 / 검증경로 10+제11후보.
> 전 축 관측/선검증(root 불변)·신규 module 0. crux-probe/좌표·필드 선검증 필수(v11 §4′j).

## 수렴 (8 agents)
| 축 | 제안 | 봉인경로 |
|---|---|---|
| P1 A₅ Fourier √5 | 01·02·03·04·05·08 (6) | Tier-0 dense 구성+검증(√5 gate 대기=관측) |
| P2 PSL(2,7) ambivalent 선검증 | 01·04·06·07·08 (5) | 관측(★A₅ 실수/PSL 허수 쌍) |
| P3 treewidth 제11경로 판정 | 01·02·04·05·06 제안 / 03·08 강등 | 판정(정직 자가강등 or 승격) |
| P4 Qutrit KS Yu-Oh 13 | 03·06·07 (3) | 관측(d=3 최소 KS) |
| P5 Kitaev class-D top.SC | 03·07·08 (3) | 관측(Pfaffian ℤ₂) |
| P6 Hecke H₃(q=i) Burau | 04·05·08 (3) | 관측(ℤ[i]⊂ℤ[ζ₈], gate 0) |
예비: full MTC(4)·Floquet SPT(3)·lattice surgery Tier-2 seal(4)·3D weak indices.

## Gantree
```
TrackHE11_report11
├─ P1_a5_fourier_sqrt5 (designing)       # A₅ DFT ∈ ℚ(√5) 구성·유니터리/orthogonality (√5 gate 대기)
│  ├─ build_a5_reps (atomic)             # 5 irrep(1,3,3,4,5) ℚ(√5) 행렬
│  ├─ dft_unitary (atomic)               # 블록대각 DFT·유니터리·convolution 정리
│  └─ witness a5_fourier_observe (atomic)
├─ P2_psl27_preverify (designing)        # ★ambivalent 판정 = A₅ 실수쌍의 허수쌍
│  ├─ build_PSL27 (atomic)               # SL(2,𝔽₇)/±I 168원소·6 켤레류(1/21/42/56/24/24)
│  ├─ ambivalent_test (atomic)           # order-7 g₇≁g₇⁶ (2 클래스 분열) → non-ambivalent
│  ├─ char_field (atomic)                # χ₃±(g₇)=(−1±i√7)/2 ∈ ℚ(√−7) 복소 필연
│  └─ witness psl27_observe (atomic)     # A₅(√5 실수)↔PSL27(√−7 허수) ambivalent 쌍
├─ P3_treewidth_verdict (designing)      # 진짜 제11 경로인가 자가강등인가 정직 판정
│  ├─ crux_tw_vs_tensornet (atomic)      # treewidth 부분수축 == tensor-net 값? 전제 겹침?
│  └─ witness treewidth_verdict (atomic) # 정직 판정(certificate layer 강등 or 승격 조건)
├─ P4_qutrit_ks13 (designing)            # Yu-Oh 13-ray d=3 KS
│  ├─ build_rays (atomic)                # ★좌표 자체 재검증(v11 교훈)·직교 그래프
│  ├─ coloring_infeasible (atomic)       # exhaustive 2^13 or α(G)<χ_p certificate
│  └─ witness ks13_qutrit_observe (atomic)
├─ P5_kitaev_class_d (designing)         # 1D Kitaev class-D ℤ₂ 위상초전도체
│  ├─ pfaffian_nu (atomic)               # (−1)^ν=sign(μ+2t)·sign(μ−2t) Pfaffian TRIM
│  ├─ dual_numeric (atomic)              # BdG eigenvector 수치 == 닫힌형
│  └─ witness kitaev_class_d_observe (atomic)
└─ P6_hecke_h3 (designing)               # H₃(q=i) Burau + Markov trace
   ├─ burau_rep (atomic)                 # g_i²=(i−1)g_i+i·Yang-Baxter·ℤ[i]
   ├─ markov_trace (atomic)              # braid closure → Jones(q=i)
   └─ witness hecke_h3_observe (atomic)
```

## PPR (acceptance_criteria 핵심)
```
def P1_a5_fourier_sqrt5:
  criteria: A₅ 5 irrep ℚ(√5)·블록대각 DFT 유니터리(F†F=I)·orthogonality·convolution 정리·
    ★봉인은 √5 gate 대기(관측=Fourier 구성+검증)·A₄ ζ₃ 복소 대조·teeth
def P2_psl27_preverify:
  criteria: PSL(2,7) 168·6 켤레류(1/21/42/56/24/24)·★order-7 2클래스 분열(g₇≁g₆⁻¹)=non-ambivalent·
    χ₃±=(−1±i√7)/2 ∈ ℚ(√−7) 복소 필연·문자표 orthogonality·Σdim²=168·A₅(√5)↔PSL(√−7) 쌍·좌표 자체유도
def P3_treewidth_verdict:
  criteria: 1D nearest-neighbor 회로 treewidth 부분수축 == dense 진폭 == tensor-net(제7)·
    ★전제 겹침 정직 판정: 값 검증=tensor-net 겹침→certificate layer 강등 or 그래프불변량만=별개
def P4_qutrit_ks13:
  criteria: Yu-Oh 13-ray ℂ³·★좌표 자체 재검증(내적 ℚ(√2))·직교그래프·exhaustive 2^13 coloring 불가·teeth
def P5_kitaev_class_d:
  criteria: Kitaev BdG class-D·(−1)^ν=sign(μ²−4t²) Pfaffian·위상상 |μ|<2t→ν=1(Majorana)·
    닫힌형==수치·gap-closing μ=±2t·2D Chern/3D ℤ₂와 AZ class 상이·teeth
def P6_hecke_h3:
  criteria: H₃(q=i) Burau 2×2 ∈ ℤ[i]·g_i²=(i−1)g_i+i·Yang-Baxter g₁g₂g₁=g₂g₁g₂·Markov trace·
    ★q=i∈ℤ[ζ₈] gate 0·Ising(k=2) 대수뼈대·teeth
```

## 실행순 & POLICY
- P2(showcase) → P1(최강, seal-prep) → P4(clean) → P5 → P6 → P3(정직 판정).
- 전 축 관측/선검증(root 불변 sidecar)·신규 module 0. 각 축 prototype 선검증→witness→test→reproduce→commit.
- 정직: 봉인 대기(√5/ζ₇ gate=사람게이트)·certificate layer 강등·좌표/필드 자체 재검증(v11 §4′j).
```
