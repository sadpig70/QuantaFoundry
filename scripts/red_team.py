# -*- coding: utf-8 -*-
"""
red_team.py — P3 FalsificationFront (task_plan_pg §P3, self-contained)

검증 시스템(오라클 contracts·guards + KeyFreeConsensus 게이트)을 *적대적으로* 시험한다.
공격을 구성해 결정론 방어선이 거부하는지 정량화하고, 뚫리는 것은 **문서화된 공백**으로 정직
보고한다. "검증이 신뢰자본을 축적한다"는 명제를 정작 미검증인 지점에서 실증(방향서 §7).

═══════════════════════════════════════════════════════════════════════════
sub-PG
═══════════════════════════════════════════════════════════════════════════
P3_FalsificationFront
    P3a_RedTeamSuite
        MatrixGateShortcut  // bloq=MatrixGate(golden) → honest-분해 우회 (코드 강제 있나?)
        GoldenCopyAttack    // golden이 bloq 자기참조 → golden_independence_guard
        IdentityGolden      // 비자명 모듈에 항등 golden → golden_guard (reward-hacking)
        UncomputeLeak       // ancilla 얽힘(누출) → C3 AncillaClean
        ConventionSplit     // endianness 오해 golden → u_hash 분기 → DIVERGENT
        CoErrorB4           // 같은-weights 동반오류 → independence_unit (P2a 재확인)
    P3b_Tier1ScaleFalsify   // 방향서 §7 최고위험: 구조통과·유니터리오류 합성
        StructPassUnitFail  // sealed children+정상 plan, 조립 unitary≠intent
        TierBoundary        // Tier-1 STRUCTURAL 봉인되나? Tier-0 dense 만 거부하나?
    P3c_SingleVsConsensus   // 단일출처 봉인 vs 합의·게이트·오라클 거부 검출률 매트릭스

정직성: 오라클/게이트/consensus 는 *시험만*(사용), 변경 0. 공격은 temp store. 기존 봉인·frozen
무변경. 뚫린 공격은 *이미 설계상 알려진 경계*(예: Tier-1=structural_wellformed≠unitary_equiv)를
정량 확인하는 것 — 새 버그 주장 아님. 결과는 .pgf/redteam/ (비파괴).
"""
from __future__ import annotations

import os
import sys
import json
import tempfile
import subprocess

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, ORACLE)
sys.path.insert(0, os.path.join(ROOT, ".pgf", "keyfree"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import verify_seal as vs        # noqa: E402
import contracts as ct          # noqa: E402
import spec_guard as sg         # noqa: E402
import golden_guard as gg       # noqa: E402
import app_assemble as aa       # noqa: E402
import consensus as cc          # noqa: E402
import gated_panel as gp        # noqa: E402

OUT = os.path.join(ROOT, ".pgf", "redteam")
TMP = tempfile.mkdtemp(prefix="redteam_")


def _write(path, text):
    open(path, "w", encoding="utf-8", newline="\n").write(text)
    return path


def _seal_module(spec_text, name):
    """temp store 에서 verify_seal 실행 → (sealed?, reason)."""
    p = _write(os.path.join(TMP, f"{name}.pg"), spec_text)
    r = subprocess.run([sys.executable, os.path.join(ORACLE, "verify_seal.py"), p, "--out", TMP],
                       capture_output=True, text=True, cwd=ORACLE)
    sealed = os.path.exists(os.path.join(TMP, f"{name}.sealed.json"))
    return sealed, (r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout + r.stderr).strip() else ""


# ── P3a 공격 ────────────────────────────────────────────────────────
def attack_matrixgate():
    """bloq=MatrixGate(golden) → 정직 분해 회피. 봉인되면 documented gap(분해정직=사회적 규약)."""
    spec = ('```python id=bloq\n'
            'import cirq, numpy as np\n'
            'from qualtran.cirq_interop import cirq_gate_to_bloq\n'
            'U = np.array([[0,1],[1,0]],dtype=complex)\n'
            'bloq = cirq_gate_to_bloq(cirq.MatrixGate(U))   # 정직 분해 우회\n'
            '```\n'
            '```python id=golden\nimport numpy as np\ngolden = np.array([[0,1],[1,0]],dtype=complex)\n```\n'
            '```json id=meta\n{"id": "atk_matrixgate", "n_sys": 1, "n_anc": 0}\n```\n')
    sealed, reason = _seal_module(spec, "atk_matrixgate")
    return {"attack": "matrixgate-shortcut", "defense": "honest-decomposition(코드강제?)",
            "sealed": sealed, "caught": not sealed,
            "note": ("봉인됨 → DOCUMENTED GAP: bloq=MatrixGate 가 코드로 막히지 않음(분해정직은 사회적 "
                     "규약). 단 golden==bloq 자명일치라 u_hash 는 정확 — '검증 무력화'가 아니라 "
                     "'분해 노력 회피'. honest 라이브러리 규율로 관리." if sealed
                     else f"거부됨: {reason[:80]}")}


def attack_golden_copy():
    """golden 이 bloq 변수 참조(자기참조) → golden_independence_guard 정적 차단."""
    spec_text = ('```python id=bloq\nfrom qualtran.bloqs.basic_gates import XGate\nbloq = XGate()\n```\n'
                 '```python id=golden\nimport numpy as np\n'
                 'golden = bloq.tensor_contract()   # 자기참조 복사\n```\n'
                 '```json id=meta\n{"id": "atk_goldencopy", "n_sys": 1, "n_anc": 0}\n```\n')
    p = _write(os.path.join(TMP, "atk_goldencopy.pg"), spec_text)
    spec = vs.load_pg_spec(p)
    v = gg.golden_independence_guard(spec)
    return {"attack": "golden-copy(self-reference)", "defense": "golden_independence_guard(AST)",
            "blocked": v.block, "caught": v.block, "reason": v.reason[:80]}


def attack_identity_golden():
    """비자명 모듈에 항등 golden → golden_guard(reward-hacking) 차단."""
    spec_text = ('```python id=bloq\nfrom qualtran.bloqs.basic_gates import XGate\nbloq = XGate()\n```\n'
                 '```python id=golden\nimport numpy as np\ngolden = np.eye(2,dtype=complex)   # 빈 모듈\n```\n'
                 '```json id=meta\n{"id": "atk_identity", "n_sys": 1, "n_anc": 0}\n```\n')
    p = _write(os.path.join(TMP, "atk_identity.pg"), spec_text)
    spec = vs.load_pg_spec(p)
    v = sg.spec_quality_guard(spec)
    return {"attack": "identity-golden(empty module)", "defense": "spec_quality_guard/golden_guard",
            "blocked": v.block, "caught": v.block, "reason": v.reason[:80]}


def attack_uncompute_leak():
    """ancilla 를 |0>로 되돌리지 않는 잘못된 uncompute → C3 AncillaClean 차단.
    규약: ancilla=MSB(outer), sys=LSB. ctrl=sys, target=anc → 입력 anc=0 인데 출력 anc=1(누출)."""
    # basis idx = anc*2+sys (sys=LSB, anc=MSB). 입력 anc=0(열 0,1) 인데 열1이 anc=1 행(2,3)로 누출.
    U = np.array([[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]], complex)
    # run_contracts 는 예외가 아니라 ContractResult(all_passed, signal) 를 반환한다(봉인 파이프라인 규약).
    res = ct.run_contracts(U, n_sys=1, n_anc=1)
    caught = (not res.all_passed) and res.signal.get("contract") == "C3"
    reason = res.signal.get("reason_code", res.signal.get("reason", ""))[:80]
    return {"attack": "uncompute-leak(ancilla entangled)", "defense": "C3 AncillaClean",
            "caught": caught, "reason": reason}


def attack_convention_split():
    """endianness 오해로 다른 u_hash → cross-model 합의가 DIVERGENT 로 거부."""
    # 같은 의도(controlled-X)를 big-endian vs little-endian 으로 → 다른 u_hash
    U_be = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], complex)  # ctrl=MSB
    U_le = np.array([[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]], complex)  # ctrl=LSB
    sources = [cc.Source("cx_m1", "model", "w1", cc.uhash(U_be)),
               cc.Source("cx_m2", "model", "w2", cc.uhash(U_le))]
    r = cc.establish_truth("atk_convention", sources, N=2)
    return {"attack": "convention-split(endianness)", "defense": "cross-model independent_votes",
            "status": r.status, "caught": r.status != "ESTABLISHED",
            "reason": (r.escalation or "")[:80]}


def attack_co_error_b4():
    """같은-weights 2페르소나 동반오류 → independence_unit 1 → 게이트 거부 (P2a 재확인)."""
    bad = cc.uhash(np.eye(2, dtype=complex))   # 둘 다 같은 (틀린) 답
    s = [cc.Source("x_p1", "model", "same-w", bad), cc.Source("x_p2", "model", "same-w", bad)]
    panel = gp.dispatch_policy("new_family")
    dec = gp.gated_seal("atk_b4", panel, s)
    return {"attack": "co-error/B4(same-weights)", "defense": "independence_unit + gate",
            "decision": dec.decision, "caught": dec.decision == "REJECT", "reason": dec.reason[:80]}


# ── P3b Tier-1 scale 반증 (§7 최고위험) ─────────────────────────────
def tier1_scale_falsify():
    """구조통과·유니터리오류: sealed children + 정상 plan 이나 조립 unitary≠intent.
    golden 없는 앱 → Tier-1 STRUCTURAL 봉인(intent 미검증). golden 있고 n≤12 → Tier-0 거부."""
    # 의도 = GHZ3 (H q0 + CNOT 0-1 + CNOT 1-2). 공격 = CNOT 1-2 를 1-0 으로 오배선(구조적으론 유효).
    # temp 앱 spec 을 specs/apps 에 둬야 ../modules 해결 (assemble 은 TMP store, registry 무오염).
    apps_dir = os.path.join(ROOT, "specs", "apps")
    tmp_specs = []
    wrong_plan = ('{"steps": [{"spec": "../modules/h_gate.pg", "targets": [0]},'
                  '{"spec": "../modules/cnot.pg", "targets": [0,1]},'
                  '{"spec": "../modules/cnot.pg", "targets": [1,0]}]}')  # 마지막 오배선
    # (A) golden 없는 앱 → Tier-1 structural
    app_no_golden = ('# atk_tier1 — golden 없는 앱(오배선 plan). Tier-1 structural 경로.\n'
                     '```json id=app_meta\n{"id": "_atk_tier1_nogolden", "n_sys": 3, "n_anc": 0}\n```\n'
                     f'```json id=plan\n{wrong_plan}\n```\n')
    pA = _write(os.path.join(apps_dir, "_atk_tier1_nogolden.app.pg"), app_no_golden)
    tmp_specs.append(pA)
    vA = aa.assemble(pA, TMP)
    # (B) 같은 오배선 plan + 올바른 GHZ3 golden → Tier-0 C-app 대조
    ghz3_golden = ('import numpy as np\n'
                   'H=np.array([[1,1],[1,-1]],dtype=complex)/np.sqrt(2)\n'
                   'CN=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]],dtype=complex)\n'
                   'I2=np.eye(2)\n'
                   'golden=np.kron(I2,CN)@np.kron(CN,I2)@np.kron(H,np.eye(4))')
    app_golden = ('# atk_tier1 — 올바른 GHZ3 golden + 오배선 plan. Tier-0 dense 대조.\n'
                  '```json id=app_meta\n{"id": "_atk_tier1_golden", "n_sys": 3, "n_anc": 0}\n```\n'
                  f'```python id=app_golden\n{ghz3_golden}\n```\n'
                  f'```json id=plan\n{wrong_plan}\n```\n')
    pB = _write(os.path.join(apps_dir, "_atk_tier1_golden.app.pg"), app_golden)
    tmp_specs.append(pB)
    vB = aa.assemble(pB, TMP)
    for sp in tmp_specs:                     # specs/apps 오염 방지
        try:
            os.remove(sp)
        except OSError:
            pass
    return {
        "attack": "Tier-1 scale (struct-pass / unit-fail)",
        "tier1_no_golden": {"sealed": vA.sealed, "tier": vA.tier,
                            "u_hash": (vA.u_hash or "")[:12]},
        "tier0_with_golden": {"sealed": vB.sealed, "tier": vB.tier, "reason": (vB.reason or "")[:80]},
        "falsified": (vA.sealed and not vB.sealed),
        "interpretation": ("§7 반증 성립(설계상 경계 확인): Tier-1 STRUCTURAL 은 오배선 plan 을 "
                           "봉인(intent 미검증) — structural_wellformed≠unitary_equiv. Tier-0 dense "
                           "C-app 만 composite≠golden 으로 거부. 따라서 teeth 는 dense/Tier-0(및 "
                           "Clifford 는 P0 Tier-2)에 있고, golden 없는 Tier-1 은 unitary 정확성을 "
                           "보증하지 않음(semantic_guarantee 가 이미 그렇게 라벨)."),
    }


def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 76)
    print("P3 FalsificationFront — 검증 시스템 적대적 시험(red-team)")
    print("정직성: 오라클/게이트 시험만(변경0). 뚫린 공격=문서화된 경계(설계상). 비파괴.")
    print("=" * 76)

    p3a = [attack_matrixgate(), attack_golden_copy(), attack_identity_golden(),
           attack_uncompute_leak(), attack_convention_split(), attack_co_error_b4()]
    print("[P3a RedTeamSuite] 공격 → 방어선 거부:")
    for a in p3a:
        mk = "✓ CAUGHT" if a["caught"] else "✗ SLIPPED(gap)"
        print(f"  {mk:16} {a['attack']:32} [{a['defense']}]")

    p3b = tier1_scale_falsify()
    print(f"[P3b Tier-1 scale 반증] golden없는 Tier-1 봉인={p3b['tier1_no_golden']['sealed']}"
          f"(tier {p3b['tier1_no_golden']['tier']}) · Tier-0(golden) 거부="
          f"{not p3b['tier0_with_golden']['sealed']} → 반증성립={p3b['falsified']}")

    # P3c: 단일출처 vs 합의/오라클 검출률
    caught = sum(1 for a in p3a if a["caught"])
    catchable = [a for a in p3a if a["attack"] not in ("matrixgate-shortcut",)]  # gap 제외
    p3c = {
        "attacks": len(p3a), "caught_by_some_defense": caught,
        "documented_gaps": [a["attack"] for a in p3a if not a["caught"]],
        "single_source_would_seal_but_consensus_rejects": ["convention-split", "co-error/B4"],
        "tier1_unitary_gap_closed_for_clifford_by_P0": True,
    }
    print(f"[P3c 검출률] {caught}/{len(p3a)} 방어선 거부 · 공백={p3c['documented_gaps']} · "
          f"단일=봉인/합의=거부: {p3c['single_source_would_seal_but_consensus_rejects']}")

    report = {
        "phase": "P3 FalsificationFront (self-contained P3a+P3b+P3c)",
        "honesty": "oracle/gate/consensus tested only (zero modification); attacks in temp store; "
                   "existing seals/frozen untouched; SLIPPED attacks = already-designed boundaries "
                   "quantified (not new bugs), e.g. Tier-1=structural_wellformed by design; "
                   "ReproBounty(P3d) stays BLOCKED (public/external).",
        "p3a_red_team": p3a,
        "p3b_tier1_scale_falsify": p3b,
        "p3c_catch_rate": p3c,
        "p3d_blocked": "ReproBounty: public adversarial challenge needs publishing + external participants.",
    }
    # 모든 의도된 방어선이 작동(매트릭스 gap 제외) + Tier-1 반증이 설계대로 성립
    designed_defenses_ok = all(a["caught"] for a in p3a if a["attack"] != "matrixgate-shortcut")
    all_ok = designed_defenses_ok and p3b["falsified"]
    report["all_ok"] = bool(all_ok)
    json.dump(report, open(os.path.join(OUT, "FALSIFICATION-REPORT.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("-" * 76)
    print(f"designed_defenses_ok={designed_defenses_ok} · tier1_falsified={p3b['falsified']} "
          f"→  .pgf/redteam/FALSIFICATION-REPORT.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
