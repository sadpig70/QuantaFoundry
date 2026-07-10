#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""matchgate_verify — TrackHE5 P3: Gaussian/matchgate **제6 독립 검증경로** (Majorana/SO(2n), 인프라).

기존 5경로(dense·tableau·ZX·path-sum ℤ[ω₈]·stabilizer-rank)에 이은 여섯 번째 독립 수학:
자유 페르미온(Gaussian) 회로를 **Jordan-Wigner Majorana 켤레 R ∈ SO(2n)** 로 재검증한다.
R 은 봉인 golden 을 읽지 않고 **plan 구조(게이트 이름·각도·배선)에서 직접 컴파일** — O(n²) 인증서가
2ⁿ 유니터리를 위상 제외 결정(Gaussian 부분군 한정)한다.

  게이트 테이블(부호 규약 = 선검증 고정):
    diag(1, e^{iθ}) on q_j (z/s/sdg/t/rz_negpi4/rz_negpi8) → 평면(2j, 2j+1) 회전 −θ
    iswap(j, j+1 인접)  → 정수 R 블록: c₂ⱼ→c₂ⱼ₊₃, c₂ⱼ₊₁→−c₂ⱼ₊₂, c₂ⱼ₊₂→c₂ⱼ₊₁, c₂ⱼ₊₃→−c₂ⱼ
    fswap(app, 인접)    → Majorana 쌍 순열(부호 없음) — 페르미온 SWAP 정의에서 유도
  검증(커버 앱마다):
    ① R-두 경로: plan 컴파일 R == golden 켤레 적합 R (평면별 회전의 정수/닫힌형 합성 vs dense 유도)
    ② RᵀR == I · det R == +1 (SO(2n) witness)
    ③ 진공 진폭: |golden[0,0]| == |det A|^{1/2} (A = 복소 페르미온 블록 — 행렬식류 자유페르미온 공식)
  커버리지: plan-구조 자동 발견(전 게이트 테이블 내 + 인접성) — skip 전수 사유 기록(silent cap 금지).
  ★census(관측 라벨 분리): 봉인 golden 의 유니터리-수준 Gaussian성 스캔(fit_R) — 예: fswap 앱은
  golden 이 Gaussian이나 plan 이 swap·cz 로 구현돼 as-written 비인식(정직 구분: 경로 독립성은
  plan-커버리지에만 주장).
  자가시험: 테이블 무작위 word(n=3, seed) R-컴파일 == 켤레 적합. teeth: cz/cnot 비-Gaussian 판정·
  비인접 iswap 배선 거부·R 각도 오염 → 두 경로 불일치.

정직 경계(INV-Q3): 인프라 — 새 봉인 0·root 불변(demo 앱은 별도 봉인분)·오라클/frozen 무접촉.
  커버 = {1q 대각 회전, 인접 iswap/fswap} 조립 앱(수보존 중심) — 전면 아님·pairing 게이트 팔레트 무.
  수치 = 부동소수(테이블 성분은 dyadic-π 닫힌형) — 전제 독립(안정군·행렬곱·경로합 아닌 SO(2n))이 요점.

사용: python scripts/matchgate_verify.py [--quick]
"""
import os, sys, re, json, glob
from functools import reduce
import numpy as np

from qf_witness.core.paths import ROOT
OUT = os.path.join(ROOT, ".pgf", "proofs", "MATCHGATE-VERIFY.json")

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)

DIAG_THETA = {"z_gate": np.pi, "s_gate": np.pi / 2, "sdg_gate": -np.pi / 2,
              "t_gate": np.pi / 4, "rz_negpi4": -np.pi / 4, "rz_negpi8": -np.pi / 8}
N_CAP = 8


def kron(*m):
    return reduce(np.kron, m)


def majorana(n):
    cs = []
    for j in range(n):
        cs.append(kron(*([Z] * j + [X] + [I2] * (n - j - 1))))
        cs.append(kron(*([Z] * j + [Y] + [I2] * (n - j - 1))))
    return cs


def fit_R(U, cs):
    """golden 켤레 적합: U c_μ U† = Σ R[μ,ν] c_ν — 실패(비-Gaussian) 시 None."""
    n2, dim = len(cs), cs[0].shape[0]
    R = np.zeros((n2, n2))
    for mu in range(n2):
        M = U @ cs[mu] @ U.conj().T
        for nu in range(n2):
            v = np.trace(cs[nu] @ M) / dim
            if abs(np.imag(v)) > 1e-9:
                return None
            R[mu, nu] = np.real(v)
        if not np.allclose(M, sum(R[mu, nu] * cs[nu] for nu in range(n2)), atol=1e-9):
            return None
    return R


def rot_plane(n2, a, b, th):
    R = np.eye(n2)
    R[a, a] = R[b, b] = np.cos(th)
    R[a, b] = -np.sin(th)
    R[b, a] = np.sin(th)
    return R


def gate_R(name, tg, n):
    """plan 게이트 → R (golden 미참조 — 테이블 규약에서 직접). 미지원/비인접 → None."""
    n2 = 2 * n
    if name in DIAG_THETA:
        j = tg[0]
        return rot_plane(n2, 2 * j, 2 * j + 1, -DIAG_THETA[name])
    if name == "iswap":
        i, j = tg
        if abs(i - j) != 1:
            return None
        a = 2 * min(i, j)
        R2 = np.eye(n2)
        R2[a, a] = R2[a + 1, a + 1] = R2[a + 2, a + 2] = R2[a + 3, a + 3] = 0
        R2[a, a + 3], R2[a + 3, a] = 1, -1
        R2[a + 1, a + 2], R2[a + 2, a + 1] = -1, 1
        return R2
    if name == "fswap":
        i, j = tg
        if abs(i - j) != 1:
            return None
        a = 2 * min(i, j)
        R = np.eye(n2)
        for r in (a, a + 1, a + 2, a + 3):
            R[r, r] = 0
        R[a, a + 2] = R[a + 2, a] = R[a + 1, a + 3] = R[a + 3, a + 1] = 1
        return R
    return None


def flatten(app_file, targets=None):
    src = open(os.path.join(ROOT, "specs", "apps", app_file), encoding="utf-8").read()
    plan = json.loads(re.search(r"```json id=plan\s*\n(.*?)\n```", src, re.S).group(1))
    ops = []
    for st in plan["steps"]:
        tg = st.get("targets")
        if tg is None:
            tg = targets
        elif targets is not None:
            tg = [targets[q] for q in tg]
        if "app" in st:
            name = st["app"][:-len(".app.pg")]
            if name == "fswap":                      # 테이블 앱 항목(페르미온 정의 유도)
                ops.append(("fswap", tg))
            else:
                ops += flatten(st["app"], tg)
            continue
        ops.append((st["spec"].split("/")[-1][:-3], tg))
    return ops


def compile_R(ops, n):
    """켤레 합성: U=U_k…U_1 → U c U† 의 R = R_1·R_2·…·R_k (적용 순 오른쪽 곱)."""
    R = np.eye(2 * n)
    for name, tg in ops:
        g = gate_R(name, tg, n)
        if g is None:
            return None, f"unsupported:{name}@{tg}"
        R = R @ g
    return R, None


def load_golden(app_file):
    src = open(os.path.join(ROOT, "specs", "apps", app_file), encoding="utf-8").read()
    m = re.search(r"```python id=app_golden\n(.*?)```", src, re.S)
    if not m:
        return None
    ns = {}
    exec(m.group(1), ns)
    return ns["golden"]


def vacuum_two_path(U, R, n):
    A = np.zeros((n, n), dtype=complex)
    for j in range(n):
        row = R[2 * j, :] + 1j * R[2 * j + 1, :]
        for k in range(n):
            A[j, k] = (row[2 * k] - 1j * row[2 * k + 1]) / 2
    return bool(abs(abs(U[0, 0]) - abs(np.linalg.det(A)) ** 0.5) < 1e-9)


def selftest(seed=0, rounds=16):
    rng = np.random.default_rng(seed)
    G1 = {"z_gate": Z, "s_gate": np.diag([1, 1j]), "sdg_gate": np.diag([1, -1j]),
          "t_gate": np.diag([1, np.exp(1j * np.pi / 4)])}
    ISW = np.array([[1, 0, 0, 0], [0, 0, 1j, 0], [0, 1j, 0, 0], [0, 0, 0, 1]], dtype=complex)
    FS = np.diag([1, 1, 1, -1]) @ np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
    n = 3
    cs = majorana(n)
    for _ in range(rounds):
        ops, U = [], np.eye(8, dtype=complex)
        for _ in range(int(rng.integers(3, 8))):
            pick = int(rng.integers(0, 6))
            if pick < 4:
                name = list(G1)[pick]
                q = int(rng.integers(0, n))
                ops.append((name, [q]))
                mats = [G1[name] if k == q else I2 for k in range(n)]
                U = kron(*mats) @ U
            else:
                i = int(rng.integers(0, n - 1))
                g = ISW if pick == 4 else FS
                ops.append(("iswap" if pick == 4 else "fswap", [i, i + 1]))
                U = kron(np.eye(2 ** i, dtype=complex), g,
                         np.eye(2 ** (n - i - 2), dtype=complex)) @ U
        Rc, err = compile_R(ops, n)
        Rf = fit_R(U, cs)
        if err or Rf is None or not np.allclose(Rc, Rf, atol=1e-9):
            return False
    return True


def verify_app(aid):
    spec = f"{aid}.app.pg"
    src_path = os.path.join(ROOT, "specs", "apps", spec)
    am = json.loads(re.search(r"```json id=app_meta\s*\n(.*?)\n```",
                              open(src_path, encoding="utf-8").read(), re.S).group(1))
    n = am["n_sys"] + am.get("n_anc", 0)
    if n > N_CAP:
        return None, f"n={n}>cap"
    try:
        ops = flatten(spec)
    except Exception as e:
        return None, f"flatten:{e}"
    Rc, err = compile_R(ops, n)
    if err:
        return None, err
    U = load_golden(spec)
    if U is None:
        return None, "no-dense-golden"
    Rf = fit_R(U, majorana(n))
    two_path = bool(Rf is not None and np.allclose(Rc, Rf, atol=1e-9))
    so_ok = bool(np.allclose(Rc @ Rc.T, np.eye(2 * n), atol=1e-10)
                 and abs(np.linalg.det(Rc) - 1) < 1e-9)
    vac_ok = vacuum_two_path(U, Rc, n)
    return {"n": n, "gates": len(ops), "R_two_path": two_path,
            "SO2n": so_ok, "vacuum_det": vac_ok,
            "pass": two_path and so_ok and vac_ok}, None


def main():
    quick = "--quick" in sys.argv
    st_ok = selftest()

    # 커버리지 자동 발견(plan-구조)
    verified, skipped = {}, {}
    for p in sorted(glob.glob(os.path.join(ROOT, "registry", "apps", "*.sealed.json"))):
        aid = os.path.basename(p)[:-len(".sealed.json")]
        if not os.path.exists(os.path.join(ROOT, "specs", "apps", f"{aid}.app.pg")):
            skipped[aid] = "no-spec"
            continue
        res, why = verify_app(aid)
        if res is None:
            skipped[aid] = why
        else:
            verified[aid] = res
    n_pass = sum(1 for v in verified.values() if v["pass"])

    # 테이블 항목 골든-정합(관측 라벨): iswap module·fswap app
    ns_ = {}
    exec(re.search(r"```python id=golden\n(.*?)```",
                   open(os.path.join(ROOT, "specs", "modules", "iswap.pg"),
                        encoding="utf-8").read(), re.S).group(1), ns_)
    isw_ok = bool(np.allclose(fit_R(ns_["golden"], majorana(2)), gate_R("iswap", [0, 1], 2), atol=1e-10))
    fs_ok = bool(np.allclose(fit_R(load_golden("fswap.app.pg"), majorana(2)),
                             gate_R("fswap", [0, 1], 2), atol=1e-10))

    # ★census(관측): 유니터리-수준 Gaussian성 (n≤4 표본 — as-written 과 구분)
    #   bogoliubov_pair = pairing(비수보존) Gaussian — 제6경로 pairing 확장(TrackHE6 P2)
    census = {}
    for aid in ("fswap", "ising_braid_b2", "du_gate_j8", "magic_cs", "bogoliubov_pair"):
        U = load_golden(f"{aid}.app.pg")
        nq = int(round(np.log2(U.shape[0])))
        census[aid] = bool(fit_R(U, majorana(nq)) is not None)
    census_ok = (census["fswap"] and census["ising_braid_b2"] and census["bogoliubov_pair"]
                 and not census["du_gate_j8"] and not census["magic_cs"])

    # teeth
    CZm = np.diag([1, 1, 1, -1]).astype(complex)
    CNOTm = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex)
    t1 = bool(fit_R(CZm, majorana(2)) is None and fit_R(CNOTm, majorana(2)) is None)
    t2 = bool(gate_R("iswap", [0, 2], 3) is None)          # 비인접 배선 거부(JW 문자열)
    Rbad = compile_R([("t_gate", [0])], 2)[0] @ rot_plane(4, 0, 1, 0.1)
    Ug = kron(np.diag([1, np.exp(1j * np.pi / 4)]), I2)
    t3 = bool(not np.allclose(Rbad, fit_R(Ug, majorana(2)), atol=1e-6))
    teeth_ok = t1 and t2 and t3

    ok = bool(st_ok and n_pass == len(verified) and len(verified) >= 2
              and isw_ok and fs_ok and census_ok and teeth_ok)
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        rep = {"_schema": "matchgate-verify-v1",
               "_note": "제6 독립 검증경로(Majorana/SO(2n) — 자유 페르미온). plan 독립 R 컴파일 vs "
                        "golden 켤레 두 경로. 인프라 — 새 봉인 0·오라클 무접촉(INV-Q3).",
               "engine_selftest": st_ok,
               "verified": verified, "verified_pass": n_pass, "verified_total": len(verified),
               "skipped_count": len(skipped),
               "table_golden_consistency": {"iswap": isw_ok, "fswap": fs_ok},
               "unitary_level_census": {**census,
                                        "note": "golden 수준 Gaussian성 관측 — as-written 커버리지와 "
                                                "구분(경로 독립성은 plan-커버리지에만 주장). "
                                                "예: fswap golden=Gaussian, plan=swap·cz 비인식"},
               "coverage_note": f"커버={{1q 대각 회전, 인접 iswap/fswap}} 조립 · n≤{N_CAP} · "
                                "pairing 게이트 팔레트 무 — 전면 아님(정직)",
               "teeth": {"cz_cnot_nongaussian": t1, "nonadjacent_rejected": t2,
                         "angle_corrupt_mismatch": t3},
               "independence": "dense(행렬곱)·tableau(안정군)·ZX(그래프)·path-sum(ℤ[ω₈])·"
                               "stab-rank(Clifford-합)와 다른 SO(2n)/자유페르미온 전제 — 여섯 번째 경로.",
               "ok": ok}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(rep, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("Gaussian/matchgate 제6 검증경로 (인프라, 새 봉인 0):", flush=True)
        print(f"  자가시험 {st_ok} · 커버 앱 검증 {n_pass}/{len(verified)} "
              f"({sorted(verified)}) · skip {len(skipped)}(사유 기록)", flush=True)
        print(f"  테이블 골든-정합 iswap {isw_ok}·fswap {fs_ok} · census(골든 수준): {census}", flush=True)
        print(f"  teeth: 비-Gaussian/비인접/각도오염 {t1}/{t2}/{t3}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"matchgate_verify: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
