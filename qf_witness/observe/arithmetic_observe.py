#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""arithmetic_observe — HE3 H3.1: 명시적 정수 산술 1급 자산 witness (신규 봉인 0).

봉인된 cuccaro_add2/add3·cmp2_ge·draper_add2 에 대해:
  1. seal 링크: 4 앱 sealed.json + u_hash.
  2. ★전수 정수 대조(two-path): path A=spec golden(순열) vs path B=독립 정수산술 함수 재계산
     (2^6·2^8·2^6·2^4 전 기저 전수) — perm_subspace 정신의 소형 dense 판.
  3. ★교차-family witness: ripple-carry(cuccaro_add2, cin=0 부분공간의 b-레지스터 작용) ==
     Fourier(draper_add2) — 서로 독립 구성(MAJ/UMA vs QFT 위상가산)이 같은 산술로 수렴.
  4. 합성 성질: add2 2회 합성 == b+2a 정수 모델 (봉인 자산 복리 산술).
  5. teeth: 오염 순열(자리올림 1비트 오류 모델)은 정수 모델과 불일치해야.

정직 경계: 봉인=가역 산술 유니터리(exact)뿐. mod 2^n wrap-around 는 사양(오류 아님).
  cmp2_ge 의 전체 유니터리 사양은 z⊕=[a≥b+cin] (cin=strict 선택자). n>3 수직 확장=차기.

사용: python -m qf_witness.observe.arithmetic_observe [--quick]
"""
import os, sys, re, json
import numpy as np

from qf_witness.core.paths import ROOT
OUT = os.path.join(ROOT, ".pgf", "proofs", "ARITHMETIC-OBSERVE.json")


def load_golden(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    ns = {}
    exec(re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1), ns)
    return ns["golden"]


def seal_link(app_id):
    p = os.path.join(ROOT, "registry", "apps", f"{app_id}.sealed.json")
    return os.path.exists(p) and bool(json.load(open(p, encoding="utf-8")).get("u_hash"))


def perm_of(U):
    """유니터리가 0/1 순열행렬인지 확인하고 매핑 반환."""
    dim = U.shape[0]
    m = {}
    for col in range(dim):
        rows = np.nonzero(np.abs(U[:, col]) > 1e-9)[0]
        if len(rows) != 1 or abs(U[rows[0], col] - 1) > 1e-9:
            return None
        m[col] = int(rows[0])
    return m


def bits_of(v, n):
    return [(v >> (n - 1 - q)) & 1 for q in range(n)]


def int_model(app_id, basis, n):
    b = bits_of(basis, n)
    if app_id in ("cuccaro_add2", "cmp2_ge"):
        A, B, CIN, Z = [1, 0], [3, 2], 4, 5
        av = sum(b[A[i]] << i for i in range(2)); bv = sum(b[B[i]] << i for i in range(2))
        out = list(b)
        if app_id == "cuccaro_add2":
            s = av + bv + b[CIN]
            for i in range(2):
                out[B[i]] = (s >> i) & 1
            out[Z] ^= (s >> 2) & 1
        else:
            out[Z] ^= 1 if av >= bv + b[CIN] else 0
    elif app_id == "cuccaro_add3":
        A, B, CIN, Z = [2, 1, 0], [5, 4, 3], 6, 7
        av = sum(b[A[i]] << i for i in range(3)); bv = sum(b[B[i]] << i for i in range(3))
        s = av + bv + b[CIN]
        out = list(b)
        for i in range(3):
            out[B[i]] = (s >> i) & 1
        out[Z] ^= (s >> 3) & 1
    elif app_id == "draper_add2":
        A, B = [1, 0], [3, 2]
        av = sum(b[A[i]] << i for i in range(2)); bv = sum(b[B[i]] << i for i in range(2))
        s = (av + bv) % 4
        out = list(b)
        for i in range(2):
            out[B[i]] = (s >> i) & 1
    return int("".join(map(str, out)), 2)


def observe():
    apps = {"cuccaro_add2": 6, "cuccaro_add3": 8, "cmp2_ge": 6, "draper_add2": 4}
    rows, all_ok = [], True
    perms = {}
    for app_id, n in apps.items():
        U = load_golden(f"{app_id}.app.pg")
        pm = perm_of(U)
        exhaustive = pm is not None and all(pm[c] == int_model(app_id, c, n) for c in range(2 ** n))
        link = seal_link(app_id)
        perms[app_id] = pm
        rows.append({"app": app_id, "n": n, "seal_link": link, "is_permutation": pm is not None,
                     "exhaustive_integer_match": bool(exhaustive), "cases": 2 ** n})
        all_ok = all_ok and link and exhaustive

    # 교차-family: cuccaro(cin=0,z=0 입력, b-레지스터 출력) == draper (a,b 4×4=16 케이스)
    pc, pd = perms["cuccaro_add2"], perms["draper_add2"]
    cross = True
    for a in range(4):
        for b in range(4):
            c_in = (((a >> 1) << 5) | ((a & 1) << 4) | ((b >> 1) << 3) | ((b & 1) << 2))  # w0..w5, cin=z=0
            c_out = pc[c_in]
            cb = bits_of(c_out, 6)
            b_c = (cb[3] | (cb[2] << 1))
            d_in = ((a >> 1) << 3) | ((a & 1) << 2) | ((b >> 1) << 1) | (b & 1)
            db = bits_of(pd[d_in], 4)
            b_d = (db[3] | (db[2] << 1))
            cross = cross and (b_c == b_d == (a + b) % 4)
    # 합성: add2(cin=0) 2회 적용 == b+2a mod4 — cuccaro 는 a·cin 을 복원하므로 s1 에 그대로 재적용 가능
    comp = True
    for a in range(4):
        for b in range(4):
            s1 = pc[((a >> 1) << 5) | ((a & 1) << 4) | ((b >> 1) << 3) | ((b & 1) << 2)]
            s2 = pc[s1]
            b2 = bits_of(s2, 6)
            comp = comp and ((b2[3] | (b2[2] << 1)) == (b + 2 * a) % 4)
    # teeth: 자리올림 오염(합에 +1 오류) 모델은 봉인 순열과 불일치해야
    bad_mismatch = 0
    for c in range(64):
        b = bits_of(c, 6)
        av = (b[1] | (b[0] << 1)); bv = (b[3] | (b[2] << 1))
        s = av + bv + b[4] + 1                      # 오염: +1
        out = list(b)
        out[3], out[2] = s & 1, (s >> 1) & 1
        out[5] ^= (s >> 2) & 1
        if int("".join(map(str, out)), 2) != pc[c]:
            bad_mismatch += 1
    teeth = bad_mismatch > 0
    ok = bool(all_ok and cross and comp and teeth)
    return {"apps": rows, "cross_family_ripple_vs_fourier_16": bool(cross),
            "composition_add_twice_eq_b_plus_2a": bool(comp),
            "teeth_corrupted_carry_detected": bool(teeth),
            "sealed_assets": "cuccaro_add2/add3·cmp2_ge·draper_add2 (Tier-0 exact, 신규 module 0)",
            "honest_boundary": "봉인=가역 산술 유니터리 exact 뿐. mod 2^n wrap=사양. cmp 전체 사양 "
                               "z⊕=[a≥b+cin]. n>3·modular add·곱셈기 조립=차기.",
            "ok": ok}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"_schema": "arithmetic-observe-v1",
                       "_note": "산술 1급 자산 witness: 전수 정수 two-path + ripple vs Fourier 교차 + teeth.",
                       "observation": res}, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("정수 산술 1급 자산 witness 관측:", flush=True)
        for r in res["apps"]:
            print(f"  {r['app']:13}: seal {r['seal_link']} · 순열 {r['is_permutation']} · "
                  f"전수 {r['cases']} 정수일치 {r['exhaustive_integer_match']}", flush=True)
        print(f"  ripple==Fourier(16) {res['cross_family_ripple_vs_fourier_16']} · "
              f"합성 b+2a {res['composition_add_twice_eq_b_plus_2a']} · teeth {res['teeth_corrupted_carry_detected']}",
              flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"arithmetic_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
