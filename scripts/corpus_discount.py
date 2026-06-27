"""corpus_discount.py — corpus 상관 할인 ρ 추정 + 효과 분석 (R-I 코드화).

리뷰 R-I: distinct weights 라도 학습 코퍼스가 겹치면 모델끼리 prior(Schelling)를 공유 →
"N개 모델 합의"가 N개 독립 확증이 아니다. 이 도구는:
  1. '정답이 임의/부재한' 의도(=corpus 상관만 수렴 유발)에서 ρ 를 추정한다.
  2. ρ 를 confidence_grade 에 주입했을 때 model-only 합의 등급이 어떻게 강등되는지 보여준다.

정직성(중요): ρ 은 *정답이 없는* 의도에서만 깨끗하다.
  - R5c(v04_hard) Class B 모호의도는 Schelling-정답이 섞여(상관 vs 정확성 혼동) ρ 를 *과대추정* → 상한.
  - v0.5(v05_div) Class C 자유파라미터는 정답이 부재 → ρ 의 *정본* 추정원(EXT 수급 후).

사용:
  python scripts/corpus_discount.py                 # 기본 v04_hard (상한 추정)
  python scripts/corpus_discount.py --dir v05_div   # v0.5 Class C (정본, 수급 후)
"""
import sys, os, json, glob
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, ".pgf", "keyfree"))
import consensus as C  # noqa: E402

# 의도별 그럴듯한 default 개수(이산이면 우연일치 보정). 모르면 continuum(c≈0) 취급.
K_DEFAULTS = {
    "amb_cnot_endianness": 2,      # control = q0 / q1
    "amb_iqft2_bitrev": 2,         # raw / bit-reversal
    "amb_cphase": 4,               # CZ/CS/CT/... canonical 후보 소수
    "free_cphase": None, "free_rz": None,            # 연속 자유각 → c≈0
    "split_rz_sign": 2, "split_ry_dir": 2, "split_csqrtz_sign": 2,
}
# '정답 없음/임의' 클래스 prefix (ρ 추정 대상). A/S(정답 있음)는 제외.
ARBITRARY_CLASS_PREFIX = ("B:", "C:", "D:")


def _matrix(s):
    return np.array(s["app_golden_real"], float) + 1j * np.array(s["app_golden_imag"], float)


def selftest():
    """estimate_corpus_rho 동작 검증(합성)."""
    print("[selftest] estimate_corpus_rho")
    cases = [
        ("all-distinct continuum", [["a", "b", "c", "d"]], None, 0.0),
        ("all-same continuum",     [["a", "a", "a", "a"]], None, 1.0),
        ("all-same k=2",           [["a", "a", "a", "a"]], [2], 1.0),
        ("half-half k=2",          [["a", "a", "b", "b"]], [2], 0.0),
    ]
    ok = True
    for name, hs, k, exp in cases:
        r = C.estimate_corpus_rho(hs, k_defaults=k)["rho"]
        good = abs(r - exp) < 0.02
        ok &= good
        print(f"   {'PASS' if good else 'FAIL'} {name}: rho={r} (expect {exp})")
    return ok


def main():
    dirname = "v04_hard"
    if "--dir" in sys.argv:
        dirname = sys.argv[sys.argv.index("--dir") + 1]
    cm = os.path.join(ROOT, "_workspace", "crossmodel", dirname)
    sub_dir = os.path.join(cm, "submissions")
    intents = json.load(open(os.path.join(cm, "app_intents.json"), encoding="utf-8"))["intents"]
    cls = {it["id"]: it.get("class", "") for it in intents}
    targets = [it["id"] for it in intents if it.get("class", "").startswith(ARBITRARY_CLASS_PREFIX)]

    print("=" * 86)
    print(f"corpus-correlation ρ 추정 (R-I) — dir={dirname}")
    print("=" * 86)
    st_ok = selftest()
    print()
    files = sorted(glob.glob(os.path.join(sub_dir, "*.app.json")))
    if not files:
        print(f"  제출물 없음: {sub_dir} — 브리프 relay 후 재실행"); return 1
    print(f"  런타임 {len(files)}개 · ρ 추정 대상(정답없음) 의도 {len(targets)}: {targets}")

    # 의도별 distinct-weights u_hash 수집
    per_intent_hashes, k_list = [], []
    rows_dump = {}
    for iid in targets:
        by_w = {}
        for f in files:
            d = json.load(open(f, encoding="utf-8"))
            wid = d.get("weights_id", os.path.basename(f).split(".")[0])
            for s in d.get("submissions", []):
                if s.get("id") == iid:
                    try:
                        by_w[wid] = C.uhash(_matrix(s))
                    except Exception:
                        pass
        hs = list(by_w.values())
        if len(hs) >= 2:
            per_intent_hashes.append(hs)
            k_list.append(K_DEFAULTS.get(iid))
            rows_dump[iid] = {"n_weights": len(hs), "distinct": len(set(hs)),
                              "unanimous": len(set(hs)) == 1, "k_defaults": K_DEFAULTS.get(iid)}

    est = C.estimate_corpus_rho(per_intent_hashes, k_defaults=k_list)
    rho = est["rho"]
    contaminated = dirname == "v04_hard" or any(c.startswith("B:") for c in cls.values())

    print("\n  의도별 일치:")
    for iid, r in rows_dump.items():
        print(f"    {iid:22} weights={r['n_weights']} distinct={r['distinct']} "
              f"{'만장일치' if r['unanimous'] else '분기'} k={r['k_defaults']}")
    print(f"\n  추정 ρ = {rho}  ({'상한(R5c 오염: Schelling-정답 혼입)' if contaminated else '정본(정답부재 의도)'})")

    # 효과: model-only 합의 N개에 ρ 적용 시 등급 강등
    print("\n  효과(model-only 합의 등급, proof-backed 는 불변):")
    print(f"    {'N_models':>8} {'N_eff(ρ)':>9}  grade@ρ=0     grade@ρ={rho}")
    eff_dump = []
    for n in (2, 3, 6):
        units = {f"model:w{i}" for i in range(n)}
        g0 = C.confidence_grade(units, rho=0.0)
        gr = C.confidence_grade(units, rho=rho)
        neff = C.effective_independent_count(n, rho)
        print(f"    {n:>8} {neff:>9.2f}  {g0:12}  {gr}")
        eff_dump.append({"n_models": n, "n_eff": round(neff, 3), "grade_rho0": g0, "grade_rho": gr})

    print("\n  해석: proof/structural 축이 있으면 PROOF_BACKED(corpus 무관) — 할인 없음. "
          "\n        model-only 합의는 ρ 가 클수록 유효 독립<2 로 CORPUS_CORRELATED 강등 → escalate.")
    print("=" * 86)

    out = {"dir": dirname, "rho": rho, "contaminated_upper_bound": bool(contaminated),
           "selftest_pass": bool(st_ok), "per_intent": est["per_intent"], "intent_rows": rows_dump,
           "effect_model_only": eff_dump,
           "note": "ρ 은 정답부재 의도에서만 정본. R5c(v04_hard)는 Schelling-정답 혼입으로 상한. "
                   "정본 추정은 v05_div Class C(free parameter) 수급 후. proof-backed 키는 corpus 무관(불변)."}
    op = os.path.join(cm, "CORPUS-RHO.json")
    json.dump(out, open(op, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"리포트: {os.path.relpath(op, ROOT)}")
    return 0 if st_ok else 1


if __name__ == "__main__":
    sys.exit(main())
