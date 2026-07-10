#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pathsum_verify — HE3 H3.4: 4번째 독립 검증경로 — sum-over-paths 정수환 exact (봉인 0·root 불변).

기존 3경로(dense 수치 오라클 · stabilizer tableau · ZX rewrite) 와 수학 기반이 다른 4번째 대조:
Clifford+T 회로의 진폭을 **ℤ[ω₈] 정수환**(ω=e^{iπ/4}, 원소=a+bω+cω²+dω³, a..d∈ℤ) × (1/√2)^k 로
**부동소수 없는 exact 정수 연산**으로 축차 경로합(H 분기=경로 변수, 축차 수축) 계산 → 봉인 앱의
dense golden 과 대조. 검증 대상: plan 이 {h,s,sdg,t,x,z,cnot,cz,cs,ct,swap2,toffoli,fredkin} 로
닫힌 봉인 앱(bell·ghz3·magic_a·reflect00·cliff1_hsh·cuccaro_add2·cmp2_ge·szegedy_2state_p12).

정직 경계:
  - 이 경로는 **봉인 판정에 불참**(sidecar witness). oracle 2파일(verify_seal/contracts) 무수정 —
    사용도 안 함(재구현 아님: 진폭 계산 방법 자체가 다름. zx_verify 3번째 경로와 같은 위상).
  - 경로합 측=exact 정수 연산. dense golden 과의 최종 대조는 float 표현 한계(1e-12)로 수행.
  - 전역위상: C-app 은 전역위상 흡수 규약 → 첫 비영 성분으로 정규화 후 대조.
  - T-count/큐빗수 큰 회로는 항 수 증가 → 소형 봉인분 한정(범위 명시). 비지원 게이트 앱=정직 스킵.

사용: python -m qf_witness.verify.pathsum_verify [--quick]
"""
import os, sys, re, json
import numpy as np

from qf_witness.core.paths import ROOT
OUT = os.path.join(ROOT, ".pgf", "proofs", "PATHSUM-VERIFY.json")

TARGET_APPS = ["bell", "ghz3", "magic_a", "reflect00", "cliff1_hsh",
               "cuccaro_add2", "cmp2_ge", "szegedy_2state_p12"]

ARITY = {"h_gate": 1, "s_gate": 1, "sdg_gate": 1, "t_gate": 1, "x_gate": 1, "z_gate": 1,
         "cnot": 2, "cz": 2, "cs_gate": 2, "ct_gate": 2, "swap2": 2,
         "toffoli": 3, "fredkin": 3}
OMEGA_POW = {"z_gate": 4, "s_gate": 2, "sdg_gate": 6, "t_gate": 1}
CTRL_OMEGA = {"cz": 4, "cs_gate": 2, "ct_gate": 1}


# ---- ℤ[ω₈] 정수환: (a,b,c,d) = a+bω+cω²+dω³, ω⁴=-1. 순수 정수 연산(부동소수 0) ----
def w_mul_pow(t, m):
    a, b, c, d = t
    for _ in range(m % 8):
        a, b, c, d = -d, a, b, c
    return (a, b, c, d)


def w_add(t1, t2):
    return tuple(x + y for x, y in zip(t1, t2))


def to_complex(t, k):
    a, b, c, d = t
    r2 = np.sqrt(2.0)
    return complex(a + (b - d) / r2, c + (b + d) / r2) / (r2 ** k)


def load_plan_and_golden(app):
    src = open(os.path.join(ROOT, "specs", "apps", f"{app}.app.pg"), encoding="utf-8").read()
    meta = json.loads(re.search(r"```json id=app_meta\n(.*?)```", src, re.S).group(1))
    plan = json.loads(re.search(r"```json id=plan\n(.*?)```", src, re.S).group(1))
    ns = {}
    exec(re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1), ns)
    return meta, plan["steps"], ns["golden"]


def pathsum_column(steps, n, basis_in):
    """입력 계산기저 → 축차 경로합. state: {basis:(a,b,c,d)}, k=√2 지수(전역)."""
    state = {basis_in: (1, 0, 0, 0)}
    k = 0
    for name, tg in steps:
        new = {}
        if name == "h_gate":
            q = tg[0]
            k += 1
            for x, amp in state.items():
                bit = (x >> (n - 1 - q)) & 1
                x0 = x & ~(1 << (n - 1 - q))
                x1 = x | (1 << (n - 1 - q))
                for xo, sgn in ((x0, 1), (x1, -1 if bit else 1)):
                    t = tuple(sgn * v for v in amp)
                    new[xo] = w_add(new.get(xo, (0, 0, 0, 0)), t)
            state = {x: t for x, t in new.items() if any(t)}
            continue
        for x, amp in state.items():
            bits = [(x >> (n - 1 - q)) & 1 for q in range(n)]
            if name == "x_gate":
                bits[tg[0]] ^= 1
            elif name in OMEGA_POW:
                if bits[tg[0]]:
                    amp = w_mul_pow(amp, OMEGA_POW[name])
            elif name == "cnot":
                bits[tg[1]] ^= bits[tg[0]]
            elif name in CTRL_OMEGA:
                if bits[tg[0]] and bits[tg[1]]:
                    amp = w_mul_pow(amp, CTRL_OMEGA[name])
            elif name == "swap2":
                bits[tg[0]], bits[tg[1]] = bits[tg[1]], bits[tg[0]]
            elif name == "toffoli":
                if bits[tg[0]] and bits[tg[1]]:
                    bits[tg[2]] ^= 1
            elif name == "fredkin":
                if bits[tg[0]]:
                    bits[tg[1]], bits[tg[2]] = bits[tg[2]], bits[tg[1]]
            else:
                raise ValueError(name)
            y = 0
            for b in bits:
                y = (y << 1) | b
            new[y] = w_add(new.get(y, (0, 0, 0, 0)), amp)
        state = {x: t for x, t in new.items() if any(t)}
    return state, k


def normalize_steps(steps):
    """plan step → (module_name, targets). 비지원/서브앱은 None(스킵 신호)."""
    out = []
    for s in steps:
        if "app" in s:
            return None
        name = os.path.basename(s["spec"]).replace(".pg", "")
        if name not in ARITY:
            return None
        tg = s.get("targets", list(range(ARITY[name])))
        out.append((name, tg))
    return out


def verify_app(app):
    meta, raw, golden = load_plan_and_golden(app)
    n = meta["n_sys"] + meta.get("n_anc", 0)
    steps = normalize_steps(raw)
    if steps is None:
        return {"app": app, "skipped": "unsupported gate/sub-app"}
    dim = 2 ** n
    U = np.zeros((dim, dim), dtype=complex)
    terms = 0
    for col in range(dim):
        st, k = pathsum_column(steps, n, col)
        terms = max(terms, len(st))
        for x, t in st.items():
            U[x, col] = to_complex(t, k)
    # 전역위상 정규화 후 대조 (C-app 위상흡수 규약)
    idx = np.argmax(np.abs(golden) > 1e-9)
    r, c = divmod(int(idx), dim)
    ph = golden[r, c] / U[r, c] if abs(U[r, c]) > 1e-12 else 1.0
    dev = float(np.abs(U * ph - golden).max())
    return {"app": app, "n": n, "steps": len(steps), "max_terms": terms,
            "phase_factor_abs1": bool(abs(abs(ph) - 1) < 1e-9), "max_dev": dev,
            "ok": bool(dev < 1e-9 and abs(abs(ph) - 1) < 1e-9)}


def observe():
    rows = [verify_app(a) for a in TARGET_APPS]
    checked = [r for r in rows if "ok" in r]
    all_ok = all(r["ok"] for r in checked) and len(checked) == len(TARGET_APPS)
    # teeth: bell 에 t 게이트 오염 주입 → 불일치 검출
    meta, raw, golden = load_plan_and_golden("bell")
    steps = normalize_steps(raw) + [("t_gate", [0])]
    dim = 4
    U = np.zeros((dim, dim), dtype=complex)
    for col in range(dim):
        st, k = pathsum_column(steps, 2, col)
        for x, t in st.items():
            U[x, col] = to_complex(t, k)
    idx = np.argmax(np.abs(golden) > 1e-9)
    r, c = divmod(int(idx), dim)
    ph = golden[r, c] / U[r, c] if abs(U[r, c]) > 1e-12 else 1.0
    teeth = bool(np.abs(U * ph - golden).max() > 1e-3)
    ok = bool(all_ok and teeth)
    return {"apps": rows, "teeth_injected_t_detected": teeth,
            "path": "4번째 독립경로: ℤ[ω₈] 정수환 축차 경로합(부동소수 0) vs dense golden",
            "honest_boundary": "봉인 판정 불참(sidecar witness)·oracle 무수정. 경로합=exact 정수, "
                               "최종 대조=float 1e-12 한계. 소형 Clifford+T 봉인분 한정, 비지원 게이트=스킵.",
            "ok": ok}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"_schema": "pathsum-verify-v1",
                       "_note": "sum-over-paths 정수환 exact 4차 검증경로. 봉인 0·root 불변·oracle 무수정.",
                       "observation": res}, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("path-sum(ℤ[ω₈]) 4차 검증경로:", flush=True)
        for r in res["apps"]:
            if "skipped" in r:
                print(f"  {r['app']:18}: SKIP({r['skipped']})", flush=True)
            else:
                print(f"  {r['app']:18}: {r['steps']}스텝 · 최대항 {r['max_terms']} · dev {r['max_dev']:.1e} · ok {r['ok']}",
                      flush=True)
        print(f"  teeth(T 오염) 검출 {res['teeth_injected_t_detected']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"pathsum_verify: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
