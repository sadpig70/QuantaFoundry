# scripts/ — permanent compatibility shims

The verification bodies live in **`qf_witness/<category>/`** (observe · family · verify ·
frontier · seal · registry · export · ops) since the 2026-07 restructuring. Every
`python scripts/<name>.py [args]` command keeps working forever through a 14-line shim
(runpy delegation; importing a shim as a module transparently resolves to the package body).

- Add a **new** verification script under `qf_witness/<cat>/` and generate its shim with
  `python tools/gen_shims.py <name>` (category from `verification/manifests/_move_map.json`).
- `structure_lint` (in the reproduce witness batch) enforces: shims-only in scripts/,
  no ROOT depth-trap patterns in qf_witness/, no qpgf-oracle copies.
- Thin entry points that are not shims: `reproduce_all.py` (wrapper → qf_verify),
  `reproduce_all_legacy.py` (preserved legacy), `qf_stdlib.py` (qf_stdlib CLI).
