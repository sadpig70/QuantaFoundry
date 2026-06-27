"""verify_seal.py — QPGF 종료 오라클 (무프로세스 스킬 스크립트).

사용:  python verify_seal.py <spec.pg> [--out DIR]
  통과 → <id>.sealed.json 생성 + exit 0   (루프 종료 신호)
  실패 → sealed 미생성 + stderr 구조화 signal + exit 1   (루프 계속 신호)

봉인권은 호출 경로가 아니라 "결정론 검증코드 + 위조불가 서명"에서 온다
(DESIGN-QPGF-Runtime-Portability §6). 정본 컨벤션 = Qualtran-native raw
tensor_contract 출력(big-endian), n_anc=0 (DESIGN-OracleSkill-Impl §0).
"""
from __future__ import annotations

# ── BLASGuard: 부동소수 누적순서 비결정성 차단 (import 전에 고정) ──
import os
for _v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")

import sys
import re
import json
import hashlib
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from contracts import run_contracts, run_contracts_iso, ATOL, ContractViolation  # noqa: E402

QUANT = 1e-9    # 해시 양자화 격자 (ATOL과 동급)
_PREQUANT = 12  # 사전 반올림 소수자리 (BLAS 잡음 흡수, QUANT보다 미세 — 격자 반경계 안정화)
RESOURCE_SCHEMA_VERSION = "qec-gates-cost-v1"  # 자원회계 스키마 버전 (cost 모델 변경 추적, 서명결합)


# ── 스펙 모델 ─────────────────────────────────────────────────────
class Spec:
    def __init__(self, id, n_sys, n_anc, bloq_src, golden_src, tier=None):
        self.id = id
        self.n_sys = n_sys
        self.n_anc = n_anc
        self.bloq_src = bloq_src
        self.golden_src = golden_src
        self.tier = tier        # None=자동(정방 dense/isometry) · "clifford"=Tier-2 tableau


_FENCE = re.compile(r"```(?:[\w.+-]+)?\s+id=([\w.-]+)\s*\n(.*?)```", re.DOTALL)


def _extract_blocks(text: str) -> dict:
    """라벨된 fenced code block 추출 (parser-free PG의 기계추출 규약)."""
    return {m.group(1): m.group(2) for m in _FENCE.finditer(text)}


def load_pg_spec(path: str) -> Spec:
    """.pg 명세에서 bloq/golden/meta 블록을 결정론 추출 (AI 해석 아님)."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    blocks = _extract_blocks(text)
    if "bloq" not in blocks:
        raise ContractViolation("spec에 ```... id=bloq``` 블록 없음")
    if "meta" not in blocks:
        raise ContractViolation("spec에 ```json id=meta``` 블록 없음")
    meta = json.loads(blocks["meta"])
    n_anc = int(meta.get("n_anc", 0))
    if n_anc < 0:
        raise ContractViolation(f"n_anc는 음수 불가 (got {n_anc})")
    # n_anc>0: alloc ancilla(비정방 isometry) 경로로 봉인. main()이 shape 정합 검증.
    tier = meta.get("tier")
    if tier not in (None, "clifford", "clifford+t"):
        raise ContractViolation(f"알 수 없는 tier='{tier}' (None|clifford|clifford+t)")
    return Spec(id=str(meta["id"]), n_sys=int(meta["n_sys"]), n_anc=n_anc,
                bloq_src=blocks["bloq"], golden_src=blocks.get("golden"), tier=tier)


def instantiate(src: str, want: str):
    """제한 네임스페이스에서 src를 exec하고 want 변수 반환.
    신뢰실행 가정(번들 무결성은 해시고정으로 별도 보장, 설계 §6)."""
    ns = {"np": np}
    exec(src, ns)
    if want not in ns:
        raise ContractViolation(f"spec src에 `{want}` 정의 없음")
    return ns[want]


# ── 결정론 서명층 (DetSig) ───────────────────────────────────────
def _norm_phase(M: np.ndarray) -> np.ndarray:
    """전역위상 제거: 첫 비영원소의 위상을 0으로."""
    flat = M.flatten()
    k = int(np.argmax(np.abs(flat) > ATOL))
    return M * np.exp(-1j * np.angle(flat[k]))


def hash_unitary(U: np.ndarray) -> str:
    """위상정규화 → 격자 양자화 → 정준바이트 → sha256. 부동소수 비결정성 차단.

    - 전역위상만 다른 U → 동일 해시 (위상 자유도 흡수)
    - 부동소수 잡음 ≤ QUANT/2 → 동일 해시 (양자화)
    """
    Un = _norm_phase(np.asarray(U, dtype=complex))
    # 격자 반경계 안정화(리뷰 P1-QUANT): BLAS 누적순서 잡음(~1e-15)을 QUANT(1e-9)보다 충분히
    # 미세한 격자(1e-12)로 사전 반올림해 흡수 → 두 런타임이 격자 반경계(±QUANT/2)를 갈라 밟을
    # 위험 차단. 구조적 유니터리(0,±1,±1/√2,…)는 경계에서 멀어 결과(정수) 불변 → 기존 해시 보존.
    re = np.round(Un.real, _PREQUANT)
    im = np.round(Un.imag, _PREQUANT)
    qre = np.round(re / QUANT).astype(np.int64)
    qim = np.round(im / QUANT).astype(np.int64)
    h = hashlib.sha256()
    h.update(repr(Un.shape).encode())
    h.update(qre.tobytes())
    h.update(qim.tobytes())
    return h.hexdigest()


def _canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


_FP_CACHE: dict = {}


def oracle_fingerprint() -> dict:
    """오라클 코드 지문 (결정론): verify_seal.py·contracts.py의 sha256.

    ★ 환경 의존이 아닌 *코드* 해시 → 같은 스킬 번들이면 머신 무관 동일(byte-identical 보존).
    봉인 서명에 결합해 '변조된 verify_seal이 만든 봉인'을 코드해시 불일치로 탐지(P0-TRUST).
    """
    if not _FP_CACHE:
        here = os.path.dirname(os.path.abspath(__file__))

        def _fh(name):
            with open(os.path.join(here, name), "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()
        _FP_CACHE["oracle_code_hash"] = _fh("verify_seal.py")
        _FP_CACHE["contracts_code_hash"] = _fh("contracts.py")
        _FP_CACHE["resource_schema_version"] = RESOURCE_SCHEMA_VERSION
    return dict(_FP_CACHE)


def sig_from_fields(spec_id: str, u_hash: str, resource: dict, atol: float,
                    provenance: dict | None = None) -> str:
    """봉인 서명 = 정준 JSON(키정렬) over (id,u_hash,resource,atol[,provenance])의 sha256.
    sealed.json 필드만으로 재계산 가능 → Registry가 V 없이 무결성 재검증.
    provenance(코드지문)가 주어지면 서명에 결합 → 코드 무결성까지 변조탐지."""
    body = {"id": spec_id, "u_hash": u_hash, "resource": resource, "atol": atol}
    if provenance:
        body["provenance"] = provenance
    return hashlib.sha256(_canonical(body)).hexdigest()


def finalize_sealed(sealed: dict) -> dict:
    """봉인 dict에 코드지문 필드 결합 + 서명 계산 (모든 봉인 경로의 단일 종결점).

    oracle_code_hash·contracts_code_hash를 sealed에 기록하고, 그 둘을 포함해 sig를 산출.
    환경 의존 필드(platform·버전)는 결정론을 깨므로 여기 넣지 않는다(사이드카 분리)."""
    fp = oracle_fingerprint()
    sealed["oracle_code_hash"] = fp["oracle_code_hash"]
    sealed["contracts_code_hash"] = fp["contracts_code_hash"]
    sealed["resource_schema_version"] = fp["resource_schema_version"]
    sealed["sig"] = sig_from_fields(sealed["id"], sealed["u_hash"],
                                    sealed["resource"], sealed["atol"], provenance=fp)
    return sealed


def deterministic_sig(U, resource: dict, atol: float, spec_id: str) -> str:
    """봉인 서명 (U로부터). 같은 입력·같은 번들 → 같은 sig (변조탐지)."""
    return sig_from_fields(spec_id, hash_unitary(U), resource, atol,
                           provenance=oracle_fingerprint())


def serialize_cost(gc) -> dict:
    """QECGatesCost GateCounts → 결정론 dict (키정렬 + total_t)."""
    d = dict(sorted(gc.asdict().items()))
    try:
        d["total_t"] = int(gc.total_t_count())
    except Exception:
        pass
    return d


# ── I/O ──────────────────────────────────────────────────────────
def emit_signal(payload: dict) -> None:
    """루프가 읽는 구조화 신호 (stderr)."""
    sys.stderr.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def write_sealed_json(spec: Spec, V, cost: dict, out_dir: str,
                      contract: str = "C1-C4") -> str:
    sealed = finalize_sealed({
        "id": spec.id,
        "sealed": True,
        "convention": "qualtran-raw",
        "n_sys": spec.n_sys,
        "n_anc": spec.n_anc,
        "contract": contract,
        "atol": ATOL,
        "u_hash": hash_unitary(V),
        "resource": cost,
    })
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{spec.id}.sealed.json")
    # 결정론·byte-identical: 타임스탬프 없음, 키정렬, 고정 indent.
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(sealed, ensure_ascii=False, sort_keys=True, indent=2))
        f.write("\n")
    return path


def write_provenance(spec_id: str, out_dir: str) -> str:
    """환경·코드 지문 사이드카(`<id>.provenance.json`) — tamper-evidence 강화·재현 추적.

    ★ sealed.json/sig와 **분리** 기록한다. 환경 의존 필드(platform·버전)는 머신마다 다르므로
    봉인의 결정론 byte-identical(Forge·R4 입증)을 깨지 않도록 서명에서 제외(통합수정설계 P0-TRUST).
    검증자는 oracle_code_hash로 verify_seal/contracts 무결성을 교차확인할 수 있다.
    """
    import platform
    prov = {
        "id": spec_id,
        **oracle_fingerprint(),            # 코드해시(서명에도 결합됨) — 사이드카에도 기록
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "registry_recompute_required": True,
        "note": "환경 의존 — sealed.json/sig와 분리. 봉인 무결성은 중앙 재계산 조건부.",
    }
    try:
        prov["numpy_version"] = __import__("numpy").__version__
    except Exception:
        pass
    try:
        import importlib.metadata as _md
        prov["qualtran_version"] = _md.version("qualtran")
    except Exception:
        pass
    path = os.path.join(out_dir, f"{spec_id}.provenance.json")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(prov, ensure_ascii=False, sort_keys=True, indent=2))
        f.write("\n")
    return path


# ── 단계(stage) 실패 신호 분류 (계약 이전 단계 — R4 fix-loop 해석용) ──
_STAGE_HINT = {
    "spec_load_fail":   ".pg 형식 확인 — bloq/meta 블록 누락, JSON 오류, n_anc 음수 등",
    "instantiate_fail": "bloq 파이썬 코드 오류 — import/생성자/레지스터 인자 확인",
    "golden_fail":      "golden 파이썬 코드 오류 — numpy 구성식/shape 확인",
    "cost_fail":        "QECGatesCost 산출 실패 — bloq가 자원회계 가능한 형태인지 확인",
    "usage":            "사용법: verify_seal.py <spec.pg> [--out DIR]",
}


def _stage_signal(code: str, detail: str = "") -> dict:
    return {"terminate": False, "reason_code": code,
            "reason": f"{code}:{detail}" if detail else code,
            "fix_hint": _STAGE_HINT.get(code, "")}


_CLIFFORD_ADVISORY_BOUND = 10   # 이하 큐비트는 dense 일치 advisory 교차검증


def _seal_clifford(spec: "Spec", bloq, out_dir: str) -> int:
    """Tier-2 Clifford 봉인: 정준 stabilizer tableau 해시(dense 미사용)로 임의 크기 정확 봉인."""
    import clifford_seal as cs
    ok, why = cs.is_clifford(bloq)
    if not ok:
        emit_signal({"terminate": False, "reason_code": "non_clifford", "reason": why,
                     "fix_hint": "tier=clifford는 Clifford 게이트(H·S·CNOT·CZ·X·Y·Z·SWAP)만 — "
                                 "T/Toffoli 포함 회로는 tier 생략(소규모 dense) 또는 Tier-3 후속"})
        return 1
    try:
        u_hash, n = cs.canonical_tableau_hash(bloq)
    except Exception as e:
        emit_signal(_stage_signal("instantiate_fail", f"tableau:{e}"))
        return 1
    if n != spec.n_sys:
        emit_signal({"terminate": False, "reason_code": "dimension_mismatch",
                     "reason": f"회로 큐비트 {n} ≠ n_sys {spec.n_sys}", "fix_hint": "meta n_sys 확인"})
        return 1
    # advisory(소규모): cirq dense == qualtran tensor_contract (변환 충실성 확인)
    if spec.n_sys <= _CLIFFORD_ADVISORY_BOUND:
        try:
            from contracts import matches_golden
            if not matches_golden(cs.dense_unitary(bloq), np.asarray(bloq.tensor_contract())):
                emit_signal({"terminate": False, "reason_code": "clifford_advisory_mismatch",
                             "reason": "cirq dense ≠ tensor_contract", "fix_hint": "변환 불일치"})
                return 1
        except Exception:
            pass   # advisory 실패는 비차단(대형/추출불가)
    try:
        from qualtran.resource_counting import get_cost_value, QECGatesCost
        cost = serialize_cost(get_cost_value(bloq, QECGatesCost()))
    except Exception as e:
        emit_signal(_stage_signal("cost_fail", str(e)))
        return 1
    sealed = finalize_sealed({
        "id": spec.id, "sealed": True, "convention": "qualtran-raw",
        "n_sys": spec.n_sys, "n_anc": 0, "contract": "C1-C4(clifford)", "tier": 2,
        "atol": ATOL, "u_hash": u_hash, "resource": cost,
    })
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{spec.id}.sealed.json")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(sealed, ensure_ascii=False, sort_keys=True, indent=2))
        f.write("\n")
    write_provenance(spec.id, out_dir)
    sys.stdout.write(f"sealed: {path}\n")
    return 0


def _seal_clifford_t(spec: "Spec", bloq, out_dir: str) -> int:
    """Tier-3 Clifford+T 봉인: bloq ≡ golden 참조회로를 ZX로 증명(dense 없음, sound)."""
    import zx_seal as zs
    if not spec.golden_src or not spec.golden_src.strip():
        emit_signal({"terminate": False, "reason_code": "golden_circuit_missing",
                     "reason": "tier=clifford+t는 golden 참조회로(cirq.Circuit) 필수",
                     "fix_hint": "golden 블록에 `import cirq; golden = cirq.Circuit(...)` 독립 참조회로"})
        return 1
    try:
        golden_circ = instantiate(spec.golden_src, "golden")   # cirq.Circuit 기대
    except Exception as e:
        emit_signal(_stage_signal("golden_fail", str(e)))
        return 1
    ok, why, u_hash, n = zs.verify_equivalent(bloq, golden_circ)
    if not ok:
        emit_signal({"terminate": False, "reason_code": "zx_not_equivalent", "reason": why,
                     "fix_hint": "bloq가 golden 참조회로와 ZX-등가가 아님(또는 비-Clifford+T/미환원). "
                                 "게이트 분해·순서 재검토 또는 소규모는 tier 생략(dense)"})
        return 1
    if n is not None and n != spec.n_sys:
        emit_signal({"terminate": False, "reason_code": "dimension_mismatch",
                     "reason": f"회로 큐비트 {n} ≠ n_sys {spec.n_sys}", "fix_hint": "meta n_sys 확인"})
        return 1
    try:
        from qualtran.resource_counting import get_cost_value, QECGatesCost
        cost = serialize_cost(get_cost_value(bloq, QECGatesCost()))
    except Exception as e:
        emit_signal(_stage_signal("cost_fail", str(e)))
        return 1
    sealed = finalize_sealed({
        "id": spec.id, "sealed": True, "convention": "qualtran-raw",
        "n_sys": spec.n_sys, "n_anc": 0, "contract": "C1-C4(zx)", "tier": 3,
        "atol": ATOL, "u_hash": u_hash, "resource": cost,
    })
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{spec.id}.sealed.json")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(sealed, ensure_ascii=False, sort_keys=True, indent=2))
        f.write("\n")
    write_provenance(spec.id, out_dir)
    sys.stdout.write(f"sealed: {path}\n")
    return 0


# ── main: 종료 계약 (exit 0 ⟺ sealed) ────────────────────────────
def main(argv) -> int:
    if not argv:
        emit_signal(_stage_signal("usage"))
        return 1
    spec_path = argv[0]
    out_dir = "."
    if "--out" in argv:
        out_dir = argv[argv.index("--out") + 1]

    try:
        spec = load_pg_spec(spec_path)
    except Exception as e:
        emit_signal(_stage_signal("spec_load_fail", str(e)))
        return 1

    try:
        bloq = instantiate(spec.bloq_src, "bloq")
    except Exception as e:
        emit_signal(_stage_signal("instantiate_fail", str(e)))
        return 1

    # ── Tier-2/3: 기호 봉인 (dense 미사용 → 대형 회로 탈출) ──
    if spec.tier == "clifford":
        return _seal_clifford(spec, bloq, out_dir)
    if spec.tier == "clifford+t":
        return _seal_clifford_t(spec, bloq, out_dir)

    try:
        U = np.asarray(bloq.tensor_contract())       # raw, big-endian (정본)
    except Exception as e:
        emit_signal(_stage_signal("instantiate_fail", str(e)))
        return 1

    golden = None
    if spec.golden_src:
        try:
            golden = np.asarray(instantiate(spec.golden_src, "golden"), dtype=complex)
        except Exception as e:
            emit_signal(_stage_signal("golden_fail", str(e)))
            return 1

    # 정방(유니터리) vs 비정방(alloc ancilla isometry) 라우팅. 정본=raw big-endian.
    if U.shape[0] == U.shape[1]:
        res = run_contracts(U, spec.n_sys, spec.n_anc, golden=golden,
                            align="raw", name=spec.id)
        contract_label = "C1-C4"
    else:
        res = run_contracts_iso(U, spec.n_sys, spec.n_anc, golden=golden,
                                name=spec.id)
        contract_label = "C1-C4(iso)"
    if not res.all_passed:
        emit_signal({"terminate": False, "signal": res.signal})
        return 1

    try:
        from qualtran.resource_counting import get_cost_value, QECGatesCost
        cost = serialize_cost(get_cost_value(bloq, QECGatesCost()))
    except Exception as e:
        emit_signal(_stage_signal("cost_fail", str(e)))
        return 1

    path = write_sealed_json(spec, res.V, cost, out_dir, contract=contract_label)
    write_provenance(spec.id, out_dir)   # 사이드카(분리) — sealed.json 결정론 불변
    sys.stdout.write(f"sealed: {path}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
