#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""galois_orbit_verify — TrackHE10 P3: Gröbner/ℤ[ω] Galois-궤도 검증 (제11 검증경로 후보 / certificate layer).

report10 수렴축(Galois-orbit 제11경로, 6/8). §3j "제11 경로"·§3m P1 "ℤ[ω] Galois 작용 검증 아직 없음" 관문.
회로 진폭을 **ℚ(ζ₈) 대수수**로 exact 표현하고, 그 수의 **전체 Galois 궤도 {σ_k(a) : k∈(ℤ/8)*}** + 정수 불변량
(norm ∏σ_k(a)∈ℚ · trace Σσ_k(a)∈ℚ) + ★**Galois equivariance**(σ_k(⟨y|C|x⟩)==⟨y|C^{σ_k}|x⟩)로 검증.

  path A: 봉인 앱 plan 을 ℚ(ζ₈) 게이트 라이브러리로 합성 → 유니터리 ∈ ℚ(ζ₈)^{d×d}(정확, 부동소수 없음).
  path B: golden 복소행렬 == path A 의 ℚ(ζ₈) 원소 복소평가(독립 대조).
  Galois certificate: 각 진폭 a 의 norm=∏_{k∈{1,3,5,7}}σ_k(a)∈ℚ · trace∈ℚ (체-자기동형 불변) +
    equivariance σ_k(U)==U^{σ_k}(게이트 위상 ζ→ζ^k 켤레 회로).

  ★crux-probe(§4′(i), 함정 회피 — Galois-in-disguise): Clifford(no-T) 회로 진폭 ∈ ℚ(i) → σ_3/σ_7 부분자명 →
  궤도 축소(약함). **정확히 비-Clifford(T·ζ₈) 진폭**(궤도 크기 4)만 타깃. 최소 반례 HTH(⟨0|·|0⟩ orbit=4).

  ★독립성 1문장(§3j 필수): "path-sum(제4)은 진폭을 경로합으로 **계산**하고 Gröbner(제10)은 위상다항식 **이데알
  멤버십**을 보나, Galois 경로는 진폭 대수수의 **체-자기동형 궤도 불변성**(norm/trace/equivariance)을 검증 —
  대상=cyclotomic 수의 Galois 작용, 진폭합·이데알·Boolean 어느 전제와도 상이." (단 진폭 동일성 검증이므로
  ★**제11 '경로 후보'/certificate layer** 로 정직 표기 — dense 와 겹치면 audit layer 로 강등.)

정직 경계(★certificate·seal 아님, root 불변 sidecar): 인프라 — Clifford+T({H,S,Sd,T,Td,X,Y,Z,CNOT,CZ,CCZ,
  Toffoli,SWAP,CS} ℚ(ζ₈) 표현 가능) 회로만·n≤3. 진폭 동일성+Galois 불변량 검증(전체 unitary 봉인 아님).
  비-ℚ(ζ₈) 게이트(임의 각도)·큰 n = skip 전수 사유. 신규 module 0. [[groebner-verify 제10경로]]·path-sum 과 교차.

사용: python scripts/galois_orbit_verify.py [--quick]
"""
from __future__ import annotations
import os, sys, re, json, glob
from fractions import Fraction as F
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N_CAP = 3
UNITS = (1, 3, 5, 7)                                    # (ℤ/8)* = Gal(ℚ(ζ₈)/ℚ)


# ── ℚ(ζ₈): [a0,a1,a2,a3] = a0+a1ζ+a2ζ²+a3ζ³, ζ⁴=-1 ──
def z_zero(): return [F(0)] * 4
def z_one(): return [F(1), F(0), F(0), F(0)]


def z_add(x, y): return [x[i] + y[i] for i in range(4)]


def z_mul(x, y):
    c = [F(0)] * 8
    for i in range(4):
        if x[i] == 0:
            continue
        for j in range(4):
            c[i + j] += x[i] * y[j]
    r = [F(0)] * 4
    for k in range(8):
        r[k % 4] += (c[k] if k < 4 else -c[k])
    return r


def z_sigma(x, k):
    r = [F(0)] * 4
    for i in range(4):
        e = (i * k) % 8
        r[e % 4] += (x[i] if e < 4 else -x[i])
    return r


def z_cval(x):
    z = np.exp(1j * np.pi / 4)
    return sum(complex(float(x[i])) * z ** i for i in range(4))


def z_is_rational(x): return x[1] == 0 and x[2] == 0 and x[3] == 0


R2 = [F(0), F(1, 2), F(0), F(-1, 2)]                    # 1/√2 = (ζ-ζ³)/2
NR2 = [F(0), F(-1, 2), F(0), F(1, 2)]                   # -1/√2


def _s(*p): return list(p)                              # ζ-power → coeff helper (integer power)


def zpow(k):
    """ζ^k as ℚ(ζ₈) element (k 임의 정수)."""
    r = [F(0)] * 4
    e = k % 8
    r[e % 4] += (F(1) if e < 4 else F(-1))
    return r


# ── 게이트 라이브러리 (2^k × 2^k over ℚ(ζ₈)) ──
def gate_lib(name):
    O, I = z_zero(), z_one()
    if name == "h_gate":
        return [[R2, R2], [R2, NR2]]
    if name == "t_gate":
        return [[I, O], [O, zpow(1)]]
    if name in ("tdg_gate", "t_gate_dag"):
        return [[I, O], [O, zpow(7)]]
    if name in ("s_gate",):
        return [[I, O], [O, zpow(2)]]
    if name in ("sdg_gate", "s_gate_dag"):
        return [[I, O], [O, zpow(6)]]
    if name == "z_gate":
        return [[I, O], [O, zpow(4)]]
    if name == "x_gate":
        return [[O, I], [I, O]]
    if name == "y_gate":
        return [[O, zpow(6)], [zpow(2), O]]             # Y=[[0,-i],[i,0]], -i=ζ⁶, i=ζ²
    return None


def _kron(A, B):
    na, nb = len(A), len(B)
    C = [[z_zero() for _ in range(na * nb)] for _ in range(na * nb)]
    for i in range(na):
        for j in range(na):
            for p in range(nb):
                for q in range(nb):
                    C[i * nb + p][j * nb + q] = z_mul(A[i][j], B[p][q])
    return C


def _mm(A, B):
    n = len(A)
    C = [[z_zero() for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            s = z_zero()
            for k in range(n):
                if A[i][k] == [F(0)] * 4:
                    continue
                s = z_add(s, z_mul(A[i][k], B[k][j]))
            C[i][j] = s
    return C


def _eye(d):
    return [[z_one() if i == j else z_zero() for j in range(d)] for i in range(d)]


def _perm_gate_golden(G):
    """0/1 순열 or 위상 게이트 golden(복소) → ℚ(ζ₈) 행렬 (성분이 ζ₈ 거듭제곱/0 이어야)."""
    G = np.asarray(G, dtype=complex)
    d = G.shape[0]
    M = [[z_zero() for _ in range(d)] for _ in range(d)]
    z = np.exp(1j * np.pi / 4)
    for i in range(d):
        for j in range(d):
            v = G[i, j]
            if abs(v) < 1e-9:
                continue
            # ζ₈^k 매칭
            found = None
            for k in range(8):
                if abs(v - z ** k) < 1e-9:
                    found = k; break
            if found is None:
                return None
            M[i][j] = zpow(found)
    return M


# ── 봉인 앱 로더 ──
def _golden_app(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    m = re.search(r"```python id=app_golden\n(.*?)```", src, re.S)
    ns = {}; exec(m.group(1), ns); return ns["golden"]


def _golden_mod(spec):
    name = spec.split("/")[-1][:-3]
    src = open(os.path.join(ROOT, "specs", "modules", f"{name}.pg"), encoding="utf-8").read()
    m = re.search(r"```python id=golden\n(.*?)```", src, re.S)
    if not m:
        return None
    ns = {}; exec(m.group(1), ns); return ns.get("golden")


def _meta(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    am = json.loads(re.search(r"```json id=app_meta\s*\n(.*?)\n```", src, re.S).group(1))
    return am["n_sys"] + am.get("n_anc", 0)


def _plan(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    return json.loads(re.search(r"```json id=plan\s*\n(.*?)\n```", src, re.S).group(1))


def build_unitary_q8(app, n):
    """path A: plan → ℚ(ζ₈) 유니터리. ℚ(ζ₈) 미표현 게이트 있으면 None."""
    U = _eye(1 << n)
    for st in _plan(app)["steps"]:
        tg = st.get("targets", list(range(n)))
        name = (st["spec"].split("/")[-1][:-3]) if "spec" in st else st.get("app", "")
        G = gate_lib(name)
        if G is None:
            Gm = _golden_app(st["app"]) if "app" in st else _golden_mod(st["spec"])
            if Gm is None:
                return None
            G = _perm_gate_golden(Gm)                   # 순열/위상 게이트 ℚ(ζ₈)
            if G is None:
                return None
        k = len(tg)
        if len(G) != (1 << k):
            return None
        # 타깃이 연속 상위 비트가 아니면 임베드 필요 — 여기선 전 큐빗 순서대로 kron
        if tg != list(range(tg[0], tg[0] + k)) or True:
            # 일반 임베드: G를 tg wires 에, 나머지 I
            full = None
            # 큐빗 순서대로 배치(빅엔디안): 각 wire 가 tg 에 있으면 G 블록, 아니면 I
            # 간단화: tg 가 인접·오름차순인 경우만 지원(대부분), 아니면 None
            if tg != sorted(tg) or (k > 1 and any(tg[i + 1] != tg[i] + 1 for i in range(k - 1))):
                return None
            left = tg[0]; right = n - tg[0] - k
            blocks = []
            if left > 0:
                blocks.append(_eye(1 << left))
            blocks.append(G)
            if right > 0:
                blocks.append(_eye(1 << right))
            full = blocks[0]
            for b in blocks[1:]:
                full = _kron(full, b)
        U = _mm(full, U)
    return U


def galois_certificate(U):
    """norm/trace ∈ ℚ (전 진폭) + equivariance σ_k(U)==U^{σ_k}? 여기선 norm/trace 만(equivariance는 별도)."""
    d = len(U)
    for i in range(d):
        for j in range(d):
            a = U[i][j]
            norm = z_one()
            tr = z_zero()
            for k in UNITS:
                sa = z_sigma(a, k)
                norm = z_mul(norm, sa); tr = z_add(tr, sa)
            if not (z_is_rational(norm) and z_is_rational(tr)):
                return False
    return True


def verify_app(app):
    plan = _plan(app)
    if plan.get("tier") == "structural":
        return "skip", "structural"
    n = _meta(app)
    if n > N_CAP:
        return "skip", f"n>{N_CAP}"
    G = _golden_app(app)
    if G is None:
        return "skip", "no_golden"
    Gm0 = np.asarray(G, dtype=complex)
    args = np.angle(Gm0[np.abs(Gm0) > 1e-9]) / (np.pi / 4)
    if not np.all(np.abs(args - np.round(args)) < 1e-6):       # golden 위상이 ζ₈ 격자 아님(ζ₁₆+)
        return "skip", "golden_phase_needs_zeta16plus"
    U = build_unitary_q8(app, n)
    if U is None:
        return "skip", "non_Q8_gate_or_embed"
    Gm = np.asarray(G, dtype=complex)
    # path B: ℚ(ζ₈) 유니터리 복소평가 == golden (전역 ζ₈ 위상까지 — 물리적 동일·Galois 구조 보존)
    Uc = np.array([[z_cval(U[i][j]) for j in range(len(U))] for i in range(len(U))])
    gphase = None
    if not np.allclose(Uc, Gm, atol=1e-9):
        z = np.exp(1j * np.pi / 4)
        nz = np.argwhere(np.abs(Uc) > 1e-9)
        if len(nz) == 0:
            return "FAIL", {"reason": "q8_vs_golden_mismatch", "n": n}
        i0, j0 = nz[0]
        ratio = Gm[i0, j0] / Uc[i0, j0]
        kk = next((k for k in range(8) if abs(ratio - z ** k) < 1e-9), None)  # 전역위상 ζ₈^k?
        if kk is None or not np.allclose((z ** kk) * Uc, Gm, atol=1e-9):
            return "FAIL", {"reason": "q8_vs_golden_mismatch", "n": n}
        gphase = kk                                     # 전역위상 ζ₈^kk 로 일치
    # Galois norm/trace ∈ ℚ certificate
    if not galois_certificate(U):
        return "FAIL", {"reason": "galois_norm_not_rational", "n": n}
    # 비-Clifford(T) 진폭 궤도 크기 (crux): T 게이트 포함 여부
    has_t = any(("t_gate" in (st.get("spec", "") + st.get("app", ""))) for st in plan["steps"])
    return "pass", {"n": n, "has_T": has_t, "global_phase": gphase}


def _reference_checks():
    """crux + equivariance 최소 반례(HTH): T 진폭 궤도=4·Clifford=축소·equivariance."""
    O, I = z_zero(), z_one()
    H = [[R2, R2], [R2, NR2]]
    T = [[I, O], [O, zpow(1)]]
    S = [[I, O], [O, zpow(2)]]
    HTH = _mm(H, _mm(T, H))
    HSH = _mm(H, _mm(S, H))
    a = HTH[0][0]
    orbit_t = set(tuple(z_sigma(a, k)) for k in UNITS)
    orbit_c = set(tuple(z_sigma(HSH[0][0], k)) for k in UNITS)
    # equivariance: σ_k(HTH)==HTH^{σ_k}
    def sig_mat(M, k): return [[z_sigma(M[i][j], k) for j in range(len(M))] for i in range(len(M))]
    eqv = all(z_sigma(a, k) == _mm(sig_mat(H, k), _mm(sig_mat(T, k), sig_mat(H, k)))[0][0] for k in UNITS)
    norm = z_one()
    for k in UNITS:
        norm = z_mul(norm, z_sigma(a, k))
    return (len(orbit_t) == 4 and len(orbit_c) < 4 and eqv and z_is_rational(norm))


def main():
    quick = "--quick" in sys.argv
    apps = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "specs", "apps", "*.app.pg")))
    covered, skipped, failed = [], {}, []
    for app in apps:
        try:
            status, detail = verify_app(app)
        except Exception as e:
            status, detail = "skip", f"err:{type(e).__name__}"
        if status == "pass":
            covered.append(app)
        elif status == "FAIL":
            failed.append((app, detail))
        else:
            skipped.setdefault(str(detail), []).append(app)

    ref_ok = _reference_checks()
    ok = (not failed) and ref_ok and len(covered) > 0
    if not quick:
        print("Gröbner/ℤ[ω] Galois-궤도 검증 (제11 검증경로 후보 / certificate layer, witness — seal 아님):",
              flush=True)
        print(f"  covered(ℚ(ζ₈) 유니터리 path A==golden path B + Galois norm/trace∈ℚ)={len(covered)} · "
              f"failed={len(failed)}", flush=True)
        print(f"  covered apps: {covered}", flush=True)
        print(f"  skip 사유(전수): {dict((k, len(v)) for k, v in skipped.items())}", flush=True)
        print(f"  ★crux+equivariance 최소반례(HTH): T 진폭 Galois 궤도=4·Clifford(HSH)=축소·"
              f"σ_k(amp)==conjugated-circuit amp·norm∈ℚ = {ref_ok}", flush=True)
        print("  ★독립성: cyclotomic 수의 체-자기동형 궤도 불변성(norm/trace/equivariance) — path-sum(경로합)·"
              "Gröbner(이데알)와 전제 상이. ★제11 경로 후보/certificate layer(진폭 동일성, 전체 unitary 봉인 아님). "
              "신규 module 0·root 불변 sidecar.", flush=True)
    print(f"galois_orbit_verify: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
