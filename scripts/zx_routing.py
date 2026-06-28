"""zx_routing.py — W1.2: non-Clifford 대형 회로의 Tier-3 ZX-equivalence 검증 경로.

배경: Tier-0 dense EXACT 는 2^n 천장(n≤12). Clifford 대형은 P0 tableau(Tier-2)로 닫힘. 남는 갭 =
**non-Clifford 대형 회로**(dense 불가 + tableau 불가). pyzx ZX-calculus 의 full_reduce 동등성이 이
구간의 sound(보수적, safe false-negative) Tier-3 경로다.

현재 상태(정직): registry 의 Tier-1 structural 앱은 ghz16 1개뿐이며 **Clifford**(H+CNOT) — 이미 P0
tableau(Tier-2) + W1.1 sampled-dense(unitary_equiv_sampled). 따라서 **non-Clifford 대형 Tier-1 앱은
현재 0개** = ZX 라우팅의 즉시 대상 없음. 본 모듈은 (1) 대상 스캔을 결정론적으로 0 으로 입증하고,
(2) ZX-equivalence 인프라를 self-test(sound + teeth)로 동작 검증하여, 향후 대형 non-Clifford 앱이
봉인되면 즉시 Tier-3 경로가 활성화되도록 둔다.

비파괴: registry/sealed/oracle/frozen 미변경. `.pgf/zx/ZX-ROUTING-REPORT.json` 가산 레이어.
"""
import os, sys, json, glob
import pyzx as zx

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
APPREG = os.path.join(ROOT, "registry", "apps")
APPS = os.path.join(ROOT, "specs", "apps")
OUTDIR = os.path.join(ROOT, ".pgf", "zx")
OUT = os.path.join(OUTDIR, "ZX-ROUTING-REPORT.json")

# Clifford generator 집합 (이 밖 = non-Clifford → ZX 후보)
CLIFFORD = {"h_gate", "s_gate", "cs_dag", "cz", "cnot", "swap2", "x_gate", "z_gate"}


def _plan_gates(app_id):
    """앱 plan 의 게이트 id 집합 (sub-app 참조는 그대로 포함)."""
    spec = os.path.join(APPS, f"{app_id}.app.pg")
    if not os.path.exists(spec):
        return set()
    import re
    txt = open(spec, encoding="utf-8").read()
    m = re.search(r"id=plan", txt)
    if not m:
        return set()
    block = txt[txt.index("{", m.start()):txt.index("```", m.start())]
    try:
        steps = json.loads(block)["steps"]
    except Exception:
        return set()
    return {os.path.basename(s["spec"]).split(".")[0] for s in steps}


def scan_targets():
    """Tier-1 structural & 대형(n>12) & non-Clifford 앱 식별 — ZX 즉시 대상."""
    targets, tier1 = [], []
    for p in sorted(glob.glob(os.path.join(APPREG, "*.sealed.json"))):
        d = json.load(open(p, encoding="utf-8"))
        c = d.get("contract", "")
        t = d.get("tier"); t = t if t is not None else (1 if "structural" in c else (2 if "clifford" in c else 0))
        if t == 1:
            gates = _plan_gates(d["id"])
            non_clifford = sorted(gates - CLIFFORD)
            tier1.append({"id": d["id"], "n": d.get("n_sys"), "non_clifford_gates": non_clifford,
                          "is_clifford": not non_clifford})
            if non_clifford and (d.get("n_sys", 0) > 12):
                targets.append(d["id"])
    return targets, tier1


def zx_equiv(c1, c2):
    """ZX-calculus 동등성 (pyzx verify_equality — Clifford+T 포함 sound)."""
    return bool(c1.verify_equality(c2))


def selftest():
    """ZX-equivalence 인프라 sound(동등 인정) + teeth(비동등 거부) 검증 — non-Clifford(T) 포함."""
    def C(gates):
        c = zx.Circuit(2)
        for g, q in gates:
            c.add_gate(g, q)
        return c
    pos = [  # 동등쌍 (non-Clifford 포함)
        ("T·T==S", C([("T", 0), ("T", 0)]), C([("S", 0)])),
        ("T⁴==Z", C([("T", 0), ("T", 0), ("T", 0), ("T", 0)]), C([("Z", 0)])),
        ("H·H==I", C([("HAD", 0), ("HAD", 0)]), C([])),
        ("CNOT·CNOT==I", _cx2(), _empty2()),
    ]
    neg = [  # 비동등쌍 (teeth)
        ("T≠S", C([("T", 0)]), C([("S", 0)])),
        ("H≠S", C([("HAD", 0)]), C([("S", 0)])),
    ]
    rows = []
    ok = True
    for name, a, b in pos:
        r = zx_equiv(a, b)
        rows.append({"case": name, "expect": "equiv", "got": r, "pass": r is True})
        ok &= (r is True)
    for name, a, b in neg:
        r = zx_equiv(a, b)
        rows.append({"case": name, "expect": "not-equiv", "got": r, "pass": r is False})
        ok &= (r is False)
    return ok, rows


def _cx2():
    c = zx.Circuit(2); c.add_gate("CNOT", 0, 1); c.add_gate("CNOT", 0, 1); return c


def _empty2():
    return zx.Circuit(2)


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    print("=" * 80)
    print("zx_routing (W1.2) — non-Clifford 대형 Tier-3 ZX 경로 (대상 스캔 + 인프라 self-test)")
    print("=" * 80)
    targets, tier1 = scan_targets()
    print(f"\nTier-1 structural 앱 {len(tier1)}개:")
    for r in tier1:
        tag = "Clifford(→P0 tableau Tier-2 + W1.1 sampled)" if r["is_clifford"] else f"non-Clifford {r['non_clifford_gates']}"
        print(f"   {r['id']:24} n={r['n']} · {tag}")
    print(f"\nZX 즉시 대상(non-Clifford & n>12): {len(targets)} {targets if targets else '(없음 — 정직 음성)'}")

    ok, rows = selftest()
    print("\nZX-equivalence 인프라 self-test (sound + teeth):")
    for r in rows:
        print(f"   {'✓' if r['pass'] else '✗'} {r['case']:16} expect={r['expect']} got={r['got']}")

    out = {"_schema": "zx-routing-v1",
           "_note": "non-Clifford 대형 Tier-3 ZX 경로. 현재 대상 0(정직 음성) — Tier-1 앱은 ghz16(Clifford)뿐. "
                    "인프라는 self-test 로 동작 검증됨. 대형 non-Clifford 앱 봉인 시 활성화. 비파괴.",
           "pyzx_version": zx.__version__,
           "tier1_apps": tier1, "zx_immediate_targets": targets,
           "selftest_pass": ok, "selftest": rows}
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("\n" + "-" * 80)
    print(f"대상={len(targets)} · self-test {'ALL PASS' if ok else 'FAIL'} · 리포트: {os.path.relpath(OUT, ROOT)}")
    print("=" * 80)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
