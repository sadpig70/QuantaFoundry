"""forge_apps.py — F3_Compose: 봉인된 베이스 모듈을 재조립해 상위 앱을 C-app 봉인.

봉인 누적의 복리(비선형 생산력) 실증: 이미 신뢰된 15개 모듈(specs/modules)을 plan 으로 합성하면
오라클(app_assemble, 사용만)이 합성품==app_golden(C-app) 대조 후 재봉인한다. 새 검증 비용은
'합성이 의도와 같은가'뿐 — 부품 정확성은 이미 지불됨(INV2).

재발견(rediscovery) 앱: cz·ccz·swap 을 *다른 모듈*의 조립으로 재구성 → 그 u_hash 가 독립적으로
cross-model 봉인된 게이트와 byte 일치함을 단언. 전체 스택(베이스 게이트 ⊕ 합성기 ⊕ 오라클)의 일관성 증명.

사용:  python .pgf/autoforge/forge_apps.py
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SCRIPTS = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, SCRIPTS)
import app_assemble as aa              # noqa: E402  (오라클 — 사용만)

APPS = os.path.join(ROOT, "specs", "apps")
STORE = os.path.join(ROOT, "registry", "apps")
MOD_REG = os.path.join(ROOT, "registry", "modules")

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
]


def _sealed_key(mid):
    p = os.path.join(MOD_REG, f"{mid}.sealed.json")
    return json.load(open(p, encoding="utf-8"))["u_hash"] if os.path.exists(p) else None


def main():
    os.makedirs(STORE, exist_ok=True)
    print("=" * 84)
    print("QuantaFoundry F3_Compose — 봉인 모듈 재조립 → C-app 봉인 (신뢰 자본 복리)")
    print("=" * 84)
    results, ok, redisc_ok = [], 0, 0
    for fname, redisc in APP_LIST:
        v = aa.assemble(os.path.join(APPS, fname), STORE)
        rec = {"app": fname[:-7], "sealed": v.sealed, "tier": v.tier,
               "u_hash": v.u_hash, "reason": v.reason, "rediscovers": redisc}
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
            icon = "✅"
            print(f"  {icon} {rec['app']:18} SEALED  tier={v.tier}  u_hash={v.u_hash[:14]}..{assertion}")
        else:
            print(f"  ❌ {rec['app']:18} REJECT  {v.reason[:50]}")
        results.append(rec)

    print("=" * 84)
    redisc_total = sum(1 for _, r in APP_LIST if r)
    print(f"앱 봉인 {ok}/{len(APP_LIST)} · 재발견 교차검증 {redisc_ok}/{redisc_total} 일치 · store=registry/apps")
    print("=" * 84)
    rep = os.path.join(HERE, "FORGE-APPS-RESULT.json")
    json.dump({"results": results, "sealed": ok, "total": len(APP_LIST),
               "rediscovery_ok": redisc_ok, "rediscovery_total": redisc_total},
              open(rep, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    all_ok = ok == len(APP_LIST) and redisc_ok == redisc_total
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
