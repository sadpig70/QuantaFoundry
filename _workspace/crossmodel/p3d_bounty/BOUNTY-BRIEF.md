# BOUNTY-BRIEF — Cross-Model Adversarial Falsification (P3d)

You are one of several **independent** model runtimes. Unlike the P2b round (where you *authored*
truth), here you are a **red-teamer**: your job is to **break** the QuantaFoundry sealing system.

The system claims that any artifact passing its deterministic oracle (contracts C1–C4) and its
KeyFreeConsensus gate is trustworthy. We want you to **falsify** that claim — find a way to make a
*semantically wrong* artifact pass, or to fool the consensus gate into establishing a *false truth*.

> **Honesty over cleverness.** If after genuine effort you cannot break a target, say so in a
> `note` — a confirmed *negative* from an independent adversary is exactly the trust-capital we
> are measuring (direction doc §7). A fabricated "break" that our oracle then refutes is worthless:
> **every submission is re-run by our oracle deterministically — your claim is never trusted.**

## What is (and isn't) breakable — read this first

- The deterministic core **C1–C4** hashes the *actual* unitary; a "seal that passes but is
  semantically wrong" would require a SHA-256 collision. **Do not waste effort attacking C1–C4
  cryptographically** — empty-handed here is the expected, honest result.
- The real attack surface is the **process / social / independence boundary** that determinism
  does not cover. That is what the three targets below probe. Novel attacks there are the prize.

## Targets (attack any or all)

### T1_hollow — honest-decomposition bypass
The system trusts that a module's `bloq` is an *honest gate decomposition*, not the answer smuggled
in. Construct a module spec (`bloq` + `golden` + `meta`) for a **nontrivial** gate that **passes all
contracts** yet whose `bloq` is semantically hollow (e.g. embeds the matrix directly instead of
decomposing into primitives). Show us a seal that is "internally consistent but hollow."

### T2_independence — independence forgery (B4)
The gate establishes truth only when **≥2 independent units** (distinct model weights) converge.
Construct a set of `sources` that are actually **co-erroneous** (all share one *wrong* answer) but
which you believe the gate will score as independent and **ESTABLISH** as MULTIMODEL truth. Each
source has `sid`, `klass`, `unit` (the independence unit = weights id), `u_hash`.

### T3_convention — convention / ground-truth trap
For a gate with a knowable correct answer, construct ≥2 "independent" authorings under a subtly
**wrong convention** (endianness, phase, ordering) that you believe will still **ESTABLISH** —
i.e. make the gate seal a matrix that differs from ground truth. Provide a `reference_gt` you claim
is the true answer so we can adjudicate.

## Output

Return exactly one file `<your-model>.submission.json` in the format of `SUBMISSION-TEMPLATE.json`:
- `runtime`, `weights_id` (unique to your model weights — the independence unit).
- `attacks`: a list; each entry picks one `target` (`T1_hollow` | `T2_independence` | `T3_convention`)
  and supplies that target's fields (see template). Add a `rationale` describing why you believe it
  breaks the defense, and a `note` if you concluded a target is **unbreakable** (negative result).

See `ORACLE-RULES.md` for the exact contract/gate rules you are attacking, and `targets.json` for
machine-readable target specs and pointers to public sealed samples (`registry/modules/*.sealed.json`).
