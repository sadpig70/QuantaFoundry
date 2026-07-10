#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""column_verify — CQV (Column-stream Quantum Verification), TrackIU IU_A (DESIGN-IntegratedUpgrade).

structural Shor 앱(Tier-1)의 **전체 유니터리**를 dense 2^n 실체화 없이 컬럼 전수로 검증한다.
subspace proof(modexp 순열 확정) 이후 남은 갭 = "조립 논증 하나"(H-wall·modexp·iQFT 의 배선/순서/embed).
이 스크립트는 그 조립을 두 독립 경로의 열(column) 폐형식으로 닫는다.

  path A' = 회로 경로: plan 배선 그대로 —
      H-wall  : h_gate 모듈 golden 의 t-fold kron (회로가 두는 부호/정규화)
      modexp  : perm_subspace path A 순열 (cmul→MCT 게이트 전개, 봉인 golden 미참조)
      iQFT    : iqft{t}.app.pg **plan 재합성** Q_circ (모듈 golden 들의 embed 곱 — 앱 golden 미참조)
  path B' = 수학 경로: Shor 스펙트럼 공식 직접 산술 (배선 무참조) —
      amp[(c',w)] = 2^{-t/2} · Σ_{c: w0·a^c mod N = w} (−1)^{c·c0} · ω^{−c'c}/√(2^t)

  판정: 전 입력 기저 |c0,w0⟩ (2^n 컬럼 전수, n ≤ 18) 에 대해 max|A'−B'| ≤ atol(1e-12)
        + negative control 3종 (iqft 게이트 제거 / modexp 배선 교란 / a+1 산술) 전부 REJECT.

정직 경계:
  - float-atol 계급 (Tier-0 dense C4 와 동일 증거 계급) — ring-exact 참칭 금지.
    exact 이종 증인은 후속 path-sum ℤ[ω_{2^t}] 확장 (DESIGN-IntegratedUpgrade backlog).
  - 성공 등급 'unitary_equiv_column_exact' 는 semantic guarantee **레이어**에서만 반영
    (tier 숫자 불변, subspace 선례). INV-R5 는 폐기가 아니라 축소 개정.

비파괴: sidecar `.pgf/proofs/<shor_id>.column_proof.json` 만 생성.
  registry root(u_hash Merkle)·기존 sealed·oracle fingerprint·frozen consensus 무영향.

사용:
  python -m qf_witness.verify.column_verify shor69 shor95      # 지정 앱
  python -m qf_witness.verify.column_verify                    # Tier-1 shor n_sys<=18 전종
  python -m qf_witness.verify.column_verify --quick            # reproduce_all 용 경량 재검증
"""
import os
import re
import sys
import json
import glob
import hashlib
import numpy as np

from qf_witness.core.paths import ROOT
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import perm_subspace_verify as psv  # noqa: E402  (파서·순열 경로 재사용)

SPECS_APPS = os.path.join(ROOT, "specs", "apps")
SPECS_MODULES = os.path.join(ROOT, "specs", "modules")
PROOFS = os.path.join(ROOT, ".pgf", "proofs")
ATOL = 1e-12
COLUMN_BOUND = 18   # n_sys ≤ 18 → 컬럼 전수; ≥19 → 범위 외(CUC 후속)


# ── spec 로드 ──────────────────────────────────────────────────────────────
def _module_golden(name):
    """specs/modules/<name>.pg 의 ```python id=golden``` 블록 → ndarray."""
    txt = open(os.path.join(SPECS_MODULES, f"{name}.pg"), encoding="utf-8").read()
    m = re.search(r"```python id=golden\s*\n(.*?)\n```", txt, re.S)
    if not m:
        raise ValueError(f"no golden block in module {name}")
    ns = {}
    exec(m.group(1), ns)  # noqa: S102 — tracked spec 파일, 봉인 시 검증된 소스
    return np.asarray(ns["golden"], dtype=complex)


def embed_unitary(Ug, targets, n):
    """g-큐빗 게이트를 n-큐빗 공간에 embed (big-endian: qubit q → bit n-1-q).
    표준 텐서 삽입: P† (I_rest ⊗ Ug) P, P = 비트 재배열 순열 (벡터화)."""
    g = len(targets)
    rest = [q for q in range(n) if q not in targets]
    idx = np.arange(1 << n)
    tb = np.zeros_like(idx)
    for m_, q in enumerate(targets):
        tb |= ((idx >> (n - 1 - q)) & 1) << (g - 1 - m_)
    rb = np.zeros_like(idx)
    for m_, q in enumerate(rest):
        rb |= ((idx >> (n - 1 - q)) & 1) << (len(rest) - 1 - m_)
    pos = (rb << g) | tb                       # |idx⟩ 가 (rest, tgt) 블록 좌표로 가는 위치
    U_block = np.kron(np.eye(1 << len(rest), dtype=complex), Ug)
    out = np.empty((1 << n, 1 << n), dtype=complex)
    # U_full[i,j] = U_block[pos[i], pos[j]]  (P 를 실체화하지 않는 인덱스 수집)
    out[:, :] = U_block[np.ix_(pos, pos)]
    return out


def compose_iqft_circuit(t, drop_last_gate=False):
    """iqft{t}.app.pg 의 plan 을 모듈 golden 으로 재합성 → Q_circ (2^t×2^t).
    회로 경로: 앱 golden(정의행렬) 미참조 — plan 의 모듈 시퀀스가 실제로 하는 일.
    drop_last_gate: negative control 용 (게이트 1개 제거 → 반드시 불일치해야)."""
    plan = psv._parse_plan(os.path.join(SPECS_APPS, f"iqft{t}.app.pg"))
    steps = plan["steps"][:-1] if drop_last_gate else plan["steps"]
    Q = np.eye(1 << t, dtype=complex)
    for st in steps:
        name = os.path.basename(st["spec"])[:-len(".pg")]
        Q = embed_unitary(_module_golden(name), st["targets"], t) @ Q
    return Q


def iqft_definition_matrix(t):
    """수학 경로: IQFT 정의행렬 (1/√M)·ω^{−jk} (배선·plan 무참조)."""
    M = 1 << t
    j, k = np.meshgrid(np.arange(M), np.arange(M), indexing="ij")
    return np.exp(-2j * np.pi * j * k / M) / np.sqrt(M)


def hwall_circuit(t):
    """회로 경로 H-wall: h_gate 모듈 golden 의 t-fold kron (2^t×2^t)."""
    H = _module_golden("h_gate")
    W = np.array([[1.0]], dtype=complex)
    for _ in range(t):
        W = np.kron(W, H)
    return W


def hwall_formula(t):
    """수학 경로 H-wall: 2^{-t/2}·(−1)^{popcount(c & c0)} (공식 직접)."""
    M = 1 << t
    c, c0 = np.meshgrid(np.arange(M), np.arange(M), indexing="ij")
    signs = 1.0 - 2.0 * (np.array([bin(x).count("1") for x in range(M)])[c & c0] % 2)
    return signs.astype(complex) / np.sqrt(M)


# ── 열 스트리밍 검증 ────────────────────────────────────────────────────────
def _perm_w_of_c(perm_vec, t, work, w0):
    """전체 순열 벡터에서 w0 슬라이스 추출: c → w'(c,w0). counting 불변도 확인."""
    c = np.arange(1 << t, dtype=np.int64)
    s = (c << work) | w0
    img = perm_vec[s]
    if not np.array_equal(img >> work, c):     # modexp 는 counting 을 건드리면 안 됨
        raise AssertionError("modexp permutation moved counting register")
    return img & ((1 << work) - 1)


def _arith_w_of_c(t, work, a, N, w0):
    """수학 경로: c → w0·a^c mod N (w0 ≥ N 은 항등)."""
    c = np.arange(1 << t)
    if w0 >= N:
        return np.full(1 << t, w0, dtype=np.int64)
    return np.array([(w0 * pow(a, int(cc), N)) % N for cc in c], dtype=np.int64)


def _stream_compare(Q_A, W_A, fw_A, Q_B, W_B, fw_B):
    """한 w0 슬라이스의 전 컬럼(전 c0) A' vs B' 최대 편차.
    R[w] = Q[:, {c: fw(c)=w}] @ W[{c: fw(c)=w}, :]  — (c'×c0) 블록별 비교."""
    dev = 0.0
    ws = np.union1d(np.unique(fw_A), np.unique(fw_B))
    for w in ws:
        ia = np.nonzero(fw_A == w)[0]
        ib = np.nonzero(fw_B == w)[0]
        RA = Q_A[:, ia] @ W_A[ia, :] if len(ia) else 0.0
        RB = Q_B[:, ib] @ W_B[ib, :] if len(ib) else 0.0
        dev = max(dev, float(np.max(np.abs(RA - RB))))
    return dev


def verify(shor_id, atol=ATOL, teeth=True, w0_limit=None):
    """전 컬럼 A'==B' + negative control 3종. → proof dict."""
    p = psv.load_shor(shor_id)
    n, t, work, a, N = p["n"], p["t"], p["work"], p["a"], p["N"]
    if n > COLUMN_BOUND:
        raise ValueError(f"{shor_id}: n_sys={n} > {COLUMN_BOUND} — CUC 경로(후속) 대상")
    gates = psv.expand_modexp_gates(p["modexp_steps"])
    perm = psv.path_a_vec(n, gates)            # 회로 순열 (전체 2^n, exact int)

    Q_A, W_A = compose_iqft_circuit(t), hwall_circuit(t)       # 회로 경로
    Q_B, W_B = iqft_definition_matrix(t), hwall_formula(t)     # 수학 경로

    w0s = range(1 << work) if w0_limit is None else range(min(w0_limit, 1 << work))
    max_dev, cols = 0.0, 0
    for w0 in w0s:
        fw_A = _perm_w_of_c(perm, t, work, w0)
        fw_B = _arith_w_of_c(t, work, a, N, w0)
        max_dev = max(max_dev, _stream_compare(Q_A, W_A, fw_A, Q_B, W_B, fw_B))
        cols += 1 << t
    ok = max_dev <= atol

    nc = {}
    if teeth:
        w0t = 1 % (1 << work)                  # 대표 슬라이스 (w0=1 < N 항상)
        fw_A = _perm_w_of_c(perm, t, work, w0t)
        fw_B = _arith_w_of_c(t, work, a, N, w0t)
        # teeth1: iqft 재합성에서 게이트 1개 제거 → 불일치해야
        nc["iqft_gate_drop"] = _stream_compare(compose_iqft_circuit(t, drop_last_gate=True),
                                               W_A, fw_A, Q_B, W_B, fw_B) > atol
        # teeth2: modexp 배선 교란 (perm_subspace 방식: 첫 게이트 target 이동) → 불일치해야.
        #   교란 게이트가 발화하지 않는 w0 슬라이스에서는 순열이 그대로일 수 있으므로,
        #   교란이 실제로 순열을 바꾸는 w0 슬라이스를 찾아 그 슬라이스의 컬럼으로 검출한다.
        mut = list(gates)
        (mc, mt) = mut[0]
        alt = (mt + 1) % n
        while alt in mc or alt == mt:
            alt = (alt + 1) % n
        mut[0] = (mc, alt)
        perm_mut = psv.path_a_vec(n, mut)
        wiring_detected = False
        for w0c in range(1 << work):
            try:
                fw_mut = _perm_w_of_c(perm_mut, t, work, w0c)
            except AssertionError:             # counting 침범 = 더 강한 규약 파괴 검출
                wiring_detected = True
                break
            if not np.array_equal(fw_mut, _perm_w_of_c(perm, t, work, w0c)):
                fw_Bc = _arith_w_of_c(t, work, a, N, w0c)
                wiring_detected = _stream_compare(Q_A, W_A, fw_mut, Q_B, W_B, fw_Bc) > atol
                break
        nc["wiring_perturb"] = wiring_detected
        # teeth3: 틀린 산술 a+1 → 불일치해야
        fw_bad = _arith_w_of_c(t, work, a + 1, N, w0t)
        nc["arith_perturb"] = _stream_compare(Q_A, W_A, fw_A, Q_B, W_B, fw_bad) > atol
    nc_all = all(nc.values()) if nc else False
    verified = ok and nc_all

    return {
        "id": shor_id, "N": N, "a": a, "n_sys": n, "counting_t": t, "work": work,
        "columns_tested": cols, "columns_total": 1 << n,
        "exhaustive": cols == (1 << n),
        "max_abs_dev": max_dev, "atol": atol,
        "path_A": "circuit: h_gate golden kron-wall · perm_subspace MCT permutation · "
                  "iqft plan recomposed from module goldens (app golden unreferenced)",
        "path_B": "math: Shor spectral formula 2^{-t/2}(−1)^{c·c0}·ω^{−c'c}/√2^t · "
                  "integer arithmetic w0·a^c mod N (wiring-free)",
        "negative_controls": nc, "negative_control_reject": nc_all,
        "verified": verified,
        "grade": "unitary_equiv_column_exact" if verified else "column_mismatch",
        "arith": "float64_atol",               # 정직: ring-exact 아님 (Tier-0 dense C4 동급)
        "dense_materialized": False,           # 최대 블록 = 2^t×2^t (t≤8) — 2^n 미실체화
        "deterministic": True,
    }


def _digest(proof):
    body = {k: proof[k] for k in ("id", "N", "a", "n_sys", "columns_tested",
                                  "columns_total", "grade")}
    return hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]


def write_sidecar(proof):
    os.makedirs(PROOFS, exist_ok=True)
    proof = dict(proof, proof_digest=_digest(proof),
                 _schema="column-proof-v1",
                 _note="비파괴 sidecar. registry root/sealed/oracle/frozen 무영향. "
                       "shor 전체 유니터리 컬럼 전수 검증(조립 논증 폐합, float-atol 계급). "
                       "INV-R5 는 이 앱에 한해 축소: 전 컬럼 A'==B' (H·iQFT 포함).")
    path = os.path.join(PROOFS, f"{proof['id']}.column_proof.json")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(proof, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    return path


def quick_recheck(shor_id="shor69"):
    """reproduce_all 용 경량 재검증: w0 2슬라이스 전 컬럼 + teeth 3종 + sidecar 정합."""
    sc_path = os.path.join(PROOFS, f"{shor_id}.column_proof.json")
    if not os.path.exists(sc_path):
        raise FileNotFoundError(f"no sidecar {shor_id}.column_proof.json")
    sc = json.load(open(sc_path, encoding="utf-8"))
    if not (sc.get("verified") and sc.get("grade") == "unitary_equiv_column_exact"):
        return False
    r = verify(shor_id, teeth=True, w0_limit=2)
    return bool(r["max_abs_dev"] <= ATOL and r["negative_control_reject"])


def main():
    args = [a for a in sys.argv[1:]]
    if "--quick" in args:
        ok = quick_recheck()
        print(f"column_verify quick: {'PASS' if ok else 'FAIL'}")
        sys.exit(0 if ok else 1)
    ids = [a for a in args if not a.startswith("-")]
    if not ids:
        ids = [s for s in psv.STRUCTURAL_SHOR
               if psv.load_shor(s)["n"] <= COLUMN_BOUND]
    all_ok = True
    for sid in ids:
        r = verify(sid)
        path = write_sidecar(r)
        flag = "OK " if r["verified"] else "FAIL"
        print(f"[{flag}] {sid}: n={r['n_sys']} cols={r['columns_tested']}/{r['columns_total']} "
              f"max_dev={r['max_abs_dev']:.2e} teeth={r['negative_control_reject']} → {os.path.basename(path)}")
        all_ok &= r["verified"]
    print(f"column_verify: {'ALL VERIFIED' if all_ok else 'SOME FAILED'} ({len(ids)} apps)")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
