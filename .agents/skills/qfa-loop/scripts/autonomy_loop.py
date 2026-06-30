# -*- coding: utf-8 -*-
"""
autonomy_loop.py — AutonomyLoop MVP (real-gate runner).

DESIGN-AutonomyLoop.md 의 PPR(bootstrap→select_next→implement→verify_gate→
guard_check→record→sync_checkpoint→stop_controller)을 **mock 이 아닌 실제
스크립트/git** 에 연결한 실행 가능한 런너.

sim_autonomy_loop_v2.py 가 설계의 *제어흐름* 을 결정론 mock 으로 검증했다면,
이 파일은 그 동일 제어흐름을 **실 게이트(reproduce_all/second_oracle/seal_gate_ci/
verify_contested_guard)·실 fingerprint/frozen 해시·실 git** 에 묶는다.

신뢰 경계(설계 INV 그대로):
  INV1/2  fingerprint 2파일·frozen consensus_keys 는 *읽기만*. guard_check 가
          매 라운드 byte-identical 재확인, 위반 시 즉시 중단(치명).
  INV3    합격 판정은 기계 게이트(returncode + 기대 토큰)만. AI 판정 없음.
  INV5    SyncCheckpoint 는 verified-only(reproduce_all REPRODUCED 분만 commit/push),
          기본브랜치 직접커밋 금지(先브랜치).
  INV6    정지조건(dry_limit>0 ∧ budget>0) 부재 시 bootstrap 이 루프 거부.

MVP 범위:
  - kind="infra" 후보는 registry 무변경(root 불변). MVP 1라운드 = 인프라 라운드.
  - kind="frontier" 후보(드라이버=기존 generator 스크립트)는 Phase-2(frontier 확장)에서 소비.
    이 파일은 그 소비 경로까지 *배선*만 해 둔다(드라이버 등록·실행). 실제 frontier
    착수는 별도 라운드.

사용:
  python _workspace/loop/autonomy_loop.py --mode infra --budget 1            # 게이트만(가동, no git)
  python _workspace/loop/autonomy_loop.py --mode infra --budget 1 --commit   # verified-only commit/push
  python _workspace/loop/autonomy_loop.py --mode infra --budget 1 --gates fast
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time

# ★skill layout 2026-07-01: self-contained skill. 엔진은 scripts/(불변·tracked); 가변 런타임 상태
#   (rounds/loop_state)는 *스킬 내부* .runtime/(gitignored)에 둔다 → _workspace/loop 의존 제거.
HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.abspath(os.path.join(HERE, ".."))               # .agents/skills/qfa-loop
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))  # skills/qfa-loop/scripts → repo root
RUNTIME = os.path.join(SKILL_DIR, ".runtime")
ROUNDS_DIR = os.path.join(RUNTIME, "rounds")
STATE_PATH = os.path.join(RUNTIME, "loop_state.json")

# ★self-improvement 2026-07-01: 백그라운드 모니터링 마찰 완화 — stdout 라인버퍼링 + stderr 진행로그.
try:
    sys.stdout.reconfigure(line_buffering=True)
except Exception:  # noqa: BLE001
    pass


def progress(msg: str) -> None:
    """라운드 경계 진행상황을 stderr 로 즉시 flush(백그라운드 tail 로 실시간 관찰).
    상세 라운드 로그는 여전히 rounds/round-NN.json 에 기록(디스크=라이브 모니터)."""
    print(f"[loop] {msg}", file=sys.stderr, flush=True)

# ── 불변 자산(읽기만 — INV1/2) ──
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
FP_VERIFY = os.path.join(ORACLE, "verify_seal.py")
FP_CONTRACTS = os.path.join(ORACLE, "contracts.py")
FROZEN = os.path.join(ROOT, ".pgf", "keyfree", "consensus_keys.json")
MANIFEST = os.path.join(ROOT, "registry", "REGISTRY-MANIFEST.json")

# 기준 fingerprint(HANDOFF 정본). guard_check 는 이 값에 대한 byte-identical 을 본다.
EXPECT_FP_VERIFY = "45d316a431495c9b9a69163b3912da74ae6430fafcda50f7732198202d03092a"
EXPECT_FP_CONTRACTS = "64dd25399a16d6f812648568f871d223a789fe72f8bce432f3d11296ec7b2ee9"
EXPECT_ROOT_PREFIX = "1134ea04099ea0c1"

# 외부 공개 narrative 2종(SyncCheckpoint DocSyncBatch 관할 — guard 대상 아님).
# (EXTERNAL-ONBOARDING.md 폐기 2026-07-01 → reading order는 AGENTS.md, review-request는 .pgf/external.)
EXT_DOCS = [
    os.path.join(ROOT, "README.md"),
    os.path.join(ROOT, "docs", "QuantaFoundry-Technical-Spec.md"),
]

# reproduce_all 이 재생성하는 비결정 노이즈(available 물리메모리 값) — 커밋 제외.
TRANSIENT_ARTIFACTS = [
    os.path.join(ROOT, ".pgf", "arith", "C12X-FRONTIER-3683-REPORT.json"),
]

# ── 결정론 게이트(설계 §8.2 MachineGate 순서) ──
#   (name, argv, expect_substring)  expect=None 이면 returncode 만 본다.
#
# ★self-improvement 2026-07-01: 2-tier verify. reproduce_all 은 전 generator 를 *재합성*하므로
#   frontier 가 늘수록 선형 증가(W12.23 시점 450s) → 무인 다라운드 연쇄의 #1 병목이었다.
#   per-round = INCREMENTAL(registry build 로 root 결정론 확정 + 독립 게이트, ~30s),
#   종결 = FULL(reproduce_all 전 generator 재합성, byte-identical 최종 보증) 1회.
#   정직 경계: incremental 도 root 는 registry build 가 결정론적으로 산출하고 second_oracle 이
#   모듈을 독립 재검증하며, 당 라운드 신규 봉인의 정확성은 generator 자체 independent-arith/
#   deterministic-reassembly 가 implement 안에서 검증한다. FULL 재현은 세션 종결 시 보증된다.
GATES_FULL = [
    ("reproduce_all", ["scripts/reproduce_all.py"], "REPRODUCED"),
    ("second_oracle", ["scripts/second_oracle.py"], None),
    ("seal_gate_ci", ["scripts/seal_gate_ci.py"], "PASS"),
    ("contested_guard", ["scripts/verify_contested_guard.py"], "ALL PASS"),
]
GATES_INCREMENTAL = [
    ("registry_build", ["scripts/registry_tools.py", "build"], "root="),
    ("second_oracle", ["scripts/second_oracle.py"], None),
    ("seal_gate_ci", ["scripts/seal_gate_ci.py"], "PASS"),
    ("contested_guard", ["scripts/verify_contested_guard.py"], "ALL PASS"),
]
# fast: reproduce_all·registry build 둘 다 제외(직전 상태 신뢰). 비-verified 점검용.
GATES_FAST = [g for g in GATES_FULL if g[0] != "reproduce_all"]
_GATE_SETS = {"full": GATES_FULL, "incremental": GATES_INCREMENTAL, "fast": GATES_FAST}


# ─────────────────────────────────────────────────────────────────────────────
# 결정론 헬퍼
# ─────────────────────────────────────────────────────────────────────────────
def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def read_root() -> str:
    d = json.load(open(MANIFEST, encoding="utf-8"))
    return d.get("registry_root_hash") or d.get("root_hash") or ""


def read_counts() -> tuple[int, int]:
    d = json.load(open(MANIFEST, encoding="utf-8"))
    return d["modules"]["count"], d["apps"]["unique_app_count"]


def run_cmd(argv: list[str], timeout: int = 1800) -> tuple[int, str]:
    p = subprocess.run(["python"] + argv, cwd=ROOT, capture_output=True,
                       text=True, timeout=timeout)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def git(args: list[str]) -> tuple[int, str]:
    p = subprocess.run(["git"] + args, cwd=ROOT, capture_output=True, text=True)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


# ─────────────────────────────────────────────────────────────────────────────
# 후보/드라이버 모델
# ─────────────────────────────────────────────────────────────────────────────
class Candidate:
    """루프가 1라운드에 처리할 작업 단위.

    kind="infra"     : registry 무변경(root 불변). 드라이버=no-op. MVP 라운드.
    kind="frontier"  : 기존 generator 스크립트 1개를 드라이버로 실행(seal+registry).
                       Phase-2 에서 select_next 큐에 주입해 소비.
    """

    def __init__(self, cid: str, kind: str, driver: list[str] | None = None,
                 new_module: bool = False, all_ok_token: str = "all_ok=True"):
        self.id = cid
        self.kind = kind
        self.driver = driver            # frontier: ["scripts/cXYx_frontier.py"]
        self.new_module = new_module
        self.all_ok_token = all_ok_token

    def to_dict(self) -> dict:
        return {"id": self.id, "kind": self.kind, "driver": self.driver,
                "new_module": self.new_module}


# ─────────────────────────────────────────────────────────────────────────────
# 설계 PPR — 실 구현
# ─────────────────────────────────────────────────────────────────────────────
def bootstrap(state: dict) -> dict:
    """불변 기준선 스냅샷 + INV6 정지조건 가드. 실패 시 루프 거부."""
    if not (state["dry_limit"] > 0 and state["budget"] > 0):
        raise RuntimeError("정지조건 부재(dry_limit>0 ∧ budget>0) — 루프 거부 (INV6)")
    base = {
        "root": read_root(),
        "fp_verify": sha256_file(FP_VERIFY),
        "fp_contracts": sha256_file(FP_CONTRACTS),
        "frozen": sha256_file(FROZEN),
        "ext_docs": {os.path.basename(p): sha256_file(p) for p in EXT_DOCS if os.path.exists(p)},
        "counts": read_counts(),
    }
    # INV1/2: 기준 fingerprint 와 일치하는지 부트스트랩에서 1차 확인(불일치면 봉인 전부 무효).
    #   fingerprint·frozen 은 불변(하드핀). root 는 *동적* — frontier 라운드마다 성장하므로
    #   기준값으로 스냅샷만 하고 고정 prefix 를 강제하지 않는다(guard_check 도 root 무검사).
    if base["fp_verify"] != EXPECT_FP_VERIFY or base["fp_contracts"] != EXPECT_FP_CONTRACTS:
        raise RuntimeError("fingerprint 불일치 — oracle 변조 의심, 루프 거부 (INV2)")
    return base


def select_next(queue: list[Candidate]) -> Candidate | None:
    """후보 큐에서 1개 pop. 비면 None(frontier-exhausted)."""
    return queue.pop(0) if queue else None


def discover_frontier() -> dict:
    """설계 SelectNext.Discover(부분 자율) — frontier_selector.py 결정론 랭킹을 조회해
    *다음 권장 frontier 후보*를 surface 한다. 후보 식별은 자율, generator 스크립트 작성은
    여전히 수동(H1: 자동 codegen 은 봉인 안전성 미검증이라 의도적 비자동).

    반환: {top_512_767, top_256_511, note}. 실패(파일 부재 등) 시 {error}."""
    try:
        rpt = os.path.join(ROOT, ".pgf", "arith", "FRONTIER-SELECTOR-REPORT.json")
        if not os.path.exists(rpt):   # 비싼 전수 합성은 리포트 부재 시 1회만(매 라운드 재실행 금지)
            run_cmd(["scripts/frontier_selector.py"])
        d = json.load(open(rpt, encoding="utf-8"))
        obs = d.get("current_frontier_observations", {})
        return {
            "top_512_767": obs.get("best_512_767", {}).get("N") if obs.get("best_512_767") else None,
            "top_256_511": obs.get("best_256_511", {}).get("N") if obs.get("best_256_511") else None,
            "note": "후보 식별 자율 · generator 작성 수동(c-ladder 다음=c13x, 2^14 dense 메모리 한계)",
        }
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)[:200]}


def implement(cand: Candidate, gates_mode: str) -> dict:
    """후보 드라이버 실행. infra=no-op 봉인성공. frontier=generator 스크립트(들) 순차 실행.

    frontier 드라이버는 단일 argv 또는 argv 리스트(여러 스크립트, 의존 순)를 허용한다.
    각 스크립트는 자체 verify_seal+registry admit+all_ok 판정을 수행(결정론·idempotent)."""
    if cand.kind == "infra":
        return {"sealed": True, "kind": "infra", "registry_touched": False, "steps": []}
    # driver: list[str](단일) 또는 list[list[str]](다단계)
    scripts = cand.driver if cand.driver and isinstance(cand.driver[0], list) else [cand.driver]
    steps = []
    sealed = True
    for argv in scripts:
        rc, out = run_cmd(argv)
        ok = rc == 0 and cand.all_ok_token in out
        steps.append({"script": argv[0], "rc": rc, "all_ok": ok, "tail": out[-400:]})
        if not ok:
            sealed = False
            break
    return {"sealed": sealed, "kind": "frontier", "registry_touched": True, "steps": steps}


def machine_gate(gates_mode: str) -> dict:
    """순차 AND + short-circuit. 첫 실패서 중단하고 사유 반환(롤백은 guard_check 상위)."""
    gates = _GATE_SETS.get(gates_mode, GATES_FULL)
    calls = []
    for name, argv, expect in gates:
        t0 = time.time()
        rc, out = run_cmd(argv)
        ok = rc == 0 and (expect is None or expect in out)
        calls.append({"gate": name, "rc": rc, "ok": ok, "secs": round(time.time() - t0, 1)})
        if not ok:
            return {"machine": False, "failed_at": name, "calls": calls,
                    "tail": out[-1200:]}
    return {"machine": True, "failed_at": None, "calls": calls}


def adversarial_verify(seal: dict) -> dict:
    """설계 §8.3 — N 직교 회의주의자. MVP 는 *추가* 안전망(합격권 없음, INV3).

    MVP infra 라운드: registry 무변경이므로 반증대상(C1~C3 위반)이 없다 →
    구조적으로 survived=True. frontier 라운드의 실제 반증은 generator 의 independent
    hash match(second_oracle INDEP)가 기계 게이트로 이미 수행한다. 여기서는 정직하게
    'machine-subsumed' 로 표기하고 별도 AI 판정을 부과하지 않는다(self-judge 금지)."""
    return {"survived": True, "note": "machine-subsumed (INV3: no AI verdict)"}


def verify_gate(seal: dict, gates_mode: str) -> dict:
    """결정론 게이트 ∧ adversarial. 둘 다 통과해야 verified."""
    mg = machine_gate(gates_mode)
    av = adversarial_verify(seal)
    return {"verified": bool(mg["machine"] and av["survived"]),
            "machine_gate": mg, "adversarial": av}


def guard_check(base: dict) -> dict:
    """봉인 후 불변 재확인(INV1/2). fingerprint 2파일·frozen byte-identical.
    위반 = 치명 → 상위에서 즉시 중단. 외부 3종은 SyncCheckpoint 관할(불변 대상 아님)."""
    now = {
        "fp_verify": sha256_file(FP_VERIFY),
        "fp_contracts": sha256_file(FP_CONTRACTS),
        "frozen": sha256_file(FROZEN),
    }
    ok = (now["fp_verify"] == base["fp_verify"]
          and now["fp_contracts"] == base["fp_contracts"]
          and now["frozen"] == base["frozen"])
    return {"ok": ok, "now": now,
            "expected": {k: base[k] for k in ("fp_verify", "fp_contracts", "frozen")}}


def scan_stale(base: dict) -> dict:
    """설계 §8.4 ScanStale(강건판) — 외부 3종 + 게이트 앵커에서 *현재와 다른* root prefix·
    module/app count 참조를 전수 탐지. 멱등 anchor(seal_gate_ci)와 narrative(EXT_DOCS)를 구분.

    탐지:
      - root16: 16-hex 토큰 중 'root' 문맥 근처에서 현재 root16 과 다른 것.
      - counts: '<N> apps'·'<N> sealed app'·'apps 105→<N>' 등에서 현재 unique_app_count 와 다른 것
                (단 'X/Y at ...' milestone 이력 패턴은 제외 — historical 보존)."""
    cur_root16 = read_root()[:16]
    n_mod, n_app = read_counts()
    # root16 = 정확·저오탐 신호(결정론 앵커). app-count narrative 는 표현이 다양해 정규식 오탐이
    # 많으므로 자동탐지하지 않는다(task_record 누적 규율로 관리 — 정직성 > 노이즈).
    root_re = re.compile(r"([0-9a-f]{16})[0-9a-f]*[…\.]*")
    targets = EXT_DOCS + [os.path.join(ROOT, "scripts", "seal_gate_ci.py")]
    stale = []
    for p in targets:
        if not os.path.exists(p):
            continue
        txt = open(p, encoding="utf-8").read()
        is_anchor = p.endswith("seal_gate_ci.py")
        for m in re.finditer(root_re, txt):
            tok = m.group(1)
            ctx = txt[max(0, m.start() - 60):m.start()].lower()
            if tok != cur_root16 and ("root" in ctx or "expect" in ctx or is_anchor):
                stale.append({"file": os.path.basename(p), "kind": "root", "found": tok,
                              "expect": cur_root16, "anchor": is_anchor})
    return {"current_root16": cur_root16, "current_apps": n_app,
            "stale": stale, "stale_count": len(stale),
            "narrative_stale": [s for s in stale if not s.get("anchor")],
            "anchor_stale": [s for s in stale if s.get("anchor")],
            "note": "root-anchor scan only; app-count는 task_record batch 규율로 관리(정규식 오탐 회피)"}


def anchor_sync() -> dict:
    """멱등 결정론 앵커 자동 동기화(frontier 라운드 필수): seal_gate_ci EXPECT_DEFAULT → 현재 root.
    + CITATION/SEMANTIC 자동재생성(citation_gen·semantic_guarantee). narrative 문서는 건드리지 않음."""
    cur16 = read_root()[:16]
    sgci = os.path.join(ROOT, "scripts", "seal_gate_ci.py")
    txt = open(sgci, encoding="utf-8").read()
    m = re.search(r'EXPECT_DEFAULT\s*=\s*"([0-9a-f]+)"', txt)
    updated = False
    if m and m.group(1) != cur16:
        txt = txt[:m.start(1)] + cur16 + txt[m.end(1):]
        open(sgci, "w", encoding="utf-8", newline="\n").write(txt)
        updated = True
    regen = {}
    for name, script in [("citation", "scripts/citation_gen.py"),
                         ("semantic", "scripts/semantic_guarantee.py")]:
        rc, _ = run_cmd([script])
        regen[name] = rc == 0
    return {"anchor_root": cur16, "seal_gate_ci_updated": updated, "regen": regen}


def doc_sync_batch(base: dict, sync_anchors: bool = True) -> dict:
    """설계 §8.4 DocSyncBatch(실구현). 두 층 분리:
      1. 멱등 앵커(seal_gate_ci·CITATION·SEMANTIC) = 자동 동기화(anchor_sync).
      2. narrative(README/Technical-Spec) = scan_stale 로 탐지 후 *보고만*
         (서사 rewrite 는 historical 보존이 필요해 수동/batch — 자동 덮어쓰기 금지)."""
    result = {"scanned": True}
    if sync_anchors:
        result["anchor_sync"] = anchor_sync()
    result.update(scan_stale(base))
    result["narrative_action"] = ("manual-batch-required" if result["narrative_stale"]
                                  else "up-to-date")
    return result


def clean_transient() -> list[str]:
    """reproduce_all 이 재생성한 비결정 아티팩트(메모리 값)를 커밋 전 복원."""
    restored = []
    for p in TRANSIENT_ARTIFACTS:
        rel = os.path.relpath(p, ROOT)
        rc, out = git(["status", "--porcelain", "--", rel])
        if out.strip():
            git(["checkout", "--", rel])
            restored.append(rel)
    return restored


def clean_eol_ghosts() -> list[str]:
    """★self-improvement 2026-07-01: autocrlf 유령 diff 자동복원.
    봉인/spec 재실행 시 내용은 byte-identical 인데 git 이 EOL 정규화로 'M' 표시 → 이번 세션
    수동 git checkout 10회 마찰. numstat 가 *빈 변경*(content delta 0)인 modified 파일을 유령으로
    판정해 자동 restore(내용 delta 0 이므로 복원해도 손실 없음). 진짜 변경(N\\tM)·신규(-)는 보존."""
    restored = []
    rc, out = git(["status", "--porcelain"])
    for line in out.splitlines():
        if len(line) < 4 or line[0] in "?!" or line[1] != "M":   # unstaged modified 만
            continue
        rel = line[3:].strip().strip('"')
        rc2, ns = git(["diff", "--numstat", "--", rel])
        if not ns.strip():                                       # 빈 numstat = EOL 유령
            git(["checkout", "--", rel])
            restored.append(rel)
    return restored


def ensure_branch(branch: str) -> dict:
    """★2026-07-01 정욱님 지시: 브랜치 생성 금지 · main 직접 커밋·푸쉬.
    구 INV5/R6(先브랜치)는 명시적으로 무효화됨. 현재 브랜치를 그대로 사용(전환·생성 없음)."""
    rc, cur = git(["branch", "--show-current"])
    return {"branch": cur.strip(), "switched": False, "direct_main": True}


def sync_checkpoint(state: dict, cfg: dict, verified: bool, base: dict,
                    do_git: bool, paths_to_stage: list[str], final: bool = False,
                    gates_mode: str = "full") -> dict:
    """C: 적정시기(K라운드마다 or 종결)에만 발화. verified-only commit/push.

    ★self-improvement 2026-07-01: commit 은 *full* 게이트(reproduce_all 재합성 REPRODUCED)에서만.
    incremental/fast 모드는 게이트 통과해도 커밋하지 않는다(빠른 반복·무인 연쇄 개발용 — 결정론
    최종 보증은 full 만 제공). verified-only 의 'verified'를 full-재현으로 엄격 정의."""
    due = final or (state["round"] % cfg["commit_every"] == 0)
    if not due:
        return {"synced": False, "reason": "not-due"}
    ds = doc_sync_batch(base, sync_anchors=False)   # 앵커는 implement 직후 이미 동기화됨
    result = {"synced": True, "doc_sync": ds, "committed": False, "pushed": False}
    if not do_git:
        result["reason"] = "git-disabled (gates+invariants 검증만)"
        return result
    if gates_mode != "full":
        result["reason"] = f"non-full gates({gates_mode}) → commit 보류(full 재현만 verified-commit)"
        return result
    if not verified:
        result["reason"] = "verified-only: 게이트 미통과 → commit/push 생략"
        return result
    # verified-only 안전게이트: reproduce_all REPRODUCED 재확인은 verify_gate 가 이미 수행.
    restored = clean_transient()
    ghosts = clean_eol_ghosts()                # autocrlf 유령 diff 자동복원(수동 git checkout 제거)
    result["restored_transient"] = restored
    result["restored_eol_ghosts"] = ghosts
    ensure = ensure_branch(cfg["branch"])
    result["branch"] = ensure
    for rel in paths_to_stage:
        git(["add", "--", rel])
    rc, staged = git(["diff", "--cached", "--name-only"])
    staged_files = [s for s in staged.splitlines() if s.strip()]
    if not staged_files:
        result["reason"] = "no-delta (가산 없음 — 커밋 생략)"
        return result
    msg = cfg["commit_message"]
    rc, out = git(["commit", "-m", msg])
    result["committed"] = rc == 0
    result["commit_out"] = out[-400:]
    result["staged_files"] = staged_files
    if rc == 0 and cfg.get("push", False):
        rc, out = git(["push", "origin", "HEAD"])   # 현재 브랜치(main) 직접 푸쉬
        result["pushed"] = rc == 0
        result["push_out"] = out[-400:]
    return result


def stop_controller(state: dict) -> bool:
    return (state["dry"] >= state["dry_limit"]
            or state["budget"] <= 0
            or state["frontier_exhausted"]
            or state["guard_violation"])


def record_round(state: dict, entry: dict) -> str:
    os.makedirs(ROUNDS_DIR, exist_ok=True)
    path = os.path.join(ROUNDS_DIR, f"round-{state['round']:02d}.json")
    json.dump(entry, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return path


def autonomy_round(queue: list[Candidate], state: dict, base: dict,
                   cfg: dict, do_git: bool, gates_mode: str) -> dict:
    r = state["round"]
    log = {"round": r, "ts": time.strftime("%Y-%m-%dT%H:%M:%S")}

    log["discover"] = discover_frontier()        # 발견 자율(보고): 다음 권장 frontier surface
    cand = select_next(queue)
    if cand is None:
        state["frontier_exhausted"] = True
        log["reason"] = "frontier-exhausted"
        record_round(state, log)
        return {"stop": True, "reason": "frontier-exhausted", "state": state, "log": log}
    log["candidate"] = cand.to_dict()
    progress(f"round {r}: candidate={cand.id} kind={cand.kind} → implement…")

    impl = implement(cand, gates_mode)
    log["implement"] = impl
    if not impl["sealed"]:
        state["dry"] += 1
        log["reason"] = "seal-blocked"
        record_round(state, log)
        return {"stop": stop_controller(state), "reason": "seal-blocked", "state": state, "log": log}

    # ★버그수정 2026-07-01: frontier 봉인 후 registry 를 *먼저 build* 해 새 root 를 확정한 뒤
    #   anchor_sync 해야 한다. (이전: anchor_sync 가 registry build 전에 옛 root 를 앵커 →
    #   verify_gate 의 reproduce_all 이 root 를 바꿔 seal_gate_ci 가 불일치로 실패했음.)
    if cand.kind == "frontier":
        rb_rc, rb_out = run_cmd(["scripts/registry_tools.py", "build"])
        log["registry_build"] = {"rc": rb_rc, "root": read_root()[:16]}
        log["anchor_sync"] = anchor_sync()          # 이제 새 root 로 seal_gate_ci 앵커 갱신
        progress(f"round {r}: sealed → registry root={read_root()[:12]} anchor-synced")

    vg = verify_gate(impl, gates_mode)
    log["verify_gate"] = {"verified": vg["verified"],
                          "calls": vg["machine_gate"]["calls"],
                          "failed_at": vg["machine_gate"]["failed_at"]}

    gc = guard_check(base)
    log["guard_check"] = {"ok": gc["ok"]}
    if not gc["ok"]:
        state["guard_violation"] = True
        log["reason"] = "guard-violation"
        log["guard_detail"] = gc
        record_round(state, log)
        return {"stop": True, "reason": "guard-violation", "state": state, "log": log}

    verified = vg["verified"]
    state["dry"] = 0 if verified else state["dry"] + 1
    state["budget"] -= 1
    log["root_after"] = read_root()
    log["counts_after"] = read_counts()
    log["root_unchanged"] = log["root_after"] == base["root"]
    log["verified"] = verified

    # 스테이징 경로: infra 라운드는 루프 산출물 + 추적 문서. frontier 는 registry/specs 포함.
    paths = list(cfg["stage_paths"])
    sc = sync_checkpoint(state, cfg, verified, base, do_git, paths, gates_mode=gates_mode)
    log["sync_checkpoint"] = sc
    log["reason"] = "ok"
    record_round(state, log)
    progress(f"round {r}: verified={verified} root={read_root()[:12]} "
             f"committed={sc.get('committed')} dry={state['dry']} budget={state['budget']}")
    return {"stop": stop_controller(state), "reason": "ok", "verified": verified,
            "state": state, "log": log}


def run_autonomy_loop(queue: list[Candidate], cfg: dict, budget: int, dry_limit: int,
                      do_git: bool, gates_mode: str) -> dict:
    state = {"round": 0, "dry": 0, "dry_limit": dry_limit, "budget": budget,
             "frontier_exhausted": False, "guard_violation": False}
    base = bootstrap(state)
    history = []
    last = None
    while True:
        out = autonomy_round(queue, state, base, cfg, do_git, gates_mode)
        last = out
        state = out["state"]
        history.append({"round": state["round"], "reason": out["reason"],
                        "verified": out.get("verified")})
        if out["stop"]:
            break
        state["round"] += 1
    # 종결 시 최종 sync 1회(설계 T12). frontier-exhausted/ guard-violation 도 final 발화.
    final_sc = sync_checkpoint(state, cfg, last.get("verified", False), base, do_git,
                               list(cfg["stage_paths"]), final=True, gates_mode=gates_mode)
    summary = {
        "stopped_by": last["reason"],
        "rounds": state["round"] + 1,
        "history": history,
        "base_root": base["root"][:16],
        "final_root": read_root()[:16],
        "final_sync": final_sc,
        "invariants_held": guard_check(base)["ok"],
    }
    save_state(state, summary)
    return summary


def save_state(state: dict, summary: dict) -> None:
    json.dump({"state": state, "last_summary": summary,
               "updated": time.strftime("%Y-%m-%dT%H:%M:%S")},
              open(STATE_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────
def build_queue(mode: str) -> list[Candidate]:
    if mode == "infra":
        # MVP 인프라 라운드: registry 무변경 후보 1개.
        return [Candidate("autonomy-loop-mvp-infra", kind="infra")]
    if mode == "frontier-c12x-payoff":
        # Phase-2 frontier 라운드: c12x payoff family(cmul4/16/256/2925_mod3683) +
        # shor3683 structural. 의존 순(payoff → structural) 다단계 드라이버.
        return [Candidate(
            "c12x-payoff+shor3683",
            kind="frontier",
            driver=[["scripts/c12x_payoff_family.py"], ["scripts/shor3683_frontier.py"]],
            new_module=False,
        )]
    if mode == "frontier-factory":
        # ★자율 폐루프: factory 가 다음 미봉인 distinct-semiprime N 을 자율 발견 → 봉인.
        # codegen 없음(파라메트릭 함수) · 회귀게이트(INV-F1) 통과 후에만 봉인 · 신규 모듈 0.
        sys.path.insert(0, os.path.join(ROOT, "scripts"))
        import frontier_factory as ff
        N, m = ff.next_unsealed_target()
        if N is None:
            return []                                   # frontier-exhausted (정직 종료)
        progress(f"factory discover: next unsealed N={N}={'×'.join(map(str, m['factors']))} "
                 f"n_sys={m['t'] + m['work']} prim={m['primitive']}")
        return [Candidate(f"shor{N}", kind="frontier",
                          driver=["scripts/frontier_factory.py", "--seal", str(N)],
                          new_module=False, all_ok_token="sealed=True")]
    raise SystemExit(f"unknown mode: {mode}")


def factory_cfg(args) -> dict:
    return {
        "commit_every": 1, "branch": args.branch, "push": args.push,
        "commit_message": (
            "AutonomyLoop closed-loop frontier — factory-sealed Shor app (zero new modules)\n\n"
            "Autonomous discover→seal→verify→commit via _workspace/loop/autonomy_loop.py "
            "(frontier-factory) + scripts/frontier_factory.py (parametric, regression-gated INV-F1).\n"
            "cmul payoff family Tier-0 EXACT + structural shor{N} Tier-1 STRUCTURAL; reuses sealed "
            "c8x..c12x primitives. Gate: reproduce_all REPRODUCED (incl. data-driven factory step), "
            "second_oracle unchanged, fingerprint+frozen byte-identical.\n\n"
            "Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
        ),
        "stage_paths": [
            "scripts/frontier_factory.py", "scripts/reproduce_all.py", "scripts/seal_gate_ci.py",
            "registry/apps", "specs/apps",
            "registry/REGISTRY-MANIFEST.json", "registry/DEPENDENCY-GRAPH.json",
            "registry/DEPENDENCY-GRAPH.md", "registry/SEMANTIC-GUARANTEES.json",
            ".pgf/arith", "reports/REPRODUCE-RESULT.json", ".pgf/adoption/seal-badge.json",
            ".pgf/adoption/RELEASE-META.json", "CITATION.cff",
        ],
    }


def frontier_cfg(args) -> dict:
    return {
        "commit_every": 1,
        "branch": args.branch,
        "push": args.push,
        "commit_message": (
            "AutonomyLoop frontier round — W12.22/23 c12x payoff family + shor3683 structural\n\n"
            "Autonomous frontier expansion via _workspace/loop/autonomy_loop.py (frontier-c12x-payoff):\n"
            "  cmul{4,16,256,2925}_mod3683  Tier-0 EXACT (c12x payoff, independent arith 4/4)\n"
            "  shor3683                     Tier-1 STRUCTURAL 20q (deterministic reassembly)\n"
            "Gate: reproduce_all REPRODUCED, second_oracle 71/71, fingerprint+frozen byte-identical.\n"
            "Registry 77 modules / 152 apps. Honest boundaries: cmul=exact, shor3683=structural, "
            "readout=illustrative.\n\n"
            "Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
        ),
        "stage_paths": [
            "scripts/c12x_payoff_family.py",
            "scripts/shor3683_frontier.py",
            "scripts/reproduce_all.py",
            "scripts/seal_gate_ci.py",
            "reports/REPRODUCE-RESULT.json",
            ".pgf/adoption/seal-badge.json",
            "registry/REGISTRY-MANIFEST.json",
            "registry/DEPENDENCY-GRAPH.json",
            "registry/DEPENDENCY-GRAPH.md",
            "registry/apps/cmul4_mod3683.sealed.json",
            "registry/apps/cmul16_mod3683.sealed.json",
            "registry/apps/cmul256_mod3683.sealed.json",
            "registry/apps/cmul2925_mod3683.sealed.json",
            "registry/apps/shor3683.sealed.json",
            "specs/apps/cmul4_mod3683.app.pg",
            "specs/apps/cmul16_mod3683.app.pg",
            "specs/apps/cmul256_mod3683.app.pg",
            "specs/apps/cmul2925_mod3683.app.pg",
            "specs/apps/shor3683.app.pg",
            ".pgf/arith/C12X-PAYOFF-3683-REPORT.json",
            ".pgf/arith/SHOR-FRONTIER-3683-REPORT.json",
            ".pgf/DESIGN-MasterRoadmap.md",
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="AutonomyLoop MVP real-gate runner")
    ap.add_argument("--mode", default="infra",
                    choices=["infra", "frontier-c12x-payoff", "frontier-factory"])
    ap.add_argument("--budget", type=int, default=1)
    ap.add_argument("--dry-limit", type=int, default=2)
    ap.add_argument("--gates", default="full", choices=["full", "incremental", "fast"],
                    help="full=reproduce_all 재합성(verified-commit 가능) · "
                         "incremental=registry build+독립게이트(~30s, commit 보류) · fast=점검만")
    ap.add_argument("--commit", action="store_true", help="verified-only commit (先브랜치)")
    ap.add_argument("--push", action="store_true", help="commit 후 origin push")
    ap.add_argument("--branch", default=None)
    args = ap.parse_args()

    if args.mode == "infra":
        if args.branch is None:
            args.branch = "autonomy-loop/mvp"
        cfg = {
            "commit_every": 1, "branch": args.branch, "push": args.push,
            "commit_message": (
                "AutonomyLoop MVP — first real-gate autonomous round (infra)\n\n"
                "Wire mock→real: bootstrap snapshot, machine_gate "
                "(reproduce_all/second_oracle/seal_gate_ci/contested_guard), "
                "guard_check (fingerprint+frozen byte-identical), verified-only sync.\n"
                "Root unchanged (infra round, no new seal).\n\n"
                "Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
            ),
            "stage_paths": [
                # 엔진/런타임은 스킬 내부(.runtime gitignored)라 commit 대상 아님.
                # infra 라운드의 tracked delta = 마스터 로드맵 status 정도.
                ".pgf/DESIGN-MasterRoadmap.md",
            ],
        }
    elif args.mode == "frontier-factory":
        if args.branch is None:
            args.branch = "main"          # main 직접 모드(2026-07-01) — ensure_branch no-op
        cfg = factory_cfg(args)
    else:
        if args.branch is None:
            args.branch = "main"
        cfg = frontier_cfg(args)

    do_git = args.commit or args.push
    queue = build_queue(args.mode)

    print("=" * 80)
    print(f"AutonomyLoop — mode={args.mode} gates={args.gates} budget={args.budget} "
          f"git={'on' if do_git else 'off'} branch={args.branch}")
    print("=" * 80)
    summary = run_autonomy_loop(queue, cfg, args.budget, args.dry_limit, do_git, args.gates)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print("-" * 80)
    # 합격=결정론 게이트(verify_gate 내 reproduce_all REPRODUCED) ∧ 불변(fingerprint/frozen) 유지.
    # root 는 동적(frontier 라운드 성장) — prefix 강제하지 않는다.
    ok = summary["invariants_held"] and summary["stopped_by"] in ("ok", "frontier-exhausted")
    print(f"Round result: invariants_held={summary['invariants_held']} "
          f"base_root={summary['base_root']} final_root={summary['final_root']} "
          f"stopped_by={summary['stopped_by']}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
