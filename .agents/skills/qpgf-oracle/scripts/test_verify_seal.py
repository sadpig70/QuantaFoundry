"""test_verify_seal.py — 종료 오라클 Acceptance 실증.

확인 항목 (DESIGN-OracleSkill-Impl §2.4 acceptance_criteria):
  A1 exit 0 ⟺ <id>.sealed.json 생성 (정상 spec)
  A2 동일 spec 2회 실행 → byte-identical sealed.json (결정론)
  A3 계약 위반 spec → exit 1 + sealed 미생성 + 구조화 stderr signal
  A4 hash_unitary 민감도: 위상만 다르면 동일 해시, 다른 모듈은 다른 해시
  A5 deterministic_sig: 같은 입력 같은 서명 / u_hash 바뀌면 서명 바뀜
"""
import sys, os, json, tempfile, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import verify_seal as vs  # noqa: E402

PASS = 0
FAIL = 0


def check(cond, label):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  ✅ {label}")
    else:
        FAIL += 1
        print(f"  ❌ {label}")


def run_cli(spec_text, out_dir):
    """spec 텍스트를 임시 .pg로 써서 verify_seal CLI 실행 → (rc, stdout, stderr)."""
    sp = os.path.join(out_dir, "spec.pg")
    with open(sp, "w", encoding="utf-8") as f:
        f.write(spec_text)
    p = subprocess.run([sys.executable, os.path.join(HERE, "verify_seal.py"),
                        sp, "--out", out_dir],
                       capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


GOOD_QFT2 = """QFT2 // 2큐비트 QFT
```python id=bloq
from qualtran.bloqs.qft.qft_text_book import QFTTextBook
bloq = QFTTextBook(2)
```
```python id=golden
N = 4
W = np.exp(2j*np.pi/N)
golden = np.array([[W**(i*j) for j in range(N)] for i in range(N)], dtype=complex)/np.sqrt(N)
```
```json id=meta
{"id": "qft2", "n_sys": 2, "n_anc": 0}
```
"""

# golden 불일치 (X에 H golden) → C4 위반
BAD_GOLDEN = """BadGolden
```python id=bloq
from qualtran.bloqs.basic_gates import XGate
bloq = XGate()
```
```python id=golden
golden = np.array([[1,1],[1,-1]], dtype=complex)/np.sqrt(2)
```
```json id=meta
{"id": "badgolden", "n_sys": 1, "n_anc": 0}
```
"""

# n_anc>0 이지만 정방(2×2) → 차원 불일치 거부 (XGate에 ancilla 1 거짓선언)
BAD_ANC = """BadAnc
```python id=bloq
from qualtran.bloqs.basic_gates import XGate
bloq = XGate()
```
```json id=meta
{"id": "badanc", "n_sys": 1, "n_anc": 1}
```
"""

# And — alloc ancilla 비정방 isometry → C3-iso 봉인 (n_anc>0 확장)
GOOD_AND = """And alloc ancilla
```python id=bloq
from qualtran.bloqs.mcmt.and_bloq import And
bloq = And()
```
```python id=golden
import numpy as np
golden = np.zeros((8, 4), dtype=complex)
for c0 in (0, 1):
    for c1 in (0, 1):
        golden[(c0 << 2) | (c1 << 1) | (c0 & c1), (c0 << 1) | c1] = 1.0
```
```json id=meta
{"id": "and_alloc", "n_sys": 2, "n_anc": 1}
```
"""

print("=" * 64)
print("A1·A2·A3 — 종료 계약 (CLI)")
print("=" * 64)
with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
    rc, out, err = run_cli(GOOD_QFT2, d1)
    sealed = os.path.join(d1, "qft2.sealed.json")
    check(rc == 0 and os.path.exists(sealed), f"A1 정상 spec: exit0({rc}) + sealed 생성")

    # A2 결정론: 두번째 실행(별도 디렉터리)과 byte 비교
    rc2, _, _ = run_cli(GOOD_QFT2, d2)
    sealed2 = os.path.join(d2, "qft2.sealed.json")
    b1 = open(sealed, "rb").read() if os.path.exists(sealed) else b"1"
    b2 = open(sealed2, "rb").read() if os.path.exists(sealed2) else b"2"
    check(rc2 == 0 and b1 == b2, "A2 동일 spec → byte-identical sealed.json")

    # A3 위반 케이스들
    rc, out, err = run_cli(BAD_GOLDEN, d1)
    no_seal = not os.path.exists(os.path.join(d1, "badgolden.sealed.json"))
    sig_ok = '"signal"' in err and "C4" in err
    check(rc == 1 and no_seal and sig_ok, f"A3a golden위반: exit1 + sealed없음 + C4 signal")

    # A3b: n_anc 거짓선언(정방 2×2 + n_anc=1) → 차원 불일치(C1) 거부
    rc, out, err = run_cli(BAD_ANC, d1)
    no_seal = not os.path.exists(os.path.join(d1, "badanc.sealed.json"))
    check(rc == 1 and no_seal and "C1" in err, "A3b n_anc 거짓선언: exit1 + C1 차원 거부")

    # A3c: And alloc ancilla(비정방 isometry) → C3-iso 봉인 (n_anc>0 확장)
    rc, out, err = run_cli(GOOD_AND, d1)
    sealed_and = os.path.join(d1, "and_alloc.sealed.json")
    iso_ok = False
    if rc == 0 and os.path.exists(sealed_and):
        s = json.load(open(sealed_and, encoding="utf-8"))
        iso_ok = s["contract"] == "C1-C4(iso)" and s["n_anc"] == 1
    check(rc == 0 and iso_ok, "A3c And isometry: exit0 + C1-C4(iso) 봉인")

    # A3d: 중첩 alloc (MultiAnd 3제어 = 2 ancilla 트리, alloc-안-alloc) → C1-C4(iso) 봉인·결정론
    NESTED = ('```python id=bloq\nfrom qualtran.bloqs.mcmt.and_bloq import MultiAnd\n'
              'bloq = MultiAnd(cvs=(1, 1, 1))\n```\n'
              '```json id=meta\n{"id": "multiand3_nested", "n_sys": 3, "n_anc": 2}\n```\n')
    rc, out, err = run_cli(NESTED, d1)
    sp = os.path.join(d1, "multiand3_nested.sealed.json")
    nested_ok = False
    if rc == 0 and os.path.exists(sp):
        s = json.load(open(sp, encoding="utf-8"))
        nested_ok = s["contract"] == "C1-C4(iso)" and s["n_anc"] == 2
    check(rc == 0 and nested_ok, "A3d 중첩 alloc(MultiAnd 2-level): exit0 + C1-C4(iso) 봉인")

print("\n" + "=" * 64)
print("A4 — hash_unitary 민감도")
print("=" * 64)
H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
X = np.array([[0, 1], [1, 0]], dtype=complex)
check(vs.hash_unitary(H) == vs.hash_unitary(np.exp(1j * 0.7) * H),
      "A4a 전역위상만 다른 U → 동일 해시")
check(vs.hash_unitary(H) != vs.hash_unitary(X), "A4b 다른 모듈 → 다른 해시")
# 허수부 보존 확인: S(위상게이트) vs Z 구분 (둘 다 실수해시면 충돌)
S = np.array([[1, 0], [0, 1j]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
check(vs.hash_unitary(S) != vs.hash_unitary(Z), "A4c S≠Z (허수부 보존 — 위상정보 손실 없음)")

print("\n" + "=" * 64)
print("A5 — deterministic_sig")
print("=" * 64)
cost = {"total_t": 4, "clifford": 5}
s1 = vs.deterministic_sig(H, cost, vs.ATOL, "m")
s2 = vs.deterministic_sig(np.exp(1j * 0.3) * H, dict(reversed(list(cost.items()))), vs.ATOL, "m")
check(s1 == s2, "A5a 같은 입력(위상·키순서 무관) → 같은 서명")
check(s1 != vs.deterministic_sig(X, cost, vs.ATOL, "m"), "A5b 다른 U → 다른 서명")

print("\n" + "=" * 64)
print(f"결과: {PASS} PASS / {FAIL} FAIL")
print("=" * 64)
sys.exit(1 if FAIL else 0)
