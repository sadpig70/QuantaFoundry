"""sampled_dense_verify.py — W1.1: Tier-1 structural 봉인의 sampled-dense 보증등급 상향.

배경(8-agent A5/A8 최약가정): Tier-1 STRUCTURAL 봉인의 u_hash 는 *자식 sealed + 배선*의 Merkle 일 뿐,
결과 유니터리가 의도와 같음을 증명하지 않는다(dense 2^n 미실체화). 복리테제는 정확히 이 스케일에서
보증을 잃는다. dense 전수검증은 불가하나, K 개 random basis-state column 을 **두 독립 경로**로 대조하면
*명시된 부분공간에서* 의도 일치를 결정론적으로 확인할 수 있다.

신규 보증등급 **unitary_equiv_sampled** (structural_wellformed ↔ unitary_equiv 사이):
  path A = 봉인된 plan 을 제1원리 게이트행렬(second_oracle.INDEP, qualtran/spec-golden 미사용)로 statevector 에 적용
  path B = 앱별 canonical 의도를 plan 파싱과 무관하게 독립 인코딩(reference registry)
  + anchor(정의 입력) + K random basis 표본 + negative control(plan 변형 탐지=teeth)
  seed 를 리포트에 명시 봉인 → 2회 byte-identical 재현(결정론 위반 0).

경계(정직): 부분(샘플) 보증이며 전수 unitary_equiv 아님. dense 미실체화(statevector 만). 비파괴
(sealed.json/oracle/frozen 미변경; registry/SAMPLED-DENSE-REPORT.json 가산 레이어).

사용:  python scripts/sampled_dense_verify.py
"""
import os, sys, json, hashlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
from second_oracle import INDEP                       # noqa: E402  제1원리 게이트(독립 구성)
from semantic_guarantee import _parse_plan, _pathB_unitary_on, resolve_tier   # noqa: E402

APPS = os.path.join(ROOT, "specs", "apps")
APPREG = os.path.join(ROOT, "registry", "apps")
OUT = os.path.join(ROOT, "registry", "SAMPLED-DENSE-REPORT.json")
SEED = 20260628


# ── path A: 봉인 plan 을 제1원리 게이트로 statevector 에 적용 (dense 행렬 미실체화, big-endian q0=MSB) ──
def _apply(psi, U, targets, n):
    k = len(targets)
    t = psi.reshape([2] * n)
    Ut = np.asarray(U, dtype=complex).reshape([2] * k + [2] * k)
    t = np.tensordot(Ut, t, axes=(list(range(k, 2 * k)), list(targets)))
    t = np.moveaxis(t, list(range(k)), list(targets))
    return t.reshape(-1)


def _path_a(psi, steps, n):
    """봉인 plan(독립 게이트 INDEP) 을 statevector 에 적용. INDEP 미보유 게이트면 None(미지원)."""
    for s in steps:
        gid = os.path.basename(s["spec"]).split(".")[0]
        if gid not in INDEP:
            return None
        psi = _apply(psi, INDEP[gid](), s["targets"], n)
    return psi


# ── path B: 앱별 canonical 의도(plan 무관 독립 인코딩) ──
def _ref_ghz(n):
    return lambda psi: _pathB_unitary_on(psi, n)


REFERENCE = {            # app_id -> (n, canonical reference factory)
    "ghz16_structural": (16, _ref_ghz),
}


def _digest(v):
    re = np.round(v.real, 9) + 0.0; im = np.round(v.imag, 9) + 0.0
    return hashlib.sha256(re.tobytes() + im.tobytes()).hexdigest()[:16]


def verify_app(app_id, n, ref_factory, n_basis=48, n_random=16, seed=SEED):
    spec = os.path.join(APPS, f"{app_id}.app.pg")
    steps = _parse_plan(spec)
    dim = 1 << n
    rng = np.random.default_rng(seed)
    refB = ref_factory(n)
    checks = {}

    # anchor: path A(|0..0>) == canonical 의도 상태 (GHZ16 = (|0..0>+|1..1>)/√2)
    e0 = np.zeros(dim, complex); e0[0] = 1.0
    a0 = _path_a(e0.copy(), steps, n)
    if a0 is None:
        return {"app": app_id, "verified": False, "reason": "unsupported_gate_in_plan"}
    checks["anchor"] = bool(np.allclose(a0, refB(e0.copy()), atol=1e-9))

    # K basis 표본: path A(e_b) == path B(e_b)
    bs = [0, dim - 1] + [int(x) for x in rng.integers(0, dim, size=max(0, n_basis - 2))]
    ok_basis = sum(1 for b in bs
                   if np.allclose(_path_a((lambda e: (e.__setitem__(b, 1.0) or e))(np.zeros(dim, complex)), steps, n),
                                  refB((lambda e: (e.__setitem__(b, 1.0) or e))(np.zeros(dim, complex))), atol=1e-9))
    checks["basis"] = {"tested": len(bs), "matched": ok_basis}

    # random 벡터(중첩 입력): path A == path B
    ok_rnd = 0
    for _ in range(n_random):
        v = rng.standard_normal(dim) + 1j * rng.standard_normal(dim); v /= np.linalg.norm(v)
        if np.allclose(_path_a(v.copy(), steps, n), refB(v.copy()), atol=1e-9):
            ok_rnd += 1
    checks["random"] = {"tested": n_random, "matched": ok_rnd}

    # negative control: plan 1수 배선 변형 → 불일치(teeth)
    mut = [dict(s) for s in steps]
    for s in mut:
        if os.path.basename(s["spec"]).startswith("cnot"):
            t = list(s["targets"]); t[1] = (t[1] + 2) % n; s["targets"] = t
            break
    vm = rng.standard_normal(dim) + 1j * rng.standard_normal(dim); vm /= np.linalg.norm(vm)
    am = _path_a(vm.copy(), mut, n)
    checks["negative_control"] = bool(am is not None and not np.allclose(am, refB(vm.copy()), atol=1e-9))

    verified = (checks["anchor"] and checks["basis"]["matched"] == checks["basis"]["tested"]
                and checks["random"]["matched"] == checks["random"]["tested"]
                and checks["negative_control"])
    return {"app": app_id, "n": n, "verified": bool(verified), "seed": seed, "atol": 1e-9,
            "checks": checks, "anchor_digest": _digest(a0),
            "method": "two-path statevector sampling: A=plan via second_oracle.INDEP (1st-principles), "
                      "B=canonical intent (plan-independent). dense 미실체화. 부분(샘플) 보증.",
            "grade": "unitary_equiv_sampled" if verified else "structural_wellformed"}


def main():
    print("=" * 84)
    print("sampled_dense_verify (W1.1) — Tier-1 structural → unitary_equiv_sampled 상향")
    print("=" * 84)
    results = {}
    all_ok = True
    for app_id, (n, ref) in REFERENCE.items():
        p = os.path.join(APPREG, f"{app_id}.sealed.json")
        if not os.path.exists(p):
            continue
        r = verify_app(app_id, n, ref)
        results[app_id] = r
        c = r.get("checks", {})
        print(f"\n[{app_id}] n={r.get('n')} seed={r.get('seed')}")
        if r["verified"]:
            print(f"   anchor={c['anchor']} · basis {c['basis']['matched']}/{c['basis']['tested']} · "
                  f"random {c['random']['matched']}/{c['random']['tested']} · negative={c['negative_control']}")
            print(f"   => grade=unitary_equiv_sampled ✅ (digest {r['anchor_digest']})")
        else:
            all_ok = False
            print(f"   => verified=False ({r.get('reason','check fail')})")
    out = {"_schema": "sampled-dense-v1",
           "_note": "Tier-1 structural 봉인의 sampled-dense 부분검증(unitary_equiv_sampled). "
                    "비파괴 가산 레이어. seed 봉인 → 결정론 재현. 전수 unitary_equiv 아님(부분 보증).",
           "seed": SEED, "results": results}
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("\n" + "-" * 84)
    print(f"sampled-dense: {sum(1 for r in results.values() if r['verified'])}/{len(results)} "
          f"unitary_equiv_sampled · 리포트: {os.path.relpath(OUT, ROOT)}")
    print("=" * 84)
    return 0 if all_ok and results else 1


if __name__ == "__main__":
    sys.exit(main())
