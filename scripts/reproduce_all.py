"""reproduce_all.py — one-command 전체 재현 검증 (외부 리뷰 R-F 대응).

외부 reviewer 가 한 번에 전 검증을 재현하도록 오케스트레이션한다. 경로 비하드코딩(스크립트 기준 상대경로).
구성: 모듈/앱 재봉인 + 재발견 교차검증 + 결정론 + 독립 2차검증 + 행동(인수분해) + registry manifest.

사용:  python scripts/reproduce_all.py
출력:  reports/REPRODUCE-RESULT.json
"""
import os, sys, json, subprocess, re

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


def main():
    result = {"bundle": "UNKNOWN", "steps": {}}

    # 1. 앱 재봉인 + 재발견 교차검증 (결정론 포함: registry 와 byte 일치 재생성)
    rc, out = run([".pgf/autoforge/forge_apps.py"])
    m = re.search(r"앱 봉인 (\d+)/(\d+) · 재발견 교차검증 (\d+)/(\d+)", out)
    result["steps"]["forge_apps"] = {
        "rc": rc, "apps_sealed": f"{m.group(1)}/{m.group(2)}" if m else "?",
        "rediscovery": f"{m.group(3)}/{m.group(4)}" if m else "?",
        "pass": rc == 0}

    # 1b. Heavy frontier generators with script-local fast paths.
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
