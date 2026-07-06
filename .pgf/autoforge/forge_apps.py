"""forge_apps.py — F3_Compose: 봉인된 베이스 모듈을 재조립해 상위 앱을 C-app 봉인.

봉인 누적의 복리(비선형 생산력) 실증: 이미 신뢰된 15개 모듈(specs/modules)을 plan 으로 합성하면
오라클(app_assemble, 사용만)이 합성품==app_golden(C-app) 대조 후 재봉인한다. 새 검증 비용은
'합성이 의도와 같은가'뿐 — 부품 정확성은 이미 지불됨(INV2).

재발견(rediscovery) 앱: cz·ccz·swap 을 *다른 모듈*의 조립으로 재구성 → 그 u_hash 가 독립적으로
cross-model 봉인된 게이트와 byte 일치함을 단언. 전체 스택(베이스 게이트 ⊕ 합성기 ⊕ 오라클)의 일관성 증명.

사용:  python .pgf/autoforge/forge_apps.py
"""
import os, sys, json, hashlib, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SCRIPTS = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, SCRIPTS)
import app_assemble as aa              # noqa: E402  (오라클 — 사용만)

APPS = os.path.join(ROOT, "specs", "apps")
STORE = os.path.join(ROOT, "registry", "apps")
MOD_REG = os.path.join(ROOT, "registry", "modules")
_ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")

# 앱 목록 (적용순) + 재발견 단언 대상(있으면 그 봉인 게이트와 u_hash 일치해야)
APP_LIST = [
    ("bell.app.pg",             None),
    ("ghz3.app.pg",             None),
    ("ghz4.app.pg",             None),
    ("ghz5.app.pg",             None),    # goal-autonomy 자율 생성 (family extension, human seed 0)
    ("ghz6.app.pg",             None),    # goal-autonomy 자율 생성 (compounding 실증)
    ("cz_rediscovered.app.pg",  "cz"),
    ("ccz_rediscovered.app.pg", "ccz"),
    ("swap_via_cnot.app.pg",    "swap2"),
    # F3 확장 (§5b): 재귀 sub-app 트리 · 실앱(Grover) · Tier-1 대규모
    ("reflect00.app.pg",         None),
    ("diffusion.app.pg",         None),   # reflect00 을 sub-app 재귀 참조
    ("grover2.app.pg",           None),   # 3레벨 트리: grover2→diffusion→reflect00, oracle=재사용 cz
    ("ghz16_structural.app.pg",  None),   # Tier-1 Merkle, 16q dense 미실체화
    # F3 확장 (§5c): QFT pipeline — 첫 비자명 알고리즘 분해, cross-model 게이트 실투입
    ("qft2_pipeline.app.pg",     "qft2"),  # h·cs·swap → 봉인 qft2 재발견
    ("qft3_pipeline.app.pg",     "qft3"),  # h·cs·ct·swap → 봉인 qft3 재발견 (ct_gate 첫 사용)
    # F3 확장 (§5d): QPE — 최초 다중레지스터 실알고리즘
    ("iqft2.app.pg",             None),    # inverse QFT2 (cs_dag 투입), QPE 빌딩블록
    ("qpe_s.app.pg",             None),    # QPE(S): 2 counting+1 target, iqft2 sub-app 재귀
    # F3 확장 (§5e): controlled-Rk 일반화 → qft4 pipeline (16×16, cr4 첫 투입)
    ("qft4_pipeline.app.pg",     "qft4"),  # h·cs(CR2)·ct(CR3)·cr4(CR4)·swap → 봉인 qft4 재발견
    # F3 확장 (§5f): 큰 정밀도 QPE — t=3 counting, inverse-QFT3
    ("iqft3.app.pg",             None),    # inverse QFT3 (cr3_dag 투입), 큰 QPE 빌딩블록
    ("iqft7.app.pg",             None),    # inverse QFT7 (cr5/6/7_dag), Shor-21 counting register
    ("qpe_t.app.pg",             None),    # QPE(T) t=3: 고유위상 1/8=0.001₂, iqft3 sub-app 재귀
    # F3 확장 (§5g): Shor 주기발견 — modular mult를 sealed Fredkin으로 정직 분해
    ("cmul2_mod15.app.pg",       None),    # controlled ×2 mod15 = controlled 좌순환1 (Fredkin ×3)
    ("cmul4_mod15.app.pg",       None),    # controlled ×4 mod15 = cmul2 ∘ cmul2 (재귀)
    ("shor15_a2.app.pg",         None),    # 최초 완전 Shor(N=15,a=2): 7q, cmul·iqft3 재귀 트리
    # F3 확장 (§5l): Shor base 독립성 — a=7 (비-shift base). ×7=NOT∘rot3 정직 분해(CNOT 첫 modular-mult 투입)
    ("cmul7_mod15.app.pg",       None),    # controlled ×7 mod15 = NOT∘rot3 (Fredkin ×3 + CNOT ×4)
    ("shor15_a7.app.pg",         None),    # 완전 Shor(N=15,a=7): cmul4(재사용)·cmul7(신규)·iqft3, r=4 → 3×5
    # F3 확장 (§5l-2): N=21 진짜 modular arithmetic — N≠2^k-1 이라 carry/reduction 강제. reversible synth → c{3,4,5}x.
    ("cmul2_mod21.app.pg",       None),    # controlled ×2 mod21 (66 gates, {toffoli,c3x,c4x,c5x}) — Shor-21 U^1, 진짜 산술
    ("cmul4_mod21.app.pg",       None),    # controlled ×4 mod21 = cmul2² (복리 재사용)
    ("cmul16_mod21.app.pg",      None),    # controlled ×16 mod21 = cmul4² — Shor-21 controlled-U^{2^j} 패밀리
    # F3 확장 (§5q W7.1): QEC stabilizer 인코더 — 새 알고리즘 클래스(오류정정), 전부 Clifford Tier-0
    ("repcode3_bitflip.app.pg",   None),   # [[3,1]] bit-flip 인코더 (CNOT×2, golden=parity perm)
    ("repcode3_phaseflip.app.pg", None),   # [[3,1]] phase-flip 인코더 (+H×3, golden=H^⊗3@parity)
    ("shor9_encoder.app.pg",      None),   # [[9,1,3]] Shor 코드(1995) 인코더 9q 512×512 — QEC capstone
    ("syndrome3_bitflip.app.pg",  None),   # bit-flip 신드롬 추출(측정前 parity-copy unitary), 5q
    # F3 확장 (§5r W8.1): Hamiltonian simulation — Trotter, 새 수평 클래스(Pauli-exp 회전)
    ("rzz_pi8.app.pg",            None),   # e^{i(π/8)Z⊗Z} = CNOT·rz_negpi4·CNOT (2q ZZ 상호작용)
    ("tfim3_trotter_step.app.pg", None),   # TFIM n=3 1차 Trotter step (3q) — step EXACT 봉인(오차=관찰)
    # F3 확장 (§5s W8.2): TrotterDeepening — {rxx,ryy,rzz} 완성 + Heisenberg family + 복리
    ("rxx_pi8.app.pg",            None),   # e^{i(π/8)X⊗X} = (H⊗H)·rzz·(H⊗H) (2q XX 상호작용)
    ("ryy_pi8.app.pg",            None),   # e^{i(π/8)Y⊗Y}, 기저 B=S·H(Z→Y) (2q YY 상호작용)
    ("heis2_trotter_step.app.pg", None),   # single-bond Heisenberg step (2q) — 교환항 → 정확(관찰)
    ("heis3_trotter_step.app.pg", None),   # Heisenberg chain step (3q) — 비가환 → Trotter 오차(관찰)
    ("tfim3_trotter_2steps.app.pg", None), # TFIM Trotter step ×2 (복리, 3q) — step^k 합성=정확
    # F3 확장 (§5t W8.3): SuzukiTrotter — 2차 대칭 분할 + 4큐비트 격자 + 차수 대비
    ("rzz_pi16.app.pg",             None), # e^{i(π/16)Z⊗Z} = CNOT·rz_negpi8·CNOT (반각 ZZ, 2차용)
    ("tfim3_trotter_step2.app.pg",  None), # TFIM3 2차 Suzuki step (3q) — per-step O(dt³)
    ("tfim4_trotter_step.app.pg",   None), # TFIM4 1차 step (4q, 격자 확장)
    ("tfim4_trotter_step2.app.pg",  None), # TFIM4 2차 Suzuki step (4q)
    # F3 확장 (§5u W9.1): AmplitudeAmplification — Grover 일반화(3q 확산/연산자 + 반복)
    ("reflect000.app.pg",           None), # 2|000><000|-I = X³·CCZ·X³ (reflect00 3q 일반화)
    ("diffusion3.app.pg",           None), # 3q 확산 (H³·reflect000·H³ = 2|s><s|-I)
    ("grover3.app.pg",              None), # 3q Grover 1-iterate (D₃∘O₃, |111>) P=0.781
    ("grover3_2iter.app.pg",        None), # 3q Grover 2-iterate G₃² (N=8 최적-k) P=0.945
    ("grover2_2iter.app.pg",        None), # 2q Grover 2-iterate G₂² (N=4 over-rotation) P=0.25
    # F3 확장 (§5v W9.2): AmplitudeEstimation(QAE) — Grover Q 에 QPE → 진폭 추정
    ("cry_pi2.app.pg",              None), # controlled-Ry(π/2) (honest CNOT·Ry 사다리)
    ("cry_pi.app.pg",               None), # controlled-Ry(π)
    ("qae3_pi8.app.pg",             None), # QAE 4q: QPE on Grover Q → a=sin²(π/8) 추정 (iqft3 복리)
    # F3 확장 (§5w W9.3): QAEDeepening — 2nd QPE-QAE(a=1/2) + iterative QAE power(QPE-free)
    ("qae3_pi2.app.pg",             None), # QAE 4q: a=1/2 (Q=Ry(π), 신규 모듈 0)
    ("grover2_3iter.app.pg",        None), # G₂³ (iterative QAE power m=3)
    ("grover3_3iter.app.pg",        None), # G₃³
    ("vqe_he2_pi4.app.pg",          None), # VQE 2q 1-layer HE ansatz θ=π/4 (ry_pi4·cnot)
    ("vqe_he2_pi2.app.pg",          None), # VQE 2q θ=π/2 (ry_pi2·cnot)
    ("vqe_he2_3pi4.app.pg",         None), # VQE 2q θ=3π/4 (ry_3pi4·cnot)
    ("vqe_he3_pi4.app.pg",          None), # VQE 3q θ=π/4, CNOT ladder
    ("vqe_he2_L2_pi4.app.pg",       None), # W10.2 2-layer per-qubit ansatz 단일각 π/4
    ("vqe_he2_L2_mix.app.pg",       None), # W10.2 2-layer 혼합각 (ry_pi4/pi2/negpi4 복리)
    ("qaoa_p3.app.pg",              None), # W11.1 QAOA MaxCut path P3 (신규 모듈 0)
    ("qaoa_c4.app.pg",              None), # W11.1 QAOA MaxCut cycle C4
    ("dj2_const1.app.pg",            None), # W12.1 Deutsch-Jozsa n=2 constant f(x)=1
    ("dj2_balanced_xor.app.pg",      None), # W12.1 Deutsch-Jozsa n=2 balanced f(x)=x0 xor x1
    ("bv3_s101.app.pg",              None), # W12.1 Bernstein-Vazirani n=3 secret s=101
    ("simon2_s11.app.pg",            None), # W12.1 Simon n=2 hidden period s=11
    ("qw_c4_step.app.pg",            None), # W12.2 coined quantum walk on cycle C4, one step
    ("qw_c4_2steps.app.pg",          None), # W12.2 C4 walk two repeated steps
    ("qw_c8_step.app.pg",            None), # W12.2 coined quantum walk on cycle C8, one step
    ("qw_c8_3steps.app.pg",          None), # W12.2 C8 walk three repeated steps
    ("rzz_y4_p_half.app.pg",         None), # W12.3 Yoshida-4 half ZZ coefficient p
    ("rzz_y4_q_half.app.pg",         None), # W12.3 Yoshida-4 half ZZ coefficient q
    ("tfim3_suzuki4_step.app.pg",    None), # W12.3 TFIM3 4th-order Suzuki step
    ("tfim4_suzuki4_step.app.pg",    None), # W12.3 TFIM4 4th-order Suzuki step
    # HE H1 (#axis-A): Alternative fermionic encoding — Bravyi-Kitaev / parity
    ("bk4_transform.app.pg",         None), # H1.1 BK-2002 U_BK n=4 basis change (GF(2) permutation, cnot 조립)
    ("bk_num1.app.pg",               None), # H1.2 BK number n_1=(I-Z0Z1)/2 block-encoding (parity-set 구조)
    ("bk_hop01.app.pg",              None), # H1.2 BK hopping H_01=X0(I-Z1)/2 block-encoding
    ("parity4_transform.app.pg",     None), # H1.4 parity 인코딩 U_par n=4 (누적 parity permutation, cnot 조립)
    # HE H2 (#axis-B): Molecular Hamiltonian seal pack
    ("be_h2.app.pg",                 None), # H2.1 H₂ 부호구조 block-encoding (dyadic uniform LCU, (−I+XX+YY+ZZ)/4)
    # HE H4 (#axis-D): Generic data oracle — qROM / SELECT-PREPARE
    ("qrom22.app.pg",                None), # H4.1 qROM 2addr×2data table lookup (|i>|d>→|i>|d⊕data[i]>, x·toffoli)
    ("select_prepare4.app.pg",       None), # H4.2 generic SELECT-PREPARE LCU 템플릿 (전 4종 Pauli, block=(I+X+Y+Z)/4)
    # HE H3 (#axis-C): FTQC non-Clifford 심화 — magic state distillation
    ("code513_encoder.app.pg",       None), # H3.1 [[5,1,3]] 오각형 graph-code 인코더 (cnot·h·cz, 증류 Clifford 핵심)
    # HE H5 (#axis-E): 표현론 — 비아벨 유한군
    ("s3_mult.app.pg",               None), # H5.1 S₃ 곱셈 오라클 |g>|h>→|g>|gh> (반직접곱 닫힌형, cnot·fredkin·c3x·x)
    ("d4_mult.app.pg",               None), # H5.2′ D₄ 곱셈 오라클 (8원소=3q 정확, 5게이트 2-bit 가산기)
    ("d4_qft.app.pg",                None), # H5.2′ 첫 비아벨 군 Fourier: F_D4 = anti-CH∘(QFT_Z4⊗I), 위상 {±1,±i} 팔레트-exact
    # HE H6 (#axis-F): qudit — 큐트릿 qubit-임베딩(삼진 산술 계층만 exact, ω-위상 게이트)
    ("qutrit_x3.app.pg",             None), # H6.1′ 큐트릿 순환 증가 X₃ (+1 mod3, x·cnot, 임베딩)
    ("qutrit_sum.app.pg",            None), # H6.1′ 큐트릿 삼진 모듈러 가산기 (a+b mod3, c3x 켤레)
    # HE2 P1 (#TOPO): Surface code + lattice surgery (위상적 논리연산)
    ("surf422_encoder.app.pg",       None), # P1.1 [[4,2,2]] 최소 surface-type CSS 인코더 (Clifford, cnot·h)
    ("surf_ls_merge_zz.app.pg",      None), # P1.2 lattice surgery coherent Z_L⊗Z_L 병합 (9q, joint-parity block, h·cz)
    ("toric22_gs.app.pg",            None), # P1.3 2×2 토릭 ground state |00>_L 준비 (8q 위상질서, star-seed h·cnot)
    # HE2 P3 (#GF): 유한체 GF(2ᵏ) 산술 (특성-2 체 대수)
    ("gf4_mul.app.pg",               None), # P3.1 GF(4) 곱셈 |a,b,0>→|a,b,a·b> (toffoli 5, permutation)
    ("gf4_frob.app.pg",              None), # P3.2 GF(4) Frobenius x↦x² (cnot 1, 갈루아 Z₂)
    ("gf8_mulx.app.pg",              None), # P3.2 GF(8) 생성원 곱 a↦a·x (LFSR cnot 5, primitive 7-cycle)
    # HE2 P4 (#ANYON): Ising/Majorana 브레이드 (위상적 양자계산)
    ("ising_braid_b2.app.pg",        None), # P4.1 Majorana 브레이드 생성자 B₂ (entangling, h·sdg·cz)
    # HE2 P2 (#MBQC): 측정기반 양자계산 (cluster state + 측정패턴)
    ("cluster3x3_prep.app.pg",       None), # P2.1 2D 3×3 cluster graph state (9q, h·cz 12간선)
    ("mbqc_h.app.pg",                None), # P2.2 MBQC H 텔레포트 coherent (2q, cz·h·cnot)
    # HE2 P5 (#QCA): 양자 셀룰러 오토마타 (discrete-time exact dynamics)
    ("qca_step.app.pg",              None), # P5.1 Clifford QCA 1-step brickwork (4q, cz·h, 병진불변)
    ("fswap.app.pg",                 None), # P6 fermionic SWAP (Verstraete-Cirac primitive, swap2·cz)
    # HE2 v3 (사람게이트 승인): T2 Z₂ gauge · T1 Schur · T4 qLDPC
    ("z2gauge3.app.pg",              None), # T2.1 Z₂ 격자게이지 gauge-invariant encoder (cnot·h, Gauss law)
    ("qldpc_hgp.app.pg",             None), # T4 하이퍼그래프곱 CSS [[8,1,2]] 인코더 (generic 구성, h·cnot)
    ("schur3.app.pg",                None), # T1 3-qubit Schur-Weyl transform (CG cascade, ry_cg_half±·toffoli·CH)
    ("aklt4.app.pg",                 None), # V4 4-site AKLT VBS 준비 (순차 조건화 등척, ry_ak41/13/7±·ry_k5 복리)
    # HE2 V6 (#CHANNEL): 열린 양자계 — CPTP 채널 Stinespring dilation (1/2 감쇠점 dyadic, 신규 module 0)
    ("stinespring_bitflip.app.pg",   None), # V6 bit-flip p½ dilation (Ry(π/2)_e·CNOT(e→s))
    ("stinespring_phasedamp.app.pg", None), # V6 phase-damping λ½ dilation (CRY(π/2) s→e)
    ("stinespring_ampdamp.app.pg",   None), # V6 amplitude-damping γ½ dilation (CRY(π/2)·CNOT(e→s))
    ("stinespring_depol.app.pg",     None), # V6.2 fully depolarizing p=1 dilation (4-Kraus, H²·cnot·cz, 2q env)
    # HE2 V8 Unitary2Design: 1q Clifford 군 C1 전체 24원소(BFS words over {h,s}, mod phase) 봉인.
    #   각 앱=2×2 Tier-0 exact, plan=기봉인 h_gate/s_gate word(신규 module 0). 재발견 6건 단언.
    #   2/3-design 성질(frame potential F2=2·F3=5)=twodesign_observe 관측(seal 아님, INV-Q3).
    ("cliff1_id.app.pg",     None),      # C1 'I' X→+X Z→+Z (plan=h·h, H²=I exact)
    ("cliff1_h.app.pg",      "h_gate"),  # C1 'h' X→+Z Z→+X (== h_gate)
    ("cliff1_s.app.pg",      "s_gate"),  # C1 's' X→+Y Z→+Z (== s_gate)
    ("cliff1_hs.app.pg",     None),      # C1 'hs' X→+Z Z→+Y
    ("cliff1_sh.app.pg",     None),      # C1 'sh' X→-Y Z→+X
    ("cliff1_ss.app.pg",     "z_gate"),  # C1 'ss' X→-X Z→+Z (== z_gate)
    ("cliff1_hsh.app.pg",    "sx"),      # C1 'hsh' X→+X Z→-Y (== sx, HSH=√X exact)
    ("cliff1_hss.app.pg",    None),      # C1 'hss' X→+Z Z→-X
    ("cliff1_shs.app.pg",    None),      # C1 'shs' X→+X Z→+Y
    ("cliff1_ssh.app.pg",    None),      # C1 'ssh' X→-Z Z→+X
    ("cliff1_sss.app.pg",    "sdg_gate"),# C1 'sss' X→-Y Z→+Z (== sdg_gate)
    ("cliff1_hshs.app.pg",   None),      # C1 'hshs' X→+Y Z→+X
    ("cliff1_hssh.app.pg",   "x_gate"),  # C1 'hssh' X→+X Z→-Z (== x_gate, HZH=X exact)
    ("cliff1_hsss.app.pg",   None),      # C1 'hsss' X→+Z Z→-Y
    ("cliff1_shss.app.pg",   None),      # C1 'shss' X→+Y Z→-X
    ("cliff1_sshs.app.pg",   None),      # C1 'sshs' X→-Z Z→+Y
    ("cliff1_hshss.app.pg",  None),      # C1 'hshss' X→-X Z→+Y
    ("cliff1_hsshs.app.pg",  None),      # C1 'hsshs' X→+Y Z→-Z
    ("cliff1_shssh.app.pg",  None),      # C1 'shssh' X→-Y Z→-Z
    ("cliff1_shsss.app.pg",  None),      # C1 'shsss' X→-X Z→-Y
    ("cliff1_sshss.app.pg",  None),      # C1 'sshss' X→-Z Z→-X
    ("cliff1_hshssh.app.pg", None),      # C1 'hshssh' X→-Z Z→-Y
    ("cliff1_hshsss.app.pg", None),      # C1 'hshsss' X→-Y Z→-X
    ("cliff1_hsshss.app.pg", None),      # C1 'hsshss' X→-X Z→-Z (mod phase = Y)
    # HE3 H3.1 QuantumArithmetic: 명시적 정수 산술 1급 자산화 (외부 8런타임 8/8 만장일치 축, 신규 module 0)
    ("cuccaro_add2.app.pg",  None),      # 2-bit ripple-carry 가산기 (MAJ/UMA, {cnot,toffoli}, 6q)
    ("cuccaro_add3.app.pg",  None),      # 3-bit ripple-carry 가산기 (family 수직 1단, 8q)
    ("cmp2_ge.app.pg",       None),      # 2-bit 비교기 z^=[a>=b+cin] (보수 carry 트릭, MAJ† 역사다리, 6q)
    ("draper_add2.app.pg",   None),      # 2-bit Draper QFT-가산기 (위상공간 가산, qft2·cs·cz·iqft2 복리, 4q)
    # HE3 H3.2 SzegedyWalk: Markov 연쇄 양자화 — 새 수평 클래스 (6/8 합의, 이분 반사, 신규 module 0)
    ("szegedy_2state_p12.app.pg", None), # 2-state 균일 P=1/2 walk (W=X⊗X 로 닫힘, 반사 구성 plan, 2q)
    ("szegedy_c4_p12.app.pg",     None), # C₄ cycle 균일 walk (★draper_add2·reflect00 sub-app 복리, 4q 30스텝)
    # HE3 H3.3 ChoiState: channel-state duality 자산화 (채널축 잔여 novelty, Bell+dilation 복리, 신규 module 0)
    ("choi_bitflip.app.pg",   None),     # J(bit-flip½) 준비 유니터리 (3q, Bell+stinespring_bitflip sub-app)
    ("choi_phasedamp.app.pg", None),     # J(phase-damp½) 준비 유니터리 (3q)
    ("choi_ampdamp.app.pg",   None),     # J(amp-damp½) 준비 유니터리 (3q)
    ("choi_depol.app.pg",     None),     # J(depol p=1)=I/4 극단 사례 (4q, env 2q)
    # TrackGate6 G1: 2×2 RVB PEPS — 2D 텐서망 새 수평 클래스 (순차 조건화 등척 33스텝, 신규 module 0)
    ("peps22_rvb.app.pg",     None),     # |cov_H⟩+|cov_V⟩ dimer 중첩, ry_k5/k6 가법·parity·부호층 Z/CZ
    # TrackGate6 G2b: d=4 MUB-20 projective state 2-design — G2a closed-negative 반증의 대체 payoff
    #   (unitary 2-design 아님 — 용어 정직). 5기저×4상태, 전부 기봉인 x/h/s/cz Clifford word(신규 module 0).
    #   기저: b1=Z⊗Z · b2=H⊗H · b3=(SH)⊗(SH) · b4=CZ·(H⊗SH){XZ,ZY} · b5=CZ·(SH⊗H){YZ,ZX} (닫힌형, 탐색 0)
    ("mub4_b1_s0.app.pg",     None),     ("mub4_b1_s1.app.pg",     None),
    ("mub4_b1_s2.app.pg",     None),     ("mub4_b1_s3.app.pg",     None),
    ("mub4_b2_s0.app.pg",     None),     ("mub4_b2_s1.app.pg",     None),
    ("mub4_b2_s2.app.pg",     None),     ("mub4_b2_s3.app.pg",     None),
    ("mub4_b3_s0.app.pg",     None),     ("mub4_b3_s1.app.pg",     None),
    ("mub4_b3_s2.app.pg",     None),     ("mub4_b3_s3.app.pg",     None),
    ("mub4_b4_s0.app.pg",     None),     ("mub4_b4_s1.app.pg",     None),
    ("mub4_b4_s2.app.pg",     None),     ("mub4_b4_s3.app.pg",     None),
    ("mub4_b5_s0.app.pg",     None),     ("mub4_b5_s1.app.pg",     None),
    ("mub4_b5_s2.app.pg",     None),     ("mub4_b5_s3.app.pg",     None),
    # TrackGate6 G3c/d/e: π/6·π/3 family 소비 (승인 module ry_pi6/ry_negpi6 — .pgf/approvals/G3-ry_pi6.md)
    ("stinespring_bitflip_g14.app.pg",   None),  # bit-flip p=¼ dilation (Ry(π/3)=ry_pi6², 첫 비-dyadic 채널)
    ("stinespring_phasedamp_g14.app.pg", None),  # phase-damp λ=¼ (CRY(π/3) 반각 ry_pi6±)
    ("stinespring_ampdamp_g14.app.pg",   None),  # amp-damp γ=¼ (CRY(π/3)·CNOT)
    ("szegedy_2state_p14.app.pg",        None),  # Szegedy P=[[¼,¾],[¼,¾]] (Ry(2π/3)=ry_pi2·ry_pi6, 비대칭 첫 연쇄)
    ("naimark_ud3.app.pg",               None),  # UD-POVM Naimark 정방 완성 (rank-1 Kraus, module 0, W 간섭층)
    # TrackGate6 G4: n=4 Schur-Weyl — ★schur3 sub-app 복리 + CG 반각 {π/6,π/4,π/3} 전부 기봉인(module 0)
    ("schur4.app.pg",                    None),  # 16×16 = spin-2 ⊕ spin-1×3 ⊕ spin-0×2 (S₄ [4]/[3,1]/[2,2])
    # TrackGate6 G5: Fibonacci anyon braid — 새 대수체 ℚ(ζ₅,√φ) 승인분(z5_gate·ry_fib), 첫 비-Clifford braid
    ("fib_braid_s1.app.pg",              None),  # σ₁ = R (z5⁷, up-to-phase)
    ("fib_braid_s2.app.pg",              None),  # σ₂ = F·R·F (F=ry_fib·z, 11스텝)
    # TrackR3Residue C7: FT 증후 추출 프리미티브 — 1-flag weight-4 stabilizer ([[4,2,2]] 쌍, 신규 module 0)
    ("flag_synd_zzzz.app.pg",            None),  # S_Z=ZZZZ 1-flag coherent 추출 (6q, h/cnot)
    ("flag_synd_xxxx.app.pg",            None),  # S_X=XXXX (H⊗4 켤레) — [[4,2,2]] stabilizer 쌍 완성
    # TrackR3Residue C8: D₄ HSP 1-shot coset 회로 — ★d4_mult·d4_qft 이중 sub-app 복리 (신규 module 0)
    ("d4_hsp_shot_s.app.pg",             None),  # H={e,s} 비정규 (ρ 가중 ½ — 격자문제 연결 사례)
    ("d4_hsp_shot_r2.app.pg",            None),  # H={e,r²} 정규 (1차원 균등 — 구별 짝)
    # TrackR3Residue C6: GF(8) 체 연산 완결 — 역원(첫 비선형)·Frobenius (신규 module 0)
    ("gf8_inv.app.pg",                   None),  # a↦a⁻¹=a⁶ (0↦0), MMD 6게이트(toffoli3·cnot3)
    ("gf8_frob.app.pg",                  None),  # a↦a² 자기동형 (GF(2)-선형 → cnot 2개, Gal≅Z₃)
    # TrackC3Hierarchy: Clifford 계층(3단계) 자체개창 — coherent gate teleportation 촉매 회로 (module 0)
    ("t_teleport.app.pg",                None),  # CS·CNOT: U(|ψ⟩⊗|A⟩)=(T|ψ⟩)⊗|A⟩ — T-촉매, U∈C₃∖C₂
    ("s_teleport.app.pg",                None),  # CZ·CNOT: U(|ψ⟩⊗|Y⟩)=(S|ψ⟩)⊗|Y⟩ — 사다리 짝, U∈C₂
    # TrackHE4 P1: Fibonacci 소비층 (report4 6/8 합의) — F-move 독립 자산 + 매듭 braid word (module 0)
    ("fib_fmove.app.pg",                 None),  # F = ry_fib·z (융합트리 기저변환, F²=I, 1+φ=φ² 단위성)
    ("fib_hopf.app.pg",                  None),  # σ₁² — 폐포 = Hopf T(2,2)⊔O (s1 sub-app ×2)
    ("fib_trefoil.app.pg",               None),  # σ₁³ — 폐포 = 삼엽 T(2,3)⊔O (s1 sub-app ×3)
    ("fib_solomon.app.pg",               None),  # σ₁⁴ — 폐포 = Solomon T(2,4)⊔O (s1 sub-app ×4)
    ("fib_trefoil_m.app.pg",             None),  # σ₁³σ₂ — Markov 안정화판 삼엽 (s2 경로 최초 소비)
    # TrackHE4 P2: C₃ 대각 phase-polynomial 정규형 (report4 5/8 합의) — T/CS/CCZ 사전 (module 0)
    ("c3_diag_ladder3.app.pg",           None),  # f=x₀+2x₀x₁+4x₀x₁x₂ — 차수 1·2·3 사다리 각 1항
    ("c3_diag_full3.app.pg",             None),  # f=Σxᵢ+2Σxᵢxⱼ+4x₀x₁x₂ — 전 계수 1 정준형 (7스텝)
]


def _sealed_key(mid):
    p = os.path.join(MOD_REG, f"{mid}.sealed.json")
    return json.load(open(p, encoding="utf-8"))["u_hash"] if os.path.exists(p) else None


def _sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest() if os.path.exists(path) else None


def _changed_specs():
    """git 기준 변경된 app/module spec 파일명 집합(추적 변경 + untracked). git 부재 시 None(→full)."""
    try:
        out = subprocess.run(["git", "-C", ROOT, "status", "--porcelain",
                              "--", "specs/apps", "specs/modules"],
                             capture_output=True, text=True, timeout=30)
        if out.returncode != 0:
            return None
    except Exception:
        return None
    changed = set()
    for line in out.stdout.splitlines():
        # porcelain: 'XY path' — path 는 3열부터
        path = line[3:].strip().strip('"')
        if path.endswith((".app.pg", ".pg")):
            changed.add(os.path.basename(path))
    return changed


def _coherence_ok(app_id, redisc):
    """저비용 coherence(재조립 없이): sealed.json 존재 + fingerprint(oracle/contracts) 현재값 일치
    + redisc 앱은 u_hash==타겟 module 일치. spec 무변경일 때만 호출(결정론: 동일 spec+동일 oracle→동일 seal)."""
    p = os.path.join(STORE, f"{app_id}.sealed.json")
    if not os.path.exists(p):
        return False, None
    d = json.load(open(p, encoding="utf-8"))
    cur_oracle = _sha256(os.path.join(_ORACLE, "verify_seal.py"))
    cur_contracts = _sha256(os.path.join(_ORACLE, "contracts.py"))
    if d.get("oracle_code_hash") != cur_oracle or d.get("contracts_code_hash") != cur_contracts:
        return False, d.get("u_hash")   # 오라클 변경 → 재조립 필요
    if redisc and d.get("u_hash") != _sealed_key(redisc):
        return False, d.get("u_hash")
    return True, d.get("u_hash")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    changed_only = "--changed-only" in argv
    os.makedirs(STORE, exist_ok=True)
    # changed-only: git 으로 변경된 spec 만 재조립. spec 무변경 앱은 저비용 coherence(fingerprint/redisc).
    #   결정론 기반: 동일 spec bytes + 동일 oracle fingerprint → 재조립은 동일 seal 을 산출(byte-identity).
    #   full(기본)은 전량 재조립(가장 강한 byte-identity 증명). 세션 종료/CI 는 full 권장.
    changed = _changed_specs() if changed_only else None
    if changed_only and changed is None:
        print("[changed-only] git 미가용 → full 재조립으로 폴백", flush=True)
        changed_only = False
    # 모듈 spec 이 하나라도 변경되면 전 앱이 영향 → full 강제(안전).
    mod_changed = bool(changed) and any(n.endswith(".pg") and not n.endswith(".app.pg") for n in changed)
    if changed_only and mod_changed:
        print("[changed-only] module spec 변경 감지 → full 재조립으로 폴백(전 앱 영향)", flush=True)
        changed_only = False
    mode = "changed-only" if changed_only else "full"
    print("=" * 84)
    print(f"QuantaFoundry F3_Compose — 봉인 모듈 재조립 → C-app 봉인 (신뢰 자본 복리) · mode={mode}")
    print("=" * 84)
    results, ok, redisc_ok, assembled, coherent = [], 0, 0, 0, 0
    for fname, redisc in APP_LIST:
        app_id = fname[:-7]
        do_assemble = True
        if changed_only and fname not in changed:
            coh, uh = _coherence_ok(app_id, redisc)
            if coh:
                do_assemble = False
                coherent += 1
                ok += 1
                if redisc:
                    redisc_ok += 1
                results.append({"app": app_id, "sealed": True, "u_hash": uh,
                                "rediscovers": redisc, "verified": "coherence"})
                continue
        assembled += 1
        v = aa.assemble(os.path.join(APPS, fname), STORE)
        rec = {"app": app_id, "sealed": v.sealed, "tier": v.tier,
               "u_hash": v.u_hash, "reason": v.reason, "rediscovers": redisc,
               "verified": "reassembled"}
        if v.sealed:
            ok += 1
            assertion = ""
            if redisc:
                want = _sealed_key(redisc)
                match = (v.u_hash == want)
                rec["rediscovery_match"] = match
                if match:
                    redisc_ok += 1
                assertion = f"  ⟺ {redisc}: {'✓일치' if match else '✗불일치!'}"
            print(f"  ✅ {app_id:18} SEALED  tier={v.tier}  u_hash={v.u_hash[:14]}..{assertion}")
        else:
            print(f"  ❌ {app_id:18} REJECT  {v.reason[:50]}")
        results.append(rec)

    print("=" * 84)
    redisc_total = sum(1 for _, r in APP_LIST if r)
    tail = f" · 재조립 {assembled} · coherence {coherent}" if changed_only else ""
    print(f"앱 봉인 {ok}/{len(APP_LIST)} · 재발견 교차검증 {redisc_ok}/{redisc_total} 일치 · store=registry/apps{tail}")
    print("=" * 84)
    # 정본 리포트는 full 모드만 기록(커밋 아티팩트 안정). changed-only 는 빠른 점검이라 정본 무변경.
    if not changed_only:
        rep = os.path.join(HERE, "FORGE-APPS-RESULT.json")
        json.dump({"results": results, "sealed": ok, "total": len(APP_LIST),
                   "rediscovery_ok": redisc_ok, "rediscovery_total": redisc_total},
                  open(rep, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    all_ok = ok == len(APP_LIST) and redisc_ok == redisc_total
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
