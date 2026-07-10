#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fib_braid_observe — TrackGate6 G5: Fibonacci anyon braid witness (신규 봉인 0).

봉인된 fib_braid_s1/s2(σ₁=R·σ₂=FRF, 1q B₃ 표현, 승인분 module z5_gate/ry_fib)에 대해:
  1. seal 링크: 앱 2 + module 2(z5_gate·ry_fib) 전부.
  2. ★독립 재구성: anyon 데이터(topological spin e^{−4πi/5}·e^{3πi/5}, 황금비 φ)에서 R/F 재구성
     → F²=I·F=F†·app golden == R·FRF exact (정의 직접 — 회로 독립).
  3. ★Yang-Baxter: σ₁σ₂σ₁ == σ₂σ₁σ₂ exact — braid 군 관계.
  4. ★B₃ 중심: (σ₁σ₂)³ = e^{2πi/5}·I exact (전역위상 포함 — 정의행렬 관측 소관).
  5. ★재발견: (z5_gate)⁵ == z_gate golden exact (Z 의 5제곱근 단언) + plan word 환원
     (z5⁷ ≅ σ₁ · [z,ry_fib]z5⁷[z,ry_fib] ≅ σ₂, up-to-phase) — honest 분해 링크.
  6. ★비-Clifford witness: 1q Clifford 24 대비 max mod-phase overlap σ₁ 0.9877·σ₂ 0.9715 < 1
     (Ising braid=Clifford 한계와 대조 — 위상적 보편성의 원천, 주장은 범위 밖).
  7. teeth: R 위상 오염(0.9배) → Yang-Baxter 잔차·중심 위상 이탈 검출.

정직 경계(INV-Q3, seal 아님, root 성장은 module 2+앱 2 봉인분뿐):
  - 봉인 = braid 생성원 유니터리 2개뿐. YB·중심·비-Clifford = witness 관측.
  - universality(braid 조밀성)·근사 컴파일(Solovay-Kitaev류)·n≥4 anyon = 범위 밖(차기).
  - field ℚ(ζ₅,√φ) 차수 8 = 승인분(.pgf/approvals/G5-fibonacci.md). 기존 braid_observe(Ising) 불변.

사용: python -m qf_witness.observe.fib_braid_observe [--quick]
"""
import os, sys, re, json
import numpy as np

from qf_witness.core.paths import ROOT
OUT = os.path.join(ROOT, ".pgf", "proofs", "FIB-BRAID-OBSERVE.json")


def load_golden(kind, name):
    src = open(os.path.join(ROOT, "specs", kind, name), encoding="utf-8").read()
    tag = "app_golden" if kind == "apps" else "golden"
    ns = {}
    exec(re.search(rf"```python id={tag}\n(.*?)```", src, re.S).group(1), ns)
    return ns["golden"]


def seal_link(store, sid):
    p = os.path.join(ROOT, "registry", store, f"{sid}.sealed.json")
    return os.path.exists(p) and bool(json.load(open(p, encoding="utf-8")).get("u_hash"))


def uptophase(A, B, tol=1e-12):
    i = np.unravel_index(np.argmax(np.abs(B)), B.shape)
    ph = A[i] / B[i]
    return bool(abs(abs(ph) - 1) < tol and np.allclose(A, ph * B, atol=tol))


def cliff24():
    H1 = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    S1 = np.diag([1, 1j]).astype(complex)
    def canon(U, tol=1e-9):
        f = U.flatten(); i = np.argmax(np.abs(f) > tol)
        return tuple(np.round(f * (np.conj(f[i]) / np.abs(f[i])), 6).tolist())
    elems = {canon(np.eye(2)): np.eye(2, dtype=complex)}
    frontier = [np.eye(2, dtype=complex)]
    while frontier:
        nxt = []
        for U in frontier:
            for G in (H1, S1):
                U2 = G @ U; k = canon(U2)
                if k not in elems:
                    elems[k] = U2; nxt.append(U2)
        frontier = nxt
    return list(elems.values())


def yb_residual(s1, s2):
    return float(np.abs(s1 @ s2 @ s1 - s2 @ s1 @ s2).max())


def observe():
    # 1. seal 링크
    seal_ok = (seal_link("apps", "fib_braid_s1") and seal_link("apps", "fib_braid_s2")
               and seal_link("modules", "z5_gate") and seal_link("modules", "ry_fib"))
    s1 = load_golden("apps", "fib_braid_s1.app.pg")
    s2 = load_golden("apps", "fib_braid_s2.app.pg")

    # 2. 독립 재구성 (anyon 데이터 → R/F)
    phi = (1 + np.sqrt(5)) / 2
    R = np.diag([np.exp(-4j * np.pi / 5), np.exp(3j * np.pi / 5)]).astype(complex)
    F = np.array([[1/phi, 1/np.sqrt(phi)], [1/np.sqrt(phi), -1/phi]], dtype=complex)
    f_ok = bool(np.allclose(F @ F, np.eye(2), atol=1e-14) and np.allclose(F, F.conj().T, atol=1e-14))
    recon_ok = bool(np.allclose(s1, R, atol=1e-13) and np.allclose(s2, F @ R @ F, atol=1e-13))

    # 3-4. Yang-Baxter + B₃ 중심
    yb = yb_residual(s1, s2)
    yb_ok = bool(yb < 1e-12)
    C = np.linalg.matrix_power(s1 @ s2, 3)
    center_dev = float(np.abs(C - np.exp(2j * np.pi / 5) * np.eye(2)).max())
    center_ok = bool(center_dev < 1e-12)

    # 5. 재발견 + plan word 환원 (module golden 경유 — honest 분해 링크)
    z5 = load_golden("modules", "z5_gate.pg")
    ryf = load_golden("modules", "ry_fib.pg")
    zg = load_golden("modules", "z_gate.pg")
    z5_5_ok = bool(np.allclose(np.linalg.matrix_power(z5, 5), zg, atol=1e-13))
    w1 = np.linalg.matrix_power(z5, 7)
    Fw = ryf @ zg
    word_ok = bool(uptophase(s1, w1) and uptophase(s2, Fw @ w1 @ Fw))

    # 6. 비-Clifford witness
    cl = cliff24()
    d1 = float(max(abs(np.trace(Cf.conj().T @ s1)) / 2 for Cf in cl))
    d2 = float(max(abs(np.trace(Cf.conj().T @ s2)) / 2 for Cf in cl))
    noncliff_ok = bool(d1 < 1 - 1e-6 and d2 < 1 - 1e-6)

    # 7. teeth: R 위상 0.9배 오염 → YB 잔차 + 중심 이탈
    Rbad = np.diag([np.exp(-4j * np.pi / 5 * 0.9), np.exp(3j * np.pi / 5 * 0.9)]).astype(complex)
    s2bad = F @ Rbad @ F
    yb_bad = yb_residual(Rbad, s2bad)
    Cbad = np.linalg.matrix_power(Rbad @ s2bad, 3)
    center_bad = float(np.abs(Cbad - np.exp(2j * np.pi / 5) * np.eye(2)).max())
    teeth_ok = bool(yb_bad > 1e-3 and center_bad > 1e-3)

    ok = bool(seal_ok and f_ok and recon_ok and yb_ok and center_ok and z5_5_ok
              and word_ok and noncliff_ok and teeth_ok)
    return {"axis": "Fibonacci anyon braid (첫 비-Clifford anyon braid — Ising=Clifford 한계와 대조)",
            "seal_links_2apps_2modules": seal_ok,
            "reconstruction": {"F_selfinv_hermitian": f_ok, "sigma_eq_R_FRF": recon_ok},
            "braid_relations": {"yang_baxter_residual": yb, "ok": yb_ok,
                                "b3_center_e2pi5_dev": center_dev, "center_ok": center_ok},
            "rediscovery": {"z5_pow5_eq_z_gate": z5_5_ok,
                            "plan_words_uptophase": word_ok},
            "nonclifford": {"cliff24_overlap_s1": d1, "cliff24_overlap_s2": d2, "ok": noncliff_ok},
            "teeth": {"r_corrupt_yb_residual": yb_bad, "r_corrupt_center_dev": center_bad,
                      "detects": teeth_ok},
            "field": "ℚ(ζ₅,√φ) ℚ위 차수 8 (승인분 .pgf/approvals/G5-fibonacci.md)",
            "honest_boundary": "봉인=braid 생성원 유니터리 2개뿐. YB·중심·비-Clifford=관측(INV-Q3). "
                               "universality·근사 컴파일·n≥4 anyon=범위 밖. braid_observe(Ising) 불변.",
            "ok": ok}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump({"_schema": "fib-braid-observe-v1",
                       "_note": "Fibonacci braid witness: YB+B₃중심+재발견+비-Clifford+teeth. "
                                "봉인=유니터리뿐(INV-Q3).",
                       "observation": res}, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        b, n, t = res["braid_relations"], res["nonclifford"], res["teeth"]
        print("Fibonacci anyon braid witness 관측 (fib_braid_s1/s2):", flush=True)
        print(f"  seal(2앱+2module) {res['seal_links_2apps_2modules']} · 재구성(R/FRF) "
              f"{res['reconstruction']['sigma_eq_R_FRF']} · F²=I {res['reconstruction']['F_selfinv_hermitian']}",
              flush=True)
        print(f"  Yang-Baxter 잔차 {b['yang_baxter_residual']:.1e} · B₃ 중심 e^(2πi/5)I dev "
              f"{b['b3_center_e2pi5_dev']:.1e}", flush=True)
        print(f"  재발견 z5⁵==z_gate {res['rediscovery']['z5_pow5_eq_z_gate']} · plan word 환원 "
              f"{res['rediscovery']['plan_words_uptophase']}", flush=True)
        print(f"  비-Clifford: overlap {n['cliff24_overlap_s1']:.4f}/{n['cliff24_overlap_s2']:.4f} <1 {n['ok']}",
              flush=True)
        print(f"  teeth: R오염 YB {t['r_corrupt_yb_residual']:.3f}·중심 {t['r_corrupt_center_dev']:.3f} "
              f"→ 검출 {t['detects']}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"fib_braid_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
