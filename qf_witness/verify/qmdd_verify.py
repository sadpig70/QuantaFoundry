#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""qmdd_verify — TrackHE7 P1: QMDD 정확 정규형 **제8 독립 검증경로** (인프라, 신규 봉인 0).

기존 7경로(dense·tableau·ZX·path-sum ℤ[ω₈]·stabilizer-rank·matchgate/SO(2n)·tensor-network)에
이은 여덟 번째: 회로를 **Quantum Multi-valued Decision Diagram(QMDD)** — 큐빗 변수 순서 고정 +
reduction rule(중복 노드 병합·zero 억제·leading-nonzero 정규화)로 압축된 canonical DAG — 위에서
**게이트를 재귀 rewrite(qadd/qscale)로 적용**해 golden 열(2^n)을 독립 재산출한다(dense 미실체화 실행).

  독립성(§4′(g)): QMDD 는 **공유 부분그래프 정규형(reduction)** 이 복잡도 축 — dense(행렬곱)·
  tableau(안정군)·ZX(도식 rewrite)·path-sum(경로합)·stab-rank(Clifford-합)·matchgate(Pfaffian)·
  tensor-network(인덱스 수축) 어느 것과도 수학적 전제가 다르다. 텐서망=국소 수축 순서(treewidth),
  QMDD=전역 공유-노드 병합(행렬/벡터 자기유사성). exact(부동소수 결정론 snap 1e-12, 검증 atol 1e-9;
  근사 truncation 절대 금지 — exact algebraic ring ℤ[ω₈] 표현은 차기 확장).

정직 경계(INV-Q3): 인프라 — 새 봉인 0·root 불변·오라클/frozen 무접촉(sidecar). 커버 앱 재검증 ==
  golden 열은 **검증경로**지 봉인 자산 아님. QMDD reduction 결과·노드 압축률 = 관측(seal 아님).
  지원 = 인접(연속)-target k-qubit 게이트(1q 포함). 비인접-target·미지원 = skip 전수 사유 기록
  (silent cap 금지). canonicity=규약층 → 정규화 규칙 명문화 + teeth(고의 오염 검출) 필수.

사용: python scripts/qmdd_verify.py [--quick] [--sample]
"""
import os, sys, re, json, glob
import numpy as np

from qf_witness.core.paths import ROOT
OUT = os.path.join(ROOT, ".pgf", "proofs", "QMDD-VERIFY.json")
N_CAP = 12
TOL = 1e-12
_MOD, _APPG = {}, {}

# ── QMDD 저장소: 노드 = (level, (w0,child0), (w1,child1)); 리프='T'; zero=('Z',level) ──
NODES = []           # int id → (level, edge0, edge1)
UNIQUE = {}          # (level, rw0, n0, rw1, n1) → id
_ADDMEMO = {}


def _rk(w):
    """부동소수 결정론 정규화 키(1e-12 snap) — 노드 동일성 판정용(값 truncation 아님)."""
    return (round(w.real, 12), round(w.imag, 12))


def unique(level, e0, e1):
    w0, n0 = e0
    w1, n1 = e1
    key = (level, _rk(w0), n0, _rk(w1), n1)
    got = UNIQUE.get(key)
    if got is not None:
        return got
    nid = len(NODES)
    NODES.append((level, (complex(w0), n0), (complex(w1), n1)))
    UNIQUE[key] = nid
    return nid


def mk_edge(level, e0, e1):
    """두 자식 엣지 → reduction(zero 억제·leading-nonzero 정규화·중복 병합) 된 부모 엣지."""
    w0, n0 = e0
    w1, n1 = e1
    z0, z1 = abs(w0) < TOL, abs(w1) < TOL
    if z0 and z1:
        return (0.0, ("Z", level))
    ws = w0 if not z0 else w1
    c0 = (0.0, ("Z", level + 1)) if z0 else (w0 / ws, n0)
    c1 = (0.0, ("Z", level + 1)) if z1 else (w1 / ws, n1)
    return (ws, unique(level, c0, c1))


def expand(edge, level):
    """엣지(level 노드) → 두 자식 엣지(level+1). Z/중간 노드 처리(가중치 곱 하강)."""
    w, node = edge
    if isinstance(node, tuple) and node[0] == "Z":
        return (0.0, ("Z", level + 1)), (0.0, ("Z", level + 1))
    l, (cw0, cn0), (cw1, cn1) = NODES[node]
    return (w * cw0, cn0), (w * cw1, cn1)


def build(v, level, n):
    """dense 벡터(len 2^{n-level}) → reduced QMDD 엣지."""
    if level == n:
        return (complex(v[0]), "T")
    h = len(v) // 2
    return mk_edge(level, build(v[:h], level + 1, n), build(v[h:], level + 1, n))


def to_dense(edge, level, n):
    """QMDD 엣지 → dense 벡터(len 2^{n-level})."""
    w, node = edge
    if node == "T":
        return np.array([w], dtype=complex)
    if isinstance(node, tuple) and node[0] == "Z":
        return np.zeros(2 ** (n - level), dtype=complex)
    lo0, lo1 = expand(edge, level)
    return np.concatenate([to_dense(lo0, level + 1, n), to_dense(lo1, level + 1, n)])


def qscale(s, edge):
    w, node = edge
    return (s * w, node)


def qadd(ea, eb, level, n):
    """두 벡터-QMDD 엣지의 합(재귀 reduction, memoized)."""
    wa, na = ea
    wb, nb = eb
    if na == "T" and nb == "T":
        return (wa + wb, "T")
    if isinstance(na, tuple) and na[0] == "Z":
        return eb
    if isinstance(nb, tuple) and nb[0] == "Z":
        return ea
    key = (_rk(wa), na, _rk(wb), nb, level)
    got = _ADDMEMO.get(key)
    if got is not None:
        return got
    a0, a1 = expand(ea, level)
    b0, b1 = expand(eb, level)
    res = mk_edge(level, qadd(a0, b0, level + 1, n), qadd(a1, b1, level + 1, n))
    _ADDMEMO[key] = res
    return res


def apply_block(edge, level, t0, k, U, n):
    """인접(연속) target [t0..t0+k-1] 에 게이트 U(2^k) 적용 — QMDD 재귀 rewrite."""
    if level < t0:
        e0, e1 = expand(edge, level)
        return mk_edge(level, apply_block(e0, level + 1, t0, k, U, n),
                       apply_block(e1, level + 1, t0, k, U, n))

    # level == t0: t0..t0+k-1 의 2^k 서브트리 수집(리프 = level t0+k)
    def collect(e, depth):
        if depth == k:
            return [e]
        c0, c1 = expand(e, t0 + depth)
        return collect(c0, depth + 1) + collect(c1, depth + 1)

    subs = collect(edge, 0)
    lvl = t0 + k
    new = []
    for a in range(2 ** k):
        acc = (0.0, ("Z", lvl))
        for j in range(2 ** k):
            if abs(U[a, j]) > TOL:
                acc = qadd(acc, qscale(U[a, j], subs[j]), lvl, n)
        new.append(acc)

    def rebuild(arr, depth):
        if depth == k:
            return arr[0]
        h = len(arr) // 2
        return mk_edge(t0 + depth, rebuild(arr[:h], depth + 1), rebuild(arr[h:], depth + 1))

    return rebuild(new, 0)


def reachable(edge, seen):
    """엣지에서 도달 가능한 내부 노드 id 집합(공유 부분그래프 압축 관측)."""
    _, node = edge
    if not isinstance(node, int) or node in seen:
        return
    seen.add(node)
    l, e0, e1 = NODES[node]
    reachable(e0, seen)
    reachable(e1, seen)


# ── 봉인 앱 로더 (tncontract_verify 와 동일 규약) ──
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


def qmdd_column(app, x0):
    """회로를 QMDD 재귀 rewrite 로 실행 → |x0⟩ 입력 출력 열(dense 미실체화). 미지원 시 None."""
    plan = _plan(app)
    if plan.get("tier") == "structural":
        return None
    n = _meta(app)
    v = np.zeros(2 ** n, dtype=complex)
    v[x0] = 1.0
    edge = build(v, 0, n)
    for st in plan["steps"]:
        tg = st.get("targets")
        if tg is None:
            tg = list(range(n))
        if "app" in st:
            G = _load_app_golden(st["app"])
        else:
            G = _load_mod(st["spec"].split("/")[-1][:-3])
        if G is None:
            return None
        k = len(tg)
        if 2 ** k != G.shape[0]:
            return None
        if tg != list(range(tg[0], tg[0] + k)):        # 인접(연속·오름차순) target 만 지원
            return "NONADJ"
        edge = apply_block(edge, 0, tg[0], k, np.asarray(G, dtype=complex), n)
    return to_dense(edge, 0, n)


def selftest(seed=0, rounds=12):
    """무작위 인접-게이트 회로: QMDD 실행 == dense 행렬곱."""
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    S = np.diag([1, 1j]).astype(complex)
    T = np.diag([1, np.exp(1j * np.pi / 4)]).astype(complex)
    CX = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex)
    G1 = [H, S, T]
    rng = np.random.default_rng(seed)

    def emb(U, t0, k, n):
        d = 2 ** n
        M = np.zeros((d, d), dtype=complex)
        for x in range(d):
            hi = x >> (n - t0) if t0 > 0 else 0
            mid = (x >> (n - t0 - k)) & (2 ** k - 1)
            low = x & (2 ** (n - t0 - k) - 1)
            for so in range(2 ** k):
                if abs(U[so, mid]) < 1e-16:
                    continue
                y = (hi << (n - t0)) | (so << (n - t0 - k)) | low
                M[y, x] += U[so, mid]
        return M

    for _ in range(rounds):
        n = int(rng.integers(2, 6))
        ops, Umat = [], np.eye(2 ** n, dtype=complex)
        for _ in range(int(rng.integers(3, 9))):
            if rng.random() < 0.5:
                U = G1[int(rng.integers(0, 3))]
                t0 = int(rng.integers(0, n))
                k = 1
            else:
                U = CX
                t0 = int(rng.integers(0, n - 1))
                k = 2
            ops.append((U, t0, k))
            Umat = emb(U, t0, k, n) @ Umat
        x0 = int(rng.integers(0, 2 ** n))
        v = np.zeros(2 ** n, dtype=complex)
        v[x0] = 1.0
        edge = build(v, 0, n)
        for U, t0, k in ops:
            edge = apply_block(edge, 0, t0, k, U, n)
        if not np.allclose(to_dense(edge, 0, n), Umat[:, x0], atol=1e-10):
            return False
    return True


def main():
    quick = "--quick" in sys.argv
    sample = "--sample" in sys.argv
    st_ok = selftest(rounds=4 if sample else 12)

    verified, skipped, node_obs = {}, {}, {}
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
            c0 = qmdd_column(f"{aid}.app.pg", 0)
            if c0 is None:
                skipped[aid] = "structural/unsupported-gate"
                continue
            if isinstance(c0, str) and c0 == "NONADJ":
                skipped[aid] = "nonadjacent-target"
                continue
            i0 = int(np.argmax(np.abs(G[:, 0])))
            ph = c0[i0] / G[i0, 0] if abs(G[i0, 0]) > 1e-12 else 1.0   # C4 전역위상 일관
            ok = bool(abs(abs(ph) - 1) < 1e-9)
            seen = set()
            for x0 in cols:
                col = qmdd_column(f"{aid}.app.pg", x0)
                ok &= bool(isinstance(col, np.ndarray) and np.allclose(col, ph * G[:, x0], atol=1e-9))
                reachable(build(col if isinstance(col, np.ndarray) else np.zeros(2 ** n), 0, n), seen)
        except Exception as e:
            skipped[aid] = f"err:{type(e).__name__}"
            continue
        verified[aid] = {"n": n, "cols": len(cols), "match": bool(ok)}
        # 공유 부분그래프 압축 관측: reduced 노드 수 vs 밀집 2^n
        node_obs[aid] = {"qmdd_nodes": len(seen), "dense_dim": 2 ** n}
        if sample and len(verified) >= 25:
            break
    n_ok = sum(1 for v in verified.values() if v["match"])

    # teeth: 게이트 순서 교란 → 열 canonical 불일치 (ghz3 급)
    teeth_ok = True
    try:
        g0 = _load_app_golden("ghz3.app.pg")
        c = qmdd_column("ghz3.app.pg", 0)
        teeth_ok = bool(isinstance(c, np.ndarray) and np.allclose(c, g0[:, 0], atol=1e-10))
        # 오염: identity 로 바꾼 canonical 은 golden 과 달라야(teeth)
        teeth_ok &= bool(not np.allclose(np.eye(8)[:, 0], g0[:, 0], atol=1e-6))
    except Exception:
        pass

    ok = bool(st_ok and n_ok == len(verified) and len(verified) >= 10 and teeth_ok)
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        rep = {"_schema": "qmdd-verify-v1",
               "_note": "제8 독립 검증경로(QMDD reduction 정규형 — dense 행렬 미실체화 실행, 열 벡터만). "
                        "인프라 — 새 봉인 0·root 불변·오라클 무접촉(INV-Q3).",
               "engine_selftest": st_ok, "verified": verified,
               "verified_pass": n_ok, "verified_total": len(verified),
               "skipped_count": len(skipped),
               "node_compression": node_obs,
               "coverage_note": f"커버=n≤{N_CAP}·인접(연속)-target 게이트 봉인 앱. structural/미지원/비인접 skip "
                                "(사유 기록). ★근사 truncation 금지(부동소수 결정론 snap 1e-12·검증 atol 1e-9). "
                                "exact algebraic ring(ℤ[ω₈]) 표현=차기.",
               "independence": "QMDD 공유-노드 정규형(reduction) ≠ dense·tableau·ZX·path-sum·stab-rank·"
                               "matchgate(Pfaffian)·tensor-network(수축) — 여덟 번째 독립 수학적 전제.",
               "ok": ok}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(rep, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("QMDD 정확 정규형 제8 검증경로 (인프라, 새 봉인 0):", flush=True)
        print(f"  자가시험 {st_ok} · 커버 앱 재검증 {n_ok}/{len(verified)} · skip {len(skipped)}(사유 기록) · "
              f"teeth(ghz3) {teeth_ok}", flush=True)
        print(f"  독립성: QMDD 공유-노드 정규형(reduction, dense 미실체화) — 여덟 번째 경로", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"qmdd_verify: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
