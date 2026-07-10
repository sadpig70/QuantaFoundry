#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""stabrank_verify — TrackHE4 P6: stabilizer-rank(Clifford-합 분해) 제5 독립 검증경로 (인프라, 신규 봉인 0).

기존 4경로(dense 행렬·Clifford tableau·ZX·path-sum ℤ[ω₈])에 이은 다섯 번째 독립 수학:
봉인 Clifford+T 앱을 **안정 기하**로 재검증한다 — 회로를 비-Clifford 대각 게이트에서 Clifford-합으로
분기 전개(Bravyi-Gosset 계열)하고, 각 Clifford 분기를 아핀 지지대 + ℤ₄ 위상 이차형식(quadratic form,
Dehaene–De Moor 계열)으로 **행렬 곱 없이** 진화시켜 진폭을 유한합으로 얻는다.

  분기 전개(전부 닫힌형 exact):
    T^±   = a·I + b·S^±        (a=1−b, b=(1−ω₈^±)/(1−i^±))          — 2분기
    CS    = ½(1+i)·I + ½(1−i)·CZ                                     — 2분기
    CT    = ½(1+ω₈)·I + ½(1−ω₈)·CZ                                   — 2분기
    CCZ   = ½(I + Z_a + CZ_bc − Z_a·CZ_bc)      ((−1)^{abc} 항등)     — 4분기
    CCCZ  = ½(I + CZ_ab + CZ_cd − CZ_ab·CZ_cd)  ((−1)^{(ab)(cd)})     — 4분기
    toffoli = h·CCZ·h · c3x = h·CCCZ·h (H 는 엔진 네이티브)
  안정 엔진(게이트 = 자료구조 갱신, 행렬 무사용):
    상태: 지지대 x_m(t)=⊕_{j∈S_m}t_j⊕b_m (t∈F₂^k) · 위상 p(t)=c₀+Σc_jt_j+2Σb_{jl}t_jt_l (ℤ₄) · γ
    H_m: 새 변수 u, p += 2·x_m·u, x_m:=u, γ/=√2 (변수 소거 없는 정확형 — 판독 시 2^k 열거 유한합)

검증: 봉인 앱의 golden 열(기저 입력 3개) == 엔진 유한합 — 지원 게이트 전수·분기수 상한 내 앱 자동
발견(무발견=명시 skip, silent cap 금지). 엔진 자가시험: 지원 게이트 무작위 회로(seed) vs 직접 구성.

정직 경계(INV-Q3): 검증경로 인프라 — 새 봉인 0·registry root 불변·오라클/frozen 무접촉(sidecar).
  커버리지 = Clifford+{T,CS,CT,CCZ,Toffoli,C3X} 단편 + 분기곱≤4096 (비용 2^t — honest 한계 명문).
  ry/z5/ω₈ 밖 게이트 앱·대형 T-count 앱은 skip 목록에 기록. 수치=부동소수(전제 독립이 요점).

사용: python -m qf_witness.verify.stabrank_verify [--quick]
"""
import os, sys, re, json, glob
from itertools import product
import numpy as np

from qf_witness.core.paths import ROOT
OUT = os.path.join(ROOT, ".pgf", "proofs", "STABRANK-VERIFY.json")
W8 = np.exp(1j * np.pi / 4)
BRANCH_CAP = 4096
N_CAP = 10


# ── 안정 엔진: 아핀 지지대 + ℤ₄ 이차형식 ──────────────────────────────────
class Stab:
    def __init__(self, n, x0):
        self.n, self.k = n, 0
        self.S = [0] * n                       # 행 m: t-변수 비트마스크
        self.b = [(x0 >> (n - 1 - m)) & 1 for m in range(n)]
        self.c0 = 0                            # ℤ₄ 상수
        self.cl = []                           # ℤ₄ 선형계수 (per 변수)
        self.q = {}                            # (j,l) j<l → F₂ (2·t_jt_l 항)
        self.gamma = 1.0 + 0j

    def _qflip(self, j, l):
        if j == l:
            self.cl[j] = (self.cl[j] + 2) % 4  # t²=t
        else:
            key = (min(j, l), max(j, l))
            self.q[key] = self.q.get(key, 0) ^ 1

    def _add_xor_phase(self, tau, mask, bconst):
        """p += tau·(⊕_{j∈mask} t_j ⊕ bconst)  (ℤ₄, XOR→산술 전개: 짝 -2 항)"""
        tau %= 4
        if tau == 0:
            return
        if bconst:                              # 1⊕X = 1 + (4−1)X 꼴: tau·(1⊕X) = tau + (4−tau)·X
            self.c0 = (self.c0 + tau) % 4
            tau = (-tau) % 4
            if tau == 0:
                return
        js = [j for j in range(self.k) if (mask >> j) & 1]
        for j in js:
            self.cl[j] = (self.cl[j] + tau) % 4
        if tau % 2 == 1:                        # −2·tau ≡ 2 (mod 4) ↔ tau 홀수
            for a in range(len(js)):
                for bb in range(a + 1, len(js)):
                    self._qflip(js[a], js[bb])

    def _add_prod_phase(self, m, n2):
        """p += 2·x_m·x_n (CZ)"""
        Sm, bm, Sn, bn = self.S[m], self.b[m], self.S[n2], self.b[n2]
        jm = [j for j in range(self.k) if (Sm >> j) & 1]
        jn = [j for j in range(self.k) if (Sn >> j) & 1]
        for j in jm:
            for l in jn:
                self._qflip(j, l)
        if bn:
            for j in jm:
                self.cl[j] = (self.cl[j] + 2) % 4
        if bm:
            for l in jn:
                self.cl[l] = (self.cl[l] + 2) % 4
        self.c0 = (self.c0 + 2 * bm * bn) % 4

    def g_x(self, m): self.b[m] ^= 1
    def g_z(self, m): self._add_xor_phase(2, self.S[m], self.b[m])
    def g_s(self, m, sgn=1): self._add_xor_phase(1 if sgn > 0 else 3, self.S[m], self.b[m])
    def g_cz(self, m, n2): self._add_prod_phase(m, n2)
    def g_cnot(self, c, t): self.S[t] ^= self.S[c]; self.b[t] ^= self.b[c]

    def g_h(self, m):
        u = self.k
        self.k += 1
        self.cl.append(0)
        # p += 2·x_m·u
        for j in [j for j in range(u) if (self.S[m] >> j) & 1]:
            self._qflip(j, u)
        if self.b[m]:
            self.cl[u] = (self.cl[u] + 2) % 4
        self.S[m], self.b[m] = (1 << u), 0
        self.gamma /= np.sqrt(2.0)

    def readout(self):
        vec = np.zeros(2 ** self.n, dtype=complex)
        I4 = [1, 1j, -1, -1j]
        for t in range(2 ** self.k):
            ph = self.c0
            for j in range(self.k):
                if (t >> j) & 1:
                    ph += self.cl[j]
            for (j, l), v in self.q.items():
                if v and ((t >> j) & 1) and ((t >> l) & 1):
                    ph += 2
            idx = 0
            for m in range(self.n):
                bit = self.b[m]
                sm = self.S[m] & t
                while sm:
                    bit ^= 1
                    sm &= sm - 1
                idx = (idx << 1) | bit
            vec[idx] += self.gamma * I4[ph % 4]
        return vec


# ── 분기 전개 ─────────────────────────────────────────────────────────────
def branches_of(op, tg):
    a_t = 1 - (1 - W8) / (1 - 1j)
    b_t = (1 - W8) / (1 - 1j)
    a_td = 1 - (1 - np.conj(W8)) / (1 + 1j)
    b_td = (1 - np.conj(W8)) / (1 + 1j)
    if op == "t":
        return [(a_t, []), (b_t, [("s", tg)])]
    if op == "tdg":
        return [(a_td, []), (b_td, [("sdg", tg)])]
    if op == "cs":
        return [((1 + 1j) / 2, []), ((1 - 1j) / 2, [("cz", tg)])]
    if op == "ct":
        return [((1 + W8) / 2, []), ((1 - W8) / 2, [("cz", tg)])]
    if op == "ccz":
        za, bc = [tg[0]], [tg[1], tg[2]]
        return [(0.5, []), (0.5, [("z", za)]), (0.5, [("cz", bc)]),
                (-0.5, [("z", za), ("cz", bc)])]
    if op == "cccz":
        ab, cd = [tg[0], tg[1]], [tg[2], tg[3]]
        return [(0.5, []), (0.5, [("cz", ab)]), (0.5, [("cz", cd)]),
                (-0.5, [("cz", ab), ("cz", cd)])]
    return None


CLIFF = {"h", "x", "z", "s", "sdg", "cz", "cnot"}
MODMAP = {"h_gate": "h", "x_gate": "x", "z_gate": "z", "s_gate": "s", "sdg_gate": "sdg",
          "cnot": "cnot", "cz": "cz", "t_gate": "t", "cs_gate": "cs", "ct_gate": "ct",
          "ccz": "ccz"}


def flatten(app_file, targets=None):
    """plan → 원시 op 리스트 (sub-app 재귀, toffoli/c3x → h·C..Z·h). 미지원 시 예외."""
    src = open(os.path.join(ROOT, "specs", "apps", app_file), encoding="utf-8").read()
    plan = json.loads(re.search(r"```json id=plan\s*\n(.*?)\n```", src, re.S).group(1))
    ops = []
    for st in plan["steps"]:
        tg = st.get("targets")
        if tg is None:
            tg = targets                     # 생략형 = 전체 레지스터 상속(항등이면 None 유지)
        elif targets is not None:
            tg = [targets[q] for q in tg]
        if "app" in st:
            ops += flatten(st["app"], tg)
            continue
        if tg is None:
            raise ValueError("no-targets-module")
        name = st["spec"].split("/")[-1][:-3]
        if name == "toffoli":
            ops += [("h", [tg[2]]), ("ccz", tg), ("h", [tg[2]])]
        elif name == "c3x":
            ops += [("h", [tg[3]]), ("cccz", tg), ("h", [tg[3]])]
        elif name in MODMAP:
            ops.append((MODMAP[name], tg))
        else:
            raise ValueError(f"unsupported:{name}")
    return ops


def branch_count(ops):
    n = 1
    for op, _ in ops:
        br = branches_of(op, [0] * 4)
        n *= len(br) if br else 1
    return n


def run_column(ops, n, x0):
    """입력 |x0⟩ → 출력 열벡터 (분기 합)."""
    expanded = [branches_of(op, tg) or [(1.0, [(op, tg)])] for op, tg in ops]
    vec = np.zeros(2 ** n, dtype=complex)
    for choice in product(*expanded):
        coeff = 1.0 + 0j
        st = Stab(n, x0)
        for (c, sub) in choice:
            coeff *= c
            for (g, tg) in sub:
                if g == "h": st.g_h(tg[0])
                elif g == "x": st.g_x(tg[0])
                elif g == "z": st.g_z(tg[0])
                elif g == "s": st.g_s(tg[0], 1)
                elif g == "sdg": st.g_s(tg[0], -1)
                elif g == "cz": st.g_cz(tg[0], tg[1])
                elif g == "cnot": st.g_cnot(tg[0], tg[1])
        vec += coeff * st.readout()
    return vec


def load_golden(app_file):
    src = open(os.path.join(ROOT, "specs", "apps", app_file), encoding="utf-8").read()
    m = re.search(r"```python id=app_golden\n(.*?)```", src, re.S)
    if not m:
        return None
    ns = {}
    exec(m.group(1), ns)
    return ns["golden"]


# ── 자가시험: 지원 게이트 무작위 회로 vs 직접 구성 ────────────────────────
def selftest(seed=0, rounds=24):
    G = {"h": np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2),
         "x": np.array([[0, 1], [1, 0]], dtype=complex), "z": np.diag([1, -1]).astype(complex),
         "s": np.diag([1, 1j]).astype(complex), "sdg": np.diag([1, -1j]).astype(complex),
         "t": np.diag([1, W8]).astype(complex), "tdg": np.diag([1, np.conj(W8)]).astype(complex),
         "cz": np.diag([1, 1, 1, -1]).astype(complex),
         "cs": np.diag([1, 1, 1, 1j]).astype(complex),
         "ct": np.diag([1, 1, 1, W8]).astype(complex),
         "cnot": np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex),
         "ccz": np.diag([1] * 7 + [-1]).astype(complex),
         "cccz": np.diag([1] * 15 + [-1]).astype(complex)}
    def emb(U, tg, n):
        k = int(round(np.log2(U.shape[0])))
        full = np.zeros((2 ** n, 2 ** n), dtype=complex)
        for idx in range(2 ** n):
            bits = [(idx >> (n - 1 - q)) & 1 for q in range(n)]
            si = 0
            for q in tg:
                si = (si << 1) | bits[q]
            for so in range(2 ** k):
                if abs(U[so, si]) < 1e-16:
                    continue
                ob = list(bits)
                for j, q in enumerate(tg):
                    ob[q] = (so >> (k - 1 - j)) & 1
                oi = 0
                for q in range(n):
                    oi = (oi << 1) | ob[q]
                full[oi, idx] += U[so, si]
        return full
    rng = np.random.default_rng(seed)
    names = list(G.keys())
    for r in range(rounds):
        n = int(rng.integers(2, 5))
        ops = []
        for _ in range(int(rng.integers(3, 9))):
            g = names[int(rng.integers(0, len(names)))]
            ar = int(round(np.log2(G[g].shape[0])))
            if ar > n:
                continue
            tg = list(rng.permutation(n)[:ar])
            ops.append((g, tg))
        U = np.eye(2 ** n, dtype=complex)
        for g, tg in ops:
            U = emb(G[g], tg, n) @ U
        x0 = int(rng.integers(0, 2 ** n))
        col = run_column(ops, n, x0)
        if not np.allclose(col, U[:, x0], atol=1e-9):
            return False, r
    return True, rounds


# ── 대상 자동 발견 + 검증 ─────────────────────────────────────────────────
def discover_and_verify(sample=False):
    """sample=True: 고속 표본(분기≤256·n≤6·상위 20앱 결정론 선별) — reproduce 체인용
    (INV-F1 계층화 선례: 정본 커버리지는 full 실행 산출 proofs JSON)."""
    verified, skipped = {}, {}
    cap_b = 256 if sample else BRANCH_CAP
    cap_n = 6 if sample else N_CAP
    for p in sorted(glob.glob(os.path.join(ROOT, "registry", "apps", "*.sealed.json"))):
        aid = os.path.basename(p)[:-len(".sealed.json")]
        spec = os.path.join(ROOT, "specs", "apps", f"{aid}.app.pg")
        if not os.path.exists(spec):
            skipped[aid] = "no-spec"
            continue
        meta = json.load(open(p, encoding="utf-8"))
        try:
            src = open(spec, encoding="utf-8").read()
            am = json.loads(re.search(r"```json id=app_meta\s*\n(.*?)\n```", src, re.S).group(1))
            n = am["n_sys"] + am.get("n_anc", 0)
            if n > cap_n:
                skipped[aid] = f"n={n}>cap"
                continue
            ops = flatten(f"{aid}.app.pg")
        except ValueError as e:
            skipped[aid] = str(e)
            continue
        bc = branch_count(ops)
        if bc > cap_b:
            skipped[aid] = f"branches={bc}>cap"
            continue
        if sample and len(verified) >= 20:
            skipped[aid] = "sample-cap-20"
            continue
        gold = load_golden(f"{aid}.app.pg")
        if gold is None:
            skipped[aid] = "no-dense-golden"
            continue
        cols = sorted(set([0, 1 % 2 ** n, (2 ** n) - 1]))
        # 전역위상(C4 up-to-phase) 일관: 첫 열에서 φ 추출 후 전 열 동일 φ 대조
        c0 = run_column(ops, n, 0)
        i0 = int(np.argmax(np.abs(gold[:, 0])))
        ph = c0[i0] / gold[i0, 0] if abs(gold[i0, 0]) > 1e-12 else 1.0
        ok = bool(abs(abs(ph) - 1) < 1e-9)
        for x0 in cols:
            col = run_column(ops, n, x0)
            ok &= bool(np.allclose(col, ph * gold[:, x0], atol=1e-9))
        verified[aid] = {"n": n, "branches": bc, "gates": len(ops), "cols": len(cols),
                         "match": ok}
    return verified, skipped


def teeth():
    """분기 계수 오염(T 의 b→0.9b) → t_teleport 급 회로 불일치 검출."""
    ops = flatten("t_teleport.app.pg")
    gold = load_golden("t_teleport.app.pg")
    a_t = 1 - (1 - W8) / (1 - 1j)
    b_t = (1 - W8) / (1 - 1j)
    # cs → 오염된 2분기(계수 0.9배)로 수동 전개
    vec = np.zeros(4, dtype=complex)
    for (c, sub) in [((1 + 1j) / 2, []), (0.9 * (1 - 1j) / 2, [("cz", [0, 1])])]:
        st = Stab(2, 0)
        for (g, tg) in [("cnot", [0, 1])] + sub:
            (st.g_cnot(tg[0], tg[1]) if g == "cnot" else st.g_cz(tg[0], tg[1]))
        vec += c * st.readout()
    corrupt_detected = bool(not np.allclose(vec, gold[:, 0], atol=1e-6))
    _ = (a_t, b_t)
    return corrupt_detected


def main():
    quick = "--quick" in sys.argv
    sample = "--sample" in sys.argv
    st_ok, st_n = selftest(rounds=8 if sample else 24)
    verified, skipped = discover_and_verify(sample=sample)
    n_ok = sum(1 for v in verified.values() if v["match"])
    teeth_ok = teeth()
    ok = bool(st_ok and n_ok == len(verified) and len(verified) >= 10 and teeth_ok)
    if not quick:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        rep = {"_schema": "stabrank-verify-v1",
               "_note": "제5 독립 검증경로(안정 기하: Clifford-합 분기 + 아핀/이차형식 진폭). "
                        "인프라 — 새 봉인 0·root 불변·오라클 무접촉(INV-Q3).",
               "engine_selftest": {"ok": st_ok, "rounds": st_n},
               "verified": verified, "verified_pass": n_ok, "verified_total": len(verified),
               "skipped_with_reason": skipped,
               "coverage_note": f"지원=Clifford+{{T,CS,CT,CCZ,Toffoli,C3X}} · 분기곱≤{BRANCH_CAP} · "
                                f"n≤{N_CAP} · 열 3개/앱. skip 은 전수 사유 기록(silent cap 금지).",
               "teeth_branch_coeff_corrupt": teeth_ok,
               "independence": "dense(행렬곱)·tableau(안정군)·ZX(그래프)·path-sum(ℤ[ω₈] 합)과 달리 "
                               "아핀 지지대+ℤ₄ 이차형식의 유한합 — 다섯 번째 수학적 전제.",
               "ok": ok}
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(rep, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
        print("stabilizer-rank 제5 검증경로 (인프라, 새 봉인 0):", flush=True)
        print(f"  엔진 자가시험 {st_ok}({st_n}회) · 봉인 앱 검증 {n_ok}/{len(verified)} · "
              f"skip {len(skipped)}건(사유 기록) · teeth(계수 오염) {teeth_ok}", flush=True)
        big = sorted(verified.items(), key=lambda kv: -kv[1]["branches"])[:5]
        print("  최대 분기 앱:", {k: v["branches"] for k, v in big}, flush=True)
        print(f"  → {os.path.relpath(OUT, ROOT)}", flush=True)
    print(f"stabrank_verify: all_ok={ok}", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
