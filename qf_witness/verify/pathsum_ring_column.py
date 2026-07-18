#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pathsum_ring_column — TrackHE14 P6b: pathsum ℤ[ζ_{2^t}] ring-exact 컬럼 증인 확장
(관측·sidecar, seal 아님·root 불변).

기존 [[pathsum_verify]](제4경로, ℤ[ω₈] exact 경로합)의 두 약점을 상향한다:
  1. **환 확장** ℤ[ω₈]→ℤ[ζ_{2^t}] (t≤8, 단일 환 ℤ[ζ₂₅₆], 벡터 128 정수): QFT 가족의
     controlled-phase 사다리(cs·ct·cr4..cr8 및 dag = ζ_{2^k}^{±1})를 exact 로 포괄 —
     기존 Clifford+T-닫힘 한계를 넘어 qft5~8·iqft7/8 pipeline 커버.
  2. **대조의 ring-exact 상향**: 기존 최종 대조는 dense golden float(1e-12 atol) — 여기서는
     plan-구동 축차 경로합(ℤ[ζ₂₅₆], √2 전역미룸 — #H 지수)과 **분석식 ring golden**
     (QFT_n[x][j]=ζ_{2^n}^{x·j}/√2^n · iqft=켤레 — 규약은 sealed golden 과 float 사전확정)을
     **정수 벡터 등식(float 0)** 으로 대조. [[ring_column_witness]](iQFT ℤ[ζ256]) 패턴의
     pathsum 판.
  3. ★P6a 바인딩: gridsynth rz_*_ct 5앱 — plan-구동 컬럼 vs gridsynth_family ring shadow
     행렬(ℤ[ω₈]→ℤ[ζ₂₅₆] 임베드, ω₈=ζ₂₅₆³²) 정수 등식. 봉인앱·ε-인증·컬럼증인 3자 일관.

스코프(정직 명시): qft5(32 전수)·qft6(64 전수)·qft7/qft8/iqft7/iqft8(각 표본 16, 결정론
  스트라이드)·rz gridsynth 10앱=_ct 5+_rs 5(전수 2컬럼). 표본 앱은 전수 아님을 결과에 표기.

정직 경계: **기존 경로 강화 — 신규 독립 검증경로(제11) 주장 아님**. 봉인 판정 불참(sidecar
  witness)·oracle 무접촉·root 불변·신규 module 0. 경로합=exact 정수(부동소수 0), float 는
  규약 확정(사전 dev)과 무관 — 본 스크립트 실행 경로에 float 대조 없음(전 등식 정수).
teeth: (i) 분석식 지수 오염 → 불일치 검출 (ii) plan 스텝 제거 → 불일치 검출
  (iii) rz ring shadow 성분 오염 → 불일치 검출.

사용: python -m qf_witness.verify.pathsum_ring_column [--quick]
"""
from __future__ import annotations
import os
import re
import sys
import json

from qf_witness.core.paths import ROOT
from qf_witness.family.gridsynth_family import ALL_SEQS as RZ_SEQS, ring_shadow

OUT = os.path.join(ROOT, ".pgf", "proofs", "PATHSUM-RING-COLUMN.json")
SPECS_APPS = os.path.join(ROOT, "specs", "apps")

D = 128                     # ℤ[ζ₂₅₆]: 벡터 길이 (ζ^128 = −1)

# 게이트명 → ζ₂₅₆ 지수 (controlled-phase, 대각 — control/target 대칭)
PHASE = {"cs_gate": 64, "ct_gate": 32, "cr4_gate": 16, "cr5_gate": 8,
         "cr6_gate": 4, "cr7_gate": 2, "cr8_gate": 1,
         "cs_dag": -64, "cr3_dag_gate": -32, "cr4_dag_gate": -16, "cr5_dag_gate": -8,
         "cr6_dag_gate": -4, "cr7_dag_gate": -2, "cr8_dag_gate": -1}


# ── ℤ[ζ₂₅₆] 정수 벡터 산술 (부동소수 0) ─────────────────────────────────────
ZVEC = tuple([0] * D)


def unit(p):
    """ζ^p (p 임의 정수) → 128-벡터."""
    p %= 256
    s = 1
    if p >= D:
        p -= D; s = -1
    v = [0] * D
    v[p] = s
    return tuple(v)


def vrot(v, p):
    """v · ζ^p — 회전(+부호)."""
    p %= 256
    s = 1
    if p >= D:
        p -= D; s = -1
    if p == 0:
        return tuple(s * x for x in v) if s < 0 else v
    return tuple([-s * x for x in v[D - p:]] + [s * x for x in v[:D - p]])


def vadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def vneg(a):
    return tuple(-x for x in a)


# ── plan 로더 ──────────────────────────────────────────────────────────────
def load_plan(app):
    src = open(os.path.join(SPECS_APPS, f"{app}.app.pg"), encoding="utf-8").read()
    meta = json.loads(re.search(r"```json id=app_meta\n(.*?)```", src, re.S).group(1))
    plan = json.loads(re.search(r"```json id=plan\n(.*?)```", src, re.S).group(1))
    return meta["n_sys"], plan["steps"]


def sim_column(n, steps, j):
    """plan-구동 exact 경로합: 컬럼 j (qubit 0=MSB). 반환 (state dict x→벡터, m=#H)."""
    state = {j: unit(0)}
    m = 0
    for st in steps:
        name = st["spec"].split("/")[-1].replace(".pg", "")
        tg = st.get("targets", [0])
        if name == "h_gate":
            m += 1
            q = tg[0]; mask = 1 << (n - 1 - q)
            ns: dict = {}
            for x, a in state.items():
                x0, x1 = x & ~mask, x | mask
                a1 = vneg(a) if (x & mask) else a
                ns[x0] = vadd(ns[x0], a) if x0 in ns else a
                ns[x1] = vadd(ns[x1], a1) if x1 in ns else a1
            state = ns
        elif name == "t_gate":
            q = tg[0]; mask = 1 << (n - 1 - q)
            state = {x: (vrot(a, 32) if (x & mask) else a) for x, a in state.items()}
        elif name == "swap2":
            q1, q2 = tg
            m1, m2 = 1 << (n - 1 - q1), 1 << (n - 1 - q2)
            ns = {}
            for x, a in state.items():
                y = x & ~(m1 | m2)
                if x & m1:
                    y |= m2
                if x & m2:
                    y |= m1
                ns[y] = a
            state = ns
        elif name in PHASE:
            q1, q2 = tg
            m1, m2 = 1 << (n - 1 - q1), 1 << (n - 1 - q2)
            p = PHASE[name]
            state = {x: (vrot(a, p) if (x & m1 and x & m2) else a)
                     for x, a in state.items()}
        else:
            raise ValueError(f"unsupported gate {name}")
    return state, m


# ── 분석식 ring golden ─────────────────────────────────────────────────────
def qft_analytic_entry(n, x, j, dag=False):
    """QFT_n[x][j] · √2^n = ζ_{2^n}^{x·j} (iqft: −x·j) — ℤ[ζ₂₅₆] 벡터."""
    e = (x * j) % (1 << n)
    if dag:
        e = -e
    return unit(e * (256 >> n))


def check_qft_app(app, n, dag, cols):
    n_file, steps = load_plan(app)
    assert n_file == n
    ok, checked = True, 0
    for j in cols:
        state, m = sim_column(n, steps, j)
        if m != n:                                     # √2 지수 = 분석식 √2^n 과 일치해야
            return False, checked
        for x in range(1 << n):
            want = qft_analytic_entry(n, x, j, dag)
            got = state.get(x, ZVEC)
            if tuple(got) != tuple(want):
                return False, checked
            checked += 1
    return ok, checked


# ── rz_ct 바인딩: plan-구동 컬럼 vs gridsynth ring shadow (ω₈=ζ₂₅₆³² 임베드) ──
def w8_embed(t4):
    """ℤ[ω₈] 4-튜플 → ℤ[ζ₂₅₆] 벡터."""
    v = ZVEC
    for i, c in enumerate(t4):
        if c:
            v = vadd(v, tuple(c * y for y in unit(32 * i)))
    return v


def check_rz_app(app_id):
    k, seq = RZ_SEQS[app_id]
    M, m_ref = ring_shadow(seq)                        # ℤ[ω₈] 2×2, √2^m_ref
    _, steps = load_plan(app_id)
    ok, checked = True, 0
    for j in (0, 1):
        state, m = sim_column(1, steps, j)
        if m != m_ref:
            return False, checked
        for x in (0, 1):
            want = w8_embed(M[x][j])
            got = state.get(x, ZVEC)
            if tuple(got) != tuple(want):
                return False, checked
            checked += 1
    return ok, checked


# ── teeth ──────────────────────────────────────────────────────────────────
def teeth():
    out = {}
    # (i) 분석식 지수 오염: qft5 col 1 에서 x=3 지수 +1 → 불일치여야
    n = 5
    _, steps = load_plan("qft5_pipeline")
    state, m = sim_column(n, steps, 1)
    bad = vrot(qft_analytic_entry(n, 3, 1), 256 >> n)  # 지수 j·x → j·x+1 오염
    out["analytic_tamper_detected"] = (m == n and tuple(state.get(3, ZVEC)) != tuple(bad))
    # (ii) plan 스텝 제거 → 전수 대조 실패여야
    _, steps_full = load_plan("qft5_pipeline")
    steps_cut = steps_full[:-1]
    state_cut, m_cut = sim_column(n, steps_cut, 1)
    mismatch = (m_cut != n) or any(
        tuple(state_cut.get(x, ZVEC)) != tuple(qft_analytic_entry(n, x, 1))
        for x in range(1 << n))
    out["plan_tamper_detected"] = bool(mismatch)
    # (iii) rz shadow 성분 오염 → 불일치여야
    k, seq = RZ_SEQS["rz_pi16_ct"]
    M, m_ref = ring_shadow(seq)
    _, steps_rz = load_plan("rz_pi16_ct")
    state_rz, m_rz = sim_column(1, steps_rz, 0)
    bad00 = w8_embed(tuple(c + (1 if i == 0 else 0) for i, c in enumerate(M[0][0])))
    out["shadow_tamper_detected"] = (m_rz == m_ref
                                     and tuple(state_rz.get(0, ZVEC)) != tuple(bad00))
    return out


def main():
    quick = "--quick" in sys.argv
    stride16 = lambda n: list(range(0, 1 << n, (1 << n) // 16))    # noqa: E731
    if quick:
        targets = [("qft5_pipeline", 5, False, list(range(32)), "exhaustive"),
                   ("iqft8", 8, True, stride16(8)[:4], "sample4"),
                   ]
        rz_list = list(RZ_SEQS)
    else:
        targets = [("qft5_pipeline", 5, False, list(range(32)), "exhaustive"),
                   ("qft6_pipeline", 6, False, list(range(64)), "exhaustive"),
                   ("qft7_pipeline", 7, False, stride16(7), "sample16"),
                   ("qft8_pipeline", 8, False, stride16(8), "sample16"),
                   ("iqft7", 7, True, stride16(7), "sample16"),
                   ("iqft8", 8, True, stride16(8), "sample16"),
                   ]
        rz_list = list(RZ_SEQS)

    res, all_ok = {}, True
    for app, n, dag, cols, scope in targets:
        ok, checked = check_qft_app(app, n, dag, cols)
        res[app] = {"ok": ok, "entries_exact": checked, "columns": len(cols),
                    "scope": scope, "ring": f"Z[zeta_{1 << n}] ⊂ Z[zeta256]"}
        all_ok &= ok
    for app_id in rz_list:
        ok, checked = check_rz_app(app_id)
        res[app_id] = {"ok": ok, "entries_exact": checked, "columns": 2,
                       "scope": "exhaustive", "ring": "Z[omega8] ⊂ Z[zeta256] (P6a shadow binding)"}
        all_ok &= ok

    th = teeth()
    all_ok &= all(th.values())

    out = {"_schema": "pathsum-ring-column/v1",
           "_note": ("pathsum 제4경로의 ring-exact 컬럼 상향(ℤ[ζ_{2^t}] t≤8·√2 전역미룸·정수 "
                     "등식 float 0) + QFT 가족 확장 + ★P6a gridsynth ring shadow 바인딩. "
                     "기존 경로 강화 — 신규 독립 검증경로(제11) 주장 아님. 관측 sidecar·"
                     "봉인 판정 불참·신규 module 0·root 불변. 표본 앱은 전수 아님 명시."),
           "results": res, "teeth": th, "all_ok": bool(all_ok)}

    if not quick:
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        for app, r in res.items():
            print(f"  {app:14} ok={r['ok']} entries={r['entries_exact']} ({r['scope']})", flush=True)
        print(f"  teeth: {th}", flush=True)
        print(f"  → .pgf/proofs/PATHSUM-RING-COLUMN.json", flush=True)
    print(f"pathsum_ring_column: all_ok={out['all_ok']}", flush=True)
    return 0 if out["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
