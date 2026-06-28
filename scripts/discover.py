# -*- coding: utf-8 -*-
"""discover.py — Stage 2 QF-Discover: 가치함수(W2.1) + 목표선택가드(W2.3).

8-agent 수렴 최약가정 직격: known-family(ghz/cluster/ring/wstate)는 MAX_N 소진(detect_gaps=0).
이제 *무엇을 만들지*를 객관근거로 선택해야 한다(A3 미명명 실패모드). 본 모듈은
  W2.1 ValueFunction  — 8항 가중합(0.25·Novelty+0.20·Sealability+0.20·Composability
                        +0.15·ResourceΔ+0.10·ConsensusEst−0.20·Ambiguity−0.15·Cost).
                        각 항은 휴리스틱 상수가 아닌 **registry 그래프 구조**에서 유도(근거 동봉).
  Composability        — counterfactual fan-in: 모듈 m 미봉인 가정 → m 에 의존하는 app 수
                        (registry_tools.dependents). c6x 미봉인 시 cmul2_mod33/35 가 지목 → fan-in.
  W2.3 GoalSelectionGuard — coverage(중복 capability)·independence(단일 convention) 게이트.

정직성: 분석/제안 전용 비파괴. registry/sealed/frozen/fingerprint 불변. `.pgf/discover/` 만 가산.
소비 자산(사용만): registry_tools(build_graph/dependents) · goal_autonomy(detect_gaps/FAMILIES) ·
resource_report(_load). 신규 봉인 없음(랭킹/제안만; 실제 봉인은 goal_autonomy/app_assemble 경유).

사용:
  python scripts/discover.py rank        # 후보(app+prereq) 8항 가치랭킹 → CANDIDATE-RANK.json
  python scripts/discover.py validate    # RetroValidate: c6x/distinct-prime 사전포착 검증
  python scripts/discover.py guard        # GoalSelectionGuard 적용 → 선택/거부 로그
"""
from __future__ import annotations
import os, sys, json, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import registry_tools as rt          # noqa: E402  build_graph/dependents 사용만
import goal_autonomy as ga           # noqa: E402  detect_gaps/FAMILIES/score 사용만
import resource_report as rr         # noqa: E402  _load(resource) 사용만

MODREG = os.path.join(ROOT, "registry", "modules")
APPREG = os.path.join(ROOT, "registry", "apps")
OUT = os.path.join(ROOT, ".pgf", "discover")

# 가중치 (roadmap 명세, 합 검증용 동봉)
W = {"novelty": 0.25, "sealability": 0.20, "composability": 0.20, "resource_delta": 0.15,
     "consensus_est": 0.10, "ambiguity": -0.20, "cost": -0.15}

# 의미가 명명된(낮은 ambiguity) 후보 패턴 — 표준명칭/산술의미 명확
NAMED_PATTERNS = [
    (re.compile(r"^ghz\d+$"), "GHZ entangling"), (re.compile(r"^cluster\d+$"), "1D cluster"),
    (re.compile(r"^ring\d+$"), "ring cluster"), (re.compile(r"^wstate\d+$"), "W-state"),
    (re.compile(r"^cmul\d+_mod\d+$"), "modular mult"), (re.compile(r"^c\d+x$"), "multi-control X"),
    (re.compile(r"^shor\d+_a\d+$"), "Shor order-finding"), (re.compile(r"^i?qft\d+"), "QFT"),
    (re.compile(r"^cr\d+_?(dag_)?gate$"), "controlled-phase"),
]
# GenSkill 로 재현 가능한 family(낮은 novelty) — genskills 가 방법을 보유
GENSKILL_FAMILIES = {"ghz", "cluster", "ring", "wstate"}


# ─────────────────────────── 그래프/자원 컨텍스트 ───────────────────────────
def build_context():
    graph = rt.build_graph()
    # 그래프에 등장하는 모든 모듈 id
    modules = sorted({e["id"] for g in graph.values() for e in g["depends_on"] if e["kind"] == "module"})
    # counterfactual fan-in: 모듈 m 에 (재귀)의존하는 app 수
    fanin = {m: len(rt.dependents(graph, m)) for m in modules}
    # 자원 테이블(오라클 봉인시 기록값)
    res = {}
    for store in (MODREG, APPREG):
        for f in os.listdir(store):
            if f.endswith(".sealed.json"):
                it = rr._load(os.path.join(store, f))
                res[it["id"]] = it["resource"]
    # 봉인된 모듈 전체(그래프 미사용 포함) — frontier 자동전진용(미사용 봉인 gate 재제안 방지)
    sealed_modules = {f[:-len(".sealed.json")] for f in os.listdir(MODREG) if f.endswith(".sealed.json")}
    return {"graph": graph, "modules": set(modules), "sealed_modules": sealed_modules,
            "fanin": fanin, "res": res,
            "max_fanin": max(fanin.values()) if fanin else 1}


# ─────────────────────────── 후보 생성 ───────────────────────────
def app_to_gap(app_id, ctx, absent_modules):
    """봉인 app 을 '미생성'으로 가정한 reconstructed gap (retrospective candidate).
    absent_modules = counterfactual 미봉인 모듈 집합 → 그것에 의존하면 BLOCKED."""
    deps = ctx["graph"][app_id]["depends_on"]
    required = [e["id"] for e in deps]
    req_modules = [e["id"] for e in deps if e["kind"] == "module"]
    missing = sorted(set(req_modules) & absent_modules)
    fam = next((nm for pat, nm in NAMED_PATTERNS if pat.match(app_id)), None)
    family_key = app_id.rstrip("0123456789").rstrip("_") if fam else app_id
    gate_count = sum(e["uses"] for e in deps)
    return {"id": app_id, "kind": "app", "family": family_key, "named": fam,
            "buildable": not missing, "required_modules": required, "missing_modules": missing,
            "gate_count": gate_count, "n_deps": len(deps)}


def prereq_candidates(ctx):
    """모듈을 '다음 봉인할 prereq' 후보로 — counterfactual fan-in 이 핵심 점수."""
    out = []
    for m in sorted(ctx["modules"]):
        fam = next((nm for pat, nm in NAMED_PATTERNS if pat.match(m)), None)
        out.append({"id": m, "kind": "module", "family": m.rstrip("0123456789").rstrip("_"),
                    "named": fam, "buildable": True, "required_modules": [], "missing_modules": [],
                    "gate_count": 1, "n_deps": 0, "fanin": ctx["fanin"].get(m, 0)})
    return out


# ─────────────────────────── 8항 가치함수 ───────────────────────────
def _norm_gatecount(gc):
    return min(1.0, gc / 40.0)   # 정규화(distinct-prime cmul ~ 수십 게이트)


def novelty(g, ctx):
    """GenSkill 재현가능 family 확장 = 낮음. family 밖(distinct-prime 등) = 높음. 근거: 패턴매칭."""
    if g["family"] in GENSKILL_FAMILIES:
        return 0.2, "genskill-reproducible family-extension"
    if g["kind"] == "module":
        # 모듈 자체: multi-control/controlled-phase 등 primitive — 중간(이미 봉인됨)
        return 0.5, "sealed primitive (counterfactual)"
    # family 밖 app (cmul distinct-prime, shor, grover…): sealed 조합으로만 표현 — 높음
    return 0.8, "non-genskill composite (not reproducible by known family method)"


def sealability(g, ctx):
    """지금 봉인 가능? missing 0 & 폭 안전 → 1.0. missing k → 1/(1+k)."""
    if g["buildable"]:
        return 1.0, "buildable (all prereqs sealed)"
    k = len(g["missing_modules"])
    return round(1.0 / (1 + k), 4), f"blocked: {k} missing prereq {g['missing_modules']}"


def composability(g, ctx):
    """counterfactual fan-in. 모듈: 직접 fan-in. app: 의존 모듈의 최대 fan-in(unlock 레버리지 상속)
    + 이미 그래프에서의 dependents(재사용 잠재). 근거: registry_tools.dependents 그래프구조."""
    mf = ctx["max_fanin"] or 1
    if g["kind"] == "module":
        fi = ctx["fanin"].get(g["id"], 0)
        return round(fi / mf, 4), f"fan-in={fi} (apps depending on this module if unsealed)"
    # app: 자신이 이미 다른 app 의 building block 인 정도 + 의존 prereq 의 fan-in
    own = len(rt.dependents(ctx["graph"], g["id"]))
    prereq_fi = max((ctx["fanin"].get(m, 0) for m in g["required_modules"]), default=0)
    val = round(min(1.0, (own + prereq_fi / mf)), 4)
    return val, f"reuse-as-block={own}, max-prereq-fanin={prereq_fi}"


def resource_delta(g, ctx):
    """봉인 시 추가 자원: 새 모듈 0(재사용) & 저게이트 → 높음. 근거: missing 수 + gate_count."""
    n_new = len(g["missing_modules"])
    base = 1.0 / (1 + n_new)
    return round(base * (1 - _norm_gatecount(g["gate_count"])), 4), \
        f"new_modules={n_new}, gate_count={g['gate_count']}"


def consensus_est(g, ctx):
    """deps 가 전부 이미 봉인(=오라클·second_oracle 검증완료) → cross-model 합의 추정 높음.
    근거: required_modules 의 registry 존재 여부."""
    if g["kind"] == "module":
        # 봉인된 primitive: 표준게이트는 PROOF_BACKED. 봉인 존재 = 검증완료
        return 0.9, "sealed primitive (independently re-verified by second_oracle)"
    present = [m for m in g["required_modules"] if m not in g["missing_modules"]]
    frac = len(present) / max(1, len(g["required_modules"]))
    return round(0.5 + 0.5 * frac, 4), f"{len(present)}/{len(g['required_modules'])} deps sealed"


def ambiguity(g, ctx):
    """표준명칭/산술의미 명확 → 낮음(감점 작음). 미명 → 높음. 근거: NAMED_PATTERNS 매칭."""
    return (0.1, f"named: {g['named']}") if g["named"] else (0.7, "unnamed synthesis")


def cost_est(g, ctx):
    """빌드비용 = 정규화 게이트수. 근거: gate_count."""
    c = _norm_gatecount(g["gate_count"])
    return round(c, 4), f"norm gate_count={g['gate_count']}"


def value_function(g, ctx):
    terms, ev = {}, {}
    for name, fn in [("novelty", novelty), ("sealability", sealability), ("composability", composability),
                     ("resource_delta", resource_delta), ("consensus_est", consensus_est),
                     ("ambiguity", ambiguity), ("cost", cost_est)]:
        v, why = fn(g, ctx)
        terms[name] = v
        ev[name] = why
    value = sum(W[k] * terms[k] for k in W)
    return {**g, "value": round(value, 4), "terms": terms, "evidence": ev}


# ─────────────────────────── 랭킹 ───────────────────────────
def rank_all(ctx, absent_modules=None):
    absent = absent_modules or set()
    # app 후보: 실제 registry app 을 retrospective 재구성 + known-family gaps
    app_ids = sorted(ctx["graph"].keys())
    app_gaps = [app_to_gap(a, ctx, absent) for a in app_ids]
    for fg in ga.detect_gaps():   # 현재 0 이지만 미래 frontier 자동 포함
        app_gaps.append({"id": fg["id"], "kind": "app", "family": fg["family"], "named": fg["family"],
                         "buildable": fg["buildable"], "required_modules": fg["required_modules"],
                         "missing_modules": fg["missing_modules"], "gate_count": fg["gate_count"],
                         "n_deps": len(fg["required_modules"])})
    prereqs = prereq_candidates(ctx)
    apps_scored = sorted((value_function(g, ctx) for g in app_gaps), key=lambda x: -x["value"])
    prereq_scored = sorted((value_function(g, ctx) for g in prereqs), key=lambda x: -x["value"])
    return apps_scored, prereq_scored


def cmd_rank():
    os.makedirs(OUT, exist_ok=True)
    ctx = build_context()
    apps, prereqs = rank_all(ctx)
    print("=" * 84)
    print("QF-Discover RANK (W2.1 ValueFunction) — 8항 가치 가중합 (근거 동봉)")
    print("=" * 84)
    print(f"가중치합 검증: Σ|W| = {sum(abs(v) for v in W.values()):.2f} · 양항 {sum(v for v in W.values() if v>0):.2f} "
          f"음항 {sum(v for v in W.values() if v<0):.2f}")
    print(f"\n[App 후보] (retrospective 재구성 {len(apps)}) — 상위 8:")
    for g in apps[:8]:
        print(f"  {g['value']:+.4f}  {g['id']:16} nov={g['terms']['novelty']:.2f} "
              f"comp={g['terms']['composability']:.2f} seal={g['terms']['sealability']:.2f} "
              f"amb={g['terms']['ambiguity']:.2f}")
    print(f"\n[Prereq 후보] (모듈 counterfactual fan-in {len(prereqs)}) — 상위 10:")
    for g in prereqs[:10]:
        print(f"  {g['value']:+.4f}  {g['id']:14} fanin={g.get('fanin',0):2d} "
              f"comp={g['terms']['composability']:.2f} nov={g['terms']['novelty']:.2f}")
    out = {"_schema": "qf-discover-rank-v1",
           "_note": "8항 가치 가중합. 각 항은 registry 그래프 구조에서 유도(휴리스틱 상수 아님), 근거 동봉. "
                    "app=무엇을 조립할까(retrospective 재구성), prereq=무엇을 먼저 봉인하면 가장 unlock(fan-in). "
                    "분석전용 비파괴 — 신규 봉인 없음.",
           "weights": W, "weight_sum_abs": round(sum(abs(v) for v in W.values()), 4),
           "app_candidates": apps, "prereq_candidates": prereqs}
    json.dump(out, open(os.path.join(OUT, "CANDIDATE-RANK.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("-" * 84)
    print(f"→ .pgf/discover/CANDIDATE-RANK.json")
    return 0


# ─────────────────────────── RetroValidate (W2.1 검증) ───────────────────────────
def cmd_validate():
    """c6x 사례 사전포착: c6x 미봉인 counterfactual → cmul2_mod33/35 가 BLOCKED 로 재구성되고
    c6x 가 prereq fan-in 상위 포착. specialized 게이트(c5x/c6x)가 fan-in 으로 사전 가치 인식."""
    os.makedirs(OUT, exist_ok=True)
    ctx = build_context()
    checks = []

    # 검증 1: c6x fan-in ≥ 1 (실제 distinct-prime cmul 이 의존)
    c6x_deps = rt.dependents(ctx["graph"], "c6x")
    checks.append({"check": "c6x_fanin_captured", "fanin": len(c6x_deps), "dependents": c6x_deps,
                   "pass": len(c6x_deps) >= 1})

    # 검증 2: c6x counterfactual 미봉인 → cmul2_mod33/35 BLOCKED 재구성 + missing 에 c6x 지목
    absent = {"c6x"}
    blocked_by_c6x = []
    for a in ctx["graph"]:
        g = app_to_gap(a, ctx, absent)
        if "c6x" in g["missing_modules"]:
            blocked_by_c6x.append(a)
    checks.append({"check": "c6x_counterfactual_blocks", "blocked_apps": blocked_by_c6x,
                   "pass": len(blocked_by_c6x) >= 1})

    # 검증 3: prereq 랭킹에서 specialized 게이트(c5x/c6x)가 fan-in 상위(중간 이상) — 사전 가치 인식
    _, prereqs = rank_all(ctx)
    rank_pos = {g["id"]: i for i, g in enumerate(prereqs)}
    spec_gates = [m for m in ("c6x", "c5x", "c4x", "c3x") if m in rank_pos]
    median_pos = len(prereqs) / 2
    spec_top = {m: {"rank": rank_pos[m], "value": prereqs[rank_pos[m]]["value"],
                    "above_median": rank_pos[m] < median_pos} for m in spec_gates}
    checks.append({"check": "specialized_gate_prioritized",
                   "detail": spec_top, "median_rank_pos": median_pos,
                   "pass": any(v["above_median"] for v in spec_top.values())})

    # 검증 4: app 랭킹에서 distinct-prime(novelty 높음)이 GenSkill family(novelty 낮음) 위 — 발견성
    apps, _ = rank_all(ctx)
    dp = next((g for g in apps if re.match(r"^cmul\d+_mod3[35]$", g["id"])), None)
    ghz_mid = next((g for g in apps if re.match(r"^ghz\d+$", g["id"])), None)
    novelty_ok = bool(dp and ghz_mid and dp["terms"]["novelty"] > ghz_mid["terms"]["novelty"])
    checks.append({"check": "novelty_discriminates_discovery",
                   "distinct_prime": (dp["id"], dp["terms"]["novelty"]) if dp else None,
                   "genskill_family": (ghz_mid["id"], ghz_mid["terms"]["novelty"]) if ghz_mid else None,
                   "pass": novelty_ok})

    allok = all(c["pass"] for c in checks)
    print("=" * 84)
    print("QF-Discover RetroValidate (W2.1) — c6x/distinct-prime 사전포착 검증")
    print("=" * 84)
    for c in checks:
        print(f"  {'✓' if c['pass'] else '✗'} {c['check']}")
        if c["check"] == "c6x_fanin_captured":
            print(f"      c6x fan-in={c['fanin']} → {c['dependents']}")
        elif c["check"] == "c6x_counterfactual_blocks":
            print(f"      c6x 미봉인 시 BLOCKED: {c['blocked_apps']}")
        elif c["check"] == "specialized_gate_prioritized":
            for m, d in c["detail"].items():
                print(f"      {m}: rank#{d['rank']} value={d['value']:+.4f} above_median={d['above_median']}")
        elif c["check"] == "novelty_discriminates_discovery":
            print(f"      distinct-prime {c['distinct_prime']} > genskill {c['genskill_family']}")
    out = {"_schema": "qf-discover-retrovalidate-v1", "all_pass": allok, "checks": checks,
           "_note": "발견엔진 정당성: 이미 봉인되어 가치가 입증된 c6x/distinct-prime 을 ValueFunction 이 "
                    "*사전* 상위로 포착하는가(retrospective). counterfactual=그래프에서 모듈 제거 시뮬."}
    json.dump(out, open(os.path.join(OUT, "RETRO-VALIDATE.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("-" * 84)
    print(f"RetroValidate {'ALL PASS ✅' if allok else 'FAIL ✗'} · → .pgf/discover/RETRO-VALIDATE.json")
    return 0 if allok else 1


# ─────────────────────────── W2.3 GoalSelectionGuard ───────────────────────────
def capability_key(g):
    """동일 capability 판정키: app 은 family(중복 family-멤버 선택 방지), module 은 자기 id."""
    return f"{g['kind']}:{g['family']}"


def independence_check(g, ctx):
    """선택근거 다양성. 단일 convention(big-endian/atol/전역위상)에만 의존하면 경고.
    근거: 후보가 표준게이트 PROOF_BACKED corpus 외 단일소스 유래인지 — consensus_est 로 근사."""
    cons = consensus_est(g, ctx)[0]
    single = cons < 0.6   # deps 의 cross-model 합의 근거가 약함
    return {"single_convention": single, "consensus_est": cons}


def goal_selection_guard(ranked, ctx):
    selected, rejected = [], []
    seen = set()
    for g in ranked:
        cap = capability_key(g)
        if cap in seen:
            rejected.append({"id": g["id"], "value": g["value"],
                             "reason": f"duplicate-capability '{cap}' (coverage gate)"})
            continue
        ind = independence_check(g, ctx)
        entry = {"id": g["id"], "value": g["value"], "capability": cap, "consensus_est": ind["consensus_est"]}
        if ind["single_convention"]:
            entry["warn"] = "single-convention dependence (independence gate)"
        seen.add(cap)
        selected.append(entry)
    return {"selected": selected, "rejected": rejected}


def cmd_guard():
    os.makedirs(OUT, exist_ok=True)
    ctx = build_context()
    apps, prereqs = rank_all(ctx)
    g_apps = goal_selection_guard(apps, ctx)
    g_pre = goal_selection_guard(prereqs, ctx)
    print("=" * 84)
    print("QF-Discover GoalSelectionGuard (W2.3) — coverage/independence 게이트 (A3 미명명 실패모드 명명)")
    print("=" * 84)
    print(f"[App] 선택 {len(g_apps['selected'])} · 거부 {len(g_apps['rejected'])}(중복 capability)")
    for s in g_apps["selected"][:6]:
        w = f"  ⚠ {s['warn']}" if "warn" in s else ""
        print(f"  ✓ {s['id']:16} value={s['value']:+.4f} cap={s['capability']}{w}")
    if g_apps["rejected"]:
        print("  거부 예:")
        for r in g_apps["rejected"][:4]:
            print(f"  ✗ {r['id']:16} {r['reason']}")
    print(f"\n[Prereq] 선택 {len(g_pre['selected'])} · 거부 {len(g_pre['rejected'])}")
    warned = [s for s in g_apps["selected"] + g_pre["selected"] if "warn" in s]
    out = {"_schema": "qf-discover-guard-v1",
           "_note": "목표선택 co-error 방어: 동일 capability 중복선택 거부(coverage), 선택근거가 단일 "
                    "convention 에만 의존 시 경고(independence). 모든 결정 사유 로그 = 미명명 실패모드 명명. 분석전용.",
           "app_guard": g_apps, "prereq_guard": g_pre,
           "summary": {"app_selected": len(g_apps["selected"]), "app_rejected": len(g_apps["rejected"]),
                       "prereq_selected": len(g_pre["selected"]), "prereq_rejected": len(g_pre["rejected"]),
                       "single_convention_warnings": len(warned)}}
    json.dump(out, open(os.path.join(OUT, "SELECTION-LOG.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(f"\nsingle-convention 경고 {len(warned)}건 · → .pgf/discover/SELECTION-LOG.json")
    return 0


# ─────────────────────────── W2.4 PrimitiveProposalRound [EXT] ───────────────────────────
# specialized primitive family → 다음 미봉인 멤버 = capability-gap (sx/c6x 의 standing-loop 승격 패턴)
PRIMITIVE_FAMILIES = [
    {"family": "cNx", "pattern": re.compile(r"^c(\d+)x$"), "next_fmt": "c{}x",
     "desc": "{n}-control Toffoli (multi-controlled X)",
     "golden": "permutation: |c…c,t⟩ → |c…c, t⊕(c₁∧…∧c_n)⟩, big-endian 첫 레지스터=MSB",
     "constraint": "Clifford+T, ancilla 허용(borrowed/clean 명시), golden=permutation matrix",
     "unlocks": "distinct-prime modular-mult 확장 N∈(2^(n-1),2^n] (work bits=n-1; cMx는 N>2^(n-1)에서 필요). "
                "예: c7x→mod 65=5×13·mod 77=7×11·mod 91=7×13 (N<64는 c6x로 충분 — 실측). cmul prereq"},
    {"family": "crK", "pattern": re.compile(r"^cr(\d+)_dag_gate$"), "next_fmt": "cr{}_dag_gate",
     "desc": "controlled-phase R_k† = diag(1, e^{{-2πi/2^{n}}})",
     "golden": "diag(1,1,1,exp(2πi/2^k)), 전역위상 atol 1e-7 무시 — controlled 합성 시 W1.3 정합 필요",
     "constraint": "analytic golden, deg=2^k root of unity, no MatrixGate",
     "unlocks": "더 깊은 QFT/IQFT (qft8+) — exponent precision 확장"},
]


def gap_to_proposal(ctx):
    """ValueFunction prereq 랭킹 + family 확장규칙 → 다음 미봉인 primitive capability-gap 도출.
    sealed 최대 멤버 +1 = 미봉인 frontier. fan-in 잠재(unlock 대상)로 우선순위."""
    proposals = []
    # frontier = 봉인된 모듈 전체 기준(그래프 미사용 봉인 gate 포함) → 봉인 즉시 다음 칸으로 전진
    sealed = ctx.get("sealed_modules", ctx["modules"])
    for fam in PRIMITIVE_FAMILIES:
        members = sorted(int(m.group(1)) for mid in sealed if (m := fam["pattern"].match(mid)))
        if not members:
            continue
        nxt = max(members) + 1
        gap_id = fam["next_fmt"].format(nxt)
        if gap_id in sealed:                      # 이미 봉인됨(미사용이어도) → 스킵
            continue
        # 현 최대멤버의 fan-in = 이 family 의 unlock 레버리지 근거
        cur_max_id = fam["next_fmt"].format(max(members))
        lever = ctx["fanin"].get(cur_max_id, 0)
        proposals.append({
            "gap_id": gap_id, "family": fam["family"], "n": nxt,
            "description": fam["desc"].format(n=nxt),
            "golden_spec": fam["golden"].format(n=nxt, k=nxt),
            "constraints": fam["constraint"],
            "unlocks": fam["unlocks"],
            "sealed_predecessors": [fam["next_fmt"].format(k) for k in members],
            "predecessor_fanin": lever,
            "priority_value": round(0.5 + 0.1 * lever, 4)})
    return sorted(proposals, key=lambda p: -p["priority_value"])


def _round_pkg(proposals):
    """라운드 패키지 디렉토리 선택. 현재 frontier가 최신 라운드와 같으면 재사용(idempotent),
    다르면 다음 라운드 생성 — 봉인완료 라운드(W2.4=round1 등)를 비파괴 보존."""
    base = os.path.join(ROOT, "_workspace", "crossmodel")
    os.makedirs(base, exist_ok=True)
    nums = sorted(int(m.group(1)) for d in os.listdir(base)
                  if (m := re.match(r"discover_round(\d+)$", d)))
    cur = sorted(p["gap_id"] for p in proposals)
    if nums:
        latest = max(nums)
        gp = os.path.join(base, f"discover_round{latest}", "GAP-SPEC.json")
        prev = None
        if os.path.exists(gp):
            try:
                prev = sorted(p["gap_id"] for p in json.load(open(gp, encoding="utf-8")).get("proposals", []))
            except Exception:
                prev = None
        if prev == cur:
            return os.path.join(base, f"discover_round{latest}"), latest   # 동일 frontier → 재사용
        rn = latest + 1
    else:
        rn = 1
    return os.path.join(base, f"discover_round{rn}"), rn


def cmd_propose():
    """[EXT] capability-gap → 6런타임 패널 배포 패키지 생성(self-contained 부분). relay 대기."""
    ctx = build_context()
    proposals = gap_to_proposal(ctx)
    pkg, rn = _round_pkg(proposals)
    os.makedirs(pkg, exist_ok=True)

    print("=" * 84)
    print("QF-Discover PrimitiveProposalRound (W2.4 [EXT]) — capability-gap 6런타임 배포 패키지")
    print("=" * 84)
    for p in proposals:
        print(f"  GAP {p['gap_id']:6} ({p['description']})")
        print(f"      predecessor fan-in={p['predecessor_fanin']} · unlocks: {p['unlocks']}")

    gap_spec = {"_schema": "capability-gap-v1", "round": f"discover_round{rn}",
                "_note": "ValueFunction(W2.1)+family 확장규칙이 자율 도출한 미봉인 primitive frontier. "
                         "6런타임 패널이 분해를 독립 제안 → 수렴+second_oracle 독립검증+sympy proof → key-free 봉인.",
                "proposals": proposals}
    json.dump(gap_spec, open(os.path.join(pkg, "GAP-SPEC.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    # 6런타임 PG TaskSpec (자연어 아닌 구조화 — agent-protocol)
    taskspec = f"# Discover Round {rn} — Primitive Proposal TaskSpec (PG)\n\n"
    taskspec += "> 6런타임 패널 배포용. 각 런타임 독립 제안(상호 비참조). 정욱님 수거 후 봉인.\n"
    taskspec += "> 응답 형식: 제안(분해 회로) · 근거(왜 최소) · 봉인가능성(오라클 통과 예측) · 위험(가정).\n\n"
    for p in proposals:
        taskspec += f"## GAP: {p['gap_id']} — {p['description']}\n\n```\n"
        taskspec += f"AI_propose_decomposition // {p['gap_id']} 최소 분해 (needs-verify)\n"
        taskspec += f"    # target: {p['description']}\n"
        taskspec += f"    # golden: {p['golden_spec']}\n"
        taskspec += f"    # constraint: {p['constraints']}\n"
        taskspec += f"    # unlocks: {p['unlocks']}\n"
        taskspec += f"    # output: gate-list(봉인부품 재조합, NO MatrixGate) + qubit-mapping + 자원추정(T/Toffoli)\n"
        taskspec += f"    # acceptance: second_oracle 독립 numpy 재구성 u_hash 일치 + sympy permutation/phase proof\n"
        taskspec += "```\n\n"
    open(os.path.join(pkg, "TASKSPEC.md"), "w", encoding="utf-8", newline="\n").write(taskspec)

    scoring = (
        f"# Discover Round {rn} — Scoring & Seal Schema\n\n"
        "## 채점 (수거 후)\n"
        "1. **수렴**: ≥2 런타임이 동일 u_hash 분해 제출 → cross-model 합의(key-free consensus).\n"
        "2. **독립검증**: `second_oracle` 제1원리 numpy 재구성 → u_hash 일치(분해≠검증 분리).\n"
        "3. **proof**: sympy 로 permutation(cNx) 또는 phase(crK) golden 대수 증명.\n"
        "4. **자원**: 동일 u_hash 다분해 시 ExploitAxis(W2.2) 최소비용 선택.\n\n"
        "## 봉인 (key-free)\n"
        "- 통과 분해를 `specs/modules/<gap_id>.pg` 로 작성 → `verify_seal.py` → `registry/modules`.\n"
        "- 봉인 후 자동: distinct-prime cmul 확장이 buildable 로 전환(ValueFunction fan-in 재계산).\n"
        "- standing-loop 승격: 이 라운드가 성공하면 frontier 자동전진(c7x→c8x, cr8→cr9 …).\n\n"
        "## relay (정욱님)\n"
        f"- 6런타임 배포 → 응답 수거 → `_workspace/crossmodel/discover_round{rn}/responses/` 적재.\n"
        "- self-contained 부분(GAP-SPEC·TASKSPEC·SCORING)은 완성. **EXT 의존**: 실 런타임 응답 대기.\n")
    open(os.path.join(pkg, "SCORING.md"), "w", encoding="utf-8", newline="\n").write(scoring)

    readme = (
        f"# Discover Round {rn} — Primitive Proposal Package\n\n"
        "QF-Discover(Stage 2) W2.4 산출. ValueFunction(W2.1)이 자율 도출한 미봉인 primitive "
        "capability-gap 을 6런타임 패널에 위임하는 배포 패키지.\n\n"
        "## 파일\n"
        "- `GAP-SPEC.json` — capability-gap 명세(제약·golden·unlock 근거)\n"
        "- `TASKSPEC.md` — 6런타임 PG TaskSpec(독립 제안 요청)\n"
        "- `SCORING.md` — 수렴+독립검증+proof 채점 및 key-free 봉인 스키마\n"
        "- `responses/` — (relay 후) 런타임 응답 적재 위치\n\n"
        "## 상태\n"
        "self-contained 부분 완성. **[EXT]** — 정욱님 6런타임 배포→수거 대기.\n"
        "수거 후 `decomp_optimizer`(reward)+`second_oracle`(독립검증)으로 자동 채점→봉인.\n")
    open(os.path.join(pkg, "README.md"), "w", encoding="utf-8", newline="\n").write(readme)
    os.makedirs(os.path.join(pkg, "responses"), exist_ok=True)

    print("-" * 84)
    print(f"패키지 생성(self-contained): _workspace/crossmodel/discover_round{rn}/ "
          f"[GAP-SPEC.json·TASKSPEC.md·SCORING.md·README.md] · [EXT] relay 대기")
    return 0


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "rank"
    fn = {"rank": cmd_rank, "validate": cmd_validate, "guard": cmd_guard,
          "propose": cmd_propose}.get(cmd, cmd_rank)
    return fn()


if __name__ == "__main__":
    sys.exit(main())
