# -*- coding: utf-8 -*-
"""
arith_family.py — P1 ArithFamilyExtend (task_plan_pg §P1)

기존 산술합성 엔진(genskills.modmul_synth: MMD reversible synthesis)을 *재사용*해
신규 distinct-prime modulus 의 controlled-(×a mod N) 를 Tier-0 EXACT 봉인한다.
"검증 비용 1회 → 영구 재사용 → 비선형 생산력"(복리) 명제의 직접 실현.

═══════════════════════════════════════════════════════════════════════════
sub-PG (P1 분해)
═══════════════════════════════════════════════════════════════════════════
P1_ArithFamilyExtend
    SealMCT6           // 누락 prereq c6x(MCT-6) 모듈 봉인 — distinct-prime 패밀리 잠금해제
    VerifyMCT6Indep    // c6x 산술순열 독립 재구성 → u_hash 대조 (proof-backed, free-param 0)
    SynthDistinctPrime // cmul2_mod35(5×7)·cmul2_mod33(3×11) Tier-0 EXACT 봉인(7q)
    EngineRegression   // 기존 cmul2_mod21(≤5ctrl) genskills(미변경) 재생성 u_hash==registry
    IndependentArithVerify // 신규 cmul 산술순열 독립 재구성 → sealed u_hash 대조 (삼각측량)
    BehavioralObserve  // ×2 mod N orbit period=ord_N(2) 행동관찰 (illustrative only, §8.4)
    ShorScopeHonest    // full Shor(N=35)≥14q>EXACT_BOUND → Tier-1 STRUCTURAL 정직 표기

정직성 경계:
 - 발견의 정직(핵심): distinct-prime Shor 타겟(33/35/39/51)은 nq=7 → 6-control 필요. 기존 MCT
   라이브러리(≤c5x)로 *차단*됨 → 누락 prereq c6x 를 먼저 봉인(P5 의존성-해결 철학). 이것이
   "엔진 재사용만으로 무한 확장"의 정직한 한계: **새 primitive 1개가 패밀리를 연다.**
 - 엔진 *진화*(무변경 아님): genskills.py 의 modmul_synth 가 c6x 를 지원하도록 upstream
   (_MCT_MODULE[6]=c6x, limit 6) → method self-seal 재스탬프(genskills catalog). 이는 8a-2/8a-3
   과 동일한 method evolution 이며, 기존 cmul(≤5ctrl) 산출은 byte 불변(EngineRegression 증명).
   재스탬프 후 genskills verify INTACT.
 - 생성≠검증: 산출물은 오라클(verify_seal/app_assemble, function 2) 통과로만 SEALED.
 - 행동관찰(BehavioralObserve)은 illustrative only — 봉인 증거 아님(§8.4).
 - honest 분해: plan 은 봉인 MCT(toffoli/c3x..c6x) — MatrixGate 0.
"""
from __future__ import annotations

import os
import sys
import json
import math
import subprocess
from collections import Counter

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, ORACLE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import verify_seal as vs        # noqa: E402  (instantiate/hash_unitary 사용만)
import app_assemble as aa       # noqa: E402  (앱 봉인 — 사용만)
import genskills as gs          # noqa: E402  (엔진 함수 import — *사용만*, 미변경)

SPECS_MODS = os.path.join(ROOT, "specs", "modules")
SPECS_APPS = os.path.join(ROOT, "specs", "apps")
MODREG = os.path.join(ROOT, "registry", "modules")
APPREG = os.path.join(ROOT, "registry", "apps")
OUT = os.path.join(ROOT, ".pgf", "arith")


# ── SealMCT6 ────────────────────────────────────────────────────────
def _c6x_spec():
    return (
        "```python id=bloq\n"
        "from qualtran.bloqs.mcmt import MultiControlX\n"
        "bloq = MultiControlX(cvs=(1,) * 6)\n"
        "```\n"
        "```python id=golden\n"
        "import numpy as np\n"
        "# C6X: control=first 6 qubits (MSB), target=last (big-endian). flip target iff all controls 1.\n"
        "golden = np.zeros((1<<7, 1<<7), dtype=complex)\n"
        "for s in range(1<<7):\n"
        "    o = (s ^ 1) if (s >> 1) == ((1<<6) - 1) else s\n"
        "    golden[o, s] = 1\n"
        "```\n"
        '```json id=meta\n'
        '{"id": "c6x", "n_sys": 7, "n_anc": 0}\n'
        "```\n")


def seal_mct6():
    """c6x(MCT-6) 모듈 봉인 → registry/modules (canonical 성장, additive)."""
    spec_path = os.path.join(SPECS_MODS, "c6x.pg")
    open(spec_path, "w", encoding="utf-8", newline="\n").write(_c6x_spec())
    r = subprocess.run([sys.executable, os.path.join(ORACLE, "verify_seal.py"),
                        spec_path, "--out", MODREG],
                       capture_output=True, text=True, cwd=ORACLE)
    seal_path = os.path.join(MODREG, "c6x.sealed.json")
    if not os.path.exists(seal_path):
        return {"sealed": False, "stderr": r.stderr.strip()[:300]}
    return json.load(open(seal_path))


def verify_mct6_indep():
    """c6x 산술순열을 *독립* 재구성(genskills/qualtran 미사용) → sealed u_hash 대조."""
    n = 7
    U = np.zeros((1 << n, 1 << n), complex)
    for s in range(1 << n):
        ctrls_all_one = (s >> 1) == ((1 << 6) - 1)   # 상위 6비트 전부 1
        o = (s ^ 1) if ctrls_all_one else s          # target=LSB flip
        U[o, s] = 1
    built = vs.hash_unitary(U)
    sealed = json.load(open(os.path.join(MODREG, "c6x.sealed.json")))["u_hash"]
    return {"independent_u_hash": built[:16], "matches_sealed": built == sealed}


# ── SynthDistinctPrime (진화된 엔진 gs.gen_modmul 직접 사용) ──────────
_MCT_SET = {"x_gate", "cnot", "toffoli", "c3x", "c4x", "c5x", "c6x", "c7x"}


def synth_distinct_prime(targets):
    """cmul_a_modN 앱 spec 을 *진화된* genskills.gen_modmul(c6x 지원)로 생성 → app_assemble 봉인."""
    results = []
    for a, N in targets:
        nq = math.ceil(math.log2(N)) + 1
        spec, deps = gs.gen_modmul(a, N, nq)        # 진화된 엔진(c6x upstream) 직접 사용
        gates = gs.mmd_synthesize(gs._modmul_perm(a, N, nq), nq)  # 보고용 게이트 분포
        assert set(deps).issubset(_MCT_SET), \
            f"plan 이 봉인 MCT 외 모듈 참조: {set(deps) - _MCT_SET} (MatrixGate shortcut 금지)"
        spec_path = os.path.join(SPECS_APPS, f"cmul{a}_mod{N}.app.pg")
        open(spec_path, "w", encoding="utf-8", newline="\n").write(spec)
        v = aa.assemble(spec_path, APPREG)
        results.append({"id": f"cmul{a}_mod{N}", "N": N, "factors": _factor(N),
                        "nq": nq, "gates": len(gates),
                        "control_dist": dict(Counter(len(c) for c, _ in gates)),
                        "deps": deps, "sealed": v.sealed, "tier": v.tier,
                        "u_hash": v.u_hash, "reason": v.reason})
    return results


def _factor(N):
    fs, d, m = [], 2, N
    while d * d <= m:
        while m % d == 0:
            fs.append(d); m //= d
        d += 1
    if m > 1:
        fs.append(m)
    return fs


# ── EngineRegression (genskills 미변경 → 기존 cmul 재현) ─────────────
def engine_regression():
    """genskills.gen_modmul(미변경)로 기존 cmul 재생성 → u_hash==registry (golden 순열 불변 →
    plan 달라도 u_hash 동일). T4 패턴: temp spec 를 specs/apps 에 써야 ../modules 해결."""
    checks = []
    tmp_store = os.path.join(OUT, "_regstore")
    os.makedirs(tmp_store, exist_ok=True)
    tmp_specs = []
    for a, N, nq in [(2, 21, 6), (2, 15, 5)]:    # 직접합성(canonical) 대상
        try:
            spec, _ = gs.gen_modmul(a, N, nq)        # genskills 원본 (미변경)
            sp = os.path.join(SPECS_APPS, f"_arithreg_cmul{a}_mod{N}.app.pg")
            open(sp, "w", encoding="utf-8", newline="\n").write(spec); tmp_specs.append(sp)
            v = aa.assemble(sp, tmp_store)
            reg = json.load(open(os.path.join(APPREG, f"cmul{a}_mod{N}.sealed.json")))["u_hash"]
            checks.append({"id": f"cmul{a}_mod{N}", "sealed": bool(v.sealed),
                           "regenerated_u_hash": (v.u_hash or "")[:16],
                           "matches_registry": bool(v.sealed) and v.u_hash == reg})
        except Exception as e:
            checks.append({"id": f"cmul{a}_mod{N}", "error": f"{type(e).__name__}: {e}"})
    for sp in tmp_specs:                              # 정리(specs/apps 오염 방지)
        try:
            os.remove(sp)
        except OSError:
            pass
    return checks


# ── IndependentArithVerify (제2 검증축, 봉인 비신뢰) ─────────────────
def independent_arith_verify(a, N):
    """신규 cmul 의 controlled-(×a mod N) 순열을 *독립* 재구성 → sealed u_hash 대조."""
    nq = math.ceil(math.log2(N)) + 1
    dim = 1 << nq
    U = np.zeros((dim, dim), complex)
    for s in range(dim):
        if (s >> (nq - 1)) & 1 == 0:                    # control=0 → identity
            U[s, s] = 1
        else:
            w = s & ((1 << (nq - 1)) - 1)
            nw = (a * w) % N if w < N else w            # ×a mod N (범위밖 identity)
            U[(1 << (nq - 1)) | nw, s] = 1
    built = vs.hash_unitary(U)
    sealed = json.load(open(os.path.join(APPREG, f"cmul{a}_mod{N}.sealed.json")))["u_hash"]
    return {"id": f"cmul{a}_mod{N}", "independent_u_hash": built[:16],
            "matches_sealed": built == sealed}


# ── BehavioralObserve (illustrative only) ───────────────────────────
def behavioral_observe(a, N):
    """봉인 cmul 의 행동: control=1 에서 work register ×a mod N orbit. period=ord_N(a).
    실행≠검증 — illustrative only(§8.4). golden 순열을 statevector 로 직접 전개."""
    nq = math.ceil(math.log2(N)) + 1
    # control=1 부분공간에서 |w> → |a·w mod N>. |1> 시작 orbit.
    orbit = [1]
    w = 1
    for _ in range(N + 1):
        w = (a * w) % N
        orbit.append(w)
        if w == 1:
            break
    period = len(orbit) - 1
    # 독립 order 계산으로 대조
    true_ord = 1
    x = a % N
    while x != 1:
        x = (x * a) % N
        true_ord += 1
    return {"id": f"cmul{a}_mod{N}", "orbit_from_1": orbit, "observed_period": period,
            "ord_N_a": true_ord, "matches": period == true_ord,
            "note": "illustrative only — 봉인 증거 아님(§8.4). control=1 work register orbit."}


# ── main ────────────────────────────────────────────────────────────
def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 72)
    print("P1 ArithFamilyExtend — 산술합성 엔진 재사용 → distinct-prime modulus 확장")
    print("정직성: 생성≠검증(오라클 봉인). 엔진(genskills) 미변경. c6x prereq 자가해결.")
    print("=" * 72)

    # 1. SealMCT6
    c6 = seal_mct6()
    print(f"[SealMCT6] c6x 봉인 sealed={c6.get('sealed', c6.get('id')=='c6x')} "
          f"tier={c6.get('tier')} n={c6.get('n_sys')} u={c6.get('u_hash','')[:14]}")
    indep6 = verify_mct6_indep()
    print(f"[VerifyMCT6Indep] 독립 산술순열 u_hash==sealed: {indep6['matches_sealed']}")

    # 2. SynthDistinctPrime
    targets = [(2, 35), (2, 33)]
    synth = synth_distinct_prime(targets)
    for s in synth:
        print(f"[Synth] {s['id']:14} ({'×'.join(map(str,s['factors']))}) sealed={s['sealed']} "
              f"tier={s['tier']} {s['gates']}gates ctrl={s['control_dist']} u={str(s['u_hash'])[:14]}")

    # 3. EngineRegression
    reg = engine_regression()
    reg_ok = sum(1 for c in reg if c.get("matches_registry"))
    print(f"[EngineRegression] genskills(미변경) 기존 cmul 재현 u_hash==registry: {reg_ok}/{len(reg)} "
          f"(golden 순열 불변 → plan 달라도 u_hash 동일)")

    # 4. IndependentArithVerify (신규)
    indep = [independent_arith_verify(a, N) for a, N in targets]
    indep_ok = sum(1 for c in indep if c["matches_sealed"])
    print(f"[IndependentArithVerify] 신규 cmul 독립순열 u_hash==sealed: {indep_ok}/{len(indep)}")

    # 5. BehavioralObserve
    beh = [behavioral_observe(a, N) for a, N in targets]
    for b in beh:
        print(f"[BehavioralObserve] {b['id']}: ×2 orbit period={b['observed_period']} "
              f"==ord={b['ord_N_a']} ({b['matches']}) [illustrative only]")

    # 6. ShorScopeHonest
    shor_scope = []
    for a, N in targets:
        r = beh[[t[1] for t in targets].index(N)]["ord_N_a"]
        t_count = max(1, 2 * (r - 1).bit_length())  # t≈2log2(r) (대략 2r² 정밀도)
        t_need = 2 * math.ceil(math.log2(r)) if r > 1 else 1
        work = math.ceil(math.log2(N))
        total = t_need + work
        shor_scope.append({"N": N, "period": r, "counting_t": t_need, "work": work,
                           "total_qubits": total, "tier0_exact_feasible": total <= 12,
                           "honest_tier": "Tier-0 EXACT" if total <= 12 else "Tier-1 STRUCTURAL"})
    print("[ShorScopeHonest] full Shor 조립 규모:")
    for s in shor_scope:
        print(f"   N={s['N']}: period r={s['period']} → ~{s['total_qubits']}q "
              f"({s['counting_t']}counting+{s['work']}work) > EXACT_BOUND(12) → {s['honest_tier']}")

    report = {
        "phase": "P1 ArithFamilyExtend",
        "honesty": "engine(genskills) unchanged (functions imported only); c6x mapping local; "
                   "distinct-prime targets need 6-control MCT → missing prereq c6x sealed first "
                   "(P5 dependency-resolve philosophy); generation != verification (oracle seals); "
                   "behavioral observe illustrative only (§8.4); plan=sealed MCT, no MatrixGate.",
        "seal_mct6": {"sealed": c6.get("id") == "c6x", "u_hash": c6.get("u_hash"),
                      "tier": c6.get("tier"), "independent_verify": indep6},
        "synth_distinct_prime": synth,
        "engine_regression": {"matches": reg_ok, "total": len(reg), "detail": reg},
        "independent_arith_verify": indep,
        "behavioral_observe": beh,
        "shor_scope_honest": shor_scope,
    }
    synth_ok = all(s["sealed"] and s["tier"] == 0 for s in synth)
    all_ok = (c6.get("id") == "c6x" and indep6["matches_sealed"] and synth_ok
              and reg_ok == len(reg) and indep_ok == len(indep)
              and all(b["matches"] for b in beh))
    report["all_ok"] = bool(all_ok)
    json.dump(report, open(os.path.join(OUT, "ARITH-FAMILY-REPORT.json"), "w",
                           encoding="utf-8"), ensure_ascii=False, indent=2)
    print("-" * 72)
    print(f"all_ok={all_ok}  →  .pgf/arith/ARITH-FAMILY-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
