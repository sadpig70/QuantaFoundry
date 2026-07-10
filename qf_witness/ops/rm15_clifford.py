#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rm15_clifford.py — TrackHE5 P4: RM [[15,1,3]] 인코더 Tier-2 CLIFFORD 봉인 드라이버 (W7.2 선례).

[[15,1,3]] punctured Reed-Muller 코드(15-to-1 magic 증류의 정준 기판, 거리-3 transversal-T):
  큐빗 q(0..14) ↔ 점 v=q+1 ∈ F₂⁴∖0. X-stab = xᵢ 평가(무게 8, 4개) · Z-stab = xᵢ·xᵢxⱼ(4+6=10개).
  논리 X̄' = 짝수좌표무게 점 7개(𝟙⊕Σxᵢ 대표 — 씨앗과 서로소가 되는 열쇠) · Z̄ = {q0,q1,q2}(직선).
★인코더 = **완전 논리-입력 유니터리**(W7.2 가 future work 로 남긴 형태): |x⟩_{q14}|0⟩^{14} → |x̄⟩.
  gates = [입력 fan: CNOT q14→X̄'∖{q14} (6)] + [씨앗 e_i={q0,q1,q3,q7}: H + CNOT→Sᵢ∖{eᵢ} (4+28)]
  — 순서 논거: X̄' 대표가 씨앗과 서로소라 fan 이 씨앗을 오염하지 않음(선검증 확정). 총 38게이트.
봉인 경로(W7.2): verify_seal module-level tier="clifford" — 정준 stabilizer tableau(dense 미사용,
  n=15 정확) → registry/modules (모듈 89→90, 7번째 Tier-2). 오라클 use-only.
코드-정확성 witness(오라클 독립, dense-free) = rm15_observe: 심볼릭 안정군 역전파(코드 안정자 14개
  → +Z_ancilla 군·X̄'→X_{q14}·Z̄→Z-string(q14 포함), Steane 7q 자가대조 포함).

사용: python -m qf_witness.ops.rm15_clifford
"""
from __future__ import annotations
import os, sys, json, subprocess

from qf_witness.core.paths import ROOT
ORACLE = os.path.join(ROOT, ".agents", "skills", "qpgf-oracle", "scripts")
sys.path.insert(0, ORACLE)
import verify_seal as vs        # noqa: E402  (Tier-2 봉인 CLI — 사용만)
import clifford_seal as cs      # noqa: E402  (정준 tableau 독립 재확인 — 사용만)

SPECS_MODS = os.path.join(ROOT, "specs", "modules")
MODREG = os.path.join(ROOT, "registry", "modules")

SEEDS = [0, 1, 3, 7]
S = [[q for q in range(15) if ((q + 1) >> i) & 1] for i in range(4)]
LP = [q for q in range(15) if bin(q + 1).count("1") % 2 == 0]
P0 = 14


def rm15_gates():
    g = [("cnot", P0, t) for t in LP if t != P0]
    for i in range(4):
        g.append(("h", SEEDS[i]))
    for i in range(4):
        for t in S[i]:
            if t != SEEDS[i]:
                g.append(("cnot", SEEDS[i], t))
    return g


def _bloq_code(n, gates):
    L = ["from qualtran import BloqBuilder",
         "from qualtran.bloqs.basic_gates import Hadamard, CNOT",
         "bb = BloqBuilder()",
         f"qs = [bb.add_register(f'q{{i}}', 1) for i in range({n})]"]
    for g in gates:
        if g[0] == "h":
            L.append(f"qs[{g[1]}] = bb.add(Hadamard(), q=qs[{g[1]}])")
        else:
            c, t = g[1], g[2]
            L.append(f"qs[{c}], qs[{t}] = bb.add(CNOT(), ctrl=qs[{c}], target=qs[{t}])")
    L.append(f"bloq = bb.finalize(**{{f'q{{i}}': qs[i] for i in range({n})}})")
    return "\n".join(L)


SPEC_META = {
    "rm15_encoder_t2": ("rm15_encoder_t2 — [[15,1,3]] punctured Reed-Muller **완전 논리-입력 인코더**"
                        "(입력 |x⟩=q14): 15-to-1 magic 증류 정준 기판, 거리-3 transversal-T 코드. "
                        "Tier-2 CLIFFORD(정준 stabilizer tableau). plan=H·CNOT 38게이트, no MatrixGate. "
                        "코드-정확성 witness=rm15_observe(심볼릭 안정군 역전파, 오라클 독립).",
                        lambda: rm15_gates()),
    "rm15_decoder_t2": ("rm15_decoder_t2 — [[15,1,3]] 디코더 = 인코더 역(H·CNOT 자기역, 역순 38게이트). "
                        "★TrackHE6 P1: 15-to-1 magic 증류의 **측정 전 coherent syndrome 추출 코어** — "
                        "부호어(논리 |x̄⟩)를 |x⟩_{q14}|0¹⁴⟩(syndrome) 로 분해, 오류 있는 magic 은 "
                        "syndrome≠0 노출. Tier-2 CLIFFORD. 증류 acceptance(syndrome=0)·성공률=관측. "
                        "witness=distill15_observe(디코더==인코더† dag·부호어→syndrome0, 오라클 독립).",
                        lambda: list(reversed(rm15_gates()))),
}


def gen_spec(name):
    header, gfn = SPEC_META[name]
    return ("# " + header + "\n"
            "```python id=bloq\n" + _bloq_code(15, gfn()) + "\n```\n"
            '```json id=meta\n'
            f'{{"id": "{name}", "n_sys": 15, "n_anc": 0, "tier": "clifford"}}\n'
            "```\n")


def seal_one(name):
    sp = os.path.join(SPECS_MODS, f"{name}.pg")
    open(sp, "w", encoding="utf-8", newline="\n").write(gen_spec(name))
    rc = subprocess.run([sys.executable, os.path.join(ORACLE, "verify_seal.py"), sp,
                         "--out", MODREG], capture_output=True, text=True, cwd=ORACLE).returncode
    seal_path = os.path.join(MODREG, f"{name}.sealed.json")
    if rc != 0 or not os.path.exists(seal_path):
        print(f"[Seal-T2] {name} FAILED rc={rc}")
        return False
    sealed = json.load(open(seal_path, encoding="utf-8"))
    bloq = vs.instantiate(open(sp, encoding="utf-8").read()
                          .split("id=bloq\n")[1].split("```")[0], "bloq")
    indep_hash, _ = cs.canonical_tableau_hash(bloq)
    match = indep_hash == sealed["u_hash"]
    print(f"[Seal-T2] {name} n_sys={sealed['n_sys']} tier={sealed['tier']} "
          f"u_hash={sealed['u_hash'][:14]}.. tableau_recompute_match={match}")
    return match


def main():
    ok = all(seal_one(n) for n in SPEC_META)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
