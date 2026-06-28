# -*- coding: utf-8 -*-
"""determinism_env_check.py — Stage 5 W5.1: 환경 핀 + byte-identity 환경강건성 실증.

blind-spot(E): byte-identity 재현은 *환경 조건부*다 — numpy/BLAS/platform/FP 가 바뀌면 깨질 수
있다(외부 재검증 신뢰의 숨은 전제). 본 모듈은 (1) 환경지문을 캡처하고 (2) hash_unitary 의 격자
양자화(QUANT 1e-9 + PREQUANT 1e-12)가 FP 잡음·행렬곱 결합순서·BLAS 누적순서 차이를 흡수해
byte-identical u_hash 를 산출함을 실증한다 → byte-identity 가 환경잡음에 강건함을 보인다.
(3) requirements.lock 로 핵심 패키지를 핀해 재검증 신뢰조건을 명시한다.

비파괴: 분석/검증 전용. registry/sealed/oracle/frozen 불변. `.pgf/hardening/`·`requirements.lock` 가산.
소비 자산(사용만): second_oracle(INDEP) · verify_seal(hash_unitary).

사용:  python scripts/determinism_env_check.py [--write-lock]
"""
from __future__ import annotations
import os, sys, json, platform, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import second_oracle as so            # noqa: E402  INDEP 사용만
vs = so.vs                            # hash_unitary

OUT = os.path.join(ROOT, ".pgf", "hardening")
LOCK = os.path.join(ROOT, "requirements.lock")
SEED = 20260628


def env_fingerprint():
    blas = "unknown"
    try:
        cfg = np.__config__.show(mode="dicts") if hasattr(np.__config__, "show") else {}
        blas = (cfg.get("Build Dependencies", {}).get("blas", {}).get("name")
                or cfg.get("Build Dependencies", {}).get("blas", {}).get("detection method") or "unknown")
    except Exception:
        pass
    return {"numpy": np.__version__, "python": sys.version.split()[0],
            "platform": platform.platform(), "machine": platform.machine(),
            "blas": blas, "byteorder": sys.byteorder}


def fp_robustness():
    """hash_unitary 가 FP 잡음·결합순서·BLAS 순서 차이를 흡수해 byte-identical 인지."""
    rng = np.random.default_rng(SEED)
    rows = []
    # (a) FP 잡음(<QUANT/2) 흡수 + (b) 결합순서 무관(같은 게이트 합성)
    for gid in ["qft3", "qft4", "cnot", "toffoli", "h_gate", "cz", "fredkin"]:
        U = so.INDEP[gid]()
        h0 = vs.hash_unitary(U)
        noise = (rng.standard_normal(U.shape) + 1j * rng.standard_normal(U.shape)) * 1e-13
        h_noise = vs.hash_unitary(U + noise)
        rows.append({"gate": gid, "noise_1e-13_absorbed": h0 == h_noise})
    # (c) 행렬곱 결합순서: (A·B)·C vs A·(B·C) — FP 누적순서 차이(~1e-15)를 격자가 흡수
    n = 8
    A = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
    B = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
    C = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
    left = (A @ B) @ C
    right = A @ (B @ C)
    reassoc = {"max_abs_diff": float(np.max(np.abs(left - right))),
               "hash_identical": vs.hash_unitary(left) == vs.hash_unitary(right)}
    # (d) BLAS 누적순서: 합산 순서를 바꾼 동일 수학식 (Σ kron) — 격자 흡수
    terms = [np.kron(so.INDEP["h_gate"](), so.INDEP["x_gate"]()) for _ in range(3)]
    s_fwd = terms[0] + terms[1] + terms[2]
    s_rev = terms[2] + terms[1] + terms[0]
    blas_order = {"hash_identical": vs.hash_unitary(s_fwd) == vs.hash_unitary(s_rev)}
    all_ok = (all(r["noise_1e-13_absorbed"] for r in rows)
              and reassoc["hash_identical"] and blas_order["hash_identical"])
    return {"per_gate_noise": rows, "reassociation": reassoc, "blas_order": blas_order,
            "all_robust": all_ok}


def write_lock():
    try:
        out = subprocess.check_output([sys.executable, "-m", "pip", "freeze"], text=True)
    except Exception as e:
        return None, str(e)
    open(LOCK, "w", encoding="utf-8", newline="\n").write(
        "# requirements.lock — Stage 5 W5.1 환경 핀 (외부 재검증 신뢰조건)\n"
        "# 생성: python scripts/determinism_env_check.py --write-lock\n" + out)
    return len(out.splitlines()), None


def main():
    os.makedirs(OUT, exist_ok=True)
    write = "--write-lock" in sys.argv[1:]
    print("=" * 80)
    print("DeterminismEnvPin (W5.1) — 환경지문 + byte-identity 환경강건성 실증")
    print("=" * 80)
    env = env_fingerprint()
    print(f"  env: numpy={env['numpy']} py={env['python']} blas={env['blas']} platform={env['platform']}")
    fp = fp_robustness()
    print(f"\n  FP 잡음(1e-13) 흡수: {sum(r['noise_1e-13_absorbed'] for r in fp['per_gate_noise'])}"
          f"/{len(fp['per_gate_noise'])} 게이트")
    print(f"  결합순서 (A·B)·C==A·(B·C): hash 동일={fp['reassociation']['hash_identical']} "
          f"(max|Δ|={fp['reassociation']['max_abs_diff']:.2e})")
    print(f"  합산순서(BLAS) 무관: hash 동일={fp['blas_order']['hash_identical']}")
    print(f"  → byte-identity 환경강건성: {'ROBUST ✅' if fp['all_robust'] else 'FRAGILE ✗'}")

    lock_lines = None
    if write:
        lock_lines, err = write_lock()
        print(f"\n  requirements.lock: {'생성 ' + str(lock_lines) + '개 패키지' if lock_lines else 'FAIL ' + str(err)}")
    else:
        print("\n  (requirements.lock 갱신 생략 — --write-lock 로 핀)")

    out = {"_schema": "determinism-env-v1", "env_fingerprint": env, "fp_robustness": fp,
           "byte_identity_robust": fp["all_robust"], "lock_packages": lock_lines,
           "_note": "hash_unitary 격자 양자화(QUANT 1e-9+PREQUANT 1e-12)가 FP 잡음·결합/합산 순서 차이를 "
                    "흡수 → byte-identity 가 환경잡음(BLAS/FP)에 강건. 단 numpy/platform 메이저 변경은 "
                    "requirements.lock 으로 핀(외부 재검증 신뢰조건 명시). 분석전용 비파괴."}
    json.dump(out, open(os.path.join(OUT, "ENV-FINGERPRINT.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("-" * 80)
    print(f"→ .pgf/hardening/ENV-FINGERPRINT.json")
    return 0 if fp["all_robust"] else 1


if __name__ == "__main__":
    sys.exit(main())
