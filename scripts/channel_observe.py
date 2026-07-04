#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""channel_observe — HE2 V6: CPTP 채널 Stinespring dilation 검증 witness (신규 봉인 0).

봉인된 dilation 유니터리(bitflip/phasedamp/ampdamp 2q + depol 3q)에 대해:
  1. ★독립 참조: E(ρ)=Tr_env[U(ρ⊗|0⟩⟨0|)U†] 가 목표 Kraus 채널 Σ K_k ρ K_k† 와 exact 일치
     (밀도행렬 기저 4원소 전수 — 선형사상이라 기저 일치=전체 일치). U 와 독립(Kraus 로 재구성).
  2. CPTP: trace preservation (Tr E(ρ)=Tr ρ) + Kraus completeness Σ K_k† K_k = I.
  3. teeth: 틀린 감쇠각(0.8·π/2) dilation 은 Kraus 채널과 불일치해야.
  4. ★compounding(합성 관측): 봉인 dilation 직렬연결 → 합성 채널의 Kraus 재구성 일치.
     phase-damp½∘½ == phase-damp(λ_eff=¾) · amp-damp½∘½ == amp-damp(γ_eff=¾). 봉인 자산 복리 실증.
  5. depol: 4-Kraus {½I,½X,½Y,½Z} 균일 Pauli twirl → E(ρ)=I/2(완전 망각) exact.

정직 경계(INV-Q3, seal 아님, root 불변):
  - 봉인 = dilation 유니터리(Tier-0 exact)뿐. 채널 E = 비유니터리 초연산자 → 관측(seal 아님).
  - 1/2 감쇠점만 dyadic-exact. 일반 감쇠율·depolarizing(3-Kraus)·다큐빗·noise 모델 합성 = 차기.
  - 하드웨어 노이즈 실측 아님(이상적 수학 채널). 신규 봉인 0.

사용: python scripts/channel_observe.py [--quick]
"""
import os, sys, re, json
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, ".pgf", "proofs", "CHANNEL-OBSERVE.json")

I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def load_golden(app):
    src = open(os.path.join(ROOT, "specs", "apps", app), encoding="utf-8").read()
    ns = {}
    exec(re.search(r"```python id=app_golden\n(.*?)```", src, re.S).group(1), ns)
    return ns["golden"]


def kraus(name):
    r2 = 1 / np.sqrt(2)
    if name == "bitflip":
        return [r2 * I, r2 * X]
    if name == "phasedamp":
        return [np.diag([1, r2]).astype(complex), np.diag([0, r2]).astype(complex)]
    if name == "ampdamp":
        return [np.diag([1, r2]).astype(complex), np.array([[0, r2], [0, 0]], dtype=complex)]
    if name == "depol":
        return [0.5 * I, 0.5 * X, 0.5 * Y, 0.5 * Z]
    raise ValueError(name)


def channel_from_unitary(U, n_env=1):
    """E(ρ)=Tr_env[U(ρ⊗|0..0⟩⟨0..0|_env)U†]. sys=q0(MSB), env=하위 n_env 큐빗."""
    dim = 2 ** (1 + n_env)
    env0 = np.zeros((2 ** n_env, 2 ** n_env), dtype=complex); env0[0, 0] = 1.0
    def E(rho):
        out = U @ np.kron(rho, env0) @ U.conj().T
        res = np.zeros((2, 2), dtype=complex)
        for ev in range(2 ** n_env):
            P = np.zeros((2, dim), dtype=complex)
            for s in range(2):
                P[s, (s << n_env) | ev] = 1.0
            res += P @ out @ P.conj().T
        return res
    return E


def channel_from_kraus(Ks):
    return lambda rho: sum(K @ rho @ K.conj().T for K in Ks)


_BASIS = [np.array([[1, 0], [0, 0]], dtype=complex), np.array([[0, 1], [0, 0]], dtype=complex),
          np.array([[0, 0], [1, 0]], dtype=complex), np.array([[0, 0], [0, 1]], dtype=complex)]


def verify_one(app_id, name, n_env=1):
    U = load_golden(f"{app_id}.app.pg")
    dim = 2 ** (1 + n_env)
    unitary = bool(np.allclose(U.conj().T @ U, np.eye(dim), atol=1e-9))
    Edil = channel_from_unitary(U, n_env)
    Ks = kraus(name)
    Ekr = channel_from_kraus(Ks)
    match = float(max(np.abs(Edil(b) - Ekr(b)).max() for b in _BASIS))
    tp = float(max(abs(np.trace(Edil(b)) - np.trace(b)) for b in _BASIS))
    comp = float(np.abs(sum(K.conj().T @ K for K in Ks) - np.eye(2)).max())
    row = {"app": app_id, "channel": name, "unitary": unitary,
           "kraus_match": match, "trace_preserving": tp, "kraus_completeness": comp}
    if name in ("bitflip", "phasedamp", "ampdamp"):
        Ubad = _wrong_angle_dilation(name)
        Ebad = channel_from_unitary(Ubad, 1)
        row["teeth_wrong_angle"] = bool(max(np.abs(Ebad(b) - Ekr(b)).max() for b in _BASIS) > 1e-3)
    else:                                       # depol: E==I/2 (완전 망각) 추가 확인
        row["teeth_wrong_angle"] = bool(max(np.abs(Edil(b) - 0.5 * np.trace(b) * I).max()
                                            for b in _BASIS) < 1e-9)
        row["fully_depolarizing_E_eq_I_over_2"] = row["teeth_wrong_angle"]
    row["ok"] = bool(unitary and match < 1e-9 and tp < 1e-9 and comp < 1e-9 and row["teeth_wrong_angle"])
    return row


def observe_composition():
    """봉인 dilation 직렬연결 → 합성 채널 관측(compounding). 2q dilation 을 두 번 통과."""
    def E2(U):
        return channel_from_unitary(U, 1)
    def compose(E1, Ea):
        return lambda r: Ea(E1(r))
    def ad_ref(g):
        return channel_from_kraus([np.diag([1, np.sqrt(1 - g)]).astype(complex),
                                   np.array([[0, np.sqrt(g)], [0, 0]], dtype=complex)])
    def pd_ref(lam):
        return channel_from_kraus([np.diag([1, np.sqrt(1 - lam)]).astype(complex),
                                   np.diag([0, np.sqrt(lam)]).astype(complex)])
    Upd = load_golden("stinespring_phasedamp.app.pg")
    Uad = load_golden("stinespring_ampdamp.app.pg")
    Epd2 = compose(E2(Upd), E2(Upd))
    Ead2 = compose(E2(Uad), E2(Uad))
    m_pd = float(max(np.abs(Epd2(b) - pd_ref(0.75)(b)).max() for b in _BASIS))
    m_ad = float(max(np.abs(Ead2(b) - ad_ref(0.75)(b)).max() for b in _BASIS))
    return {"phasedamp_half_composed": "== phase-damping(λ_eff=3/4)", "phasedamp_match": m_pd,
            "ampdamp_half_composed": "== amplitude-damping(γ_eff=3/4)", "ampdamp_match": m_ad,
            "ok": bool(m_pd < 1e-9 and m_ad < 1e-9)}


def _ry(a):
    return np.array([[np.cos(a/2), -np.sin(a/2)], [np.sin(a/2), np.cos(a/2)]], dtype=complex)


def _emb(op, q):
    return np.kron(op, I) if q == 0 else np.kron(I, op)


def _cnot(c, t):
    M = np.zeros((4, 4), dtype=complex)
    for x in range(4):
        b = [(x >> 1) & 1, x & 1]; b[t] ^= b[c]
        M[(b[0] << 1) | b[1], x] = 1.0
    return M


def _cry(theta, c, t):
    U = np.eye(4, dtype=complex)
    for G in [_cnot(c, t), _emb(_ry(-theta/2), t), _cnot(c, t), _emb(_ry(theta/2), t)]:
        U = G @ U
    return U


def _wrong_angle_dilation(name):
    bad = 0.8 * np.pi / 2
    if name == "bitflip":
        return _cnot(1, 0) @ _emb(_ry(bad), 1)
    if name == "phasedamp":
        return _cry(bad, 0, 1)
    if name == "ampdamp":
        return _cnot(1, 0) @ _cry(bad, 0, 1)


def observe():
    rows = [verify_one("stinespring_bitflip", "bitflip"),
            verify_one("stinespring_phasedamp", "phasedamp"),
            verify_one("stinespring_ampdamp", "ampdamp"),
            verify_one("stinespring_depol", "depol", n_env=2)]
    comp = observe_composition()
    ok = all(r["ok"] for r in rows) and comp["ok"]
    return {"axis": "열린 양자계 (CPTP 채널 Stinespring dilation + compounding)",
            "sealed_assets": "stinespring_bitflip/phasedamp/ampdamp/depol (dilation 유니터리 Tier-0 exact)",
            "channels": rows,
            "composition": comp,
            "honest_boundary": "봉인=dilation 유니터리뿐. 채널 E(ρ)=Tr_env[U(ρ⊗|0⟩⟨0|)U†]=비유니터리 "
                               "초연산자 → 관측(seal 아님). dyadic 점(½ 감쇠·depol p=1)만 exact; 일반 감쇠율·"
                               "다큐빗·하드웨어 노이즈=차기. 합성=봉인 자산 복리 관측. 신규 봉인=depol 1개(INV-Q3).",
            "ok": bool(ok)}


def main():
    quick = "--quick" in sys.argv
    res = observe()
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        report = {"_schema": "channel-observe-v1",
                  "_note": "3 채널 dilation 의 Tr_env == Kraus 채널 exact + CPTP witness. 봉인=유니터리뿐(INV-Q3). 신규 봉인 0.",
                  "observation": res}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("CPTP 채널 Stinespring dilation witness 관측:", flush=True)
        for r in res["channels"]:
            print(f"  {r['channel']:10}: Tr_env==Kraus {r['kraus_match']:.1e} · trace-preserve {r['trace_preserving']:.1e} "
                  f"· ΣK†K=I {r['kraus_completeness']:.1e} · teeth/E=I/2 {r['teeth_wrong_angle']}", flush=True)
        c = res["composition"]
        print(f"  compose   : phasedamp½∘½==λ¾ {c['phasedamp_match']:.1e} · ampdamp½∘½==γ¾ {c['ampdamp_match']:.1e}", flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"channel_observe: all_ok={res['ok']}", flush=True)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
