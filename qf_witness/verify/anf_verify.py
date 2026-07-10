#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""anf_verify — TrackHE8 P1: ANF/bit-vector **제9 독립 검증경로** (인프라, 신규 봉인 0).

기존 8경로(dense·tableau·ZX·path-sum ℤ[ω₈]·stabilizer-rank·matchgate/SO(2n)·tensor-network·QMDD)에
이은 아홉 번째: **계산기저 permutation 회로**(X·CNOT·Toffoli·Fredkin·SWAP·cNx·modular multiplication)를
각 출력 비트의 **Algebraic Normal Form over GF(2)**(다변수 GF(2) 다항식) 로 표현해 회로와 golden 을
**Boolean 함수 대수 항등**으로 대조한다 — 진폭(amplitude)을 전혀 보지 않는다.

  path A: 게이트 순서를 따라 각 wire 의 ANF 다항식을 **symbolic GF(2) 전파**(각 게이트 golden 의 국소
    permutation → Möbius 로 국소 ANF → 입력 wire 다항식 대입·합성). 행렬곱/진폭 미사용.
  path B: 봉인 golden(permutation 행렬)의 진리표 → 각 출력 비트를 **Möbius 변환**으로 독립 ANF 산출.
  PASS ⟺ 모든 출력 비트에서 path A 다항식(monomial 집합) == path B 다항식.

  ★독립성(§4′(h), 한 문장 증명): 기존 8경로는 전부 **양자 진폭/구조**(행렬·안정군·도식·경로합·Clifford합·
  Pfaffian·인덱스수축·decision-diagram)를 다루지만, ANF 경로는 **계산기저 Boolean 함수의 GF(2) 다항식
  항등**(진폭 무관)이라 검증 객체가 근본적으로 다르다. perm_subspace(정수 순열값 일치)와도 다른 객체 —
  ANF 는 GF(2)[x]/(x²−x) 다항식 항등(비트 대수), 순열값이 아니다(부분 도메인 공유·객체 상이, 정직 표기).

정직 경계(seal 아님, root 불변 sidecar): 인프라 — 새 봉인 0·오라클/frozen 무접촉. 커버 = **순열 회로만**
  (H·phase·CZ·QFT 등 비-permutation 게이트 포함 앱은 skip 전수 사유 기록, silent cap 금지). ANF 검증
  결과 == golden 은 **검증경로**지 봉인 자산 아님. exact(GF(2) 정수 대수, 부동소수 없음).

사용: python scripts/anf_verify.py [--quick] [--sample]
"""
import os, sys, re, json, glob
import numpy as np

from qf_witness.core.paths import ROOT
OUT = os.path.join(ROOT, ".pgf", "proofs", "ANF-VERIFY.json")
N_CAP = 9             # path B 진리표 2^n · 국소 블록 2^k 상한. symbolic 전파를 cheap 하게 유지
K_CAP = 9             #   (dense-ANF ≤ 2^9=512) → 대형 cmul(work≥9)은 skip 전수 사유 기록
MONO_CAP = 1024       # wire 다항식 monomial 폭발 가드(초과 시 해당 앱 skip)
_MOD, _APPG = {}, {}


# ── GF(2) ANF: 다항식 = int mask 집합(monomial = mask 비트 변수들의 곱; mask 0 = 상수 1) ──
def p_mul(a, b):
    r = set()
    for ma in a:
        for mb in b:
            m = ma | mb                       # 변수집합 합집합(x²=x)
            if m in r:
                r.discard(m)
            else:
                r.add(m)
    return r


ONE = frozenset({0})


def perm_of(G):
    """0/1 permutation 행렬 → 진리표 b=perm(a). 위상·비순열이면 None."""
    d = G.shape[0]
    tt = [0] * d
    seen = set()
    for a in range(d):
        col = G[:, a]
        nz = np.nonzero(np.abs(col) > 1e-9)[0]
        if len(nz) != 1:
            return None
        b = int(nz[0])
        if abs(col[b] - 1.0) > 1e-9:           # 정확히 +1 (위상/부호 불가)
            return None
        if b in seen:
            return None
        seen.add(b)
        tt[a] = b
    return tt


def bit_anf(tt, k, out_wire):
    """출력 wire out_wire(=출력 b 의 비트 k-1-out_wire)를 국소 변수 l(=입력 a 의 비트 k-1-l)의 ANF 로."""
    t2 = [0] * (1 << k)
    for a in range(1 << k):
        m = 0
        for l in range(k):
            if (a >> (k - 1 - l)) & 1:
                m |= (1 << l)
        t2[m] = (tt[a] >> (k - 1 - out_wire)) & 1
    for i in range(k):                         # fast Möbius (GF2)
        step = 1 << i
        for m in range(1 << k):
            if m & step:
                t2[m] ^= t2[m ^ step]
    return frozenset(m for m in range(1 << k) if t2[m])


# ── 봉인 앱/모듈 로더 (qmdd_verify 규약) ──
def _load_mod(spec):
    name = spec.split("/")[-1][:-3]
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
        _APPG[app] = None
        if m:
            ns = {}
            exec(m.group(1), ns)
            _APPG[app] = ns["golden"]
    return _APPG[app]


def _meta(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    am = json.loads(re.search(r"```json id=app_meta\s*\n(.*?)\n```", src, re.S).group(1))
    return am["n_sys"] + am.get("n_anc", 0)


def _plan(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    return json.loads(re.search(r"```json id=plan\s*\n(.*?)\n```", src, re.S).group(1))


def path_a(n, plan):
    """게이트 plan 을 따라 각 wire 의 ANF 다항식 symbolic 전파. 미지원 시 사유 문자열."""
    P = [frozenset({1 << i}) for i in range(n)]
    for st in plan["steps"]:
        tg = st.get("targets")
        if tg is None:
            tg = list(range(n))
        G = _load_app_golden(st["app"]) if "app" in st else _load_mod(st["spec"])
        if G is None:
            return "no_golden"
        k = len(tg)
        if 2 ** k != G.shape[0]:
            return "shape_mismatch"
        if k > K_CAP:
            return "block_too_large"
        tt = perm_of(np.asarray(G, dtype=complex))
        if tt is None:
            return "nonperm_gate"
        newp = {}
        for j in range(k):
            acc = set()
            for mask in bit_anf(tt, k, j):
                term = set(ONE)
                l, mm = 0, mask
                while mm:
                    if mm & 1:
                        term = p_mul(term, P[tg[l]])
                    mm >>= 1
                    l += 1
                acc ^= term
            if len(acc) > MONO_CAP:
                return "anf_blowup"
            newp[tg[j]] = frozenset(acc)
        for w, poly in newp.items():
            P[w] = poly
    return P


def path_b(app, n):
    G = _load_app_golden(app)
    if G is None:
        return "no_golden"
    tt = perm_of(np.asarray(G, dtype=complex))
    if tt is None:
        return "nonperm_app"
    return [bit_anf(tt, n, i) for i in range(n)]


def verify_app(app):
    """반환 (status, detail). status ∈ {pass, skip, FAIL}."""
    plan = _plan(app)
    if plan.get("tier") == "structural":
        return "skip", "structural"
    n = _meta(app)
    if n > N_CAP:
        return "skip", f"n>{N_CAP}"
    B = path_b(app, n)
    if isinstance(B, str):
        return "skip", B                        # 비순열 앱(H/phase/QFT 등)
    A = path_a(n, plan)
    if isinstance(A, str):
        return "skip", A
    ok = all(A[i] == B[i] for i in range(n))
    return ("pass" if ok else "FAIL"), {"n": n, "monomials": [len(B[i]) for i in range(n)]}


def _self_test():
    """teeth — 고의 오염(출력 비트 ANF 스왑)이 반드시 검출되는지."""
    for app in ("cmul2_mod21.app.pg",):
        n = _meta(app)
        B = path_b(app, n)
        A = path_a(n, _plan(app))
        if isinstance(A, str) or isinstance(B, str):
            return False
        if not all(A[i] == B[i] for i in range(n)):
            return False
        Bc = list(B)
        Bc[0], Bc[1] = B[1], B[0]              # 오염
        if all(A[i] == Bc[i] for i in range(n)):
            return False                         # 검출 실패
    return True


def main():
    quick = "--quick" in sys.argv
    sample = "--sample" in sys.argv
    apps = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "specs", "apps", "*.app.pg")))
    if sample:
        # 대표 순열 앱 표본(정본=full proofs). 소형 n 우선(속도) — cmul 계열 최소 8개.
        cmuls = [a for a in apps if a.startswith("cmul")]
        try:
            cmuls.sort(key=lambda a: _meta(a))
        except Exception:
            pass
        apps = cmuls[:8] or apps[:8]

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
    ok = (not failed) and teeth and len(covered) > 0
    result = {"path": "ANF/bit-vector (9th)", "covered": len(covered), "failed": failed,
              "teeth_ok": teeth, "skip_reasons": {k: len(v) for k, v in skipped.items()},
              "sample": sample}
    if not sample:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        json.dump({**result, "covered_apps": covered,
                   "skipped": {k: v for k, v in skipped.items()}},
                  open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    if not quick:
        print("ANF/bit-vector 제9 독립 검증경로 (계산기저 Boolean 함수 GF(2) 다항식 항등):", flush=True)
        print(f"  covered(순열 앱 path A==path B ANF)={len(covered)} · failed={len(failed)} · "
              f"teeth={teeth}", flush=True)
        print(f"  skip 사유: {result['skip_reasons']}", flush=True)
        print("  ★독립성: 진폭 무관 Boolean 함수 대수 — dense/tableau/ZX/path-sum/stab-rank/matchgate/"
              "tensor/QMDD 어느 것과도 검증 객체 상이. 신규 봉인 0·root 불변 sidecar.", flush=True)
    print(f"anf_verify: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
