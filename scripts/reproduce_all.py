"""reproduce_all.py — one-command 전체 재현 검증 (compatibility wrapper).

기존 명령 그대로 (INV-RA1):
  python scripts/reproduce_all.py                  # full: 전 앱 byte-identity 재합성
  python scripts/reproduce_all.py --changed-only   # 변경 spec 만 재합성 + coherence
  python scripts/reproduce_all.py --jobs 6         # 독립 검증 스텝 병렬(root 불변, 벽시계 단축)
  python scripts/reproduce_all.py --incremental    # 지문 캐시 가속(부가 모드, INV-INC1: full 이 정본)
출력: reports/REPRODUCE-RESULT.json (기존 형식, INV-RA2) + reports/EVIDENCE-REPORT.json (가산)

내부 위임 (TrackReproduceUpgrade — 확정 플랜 _workspace/reproduce_all_upgrade_plan.md):
  검증 정의 = verification/manifests/*.json   (스텝 추가 = manifest 항목 추가, 코드 무수정)
  실행 엔진 = qf_verify.runner                 (순차 고정 — 결정론 재현 우선)
  legacy    = scripts/reproduce_all_legacy.py  (--legacy 로 구 구현 직접 실행 — 탈출구)

전환 게이트(INV-RA7) 실증: 신구 REPRODUCE-RESULT.json 이 changed 모드에서 107 스텝
키 집합·전 필드 값·bundle 완전 동치 (2026-07-10).
"""
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, ROOT)


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--legacy" in argv:                        # 탈출구: 구 구현 그대로 실행
        argv.remove("--legacy")
        import subprocess
        p = subprocess.run(["python", os.path.join("scripts", "reproduce_all_legacy.py")] + argv,
                           cwd=ROOT)
        return p.returncode
    jobs = 1
    for flag in ("--jobs", "-j"):
        if flag in argv:
            k = argv.index(flag)
            jobs = int(argv[k + 1])
            del argv[k:k + 2]
    incremental = "--incremental" in argv
    if incremental:
        argv.remove("--incremental")
    profile = "changed" if "--changed-only" in argv else "full"
    if incremental and profile == "changed":
        print("reproduce_all: --incremental 은 full 전용 (--changed-only 와 조합 금지)")
        return 2
    from qf_verify import runner
    _, _, code = runner.run_profile(profile, jobs=jobs, incremental=incremental)
    return code


if __name__ == "__main__":
    sys.exit(main())
