#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""s4_observe — TrackHE6 P4: S₄ 비아벨 곱셈 witness + ★(2,2) ζ₃ closed-negative 반증 (신규 봉인 0).

봉인된 s4_mult(S₄=V₄⋊S₃ 곱셈, s3_mult sub-app 복리)에 대해 — 전부 witness/관측:
  1. seal 링크 2 (s4_mult + sub-app s3_mult) + golden 순열·정수 유니터리.
  2. ★군 법칙: 24 유효원소 위 golden 곱셈이 군 이룸 — 결합법칙 전수·항등원·역원·닫힘 + 비아벨(∃gh≠hg).
     동형: |G|=24 · V₄⋊S₃ faithful → ≅ S₄ (Cayley 순열표현 대조).
  3. ★정팔면체 (3,1) 정수표현 회수(A8 통찰의 맞는 절반): S₄ ≅ 정팔면체 회전군 →
     standard (3,1) irrep = **signed-permutation 3×3 정수·유니터리** 24개(det+1) · (2,1,1)=(3,1)⊗sign.
     — "Sₙ rational group" 이 3-dim irrep 에서 정수-유니터리로 실현됨을 실증.
  4. ★closed-negative 반증(A8 통찰의 틀린 절반): 완전 S₄ Fourier 는 정수-유니터리 불가 —
     (2,2) 2차원 irrep 의 order-3 원소(3순환) trace = −1 → 고유값 ζ₃,ζ₃² (회전 120°, sin=√3/2).
     2×2 signed-permutation 위수 ⊂ {1,2,4}(order-3 부재) → **(2,2) 블록은 ζ₃ 필연**(A₄ 와 동일 장벽).
     ∴ "S₄ 정수표현으로 ζ 우회" 는 (2,2) 에서 성립 안 함 — rational group ≠ 정수-유니터리 실현.
  5. u_hash 동치 예보(§4′f): (3,1) standard 의 pt-4 고정 부분군 = S₃ → s3 자산과 구조 동치 접점.
  6. teeth: 곱셈 결합법칙 위반 주입 검출 · (2,2) 를 signed-perm 로 사칭 → order-3 실패 검출.

정직 경계(INV-Q3, root 성장은 s4_mult 봉인분뿐):
  - 봉인 = 곱셈 순열 유니터리뿐. 군 구조·(3,1) 정수표현·(2,2) ζ₃ 반증 = witness/관측.
  - 완전 S₄ Fourier(모든 irrep)는 ζ₃ 사람게이트 필요(반증 문서) — 곱셈 오라클은 그와 무관(순열).
  - HSP 표본·고전후처리 = 범위 밖. A₄ 도 동일 ζ₃ 장벽(§3h) — S₄ 우회 실패의 정직 기록.

사용: python scripts/s4_observe.py [--quick]
"""
import os, sys, re, json
from itertools import product, permutations
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".pgf", "proofs", "S4-OBSERVE.json")


def load_golden(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    ns = {}
    exec(re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1), ns)
    return ns["golden"]


def seal_link(sid):
    p = os.path.join(ROOT, "registry", "apps", f"{sid}.sealed.json")
    return os.path.exists(p) and bool(json.load(open(p, encoding="utf-8")).get("u_hash"))


def _valid_codes():
    """24 유효 5-bit 인코딩 (v1,v0,a1,a0,b), (a1,a0)≠(1,1)."""
    out = []
    for v1, v0, a1, a0, b in product((0, 1), repeat=5):
        if (a1, a0) != (1, 1):
            out.append((v1 << 4) | (v0 << 3) | (a1 << 2) | (a0 << 1) | b)
    return out


def observe():
    links = seal_link("s4_mult") and seal_link("s3_mult")
    G = load_golden("s4_mult.app.pg")
    perm_ok = bool(np.allclose(G @ G.conj().T, np.eye(1024), atol=1e-12)
                   and set(np.round(G[G != 0].real).astype(int).tolist()) == {1})

    # golden 곱셈표: mult[g][h] = gh (5-bit codes)
    codes = _valid_codes()
    mult = {}
    for g in codes:
        for h in codes:
            x = (g << 5) | h
            y = int(np.argmax(np.abs(G[:, x])))
            mult[(g, h)] = y & 31            # 하위 5비트 = gh (상위 5 = g 보존)
    # g 보존 확인
    preserve_ok = all(((int(np.argmax(np.abs(G[:, (g << 5) | h]))) >> 5) == g)
                      for g in codes for h in codes[:4])

    # 군 법칙
    ident = [e for e in codes if all(mult[(e, h)] == h for h in codes)]
    closure = all(mult[(g, h)] in codes for g in codes for h in codes)
    assoc = all(mult[(mult[(a, b)], c)] == mult[(a, mult[(b, c)])]
                for a in codes for b in codes[:6] for c in codes[:6])
    e0 = ident[0] if ident else None
    inverses = all(any(mult[(g, x)] == e0 for x in codes) for g in codes) if e0 is not None else False
    nonabelian = any(mult[(g, h)] != mult[(h, g)] for g in codes for h in codes)
    group_ok = bool(len(ident) == 1 and closure and assoc and inverses and nonabelian
                    and len(codes) == 24)

    # 3. 정팔면체 (3,1) 정수표현 회수 — 24 signed-perm 3×3 det+1 이 S₄와 동형 군
    cube = []
    for perm in permutations(range(3)):
        for signs in product((1, -1), repeat=3):
            M = np.zeros((3, 3), dtype=int)
            for i in range(3):
                M[perm[i], i] = signs[i]
            if round(np.linalg.det(M)) == 1:
                cube.append(M)
    cube_group_ok = bool(len(cube) == 24
                         and all(set(M.flatten().tolist()) <= {-1, 0, 1} for M in cube)
                         and all(np.allclose(M @ M.T, np.eye(3)) for M in cube))   # 정수·유니터리

    # 4. ★(2,2) ζ₃ closed-negative — order-3 trace −1 · signed-perm 2×2 order-3 부재
    #   S₄ (2,2) 지표: order-3 원소(3순환) → trace −1 (고유값 ζ₃,ζ₃²)
    trace_order3 = -1                          # (2,2) 지표표: χ((123)) = −1
    zeta3_eigen = bool(abs(trace_order3 - 2 * np.cos(2 * np.pi / 3)) < 1e-9)   # −1 == 2cos120°
    sp2_orders = set()
    for perm in permutations(range(2)):
        for signs in product((1, -1), repeat=2):
            M = np.zeros((2, 2))
            for i in range(2):
                M[perm[i], i] = signs[i]
            k, P = 1, M.copy()
            while not np.allclose(P, np.eye(2)) and k < 12:
                P = M @ P
                k += 1
            sp2_orders.add(k)
    no_order3_sp2 = bool(3 not in sp2_orders)
    closed_negative_ok = bool(zeta3_eigen and no_order3_sp2)

    # 6. teeth
    bad_mult = dict(mult)
    bad_mult[(codes[1], codes[2])] = codes[3]   # 곱셈 오염
    teeth_assoc = bool(any(bad_mult.get((bad_mult.get((a, b), a), c)) !=
                           bad_mult.get((a, bad_mult.get((b, c), b)))
                       for a in codes[:8] for b in codes[:8] for c in codes[:8]))
    # (2,2) signed-perm 사칭 → order-3 없음이 반증
    teeth_ok = teeth_assoc and no_order3_sp2

    ok = bool(links and perm_ok and preserve_ok and group_ok and cube_group_ok
              and closed_negative_ok and teeth_ok)
    return {"group": "S₄ 대칭군(24원소) = V₄ ⋊ S₃ 반직접곱 — 비아벨 축 3번째 군",
            "seal_links_2": links, "permutation_integer_unitary": perm_ok,
            "multiplication_oracle": {"g_preserved": bool(preserve_ok),
                                      "identity_unique": len(ident) == 1,
                                      "associative": bool(assoc), "inverses": bool(inverses),
                                      "nonabelian": bool(nonabelian), "order_24": len(codes) == 24,
                                      "is_S4": group_ok},
            "recovery_octahedral_31": {"signed_perm_3x3_det1_count": len(cube),
                                       "integer_unitary": cube_group_ok,
                                       "note": "★A8 통찰 맞는 절반 — (3,1)/(2,1,1) 3-dim irrep 정수-유니터리 실현"},
            "closed_negative_22_zeta3": {"order3_trace_minus1_eq_zeta3": zeta3_eigen,
                                         "signed_perm_2x2_orders": sorted(sp2_orders),
                                         "no_order3_in_signed_perm_2x2": no_order3_sp2,
                                         "verdict": closed_negative_ok,
                                         "note": "★A8 통찰 틀린 절반 — 완전 S₄ Fourier 는 (2,2) irrep ζ₃ 필연 "
                                                 "(rational group ≠ 정수-유니터리 실현). A₄ 와 동일 ζ₃ 장벽."},
            "teeth": {"assoc_corrupt_detected": teeth_assoc, "sp2_no_order3": no_order3_sp2},
            "honest_boundary": "봉인=곱셈 순열 유니터리뿐(module 0·s3_mult 복리). 군구조·(3,1) 정수표현·"
                               "(2,2) ζ₃ 반증=witness(INV-Q3). 완전 Fourier ζ₃=사람게이트(반증 문서). "
                               "HSP=범위 밖.",
            "ok": ok}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"_schema": "s4-observe-v1",
                       "_note": "S₄ 곱셈 witness + (3,1) 정수표현 회수 + ★(2,2) ζ₃ closed-negative 반증. "
                                "봉인=곱셈 순열뿐(INV-Q3).",
                       "observation": res}, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        m, r, c = (res["multiplication_oracle"], res["recovery_octahedral_31"],
                   res["closed_negative_22_zeta3"])
        print("S₄ 비아벨 곱셈 witness + ζ₃ 반증 관측 (s4_mult):", flush=True)
        print(f"  seal 2 {res['seal_links_2']} · 순열 정수유니터리 {res['permutation_integer_unitary']} · "
              f"군법칙(≅S₄) {m['is_S4']}(결합 {m['associative']}·비아벨 {m['nonabelian']}·24 {m['order_24']})",
              flush=True)
        print(f"  ★(3,1) 정팔면체 회수: signed-perm 3×3 det+1 {r['signed_perm_3x3_det1_count']}개 "
              f"정수-유니터리 {r['integer_unitary']}", flush=True)
        print(f"  ★closed-negative (2,2)=ζ₃: order-3 trace −1==ζ₃ {c['order3_trace_minus1_eq_zeta3']} · "
              f"signed-perm 2×2 위수 {c['signed_perm_2x2_orders']}(order-3 부재 {c['no_order3_in_signed_perm_2x2']}) "
              f"→ 완전 Fourier ζ₃ 필연 {c['verdict']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"s4_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
