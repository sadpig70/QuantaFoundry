# -*- coding: utf-8 -*-
"""frontier_batch — qfa-loop 배치 + 표준 후처리 원커맨드 (FrontierBatchOps, 2026-07-13).

순수 오케스트레이션(검증 로직 무수정): 각 단계는 기존 게이트의 subprocess 호출이며,
합격 판정은 그 게이트들의 exit code·출력만 사용한다(self-judge 금지 상속). 어느 단계든
실패하면 **마감 커밋 없이 정지**하고 상태 파일에 남긴다.

단계:
  1. qfa-loop budget N (라운드별 verified-commit 은 루프 자신이 수행; invariants_held 필수)
  2. compositional --deep 재개 (신규 cmul over-budget 자동 커버, 순열 커널)
  3. coverage_matrix → quality_scorecard → release_root → check-claims → seal_gate_ci
  4. full reproduce (--jobs J) → REPRODUCED (mode=full)
  5. 전부 PASS 시에만 마감 커밋·push (verified-only)

사용:  python -m qf_witness.ops.frontier_batch --budget 8 [--jobs 6] [--skip-loop] [--no-commit]
상태:  _workspace/frontier_batch_status.json (gitignored 머신로컬)
"""
from __future__ import annotations
import argparse
import json
import os
import subprocess
import sys
import time

from qf_witness.core.paths import ROOT

STATUS = os.path.join(ROOT, "_workspace", "frontier_batch_status.json")
LOOP = os.path.join(".agents", "skills", "qfa-loop", "scripts", "autonomy_loop.py")
ENV_NOISE = [os.path.join(".pgf", "arith", "C12X-FRONTIER-3683-REPORT.json")]


def _run(argv, timeout=14400):
    t0 = time.time()
    p = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=timeout)
    out = (p.stdout or "") + (p.stderr or "")
    return p.returncode, out, round(time.time() - t0, 1)


def _py(args, timeout=14400):
    return _run(["python"] + args, timeout=timeout)


def _record(state, entry):
    state["steps"].append(entry)
    os.makedirs(os.path.dirname(STATUS), exist_ok=True)
    with open(STATUS, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=1)
    tail = " | ".join(entry.get("tail", [])[-1:])
    print(f"[batch] {entry['step']}: ok={entry['ok']} rc={entry['rc']} "
          f"{entry['seconds']}s {tail}", flush=True)


def _step(state, name, args, ok_fn, timeout=14400):
    rc, out, sec = _py(args, timeout=timeout)
    entry = {"step": name, "rc": rc, "ok": bool(ok_fn(rc, out)), "seconds": sec,
             "tail": out.strip().splitlines()[-3:]}
    _record(state, entry)
    return entry["ok"]


def _finalize_commit(state, push):
    """전 단계 PASS 후에만 호출 — 후처리 산출물 마감 커밋 (변경 없으면 정직 스킵)."""
    _run(["git", "checkout", "--"] + ENV_NOISE)          # 환경 노이즈 필드 복원
    _run(["git", "add", "-A"])
    rc, out, _ = _run(["git", "diff", "--cached", "--quiet"])
    if rc == 0:
        _record(state, {"step": "finalize", "rc": 0, "ok": True, "seconds": 0,
                        "tail": ["no staged changes — 커밋 생략"]})
        return True
    try:
        onto = json.load(open(os.path.join(ROOT, "registry", "COUNT-ONTOLOGY.json"),
                              encoding="utf-8"))["headline"]
        head = f"{onto['modules']}모듈/{onto['unique_apps']}앱·root {onto['root16']}"
    except Exception:
        head = "counts=COUNT-ONTOLOGY 참조"
    msg = (f"FrontierBatch 마감: 배치 후처리 — {head}\n\n"
           "- qf_witness.ops.frontier_batch 자동 마감(전 게이트 PASS 후 verified-only)\n"
           "- deep 재개·coverage/scorecard/release_root·앵커·full REPRODUCED 통과분\n\n"
           "Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>")
    rc, out, sec = _run(["git", "commit", "-m", msg])
    ok = rc == 0
    if ok and push:
        rc2, out2, _ = _run(["git", "push", "origin", "main"])
        ok = rc2 == 0
        out += out2
    _record(state, {"step": "finalize", "rc": rc, "ok": ok, "seconds": sec,
                    "tail": out.strip().splitlines()[-2:]})
    return ok


LOCK = os.path.join(ROOT, "_workspace", "frontier_batch.lock")


def _acquire_lock():
    """중복 실행 방지(야간 스케줄 겹침 대비): 살아있는 PID 의 락이 있으면 정지."""
    if os.path.exists(LOCK):
        try:
            pid = int(open(LOCK, encoding="utf-8").read().strip())
            rc, out, _ = _run(["tasklist", "/FI", f"PID eq {pid}"], timeout=30)
            if str(pid) in out:
                print(f"[batch] ABORT: 이미 실행 중 (lock pid={pid}) — 이번 회차 생략", flush=True)
                return False
        except Exception:
            pass                                        # 죽은/손상 락 → 회수
    os.makedirs(os.path.dirname(LOCK), exist_ok=True)
    with open(LOCK, "w", encoding="utf-8") as f:
        f.write(str(os.getpid()))
    return True


def main():
    ap = argparse.ArgumentParser(description="qfa-loop batch + standard post-processing")
    ap.add_argument("--budget", type=int, default=8)
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--skip-loop", action="store_true", help="후처리만 (기존 상태 마감)")
    ap.add_argument("--no-commit", action="store_true", help="마감 커밋 생략 (검사만)")
    ap.add_argument("--no-push", action="store_true")
    a = ap.parse_args()
    if not _acquire_lock():
        return 2
    try:
        return _run_batch(a)
    finally:
        try:
            os.remove(LOCK)
        except OSError:
            pass


def _run_batch(a):
    state = {"_schema": "frontier-batch/v1", "budget": a.budget, "steps": []}

    if not a.skip_loop:
        ok = _step(state, "qfa_loop",
                   [LOOP, "--mode", "frontier-factory", "--budget", str(a.budget),
                    "--gates", "changed", "--commit", "--push"],
                   lambda rc, out: rc == 0 and "invariants_held=True" in out)
        if not ok:
            print("[batch] ABORT: qfa-loop 실패 — 마감 커밋 없음", flush=True)
            return 1

    chain = [
        # full 패스 sidecar 재생성 — cost≤1e8 신규 앱 사각지대 폐쇄(deep 은 1e8<cost 만 target,
        # PrimaryOnlyRedeem 2026-07-15: cmul2_mod447/493/501 실사례). 순열 커널로 초 단위.
        ("compositional_full", ["-m", "qf_witness.verify.compositional_verify"],
         lambda rc, out: rc == 0 and "all_ok=True" in out),
        ("deep_resume", ["-m", "qf_witness.verify.compositional_verify", "--deep"],
         lambda rc, out: rc == 0 and "all_ok=True" in out),
        ("coverage", ["-m", "qf_witness.registry.coverage_matrix"],
         lambda rc, out: rc == 0),
        ("scorecard", ["-m", "qf_witness.registry.quality_scorecard"],
         lambda rc, out: rc == 0),
        ("release_root", ["-m", "qf_witness.registry.release_root"],
         lambda rc, out: rc == 0),
        ("check_claims", ["-m", "qf_verify.cli", "check-claims"],
         lambda rc, out: rc == 0 and "all_ok=True" in out),
        ("seal_gate", ["-m", "qf_witness.seal.seal_gate_ci"],
         lambda rc, out: rc == 0 and "PASS ✓" in out and "드리프트 감지" not in out),
        ("full_reproduce", ["scripts/reproduce_all.py", "--jobs", str(a.jobs)],
         lambda rc, out: rc == 0 and "REPRODUCE-ALL → REPRODUCED" in out),
    ]
    for name, args, ok_fn in chain:
        if not _step(state, name, args, ok_fn):
            print(f"[batch] ABORT: {name} 실패 — 마감 커밋 없음", flush=True)
            return 1

    if a.no_commit:
        print("[batch] --no-commit: 전 게이트 PASS, 커밋 생략", flush=True)
        return 0
    if not _finalize_commit(state, push=not a.no_push):
        return 1
    print("[batch] DONE: 배치+후처리 완주 (verified-only 마감)", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
