"""registry.py — 봉인권 집행 계층 (SealAuthority).

verify_seal이 *산출*한 서명을 Registry가 *집행*한다. 설계 불변식(DESIGN-QPGF §5):
  INV1  ContractGate 거부 모듈은 registry 진입 불가
  INV2  합성 입력 모듈은 전부 sealed=True
  INV3  합성 결과는 재검증 필수

집행 모델(DESIGN-Registry §1): 봉인의 단일 진입점은 register(spec) — Registry는
봉인을 손으로 받지 않고 내부에서 verify_seal을 경유해서만 등록한다. 따라서 검증
실패(exit≠0) 모듈은 구조적으로 진입 불가(INV1).
"""
from __future__ import annotations
import os, sys, json, tempfile, io, contextlib
from functools import reduce
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify_seal as vs              # noqa: E402
import contracts                      # noqa: E402


class RegResult:
    def __init__(self, admitted: bool, reason: str = "", id: str | None = None):
        self.admitted = admitted
        self.reason = reason
        self.id = id

    def __repr__(self):
        return f"RegResult(admitted={self.admitted}, id={self.id}, reason={self.reason!r})"


def _aggregate_cost(costs: list[dict]) -> dict:
    """자원비용 키별 합산 (FTQC: T·magic state 누적)."""
    out: dict = {}
    for c in costs:
        for k, v in c.items():
            out[k] = out.get(k, 0) + v
    return dict(sorted(out.items()))


class Registry:
    """봉인된 모듈의 단일 신뢰소스. store_dir에 영속(+메모리 캐시)."""

    def __init__(self, store_dir: str):
        self.store_dir = store_dir
        os.makedirs(store_dir, exist_ok=True)
        self._store: dict[str, dict] = {}
        self._load_existing()

    def _load_existing(self):
        for fn in os.listdir(self.store_dir):
            if fn.endswith(".sealed.json"):
                with open(os.path.join(self.store_dir, fn), encoding="utf-8") as f:
                    s = json.load(f)
                if self._sig_ok(s):
                    self._store[s["id"]] = s

    # ── 무결성 ────────────────────────────────────────────────
    @staticmethod
    def _sig_ok(sealed: dict) -> bool:
        """sig가 필드와 내부일관한가 (변조 적발). V 없이 재계산.
        코드지문(oracle/contracts_code_hash)이 sealed에 있으면 서명 재계산에 포함."""
        prov = None
        if "oracle_code_hash" in sealed and "contracts_code_hash" in sealed:
            prov = {"oracle_code_hash": sealed["oracle_code_hash"],
                    "contracts_code_hash": sealed["contracts_code_hash"]}
            if "resource_schema_version" in sealed:
                prov["resource_schema_version"] = sealed["resource_schema_version"]
        expect = vs.sig_from_fields(sealed["id"], sealed["u_hash"],
                                    sealed["resource"], sealed["atol"], provenance=prov)
        return expect == sealed.get("sig")

    def verify_integrity(self, sealed_path: str) -> bool:
        with open(sealed_path, encoding="utf-8") as f:
            return self._sig_ok(json.load(f))

    @staticmethod
    def verify_provenance(sealed: dict) -> bool:
        """봉인을 *만든* 오라클 코드가 이 번들과 동일한가 (P0-TRUST 신뢰 검증).

        _sig_ok(내부 일관성)와 분리: 외부 제출 봉인이 *신뢰 번들*로 만들어졌는지 확인.
        변조된 verify_seal/contracts가 만든 봉인은 코드해시 불일치로 탐지된다.
        (register는 항상 verify_seal을 중앙 재실행하므로 코드해시는 자동으로 로컬과 일치.)"""
        fp = vs.oracle_fingerprint()
        return (sealed.get("oracle_code_hash") == fp["oracle_code_hash"] and
                sealed.get("contracts_code_hash") == fp["contracts_code_hash"])

    # ── 등록 (INV1) ───────────────────────────────────────────
    def register(self, spec_path: str) -> RegResult:
        """봉인의 단일 진입점. verify_seal 경유로만 등록 → 거부모듈 진입 불가(INV1)."""
        spec = vs.load_pg_spec(spec_path)
        with tempfile.TemporaryDirectory() as tmp:
            # verify_seal의 stdout("sealed:" CLI 줄) 억제. stderr signal은 보존(거부사유 가시성).
            with contextlib.redirect_stdout(io.StringIO()):
                rc = vs.main([spec_path, "--out", tmp])
            if rc != 0:
                return RegResult(False, "contract_rejected", spec.id)   # INV1
            with open(os.path.join(tmp, f"{spec.id}.sealed.json"), encoding="utf-8") as f:
                sealed = json.load(f)
        return self._admit(sealed)

    def _admit(self, sealed: dict) -> RegResult:
        sid = sealed["id"]
        if not self._sig_ok(sealed):
            return RegResult(False, "sig_mismatch", sid)          # 변조
        prev = self._store.get(sid)
        if prev and prev["sig"] != sealed["sig"]:
            return RegResult(False, "duplicate_conflict", sid)    # 같은 id 다른 sig
        self._store[sid] = sealed
        with open(os.path.join(self.store_dir, f"{sid}.sealed.json"),
                  "w", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(sealed, ensure_ascii=False, sort_keys=True, indent=2))
            f.write("\n")
        return RegResult(True, "admitted", sid)

    # ── 조회 ──────────────────────────────────────────────────
    def is_sealed(self, sid: str) -> bool:
        return sid in self._store

    def get(self, sid: str) -> dict | None:
        return self._store.get(sid)

    def can_compose(self, *ids: str) -> bool:
        """INV2: 모든 입력이 sealed인가."""
        return all(self.is_sealed(i) for i in ids)

    # ── 합성 (INV2·INV3) ──────────────────────────────────────
    def compose(self, spec_paths: list[str], out_id: str) -> RegResult:
        """봉인된 모듈만 합성(INV2), 합성결과 재검증(INV3) 후 재봉인·등록."""
        specs = [vs.load_pg_spec(p) for p in spec_paths]
        if not self.can_compose(*[s.id for s in specs]):
            return RegResult(False, "unsealed_input", out_id)        # INV2

        Vs = []
        for s in specs:
            bloq = vs.instantiate(s.bloq_src, "bloq")
            Vs.append(np.asarray(bloq.tensor_contract()))            # raw, n_anc=0 → V=U
        # 누적 합성: contracts.compose가 인터페이스·재유니터리성 검증 (INV3)
        try:
            V = reduce(lambda a, b: contracts.compose(a, b, out_id), Vs)
        except contracts.ContractViolation as e:
            return RegResult(False, f"compose_violation:{e}", out_id)  # INV3

        u_hash = vs.hash_unitary(V)
        resource = _aggregate_cost([self._store[s.id]["resource"] for s in specs])
        sealed = vs.finalize_sealed({
            "id": out_id, "sealed": True, "convention": "qualtran-raw",
            "n_sys": specs[0].n_sys, "n_anc": 0, "contract": "C1-C4(composed)",
            "atol": vs.ATOL, "u_hash": u_hash, "resource": resource,
        })
        return self._admit(sealed)

    def compose_hetero(self, items: list[tuple[str, list[int]]], out_id: str,
                       n_sys: int) -> RegResult:
        """이종 인터페이스 합성: 각 봉인모듈을 n_sys 와이어의 명시 target에 임베딩 후 합성.

        items = [(spec_path, targets), ...] — 적용 순서대로. targets는 n_sys
        레지스터 내 와이어(big-endian raw). INV2(sealed만)·INV3(재검증) 보존,
        n_anc=0. 동종(compose)과 달리 폭이 다른 모듈을 한 앱에 조립한다.
        """
        specs = [vs.load_pg_spec(p) for p, _ in items]
        if not self.can_compose(*[s.id for s in specs]):
            return RegResult(False, "unsealed_input", out_id)        # INV2

        Vs = []
        for (path, targets), s in zip(items, specs):
            bloq = vs.instantiate(s.bloq_src, "bloq")
            U = np.asarray(bloq.tensor_contract())                   # raw, n_anc=0
            try:
                Vs.append(contracts.embed_unitary(U, targets, n_sys))
            except contracts.ContractViolation as e:
                return RegResult(False, f"embed_violation:{e}", out_id)
        try:
            V = reduce(lambda a, b: contracts.compose(a, b, out_id), Vs)
        except contracts.ContractViolation as e:
            return RegResult(False, f"compose_violation:{e}", out_id)  # INV3

        u_hash = vs.hash_unitary(V)
        resource = _aggregate_cost([self._store[s.id]["resource"] for s in specs])
        sealed = vs.finalize_sealed({
            "id": out_id, "sealed": True, "convention": "qualtran-raw",
            "n_sys": n_sys, "n_anc": 0, "contract": "C1-C4(composed-hetero)",
            "atol": vs.ATOL, "u_hash": u_hash, "resource": resource,
        })
        return self._admit(sealed)

    def compose_uncompute(self, alloc_path: str,
                          middle_items: list[tuple[str, list[int]]],
                          out_id: str) -> RegResult:
        """compute-uncompute 합성: 봉인 alloc isometry V로 ancilla를 alloc·계산하고,
        중간 봉인 모듈 M을 적용한 뒤 V†로 uncompute → 시스템 유효 연산 R = V† M V.

        FTQC 핵심 패턴(예: And†·Z_target·And = CZ). uncompute는 alloc의 dagger(V†)이며
        별도 모듈이 아니다. **청정성 계약(INV3)**: R이 정방 **유니터리**여야 봉인 —
        그렇지 않으면 ancilla가 |0>으로 복귀 못 한 것(부적절한 M)으로 거부.
        INV2: alloc·중간 모듈 전부 sealed.
        """
        a_spec = vs.load_pg_spec(alloc_path)
        m_specs = [vs.load_pg_spec(p) for p, _ in middle_items]
        if not self.can_compose(a_spec.id, *[s.id for s in m_specs]):
            return RegResult(False, "unsealed_input", out_id)        # INV2

        V = np.asarray(vs.instantiate(a_spec.bloq_src, "bloq").tensor_contract())
        if V.shape[0] == V.shape[1]:
            return RegResult(False, "alloc_not_isometry: V 정방(비alloc)", out_id)
        n_out = int(np.log2(V.shape[0]))
        n_in = int(np.log2(V.shape[1]))
        try:
            contracts.check_isometry(V, n_in, n_out - n_in, a_spec.id)   # alloc 충실성
            M = np.eye(1 << n_out, dtype=complex)
            for (path, targets), s in zip(middle_items, m_specs):
                u = np.asarray(vs.instantiate(s.bloq_src, "bloq").tensor_contract())
                M = contracts.embed_unitary(u, targets, n_out) @ M
            R = V.conj().T @ M @ V                                       # uncompute = V†
            contracts.check_c1_c2(R, n_in, out_id)                       # INV3: 청정 유니터리
        except contracts.ContractViolation as e:
            return RegResult(False, f"uncompute_unclean:{e}", out_id)   # ancilla 비복귀

        u_hash = vs.hash_unitary(R)
        resource = _aggregate_cost(
            [self._store[a_spec.id]["resource"]] + [self._store[s.id]["resource"] for s in m_specs])
        sealed = vs.finalize_sealed({
            "id": out_id, "sealed": True, "convention": "qualtran-raw",
            "n_sys": n_in, "n_anc": 0, "contract": "C1-C4(uncompute)",
            "atol": vs.ATOL, "u_hash": u_hash, "resource": resource,
        })
        return self._admit(sealed)
