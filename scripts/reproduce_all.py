"""reproduce_all.py — one-command 전체 재현 검증 (외부 리뷰 R-F 대응).

외부 reviewer 가 한 번에 전 검증을 재현하도록 오케스트레이션한다. 경로 비하드코딩(스크립트 기준 상대경로).
구성: 모듈/앱 재봉인 + 재발견 교차검증 + 결정론 + 독립 2차검증 + 행동(인수분해) + registry manifest.

사용:  python scripts/reproduce_all.py                 # full: 전 앱 byte-identity 재합성(가장 강함, CI/세션종료)
      python scripts/reproduce_all.py --changed-only   # 변경 spec 만 재합성 + 나머지 coherence(무인 라운드용)
출력:  reports/REPRODUCE-RESULT.json

--changed-only (검증 계층화): forge_apps 를 changed-only 로 위임(변경 spec 재조립 + 무변경 앱 fingerprint
  coherence) · factory 는 --verify-regression(byte-identity) 대신 --reproduce(캐시 재봉인, 저비용) 유지 ·
  독립 오라클 게이트(second_oracle·perm_subspace·resource·convention)는 전부 그대로. full 대비 forge 95s→~0s.
  결정론 보증: 동일 spec bytes + 동일 oracle fingerprint → 재조립 동일 seal(byte-identity). full 은 세션종료 1회.
"""
import os, sys, json, subprocess, re

CHANGED_ONLY = "--changed-only" in sys.argv

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
REPORTS = os.path.join(ROOT, "reports")
os.makedirs(REPORTS, exist_ok=True)

FRONTIER_STEPS = [
    ("shor_frontier", "scripts/shor_frontier.py"),
    ("c8x_frontier", "scripts/c8x_frontier.py"),
    ("shor221_frontier", "scripts/shor221_frontier.py"),
    ("c9x_shor381_frontier", "scripts/c9x_shor381_frontier.py"),
    ("c10x_frontier", "scripts/c10x_frontier.py"),
    ("shor635_frontier", "scripts/shor635_frontier.py"),
    ("c11x_frontier", "scripts/c11x_frontier.py"),
    ("c11x_payoff_family", "scripts/c11x_payoff_family.py"),
    ("shor1285_frontier", "scripts/shor1285_frontier.py"),
    ("c12x_frontier", "scripts/c12x_frontier.py"),
    ("c12x_payoff_family", "scripts/c12x_payoff_family.py"),
    ("shor3683_frontier", "scripts/shor3683_frontier.py"),
]

# Data-driven factory reproduction (INV-F5): re-seals every N in FACTORY-FRONTIER.json
# byte-identically. Adding a new factory N needs no code change here.
FACTORY_STEP = ("frontier_factory", "scripts/frontier_factory.py")


def run(args, cwd=ROOT):
    p = subprocess.run(["python"] + args, cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


# ── changed-only 지원: frontier/factory 앱 coherence 스윕 ──────────────────────
import glob, hashlib   # noqa: E402

_APPREG = os.path.join(ROOT, "registry", "apps")
_SPECS_APPS = os.path.join(ROOT, "specs", "apps")
_ORACLE_DIR = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")

# forge_apps 가 관리하는 템플릿 앱(1단계 forge_apps --changed-only 담당)을 제외한 나머지=
# frontier/factory 앱. 이들의 spec 변경 여부만 별도 판정.
def _template_app_ids():
    sys.path.insert(0, os.path.join(ROOT, ".pgf", "autoforge"))
    import forge_apps as fa  # noqa: E402  (APP_LIST 참조만)
    return {fn[:-7] for fn, _ in fa.APP_LIST}


def _git_changed_specs():
    """git porcelain 으로 변경된 specs/apps·specs/modules 파일 basename 집합(추적변경+untracked)."""
    try:
        out = subprocess.run(["git", "-C", ROOT, "status", "--porcelain",
                              "--", "specs/apps", "specs/modules"],
                             capture_output=True, text=True, timeout=30)
        if out.returncode != 0:
            return None
    except Exception:
        return None
    return {os.path.basename(l[3:].strip().strip('"'))
            for l in out.stdout.splitlines() if l[3:].strip().endswith((".app.pg", ".pg"))}


def _factory_app_ids():
    """FACTORY-FRONTIER.json 의 sealed_N → 그 N 의 shor/cmul 앱 id 집합.
    이 앱들은 changed-only 에서 factory --reproduce(저비용 9s)가 담당하므로 legacy 판정·coherence 에서 제외."""
    db = os.path.join(ROOT, ".pgf", "arith", "FACTORY-FRONTIER.json")
    if not os.path.exists(db):
        return set()
    ids = set()
    for e in json.load(open(db, encoding="utf-8")).get("sealed_N", []):
        N = e["N"]
        ids.add(f"shor{N}")
        for mul in e.get("unique_powers", []):
            ids.add(f"cmul{mul}_mod{N}")
    return ids


def _frontier_specs_changed():
    """legacy frontier(=템플릿·factory 외) 앱 spec 또는 module spec 변경? git 부재 시 True(→full 폴백).
    factory 앱 spec 변경은 여기서 무시(factory --reproduce 가 저비용 담당)."""
    changed = _git_changed_specs()
    if changed is None:
        return True
    if any(n.endswith(".pg") and not n.endswith(".app.pg") for n in changed):
        return True                                  # module 변경 → 전 앱 영향
    tmpl = _template_app_ids()
    fac = _factory_app_ids()
    for n in changed:
        if n.endswith(".app.pg"):
            aid = n[:-7]
            if aid not in tmpl and aid not in fac:
                return True                          # legacy frontier 앱 spec 변경(드묾) → FRONTIER_STEPS
    return False


def _coherence_sweep_frontier():
    """무변경 frontier/factory 앱 sealed.json 을 재봉인 없이 coherence 검증:
    fingerprint(oracle/contracts_code_hash)==현재값 + u_hash 존재. 결정론 기반(동일 spec+동일 oracle→동일 seal)."""
    cur_oracle = hashlib.sha256(open(os.path.join(_ORACLE_DIR, "verify_seal.py"), "rb").read()).hexdigest()
    cur_contracts = hashlib.sha256(open(os.path.join(_ORACLE_DIR, "contracts.py"), "rb").read()).hexdigest()
    skip = _template_app_ids() | _factory_app_ids()  # 템플릿=forge_apps, factory=factory --reproduce 담당
    checked, bad = 0, []
    for p in glob.glob(os.path.join(_APPREG, "*.sealed.json")):
        app_id = os.path.basename(p)[:-len(".sealed.json")]
        if app_id in skip:
            continue
        try:
            d = json.load(open(p, encoding="utf-8"))
        except Exception:
            bad.append(app_id); continue
        if (d.get("oracle_code_hash") != cur_oracle or d.get("contracts_code_hash") != cur_contracts
                or not d.get("u_hash")):
            bad.append(app_id)
        else:
            checked += 1
    return {"coherence_checked": checked, "failed": bad[:20], "n_failed": len(bad),
            "pass": len(bad) == 0}


def main():
    result = {"bundle": "UNKNOWN", "steps": {}}

    result["mode"] = "changed-only" if CHANGED_ONLY else "full"

    # 1. 앱 재봉인 + 재발견 교차검증 (결정론 포함: registry 와 byte 일치 재생성)
    #    changed-only: forge_apps 가 변경 spec 만 재조립 + 무변경 앱 coherence(fingerprint/redisc).
    forge_args = [".pgf/autoforge/forge_apps.py"] + (["--changed-only"] if CHANGED_ONLY else [])
    rc, out = run(forge_args)
    m = re.search(r"앱 봉인 (\d+)/(\d+) · 재발견 교차검증 (\d+)/(\d+)", out)
    fa = {"rc": rc, "apps_sealed": f"{m.group(1)}/{m.group(2)}" if m else "?",
          "rediscovery": f"{m.group(3)}/{m.group(4)}" if m else "?", "pass": rc == 0}
    if CHANGED_ONLY:
        cm = re.search(r"재조립 (\d+) · coherence (\d+)", out)
        if cm:
            fa["reassembled"], fa["coherence"] = int(cm.group(1)), int(cm.group(2))
    result["steps"]["forge_apps"] = fa

    # 1b. Heavy frontier generators with script-local fast paths.
    #     changed-only: frontier/factory 앱 spec 이 무변경이면 재봉인(수백초) 대신 coherence 스윕으로 대체.
    #       변경된 frontier/factory spec 이 있으면 full 재봉인으로 안전 폴백.
    frontier_specs_changed = _frontier_specs_changed() if CHANGED_ONLY else True
    if CHANGED_ONLY and not frontier_specs_changed:
        # legacy frontier 무변경 → coherence 스윕. factory 앱은 factory --reproduce(저비용)가 담당.
        cov = _coherence_sweep_frontier()
        result["steps"]["frontier_coherence"] = cov
        fstep_id, fscript = FACTORY_STEP
        rc, out = run([fscript, "--reproduce"])       # 9s, factory N 전부 byte-identity 재봉인
        result["steps"][fstep_id] = {
            "rc": rc, "all_ok": "all_ok=True" in out,
            "pass": rc == 0 and "all_ok=True" in out}
    else:
        for step_id, script in FRONTIER_STEPS:
            rc, out = run([script])
            result["steps"][step_id] = {
                "rc": rc,
                "all_ok": "all_ok=True" in out,
                "pass": rc == 0 and "all_ok=True" in out}
        # Data-driven factory reproduction (INV-F5)
        fstep_id, fscript = FACTORY_STEP
        rc, out = run([fscript, "--reproduce"])
        result["steps"][fstep_id] = {
            "rc": rc, "all_ok": "all_ok=True" in out,
            "pass": rc == 0 and "all_ok=True" in out}

    # 2. registry manifest + dependency graph
    rc, out = run(["scripts/registry_tools.py", "build"])
    mm = re.search(r"modules=(\d+) unique_apps=(\d+) cached=(\d+) root=(\w+)", out)
    result["steps"]["registry"] = {
        "rc": rc, "modules": mm.group(1) if mm else "?", "unique_apps": mm.group(2) if mm else "?",
        "cached": mm.group(3) if mm else "?", "root_hash": mm.group(4) if mm else "?", "pass": rc == 0}

    # 3. 독립 2차 검증 (Qualtran 비의존)
    rc, out = run(["scripts/second_oracle.py"])
    sm = re.search(r"모듈 독립검증 (\d+)/(\d+)", out)
    result["steps"]["second_oracle"] = {"rc": rc, "modules": f"{sm.group(1)}/{sm.group(2)}" if sm else "?",
                                        "pass": rc == 0}

    # 3a2. V08_5: 규약(전역위상·atol) 변주 하 seal 재현 실증 (convention-independence, A3)
    rc, out = run(["scripts/inverted_second_oracle.py", "--quick"])
    result["steps"]["convention_independence"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3b. V08 P0: structural Shor 앱 modexp 코어 부분공간 순열 강검증 (경량 재검증)
    #     path A=회로 게이트순열 vs path B=정수산술 w·a^c mod N. sidecar(.pgf/proofs) 비파괴, root 무영향.
    rc, out = run(["scripts/perm_subspace_verify.py", "--quick"])
    result["steps"]["perm_subspace"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3c. V08 HonestyHardening: 봉인 resource == 자식 resource 합 독립 재계산 (A6)
    rc, out = run(["scripts/resource_witness.py", "--quick"])
    result["steps"]["resource_witness"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3d. V08_6/8: block-encoding 규약 감사 + QSP 다항식 관측 (QSVT 수평클래스)
    rc, out = run(["scripts/blockencoding_audit.py", "--quick"])
    result["steps"]["blockencoding_audit"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3e. V08_10: 봉인 팔레트로 타겟 golden 재분해 자동 탐색 → oracle 하드게이트 (발견 자율화)
    rc, out = run(["scripts/discovery_superopt.py", "--quick"])
    result["steps"]["discovery_superopt"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3f. V08 QSVT consumer: e^{-iAt} Chebyshev(Jacobi-Anger) 근사 관측 (Hamiltonian sim, observation)
    rc, out = run(["scripts/qsvt_hamsim_observe.py", "--quick"])
    result["steps"]["qsvt_hamsim_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3g. V08 QSVT consumer: amplitude amplification = QSP 홀수 다항식 관측 (검색, observation)
    rc, out = run(["scripts/qsvt_ampamp_observe.py", "--quick"])
    result["steps"]["qsvt_ampamp_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3h. V08 Fermionic simulation: Jordan-Wigner 반교환 보존 검증 + be_hop (새 수평축)
    rc, out = run(["scripts/fermionic_jw_observe.py", "--quick"])
    result["steps"]["fermionic_jw_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3i. V08 Fermionic: 완전한 t-V Fermi-Hubbard 모델 관측 (be_hop + be_num)
    rc, out = run(["scripts/hubbard_observe.py", "--quick"])
    result["steps"]["hubbard_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3j. V08 QSVT consumer: matrix inversion(linear systems) = 홀수 다항식 P(A)≈c·A⁻¹ 관측 (선형대수)
    rc, out = run(["scripts/matrix_inversion_observe.py", "--quick"])
    result["steps"]["matrix_inversion_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3k. V08 Fermionic: 정통 spinful Fermi-Hubbard (2site×2spin, be_hopz Z-string + be_num)
    rc, out = run(["scripts/spinful_hubbard_observe.py", "--quick"])
    result["steps"]["spinful_hubbard_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3l. V08 FTQC: non-Clifford universality (magic state |A> + T-injection)
    rc, out = run(["scripts/magic_state_observe.py", "--quick"])
    result["steps"]["magic_state_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3m. V08 Fermionic 응용: 실제 분자 H₂ 양자화학 (봉인 be_hop·be_num 조합, observation)
    rc, out = run(["scripts/h2_molecule_observe.py", "--quick"])
    result["steps"]["h2_molecule_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3n. HE H1.3: JW↔BK 인코딩 등가성(exact 켤레변환)+weight payoff (bk4_transform·bk_num1·bk_hop01, observation)
    rc, out = run(["scripts/bk_equiv_observe.py", "--quick"])
    result["steps"]["bk_equiv_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3o. HE H1.4: parity 인코딩 입자수-대칭 tapering (parity4_transform 켤레변환, observation)
    rc, out = run(["scripts/parity_taper_observe.py", "--quick"])
    result["steps"]["parity_taper_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3p. HE H3.1: [[5,1,3]] 5-to-1 magic distillation coherent-branch (code513_encoder, observation)
    rc, out = run(["scripts/distill5to1_observe.py", "--quick"])
    result["steps"]["distill5to1_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3q. HE H3.2: Steane 논리 T-injection — encoded non-Clifford (신규 봉인 0, observation)
    rc, out = run(["scripts/steane_encoded_t_observe.py", "--quick"])
    result["steps"]["steane_encoded_t_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3r. HE H5.2′: 이면군 D₄ Hidden Subgroup 소비 (d4_mult·d4_qft 구동, 문자론 참조, observation)
    rc, out = run(["scripts/d4_hsp_observe.py", "--quick"])
    result["steps"]["d4_hsp_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3s. HE H6.1′: 큐트릿 삼진 산술 관측 + qudit 게이트 경계 (qutrit_x3·qutrit_sum, observation)
    rc, out = run(["scripts/qutrit_arith_observe.py", "--quick"])
    result["steps"]["qutrit_arith_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3t. HE2 P1.4: 완전 FTQC 논리 스택 관측 (surf422·toric22·ls_merge + v1 magic 자산 정합, observation)
    rc, out = run(["scripts/logical_stack_observe.py", "--quick"])
    result["steps"]["logical_stack_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3u. HE2 P4.1: Ising/Majorana 브레이드 Yang-Baxter 관계 (ising_braid_b2, observation)
    rc, out = run(["scripts/braid_observe.py", "--quick"])
    result["steps"]["braid_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3v. HE2 P2.2: MBQC 측정패턴↔회로 등가 (cluster3x3·mbqc_h, observation)
    rc, out = run(["scripts/mbqc_observe.py", "--quick"])
    result["steps"]["mbqc_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3w. HE2 P5.1: Clifford QCA 위상분류 + discrete-time exact (qca_step, observation)
    rc, out = run(["scripts/gnvw_index_observe.py", "--quick"])
    result["steps"]["gnvw_index_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3x. HE2 T2.2: Z₂ 격자게이지 Gauss law + gauge-invariant H (z2gauge3, observation)
    rc, out = run(["scripts/z2gauge_observe.py", "--quick"])
    result["steps"]["z2gauge_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3y. HE2 T3: ZX-calculus Clifford fragment 3번째 독립 검증 경로 (verification)
    rc, out = run(["scripts/zx_verify.py", "--quick"])
    result["steps"]["zx_verify"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3z. HE2 T1: Schur-Weyl transform J²/Jz 동시대각 + S₃ duality witness (schur3, observation)
    rc, out = run(["scripts/schur_observe.py", "--quick"])
    result["steps"]["schur_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3aa. HE2 V4: AKLT₄ VBS — 독립 MPS 수축 exact + parent-H/triplet witness (aklt4, observation)
    rc, out = run(["scripts/aklt_observe.py", "--quick"])
    result["steps"]["aklt_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3ab. HE2 V6: CPTP 채널 Stinespring dilation — Tr_env==Kraus 채널 exact + CPTP witness (observation)
    rc, out = run(["scripts/channel_observe.py", "--quick"])
    result["steps"]["channel_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3ac. HE2 V7: 채널→QEC 완결 파이프라인 — 봉인 채널 오류주입→봉인 QEC 정정→exact 복원 (observation)
    rc, out = run(["scripts/qec_channel_observe.py", "--quick"])
    result["steps"]["qec_channel_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3ad. HE2 V8: 1q Clifford 군(cliff1_* 24 봉인 앱) = 정확 unitary 2/3-design witness (observation)
    rc, out = run(["scripts/twodesign_observe.py", "--quick"])
    result["steps"]["twodesign_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3ae. HE3 H3.1: 정수 산술 1급 자산 — 전수 정수 two-path + ripple==Fourier 교차 (observation)
    rc, out = run(["scripts/arithmetic_observe.py", "--quick"])
    result["steps"]["arithmetic_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3af. HE3 H3.2: Szegedy walk — 정의식 재유도 + 스펙트럼 정리 + 정상벡터 witness (observation)
    rc, out = run(["scripts/szegedy_observe.py", "--quick"])
    result["steps"]["szegedy_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3ag. HE3 H3.3: Choi channel-state duality — J==Kraus·CP/TP·J→E 재구성 witness (observation)
    rc, out = run(["scripts/choi_observe.py", "--quick"])
    result["steps"]["choi_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3ah. HE3 H3.4: path-sum(ℤ[ω₈]) 4번째 독립 검증경로 — 봉인 0, sidecar witness (observation)
    rc, out = run(["scripts/pathsum_verify.py", "--quick"])
    result["steps"]["pathsum_verify"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3ai. TrackGate6 G1: 2×2 RVB PEPS — dimer 정의 독립 재구성+S_tot²=0+reduced I/2 witness (observation)
    rc, out = run(["scripts/peps_observe.py", "--quick"])
    result["steps"]["peps_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3aj. TrackGate6 G2b: d=4 MUB-20 — Pauli 라벨맵+비편향+state 2-design+단층재구성 witness (observation)
    rc, out = run(["scripts/mub_observe.py", "--quick"])
    result["steps"]["mub_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3ak. TrackGate6 G3e: UD-POVM Naimark 완성 — E_k==IDP·UD·통계·W층 teeth witness (observation)
    rc, out = run(["scripts/naimark_observe.py", "--quick"])
    result["steps"]["naimark_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3al. TrackGate6 G4: 4-qubit Schur-Weyl — J²/Jz 동시대각+S₄ duality+teeth witness (observation)
    rc, out = run(["scripts/schur4_observe.py", "--quick"])
    result["steps"]["schur4_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3am. TrackGate6 G5: Fibonacci braid — Yang-Baxter+B₃중심+z5⁵=Z 재발견+비-Clifford witness (observation)
    rc, out = run(["scripts/fib_braid_observe.py", "--quick"])
    result["steps"]["fib_braid_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3an. TrackR3Residue C7: 1-flag FT 증후 추출 — flag 정리+hook teeth+surf422 복리 witness (observation)
    rc, out = run(["scripts/flag_syndrome_observe.py", "--quick"])
    result["steps"]["flag_syndrome_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3ao. TrackR3Residue C6: GF(8) 역원·Frobenius — 독립 산술+Galois 구조+mulx 궤도 witness (observation)
    rc, out = run(["scripts/gf8_observe.py", "--quick"])
    result["steps"]["gf8_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3ap. TrackC3Hierarchy: Clifford 계층·teleportation 촉매 — 계층 판정+촉매+사다리 witness (observation)
    rc, out = run(["scripts/hierarchy_observe.py", "--quick"])
    result["steps"]["hierarchy_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3aq. TrackHE4 P1: Fibonacci 소비층 — F-move 교차 + Jones 두 독립 경로 + Markov 소멸 (observation)
    rc, out = run(["scripts/fib_jones_observe.py", "--quick"])
    result["steps"]["fib_jones_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3ar. TrackHE4 P6: stabilizer-rank 제5 독립 검증경로 — 표본 모드(INV-F1 계층화; 정본=full proofs)
    rc, out = run(["scripts/stabrank_verify.py", "--quick", "--sample"])
    result["steps"]["stabrank_verify_sample"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3as. TrackHE4-R2: [[8,3,2]] triorthogonal — 첫 비-Clifford 횡단 논리 CCZ witness (observation)
    rc, out = run(["scripts/code832_observe.py", "--quick"])
    result["steps"]["code832_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3at. TrackHE5 P1: 정확해 동역학 — dual-unitary 쌍대성·광원뿔 두 경로·Floquet (observation)
    rc, out = run(["scripts/dyn_observe.py", "--quick"])
    result["steps"]["dyn_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3au. TrackHE5 P2: magic 자원 exact 증명서 — extent/robustness/T-count/변환 판정 (observation)
    rc, out = run(["scripts/magic_resource_observe.py", "--quick"])
    result["steps"]["magic_resource_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3av. TrackHE5 P3: Gaussian/matchgate 제6 독립 검증경로 — Majorana/SO(2n) (infra)
    rc, out = run(["scripts/matchgate_verify.py", "--quick"])
    result["steps"]["matchgate_verify"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3aw. TrackHE5 P4: RM [[15,1,3]] + transversal T — 정수/심볼릭 witness (observation)
    rc, out = run(["scripts/rm15_observe.py", "--quick"])
    result["steps"]["rm15_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3ax. TrackHE6 P4: S₄ 비아벨 곱셈 witness + (2,2) ζ₃ closed-negative 반증 (observation)
    rc, out = run(["scripts/s4_observe.py", "--quick"])
    result["steps"]["s4_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3ay. TrackHE6 P2: Bogoliubov/Kitaev pairing — 수보존 깸·R∈SO(4)·Pfaffian Z₂ (observation)
    rc, out = run(["scripts/bogoliubov_observe.py", "--quick"])
    result["steps"]["bogoliubov_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3az. TrackHE6 P5: 텐서망 정확 수축 제7 독립 검증경로 — 표본 모드(정본=full proofs)
    rc, out = run(["scripts/tncontract_verify.py", "--quick", "--sample"])
    result["steps"]["tncontract_verify_sample"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3aaa. TrackHE7 P1: QMDD 정확 정규형 제8 독립 검증경로 — 표본 모드(정본=full proofs)
    rc, out = run(["scripts/qmdd_verify.py", "--quick", "--sample"])
    result["steps"]["qmdd_verify_sample"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3aab. TrackHE7 P2: 4-Majorana braiding 구조 관측 witness (§3i 축 개창, seal 아님)
    rc, out = run(["scripts/maj_observe.py", "--quick"])
    result["steps"]["maj_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3aac. TrackHE7 P3: Pauli 채널 diamond-norm exact distance certificate (자원이론, seal 아님)
    rc, out = run(["scripts/diamond_observe.py", "--quick"])
    result["steps"]["diamond_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3aad. TrackHE7 P4: dual-unitary operator entanglement exact witness (동역학, seal 아님)
    rc, out = run(["scripts/op_ee_observe.py", "--quick"])
    result["steps"]["op_ee_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3aae. TrackHE7 P6: 부호 연접 [[25,1,9]] 코드-정확성 witness (§3i concatenation 개창, seal 아님)
    rc, out = run(["scripts/concat_observe.py", "--quick"])
    result["steps"]["concat_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3aaf. TrackHE8 P1: ANF/bit-vector 제9 독립 검증경로 — 표본 모드(정본=full ANF-VERIFY.json)
    rc, out = run(["scripts/anf_verify.py", "--quick", "--sample"])
    result["steps"]["anf_verify_sample"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3aap. TrackHE9 P1: Gröbner/ℤ[ω] phase-ideal 제10 독립 검증경로 — 표본(정본=full GROEBNER-VERIFY.json)
    rc, out = run(["scripts/groebner_verify.py", "--quick", "--sample"])
    result["steps"]["groebner_verify_sample"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3aaq. TrackHE9 P4: A₄ ζ₃-필연 문자표 witness (선검증·비-rational 군-Fourier 닫힘, seal 아님)
    rc, out = run(["scripts/a4_observe.py", "--quick"])
    result["steps"]["a4_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3aag. TrackHE8 P2: B₃ 초팔면체군 ζ-free 정수-monomial 구조 witness (S₄ ζ₃ 상보 positive, seal 아님)
    rc, out = run(["scripts/b3_observe.py", "--quick"])
    result["steps"]["b3_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3aah. TrackHE8 P4: 하이퍼그래프곱 qLDPC [[27,4,3]] 코드-정확성 witness (§3k P6 대형 HGP 개창, seal 아님)
    rc, out = run(["scripts/hgp_observe.py", "--quick"])
    result["steps"]["hgp_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3aai. TrackHE8 P3: 2D QWZ Chern 정수 위상 불변량 witness (§3k P2 2D Chern 개창, seal 아님)
    rc, out = run(["scripts/chern_observe.py", "--quick"])
    result["steps"]["chern_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3aaj. TrackHE8 P6: non-Pauli(coherent) 유니터리 채널 diamond-norm exact witness (§3k P3 상보, seal 아님)
    rc, out = run(["scripts/diamond_unitary_observe.py", "--quick"])
    result["steps"]["diamond_unitary_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3aak. TrackHE8 P5: Peres-Mermin state-independent 맥락성 증명서 (§3j 맥락성 개창, seal 아님)
    rc, out = run(["scripts/peres_mermin_observe.py", "--quick"])
    result["steps"]["peres_mermin_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3aal. 순환 Hamming/BCH CSS [[15,7,3]] 코드-정확성 witness (§3j cyclic 대수부호 개창, seal 아님)
    rc, out = run(["scripts/bch_observe.py", "--quick"])
    result["steps"]["bch_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3aam. distance-5 순환 BCH CSS [[31,11,5]] 코드-정확성 witness (§4 d≥5·BCH 관문, seal 아님)
    rc, out = run(["scripts/bch31_observe.py", "--quick"])
    result["steps"]["bch31_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3aan. TrackHE9 P2: Peres-Mermin contextual fraction LP 정량화 witness (§3l P5 승격, seal 아님)
    rc, out = run(["scripts/contextual_fraction_observe.py", "--quick"])
    result["steps"]["contextual_fraction_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 3aao. TrackHE9 P3: |C|≥2 고차 Chern (spin-S multi-Weyl) 정수 위상 witness (§3l P3, seal 아님)
    rc, out = run(["scripts/chern_higher_observe.py", "--quick"])
    result["steps"]["chern_higher_observe"] = {
        "rc": rc, "all_ok": "all_ok=True" in out,
        "pass": rc == 0 and "all_ok=True" in out}

    # 4. 행동 검증 — Shor 인수분해 (15=3×5 via a2,a7) + cmul21 orbit(period 6 → 21=3×7)
    beh = {}
    import numpy as np
    def golden_of(app):
        src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
        code = re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1)
        ns = {}; exec(code, ns); return ns["golden"]
    for app, dim, exp in [("shor15_a2.app.pg", 128, {0, 2, 4, 6}), ("shor15_a7.app.pg", 128, {0, 2, 4, 6})]:
        G = golden_of(app); psi = np.zeros(dim, complex); psi[1] = 1.0
        out = G @ psi; pk = {}
        for s in range(dim):
            if abs(out[s]) ** 2 > 1e-9:
                c = (s >> 4) & 7; pk[c] = pk.get(c, 0) + abs(out[s]) ** 2
        beh[app[:-7]] = {"peaks": sorted(pk), "expected": sorted(exp),
                         "pass": set(k for k in pk if pk[k] > 0.01) == exp}
    # cmul2_mod21 orbit period 6
    G = golden_of("cmul2_mod21.app.pg")
    w = 1; orbit = [1]
    for _ in range(6):
        w = int(np.argmax(G[:, (1 << 5) | w])) & 31; orbit.append(w)
    beh["cmul2_mod21_orbit"] = {"orbit": orbit, "period6": orbit[0] == orbit[6] and len(set(orbit[:6])) == 6}
    result["steps"]["behavior"] = {"detail": beh,
                                   "pass": all(v.get("pass", v.get("period6")) for v in beh.values())}

    allpass = all(s.get("pass") for s in result["steps"].values())
    result["bundle"] = "REPRODUCED" if allpass else "FAILED"
    json.dump(result, open(os.path.join(REPORTS, "REPRODUCE-RESULT.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("=" * 70)
    print(f"REPRODUCE-ALL → {result['bundle']}")
    for k, v in result["steps"].items():
        print(f"  {'✓' if v.get('pass') else '✗'} {k}: " +
              ", ".join(f"{kk}={vv}" for kk, vv in v.items() if kk not in ("detail", "rc")))
    print("-" * 70)
    print("INV-R1: 'REPRODUCED'=결정론적 byte-identical 재현이지 correctness 증명이 아니다.")
    print("  정확성은 오라클의 독립검증(C1-C4·second_oracle·subspace/resource witness)에서 온다.")
    print("=" * 70)
    return 0 if allpass else 1


if __name__ == "__main__":
    sys.exit(main())
