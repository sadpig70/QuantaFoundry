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


def confidence_grade(units: set) -> str:
    has_proof = any(u.startswith("proof:") for u in units)
    n_models = len({u for u in units if u.startswith("model:")})
    if has_proof and len(units) >= 2:
        return "PROOF_BACKED"
    if n_models >= 2:
        return "MULTIMODEL"
    return "INSUFFICIENT"


@dataclass
class ConsensusResult:
    intent_id: str
    status: str                       # ESTABLISHED | DIVERGENT | INSUFFICIENT
    key: str = None
    grade: str = None
    provenance: list = field(default_factory=list)
    distribution: dict = field(default_factory=dict)
    escalation: str = ""


def establish_truth(intent_id, sources, N=2) -> ConsensusResult:
    """독립 출처 ≥N개가 같은 u_hash에 수렴하면 consensus_key 창발. 아니면 escalation."""
    votes = independent_votes(sources)
    dist = {h[:12]: len(u) for h, u in votes.items()}
    if not votes:
        return ConsensusResult(intent_id, "DIVERGENT", escalation="no sources", distribution=dist)
    winner, units = max(votes.items(), key=lambda kv: len(kv[1]))
    if len(units) < N:
        return ConsensusResult(intent_id, "DIVERGENT", distribution=dist,
                               escalation=f"max independent agreement {len(units)} < N={N}; "
                                          f"refine intent or add cross-model/proof source")
    grade = confidence_grade(units)
    if grade == "INSUFFICIENT":
        return ConsensusResult(intent_id, "INSUFFICIENT", distribution=dist,
                               escalation="agreement within a single independence unit")
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
