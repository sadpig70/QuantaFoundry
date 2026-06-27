r"""sync_qpgf.py — QPGF 오라클 벤더 동기화·검증 (소비방식=벤더 복사, 정욱님 승인 2026-06-27).

QuantaFoundry 는 QPGF 오라클을 `.agents/skills/qpgf-oracle/` 에 **벤더 복사**로 소비한다.
이 방식이 봉인 결정론에 최강인 이유: 봉인 산출물과 *그것을 봉인한 오라클 코드*가 동일 커밋에
존재 → checkout 만으로 재현(환경 재구성 불요). 단, 동기화가 수동이라 (1) "어느 버전인가"의
provenance 와 (2) 오라클 변경 시 봉인 u_hash 불변 게이트를 이 스크립트로 강화한다.

★ 결정론 원칙: 오라클 코드/의존성이 바뀌면 봉인 u_hash·서명이 바뀔 수 있다(oracle_fingerprint
가 봉인 서명에 결합됨). 따라서 오라클 업그레이드는 **의도적·회귀검증된 semver 게이트 이벤트**다.
자동 동기화(submodule/pip)는 이 불변식을 조용히 깰 수 있어 의도적으로 채택하지 않는다.

사용:
  python scripts/sync_qpgf.py stamp [--commit SHA] [--version vX] [--date YYYY-MM-DD]
      # 현재 벤더본 기준으로 VENDOR.json 생성/갱신 (fingerprint·bundle root·deps·upstream meta)
  python scripts/sync_qpgf.py check
      # VENDOR.json ↔ 현재 벤더본 일치(변조탐지) + 결정론 게이트(대표 봉인 u_hash 불변) 검증

오라클 업그레이드 절차(adopt — 수동, 이 순서 엄수):
  1. D:\QPGF 를 태그본으로 동기화하고 skill 번들을 .agents/skills/qpgf-oracle/ 에 복사.
  2. python .agents/skills/qpgf-oracle/scripts/bundle_manifest.py --verify   # 번들 무결성
  3. python .agents/skills/qpgf-oracle/scripts/test_verify_seal.py            # 오라클 자가시험
  4. python scripts/sync_qpgf.py check                                        # 봉인 u_hash 불변 게이트
     → u_hash 가 하나라도 바뀌면 BREAKING: 재봉인 + frozen 키 검토 없이는 커밋 금지.
  5. python scripts/sync_qpgf.py stamp --commit <SHA> --version <tag> --date <YYYY-MM-DD>
"""
import os, sys, json, hashlib, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle")
VENDOR_PATH = os.path.join(ORACLE, "VENDOR.json")
MODREG = os.path.join(ROOT, "registry", "modules")
APPREG = os.path.join(ROOT, "registry", "apps")
APPS = os.path.join(ROOT, "specs", "apps")
MODSPECS = os.path.join(ROOT, "specs", "modules")
sys.path.insert(0, os.path.join(ORACLE, "scripts"))

UPSTREAM = "github.com/sadpig70/QPGF"
# 결정론 게이트 표본: 대표 모듈(분해계층별) + 소형 앱. 빠르게 u_hash 불변만 확인.
GATE_MODULES = ["x_gate", "h_gate", "cz", "t_gate", "qft3", "cr5_gate", "ry_k3"]
GATE_APPS = ["bell", "ghz3", "cmul2_mod21"]


def _sha256_file(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def bundle_root():
    return _sha256_file(os.path.join(ORACLE, "BUNDLE.sha256"))


def parse_deps_lock():
    deps = {}
    p = os.path.join(ORACLE, "DEPENDENCIES.lock")
    for line in open(p, encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#") and "==" in line:
            k, v = line.split("==", 1)
            deps[k.strip()] = v.strip()
    return deps


def fingerprint():
    import verify_seal as vs
    return vs.oracle_fingerprint()


def _upstream_git():
    """D:\\QPGF 가 git 이면 (commit, describe) 반환, 아니면 (None, None)."""
    qpgf = os.environ.get("QPGF_SRC", "D:\\QPGF")
    try:
        commit = subprocess.check_output(["git", "-C", qpgf, "rev-parse", "HEAD"],
                                         stderr=subprocess.DEVNULL).decode().strip()
        desc = subprocess.check_output(["git", "-C", qpgf, "describe", "--tags"],
                                       stderr=subprocess.DEVNULL).decode().strip()
        return commit, desc
    except Exception:
        return None, None


def cmd_stamp(argv):
    args = dict(zip(argv[::2], argv[1::2])) if argv else {}
    git_commit, git_desc = _upstream_git()
    commit = args.get("--commit", git_commit)
    version = args.get("--version", (git_desc.split("-")[0] if git_desc else "v0.1.0"))
    date = args.get("--date", "unknown")  # 결정론: 날짜는 명시 전달 권장(미전달 시 'unknown')
    vendor = {
        "schema": "qpgf-vendor/v1",
        "consumption": "vendored (copied into repo; not submodule/pip — see scripts/sync_qpgf.py)",
        "upstream": UPSTREAM,
        "version": version,
        "upstream_commit": commit,
        "upstream_describe": git_desc,
        "synced_at": date,
        "bundle_sha256_root": bundle_root(),
        "dependencies_lock": parse_deps_lock(),
        "oracle_fingerprint": fingerprint(),
        "policy": "Manual, deliberate sync only. Oracle code/deps changes can alter seal u_hash/signature "
                  "(oracle_fingerprint is bound into every seal). Any upgrade is a semver-gated event "
                  "verified by `python scripts/sync_qpgf.py check` (seal u_hash invariance) before commit.",
    }
    json.dump(vendor, open(VENDOR_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"wrote {VENDOR_PATH}")
    print(f"  version={version} commit={str(commit)[:12]} bundle_root={vendor['bundle_sha256_root'][:16]}")
    print(f"  oracle_code_hash={vendor['oracle_fingerprint']['oracle_code_hash'][:16]}")
    return 0


def _reseal_module_uhash(mid):
    """모듈 bloq 재실체화 → u_hash (verify_seal 의 hash 경로)."""
    import numpy as np, verify_seal as vs
    spec = vs.load_pg_spec(os.path.join(MODSPECS, f"{mid}.pg"))
    V = np.asarray(vs.instantiate(spec.bloq_src, "bloq").tensor_contract())
    return vs.hash_unitary(V)


def cmd_check():
    import shutil, tempfile
    ok_all = True

    def ck(name, cond, detail=""):
        nonlocal ok_all
        ok_all = ok_all and cond
        print(f"  {'✅' if cond else '❌'} {name}{(' — ' + detail) if detail else ''}")

    print("=" * 76)
    print("QPGF 벤더 검증 — VENDOR.json 일치(변조탐지) + 봉인 u_hash 불변 게이트")
    print("=" * 76)
    if not os.path.exists(VENDOR_PATH):
        print("VENDOR.json 없음 — 먼저 `stamp` 실행"); return 1
    v = json.load(open(VENDOR_PATH, encoding="utf-8"))

    # 1) 벤더본 무결성: fingerprint·bundle root 가 VENDOR.json 과 일치?
    print("── 1. 벤더본 무결성 (VENDOR.json vs 현재 코드) ──")
    fp = fingerprint()
    ck("oracle_code_hash", fp["oracle_code_hash"] == v["oracle_fingerprint"]["oracle_code_hash"])
    ck("contracts_code_hash", fp["contracts_code_hash"] == v["oracle_fingerprint"]["contracts_code_hash"])
    ck("bundle_sha256_root", bundle_root() == v["bundle_sha256_root"])

    # 2) 런타임 의존성 일치 (경고성 — 불일치 시 u_hash 변동 위험)
    print("── 2. 런타임 의존성 (DEPENDENCIES.lock vs 설치본) ──")
    import importlib.metadata as im
    name_map = {"cirq-core": "cirq-core"}
    for pkg, want in v["dependencies_lock"].items():
        if pkg == "python":
            got = ".".join(map(str, sys.version_info[:3]))
        else:
            try:
                got = im.version(name_map.get(pkg, pkg))
            except Exception:
                got = "MISSING"
        ck(f"{pkg}=={want}", got == want, "" if got == want else f"installed {got}")

    # 3) 결정론 게이트: 대표 봉인의 u_hash 가 registry 와 불변? (오라클 drift 탐지)
    print("── 3. 결정론 게이트 (대표 봉인 u_hash == registry) ──")
    for mid in GATE_MODULES:
        sp = os.path.join(MODREG, f"{mid}.sealed.json")
        if not os.path.exists(sp):
            ck(f"module {mid} (seal 부재)", False); continue
        ref = json.load(open(sp, encoding="utf-8"))["u_hash"]
        try:
            got = _reseal_module_uhash(mid)
            ck(f"module {mid}", got == ref, "" if got == ref else f"got {got[:12]} ref {ref[:12]}")
        except Exception as e:
            ck(f"module {mid}", False, f"err {e}")
    import app_assemble as aa
    tmp = tempfile.mkdtemp(prefix="qpgf_check_")
    try:
        for aid in GATE_APPS:
            sp = os.path.join(APPREG, f"{aid}.sealed.json")
            asp = os.path.join(APPS, f"{aid}.app.pg")
            if not (os.path.exists(sp) and os.path.exists(asp)):
                ck(f"app {aid} (부재)", False); continue
            ref = json.load(open(sp, encoding="utf-8"))["u_hash"]
            r = aa.assemble(asp, tmp)
            ck(f"app {aid}", bool(r.sealed) and r.u_hash == ref,
               "" if (r.sealed and r.u_hash == ref) else f"sealed={r.sealed}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("=" * 76)
    print("벤더 검증:", "PASS (오라클 drift 없음)" if ok_all else "FAIL (drift/변조 — 커밋 금지)")
    return 0 if ok_all else 1


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "stamp":
        return cmd_stamp(sys.argv[2:])
    if cmd == "check":
        return cmd_check()
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
