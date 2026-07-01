#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inverted_second_oracle — V08_5 ConventionIndependence (A3 리뷰: 규약 뒤집은 오라클).

second_oracle(71/71)은 *하나의* 규약(big-endian · canonical 전역위상 · QUANT atol 격자)으로 봉인
u_hash 를 재현한다. 그 규약 자체가 우연이면 검증은 규약-순환적일 수 있다(A1/2/3 최약가정: 공유 규약
오류 = vacuous seal). 이 오라클은 **규약을 변주해도 동일 seal 을 재현함**을 실증한다:

  (1) phase-convention 독립: 임의 전역위상 e^{iθ}·U 를 곱해도 hash_unitary(U) 재현
        → 봉인이 특정 위상 기준점에 의존하지 않음(전역위상 동치류의 정규 대표원).
  (2) atol-convention 독립: 양자화 격자(QUANT) *이내* 미세섭동을 흡수해 동일 hash
        → 봉인이 격자 규약의 정확한 경계선택에 의존하지 않음.

teeth(공허하지 않음): 전역이 *아닌* 상대위상, 격자 *밖* 섭동은 반드시 불일치해야 한다.

honest 경계: endian 은 표현 규약이라 seal 은 특정 endian(big)에 *고정*된다(little-endian 은
bit-reversal 로 연결된 다른 표현) — 규약-불변이 아니라 규약-고정. 이는 정직하게 표기하며, 규약-불변
축은 위상/atol 이다. 측정도구 vs.hash_unitary 는 공유(사용만) — 변주는 *입력 규약*에 가한다.

사용: python scripts/inverted_second_oracle.py [--quick]
"""
import os, sys, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts"))
import verify_seal as vs           # noqa: E402  (공통 측정도구 — 사용만)
sys.path.insert(0, HERE)
import second_oracle as so         # noqa: E402  (제1원리 INDEP 게이트 재사용)

OUT = os.path.join(ROOT, ".pgf", "proofs", "CONVENTION-INDEPENDENCE.json")
SEED = 20260701
PHASES = [0.37, 1.9, -2.6, np.pi / 3, 3.0, -0.88]   # 전역위상 변주


def _sealed_uhash(gid):
    p = os.path.join(so.MODREG, f"{gid}.sealed.json")
    return json.load(open(p, encoding="utf-8"))["u_hash"] if os.path.exists(p) else None


def check_gate(gid, U, sealed):
    """규약 변주 하 seal 재현 + teeth. → dict."""
    # (1) phase-convention 독립: 전역위상 곱 → 동일 hash
    phase_indep = all(vs.hash_unitary(np.exp(1j * th) * U) == sealed for th in PHASES)
    # phase teeth: 상대위상(전역 아님) — 최대원소 하나에만 위상 → 불일치해야
    idx = np.unravel_index(int(np.argmax(np.abs(U))), U.shape)
    Urel = U.copy(); Urel[idx] *= np.exp(1j * 0.5)
    phase_teeth = (vs.hash_unitary(Urel) != sealed)
    # (2) atol-convention 독립: 격자 이내 미세섭동 흡수 → 동일 hash
    eps_in = 10.0 ** (-(vs._PREQUANT + 2))            # QUANT 격자 이내
    atol_indep = (vs.hash_unitary(U + eps_in) == sealed)
    # atol teeth: 격자 밖 섭동 → 불일치해야
    atol_teeth = (vs.hash_unitary(U + 1e-3) != sealed)
    ok = phase_indep and atol_indep and phase_teeth and atol_teeth
    return {"phase_indep": phase_indep, "atol_indep": atol_indep,
            "phase_teeth": phase_teeth, "atol_teeth": atol_teeth, "ok": ok}


def main():
    quick = "--quick" in sys.argv
    rows = {}
    n_total = n_ok = 0
    fails = []
    for gid, fn in sorted(so.INDEP.items()):
        sealed = _sealed_uhash(gid)
        if sealed is None:
            continue
        n_total += 1
        r = check_gate(gid, fn(), sealed)
        rows[gid] = r
        if r["ok"]:
            n_ok += 1
        else:
            fails.append((gid, {k: v for k, v in r.items() if v is False}))
    all_ok = (n_ok == n_total) and n_total > 0

    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        report = {"_schema": "convention-independence-v1",
                  "_note": "규약(전역위상·atol 격자) 변주 하 seal 재현 실증 + teeth. "
                           "endian 은 규약-고정(big) — 정직 표기. 측정도구 공유(사용만).",
                  "convention_invariant_axes": ["global-phase", "atol-grid"],
                  "convention_fixed_axes": ["endian(big) — bit-reversal 로 연결된 다른 표현"],
                  "modules_checked": n_total, "modules_ok": n_ok,
                  "failures": fails, "results": rows}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print(f"inverted_second_oracle: 규약-독립 재현 {n_ok}/{n_total} 모듈 "
              f"(phase·atol 변주 불변 + teeth)", flush=True)
        if fails:
            print(f"  ⚠ 규약-의존/무-teeth: {fails}", flush=True)
        print(f"  endian=규약-고정(big, 정직표기) · → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"inverted_second_oracle: all_ok={all_ok}", flush=True)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
