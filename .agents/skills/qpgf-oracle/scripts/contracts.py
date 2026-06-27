"""contracts.py — QPGF 종료 오라클의 계약 검증 코어.

self-contained·numpy only. qcore(C1~C4 계약강제 런타임)의 검증 로직을 스킬
번들로 이식한 것이며, Qualtran `tensor_contract()` 출력의 endianness 정렬
(big-endian → qcore little-endian)을 강제하는 정렬 계층을 추가로 둔다.

4대 계약 (qcore와 동일 정의):
  C1 FullCharacterization : 완전기저 유니터리 보유 (차원 = 2^(n_sys+n_anc))
  C2 PhasePreserved       : 복소 유니터리성 U†U=I (위상/진폭 보존, 확률붕괴 금지)
  C3 AncillaClean         : 입력 anc=|0> → 출력 anc=|0> (누출 0), 유효 V 추출
  C4 ComposableContract   : (golden 또는 합성) 명세와 유효 유니터리 일치 재검증

설계 근거: PortPoC(HANDOFF §8) — Qualtran은 첫 레지스터가 MSB(big-endian),
qcore는 q0이 LSB(little-endian). 비대칭 다중큐비트 게이트(CNOT·Toffoli)에서만
드러나고 대칭 게이트(CZ)는 무차별이라, *항상* 비트순서 반전을 적용해야
hash_unitary 결정론과 golden 대조가 일관되게 성립한다.
"""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass, field

ATOL = 1e-9  # 완전특성화 환경: 수치 허용오차는 엄격하게 (qcore와 동일)


class ContractViolation(Exception):
    """계약 위반 = 검증 거부."""


# ── endianness 정렬 계층 (Qualtran ↔ qcore) ───────────────────────
def reverse_qubit_order(U: np.ndarray, n: int) -> np.ndarray:
    """큐비트 비트순서를 반전해 basis를 재배열.

    Qualtran tensor_contract(big-endian: 첫 레지스터=MSB) 출력을 qcore
    컨벤션(little-endian: q0=LSB)으로 옮긴다. 대칭 게이트는 불변이지만
    비대칭 게이트(CNOT/Toffoli)는 이 변환이 없으면 봉인이 깨진다(HANDOFF §8).
    """
    dim = 1 << n
    if U.shape != (dim, dim):
        raise ContractViolation(
            f"reverse_qubit_order: U.shape {U.shape} != ({dim},{dim}) for n={n}")
    perm = [int(format(i, f"0{n}b")[::-1], 2) for i in range(dim)]
    return U[np.ix_(perm, perm)]


def embed_unitary(U: np.ndarray, targets: list[int], n: int) -> np.ndarray:
    """k큐비트 유니터리 U를 n큐비트 레지스터의 명시적 target 와이어에 배치(나머지=항등).

    이종 인터페이스 합성용: 2큐비트 모듈을 3큐비트 앱의 특정 와이어에 올린다.
    컨벤션 = Qualtran-native raw big-endian (와이어 w의 가중치 = 2^(n-1-w),
    qubit 0 = MSB). targets는 **연산자 큐비트 순서** → U의 qubit j = targets[j].

    결정론·위조방지: targets는 **명시 지정만**(자동선택 금지). U가 유니터리면
    결과도 유니터리(U⊗I의 순열켤레)라 INV3 재유니터리성은 자동 보존된다.
    """
    k = len(targets)
    if U.shape != (1 << k, 1 << k):
        raise ContractViolation(
            f"embed_unitary: U.shape {U.shape} != ({1<<k},{1<<k}) for k={k}")
    if len(set(targets)) != k or any(w < 0 or w >= n for w in targets):
        raise ContractViolation(
            f"embed_unitary: targets {targets} 비유효 (중복/범위초과, n={n})")
    others = [w for w in range(n) if w not in targets]
    dim = 1 << n

    def bit(idx, w):              # big-endian: 와이어 w의 비트
        return (idx >> (n - 1 - w)) & 1

    def sub(idx):                 # target 와이어들 → U 부분인덱스 (연산자 순서)
        s = 0
        for w in targets:
            s = (s << 1) | bit(idx, w)
        return s

    full = np.zeros((dim, dim), dtype=complex)
    for r in range(dim):
        for c in range(dim):
            if any(bit(r, w) != bit(c, w) for w in others):
                continue          # 비대상 와이어는 항등
            full[r, c] = U[sub(r), sub(c)]
    return full


# ── 계약 검증 결과 ────────────────────────────────────────────────
@dataclass
class ContractResult:
    """run_contracts의 구조화 산출. 통과 시 V(유효 시스템 유니터리)를 담는다.

    signal: 자율 루프가 다음 수정에 쓰는 구조화 실패신호(또는 통과신호).
            {"contract": "C2", "reason": "...", "detail": {...}} 형식.
    """
    all_passed: bool
    V: np.ndarray | None = None
    signal: dict = field(default_factory=dict)


# ── C1+C2: 완전특성화 + 유니터리성(위상 보존) ─────────────────────
def check_c1_c2(U: np.ndarray, n_total: int, name: str) -> None:
    """차원(C1) + 유니터리성(C1/C2). 위반 시 ContractViolation."""
    dim = 2 ** n_total
    if U.shape != (dim, dim):
        raise ContractViolation(
            f"[{name}] C1 위반: 차원 {U.shape} != ({dim},{dim}) — 완전특성화 아님")
    if not np.allclose(U.conj().T @ U, np.eye(dim), atol=ATOL):
        raise ContractViolation(
            f"[{name}] C1/C2 위반: 비유니터리 (위상/완전성 손상)")


# ── C3: 보조큐비트 청정성 + 유효 시스템 유니터리 V 추출 ───────────
def check_c3_extract(U: np.ndarray, n_sys: int, n_anc: int, name: str) -> np.ndarray:
    """입력 anc=|0> 열이 출력 anc=|0> 행에만 지지하는지 검증하고 V 추출.

    인덱싱은 qcore와 동일: 시스템이 하위 비트(0..n_sys-1), 보조가 상위
    (n_sys..). anc=0 입력/출력 인덱스 = [0, 2^n_sys).
    """
    if n_anc == 0:
        return U  # 보조 없음 → 시스템 유니터리 = U

    d_sys = 2 ** n_sys
    in_cols = np.arange(d_sys)        # ancilla |0> 입력 열
    block = U[:, in_cols]             # (dim, d_sys)
    out_anc0 = block[:d_sys, :]       # ancilla |0> 출력 (d_sys, d_sys)
    out_other = block[d_sys:, :]      # ancilla != |0> 누출

    leak = np.linalg.norm(out_other)
    if leak > ATOL:
        raise ContractViolation(
            f"[{name}] C3 위반: 보조큐비트 누출 ‖leak‖={leak:.2e} "
            f"(uncompute 실패 또는 잔류 얽힘)")
    if not np.allclose(out_anc0.conj().T @ out_anc0, np.eye(d_sys), atol=ATOL):
        raise ContractViolation(
            f"[{name}] C3 위반: 유효 시스템 작용이 비유니터리")
    return out_anc0


# ── C3-iso: alloc ancilla 비정방 모듈 (isometry 계약) ──────────────
def check_isometry(V: np.ndarray, n_in: int, n_alloc: int, name: str) -> np.ndarray:
    """alloc ancilla로 비정방이 된 모듈을 isometry로 검증: V†V = I_{2^n_in}.

    Qualtran raw big-endian에서 RIGHT(alloc) 레지스터는 |0>으로 태어나 계산된다
    (예: And — target 큐비트 alloc). tensor_contract는 (2^(n_in+n_alloc), 2^n_in)
    비정방 isometry를 준다. V†V=I 는 **충실한 임베딩**(노름·내적 보존, 정보손실
    0, ancilla가 결정적 값을 가짐) = 정방 유니터리성의 isometry 일반화.

    경계: 이는 *생성(alloc)* 측 계약이다. uncompute(free) 측은 별도 봉인모듈이며,
    둘의 합성이 시스템 항등으로 복귀하는지는 합성 재검증(INV3)의 몫(향후).
    """
    d_in = 1 << n_in
    d_out = 1 << (n_in + n_alloc)
    if V.shape != (d_out, d_in):
        raise ContractViolation(
            f"[{name}] C1 차원: isometry V.shape {V.shape} != ({d_out},{d_in}) "
            f"(n_in={n_in}, n_alloc={n_alloc})")
    if not np.allclose(V.conj().T @ V, np.eye(d_in), atol=ATOL):
        raise ContractViolation(
            f"[{name}] C3iso 위반: V†V≠I (비충실 임베딩 — 노름 비보존/잔류 얽힘)")
    return V


def run_contracts_iso(V: np.ndarray, n_in: int, n_alloc: int, *,
                      golden: np.ndarray | None = None,
                      name: str = "module") -> ContractResult:
    """비정방(alloc ancilla) 모듈에 C1(차원)+C3iso(isometry)+C4(golden) 적용.

    정방 경로(run_contracts)와 분리된 가산 경로. raw big-endian 정본만.
    """
    try:
        check_isometry(V, n_in, n_alloc, name)
        if golden is not None and not matches_golden(V, golden):
            raise ContractViolation(f"[{name}] C4 위반: golden 명세 불일치")
    except ContractViolation as e:
        msg = str(e)
        contract = classify_contract(msg)
        extra = {}
        if contract == "C4" and golden is not None:
            extra["norm_delta"] = golden_delta(V, golden)
        return ContractResult(False, None, build_signal(contract, msg, **extra))
    return ContractResult(True, V, {"contract": "C1-C4(iso)", "reason": "all_passed"})


# ── C4(부분): golden 명세 대조 (전역위상 무시) ─────────────────────
def _norm_phase(M: np.ndarray) -> np.ndarray:
    """전역위상 정규화: 첫 비영 원소의 위상을 0으로."""
    flat = M.flatten()
    k = int(np.argmax(np.abs(flat) > ATOL))
    return M * np.exp(-1j * np.angle(flat[k]))


def matches_golden(V: np.ndarray, golden: np.ndarray, atol: float = 1e-7) -> bool:
    """유효 유니터리 V가 해석적 명세(golden)와 일치하는가 (전역위상 무시).

    rtol=0: np.allclose 기본 rtol(1e-5)이 atol(1e-7)을 가려 실효 허용오차가 ~1e-5가 되는
    문제를 차단(리뷰 반영). 절대 허용오차 atol만 적용 → 명시된 민감도가 실제로 성립.
    """
    return V.shape == golden.shape and np.allclose(
        _norm_phase(V), _norm_phase(golden), atol=atol, rtol=0)


def golden_delta(V: np.ndarray, golden: np.ndarray) -> float:
    """V와 golden의 거리 (전역위상 무시 최대원소 차). fix-loop 신호(norm_delta)용."""
    if V.shape != golden.shape:
        return float("inf")
    return float(np.max(np.abs(_norm_phase(V) - _norm_phase(golden))))


# ── 신호 분류(taxonomy) — R4 자율 fix-loop 해석 강화 (리뷰 반영) ──
_TAXONOMY = {
    "C1":    ("dimension_mismatch", "차원이 2^(n_sys+n_anc)과 불일치 — meta의 n_sys/n_anc 또는 bloq 큐비트 수 확인"),
    "C2":    ("non_unitary", "U†U≠I — bloq가 유니터리가 아님(게이트 분해/정규화 확인)"),
    "C3":    ("ancilla_leak", "보조큐비트가 |0>으로 복귀 안 함(uncompute 누락/잔류 얽힘)"),
    "C3iso": ("isometry_non_faithful", "V†V≠I — alloc isometry 비충실(노름 비보존)"),
    "C4":    ("golden_mismatch", "tensor_contract가 golden과 불일치 — 엔디안(big-endian)·게이트 순서·위상 각도 확인"),
    "C?":    ("unknown", "분류되지 않은 계약 위반"),
}


def classify_contract(msg: str) -> str:
    """위반 메시지 → 계약 분류. 'C1/C2 비유니터리'는 C2(non_unitary)로 정확 분류."""
    if "C1/C2" in msg:          # check_c1_c2의 유니터리성 위반 = C2 의미
        return "C2"
    for c in ("C3iso", "C4", "C3", "C1"):   # 구체적 먼저 (C3iso ⊃ C3)
        if c in msg:
            return c
    return "C?"


def build_signal(contract: str, msg: str, **extra) -> dict:
    """구조화 위반 신호: contract + reason_code + reason + fix_hint (+ norm_delta 등)."""
    code, hint = _TAXONOMY.get(contract, _TAXONOMY["C?"])
    sig = {"contract": contract, "reason_code": code, "reason": msg, "fix_hint": hint}
    sig.update(extra)
    return sig


# ── 오케스트레이터: C1~C4 일괄 (verify_seal.py가 호출) ────────────
def run_contracts(U: np.ndarray, n_sys: int, n_anc: int = 0, *,
                  golden: np.ndarray | None = None,
                  align: str = "raw",
                  name: str = "module") -> ContractResult:
    """단일 모듈 유니터리에 C1~C4를 exact 적용.

    align — 입력 유니터리의 비트순서 정렬 모드 (DESIGN-OracleSkill-Impl §0):
      "raw"     : 변환 없음. **봉인 정본 컨벤션**(Qualtran tensor_contract big-endian).
      "reverse" : reverse_qubit_order 선적용. qcore-legacy golden(little-endian) 호환 전용.
    통과 시 V를 담은 ContractResult(all_passed=True), 위반 시 all_passed=False + 구조화 signal.
    """
    n_total = n_sys + n_anc
    V = None
    try:
        if align == "reverse":
            U = reverse_qubit_order(U, n_total)
        elif align != "raw":
            raise ContractViolation(f"[{name}] 알 수 없는 align='{align}' (raw|reverse)")
        check_c1_c2(U, n_total, name)
        V = check_c3_extract(U, n_sys, n_anc, name)
        if golden is not None and not matches_golden(V, golden):
            raise ContractViolation(f"[{name}] C4 위반: golden 명세 불일치")
    except ContractViolation as e:
        msg = str(e)
        contract = classify_contract(msg)
        extra = {}
        if contract == "C4" and golden is not None and isinstance(V, np.ndarray):
            extra["norm_delta"] = golden_delta(V, golden)   # golden과의 실제 거리
        return ContractResult(False, None, build_signal(contract, msg, **extra))
    return ContractResult(True, V, {"contract": "C1-C4", "reason": "all_passed"})


# ── C4(합성): 검증된 두 모듈의 유효 유니터리 합성 + 재검증 ────────
def compose(V_first: np.ndarray, V_second: np.ndarray, name: str = "compose"
            ) -> np.ndarray:
    """self 다음 other 적용 (시스템 레벨 합성 = 행렬곱, 위상 포함). 재검증.

    qcore.QModule.then 이식. 차원 불일치(인터페이스 비호환)는 C4 위반.
    """
    if V_first.shape != V_second.shape:
        raise ContractViolation(
            f"[{name}] C4 인터페이스 불일치: {V_first.shape} -> {V_second.shape}")
    V = V_second @ V_first
    dim = V.shape[0]
    if not np.allclose(V.conj().T @ V, np.eye(dim), atol=ATOL):
        raise ContractViolation(f"[{name}] C4 위반: 합성 결과 비유니터리")
    return V
