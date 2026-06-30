# C12xFrontier Design @v:1.0

## Gantree

```text
C12xFrontier // W12.21 c12x primitive + cmul2_mod3683 payoff only (done) @v:1.0
    SealPrimitive // seal c12x Tier-0 exact module (done)
    SealPayoff // seal cmul2_mod3683 Tier-0 exact app (done) @dep:SealPrimitive
    IntegrateRegistry // connect genskills/reproduce/registry layers (done) @dep:SealPayoff
    VerifyBoundary // full regression and honesty-boundary verification (done) @dep:IntegrateRegistry
    UpdateBacklog // handoff/remain/task_record update and next candidate selection (done) @dep:VerifyBoundary
```

## PPR

```python
def seal_primitive() -> dict:
    """Seal c12x through the qpgf oracle."""
    # input: specs/modules/c12x.pg generated from MultiControlX(cvs=(1,)*12)
    # process: verify_seal.py -> registry/modules/c12x.sealed.json
    # criteria:
    #   - sealed=True
    #   - tier=0
    #   - n_sys=13
    #   - independent cnx_perm(12) u_hash matches sealed u_hash
```

```python
def seal_payoff() -> dict:
    """Seal one representative c12x-consuming modular multiplier app."""
    # input: N=3683=29*127, a=2, nq=13
    # process:
    #   gen_modmul cap extends to c12x
    #   MMD plan permutation == independent arithmetic permutation
    #   fast exact permutation C-app seal writes cmul2_mod3683
    # criteria:
    #   - cmul2_mod3683 sealed=True
    #   - tier=0
    #   - max_control=12
    #   - deps include c12x
    #   - independent arithmetic u_hash matches sealed u_hash
```

```python
def verify_boundary() -> dict:
    """Verify regression and keep scope honest."""
    # criteria:
    #   - no payoff family in this node
    #   - no shor3683 in this node
    #   - reproduce_all == REPRODUCED
    #   - second_oracle, seal_gate_ci, verify_contested_guard pass
    #   - genskills verify INTACT
    #   - qpgf oracle fingerprints byte-identical
```
