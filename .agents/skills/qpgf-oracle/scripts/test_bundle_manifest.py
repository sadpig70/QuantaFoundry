"""test_bundle_manifest.py — 번들 무결성 매니페스트 검증 (격리: 임시 root)."""
import sys, os, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bundle_manifest as bm   # noqa: E402

PASS = 0
FAIL = 0


def check(cond, label):
    global PASS, FAIL
    PASS, FAIL = (PASS + 1, FAIL) if cond else (PASS, FAIL + 1)
    print(f"  {'✅' if cond else '❌'} {label}")


print("=" * 60)
print("bundle_manifest — 무결성 매니페스트")
print("=" * 60)
with tempfile.TemporaryDirectory() as root:
    # 합성 번들
    os.makedirs(os.path.join(root, "scripts"))
    open(os.path.join(root, "scripts", "a.py"), "w").write("print(1)\n")
    open(os.path.join(root, "SKILL.md"), "w").write("# skill\n")
    open(os.path.join(root, "scripts", "ignore.txt"), "w").write("not hashed\n")

    m1 = bm.compute_manifest(root)
    m2 = bm.compute_manifest(root)
    check(m1 == m2, "compute_manifest 결정론 (2회 동일)")
    check(set(m1) == {"scripts/a.py", "SKILL.md"}, ".py/.md/.pg만 대상 (.txt 제외)")

    bm.write_manifest(root)
    ok, mm = bm.verify_manifest(root)
    check(ok and not mm, "write→verify 라운드트립 ok")

    # 변조: 파일 수정 → modified 탐지
    open(os.path.join(root, "scripts", "a.py"), "w").write("print(2)\n")
    ok, mm = bm.verify_manifest(root)
    check(not ok and ("scripts/a.py", "modified") in mm, "파일 변조 → modified 탐지")

    # 신규 파일 → untracked 탐지
    bm.write_manifest(root)
    open(os.path.join(root, "scripts", "b.py"), "w").write("x=1\n")
    ok, mm = bm.verify_manifest(root)
    check(not ok and ("scripts/b.py", "untracked") in mm, "추적외 파일 → untracked 탐지")

print("\n" + "=" * 60)
print(f"결과: {PASS} PASS / {FAIL} FAIL")
print("=" * 60)
sys.exit(1 if FAIL else 0)
