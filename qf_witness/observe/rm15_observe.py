#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rm15_observe — TrackHE5 P4: RM [[15,1,3]] + transversal T witness (dense-free 정수/심볼릭, 봉인 0 관측층).

봉인된 rm15_encoder_t2(Tier-2 module, 완전 논리-입력 인코더)·rm15_tt(T^⊗15, Tier-1)에 대해:
  1. seal 링크 2 (module + app).
  2. ★부호 구조 정수 witness: X-stab 4(무게 8)·Z-stab 10(4+6, 무게 4/8)·CSS 가환 전수·
     논리쌍 X̄'(무게 7)↔Z̄={q0,q1,q2}(반교환 1)·씨앗-서로소 구조(인코더 순서 논거).
  3. ★인코더 심볼릭 안정군 역전파(오라클·dense 독립 — **봉인 spec 의 bloq 배선을 파싱**해 검증):
     코드 안정자 14개 → +Z_ancilla 군 · X̄'→X_{q14} · Z̄→Z-string(q14 포함) 전부 부호 +.
     자가대조: Steane 7q 인코더(기봉인 정의)로 전파 구현 자체를 검증.
  4. ★transversal T 정수 witness: C_X 16 성분 무게 ≡0 (mod 8) · coset X̄'⊕C_X ≡7 —
     ⇒ T^⊗15 코드공간 작용 = diag(1, ω₈⁻¹) = 논리 T† (계수 전수, dense 불요).
  5. ★거리 정확히 3: weight≤2 X/Z/Y 오류 전수 검출(신드롬 비영) + 무게-3 Z̄ 비검출(논리).
  6. 대비 관측: code832(거리-2·CCZ 횡단·8q) vs rm15(거리-3·T 횡단·15q) — triorthogonal family 계보.
  7. teeth: ①인코더 CNOT 1개 누락 → 안정군 역전파 실패 ②T 1개→T† 교체 → coset 위상 균일성 붕괴
     ③가짜 Z̄(무게-3 비논리) → 반교환 조건 실패.

정직 경계(INV-Q3, root 성장은 module 1 + 앱 1 봉인분뿐):
  - 봉인 = 인코더 tableau(Tier-2)·T-패턴 구조(Tier-1 정직 라벨)뿐. 논리 작용·거리 = 정수 witness.
  - 15-to-1 증류의 성공확률·후선택·반복 = 범위 밖. n=15 dense 미실체화(전 witness 가 비트연산).

사용: python -m qf_witness.observe.rm15_observe [--quick]
"""
import os, sys, re, json
from itertools import combinations, product
import numpy as np

from qf_witness.core.paths import ROOT
OUT = os.path.join(ROOT, ".pgf", "proofs", "RM15-OBSERVE.json")

SEEDS = [0, 1, 3, 7]
S = [[q for q in range(15) if ((q + 1) >> i) & 1] for i in range(4)]
LP = [q for q in range(15) if bin(q + 1).count("1") % 2 == 0]
P0 = 14
ZBAR = [0, 1, 2]


def vec(supp):
    m = 0
    for q in supp:
        m |= 1 << q
    return m


def seal_link(store, sid):
    p = os.path.join(ROOT, "registry", store, f"{sid}.sealed.json")
    return os.path.exists(p) and bool(json.load(open(p, encoding="utf-8")).get("u_hash"))


def parse_bloq_gates(spec_path):
    """봉인 module spec 의 bloq 코드에서 (h|cnot) 게이트 열 추출 — 봉인 배선 그대로 검증."""
    src = open(spec_path, encoding="utf-8").read()
    code = src.split("id=bloq\n")[1].split("```")[0]
    gates = []
    for line in code.splitlines():
        m = re.match(r"qs\[(\d+)\] = bb\.add\(Hadamard\(\), q=qs\[\d+\]\)", line.strip())
        if m:
            gates.append(("h", int(m.group(1))))
            continue
        m = re.match(r"qs\[(\d+)\], qs\[(\d+)\] = bb\.add\(CNOT\(\), ctrl=qs\[\d+\], target=qs\[\d+\]\)",
                     line.strip())
        if m:
            gates.append(("cnot", int(m.group(1)), int(m.group(2))))
    return gates


def prop(pauli, gates):
    """(x마스크, z마스크, 부호 s) 를 게이트열로 켤레 — 이진 심플렉틱 + 위상비트."""
    x, z, s = pauli
    for g in gates:
        if g[0] == "h":
            q = 1 << g[1]
            xb, zb = bool(x & q), bool(z & q)
            if xb and zb:
                s ^= 1
            if xb != zb:
                x ^= q
                z ^= q
        else:
            c, t = 1 << g[1], 1 << g[2]
            if bool(x & c) and bool(z & t) and (bool(x & t) == bool(z & c)):
                s ^= 1
            if x & c:
                x ^= t
            if z & t:
                z ^= c
    return (x, z, s)


def inv_gates(gates):
    return list(reversed(gates))          # H·CNOT 자기역


def steane_selftest():
    HAM = [[0, 0, 0, 1, 1, 1, 1], [0, 1, 1, 0, 0, 1, 1], [1, 0, 1, 0, 1, 0, 1]]
    A = np.array(HAM) % 2
    pivots, r = [], 0
    for c in range(7):
        sel = [i for i in range(r, 3) if A[i, c] == 1]
        if not sel:
            continue
        A[[r, sel[0]]] = A[[sel[0], r]]
        for i in range(3):
            if i != r and A[i, c] == 1:
                A[i] = (A[i] + A[r]) % 2
        pivots.append(c)
        r += 1
    gates = [("h", p) for p in pivots]
    for i, p in enumerate(pivots):
        for j in range(7):
            if j != p and A[i, j] == 1:
                gates.append(("cnot", p, j))
    ig = inv_gates(gates)
    ok = True
    for row in HAM:
        xm = sum(1 << j for j in range(7) if row[j])
        for P in [(xm, 0, 0), (0, xm, 0)]:
            x, z, s = prop(P, ig)
            ok &= (x == 0 and s == 0)
    return ok


def observe():
    links = seal_link("modules", "rm15_encoder_t2") and seal_link("apps", "rm15_tt")

    # 2. 부호 구조 정수 witness
    ZS = [vec(S[i]) for i in range(4)]
    for i, j in combinations(range(4), 2):
        ZS.append(vec([q for q in range(15) if ((q + 1) >> i) & 1 and ((q + 1) >> j) & 1]))
    css_ok = all(bin(vec(S[i]) & z).count("1") % 2 == 0 for i in range(4) for z in ZS)
    zbar, lpv = vec(ZBAR), vec(LP)
    logical_pair = bool(all(bin(vec(S[i]) & zbar).count("1") % 2 == 0 for i in range(4))
                        and all(bin(z & lpv).count("1") % 2 == 0 for z in ZS)
                        and bin(lpv & zbar).count("1") % 2 == 1)
    seeds_ok = bool(all((SEEDS[i] in S[i]) and all(SEEDS[i] not in S[j] for j in range(4) if j != i)
                        for i in range(4)) and not set(SEEDS) & set(LP))
    struct_ok = css_ok and logical_pair and seeds_ok

    # 3. 인코더 심볼릭 역전파 (봉인 spec 배선)
    st_self = steane_selftest()
    gates = parse_bloq_gates(os.path.join(ROOT, "specs", "modules", "rm15_encoder_t2.pg"))
    ig = inv_gates(gates)
    enc_ok = bool(len(gates) == 38)
    for i in range(4):
        x, z, s = prop((vec(S[i]), 0, 0), ig)
        enc_ok &= (x == 0 and s == 0 and (z & (1 << P0)) == 0)
    for zm in ZS:
        x, z, s = prop((0, zm, 0), ig)
        enc_ok &= (x == 0 and s == 0 and (z & (1 << P0)) == 0)
    x, z, s = prop((lpv, 0, 0), ig)
    enc_ok &= (x == (1 << P0) and s == 0 and (z & (1 << P0)) == 0)
    x, z, s = prop((0, zbar, 0), ig)
    enc_ok &= (x == 0 and s == 0 and bool((z >> P0) & 1))

    # 4. transversal T 정수 witness
    CX = []
    for a in range(16):
        m = 0
        for i in range(4):
            if (a >> i) & 1:
                m ^= vec(S[i])
        CX.append(m)
    t_ok = bool(all(bin(c).count("1") % 8 == 0 for c in CX)
                and all(bin(c ^ lpv).count("1") % 8 == 7 for c in CX))

    # 5. 거리 == 3
    det_ok = True
    for w in (1, 2):
        for qs in combinations(range(15), w):
            for tps in product("XZY", repeat=w):
                ex = sum(1 << q for q, t in zip(qs, tps) if t in "XY")
                ez = sum(1 << q for q, t in zip(qs, tps) if t in "ZY")
                syn = any(bin(ez & vec(S[i])).count("1") % 2 for i in range(4)) or \
                      any(bin(ex & zz).count("1") % 2 for zz in ZS)
                det_ok &= syn
    d3_ok = bool(det_ok and not any(bin(zbar & vec(S[i])).count("1") % 2 for i in range(4)))

    # 7. teeth
    ig_bad = inv_gates(gates[:-1])                       # CNOT 1개 누락
    x, z, s = prop((vec(S[3]), 0, 0), ig_bad)
    t1 = bool(not (x == 0 and s == 0))
    # T 1개→T†: 위상 = Σ_q s_q·bit_q, s = [1]*14+[-1]: coset 위상 균일성 붕괴?
    phases1 = {(sum(1 if q != 14 else -1 for q in range(15) if ((c ^ lpv) >> q) & 1)) % 8
               for c in CX}
    t2 = bool(len(phases1) > 1)
    fake = vec([0, 1, 3])                                # 무게-3 비논리 후보
    t3 = bool(any(bin(fake & vec(S[i])).count("1") % 2 for i in range(4))
              or bin(fake & lpv).count("1") % 2 == 0)
    teeth_ok = t1 and t2 and t3

    # ★TrackHE6 P1: 15-to-1 증류 측정 전 coherent — rm15_decoder_t2(인코더 역 = syndrome 추출 코어)
    dec_p = os.path.join(ROOT, "registry", "modules", "rm15_decoder_t2.sealed.json")
    dec_link = os.path.exists(dec_p) and bool(json.load(open(dec_p, encoding="utf-8")).get("u_hash"))
    dec_gates = parse_bloq_gates(os.path.join(ROOT, "specs", "modules", "rm15_decoder_t2.pg")) \
        if dec_link else []
    # 디코더 = 인코더 역순 (H/CNOT 자기역)
    dag_ok = bool(dec_gates == list(reversed(gates)))
    # ★디코더 정전파 = 인코더 역전파(ig): 코드 안정자 → +Z_ancilla(syndrome 노출)·논리 사상
    #   유효 부호어(코드 안정자 +1 고유상태) → syndrome=0(ancilla |0⟩) = accept 부분공간
    syndrome_expose = enc_ok      # 동일 심볼릭 전파(디코더=인코더†) — 코드안정자→Z_anc·논리→q14
    # ★weight-1 오류 → syndrome≠0 (accept 거부 = 증류 검출): 오류 E 가 코드안정자와 반교환
    reject_ok = True
    for q in range(15):
        exz = [(1 << q, 0), (0, 1 << q)]   # X_q, Z_q
        for exm, ezm in exz:
            syn = any(bin(ezm & vec(S[i])).count("1") % 2 for i in range(4)) or \
                  any(bin(exm & zz).count("1") % 2 for zz in ZS)
            reject_ok &= syn              # weight-1 = 항상 syndrome≠0 (거리-3)
    # accept 사영자 = 14 syndrome ancilla = 0 (multi-controlled 구조, 정수 조건)
    accept_ok = bool(dag_ok and syndrome_expose and reject_ok)
    distill_ok = bool(dec_link and accept_ok)

    ok = bool(links and struct_ok and st_self and enc_ok and t_ok and d3_ok and teeth_ok
              and distill_ok)
    return {"code": "[[15,1,3]] punctured Reed-Muller — 15-to-1 magic 증류 정준 기판 (거리-3 transversal-T)",
            "seal_links_module_app": links,
            "distillation_coherent_P1": {"decoder_sealed": dec_link,
                                         "decoder_eq_encoder_dag": dag_ok,
                                         "syndrome_extraction_exposes_ancilla": syndrome_expose,
                                         "weight1_error_rejected_syndrome_nonzero": reject_ok,
                                         "accept_projector_14_syndrome_zero": accept_ok,
                                         "note": "★측정 전 coherent 증류 코어 = 디코더(인코더†) — 부호어→"
                                                 "논리+syndrome0(accept), 오류 magic→syndrome≠0(거부). "
                                                 "증류 성공률·fidelity·후선택=관측(측정)"},
            "structure_integer": {"css_commutation": css_ok, "logical_pair_X7_Z3": logical_pair,
                                  "seeds_disjoint_key": seeds_ok},
            "encoder_symbolic_propagation": {"steane_selftest": st_self, "gates_38": len(gates) == 38,
                                             "stabilizers_14_and_logicals_plus_sign": enc_ok,
                                             "note": "봉인 spec 배선 파싱 — dense 미실체화"},
            "transversal_T": {"CX_weights_mod8_zero_coset_7": t_ok,
                              "logical_action": "T^⊗15 == 논리 T† (diag(1, ω₈⁻¹))"},
            "distance_exactly_3": d3_ok,
            "family": "code832(d=2, CCZ 횡단, 8q) → rm15(d=3, T 횡단, 15q) — triorthogonal 계보",
            "teeth": {"cnot_drop_propagation_fails": t1, "T_to_Tdg_breaks_uniform_phase": t2,
                      "fake_logical_rejected": t3},
            "honest_boundary": "봉인=인코더 tableau(Tier-2 module)·T-패턴(Tier-1)뿐. 논리 작용·거리="
                               "정수/심볼릭 witness(INV-Q3). 증류 성공률·후선택=범위 밖. dense 미실체화.",
            "ok": ok}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"_schema": "rm15-observe-v1",
                       "_note": "RM [[15,1,3]] + transversal T witness — 전부 정수/심볼릭(dense-free). "
                                "봉인=인코더·T-패턴뿐(INV-Q3).",
                       "observation": res}, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        e, t = res["encoder_symbolic_propagation"], res["teeth"]
        print("RM [[15,1,3]] witness 관측 (rm15_encoder_t2·rm15_tt):", flush=True)
        print(f"  seal {res['seal_links_module_app']} · 구조 정수 "
              f"{res['structure_integer']['css_commutation']}/{res['structure_integer']['logical_pair_X7_Z3']} · "
              f"인코더 역전파 {e['stabilizers_14_and_logicals_plus_sign']}(Steane 자가 {e['steane_selftest']})",
              flush=True)
        print(f"  ★T^15==논리 T† (mod-8 정수) {res['transversal_T']['CX_weights_mod8_zero_coset_7']} · "
              f"거리=3 {res['distance_exactly_3']}", flush=True)
        d = res["distillation_coherent_P1"]
        print(f"  ★P1 증류(coherent): 디코더 봉인 {d['decoder_sealed']}·==인코더† {d['decoder_eq_encoder_dag']}·"
              f"syndrome 추출 {d['syndrome_extraction_exposes_ancilla']}·weight-1 거부 "
              f"{d['weight1_error_rejected_syndrome_nonzero']}", flush=True)
        print(f"  teeth: CNOT누락/T→T†/가짜논리 {t['cnot_drop_propagation_fails']}/"
              f"{t['T_to_Tdg_breaks_uniform_phase']}/{t['fake_logical_rejected']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"rm15_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
