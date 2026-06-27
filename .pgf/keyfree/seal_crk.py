"""seal_crk.py — controlled-Rk 게이트군 일반화 봉인 (CRk = diag(1,1,1, exp(2πi/2^k))).

cz=CR1, cs_gate=CR2, ct_gate=CR3 는 이미 봉인됨(별칭 유지). 이 드라이버는 임의 k(기본 k≥4)에 대해:
  1. crk_sources(k) proof(sympy)⊕structural(projector) 독립 수렴 → consensus_key 확립(key-free)
  2. consensus_keys.json frozen 등록 (멱등: 동일 키면 보존, 다르면 중단)
  3. module spec(.pg) 작성: golden=diag(1,1,1,exp(2πi/2^k)), bloq=ZPowGate(1/2^(k-1)).controlled()
  4. registry.register 봉인 + anti-swap(봉인 u_hash == frozen 키) 확인

사용:  python .pgf/keyfree/seal_crk.py 4 5 6        # CR4·CR5·CR6 봉인 (인자 없으면 [4])
       python .pgf/keyfree/seal_crk.py dag 3 4      # CR3†·CR4† 봉인 (inverse-QFT 군)
"""
import os, sys, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts"))
import consensus as C                  # noqa: E402
import verify_seal as vs               # noqa: E402
from registry import Registry          # noqa: E402

KEYS = os.path.join(HERE, "consensus_keys.json")
MODSPEC = os.path.join(ROOT, "specs", "modules")
MODREG = os.path.join(ROOT, "registry", "modules")

# CRk / CRk† 별칭(이미 봉인된 동치 모듈) — 재봉인 대신 안내
ALIAS = {1: "cz", 2: "cs_gate", 3: "ct_gate"}
ALIAS_DAG = {1: "cz", 2: "cs_dag"}   # CR1†=cz(자기역), CR2†=cs_dag(기존 봉인)


def _seal(k, gate_id, sources, note, golden_code, bloq_code):
    res = C.establish_truth(gate_id, sources, N=2)
    if res.status != "ESTABLISHED":
        return {"k": k, "id": gate_id, "status": "FAIL", "reason": res.status}
    keys = json.load(open(KEYS, encoding="utf-8"))
    if gate_id in keys and keys[gate_id].get("frozen") and keys[gate_id]["key"] != res.key:
        return {"k": k, "id": gate_id, "status": "FROZEN_CONFLICT"}
    keys[gate_id] = {"key": res.key, "status": res.status, "grade": res.grade,
                     "provenance": res.provenance, "key_version": 1, "frozen": True,
                     "source": "proof+structural", "note": note}
    json.dump(keys, open(KEYS, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    spec = (f"```python id=bloq\n{bloq_code}\n```\n"
            f"```python id=golden\n{golden_code}\n```\n"
            f'```json id=meta\n{{"id": "{gate_id}", "n_sys": 2, "n_anc": 0}}\n```\n')
    sp = os.path.join(MODSPEC, f"{gate_id}.pg")
    open(sp, "w", encoding="utf-8").write(spec)
    rr = Registry(MODREG).register(sp)
    if not rr.admitted:
        return {"k": k, "id": gate_id, "status": "REJECT", "reason": rr.reason}
    sealed = json.load(open(os.path.join(MODREG, f"{gate_id}.sealed.json"), encoding="utf-8"))
    return {"k": k, "id": gate_id, "status": "SEALED", "key": res.key,
            "anti_swap_ok": sealed["u_hash"] == res.key, "grade": res.grade}


def seal_one(k):
    gate_id = f"cr{k}_gate"
    if k in ALIAS:
        return {"k": k, "id": gate_id, "status": "ALIAS", "of": ALIAS[k]}
    golden = ("import numpy as np\n"
              f"# controlled-R{k} (control=first, big-endian): diag(1,1,1, exp(2*pi*i/2**{k}))\n"
              f"golden = np.diag([1, 1, 1, np.exp(2j*np.pi/2**{k})]).astype(complex)")
    bloq = ("from qualtran.bloqs.basic_gates import ZPowGate\n"
            f"bloq = ZPowGate(exponent=1/2**({k}-1)).controlled()")
    return _seal(k, gate_id, C.crk_sources(k),
                 f"controlled-R{k} = diag(1,1,1,exp(2πi/2^{k}))", golden, bloq)


def seal_one_dag(k):
    gate_id = f"cr{k}_dag_gate"
    if k in ALIAS_DAG:
        return {"k": k, "id": gate_id, "status": "ALIAS", "of": ALIAS_DAG[k]}
    golden = ("import numpy as np\n"
              f"# controlled-R{k}-dagger (control=first, big-endian): diag(1,1,1, exp(-2*pi*i/2**{k}))\n"
              f"golden = np.diag([1, 1, 1, np.exp(-2j*np.pi/2**{k})]).astype(complex)")
    bloq = ("from qualtran.bloqs.basic_gates import ZPowGate\n"
            f"bloq = ZPowGate(exponent=-1/2**({k}-1)).controlled()")
    return _seal(k, gate_id, C.crk_dag_sources(k),
                 f"controlled-R{k}† = diag(1,1,1,exp(-2πi/2^{k}))", golden, bloq)


def main():
    args = sys.argv[1:]
    dag = args and args[0] == "dag"
    if dag:
        args = args[1:]
    ks = [int(a) for a in args] or [4]
    fn = seal_one_dag if dag else seal_one
    sym = "†" if dag else " "
    print("=" * 78)
    kind = "CRk† = diag(1,1,1, exp(-2πi/2^k))" if dag else "CRk = diag(1,1,1, exp(2πi/2^k))"
    print(f"controlled-Rk{'†' if dag else ''} 일반화 봉인 ({kind}, key-free proof⊕structural)")
    print("=" * 78)
    ok = 0
    for k in ks:
        r = fn(k)
        if r["status"] == "ALIAS":
            print(f"  ◦ CR{k}{sym} {r['id']:13} = 기존 봉인 {r['of']} (별칭, 재봉인 불요)")
        elif r["status"] == "SEALED":
            ok += 1
            print(f"  ✅ CR{k}{sym} {r['id']:13} SEALED {r['grade']} key={r['key'][:14]}.. anti-swap={'✓' if r['anti_swap_ok'] else '✗'}")
        else:
            print(f"  ❌ CR{k}{sym} {r['id']:13} {r['status']} {r.get('reason','')}")
    n = len([f for f in os.listdir(MODREG) if f.endswith('.sealed.json')])
    print("=" * 78)
    print(f"신규 봉인 {ok} · 라이브러리 모듈 총 {n}")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
