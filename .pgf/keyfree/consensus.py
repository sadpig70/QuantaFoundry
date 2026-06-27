"""consensus.py — KeyFreeConsensus 합의 엔진 (DESIGN-KeyFreeConsensus 구현).

answer-key seed(인간 단일 정답표)를 *독립 출처의 u_hash 수렴*으로 대체한다.
독립성 단위가 핵심(B4 교훈): 같은 weights/도구의 다수 산출은 1 vote로 병합 → 같은 모델이
우연히 합의(B4)해도 정답이 창발하지 않는다.

출처(Source) 종류:
  - model      : LLM 산출 golden (weights_id 별로 1 독립단위)  ← cross-model이라야 ≥2
  - proof      : sympy 등 symbolic 유도 (모델 독립)
  - structural : 진리표/projector 등 대수적 독립 구성

u_hash 는 오라클 verify_seal.hash_unitary 로 계산(공통 측정 도구; 출처 독립성은 golden을 *어떻게
만들었나*에 있지 측정 도구에 있지 않다).
"""
import sys, os
from dataclasses import dataclass, field
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts"))
import verify_seal as vs   # noqa: E402  (오라클 — 사용만; hash_unitary 공통 측정)


def uhash(U) -> str:
    return vs.hash_unitary(np.array(U, dtype=complex))


@dataclass
class Source:
    sid: str
    klass: str          # "model" | "proof" | "structural"
    unit: str           # weights_id(model) | tool(proof) | method(structural)
    u_hash: str


def independence_unit(s: Source) -> str:
    """물리적 독립 단위. 같은 weights·도구는 같은 단위 → 1 vote."""
    return f"{s.klass}:{s.unit}"


def independent_votes(sources):
    """u_hash → 그것을 지지하는 *독립 단위* 집합 (같은 단위 중복 산출은 합쳐짐)."""
    votes = {}
    for s in sources:
        votes.setdefault(s.u_hash, set()).add(independence_unit(s))
    return votes


def effective_independent_count(n_models: int, rho: float) -> float:
    """corpus 상관 할인 (R-I). 같은 weights 가 아니어도 학습 코퍼스가 겹치면 모델끼리 prior(Schelling)
    를 공유한다 — distinct weights 라도 진짜 독립이 아니다. 설문통계의 design-effect/ICC 공식으로
    유효 독립표본수를 환산: N_eff = N / (1 + (N-1)·ρ).  ρ=0 → N_eff=N(상관 없음, 기존 동작),
    ρ=1 → N_eff=1(완전 상관 = 한 출처와 동등)."""
    if n_models <= 0:
        return 0.0
    rho = min(max(float(rho), 0.0), 1.0)
    return n_models / (1.0 + (n_models - 1) * rho)


def confidence_grade(units: set, rho: float = 0.0) -> str:
    """ρ=0(기본): 기존 동작과 byte-identical. ρ>0: model-only 합의에 corpus 상관 할인 적용 —
    유효 독립모델수<2 면 MULTIMODEL→CORPUS_CORRELATED 로 강등(proof/structural 축이나 독립계보
    출처 보강 필요). proof-backed 는 corpus 무관 독립축이므로 할인 없음."""
    has_proof = any(u.startswith("proof:") for u in units)
    n_models = len({u for u in units if u.startswith("model:")})
    if has_proof and len(units) >= 2:
        return "PROOF_BACKED"
    if n_models >= 2:
        if rho > 0 and effective_independent_count(n_models, rho) < 2:
            return "CORPUS_CORRELATED"
        return "MULTIMODEL"
    return "INSUFFICIENT"


@dataclass
class ConsensusResult:
    intent_id: str
    status: str                       # ESTABLISHED | DIVERGENT | CONTESTED | INSUFFICIENT
    key: str = None
    grade: str = None
    provenance: list = field(default_factory=list)
    distribution: dict = field(default_factory=dict)
    escalation: str = ""


def establish_truth(intent_id, sources, N=2, rho=0.0) -> ConsensusResult:
    """독립 출처 ≥N개가 같은 u_hash에 수렴하면 consensus_key 창발. 아니면 escalation.
    rho(기본 0): corpus 상관 할인. ρ=0 이면 기존 동작 byte-identical. ρ>0 이면 model-only 합의가
    corpus 상관으로 유효 독립<2 일 때 ESTABLISHED 대신 INSUFFICIENT(grade=CORPUS_CORRELATED)로 escalate
    — proof/structural 또는 독립계보 출처 보강을 요구."""
    votes = independent_votes(sources)
    dist = {h[:12]: len(u) for h, u in votes.items()}
    if not votes:
        return ConsensusResult(intent_id, "DIVERGENT", escalation="no sources", distribution=dist)
    winner, units = max(votes.items(), key=lambda kv: len(kv[1]))
    w = len(units)
    if w < N:
        return ConsensusResult(intent_id, "DIVERGENT", distribution=dist,
                               escalation=f"max independent agreement {w} < N={N}; "
                                          f"refine intent or add cross-model/proof source")
    # contested near-tie guard (v0.5, R5 실증): top-2 독립단위가 동률이면 plurality 부재 →
    # 어느 쪽을 봉인해도 임의(max() 임의측) → 봉인 거부하고 escalate. 단일-그룹 수렴(runner_up=0)
    # 인 기존 frozen 키 빌드 경로는 발동하지 않음(결정론 불변, verify_contested_guard.py 로 보증).
    runner_up = max((len(u) for h, u in votes.items() if h != winner), default=0)
    if runner_up == w:
        return ConsensusResult(intent_id, "CONTESTED", distribution=dist,
                               escalation=f"top-2 independence tie ({w}={runner_up}); no plurality — "
                                          f"refine intent or add proof/structural tie-breaker")
    grade = confidence_grade(units, rho=rho)
    if grade == "INSUFFICIENT":
        return ConsensusResult(intent_id, "INSUFFICIENT", distribution=dist,
                               escalation="agreement within a single independence unit")
    if grade == "CORPUS_CORRELATED":
        n_models = len({u for u in units if u.startswith("model:")})
        return ConsensusResult(intent_id, "INSUFFICIENT", grade=grade, distribution=dist,
                               escalation=f"models agree but corpus-correlated (ρ={rho}): "
                                          f"N_eff={effective_independent_count(n_models, rho):.2f}<2; "
                                          f"add proof/structural or independent-lineage source")
    return ConsensusResult(intent_id, "ESTABLISHED", key=winner, grade=grade,
                           provenance=sorted(units), distribution=dist)


# ───────────────────────── 독립 출처 생성기 (데모용) ─────────────────────────

def proof_cnot_sympy():
    """sympy 진리표 permutation 으로 CNOT(control=first) golden 독립 유도 (모델 독립)."""
    import sympy as sp
    M = sp.zeros(4, 4)
    for c in (0, 1):
        for t in (0, 1):
            i = 2 * c + t
            j = 2 * c + (t ^ c)      # control=first(MSB): c=1 이면 target 반전
            M[j, i] = 1
    return np.array(M.tolist(), dtype=complex)


def struct_cnot_projector():
    """projector 분해 |0><0|⊗I + |1><1|⊗X 로 CNOT 독립 구성 (proof와 다른 경로)."""
    P0 = np.array([[1, 0], [0, 0]]); P1 = np.array([[0, 0], [0, 1]])
    I = np.eye(2); X = np.array([[0, 1], [1, 0]])
    return (np.kron(P0, I) + np.kron(P1, X)).astype(complex)


def cphase_golden(phase_rad):
    """|11> 에 위상 적용한 cphase golden (E5' 산출 재현용)."""
    d = np.ones(4, dtype=complex); d[3] = np.exp(1j * phase_rad)
    return np.diag(d)


# ── 베이스 8게이트의 *독립 대수* proof 생성기 (직접 정의가 아닌 다른 경로로 유도) ──
_I = np.eye(2, dtype=complex)
_X = np.array([[0, 1], [1, 0]], dtype=complex)
_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
_Z = np.array([[1, 0], [0, -1]], dtype=complex)
_H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
_P0 = np.array([[1, 0], [0, 0]], dtype=complex)
_P1 = np.array([[0, 0], [0, 1]], dtype=complex)


def proof_x():     return _H @ _Z @ _H               # X = H Z H
def proof_z():     return _H @ _X @ _H               # Z = H X H
def proof_h():     return (_X + _Z) / np.sqrt(2)     # H = (X+Z)/√2
def proof_cnot():  return np.kron(_P0, _I) + np.kron(_P1, _X)           # projector 분해
def proof_swap():  return (np.kron(_I, _I) + np.kron(_X, _X)            # SWAP = ½(II+XX+YY+ZZ)
                           + np.kron(_Y, _Y) + np.kron(_Z, _Z)) / 2
def proof_toffoli():                                                    # control=q0,q1; target=q2
    return (np.kron(np.kron(_P0, _I), _I)
            + np.kron(np.kron(_P1, _P0), _I)
            + np.kron(np.kron(_P1, _P1), _X))


def proof_qft(n):                                                       # sympy exact roots of unity
    import sympy as sp
    N = 2 ** n; w = sp.exp(2 * sp.pi * sp.I / N)
    M = sp.Matrix(N, N, lambda i, j: w ** (i * j)) / sp.sqrt(N)
    return np.array(M.evalf(40), dtype=complex)


PROOF_GENERATORS = {
    "x_gate": proof_x, "z_gate": proof_z, "h_gate": proof_h, "cnot": proof_cnot,
    "swap2": proof_swap, "toffoli": proof_toffoli,
    "qft2": lambda: proof_qft(2), "qft3": lambda: proof_qft(3),
}


# ── 신규 unkeyed 게이트: proof(symbolic) + structural(다른 대수 경로) 2독립 출처 ──
def proof_s():   import sympy as sp; return np.diag([1, complex(sp.exp(sp.I * sp.pi / 2))])  # diag(1,i)
def struct_s():  T = np.diag([1, np.exp(1j * np.pi / 4)]); return T @ T                       # S = T²
def proof_t():   import sympy as sp; return np.diag([1, complex(sp.exp(sp.I * sp.pi / 4))])
def struct_t():  return np.diag([1, np.cos(np.pi / 4) + 1j * np.sin(np.pi / 4)])              # Euler 경로
def proof_cz():  return np.diag([1, 1, 1, -1]).astype(complex)
def struct_cz(): IH = np.kron(_I, _H); return IH @ proof_cnot() @ IH                          # CZ=(I⊗H)CX(I⊗H)
def proof_ct():  import sympy as sp; return np.diag([1, 1, 1, complex(sp.exp(sp.I * sp.pi / 4))])  # controlled-T diag
def struct_ct(): T = np.diag([1, np.exp(1j * np.pi / 4)]).astype(complex); return np.kron(_P0, _I) + np.kron(_P1, T)  # |0><0|⊗I + |1><1|⊗T
def proof_csdag():  import sympy as sp; return np.diag([1, 1, 1, complex(sp.exp(-sp.I * sp.pi / 2))])  # controlled-S† diag(1,1,1,-i)
def struct_csdag(): Sd = np.diag([1, -1j]).astype(complex); return np.kron(_P0, _I) + np.kron(_P1, Sd)  # |0><0|⊗I + |1><1|⊗S†

def proof_fredkin():                                    # CSwap perm [0,1,2,3,4,6,5,7]
    M = np.zeros((8, 8), dtype=complex)
    for i, o in enumerate([0, 1, 2, 3, 4, 6, 5, 7]):
        M[o, i] = 1
    return M
def struct_fredkin():                                   # |0><0|⊗I4 + |1><1|⊗SWAP
    SW = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], dtype=complex)
    return np.kron(_P0, np.eye(4)) + np.kron(_P1, SW)

NEW_GATE_SOURCES = {            # gate -> (proof_fn, struct_fn)
    "s_gate": (proof_s, struct_s),
    "t_gate": (proof_t, struct_t),
    "cz":     (proof_cz, struct_cz),
    "ct_gate": (proof_ct, struct_ct),       # controlled-T (control=first): qft3 pipeline 수요
    "cs_dag": (proof_csdag, struct_csdag),  # controlled-S† : QPE inverse-QFT 수요
    "fredkin": (proof_fredkin, struct_fredkin),  # controlled-SWAP: Shor modular-mult 수요
}


# ── controlled-Rk 일반화: CRk = diag(1,1,1, exp(2πi/2^k)) (control=first) ──
#   cz=CR1, cs_gate=CR2, ct_gate=CR3 의 매개변수 통일. proof(sympy 정확)⊕structural(projector 분해).
def proof_crk(k):
    import sympy as sp
    ph = complex(sp.exp(2 * sp.I * sp.pi / (2 ** k)))   # exp(2πi/2^k) 정확
    return np.diag([1, 1, 1, ph]).astype(complex)


def struct_crk(k):
    Rk = np.diag([1, np.exp(2j * np.pi / (2 ** k))]).astype(complex)   # 1q phase
    return np.kron(_P0, _I) + np.kron(_P1, Rk)          # |0><0|⊗I + |1><1|⊗Rk


def crk_sources(k):
    """controlled-Rk 의 2 독립 출처(proof, structural). k는 정수≥1."""
    return [Source(f"cr{k}_proof", "proof", "sympy", uhash(proof_crk(k))),
            Source(f"cr{k}_struct", "structural", "projector", uhash(struct_crk(k)))]


# ── controlled-Rk† 일반화: CRk† = diag(1,1,1, exp(-2πi/2^k)) (inverse-QFT 군 토대) ──
def proof_crk_dag(k):
    import sympy as sp
    ph = complex(sp.exp(-2 * sp.I * sp.pi / (2 ** k)))
    return np.diag([1, 1, 1, ph]).astype(complex)


def struct_crk_dag(k):
    Rk = np.diag([1, np.exp(-2j * np.pi / (2 ** k))]).astype(complex)
    return np.kron(_P0, _I) + np.kron(_P1, Rk)


def crk_dag_sources(k):
    """controlled-Rk† 의 2 독립 출처(proof, structural)."""
    return [Source(f"cr{k}dag_proof", "proof", "sympy", uhash(proof_crk_dag(k))),
            Source(f"cr{k}dag_struct", "structural", "projector", uhash(struct_crk_dag(k)))]


# ── corpus 상관 ρ 추정 (R-I) — "정답이 없는" 의도에서만 깨끗이 추정 가능 ──
def _pairwise_agreement(hashes):
    """한 의도에 대해 distinct 모델들이 낸 u_hash 리스트 → 관측 pairwise 일치율 a∈[0,1]."""
    n = len(hashes)
    if n < 2:
        return None
    agree = tot = 0
    for i in range(n):
        for j in range(i + 1, n):
            tot += 1
            agree += (hashes[i] == hashes[j])
    return agree / tot


def estimate_corpus_rho(intent_hashes, k_defaults=None):
    """corpus 상관계수 ρ 추정 (chance-corrected pairwise agreement = ICC proxy).

    intent_hashes: list[list[str]] — 각 원소는 *한 의도*에 대해 distinct-weights 모델들이 낸 u_hash 들.
        반드시 '정답이 임의/부재한' 의도여야 한다(자유 파라미터 = v0.5 Class C). 정답이 있는 의도는
        '정확성에 의한 수렴'과 'corpus 상관에 의한 수렴'이 혼동되어 ρ 를 과대추정한다(R5c 오염).
    k_defaults: 의도별 그럴듯한 default 개수(이산이면). 우연일치 보정 c=1/k. 연속(자유각)이면 c≈0.
        ρ_i = (a_i - c_i)/(1 - c_i), [0,1] clip. 반환 = 의도 평균 ρ + 진단.
    """
    rows, details = [], []
    for idx, hs in enumerate(intent_hashes):
        a = _pairwise_agreement(hs)
        if a is None:
            continue
        k = (k_defaults[idx] if isinstance(k_defaults, (list, tuple)) else k_defaults)
        c = (1.0 / k) if (k and k > 1) else 0.0
        rho_i = 0.0 if (1 - c) == 0 else max(0.0, min(1.0, (a - c) / (1 - c)))
        rows.append(rho_i)
        details.append({"intent_index": idx, "n_models": len(hs), "observed_agreement": round(a, 4),
                        "chance": round(c, 4), "rho_i": round(rho_i, 4)})
    rho = sum(rows) / len(rows) if rows else 0.0
    return {"rho": round(rho, 4), "n_intents": len(rows), "per_intent": details}
