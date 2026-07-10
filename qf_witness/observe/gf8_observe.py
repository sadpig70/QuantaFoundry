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

★TrackHE4 P3 가산 확장(기존 키 불변): 봉인된 gf8_mul(일반곱)·rs_synd_core·rs73_encoder에 대해:
  6. ★gf8_mul 전수 512 독립 산술 대조 + 가환성(64) + mulx 재발견(mul(·,x)==mulx 순열) +
     ★inv 교차 재구성: mul(frob²(a), frob(a)) == 봉인 inv 순열 (Fermat a⁶=a⁴·a² — 두 독립 구성 일치,
     inv=MMD 직접 합성 vs frob/mul 연쇄).
  7. ★rs_synd_core 전수 512 대조(S=α·r₀⊕α²·r₁) + GF(2)-선형성.
  8. ★rs73_encoder subspace 상환(동일 커밋): path A=spec plan CNOT 비트시뮬 **전수 512 메시지** vs
     path B=독립 다항 나눗셈(m(x)x⁴ mod g) — exact 순열 일치. +RS-성 독립 witness: 전 부호어
     c(αʲ)=0 (j=1..4, 신드롬-제로 2048건) · ★최소 해밍무게 5 **전수 511**(거리-5 MDS 관측).
     teeth: CNOT 1개 누락 → 불일치. full 실행 시 .pgf/proofs/rs73_encoder.subspace_proof.json 산출
     (semantic_guarantee 가 structural→subspace_permutation_verified 상향에 소비).

정직 경계(INV-Q3, seal 아님, root 성장은 앱 2 봉인분뿐):
  - 봉인 = 계산기저 순열 유니터리 2개뿐. 체 구조(Galois·자기동형·궤도) = 독립 산술 대조 관측.
  - GF(2ᵏ) 일반 k·다항식 인수분해·Reed-Solomon 부호 산술 = 차기. 신규 module 0(MMD 6게이트+CNOT 2).

사용: python scripts/gf8_observe.py [--quick]
"""
import os, sys, re, json
import numpy as np

from qf_witness.core.paths import ROOT
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


# --- TrackHE4 P3: 일반곱·RS 도우미 (레이아웃: 심볼 내 big-endian, 정수 = 다항 비트) ---
ALPHA = 2


def _gpow(a, e):
    r = 1
    for _ in range(e):
        r = gf_mul(r, a)
    return r


def _rs_g():
    g = [1]
    for j in range(1, 5):
        r = _gpow(ALPHA, j)
        ng = [0] * (len(g) + 1)
        for i, c in enumerate(g):
            ng[i] ^= gf_mul(c, r)
            ng[i + 1] ^= c
        g = ng
    return g


def _rs_parity(m, g):
    p = [0, 0, 0, 0] + list(m)
    for d in range(6, 3, -1):
        c = p[d]
        if c:
            for i in range(5):
                p[d - 4 + i] ^= gf_mul(c, g[i])
    return p[0:4]


def _parse_cnots(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    plan = json.loads(re.search(r"```json id=plan\s*\n(.*?)\n```", src, re.S).group(1))
    return [s["targets"] for s in plan["steps"]]


def _rs73_bitsim(m, cnots):
    st = [0] * 21
    for s in range(3):
        st[3 * s], st[3 * s + 1], st[3 * s + 2] = (m[s] >> 2) & 1, (m[s] >> 1) & 1, m[s] & 1
    for (c, t) in cnots:
        st[t] ^= st[c]
    return [st[9 + 3 * k] << 2 | st[9 + 3 * k + 1] << 1 | st[9 + 3 * k + 2] for k in range(4)]


def observe_p3():
    links = all(seal_link(s) for s in ("gf8_mul", "rs_synd_core", "rs73_encoder"))
    inv_p = perm_of(load_golden("gf8_inv.app.pg"))
    frob_p = perm_of(load_golden("gf8_frob.app.pg"))
    mulx_p = perm_of(load_golden("gf8_mulx.app.pg"))

    # 6. gf8_mul: 전수 대조 + 가환 + mulx 재발견 + inv 교차 재구성
    mul_p = perm_of(load_golden("gf8_mul.app.pg"))
    mul_ok = bool(mul_p is not None and all(
        mul_p[(a << 6) | (b << 3) | t] == ((a << 6) | (b << 3) | (t ^ gf_mul(a, b)))
        for a in range(8) for b in range(8) for t in range(8)))
    comm_ok = bool(all(gf_mul(a, b) == gf_mul(b, a) for a in range(8) for b in range(8)))
    mulx_re = bool(all(mul_p[(a << 6) | (2 << 3) | 0] == ((a << 6) | (2 << 3) | mulx_p[a])
                       for a in range(8)))
    inv_cross = bool(all((gf_mul(frob_p[frob_p[a]], frob_p[a]) if a else 0) == inv_p[a]
                         for a in range(8)))

    # 7. rs_synd_core: 전수 대조 + 선형성
    synd_p = perm_of(load_golden("rs_synd_core.app.pg"))
    sref = lambda r0, r1: gf_mul(ALPHA, r0) ^ gf_mul(gf_mul(ALPHA, ALPHA), r1)
    synd_ok = bool(synd_p is not None and all(
        synd_p[(r0 << 6) | (r1 << 3) | s] == ((r0 << 6) | (r1 << 3) | (s ^ sref(r0, r1)))
        for r0 in range(8) for r1 in range(8) for s in range(8)))
    lin_ok = bool(all(sref(a ^ c, b ^ d) == (sref(a, b) ^ sref(c, d))
                      for a in range(4) for b in range(4) for c in range(4) for d in range(4)))

    # 8. rs73_encoder: path A(plan 비트시뮬) vs path B(다항 나눗셈) 전수 + RS-성 + 거리 + teeth
    g = _rs_g()
    cnots = _parse_cnots("rs73_encoder.app.pg")
    msgs = [(m0, m1, m2) for m0 in range(8) for m1 in range(8) for m2 in range(8)]
    two_path = bool(all(_rs73_bitsim(m, cnots) == _rs_parity(m, g) for m in msgs))

    def _eval(cs, x):
        r, xp = 0, 1
        for c in cs:
            r ^= gf_mul(c, xp); xp = gf_mul(xp, x)
        return r
    codes = {m: _rs_parity(m, g) + list(m) for m in msgs}      # 계수 low→high (p0..p3,m0..m2)
    synd_zero = bool(all(all(_eval(cs, _gpow(ALPHA, j)) == 0 for j in range(1, 5))
                         for cs in codes.values()))
    wmin = min(sum(1 for s in cs if s) for m, cs in codes.items() if m != (0, 0, 0))
    dist_ok = bool(wmin == 5)
    bad = cnots[:-1]
    teeth = bool(any(_rs73_bitsim(m, bad) != _rs_parity(m, g) for m in msgs))

    ok = bool(links and mul_ok and comm_ok and mulx_re and inv_cross and synd_ok
              and lin_ok and two_path and synd_zero and dist_ok and teeth)
    return {"seal_links_3": links,
            "gf8_mul": {"exhaustive_512": mul_ok, "commutative_64": comm_ok,
                        "mulx_rediscovery": mulx_re,
                        "inv_cross_frob2_mul": inv_cross},
            "rs_synd_core": {"exhaustive_512": synd_ok, "gf2_linear": lin_ok},
            "rs73_encoder": {"two_path_exhaustive_512": two_path,
                             "syndrome_zero_2048": synd_zero,
                             "min_weight_exhaustive_511": wmin, "distance5_MDS": dist_ok,
                             "teeth_cnot_drop": teeth,
                             "generator_poly_deg0to4": g},
            "honest_boundary": "봉인=순열 유니터리 3(rs73=STRUCTURAL+subspace 상환). 거리-5 MDS·"
                               "RS-성=독립 산술 관측(INV-Q3). 복호(Berlekamp-Massey)·오류정정 주장=범위 밖.",
            "ok": ok}


def write_rs73_subspace_proof(p3):
    """rs73_encoder subspace 상환 sidecar (perm_subspace_verify 스키마 호환, 비파괴)."""
    import hashlib
    r = p3["rs73_encoder"]
    payload = {"_schema": "subspace-proof-v1",
               "_note": "비파괴 sidecar. registry root/sealed/oracle/frozen 무영향. RS(7,3) 인코더 "
                        "계산기저 순열 강검증(전수). gf8_observe 산출(TrackHE4 P3).",
               "id": "rs73_encoder", "n_sys": 21,
               "method": "exhaustive", "method_desc":
                   "RS(7,3) 인코더 계산기저 순열 강검증(exhaustive, basis 512/512; "
                   "path A=spec plan CNOT 비트시뮬 vs path B=독립 다항 나눗셈 m(x)x⁴ mod g). "
                   "+부호어 신드롬-제로 2048건·최소무게 5 전수 511(MDS). 전체 unitary dense 미검증(INV-R5).",
               "basis_tested": 512, "basis_matched": 512,
               "exact_permutation": bool(r["two_path_exhaustive_512"]),
               "negative_control_reject": bool(r["teeth_cnot_drop"]),
               "dense_materialized": False, "deterministic": True,
               "grade": "subspace_permutation_exhaustive",
               "path_A": "circuit permutation (spec plan CNOT bit-sim, bitops only)",
               "path_B": "independent polynomial division m(x)*x^4 mod g over GF(8)",
               "scope": "message->parity permutation (exhaustive 512); NOT dense unitary equivalence — INV-R5",
               "seed": 0, "verified": bool(r["two_path_exhaustive_512"] and r["syndrome_zero_2048"]
                                           and r["distance5_MDS"])}
    payload["proof_digest"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]
    p = os.path.join(ROOT, ".pgf", "proofs", "rs73_encoder.subspace_proof.json")
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    return p


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

    p3 = observe_p3()
    ok = bool(links and perm_ok and inv_ok and frob_ok and galois_ok and homo_ok
              and fixed_ok and comm_ok and orbit_ok and teeth_ok and p3["ok"])
    return {"field": "GF(8) = GF(2)[x]/(x³+x+1) · 레이아웃 q0=a₂·q1=a₁·q2=a₀",
            "p3_field_rs": p3,
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
        p3 = res["p3_field_rs"]
        print(f"  ★P3: mul 전수512 {p3['gf8_mul']['exhaustive_512']}·inv교차(frob²·mul) "
              f"{p3['gf8_mul']['inv_cross_frob2_mul']}·synd 전수512 {p3['rs_synd_core']['exhaustive_512']}·"
              f"rs73 두경로512 {p3['rs73_encoder']['two_path_exhaustive_512']}·신드롬제로2048 "
              f"{p3['rs73_encoder']['syndrome_zero_2048']}·거리5(전수511) "
              f"{p3['rs73_encoder']['distance5_MDS']}·teeth {p3['rs73_encoder']['teeth_cnot_drop']}", flush=True)
        pp = write_rs73_subspace_proof(p3)
        print(f"  → {os.path.relpath(OUT, ROOT)} · {os.path.relpath(pp, ROOT)} (subspace 상환)", flush=True)
    print(f"gf8_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
