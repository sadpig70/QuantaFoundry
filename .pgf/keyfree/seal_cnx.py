"""seal_cnx.py — multi-control X (CnX) 게이트군 봉인 (c3x·c4x·…).

honest N=21 modular arithmetic(예: ×2 mod 21 reversible synthesis)이 C3X/C4X를 요구한다.
fredkin/toffoli와 동일 패턴으로 proof(permutation)⊕structural(projector) 독립 수렴 → key-free 확립.
bloq = qualtran MultiControlX(cvs=(1,..)) (MatrixGate 아님, 실제 게이트), golden = 독립 permutation.

control = first nc qubits (MSB), target = last qubit (big-endian, 라이브러리 컨벤션).

사용:  python .pgf/keyfree/seal_cnx.py 3 4        # c3x·c4x 봉인 (인자 없으면 [3,4])
"""
import os, sys, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts"))
import consensus as C                  # noqa: E402  (establish_truth, Source, uhash)
from registry import Registry          # noqa: E402

KEYS = os.path.join(HERE, "consensus_keys.json")
MODSPEC = os.path.join(ROOT, "specs", "modules")
MODREG = os.path.join(ROOT, "registry", "modules")


def cnx_perm(nc):
    """proof 경로: truth-table permutation (control=first nc, target=last). |1..1,t> -> |1..1, t^1>."""
    n = nc + 1
    M = np.zeros((1 << n, 1 << n), dtype=complex)
    for s in range(1 << n):
        o = (s ^ 1) if (s >> 1) == ((1 << nc) - 1) else s
        M[o, s] = 1
    return M


def cnx_projector(nc):
    """structural 경로: Σ_p |p><p| ⊗ (X if p=all1 else I) — proof와 다른 대수 구성."""
    X = np.array([[0, 1], [1, 0]], dtype=complex)
    I = np.eye(2, dtype=complex)
    dimc = 1 << nc
    M = np.zeros((dimc * 2, dimc * 2), dtype=complex)
    for p in range(dimc):
        proj = np.zeros((dimc, dimc), dtype=complex)
        proj[p, p] = 1
        M += np.kron(proj, X if p == dimc - 1 else I)
    return M


def seal_one(nc):
    gate_id = f"c{nc}x"
    if nc < 3:
        return {"nc": nc, "id": gate_id, "status": "SKIP", "reason": "nc<3 (c1x=cnot, c2x=toffoli 별칭)"}
    proof = cnx_perm(nc)
    struct = cnx_projector(nc)
    assert np.allclose(proof, struct), "proof/structural 불일치 — 구성 오류"
    sources = [C.Source(f"{gate_id}_proof", "proof", "perm", C.uhash(proof)),
               C.Source(f"{gate_id}_struct", "structural", "projector", C.uhash(struct))]
    res = C.establish_truth(gate_id, sources, N=2)
    if res.status != "ESTABLISHED":
        return {"nc": nc, "id": gate_id, "status": "FAIL", "reason": res.status}
    keys = json.load(open(KEYS, encoding="utf-8"))
    if gate_id in keys and keys[gate_id].get("frozen") and keys[gate_id]["key"] != res.key:
        return {"nc": nc, "id": gate_id, "status": "FROZEN_CONFLICT"}
    keys[gate_id] = {"key": res.key, "status": res.status, "grade": res.grade,
                     "provenance": res.provenance, "key_version": 1, "frozen": True,
                     "source": "proof+structural", "note": f"C{nc}X = multi-control X (control=first {nc}, target=last)"}
    json.dump(keys, open(KEYS, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    golden = ("import numpy as np\n"
              f"# C{nc}X: control=first {nc} qubits (MSB), target=last (big-endian). flip target iff all controls 1.\n"
              f"golden = np.zeros((1<<{nc+1}, 1<<{nc+1}), dtype=complex)\n"
              f"for s in range(1<<{nc+1}):\n"
              f"    o = (s ^ 1) if (s >> 1) == ((1<<{nc}) - 1) else s\n"
              f"    golden[o, s] = 1")
    bloq = ("from qualtran.bloqs.mcmt import MultiControlX\n"
            f"bloq = MultiControlX(cvs=(1,) * {nc})")
    spec = (f"```python id=bloq\n{bloq}\n```\n"
            f"```python id=golden\n{golden}\n```\n"
            f'```json id=meta\n{{"id": "{gate_id}", "n_sys": {nc+1}, "n_anc": 0}}\n```\n')
    sp = os.path.join(MODSPEC, f"{gate_id}.pg")
    open(sp, "w", encoding="utf-8").write(spec)
    rr = Registry(MODREG).register(sp)
    if not rr.admitted:
        return {"nc": nc, "id": gate_id, "status": "REJECT", "reason": rr.reason}
    sealed = json.load(open(os.path.join(MODREG, f"{gate_id}.sealed.json"), encoding="utf-8"))
    return {"nc": nc, "id": gate_id, "status": "SEALED", "key": res.key,
            "anti_swap_ok": sealed["u_hash"] == res.key, "grade": res.grade}


def main():
    ks = [int(a) for a in sys.argv[1:]] or [3, 4]
    print("=" * 78)
    print("multi-control X (CnX) 봉인 (key-free proof⊕structural, bloq=qualtran MultiControlX)")
    print("=" * 78)
    ok = 0
    for nc in ks:
        r = seal_one(nc)
        if r["status"] == "SEALED":
            ok += 1
            print(f"  ✅ C{nc}X {r['id']:5} SEALED {r['grade']} key={r['key'][:14]}.. anti-swap={'✓' if r['anti_swap_ok'] else '✗'}")
        else:
            print(f"  ❌ C{nc}X {r['id']:5} {r['status']} {r.get('reason','')}")
    n = len([f for f in os.listdir(MODREG) if f.endswith('.sealed.json')])
    print("=" * 78)
    print(f"신규 봉인 {ok} · 라이브러리 모듈 총 {n}")
    print("=" * 78)
    return 0 if ok == len([k for k in ks if k >= 3]) else 1


if __name__ == "__main__":
    sys.exit(main())
