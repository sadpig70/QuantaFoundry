"""test_golden_guard.py — golden 독립성 게이트 검증 (P0-GOLDEN).

  G1 독립 golden(np.array/diag) → 통과
  G2 자기참조: golden에 bloq.tensor_contract() → 차단
  G3 자기참조: golden = bloq → 차단
  G4 항등 golden(비자명 정방) → 차단
  G5 isometry golden(비정방, and_alloc류) → 항등검사 생략 통과
  G6 통합: spec_quality_guard가 자기참조를 차단(preflight 전파)
"""
import sys, os, tempfile
import numpy as np  # noqa: F401

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import golden_guard as gg          # noqa: E402
import spec_guard as sg            # noqa: E402
from verify_seal import load_pg_spec  # noqa: E402

PASS = 0
FAIL = 0


def check(cond, label):
    global PASS, FAIL
    PASS, FAIL = (PASS + 1, FAIL) if cond else (PASS, FAIL + 1)
    print(f"  {'✅' if cond else '❌'} {label}")


def spec_from(bloq_src, golden_src, sid="t", n_sys=1, n_anc=0):
    """임시 .pg 작성 후 load."""
    d = tempfile.mkdtemp()
    p = os.path.join(d, f"{sid}.pg")
    g = f"```python id=golden\n{golden_src}\n```\n" if golden_src is not None else ""
    open(p, "w", encoding="utf-8").write(
        f"```python id=bloq\n{bloq_src}\n```\n{g}"
        f'```json id=meta\n{{"id": "{sid}", "n_sys": {n_sys}, "n_anc": {n_anc}}}\n```\n')
    return load_pg_spec(p)


print("=" * 60)
print("golden_guard — 독립성 강제")
print("=" * 60)

# G1 독립 golden → 통과
s = spec_from("from qualtran.bloqs.basic_gates import XGate\nbloq = XGate()",
              "import numpy as np\ngolden = np.array([[0,1],[1,0]], dtype=complex)")
check(not gg.golden_independence_guard(s).block, "독립 golden(np.array) 통과")

# G2 자기참조: tensor_contract 복사 → 차단
s = spec_from("from qualtran.bloqs.basic_gates import XGate\nbloq = XGate()",
              "import numpy as np\ngolden = np.asarray(bloq.tensor_contract())")
v = gg.golden_independence_guard(s)
check(v.block and v.reason.startswith("golden_self_reference"), f"tensor_contract 복사 차단 → {v.reason[:30]}")

# G3 자기참조: golden = bloq (Name 참조)
s = spec_from("from qualtran.bloqs.basic_gates import XGate\nbloq = XGate()",
              "golden = bloq")
v = gg.golden_independence_guard(s)
check(v.block and v.reason.startswith("golden_self_reference"), f"bloq 변수 참조 차단 → {v.reason[:30]}")

# G4 항등 golden(비자명 정방) → 차단
s = spec_from("from qualtran.bloqs.basic_gates import XGate\nbloq = XGate()",
              "import numpy as np\ngolden = np.eye(2, dtype=complex)", n_sys=1)
v = gg.golden_independence_guard(s)
check(v.block and v.reason.startswith("identity_golden"), f"항등 golden 차단 → {v.reason[:30]}")

# G5 isometry golden(비정방) → 항등검사 생략, 통과
s = spec_from("from qualtran.bloqs.mcmt.and_bloq import And\nbloq = And()",
              "import numpy as np\ngolden = np.zeros((8,4), dtype=complex)\n"
              "for c0 in (0,1):\n for c1 in (0,1):\n  golden[(c0<<2)|(c1<<1)|(c0&c1),(c0<<1)|c1]=1.0",
              n_sys=2, n_anc=1)
check(not gg.golden_independence_guard(s).block, "isometry golden(비정방) 통과(항등검사 생략)")

# G6 통합: spec_quality_guard 가 자기참조 차단 (preflight 전파)
s = spec_from("from qualtran.bloqs.basic_gates import XGate\nbloq = XGate()",
              "golden = bloq")
check(sg.spec_quality_guard(s).block, "spec_quality_guard 통합: 자기참조 차단")

print("\n" + "=" * 60)
print(f"결과: {PASS} PASS / {FAIL} FAIL")
print("=" * 60)
sys.exit(1 if FAIL else 0)
