#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cuc_verify — CUC 조립 인증서 (design01 §2.3), shor1285/3683 (n≥19) compositionally_verified.

CQV column_verify 는 n≤18 만(dense 컬럼 수축 비용). n≥19 의 shor1285(19q)·shor3683(20q)는
컬럼 전수 불가 → design01 §2.3 CUC(Compositional Unitary Certificate)로 **조립 논증** 인증.

핵심(전체 유니터리 = 3인자 곱, 각 인자 exact):
  U_shor = Embed(iqft8, counting) · P_modexp · Embed(H^⊗t, counting)
    · iqft8 인자 : ★ring-exact (RING-COLUMN witness, ℤ[ζ_256] float 0 — 앱 무관 공유)
    · modexp     : ★**exhaustive 순열**(본 witness — 기존 sampled 4099 → 전수 2^n 상향,
                    path A=회로 MCT 게이트순열 vs path B=정수산술 w·a^c mod N, atol 없음)
    · H-wall     : ±1 부호 (자명 exact)
  세 인자가 전부 exact + 배선 정형성(targets 단사·범위·ancilla 0) + 자식 등급(cmul 봉인·iqft8 Tier-0)
  ⟹ compositionally_verified: structural 보다 강하고 column_exact 보다 약함(전체 유니터리 컬럼
  전수 대신 인자-분해 + 조립 논증). 정직 경계 명시.

CUC 인증 3항(design01 §2.3):
  1. 자식 등급 조건: plan 자식(cmul·iqft8·h_gate) 봉인 등급 조회
  2. 배선 정형성: 각 step targets 단사·범위·중복없음·n_anc=0 — 결정론 코드 검사
  3. 기능 증인: modexp exhaustive 순열 A==B + negative control(배선 교란·틀린 산술)

정직 경계(★봉인 아님·root 불변 sidecar `.pgf/proofs/<id>.cuc_proof.json`·oracle 무접촉):
  - grade = compositionally_verified — column_exact(전체 컬럼 dense 대조) 아님. 조립 논증은
    "Embed 구현이 표준 텐서 삽입"이라는 코드 신뢰 전제(contracts_code_hash 고정으로 완화).
  - INV-R5 잔여 축소: n≥19 도 modexp exhaustive + iQFT ring-exact → 인자 전부 exact
    (기존 subspace_permutation_sampled 대비 강화). 전체 유니터리 dense 동등은 여전히 미검증.

사용: python scripts/cuc_verify.py [shor1285 shor3683] [--quick]
  --quick: sidecar verified + 배선/자식/ring 재확인 + modexp 표본 재검(전수 재실행 회피, ~수초)
"""
import os
import re
import sys
import json
import glob
import hashlib
import numpy as np

from qf_witness.core.paths import ROOT, SPECS_APPS, PROOFS, REGISTRY_APPS
sys.path.insert(0, os.path.join(ROOT, "qf_witness", "verify"))
import perm_subspace_verify as psv  # noqa: E402

LARGE_SHOR = ["shor1285", "shor3683"]   # n≥19 (column_verify 범위 밖)
SAMPLE_QUICK = 512


def _parse_plan(spec_path):
    txt = open(spec_path, encoding="utf-8").read()
    m = re.search(r"```json id=plan\s*\n(.*?)\n```", txt, re.S)
    return json.loads(m.group(1))


def wiring_formality(shor_id, n):
    """배선 정형성: 각 step targets 단사·범위 [0,n)·중복없음. n_anc=0 확인."""
    spec = os.path.join(SPECS_APPS, f"{shor_id}.app.pg")
    meta = re.search(r"```json id=app_meta\s*\n(.*?)\n```", open(spec, encoding="utf-8").read(), re.S)
    md = json.loads(meta.group(1))
    plan = _parse_plan(spec)
    issues = []
    if md.get("n_anc", 0) != 0:
        issues.append(f"n_anc={md.get('n_anc')} != 0")
    for i, st in enumerate(plan["steps"]):
        tg = st["targets"]
        if len(set(tg)) != len(tg):
            issues.append(f"step{i}: duplicate targets {tg}")
        if any(q < 0 or q >= n for q in tg):
            issues.append(f"step{i}: target out of range [0,{n}) {tg}")
    return {"ok": not issues, "issues": issues, "n_steps": len(plan["steps"])}


def child_grades(shor_id):
    """자식 등급 조회: plan 의 cmul 자식·iqft8·h_gate 봉인 존재 확인."""
    plan = _parse_plan(os.path.join(SPECS_APPS, f"{shor_id}.app.pg"))
    children, missing = [], []
    for st in plan["steps"]:
        ref = st.get("app") or st.get("spec")
        base = os.path.basename(ref)
        if base.endswith(".app.pg"):
            cid = base[:-len(".app.pg")]
            sealed = os.path.join(REGISTRY_APPS, f"{cid}.sealed.json")
            (children if os.path.exists(sealed) else missing).append(cid)
        # spec (module) 은 Tier-0 모듈 — 존재 자명(h_gate 등)
    uniq = sorted(set(children))
    return {"sealed_children": uniq, "n_sealed": len(uniq), "missing": missing, "ok": not missing}


def modexp_exhaustive(shor_id):
    """modexp 코어 exhaustive 순열: path A(회로 MCT)==path B(정수산술), 전수 2^n. + teeth."""
    p = psv.load_shor(shor_id)
    n, t, work, a, N = p["n"], p["t"], p["work"], p["a"], p["N"]
    gates = psv.expand_modexp_gates(p["modexp_steps"])
    pa = psv.path_a_vec(n, gates)                  # 전수 1회 (비쌈: n=20 ~27분)
    pb = psv.path_b_vec(n, t, work, a, N)          # 빠름
    matched = int((pa == pb).sum())
    exact = matched == (1 << n)
    # teeth: 표본 기반(전수 path_a_vec 재실행 회피 — 교란이 순열을 바꿈을 표본으로 검출).
    #   배선 교란(첫 게이트 target 이동)·틀린 산술(a+1).
    mut = list(gates)
    (mc, mt) = mut[0]
    alt = (mt + 1) % n
    while alt in mc or alt == mt:
        alt = (alt + 1) % n
    mut[0] = (mc, alt)
    rng = np.random.default_rng(psv.SEED)
    tsamp = [0, (1 << n) - 1, (1 << work) + 1] + [int(x) for x in rng.integers(0, 1 << n, size=4096)]
    pb_bad = psv.path_b_vec(n, t, work, a + 1, N)   # 빠름(정수산술)
    nc_wiring = any(psv.path_a_single(n, mut, s) != int(pb[s]) for s in tsamp)
    nc_arith = any(int(pa[s]) != int(pb_bad[s]) for s in tsamp)
    return {"n": n, "n_modexp_gates": len(gates), "basis_tested": 1 << n,
            "basis_matched": matched, "exact_permutation": exact,
            "nc_wiring_teeth": bool(nc_wiring), "nc_arith_teeth": bool(nc_arith),
            "negative_control_reject": bool(nc_wiring and nc_arith)}


def _ring_covers_iqft8():
    """RING-COLUMN witness 가 iqft8 ring-exact 를 확립했는지(앱 무관 공유 인자)."""
    rp = os.path.join(PROOFS, "RING-COLUMN.json")
    if not os.path.exists(rp):
        return {"ok": False, "reason": "RING-COLUMN.json absent"}
    r = json.load(open(rp, encoding="utf-8"))
    return {"ok": bool(r.get("iqft_ring_exact")), "ring": r.get("ring"),
            "iqft_checked": r.get("iqft_checked"), "float_operations": r.get("float_operations"),
            "digest": r.get("proof_digest")}


def _digest(payload):
    body = {k: payload[k] for k in ("id", "n_sys", "basis_matched", "basis_tested",
                                    "wiring_ok", "child_ok", "iqft_ring_exact", "grade")}
    return hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]


def certify(shor_id):
    p = psv.load_shor(shor_id)
    n = p["n"]
    wiring = wiring_formality(shor_id, n)
    child = child_grades(shor_id)
    ring = _ring_covers_iqft8()
    modexp = modexp_exhaustive(shor_id)
    verified = (wiring["ok"] and child["ok"] and ring["ok"]
                and modexp["exact_permutation"] and modexp["negative_control_reject"])
    payload = {
        "_schema": "cuc-proof-v1",
        "_note": "CUC 조립 인증서(design01 §2.3). 전체 유니터리=iqft8(ring-exact)·modexp(exhaustive 순열)·"
                 "H-wall(±1) 3인자 + 배선 정형성 + 자식 등급 → compositionally_verified. "
                 "★봉인 아님·root 불변 sidecar·oracle 무접촉. column_exact(전체 컬럼 dense) 아님 — "
                 "조립 논증(Embed=표준 텐서 삽입 코드 신뢰). INV-R5 잔여 축소(n≥19 인자 전부 exact).",
        "id": shor_id, "N": p["N"], "a": p["a"], "n_sys": n,
        "counting_t": p["t"], "work": p["work"],
        # 인자 1: iqft8 ring-exact (공유 witness)
        "iqft_ring_exact": ring["ok"], "iqft_ring": ring.get("ring"),
        "iqft_float_operations": ring.get("float_operations"),
        "iqft_ring_digest": ring.get("digest"),
        # 인자 2: modexp exhaustive
        "n_modexp_gates": modexp["n_modexp_gates"],
        "basis_tested": modexp["basis_tested"], "basis_matched": modexp["basis_matched"],
        "modexp_exhaustive_exact": modexp["exact_permutation"],
        "nc_wiring_teeth": modexp["nc_wiring_teeth"], "nc_arith_teeth": modexp["nc_arith_teeth"],
        "negative_control_reject": modexp["negative_control_reject"],
        # 인자 3 + 조립
        "hwall_trivial": True,
        "wiring_ok": wiring["ok"], "wiring_issues": wiring["issues"], "wiring_steps": wiring["n_steps"],
        "child_ok": child["ok"], "sealed_children": child["sealed_children"],
        "child_missing": child["missing"],
        "verified": verified,
        "grade": "compositionally_verified" if verified else "cuc_incomplete",
        "scope": "iqft8 ring-exact + modexp exhaustive perm + H-wall ±1 + wiring formality; "
                 "NOT full-unitary column dense (compositional argument via standard Embed). "
                 "stronger than subspace_permutation_sampled, weaker than unitary_equiv_column_exact.",
    }
    payload["proof_digest"] = _digest(payload)
    return payload


def write_sidecar(payload):
    os.makedirs(PROOFS, exist_ok=True)
    path = os.path.join(PROOFS, f"{payload['id']}.cuc_proof.json")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    return path


def quick_recheck():
    """reproduce 용 경량: sidecar verified + 배선/자식/ring 재확인 + modexp 표본(전수 회피)."""
    ok = True
    for sid in LARGE_SHOR:
        sc = os.path.join(PROOFS, f"{sid}.cuc_proof.json")
        if not os.path.exists(sc):
            return False
        d = json.load(open(sc, encoding="utf-8"))
        if not (d.get("verified") and d.get("grade") == "compositionally_verified"):
            return False
        # 배선·자식·ring 재확인(가벼움)
        p = psv.load_shor(sid)
        if not wiring_formality(sid, p["n"])["ok"]:
            return False
        if not child_grades(sid)["ok"]:
            return False
        if not _ring_covers_iqft8()["ok"]:
            return False
        # modexp 표본 재검(전수 2^n 회피)
        n, t, work, a, N = p["n"], p["t"], p["work"], p["a"], p["N"]
        gates = psv.expand_modexp_gates(p["modexp_steps"])
        rng = np.random.default_rng(psv.SEED)
        samples = [0, (1 << n) - 1] + [int(x) for x in rng.integers(0, 1 << n, size=SAMPLE_QUICK)]
        bad = any(psv.path_a_single(n, gates, s) != psv.path_b_single(n, t, work, a, N, s)
                  for s in samples)
        ok &= not bad
    return ok


def main():
    args = [a for a in sys.argv[1:]]
    if "--quick" in args:
        r = quick_recheck()
        print(f"cuc_verify quick: all_ok={r}")   # witness_batch 규약(all_ok=True)
        sys.exit(0 if r else 1)
    ids = [a for a in args if not a.startswith("-")] or LARGE_SHOR
    all_ok = True
    for sid in ids:
        pl = certify(sid)
        path = write_sidecar(pl)
        flag = "OK " if pl["verified"] else "FAIL"
        print(f"[{flag}] {sid}: n={pl['n_sys']} modexp {pl['basis_matched']}/{pl['basis_tested']} "
              f"exhaustive={pl['modexp_exhaustive_exact']} iqft_ring={pl['iqft_ring_exact']} "
              f"wiring={pl['wiring_ok']} child={pl['child_ok']} → {pl['grade']}")
        all_ok &= pl["verified"]
    print(f"cuc_verify: {'ALL VERIFIED' if all_ok else 'SOME FAILED'} ({len(ids)} apps)")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
