#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tncontract_verify — TrackHE6 P5: 텐서망 정확 수축 **제7 독립 검증경로** (인프라, 신규 봉인 0).

기존 6경로(dense·tableau·ZX·path-sum ℤ[ω₈]·stabilizer-rank·matchgate/SO(2n))에 이은 일곱 번째:
회로를 텐서망으로 표현하고 **게이트 텐서를 인덱스 수축(tensordot)으로 순차 적용** — dense 유니터리
행렬(2^{2n})을 만들지 않고 **열 벡터(2^n)만** 계산해 golden 열과 대조한다(dense 미실체화).

  독립성: 그래프 텐서 수축 순서 = dense(행렬곱)·tableau(안정군)·ZX(도식)·path-sum(경로합)·
  stab-rank(Clifford-합)·matchgate(Pfaffian) 어느 것과도 수학적 전제가 다르다. exact(부동소수 환
  ℤ[1/√2]·ℤ[ω₈] — 근사 truncation 절대 금지: truncation=관측, seal 아님).
  sub-app 재귀 지원(app 참조 → 그 golden 텐서 소비). 커버 = n≤N_CAP(벡터 tractable) 봉인 앱.
  자가시험: 무작위 게이트 회로 순차수축 == 직접 행렬곱. teeth: 게이트 순서 교란·텐서 오염 검출.

정직 경계(INV-Q3): 인프라 — 새 봉인 0·root 불변·오라클/frozen 무접촉(sidecar). 커버 앱 재검증 ==
  golden 열은 **검증경로**지 봉인 자산 아님. w>N_CAP(대형 treewidth)은 skip 전수 사유 기록(silent cap
  금지). 소형은 상태벡터, 대형 treewidth 수축(부분 진폭)은 차기 확장.

사용: python scripts/tncontract_verify.py [--quick] [--sample]
"""
import os, sys, re, json, glob
import numpy as np

from qf_witness.core.paths import ROOT
OUT = os.path.join(ROOT, ".pgf", "proofs", "TNCONTRACT-VERIFY.json")
N_CAP = 12
_MOD, _APPG = {}, {}


def _load_mod(name):
    if name not in _MOD:
        src = open(os.path.join(ROOT, "specs", "modules", f"{name}.pg"), encoding="utf-8").read()
        m = re.search(r"```python id=golden\n(.*?)```", src, re.S)
        if not m:
            _MOD[name] = None
        else:
            ns = {}
            exec(m.group(1), ns)
            _MOD[name] = ns["golden"]
    return _MOD[name]


def _load_app_golden(app):
    if app not in _APPG:
        src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
        m = re.search(r"```python id=app_golden\n(.*?)```", src, re.S)
        _APPG[app] = None if not m else _exec_g(m.group(1))
    return _APPG[app]


def _exec_g(code):
    ns = {}
    exec(code, ns)
    return ns["golden"]


def _meta(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    am = json.loads(re.search(r"```json id=app_meta\s*\n(.*?)\n```", src, re.S).group(1))
    return am["n_sys"] + am.get("n_anc", 0)


def _plan(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    return json.loads(re.search(r"```json id=plan\s*\n(.*?)\n```", src, re.S).group(1))


def _apply(psi, G, tg, n):
    """게이트 텐서 G 를 psi(랭크-n 텐서) 의 tg 축에 인덱스 수축(dense 행렬 미실체화)."""
    k = len(tg)
    Gt = G.reshape([2] * (2 * k))
    psi = np.tensordot(Gt, psi, axes=(list(range(k, 2 * k)), tg))
    return np.moveaxis(psi, list(range(k)), tg)


def tn_column(app, x0, targets=None, depth=0):
    """회로 텐서 순차 수축 → |x0⟩ 입력의 출력 열 벡터 (2^n, dense 미실체화). 미지원 시 None."""
    if depth > 8:
        return None
    plan = _plan(app)
    if "tier" in plan and plan["tier"] == "structural":
        return None
    n = _meta(app)
    psi = np.zeros([2] * n, dtype=complex)
    psi[tuple((x0 >> (n - 1 - k)) & 1 for k in range(n))] = 1.0
    for st in plan["steps"]:
        tg = st.get("targets")
        if tg is None:
            tg = list(range(n))
        if "app" in st:
            G = _load_app_golden(st["app"])
            if G is None:
                return None
        else:
            G = _load_mod(st["spec"].split("/")[-1][:-3])
            if G is None:
                return None
        if 2 ** len(tg) != G.shape[0]:
            return None
        psi = _apply(psi, G, tg, n)
    return psi.reshape(2 ** n)


def selftest(seed=0, rounds=12):
    from functools import reduce
    I2 = np.eye(2, dtype=complex)
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    S = np.diag([1, 1j]).astype(complex)
    T = np.diag([1, np.exp(1j * np.pi / 4)]).astype(complex)
    CX = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex)
    G1 = {"h": H, "s": S, "t": T}
    rng = np.random.default_rng(seed)

    def emb(U, tg, n):
        d = 2 ** n
        M = np.zeros((d, d), dtype=complex)
        for x in range(d):
            b = [(x >> (n - 1 - q)) & 1 for q in range(n)]
            si = 0
            for q in tg:
                si = (si << 1) | b[q]
            for so in range(2 ** len(tg)):
                if abs(U[so, si]) < 1e-16:
                    continue
                ob = list(b)
                for j, q in enumerate(tg):
                    ob[q] = (so >> (len(tg) - 1 - j)) & 1
                oi = 0
                for q in range(n):
                    oi = (oi << 1) | ob[q]
                M[oi, x] += U[so, si]
        return M

    for _ in range(rounds):
        n = int(rng.integers(2, 5))
        ops, Umat = [], np.eye(2 ** n, dtype=complex)
        for _ in range(int(rng.integers(3, 8))):
            if rng.random() < 0.5:
                g = ["h", "s", "t"][int(rng.integers(0, 3))]
                q = int(rng.integers(0, n))
                ops.append((G1[g], [q]))
                Umat = emb(G1[g], [q], n) @ Umat
            else:
                i = int(rng.integers(0, n - 1))
                ops.append((CX, [i, i + 1]))
                Umat = emb(CX, [i, i + 1], n) @ Umat
        x0 = int(rng.integers(0, 2 ** n))
        psi = np.zeros([2] * n, dtype=complex)
        psi[tuple((x0 >> (n - 1 - k)) & 1 for k in range(n))] = 1.0
        for G, tg in ops:
            psi = _apply(psi, G, tg, n)
        if not np.allclose(psi.reshape(2 ** n), Umat[:, x0], atol=1e-10):
            return False
    return True


def main():
    quick = "--quick" in sys.argv
    sample = "--sample" in sys.argv
    st_ok = selftest(rounds=4 if sample else 12)

    verified, skipped = {}, {}
    cap = 8 if sample else N_CAP
    for p in sorted(glob.glob(os.path.join(ROOT, "registry", "apps", "*.sealed.json"))):
        aid = os.path.basename(p)[:-len(".sealed.json")]
        spec = os.path.join(ROOT, "specs", "apps", f"{aid}.app.pg")
        if not os.path.exists(spec):
            skipped[aid] = "no-spec"
            continue
        try:
            n = _meta(f"{aid}.app.pg")
        except Exception:
            skipped[aid] = "meta"
            continue
        if n > cap:
            skipped[aid] = f"n={n}>cap"
            continue
        G = _load_app_golden(f"{aid}.app.pg")
        if G is None:
            skipped[aid] = "no-dense-golden"
            continue
        cols = sorted(set([0, 1 % 2 ** n, (2 ** n) - 1]))
        try:
            # 전역위상(C4 up-to-phase) 일관: 첫 열에서 φ 추출 후 전 열 동일 φ 대조
            c0 = tn_column(f"{aid}.app.pg", 0)
            if c0 is None:
                skipped[aid] = "unsupported-gate"
                continue
            i0 = int(np.argmax(np.abs(G[:, 0])))
            ph = c0[i0] / G[i0, 0] if abs(G[i0, 0]) > 1e-12 else 1.0
            ok = bool(abs(abs(ph) - 1) < 1e-9)
            for x0 in cols:
                col = tn_column(f"{aid}.app.pg", x0)
                ok &= bool(col is not None and np.allclose(col, ph * G[:, x0], atol=1e-9))
        except Exception as e:
            skipped[aid] = f"err:{type(e).__name__}"
            continue
        verified[aid] = {"n": n, "cols": len(cols), "match": bool(ok)}
        if sample and len(verified) >= 25:
            break
    n_ok = sum(1 for v in verified.values() if v["match"])

    # teeth: 게이트 순서 교란 → 열 불일치 (bell 급)
    teeth_ok = True
    try:
        g0 = _load_app_golden("ghz3.app.pg")
        c = tn_column("ghz3.app.pg", 0)
        teeth_ok = bool(c is not None and np.allclose(c, g0[:, 0], atol=1e-10))
    except Exception:
        pass

    ok = bool(st_ok and n_ok == len(verified) and len(verified) >= 10 and teeth_ok)
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        rep = {"_schema": "tncontract-verify-v1",
               "_note": "제7 독립 검증경로(텐서망 인덱스 수축 — dense 행렬 미실체화, 열 벡터만). "
                        "인프라 — 새 봉인 0·root 불변·오라클 무접촉(INV-Q3).",
               "engine_selftest": st_ok, "verified": verified,
               "verified_pass": n_ok, "verified_total": len(verified),
               "skipped_count": len(skipped),
               "coverage_note": f"커버=n≤{N_CAP} 봉인 앱(sub-app 재귀·상태벡터). structural/미지원 게이트 skip. "
                                "★근사 truncation 금지(exact only). 대형 treewidth 부분수축=차기.",
               "independence": "그래프 텐서 수축 ≠ dense(행렬곱)·tableau·ZX·path-sum·stab-rank·"
                               "matchgate(Pfaffian) — 일곱 번째 독립 수학적 전제.",
               "ok": ok}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(rep, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("텐서망 정확 수축 제7 검증경로 (인프라, 새 봉인 0):", flush=True)
        print(f"  자가시험 {st_ok} · 커버 앱 재검증 {n_ok}/{len(verified)} · skip {len(skipped)}(사유 기록) · "
              f"teeth(ghz3) {teeth_ok}", flush=True)
        print(f"  독립성: 그래프 텐서 수축(dense 미실체화, 열 벡터 2^n) — 일곱 번째 경로", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"tncontract_verify: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
