"""test_verify_bundle.py — 배포신뢰 게이트 검증 (격리: 임시 번들)."""
import sys, os, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bundle_manifest as bm   # noqa: E402
import verify_bundle as vb     # noqa: E402

PASS = 0
FAIL = 0


def check(cond, label):
    global PASS, FAIL
    PASS, FAIL = (PASS + 1, FAIL) if cond else (PASS, FAIL + 1)
    print(f"  {'✅' if cond else '❌'} {label}")


print("=" * 60)
print("verify_bundle — 배포신뢰 게이트")
print("=" * 60)
with tempfile.TemporaryDirectory() as root:
    os.makedirs(os.path.join(root, "scripts"))
    open(os.path.join(root, "scripts", "a.py"), "w").write("x=1\n")
    open(os.path.join(root, "SKILL.md"), "w").write("# s\n")

    # 매니페스트 없음 → TAMPERED(무결성 실패)
    st, integ, sig, mm = vb.verify(root)
    check(st == "TAMPERED" and not integ, "매니페스트 없음 → TAMPERED")

    # 매니페스트 생성 → 미서명이므로 INTEGRITY_ONLY (개발 게이트 통과)
    bm.write_manifest(root)
    st, integ, sig, mm = vb.verify(root)
    check(st == "INTEGRITY_ONLY" and integ and sig == "unsigned", "무결성O·미서명 → INTEGRITY_ONLY")

    # 서명 요구(배포) → 미서명이면 거부
    st, *_ = vb.verify(root, require_signature=True)
    check(st == "UNSIGNED_REJECTED", "--require-signature + 미서명 → 거부")

    # 파일 변조 → TAMPERED
    open(os.path.join(root, "scripts", "a.py"), "w").write("x=2\n")
    st, integ, sig, mm = vb.verify(root)
    check(st == "TAMPERED" and ("scripts/a.py", "modified") in mm, "파일 변조 → TAMPERED(modified 탐지)")

print("\n" + "=" * 60)
print("실제 번들 무결성 게이트 (현재 번들)")
print("=" * 60)
st, integ, sig, mm = vb.verify()
check(integ and st in ("INTEGRITY_ONLY", "TRUSTED"), f"현재 번들 무결성 OK (status={st}, sig={sig})")

print("\n" + "=" * 60)
print(f"결과: {PASS} PASS / {FAIL} FAIL")
print("=" * 60)
sys.exit(1 if FAIL else 0)
