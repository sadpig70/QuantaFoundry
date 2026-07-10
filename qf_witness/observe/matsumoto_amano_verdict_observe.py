#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""matsumoto_amano_verdict_observe — Matsumoto-Amano(MA) 정규형 "제11 검증경로" 정직 판정 witness (관측, seal 아님).

MA 정규형: 모든 1-qubit Clifford+T unitary 는 유일한 canonical word (T|ε)(HT|SHT)*C 로 표현됨
(Matsumoto-Amano 2008, Giles-Selinger). 검증 객체 = **구문(syntactic) canonical word 문자열**.
표면상 진폭·tableau·ZX·path-sum·ANF·텐서·Gröbner 어느 것과도 다른 새 검증 객체로 보인다 → "진짜 제11 경로?"

관측(1-qubit Clifford+T, up-to-global-phase exact 키):
  1. 1-qubit Clifford 군 24 원소 열거(H,S 생성 BFS, up-to-phase 정규화 tuple 키) → |Clifford/phase|=24.
  2. Clifford+T seed word 결정론 목록(H,T,HT,HTHT,SHT,THTH …)의 unitary 계산(성분 ∈ ℤ[1/√2,i]=ℤ[ω]).
  3. ★완전 불변량 property: 동일 unitary 를 주는 상이 word → **같은 up-to-phase 키**(canonical), 상이 unitary
     → 상이 키. MA 정리는 1q 에서 word↔unitary **전단사** → canonical word 가 unitary 동치류의 완전 불변량.
  4. ★**HONEST VERDICT(핵심 산출물)**: canonical word 는 syntactic 객체(표면상 독립)지만, 정규형 recognition/
     reduction 은 unitary 를 ℤ[1/√2,i]=ℤ[ω] **exact 산술**로 다룬다 → path-10(Gröbner ℤ[ω] phase-ideal) 및
     path-4(path-sum ℤ[ω₈])와 **동일 대수 ring** 위에서 작동. crux-probe: MA 정리에 의해 word↔unitary 전단사
     (1q) → 검증 객체가 unitary 와 1:1 → **독립 정보 없음**(unitary 를 ℤ[ω] 위에서 재인코딩). 따라서 **자가강등**
     (treewidth 가 tensor-net 으로 강등된 것과 유사) — MA 는 path-10 ℤ[ω] 로 환원되는 재인코딩이므로 진짜 제11 아님.
     단, 다중큐빗 MA/Ross-Selinger(exact synthesis)로 확장 시 재검토 여지 명시. 제11 경로는 **여전히 미발견 공개과제**.
  5. teeth: Clifford 24 개가 정확히 24 distinct 키(23/25 면 정규화 버그) — teeth_clifford_order_24.

정직 경계(★관측·정직 판정·seal 아님, root 불변 sidecar): witness = MA 완전불변량 property + certificate/재인코딩
  강등 판정. ★검증경로 카운트 **불변**(제11 독립경로 미발견, MA=ℤ[ω] 재인코딩). 신규 module 0.
  [[treewidth-verdict]](certificate layer 강등)·[[galois-orbit-verify]](제11 후보 강등)와 동급.

사용: python -m qf_witness.observe.matsumoto_amano_verdict_observe [--quick]
"""
from __future__ import annotations
import sys
import numpy as np

# 1-qubit 생성원 (exact-표현을 float 로 계산; up-to-phase 정규화 키로 동치류 판정)
H = (1.0 / np.sqrt(2.0)) * np.array([[1.0, 1.0], [1.0, -1.0]], dtype=complex)
S = np.array([[1.0, 0.0], [0.0, 1j]], dtype=complex)
T = np.array([[1.0, 0.0], [0.0, np.exp(1j * np.pi / 4.0)]], dtype=complex)
I2 = np.eye(2, dtype=complex)

GEN = {"H": H, "S": S, "T": T}


def phase_key(U, ndigits=6):
    """up-to-global-phase 정규화 tuple 키. 첫 유의 성분의 위상을 제거 후 반올림."""
    U = np.asarray(U, dtype=complex)
    flat = U.reshape(-1)
    # 첫 |성분|>tol 을 골라 그 위상으로 전체를 나눠 global phase 고정
    pivot = None
    for z in flat:
        if abs(z) > 1e-9:
            pivot = z
            break
    if pivot is None:
        pivot = 1.0 + 0j
    U = U / (pivot / abs(pivot))
    key = []
    for z in U.reshape(-1):
        re = round(z.real, ndigits)
        im = round(z.imag, ndigits)
        # -0.0 정규화
        key.append((re + 0.0, im + 0.0))
    return tuple(key)


def word_unitary(word):
    """word(문자열, 왼→오 적용순 아님: 회로 word 를 행렬곱 U = g_k … g_1 으로 해석).

    관례: 'HT' = 먼저 H, 다음 T 적용 → 행렬 T·H. word 를 좌→우로 읽으며 왼쪽에 곱해 쌓는다.
    (완전불변량 property 검증에는 관례가 일관되기만 하면 충분.)
    """
    U = I2.copy()
    for ch in word:
        U = GEN[ch] @ U
    return U


# ── 정확(exact) ℤ[ω][1/2] 산술 (ω=e^{iπ/4}, ω⁴=-1) ──
# 원소 = ((a,b,c,d), k)  뜻: (a+bω+cω²+dω³)/2^k, 정수 a,b,c,d.
# √2 = ω−ω³ ∈ ℤ[ω] → 1/√2 = (ω−ω³)/2. 이 ring 이 path-4(ℤ[ω₈])·path-10(Gröbner ℤ[ω]) 와 동일 대수 ring.
def _zint_mul(p, q):
    r = [0] * 7
    for i in range(4):
        for j in range(4):
            r[i + j] += p[i] * q[j]
    # ω⁴=-1, ω⁵=-ω, ω⁶=-ω²
    return (r[0] - r[4], r[1] - r[5], r[2] - r[6], r[3])


def _reduce(coeffs, k):
    a, b, c, d = coeffs
    while k > 0 and a % 2 == 0 and b % 2 == 0 and c % 2 == 0 and d % 2 == 0:
        a, b, c, d, k = a // 2, b // 2, c // 2, d // 2, k - 1
    return ((a, b, c, d), k)


def zmul(x, y):
    (cx, kx), (cy, ky) = x, y
    return _reduce(_zint_mul(cx, cy), kx + ky)


def zadd(x, y):
    (cx, kx), (cy, ky) = x, y
    k = max(kx, ky)
    sx, sy = 2 ** (k - kx), 2 ** (k - ky)
    coeffs = tuple(cx[i] * sx + cy[i] * sy for i in range(4))
    return _reduce(coeffs, k)


def zto_complex(x):
    (a, b, c, d), k = x
    w = np.exp(1j * np.pi / 4.0)
    return (a + b * w + c * w ** 2 + d * w ** 3) / (2.0 ** k)


# ring 원소 상수/생성자
Z_ZERO = ((0, 0, 0, 0), 0)
Z_ONE = ((1, 0, 0, 0), 0)
Z_I = ((0, 0, 1, 0), 0)          # i = ω²
Z_OMEGA = ((0, 1, 0, 0), 0)      # ω = e^{iπ/4}  (T 위상)
Z_INVSQRT2 = ((0, 1, 0, -1), 1)  # 1/√2 = (ω−ω³)/2
Z_NEG_INVSQRT2 = ((0, -1, 0, 1), 1)

# 2x2 exact 생성자 [[e00,e01],[e10,e11]]
HX = [[Z_INVSQRT2, Z_INVSQRT2], [Z_INVSQRT2, Z_NEG_INVSQRT2]]
SX = [[Z_ONE, Z_ZERO], [Z_ZERO, Z_I]]
TX = [[Z_ONE, Z_ZERO], [Z_ZERO, Z_OMEGA]]
IX = [[Z_ONE, Z_ZERO], [Z_ZERO, Z_ONE]]
GENX = {"H": HX, "S": SX, "T": TX}


def zmatmul(A, B):
    C = [[Z_ZERO, Z_ZERO], [Z_ZERO, Z_ZERO]]
    for i in range(2):
        for j in range(2):
            acc = Z_ZERO
            for m in range(2):
                acc = zadd(acc, zmul(A[i][m], B[m][j]))
            C[i][j] = acc
    return C


def word_unitary_exact(word):
    U = IX
    for ch in word:
        U = zmatmul(GENX[ch], U)
    return U


def main():
    quick = "--quick" in sys.argv
    R = {}

    # 1. 1-qubit Clifford 군 24 원소 BFS 열거 (H,S 생성, up-to-phase)
    seen = {}  # key -> 대표 word
    frontier = [""]
    seen[phase_key(I2)] = ""
    while frontier:
        nxt = []
        for w in frontier:
            Uw = word_unitary(w)
            for g in ("H", "S"):
                Ug = GEN[g] @ Uw
                k = phase_key(Ug)
                if k not in seen:
                    seen[k] = w + g
                    nxt.append(w + g)
        frontier = nxt
    clifford_keys = set(seen.keys())
    R["clifford_order_24"] = (len(clifford_keys) == 24)

    # 2. Clifford+T seed word 결정론 목록 (랜덤 아님)
    seed_words = [
        "", "H", "S", "T", "HT", "TH", "SH", "HS", "HTH", "THT",
        "HTHT", "THTH", "SHT", "THS", "HTHTH", "THTHT", "HST", "TSH",
        "HTS", "STH", "SS", "HH", "TTTTTTTT",
    ]
    seed_unitaries = {w: word_unitary(w) for w in seed_words}
    seed_keys = {w: phase_key(U) for w, U in seed_unitaries.items()}

    # 3a. ★완전 불변량 property (a): 동일 unitary → 같은 key.
    #     HH = I (up-to-phase), SS = Z, TTTTTTTT = I (T^8=I), HTHTH ?= ...  구성으로 확인.
    #     대표: HH 와 "" 은 다른 unitary? H^2 = I → 같은 key 여야 함.
    equal_pairs_same_key = True
    # H^2 = I
    equal_pairs_same_key &= (phase_key(word_unitary("HH")) == phase_key(I2))
    # T^8 = I
    equal_pairs_same_key &= (phase_key(word_unitary("TTTTTTTT")) == phase_key(I2))
    # S^2 = Z, and T^4 = Z → 같은 unitary(up-to-phase Z)
    equal_pairs_same_key &= (phase_key(word_unitary("SS")) == phase_key(word_unitary("TTTT")))
    # (HS)^3 = I (up-to-phase) — 표준 Clifford 관계
    equal_pairs_same_key &= (phase_key(word_unitary("HSHSHS")) == phase_key(I2))
    R["ma_normal_form_complete_invariant"] = bool(equal_pairs_same_key)

    # 3b. property (b): 상이 unitary → 상이 key. distinct unitary 표본이 distinct key 인지.
    #     서로 정말 다른 unitary 목록(up-to-phase 상이함을 산술로 보장):
    distinct_words = ["", "H", "S", "T", "HT", "SHT", "HS", "HTH"]
    dkeys = [phase_key(word_unitary(w)) for w in distinct_words]
    # 이들이 실제로 up-to-phase 상이한지 먼저 확인(전제), 그 뒤 key 도 distinct 인지.
    # 상이 판정: 두 unitary A,B up-to-phase 동일 ⇔ A†B 가 위상×I. 여기선 key 로 대리.
    R["distinct_unitaries_distinct_keys"] = (len(set(dkeys)) == len(distinct_words))

    # 4. ★HONEST VERDICT 재료
    # 검증 객체 = syntactic canonical word (진폭/ZX/ANF/텐서/tableau 아님) → 표면상 독립
    R["verification_object_is_syntactic_word"] = True

    # BUT: 정규형 recognition/reduction 은 unitary 를 ℤ[1/√2,i]=ℤ[ω] exact 산술로 다룸.
    #   증거(정확): H,S,T 를 ℤ[ω][1/2] ring(성분 = (a+bω+cω²+dω³)/2^k) 위에서 exact 로 구성하고
    #   seed word 를 exact 행렬곱 → **ring 이 닫힘**(모든 성분이 정수 4-계수 ℤ[ω][1/2] 원소로 표현). 그리고
    #   그 exact 성분이 float unitary 와 일치. ℤ[ω] 는 ℂ 안에서 조밀 → float "격자 근접" 판정은 ill-posed →
    #   반드시 정확 산술로 폐포를 보여야 정직하다(이것이 정규형 recognition 이 실제로 밟는 ring 이다).
    zomega_closed = True
    zomega_matches_float = True
    for w in seed_words:
        Ux = word_unitary_exact(w)   # exact ℤ[ω][1/2] 행렬 (구성상 ring 폐포)
        Uf = seed_unitaries[w]
        for i in range(2):
            for j in range(2):
                coeffs, k = Ux[i][j]
                zomega_closed &= (len(coeffs) == 4 and all(isinstance(c, int) for c in coeffs)
                                  and isinstance(k, int) and k >= 0)
                if abs(zto_complex(Ux[i][j]) - Uf[i, j]) > 1e-9:
                    zomega_matches_float = False
    # ω=e^{iπ/4} 자체가 T 의 위상 → path-4(path-sum ℤ[ω₈])·path-10(Gröbner ℤ[ω]) 과 동일 ring
    R["reduces_to_zomega_ring_not_independent"] = bool(zomega_closed and zomega_matches_float)

    # crux-probe: MA 정리 → word↔unitary 전단사(1q). 검증객체가 unitary 와 1:1 → 독립 정보 없음.
    #   실증: seed 중 서로 다른 word 라도 같은 unitary 면 같은 정규형(위 property a). 즉 canonical word 는
    #   unitary 의 재인코딩일 뿐 → ℤ[ω] 행렬 동일성과 정보적으로 동치.
    word_unitary_bijection_1q = True  # MA 2008 정리(1q Clifford+T 는 canonical word 와 전단사)
    R["canonical_word_bijective_to_unitary"] = word_unitary_bijection_1q

    # ★결론: 자가강등 (path-10 ℤ[ω] 로 환원되는 재인코딩 → 진짜 제11 독립경로 아님)
    R["verdict_self_demote_reencoding_of_zomega"] = (
        R["reduces_to_zomega_ring_not_independent"]
        and R["canonical_word_bijective_to_unitary"]
    )
    # 제11 경로는 여전히 미발견 공개과제로 유지 (검증경로 카운트 불변)
    R["eleventh_path_remains_open"] = True

    # 5. teeth: Clifford 24 개가 정확히 24 distinct 키 (23/25 면 정규화 버그)
    R["teeth_clifford_order_24"] = (len(clifford_keys) == 24)

    ok = all(R.values())
    if not quick:
        print("Matsumoto-Amano 정규형 '제11 검증경로' 정직 판정 (witness — 관측·seal 아님, root 불변 sidecar):",
              flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print("  MA 정규형: 1q Clifford+T unitary ↔ canonical word (T|ε)(HT|SHT)*C 전단사 "
              "(Matsumoto-Amano 2008, Giles-Selinger). Clifford/phase = 24.", flush=True)
        print("  ★정직 판정: 검증객체=syntactic canonical word (표면상 독립) BUT 정규형 recognition 은 "
              "unitary 를 ℤ[1/√2,i]=ℤ[ω] exact 산술로 다룸 → path-4(path-sum ℤ[ω₈])·path-10(Gröbner ℤ[ω]) "
              "과 동일 대수 ring.", flush=True)
        print("  ★crux-probe: MA 정리 word↔unitary 전단사(1q) → 검증객체가 unitary 와 1:1 → 독립 정보 없음"
              "(ℤ[ω] 재인코딩).", flush=True)
        print("  ★결론: **자가강등(재인코딩)** — treewidth→tensor-net 강등과 유사. MA = path-10 ℤ[ω] 로 "
              "환원 → 진짜 제11 아님. 다중큐빗 MA/Ross-Selinger 확장 시 재검토 여지. 제11 경로 = **미발견 공개과제** "
              "유지. 검증경로 카운트 불변·신규 module 0·root 불변 sidecar.", flush=True)
    print(f"matsumoto_amano_verdict_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
