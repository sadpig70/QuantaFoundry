"""app_assemble.py — 고수준 양자 앱 분해·검증 어셈블리 (결정론, 재귀, Seal Tier).

앱 매니페스트(app_meta + plan [+ app_golden])를 받아 서브모듈을 봉인·합성·봉인한다.
plan의 step은 리프 모듈({"spec": "x.pg"}) 또는 sub-app({"app": "x.app.pg"}, 재귀).

★ Seal Tier (통합수정설계 v1.1 §5 — 7리뷰 수렴 SmallNBound 탈출):
  - Tier-0 EXACT     : dense V_app 재실체화 → C-app(==app_golden) → u_hash=hash_unitary(V_app).
                       소규모(n_sys≤EXACT_BOUND)·golden 존재·모든 자식 dense일 때. (정본 dense 봉인)
  - Tier-1 STRUCTURAL: dense 미실체화. app_u_hash = sha256(자식 u_hash + 합성구조)(Merkle).
                       correct-by-construction(자식 sealed[INV2] + 인터페이스 정합[INV-IFACE]).
                       → **규모 무관**(작은 폭 리프의 큰 트리도 봉인). 자식이 옳고 합성이 well-formed면
                       그 합성은 *계획된 합성*과 정의상 일치. golden+소규모면 dense advisory 교차검증.
  - ADVISORY(확률 등)는 seal 아님(INV-TIER) — 본 모듈은 결정론 tier만 봉인.

tier 전파: Tier-1 봉인은 부모에 dense V를 노출하지 않는다(V=None) → 구조적 자식을 가진 부모도
구조적. Tier-0은 V를 노출해 부모가 dense 합성 가능. (혼합 트리에서 tier가 위로 전파)

사용:  python app_assemble.py <app.pg> [--store DIR]
"""
import sys, os, json, hashlib
from functools import reduce
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import verify_seal as vs                       # noqa: E402
import spec_guard as sg                        # noqa: E402
import contracts                               # noqa: E402
from registry import Registry, _aggregate_cost  # noqa: E402

MAX_DEPTH = 8       # 분해 트리 깊이 상한
EXACT_BOUND = 12    # dense 재실체화 허용 큐비트 상한 (2^12=4096). 초과·golden부재 → Tier-1


class AppVerdict:
    def __init__(self, sealed, id=None, reason="", u_hash=None, resource=None,
                 V=None, tier=None, n_sys=None):
        self.sealed = sealed
        self.id = id
        self.reason = reason
        self.u_hash = u_hash
        self.resource = resource
        self.V = V          # dense 유니터리 (Tier-0만). Tier-1은 None → 부모도 구조적.
        self.tier = tier
        self.n_sys = n_sys

    def __repr__(self):
        return f"AppVerdict(sealed={self.sealed}, id={self.id}, tier={self.tier}, reason={self.reason!r})"


def _structural_hash(children, n_sys):
    """dense 미실체화 — 자식 u_hash + 합성구조의 sha256 (Merkle, 순서 보존)."""
    payload = {
        "kind": "structural-compose-v1",
        "n_sys": n_sys,
        "steps": [{"u_hash": c["u_hash"], "targets": c["targets"]} for c in children],
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _placed(V, targets, n_sys):
    return contracts.embed_unitary(V, targets, n_sys) if targets else V


def _seal_dict(app_id, n_sys, contract, u_hash, resource, tier, extra=None):
    sealed = {
        "id": app_id, "sealed": True, "convention": "qualtran-raw",
        "n_sys": n_sys, "n_anc": 0, "contract": contract, "tier": tier,
        "atol": vs.ATOL, "u_hash": u_hash, "resource": resource,
    }
    if extra:
        sealed.update(extra)
    return vs.finalize_sealed(sealed)   # 코드지문 결합 + 서명 (P0-TRUST)


def assemble(manifest_path, store, sub_dir=None, _depth=0, _chain=None) -> AppVerdict:
    if _depth > MAX_DEPTH:
        return AppVerdict(False, reason=f"max_depth_exceeded(>{MAX_DEPTH})")
    abspath = os.path.abspath(manifest_path)
    _chain = _chain or []
    if abspath in _chain:
        return AppVerdict(False, reason=f"cycle_detected:{os.path.basename(manifest_path)}")
    _chain = _chain + [abspath]

    if not os.path.exists(manifest_path):
        return AppVerdict(False, reason=f"manifest_missing:{os.path.basename(manifest_path)}")
    with open(manifest_path, encoding="utf-8") as f:
        blocks = vs._extract_blocks(f.read())
    for need in ("app_meta", "plan"):            # app_golden은 Tier-1에서 선택
        if need not in blocks:
            return AppVerdict(False, reason=f"manifest_missing_block:{need}")
    meta = json.loads(blocks["app_meta"])
    plan = json.loads(blocks["plan"])
    golden = (np.asarray(vs.instantiate(blocks["app_golden"], "golden"), dtype=complex)
              if "app_golden" in blocks else None)
    sub_dir = sub_dir or os.path.dirname(abspath)
    reg = Registry(store)
    n_sys = meta["n_sys"]

    explicit_tier = plan.get("tier")
    if explicit_tier not in (None, "exact", "structural"):
        return AppVerdict(False, reason=f"invalid_tier:{explicit_tier} (ADVISORY는 seal 아님, INV-TIER)")

    # ── 자식 봉인 (INV1·spec_guard / 재귀) ──
    children = []
    for step in plan["steps"]:
        if "app" in step:
            v = assemble(os.path.join(sub_dir, step["app"]), store, _depth=_depth + 1, _chain=_chain)
            if not v.sealed:
                return AppVerdict(False, reason=f"subapp_failed:{step['app']}:{v.reason}")
            children.append({"u_hash": v.u_hash, "resource": v.resource,
                             "targets": step.get("targets"), "n_qubits": v.n_sys, "V": v.V})
        else:
            p = os.path.join(sub_dir, step["spec"])
            if not os.path.exists(p):
                return AppVerdict(False, reason=f"submodule_missing:{os.path.basename(p)}")
            try:
                spec = vs.load_pg_spec(p)
            except Exception as e:
                return AppVerdict(False, reason=f"submodule_load:{os.path.basename(p)}:{e}")
            if sg.spec_quality_guard(spec).block:
                return AppVerdict(False, reason=f"submodule_specguard:{os.path.basename(p)} (golden 부재 등)")
            r = reg.register(p)
            if not r.admitted:
                return AppVerdict(False, reason=f"submodule_unsealed:{os.path.basename(p)}:{r.reason}")
            sd = reg.get(spec.id)
            V = np.asarray(vs.instantiate(spec.bloq_src, "bloq").tensor_contract())  # 리프=소규모
            children.append({"u_hash": sd["u_hash"], "resource": sd["resource"],
                             "targets": step.get("targets"), "n_qubits": spec.n_sys, "V": V})

    # ── 인터페이스 정합 (INV-IFACE): 각 자식이 n_sys 안에 배치 가능한가 (저비용) ──
    for c in children:
        tw = c["targets"]
        if tw is None:
            if c["n_qubits"] != n_sys:
                return AppVerdict(False, id=meta["id"],
                                  reason=f"interface_mismatch: 폭 {c['n_qubits']}≠n_sys {n_sys} (targets 필요)")
        else:
            if len(tw) != c["n_qubits"] or len(set(tw)) != len(tw) or any(w < 0 or w >= n_sys for w in tw):
                return AppVerdict(False, id=meta["id"], reason=f"interface_mismatch: targets {tw}")

    resource = _aggregate_cost([c["resource"] for c in children])
    all_dense = all(c["V"] is not None for c in children)
    exact = ((explicit_tier == "exact") or
             (explicit_tier is None and golden is not None and n_sys <= EXACT_BOUND and all_dense))

    if exact:
        # ── Tier-0 EXACT (dense) ──
        if not all_dense:
            return AppVerdict(False, id=meta["id"], reason="tier0_requires_dense_children")
        try:
            V_app = reduce(lambda a, b: contracts.compose(a, b, meta["id"]),
                           [_placed(c["V"], c["targets"], n_sys) for c in children])
        except contracts.ContractViolation as e:
            return AppVerdict(False, id=meta["id"], reason=f"compose_violation:{e}")
        u_hash = vs.hash_unitary(V_app)
        if golden is not None and u_hash != vs.hash_unitary(golden):
            return AppVerdict(False, id=meta["id"],
                              reason="decomposition_mismatch: composite≠app_golden")
        sealed = _seal_dict(meta["id"], n_sys, "C1-C4(app)", u_hash, resource, 0)
        reg._admit(sealed)
        return AppVerdict(True, id=meta["id"], u_hash=u_hash, resource=resource,
                          V=V_app, tier=0, n_sys=n_sys)

    # ── Tier-1 STRUCTURAL (dense 미실체화) ──
    u_hash = _structural_hash(children, n_sys)
    extra = {}
    # advisory: 소규모 + golden + 모든 dense면 dense 교차검증(seal은 구조적 유지, 불일치는 거부)
    if golden is not None and all_dense and n_sys <= EXACT_BOUND:
        try:
            V_app = reduce(lambda a, b: contracts.compose(a, b, meta["id"]),
                           [_placed(c["V"], c["targets"], n_sys) for c in children])
        except contracts.ContractViolation as e:
            return AppVerdict(False, id=meta["id"], reason=f"compose_violation:{e}")
        if vs.hash_unitary(V_app) != vs.hash_unitary(golden):
            return AppVerdict(False, id=meta["id"],
                              reason="decomposition_mismatch (structural advisory)")
        extra["advisory"] = "dense_crosscheck_ok"
    sealed = _seal_dict(meta["id"], n_sys, "C1-C4(structural)", u_hash, resource, 1, extra)
    reg._admit(sealed)
    return AppVerdict(True, id=meta["id"], u_hash=u_hash, resource=resource,
                      V=None, tier=1, n_sys=n_sys)   # V=None → 부모도 Tier-1


def main(argv) -> int:
    if not argv:
        sys.stderr.write("usage: app_assemble.py <app.pg> [--store DIR]\n")
        return 1
    manifest = argv[0]
    if "--store" in argv:
        store = argv[argv.index("--store") + 1]
    else:
        store = os.path.join(os.path.dirname(os.path.abspath(manifest)), "_app_store")
    v = assemble(manifest, store)
    if v.sealed:
        sys.stdout.write(f"APP SEALED: {v.id}  tier={v.tier}  u_hash={v.u_hash[:16]}..  resource={v.resource}\n")
        return 0
    sys.stderr.write(f"APP REJECT: {v.reason}\n")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
