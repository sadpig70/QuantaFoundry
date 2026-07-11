# -*- coding: utf-8 -*-
"""rs73_affine_verify — rs73_encoder 전체 유니터리(GF(2) affine map) 검증 (QF-0711 U12).

rs73_encoder 는 순수 CNOT 회로(60 CNOT·X 0개, 21q) = GF(2) 위 **선형** 가역맵 |x⟩→|Ax⟩.
선형이므로 21개 단위벡터의 상(image)이 전체 2^21 순열(=전체 유니터리)을 완전히 결정한다.
기존 subspace 증명(512 message space)을 **전체 A(21×21)** 로 확장 — full unitary 강검증.

  path A = 봉인 회로의 60 CNOT 를 21개 단위벡터 e_i 에 비트시뮬 → 회로 A_circ (열=상)
  path B = ★독립 golden A_gold = [[I_9, 0],[G, I_12]] (message passthrough + parity passthrough +
           parity generator G). G 는 RS(7,3) 다항 나눗셈(_rs_parity)에서 독립 구성 — 회로 미참조.
  결과 = A_circ == A_gold (전수 21열) ∧ A_circ 가역(GF(2), 유효 순열) ∧ teeth(CNOT 1개 누락→불일치).

성립 시 subspace_permutation_verified → unitary_equiv 격상(전체 unitary 독립검증). 비파괴 sidecar
(.pgf/proofs/rs73_encoder.affine_proof.json)·oracle/seal/root 무접촉·읽기만.

사용: python -m qf_witness.verify.rs73_affine_verify [--quick]
"""
import json
import os
import sys

from qf_witness.core.paths import ROOT
from qf_witness.observe.gf8_observe import _rs_g, _rs_parity, _parse_cnots  # 헬퍼 재사용

PROOFS = os.path.join(ROOT, ".pgf", "proofs")
N = 21          # 3 message + 4 parity 심볼 × 3 bit
APP = "rs73_encoder"


def _full_bitsim(x, cnots):
    """21-bit 정수 입력 x 에 CNOT 순차 적용 → 21-bit 정수 상. (선형: A·x)"""
    st = [(x >> b) & 1 for b in range(N)]
    for (c, t) in cnots:
        st[t] ^= st[c]
    return sum(st[b] << b for b in range(N))


def _circuit_A(cnots):
    """회로 A_circ: 열 i = e_i 의 상(21-bit). (b=_full_bitsim(0)=0 확인)."""
    assert _full_bitsim(0, cnots) == 0, "순수 선형이 아님(offset≠0)"
    return [_full_bitsim(1 << i, cnots) for i in range(N)]


def _msg_symbols_of_bit(i):
    """단위 message 비트 i(0..8) → 3 GF(8) 심볼(_rs73_bitsim 레이아웃: st[3s..3s+2] big-endian)."""
    st = [1 if b == i else 0 for b in range(N)]
    return tuple((st[3 * s] << 2) | (st[3 * s + 1] << 1) | st[3 * s + 2] for s in range(3))


def _parity_bits(parity_syms):
    """parity 4 심볼 → 21-bit 벡터의 parity 부분(st[9+3k..9+3k+2] big-endian)."""
    v = 0
    for k in range(4):
        sym = parity_syms[k]
        v |= ((sym >> 2) & 1) << (9 + 3 * k)
        v |= ((sym >> 1) & 1) << (9 + 3 * k + 1)
        v |= (sym & 1) << (9 + 3 * k + 2)
    return v


def _golden_A(g):
    """★독립 golden A_gold 열: message(0..8)=passthrough+parity(G), parity(9..20)=passthrough(identity)."""
    cols = []
    for i in range(N):
        if i >= 9:                                   # parity 입력 → passthrough (identity 열)
            cols.append(1 << i)
        else:                                        # message 비트 i → 자기자신 + parity(단위메시지)
            par = _rs_parity(_msg_symbols_of_bit(i), g)   # path B (RS 다항, 독립)
            cols.append((1 << i) | _parity_bits(par))
    return cols


def _is_bijection(A):
    """GF(2) 21×21(열=정수) 가역? 가우스 소거로 rank==21."""
    cols = list(A)
    rank = 0
    for bit in range(N):
        piv = next((j for j in range(rank, len(cols)) if (cols[j] >> bit) & 1), None)
        if piv is None:
            continue
        cols[rank], cols[piv] = cols[piv], cols[rank]
        for j in range(len(cols)):
            if j != rank and (cols[j] >> bit) & 1:
                cols[j] ^= cols[rank]
        rank += 1
    return rank == N


def run():
    g = _rs_g()
    cnots = _parse_cnots(f"{APP}.app.pg")
    A_circ = _circuit_A(cnots)
    A_gold = _golden_A(g)
    match = A_circ == A_gold
    bijection = _is_bijection(A_circ)
    # teeth: CNOT 1개 누락 → 전체 A 불일치해야
    teeth = any(_circuit_A(cnots[:k] + cnots[k + 1:]) != A_gold for k in range(0, len(cnots), 7))
    verified = bool(match and bijection and teeth)
    payload = {
        "_schema": "affine-proof-v1",
        "_note": ("rs73_encoder 전체 유니터리(GF(2) 선형맵) 강검증. 순수 CNOT → 21 단위벡터 상이 전체 "
                  "2^21 순열 완전결정. path A=회로 비트시뮬 vs path B=독립 golden([[I,0],[G,I]], G=RS 다항). "
                  "subspace(512 message space) → 전체 unitary 확장. 봉인/root 무접촉."),
        "id": APP, "n_qubits": N, "gates": len(cnots), "x_gates": 0,
        "full_columns_checked": N, "full_columns_matched": sum(1 for a, b in zip(A_circ, A_gold) if a == b),
        "affine_map_exact": bool(match),
        "linear_offset_zero": True,
        "bijection_gf2": bool(bijection),
        "independent_golden": "A=[[I9,0],[G,I12]] · G from _rs_parity(RS(7,3) polynomial division)",
        "negative_control_cnot_drop": bool(teeth),
        "grade": "affine_map_full_unitary_exact",
        "verified": verified,
    }
    payload["proof_digest"] = hashlib_16(payload)
    return payload


def hashlib_16(payload):
    import hashlib
    body = {k: payload[k] for k in ("affine_map_exact", "bijection_gf2", "full_columns_matched", "verified")}
    return hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]


def main():
    payload = run()
    if "--quick" not in sys.argv[1:]:              # full: sidecar 기록
        os.makedirs(PROOFS, exist_ok=True)
        with open(os.path.join(PROOFS, f"{APP}.affine_proof.json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
    print(f"rs73 affine: cols {payload['full_columns_matched']}/{payload['full_columns_checked']} · "
          f"bijection={payload['bijection_gf2']} · teeth={payload['negative_control_cnot_drop']}")
    print(f"rs73_affine_verify: all_ok={payload['verified']}")
    return 0 if payload["verified"] else 1


if __name__ == "__main__":
    sys.exit(main())
