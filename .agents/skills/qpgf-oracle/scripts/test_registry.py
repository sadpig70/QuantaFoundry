"""test_registry.py — 봉인권 집행(SealAuthority) 검증.

  R1  register: 정상 spec admit / 위반 spec 거부 (INV1)
  R2  integrity: 변조 sealed.json 적발
  R3  duplicate: 동일 spec idempotent / 같은 id 다른 sig 충돌
  R4  can_compose: 전부 sealed만 True (INV2)
  R5  compose: 봉인모듈 합성 + 자원합산 + 결과등록 (INV3)
  R6  compose 거부: 미봉인 입력(INV2) / 인터페이스 불일치(INV3)
"""
import sys, os, json, copy, tempfile
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from registry import Registry  # noqa: E402
import verify_seal as vs       # noqa: E402

PASS = 0
FAIL = 0


def check(cond, label):
    global PASS, FAIL
    PASS, FAIL = (PASS + 1, FAIL) if cond else (PASS, FAIL + 1)
    print(f"  {'✅' if cond else '❌'} {label}")


def spec_text(imp, expr, golden_expr, sid, n_sys):
    g = f"```python id=golden\ngolden = {golden_expr}\n```\n" if golden_expr else ""
    return (f"M\n```python id=bloq\nfrom qualtran.bloqs.basic_gates import {imp}\n"
            f"bloq = {expr}\n```\n{g}"
            f"```json id=meta\n{{\"id\": \"{sid}\", \"n_sys\": {n_sys}, \"n_anc\": 0}}\n```\n")


SPECS = {
    "mx":   ("XGate", "XGate()", "np.array([[0,1],[1,0]], dtype=complex)", 1),
    "mz":   ("ZGate", "ZGate()", "np.array([[1,0],[0,-1]], dtype=complex)", 1),
    "mbad": ("XGate", "XGate()", "np.array([[1,1],[1,-1]],dtype=complex)/np.sqrt(2)", 1),
    "mcz":  ("CZ",    "CZ()",    "np.diag([1,1,1,-1]).astype(complex)", 2),
}


def write_specs(d):
    paths = {}
    for sid, (imp, expr, g, n) in SPECS.items():
        p = os.path.join(d, f"{sid}.pg")
        open(p, "w", encoding="utf-8").write(spec_text(imp, expr, g, sid, n))
        paths[sid] = p
    return paths


with tempfile.TemporaryDirectory() as work, tempfile.TemporaryDirectory() as store:
    P = write_specs(work)
    reg = Registry(store)

    print("=" * 60)
    print("R1 — register (INV1)")
    print("=" * 60)
    r = reg.register(P["mx"])
    check(r.admitted and reg.is_sealed("mx"), "정상 spec(mx) admit + is_sealed")
    r = reg.register(P["mbad"])
    check(not r.admitted and r.reason == "contract_rejected" and not reg.is_sealed("mbad"),
          "위반 spec(mbad) 거부 + store 미진입 (INV1)")

    print("\n" + "=" * 60)
    print("R2 — integrity (변조 적발)")
    print("=" * 60)
    sealed_path = os.path.join(store, "mx.sealed.json")
    check(reg.verify_integrity(sealed_path), "정상 sealed.json 무결성 OK")
    tampered = json.load(open(sealed_path, encoding="utf-8"))
    tampered["resource"] = {"total_t": 999}                 # 자원 조작
    tp = os.path.join(work, "tampered.sealed.json")
    json.dump(tampered, open(tp, "w", encoding="utf-8"))
    check(not reg.verify_integrity(tp), "변조 sealed.json(resource 조작) 적발")

    print("\n" + "=" * 60)
    print("R3 — duplicate")
    print("=" * 60)
    r = reg.register(P["mx"])
    check(r.admitted, "동일 spec 재등록 idempotent (same sig)")
    conflict = copy.deepcopy(reg.get("mx"))
    conflict["sig"] = "deadbeef"                             # 같은 id 다른 sig
    r = reg._admit(conflict)
    check(not r.admitted and r.reason in ("sig_mismatch", "duplicate_conflict"),
          f"같은 id 다른 sig 거부 → {r.reason}")

    print("\n" + "=" * 60)
    print("R4 — can_compose (INV2)")
    print("=" * 60)
    reg.register(P["mz"])
    check(reg.can_compose("mx", "mz"), "둘 다 sealed → can_compose True")
    check(not reg.can_compose("mx", "nope"), "미봉인 포함 → can_compose False (INV2)")

    print("\n" + "=" * 60)
    print("R5 — compose (INV3, 자원합산)")
    print("=" * 60)
    r = reg.compose([P["mx"], P["mz"]], "mxz")
    check(r.admitted and reg.is_sealed("mxz"), "X∘Z 합성 admit + 등록")
    if reg.is_sealed("mxz"):
        # V = Z@X (contracts.compose(a,b)=b@a)
        Vx = np.array([[0, 1], [1, 0]], dtype=complex)
        Vz = np.array([[1, 0], [0, -1]], dtype=complex)
        check(reg.get("mxz")["u_hash"] == vs.hash_unitary(Vz @ Vx), "합성 u_hash == hash(Z@X)")
        agg = reg.get("mxz")["resource"]
        # X와 Z 각각의 clifford 합 (각 1 → 2)
        check(agg.get("clifford", 0) == reg.get("mx")["resource"].get("clifford", 0)
              + reg.get("mz")["resource"].get("clifford", 0), "자원 키별 합산")

    print("\n" + "=" * 60)
    print("R6 — compose 거부")
    print("=" * 60)
    r = reg.compose([P["mx"], P["mz"]], "mxz")  # already exists, same sig → idempotent ok
    # 미봉인 입력
    unsealed = os.path.join(work, "u.pg")
    open(unsealed, "w", encoding="utf-8").write(spec_text("YGate", "YGate()", None, "munsealed", 1))
    r = reg.compose([P["mx"], unsealed], "mxu")
    check(not r.admitted and r.reason == "unsealed_input", "미봉인 입력 합성 거부 (INV2)")
    # 인터페이스 불일치: 1q ∘ 2q
    reg.register(P["mcz"])
    r = reg.compose([P["mx"], P["mcz"]], "mxcz")
    check(not r.admitted and r.reason.startswith("compose_violation"),
          f"인터페이스 불일치 합성 거부 (INV3) → {r.reason[:40]}")

    print("\n" + "=" * 60)
    print("R7 — compose_uncompute (compute-uncompute isometry)")
    print("=" * 60)
    # alloc isometry(And) + 중간(Z) 봉인 등록
    and_pg = os.path.join(work, "and.pg")
    open(and_pg, "w", encoding="utf-8").write(
        'And\n```python id=bloq\nfrom qualtran.bloqs.mcmt.and_bloq import And\nbloq = And()\n```\n'
        '```json id=meta\n{"id": "rand", "n_sys": 2, "n_anc": 1}\n```\n')
    reg.register(and_pg)
    reg.register(P["mz"])
    # 정상: And†·Z_target·And == CZ
    r = reg.compose_uncompute(and_pg, [(P["mz"], [2])], "rcz")
    cz_uhash = vs.hash_unitary(np.diag([1, 1, 1, -1]).astype(complex))
    check(r.admitted and reg.get("rcz")["contract"] == "C1-C4(uncompute)"
          and reg.get("rcz")["u_hash"] == cz_uhash, "And†·Z·And == CZ 봉인 (u_hash 일치)")
    # 청정성 negative: 중간 X → ancilla 비복귀 → 비유니터리 거부
    r = reg.compose_uncompute(and_pg, [(P["mx"], [2])], "rbad")
    check(not r.admitted and r.reason.startswith("uncompute_unclean"),
          f"X 중간연산 청정성 거부 (INV3) → {r.reason[:30]}")
    # INV2: 미봉인 중간모듈 거부
    umid = os.path.join(work, "umid.pg")
    open(umid, "w", encoding="utf-8").write(spec_text("ZGate", "ZGate()", None, "umid", 1))
    r = reg.compose_uncompute(and_pg, [(umid, [2])], "rinv2")
    check(not r.admitted and r.reason == "unsealed_input", "미봉인 중간모듈 거부 (INV2)")
    # 다중 alloc(MultiAnd, n_alloc=2): MultiAnd†·Z_wire4·MultiAnd == CCZ
    mand_pg = os.path.join(work, "mand.pg")
    gold_mand = ("np.zeros((32,8),dtype=complex)\n"
                 "for _a in range(2):\n"
                 " for _b in range(2):\n"
                 "  for _c in range(2):\n"
                 "   golden[(_a<<4)|(_b<<3)|(_c<<2)|((_a&_b)<<1)|((_a&_b)&_c),(_a<<2)|(_b<<1)|_c]=1.0")
    open(mand_pg, "w", encoding="utf-8").write(
        'M\n```python id=bloq\nfrom qualtran.bloqs.mcmt import MultiAnd\nbloq = MultiAnd((1,1,1))\n```\n'
        f'```python id=golden\ngolden = {gold_mand}\n```\n'
        '```json id=meta\n{"id": "rmand", "n_sys": 3, "n_anc": 2}\n```\n')
    reg.register(mand_pg)
    r = reg.compose_uncompute(mand_pg, [(P["mz"], [4])], "rccz")
    ccz_uhash = vs.hash_unitary(np.diag([1, 1, 1, 1, 1, 1, 1, -1]).astype(complex))
    check(r.admitted and reg.get("rccz")["u_hash"] == ccz_uhash,
          "다중 alloc: MultiAnd†·Z·MultiAnd == CCZ 봉인 (n_alloc=2)")

    print("\n" + "=" * 60)
    print("R8 — provenance 서명결합 (P0-TRUST)")
    print("=" * 60)
    import copy as _copy
    mx = reg.get("mx")
    check("oracle_code_hash" in mx and "contracts_code_hash" in mx,
          "봉인에 코드지문(oracle/contracts_code_hash) 기록")
    check(reg.verify_provenance(mx), "verify_provenance: 봉인 코드해시 == 로컬 번들")
    # 코드해시 변조 → sig에 결합됐으므로 _sig_ok 가 탐지
    tam = _copy.deepcopy(mx); tam["oracle_code_hash"] = "deadbeef" * 8
    check(not reg._sig_ok(tam), "코드해시 변조 → _sig_ok 탐지(서명 결합)")
    # 타번들(다른 코드해시)이 만든 봉인 → verify_provenance 탐지 (내부일관성과 분리)
    other = _copy.deepcopy(mx); other["oracle_code_hash"] = "0" * 64
    check(not reg.verify_provenance(other), "타번들 코드해시 → verify_provenance 탐지")

print("\n" + "=" * 60)
print(f"결과: {PASS} PASS / {FAIL} FAIL")
print("=" * 60)
sys.exit(1 if FAIL else 0)
