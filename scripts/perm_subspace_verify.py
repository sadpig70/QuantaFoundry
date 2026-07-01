#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""perm_subspace_verify — P0 PermutationSubspaceContract (v0.8 통합로드맵).

structural Shor 앱(shor{N}, Tier-1 Merkle)의 *modexp 코어*를 계산기저 부분공간에서
exact 순열로 강검증한다. dense 2^total 미실체화(basis-state 정수 추적).

  path A = shor 배선대로 cmul 을 내부 MCT 게이트까지 전개해 basis state 순열 시뮬
           (회로가 *실제로* 하는 일 — 오직 비트연산, 봉인 u_hash/golden 미참조)
  path B = w·a^c mod N 순수 정수산술 (Shor 수학이 *요구*하는 것 — a·N·배선무관, 독립)

structural(자식 u_hash Merkle + 배선 기록)을 넘어 "기록된 배선이 실제로 올바른
modular-exponentiation 순열을 계산기저에서 구현함"을 독립 2-경로로 확인 (ghz16 선례).

정직 경계 (INV-R5): 강검증 대상은 modexp 코어(H·iQFT 제외한 controlled-cmul 시퀀스).
  H·iQFT 를 포함한 shor 전체 unitary 는 여전히 dense 미검증(중첩 생성). "그 부분공간에서만".

비파괴: sidecar `.pgf/proofs/<shor_id>.subspace_proof.json` 만 생성.
  registry root(module/app u_hash Merkle)·기존 sealed·oracle fingerprint·frozen 무영향.

사용: python scripts/perm_subspace_verify.py [shor69 shor91 ...]  (인자 없으면 9개 전부)
"""
import os, re, sys, json, hashlib
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPECS_APPS = os.path.join(ROOT, "specs", "apps")
PROOFS = os.path.join(ROOT, ".pgf", "proofs")

# 9개 structural Shor 앱 (HANDOFF Current)
STRUCTURAL_SHOR = ["shor69", "shor77", "shor91", "shor119", "shor221",
                   "shor381", "shor635", "shor1285", "shor3683"]

EXHAUSTIVE_BOUND = 18   # n_sys ≤ 18 → 전수 vectorized; ≥19 → 표본(sampled)
N_BASIS = 4096          # 표본 basis state 수 (n≥19)
SEED = 20260701


# ── 파싱 ──────────────────────────────────────────────────────────────────
def _parse_plan(spec_path):
    """app.pg 의 ```json id=plan``` fence → dict."""
    txt = open(spec_path, encoding="utf-8").read()
    m = re.search(r"```json id=plan\s*\n(.*?)\n```", txt, re.S)
    if not m:
        raise ValueError(f"no id=plan fence in {spec_path}")
    return json.loads(m.group(1))


def _shor_NA(shor_id):
    """shor{N} 헤더에서 (N, a) 추출. 헤더 포맷 변형에 무관하게 N=…= 와 a=… 만 매칭."""
    spec = os.path.join(SPECS_APPS, f"{shor_id}.app.pg")
    head = open(spec, encoding="utf-8").readline()
    mN = re.search(r"N=(\d+)=", head)
    ma = re.search(r"a=(\d+)", head)
    if not (mN and ma):
        raise ValueError(f"cannot parse N/a from header: {head!r}")
    return int(mN.group(1)), int(ma.group(1))


def load_shor(shor_id):
    """→ dict(n, t, work, a, N, modexp_steps). t = counting register = plan 의 H 게이트 수(포맷 무관)."""
    spec = os.path.join(SPECS_APPS, f"{shor_id}.app.pg")
    meta = re.search(r"```json id=app_meta\s*\n(.*?)\n```",
                     open(spec, encoding="utf-8").read(), re.S)
    n = json.loads(meta.group(1))["n_sys"]
    N, a = _shor_NA(shor_id)
    plan = _parse_plan(spec)
    t = sum(1 for st in plan["steps"]
            if "spec" in st and os.path.basename(st["spec"]).startswith("h_gate"))
    modexp = [st for st in plan["steps"]
              if "app" in st and os.path.basename(st["app"]).startswith("cmul")]
    return {"n": n, "t": t, "work": n - t, "a": a, "N": N, "modexp_steps": modexp}


def expand_modexp_gates(modexp_steps):
    """controlled-cmul step 들을 절대 qubit MCT 게이트 [(controls, target)] 로 전개.
    각 cmul 내부 plan(모두 c_nx, targets=controls+[target])을 shor 배선(abs_targets)으로 remap."""
    gates = []
    for st in modexp_steps:
        abs_targets = st["targets"]                       # cmul 로컬 0..nq-1 → 절대 qubit
        cmul_spec = os.path.join(SPECS_APPS, os.path.basename(st["app"]))
        for g in _parse_plan(cmul_spec)["steps"]:
            loc = g["targets"]
            absidx = [abs_targets[l] for l in loc]        # MCT 관례: 마지막=target
            gates.append((tuple(absidx[:-1]), absidx[-1]))
    return gates


# ── 2-경로 순열 ────────────────────────────────────────────────────────────
def path_a_vec(n, gates):
    """전수 vectorized: 모든 계산기저 상태의 상(image). big-endian(qubit q → bit n-1-q)."""
    v = np.arange(1 << n, dtype=np.int64)
    for controls, target in gates:
        cmask = 0
        for c in controls:
            cmask |= (1 << (n - 1 - c))
        tmask = np.int64(1) << (n - 1 - target)
        hit = (v & cmask) == cmask
        v = np.where(hit, v ^ tmask, v)
    return v


def path_a_single(n, gates, s):
    """표본용 단일 basis state 순열."""
    for controls, target in gates:
        if all((s >> (n - 1 - c)) & 1 for c in controls):
            s ^= (1 << (n - 1 - target))
    return s


def path_b_vec(n, t, work, a, N):
    """전수 vectorized: (c,w) → (c, w·a^c mod N) if w<N else identity. 배선무관, a·N만."""
    s = np.arange(1 << n, dtype=np.int64)
    c = s >> work
    w = s & ((1 << work) - 1)
    table = np.array([pow(a, int(cc), N) for cc in range(1 << t)], dtype=np.int64)
    mult = table[c]
    wnew = np.where(w < N, (w * mult) % N, w)
    return (c << work) | wnew


def path_b_single(n, t, work, a, N, s):
    c = s >> work
    w = s & ((1 << work) - 1)
    wnew = (w * pow(a, int(c), N)) % N if w < N else w
    return (c << work) | wnew


# ── 검증 ──────────────────────────────────────────────────────────────────
def verify(shor_id):
    p = load_shor(shor_id)
    n, t, work, a, N = p["n"], p["t"], p["work"], p["a"], p["N"]
    gates = expand_modexp_gates(p["modexp_steps"])
    rng = np.random.default_rng(SEED)
    exhaustive = n <= EXHAUSTIVE_BOUND

    # 배선 mutation (회로 teeth): 첫 게이트의 target 을 다른 qubit 으로 손상
    mut = list(gates)
    ci, (mc, mt_) = next((i, g) for i, g in enumerate(gates))
    alt = (mt_ + 1) % n
    while alt in mc or alt == mt_:
        alt = (alt + 1) % n
    mut[ci] = (mc, alt)
    wrong_a = a + 1                                          # 틀린 산술 reference (산술 teeth)

    if exhaustive:
        pa = path_a_vec(n, gates)
        pb = path_b_vec(n, t, work, a, N)
        matched = int(np.count_nonzero(pa == pb))
        tested = 1 << n
        exact = bool(matched == tested)
        method = "exhaustive"
        # teeth1: 회로 배선 mutation → path B 와 불일치
        nc_wiring = bool(not np.array_equal(path_a_vec(n, mut), pb))
        # teeth2: 틀린 산술(a+1) → path A(정확 회로)와 불일치 (검증이 정확한 modexp 에만 통과)
        nc_arith = bool(not np.array_equal(pa, path_b_vec(n, t, work, wrong_a, N)))
        nc_reject = nc_wiring and nc_arith
    else:
        anchors = [0, (1 << n) - 1, (1 << work) + 1]         # |0>, all-1, |c=1,w=1>
        samples = anchors + [int(x) for x in rng.integers(0, 1 << n, size=N_BASIS)]
        pa_s = [path_a_single(n, gates, s) for s in samples]
        pb_s = [path_b_single(n, t, work, a, N, s) for s in samples]
        matched = sum(1 for x, y in zip(pa_s, pb_s) if x == y)
        tested = len(samples)
        exact = bool(matched == tested)
        method = "sampled"
        # teeth2(주): 틀린 산술은 표본무관 robust — path A(정확 회로)가 a+1 산술과 거의 전부 불일치
        nc_arith = any(pa_s[i] != path_b_single(n, t, work, wrong_a, N, samples[i])
                       for i in range(len(samples)))
        # teeth1(보조): 배선 mutation 이 표본에서 순열을 바꾸는지
        nc_wiring = any(path_a_single(n, mut, s) != pb_s[i] for i, s in enumerate(samples))
        nc_reject = nc_arith                                 # 표본에선 산술 teeth 를 주 판정으로

    verified = exact and nc_reject
    grade = "subspace_permutation_exhaustive" if (verified and exhaustive) \
        else "subspace_permutation_sampled" if verified else "structural_only"
    return {
        "id": shor_id, "N": N, "a": a, "n_sys": n, "counting_t": t, "work": work,
        "n_modexp_gates": len(gates),
        "path_A": "circuit permutation (cmul→MCT gate expansion, bitops only)",
        "path_B": "integer arithmetic w·a^c mod N (independent, wiring-free)",
        "method": method, "basis_tested": tested, "basis_matched": matched,
        "exact_permutation": exact, "negative_control_reject": nc_reject,
        "nc_wiring_teeth": nc_wiring, "nc_arith_teeth": nc_arith,
        "verified": verified, "grade": grade,
        "dense_materialized": False, "deterministic": True,
        "scope": "modexp core only (H·iQFT excluded); NOT full-unitary equivalence — INV-R5",
        "seed": SEED,
    }


def _digest(proof):
    """결정론 확인용 안정 다이제스트."""
    body = {k: proof[k] for k in ("id", "N", "a", "n_sys", "n_modexp_gates",
                                  "basis_tested", "basis_matched", "grade")}
    return hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]


def write_sidecar(proof):
    os.makedirs(PROOFS, exist_ok=True)
    proof = dict(proof, proof_digest=_digest(proof),
                 _schema="subspace-proof-v1",
                 _note="비파괴 sidecar. registry root/sealed/oracle/frozen 무영향. "
                       "modexp 코어 계산기저 부분공간 순열 강검증(structural 상향). "
                       "H·iQFT 포함 전체 unitary 는 여전히 미검증(INV-R5).")
    path = os.path.join(PROOFS, f"{proof['id']}.subspace_proof.json")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(proof, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    return path


def quick_recheck(shor_id, k=48):
    """reproduce_all 용 경량 재검증: 소수 basis exact + 산술 teeth + sidecar verified 확인.
    전수 재시뮬(수분) 대신 표본만 — P0 강검증이 여전히 유효함을 빠르게 확인."""
    sc_path = os.path.join(PROOFS, f"{shor_id}.subspace_proof.json")
    if not os.path.exists(sc_path):
        raise FileNotFoundError(f"no sidecar {shor_id}.subspace_proof.json")
    sc = json.load(open(sc_path, encoding="utf-8"))
    if not sc.get("verified"):
        return False
    p = load_shor(shor_id)
    n, t, work, a, N = p["n"], p["t"], p["work"], p["a"], p["N"]
    gates = expand_modexp_gates(p["modexp_steps"])
    rng = np.random.default_rng(SEED + 1)
    samples = [0, (1 << work) + 1] + [int(x) for x in rng.integers(0, 1 << n, size=k)]
    exact = all(path_a_single(n, gates, s) == path_b_single(n, t, work, a, N, s) for s in samples)
    teeth = any(path_a_single(n, gates, s) != path_b_single(n, t, work, a + 1, N, s) for s in samples)
    return bool(exact and teeth)


def main():
    args = sys.argv[1:]
    quick = "--quick" in args
    targets = [x for x in args if not x.startswith("--")] or STRUCTURAL_SHOR
    if quick:
        all_ok = True
        for sid in targets:
            try:
                ok = quick_recheck(sid)
            except Exception as e:
                print(f"  {sid}: ERROR {e}", flush=True); all_ok = False; continue
            all_ok = all_ok and ok
            print(f"  {sid}: quick_recheck={'PASS' if ok else 'FAIL'}", flush=True)
        print(f"\nperm_subspace_verify --quick: {len(targets)} apps · all_ok={all_ok}", flush=True)
        return 0 if all_ok else 1
    all_ok = True
    results = []
    for sid in targets:
        try:
            pr = verify(sid)
        except Exception as e:
            print(f"  {sid}: ERROR {e}", flush=True)
            all_ok = False
            continue
        write_sidecar(pr)
        ok = pr["verified"]
        all_ok = all_ok and ok
        results.append(pr)
        print(f"  {sid}: {pr['grade']} · {pr['method']} "
              f"basis {pr['basis_matched']}/{pr['basis_tested']} "
              f"· neg_control_reject={pr['negative_control_reject']} "
              f"· gates={pr['n_modexp_gates']} · digest={_digest(pr)}", flush=True)
    print(f"\nperm_subspace_verify: {len(results)}/{len(targets)} · all_ok={all_ok}", flush=True)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
