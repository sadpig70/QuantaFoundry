"""forge_apps.py — F3_Compose: 봉인된 베이스 모듈을 재조립해 상위 앱을 C-app 봉인.

봉인 누적의 복리(비선형 생산력) 실증: 이미 신뢰된 15개 모듈(specs/modules)을 plan 으로 합성하면
오라클(app_assemble, 사용만)이 합성품==app_golden(C-app) 대조 후 재봉인한다. 새 검증 비용은
'합성이 의도와 같은가'뿐 — 부품 정확성은 이미 지불됨(INV2).

재발견(rediscovery) 앱: cz·ccz·swap 을 *다른 모듈*의 조립으로 재구성 → 그 u_hash 가 독립적으로
cross-model 봉인된 게이트와 byte 일치함을 단언. 전체 스택(베이스 게이트 ⊕ 합성기 ⊕ 오라클)의 일관성 증명.

사용:  python .pgf/autoforge/forge_apps.py
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SCRIPTS = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, SCRIPTS)
import app_assemble as aa              # noqa: E402  (오라클 — 사용만)

APPS = os.path.join(ROOT, "specs", "apps")
STORE = os.path.join(ROOT, "registry", "apps")
MOD_REG = os.path.join(ROOT, "registry", "modules")

# 앱 목록 (적용순) + 재발견 단언 대상(있으면 그 봉인 게이트와 u_hash 일치해야)
APP_LIST = [
    ("bell.app.pg",             None),
    ("ghz3.app.pg",             None),
    ("ghz4.app.pg",             None),
    ("ghz5.app.pg",             None),    # goal-autonomy 자율 생성 (family extension, human seed 0)
    ("ghz6.app.pg",             None),    # goal-autonomy 자율 생성 (compounding 실증)
    ("cz_rediscovered.app.pg",  "cz"),
    ("ccz_rediscovered.app.pg", "ccz"),
    ("swap_via_cnot.app.pg",    "swap2"),
    # F3 확장 (§5b): 재귀 sub-app 트리 · 실앱(Grover) · Tier-1 대규모
    ("reflect00.app.pg",         None),
    ("diffusion.app.pg",         None),   # reflect00 을 sub-app 재귀 참조
    ("grover2.app.pg",           None),   # 3레벨 트리: grover2→diffusion→reflect00, oracle=재사용 cz
    ("ghz16_structural.app.pg",  None),   # Tier-1 Merkle, 16q dense 미실체화
    # F3 확장 (§5c): QFT pipeline — 첫 비자명 알고리즘 분해, cross-model 게이트 실투입
    ("qft2_pipeline.app.pg",     "qft2"),  # h·cs·swap → 봉인 qft2 재발견
    ("qft3_pipeline.app.pg",     "qft3"),  # h·cs·ct·swap → 봉인 qft3 재발견 (ct_gate 첫 사용)
    # F3 확장 (§5d): QPE — 최초 다중레지스터 실알고리즘
    ("iqft2.app.pg",             None),    # inverse QFT2 (cs_dag 투입), QPE 빌딩블록
    ("qpe_s.app.pg",             None),    # QPE(S): 2 counting+1 target, iqft2 sub-app 재귀
    # F3 확장 (§5e): controlled-Rk 일반화 → qft4 pipeline (16×16, cr4 첫 투입)
    ("qft4_pipeline.app.pg",     "qft4"),  # h·cs(CR2)·ct(CR3)·cr4(CR4)·swap → 봉인 qft4 재발견
    # F3 확장 (§5f): 큰 정밀도 QPE — t=3 counting, inverse-QFT3
    ("iqft3.app.pg",             None),    # inverse QFT3 (cr3_dag 투입), 큰 QPE 빌딩블록
    ("iqft7.app.pg",             None),    # inverse QFT7 (cr5/6/7_dag), Shor-21 counting register
    ("qpe_t.app.pg",             None),    # QPE(T) t=3: 고유위상 1/8=0.001₂, iqft3 sub-app 재귀
    # F3 확장 (§5g): Shor 주기발견 — modular mult를 sealed Fredkin으로 정직 분해
    ("cmul2_mod15.app.pg",       None),    # controlled ×2 mod15 = controlled 좌순환1 (Fredkin ×3)
    ("cmul4_mod15.app.pg",       None),    # controlled ×4 mod15 = cmul2 ∘ cmul2 (재귀)
    ("shor15_a2.app.pg",         None),    # 최초 완전 Shor(N=15,a=2): 7q, cmul·iqft3 재귀 트리
    # F3 확장 (§5l): Shor base 독립성 — a=7 (비-shift base). ×7=NOT∘rot3 정직 분해(CNOT 첫 modular-mult 투입)
    ("cmul7_mod15.app.pg",       None),    # controlled ×7 mod15 = NOT∘rot3 (Fredkin ×3 + CNOT ×4)
    ("shor15_a7.app.pg",         None),    # 완전 Shor(N=15,a=7): cmul4(재사용)·cmul7(신규)·iqft3, r=4 → 3×5
    # F3 확장 (§5l-2): N=21 진짜 modular arithmetic — N≠2^k-1 이라 carry/reduction 강제. reversible synth → c{3,4,5}x.
    ("cmul2_mod21.app.pg",       None),    # controlled ×2 mod21 (66 gates, {toffoli,c3x,c4x,c5x}) — Shor-21 U^1, 진짜 산술
    ("cmul4_mod21.app.pg",       None),    # controlled ×4 mod21 = cmul2² (복리 재사용)
    ("cmul16_mod21.app.pg",      None),    # controlled ×16 mod21 = cmul4² — Shor-21 controlled-U^{2^j} 패밀리
]


def _sealed_key(mid):
    p = os.path.join(MOD_REG, f"{mid}.sealed.json")
    return json.load(open(p, encoding="utf-8"))["u_hash"] if os.path.exists(p) else None


def main():
    os.makedirs(STORE, exist_ok=True)
    print("=" * 84)
    print("QuantaFoundry F3_Compose — 봉인 모듈 재조립 → C-app 봉인 (신뢰 자본 복리)")
    print("=" * 84)
    results, ok, redisc_ok = [], 0, 0
    for fname, redisc in APP_LIST:
        v = aa.assemble(os.path.join(APPS, fname), STORE)
        rec = {"app": fname[:-7], "sealed": v.sealed, "tier": v.tier,
               "u_hash": v.u_hash, "reason": v.reason, "rediscovers": redisc}
        if v.sealed:
            ok += 1
            assertion = ""
            if redisc:
                want = _sealed_key(redisc)
                match = (v.u_hash == want)
                rec["rediscovery_match"] = match
                if match:
                    redisc_ok += 1
                assertion = f"  ⟺ {redisc}: {'✓일치' if match else '✗불일치!'}"
            icon = "✅"
            print(f"  {icon} {rec['app']:18} SEALED  tier={v.tier}  u_hash={v.u_hash[:14]}..{assertion}")
        else:
            print(f"  ❌ {rec['app']:18} REJECT  {v.reason[:50]}")
        results.append(rec)

    print("=" * 84)
    redisc_total = sum(1 for _, r in APP_LIST if r)
    print(f"앱 봉인 {ok}/{len(APP_LIST)} · 재발견 교차검증 {redisc_ok}/{redisc_total} 일치 · store=registry/apps")
    print("=" * 84)
    rep = os.path.join(HERE, "FORGE-APPS-RESULT.json")
    json.dump({"results": results, "sealed": ok, "total": len(APP_LIST),
               "rediscovery_ok": redisc_ok, "rediscovery_total": redisc_total},
              open(rep, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    all_ok = ok == len(APP_LIST) and redisc_ok == redisc_total
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
