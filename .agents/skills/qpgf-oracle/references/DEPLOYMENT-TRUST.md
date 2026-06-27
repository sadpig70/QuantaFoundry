# DEPLOYMENT-TRUST — QPGF Oracle Deployment Trust Model

This document closes the last assumption behind seal integrity:

```text
the verifier must know that the oracle bundle itself is authentic
```

Current repository status:

- manifest and integrity gates exist;
- `BUNDLE.sha256` can be verified;
- release signing is wired via **Sigstore keyless CI** (`.github/workflows/release.yml`, no
  private key) and verified by `verify_bundle.py`; GPG is an offline alternative (Option A).

## Threat Model

| Threat | Current Defense | Residual Risk |
|---|---|---|
| field tampering inside `sealed.json` | deterministic `sig` over canonical fields | none if trusted verifier is used |
| seal produced by a different oracle bundle | code fingerprints plus provenance check | requires a trusted local bundle |
| partial bundle tampering | `BUNDLE.sha256` manifest | none if manifest is trusted |
| coherent replacement of the whole bundle and manifest | self-checks still pass | requires external signature |

The critical point:

```text
self-checks cannot prove the bundle's origin
```

They prove only internal consistency. An external trust anchor is required for releases.

## Trust Chain

```text
trusted channel:
  maintainer public-key fingerprint
  or Sigstore identity

then:
  verify BUNDLE.sha256 against the working tree
  verify BUNDLE.sha256 signature
  only then trust verify_seal output
```

Judgments:

| Verdict | Meaning |
|---|---|
| `TRUSTED` | manifest matches and signature is valid |
| `INTEGRITY_ONLY` | manifest matches but no trusted signature is required or present |
| `UNTRUSTED_SIGNATURE` | signature check failed or signer is not trusted |
| `TAMPERED` | manifest does not match current files |

Deployment verifiers should use `--require-signature` for release trust.

## Option A — GPG

Maintainer setup:

```bash
gpg --full-generate-key
gpg --fingerprint
```

Publish the fingerprint out of band.

For every release:

```bash
python scripts/bundle_manifest.py
gpg --detach-sign --armor -o BUNDLE.sha256.asc BUNDLE.sha256
```

Verifier:

```bash
gpg --import maintainer-public-key.asc
python scripts/verify_bundle.py --require-signature
```

## Option B — Sigstore / Cosign  (realized via CI)

Keyless signing with GitHub Actions OIDC plus the Rekor transparency log — **no long-lived
private key**. This is wired up: `.github/workflows/release.yml` signs `BUNDLE.sha256` on every
version tag (`v*`) and publishes `BUNDLE.sha256.sig` + `BUNDLE.sha256.pem` as release assets.

Verify (anyone, from the release assets):

```bash
cosign verify-blob \
  --certificate BUNDLE.sha256.pem \
  --signature BUNDLE.sha256.sig \
  --certificate-identity-regexp 'https://github.com/sadpig70/QPGF/.*' \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com \
  BUNDLE.sha256
# then the gate (cosign path is built in):
python scripts/verify_bundle.py --require-signature   # -> TRUSTED
```

`verify_bundle.py` checks the cosign signature automatically when `BUNDLE.sha256.sig` +
`.pem` are present (identity/issuer overridable via `QPGF_COSIGN_IDENTITY_REGEXP` /
`QPGF_COSIGN_ISSUER`). Pros: no key custody, auditable, SLSA-aligned. Cons: needs CI + (for
verification) network access to the transparency log.

## Option C — Reproducible Source Tree

This bundle is pure source. A clean checkout should reproduce the same manifest:

```bash
python scripts/bundle_manifest.py
python scripts/bundle_manifest.py --verify
```

Pinned dependencies in `DEPENDENCIES.lock` help reproduce the runtime environment, but dependency trust remains a separate concern.

## Honest Limits

- Trust is not eliminated. It is moved from local mutable files to an external public key, transparency log, CI identity, or equivalent anchor.
- `verify_bundle.py` is itself part of the bundle. Bootstrap trust comes from the external signature and trusted key, not from trusting the script blindly.
- If no release signature is configured, the bundle can still be useful for development, but the correct verdict is `INTEGRITY_ONLY`, not `TRUSTED`.

## Recommended Release Gate

```bash
python scripts/bundle_manifest.py --verify
python scripts/verify_bundle.py --require-signature
python scripts/test_bundle_manifest.py
python scripts/test_verify_bundle.py
```

Only after this should downstream users treat seals from the bundle as release-trusted.
