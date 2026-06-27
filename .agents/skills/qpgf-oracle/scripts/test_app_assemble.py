"""test_app_assemble.py — 앱 분해·검증 어셈블리 검증.

  A1 positive  — Grover 앱 분해→봉인, u_hash == 해석적 G
  A2 determinism — 동일 매니페스트 2회 byte-identical 앱 sealed.json
  A3 wrong_decomp — diffusion 누락 → decomposition_mismatch (C-app)
  A4 unsealed_sub — golden 없는 비자명 서브 → spec_guard 거부
  A5 inv2/compose — 합성·앱 golden 정합 (registry INV2·INV3 경유)
"""
import sys, os, json, tempfile, shutil
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import app_assemble as aa            # noqa: E402
import verify_seal as vs             # noqa: E402

EX = os.path.abspath(os.path.join(HERE, "..", "examples", "grover2"))
EX_HET = os.path.abspath(os.path.join(HERE, "..", "examples", "hetero_app"))

PASS = 0
FAIL = 0


def check(cond, label):
    global PASS, FAIL
    PASS, FAIL = (PASS + 1, FAIL) if cond else (PASS, FAIL + 1)
    print(f"  {'✅' if cond else '❌'} {label}")


def grover_G():
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    O = np.diag([1, 1, 1, -1]).astype(complex)
    D = np.kron(H, H) @ np.diag([1, -1, -1, -1]).astype(complex) @ np.kron(H, H)
    return D @ O


print("=" * 60)
print("A1 — Grover 앱 분해·봉인 (positive)")
print("=" * 60)
with tempfile.TemporaryDirectory() as store:
    v = aa.assemble(os.path.join(EX, "grover2.app.pg"), store)
    G = grover_G()
    check(v.sealed and v.id == "grover2", f"앱 봉인 SEALED (id={v.id})")
    check(v.sealed and v.u_hash == vs.hash_unitary(G), "앱 u_hash == 해석적 Grover G (C-app)")
    # 앱이 실제로 정답 |11> 탐색
    s = np.kron(np.array([[1, 1], [1, -1]]) / np.sqrt(2), np.array([[1, 1], [1, -1]]) / np.sqrt(2)) @ np.array([1, 0, 0, 0], dtype=complex)
    check(np.isclose(abs((G @ s)[3]) ** 2, 1.0), "앱 동작: G|s> = |11> 확률 1 (정답 탐색)")

print("\n" + "=" * 60)
print("A2 — 결정론 (동일 매니페스트 byte-identical)")
print("=" * 60)
with tempfile.TemporaryDirectory() as s1, tempfile.TemporaryDirectory() as s2:
    v1 = aa.assemble(os.path.join(EX, "grover2.app.pg"), s1)
    v2 = aa.assemble(os.path.join(EX, "grover2.app.pg"), s2)
    b1 = open(os.path.join(s1, "grover2.sealed.json"), "rb").read()
    b2 = open(os.path.join(s2, "grover2.sealed.json"), "rb").read()
    check(v1.sealed and v2.sealed and b1 == b2, "동일 매니페스트 → byte-identical 앱 sealed.json")

print("\n" + "=" * 60)
print("A3 — 틀린 분해 거부 (decomposition_mismatch, C-app)")
print("=" * 60)
with tempfile.TemporaryDirectory() as work, tempfile.TemporaryDirectory() as store:
    shutil.copy(os.path.join(EX, "oracle.pg"), os.path.join(work, "oracle.pg"))
    shutil.copy(os.path.join(EX, "diffusion.pg"), os.path.join(work, "diffusion.pg"))
    # app_golden = G 인데 plan은 oracle만 → 합성품(oracle) ≠ G
    open(os.path.join(work, "bad.app.pg"), "w", encoding="utf-8").write(
        '```json id=app_meta\n{"id": "grover2_bad", "n_sys": 2, "n_anc": 0}\n```\n'
        '```python id=app_golden\nimport numpy as np\n'
        'H=np.array([[1,1],[1,-1]],dtype=complex)/np.sqrt(2)\n'
        'O=np.diag([1,1,1,-1]).astype(complex)\n'
        'D=np.kron(H,H)@np.diag([1,-1,-1,-1]).astype(complex)@np.kron(H,H)\n'
        'golden = D @ O\n```\n'
        '```json id=plan\n{"compose": "homogeneous", "steps": [{"spec": "oracle.pg"}]}\n```\n')
    v = aa.assemble(os.path.join(work, "bad.app.pg"), store)
    check(not v.sealed and v.reason.startswith("decomposition_mismatch"),
          f"분해 불일치 거부 → {v.reason[:40]}")

print("\n" + "=" * 60)
print("A4 — 미봉인 서브모듈 거부 (spec_guard reward-hacking 차단)")
print("=" * 60)
with tempfile.TemporaryDirectory() as work, tempfile.TemporaryDirectory() as store:
    # golden 없는 비자명(n_sys=2) 서브 → spec_guard block
    open(os.path.join(work, "nogold.pg"), "w", encoding="utf-8").write(
        '```python id=bloq\nfrom qualtran.bloqs.basic_gates import CZ\nbloq = CZ()\n```\n'
        '```json id=meta\n{"id": "nogold", "n_sys": 2, "n_anc": 0}\n```\n')
    open(os.path.join(work, "app.pg"), "w", encoding="utf-8").write(
        '```json id=app_meta\n{"id": "app_ng", "n_sys": 2, "n_anc": 0}\n```\n'
        '```python id=app_golden\nimport numpy as np\ngolden = np.diag([1,1,1,-1]).astype(complex)\n```\n'
        '```json id=plan\n{"compose": "homogeneous", "steps": [{"spec": "nogold.pg"}]}\n```\n')
    v = aa.assemble(os.path.join(work, "app.pg"), store)
    check(not v.sealed and v.reason.startswith("submodule_specguard"),
          f"golden 부재 서브 거부 → {v.reason[:40]}")

print("\n" + "=" * 60)
print("A5 — 재귀 분해 (sub-app 트리, bottom-up 봉인)")
print("=" * 60)
with tempfile.TemporaryDirectory() as store:
    v = aa.assemble(os.path.join(EX, "grover2_rec.app.pg"), store)
    check(v.sealed and v.id == "grover2_rec", f"재귀 앱 봉인 SEALED (id={v.id})")
    check(v.sealed and v.u_hash == vs.hash_unitary(grover_G()),
          "재귀 합성품 == 해석적 G (C-app 트리 전파)")
    # 트리 전체가 bottom-up 봉인됐는가 (sub-app + 리프들)
    sealed_files = set(os.listdir(store))
    expect = {"grover2_rec.sealed.json", "grover2_diffusion_app.sealed.json",
              "grover2_oracle.sealed.json", "hlayer2.sealed.json", "reflect00.sealed.json"}
    check(expect <= sealed_files, "분해 트리 전체 봉인 (sub-app+리프 5종)")

print("\n" + "=" * 60)
print("A6 — 순환 분해 거부 (cycle guard)")
print("=" * 60)
with tempfile.TemporaryDirectory() as work, tempfile.TemporaryDirectory() as store:
    # 자기 자신을 sub-app으로 참조 → 무한 재귀 → cycle_detected
    open(os.path.join(work, "self.app.pg"), "w", encoding="utf-8").write(
        '```json id=app_meta\n{"id": "selfref", "n_sys": 2, "n_anc": 0}\n```\n'
        '```python id=app_golden\nimport numpy as np\ngolden = np.eye(4, dtype=complex)\n```\n'
        '```json id=plan\n{"steps": [{"app": "self.app.pg"}]}\n```\n')
    v = aa.assemble(os.path.join(work, "self.app.pg"), store)
    check(not v.sealed and "cycle_detected" in v.reason, f"자기참조 분해 거부 → {v.reason[:34]}")

print("\n" + "=" * 60)
print("A7 — 이종 인터페이스 앱 (폭 다른 부품 트리)")
print("=" * 60)
with tempfile.TemporaryDirectory() as store:
    v = aa.assemble(os.path.join(EX_HET, "hetero.app.pg"), store)
    SW = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], dtype=complex)
    TOFF = np.eye(8, dtype=complex); TOFF[6, 6] = 0; TOFF[6, 7] = 1; TOFF[7, 6] = 1; TOFF[7, 7] = 0
    het_golden = TOFF @ np.kron(np.eye(2), SW)
    check(v.sealed and v.id == "hetero_app", f"이종 앱 봉인 SEALED (id={v.id})")
    check(v.sealed and v.u_hash == vs.hash_unitary(het_golden),
          "이종 합성품(2q@[1,2]+3q) == 앱 golden (C-app)")
    # 폭 다른 서브모듈이 함께 봉인됐는가
    files = set(os.listdir(store))
    check({"hetero_app.sealed.json", "hetero_swap2.sealed.json",
           "hetero_toffoli.sealed.json"} <= files, "이종 부품(2q swap + 3q toffoli) 봉인")

print("\n" + "=" * 60)
print("A8 — Seal Tier: Tier-0(dense) vs Tier-1(structural)")
print("=" * 60)
EX_STR = os.path.abspath(os.path.join(HERE, "..", "examples", "structural"))
with tempfile.TemporaryDirectory() as s0, tempfile.TemporaryDirectory() as s1:
    v0 = aa.assemble(os.path.join(EX, "grover2.app.pg"), s0)
    v1 = aa.assemble(os.path.join(EX, "grover2_structural.app.pg"), s1)
    check(v0.sealed and v0.tier == 0 and v0.u_hash == vs.hash_unitary(grover_G()),
          "Tier-0 dense: u_hash == 해석적 G")
    check(v1.sealed and v1.tier == 1 and v1.u_hash != v0.u_hash,
          "Tier-1 structural: 봉인, u_hash=구조적(dense와 상이)")
    # Tier-1 advisory(소규모+golden) 통과 = 구조적 봉인이 참 유니터리와 정합
    check(json.load(open(os.path.join(s1, "grover2_structural.sealed.json")))
          .get("advisory") == "dense_crosscheck_ok", "Tier-1 advisory dense 교차검증 통과")

print("\n" + "=" * 60)
print("A9 — SmallNBound 탈출: 20큐비트 구조적 봉인 (dense 미실체화)")
print("=" * 60)
with tempfile.TemporaryDirectory() as store:
    v = aa.assemble(os.path.join(EX_STR, "big20.app.pg"), store)
    sd = json.load(open(os.path.join(store, "big20.sealed.json"))) if v.sealed else {}
    check(v.sealed and v.tier == 1 and v.n_sys == 20,
          f"20큐비트 앱 구조적 봉인 (Tier-0이면 2^20 불가) tier={v.tier}")
    check(sd.get("contract") == "C1-C4(structural)" and sd.get("resource", {}).get("clifford") == 5,
          "구조적 contract + 자원합산(CNOT 5)")
    # 결정론: 2회 동일 structural u_hash
    with tempfile.TemporaryDirectory() as s2:
        v2 = aa.assemble(os.path.join(EX_STR, "big20.app.pg"), s2)
        check(v2.sealed and v2.u_hash == v.u_hash, "구조적 u_hash 결정론(2회 동일)")

print("\n" + "=" * 60)
print("A10 — INV-IFACE: 인터페이스 정합 위반 거부")
print("=" * 60)
with tempfile.TemporaryDirectory() as work, tempfile.TemporaryDirectory() as store:
    import shutil as _sh
    _sh.copy(os.path.join(EX_STR, "cnot.pg"), os.path.join(work, "cnot.pg"))
    # targets [0,25] 가 n_sys=3 범위 초과 → interface_mismatch
    open(os.path.join(work, "bad.app.pg"), "w", encoding="utf-8").write(
        '```json id=app_meta\n{"id": "iface_bad", "n_sys": 3, "n_anc": 0}\n```\n'
        '```json id=plan\n{"tier": "structural", "steps": [{"spec": "cnot.pg", "targets": [0, 25]}]}\n```\n')
    v = aa.assemble(os.path.join(work, "bad.app.pg"), store)
    check(not v.sealed and v.reason.startswith("interface_mismatch"),
          f"범위초과 targets 거부 → {v.reason[:30]}")

print("\n" + "=" * 60)
print("A11 — INV-TIER: 확률(advisory) tier는 seal 불가")
print("=" * 60)
with tempfile.TemporaryDirectory() as work, tempfile.TemporaryDirectory() as store:
    open(os.path.join(work, "adv.app.pg"), "w", encoding="utf-8").write(
        '```json id=app_meta\n{"id": "adv", "n_sys": 2, "n_anc": 0}\n```\n'
        '```json id=plan\n{"tier": "advisory", "steps": []}\n```\n')
    v = aa.assemble(os.path.join(work, "adv.app.pg"), store)
    check(not v.sealed and v.reason.startswith("invalid_tier"),
          f"advisory tier 봉인 거부(INV-TIER) → {v.reason[:30]}")

print("\n" + "=" * 60)
print("A12 — 실제 게이트 identity: CCZ = H(wire2)·Toffoli·H(wire2)")
print("=" * 60)
EX_CCZ = os.path.abspath(os.path.join(HERE, "..", "examples", "ccz"))
with tempfile.TemporaryDirectory() as store:
    v = aa.assemble(os.path.join(EX_CCZ, "ccz.app.pg"), store)
    CCZ = np.diag([1, 1, 1, 1, 1, 1, 1, -1]).astype(complex)
    check(v.sealed and v.u_hash == vs.hash_unitary(CCZ),
          "CCZ 앱 봉인 + u_hash == diag(...,−1) (실제 게이트 분해 검증)")
    sd = json.load(open(os.path.join(store, "ccz_app.sealed.json")))
    check(sd["resource"].get("toffoli") == 1 and sd["resource"].get("clifford") == 2,
          "자원: toffoli 1 + clifford 2(H 2)")

print("\n" + "=" * 60)
print(f"결과: {PASS} PASS / {FAIL} FAIL")
print("=" * 60)
sys.exit(1 if FAIL else 0)
