#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gf8_observe — TrackR3Residue C6: GF(8) 체 연산(역원·Frobenius) witness (신규 봉인 0).

봉인된 gf8_inv(a↦a⁻¹, 첫 비선형 체 연산)·gf8_frob(a↦a², 자기동형)·기봉인 gf8_mulx 에 대해:
  1. seal 링크 3 + golden 순열성(permutation matrix).
  2. ★독립 산술 대조: 회로 순열 == GF(2)[x]/(x³+x+1) 직접 산술 — inv: a·a⁻¹=1 **전수 7/7**(0↦0 규약)
     + 대합(inv²=id) · frob: a² 전수 + GF(2)-선형성.
  3. ★체 구조 witness: Galois 군 frob³=id(Z₃) · 자기동형 frob(ab)=frob(a)·frob(b)(64 전수) ·
     고정체 Fix(frob)={0,1}=GF(2) · frob∘inv==inv∘frob(가환).
  4. ★복리(gf8_mulx 궤도): inv(xᵏ)=x^(7−k) — 역원이 primitive 궤도를 반전(mulx 봉인 순열로 확인).
  5. teeth: 틀린 기약다항식(x³+x²+1) 역원표 ≠ 봉인 순열 · frob 순서 교란(cnot 역순) ≠ a².

정직 경계(INV-Q3, seal 아님, root 성장은 앱 2 봉인분뿐):
  - 봉인 = 계산기저 순열 유니터리 2개뿐. 체 구조(Galois·자기동형·궤도) = 독립 산술 대조 관측.
  - GF(2ᵏ) 일반 k·다항식 인수분해·Reed-Solomon 부호 산술 = 차기. 신규 module 0(MMD 6게이트+CNOT 2).

사용: python scripts/gf8_observe.py [--quick]
"""
import os, sys, re, json
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".pgf", "proofs", "GF8-OBSERVE.json")


def gf_mul(a, b, poly=0b1011):
    r = 0
    for i in range(3):
        if (b >> i) & 1:
            r ^= a << i
    for d in (5, 4, 3):
        if (r >> d) & 1:
            r ^= poly << (d - 3)
    return r & 7


def load_golden(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    ns = {}
    exec(re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1), ns)
    return ns["golden"]


def seal_link(sid):
    p = os.path.join(ROOT, "registry", "apps", f"{sid}.sealed.json")
    return os.path.exists(p) and bool(json.load(open(p, encoding="utf-8")).get("u_hash"))


def perm_of(U):
    """permutation matrix → 매핑 리스트 (아니면 None)."""
    out = []
    for c in range(U.shape[1]):
        col = U[:, c]
        j = int(np.argmax(np.abs(col)))
        if abs(col[j] - 1) > 1e-12 or abs(np.abs(col).sum() - 1) > 1e-12:
            return None
        out.append(j)
    return out


def observe():
    links = all(seal_link(s) for s in ("gf8_inv", "gf8_frob", "gf8_mulx"))
    inv_p = perm_of(load_golden("gf8_inv.app.pg"))
    frob_p = perm_of(load_golden("gf8_frob.app.pg"))
    mulx_p = perm_of(load_golden("gf8_mulx.app.pg"))
    perm_ok = all(p is not None for p in (inv_p, frob_p, mulx_p))

    # 2. 독립 산술 대조
    inv_ref = [0] + [next(b for b in range(1, 8) if gf_mul(a, b) == 1) for a in range(1, 8)]
    inv_ok = bool(inv_p == inv_ref and all(gf_mul(a, inv_p[a]) == 1 for a in range(1, 8))
                  and all(inv_p[inv_p[a]] == a for a in range(8)))
    frob_ref = [gf_mul(a, a) for a in range(8)]
    lin_ok = all(frob_ref[a ^ b] == (frob_ref[a] ^ frob_ref[b]) for a in range(8) for b in range(8))
    frob_ok = bool(frob_p == frob_ref and lin_ok)

    # 3. 체 구조
    frob3 = [frob_p[frob_p[frob_p[a]]] for a in range(8)]
    galois_ok = bool(frob3 == list(range(8)))
    homo_ok = bool(all(frob_p[gf_mul(a, b)] == gf_mul(frob_p[a], frob_p[b])
                       for a in range(8) for b in range(8)))
    fixed_ok = bool([a for a in range(8) if frob_p[a] == a] == [0, 1])
    comm_ok = bool(all(frob_p[inv_p[a]] == inv_p[frob_p[a]] for a in range(8)))

    # 4. mulx 궤도 반전: x^k = mulx^k(1) → inv(x^k) == x^((7-k) mod 7)
    orbit = [1]
    for _ in range(6):
        orbit.append(mulx_p[orbit[-1]])
    orbit_ok = bool(len(set(orbit)) == 7
                    and all(inv_p[orbit[k]] == orbit[(7 - k) % 7] for k in range(7)))

    # 5. teeth
    bad_inv = [0] + [next(b for b in range(1, 8) if gf_mul(a, b, poly=0b1101) == 1)
                     for a in range(1, 8)]                     # x³+x²+1
    teeth_poly = bool(bad_inv != inv_p)
    bad_frob = list(range(8))
    for c, t in [(0, 1), (1, 0)]:                              # cnot 역순 교란
        cm, tm = 1 << (2 - c), 1 << (2 - t)
        bad_frob = [x ^ tm if (x & cm) == cm else x for x in bad_frob]
    teeth_frob = bool(bad_frob != frob_p)
    teeth_ok = teeth_poly and teeth_frob

    ok = bool(links and perm_ok and inv_ok and frob_ok and galois_ok and homo_ok
              and fixed_ok and comm_ok and orbit_ok and teeth_ok)
    return {"field": "GF(8) = GF(2)[x]/(x³+x+1) · 레이아웃 q0=a₂·q1=a₁·q2=a₀",
            "seal_links_3": links, "permutations": perm_ok,
            "inversion": {"matches_arithmetic_7of7": inv_ok, "involution": True,
                          "note": "첫 비선형 체 연산 (0↦0 규약, MMD 6게이트)"},
            "frobenius": {"matches_a_squared": frob_ok, "gf2_linear": bool(lin_ok)},
            "field_structure": {"galois_frob_cubed_id_Z3": galois_ok,
                                "automorphism_64_products": homo_ok,
                                "fixed_field_GF2": fixed_ok,
                                "frob_inv_commute": comm_ok},
            "mulx_orbit_reversal": {"inv_xk_eq_x_7mk": orbit_ok,
                                    "note": "역원이 primitive 궤도 반전 — gf8_mulx 복리"},
            "teeth": {"wrong_poly_x3x2_1_detected": teeth_poly,
                      "frob_gate_order_detected": teeth_frob},
            "honest_boundary": "봉인=계산기저 순열 2개뿐. 체 구조=독립 산술 대조 관측(INV-Q3). "
                               "일반 GF(2ᵏ)·다항식 인수분해·Reed-Solomon=차기. 신규 module 0.",
            "ok": ok}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"_schema": "gf8-observe-v1",
                       "_note": "GF(8) 역원·Frobenius witness: 독립 산술+Galois 구조+궤도 복리+teeth. "
                                "봉인=순열뿐(INV-Q3).",
                       "observation": res}, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        fs = res["field_structure"]
        print("GF(8) 체 연산 witness 관측 (gf8_inv·gf8_frob):", flush=True)
        print(f"  seal 3 {res['seal_links_3']} · 역원==산술 7/7 {res['inversion']['matches_arithmetic_7of7']} "
              f"· frob==a² {res['frobenius']['matches_a_squared']}", flush=True)
        print(f"  체 구조: Gal(Z₃) {fs['galois_frob_cubed_id_Z3']} · 자기동형(64곱) "
              f"{fs['automorphism_64_products']} · 고정체 GF(2) {fs['fixed_field_GF2']} · "
              f"inv 가환 {fs['frob_inv_commute']}", flush=True)
        print(f"  mulx 궤도 반전 {res['mulx_orbit_reversal']['inv_xk_eq_x_7mk']} · teeth(틀린 poly·게이트 순서) "
              f"{res['teeth']['wrong_poly_x3x2_1_detected']}/{res['teeth']['frob_gate_order_detected']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"gf8_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
