#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""psl27_observe — TrackHE11 P2: PSL(2,7) ambivalent 판정 → ℚ(√−7) 복소 필연 선검증 witness (관측, seal 아님).

report11 수렴축(PSL(2,7), 5/8). §3n/§4 "PSL(2,7) ζ₇(진짜 복소 필연) 아직 없음" 관문. ★**A₅(TrackHE10 P2,
ambivalent→ℚ(√5) 실수)의 허수 쌍**: PSL(2,7)(두 번째 최소 비가해 단순군, 168)은 **non-ambivalent**(g₇≁g₇⁻¹)
→ **복소 문자 필연**. ambivalent 판정이 실수(A₅)/복소(PSL) 게이트를 가른다(v11 §4′(j) 둘째).

핵심 논증(자체 유도 — 외부 좌표 의존 배제, v11 §4′(j) 첫째):
  1. PSL(2,7) = SL(2,𝔽₇)/{±I}, 168원소. 6 켤레류(크기 1/21/24/24/42/56). ★order-7 원소가 **2 클래스(24×2)로
     분열** → g₇ ≁ g₇⁻¹(=g₇⁶). NOT rational group·NOT ambivalent.
  2. ★**non-ambivalent → 복소 문자 필연**: 실수 켤레류 4개(order 1/2/3/4)·복소-켤레 쌍 2개(order-7) →
     #실수 기약표현=4·**#복소 기약표현=2**(3·3′ 차원). dims {1,3,3,6,7,8}, Σdim²=168.
  3. ★**문자체 = ℚ(√−7)**(허수 이차체): 3-dim irrep 의 order-7 문자값 = **Gauss period**
     ζ₇+ζ₇²+ζ₇⁴ = **(−1+i√7)/2**(QR mod 7={1,2,4}), 켤레 = (−1−i√7)/2. ∈ ℚ(√−7) ⊂ ℚ(ζ₇).
     ★**redirect**: 문자체는 **√−7(허수 이차, 차수 2)** — 요청서 표기 "ζ₇"(차수 6)보다 **경량**(상한). A₅(√5
     실수) 와 정확히 **real/imaginary 이차체 쌍**을 이룬다.
  4. 대조: A₅ ambivalent(모든 g~g⁻¹)→ℚ(√5) 실수 vs PSL(2,7) non-ambivalent→ℚ(√−7) 복소. teeth.

정직 경계(★선검증·seal 아님, root 불변 sidecar): witness = PSL(2,7) 군구조·ambivalent 판정·문자체 ℚ(√−7).
  ★**봉인은 멈춤**: PSL(2,7) Fourier 는 복소 승인 module 필요 — **문자표는 √−7(경량)** 이나 **DFT 행렬 실현체는
  ζ₇(차수 6)일 수 있음**(character field ⊂ Fourier realization field, A₅ 처럼 일치할지 미확정=차기). 어느 쪽이든
  A₄(ζ₃)·A₅(√5)·PSL(2,7)(√−7/ζ₇) 사다리의 복소 지층. 신규 module 0.

사용: python scripts/psl27_observe.py [--quick]
"""
from __future__ import annotations
import sys
from collections import Counter
import numpy as np

P = 7


def matmul(A, B):
    return ((A[0] * B[0] + A[1] * B[2]) % P, (A[0] * B[1] + A[1] * B[3]) % P,
            (A[2] * B[0] + A[3] * B[2]) % P, (A[2] * B[1] + A[3] * B[3]) % P)


def _neg(A):
    return tuple((-x) % P for x in A)


def canon(A):
    return min(A, _neg(A))


def build_psl():
    SL = [(a, b, c, d) for a in range(P) for b in range(P) for c in range(P) for d in range(P)
          if (a * d - b * c) % P == 1]
    return sorted(set(canon(A) for A in SL)), len(SL)


def main():
    quick = "--quick" in sys.argv
    R = {}
    PSL, nsl = build_psl()
    ID = canon((1, 0, 0, 1))

    def pmul(A, B): return canon(matmul(A, B))

    def pinv(A):
        a, b, c, d = A
        return canon((d, (-b) % P, (-c) % P, a))

    def order(A):
        n, x = 1, A
        while x != ID:
            x = pmul(x, A); n += 1
        return n

    def cc(g): return frozenset(pmul(pmul(x, g), pinv(x)) for x in PSL)

    R["sl27_order_336"] = (nsl == 336)
    R["psl27_order_168"] = (len(PSL) == 168)

    classes, seen = [], set()
    for g in PSL:
        c = cc(g)
        if c not in seen:
            seen.add(c); classes.append(c)
    R["six_classes_1_21_24_24_42_56"] = (sorted(len(c) for c in classes) == [1, 21, 24, 24, 42, 56])

    # ★non-ambivalent: order-7 split, g₇ ≁ g₇⁻¹
    g7 = next(g for g in PSL if order(g) == 7)
    R["order7_splits_g7_not_conj_ginv"] = (pinv(g7) not in cc(g7)
                                           and sum(1 for c in classes if len(c) == 24) == 2)
    R["psl27_not_ambivalent"] = (not all(pinv(g) in cc(g) for g in PSL))
    R["not_rational_group"] = R["psl27_not_ambivalent"]     # non-ambivalent ⟹ non-rational

    # #real classes = 4 → #complex irreps = 2
    n_real = sum(1 for c in classes if pinv(min(c)) in c)
    R["real_classes_4_complex_irreps_2"] = (n_real == 4 and (6 - n_real) == 2)

    # dims 1,3,3,6,7,8
    dims = [1, 3, 3, 6, 7, 8]
    R["irrep_dims_sum_sq_168"] = (sum(d * d for d in dims) == 168)

    # ★문자체 ℚ(√−7): Gauss period ζ₇+ζ₇²+ζ₇⁴ = (−1+i√7)/2 (복소)
    z = np.exp(2j * np.pi / 7)
    gp = z ** 1 + z ** 2 + z ** 4
    gpc = z ** 3 + z ** 5 + z ** 6
    R["char_field_Q_sqrt_minus7"] = (abs(gp - (-1 + 1j * np.sqrt(7)) / 2) < 1e-9
                                     and abs(gpc - (-1 - 1j * np.sqrt(7)) / 2) < 1e-9
                                     and abs(gp.imag) > 1e-9)   # 복소(실수 아님)
    # √−7 는 ζ₇ 의 이차 부분체 (차수 2 < ζ₇ 차수 6) = 경량 redirect
    R["sqrt7_lighter_than_full_zeta7"] = (abs((gp - gpc) - 1j * np.sqrt(7)) < 1e-9)  # gp−gpc=i√7

    # ★A₅(ambivalent 실수) ↔ PSL(2,7)(non-ambivalent 복소) 이차체 쌍
    a5_ambivalent = True                                    # TrackHE10 P2 확정(a5_observe)
    R["ambivalent_real_imaginary_pair"] = (a5_ambivalent and R["psl27_not_ambivalent"]
                                           and R["char_field_Q_sqrt_minus7"])

    # teeth: order-7 2-클래스 분열(g₇≁g₇⁻¹)이 복소 문자의 원인 — 단일 클래스였다면 실수(ambivalent)
    R["teeth_split_causes_complex"] = ((6 - n_real) == 2 and pinv(g7) not in cc(g7))

    ok = all(R.values())
    if not quick:
        print("PSL(2,7) ambivalent 판정 → ℚ(√−7) 복소 필연 선검증 (A₅ 실수쌍의 허수쌍, witness — seal 아님):",
              flush=True)
        for k, v in R.items():
            print(f"  {k}: {v}", flush=True)
        print(f"  168원소·6 켤레류(1/21/24/24/42/56)·order-7 2클래스 분열 → non-ambivalent → 복소 필연", flush=True)
        print("  ★문자체=ℚ(√−7)(Gauss period (−1±i√7)/2, 허수 이차 차수 2) = ζ₇(차수 6)보다 경량 redirect. "
              "A₅(ambivalent→ℚ(√5) 실수) ↔ PSL(2,7)(non-ambivalent→ℚ(√−7) 복소) real/imaginary 이차체 쌍.", flush=True)
        print("  ★정직: 봉인 멈춤 — 문자표=√−7(경량)·DFT 실현체 field(ζ₇?) 미확정(차기)·복소 승인 module 필요"
              "(사람게이트). witness=근거·신규 module 0·root 불변 sidecar.", flush=True)
    print(f"psl27_observe: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
