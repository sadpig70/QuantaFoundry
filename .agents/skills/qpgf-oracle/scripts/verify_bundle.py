"""verify_bundle.py — 배포신뢰 게이트 (통합수정설계 P0-TRUST 마무리, 스캐폴딩).

봉인을 신뢰하기 *전에* 번들의 무결성 + 서명을 검증해 **신뢰 뿌리를 로컬 파일에서 외부
서명키로 이동**한다. 검증 순서:
  1) 무결성: `BUNDLE.sha256` 매니페스트 == 현재 파일 (bundle_manifest).
  2) 서명(있으면): `BUNDLE.sha256.sig`(또는 `.asc`)를 신뢰 공개키로 검증 (gpg). cosign/Sigstore도 후크.
  3) 판정: TRUSTED(무결성+서명) / INTEGRITY_ONLY(무결성O·미서명, 개발용) / UNTRUSTED_SIGNATURE / TAMPERED.

★ 한계(정직): 이 스크립트도 번들 *내부*다. 최초 신뢰는 **신뢰 채널로 받은 공개키**로 서명된
매니페스트를 검증할 때 성립한다(out-of-band). 서명은 신뢰를 *제거*하지 않고 *외부 앵커로 이동*시킨다.
실제 서명(BUNDLE.sha256.sig)은 유지보수자 키 셋업 후 추가(GPG 또는 Sigstore — DEPLOYMENT-TRUST.md).

사용:  python verify_bundle.py            # 게이트 (무결성+서명 상태 출력)
       python verify_bundle.py --require-signature   # 서명 없으면 실패(배포용)
"""
import sys, os, subprocess, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bundle_manifest as bm   # noqa: E402

BUNDLE = bm.BUNDLE


def check_integrity(root=BUNDLE):
    """매니페스트 == 현재 파일? 반환 (ok, mismatches)."""
    if not os.path.exists(os.path.join(root, "BUNDLE.sha256")):
        return False, [("BUNDLE.sha256", "missing")]
    return bm.verify_manifest(root)


def _sig_path(root):
    for ext in (".sig", ".asc"):
        p = os.path.join(root, "BUNDLE.sha256" + ext)
        if os.path.exists(p):
            return p
    return None


def _check_cosign(root):
    """Sigstore 키리스: BUNDLE.sha256.sig + .pem 를 cosign 으로 검증.

    신원/발급자는 환경변수로(번들 밖=신뢰 채널): QPGF_COSIGN_IDENTITY_REGEXP,
    QPGF_COSIGN_ISSUER(기본 GitHub Actions OIDC). 반환 (status, detail) 또는 None(미적용)."""
    sig = os.path.join(root, "BUNDLE.sha256.sig")
    cert = os.path.join(root, "BUNDLE.sha256.pem")
    if not (os.path.exists(sig) and os.path.exists(cert)):
        return None
    if shutil.which("cosign") is None:
        return "no_tooling", "Sigstore 서명(.sig/.pem) 존재하나 cosign 미설치 — 검증 불가"
    ident = os.environ.get("QPGF_COSIGN_IDENTITY_REGEXP", "https://github.com/sadpig70/QPGF/.*")
    issuer = os.environ.get("QPGF_COSIGN_ISSUER", "https://token.actions.githubusercontent.com")
    manifest = os.path.join(root, "BUNDLE.sha256")
    try:
        r = subprocess.run(["cosign", "verify-blob", "--certificate", cert, "--signature", sig,
                            "--certificate-identity-regexp", ident,
                            "--certificate-oidc-issuer", issuer, manifest],
                           capture_output=True, text=True, timeout=60)
        if r.returncode == 0:
            return "verified", "cosign(Sigstore) 키리스 서명 검증 통과 (Rekor 투명성로그)"
        return "invalid", f"cosign 검증 실패: {r.stderr.strip()[:140]}"
    except Exception as e:
        return "no_tooling", f"cosign 실행 오류: {e}"


def check_signature(root=BUNDLE):
    """서명 검증 (Sigstore cosign 우선, 없으면 GPG). 반환 (status, detail)."""
    cs = _check_cosign(root)
    if cs is not None:
        return cs
    sig = _sig_path(root)
    if sig is None:
        return "unsigned", "서명(.sig/.pem/.asc) 없음 (유지보수자 서명 미설정)"
    if shutil.which("gpg") is None:
        return "no_tooling", "서명 존재하나 gpg 미설치 — 검증 불가"
    manifest = os.path.join(root, "BUNDLE.sha256")
    try:
        r = subprocess.run(["gpg", "--verify", sig, manifest],
                           capture_output=True, text=True, timeout=30)
        if r.returncode == 0:
            return "verified", "gpg 서명 검증 통과 (신뢰 공개키 import 가정)"
        return "invalid", f"gpg 검증 실패: {r.stderr.strip()[:120]}"
    except Exception as e:
        return "no_tooling", f"gpg 실행 오류: {e}"


def verify(root=BUNDLE, require_signature=False):
    """종합 판정. 반환 (status, integrity_ok, sig_status, mismatches)."""
    ok, mm = check_integrity(root)
    if not ok:
        return "TAMPERED", ok, "skipped", mm
    sig_status, _ = check_signature(root)
    if sig_status == "verified":
        return "TRUSTED", ok, sig_status, mm
    if sig_status == "invalid":
        return "UNTRUSTED_SIGNATURE", ok, sig_status, mm
    # unsigned / no_tooling
    if require_signature:
        return "UNSIGNED_REJECTED", ok, sig_status, mm
    return "INTEGRITY_ONLY", ok, sig_status, mm


def main(argv):
    require = "--require-signature" in argv
    status, integ, sig, mm = verify(require_signature=require)
    print(f"무결성: {'✅ OK' if integ else '❌ 불일치'}  ·  서명: {sig}")
    if mm:
        for rel, st in mm[:10]:
            print(f"  ! {st:9} {rel}")
    icon = {"TRUSTED": "✅", "INTEGRITY_ONLY": "🟡", "UNSIGNED_REJECTED": "❌",
            "UNTRUSTED_SIGNATURE": "❌", "TAMPERED": "❌"}.get(status, "?")
    print(f"{icon} 판정: {status}")
    # exit0 = 신뢰가능(TRUSTED) 또는 개발모드 무결성ok(INTEGRITY_ONLY, 서명 미요구)
    ok = status == "TRUSTED" or (status == "INTEGRITY_ONLY" and not require)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
