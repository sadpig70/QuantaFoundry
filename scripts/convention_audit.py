# -*- coding: utf-8 -*-
"""convention_audit.py — Stage 4 W4.1: second_oracle 독립유도 vs 공유가정 감사 (A3 고유통찰).

8-agent 잔여 최약가정(B2): convention 단일문화(big-endian/atol/전역위상)가 *전역 단일실패점*.
second_oracle 은 risk(d)[Qualtran 구성버그]를 닫는다고 주장하나, convention/측정도구는 verify_seal
과 *공유*한다(docstring 라인 8 자인). 본 감사는 그 독립성 경계를 **체계적으로 판정**한다:
어느 차원이 독립유도(numpy 제1원리)이고 어느 차원이 공유가정(endian/phase/atol/hash)인가.

판정 결과는 과장 제거용 — 가정 차원은 "검증 필요" 갭으로 명시 문서화한다.

비파괴: 분석전용. registry/sealed/oracle/frozen 불변. `.pgf/consensus/`·`docs/` 가산.
소비 자산(사용만): second_oracle(INDEP/embed/my_canonical_hash) · verify_seal(hash_unitary).

사용:  python scripts/convention_audit.py
"""
from __future__ import annotations
import os, sys, json, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import second_oracle as so            # noqa: E402  INDEP/embed/my_canonical_hash 사용만
vs = so.vs                            # 공통 측정도구 hash_unitary

MODREG = os.path.join(ROOT, "registry", "modules")
OUT = os.path.join(ROOT, ".pgf", "consensus")
DOCOUT = os.path.join(ROOT, "docs", "CONVENTION-AUDIT.md")


def _nq(gid):
    return int(round(math.log2(so.INDEP[gid]().shape[0])))


def endian_audit(gids):
    """비대칭 multi-qubit 게이트: big-endian embed 가 sealed 와 일치하고 qubit-reversed 는 불일치
    → sealed 가 big-endian convention 에 의존 = second_oracle 도 동일 가정(독립유도 아님)."""
    rows = []
    for gid in gids:
        nq = _nq(gid)
        if nq < 2:
            continue
        sealed_p = os.path.join(MODREG, f"{gid}.sealed.json")
        if not os.path.exists(sealed_p):
            continue
        sealed = json.load(open(sealed_p, encoding="utf-8"))["u_hash"]
        U = so.INDEP[gid]()
        fwd = list(range(nq))
        rev = list(reversed(range(nq)))
        be = vs.hash_unitary(so.embed(U, fwd, nq))
        le = vs.hash_unitary(so.embed(U, rev, nq))
        rows.append({"gid": gid, "nq": nq,
                     "big_endian_matches_sealed": be == sealed,
                     "reversed_differs_from_bigendian": le != be,
                     "endian_sensitive": le != be})
    sensitive = [r for r in rows if r["endian_sensitive"]]
    all_be_match = all(r["big_endian_matches_sealed"] for r in rows)
    return {"rows": rows, "n_checked": len(rows), "n_endian_sensitive": len(sensitive),
            "all_bigendian_match_sealed": all_be_match,
            "verdict": "endian = SHARED ASSUMPTION (big-endian 하드코딩; sealed 가 이에 의존, "
                       "second_oracle 도 동일 convention 가정 → 독립유도 아님)"}


def phase_atol_audit(gids):
    """전역위상/atol 공유 가정 확인 — U vs U·e^{iφ}, U vs U+ε(ε<atol) 동일 hash 여부."""
    phase_inv, atol_inv, my_phase_inv = 0, 0, 0
    n = 0
    for gid in gids:
        U = so.INDEP[gid]()
        n += 1
        if vs.hash_unitary(U) == vs.hash_unitary(U * np.exp(1j * 0.7)):
            phase_inv += 1
        if vs.hash_unitary(U) == vs.hash_unitary(U + 1e-11):   # < QUANT/2(=5e-10) → 격자 흡수
            atol_inv += 1
        if so.my_canonical_hash(U) == so.my_canonical_hash(U * np.exp(1j * 0.7)):
            my_phase_inv += 1
    return {"n": n, "global_phase_invariant": phase_inv, "atol_invariant": atol_inv,
            "my_hash_phase_invariant": my_phase_inv,
            "verdict": "전역위상/atol = SHARED ASSUMPTION (vs.hash_unitary 와 my_canonical_hash 모두 "
                       "전역위상 제거 + 1e-7 round 동일 철학 → canonicalization 공유)"}


def hash_independence_audit(gids):
    """측정 부분독립 측정: 게이트쌍의 동일성 판정이 vs.hash_unitary 와 my_canonical_hash 에서
    일치하는가. 일치=두 측정도구가 같은 동치류를 본다(공유 철학; my 는 독립 구현이라 구현버그는 분리)."""
    items = [(gid, so.INDEP[gid]()) for gid in gids]
    agree, total = 0, 0
    disagreements = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            gi, Ui = items[i]; gj, Uj = items[j]
            if Ui.shape != Uj.shape:
                continue
            total += 1
            vs_eq = vs.hash_unitary(Ui) == vs.hash_unitary(Uj)
            my_eq = so.my_canonical_hash(Ui) == so.my_canonical_hash(Uj)
            if vs_eq == my_eq:
                agree += 1
            else:
                disagreements.append({"a": gi, "b": gj, "vs_eq": vs_eq, "my_eq": my_eq})
    return {"pairs_checked": total, "judgment_agreement": agree,
            "disagreements": disagreements[:10],
            "verdict": f"vs.hash_unitary ↔ my_canonical_hash 판정 일치 {agree}/{total} — 측정 동치류 "
                       "공유(독립 구현이나 동일 canonicalization 철학; 구성버그는 분리, convention 버그는 공동)"}


def main():
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.dirname(DOCOUT), exist_ok=True)
    gids = list(so.INDEP.keys())
    print("=" * 84)
    print("ConventionIndependenceAudit (W4.1) — second_oracle 독립유도 vs 공유가정 판정")
    print("=" * 84)

    ea = endian_audit(gids)
    pa = phase_atol_audit(gids)
    ha = hash_independence_audit(gids)

    print(f"\n[Endian] multi-q {ea['n_checked']} 검사 · endian-sensitive {ea['n_endian_sensitive']} · "
          f"big-endian 전부 sealed 일치={ea['all_bigendian_match_sealed']}")
    print(f"   판정: {ea['verdict']}")
    print(f"\n[Phase/atol] {pa['n']} 게이트 · 전역위상불변 {pa['global_phase_invariant']}/{pa['n']} · "
          f"atol불변 {pa['atol_invariant']}/{pa['n']}")
    print(f"   판정: {pa['verdict']}")
    print(f"\n[Hash독립] 쌍 {ha['pairs_checked']} · 판정일치 {ha['judgment_agreement']} · "
          f"불일치 {len(ha['disagreements'])}")
    print(f"   판정: {ha['verdict']}")

    matrix = [
        {"dimension": "유니터리 구성", "verdict": "INDEPENDENT",
         "basis": "numpy 제1원리 (qualtran/spec-golden 미실행) — risk(d) 구성버그 차단"},
        {"dimension": "endian convention", "verdict": "SHARED ASSUMPTION",
         "basis": f"embed big-endian 하드코딩; sealed 의존; endian-sensitive {ea['n_endian_sensitive']}건"},
        {"dimension": "전역위상", "verdict": "SHARED ASSUMPTION",
         "basis": f"vs+my 모두 전역위상 제거 ({pa['global_phase_invariant']}/{pa['n']})"},
        {"dimension": "atol(1e-7)", "verdict": "SHARED ASSUMPTION",
         "basis": f"양 측정 동일 round ({pa['atol_invariant']}/{pa['n']})"},
        {"dimension": "canonical hash", "verdict": "SHARED (부분독립 측정)",
         "basis": f"vs↔my 판정일치 {ha['judgment_agreement']}/{ha['pairs_checked']}; 구현분리·철학공유"},
    ]
    gap = ("second_oracle 은 *유니터리 구성*을 독립화해 risk(d)[Qualtran 구성/canonicalization 버그]를 "
           "닫는다. 그러나 endian·전역위상·atol·hash canonicalization 은 verify_seal 과 **공유 가정**이다. "
           "따라서 convention 단일문화(big-endian/atol/전역위상)에 *공통 버그*가 있으면 second_oracle 도 "
           "같이 통과한다 — 이 축은 미차단 단일실패점. 닫으려면 독립 convention(예: little-endian 재유도 + "
           "교차대조) 또는 형식증명(consensus.proof_*)이 필요. 현재는 명시된 갭(검증 필요).")

    out = {"_schema": "convention-audit-v1",
           "independence_matrix": matrix, "endian": ea, "phase_atol": pa, "hash_independence": ha,
           "gap": gap,
           "_note": "분석전용 비파괴. second_oracle 독립성 경계의 정직 판정 — 과장 제거. "
                    "구성=독립(risk d 차단), convention/측정=공유가정(미차단 갭 명시)."}
    json.dump(out, open(os.path.join(OUT, "CONVENTION-AUDIT.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    # 갭 문서
    doc = ["# Convention Independence Audit (Stage 4 W4.1)\n",
           "> second_oracle 의 독립성 경계 정직 판정. 분석전용 비파괴.\n",
           "## 판정 매트릭스\n", "| 차원 | 판정 | 근거 |", "|---|---|---|"]
    for m in matrix:
        doc.append(f"| {m['dimension']} | **{m['verdict']}** | {m['basis']} |")
    doc += ["\n## 갭 (검증 필요 — 과장 제거)\n", gap,
            "\n## 닫는 경로\n",
            "- 독립 convention 재유도: little-endian 으로 재구성 후 big-endian 과 교차대조.",
            "- 형식증명 축: `consensus.proof_*`(corpus 무관 독립축)로 PROOF_BACKED 보강.",
            "- 본 감사는 risk(d) *구성버그* 차단은 유효함을 확인하고, *convention 버그* 축만 갭으로 남긴다.\n"]
    open(DOCOUT, "w", encoding="utf-8", newline="\n").write("\n".join(doc))

    print("\n" + "-" * 84)
    print("판정: 구성=INDEPENDENT(risk d 차단) · convention(endian/phase/atol/hash)=SHARED ASSUMPTION(갭)")
    print(f"→ .pgf/consensus/CONVENTION-AUDIT.json · docs/CONVENTION-AUDIT.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
