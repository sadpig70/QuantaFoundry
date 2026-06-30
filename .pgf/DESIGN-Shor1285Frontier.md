# Shor1285Frontier Design @v:1.0

## Gantree

```text
Shor1285Frontier // W12.19 c11x payoff to Shor-1285 structural app (done) @v:1.0
    VerifyChildrenSealed // cmul{2,4,16,256}_mod1285 family already Tier-0 exact (done)
        IndependentArithCheck // rebuild each multiplier permutation, match sealed u_hash 4/4 (done)
        ChildrenPresence // cmul family + iqft8 apps + h_gate module all sealed (done)
    AssembleStructuralShor // shor1285 Tier-1 structural app (done) @dep:VerifyChildrenSealed
    VerifyRegression // registry and global regression gates (done) @dep:AssembleStructuralShor
    UpdateBacklog // HANDOFF/remain/task_record/master current-state update (done) @dep:VerifyRegression
```

## PPR

```python
def verify_children_sealed() -> dict:
    """The N=1285 multiplier family is already sealed by W12.17/W12.18; do not re-seal."""
    powers = [2, 4, 16, 256]
    # deterministic code path (no re-seal):
    #   rebuild controlled modular-multiplier permutation from arithmetic (dim 2^12)
    #   hash via verify_seal.hash_unitary
    # acceptance_criteria:
    #   - independent arithmetic u_hash matches sealed u_hash for 4/4 powers
    #   - each sealed app has tier == 0
    #   - cmul family + iqft8 apps and h_gate module all present
    return {"powers": powers}


def assemble_structural_shor() -> dict:
    """Assemble H^8 · controlled-U^(2^j) · iqft8 as Tier-1 structural at n_sys=19."""
    powa = [1, 1, 1, 1, 256, 16, 4, 2]
    # acceptance_criteria:
    #   - all h_gate/iqft8/cmul children are sealed
    #   - target widths and placements match n_sys=19 (counting=8, work=11)
    #   - structural hash is deterministic on reassembly
    #   - period/factor readout is explicitly illustrative, not seal evidence
    #     (ord_1285(2)=16 -> 2^8 mod 1285 = 256 -> factors [5, 257])
    return {"powa": powa, "tier": 1, "n_sys": 19}
```

## Honesty boundary

- The four `cmul*_mod1285` apps carry the exact Tier-0 (`C1-C4(app)`) claims; they were
  sealed in W12.17 (`cmul2`) and W12.18 (`cmul4/16/256`) and are only re-verified here,
  never rewritten.
- `shor1285` is Tier-1 STRUCTURAL (`C1-C4(structural)`); 19q > EXACT_BOUND so dense
  whole-unitary equivalence is **not** claimed.
- The period/factor readout is illustrative only; it is not seal evidence.
