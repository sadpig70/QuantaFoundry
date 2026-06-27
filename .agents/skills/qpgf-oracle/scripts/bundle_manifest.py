"""bundle_manifest.py — 스킬 번들 무결성 매니페스트 (배포신뢰, 통합수정설계 P0-TRUST).

봉인의 코드지문(oracle_code_hash·contracts_code_hash)은 *그 두 파일*만 본다. 번들 전체
(scripts·references·SKILL.md)의 무결성을 한 번에 검증하려면 매니페스트가 필요하다.
이 도구는 번들 핵심 파일의 sha256을 결정론 매니페스트(`BUNDLE.sha256`)로 산출/대조한다.
읽기전용 배포·재현빌드의 solo 토대 (Sigstore/GPG 비밀키 서명은 인프라 후속).

사용:
  python bundle_manifest.py            # 매니페스트 생성/갱신 → <bundle>/BUNDLE.sha256
  python bundle_manifest.py --verify   # 현재 파일 vs 매니페스트 대조 (불일치 시 exit1)
"""
import sys, os, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
BUNDLE = os.path.abspath(os.path.join(HERE, ".."))      # .../qpgf-oracle/
MANIFEST = os.path.join(BUNDLE, "BUNDLE.sha256")


def _manifest_files(root=BUNDLE):
    """매니페스트 대상: 번들의 *.py·*.md·*.pg (전체무결성). __pycache__·BUNDLE.sha256 제외."""
    files = []
    for r, _dirs, names in os.walk(root):
        if "__pycache__" in r:
            continue
        for n in names:
            rel = os.path.relpath(os.path.join(r, n), root).replace("\\", "/")
            if rel == "BUNDLE.sha256":
                continue
            if rel.endswith((".py", ".md", ".pg", ".lock")):
                files.append(rel)
    return sorted(files)


def _sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def compute_manifest(root=BUNDLE):
    """{relpath: sha256} (결정론, 정렬)."""
    return {rel: _sha256(os.path.join(root, rel)) for rel in _manifest_files(root)}


def manifest_text(man):
    return "".join(f"{man[rel]}  {rel}\n" for rel in sorted(man))


def write_manifest(root=BUNDLE):
    man = compute_manifest(root)
    with open(os.path.join(root, "BUNDLE.sha256"), "w", encoding="utf-8", newline="\n") as f:
        f.write(manifest_text(man))
    return man


def load_manifest(root=BUNDLE):
    out = {}
    with open(os.path.join(root, "BUNDLE.sha256"), encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            h, rel = line.split("  ", 1)
            out[rel] = h
    return out


def verify_manifest(root=BUNDLE):
    """현재 파일 vs 매니페스트. 반환: (ok, mismatches[list of (rel, status)])."""
    recorded = load_manifest(root)
    current = compute_manifest(root)
    mismatch = []
    for rel in sorted(set(recorded) | set(current)):
        if rel not in current:
            mismatch.append((rel, "missing"))
        elif rel not in recorded:
            mismatch.append((rel, "untracked"))
        elif recorded[rel] != current[rel]:
            mismatch.append((rel, "modified"))
    return (not mismatch), mismatch


def main(argv):
    if "--verify" in argv:
        if not os.path.exists(MANIFEST):
            sys.stderr.write("BUNDLE.sha256 없음 — 먼저 생성하세요\n")
            return 1
        ok, mm = verify_manifest()
        if ok:
            sys.stdout.write(f"bundle_ok: {len(load_manifest())} 파일 무결성 일치\n")
            return 0
        for rel, st in mm:
            sys.stderr.write(f"  ! {st:9} {rel}\n")
        sys.stderr.write(f"bundle_mismatch: {len(mm)} 항목\n")
        return 1
    man = write_manifest()
    sys.stdout.write(f"bundle_manifest 생성: {len(man)} 파일 → {os.path.relpath(MANIFEST, BUNDLE)}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
