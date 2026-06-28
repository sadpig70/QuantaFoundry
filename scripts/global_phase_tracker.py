"""global_phase_tracker.py — W1.3 (A2 고유통찰): 전역위상 floating 추적 + controlled 합성 안전.

A2 우려: C4(골든 비교)는 전역위상을 atol 무시한다. single-gate 봉인에서는 정당(전역위상 관측 불가)
하지만 봉인 모듈 U 를 **controlled-U 하위블록**으로 합성하면 무시됐던 전역위상 e^{iφ} 가 |1⟩ 분기에만
걸리는 *상대위상*으로 변모해 알고리즘을 깨뜨린다. 즉 "U 를 봉인했으니 c-U 도 안전"이라는 재사용이
전역위상에서 샐 수 있다.

본 모듈(비파괴 분석 레이어):
  1. 48 모듈의 전역위상 자유도 명시 — 각 봉인이 C4 로 무시한 전역위상은 *미보증*임을 기록.
  2. controlled-pair 정합 검증(teeth) — 라이브러리의 controlled 게이트가 base 의 *정확한* controlled
     (diag-block(I, base), 전역위상 포함)와 일치하는지 확인. 일치 = base 전역위상이 canonical → 합성 안전.
  3. controlled-wrapping 정적 스캔 — 앱 plan 이 봉인 모듈을 controlled 로 wrap 하는 패턴 탐지(현재 0;
     미래 goal-autonomy/discover 가 생성 시 가드 필요).

비파괴: sealed.json/oracle/frozen 미변경(sealed 메타 기록 불가=fingerprint 결합). `registry/GLOBAL-PHASE.json` 가산.
"""
import os, sys, json, glob, re
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
from second_oracle import INDEP   # noqa: E402  제1원리 게이트

APPS = os.path.join(ROOT, "specs", "apps")
APPREG = os.path.join(ROOT, "registry", "apps")
OUT = os.path.join(ROOT, "registry", "GLOBAL-PHASE.json")

# (base 1q gate, 라이브러리 controlled gate) — controlled 가 base 의 정확한 controlled 인가?
CONTROLLED_PAIRS = [("x_gate", "cnot"), ("z_gate", "cz"), ("s_gate", "cs_gate"), ("t_gate", "ct_gate")]


def canonical_global_phase(U):
    """C4 가 무시하는 전역위상 = 첫 비영 원소의 위상(canonical hash 기준)."""
    flat = np.asarray(U, complex).flatten()
    nz = flat[np.abs(flat) > 1e-9]
    return float(np.angle(nz[0])) if len(nz) else 0.0


def controlled_of(U1q):
    """1q U → 2q controlled (control=q0=MSB big-endian): diag-block(I2, U)."""
    C = np.eye(4, dtype=complex)
    C[2:, 2:] = U1q
    return C


def check_controlled_pairs():
    rows = []
    for base, cgate in CONTROLLED_PAIRS:
        if base not in INDEP or cgate not in INDEP:
            continue
        Ub = INDEP[base](); Uc = INDEP[cgate]()
        expect = controlled_of(Ub)
        match = bool(np.allclose(expect, Uc, atol=1e-9))   # 전역위상까지 정확(allclose, not phase-free)
        rows.append({"base": base, "controlled": cgate, "exact_match": match,
                     "base_global_phase": round(canonical_global_phase(Ub), 6)})
    return rows


def scan_controlled_wrapping():
    """앱 plan 이 모듈을 controlled 로 wrap 하는 패턴 탐지 — 현재 라이브러리는 controlled 를 직접 봉인."""
    flagged = []
    for p in sorted(glob.glob(os.path.join(APPS, "*.app.pg"))):
        txt = open(p, encoding="utf-8").read()
        if re.search(r'"control"|"wrap"|controlled_of|add_control', txt):   # 보수적 패턴
            flagged.append(os.path.basename(p))
    return flagged


def main():
    print("=" * 82)
    print("global_phase_tracker (W1.3) — 전역위상 floating 추적 + controlled 합성 안전")
    print("=" * 82)

    # 1. 전역위상 자유도
    phases = {gid: round(canonical_global_phase(fn()), 6) for gid, fn in INDEP.items()}
    bearing = {g: p for g, p in phases.items() if abs(p) > 1e-9}

    # 2. controlled-pair 정합(teeth)
    pairs = check_controlled_pairs()
    all_pair_ok = all(r["exact_match"] for r in pairs)
    print("\ncontrolled-pair 정합(base 전역위상이 controlled 합성에 정합 = 안전):")
    for r in pairs:
        print(f"   {'✓' if r['exact_match'] else '✗'} {r['controlled']:10} == controlled({r['base']}) "
              f"(전역위상까지 정확)  base_phase={r['base_global_phase']}")

    # 3. controlled-wrapping 정적 스캔
    wrapped = scan_controlled_wrapping()
    print(f"\ncontrolled-wrapping 앱(모듈을 controlled 로 재사용): {len(wrapped)} "
          f"{wrapped if wrapped else '(없음 — 현재 라이브러리는 controlled 를 직접 봉인=안전)'}")

    print(f"\n전역위상 보유(canonical phase≠0) 모듈: {len(bearing)}/48 "
          f"(single-gate 봉인엔 무해; controlled 합성 시 정합 필요)")

    out = {"_schema": "global-phase-v1",
           "_note": "C4 는 single-gate 전역위상을 정당히 무시(관측 불가). 위험은 controlled 합성 시 발현. "
                    "controlled-pair 정합으로 base 전역위상이 canonical 임을 실증 → 합성 안전. 비파괴.",
           "canonical_global_phase": phases,
           "controlled_pairs": pairs, "controlled_pairs_all_exact": all_pair_ok,
           "controlled_wrapping_apps": wrapped,
           "phase_bearing_modules": bearing,
           "guard_note": "goal-autonomy/discover 가 모듈을 controlled 로 wrap 하면 전역위상 정합을 "
                         "반드시 검증해야 함(현재 패턴 0). diag-block(I,U) 합성은 U 의 전역위상을 보존해야 한다."}
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("\n" + "-" * 82)
    print(f"controlled-pair {'ALL EXACT ✅' if all_pair_ok else 'MISMATCH ✗'} · "
          f"wrapping 위험 {len(wrapped)} · 리포트: {os.path.relpath(OUT, ROOT)}")
    print("=" * 82)
    return 0 if all_pair_ok and not wrapped else 1


if __name__ == "__main__":
    sys.exit(main())
