#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""code832_observe — TrackHE4-R2: [[8,3,2]] triorthogonal + transversal 논리 CCZ witness (신규 봉인 0).

봉인된 code832_encoder(정육면체 CSS 인코더)·code832_tccz(⊗T^{±1})에 대해:
  1. seal 링크 2 + 인코더 정의 열 8/8 == (|Ax⟩+|Ax⊕1⁸⟩)/√2 (F₂ 독립 구성 대조).
  2. ★triorthogonality 정수 witness: 논리 X̄ 면 f₁f₂f₃ 의 |fᵢ|·쌍·삼중 교집합 mod2 = (0,0,1)
     — 비-Clifford 횡단성의 대수적 필요조건(Bravyi-Haah)을 순수 정수 산술로.
  3. ★논리 작용: U_T·|x̄⟩ == (−1)^{x₁x₂x₃}·|x̄⟩ 전수 8/8 — 물리 T-패턴의 코드공간 사영 == 논리 CCZ.
     + 논리 행렬 M[x,y]=⟨x̄|U_T|ȳ⟩ == diag CCZ exact + 코드공간 사영자 보존 U_T·P·U_T† == P.
  4. ★거리-2: weight-1 X/Z 오류 전수 16 — 스태빌라이저 반교환(정수) + P·E|x̄⟩==0 (검출 전용, 정정 아님).
  5. CSS 정합: Z-stab(면 {a=0}/{b=0}/{c=0}·Z^⊗8) ⊥ X-stab(X^⊗8)·논리X — 짝 교차 전수.
  6. teeth: ①전부 T(부호 패턴 무시) → 논리 CCZ 실패 ②f₃ 정점 1개 제거 → triorthogonality 붕괴.

정직 경계(INV-Q3, seal 아님, root 성장은 앱 2 봉인분뿐):
  - 봉인 = 물리 유니터리 2개뿐. '논리 CCZ'·triorthogonality·거리 = witness 관측.
  - 거리-2 = 오류 **검출** 전용(정정 아님). magic 증류·FT threshold·d≥3 색부호 = 범위 밖.
  - ★제5 경로 소비: code832_tccz(T-count 8=256분기)·encoder(Clifford) 가 stabrank_verify 자동 커버.

사용: python -m qf_witness.observe.code832_observe [--quick]
"""
import os, sys, re, json
from itertools import product
import numpy as np

from qf_witness.core.paths import ROOT
OUT = os.path.join(ROOT, ".pgf", "proofs", "CODE832-OBSERVE.json")

F = [[v for v in range(8) if (v >> 2) & 1],
     [v for v in range(8) if (v >> 1) & 1],
     [v for v in range(8) if v & 1]]


def load_golden(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    ns = {}
    exec(re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1), ns)
    return ns["golden"]


def seal_link(sid):
    p = os.path.join(ROOT, "registry", "apps", f"{sid}.sealed.json")
    return os.path.exists(p) and bool(json.load(open(p, encoding="utf-8")).get("u_hash"))


def _mask(supp):
    m = 0
    for v in supp:
        m |= 1 << v
    return m


def _idx(word_vbits):
    """정점 점유 마스크(비트 v=정점 v) → 상태 인덱스(big-endian 큐빗 v=비트 7−v)."""
    idx = 0
    for q in range(8):
        idx = (idx << 1) | ((word_vbits >> q) & 1)
    return idx


def observe():
    links = seal_link("code832_encoder") and seal_link("code832_tccz")
    Ue = load_golden("code832_encoder.app.pg")
    Ut = load_golden("code832_tccz.app.pg")

    # 2. triorthogonality 정수 witness
    m = [_mask(f) for f in F]
    tri_vals = {"weights": [bin(x).count("1") for x in m],
                "pair": [bin(m[i] & m[j]).count("1") for i in range(3) for j in range(i + 1, 3)],
                "triple": bin(m[0] & m[1] & m[2]).count("1")}
    tri_ok = bool(all(w % 2 == 0 for w in tri_vals["weights"] + tri_vals["pair"])
                  and tri_vals["triple"] % 2 == 1)

    # 1+3. 인코더 정의열 + 논리 작용
    def Ax(x):
        r = 0
        for xi, mm in zip(x, m):
            if xi:
                r ^= mm
        return r
    enc_ok = logical_ok = True
    codewords = {}
    for x in product((0, 1), repeat=3):
        z_in = _idx((x[0] << 4) | (x[1] << 2) | (x[2] << 1))
        col = Ue[:, z_in]
        a = Ax(x)
        want = np.zeros(256, dtype=complex)
        want[_idx(a)] = want[_idx(a ^ 0xFF)] = 1 / np.sqrt(2)
        enc_ok &= bool(np.allclose(col, want, atol=1e-13))
        codewords[x] = col
        out = Ut @ col
        ph = (-1.0) ** (x[0] & x[1] & x[2])
        logical_ok &= bool(np.allclose(out, ph * col, atol=1e-13))
    # 논리 행렬 == CCZ + 사영자 보존
    M = np.zeros((8, 8), dtype=complex)
    P = np.zeros((256, 256), dtype=complex)
    for i, xi in enumerate(product((0, 1), repeat=3)):
        P += np.outer(codewords[xi], codewords[xi].conj())
        for j, xj in enumerate(product((0, 1), repeat=3)):
            M[i, j] = codewords[xi].conj() @ Ut @ codewords[xj]
    CCZ8 = np.diag([1] * 7 + [-1]).astype(complex)
    lmat_ok = bool(np.allclose(M, CCZ8, atol=1e-12))
    proj_ok = bool(np.allclose(Ut @ P @ Ut.conj().T, P, atol=1e-12))

    # 4+5. 거리-2 + CSS 정합 (정수) + 코드공간 이탈(행렬)
    ZS = [_mask([v for v in range(8) if not ((v >> 2) & 1)]),
          _mask([v for v in range(8) if not ((v >> 1) & 1)]),
          _mask([v for v in range(8) if not (v & 1)]), 0xFF]
    det_ok = all(any(bin((1 << v) & zs).count("1") % 2 == 1 for zs in ZS) for v in range(8)) \
        and all(bin((1 << v) & 0xFF).count("1") % 2 == 1 for v in range(8))
    css_ok = all(bin(zs & 0xFF).count("1") % 2 == 0 for zs in ZS) and \
        all(bin(zs & mm).count("1") % 2 == 0 for zs in ZS for mm in m)
    X1 = np.array([[0, 1], [1, 0]], dtype=complex)
    Z1 = np.diag([1, -1]).astype(complex)
    esc_ok = True
    for q in (0, 5):                                 # 표본 정점 2 × 오류 2종 (전수는 정수측이 담당)
        for E1 in (X1, Z1):
            E = np.eye(1, dtype=complex)
            for qq in range(8):
                E = np.kron(E, E1 if qq == q else np.eye(2))
            v = E @ codewords[(0, 0, 0)]
            esc_ok &= bool(np.abs(P @ v).max() < 1e-12)

    # 6. teeth
    w8 = np.exp(1j * np.pi / 4)
    d_bad = np.ones(256, dtype=complex)
    for idx in range(256):
        d_bad[idx] = w8 ** (bin(idx).count("1") % 8)          # 전부 T (부호 무시)
    Ubad = np.diag(d_bad)
    # 전부-T 는 |111̄⟩에선 우연히 −1 이 맞으므로(|Ax|=4 짝) x=(1,0,0)에서 검출: CCZ 는 +1 요구
    t1 = bool(not np.allclose(Ubad @ codewords[(1, 0, 0)],
                              codewords[(1, 0, 0)], atol=1e-6))
    m_bad = list(m)
    m_bad[2] ^= 1 << 7                                        # f₃에서 정점 7 제거
    t2 = bool(not (bin(m_bad[0] & m_bad[1] & m_bad[2]).count("1") % 2 == 1
                   and bin(m_bad[2]).count("1") % 2 == 0))
    teeth_ok = t1 and t2

    ok = bool(links and tri_ok and enc_ok and logical_ok and lmat_ok and proj_ok
              and det_ok and css_ok and esc_ok and teeth_ok)
    return {"code": "[[8,3,2]] triorthogonal 색부호(정육면체) — smallest interesting code",
            "seal_links_2": links,
            "triorthogonality_mod2": {**tri_vals, "condition_0_0_1": tri_ok},
            "encoder_def_cols_8of8": enc_ok,
            "transversal_logical_CCZ": {"phase_8of8": logical_ok,
                                        "logical_matrix_eq_CCZ": lmat_ok,
                                        "codespace_projector_preserved": proj_ok},
            "distance2": {"weight1_detected_16of16_integer": bool(det_ok),
                          "css_commutation": bool(css_ok),
                          "error_escapes_codespace_sample": bool(esc_ok),
                          "note": "검출 전용(d=2) — 정정 아님"},
            "teeth": {"all_T_pattern_fails_CCZ": t1, "f3_corrupt_breaks_triorth": t2},
            "fifth_path": "code832_tccz(256분기)·encoder = stabrank_verify 자동 커버(정본 proofs 참조)",
            "honest_boundary": "봉인=물리 유니터리 2뿐. 논리 CCZ·triorthogonality·거리=관측(INV-Q3). "
                               "magic 증류·FT threshold·d≥3=범위 밖.",
            "ok": ok}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"_schema": "code832-observe-v1",
                       "_note": "[[8,3,2]] triorthogonal + 첫 비-Clifford 횡단 논리 게이트 witness. "
                                "봉인=유니터리뿐(INV-Q3).",
                       "observation": res}, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        t = res["transversal_logical_CCZ"]
        print("[[8,3,2]] triorthogonal witness 관측 (code832_encoder·code832_tccz):", flush=True)
        print(f"  seal {res['seal_links_2']} · triorth(0,0,1) "
              f"{res['triorthogonality_mod2']['condition_0_0_1']} · 인코더 정의열 "
              f"{res['encoder_def_cols_8of8']}", flush=True)
        print(f"  ★논리 CCZ: 위상 8/8 {t['phase_8of8']} · 논리행렬==CCZ {t['logical_matrix_eq_CCZ']} · "
              f"사영자 보존 {t['codespace_projector_preserved']}", flush=True)
        print(f"  거리-2 검출 {res['distance2']['weight1_detected_16of16_integer']} · "
              f"teeth {res['teeth']['all_T_pattern_fails_CCZ']}/{res['teeth']['f3_corrupt_breaks_triorth']}",
              flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"code832_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
