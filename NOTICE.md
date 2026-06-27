# NOTICE

QuantaFoundry is released under the MIT License (see `LICENSE`), © 2026 Jung Wook Yang.

## Vendored component — QPGF oracle

`.agents/skills/qpgf-oracle/` is a **vendored copy** of the QPGF termination oracle, used as-is
(never re-implemented or modified inside this repository):

- Upstream: **https://github.com/sadpig70/QPGF** (v0.1.0)
- License: MIT (same author)
- Integrity: every file is hashed in `.agents/skills/qpgf-oracle/BUNDLE.sha256`; pinned
  dependencies are in `DEPENDENCIES.lock`.

QuantaFoundry **uses** this oracle (calls `verify_seal` / `registry` / `app_assemble`) and does not
alter its verification logic. The seal's provenance fields (`oracle_code_hash`,
`contracts_code_hash`) bind every seal to the exact oracle code that produced it.

## Cross-model evidence

`_workspace/crossmodel/` contains submissions independently authored by external AI runtimes
(OpenAI GPT-5, Google Gemini, xAI Grok, Moonshot Kimi, Alibaba Qwen, DeepSeek) for the purpose of
key-free consensus establishment. These are reproduction artifacts for the claims in
`docs/QuantaFoundry-Technical-Spec.md` §8.2–8.6; each submission carries its `runtime` and
`weights_id` for provenance. No proprietary model internals are included — only the authored
quantum-gate/application matrices, generating numpy snippets, and circuits.
