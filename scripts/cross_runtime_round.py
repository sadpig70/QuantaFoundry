# -*- coding: utf-8 -*-
"""
cross_runtime_round.py — P3d round 2: 진짜 cross-runtime 동반오류(corpus 상관) 실측

라운드1 의 cross-runtime 테스트는 공허했다(런타임들이 서로 다른 intent 선택 → 공유표적 0).
이 라운드는 *공통 intent* 를 고정 배포한다. 6 distinct-weights 실런타임을 weights_id(=독립단위,
운영자 provenance 바인딩)로 풀링해 establish_truth 를 돌리고 측정한다:

  - cnot_std (sanity): 알려진 답 → GT 수렴으로 convention 정렬 calibration.
  - cnot_lower (probe): control=q1(LSB) CNOT. 모델이 "표준 CNOT(control=MSB)" 로 반사하면
    *공유 오답* = 진짜 corpus-상관 동반오류. 다수가 틀린 답에 수렴 → ESTABLISHED-wrong = BREAK.

핵심: 여기 단위는 *진짜* 서로 다른 런타임(라운드1 의 위조 peer 아님). 그래서 동반오류가 나오면
게이트는 그것을 정당하게 ESTABLISHED 한다 — ρ=0 의 한계. 그 다음 **ρ-할인**(corpus 상관)을
적용하면 유효 독립<2 로 INSUFFICIENT 강등되는지 시연(기존 방어의 실효 확인).

비파괴: consensus/verify_seal *사용만*. registry/specs/frozen 무변경. 봉인 안 함(측정만).
"""
from __future__ import annotations

import os
import sys
import json
import glob

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, ORACLE)
sys.path.insert(0, os.path.join(ROOT, ".pgf", "keyfree"))
import verify_seal as vs        # noqa: E402
import consensus as cc          # noqa: E402

OUT = os.path.join(ROOT, ".pgf", "bounty")

# 알려진 정답(big-endian, q0=MSB, U[out,in]). round2 내장 기본값. round dir 에 _ground_truth.json
# 이 있으면 그것으로 갱신(라운드-무관). sanity/probe 둘 다 답이 명확 = 정답 존재.
_GT = {
    "cnot_std":   np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], complex),
    "cnot_lower": np.array([[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]], complex),
}
# 가장 그럴듯한 오답(Schelling): probe 에 표준 CNOT 을 반사 출력. (selftest 합성 전용)
_SCHELLING_WRONG = {"cnot_lower": _GT["cnot_std"]}


def load_ground_truth(round_dir):
    """round dir 의 _ground_truth.json(운영자 전용, real/imag)으로 _GT 갱신. 없으면 내장값 유지."""
    p = os.path.join(round_dir, "_ground_truth.json")
    if not os.path.exists(p):
        return
    gt = json.load(open(p, encoding="utf-8"))
    for k, v in gt.items():
        re_ = np.array(v["real"], dtype=float)
        im = np.array(v.get("imag", np.zeros_like(re_)), dtype=float)
        _GT[k] = re_ + 1j * im


def _mat(entry):
    re_ = np.array(entry["golden_real"], dtype=float)
    im = np.array(entry.get("golden_imag", np.zeros_like(re_)), dtype=float)
    return re_ + 1j * im


def measure_intent(intent_id, sources, rho_probe=0.5):
    """진짜 독립단위로 establish_truth. GT 대조 + 동반오류면 ρ-할인 방어 시연."""
    gt = vs.hash_unitary(_GT[intent_id]) if intent_id in _GT else None
    r0 = cc.establish_truth(intent_id, sources, N=2, rho=0.0)
    out = {"intent": intent_id, "n_runtimes": len({s.unit for s in sources}),
           "status": r0.status, "grade": r0.grade, "distribution": r0.distribution}
    if r0.status == "ESTABLISHED":
        out["established_matches_GT"] = (gt is not None and r0.key == gt)
        # 동반오류(틀린 답에 진짜 독립단위 수렴) → corpus-상관 BREAK 후보
        out["co_error_established_wrong"] = (gt is not None and r0.key != gt)
        if out["co_error_established_wrong"]:
            # 기존 방어: ρ>0 corpus 할인 → 유효 독립<2 면 INSUFFICIENT(CORPUS_CORRELATED) 강등
            rrho = cc.establish_truth(intent_id, sources, N=2, rho=rho_probe)
            out["rho_discount"] = {"rho": rho_probe, "status": rrho.status, "grade": rrho.grade,
                                   "defended": rrho.status != "ESTABLISHED"}
    else:
        out["established_matches_GT"] = False
        out["co_error_established_wrong"] = False
    return out


def adjudicate(files):
    by_intent = {}                                   # intent → [Source] (진짜 weights_id 단위)
    per_runtime = []
    for f in files:
        d = json.load(open(f, encoding="utf-8"))
        wid = d.get("weights_id", d.get("runtime", os.path.basename(f)))
        for s in d.get("submissions", []):
            iid = s["id"]
            uh = cc.uhash(_mat(s))
            by_intent.setdefault(iid, []).append(cc.Source(f"{iid}_{wid}", "model", wid, uh))
            gt = vs.hash_unitary(_GT[iid]) if iid in _GT else None
            per_runtime.append({"runtime": d.get("runtime"), "intent": iid,
                                "correct": (gt is not None and uh == gt)})
    return [measure_intent(i, srcs) for i, srcs in sorted(by_intent.items())], per_runtime


def _selftest():
    """합성: (A) 표준-CNOT 반사 co-error 4런타임 → ESTABLISHED-wrong, ρ>0 방어;
             (B) 정답 수렴; (C) 발산. 채점기 결정론 검증."""
    def src(intent, wid, M):
        return cc.Source(f"{intent}_{wid}", "model", wid, cc.uhash(M))
    wrong = _SCHELLING_WRONG["cnot_lower"]; right = _GT["cnot_lower"]
    A = [src("cnot_lower", f"rt{i}", wrong) for i in range(4)]            # 동반오류
    B = [src("cnot_lower", f"rt{i}", right) for i in range(3)]            # 정답 수렴
    other = np.eye(4, dtype=complex)
    C = [src("cnot_lower", "rt0", wrong), src("cnot_lower", "rt1", right),
         src("cnot_lower", "rt2", other)]                                # 발산(각 1)
    rA, rB, rC = measure_intent("cnot_lower", A), measure_intent("cnot_lower", B), measure_intent("cnot_lower", C)
    checks = [
        ("A co-error→wrong", rA["status"] == "ESTABLISHED" and rA["co_error_established_wrong"]),
        ("A ρ-할인 방어", rA.get("rho_discount", {}).get("defended") is True),
        ("B 정답수렴", rB["status"] == "ESTABLISHED" and rB["established_matches_GT"]),
        ("C 발산", rC["status"] == "DIVERGENT"),
    ]
    ok = sum(c for _, c in checks)
    print("[selftest] cross-runtime 채점기 결정론:")
    for name, c in checks:
        print(f"  {'✓' if c else '✗'} {name}")
    print(f"[selftest] {ok}/{len(checks)} 통과")
    return ok == len(checks)


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", default="p3d_round2", help="crossmodel round dir (예: p3d_round3)")
    args = ap.parse_args()
    round_dir = os.path.join(ROOT, "_workspace", "crossmodel", args.round)
    subs = os.path.join(round_dir, "submissions")
    load_ground_truth(round_dir)                 # _ground_truth.json 있으면 _GT 갱신
    rtag = args.round.split("_")[-1].upper()     # round2 → ROUND2
    out_name = f"P3D-{rtag}.json"

    os.makedirs(OUT, exist_ok=True)
    print("=" * 76)
    print(f"P3d {args.round} — cross-runtime 동반오류(corpus 상관) 실측")
    print("정직성: 진짜 weights_id 독립단위 풀링·consensus 사용만·비파괴(봉인 안 함).")
    print("=" * 76)

    selftest_ok = _selftest()
    files = sorted(glob.glob(os.path.join(subs, "*.submission.json")))
    relay_pending = len(files) == 0

    measures, per_runtime = ([], [])
    if not relay_pending:
        measures, per_runtime = adjudicate(files)
        for m in measures:
            tag = ("GT수렴(truth)" if m.get("established_matches_GT") else
                   "동반오류-wrong(BREAK)" if m.get("co_error_established_wrong") else m["status"])
            extra = ""
            if m.get("co_error_established_wrong"):
                rd = m.get("rho_discount", {})
                extra = f" · ρ={rd.get('rho')} 방어={rd.get('defended')}({rd.get('status')})"
            print(f"  [{m['intent']:11}] {m['n_runtimes']}런타임 · {tag}{extra}")

    co_errors = [m for m in measures if m.get("co_error_established_wrong")]
    co_error_undefended = [m for m in co_errors if not m.get("rho_discount", {}).get("defended")]
    report = {
        "phase": f"P3d {args.round} — cross-runtime co-error measurement",
        "honesty": "real weights_id independence units (NOT round-1 forged peers); consensus used "
                   "only; non-destructive (no seal). corpus-correlation ρ-discount demonstrated as "
                   "the existing defense against genuine cross-runtime co-error.",
        "engine_selftest_passed": selftest_ok,
        "submissions_ingested": len(files),
        "relay_pending": relay_pending,
        "measures": measures,
        "per_runtime": per_runtime,
        "co_error_intents": [m["intent"] for m in co_errors],
        "co_error_undefended_by_rho": [m["intent"] for m in co_error_undefended],
        "limitations": (
            "정직한 음성의 범위 한정: (1) 테스트한 probe 들에서 동반오류 0 = co-error '미발생'이지 "
            "'불가능' 증명 아님(probe 가 충분히 적대적이지 못했을 수 있음). (2) 동반오류가 0 이라 "
            "ρ-할인 방어는 *실데이터로 미검증*(selftest 합성으로만 입증). 더 모호한 probe 로 후속 "
            "라운드 시 ρ-경로 실측 가능."
            if not co_errors else
            "동반오류 측정됨(진짜 독립 런타임이 공유 오답 prior 로 수렴) — ρ-할인 방어 여부 measures 참조."),
        "note": (f"RELAY PENDING: {args.round} 패키지 준비 완료, 정욱님 6런타임 공통 intent 수거 대기. "
                 "selftest 로 채점기 결정론만 self-contained 입증." if relay_pending else
                 ("동반오류 측정됨 — ρ-할인 방어 여부는 measures 참조" if co_errors else
                  "동반오류 없음(런타임들이 정답 수렴 또는 발산) — corpus-상관 BREAK 미발생(정직한 음성)")),
    }
    json.dump(report, open(os.path.join(OUT, out_name), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("-" * 76)
    print(f"engine_selftest={selftest_ok} · 제출={len(files)}"
          f"{' (relay 대기)' if relay_pending else ''} · 동반오류 intent={len(co_errors)}"
          f"{f'(ρ-미방어 {len(co_error_undefended)})' if co_errors else ''}"
          f"  →  .pgf/bounty/{out_name}")
    return 0 if selftest_ok else 1


if __name__ == "__main__":
    sys.exit(main())
