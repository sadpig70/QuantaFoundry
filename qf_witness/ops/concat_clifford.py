#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""concat_clifford.py — TrackHE7 P6: 부호 연접(concatenation) [[25,1,9]] Tier-2 CLIFFORD 봉인 드라이버.

concat_513_513 = [[5,1,3]] ∘ [[5,1,3]] = [[25,1,9]] (25q, 거리 9):
  §3i 관문("concatenation 은 아직 없음") 개창 — registry 첫 부호-간 조립(연접) 계층.
  ★자기연접(대칭·양자 완전 부호): 거리 9 = d_outer·d_inner = 3·3 (concatenation 정리).
인코더(전부 code513_encoder 게이트 시퀀스 = CNOT×4·H×5·CZ ring 5, sub-app ×6 대량 복리, §4′g):
  block b(0..4) = wires {5b..5b+4}, 대표 = {0,5,10,15,20}.
  step1(outer): code513 on 대표 [0,5,10,15,20] — 논리입력 wire 0, 대표 4개는 |0⟩.
  step2(inner): 각 블록 [5b..5b+4] 에 code513 — 대표 5b 가 논리입력(outer 부호어의 b번째 physical),
                블록 내 나머지 4 wire 는 |0⟩. → 대표를 논리입력으로 재인코딩.
  = 84게이트(6×14). 전-Clifford → Tier-2 정준 stabilizer tableau 로 exact(dense 2^25 불필요).
봉인 경로(W7.2/rm15 선례): verify_seal module-level tier="clifford"(dense 미사용, n=25 정확)
  → registry/modules. 오라클 use-only. 독립 재확인 = clifford_seal.canonical_tableau_hash.
코드-정확성 witness(오라클 독립, dense-free) = concat_observe: 심볼릭 안정군 역전파(24 stab =
  20 inner-block + 4 outer-lift, 연접 정리 구조 exact 대조 + 논리 X̄/Z̄ 최소무게 9 관측).

정직 경계(seal 아님): 봉인 = 연접 인코더 stabilizer 구조 exact(Tier-2)뿐. 거리 9 달성·임계값·
  디코드·오류율 = 관측/범위밖. 신규 module 0(bloq 기본 게이트만).

사용: python scripts/concat_clifford.py
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


def code513_gates(w):
    """[[5,1,3]] 오각형 graph-code 인코더 게이트(로컬 0..4 → 물리 wires w). CNOT×4·H×5·CZ ring 5."""
    a, b, c, d, e = w
    return [("cnot", a, b), ("cnot", a, c), ("cnot", a, d), ("cnot", a, e),
            ("h", a), ("h", b), ("h", c), ("h", d), ("h", e),
            ("cz", a, b), ("cz", b, c), ("cz", c, d), ("cz", d, e), ("cz", e, a)]


def concat_gates():
    reps = [0, 5, 10, 15, 20]
    g = code513_gates(reps)                       # step1: outer on 대표
    for blk in range(5):                          # step2: inner on 각 블록
        g += code513_gates([5 * blk + k for k in range(5)])
    return g


def _bloq_code(n, gates):
    L = ["from qualtran import BloqBuilder",
         "from qualtran.bloqs.basic_gates import Hadamard, CNOT, CZ",
         "bb = BloqBuilder()",
         f"qs = [bb.add_register(f'q{{i}}', 1) for i in range({n})]"]
    for g in gates:
        if g[0] == "h":
            L.append(f"qs[{g[1]}] = bb.add(Hadamard(), q=qs[{g[1]}])")
        elif g[0] == "cnot":
            c, t = g[1], g[2]
            L.append(f"qs[{c}], qs[{t}] = bb.add(CNOT(), ctrl=qs[{c}], target=qs[{t}])")
        elif g[0] == "cz":
            a, b = g[1], g[2]
            L.append(f"qs[{a}], qs[{b}] = bb.add(CZ(), q1=qs[{a}], q2=qs[{b}])")
        else:
            raise ValueError(g)
    L.append(f"bloq = bb.finalize(**{{f'q{{i}}': qs[i] for i in range({n})}})")
    return "\n".join(L)


HEADER = ("concat_513_513 — 부호 연접 [[5,1,3]]∘[[5,1,3]] = [[25,1,9]] **완전 인코더**(논리입력 wire 0): "
          "§3i concatenation 계층 개창, 거리 9 = 3·3(연접 정리). Tier-2 CLIFFORD(정준 stabilizer tableau, "
          "dense 2^25 불필요). plan=code513_encoder 게이트 ×6 복리 = CNOT·H·CZ 84게이트, no MatrixGate, "
          "신규 module 0. 코드-정확성 witness=concat_observe(심볼릭 안정군 역전파 24 stab, 오라클 독립).")


def gen_spec():
    return ("# " + HEADER + "\n"
            "```python id=bloq\n" + _bloq_code(25, concat_gates()) + "\n```\n"
            '```json id=meta\n'
            '{"id": "concat_513_513", "n_sys": 25, "n_anc": 0, "tier": "clifford"}\n'
            "```\n")


def seal_one():
    name = "concat_513_513"
    sp = os.path.join(SPECS_MODS, f"{name}.pg")
    open(sp, "w", encoding="utf-8", newline="\n").write(gen_spec())
    rc = subprocess.run([sys.executable, os.path.join(ORACLE, "verify_seal.py"), sp,
                         "--out", MODREG], capture_output=True, text=True, cwd=ORACLE).returncode
    seal_path = os.path.join(MODREG, f"{name}.sealed.json")
    if rc != 0 or not os.path.exists(seal_path):
        print(f"[Seal-T2] {name} FAILED rc={rc}")
        return False
    sealed = json.load(open(seal_path, encoding="utf-8"))
    bloq = vs.instantiate(open(sp, encoding="utf-8").read()
                          .split("id=bloq\n")[1].split("```")[0], "bloq")
    indep_hash, n = cs.canonical_tableau_hash(bloq)
    match = indep_hash == sealed["u_hash"]
    print(f"[Seal-T2] {name} n_sys={sealed['n_sys']} tier={sealed['tier']} n_qubits={n} "
          f"u_hash={sealed['u_hash'][:14]}.. tableau_recompute_match={match}")
    return match


def main():
    return 0 if seal_one() else 1


if __name__ == "__main__":
    sys.exit(main())
