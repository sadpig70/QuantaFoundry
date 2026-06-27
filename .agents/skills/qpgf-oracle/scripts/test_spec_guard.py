"""test_spec_guard.py — R2 명세 충분성 게이트 검증."""
import sys, os, tempfile, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import spec_guard as sg  # noqa: E402
from verify_seal import load_pg_spec  # noqa: E402

PASS = 0
FAIL = 0


def check(cond, label):
    global PASS, FAIL
    PASS, FAIL = (PASS + 1, FAIL) if cond else (PASS, FAIL + 1)
    print(f"  {'✅' if cond else '❌'} {label}")


def run_cli(text):
    with tempfile.TemporaryDirectory() as d:
        sp = os.path.join(d, "s.pg")
        open(sp, "w", encoding="utf-8").write(text)
        p = subprocess.run([sys.executable, os.path.join(HERE, "spec_guard.py"), sp],
                           capture_output=True, text=True)
        return p.returncode, p.stderr


WITH_GOLDEN = """M
```python id=bloq
from qualtran.bloqs.basic_gates import XGate
bloq = XGate()
```
```python id=golden
golden = np.array([[0,1],[1,0]], dtype=complex)
```
```json id=meta
{"id": "m", "n_sys": 1, "n_anc": 0}
```
"""

NO_GOLDEN = """M
```python id=bloq
from qualtran.bloqs.basic_gates import XGate
bloq = XGate()
```
```json id=meta
{"id": "nog", "n_sys": 1, "n_anc": 0}
```
"""

print("=" * 56)
print("R2 SpecGuard")
print("=" * 56)
rc, err = run_cli(WITH_GOLDEN)
check(rc == 0, "golden 있는 비자명 spec → 통과(exit0)")

rc, err = run_cli(NO_GOLDEN)
check(rc == 1 and '"block": true' in err.lower().replace(" ", " "), "golden 없는 비자명 spec → 차단(exit1+signal)")
check("reward-hacking" in err, "차단 사유에 reward-hacking 명시")

print(f"\n결과: {PASS} PASS / {FAIL} FAIL")
sys.exit(1 if FAIL else 0)
