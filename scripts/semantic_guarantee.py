"""semantic_guarantee.py — Tier 별 봉인 의미(semantic_guarantee) 비파괴 레이어 + ghz16 부분검증 (R-K).

리뷰 R-K: Tier-1(STRUCTURAL) 봉인의 u_hash 는 *자식 sealed + 배선 구조*의 Merkle 일 뿐, 결과 유니터리가
의도(예: GHZ16)와 같다는 것을 증명하지 않는다(dense 2^n 미실체화, C4 미적용). Tier-0/2/3 의 unitary_equiv
와 혼동하면 과대표현. → 각 seal 이 *무엇을 보장하는지* 명시한다.

제약 준수:
  - 오라클(verify_seal)·sealed.json 은 건드리지 않는다(사용만, 결정론 byte-identical). semantic_guarantee 는
    REGISTRY-MANIFEST/DEPENDENCY-GRAPH 처럼 **비파괴 registry 레이어** `registry/SEMANTIC-GUARANTEES.json` 로 둔다.
  - ghz16 부분검증: dense(2^16×2^16=4G) 미실체화. **statevector(2^16=65536, 1MB)** 두 독립 경로로 비교:
      path A = 봉인된 plan 을 게이트행렬로 적용(statevector 엔진)
      path B = canonical GHZ16 의도(H on q0 + 선형 CNOT 체인)를 정수 비트연산으로 — plan 파싱과 무관
    + 앵커: path A(|0..0>) == GHZ16 상태 (의도 정의) → structural seal 이 GHZ16 을 실제 구현함을 부분보증.
    + negative control: plan 1수 변형 시 검증이 실패함을 확인(테스트가 공허하지 않음 = teeth).

사용:  python scripts/semantic_guarantee.py
"""
import os, sys, json, glob
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
MODREG = os.path.join(ROOT, "registry", "modules")
APPREG = os.path.join(ROOT, "registry", "apps")
APPS = os.path.join(ROOT, "specs", "apps")
OUT = os.path.join(ROOT, "registry", "SEMANTIC-GUARANTEES.json")

# Tier → semantic_guarantee (P-5 표 코드화)
TIER_GUARANTEE = {
    0: {"class": "unitary_equiv", "method": "dense EXACT (composite == golden, C4, 전역위상 무시)"},
    1: {"class": "structural_wellformed", "method": "Merkle(자식 sealed u_hash + 배선). ⚠ unitary 동등성 미증명"},
    2: {"class": "unitary_equiv", "method": "Clifford tableau"},
    3: {"class": "unitary_equiv", "method": "Clifford+T ZX (conservative, safe false-negative)"},
}


def resolve_tier(d):
    """sealed dict → (tier:int, source). tier 명시 없으면 contract 로 추론.
    verify_seal: tier 생략(None)=정방 dense EXACT(Tier-0); contract 접미사로 structural/clifford/zx 구분."""
    t = d.get("tier")
    if t is not None:
        return int(t), "explicit"
    c = d.get("contract", "")
    if "structural" in c:
        return 1, "inferred(contract)"
    if "clifford+t" in c or "zx" in c:
        return 3, "inferred(contract)"
    if "clifford" in c:
        return 2, "inferred(contract)"
    return 0, "inferred(default-dense)"   # plain C1-C4 = Tier-0 EXACT

# ── ghz16 부분검증: 독립 두 경로 statevector ──
_H = np.array([[1, 1], [1, -1]], complex) / np.sqrt(2)


def _parse_plan(spec_path):
    """spec 의 ```json id=plan``` 블록에서 steps 추출."""
    txt = open(spec_path, encoding="utf-8").read()
    key = "id=plan"
    i = txt.index(key); j = txt.index("```", i)
    block = txt[txt.index("{", i):j]
    return json.loads(block)["steps"]


# path A: statevector 엔진(게이트행렬 적용)
def _apply_1q(psi, U, q, n):
    psi = psi.reshape([2] * n)
    psi = np.tensordot(U, psi, axes=([1], [q]))
    psi = np.moveaxis(psi, 0, q)
    return psi.reshape(-1)


def _apply_cnot(psi, c, t, n):
    psi = psi.reshape([2] * n)
    idx = [slice(None)] * n
    idx[c] = 1
    sub = psi[tuple(idx)]
    sub = np.flip(sub, axis=(t if t < c else t - 1))
    psi[tuple(idx)] = sub
    return psi.reshape(-1)


def _pathA(psi, steps, n):
    """봉인 plan 을 게이트행렬로 적용 (big-endian: qubit q = axis q = bit n-1-q)."""
    for s in steps:
        g = os.path.basename(s["spec"]).split(".")[0]
        tg = s["targets"]
        if g == "h_gate":
            psi = _apply_1q(psi, _H, tg[0], n)
        elif g == "cnot":
            psi = _apply_cnot(psi, tg[0], tg[1], n)
        else:
            raise ValueError(f"부분검증 미지원 게이트 {g}")
    return psi


# path B: canonical GHZ_n 의도(H on q0 + 선형 CNOT 체인 0-1-...-n-1)를 정수 비트연산으로.
# ★ plan 파싱과 무관(하드코딩 의도) — path A(봉인 plan) vs path B(의도) 비교가 "plan 이 의도를
#   실현하는가"를 검증한다(둘 다 plan 을 읽으면 plan 버그를 못 잡으므로 의도를 독립 인코딩).
def _pathB_unitary_on(psi, n):
    """canonical GHZ_n 유니터리를 basis 정수에 직접 전파해 U@psi 반환(게이트행렬 미사용)."""
    dim = 1 << n
    b = np.arange(dim, dtype=np.int64)
    out = np.zeros(dim, complex)
    qh = 0
    ph = n - 1 - qh                     # big-endian bit position (q0 = MSB)
    mh = np.int64(1) << ph

    def chain(x):                       # canonical CNOT 체인 (i,i+1) i=0..n-2, classical XOR
        x = x.copy()
        for i in range(n - 1):
            pc = n - 1 - i; pt = n - 1 - (i + 1)
            x ^= ((x >> pc) & 1) << pt
        return x
    b0 = b & ~mh                        # q0 = 0 분기
    b1 = b | mh                         # q0 = 1 분기
    phase = np.where((b >> ph) & 1, -1.0, 1.0)   # H|x> 의 (-1)^x
    inv = 1.0 / np.sqrt(2)
    np.add.at(out, chain(b0), psi * inv)
    np.add.at(out, chain(b1), psi * (inv * phase))
    return out


def partial_verify_ghz16(seed=20260627):
    spec = os.path.join(APPS, "ghz16_structural.app.pg")
    steps = _parse_plan(spec)
    n = 16; dim = 1 << n
    rng = np.random.default_rng(seed)
    checks = {}

    # 앵커(의도 정의, path B 무관): path A(|0..0>) == GHZ16 = (|0..0>+|1..1>)/√2
    e0 = np.zeros(dim, complex); e0[0] = 1.0
    psiA0 = _pathA(e0.copy(), steps, n)
    ghz = np.zeros(dim, complex); ghz[0] = ghz[dim - 1] = 1 / np.sqrt(2)
    checks["anchor_ghz_state"] = bool(np.allclose(psiA0, ghz, atol=1e-9))

    # basis 표본: path A(e_b) == path B(U@e_b)
    n_basis = 48
    bs = [0, dim - 1] + list(rng.integers(0, dim, size=n_basis - 2))
    ok_basis = 0
    for bidx in bs:
        e = np.zeros(dim, complex); e[bidx] = 1.0
        a = _pathA(e.copy(), steps, n)
        bvec = _pathB_unitary_on(e, n)
        ok_basis += bool(np.allclose(a, bvec, atol=1e-9))
    checks["basis_inputs"] = {"tested": len(bs), "matched": ok_basis}

    # random-subspace projection: 무작위 입력벡터에서 path A == path B
    n_rand = 16
    ok_rand = 0
    for _ in range(n_rand):
        v = rng.standard_normal(dim) + 1j * rng.standard_normal(dim)
        v /= np.linalg.norm(v)
        a = _pathA(v.copy(), steps, n)
        bvec = _pathB_unitary_on(v, n)
        ok_rand += bool(np.allclose(a, bvec, atol=1e-9) and abs(np.linalg.norm(a) - 1) < 1e-9)
    checks["random_vectors"] = {"tested": n_rand, "matched": ok_rand}

    # negative control: plan 의 한 CNOT target 을 변형 → path A 가 의도(path B)와 불일치해야 함(teeth).
    mutated = [dict(s) for s in steps]
    for s in mutated:
        if os.path.basename(s["spec"]).startswith("cnot"):
            t = list(s["targets"]); t[1] = (t[1] + 2) % n; s["targets"] = t  # 배선 손상
            break
    vm = (rng.standard_normal(dim) + 1j * rng.standard_normal(dim)); vm /= np.linalg.norm(vm)
    a_mut = _pathA(vm.copy(), mutated, n)
    checks["negative_control_detects_mutation"] = bool(not np.allclose(a_mut, _pathB_unitary_on(vm, n), atol=1e-9))

    verified = (checks["anchor_ghz_state"]
                and checks["basis_inputs"]["matched"] == checks["basis_inputs"]["tested"]
                and checks["random_vectors"]["matched"] == checks["random_vectors"]["tested"]
                and checks["negative_control_detects_mutation"])
    return {"verified": bool(verified), "method": "statevector 2^16 (dense 미실체화); "
            "path A=게이트행렬 적용 vs path B=정수 비트연산(독립); 앵커=A(|0..0>)==GHZ16 상태",
            "atol": 1e-9, "seed": seed, "checks": checks,
            "scope": "부분(샘플 basis 48 + random 16); 전수 unitary 동등성 아님 — Tier-1 약한 의미보증 상향"}


def main():
    sealed = {}   # key = "<kind>:<id>" (module/app 는 별도 네임스페이스 — 게이트가 양쪽에 봉인됨)
    for reg, kind in ((MODREG, "module"), (APPREG, "app")):
        for p in sorted(glob.glob(os.path.join(reg, "*.sealed.json"))):
            d = json.load(open(p, encoding="utf-8"))
            tier, tsrc = resolve_tier(d)
            sealed[f"{kind}:{d['id']}"] = {"id": d["id"], "kind": kind, "tier": tier, "tier_source": tsrc,
                                           "contract": d.get("contract"), "u_hash": d.get("u_hash"),
                                           "n_sys": d.get("n_sys")}
    # W1.1: sampled-dense 격상 로드(비파괴 파일 읽기; sampled_dense_verify.py 산출) — structural → unitary_equiv_sampled
    sampled = {}
    sp = os.path.join(ROOT, "registry", "SAMPLED-DENSE-REPORT.json")
    if os.path.exists(sp):
        rep = json.load(open(sp, encoding="utf-8")).get("results", {})
        sampled = {f"app:{aid}": r for aid, r in rep.items() if r.get("verified")}
    print("=" * 84)
    print("semantic_guarantee 비파괴 레이어 (R-K) — sealed/oracle 미변경")
    print("=" * 84)

    # ghz16 부분검증
    pv = None
    if "app:ghz16_structural" in sealed:
        print("\n[ghz16_structural] Tier-1 부분검증 (statevector 2^16, 독립 두 경로)...")
        pv = partial_verify_ghz16()
        c = pv["checks"]
        print(f"   anchor GHZ16 상태: {'PASS' if c['anchor_ghz_state'] else 'FAIL'}")
        print(f"   basis 입력: {c['basis_inputs']['matched']}/{c['basis_inputs']['tested']}")
        print(f"   random 벡터: {c['random_vectors']['matched']}/{c['random_vectors']['tested']}")
        print(f"   negative control(변형 탐지): {'PASS' if c['negative_control_detects_mutation'] else 'FAIL'}")
        print(f"   => verified={pv['verified']}")

    out = {"_schema": "semantic-guarantee-v1",
           "_note": "비파괴 레이어. sealed.json/oracle 불변. Tier-1=structural_wellformed(Merkle)≠unitary_equiv; "
                    "부분검증 첨부 시 명시된 입력부분공간에서 의도 일치 확인됨.",
           "tier_legend": TIER_GUARANTEE, "guarantees": {}}
    by_class = {}
    by_kind_class = {}   # W0.2: 헤드라인 분리표기 — kind(module/app)별 보증등급 분포
    for key, s in sorted(sealed.items()):
        g = dict(TIER_GUARANTEE.get(s["tier"], {"class": "unknown", "method": "?"}))
        if key in sampled and g["class"] == "structural_wellformed":   # W1.1 격상
            g = {"class": "unitary_equiv_sampled",
                 "method": "sampled-dense 두 독립경로 statevector(seed 봉인, W1.1). 부분(샘플) 보증 — 전수 unitary_equiv 아님"}
        entry = {"kind": s["kind"], "id": s["id"], "tier": s["tier"], "tier_source": s["tier_source"],
                 "semantic_guarantee": g["class"], "method": g["method"], "u_hash": s["u_hash"]}
        if key in sampled:
            entry["sampled_dense"] = {"seed": sampled[key]["seed"], "anchor_digest": sampled[key]["anchor_digest"],
                                      "checks": sampled[key]["checks"]}
        if s["id"] == "ghz16_structural" and pv:
            entry["partial_verification"] = pv
        out["guarantees"][key] = entry
        by_class[g["class"]] = by_class.get(g["class"], 0) + 1
        kc = by_kind_class.setdefault(s["kind"], {})
        kc[g["class"]] = kc.get(g["class"], 0) + 1
    out["headline_split"] = {
        "_note": "헤드라인 수치를 보증등급으로 분리(exact 과대표시 방지, A3/A8 blind-spot). "
                 "structural_wellformed=Merkle 구조보증(unitary 미보증); 부분검증 첨부 시 명시 부분공간에서만 의도일치.",
        "by_kind_class": by_kind_class, "by_class": by_class}

    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("\n" + "-" * 84)
    print("headline_split: " + " | ".join(
        f"{kind} " + ",".join(f"{c}={n}" for c, n in sorted(cc.items())) for kind, cc in sorted(by_kind_class.items())))
    print(f"봉인 {len(sealed)}개 분류: " + " · ".join(f"{k}={v}" for k, v in sorted(by_class.items())))
    t1 = [i for i, s in sealed.items() if s["tier"] == 1]
    print(f"Tier-1(structural_wellformed) {len(t1)}개: {t1}")
    if pv:
        print(f"ghz16 부분검증: {'✅ verified (약한 의미보증 상향)' if pv['verified'] else '❌ FAIL'}")
    print(f"리포트: {os.path.relpath(OUT, ROOT)}")
    print("=" * 84)
    ok = (pv["verified"] if pv else True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
