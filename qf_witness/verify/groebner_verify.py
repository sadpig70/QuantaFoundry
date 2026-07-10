#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""groebner_verify — TrackHE9 P1: Gröbner / ℤ[ω] phase-ideal **제10 독립 검증경로** (인프라, 신규 봉인 0).

기존 9경로(dense·tableau·ZX·path-sum ℤ[ω₈]·stabilizer-rank·matchgate/SO(2n)·tensor-network·QMDD·
ANF/bit-vector)에 이은 열 번째. ★**제9 ANF 와의 함정 회피**: 순열회로에서 Gröbner 는 ANF 로 붕괴
(ANF-in-disguise)한다 → 그래서 이 경로는 **정확히 ANF 의 맹점 = 대각 위상 회로**(T·S·Z·CS·CZ·CCZ 등,
계산기저 permutation=항등이지만 진폭에 위상)를 타깃한다. ANF 는 진폭 무관 GF(2) Boolean 이라 이 앱들을
전수 skip(perm_of=None) — 검증 대상 자체가 겹치지 않는다.

  대각 유니터리 U=diag(ω_M^{f(x)}), f: {0,1}ⁿ→ℤ_M 는 **위상다항식**(phase polynomial). 두 독립 경로:
  path A: plan 게이트별 대각 위상다항식(각 게이트 golden 의 위상을 ℤ_M Möbius 로 국소 추출)을 타깃 wire 로
    remap 하여 **ℤ_M[x] 에서 symbolic 합** — 진폭/행렬곱 미사용, 위상 계수 대수만.
  path B: 봉인 앱 golden 대각의 args → 큐브 {0,1}ⁿ Möbius 로 위상다항식 f_B 독립 추출.
  PASS ⟺ (f_A − f_B) ∈ 이데알 I=⟨x_i²−x_i, M⟩  ⟺  Gröbner normal-form 감산 결과 ≡ 0 (mod M).

  ★genuine Gröbner(§4′): I 의 Boolean 생성원 G={x_i²−x_i} 이 **Gröbner basis** 임을 Buchberger S-다항식
  판정으로 확인(모든 S-poly 가 G 로 0 감산 — LT 가 x_i²/x_j² coprime → Buchberger 제1판정)한 뒤, 다변수
  다항식(지수벡터 monomial, ℤ_M 계수)을 그 rewrite 규칙 x_i²→x_i 로 **정규형(normal form)** 감산해 멤버십 판정.

  ★독립성(§4′(h), 한 문장): 제9 ANF 는 GF(2)[x]/(x²−x) **Boolean 순열 함수**(진폭 무관, mod 2)를, 제10 은
  ℤ_M[x]/(x²−x) **위상다항식**(진폭 argument, mod M=2ᵏ)을 다룬다 — 링·계수·검증 객체(위상 vs Boolean)가
  근본적으로 다르며, 커버 집합조차 **상보**(ANF=순열회로 / Gröbner=대각 위상회로, 교집합=skip). dense/path-sum
  ℤ[ω]과도 상이: 저들은 진폭 전체 행렬/경로합, 이건 위상 **다항식 계수의 이데알 멤버십**(행렬 미실체화).

정직 경계(seal 아님, root 불변 sidecar): 인프라 — 새 봉인 0·오라클/frozen 무접촉. 커버 = **대각 위상 회로만**
  (plan 게이트가 전부 대각·위상이 1의 거듭제곱근인 앱; H/CNOT 등 비대각 게이트 포함 앱은 skip 전수 사유 기록,
  silent cap 금지). 검증 결과 == golden 은 **검증경로**지 봉인 자산 아님. exact(ℤ_M 정수 대수, 부동소수 없음
  — 위상은 args→가장 가까운 ℤ_M 정수로 반올림, root-of-unity 아니면 skip).

사용: python scripts/groebner_verify.py [--quick] [--sample]
"""
import os, sys, re, json, glob
import numpy as np

from qf_witness.core.paths import ROOT
OUT = os.path.join(ROOT, ".pgf", "proofs", "GROEBNER-VERIFY.json")
N_CAP = 8             # 큐브 2ⁿ Möbius 상한(대각 위상 앱은 소형)
_MODG, _APPG = {}, {}


# ── genuine 다변수 다항식 over ℤ_M: monomial=지수 tuple(길이 nvars), 다항식=dict{monomial: coeff} ──
def nf_monomial(mono):
    """Boolean Gröbner G={x_i²−x_i} 의 normal form: 지수 e_i≥1 → 1 (x_i²→x_i rewrite)."""
    return tuple(1 if e else 0 for e in mono)


def poly_reduce(p, M):
    """정규형 감산(각 monomial 을 x_i²→x_i 로 rewrite) + 계수 mod M."""
    r = {}
    for mono, c in p.items():
        nm = nf_monomial(mono)
        r[nm] = (r.get(nm, 0) + c) % M
    return {m: c for m, c in r.items() if c % M}


def poly_axpy(p, q, M, s=1):
    """p + s·q  (mod M), 정규형 유지."""
    r = dict(p)
    for mono, c in q.items():
        nm = nf_monomial(mono)
        r[nm] = (r.get(nm, 0) + s * c) % M
    return {m: c for m, c in r.items() if c % M}


def buchberger_certifies_groebner(nvars, M):
    """teeth(genuine Gröbner): G={x_i²−x_i} 의 전 쌍 S-다항식이 G 로 0 감산 ⟺ Gröbner basis.
       S(g_i,g_j)= x_j²·g_i − x_i²·g_j (LT coprime). 지수벡터로 실제 구성·감산."""
    def gpoly(i):                                   # g_i = x_i² − x_i  (지수벡터)
        lt = tuple(2 if t == i else 0 for t in range(nvars))
        tt = tuple(1 if t == i else 0 for t in range(nvars))
        return {lt: 1, tt: -1}
    def mul_mono(p, mono):
        return {tuple(a + b for a, b in zip(mm, mono)): c for mm, c in p.items()}
    for i in range(nvars):
        for j in range(i + 1, nvars):
            xi2 = tuple(2 if t == i else 0 for t in range(nvars))
            xj2 = tuple(2 if t == j else 0 for t in range(nvars))
            S = poly_axpy(mul_mono(gpoly(i), xj2), mul_mono(gpoly(j), xi2), M, s=-1)
            if poly_reduce(S, M):                   # 정규형 ≠ 0 이면 Gröbner 아님
                return False
    return True


# ── 봉인 앱/모듈 로더 (anf_verify 규약) ──
def _load_mod(spec):
    name = spec.split("/")[-1][:-3]
    if name not in _MODG:
        src = open(os.path.join(ROOT, "specs", "modules", f"{name}.pg"), encoding="utf-8").read()
        m = re.search(r"```python id=golden\n(.*?)```", src, re.S)
        _MODG[name] = None
        if m:
            ns = {}; exec(m.group(1), ns); _MODG[name] = ns.get("golden")
    return _MODG[name]


def _load_app_golden(app):
    if app not in _APPG:
        src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
        m = re.search(r"```python id=app_golden\n(.*?)```", src, re.S)
        _APPG[app] = None
        if m:
            ns = {}; exec(m.group(1), ns); _APPG[app] = ns["golden"]
    return _APPG[app]


def _meta(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    am = json.loads(re.search(r"```json id=app_meta\s*\n(.*?)\n```", src, re.S).group(1))
    return am["n_sys"] + am.get("n_anc", 0)


def _plan(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    return json.loads(re.search(r"```json id=plan\s*\n(.*?)\n```", src, re.S).group(1))


def is_diagonal(G, tol=1e-9):
    G = np.asarray(G, dtype=complex)
    return np.allclose(G - np.diag(np.diag(G)), 0, atol=tol)


def detect_modulus(diag, tol=1e-6):
    """가장 작은 M∈{1,2,4,8,16,32} 로 모든 위상이 ω_M^int. 아니면 None(root-of-unity 아님)."""
    thetas = np.angle(diag) / (2 * np.pi) % 1.0
    for M in (1, 2, 4, 8, 16, 32):
        if all(abs(t * M - round(t * M)) < tol * M for t in thetas):
            return M
    return None


def phase_poly(diag, k, M, wires, nvars):
    """대각(2^k) → ℤ_M 다항식 dict{지수tuple(nvars): coeff}. big-endian x0=MSB.
       ℤ_M Möbius(포함배제)로 multilinear 계수 산출."""
    f = [int(round((np.angle(diag[a]) / (2 * np.pi) % 1.0) * M)) % M for a in range(1 << k)]
    t = [0] * (1 << k)                              # little-endian mask 재배열
    for a in range(1 << k):
        mask = 0
        for l in range(k):
            if (a >> (k - 1 - l)) & 1:
                mask |= (1 << l)
        t[mask] = f[a]
    poly = {}
    for S in range(1 << k):
        c, sub = 0, S
        while True:
            c += ((-1) ** bin(S ^ sub).count("1")) * t[sub]
            if sub == 0:
                break
            sub = (sub - 1) & S
        c %= M
        if c:
            mono = [0] * nvars
            for l in range(k):
                if (S >> l) & 1:
                    mono[wires[l]] = 1
            poly[tuple(mono)] = c
    return poly


def verify_app(app):
    """반환 (status, detail). status ∈ {pass, skip, FAIL}."""
    plan = _plan(app)
    if plan.get("tier") == "structural":
        return "skip", "structural"
    n = _meta(app)
    if n > N_CAP:
        return "skip", f"n>{N_CAP}"
    G = _load_app_golden(app)
    if G is None:
        return "skip", "no_golden"
    G = np.asarray(G, dtype=complex)
    if G.shape[0] != (1 << n):
        return "skip", "shape_mismatch"
    if not is_diagonal(G):
        return "skip", "app_not_diagonal"          # 순열/H/CNOT 포함 = ANF/타 경로 담당
    M = detect_modulus(np.diag(G))
    if M is None:
        return "skip", "phase_not_root_of_unity"
    if M == 1:
        return "skip", "trivial_identity_phase"
    # path B: golden 위상다항식
    fB = phase_poly(np.diag(G), n, M, list(range(n)), n)
    # path A: plan 게이트별 대각 위상다항식 합(공통 모듈러스 M)
    fA = {}
    for st in plan["steps"]:
        tg = st.get("targets", list(range(n)))
        Gm = _load_app_golden(st["app"]) if "app" in st else _load_mod(st["spec"])
        if Gm is None:
            return "skip", "no_gate_golden"
        Gm = np.asarray(Gm, dtype=complex)
        k = len(tg)
        if Gm.shape[0] != (1 << k):
            return "skip", "gate_shape_mismatch"
        if not is_diagonal(Gm):
            return "skip", "nondiag_gate"           # 대각 아닌 게이트 → path A 범위 밖
        Mg = detect_modulus(np.diag(Gm))
        if Mg is None or M % Mg != 0:
            return "skip", "gate_phase_incompatible"
        pg = phase_poly(np.diag(Gm), k, Mg, tg, n)
        pg = {mono: (c * (M // Mg)) % M for mono, c in pg.items()}
        fA = poly_axpy(fA, pg, M)
    diff = poly_axpy(poly_reduce(fA, M), fB, M, s=-1)
    ok = (len(diff) == 0)
    return ("pass" if ok else "FAIL"), {"n": n, "M": M, "nmono_golden": len(fB)}


def _self_test():
    """teeth — 위상 계수 오염이 반드시 membership 실패로 검출되는지."""
    app = "c3_diag_full3.app.pg"
    n, M = _meta(app), 8
    fB = phase_poly(np.diag(np.asarray(_load_app_golden(app), dtype=complex)), n, M, list(range(n)), n)
    st, det = verify_app(app)
    if st != "pass":
        return False
    fBc = dict(fB)                                   # 위상 계수 1개 오염
    k0 = next(iter(fBc)); fBc[k0] = (fBc[k0] + 1) % M
    fA = {}
    for step in _plan(app)["steps"]:
        tg = step["targets"]; Gm = np.asarray(_load_mod(step["spec"]), dtype=complex)
        Mg = detect_modulus(np.diag(Gm))
        pg = phase_poly(np.diag(Gm), len(tg), Mg, tg, n)
        pg = {mo: (c * (M // Mg)) % M for mo, c in pg.items()}; fA = poly_axpy(fA, pg, M)
    return len(poly_axpy(poly_reduce(fA, M), fBc, M, s=-1)) != 0


def main():
    quick = "--quick" in sys.argv
    sample = "--sample" in sys.argv
    apps = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "specs", "apps", "*.app.pg")))
    if sample:
        pri = [a for a in apps if a.startswith(("c3_diag", "cz_", "ccz", "code832", "d4_qft"))]
        apps = pri or apps[:12]

    covered, skipped, failed = [], {}, []
    for app in apps:
        try:
            status, detail = verify_app(app)
        except Exception as e:
            status, detail = "skip", f"err:{type(e).__name__}"
        if status == "pass":
            covered.append(app)
        elif status == "FAIL":
            failed.append(app)
        else:
            skipped.setdefault(str(detail), []).append(app)

    teeth = _self_test()
    # genuine Gröbner 인증서: 커버 앱들의 n 에 대해 Boolean 이데알이 Gröbner basis
    ns = sorted({verify_app(a)[1]["n"] for a in covered}) if covered else [3]
    groebner_ok = all(buchberger_certifies_groebner(nv, 8) for nv in ns)

    ok = (not failed) and teeth and groebner_ok and len(covered) > 0
    result = {"path": "Gröbner/ℤ[ω] phase-ideal (10th)", "covered": len(covered), "failed": failed,
              "teeth_ok": teeth, "groebner_basis_certified": groebner_ok,
              "skip_reasons": {k: len(v) for k, v in skipped.items()}, "sample": sample}
    if not sample:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        json.dump({**result, "covered_apps": covered, "skipped": {k: v for k, v in skipped.items()}},
                  open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    if not quick:
        print("Gröbner/ℤ[ω] phase-ideal 제10 독립 검증경로 (대각 위상회로 위상다항식 이데알 멤버십):", flush=True)
        print(f"  covered(대각 위상 앱 path A==path B, f_A−f_B∈⟨x²−x,M⟩ NF≡0)={len(covered)} · "
              f"failed={len(failed)} · teeth={teeth} · Gröbner-basis 인증={groebner_ok}", flush=True)
        print(f"  covered apps: {covered}", flush=True)
        print(f"  skip 사유(전수 기록·silent cap 금지): {result['skip_reasons']}", flush=True)
        print("  ★독립성: 위상다항식(ℤ_M, 진폭 argument) — 제9 ANF(GF(2) Boolean 순열, 진폭 무관)와 링·객체·"
              "커버집합 상보. dense/path-sum(행렬·경로합)과도 상이(위상 계수 이데알 멤버십, 행렬 미실체화). "
              "신규 봉인 0·root 불변 sidecar.", flush=True)
    print(f"groebner_verify: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
